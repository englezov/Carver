from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isclose, isfinite
from numbers import Integral, Real

from .m0 import CompletedBar, LaneClass, SourceRuleStatus, CarverBlocked, require_finite_positive, require_non_empty_text, require_source_native
from .m1 import TimedValue
from .m2 import FORECAST_CAP, cap_forecast


class S11ForecastStyle(StrEnum):
    TREND = "TREND_DIVERGENT"
    CARRY = "CARRY_CONVERGENT"


S11_SOURCE_STYLE_WEIGHTS = {
    S11ForecastStyle.TREND: 0.60,
    S11ForecastStyle.CARRY: 0.40,
}


@dataclass(frozen=True)
class S11CombinedCarryTrendSourceLocks:
    s09_input_provenance_status: SourceRuleStatus
    s10_input_provenance_status: SourceRuleStatus
    style_grouping_status: SourceRuleStatus
    style_mix_status: SourceRuleStatus
    top_down_weight_status: SourceRuleStatus
    eligible_rule_set_status: SourceRuleStatus
    fdm_status: SourceRuleStatus
    combined_cap_status: SourceRuleStatus
    output_boundary_status: SourceRuleStatus

    def validate(self) -> None:
        for name, status in (
            ("S09 input provenance", self.s09_input_provenance_status),
            ("S10 input provenance", self.s10_input_provenance_status),
            ("S11 style grouping", self.style_grouping_status),
            ("S11 style mix", self.style_mix_status),
            ("S11 top-down forecast weight", self.top_down_weight_status),
            ("S11 eligible rule set", self.eligible_rule_set_status),
            ("S11 FDM", self.fdm_status),
            ("S11 combined cap", self.combined_cap_status),
            ("S11 output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"{name} source is unresolved")


@dataclass(frozen=True)
class S11SyntheticForecastInput:
    label: str
    rule_id: str
    style: S11ForecastStyle
    capped_forecast: TimedValue
    input_status: SourceRuleStatus
    style_weight: float
    rule_weight: float
    variation_weight: float
    weight_status: SourceRuleStatus

    @property
    def top_down_weight(self) -> float:
        return self.style_weight * self.rule_weight * self.variation_weight

    def validate(self, completed_bar: CompletedBar) -> None:
        require_non_empty_text("S11 synthetic input label", self.label)
        require_non_empty_text("S11 forecast rule id", self.rule_id)
        if not self.label.startswith("synthetic_"):
            raise CarverBlocked("S11 input label must be synthetic")
        if self.input_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S11 forecast input source is unresolved")
        if self.weight_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S11 top-down weight source is unresolved")
        if self.capped_forecast.as_of != completed_bar.timestamp:
            raise CarverBlocked("S11 forecast input timestamp is not aligned to completed bar")
        _require_finite("S11 capped forecast input", self.capped_forecast.value)
        if abs(float(self.capped_forecast.value)) > FORECAST_CAP:
            raise CarverBlocked("S11 forecast input must already be capped")
        require_finite_positive("S11 style weight", self.style_weight)
        require_finite_positive("S11 rule weight", self.rule_weight)
        require_finite_positive("S11 variation weight", self.variation_weight)
        if self.style not in S11_SOURCE_STYLE_WEIGHTS:
            raise CarverBlocked("S11 forecast style is unresolved")
        if not isclose(self.style_weight, S11_SOURCE_STYLE_WEIGHTS[self.style], rel_tol=0.0, abs_tol=1e-12):
            raise CarverBlocked("S11 style weight does not match locked style mix")
        if self.style is S11ForecastStyle.TREND and not self.rule_id.startswith("EWMAC"):
            raise CarverBlocked("S11 trend input must use an S09 EWMAC rule id")
        if self.style is S11ForecastStyle.CARRY and not self.rule_id.startswith("Carry"):
            raise CarverBlocked("S11 carry input must use an S10 Carry rule id")


@dataclass(frozen=True)
class S11CombinedForecastRuleResult:
    rule_id: str
    style: S11ForecastStyle
    input_capped_forecast: float
    style_weight: float
    rule_weight: float
    variation_weight: float
    top_down_weight: float


@dataclass(frozen=True)
class S11CombinedCarryTrendConformanceRequest:
    completed_bar: CompletedBar
    forecast_inputs: tuple[S11SyntheticForecastInput, ...]
    eligible_rule_ids: tuple[str, ...]
    s11_fdm: float
    fdm_rule_count: int
    fdm_label: str
    source_locks: S11CombinedCarryTrendSourceLocks
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S11CombinedCarryTrendConformanceResult:
    completed_bar: CompletedBar
    rule_results: tuple[S11CombinedForecastRuleResult, ...]
    pre_fdm_forecast: float
    fdm: float
    post_fdm_forecast: float
    final_capped_s11_combined_forecast: float
    interpretable_trading_signal: bool = False
    performance_metrics: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


def s11_combined_carry_trend_conformance(
    request: S11CombinedCarryTrendConformanceRequest,
) -> S11CombinedCarryTrendConformanceResult:
    require_source_native(request.lane_class)
    request.completed_bar.validate()
    request.source_locks.validate()
    _validate_fdm(request)
    _validate_eligible_rule_ids(request.eligible_rule_ids)

    inputs_by_id: dict[str, S11SyntheticForecastInput] = {}
    for forecast_input in request.forecast_inputs:
        forecast_input.validate(request.completed_bar)
        if forecast_input.rule_id in inputs_by_id:
            raise CarverBlocked("S11 forecast inputs must be unique")
        inputs_by_id[forecast_input.rule_id] = forecast_input

    if tuple(inputs_by_id) != request.eligible_rule_ids:
        raise CarverBlocked("S11 forecast inputs must exactly match the locked eligible rule set")

    _validate_style_coverage(tuple(inputs_by_id.values()))
    _validate_top_down_weights(tuple(inputs_by_id.values()))

    rule_results = tuple(
        S11CombinedForecastRuleResult(
            rule_id=rule_id,
            style=forecast_input.style,
            input_capped_forecast=forecast_input.capped_forecast.value,
            style_weight=forecast_input.style_weight,
            rule_weight=forecast_input.rule_weight,
            variation_weight=forecast_input.variation_weight,
            top_down_weight=forecast_input.top_down_weight,
        )
        for rule_id, forecast_input in inputs_by_id.items()
    )
    pre_fdm = sum(result.input_capped_forecast * result.top_down_weight for result in rule_results)
    _require_finite("S11 pre-FDM forecast", pre_fdm)
    post_fdm = pre_fdm * request.s11_fdm
    _require_finite("S11 post-FDM forecast", post_fdm)
    final = cap_forecast(post_fdm, FORECAST_CAP)
    result = S11CombinedCarryTrendConformanceResult(
        completed_bar=request.completed_bar,
        rule_results=rule_results,
        pre_fdm_forecast=pre_fdm,
        fdm=request.s11_fdm,
        post_fdm_forecast=post_fdm,
        final_capped_s11_combined_forecast=final,
    )
    if result.interpretable_trading_signal or result.performance_metrics or result.position_outputs:
        raise CarverBlocked("S11 combined forecast must not emit performance, trading, or position outputs")
    return result


def _validate_eligible_rule_ids(eligible_rule_ids: tuple[str, ...]) -> None:
    if not eligible_rule_ids:
        raise CarverBlocked("S11 requires at least one eligible forecast rule")
    if len(set(eligible_rule_ids)) != len(eligible_rule_ids):
        raise CarverBlocked("S11 eligible forecast rules must be unique")
    for rule_id in eligible_rule_ids:
        require_non_empty_text("S11 eligible forecast rule id", rule_id)


def _validate_fdm(request: S11CombinedCarryTrendConformanceRequest) -> None:
    require_non_empty_text("S11 FDM label", request.fdm_label)
    if not request.fdm_label.startswith("synthetic_"):
        raise CarverBlocked("S11 FDM label must be synthetic")
    require_finite_positive("S11 FDM", request.s11_fdm)
    if isinstance(request.fdm_rule_count, bool) or not isinstance(request.fdm_rule_count, Integral):
        raise CarverBlocked("S11 FDM rule count must be an integer")
    if request.fdm_rule_count != len(request.eligible_rule_ids):
        raise CarverBlocked("S11 FDM rule count must match locked eligible rule count")


def _validate_style_coverage(inputs: tuple[S11SyntheticForecastInput, ...]) -> None:
    styles = {forecast_input.style for forecast_input in inputs}
    if styles != {S11ForecastStyle.TREND, S11ForecastStyle.CARRY}:
        raise CarverBlocked("S11 combined carry/trend requires both trend and carry styles")


def _validate_top_down_weights(inputs: tuple[S11SyntheticForecastInput, ...]) -> None:
    totals = {
        S11ForecastStyle.TREND: 0.0,
        S11ForecastStyle.CARRY: 0.0,
    }
    for forecast_input in inputs:
        _require_finite("S11 top-down weight", forecast_input.top_down_weight)
        if forecast_input.top_down_weight <= 0:
            raise CarverBlocked("S11 top-down weight must be positive")
        totals[forecast_input.style] += forecast_input.top_down_weight

    for style, expected in S11_SOURCE_STYLE_WEIGHTS.items():
        if not isclose(totals[style], expected, rel_tol=0.0, abs_tol=1e-12):
            raise CarverBlocked("S11 top-down weights do not match locked style mix")
    total_weight = sum(totals.values())
    if not isclose(total_weight, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked("S11 top-down weights must sum to 1")


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")

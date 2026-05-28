from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite
from numbers import Real

from .m0 import CompletedBar, LaneClass, SourceRuleStatus, CarverBlocked, require_finite_positive, require_non_empty_text, require_source_native
from .m1 import TimedValue


S09_EWMAC_SPANS = (2, 4, 8, 16, 32, 64)
S09_EWMAC_SCALARS = {
    2: 12.1,
    4: 8.53,
    8: 5.95,
    16: 4.10,
    32: 2.79,
    64: 1.91,
}
S09_EWMAC_FDM_ROWS = {
    (2, 4, 8, 16, 32, 64): 1.26,
    (4, 8, 16, 32, 64): 1.19,
    (8, 16, 32, 64): 1.13,
    (16, 32, 64): 1.08,
    (32, 64): 1.03,
    (64,): 1.0,
}
FORECAST_CAP = 20.0


@dataclass(frozen=True)
class ForecastRuleInput:
    rule_id: str
    raw_forecast: TimedValue
    scalar: float
    scalar_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    cap: float = FORECAST_CAP
    cap_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    def validate(self, completed_bar: CompletedBar) -> None:
        require_source_native(self.lane_class)
        completed_bar.validate()
        require_non_empty_text("forecast rule id", self.rule_id)
        _require_finite("raw forecast", self.raw_forecast.value)
        require_finite_positive("forecast scalar", self.scalar)
        require_finite_positive("forecast cap", self.cap)
        if self.raw_forecast.as_of != completed_bar.timestamp:
            raise CarverBlocked("raw forecast timestamp is not aligned to completed bar")
        if self.scalar_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("forecast scalar source is unresolved")
        if self.cap_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("forecast cap source is unresolved")

    @property
    def scaled_forecast(self) -> float:
        return self.raw_forecast.value * self.scalar

    @property
    def capped_forecast(self) -> float:
        return cap_forecast(self.scaled_forecast, self.cap)


@dataclass(frozen=True)
class ForecastRuleResult:
    rule_id: str
    raw_forecast: float
    scalar: float
    scaled_forecast: float
    capped_forecast: float
    weight: float


@dataclass(frozen=True)
class ForecastBlockRequest:
    completed_bar: CompletedBar
    rule_inputs: tuple[ForecastRuleInput, ...]
    allowed_rule_ids: tuple[str, ...]
    fdm: float
    weight_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    fdm_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    speed_rule_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    combined_cap: float = FORECAST_CAP
    combined_cap_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class ForecastBlockResult:
    completed_bar: CompletedBar
    rule_results: tuple[ForecastRuleResult, ...]
    pre_fdm_forecast: float
    fdm: float
    post_fdm_forecast: float
    final_forecast: float


def cap_forecast(value: float, cap: float = FORECAST_CAP) -> float:
    _require_finite("forecast value", value)
    require_finite_positive("forecast cap", cap)
    if value > cap:
        return cap
    if value < -cap:
        return -cap
    return value


def combine_forecast_block(request: ForecastBlockRequest) -> ForecastBlockResult:
    require_source_native(request.lane_class)
    request.completed_bar.validate()
    require_finite_positive("forecast diversification multiplier", request.fdm)
    require_finite_positive("combined forecast cap", request.combined_cap)
    if request.weight_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("forecast weight source is unresolved")
    if request.fdm_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("forecast diversification multiplier source is unresolved")
    if request.speed_rule_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("forecast speed eligibility source is unresolved")
    if request.combined_cap_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("combined forecast cap source is unresolved")
    if not request.allowed_rule_ids:
        raise CarverBlocked("at least one eligible forecast rule is required")
    if len(set(request.allowed_rule_ids)) != len(request.allowed_rule_ids):
        raise CarverBlocked("eligible forecast rules must be unique")
    if not request.rule_inputs:
        raise CarverBlocked("forecast block requires rule inputs")

    inputs_by_id: dict[str, ForecastRuleInput] = {}
    for rule_input in request.rule_inputs:
        rule_input.validate(request.completed_bar)
        if rule_input.rule_id in inputs_by_id:
            raise CarverBlocked("forecast rule inputs must be unique")
        inputs_by_id[rule_input.rule_id] = rule_input

    missing = [rule_id for rule_id in request.allowed_rule_ids if rule_id not in inputs_by_id]
    if missing:
        raise CarverBlocked("eligible forecast rule is missing input")

    weight = 1.0 / len(request.allowed_rule_ids)
    if not isclose(weight * len(request.allowed_rule_ids), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked("forecast weights must sum to 1")

    rule_results = tuple(
        ForecastRuleResult(
            rule_id=rule_id,
            raw_forecast=inputs_by_id[rule_id].raw_forecast.value,
            scalar=inputs_by_id[rule_id].scalar,
            scaled_forecast=inputs_by_id[rule_id].scaled_forecast,
            capped_forecast=inputs_by_id[rule_id].capped_forecast,
            weight=weight,
        )
        for rule_id in request.allowed_rule_ids
    )
    pre_fdm = sum(result.capped_forecast * result.weight for result in rule_results)
    post_fdm = pre_fdm * request.fdm
    final = cap_forecast(post_fdm, request.combined_cap)
    return ForecastBlockResult(
        completed_bar=request.completed_bar,
        rule_results=rule_results,
        pre_fdm_forecast=pre_fdm,
        fdm=request.fdm,
        post_fdm_forecast=post_fdm,
        final_forecast=final,
    )


def s09_rule_id(span: int) -> str:
    if span not in S09_EWMAC_SPANS:
        raise CarverBlocked("S09 EWMAC span is not source-locked")
    return f"EWMAC{span}"


def s09_fdm_for_allowed_spans(allowed_spans: tuple[int, ...]) -> float:
    _validate_s09_allowed_spans(allowed_spans)
    fdm = S09_EWMAC_FDM_ROWS.get(allowed_spans)
    if fdm is None:
        raise CarverBlocked("S09 FDM row is unresolved for eligible speed set")
    return fdm


def _validate_s09_allowed_spans(allowed_spans: tuple[int, ...]) -> None:
    if not allowed_spans:
        raise CarverBlocked("S09 requires at least one eligible EWMAC speed")
    if allowed_spans != tuple(sorted(allowed_spans)):
        raise CarverBlocked("S09 EWMAC speeds must be ordered from fastest to slowest")
    if len(set(allowed_spans)) != len(allowed_spans):
        raise CarverBlocked("S09 EWMAC speeds must be unique")
    if any(span not in S09_EWMAC_SPANS for span in allowed_spans):
        raise CarverBlocked("S09 EWMAC speed is not source-locked")


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from math import isclose, isfinite
from numbers import Real

from .m0 import CompletedBar, LaneClass, SourceRuleStatus, CarverBlocked, require_non_empty_text, require_source_native
from .m1 import TimedValue
from .m2 import (
    FORECAST_CAP,
    ForecastBlockRequest,
    ForecastBlockResult,
    ForecastRuleInput,
    combine_forecast_block,
)


S10_CARRY_SPANS = (5, 20, 60, 120)
S10_CARRY_SCALAR = 30.0
S10_CARRY_FDM_ROWS = {
    (5, 20, 60, 120): 1.04,
    (20, 60, 120): 1.03,
    (60, 120): 1.02,
    (120,): 1.0,
}


@dataclass(frozen=True)
class S10CarryForecastBlockSourceLocks:
    m5_input_provenance_status: SourceRuleStatus
    input_history_status: SourceRuleStatus
    smoothing_span_status: SourceRuleStatus
    scalar_status: SourceRuleStatus
    cap_status: SourceRuleStatus
    eligibility_status: SourceRuleStatus
    weight_status: SourceRuleStatus
    fdm_status: SourceRuleStatus
    output_boundary_status: SourceRuleStatus

    def validate(self) -> None:
        for name, status in (
            ("M5 input provenance", self.m5_input_provenance_status),
            ("carry input history", self.input_history_status),
            ("carry smoothing span set", self.smoothing_span_status),
            ("carry scalar", self.scalar_status),
            ("forecast cap", self.cap_status),
            ("eligible carry span set", self.eligibility_status),
            ("carry forecast weight", self.weight_status),
            ("carry FDM", self.fdm_status),
            ("S10 output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"S10 {name} source is unresolved")


@dataclass(frozen=True)
class S10M5RiskAdjustedCarryInput:
    label: str
    risk_adjusted_carry: TimedValue
    status: SourceRuleStatus

    def validate(self) -> None:
        require_non_empty_text("S10 M5 carry input label", self.label)
        if not self.label.startswith("synthetic_"):
            raise CarverBlocked("S10 M5 carry input label must be synthetic")
        if self.status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S10 M5 carry input source is unresolved")
        _require_finite("S10 M5 risk-adjusted carry input", self.risk_adjusted_carry.value)


@dataclass(frozen=True)
class S10CarrySpanForecast:
    span: int
    rule_id: str
    smoothed_risk_adjusted_carry: float


@dataclass(frozen=True)
class S10CarryForecastBlockRequest:
    completed_bar: CompletedBar
    m5_carry_inputs: tuple[S10M5RiskAdjustedCarryInput, ...]
    eligible_spans: tuple[int, ...]
    source_locks: S10CarryForecastBlockSourceLocks
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S10CarryForecastBlockResult:
    completed_bar: CompletedBar
    span_forecasts: tuple[S10CarrySpanForecast, ...]
    forecast_block: ForecastBlockResult
    final_capped_s10_carry_forecast: float
    interpretable_trading_signal: bool = False
    performance_metrics: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


def s10_carry_rule_id(span: int) -> str:
    if span not in S10_CARRY_SPANS:
        raise CarverBlocked("S10 carry span is not source-locked")
    return f"Carry{span}"


def s10_carry_fdm_for_eligible_spans(eligible_spans: tuple[int, ...]) -> float:
    _validate_eligible_spans(eligible_spans)
    fdm = S10_CARRY_FDM_ROWS.get(eligible_spans)
    if fdm is None:
        raise CarverBlocked("S10 carry FDM row is unresolved for eligible span set")
    return fdm


def s10_carry_forecast_block_conformance(
    request: S10CarryForecastBlockRequest,
) -> S10CarryForecastBlockResult:
    require_source_native(request.lane_class)
    request.completed_bar.validate()
    request.source_locks.validate()
    _validate_eligible_spans(request.eligible_spans)
    _validate_history(request)

    span_forecasts = tuple(
        S10CarrySpanForecast(
            span=span,
            rule_id=s10_carry_rule_id(span),
            smoothed_risk_adjusted_carry=_synthetic_ewma(
                tuple(item.risk_adjusted_carry.value for item in request.m5_carry_inputs),
                span,
            ),
        )
        for span in request.eligible_spans
    )
    rule_inputs = tuple(
        ForecastRuleInput(
            rule_id=forecast.rule_id,
            raw_forecast=TimedValue(forecast.smoothed_risk_adjusted_carry, request.completed_bar.timestamp),
            scalar=S10_CARRY_SCALAR,
            scalar_status=request.source_locks.scalar_status,
            cap=FORECAST_CAP,
            cap_status=request.source_locks.cap_status,
            lane_class=request.lane_class,
        )
        for forecast in span_forecasts
    )
    block = combine_forecast_block(
        ForecastBlockRequest(
            completed_bar=request.completed_bar,
            rule_inputs=rule_inputs,
            allowed_rule_ids=tuple(forecast.rule_id for forecast in span_forecasts),
            fdm=s10_carry_fdm_for_eligible_spans(request.eligible_spans),
            weight_status=request.source_locks.weight_status,
            fdm_status=request.source_locks.fdm_status,
            speed_rule_status=request.source_locks.eligibility_status,
            combined_cap=FORECAST_CAP,
            combined_cap_status=request.source_locks.cap_status,
            lane_class=request.lane_class,
        )
    )
    result = S10CarryForecastBlockResult(
        completed_bar=request.completed_bar,
        span_forecasts=span_forecasts,
        forecast_block=block,
        final_capped_s10_carry_forecast=block.final_forecast,
    )
    if result.interpretable_trading_signal or result.performance_metrics or result.position_outputs:
        raise CarverBlocked("S10 carry forecast block must not emit performance, trading, or position outputs")
    return result


def _validate_eligible_spans(eligible_spans: tuple[int, ...]) -> None:
    if not eligible_spans:
        raise CarverBlocked("S10 carry requires at least one eligible span")
    if eligible_spans != tuple(sorted(eligible_spans)):
        raise CarverBlocked("S10 carry spans must be ordered from fastest to slowest")
    if len(set(eligible_spans)) != len(eligible_spans):
        raise CarverBlocked("S10 carry spans must be unique")
    if any(span not in S10_CARRY_SPANS for span in eligible_spans):
        raise CarverBlocked("S10 carry span is not source-locked")
    if eligible_spans not in S10_CARRY_FDM_ROWS:
        raise CarverBlocked("S10 carry eligible span set is not source-permitted")


def _validate_history(request: S10CarryForecastBlockRequest) -> None:
    inputs = request.m5_carry_inputs
    if len(inputs) < max(request.eligible_spans):
        raise CarverBlocked("S10 carry input history is insufficient for requested smoothing span")

    previous = None
    for item in inputs:
        item.validate()
        CompletedBar(item.risk_adjusted_carry.as_of).validate()
        if previous is not None:
            if item.risk_adjusted_carry.as_of <= previous:
                raise CarverBlocked("S10 carry input timestamps must be strictly increasing")
            if item.risk_adjusted_carry.as_of - previous != timedelta(days=1):
                raise CarverBlocked("S10 carry input history must use a daily synthetic cadence")
        previous = item.risk_adjusted_carry.as_of

    if inputs[-1].risk_adjusted_carry.as_of != request.completed_bar.timestamp:
        raise CarverBlocked("S10 carry input history is stale versus completed bar")


def _synthetic_ewma(values: tuple[float, ...], span: int) -> float:
    if span not in S10_CARRY_SPANS:
        raise CarverBlocked("S10 carry span is not source-locked")
    alpha = 2.0 / (span + 1.0)
    smoothed = values[0]
    _require_finite("S10 carry EWMA seed", smoothed)
    for value in values[1:]:
        _require_finite("S10 carry EWMA input", value)
        smoothed = alpha * value + (1.0 - alpha) * smoothed
    _require_finite("S10 carry smoothed forecast", smoothed)
    return smoothed


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")

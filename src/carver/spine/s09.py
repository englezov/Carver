from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from numbers import Real

from .daily_bars import CompletedDailyMarketBar
from .m0 import LaneClass, SourceRuleStatus, CarverBlocked, require_finite_positive, require_source_native
from .m1 import TimedValue
from .m2 import (
    FORECAST_CAP,
    S09_EWMAC_SCALARS,
    ForecastBlockRequest,
    ForecastBlockResult,
    ForecastRuleInput,
    combine_forecast_block,
    s09_fdm_for_allowed_spans,
    s09_rule_id,
)


@dataclass(frozen=True)
class S09SyntheticConvention:
    ewma_convention_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    daily_price_risk_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    scalar_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    cap_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    speed_rule_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    fdm_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    combined_cap_status: SourceRuleStatus = SourceRuleStatus.LOCKED

    def validate(self) -> None:
        if self.ewma_convention_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S09 EWMA convention is unresolved")
        if self.daily_price_risk_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S09 daily price risk source is unresolved")
        if self.scalar_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S09 forecast scalar source is unresolved")
        if self.cap_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S09 forecast cap source is unresolved")
        if self.speed_rule_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S09 speed eligibility source is unresolved")
        if self.fdm_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S09 FDM source is unresolved")
        if self.combined_cap_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("S09 combined cap source is unresolved")


@dataclass(frozen=True)
class S09TrendForecastRequest:
    bars: tuple[CompletedDailyMarketBar, ...]
    as_of: datetime
    daily_price_risk: TimedValue
    allowed_spans: tuple[int, ...]
    convention: S09SyntheticConvention = S09SyntheticConvention()
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S09RuleForecast:
    span: int
    fast_span: int
    slow_span: int
    fast_ewma: float
    slow_ewma: float
    raw_forecast: float
    scalar: float
    capped_forecast: float


@dataclass(frozen=True)
class S09TrendForecastResult:
    contract_code: str
    as_of: datetime
    rule_forecasts: tuple[S09RuleForecast, ...]
    forecast_block: ForecastBlockResult

    @property
    def final_forecast(self) -> float:
        return self.forecast_block.final_forecast


def s09_multiple_trend_forecast(request: S09TrendForecastRequest) -> S09TrendForecastResult:
    require_source_native(request.lane_class)
    request.convention.validate()
    require_finite_positive("S09 daily price risk", request.daily_price_risk.value)
    if request.daily_price_risk.as_of != request.as_of:
        raise CarverBlocked("S09 daily price risk timestamp must align to forecast timestamp")
    if not request.bars:
        raise CarverBlocked("S09 requires completed daily bars")

    _validate_completed_bars(request.bars, request.as_of)
    fdm = s09_fdm_for_allowed_spans(request.allowed_spans)
    slowest_span = max(span * 4 for span in request.allowed_spans)
    if len(request.bars) < slowest_span + 1:
        raise CarverBlocked("S09 synthetic EWMA warm-up requires at least slowest span plus one completed bars")

    closes = tuple(bar.close for bar in request.bars)
    final_bar = request.bars[-1].completed_bar
    rule_forecasts: list[S09RuleForecast] = []
    rule_inputs: list[ForecastRuleInput] = []
    for span in request.allowed_spans:
        fast_span = span
        slow_span = span * 4
        fast = _recursive_ewma(closes, fast_span)
        slow = _recursive_ewma(closes, slow_span)
        raw = (fast - slow) / request.daily_price_risk.value
        _require_finite("S09 raw forecast", raw)
        scalar = S09_EWMAC_SCALARS[span]
        rule_id = s09_rule_id(span)
        rule_input = ForecastRuleInput(
            rule_id=rule_id,
            raw_forecast=TimedValue(raw, request.as_of),
            scalar=scalar,
            scalar_status=request.convention.scalar_status,
            cap=FORECAST_CAP,
            cap_status=request.convention.cap_status,
            lane_class=request.lane_class,
        )
        rule_input.validate(final_bar)
        rule_forecasts.append(
            S09RuleForecast(
                span=span,
                fast_span=fast_span,
                slow_span=slow_span,
                fast_ewma=fast,
                slow_ewma=slow,
                raw_forecast=raw,
                scalar=scalar,
                capped_forecast=rule_input.capped_forecast,
            )
        )
        rule_inputs.append(rule_input)

    block = combine_forecast_block(
        ForecastBlockRequest(
            completed_bar=final_bar,
            rule_inputs=tuple(rule_inputs),
            allowed_rule_ids=tuple(s09_rule_id(span) for span in request.allowed_spans),
            fdm=fdm,
            speed_rule_status=request.convention.speed_rule_status,
            fdm_status=request.convention.fdm_status,
            combined_cap_status=request.convention.combined_cap_status,
            lane_class=request.lane_class,
        )
    )
    return S09TrendForecastResult(
        contract_code=request.bars[-1].code,
        as_of=request.as_of,
        rule_forecasts=tuple(rule_forecasts),
        forecast_block=block,
    )


def _recursive_ewma(values: tuple[float, ...], span: int) -> float:
    if span < 2:
        raise CarverBlocked("EWMA span must be at least 2")
    alpha = 2.0 / (span + 1.0)
    average = values[0]
    require_finite_positive("initial EWMA value", average)
    for value in values[1:]:
        require_finite_positive("EWMA input value", value)
        average = alpha * value + (1.0 - alpha) * average
    return average


def _validate_completed_bars(bars: tuple[CompletedDailyMarketBar, ...], as_of: datetime) -> None:
    previous_timestamp: datetime | None = None
    contract = bars[0].contract
    for bar in bars:
        bar.validate()
        if bar.contract != contract:
            raise CarverBlocked("S09 bars must use one exact source-native contract")
        if previous_timestamp is not None and bar.timestamp <= previous_timestamp:
            raise CarverBlocked("S09 completed daily bars must be strictly increasing")
        if bar.timestamp > as_of:
            raise CarverBlocked("S09 forecast input includes future bars")
        previous_timestamp = bar.timestamp
    if bars[-1].timestamp != as_of:
        raise CarverBlocked("S09 forecast timestamp must be the last completed bar")


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")

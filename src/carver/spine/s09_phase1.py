from __future__ import annotations

from dataclasses import dataclass

from .continuous import ContinuousChainBuildResult
from .data_acquisition import Phase1ContinuousReadinessReport
from .m0 import LaneClass, CarverBlocked, require_finite_positive, require_source_native
from .m1 import TimedValue
from .s09 import S09SyntheticConvention, S09TrendForecastRequest, S09TrendForecastResult, s09_multiple_trend_forecast


S09_PHASE1_ROOTS = ("MES", "ZN", "ZF")
S09_PHASE1_CONTRACT_MONTHS = ("09-25", "12-25", "03-26", "06-26")
S09_PHASE1_ELIGIBLE_SPANS = (32, 64)
S09_PHASE1_REQUIRED_DAILY_BARS = 257


@dataclass(frozen=True)
class S09Phase1InstrumentForecastInput:
    root: str
    continuous_result: ContinuousChainBuildResult
    daily_price_risk: TimedValue
    eligible_spans: tuple[int, ...] = S09_PHASE1_ELIGIBLE_SPANS

    def validate(self) -> None:
        if self.root not in S09_PHASE1_ROOTS:
            raise CarverBlocked("S09 phase-1 forecast root must be MES, ZN, or ZF")
        self.continuous_result.validate()
        if not self.continuous_result.ready:
            raise CarverBlocked("S09 phase-1 forecast requires a ready continuous chain")
        if self.continuous_result.source_contract_months != S09_PHASE1_CONTRACT_MONTHS:
            raise CarverBlocked("S09 phase-1 forecast source contract months do not match the locked phase-1 chain")
        if len(self.continuous_result.adjusted_bars) < S09_PHASE1_REQUIRED_DAILY_BARS:
            raise CarverBlocked("S09 phase-1 forecast requires at least 257 adjusted daily bars")
        if self.eligible_spans != S09_PHASE1_ELIGIBLE_SPANS:
            raise CarverBlocked("S09 phase-1 forecast is locked to EWMAC32 and EWMAC64")
        final_timestamp = self.continuous_result.adjusted_bars[-1].timestamp
        if self.daily_price_risk.as_of != final_timestamp:
            raise CarverBlocked("S09 phase-1 daily price risk timestamp must align to final adjusted bar")
        require_finite_positive("S09 phase-1 daily price risk", self.daily_price_risk.value)
        previous_month_index = -1
        seen_months: set[str] = set()
        for bar in self.continuous_result.adjusted_bars:
            bar.validate()
            if bar.code != self.root:
                raise CarverBlocked("S09 phase-1 adjusted bars must match the requested root")
            if bar.contract_month not in S09_PHASE1_CONTRACT_MONTHS:
                raise CarverBlocked("S09 phase-1 adjusted bar has an unlocked contract month")
            month_index = S09_PHASE1_CONTRACT_MONTHS.index(bar.contract_month)
            if month_index < previous_month_index:
                raise CarverBlocked("S09 phase-1 adjusted bar contract months must not move backward")
            previous_month_index = month_index
            seen_months.add(bar.contract_month)
        if tuple(month for month in S09_PHASE1_CONTRACT_MONTHS if month in seen_months) != S09_PHASE1_CONTRACT_MONTHS:
            raise CarverBlocked("S09 phase-1 adjusted bars must include every locked source contract month")


@dataclass(frozen=True)
class S09Phase1MultiInstrumentConformanceRequest:
    readiness_report: Phase1ContinuousReadinessReport
    instrument_inputs: tuple[S09Phase1InstrumentForecastInput, ...]
    required_roots: tuple[str, ...] = S09_PHASE1_ROOTS
    convention: S09SyntheticConvention = S09SyntheticConvention()
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S09Phase1InstrumentForecastResult:
    root: str
    available_row_count: int
    input_row_count: int
    source_contract_months: tuple[str, ...]
    forecast_result: S09TrendForecastResult

    @property
    def final_forecast(self) -> float:
        return self.forecast_result.final_forecast


@dataclass(frozen=True)
class S09Phase1MultiInstrumentConformanceResult:
    instrument_results: tuple[S09Phase1InstrumentForecastResult, ...]
    interpretable_portfolio_signal: bool = False
    performance_metrics: tuple[str, ...] = ()

    @property
    def roots(self) -> tuple[str, ...]:
        return tuple(result.root for result in self.instrument_results)


def s09_phase1_multi_instrument_forecast_conformance(
    request: S09Phase1MultiInstrumentConformanceRequest,
) -> S09Phase1MultiInstrumentConformanceResult:
    require_source_native(request.lane_class)
    request.convention.validate()
    request.readiness_report.validate()
    if request.required_roots != S09_PHASE1_ROOTS:
        raise CarverBlocked("S09 phase-1 conformance required roots are locked to MES, ZN, and ZF")
    if not request.readiness_report.all_ready:
        raise CarverBlocked("S09 phase-1 conformance requires all readiness summaries to be ready")
    if tuple(summary.root for summary in request.readiness_report.summaries) != request.required_roots:
        raise CarverBlocked("S09 phase-1 readiness report root order does not match required roots")
    if tuple(instrument.root for instrument in request.instrument_inputs) != request.required_roots:
        raise CarverBlocked("S09 phase-1 instrument inputs must cover MES, ZN, and ZF in order")

    results: list[S09Phase1InstrumentForecastResult] = []
    for summary, instrument in zip(request.readiness_report.summaries, request.instrument_inputs, strict=True):
        instrument.validate()
        if summary.root != instrument.root:
            raise CarverBlocked("S09 phase-1 readiness summary does not match instrument input")
        if summary.adjusted_row_count != len(instrument.continuous_result.adjusted_bars):
            raise CarverBlocked("S09 phase-1 readiness row count does not match continuous input")
        if summary.minimum_rows != S09_PHASE1_REQUIRED_DAILY_BARS:
            raise CarverBlocked("S09 phase-1 readiness minimum rows do not match the locked S09 requirement")
        if summary.source_contract_months != instrument.continuous_result.source_contract_months:
            raise CarverBlocked("S09 phase-1 readiness source months do not match continuous input")
        if summary.first_date != instrument.continuous_result.adjusted_bars[0].timestamp.date().isoformat():
            raise CarverBlocked("S09 phase-1 readiness first date does not match continuous input")
        if summary.last_date != instrument.continuous_result.adjusted_bars[-1].timestamp.date().isoformat():
            raise CarverBlocked("S09 phase-1 readiness last date does not match continuous input")

        forecast_bars = instrument.continuous_result.adjusted_bars[-S09_PHASE1_REQUIRED_DAILY_BARS :]
        forecast = s09_multiple_trend_forecast(
            S09TrendForecastRequest(
                bars=forecast_bars,
                as_of=forecast_bars[-1].timestamp,
                daily_price_risk=instrument.daily_price_risk,
                allowed_spans=instrument.eligible_spans,
                convention=request.convention,
                lane_class=request.lane_class,
            )
        )
        results.append(
            S09Phase1InstrumentForecastResult(
                root=instrument.root,
                available_row_count=len(instrument.continuous_result.adjusted_bars),
                input_row_count=len(forecast_bars),
                source_contract_months=instrument.continuous_result.source_contract_months,
                forecast_result=forecast,
            )
        )

    result = S09Phase1MultiInstrumentConformanceResult(tuple(results))
    if result.interpretable_portfolio_signal:
        raise CarverBlocked("S09 phase-1 conformance must not produce an interpretable portfolio signal")
    if result.performance_metrics:
        raise CarverBlocked("S09 phase-1 conformance must not produce performance metrics")
    return result

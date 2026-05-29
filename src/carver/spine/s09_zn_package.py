from __future__ import annotations

from dataclasses import dataclass

from .continuous import ContinuousChainBuildResult
from .daily_bars import CompletedDailyMarketBar
from .m0 import BackAdjustmentSpec, LaneClass, RollRuleSpec, SessionCalendarSpec, SourceRuleStatus, CarverBlocked, require_source_native
from .m1 import TimedValue
from .m2 import s09_fdm_for_allowed_spans
from .m3 import zn_contract
from .portfolio_completion import IntakeRouteContract, PortfolioIntakeMode, SourceArtifactRef
from .s09 import S09TrendForecastRequest, S09TrendForecastResult, s09_multiple_trend_forecast
from .s09_readiness import S09InstrumentDataContract, S09ReadinessReport, build_s09_readiness_report
from .web_chart_api import ChartBarType, LockedWebChartSymbol, WebChartProbePlan, WebChartRequest, WebChartSymbol


S09_ZN_CONTRACT_MONTH = "06-26"
S09_ZN_PROVIDER_SYMBOL_ID = "4470301"
S09_ZN_DISPLAY_SYMBOL = "ZN JUN26"
S09_ZN_ELIGIBLE_SPANS = (32, 64)
S09_ZN_REQUIRED_DAILY_BARS = max(S09_ZN_ELIGIBLE_SPANS) * 4 + 1
S09_ZN_GATE_ARTIFACT = SourceArtifactRef("docs/process/CARVER_S09_REAL_DATA_READINESS_GATE_2026-05-29.md")
S09_ZN_CONTINUOUS_CONTRACT_MONTHS = ("09-25", "12-25", "03-26", "06-26")
S09_ZN_CONTINUOUS_ROLL_DATES = ("2025-09-22", "2025-12-22", "2026-03-23")
S09_ZN_UNIT_PRICE_RISK_CONFORMANCE_MODE = "UNIT_PRICE_RISK_CONFORMANCE_ONLY_NOT_SOURCE_RISK"


@dataclass(frozen=True)
class S09ZnPackage:
    instrument_contract: S09InstrumentDataContract
    readiness_report: S09ReadinessReport
    probe_plan: WebChartProbePlan

    def validate(self) -> None:
        self.instrument_contract.validate_shape()
        if self.instrument_contract.contract != zn_contract():
            raise CarverBlocked("S09 ZN package requires exact ZN contract")
        if self.instrument_contract.contract_month != S09_ZN_CONTRACT_MONTH:
            raise CarverBlocked("S09 ZN package requires the locked ZN contract month")
        if self.instrument_contract.eligible_spans != S09_ZN_ELIGIBLE_SPANS:
            raise CarverBlocked("S09 ZN package requires locked ZN eligible EWMAC spans")
        self.readiness_report.require_real_data_ready()
        self.probe_plan.request.validate()
        if self.probe_plan.execution_authorized:
            raise CarverBlocked("S09 ZN package probe must remain unexecuted in this gate")


@dataclass(frozen=True)
class S09TinySliceConformanceRequest:
    bars: tuple[CompletedDailyMarketBar, ...]
    daily_price_risk: TimedValue
    package: S09ZnPackage
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S09ContinuousTinySliceConformanceRequest:
    continuous_result: ContinuousChainBuildResult
    daily_price_risk: TimedValue
    package: S09ZnPackage
    price_risk_mode: str = S09_ZN_UNIT_PRICE_RISK_CONFORMANCE_MODE
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S09ContinuousTinySliceConformanceResult:
    forecast_result: S09TrendForecastResult
    source_contract_months: tuple[str, ...]
    roll_dates: tuple[str, ...]
    available_row_count: int
    input_row_count: int
    price_risk_mode: str
    interpretable_signal: bool = False

    @property
    def final_forecast(self) -> float:
        return self.forecast_result.final_forecast

    def validate(self) -> None:
        if self.source_contract_months != S09_ZN_CONTINUOUS_CONTRACT_MONTHS:
            raise CarverBlocked("S09 continuous conformance source months do not match the locked ZN chain")
        if self.roll_dates != S09_ZN_CONTINUOUS_ROLL_DATES:
            raise CarverBlocked("S09 continuous conformance roll dates do not match the locked ZN chain")
        if self.input_row_count != S09_ZN_REQUIRED_DAILY_BARS:
            raise CarverBlocked("S09 continuous conformance must use the exact tiny-slice row count")
        if self.available_row_count < self.input_row_count:
            raise CarverBlocked("S09 continuous conformance available row count is below input row count")
        if self.price_risk_mode != S09_ZN_UNIT_PRICE_RISK_CONFORMANCE_MODE:
            raise CarverBlocked("S09 continuous conformance price-risk mode is not the locked sentinel")
        if self.interpretable_signal:
            raise CarverBlocked("S09 continuous conformance result must not claim an interpretable signal")


def build_s09_zn_package() -> S09ZnPackage:
    instrument_contract = S09InstrumentDataContract(
        contract=zn_contract(),
        contract_month=S09_ZN_CONTRACT_MONTH,
        intake_contract=IntakeRouteContract(
            PortfolioIntakeMode.DIRECT_DAILY_PRIMARY,
            SourceRuleStatus.LOCKED,
            S09_ZN_GATE_ARTIFACT,
        ),
        session_calendar=SessionCalendarSpec("S09 ZN session calendar", SourceRuleStatus.LOCKED, "UTC"),
        roll_rule=RollRuleSpec("S09 ZN roll rule", SourceRuleStatus.LOCKED),
        back_adjustment=BackAdjustmentSpec("S09 ZN back-adjustment rule", SourceRuleStatus.LOCKED),
        daily_price_risk_status=SourceRuleStatus.LOCKED,
        eligible_spans_status=SourceRuleStatus.LOCKED,
        eligible_spans=S09_ZN_ELIGIBLE_SPANS,
        session_artifact=S09_ZN_GATE_ARTIFACT,
        roll_artifact=S09_ZN_GATE_ARTIFACT,
        back_adjustment_artifact=S09_ZN_GATE_ARTIFACT,
        daily_price_risk_artifact=S09_ZN_GATE_ARTIFACT,
        eligible_spans_artifact=S09_ZN_GATE_ARTIFACT,
    )
    readiness_report = build_s09_readiness_report(instrument_contract)
    locked_symbol = LockedWebChartSymbol(
        zn_contract(),
        S09_ZN_CONTRACT_MONTH,
        S09_ZN_PROVIDER_SYMBOL_ID,
        S09_ZN_DISPLAY_SYMBOL,
    )
    request = WebChartRequest(
        WebChartSymbol(locked_symbol, S09_ZN_PROVIDER_SYMBOL_ID, S09_ZN_DISPLAY_SYMBOL),
        ChartBarType.DAILY,
        element_size=1,
        element_count=S09_ZN_REQUIRED_DAILY_BARS,
    )
    package = S09ZnPackage(
        instrument_contract=instrument_contract,
        readiness_report=readiness_report,
        probe_plan=WebChartProbePlan(request, execution_authorized=False),
    )
    package.validate()
    return package


def require_s09_zn_probe_authorization(package: S09ZnPackage) -> None:
    package.validate()
    package.probe_plan.require_authorized()


def s09_zn_tiny_slice_forecast_conformance(request: S09TinySliceConformanceRequest) -> S09TrendForecastResult:
    require_source_native(request.lane_class)
    request.package.validate()
    if len(request.bars) < S09_ZN_REQUIRED_DAILY_BARS:
        raise CarverBlocked("S09 ZN tiny-slice conformance requires enough completed bars for synthetic warm-up")
    for bar in request.bars:
        bar.validate()
        if bar.contract != zn_contract() or bar.contract_month != S09_ZN_CONTRACT_MONTH:
            raise CarverBlocked("S09 ZN tiny-slice conformance requires exact ZN completed daily bars")
    if request.daily_price_risk.as_of != request.bars[-1].timestamp:
        raise CarverBlocked("S09 ZN tiny-slice daily price risk must align to final completed bar")
    s09_fdm_for_allowed_spans(S09_ZN_ELIGIBLE_SPANS)
    return s09_multiple_trend_forecast(
        S09TrendForecastRequest(
            bars=request.bars,
            as_of=request.bars[-1].timestamp,
            daily_price_risk=request.daily_price_risk,
            allowed_spans=S09_ZN_ELIGIBLE_SPANS,
            lane_class=request.lane_class,
        )
    )


def s09_zn_continuous_tiny_slice_forecast_conformance(
    request: S09ContinuousTinySliceConformanceRequest,
) -> S09ContinuousTinySliceConformanceResult:
    require_source_native(request.lane_class)
    request.package.validate()
    request.continuous_result.validate()
    if not request.continuous_result.ready:
        raise CarverBlocked("S09 continuous conformance requires a ready continuous ZN chain")
    if request.continuous_result.source_contract_months != S09_ZN_CONTINUOUS_CONTRACT_MONTHS:
        raise CarverBlocked("S09 continuous conformance requires the locked ZN contract-month chain")
    if request.continuous_result.roll_dates != S09_ZN_CONTINUOUS_ROLL_DATES:
        raise CarverBlocked("S09 continuous conformance requires the locked ZN roll dates")
    if request.price_risk_mode != S09_ZN_UNIT_PRICE_RISK_CONFORMANCE_MODE:
        raise CarverBlocked("S09 continuous conformance only admits the unit price-risk sentinel")
    if request.daily_price_risk.value != 1.0:
        raise CarverBlocked("S09 continuous conformance unit price-risk sentinel must equal 1.0")
    if len(request.continuous_result.adjusted_bars) < S09_ZN_REQUIRED_DAILY_BARS:
        raise CarverBlocked("S09 continuous conformance requires enough adjusted completed daily bars")

    bars = request.continuous_result.adjusted_bars[-S09_ZN_REQUIRED_DAILY_BARS :]
    previous_month_index = -1
    for bar in bars:
        bar.validate()
        if bar.contract != zn_contract():
            raise CarverBlocked("S09 continuous conformance requires exact ZN adjusted bars")
        if bar.contract_month not in S09_ZN_CONTINUOUS_CONTRACT_MONTHS:
            raise CarverBlocked("S09 continuous conformance adjusted bar month is outside the locked ZN chain")
        month_index = S09_ZN_CONTINUOUS_CONTRACT_MONTHS.index(bar.contract_month)
        if month_index < previous_month_index:
            raise CarverBlocked("S09 continuous conformance adjusted bar months must follow the locked chain order")
        previous_month_index = month_index
    if request.daily_price_risk.as_of != bars[-1].timestamp:
        raise CarverBlocked("S09 continuous conformance daily price-risk sentinel must align to final completed bar")
    s09_fdm_for_allowed_spans(S09_ZN_ELIGIBLE_SPANS)
    forecast = s09_multiple_trend_forecast(
        S09TrendForecastRequest(
            bars=bars,
            as_of=bars[-1].timestamp,
            daily_price_risk=request.daily_price_risk,
            allowed_spans=S09_ZN_ELIGIBLE_SPANS,
            lane_class=request.lane_class,
        )
    )
    result = S09ContinuousTinySliceConformanceResult(
        forecast_result=forecast,
        source_contract_months=request.continuous_result.source_contract_months,
        roll_dates=request.continuous_result.roll_dates,
        available_row_count=len(request.continuous_result.adjusted_bars),
        input_row_count=len(bars),
        price_risk_mode=request.price_risk_mode,
    )
    result.validate()
    return result

from __future__ import annotations

from dataclasses import dataclass

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

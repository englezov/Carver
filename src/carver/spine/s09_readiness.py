from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .m0 import BackAdjustmentSpec, ContractSpec, LaneClass, RollRuleSpec, SessionCalendarSpec, SourceRuleStatus, CarverBlocked, require_source_native
from .m2 import s09_fdm_for_allowed_spans
from .portfolio_completion import IntakeRouteContract, PortfolioIntakeMode, SourceArtifactRef, locked_rule_artifact_blockers
from .portfolio_conformance import ProviderMappingStatus
from .web_chart_api import LOCKED_WEB_CHART_PROVIDER_SYMBOLS


class S09ReadinessStatus(StrEnum):
    SYNTHETIC_READY_REAL_DATA_BLOCKED = "SYNTHETIC_READY_REAL_DATA_BLOCKED"
    REAL_DATA_READY_NOT_EXECUTION_AUTHORIZATION = "REAL_DATA_READY_NOT_EXECUTION_AUTHORIZATION"


@dataclass(frozen=True)
class S09ProviderMappingRow:
    contract_code: str
    contract_month: str
    display_symbol: str
    status: ProviderMappingStatus
    provider_symbol_id: str | None = None


@dataclass(frozen=True)
class S09InstrumentDataContract:
    contract: ContractSpec
    contract_month: str
    intake_contract: IntakeRouteContract = IntakeRouteContract(PortfolioIntakeMode.DIRECT_DAILY_PRIMARY)
    session_calendar: SessionCalendarSpec = SessionCalendarSpec("S09 session calendar")
    roll_rule: RollRuleSpec = RollRuleSpec("S09 roll rule")
    back_adjustment: BackAdjustmentSpec = BackAdjustmentSpec("S09 back-adjustment rule")
    daily_price_risk_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    eligible_spans_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    eligible_spans: tuple[int, ...] = ()
    session_artifact: SourceArtifactRef | None = None
    roll_artifact: SourceArtifactRef | None = None
    back_adjustment_artifact: SourceArtifactRef | None = None
    daily_price_risk_artifact: SourceArtifactRef | None = None
    eligible_spans_artifact: SourceArtifactRef | None = None
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    def validate_shape(self) -> None:
        require_source_native(self.lane_class)
        self.contract.validate()
        _require_contract_month(self.contract_month)
        self.intake_contract.validate()
        if self.intake_contract.mode is not PortfolioIntakeMode.DIRECT_DAILY_PRIMARY:
            if self.intake_contract.mode is not PortfolioIntakeMode.MINUTE_DERIVED_FALLBACK:
                raise CarverBlocked("S09 intake route mode is unresolved")
        if self.eligible_spans_status is SourceRuleStatus.LOCKED:
            s09_fdm_for_allowed_spans(self.eligible_spans)


@dataclass(frozen=True)
class S09ReadinessReport:
    contract_code: str
    mapping_row: S09ProviderMappingRow
    intake_contract: IntakeRouteContract
    blockers: tuple[str, ...]

    @property
    def status(self) -> S09ReadinessStatus:
        if self.blockers:
            return S09ReadinessStatus.SYNTHETIC_READY_REAL_DATA_BLOCKED
        return S09ReadinessStatus.REAL_DATA_READY_NOT_EXECUTION_AUTHORIZATION

    def require_real_data_ready(self) -> None:
        if self.status is not S09ReadinessStatus.REAL_DATA_READY_NOT_EXECUTION_AUTHORIZATION:
            raise CarverBlocked("; ".join(self.blockers))


def s09_provider_mapping_status(contract: ContractSpec, contract_month: str) -> S09ProviderMappingRow:
    contract.validate()
    _require_contract_month(contract_month)
    display_symbol = _display_symbol(contract.code, contract_month)
    provider_symbol_id = LOCKED_WEB_CHART_PROVIDER_SYMBOLS.get((contract.code, contract_month, display_symbol))
    return S09ProviderMappingRow(
        contract_code=contract.code,
        contract_month=contract_month,
        display_symbol=display_symbol,
        status=ProviderMappingStatus.LOCKED if provider_symbol_id else ProviderMappingStatus.UNRESOLVED,
        provider_symbol_id=provider_symbol_id,
    )


def build_s09_readiness_report(contract: S09InstrumentDataContract) -> S09ReadinessReport:
    contract.validate_shape()
    mapping_row = s09_provider_mapping_status(contract.contract, contract.contract_month)
    blockers: list[str] = []
    if mapping_row.status is not ProviderMappingStatus.LOCKED:
        blockers.append(f"provider mapping unresolved for {mapping_row.contract_code} {mapping_row.contract_month}")
    _append_source_rule_blocker(blockers, contract.session_calendar, "session calendar")
    _append_source_rule_blocker(blockers, contract.roll_rule, "roll rule")
    _append_source_rule_blocker(blockers, contract.back_adjustment, "back-adjustment rule")
    blockers.extend(
        locked_rule_artifact_blockers(
            contract.session_calendar,
            contract.roll_rule,
            contract.back_adjustment,
            contract.session_artifact,
            contract.roll_artifact,
            contract.back_adjustment_artifact,
        )
    )
    blockers.extend(contract.intake_contract.blockers())
    _append_status_artifact_blocker(
        blockers,
        contract.daily_price_risk_status,
        contract.daily_price_risk_artifact,
        "daily price-risk source",
    )
    _append_status_artifact_blocker(
        blockers,
        contract.eligible_spans_status,
        contract.eligible_spans_artifact,
        "eligible EWMAC speed-set source",
    )
    return S09ReadinessReport(
        contract_code=contract.contract.code,
        mapping_row=mapping_row,
        intake_contract=contract.intake_contract,
        blockers=tuple(blockers),
    )


def require_s09_real_data_readiness_preflight(report: S09ReadinessReport) -> None:
    report.require_real_data_ready()


def _append_source_rule_blocker(blockers: list[str], rule, label: str) -> None:
    try:
        rule.require_locked()
    except CarverBlocked:
        blockers.append(f"{label} is unresolved")


def _append_status_artifact_blocker(
    blockers: list[str],
    status: SourceRuleStatus,
    artifact: SourceArtifactRef | None,
    label: str,
) -> None:
    if status is not SourceRuleStatus.LOCKED:
        blockers.append(f"{label} is unresolved")
        return
    if not isinstance(artifact, SourceArtifactRef):
        blockers.append(f"{label} artifact is unresolved")
        return
    try:
        artifact.validate(f"{label} artifact")
    except CarverBlocked:
        blockers.append(f"{label} artifact is unresolved")


def _display_symbol(contract_code: str, contract_month: str) -> str:
    month, year = _split_contract_month(contract_month)
    month_names = {
        "01": "JAN",
        "02": "FEB",
        "03": "MAR",
        "04": "APR",
        "05": "MAY",
        "06": "JUN",
        "07": "JUL",
        "08": "AUG",
        "09": "SEP",
        "10": "OCT",
        "11": "NOV",
        "12": "DEC",
    }
    if month not in month_names:
        raise CarverBlocked("contract month has invalid display month")
    return f"{contract_code} {month_names[month]}{year}"


def _require_contract_month(value: str) -> None:
    _split_contract_month(value)


def _split_contract_month(value: str) -> tuple[str, str]:
    if not isinstance(value, str) or len(value) != 5 or value[2] != "-":
        raise CarverBlocked("contract month must use MM-YY")
    month, year = value.split("-")
    if not (month.isdigit() and year.isdigit()):
        raise CarverBlocked("contract month must use MM-YY")
    if int(month) < 1 or int(month) > 12:
        raise CarverBlocked("contract month has invalid month")
    return month, year

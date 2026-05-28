from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from .m0 import BackAdjustmentSpec, CarverBlocked, RollRuleSpec, SessionCalendarSpec, SourceRuleStatus, require_non_empty_text
from .m3 import PortfolioSpec
from .portfolio_conformance import (
    PortfolioProviderMappingSet,
    PortfolioProviderMappingRow,
    ProviderMappingStatus,
    portfolio_web_chart_mapping_status,
    require_locked_provider_mapping_set,
)


@dataclass(frozen=True)
class SourceArtifactRef:
    path: str

    def validate(self, name: str) -> None:
        require_non_empty_text(name, self.path)
        path = Path(self.path)
        if path.is_absolute() or ".." in path.parts:
            raise CarverBlocked(f"{name} must be a repo-local relative path")
        if len(path.parts) < 3 or path.parts[0] != "docs" or path.parts[1] not in {"process", "researchops"}:
            raise CarverBlocked(f"{name} must point to a repo-local markdown process/researchops artifact")
        if path.suffix.lower() != ".md":
            raise CarverBlocked(f"{name} must point to a markdown artifact")
        repo_root = Path(__file__).resolve().parents[3]
        try:
            resolved = (repo_root / path).resolve(strict=True)
        except FileNotFoundError as exc:
            raise CarverBlocked(f"{name} does not exist") from exc
        try:
            resolved.relative_to(repo_root)
        except ValueError as exc:
            raise CarverBlocked(f"{name} must stay inside the Carver workspace") from exc
        if not resolved.is_file():
            raise CarverBlocked(f"{name} must be a file")


class PortfolioIntakeMode(StrEnum):
    DIRECT_DAILY_PRIMARY = "DIRECT_DAILY_PRIMARY"
    MINUTE_DERIVED_FALLBACK = "MINUTE_DERIVED_FALLBACK"


class PortfolioCompletionStatus(StrEnum):
    SYNTHETIC_READY_REAL_DATA_BLOCKED = "SYNTHETIC_READY_REAL_DATA_BLOCKED"
    REAL_DATA_READY_NOT_BACKTEST_AUTHORIZATION = "REAL_DATA_READY_NOT_BACKTEST_AUTHORIZATION"


@dataclass(frozen=True)
class RiskFxInputContract:
    as_of: datetime
    annual_risk_status: SourceRuleStatus
    fx_status: SourceRuleStatus
    annual_risk_artifact: SourceArtifactRef | None = None
    fx_artifact: SourceArtifactRef | None = None

    def validate(self) -> None:
        if self.as_of.tzinfo is None or self.as_of.utcoffset() is None:
            raise CarverBlocked("risk/FX contract timestamp must be timezone-aware")
        if self.as_of.hour or self.as_of.minute or self.as_of.second or self.as_of.microsecond:
            raise CarverBlocked("risk/FX contract timestamp must be date-aligned")
        if self.annual_risk_status is SourceRuleStatus.LOCKED:
            if not isinstance(self.annual_risk_artifact, SourceArtifactRef):
                raise CarverBlocked("annual risk artifact is unresolved")
            self.annual_risk_artifact.validate("annual risk artifact")
        if self.fx_status is SourceRuleStatus.LOCKED:
            if not isinstance(self.fx_artifact, SourceArtifactRef):
                raise CarverBlocked("FX artifact is unresolved")
            self.fx_artifact.validate("FX artifact")

    def blockers(self) -> tuple[str, ...]:
        self.validate()
        items: list[str] = []
        if self.annual_risk_status is not SourceRuleStatus.LOCKED:
            items.append("annual risk input contract is unresolved")
        if self.fx_status is not SourceRuleStatus.LOCKED:
            items.append("FX input contract is unresolved")
        return tuple(items)


@dataclass(frozen=True)
class IntakeRouteContract:
    mode: PortfolioIntakeMode
    status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    source_artifact: SourceArtifactRef | None = None
    direct_daily_blocked_artifact: SourceArtifactRef | None = None

    def validate(self) -> None:
        if not isinstance(self.mode, PortfolioIntakeMode):
            raise CarverBlocked("portfolio intake mode must be locked")
        if self.status is SourceRuleStatus.LOCKED:
            if not isinstance(self.source_artifact, SourceArtifactRef):
                raise CarverBlocked("intake route source artifact is unresolved")
            self.source_artifact.validate("intake route source artifact")
            if self.mode is PortfolioIntakeMode.MINUTE_DERIVED_FALLBACK:
                if not isinstance(self.direct_daily_blocked_artifact, SourceArtifactRef):
                    raise CarverBlocked("minute-derived fallback requires a direct-daily-blocked artifact")
                self.direct_daily_blocked_artifact.validate("direct-daily-blocked artifact")

    def blockers(self) -> tuple[str, ...]:
        self.validate()
        if self.status is not SourceRuleStatus.LOCKED:
            return ("intake route contract is unresolved",)
        return ()


@dataclass(frozen=True)
class PortfolioCompletionReport:
    portfolio_id: str
    intake_contract: IntakeRouteContract
    mapping_rows: tuple[PortfolioProviderMappingRow, ...]
    session_calendar: SessionCalendarSpec
    roll_rule: RollRuleSpec
    back_adjustment: BackAdjustmentSpec
    session_artifact: SourceArtifactRef | None
    roll_artifact: SourceArtifactRef | None
    back_adjustment_artifact: SourceArtifactRef | None
    risk_fx_contract: RiskFxInputContract
    blockers: tuple[str, ...]

    @property
    def intake_mode(self) -> PortfolioIntakeMode:
        return self.intake_contract.mode

    @property
    def status(self) -> PortfolioCompletionStatus:
        if self.blockers:
            return PortfolioCompletionStatus.SYNTHETIC_READY_REAL_DATA_BLOCKED
        return PortfolioCompletionStatus.REAL_DATA_READY_NOT_BACKTEST_AUTHORIZATION

    def require_real_data_ready(self) -> None:
        if self.status is not PortfolioCompletionStatus.REAL_DATA_READY_NOT_BACKTEST_AUTHORIZATION:
            raise CarverBlocked("; ".join(self.blockers))


def require_real_data_conformance_preflight(report: PortfolioCompletionReport) -> None:
    report.require_real_data_ready()


def build_portfolio_completion_report(
    portfolio: PortfolioSpec,
    contract_months: dict[str, str],
    risk_fx_contract: RiskFxInputContract,
    provider_mapping_set: PortfolioProviderMappingSet | None = None,
    intake_contract: IntakeRouteContract | None = None,
    session_calendar: SessionCalendarSpec | None = None,
    roll_rule: RollRuleSpec | None = None,
    back_adjustment: BackAdjustmentSpec | None = None,
    session_artifact: SourceArtifactRef | None = None,
    roll_artifact: SourceArtifactRef | None = None,
    back_adjustment_artifact: SourceArtifactRef | None = None,
) -> PortfolioCompletionReport:
    portfolio.validate()
    if intake_contract is None:
        intake_contract = IntakeRouteContract(PortfolioIntakeMode.DIRECT_DAILY_PRIMARY)
    if session_calendar is None:
        session_calendar = SessionCalendarSpec("P01/P02 session calendar")
    if roll_rule is None:
        roll_rule = RollRuleSpec("P01/P02 roll rule")
    if back_adjustment is None:
        back_adjustment = BackAdjustmentSpec("P01/P02 back-adjustment rule")
    intake_contract.validate()
    risk_fx_contract.validate()
    if provider_mapping_set is not None:
        require_locked_provider_mapping_set(provider_mapping_set)
        if provider_mapping_set.portfolio != portfolio:
            raise CarverBlocked("provider mapping set portfolio does not match completion portfolio")
        if provider_mapping_set.contract_months != contract_months:
            raise CarverBlocked("provider mapping set months do not match completion months")
    mapping_rows = portfolio_web_chart_mapping_status(portfolio, contract_months)
    blockers: list[str] = []
    for row in mapping_rows:
        if row.status is not ProviderMappingStatus.LOCKED:
            blockers.append(f"provider mapping unresolved for {row.contract_code} {row.contract_month}")
    try:
        session_calendar.require_locked()
    except CarverBlocked:
        blockers.append("session calendar is unresolved")
    try:
        roll_rule.require_locked()
    except CarverBlocked:
        blockers.append("roll rule is unresolved")
    try:
        back_adjustment.require_locked()
    except CarverBlocked:
        blockers.append("back-adjustment rule is unresolved")
    blockers.extend(
        locked_rule_artifact_blockers(
            session_calendar,
            roll_rule,
            back_adjustment,
            session_artifact,
            roll_artifact,
            back_adjustment_artifact,
        )
    )
    blockers.extend(intake_contract.blockers())
    blockers.extend(risk_fx_contract.blockers())
    return PortfolioCompletionReport(
        portfolio_id=portfolio.portfolio_id,
        intake_contract=intake_contract,
        mapping_rows=mapping_rows,
        session_calendar=session_calendar,
        roll_rule=roll_rule,
        back_adjustment=back_adjustment,
        session_artifact=session_artifact,
        roll_artifact=roll_artifact,
        back_adjustment_artifact=back_adjustment_artifact,
        risk_fx_contract=risk_fx_contract,
        blockers=tuple(blockers),
    )


def locked_rule_artifact_blockers(
    session_calendar: SessionCalendarSpec,
    roll_rule: RollRuleSpec,
    back_adjustment: BackAdjustmentSpec,
    session_artifact: SourceArtifactRef | None,
    roll_artifact: SourceArtifactRef | None,
    back_adjustment_artifact: SourceArtifactRef | None,
) -> tuple[str, ...]:
    blockers: list[str] = []
    if session_calendar.status is SourceRuleStatus.LOCKED:
        if not isinstance(session_artifact, SourceArtifactRef):
            blockers.append("session calendar artifact is unresolved")
        else:
            try:
                session_artifact.validate("session calendar artifact")
            except CarverBlocked:
                blockers.append("session calendar artifact is unresolved")
    if roll_rule.status is SourceRuleStatus.LOCKED:
        if not isinstance(roll_artifact, SourceArtifactRef):
            blockers.append("roll rule artifact is unresolved")
        else:
            try:
                roll_artifact.validate("roll rule artifact")
            except CarverBlocked:
                blockers.append("roll rule artifact is unresolved")
    if back_adjustment.status is SourceRuleStatus.LOCKED:
        if not isinstance(back_adjustment_artifact, SourceArtifactRef):
            blockers.append("back-adjustment artifact is unresolved")
        else:
            try:
                back_adjustment_artifact.validate("back-adjustment artifact")
            except CarverBlocked:
                blockers.append("back-adjustment artifact is unresolved")
    return tuple(blockers)

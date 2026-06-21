from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..m0 import CarverBlocked
from .identity import ReplayIdentity
from .source_universe import SourceUniverseProof
from .validation import (
    require_hash,
    require_hour_aligned_utc,
    require_iso_date,
    require_positive_number,
    require_text,
)


@dataclass(frozen=True)
class LocalDailySourceRow:
    completed_timestamp_utc: datetime
    trading_date: str
    raw_symbol: str
    row_locator: str
    close_price: float
    annual_percentage_sigma: float
    readiness_status: str
    row_hash: str

    def validate(self) -> None:
        require_hour_aligned_utc("S27 v2 daily completed timestamp", self.completed_timestamp_utc)
        require_iso_date("S27 v2 daily trading date", self.trading_date)
        require_text("S27 v2 daily raw symbol", self.raw_symbol)
        require_text("S27 v2 daily row locator", self.row_locator)
        require_positive_number("S27 v2 daily close price", self.close_price)
        require_positive_number("S27 v2 daily annual percentage sigma", self.annual_percentage_sigma)
        if self.readiness_status != "READY_COMPLETED_BAR":
            raise CarverBlocked("S27 v2 daily row readiness must be READY_COMPLETED_BAR")
        require_hash("S27 v2 daily source row hash", self.row_hash)


@dataclass(frozen=True)
class LocalHourlySourceRow:
    completed_timestamp_utc: datetime
    trading_date: str
    raw_symbol: str
    session_id: str
    row_locator: str
    close_price: float
    readiness_status: str
    row_hash: str

    def validate(self) -> None:
        require_hour_aligned_utc("S27 v2 hourly completed timestamp", self.completed_timestamp_utc)
        require_iso_date("S27 v2 hourly trading date", self.trading_date)
        require_text("S27 v2 hourly raw symbol", self.raw_symbol)
        require_text("S27 v2 hourly session id", self.session_id)
        require_text("S27 v2 hourly row locator", self.row_locator)
        require_positive_number("S27 v2 hourly close price", self.close_price)
        if self.readiness_status != "READY_COMPLETED_BAR":
            raise CarverBlocked("S27 v2 hourly row readiness must be READY_COMPLETED_BAR")
        require_hash("S27 v2 hourly source row hash", self.row_hash)


@dataclass(frozen=True)
class LocalSessionSourceRow:
    trading_date: str
    session_id: str
    raw_symbol: str
    session_open_utc: datetime
    session_close_utc: datetime
    row_locator: str
    readiness_status: str
    row_hash: str

    def validate(self) -> None:
        require_iso_date("S27 v2 session trading date", self.trading_date)
        require_text("S27 v2 session id", self.session_id)
        require_text("S27 v2 session raw symbol", self.raw_symbol)
        require_hour_aligned_utc("S27 v2 session open", self.session_open_utc)
        require_hour_aligned_utc("S27 v2 session close", self.session_close_utc)
        if self.session_close_utc <= self.session_open_utc:
            raise CarverBlocked("S27 v2 session close must follow session open")
        require_text("S27 v2 session row locator", self.row_locator)
        if self.readiness_status != "READY_SESSION_CALENDAR":
            raise CarverBlocked("S27 v2 session readiness must be READY_SESSION_CALENDAR")
        require_hash("S27 v2 session source row hash", self.row_hash)


@dataclass(frozen=True)
class LocalRollSourceRow:
    trading_date: str
    expiring_raw_symbol: str
    incoming_raw_symbol: str
    roll_policy_hash: str
    row_locator: str
    readiness_status: str
    row_hash: str

    def validate(self) -> None:
        require_iso_date("S27 v2 roll trading date", self.trading_date)
        require_text("S27 v2 expiring raw symbol", self.expiring_raw_symbol)
        require_text("S27 v2 incoming raw symbol", self.incoming_raw_symbol)
        require_hash("S27 v2 roll policy hash", self.roll_policy_hash)
        require_text("S27 v2 roll row locator", self.row_locator)
        if self.readiness_status != "READY_ROLL_CALENDAR":
            raise CarverBlocked("S27 v2 roll readiness must be READY_ROLL_CALENDAR")
        require_hash("S27 v2 roll source row hash", self.row_hash)


@dataclass(frozen=True)
class LocalCostParameterRow:
    effective_trading_date: str
    raw_symbol: str
    commission_policy_hash: str
    spread_policy_hash: str
    contract_multiplier_value_hash: str
    currency_policy_hash: str
    row_locator: str
    readiness_status: str
    row_hash: str

    def validate(self) -> None:
        require_iso_date("S27 v2 cost parameter effective trading date", self.effective_trading_date)
        require_text("S27 v2 cost parameter raw symbol", self.raw_symbol)
        require_hash("S27 v2 cost parameter commission policy hash", self.commission_policy_hash)
        require_hash("S27 v2 cost parameter spread policy hash", self.spread_policy_hash)
        require_hash("S27 v2 cost parameter multiplier value hash", self.contract_multiplier_value_hash)
        require_hash("S27 v2 cost parameter currency policy hash", self.currency_policy_hash)
        require_text("S27 v2 cost parameter row locator", self.row_locator)
        if self.readiness_status != "READY_COST_PARAMETERS":
            raise CarverBlocked("S27 v2 cost parameter readiness must be READY_COST_PARAMETERS")
        require_hash("S27 v2 cost parameter row hash", self.row_hash)


@dataclass(frozen=True)
class SourceInputManifestRow:
    identity: ReplayIdentity
    source_universe: SourceUniverseProof
    daily_continuous_row_hash: str
    daily_current_contract_row_hash: str
    previous_completed_current_contract_close_hash: str
    hourly_decision_row_hash: str
    hourly_fill_row_hash: str
    runtime_history_hash: str
    daily_hourly_level_compatibility_hash: str
    sigma_bridge_level_source_hash: str
    continuous_to_current_contract_level_bridge_hash: str
    source_input_hash: str

    def validate(self) -> None:
        self.identity.validate()
        self.source_universe.validate()
        require_hash("S27 v2 source manifest daily continuous row hash", self.daily_continuous_row_hash)
        require_hash("S27 v2 source manifest daily current-contract row hash", self.daily_current_contract_row_hash)
        require_hash(
            "S27 v2 source manifest previous completed current-contract close hash",
            self.previous_completed_current_contract_close_hash,
        )
        require_hash("S27 v2 source manifest hourly decision row hash", self.hourly_decision_row_hash)
        require_hash("S27 v2 source manifest hourly fill row hash", self.hourly_fill_row_hash)
        require_hash("S27 v2 source manifest runtime history hash", self.runtime_history_hash)
        require_hash(
            "S27 v2 source manifest daily/hourly level compatibility hash",
            self.daily_hourly_level_compatibility_hash,
        )
        require_hash("S27 v2 source manifest sigma bridge level source hash", self.sigma_bridge_level_source_hash)
        require_hash(
            "S27 v2 source manifest continuous/current bridge hash",
            self.continuous_to_current_contract_level_bridge_hash,
        )
        require_hash("S27 v2 source input hash", self.source_input_hash)

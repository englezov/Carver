from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import BLOCKED_LEVEL_COMPATIBILITY
from .identity import ReplayIdentity
from .validation import require_hash, require_text


@dataclass(frozen=True)
class DailyHourlyLevelCompatibilityLedgerRow:
    identity: ReplayIdentity
    daily_continuous_row_hash: str
    daily_current_contract_row_hash: str
    previous_completed_current_contract_close_hash: str
    hourly_decision_row_hash: str
    hourly_fill_decision_row_hash: str
    current_contract_raw_symbol: str
    hourly_decision_raw_symbol: str
    hourly_fill_raw_symbol: str
    continuous_adjustment_bridge_policy_hash: str
    sigma_bridge_level_source_hash: str
    sigma_bridge_uses_previous_completed_current_contract_close_proof_hash: str
    hourly_current_matches_daily_current_contract_level_proof_hash: str
    continuous_to_current_contract_level_bridge_hash: str
    bridged_daily_continuous_equilibrium_proof_hash: str
    compatibility_verdict: str
    compatibility_reason_code: str
    daily_hourly_level_compatibility_hash: str

    def validate(self) -> None:
        try:
            self.identity.validate()
            require_hash("S27 v2 daily continuous row hash", self.daily_continuous_row_hash)
            require_hash("S27 v2 daily current-contract row hash", self.daily_current_contract_row_hash)
            require_hash(
                "S27 v2 previous completed current-contract close hash",
                self.previous_completed_current_contract_close_hash,
            )
            require_hash("S27 v2 hourly decision row hash", self.hourly_decision_row_hash)
            require_hash("S27 v2 hourly fill-decision row hash", self.hourly_fill_decision_row_hash)
            require_text("S27 v2 current contract raw symbol", self.current_contract_raw_symbol)
            require_text("S27 v2 hourly decision raw symbol", self.hourly_decision_raw_symbol)
            require_text("S27 v2 hourly fill raw symbol", self.hourly_fill_raw_symbol)
            require_hash(
                "S27 v2 continuous adjustment bridge policy hash",
                self.continuous_adjustment_bridge_policy_hash,
            )
            require_hash("S27 v2 sigma bridge level source hash", self.sigma_bridge_level_source_hash)
            require_hash(
                "S27 v2 sigma bridge previous completed current-contract proof hash",
                self.sigma_bridge_uses_previous_completed_current_contract_close_proof_hash,
            )
            require_hash(
                "S27 v2 hourly/current contract same-level proof hash",
                self.hourly_current_matches_daily_current_contract_level_proof_hash,
            )
            require_hash(
                "S27 v2 continuous/current contract bridge hash",
                self.continuous_to_current_contract_level_bridge_hash,
            )
            require_hash(
                "S27 v2 bridged daily continuous equilibrium proof hash",
                self.bridged_daily_continuous_equilibrium_proof_hash,
            )
            require_text("S27 v2 compatibility verdict", self.compatibility_verdict)
            if self.compatibility_verdict != "PASS":
                raise CarverBlocked("S27 v2 daily/hourly compatibility verdict must be PASS")
            require_text("S27 v2 compatibility reason code", self.compatibility_reason_code)
            if self.compatibility_reason_code not in ("SAME_LEVEL_COMPATIBLE", "BRIDGED_CONTINUOUS_COMPATIBLE"):
                raise CarverBlocked("S27 v2 daily/hourly compatibility reason code is unresolved")
            require_hash(
                "S27 v2 daily/hourly level compatibility hash",
                self.daily_hourly_level_compatibility_hash,
            )
        except CarverBlocked as exc:
            raise CarverBlocked(BLOCKED_LEVEL_COMPATIBILITY) from exc

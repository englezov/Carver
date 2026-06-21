from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import BLOCKED_RUNTIME_HISTORY, BLOCKED_SIGMA
from .identity import ReplayIdentity
from .validation import require_hash


@dataclass(frozen=True)
class RuntimeHistoryLedgerRow:
    identity: ReplayIdentity
    runtime_history_hash: str
    ewma5_state_hash: str
    ewmac16_64_state_hash: str
    sigma_estimator_definition_hash: str
    sigma_input_window_hash: str
    sigma_annualization_policy_hash: str
    sigma_estimator_state_hash: str
    vqm_history_hash: str

    def validate(self) -> None:
        try:
            self.identity.validate()
            require_hash("S27 v2 runtime history hash", self.runtime_history_hash)
            require_hash("S27 v2 EWMA5 state hash", self.ewma5_state_hash)
            require_hash("S27 v2 EWMAC16/64 state hash", self.ewmac16_64_state_hash)
            require_hash("S27 v2 sigma estimator definition hash", self.sigma_estimator_definition_hash)
            require_hash("S27 v2 sigma input window hash", self.sigma_input_window_hash)
            require_hash("S27 v2 sigma annualization policy hash", self.sigma_annualization_policy_hash)
            require_hash("S27 v2 sigma estimator state hash", self.sigma_estimator_state_hash)
            require_hash("S27 v2 V/Q/M history hash", self.vqm_history_hash)
        except CarverBlocked as exc:
            raise CarverBlocked(f"{BLOCKED_RUNTIME_HISTORY}; {BLOCKED_SIGMA}") from exc

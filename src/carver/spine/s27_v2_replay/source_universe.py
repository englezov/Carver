from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ..m0 import CarverBlocked
from .constants import BLOCKED_SOURCE_UNIVERSE
from .validation import require_hash, require_iso_date


@dataclass(frozen=True)
class SourceUniverseProof:
    source_universe_hash: str
    raw_file_hash_set_hash: str
    row_locator_hash: str
    strict_prior_candidate_set_hash: str
    no_future_rows_proof_hash: str
    missing_row_proof_hash: str
    repair_rejection_proof_hash: str
    requested_start: str
    requested_end: str
    instrument_universe_hash: str
    raw_symbol_universe_hash: str
    daily_row_universe_hash: str
    hourly_decision_fill_row_universe_hash: str
    session_row_universe_hash: str
    roll_row_universe_hash: str
    cost_parameter_row_universe_hash: str
    inclusion_exclusion_reason_code_hash: str
    duplicate_policy_hash: str
    canonical_row_locator_serialization_hash: str

    def validate(self) -> None:
        try:
            require_hash("S27 v2 source universe hash", self.source_universe_hash)
            require_hash("S27 v2 raw file hash-set hash", self.raw_file_hash_set_hash)
            require_hash("S27 v2 row locator hash", self.row_locator_hash)
            require_hash("S27 v2 strict-prior candidate-set hash", self.strict_prior_candidate_set_hash)
            require_hash("S27 v2 no-future-rows proof hash", self.no_future_rows_proof_hash)
            require_hash("S27 v2 missing-row proof hash", self.missing_row_proof_hash)
            require_hash("S27 v2 repair/rejection proof hash", self.repair_rejection_proof_hash)
            require_iso_date("S27 v2 requested start", self.requested_start)
            require_iso_date("S27 v2 requested end", self.requested_end)
            if date.fromisoformat(self.requested_end) < date.fromisoformat(self.requested_start):
                raise CarverBlocked("S27 v2 requested end must not precede requested start")
            require_hash("S27 v2 instrument universe hash", self.instrument_universe_hash)
            require_hash("S27 v2 raw-symbol universe hash", self.raw_symbol_universe_hash)
            require_hash("S27 v2 daily row universe hash", self.daily_row_universe_hash)
            require_hash(
                "S27 v2 hourly decision/fill row universe hash",
                self.hourly_decision_fill_row_universe_hash,
            )
            require_hash("S27 v2 session row universe hash", self.session_row_universe_hash)
            require_hash("S27 v2 roll row universe hash", self.roll_row_universe_hash)
            require_hash("S27 v2 cost parameter row universe hash", self.cost_parameter_row_universe_hash)
            require_hash(
                "S27 v2 inclusion/exclusion reason-code hash",
                self.inclusion_exclusion_reason_code_hash,
            )
            require_hash("S27 v2 duplicate policy hash", self.duplicate_policy_hash)
            require_hash(
                "S27 v2 canonical row-locator serialization hash",
                self.canonical_row_locator_serialization_hash,
            )
        except CarverBlocked as exc:
            raise CarverBlocked(BLOCKED_SOURCE_UNIVERSE) from exc

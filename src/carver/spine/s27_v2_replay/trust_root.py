from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .canonical_hash import CanonicalSerializationPolicy
from .constants import BLOCKED_TRUST_ROOT
from .validation import require_hash


@dataclass(frozen=True)
class ReplayTrustRoot:
    replay_trust_root_hash: str
    source_lock_hash: str
    local_data_contract_hash: str
    provenance_design_hash: str
    runner_implementation_hash: str
    parser_extractor_source_hash: str
    dependency_runtime_manifest_hash: str
    replay_config_hash: str
    source_input_universe_manifest_hash: str
    raw_source_file_hash_set_hash: str
    source_row_batch_contract_hash: str
    source_row_batch_set_hash: str
    source_row_locator_hash: str
    source_row_selection_authority_hash: str
    canonical_serialization_policy: CanonicalSerializationPolicy
    session_calendar_policy_hash: str
    roll_calendar_policy_hash: str
    tick_rounding_policy_hash: str
    commission_policy_hash: str
    spread_unit_policy_hash: str
    contract_multiplier_currency_policy_hash: str
    daily_hourly_level_compatibility_policy_hash: str
    stale_evidence_supersession_manifest_hash: str
    active_evidence_manifest_hash: str

    def validate(self) -> None:
        try:
            require_hash("S27 v2 replay trust root hash", self.replay_trust_root_hash)
            require_hash("S27 v2 source lock hash", self.source_lock_hash)
            require_hash("S27 v2 local data contract hash", self.local_data_contract_hash)
            require_hash("S27 v2 provenance design hash", self.provenance_design_hash)
            require_hash("S27 v2 runner implementation hash", self.runner_implementation_hash)
            require_hash("S27 v2 parser/extractor source hash", self.parser_extractor_source_hash)
            require_hash("S27 v2 dependency/runtime manifest hash", self.dependency_runtime_manifest_hash)
            require_hash("S27 v2 replay config hash", self.replay_config_hash)
            require_hash("S27 v2 source input universe manifest hash", self.source_input_universe_manifest_hash)
            require_hash("S27 v2 raw source file hash-set hash", self.raw_source_file_hash_set_hash)
            require_hash("S27 v2 source row batch contract hash", self.source_row_batch_contract_hash)
            require_hash("S27 v2 source row batch-set hash", self.source_row_batch_set_hash)
            require_hash("S27 v2 source row locator hash", self.source_row_locator_hash)
            require_hash(
                "S27 v2 source row selection authority hash",
                self.source_row_selection_authority_hash,
            )
            self.canonical_serialization_policy.validate()
            require_hash("S27 v2 session calendar policy hash", self.session_calendar_policy_hash)
            require_hash("S27 v2 roll calendar policy hash", self.roll_calendar_policy_hash)
            require_hash("S27 v2 tick rounding policy hash", self.tick_rounding_policy_hash)
            require_hash("S27 v2 commission policy hash", self.commission_policy_hash)
            require_hash("S27 v2 spread-unit policy hash", self.spread_unit_policy_hash)
            require_hash(
                "S27 v2 multiplier/currency policy hash",
                self.contract_multiplier_currency_policy_hash,
            )
            require_hash(
                "S27 v2 daily/hourly compatibility policy hash",
                self.daily_hourly_level_compatibility_policy_hash,
            )
            require_hash(
                "S27 v2 stale evidence supersession manifest hash",
                self.stale_evidence_supersession_manifest_hash,
            )
            require_hash("S27 v2 active evidence manifest hash", self.active_evidence_manifest_hash)
        except CarverBlocked as exc:
            raise CarverBlocked(BLOCKED_TRUST_ROOT) from exc

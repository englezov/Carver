from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .canonical_hash import CanonicalSerializationPolicy
from .constants import (
    S27_V2_INSTRUMENT,
    S27_V2_LANE,
    S27_V2_REPLAY_NON_AUTHORIZATION,
    S27_V2_STRATEGY_ID,
)
from .file_contract import ReplayInputDirectoryDeclaration
from .validation import require_hash, require_iso_date, require_text


@dataclass(frozen=True)
class ReplayWindowDeclaration:
    window_label: str
    start_trading_date: str
    end_trading_date: str
    evidence_stage_label: str
    window_policy_hash: str

    def validate(self) -> None:
        require_text("S27 v2 replay window label", self.window_label)
        require_iso_date("S27 v2 replay start trading date", self.start_trading_date)
        require_iso_date("S27 v2 replay end trading date", self.end_trading_date)
        if self.end_trading_date < self.start_trading_date:
            raise CarverBlocked("S27 v2 replay window end date must not precede start date")
        require_text("S27 v2 replay evidence stage label", self.evidence_stage_label)
        require_hash("S27 v2 replay window policy hash", self.window_policy_hash)


@dataclass(frozen=True)
class ReplayPolicyHashSet:
    source_lock_hash: str
    local_data_contract_hash: str
    provenance_design_hash: str
    source_universe_manifest_hash: str
    raw_file_hash_set_hash: str
    source_row_batch_contract_hash: str
    source_row_batch_set_hash: str
    row_locator_hash: str
    source_row_selection_authority_hash: str
    canonical_serialization_policy: CanonicalSerializationPolicy
    session_calendar_policy_hash: str
    roll_calendar_policy_hash: str
    tick_rounding_policy_hash: str
    commission_policy_hash: str
    spread_unit_policy_hash: str
    contract_multiplier_currency_policy_hash: str
    daily_hourly_compatibility_policy_hash: str
    active_evidence_manifest_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 source lock hash", self.source_lock_hash)
        require_hash("S27 v2 local data contract hash", self.local_data_contract_hash)
        require_hash("S27 v2 provenance design hash", self.provenance_design_hash)
        require_hash("S27 v2 source universe manifest hash", self.source_universe_manifest_hash)
        require_hash("S27 v2 raw file hash-set hash", self.raw_file_hash_set_hash)
        require_hash("S27 v2 source row batch contract hash", self.source_row_batch_contract_hash)
        require_hash("S27 v2 source row batch-set hash", self.source_row_batch_set_hash)
        require_hash("S27 v2 source row locator hash", self.row_locator_hash)
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
            "S27 v2 contract multiplier/currency policy hash",
            self.contract_multiplier_currency_policy_hash,
        )
        require_hash(
            "S27 v2 daily/hourly compatibility policy hash",
            self.daily_hourly_compatibility_policy_hash,
        )
        require_hash("S27 v2 active evidence manifest hash", self.active_evidence_manifest_hash)


@dataclass(frozen=True)
class ReplayAuthorizationBoundary:
    authorization_label: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 replay authorization label", self.authorization_label)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 replay planning config must preserve non-authorizations")


@dataclass(frozen=True)
class S27ReplayPlanningConfig:
    strategy_id: str
    lane: str
    instrument: str
    replay_window: ReplayWindowDeclaration
    input_directory: ReplayInputDirectoryDeclaration
    policy_hashes: ReplayPolicyHashSet
    authorization_boundary: ReplayAuthorizationBoundary
    planning_config_hash: str

    def validate(self) -> None:
        if self.strategy_id != S27_V2_STRATEGY_ID:
            raise CarverBlocked("S27 v2 replay planning config strategy id mismatch")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 replay planning config lane mismatch")
        if self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 replay planning config instrument mismatch")
        self.replay_window.validate()
        self.input_directory.validate()
        self.policy_hashes.validate()
        self.authorization_boundary.validate()
        if self.input_directory.source_universe_manifest_hash != self.policy_hashes.source_universe_manifest_hash:
            raise CarverBlocked("S27 v2 replay planning config source universe hash mismatch")
        if self.input_directory.raw_file_hash_set_hash != self.policy_hashes.raw_file_hash_set_hash:
            raise CarverBlocked("S27 v2 replay planning config raw file hash-set mismatch")
        if self.input_directory.row_locator_hash != self.policy_hashes.row_locator_hash:
            raise CarverBlocked("S27 v2 replay planning config row locator hash mismatch")
        canonical_policy_hash = self.policy_hashes.canonical_serialization_policy.canonical_serialization_policy_hash
        for raw_source_file in self.input_directory.raw_source_files:
            if raw_source_file.local_file.canonical_serialization_policy_hash != canonical_policy_hash:
                raise CarverBlocked("S27 v2 replay planning config raw file canonical policy mismatch")
        require_hash("S27 v2 replay planning config hash", self.planning_config_hash)

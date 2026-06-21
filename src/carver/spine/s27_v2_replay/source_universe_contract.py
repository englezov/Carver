from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ..m0 import CarverBlocked
from .constants import (
    S27_V2_INSTRUMENT,
    S27_V2_LANE,
    S27_V2_REPLAY_NON_AUTHORIZATION,
    S27_V2_STRATEGY_ID,
)
from .row_locator_contract import REQUIRED_ROW_LOCATOR_FAMILIES
from .validation import require_hash, require_iso_date, require_non_empty_tuple, require_text


S27_V2_SOURCE_UNIVERSE_CONTRACT_ONLY_STATUS = "S27_V2_SOURCE_UNIVERSE_CONTRACT_ONLY"
PLANNED_SOURCE_UNIVERSE_FAMILY_STATUS = "PLANNED_SOURCE_UNIVERSE_FAMILY_ONLY"

REQUIRED_SOURCE_UNIVERSE_FAMILIES = (
    "INSTRUMENT_UNIVERSE",
    "RAW_SYMBOL_UNIVERSE",
    "DAILY_ROW_UNIVERSE",
    "HOURLY_DECISION_FILL_ROW_UNIVERSE",
    "SESSION_ROW_UNIVERSE",
    "ROLL_ROW_UNIVERSE",
    "COST_PARAMETER_ROW_UNIVERSE",
)


@dataclass(frozen=True)
class SourceUniverseInclusionRule:
    rule_label: str
    applies_to_family: str
    inclusion_reason_code_hash: str
    exclusion_reason_code_hash: str
    rule_policy_hash: str

    def validate(self) -> None:
        require_text("S27 v2 source universe inclusion rule label", self.rule_label)
        require_text("S27 v2 source universe inclusion rule family", self.applies_to_family)
        if self.applies_to_family not in REQUIRED_SOURCE_UNIVERSE_FAMILIES:
            raise CarverBlocked("S27 v2 source universe inclusion rule family is not locked")
        require_hash("S27 v2 source universe inclusion reason-code hash", self.inclusion_reason_code_hash)
        require_hash("S27 v2 source universe exclusion reason-code hash", self.exclusion_reason_code_hash)
        require_hash("S27 v2 source universe inclusion rule policy hash", self.rule_policy_hash)


@dataclass(frozen=True)
class SourceUniverseFamilyContract:
    universe_family: str
    family_status: str
    source_row_locator_family: str
    planned_universe_hash: str
    inclusion_rule_hash: str
    duplicate_policy_hash: str
    missing_policy_hash: str
    repair_rejection_policy_hash: str
    no_future_rows_proof_hash: str
    family_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 source universe family", self.universe_family)
        if self.universe_family not in REQUIRED_SOURCE_UNIVERSE_FAMILIES:
            raise CarverBlocked("S27 v2 source universe family is not locked")
        require_text("S27 v2 source universe family status", self.family_status)
        if self.family_status != PLANNED_SOURCE_UNIVERSE_FAMILY_STATUS:
            raise CarverBlocked("S27 v2 source universe family must remain planned-only")
        require_text("S27 v2 source universe row-locator family", self.source_row_locator_family)
        if (
            self.universe_family != "INSTRUMENT_UNIVERSE"
            and self.universe_family != "RAW_SYMBOL_UNIVERSE"
            and self.source_row_locator_family not in REQUIRED_ROW_LOCATOR_FAMILIES
        ):
            raise CarverBlocked("S27 v2 source universe row-locator family is not locked")
        require_hash("S27 v2 source universe planned universe hash", self.planned_universe_hash)
        require_hash("S27 v2 source universe inclusion rule hash", self.inclusion_rule_hash)
        require_hash("S27 v2 source universe duplicate policy hash", self.duplicate_policy_hash)
        require_hash("S27 v2 source universe missing policy hash", self.missing_policy_hash)
        require_hash("S27 v2 source universe repair/rejection policy hash", self.repair_rejection_policy_hash)
        require_hash("S27 v2 source universe no-future-rows proof hash", self.no_future_rows_proof_hash)
        require_hash("S27 v2 source universe family contract hash", self.family_contract_hash)


@dataclass(frozen=True)
class SourceUniverseContractBundle:
    status: str
    strategy_id: str
    lane: str
    instrument: str
    requested_start: str
    requested_end: str
    raw_file_hash_set_hash: str
    row_locator_contract_bundle_hash: str
    strict_prior_candidate_set_hash: str
    canonical_row_locator_serialization_hash: str
    inclusion_rules: tuple[SourceUniverseInclusionRule, ...]
    family_contracts: tuple[SourceUniverseFamilyContract, ...]
    source_universe_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 source universe contract status", self.status)
        if self.status != S27_V2_SOURCE_UNIVERSE_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 source universe contract must remain contract-only")
        if self.strategy_id != S27_V2_STRATEGY_ID:
            raise CarverBlocked("S27 v2 source universe contract strategy id mismatch")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 source universe contract lane mismatch")
        if self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 source universe contract instrument mismatch")
        require_iso_date("S27 v2 source universe requested start", self.requested_start)
        require_iso_date("S27 v2 source universe requested end", self.requested_end)
        if date.fromisoformat(self.requested_end) < date.fromisoformat(self.requested_start):
            raise CarverBlocked("S27 v2 source universe requested end must not precede start")
        require_hash("S27 v2 source universe raw file hash-set hash", self.raw_file_hash_set_hash)
        require_hash(
            "S27 v2 source universe row locator contract bundle hash",
            self.row_locator_contract_bundle_hash,
        )
        require_hash("S27 v2 source universe strict-prior candidate-set hash", self.strict_prior_candidate_set_hash)
        require_hash(
            "S27 v2 source universe canonical row-locator serialization hash",
            self.canonical_row_locator_serialization_hash,
        )
        require_non_empty_tuple("S27 v2 source universe inclusion rules", self.inclusion_rules)
        seen_rule_families: set[str] = set()
        for rule in self.inclusion_rules:
            rule.validate()
            if rule.applies_to_family in seen_rule_families:
                raise CarverBlocked("S27 v2 source universe inclusion rule families must be unique")
            seen_rule_families.add(rule.applies_to_family)
        if tuple(rule.applies_to_family for rule in self.inclusion_rules) != REQUIRED_SOURCE_UNIVERSE_FAMILIES:
            raise CarverBlocked("S27 v2 source universe inclusion rules must match locked family tuple")
        require_non_empty_tuple("S27 v2 source universe family contracts", self.family_contracts)
        seen_contract_families: set[str] = set()
        for contract in self.family_contracts:
            contract.validate()
            if contract.universe_family in seen_contract_families:
                raise CarverBlocked("S27 v2 source universe family contracts must be unique")
            seen_contract_families.add(contract.universe_family)
        if tuple(contract.universe_family for contract in self.family_contracts) != REQUIRED_SOURCE_UNIVERSE_FAMILIES:
            raise CarverBlocked("S27 v2 source universe family contracts must match locked family tuple")
        require_hash(
            "S27 v2 source universe contract bundle hash",
            self.source_universe_contract_bundle_hash,
        )
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 source universe contract must preserve non-authorizations")

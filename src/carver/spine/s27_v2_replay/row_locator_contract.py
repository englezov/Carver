from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_ROW_LOCATOR_CONTRACT_ONLY_STATUS = "S27_V2_ROW_LOCATOR_CONTRACT_ONLY"
PLANNED_ROW_LOCATOR_FAMILY_STATUS = "PLANNED_ROW_LOCATOR_FAMILY_ONLY"

REQUIRED_ROW_LOCATOR_FAMILIES = (
    "DAILY_CONTINUOUS_COMPLETED_BAR",
    "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
    "HOURLY_DECISION_COMPLETED_BAR",
    "HOURLY_FILL_COMPLETED_BAR",
    "SESSION_CALENDAR",
    "ROLL_CALENDAR",
    "COST_PARAMETER",
)


@dataclass(frozen=True)
class RowLocatorFieldBinding:
    row_family: str
    raw_symbol_family: str
    locator_component_names: tuple[str, ...]
    timestamp_component_name: str
    trading_date_component_name: str
    canonical_serialization_policy_hash: str
    row_locator_policy_hash: str

    def validate(self) -> None:
        require_text("S27 v2 row locator field binding row family", self.row_family)
        if self.row_family not in REQUIRED_ROW_LOCATOR_FAMILIES:
            raise CarverBlocked("S27 v2 row locator field binding row family is not locked")
        require_text("S27 v2 row locator field binding raw symbol family", self.raw_symbol_family)
        require_non_empty_tuple("S27 v2 row locator component names", self.locator_component_names)
        seen_components: set[str] = set()
        for component_name in self.locator_component_names:
            require_text("S27 v2 row locator component name", component_name)
            if component_name in seen_components:
                raise CarverBlocked("S27 v2 row locator component names must be unique")
            seen_components.add(component_name)
        require_text("S27 v2 row locator timestamp component name", self.timestamp_component_name)
        require_text("S27 v2 row locator trading-date component name", self.trading_date_component_name)
        if self.timestamp_component_name not in seen_components:
            raise CarverBlocked("S27 v2 row locator timestamp component must be part of locator components")
        if self.trading_date_component_name not in seen_components:
            raise CarverBlocked("S27 v2 row locator trading date component must be part of locator components")
        require_hash(
            "S27 v2 row locator canonical serialization policy hash",
            self.canonical_serialization_policy_hash,
        )
        require_hash("S27 v2 row locator policy hash", self.row_locator_policy_hash)


@dataclass(frozen=True)
class SourceRowFamilyLocatorContract:
    row_family: str
    family_status: str
    raw_file_declaration_hash: str
    parser_family_plan_hash: str
    expected_output_schema_family: str
    field_binding: RowLocatorFieldBinding
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    duplicate_policy_hash: str
    missing_policy_hash: str
    no_future_rows_proof_hash: str
    planned_row_universe_hash: str
    planned_locator_output_hash: str
    family_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 source row locator family", self.row_family)
        if self.row_family not in REQUIRED_ROW_LOCATOR_FAMILIES:
            raise CarverBlocked("S27 v2 source row locator family is not locked")
        require_text("S27 v2 source row locator family status", self.family_status)
        if self.family_status != PLANNED_ROW_LOCATOR_FAMILY_STATUS:
            raise CarverBlocked("S27 v2 source row locator family must remain planned-only")
        require_hash("S27 v2 source row locator raw file declaration hash", self.raw_file_declaration_hash)
        require_hash("S27 v2 source row locator parser family plan hash", self.parser_family_plan_hash)
        require_text("S27 v2 source row locator expected output schema family", self.expected_output_schema_family)
        self.field_binding.validate()
        if self.field_binding.row_family != self.row_family:
            raise CarverBlocked("S27 v2 source row locator field binding family mismatch")
        require_hash("S27 v2 source row locator completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 source row locator strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 source row locator duplicate policy hash", self.duplicate_policy_hash)
        require_hash("S27 v2 source row locator missing policy hash", self.missing_policy_hash)
        require_hash("S27 v2 source row locator no-future-rows proof hash", self.no_future_rows_proof_hash)
        require_hash("S27 v2 source row locator planned row universe hash", self.planned_row_universe_hash)
        require_hash("S27 v2 source row locator planned locator output hash", self.planned_locator_output_hash)
        require_hash("S27 v2 source row locator family contract hash", self.family_contract_hash)


@dataclass(frozen=True)
class SourceRowLocatorContractBundle:
    status: str
    input_directory_declaration_hash: str
    source_universe_manifest_hash: str
    raw_file_hash_set_hash: str
    row_locator_policy_hash: str
    row_family_contracts: tuple[SourceRowFamilyLocatorContract, ...]
    row_locator_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 source row locator contract bundle status", self.status)
        if self.status != S27_V2_ROW_LOCATOR_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 source row locator contract bundle must remain contract-only")
        require_hash(
            "S27 v2 source row locator input directory declaration hash",
            self.input_directory_declaration_hash,
        )
        require_hash("S27 v2 source row locator universe manifest hash", self.source_universe_manifest_hash)
        require_hash("S27 v2 source row locator raw file hash-set hash", self.raw_file_hash_set_hash)
        require_hash("S27 v2 source row locator policy hash", self.row_locator_policy_hash)
        require_non_empty_tuple("S27 v2 source row locator family contracts", self.row_family_contracts)
        seen_families: set[str] = set()
        for contract in self.row_family_contracts:
            contract.validate()
            if contract.row_family in seen_families:
                raise CarverBlocked("S27 v2 source row locator family contracts must be unique")
            if contract.field_binding.row_locator_policy_hash != self.row_locator_policy_hash:
                raise CarverBlocked("S27 v2 source row locator family policy hash mismatch")
            seen_families.add(contract.row_family)
        if tuple(contract.row_family for contract in self.row_family_contracts) != REQUIRED_ROW_LOCATOR_FAMILIES:
            raise CarverBlocked("S27 v2 source row locator families must match the locked family tuple")
        require_hash(
            "S27 v2 source row locator contract bundle hash",
            self.row_locator_contract_bundle_hash,
        )
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 source row locator contract must preserve non-authorizations")

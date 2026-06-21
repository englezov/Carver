from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .parser_output_contract import (
    REQUIRED_PARSER_OUTPUT_ROW_FAMILIES,
    ParserOutputBatchSetContract,
)
from .validation import (
    require_hash,
    require_hash_map_matches_active_authority,
    require_non_empty_tuple,
    require_text,
)


S27_V2_SOURCE_ROW_BATCH_CONTRACT_ONLY_STATUS = "S27_V2_SOURCE_ROW_BATCH_CONTRACT_ONLY"
PLANNED_SOURCE_ROW_BATCH_FAMILY_STATUS = "PLANNED_SOURCE_ROW_BATCH_FAMILY_ONLY"

REQUIRED_SOURCE_ROW_BATCH_FAMILIES = REQUIRED_PARSER_OUTPUT_ROW_FAMILIES

REQUIRED_SOURCE_ROW_SCHEMA_BY_FAMILY = {
    "DAILY_CONTINUOUS_COMPLETED_BAR": "LOCAL_DAILY_SOURCE_ROW",
    "DAILY_CURRENT_CONTRACT_COMPLETED_BAR": "LOCAL_DAILY_SOURCE_ROW",
    "HOURLY_DECISION_COMPLETED_BAR": "LOCAL_HOURLY_SOURCE_ROW",
    "HOURLY_FILL_COMPLETED_BAR": "LOCAL_HOURLY_SOURCE_ROW",
    "SESSION_CALENDAR": "LOCAL_SESSION_SOURCE_ROW",
    "ROLL_CALENDAR": "LOCAL_ROLL_SOURCE_ROW",
    "COST_PARAMETER": "LOCAL_COST_PARAMETER_ROW",
}

REQUIRED_READINESS_STATUS_BY_FAMILY = {
    "DAILY_CONTINUOUS_COMPLETED_BAR": "READY_COMPLETED_BAR",
    "DAILY_CURRENT_CONTRACT_COMPLETED_BAR": "READY_COMPLETED_BAR",
    "HOURLY_DECISION_COMPLETED_BAR": "READY_COMPLETED_BAR",
    "HOURLY_FILL_COMPLETED_BAR": "READY_COMPLETED_BAR",
    "SESSION_CALENDAR": "READY_SESSION_CALENDAR",
    "ROLL_CALENDAR": "READY_ROLL_CALENDAR",
    "COST_PARAMETER": "READY_COST_PARAMETERS",
}


@dataclass(frozen=True)
class SourceRowBatchFamilyContract:
    row_family: str
    family_status: str
    parser_output_family_contract_hash: str
    parser_output_batch_hash: str
    source_row_schema_label: str
    source_row_schema_hash: str
    readiness_status_label: str
    readiness_status_policy_hash: str
    source_universe_family_contract_hash: str
    row_locator_family_contract_hash: str
    row_locator_policy_hash: str
    row_hash_schema_hash: str
    row_ordering_policy_hash: str
    duplicate_policy_hash: str
    missing_policy_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    no_future_rows_proof_hash: str
    row_count_manifest_hash: str
    first_last_row_locator_manifest_hash: str
    source_row_batch_hash: str
    source_row_batch_family_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 source row batch family", self.row_family)
        if self.row_family not in REQUIRED_SOURCE_ROW_BATCH_FAMILIES:
            raise CarverBlocked("S27 v2 source row batch family is not locked")
        require_text("S27 v2 source row batch family status", self.family_status)
        if self.family_status != PLANNED_SOURCE_ROW_BATCH_FAMILY_STATUS:
            raise CarverBlocked("S27 v2 source row batch family must remain planned-only")
        require_hash(
            "S27 v2 source row batch parser output family contract hash",
            self.parser_output_family_contract_hash,
        )
        require_hash("S27 v2 source row batch parser output batch hash", self.parser_output_batch_hash)
        require_text("S27 v2 source row schema label", self.source_row_schema_label)
        if self.source_row_schema_label != REQUIRED_SOURCE_ROW_SCHEMA_BY_FAMILY[self.row_family]:
            raise CarverBlocked("S27 v2 source row schema label must match the locked row family")
        require_hash("S27 v2 source row schema hash", self.source_row_schema_hash)
        require_text("S27 v2 source row readiness status label", self.readiness_status_label)
        if self.readiness_status_label != REQUIRED_READINESS_STATUS_BY_FAMILY[self.row_family]:
            raise CarverBlocked("S27 v2 source row readiness status must match the locked row family")
        require_hash("S27 v2 source row readiness status policy hash", self.readiness_status_policy_hash)
        require_hash(
            "S27 v2 source row batch source universe family contract hash",
            self.source_universe_family_contract_hash,
        )
        require_hash(
            "S27 v2 source row batch row locator family contract hash",
            self.row_locator_family_contract_hash,
        )
        require_hash("S27 v2 source row batch row locator policy hash", self.row_locator_policy_hash)
        require_hash("S27 v2 source row batch row hash schema hash", self.row_hash_schema_hash)
        require_hash("S27 v2 source row batch row ordering policy hash", self.row_ordering_policy_hash)
        require_hash("S27 v2 source row batch duplicate policy hash", self.duplicate_policy_hash)
        require_hash("S27 v2 source row batch missing policy hash", self.missing_policy_hash)
        require_hash("S27 v2 source row batch completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 source row batch strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 source row batch no-future-rows proof hash", self.no_future_rows_proof_hash)
        require_hash("S27 v2 source row batch row-count manifest hash", self.row_count_manifest_hash)
        require_hash(
            "S27 v2 source row batch first/last row-locator manifest hash",
            self.first_last_row_locator_manifest_hash,
        )
        require_hash("S27 v2 source row batch hash", self.source_row_batch_hash)
        require_hash(
            "S27 v2 source row batch family contract hash",
            self.source_row_batch_family_contract_hash,
        )


@dataclass(frozen=True)
class SourceRowBatchSetContract:
    status: str
    parser_output_contract_hash: str
    parsed_output_batch_set_hash: str
    source_universe_contract_bundle_hash: str
    row_locator_contract_bundle_hash: str
    canonical_serialization_policy_hash: str
    source_row_batch_family_contracts: tuple[SourceRowBatchFamilyContract, ...]
    source_row_batch_set_hash: str
    source_row_batch_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 source row batch contract requires parser-output authority"
        )

    def validate_against_parser_output_authority(
        self,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        parser_output_contract.validate()
        self._validate_contract_only_shape()
        self._validate_parser_output_authority(parser_output_contract)

    def _validate_contract_only_shape(self) -> None:
        require_text("S27 v2 source row batch contract status", self.status)
        if self.status != S27_V2_SOURCE_ROW_BATCH_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 source row batch contract must remain contract-only")
        if tuple(REQUIRED_SOURCE_ROW_SCHEMA_BY_FAMILY) != REQUIRED_SOURCE_ROW_BATCH_FAMILIES:
            raise CarverBlocked("S27 v2 source row schema map must cover the locked family tuple")
        if tuple(REQUIRED_READINESS_STATUS_BY_FAMILY) != REQUIRED_SOURCE_ROW_BATCH_FAMILIES:
            raise CarverBlocked("S27 v2 source row readiness map must cover the locked family tuple")
        require_hash("S27 v2 source row batch parser output contract hash", self.parser_output_contract_hash)
        require_hash("S27 v2 source row batch parsed output batch-set hash", self.parsed_output_batch_set_hash)
        require_hash(
            "S27 v2 source row batch source universe contract bundle hash",
            self.source_universe_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source row batch row locator contract bundle hash",
            self.row_locator_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source row batch canonical serialization policy hash",
            self.canonical_serialization_policy_hash,
        )
        require_non_empty_tuple(
            "S27 v2 source row batch family contracts",
            self.source_row_batch_family_contracts,
        )
        seen_families: set[str] = set()
        for contract in self.source_row_batch_family_contracts:
            contract.validate()
            if contract.row_family in seen_families:
                raise CarverBlocked("S27 v2 source row batch families must be unique")
            seen_families.add(contract.row_family)
        if (
            tuple(contract.row_family for contract in self.source_row_batch_family_contracts)
            != REQUIRED_SOURCE_ROW_BATCH_FAMILIES
        ):
            raise CarverBlocked("S27 v2 source row batch families must match the locked family tuple")
        require_hash("S27 v2 source row batch-set hash", self.source_row_batch_set_hash)
        require_hash("S27 v2 source row batch contract hash", self.source_row_batch_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 source row batch contract must preserve non-authorizations")

    def _validate_parser_output_authority(
        self,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        if parser_output_contract.parser_output_contract_hash != self.parser_output_contract_hash:
            raise CarverBlocked("S27 v2 source row batch must bind cited parser output contract")
        if parser_output_contract.parsed_output_batch_set_hash != self.parsed_output_batch_set_hash:
            raise CarverBlocked("S27 v2 source row batch must bind cited parsed output batch set")
        require_hash_map_matches_active_authority(
            "S27 v2 source row batch parser output family contract authority",
            {
                contract.row_family: contract.parser_output_family_contract_hash
                for contract in self.source_row_batch_family_contracts
            },
            {
                contract.row_family: contract.parser_output_family_contract_hash
                for contract in parser_output_contract.parsed_output_family_contracts
            },
            REQUIRED_SOURCE_ROW_BATCH_FAMILIES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source row batch parsed output batch authority",
            {
                contract.row_family: contract.parser_output_batch_hash
                for contract in self.source_row_batch_family_contracts
            },
            {
                contract.row_family: contract.planned_row_batch_hash
                for contract in parser_output_contract.parsed_output_family_contracts
            },
            REQUIRED_SOURCE_ROW_BATCH_FAMILIES,
        )

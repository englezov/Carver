from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .raw_file_hash_contract import REQUIRED_RAW_SOURCE_FILE_FAMILIES
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_PARSER_OUTPUT_CONTRACT_ONLY_STATUS = "S27_V2_PARSER_OUTPUT_CONTRACT_ONLY"
PLANNED_PARSER_OUTPUT_FAMILY_STATUS = "PLANNED_PARSER_OUTPUT_FAMILY_ONLY"

REQUIRED_PARSER_OUTPUT_ROW_FAMILIES = REQUIRED_RAW_SOURCE_FILE_FAMILIES


@dataclass(frozen=True)
class ParserOutputFamilyContract:
    row_family: str
    family_status: str
    raw_file_hash_binding_hash: str
    parser_family_plan_hash: str
    expected_source_row_schema_family: str
    row_locator_family_contract_hash: str
    planned_row_batch_hash: str
    row_hash_schema_hash: str
    row_ordering_policy_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    no_future_rows_proof_hash: str
    no_parser_execution_assertion_label: str
    parser_output_family_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 parser output row family", self.row_family)
        if self.row_family not in REQUIRED_PARSER_OUTPUT_ROW_FAMILIES:
            raise CarverBlocked("S27 v2 parser output row family is not locked")
        require_text("S27 v2 parser output family status", self.family_status)
        if self.family_status != PLANNED_PARSER_OUTPUT_FAMILY_STATUS:
            raise CarverBlocked("S27 v2 parser output family must remain planned-only")
        require_hash("S27 v2 parser output raw file hash binding hash", self.raw_file_hash_binding_hash)
        require_hash("S27 v2 parser output parser family plan hash", self.parser_family_plan_hash)
        require_text(
            "S27 v2 parser output expected source row schema family",
            self.expected_source_row_schema_family,
        )
        if self.expected_source_row_schema_family != self.row_family:
            raise CarverBlocked("S27 v2 parser output source row schema family must match row family")
        require_hash(
            "S27 v2 parser output row locator family contract hash",
            self.row_locator_family_contract_hash,
        )
        require_hash("S27 v2 parser output planned row batch hash", self.planned_row_batch_hash)
        require_hash("S27 v2 parser output row hash schema hash", self.row_hash_schema_hash)
        require_hash("S27 v2 parser output row ordering policy hash", self.row_ordering_policy_hash)
        require_hash("S27 v2 parser output completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 parser output strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 parser output no-future-rows proof hash", self.no_future_rows_proof_hash)
        require_text(
            "S27 v2 parser output no-parser-execution assertion label",
            self.no_parser_execution_assertion_label,
        )
        if self.no_parser_execution_assertion_label != "NO_PARSER_FILE_REPLAY_EXECUTION":
            raise CarverBlocked("S27 v2 parser output contract must assert no parser/file replay execution")
        require_hash(
            "S27 v2 parser output family contract hash",
            self.parser_output_family_contract_hash,
        )


@dataclass(frozen=True)
class ParserOutputBatchSetContract:
    status: str
    raw_file_hash_contract_hash: str
    raw_file_hash_set_hash: str
    parser_plan_bundle_hash: str
    row_locator_contract_bundle_hash: str
    canonical_serialization_policy_hash: str
    parsed_output_family_contracts: tuple[ParserOutputFamilyContract, ...]
    parsed_output_batch_set_hash: str
    parser_output_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 parser output contract status", self.status)
        if self.status != S27_V2_PARSER_OUTPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 parser output contract must remain contract-only")
        require_hash("S27 v2 parser output raw file hash contract hash", self.raw_file_hash_contract_hash)
        require_hash("S27 v2 parser output raw file hash-set hash", self.raw_file_hash_set_hash)
        require_hash("S27 v2 parser output parser plan bundle hash", self.parser_plan_bundle_hash)
        require_hash(
            "S27 v2 parser output row locator contract bundle hash",
            self.row_locator_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 parser output canonical serialization policy hash",
            self.canonical_serialization_policy_hash,
        )
        require_non_empty_tuple(
            "S27 v2 parser output family contracts",
            self.parsed_output_family_contracts,
        )
        seen_families: set[str] = set()
        for contract in self.parsed_output_family_contracts:
            contract.validate()
            if contract.row_family in seen_families:
                raise CarverBlocked("S27 v2 parser output row families must be unique")
            seen_families.add(contract.row_family)
        if (
            tuple(contract.row_family for contract in self.parsed_output_family_contracts)
            != REQUIRED_PARSER_OUTPUT_ROW_FAMILIES
        ):
            raise CarverBlocked("S27 v2 parser output row families must match the locked family tuple")
        require_hash("S27 v2 parsed output batch-set hash", self.parsed_output_batch_set_hash)
        require_hash("S27 v2 parser output contract hash", self.parser_output_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 parser output contract must preserve non-authorizations")

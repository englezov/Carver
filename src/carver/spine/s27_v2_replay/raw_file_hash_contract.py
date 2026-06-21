from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .row_locator_contract import REQUIRED_ROW_LOCATOR_FAMILIES
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_RAW_FILE_HASH_CONTRACT_ONLY_STATUS = "S27_V2_RAW_FILE_HASH_CONTRACT_ONLY"
PLANNED_RAW_FILE_HASH_FAMILY_STATUS = "PLANNED_RAW_FILE_HASH_FAMILY_ONLY"

REQUIRED_RAW_SOURCE_FILE_FAMILIES = REQUIRED_ROW_LOCATOR_FAMILIES


@dataclass(frozen=True)
class RawSourceFileHashBinding:
    file_family: str
    family_status: str
    local_file_declaration_hash: str
    declared_path_label_hash: str
    file_sha256: str
    parser_family_plan_hash: str
    expected_output_row_family: str
    completed_bar_policy_hash: str
    no_provider_no_download_assertion_label: str
    file_hash_binding_hash: str

    def validate(self) -> None:
        require_text("S27 v2 raw source file family", self.file_family)
        if self.file_family not in REQUIRED_RAW_SOURCE_FILE_FAMILIES:
            raise CarverBlocked("S27 v2 raw source file family is not locked")
        require_text("S27 v2 raw source file family status", self.family_status)
        if self.family_status != PLANNED_RAW_FILE_HASH_FAMILY_STATUS:
            raise CarverBlocked("S27 v2 raw source file hash family must remain planned-only")
        require_hash("S27 v2 raw source local file declaration hash", self.local_file_declaration_hash)
        require_hash("S27 v2 raw source declared path label hash", self.declared_path_label_hash)
        require_hash("S27 v2 raw source file SHA256", self.file_sha256)
        require_hash("S27 v2 raw source parser family plan hash", self.parser_family_plan_hash)
        require_text("S27 v2 raw source expected output row family", self.expected_output_row_family)
        if self.expected_output_row_family != self.file_family:
            raise CarverBlocked("S27 v2 raw source expected output row family must match file family")
        require_hash("S27 v2 raw source completed-bar policy hash", self.completed_bar_policy_hash)
        require_text(
            "S27 v2 raw source no-provider/no-download assertion label",
            self.no_provider_no_download_assertion_label,
        )
        if self.no_provider_no_download_assertion_label != "NO_PROVIDER_API_NO_DOWNLOAD":
            raise CarverBlocked("S27 v2 raw source file hash binding must assert NO_PROVIDER_API_NO_DOWNLOAD")
        require_hash("S27 v2 raw source file hash binding hash", self.file_hash_binding_hash)


@dataclass(frozen=True)
class RawSourceFileHashSetContract:
    status: str
    input_directory_declaration_hash: str
    source_universe_manifest_hash: str
    parser_plan_bundle_hash: str
    raw_file_hash_bindings: tuple[RawSourceFileHashBinding, ...]
    raw_file_hash_set_hash: str
    no_download_policy_hash: str
    raw_file_hash_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 raw file hash contract status", self.status)
        if self.status != S27_V2_RAW_FILE_HASH_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 raw file hash contract must remain contract-only")
        require_hash(
            "S27 v2 raw file hash input directory declaration hash",
            self.input_directory_declaration_hash,
        )
        require_hash("S27 v2 raw file hash source universe manifest hash", self.source_universe_manifest_hash)
        require_hash("S27 v2 raw file hash parser plan bundle hash", self.parser_plan_bundle_hash)
        require_non_empty_tuple("S27 v2 raw source file hash bindings", self.raw_file_hash_bindings)
        seen_families: set[str] = set()
        for binding in self.raw_file_hash_bindings:
            binding.validate()
            if binding.file_family in seen_families:
                raise CarverBlocked("S27 v2 raw source file hash families must be unique")
            seen_families.add(binding.file_family)
        if tuple(binding.file_family for binding in self.raw_file_hash_bindings) != REQUIRED_RAW_SOURCE_FILE_FAMILIES:
            raise CarverBlocked("S27 v2 raw source file hash families must match the locked family tuple")
        require_hash("S27 v2 raw file hash-set hash", self.raw_file_hash_set_hash)
        require_hash("S27 v2 raw file no-download policy hash", self.no_download_policy_hash)
        require_hash("S27 v2 raw file hash contract hash", self.raw_file_hash_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 raw file hash contract must preserve non-authorizations")

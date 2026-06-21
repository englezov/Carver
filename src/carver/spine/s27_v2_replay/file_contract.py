from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .row_locator_contract import REQUIRED_ROW_LOCATOR_FAMILIES
from .validation import require_hash, require_non_empty_tuple, require_text, require_tuple


S27_V2_LOCAL_FILE_DECLARATION_ONLY_STATUS = "S27_V2_LOCAL_FILE_DECLARATION_ONLY"
S27_V2_RAW_SOURCE_FILE_DECLARATION_ONLY_STATUS = "S27_V2_RAW_SOURCE_FILE_DECLARATION_ONLY"
S27_V2_PARSER_SOURCE_DECLARATION_ONLY_STATUS = "S27_V2_PARSER_SOURCE_DECLARATION_ONLY"
S27_V2_RUNTIME_DEPENDENCY_DECLARATION_ONLY_STATUS = "S27_V2_RUNTIME_DEPENDENCY_DECLARATION_ONLY"
S27_V2_REPLAY_INPUT_DIRECTORY_DECLARATION_ONLY_STATUS = "S27_V2_REPLAY_INPUT_DIRECTORY_DECLARATION_ONLY"

REQUIRED_REPLAY_INPUT_PARSER_SOURCE_NAMES = (
    "DAILY_COMPLETED_BAR_PARSER_PLAN",
    "HOURLY_COMPLETED_BAR_PARSER_PLAN",
    "SESSION_CALENDAR_PARSER_PLAN",
    "ROLL_CALENDAR_PARSER_PLAN",
    "COST_PARAMETER_PARSER_PLAN",
)

REQUIRED_REPLAY_INPUT_PARSER_OUTPUT_ROW_FAMILY_LABEL_BY_NAME = {
    "DAILY_COMPLETED_BAR_PARSER_PLAN": "DAILY_COMPLETED_BAR_OUTPUT_ROWS",
    "HOURLY_COMPLETED_BAR_PARSER_PLAN": "HOURLY_COMPLETED_BAR_OUTPUT_ROWS",
    "SESSION_CALENDAR_PARSER_PLAN": "SESSION_CALENDAR_OUTPUT_ROWS",
    "ROLL_CALENDAR_PARSER_PLAN": "ROLL_CALENDAR_OUTPUT_ROWS",
    "COST_PARAMETER_PARSER_PLAN": "COST_PARAMETER_OUTPUT_ROWS",
}

REQUIRED_REPLAY_INPUT_PARSER_OUTPUT_ROW_FAMILIES_BY_NAME = {
    "DAILY_COMPLETED_BAR_PARSER_PLAN": (
        "DAILY_CONTINUOUS_COMPLETED_BAR",
        "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
    ),
    "HOURLY_COMPLETED_BAR_PARSER_PLAN": (
        "HOURLY_DECISION_COMPLETED_BAR",
        "HOURLY_FILL_COMPLETED_BAR",
    ),
    "SESSION_CALENDAR_PARSER_PLAN": ("SESSION_CALENDAR",),
    "ROLL_CALENDAR_PARSER_PLAN": ("ROLL_CALENDAR",),
    "COST_PARAMETER_PARSER_PLAN": ("COST_PARAMETER",),
}


@dataclass(frozen=True)
class LocalFileDeclaration:
    declared_path: str
    expected_artifact_type: str
    expected_sha256: str
    expected_row_family: str
    expected_timezone_policy_hash: str
    canonical_serialization_policy_hash: str
    operator_authorization_label: str
    no_provider_no_download_assertion_label: str
    declaration_status: str = S27_V2_LOCAL_FILE_DECLARATION_ONLY_STATUS

    def validate(self) -> None:
        require_text("S27 v2 local file declaration status", self.declaration_status)
        if self.declaration_status != S27_V2_LOCAL_FILE_DECLARATION_ONLY_STATUS:
            raise CarverBlocked("S27 v2 local file declaration must remain declaration-only")
        require_text("S27 v2 local file declared path", self.declared_path)
        require_text("S27 v2 local file expected artifact type", self.expected_artifact_type)
        require_hash("S27 v2 local file expected SHA256", self.expected_sha256)
        require_text("S27 v2 local file expected row family", self.expected_row_family)
        if self.expected_row_family not in REQUIRED_ROW_LOCATOR_FAMILIES:
            raise CarverBlocked("S27 v2 local file expected row family must be locked")
        require_hash("S27 v2 local file timezone policy hash", self.expected_timezone_policy_hash)
        require_hash(
            "S27 v2 local file canonical serialization policy hash",
            self.canonical_serialization_policy_hash,
        )
        require_text("S27 v2 local file operator authorization label", self.operator_authorization_label)
        require_text(
            "S27 v2 local file no-provider/no-download-assertion label",
            self.no_provider_no_download_assertion_label,
        )
        if self.no_provider_no_download_assertion_label != "NO_PROVIDER_API_NO_DOWNLOAD":
            raise CarverBlocked("S27 v2 local file declaration must assert NO_PROVIDER_API_NO_DOWNLOAD")


@dataclass(frozen=True)
class RawSourceFileDeclaration:
    local_file: LocalFileDeclaration
    raw_symbol_family: str
    completed_bar_policy_hash: str
    row_locator_policy_hash: str
    strict_prior_policy_hash: str
    declaration_status: str = S27_V2_RAW_SOURCE_FILE_DECLARATION_ONLY_STATUS

    def validate(self) -> None:
        require_text("S27 v2 raw source file declaration status", self.declaration_status)
        if self.declaration_status != S27_V2_RAW_SOURCE_FILE_DECLARATION_ONLY_STATUS:
            raise CarverBlocked("S27 v2 raw source file declaration must remain declaration-only")
        self.local_file.validate()
        require_text("S27 v2 raw source file symbol family", self.raw_symbol_family)
        require_hash("S27 v2 raw source completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 raw source row-locator policy hash", self.row_locator_policy_hash)
        require_hash("S27 v2 raw source strict-prior policy hash", self.strict_prior_policy_hash)


@dataclass(frozen=True)
class ParserSourceDeclaration:
    parser_name: str
    parser_source_hash: str
    parser_contract_hash: str
    expected_input_artifact_type: str
    expected_output_row_family: str
    expected_output_row_families: tuple[str, ...]
    declaration_status: str = S27_V2_PARSER_SOURCE_DECLARATION_ONLY_STATUS

    def validate(self) -> None:
        require_text("S27 v2 parser source declaration status", self.declaration_status)
        if self.declaration_status != S27_V2_PARSER_SOURCE_DECLARATION_ONLY_STATUS:
            raise CarverBlocked("S27 v2 parser source declaration must remain declaration-only")
        require_text("S27 v2 parser source name", self.parser_name)
        if self.parser_name not in REQUIRED_REPLAY_INPUT_PARSER_SOURCE_NAMES:
            raise CarverBlocked("S27 v2 parser source name must be locked")
        require_hash("S27 v2 parser source hash", self.parser_source_hash)
        require_hash("S27 v2 parser contract hash", self.parser_contract_hash)
        require_text("S27 v2 parser expected input artifact type", self.expected_input_artifact_type)
        require_text("S27 v2 parser expected output row family label", self.expected_output_row_family)
        if (
            self.expected_output_row_family
            != REQUIRED_REPLAY_INPUT_PARSER_OUTPUT_ROW_FAMILY_LABEL_BY_NAME[self.parser_name]
        ):
            raise CarverBlocked("S27 v2 parser output row family label must match locked parser mapping")
        require_tuple("S27 v2 parser expected output row families", self.expected_output_row_families)
        if (
            self.expected_output_row_families
            != REQUIRED_REPLAY_INPUT_PARSER_OUTPUT_ROW_FAMILIES_BY_NAME[self.parser_name]
        ):
            raise CarverBlocked("S27 v2 parser output row families must match locked parser mapping")


@dataclass(frozen=True)
class RuntimeDependencyDeclaration:
    dependency_name: str
    dependency_version_label: str
    dependency_manifest_hash: str
    runtime_environment_hash: str
    declaration_status: str = S27_V2_RUNTIME_DEPENDENCY_DECLARATION_ONLY_STATUS

    def validate(self) -> None:
        require_text("S27 v2 runtime dependency declaration status", self.declaration_status)
        if self.declaration_status != S27_V2_RUNTIME_DEPENDENCY_DECLARATION_ONLY_STATUS:
            raise CarverBlocked("S27 v2 runtime dependency declaration must remain declaration-only")
        require_text("S27 v2 runtime dependency name", self.dependency_name)
        require_text("S27 v2 runtime dependency version label", self.dependency_version_label)
        require_hash("S27 v2 runtime dependency manifest hash", self.dependency_manifest_hash)
        require_hash("S27 v2 runtime environment hash", self.runtime_environment_hash)


@dataclass(frozen=True)
class ReplayInputDirectoryDeclaration:
    declared_path: str
    source_universe_manifest_hash: str
    raw_file_hash_set_hash: str
    row_locator_hash: str
    raw_source_files: tuple[RawSourceFileDeclaration, ...]
    parser_sources: tuple[ParserSourceDeclaration, ...]
    runtime_dependencies: tuple[RuntimeDependencyDeclaration, ...]
    input_directory_declaration_hash: str
    declaration_status: str = S27_V2_REPLAY_INPUT_DIRECTORY_DECLARATION_ONLY_STATUS
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 replay input directory declaration status", self.declaration_status)
        if self.declaration_status != S27_V2_REPLAY_INPUT_DIRECTORY_DECLARATION_ONLY_STATUS:
            raise CarverBlocked("S27 v2 replay input directory must remain declaration-only")
        require_text("S27 v2 replay input directory declared path", self.declared_path)
        require_hash("S27 v2 source universe manifest hash", self.source_universe_manifest_hash)
        require_hash("S27 v2 raw file hash-set hash", self.raw_file_hash_set_hash)
        require_hash("S27 v2 source row locator hash", self.row_locator_hash)
        require_non_empty_tuple("S27 v2 raw source file declarations", self.raw_source_files)
        for declaration in self.raw_source_files:
            declaration.validate()
        if tuple(declaration.local_file.expected_row_family for declaration in self.raw_source_files) != REQUIRED_ROW_LOCATOR_FAMILIES:
            raise CarverBlocked("S27 v2 raw source file declarations must match the locked row-family tuple")
        require_non_empty_tuple("S27 v2 parser source declarations", self.parser_sources)
        seen_parser_names: set[str] = set()
        for declaration in self.parser_sources:
            declaration.validate()
            if declaration.parser_name in seen_parser_names:
                raise CarverBlocked("S27 v2 parser source declarations must be unique")
            seen_parser_names.add(declaration.parser_name)
        if tuple(declaration.parser_name for declaration in self.parser_sources) != REQUIRED_REPLAY_INPUT_PARSER_SOURCE_NAMES:
            raise CarverBlocked("S27 v2 parser source declarations must match the locked parser-source tuple")
        parser_output_families = tuple(
            row_family
            for declaration in self.parser_sources
            for row_family in declaration.expected_output_row_families
        )
        if parser_output_families != REQUIRED_ROW_LOCATOR_FAMILIES:
            raise CarverBlocked("S27 v2 parser source output families must match the locked row-family tuple")
        require_non_empty_tuple("S27 v2 runtime dependency declarations", self.runtime_dependencies)
        for declaration in self.runtime_dependencies:
            declaration.validate()
        require_hash("S27 v2 input directory declaration hash", self.input_directory_declaration_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 replay input directory declaration must preserve non-authorizations")

from __future__ import annotations

from csv import DictReader
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable

from ..m0 import CarverBlocked
from .canonical_hash import CanonicalSerializationPolicy
from .canonical_hash import HashedArtifact
from .construction_contract import (
    PLANNED_CONSTRUCTION_PHASES,
    REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE,
    S27_V2_CONSTRUCTION_SCAFFOLD_ONLY_STATUS,
    ConstructionArtifactReference,
    ConstructionPhaseBoundary,
    ParserFileReplayConstructionContract,
)
from .file_contract import RawSourceFileDeclaration, ReplayInputDirectoryDeclaration
from .constants import (
    ACTIVE_EVIDENCE_STATUS_LABEL,
    REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES,
    REQUIRED_UNRESOLVED_GATE_LABELS,
    S27_V2_REPLAY_NON_AUTHORIZATION,
    S27_V2_TRUSTED_REPLAY_BUNDLE_STATUS,
)
from .cost_contract import (
    PLANNED_COST_COMPONENT_STATUS,
    REQUIRED_COST_BRANCH_LABELS,
    REQUIRED_COST_COMPONENT_FAMILIES,
    REQUIRED_COST_INVARIANTS,
    REQUIRED_SPREAD_SPACE_LABELS,
    S27_V2_COST_CONTRACT_ONLY_STATUS,
    CostBranchContract,
    CostComponentContract,
    CostContractBundle,
    CostInvariantContract,
    CostSourceBinding,
    SpreadSpaceContract,
)
from .cost_input_contract import (
    COST_INPUT_NOT_APPLICABLE,
    PLANNED_COST_INPUT_STATUS,
    REQUIRED_COST_BRANCH_BY_COST_INPUT,
    REQUIRED_COST_DEPENDENCIES_BY_COMPONENT,
    REQUIRED_COST_DEPENDENCIES_BY_INVARIANT,
    REQUIRED_COST_INPUTS,
    REQUIRED_CURRENCY_PROOF_BY_COST_INPUT,
    REQUIRED_FILL_LEDGER_OUTPUT_BY_COST_INPUT,
    REQUIRED_MULTIPLIER_PROOF_BY_COST_INPUT,
    REQUIRED_POLICY_LABEL_BY_COST_INPUT,
    REQUIRED_SOURCE_KIND_BY_COST_INPUT,
    REQUIRED_SPREAD_SPACE_BY_COST_INPUT,
    S27_V2_COST_INPUT_CONTRACT_ONLY_STATUS,
    CostDependencyBindingContract,
    CostInputContractBundle,
    CostInputFieldContract,
)
from .evidence_manifest import EvidenceManifest, EvidenceManifestEntry
from .fill_contract import (
    PLANNED_FILL_COMPONENT_STATUS,
    REQUIRED_FILL_BRANCH_LABELS,
    REQUIRED_FILL_COMPONENT_FAMILIES,
    REQUIRED_FILL_INVARIANTS,
    REQUIRED_FILL_PRICE_PROVENANCE_LABELS,
    S27_V2_FILL_CONTRACT_ONLY_STATUS,
    FillBranchContract,
    FillComponentContract,
    FillContractBundle,
    FillInvariantContract,
    FillPriceProvenanceContract,
    FillSourceBinding,
)
from .fill_input_contract import (
    FILL_INPUT_NOT_APPLICABLE,
    FILL_SOURCE_ROW_MANIFEST_FIELD,
    PLANNED_FILL_INPUT_STATUS,
    REQUIRED_FILL_BRANCH_BY_FILL_INPUT,
    REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT,
    REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT,
    REQUIRED_FILL_INPUTS,
    REQUIRED_FILL_PRICE_PROVENANCE_BY_FILL_INPUT,
    REQUIRED_ORDER_LEDGER_OUTPUT_BY_FILL_INPUT,
    REQUIRED_POLICY_LABEL_BY_FILL_INPUT,
    REQUIRED_SOURCE_KIND_BY_FILL_INPUT,
    REQUIRED_SOURCE_ROW_PROOF_BY_FILL_INPUT,
    REQUIRED_WORKING_ORDER_TRANSITION_OUTPUT_BY_FILL_INPUT,
    S27_V2_FILL_INPUT_CONTRACT_ONLY_STATUS,
    FillDependencyBindingContract,
    FillInputContractBundle,
    FillInputFieldContract,
)
from .forecast_contract import (
    PLANNED_FORECAST_COMPONENT_STATUS,
    REQUIRED_FORECAST_COMPONENT_FAMILIES,
    REQUIRED_FORECAST_DECISION_BRANCHES,
    REQUIRED_FORECAST_INVARIANTS,
    S27_V2_FORECAST_CONTRACT_ONLY_STATUS,
    ForecastComponentContract,
    ForecastContractBundle,
    ForecastDecisionBranchContract,
    ForecastInvariantContract,
    ForecastSourceBinding,
)
from .forecast_input_contract import (
    FORECAST_INPUT_NOT_APPLICABLE,
    PLANNED_FORECAST_INPUT_STATUS,
    REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT,
    REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH,
    REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT,
    REQUIRED_FORECAST_INPUTS,
    REQUIRED_POLICY_LABEL_BY_FORECAST_INPUT,
    REQUIRED_RUNTIME_HISTORY_INPUT_BY_FORECAST_INPUT,
    REQUIRED_RUNTIME_STATE_BY_FORECAST_INPUT,
    REQUIRED_SOURCE_KIND_BY_FORECAST_INPUT,
    REQUIRED_VQM_COMPONENT_BY_FORECAST_INPUT,
    S27_V2_FORECAST_INPUT_CONTRACT_ONLY_STATUS,
    ForecastDependencyBindingContract,
    ForecastInputContractBundle,
    ForecastInputFieldContract,
)
from .level_compatibility_contract import (
    PLANNED_LEVEL_COMPATIBILITY_PROOF_STATUS,
    REQUIRED_LEVEL_COMPATIBILITY_PROOFS,
    S27_V2_LEVEL_COMPATIBILITY_CONTRACT_ONLY_STATUS,
    LevelCompatibilityContractBundle,
    LevelCompatibilityProofContract,
    LevelCompatibilitySourceBinding,
    LevelCompatibilityVerdictContract,
)
from .level_compatibility_input_contract import (
    PLANNED_LEVEL_COMPATIBILITY_INPUT_STATUS,
    REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
    REQUIRED_LEVEL_COMPATIBILITY_INPUTS_BY_PROOF,
    REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT,
    S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_ONLY_STATUS,
    LevelCompatibilityInputContractBundle,
    LevelCompatibilityInputFieldContract,
    LevelCompatibilityProofInputBindingContract,
)
from .parser_output_contract import (
    PLANNED_PARSER_OUTPUT_FAMILY_STATUS,
    S27_V2_PARSER_OUTPUT_CONTRACT_ONLY_STATUS,
    ParserOutputBatchSetContract,
    ParserOutputFamilyContract,
)
from .parser_plan import ParserPlanBundle
from .pnl_contract import (
    PLANNED_PNL_COMPONENT_STATUS,
    REQUIRED_PNL_BRIDGE_LABELS,
    REQUIRED_PNL_COMPONENT_FAMILIES,
    REQUIRED_PNL_INVARIANTS,
    REQUIRED_PNL_PRICE_SOURCE_LABELS,
    S27_V2_PNL_CONTRACT_ONLY_STATUS,
    PnlBridgeContract,
    PnlComponentContract,
    PnlContractBundle,
    PnlInvariantContract,
    PnlPriceSourceContract,
    PnlSourceBinding,
)
from .pnl_input_contract import (
    PNL_INPUT_NOT_APPLICABLE,
    PNL_PRICE_ROW_MANIFEST_FIELD,
    PLANNED_PNL_INPUT_STATUS,
    REQUIRED_BRIDGE_PROOF_BY_PNL_INPUT,
    REQUIRED_COST_HASH_SET_OUTPUT_BY_PNL_INPUT,
    REQUIRED_CURRENCY_PROOF_BY_PNL_INPUT,
    REQUIRED_FILL_HASH_SET_OUTPUT_BY_PNL_INPUT,
    REQUIRED_MULTIPLIER_PROOF_BY_PNL_INPUT,
    REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT,
    REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT,
    REQUIRED_PNL_INPUTS,
    REQUIRED_POLICY_LABEL_BY_PNL_INPUT,
    REQUIRED_POSITION_SOURCE_OUTPUT_BY_PNL_INPUT,
    REQUIRED_PRICE_ROW_PROOF_BY_PNL_INPUT,
    REQUIRED_PRICE_SOURCE_BY_PNL_INPUT,
    REQUIRED_SOURCE_KIND_BY_PNL_INPUT,
    REQUIRED_SOURCE_UNIVERSE_OUTPUT_BY_PNL_INPUT,
    REQUIRED_TRANSITION_LEDGER_OUTPUT_BY_PNL_INPUT,
    REQUIRED_TRUST_ROOT_OUTPUT_BY_PNL_INPUT,
    S27_V2_PNL_INPUT_CONTRACT_ONLY_STATUS,
    PnlDependencyBindingContract,
    PnlInputContractBundle,
    PnlInputFieldContract,
)
from .order_contract import (
    PLANNED_ORDER_COMPONENT_STATUS,
    REQUIRED_ORDER_COMPONENT_FAMILIES,
    REQUIRED_ORDER_INVARIANTS,
    REQUIRED_ORDER_KIND_LABELS,
    REQUIRED_ORDER_TRANSITION_KIND_LABELS,
    S27_V2_ORDER_CONTRACT_ONLY_STATUS,
    OrderComponentContract,
    OrderContractBundle,
    OrderInvariantContract,
    OrderKindContract,
    OrderSourceBinding,
    OrderTransitionKindContract,
)
from .order_input_contract import (
    ORDER_INPUT_NOT_APPLICABLE,
    PLANNED_ORDER_INPUT_STATUS,
    REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT,
    REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT,
    REQUIRED_ORDER_INPUTS,
    REQUIRED_ORDER_KIND_BY_ORDER_INPUT,
    REQUIRED_ORDER_STATE_CONTEXT_BY_ORDER_INPUT,
    REQUIRED_ORDER_TRANSITION_KIND_BY_ORDER_INPUT,
    REQUIRED_POLICY_LABEL_BY_ORDER_INPUT,
    REQUIRED_POSITION_COMPONENT_BY_ORDER_INPUT,
    REQUIRED_POSITION_LEDGER_OUTPUT_BY_ORDER_INPUT,
    REQUIRED_SOURCE_KIND_BY_ORDER_INPUT,
    S27_V2_ORDER_INPUT_CONTRACT_ONLY_STATUS,
    OrderDependencyBindingContract,
    OrderInputContractBundle,
    OrderInputFieldContract,
)
from .position_contract import (
    PLANNED_POSITION_COMPONENT_STATUS,
    REQUIRED_POSITION_COMPONENT_FAMILIES,
    REQUIRED_POSITION_INVARIANTS,
    REQUIRED_ROUNDING_POLICY_LABELS,
    S27_V2_POSITION_CONTRACT_ONLY_STATUS,
    PositionComponentContract,
    PositionContractBundle,
    PositionInvariantContract,
    PositionRoundingPolicyContract,
    PositionSourceBinding,
)
from .position_input_contract import (
    PLANNED_POSITION_INPUT_STATUS,
    POSITION_INPUT_NOT_APPLICABLE,
    REQUIRED_FORECAST_COMPONENT_BY_POSITION_INPUT,
    REQUIRED_FORECAST_LEDGER_OUTPUT_BY_POSITION_INPUT,
    REQUIRED_POLICY_LABEL_BY_POSITION_INPUT,
    REQUIRED_POSITION_DEPENDENCIES_BY_COMPONENT,
    REQUIRED_POSITION_DEPENDENCIES_BY_INVARIANT,
    REQUIRED_POSITION_INPUTS,
    REQUIRED_POSITION_STATE_CONTEXT_BY_POSITION_INPUT,
    REQUIRED_ROUNDING_POLICY_BY_POSITION_INPUT,
    REQUIRED_SOURCE_KIND_BY_POSITION_INPUT,
    S27_V2_POSITION_INPUT_CONTRACT_ONLY_STATUS,
    PositionDependencyBindingContract,
    PositionInputContractBundle,
    PositionInputFieldContract,
)
from .raw_file_hash_contract import (
    PLANNED_RAW_FILE_HASH_FAMILY_STATUS,
    S27_V2_RAW_FILE_HASH_CONTRACT_ONLY_STATUS,
    RawSourceFileHashBinding,
    RawSourceFileHashSetContract,
)
from .row_locator_contract import REQUIRED_ROW_LOCATOR_FAMILIES, SourceRowLocatorContractBundle
from .runtime_history_contract import (
    PLANNED_RUNTIME_HISTORY_STATE_STATUS,
    REQUIRED_RUNTIME_STATE_FAMILIES,
    REQUIRED_VQM_COMPONENTS,
    S27_V2_RUNTIME_HISTORY_CONTRACT_ONLY_STATUS,
    RuntimeHistoryContractBundle,
    RuntimeHistorySourceBinding,
    RuntimeStateFamilyContract,
    VqmComponentContract,
)
from .runtime_history_input_contract import (
    PLANNED_RUNTIME_HISTORY_INPUT_STATUS,
    REQUIRED_LEVEL_COMPATIBILITY_INPUT_BY_RUNTIME_HISTORY_INPUT,
    REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT,
    REQUIRED_RUNTIME_HISTORY_DEPENDENCIES_BY_VQM_COMPONENT,
    REQUIRED_RUNTIME_HISTORY_INPUTS,
    REQUIRED_RUNTIME_HISTORY_INPUTS_BY_STATE,
    S27_V2_RUNTIME_HISTORY_INPUT_CONTRACT_ONLY_STATUS,
    RuntimeHistoryInputContractBundle,
    RuntimeHistoryInputFieldContract,
    RuntimeHistoryLevelCompatibilityInputBindingContract,
    RuntimeHistoryStateInputBindingContract,
    RuntimeHistoryVqmDependencyBindingContract,
)
from .source_row_batch_contract import (
    PLANNED_SOURCE_ROW_BATCH_FAMILY_STATUS,
    REQUIRED_READINESS_STATUS_BY_FAMILY,
    REQUIRED_SOURCE_ROW_SCHEMA_BY_FAMILY,
    S27_V2_SOURCE_ROW_BATCH_CONTRACT_ONLY_STATUS,
    SourceRowBatchFamilyContract,
    SourceRowBatchSetContract,
)
from .source_input_manifest_contract import (
    PLANNED_SOURCE_INPUT_MANIFEST_FIELD_STATUS,
    REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS,
    REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD,
    S27_V2_SOURCE_INPUT_MANIFEST_CONTRACT_ONLY_STATUS,
    SourceInputManifestContractBundle,
    SourceInputManifestFieldContract,
)
from .source_input_selection_contract import (
    PLANNED_SOURCE_INPUT_ROLE_STATUS,
    PLANNED_SOURCE_ROW_SELECTION_AUTHORITY_STATUS,
    PLANNED_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_STATUS,
    REQUIRED_SOURCE_INPUT_ROLES,
    REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE,
    S27_V2_SOURCE_INPUT_SELECTION_CONTRACT_ONLY_STATUS,
    SourceInputRoleSelectionContract,
    SourceInputSelectionContractBundle,
    SourceRowSelectionAuthorityContract,
    SourceRowSelectionExternalAuthorityHandle,
)
from .source_rows import (
    LocalCostParameterRow,
    LocalDailySourceRow,
    LocalHourlySourceRow,
    LocalRollSourceRow,
    LocalSessionSourceRow,
)
from .source_universe_contract import SourceUniverseContractBundle
from .trust_root import ReplayTrustRoot
from .trusted_bundle_contract import (
    PLANNED_TRUSTED_BUNDLE_INPUT_STATUS,
    REQUIRED_BUNDLE_DEPENDENCIES_BY_COMPONENT,
    REQUIRED_BUNDLE_DEPENDENCIES_BY_INVARIANT,
    REQUIRED_BUNDLE_STATUS_BY_INPUT,
    REQUIRED_CONSTRUCTION_CONTRACT_OUTPUT_BY_BUNDLE_INPUT,
    REQUIRED_EVIDENCE_MANIFEST_OUTPUT_BY_BUNDLE_INPUT,
    REQUIRED_LOCAL_AUDIT_OUTPUT_BY_BUNDLE_INPUT,
    REQUIRED_POLICY_LABEL_BY_BUNDLE_INPUT,
    REQUIRED_PROVENANCE_LEDGER_OUTPUT_BY_BUNDLE_INPUT,
    REQUIRED_SOURCE_KIND_BY_TRUSTED_BUNDLE_INPUT,
    REQUIRED_TRUSTED_BUNDLE_COMPONENTS,
    REQUIRED_TRUSTED_BUNDLE_INPUTS,
    REQUIRED_TRUSTED_BUNDLE_INVARIANTS,
    REQUIRED_TRUST_ROOT_OUTPUT_BY_BUNDLE_INPUT,
    REQUIRED_VALIDATION_CONTRACT_OUTPUT_BY_BUNDLE_INPUT,
    REQUIRED_VALIDATION_INPUT_CONTRACT_OUTPUT_BY_BUNDLE_INPUT,
    REQUIRED_VALIDATION_LEDGER_OUTPUT_BY_BUNDLE_INPUT,
    S27_V2_TRUSTED_BUNDLE_CONTRACT_ONLY_STATUS,
    TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE,
    TrustedBundleContractBundle,
    TrustedBundleDependencyBindingContract,
    TrustedBundleInputFieldContract,
)
from .validation_contract import (
    PLANNED_VALIDATION_COMPONENT_STATUS,
    REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS,
    REQUIRED_VALIDATION_COMPONENT_FAMILIES,
    REQUIRED_VALIDATION_INVARIANTS,
    REQUIRED_VALIDATION_LEDGER_LABELS,
    S27_V2_VALIDATION_CONTRACT_ONLY_STATUS,
    ValidationAuditCheckpointContract,
    ValidationComponentContract,
    ValidationContractBundle,
    ValidationInvariantContract,
    ValidationLedgerContract,
    ValidationSourceBinding,
)
from .validation_input_contract import (
    PLANNED_VALIDATION_INPUT_STATUS,
    REQUIRED_EVIDENCE_MANIFEST_OUTPUT_BY_VALIDATION_INPUT,
    REQUIRED_LOCAL_AUDIT_SCHEMA_OUTPUT_BY_VALIDATION_INPUT,
    REQUIRED_PNL_CONTRACT_OUTPUT_BY_VALIDATION_INPUT,
    REQUIRED_PNL_INPUT_CONTRACT_OUTPUT_BY_VALIDATION_INPUT,
    REQUIRED_POLICY_LABEL_BY_VALIDATION_INPUT,
    REQUIRED_PROVENANCE_SCHEMA_OUTPUT_BY_VALIDATION_INPUT,
    REQUIRED_SOURCE_INPUT_MANIFEST_OUTPUT_BY_VALIDATION_INPUT,
    REQUIRED_SOURCE_KIND_BY_VALIDATION_INPUT,
    REQUIRED_TRUST_ROOT_OUTPUT_BY_VALIDATION_INPUT,
    REQUIRED_UNRESOLVED_GATE_SET_BY_VALIDATION_INPUT,
    REQUIRED_VALIDATION_DEPENDENCIES_BY_AUDIT_CHECKPOINT,
    REQUIRED_VALIDATION_DEPENDENCIES_BY_COMPONENT,
    REQUIRED_VALIDATION_DEPENDENCIES_BY_INVARIANT,
    REQUIRED_VALIDATION_DEPENDENCIES_BY_LEDGER,
    REQUIRED_VALIDATION_INPUTS,
    REQUIRED_VALIDATION_SCHEMA_OUTPUT_BY_VALIDATION_INPUT,
    S27_V2_VALIDATION_INPUT_CONTRACT_ONLY_STATUS,
    VALIDATION_INPUT_NOT_APPLICABLE,
    ValidationDependencyBindingContract,
    ValidationInputContractBundle,
    ValidationInputFieldContract,
)


ROW_FAMILY_TO_PARSER_NAME = {
    "DAILY_CONTINUOUS_COMPLETED_BAR": "DAILY_COMPLETED_BAR_PARSER_PLAN",
    "DAILY_CURRENT_CONTRACT_COMPLETED_BAR": "DAILY_COMPLETED_BAR_PARSER_PLAN",
    "HOURLY_DECISION_COMPLETED_BAR": "HOURLY_COMPLETED_BAR_PARSER_PLAN",
    "HOURLY_FILL_COMPLETED_BAR": "HOURLY_COMPLETED_BAR_PARSER_PLAN",
    "SESSION_CALENDAR": "SESSION_CALENDAR_PARSER_PLAN",
    "ROLL_CALENDAR": "ROLL_CALENDAR_PARSER_PLAN",
    "COST_PARAMETER": "COST_PARAMETER_PARSER_PLAN",
}

ROW_FAMILY_TO_SOURCE_UNIVERSE_FAMILY = {
    "DAILY_CONTINUOUS_COMPLETED_BAR": "DAILY_ROW_UNIVERSE",
    "DAILY_CURRENT_CONTRACT_COMPLETED_BAR": "DAILY_ROW_UNIVERSE",
    "HOURLY_DECISION_COMPLETED_BAR": "HOURLY_DECISION_FILL_ROW_UNIVERSE",
    "HOURLY_FILL_COMPLETED_BAR": "HOURLY_DECISION_FILL_ROW_UNIVERSE",
    "SESSION_CALENDAR": "SESSION_ROW_UNIVERSE",
    "ROLL_CALENDAR": "ROLL_ROW_UNIVERSE",
    "COST_PARAMETER": "COST_PARAMETER_ROW_UNIVERSE",
}

SOURCE_UNIVERSE_FAMILY_TO_ROW_LOCATOR_FAMILY = {
    "INSTRUMENT_UNIVERSE": "N/A",
    "RAW_SYMBOL_UNIVERSE": "N/A",
    "DAILY_ROW_UNIVERSE": "DAILY_CONTINUOUS_COMPLETED_BAR",
    "HOURLY_DECISION_FILL_ROW_UNIVERSE": "HOURLY_DECISION_COMPLETED_BAR",
    "SESSION_ROW_UNIVERSE": "SESSION_CALENDAR",
    "ROLL_ROW_UNIVERSE": "ROLL_CALENDAR",
    "COST_PARAMETER_ROW_UNIVERSE": "COST_PARAMETER",
}

REQUIRED_COLUMNS_BY_ROW_FAMILY = {
    "DAILY_CONTINUOUS_COMPLETED_BAR": (
        "completed_timestamp_utc",
        "trading_date",
        "raw_symbol",
        "row_locator",
        "close_price",
        "annual_percentage_sigma",
        "readiness_status",
    ),
    "DAILY_CURRENT_CONTRACT_COMPLETED_BAR": (
        "completed_timestamp_utc",
        "trading_date",
        "raw_symbol",
        "row_locator",
        "close_price",
        "annual_percentage_sigma",
        "readiness_status",
    ),
    "HOURLY_DECISION_COMPLETED_BAR": (
        "completed_timestamp_utc",
        "trading_date",
        "raw_symbol",
        "session_id",
        "row_locator",
        "close_price",
        "readiness_status",
    ),
    "HOURLY_FILL_COMPLETED_BAR": (
        "completed_timestamp_utc",
        "trading_date",
        "raw_symbol",
        "session_id",
        "row_locator",
        "close_price",
        "readiness_status",
    ),
    "SESSION_CALENDAR": (
        "trading_date",
        "session_id",
        "raw_symbol",
        "session_open_utc",
        "session_close_utc",
        "row_locator",
        "readiness_status",
    ),
    "ROLL_CALENDAR": (
        "trading_date",
        "expiring_raw_symbol",
        "incoming_raw_symbol",
        "roll_policy_hash",
        "row_locator",
        "readiness_status",
    ),
    "COST_PARAMETER": (
        "effective_trading_date",
        "raw_symbol",
        "commission_policy_hash",
        "spread_policy_hash",
        "contract_multiplier_value_hash",
        "currency_policy_hash",
        "row_locator",
        "readiness_status",
    ),
}


def canonical_sha256(payload: object) -> str:
    encoded = json.dumps(
        _canonical_payload(payload),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _canonical_payload(payload: object) -> object:
    if is_dataclass(payload):
        return _canonical_payload(asdict(payload))
    if isinstance(payload, datetime):
        normalized = payload.astimezone(timezone.utc).replace(tzinfo=timezone.utc)
        return normalized.isoformat().replace("+00:00", "Z")
    if isinstance(payload, Enum):
        return payload.value
    if isinstance(payload, dict):
        return {str(key): _canonical_payload(value) for key, value in payload.items()}
    if isinstance(payload, tuple):
        return [_canonical_payload(value) for value in payload]
    if isinstance(payload, list):
        return [_canonical_payload(value) for value in payload]
    if isinstance(payload, Path):
        return str(payload)
    return payload


@dataclass(frozen=True)
class ParsedDeclaredSourceFile:
    declaration: RawSourceFileDeclaration
    resolved_path: str
    file_sha256: str
    row_family: str
    rows: tuple[
        LocalDailySourceRow
        | LocalHourlySourceRow
        | LocalSessionSourceRow
        | LocalRollSourceRow
        | LocalCostParameterRow,
        ...,
    ]
    row_hashes: tuple[str, ...]
    parsed_output_batch_hash: str

    def validate(self) -> None:
        self.declaration.validate()
        if self.row_family != self.declaration.local_file.expected_row_family:
            raise CarverBlocked("S27 v2 parsed source file row family must match declaration")
        if self.file_sha256 != self.declaration.local_file.expected_sha256:
            raise CarverBlocked("S27 v2 parsed source file SHA256 must match declaration")
        if not self.rows:
            raise CarverBlocked("S27 v2 parsed source file must contain at least one row")
        if self.row_hashes != tuple(row.row_hash for row in self.rows):
            raise CarverBlocked("S27 v2 parsed source row hashes must match rows")
        if len(set(self.row_hashes)) != len(self.row_hashes):
            raise CarverBlocked("S27 v2 parsed source row hashes must be unique")
        for row in self.rows:
            row.validate()
        expected_hash = canonical_sha256(
            {
                "artifact": "S27_V2_PARSED_DECLARED_SOURCE_FILE",
                "file_sha256": self.file_sha256,
                "resolved_path": self.resolved_path,
                "row_family": self.row_family,
                "row_hashes": self.row_hashes,
            }
        )
        if self.parsed_output_batch_hash != expected_hash:
            raise CarverBlocked("S27 v2 parsed output batch hash must be content-bound")


@dataclass(frozen=True)
class LocalParserFileReplaySlice1Inputs:
    input_directory: ReplayInputDirectoryDeclaration
    parser_plan_bundle: ParserPlanBundle
    row_locator_contract: SourceRowLocatorContractBundle
    source_universe_contract: SourceUniverseContractBundle
    canonical_serialization_policy: CanonicalSerializationPolicy

    def validate(self) -> None:
        self.input_directory.validate()
        self.parser_plan_bundle.validate()
        self.row_locator_contract.validate()
        self.source_universe_contract.validate()
        self.canonical_serialization_policy.validate()
        _require_parser_plan_bundle_content_bound(self.parser_plan_bundle)
        if self.row_locator_contract.row_locator_contract_bundle_hash != self.input_directory.row_locator_hash:
            raise CarverBlocked("S27 v2 local replay inputs must bind declared row locator")
        if (
            self.source_universe_contract.source_universe_contract_bundle_hash
            != self.input_directory.source_universe_manifest_hash
        ):
            raise CarverBlocked("S27 v2 local replay inputs must bind declared source universe")
        if (
            self.row_locator_contract.input_directory_declaration_hash
            != self.input_directory.input_directory_declaration_hash
        ):
            raise CarverBlocked("S27 v2 local replay inputs must bind row locator to input directory")
        if (
            self.row_locator_contract.source_universe_manifest_hash
            != self.input_directory.source_universe_manifest_hash
        ):
            raise CarverBlocked("S27 v2 local replay inputs must bind row locator to source universe")
        if self.row_locator_contract.raw_file_hash_set_hash != self.input_directory.raw_file_hash_set_hash:
            raise CarverBlocked("S27 v2 local replay inputs must bind row locator to raw file hash set")
        if self.source_universe_contract.raw_file_hash_set_hash != self.input_directory.raw_file_hash_set_hash:
            raise CarverBlocked("S27 v2 local replay inputs must bind source universe to raw file hash set")
        if (
            self.source_universe_contract.row_locator_contract_bundle_hash
            != self.row_locator_contract.row_locator_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 local replay inputs must bind source universe to row locator")
        for declaration in self.input_directory.raw_source_files:
            if (
                declaration.local_file.canonical_serialization_policy_hash
                != self.canonical_serialization_policy.canonical_serialization_policy_hash
            ):
                raise CarverBlocked("S27 v2 local replay declarations must bind canonical policy")
        _require_row_locator_contract_content_bound(self)
        _require_source_universe_contract_content_bound(self)


@dataclass(frozen=True)
class LocalParserFileReplaySlice1Artifacts:
    parsed_files: tuple[ParsedDeclaredSourceFile, ...]
    raw_file_hash_contract: RawSourceFileHashSetContract
    parser_output_contract: ParserOutputBatchSetContract
    source_row_batch_contract: SourceRowBatchSetContract

    def validate(self) -> None:
        if tuple(parsed.row_family for parsed in self.parsed_files) != REQUIRED_ROW_LOCATOR_FAMILIES:
            raise CarverBlocked("S27 v2 local replay parsed files must match locked row-family tuple")
        for parsed in self.parsed_files:
            parsed.validate()
        self.raw_file_hash_contract.validate()
        self.parser_output_contract.validate()
        self.source_row_batch_contract.validate_against_parser_output_authority(self.parser_output_contract)


@dataclass(frozen=True)
class LocalParserFileReplaySlice2Artifacts:
    slice1_artifacts: LocalParserFileReplaySlice1Artifacts
    source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle
    source_input_selection_contract: SourceInputSelectionContractBundle
    source_input_manifest_contract: SourceInputManifestContractBundle

    def validate(self) -> None:
        self.slice1_artifacts.validate()
        self.source_row_selection_external_authority.validate()
        _validate_source_row_selection_authority_matches_rows(
            self.source_input_selection_contract.source_row_selection_authority,
            self.slice1_artifacts,
        )
        self.source_input_selection_contract.validate_against_external_authority(
            self.source_row_selection_external_authority,
            self.slice1_artifacts.source_row_batch_contract,
            self.slice1_artifacts.parser_output_contract,
        )
        _validate_source_input_selection_contract_content_bound(self.source_input_selection_contract)
        _validate_source_row_selection_external_authority_content_bound(
            self.source_row_selection_external_authority,
            self.source_input_selection_contract.source_row_selection_authority,
        )
        _validate_source_input_manifest_contract_local_only(
            self.source_input_manifest_contract,
            self.source_row_selection_external_authority,
            self.slice1_artifacts.source_row_batch_contract,
            self.slice1_artifacts.parser_output_contract,
        )


@dataclass(frozen=True)
class LocalParserFileReplaySlice3Artifacts:
    slice2_artifacts: LocalParserFileReplaySlice2Artifacts
    level_compatibility_input_contract: LevelCompatibilityInputContractBundle
    level_compatibility_contract: LevelCompatibilityContractBundle
    runtime_history_input_contract: RuntimeHistoryInputContractBundle
    runtime_history_contract: RuntimeHistoryContractBundle

    def validate(self) -> None:
        self.slice2_artifacts.validate()
        _validate_level_compatibility_input_contract_local_only(
            self.level_compatibility_input_contract,
            self.slice2_artifacts.source_input_manifest_contract,
        )
        _validate_level_compatibility_contract_content_bound(
            self.level_compatibility_contract,
            self.level_compatibility_input_contract,
            self.slice2_artifacts.slice1_artifacts.source_row_batch_contract,
        )
        _validate_runtime_history_input_contract_local_only(
            self.runtime_history_input_contract,
            self.slice2_artifacts.source_input_manifest_contract,
            self.level_compatibility_input_contract,
            self.level_compatibility_contract,
        )
        _validate_runtime_history_contract_content_bound(
            self.runtime_history_contract,
            self.runtime_history_input_contract,
            self.level_compatibility_contract,
            self.slice2_artifacts.slice1_artifacts.source_row_batch_contract,
        )


@dataclass(frozen=True)
class LocalParserFileReplaySlice4Artifacts:
    slice3_artifacts: LocalParserFileReplaySlice3Artifacts
    forecast_input_contract: ForecastInputContractBundle
    forecast_contract: ForecastContractBundle
    position_input_contract: PositionInputContractBundle
    position_contract: PositionContractBundle
    order_input_contract: OrderInputContractBundle
    order_contract: OrderContractBundle

    def validate(self) -> None:
        self.slice3_artifacts.validate()
        _validate_forecast_input_contract_local_only(
            self.forecast_input_contract,
            self.slice3_artifacts,
        )
        _validate_forecast_contract_content_bound(
            self.forecast_contract,
            self.forecast_input_contract,
            self.slice3_artifacts,
        )
        _validate_position_input_contract_local_only(
            self.position_input_contract,
            self.forecast_input_contract,
            self.forecast_contract,
        )
        _validate_position_contract_content_bound(
            self.position_contract,
            self.position_input_contract,
            self.forecast_contract,
        )
        _validate_order_input_contract_local_only(
            self.order_input_contract,
            self.position_input_contract,
            self.position_contract,
        )
        _validate_order_contract_content_bound(
            self.order_contract,
            self.order_input_contract,
            self.position_contract,
        )


@dataclass(frozen=True)
class LocalParserFileReplaySlice5Artifacts:
    slice4_artifacts: LocalParserFileReplaySlice4Artifacts
    fill_input_contract: FillInputContractBundle
    fill_contract: FillContractBundle

    def validate(self) -> None:
        self.slice4_artifacts.validate()
        _validate_fill_input_contract_local_only(
            self.fill_input_contract,
            self.slice4_artifacts,
        )
        _validate_fill_contract_content_bound(
            self.fill_contract,
            self.fill_input_contract,
            self.slice4_artifacts,
        )


@dataclass(frozen=True)
class LocalParserFileReplaySlice6Artifacts:
    slice5_artifacts: LocalParserFileReplaySlice5Artifacts
    replay_trust_root: ReplayTrustRoot
    evidence_manifest: EvidenceManifest
    cost_input_contract: CostInputContractBundle
    cost_contract: CostContractBundle

    def validate(self) -> None:
        self.slice5_artifacts.validate()
        self.replay_trust_root.validate()
        self.evidence_manifest.validate()
        _validate_cost_input_contract_local_only(
            self.cost_input_contract,
            self.slice5_artifacts,
            self.replay_trust_root,
            self.evidence_manifest,
        )
        _validate_cost_contract_content_bound(
            self.cost_contract,
            self.cost_input_contract,
            self.slice5_artifacts,
            self.replay_trust_root,
            self.evidence_manifest,
        )


@dataclass(frozen=True)
class LocalParserFileReplaySlice7Artifacts:
    slice6_artifacts: LocalParserFileReplaySlice6Artifacts
    pnl_input_contract: PnlInputContractBundle
    pnl_contract: PnlContractBundle

    def validate(self) -> None:
        self.slice6_artifacts.validate()
        _validate_pnl_input_contract_local_only(
            self.pnl_input_contract,
            self.slice6_artifacts,
        )
        _validate_pnl_contract_content_bound(
            self.pnl_contract,
            self.pnl_input_contract,
            self.slice6_artifacts,
        )


@dataclass(frozen=True)
class LocalParserFileReplayCompletionArtifacts:
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts
    construction_contract: ParserFileReplayConstructionContract
    validation_input_contract: ValidationInputContractBundle
    validation_contract: ValidationContractBundle
    trusted_bundle_contract: TrustedBundleContractBundle

    def validate(self) -> None:
        self.slice7_artifacts.validate()
        _validate_construction_contract_local_only(
            self.construction_contract,
            self.slice7_artifacts,
        )
        _validate_validation_input_contract_local_only(
            self.validation_input_contract,
            self.slice7_artifacts,
            self.validation_contract,
        )
        _validate_validation_contract_content_bound(
            self.validation_contract,
            self.validation_input_contract,
            self.slice7_artifacts,
        )
        _validate_trusted_bundle_contract_content_bound(
            self.trusted_bundle_contract,
            self.construction_contract,
            self.validation_input_contract,
            self.validation_contract,
            self.slice7_artifacts,
        )


def read_declared_local_file(
    input_directory: ReplayInputDirectoryDeclaration,
    raw_declaration: RawSourceFileDeclaration,
) -> bytes:
    input_directory.validate()
    _require_declared_raw_source(input_directory, raw_declaration)
    resolved_path = _resolve_declared_path(input_directory.declared_path, raw_declaration.local_file.declared_path)
    return resolved_path.read_bytes()


def parse_declared_source_file(
    input_directory: ReplayInputDirectoryDeclaration,
    raw_declaration: RawSourceFileDeclaration,
) -> ParsedDeclaredSourceFile:
    raw_declaration.validate()
    file_bytes = read_declared_local_file(input_directory, raw_declaration)
    file_sha256 = sha256(file_bytes).hexdigest()
    if file_sha256 != raw_declaration.local_file.expected_sha256:
        raise CarverBlocked("S27 v2 declared local file SHA256 mismatch")
    row_family = raw_declaration.local_file.expected_row_family
    rows = tuple(_parse_csv_rows(file_bytes.decode("utf-8-sig"), row_family))
    parsed = ParsedDeclaredSourceFile(
        declaration=raw_declaration,
        resolved_path=str(_resolve_declared_path(input_directory.declared_path, raw_declaration.local_file.declared_path)),
        file_sha256=file_sha256,
        row_family=row_family,
        rows=rows,
        row_hashes=tuple(row.row_hash for row in rows),
        parsed_output_batch_hash=canonical_sha256(
            {
                "artifact": "S27_V2_PARSED_DECLARED_SOURCE_FILE",
                "file_sha256": file_sha256,
                "resolved_path": str(
                    _resolve_declared_path(input_directory.declared_path, raw_declaration.local_file.declared_path)
                ),
                "row_family": row_family,
                "row_hashes": tuple(row.row_hash for row in rows),
            }
        ),
    )
    parsed.validate()
    return parsed


def build_local_parser_file_replay_slice1(
    inputs: LocalParserFileReplaySlice1Inputs,
) -> LocalParserFileReplaySlice1Artifacts:
    inputs.validate()
    parsed_files = tuple(
        parse_declared_source_file(inputs.input_directory, declaration)
        for declaration in inputs.input_directory.raw_source_files
    )
    raw_file_hash_contract = build_raw_file_hash_set_contract(
        inputs.input_directory,
        inputs.parser_plan_bundle,
        parsed_files,
    )
    parser_output_contract = build_parser_output_contract(
        inputs,
        raw_file_hash_contract,
        parsed_files,
    )
    source_row_batch_contract = build_source_row_batch_contract(
        inputs,
        parser_output_contract,
        parsed_files,
    )
    artifacts = LocalParserFileReplaySlice1Artifacts(
        parsed_files=parsed_files,
        raw_file_hash_contract=raw_file_hash_contract,
        parser_output_contract=parser_output_contract,
        source_row_batch_contract=source_row_batch_contract,
    )
    artifacts.validate()
    return artifacts


def build_local_parser_file_replay_slice2(
    inputs: LocalParserFileReplaySlice1Inputs,
) -> LocalParserFileReplaySlice2Artifacts:
    slice1_artifacts = build_local_parser_file_replay_slice1(inputs)
    source_row_selection_authority = build_source_row_selection_authority_contract(
        inputs,
        slice1_artifacts,
    )
    source_row_selection_external_authority = build_source_row_selection_external_authority_handle(
        inputs,
        slice1_artifacts,
        source_row_selection_authority,
    )
    source_input_selection_contract = build_source_input_selection_contract(
        inputs,
        slice1_artifacts,
        source_row_selection_external_authority,
        source_row_selection_authority,
    )
    source_input_manifest_contract = build_source_input_manifest_contract(
        inputs,
        slice1_artifacts,
        source_row_selection_external_authority,
        source_input_selection_contract,
    )
    artifacts = LocalParserFileReplaySlice2Artifacts(
        slice1_artifacts=slice1_artifacts,
        source_row_selection_external_authority=source_row_selection_external_authority,
        source_input_selection_contract=source_input_selection_contract,
        source_input_manifest_contract=source_input_manifest_contract,
    )
    artifacts.validate()
    return artifacts


def build_local_parser_file_replay_slice3(
    inputs: LocalParserFileReplaySlice1Inputs,
) -> LocalParserFileReplaySlice3Artifacts:
    slice2_artifacts = build_local_parser_file_replay_slice2(inputs)
    level_compatibility_input_contract = build_level_compatibility_input_contract(slice2_artifacts)
    level_compatibility_contract = build_level_compatibility_contract(
        slice2_artifacts,
        level_compatibility_input_contract,
    )
    runtime_history_input_contract = build_runtime_history_input_contract(
        slice2_artifacts,
        level_compatibility_input_contract,
        level_compatibility_contract,
    )
    runtime_history_contract = build_runtime_history_contract(
        slice2_artifacts,
        runtime_history_input_contract,
        level_compatibility_contract,
    )
    artifacts = LocalParserFileReplaySlice3Artifacts(
        slice2_artifacts=slice2_artifacts,
        level_compatibility_input_contract=level_compatibility_input_contract,
        level_compatibility_contract=level_compatibility_contract,
        runtime_history_input_contract=runtime_history_input_contract,
        runtime_history_contract=runtime_history_contract,
    )
    artifacts.validate()
    return artifacts


def build_local_parser_file_replay_slice4(
    inputs: LocalParserFileReplaySlice1Inputs,
) -> LocalParserFileReplaySlice4Artifacts:
    slice3_artifacts = build_local_parser_file_replay_slice3(inputs)
    forecast_input_contract = build_forecast_input_contract(slice3_artifacts)
    forecast_contract = build_forecast_contract(slice3_artifacts, forecast_input_contract)
    position_input_contract = build_position_input_contract(
        slice3_artifacts,
        forecast_input_contract,
        forecast_contract,
    )
    position_contract = build_position_contract(
        forecast_input_contract,
        forecast_contract,
        position_input_contract,
    )
    order_input_contract = build_order_input_contract(
        slice3_artifacts,
        forecast_contract,
        position_input_contract,
        position_contract,
    )
    order_contract = build_order_contract(position_input_contract, position_contract, order_input_contract)
    artifacts = LocalParserFileReplaySlice4Artifacts(
        slice3_artifacts=slice3_artifacts,
        forecast_input_contract=forecast_input_contract,
        forecast_contract=forecast_contract,
        position_input_contract=position_input_contract,
        position_contract=position_contract,
        order_input_contract=order_input_contract,
        order_contract=order_contract,
    )
    artifacts.validate()
    return artifacts


def build_local_parser_file_replay_slice5(
    inputs: LocalParserFileReplaySlice1Inputs,
) -> LocalParserFileReplaySlice5Artifacts:
    slice4_artifacts = build_local_parser_file_replay_slice4(inputs)
    fill_input_contract = build_fill_input_contract(slice4_artifacts)
    fill_contract = build_fill_contract(slice4_artifacts, fill_input_contract)
    artifacts = LocalParserFileReplaySlice5Artifacts(
        slice4_artifacts=slice4_artifacts,
        fill_input_contract=fill_input_contract,
        fill_contract=fill_contract,
    )
    artifacts.validate()
    return artifacts


def build_local_parser_file_replay_slice6(
    inputs: LocalParserFileReplaySlice1Inputs,
) -> LocalParserFileReplaySlice6Artifacts:
    slice5_artifacts = build_local_parser_file_replay_slice5(inputs)
    replay_trust_root = build_local_only_replay_trust_root(inputs, slice5_artifacts)
    evidence_manifest = build_local_only_evidence_manifest(replay_trust_root)
    cost_input_contract = build_cost_input_contract(
        slice5_artifacts,
        replay_trust_root,
        evidence_manifest,
    )
    cost_contract = build_cost_contract(
        slice5_artifacts,
        cost_input_contract,
        replay_trust_root,
        evidence_manifest,
    )
    artifacts = LocalParserFileReplaySlice6Artifacts(
        slice5_artifacts=slice5_artifacts,
        replay_trust_root=replay_trust_root,
        evidence_manifest=evidence_manifest,
        cost_input_contract=cost_input_contract,
        cost_contract=cost_contract,
    )
    artifacts.validate()
    return artifacts


def build_local_parser_file_replay_slice7(
    inputs: LocalParserFileReplaySlice1Inputs,
) -> LocalParserFileReplaySlice7Artifacts:
    slice6_artifacts = build_local_parser_file_replay_slice6(inputs)
    pnl_input_contract = build_pnl_input_contract(slice6_artifacts)
    pnl_contract = build_pnl_contract(slice6_artifacts, pnl_input_contract)
    artifacts = LocalParserFileReplaySlice7Artifacts(
        slice6_artifacts=slice6_artifacts,
        pnl_input_contract=pnl_input_contract,
        pnl_contract=pnl_contract,
    )
    artifacts.validate()
    return artifacts


def build_local_parser_file_replay_completion(
    inputs: LocalParserFileReplaySlice1Inputs,
) -> LocalParserFileReplayCompletionArtifacts:
    slice7_artifacts = build_local_parser_file_replay_slice7(inputs)
    construction_contract = build_local_only_construction_contract(inputs, slice7_artifacts)
    validation_contract = build_validation_contract(
        slice7_artifacts,
    )
    validation_input_contract = build_validation_input_contract(
        slice7_artifacts,
        validation_contract,
    )
    trusted_bundle_contract = build_trusted_bundle_contract(
        slice7_artifacts,
        construction_contract,
        validation_input_contract,
        validation_contract,
    )
    artifacts = LocalParserFileReplayCompletionArtifacts(
        slice7_artifacts=slice7_artifacts,
        construction_contract=construction_contract,
        validation_input_contract=validation_input_contract,
        validation_contract=validation_contract,
        trusted_bundle_contract=trusted_bundle_contract,
    )
    artifacts.validate()
    return artifacts


def build_raw_file_hash_set_contract(
    input_directory: ReplayInputDirectoryDeclaration,
    parser_plan_bundle: ParserPlanBundle,
    parsed_files: tuple[ParsedDeclaredSourceFile, ...],
) -> RawSourceFileHashSetContract:
    input_directory.validate()
    parser_plan_bundle.validate()
    _require_parser_plan_bundle_content_bound(parser_plan_bundle)
    _require_parsed_family_tuple(parsed_files)
    _require_parsed_files_match_input_directory(input_directory, parsed_files)
    parser_plan_hash_by_family = _parser_plan_hash_by_row_family(parser_plan_bundle)
    bindings = tuple(
        _build_raw_source_file_hash_binding(parsed, parser_plan_hash_by_family[parsed.row_family])
        for parsed in parsed_files
    )
    raw_file_hash_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_RAW_FILE_HASH_SET",
            "binding_hashes": tuple(binding.file_hash_binding_hash for binding in bindings),
            "input_directory_declaration_hash": input_directory.input_directory_declaration_hash,
            "parser_plan_bundle_hash": parser_plan_bundle.parser_plan_bundle_hash,
        }
    )
    if raw_file_hash_set_hash != input_directory.raw_file_hash_set_hash:
        raise CarverBlocked("S27 v2 computed raw file hash set must match declared authority")
    contract = RawSourceFileHashSetContract(
        status=S27_V2_RAW_FILE_HASH_CONTRACT_ONLY_STATUS,
        input_directory_declaration_hash=input_directory.input_directory_declaration_hash,
        source_universe_manifest_hash=input_directory.source_universe_manifest_hash,
        parser_plan_bundle_hash=parser_plan_bundle.parser_plan_bundle_hash,
        raw_file_hash_bindings=bindings,
        raw_file_hash_set_hash=raw_file_hash_set_hash,
        no_download_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_NO_DOWNLOAD_POLICY",
                "assertion": "NO_PROVIDER_API_NO_DOWNLOAD",
                "input_directory_declaration_hash": input_directory.input_directory_declaration_hash,
            }
        ),
        raw_file_hash_contract_hash=canonical_sha256(
            {
                "artifact": "S27_V2_RAW_FILE_HASH_CONTRACT",
                "raw_file_hash_set_hash": raw_file_hash_set_hash,
                "source_universe_manifest_hash": input_directory.source_universe_manifest_hash,
            }
        ),
    )
    contract.validate()
    return contract


def build_parser_output_contract(
    inputs: LocalParserFileReplaySlice1Inputs,
    raw_file_hash_contract: RawSourceFileHashSetContract,
    parsed_files: tuple[ParsedDeclaredSourceFile, ...],
) -> ParserOutputBatchSetContract:
    inputs.validate()
    raw_file_hash_contract.validate()
    _require_parsed_family_tuple(parsed_files)
    _require_parsed_files_match_declared_local_files(inputs, parsed_files)
    _require_raw_file_hash_contract_matches_inputs(raw_file_hash_contract, inputs, parsed_files)
    raw_binding_by_family = {
        binding.file_family: binding
        for binding in raw_file_hash_contract.raw_file_hash_bindings
    }
    locator_contract_by_family = {
        contract.row_family: contract
        for contract in inputs.row_locator_contract.row_family_contracts
    }
    family_contracts = tuple(
        _build_parser_output_family_contract(
            parsed,
            raw_binding_by_family[parsed.row_family],
            locator_contract_by_family[parsed.row_family].family_contract_hash,
            inputs.canonical_serialization_policy,
        )
        for parsed in parsed_files
    )
    parsed_output_batch_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_PARSED_OUTPUT_BATCH_SET",
            "family_contract_hashes": tuple(
                contract.parser_output_family_contract_hash
                for contract in family_contracts
            ),
        }
    )
    contract = ParserOutputBatchSetContract(
        status=S27_V2_PARSER_OUTPUT_CONTRACT_ONLY_STATUS,
        raw_file_hash_contract_hash=raw_file_hash_contract.raw_file_hash_contract_hash,
        raw_file_hash_set_hash=raw_file_hash_contract.raw_file_hash_set_hash,
        parser_plan_bundle_hash=inputs.parser_plan_bundle.parser_plan_bundle_hash,
        row_locator_contract_bundle_hash=inputs.row_locator_contract.row_locator_contract_bundle_hash,
        canonical_serialization_policy_hash=(
            inputs.canonical_serialization_policy.canonical_serialization_policy_hash
        ),
        parsed_output_family_contracts=family_contracts,
        parsed_output_batch_set_hash=parsed_output_batch_set_hash,
        parser_output_contract_hash=canonical_sha256(
            {
                "artifact": "S27_V2_PARSER_OUTPUT_CONTRACT",
                "parsed_output_batch_set_hash": parsed_output_batch_set_hash,
                "raw_file_hash_contract_hash": raw_file_hash_contract.raw_file_hash_contract_hash,
            }
        ),
    )
    contract.validate()
    return contract


def build_source_row_batch_contract(
    inputs: LocalParserFileReplaySlice1Inputs,
    parser_output_contract: ParserOutputBatchSetContract,
    parsed_files: tuple[ParsedDeclaredSourceFile, ...],
) -> SourceRowBatchSetContract:
    inputs.validate()
    parser_output_contract.validate()
    _require_parsed_family_tuple(parsed_files)
    _require_parsed_files_match_declared_local_files(inputs, parsed_files)
    _require_parser_output_contract_matches_inputs(parser_output_contract, inputs, parsed_files)
    parser_output_by_family = {
        contract.row_family: contract
        for contract in parser_output_contract.parsed_output_family_contracts
    }
    universe_family_contract_hash = {
        contract.universe_family: contract.family_contract_hash
        for contract in inputs.source_universe_contract.family_contracts
    }
    locator_contract_by_family = {
        contract.row_family: contract
        for contract in inputs.row_locator_contract.row_family_contracts
    }
    family_contracts = tuple(
        _build_source_row_batch_family_contract(
            parsed,
            parser_output_by_family[parsed.row_family],
            universe_family_contract_hash[ROW_FAMILY_TO_SOURCE_UNIVERSE_FAMILY[parsed.row_family]],
            locator_contract_by_family[parsed.row_family].family_contract_hash,
        )
        for parsed in parsed_files
    )
    source_row_batch_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_ROW_BATCH_SET",
            "family_contract_hashes": tuple(
                contract.source_row_batch_family_contract_hash
                for contract in family_contracts
            ),
        }
    )
    contract = SourceRowBatchSetContract(
        status=S27_V2_SOURCE_ROW_BATCH_CONTRACT_ONLY_STATUS,
        parser_output_contract_hash=parser_output_contract.parser_output_contract_hash,
        parsed_output_batch_set_hash=parser_output_contract.parsed_output_batch_set_hash,
        source_universe_contract_bundle_hash=(
            inputs.source_universe_contract.source_universe_contract_bundle_hash
        ),
        row_locator_contract_bundle_hash=inputs.row_locator_contract.row_locator_contract_bundle_hash,
        canonical_serialization_policy_hash=(
            inputs.canonical_serialization_policy.canonical_serialization_policy_hash
        ),
        source_row_batch_family_contracts=family_contracts,
        source_row_batch_set_hash=source_row_batch_set_hash,
        source_row_batch_contract_hash=canonical_sha256(
            {
                "artifact": "S27_V2_SOURCE_ROW_BATCH_CONTRACT",
                "parser_output_contract_hash": parser_output_contract.parser_output_contract_hash,
                "source_row_batch_set_hash": source_row_batch_set_hash,
            }
        ),
    )
    contract.validate_against_parser_output_authority(parser_output_contract)
    return contract


def build_source_row_selection_authority_contract(
    inputs: LocalParserFileReplaySlice1Inputs,
    slice1_artifacts: LocalParserFileReplaySlice1Artifacts,
) -> SourceRowSelectionAuthorityContract:
    _require_slice1_artifacts_match_inputs(inputs, slice1_artifacts)
    family_contract_by_family = _source_row_batch_family_contract_by_family(slice1_artifacts.source_row_batch_contract)
    parsed_by_family = _parsed_file_by_family(slice1_artifacts.parsed_files)
    selected_row_hash_by_role: dict[str, str] = {}
    selected_row_locator_hash_by_role: dict[str, str] = {}
    selected_row_membership_proof_hash_by_role: dict[str, str] = {}
    selected_row_locator_membership_proof_hash_by_role: dict[str, str] = {}
    for role in REQUIRED_SOURCE_INPUT_ROLES:
        family = REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[role]
        family_contract = family_contract_by_family[family]
        row = parsed_by_family[family].rows[0]
        selected_row_hash_by_role[role] = row.row_hash
        selected_row_locator_hash_by_role[role] = _selected_row_locator_hash(role, family, row)
        selected_row_membership_proof_hash_by_role[role] = canonical_sha256(
            {
                "artifact": "S27_V2_SELECTED_ROW_MEMBERSHIP_PROOF",
                "input_role": role,
                "row_family": family,
                "selected_row_hash": row.row_hash,
                "source_row_batch_family_contract_hash": family_contract.source_row_batch_family_contract_hash,
                "source_row_batch_hash": family_contract.source_row_batch_hash,
            }
        )
        selected_row_locator_membership_proof_hash_by_role[role] = canonical_sha256(
            {
                "artifact": "S27_V2_SELECTED_ROW_LOCATOR_MEMBERSHIP_PROOF",
                "input_role": role,
                "row_family": family,
                "selected_row_locator_hash": selected_row_locator_hash_by_role[role],
                "row_locator_family_contract_hash": family_contract.row_locator_family_contract_hash,
                "row_locator_policy_hash": family_contract.row_locator_policy_hash,
            }
        )
    selected_row_membership_proof_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_ROW_SELECTION_SELECTED_ROW_MEMBERSHIP_PROOF_SET",
            "authority_status": PLANNED_SOURCE_ROW_SELECTION_AUTHORITY_STATUS,
            "proof_hash_by_input_role": _ordered_hash_map_payload(
                selected_row_membership_proof_hash_by_role,
                REQUIRED_SOURCE_INPUT_ROLES,
            ),
            "source_row_batch_contract_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
            "source_row_batch_set_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_set_hash,
            "source_universe_contract_bundle_hash": inputs.source_universe_contract.source_universe_contract_bundle_hash,
        }
    )
    selected_row_locator_membership_proof_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_ROW_SELECTION_SELECTED_ROW_LOCATOR_MEMBERSHIP_PROOF_SET",
            "authority_status": PLANNED_SOURCE_ROW_SELECTION_AUTHORITY_STATUS,
            "proof_hash_by_input_role": _ordered_hash_map_payload(
                selected_row_locator_membership_proof_hash_by_role,
                REQUIRED_SOURCE_INPUT_ROLES,
            ),
            "row_locator_contract_bundle_hash": inputs.row_locator_contract.row_locator_contract_bundle_hash,
            "source_row_batch_contract_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
            "source_row_batch_set_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_set_hash,
            "source_universe_contract_bundle_hash": inputs.source_universe_contract.source_universe_contract_bundle_hash,
        }
    )
    policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_ROW_SELECTION_AUTHORITY_POLICY",
            "selection_rule": "FIRST_COMPLETED_LOCAL_ROW_PER_LOCKED_INPUT_ROLE_FOR_CONSTRUCTION_SCAFFOLD_ONLY",
            "input_roles": REQUIRED_SOURCE_INPUT_ROLES,
        }
    )
    authority_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_ROW_SELECTION_AUTHORITY",
            "authority_status": PLANNED_SOURCE_ROW_SELECTION_AUTHORITY_STATUS,
            "row_locator_contract_bundle_hash": inputs.row_locator_contract.row_locator_contract_bundle_hash,
            "selected_row_hash_by_input_role": _ordered_hash_map_payload(
                selected_row_hash_by_role,
                REQUIRED_SOURCE_INPUT_ROLES,
            ),
            "selected_row_locator_hash_by_input_role": _ordered_hash_map_payload(
                selected_row_locator_hash_by_role,
                REQUIRED_SOURCE_INPUT_ROLES,
            ),
            "selected_row_locator_membership_proof_hash_by_input_role": _ordered_hash_map_payload(
                selected_row_locator_membership_proof_hash_by_role,
                REQUIRED_SOURCE_INPUT_ROLES,
            ),
            "selected_row_locator_membership_proof_set_hash": selected_row_locator_membership_proof_set_hash,
            "selected_row_membership_proof_hash_by_input_role": _ordered_hash_map_payload(
                selected_row_membership_proof_hash_by_role,
                REQUIRED_SOURCE_INPUT_ROLES,
            ),
            "selected_row_membership_proof_set_hash": selected_row_membership_proof_set_hash,
            "source_row_batch_contract_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
            "source_row_batch_set_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_set_hash,
            "source_row_selection_authority_policy_hash": policy_hash,
            "source_universe_contract_bundle_hash": inputs.source_universe_contract.source_universe_contract_bundle_hash,
        }
    )
    contract = SourceRowSelectionAuthorityContract(
        authority_status=PLANNED_SOURCE_ROW_SELECTION_AUTHORITY_STATUS,
        source_row_batch_contract_hash=slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
        source_row_batch_set_hash=slice1_artifacts.source_row_batch_contract.source_row_batch_set_hash,
        source_universe_contract_bundle_hash=inputs.source_universe_contract.source_universe_contract_bundle_hash,
        row_locator_contract_bundle_hash=inputs.row_locator_contract.row_locator_contract_bundle_hash,
        selected_row_membership_proof_set_hash=selected_row_membership_proof_set_hash,
        selected_row_locator_membership_proof_set_hash=selected_row_locator_membership_proof_set_hash,
        selected_row_hash_by_input_role=selected_row_hash_by_role,
        selected_row_locator_hash_by_input_role=selected_row_locator_hash_by_role,
        selected_row_membership_proof_hash_by_input_role=selected_row_membership_proof_hash_by_role,
        selected_row_locator_membership_proof_hash_by_input_role=selected_row_locator_membership_proof_hash_by_role,
        source_row_selection_authority_policy_hash=policy_hash,
        source_row_selection_authority_hash=authority_hash,
    )
    contract.validate()
    _validate_source_row_selection_authority_matches_rows(contract, slice1_artifacts)
    return contract


def build_source_row_selection_external_authority_handle(
    inputs: LocalParserFileReplaySlice1Inputs,
    slice1_artifacts: LocalParserFileReplaySlice1Artifacts,
    source_row_selection_authority: SourceRowSelectionAuthorityContract,
) -> SourceRowSelectionExternalAuthorityHandle:
    _require_slice1_artifacts_match_inputs(inputs, slice1_artifacts)
    source_row_selection_authority.validate()
    replay_trust_root_hash = canonical_sha256(
        {
            "artifact": "S27_V2_LOCAL_ONLY_PLACEHOLDER_REPLAY_TRUST_ROOT_HASH",
            "status": "LOCAL_ONLY_SLICE2_NOT_ACTIVE_TRUST_AUTHORITY",
            "source_row_selection_authority_hash": source_row_selection_authority.source_row_selection_authority_hash,
        }
    )
    active_evidence_manifest_hash = canonical_sha256(
        {
            "artifact": "S27_V2_LOCAL_ONLY_PLACEHOLDER_ACTIVE_EVIDENCE_MANIFEST_HASH",
            "status": "LOCAL_ONLY_SLICE2_NOT_ACTIVE_EVIDENCE_AUTHORITY",
            "source_row_batch_contract_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
            "source_row_selection_authority_hash": source_row_selection_authority.source_row_selection_authority_hash,
        }
    )
    policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_HANDLE_POLICY",
            "restriction": "LOCAL_ONLY_SLICE2_CONSTRUCTION_HANDLE_NOT_ACTIVE_TRUST_VALIDATION",
        }
    )
    handle_hash = canonical_sha256(
        {
            "active_evidence_manifest_hash": active_evidence_manifest_hash,
            "artifact": "S27_V2_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_HANDLE",
            "authority_handle_policy_hash": policy_hash,
            "authority_status": PLANNED_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_STATUS,
            "replay_trust_root_hash": replay_trust_root_hash,
            "row_locator_contract_bundle_hash": inputs.row_locator_contract.row_locator_contract_bundle_hash,
            "selected_row_locator_membership_proof_set_hash": (
                source_row_selection_authority.selected_row_locator_membership_proof_set_hash
            ),
            "selected_row_membership_proof_set_hash": (
                source_row_selection_authority.selected_row_membership_proof_set_hash
            ),
            "source_row_batch_contract_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
            "source_row_batch_set_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_set_hash,
            "source_row_selection_authority_hash": source_row_selection_authority.source_row_selection_authority_hash,
            "source_universe_contract_bundle_hash": inputs.source_universe_contract.source_universe_contract_bundle_hash,
        }
    )
    handle = SourceRowSelectionExternalAuthorityHandle(
        authority_status=PLANNED_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_STATUS,
        replay_trust_root_hash=replay_trust_root_hash,
        active_evidence_manifest_hash=active_evidence_manifest_hash,
        source_row_batch_contract_hash=slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
        source_row_batch_set_hash=slice1_artifacts.source_row_batch_contract.source_row_batch_set_hash,
        source_universe_contract_bundle_hash=inputs.source_universe_contract.source_universe_contract_bundle_hash,
        row_locator_contract_bundle_hash=inputs.row_locator_contract.row_locator_contract_bundle_hash,
        source_row_selection_authority_hash=source_row_selection_authority.source_row_selection_authority_hash,
        selected_row_membership_proof_set_hash=(
            source_row_selection_authority.selected_row_membership_proof_set_hash
        ),
        selected_row_locator_membership_proof_set_hash=(
            source_row_selection_authority.selected_row_locator_membership_proof_set_hash
        ),
        authority_handle_policy_hash=policy_hash,
        authority_handle_hash=handle_hash,
    )
    handle.validate()
    _validate_source_row_selection_external_authority_content_bound(handle, source_row_selection_authority)
    return handle


def build_source_input_selection_contract(
    inputs: LocalParserFileReplaySlice1Inputs,
    slice1_artifacts: LocalParserFileReplaySlice1Artifacts,
    source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
    source_row_selection_authority: SourceRowSelectionAuthorityContract,
) -> SourceInputSelectionContractBundle:
    _require_slice1_artifacts_match_inputs(inputs, slice1_artifacts)
    _validate_source_row_selection_external_authority_content_bound(
        source_row_selection_external_authority,
        source_row_selection_authority,
    )
    family_contract_by_family = _source_row_batch_family_contract_by_family(slice1_artifacts.source_row_batch_contract)
    role_contracts = tuple(
        _build_source_input_role_selection_contract(
            role,
            family_contract_by_family[REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[role]],
            source_row_selection_authority,
        )
        for role in REQUIRED_SOURCE_INPUT_ROLES
    )
    source_input_selection_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_SELECTION_SET",
            "role_contract_hashes": tuple(
                contract.source_input_role_contract_hash
                for contract in role_contracts
            ),
            "source_row_selection_authority_hash": source_row_selection_authority.source_row_selection_authority_hash,
        }
    )
    source_input_selection_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_SELECTION_CONTRACT",
            "source_input_selection_set_hash": source_input_selection_set_hash,
            "source_row_batch_contract_hash": slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
            "source_row_selection_authority_hash": source_row_selection_authority.source_row_selection_authority_hash,
        }
    )
    contract = SourceInputSelectionContractBundle(
        status=S27_V2_SOURCE_INPUT_SELECTION_CONTRACT_ONLY_STATUS,
        source_row_batch_contract_hash=slice1_artifacts.source_row_batch_contract.source_row_batch_contract_hash,
        source_row_batch_set_hash=slice1_artifacts.source_row_batch_contract.source_row_batch_set_hash,
        source_universe_contract_bundle_hash=inputs.source_universe_contract.source_universe_contract_bundle_hash,
        row_locator_contract_bundle_hash=inputs.row_locator_contract.row_locator_contract_bundle_hash,
        canonical_serialization_policy_hash=(
            inputs.canonical_serialization_policy.canonical_serialization_policy_hash
        ),
        source_row_selection_authority=source_row_selection_authority,
        source_row_selection_authority_hash=source_row_selection_authority.source_row_selection_authority_hash,
        role_selection_contracts=role_contracts,
        expected_source_row_batch_contract_hash_by_input_role={
            role: family_contract_by_family[
                REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[role]
            ].source_row_batch_family_contract_hash
            for role in REQUIRED_SOURCE_INPUT_ROLES
        },
        expected_source_row_batch_hash_by_input_role={
            role: family_contract_by_family[
                REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[role]
            ].source_row_batch_hash
            for role in REQUIRED_SOURCE_INPUT_ROLES
        },
        active_selected_row_hash_by_input_role=dict(
            source_row_selection_authority.selected_row_hash_by_input_role
        ),
        active_selected_row_locator_hash_by_input_role=dict(
            source_row_selection_authority.selected_row_locator_hash_by_input_role
        ),
        expected_selected_row_hash_by_input_role={
            contract.input_role: contract.selected_row_hash
            for contract in role_contracts
        },
        expected_selected_row_locator_hash_by_input_role={
            contract.input_role: contract.selected_row_locator_hash
            for contract in role_contracts
        },
        expected_selected_row_membership_proof_hash_by_input_role={
            contract.input_role: contract.selected_row_membership_proof_hash
            for contract in role_contracts
        },
        expected_selected_row_locator_membership_proof_hash_by_input_role={
            contract.input_role: contract.selected_row_locator_membership_proof_hash
            for contract in role_contracts
        },
        source_input_selection_set_hash=source_input_selection_set_hash,
        source_input_selection_contract_hash=source_input_selection_contract_hash,
    )
    contract.validate_against_external_authority(
        source_row_selection_external_authority,
        slice1_artifacts.source_row_batch_contract,
        slice1_artifacts.parser_output_contract,
    )
    _validate_source_input_selection_contract_content_bound(contract)
    return contract


def build_source_input_manifest_contract(
    inputs: LocalParserFileReplaySlice1Inputs,
    slice1_artifacts: LocalParserFileReplaySlice1Artifacts,
    source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
    source_input_selection_contract: SourceInputSelectionContractBundle,
) -> SourceInputManifestContractBundle:
    _require_slice1_artifacts_match_inputs(inputs, slice1_artifacts)
    source_input_selection_contract.validate_against_external_authority(
        source_row_selection_external_authority,
        slice1_artifacts.source_row_batch_contract,
        slice1_artifacts.parser_output_contract,
    )
    _validate_source_input_selection_contract_content_bound(source_input_selection_contract)
    role_contract_by_role = {
        contract.input_role: contract
        for contract in source_input_selection_contract.role_selection_contracts
    }
    field_contracts = tuple(
        _build_source_input_manifest_field_contract(
            field,
            role_contract_by_role[REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[field]],
        )
        for field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
    )
    schema_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST_SCHEMA",
            "manifest_fields": REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS,
            "role_by_manifest_field": tuple(
                (field, REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[field])
                for field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
            ),
        }
    )
    manifest_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST",
            "field_contract_hashes": tuple(
                contract.manifest_field_contract_hash
                for contract in field_contracts
            ),
            "source_input_selection_contract_hash": (
                source_input_selection_contract.source_input_selection_contract_hash
            ),
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST_CONTRACT",
            "source_input_manifest_hash": manifest_hash,
            "source_input_manifest_schema_hash": schema_hash,
            "source_input_selection_contract_hash": (
                source_input_selection_contract.source_input_selection_contract_hash
            ),
        }
    )
    contract = SourceInputManifestContractBundle(
        status=S27_V2_SOURCE_INPUT_MANIFEST_CONTRACT_ONLY_STATUS,
        source_input_selection_contract_hash=source_input_selection_contract.source_input_selection_contract_hash,
        source_input_selection_set_hash=source_input_selection_contract.source_input_selection_set_hash,
        source_universe_contract_bundle_hash=source_input_selection_contract.source_universe_contract_bundle_hash,
        row_locator_contract_bundle_hash=source_input_selection_contract.row_locator_contract_bundle_hash,
        canonical_serialization_policy_hash=(
            inputs.canonical_serialization_policy.canonical_serialization_policy_hash
        ),
        source_input_selection_contract_bundle=source_input_selection_contract,
        manifest_field_contracts=field_contracts,
        source_input_role_selection_contracts=source_input_selection_contract.role_selection_contracts,
        active_source_input_role_contract_hash_by_input_role={
            role: role_contract_by_role[role].source_input_role_contract_hash
            for role in REQUIRED_SOURCE_INPUT_ROLES
        },
        active_selected_row_hash_by_input_role={
            role: role_contract_by_role[role].selected_row_hash
            for role in REQUIRED_SOURCE_INPUT_ROLES
        },
        active_selected_row_locator_hash_by_input_role={
            role: role_contract_by_role[role].selected_row_locator_hash
            for role in REQUIRED_SOURCE_INPUT_ROLES
        },
        expected_source_input_role_contract_hash_by_manifest_field={
            field: role_contract_by_role[
                REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[field]
            ].source_input_role_contract_hash
            for field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
        },
        expected_selected_row_hash_by_manifest_field={
            field: role_contract_by_role[
                REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[field]
            ].selected_row_hash
            for field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
        },
        expected_selected_row_locator_hash_by_manifest_field={
            field: role_contract_by_role[
                REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[field]
            ].selected_row_locator_hash
            for field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
        },
        source_input_manifest_schema_hash=schema_hash,
        source_input_manifest_hash=manifest_hash,
        source_input_manifest_contract_hash=contract_hash,
    )
    _validate_source_input_manifest_contract_local_only(
        contract,
        source_row_selection_external_authority,
        slice1_artifacts.source_row_batch_contract,
        slice1_artifacts.parser_output_contract,
    )
    return contract


def build_level_compatibility_input_contract(
    slice2_artifacts: LocalParserFileReplaySlice2Artifacts,
) -> LevelCompatibilityInputContractBundle:
    slice2_artifacts.validate()
    manifest = slice2_artifacts.source_input_manifest_contract
    field_by_manifest_field = _source_input_manifest_field_contract_by_field(manifest)
    input_fields = tuple(
        _build_level_compatibility_input_field_contract(
            input_label,
            field_by_manifest_field[REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]],
        )
        for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
    )
    input_hash_by_label = {
        contract.input_label: contract.input_field_contract_hash
        for contract in input_fields
    }
    proof_bindings = tuple(
        _build_level_compatibility_proof_input_binding_contract(
            proof_label,
            input_hash_by_label,
        )
        for proof_label in REQUIRED_LEVEL_COMPATIBILITY_PROOFS
    )
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_SET",
            "input_field_contract_hashes": tuple(
                contract.input_field_contract_hash
                for contract in input_fields
            ),
            "proof_input_binding_contract_hashes": tuple(
                binding.proof_input_binding_contract_hash
                for binding in proof_bindings
            ),
            "source_input_manifest_contract_hash": manifest.source_input_manifest_contract_hash,
            "source_input_manifest_hash": manifest.source_input_manifest_hash,
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT",
            "level_compatibility_policy_hash": canonical_sha256(
                {
                    "artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_POLICY",
                    "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
                }
            ),
            "level_compatibility_input_set_hash": input_set_hash,
            "source_input_manifest_contract_hash": manifest.source_input_manifest_contract_hash,
            "source_input_manifest_hash": manifest.source_input_manifest_hash,
        }
    )
    contract = LevelCompatibilityInputContractBundle(
        status=S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_ONLY_STATUS,
        source_input_manifest_contract_hash=manifest.source_input_manifest_contract_hash,
        source_input_manifest_hash=manifest.source_input_manifest_hash,
        source_input_selection_contract_hash=manifest.source_input_selection_contract_hash,
        level_compatibility_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_POLICY",
                "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
            }
        ),
        source_input_manifest_contract_bundle=manifest,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label={
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ].manifest_field_contract_hash
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        },
        expected_selected_row_hash_by_input_label={
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ].selected_row_hash
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        },
        expected_selected_row_locator_hash_by_input_label={
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ].selected_row_locator_hash
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        },
        proof_input_binding_contracts=proof_bindings,
        level_compatibility_input_set_hash=input_set_hash,
        level_compatibility_input_contract_hash=contract_hash,
    )
    _validate_level_compatibility_input_contract_local_only(contract, manifest)
    return contract


def build_level_compatibility_contract(
    slice2_artifacts: LocalParserFileReplaySlice2Artifacts,
    level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
) -> LevelCompatibilityContractBundle:
    slice2_artifacts.validate()
    _validate_level_compatibility_input_contract_local_only(
        level_compatibility_input_contract,
        slice2_artifacts.source_input_manifest_contract,
    )
    source_row_batch = slice2_artifacts.slice1_artifacts.source_row_batch_contract
    family_hash_by_family = _source_row_batch_family_contract_hash_by_family(source_row_batch)
    policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_DAILY_HOURLY_LEVEL_COMPATIBILITY_POLICY",
            "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
        }
    )
    source_binding = LevelCompatibilitySourceBinding(
        daily_continuous_row_family_hash=family_hash_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"],
        daily_current_contract_row_family_hash=family_hash_by_family[
            "DAILY_CURRENT_CONTRACT_COMPLETED_BAR"
        ],
        previous_completed_current_contract_close_family_hash=family_hash_by_family[
            "DAILY_CURRENT_CONTRACT_COMPLETED_BAR"
        ],
        hourly_decision_row_family_hash=family_hash_by_family["HOURLY_DECISION_COMPLETED_BAR"],
        hourly_fill_row_family_hash=family_hash_by_family["HOURLY_FILL_COMPLETED_BAR"],
        source_universe_contract_hash=source_row_batch.source_universe_contract_bundle_hash,
        row_locator_contract_hash=source_row_batch.row_locator_contract_bundle_hash,
        binding_hash="0" * 64,
    )
    source_binding = LevelCompatibilitySourceBinding(
        **{
            **asdict(source_binding),
            "binding_hash": canonical_sha256(_level_compatibility_source_binding_hash_payload(source_binding)),
        }
    )
    input_hash_by_label = _level_compatibility_input_field_contract_hash_by_label(
        level_compatibility_input_contract,
    )
    proof_contracts = tuple(
        _build_level_compatibility_proof_contract(proof_label, input_hash_by_label)
        for proof_label in REQUIRED_LEVEL_COMPATIBILITY_PROOFS
    )
    verdict = LevelCompatibilityVerdictContract(
        compatibility_verdict="PASS",
        compatibility_reason_code="BRIDGED_CONTINUOUS_COMPATIBLE",
        required_proof_contract_hashes=tuple(
            proof.proof_contract_hash
            for proof in proof_contracts
        ),
        continuous_adjustment_bridge_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_CONTINUOUS_ADJUSTMENT_BRIDGE_POLICY",
                "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
            }
        ),
        sigma_bridge_level_source_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_SIGMA_BRIDGE_LEVEL_SOURCE_POLICY",
                "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
            }
        ),
        verdict_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_LEVEL_COMPATIBILITY_VERDICT_POLICY",
                "scope": "LOCAL_ONLY_PLANNED_PASS_SHAPE",
            }
        ),
        planned_ledger_schema_hash=canonical_sha256(
            {
                "artifact": "S27_V2_LEVEL_COMPATIBILITY_LEDGER_SCHEMA",
                "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
            }
        ),
        verdict_contract_hash="0" * 64,
    )
    verdict = LevelCompatibilityVerdictContract(
        **{
            **asdict(verdict),
            "verdict_contract_hash": canonical_sha256(_level_compatibility_verdict_hash_payload(verdict)),
        }
    )
    contract = LevelCompatibilityContractBundle(
        status=S27_V2_LEVEL_COMPATIBILITY_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        proof_contracts=proof_contracts,
        verdict_contract=verdict,
        daily_hourly_level_compatibility_policy_hash=policy_hash,
        level_compatibility_contract_bundle_hash="0" * 64,
    )
    contract = LevelCompatibilityContractBundle(
        **{
            **asdict(contract),
            "source_binding": source_binding,
            "proof_contracts": proof_contracts,
            "verdict_contract": verdict,
            "level_compatibility_contract_bundle_hash": canonical_sha256(
                _level_compatibility_contract_bundle_hash_payload(contract)
            ),
        }
    )
    _validate_level_compatibility_contract_content_bound(
        contract,
        level_compatibility_input_contract,
        source_row_batch,
    )
    return contract


def build_runtime_history_input_contract(
    slice2_artifacts: LocalParserFileReplaySlice2Artifacts,
    level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
    level_compatibility_contract: LevelCompatibilityContractBundle,
) -> RuntimeHistoryInputContractBundle:
    slice2_artifacts.validate()
    manifest = slice2_artifacts.source_input_manifest_contract
    _validate_level_compatibility_input_contract_local_only(level_compatibility_input_contract, manifest)
    _validate_level_compatibility_contract_content_bound(
        level_compatibility_contract,
        level_compatibility_input_contract,
        slice2_artifacts.slice1_artifacts.source_row_batch_contract,
    )
    field_by_manifest_field = _source_input_manifest_field_contract_by_field(manifest)
    input_fields = tuple(
        _build_runtime_history_input_field_contract(
            input_label,
            field_by_manifest_field[REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]],
        )
        for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
    )
    runtime_input_hash_by_label = {
        contract.input_label: contract.input_field_contract_hash
        for contract in input_fields
    }
    level_input_hash_by_label = _level_compatibility_input_field_contract_hash_by_label(
        level_compatibility_input_contract,
    )
    level_bindings = tuple(
        _build_runtime_history_level_compatibility_binding_contract(
            runtime_input_label,
            runtime_input_hash_by_label,
            level_input_hash_by_label,
        )
        for runtime_input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUT_BY_RUNTIME_HISTORY_INPUT
    )
    state_bindings = tuple(
        _build_runtime_history_state_input_binding_contract(
            state_family,
            runtime_input_hash_by_label,
        )
        for state_family in REQUIRED_RUNTIME_STATE_FAMILIES
    )
    dependency_hash_by_label = {
        binding.state_family: binding.state_input_binding_contract_hash
        for binding in state_bindings
    }
    vqm_bindings: list[RuntimeHistoryVqmDependencyBindingContract] = []
    for component_label in REQUIRED_VQM_COMPONENTS:
        binding = _build_runtime_history_vqm_dependency_binding_contract(
            component_label,
            dependency_hash_by_label,
        )
        vqm_bindings.append(binding)
        dependency_hash_by_label[component_label] = binding.vqm_dependency_binding_contract_hash
    runtime_input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_RUNTIME_HISTORY_INPUT_SET",
            "input_field_contract_hashes": tuple(runtime_input_hash_by_label.values()),
            "level_compatibility_input_binding_hashes": tuple(
                binding.level_compatibility_input_binding_contract_hash
                for binding in level_bindings
            ),
            "state_input_binding_hashes": tuple(
                binding.state_input_binding_contract_hash
                for binding in state_bindings
            ),
            "vqm_dependency_binding_hashes": tuple(
                binding.vqm_dependency_binding_contract_hash
                for binding in vqm_bindings
            ),
            "source_input_manifest_contract_hash": manifest.source_input_manifest_contract_hash,
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_RUNTIME_HISTORY_INPUT_CONTRACT",
            "level_compatibility_contract_hash": (
                level_compatibility_contract.level_compatibility_contract_bundle_hash
            ),
            "level_compatibility_input_contract_hash": (
                level_compatibility_input_contract.level_compatibility_input_contract_hash
            ),
            "runtime_history_input_policy_hash": canonical_sha256(
                {
                    "artifact": "S27_V2_RUNTIME_HISTORY_INPUT_POLICY",
                    "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
                }
            ),
            "runtime_history_input_set_hash": runtime_input_set_hash,
            "source_input_manifest_contract_hash": manifest.source_input_manifest_contract_hash,
        }
    )
    contract = RuntimeHistoryInputContractBundle(
        status=S27_V2_RUNTIME_HISTORY_INPUT_CONTRACT_ONLY_STATUS,
        source_input_manifest_contract_hash=manifest.source_input_manifest_contract_hash,
        source_input_manifest_hash=manifest.source_input_manifest_hash,
        level_compatibility_input_contract_hash=(
            level_compatibility_input_contract.level_compatibility_input_contract_hash
        ),
        level_compatibility_contract_hash=level_compatibility_contract.level_compatibility_contract_bundle_hash,
        runtime_history_input_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_RUNTIME_HISTORY_INPUT_POLICY",
                "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
            }
        ),
        source_input_manifest_contract_bundle=manifest,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label={
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ].manifest_field_contract_hash
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        },
        expected_selected_row_hash_by_input_label={
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ].selected_row_hash
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        },
        expected_selected_row_locator_hash_by_input_label={
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ].selected_row_locator_hash
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        },
        level_compatibility_input_bindings=level_bindings,
        state_input_binding_contracts=state_bindings,
        vqm_dependency_binding_contracts=tuple(vqm_bindings),
        runtime_history_input_set_hash=runtime_input_set_hash,
        runtime_history_input_contract_hash=contract_hash,
    )
    _validate_runtime_history_input_contract_local_only(
        contract,
        manifest,
        level_compatibility_input_contract,
        level_compatibility_contract,
    )
    return contract


def build_runtime_history_contract(
    slice2_artifacts: LocalParserFileReplaySlice2Artifacts,
    runtime_history_input_contract: RuntimeHistoryInputContractBundle,
    level_compatibility_contract: LevelCompatibilityContractBundle,
) -> RuntimeHistoryContractBundle:
    slice2_artifacts.validate()
    _validate_runtime_history_input_contract_local_only(
        runtime_history_input_contract,
        slice2_artifacts.source_input_manifest_contract,
        build_level_compatibility_input_contract(slice2_artifacts),
        level_compatibility_contract,
    )
    source_row_batch = slice2_artifacts.slice1_artifacts.source_row_batch_contract
    family_hash_by_family = _source_row_batch_family_contract_hash_by_family(source_row_batch)
    first_daily_family = _source_row_batch_family_contract_by_family(source_row_batch)[
        "DAILY_CONTINUOUS_COMPLETED_BAR"
    ]
    source_binding = RuntimeHistorySourceBinding(
        source_input_manifest_hash=runtime_history_input_contract.source_input_manifest_hash,
        level_compatibility_contract_hash=level_compatibility_contract.level_compatibility_contract_bundle_hash,
        daily_continuous_row_family_hash=family_hash_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"],
        daily_current_contract_row_family_hash=family_hash_by_family[
            "DAILY_CURRENT_CONTRACT_COMPLETED_BAR"
        ],
        hourly_decision_row_family_hash=family_hash_by_family["HOURLY_DECISION_COMPLETED_BAR"],
        completed_bar_policy_hash=first_daily_family.completed_bar_policy_hash,
        strict_prior_policy_hash=first_daily_family.strict_prior_policy_hash,
        source_binding_hash="0" * 64,
    )
    source_binding = RuntimeHistorySourceBinding(
        **{
            **asdict(source_binding),
            "source_binding_hash": canonical_sha256(_runtime_history_source_binding_hash_payload(source_binding)),
        }
    )
    state_input_binding_hash_by_state = {
        binding.state_family: binding.state_input_binding_contract_hash
        for binding in runtime_history_input_contract.state_input_binding_contracts
    }
    state_contracts = tuple(
        _build_runtime_state_family_contract(
            state_family,
            state_input_binding_hash_by_state,
        )
        for state_family in REQUIRED_RUNTIME_STATE_FAMILIES
    )
    dependency_hash_by_label = {
        contract.state_family: contract.state_contract_hash
        for contract in state_contracts
    }
    component_contracts: list[VqmComponentContract] = []
    for component_label in REQUIRED_VQM_COMPONENTS:
        contract = _build_vqm_component_contract(component_label, dependency_hash_by_label)
        component_contracts.append(contract)
        dependency_hash_by_label[component_label] = contract.component_contract_hash
    runtime_contract = RuntimeHistoryContractBundle(
        status=S27_V2_RUNTIME_HISTORY_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        state_contracts=state_contracts,
        vqm_component_contracts=tuple(component_contracts),
        sigma_estimator_definition_hash=canonical_sha256(
            {"artifact": "S27_V2_SIGMA_ESTIMATOR_DEFINITION", "scope": "LOCAL_ONLY_SCAFFOLD"}
        ),
        sigma_input_window_policy_hash=canonical_sha256(
            {"artifact": "S27_V2_SIGMA_INPUT_WINDOW_POLICY", "scope": "LOCAL_ONLY_SCAFFOLD"}
        ),
        sigma_annualization_policy_hash=canonical_sha256(
            {"artifact": "S27_V2_SIGMA_ANNUALIZATION_POLICY", "scope": "LOCAL_ONLY_SCAFFOLD"}
        ),
        runtime_history_ledger_schema_hash=canonical_sha256(
            {"artifact": "S27_V2_RUNTIME_HISTORY_LEDGER_SCHEMA", "scope": "LOCAL_ONLY_SCAFFOLD"}
        ),
        runtime_history_contract_bundle_hash="0" * 64,
    )
    runtime_contract = RuntimeHistoryContractBundle(
        **{
            **asdict(runtime_contract),
            "source_binding": source_binding,
            "state_contracts": state_contracts,
            "vqm_component_contracts": tuple(component_contracts),
            "runtime_history_contract_bundle_hash": canonical_sha256(
                _runtime_history_contract_bundle_hash_payload(runtime_contract)
            ),
        }
    )
    _validate_runtime_history_contract_content_bound(
        runtime_contract,
        runtime_history_input_contract,
        level_compatibility_contract,
        source_row_batch,
    )
    return runtime_contract


def build_forecast_input_contract(
    slice3_artifacts: LocalParserFileReplaySlice3Artifacts,
) -> ForecastInputContractBundle:
    slice3_artifacts.validate()
    policy_hash = _slice4_policy_hash("FORECAST_INPUT")
    active_source_hash_by_label = _forecast_active_source_hash_by_label(
        policy_hash,
        slice3_artifacts.runtime_history_input_contract,
        slice3_artifacts.runtime_history_contract,
    )
    input_fields = tuple(
        _build_forecast_input_field_contract(
            input_label,
            active_source_hash_by_label[input_label],
            policy_hash,
        )
        for input_label in REQUIRED_FORECAST_INPUTS
    )
    dependency_hash_by_label = {
        field.input_label: field.input_field_contract_hash
        for field in input_fields
    }
    component_bindings_list: list[ForecastDependencyBindingContract] = []
    for component_family in REQUIRED_FORECAST_COMPONENT_FAMILIES:
        binding = _build_forecast_dependency_binding_contract(
            component_family,
            REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT[component_family],
            dependency_hash_by_label,
            "COMPONENT",
        )
        component_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    component_bindings = tuple(component_bindings_list)
    branch_bindings_list: list[ForecastDependencyBindingContract] = []
    for branch_label in REQUIRED_FORECAST_DECISION_BRANCHES:
        binding = _build_forecast_dependency_binding_contract(
            branch_label,
            REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH[branch_label],
            dependency_hash_by_label,
            "DECISION_BRANCH",
        )
        branch_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    branch_bindings = tuple(branch_bindings_list)
    invariant_bindings = tuple(
        _build_forecast_dependency_binding_contract(
            invariant_label,
            REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT[invariant_label],
            dependency_hash_by_label,
            "INVARIANT",
        )
        for invariant_label in REQUIRED_FORECAST_INVARIANTS
    )
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FORECAST_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in component_bindings
            ),
            "decision_branch_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in branch_bindings
            ),
            "input_field_contract_hashes": tuple(dependency_hash_by_label[label] for label in REQUIRED_FORECAST_INPUTS),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in invariant_bindings
            ),
            "runtime_history_contract_bundle_hash": (
                slice3_artifacts.runtime_history_contract.runtime_history_contract_bundle_hash
            ),
            "runtime_history_input_contract_hash": (
                slice3_artifacts.runtime_history_input_contract.runtime_history_input_contract_hash
            ),
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FORECAST_INPUT_CONTRACT",
            "forecast_input_policy_hash": policy_hash,
            "forecast_input_set_hash": input_set_hash,
            "runtime_history_contract_bundle_hash": (
                slice3_artifacts.runtime_history_contract.runtime_history_contract_bundle_hash
            ),
            "runtime_history_input_contract_hash": (
                slice3_artifacts.runtime_history_input_contract.runtime_history_input_contract_hash
            ),
            "source_input_manifest_contract_hash": (
                slice3_artifacts.runtime_history_input_contract.source_input_manifest_contract_hash
            ),
        }
    )
    contract = ForecastInputContractBundle(
        status=S27_V2_FORECAST_INPUT_CONTRACT_ONLY_STATUS,
        source_input_manifest_contract_hash=(
            slice3_artifacts.runtime_history_input_contract.source_input_manifest_contract_hash
        ),
        runtime_history_input_contract_hash=(
            slice3_artifacts.runtime_history_input_contract.runtime_history_input_contract_hash
        ),
        runtime_history_contract_bundle_hash=(
            slice3_artifacts.runtime_history_contract.runtime_history_contract_bundle_hash
        ),
        forecast_input_policy_hash=policy_hash,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label=active_source_hash_by_label,
        component_dependency_bindings=component_bindings,
        decision_branch_dependency_bindings=branch_bindings,
        invariant_dependency_bindings=invariant_bindings,
        forecast_input_set_hash=input_set_hash,
        forecast_input_contract_hash=contract_hash,
    )
    _validate_forecast_input_contract_local_only(contract, slice3_artifacts)
    return contract


def build_forecast_contract(
    slice3_artifacts: LocalParserFileReplaySlice3Artifacts,
    forecast_input_contract: ForecastInputContractBundle,
) -> ForecastContractBundle:
    slice3_artifacts.validate()
    _validate_forecast_input_contract_local_only(forecast_input_contract, slice3_artifacts)
    source_binding = ForecastSourceBinding(
        source_input_manifest_hash=slice3_artifacts.runtime_history_input_contract.source_input_manifest_hash,
        runtime_history_contract_bundle_hash=slice3_artifacts.runtime_history_contract.runtime_history_contract_bundle_hash,
        runtime_history_ledger_schema_hash=slice3_artifacts.runtime_history_contract.runtime_history_ledger_schema_hash,
        forecast_ledger_schema_hash=_slice4_policy_hash("FORECAST_LEDGER_SCHEMA"),
        completed_bar_policy_hash=slice3_artifacts.runtime_history_contract.source_binding.completed_bar_policy_hash,
        strict_prior_policy_hash=slice3_artifacts.runtime_history_contract.source_binding.strict_prior_policy_hash,
        forecast_source_binding_hash="0" * 64,
    )
    source_binding = ForecastSourceBinding(
        **{
            **asdict(source_binding),
            "forecast_source_binding_hash": canonical_sha256(
                _forecast_source_binding_hash_payload(source_binding)
            ),
        }
    )
    dependency_hash_by_label = _forecast_input_hash_by_label(forecast_input_contract)
    component_contracts_list: list[ForecastComponentContract] = []
    for component_family in REQUIRED_FORECAST_COMPONENT_FAMILIES:
        component = _build_forecast_component_contract(component_family, dependency_hash_by_label)
        component_contracts_list.append(component)
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    component_contracts = tuple(component_contracts_list)
    branch_contracts_list: list[ForecastDecisionBranchContract] = []
    for branch_label in REQUIRED_FORECAST_DECISION_BRANCHES:
        branch = _build_forecast_branch_contract(branch_label, dependency_hash_by_label)
        branch_contracts_list.append(branch)
        dependency_hash_by_label[branch.branch_label] = branch.branch_contract_hash
    branch_contracts = tuple(branch_contracts_list)
    invariant_contracts = tuple(
        _build_forecast_invariant_contract(invariant, dependency_hash_by_label)
        for invariant in REQUIRED_FORECAST_INVARIANTS
    )
    contract = ForecastContractBundle(
        status=S27_V2_FORECAST_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        component_contracts=component_contracts,
        decision_branch_contracts=branch_contracts,
        invariant_contracts=invariant_contracts,
        scalar_source_lock_hash=forecast_input_contract.forecast_input_policy_hash,
        cap_policy_hash=forecast_input_contract.forecast_input_policy_hash,
        desired_position_link_policy_hash=forecast_input_contract.forecast_input_policy_hash,
        forecast_contract_bundle_hash="0" * 64,
    )
    contract = ForecastContractBundle(
        **{
            **asdict(contract),
            "source_binding": source_binding,
            "component_contracts": component_contracts,
            "decision_branch_contracts": branch_contracts,
            "invariant_contracts": invariant_contracts,
            "forecast_contract_bundle_hash": canonical_sha256(
                _forecast_contract_bundle_hash_payload(contract)
            ),
        }
    )
    _validate_forecast_contract_content_bound(contract, forecast_input_contract, slice3_artifacts)
    return contract


def build_position_input_contract(
    slice3_artifacts: LocalParserFileReplaySlice3Artifacts,
    forecast_input_contract: ForecastInputContractBundle,
    forecast_contract: ForecastContractBundle,
) -> PositionInputContractBundle:
    slice3_artifacts.validate()
    _validate_forecast_input_contract_local_only(forecast_input_contract, slice3_artifacts)
    _validate_forecast_contract_content_bound(forecast_contract, forecast_input_contract, slice3_artifacts)
    policy_hash = _slice4_policy_hash("POSITION_INPUT")
    active_source_hash_by_label = _position_active_source_hash_by_label(policy_hash, forecast_contract)
    input_fields = tuple(
        _build_position_input_field_contract(
            input_label,
            active_source_hash_by_label[input_label],
            policy_hash,
        )
        for input_label in REQUIRED_POSITION_INPUTS
    )
    dependency_hash_by_label = {
        field.input_label: field.input_field_contract_hash
        for field in input_fields
    }
    component_bindings_list: list[PositionDependencyBindingContract] = []
    for component in REQUIRED_POSITION_COMPONENT_FAMILIES:
        binding = _build_position_dependency_binding_contract(
            component,
            REQUIRED_POSITION_DEPENDENCIES_BY_COMPONENT[component],
            dependency_hash_by_label,
            "COMPONENT",
        )
        component_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    component_bindings = tuple(component_bindings_list)
    invariant_bindings = tuple(
        _build_position_dependency_binding_contract(
            invariant,
            REQUIRED_POSITION_DEPENDENCIES_BY_INVARIANT[invariant],
            dependency_hash_by_label,
            "INVARIANT",
        )
        for invariant in REQUIRED_POSITION_INVARIANTS
    )
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_POSITION_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in component_bindings
            ),
            "forecast_contract_bundle_hash": forecast_contract.forecast_contract_bundle_hash,
            "forecast_input_contract_hash": forecast_input_contract.forecast_input_contract_hash,
            "input_field_contract_hashes": tuple(
                field.input_field_contract_hash for field in input_fields
            ),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in invariant_bindings
            ),
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_POSITION_INPUT_CONTRACT",
            "forecast_contract_bundle_hash": forecast_contract.forecast_contract_bundle_hash,
            "forecast_input_contract_hash": forecast_input_contract.forecast_input_contract_hash,
            "position_input_policy_hash": policy_hash,
            "position_input_set_hash": input_set_hash,
            "source_input_manifest_contract_hash": forecast_input_contract.source_input_manifest_contract_hash,
        }
    )
    contract = PositionInputContractBundle(
        status=S27_V2_POSITION_INPUT_CONTRACT_ONLY_STATUS,
        source_input_manifest_contract_hash=forecast_input_contract.source_input_manifest_contract_hash,
        forecast_input_contract_hash=forecast_input_contract.forecast_input_contract_hash,
        forecast_contract_bundle_hash=forecast_contract.forecast_contract_bundle_hash,
        position_input_policy_hash=policy_hash,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label=active_source_hash_by_label,
        component_dependency_bindings=component_bindings,
        invariant_dependency_bindings=invariant_bindings,
        position_input_set_hash=input_set_hash,
        position_input_contract_hash=contract_hash,
    )
    _validate_position_input_contract_local_only(contract, forecast_input_contract, forecast_contract)
    return contract


def build_position_contract(
    forecast_input_contract: ForecastInputContractBundle,
    forecast_contract: ForecastContractBundle,
    position_input_contract: PositionInputContractBundle,
) -> PositionContractBundle:
    forecast_contract.validate()
    _validate_position_input_contract_local_only(
        position_input_contract,
        forecast_input_contract,
        forecast_contract,
    )
    source_binding = PositionSourceBinding(
        source_input_manifest_hash=forecast_contract.source_binding.source_input_manifest_hash,
        forecast_contract_bundle_hash=forecast_contract.forecast_contract_bundle_hash,
        forecast_ledger_schema_hash=forecast_contract.source_binding.forecast_ledger_schema_hash,
        desired_position_ledger_schema_hash=_slice4_policy_hash("DESIRED_POSITION_LEDGER_SCHEMA"),
        completed_bar_policy_hash=forecast_contract.source_binding.completed_bar_policy_hash,
        strict_prior_policy_hash=forecast_contract.source_binding.strict_prior_policy_hash,
        position_source_binding_hash="0" * 64,
    )
    source_binding = PositionSourceBinding(
        **{
            **asdict(source_binding),
            "position_source_binding_hash": canonical_sha256(
                _position_source_binding_hash_payload(source_binding)
            ),
        }
    )
    dependency_hash_by_label = _position_input_hash_by_label(position_input_contract)
    component_contracts_list: list[PositionComponentContract] = []
    for component_family in REQUIRED_POSITION_COMPONENT_FAMILIES:
        component = _build_position_component_contract(component_family, dependency_hash_by_label)
        component_contracts_list.append(component)
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    component_contracts = tuple(component_contracts_list)
    rounding_policy_contracts = tuple(
        _build_position_rounding_policy_contract(label, position_input_contract.position_input_policy_hash)
        for label in REQUIRED_ROUNDING_POLICY_LABELS
    )
    invariant_contracts = tuple(
        _build_position_invariant_contract(invariant, dependency_hash_by_label)
        for invariant in REQUIRED_POSITION_INVARIANTS
    )
    contract = PositionContractBundle(
        status=S27_V2_POSITION_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        component_contracts=component_contracts,
        rounding_policy_contracts=rounding_policy_contracts,
        invariant_contracts=invariant_contracts,
        forecast_to_position_divisor_policy_hash=position_input_contract.position_input_policy_hash,
        initial_position_policy_hash=position_input_contract.position_input_policy_hash,
        desired_position_contract_bundle_hash="0" * 64,
    )
    contract = PositionContractBundle(
        **{
            **asdict(contract),
            "source_binding": source_binding,
            "component_contracts": component_contracts,
            "rounding_policy_contracts": rounding_policy_contracts,
            "invariant_contracts": invariant_contracts,
            "desired_position_contract_bundle_hash": canonical_sha256(
                _position_contract_bundle_hash_payload(contract)
            ),
        }
    )
    _validate_position_contract_content_bound(contract, position_input_contract, forecast_contract)
    return contract


def build_order_input_contract(
    slice3_artifacts: LocalParserFileReplaySlice3Artifacts,
    forecast_contract: ForecastContractBundle,
    position_input_contract: PositionInputContractBundle,
    position_contract: PositionContractBundle,
) -> OrderInputContractBundle:
    slice3_artifacts.validate()
    _validate_position_contract_content_bound(position_contract, position_input_contract, forecast_contract)
    policy_hash = _slice4_policy_hash("ORDER_INPUT")
    active_source_hash_by_label = _order_active_source_hash_by_label(policy_hash, position_contract)
    input_fields = tuple(
        _build_order_input_field_contract(input_label, active_source_hash_by_label[input_label], policy_hash)
        for input_label in REQUIRED_ORDER_INPUTS
    )
    dependency_hash_by_label = {
        field.input_label: field.input_field_contract_hash
        for field in input_fields
    }
    component_bindings_list: list[OrderDependencyBindingContract] = []
    for component in REQUIRED_ORDER_COMPONENT_FAMILIES:
        binding = _build_order_dependency_binding_contract(
            component,
            REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT[component],
            dependency_hash_by_label,
            "COMPONENT",
        )
        component_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    component_bindings = tuple(component_bindings_list)
    invariant_bindings = tuple(
        _build_order_dependency_binding_contract(
            invariant,
            REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT[invariant],
            dependency_hash_by_label,
            "INVARIANT",
        )
        for invariant in REQUIRED_ORDER_INVARIANTS
    )
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_ORDER_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in component_bindings
            ),
            "input_field_contract_hashes": tuple(field.input_field_contract_hash for field in input_fields),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in invariant_bindings
            ),
            "position_contract_bundle_hash": position_contract.desired_position_contract_bundle_hash,
            "position_input_contract_hash": position_input_contract.position_input_contract_hash,
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_ORDER_INPUT_CONTRACT",
            "order_input_policy_hash": policy_hash,
            "order_input_set_hash": input_set_hash,
            "position_contract_bundle_hash": position_contract.desired_position_contract_bundle_hash,
            "position_input_contract_hash": position_input_contract.position_input_contract_hash,
            "source_input_manifest_contract_hash": position_input_contract.source_input_manifest_contract_hash,
        }
    )
    contract = OrderInputContractBundle(
        status=S27_V2_ORDER_INPUT_CONTRACT_ONLY_STATUS,
        source_input_manifest_contract_hash=position_input_contract.source_input_manifest_contract_hash,
        position_input_contract_hash=position_input_contract.position_input_contract_hash,
        position_contract_bundle_hash=position_contract.desired_position_contract_bundle_hash,
        order_input_policy_hash=policy_hash,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label=active_source_hash_by_label,
        component_dependency_bindings=component_bindings,
        invariant_dependency_bindings=invariant_bindings,
        order_input_set_hash=input_set_hash,
        order_input_contract_hash=contract_hash,
    )
    _validate_order_input_contract_local_only(contract, position_input_contract, position_contract)
    return contract


def build_order_contract(
    position_input_contract: PositionInputContractBundle,
    position_contract: PositionContractBundle,
    order_input_contract: OrderInputContractBundle,
) -> OrderContractBundle:
    position_contract.validate()
    _validate_order_input_contract_local_only(
        order_input_contract,
        position_input_contract,
        position_contract,
    )
    source_binding = OrderSourceBinding(
        source_input_manifest_hash=position_contract.source_binding.source_input_manifest_hash,
        position_contract_bundle_hash=position_contract.desired_position_contract_bundle_hash,
        desired_position_ledger_schema_hash=position_contract.source_binding.desired_position_ledger_schema_hash,
        limit_order_ledger_schema_hash=_slice4_policy_hash("LIMIT_ORDER_LEDGER_SCHEMA"),
        market_order_ledger_schema_hash=_slice4_policy_hash("MARKET_ORDER_LEDGER_SCHEMA"),
        working_order_transition_schema_hash=_slice4_policy_hash("WORKING_ORDER_TRANSITION_SCHEMA"),
        completed_bar_policy_hash=position_contract.source_binding.completed_bar_policy_hash,
        strict_prior_policy_hash=position_contract.source_binding.strict_prior_policy_hash,
        order_source_binding_hash="0" * 64,
    )
    source_binding = OrderSourceBinding(
        **{
            **asdict(source_binding),
            "order_source_binding_hash": canonical_sha256(_order_source_binding_hash_payload(source_binding)),
        }
    )
    dependency_hash_by_label = _order_input_hash_by_label(order_input_contract)
    component_contracts_list: list[OrderComponentContract] = []
    for component_family in REQUIRED_ORDER_COMPONENT_FAMILIES:
        component = _build_order_component_contract(component_family, dependency_hash_by_label)
        component_contracts_list.append(component)
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    component_contracts = tuple(component_contracts_list)
    order_kind_contracts = tuple(
        _build_order_kind_contract(kind, order_input_contract.order_input_policy_hash)
        for kind in REQUIRED_ORDER_KIND_LABELS
    )
    transition_kind_contracts = tuple(
        _build_order_transition_kind_contract(kind, order_input_contract.order_input_policy_hash)
        for kind in REQUIRED_ORDER_TRANSITION_KIND_LABELS
    )
    invariant_contracts = tuple(
        _build_order_invariant_contract(invariant, dependency_hash_by_label)
        for invariant in REQUIRED_ORDER_INVARIANTS
    )
    contract = OrderContractBundle(
        status=S27_V2_ORDER_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        component_contracts=component_contracts,
        order_kind_contracts=order_kind_contracts,
        transition_kind_contracts=transition_kind_contracts,
        invariant_contracts=invariant_contracts,
        tick_rounding_policy_hash=order_input_contract.order_input_policy_hash,
        working_limit_lifecycle_policy_hash=order_input_contract.order_input_policy_hash,
        overnight_recompute_policy_hash=order_input_contract.order_input_policy_hash,
        roll_boundary_policy_hash=order_input_contract.order_input_policy_hash,
        order_contract_bundle_hash="0" * 64,
    )
    contract = OrderContractBundle(
        **{
            **asdict(contract),
            "source_binding": source_binding,
            "component_contracts": component_contracts,
            "order_kind_contracts": order_kind_contracts,
            "transition_kind_contracts": transition_kind_contracts,
            "invariant_contracts": invariant_contracts,
            "order_contract_bundle_hash": canonical_sha256(_order_contract_bundle_hash_payload(contract)),
        }
    )
    _validate_order_contract_content_bound(contract, order_input_contract, position_contract)
    return contract


def build_fill_input_contract(
    slice4_artifacts: LocalParserFileReplaySlice4Artifacts,
) -> FillInputContractBundle:
    slice4_artifacts.validate()
    policy_hash = _slice5_policy_hash("FILL_INPUT")
    active_source_hash_by_label = _fill_active_source_hash_by_label(
        policy_hash,
        slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract,
        slice4_artifacts.order_contract,
    )
    input_fields = tuple(
        _build_fill_input_field_contract(
            input_label,
            active_source_hash_by_label[input_label],
            policy_hash,
        )
        for input_label in REQUIRED_FILL_INPUTS
    )
    dependency_hash_by_label = {
        field.input_label: field.input_field_contract_hash
        for field in input_fields
    }
    component_bindings_list: list[FillDependencyBindingContract] = []
    for component in REQUIRED_FILL_COMPONENT_FAMILIES:
        binding = _build_fill_dependency_binding_contract(
            component,
            REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT[component],
            dependency_hash_by_label,
            "COMPONENT",
        )
        component_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    component_bindings = tuple(component_bindings_list)
    invariant_bindings = tuple(
        _build_fill_dependency_binding_contract(
            invariant,
            REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT[invariant],
            dependency_hash_by_label,
            "INVARIANT",
        )
        for invariant in REQUIRED_FILL_INVARIANTS
    )
    source_manifest = slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FILL_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in component_bindings
            ),
            "input_field_contract_hashes": tuple(field.input_field_contract_hash for field in input_fields),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in invariant_bindings
            ),
            "order_contract_bundle_hash": slice4_artifacts.order_contract.order_contract_bundle_hash,
            "order_input_contract_hash": slice4_artifacts.order_input_contract.order_input_contract_hash,
            "source_input_manifest_contract_hash": source_manifest.source_input_manifest_contract_hash,
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FILL_INPUT_CONTRACT",
            "fill_input_policy_hash": policy_hash,
            "fill_input_set_hash": input_set_hash,
            "order_contract_bundle_hash": slice4_artifacts.order_contract.order_contract_bundle_hash,
            "order_input_contract_hash": slice4_artifacts.order_input_contract.order_input_contract_hash,
            "source_input_manifest_contract_hash": source_manifest.source_input_manifest_contract_hash,
        }
    )
    contract = FillInputContractBundle(
        status=S27_V2_FILL_INPUT_CONTRACT_ONLY_STATUS,
        source_input_manifest_contract_hash=source_manifest.source_input_manifest_contract_hash,
        order_input_contract_hash=slice4_artifacts.order_input_contract.order_input_contract_hash,
        order_contract_bundle_hash=slice4_artifacts.order_contract.order_contract_bundle_hash,
        fill_input_policy_hash=policy_hash,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label=active_source_hash_by_label,
        component_dependency_bindings=component_bindings,
        invariant_dependency_bindings=invariant_bindings,
        fill_input_set_hash=input_set_hash,
        fill_input_contract_hash=contract_hash,
    )
    _validate_fill_input_contract_local_only(contract, slice4_artifacts)
    return contract


def build_fill_contract(
    slice4_artifacts: LocalParserFileReplaySlice4Artifacts,
    fill_input_contract: FillInputContractBundle,
) -> FillContractBundle:
    slice4_artifacts.validate()
    _validate_fill_input_contract_local_only(fill_input_contract, slice4_artifacts)
    order_contract = slice4_artifacts.order_contract
    source_binding = FillSourceBinding(
        source_input_manifest_hash=order_contract.source_binding.source_input_manifest_hash,
        order_contract_bundle_hash=order_contract.order_contract_bundle_hash,
        limit_order_ledger_schema_hash=order_contract.source_binding.limit_order_ledger_schema_hash,
        market_order_ledger_schema_hash=order_contract.source_binding.market_order_ledger_schema_hash,
        working_order_transition_schema_hash=order_contract.source_binding.working_order_transition_schema_hash,
        fill_ledger_schema_hash=_slice5_policy_hash("FILL_LEDGER_SCHEMA"),
        completed_bar_policy_hash=order_contract.source_binding.completed_bar_policy_hash,
        strict_prior_policy_hash=order_contract.source_binding.strict_prior_policy_hash,
        fill_source_binding_hash="0" * 64,
    )
    source_binding = FillSourceBinding(
        **{
            **asdict(source_binding),
            "fill_source_binding_hash": canonical_sha256(_fill_source_binding_hash_payload(source_binding)),
        }
    )
    dependency_hash_by_label = _fill_input_hash_by_label(fill_input_contract)
    component_contracts_list: list[FillComponentContract] = []
    for component in REQUIRED_FILL_COMPONENT_FAMILIES:
        contract = _build_fill_component_contract(component, dependency_hash_by_label)
        component_contracts_list.append(contract)
        dependency_hash_by_label[contract.component_family] = contract.component_contract_hash
    component_contracts = tuple(component_contracts_list)
    price_provenance_contracts = tuple(
        _build_fill_price_provenance_contract(
            provenance,
            fill_input_contract.fill_input_policy_hash,
        )
        for provenance in REQUIRED_FILL_PRICE_PROVENANCE_LABELS
    )
    branch_contracts = tuple(
        _build_fill_branch_contract(
            branch,
            dependency_hash_by_label,
        )
        for branch in REQUIRED_FILL_BRANCH_LABELS
    )
    for branch in branch_contracts:
        dependency_hash_by_label[branch.branch_label] = branch.branch_contract_hash
    invariant_contracts = tuple(
        _build_fill_invariant_contract(invariant, dependency_hash_by_label)
        for invariant in REQUIRED_FILL_INVARIANTS
    )
    contract = FillContractBundle(
        status=S27_V2_FILL_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        component_contracts=component_contracts,
        price_provenance_contracts=price_provenance_contracts,
        branch_contracts=branch_contracts,
        invariant_contracts=invariant_contracts,
        one_hour_lag_policy_hash=fill_input_contract.fill_input_policy_hash,
        session_gap_policy_hash=fill_input_contract.fill_input_policy_hash,
        fill_contract_bundle_hash="0" * 64,
    )
    contract = FillContractBundle(
        **{
            **asdict(contract),
            "source_binding": source_binding,
            "component_contracts": component_contracts,
            "price_provenance_contracts": price_provenance_contracts,
            "branch_contracts": branch_contracts,
            "invariant_contracts": invariant_contracts,
            "fill_contract_bundle_hash": canonical_sha256(_fill_contract_bundle_hash_payload(contract)),
        }
    )
    _validate_fill_contract_content_bound(contract, fill_input_contract, slice4_artifacts)
    return contract


def build_local_only_replay_trust_root(
    inputs: LocalParserFileReplaySlice1Inputs,
    slice5_artifacts: LocalParserFileReplaySlice5Artifacts,
) -> ReplayTrustRoot:
    slice5_artifacts.validate()
    external_authority = (
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_row_selection_external_authority
    )
    source_row_batch_contract = (
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.source_row_batch_contract
    )
    trust_root = ReplayTrustRoot(
        replay_trust_root_hash=external_authority.replay_trust_root_hash,
        source_lock_hash=_local_only_trust_hash("SOURCE_LOCK"),
        local_data_contract_hash=inputs.input_directory.input_directory_declaration_hash,
        provenance_design_hash=_local_only_trust_hash("PROVENANCE_DESIGN"),
        runner_implementation_hash=_local_only_trust_hash("RUNNER_IMPLEMENTATION"),
        parser_extractor_source_hash=inputs.parser_plan_bundle.parser_plan_bundle_hash,
        dependency_runtime_manifest_hash=_local_only_trust_hash("DEPENDENCY_RUNTIME_MANIFEST"),
        replay_config_hash=_local_only_trust_hash("REPLAY_CONFIG"),
        source_input_universe_manifest_hash=inputs.source_universe_contract.source_universe_contract_bundle_hash,
        raw_source_file_hash_set_hash=inputs.input_directory.raw_file_hash_set_hash,
        source_row_batch_contract_hash=source_row_batch_contract.source_row_batch_contract_hash,
        source_row_batch_set_hash=source_row_batch_contract.source_row_batch_set_hash,
        source_row_locator_hash=inputs.row_locator_contract.row_locator_contract_bundle_hash,
        source_row_selection_authority_hash=external_authority.source_row_selection_authority_hash,
        canonical_serialization_policy=inputs.canonical_serialization_policy,
        session_calendar_policy_hash=_local_only_trust_hash("SESSION_CALENDAR_POLICY"),
        roll_calendar_policy_hash=_local_only_trust_hash("ROLL_CALENDAR_POLICY"),
        tick_rounding_policy_hash=_local_only_trust_hash("TICK_ROUNDING_POLICY"),
        commission_policy_hash=_local_only_trust_hash("COMMISSION_POLICY"),
        spread_unit_policy_hash=_local_only_trust_hash("SPREAD_UNIT_POLICY"),
        contract_multiplier_currency_policy_hash=_local_only_trust_hash(
            "CONTRACT_MULTIPLIER_CURRENCY_POLICY"
        ),
        daily_hourly_level_compatibility_policy_hash=(
            slice5_artifacts.slice4_artifacts.slice3_artifacts.level_compatibility_contract
            .daily_hourly_level_compatibility_policy_hash
        ),
        stale_evidence_supersession_manifest_hash=_local_only_trust_hash(
            "STALE_EVIDENCE_SUPERSESSION_MANIFEST"
        ),
        active_evidence_manifest_hash=external_authority.active_evidence_manifest_hash,
    )
    trust_root.validate()
    return trust_root


def build_local_only_evidence_manifest(replay_trust_root: ReplayTrustRoot) -> EvidenceManifest:
    replay_trust_root.validate()
    active_hash_by_type = {
        "SOURCE_LOCK": replay_trust_root.source_lock_hash,
        "LOCAL_DATA_CONTRACT": replay_trust_root.local_data_contract_hash,
        "PROVENANCE_DESIGN": replay_trust_root.provenance_design_hash,
        "RUNNER_IMPLEMENTATION": replay_trust_root.runner_implementation_hash,
        "PARSER_EXTRACTOR_SOURCE": replay_trust_root.parser_extractor_source_hash,
        "DEPENDENCY_RUNTIME_MANIFEST": replay_trust_root.dependency_runtime_manifest_hash,
        "REPLAY_CONFIG": replay_trust_root.replay_config_hash,
        "SOURCE_INPUT_UNIVERSE_MANIFEST": replay_trust_root.source_input_universe_manifest_hash,
        "RAW_SOURCE_FILE_HASH_SET": replay_trust_root.raw_source_file_hash_set_hash,
        "SOURCE_ROW_BATCH_CONTRACT": replay_trust_root.source_row_batch_contract_hash,
        "SOURCE_ROW_BATCH_SET": replay_trust_root.source_row_batch_set_hash,
        "SOURCE_ROW_LOCATOR": replay_trust_root.source_row_locator_hash,
        "SOURCE_ROW_SELECTION_AUTHORITY": replay_trust_root.source_row_selection_authority_hash,
        "CANONICAL_SERIALIZATION_POLICY": (
            replay_trust_root.canonical_serialization_policy.canonical_serialization_policy_hash
        ),
        "CANONICAL_SERIALIZATION_SCHEMA": replay_trust_root.canonical_serialization_policy.schema_hash,
        "HASH_ALGORITHM_VERSION": (
            replay_trust_root.canonical_serialization_policy.hash_algorithm_version_hash
        ),
        "FIELD_ORDERING_POLICY": replay_trust_root.canonical_serialization_policy.field_ordering_policy_hash,
        "DECIMAL_FLOAT_NORMALIZATION_POLICY": (
            replay_trust_root.canonical_serialization_policy.decimal_float_normalization_policy_hash
        ),
        "TIMEZONE_NORMALIZATION_POLICY": (
            replay_trust_root.canonical_serialization_policy.timezone_normalization_policy_hash
        ),
        "ROW_ORDERING_COLLATION_POLICY": (
            replay_trust_root.canonical_serialization_policy.row_ordering_collation_policy_hash
        ),
        "NULL_MISSING_SENTINEL_POLICY": (
            replay_trust_root.canonical_serialization_policy.null_missing_sentinel_policy_hash
        ),
        "STRING_ENCODING_POLICY": replay_trust_root.canonical_serialization_policy.string_encoding_policy_hash,
        "HASH_PAYLOAD_VERSION_POLICY": (
            replay_trust_root.canonical_serialization_policy.hash_payload_version_policy_hash
        ),
        "SESSION_CALENDAR_POLICY": replay_trust_root.session_calendar_policy_hash,
        "ROLL_CALENDAR_POLICY": replay_trust_root.roll_calendar_policy_hash,
        "TICK_ROUNDING_POLICY": replay_trust_root.tick_rounding_policy_hash,
        "COMMISSION_POLICY": replay_trust_root.commission_policy_hash,
        "SPREAD_UNIT_POLICY": replay_trust_root.spread_unit_policy_hash,
        "CONTRACT_MULTIPLIER_CURRENCY_POLICY": (
            replay_trust_root.contract_multiplier_currency_policy_hash
        ),
        "DAILY_HOURLY_COMPATIBILITY_POLICY": (
            replay_trust_root.daily_hourly_level_compatibility_policy_hash
        ),
        "STALE_EVIDENCE_SUPERSESSION_MANIFEST": (
            replay_trust_root.stale_evidence_supersession_manifest_hash
        ),
    }
    entries = tuple(
        EvidenceManifestEntry(
            artifact=HashedArtifact(
                artifact_type=artifact_type,
                path=f"LOCAL_ONLY_PLACEHOLDER/{artifact_type}",
                content_hash=active_hash_by_type[artifact_type],
                status_label=ACTIVE_EVIDENCE_STATUS_LABEL,
            )
        )
        for artifact_type in REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES
    )
    manifest = EvidenceManifest(
        active_entries=entries,
        superseded_artifacts=(),
        active_evidence_manifest_hash=replay_trust_root.active_evidence_manifest_hash,
    )
    manifest.validate()
    return manifest


def build_cost_input_contract(
    slice5_artifacts: LocalParserFileReplaySlice5Artifacts,
    replay_trust_root: ReplayTrustRoot,
    evidence_manifest: EvidenceManifest,
) -> CostInputContractBundle:
    slice5_artifacts.validate()
    replay_trust_root.validate()
    evidence_manifest.validate()
    policy_hash = _slice6_policy_hash("COST_INPUT")
    active_source_hash_by_label = _cost_active_source_hash_by_label(
        policy_hash,
        replay_trust_root,
        slice5_artifacts.fill_contract,
    )
    input_fields = tuple(
        _build_cost_input_field_contract(
            input_label,
            active_source_hash_by_label[input_label],
            policy_hash,
        )
        for input_label in REQUIRED_COST_INPUTS
    )
    dependency_hash_by_label = {field.input_label: field.input_field_contract_hash for field in input_fields}
    component_binding_by_label: dict[str, CostDependencyBindingContract] = {}

    def ensure_component_binding(component: str) -> CostDependencyBindingContract:
        if component in component_binding_by_label:
            return component_binding_by_label[component]
        for dependency_label in REQUIRED_COST_DEPENDENCIES_BY_COMPONENT[component]:
            if dependency_label in REQUIRED_COST_COMPONENT_FAMILIES and dependency_label not in dependency_hash_by_label:
                ensure_component_binding(dependency_label)
        binding = _build_cost_dependency_binding_contract(
            component,
            REQUIRED_COST_DEPENDENCIES_BY_COMPONENT[component],
            dependency_hash_by_label,
            "COMPONENT",
        )
        component_binding_by_label[component] = binding
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
        return binding

    for component in REQUIRED_COST_COMPONENT_FAMILIES:
        ensure_component_binding(component)
    component_bindings = tuple(component_binding_by_label[component] for component in REQUIRED_COST_COMPONENT_FAMILIES)
    invariant_bindings = tuple(
        _build_cost_dependency_binding_contract(
            invariant,
            REQUIRED_COST_DEPENDENCIES_BY_INVARIANT[invariant],
            dependency_hash_by_label,
            "INVARIANT",
        )
        for invariant in REQUIRED_COST_INVARIANTS
    )
    source_manifest = (
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_COST_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in component_bindings
            ),
            "fill_contract_bundle_hash": slice5_artifacts.fill_contract.fill_contract_bundle_hash,
            "fill_input_contract_hash": slice5_artifacts.fill_input_contract.fill_input_contract_hash,
            "input_field_contract_hashes": tuple(field.input_field_contract_hash for field in input_fields),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in invariant_bindings
            ),
            "source_input_manifest_contract_hash": source_manifest.source_input_manifest_contract_hash,
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_COST_INPUT_CONTRACT",
            "cost_input_policy_hash": policy_hash,
            "cost_input_set_hash": input_set_hash,
            "fill_contract_bundle_hash": slice5_artifacts.fill_contract.fill_contract_bundle_hash,
            "fill_input_contract_hash": slice5_artifacts.fill_input_contract.fill_input_contract_hash,
            "source_input_manifest_contract_hash": source_manifest.source_input_manifest_contract_hash,
        }
    )
    contract = CostInputContractBundle(
        status=S27_V2_COST_INPUT_CONTRACT_ONLY_STATUS,
        source_input_manifest_contract_hash=source_manifest.source_input_manifest_contract_hash,
        fill_input_contract_hash=slice5_artifacts.fill_input_contract.fill_input_contract_hash,
        fill_contract_bundle_hash=slice5_artifacts.fill_contract.fill_contract_bundle_hash,
        cost_input_policy_hash=policy_hash,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label=active_source_hash_by_label,
        component_dependency_bindings=component_bindings,
        invariant_dependency_bindings=invariant_bindings,
        cost_input_set_hash=input_set_hash,
        cost_input_contract_hash=contract_hash,
    )
    _validate_cost_input_contract_local_only(
        contract,
        slice5_artifacts,
        replay_trust_root,
        evidence_manifest,
    )
    return contract


def build_cost_contract(
    slice5_artifacts: LocalParserFileReplaySlice5Artifacts,
    cost_input_contract: CostInputContractBundle,
    replay_trust_root: ReplayTrustRoot,
    evidence_manifest: EvidenceManifest,
) -> CostContractBundle:
    slice5_artifacts.validate()
    _validate_cost_input_contract_local_only(
        cost_input_contract,
        slice5_artifacts,
        replay_trust_root,
        evidence_manifest,
    )
    source_manifest = (
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    source_binding = CostSourceBinding(
        source_input_manifest_hash=source_manifest.source_input_manifest_hash,
        fill_contract_bundle_hash=slice5_artifacts.fill_contract.fill_contract_bundle_hash,
        fill_ledger_schema_hash=slice5_artifacts.fill_contract.source_binding.fill_ledger_schema_hash,
        commission_ledger_schema_hash=_slice6_policy_hash("COMMISSION_LEDGER_SCHEMA"),
        spread_cost_ledger_schema_hash=_slice6_policy_hash("SPREAD_COST_LEDGER_SCHEMA"),
        cost_ledger_schema_hash=_slice6_policy_hash("COST_LEDGER_SCHEMA"),
        cost_source_binding_hash="0" * 64,
    )
    source_binding = CostSourceBinding(
        **{
            **asdict(source_binding),
            "cost_source_binding_hash": canonical_sha256(_cost_source_binding_hash_payload(source_binding)),
        }
    )
    dependency_hash_by_label = _cost_input_hash_by_label(cost_input_contract)
    component_contract_by_family: dict[str, CostComponentContract] = {}

    def ensure_component_contract(component: str) -> CostComponentContract:
        if component in component_contract_by_family:
            return component_contract_by_family[component]
        for dependency_label in REQUIRED_COST_DEPENDENCIES_BY_COMPONENT[component]:
            if dependency_label in REQUIRED_COST_COMPONENT_FAMILIES and dependency_label not in dependency_hash_by_label:
                ensure_component_contract(dependency_label)
        contract = _build_cost_component_contract(component, dependency_hash_by_label)
        component_contract_by_family[component] = contract
        dependency_hash_by_label[contract.component_family] = contract.component_contract_hash
        return contract

    for component in REQUIRED_COST_COMPONENT_FAMILIES:
        ensure_component_contract(component)
    component_contracts = tuple(
        component_contract_by_family[component] for component in REQUIRED_COST_COMPONENT_FAMILIES
    )
    branch_contracts = tuple(
        _build_cost_branch_contract(branch, dependency_hash_by_label)
        for branch in REQUIRED_COST_BRANCH_LABELS
    )
    for branch in branch_contracts:
        dependency_hash_by_label[branch.branch_label] = branch.branch_contract_hash
    spread_space_contracts = tuple(
        _build_spread_space_contract(spread_space, replay_trust_root.spread_unit_policy_hash)
        for spread_space in REQUIRED_SPREAD_SPACE_LABELS
    )
    invariant_contracts = tuple(
        _build_cost_invariant_contract(invariant, dependency_hash_by_label)
        for invariant in REQUIRED_COST_INVARIANTS
    )
    contract = CostContractBundle(
        status=S27_V2_COST_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        component_contracts=component_contracts,
        branch_contracts=branch_contracts,
        spread_space_contracts=spread_space_contracts,
        invariant_contracts=invariant_contracts,
        commission_policy_hash=replay_trust_root.commission_policy_hash,
        spread_policy_hash=replay_trust_root.spread_unit_policy_hash,
        cost_calculation_policy_hash=cost_input_contract.cost_input_policy_hash,
        contract_multiplier_policy_hash=replay_trust_root.contract_multiplier_currency_policy_hash,
        currency_conversion_policy_hash=replay_trust_root.contract_multiplier_currency_policy_hash,
        deflation_policy_hash=cost_input_contract.cost_input_policy_hash,
        cost_contract_bundle_hash="0" * 64,
    )
    contract = CostContractBundle(
        **{
            **asdict(contract),
            "source_binding": source_binding,
            "component_contracts": component_contracts,
            "branch_contracts": branch_contracts,
            "spread_space_contracts": spread_space_contracts,
            "invariant_contracts": invariant_contracts,
            "cost_contract_bundle_hash": canonical_sha256(_cost_contract_bundle_hash_payload(contract)),
        }
    )
    _validate_cost_contract_content_bound(
        contract,
        cost_input_contract,
        slice5_artifacts,
        replay_trust_root,
        evidence_manifest,
    )
    return contract


def build_pnl_input_contract(
    slice6_artifacts: LocalParserFileReplaySlice6Artifacts,
) -> PnlInputContractBundle:
    slice6_artifacts.validate()
    policy_hash = _slice7_policy_hash("PNL_INPUT")
    active_source_hash_by_label = _pnl_active_source_hash_by_label(
        policy_hash,
        slice6_artifacts,
    )
    input_fields = tuple(
        _build_pnl_input_field_contract(
            input_label,
            active_source_hash_by_label[input_label],
            policy_hash,
        )
        for input_label in REQUIRED_PNL_INPUTS
    )
    dependency_hash_by_label = {field.input_label: field.input_field_contract_hash for field in input_fields}
    component_bindings_list: list[PnlDependencyBindingContract] = []
    for component in REQUIRED_PNL_COMPONENT_FAMILIES:
        binding = _build_pnl_dependency_binding_contract(
            component,
            REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT[component],
            dependency_hash_by_label,
            "COMPONENT",
        )
        component_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    component_bindings = tuple(component_bindings_list)
    invariant_bindings = tuple(
        _build_pnl_dependency_binding_contract(
            invariant,
            REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT[invariant],
            dependency_hash_by_label,
            "INVARIANT",
        )
        for invariant in REQUIRED_PNL_INVARIANTS
    )
    source_manifest = (
        slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_PNL_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in component_bindings
            ),
            "cost_contract_bundle_hash": slice6_artifacts.cost_contract.cost_contract_bundle_hash,
            "cost_input_contract_hash": slice6_artifacts.cost_input_contract.cost_input_contract_hash,
            "input_field_contract_hashes": tuple(field.input_field_contract_hash for field in input_fields),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in invariant_bindings
            ),
            "source_input_manifest_contract_hash": source_manifest.source_input_manifest_contract_hash,
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_PNL_INPUT_CONTRACT",
            "cost_contract_bundle_hash": slice6_artifacts.cost_contract.cost_contract_bundle_hash,
            "cost_input_contract_hash": slice6_artifacts.cost_input_contract.cost_input_contract_hash,
            "pnl_input_policy_hash": policy_hash,
            "pnl_input_set_hash": input_set_hash,
            "source_input_manifest_contract_hash": source_manifest.source_input_manifest_contract_hash,
        }
    )
    contract = PnlInputContractBundle(
        status=S27_V2_PNL_INPUT_CONTRACT_ONLY_STATUS,
        replay_trust_root_hash=slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        source_universe_hash=(
            slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts
            .source_row_selection_external_authority.source_universe_contract_bundle_hash
        ),
        previous_step_or_initial_state_hash=(
            slice6_artifacts.slice5_artifacts.slice4_artifacts.order_contract.order_contract_bundle_hash
        ),
        starting_working_state_hash=slice6_artifacts.slice5_artifacts.slice4_artifacts.order_contract.order_contract_bundle_hash,
        transition_hash=slice6_artifacts.slice5_artifacts.slice4_artifacts.order_contract.order_contract_bundle_hash,
        ending_working_state_hash=slice6_artifacts.slice5_artifacts.slice4_artifacts.order_contract.order_contract_bundle_hash,
        starting_position_hash=slice6_artifacts.slice5_artifacts.slice4_artifacts.order_contract.order_contract_bundle_hash,
        ending_position_hash=slice6_artifacts.slice5_artifacts.slice4_artifacts.order_contract.order_contract_bundle_hash,
        position_source_hash=(
            slice6_artifacts.slice5_artifacts.slice4_artifacts.position_contract.desired_position_contract_bundle_hash
        ),
        close_only_price_source_policy_hash=policy_hash,
        start_price_source_row_hash=source_manifest.expected_selected_row_hash_by_manifest_field[
            PNL_PRICE_ROW_MANIFEST_FIELD
        ],
        end_price_source_row_hash=source_manifest.expected_selected_row_hash_by_manifest_field[
            PNL_PRICE_ROW_MANIFEST_FIELD
        ],
        raw_symbol_continuity_proof_hash=source_manifest.source_input_manifest_hash,
        roll_bridge_proof_hash=source_manifest.source_input_manifest_hash,
        contract_multiplier_proof_hash=(
            slice6_artifacts.replay_trust_root.contract_multiplier_currency_policy_hash
        ),
        currency_policy_proof_hash=slice6_artifacts.replay_trust_root.contract_multiplier_currency_policy_hash,
        fill_hash_set_hash=slice6_artifacts.slice5_artifacts.fill_contract.fill_contract_bundle_hash,
        cost_hash_set_hash=slice6_artifacts.cost_contract.cost_contract_bundle_hash,
        source_input_manifest_contract_hash=source_manifest.source_input_manifest_contract_hash,
        cost_input_contract_hash=slice6_artifacts.cost_input_contract.cost_input_contract_hash,
        cost_contract_bundle_hash=slice6_artifacts.cost_contract.cost_contract_bundle_hash,
        pnl_input_policy_hash=policy_hash,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label=active_source_hash_by_label,
        component_dependency_bindings=component_bindings,
        invariant_dependency_bindings=invariant_bindings,
        pnl_input_set_hash=input_set_hash,
        pnl_input_contract_hash=contract_hash,
    )
    _validate_pnl_input_contract_local_only(contract, slice6_artifacts)
    return contract


def build_pnl_contract(
    slice6_artifacts: LocalParserFileReplaySlice6Artifacts,
    pnl_input_contract: PnlInputContractBundle,
) -> PnlContractBundle:
    slice6_artifacts.validate()
    _validate_pnl_input_contract_local_only(pnl_input_contract, slice6_artifacts)
    source_manifest = (
        slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    source_binding = PnlSourceBinding(
        replay_trust_root_hash=slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        source_input_manifest_hash=source_manifest.source_input_manifest_hash,
        transition_ledger_schema_hash=(
            slice6_artifacts.slice5_artifacts.slice4_artifacts.order_contract.source_binding
            .working_order_transition_schema_hash
        ),
        fill_ledger_schema_hash=slice6_artifacts.slice5_artifacts.fill_contract.source_binding.fill_ledger_schema_hash,
        cost_ledger_schema_hash=slice6_artifacts.cost_contract.source_binding.cost_ledger_schema_hash,
        pnl_ledger_schema_hash=_slice7_policy_hash("PNL_LEDGER_SCHEMA"),
        pnl_source_binding_hash="0" * 64,
    )
    source_binding = PnlSourceBinding(
        **{
            **asdict(source_binding),
            "pnl_source_binding_hash": canonical_sha256(_pnl_source_binding_hash_payload(source_binding)),
        }
    )
    dependency_hash_by_label = _pnl_input_hash_by_label(pnl_input_contract)
    component_contracts_list: list[PnlComponentContract] = []
    for component in REQUIRED_PNL_COMPONENT_FAMILIES:
        contract = _build_pnl_component_contract(component, dependency_hash_by_label)
        component_contracts_list.append(contract)
        dependency_hash_by_label[contract.component_family] = contract.component_contract_hash
    component_contracts = tuple(component_contracts_list)
    price_source_contracts = tuple(
        _build_pnl_price_source_contract(price_source, pnl_input_contract.pnl_input_policy_hash)
        for price_source in REQUIRED_PNL_PRICE_SOURCE_LABELS
    )
    bridge_contracts = tuple(
        _build_pnl_bridge_contract(bridge, dependency_hash_by_label)
        for bridge in REQUIRED_PNL_BRIDGE_LABELS
    )
    for bridge in bridge_contracts:
        dependency_hash_by_label[bridge.bridge_label] = bridge.bridge_contract_hash
    invariant_contracts = tuple(
        _build_pnl_invariant_contract(invariant, dependency_hash_by_label)
        for invariant in REQUIRED_PNL_INVARIANTS
    )
    contract = PnlContractBundle(
        status=S27_V2_PNL_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        component_contracts=component_contracts,
        price_source_contracts=price_source_contracts,
        bridge_contracts=bridge_contracts,
        invariant_contracts=invariant_contracts,
        pnl_formula_policy_hash=pnl_input_contract.pnl_input_policy_hash,
        close_price_source_policy_hash=pnl_input_contract.pnl_input_policy_hash,
        cost_application_policy_hash=pnl_input_contract.pnl_input_policy_hash,
        contract_multiplier_policy_hash=slice6_artifacts.replay_trust_root.contract_multiplier_currency_policy_hash,
        currency_policy_hash=slice6_artifacts.replay_trust_root.contract_multiplier_currency_policy_hash,
        target_position_shortcut_quarantine_policy_hash=pnl_input_contract.pnl_input_policy_hash,
        pnl_contract_bundle_hash="0" * 64,
    )
    contract = PnlContractBundle(
        **{
            **asdict(contract),
            "source_binding": source_binding,
            "component_contracts": component_contracts,
            "price_source_contracts": price_source_contracts,
            "bridge_contracts": bridge_contracts,
            "invariant_contracts": invariant_contracts,
            "pnl_contract_bundle_hash": canonical_sha256(_pnl_contract_bundle_hash_payload(contract)),
        }
    )
    _validate_pnl_contract_content_bound(contract, pnl_input_contract, slice6_artifacts)
    return contract


def build_local_only_construction_contract(
    inputs: LocalParserFileReplaySlice1Inputs,
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
) -> ParserFileReplayConstructionContract:
    inputs.validate()
    slice7_artifacts.validate()
    planned_hash_by_family = _planned_artifact_hash_by_family(slice7_artifacts)
    gate_index = 0
    phase_contracts: list[ConstructionPhaseBoundary] = []
    for index, phase_label in enumerate(PLANNED_CONSTRUCTION_PHASES, start=1):
        gate_count = 2 if index in (1, 2) else 1
        blocked_gates = REQUIRED_UNRESOLVED_GATE_LABELS[gate_index : gate_index + gate_count]
        gate_index += gate_count
        artifacts = tuple(
            ConstructionArtifactReference(
                artifact_family=artifact_family,
                schema_family=f"{artifact_family}_SCHEMA",
                artifact_hash=planned_hash_by_family[artifact_family],
                producer_phase_label=phase_label,
                status_label="PLANNED_STRUCTURAL_ARTIFACT_ONLY",
            )
            for artifact_family in REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE[phase_label]
        )
        phase = ConstructionPhaseBoundary(
            phase_index=index,
            phase_label=phase_label,
            required_input_hashes=(
                inputs.input_directory.input_directory_declaration_hash,
                inputs.parser_plan_bundle.parser_plan_bundle_hash,
                slice7_artifacts.pnl_contract.pnl_contract_bundle_hash,
            ),
            planned_output_artifacts=artifacts,
            blocked_gate_statuses=blocked_gates,
            phase_contract_hash="0" * 64,
        )
        phase = ConstructionPhaseBoundary(
            **{
                **asdict(phase),
                "planned_output_artifacts": artifacts,
                "phase_contract_hash": canonical_sha256(_construction_phase_hash_payload(phase)),
            }
        )
        phase.validate()
        phase_contracts.append(phase)
    if gate_index != len(REQUIRED_UNRESOLVED_GATE_LABELS):
        raise CarverBlocked("S27 v2 construction gate assignment must cover locked gates")
    contract = ParserFileReplayConstructionContract(
        status=S27_V2_CONSTRUCTION_SCAFFOLD_ONLY_STATUS,
        planning_config_hash=_local_only_trust_hash("PLANNING_CONFIG"),
        parser_plan_bundle_hash=inputs.parser_plan_bundle.parser_plan_bundle_hash,
        input_directory_declaration_hash=inputs.input_directory.input_directory_declaration_hash,
        artifact_manifest_plan_hash=_local_only_trust_hash("ARTIFACT_MANIFEST_PLAN"),
        construction_phases=tuple(phase_contracts),
        construction_contract_hash="0" * 64,
    )
    contract = ParserFileReplayConstructionContract(
        **{
            **asdict(contract),
            "construction_phases": tuple(phase_contracts),
            "construction_contract_hash": canonical_sha256(_construction_contract_hash_payload(contract)),
        }
    )
    _validate_construction_contract_local_only(contract, slice7_artifacts)
    return contract


def build_validation_contract(
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
) -> ValidationContractBundle:
    slice7_artifacts.validate()
    source_manifest = (
        slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts
        .source_input_manifest_contract
    )
    source_binding = ValidationSourceBinding(
        replay_trust_root_hash=slice7_artifacts.slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        active_evidence_manifest_hash=slice7_artifacts.slice6_artifacts.evidence_manifest.active_evidence_manifest_hash,
        source_input_manifest_hash=source_manifest.source_input_manifest_hash,
        pnl_contract_bundle_hash=slice7_artifacts.pnl_contract.pnl_contract_bundle_hash,
        validation_ledger_schema_hash=_slice8_policy_hash("VALIDATION_LEDGER_SCHEMA"),
        provenance_and_hash_ledger_schema_hash=_slice8_policy_hash("PROVENANCE_AND_HASH_LEDGER_SCHEMA"),
        local_hostile_audit_result_schema_hash=_slice8_policy_hash("LOCAL_HOSTILE_AUDIT_RESULT_SCHEMA"),
        validation_source_binding_hash="0" * 64,
    )
    source_binding = ValidationSourceBinding(
        **{
            **asdict(source_binding),
            "validation_source_binding_hash": canonical_sha256(_validation_source_binding_hash_payload(source_binding)),
        }
    )
    dependency_hash_by_label = _validation_base_input_hash_by_label(slice7_artifacts, source_binding)
    component_contracts_list: list[ValidationComponentContract] = []
    for component in REQUIRED_VALIDATION_COMPONENT_FAMILIES:
        contract = _build_validation_component_contract(component, dependency_hash_by_label)
        component_contracts_list.append(contract)
        dependency_hash_by_label[contract.component_family] = contract.component_contract_hash
    component_contracts = tuple(component_contracts_list)
    ledger_contracts_list: list[ValidationLedgerContract] = []
    for ledger in REQUIRED_VALIDATION_LEDGER_LABELS:
        contract = _build_validation_ledger_contract(ledger, dependency_hash_by_label, source_binding)
        ledger_contracts_list.append(contract)
        dependency_hash_by_label[contract.ledger_label] = contract.ledger_contract_hash
    ledger_contracts = tuple(ledger_contracts_list)
    audit_checkpoint_contracts_list: list[ValidationAuditCheckpointContract] = []
    for checkpoint in REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS:
        contract = _build_validation_audit_checkpoint_contract(checkpoint, dependency_hash_by_label)
        audit_checkpoint_contracts_list.append(contract)
        dependency_hash_by_label[contract.checkpoint_label] = contract.audit_checkpoint_contract_hash
    audit_checkpoint_contracts = tuple(audit_checkpoint_contracts_list)
    invariant_contracts = tuple(
        _build_validation_invariant_contract(invariant, dependency_hash_by_label)
        for invariant in REQUIRED_VALIDATION_INVARIANTS
    )
    contract = ValidationContractBundle(
        status=S27_V2_VALIDATION_CONTRACT_ONLY_STATUS,
        source_binding=source_binding,
        component_contracts=component_contracts,
        ledger_contracts=ledger_contracts,
        audit_checkpoint_contracts=audit_checkpoint_contracts,
        invariant_contracts=invariant_contracts,
        required_unresolved_gate_labels=REQUIRED_UNRESOLVED_GATE_LABELS,
        required_artifact_family_policy_hash=_slice8_policy_hash("REQUIRED_ARTIFACT_FAMILY_POLICY"),
        provenance_hash_chain_policy_hash=_slice8_policy_hash("PROVENANCE_HASH_CHAIN_POLICY"),
        fail_closed_gate_policy_hash=_slice8_policy_hash("FAIL_CLOSED_GATE_POLICY"),
        stale_evidence_supersession_policy_hash=_slice8_policy_hash("STALE_EVIDENCE_SUPERSESSION_POLICY"),
        local_hostile_audit_policy_hash=_slice8_policy_hash("LOCAL_HOSTILE_AUDIT_POLICY"),
        external_audit_packet_policy_hash=_slice8_policy_hash("EXTERNAL_AUDIT_PACKET_POLICY"),
        validation_contract_bundle_hash="0" * 64,
    )
    contract = ValidationContractBundle(
        **{
            **asdict(contract),
            "source_binding": source_binding,
            "component_contracts": component_contracts,
            "ledger_contracts": ledger_contracts,
            "audit_checkpoint_contracts": audit_checkpoint_contracts,
            "invariant_contracts": invariant_contracts,
            "validation_contract_bundle_hash": canonical_sha256(_validation_contract_bundle_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def build_validation_input_contract(
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
    validation_contract: ValidationContractBundle,
) -> ValidationInputContractBundle:
    slice7_artifacts.validate()
    validation_contract.validate()
    policy_hash = _slice8_policy_hash("VALIDATION_INPUT")
    active_source_hash_by_label = _validation_active_source_hash_by_label(
        policy_hash,
        slice7_artifacts,
        validation_contract,
    )
    input_fields = tuple(
        _build_validation_input_field_contract(
            input_label,
            active_source_hash_by_label[input_label],
            policy_hash,
        )
        for input_label in REQUIRED_VALIDATION_INPUTS
    )
    dependency_hash_by_label = {field.input_label: field.input_field_contract_hash for field in input_fields}
    component_bindings_list: list[ValidationDependencyBindingContract] = []
    for component in REQUIRED_VALIDATION_COMPONENT_FAMILIES:
        binding = _build_validation_dependency_binding_contract(
            component,
            REQUIRED_VALIDATION_DEPENDENCIES_BY_COMPONENT[component],
            dependency_hash_by_label,
            "COMPONENT",
        )
        component_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    component_bindings = tuple(component_bindings_list)
    ledger_bindings_list: list[ValidationDependencyBindingContract] = []
    for ledger in REQUIRED_VALIDATION_LEDGER_LABELS:
        binding = _build_validation_dependency_binding_contract(
            ledger,
            REQUIRED_VALIDATION_DEPENDENCIES_BY_LEDGER[ledger],
            dependency_hash_by_label,
            "LEDGER",
        )
        ledger_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    ledger_bindings = tuple(ledger_bindings_list)
    audit_bindings_list: list[ValidationDependencyBindingContract] = []
    for checkpoint in REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS:
        binding = _build_validation_dependency_binding_contract(
            checkpoint,
            REQUIRED_VALIDATION_DEPENDENCIES_BY_AUDIT_CHECKPOINT[checkpoint],
            dependency_hash_by_label,
            "AUDIT",
        )
        audit_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    audit_bindings = tuple(audit_bindings_list)
    invariant_bindings = tuple(
        _build_validation_dependency_binding_contract(
            invariant,
            REQUIRED_VALIDATION_DEPENDENCIES_BY_INVARIANT[invariant],
            dependency_hash_by_label,
            "INVARIANT",
        )
        for invariant in REQUIRED_VALIDATION_INVARIANTS
    )
    source_manifest = (
        slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts
        .source_input_manifest_contract
    )
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_VALIDATION_INPUT_SET",
            "audit_checkpoint_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in audit_bindings
            ),
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in component_bindings
            ),
            "input_field_contract_hashes": tuple(field.input_field_contract_hash for field in input_fields),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in invariant_bindings
            ),
            "ledger_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in ledger_bindings
            ),
            "pnl_contract_bundle_hash": slice7_artifacts.pnl_contract.pnl_contract_bundle_hash,
            "pnl_input_contract_hash": slice7_artifacts.pnl_input_contract.pnl_input_contract_hash,
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_VALIDATION_INPUT_CONTRACT",
            "pnl_contract_bundle_hash": slice7_artifacts.pnl_contract.pnl_contract_bundle_hash,
            "pnl_input_contract_hash": slice7_artifacts.pnl_input_contract.pnl_input_contract_hash,
            "validation_input_policy_hash": policy_hash,
            "validation_input_set_hash": input_set_hash,
        }
    )
    contract = ValidationInputContractBundle(
        status=S27_V2_VALIDATION_INPUT_CONTRACT_ONLY_STATUS,
        replay_trust_root_hash=slice7_artifacts.slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        active_evidence_manifest_hash=slice7_artifacts.slice6_artifacts.evidence_manifest.active_evidence_manifest_hash,
        source_input_manifest_hash=source_manifest.source_input_manifest_hash,
        source_input_manifest_contract_hash=source_manifest.source_input_manifest_contract_hash,
        pnl_input_contract_hash=slice7_artifacts.pnl_input_contract.pnl_input_contract_hash,
        pnl_contract_bundle_hash=slice7_artifacts.pnl_contract.pnl_contract_bundle_hash,
        validation_contract_bundle_hash=validation_contract.validation_contract_bundle_hash,
        validation_ledger_schema_hash=validation_contract.source_binding.validation_ledger_schema_hash,
        provenance_ledger_schema_hash=validation_contract.source_binding.provenance_and_hash_ledger_schema_hash,
        local_hostile_audit_schema_hash=validation_contract.source_binding.local_hostile_audit_result_schema_hash,
        validation_input_policy_hash=policy_hash,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label=active_source_hash_by_label,
        component_dependency_bindings=component_bindings,
        ledger_dependency_bindings=ledger_bindings,
        audit_checkpoint_dependency_bindings=audit_bindings,
        invariant_dependency_bindings=invariant_bindings,
        validation_input_set_hash=input_set_hash,
        validation_input_contract_hash=contract_hash,
    )
    _validate_validation_input_contract_local_only(contract, slice7_artifacts, validation_contract)
    return contract


def build_trusted_bundle_contract(
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
    construction_contract: ParserFileReplayConstructionContract,
    validation_input_contract: ValidationInputContractBundle,
    validation_contract: ValidationContractBundle,
) -> TrustedBundleContractBundle:
    slice7_artifacts.validate()
    construction_contract.validate()
    _validate_validation_input_contract_local_only(validation_input_contract, slice7_artifacts, validation_contract)
    _validate_validation_contract_content_bound(validation_contract, validation_input_contract, slice7_artifacts)
    policy_hash = _slice8_policy_hash("TRUSTED_BUNDLE")
    validation_ledger_hash = _validation_planned_ledger_hash(validation_contract, "VALIDATION_LEDGER")
    provenance_ledger_hash = _validation_planned_ledger_hash(validation_contract, "PROVENANCE_AND_HASH_LEDGER")
    local_audit_hash = _validation_planned_ledger_hash(validation_contract, "LOCAL_HOSTILE_AUDIT_RESULT")
    active_source_hash_by_label = _trusted_bundle_active_source_hash_by_label(
        policy_hash,
        slice7_artifacts,
        construction_contract,
        validation_input_contract,
        validation_contract,
        validation_ledger_hash,
        provenance_ledger_hash,
        local_audit_hash,
    )
    input_fields = tuple(
        _build_trusted_bundle_input_field_contract(
            input_label,
            active_source_hash_by_label[input_label],
            policy_hash,
        )
        for input_label in REQUIRED_TRUSTED_BUNDLE_INPUTS
    )
    dependency_hash_by_label = {field.input_label: field.input_field_contract_hash for field in input_fields}
    component_bindings_list: list[TrustedBundleDependencyBindingContract] = []
    for component in REQUIRED_TRUSTED_BUNDLE_COMPONENTS:
        binding = _build_trusted_bundle_dependency_binding_contract(
            component,
            REQUIRED_BUNDLE_DEPENDENCIES_BY_COMPONENT[component],
            dependency_hash_by_label,
            "COMPONENT",
        )
        component_bindings_list.append(binding)
        dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash
    component_bindings = tuple(component_bindings_list)
    invariant_bindings = tuple(
        _build_trusted_bundle_dependency_binding_contract(
            invariant,
            REQUIRED_BUNDLE_DEPENDENCIES_BY_INVARIANT[invariant],
            dependency_hash_by_label,
            "INVARIANT",
        )
        for invariant in REQUIRED_TRUSTED_BUNDLE_INVARIANTS
    )
    input_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_TRUSTED_BUNDLE_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in component_bindings
            ),
            "input_field_contract_hashes": tuple(field.input_field_contract_hash for field in input_fields),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in invariant_bindings
            ),
        }
    )
    contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_TRUSTED_BUNDLE_CONTRACT",
            "trusted_bundle_input_set_hash": input_set_hash,
            "trusted_bundle_policy_hash": policy_hash,
        }
    )
    contract = TrustedBundleContractBundle(
        status=S27_V2_TRUSTED_BUNDLE_CONTRACT_ONLY_STATUS,
        replay_trust_root_hash=slice7_artifacts.slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        active_evidence_manifest_hash=slice7_artifacts.slice6_artifacts.evidence_manifest.active_evidence_manifest_hash,
        construction_contract_hash=construction_contract.construction_contract_hash,
        validation_input_contract_hash=validation_input_contract.validation_input_contract_hash,
        validation_contract_bundle_hash=validation_contract.validation_contract_bundle_hash,
        validation_ledger_hash=validation_ledger_hash,
        provenance_ledger_hash=provenance_ledger_hash,
        local_hostile_audit_result_hash=local_audit_hash,
        trusted_bundle_policy_hash=policy_hash,
        input_field_contracts=input_fields,
        expected_source_contract_hash_by_input_label=active_source_hash_by_label,
        component_dependency_bindings=component_bindings,
        invariant_dependency_bindings=invariant_bindings,
        trusted_bundle_input_set_hash=input_set_hash,
        trusted_bundle_contract_hash=contract_hash,
    )
    _validate_trusted_bundle_contract_content_bound(
        contract,
        construction_contract,
        validation_input_contract,
        validation_contract,
        slice7_artifacts,
    )
    return contract


def _slice5_policy_hash(label: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_LOCAL_ONLY_SLICE5_POLICY",
            "label": label,
            "scope": "FILL_CONSTRUCTION_SCAFFOLD_ONLY",
        }
    )


def _slice6_policy_hash(label: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_LOCAL_ONLY_SLICE6_POLICY",
            "label": label,
            "scope": "COST_CONSTRUCTION_SCAFFOLD_ONLY",
        }
    )


def _slice7_policy_hash(label: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_LOCAL_ONLY_SLICE7_POLICY",
            "label": label,
            "scope": "PNL_CONSTRUCTION_SCAFFOLD_ONLY",
        }
    )


def _slice8_policy_hash(label: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_LOCAL_ONLY_COMPLETION_POLICY",
            "label": label,
            "scope": "VALIDATION_PROVENANCE_TRUSTED_BUNDLE_SCAFFOLD_ONLY",
        }
    )


def _local_only_trust_hash(label: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_LOCAL_ONLY_TRUST_PLACEHOLDER",
            "label": label,
            "restriction": "LOCAL_ONLY_CONSTRUCTION_SCAFFOLD_NOT_SOURCE_EVIDENCE",
        }
    )


def _cost_active_source_hash_by_label(
    cost_input_policy_hash: str,
    replay_trust_root: ReplayTrustRoot,
    fill_contract: FillContractBundle,
) -> dict[str, str]:
    active_hash_by_label: dict[str, str] = {}
    for input_label in REQUIRED_COST_INPUTS:
        source_kind = REQUIRED_SOURCE_KIND_BY_COST_INPUT[input_label]
        if source_kind == "FILL_LEDGER_OUTPUT":
            active_hash_by_label[input_label] = fill_contract.fill_contract_bundle_hash
        elif source_kind == "COST_BRANCH":
            active_hash_by_label[input_label] = cost_input_policy_hash
        elif source_kind == "SPREAD_SPACE":
            active_hash_by_label[input_label] = replay_trust_root.spread_unit_policy_hash
        elif source_kind == "POLICY_INPUT":
            active_hash_by_label[input_label] = _cost_active_policy_hash_for_input(
                replay_trust_root,
                cost_input_policy_hash,
                input_label,
            )
        elif source_kind in {"MULTIPLIER_PROOF_INPUT", "CURRENCY_PROOF_INPUT"}:
            active_hash_by_label[input_label] = replay_trust_root.contract_multiplier_currency_policy_hash
        else:
            raise CarverBlocked("S27 v2 cost source kind cannot be authority-bound")
    return active_hash_by_label


def _cost_active_policy_hash_for_input(
    replay_trust_root: ReplayTrustRoot,
    cost_input_policy_hash: str,
    input_label: str,
) -> str:
    if input_label == "COST_COMMISSION_POLICY_INPUT":
        return replay_trust_root.commission_policy_hash
    if input_label == "COST_SPREAD_POLICY_INPUT":
        return replay_trust_root.spread_unit_policy_hash
    if input_label in {"COST_DEFLATION_POLICY_INPUT", "COST_CALCULATION_POLICY_INPUT"}:
        return cost_input_policy_hash
    raise CarverBlocked("S27 v2 cost policy input cannot be authority-bound")


def _pnl_active_source_hash_by_label(
    pnl_input_policy_hash: str,
    slice6_artifacts: LocalParserFileReplaySlice6Artifacts,
) -> dict[str, str]:
    source_manifest = (
        slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    order_contract = slice6_artifacts.slice5_artifacts.slice4_artifacts.order_contract
    position_contract = slice6_artifacts.slice5_artifacts.slice4_artifacts.position_contract
    external_authority = (
        slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts
        .source_row_selection_external_authority
    )
    return {
        "PNL_TRUST_ROOT_HASH_INPUT": slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        "PNL_SOURCE_UNIVERSE_HASH_INPUT": external_authority.source_universe_contract_bundle_hash,
        "PNL_PREVIOUS_STEP_OR_INITIAL_STATE_HASH_INPUT": order_contract.order_contract_bundle_hash,
        "PNL_STARTING_WORKING_STATE_HASH_INPUT": order_contract.order_contract_bundle_hash,
        "PNL_TRANSITION_HASH_INPUT": order_contract.order_contract_bundle_hash,
        "PNL_ENDING_WORKING_STATE_HASH_INPUT": order_contract.order_contract_bundle_hash,
        "PNL_STARTING_POSITION_INPUT": order_contract.order_contract_bundle_hash,
        "PNL_ENDING_POSITION_INPUT": order_contract.order_contract_bundle_hash,
        "PNL_POSITION_SOURCE_HASH_INPUT": position_contract.desired_position_contract_bundle_hash,
        "PNL_CLOSE_ONLY_PRICE_SOURCE_INPUT": pnl_input_policy_hash,
        "PNL_START_PRICE_ROW_HASH_INPUT": source_manifest.expected_selected_row_hash_by_manifest_field[
            PNL_PRICE_ROW_MANIFEST_FIELD
        ],
        "PNL_END_PRICE_ROW_HASH_INPUT": source_manifest.expected_selected_row_hash_by_manifest_field[
            PNL_PRICE_ROW_MANIFEST_FIELD
        ],
        "PNL_RAW_SYMBOL_CONTINUITY_INPUT": source_manifest.source_input_manifest_hash,
        "PNL_ROLL_BRIDGE_INPUT": source_manifest.source_input_manifest_hash,
        "PNL_CONTRACT_MULTIPLIER_POLICY_INPUT": (
            slice6_artifacts.replay_trust_root.contract_multiplier_currency_policy_hash
        ),
        "PNL_CURRENCY_POLICY_INPUT": slice6_artifacts.replay_trust_root.contract_multiplier_currency_policy_hash,
        "PNL_FILL_HASH_SET_INPUT": slice6_artifacts.slice5_artifacts.fill_contract.fill_contract_bundle_hash,
        "PNL_COST_HASH_SET_INPUT": slice6_artifacts.cost_contract.cost_contract_bundle_hash,
        "PNL_FORMULA_POLICY_INPUT": pnl_input_policy_hash,
        "PNL_COST_APPLICATION_POLICY_INPUT": pnl_input_policy_hash,
        "PNL_TARGET_POSITION_SHORTCUT_QUARANTINE_INPUT": pnl_input_policy_hash,
    }


def _planned_artifact_hash_by_family(
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
) -> dict[str, str]:
    slice6 = slice7_artifacts.slice6_artifacts
    slice5 = slice6.slice5_artifacts
    slice4 = slice5.slice4_artifacts
    slice3 = slice4.slice3_artifacts
    slice2 = slice3.slice2_artifacts
    return {
        "SOURCE_INPUT_MANIFEST": slice2.source_input_manifest_contract.source_input_manifest_hash,
        "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER": (
            slice3.level_compatibility_contract.level_compatibility_contract_bundle_hash
        ),
        "RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM": (
            slice3.runtime_history_contract.runtime_history_contract_bundle_hash
        ),
        "FORECAST_REPLAY_LEDGER": slice4.forecast_contract.forecast_contract_bundle_hash,
        "DESIRED_POSITION_LEDGER": slice4.position_contract.desired_position_contract_bundle_hash,
        "LIMIT_ORDER_LEDGER": slice4.order_contract.order_contract_bundle_hash,
        "MARKET_ORDER_LEDGER": slice4.order_contract.order_contract_bundle_hash,
        "WORKING_ORDER_TRANSITION_LEDGER": slice4.order_contract.order_contract_bundle_hash,
        "REMAINING_LIMIT_ORDER_LEDGER": slice4.order_contract.order_contract_bundle_hash,
        "CANCELED_LIMIT_ORDER_LEDGER": slice4.order_contract.order_contract_bundle_hash,
        "FILL_LEDGER": slice5.fill_contract.fill_contract_bundle_hash,
        "COMMISSION_LEDGER": slice6.cost_contract.cost_contract_bundle_hash,
        "SPREAD_COST_LEDGER": slice6.cost_contract.cost_contract_bundle_hash,
        "PNL_LEDGER": slice7_artifacts.pnl_contract.pnl_contract_bundle_hash,
        "VALIDATION_LEDGER": _slice8_policy_hash("VALIDATION_LEDGER_OUTPUT"),
        "PROVENANCE_AND_HASH_LEDGER": _slice8_policy_hash("PROVENANCE_AND_HASH_LEDGER_OUTPUT"),
        "LOCAL_HOSTILE_AUDIT_RESULT": _slice8_policy_hash("LOCAL_HOSTILE_AUDIT_RESULT_OUTPUT"),
    }


def _validation_planned_ledger_hash(
    validation_contract: ValidationContractBundle,
    ledger_label: str,
) -> str:
    matches = [
        ledger.planned_ledger_output_hash
        for ledger in validation_contract.ledger_contracts
        if ledger.ledger_label == ledger_label
    ]
    if len(matches) != 1:
        raise CarverBlocked("S27 v2 validation planned ledger hash lookup must be unique")
    return matches[0]


def _validation_base_input_hash_by_label(
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
    source_binding: ValidationSourceBinding,
) -> dict[str, str]:
    source_manifest = (
        slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts
        .source_input_manifest_contract
    )
    policy_hash = _slice8_policy_hash("VALIDATION_INPUT")
    return {
        "VALIDATION_TRUST_ROOT_HASH_INPUT": slice7_artifacts.slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        "VALIDATION_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": (
            slice7_artifacts.slice6_artifacts.evidence_manifest.active_evidence_manifest_hash
        ),
        "VALIDATION_SOURCE_INPUT_MANIFEST_HASH_INPUT": source_manifest.source_input_manifest_hash,
        "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT": slice7_artifacts.pnl_contract.pnl_contract_bundle_hash,
        "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT": slice7_artifacts.pnl_input_contract.pnl_input_contract_hash,
        "VALIDATION_LEDGER_SCHEMA_HASH_INPUT": source_binding.validation_ledger_schema_hash,
        "VALIDATION_PROVENANCE_LEDGER_SCHEMA_HASH_INPUT": source_binding.provenance_and_hash_ledger_schema_hash,
        "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT": source_binding.local_hostile_audit_result_schema_hash,
        "VALIDATION_REQUIRED_ARTIFACT_FAMILY_POLICY_INPUT": policy_hash,
        "VALIDATION_PROVENANCE_HASH_CHAIN_POLICY_INPUT": policy_hash,
        "VALIDATION_FAIL_CLOSED_GATE_POLICY_INPUT": policy_hash,
        "VALIDATION_STALE_EVIDENCE_SUPERSESSION_POLICY_INPUT": policy_hash,
        "VALIDATION_LOCAL_HOSTILE_AUDIT_POLICY_INPUT": policy_hash,
        "VALIDATION_EXTERNAL_AUDIT_PACKET_POLICY_INPUT": policy_hash,
        "VALIDATION_UNRESOLVED_GATE_SET_INPUT": policy_hash,
        "VALIDATION_NO_EXECUTION_POLICY_INPUT": policy_hash,
        "VALIDATION_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT": policy_hash,
    }


def _validation_active_source_hash_by_label(
    validation_input_policy_hash: str,
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
    validation_contract: ValidationContractBundle,
) -> dict[str, str]:
    source_manifest = (
        slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts
        .source_input_manifest_contract
    )
    return {
        "VALIDATION_TRUST_ROOT_HASH_INPUT": slice7_artifacts.slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        "VALIDATION_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": (
            slice7_artifacts.slice6_artifacts.evidence_manifest.active_evidence_manifest_hash
        ),
        "VALIDATION_SOURCE_INPUT_MANIFEST_HASH_INPUT": source_manifest.source_input_manifest_hash,
        "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT": slice7_artifacts.pnl_contract.pnl_contract_bundle_hash,
        "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT": slice7_artifacts.pnl_input_contract.pnl_input_contract_hash,
        "VALIDATION_LEDGER_SCHEMA_HASH_INPUT": validation_contract.source_binding.validation_ledger_schema_hash,
        "VALIDATION_PROVENANCE_LEDGER_SCHEMA_HASH_INPUT": (
            validation_contract.source_binding.provenance_and_hash_ledger_schema_hash
        ),
        "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT": (
            validation_contract.source_binding.local_hostile_audit_result_schema_hash
        ),
        **{
            input_label: validation_input_policy_hash
            for input_label in REQUIRED_VALIDATION_INPUTS
            if REQUIRED_SOURCE_KIND_BY_VALIDATION_INPUT[input_label] in {"UNRESOLVED_GATE_SET", "POLICY_INPUT"}
        },
    }


def _trusted_bundle_active_source_hash_by_label(
    trusted_bundle_policy_hash: str,
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
    construction_contract: ParserFileReplayConstructionContract,
    validation_input_contract: ValidationInputContractBundle,
    validation_contract: ValidationContractBundle,
    validation_ledger_hash: str,
    provenance_ledger_hash: str,
    local_audit_hash: str,
) -> dict[str, str]:
    return {
        "BUNDLE_STATUS_INPUT": trusted_bundle_policy_hash,
        "BUNDLE_TRUST_ROOT_HASH_INPUT": slice7_artifacts.slice6_artifacts.replay_trust_root.replay_trust_root_hash,
        "BUNDLE_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": (
            slice7_artifacts.slice6_artifacts.evidence_manifest.active_evidence_manifest_hash
        ),
        "BUNDLE_CONSTRUCTION_CONTRACT_HASH_INPUT": construction_contract.construction_contract_hash,
        "BUNDLE_VALIDATION_INPUT_CONTRACT_HASH_INPUT": validation_input_contract.validation_input_contract_hash,
        "BUNDLE_VALIDATION_CONTRACT_BUNDLE_HASH_INPUT": validation_contract.validation_contract_bundle_hash,
        "BUNDLE_VALIDATION_LEDGER_HASH_INPUT": validation_ledger_hash,
        "BUNDLE_PROVENANCE_LEDGER_HASH_INPUT": provenance_ledger_hash,
        "BUNDLE_LOCAL_HOSTILE_AUDIT_RESULT_HASH_INPUT": local_audit_hash,
        "BUNDLE_FINAL_ASSEMBLY_POLICY_INPUT": trusted_bundle_policy_hash,
        "BUNDLE_PUBLIC_BOUNDARY_POLICY_INPUT": trusted_bundle_policy_hash,
        "BUNDLE_NON_AUTHORIZATION_POLICY_INPUT": trusted_bundle_policy_hash,
        "BUNDLE_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT": trusted_bundle_policy_hash,
    }


def _build_cost_input_field_contract(
    input_label: str,
    source_contract_hash: str,
    cost_input_policy_hash: str,
) -> CostInputFieldContract:
    source_kind = REQUIRED_SOURCE_KIND_BY_COST_INPUT[input_label]
    contract = CostInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_COST_INPUT_STATUS,
        source_kind=source_kind,
        fill_ledger_output_label=(
            REQUIRED_FILL_LEDGER_OUTPUT_BY_COST_INPUT[input_label]
            if source_kind == "FILL_LEDGER_OUTPUT"
            else COST_INPUT_NOT_APPLICABLE
        ),
        cost_branch_label=(
            REQUIRED_COST_BRANCH_BY_COST_INPUT[input_label]
            if source_kind == "COST_BRANCH"
            else COST_INPUT_NOT_APPLICABLE
        ),
        spread_space_label=(
            REQUIRED_SPREAD_SPACE_BY_COST_INPUT[input_label]
            if source_kind == "SPREAD_SPACE"
            else COST_INPUT_NOT_APPLICABLE
        ),
        source_policy_label=(
            REQUIRED_POLICY_LABEL_BY_COST_INPUT[input_label]
            if source_kind == "POLICY_INPUT"
            else COST_INPUT_NOT_APPLICABLE
        ),
        multiplier_proof_label=(
            REQUIRED_MULTIPLIER_PROOF_BY_COST_INPUT[input_label]
            if source_kind == "MULTIPLIER_PROOF_INPUT"
            else COST_INPUT_NOT_APPLICABLE
        ),
        currency_proof_label=(
            REQUIRED_CURRENCY_PROOF_BY_COST_INPUT[input_label]
            if source_kind == "CURRENCY_PROOF_INPUT"
            else COST_INPUT_NOT_APPLICABLE
        ),
        source_contract_hash=source_contract_hash,
        cost_input_policy_hash=cost_input_policy_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = CostInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(_cost_input_field_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_pnl_input_field_contract(
    input_label: str,
    source_contract_hash: str,
    pnl_input_policy_hash: str,
) -> PnlInputFieldContract:
    source_kind = REQUIRED_SOURCE_KIND_BY_PNL_INPUT[input_label]
    contract = PnlInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_PNL_INPUT_STATUS,
        source_kind=source_kind,
        trust_root_output_label=(
            REQUIRED_TRUST_ROOT_OUTPUT_BY_PNL_INPUT[input_label]
            if source_kind == "TRUST_ROOT_OUTPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        source_universe_output_label=(
            REQUIRED_SOURCE_UNIVERSE_OUTPUT_BY_PNL_INPUT[input_label]
            if source_kind == "SOURCE_UNIVERSE_OUTPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        transition_ledger_output_label=(
            REQUIRED_TRANSITION_LEDGER_OUTPUT_BY_PNL_INPUT[input_label]
            if source_kind == "TRANSITION_LEDGER_OUTPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        position_source_output_label=(
            REQUIRED_POSITION_SOURCE_OUTPUT_BY_PNL_INPUT[input_label]
            if source_kind == "POSITION_SOURCE_OUTPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        price_source_label=(
            REQUIRED_PRICE_SOURCE_BY_PNL_INPUT[input_label]
            if source_kind == "PRICE_SOURCE"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        price_row_proof_label=(
            REQUIRED_PRICE_ROW_PROOF_BY_PNL_INPUT[input_label]
            if source_kind == "PRICE_ROW_PROOF"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        bridge_proof_label=(
            REQUIRED_BRIDGE_PROOF_BY_PNL_INPUT[input_label]
            if source_kind == "BRIDGE_PROOF"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        fill_hash_set_output_label=(
            REQUIRED_FILL_HASH_SET_OUTPUT_BY_PNL_INPUT[input_label]
            if source_kind == "FILL_HASH_SET_OUTPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        cost_hash_set_output_label=(
            REQUIRED_COST_HASH_SET_OUTPUT_BY_PNL_INPUT[input_label]
            if source_kind == "COST_HASH_SET_OUTPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        multiplier_proof_label=(
            REQUIRED_MULTIPLIER_PROOF_BY_PNL_INPUT[input_label]
            if source_kind == "MULTIPLIER_PROOF_INPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        currency_proof_label=(
            REQUIRED_CURRENCY_PROOF_BY_PNL_INPUT[input_label]
            if source_kind == "CURRENCY_PROOF_INPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        source_policy_label=(
            REQUIRED_POLICY_LABEL_BY_PNL_INPUT[input_label]
            if source_kind == "POLICY_INPUT"
            else PNL_INPUT_NOT_APPLICABLE
        ),
        source_contract_hash=source_contract_hash,
        pnl_input_policy_hash=pnl_input_policy_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = PnlInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(_pnl_input_field_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_validation_input_field_contract(
    input_label: str,
    source_contract_hash: str,
    validation_input_policy_hash: str,
) -> ValidationInputFieldContract:
    source_kind = REQUIRED_SOURCE_KIND_BY_VALIDATION_INPUT[input_label]
    contract = ValidationInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_VALIDATION_INPUT_STATUS,
        source_kind=source_kind,
        trust_root_output_label=(
            REQUIRED_TRUST_ROOT_OUTPUT_BY_VALIDATION_INPUT[input_label]
            if source_kind == "TRUST_ROOT_OUTPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        evidence_manifest_output_label=(
            REQUIRED_EVIDENCE_MANIFEST_OUTPUT_BY_VALIDATION_INPUT[input_label]
            if source_kind == "EVIDENCE_MANIFEST_OUTPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        source_input_manifest_output_label=(
            REQUIRED_SOURCE_INPUT_MANIFEST_OUTPUT_BY_VALIDATION_INPUT[input_label]
            if source_kind == "SOURCE_INPUT_MANIFEST_OUTPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        pnl_contract_output_label=(
            REQUIRED_PNL_CONTRACT_OUTPUT_BY_VALIDATION_INPUT[input_label]
            if source_kind == "PNL_CONTRACT_OUTPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        pnl_input_contract_output_label=(
            REQUIRED_PNL_INPUT_CONTRACT_OUTPUT_BY_VALIDATION_INPUT[input_label]
            if source_kind == "PNL_INPUT_CONTRACT_OUTPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        validation_schema_output_label=(
            REQUIRED_VALIDATION_SCHEMA_OUTPUT_BY_VALIDATION_INPUT[input_label]
            if source_kind == "VALIDATION_SCHEMA_OUTPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        provenance_schema_output_label=(
            REQUIRED_PROVENANCE_SCHEMA_OUTPUT_BY_VALIDATION_INPUT[input_label]
            if source_kind == "PROVENANCE_SCHEMA_OUTPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        local_audit_schema_output_label=(
            REQUIRED_LOCAL_AUDIT_SCHEMA_OUTPUT_BY_VALIDATION_INPUT[input_label]
            if source_kind == "LOCAL_AUDIT_SCHEMA_OUTPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        unresolved_gate_set_label=(
            REQUIRED_UNRESOLVED_GATE_SET_BY_VALIDATION_INPUT[input_label]
            if source_kind == "UNRESOLVED_GATE_SET"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        unresolved_gate_labels=(
            REQUIRED_UNRESOLVED_GATE_LABELS
            if source_kind == "UNRESOLVED_GATE_SET"
            else (VALIDATION_INPUT_NOT_APPLICABLE,)
        ),
        source_policy_label=(
            REQUIRED_POLICY_LABEL_BY_VALIDATION_INPUT[input_label]
            if source_kind == "POLICY_INPUT"
            else VALIDATION_INPUT_NOT_APPLICABLE
        ),
        source_contract_hash=source_contract_hash,
        validation_input_policy_hash=validation_input_policy_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = ValidationInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(_validation_input_field_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_trusted_bundle_input_field_contract(
    input_label: str,
    source_contract_hash: str,
    trusted_bundle_policy_hash: str,
) -> TrustedBundleInputFieldContract:
    source_kind = REQUIRED_SOURCE_KIND_BY_TRUSTED_BUNDLE_INPUT[input_label]
    contract = TrustedBundleInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_TRUSTED_BUNDLE_INPUT_STATUS,
        source_kind=source_kind,
        bundle_status_label=(
            REQUIRED_BUNDLE_STATUS_BY_INPUT[input_label]
            if source_kind == "BUNDLE_STATUS"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        trust_root_output_label=(
            REQUIRED_TRUST_ROOT_OUTPUT_BY_BUNDLE_INPUT[input_label]
            if source_kind == "TRUST_ROOT_OUTPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        evidence_manifest_output_label=(
            REQUIRED_EVIDENCE_MANIFEST_OUTPUT_BY_BUNDLE_INPUT[input_label]
            if source_kind == "EVIDENCE_MANIFEST_OUTPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        construction_contract_output_label=(
            REQUIRED_CONSTRUCTION_CONTRACT_OUTPUT_BY_BUNDLE_INPUT[input_label]
            if source_kind == "CONSTRUCTION_CONTRACT_OUTPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        validation_input_contract_output_label=(
            REQUIRED_VALIDATION_INPUT_CONTRACT_OUTPUT_BY_BUNDLE_INPUT[input_label]
            if source_kind == "VALIDATION_INPUT_CONTRACT_OUTPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        validation_contract_output_label=(
            REQUIRED_VALIDATION_CONTRACT_OUTPUT_BY_BUNDLE_INPUT[input_label]
            if source_kind == "VALIDATION_CONTRACT_OUTPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        validation_ledger_output_label=(
            REQUIRED_VALIDATION_LEDGER_OUTPUT_BY_BUNDLE_INPUT[input_label]
            if source_kind == "VALIDATION_LEDGER_OUTPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        provenance_ledger_output_label=(
            REQUIRED_PROVENANCE_LEDGER_OUTPUT_BY_BUNDLE_INPUT[input_label]
            if source_kind == "PROVENANCE_LEDGER_OUTPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        local_audit_output_label=(
            REQUIRED_LOCAL_AUDIT_OUTPUT_BY_BUNDLE_INPUT[input_label]
            if source_kind == "LOCAL_AUDIT_OUTPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        source_policy_label=(
            REQUIRED_POLICY_LABEL_BY_BUNDLE_INPUT[input_label]
            if source_kind == "POLICY_INPUT"
            else TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE
        ),
        source_contract_hash=source_contract_hash,
        trusted_bundle_input_policy_hash=trusted_bundle_policy_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = TrustedBundleInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(_trusted_bundle_input_field_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_cost_dependency_binding_contract(
    label: str,
    required_labels: tuple[str, ...],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
) -> CostDependencyBindingContract:
    contract = CostDependencyBindingContract(
        dependency_label=label,
        required_dependency_labels=required_labels,
        required_dependency_contract_hashes=tuple(dependency_hash_by_label[item] for item in required_labels),
        dependency_binding_policy_hash=_slice6_policy_hash(f"COST_{dependency_kind}_DEPENDENCY_{label}"),
        dependency_binding_contract_hash="0" * 64,
    )
    contract = CostDependencyBindingContract(
        **{
            **asdict(contract),
            "dependency_binding_contract_hash": canonical_sha256(_cost_dependency_binding_hash_payload(contract)),
        }
    )
    if dependency_kind == "COMPONENT":
        contract.validate_component()
    else:
        contract.validate_invariant()
    return contract


def _build_pnl_dependency_binding_contract(
    label: str,
    required_labels: tuple[str, ...],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
) -> PnlDependencyBindingContract:
    contract = PnlDependencyBindingContract(
        dependency_label=label,
        required_dependency_labels=required_labels,
        required_dependency_contract_hashes=tuple(dependency_hash_by_label[item] for item in required_labels),
        dependency_binding_policy_hash=_slice7_policy_hash(f"PNL_{dependency_kind}_DEPENDENCY_{label}"),
        dependency_binding_contract_hash="0" * 64,
    )
    contract = PnlDependencyBindingContract(
        **{
            **asdict(contract),
            "dependency_binding_contract_hash": canonical_sha256(_pnl_dependency_binding_hash_payload(contract)),
        }
    )
    if dependency_kind == "COMPONENT":
        contract.validate_component()
    else:
        contract.validate_invariant()
    return contract


def _build_validation_dependency_binding_contract(
    label: str,
    required_labels: tuple[str, ...],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
) -> ValidationDependencyBindingContract:
    contract = ValidationDependencyBindingContract(
        dependency_label=label,
        required_dependency_labels=required_labels,
        required_dependency_contract_hashes=tuple(dependency_hash_by_label[item] for item in required_labels),
        dependency_binding_policy_hash=_slice8_policy_hash(f"VALIDATION_{dependency_kind}_DEPENDENCY_{label}"),
        dependency_binding_contract_hash="0" * 64,
    )
    contract = ValidationDependencyBindingContract(
        **{
            **asdict(contract),
            "dependency_binding_contract_hash": canonical_sha256(_validation_dependency_binding_hash_payload(contract)),
        }
    )
    if dependency_kind == "COMPONENT":
        contract.validate_component()
    elif dependency_kind == "LEDGER":
        contract.validate_ledger()
    elif dependency_kind == "AUDIT":
        contract.validate_audit_checkpoint()
    else:
        contract.validate_invariant()
    return contract


def _build_trusted_bundle_dependency_binding_contract(
    label: str,
    required_labels: tuple[str, ...],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
) -> TrustedBundleDependencyBindingContract:
    contract = TrustedBundleDependencyBindingContract(
        dependency_label=label,
        required_dependency_labels=required_labels,
        required_dependency_contract_hashes=tuple(dependency_hash_by_label[item] for item in required_labels),
        dependency_binding_policy_hash=_slice8_policy_hash(f"TRUSTED_BUNDLE_{dependency_kind}_DEPENDENCY_{label}"),
        dependency_binding_contract_hash="0" * 64,
    )
    contract = TrustedBundleDependencyBindingContract(
        **{
            **asdict(contract),
            "dependency_binding_contract_hash": canonical_sha256(_trusted_bundle_dependency_binding_hash_payload(contract)),
        }
    )
    if dependency_kind == "COMPONENT":
        contract.validate_component()
    else:
        contract.validate_invariant()
    return contract


def _build_cost_component_contract(
    component_family: str,
    dependency_hash_by_label: dict[str, str],
) -> CostComponentContract:
    required_labels = REQUIRED_COST_DEPENDENCIES_BY_COMPONENT[component_family]
    contract = CostComponentContract(
        component_family=component_family,
        component_status=PLANNED_COST_COMPONENT_STATUS,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        component_definition_hash=_slice6_policy_hash(f"COST_COMPONENT_DEFINITION_{component_family}"),
        component_policy_hash=_slice6_policy_hash(f"COST_COMPONENT_POLICY_{component_family}"),
        planned_component_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_COST_PLANNED_COMPONENT_OUTPUT",
                "component_family": component_family,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        component_contract_hash="0" * 64,
    )
    contract = CostComponentContract(
        **{**asdict(contract), "component_contract_hash": canonical_sha256(_cost_component_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_cost_branch_contract(
    branch_label: str,
    dependency_hash_by_label: dict[str, str],
) -> CostBranchContract:
    input_label = _cost_branch_input_label(branch_label)
    contract = CostBranchContract(
        branch_label=branch_label,
        required_input_hashes=(dependency_hash_by_label[input_label],),
        branch_policy_hash=_slice6_policy_hash(f"COST_BRANCH_POLICY_{branch_label}"),
        planned_branch_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_COST_PLANNED_BRANCH_OUTPUT",
                "branch_label": branch_label,
                "required_input_hashes": (dependency_hash_by_label[input_label],),
            }
        ),
        branch_contract_hash="0" * 64,
    )
    contract = CostBranchContract(
        **{**asdict(contract), "branch_contract_hash": canonical_sha256(_cost_branch_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_spread_space_contract(
    spread_space_label: str,
    spread_policy_hash: str,
) -> SpreadSpaceContract:
    contract = SpreadSpaceContract(
        spread_space_label=spread_space_label,
        required_policy_hashes=(spread_policy_hash, _slice6_policy_hash(f"SPREAD_SPACE_{spread_space_label}")),
        spread_space_contract_hash="0" * 64,
    )
    contract = SpreadSpaceContract(
        **{
            **asdict(contract),
            "spread_space_contract_hash": canonical_sha256(_spread_space_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_cost_invariant_contract(
    invariant_label: str,
    dependency_hash_by_label: dict[str, str],
) -> CostInvariantContract:
    required_labels = REQUIRED_COST_DEPENDENCIES_BY_INVARIANT[invariant_label]
    contract = CostInvariantContract(
        invariant_label=invariant_label,
        required_proof_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        invariant_policy_hash=_slice6_policy_hash(f"COST_INVARIANT_POLICY_{invariant_label}"),
        invariant_contract_hash="0" * 64,
    )
    contract = CostInvariantContract(
        **{**asdict(contract), "invariant_contract_hash": canonical_sha256(_cost_invariant_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_pnl_component_contract(
    component_family: str,
    dependency_hash_by_label: dict[str, str],
) -> PnlComponentContract:
    required_labels = REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT[component_family]
    contract = PnlComponentContract(
        component_family=component_family,
        component_status=PLANNED_PNL_COMPONENT_STATUS,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        component_definition_hash=_slice7_policy_hash(f"PNL_COMPONENT_DEFINITION_{component_family}"),
        component_policy_hash=_slice7_policy_hash(f"PNL_COMPONENT_POLICY_{component_family}"),
        planned_component_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_PNL_PLANNED_COMPONENT_OUTPUT",
                "component_family": component_family,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        component_contract_hash="0" * 64,
    )
    contract = PnlComponentContract(
        **{**asdict(contract), "component_contract_hash": canonical_sha256(_pnl_component_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_pnl_price_source_contract(
    price_source_label: str,
    pnl_input_policy_hash: str,
) -> PnlPriceSourceContract:
    contract = PnlPriceSourceContract(
        price_source_label=price_source_label,
        required_policy_hashes=(pnl_input_policy_hash, _slice7_policy_hash(f"PNL_PRICE_SOURCE_{price_source_label}")),
        price_source_contract_hash="0" * 64,
    )
    contract = PnlPriceSourceContract(
        **{
            **asdict(contract),
            "price_source_contract_hash": canonical_sha256(_pnl_price_source_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_pnl_bridge_contract(
    bridge_label: str,
    dependency_hash_by_label: dict[str, str],
) -> PnlBridgeContract:
    input_label = _pnl_bridge_input_label(bridge_label)
    contract = PnlBridgeContract(
        bridge_label=bridge_label,
        required_proof_hashes=(dependency_hash_by_label[input_label],),
        bridge_policy_hash=_slice7_policy_hash(f"PNL_BRIDGE_POLICY_{bridge_label}"),
        bridge_contract_hash="0" * 64,
    )
    contract = PnlBridgeContract(
        **{**asdict(contract), "bridge_contract_hash": canonical_sha256(_pnl_bridge_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_pnl_invariant_contract(
    invariant_label: str,
    dependency_hash_by_label: dict[str, str],
) -> PnlInvariantContract:
    required_labels = REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT[invariant_label]
    contract = PnlInvariantContract(
        invariant_label=invariant_label,
        required_proof_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        invariant_policy_hash=_slice7_policy_hash(f"PNL_INVARIANT_POLICY_{invariant_label}"),
        invariant_contract_hash="0" * 64,
    )
    contract = PnlInvariantContract(
        **{**asdict(contract), "invariant_contract_hash": canonical_sha256(_pnl_invariant_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_validation_component_contract(
    component_family: str,
    dependency_hash_by_label: dict[str, str],
) -> ValidationComponentContract:
    required_labels = REQUIRED_VALIDATION_DEPENDENCIES_BY_COMPONENT[component_family]
    contract = ValidationComponentContract(
        component_family=component_family,
        component_status=PLANNED_VALIDATION_COMPONENT_STATUS,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        component_definition_hash=_slice8_policy_hash(f"VALIDATION_COMPONENT_DEFINITION_{component_family}"),
        component_policy_hash=_slice8_policy_hash(f"VALIDATION_COMPONENT_POLICY_{component_family}"),
        planned_component_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_VALIDATION_PLANNED_COMPONENT_OUTPUT",
                "component_family": component_family,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        component_contract_hash="0" * 64,
    )
    contract = ValidationComponentContract(
        **{
            **asdict(contract),
            "component_contract_hash": canonical_sha256(_validation_component_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_validation_ledger_contract(
    ledger_label: str,
    dependency_hash_by_label: dict[str, str],
    source_binding: ValidationSourceBinding,
) -> ValidationLedgerContract:
    required_labels = REQUIRED_VALIDATION_DEPENDENCIES_BY_LEDGER[ledger_label]
    schema_hash_by_label = {
        "VALIDATION_LEDGER": source_binding.validation_ledger_schema_hash,
        "PROVENANCE_AND_HASH_LEDGER": source_binding.provenance_and_hash_ledger_schema_hash,
        "LOCAL_HOSTILE_AUDIT_RESULT": source_binding.local_hostile_audit_result_schema_hash,
    }
    contract = ValidationLedgerContract(
        ledger_label=ledger_label,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        ledger_schema_hash=schema_hash_by_label[ledger_label],
        ledger_policy_hash=_slice8_policy_hash(f"VALIDATION_LEDGER_POLICY_{ledger_label}"),
        planned_ledger_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_VALIDATION_PLANNED_LEDGER_OUTPUT",
                "ledger_label": ledger_label,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        ledger_contract_hash="0" * 64,
    )
    contract = ValidationLedgerContract(
        **{**asdict(contract), "ledger_contract_hash": canonical_sha256(_validation_ledger_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_validation_audit_checkpoint_contract(
    checkpoint_label: str,
    dependency_hash_by_label: dict[str, str],
) -> ValidationAuditCheckpointContract:
    required_labels = REQUIRED_VALIDATION_DEPENDENCIES_BY_AUDIT_CHECKPOINT[checkpoint_label]
    contract = ValidationAuditCheckpointContract(
        checkpoint_label=checkpoint_label,
        required_policy_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        planned_audit_scope_hash=canonical_sha256(
            {
                "artifact": "S27_V2_VALIDATION_PLANNED_AUDIT_SCOPE",
                "checkpoint_label": checkpoint_label,
                "required_policy_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        audit_checkpoint_contract_hash="0" * 64,
    )
    contract = ValidationAuditCheckpointContract(
        **{
            **asdict(contract),
            "audit_checkpoint_contract_hash": canonical_sha256(_validation_audit_checkpoint_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_validation_invariant_contract(
    invariant_label: str,
    dependency_hash_by_label: dict[str, str],
) -> ValidationInvariantContract:
    required_labels = REQUIRED_VALIDATION_DEPENDENCIES_BY_INVARIANT[invariant_label]
    contract = ValidationInvariantContract(
        invariant_label=invariant_label,
        required_proof_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        invariant_policy_hash=_slice8_policy_hash(f"VALIDATION_INVARIANT_POLICY_{invariant_label}"),
        invariant_contract_hash="0" * 64,
    )
    contract = ValidationInvariantContract(
        **{
            **asdict(contract),
            "invariant_contract_hash": canonical_sha256(_validation_invariant_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _fill_active_source_hash_by_label(
    fill_input_policy_hash: str,
    source_input_manifest_contract: SourceInputManifestContractBundle,
    order_contract: OrderContractBundle,
) -> dict[str, str]:
    active_hash_by_label: dict[str, str] = {}
    for input_label in REQUIRED_FILL_INPUTS:
        source_kind = REQUIRED_SOURCE_KIND_BY_FILL_INPUT[input_label]
        if source_kind in {"ORDER_LEDGER_OUTPUT", "WORKING_ORDER_TRANSITION_OUTPUT"}:
            active_hash_by_label[input_label] = order_contract.order_contract_bundle_hash
        elif source_kind == "SOURCE_ROW_PROOF":
            active_hash_by_label[input_label] = (
                source_input_manifest_contract.expected_selected_row_hash_by_manifest_field[
                    FILL_SOURCE_ROW_MANIFEST_FIELD
                ]
            )
        elif source_kind in {"FILL_PRICE_PROVENANCE", "FILL_BRANCH", "POLICY_INPUT"}:
            active_hash_by_label[input_label] = fill_input_policy_hash
        else:
            raise CarverBlocked("S27 v2 fill source kind cannot be authority-bound")
    return active_hash_by_label


def _build_fill_input_field_contract(
    input_label: str,
    source_contract_hash: str,
    fill_input_policy_hash: str,
) -> FillInputFieldContract:
    source_kind = REQUIRED_SOURCE_KIND_BY_FILL_INPUT[input_label]
    contract = FillInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_FILL_INPUT_STATUS,
        source_kind=source_kind,
        order_ledger_output_label=(
            REQUIRED_ORDER_LEDGER_OUTPUT_BY_FILL_INPUT[input_label]
            if source_kind == "ORDER_LEDGER_OUTPUT"
            else FILL_INPUT_NOT_APPLICABLE
        ),
        working_order_transition_output_label=(
            REQUIRED_WORKING_ORDER_TRANSITION_OUTPUT_BY_FILL_INPUT[input_label]
            if source_kind == "WORKING_ORDER_TRANSITION_OUTPUT"
            else FILL_INPUT_NOT_APPLICABLE
        ),
        source_row_proof_label=(
            REQUIRED_SOURCE_ROW_PROOF_BY_FILL_INPUT[input_label]
            if source_kind == "SOURCE_ROW_PROOF"
            else FILL_INPUT_NOT_APPLICABLE
        ),
        fill_price_provenance_label=(
            REQUIRED_FILL_PRICE_PROVENANCE_BY_FILL_INPUT[input_label]
            if source_kind == "FILL_PRICE_PROVENANCE"
            else FILL_INPUT_NOT_APPLICABLE
        ),
        fill_branch_label=(
            REQUIRED_FILL_BRANCH_BY_FILL_INPUT[input_label]
            if source_kind == "FILL_BRANCH"
            else FILL_INPUT_NOT_APPLICABLE
        ),
        source_policy_label=(
            REQUIRED_POLICY_LABEL_BY_FILL_INPUT[input_label]
            if source_kind == "POLICY_INPUT"
            else FILL_INPUT_NOT_APPLICABLE
        ),
        source_contract_hash=source_contract_hash,
        fill_input_policy_hash=fill_input_policy_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = FillInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(_fill_input_field_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_fill_dependency_binding_contract(
    label: str,
    required_labels: tuple[str, ...],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
) -> FillDependencyBindingContract:
    contract = FillDependencyBindingContract(
        dependency_label=label,
        required_dependency_labels=required_labels,
        required_dependency_contract_hashes=tuple(dependency_hash_by_label[item] for item in required_labels),
        dependency_binding_policy_hash=_slice5_policy_hash(f"FILL_{dependency_kind}_DEPENDENCY_{label}"),
        dependency_binding_contract_hash="0" * 64,
    )
    contract = FillDependencyBindingContract(
        **{
            **asdict(contract),
            "dependency_binding_contract_hash": canonical_sha256(_fill_dependency_binding_hash_payload(contract)),
        }
    )
    if dependency_kind == "COMPONENT":
        contract.validate_component()
    else:
        contract.validate_invariant()
    return contract


def _build_fill_component_contract(
    component_family: str,
    dependency_hash_by_label: dict[str, str],
) -> FillComponentContract:
    required_labels = REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT[component_family]
    contract = FillComponentContract(
        component_family=component_family,
        component_status=PLANNED_FILL_COMPONENT_STATUS,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        component_definition_hash=_slice5_policy_hash(f"FILL_COMPONENT_DEFINITION_{component_family}"),
        component_policy_hash=_slice5_policy_hash(f"FILL_COMPONENT_POLICY_{component_family}"),
        planned_component_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_FILL_PLANNED_COMPONENT_OUTPUT",
                "component_family": component_family,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        component_contract_hash="0" * 64,
    )
    contract = FillComponentContract(
        **{**asdict(contract), "component_contract_hash": canonical_sha256(_fill_component_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_fill_price_provenance_contract(
    provenance_label: str,
    source_policy_hash: str,
) -> FillPriceProvenanceContract:
    contract = FillPriceProvenanceContract(
        provenance_label=provenance_label,
        required_policy_hashes=(
            source_policy_hash,
            _slice5_policy_hash(f"FILL_PRICE_PROVENANCE_POLICY_{provenance_label}"),
        ),
        provenance_contract_hash="0" * 64,
    )
    contract = FillPriceProvenanceContract(
        **{
            **asdict(contract),
            "provenance_contract_hash": canonical_sha256(_fill_price_provenance_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_fill_branch_contract(
    branch_label: str,
    dependency_hash_by_label: dict[str, str],
) -> FillBranchContract:
    input_label = _fill_branch_input_label(branch_label)
    contract = FillBranchContract(
        branch_label=branch_label,
        required_input_hashes=(dependency_hash_by_label[input_label],),
        branch_policy_hash=_slice5_policy_hash(f"FILL_BRANCH_POLICY_{branch_label}"),
        planned_branch_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_FILL_PLANNED_BRANCH_OUTPUT",
                "branch_label": branch_label,
                "required_input_hashes": (dependency_hash_by_label[input_label],),
            }
        ),
        branch_contract_hash="0" * 64,
    )
    contract = FillBranchContract(
        **{**asdict(contract), "branch_contract_hash": canonical_sha256(_fill_branch_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_fill_invariant_contract(
    invariant_label: str,
    dependency_hash_by_label: dict[str, str],
) -> FillInvariantContract:
    required_labels = REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT[invariant_label]
    contract = FillInvariantContract(
        invariant_label=invariant_label,
        required_proof_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        invariant_policy_hash=_slice5_policy_hash(f"FILL_INVARIANT_POLICY_{invariant_label}"),
        invariant_contract_hash="0" * 64,
    )
    contract = FillInvariantContract(
        **{**asdict(contract), "invariant_contract_hash": canonical_sha256(_fill_invariant_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _validate_fill_input_contract_local_only(
    contract: FillInputContractBundle,
    slice4_artifacts: LocalParserFileReplaySlice4Artifacts,
) -> None:
    source_manifest = slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    if contract.status != S27_V2_FILL_INPUT_CONTRACT_ONLY_STATUS:
        raise CarverBlocked("S27 v2 fill input contract must remain contract-only")
    if contract.source_input_manifest_contract_hash != source_manifest.source_input_manifest_contract_hash:
        raise CarverBlocked("S27 v2 fill input must bind active source-input manifest")
    if contract.order_input_contract_hash != slice4_artifacts.order_input_contract.order_input_contract_hash:
        raise CarverBlocked("S27 v2 fill input must bind active order input")
    if contract.order_contract_bundle_hash != slice4_artifacts.order_contract.order_contract_bundle_hash:
        raise CarverBlocked("S27 v2 fill input must bind active order contract")
    expected_policy_hash = _slice5_policy_hash("FILL_INPUT")
    if contract.fill_input_policy_hash != expected_policy_hash:
        raise CarverBlocked("S27 v2 fill input policy hash must be content-bound")
    active_source_hash_by_label = _fill_active_source_hash_by_label(
        contract.fill_input_policy_hash,
        source_manifest,
        slice4_artifacts.order_contract,
    )
    _require_hash_map_exact(
        "S27 v2 fill expected source contract map",
        contract.expected_source_contract_hash_by_input_label,
        active_source_hash_by_label,
        REQUIRED_FILL_INPUTS,
    )
    dependency_hash_by_label = _validate_fill_input_fields(contract)
    _validate_fill_dependency_bindings(
        contract.component_dependency_bindings,
        REQUIRED_FILL_COMPONENT_FAMILIES,
        REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT,
        dependency_hash_by_label,
        "component",
    )
    _validate_fill_dependency_bindings(
        contract.invariant_dependency_bindings,
        REQUIRED_FILL_INVARIANTS,
        REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT,
        dependency_hash_by_label,
        "invariant",
        update_dependency_map=False,
    )
    expected_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FILL_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.component_dependency_bindings
            ),
            "input_field_contract_hashes": tuple(
                field.input_field_contract_hash for field in contract.input_field_contracts
            ),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.invariant_dependency_bindings
            ),
            "order_contract_bundle_hash": contract.order_contract_bundle_hash,
            "order_input_contract_hash": contract.order_input_contract_hash,
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.fill_input_set_hash != expected_set_hash:
        raise CarverBlocked("S27 v2 fill input set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FILL_INPUT_CONTRACT",
            "fill_input_policy_hash": contract.fill_input_policy_hash,
            "fill_input_set_hash": contract.fill_input_set_hash,
            "order_contract_bundle_hash": contract.order_contract_bundle_hash,
            "order_input_contract_hash": contract.order_input_contract_hash,
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.fill_input_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 fill input contract hash must be content-bound")


def _validate_fill_contract_content_bound(
    contract: FillContractBundle,
    fill_input_contract: FillInputContractBundle,
    slice4_artifacts: LocalParserFileReplaySlice4Artifacts,
) -> None:
    contract.validate()
    order_contract = slice4_artifacts.order_contract
    if contract.source_binding.order_contract_bundle_hash != order_contract.order_contract_bundle_hash:
        raise CarverBlocked("S27 v2 fill source binding must bind order contract")
    if contract.source_binding.source_input_manifest_hash != order_contract.source_binding.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 fill source binding must bind source-input manifest")
    if contract.source_binding.limit_order_ledger_schema_hash != order_contract.source_binding.limit_order_ledger_schema_hash:
        raise CarverBlocked("S27 v2 fill source binding must bind limit-order schema")
    if contract.source_binding.market_order_ledger_schema_hash != order_contract.source_binding.market_order_ledger_schema_hash:
        raise CarverBlocked("S27 v2 fill source binding must bind market-order schema")
    if (
        contract.source_binding.working_order_transition_schema_hash
        != order_contract.source_binding.working_order_transition_schema_hash
    ):
        raise CarverBlocked("S27 v2 fill source binding must bind working-order transition schema")
    if contract.source_binding.fill_source_binding_hash != canonical_sha256(
        _fill_source_binding_hash_payload(contract.source_binding)
    ):
        raise CarverBlocked("S27 v2 fill source binding hash must be content-bound")
    dependency_hash_by_label = _fill_input_hash_by_label(fill_input_contract)
    for component in contract.component_contracts:
        if component.required_input_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT[component.component_family]
        ):
            raise CarverBlocked("S27 v2 fill component must bind active fill inputs")
        if component.component_contract_hash != canonical_sha256(_fill_component_hash_payload(component)):
            raise CarverBlocked("S27 v2 fill component hash must be content-bound")
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    for provenance in contract.price_provenance_contracts:
        if provenance.required_policy_hashes[0] != fill_input_contract.fill_input_policy_hash:
            raise CarverBlocked("S27 v2 fill price provenance must bind fill input policy")
        if provenance.provenance_contract_hash != canonical_sha256(
            _fill_price_provenance_hash_payload(provenance)
        ):
            raise CarverBlocked("S27 v2 fill price provenance hash must be content-bound")
    for branch in contract.branch_contracts:
        expected_input = _fill_branch_input_label(branch.branch_label)
        if branch.required_input_hashes != (dependency_hash_by_label[expected_input],):
            raise CarverBlocked("S27 v2 fill branch must bind active fill branch input")
        if branch.branch_contract_hash != canonical_sha256(_fill_branch_hash_payload(branch)):
            raise CarverBlocked("S27 v2 fill branch hash must be content-bound")
        dependency_hash_by_label[branch.branch_label] = branch.branch_contract_hash
    for invariant in contract.invariant_contracts:
        if invariant.required_proof_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT[invariant.invariant_label]
        ):
            raise CarverBlocked("S27 v2 fill invariant must bind active dependencies")
        if invariant.invariant_contract_hash != canonical_sha256(_fill_invariant_hash_payload(invariant)):
            raise CarverBlocked("S27 v2 fill invariant hash must be content-bound")
    if contract.one_hour_lag_policy_hash != fill_input_contract.fill_input_policy_hash:
        raise CarverBlocked("S27 v2 fill one-hour lag policy must bind fill input policy")
    if contract.session_gap_policy_hash != fill_input_contract.fill_input_policy_hash:
        raise CarverBlocked("S27 v2 fill session-gap policy must bind fill input policy")
    if contract.fill_contract_bundle_hash != canonical_sha256(_fill_contract_bundle_hash_payload(contract)):
        raise CarverBlocked("S27 v2 fill contract bundle hash must be content-bound")


def _validate_cost_input_contract_local_only(
    contract: CostInputContractBundle,
    slice5_artifacts: LocalParserFileReplaySlice5Artifacts,
    replay_trust_root: ReplayTrustRoot,
    evidence_manifest: EvidenceManifest,
) -> None:
    source_manifest = (
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    contract.validate_against_fill_authority(
        replay_trust_root,
        evidence_manifest,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_row_selection_external_authority,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.source_row_batch_contract,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.parser_output_contract,
        source_manifest,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.level_compatibility_input_contract,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.level_compatibility_contract,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.runtime_history_input_contract,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.runtime_history_contract,
        slice5_artifacts.slice4_artifacts.forecast_input_contract,
        slice5_artifacts.slice4_artifacts.forecast_contract,
        slice5_artifacts.slice4_artifacts.position_input_contract,
        slice5_artifacts.slice4_artifacts.position_contract,
        slice5_artifacts.slice4_artifacts.order_input_contract,
        slice5_artifacts.slice4_artifacts.order_contract,
        slice5_artifacts.fill_input_contract,
        slice5_artifacts.fill_contract,
    )
    expected_policy_hash = _slice6_policy_hash("COST_INPUT")
    if contract.cost_input_policy_hash != expected_policy_hash:
        raise CarverBlocked("S27 v2 cost input policy hash must be content-bound")
    active_source_hash_by_label = _cost_active_source_hash_by_label(
        contract.cost_input_policy_hash,
        replay_trust_root,
        slice5_artifacts.fill_contract,
    )
    _require_hash_map_exact(
        "S27 v2 cost expected source contract map",
        contract.expected_source_contract_hash_by_input_label,
        active_source_hash_by_label,
        REQUIRED_COST_INPUTS,
    )
    dependency_hash_by_label = _validate_cost_input_fields(contract)
    _validate_cost_dependency_bindings(
        contract.component_dependency_bindings,
        REQUIRED_COST_COMPONENT_FAMILIES,
        REQUIRED_COST_DEPENDENCIES_BY_COMPONENT,
        dependency_hash_by_label,
        "component",
    )
    _validate_cost_dependency_bindings(
        contract.invariant_dependency_bindings,
        REQUIRED_COST_INVARIANTS,
        REQUIRED_COST_DEPENDENCIES_BY_INVARIANT,
        dependency_hash_by_label,
        "invariant",
        update_dependency_map=False,
    )
    expected_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_COST_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.component_dependency_bindings
            ),
            "fill_contract_bundle_hash": contract.fill_contract_bundle_hash,
            "fill_input_contract_hash": contract.fill_input_contract_hash,
            "input_field_contract_hashes": tuple(
                field.input_field_contract_hash for field in contract.input_field_contracts
            ),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.invariant_dependency_bindings
            ),
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.cost_input_set_hash != expected_set_hash:
        raise CarverBlocked("S27 v2 cost input set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_COST_INPUT_CONTRACT",
            "cost_input_policy_hash": contract.cost_input_policy_hash,
            "cost_input_set_hash": contract.cost_input_set_hash,
            "fill_contract_bundle_hash": contract.fill_contract_bundle_hash,
            "fill_input_contract_hash": contract.fill_input_contract_hash,
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.cost_input_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 cost input contract hash must be content-bound")


def _validate_cost_contract_content_bound(
    contract: CostContractBundle,
    cost_input_contract: CostInputContractBundle,
    slice5_artifacts: LocalParserFileReplaySlice5Artifacts,
    replay_trust_root: ReplayTrustRoot,
    evidence_manifest: EvidenceManifest,
) -> None:
    contract.validate_against_policy_authority(replay_trust_root, evidence_manifest)
    source_manifest = (
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    if contract.source_binding.source_input_manifest_hash != source_manifest.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 cost source binding must bind source-input manifest")
    if contract.source_binding.fill_contract_bundle_hash != slice5_artifacts.fill_contract.fill_contract_bundle_hash:
        raise CarverBlocked("S27 v2 cost source binding must bind fill contract")
    if contract.source_binding.fill_ledger_schema_hash != slice5_artifacts.fill_contract.source_binding.fill_ledger_schema_hash:
        raise CarverBlocked("S27 v2 cost source binding must bind fill ledger schema")
    if contract.source_binding.cost_source_binding_hash != canonical_sha256(
        _cost_source_binding_hash_payload(contract.source_binding)
    ):
        raise CarverBlocked("S27 v2 cost source binding hash must be content-bound")
    dependency_hash_by_label = _cost_input_hash_by_label(cost_input_contract)
    component_hash_by_family = {
        component.component_family: component.component_contract_hash
        for component in contract.component_contracts
    }
    for component in contract.component_contracts:
        expected_component_inputs = tuple(
            dependency_hash_by_label[label]
            if label in dependency_hash_by_label
            else component_hash_by_family[label]
            for label in REQUIRED_COST_DEPENDENCIES_BY_COMPONENT[component.component_family]
        )
        if component.required_input_hashes != expected_component_inputs:
            raise CarverBlocked("S27 v2 cost component must bind active cost inputs")
        if component.component_contract_hash != canonical_sha256(_cost_component_hash_payload(component)):
            raise CarverBlocked("S27 v2 cost component hash must be content-bound")
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    for branch in contract.branch_contracts:
        expected_input = _cost_branch_input_label(branch.branch_label)
        if branch.required_input_hashes != (dependency_hash_by_label[expected_input],):
            raise CarverBlocked("S27 v2 cost branch must bind active branch input")
        if branch.branch_contract_hash != canonical_sha256(_cost_branch_hash_payload(branch)):
            raise CarverBlocked("S27 v2 cost branch hash must be content-bound")
        dependency_hash_by_label[branch.branch_label] = branch.branch_contract_hash
    for spread_space in contract.spread_space_contracts:
        if spread_space.required_policy_hashes[0] != replay_trust_root.spread_unit_policy_hash:
            raise CarverBlocked("S27 v2 cost spread-space must bind trust-root spread policy")
        if spread_space.spread_space_contract_hash != canonical_sha256(_spread_space_hash_payload(spread_space)):
            raise CarverBlocked("S27 v2 cost spread-space hash must be content-bound")
    for invariant in contract.invariant_contracts:
        if invariant.required_proof_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_COST_DEPENDENCIES_BY_INVARIANT[invariant.invariant_label]
        ):
            raise CarverBlocked("S27 v2 cost invariant must bind active dependencies")
        if invariant.invariant_contract_hash != canonical_sha256(_cost_invariant_hash_payload(invariant)):
            raise CarverBlocked("S27 v2 cost invariant hash must be content-bound")
    if contract.cost_calculation_policy_hash != cost_input_contract.cost_input_policy_hash:
        raise CarverBlocked("S27 v2 cost calculation policy must bind cost input policy")
    if contract.deflation_policy_hash != cost_input_contract.cost_input_policy_hash:
        raise CarverBlocked("S27 v2 cost deflation policy must bind cost input policy")
    if contract.cost_contract_bundle_hash != canonical_sha256(_cost_contract_bundle_hash_payload(contract)):
        raise CarverBlocked("S27 v2 cost contract bundle hash must be content-bound")


def _validate_pnl_input_contract_local_only(
    contract: PnlInputContractBundle,
    slice6_artifacts: LocalParserFileReplaySlice6Artifacts,
) -> None:
    slice5_artifacts = slice6_artifacts.slice5_artifacts
    source_manifest = (
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    contract.validate_against_cost_authority(
        slice6_artifacts.replay_trust_root,
        slice6_artifacts.evidence_manifest,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_row_selection_external_authority,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.source_row_batch_contract,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.parser_output_contract,
        source_manifest,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.level_compatibility_input_contract,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.level_compatibility_contract,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.runtime_history_input_contract,
        slice5_artifacts.slice4_artifacts.slice3_artifacts.runtime_history_contract,
        slice5_artifacts.slice4_artifacts.forecast_input_contract,
        slice5_artifacts.slice4_artifacts.forecast_contract,
        slice5_artifacts.slice4_artifacts.position_input_contract,
        slice5_artifacts.slice4_artifacts.position_contract,
        slice5_artifacts.slice4_artifacts.order_input_contract,
        slice5_artifacts.slice4_artifacts.order_contract,
        slice5_artifacts.fill_input_contract,
        slice5_artifacts.fill_contract,
        slice6_artifacts.cost_input_contract,
        slice6_artifacts.cost_contract,
    )
    expected_policy_hash = _slice7_policy_hash("PNL_INPUT")
    if contract.pnl_input_policy_hash != expected_policy_hash:
        raise CarverBlocked("S27 v2 PnL input policy hash must be content-bound")
    active_source_hash_by_label = _pnl_active_source_hash_by_label(contract.pnl_input_policy_hash, slice6_artifacts)
    _require_hash_map_exact(
        "S27 v2 PnL expected source contract map",
        contract.expected_source_contract_hash_by_input_label,
        active_source_hash_by_label,
        REQUIRED_PNL_INPUTS,
    )
    dependency_hash_by_label = _validate_pnl_input_fields(contract)
    _validate_pnl_dependency_bindings(
        contract.component_dependency_bindings,
        REQUIRED_PNL_COMPONENT_FAMILIES,
        REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT,
        dependency_hash_by_label,
        "component",
    )
    _validate_pnl_dependency_bindings(
        contract.invariant_dependency_bindings,
        REQUIRED_PNL_INVARIANTS,
        REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT,
        dependency_hash_by_label,
        "invariant",
        update_dependency_map=False,
    )
    expected_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_PNL_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.component_dependency_bindings
            ),
            "cost_contract_bundle_hash": contract.cost_contract_bundle_hash,
            "cost_input_contract_hash": contract.cost_input_contract_hash,
            "input_field_contract_hashes": tuple(
                field.input_field_contract_hash for field in contract.input_field_contracts
            ),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.invariant_dependency_bindings
            ),
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.pnl_input_set_hash != expected_set_hash:
        raise CarverBlocked("S27 v2 PnL input set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_PNL_INPUT_CONTRACT",
            "cost_contract_bundle_hash": contract.cost_contract_bundle_hash,
            "cost_input_contract_hash": contract.cost_input_contract_hash,
            "pnl_input_policy_hash": contract.pnl_input_policy_hash,
            "pnl_input_set_hash": contract.pnl_input_set_hash,
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.pnl_input_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 PnL input contract hash must be content-bound")


def _validate_pnl_contract_content_bound(
    contract: PnlContractBundle,
    pnl_input_contract: PnlInputContractBundle,
    slice6_artifacts: LocalParserFileReplaySlice6Artifacts,
) -> None:
    contract.validate()
    source_manifest = (
        slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    if contract.source_binding.replay_trust_root_hash != slice6_artifacts.replay_trust_root.replay_trust_root_hash:
        raise CarverBlocked("S27 v2 PnL source binding must bind replay trust root")
    if contract.source_binding.source_input_manifest_hash != source_manifest.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 PnL source binding must bind source-input manifest")
    if contract.source_binding.fill_ledger_schema_hash != slice6_artifacts.slice5_artifacts.fill_contract.source_binding.fill_ledger_schema_hash:
        raise CarverBlocked("S27 v2 PnL source binding must bind fill ledger schema")
    if contract.source_binding.cost_ledger_schema_hash != slice6_artifacts.cost_contract.source_binding.cost_ledger_schema_hash:
        raise CarverBlocked("S27 v2 PnL source binding must bind cost ledger schema")
    if contract.source_binding.pnl_source_binding_hash != canonical_sha256(
        _pnl_source_binding_hash_payload(contract.source_binding)
    ):
        raise CarverBlocked("S27 v2 PnL source binding hash must be content-bound")
    dependency_hash_by_label = _pnl_input_hash_by_label(pnl_input_contract)
    for component in contract.component_contracts:
        if component.required_input_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT[component.component_family]
        ):
            raise CarverBlocked("S27 v2 PnL component must bind active PnL inputs")
        if component.component_contract_hash != canonical_sha256(_pnl_component_hash_payload(component)):
            raise CarverBlocked("S27 v2 PnL component hash must be content-bound")
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    for price_source in contract.price_source_contracts:
        if price_source.required_policy_hashes[0] != pnl_input_contract.pnl_input_policy_hash:
            raise CarverBlocked("S27 v2 PnL price source must bind PnL input policy")
        if price_source.price_source_contract_hash != canonical_sha256(_pnl_price_source_hash_payload(price_source)):
            raise CarverBlocked("S27 v2 PnL price source hash must be content-bound")
    for bridge in contract.bridge_contracts:
        expected_input = _pnl_bridge_input_label(bridge.bridge_label)
        if bridge.required_proof_hashes != (dependency_hash_by_label[expected_input],):
            raise CarverBlocked("S27 v2 PnL bridge must bind active bridge input")
        if bridge.bridge_contract_hash != canonical_sha256(_pnl_bridge_hash_payload(bridge)):
            raise CarverBlocked("S27 v2 PnL bridge hash must be content-bound")
        dependency_hash_by_label[bridge.bridge_label] = bridge.bridge_contract_hash
    for invariant in contract.invariant_contracts:
        if invariant.required_proof_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT[invariant.invariant_label]
        ):
            raise CarverBlocked("S27 v2 PnL invariant must bind active dependencies")
        if invariant.invariant_contract_hash != canonical_sha256(_pnl_invariant_hash_payload(invariant)):
            raise CarverBlocked("S27 v2 PnL invariant hash must be content-bound")
    if contract.pnl_formula_policy_hash != pnl_input_contract.pnl_input_policy_hash:
        raise CarverBlocked("S27 v2 PnL formula policy must bind PnL input policy")
    if contract.contract_multiplier_policy_hash != slice6_artifacts.replay_trust_root.contract_multiplier_currency_policy_hash:
        raise CarverBlocked("S27 v2 PnL multiplier policy must bind trust root")
    if contract.currency_policy_hash != slice6_artifacts.replay_trust_root.contract_multiplier_currency_policy_hash:
        raise CarverBlocked("S27 v2 PnL currency policy must bind trust root")
    if contract.pnl_contract_bundle_hash != canonical_sha256(_pnl_contract_bundle_hash_payload(contract)):
        raise CarverBlocked("S27 v2 PnL contract bundle hash must be content-bound")


def _validate_construction_contract_local_only(
    contract: ParserFileReplayConstructionContract,
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
) -> None:
    contract.validate()
    if contract.construction_contract_hash != canonical_sha256(_construction_contract_hash_payload(contract)):
        raise CarverBlocked("S27 v2 construction contract hash must be content-bound")
    planned_hash_by_family = _planned_artifact_hash_by_family(slice7_artifacts)
    for phase in contract.construction_phases:
        if phase.phase_contract_hash != canonical_sha256(_construction_phase_hash_payload(phase)):
            raise CarverBlocked("S27 v2 construction phase hash must be content-bound")
        for artifact in phase.planned_output_artifacts:
            if artifact.artifact_hash != planned_hash_by_family[artifact.artifact_family]:
                raise CarverBlocked("S27 v2 construction artifact must bind active planned artifact")


def _validate_validation_input_contract_local_only(
    contract: ValidationInputContractBundle,
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
    validation_contract: ValidationContractBundle,
) -> None:
    slice6 = slice7_artifacts.slice6_artifacts
    slice5 = slice6.slice5_artifacts
    source_manifest = (
        slice5.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    )
    contract.validate_against_pnl_authority(
        slice6.replay_trust_root,
        slice6.evidence_manifest,
        slice5.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_row_selection_external_authority,
        slice5.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.source_row_batch_contract,
        slice5.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.parser_output_contract,
        source_manifest,
        slice5.slice4_artifacts.slice3_artifacts.level_compatibility_input_contract,
        slice5.slice4_artifacts.slice3_artifacts.level_compatibility_contract,
        slice5.slice4_artifacts.slice3_artifacts.runtime_history_input_contract,
        slice5.slice4_artifacts.slice3_artifacts.runtime_history_contract,
        slice5.slice4_artifacts.forecast_input_contract,
        slice5.slice4_artifacts.forecast_contract,
        slice5.slice4_artifacts.position_input_contract,
        slice5.slice4_artifacts.position_contract,
        slice5.slice4_artifacts.order_input_contract,
        slice5.slice4_artifacts.order_contract,
        slice5.fill_input_contract,
        slice5.fill_contract,
        slice6.cost_input_contract,
        slice6.cost_contract,
        slice7_artifacts.pnl_input_contract,
        slice7_artifacts.pnl_contract,
    )
    if contract.validation_contract_bundle_hash != validation_contract.validation_contract_bundle_hash:
        raise CarverBlocked("S27 v2 validation input must bind validation contract bundle")
    if contract.validation_input_policy_hash != _slice8_policy_hash("VALIDATION_INPUT"):
        raise CarverBlocked("S27 v2 validation input policy hash must be content-bound")
    active_source_hash_by_label = _validation_active_source_hash_by_label(
        contract.validation_input_policy_hash,
        slice7_artifacts,
        validation_contract,
    )
    _require_hash_map_exact(
        "S27 v2 validation expected source contract map",
        contract.expected_source_contract_hash_by_input_label,
        active_source_hash_by_label,
        REQUIRED_VALIDATION_INPUTS,
    )
    dependency_hash_by_label = _validate_validation_input_fields(contract)
    _validate_validation_dependency_bindings(
        contract.component_dependency_bindings,
        REQUIRED_VALIDATION_COMPONENT_FAMILIES,
        REQUIRED_VALIDATION_DEPENDENCIES_BY_COMPONENT,
        dependency_hash_by_label,
        "component",
    )
    _validate_validation_dependency_bindings(
        contract.ledger_dependency_bindings,
        REQUIRED_VALIDATION_LEDGER_LABELS,
        REQUIRED_VALIDATION_DEPENDENCIES_BY_LEDGER,
        dependency_hash_by_label,
        "ledger",
    )
    _validate_validation_dependency_bindings(
        contract.audit_checkpoint_dependency_bindings,
        REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS,
        REQUIRED_VALIDATION_DEPENDENCIES_BY_AUDIT_CHECKPOINT,
        dependency_hash_by_label,
        "audit checkpoint",
    )
    _validate_validation_dependency_bindings(
        contract.invariant_dependency_bindings,
        REQUIRED_VALIDATION_INVARIANTS,
        REQUIRED_VALIDATION_DEPENDENCIES_BY_INVARIANT,
        dependency_hash_by_label,
        "invariant",
        update_dependency_map=False,
    )
    if contract.validation_input_contract_hash != canonical_sha256(_validation_input_contract_hash_payload(contract)):
        raise CarverBlocked("S27 v2 validation input contract hash must be content-bound")


def _validate_validation_contract_content_bound(
    contract: ValidationContractBundle,
    validation_input_contract: ValidationInputContractBundle,
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
) -> None:
    contract.validate()
    if contract.source_binding.replay_trust_root_hash != slice7_artifacts.slice6_artifacts.replay_trust_root.replay_trust_root_hash:
        raise CarverBlocked("S27 v2 validation source binding must bind replay trust root")
    if contract.source_binding.active_evidence_manifest_hash != (
        slice7_artifacts.slice6_artifacts.evidence_manifest.active_evidence_manifest_hash
    ):
        raise CarverBlocked("S27 v2 validation source binding must bind evidence manifest")
    if contract.source_binding.pnl_contract_bundle_hash != slice7_artifacts.pnl_contract.pnl_contract_bundle_hash:
        raise CarverBlocked("S27 v2 validation source binding must bind PnL contract")
    if contract.validation_contract_bundle_hash != canonical_sha256(_validation_contract_bundle_hash_payload(contract)):
        raise CarverBlocked("S27 v2 validation contract bundle hash must be content-bound")
    if validation_input_contract.validation_contract_bundle_hash != contract.validation_contract_bundle_hash:
        raise CarverBlocked("S27 v2 validation contract must be bound by validation input")


def _validate_trusted_bundle_contract_content_bound(
    contract: TrustedBundleContractBundle,
    construction_contract: ParserFileReplayConstructionContract,
    validation_input_contract: ValidationInputContractBundle,
    validation_contract: ValidationContractBundle,
    slice7_artifacts: LocalParserFileReplaySlice7Artifacts,
) -> None:
    slice6 = slice7_artifacts.slice6_artifacts
    slice5 = slice6.slice5_artifacts
    contract.validate_against_validation_authority(
        slice6.replay_trust_root,
        slice6.evidence_manifest,
        slice5.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_row_selection_external_authority,
        slice5.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.source_row_batch_contract,
        slice5.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts.parser_output_contract,
        slice5.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract,
        slice5.slice4_artifacts.slice3_artifacts.level_compatibility_input_contract,
        slice5.slice4_artifacts.slice3_artifacts.level_compatibility_contract,
        slice5.slice4_artifacts.slice3_artifacts.runtime_history_input_contract,
        slice5.slice4_artifacts.slice3_artifacts.runtime_history_contract,
        slice5.slice4_artifacts.forecast_input_contract,
        slice5.slice4_artifacts.forecast_contract,
        slice5.slice4_artifacts.position_input_contract,
        slice5.slice4_artifacts.position_contract,
        slice5.slice4_artifacts.order_input_contract,
        slice5.slice4_artifacts.order_contract,
        slice5.fill_input_contract,
        slice5.fill_contract,
        slice6.cost_input_contract,
        slice6.cost_contract,
        slice7_artifacts.pnl_input_contract,
        slice7_artifacts.pnl_contract,
        construction_contract,
        validation_input_contract,
        validation_contract,
    )
    if contract.trusted_bundle_contract_hash != canonical_sha256(_trusted_bundle_contract_hash_payload(contract)):
        raise CarverBlocked("S27 v2 trusted bundle contract hash must be content-bound")


def _slice4_policy_hash(label: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_LOCAL_ONLY_SLICE4_POLICY",
            "label": label,
            "scope": "FORECAST_POSITION_ORDER_TRANSITION_CONSTRUCTION_SCAFFOLD_ONLY",
        }
    )


def _forecast_active_source_hash_by_label(
    forecast_input_policy_hash: str,
    runtime_history_input_contract: RuntimeHistoryInputContractBundle,
    runtime_history_contract: RuntimeHistoryContractBundle,
) -> dict[str, str]:
    runtime_input_hash_by_label = _runtime_history_input_hash_by_label(runtime_history_input_contract)
    runtime_state_hash_by_family = {
        contract.state_family: contract.state_contract_hash
        for contract in runtime_history_contract.state_contracts
    }
    vqm_hash_by_label = {
        contract.component_label: contract.component_contract_hash
        for contract in runtime_history_contract.vqm_component_contracts
    }
    if tuple(runtime_state_hash_by_family) != REQUIRED_RUNTIME_STATE_FAMILIES:
        raise CarverBlocked("S27 v2 forecast active runtime-state authority must match locked tuple")
    if tuple(vqm_hash_by_label) != REQUIRED_VQM_COMPONENTS:
        raise CarverBlocked("S27 v2 forecast active V/Q/M authority must match locked tuple")
    active_hash_by_label: dict[str, str] = {}
    for input_label in REQUIRED_FORECAST_INPUTS:
        source_kind = REQUIRED_SOURCE_KIND_BY_FORECAST_INPUT[input_label]
        if source_kind == "RUNTIME_INPUT":
            active_hash_by_label[input_label] = runtime_input_hash_by_label[
                REQUIRED_RUNTIME_HISTORY_INPUT_BY_FORECAST_INPUT[input_label]
            ]
        elif source_kind == "RUNTIME_STATE":
            active_hash_by_label[input_label] = runtime_state_hash_by_family[
                REQUIRED_RUNTIME_STATE_BY_FORECAST_INPUT[input_label]
            ]
        elif source_kind == "VQM_COMPONENT":
            active_hash_by_label[input_label] = vqm_hash_by_label[
                REQUIRED_VQM_COMPONENT_BY_FORECAST_INPUT[input_label]
            ]
        elif source_kind == "POLICY_INPUT":
            active_hash_by_label[input_label] = forecast_input_policy_hash
        else:
            raise CarverBlocked("S27 v2 forecast source kind cannot be authority-bound")
    return active_hash_by_label


def _position_active_source_hash_by_label(
    position_input_policy_hash: str,
    forecast_contract: ForecastContractBundle,
) -> dict[str, str]:
    forecast_component_hash_by_family = _forecast_component_hash_by_family(forecast_contract)
    active_hash_by_label: dict[str, str] = {}
    for input_label in REQUIRED_POSITION_INPUTS:
        source_kind = REQUIRED_SOURCE_KIND_BY_POSITION_INPUT[input_label]
        if source_kind == "FORECAST_COMPONENT":
            active_hash_by_label[input_label] = forecast_component_hash_by_family[
                REQUIRED_FORECAST_COMPONENT_BY_POSITION_INPUT[input_label]
            ]
        elif source_kind == "FORECAST_LEDGER_OUTPUT":
            active_hash_by_label[input_label] = forecast_contract.forecast_contract_bundle_hash
        elif source_kind in {"ROUNDING_POLICY", "POSITION_STATE_CONTEXT", "POLICY_INPUT"}:
            active_hash_by_label[input_label] = position_input_policy_hash
        else:
            raise CarverBlocked("S27 v2 position source kind cannot be authority-bound")
    return active_hash_by_label


def _order_active_source_hash_by_label(
    order_input_policy_hash: str,
    position_contract: PositionContractBundle,
) -> dict[str, str]:
    position_component_hash_by_family = _position_component_hash_by_family(position_contract)
    active_hash_by_label: dict[str, str] = {}
    for input_label in REQUIRED_ORDER_INPUTS:
        source_kind = REQUIRED_SOURCE_KIND_BY_ORDER_INPUT[input_label]
        if source_kind == "POSITION_COMPONENT":
            active_hash_by_label[input_label] = position_component_hash_by_family[
                REQUIRED_POSITION_COMPONENT_BY_ORDER_INPUT[input_label]
            ]
        elif source_kind == "POSITION_LEDGER_OUTPUT":
            active_hash_by_label[input_label] = position_contract.desired_position_contract_bundle_hash
        elif source_kind in {"ORDER_KIND", "ORDER_TRANSITION_KIND", "ORDER_STATE_CONTEXT", "POLICY_INPUT"}:
            active_hash_by_label[input_label] = order_input_policy_hash
        else:
            raise CarverBlocked("S27 v2 order source kind cannot be authority-bound")
    return active_hash_by_label


def _build_forecast_input_field_contract(
    input_label: str,
    source_contract_hash: str,
    forecast_input_policy_hash: str,
) -> ForecastInputFieldContract:
    source_kind = REQUIRED_SOURCE_KIND_BY_FORECAST_INPUT[input_label]
    contract = ForecastInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_FORECAST_INPUT_STATUS,
        source_kind=source_kind,
        runtime_history_input_label=(
            REQUIRED_RUNTIME_HISTORY_INPUT_BY_FORECAST_INPUT[input_label]
            if source_kind == "RUNTIME_INPUT"
            else FORECAST_INPUT_NOT_APPLICABLE
        ),
        runtime_state_family=(
            REQUIRED_RUNTIME_STATE_BY_FORECAST_INPUT[input_label]
            if source_kind == "RUNTIME_STATE"
            else FORECAST_INPUT_NOT_APPLICABLE
        ),
        vqm_component_label=(
            REQUIRED_VQM_COMPONENT_BY_FORECAST_INPUT[input_label]
            if source_kind == "VQM_COMPONENT"
            else FORECAST_INPUT_NOT_APPLICABLE
        ),
        source_policy_label=(
            REQUIRED_POLICY_LABEL_BY_FORECAST_INPUT[input_label]
            if source_kind == "POLICY_INPUT"
            else FORECAST_INPUT_NOT_APPLICABLE
        ),
        source_contract_hash=source_contract_hash,
        forecast_input_policy_hash=forecast_input_policy_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = ForecastInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(_forecast_input_field_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_position_input_field_contract(
    input_label: str,
    source_contract_hash: str,
    position_input_policy_hash: str,
) -> PositionInputFieldContract:
    source_kind = REQUIRED_SOURCE_KIND_BY_POSITION_INPUT[input_label]
    contract = PositionInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_POSITION_INPUT_STATUS,
        source_kind=source_kind,
        forecast_input_label=POSITION_INPUT_NOT_APPLICABLE,
        forecast_component_family=(
            REQUIRED_FORECAST_COMPONENT_BY_POSITION_INPUT[input_label]
            if source_kind == "FORECAST_COMPONENT"
            else POSITION_INPUT_NOT_APPLICABLE
        ),
        forecast_ledger_output_label=(
            REQUIRED_FORECAST_LEDGER_OUTPUT_BY_POSITION_INPUT[input_label]
            if source_kind == "FORECAST_LEDGER_OUTPUT"
            else POSITION_INPUT_NOT_APPLICABLE
        ),
        rounding_policy_label=(
            REQUIRED_ROUNDING_POLICY_BY_POSITION_INPUT[input_label]
            if source_kind == "ROUNDING_POLICY"
            else POSITION_INPUT_NOT_APPLICABLE
        ),
        position_state_context_label=(
            REQUIRED_POSITION_STATE_CONTEXT_BY_POSITION_INPUT[input_label]
            if source_kind == "POSITION_STATE_CONTEXT"
            else POSITION_INPUT_NOT_APPLICABLE
        ),
        source_policy_label=(
            REQUIRED_POLICY_LABEL_BY_POSITION_INPUT[input_label]
            if source_kind == "POLICY_INPUT"
            else POSITION_INPUT_NOT_APPLICABLE
        ),
        source_contract_hash=source_contract_hash,
        position_input_policy_hash=position_input_policy_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = PositionInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(_position_input_field_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_order_input_field_contract(
    input_label: str,
    source_contract_hash: str,
    order_input_policy_hash: str,
) -> OrderInputFieldContract:
    source_kind = REQUIRED_SOURCE_KIND_BY_ORDER_INPUT[input_label]
    contract = OrderInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_ORDER_INPUT_STATUS,
        source_kind=source_kind,
        position_component_family=(
            REQUIRED_POSITION_COMPONENT_BY_ORDER_INPUT[input_label]
            if source_kind == "POSITION_COMPONENT"
            else ORDER_INPUT_NOT_APPLICABLE
        ),
        position_ledger_output_label=(
            REQUIRED_POSITION_LEDGER_OUTPUT_BY_ORDER_INPUT[input_label]
            if source_kind == "POSITION_LEDGER_OUTPUT"
            else ORDER_INPUT_NOT_APPLICABLE
        ),
        order_kind_label=(
            REQUIRED_ORDER_KIND_BY_ORDER_INPUT[input_label]
            if source_kind == "ORDER_KIND"
            else ORDER_INPUT_NOT_APPLICABLE
        ),
        order_transition_kind_label=(
            REQUIRED_ORDER_TRANSITION_KIND_BY_ORDER_INPUT[input_label]
            if source_kind == "ORDER_TRANSITION_KIND"
            else ORDER_INPUT_NOT_APPLICABLE
        ),
        order_state_context_label=(
            REQUIRED_ORDER_STATE_CONTEXT_BY_ORDER_INPUT[input_label]
            if source_kind == "ORDER_STATE_CONTEXT"
            else ORDER_INPUT_NOT_APPLICABLE
        ),
        source_policy_label=(
            REQUIRED_POLICY_LABEL_BY_ORDER_INPUT[input_label]
            if source_kind == "POLICY_INPUT"
            else ORDER_INPUT_NOT_APPLICABLE
        ),
        source_contract_hash=source_contract_hash,
        order_input_policy_hash=order_input_policy_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = OrderInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(_order_input_field_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_forecast_dependency_binding_contract(
    label: str,
    required_labels: tuple[str, ...],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
) -> ForecastDependencyBindingContract:
    contract = ForecastDependencyBindingContract(
        dependency_label=label,
        required_dependency_labels=required_labels,
        required_dependency_contract_hashes=tuple(dependency_hash_by_label[item] for item in required_labels),
        dependency_binding_policy_hash=_slice4_policy_hash(f"FORECAST_{dependency_kind}_DEPENDENCY_{label}"),
        dependency_binding_contract_hash="0" * 64,
    )
    contract = ForecastDependencyBindingContract(
        **{
            **asdict(contract),
            "dependency_binding_contract_hash": canonical_sha256(
                _forecast_dependency_binding_hash_payload(contract)
            ),
        }
    )
    if dependency_kind == "COMPONENT":
        contract.validate_component()
    elif dependency_kind == "DECISION_BRANCH":
        contract.validate_decision_branch()
    else:
        contract.validate_invariant()
    return contract


def _build_position_dependency_binding_contract(
    label: str,
    required_labels: tuple[str, ...],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
) -> PositionDependencyBindingContract:
    contract = PositionDependencyBindingContract(
        dependency_label=label,
        required_dependency_labels=required_labels,
        required_dependency_contract_hashes=tuple(dependency_hash_by_label[item] for item in required_labels),
        dependency_binding_policy_hash=_slice4_policy_hash(f"POSITION_{dependency_kind}_DEPENDENCY_{label}"),
        dependency_binding_contract_hash="0" * 64,
    )
    contract = PositionDependencyBindingContract(
        **{
            **asdict(contract),
            "dependency_binding_contract_hash": canonical_sha256(
                _position_dependency_binding_hash_payload(contract)
            ),
        }
    )
    if dependency_kind == "COMPONENT":
        contract.validate_component()
    else:
        contract.validate_invariant()
    return contract


def _build_order_dependency_binding_contract(
    label: str,
    required_labels: tuple[str, ...],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
) -> OrderDependencyBindingContract:
    contract = OrderDependencyBindingContract(
        dependency_label=label,
        required_dependency_labels=required_labels,
        required_dependency_contract_hashes=tuple(dependency_hash_by_label[item] for item in required_labels),
        dependency_binding_policy_hash=_slice4_policy_hash(f"ORDER_{dependency_kind}_DEPENDENCY_{label}"),
        dependency_binding_contract_hash="0" * 64,
    )
    contract = OrderDependencyBindingContract(
        **{
            **asdict(contract),
            "dependency_binding_contract_hash": canonical_sha256(_order_dependency_binding_hash_payload(contract)),
        }
    )
    if dependency_kind == "COMPONENT":
        contract.validate_component()
    else:
        contract.validate_invariant()
    return contract


def _build_forecast_component_contract(
    component_family: str,
    dependency_hash_by_label: dict[str, str],
) -> ForecastComponentContract:
    required_labels = REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT[component_family]
    contract = ForecastComponentContract(
        component_family=component_family,
        component_status=PLANNED_FORECAST_COMPONENT_STATUS,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        component_definition_hash=_slice4_policy_hash(f"FORECAST_COMPONENT_DEFINITION_{component_family}"),
        component_policy_hash=_slice4_policy_hash(f"FORECAST_COMPONENT_POLICY_{component_family}"),
        planned_component_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_FORECAST_PLANNED_COMPONENT_OUTPUT",
                "component_family": component_family,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        component_contract_hash="0" * 64,
    )
    contract = ForecastComponentContract(
        **{**asdict(contract), "component_contract_hash": canonical_sha256(_forecast_component_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_forecast_branch_contract(
    branch_label: str,
    dependency_hash_by_label: dict[str, str],
) -> ForecastDecisionBranchContract:
    required_labels = REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH[branch_label]
    contract = ForecastDecisionBranchContract(
        branch_label=branch_label,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        branch_policy_hash=_slice4_policy_hash(f"FORECAST_BRANCH_POLICY_{branch_label}"),
        planned_branch_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_FORECAST_PLANNED_BRANCH_OUTPUT",
                "branch_label": branch_label,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        branch_contract_hash="0" * 64,
    )
    contract = ForecastDecisionBranchContract(
        **{**asdict(contract), "branch_contract_hash": canonical_sha256(_forecast_branch_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_forecast_invariant_contract(
    invariant_label: str,
    dependency_hash_by_label: dict[str, str],
) -> ForecastInvariantContract:
    required_labels = REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT[invariant_label]
    contract = ForecastInvariantContract(
        invariant_label=invariant_label,
        required_proof_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        invariant_policy_hash=_slice4_policy_hash(f"FORECAST_INVARIANT_POLICY_{invariant_label}"),
        invariant_contract_hash="0" * 64,
    )
    contract = ForecastInvariantContract(
        **{
            **asdict(contract),
            "invariant_contract_hash": canonical_sha256(_forecast_invariant_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_position_component_contract(
    component_family: str,
    dependency_hash_by_label: dict[str, str],
) -> PositionComponentContract:
    required_labels = REQUIRED_POSITION_DEPENDENCIES_BY_COMPONENT[component_family]
    contract = PositionComponentContract(
        component_family=component_family,
        component_status=PLANNED_POSITION_COMPONENT_STATUS,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        component_definition_hash=_slice4_policy_hash(f"POSITION_COMPONENT_DEFINITION_{component_family}"),
        component_policy_hash=_slice4_policy_hash(f"POSITION_COMPONENT_POLICY_{component_family}"),
        planned_component_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_POSITION_PLANNED_COMPONENT_OUTPUT",
                "component_family": component_family,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        component_contract_hash="0" * 64,
    )
    contract = PositionComponentContract(
        **{**asdict(contract), "component_contract_hash": canonical_sha256(_position_component_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_position_rounding_policy_contract(
    rounding_label: str,
    source_policy_hash: str,
) -> PositionRoundingPolicyContract:
    contract = PositionRoundingPolicyContract(
        rounding_policy_label=rounding_label,
        source_policy_hash=source_policy_hash,
        rounding_direction_policy_hash=_slice4_policy_hash(f"POSITION_ROUNDING_DIRECTION_{rounding_label}"),
        tie_break_policy_hash=_slice4_policy_hash(f"POSITION_ROUNDING_TIE_BREAK_{rounding_label}"),
        rounding_policy_contract_hash="0" * 64,
    )
    contract = PositionRoundingPolicyContract(
        **{
            **asdict(contract),
            "rounding_policy_contract_hash": canonical_sha256(_position_rounding_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_position_invariant_contract(
    invariant_label: str,
    dependency_hash_by_label: dict[str, str],
) -> PositionInvariantContract:
    required_labels = REQUIRED_POSITION_DEPENDENCIES_BY_INVARIANT[invariant_label]
    contract = PositionInvariantContract(
        invariant_label=invariant_label,
        required_proof_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        invariant_policy_hash=_slice4_policy_hash(f"POSITION_INVARIANT_POLICY_{invariant_label}"),
        invariant_contract_hash="0" * 64,
    )
    contract = PositionInvariantContract(
        **{**asdict(contract), "invariant_contract_hash": canonical_sha256(_position_invariant_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_order_component_contract(
    component_family: str,
    dependency_hash_by_label: dict[str, str],
) -> OrderComponentContract:
    required_labels = REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT[component_family]
    contract = OrderComponentContract(
        component_family=component_family,
        component_status=PLANNED_ORDER_COMPONENT_STATUS,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        component_definition_hash=_slice4_policy_hash(f"ORDER_COMPONENT_DEFINITION_{component_family}"),
        component_policy_hash=_slice4_policy_hash(f"ORDER_COMPONENT_POLICY_{component_family}"),
        planned_component_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_ORDER_PLANNED_COMPONENT_OUTPUT",
                "component_family": component_family,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        component_contract_hash="0" * 64,
    )
    contract = OrderComponentContract(
        **{**asdict(contract), "component_contract_hash": canonical_sha256(_order_component_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_order_kind_contract(
    order_kind_label: str,
    source_policy_hash: str,
) -> OrderKindContract:
    contract = OrderKindContract(
        order_kind_label=order_kind_label,
        required_policy_hashes=(source_policy_hash, _slice4_policy_hash(f"ORDER_KIND_POLICY_{order_kind_label}")),
        order_kind_contract_hash="0" * 64,
    )
    contract = OrderKindContract(
        **{**asdict(contract), "order_kind_contract_hash": canonical_sha256(_order_kind_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _build_order_transition_kind_contract(
    transition_kind_label: str,
    source_policy_hash: str,
) -> OrderTransitionKindContract:
    contract = OrderTransitionKindContract(
        transition_kind_label=transition_kind_label,
        required_policy_hashes=(
            source_policy_hash,
            _slice4_policy_hash(f"ORDER_TRANSITION_KIND_POLICY_{transition_kind_label}"),
        ),
        transition_kind_contract_hash="0" * 64,
    )
    contract = OrderTransitionKindContract(
        **{
            **asdict(contract),
            "transition_kind_contract_hash": canonical_sha256(_order_transition_kind_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_order_invariant_contract(
    invariant_label: str,
    dependency_hash_by_label: dict[str, str],
) -> OrderInvariantContract:
    required_labels = REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT[invariant_label]
    contract = OrderInvariantContract(
        invariant_label=invariant_label,
        required_proof_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        invariant_policy_hash=_slice4_policy_hash(f"ORDER_INVARIANT_POLICY_{invariant_label}"),
        invariant_contract_hash="0" * 64,
    )
    contract = OrderInvariantContract(
        **{**asdict(contract), "invariant_contract_hash": canonical_sha256(_order_invariant_hash_payload(contract))}
    )
    contract.validate()
    return contract


def _validate_forecast_input_contract_local_only(
    contract: ForecastInputContractBundle,
    slice3_artifacts: LocalParserFileReplaySlice3Artifacts,
) -> None:
    if contract.status != S27_V2_FORECAST_INPUT_CONTRACT_ONLY_STATUS:
        raise CarverBlocked("S27 v2 forecast input contract must remain contract-only")
    if contract.source_input_manifest_contract_hash != (
        slice3_artifacts.runtime_history_input_contract.source_input_manifest_contract_hash
    ):
        raise CarverBlocked("S27 v2 forecast input must bind runtime-history source-input manifest")
    if contract.runtime_history_input_contract_hash != (
        slice3_artifacts.runtime_history_input_contract.runtime_history_input_contract_hash
    ):
        raise CarverBlocked("S27 v2 forecast input must bind active runtime-history input")
    if contract.runtime_history_contract_bundle_hash != (
        slice3_artifacts.runtime_history_contract.runtime_history_contract_bundle_hash
    ):
        raise CarverBlocked("S27 v2 forecast input must bind active runtime-history contract")
    expected_policy_hash = _slice4_policy_hash("FORECAST_INPUT")
    if contract.forecast_input_policy_hash != expected_policy_hash:
        raise CarverBlocked("S27 v2 forecast input policy hash must be content-bound")
    active_source_hash_by_label = _forecast_active_source_hash_by_label(
        contract.forecast_input_policy_hash,
        slice3_artifacts.runtime_history_input_contract,
        slice3_artifacts.runtime_history_contract,
    )
    _require_hash_map_exact(
        "S27 v2 forecast expected source contract map",
        contract.expected_source_contract_hash_by_input_label,
        active_source_hash_by_label,
        REQUIRED_FORECAST_INPUTS,
    )
    dependency_hash_by_label = _validate_forecast_input_fields(contract)
    _validate_forecast_dependency_bindings(
        contract.component_dependency_bindings,
        REQUIRED_FORECAST_COMPONENT_FAMILIES,
        REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT,
        dependency_hash_by_label,
        "component",
    )
    _validate_forecast_dependency_bindings(
        contract.decision_branch_dependency_bindings,
        REQUIRED_FORECAST_DECISION_BRANCHES,
        REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH,
        dependency_hash_by_label,
        "decision branch",
    )
    _validate_forecast_dependency_bindings(
        contract.invariant_dependency_bindings,
        REQUIRED_FORECAST_INVARIANTS,
        REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT,
        dependency_hash_by_label,
        "invariant",
        update_dependency_map=False,
    )
    expected_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FORECAST_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.component_dependency_bindings
            ),
            "decision_branch_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.decision_branch_dependency_bindings
            ),
            "input_field_contract_hashes": tuple(
                field.input_field_contract_hash for field in contract.input_field_contracts
            ),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.invariant_dependency_bindings
            ),
            "runtime_history_contract_bundle_hash": contract.runtime_history_contract_bundle_hash,
            "runtime_history_input_contract_hash": contract.runtime_history_input_contract_hash,
        }
    )
    if contract.forecast_input_set_hash != expected_set_hash:
        raise CarverBlocked("S27 v2 forecast input set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FORECAST_INPUT_CONTRACT",
            "forecast_input_policy_hash": contract.forecast_input_policy_hash,
            "forecast_input_set_hash": contract.forecast_input_set_hash,
            "runtime_history_contract_bundle_hash": contract.runtime_history_contract_bundle_hash,
            "runtime_history_input_contract_hash": contract.runtime_history_input_contract_hash,
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.forecast_input_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 forecast input contract hash must be content-bound")


def _validate_forecast_contract_content_bound(
    contract: ForecastContractBundle,
    forecast_input_contract: ForecastInputContractBundle,
    slice3_artifacts: LocalParserFileReplaySlice3Artifacts,
) -> None:
    contract.validate()
    source_binding = contract.source_binding
    if source_binding.runtime_history_contract_bundle_hash != (
        slice3_artifacts.runtime_history_contract.runtime_history_contract_bundle_hash
    ):
        raise CarverBlocked("S27 v2 forecast source binding must bind runtime-history contract")
    if source_binding.source_input_manifest_hash != slice3_artifacts.runtime_history_input_contract.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 forecast source binding must bind source-input manifest")
    if source_binding.runtime_history_ledger_schema_hash != (
        slice3_artifacts.runtime_history_contract.runtime_history_ledger_schema_hash
    ):
        raise CarverBlocked("S27 v2 forecast source binding must bind runtime-history ledger schema")
    if source_binding.forecast_source_binding_hash != canonical_sha256(
        _forecast_source_binding_hash_payload(source_binding)
    ):
        raise CarverBlocked("S27 v2 forecast source binding hash must be content-bound")
    dependency_hash_by_label = _forecast_input_hash_by_label(forecast_input_contract)
    for component in contract.component_contracts:
        if component.required_input_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT[component.component_family]
        ):
            raise CarverBlocked("S27 v2 forecast component must bind active forecast inputs")
        if component.component_contract_hash != canonical_sha256(_forecast_component_hash_payload(component)):
            raise CarverBlocked("S27 v2 forecast component hash must be content-bound")
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    for branch in contract.decision_branch_contracts:
        if branch.required_input_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH[branch.branch_label]
        ):
            raise CarverBlocked("S27 v2 forecast branch must bind active dependencies")
        if branch.branch_contract_hash != canonical_sha256(_forecast_branch_hash_payload(branch)):
            raise CarverBlocked("S27 v2 forecast branch hash must be content-bound")
        dependency_hash_by_label[branch.branch_label] = branch.branch_contract_hash
    for invariant in contract.invariant_contracts:
        if invariant.required_proof_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT[invariant.invariant_label]
        ):
            raise CarverBlocked("S27 v2 forecast invariant must bind active dependencies")
        if invariant.invariant_contract_hash != canonical_sha256(_forecast_invariant_hash_payload(invariant)):
            raise CarverBlocked("S27 v2 forecast invariant hash must be content-bound")
    if contract.scalar_source_lock_hash != forecast_input_contract.forecast_input_policy_hash:
        raise CarverBlocked("S27 v2 forecast scalar source-lock must bind forecast input policy")
    if contract.cap_policy_hash != forecast_input_contract.forecast_input_policy_hash:
        raise CarverBlocked("S27 v2 forecast cap policy must bind forecast input policy")
    if contract.desired_position_link_policy_hash != forecast_input_contract.forecast_input_policy_hash:
        raise CarverBlocked("S27 v2 forecast desired-position link policy must bind forecast input policy")
    if contract.forecast_contract_bundle_hash != canonical_sha256(_forecast_contract_bundle_hash_payload(contract)):
        raise CarverBlocked("S27 v2 forecast contract bundle hash must be content-bound")


def _validate_position_input_contract_local_only(
    contract: PositionInputContractBundle,
    forecast_input_contract: ForecastInputContractBundle,
    forecast_contract: ForecastContractBundle,
) -> None:
    if contract.status != S27_V2_POSITION_INPUT_CONTRACT_ONLY_STATUS:
        raise CarverBlocked("S27 v2 position input contract must remain contract-only")
    if contract.source_input_manifest_contract_hash != forecast_input_contract.source_input_manifest_contract_hash:
        raise CarverBlocked("S27 v2 position input must bind forecast source-input manifest")
    if contract.forecast_input_contract_hash != forecast_input_contract.forecast_input_contract_hash:
        raise CarverBlocked("S27 v2 position input must bind forecast input contract")
    if contract.forecast_contract_bundle_hash != forecast_contract.forecast_contract_bundle_hash:
        raise CarverBlocked("S27 v2 position input must bind active forecast contract")
    expected_policy_hash = _slice4_policy_hash("POSITION_INPUT")
    if contract.position_input_policy_hash != expected_policy_hash:
        raise CarverBlocked("S27 v2 position input policy hash must be content-bound")
    active_source_hash_by_label = _position_active_source_hash_by_label(
        contract.position_input_policy_hash,
        forecast_contract,
    )
    _require_hash_map_exact(
        "S27 v2 position expected source contract map",
        contract.expected_source_contract_hash_by_input_label,
        active_source_hash_by_label,
        REQUIRED_POSITION_INPUTS,
    )
    dependency_hash_by_label = _validate_position_input_fields(contract)
    _validate_position_dependency_bindings(
        contract.component_dependency_bindings,
        REQUIRED_POSITION_COMPONENT_FAMILIES,
        REQUIRED_POSITION_DEPENDENCIES_BY_COMPONENT,
        dependency_hash_by_label,
        "component",
    )
    _validate_position_dependency_bindings(
        contract.invariant_dependency_bindings,
        REQUIRED_POSITION_INVARIANTS,
        REQUIRED_POSITION_DEPENDENCIES_BY_INVARIANT,
        dependency_hash_by_label,
        "invariant",
        update_dependency_map=False,
    )
    expected_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_POSITION_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.component_dependency_bindings
            ),
            "forecast_contract_bundle_hash": contract.forecast_contract_bundle_hash,
            "forecast_input_contract_hash": contract.forecast_input_contract_hash,
            "input_field_contract_hashes": tuple(
                field.input_field_contract_hash for field in contract.input_field_contracts
            ),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.invariant_dependency_bindings
            ),
        }
    )
    if contract.position_input_set_hash != expected_set_hash:
        raise CarverBlocked("S27 v2 position input set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_POSITION_INPUT_CONTRACT",
            "forecast_contract_bundle_hash": contract.forecast_contract_bundle_hash,
            "forecast_input_contract_hash": contract.forecast_input_contract_hash,
            "position_input_policy_hash": contract.position_input_policy_hash,
            "position_input_set_hash": contract.position_input_set_hash,
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.position_input_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 position input contract hash must be content-bound")


def _validate_position_contract_content_bound(
    contract: PositionContractBundle,
    position_input_contract: PositionInputContractBundle,
    forecast_contract: ForecastContractBundle,
) -> None:
    contract.validate()
    if contract.source_binding.forecast_contract_bundle_hash != forecast_contract.forecast_contract_bundle_hash:
        raise CarverBlocked("S27 v2 position source binding must bind forecast contract")
    if contract.source_binding.source_input_manifest_hash != forecast_contract.source_binding.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 position source binding must bind source-input manifest")
    if contract.source_binding.forecast_ledger_schema_hash != forecast_contract.source_binding.forecast_ledger_schema_hash:
        raise CarverBlocked("S27 v2 position source binding must bind forecast ledger schema")
    if contract.source_binding.position_source_binding_hash != canonical_sha256(
        _position_source_binding_hash_payload(contract.source_binding)
    ):
        raise CarverBlocked("S27 v2 position source binding hash must be content-bound")
    dependency_hash_by_label = _position_input_hash_by_label(position_input_contract)
    for component in contract.component_contracts:
        if component.required_input_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_POSITION_DEPENDENCIES_BY_COMPONENT[component.component_family]
        ):
            raise CarverBlocked("S27 v2 position component must bind active position inputs")
        if component.component_contract_hash != canonical_sha256(_position_component_hash_payload(component)):
            raise CarverBlocked("S27 v2 position component hash must be content-bound")
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    for rounding in contract.rounding_policy_contracts:
        if rounding.source_policy_hash != position_input_contract.position_input_policy_hash:
            raise CarverBlocked("S27 v2 rounding policy must bind position input policy")
        if rounding.rounding_policy_contract_hash != canonical_sha256(_position_rounding_hash_payload(rounding)):
            raise CarverBlocked("S27 v2 rounding policy hash must be content-bound")
    for invariant in contract.invariant_contracts:
        if invariant.required_proof_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_POSITION_DEPENDENCIES_BY_INVARIANT[invariant.invariant_label]
        ):
            raise CarverBlocked("S27 v2 position invariant must bind active dependencies")
        if invariant.invariant_contract_hash != canonical_sha256(_position_invariant_hash_payload(invariant)):
            raise CarverBlocked("S27 v2 position invariant hash must be content-bound")
    if contract.forecast_to_position_divisor_policy_hash != position_input_contract.position_input_policy_hash:
        raise CarverBlocked("S27 v2 position divisor policy must bind position input policy")
    if contract.initial_position_policy_hash != position_input_contract.position_input_policy_hash:
        raise CarverBlocked("S27 v2 initial position policy must bind position input policy")
    if contract.desired_position_contract_bundle_hash != canonical_sha256(_position_contract_bundle_hash_payload(contract)):
        raise CarverBlocked("S27 v2 position contract bundle hash must be content-bound")


def _validate_order_input_contract_local_only(
    contract: OrderInputContractBundle,
    position_input_contract: PositionInputContractBundle,
    position_contract: PositionContractBundle,
) -> None:
    if contract.status != S27_V2_ORDER_INPUT_CONTRACT_ONLY_STATUS:
        raise CarverBlocked("S27 v2 order input contract must remain contract-only")
    if contract.source_input_manifest_contract_hash != position_input_contract.source_input_manifest_contract_hash:
        raise CarverBlocked("S27 v2 order input must bind position source-input manifest")
    if contract.position_input_contract_hash != position_input_contract.position_input_contract_hash:
        raise CarverBlocked("S27 v2 order input must bind position input contract")
    if contract.position_contract_bundle_hash != position_contract.desired_position_contract_bundle_hash:
        raise CarverBlocked("S27 v2 order input must bind active position contract")
    expected_policy_hash = _slice4_policy_hash("ORDER_INPUT")
    if contract.order_input_policy_hash != expected_policy_hash:
        raise CarverBlocked("S27 v2 order input policy hash must be content-bound")
    active_source_hash_by_label = _order_active_source_hash_by_label(
        contract.order_input_policy_hash,
        position_contract,
    )
    _require_hash_map_exact(
        "S27 v2 order expected source contract map",
        contract.expected_source_contract_hash_by_input_label,
        active_source_hash_by_label,
        REQUIRED_ORDER_INPUTS,
    )
    dependency_hash_by_label = _validate_order_input_fields(contract)
    _validate_order_dependency_bindings(
        contract.component_dependency_bindings,
        REQUIRED_ORDER_COMPONENT_FAMILIES,
        REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT,
        dependency_hash_by_label,
        "component",
    )
    _validate_order_dependency_bindings(
        contract.invariant_dependency_bindings,
        REQUIRED_ORDER_INVARIANTS,
        REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT,
        dependency_hash_by_label,
        "invariant",
        update_dependency_map=False,
    )
    expected_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_ORDER_INPUT_SET",
            "component_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.component_dependency_bindings
            ),
            "input_field_contract_hashes": tuple(
                field.input_field_contract_hash for field in contract.input_field_contracts
            ),
            "invariant_dependency_binding_hashes": tuple(
                binding.dependency_binding_contract_hash for binding in contract.invariant_dependency_bindings
            ),
            "position_contract_bundle_hash": contract.position_contract_bundle_hash,
            "position_input_contract_hash": contract.position_input_contract_hash,
        }
    )
    if contract.order_input_set_hash != expected_set_hash:
        raise CarverBlocked("S27 v2 order input set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_ORDER_INPUT_CONTRACT",
            "order_input_policy_hash": contract.order_input_policy_hash,
            "order_input_set_hash": contract.order_input_set_hash,
            "position_contract_bundle_hash": contract.position_contract_bundle_hash,
            "position_input_contract_hash": contract.position_input_contract_hash,
            "source_input_manifest_contract_hash": contract.source_input_manifest_contract_hash,
        }
    )
    if contract.order_input_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 order input contract hash must be content-bound")


def _validate_order_contract_content_bound(
    contract: OrderContractBundle,
    order_input_contract: OrderInputContractBundle,
    position_contract: PositionContractBundle,
) -> None:
    contract.validate()
    if contract.source_binding.position_contract_bundle_hash != position_contract.desired_position_contract_bundle_hash:
        raise CarverBlocked("S27 v2 order source binding must bind position contract")
    if contract.source_binding.source_input_manifest_hash != position_contract.source_binding.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 order source binding must bind source-input manifest")
    if contract.source_binding.desired_position_ledger_schema_hash != (
        position_contract.source_binding.desired_position_ledger_schema_hash
    ):
        raise CarverBlocked("S27 v2 order source binding must bind desired-position ledger schema")
    if contract.source_binding.order_source_binding_hash != canonical_sha256(
        _order_source_binding_hash_payload(contract.source_binding)
    ):
        raise CarverBlocked("S27 v2 order source binding hash must be content-bound")
    dependency_hash_by_label = _order_input_hash_by_label(order_input_contract)
    for component in contract.component_contracts:
        if component.required_input_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT[component.component_family]
        ):
            raise CarverBlocked("S27 v2 order component must bind active order inputs")
        if component.component_contract_hash != canonical_sha256(_order_component_hash_payload(component)):
            raise CarverBlocked("S27 v2 order component hash must be content-bound")
        dependency_hash_by_label[component.component_family] = component.component_contract_hash
    for kind in contract.order_kind_contracts:
        if kind.required_policy_hashes[0] != order_input_contract.order_input_policy_hash:
            raise CarverBlocked("S27 v2 order kind must bind order input policy")
        if kind.order_kind_contract_hash != canonical_sha256(_order_kind_hash_payload(kind)):
            raise CarverBlocked("S27 v2 order kind hash must be content-bound")
    for transition_kind in contract.transition_kind_contracts:
        if transition_kind.required_policy_hashes[0] != order_input_contract.order_input_policy_hash:
            raise CarverBlocked("S27 v2 order transition kind must bind order input policy")
        if transition_kind.transition_kind_contract_hash != canonical_sha256(
            _order_transition_kind_hash_payload(transition_kind)
        ):
            raise CarverBlocked("S27 v2 order transition kind hash must be content-bound")
    for invariant in contract.invariant_contracts:
        if invariant.required_proof_hashes != tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT[invariant.invariant_label]
        ):
            raise CarverBlocked("S27 v2 order invariant must bind active dependencies")
        if invariant.invariant_contract_hash != canonical_sha256(_order_invariant_hash_payload(invariant)):
            raise CarverBlocked("S27 v2 order invariant hash must be content-bound")
    if contract.tick_rounding_policy_hash != order_input_contract.order_input_policy_hash:
        raise CarverBlocked("S27 v2 order tick rounding policy must bind order input policy")
    if contract.working_limit_lifecycle_policy_hash != order_input_contract.order_input_policy_hash:
        raise CarverBlocked("S27 v2 order lifecycle policy must bind order input policy")
    if contract.overnight_recompute_policy_hash != order_input_contract.order_input_policy_hash:
        raise CarverBlocked("S27 v2 order overnight policy must bind order input policy")
    if contract.roll_boundary_policy_hash != order_input_contract.order_input_policy_hash:
        raise CarverBlocked("S27 v2 order roll policy must bind order input policy")
    if contract.order_contract_bundle_hash != canonical_sha256(_order_contract_bundle_hash_payload(contract)):
        raise CarverBlocked("S27 v2 order contract bundle hash must be content-bound")


def _validate_forecast_input_fields(contract: ForecastInputContractBundle) -> dict[str, str]:
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_FORECAST_INPUTS:
        raise CarverBlocked("S27 v2 forecast input fields must match locked tuple")
    hash_by_label: dict[str, str] = {}
    for field in contract.input_field_contracts:
        field.validate()
        if field.source_contract_hash != contract.expected_source_contract_hash_by_input_label[field.input_label]:
            raise CarverBlocked("S27 v2 forecast input field must bind active source contract")
        if field.input_field_contract_hash != canonical_sha256(_forecast_input_field_hash_payload(field)):
            raise CarverBlocked("S27 v2 forecast input field hash must be content-bound")
        hash_by_label[field.input_label] = field.input_field_contract_hash
    return hash_by_label


def _validate_position_input_fields(contract: PositionInputContractBundle) -> dict[str, str]:
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_POSITION_INPUTS:
        raise CarverBlocked("S27 v2 position input fields must match locked tuple")
    hash_by_label: dict[str, str] = {}
    for field in contract.input_field_contracts:
        field.validate()
        if field.source_contract_hash != contract.expected_source_contract_hash_by_input_label[field.input_label]:
            raise CarverBlocked("S27 v2 position input field must bind active source contract")
        if field.input_field_contract_hash != canonical_sha256(_position_input_field_hash_payload(field)):
            raise CarverBlocked("S27 v2 position input field hash must be content-bound")
        hash_by_label[field.input_label] = field.input_field_contract_hash
    return hash_by_label


def _validate_order_input_fields(contract: OrderInputContractBundle) -> dict[str, str]:
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_ORDER_INPUTS:
        raise CarverBlocked("S27 v2 order input fields must match locked tuple")
    hash_by_label: dict[str, str] = {}
    for field in contract.input_field_contracts:
        field.validate()
        if field.source_contract_hash != contract.expected_source_contract_hash_by_input_label[field.input_label]:
            raise CarverBlocked("S27 v2 order input field must bind active source contract")
        if field.input_field_contract_hash != canonical_sha256(_order_input_field_hash_payload(field)):
            raise CarverBlocked("S27 v2 order input field hash must be content-bound")
        hash_by_label[field.input_label] = field.input_field_contract_hash
    return hash_by_label


def _validate_fill_input_fields(contract: FillInputContractBundle) -> dict[str, str]:
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_FILL_INPUTS:
        raise CarverBlocked("S27 v2 fill input fields must match locked tuple")
    hash_by_label: dict[str, str] = {}
    for field in contract.input_field_contracts:
        field.validate()
        if field.source_contract_hash != contract.expected_source_contract_hash_by_input_label[field.input_label]:
            raise CarverBlocked("S27 v2 fill input field must bind active source contract")
        if field.input_field_contract_hash != canonical_sha256(_fill_input_field_hash_payload(field)):
            raise CarverBlocked("S27 v2 fill input field hash must be content-bound")
        hash_by_label[field.input_label] = field.input_field_contract_hash
    return hash_by_label


def _validate_cost_input_fields(contract: CostInputContractBundle) -> dict[str, str]:
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_COST_INPUTS:
        raise CarverBlocked("S27 v2 cost input fields must match locked tuple")
    hash_by_label: dict[str, str] = {}
    for field in contract.input_field_contracts:
        field.validate()
        if field.source_contract_hash != contract.expected_source_contract_hash_by_input_label[field.input_label]:
            raise CarverBlocked("S27 v2 cost input field must bind active source contract")
        if field.input_field_contract_hash != canonical_sha256(_cost_input_field_hash_payload(field)):
            raise CarverBlocked("S27 v2 cost input field hash must be content-bound")
        hash_by_label[field.input_label] = field.input_field_contract_hash
    return hash_by_label


def _validate_pnl_input_fields(contract: PnlInputContractBundle) -> dict[str, str]:
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_PNL_INPUTS:
        raise CarverBlocked("S27 v2 PnL input fields must match locked tuple")
    hash_by_label: dict[str, str] = {}
    for field in contract.input_field_contracts:
        field.validate()
        if field.source_contract_hash != contract.expected_source_contract_hash_by_input_label[field.input_label]:
            raise CarverBlocked("S27 v2 PnL input field must bind active source contract")
        if field.input_field_contract_hash != canonical_sha256(_pnl_input_field_hash_payload(field)):
            raise CarverBlocked("S27 v2 PnL input field hash must be content-bound")
        hash_by_label[field.input_label] = field.input_field_contract_hash
    return hash_by_label


def _validate_validation_input_fields(contract: ValidationInputContractBundle) -> dict[str, str]:
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_VALIDATION_INPUTS:
        raise CarverBlocked("S27 v2 validation input fields must match locked tuple")
    hash_by_label: dict[str, str] = {}
    for field in contract.input_field_contracts:
        field.validate()
        if field.source_contract_hash != contract.expected_source_contract_hash_by_input_label[field.input_label]:
            raise CarverBlocked("S27 v2 validation input field must bind active source contract")
        if field.input_field_contract_hash != canonical_sha256(_validation_input_field_hash_payload(field)):
            raise CarverBlocked("S27 v2 validation input field hash must be content-bound")
        hash_by_label[field.input_label] = field.input_field_contract_hash
    return hash_by_label


def _validate_forecast_dependency_bindings(
    bindings: tuple[ForecastDependencyBindingContract, ...],
    required_labels: tuple[str, ...],
    required_dependency_labels_by_label: dict[str, tuple[str, ...]],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
    update_dependency_map: bool = True,
) -> None:
    if tuple(binding.dependency_label for binding in bindings) != required_labels:
        raise CarverBlocked(f"S27 v2 forecast {dependency_kind} dependencies must match locked tuple")
    for binding in bindings:
        if binding.required_dependency_labels != required_dependency_labels_by_label[binding.dependency_label]:
            raise CarverBlocked(f"S27 v2 forecast {dependency_kind} dependency labels must be locked")
        if binding.required_dependency_contract_hashes != tuple(
            dependency_hash_by_label[label] for label in binding.required_dependency_labels
        ):
            raise CarverBlocked(f"S27 v2 forecast {dependency_kind} dependency must bind active dependencies")
        if binding.dependency_binding_contract_hash != canonical_sha256(
            _forecast_dependency_binding_hash_payload(binding)
        ):
            raise CarverBlocked(f"S27 v2 forecast {dependency_kind} dependency hash must be content-bound")
        if update_dependency_map:
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash


def _validate_position_dependency_bindings(
    bindings: tuple[PositionDependencyBindingContract, ...],
    required_labels: tuple[str, ...],
    required_dependency_labels_by_label: dict[str, tuple[str, ...]],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
    update_dependency_map: bool = True,
) -> None:
    if tuple(binding.dependency_label for binding in bindings) != required_labels:
        raise CarverBlocked(f"S27 v2 position {dependency_kind} dependencies must match locked tuple")
    for binding in bindings:
        if binding.required_dependency_labels != required_dependency_labels_by_label[binding.dependency_label]:
            raise CarverBlocked(f"S27 v2 position {dependency_kind} dependency labels must be locked")
        if binding.required_dependency_contract_hashes != tuple(
            dependency_hash_by_label[label] for label in binding.required_dependency_labels
        ):
            raise CarverBlocked(f"S27 v2 position {dependency_kind} dependency must bind active dependencies")
        if binding.dependency_binding_contract_hash != canonical_sha256(
            _position_dependency_binding_hash_payload(binding)
        ):
            raise CarverBlocked(f"S27 v2 position {dependency_kind} dependency hash must be content-bound")
        if update_dependency_map:
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash


def _validate_order_dependency_bindings(
    bindings: tuple[OrderDependencyBindingContract, ...],
    required_labels: tuple[str, ...],
    required_dependency_labels_by_label: dict[str, tuple[str, ...]],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
    update_dependency_map: bool = True,
) -> None:
    if tuple(binding.dependency_label for binding in bindings) != required_labels:
        raise CarverBlocked(f"S27 v2 order {dependency_kind} dependencies must match locked tuple")
    for binding in bindings:
        if binding.required_dependency_labels != required_dependency_labels_by_label[binding.dependency_label]:
            raise CarverBlocked(f"S27 v2 order {dependency_kind} dependency labels must be locked")
        if binding.required_dependency_contract_hashes != tuple(
            dependency_hash_by_label[label] for label in binding.required_dependency_labels
        ):
            raise CarverBlocked(f"S27 v2 order {dependency_kind} dependency must bind active dependencies")
        if binding.dependency_binding_contract_hash != canonical_sha256(_order_dependency_binding_hash_payload(binding)):
            raise CarverBlocked(f"S27 v2 order {dependency_kind} dependency hash must be content-bound")
        if update_dependency_map:
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash


def _validate_fill_dependency_bindings(
    bindings: tuple[FillDependencyBindingContract, ...],
    required_labels: tuple[str, ...],
    required_dependency_labels_by_label: dict[str, tuple[str, ...]],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
    update_dependency_map: bool = True,
) -> None:
    if tuple(binding.dependency_label for binding in bindings) != required_labels:
        raise CarverBlocked(f"S27 v2 fill {dependency_kind} dependencies must match locked tuple")
    for binding in bindings:
        if binding.required_dependency_labels != required_dependency_labels_by_label[binding.dependency_label]:
            raise CarverBlocked(f"S27 v2 fill {dependency_kind} dependency labels must be locked")
        if binding.required_dependency_contract_hashes != tuple(
            dependency_hash_by_label[label] for label in binding.required_dependency_labels
        ):
            raise CarverBlocked(f"S27 v2 fill {dependency_kind} dependency must bind active dependencies")
        if binding.dependency_binding_contract_hash != canonical_sha256(_fill_dependency_binding_hash_payload(binding)):
            raise CarverBlocked(f"S27 v2 fill {dependency_kind} dependency hash must be content-bound")
        if update_dependency_map:
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash


def _validate_cost_dependency_bindings(
    bindings: tuple[CostDependencyBindingContract, ...],
    required_labels: tuple[str, ...],
    required_dependency_labels_by_label: dict[str, tuple[str, ...]],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
    update_dependency_map: bool = True,
) -> None:
    if tuple(binding.dependency_label for binding in bindings) != required_labels:
        raise CarverBlocked(f"S27 v2 cost {dependency_kind} dependencies must match locked tuple")
    binding_hash_by_label = {
        binding.dependency_label: binding.dependency_binding_contract_hash
        for binding in bindings
    }
    for binding in bindings:
        if binding.required_dependency_labels != required_dependency_labels_by_label[binding.dependency_label]:
            raise CarverBlocked(f"S27 v2 cost {dependency_kind} dependency labels must be locked")
        expected_dependency_hashes = tuple(
            dependency_hash_by_label[label]
            if label in dependency_hash_by_label
            else binding_hash_by_label[label]
            for label in binding.required_dependency_labels
        )
        if binding.required_dependency_contract_hashes != expected_dependency_hashes:
            raise CarverBlocked(f"S27 v2 cost {dependency_kind} dependency must bind active dependencies")
        if binding.dependency_binding_contract_hash != canonical_sha256(_cost_dependency_binding_hash_payload(binding)):
            raise CarverBlocked(f"S27 v2 cost {dependency_kind} dependency hash must be content-bound")
        if update_dependency_map:
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash


def _validate_pnl_dependency_bindings(
    bindings: tuple[PnlDependencyBindingContract, ...],
    required_labels: tuple[str, ...],
    required_dependency_labels_by_label: dict[str, tuple[str, ...]],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
    update_dependency_map: bool = True,
) -> None:
    if tuple(binding.dependency_label for binding in bindings) != required_labels:
        raise CarverBlocked(f"S27 v2 PnL {dependency_kind} dependencies must match locked tuple")
    for binding in bindings:
        if binding.required_dependency_labels != required_dependency_labels_by_label[binding.dependency_label]:
            raise CarverBlocked(f"S27 v2 PnL {dependency_kind} dependency labels must be locked")
        if binding.required_dependency_contract_hashes != tuple(
            dependency_hash_by_label[label] for label in binding.required_dependency_labels
        ):
            raise CarverBlocked(f"S27 v2 PnL {dependency_kind} dependency must bind active dependencies")
        if binding.dependency_binding_contract_hash != canonical_sha256(_pnl_dependency_binding_hash_payload(binding)):
            raise CarverBlocked(f"S27 v2 PnL {dependency_kind} dependency hash must be content-bound")
        if update_dependency_map:
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash


def _validate_validation_dependency_bindings(
    bindings: tuple[ValidationDependencyBindingContract, ...],
    required_labels: tuple[str, ...],
    required_dependency_labels_by_label: dict[str, tuple[str, ...]],
    dependency_hash_by_label: dict[str, str],
    dependency_kind: str,
    update_dependency_map: bool = True,
) -> None:
    if tuple(binding.dependency_label for binding in bindings) != required_labels:
        raise CarverBlocked(f"S27 v2 validation {dependency_kind} dependencies must match locked tuple")
    for binding in bindings:
        if binding.required_dependency_labels != required_dependency_labels_by_label[binding.dependency_label]:
            raise CarverBlocked(f"S27 v2 validation {dependency_kind} dependency labels must be locked")
        if binding.required_dependency_contract_hashes != tuple(
            dependency_hash_by_label[label] for label in binding.required_dependency_labels
        ):
            raise CarverBlocked(f"S27 v2 validation {dependency_kind} dependency must bind active dependencies")
        if binding.dependency_binding_contract_hash != canonical_sha256(_validation_dependency_binding_hash_payload(binding)):
            raise CarverBlocked(f"S27 v2 validation {dependency_kind} dependency hash must be content-bound")
        if update_dependency_map:
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash


def _runtime_history_input_hash_by_label(contract: RuntimeHistoryInputContractBundle) -> dict[str, str]:
    by_label = {field.input_label: field.input_field_contract_hash for field in contract.input_field_contracts}
    if tuple(by_label) != REQUIRED_RUNTIME_HISTORY_INPUTS:
        raise CarverBlocked("S27 v2 runtime history input hash map must match locked tuple")
    return by_label


def _forecast_input_hash_by_label(contract: ForecastInputContractBundle) -> dict[str, str]:
    by_label = {field.input_label: field.input_field_contract_hash for field in contract.input_field_contracts}
    if tuple(by_label) != REQUIRED_FORECAST_INPUTS:
        raise CarverBlocked("S27 v2 forecast input hash map must match locked tuple")
    return by_label


def _position_input_hash_by_label(contract: PositionInputContractBundle) -> dict[str, str]:
    by_label = {field.input_label: field.input_field_contract_hash for field in contract.input_field_contracts}
    if tuple(by_label) != REQUIRED_POSITION_INPUTS:
        raise CarverBlocked("S27 v2 position input hash map must match locked tuple")
    return by_label


def _order_input_hash_by_label(contract: OrderInputContractBundle) -> dict[str, str]:
    by_label = {field.input_label: field.input_field_contract_hash for field in contract.input_field_contracts}
    if tuple(by_label) != REQUIRED_ORDER_INPUTS:
        raise CarverBlocked("S27 v2 order input hash map must match locked tuple")
    return by_label


def _fill_input_hash_by_label(contract: FillInputContractBundle) -> dict[str, str]:
    by_label = {field.input_label: field.input_field_contract_hash for field in contract.input_field_contracts}
    if tuple(by_label) != REQUIRED_FILL_INPUTS:
        raise CarverBlocked("S27 v2 fill input hash map must match locked tuple")
    return by_label


def _cost_input_hash_by_label(contract: CostInputContractBundle) -> dict[str, str]:
    by_label = {field.input_label: field.input_field_contract_hash for field in contract.input_field_contracts}
    if tuple(by_label) != REQUIRED_COST_INPUTS:
        raise CarverBlocked("S27 v2 cost input hash map must match locked tuple")
    return by_label


def _pnl_input_hash_by_label(contract: PnlInputContractBundle) -> dict[str, str]:
    by_label = {field.input_label: field.input_field_contract_hash for field in contract.input_field_contracts}
    if tuple(by_label) != REQUIRED_PNL_INPUTS:
        raise CarverBlocked("S27 v2 PnL input hash map must match locked tuple")
    return by_label


def _forecast_component_hash_by_family(contract: ForecastContractBundle) -> dict[str, str]:
    by_family = {item.component_family: item.component_contract_hash for item in contract.component_contracts}
    if tuple(by_family) != REQUIRED_FORECAST_COMPONENT_FAMILIES:
        raise CarverBlocked("S27 v2 forecast component hash map must match locked tuple")
    return by_family


def _position_component_hash_by_family(contract: PositionContractBundle) -> dict[str, str]:
    by_family = {item.component_family: item.component_contract_hash for item in contract.component_contracts}
    if tuple(by_family) != REQUIRED_POSITION_COMPONENT_FAMILIES:
        raise CarverBlocked("S27 v2 position component hash map must match locked tuple")
    return by_family


def _hash_payload_with_null_hash(contract: object, artifact: str, hash_field: str) -> dict[str, object]:
    return {"artifact": artifact, **asdict(contract), hash_field: None}


def _forecast_input_field_hash_payload(contract: ForecastInputFieldContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FORECAST_INPUT_FIELD_CONTRACT", "input_field_contract_hash")


def _position_input_field_hash_payload(contract: PositionInputFieldContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_POSITION_INPUT_FIELD_CONTRACT", "input_field_contract_hash")


def _order_input_field_hash_payload(contract: OrderInputFieldContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_ORDER_INPUT_FIELD_CONTRACT", "input_field_contract_hash")


def _fill_input_field_hash_payload(contract: FillInputFieldContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FILL_INPUT_FIELD_CONTRACT", "input_field_contract_hash")


def _cost_input_field_hash_payload(contract: CostInputFieldContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_COST_INPUT_FIELD_CONTRACT", "input_field_contract_hash")


def _pnl_input_field_hash_payload(contract: PnlInputFieldContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_PNL_INPUT_FIELD_CONTRACT", "input_field_contract_hash")


def _validation_input_field_hash_payload(contract: ValidationInputFieldContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_VALIDATION_INPUT_FIELD_CONTRACT", "input_field_contract_hash")


def _trusted_bundle_input_field_hash_payload(contract: TrustedBundleInputFieldContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_TRUSTED_BUNDLE_INPUT_FIELD_CONTRACT", "input_field_contract_hash")


def _forecast_dependency_binding_hash_payload(contract: ForecastDependencyBindingContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FORECAST_DEPENDENCY_BINDING_CONTRACT", "dependency_binding_contract_hash")


def _position_dependency_binding_hash_payload(contract: PositionDependencyBindingContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_POSITION_DEPENDENCY_BINDING_CONTRACT", "dependency_binding_contract_hash")


def _order_dependency_binding_hash_payload(contract: OrderDependencyBindingContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_ORDER_DEPENDENCY_BINDING_CONTRACT", "dependency_binding_contract_hash")


def _fill_dependency_binding_hash_payload(contract: FillDependencyBindingContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FILL_DEPENDENCY_BINDING_CONTRACT", "dependency_binding_contract_hash")


def _cost_dependency_binding_hash_payload(contract: CostDependencyBindingContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_COST_DEPENDENCY_BINDING_CONTRACT", "dependency_binding_contract_hash")


def _pnl_dependency_binding_hash_payload(contract: PnlDependencyBindingContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_PNL_DEPENDENCY_BINDING_CONTRACT", "dependency_binding_contract_hash")


def _validation_dependency_binding_hash_payload(contract: ValidationDependencyBindingContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_VALIDATION_DEPENDENCY_BINDING_CONTRACT", "dependency_binding_contract_hash")


def _trusted_bundle_dependency_binding_hash_payload(contract: TrustedBundleDependencyBindingContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_TRUSTED_BUNDLE_DEPENDENCY_BINDING_CONTRACT", "dependency_binding_contract_hash")


def _forecast_source_binding_hash_payload(contract: ForecastSourceBinding) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FORECAST_SOURCE_BINDING", "forecast_source_binding_hash")


def _position_source_binding_hash_payload(contract: PositionSourceBinding) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_POSITION_SOURCE_BINDING", "position_source_binding_hash")


def _order_source_binding_hash_payload(contract: OrderSourceBinding) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_ORDER_SOURCE_BINDING", "order_source_binding_hash")


def _fill_source_binding_hash_payload(contract: FillSourceBinding) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FILL_SOURCE_BINDING", "fill_source_binding_hash")


def _cost_source_binding_hash_payload(contract: CostSourceBinding) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_COST_SOURCE_BINDING", "cost_source_binding_hash")


def _pnl_source_binding_hash_payload(contract: PnlSourceBinding) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_PNL_SOURCE_BINDING", "pnl_source_binding_hash")


def _validation_source_binding_hash_payload(contract: ValidationSourceBinding) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_VALIDATION_SOURCE_BINDING", "validation_source_binding_hash")


def _forecast_component_hash_payload(contract: ForecastComponentContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FORECAST_COMPONENT_CONTRACT", "component_contract_hash")


def _forecast_branch_hash_payload(contract: ForecastDecisionBranchContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FORECAST_DECISION_BRANCH_CONTRACT", "branch_contract_hash")


def _forecast_invariant_hash_payload(contract: ForecastInvariantContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FORECAST_INVARIANT_CONTRACT", "invariant_contract_hash")


def _position_component_hash_payload(contract: PositionComponentContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_POSITION_COMPONENT_CONTRACT", "component_contract_hash")


def _position_rounding_hash_payload(contract: PositionRoundingPolicyContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_POSITION_ROUNDING_POLICY_CONTRACT", "rounding_policy_contract_hash")


def _position_invariant_hash_payload(contract: PositionInvariantContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_POSITION_INVARIANT_CONTRACT", "invariant_contract_hash")


def _order_component_hash_payload(contract: OrderComponentContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_ORDER_COMPONENT_CONTRACT", "component_contract_hash")


def _order_kind_hash_payload(contract: OrderKindContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_ORDER_KIND_CONTRACT", "order_kind_contract_hash")


def _order_transition_kind_hash_payload(contract: OrderTransitionKindContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_ORDER_TRANSITION_KIND_CONTRACT", "transition_kind_contract_hash")


def _order_invariant_hash_payload(contract: OrderInvariantContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_ORDER_INVARIANT_CONTRACT", "invariant_contract_hash")


def _fill_component_hash_payload(contract: FillComponentContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FILL_COMPONENT_CONTRACT", "component_contract_hash")


def _cost_component_hash_payload(contract: CostComponentContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_COST_COMPONENT_CONTRACT", "component_contract_hash")


def _pnl_component_hash_payload(contract: PnlComponentContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_PNL_COMPONENT_CONTRACT", "component_contract_hash")


def _validation_component_hash_payload(contract: ValidationComponentContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_VALIDATION_COMPONENT_CONTRACT", "component_contract_hash")


def _fill_price_provenance_hash_payload(contract: FillPriceProvenanceContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FILL_PRICE_PROVENANCE_CONTRACT", "provenance_contract_hash")


def _fill_branch_hash_payload(contract: FillBranchContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FILL_BRANCH_CONTRACT", "branch_contract_hash")


def _cost_branch_hash_payload(contract: CostBranchContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_COST_BRANCH_CONTRACT", "branch_contract_hash")


def _spread_space_hash_payload(contract: SpreadSpaceContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_SPREAD_SPACE_CONTRACT", "spread_space_contract_hash")


def _pnl_price_source_hash_payload(contract: PnlPriceSourceContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_PNL_PRICE_SOURCE_CONTRACT", "price_source_contract_hash")


def _pnl_bridge_hash_payload(contract: PnlBridgeContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_PNL_BRIDGE_CONTRACT", "bridge_contract_hash")


def _validation_ledger_hash_payload(contract: ValidationLedgerContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_VALIDATION_LEDGER_CONTRACT", "ledger_contract_hash")


def _validation_audit_checkpoint_hash_payload(contract: ValidationAuditCheckpointContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(
        contract,
        "S27_V2_VALIDATION_AUDIT_CHECKPOINT_CONTRACT",
        "audit_checkpoint_contract_hash",
    )


def _fill_invariant_hash_payload(contract: FillInvariantContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_FILL_INVARIANT_CONTRACT", "invariant_contract_hash")


def _cost_invariant_hash_payload(contract: CostInvariantContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_COST_INVARIANT_CONTRACT", "invariant_contract_hash")


def _pnl_invariant_hash_payload(contract: PnlInvariantContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_PNL_INVARIANT_CONTRACT", "invariant_contract_hash")


def _validation_invariant_hash_payload(contract: ValidationInvariantContract) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_VALIDATION_INVARIANT_CONTRACT", "invariant_contract_hash")


def _forecast_contract_bundle_hash_payload(contract: ForecastContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_FORECAST_CONTRACT_BUNDLE",
        "cap_policy_hash": contract.cap_policy_hash,
        "component_contract_hashes": tuple(item.component_contract_hash for item in contract.component_contracts),
        "decision_branch_contract_hashes": tuple(
            item.branch_contract_hash for item in contract.decision_branch_contracts
        ),
        "desired_position_link_policy_hash": contract.desired_position_link_policy_hash,
        "invariant_contract_hashes": tuple(item.invariant_contract_hash for item in contract.invariant_contracts),
        "scalar_source_lock_hash": contract.scalar_source_lock_hash,
        "source_binding_hash": contract.source_binding.forecast_source_binding_hash,
        "status": contract.status,
    }


def _position_contract_bundle_hash_payload(contract: PositionContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_POSITION_CONTRACT_BUNDLE",
        "component_contract_hashes": tuple(item.component_contract_hash for item in contract.component_contracts),
        "forecast_to_position_divisor_policy_hash": contract.forecast_to_position_divisor_policy_hash,
        "initial_position_policy_hash": contract.initial_position_policy_hash,
        "invariant_contract_hashes": tuple(item.invariant_contract_hash for item in contract.invariant_contracts),
        "rounding_policy_contract_hashes": tuple(
            item.rounding_policy_contract_hash for item in contract.rounding_policy_contracts
        ),
        "source_binding_hash": contract.source_binding.position_source_binding_hash,
        "status": contract.status,
    }


def _order_contract_bundle_hash_payload(contract: OrderContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_ORDER_CONTRACT_BUNDLE",
        "component_contract_hashes": tuple(item.component_contract_hash for item in contract.component_contracts),
        "invariant_contract_hashes": tuple(item.invariant_contract_hash for item in contract.invariant_contracts),
        "order_kind_contract_hashes": tuple(item.order_kind_contract_hash for item in contract.order_kind_contracts),
        "overnight_recompute_policy_hash": contract.overnight_recompute_policy_hash,
        "roll_boundary_policy_hash": contract.roll_boundary_policy_hash,
        "source_binding_hash": contract.source_binding.order_source_binding_hash,
        "status": contract.status,
        "tick_rounding_policy_hash": contract.tick_rounding_policy_hash,
        "transition_kind_contract_hashes": tuple(
            item.transition_kind_contract_hash for item in contract.transition_kind_contracts
        ),
        "working_limit_lifecycle_policy_hash": contract.working_limit_lifecycle_policy_hash,
    }


def _fill_contract_bundle_hash_payload(contract: FillContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_FILL_CONTRACT_BUNDLE",
        "branch_contract_hashes": tuple(item.branch_contract_hash for item in contract.branch_contracts),
        "component_contract_hashes": tuple(item.component_contract_hash for item in contract.component_contracts),
        "fill_source_binding_hash": contract.source_binding.fill_source_binding_hash,
        "invariant_contract_hashes": tuple(item.invariant_contract_hash for item in contract.invariant_contracts),
        "one_hour_lag_policy_hash": contract.one_hour_lag_policy_hash,
        "price_provenance_contract_hashes": tuple(
            item.provenance_contract_hash for item in contract.price_provenance_contracts
        ),
        "session_gap_policy_hash": contract.session_gap_policy_hash,
        "status": contract.status,
    }


def _cost_contract_bundle_hash_payload(contract: CostContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_COST_CONTRACT_BUNDLE",
        "branch_contract_hashes": tuple(item.branch_contract_hash for item in contract.branch_contracts),
        "commission_policy_hash": contract.commission_policy_hash,
        "component_contract_hashes": tuple(item.component_contract_hash for item in contract.component_contracts),
        "contract_multiplier_policy_hash": contract.contract_multiplier_policy_hash,
        "cost_calculation_policy_hash": contract.cost_calculation_policy_hash,
        "currency_conversion_policy_hash": contract.currency_conversion_policy_hash,
        "deflation_policy_hash": contract.deflation_policy_hash,
        "invariant_contract_hashes": tuple(item.invariant_contract_hash for item in contract.invariant_contracts),
        "source_binding_hash": contract.source_binding.cost_source_binding_hash,
        "spread_policy_hash": contract.spread_policy_hash,
        "spread_space_contract_hashes": tuple(
            item.spread_space_contract_hash for item in contract.spread_space_contracts
        ),
        "status": contract.status,
    }


def _pnl_contract_bundle_hash_payload(contract: PnlContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_PNL_CONTRACT_BUNDLE",
        "bridge_contract_hashes": tuple(item.bridge_contract_hash for item in contract.bridge_contracts),
        "close_price_source_policy_hash": contract.close_price_source_policy_hash,
        "component_contract_hashes": tuple(item.component_contract_hash for item in contract.component_contracts),
        "contract_multiplier_policy_hash": contract.contract_multiplier_policy_hash,
        "cost_application_policy_hash": contract.cost_application_policy_hash,
        "currency_policy_hash": contract.currency_policy_hash,
        "invariant_contract_hashes": tuple(item.invariant_contract_hash for item in contract.invariant_contracts),
        "pnl_formula_policy_hash": contract.pnl_formula_policy_hash,
        "price_source_contract_hashes": tuple(
            item.price_source_contract_hash for item in contract.price_source_contracts
        ),
        "source_binding_hash": contract.source_binding.pnl_source_binding_hash,
        "status": contract.status,
        "target_position_shortcut_quarantine_policy_hash": (
            contract.target_position_shortcut_quarantine_policy_hash
        ),
    }


def _construction_phase_hash_payload(contract: ConstructionPhaseBoundary) -> dict[str, object]:
    return _hash_payload_with_null_hash(contract, "S27_V2_CONSTRUCTION_PHASE_BOUNDARY", "phase_contract_hash")


def _construction_contract_hash_payload(contract: ParserFileReplayConstructionContract) -> dict[str, object]:
    return {
        "artifact": "S27_V2_PARSER_FILE_REPLAY_CONSTRUCTION_CONTRACT",
        "artifact_manifest_plan_hash": contract.artifact_manifest_plan_hash,
        "construction_phase_hashes": tuple(phase.phase_contract_hash for phase in contract.construction_phases),
        "input_directory_declaration_hash": contract.input_directory_declaration_hash,
        "parser_plan_bundle_hash": contract.parser_plan_bundle_hash,
        "planning_config_hash": contract.planning_config_hash,
        "status": contract.status,
    }


def _validation_input_contract_hash_payload(contract: ValidationInputContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_VALIDATION_INPUT_CONTRACT",
        "pnl_contract_bundle_hash": contract.pnl_contract_bundle_hash,
        "pnl_input_contract_hash": contract.pnl_input_contract_hash,
        "validation_input_policy_hash": contract.validation_input_policy_hash,
        "validation_input_set_hash": contract.validation_input_set_hash,
    }


def _validation_contract_bundle_hash_payload(contract: ValidationContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_VALIDATION_CONTRACT_BUNDLE",
        "audit_checkpoint_contract_hashes": tuple(
            item.audit_checkpoint_contract_hash for item in contract.audit_checkpoint_contracts
        ),
        "component_contract_hashes": tuple(item.component_contract_hash for item in contract.component_contracts),
        "external_audit_packet_policy_hash": contract.external_audit_packet_policy_hash,
        "fail_closed_gate_policy_hash": contract.fail_closed_gate_policy_hash,
        "invariant_contract_hashes": tuple(item.invariant_contract_hash for item in contract.invariant_contracts),
        "ledger_contract_hashes": tuple(item.ledger_contract_hash for item in contract.ledger_contracts),
        "local_hostile_audit_policy_hash": contract.local_hostile_audit_policy_hash,
        "provenance_hash_chain_policy_hash": contract.provenance_hash_chain_policy_hash,
        "required_artifact_family_policy_hash": contract.required_artifact_family_policy_hash,
        "required_unresolved_gate_labels": contract.required_unresolved_gate_labels,
        "source_binding_hash": contract.source_binding.validation_source_binding_hash,
        "stale_evidence_supersession_policy_hash": contract.stale_evidence_supersession_policy_hash,
        "status": contract.status,
    }


def _trusted_bundle_contract_hash_payload(contract: TrustedBundleContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_TRUSTED_BUNDLE_CONTRACT",
        "trusted_bundle_input_set_hash": contract.trusted_bundle_input_set_hash,
        "trusted_bundle_policy_hash": contract.trusted_bundle_policy_hash,
    }


def _fill_branch_input_label(branch_label: str) -> str:
    if branch_label == "LIMIT_FILL":
        return "FILL_LIMIT_BRANCH_INPUT"
    if branch_label == "MARKET_FILL":
        return "FILL_MARKET_BRANCH_INPUT"
    raise CarverBlocked("S27 v2 fill branch label cannot be mapped to input")


def _cost_branch_input_label(branch_label: str) -> str:
    if branch_label == "LIMIT_COMMISSION_ONLY":
        return "COST_LIMIT_COMMISSION_ONLY_BRANCH_INPUT"
    if branch_label == "MARKET_COMMISSION_PLUS_SPREAD":
        return "COST_MARKET_COMMISSION_PLUS_SPREAD_BRANCH_INPUT"
    raise CarverBlocked("S27 v2 cost branch label cannot be mapped to input")


def _pnl_bridge_input_label(bridge_label: str) -> str:
    if bridge_label == "RAW_SYMBOL_CONTINUITY":
        return "PNL_RAW_SYMBOL_CONTINUITY_INPUT"
    if bridge_label == "ROLL_BRIDGE":
        return "PNL_ROLL_BRIDGE_INPUT"
    raise CarverBlocked("S27 v2 PnL bridge label cannot be mapped to input")


def _build_raw_source_file_hash_binding(
    parsed: ParsedDeclaredSourceFile,
    parser_family_plan_hash: str,
) -> RawSourceFileHashBinding:
    payload = {
        "artifact": "S27_V2_RAW_SOURCE_FILE_HASH_BINDING",
        "file_family": parsed.row_family,
        "file_sha256": parsed.file_sha256,
        "local_file_declaration_hash": canonical_sha256(parsed.declaration.local_file),
        "parser_family_plan_hash": parser_family_plan_hash,
    }
    binding = RawSourceFileHashBinding(
        file_family=parsed.row_family,
        family_status=PLANNED_RAW_FILE_HASH_FAMILY_STATUS,
        local_file_declaration_hash=canonical_sha256(parsed.declaration.local_file),
        declared_path_label_hash=canonical_sha256(
            {
                "artifact": "S27_V2_DECLARED_PATH_LABEL",
                "declared_path": parsed.declaration.local_file.declared_path,
            }
        ),
        file_sha256=parsed.file_sha256,
        parser_family_plan_hash=parser_family_plan_hash,
        expected_output_row_family=parsed.row_family,
        completed_bar_policy_hash=parsed.declaration.completed_bar_policy_hash,
        no_provider_no_download_assertion_label=(
            parsed.declaration.local_file.no_provider_no_download_assertion_label
        ),
        file_hash_binding_hash=canonical_sha256(payload),
    )
    binding.validate()
    return binding


def _build_parser_output_family_contract(
    parsed: ParsedDeclaredSourceFile,
    raw_binding: RawSourceFileHashBinding,
    row_locator_family_contract_hash: str,
    canonical_policy: CanonicalSerializationPolicy,
) -> ParserOutputFamilyContract:
    row_ordering_policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_ROW_ORDERING_POLICY",
            "row_family": parsed.row_family,
            "row_locators": tuple(row.row_locator for row in parsed.rows),
        }
    )
    family_hash = canonical_sha256(
        {
            "artifact": "S27_V2_PARSER_OUTPUT_FAMILY_CONTRACT",
            "planned_row_batch_hash": parsed.parsed_output_batch_hash,
            "raw_file_hash_binding_hash": raw_binding.file_hash_binding_hash,
            "row_family": parsed.row_family,
        }
    )
    contract = ParserOutputFamilyContract(
        row_family=parsed.row_family,
        family_status=PLANNED_PARSER_OUTPUT_FAMILY_STATUS,
        raw_file_hash_binding_hash=raw_binding.file_hash_binding_hash,
        parser_family_plan_hash=raw_binding.parser_family_plan_hash,
        expected_source_row_schema_family=parsed.row_family,
        row_locator_family_contract_hash=row_locator_family_contract_hash,
        planned_row_batch_hash=parsed.parsed_output_batch_hash,
        row_hash_schema_hash=canonical_sha256(
            {
                "artifact": "S27_V2_ROW_HASH_SCHEMA",
                "row_family": parsed.row_family,
                "canonical_policy_hash": canonical_policy.canonical_serialization_policy_hash,
            }
        ),
        row_ordering_policy_hash=row_ordering_policy_hash,
        completed_bar_policy_hash=parsed.declaration.completed_bar_policy_hash,
        strict_prior_policy_hash=parsed.declaration.strict_prior_policy_hash,
        no_future_rows_proof_hash=_no_future_rows_proof_hash(parsed.rows),
        no_parser_execution_assertion_label="NO_PARSER_FILE_REPLAY_EXECUTION",
        parser_output_family_contract_hash=family_hash,
    )
    contract.validate()
    return contract


def _build_source_row_batch_family_contract(
    parsed: ParsedDeclaredSourceFile,
    parser_output_family: ParserOutputFamilyContract,
    source_universe_family_contract_hash: str,
    row_locator_family_contract_hash: str,
) -> SourceRowBatchFamilyContract:
    row_count_manifest_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_ROW_COUNT_MANIFEST",
            "row_count": len(parsed.rows),
            "row_family": parsed.row_family,
        }
    )
    first_last_row_locator_manifest_hash = canonical_sha256(
        {
            "artifact": "S27_V2_FIRST_LAST_ROW_LOCATOR_MANIFEST",
            "first_row_locator": parsed.rows[0].row_locator,
            "last_row_locator": parsed.rows[-1].row_locator,
            "row_family": parsed.row_family,
        }
    )
    family_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_ROW_BATCH_FAMILY_CONTRACT",
            "parser_output_family_contract_hash": parser_output_family.parser_output_family_contract_hash,
            "source_row_batch_hash": parsed.parsed_output_batch_hash,
            "row_family": parsed.row_family,
        }
    )
    contract = SourceRowBatchFamilyContract(
        row_family=parsed.row_family,
        family_status=PLANNED_SOURCE_ROW_BATCH_FAMILY_STATUS,
        parser_output_family_contract_hash=parser_output_family.parser_output_family_contract_hash,
        parser_output_batch_hash=parser_output_family.planned_row_batch_hash,
        source_row_schema_label=REQUIRED_SOURCE_ROW_SCHEMA_BY_FAMILY[parsed.row_family],
        source_row_schema_hash=canonical_sha256(
            {
                "artifact": "S27_V2_SOURCE_ROW_SCHEMA",
                "schema_label": REQUIRED_SOURCE_ROW_SCHEMA_BY_FAMILY[parsed.row_family],
            }
        ),
        readiness_status_label=REQUIRED_READINESS_STATUS_BY_FAMILY[parsed.row_family],
        readiness_status_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_READINESS_STATUS_POLICY",
                "readiness_status": REQUIRED_READINESS_STATUS_BY_FAMILY[parsed.row_family],
                "row_family": parsed.row_family,
            }
        ),
        source_universe_family_contract_hash=source_universe_family_contract_hash,
        row_locator_family_contract_hash=row_locator_family_contract_hash,
        row_locator_policy_hash=parsed.declaration.row_locator_policy_hash,
        row_hash_schema_hash=parser_output_family.row_hash_schema_hash,
        row_ordering_policy_hash=parser_output_family.row_ordering_policy_hash,
        duplicate_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_DUPLICATE_POLICY_PROOF",
                "row_family": parsed.row_family,
                "unique_row_hashes": parsed.row_hashes,
            }
        ),
        missing_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_MISSING_POLICY_PROOF",
                "row_count": len(parsed.rows),
                "row_family": parsed.row_family,
            }
        ),
        completed_bar_policy_hash=parsed.declaration.completed_bar_policy_hash,
        strict_prior_policy_hash=parsed.declaration.strict_prior_policy_hash,
        no_future_rows_proof_hash=parser_output_family.no_future_rows_proof_hash,
        row_count_manifest_hash=row_count_manifest_hash,
        first_last_row_locator_manifest_hash=first_last_row_locator_manifest_hash,
        source_row_batch_hash=parsed.parsed_output_batch_hash,
        source_row_batch_family_contract_hash=family_contract_hash,
    )
    contract.validate()
    return contract


def _build_source_input_role_selection_contract(
    role: str,
    family_contract: SourceRowBatchFamilyContract,
    source_row_selection_authority: SourceRowSelectionAuthorityContract,
) -> SourceInputRoleSelectionContract:
    family = REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[role]
    if family_contract.row_family != family:
        raise CarverBlocked("S27 v2 source input role builder must use locked row family")
    row_selector_policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_ROW_SELECTOR_POLICY",
            "input_role": role,
            "selection_rule": "FIRST_COMPLETED_LOCAL_ROW_PER_LOCKED_INPUT_ROLE_FOR_CONSTRUCTION_SCAFFOLD_ONLY",
            "source_row_family": family,
        }
    )
    row_locator_policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_ROW_LOCATOR_POLICY",
            "input_role": role,
            "row_locator_family_contract_hash": family_contract.row_locator_family_contract_hash,
            "source_row_family": family,
        }
    )
    selected_row_timestamp_policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_SELECTED_ROW_TIMESTAMP_POLICY",
            "input_role": role,
            "completed_bar_policy_hash": family_contract.completed_bar_policy_hash,
            "strict_prior_policy_hash": family_contract.strict_prior_policy_hash,
        }
    )
    contract = SourceInputRoleSelectionContract(
        input_role=role,
        role_status=PLANNED_SOURCE_INPUT_ROLE_STATUS,
        source_row_family=family,
        source_row_batch_family_contract_hash=family_contract.source_row_batch_family_contract_hash,
        source_row_batch_hash=family_contract.source_row_batch_hash,
        row_selector_policy_hash=row_selector_policy_hash,
        row_locator_policy_hash=row_locator_policy_hash,
        selected_row_locator_hash=source_row_selection_authority.selected_row_locator_hash_by_input_role[role],
        selected_row_hash=source_row_selection_authority.selected_row_hash_by_input_role[role],
        selected_row_membership_proof_hash=(
            source_row_selection_authority.selected_row_membership_proof_hash_by_input_role[role]
        ),
        selected_row_locator_membership_proof_hash=(
            source_row_selection_authority.selected_row_locator_membership_proof_hash_by_input_role[role]
        ),
        selected_row_timestamp_policy_hash=selected_row_timestamp_policy_hash,
        completed_bar_policy_hash=family_contract.completed_bar_policy_hash,
        strict_prior_policy_hash=family_contract.strict_prior_policy_hash,
        no_future_rows_proof_hash=family_contract.no_future_rows_proof_hash,
        source_input_role_contract_hash="0" * 64,
    )
    contract = SourceInputRoleSelectionContract(
        **{
            **asdict(contract),
            "source_input_role_contract_hash": canonical_sha256(
                _source_input_role_contract_hash_payload(contract)
            ),
        }
    )
    contract.validate()
    _validate_source_input_role_selection_contract_content_bound(contract)
    return contract


def _build_source_input_manifest_field_contract(
    manifest_field: str,
    role_contract: SourceInputRoleSelectionContract,
) -> SourceInputManifestFieldContract:
    if role_contract.input_role != REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[manifest_field]:
        raise CarverBlocked("S27 v2 source input manifest field builder must use locked role")
    manifest_field_policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST_FIELD_POLICY",
            "manifest_field": manifest_field,
            "source_input_role": role_contract.input_role,
        }
    )
    canonical_field_serialization_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST_CANONICAL_FIELD_SERIALIZATION",
            "manifest_field": manifest_field,
            "selected_row_hash": role_contract.selected_row_hash,
            "selected_row_locator_hash": role_contract.selected_row_locator_hash,
        }
    )
    contract_hash = canonical_sha256(
        _source_input_manifest_field_contract_hash_payload(
            SourceInputManifestFieldContract(
                manifest_field=manifest_field,
                field_status=PLANNED_SOURCE_INPUT_MANIFEST_FIELD_STATUS,
                source_input_role=role_contract.input_role,
                source_input_role_contract_hash=role_contract.source_input_role_contract_hash,
                selected_row_hash=role_contract.selected_row_hash,
                selected_row_locator_hash=role_contract.selected_row_locator_hash,
                manifest_field_policy_hash=manifest_field_policy_hash,
                canonical_field_serialization_hash=canonical_field_serialization_hash,
                completed_bar_policy_hash=role_contract.completed_bar_policy_hash,
                strict_prior_policy_hash=role_contract.strict_prior_policy_hash,
                no_future_rows_proof_hash=role_contract.no_future_rows_proof_hash,
                manifest_field_contract_hash="0" * 64,
            )
        )
    )
    contract = SourceInputManifestFieldContract(
        manifest_field=manifest_field,
        field_status=PLANNED_SOURCE_INPUT_MANIFEST_FIELD_STATUS,
        source_input_role=role_contract.input_role,
        source_input_role_contract_hash=role_contract.source_input_role_contract_hash,
        selected_row_hash=role_contract.selected_row_hash,
        selected_row_locator_hash=role_contract.selected_row_locator_hash,
        manifest_field_policy_hash=manifest_field_policy_hash,
        canonical_field_serialization_hash=canonical_field_serialization_hash,
        completed_bar_policy_hash=role_contract.completed_bar_policy_hash,
        strict_prior_policy_hash=role_contract.strict_prior_policy_hash,
        no_future_rows_proof_hash=role_contract.no_future_rows_proof_hash,
        manifest_field_contract_hash=contract_hash,
    )
    contract.validate()
    _validate_source_input_manifest_field_contract_content_bound(contract)
    return contract


def _source_input_role_contract_hash_payload(
    contract: SourceInputRoleSelectionContract,
) -> dict[str, object]:
    return {
        "artifact": "S27_V2_SOURCE_INPUT_ROLE_SELECTION_CONTRACT",
        "completed_bar_policy_hash": contract.completed_bar_policy_hash,
        "input_role": contract.input_role,
        "no_future_rows_proof_hash": contract.no_future_rows_proof_hash,
        "role_status": contract.role_status,
        "row_locator_policy_hash": contract.row_locator_policy_hash,
        "row_selector_policy_hash": contract.row_selector_policy_hash,
        "selected_row_hash": contract.selected_row_hash,
        "selected_row_locator_hash": contract.selected_row_locator_hash,
        "selected_row_locator_membership_proof_hash": contract.selected_row_locator_membership_proof_hash,
        "selected_row_membership_proof_hash": contract.selected_row_membership_proof_hash,
        "selected_row_timestamp_policy_hash": contract.selected_row_timestamp_policy_hash,
        "source_row_batch_family_contract_hash": contract.source_row_batch_family_contract_hash,
        "source_row_batch_hash": contract.source_row_batch_hash,
        "source_row_family": contract.source_row_family,
        "strict_prior_policy_hash": contract.strict_prior_policy_hash,
    }


def _source_input_manifest_field_contract_hash_payload(
    contract: SourceInputManifestFieldContract,
) -> dict[str, object]:
    return {
        "artifact": "S27_V2_SOURCE_INPUT_MANIFEST_FIELD_CONTRACT",
        "canonical_field_serialization_hash": contract.canonical_field_serialization_hash,
        "completed_bar_policy_hash": contract.completed_bar_policy_hash,
        "field_status": contract.field_status,
        "manifest_field": contract.manifest_field,
        "manifest_field_policy_hash": contract.manifest_field_policy_hash,
        "no_future_rows_proof_hash": contract.no_future_rows_proof_hash,
        "selected_row_hash": contract.selected_row_hash,
        "selected_row_locator_hash": contract.selected_row_locator_hash,
        "source_input_role": contract.source_input_role,
        "source_input_role_contract_hash": contract.source_input_role_contract_hash,
        "strict_prior_policy_hash": contract.strict_prior_policy_hash,
    }


def _build_level_compatibility_input_field_contract(
    input_label: str,
    manifest_field_contract: SourceInputManifestFieldContract,
) -> LevelCompatibilityInputFieldContract:
    manifest_field = REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
    if manifest_field_contract.manifest_field != manifest_field:
        raise CarverBlocked("S27 v2 level compatibility input builder must use locked manifest field")
    contract = LevelCompatibilityInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_LEVEL_COMPATIBILITY_INPUT_STATUS,
        source_input_manifest_field=manifest_field,
        source_input_role=manifest_field_contract.source_input_role,
        source_input_manifest_field_contract_hash=manifest_field_contract.manifest_field_contract_hash,
        selected_row_hash=manifest_field_contract.selected_row_hash,
        selected_row_locator_hash=manifest_field_contract.selected_row_locator_hash,
        level_compatibility_input_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_FIELD_POLICY",
                "input_label": input_label,
                "manifest_field": manifest_field,
            }
        ),
        price_level_space_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_LEVEL_COMPATIBILITY_PRICE_LEVEL_SPACE_POLICY",
                "input_label": input_label,
                "manifest_field": manifest_field,
            }
        ),
        completed_bar_policy_hash=manifest_field_contract.completed_bar_policy_hash,
        strict_prior_policy_hash=manifest_field_contract.strict_prior_policy_hash,
        no_future_rows_proof_hash=manifest_field_contract.no_future_rows_proof_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = LevelCompatibilityInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(
                _level_compatibility_input_field_hash_payload(contract)
            ),
        }
    )
    contract.validate()
    return contract


def _build_level_compatibility_proof_input_binding_contract(
    proof_label: str,
    input_hash_by_label: dict[str, str],
) -> LevelCompatibilityProofInputBindingContract:
    required_input_labels = REQUIRED_LEVEL_COMPATIBILITY_INPUTS_BY_PROOF[proof_label]
    contract = LevelCompatibilityProofInputBindingContract(
        proof_label=proof_label,
        required_input_labels=required_input_labels,
        required_input_field_contract_hashes=tuple(
            input_hash_by_label[label]
            for label in required_input_labels
        ),
        proof_input_binding_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_LEVEL_COMPATIBILITY_PROOF_INPUT_BINDING_POLICY",
                "proof_label": proof_label,
                "required_input_labels": required_input_labels,
            }
        ),
        proof_input_binding_contract_hash="0" * 64,
    )
    contract = LevelCompatibilityProofInputBindingContract(
        **{
            **asdict(contract),
            "proof_input_binding_contract_hash": canonical_sha256(
                _level_compatibility_proof_input_binding_hash_payload(contract)
            ),
        }
    )
    contract.validate()
    return contract


def _build_level_compatibility_proof_contract(
    proof_label: str,
    input_hash_by_label: dict[str, str],
) -> LevelCompatibilityProofContract:
    required_input_labels = REQUIRED_LEVEL_COMPATIBILITY_INPUTS_BY_PROOF[proof_label]
    contract = LevelCompatibilityProofContract(
        proof_label=proof_label,
        proof_status=PLANNED_LEVEL_COMPATIBILITY_PROOF_STATUS,
        required_input_hashes=tuple(input_hash_by_label[label] for label in required_input_labels),
        proof_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_LEVEL_COMPATIBILITY_PROOF_POLICY",
                "proof_label": proof_label,
                "required_input_labels": required_input_labels,
            }
        ),
        planned_proof_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_LEVEL_COMPATIBILITY_PLANNED_PROOF_OUTPUT",
                "proof_label": proof_label,
                "required_input_hashes": tuple(input_hash_by_label[label] for label in required_input_labels),
            }
        ),
        proof_contract_hash="0" * 64,
    )
    contract = LevelCompatibilityProofContract(
        **{
            **asdict(contract),
            "proof_contract_hash": canonical_sha256(_level_compatibility_proof_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_runtime_history_input_field_contract(
    input_label: str,
    manifest_field_contract: SourceInputManifestFieldContract,
) -> RuntimeHistoryInputFieldContract:
    manifest_field = REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
    if manifest_field_contract.manifest_field != manifest_field:
        raise CarverBlocked("S27 v2 runtime history input builder must use locked manifest field")
    contract = RuntimeHistoryInputFieldContract(
        input_label=input_label,
        input_status=PLANNED_RUNTIME_HISTORY_INPUT_STATUS,
        source_input_manifest_field=manifest_field,
        source_input_role=manifest_field_contract.source_input_role,
        source_input_manifest_field_contract_hash=manifest_field_contract.manifest_field_contract_hash,
        selected_row_hash=manifest_field_contract.selected_row_hash,
        selected_row_locator_hash=manifest_field_contract.selected_row_locator_hash,
        runtime_history_input_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_RUNTIME_HISTORY_INPUT_FIELD_POLICY",
                "input_label": input_label,
                "manifest_field": manifest_field,
            }
        ),
        completed_bar_policy_hash=manifest_field_contract.completed_bar_policy_hash,
        strict_prior_policy_hash=manifest_field_contract.strict_prior_policy_hash,
        no_future_rows_proof_hash=manifest_field_contract.no_future_rows_proof_hash,
        input_field_contract_hash="0" * 64,
    )
    contract = RuntimeHistoryInputFieldContract(
        **{
            **asdict(contract),
            "input_field_contract_hash": canonical_sha256(
                _runtime_history_input_field_hash_payload(contract)
            ),
        }
    )
    contract.validate()
    return contract


def _build_runtime_history_level_compatibility_binding_contract(
    runtime_input_label: str,
    runtime_input_hash_by_label: dict[str, str],
    level_input_hash_by_label: dict[str, str],
) -> RuntimeHistoryLevelCompatibilityInputBindingContract:
    level_input_label = REQUIRED_LEVEL_COMPATIBILITY_INPUT_BY_RUNTIME_HISTORY_INPUT[runtime_input_label]
    contract = RuntimeHistoryLevelCompatibilityInputBindingContract(
        runtime_input_label=runtime_input_label,
        level_compatibility_input_label=level_input_label,
        runtime_input_field_contract_hash=runtime_input_hash_by_label[runtime_input_label],
        level_compatibility_input_field_contract_hash=level_input_hash_by_label[level_input_label],
        level_compatibility_input_binding_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_RUNTIME_HISTORY_LEVEL_COMPATIBILITY_INPUT_BINDING_POLICY",
                "runtime_input_label": runtime_input_label,
                "level_compatibility_input_label": level_input_label,
            }
        ),
        level_compatibility_input_binding_contract_hash="0" * 64,
    )
    contract = RuntimeHistoryLevelCompatibilityInputBindingContract(
        **{
            **asdict(contract),
            "level_compatibility_input_binding_contract_hash": canonical_sha256(
                _runtime_history_level_compatibility_binding_hash_payload(contract)
            ),
        }
    )
    contract.validate()
    return contract


def _build_runtime_history_state_input_binding_contract(
    state_family: str,
    runtime_input_hash_by_label: dict[str, str],
) -> RuntimeHistoryStateInputBindingContract:
    required_labels = REQUIRED_RUNTIME_HISTORY_INPUTS_BY_STATE[state_family]
    contract = RuntimeHistoryStateInputBindingContract(
        state_family=state_family,
        required_runtime_input_labels=required_labels,
        required_runtime_input_field_contract_hashes=tuple(
            runtime_input_hash_by_label[label]
            for label in required_labels
        ),
        state_input_binding_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_RUNTIME_HISTORY_STATE_INPUT_BINDING_POLICY",
                "state_family": state_family,
                "required_runtime_input_labels": required_labels,
            }
        ),
        state_input_binding_contract_hash="0" * 64,
    )
    contract = RuntimeHistoryStateInputBindingContract(
        **{
            **asdict(contract),
            "state_input_binding_contract_hash": canonical_sha256(
                _runtime_history_state_input_binding_hash_payload(contract)
            ),
        }
    )
    contract.validate()
    return contract


def _build_runtime_history_vqm_dependency_binding_contract(
    component_label: str,
    dependency_hash_by_label: dict[str, str],
) -> RuntimeHistoryVqmDependencyBindingContract:
    required_labels = REQUIRED_RUNTIME_HISTORY_DEPENDENCIES_BY_VQM_COMPONENT[component_label]
    contract = RuntimeHistoryVqmDependencyBindingContract(
        component_label=component_label,
        required_runtime_dependency_labels=required_labels,
        required_runtime_dependency_contract_hashes=tuple(
            dependency_hash_by_label[label]
            for label in required_labels
        ),
        vqm_dependency_binding_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_RUNTIME_HISTORY_VQM_DEPENDENCY_BINDING_POLICY",
                "component_label": component_label,
                "required_runtime_dependency_labels": required_labels,
            }
        ),
        vqm_dependency_binding_contract_hash="0" * 64,
    )
    contract = RuntimeHistoryVqmDependencyBindingContract(
        **{
            **asdict(contract),
            "vqm_dependency_binding_contract_hash": canonical_sha256(
                _runtime_history_vqm_dependency_binding_hash_payload(contract)
            ),
        }
    )
    contract.validate()
    return contract


def _build_runtime_state_family_contract(
    state_family: str,
    state_input_binding_hash_by_state: dict[str, str],
) -> RuntimeStateFamilyContract:
    contract = RuntimeStateFamilyContract(
        state_family=state_family,
        state_status=PLANNED_RUNTIME_HISTORY_STATE_STATUS,
        required_input_hashes=(state_input_binding_hash_by_state[state_family],),
        state_definition_hash=canonical_sha256(
            {"artifact": "S27_V2_RUNTIME_STATE_DEFINITION", "state_family": state_family}
        ),
        state_policy_hash=canonical_sha256(
            {"artifact": "S27_V2_RUNTIME_STATE_POLICY", "state_family": state_family}
        ),
        planned_state_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_RUNTIME_STATE_PLANNED_OUTPUT",
                "state_family": state_family,
                "state_input_binding_hash": state_input_binding_hash_by_state[state_family],
            }
        ),
        state_contract_hash="0" * 64,
    )
    contract = RuntimeStateFamilyContract(
        **{
            **asdict(contract),
            "state_contract_hash": canonical_sha256(_runtime_state_family_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _build_vqm_component_contract(
    component_label: str,
    dependency_hash_by_label: dict[str, str],
) -> VqmComponentContract:
    required_labels = REQUIRED_RUNTIME_HISTORY_DEPENDENCIES_BY_VQM_COMPONENT[component_label]
    contract = VqmComponentContract(
        component_label=component_label,
        required_input_hashes=tuple(dependency_hash_by_label[label] for label in required_labels),
        component_policy_hash=canonical_sha256(
            {"artifact": "S27_V2_VQM_COMPONENT_POLICY", "component_label": component_label}
        ),
        planned_component_output_hash=canonical_sha256(
            {
                "artifact": "S27_V2_VQM_COMPONENT_PLANNED_OUTPUT",
                "component_label": component_label,
                "required_input_hashes": tuple(dependency_hash_by_label[label] for label in required_labels),
            }
        ),
        component_contract_hash="0" * 64,
    )
    contract = VqmComponentContract(
        **{
            **asdict(contract),
            "component_contract_hash": canonical_sha256(_vqm_component_hash_payload(contract)),
        }
    )
    contract.validate()
    return contract


def _validate_level_compatibility_input_contract_local_only(
    contract: LevelCompatibilityInputContractBundle,
    manifest: SourceInputManifestContractBundle,
) -> None:
    if contract.source_input_manifest_contract_bundle != manifest:
        raise CarverBlocked("S27 v2 level compatibility input must embed active source-input manifest")
    if contract.status != S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_ONLY_STATUS:
        raise CarverBlocked("S27 v2 level compatibility input contract must remain contract-only")
    if contract.source_input_manifest_contract_hash != manifest.source_input_manifest_contract_hash:
        raise CarverBlocked("S27 v2 level compatibility input must bind active source-input manifest contract")
    if contract.source_input_manifest_hash != manifest.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 level compatibility input must bind active source-input manifest hash")
    if contract.source_input_selection_contract_hash != manifest.source_input_selection_contract_hash:
        raise CarverBlocked("S27 v2 level compatibility input must bind active source-input selection")
    expected_policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_POLICY",
            "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
        }
    )
    if contract.level_compatibility_policy_hash != expected_policy_hash:
        raise CarverBlocked("S27 v2 level compatibility input policy hash must be content-bound")
    field_by_manifest_field = _source_input_manifest_field_contract_by_field(manifest)
    input_hash_by_label: dict[str, str] = {}
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_LEVEL_COMPATIBILITY_INPUTS:
        raise CarverBlocked("S27 v2 level compatibility input fields must match locked tuple")
    for field in contract.input_field_contracts:
        field.validate()
        _validate_level_compatibility_input_field_content_bound(field)
        manifest_field = REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[field.input_label]
        manifest_field_contract = field_by_manifest_field[manifest_field]
        if field.source_input_manifest_field_contract_hash != manifest_field_contract.manifest_field_contract_hash:
            raise CarverBlocked("S27 v2 level compatibility input field must bind active manifest field")
        if field.selected_row_hash != manifest_field_contract.selected_row_hash:
            raise CarverBlocked("S27 v2 level compatibility input field must bind active selected row")
        if field.selected_row_locator_hash != manifest_field_contract.selected_row_locator_hash:
            raise CarverBlocked("S27 v2 level compatibility input field must bind active selected row locator")
        input_hash_by_label[field.input_label] = field.input_field_contract_hash
    _require_hash_map_exact(
        "S27 v2 level compatibility source contract map",
        contract.expected_source_contract_hash_by_input_label,
        {
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ].manifest_field_contract_hash
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        },
        REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
    )
    _require_hash_map_exact(
        "S27 v2 level compatibility selected-row map",
        contract.expected_selected_row_hash_by_input_label,
        {
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ].selected_row_hash
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        },
        REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
    )
    _require_hash_map_exact(
        "S27 v2 level compatibility selected-row-locator map",
        contract.expected_selected_row_locator_hash_by_input_label,
        {
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ].selected_row_locator_hash
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        },
        REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
    )
    if tuple(binding.proof_label for binding in contract.proof_input_binding_contracts) != REQUIRED_LEVEL_COMPATIBILITY_PROOFS:
        raise CarverBlocked("S27 v2 level compatibility proof bindings must match locked tuple")
    for binding in contract.proof_input_binding_contracts:
        binding.validate()
        _validate_level_compatibility_proof_input_binding_content_bound(binding)
        expected_hashes = tuple(input_hash_by_label[label] for label in binding.required_input_labels)
        if binding.required_input_field_contract_hashes != expected_hashes:
            raise CarverBlocked("S27 v2 level compatibility proof binding must bind active input fields")
    expected_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_SET",
            "input_field_contract_hashes": tuple(input_hash_by_label.values()),
            "proof_input_binding_contract_hashes": tuple(
                binding.proof_input_binding_contract_hash
                for binding in contract.proof_input_binding_contracts
            ),
            "source_input_manifest_contract_hash": manifest.source_input_manifest_contract_hash,
            "source_input_manifest_hash": manifest.source_input_manifest_hash,
        }
    )
    if contract.level_compatibility_input_set_hash != expected_set_hash:
        raise CarverBlocked("S27 v2 level compatibility input set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT",
            "level_compatibility_policy_hash": contract.level_compatibility_policy_hash,
            "level_compatibility_input_set_hash": contract.level_compatibility_input_set_hash,
            "source_input_manifest_contract_hash": manifest.source_input_manifest_contract_hash,
            "source_input_manifest_hash": manifest.source_input_manifest_hash,
        }
    )
    if contract.level_compatibility_input_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 level compatibility input contract hash must be content-bound")


def _validate_runtime_history_input_contract_local_only(
    contract: RuntimeHistoryInputContractBundle,
    manifest: SourceInputManifestContractBundle,
    level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
    level_compatibility_contract: LevelCompatibilityContractBundle,
) -> None:
    if contract.source_input_manifest_contract_bundle != manifest:
        raise CarverBlocked("S27 v2 runtime history input must embed active source-input manifest")
    if contract.status != S27_V2_RUNTIME_HISTORY_INPUT_CONTRACT_ONLY_STATUS:
        raise CarverBlocked("S27 v2 runtime history input contract must remain contract-only")
    if contract.source_input_manifest_contract_hash != manifest.source_input_manifest_contract_hash:
        raise CarverBlocked("S27 v2 runtime history input must bind active source-input manifest contract")
    if contract.source_input_manifest_hash != manifest.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 runtime history input must bind active source-input manifest hash")
    if (
        contract.level_compatibility_input_contract_hash
        != level_compatibility_input_contract.level_compatibility_input_contract_hash
    ):
        raise CarverBlocked("S27 v2 runtime history input must bind level compatibility input")
    if contract.level_compatibility_contract_hash != level_compatibility_contract.level_compatibility_contract_bundle_hash:
        raise CarverBlocked("S27 v2 runtime history input must bind level compatibility contract")
    expected_policy_hash = canonical_sha256(
        {
            "artifact": "S27_V2_RUNTIME_HISTORY_INPUT_POLICY",
            "scope": "LOCAL_ONLY_SLICE3_CONSTRUCTION_SCAFFOLD",
        }
    )
    if contract.runtime_history_input_policy_hash != expected_policy_hash:
        raise CarverBlocked("S27 v2 runtime history input policy hash must be content-bound")
    field_by_manifest_field = _source_input_manifest_field_contract_by_field(manifest)
    runtime_input_hash_by_label: dict[str, str] = {}
    if tuple(field.input_label for field in contract.input_field_contracts) != REQUIRED_RUNTIME_HISTORY_INPUTS:
        raise CarverBlocked("S27 v2 runtime history input fields must match locked tuple")
    for field in contract.input_field_contracts:
        field.validate()
        _validate_runtime_history_input_field_content_bound(field)
        manifest_field_contract = field_by_manifest_field[
            REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[field.input_label]
        ]
        if field.source_input_manifest_field_contract_hash != manifest_field_contract.manifest_field_contract_hash:
            raise CarverBlocked("S27 v2 runtime history input field must bind active manifest field")
        if field.selected_row_hash != manifest_field_contract.selected_row_hash:
            raise CarverBlocked("S27 v2 runtime history input field must bind active selected row")
        if field.selected_row_locator_hash != manifest_field_contract.selected_row_locator_hash:
            raise CarverBlocked("S27 v2 runtime history input field must bind active selected row locator")
        runtime_input_hash_by_label[field.input_label] = field.input_field_contract_hash
    level_input_hash_by_label = _level_compatibility_input_field_contract_hash_by_label(
        level_compatibility_input_contract,
    )
    for binding in contract.level_compatibility_input_bindings:
        binding.validate()
        _validate_runtime_history_level_compatibility_binding_content_bound(binding)
        if binding.runtime_input_field_contract_hash != runtime_input_hash_by_label[binding.runtime_input_label]:
            raise CarverBlocked("S27 v2 runtime history level binding must bind active runtime input")
        if (
            binding.level_compatibility_input_field_contract_hash
            != level_input_hash_by_label[binding.level_compatibility_input_label]
        ):
            raise CarverBlocked("S27 v2 runtime history level binding must bind active level input")
    for binding in contract.state_input_binding_contracts:
        binding.validate()
        _validate_runtime_history_state_input_binding_content_bound(binding)
        if binding.required_runtime_input_field_contract_hashes != tuple(
            runtime_input_hash_by_label[label] for label in binding.required_runtime_input_labels
        ):
            raise CarverBlocked("S27 v2 runtime history state binding must bind active runtime inputs")
    dependency_hash_by_label = {
        binding.state_family: binding.state_input_binding_contract_hash
        for binding in contract.state_input_binding_contracts
    }
    for binding in contract.vqm_dependency_binding_contracts:
        binding.validate()
        _validate_runtime_history_vqm_dependency_binding_content_bound(binding)
        expected_hashes = tuple(
            dependency_hash_by_label[label]
            for label in binding.required_runtime_dependency_labels
        )
        if binding.required_runtime_dependency_contract_hashes != expected_hashes:
            raise CarverBlocked("S27 v2 runtime history V/Q/M binding must bind active dependencies")
        dependency_hash_by_label[binding.component_label] = binding.vqm_dependency_binding_contract_hash
    _require_hash_map_exact(
        "S27 v2 runtime history source contract map",
        contract.expected_source_contract_hash_by_input_label,
        {
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ].manifest_field_contract_hash
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        },
        REQUIRED_RUNTIME_HISTORY_INPUTS,
    )
    _require_hash_map_exact(
        "S27 v2 runtime history selected-row map",
        contract.expected_selected_row_hash_by_input_label,
        {
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ].selected_row_hash
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        },
        REQUIRED_RUNTIME_HISTORY_INPUTS,
    )
    _require_hash_map_exact(
        "S27 v2 runtime history selected-row-locator map",
        contract.expected_selected_row_locator_hash_by_input_label,
        {
            input_label: field_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ].selected_row_locator_hash
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        },
        REQUIRED_RUNTIME_HISTORY_INPUTS,
    )
    expected_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_RUNTIME_HISTORY_INPUT_SET",
            "input_field_contract_hashes": tuple(runtime_input_hash_by_label.values()),
            "level_compatibility_input_binding_hashes": tuple(
                binding.level_compatibility_input_binding_contract_hash
                for binding in contract.level_compatibility_input_bindings
            ),
            "state_input_binding_hashes": tuple(
                binding.state_input_binding_contract_hash
                for binding in contract.state_input_binding_contracts
            ),
            "vqm_dependency_binding_hashes": tuple(
                binding.vqm_dependency_binding_contract_hash
                for binding in contract.vqm_dependency_binding_contracts
            ),
            "source_input_manifest_contract_hash": manifest.source_input_manifest_contract_hash,
        }
    )
    if contract.runtime_history_input_set_hash != expected_set_hash:
        raise CarverBlocked("S27 v2 runtime history input set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_RUNTIME_HISTORY_INPUT_CONTRACT",
            "level_compatibility_contract_hash": level_compatibility_contract.level_compatibility_contract_bundle_hash,
            "level_compatibility_input_contract_hash": (
                level_compatibility_input_contract.level_compatibility_input_contract_hash
            ),
            "runtime_history_input_policy_hash": contract.runtime_history_input_policy_hash,
            "runtime_history_input_set_hash": contract.runtime_history_input_set_hash,
            "source_input_manifest_contract_hash": manifest.source_input_manifest_contract_hash,
        }
    )
    if contract.runtime_history_input_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 runtime history input contract hash must be content-bound")


def _validate_level_compatibility_contract_content_bound(
    contract: LevelCompatibilityContractBundle,
    level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
    source_row_batch_contract: SourceRowBatchSetContract,
) -> None:
    contract.validate()
    level_input_hash_by_label = _level_compatibility_input_field_contract_hash_by_label(
        level_compatibility_input_contract,
    )
    family_hash_by_family = _source_row_batch_family_contract_hash_by_family(source_row_batch_contract)
    if contract.source_binding.daily_continuous_row_family_hash != family_hash_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 level compatibility source binding must bind daily continuous family")
    if contract.source_binding.daily_current_contract_row_family_hash != family_hash_by_family["DAILY_CURRENT_CONTRACT_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 level compatibility source binding must bind daily current family")
    if contract.source_binding.previous_completed_current_contract_close_family_hash != family_hash_by_family["DAILY_CURRENT_CONTRACT_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 level compatibility source binding must bind previous close family")
    if contract.source_binding.hourly_decision_row_family_hash != family_hash_by_family["HOURLY_DECISION_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 level compatibility source binding must bind hourly decision family")
    if contract.source_binding.hourly_fill_row_family_hash != family_hash_by_family["HOURLY_FILL_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 level compatibility source binding must bind hourly fill family")
    if contract.source_binding.source_universe_contract_hash != source_row_batch_contract.source_universe_contract_bundle_hash:
        raise CarverBlocked("S27 v2 level compatibility source binding must bind source universe")
    if contract.source_binding.row_locator_contract_hash != source_row_batch_contract.row_locator_contract_bundle_hash:
        raise CarverBlocked("S27 v2 level compatibility source binding must bind row locator")
    if contract.source_binding.binding_hash != canonical_sha256(
        _level_compatibility_source_binding_hash_payload(contract.source_binding)
    ):
        raise CarverBlocked("S27 v2 level compatibility source binding hash must be content-bound")
    for proof in contract.proof_contracts:
        expected_inputs = tuple(
            level_input_hash_by_label[label]
            for label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS_BY_PROOF[proof.proof_label]
        )
        if proof.required_input_hashes != expected_inputs:
            raise CarverBlocked("S27 v2 level compatibility proof must bind active input fields")
        if proof.proof_contract_hash != canonical_sha256(_level_compatibility_proof_hash_payload(proof)):
            raise CarverBlocked("S27 v2 level compatibility proof hash must be content-bound")
    if contract.verdict_contract.verdict_contract_hash != canonical_sha256(
        _level_compatibility_verdict_hash_payload(contract.verdict_contract)
    ):
        raise CarverBlocked("S27 v2 level compatibility verdict hash must be content-bound")
    if contract.level_compatibility_contract_bundle_hash != canonical_sha256(
        _level_compatibility_contract_bundle_hash_payload(contract)
    ):
        raise CarverBlocked("S27 v2 level compatibility contract bundle hash must be content-bound")


def _validate_runtime_history_contract_content_bound(
    contract: RuntimeHistoryContractBundle,
    runtime_history_input_contract: RuntimeHistoryInputContractBundle,
    level_compatibility_contract: LevelCompatibilityContractBundle,
    source_row_batch_contract: SourceRowBatchSetContract,
) -> None:
    contract.validate()
    family_hash_by_family = _source_row_batch_family_contract_hash_by_family(source_row_batch_contract)
    if contract.source_binding.source_input_manifest_hash != runtime_history_input_contract.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 runtime history source binding must bind source-input manifest")
    if contract.source_binding.level_compatibility_contract_hash != level_compatibility_contract.level_compatibility_contract_bundle_hash:
        raise CarverBlocked("S27 v2 runtime history source binding must bind level compatibility contract")
    if contract.source_binding.daily_continuous_row_family_hash != family_hash_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 runtime history source binding must bind daily continuous family")
    if contract.source_binding.daily_current_contract_row_family_hash != family_hash_by_family["DAILY_CURRENT_CONTRACT_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 runtime history source binding must bind daily current family")
    if contract.source_binding.hourly_decision_row_family_hash != family_hash_by_family["HOURLY_DECISION_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 runtime history source binding must bind hourly decision family")
    if contract.source_binding.source_binding_hash != canonical_sha256(
        _runtime_history_source_binding_hash_payload(contract.source_binding)
    ):
        raise CarverBlocked("S27 v2 runtime history source binding hash must be content-bound")
    state_input_hash_by_state = {
        binding.state_family: binding.state_input_binding_contract_hash
        for binding in runtime_history_input_contract.state_input_binding_contracts
    }
    for state in contract.state_contracts:
        if state.required_input_hashes != (state_input_hash_by_state[state.state_family],):
            raise CarverBlocked("S27 v2 runtime state must bind active state input binding")
        if state.state_contract_hash != canonical_sha256(_runtime_state_family_hash_payload(state)):
            raise CarverBlocked("S27 v2 runtime state contract hash must be content-bound")
    dependency_hash_by_label = {
        state.state_family: state.state_contract_hash
        for state in contract.state_contracts
    }
    for component in contract.vqm_component_contracts:
        expected_inputs = tuple(
            dependency_hash_by_label[label]
            for label in REQUIRED_RUNTIME_HISTORY_DEPENDENCIES_BY_VQM_COMPONENT[component.component_label]
        )
        if component.required_input_hashes != expected_inputs:
            raise CarverBlocked("S27 v2 V/Q/M component must bind active dependencies")
        if component.component_contract_hash != canonical_sha256(_vqm_component_hash_payload(component)):
            raise CarverBlocked("S27 v2 V/Q/M component contract hash must be content-bound")
        dependency_hash_by_label[component.component_label] = component.component_contract_hash
    if contract.runtime_history_contract_bundle_hash != canonical_sha256(
        _runtime_history_contract_bundle_hash_payload(contract)
    ):
        raise CarverBlocked("S27 v2 runtime history contract bundle hash must be content-bound")


def _source_input_manifest_field_contract_by_field(
    manifest: SourceInputManifestContractBundle,
) -> dict[str, SourceInputManifestFieldContract]:
    by_field = {contract.manifest_field: contract for contract in manifest.manifest_field_contracts}
    if tuple(by_field) != REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS:
        raise CarverBlocked("S27 v2 source-input manifest fields must match locked tuple")
    return by_field


def _level_compatibility_input_field_contract_hash_by_label(
    contract: LevelCompatibilityInputContractBundle,
) -> dict[str, str]:
    by_label = {field.input_label: field.input_field_contract_hash for field in contract.input_field_contracts}
    if tuple(by_label) != REQUIRED_LEVEL_COMPATIBILITY_INPUTS:
        raise CarverBlocked("S27 v2 level compatibility input hash map must match locked tuple")
    return by_label


def _source_row_batch_family_contract_hash_by_family(
    source_row_batch_contract: SourceRowBatchSetContract,
) -> dict[str, str]:
    by_family = {
        contract.row_family: contract.source_row_batch_family_contract_hash
        for contract in source_row_batch_contract.source_row_batch_family_contracts
    }
    if tuple(by_family) != REQUIRED_ROW_LOCATOR_FAMILIES:
        raise CarverBlocked("S27 v2 source-row batch family hash map must match locked tuple")
    return by_family


def _require_hash_map_exact(
    name: str,
    observed: dict[str, str],
    expected: dict[str, str],
    labels: tuple[str, ...],
) -> None:
    if tuple(observed) != labels or tuple(expected) != labels:
        raise CarverBlocked(f"{name} must match locked label tuple")
    if observed != expected:
        raise CarverBlocked(f"{name} must match active upstream authority")


def _validate_level_compatibility_input_field_content_bound(contract: LevelCompatibilityInputFieldContract) -> None:
    if contract.input_field_contract_hash != canonical_sha256(_level_compatibility_input_field_hash_payload(contract)):
        raise CarverBlocked("S27 v2 level compatibility input field hash must be content-bound")


def _validate_level_compatibility_proof_input_binding_content_bound(
    contract: LevelCompatibilityProofInputBindingContract,
) -> None:
    if contract.proof_input_binding_contract_hash != canonical_sha256(_level_compatibility_proof_input_binding_hash_payload(contract)):
        raise CarverBlocked("S27 v2 level compatibility proof-input binding hash must be content-bound")


def _validate_runtime_history_input_field_content_bound(contract: RuntimeHistoryInputFieldContract) -> None:
    if contract.input_field_contract_hash != canonical_sha256(_runtime_history_input_field_hash_payload(contract)):
        raise CarverBlocked("S27 v2 runtime history input field hash must be content-bound")


def _validate_runtime_history_level_compatibility_binding_content_bound(
    contract: RuntimeHistoryLevelCompatibilityInputBindingContract,
) -> None:
    if contract.level_compatibility_input_binding_contract_hash != canonical_sha256(_runtime_history_level_compatibility_binding_hash_payload(contract)):
        raise CarverBlocked("S27 v2 runtime history level binding hash must be content-bound")


def _validate_runtime_history_state_input_binding_content_bound(
    contract: RuntimeHistoryStateInputBindingContract,
) -> None:
    if contract.state_input_binding_contract_hash != canonical_sha256(_runtime_history_state_input_binding_hash_payload(contract)):
        raise CarverBlocked("S27 v2 runtime history state binding hash must be content-bound")


def _validate_runtime_history_vqm_dependency_binding_content_bound(
    contract: RuntimeHistoryVqmDependencyBindingContract,
) -> None:
    if contract.vqm_dependency_binding_contract_hash != canonical_sha256(_runtime_history_vqm_dependency_binding_hash_payload(contract)):
        raise CarverBlocked("S27 v2 runtime history V/Q/M binding hash must be content-bound")


def _level_compatibility_input_field_hash_payload(contract: LevelCompatibilityInputFieldContract) -> dict[str, object]:
    return {"artifact": "S27_V2_LEVEL_COMPATIBILITY_INPUT_FIELD_CONTRACT", **asdict(contract), "input_field_contract_hash": None}


def _level_compatibility_proof_input_binding_hash_payload(contract: LevelCompatibilityProofInputBindingContract) -> dict[str, object]:
    return {"artifact": "S27_V2_LEVEL_COMPATIBILITY_PROOF_INPUT_BINDING_CONTRACT", **asdict(contract), "proof_input_binding_contract_hash": None}


def _level_compatibility_source_binding_hash_payload(contract: LevelCompatibilitySourceBinding) -> dict[str, object]:
    return {"artifact": "S27_V2_LEVEL_COMPATIBILITY_SOURCE_BINDING", **asdict(contract), "binding_hash": None}


def _level_compatibility_proof_hash_payload(contract: LevelCompatibilityProofContract) -> dict[str, object]:
    return {"artifact": "S27_V2_LEVEL_COMPATIBILITY_PROOF_CONTRACT", **asdict(contract), "proof_contract_hash": None}


def _level_compatibility_verdict_hash_payload(contract: LevelCompatibilityVerdictContract) -> dict[str, object]:
    return {"artifact": "S27_V2_LEVEL_COMPATIBILITY_VERDICT_CONTRACT", **asdict(contract), "verdict_contract_hash": None}


def _level_compatibility_contract_bundle_hash_payload(contract: LevelCompatibilityContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_LEVEL_COMPATIBILITY_CONTRACT_BUNDLE",
        "daily_hourly_level_compatibility_policy_hash": contract.daily_hourly_level_compatibility_policy_hash,
        "proof_contract_hashes": tuple(proof.proof_contract_hash for proof in contract.proof_contracts),
        "source_binding_hash": contract.source_binding.binding_hash,
        "status": contract.status,
        "verdict_contract_hash": contract.verdict_contract.verdict_contract_hash,
    }


def _runtime_history_input_field_hash_payload(contract: RuntimeHistoryInputFieldContract) -> dict[str, object]:
    return {"artifact": "S27_V2_RUNTIME_HISTORY_INPUT_FIELD_CONTRACT", **asdict(contract), "input_field_contract_hash": None}


def _runtime_history_level_compatibility_binding_hash_payload(contract: RuntimeHistoryLevelCompatibilityInputBindingContract) -> dict[str, object]:
    return {"artifact": "S27_V2_RUNTIME_HISTORY_LEVEL_COMPATIBILITY_INPUT_BINDING_CONTRACT", **asdict(contract), "level_compatibility_input_binding_contract_hash": None}


def _runtime_history_state_input_binding_hash_payload(contract: RuntimeHistoryStateInputBindingContract) -> dict[str, object]:
    return {"artifact": "S27_V2_RUNTIME_HISTORY_STATE_INPUT_BINDING_CONTRACT", **asdict(contract), "state_input_binding_contract_hash": None}


def _runtime_history_vqm_dependency_binding_hash_payload(contract: RuntimeHistoryVqmDependencyBindingContract) -> dict[str, object]:
    return {"artifact": "S27_V2_RUNTIME_HISTORY_VQM_DEPENDENCY_BINDING_CONTRACT", **asdict(contract), "vqm_dependency_binding_contract_hash": None}


def _runtime_history_source_binding_hash_payload(contract: RuntimeHistorySourceBinding) -> dict[str, object]:
    return {"artifact": "S27_V2_RUNTIME_HISTORY_SOURCE_BINDING", **asdict(contract), "source_binding_hash": None}


def _runtime_state_family_hash_payload(contract: RuntimeStateFamilyContract) -> dict[str, object]:
    return {"artifact": "S27_V2_RUNTIME_STATE_FAMILY_CONTRACT", **asdict(contract), "state_contract_hash": None}


def _vqm_component_hash_payload(contract: VqmComponentContract) -> dict[str, object]:
    return {"artifact": "S27_V2_VQM_COMPONENT_CONTRACT", **asdict(contract), "component_contract_hash": None}


def _runtime_history_contract_bundle_hash_payload(contract: RuntimeHistoryContractBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_RUNTIME_HISTORY_CONTRACT_BUNDLE",
        "runtime_history_ledger_schema_hash": contract.runtime_history_ledger_schema_hash,
        "sigma_annualization_policy_hash": contract.sigma_annualization_policy_hash,
        "sigma_estimator_definition_hash": contract.sigma_estimator_definition_hash,
        "sigma_input_window_policy_hash": contract.sigma_input_window_policy_hash,
        "source_binding_hash": contract.source_binding.source_binding_hash,
        "state_contract_hashes": tuple(state.state_contract_hash for state in contract.state_contracts),
        "status": contract.status,
        "vqm_component_contract_hashes": tuple(component.component_contract_hash for component in contract.vqm_component_contracts),
    }


def _require_slice1_artifacts_match_inputs(
    inputs: LocalParserFileReplaySlice1Inputs,
    slice1_artifacts: LocalParserFileReplaySlice1Artifacts,
) -> None:
    inputs.validate()
    slice1_artifacts.validate()
    expected = build_local_parser_file_replay_slice1(inputs)
    if slice1_artifacts != expected:
        raise CarverBlocked("S27 v2 slice1 artifacts must match active local inputs")


def _source_row_batch_family_contract_by_family(
    source_row_batch_contract: SourceRowBatchSetContract,
) -> dict[str, SourceRowBatchFamilyContract]:
    source_row_batch_contract._validate_contract_only_shape()
    by_family = {
        contract.row_family: contract
        for contract in source_row_batch_contract.source_row_batch_family_contracts
    }
    if tuple(by_family) != REQUIRED_ROW_LOCATOR_FAMILIES:
        raise CarverBlocked("S27 v2 source row batch family map must match locked tuple")
    return by_family


def _parsed_file_by_family(
    parsed_files: tuple[ParsedDeclaredSourceFile, ...],
) -> dict[str, ParsedDeclaredSourceFile]:
    _require_parsed_family_tuple(parsed_files)
    by_family = {
        parsed.row_family: parsed
        for parsed in parsed_files
    }
    if tuple(by_family) != REQUIRED_ROW_LOCATOR_FAMILIES:
        raise CarverBlocked("S27 v2 parsed file family map must match locked tuple")
    return by_family


def _selected_row_locator_hash(
    role: str,
    family: str,
    row: (
        LocalDailySourceRow
        | LocalHourlySourceRow
        | LocalSessionSourceRow
        | LocalRollSourceRow
        | LocalCostParameterRow
    ),
) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_SELECTED_ROW_LOCATOR_HASH",
            "input_role": role,
            "row_family": family,
            "row_locator": row.row_locator,
            "selected_row_hash": row.row_hash,
        }
    )


def _ordered_hash_map_payload(
    hash_by_label: dict[str, str],
    required_labels: tuple[str, ...],
) -> tuple[tuple[str, str], ...]:
    if tuple(hash_by_label) != required_labels:
        raise CarverBlocked("S27 v2 hash map payload must match locked label tuple")
    return tuple((label, hash_by_label[label]) for label in required_labels)


def _validate_source_row_selection_authority_matches_rows(
    authority: SourceRowSelectionAuthorityContract,
    slice1_artifacts: LocalParserFileReplaySlice1Artifacts,
) -> None:
    authority.validate()
    parsed_by_family = _parsed_file_by_family(slice1_artifacts.parsed_files)
    family_contract_by_family = _source_row_batch_family_contract_by_family(slice1_artifacts.source_row_batch_contract)
    for role in REQUIRED_SOURCE_INPUT_ROLES:
        family = REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[role]
        row = parsed_by_family[family].rows[0]
        family_contract = family_contract_by_family[family]
        if authority.selected_row_hash_by_input_role[role] != row.row_hash:
            raise CarverBlocked("S27 v2 selected row authority must bind active parsed row")
        if authority.selected_row_locator_hash_by_input_role[role] != _selected_row_locator_hash(role, family, row):
            raise CarverBlocked("S27 v2 selected row-locator authority must bind active parsed row")
        expected_row_proof = canonical_sha256(
            {
                "artifact": "S27_V2_SELECTED_ROW_MEMBERSHIP_PROOF",
                "input_role": role,
                "row_family": family,
                "selected_row_hash": row.row_hash,
                "source_row_batch_family_contract_hash": family_contract.source_row_batch_family_contract_hash,
                "source_row_batch_hash": family_contract.source_row_batch_hash,
            }
        )
        if authority.selected_row_membership_proof_hash_by_input_role[role] != expected_row_proof:
            raise CarverBlocked("S27 v2 selected row proof must bind active source-row batch")
        expected_locator_proof = canonical_sha256(
            {
                "artifact": "S27_V2_SELECTED_ROW_LOCATOR_MEMBERSHIP_PROOF",
                "input_role": role,
                "row_family": family,
                "selected_row_locator_hash": authority.selected_row_locator_hash_by_input_role[role],
                "row_locator_family_contract_hash": family_contract.row_locator_family_contract_hash,
                "row_locator_policy_hash": family_contract.row_locator_policy_hash,
            }
        )
        if authority.selected_row_locator_membership_proof_hash_by_input_role[role] != expected_locator_proof:
            raise CarverBlocked("S27 v2 selected row-locator proof must bind active row locator")
    if (
        authority.source_universe_contract_bundle_hash
        != slice1_artifacts.source_row_batch_contract.source_universe_contract_bundle_hash
    ):
        raise CarverBlocked("S27 v2 source row selection authority must bind active source universe")
    if (
        authority.row_locator_contract_bundle_hash
        != slice1_artifacts.source_row_batch_contract.row_locator_contract_bundle_hash
    ):
        raise CarverBlocked("S27 v2 source row selection authority must bind active row locator")


def _validate_source_row_selection_external_authority_content_bound(
    external_authority: SourceRowSelectionExternalAuthorityHandle,
    source_row_selection_authority: SourceRowSelectionAuthorityContract,
) -> None:
    external_authority.validate()
    source_row_selection_authority.validate()
    if external_authority.source_row_selection_authority_hash != (
        source_row_selection_authority.source_row_selection_authority_hash
    ):
        raise CarverBlocked("S27 v2 external source-row-selection handle must bind authority hash")
    if external_authority.selected_row_membership_proof_set_hash != (
        source_row_selection_authority.selected_row_membership_proof_set_hash
    ):
        raise CarverBlocked("S27 v2 external source-row-selection handle must bind row proof set")
    if external_authority.selected_row_locator_membership_proof_set_hash != (
        source_row_selection_authority.selected_row_locator_membership_proof_set_hash
    ):
        raise CarverBlocked("S27 v2 external source-row-selection handle must bind locator proof set")
    expected_handle_hash = canonical_sha256(
        {
            "active_evidence_manifest_hash": external_authority.active_evidence_manifest_hash,
            "artifact": "S27_V2_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_HANDLE",
            "authority_handle_policy_hash": external_authority.authority_handle_policy_hash,
            "authority_status": external_authority.authority_status,
            "replay_trust_root_hash": external_authority.replay_trust_root_hash,
            "row_locator_contract_bundle_hash": external_authority.row_locator_contract_bundle_hash,
            "selected_row_locator_membership_proof_set_hash": (
                external_authority.selected_row_locator_membership_proof_set_hash
            ),
            "selected_row_membership_proof_set_hash": (
                external_authority.selected_row_membership_proof_set_hash
            ),
            "source_row_batch_contract_hash": external_authority.source_row_batch_contract_hash,
            "source_row_batch_set_hash": external_authority.source_row_batch_set_hash,
            "source_row_selection_authority_hash": external_authority.source_row_selection_authority_hash,
            "source_universe_contract_bundle_hash": external_authority.source_universe_contract_bundle_hash,
        }
    )
    if external_authority.authority_handle_hash != expected_handle_hash:
        raise CarverBlocked("S27 v2 external source-row-selection handle hash must be content-bound")


def _validate_source_input_role_selection_contract_content_bound(
    contract: SourceInputRoleSelectionContract,
) -> None:
    contract.validate()
    expected_hash = canonical_sha256(_source_input_role_contract_hash_payload(contract))
    if contract.source_input_role_contract_hash != expected_hash:
        raise CarverBlocked("S27 v2 source input role contract hash must be content-bound")


def _validate_source_input_selection_contract_content_bound(
    contract: SourceInputSelectionContractBundle,
) -> None:
    contract.source_row_selection_authority.validate()
    for role_contract in contract.role_selection_contracts:
        _validate_source_input_role_selection_contract_content_bound(role_contract)
    expected_selection_set_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_SELECTION_SET",
            "role_contract_hashes": tuple(
                role_contract.source_input_role_contract_hash
                for role_contract in contract.role_selection_contracts
            ),
            "source_row_selection_authority_hash": contract.source_row_selection_authority_hash,
        }
    )
    if contract.source_input_selection_set_hash != expected_selection_set_hash:
        raise CarverBlocked("S27 v2 source input selection set hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_SELECTION_CONTRACT",
            "source_input_selection_set_hash": contract.source_input_selection_set_hash,
            "source_row_batch_contract_hash": contract.source_row_batch_contract_hash,
            "source_row_selection_authority_hash": contract.source_row_selection_authority_hash,
        }
    )
    if contract.source_input_selection_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 source input selection contract hash must be content-bound")


def _validate_source_input_manifest_field_contract_content_bound(
    contract: SourceInputManifestFieldContract,
) -> None:
    contract.validate()
    expected_canonical_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST_CANONICAL_FIELD_SERIALIZATION",
            "manifest_field": contract.manifest_field,
            "selected_row_hash": contract.selected_row_hash,
            "selected_row_locator_hash": contract.selected_row_locator_hash,
        }
    )
    if contract.canonical_field_serialization_hash != expected_canonical_hash:
        raise CarverBlocked("S27 v2 source input manifest field serialization hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        _source_input_manifest_field_contract_hash_payload(contract)
    )
    if contract.manifest_field_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 source input manifest field contract hash must be content-bound")


def _validate_source_input_manifest_contract_local_only(
    contract: SourceInputManifestContractBundle,
    source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
    source_row_batch_contract: SourceRowBatchSetContract,
    parser_output_contract: ParserOutputBatchSetContract,
) -> None:
    contract._validate_contract_only_shape(
        source_row_selection_external_authority,
        source_row_batch_contract,
        parser_output_contract,
    )
    _validate_source_input_selection_contract_content_bound(contract.source_input_selection_contract_bundle)
    for field_contract in contract.manifest_field_contracts:
        _validate_source_input_manifest_field_contract_content_bound(field_contract)
    expected_schema_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST_SCHEMA",
            "manifest_fields": REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS,
            "role_by_manifest_field": tuple(
                (field, REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[field])
                for field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
            ),
        }
    )
    if contract.source_input_manifest_schema_hash != expected_schema_hash:
        raise CarverBlocked("S27 v2 source input manifest schema hash must be content-bound")
    expected_manifest_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST",
            "field_contract_hashes": tuple(
                field_contract.manifest_field_contract_hash
                for field_contract in contract.manifest_field_contracts
            ),
            "source_input_selection_contract_hash": contract.source_input_selection_contract_hash,
        }
    )
    if contract.source_input_manifest_hash != expected_manifest_hash:
        raise CarverBlocked("S27 v2 source input manifest hash must be content-bound")
    expected_contract_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_INPUT_MANIFEST_CONTRACT",
            "source_input_manifest_hash": contract.source_input_manifest_hash,
            "source_input_manifest_schema_hash": contract.source_input_manifest_schema_hash,
            "source_input_selection_contract_hash": contract.source_input_selection_contract_hash,
        }
    )
    if contract.source_input_manifest_contract_hash != expected_contract_hash:
        raise CarverBlocked("S27 v2 source input manifest contract hash must be content-bound")


def _parse_csv_rows(
    text: str,
    row_family: str,
) -> Iterable[
    LocalDailySourceRow
    | LocalHourlySourceRow
    | LocalSessionSourceRow
    | LocalRollSourceRow
    | LocalCostParameterRow
]:
    if row_family not in REQUIRED_COLUMNS_BY_ROW_FAMILY:
        raise CarverBlocked("S27 v2 parser row family is not locked")
    reader = DictReader(text.splitlines())
    required_columns = REQUIRED_COLUMNS_BY_ROW_FAMILY[row_family]
    if reader.fieldnames is None:
        raise CarverBlocked("S27 v2 declared CSV must have a header")
    if tuple(reader.fieldnames) != required_columns:
        raise CarverBlocked("S27 v2 declared CSV header must match locked row-family columns")
    seen_locators: set[str] = set()
    for row_number, raw_row in enumerate(reader, start=1):
        if None in raw_row or tuple(raw_row.keys()) != required_columns:
            raise CarverBlocked("S27 v2 declared CSV row width must match locked row-family columns")
        if any(raw_row[column] is None for column in required_columns):
            raise CarverBlocked("S27 v2 declared CSV row must include every locked column")
        if raw_row.get("row_locator") in seen_locators:
            raise CarverBlocked("S27 v2 declared CSV row locators must be unique")
        seen_locators.add(raw_row["row_locator"])
        yield _parse_source_row(row_family, raw_row, row_number)


def _parse_source_row(
    row_family: str,
    raw_row: dict[str, str],
    row_number: int,
) -> LocalDailySourceRow | LocalHourlySourceRow | LocalSessionSourceRow | LocalRollSourceRow | LocalCostParameterRow:
    base_payload = {
        "artifact": "S27_V2_LOCAL_SOURCE_ROW",
        "row_family": row_family,
        "row_number": row_number,
        "row": raw_row,
    }
    row_hash = canonical_sha256(base_payload)
    if row_family in ("DAILY_CONTINUOUS_COMPLETED_BAR", "DAILY_CURRENT_CONTRACT_COMPLETED_BAR"):
        row = LocalDailySourceRow(
            completed_timestamp_utc=_parse_utc_hour(raw_row["completed_timestamp_utc"]),
            trading_date=raw_row["trading_date"],
            raw_symbol=raw_row["raw_symbol"],
            row_locator=raw_row["row_locator"],
            close_price=_parse_float("S27 v2 daily close price", raw_row["close_price"]),
            annual_percentage_sigma=_parse_float(
                "S27 v2 daily annual percentage sigma",
                raw_row["annual_percentage_sigma"],
            ),
            readiness_status=raw_row["readiness_status"],
            row_hash=row_hash,
        )
    elif row_family in ("HOURLY_DECISION_COMPLETED_BAR", "HOURLY_FILL_COMPLETED_BAR"):
        row = LocalHourlySourceRow(
            completed_timestamp_utc=_parse_utc_hour(raw_row["completed_timestamp_utc"]),
            trading_date=raw_row["trading_date"],
            raw_symbol=raw_row["raw_symbol"],
            session_id=raw_row["session_id"],
            row_locator=raw_row["row_locator"],
            close_price=_parse_float("S27 v2 hourly close price", raw_row["close_price"]),
            readiness_status=raw_row["readiness_status"],
            row_hash=row_hash,
        )
    elif row_family == "SESSION_CALENDAR":
        row = LocalSessionSourceRow(
            trading_date=raw_row["trading_date"],
            session_id=raw_row["session_id"],
            raw_symbol=raw_row["raw_symbol"],
            session_open_utc=_parse_utc_hour(raw_row["session_open_utc"]),
            session_close_utc=_parse_utc_hour(raw_row["session_close_utc"]),
            row_locator=raw_row["row_locator"],
            readiness_status=raw_row["readiness_status"],
            row_hash=row_hash,
        )
    elif row_family == "ROLL_CALENDAR":
        row = LocalRollSourceRow(
            trading_date=raw_row["trading_date"],
            expiring_raw_symbol=raw_row["expiring_raw_symbol"],
            incoming_raw_symbol=raw_row["incoming_raw_symbol"],
            roll_policy_hash=raw_row["roll_policy_hash"],
            row_locator=raw_row["row_locator"],
            readiness_status=raw_row["readiness_status"],
            row_hash=row_hash,
        )
    elif row_family == "COST_PARAMETER":
        row = LocalCostParameterRow(
            effective_trading_date=raw_row["effective_trading_date"],
            raw_symbol=raw_row["raw_symbol"],
            commission_policy_hash=raw_row["commission_policy_hash"],
            spread_policy_hash=raw_row["spread_policy_hash"],
            contract_multiplier_value_hash=raw_row["contract_multiplier_value_hash"],
            currency_policy_hash=raw_row["currency_policy_hash"],
            row_locator=raw_row["row_locator"],
            readiness_status=raw_row["readiness_status"],
            row_hash=row_hash,
        )
    else:
        raise CarverBlocked("S27 v2 parser row family is not locked")
    row.validate()
    return row


def _resolve_declared_path(input_directory_path: str, declared_path: str) -> Path:
    base = Path(input_directory_path).expanduser().resolve()
    path = Path(declared_path).expanduser()
    resolved = path.resolve() if path.is_absolute() else (base / path).resolve()
    try:
        resolved.relative_to(base)
    except ValueError as exc:
        raise CarverBlocked("S27 v2 declared local file path must stay inside input directory") from exc
    if not resolved.is_file():
        raise CarverBlocked("S27 v2 declared local file must exist")
    return resolved


def _require_declared_raw_source(
    input_directory: ReplayInputDirectoryDeclaration,
    raw_declaration: RawSourceFileDeclaration,
) -> None:
    if raw_declaration not in input_directory.raw_source_files:
        raise CarverBlocked("S27 v2 local file read must use a declared raw source file")


def _parse_utc_hour(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise CarverBlocked("S27 v2 timestamp must be valid ISO datetime") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CarverBlocked("S27 v2 timestamp must be timezone-aware UTC")
    parsed = parsed.astimezone(timezone.utc)
    if parsed.minute or parsed.second or parsed.microsecond:
        raise CarverBlocked("S27 v2 timestamp must be hour-aligned")
    return parsed


def _parse_float(label: str, value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise CarverBlocked(f"{label} must be numeric") from exc


def _require_parsed_family_tuple(parsed_files: tuple[ParsedDeclaredSourceFile, ...]) -> None:
    if tuple(parsed.row_family for parsed in parsed_files) != REQUIRED_ROW_LOCATOR_FAMILIES:
        raise CarverBlocked("S27 v2 parsed source files must match locked row-family tuple")
    for parsed in parsed_files:
        parsed.validate()


def _require_parsed_files_match_declared_local_files(
    inputs: LocalParserFileReplaySlice1Inputs,
    parsed_files: tuple[ParsedDeclaredSourceFile, ...],
) -> None:
    _require_parsed_files_match_input_directory(inputs.input_directory, parsed_files)


def _require_parsed_files_match_input_directory(
    input_directory: ReplayInputDirectoryDeclaration,
    parsed_files: tuple[ParsedDeclaredSourceFile, ...],
) -> None:
    expected_parsed_files = tuple(
        parse_declared_source_file(input_directory, declaration)
        for declaration in input_directory.raw_source_files
    )
    if parsed_files != expected_parsed_files:
        raise CarverBlocked("S27 v2 parsed files must match declared local file bytes")


def _require_raw_file_hash_contract_matches_inputs(
    raw_file_hash_contract: RawSourceFileHashSetContract,
    inputs: LocalParserFileReplaySlice1Inputs,
    parsed_files: tuple[ParsedDeclaredSourceFile, ...],
) -> None:
    if (
        raw_file_hash_contract.input_directory_declaration_hash
        != inputs.input_directory.input_directory_declaration_hash
    ):
        raise CarverBlocked("S27 v2 raw file hash contract must bind active input directory")
    if (
        raw_file_hash_contract.source_universe_manifest_hash
        != inputs.input_directory.source_universe_manifest_hash
    ):
        raise CarverBlocked("S27 v2 raw file hash contract must bind active source universe")
    if raw_file_hash_contract.parser_plan_bundle_hash != inputs.parser_plan_bundle.parser_plan_bundle_hash:
        raise CarverBlocked("S27 v2 raw file hash contract must bind active parser plan")
    if raw_file_hash_contract.raw_file_hash_set_hash != inputs.input_directory.raw_file_hash_set_hash:
        raise CarverBlocked("S27 v2 raw file hash contract must bind active raw file hash set")
    expected_contract = build_raw_file_hash_set_contract(
        inputs.input_directory,
        inputs.parser_plan_bundle,
        parsed_files,
    )
    if raw_file_hash_contract != expected_contract:
        raise CarverBlocked("S27 v2 raw file hash contract must match deterministic active construction")


def _require_parser_output_contract_matches_inputs(
    parser_output_contract: ParserOutputBatchSetContract,
    inputs: LocalParserFileReplaySlice1Inputs,
    parsed_files: tuple[ParsedDeclaredSourceFile, ...],
) -> None:
    if parser_output_contract.raw_file_hash_set_hash != inputs.input_directory.raw_file_hash_set_hash:
        raise CarverBlocked("S27 v2 parser output contract must bind active raw file hash set")
    if parser_output_contract.parser_plan_bundle_hash != inputs.parser_plan_bundle.parser_plan_bundle_hash:
        raise CarverBlocked("S27 v2 parser output contract must bind active parser plan")
    if (
        parser_output_contract.row_locator_contract_bundle_hash
        != inputs.row_locator_contract.row_locator_contract_bundle_hash
    ):
        raise CarverBlocked("S27 v2 parser output contract must bind active row locator")
    if (
        parser_output_contract.canonical_serialization_policy_hash
        != inputs.canonical_serialization_policy.canonical_serialization_policy_hash
    ):
        raise CarverBlocked("S27 v2 parser output contract must bind active canonical policy")
    expected_raw_file_hash_contract = build_raw_file_hash_set_contract(
        inputs.input_directory,
        inputs.parser_plan_bundle,
        parsed_files,
    )
    expected_parser_output_contract = build_parser_output_contract(
        inputs,
        expected_raw_file_hash_contract,
        parsed_files,
    )
    if parser_output_contract != expected_parser_output_contract:
        raise CarverBlocked("S27 v2 parser output contract must match deterministic active construction")


def _require_row_locator_contract_content_bound(inputs: LocalParserFileReplaySlice1Inputs) -> None:
    parser_plan_hash_by_family = _parser_plan_hash_by_row_family(inputs.parser_plan_bundle)
    declaration_by_family = {
        declaration.local_file.expected_row_family: declaration
        for declaration in inputs.input_directory.raw_source_files
    }
    expected_family_hashes: list[str] = []
    for contract in inputs.row_locator_contract.row_family_contracts:
        declaration = declaration_by_family[contract.row_family]
        if contract.raw_file_declaration_hash != canonical_sha256(declaration):
            raise CarverBlocked("S27 v2 row locator family must bind active raw file declaration")
        if contract.parser_family_plan_hash != parser_plan_hash_by_family[contract.row_family]:
            raise CarverBlocked("S27 v2 row locator family must bind active parser plan")
        expected_family_hash = _row_locator_family_contract_hash(contract)
        if contract.family_contract_hash != expected_family_hash:
            raise CarverBlocked("S27 v2 row locator family hash must be content-bound")
        expected_family_hashes.append(expected_family_hash)
    expected_bundle_hash = canonical_sha256(
        {
            "artifact": "S27_V2_ROW_LOCATOR_CONTRACT_BUNDLE",
            "family_contract_hashes": tuple(expected_family_hashes),
            "input_directory_declaration_hash": inputs.row_locator_contract.input_directory_declaration_hash,
            "raw_file_hash_set_hash": inputs.row_locator_contract.raw_file_hash_set_hash,
            "row_locator_policy_hash": inputs.row_locator_contract.row_locator_policy_hash,
            "status": inputs.row_locator_contract.status,
        }
    )
    if inputs.row_locator_contract.row_locator_contract_bundle_hash != expected_bundle_hash:
        raise CarverBlocked("S27 v2 row locator bundle hash must bind active family contracts")


def _require_source_universe_contract_content_bound(inputs: LocalParserFileReplaySlice1Inputs) -> None:
    expected_family_hashes: list[str] = []
    for contract in inputs.source_universe_contract.family_contracts:
        if (
            contract.source_row_locator_family
            != SOURCE_UNIVERSE_FAMILY_TO_ROW_LOCATOR_FAMILY[contract.universe_family]
        ):
            raise CarverBlocked("S27 v2 source universe row-locator family must match locked mapping")
        expected_family_hash = _source_universe_family_contract_hash(contract)
        if contract.family_contract_hash != expected_family_hash:
            raise CarverBlocked("S27 v2 source universe family hash must be content-bound")
        expected_family_hashes.append(expected_family_hash)
    expected_bundle_hash = canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_UNIVERSE_CONTRACT_BUNDLE",
            "family_contract_hashes": tuple(expected_family_hashes),
            "inclusion_rule_hashes": tuple(
                canonical_sha256(rule)
                for rule in inputs.source_universe_contract.inclusion_rules
            ),
            "instrument": inputs.source_universe_contract.instrument,
            "lane": inputs.source_universe_contract.lane,
            "raw_file_hash_set_hash": inputs.source_universe_contract.raw_file_hash_set_hash,
            "requested_end": inputs.source_universe_contract.requested_end,
            "requested_start": inputs.source_universe_contract.requested_start,
            "row_locator_contract_bundle_hash": inputs.source_universe_contract.row_locator_contract_bundle_hash,
            "status": inputs.source_universe_contract.status,
            "strategy_id": inputs.source_universe_contract.strategy_id,
        }
    )
    if inputs.source_universe_contract.source_universe_contract_bundle_hash != expected_bundle_hash:
        raise CarverBlocked("S27 v2 source universe bundle hash must bind active family contracts")


def _row_locator_family_contract_hash(contract: object) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_ROW_LOCATOR_FAMILY_CONTRACT",
            "completed_bar_policy_hash": contract.completed_bar_policy_hash,
            "duplicate_policy_hash": contract.duplicate_policy_hash,
            "expected_output_schema_family": contract.expected_output_schema_family,
            "family_status": contract.family_status,
            "field_binding": contract.field_binding,
            "missing_policy_hash": contract.missing_policy_hash,
            "no_future_rows_proof_hash": contract.no_future_rows_proof_hash,
            "parser_family_plan_hash": contract.parser_family_plan_hash,
            "planned_locator_output_hash": contract.planned_locator_output_hash,
            "planned_row_universe_hash": contract.planned_row_universe_hash,
            "raw_file_declaration_hash": contract.raw_file_declaration_hash,
            "row_family": contract.row_family,
            "strict_prior_policy_hash": contract.strict_prior_policy_hash,
        }
    )


def _source_universe_family_contract_hash(contract: object) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_UNIVERSE_FAMILY_CONTRACT",
            "duplicate_policy_hash": contract.duplicate_policy_hash,
            "family_status": contract.family_status,
            "inclusion_rule_hash": contract.inclusion_rule_hash,
            "missing_policy_hash": contract.missing_policy_hash,
            "no_future_rows_proof_hash": contract.no_future_rows_proof_hash,
            "planned_universe_hash": contract.planned_universe_hash,
            "repair_rejection_policy_hash": contract.repair_rejection_policy_hash,
            "source_row_locator_family": contract.source_row_locator_family,
            "universe_family": contract.universe_family,
        }
    )


def _parser_plan_hash_by_row_family(parser_plan_bundle: ParserPlanBundle) -> dict[str, str]:
    parser_plan_by_name = {
        "DAILY_COMPLETED_BAR_PARSER_PLAN": parser_plan_bundle.daily_parser_plan.family_plan.parser_plan_hash,
        "HOURLY_COMPLETED_BAR_PARSER_PLAN": parser_plan_bundle.hourly_parser_plan.family_plan.parser_plan_hash,
        "SESSION_CALENDAR_PARSER_PLAN": parser_plan_bundle.session_parser_plan.family_plan.parser_plan_hash,
        "ROLL_CALENDAR_PARSER_PLAN": parser_plan_bundle.roll_parser_plan.family_plan.parser_plan_hash,
        "COST_PARAMETER_PARSER_PLAN": parser_plan_bundle.cost_parameter_parser_plan.family_plan.parser_plan_hash,
    }
    return {
        row_family: parser_plan_by_name[parser_name]
        for row_family, parser_name in ROW_FAMILY_TO_PARSER_NAME.items()
    }


def _require_parser_plan_bundle_content_bound(parser_plan_bundle: ParserPlanBundle) -> None:
    family_plans = (
        parser_plan_bundle.daily_parser_plan.family_plan,
        parser_plan_bundle.hourly_parser_plan.family_plan,
        parser_plan_bundle.session_parser_plan.family_plan,
        parser_plan_bundle.roll_parser_plan.family_plan,
        parser_plan_bundle.cost_parameter_parser_plan.family_plan,
    )
    expected_family_plan_hashes = tuple(_parser_family_plan_hash(family_plan) for family_plan in family_plans)
    for family_plan, expected_hash in zip(family_plans, expected_family_plan_hashes, strict=True):
        if family_plan.parser_plan_hash != expected_hash:
            raise CarverBlocked("S27 v2 parser family plan hash must be content-bound")
    expected_bundle_hash = canonical_sha256(
        {
            "artifact": "S27_V2_PARSER_PLAN_BUNDLE",
            "parser_plan_hashes": expected_family_plan_hashes,
        }
    )
    if parser_plan_bundle.parser_plan_bundle_hash != expected_bundle_hash:
        raise CarverBlocked("S27 v2 parser plan bundle hash must bind parser family plans")


def _parser_family_plan_hash(family_plan: object) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_PARSER_FAMILY_PLAN",
            "canonical_row_locator_policy_hash": family_plan.canonical_row_locator_policy_hash,
            "completed_bar_policy_hash": family_plan.completed_bar_policy_hash,
            "degraded_row_policy_hash": family_plan.degraded_row_policy_hash,
            "duplicate_policy_hash": family_plan.duplicate_policy_hash,
            "expected_input_artifact_types": family_plan.expected_input_artifact_types,
            "expected_output_row_schema_family": family_plan.expected_output_row_schema_family,
            "fail_closed_reason_code": family_plan.fail_closed_reason_code,
            "missing_policy_hash": family_plan.missing_policy_hash,
            "parser_extractor_source_hash": family_plan.parser_extractor_source_hash,
            "parser_family_label": family_plan.parser_family_label,
            "strict_prior_policy_hash": family_plan.strict_prior_policy_hash,
        }
    )


def _no_future_rows_proof_hash(
    rows: tuple[
        LocalDailySourceRow
        | LocalHourlySourceRow
        | LocalSessionSourceRow
        | LocalRollSourceRow
        | LocalCostParameterRow,
        ...,
    ],
) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_NO_FUTURE_ROWS_PROOF",
            "row_hashes": tuple(row.row_hash for row in rows),
            "row_locators": tuple(row.row_locator for row in rows),
        }
    )

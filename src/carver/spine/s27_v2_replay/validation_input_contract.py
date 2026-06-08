from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import REQUIRED_UNRESOLVED_GATE_LABELS, S27_V2_REPLAY_NON_AUTHORIZATION
from .cost_contract import CostContractBundle
from .cost_input_contract import CostInputContractBundle
from .evidence_manifest import EvidenceManifest
from .fill_contract import FillContractBundle
from .fill_input_contract import FillInputContractBundle
from .forecast_contract import ForecastContractBundle
from .forecast_input_contract import ForecastInputContractBundle
from .level_compatibility_contract import LevelCompatibilityContractBundle
from .level_compatibility_input_contract import LevelCompatibilityInputContractBundle
from .order_contract import OrderContractBundle
from .order_input_contract import OrderInputContractBundle
from .parser_output_contract import ParserOutputBatchSetContract
from .pnl_contract import PnlContractBundle
from .pnl_input_contract import PnlInputContractBundle
from .position_contract import PositionContractBundle
from .position_input_contract import PositionInputContractBundle
from .runtime_history_contract import RuntimeHistoryContractBundle
from .runtime_history_input_contract import RuntimeHistoryInputContractBundle
from .source_input_manifest_contract import SourceInputManifestContractBundle
from .source_input_selection_contract import SourceRowSelectionExternalAuthorityHandle
from .source_row_batch_contract import SourceRowBatchSetContract
from .trust_root import ReplayTrustRoot
from .validation import (
    require_expected_hash,
    require_hash,
    require_hash_map,
    require_hash_map_matches_active_authority,
    require_matching_dependency_hashes,
    require_non_empty_tuple,
    require_text,
)
from .validation_contract import (
    REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS,
    REQUIRED_VALIDATION_COMPONENT_FAMILIES,
    REQUIRED_VALIDATION_INVARIANTS,
    REQUIRED_VALIDATION_LEDGER_LABELS,
)


S27_V2_VALIDATION_INPUT_CONTRACT_ONLY_STATUS = "S27_V2_VALIDATION_INPUT_CONTRACT_ONLY"
PLANNED_VALIDATION_INPUT_STATUS = "PLANNED_VALIDATION_INPUT_ONLY"

VALIDATION_INPUT_NOT_APPLICABLE = "NOT_APPLICABLE"

VALIDATION_INPUT_SOURCE_KINDS = (
    "TRUST_ROOT_OUTPUT",
    "EVIDENCE_MANIFEST_OUTPUT",
    "SOURCE_INPUT_MANIFEST_OUTPUT",
    "PNL_CONTRACT_OUTPUT",
    "PNL_INPUT_CONTRACT_OUTPUT",
    "VALIDATION_SCHEMA_OUTPUT",
    "PROVENANCE_SCHEMA_OUTPUT",
    "LOCAL_AUDIT_SCHEMA_OUTPUT",
    "UNRESOLVED_GATE_SET",
    "POLICY_INPUT",
)

REQUIRED_VALIDATION_INPUTS = (
    "VALIDATION_TRUST_ROOT_HASH_INPUT",
    "VALIDATION_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT",
    "VALIDATION_SOURCE_INPUT_MANIFEST_HASH_INPUT",
    "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT",
    "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT",
    "VALIDATION_LEDGER_SCHEMA_HASH_INPUT",
    "VALIDATION_PROVENANCE_LEDGER_SCHEMA_HASH_INPUT",
    "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT",
    "VALIDATION_REQUIRED_ARTIFACT_FAMILY_POLICY_INPUT",
    "VALIDATION_PROVENANCE_HASH_CHAIN_POLICY_INPUT",
    "VALIDATION_FAIL_CLOSED_GATE_POLICY_INPUT",
    "VALIDATION_STALE_EVIDENCE_SUPERSESSION_POLICY_INPUT",
    "VALIDATION_LOCAL_HOSTILE_AUDIT_POLICY_INPUT",
    "VALIDATION_EXTERNAL_AUDIT_PACKET_POLICY_INPUT",
    "VALIDATION_UNRESOLVED_GATE_SET_INPUT",
    "VALIDATION_NO_EXECUTION_POLICY_INPUT",
    "VALIDATION_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT",
)

REQUIRED_SOURCE_KIND_BY_VALIDATION_INPUT = {
    "VALIDATION_TRUST_ROOT_HASH_INPUT": "TRUST_ROOT_OUTPUT",
    "VALIDATION_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": "EVIDENCE_MANIFEST_OUTPUT",
    "VALIDATION_SOURCE_INPUT_MANIFEST_HASH_INPUT": "SOURCE_INPUT_MANIFEST_OUTPUT",
    "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT": "PNL_CONTRACT_OUTPUT",
    "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT": "PNL_INPUT_CONTRACT_OUTPUT",
    "VALIDATION_LEDGER_SCHEMA_HASH_INPUT": "VALIDATION_SCHEMA_OUTPUT",
    "VALIDATION_PROVENANCE_LEDGER_SCHEMA_HASH_INPUT": "PROVENANCE_SCHEMA_OUTPUT",
    "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT": "LOCAL_AUDIT_SCHEMA_OUTPUT",
    "VALIDATION_REQUIRED_ARTIFACT_FAMILY_POLICY_INPUT": "POLICY_INPUT",
    "VALIDATION_PROVENANCE_HASH_CHAIN_POLICY_INPUT": "POLICY_INPUT",
    "VALIDATION_FAIL_CLOSED_GATE_POLICY_INPUT": "POLICY_INPUT",
    "VALIDATION_STALE_EVIDENCE_SUPERSESSION_POLICY_INPUT": "POLICY_INPUT",
    "VALIDATION_LOCAL_HOSTILE_AUDIT_POLICY_INPUT": "POLICY_INPUT",
    "VALIDATION_EXTERNAL_AUDIT_PACKET_POLICY_INPUT": "POLICY_INPUT",
    "VALIDATION_UNRESOLVED_GATE_SET_INPUT": "UNRESOLVED_GATE_SET",
    "VALIDATION_NO_EXECUTION_POLICY_INPUT": "POLICY_INPUT",
    "VALIDATION_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT": "POLICY_INPUT",
}

REQUIRED_TRUST_ROOT_OUTPUT_BY_VALIDATION_INPUT = {
    "VALIDATION_TRUST_ROOT_HASH_INPUT": "REPLAY_TRUST_ROOT_HASH",
}

REQUIRED_EVIDENCE_MANIFEST_OUTPUT_BY_VALIDATION_INPUT = {
    "VALIDATION_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": "ACTIVE_EVIDENCE_MANIFEST_HASH",
}

REQUIRED_SOURCE_INPUT_MANIFEST_OUTPUT_BY_VALIDATION_INPUT = {
    "VALIDATION_SOURCE_INPUT_MANIFEST_HASH_INPUT": "SOURCE_INPUT_MANIFEST_HASH",
}

REQUIRED_PNL_CONTRACT_OUTPUT_BY_VALIDATION_INPUT = {
    "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT": "PNL_CONTRACT_BUNDLE_HASH",
}

REQUIRED_PNL_INPUT_CONTRACT_OUTPUT_BY_VALIDATION_INPUT = {
    "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT": "PNL_INPUT_CONTRACT_HASH",
}

REQUIRED_VALIDATION_SCHEMA_OUTPUT_BY_VALIDATION_INPUT = {
    "VALIDATION_LEDGER_SCHEMA_HASH_INPUT": "VALIDATION_LEDGER_SCHEMA_HASH",
}

REQUIRED_PROVENANCE_SCHEMA_OUTPUT_BY_VALIDATION_INPUT = {
    "VALIDATION_PROVENANCE_LEDGER_SCHEMA_HASH_INPUT": "PROVENANCE_AND_HASH_LEDGER_SCHEMA_HASH",
}

REQUIRED_LOCAL_AUDIT_SCHEMA_OUTPUT_BY_VALIDATION_INPUT = {
    "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT": "LOCAL_HOSTILE_AUDIT_RESULT_SCHEMA_HASH",
}

REQUIRED_POLICY_LABEL_BY_VALIDATION_INPUT = {
    "VALIDATION_REQUIRED_ARTIFACT_FAMILY_POLICY_INPUT": "REQUIRED_ARTIFACT_FAMILY_POLICY",
    "VALIDATION_PROVENANCE_HASH_CHAIN_POLICY_INPUT": "PROVENANCE_HASH_CHAIN_POLICY",
    "VALIDATION_FAIL_CLOSED_GATE_POLICY_INPUT": "FAIL_CLOSED_GATE_POLICY",
    "VALIDATION_STALE_EVIDENCE_SUPERSESSION_POLICY_INPUT": "STALE_EVIDENCE_SUPERSESSION_POLICY",
    "VALIDATION_LOCAL_HOSTILE_AUDIT_POLICY_INPUT": "LOCAL_HOSTILE_AUDIT_POLICY",
    "VALIDATION_EXTERNAL_AUDIT_PACKET_POLICY_INPUT": "EXTERNAL_AUDIT_PACKET_POLICY",
    "VALIDATION_NO_EXECUTION_POLICY_INPUT": "NO_PARSER_REPLAY_EXECUTION_IN_VALIDATION_CONTRACT",
    "VALIDATION_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT": "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM_IN_VALIDATION_CONTRACT",
}

REQUIRED_UNRESOLVED_GATE_SET_BY_VALIDATION_INPUT = {
    "VALIDATION_UNRESOLVED_GATE_SET_INPUT": "REQUIRED_UNRESOLVED_GATE_LABELS",
}

REQUIRED_VALIDATION_DEPENDENCIES_BY_COMPONENT = {
    "TRUST_ROOT_REFERENCE": (
        "VALIDATION_TRUST_ROOT_HASH_INPUT",
    ),
    "EVIDENCE_MANIFEST_REFERENCE": (
        "VALIDATION_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT",
        "VALIDATION_SOURCE_INPUT_MANIFEST_HASH_INPUT",
    ),
    "REQUIRED_LEDGER_FAMILY_COVERAGE": (
        "VALIDATION_REQUIRED_ARTIFACT_FAMILY_POLICY_INPUT",
        "VALIDATION_LEDGER_SCHEMA_HASH_INPUT",
        "VALIDATION_PROVENANCE_LEDGER_SCHEMA_HASH_INPUT",
        "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT",
    ),
    "PROVENANCE_HASH_CHAIN": (
        "VALIDATION_PROVENANCE_HASH_CHAIN_POLICY_INPUT",
        "VALIDATION_TRUST_ROOT_HASH_INPUT",
        "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT",
        "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT",
    ),
    "FAIL_CLOSED_GATE_STATUS": (
        "VALIDATION_FAIL_CLOSED_GATE_POLICY_INPUT",
        "VALIDATION_UNRESOLVED_GATE_SET_INPUT",
    ),
    "LOCAL_HOSTILE_AUDIT_PACKET": (
        "VALIDATION_LOCAL_HOSTILE_AUDIT_POLICY_INPUT",
        "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT",
    ),
    "SUPERSESSION_MANIFEST": (
        "VALIDATION_STALE_EVIDENCE_SUPERSESSION_POLICY_INPUT",
        "EVIDENCE_MANIFEST_REFERENCE",
    ),
    "NON_AUTHORIZATION_PRESERVATION": (
        "VALIDATION_NO_EXECUTION_POLICY_INPUT",
        "VALIDATION_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT",
    ),
}

REQUIRED_VALIDATION_DEPENDENCIES_BY_LEDGER = {
    "VALIDATION_LEDGER": (
        "TRUST_ROOT_REFERENCE",
        "EVIDENCE_MANIFEST_REFERENCE",
        "REQUIRED_LEDGER_FAMILY_COVERAGE",
        "FAIL_CLOSED_GATE_STATUS",
    ),
    "PROVENANCE_AND_HASH_LEDGER": (
        "TRUST_ROOT_REFERENCE",
        "PROVENANCE_HASH_CHAIN",
        "SUPERSESSION_MANIFEST",
    ),
    "LOCAL_HOSTILE_AUDIT_RESULT": (
        "LOCAL_HOSTILE_AUDIT_PACKET",
        "NON_AUTHORIZATION_PRESERVATION",
    ),
}

REQUIRED_VALIDATION_DEPENDENCIES_BY_AUDIT_CHECKPOINT = {
    "SCHEMA_AND_TRUST_ROOT_CODE": (
        "TRUST_ROOT_REFERENCE",
        "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT",
        "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT",
    ),
    "FAIL_CLOSED_ROW_PATHS": (
        "FAIL_CLOSED_GATE_STATUS",
    ),
    "DAILY_HOURLY_LEVEL_COMPATIBILITY_AND_SIGMA_BRIDGE": (
        "EVIDENCE_MANIFEST_REFERENCE",
        "PROVENANCE_HASH_CHAIN",
    ),
    "FORECAST_ARITHMETIC_AND_GATES": (
        "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT",
        "PROVENANCE_HASH_CHAIN",
    ),
    "ORDER_FILL_COST_PNL_PROVENANCE": (
        "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT",
        "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT",
        "PROVENANCE_HASH_CHAIN",
    ),
    "EXTERNAL_AUDIT_PACKET_AFTER_ARTIFACTS_EXIST": (
        "VALIDATION_EXTERNAL_AUDIT_PACKET_POLICY_INPUT",
        "LOCAL_HOSTILE_AUDIT_PACKET",
        "NON_AUTHORIZATION_PRESERVATION",
    ),
}

REQUIRED_VALIDATION_DEPENDENCIES_BY_INVARIANT = {
    "ACTIVE_EVIDENCE_MANIFEST_HASH_BINDING": (
        "VALIDATION_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT",
        "EVIDENCE_MANIFEST_REFERENCE",
    ),
    "REQUIRED_ARTIFACT_FAMILY_COVERAGE": (
        "REQUIRED_LEDGER_FAMILY_COVERAGE",
    ),
    "TRUST_ROOT_EVIDENCE_MANIFEST_CROSS_CHECK": (
        "TRUST_ROOT_REFERENCE",
        "EVIDENCE_MANIFEST_REFERENCE",
    ),
    "VALIDATION_LEDGER_HASH_BINDING": (
        "VALIDATION_LEDGER",
        "VALIDATION_LEDGER_SCHEMA_HASH_INPUT",
    ),
    "PROVENANCE_AND_HASH_LEDGER_BINDING": (
        "PROVENANCE_AND_HASH_LEDGER",
        "VALIDATION_PROVENANCE_LEDGER_SCHEMA_HASH_INPUT",
    ),
    "LOCAL_HOSTILE_AUDIT_RESULT_BINDING": (
        "LOCAL_HOSTILE_AUDIT_RESULT",
        "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT",
    ),
    "STALE_EVIDENCE_SUPERSESSION_BINDING": (
        "SUPERSESSION_MANIFEST",
    ),
    "FAIL_CLOSED_UNRESOLVED_GATES_BINDING": (
        "FAIL_CLOSED_GATE_STATUS",
        "VALIDATION_UNRESOLVED_GATE_SET_INPUT",
    ),
    "NO_PARSER_REPLAY_EXECUTION_IN_VALIDATION_CONTRACT": (
        "VALIDATION_NO_EXECUTION_POLICY_INPUT",
        "NON_AUTHORIZATION_PRESERVATION",
    ),
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM_IN_VALIDATION_CONTRACT": (
        "VALIDATION_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT",
        "NON_AUTHORIZATION_PRESERVATION",
    ),
}


@dataclass(frozen=True)
class ValidationInputFieldContract:
    input_label: str
    input_status: str
    source_kind: str
    trust_root_output_label: str
    evidence_manifest_output_label: str
    source_input_manifest_output_label: str
    pnl_contract_output_label: str
    pnl_input_contract_output_label: str
    validation_schema_output_label: str
    provenance_schema_output_label: str
    local_audit_schema_output_label: str
    unresolved_gate_set_label: str
    unresolved_gate_labels: tuple[str, ...]
    source_policy_label: str
    source_contract_hash: str
    validation_input_policy_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 validation input label", self.input_label)
        if self.input_label not in REQUIRED_VALIDATION_INPUTS:
            raise CarverBlocked("S27 v2 validation input label is not locked")
        require_text("S27 v2 validation input status", self.input_status)
        if self.input_status != PLANNED_VALIDATION_INPUT_STATUS:
            raise CarverBlocked("S27 v2 validation input must remain planned-only")
        require_text("S27 v2 validation input source kind", self.source_kind)
        if self.source_kind not in VALIDATION_INPUT_SOURCE_KINDS:
            raise CarverBlocked("S27 v2 validation input source kind is not locked")
        if self.source_kind != REQUIRED_SOURCE_KIND_BY_VALIDATION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 validation input must use the locked source kind")
        self._validate_source_target()
        require_hash("S27 v2 validation input source contract hash", self.source_contract_hash)
        require_hash("S27 v2 validation input policy hash", self.validation_input_policy_hash)
        require_hash("S27 v2 validation input field contract hash", self.input_field_contract_hash)

    def _validate_source_target(self) -> None:
        if self.source_kind == "TRUST_ROOT_OUTPUT":
            self._validate_trust_root_output_target()
        elif self.source_kind == "EVIDENCE_MANIFEST_OUTPUT":
            self._validate_evidence_manifest_output_target()
        elif self.source_kind == "SOURCE_INPUT_MANIFEST_OUTPUT":
            self._validate_source_input_manifest_output_target()
        elif self.source_kind == "PNL_CONTRACT_OUTPUT":
            self._validate_pnl_contract_output_target()
        elif self.source_kind == "PNL_INPUT_CONTRACT_OUTPUT":
            self._validate_pnl_input_contract_output_target()
        elif self.source_kind == "VALIDATION_SCHEMA_OUTPUT":
            self._validate_validation_schema_output_target()
        elif self.source_kind == "PROVENANCE_SCHEMA_OUTPUT":
            self._validate_provenance_schema_output_target()
        elif self.source_kind == "LOCAL_AUDIT_SCHEMA_OUTPUT":
            self._validate_local_audit_schema_output_target()
        elif self.source_kind == "UNRESOLVED_GATE_SET":
            self._validate_unresolved_gate_set_target()
        elif self.source_kind == "POLICY_INPUT":
            self._validate_policy_input_target()

    def _require_not_applicable(self, name: str, value: str) -> None:
        require_text(name, value)
        if value != VALIDATION_INPUT_NOT_APPLICABLE:
            raise CarverBlocked(f"{name} must be not applicable")

    def _require_common_targets_not_applicable(self, exempt_name: str) -> None:
        targets = (
            ("S27 v2 validation trust-root output label", self.trust_root_output_label),
            ("S27 v2 validation evidence-manifest output label", self.evidence_manifest_output_label),
            (
                "S27 v2 validation source-input manifest output label",
                self.source_input_manifest_output_label,
            ),
            ("S27 v2 validation PnL contract output label", self.pnl_contract_output_label),
            (
                "S27 v2 validation PnL input contract output label",
                self.pnl_input_contract_output_label,
            ),
            ("S27 v2 validation ledger schema output label", self.validation_schema_output_label),
            ("S27 v2 validation provenance schema output label", self.provenance_schema_output_label),
            ("S27 v2 validation local audit schema output label", self.local_audit_schema_output_label),
            ("S27 v2 validation unresolved gate-set label", self.unresolved_gate_set_label),
            ("S27 v2 validation source policy label", self.source_policy_label),
        )
        for name, value in targets:
            if name != exempt_name:
                self._require_not_applicable(name, value)
        if exempt_name != "S27 v2 validation unresolved gate-set label":
            if self.unresolved_gate_labels != (VALIDATION_INPUT_NOT_APPLICABLE,):
                raise CarverBlocked("S27 v2 validation unresolved gate labels must be not applicable")

    def _validate_trust_root_output_target(self) -> None:
        require_text("S27 v2 validation trust-root output label", self.trust_root_output_label)
        if self.trust_root_output_label != REQUIRED_TRUST_ROOT_OUTPUT_BY_VALIDATION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 validation input must use the locked trust-root output")
        self._require_common_targets_not_applicable("S27 v2 validation trust-root output label")

    def _validate_evidence_manifest_output_target(self) -> None:
        require_text(
            "S27 v2 validation evidence-manifest output label",
            self.evidence_manifest_output_label,
        )
        if (
            self.evidence_manifest_output_label
            != REQUIRED_EVIDENCE_MANIFEST_OUTPUT_BY_VALIDATION_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 validation input must use the locked evidence-manifest output")
        self._require_common_targets_not_applicable("S27 v2 validation evidence-manifest output label")

    def _validate_source_input_manifest_output_target(self) -> None:
        require_text(
            "S27 v2 validation source-input manifest output label",
            self.source_input_manifest_output_label,
        )
        if (
            self.source_input_manifest_output_label
            != REQUIRED_SOURCE_INPUT_MANIFEST_OUTPUT_BY_VALIDATION_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 validation input must use the locked source-input manifest output")
        self._require_common_targets_not_applicable("S27 v2 validation source-input manifest output label")

    def _validate_pnl_contract_output_target(self) -> None:
        require_text("S27 v2 validation PnL contract output label", self.pnl_contract_output_label)
        if self.pnl_contract_output_label != REQUIRED_PNL_CONTRACT_OUTPUT_BY_VALIDATION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 validation input must use the locked PnL contract output")
        self._require_common_targets_not_applicable("S27 v2 validation PnL contract output label")

    def _validate_pnl_input_contract_output_target(self) -> None:
        require_text(
            "S27 v2 validation PnL input contract output label",
            self.pnl_input_contract_output_label,
        )
        if (
            self.pnl_input_contract_output_label
            != REQUIRED_PNL_INPUT_CONTRACT_OUTPUT_BY_VALIDATION_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 validation input must use the locked PnL input contract output")
        self._require_common_targets_not_applicable("S27 v2 validation PnL input contract output label")

    def _validate_validation_schema_output_target(self) -> None:
        require_text("S27 v2 validation ledger schema output label", self.validation_schema_output_label)
        if self.validation_schema_output_label != REQUIRED_VALIDATION_SCHEMA_OUTPUT_BY_VALIDATION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 validation input must use the locked validation schema output")
        self._require_common_targets_not_applicable("S27 v2 validation ledger schema output label")

    def _validate_provenance_schema_output_target(self) -> None:
        require_text(
            "S27 v2 validation provenance schema output label",
            self.provenance_schema_output_label,
        )
        if self.provenance_schema_output_label != REQUIRED_PROVENANCE_SCHEMA_OUTPUT_BY_VALIDATION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 validation input must use the locked provenance schema output")
        self._require_common_targets_not_applicable("S27 v2 validation provenance schema output label")

    def _validate_local_audit_schema_output_target(self) -> None:
        require_text(
            "S27 v2 validation local audit schema output label",
            self.local_audit_schema_output_label,
        )
        if self.local_audit_schema_output_label != REQUIRED_LOCAL_AUDIT_SCHEMA_OUTPUT_BY_VALIDATION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 validation input must use the locked local audit schema output")
        self._require_common_targets_not_applicable("S27 v2 validation local audit schema output label")

    def _validate_unresolved_gate_set_target(self) -> None:
        require_text("S27 v2 validation unresolved gate-set label", self.unresolved_gate_set_label)
        if self.unresolved_gate_set_label != REQUIRED_UNRESOLVED_GATE_SET_BY_VALIDATION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 validation input must use the locked unresolved gate-set label")
        if self.unresolved_gate_labels != REQUIRED_UNRESOLVED_GATE_LABELS:
            raise CarverBlocked("S27 v2 validation input must bind complete unresolved gate tuple")
        self._require_common_targets_not_applicable("S27 v2 validation unresolved gate-set label")

    def _validate_policy_input_target(self) -> None:
        require_text("S27 v2 validation source policy label", self.source_policy_label)
        if self.source_policy_label != REQUIRED_POLICY_LABEL_BY_VALIDATION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 validation input must use the locked policy label")
        self._require_common_targets_not_applicable("S27 v2 validation source policy label")


@dataclass(frozen=True)
class ValidationDependencyBindingContract:
    dependency_label: str
    required_dependency_labels: tuple[str, ...]
    required_dependency_contract_hashes: tuple[str, ...]
    dependency_binding_policy_hash: str
    dependency_binding_contract_hash: str

    def validate_component(self) -> None:
        require_text("S27 v2 validation component dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_VALIDATION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 validation component dependency label is not locked")
        self._validate_required_dependencies(
            REQUIRED_VALIDATION_DEPENDENCIES_BY_COMPONENT[self.dependency_label],
        )

    def validate_ledger(self) -> None:
        require_text("S27 v2 validation ledger dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_VALIDATION_LEDGER_LABELS:
            raise CarverBlocked("S27 v2 validation ledger dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_VALIDATION_DEPENDENCIES_BY_LEDGER[self.dependency_label])

    def validate_audit_checkpoint(self) -> None:
        require_text("S27 v2 validation audit-checkpoint dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS:
            raise CarverBlocked("S27 v2 validation audit-checkpoint dependency label is not locked")
        self._validate_required_dependencies(
            REQUIRED_VALIDATION_DEPENDENCIES_BY_AUDIT_CHECKPOINT[self.dependency_label],
        )

    def validate_invariant(self) -> None:
        require_text("S27 v2 validation invariant dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_VALIDATION_INVARIANTS:
            raise CarverBlocked("S27 v2 validation invariant dependency label is not locked")
        self._validate_required_dependencies(
            REQUIRED_VALIDATION_DEPENDENCIES_BY_INVARIANT[self.dependency_label],
        )

    def _validate_required_dependencies(self, locked_labels: tuple[str, ...]) -> None:
        require_non_empty_tuple("S27 v2 validation required dependency labels", self.required_dependency_labels)
        if self.required_dependency_labels != locked_labels:
            raise CarverBlocked("S27 v2 validation dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 validation required dependency contract hashes",
            self.required_dependency_contract_hashes,
        )
        if len(self.required_dependency_contract_hashes) != len(self.required_dependency_labels):
            raise CarverBlocked("S27 v2 validation dependency hashes must match labels")
        for dependency_hash in self.required_dependency_contract_hashes:
            require_hash("S27 v2 validation dependency contract hash", dependency_hash)
        require_hash("S27 v2 validation dependency binding policy hash", self.dependency_binding_policy_hash)
        require_hash("S27 v2 validation dependency binding contract hash", self.dependency_binding_contract_hash)


@dataclass(frozen=True)
class ValidationInputContractBundle:
    status: str
    replay_trust_root_hash: str
    active_evidence_manifest_hash: str
    source_input_manifest_hash: str
    source_input_manifest_contract_hash: str
    pnl_input_contract_hash: str
    pnl_contract_bundle_hash: str
    validation_contract_bundle_hash: str
    validation_ledger_schema_hash: str
    provenance_ledger_schema_hash: str
    local_hostile_audit_schema_hash: str
    validation_input_policy_hash: str
    input_field_contracts: tuple[ValidationInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    component_dependency_bindings: tuple[ValidationDependencyBindingContract, ...]
    ledger_dependency_bindings: tuple[ValidationDependencyBindingContract, ...]
    audit_checkpoint_dependency_bindings: tuple[ValidationDependencyBindingContract, ...]
    invariant_dependency_bindings: tuple[ValidationDependencyBindingContract, ...]
    validation_input_set_hash: str
    validation_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 validation input requires PnL and trust authority"
        )

    def validate_against_pnl_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
        source_input_manifest_contract: SourceInputManifestContractBundle,
        level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
        level_compatibility_contract: LevelCompatibilityContractBundle,
        runtime_history_input_contract: RuntimeHistoryInputContractBundle,
        runtime_history_contract: RuntimeHistoryContractBundle,
        forecast_input_contract: ForecastInputContractBundle,
        forecast_contract: ForecastContractBundle,
        position_input_contract: PositionInputContractBundle,
        position_contract: PositionContractBundle,
        order_input_contract: OrderInputContractBundle,
        order_contract: OrderContractBundle,
        fill_input_contract: FillInputContractBundle,
        fill_contract: FillContractBundle,
        cost_input_contract: CostInputContractBundle,
        cost_contract: CostContractBundle,
        pnl_input_contract: PnlInputContractBundle,
        pnl_contract: PnlContractBundle,
    ) -> None:
        pnl_input_contract.validate_against_cost_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
            source_input_manifest_contract,
            level_compatibility_input_contract,
            level_compatibility_contract,
            runtime_history_input_contract,
            runtime_history_contract,
            forecast_input_contract,
            forecast_contract,
            position_input_contract,
            position_contract,
            order_input_contract,
            order_contract,
            fill_input_contract,
            fill_contract,
            cost_input_contract,
            cost_contract,
        )
        pnl_contract.validate()
        require_text("S27 v2 validation input contract status", self.status)
        if self.status != S27_V2_VALIDATION_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 validation input contract must remain contract-only")
        self._validate_locked_maps()
        require_hash("S27 v2 validation replay trust-root hash", self.replay_trust_root_hash)
        require_hash("S27 v2 validation active evidence-manifest hash", self.active_evidence_manifest_hash)
        require_hash("S27 v2 validation source-input manifest hash", self.source_input_manifest_hash)
        require_hash(
            "S27 v2 validation source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash("S27 v2 validation PnL input contract hash", self.pnl_input_contract_hash)
        require_hash("S27 v2 validation PnL contract bundle hash", self.pnl_contract_bundle_hash)
        require_hash("S27 v2 validation contract bundle hash", self.validation_contract_bundle_hash)
        require_hash("S27 v2 validation ledger schema hash", self.validation_ledger_schema_hash)
        require_hash("S27 v2 validation provenance ledger schema hash", self.provenance_ledger_schema_hash)
        require_hash("S27 v2 validation local hostile audit schema hash", self.local_hostile_audit_schema_hash)
        require_hash("S27 v2 validation input policy hash", self.validation_input_policy_hash)
        require_hash_map(
            "S27 v2 validation expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_VALIDATION_INPUTS,
        )
        self._validate_pnl_authority(
            replay_trust_root,
            evidence_manifest,
            source_input_manifest_contract,
            pnl_input_contract,
            pnl_contract,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 validation expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(
                replay_trust_root,
                evidence_manifest,
                source_input_manifest_contract,
                pnl_input_contract,
                pnl_contract,
            ),
            REQUIRED_VALIDATION_INPUTS,
        )
        dependency_hash_by_label = self._validate_input_fields()
        self._validate_component_dependencies(dependency_hash_by_label)
        self._validate_ledger_dependencies(dependency_hash_by_label)
        self._validate_audit_checkpoint_dependencies(dependency_hash_by_label)
        self._validate_invariant_dependencies(dependency_hash_by_label)
        require_hash("S27 v2 validation input set hash", self.validation_input_set_hash)
        require_hash("S27 v2 validation input contract hash", self.validation_input_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 validation input contract must preserve non-authorizations")

    def _validate_locked_maps(self) -> None:
        if tuple(REQUIRED_SOURCE_KIND_BY_VALIDATION_INPUT) != REQUIRED_VALIDATION_INPUTS:
            raise CarverBlocked("S27 v2 validation input source-kind map must cover locked inputs")
        if tuple(REQUIRED_VALIDATION_DEPENDENCIES_BY_COMPONENT) != REQUIRED_VALIDATION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 validation component dependency map must cover locked components")
        if tuple(REQUIRED_VALIDATION_DEPENDENCIES_BY_LEDGER) != REQUIRED_VALIDATION_LEDGER_LABELS:
            raise CarverBlocked("S27 v2 validation ledger dependency map must cover locked ledgers")
        if (
            tuple(REQUIRED_VALIDATION_DEPENDENCIES_BY_AUDIT_CHECKPOINT)
            != REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS
        ):
            raise CarverBlocked("S27 v2 validation audit-checkpoint map must cover locked checkpoints")
        if tuple(REQUIRED_VALIDATION_DEPENDENCIES_BY_INVARIANT) != REQUIRED_VALIDATION_INVARIANTS:
            raise CarverBlocked("S27 v2 validation invariant dependency map must cover locked invariants")

    def _active_source_contract_hash_by_input_label(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_input_manifest_contract: SourceInputManifestContractBundle,
        pnl_input_contract: PnlInputContractBundle,
        pnl_contract: PnlContractBundle,
    ) -> dict[str, str]:
        active_hash_by_label: dict[str, str] = {}
        for input_label in REQUIRED_VALIDATION_INPUTS:
            source_kind = REQUIRED_SOURCE_KIND_BY_VALIDATION_INPUT[input_label]
            if source_kind == "TRUST_ROOT_OUTPUT":
                active_hash_by_label[input_label] = replay_trust_root.replay_trust_root_hash
            elif source_kind == "EVIDENCE_MANIFEST_OUTPUT":
                active_hash_by_label[input_label] = evidence_manifest.active_evidence_manifest_hash
            elif source_kind == "SOURCE_INPUT_MANIFEST_OUTPUT":
                active_hash_by_label[input_label] = source_input_manifest_contract.source_input_manifest_hash
            elif source_kind == "PNL_CONTRACT_OUTPUT":
                active_hash_by_label[input_label] = pnl_contract.pnl_contract_bundle_hash
            elif source_kind == "PNL_INPUT_CONTRACT_OUTPUT":
                active_hash_by_label[input_label] = pnl_input_contract.pnl_input_contract_hash
            elif source_kind == "VALIDATION_SCHEMA_OUTPUT":
                active_hash_by_label[input_label] = self.validation_ledger_schema_hash
            elif source_kind == "PROVENANCE_SCHEMA_OUTPUT":
                active_hash_by_label[input_label] = self.provenance_ledger_schema_hash
            elif source_kind == "LOCAL_AUDIT_SCHEMA_OUTPUT":
                active_hash_by_label[input_label] = self.local_hostile_audit_schema_hash
            elif source_kind in {"UNRESOLVED_GATE_SET", "POLICY_INPUT"}:
                active_hash_by_label[input_label] = self.validation_input_policy_hash
            else:
                raise CarverBlocked("S27 v2 validation input source kind cannot be authority-bound")
        return active_hash_by_label

    def _validate_pnl_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_input_manifest_contract: SourceInputManifestContractBundle,
        pnl_input_contract: PnlInputContractBundle,
        pnl_contract: PnlContractBundle,
    ) -> None:
        active_source_hash_by_input_label = self._active_source_contract_hash_by_input_label(
            replay_trust_root,
            evidence_manifest,
            source_input_manifest_contract,
            pnl_input_contract,
            pnl_contract,
        )
        observed_source_hash_by_input_label = {
            "VALIDATION_TRUST_ROOT_HASH_INPUT": self.replay_trust_root_hash,
            "VALIDATION_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": self.active_evidence_manifest_hash,
            "VALIDATION_SOURCE_INPUT_MANIFEST_HASH_INPUT": self.source_input_manifest_hash,
            "VALIDATION_PNL_CONTRACT_BUNDLE_HASH_INPUT": self.pnl_contract_bundle_hash,
            "VALIDATION_PNL_INPUT_CONTRACT_HASH_INPUT": self.pnl_input_contract_hash,
            "VALIDATION_LEDGER_SCHEMA_HASH_INPUT": self.validation_ledger_schema_hash,
            "VALIDATION_PROVENANCE_LEDGER_SCHEMA_HASH_INPUT": self.provenance_ledger_schema_hash,
            "VALIDATION_LOCAL_HOSTILE_AUDIT_SCHEMA_HASH_INPUT": self.local_hostile_audit_schema_hash,
            "VALIDATION_REQUIRED_ARTIFACT_FAMILY_POLICY_INPUT": self.validation_input_policy_hash,
            "VALIDATION_PROVENANCE_HASH_CHAIN_POLICY_INPUT": self.validation_input_policy_hash,
            "VALIDATION_FAIL_CLOSED_GATE_POLICY_INPUT": self.validation_input_policy_hash,
            "VALIDATION_STALE_EVIDENCE_SUPERSESSION_POLICY_INPUT": self.validation_input_policy_hash,
            "VALIDATION_LOCAL_HOSTILE_AUDIT_POLICY_INPUT": self.validation_input_policy_hash,
            "VALIDATION_EXTERNAL_AUDIT_PACKET_POLICY_INPUT": self.validation_input_policy_hash,
            "VALIDATION_UNRESOLVED_GATE_SET_INPUT": self.validation_input_policy_hash,
            "VALIDATION_NO_EXECUTION_POLICY_INPUT": self.validation_input_policy_hash,
            "VALIDATION_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT": self.validation_input_policy_hash,
        }
        require_hash_map_matches_active_authority(
            "S27 v2 validation routed authority",
            observed_source_hash_by_input_label,
            active_source_hash_by_input_label,
            REQUIRED_VALIDATION_INPUTS,
        )
        if source_input_manifest_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 validation input must bind source-input manifest contract")
        if pnl_input_contract.pnl_input_contract_hash != self.pnl_input_contract_hash:
            raise CarverBlocked("S27 v2 validation input must bind PnL input contract")
        if pnl_contract.pnl_contract_bundle_hash != self.pnl_contract_bundle_hash:
            raise CarverBlocked("S27 v2 validation input must bind PnL contract bundle")
        if pnl_input_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 validation input must bind PnL source-input manifest")
        if pnl_contract.source_binding.replay_trust_root_hash != replay_trust_root.replay_trust_root_hash:
            raise CarverBlocked("S27 v2 validation input must bind PnL replay trust root")
        if pnl_contract.source_binding.source_input_manifest_hash != source_input_manifest_contract.source_input_manifest_hash:
            raise CarverBlocked("S27 v2 validation input must bind PnL source manifest hash")

    def _validate_input_fields(self) -> dict[str, str]:
        require_non_empty_tuple("S27 v2 validation input field contracts", self.input_field_contracts)
        seen_inputs: set[str] = set()
        dependency_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 validation input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 validation input source contract hash",
                contract.input_label,
                contract.source_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            dependency_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_VALIDATION_INPUTS:
            raise CarverBlocked("S27 v2 validation inputs must match locked input tuple")
        return dependency_hash_by_label

    def _validate_component_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 validation component dependency bindings",
            self.component_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.component_dependency_bindings)
            != REQUIRED_VALIDATION_COMPONENT_FAMILIES
        ):
            raise CarverBlocked("S27 v2 validation component dependencies must match locked components")
        seen_components: set[str] = set()
        for binding in self.component_dependency_bindings:
            binding.validate_component()
            if binding.dependency_label in seen_components:
                raise CarverBlocked("S27 v2 validation component dependency bindings must be unique")
            seen_components.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_ledger_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 validation ledger dependency bindings",
            self.ledger_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.ledger_dependency_bindings)
            != REQUIRED_VALIDATION_LEDGER_LABELS
        ):
            raise CarverBlocked("S27 v2 validation ledger dependencies must match locked ledgers")
        seen_ledgers: set[str] = set()
        for binding in self.ledger_dependency_bindings:
            binding.validate_ledger()
            if binding.dependency_label in seen_ledgers:
                raise CarverBlocked("S27 v2 validation ledger dependency bindings must be unique")
            seen_ledgers.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_audit_checkpoint_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 validation audit-checkpoint dependency bindings",
            self.audit_checkpoint_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.audit_checkpoint_dependency_bindings)
            != REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS
        ):
            raise CarverBlocked("S27 v2 validation audit-checkpoint dependencies must match locked checkpoints")
        seen_checkpoints: set[str] = set()
        for binding in self.audit_checkpoint_dependency_bindings:
            binding.validate_audit_checkpoint()
            if binding.dependency_label in seen_checkpoints:
                raise CarverBlocked("S27 v2 validation audit-checkpoint bindings must be unique")
            seen_checkpoints.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_invariant_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 validation invariant dependency bindings",
            self.invariant_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.invariant_dependency_bindings)
            != REQUIRED_VALIDATION_INVARIANTS
        ):
            raise CarverBlocked("S27 v2 validation invariant dependencies must match locked invariants")
        seen_invariants: set[str] = set()
        for binding in self.invariant_dependency_bindings:
            binding.validate_invariant()
            if binding.dependency_label in seen_invariants:
                raise CarverBlocked("S27 v2 validation invariant dependency bindings must be unique")
            seen_invariants.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)

    def _require_matching_dependency_hashes(
        self,
        binding: ValidationDependencyBindingContract,
        dependency_hash_by_label: dict[str, str],
    ) -> None:
        require_matching_dependency_hashes(
            "S27 v2 validation",
            binding.required_dependency_labels,
            binding.required_dependency_contract_hashes,
            dependency_hash_by_label,
        )

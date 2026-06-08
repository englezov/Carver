from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .construction_contract import ParserFileReplayConstructionContract
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION, S27_V2_TRUSTED_REPLAY_BUNDLE_STATUS
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
from .validation_contract import ValidationContractBundle
from .validation_input_contract import ValidationInputContractBundle


S27_V2_TRUSTED_BUNDLE_CONTRACT_ONLY_STATUS = "S27_V2_TRUSTED_BUNDLE_CONTRACT_ONLY"
PLANNED_TRUSTED_BUNDLE_INPUT_STATUS = "PLANNED_TRUSTED_BUNDLE_INPUT_ONLY"

TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE = "NOT_APPLICABLE"

TRUSTED_BUNDLE_INPUT_SOURCE_KINDS = (
    "BUNDLE_STATUS",
    "TRUST_ROOT_OUTPUT",
    "EVIDENCE_MANIFEST_OUTPUT",
    "CONSTRUCTION_CONTRACT_OUTPUT",
    "VALIDATION_INPUT_CONTRACT_OUTPUT",
    "VALIDATION_CONTRACT_OUTPUT",
    "VALIDATION_LEDGER_OUTPUT",
    "PROVENANCE_LEDGER_OUTPUT",
    "LOCAL_AUDIT_OUTPUT",
    "POLICY_INPUT",
)

REQUIRED_TRUSTED_BUNDLE_INPUTS = (
    "BUNDLE_STATUS_INPUT",
    "BUNDLE_TRUST_ROOT_HASH_INPUT",
    "BUNDLE_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT",
    "BUNDLE_CONSTRUCTION_CONTRACT_HASH_INPUT",
    "BUNDLE_VALIDATION_INPUT_CONTRACT_HASH_INPUT",
    "BUNDLE_VALIDATION_CONTRACT_BUNDLE_HASH_INPUT",
    "BUNDLE_VALIDATION_LEDGER_HASH_INPUT",
    "BUNDLE_PROVENANCE_LEDGER_HASH_INPUT",
    "BUNDLE_LOCAL_HOSTILE_AUDIT_RESULT_HASH_INPUT",
    "BUNDLE_FINAL_ASSEMBLY_POLICY_INPUT",
    "BUNDLE_PUBLIC_BOUNDARY_POLICY_INPUT",
    "BUNDLE_NON_AUTHORIZATION_POLICY_INPUT",
    "BUNDLE_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT",
)

REQUIRED_SOURCE_KIND_BY_TRUSTED_BUNDLE_INPUT = {
    "BUNDLE_STATUS_INPUT": "BUNDLE_STATUS",
    "BUNDLE_TRUST_ROOT_HASH_INPUT": "TRUST_ROOT_OUTPUT",
    "BUNDLE_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": "EVIDENCE_MANIFEST_OUTPUT",
    "BUNDLE_CONSTRUCTION_CONTRACT_HASH_INPUT": "CONSTRUCTION_CONTRACT_OUTPUT",
    "BUNDLE_VALIDATION_INPUT_CONTRACT_HASH_INPUT": "VALIDATION_INPUT_CONTRACT_OUTPUT",
    "BUNDLE_VALIDATION_CONTRACT_BUNDLE_HASH_INPUT": "VALIDATION_CONTRACT_OUTPUT",
    "BUNDLE_VALIDATION_LEDGER_HASH_INPUT": "VALIDATION_LEDGER_OUTPUT",
    "BUNDLE_PROVENANCE_LEDGER_HASH_INPUT": "PROVENANCE_LEDGER_OUTPUT",
    "BUNDLE_LOCAL_HOSTILE_AUDIT_RESULT_HASH_INPUT": "LOCAL_AUDIT_OUTPUT",
    "BUNDLE_FINAL_ASSEMBLY_POLICY_INPUT": "POLICY_INPUT",
    "BUNDLE_PUBLIC_BOUNDARY_POLICY_INPUT": "POLICY_INPUT",
    "BUNDLE_NON_AUTHORIZATION_POLICY_INPUT": "POLICY_INPUT",
    "BUNDLE_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT": "POLICY_INPUT",
}

REQUIRED_BUNDLE_STATUS_BY_INPUT = {
    "BUNDLE_STATUS_INPUT": S27_V2_TRUSTED_REPLAY_BUNDLE_STATUS,
}

REQUIRED_TRUST_ROOT_OUTPUT_BY_BUNDLE_INPUT = {
    "BUNDLE_TRUST_ROOT_HASH_INPUT": "REPLAY_TRUST_ROOT_HASH",
}

REQUIRED_EVIDENCE_MANIFEST_OUTPUT_BY_BUNDLE_INPUT = {
    "BUNDLE_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": "ACTIVE_EVIDENCE_MANIFEST_HASH",
}

REQUIRED_CONSTRUCTION_CONTRACT_OUTPUT_BY_BUNDLE_INPUT = {
    "BUNDLE_CONSTRUCTION_CONTRACT_HASH_INPUT": "CONSTRUCTION_CONTRACT_HASH",
}

REQUIRED_VALIDATION_INPUT_CONTRACT_OUTPUT_BY_BUNDLE_INPUT = {
    "BUNDLE_VALIDATION_INPUT_CONTRACT_HASH_INPUT": "VALIDATION_INPUT_CONTRACT_HASH",
}

REQUIRED_VALIDATION_CONTRACT_OUTPUT_BY_BUNDLE_INPUT = {
    "BUNDLE_VALIDATION_CONTRACT_BUNDLE_HASH_INPUT": "VALIDATION_CONTRACT_BUNDLE_HASH",
}

REQUIRED_VALIDATION_LEDGER_OUTPUT_BY_BUNDLE_INPUT = {
    "BUNDLE_VALIDATION_LEDGER_HASH_INPUT": "VALIDATION_LEDGER_HASH",
}

REQUIRED_PROVENANCE_LEDGER_OUTPUT_BY_BUNDLE_INPUT = {
    "BUNDLE_PROVENANCE_LEDGER_HASH_INPUT": "PROVENANCE_AND_HASH_LEDGER_HASH",
}

REQUIRED_LOCAL_AUDIT_OUTPUT_BY_BUNDLE_INPUT = {
    "BUNDLE_LOCAL_HOSTILE_AUDIT_RESULT_HASH_INPUT": "LOCAL_HOSTILE_AUDIT_RESULT_HASH",
}

REQUIRED_POLICY_LABEL_BY_BUNDLE_INPUT = {
    "BUNDLE_FINAL_ASSEMBLY_POLICY_INPUT": "FINAL_TRUSTED_REPLAY_BUNDLE_ASSEMBLY_POLICY",
    "BUNDLE_PUBLIC_BOUNDARY_POLICY_INPUT": "PUBLIC_BOUNDARY_TRUSTED_BUNDLE_ONLY_POLICY",
    "BUNDLE_NON_AUTHORIZATION_POLICY_INPUT": "S27_V2_REPLAY_NON_AUTHORIZATION_PRESERVATION_POLICY",
    "BUNDLE_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT": "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM_FROM_SCAFFOLD_POLICY",
}

REQUIRED_TRUSTED_BUNDLE_COMPONENTS = (
    "PUBLIC_BOUNDARY_STATUS",
    "TRUST_ROOT_AND_EVIDENCE_MANIFEST_REFERENCE",
    "CONSTRUCTION_AND_VALIDATION_CONTRACT_REFERENCE",
    "VALIDATION_PROVENANCE_AUDIT_LEDGER_REFERENCE",
    "NON_AUTHORIZATION_REFERENCE",
    "FINAL_BUNDLE_ASSEMBLY_REFERENCE",
)

REQUIRED_TRUSTED_BUNDLE_INVARIANTS = (
    "TRUST_ROOT_HASH_BINDING",
    "ACTIVE_EVIDENCE_MANIFEST_HASH_BINDING",
    "CONSTRUCTION_CONTRACT_HASH_BINDING",
    "VALIDATION_INPUT_CONTRACT_HASH_BINDING",
    "VALIDATION_CONTRACT_BUNDLE_HASH_BINDING",
    "VALIDATION_LEDGER_HASH_BINDING",
    "PROVENANCE_LEDGER_HASH_BINDING",
    "LOCAL_HOSTILE_AUDIT_RESULT_HASH_BINDING",
    "PUBLIC_BOUNDARY_EXPORT_POLICY_BINDING",
    "NON_AUTHORIZATION_PRESERVATION",
    "NO_BUNDLE_ASSEMBLY_EXECUTION_IN_CONTRACT",
    "NO_SOURCE_FAITHFUL_CLAIM_FROM_SCAFFOLD",
)

REQUIRED_BUNDLE_DEPENDENCIES_BY_COMPONENT = {
    "PUBLIC_BOUNDARY_STATUS": (
        "BUNDLE_STATUS_INPUT",
        "BUNDLE_PUBLIC_BOUNDARY_POLICY_INPUT",
    ),
    "TRUST_ROOT_AND_EVIDENCE_MANIFEST_REFERENCE": (
        "BUNDLE_TRUST_ROOT_HASH_INPUT",
        "BUNDLE_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT",
    ),
    "CONSTRUCTION_AND_VALIDATION_CONTRACT_REFERENCE": (
        "BUNDLE_CONSTRUCTION_CONTRACT_HASH_INPUT",
        "BUNDLE_VALIDATION_INPUT_CONTRACT_HASH_INPUT",
        "BUNDLE_VALIDATION_CONTRACT_BUNDLE_HASH_INPUT",
    ),
    "VALIDATION_PROVENANCE_AUDIT_LEDGER_REFERENCE": (
        "BUNDLE_VALIDATION_LEDGER_HASH_INPUT",
        "BUNDLE_PROVENANCE_LEDGER_HASH_INPUT",
        "BUNDLE_LOCAL_HOSTILE_AUDIT_RESULT_HASH_INPUT",
    ),
    "NON_AUTHORIZATION_REFERENCE": (
        "BUNDLE_NON_AUTHORIZATION_POLICY_INPUT",
        "BUNDLE_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT",
    ),
    "FINAL_BUNDLE_ASSEMBLY_REFERENCE": (
        "PUBLIC_BOUNDARY_STATUS",
        "TRUST_ROOT_AND_EVIDENCE_MANIFEST_REFERENCE",
        "CONSTRUCTION_AND_VALIDATION_CONTRACT_REFERENCE",
        "VALIDATION_PROVENANCE_AUDIT_LEDGER_REFERENCE",
        "NON_AUTHORIZATION_REFERENCE",
        "BUNDLE_FINAL_ASSEMBLY_POLICY_INPUT",
    ),
}

REQUIRED_BUNDLE_DEPENDENCIES_BY_INVARIANT = {
    "TRUST_ROOT_HASH_BINDING": (
        "BUNDLE_TRUST_ROOT_HASH_INPUT",
        "TRUST_ROOT_AND_EVIDENCE_MANIFEST_REFERENCE",
    ),
    "ACTIVE_EVIDENCE_MANIFEST_HASH_BINDING": (
        "BUNDLE_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT",
        "TRUST_ROOT_AND_EVIDENCE_MANIFEST_REFERENCE",
    ),
    "CONSTRUCTION_CONTRACT_HASH_BINDING": (
        "BUNDLE_CONSTRUCTION_CONTRACT_HASH_INPUT",
        "CONSTRUCTION_AND_VALIDATION_CONTRACT_REFERENCE",
    ),
    "VALIDATION_INPUT_CONTRACT_HASH_BINDING": (
        "BUNDLE_VALIDATION_INPUT_CONTRACT_HASH_INPUT",
        "CONSTRUCTION_AND_VALIDATION_CONTRACT_REFERENCE",
    ),
    "VALIDATION_CONTRACT_BUNDLE_HASH_BINDING": (
        "BUNDLE_VALIDATION_CONTRACT_BUNDLE_HASH_INPUT",
        "CONSTRUCTION_AND_VALIDATION_CONTRACT_REFERENCE",
    ),
    "VALIDATION_LEDGER_HASH_BINDING": (
        "BUNDLE_VALIDATION_LEDGER_HASH_INPUT",
        "VALIDATION_PROVENANCE_AUDIT_LEDGER_REFERENCE",
    ),
    "PROVENANCE_LEDGER_HASH_BINDING": (
        "BUNDLE_PROVENANCE_LEDGER_HASH_INPUT",
        "VALIDATION_PROVENANCE_AUDIT_LEDGER_REFERENCE",
    ),
    "LOCAL_HOSTILE_AUDIT_RESULT_HASH_BINDING": (
        "BUNDLE_LOCAL_HOSTILE_AUDIT_RESULT_HASH_INPUT",
        "VALIDATION_PROVENANCE_AUDIT_LEDGER_REFERENCE",
    ),
    "PUBLIC_BOUNDARY_EXPORT_POLICY_BINDING": (
        "PUBLIC_BOUNDARY_STATUS",
        "BUNDLE_PUBLIC_BOUNDARY_POLICY_INPUT",
    ),
    "NON_AUTHORIZATION_PRESERVATION": (
        "NON_AUTHORIZATION_REFERENCE",
    ),
    "NO_BUNDLE_ASSEMBLY_EXECUTION_IN_CONTRACT": (
        "BUNDLE_FINAL_ASSEMBLY_POLICY_INPUT",
        "FINAL_BUNDLE_ASSEMBLY_REFERENCE",
    ),
    "NO_SOURCE_FAITHFUL_CLAIM_FROM_SCAFFOLD": (
        "BUNDLE_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT",
        "FINAL_BUNDLE_ASSEMBLY_REFERENCE",
    ),
}


@dataclass(frozen=True)
class TrustedBundleInputFieldContract:
    input_label: str
    input_status: str
    source_kind: str
    bundle_status_label: str
    trust_root_output_label: str
    evidence_manifest_output_label: str
    construction_contract_output_label: str
    validation_input_contract_output_label: str
    validation_contract_output_label: str
    validation_ledger_output_label: str
    provenance_ledger_output_label: str
    local_audit_output_label: str
    source_policy_label: str
    source_contract_hash: str
    trusted_bundle_input_policy_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 trusted bundle input label", self.input_label)
        if self.input_label not in REQUIRED_TRUSTED_BUNDLE_INPUTS:
            raise CarverBlocked("S27 v2 trusted bundle input label is not locked")
        require_text("S27 v2 trusted bundle input status", self.input_status)
        if self.input_status != PLANNED_TRUSTED_BUNDLE_INPUT_STATUS:
            raise CarverBlocked("S27 v2 trusted bundle input must remain planned-only")
        require_text("S27 v2 trusted bundle input source kind", self.source_kind)
        if self.source_kind not in TRUSTED_BUNDLE_INPUT_SOURCE_KINDS:
            raise CarverBlocked("S27 v2 trusted bundle input source kind is not locked")
        if self.source_kind != REQUIRED_SOURCE_KIND_BY_TRUSTED_BUNDLE_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked source kind")
        self._validate_source_target()
        require_hash("S27 v2 trusted bundle input source contract hash", self.source_contract_hash)
        require_hash("S27 v2 trusted bundle input policy hash", self.trusted_bundle_input_policy_hash)
        require_hash("S27 v2 trusted bundle input field contract hash", self.input_field_contract_hash)

    def _validate_source_target(self) -> None:
        if self.source_kind == "BUNDLE_STATUS":
            self._validate_bundle_status_target()
        elif self.source_kind == "TRUST_ROOT_OUTPUT":
            self._validate_trust_root_output_target()
        elif self.source_kind == "EVIDENCE_MANIFEST_OUTPUT":
            self._validate_evidence_manifest_output_target()
        elif self.source_kind == "CONSTRUCTION_CONTRACT_OUTPUT":
            self._validate_construction_contract_output_target()
        elif self.source_kind == "VALIDATION_INPUT_CONTRACT_OUTPUT":
            self._validate_validation_input_contract_output_target()
        elif self.source_kind == "VALIDATION_CONTRACT_OUTPUT":
            self._validate_validation_contract_output_target()
        elif self.source_kind == "VALIDATION_LEDGER_OUTPUT":
            self._validate_validation_ledger_output_target()
        elif self.source_kind == "PROVENANCE_LEDGER_OUTPUT":
            self._validate_provenance_ledger_output_target()
        elif self.source_kind == "LOCAL_AUDIT_OUTPUT":
            self._validate_local_audit_output_target()
        elif self.source_kind == "POLICY_INPUT":
            self._validate_policy_input_target()

    def _require_not_applicable(self, name: str, value: str) -> None:
        require_text(name, value)
        if value != TRUSTED_BUNDLE_INPUT_NOT_APPLICABLE:
            raise CarverBlocked(f"{name} must be not applicable")

    def _require_common_targets_not_applicable(self, exempt_name: str) -> None:
        targets = (
            ("S27 v2 trusted bundle status label", self.bundle_status_label),
            ("S27 v2 trusted bundle trust-root output label", self.trust_root_output_label),
            (
                "S27 v2 trusted bundle evidence-manifest output label",
                self.evidence_manifest_output_label,
            ),
            (
                "S27 v2 trusted bundle construction contract output label",
                self.construction_contract_output_label,
            ),
            (
                "S27 v2 trusted bundle validation input contract output label",
                self.validation_input_contract_output_label,
            ),
            (
                "S27 v2 trusted bundle validation contract output label",
                self.validation_contract_output_label,
            ),
            ("S27 v2 trusted bundle validation ledger output label", self.validation_ledger_output_label),
            ("S27 v2 trusted bundle provenance ledger output label", self.provenance_ledger_output_label),
            ("S27 v2 trusted bundle local audit output label", self.local_audit_output_label),
            ("S27 v2 trusted bundle source policy label", self.source_policy_label),
        )
        for name, value in targets:
            if name != exempt_name:
                self._require_not_applicable(name, value)

    def _validate_bundle_status_target(self) -> None:
        require_text("S27 v2 trusted bundle status label", self.bundle_status_label)
        if self.bundle_status_label != REQUIRED_BUNDLE_STATUS_BY_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked bundle status")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle status label")

    def _validate_trust_root_output_target(self) -> None:
        require_text("S27 v2 trusted bundle trust-root output label", self.trust_root_output_label)
        if self.trust_root_output_label != REQUIRED_TRUST_ROOT_OUTPUT_BY_BUNDLE_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked trust-root output")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle trust-root output label")

    def _validate_evidence_manifest_output_target(self) -> None:
        require_text(
            "S27 v2 trusted bundle evidence-manifest output label",
            self.evidence_manifest_output_label,
        )
        if self.evidence_manifest_output_label != REQUIRED_EVIDENCE_MANIFEST_OUTPUT_BY_BUNDLE_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked evidence-manifest output")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle evidence-manifest output label")

    def _validate_construction_contract_output_target(self) -> None:
        require_text(
            "S27 v2 trusted bundle construction contract output label",
            self.construction_contract_output_label,
        )
        if (
            self.construction_contract_output_label
            != REQUIRED_CONSTRUCTION_CONTRACT_OUTPUT_BY_BUNDLE_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked construction contract output")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle construction contract output label")

    def _validate_validation_input_contract_output_target(self) -> None:
        require_text(
            "S27 v2 trusted bundle validation input contract output label",
            self.validation_input_contract_output_label,
        )
        if (
            self.validation_input_contract_output_label
            != REQUIRED_VALIDATION_INPUT_CONTRACT_OUTPUT_BY_BUNDLE_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked validation input contract output")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle validation input contract output label")

    def _validate_validation_contract_output_target(self) -> None:
        require_text(
            "S27 v2 trusted bundle validation contract output label",
            self.validation_contract_output_label,
        )
        if self.validation_contract_output_label != REQUIRED_VALIDATION_CONTRACT_OUTPUT_BY_BUNDLE_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked validation contract output")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle validation contract output label")

    def _validate_validation_ledger_output_target(self) -> None:
        require_text("S27 v2 trusted bundle validation ledger output label", self.validation_ledger_output_label)
        if self.validation_ledger_output_label != REQUIRED_VALIDATION_LEDGER_OUTPUT_BY_BUNDLE_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked validation ledger output")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle validation ledger output label")

    def _validate_provenance_ledger_output_target(self) -> None:
        require_text("S27 v2 trusted bundle provenance ledger output label", self.provenance_ledger_output_label)
        if self.provenance_ledger_output_label != REQUIRED_PROVENANCE_LEDGER_OUTPUT_BY_BUNDLE_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked provenance ledger output")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle provenance ledger output label")

    def _validate_local_audit_output_target(self) -> None:
        require_text("S27 v2 trusted bundle local audit output label", self.local_audit_output_label)
        if self.local_audit_output_label != REQUIRED_LOCAL_AUDIT_OUTPUT_BY_BUNDLE_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked local audit output")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle local audit output label")

    def _validate_policy_input_target(self) -> None:
        require_text("S27 v2 trusted bundle source policy label", self.source_policy_label)
        if self.source_policy_label != REQUIRED_POLICY_LABEL_BY_BUNDLE_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 trusted bundle input must use the locked source policy")
        self._require_common_targets_not_applicable("S27 v2 trusted bundle source policy label")


@dataclass(frozen=True)
class TrustedBundleDependencyBindingContract:
    dependency_label: str
    required_dependency_labels: tuple[str, ...]
    required_dependency_contract_hashes: tuple[str, ...]
    dependency_binding_policy_hash: str
    dependency_binding_contract_hash: str

    def validate_component(self) -> None:
        require_text("S27 v2 trusted bundle component dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_TRUSTED_BUNDLE_COMPONENTS:
            raise CarverBlocked("S27 v2 trusted bundle component dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_BUNDLE_DEPENDENCIES_BY_COMPONENT[self.dependency_label])

    def validate_invariant(self) -> None:
        require_text("S27 v2 trusted bundle invariant dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_TRUSTED_BUNDLE_INVARIANTS:
            raise CarverBlocked("S27 v2 trusted bundle invariant dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_BUNDLE_DEPENDENCIES_BY_INVARIANT[self.dependency_label])

    def _validate_required_dependencies(self, locked_labels: tuple[str, ...]) -> None:
        require_non_empty_tuple("S27 v2 trusted bundle required dependency labels", self.required_dependency_labels)
        if self.required_dependency_labels != locked_labels:
            raise CarverBlocked("S27 v2 trusted bundle dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 trusted bundle required dependency contract hashes",
            self.required_dependency_contract_hashes,
        )
        if len(self.required_dependency_contract_hashes) != len(self.required_dependency_labels):
            raise CarverBlocked("S27 v2 trusted bundle dependency hashes must match labels")
        for dependency_hash in self.required_dependency_contract_hashes:
            require_hash("S27 v2 trusted bundle dependency contract hash", dependency_hash)
        require_hash("S27 v2 trusted bundle dependency binding policy hash", self.dependency_binding_policy_hash)
        require_hash("S27 v2 trusted bundle dependency binding contract hash", self.dependency_binding_contract_hash)


@dataclass(frozen=True)
class TrustedBundleContractBundle:
    status: str
    replay_trust_root_hash: str
    active_evidence_manifest_hash: str
    construction_contract_hash: str
    validation_input_contract_hash: str
    validation_contract_bundle_hash: str
    validation_ledger_hash: str
    provenance_ledger_hash: str
    local_hostile_audit_result_hash: str
    trusted_bundle_policy_hash: str
    input_field_contracts: tuple[TrustedBundleInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    component_dependency_bindings: tuple[TrustedBundleDependencyBindingContract, ...]
    invariant_dependency_bindings: tuple[TrustedBundleDependencyBindingContract, ...]
    trusted_bundle_input_set_hash: str
    trusted_bundle_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 trusted bundle requires routed validation and trust authority"
        )

    def validate_against_validation_authority(
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
        construction_contract: ParserFileReplayConstructionContract,
        validation_input_contract: ValidationInputContractBundle,
        validation_contract: ValidationContractBundle,
    ) -> None:
        construction_contract.validate()
        validation_input_contract.validate_against_pnl_authority(
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
            pnl_input_contract,
            pnl_contract,
        )
        validation_contract.validate()
        require_text("S27 v2 trusted bundle contract status", self.status)
        if self.status != S27_V2_TRUSTED_BUNDLE_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 trusted bundle contract must remain contract-only")
        self._validate_locked_maps()
        require_hash("S27 v2 trusted bundle replay trust-root hash", self.replay_trust_root_hash)
        require_hash(
            "S27 v2 trusted bundle active evidence-manifest hash",
            self.active_evidence_manifest_hash,
        )
        require_hash("S27 v2 trusted bundle construction contract hash", self.construction_contract_hash)
        require_hash("S27 v2 trusted bundle validation input contract hash", self.validation_input_contract_hash)
        require_hash("S27 v2 trusted bundle validation contract bundle hash", self.validation_contract_bundle_hash)
        require_hash("S27 v2 trusted bundle validation ledger hash", self.validation_ledger_hash)
        require_hash("S27 v2 trusted bundle provenance ledger hash", self.provenance_ledger_hash)
        require_hash(
            "S27 v2 trusted bundle local hostile audit result hash",
            self.local_hostile_audit_result_hash,
        )
        require_hash("S27 v2 trusted bundle policy hash", self.trusted_bundle_policy_hash)
        require_hash_map(
            "S27 v2 trusted bundle expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_TRUSTED_BUNDLE_INPUTS,
        )
        self._validate_validation_authority(
            replay_trust_root,
            evidence_manifest,
            construction_contract,
            validation_input_contract,
            validation_contract,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 trusted bundle expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(
                replay_trust_root,
                evidence_manifest,
                construction_contract,
                validation_input_contract,
                validation_contract,
            ),
            REQUIRED_TRUSTED_BUNDLE_INPUTS,
        )
        dependency_hash_by_label = self._validate_input_fields()
        self._validate_component_dependencies(dependency_hash_by_label)
        self._validate_invariant_dependencies(dependency_hash_by_label)
        require_hash("S27 v2 trusted bundle input set hash", self.trusted_bundle_input_set_hash)
        require_hash("S27 v2 trusted bundle contract hash", self.trusted_bundle_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 trusted bundle contract must preserve non-authorizations")

    def _validate_locked_maps(self) -> None:
        if tuple(REQUIRED_SOURCE_KIND_BY_TRUSTED_BUNDLE_INPUT) != REQUIRED_TRUSTED_BUNDLE_INPUTS:
            raise CarverBlocked("S27 v2 trusted bundle input source-kind map must cover locked inputs")
        if tuple(REQUIRED_BUNDLE_DEPENDENCIES_BY_COMPONENT) != REQUIRED_TRUSTED_BUNDLE_COMPONENTS:
            raise CarverBlocked("S27 v2 trusted bundle component dependency map must cover locked components")
        if tuple(REQUIRED_BUNDLE_DEPENDENCIES_BY_INVARIANT) != REQUIRED_TRUSTED_BUNDLE_INVARIANTS:
            raise CarverBlocked("S27 v2 trusted bundle invariant dependency map must cover locked invariants")

    def _active_source_contract_hash_by_input_label(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        construction_contract: ParserFileReplayConstructionContract,
        validation_input_contract: ValidationInputContractBundle,
        validation_contract: ValidationContractBundle,
    ) -> dict[str, str]:
        active_hash_by_label: dict[str, str] = {}
        for input_label in REQUIRED_TRUSTED_BUNDLE_INPUTS:
            source_kind = REQUIRED_SOURCE_KIND_BY_TRUSTED_BUNDLE_INPUT[input_label]
            if source_kind == "BUNDLE_STATUS":
                active_hash_by_label[input_label] = self.trusted_bundle_policy_hash
            elif source_kind == "TRUST_ROOT_OUTPUT":
                active_hash_by_label[input_label] = replay_trust_root.replay_trust_root_hash
            elif source_kind == "EVIDENCE_MANIFEST_OUTPUT":
                active_hash_by_label[input_label] = evidence_manifest.active_evidence_manifest_hash
            elif source_kind == "CONSTRUCTION_CONTRACT_OUTPUT":
                active_hash_by_label[input_label] = construction_contract.construction_contract_hash
            elif source_kind == "VALIDATION_INPUT_CONTRACT_OUTPUT":
                active_hash_by_label[input_label] = validation_input_contract.validation_input_contract_hash
            elif source_kind == "VALIDATION_CONTRACT_OUTPUT":
                active_hash_by_label[input_label] = validation_contract.validation_contract_bundle_hash
            elif source_kind == "VALIDATION_LEDGER_OUTPUT":
                active_hash_by_label[input_label] = self.validation_ledger_hash
            elif source_kind == "PROVENANCE_LEDGER_OUTPUT":
                active_hash_by_label[input_label] = self.provenance_ledger_hash
            elif source_kind == "LOCAL_AUDIT_OUTPUT":
                active_hash_by_label[input_label] = self.local_hostile_audit_result_hash
            elif source_kind == "POLICY_INPUT":
                active_hash_by_label[input_label] = self.trusted_bundle_policy_hash
            else:
                raise CarverBlocked("S27 v2 trusted bundle input source kind cannot be authority-bound")
        return active_hash_by_label

    def _validate_validation_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        construction_contract: ParserFileReplayConstructionContract,
        validation_input_contract: ValidationInputContractBundle,
        validation_contract: ValidationContractBundle,
    ) -> None:
        active_source_hash_by_input_label = self._active_source_contract_hash_by_input_label(
            replay_trust_root,
            evidence_manifest,
            construction_contract,
            validation_input_contract,
            validation_contract,
        )
        observed_source_hash_by_input_label = {
            "BUNDLE_STATUS_INPUT": self.trusted_bundle_policy_hash,
            "BUNDLE_TRUST_ROOT_HASH_INPUT": self.replay_trust_root_hash,
            "BUNDLE_ACTIVE_EVIDENCE_MANIFEST_HASH_INPUT": self.active_evidence_manifest_hash,
            "BUNDLE_CONSTRUCTION_CONTRACT_HASH_INPUT": self.construction_contract_hash,
            "BUNDLE_VALIDATION_INPUT_CONTRACT_HASH_INPUT": self.validation_input_contract_hash,
            "BUNDLE_VALIDATION_CONTRACT_BUNDLE_HASH_INPUT": self.validation_contract_bundle_hash,
            "BUNDLE_VALIDATION_LEDGER_HASH_INPUT": self.validation_ledger_hash,
            "BUNDLE_PROVENANCE_LEDGER_HASH_INPUT": self.provenance_ledger_hash,
            "BUNDLE_LOCAL_HOSTILE_AUDIT_RESULT_HASH_INPUT": self.local_hostile_audit_result_hash,
            "BUNDLE_FINAL_ASSEMBLY_POLICY_INPUT": self.trusted_bundle_policy_hash,
            "BUNDLE_PUBLIC_BOUNDARY_POLICY_INPUT": self.trusted_bundle_policy_hash,
            "BUNDLE_NON_AUTHORIZATION_POLICY_INPUT": self.trusted_bundle_policy_hash,
            "BUNDLE_NO_SOURCE_FAITHFUL_CLAIM_POLICY_INPUT": self.trusted_bundle_policy_hash,
        }
        require_hash_map_matches_active_authority(
            "S27 v2 trusted bundle routed authority",
            observed_source_hash_by_input_label,
            active_source_hash_by_input_label,
            REQUIRED_TRUSTED_BUNDLE_INPUTS,
        )
        if validation_input_contract.replay_trust_root_hash != replay_trust_root.replay_trust_root_hash:
            raise CarverBlocked("S27 v2 trusted bundle must bind validation input replay trust root")
        if validation_input_contract.active_evidence_manifest_hash != evidence_manifest.active_evidence_manifest_hash:
            raise CarverBlocked("S27 v2 trusted bundle must bind validation input evidence manifest")
        if validation_contract.source_binding.replay_trust_root_hash != replay_trust_root.replay_trust_root_hash:
            raise CarverBlocked("S27 v2 trusted bundle must bind validation contract replay trust root")
        if validation_contract.source_binding.active_evidence_manifest_hash != evidence_manifest.active_evidence_manifest_hash:
            raise CarverBlocked("S27 v2 trusted bundle must bind validation contract evidence manifest")
        if (
            validation_contract.source_binding.source_input_manifest_hash
            != validation_input_contract.source_input_manifest_hash
        ):
            raise CarverBlocked("S27 v2 trusted bundle must bind validation contract source manifest")
        if validation_contract.source_binding.pnl_contract_bundle_hash != validation_input_contract.pnl_contract_bundle_hash:
            raise CarverBlocked("S27 v2 trusted bundle must bind validation contract PnL bundle")
        if validation_contract.source_binding.validation_ledger_schema_hash != validation_input_contract.validation_ledger_schema_hash:
            raise CarverBlocked("S27 v2 trusted bundle must bind validation ledger schema")
        if (
            validation_contract.source_binding.provenance_and_hash_ledger_schema_hash
            != validation_input_contract.provenance_ledger_schema_hash
        ):
            raise CarverBlocked("S27 v2 trusted bundle must bind provenance ledger schema")
        if (
            validation_contract.source_binding.local_hostile_audit_result_schema_hash
            != validation_input_contract.local_hostile_audit_schema_hash
        ):
            raise CarverBlocked("S27 v2 trusted bundle must bind local hostile audit schema")

    def _validate_input_fields(self) -> dict[str, str]:
        require_non_empty_tuple("S27 v2 trusted bundle input field contracts", self.input_field_contracts)
        seen_inputs: set[str] = set()
        dependency_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 trusted bundle input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 trusted bundle input source contract hash",
                contract.input_label,
                contract.source_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            dependency_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_TRUSTED_BUNDLE_INPUTS:
            raise CarverBlocked("S27 v2 trusted bundle inputs must match locked input tuple")
        return dependency_hash_by_label

    def _validate_component_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 trusted bundle component dependency bindings",
            self.component_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.component_dependency_bindings)
            != REQUIRED_TRUSTED_BUNDLE_COMPONENTS
        ):
            raise CarverBlocked("S27 v2 trusted bundle component dependencies must match locked components")
        seen_components: set[str] = set()
        for binding in self.component_dependency_bindings:
            binding.validate_component()
            if binding.dependency_label in seen_components:
                raise CarverBlocked("S27 v2 trusted bundle component dependency bindings must be unique")
            seen_components.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_invariant_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 trusted bundle invariant dependency bindings",
            self.invariant_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.invariant_dependency_bindings)
            != REQUIRED_TRUSTED_BUNDLE_INVARIANTS
        ):
            raise CarverBlocked("S27 v2 trusted bundle invariant dependencies must match locked invariants")
        seen_invariants: set[str] = set()
        for binding in self.invariant_dependency_bindings:
            binding.validate_invariant()
            if binding.dependency_label in seen_invariants:
                raise CarverBlocked("S27 v2 trusted bundle invariant dependency bindings must be unique")
            seen_invariants.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)

    def _require_matching_dependency_hashes(
        self,
        binding: TrustedBundleDependencyBindingContract,
        dependency_hash_by_label: dict[str, str],
    ) -> None:
        require_matching_dependency_hashes(
            "S27 v2 trusted bundle",
            binding.required_dependency_labels,
            binding.required_dependency_contract_hashes,
            dependency_hash_by_label,
        )

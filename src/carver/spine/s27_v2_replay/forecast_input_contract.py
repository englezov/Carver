from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest
from .forecast_contract import (
    REQUIRED_FORECAST_COMPONENT_FAMILIES,
    REQUIRED_FORECAST_DECISION_BRANCHES,
    REQUIRED_FORECAST_INVARIANTS,
)
from .level_compatibility_contract import LevelCompatibilityContractBundle
from .level_compatibility_input_contract import LevelCompatibilityInputContractBundle
from .parser_output_contract import ParserOutputBatchSetContract
from .runtime_history_contract import (
    REQUIRED_RUNTIME_STATE_FAMILIES,
    REQUIRED_VQM_COMPONENTS,
    RuntimeHistoryContractBundle,
)
from .runtime_history_input_contract import (
    REQUIRED_RUNTIME_HISTORY_INPUTS,
    RuntimeHistoryInputContractBundle,
)
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


S27_V2_FORECAST_INPUT_CONTRACT_ONLY_STATUS = "S27_V2_FORECAST_INPUT_CONTRACT_ONLY"
PLANNED_FORECAST_INPUT_STATUS = "PLANNED_FORECAST_INPUT_ONLY"

FORECAST_INPUT_NOT_APPLICABLE = "NOT_APPLICABLE"

FORECAST_INPUT_SOURCE_KINDS = (
    "RUNTIME_INPUT",
    "RUNTIME_STATE",
    "VQM_COMPONENT",
    "POLICY_INPUT",
)

REQUIRED_FORECAST_INPUTS = (
    "FORECAST_HOURLY_DECISION_PRICE_INPUT",
    "FORECAST_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_INPUT",
    "FORECAST_EWMA5_EQUILIBRIUM_STATE_INPUT",
    "FORECAST_SIGMA_ESTIMATOR_STATE_INPUT",
    "FORECAST_EWMAC16_64_TREND_STATE_INPUT",
    "FORECAST_RELATIVE_VOLATILITY_V_INPUT",
    "FORECAST_EXPANDING_QUANTILE_Q_INPUT",
    "FORECAST_RAW_VOLATILITY_MULTIPLIER_INPUT",
    "FORECAST_EWMA10_MULTIPLIER_M_INPUT",
    "FORECAST_SCALAR_SOURCE_LOCK_INPUT",
    "FORECAST_CAP_POLICY_INPUT",
    "FORECAST_DESIRED_POSITION_REFERENCE_POLICY_INPUT",
)

REQUIRED_SOURCE_KIND_BY_FORECAST_INPUT = {
    "FORECAST_HOURLY_DECISION_PRICE_INPUT": "RUNTIME_INPUT",
    "FORECAST_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_INPUT": "RUNTIME_INPUT",
    "FORECAST_EWMA5_EQUILIBRIUM_STATE_INPUT": "RUNTIME_STATE",
    "FORECAST_SIGMA_ESTIMATOR_STATE_INPUT": "RUNTIME_STATE",
    "FORECAST_EWMAC16_64_TREND_STATE_INPUT": "RUNTIME_STATE",
    "FORECAST_RELATIVE_VOLATILITY_V_INPUT": "VQM_COMPONENT",
    "FORECAST_EXPANDING_QUANTILE_Q_INPUT": "VQM_COMPONENT",
    "FORECAST_RAW_VOLATILITY_MULTIPLIER_INPUT": "VQM_COMPONENT",
    "FORECAST_EWMA10_MULTIPLIER_M_INPUT": "VQM_COMPONENT",
    "FORECAST_SCALAR_SOURCE_LOCK_INPUT": "POLICY_INPUT",
    "FORECAST_CAP_POLICY_INPUT": "POLICY_INPUT",
    "FORECAST_DESIRED_POSITION_REFERENCE_POLICY_INPUT": "POLICY_INPUT",
}

REQUIRED_RUNTIME_HISTORY_INPUT_BY_FORECAST_INPUT = {
    "FORECAST_HOURLY_DECISION_PRICE_INPUT": "RUNTIME_HOURLY_DECISION_PRICE_INPUT",
    "FORECAST_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_INPUT": (
        "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT"
    ),
}

REQUIRED_RUNTIME_STATE_BY_FORECAST_INPUT = {
    "FORECAST_EWMA5_EQUILIBRIUM_STATE_INPUT": "EWMA5_EQUILIBRIUM_STATE",
    "FORECAST_SIGMA_ESTIMATOR_STATE_INPUT": "SIGMA_ESTIMATOR_STATE",
    "FORECAST_EWMAC16_64_TREND_STATE_INPUT": "EWMAC16_64_TREND_STATE",
}

REQUIRED_VQM_COMPONENT_BY_FORECAST_INPUT = {
    "FORECAST_RELATIVE_VOLATILITY_V_INPUT": "RELATIVE_VOLATILITY_V",
    "FORECAST_EXPANDING_QUANTILE_Q_INPUT": "EXPANDING_QUANTILE_Q",
    "FORECAST_RAW_VOLATILITY_MULTIPLIER_INPUT": "RAW_VOLATILITY_MULTIPLIER",
    "FORECAST_EWMA10_MULTIPLIER_M_INPUT": "EWMA10_MULTIPLIER_M",
}

REQUIRED_POLICY_LABEL_BY_FORECAST_INPUT = {
    "FORECAST_SCALAR_SOURCE_LOCK_INPUT": "S27_SCALAR_SOURCE_LOCK_POLICY",
    "FORECAST_CAP_POLICY_INPUT": "FORECAST_CAP_POLICY",
    "FORECAST_DESIRED_POSITION_REFERENCE_POLICY_INPUT": "DESIRED_POSITION_REFERENCE_POLICY",
}

REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT = {
    "RAW_MEAN_REVERSION_FORECAST": (
        "FORECAST_HOURLY_DECISION_PRICE_INPUT",
        "FORECAST_EWMA5_EQUILIBRIUM_STATE_INPUT",
    ),
    "SIGMA_PRICE_BRIDGE": (
        "FORECAST_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_INPUT",
        "FORECAST_SIGMA_ESTIMATOR_STATE_INPUT",
    ),
    "RISK_ADJUSTED_FORECAST_PRE_TREND_VETO": (
        "RAW_MEAN_REVERSION_FORECAST",
        "SIGMA_PRICE_BRIDGE",
    ),
    "EWMAC16_64_TREND_GATE": (
        "RISK_ADJUSTED_FORECAST_PRE_TREND_VETO",
        "FORECAST_EWMAC16_64_TREND_STATE_INPUT",
    ),
    "VQM_MULTIPLIER_APPLICATION": (
        "EWMAC16_64_TREND_GATE",
        "FORECAST_RELATIVE_VOLATILITY_V_INPUT",
        "FORECAST_EXPANDING_QUANTILE_Q_INPUT",
        "FORECAST_RAW_VOLATILITY_MULTIPLIER_INPUT",
        "FORECAST_EWMA10_MULTIPLIER_M_INPUT",
    ),
    "SCALAR_AND_CAP_APPLICATION": (
        "VQM_MULTIPLIER_APPLICATION",
        "FORECAST_SCALAR_SOURCE_LOCK_INPUT",
        "FORECAST_CAP_POLICY_INPUT",
    ),
    "DESIRED_POSITION_REFERENCE": (
        "SCALAR_AND_CAP_APPLICATION",
        "FORECAST_DESIRED_POSITION_REFERENCE_POLICY_INPUT",
    ),
}

REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH = {
    "PERMIT_MEAN_REVERSION": (
        "RISK_ADJUSTED_FORECAST_PRE_TREND_VETO",
        "EWMAC16_64_TREND_GATE",
    ),
    "ZERO_FORECAST_BY_TREND_VETO": (
        "RISK_ADJUSTED_FORECAST_PRE_TREND_VETO",
        "EWMAC16_64_TREND_GATE",
    ),
    "FLAT_AT_EQUILIBRIUM": ("RAW_MEAN_REVERSION_FORECAST",),
}

REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT = {
    "STRICT_PRIOR_RUNTIME_INPUTS": (
        "FORECAST_HOURLY_DECISION_PRICE_INPUT",
        "FORECAST_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_INPUT",
        "FORECAST_EWMA5_EQUILIBRIUM_STATE_INPUT",
        "FORECAST_SIGMA_ESTIMATOR_STATE_INPUT",
        "FORECAST_EWMAC16_64_TREND_STATE_INPUT",
    ),
    "COMPLETED_BAR_FORECAST_TIMESTAMP": (
        "FORECAST_HOURLY_DECISION_PRICE_INPUT",
        "FORECAST_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_INPUT",
    ),
    "POSITIVE_SIGMA_AND_PRICE_INPUTS": (
        "FORECAST_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_INPUT",
        "FORECAST_SIGMA_ESTIMATOR_STATE_INPUT",
        "SIGMA_PRICE_BRIDGE",
    ),
    "ZERO_EQUILIBRIUM_FLAT_BRANCH": (
        "RAW_MEAN_REVERSION_FORECAST",
        "FLAT_AT_EQUILIBRIUM",
    ),
    "TREND_VETO_SIGN_GATE": (
        "RISK_ADJUSTED_FORECAST_PRE_TREND_VETO",
        "EWMAC16_64_TREND_GATE",
        "PERMIT_MEAN_REVERSION",
        "ZERO_FORECAST_BY_TREND_VETO",
    ),
    "POST_VETO_VQM_MULTIPLIER_BINDING": (
        "EWMAC16_64_TREND_GATE",
        "VQM_MULTIPLIER_APPLICATION",
        "FORECAST_EWMA10_MULTIPLIER_M_INPUT",
    ),
    "SCALAR_CAP_BINDING": (
        "VQM_MULTIPLIER_APPLICATION",
        "SCALAR_AND_CAP_APPLICATION",
        "FORECAST_SCALAR_SOURCE_LOCK_INPUT",
        "FORECAST_CAP_POLICY_INPUT",
    ),
    "DESIRED_POSITION_REFERENCE_BINDING": (
        "SCALAR_AND_CAP_APPLICATION",
        "DESIRED_POSITION_REFERENCE",
        "FORECAST_DESIRED_POSITION_REFERENCE_POLICY_INPUT",
    ),
}


@dataclass(frozen=True)
class ForecastInputFieldContract:
    input_label: str
    input_status: str
    source_kind: str
    runtime_history_input_label: str
    runtime_state_family: str
    vqm_component_label: str
    source_policy_label: str
    source_contract_hash: str
    forecast_input_policy_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 forecast input label", self.input_label)
        if self.input_label not in REQUIRED_FORECAST_INPUTS:
            raise CarverBlocked("S27 v2 forecast input label is not locked")
        require_text("S27 v2 forecast input status", self.input_status)
        if self.input_status != PLANNED_FORECAST_INPUT_STATUS:
            raise CarverBlocked("S27 v2 forecast input must remain planned-only")
        require_text("S27 v2 forecast input source kind", self.source_kind)
        if self.source_kind not in FORECAST_INPUT_SOURCE_KINDS:
            raise CarverBlocked("S27 v2 forecast input source kind is not locked")
        if self.source_kind != REQUIRED_SOURCE_KIND_BY_FORECAST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 forecast input must use the locked source kind")
        self._validate_source_target()
        require_hash("S27 v2 forecast input source contract hash", self.source_contract_hash)
        require_hash("S27 v2 forecast input policy hash", self.forecast_input_policy_hash)
        require_hash("S27 v2 forecast input field contract hash", self.input_field_contract_hash)

    def _validate_source_target(self) -> None:
        if self.source_kind == "RUNTIME_INPUT":
            self._validate_runtime_input_target()
        elif self.source_kind == "RUNTIME_STATE":
            self._validate_runtime_state_target()
        elif self.source_kind == "VQM_COMPONENT":
            self._validate_vqm_component_target()
        elif self.source_kind == "POLICY_INPUT":
            self._validate_policy_input_target()

    def _require_not_applicable(self, name: str, value: str) -> None:
        require_text(name, value)
        if value != FORECAST_INPUT_NOT_APPLICABLE:
            raise CarverBlocked(f"{name} must be not applicable")

    def _validate_runtime_input_target(self) -> None:
        require_text("S27 v2 forecast runtime-history input label", self.runtime_history_input_label)
        if self.runtime_history_input_label not in REQUIRED_RUNTIME_HISTORY_INPUTS:
            raise CarverBlocked("S27 v2 forecast runtime-history input label is not locked")
        if (
            self.runtime_history_input_label
            != REQUIRED_RUNTIME_HISTORY_INPUT_BY_FORECAST_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 forecast input must use the locked runtime-history input")
        self._require_not_applicable("S27 v2 forecast runtime state family", self.runtime_state_family)
        self._require_not_applicable("S27 v2 forecast V/Q/M component", self.vqm_component_label)
        self._require_not_applicable("S27 v2 forecast source policy label", self.source_policy_label)

    def _validate_runtime_state_target(self) -> None:
        require_text("S27 v2 forecast runtime state family", self.runtime_state_family)
        if self.runtime_state_family not in REQUIRED_RUNTIME_STATE_FAMILIES:
            raise CarverBlocked("S27 v2 forecast runtime state family is not locked")
        if self.runtime_state_family != REQUIRED_RUNTIME_STATE_BY_FORECAST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 forecast input must use the locked runtime state")
        self._require_not_applicable(
            "S27 v2 forecast runtime-history input label",
            self.runtime_history_input_label,
        )
        self._require_not_applicable("S27 v2 forecast V/Q/M component", self.vqm_component_label)
        self._require_not_applicable("S27 v2 forecast source policy label", self.source_policy_label)

    def _validate_vqm_component_target(self) -> None:
        require_text("S27 v2 forecast V/Q/M component", self.vqm_component_label)
        if self.vqm_component_label not in REQUIRED_VQM_COMPONENTS:
            raise CarverBlocked("S27 v2 forecast V/Q/M component is not locked")
        if self.vqm_component_label != REQUIRED_VQM_COMPONENT_BY_FORECAST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 forecast input must use the locked V/Q/M component")
        self._require_not_applicable(
            "S27 v2 forecast runtime-history input label",
            self.runtime_history_input_label,
        )
        self._require_not_applicable("S27 v2 forecast runtime state family", self.runtime_state_family)
        self._require_not_applicable("S27 v2 forecast source policy label", self.source_policy_label)

    def _validate_policy_input_target(self) -> None:
        require_text("S27 v2 forecast source policy label", self.source_policy_label)
        if self.source_policy_label != REQUIRED_POLICY_LABEL_BY_FORECAST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 forecast input must use the locked source policy")
        self._require_not_applicable(
            "S27 v2 forecast runtime-history input label",
            self.runtime_history_input_label,
        )
        self._require_not_applicable("S27 v2 forecast runtime state family", self.runtime_state_family)
        self._require_not_applicable("S27 v2 forecast V/Q/M component", self.vqm_component_label)


@dataclass(frozen=True)
class ForecastDependencyBindingContract:
    dependency_label: str
    required_dependency_labels: tuple[str, ...]
    required_dependency_contract_hashes: tuple[str, ...]
    dependency_binding_policy_hash: str
    dependency_binding_contract_hash: str

    def validate_component(self) -> None:
        require_text("S27 v2 forecast component dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_FORECAST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 forecast component dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT[self.dependency_label])

    def validate_decision_branch(self) -> None:
        require_text("S27 v2 forecast decision-branch dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_FORECAST_DECISION_BRANCHES:
            raise CarverBlocked("S27 v2 forecast decision-branch dependency label is not locked")
        self._validate_required_dependencies(
            REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH[self.dependency_label]
        )

    def validate_invariant(self) -> None:
        require_text("S27 v2 forecast invariant dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_FORECAST_INVARIANTS:
            raise CarverBlocked("S27 v2 forecast invariant dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT[self.dependency_label])

    def _validate_required_dependencies(self, locked_labels: tuple[str, ...]) -> None:
        require_non_empty_tuple("S27 v2 forecast required dependency labels", self.required_dependency_labels)
        if self.required_dependency_labels != locked_labels:
            raise CarverBlocked("S27 v2 forecast dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 forecast required dependency contract hashes",
            self.required_dependency_contract_hashes,
        )
        if len(self.required_dependency_contract_hashes) != len(self.required_dependency_labels):
            raise CarverBlocked("S27 v2 forecast dependency hashes must match labels")
        for dependency_hash in self.required_dependency_contract_hashes:
            require_hash("S27 v2 forecast dependency contract hash", dependency_hash)
        require_hash("S27 v2 forecast dependency binding policy hash", self.dependency_binding_policy_hash)
        require_hash("S27 v2 forecast dependency binding contract hash", self.dependency_binding_contract_hash)


@dataclass(frozen=True)
class ForecastInputContractBundle:
    status: str
    source_input_manifest_contract_hash: str
    runtime_history_input_contract_hash: str
    runtime_history_contract_bundle_hash: str
    forecast_input_policy_hash: str
    input_field_contracts: tuple[ForecastInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    component_dependency_bindings: tuple[ForecastDependencyBindingContract, ...]
    decision_branch_dependency_bindings: tuple[ForecastDependencyBindingContract, ...]
    invariant_dependency_bindings: tuple[ForecastDependencyBindingContract, ...]
    forecast_input_set_hash: str
    forecast_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 forecast input requires runtime-history authority"
        )

    def validate_against_runtime_history_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
        level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
        level_compatibility_contract: LevelCompatibilityContractBundle,
        runtime_history_input_contract: RuntimeHistoryInputContractBundle,
        runtime_history_contract: RuntimeHistoryContractBundle,
    ) -> None:
        runtime_history_input_contract.validate_against_active_trust_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
            level_compatibility_input_contract,
            level_compatibility_contract,
        )
        runtime_history_contract.validate()
        require_text("S27 v2 forecast input contract status", self.status)
        if self.status != S27_V2_FORECAST_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 forecast input contract must remain contract-only")
        self._validate_locked_maps()
        require_hash(
            "S27 v2 forecast source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash(
            "S27 v2 forecast runtime-history input contract hash",
            self.runtime_history_input_contract_hash,
        )
        require_hash(
            "S27 v2 forecast runtime-history contract bundle hash",
            self.runtime_history_contract_bundle_hash,
        )
        require_hash("S27 v2 forecast input policy hash", self.forecast_input_policy_hash)
        require_hash_map(
            "S27 v2 forecast expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_FORECAST_INPUTS,
        )
        self._validate_runtime_history_authority(
            runtime_history_input_contract,
            runtime_history_contract,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 forecast expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(
                runtime_history_input_contract,
                runtime_history_contract,
            ),
            REQUIRED_FORECAST_INPUTS,
        )
        dependency_hash_by_label = self._validate_input_fields()
        self._validate_component_dependencies(dependency_hash_by_label)
        self._validate_decision_branch_dependencies(dependency_hash_by_label)
        self._validate_invariant_dependencies(dependency_hash_by_label)
        require_hash("S27 v2 forecast input set hash", self.forecast_input_set_hash)
        require_hash("S27 v2 forecast input contract hash", self.forecast_input_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 forecast input contract must preserve non-authorizations")

    def _validate_locked_maps(self) -> None:
        if tuple(REQUIRED_SOURCE_KIND_BY_FORECAST_INPUT) != REQUIRED_FORECAST_INPUTS:
            raise CarverBlocked("S27 v2 forecast input source-kind map must cover locked inputs")
        if tuple(REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT) != REQUIRED_FORECAST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 forecast component dependency map must cover locked components")
        if tuple(REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH) != REQUIRED_FORECAST_DECISION_BRANCHES:
            raise CarverBlocked("S27 v2 forecast branch dependency map must cover locked branches")
        if tuple(REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT) != REQUIRED_FORECAST_INVARIANTS:
            raise CarverBlocked("S27 v2 forecast invariant dependency map must cover locked invariants")

    def _active_source_contract_hash_by_input_label(
        self,
        runtime_history_input_contract: RuntimeHistoryInputContractBundle,
        runtime_history_contract: RuntimeHistoryContractBundle,
    ) -> dict[str, str]:
        runtime_input_contract_hash_by_label = self._runtime_input_field_contract_hash_by_label(
            runtime_history_input_contract,
        )
        runtime_state_contract_hash_by_family = self._runtime_state_contract_hash_by_family(
            runtime_history_contract,
        )
        vqm_component_contract_hash_by_label = self._vqm_component_contract_hash_by_label(
            runtime_history_contract,
        )
        active_hash_by_label: dict[str, str] = {}
        for input_label in REQUIRED_FORECAST_INPUTS:
            source_kind = REQUIRED_SOURCE_KIND_BY_FORECAST_INPUT[input_label]
            if source_kind == "RUNTIME_INPUT":
                active_hash_by_label[input_label] = runtime_input_contract_hash_by_label[
                    REQUIRED_RUNTIME_HISTORY_INPUT_BY_FORECAST_INPUT[input_label]
                ]
            elif source_kind == "RUNTIME_STATE":
                active_hash_by_label[input_label] = runtime_state_contract_hash_by_family[
                    REQUIRED_RUNTIME_STATE_BY_FORECAST_INPUT[input_label]
                ]
            elif source_kind == "VQM_COMPONENT":
                active_hash_by_label[input_label] = vqm_component_contract_hash_by_label[
                    REQUIRED_VQM_COMPONENT_BY_FORECAST_INPUT[input_label]
                ]
            elif source_kind == "POLICY_INPUT":
                active_hash_by_label[input_label] = self.forecast_input_policy_hash
            else:
                raise CarverBlocked("S27 v2 forecast input source kind cannot be authority-bound")
        return active_hash_by_label

    def _validate_runtime_history_authority(
        self,
        runtime_history_input_contract: RuntimeHistoryInputContractBundle,
        runtime_history_contract: RuntimeHistoryContractBundle,
    ) -> None:
        if (
            runtime_history_input_contract.runtime_history_input_contract_hash
            != self.runtime_history_input_contract_hash
        ):
            raise CarverBlocked("S27 v2 forecast input must bind runtime-history input contract")
        if (
            runtime_history_contract.runtime_history_contract_bundle_hash
            != self.runtime_history_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 forecast input must bind runtime-history contract bundle")
        if (
            runtime_history_input_contract.source_input_manifest_contract_hash
            != self.source_input_manifest_contract_hash
        ):
            raise CarverBlocked("S27 v2 forecast input must bind runtime-history source-input manifest")
        if (
            runtime_history_contract.source_binding.source_input_manifest_hash
            != runtime_history_input_contract.source_input_manifest_hash
        ):
            raise CarverBlocked("S27 v2 forecast input must bind runtime-history source manifest hash")

    def _runtime_input_field_contract_hash_by_label(
        self,
        runtime_history_input_contract: RuntimeHistoryInputContractBundle,
    ) -> dict[str, str]:
        runtime_input_contract_hash_by_label = {
            contract.input_label: contract.input_field_contract_hash
            for contract in runtime_history_input_contract.input_field_contracts
        }
        if tuple(runtime_input_contract_hash_by_label) != REQUIRED_RUNTIME_HISTORY_INPUTS:
            raise CarverBlocked("S27 v2 forecast runtime-history inputs must match locked tuple")
        return runtime_input_contract_hash_by_label

    def _runtime_state_contract_hash_by_family(
        self,
        runtime_history_contract: RuntimeHistoryContractBundle,
    ) -> dict[str, str]:
        runtime_state_contract_hash_by_family = {
            contract.state_family: contract.state_contract_hash
            for contract in runtime_history_contract.state_contracts
        }
        if tuple(runtime_state_contract_hash_by_family) != REQUIRED_RUNTIME_STATE_FAMILIES:
            raise CarverBlocked("S27 v2 forecast runtime states must match locked tuple")
        return runtime_state_contract_hash_by_family

    def _vqm_component_contract_hash_by_label(
        self,
        runtime_history_contract: RuntimeHistoryContractBundle,
    ) -> dict[str, str]:
        vqm_component_contract_hash_by_label = {
            contract.component_label: contract.component_contract_hash
            for contract in runtime_history_contract.vqm_component_contracts
        }
        if tuple(vqm_component_contract_hash_by_label) != REQUIRED_VQM_COMPONENTS:
            raise CarverBlocked("S27 v2 forecast V/Q/M components must match locked tuple")
        return vqm_component_contract_hash_by_label

    def _validate_input_fields(self) -> dict[str, str]:
        require_non_empty_tuple("S27 v2 forecast input field contracts", self.input_field_contracts)
        seen_inputs: set[str] = set()
        dependency_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 forecast input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 forecast input source contract hash",
                contract.input_label,
                contract.source_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            dependency_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_FORECAST_INPUTS:
            raise CarverBlocked("S27 v2 forecast inputs must match locked input tuple")
        return dependency_hash_by_label

    def _validate_component_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 forecast component dependency bindings",
            self.component_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.component_dependency_bindings)
            != REQUIRED_FORECAST_COMPONENT_FAMILIES
        ):
            raise CarverBlocked("S27 v2 forecast component dependencies must match locked components")
        seen_components: set[str] = set()
        for binding in self.component_dependency_bindings:
            binding.validate_component()
            if binding.dependency_label in seen_components:
                raise CarverBlocked("S27 v2 forecast component dependency bindings must be unique")
            seen_components.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_decision_branch_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 forecast decision-branch dependency bindings",
            self.decision_branch_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.decision_branch_dependency_bindings)
            != REQUIRED_FORECAST_DECISION_BRANCHES
        ):
            raise CarverBlocked("S27 v2 forecast decision-branch dependencies must match locked branches")
        seen_branches: set[str] = set()
        for binding in self.decision_branch_dependency_bindings:
            binding.validate_decision_branch()
            if binding.dependency_label in seen_branches:
                raise CarverBlocked("S27 v2 forecast decision-branch dependency bindings must be unique")
            seen_branches.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_invariant_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 forecast invariant dependency bindings",
            self.invariant_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.invariant_dependency_bindings)
            != REQUIRED_FORECAST_INVARIANTS
        ):
            raise CarverBlocked("S27 v2 forecast invariant dependencies must match locked invariants")
        seen_invariants: set[str] = set()
        for binding in self.invariant_dependency_bindings:
            binding.validate_invariant()
            if binding.dependency_label in seen_invariants:
                raise CarverBlocked("S27 v2 forecast invariant dependency bindings must be unique")
            seen_invariants.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)

    def _require_matching_dependency_hashes(
        self,
        binding: ForecastDependencyBindingContract,
        dependency_hash_by_label: dict[str, str],
    ) -> None:
        require_matching_dependency_hashes(
            "S27 v2 forecast",
            binding.required_dependency_labels,
            binding.required_dependency_contract_hashes,
            dependency_hash_by_label,
        )

from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest
from .forecast_contract import (
    REQUIRED_FORECAST_COMPONENT_FAMILIES,
    ForecastContractBundle,
)
from .forecast_input_contract import ForecastInputContractBundle
from .level_compatibility_contract import LevelCompatibilityContractBundle
from .level_compatibility_input_contract import LevelCompatibilityInputContractBundle
from .parser_output_contract import ParserOutputBatchSetContract
from .position_contract import (
    REQUIRED_POSITION_COMPONENT_FAMILIES,
    REQUIRED_POSITION_INVARIANTS,
    REQUIRED_ROUNDING_POLICY_LABELS,
)
from .runtime_history_contract import RuntimeHistoryContractBundle
from .runtime_history_input_contract import RuntimeHistoryInputContractBundle
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


S27_V2_POSITION_INPUT_CONTRACT_ONLY_STATUS = "S27_V2_POSITION_INPUT_CONTRACT_ONLY"
PLANNED_POSITION_INPUT_STATUS = "PLANNED_POSITION_INPUT_ONLY"

POSITION_INPUT_NOT_APPLICABLE = "NOT_APPLICABLE"

POSITION_INPUT_SOURCE_KINDS = (
    "FORECAST_COMPONENT",
    "FORECAST_LEDGER_OUTPUT",
    "ROUNDING_POLICY",
    "POSITION_STATE_CONTEXT",
    "POLICY_INPUT",
)

REQUIRED_POSITION_INPUTS = (
    "POSITION_FORECAST_HASH_INPUT",
    "POSITION_CAPPED_FORECAST_INPUT",
    "POSITION_DESIRED_POSITION_REFERENCE_INPUT",
    "POSITION_FORECAST_TO_POSITION_DIVISOR_POLICY_INPUT",
    "POSITION_ROUNDING_POLICY_INPUT",
    "POSITION_CURRENT_POSITION_CONTEXT_INPUT",
    "POSITION_INITIAL_POSITION_POLICY_INPUT",
)

REQUIRED_SOURCE_KIND_BY_POSITION_INPUT = {
    "POSITION_FORECAST_HASH_INPUT": "FORECAST_LEDGER_OUTPUT",
    "POSITION_CAPPED_FORECAST_INPUT": "FORECAST_COMPONENT",
    "POSITION_DESIRED_POSITION_REFERENCE_INPUT": "FORECAST_COMPONENT",
    "POSITION_FORECAST_TO_POSITION_DIVISOR_POLICY_INPUT": "POLICY_INPUT",
    "POSITION_ROUNDING_POLICY_INPUT": "ROUNDING_POLICY",
    "POSITION_CURRENT_POSITION_CONTEXT_INPUT": "POSITION_STATE_CONTEXT",
    "POSITION_INITIAL_POSITION_POLICY_INPUT": "POLICY_INPUT",
}

REQUIRED_FORECAST_COMPONENT_BY_POSITION_INPUT = {
    "POSITION_CAPPED_FORECAST_INPUT": "SCALAR_AND_CAP_APPLICATION",
    "POSITION_DESIRED_POSITION_REFERENCE_INPUT": "DESIRED_POSITION_REFERENCE",
}

REQUIRED_FORECAST_LEDGER_OUTPUT_BY_POSITION_INPUT = {
    "POSITION_FORECAST_HASH_INPUT": "FORECAST_LEDGER_ROW_HASH",
}

REQUIRED_ROUNDING_POLICY_BY_POSITION_INPUT = {
    "POSITION_ROUNDING_POLICY_INPUT": "NEAREST",
}

REQUIRED_POSITION_STATE_CONTEXT_BY_POSITION_INPUT = {
    "POSITION_CURRENT_POSITION_CONTEXT_INPUT": "CURRENT_POSITION_CONTEXT",
}

REQUIRED_POLICY_LABEL_BY_POSITION_INPUT = {
    "POSITION_FORECAST_TO_POSITION_DIVISOR_POLICY_INPUT": "FORECAST_TO_POSITION_DIVISOR_POLICY",
    "POSITION_INITIAL_POSITION_POLICY_INPUT": "INITIAL_POSITION_POLICY",
}

REQUIRED_POSITION_DEPENDENCIES_BY_COMPONENT = {
    "FORECAST_TO_POSITION_DIVISOR": (
        "POSITION_FORECAST_TO_POSITION_DIVISOR_POLICY_INPUT",
    ),
    "DESIRED_UNROUNDED_POSITION": (
        "POSITION_CAPPED_FORECAST_INPUT",
        "POSITION_DESIRED_POSITION_REFERENCE_INPUT",
        "FORECAST_TO_POSITION_DIVISOR",
    ),
    "ROUNDING_POLICY_APPLICATION": (
        "DESIRED_UNROUNDED_POSITION",
        "POSITION_ROUNDING_POLICY_INPUT",
    ),
    "DESIRED_ROUNDED_POSITION": (
        "ROUNDING_POLICY_APPLICATION",
    ),
    "CURRENT_POSITION_CONTEXT": (
        "POSITION_CURRENT_POSITION_CONTEXT_INPUT",
    ),
    "INITIAL_POSITION_POLICY": (
        "POSITION_INITIAL_POSITION_POLICY_INPUT",
    ),
}

REQUIRED_POSITION_DEPENDENCIES_BY_INVARIANT = {
    "FORECAST_LEDGER_HASH_BINDING": (
        "POSITION_FORECAST_HASH_INPUT",
        "POSITION_CAPPED_FORECAST_INPUT",
        "POSITION_DESIRED_POSITION_REFERENCE_INPUT",
    ),
    "DESIRED_UNROUNDED_POSITION_HASH_BINDING": (
        "DESIRED_UNROUNDED_POSITION",
    ),
    "ROUNDING_POLICY_SOURCE_BINDING": (
        "POSITION_ROUNDING_POLICY_INPUT",
        "ROUNDING_POLICY_APPLICATION",
    ),
    "ROUNDED_POSITION_HASH_BINDING": (
        "DESIRED_ROUNDED_POSITION",
    ),
    "CURRENT_POSITION_STATE_HASH_BINDING": (
        "CURRENT_POSITION_CONTEXT",
    ),
    "NO_ORDER_GENERATION_IN_POSITION_CONTRACT": (
        "DESIRED_ROUNDED_POSITION",
        "CURRENT_POSITION_CONTEXT",
    ),
}


@dataclass(frozen=True)
class PositionInputFieldContract:
    input_label: str
    input_status: str
    source_kind: str
    forecast_input_label: str
    forecast_component_family: str
    forecast_ledger_output_label: str
    rounding_policy_label: str
    position_state_context_label: str
    source_policy_label: str
    source_contract_hash: str
    position_input_policy_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 position input label", self.input_label)
        if self.input_label not in REQUIRED_POSITION_INPUTS:
            raise CarverBlocked("S27 v2 position input label is not locked")
        require_text("S27 v2 position input status", self.input_status)
        if self.input_status != PLANNED_POSITION_INPUT_STATUS:
            raise CarverBlocked("S27 v2 position input must remain planned-only")
        require_text("S27 v2 position input source kind", self.source_kind)
        if self.source_kind not in POSITION_INPUT_SOURCE_KINDS:
            raise CarverBlocked("S27 v2 position input source kind is not locked")
        if self.source_kind != REQUIRED_SOURCE_KIND_BY_POSITION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 position input must use the locked source kind")
        self._validate_source_target()
        require_hash("S27 v2 position input source contract hash", self.source_contract_hash)
        require_hash("S27 v2 position input policy hash", self.position_input_policy_hash)
        require_hash("S27 v2 position input field contract hash", self.input_field_contract_hash)

    def _validate_source_target(self) -> None:
        if self.source_kind == "FORECAST_COMPONENT":
            self._validate_forecast_component_target()
        elif self.source_kind == "FORECAST_LEDGER_OUTPUT":
            self._validate_forecast_ledger_output_target()
        elif self.source_kind == "ROUNDING_POLICY":
            self._validate_rounding_policy_target()
        elif self.source_kind == "POSITION_STATE_CONTEXT":
            self._validate_position_state_context_target()
        elif self.source_kind == "POLICY_INPUT":
            self._validate_policy_input_target()

    def _require_not_applicable(self, name: str, value: str) -> None:
        require_text(name, value)
        if value != POSITION_INPUT_NOT_APPLICABLE:
            raise CarverBlocked(f"{name} must be not applicable")

    def _validate_forecast_component_target(self) -> None:
        require_text("S27 v2 position forecast component family", self.forecast_component_family)
        if self.forecast_component_family not in REQUIRED_FORECAST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 position forecast component family is not locked")
        if self.forecast_component_family != REQUIRED_FORECAST_COMPONENT_BY_POSITION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 position input must use the locked forecast component")
        self._require_not_applicable("S27 v2 position forecast input label", self.forecast_input_label)
        self._require_not_applicable(
            "S27 v2 position forecast ledger output",
            self.forecast_ledger_output_label,
        )
        self._require_not_applicable("S27 v2 position rounding policy label", self.rounding_policy_label)
        self._require_not_applicable(
            "S27 v2 position state context label",
            self.position_state_context_label,
        )
        self._require_not_applicable("S27 v2 position source policy label", self.source_policy_label)

    def _validate_forecast_ledger_output_target(self) -> None:
        require_text("S27 v2 position forecast ledger output", self.forecast_ledger_output_label)
        if (
            self.forecast_ledger_output_label
            != REQUIRED_FORECAST_LEDGER_OUTPUT_BY_POSITION_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 position input must use the locked forecast ledger output")
        self._require_not_applicable("S27 v2 position forecast input label", self.forecast_input_label)
        self._require_not_applicable(
            "S27 v2 position forecast component family",
            self.forecast_component_family,
        )
        self._require_not_applicable("S27 v2 position rounding policy label", self.rounding_policy_label)
        self._require_not_applicable(
            "S27 v2 position state context label",
            self.position_state_context_label,
        )
        self._require_not_applicable("S27 v2 position source policy label", self.source_policy_label)

    def _validate_rounding_policy_target(self) -> None:
        require_text("S27 v2 position rounding policy label", self.rounding_policy_label)
        if self.rounding_policy_label not in REQUIRED_ROUNDING_POLICY_LABELS:
            raise CarverBlocked("S27 v2 position rounding policy label is not locked")
        if self.rounding_policy_label != REQUIRED_ROUNDING_POLICY_BY_POSITION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 position input must use the locked rounding policy")
        self._require_not_applicable("S27 v2 position forecast input label", self.forecast_input_label)
        self._require_not_applicable(
            "S27 v2 position forecast component family",
            self.forecast_component_family,
        )
        self._require_not_applicable(
            "S27 v2 position forecast ledger output",
            self.forecast_ledger_output_label,
        )
        self._require_not_applicable(
            "S27 v2 position state context label",
            self.position_state_context_label,
        )
        self._require_not_applicable("S27 v2 position source policy label", self.source_policy_label)

    def _validate_position_state_context_target(self) -> None:
        require_text("S27 v2 position state context label", self.position_state_context_label)
        if (
            self.position_state_context_label
            != REQUIRED_POSITION_STATE_CONTEXT_BY_POSITION_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 position input must use the locked position state context")
        self._require_not_applicable("S27 v2 position forecast input label", self.forecast_input_label)
        self._require_not_applicable(
            "S27 v2 position forecast component family",
            self.forecast_component_family,
        )
        self._require_not_applicable(
            "S27 v2 position forecast ledger output",
            self.forecast_ledger_output_label,
        )
        self._require_not_applicable("S27 v2 position rounding policy label", self.rounding_policy_label)
        self._require_not_applicable("S27 v2 position source policy label", self.source_policy_label)

    def _validate_policy_input_target(self) -> None:
        require_text("S27 v2 position source policy label", self.source_policy_label)
        if self.source_policy_label != REQUIRED_POLICY_LABEL_BY_POSITION_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 position input must use the locked source policy")
        self._require_not_applicable("S27 v2 position forecast input label", self.forecast_input_label)
        self._require_not_applicable(
            "S27 v2 position forecast component family",
            self.forecast_component_family,
        )
        self._require_not_applicable(
            "S27 v2 position forecast ledger output",
            self.forecast_ledger_output_label,
        )
        self._require_not_applicable("S27 v2 position rounding policy label", self.rounding_policy_label)
        self._require_not_applicable(
            "S27 v2 position state context label",
            self.position_state_context_label,
        )


@dataclass(frozen=True)
class PositionDependencyBindingContract:
    dependency_label: str
    required_dependency_labels: tuple[str, ...]
    required_dependency_contract_hashes: tuple[str, ...]
    dependency_binding_policy_hash: str
    dependency_binding_contract_hash: str

    def validate_component(self) -> None:
        require_text("S27 v2 position component dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_POSITION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 position component dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_POSITION_DEPENDENCIES_BY_COMPONENT[self.dependency_label])

    def validate_invariant(self) -> None:
        require_text("S27 v2 position invariant dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_POSITION_INVARIANTS:
            raise CarverBlocked("S27 v2 position invariant dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_POSITION_DEPENDENCIES_BY_INVARIANT[self.dependency_label])

    def _validate_required_dependencies(self, locked_labels: tuple[str, ...]) -> None:
        require_non_empty_tuple("S27 v2 position required dependency labels", self.required_dependency_labels)
        if self.required_dependency_labels != locked_labels:
            raise CarverBlocked("S27 v2 position dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 position required dependency contract hashes",
            self.required_dependency_contract_hashes,
        )
        if len(self.required_dependency_contract_hashes) != len(self.required_dependency_labels):
            raise CarverBlocked("S27 v2 position dependency hashes must match labels")
        for dependency_hash in self.required_dependency_contract_hashes:
            require_hash("S27 v2 position dependency contract hash", dependency_hash)
        require_hash("S27 v2 position dependency binding policy hash", self.dependency_binding_policy_hash)
        require_hash("S27 v2 position dependency binding contract hash", self.dependency_binding_contract_hash)


@dataclass(frozen=True)
class PositionInputContractBundle:
    status: str
    source_input_manifest_contract_hash: str
    forecast_input_contract_hash: str
    forecast_contract_bundle_hash: str
    position_input_policy_hash: str
    input_field_contracts: tuple[PositionInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    component_dependency_bindings: tuple[PositionDependencyBindingContract, ...]
    invariant_dependency_bindings: tuple[PositionDependencyBindingContract, ...]
    position_input_set_hash: str
    position_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 position input requires forecast authority"
        )

    def validate_against_forecast_authority(
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
        forecast_input_contract: ForecastInputContractBundle,
        forecast_contract: ForecastContractBundle,
    ) -> None:
        forecast_input_contract.validate_against_runtime_history_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
            level_compatibility_input_contract,
            level_compatibility_contract,
            runtime_history_input_contract,
            runtime_history_contract,
        )
        forecast_contract.validate()
        require_text("S27 v2 position input contract status", self.status)
        if self.status != S27_V2_POSITION_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 position input contract must remain contract-only")
        self._validate_locked_maps()
        require_hash(
            "S27 v2 position source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash("S27 v2 position forecast input contract hash", self.forecast_input_contract_hash)
        require_hash("S27 v2 position forecast contract bundle hash", self.forecast_contract_bundle_hash)
        require_hash("S27 v2 position input policy hash", self.position_input_policy_hash)
        require_hash_map(
            "S27 v2 position expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_POSITION_INPUTS,
        )
        self._validate_forecast_authority(forecast_input_contract, forecast_contract)
        require_hash_map_matches_active_authority(
            "S27 v2 position expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(forecast_contract),
            REQUIRED_POSITION_INPUTS,
        )
        dependency_hash_by_label = self._validate_input_fields()
        self._validate_component_dependencies(dependency_hash_by_label)
        self._validate_invariant_dependencies(dependency_hash_by_label)
        require_hash("S27 v2 position input set hash", self.position_input_set_hash)
        require_hash("S27 v2 position input contract hash", self.position_input_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 position input contract must preserve non-authorizations")

    def _validate_locked_maps(self) -> None:
        if tuple(REQUIRED_SOURCE_KIND_BY_POSITION_INPUT) != REQUIRED_POSITION_INPUTS:
            raise CarverBlocked("S27 v2 position input source-kind map must cover locked inputs")
        if tuple(REQUIRED_POSITION_DEPENDENCIES_BY_COMPONENT) != REQUIRED_POSITION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 position component dependency map must cover locked components")
        if tuple(REQUIRED_POSITION_DEPENDENCIES_BY_INVARIANT) != REQUIRED_POSITION_INVARIANTS:
            raise CarverBlocked("S27 v2 position invariant dependency map must cover locked invariants")

    def _active_source_contract_hash_by_input_label(
        self,
        forecast_contract: ForecastContractBundle,
    ) -> dict[str, str]:
        forecast_component_contract_hash_by_family = self._forecast_component_contract_hash_by_family(
            forecast_contract,
        )
        active_hash_by_label: dict[str, str] = {}
        for input_label in REQUIRED_POSITION_INPUTS:
            source_kind = REQUIRED_SOURCE_KIND_BY_POSITION_INPUT[input_label]
            if source_kind == "FORECAST_COMPONENT":
                active_hash_by_label[input_label] = forecast_component_contract_hash_by_family[
                    REQUIRED_FORECAST_COMPONENT_BY_POSITION_INPUT[input_label]
                ]
            elif source_kind == "FORECAST_LEDGER_OUTPUT":
                active_hash_by_label[input_label] = forecast_contract.forecast_contract_bundle_hash
            elif source_kind in {"ROUNDING_POLICY", "POSITION_STATE_CONTEXT", "POLICY_INPUT"}:
                active_hash_by_label[input_label] = self.position_input_policy_hash
            else:
                raise CarverBlocked("S27 v2 position input source kind cannot be authority-bound")
        return active_hash_by_label

    def _validate_forecast_authority(
        self,
        forecast_input_contract: ForecastInputContractBundle,
        forecast_contract: ForecastContractBundle,
    ) -> None:
        if forecast_input_contract.forecast_input_contract_hash != self.forecast_input_contract_hash:
            raise CarverBlocked("S27 v2 position input must bind forecast input contract")
        if forecast_contract.forecast_contract_bundle_hash != self.forecast_contract_bundle_hash:
            raise CarverBlocked("S27 v2 position input must bind forecast contract bundle")
        if forecast_input_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 position input must bind forecast source-input manifest")
        if (
            forecast_contract.source_binding.runtime_history_contract_bundle_hash
            != forecast_input_contract.runtime_history_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 position input must bind forecast runtime-history authority")

    def _forecast_component_contract_hash_by_family(
        self,
        forecast_contract: ForecastContractBundle,
    ) -> dict[str, str]:
        forecast_component_contract_hash_by_family = {
            contract.component_family: contract.component_contract_hash
            for contract in forecast_contract.component_contracts
        }
        if tuple(forecast_component_contract_hash_by_family) != REQUIRED_FORECAST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 position forecast components must match locked tuple")
        return forecast_component_contract_hash_by_family

    def _validate_input_fields(self) -> dict[str, str]:
        require_non_empty_tuple("S27 v2 position input field contracts", self.input_field_contracts)
        seen_inputs: set[str] = set()
        dependency_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 position input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 position input source contract hash",
                contract.input_label,
                contract.source_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            dependency_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_POSITION_INPUTS:
            raise CarverBlocked("S27 v2 position inputs must match locked input tuple")
        return dependency_hash_by_label

    def _validate_component_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 position component dependency bindings",
            self.component_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.component_dependency_bindings)
            != REQUIRED_POSITION_COMPONENT_FAMILIES
        ):
            raise CarverBlocked("S27 v2 position component dependencies must match locked components")
        seen_components: set[str] = set()
        for binding in self.component_dependency_bindings:
            binding.validate_component()
            if binding.dependency_label in seen_components:
                raise CarverBlocked("S27 v2 position component dependency bindings must be unique")
            seen_components.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_invariant_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 position invariant dependency bindings",
            self.invariant_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.invariant_dependency_bindings)
            != REQUIRED_POSITION_INVARIANTS
        ):
            raise CarverBlocked("S27 v2 position invariant dependencies must match locked invariants")
        seen_invariants: set[str] = set()
        for binding in self.invariant_dependency_bindings:
            binding.validate_invariant()
            if binding.dependency_label in seen_invariants:
                raise CarverBlocked("S27 v2 position invariant dependency bindings must be unique")
            seen_invariants.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)

    def _require_matching_dependency_hashes(
        self,
        binding: PositionDependencyBindingContract,
        dependency_hash_by_label: dict[str, str],
    ) -> None:
        require_matching_dependency_hashes(
            "S27 v2 position",
            binding.required_dependency_labels,
            binding.required_dependency_contract_hashes,
            dependency_hash_by_label,
        )

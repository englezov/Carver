from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest
from .forecast_contract import ForecastContractBundle
from .forecast_input_contract import ForecastInputContractBundle
from .level_compatibility_contract import LevelCompatibilityContractBundle
from .level_compatibility_input_contract import LevelCompatibilityInputContractBundle
from .order_contract import (
    REQUIRED_ORDER_COMPONENT_FAMILIES,
    REQUIRED_ORDER_INVARIANTS,
    REQUIRED_ORDER_KIND_LABELS,
    REQUIRED_ORDER_TRANSITION_KIND_LABELS,
)
from .parser_output_contract import ParserOutputBatchSetContract
from .position_contract import (
    REQUIRED_POSITION_COMPONENT_FAMILIES,
    PositionContractBundle,
)
from .position_input_contract import PositionInputContractBundle
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


S27_V2_ORDER_INPUT_CONTRACT_ONLY_STATUS = "S27_V2_ORDER_INPUT_CONTRACT_ONLY"
PLANNED_ORDER_INPUT_STATUS = "PLANNED_ORDER_INPUT_ONLY"

ORDER_INPUT_NOT_APPLICABLE = "NOT_APPLICABLE"

ORDER_INPUT_SOURCE_KINDS = (
    "POSITION_COMPONENT",
    "POSITION_LEDGER_OUTPUT",
    "ORDER_KIND",
    "ORDER_TRANSITION_KIND",
    "ORDER_STATE_CONTEXT",
    "POLICY_INPUT",
)

REQUIRED_ORDER_INPUTS = (
    "ORDER_DESIRED_POSITION_HASH_INPUT",
    "ORDER_DESIRED_ROUNDED_POSITION_INPUT",
    "ORDER_CURRENT_POSITION_CONTEXT_INPUT",
    "ORDER_LIMIT_KIND_POLICY_INPUT",
    "ORDER_MARKET_KIND_POLICY_INPUT",
    "ORDER_NORMAL_ONE_HOUR_LAG_TRANSITION_INPUT",
    "ORDER_EOD_OVERNIGHT_RECOMPUTE_TRANSITION_INPUT",
    "ORDER_ROLL_BOUNDARY_TRANSITION_INPUT",
    "ORDER_WORKING_ORDER_STATE_CONTEXT_INPUT",
    "ORDER_TICK_ROUNDING_POLICY_INPUT",
    "ORDER_ADJACENT_LIMIT_LADDER_POLICY_INPUT",
    "ORDER_MARKET_FALLBACK_POLICY_INPUT",
)

REQUIRED_SOURCE_KIND_BY_ORDER_INPUT = {
    "ORDER_DESIRED_POSITION_HASH_INPUT": "POSITION_LEDGER_OUTPUT",
    "ORDER_DESIRED_ROUNDED_POSITION_INPUT": "POSITION_COMPONENT",
    "ORDER_CURRENT_POSITION_CONTEXT_INPUT": "POSITION_COMPONENT",
    "ORDER_LIMIT_KIND_POLICY_INPUT": "ORDER_KIND",
    "ORDER_MARKET_KIND_POLICY_INPUT": "ORDER_KIND",
    "ORDER_NORMAL_ONE_HOUR_LAG_TRANSITION_INPUT": "ORDER_TRANSITION_KIND",
    "ORDER_EOD_OVERNIGHT_RECOMPUTE_TRANSITION_INPUT": "ORDER_TRANSITION_KIND",
    "ORDER_ROLL_BOUNDARY_TRANSITION_INPUT": "ORDER_TRANSITION_KIND",
    "ORDER_WORKING_ORDER_STATE_CONTEXT_INPUT": "ORDER_STATE_CONTEXT",
    "ORDER_TICK_ROUNDING_POLICY_INPUT": "POLICY_INPUT",
    "ORDER_ADJACENT_LIMIT_LADDER_POLICY_INPUT": "POLICY_INPUT",
    "ORDER_MARKET_FALLBACK_POLICY_INPUT": "POLICY_INPUT",
}

REQUIRED_POSITION_COMPONENT_BY_ORDER_INPUT = {
    "ORDER_DESIRED_ROUNDED_POSITION_INPUT": "DESIRED_ROUNDED_POSITION",
    "ORDER_CURRENT_POSITION_CONTEXT_INPUT": "CURRENT_POSITION_CONTEXT",
}

REQUIRED_POSITION_LEDGER_OUTPUT_BY_ORDER_INPUT = {
    "ORDER_DESIRED_POSITION_HASH_INPUT": "DESIRED_POSITION_LEDGER_ROW_HASH",
}

REQUIRED_ORDER_KIND_BY_ORDER_INPUT = {
    "ORDER_LIMIT_KIND_POLICY_INPUT": "LIMIT",
    "ORDER_MARKET_KIND_POLICY_INPUT": "MARKET",
}

REQUIRED_ORDER_TRANSITION_KIND_BY_ORDER_INPUT = {
    "ORDER_NORMAL_ONE_HOUR_LAG_TRANSITION_INPUT": "NORMAL_ONE_HOUR_LAG",
    "ORDER_EOD_OVERNIGHT_RECOMPUTE_TRANSITION_INPUT": "EOD_OVERNIGHT_RECOMPUTE",
    "ORDER_ROLL_BOUNDARY_TRANSITION_INPUT": "ROLL_BOUNDARY",
}

REQUIRED_ORDER_STATE_CONTEXT_BY_ORDER_INPUT = {
    "ORDER_WORKING_ORDER_STATE_CONTEXT_INPUT": "WORKING_ORDER_STATE_CONTEXT",
}

REQUIRED_POLICY_LABEL_BY_ORDER_INPUT = {
    "ORDER_TICK_ROUNDING_POLICY_INPUT": "TICK_ROUNDING_POLICY",
    "ORDER_ADJACENT_LIMIT_LADDER_POLICY_INPUT": "ADJACENT_LIMIT_LADDER_POLICY",
    "ORDER_MARKET_FALLBACK_POLICY_INPUT": "MARKET_FALLBACK_POLICY",
}

REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT = {
    "LIMIT_ORDER_PLAN": (
        "ORDER_DESIRED_ROUNDED_POSITION_INPUT",
        "ORDER_CURRENT_POSITION_CONTEXT_INPUT",
        "ORDER_LIMIT_KIND_POLICY_INPUT",
        "ORDER_NORMAL_ONE_HOUR_LAG_TRANSITION_INPUT",
        "ORDER_WORKING_ORDER_STATE_CONTEXT_INPUT",
        "ORDER_ADJACENT_LIMIT_LADDER_POLICY_INPUT",
        "ORDER_TICK_ROUNDING_POLICY_INPUT",
    ),
    "MARKET_ORDER_PLAN": (
        "ORDER_DESIRED_ROUNDED_POSITION_INPUT",
        "ORDER_CURRENT_POSITION_CONTEXT_INPUT",
        "ORDER_MARKET_KIND_POLICY_INPUT",
        "ORDER_EOD_OVERNIGHT_RECOMPUTE_TRANSITION_INPUT",
        "ORDER_ROLL_BOUNDARY_TRANSITION_INPUT",
        "ORDER_MARKET_FALLBACK_POLICY_INPUT",
    ),
    "ADJACENT_POSITION_LIMIT_LADDER": (
        "ORDER_DESIRED_ROUNDED_POSITION_INPUT",
        "ORDER_CURRENT_POSITION_CONTEXT_INPUT",
        "ORDER_ADJACENT_LIMIT_LADDER_POLICY_INPUT",
        "ORDER_TICK_ROUNDING_POLICY_INPUT",
    ),
    "TICK_ROUNDING_POLICY": (
        "ORDER_TICK_ROUNDING_POLICY_INPUT",
    ),
    "WORKING_ORDER_STATE_REFERENCE": (
        "ORDER_WORKING_ORDER_STATE_CONTEXT_INPUT",
    ),
    "TRANSITION_KIND_REFERENCE": (
        "ORDER_NORMAL_ONE_HOUR_LAG_TRANSITION_INPUT",
        "ORDER_EOD_OVERNIGHT_RECOMPUTE_TRANSITION_INPUT",
        "ORDER_ROLL_BOUNDARY_TRANSITION_INPUT",
    ),
}

REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT = {
    "DESIRED_POSITION_LEDGER_HASH_BINDING": (
        "ORDER_DESIRED_POSITION_HASH_INPUT",
        "ORDER_DESIRED_ROUNDED_POSITION_INPUT",
    ),
    "CURRENT_POSITION_STATE_HASH_BINDING": (
        "ORDER_CURRENT_POSITION_CONTEXT_INPUT",
    ),
    "ADJACENT_LIMIT_SINGLE_LOT_BINDING": (
        "ADJACENT_POSITION_LIMIT_LADDER",
        "LIMIT_ORDER_PLAN",
    ),
    "MARKET_ORDER_DELTA_QUANTITY_BINDING": (
        "MARKET_ORDER_PLAN",
    ),
    "TICK_ROUNDING_POLICY_BINDING": (
        "ORDER_TICK_ROUNDING_POLICY_INPUT",
        "TICK_ROUNDING_POLICY",
    ),
    "NO_FILL_EXECUTION_IN_ORDER_CONTRACT": (
        "LIMIT_ORDER_PLAN",
        "MARKET_ORDER_PLAN",
        "WORKING_ORDER_STATE_REFERENCE",
    ),
}


@dataclass(frozen=True)
class OrderInputFieldContract:
    input_label: str
    input_status: str
    source_kind: str
    position_component_family: str
    position_ledger_output_label: str
    order_kind_label: str
    order_transition_kind_label: str
    order_state_context_label: str
    source_policy_label: str
    source_contract_hash: str
    order_input_policy_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 order input label", self.input_label)
        if self.input_label not in REQUIRED_ORDER_INPUTS:
            raise CarverBlocked("S27 v2 order input label is not locked")
        require_text("S27 v2 order input status", self.input_status)
        if self.input_status != PLANNED_ORDER_INPUT_STATUS:
            raise CarverBlocked("S27 v2 order input must remain planned-only")
        require_text("S27 v2 order input source kind", self.source_kind)
        if self.source_kind not in ORDER_INPUT_SOURCE_KINDS:
            raise CarverBlocked("S27 v2 order input source kind is not locked")
        if self.source_kind != REQUIRED_SOURCE_KIND_BY_ORDER_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 order input must use the locked source kind")
        self._validate_source_target()
        require_hash("S27 v2 order input source contract hash", self.source_contract_hash)
        require_hash("S27 v2 order input policy hash", self.order_input_policy_hash)
        require_hash("S27 v2 order input field contract hash", self.input_field_contract_hash)

    def _validate_source_target(self) -> None:
        if self.source_kind == "POSITION_COMPONENT":
            self._validate_position_component_target()
        elif self.source_kind == "POSITION_LEDGER_OUTPUT":
            self._validate_position_ledger_output_target()
        elif self.source_kind == "ORDER_KIND":
            self._validate_order_kind_target()
        elif self.source_kind == "ORDER_TRANSITION_KIND":
            self._validate_order_transition_kind_target()
        elif self.source_kind == "ORDER_STATE_CONTEXT":
            self._validate_order_state_context_target()
        elif self.source_kind == "POLICY_INPUT":
            self._validate_policy_input_target()

    def _require_not_applicable(self, name: str, value: str) -> None:
        require_text(name, value)
        if value != ORDER_INPUT_NOT_APPLICABLE:
            raise CarverBlocked(f"{name} must be not applicable")

    def _validate_position_component_target(self) -> None:
        require_text("S27 v2 order position component family", self.position_component_family)
        if self.position_component_family not in REQUIRED_POSITION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 order position component family is not locked")
        if self.position_component_family != REQUIRED_POSITION_COMPONENT_BY_ORDER_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 order input must use the locked position component")
        self._require_not_applicable("S27 v2 order position ledger output", self.position_ledger_output_label)
        self._require_not_applicable("S27 v2 order kind label", self.order_kind_label)
        self._require_not_applicable(
            "S27 v2 order transition kind label",
            self.order_transition_kind_label,
        )
        self._require_not_applicable("S27 v2 order state context label", self.order_state_context_label)
        self._require_not_applicable("S27 v2 order source policy label", self.source_policy_label)

    def _validate_position_ledger_output_target(self) -> None:
        require_text("S27 v2 order position ledger output", self.position_ledger_output_label)
        if self.position_ledger_output_label != REQUIRED_POSITION_LEDGER_OUTPUT_BY_ORDER_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 order input must use the locked position ledger output")
        self._require_not_applicable(
            "S27 v2 order position component family",
            self.position_component_family,
        )
        self._require_not_applicable("S27 v2 order kind label", self.order_kind_label)
        self._require_not_applicable(
            "S27 v2 order transition kind label",
            self.order_transition_kind_label,
        )
        self._require_not_applicable("S27 v2 order state context label", self.order_state_context_label)
        self._require_not_applicable("S27 v2 order source policy label", self.source_policy_label)

    def _validate_order_kind_target(self) -> None:
        require_text("S27 v2 order kind label", self.order_kind_label)
        if self.order_kind_label not in REQUIRED_ORDER_KIND_LABELS:
            raise CarverBlocked("S27 v2 order kind label is not locked")
        if self.order_kind_label != REQUIRED_ORDER_KIND_BY_ORDER_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 order input must use the locked order kind")
        self._require_not_applicable(
            "S27 v2 order position component family",
            self.position_component_family,
        )
        self._require_not_applicable("S27 v2 order position ledger output", self.position_ledger_output_label)
        self._require_not_applicable(
            "S27 v2 order transition kind label",
            self.order_transition_kind_label,
        )
        self._require_not_applicable("S27 v2 order state context label", self.order_state_context_label)
        self._require_not_applicable("S27 v2 order source policy label", self.source_policy_label)

    def _validate_order_transition_kind_target(self) -> None:
        require_text("S27 v2 order transition kind label", self.order_transition_kind_label)
        if self.order_transition_kind_label not in REQUIRED_ORDER_TRANSITION_KIND_LABELS:
            raise CarverBlocked("S27 v2 order transition kind label is not locked")
        if self.order_transition_kind_label != REQUIRED_ORDER_TRANSITION_KIND_BY_ORDER_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 order input must use the locked transition kind")
        self._require_not_applicable(
            "S27 v2 order position component family",
            self.position_component_family,
        )
        self._require_not_applicable("S27 v2 order position ledger output", self.position_ledger_output_label)
        self._require_not_applicable("S27 v2 order kind label", self.order_kind_label)
        self._require_not_applicable("S27 v2 order state context label", self.order_state_context_label)
        self._require_not_applicable("S27 v2 order source policy label", self.source_policy_label)

    def _validate_order_state_context_target(self) -> None:
        require_text("S27 v2 order state context label", self.order_state_context_label)
        if self.order_state_context_label != REQUIRED_ORDER_STATE_CONTEXT_BY_ORDER_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 order input must use the locked order state context")
        self._require_not_applicable(
            "S27 v2 order position component family",
            self.position_component_family,
        )
        self._require_not_applicable("S27 v2 order position ledger output", self.position_ledger_output_label)
        self._require_not_applicable("S27 v2 order kind label", self.order_kind_label)
        self._require_not_applicable(
            "S27 v2 order transition kind label",
            self.order_transition_kind_label,
        )
        self._require_not_applicable("S27 v2 order source policy label", self.source_policy_label)

    def _validate_policy_input_target(self) -> None:
        require_text("S27 v2 order source policy label", self.source_policy_label)
        if self.source_policy_label != REQUIRED_POLICY_LABEL_BY_ORDER_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 order input must use the locked source policy")
        self._require_not_applicable(
            "S27 v2 order position component family",
            self.position_component_family,
        )
        self._require_not_applicable("S27 v2 order position ledger output", self.position_ledger_output_label)
        self._require_not_applicable("S27 v2 order kind label", self.order_kind_label)
        self._require_not_applicable(
            "S27 v2 order transition kind label",
            self.order_transition_kind_label,
        )
        self._require_not_applicable("S27 v2 order state context label", self.order_state_context_label)


@dataclass(frozen=True)
class OrderDependencyBindingContract:
    dependency_label: str
    required_dependency_labels: tuple[str, ...]
    required_dependency_contract_hashes: tuple[str, ...]
    dependency_binding_policy_hash: str
    dependency_binding_contract_hash: str

    def validate_component(self) -> None:
        require_text("S27 v2 order component dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_ORDER_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 order component dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT[self.dependency_label])

    def validate_invariant(self) -> None:
        require_text("S27 v2 order invariant dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_ORDER_INVARIANTS:
            raise CarverBlocked("S27 v2 order invariant dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT[self.dependency_label])

    def _validate_required_dependencies(self, locked_labels: tuple[str, ...]) -> None:
        require_non_empty_tuple("S27 v2 order required dependency labels", self.required_dependency_labels)
        if self.required_dependency_labels != locked_labels:
            raise CarverBlocked("S27 v2 order dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 order required dependency contract hashes",
            self.required_dependency_contract_hashes,
        )
        if len(self.required_dependency_contract_hashes) != len(self.required_dependency_labels):
            raise CarverBlocked("S27 v2 order dependency hashes must match labels")
        for dependency_hash in self.required_dependency_contract_hashes:
            require_hash("S27 v2 order dependency contract hash", dependency_hash)
        require_hash("S27 v2 order dependency binding policy hash", self.dependency_binding_policy_hash)
        require_hash("S27 v2 order dependency binding contract hash", self.dependency_binding_contract_hash)


@dataclass(frozen=True)
class OrderInputContractBundle:
    status: str
    source_input_manifest_contract_hash: str
    position_input_contract_hash: str
    position_contract_bundle_hash: str
    order_input_policy_hash: str
    input_field_contracts: tuple[OrderInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    component_dependency_bindings: tuple[OrderDependencyBindingContract, ...]
    invariant_dependency_bindings: tuple[OrderDependencyBindingContract, ...]
    order_input_set_hash: str
    order_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 order input requires position authority"
        )

    def validate_against_position_authority(
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
        position_input_contract: PositionInputContractBundle,
        position_contract: PositionContractBundle,
    ) -> None:
        position_input_contract.validate_against_forecast_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
            level_compatibility_input_contract,
            level_compatibility_contract,
            runtime_history_input_contract,
            runtime_history_contract,
            forecast_input_contract,
            forecast_contract,
        )
        position_contract.validate()
        require_text("S27 v2 order input contract status", self.status)
        if self.status != S27_V2_ORDER_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 order input contract must remain contract-only")
        self._validate_locked_maps()
        require_hash(
            "S27 v2 order source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash("S27 v2 order position input contract hash", self.position_input_contract_hash)
        require_hash("S27 v2 order position contract bundle hash", self.position_contract_bundle_hash)
        require_hash("S27 v2 order input policy hash", self.order_input_policy_hash)
        require_hash_map(
            "S27 v2 order expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_ORDER_INPUTS,
        )
        self._validate_position_authority(position_input_contract, position_contract)
        require_hash_map_matches_active_authority(
            "S27 v2 order expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(position_contract),
            REQUIRED_ORDER_INPUTS,
        )
        dependency_hash_by_label = self._validate_input_fields()
        self._validate_component_dependencies(dependency_hash_by_label)
        self._validate_invariant_dependencies(dependency_hash_by_label)
        require_hash("S27 v2 order input set hash", self.order_input_set_hash)
        require_hash("S27 v2 order input contract hash", self.order_input_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 order input contract must preserve non-authorizations")

    def _validate_locked_maps(self) -> None:
        if tuple(REQUIRED_SOURCE_KIND_BY_ORDER_INPUT) != REQUIRED_ORDER_INPUTS:
            raise CarverBlocked("S27 v2 order input source-kind map must cover locked inputs")
        if tuple(REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT) != REQUIRED_ORDER_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 order component dependency map must cover locked components")
        if tuple(REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT) != REQUIRED_ORDER_INVARIANTS:
            raise CarverBlocked("S27 v2 order invariant dependency map must cover locked invariants")

    def _active_source_contract_hash_by_input_label(
        self,
        position_contract: PositionContractBundle,
    ) -> dict[str, str]:
        position_component_contract_hash_by_family = self._position_component_contract_hash_by_family(
            position_contract,
        )
        active_hash_by_label: dict[str, str] = {}
        for input_label in REQUIRED_ORDER_INPUTS:
            source_kind = REQUIRED_SOURCE_KIND_BY_ORDER_INPUT[input_label]
            if source_kind == "POSITION_COMPONENT":
                active_hash_by_label[input_label] = position_component_contract_hash_by_family[
                    REQUIRED_POSITION_COMPONENT_BY_ORDER_INPUT[input_label]
                ]
            elif source_kind == "POSITION_LEDGER_OUTPUT":
                active_hash_by_label[input_label] = position_contract.desired_position_contract_bundle_hash
            elif source_kind in {
                "ORDER_KIND",
                "ORDER_TRANSITION_KIND",
                "ORDER_STATE_CONTEXT",
                "POLICY_INPUT",
            }:
                active_hash_by_label[input_label] = self.order_input_policy_hash
            else:
                raise CarverBlocked("S27 v2 order input source kind cannot be authority-bound")
        return active_hash_by_label

    def _validate_position_authority(
        self,
        position_input_contract: PositionInputContractBundle,
        position_contract: PositionContractBundle,
    ) -> None:
        if position_input_contract.position_input_contract_hash != self.position_input_contract_hash:
            raise CarverBlocked("S27 v2 order input must bind position input contract")
        if position_contract.desired_position_contract_bundle_hash != self.position_contract_bundle_hash:
            raise CarverBlocked("S27 v2 order input must bind position contract bundle")
        if position_input_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 order input must bind position source-input manifest")
        if (
            position_contract.source_binding.forecast_contract_bundle_hash
            != position_input_contract.forecast_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 order input must bind position forecast authority")

    def _position_component_contract_hash_by_family(
        self,
        position_contract: PositionContractBundle,
    ) -> dict[str, str]:
        position_component_contract_hash_by_family = {
            contract.component_family: contract.component_contract_hash
            for contract in position_contract.component_contracts
        }
        if tuple(position_component_contract_hash_by_family) != REQUIRED_POSITION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 order position components must match locked tuple")
        return position_component_contract_hash_by_family

    def _validate_input_fields(self) -> dict[str, str]:
        require_non_empty_tuple("S27 v2 order input field contracts", self.input_field_contracts)
        seen_inputs: set[str] = set()
        dependency_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 order input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 order input source contract hash",
                contract.input_label,
                contract.source_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            dependency_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_ORDER_INPUTS:
            raise CarverBlocked("S27 v2 order inputs must match locked input tuple")
        return dependency_hash_by_label

    def _validate_component_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 order component dependency bindings",
            self.component_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.component_dependency_bindings)
            != REQUIRED_ORDER_COMPONENT_FAMILIES
        ):
            raise CarverBlocked("S27 v2 order component dependencies must match locked components")
        seen_components: set[str] = set()
        for binding in self.component_dependency_bindings:
            binding.validate_component()
            if binding.dependency_label in seen_components:
                raise CarverBlocked("S27 v2 order component dependency bindings must be unique")
            seen_components.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_invariant_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 order invariant dependency bindings",
            self.invariant_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.invariant_dependency_bindings)
            != REQUIRED_ORDER_INVARIANTS
        ):
            raise CarverBlocked("S27 v2 order invariant dependencies must match locked invariants")
        seen_invariants: set[str] = set()
        for binding in self.invariant_dependency_bindings:
            binding.validate_invariant()
            if binding.dependency_label in seen_invariants:
                raise CarverBlocked("S27 v2 order invariant dependency bindings must be unique")
            seen_invariants.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)

    def _require_matching_dependency_hashes(
        self,
        binding: OrderDependencyBindingContract,
        dependency_hash_by_label: dict[str, str],
    ) -> None:
        require_matching_dependency_hashes(
            "S27 v2 order",
            binding.required_dependency_labels,
            binding.required_dependency_contract_hashes,
            dependency_hash_by_label,
        )

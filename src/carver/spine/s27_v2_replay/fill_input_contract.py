from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest
from .fill_contract import (
    REQUIRED_FILL_BRANCH_LABELS,
    REQUIRED_FILL_COMPONENT_FAMILIES,
    REQUIRED_FILL_INVARIANTS,
    REQUIRED_FILL_PRICE_PROVENANCE_LABELS,
)
from .forecast_contract import ForecastContractBundle
from .forecast_input_contract import ForecastInputContractBundle
from .level_compatibility_contract import LevelCompatibilityContractBundle
from .level_compatibility_input_contract import LevelCompatibilityInputContractBundle
from .order_contract import OrderContractBundle
from .order_input_contract import OrderInputContractBundle
from .parser_output_contract import ParserOutputBatchSetContract
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


S27_V2_FILL_INPUT_CONTRACT_ONLY_STATUS = "S27_V2_FILL_INPUT_CONTRACT_ONLY"
PLANNED_FILL_INPUT_STATUS = "PLANNED_FILL_INPUT_ONLY"

FILL_INPUT_NOT_APPLICABLE = "NOT_APPLICABLE"

FILL_INPUT_SOURCE_KINDS = (
    "ORDER_LEDGER_OUTPUT",
    "WORKING_ORDER_TRANSITION_OUTPUT",
    "SOURCE_ROW_PROOF",
    "FILL_PRICE_PROVENANCE",
    "FILL_BRANCH",
    "POLICY_INPUT",
)

REQUIRED_FILL_INPUTS = (
    "FILL_ORDER_PLAN_HASH_INPUT",
    "FILL_LIMIT_ORDER_HASH_INPUT",
    "FILL_MARKET_ORDER_HASH_INPUT",
    "FILL_WORKING_ORDER_TRANSITION_HASH_INPUT",
    "FILL_NEXT_COMPLETED_HOURLY_ROW_HASH_INPUT",
    "FILL_LIMIT_PRICE_PROVENANCE_INPUT",
    "FILL_MARKET_PRICE_PROVENANCE_INPUT",
    "FILL_LIMIT_BRANCH_INPUT",
    "FILL_MARKET_BRANCH_INPUT",
    "FILL_QUANTITY_AND_SIDE_BINDING_INPUT",
    "FILL_ONE_HOUR_LAG_POLICY_INPUT",
    "FILL_SESSION_GAP_POLICY_INPUT",
)

REQUIRED_SOURCE_KIND_BY_FILL_INPUT = {
    "FILL_ORDER_PLAN_HASH_INPUT": "ORDER_LEDGER_OUTPUT",
    "FILL_LIMIT_ORDER_HASH_INPUT": "ORDER_LEDGER_OUTPUT",
    "FILL_MARKET_ORDER_HASH_INPUT": "ORDER_LEDGER_OUTPUT",
    "FILL_WORKING_ORDER_TRANSITION_HASH_INPUT": "WORKING_ORDER_TRANSITION_OUTPUT",
    "FILL_NEXT_COMPLETED_HOURLY_ROW_HASH_INPUT": "SOURCE_ROW_PROOF",
    "FILL_LIMIT_PRICE_PROVENANCE_INPUT": "FILL_PRICE_PROVENANCE",
    "FILL_MARKET_PRICE_PROVENANCE_INPUT": "FILL_PRICE_PROVENANCE",
    "FILL_LIMIT_BRANCH_INPUT": "FILL_BRANCH",
    "FILL_MARKET_BRANCH_INPUT": "FILL_BRANCH",
    "FILL_QUANTITY_AND_SIDE_BINDING_INPUT": "ORDER_LEDGER_OUTPUT",
    "FILL_ONE_HOUR_LAG_POLICY_INPUT": "POLICY_INPUT",
    "FILL_SESSION_GAP_POLICY_INPUT": "POLICY_INPUT",
}

REQUIRED_ORDER_LEDGER_OUTPUT_BY_FILL_INPUT = {
    "FILL_ORDER_PLAN_HASH_INPUT": "ORDER_PLAN_HASH",
    "FILL_LIMIT_ORDER_HASH_INPUT": "LIMIT_ORDER_HASH",
    "FILL_MARKET_ORDER_HASH_INPUT": "MARKET_ORDER_HASH",
    "FILL_QUANTITY_AND_SIDE_BINDING_INPUT": "ORDER_QUANTITY_AND_SIDE",
}

REQUIRED_WORKING_ORDER_TRANSITION_OUTPUT_BY_FILL_INPUT = {
    "FILL_WORKING_ORDER_TRANSITION_HASH_INPUT": "TRANSITION_HASH",
}

REQUIRED_SOURCE_ROW_PROOF_BY_FILL_INPUT = {
    "FILL_NEXT_COMPLETED_HOURLY_ROW_HASH_INPUT": "NEXT_COMPLETED_HOURLY_FILL_ROW_HASH",
}

REQUIRED_FILL_PRICE_PROVENANCE_BY_FILL_INPUT = {
    "FILL_LIMIT_PRICE_PROVENANCE_INPUT": "LIMIT_ORDER_PRICE_FROM_FILLED_ORDER",
    "FILL_MARKET_PRICE_PROVENANCE_INPUT": "MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE",
}

REQUIRED_FILL_BRANCH_BY_FILL_INPUT = {
    "FILL_LIMIT_BRANCH_INPUT": "LIMIT_FILL",
    "FILL_MARKET_BRANCH_INPUT": "MARKET_FILL",
}

REQUIRED_POLICY_LABEL_BY_FILL_INPUT = {
    "FILL_ONE_HOUR_LAG_POLICY_INPUT": "ONE_HOUR_LAG_POLICY",
    "FILL_SESSION_GAP_POLICY_INPUT": "SESSION_GAP_POLICY",
}

FILL_SOURCE_ROW_MANIFEST_FIELD = "HOURLY_FILL_ROW_HASH"

REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT = {
    "ORDER_PLAN_REFERENCE": (
        "FILL_ORDER_PLAN_HASH_INPUT",
        "FILL_LIMIT_ORDER_HASH_INPUT",
        "FILL_MARKET_ORDER_HASH_INPUT",
    ),
    "WORKING_ORDER_TRANSITION_REFERENCE": (
        "FILL_WORKING_ORDER_TRANSITION_HASH_INPUT",
        "FILL_ONE_HOUR_LAG_POLICY_INPUT",
        "FILL_SESSION_GAP_POLICY_INPUT",
    ),
    "NEXT_COMPLETED_HOURLY_FILL_ROW": (
        "FILL_WORKING_ORDER_TRANSITION_HASH_INPUT",
        "FILL_NEXT_COMPLETED_HOURLY_ROW_HASH_INPUT",
    ),
    "LIMIT_FILL_PRICE_PROVENANCE": (
        "FILL_LIMIT_ORDER_HASH_INPUT",
        "FILL_LIMIT_PRICE_PROVENANCE_INPUT",
        "NEXT_COMPLETED_HOURLY_FILL_ROW",
    ),
    "MARKET_FILL_PRICE_PROVENANCE": (
        "FILL_MARKET_ORDER_HASH_INPUT",
        "FILL_MARKET_PRICE_PROVENANCE_INPUT",
        "NEXT_COMPLETED_HOURLY_FILL_ROW",
    ),
    "FILL_QUANTITY_AND_SIDE_BINDING": (
        "FILL_QUANTITY_AND_SIDE_BINDING_INPUT",
        "ORDER_PLAN_REFERENCE",
    ),
}

REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT = {
    "ORDER_CONTRACT_BUNDLE_HASH_BINDING": (
        "ORDER_PLAN_REFERENCE",
    ),
    "TRANSITION_HASH_BINDING": (
        "WORKING_ORDER_TRANSITION_REFERENCE",
    ),
    "EXACT_NEXT_COMPLETED_HOURLY_ROW_BINDING": (
        "NEXT_COMPLETED_HOURLY_FILL_ROW",
    ),
    "FILL_TIMESTAMP_IDENTITY_BINDING": (
        "FILL_NEXT_COMPLETED_HOURLY_ROW_HASH_INPUT",
        "WORKING_ORDER_TRANSITION_REFERENCE",
    ),
    "LIMIT_FILL_PRICE_EQUALS_SUBMITTED_LIMIT": (
        "FILL_LIMIT_BRANCH_INPUT",
        "LIMIT_FILL_PRICE_PROVENANCE",
    ),
    "MARKET_FILL_PRICE_FROM_NEXT_COMPLETED_CLOSE": (
        "FILL_MARKET_BRANCH_INPUT",
        "MARKET_FILL_PRICE_PROVENANCE",
        "NEXT_COMPLETED_HOURLY_FILL_ROW",
    ),
    "NO_COST_ACCOUNTING_IN_FILL_CONTRACT": (
        "FILL_QUANTITY_AND_SIDE_BINDING",
        "LIMIT_FILL_PRICE_PROVENANCE",
        "MARKET_FILL_PRICE_PROVENANCE",
    ),
}


@dataclass(frozen=True)
class FillInputFieldContract:
    input_label: str
    input_status: str
    source_kind: str
    order_ledger_output_label: str
    working_order_transition_output_label: str
    source_row_proof_label: str
    fill_price_provenance_label: str
    fill_branch_label: str
    source_policy_label: str
    source_contract_hash: str
    fill_input_policy_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 fill input label", self.input_label)
        if self.input_label not in REQUIRED_FILL_INPUTS:
            raise CarverBlocked("S27 v2 fill input label is not locked")
        require_text("S27 v2 fill input status", self.input_status)
        if self.input_status != PLANNED_FILL_INPUT_STATUS:
            raise CarverBlocked("S27 v2 fill input must remain planned-only")
        require_text("S27 v2 fill input source kind", self.source_kind)
        if self.source_kind not in FILL_INPUT_SOURCE_KINDS:
            raise CarverBlocked("S27 v2 fill input source kind is not locked")
        if self.source_kind != REQUIRED_SOURCE_KIND_BY_FILL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 fill input must use the locked source kind")
        self._validate_source_target()
        require_hash("S27 v2 fill input source contract hash", self.source_contract_hash)
        require_hash("S27 v2 fill input policy hash", self.fill_input_policy_hash)
        require_hash("S27 v2 fill input field contract hash", self.input_field_contract_hash)

    def _validate_source_target(self) -> None:
        if self.source_kind == "ORDER_LEDGER_OUTPUT":
            self._validate_order_ledger_output_target()
        elif self.source_kind == "WORKING_ORDER_TRANSITION_OUTPUT":
            self._validate_working_order_transition_output_target()
        elif self.source_kind == "SOURCE_ROW_PROOF":
            self._validate_source_row_proof_target()
        elif self.source_kind == "FILL_PRICE_PROVENANCE":
            self._validate_fill_price_provenance_target()
        elif self.source_kind == "FILL_BRANCH":
            self._validate_fill_branch_target()
        elif self.source_kind == "POLICY_INPUT":
            self._validate_policy_input_target()

    def _require_not_applicable(self, name: str, value: str) -> None:
        require_text(name, value)
        if value != FILL_INPUT_NOT_APPLICABLE:
            raise CarverBlocked(f"{name} must be not applicable")

    def _validate_order_ledger_output_target(self) -> None:
        require_text("S27 v2 fill order ledger output", self.order_ledger_output_label)
        if self.order_ledger_output_label != REQUIRED_ORDER_LEDGER_OUTPUT_BY_FILL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 fill input must use the locked order ledger output")
        self._require_not_applicable(
            "S27 v2 fill working-order transition output",
            self.working_order_transition_output_label,
        )
        self._require_not_applicable("S27 v2 fill source row proof label", self.source_row_proof_label)
        self._require_not_applicable(
            "S27 v2 fill price provenance label",
            self.fill_price_provenance_label,
        )
        self._require_not_applicable("S27 v2 fill branch label", self.fill_branch_label)
        self._require_not_applicable("S27 v2 fill source policy label", self.source_policy_label)

    def _validate_working_order_transition_output_target(self) -> None:
        require_text(
            "S27 v2 fill working-order transition output",
            self.working_order_transition_output_label,
        )
        if (
            self.working_order_transition_output_label
            != REQUIRED_WORKING_ORDER_TRANSITION_OUTPUT_BY_FILL_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 fill input must use the locked transition output")
        self._require_not_applicable("S27 v2 fill order ledger output", self.order_ledger_output_label)
        self._require_not_applicable("S27 v2 fill source row proof label", self.source_row_proof_label)
        self._require_not_applicable(
            "S27 v2 fill price provenance label",
            self.fill_price_provenance_label,
        )
        self._require_not_applicable("S27 v2 fill branch label", self.fill_branch_label)
        self._require_not_applicable("S27 v2 fill source policy label", self.source_policy_label)

    def _validate_source_row_proof_target(self) -> None:
        require_text("S27 v2 fill source row proof label", self.source_row_proof_label)
        if self.source_row_proof_label != REQUIRED_SOURCE_ROW_PROOF_BY_FILL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 fill input must use the locked source row proof")
        self._require_not_applicable("S27 v2 fill order ledger output", self.order_ledger_output_label)
        self._require_not_applicable(
            "S27 v2 fill working-order transition output",
            self.working_order_transition_output_label,
        )
        self._require_not_applicable(
            "S27 v2 fill price provenance label",
            self.fill_price_provenance_label,
        )
        self._require_not_applicable("S27 v2 fill branch label", self.fill_branch_label)
        self._require_not_applicable("S27 v2 fill source policy label", self.source_policy_label)

    def _validate_fill_price_provenance_target(self) -> None:
        require_text("S27 v2 fill price provenance label", self.fill_price_provenance_label)
        if self.fill_price_provenance_label not in REQUIRED_FILL_PRICE_PROVENANCE_LABELS:
            raise CarverBlocked("S27 v2 fill price provenance label is not locked")
        if self.fill_price_provenance_label != REQUIRED_FILL_PRICE_PROVENANCE_BY_FILL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 fill input must use the locked price provenance")
        self._require_not_applicable("S27 v2 fill order ledger output", self.order_ledger_output_label)
        self._require_not_applicable(
            "S27 v2 fill working-order transition output",
            self.working_order_transition_output_label,
        )
        self._require_not_applicable("S27 v2 fill source row proof label", self.source_row_proof_label)
        self._require_not_applicable("S27 v2 fill branch label", self.fill_branch_label)
        self._require_not_applicable("S27 v2 fill source policy label", self.source_policy_label)

    def _validate_fill_branch_target(self) -> None:
        require_text("S27 v2 fill branch label", self.fill_branch_label)
        if self.fill_branch_label not in REQUIRED_FILL_BRANCH_LABELS:
            raise CarverBlocked("S27 v2 fill branch label is not locked")
        if self.fill_branch_label != REQUIRED_FILL_BRANCH_BY_FILL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 fill input must use the locked fill branch")
        self._require_not_applicable("S27 v2 fill order ledger output", self.order_ledger_output_label)
        self._require_not_applicable(
            "S27 v2 fill working-order transition output",
            self.working_order_transition_output_label,
        )
        self._require_not_applicable("S27 v2 fill source row proof label", self.source_row_proof_label)
        self._require_not_applicable(
            "S27 v2 fill price provenance label",
            self.fill_price_provenance_label,
        )
        self._require_not_applicable("S27 v2 fill source policy label", self.source_policy_label)

    def _validate_policy_input_target(self) -> None:
        require_text("S27 v2 fill source policy label", self.source_policy_label)
        if self.source_policy_label != REQUIRED_POLICY_LABEL_BY_FILL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 fill input must use the locked source policy")
        self._require_not_applicable("S27 v2 fill order ledger output", self.order_ledger_output_label)
        self._require_not_applicable(
            "S27 v2 fill working-order transition output",
            self.working_order_transition_output_label,
        )
        self._require_not_applicable("S27 v2 fill source row proof label", self.source_row_proof_label)
        self._require_not_applicable(
            "S27 v2 fill price provenance label",
            self.fill_price_provenance_label,
        )
        self._require_not_applicable("S27 v2 fill branch label", self.fill_branch_label)


@dataclass(frozen=True)
class FillDependencyBindingContract:
    dependency_label: str
    required_dependency_labels: tuple[str, ...]
    required_dependency_contract_hashes: tuple[str, ...]
    dependency_binding_policy_hash: str
    dependency_binding_contract_hash: str

    def validate_component(self) -> None:
        require_text("S27 v2 fill component dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_FILL_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 fill component dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT[self.dependency_label])

    def validate_invariant(self) -> None:
        require_text("S27 v2 fill invariant dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_FILL_INVARIANTS:
            raise CarverBlocked("S27 v2 fill invariant dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT[self.dependency_label])

    def _validate_required_dependencies(self, locked_labels: tuple[str, ...]) -> None:
        require_non_empty_tuple("S27 v2 fill required dependency labels", self.required_dependency_labels)
        if self.required_dependency_labels != locked_labels:
            raise CarverBlocked("S27 v2 fill dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 fill required dependency contract hashes",
            self.required_dependency_contract_hashes,
        )
        if len(self.required_dependency_contract_hashes) != len(self.required_dependency_labels):
            raise CarverBlocked("S27 v2 fill dependency hashes must match labels")
        for dependency_hash in self.required_dependency_contract_hashes:
            require_hash("S27 v2 fill dependency contract hash", dependency_hash)
        require_hash("S27 v2 fill dependency binding policy hash", self.dependency_binding_policy_hash)
        require_hash("S27 v2 fill dependency binding contract hash", self.dependency_binding_contract_hash)


@dataclass(frozen=True)
class FillInputContractBundle:
    status: str
    source_input_manifest_contract_hash: str
    order_input_contract_hash: str
    order_contract_bundle_hash: str
    fill_input_policy_hash: str
    input_field_contracts: tuple[FillInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    component_dependency_bindings: tuple[FillDependencyBindingContract, ...]
    invariant_dependency_bindings: tuple[FillDependencyBindingContract, ...]
    fill_input_set_hash: str
    fill_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 fill input requires order and source-row authority"
        )

    def validate_against_order_authority(
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
    ) -> None:
        source_input_manifest_contract.validate_against_active_trust_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )
        order_input_contract.validate_against_position_authority(
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
            position_input_contract,
            position_contract,
        )
        order_contract.validate()
        require_text("S27 v2 fill input contract status", self.status)
        if self.status != S27_V2_FILL_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 fill input contract must remain contract-only")
        self._validate_locked_maps()
        require_hash(
            "S27 v2 fill source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash("S27 v2 fill order input contract hash", self.order_input_contract_hash)
        require_hash("S27 v2 fill order contract bundle hash", self.order_contract_bundle_hash)
        require_hash("S27 v2 fill input policy hash", self.fill_input_policy_hash)
        require_hash_map(
            "S27 v2 fill expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_FILL_INPUTS,
        )
        self._validate_order_authority(
            source_input_manifest_contract,
            order_input_contract,
            order_contract,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 fill expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(
                source_input_manifest_contract,
                order_contract,
            ),
            REQUIRED_FILL_INPUTS,
        )
        dependency_hash_by_label = self._validate_input_fields()
        self._validate_component_dependencies(dependency_hash_by_label)
        self._validate_invariant_dependencies(dependency_hash_by_label)
        require_hash("S27 v2 fill input set hash", self.fill_input_set_hash)
        require_hash("S27 v2 fill input contract hash", self.fill_input_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 fill input contract must preserve non-authorizations")

    def _validate_locked_maps(self) -> None:
        if tuple(REQUIRED_SOURCE_KIND_BY_FILL_INPUT) != REQUIRED_FILL_INPUTS:
            raise CarverBlocked("S27 v2 fill input source-kind map must cover locked inputs")
        if tuple(REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT) != REQUIRED_FILL_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 fill component dependency map must cover locked components")
        if tuple(REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT) != REQUIRED_FILL_INVARIANTS:
            raise CarverBlocked("S27 v2 fill invariant dependency map must cover locked invariants")

    def _active_source_contract_hash_by_input_label(
        self,
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
                active_hash_by_label[input_label] = self.fill_input_policy_hash
            else:
                raise CarverBlocked("S27 v2 fill input source kind cannot be authority-bound")
        return active_hash_by_label

    def _validate_order_authority(
        self,
        source_input_manifest_contract: SourceInputManifestContractBundle,
        order_input_contract: OrderInputContractBundle,
        order_contract: OrderContractBundle,
    ) -> None:
        if source_input_manifest_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 fill input must bind source-input manifest contract")
        if order_input_contract.order_input_contract_hash != self.order_input_contract_hash:
            raise CarverBlocked("S27 v2 fill input must bind order input contract")
        if order_contract.order_contract_bundle_hash != self.order_contract_bundle_hash:
            raise CarverBlocked("S27 v2 fill input must bind order contract bundle")
        if order_input_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 fill input must bind order source-input manifest")
        if (
            order_contract.source_binding.position_contract_bundle_hash
            != order_input_contract.position_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 fill input must bind order position authority")
        if order_contract.source_binding.source_input_manifest_hash != source_input_manifest_contract.source_input_manifest_hash:
            raise CarverBlocked("S27 v2 fill input must bind order source manifest hash")

    def _validate_input_fields(self) -> dict[str, str]:
        require_non_empty_tuple("S27 v2 fill input field contracts", self.input_field_contracts)
        seen_inputs: set[str] = set()
        dependency_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 fill input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 fill input source contract hash",
                contract.input_label,
                contract.source_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            dependency_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_FILL_INPUTS:
            raise CarverBlocked("S27 v2 fill inputs must match locked input tuple")
        return dependency_hash_by_label

    def _validate_component_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 fill component dependency bindings",
            self.component_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.component_dependency_bindings)
            != REQUIRED_FILL_COMPONENT_FAMILIES
        ):
            raise CarverBlocked("S27 v2 fill component dependencies must match locked components")
        seen_components: set[str] = set()
        for binding in self.component_dependency_bindings:
            binding.validate_component()
            if binding.dependency_label in seen_components:
                raise CarverBlocked("S27 v2 fill component dependency bindings must be unique")
            seen_components.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_invariant_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 fill invariant dependency bindings",
            self.invariant_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.invariant_dependency_bindings)
            != REQUIRED_FILL_INVARIANTS
        ):
            raise CarverBlocked("S27 v2 fill invariant dependencies must match locked invariants")
        seen_invariants: set[str] = set()
        for binding in self.invariant_dependency_bindings:
            binding.validate_invariant()
            if binding.dependency_label in seen_invariants:
                raise CarverBlocked("S27 v2 fill invariant dependency bindings must be unique")
            seen_invariants.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)

    def _require_matching_dependency_hashes(
        self,
        binding: FillDependencyBindingContract,
        dependency_hash_by_label: dict[str, str],
    ) -> None:
        require_matching_dependency_hashes(
            "S27 v2 fill",
            binding.required_dependency_labels,
            binding.required_dependency_contract_hashes,
            dependency_hash_by_label,
        )

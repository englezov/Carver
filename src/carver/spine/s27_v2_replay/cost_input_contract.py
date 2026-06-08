from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest, require_evidence_manifest_matches_trust_root
from .cost_contract import (
    REQUIRED_COST_BRANCH_LABELS,
    REQUIRED_COST_COMPONENT_FAMILIES,
    REQUIRED_COST_INVARIANTS,
    REQUIRED_SPREAD_SPACE_LABELS,
)
from .fill_contract import FillContractBundle
from .fill_input_contract import FillInputContractBundle
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


S27_V2_COST_INPUT_CONTRACT_ONLY_STATUS = "S27_V2_COST_INPUT_CONTRACT_ONLY"
PLANNED_COST_INPUT_STATUS = "PLANNED_COST_INPUT_ONLY"

COST_INPUT_NOT_APPLICABLE = "NOT_APPLICABLE"

COST_INPUT_SOURCE_KINDS = (
    "FILL_LEDGER_OUTPUT",
    "COST_BRANCH",
    "SPREAD_SPACE",
    "POLICY_INPUT",
    "MULTIPLIER_PROOF_INPUT",
    "CURRENCY_PROOF_INPUT",
)

REQUIRED_COST_INPUTS = (
    "COST_FILL_LEDGER_HASH_INPUT",
    "COST_FILL_ORDER_KIND_INPUT",
    "COST_FILL_QUANTITY_INPUT",
    "COST_LIMIT_COMMISSION_ONLY_BRANCH_INPUT",
    "COST_MARKET_COMMISSION_PLUS_SPREAD_BRANCH_INPUT",
    "COST_COMMISSION_POLICY_INPUT",
    "COST_SPREAD_POLICY_INPUT",
    "COST_PRICE_SPACE_INPUT",
    "COST_CURRENCY_SPACE_INPUT",
    "COST_CONTRACT_MULTIPLIER_POLICY_INPUT",
    "COST_CURRENCY_CONVERSION_POLICY_INPUT",
    "COST_DEFLATION_POLICY_INPUT",
    "COST_CALCULATION_POLICY_INPUT",
)

REQUIRED_SOURCE_KIND_BY_COST_INPUT = {
    "COST_FILL_LEDGER_HASH_INPUT": "FILL_LEDGER_OUTPUT",
    "COST_FILL_ORDER_KIND_INPUT": "FILL_LEDGER_OUTPUT",
    "COST_FILL_QUANTITY_INPUT": "FILL_LEDGER_OUTPUT",
    "COST_LIMIT_COMMISSION_ONLY_BRANCH_INPUT": "COST_BRANCH",
    "COST_MARKET_COMMISSION_PLUS_SPREAD_BRANCH_INPUT": "COST_BRANCH",
    "COST_COMMISSION_POLICY_INPUT": "POLICY_INPUT",
    "COST_SPREAD_POLICY_INPUT": "POLICY_INPUT",
    "COST_PRICE_SPACE_INPUT": "SPREAD_SPACE",
    "COST_CURRENCY_SPACE_INPUT": "SPREAD_SPACE",
    "COST_CONTRACT_MULTIPLIER_POLICY_INPUT": "MULTIPLIER_PROOF_INPUT",
    "COST_CURRENCY_CONVERSION_POLICY_INPUT": "CURRENCY_PROOF_INPUT",
    "COST_DEFLATION_POLICY_INPUT": "POLICY_INPUT",
    "COST_CALCULATION_POLICY_INPUT": "POLICY_INPUT",
}

REQUIRED_FILL_LEDGER_OUTPUT_BY_COST_INPUT = {
    "COST_FILL_LEDGER_HASH_INPUT": "FILL_LEDGER_ROW_HASH",
    "COST_FILL_ORDER_KIND_INPUT": "FILL_ORDER_KIND",
    "COST_FILL_QUANTITY_INPUT": "FILL_QUANTITY",
}

REQUIRED_COST_BRANCH_BY_COST_INPUT = {
    "COST_LIMIT_COMMISSION_ONLY_BRANCH_INPUT": "LIMIT_COMMISSION_ONLY",
    "COST_MARKET_COMMISSION_PLUS_SPREAD_BRANCH_INPUT": "MARKET_COMMISSION_PLUS_SPREAD",
}

REQUIRED_SPREAD_SPACE_BY_COST_INPUT = {
    "COST_PRICE_SPACE_INPUT": "PRICE_SPACE",
    "COST_CURRENCY_SPACE_INPUT": "CURRENCY_SPACE",
}

REQUIRED_POLICY_LABEL_BY_COST_INPUT = {
    "COST_COMMISSION_POLICY_INPUT": "COMMISSION_POLICY",
    "COST_SPREAD_POLICY_INPUT": "SPREAD_POLICY",
    "COST_DEFLATION_POLICY_INPUT": "DEFLATION_POLICY",
    "COST_CALCULATION_POLICY_INPUT": "COST_CALCULATION_POLICY",
}

REQUIRED_MULTIPLIER_PROOF_BY_COST_INPUT = {
    "COST_CONTRACT_MULTIPLIER_POLICY_INPUT": "CONTRACT_MULTIPLIER_VALUE_AND_SOURCE_PROOF",
}

REQUIRED_CURRENCY_PROOF_BY_COST_INPUT = {
    "COST_CURRENCY_CONVERSION_POLICY_INPUT": "CURRENCY_CONVERSION_VALUE_AND_SOURCE_PROOF",
}

REQUIRED_COST_DEPENDENCIES_BY_COMPONENT = {
    "FILL_LEDGER_REFERENCE": (
        "COST_FILL_LEDGER_HASH_INPUT",
        "COST_FILL_ORDER_KIND_INPUT",
        "COST_FILL_QUANTITY_INPUT",
    ),
    "COMMISSION_POLICY": (
        "COST_COMMISSION_POLICY_INPUT",
        "COST_FILL_QUANTITY_INPUT",
    ),
    "LIMIT_FILL_COMMISSION_ONLY_BRANCH": (
        "COST_LIMIT_COMMISSION_ONLY_BRANCH_INPUT",
        "COMMISSION_POLICY",
        "FILL_LEDGER_REFERENCE",
    ),
    "MARKET_FILL_SPREAD_COST_BRANCH": (
        "COST_MARKET_COMMISSION_PLUS_SPREAD_BRANCH_INPUT",
        "COMMISSION_POLICY",
        "COST_SPREAD_POLICY_INPUT",
        "SPREAD_SPACE_POLICY",
        "FILL_LEDGER_REFERENCE",
    ),
    "SPREAD_SPACE_POLICY": (
        "COST_PRICE_SPACE_INPUT",
        "COST_CURRENCY_SPACE_INPUT",
    ),
    "CONTRACT_MULTIPLIER_CURRENCY_POLICY": (
        "COST_CONTRACT_MULTIPLIER_POLICY_INPUT",
        "COST_CURRENCY_CONVERSION_POLICY_INPUT",
        "COST_DEFLATION_POLICY_INPUT",
    ),
    "TOTAL_COST_SUMMARY": (
        "LIMIT_FILL_COMMISSION_ONLY_BRANCH",
        "MARKET_FILL_SPREAD_COST_BRANCH",
        "COST_CALCULATION_POLICY_INPUT",
    ),
}

REQUIRED_COST_DEPENDENCIES_BY_INVARIANT = {
    "FILL_CONTRACT_BUNDLE_HASH_BINDING": (
        "FILL_LEDGER_REFERENCE",
    ),
    "COMMISSION_PER_CONTRACT_TIMES_QUANTITY_BINDING": (
        "COMMISSION_POLICY",
        "COST_FILL_QUANTITY_INPUT",
    ),
    "LIMIT_FILL_ZERO_SPREAD_BINDING": (
        "LIMIT_FILL_COMMISSION_ONLY_BRANCH",
    ),
    "MARKET_FILL_POSITIVE_SPREAD_BINDING": (
        "MARKET_FILL_SPREAD_COST_BRANCH",
    ),
    "PRICE_SPACE_SPREAD_MULTIPLIER_BINDING": (
        "COST_PRICE_SPACE_INPUT",
        "COST_CONTRACT_MULTIPLIER_POLICY_INPUT",
        "MARKET_FILL_SPREAD_COST_BRANCH",
    ),
    "CURRENCY_SPACE_SPREAD_DIRECT_AMOUNT_BINDING": (
        "COST_CURRENCY_SPACE_INPUT",
        "MARKET_FILL_SPREAD_COST_BRANCH",
    ),
    "TOTAL_COST_EQUALS_COMMISSION_PLUS_SPREAD_BINDING": (
        "TOTAL_COST_SUMMARY",
        "COMMISSION_POLICY",
        "MARKET_FILL_SPREAD_COST_BRANCH",
    ),
    "NO_PNL_ACCOUNTING_IN_COST_CONTRACT": (
        "TOTAL_COST_SUMMARY",
    ),
}


@dataclass(frozen=True)
class CostInputFieldContract:
    input_label: str
    input_status: str
    source_kind: str
    fill_ledger_output_label: str
    cost_branch_label: str
    spread_space_label: str
    source_policy_label: str
    multiplier_proof_label: str
    currency_proof_label: str
    source_contract_hash: str
    cost_input_policy_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 cost input label", self.input_label)
        if self.input_label not in REQUIRED_COST_INPUTS:
            raise CarverBlocked("S27 v2 cost input label is not locked")
        require_text("S27 v2 cost input status", self.input_status)
        if self.input_status != PLANNED_COST_INPUT_STATUS:
            raise CarverBlocked("S27 v2 cost input must remain planned-only")
        require_text("S27 v2 cost input source kind", self.source_kind)
        if self.source_kind not in COST_INPUT_SOURCE_KINDS:
            raise CarverBlocked("S27 v2 cost input source kind is not locked")
        if self.source_kind != REQUIRED_SOURCE_KIND_BY_COST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 cost input must use the locked source kind")
        self._validate_source_target()
        require_hash("S27 v2 cost input source contract hash", self.source_contract_hash)
        require_hash("S27 v2 cost input policy hash", self.cost_input_policy_hash)
        require_hash("S27 v2 cost input field contract hash", self.input_field_contract_hash)

    def _validate_source_target(self) -> None:
        if self.source_kind == "FILL_LEDGER_OUTPUT":
            self._validate_fill_ledger_output_target()
        elif self.source_kind == "COST_BRANCH":
            self._validate_cost_branch_target()
        elif self.source_kind == "SPREAD_SPACE":
            self._validate_spread_space_target()
        elif self.source_kind == "POLICY_INPUT":
            self._validate_policy_input_target()
        elif self.source_kind == "MULTIPLIER_PROOF_INPUT":
            self._validate_multiplier_proof_target()
        elif self.source_kind == "CURRENCY_PROOF_INPUT":
            self._validate_currency_proof_target()

    def _require_not_applicable(self, name: str, value: str) -> None:
        require_text(name, value)
        if value != COST_INPUT_NOT_APPLICABLE:
            raise CarverBlocked(f"{name} must be not applicable")

    def _validate_fill_ledger_output_target(self) -> None:
        require_text("S27 v2 cost fill ledger output", self.fill_ledger_output_label)
        if self.fill_ledger_output_label != REQUIRED_FILL_LEDGER_OUTPUT_BY_COST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 cost input must use the locked fill ledger output")
        self._require_not_applicable("S27 v2 cost branch label", self.cost_branch_label)
        self._require_not_applicable("S27 v2 cost spread-space label", self.spread_space_label)
        self._require_not_applicable("S27 v2 cost source policy label", self.source_policy_label)
        self._require_not_applicable("S27 v2 cost multiplier proof label", self.multiplier_proof_label)
        self._require_not_applicable("S27 v2 cost currency proof label", self.currency_proof_label)

    def _validate_cost_branch_target(self) -> None:
        require_text("S27 v2 cost branch label", self.cost_branch_label)
        if self.cost_branch_label not in REQUIRED_COST_BRANCH_LABELS:
            raise CarverBlocked("S27 v2 cost branch label is not locked")
        if self.cost_branch_label != REQUIRED_COST_BRANCH_BY_COST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 cost input must use the locked cost branch")
        self._require_not_applicable("S27 v2 cost fill ledger output", self.fill_ledger_output_label)
        self._require_not_applicable("S27 v2 cost spread-space label", self.spread_space_label)
        self._require_not_applicable("S27 v2 cost source policy label", self.source_policy_label)
        self._require_not_applicable("S27 v2 cost multiplier proof label", self.multiplier_proof_label)
        self._require_not_applicable("S27 v2 cost currency proof label", self.currency_proof_label)

    def _validate_spread_space_target(self) -> None:
        require_text("S27 v2 cost spread-space label", self.spread_space_label)
        if self.spread_space_label not in REQUIRED_SPREAD_SPACE_LABELS:
            raise CarverBlocked("S27 v2 cost spread-space label is not locked")
        if self.spread_space_label != REQUIRED_SPREAD_SPACE_BY_COST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 cost input must use the locked spread space")
        self._require_not_applicable("S27 v2 cost fill ledger output", self.fill_ledger_output_label)
        self._require_not_applicable("S27 v2 cost branch label", self.cost_branch_label)
        self._require_not_applicable("S27 v2 cost source policy label", self.source_policy_label)
        self._require_not_applicable("S27 v2 cost multiplier proof label", self.multiplier_proof_label)
        self._require_not_applicable("S27 v2 cost currency proof label", self.currency_proof_label)

    def _validate_policy_input_target(self) -> None:
        require_text("S27 v2 cost source policy label", self.source_policy_label)
        if self.source_policy_label != REQUIRED_POLICY_LABEL_BY_COST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 cost input must use the locked source policy")
        self._require_not_applicable("S27 v2 cost fill ledger output", self.fill_ledger_output_label)
        self._require_not_applicable("S27 v2 cost branch label", self.cost_branch_label)
        self._require_not_applicable("S27 v2 cost spread-space label", self.spread_space_label)
        self._require_not_applicable("S27 v2 cost multiplier proof label", self.multiplier_proof_label)
        self._require_not_applicable("S27 v2 cost currency proof label", self.currency_proof_label)

    def _validate_multiplier_proof_target(self) -> None:
        require_text("S27 v2 cost multiplier proof label", self.multiplier_proof_label)
        if self.multiplier_proof_label != REQUIRED_MULTIPLIER_PROOF_BY_COST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 cost input must use the locked multiplier proof")
        self._require_not_applicable("S27 v2 cost fill ledger output", self.fill_ledger_output_label)
        self._require_not_applicable("S27 v2 cost branch label", self.cost_branch_label)
        self._require_not_applicable("S27 v2 cost spread-space label", self.spread_space_label)
        self._require_not_applicable("S27 v2 cost source policy label", self.source_policy_label)
        self._require_not_applicable("S27 v2 cost currency proof label", self.currency_proof_label)

    def _validate_currency_proof_target(self) -> None:
        require_text("S27 v2 cost currency proof label", self.currency_proof_label)
        if self.currency_proof_label != REQUIRED_CURRENCY_PROOF_BY_COST_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 cost input must use the locked currency proof")
        self._require_not_applicable("S27 v2 cost fill ledger output", self.fill_ledger_output_label)
        self._require_not_applicable("S27 v2 cost branch label", self.cost_branch_label)
        self._require_not_applicable("S27 v2 cost spread-space label", self.spread_space_label)
        self._require_not_applicable("S27 v2 cost source policy label", self.source_policy_label)
        self._require_not_applicable("S27 v2 cost multiplier proof label", self.multiplier_proof_label)


@dataclass(frozen=True)
class CostDependencyBindingContract:
    dependency_label: str
    required_dependency_labels: tuple[str, ...]
    required_dependency_contract_hashes: tuple[str, ...]
    dependency_binding_policy_hash: str
    dependency_binding_contract_hash: str

    def validate_component(self) -> None:
        require_text("S27 v2 cost component dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_COST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 cost component dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_COST_DEPENDENCIES_BY_COMPONENT[self.dependency_label])

    def validate_invariant(self) -> None:
        require_text("S27 v2 cost invariant dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_COST_INVARIANTS:
            raise CarverBlocked("S27 v2 cost invariant dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_COST_DEPENDENCIES_BY_INVARIANT[self.dependency_label])

    def _validate_required_dependencies(self, locked_labels: tuple[str, ...]) -> None:
        require_non_empty_tuple("S27 v2 cost required dependency labels", self.required_dependency_labels)
        if self.required_dependency_labels != locked_labels:
            raise CarverBlocked("S27 v2 cost dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 cost required dependency contract hashes",
            self.required_dependency_contract_hashes,
        )
        if len(self.required_dependency_contract_hashes) != len(self.required_dependency_labels):
            raise CarverBlocked("S27 v2 cost dependency hashes must match labels")
        for dependency_hash in self.required_dependency_contract_hashes:
            require_hash("S27 v2 cost dependency contract hash", dependency_hash)
        require_hash("S27 v2 cost dependency binding policy hash", self.dependency_binding_policy_hash)
        require_hash("S27 v2 cost dependency binding contract hash", self.dependency_binding_contract_hash)


@dataclass(frozen=True)
class CostInputContractBundle:
    status: str
    source_input_manifest_contract_hash: str
    fill_input_contract_hash: str
    fill_contract_bundle_hash: str
    cost_input_policy_hash: str
    input_field_contracts: tuple[CostInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    component_dependency_bindings: tuple[CostDependencyBindingContract, ...]
    invariant_dependency_bindings: tuple[CostDependencyBindingContract, ...]
    cost_input_set_hash: str
    cost_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 cost input requires fill authority"
        )

    def validate_against_fill_authority(
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
    ) -> None:
        fill_input_contract.validate_against_order_authority(
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
        )
        fill_contract.validate()
        require_evidence_manifest_matches_trust_root(replay_trust_root, evidence_manifest)
        require_text("S27 v2 cost input contract status", self.status)
        if self.status != S27_V2_COST_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 cost input contract must remain contract-only")
        self._validate_locked_maps()
        require_hash(
            "S27 v2 cost source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash("S27 v2 cost fill input contract hash", self.fill_input_contract_hash)
        require_hash("S27 v2 cost fill contract bundle hash", self.fill_contract_bundle_hash)
        require_hash("S27 v2 cost input policy hash", self.cost_input_policy_hash)
        require_hash_map(
            "S27 v2 cost expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_COST_INPUTS,
        )
        self._validate_fill_authority(
            source_input_manifest_contract,
            fill_input_contract,
            fill_contract,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 cost expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(replay_trust_root, fill_contract),
            REQUIRED_COST_INPUTS,
        )
        dependency_hash_by_label = self._validate_input_fields()
        self._validate_component_dependencies(dependency_hash_by_label)
        self._validate_invariant_dependencies(dependency_hash_by_label)
        require_hash("S27 v2 cost input set hash", self.cost_input_set_hash)
        require_hash("S27 v2 cost input contract hash", self.cost_input_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 cost input contract must preserve non-authorizations")

    def _validate_locked_maps(self) -> None:
        if tuple(REQUIRED_SOURCE_KIND_BY_COST_INPUT) != REQUIRED_COST_INPUTS:
            raise CarverBlocked("S27 v2 cost input source-kind map must cover locked inputs")
        if tuple(REQUIRED_COST_DEPENDENCIES_BY_COMPONENT) != REQUIRED_COST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 cost component dependency map must cover locked components")
        if tuple(REQUIRED_COST_DEPENDENCIES_BY_INVARIANT) != REQUIRED_COST_INVARIANTS:
            raise CarverBlocked("S27 v2 cost invariant dependency map must cover locked invariants")

    def _active_source_contract_hash_by_input_label(
        self,
        replay_trust_root: ReplayTrustRoot,
        fill_contract: FillContractBundle,
    ) -> dict[str, str]:
        active_hash_by_label: dict[str, str] = {}
        for input_label in REQUIRED_COST_INPUTS:
            source_kind = REQUIRED_SOURCE_KIND_BY_COST_INPUT[input_label]
            if source_kind == "FILL_LEDGER_OUTPUT":
                active_hash_by_label[input_label] = fill_contract.fill_contract_bundle_hash
            elif source_kind == "COST_BRANCH":
                active_hash_by_label[input_label] = self.cost_input_policy_hash
            elif source_kind == "SPREAD_SPACE":
                active_hash_by_label[input_label] = replay_trust_root.spread_unit_policy_hash
            elif source_kind == "POLICY_INPUT":
                active_hash_by_label[input_label] = self._active_policy_hash_for_input(
                    replay_trust_root,
                    input_label,
                )
            elif source_kind in {"MULTIPLIER_PROOF_INPUT", "CURRENCY_PROOF_INPUT"}:
                active_hash_by_label[input_label] = (
                    replay_trust_root.contract_multiplier_currency_policy_hash
                )
            else:
                raise CarverBlocked("S27 v2 cost input source kind cannot be authority-bound")
        return active_hash_by_label

    def _active_policy_hash_for_input(
        self,
        replay_trust_root: ReplayTrustRoot,
        input_label: str,
    ) -> str:
        if input_label == "COST_COMMISSION_POLICY_INPUT":
            return replay_trust_root.commission_policy_hash
        if input_label == "COST_SPREAD_POLICY_INPUT":
            return replay_trust_root.spread_unit_policy_hash
        if input_label in {"COST_DEFLATION_POLICY_INPUT", "COST_CALCULATION_POLICY_INPUT"}:
            return self.cost_input_policy_hash
        raise CarverBlocked("S27 v2 cost policy input cannot be authority-bound")

    def _validate_fill_authority(
        self,
        source_input_manifest_contract: SourceInputManifestContractBundle,
        fill_input_contract: FillInputContractBundle,
        fill_contract: FillContractBundle,
    ) -> None:
        if source_input_manifest_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 cost input must bind source-input manifest contract")
        if fill_input_contract.fill_input_contract_hash != self.fill_input_contract_hash:
            raise CarverBlocked("S27 v2 cost input must bind fill input contract")
        if fill_contract.fill_contract_bundle_hash != self.fill_contract_bundle_hash:
            raise CarverBlocked("S27 v2 cost input must bind fill contract bundle")
        if fill_input_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 cost input must bind fill source-input manifest")
        if fill_contract.source_binding.order_contract_bundle_hash != fill_input_contract.order_contract_bundle_hash:
            raise CarverBlocked("S27 v2 cost input must bind fill order authority")
        if fill_contract.source_binding.source_input_manifest_hash != source_input_manifest_contract.source_input_manifest_hash:
            raise CarverBlocked("S27 v2 cost input must bind fill source manifest hash")

    def _validate_input_fields(self) -> dict[str, str]:
        require_non_empty_tuple("S27 v2 cost input field contracts", self.input_field_contracts)
        seen_inputs: set[str] = set()
        dependency_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 cost input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 cost input source contract hash",
                contract.input_label,
                contract.source_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            dependency_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_COST_INPUTS:
            raise CarverBlocked("S27 v2 cost inputs must match locked input tuple")
        return dependency_hash_by_label

    def _validate_component_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 cost component dependency bindings",
            self.component_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.component_dependency_bindings)
            != REQUIRED_COST_COMPONENT_FAMILIES
        ):
            raise CarverBlocked("S27 v2 cost component dependencies must match locked components")
        component_binding_hash_by_label = {
            binding.dependency_label: binding.dependency_binding_contract_hash
            for binding in self.component_dependency_bindings
        }
        seen_components: set[str] = set()
        for binding in self.component_dependency_bindings:
            binding.validate_component()
            if binding.dependency_label in seen_components:
                raise CarverBlocked("S27 v2 cost component dependency bindings must be unique")
            seen_components.add(binding.dependency_label)
            self._require_matching_dependency_hashes(
                binding,
                {
                    **component_binding_hash_by_label,
                    **dependency_hash_by_label,
                },
            )
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_invariant_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 cost invariant dependency bindings",
            self.invariant_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.invariant_dependency_bindings)
            != REQUIRED_COST_INVARIANTS
        ):
            raise CarverBlocked("S27 v2 cost invariant dependencies must match locked invariants")
        seen_invariants: set[str] = set()
        for binding in self.invariant_dependency_bindings:
            binding.validate_invariant()
            if binding.dependency_label in seen_invariants:
                raise CarverBlocked("S27 v2 cost invariant dependency bindings must be unique")
            seen_invariants.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)

    def _require_matching_dependency_hashes(
        self,
        binding: CostDependencyBindingContract,
        dependency_hash_by_label: dict[str, str],
    ) -> None:
        require_matching_dependency_hashes(
            "S27 v2 cost",
            binding.required_dependency_labels,
            binding.required_dependency_contract_hashes,
            dependency_hash_by_label,
        )

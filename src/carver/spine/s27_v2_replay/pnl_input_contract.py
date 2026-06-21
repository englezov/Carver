from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
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
from .pnl_contract import (
    REQUIRED_PNL_BRIDGE_LABELS,
    REQUIRED_PNL_COMPONENT_FAMILIES,
    REQUIRED_PNL_INVARIANTS,
    REQUIRED_PNL_PRICE_SOURCE_LABELS,
)
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


S27_V2_PNL_INPUT_CONTRACT_ONLY_STATUS = "S27_V2_PNL_INPUT_CONTRACT_ONLY"
PLANNED_PNL_INPUT_STATUS = "PLANNED_PNL_INPUT_ONLY"

PNL_INPUT_NOT_APPLICABLE = "NOT_APPLICABLE"

PNL_INPUT_SOURCE_KINDS = (
    "TRUST_ROOT_OUTPUT",
    "SOURCE_UNIVERSE_OUTPUT",
    "TRANSITION_LEDGER_OUTPUT",
    "POSITION_SOURCE_OUTPUT",
    "PRICE_SOURCE",
    "PRICE_ROW_PROOF",
    "BRIDGE_PROOF",
    "FILL_HASH_SET_OUTPUT",
    "COST_HASH_SET_OUTPUT",
    "MULTIPLIER_PROOF_INPUT",
    "CURRENCY_PROOF_INPUT",
    "POLICY_INPUT",
)

REQUIRED_PNL_INPUTS = (
    "PNL_TRUST_ROOT_HASH_INPUT",
    "PNL_SOURCE_UNIVERSE_HASH_INPUT",
    "PNL_PREVIOUS_STEP_OR_INITIAL_STATE_HASH_INPUT",
    "PNL_STARTING_WORKING_STATE_HASH_INPUT",
    "PNL_TRANSITION_HASH_INPUT",
    "PNL_ENDING_WORKING_STATE_HASH_INPUT",
    "PNL_STARTING_POSITION_INPUT",
    "PNL_ENDING_POSITION_INPUT",
    "PNL_POSITION_SOURCE_HASH_INPUT",
    "PNL_CLOSE_ONLY_PRICE_SOURCE_INPUT",
    "PNL_START_PRICE_ROW_HASH_INPUT",
    "PNL_END_PRICE_ROW_HASH_INPUT",
    "PNL_RAW_SYMBOL_CONTINUITY_INPUT",
    "PNL_ROLL_BRIDGE_INPUT",
    "PNL_CONTRACT_MULTIPLIER_POLICY_INPUT",
    "PNL_CURRENCY_POLICY_INPUT",
    "PNL_FILL_HASH_SET_INPUT",
    "PNL_COST_HASH_SET_INPUT",
    "PNL_FORMULA_POLICY_INPUT",
    "PNL_COST_APPLICATION_POLICY_INPUT",
    "PNL_TARGET_POSITION_SHORTCUT_QUARANTINE_INPUT",
)

REQUIRED_SOURCE_KIND_BY_PNL_INPUT = {
    "PNL_TRUST_ROOT_HASH_INPUT": "TRUST_ROOT_OUTPUT",
    "PNL_SOURCE_UNIVERSE_HASH_INPUT": "SOURCE_UNIVERSE_OUTPUT",
    "PNL_PREVIOUS_STEP_OR_INITIAL_STATE_HASH_INPUT": "TRANSITION_LEDGER_OUTPUT",
    "PNL_STARTING_WORKING_STATE_HASH_INPUT": "TRANSITION_LEDGER_OUTPUT",
    "PNL_TRANSITION_HASH_INPUT": "TRANSITION_LEDGER_OUTPUT",
    "PNL_ENDING_WORKING_STATE_HASH_INPUT": "TRANSITION_LEDGER_OUTPUT",
    "PNL_STARTING_POSITION_INPUT": "TRANSITION_LEDGER_OUTPUT",
    "PNL_ENDING_POSITION_INPUT": "TRANSITION_LEDGER_OUTPUT",
    "PNL_POSITION_SOURCE_HASH_INPUT": "POSITION_SOURCE_OUTPUT",
    "PNL_CLOSE_ONLY_PRICE_SOURCE_INPUT": "PRICE_SOURCE",
    "PNL_START_PRICE_ROW_HASH_INPUT": "PRICE_ROW_PROOF",
    "PNL_END_PRICE_ROW_HASH_INPUT": "PRICE_ROW_PROOF",
    "PNL_RAW_SYMBOL_CONTINUITY_INPUT": "BRIDGE_PROOF",
    "PNL_ROLL_BRIDGE_INPUT": "BRIDGE_PROOF",
    "PNL_CONTRACT_MULTIPLIER_POLICY_INPUT": "MULTIPLIER_PROOF_INPUT",
    "PNL_CURRENCY_POLICY_INPUT": "CURRENCY_PROOF_INPUT",
    "PNL_FILL_HASH_SET_INPUT": "FILL_HASH_SET_OUTPUT",
    "PNL_COST_HASH_SET_INPUT": "COST_HASH_SET_OUTPUT",
    "PNL_FORMULA_POLICY_INPUT": "POLICY_INPUT",
    "PNL_COST_APPLICATION_POLICY_INPUT": "POLICY_INPUT",
    "PNL_TARGET_POSITION_SHORTCUT_QUARANTINE_INPUT": "POLICY_INPUT",
}

REQUIRED_TRUST_ROOT_OUTPUT_BY_PNL_INPUT = {
    "PNL_TRUST_ROOT_HASH_INPUT": "REPLAY_TRUST_ROOT_HASH",
}

REQUIRED_SOURCE_UNIVERSE_OUTPUT_BY_PNL_INPUT = {
    "PNL_SOURCE_UNIVERSE_HASH_INPUT": "SOURCE_UNIVERSE_HASH",
}

REQUIRED_TRANSITION_LEDGER_OUTPUT_BY_PNL_INPUT = {
    "PNL_PREVIOUS_STEP_OR_INITIAL_STATE_HASH_INPUT": "PREVIOUS_STEP_OR_INITIAL_STATE_HASH",
    "PNL_STARTING_WORKING_STATE_HASH_INPUT": "STARTING_WORKING_STATE_HASH",
    "PNL_TRANSITION_HASH_INPUT": "TRANSITION_HASH",
    "PNL_ENDING_WORKING_STATE_HASH_INPUT": "ENDING_WORKING_STATE_HASH",
    "PNL_STARTING_POSITION_INPUT": "STARTING_POSITION",
    "PNL_ENDING_POSITION_INPUT": "ENDING_POSITION",
}

REQUIRED_POSITION_SOURCE_OUTPUT_BY_PNL_INPUT = {
    "PNL_POSITION_SOURCE_HASH_INPUT": "POSITION_SOURCE_HASH",
}

REQUIRED_PRICE_SOURCE_BY_PNL_INPUT = {
    "PNL_CLOSE_ONLY_PRICE_SOURCE_INPUT": "CLOSE_ONLY",
}

REQUIRED_PRICE_ROW_PROOF_BY_PNL_INPUT = {
    "PNL_START_PRICE_ROW_HASH_INPUT": "START_PRICE_SOURCE_ROW_HASH",
    "PNL_END_PRICE_ROW_HASH_INPUT": "END_PRICE_SOURCE_ROW_HASH",
}

REQUIRED_BRIDGE_PROOF_BY_PNL_INPUT = {
    "PNL_RAW_SYMBOL_CONTINUITY_INPUT": "RAW_SYMBOL_CONTINUITY",
    "PNL_ROLL_BRIDGE_INPUT": "ROLL_BRIDGE",
}

REQUIRED_FILL_HASH_SET_OUTPUT_BY_PNL_INPUT = {
    "PNL_FILL_HASH_SET_INPUT": "FILL_HASH_SET_HASH",
}

REQUIRED_COST_HASH_SET_OUTPUT_BY_PNL_INPUT = {
    "PNL_COST_HASH_SET_INPUT": "COST_HASH_SET_HASH",
}

REQUIRED_MULTIPLIER_PROOF_BY_PNL_INPUT = {
    "PNL_CONTRACT_MULTIPLIER_POLICY_INPUT": "CONTRACT_MULTIPLIER_VALUE_AND_SOURCE_PROOF",
}

REQUIRED_CURRENCY_PROOF_BY_PNL_INPUT = {
    "PNL_CURRENCY_POLICY_INPUT": "CURRENCY_POLICY_AND_OPTIONAL_CONVERSION_PROOF",
}

REQUIRED_POLICY_LABEL_BY_PNL_INPUT = {
    "PNL_FORMULA_POLICY_INPUT": "PNL_FORMULA_POLICY",
    "PNL_COST_APPLICATION_POLICY_INPUT": "COST_APPLICATION_POLICY",
    "PNL_TARGET_POSITION_SHORTCUT_QUARANTINE_INPUT": "TARGET_POSITION_SHORTCUT_QUARANTINE_POLICY",
}

PNL_PRICE_ROW_MANIFEST_FIELD = "DAILY_CURRENT_CONTRACT_ROW_HASH"

REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT = {
    "TRUST_ROOT_REFERENCE": (
        "PNL_TRUST_ROOT_HASH_INPUT",
        "PNL_SOURCE_UNIVERSE_HASH_INPUT",
    ),
    "TRANSITION_STATE_REFERENCE": (
        "PNL_PREVIOUS_STEP_OR_INITIAL_STATE_HASH_INPUT",
        "PNL_STARTING_WORKING_STATE_HASH_INPUT",
        "PNL_TRANSITION_HASH_INPUT",
        "PNL_ENDING_WORKING_STATE_HASH_INPUT",
        "PNL_STARTING_POSITION_INPUT",
        "PNL_ENDING_POSITION_INPUT",
    ),
    "POSITION_SOURCE_REFERENCE": (
        "PNL_POSITION_SOURCE_HASH_INPUT",
    ),
    "CLOSE_ONLY_PRICE_SOURCE_POLICY": (
        "PNL_CLOSE_ONLY_PRICE_SOURCE_INPUT",
        "PNL_START_PRICE_ROW_HASH_INPUT",
        "PNL_END_PRICE_ROW_HASH_INPUT",
    ),
    "RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE": (
        "PNL_RAW_SYMBOL_CONTINUITY_INPUT",
        "PNL_ROLL_BRIDGE_INPUT",
    ),
    "CONTRACT_MULTIPLIER_CURRENCY_POLICY": (
        "PNL_CONTRACT_MULTIPLIER_POLICY_INPUT",
        "PNL_CURRENCY_POLICY_INPUT",
    ),
    "FILL_COST_APPLICATION": (
        "PNL_FILL_HASH_SET_INPUT",
        "PNL_COST_HASH_SET_INPUT",
        "PNL_COST_APPLICATION_POLICY_INPUT",
    ),
    "PNL_SUMMARY": (
        "TRUST_ROOT_REFERENCE",
        "TRANSITION_STATE_REFERENCE",
        "POSITION_SOURCE_REFERENCE",
        "CLOSE_ONLY_PRICE_SOURCE_POLICY",
        "RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE",
        "CONTRACT_MULTIPLIER_CURRENCY_POLICY",
        "FILL_COST_APPLICATION",
        "PNL_FORMULA_POLICY_INPUT",
        "PNL_TARGET_POSITION_SHORTCUT_QUARANTINE_INPUT",
    ),
}

REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT = {
    "TRUST_ROOT_HASH_BINDING": (
        "TRUST_ROOT_REFERENCE",
    ),
    "PREVIOUS_STEP_OR_INITIAL_STATE_HASH_BINDING": (
        "PNL_PREVIOUS_STEP_OR_INITIAL_STATE_HASH_INPUT",
    ),
    "TRANSITION_AND_WORKING_STATE_HASH_BINDING": (
        "TRANSITION_STATE_REFERENCE",
    ),
    "POSITION_SOURCE_HASH_BINDING": (
        "POSITION_SOURCE_REFERENCE",
    ),
    "CLOSE_ONLY_START_END_PRICE_ROW_HASH_BINDING": (
        "CLOSE_ONLY_PRICE_SOURCE_POLICY",
    ),
    "RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE_HASH_BINDING": (
        "RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE",
    ),
    "CONTRACT_MULTIPLIER_SOURCE_BINDING": (
        "PNL_CONTRACT_MULTIPLIER_POLICY_INPUT",
        "CONTRACT_MULTIPLIER_CURRENCY_POLICY",
    ),
    "CURRENCY_POLICY_OPTIONAL_FIELD_BINDING": (
        "PNL_CURRENCY_POLICY_INPUT",
        "CONTRACT_MULTIPLIER_CURRENCY_POLICY",
    ),
    "FILL_HASH_SET_BINDING": (
        "PNL_FILL_HASH_SET_INPUT",
        "FILL_COST_APPLICATION",
    ),
    "COST_HASH_SET_BINDING": (
        "PNL_COST_HASH_SET_INPUT",
        "FILL_COST_APPLICATION",
    ),
    "PNL_FORMULA_POLICY_BINDING": (
        "PNL_FORMULA_POLICY_INPUT",
        "PNL_SUMMARY",
    ),
    "NO_TARGET_POSITION_SHORTCUT_PNL": (
        "PNL_TARGET_POSITION_SHORTCUT_QUARANTINE_INPUT",
        "PNL_SUMMARY",
    ),
    "NO_RESULT_INTERPRETATION_IN_PNL_CONTRACT": (
        "PNL_SUMMARY",
    ),
}


@dataclass(frozen=True)
class PnlInputFieldContract:
    input_label: str
    input_status: str
    source_kind: str
    trust_root_output_label: str
    source_universe_output_label: str
    transition_ledger_output_label: str
    position_source_output_label: str
    price_source_label: str
    price_row_proof_label: str
    bridge_proof_label: str
    fill_hash_set_output_label: str
    cost_hash_set_output_label: str
    multiplier_proof_label: str
    currency_proof_label: str
    source_policy_label: str
    source_contract_hash: str
    pnl_input_policy_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 PnL input label", self.input_label)
        if self.input_label not in REQUIRED_PNL_INPUTS:
            raise CarverBlocked("S27 v2 PnL input label is not locked")
        require_text("S27 v2 PnL input status", self.input_status)
        if self.input_status != PLANNED_PNL_INPUT_STATUS:
            raise CarverBlocked("S27 v2 PnL input must remain planned-only")
        require_text("S27 v2 PnL input source kind", self.source_kind)
        if self.source_kind not in PNL_INPUT_SOURCE_KINDS:
            raise CarverBlocked("S27 v2 PnL input source kind is not locked")
        if self.source_kind != REQUIRED_SOURCE_KIND_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked source kind")
        self._validate_source_target()
        require_hash("S27 v2 PnL input source contract hash", self.source_contract_hash)
        require_hash("S27 v2 PnL input policy hash", self.pnl_input_policy_hash)
        require_hash("S27 v2 PnL input field contract hash", self.input_field_contract_hash)

    def _validate_source_target(self) -> None:
        if self.source_kind == "TRUST_ROOT_OUTPUT":
            self._validate_trust_root_output_target()
        elif self.source_kind == "SOURCE_UNIVERSE_OUTPUT":
            self._validate_source_universe_output_target()
        elif self.source_kind == "TRANSITION_LEDGER_OUTPUT":
            self._validate_transition_ledger_output_target()
        elif self.source_kind == "POSITION_SOURCE_OUTPUT":
            self._validate_position_source_output_target()
        elif self.source_kind == "PRICE_SOURCE":
            self._validate_price_source_target()
        elif self.source_kind == "PRICE_ROW_PROOF":
            self._validate_price_row_proof_target()
        elif self.source_kind == "BRIDGE_PROOF":
            self._validate_bridge_proof_target()
        elif self.source_kind == "FILL_HASH_SET_OUTPUT":
            self._validate_fill_hash_set_output_target()
        elif self.source_kind == "COST_HASH_SET_OUTPUT":
            self._validate_cost_hash_set_output_target()
        elif self.source_kind == "MULTIPLIER_PROOF_INPUT":
            self._validate_multiplier_proof_target()
        elif self.source_kind == "CURRENCY_PROOF_INPUT":
            self._validate_currency_proof_target()
        elif self.source_kind == "POLICY_INPUT":
            self._validate_policy_input_target()

    def _require_not_applicable(self, name: str, value: str) -> None:
        require_text(name, value)
        if value != PNL_INPUT_NOT_APPLICABLE:
            raise CarverBlocked(f"{name} must be not applicable")

    def _require_common_targets_not_applicable(self, exempt_name: str) -> None:
        targets = (
            ("S27 v2 PnL trust-root output label", self.trust_root_output_label),
            ("S27 v2 PnL source-universe output label", self.source_universe_output_label),
            ("S27 v2 PnL transition ledger output label", self.transition_ledger_output_label),
            ("S27 v2 PnL position source output label", self.position_source_output_label),
            ("S27 v2 PnL price source label", self.price_source_label),
            ("S27 v2 PnL price row proof label", self.price_row_proof_label),
            ("S27 v2 PnL bridge proof label", self.bridge_proof_label),
            ("S27 v2 PnL fill hash-set output label", self.fill_hash_set_output_label),
            ("S27 v2 PnL cost hash-set output label", self.cost_hash_set_output_label),
            ("S27 v2 PnL multiplier proof label", self.multiplier_proof_label),
            ("S27 v2 PnL currency proof label", self.currency_proof_label),
            ("S27 v2 PnL source policy label", self.source_policy_label),
        )
        for name, value in targets:
            if name != exempt_name:
                self._require_not_applicable(name, value)

    def _validate_trust_root_output_target(self) -> None:
        require_text("S27 v2 PnL trust-root output label", self.trust_root_output_label)
        if self.trust_root_output_label != REQUIRED_TRUST_ROOT_OUTPUT_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked trust-root output")
        self._require_common_targets_not_applicable("S27 v2 PnL trust-root output label")

    def _validate_source_universe_output_target(self) -> None:
        require_text("S27 v2 PnL source-universe output label", self.source_universe_output_label)
        if (
            self.source_universe_output_label
            != REQUIRED_SOURCE_UNIVERSE_OUTPUT_BY_PNL_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 PnL input must use the locked source-universe output")
        self._require_common_targets_not_applicable("S27 v2 PnL source-universe output label")

    def _validate_transition_ledger_output_target(self) -> None:
        require_text("S27 v2 PnL transition ledger output label", self.transition_ledger_output_label)
        if self.transition_ledger_output_label != REQUIRED_TRANSITION_LEDGER_OUTPUT_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked transition output")
        self._require_common_targets_not_applicable("S27 v2 PnL transition ledger output label")

    def _validate_position_source_output_target(self) -> None:
        require_text("S27 v2 PnL position source output label", self.position_source_output_label)
        if self.position_source_output_label != REQUIRED_POSITION_SOURCE_OUTPUT_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked position source output")
        self._require_common_targets_not_applicable("S27 v2 PnL position source output label")

    def _validate_price_source_target(self) -> None:
        require_text("S27 v2 PnL price source label", self.price_source_label)
        if self.price_source_label not in REQUIRED_PNL_PRICE_SOURCE_LABELS:
            raise CarverBlocked("S27 v2 PnL price source label is not locked")
        if self.price_source_label != REQUIRED_PRICE_SOURCE_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked price source")
        self._require_common_targets_not_applicable("S27 v2 PnL price source label")

    def _validate_price_row_proof_target(self) -> None:
        require_text("S27 v2 PnL price row proof label", self.price_row_proof_label)
        if self.price_row_proof_label != REQUIRED_PRICE_ROW_PROOF_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked price row proof")
        self._require_common_targets_not_applicable("S27 v2 PnL price row proof label")

    def _validate_bridge_proof_target(self) -> None:
        require_text("S27 v2 PnL bridge proof label", self.bridge_proof_label)
        if self.bridge_proof_label not in REQUIRED_PNL_BRIDGE_LABELS:
            raise CarverBlocked("S27 v2 PnL bridge proof label is not locked")
        if self.bridge_proof_label != REQUIRED_BRIDGE_PROOF_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked bridge proof")
        self._require_common_targets_not_applicable("S27 v2 PnL bridge proof label")

    def _validate_fill_hash_set_output_target(self) -> None:
        require_text("S27 v2 PnL fill hash-set output label", self.fill_hash_set_output_label)
        if self.fill_hash_set_output_label != REQUIRED_FILL_HASH_SET_OUTPUT_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked fill hash-set output")
        self._require_common_targets_not_applicable("S27 v2 PnL fill hash-set output label")

    def _validate_cost_hash_set_output_target(self) -> None:
        require_text("S27 v2 PnL cost hash-set output label", self.cost_hash_set_output_label)
        if self.cost_hash_set_output_label != REQUIRED_COST_HASH_SET_OUTPUT_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked cost hash-set output")
        self._require_common_targets_not_applicable("S27 v2 PnL cost hash-set output label")

    def _validate_multiplier_proof_target(self) -> None:
        require_text("S27 v2 PnL multiplier proof label", self.multiplier_proof_label)
        if self.multiplier_proof_label != REQUIRED_MULTIPLIER_PROOF_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked multiplier proof")
        self._require_common_targets_not_applicable("S27 v2 PnL multiplier proof label")

    def _validate_currency_proof_target(self) -> None:
        require_text("S27 v2 PnL currency proof label", self.currency_proof_label)
        if self.currency_proof_label != REQUIRED_CURRENCY_PROOF_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked currency proof")
        self._require_common_targets_not_applicable("S27 v2 PnL currency proof label")

    def _validate_policy_input_target(self) -> None:
        require_text("S27 v2 PnL source policy label", self.source_policy_label)
        if self.source_policy_label != REQUIRED_POLICY_LABEL_BY_PNL_INPUT[self.input_label]:
            raise CarverBlocked("S27 v2 PnL input must use the locked source policy")
        self._require_common_targets_not_applicable("S27 v2 PnL source policy label")


@dataclass(frozen=True)
class PnlDependencyBindingContract:
    dependency_label: str
    required_dependency_labels: tuple[str, ...]
    required_dependency_contract_hashes: tuple[str, ...]
    dependency_binding_policy_hash: str
    dependency_binding_contract_hash: str

    def validate_component(self) -> None:
        require_text("S27 v2 PnL component dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_PNL_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 PnL component dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT[self.dependency_label])

    def validate_invariant(self) -> None:
        require_text("S27 v2 PnL invariant dependency label", self.dependency_label)
        if self.dependency_label not in REQUIRED_PNL_INVARIANTS:
            raise CarverBlocked("S27 v2 PnL invariant dependency label is not locked")
        self._validate_required_dependencies(REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT[self.dependency_label])

    def _validate_required_dependencies(self, locked_labels: tuple[str, ...]) -> None:
        require_non_empty_tuple("S27 v2 PnL required dependency labels", self.required_dependency_labels)
        if self.required_dependency_labels != locked_labels:
            raise CarverBlocked("S27 v2 PnL dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 PnL required dependency contract hashes",
            self.required_dependency_contract_hashes,
        )
        if len(self.required_dependency_contract_hashes) != len(self.required_dependency_labels):
            raise CarverBlocked("S27 v2 PnL dependency hashes must match labels")
        for dependency_hash in self.required_dependency_contract_hashes:
            require_hash("S27 v2 PnL dependency contract hash", dependency_hash)
        require_hash("S27 v2 PnL dependency binding policy hash", self.dependency_binding_policy_hash)
        require_hash("S27 v2 PnL dependency binding contract hash", self.dependency_binding_contract_hash)


@dataclass(frozen=True)
class PnlInputContractBundle:
    status: str
    replay_trust_root_hash: str
    source_universe_hash: str
    previous_step_or_initial_state_hash: str
    starting_working_state_hash: str
    transition_hash: str
    ending_working_state_hash: str
    starting_position_hash: str
    ending_position_hash: str
    position_source_hash: str
    close_only_price_source_policy_hash: str
    start_price_source_row_hash: str
    end_price_source_row_hash: str
    raw_symbol_continuity_proof_hash: str
    roll_bridge_proof_hash: str
    contract_multiplier_proof_hash: str
    currency_policy_proof_hash: str
    fill_hash_set_hash: str
    cost_hash_set_hash: str
    source_input_manifest_contract_hash: str
    cost_input_contract_hash: str
    cost_contract_bundle_hash: str
    pnl_input_policy_hash: str
    input_field_contracts: tuple[PnlInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    component_dependency_bindings: tuple[PnlDependencyBindingContract, ...]
    invariant_dependency_bindings: tuple[PnlDependencyBindingContract, ...]
    pnl_input_set_hash: str
    pnl_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 PnL input requires cost and upstream replay authority"
        )

    def validate_against_cost_authority(
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
    ) -> None:
        cost_input_contract.validate_against_fill_authority(
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
        )
        cost_contract.validate_against_policy_authority(replay_trust_root, evidence_manifest)
        require_text("S27 v2 PnL input contract status", self.status)
        if self.status != S27_V2_PNL_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 PnL input contract must remain contract-only")
        self._validate_locked_maps()
        require_hash("S27 v2 PnL replay trust-root hash", self.replay_trust_root_hash)
        require_hash("S27 v2 PnL source-universe hash", self.source_universe_hash)
        require_hash(
            "S27 v2 PnL previous-step or initial-state hash",
            self.previous_step_or_initial_state_hash,
        )
        require_hash("S27 v2 PnL starting working-state hash", self.starting_working_state_hash)
        require_hash("S27 v2 PnL transition hash", self.transition_hash)
        require_hash("S27 v2 PnL ending working-state hash", self.ending_working_state_hash)
        require_hash("S27 v2 PnL starting position hash", self.starting_position_hash)
        require_hash("S27 v2 PnL ending position hash", self.ending_position_hash)
        require_hash("S27 v2 PnL position source hash", self.position_source_hash)
        require_hash("S27 v2 PnL close-only price-source policy hash", self.close_only_price_source_policy_hash)
        require_hash("S27 v2 PnL start price source row hash", self.start_price_source_row_hash)
        require_hash("S27 v2 PnL end price source row hash", self.end_price_source_row_hash)
        require_hash("S27 v2 PnL raw symbol continuity proof hash", self.raw_symbol_continuity_proof_hash)
        require_hash("S27 v2 PnL roll bridge proof hash", self.roll_bridge_proof_hash)
        require_hash("S27 v2 PnL contract multiplier proof hash", self.contract_multiplier_proof_hash)
        require_hash("S27 v2 PnL currency policy proof hash", self.currency_policy_proof_hash)
        require_hash("S27 v2 PnL fill hash-set hash", self.fill_hash_set_hash)
        require_hash("S27 v2 PnL cost hash-set hash", self.cost_hash_set_hash)
        require_hash(
            "S27 v2 PnL source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash("S27 v2 PnL cost input contract hash", self.cost_input_contract_hash)
        require_hash("S27 v2 PnL cost contract bundle hash", self.cost_contract_bundle_hash)
        require_hash("S27 v2 PnL input policy hash", self.pnl_input_policy_hash)
        require_hash_map(
            "S27 v2 PnL expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_PNL_INPUTS,
        )
        self._validate_cost_authority(
            replay_trust_root,
            source_row_selection_external_authority,
            source_input_manifest_contract,
            position_contract,
            order_contract,
            fill_contract,
            cost_input_contract,
            cost_contract,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 PnL expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(
                replay_trust_root,
                source_row_selection_external_authority,
                source_input_manifest_contract,
                position_contract,
                order_contract,
                fill_contract,
                cost_contract,
            ),
            REQUIRED_PNL_INPUTS,
        )
        dependency_hash_by_label = self._validate_input_fields()
        self._validate_component_dependencies(dependency_hash_by_label)
        self._validate_invariant_dependencies(dependency_hash_by_label)
        require_hash("S27 v2 PnL input set hash", self.pnl_input_set_hash)
        require_hash("S27 v2 PnL input contract hash", self.pnl_input_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 PnL input contract must preserve non-authorizations")

    def _validate_locked_maps(self) -> None:
        if tuple(REQUIRED_SOURCE_KIND_BY_PNL_INPUT) != REQUIRED_PNL_INPUTS:
            raise CarverBlocked("S27 v2 PnL input source-kind map must cover locked inputs")
        if tuple(REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT) != REQUIRED_PNL_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 PnL component dependency map must cover locked components")
        if tuple(REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT) != REQUIRED_PNL_INVARIANTS:
            raise CarverBlocked("S27 v2 PnL invariant dependency map must cover locked invariants")

    def _active_source_contract_hash_by_input_label(
        self,
        replay_trust_root: ReplayTrustRoot,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_input_manifest_contract: SourceInputManifestContractBundle,
        position_contract: PositionContractBundle,
        order_contract: OrderContractBundle,
        fill_contract: FillContractBundle,
        cost_contract: CostContractBundle,
    ) -> dict[str, str]:
        return {
            "PNL_TRUST_ROOT_HASH_INPUT": replay_trust_root.replay_trust_root_hash,
            "PNL_SOURCE_UNIVERSE_HASH_INPUT": (
                source_row_selection_external_authority.source_universe_contract_bundle_hash
            ),
            "PNL_PREVIOUS_STEP_OR_INITIAL_STATE_HASH_INPUT": order_contract.order_contract_bundle_hash,
            "PNL_STARTING_WORKING_STATE_HASH_INPUT": order_contract.order_contract_bundle_hash,
            "PNL_TRANSITION_HASH_INPUT": order_contract.order_contract_bundle_hash,
            "PNL_ENDING_WORKING_STATE_HASH_INPUT": order_contract.order_contract_bundle_hash,
            "PNL_STARTING_POSITION_INPUT": order_contract.order_contract_bundle_hash,
            "PNL_ENDING_POSITION_INPUT": order_contract.order_contract_bundle_hash,
            "PNL_POSITION_SOURCE_HASH_INPUT": position_contract.desired_position_contract_bundle_hash,
            "PNL_CLOSE_ONLY_PRICE_SOURCE_INPUT": self.pnl_input_policy_hash,
            "PNL_START_PRICE_ROW_HASH_INPUT": (
                source_input_manifest_contract.expected_selected_row_hash_by_manifest_field[
                    PNL_PRICE_ROW_MANIFEST_FIELD
                ]
            ),
            "PNL_END_PRICE_ROW_HASH_INPUT": (
                source_input_manifest_contract.expected_selected_row_hash_by_manifest_field[
                    PNL_PRICE_ROW_MANIFEST_FIELD
                ]
            ),
            "PNL_RAW_SYMBOL_CONTINUITY_INPUT": source_input_manifest_contract.source_input_manifest_hash,
            "PNL_ROLL_BRIDGE_INPUT": source_input_manifest_contract.source_input_manifest_hash,
            "PNL_CONTRACT_MULTIPLIER_POLICY_INPUT": (
                replay_trust_root.contract_multiplier_currency_policy_hash
            ),
            "PNL_CURRENCY_POLICY_INPUT": replay_trust_root.contract_multiplier_currency_policy_hash,
            "PNL_FILL_HASH_SET_INPUT": fill_contract.fill_contract_bundle_hash,
            "PNL_COST_HASH_SET_INPUT": cost_contract.cost_contract_bundle_hash,
            "PNL_FORMULA_POLICY_INPUT": self.pnl_input_policy_hash,
            "PNL_COST_APPLICATION_POLICY_INPUT": self.pnl_input_policy_hash,
            "PNL_TARGET_POSITION_SHORTCUT_QUARANTINE_INPUT": self.pnl_input_policy_hash,
        }

    def _validate_cost_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_input_manifest_contract: SourceInputManifestContractBundle,
        position_contract: PositionContractBundle,
        order_contract: OrderContractBundle,
        fill_contract: FillContractBundle,
        cost_input_contract: CostInputContractBundle,
        cost_contract: CostContractBundle,
    ) -> None:
        active_source_hash_by_input_label = self._active_source_contract_hash_by_input_label(
            replay_trust_root,
            source_row_selection_external_authority,
            source_input_manifest_contract,
            position_contract,
            order_contract,
            fill_contract,
            cost_contract,
        )
        observed_source_hash_by_input_label = {
            "PNL_TRUST_ROOT_HASH_INPUT": self.replay_trust_root_hash,
            "PNL_SOURCE_UNIVERSE_HASH_INPUT": self.source_universe_hash,
            "PNL_PREVIOUS_STEP_OR_INITIAL_STATE_HASH_INPUT": self.previous_step_or_initial_state_hash,
            "PNL_STARTING_WORKING_STATE_HASH_INPUT": self.starting_working_state_hash,
            "PNL_TRANSITION_HASH_INPUT": self.transition_hash,
            "PNL_ENDING_WORKING_STATE_HASH_INPUT": self.ending_working_state_hash,
            "PNL_STARTING_POSITION_INPUT": self.starting_position_hash,
            "PNL_ENDING_POSITION_INPUT": self.ending_position_hash,
            "PNL_POSITION_SOURCE_HASH_INPUT": self.position_source_hash,
            "PNL_CLOSE_ONLY_PRICE_SOURCE_INPUT": self.close_only_price_source_policy_hash,
            "PNL_START_PRICE_ROW_HASH_INPUT": self.start_price_source_row_hash,
            "PNL_END_PRICE_ROW_HASH_INPUT": self.end_price_source_row_hash,
            "PNL_RAW_SYMBOL_CONTINUITY_INPUT": self.raw_symbol_continuity_proof_hash,
            "PNL_ROLL_BRIDGE_INPUT": self.roll_bridge_proof_hash,
            "PNL_CONTRACT_MULTIPLIER_POLICY_INPUT": self.contract_multiplier_proof_hash,
            "PNL_CURRENCY_POLICY_INPUT": self.currency_policy_proof_hash,
            "PNL_FILL_HASH_SET_INPUT": self.fill_hash_set_hash,
            "PNL_COST_HASH_SET_INPUT": self.cost_hash_set_hash,
            "PNL_FORMULA_POLICY_INPUT": self.pnl_input_policy_hash,
            "PNL_COST_APPLICATION_POLICY_INPUT": self.pnl_input_policy_hash,
            "PNL_TARGET_POSITION_SHORTCUT_QUARANTINE_INPUT": self.pnl_input_policy_hash,
        }
        require_hash_map_matches_active_authority(
            "S27 v2 PnL routed authority",
            observed_source_hash_by_input_label,
            active_source_hash_by_input_label,
            REQUIRED_PNL_INPUTS,
        )
        if source_input_manifest_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 PnL input must bind source-input manifest contract")
        if cost_input_contract.cost_input_contract_hash != self.cost_input_contract_hash:
            raise CarverBlocked("S27 v2 PnL input must bind cost input contract")
        if cost_contract.cost_contract_bundle_hash != self.cost_contract_bundle_hash:
            raise CarverBlocked("S27 v2 PnL input must bind cost contract bundle")
        if cost_input_contract.source_input_manifest_contract_hash != self.source_input_manifest_contract_hash:
            raise CarverBlocked("S27 v2 PnL input must bind cost source-input manifest")
        if cost_contract.source_binding.fill_contract_bundle_hash != cost_input_contract.fill_contract_bundle_hash:
            raise CarverBlocked("S27 v2 PnL input must bind cost fill authority")
        if cost_contract.source_binding.source_input_manifest_hash != source_input_manifest_contract.source_input_manifest_hash:
            raise CarverBlocked("S27 v2 PnL input must bind cost source manifest hash")
        if cost_contract.contract_multiplier_policy_hash != replay_trust_root.contract_multiplier_currency_policy_hash:
            raise CarverBlocked("S27 v2 PnL input must bind cost multiplier policy to trust root")
        if cost_contract.currency_conversion_policy_hash != replay_trust_root.contract_multiplier_currency_policy_hash:
            raise CarverBlocked("S27 v2 PnL input must bind cost currency policy to trust root")

    def _validate_input_fields(self) -> dict[str, str]:
        require_non_empty_tuple("S27 v2 PnL input field contracts", self.input_field_contracts)
        seen_inputs: set[str] = set()
        dependency_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 PnL input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 PnL input source contract hash",
                contract.input_label,
                contract.source_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            dependency_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_PNL_INPUTS:
            raise CarverBlocked("S27 v2 PnL inputs must match locked input tuple")
        return dependency_hash_by_label

    def _validate_component_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 PnL component dependency bindings",
            self.component_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.component_dependency_bindings)
            != REQUIRED_PNL_COMPONENT_FAMILIES
        ):
            raise CarverBlocked("S27 v2 PnL component dependencies must match locked components")
        seen_components: set[str] = set()
        for binding in self.component_dependency_bindings:
            binding.validate_component()
            if binding.dependency_label in seen_components:
                raise CarverBlocked("S27 v2 PnL component dependency bindings must be unique")
            seen_components.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)
            dependency_hash_by_label[binding.dependency_label] = binding.dependency_binding_contract_hash

    def _validate_invariant_dependencies(self, dependency_hash_by_label: dict[str, str]) -> None:
        require_non_empty_tuple(
            "S27 v2 PnL invariant dependency bindings",
            self.invariant_dependency_bindings,
        )
        if (
            tuple(binding.dependency_label for binding in self.invariant_dependency_bindings)
            != REQUIRED_PNL_INVARIANTS
        ):
            raise CarverBlocked("S27 v2 PnL invariant dependencies must match locked invariants")
        seen_invariants: set[str] = set()
        for binding in self.invariant_dependency_bindings:
            binding.validate_invariant()
            if binding.dependency_label in seen_invariants:
                raise CarverBlocked("S27 v2 PnL invariant dependency bindings must be unique")
            seen_invariants.add(binding.dependency_label)
            self._require_matching_dependency_hashes(binding, dependency_hash_by_label)

    def _require_matching_dependency_hashes(
        self,
        binding: PnlDependencyBindingContract,
        dependency_hash_by_label: dict[str, str],
    ) -> None:
        require_matching_dependency_hashes(
            "S27 v2 PnL",
            binding.required_dependency_labels,
            binding.required_dependency_contract_hashes,
            dependency_hash_by_label,
        )

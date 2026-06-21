from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest
from .level_compatibility_contract import LevelCompatibilityContractBundle
from .level_compatibility_input_contract import (
    REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
    LevelCompatibilityInputContractBundle,
)
from .parser_output_contract import ParserOutputBatchSetContract
from .runtime_history_contract import REQUIRED_RUNTIME_STATE_FAMILIES, REQUIRED_VQM_COMPONENTS
from .source_input_manifest_contract import (
    REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS,
    REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD,
    SourceInputManifestContractBundle,
)
from .source_input_selection_contract import (
    REQUIRED_SOURCE_INPUT_ROLES,
    SourceRowSelectionExternalAuthorityHandle,
)
from .source_row_batch_contract import REQUIRED_SOURCE_ROW_BATCH_FAMILIES, SourceRowBatchSetContract
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


S27_V2_RUNTIME_HISTORY_INPUT_CONTRACT_ONLY_STATUS = "S27_V2_RUNTIME_HISTORY_INPUT_CONTRACT_ONLY"
PLANNED_RUNTIME_HISTORY_INPUT_STATUS = "PLANNED_RUNTIME_HISTORY_INPUT_ONLY"

REQUIRED_RUNTIME_HISTORY_INPUTS = (
    "RUNTIME_DAILY_CONTINUOUS_EQUILIBRIUM_INPUT",
    "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT",
    "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT",
    "RUNTIME_HOURLY_DECISION_PRICE_INPUT",
    "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
    "RUNTIME_ROLL_CALENDAR_CONTEXT_INPUT",
)

REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT = {
    "RUNTIME_DAILY_CONTINUOUS_EQUILIBRIUM_INPUT": "DAILY_CONTINUOUS_ROW_HASH",
    "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT": "DAILY_CURRENT_CONTRACT_ROW_HASH",
    "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT": "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_HASH",
    "RUNTIME_HOURLY_DECISION_PRICE_INPUT": "HOURLY_DECISION_ROW_HASH",
    "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT": "SESSION_CALENDAR_CONTEXT_HASH",
    "RUNTIME_ROLL_CALENDAR_CONTEXT_INPUT": "ROLL_CALENDAR_CONTEXT_HASH",
}

REQUIRED_LEVEL_COMPATIBILITY_INPUT_BY_RUNTIME_HISTORY_INPUT = {
    "RUNTIME_DAILY_CONTINUOUS_EQUILIBRIUM_INPUT": "LEVEL_COMPAT_DAILY_CONTINUOUS_INPUT",
    "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT": "LEVEL_COMPAT_DAILY_CURRENT_CONTRACT_INPUT",
    "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT": "LEVEL_COMPAT_PREVIOUS_CURRENT_CLOSE_INPUT",
    "RUNTIME_HOURLY_DECISION_PRICE_INPUT": "LEVEL_COMPAT_HOURLY_DECISION_INPUT",
}

REQUIRED_RUNTIME_HISTORY_INPUTS_BY_STATE = {
    "EWMA5_EQUILIBRIUM_STATE": (
        "RUNTIME_DAILY_CONTINUOUS_EQUILIBRIUM_INPUT",
        "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
        "RUNTIME_ROLL_CALENDAR_CONTEXT_INPUT",
    ),
    "EWMAC16_64_TREND_STATE": (
        "RUNTIME_DAILY_CONTINUOUS_EQUILIBRIUM_INPUT",
        "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
        "RUNTIME_ROLL_CALENDAR_CONTEXT_INPUT",
    ),
    "SIGMA_ESTIMATOR_STATE": (
        "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT",
        "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT",
        "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
    ),
    "VQM_HISTORY_STATE": (
        "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT",
        "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT",
        "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
    ),
    "TEN_YEAR_ROLLING_MEAN_PERCENTAGE_SIGMA_STATE": (
        "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT",
        "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT",
        "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
    ),
    "EXPANDING_RELATIVE_VOLATILITY_DISTRIBUTION_STATE": (
        "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT",
        "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT",
        "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
    ),
    "PRIOR_EWMA10_MULTIPLIER_STATE": (
        "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT",
        "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT",
        "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
    ),
}

REQUIRED_RUNTIME_HISTORY_DEPENDENCIES_BY_VQM_COMPONENT = {
    "RELATIVE_VOLATILITY_V": (
        "SIGMA_ESTIMATOR_STATE",
        "TEN_YEAR_ROLLING_MEAN_PERCENTAGE_SIGMA_STATE",
    ),
    "EXPANDING_QUANTILE_Q": (
        "RELATIVE_VOLATILITY_V",
        "EXPANDING_RELATIVE_VOLATILITY_DISTRIBUTION_STATE",
    ),
    "RAW_VOLATILITY_MULTIPLIER": ("EXPANDING_QUANTILE_Q",),
    "EWMA10_MULTIPLIER_M": (
        "RAW_VOLATILITY_MULTIPLIER",
        "PRIOR_EWMA10_MULTIPLIER_STATE",
    ),
}


@dataclass(frozen=True)
class RuntimeHistoryInputFieldContract:
    input_label: str
    input_status: str
    source_input_manifest_field: str
    source_input_role: str
    source_input_manifest_field_contract_hash: str
    selected_row_hash: str
    selected_row_locator_hash: str
    runtime_history_input_policy_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    no_future_rows_proof_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 runtime history input label", self.input_label)
        if self.input_label not in REQUIRED_RUNTIME_HISTORY_INPUTS:
            raise CarverBlocked("S27 v2 runtime history input label is not locked")
        require_text("S27 v2 runtime history input status", self.input_status)
        if self.input_status != PLANNED_RUNTIME_HISTORY_INPUT_STATUS:
            raise CarverBlocked("S27 v2 runtime history input must remain planned-only")
        require_text(
            "S27 v2 runtime history source input manifest field",
            self.source_input_manifest_field,
        )
        if self.source_input_manifest_field not in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS:
            raise CarverBlocked("S27 v2 runtime history manifest field is not locked")
        if (
            self.source_input_manifest_field
            != REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[self.input_label]
        ):
            raise CarverBlocked("S27 v2 runtime history input must use the locked manifest field")
        require_text("S27 v2 runtime history source input role", self.source_input_role)
        if self.source_input_role not in REQUIRED_SOURCE_INPUT_ROLES:
            raise CarverBlocked("S27 v2 runtime history source input role is not locked")
        if (
            self.source_input_role
            != REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[self.source_input_manifest_field]
        ):
            raise CarverBlocked("S27 v2 runtime history input must use the locked source-input role")
        require_hash(
            "S27 v2 runtime history source-input manifest field contract hash",
            self.source_input_manifest_field_contract_hash,
        )
        require_hash("S27 v2 runtime history selected row hash", self.selected_row_hash)
        require_hash("S27 v2 runtime history selected row locator hash", self.selected_row_locator_hash)
        require_hash("S27 v2 runtime history input policy hash", self.runtime_history_input_policy_hash)
        require_hash("S27 v2 runtime history completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 runtime history strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 runtime history no-future-rows proof hash", self.no_future_rows_proof_hash)
        require_hash("S27 v2 runtime history input field contract hash", self.input_field_contract_hash)


@dataclass(frozen=True)
class RuntimeHistoryLevelCompatibilityInputBindingContract:
    runtime_input_label: str
    level_compatibility_input_label: str
    runtime_input_field_contract_hash: str
    level_compatibility_input_field_contract_hash: str
    level_compatibility_input_binding_policy_hash: str
    level_compatibility_input_binding_contract_hash: str

    def validate(self) -> None:
        require_text(
            "S27 v2 runtime history level-compatibility runtime input label",
            self.runtime_input_label,
        )
        if self.runtime_input_label not in REQUIRED_LEVEL_COMPATIBILITY_INPUT_BY_RUNTIME_HISTORY_INPUT:
            raise CarverBlocked("S27 v2 runtime history level-compatibility runtime input is not locked")
        require_text(
            "S27 v2 runtime history level-compatibility input label",
            self.level_compatibility_input_label,
        )
        if self.level_compatibility_input_label not in REQUIRED_LEVEL_COMPATIBILITY_INPUTS:
            raise CarverBlocked("S27 v2 runtime history level-compatibility input is not locked")
        if (
            self.level_compatibility_input_label
            != REQUIRED_LEVEL_COMPATIBILITY_INPUT_BY_RUNTIME_HISTORY_INPUT[self.runtime_input_label]
        ):
            raise CarverBlocked(
                "S27 v2 runtime history input must use the locked level-compatibility input"
            )
        require_hash(
            "S27 v2 runtime history runtime input field contract hash",
            self.runtime_input_field_contract_hash,
        )
        require_hash(
            "S27 v2 runtime history level-compatibility input field contract hash",
            self.level_compatibility_input_field_contract_hash,
        )
        require_hash(
            "S27 v2 runtime history level-compatibility input binding policy hash",
            self.level_compatibility_input_binding_policy_hash,
        )
        require_hash(
            "S27 v2 runtime history level-compatibility input binding contract hash",
            self.level_compatibility_input_binding_contract_hash,
        )


@dataclass(frozen=True)
class RuntimeHistoryStateInputBindingContract:
    state_family: str
    required_runtime_input_labels: tuple[str, ...]
    required_runtime_input_field_contract_hashes: tuple[str, ...]
    state_input_binding_policy_hash: str
    state_input_binding_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 runtime history state input family", self.state_family)
        if self.state_family not in REQUIRED_RUNTIME_STATE_FAMILIES:
            raise CarverBlocked("S27 v2 runtime history state input family is not locked")
        require_non_empty_tuple(
            "S27 v2 runtime history state required input labels",
            self.required_runtime_input_labels,
        )
        if self.required_runtime_input_labels != REQUIRED_RUNTIME_HISTORY_INPUTS_BY_STATE[self.state_family]:
            raise CarverBlocked("S27 v2 runtime history state inputs must match locked input tuple")
        require_non_empty_tuple(
            "S27 v2 runtime history state required input field contract hashes",
            self.required_runtime_input_field_contract_hashes,
        )
        if len(self.required_runtime_input_field_contract_hashes) != len(self.required_runtime_input_labels):
            raise CarverBlocked("S27 v2 runtime history state input hashes must match input labels")
        for input_hash in self.required_runtime_input_field_contract_hashes:
            require_hash("S27 v2 runtime history state input field contract hash", input_hash)
        require_hash(
            "S27 v2 runtime history state input binding policy hash",
            self.state_input_binding_policy_hash,
        )
        require_hash(
            "S27 v2 runtime history state input binding contract hash",
            self.state_input_binding_contract_hash,
        )


@dataclass(frozen=True)
class RuntimeHistoryVqmDependencyBindingContract:
    component_label: str
    required_runtime_dependency_labels: tuple[str, ...]
    required_runtime_dependency_contract_hashes: tuple[str, ...]
    vqm_dependency_binding_policy_hash: str
    vqm_dependency_binding_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 runtime history V/Q/M dependency component", self.component_label)
        if self.component_label not in REQUIRED_VQM_COMPONENTS:
            raise CarverBlocked("S27 v2 runtime history V/Q/M component is not locked")
        require_non_empty_tuple(
            "S27 v2 runtime history V/Q/M dependency labels",
            self.required_runtime_dependency_labels,
        )
        if (
            self.required_runtime_dependency_labels
            != REQUIRED_RUNTIME_HISTORY_DEPENDENCIES_BY_VQM_COMPONENT[self.component_label]
        ):
            raise CarverBlocked("S27 v2 runtime history V/Q/M dependencies must match locked tuple")
        require_non_empty_tuple(
            "S27 v2 runtime history V/Q/M dependency contract hashes",
            self.required_runtime_dependency_contract_hashes,
        )
        if len(self.required_runtime_dependency_contract_hashes) != len(
            self.required_runtime_dependency_labels
        ):
            raise CarverBlocked("S27 v2 runtime history V/Q/M dependency hashes must match labels")
        for dependency_hash in self.required_runtime_dependency_contract_hashes:
            require_hash("S27 v2 runtime history V/Q/M dependency contract hash", dependency_hash)
        require_hash(
            "S27 v2 runtime history V/Q/M dependency binding policy hash",
            self.vqm_dependency_binding_policy_hash,
        )
        require_hash(
            "S27 v2 runtime history V/Q/M dependency binding contract hash",
            self.vqm_dependency_binding_contract_hash,
        )


@dataclass(frozen=True)
class RuntimeHistoryInputContractBundle:
    status: str
    source_input_manifest_contract_hash: str
    source_input_manifest_hash: str
    level_compatibility_input_contract_hash: str
    level_compatibility_contract_hash: str
    runtime_history_input_policy_hash: str
    source_input_manifest_contract_bundle: SourceInputManifestContractBundle
    input_field_contracts: tuple[RuntimeHistoryInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    expected_selected_row_hash_by_input_label: dict[str, str]
    expected_selected_row_locator_hash_by_input_label: dict[str, str]
    level_compatibility_input_bindings: tuple[
        RuntimeHistoryLevelCompatibilityInputBindingContract, ...
    ]
    state_input_binding_contracts: tuple[RuntimeHistoryStateInputBindingContract, ...]
    vqm_dependency_binding_contracts: tuple[RuntimeHistoryVqmDependencyBindingContract, ...]
    runtime_history_input_set_hash: str
    runtime_history_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 runtime history input requires active trust authority"
        )

    def validate_against_active_trust_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
        level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
        level_compatibility_contract: LevelCompatibilityContractBundle,
    ) -> None:
        self._validate_contract_only_shape(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
            level_compatibility_input_contract,
            level_compatibility_contract,
        )

    def _validate_contract_only_shape(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
        level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
        level_compatibility_contract: LevelCompatibilityContractBundle,
    ) -> None:
        require_text("S27 v2 runtime history input contract status", self.status)
        if self.status != S27_V2_RUNTIME_HISTORY_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 runtime history input contract must remain contract-only")
        if tuple(REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT) != REQUIRED_RUNTIME_HISTORY_INPUTS:
            raise CarverBlocked("S27 v2 runtime history input map must cover the locked input tuple")
        if tuple(REQUIRED_RUNTIME_HISTORY_INPUTS_BY_STATE) != REQUIRED_RUNTIME_STATE_FAMILIES:
            raise CarverBlocked("S27 v2 runtime history state-input map must cover locked states")
        if tuple(REQUIRED_RUNTIME_HISTORY_DEPENDENCIES_BY_VQM_COMPONENT) != REQUIRED_VQM_COMPONENTS:
            raise CarverBlocked("S27 v2 runtime history V/Q/M dependency map must cover locked components")
        require_hash(
            "S27 v2 runtime history source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash("S27 v2 runtime history source-input manifest hash", self.source_input_manifest_hash)
        require_hash(
            "S27 v2 runtime history level-compatibility input contract hash",
            self.level_compatibility_input_contract_hash,
        )
        require_hash(
            "S27 v2 runtime history level-compatibility contract hash",
            self.level_compatibility_contract_hash,
        )
        require_hash("S27 v2 runtime history input policy hash", self.runtime_history_input_policy_hash)
        self._validate_source_input_manifest_bundle_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )
        self._validate_level_compatibility_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
            level_compatibility_input_contract,
            level_compatibility_contract,
        )
        require_hash_map(
            "S27 v2 runtime history expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_RUNTIME_HISTORY_INPUTS,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 runtime history expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(),
            REQUIRED_RUNTIME_HISTORY_INPUTS,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 runtime history selected-row hash map",
            self.expected_selected_row_hash_by_input_label,
            self._active_selected_row_hash_by_input_label(),
            REQUIRED_RUNTIME_HISTORY_INPUTS,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 runtime history selected-row-locator hash map",
            self.expected_selected_row_locator_hash_by_input_label,
            self._active_selected_row_locator_hash_by_input_label(),
            REQUIRED_RUNTIME_HISTORY_INPUTS,
        )
        require_non_empty_tuple("S27 v2 runtime history input field contracts", self.input_field_contracts)
        input_contract_hash_by_label: dict[str, str] = {}
        seen_inputs: set[str] = set()
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 runtime history input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 runtime history input source contract hash",
                contract.input_label,
                contract.source_input_manifest_field_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            require_expected_hash(
                "S27 v2 runtime history selected row hash",
                contract.input_label,
                contract.selected_row_hash,
                self.expected_selected_row_hash_by_input_label,
            )
            require_expected_hash(
                "S27 v2 runtime history selected row locator hash",
                contract.input_label,
                contract.selected_row_locator_hash,
                self.expected_selected_row_locator_hash_by_input_label,
            )
            input_contract_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if tuple(contract.input_label for contract in self.input_field_contracts) != REQUIRED_RUNTIME_HISTORY_INPUTS:
            raise CarverBlocked("S27 v2 runtime history inputs must match the locked input tuple")
        require_non_empty_tuple(
            "S27 v2 runtime history level-compatibility input bindings",
            self.level_compatibility_input_bindings,
        )
        seen_level_compat_inputs: set[str] = set()
        level_compatibility_input_hash_by_label = (
            self._level_compatibility_input_field_contract_hash_by_label(
                level_compatibility_input_contract,
            )
        )
        for binding in self.level_compatibility_input_bindings:
            binding.validate()
            if binding.runtime_input_label in seen_level_compat_inputs:
                raise CarverBlocked("S27 v2 runtime history level-compatibility bindings must be unique")
            seen_level_compat_inputs.add(binding.runtime_input_label)
            require_matching_dependency_hashes(
                "S27 v2 runtime history level-compatibility input",
                (binding.runtime_input_label,),
                (binding.runtime_input_field_contract_hash,),
                input_contract_hash_by_label,
            )
            require_expected_hash(
                "S27 v2 runtime history level-compatibility field contract hash",
                binding.level_compatibility_input_label,
                binding.level_compatibility_input_field_contract_hash,
                level_compatibility_input_hash_by_label,
            )
        if (
            tuple(binding.runtime_input_label for binding in self.level_compatibility_input_bindings)
            != tuple(REQUIRED_LEVEL_COMPATIBILITY_INPUT_BY_RUNTIME_HISTORY_INPUT)
        ):
            raise CarverBlocked(
                "S27 v2 runtime history level-compatibility bindings must match locked tuple"
            )
        require_non_empty_tuple(
            "S27 v2 runtime history state input binding contracts",
            self.state_input_binding_contracts,
        )
        state_contract_hash_by_family: dict[str, str] = {}
        seen_states: set[str] = set()
        for binding in self.state_input_binding_contracts:
            binding.validate()
            if binding.state_family in seen_states:
                raise CarverBlocked("S27 v2 runtime history state input bindings must be unique")
            seen_states.add(binding.state_family)
            require_matching_dependency_hashes(
                "S27 v2 runtime history state input",
                binding.required_runtime_input_labels,
                binding.required_runtime_input_field_contract_hashes,
                input_contract_hash_by_label,
            )
            state_contract_hash_by_family[binding.state_family] = binding.state_input_binding_contract_hash
        if (
            tuple(binding.state_family for binding in self.state_input_binding_contracts)
            != REQUIRED_RUNTIME_STATE_FAMILIES
        ):
            raise CarverBlocked("S27 v2 runtime history state input bindings must match locked states")
        require_non_empty_tuple(
            "S27 v2 runtime history V/Q/M dependency binding contracts",
            self.vqm_dependency_binding_contracts,
        )
        if (
            tuple(binding.component_label for binding in self.vqm_dependency_binding_contracts)
            != REQUIRED_VQM_COMPONENTS
        ):
            raise CarverBlocked("S27 v2 runtime history V/Q/M dependency bindings must match components")
        dependency_contract_hash_by_label: dict[str, str] = dict(state_contract_hash_by_family)
        seen_components: set[str] = set()
        for binding in self.vqm_dependency_binding_contracts:
            binding.validate()
            if binding.component_label in seen_components:
                raise CarverBlocked("S27 v2 runtime history V/Q/M dependency bindings must be unique")
            seen_components.add(binding.component_label)
            require_matching_dependency_hashes(
                "S27 v2 runtime history V/Q/M",
                binding.required_runtime_dependency_labels,
                binding.required_runtime_dependency_contract_hashes,
                dependency_contract_hash_by_label,
            )
            dependency_contract_hash_by_label[binding.component_label] = (
                binding.vqm_dependency_binding_contract_hash
            )
        require_hash("S27 v2 runtime history input set hash", self.runtime_history_input_set_hash)
        require_hash("S27 v2 runtime history input contract hash", self.runtime_history_input_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 runtime history input contract must preserve non-authorizations")

    def _active_source_contract_hash_by_input_label(self) -> dict[str, str]:
        manifest_field_contract_hash_by_field = self._manifest_field_contract_hash_by_field()
        return {
            input_label: manifest_field_contract_hash_by_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ]
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        }

    def _active_selected_row_hash_by_input_label(self) -> dict[str, str]:
        return {
            input_label: self.source_input_manifest_contract_bundle.expected_selected_row_hash_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ]
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        }

    def _active_selected_row_locator_hash_by_input_label(self) -> dict[str, str]:
        return {
            input_label: self.source_input_manifest_contract_bundle.expected_selected_row_locator_hash_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_RUNTIME_HISTORY_INPUT[input_label]
            ]
            for input_label in REQUIRED_RUNTIME_HISTORY_INPUTS
        }

    def _validate_source_input_manifest_bundle_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        self.source_input_manifest_contract_bundle.validate_against_active_trust_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )
        if (
            self.source_input_manifest_contract_bundle.source_input_manifest_contract_hash
            != self.source_input_manifest_contract_hash
        ):
            raise CarverBlocked("S27 v2 runtime history must bind cited source-input manifest contract")
        if self.source_input_manifest_contract_bundle.source_input_manifest_hash != self.source_input_manifest_hash:
            raise CarverBlocked("S27 v2 runtime history must bind cited source-input manifest hash")

    def _validate_level_compatibility_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
        level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
        level_compatibility_contract: LevelCompatibilityContractBundle,
    ) -> None:
        level_compatibility_input_contract.validate_against_active_trust_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )
        level_compatibility_contract.validate()
        if (
            level_compatibility_input_contract.level_compatibility_input_contract_hash
            != self.level_compatibility_input_contract_hash
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility input contract")
        if (
            level_compatibility_contract.level_compatibility_contract_bundle_hash
            != self.level_compatibility_contract_hash
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility contract bundle")
        if (
            level_compatibility_input_contract.source_input_manifest_contract_hash
            != self.source_input_manifest_contract_hash
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility source manifest contract")
        if level_compatibility_input_contract.source_input_manifest_hash != self.source_input_manifest_hash:
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility source manifest hash")
        if (
            level_compatibility_contract.source_binding.source_universe_contract_hash
            != source_row_selection_external_authority.source_universe_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility source universe")
        if (
            level_compatibility_contract.daily_hourly_level_compatibility_policy_hash
            != replay_trust_root.daily_hourly_level_compatibility_policy_hash
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility trust-root policy")
        source_row_family_hash_by_family = self._source_row_batch_family_contract_hash_by_family(
            source_row_batch_contract,
        )
        if (
            level_compatibility_contract.source_binding.daily_continuous_row_family_hash
            != source_row_family_hash_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"]
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility daily continuous family")
        if (
            level_compatibility_contract.source_binding.daily_current_contract_row_family_hash
            != source_row_family_hash_by_family["DAILY_CURRENT_CONTRACT_COMPLETED_BAR"]
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility daily current family")
        if (
            level_compatibility_contract.source_binding.previous_completed_current_contract_close_family_hash
            != source_row_family_hash_by_family["DAILY_CURRENT_CONTRACT_COMPLETED_BAR"]
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility previous close family")
        if (
            level_compatibility_contract.source_binding.hourly_decision_row_family_hash
            != source_row_family_hash_by_family["HOURLY_DECISION_COMPLETED_BAR"]
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility hourly decision family")
        if (
            level_compatibility_contract.source_binding.hourly_fill_row_family_hash
            != source_row_family_hash_by_family["HOURLY_FILL_COMPLETED_BAR"]
        ):
            raise CarverBlocked("S27 v2 runtime history must bind level-compatibility hourly fill family")

    def _level_compatibility_input_field_contract_hash_by_label(
        self,
        level_compatibility_input_contract: LevelCompatibilityInputContractBundle,
    ) -> dict[str, str]:
        input_hash_by_label = {
            contract.input_label: contract.input_field_contract_hash
            for contract in level_compatibility_input_contract.input_field_contracts
        }
        if tuple(input_hash_by_label) != REQUIRED_LEVEL_COMPATIBILITY_INPUTS:
            raise CarverBlocked("S27 v2 runtime history level-compatibility inputs must match locked tuple")
        return input_hash_by_label

    def _source_row_batch_family_contract_hash_by_family(
        self,
        source_row_batch_contract: SourceRowBatchSetContract,
    ) -> dict[str, str]:
        family_hash_by_family = {
            contract.row_family: contract.source_row_batch_family_contract_hash
            for contract in source_row_batch_contract.source_row_batch_family_contracts
        }
        if tuple(family_hash_by_family) != REQUIRED_SOURCE_ROW_BATCH_FAMILIES:
            raise CarverBlocked("S27 v2 runtime history source-row batch families must match locked tuple")
        return family_hash_by_family

    def _manifest_field_contract_hash_by_field(self) -> dict[str, str]:
        manifest_field_contract_hash_by_field = {
            contract.manifest_field: contract.manifest_field_contract_hash
            for contract in self.source_input_manifest_contract_bundle.manifest_field_contracts
        }
        if tuple(manifest_field_contract_hash_by_field) != REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS:
            raise CarverBlocked("S27 v2 runtime history manifest field contracts must match locked fields")
        return manifest_field_contract_hash_by_field

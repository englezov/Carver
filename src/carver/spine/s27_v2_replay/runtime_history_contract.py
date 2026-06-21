from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_RUNTIME_HISTORY_CONTRACT_ONLY_STATUS = "S27_V2_RUNTIME_HISTORY_CONTRACT_ONLY"
PLANNED_RUNTIME_HISTORY_STATE_STATUS = "PLANNED_RUNTIME_HISTORY_STATE_ONLY"

REQUIRED_RUNTIME_STATE_FAMILIES = (
    "EWMA5_EQUILIBRIUM_STATE",
    "EWMAC16_64_TREND_STATE",
    "SIGMA_ESTIMATOR_STATE",
    "VQM_HISTORY_STATE",
    "TEN_YEAR_ROLLING_MEAN_PERCENTAGE_SIGMA_STATE",
    "EXPANDING_RELATIVE_VOLATILITY_DISTRIBUTION_STATE",
    "PRIOR_EWMA10_MULTIPLIER_STATE",
)

REQUIRED_VQM_COMPONENTS = (
    "RELATIVE_VOLATILITY_V",
    "EXPANDING_QUANTILE_Q",
    "RAW_VOLATILITY_MULTIPLIER",
    "EWMA10_MULTIPLIER_M",
)


@dataclass(frozen=True)
class RuntimeHistorySourceBinding:
    source_input_manifest_hash: str
    level_compatibility_contract_hash: str
    daily_continuous_row_family_hash: str
    daily_current_contract_row_family_hash: str
    hourly_decision_row_family_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    source_binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 runtime source input manifest hash", self.source_input_manifest_hash)
        require_hash(
            "S27 v2 runtime level compatibility contract hash",
            self.level_compatibility_contract_hash,
        )
        require_hash("S27 v2 runtime daily continuous row family hash", self.daily_continuous_row_family_hash)
        require_hash(
            "S27 v2 runtime daily current-contract row family hash",
            self.daily_current_contract_row_family_hash,
        )
        require_hash("S27 v2 runtime hourly decision row family hash", self.hourly_decision_row_family_hash)
        require_hash("S27 v2 runtime completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 runtime strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 runtime source binding hash", self.source_binding_hash)


@dataclass(frozen=True)
class RuntimeStateFamilyContract:
    state_family: str
    state_status: str
    required_input_hashes: tuple[str, ...]
    state_definition_hash: str
    state_policy_hash: str
    planned_state_output_hash: str
    state_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 runtime state family", self.state_family)
        if self.state_family not in REQUIRED_RUNTIME_STATE_FAMILIES:
            raise CarverBlocked("S27 v2 runtime state family is not locked")
        require_text("S27 v2 runtime state status", self.state_status)
        if self.state_status != PLANNED_RUNTIME_HISTORY_STATE_STATUS:
            raise CarverBlocked("S27 v2 runtime state must remain planned-only")
        require_non_empty_tuple("S27 v2 runtime state input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 runtime state input hash", input_hash)
        require_hash("S27 v2 runtime state definition hash", self.state_definition_hash)
        require_hash("S27 v2 runtime state policy hash", self.state_policy_hash)
        require_hash("S27 v2 runtime planned state output hash", self.planned_state_output_hash)
        require_hash("S27 v2 runtime state contract hash", self.state_contract_hash)


@dataclass(frozen=True)
class VqmComponentContract:
    component_label: str
    required_input_hashes: tuple[str, ...]
    component_policy_hash: str
    planned_component_output_hash: str
    component_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 V/Q/M component label", self.component_label)
        if self.component_label not in REQUIRED_VQM_COMPONENTS:
            raise CarverBlocked("S27 v2 V/Q/M component label is not locked")
        require_non_empty_tuple("S27 v2 V/Q/M component input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 V/Q/M component input hash", input_hash)
        require_hash("S27 v2 V/Q/M component policy hash", self.component_policy_hash)
        require_hash("S27 v2 V/Q/M planned component output hash", self.planned_component_output_hash)
        require_hash("S27 v2 V/Q/M component contract hash", self.component_contract_hash)


@dataclass(frozen=True)
class RuntimeHistoryContractBundle:
    status: str
    source_binding: RuntimeHistorySourceBinding
    state_contracts: tuple[RuntimeStateFamilyContract, ...]
    vqm_component_contracts: tuple[VqmComponentContract, ...]
    sigma_estimator_definition_hash: str
    sigma_input_window_policy_hash: str
    sigma_annualization_policy_hash: str
    runtime_history_ledger_schema_hash: str
    runtime_history_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 runtime history contract status", self.status)
        if self.status != S27_V2_RUNTIME_HISTORY_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 runtime history contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 runtime state contracts", self.state_contracts)
        seen_states: set[str] = set()
        for state_contract in self.state_contracts:
            state_contract.validate()
            if state_contract.state_family in seen_states:
                raise CarverBlocked("S27 v2 runtime state contracts must be unique")
            seen_states.add(state_contract.state_family)
        if tuple(contract.state_family for contract in self.state_contracts) != REQUIRED_RUNTIME_STATE_FAMILIES:
            raise CarverBlocked("S27 v2 runtime state contracts must match locked state tuple")
        require_non_empty_tuple("S27 v2 V/Q/M component contracts", self.vqm_component_contracts)
        seen_components: set[str] = set()
        for component_contract in self.vqm_component_contracts:
            component_contract.validate()
            if component_contract.component_label in seen_components:
                raise CarverBlocked("S27 v2 V/Q/M component contracts must be unique")
            seen_components.add(component_contract.component_label)
        if tuple(contract.component_label for contract in self.vqm_component_contracts) != REQUIRED_VQM_COMPONENTS:
            raise CarverBlocked("S27 v2 V/Q/M component contracts must match locked component tuple")
        require_hash("S27 v2 runtime sigma estimator definition hash", self.sigma_estimator_definition_hash)
        require_hash("S27 v2 runtime sigma input window policy hash", self.sigma_input_window_policy_hash)
        require_hash("S27 v2 runtime sigma annualization policy hash", self.sigma_annualization_policy_hash)
        require_hash("S27 v2 runtime history ledger schema hash", self.runtime_history_ledger_schema_hash)
        require_hash(
            "S27 v2 runtime history contract bundle hash",
            self.runtime_history_contract_bundle_hash,
        )
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 runtime history contract must preserve non-authorizations")

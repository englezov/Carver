from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_FORECAST_CONTRACT_ONLY_STATUS = "S27_V2_FORECAST_CONTRACT_ONLY"
PLANNED_FORECAST_COMPONENT_STATUS = "PLANNED_FORECAST_COMPONENT_ONLY"

REQUIRED_FORECAST_COMPONENT_FAMILIES = (
    "RAW_MEAN_REVERSION_FORECAST",
    "SIGMA_PRICE_BRIDGE",
    "RISK_ADJUSTED_FORECAST_PRE_TREND_VETO",
    "EWMAC16_64_TREND_GATE",
    "VQM_MULTIPLIER_APPLICATION",
    "SCALAR_AND_CAP_APPLICATION",
    "DESIRED_POSITION_REFERENCE",
)

REQUIRED_FORECAST_DECISION_BRANCHES = (
    "PERMIT_MEAN_REVERSION",
    "ZERO_FORECAST_BY_TREND_VETO",
    "FLAT_AT_EQUILIBRIUM",
)

REQUIRED_FORECAST_INVARIANTS = (
    "STRICT_PRIOR_RUNTIME_INPUTS",
    "COMPLETED_BAR_FORECAST_TIMESTAMP",
    "POSITIVE_SIGMA_AND_PRICE_INPUTS",
    "ZERO_EQUILIBRIUM_FLAT_BRANCH",
    "TREND_VETO_SIGN_GATE",
    "POST_VETO_VQM_MULTIPLIER_BINDING",
    "SCALAR_CAP_BINDING",
    "DESIRED_POSITION_REFERENCE_BINDING",
)


@dataclass(frozen=True)
class ForecastSourceBinding:
    source_input_manifest_hash: str
    runtime_history_contract_bundle_hash: str
    runtime_history_ledger_schema_hash: str
    forecast_ledger_schema_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    forecast_source_binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 forecast source input manifest hash", self.source_input_manifest_hash)
        require_hash(
            "S27 v2 forecast runtime-history contract bundle hash",
            self.runtime_history_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 forecast runtime-history ledger schema hash",
            self.runtime_history_ledger_schema_hash,
        )
        require_hash("S27 v2 forecast ledger schema hash", self.forecast_ledger_schema_hash)
        require_hash("S27 v2 forecast completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 forecast strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 forecast source binding hash", self.forecast_source_binding_hash)


@dataclass(frozen=True)
class ForecastComponentContract:
    component_family: str
    component_status: str
    required_input_hashes: tuple[str, ...]
    component_definition_hash: str
    component_policy_hash: str
    planned_component_output_hash: str
    component_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 forecast component family", self.component_family)
        if self.component_family not in REQUIRED_FORECAST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 forecast component family is not locked")
        require_text("S27 v2 forecast component status", self.component_status)
        if self.component_status != PLANNED_FORECAST_COMPONENT_STATUS:
            raise CarverBlocked("S27 v2 forecast component must remain planned-only")
        require_non_empty_tuple("S27 v2 forecast component input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 forecast component input hash", input_hash)
        require_hash("S27 v2 forecast component definition hash", self.component_definition_hash)
        require_hash("S27 v2 forecast component policy hash", self.component_policy_hash)
        require_hash("S27 v2 forecast planned component output hash", self.planned_component_output_hash)
        require_hash("S27 v2 forecast component contract hash", self.component_contract_hash)


@dataclass(frozen=True)
class ForecastDecisionBranchContract:
    branch_label: str
    required_input_hashes: tuple[str, ...]
    branch_policy_hash: str
    planned_branch_output_hash: str
    branch_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 forecast decision branch label", self.branch_label)
        if self.branch_label not in REQUIRED_FORECAST_DECISION_BRANCHES:
            raise CarverBlocked("S27 v2 forecast decision branch label is not locked")
        require_non_empty_tuple("S27 v2 forecast decision branch input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 forecast decision branch input hash", input_hash)
        require_hash("S27 v2 forecast decision branch policy hash", self.branch_policy_hash)
        require_hash("S27 v2 forecast planned branch output hash", self.planned_branch_output_hash)
        require_hash("S27 v2 forecast decision branch contract hash", self.branch_contract_hash)


@dataclass(frozen=True)
class ForecastInvariantContract:
    invariant_label: str
    required_proof_hashes: tuple[str, ...]
    invariant_policy_hash: str
    invariant_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 forecast invariant label", self.invariant_label)
        if self.invariant_label not in REQUIRED_FORECAST_INVARIANTS:
            raise CarverBlocked("S27 v2 forecast invariant label is not locked")
        require_non_empty_tuple("S27 v2 forecast invariant proof hashes", self.required_proof_hashes)
        for proof_hash in self.required_proof_hashes:
            require_hash("S27 v2 forecast invariant proof hash", proof_hash)
        require_hash("S27 v2 forecast invariant policy hash", self.invariant_policy_hash)
        require_hash("S27 v2 forecast invariant contract hash", self.invariant_contract_hash)


@dataclass(frozen=True)
class ForecastContractBundle:
    status: str
    source_binding: ForecastSourceBinding
    component_contracts: tuple[ForecastComponentContract, ...]
    decision_branch_contracts: tuple[ForecastDecisionBranchContract, ...]
    invariant_contracts: tuple[ForecastInvariantContract, ...]
    scalar_source_lock_hash: str
    cap_policy_hash: str
    desired_position_link_policy_hash: str
    forecast_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 forecast contract status", self.status)
        if self.status != S27_V2_FORECAST_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 forecast contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 forecast component contracts", self.component_contracts)
        seen_components: set[str] = set()
        for component_contract in self.component_contracts:
            component_contract.validate()
            if component_contract.component_family in seen_components:
                raise CarverBlocked("S27 v2 forecast component contracts must be unique")
            seen_components.add(component_contract.component_family)
        if tuple(contract.component_family for contract in self.component_contracts) != REQUIRED_FORECAST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 forecast component contracts must match locked component tuple")
        require_non_empty_tuple("S27 v2 forecast decision branch contracts", self.decision_branch_contracts)
        seen_branches: set[str] = set()
        for branch_contract in self.decision_branch_contracts:
            branch_contract.validate()
            if branch_contract.branch_label in seen_branches:
                raise CarverBlocked("S27 v2 forecast decision branch contracts must be unique")
            seen_branches.add(branch_contract.branch_label)
        if tuple(contract.branch_label for contract in self.decision_branch_contracts) != REQUIRED_FORECAST_DECISION_BRANCHES:
            raise CarverBlocked("S27 v2 forecast decision branch contracts must match locked branch tuple")
        require_non_empty_tuple("S27 v2 forecast invariant contracts", self.invariant_contracts)
        seen_invariants: set[str] = set()
        for invariant_contract in self.invariant_contracts:
            invariant_contract.validate()
            if invariant_contract.invariant_label in seen_invariants:
                raise CarverBlocked("S27 v2 forecast invariant contracts must be unique")
            seen_invariants.add(invariant_contract.invariant_label)
        if tuple(contract.invariant_label for contract in self.invariant_contracts) != REQUIRED_FORECAST_INVARIANTS:
            raise CarverBlocked("S27 v2 forecast invariant contracts must match locked invariant tuple")
        require_hash("S27 v2 forecast scalar source-lock hash", self.scalar_source_lock_hash)
        require_hash("S27 v2 forecast cap policy hash", self.cap_policy_hash)
        require_hash("S27 v2 forecast desired-position link policy hash", self.desired_position_link_policy_hash)
        require_hash("S27 v2 forecast contract bundle hash", self.forecast_contract_bundle_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 forecast contract must preserve non-authorizations")

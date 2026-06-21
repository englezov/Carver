from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_FILL_CONTRACT_ONLY_STATUS = "S27_V2_FILL_CONTRACT_ONLY"
PLANNED_FILL_COMPONENT_STATUS = "PLANNED_FILL_COMPONENT_ONLY"

REQUIRED_FILL_COMPONENT_FAMILIES = (
    "ORDER_PLAN_REFERENCE",
    "WORKING_ORDER_TRANSITION_REFERENCE",
    "NEXT_COMPLETED_HOURLY_FILL_ROW",
    "LIMIT_FILL_PRICE_PROVENANCE",
    "MARKET_FILL_PRICE_PROVENANCE",
    "FILL_QUANTITY_AND_SIDE_BINDING",
)

REQUIRED_FILL_PRICE_PROVENANCE_LABELS = (
    "LIMIT_ORDER_PRICE_FROM_FILLED_ORDER",
    "MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE",
)

REQUIRED_FILL_BRANCH_LABELS = (
    "LIMIT_FILL",
    "MARKET_FILL",
)

REQUIRED_FILL_INVARIANTS = (
    "ORDER_CONTRACT_BUNDLE_HASH_BINDING",
    "TRANSITION_HASH_BINDING",
    "EXACT_NEXT_COMPLETED_HOURLY_ROW_BINDING",
    "FILL_TIMESTAMP_IDENTITY_BINDING",
    "LIMIT_FILL_PRICE_EQUALS_SUBMITTED_LIMIT",
    "MARKET_FILL_PRICE_FROM_NEXT_COMPLETED_CLOSE",
    "NO_COST_ACCOUNTING_IN_FILL_CONTRACT",
)


@dataclass(frozen=True)
class FillSourceBinding:
    source_input_manifest_hash: str
    order_contract_bundle_hash: str
    limit_order_ledger_schema_hash: str
    market_order_ledger_schema_hash: str
    working_order_transition_schema_hash: str
    fill_ledger_schema_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    fill_source_binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 fill source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 fill order contract bundle hash", self.order_contract_bundle_hash)
        require_hash("S27 v2 fill limit-order ledger schema hash", self.limit_order_ledger_schema_hash)
        require_hash("S27 v2 fill market-order ledger schema hash", self.market_order_ledger_schema_hash)
        require_hash(
            "S27 v2 fill working-order transition schema hash",
            self.working_order_transition_schema_hash,
        )
        require_hash("S27 v2 fill ledger schema hash", self.fill_ledger_schema_hash)
        require_hash("S27 v2 fill completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 fill strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 fill source binding hash", self.fill_source_binding_hash)


@dataclass(frozen=True)
class FillComponentContract:
    component_family: str
    component_status: str
    required_input_hashes: tuple[str, ...]
    component_definition_hash: str
    component_policy_hash: str
    planned_component_output_hash: str
    component_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 fill component family", self.component_family)
        if self.component_family not in REQUIRED_FILL_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 fill component family is not locked")
        require_text("S27 v2 fill component status", self.component_status)
        if self.component_status != PLANNED_FILL_COMPONENT_STATUS:
            raise CarverBlocked("S27 v2 fill component must remain planned-only")
        require_non_empty_tuple("S27 v2 fill component input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 fill component input hash", input_hash)
        require_hash("S27 v2 fill component definition hash", self.component_definition_hash)
        require_hash("S27 v2 fill component policy hash", self.component_policy_hash)
        require_hash("S27 v2 fill planned component output hash", self.planned_component_output_hash)
        require_hash("S27 v2 fill component contract hash", self.component_contract_hash)


@dataclass(frozen=True)
class FillPriceProvenanceContract:
    provenance_label: str
    required_policy_hashes: tuple[str, ...]
    provenance_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 fill price provenance label", self.provenance_label)
        if self.provenance_label not in REQUIRED_FILL_PRICE_PROVENANCE_LABELS:
            raise CarverBlocked("S27 v2 fill price provenance label is not locked")
        require_non_empty_tuple("S27 v2 fill price provenance policy hashes", self.required_policy_hashes)
        for policy_hash in self.required_policy_hashes:
            require_hash("S27 v2 fill price provenance policy hash", policy_hash)
        require_hash("S27 v2 fill price provenance contract hash", self.provenance_contract_hash)


@dataclass(frozen=True)
class FillBranchContract:
    branch_label: str
    required_input_hashes: tuple[str, ...]
    branch_policy_hash: str
    planned_branch_output_hash: str
    branch_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 fill branch label", self.branch_label)
        if self.branch_label not in REQUIRED_FILL_BRANCH_LABELS:
            raise CarverBlocked("S27 v2 fill branch label is not locked")
        require_non_empty_tuple("S27 v2 fill branch input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 fill branch input hash", input_hash)
        require_hash("S27 v2 fill branch policy hash", self.branch_policy_hash)
        require_hash("S27 v2 fill planned branch output hash", self.planned_branch_output_hash)
        require_hash("S27 v2 fill branch contract hash", self.branch_contract_hash)


@dataclass(frozen=True)
class FillInvariantContract:
    invariant_label: str
    required_proof_hashes: tuple[str, ...]
    invariant_policy_hash: str
    invariant_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 fill invariant label", self.invariant_label)
        if self.invariant_label not in REQUIRED_FILL_INVARIANTS:
            raise CarverBlocked("S27 v2 fill invariant label is not locked")
        require_non_empty_tuple("S27 v2 fill invariant proof hashes", self.required_proof_hashes)
        for proof_hash in self.required_proof_hashes:
            require_hash("S27 v2 fill invariant proof hash", proof_hash)
        require_hash("S27 v2 fill invariant policy hash", self.invariant_policy_hash)
        require_hash("S27 v2 fill invariant contract hash", self.invariant_contract_hash)


@dataclass(frozen=True)
class FillContractBundle:
    status: str
    source_binding: FillSourceBinding
    component_contracts: tuple[FillComponentContract, ...]
    price_provenance_contracts: tuple[FillPriceProvenanceContract, ...]
    branch_contracts: tuple[FillBranchContract, ...]
    invariant_contracts: tuple[FillInvariantContract, ...]
    one_hour_lag_policy_hash: str
    session_gap_policy_hash: str
    fill_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 fill contract status", self.status)
        if self.status != S27_V2_FILL_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 fill contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 fill component contracts", self.component_contracts)
        seen_components: set[str] = set()
        for component_contract in self.component_contracts:
            component_contract.validate()
            if component_contract.component_family in seen_components:
                raise CarverBlocked("S27 v2 fill component contracts must be unique")
            seen_components.add(component_contract.component_family)
        if tuple(contract.component_family for contract in self.component_contracts) != REQUIRED_FILL_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 fill component contracts must match locked component tuple")
        require_non_empty_tuple("S27 v2 fill price provenance contracts", self.price_provenance_contracts)
        seen_provenance: set[str] = set()
        for provenance_contract in self.price_provenance_contracts:
            provenance_contract.validate()
            if provenance_contract.provenance_label in seen_provenance:
                raise CarverBlocked("S27 v2 fill price provenance contracts must be unique")
            seen_provenance.add(provenance_contract.provenance_label)
        if tuple(
            contract.provenance_label for contract in self.price_provenance_contracts
        ) != REQUIRED_FILL_PRICE_PROVENANCE_LABELS:
            raise CarverBlocked("S27 v2 fill price provenance contracts must match locked provenance tuple")
        require_non_empty_tuple("S27 v2 fill branch contracts", self.branch_contracts)
        seen_branches: set[str] = set()
        for branch_contract in self.branch_contracts:
            branch_contract.validate()
            if branch_contract.branch_label in seen_branches:
                raise CarverBlocked("S27 v2 fill branch contracts must be unique")
            seen_branches.add(branch_contract.branch_label)
        if tuple(contract.branch_label for contract in self.branch_contracts) != REQUIRED_FILL_BRANCH_LABELS:
            raise CarverBlocked("S27 v2 fill branch contracts must match locked branch tuple")
        require_non_empty_tuple("S27 v2 fill invariant contracts", self.invariant_contracts)
        seen_invariants: set[str] = set()
        for invariant_contract in self.invariant_contracts:
            invariant_contract.validate()
            if invariant_contract.invariant_label in seen_invariants:
                raise CarverBlocked("S27 v2 fill invariant contracts must be unique")
            seen_invariants.add(invariant_contract.invariant_label)
        if tuple(contract.invariant_label for contract in self.invariant_contracts) != REQUIRED_FILL_INVARIANTS:
            raise CarverBlocked("S27 v2 fill invariant contracts must match locked invariant tuple")
        require_hash("S27 v2 fill one-hour lag policy hash", self.one_hour_lag_policy_hash)
        require_hash("S27 v2 fill session-gap policy hash", self.session_gap_policy_hash)
        require_hash("S27 v2 fill contract bundle hash", self.fill_contract_bundle_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 fill contract must preserve non-authorizations")

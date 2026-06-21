from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_ORDER_CONTRACT_ONLY_STATUS = "S27_V2_ORDER_CONTRACT_ONLY"
PLANNED_ORDER_COMPONENT_STATUS = "PLANNED_ORDER_COMPONENT_ONLY"

REQUIRED_ORDER_COMPONENT_FAMILIES = (
    "LIMIT_ORDER_PLAN",
    "MARKET_ORDER_PLAN",
    "ADJACENT_POSITION_LIMIT_LADDER",
    "TICK_ROUNDING_POLICY",
    "WORKING_ORDER_STATE_REFERENCE",
    "TRANSITION_KIND_REFERENCE",
)

REQUIRED_ORDER_KIND_LABELS = (
    "LIMIT",
    "MARKET",
)

REQUIRED_ORDER_TRANSITION_KIND_LABELS = (
    "NORMAL_ONE_HOUR_LAG",
    "EOD_OVERNIGHT_RECOMPUTE",
    "ROLL_BOUNDARY",
)

REQUIRED_ORDER_INVARIANTS = (
    "DESIRED_POSITION_LEDGER_HASH_BINDING",
    "CURRENT_POSITION_STATE_HASH_BINDING",
    "ADJACENT_LIMIT_SINGLE_LOT_BINDING",
    "MARKET_ORDER_DELTA_QUANTITY_BINDING",
    "TICK_ROUNDING_POLICY_BINDING",
    "NO_FILL_EXECUTION_IN_ORDER_CONTRACT",
)


@dataclass(frozen=True)
class OrderSourceBinding:
    source_input_manifest_hash: str
    position_contract_bundle_hash: str
    desired_position_ledger_schema_hash: str
    limit_order_ledger_schema_hash: str
    market_order_ledger_schema_hash: str
    working_order_transition_schema_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    order_source_binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 order source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 order position contract bundle hash", self.position_contract_bundle_hash)
        require_hash(
            "S27 v2 order desired-position ledger schema hash",
            self.desired_position_ledger_schema_hash,
        )
        require_hash("S27 v2 limit-order ledger schema hash", self.limit_order_ledger_schema_hash)
        require_hash("S27 v2 market-order ledger schema hash", self.market_order_ledger_schema_hash)
        require_hash(
            "S27 v2 working-order transition schema hash",
            self.working_order_transition_schema_hash,
        )
        require_hash("S27 v2 order completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 order strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 order source binding hash", self.order_source_binding_hash)


@dataclass(frozen=True)
class OrderComponentContract:
    component_family: str
    component_status: str
    required_input_hashes: tuple[str, ...]
    component_definition_hash: str
    component_policy_hash: str
    planned_component_output_hash: str
    component_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 order component family", self.component_family)
        if self.component_family not in REQUIRED_ORDER_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 order component family is not locked")
        require_text("S27 v2 order component status", self.component_status)
        if self.component_status != PLANNED_ORDER_COMPONENT_STATUS:
            raise CarverBlocked("S27 v2 order component must remain planned-only")
        require_non_empty_tuple("S27 v2 order component input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 order component input hash", input_hash)
        require_hash("S27 v2 order component definition hash", self.component_definition_hash)
        require_hash("S27 v2 order component policy hash", self.component_policy_hash)
        require_hash("S27 v2 order planned component output hash", self.planned_component_output_hash)
        require_hash("S27 v2 order component contract hash", self.component_contract_hash)


@dataclass(frozen=True)
class OrderKindContract:
    order_kind_label: str
    required_policy_hashes: tuple[str, ...]
    order_kind_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 order kind label", self.order_kind_label)
        if self.order_kind_label not in REQUIRED_ORDER_KIND_LABELS:
            raise CarverBlocked("S27 v2 order kind label is not locked")
        require_non_empty_tuple("S27 v2 order kind policy hashes", self.required_policy_hashes)
        for policy_hash in self.required_policy_hashes:
            require_hash("S27 v2 order kind policy hash", policy_hash)
        require_hash("S27 v2 order kind contract hash", self.order_kind_contract_hash)


@dataclass(frozen=True)
class OrderTransitionKindContract:
    transition_kind_label: str
    required_policy_hashes: tuple[str, ...]
    transition_kind_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 order transition kind label", self.transition_kind_label)
        if self.transition_kind_label not in REQUIRED_ORDER_TRANSITION_KIND_LABELS:
            raise CarverBlocked("S27 v2 order transition kind label is not locked")
        require_non_empty_tuple("S27 v2 order transition kind policy hashes", self.required_policy_hashes)
        for policy_hash in self.required_policy_hashes:
            require_hash("S27 v2 order transition kind policy hash", policy_hash)
        require_hash("S27 v2 order transition kind contract hash", self.transition_kind_contract_hash)


@dataclass(frozen=True)
class OrderInvariantContract:
    invariant_label: str
    required_proof_hashes: tuple[str, ...]
    invariant_policy_hash: str
    invariant_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 order invariant label", self.invariant_label)
        if self.invariant_label not in REQUIRED_ORDER_INVARIANTS:
            raise CarverBlocked("S27 v2 order invariant label is not locked")
        require_non_empty_tuple("S27 v2 order invariant proof hashes", self.required_proof_hashes)
        for proof_hash in self.required_proof_hashes:
            require_hash("S27 v2 order invariant proof hash", proof_hash)
        require_hash("S27 v2 order invariant policy hash", self.invariant_policy_hash)
        require_hash("S27 v2 order invariant contract hash", self.invariant_contract_hash)


@dataclass(frozen=True)
class OrderContractBundle:
    status: str
    source_binding: OrderSourceBinding
    component_contracts: tuple[OrderComponentContract, ...]
    order_kind_contracts: tuple[OrderKindContract, ...]
    transition_kind_contracts: tuple[OrderTransitionKindContract, ...]
    invariant_contracts: tuple[OrderInvariantContract, ...]
    tick_rounding_policy_hash: str
    working_limit_lifecycle_policy_hash: str
    overnight_recompute_policy_hash: str
    roll_boundary_policy_hash: str
    order_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 order contract status", self.status)
        if self.status != S27_V2_ORDER_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 order contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 order component contracts", self.component_contracts)
        seen_components: set[str] = set()
        for component_contract in self.component_contracts:
            component_contract.validate()
            if component_contract.component_family in seen_components:
                raise CarverBlocked("S27 v2 order component contracts must be unique")
            seen_components.add(component_contract.component_family)
        if tuple(contract.component_family for contract in self.component_contracts) != REQUIRED_ORDER_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 order component contracts must match locked component tuple")
        require_non_empty_tuple("S27 v2 order kind contracts", self.order_kind_contracts)
        seen_kinds: set[str] = set()
        for kind_contract in self.order_kind_contracts:
            kind_contract.validate()
            if kind_contract.order_kind_label in seen_kinds:
                raise CarverBlocked("S27 v2 order kind contracts must be unique")
            seen_kinds.add(kind_contract.order_kind_label)
        if tuple(contract.order_kind_label for contract in self.order_kind_contracts) != REQUIRED_ORDER_KIND_LABELS:
            raise CarverBlocked("S27 v2 order kind contracts must match locked order-kind tuple")
        require_non_empty_tuple("S27 v2 order transition kind contracts", self.transition_kind_contracts)
        seen_transition_kinds: set[str] = set()
        for transition_contract in self.transition_kind_contracts:
            transition_contract.validate()
            if transition_contract.transition_kind_label in seen_transition_kinds:
                raise CarverBlocked("S27 v2 order transition kind contracts must be unique")
            seen_transition_kinds.add(transition_contract.transition_kind_label)
        if tuple(
            contract.transition_kind_label for contract in self.transition_kind_contracts
        ) != REQUIRED_ORDER_TRANSITION_KIND_LABELS:
            raise CarverBlocked("S27 v2 order transition kind contracts must match locked transition-kind tuple")
        require_non_empty_tuple("S27 v2 order invariant contracts", self.invariant_contracts)
        seen_invariants: set[str] = set()
        for invariant_contract in self.invariant_contracts:
            invariant_contract.validate()
            if invariant_contract.invariant_label in seen_invariants:
                raise CarverBlocked("S27 v2 order invariant contracts must be unique")
            seen_invariants.add(invariant_contract.invariant_label)
        if tuple(contract.invariant_label for contract in self.invariant_contracts) != REQUIRED_ORDER_INVARIANTS:
            raise CarverBlocked("S27 v2 order invariant contracts must match locked invariant tuple")
        require_hash("S27 v2 order tick-rounding policy hash", self.tick_rounding_policy_hash)
        require_hash(
            "S27 v2 working-limit lifecycle policy hash",
            self.working_limit_lifecycle_policy_hash,
        )
        require_hash("S27 v2 overnight recompute policy hash", self.overnight_recompute_policy_hash)
        require_hash("S27 v2 roll-boundary policy hash", self.roll_boundary_policy_hash)
        require_hash("S27 v2 order contract bundle hash", self.order_contract_bundle_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 order contract must preserve non-authorizations")

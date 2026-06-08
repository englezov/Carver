from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_POSITION_CONTRACT_ONLY_STATUS = "S27_V2_POSITION_CONTRACT_ONLY"
PLANNED_POSITION_COMPONENT_STATUS = "PLANNED_POSITION_COMPONENT_ONLY"

REQUIRED_POSITION_COMPONENT_FAMILIES = (
    "FORECAST_TO_POSITION_DIVISOR",
    "DESIRED_UNROUNDED_POSITION",
    "ROUNDING_POLICY_APPLICATION",
    "DESIRED_ROUNDED_POSITION",
    "CURRENT_POSITION_CONTEXT",
    "INITIAL_POSITION_POLICY",
)

REQUIRED_POSITION_INVARIANTS = (
    "FORECAST_LEDGER_HASH_BINDING",
    "DESIRED_UNROUNDED_POSITION_HASH_BINDING",
    "ROUNDING_POLICY_SOURCE_BINDING",
    "ROUNDED_POSITION_HASH_BINDING",
    "CURRENT_POSITION_STATE_HASH_BINDING",
    "NO_ORDER_GENERATION_IN_POSITION_CONTRACT",
)

REQUIRED_ROUNDING_POLICY_LABELS = (
    "NEAREST",
)


@dataclass(frozen=True)
class PositionSourceBinding:
    source_input_manifest_hash: str
    forecast_contract_bundle_hash: str
    forecast_ledger_schema_hash: str
    desired_position_ledger_schema_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    position_source_binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 position source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 position forecast contract bundle hash", self.forecast_contract_bundle_hash)
        require_hash("S27 v2 position forecast ledger schema hash", self.forecast_ledger_schema_hash)
        require_hash(
            "S27 v2 desired-position ledger schema hash",
            self.desired_position_ledger_schema_hash,
        )
        require_hash("S27 v2 position completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 position strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 position source binding hash", self.position_source_binding_hash)


@dataclass(frozen=True)
class PositionComponentContract:
    component_family: str
    component_status: str
    required_input_hashes: tuple[str, ...]
    component_definition_hash: str
    component_policy_hash: str
    planned_component_output_hash: str
    component_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 position component family", self.component_family)
        if self.component_family not in REQUIRED_POSITION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 position component family is not locked")
        require_text("S27 v2 position component status", self.component_status)
        if self.component_status != PLANNED_POSITION_COMPONENT_STATUS:
            raise CarverBlocked("S27 v2 position component must remain planned-only")
        require_non_empty_tuple("S27 v2 position component input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 position component input hash", input_hash)
        require_hash("S27 v2 position component definition hash", self.component_definition_hash)
        require_hash("S27 v2 position component policy hash", self.component_policy_hash)
        require_hash("S27 v2 position planned component output hash", self.planned_component_output_hash)
        require_hash("S27 v2 position component contract hash", self.component_contract_hash)


@dataclass(frozen=True)
class PositionRoundingPolicyContract:
    rounding_policy_label: str
    source_policy_hash: str
    rounding_direction_policy_hash: str
    tie_break_policy_hash: str
    rounding_policy_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 position rounding policy label", self.rounding_policy_label)
        if self.rounding_policy_label not in REQUIRED_ROUNDING_POLICY_LABELS:
            raise CarverBlocked("S27 v2 position rounding policy label is not locked")
        require_hash("S27 v2 position rounding source policy hash", self.source_policy_hash)
        require_hash("S27 v2 position rounding direction policy hash", self.rounding_direction_policy_hash)
        require_hash("S27 v2 position rounding tie-break policy hash", self.tie_break_policy_hash)
        require_hash("S27 v2 position rounding policy contract hash", self.rounding_policy_contract_hash)


@dataclass(frozen=True)
class PositionInvariantContract:
    invariant_label: str
    required_proof_hashes: tuple[str, ...]
    invariant_policy_hash: str
    invariant_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 position invariant label", self.invariant_label)
        if self.invariant_label not in REQUIRED_POSITION_INVARIANTS:
            raise CarverBlocked("S27 v2 position invariant label is not locked")
        require_non_empty_tuple("S27 v2 position invariant proof hashes", self.required_proof_hashes)
        for proof_hash in self.required_proof_hashes:
            require_hash("S27 v2 position invariant proof hash", proof_hash)
        require_hash("S27 v2 position invariant policy hash", self.invariant_policy_hash)
        require_hash("S27 v2 position invariant contract hash", self.invariant_contract_hash)


@dataclass(frozen=True)
class PositionContractBundle:
    status: str
    source_binding: PositionSourceBinding
    component_contracts: tuple[PositionComponentContract, ...]
    rounding_policy_contracts: tuple[PositionRoundingPolicyContract, ...]
    invariant_contracts: tuple[PositionInvariantContract, ...]
    forecast_to_position_divisor_policy_hash: str
    initial_position_policy_hash: str
    desired_position_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 position contract status", self.status)
        if self.status != S27_V2_POSITION_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 position contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 position component contracts", self.component_contracts)
        seen_components: set[str] = set()
        for component_contract in self.component_contracts:
            component_contract.validate()
            if component_contract.component_family in seen_components:
                raise CarverBlocked("S27 v2 position component contracts must be unique")
            seen_components.add(component_contract.component_family)
        if tuple(contract.component_family for contract in self.component_contracts) != REQUIRED_POSITION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 position component contracts must match locked component tuple")
        require_non_empty_tuple("S27 v2 rounding policy contracts", self.rounding_policy_contracts)
        seen_rounding: set[str] = set()
        for rounding_contract in self.rounding_policy_contracts:
            rounding_contract.validate()
            if rounding_contract.rounding_policy_label in seen_rounding:
                raise CarverBlocked("S27 v2 rounding policy contracts must be unique")
            seen_rounding.add(rounding_contract.rounding_policy_label)
        if tuple(contract.rounding_policy_label for contract in self.rounding_policy_contracts) != REQUIRED_ROUNDING_POLICY_LABELS:
            raise CarverBlocked("S27 v2 rounding policy contracts must match locked rounding tuple")
        require_non_empty_tuple("S27 v2 position invariant contracts", self.invariant_contracts)
        seen_invariants: set[str] = set()
        for invariant_contract in self.invariant_contracts:
            invariant_contract.validate()
            if invariant_contract.invariant_label in seen_invariants:
                raise CarverBlocked("S27 v2 position invariant contracts must be unique")
            seen_invariants.add(invariant_contract.invariant_label)
        if tuple(contract.invariant_label for contract in self.invariant_contracts) != REQUIRED_POSITION_INVARIANTS:
            raise CarverBlocked("S27 v2 position invariant contracts must match locked invariant tuple")
        require_hash(
            "S27 v2 forecast-to-position divisor policy hash",
            self.forecast_to_position_divisor_policy_hash,
        )
        require_hash("S27 v2 initial-position policy hash", self.initial_position_policy_hash)
        require_hash(
            "S27 v2 desired-position contract bundle hash",
            self.desired_position_contract_bundle_hash,
        )
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 position contract must preserve non-authorizations")

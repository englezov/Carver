from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_PNL_CONTRACT_ONLY_STATUS = "S27_V2_PNL_CONTRACT_ONLY"
PLANNED_PNL_COMPONENT_STATUS = "PLANNED_PNL_COMPONENT_ONLY"

REQUIRED_PNL_COMPONENT_FAMILIES = (
    "TRUST_ROOT_REFERENCE",
    "TRANSITION_STATE_REFERENCE",
    "POSITION_SOURCE_REFERENCE",
    "CLOSE_ONLY_PRICE_SOURCE_POLICY",
    "RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE",
    "CONTRACT_MULTIPLIER_CURRENCY_POLICY",
    "FILL_COST_APPLICATION",
    "PNL_SUMMARY",
)

REQUIRED_PNL_PRICE_SOURCE_LABELS = (
    "CLOSE_ONLY",
)

REQUIRED_PNL_BRIDGE_LABELS = (
    "RAW_SYMBOL_CONTINUITY",
    "ROLL_BRIDGE",
)

REQUIRED_PNL_INVARIANTS = (
    "TRUST_ROOT_HASH_BINDING",
    "PREVIOUS_STEP_OR_INITIAL_STATE_HASH_BINDING",
    "TRANSITION_AND_WORKING_STATE_HASH_BINDING",
    "POSITION_SOURCE_HASH_BINDING",
    "CLOSE_ONLY_START_END_PRICE_ROW_HASH_BINDING",
    "RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE_HASH_BINDING",
    "CONTRACT_MULTIPLIER_SOURCE_BINDING",
    "CURRENCY_POLICY_OPTIONAL_FIELD_BINDING",
    "FILL_HASH_SET_BINDING",
    "COST_HASH_SET_BINDING",
    "PNL_FORMULA_POLICY_BINDING",
    "NO_TARGET_POSITION_SHORTCUT_PNL",
    "NO_RESULT_INTERPRETATION_IN_PNL_CONTRACT",
)


@dataclass(frozen=True)
class PnlSourceBinding:
    replay_trust_root_hash: str
    source_input_manifest_hash: str
    transition_ledger_schema_hash: str
    fill_ledger_schema_hash: str
    cost_ledger_schema_hash: str
    pnl_ledger_schema_hash: str
    pnl_source_binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 PnL replay trust-root hash", self.replay_trust_root_hash)
        require_hash("S27 v2 PnL source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 PnL transition ledger schema hash", self.transition_ledger_schema_hash)
        require_hash("S27 v2 PnL fill ledger schema hash", self.fill_ledger_schema_hash)
        require_hash("S27 v2 PnL cost ledger schema hash", self.cost_ledger_schema_hash)
        require_hash("S27 v2 PnL ledger schema hash", self.pnl_ledger_schema_hash)
        require_hash("S27 v2 PnL source binding hash", self.pnl_source_binding_hash)


@dataclass(frozen=True)
class PnlComponentContract:
    component_family: str
    component_status: str
    required_input_hashes: tuple[str, ...]
    component_definition_hash: str
    component_policy_hash: str
    planned_component_output_hash: str
    component_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 PnL component family", self.component_family)
        if self.component_family not in REQUIRED_PNL_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 PnL component family is not locked")
        require_text("S27 v2 PnL component status", self.component_status)
        if self.component_status != PLANNED_PNL_COMPONENT_STATUS:
            raise CarverBlocked("S27 v2 PnL component must remain planned-only")
        require_non_empty_tuple("S27 v2 PnL component input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 PnL component input hash", input_hash)
        require_hash("S27 v2 PnL component definition hash", self.component_definition_hash)
        require_hash("S27 v2 PnL component policy hash", self.component_policy_hash)
        require_hash("S27 v2 PnL planned component output hash", self.planned_component_output_hash)
        require_hash("S27 v2 PnL component contract hash", self.component_contract_hash)


@dataclass(frozen=True)
class PnlPriceSourceContract:
    price_source_label: str
    required_policy_hashes: tuple[str, ...]
    price_source_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 PnL price source label", self.price_source_label)
        if self.price_source_label not in REQUIRED_PNL_PRICE_SOURCE_LABELS:
            raise CarverBlocked("S27 v2 PnL price source label is not locked")
        require_non_empty_tuple("S27 v2 PnL price source policy hashes", self.required_policy_hashes)
        for policy_hash in self.required_policy_hashes:
            require_hash("S27 v2 PnL price source policy hash", policy_hash)
        require_hash("S27 v2 PnL price source contract hash", self.price_source_contract_hash)


@dataclass(frozen=True)
class PnlBridgeContract:
    bridge_label: str
    required_proof_hashes: tuple[str, ...]
    bridge_policy_hash: str
    bridge_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 PnL bridge label", self.bridge_label)
        if self.bridge_label not in REQUIRED_PNL_BRIDGE_LABELS:
            raise CarverBlocked("S27 v2 PnL bridge label is not locked")
        require_non_empty_tuple("S27 v2 PnL bridge proof hashes", self.required_proof_hashes)
        for proof_hash in self.required_proof_hashes:
            require_hash("S27 v2 PnL bridge proof hash", proof_hash)
        require_hash("S27 v2 PnL bridge policy hash", self.bridge_policy_hash)
        require_hash("S27 v2 PnL bridge contract hash", self.bridge_contract_hash)


@dataclass(frozen=True)
class PnlInvariantContract:
    invariant_label: str
    required_proof_hashes: tuple[str, ...]
    invariant_policy_hash: str
    invariant_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 PnL invariant label", self.invariant_label)
        if self.invariant_label not in REQUIRED_PNL_INVARIANTS:
            raise CarverBlocked("S27 v2 PnL invariant label is not locked")
        require_non_empty_tuple("S27 v2 PnL invariant proof hashes", self.required_proof_hashes)
        for proof_hash in self.required_proof_hashes:
            require_hash("S27 v2 PnL invariant proof hash", proof_hash)
        require_hash("S27 v2 PnL invariant policy hash", self.invariant_policy_hash)
        require_hash("S27 v2 PnL invariant contract hash", self.invariant_contract_hash)


@dataclass(frozen=True)
class PnlContractBundle:
    status: str
    source_binding: PnlSourceBinding
    component_contracts: tuple[PnlComponentContract, ...]
    price_source_contracts: tuple[PnlPriceSourceContract, ...]
    bridge_contracts: tuple[PnlBridgeContract, ...]
    invariant_contracts: tuple[PnlInvariantContract, ...]
    pnl_formula_policy_hash: str
    close_price_source_policy_hash: str
    cost_application_policy_hash: str
    contract_multiplier_policy_hash: str
    currency_policy_hash: str
    target_position_shortcut_quarantine_policy_hash: str
    pnl_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 PnL contract status", self.status)
        if self.status != S27_V2_PNL_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 PnL contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 PnL component contracts", self.component_contracts)
        seen_components: set[str] = set()
        for component_contract in self.component_contracts:
            component_contract.validate()
            if component_contract.component_family in seen_components:
                raise CarverBlocked("S27 v2 PnL component contracts must be unique")
            seen_components.add(component_contract.component_family)
        if tuple(contract.component_family for contract in self.component_contracts) != REQUIRED_PNL_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 PnL component contracts must match locked component tuple")
        require_non_empty_tuple("S27 v2 PnL price source contracts", self.price_source_contracts)
        seen_price_sources: set[str] = set()
        for price_source_contract in self.price_source_contracts:
            price_source_contract.validate()
            if price_source_contract.price_source_label in seen_price_sources:
                raise CarverBlocked("S27 v2 PnL price source contracts must be unique")
            seen_price_sources.add(price_source_contract.price_source_label)
        if (
            tuple(contract.price_source_label for contract in self.price_source_contracts)
            != REQUIRED_PNL_PRICE_SOURCE_LABELS
        ):
            raise CarverBlocked("S27 v2 PnL price source contracts must match locked price source tuple")
        require_non_empty_tuple("S27 v2 PnL bridge contracts", self.bridge_contracts)
        seen_bridges: set[str] = set()
        for bridge_contract in self.bridge_contracts:
            bridge_contract.validate()
            if bridge_contract.bridge_label in seen_bridges:
                raise CarverBlocked("S27 v2 PnL bridge contracts must be unique")
            seen_bridges.add(bridge_contract.bridge_label)
        if tuple(contract.bridge_label for contract in self.bridge_contracts) != REQUIRED_PNL_BRIDGE_LABELS:
            raise CarverBlocked("S27 v2 PnL bridge contracts must match locked bridge tuple")
        require_non_empty_tuple("S27 v2 PnL invariant contracts", self.invariant_contracts)
        seen_invariants: set[str] = set()
        for invariant_contract in self.invariant_contracts:
            invariant_contract.validate()
            if invariant_contract.invariant_label in seen_invariants:
                raise CarverBlocked("S27 v2 PnL invariant contracts must be unique")
            seen_invariants.add(invariant_contract.invariant_label)
        if tuple(contract.invariant_label for contract in self.invariant_contracts) != REQUIRED_PNL_INVARIANTS:
            raise CarverBlocked("S27 v2 PnL invariant contracts must match locked invariant tuple")
        require_hash("S27 v2 PnL formula policy hash", self.pnl_formula_policy_hash)
        require_hash("S27 v2 close price source policy hash", self.close_price_source_policy_hash)
        require_hash("S27 v2 PnL cost application policy hash", self.cost_application_policy_hash)
        require_hash("S27 v2 PnL contract multiplier policy hash", self.contract_multiplier_policy_hash)
        require_hash("S27 v2 PnL currency policy hash", self.currency_policy_hash)
        require_hash(
            "S27 v2 target-position shortcut quarantine policy hash",
            self.target_position_shortcut_quarantine_policy_hash,
        )
        require_hash("S27 v2 PnL contract bundle hash", self.pnl_contract_bundle_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 PnL contract must preserve non-authorizations")

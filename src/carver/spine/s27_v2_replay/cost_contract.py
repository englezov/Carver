from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest, require_evidence_manifest_matches_trust_root
from .trust_root import ReplayTrustRoot
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_COST_CONTRACT_ONLY_STATUS = "S27_V2_COST_CONTRACT_ONLY"
PLANNED_COST_COMPONENT_STATUS = "PLANNED_COST_COMPONENT_ONLY"

REQUIRED_COST_COMPONENT_FAMILIES = (
    "FILL_LEDGER_REFERENCE",
    "COMMISSION_POLICY",
    "LIMIT_FILL_COMMISSION_ONLY_BRANCH",
    "MARKET_FILL_SPREAD_COST_BRANCH",
    "SPREAD_SPACE_POLICY",
    "CONTRACT_MULTIPLIER_CURRENCY_POLICY",
    "TOTAL_COST_SUMMARY",
)

REQUIRED_COST_BRANCH_LABELS = (
    "LIMIT_COMMISSION_ONLY",
    "MARKET_COMMISSION_PLUS_SPREAD",
)

REQUIRED_SPREAD_SPACE_LABELS = (
    "PRICE_SPACE",
    "CURRENCY_SPACE",
)

REQUIRED_COST_INVARIANTS = (
    "FILL_CONTRACT_BUNDLE_HASH_BINDING",
    "COMMISSION_PER_CONTRACT_TIMES_QUANTITY_BINDING",
    "LIMIT_FILL_ZERO_SPREAD_BINDING",
    "MARKET_FILL_POSITIVE_SPREAD_BINDING",
    "PRICE_SPACE_SPREAD_MULTIPLIER_BINDING",
    "CURRENCY_SPACE_SPREAD_DIRECT_AMOUNT_BINDING",
    "TOTAL_COST_EQUALS_COMMISSION_PLUS_SPREAD_BINDING",
    "NO_PNL_ACCOUNTING_IN_COST_CONTRACT",
)


@dataclass(frozen=True)
class CostSourceBinding:
    source_input_manifest_hash: str
    fill_contract_bundle_hash: str
    fill_ledger_schema_hash: str
    commission_ledger_schema_hash: str
    spread_cost_ledger_schema_hash: str
    cost_ledger_schema_hash: str
    cost_source_binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 cost source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 cost fill contract bundle hash", self.fill_contract_bundle_hash)
        require_hash("S27 v2 cost fill ledger schema hash", self.fill_ledger_schema_hash)
        require_hash("S27 v2 commission ledger schema hash", self.commission_ledger_schema_hash)
        require_hash("S27 v2 spread-cost ledger schema hash", self.spread_cost_ledger_schema_hash)
        require_hash("S27 v2 cost ledger schema hash", self.cost_ledger_schema_hash)
        require_hash("S27 v2 cost source binding hash", self.cost_source_binding_hash)


@dataclass(frozen=True)
class CostComponentContract:
    component_family: str
    component_status: str
    required_input_hashes: tuple[str, ...]
    component_definition_hash: str
    component_policy_hash: str
    planned_component_output_hash: str
    component_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 cost component family", self.component_family)
        if self.component_family not in REQUIRED_COST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 cost component family is not locked")
        require_text("S27 v2 cost component status", self.component_status)
        if self.component_status != PLANNED_COST_COMPONENT_STATUS:
            raise CarverBlocked("S27 v2 cost component must remain planned-only")
        require_non_empty_tuple("S27 v2 cost component input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 cost component input hash", input_hash)
        require_hash("S27 v2 cost component definition hash", self.component_definition_hash)
        require_hash("S27 v2 cost component policy hash", self.component_policy_hash)
        require_hash("S27 v2 cost planned component output hash", self.planned_component_output_hash)
        require_hash("S27 v2 cost component contract hash", self.component_contract_hash)


@dataclass(frozen=True)
class CostBranchContract:
    branch_label: str
    required_input_hashes: tuple[str, ...]
    branch_policy_hash: str
    planned_branch_output_hash: str
    branch_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 cost branch label", self.branch_label)
        if self.branch_label not in REQUIRED_COST_BRANCH_LABELS:
            raise CarverBlocked("S27 v2 cost branch label is not locked")
        require_non_empty_tuple("S27 v2 cost branch input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 cost branch input hash", input_hash)
        require_hash("S27 v2 cost branch policy hash", self.branch_policy_hash)
        require_hash("S27 v2 cost planned branch output hash", self.planned_branch_output_hash)
        require_hash("S27 v2 cost branch contract hash", self.branch_contract_hash)


@dataclass(frozen=True)
class SpreadSpaceContract:
    spread_space_label: str
    required_policy_hashes: tuple[str, ...]
    spread_space_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 spread-space label", self.spread_space_label)
        if self.spread_space_label not in REQUIRED_SPREAD_SPACE_LABELS:
            raise CarverBlocked("S27 v2 spread-space label is not locked")
        require_non_empty_tuple("S27 v2 spread-space policy hashes", self.required_policy_hashes)
        for policy_hash in self.required_policy_hashes:
            require_hash("S27 v2 spread-space policy hash", policy_hash)
        require_hash("S27 v2 spread-space contract hash", self.spread_space_contract_hash)


@dataclass(frozen=True)
class CostInvariantContract:
    invariant_label: str
    required_proof_hashes: tuple[str, ...]
    invariant_policy_hash: str
    invariant_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 cost invariant label", self.invariant_label)
        if self.invariant_label not in REQUIRED_COST_INVARIANTS:
            raise CarverBlocked("S27 v2 cost invariant label is not locked")
        require_non_empty_tuple("S27 v2 cost invariant proof hashes", self.required_proof_hashes)
        for proof_hash in self.required_proof_hashes:
            require_hash("S27 v2 cost invariant proof hash", proof_hash)
        require_hash("S27 v2 cost invariant policy hash", self.invariant_policy_hash)
        require_hash("S27 v2 cost invariant contract hash", self.invariant_contract_hash)


@dataclass(frozen=True)
class CostContractBundle:
    status: str
    source_binding: CostSourceBinding
    component_contracts: tuple[CostComponentContract, ...]
    branch_contracts: tuple[CostBranchContract, ...]
    spread_space_contracts: tuple[SpreadSpaceContract, ...]
    invariant_contracts: tuple[CostInvariantContract, ...]
    commission_policy_hash: str
    spread_policy_hash: str
    cost_calculation_policy_hash: str
    contract_multiplier_policy_hash: str
    currency_conversion_policy_hash: str
    deflation_policy_hash: str
    cost_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 cost contract status", self.status)
        if self.status != S27_V2_COST_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 cost contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 cost component contracts", self.component_contracts)
        seen_components: set[str] = set()
        for component_contract in self.component_contracts:
            component_contract.validate()
            if component_contract.component_family in seen_components:
                raise CarverBlocked("S27 v2 cost component contracts must be unique")
            seen_components.add(component_contract.component_family)
        if tuple(contract.component_family for contract in self.component_contracts) != REQUIRED_COST_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 cost component contracts must match locked component tuple")
        require_non_empty_tuple("S27 v2 cost branch contracts", self.branch_contracts)
        seen_branches: set[str] = set()
        for branch_contract in self.branch_contracts:
            branch_contract.validate()
            if branch_contract.branch_label in seen_branches:
                raise CarverBlocked("S27 v2 cost branch contracts must be unique")
            seen_branches.add(branch_contract.branch_label)
        if tuple(contract.branch_label for contract in self.branch_contracts) != REQUIRED_COST_BRANCH_LABELS:
            raise CarverBlocked("S27 v2 cost branch contracts must match locked branch tuple")
        require_non_empty_tuple("S27 v2 spread-space contracts", self.spread_space_contracts)
        seen_spaces: set[str] = set()
        for spread_space_contract in self.spread_space_contracts:
            spread_space_contract.validate()
            if spread_space_contract.spread_space_label in seen_spaces:
                raise CarverBlocked("S27 v2 spread-space contracts must be unique")
            seen_spaces.add(spread_space_contract.spread_space_label)
        if tuple(contract.spread_space_label for contract in self.spread_space_contracts) != REQUIRED_SPREAD_SPACE_LABELS:
            raise CarverBlocked("S27 v2 spread-space contracts must match locked spread-space tuple")
        require_non_empty_tuple("S27 v2 cost invariant contracts", self.invariant_contracts)
        seen_invariants: set[str] = set()
        for invariant_contract in self.invariant_contracts:
            invariant_contract.validate()
            if invariant_contract.invariant_label in seen_invariants:
                raise CarverBlocked("S27 v2 cost invariant contracts must be unique")
            seen_invariants.add(invariant_contract.invariant_label)
        if tuple(contract.invariant_label for contract in self.invariant_contracts) != REQUIRED_COST_INVARIANTS:
            raise CarverBlocked("S27 v2 cost invariant contracts must match locked invariant tuple")
        require_hash("S27 v2 commission policy hash", self.commission_policy_hash)
        require_hash("S27 v2 spread policy hash", self.spread_policy_hash)
        require_hash("S27 v2 cost calculation policy hash", self.cost_calculation_policy_hash)
        require_hash("S27 v2 contract multiplier policy hash", self.contract_multiplier_policy_hash)
        require_hash("S27 v2 currency conversion policy hash", self.currency_conversion_policy_hash)
        require_hash("S27 v2 deflation policy hash", self.deflation_policy_hash)
        require_hash("S27 v2 cost contract bundle hash", self.cost_contract_bundle_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 cost contract must preserve non-authorizations")

    def validate_against_policy_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
    ) -> None:
        require_evidence_manifest_matches_trust_root(replay_trust_root, evidence_manifest)
        self.validate()
        if self.commission_policy_hash != replay_trust_root.commission_policy_hash:
            raise CarverBlocked("S27 v2 cost contract must bind trust-root commission policy")
        if self.spread_policy_hash != replay_trust_root.spread_unit_policy_hash:
            raise CarverBlocked("S27 v2 cost contract must bind trust-root spread-unit policy")
        if self.contract_multiplier_policy_hash != replay_trust_root.contract_multiplier_currency_policy_hash:
            raise CarverBlocked("S27 v2 cost contract must bind trust-root multiplier/currency policy")
        if self.currency_conversion_policy_hash != replay_trust_root.contract_multiplier_currency_policy_hash:
            raise CarverBlocked("S27 v2 cost contract must bind trust-root multiplier/currency policy")

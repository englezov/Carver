from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import REQUIRED_UNRESOLVED_GATE_LABELS, S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_VALIDATION_CONTRACT_ONLY_STATUS = "S27_V2_VALIDATION_CONTRACT_ONLY"
PLANNED_VALIDATION_COMPONENT_STATUS = "PLANNED_VALIDATION_COMPONENT_ONLY"

REQUIRED_VALIDATION_COMPONENT_FAMILIES = (
    "TRUST_ROOT_REFERENCE",
    "EVIDENCE_MANIFEST_REFERENCE",
    "REQUIRED_LEDGER_FAMILY_COVERAGE",
    "PROVENANCE_HASH_CHAIN",
    "FAIL_CLOSED_GATE_STATUS",
    "LOCAL_HOSTILE_AUDIT_PACKET",
    "SUPERSESSION_MANIFEST",
    "NON_AUTHORIZATION_PRESERVATION",
)

REQUIRED_VALIDATION_LEDGER_LABELS = (
    "VALIDATION_LEDGER",
    "PROVENANCE_AND_HASH_LEDGER",
    "LOCAL_HOSTILE_AUDIT_RESULT",
)

REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS = (
    "SCHEMA_AND_TRUST_ROOT_CODE",
    "FAIL_CLOSED_ROW_PATHS",
    "DAILY_HOURLY_LEVEL_COMPATIBILITY_AND_SIGMA_BRIDGE",
    "FORECAST_ARITHMETIC_AND_GATES",
    "ORDER_FILL_COST_PNL_PROVENANCE",
    "EXTERNAL_AUDIT_PACKET_AFTER_ARTIFACTS_EXIST",
)

REQUIRED_VALIDATION_INVARIANTS = (
    "ACTIVE_EVIDENCE_MANIFEST_HASH_BINDING",
    "REQUIRED_ARTIFACT_FAMILY_COVERAGE",
    "TRUST_ROOT_EVIDENCE_MANIFEST_CROSS_CHECK",
    "VALIDATION_LEDGER_HASH_BINDING",
    "PROVENANCE_AND_HASH_LEDGER_BINDING",
    "LOCAL_HOSTILE_AUDIT_RESULT_BINDING",
    "STALE_EVIDENCE_SUPERSESSION_BINDING",
    "FAIL_CLOSED_UNRESOLVED_GATES_BINDING",
    "NO_PARSER_REPLAY_EXECUTION_IN_VALIDATION_CONTRACT",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM_IN_VALIDATION_CONTRACT",
)


@dataclass(frozen=True)
class ValidationSourceBinding:
    replay_trust_root_hash: str
    active_evidence_manifest_hash: str
    source_input_manifest_hash: str
    pnl_contract_bundle_hash: str
    validation_ledger_schema_hash: str
    provenance_and_hash_ledger_schema_hash: str
    local_hostile_audit_result_schema_hash: str
    validation_source_binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 validation replay trust-root hash", self.replay_trust_root_hash)
        require_hash("S27 v2 validation active evidence manifest hash", self.active_evidence_manifest_hash)
        require_hash("S27 v2 validation source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 validation PnL contract bundle hash", self.pnl_contract_bundle_hash)
        require_hash("S27 v2 validation ledger schema hash", self.validation_ledger_schema_hash)
        require_hash(
            "S27 v2 provenance and hash ledger schema hash",
            self.provenance_and_hash_ledger_schema_hash,
        )
        require_hash(
            "S27 v2 local hostile audit result schema hash",
            self.local_hostile_audit_result_schema_hash,
        )
        require_hash("S27 v2 validation source binding hash", self.validation_source_binding_hash)


@dataclass(frozen=True)
class ValidationComponentContract:
    component_family: str
    component_status: str
    required_input_hashes: tuple[str, ...]
    component_definition_hash: str
    component_policy_hash: str
    planned_component_output_hash: str
    component_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 validation component family", self.component_family)
        if self.component_family not in REQUIRED_VALIDATION_COMPONENT_FAMILIES:
            raise CarverBlocked("S27 v2 validation component family is not locked")
        require_text("S27 v2 validation component status", self.component_status)
        if self.component_status != PLANNED_VALIDATION_COMPONENT_STATUS:
            raise CarverBlocked("S27 v2 validation component must remain planned-only")
        require_non_empty_tuple("S27 v2 validation component input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 validation component input hash", input_hash)
        require_hash("S27 v2 validation component definition hash", self.component_definition_hash)
        require_hash("S27 v2 validation component policy hash", self.component_policy_hash)
        require_hash("S27 v2 validation planned component output hash", self.planned_component_output_hash)
        require_hash("S27 v2 validation component contract hash", self.component_contract_hash)


@dataclass(frozen=True)
class ValidationLedgerContract:
    ledger_label: str
    required_input_hashes: tuple[str, ...]
    ledger_schema_hash: str
    ledger_policy_hash: str
    planned_ledger_output_hash: str
    ledger_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 validation ledger label", self.ledger_label)
        if self.ledger_label not in REQUIRED_VALIDATION_LEDGER_LABELS:
            raise CarverBlocked("S27 v2 validation ledger label is not locked")
        require_non_empty_tuple("S27 v2 validation ledger input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 validation ledger input hash", input_hash)
        require_hash("S27 v2 validation ledger schema hash", self.ledger_schema_hash)
        require_hash("S27 v2 validation ledger policy hash", self.ledger_policy_hash)
        require_hash("S27 v2 validation planned ledger output hash", self.planned_ledger_output_hash)
        require_hash("S27 v2 validation ledger contract hash", self.ledger_contract_hash)


@dataclass(frozen=True)
class ValidationAuditCheckpointContract:
    checkpoint_label: str
    required_policy_hashes: tuple[str, ...]
    planned_audit_scope_hash: str
    audit_checkpoint_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 validation audit checkpoint label", self.checkpoint_label)
        if self.checkpoint_label not in REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS:
            raise CarverBlocked("S27 v2 validation audit checkpoint label is not locked")
        require_non_empty_tuple(
            "S27 v2 validation audit checkpoint policy hashes",
            self.required_policy_hashes,
        )
        for policy_hash in self.required_policy_hashes:
            require_hash("S27 v2 validation audit checkpoint policy hash", policy_hash)
        require_hash("S27 v2 validation planned audit scope hash", self.planned_audit_scope_hash)
        require_hash("S27 v2 validation audit checkpoint contract hash", self.audit_checkpoint_contract_hash)


@dataclass(frozen=True)
class ValidationInvariantContract:
    invariant_label: str
    required_proof_hashes: tuple[str, ...]
    invariant_policy_hash: str
    invariant_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 validation invariant label", self.invariant_label)
        if self.invariant_label not in REQUIRED_VALIDATION_INVARIANTS:
            raise CarverBlocked("S27 v2 validation invariant label is not locked")
        require_non_empty_tuple("S27 v2 validation invariant proof hashes", self.required_proof_hashes)
        for proof_hash in self.required_proof_hashes:
            require_hash("S27 v2 validation invariant proof hash", proof_hash)
        require_hash("S27 v2 validation invariant policy hash", self.invariant_policy_hash)
        require_hash("S27 v2 validation invariant contract hash", self.invariant_contract_hash)


@dataclass(frozen=True)
class ValidationContractBundle:
    status: str
    source_binding: ValidationSourceBinding
    component_contracts: tuple[ValidationComponentContract, ...]
    ledger_contracts: tuple[ValidationLedgerContract, ...]
    audit_checkpoint_contracts: tuple[ValidationAuditCheckpointContract, ...]
    invariant_contracts: tuple[ValidationInvariantContract, ...]
    required_unresolved_gate_labels: tuple[str, ...]
    required_artifact_family_policy_hash: str
    provenance_hash_chain_policy_hash: str
    fail_closed_gate_policy_hash: str
    stale_evidence_supersession_policy_hash: str
    local_hostile_audit_policy_hash: str
    external_audit_packet_policy_hash: str
    validation_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 validation contract status", self.status)
        if self.status != S27_V2_VALIDATION_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 validation contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 validation component contracts", self.component_contracts)
        seen_components: set[str] = set()
        for component_contract in self.component_contracts:
            component_contract.validate()
            if component_contract.component_family in seen_components:
                raise CarverBlocked("S27 v2 validation component contracts must be unique")
            seen_components.add(component_contract.component_family)
        if (
            tuple(contract.component_family for contract in self.component_contracts)
            != REQUIRED_VALIDATION_COMPONENT_FAMILIES
        ):
            raise CarverBlocked("S27 v2 validation component contracts must match locked component tuple")
        require_non_empty_tuple("S27 v2 validation ledger contracts", self.ledger_contracts)
        seen_ledgers: set[str] = set()
        for ledger_contract in self.ledger_contracts:
            ledger_contract.validate()
            if ledger_contract.ledger_label in seen_ledgers:
                raise CarverBlocked("S27 v2 validation ledger contracts must be unique")
            seen_ledgers.add(ledger_contract.ledger_label)
        if tuple(contract.ledger_label for contract in self.ledger_contracts) != REQUIRED_VALIDATION_LEDGER_LABELS:
            raise CarverBlocked("S27 v2 validation ledger contracts must match locked ledger tuple")
        require_non_empty_tuple(
            "S27 v2 validation audit checkpoint contracts",
            self.audit_checkpoint_contracts,
        )
        seen_checkpoints: set[str] = set()
        for checkpoint_contract in self.audit_checkpoint_contracts:
            checkpoint_contract.validate()
            if checkpoint_contract.checkpoint_label in seen_checkpoints:
                raise CarverBlocked("S27 v2 validation audit checkpoint contracts must be unique")
            seen_checkpoints.add(checkpoint_contract.checkpoint_label)
        if (
            tuple(contract.checkpoint_label for contract in self.audit_checkpoint_contracts)
            != REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS
        ):
            raise CarverBlocked("S27 v2 validation audit checkpoint contracts must match locked checkpoint tuple")
        require_non_empty_tuple("S27 v2 validation invariant contracts", self.invariant_contracts)
        seen_invariants: set[str] = set()
        for invariant_contract in self.invariant_contracts:
            invariant_contract.validate()
            if invariant_contract.invariant_label in seen_invariants:
                raise CarverBlocked("S27 v2 validation invariant contracts must be unique")
            seen_invariants.add(invariant_contract.invariant_label)
        if tuple(contract.invariant_label for contract in self.invariant_contracts) != REQUIRED_VALIDATION_INVARIANTS:
            raise CarverBlocked("S27 v2 validation invariant contracts must match locked invariant tuple")
        require_non_empty_tuple(
            "S27 v2 validation required unresolved gate labels",
            self.required_unresolved_gate_labels,
        )
        if self.required_unresolved_gate_labels != REQUIRED_UNRESOLVED_GATE_LABELS:
            raise CarverBlocked("S27 v2 validation contract must bind the complete locked unresolved gate tuple")
        require_hash("S27 v2 required artifact family policy hash", self.required_artifact_family_policy_hash)
        require_hash("S27 v2 provenance hash-chain policy hash", self.provenance_hash_chain_policy_hash)
        require_hash("S27 v2 fail-closed gate policy hash", self.fail_closed_gate_policy_hash)
        require_hash(
            "S27 v2 stale evidence supersession policy hash",
            self.stale_evidence_supersession_policy_hash,
        )
        require_hash("S27 v2 local hostile audit policy hash", self.local_hostile_audit_policy_hash)
        require_hash("S27 v2 external audit packet policy hash", self.external_audit_packet_policy_hash)
        require_hash("S27 v2 validation contract bundle hash", self.validation_contract_bundle_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 validation contract must preserve non-authorizations")

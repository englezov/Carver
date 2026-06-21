from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import ARTIFACT_FAMILIES, REQUIRED_UNRESOLVED_GATE_LABELS
from .construction_contract import (
    PLANNED_CONSTRUCTION_PHASES,
    REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE,
    REQUIRED_SCHEMA_FAMILY_BY_ARTIFACT_FAMILY,
)
from .validation import require_hash, require_integer, require_non_empty_tuple, require_text, require_tuple


@dataclass(frozen=True)
class ReplayFailClosedGatePlan:
    gate_label: str
    blocked_status: str
    required_evidence_hash: str

    def validate(self) -> None:
        require_text("S27 v2 replay fail-closed gate label", self.gate_label)
        require_text("S27 v2 replay fail-closed blocked status", self.blocked_status)
        if self.blocked_status not in REQUIRED_UNRESOLVED_GATE_LABELS:
            raise CarverBlocked("S27 v2 replay fail-closed gate must use a locked unresolved status")
        if self.gate_label != self.blocked_status:
            raise CarverBlocked("S27 v2 replay fail-closed gate label must match locked blocked status")
        require_hash("S27 v2 replay fail-closed required evidence hash", self.required_evidence_hash)


@dataclass(frozen=True)
class ReplayLedgerEmissionPlan:
    ledger_family: str
    allowed_schema_family: str
    required_input_hashes: tuple[str, ...]
    output_hash_label: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 replay ledger emission must be validated against a locked construction step")

    def validate_against_locked_step(self, step_label: str) -> None:
        require_text("S27 v2 replay ledger construction step label", step_label)
        if step_label not in PLANNED_CONSTRUCTION_PHASES:
            raise CarverBlocked("S27 v2 replay ledger construction step label is not locked")
        require_text("S27 v2 replay ledger family", self.ledger_family)
        if self.ledger_family not in REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE[step_label]:
            raise CarverBlocked("S27 v2 replay ledger family is not allowed for the locked construction step")
        require_text("S27 v2 replay ledger allowed schema family", self.allowed_schema_family)
        if self.allowed_schema_family != REQUIRED_SCHEMA_FAMILY_BY_ARTIFACT_FAMILY[self.ledger_family]:
            raise CarverBlocked("S27 v2 replay ledger schema family does not match locked artifact schema")
        require_non_empty_tuple("S27 v2 replay ledger required input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 replay ledger required input hash", input_hash)
        require_text("S27 v2 replay ledger output hash label", self.output_hash_label)
        if self.output_hash_label != f"{self.ledger_family}_HASH":
            raise CarverBlocked("S27 v2 replay ledger output hash label must be locked to artifact family")


@dataclass(frozen=True)
class ReplayConstructionStepPlan:
    step_index: int
    step_label: str
    ledger_emissions: tuple[ReplayLedgerEmissionPlan, ...]
    fail_closed_gates: tuple[ReplayFailClosedGatePlan, ...]
    step_plan_hash: str

    def validate(self) -> None:
        require_integer("S27 v2 replay construction step index", self.step_index)
        if self.step_index < 1 or self.step_index > len(PLANNED_CONSTRUCTION_PHASES):
            raise CarverBlocked("S27 v2 replay construction step index is outside the locked construction range")
        require_text("S27 v2 replay construction step label", self.step_label)
        if self.step_label != PLANNED_CONSTRUCTION_PHASES[self.step_index - 1]:
            raise CarverBlocked("S27 v2 replay construction step label does not match locked construction order")
        require_tuple("S27 v2 replay construction ledger emissions", self.ledger_emissions)
        required_ledger_families = REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE[self.step_label]
        if tuple(emission.ledger_family for emission in self.ledger_emissions) != required_ledger_families:
            raise CarverBlocked("S27 v2 replay construction ledger emissions must match locked artifact tuple")
        for emission in self.ledger_emissions:
            emission.validate_against_locked_step(self.step_label)
        require_tuple("S27 v2 replay construction fail-closed gates", self.fail_closed_gates)
        for gate in self.fail_closed_gates:
            gate.validate()
        require_hash("S27 v2 replay construction step plan hash", self.step_plan_hash)


@dataclass(frozen=True)
class TrustedReplayBuilderPlan:
    planning_config_hash: str
    parser_plan_bundle_hash: str
    construction_steps: tuple[ReplayConstructionStepPlan, ...]
    final_bundle_assembly_policy_hash: str
    builder_plan_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 trusted replay planning config hash", self.planning_config_hash)
        require_hash("S27 v2 trusted replay parser plan bundle hash", self.parser_plan_bundle_hash)
        require_non_empty_tuple("S27 v2 trusted replay construction steps", self.construction_steps)
        if len(self.construction_steps) != len(PLANNED_CONSTRUCTION_PHASES):
            raise CarverBlocked("S27 v2 trusted replay builder plan must include every locked construction step")
        previous_index = 0
        seen_labels: set[str] = set()
        for step in self.construction_steps:
            step.validate()
            if step.step_index <= previous_index:
                raise CarverBlocked("S27 v2 replay construction steps must be strictly ordered")
            if step.step_label in seen_labels:
                raise CarverBlocked("S27 v2 replay construction step labels must be unique")
            previous_index = step.step_index
            seen_labels.add(step.step_label)
        if tuple(step.step_label for step in self.construction_steps) != PLANNED_CONSTRUCTION_PHASES:
            raise CarverBlocked("S27 v2 trusted replay builder steps must match the locked construction tuple")
        covered_gates = tuple(
            gate.blocked_status
            for step in self.construction_steps
            for gate in step.fail_closed_gates
        )
        if covered_gates != REQUIRED_UNRESOLVED_GATE_LABELS:
            raise CarverBlocked("S27 v2 trusted replay builder plan must cover every locked unresolved gate exactly once")
        covered_artifacts = tuple(
            emission.ledger_family
            for step in self.construction_steps
            for emission in step.ledger_emissions
        )
        if covered_artifacts != ARTIFACT_FAMILIES:
            raise CarverBlocked("S27 v2 trusted replay builder plan must cover every locked artifact exactly once")
        require_hash(
            "S27 v2 trusted replay final bundle assembly policy hash",
            self.final_bundle_assembly_policy_hash,
        )
        require_hash("S27 v2 trusted replay builder plan hash", self.builder_plan_hash)

from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import ARTIFACT_FAMILIES, REQUIRED_UNRESOLVED_GATE_LABELS, S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_integer, require_non_empty_tuple, require_text


S27_V2_CONSTRUCTION_SCAFFOLD_ONLY_STATUS = "S27_V2_PARSER_FILE_REPLAY_CONSTRUCTION_SCAFFOLD_ONLY"

PLANNED_CONSTRUCTION_PHASES = (
    "CANONICAL_SERIALIZATION_AND_HASH_POLICY_VALIDATION",
    "FILE_DECLARATION_AND_RAW_FILE_HASH_SET_BINDING",
    "SOURCE_UNIVERSE_AND_ROW_LOCATOR_CONSTRUCTION",
    "DAILY_HOURLY_LEVEL_COMPATIBILITY_CONSTRUCTION",
    "RUNTIME_HISTORY_CONSTRUCTION",
    "FORECAST_AND_DESIRED_POSITION_CONSTRUCTION",
    "ORDER_AND_TRANSITION_CONSTRUCTION",
    "FILL_CONSTRUCTION",
    "COST_CONSTRUCTION",
    "PNL_CONSTRUCTION",
    "VALIDATION_PROVENANCE_EVIDENCE_MANIFEST_CONSTRUCTION",
    "FINAL_TRUSTED_REPLAY_BUNDLE_ASSEMBLY",
)

REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE = {
    "CANONICAL_SERIALIZATION_AND_HASH_POLICY_VALIDATION": (),
    "FILE_DECLARATION_AND_RAW_FILE_HASH_SET_BINDING": (),
    "SOURCE_UNIVERSE_AND_ROW_LOCATOR_CONSTRUCTION": ("SOURCE_INPUT_MANIFEST",),
    "DAILY_HOURLY_LEVEL_COMPATIBILITY_CONSTRUCTION": (
        "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER",
    ),
    "RUNTIME_HISTORY_CONSTRUCTION": ("RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM",),
    "FORECAST_AND_DESIRED_POSITION_CONSTRUCTION": (
        "FORECAST_REPLAY_LEDGER",
        "DESIRED_POSITION_LEDGER",
    ),
    "ORDER_AND_TRANSITION_CONSTRUCTION": (
        "LIMIT_ORDER_LEDGER",
        "MARKET_ORDER_LEDGER",
        "WORKING_ORDER_TRANSITION_LEDGER",
        "REMAINING_LIMIT_ORDER_LEDGER",
        "CANCELED_LIMIT_ORDER_LEDGER",
    ),
    "FILL_CONSTRUCTION": ("FILL_LEDGER",),
    "COST_CONSTRUCTION": (
        "COMMISSION_LEDGER",
        "SPREAD_COST_LEDGER",
    ),
    "PNL_CONSTRUCTION": ("PNL_LEDGER",),
    "VALIDATION_PROVENANCE_EVIDENCE_MANIFEST_CONSTRUCTION": (
        "VALIDATION_LEDGER",
        "PROVENANCE_AND_HASH_LEDGER",
        "LOCAL_HOSTILE_AUDIT_RESULT",
    ),
    "FINAL_TRUSTED_REPLAY_BUNDLE_ASSEMBLY": (),
}

REQUIRED_SCHEMA_FAMILY_BY_ARTIFACT_FAMILY = {
    artifact_family: f"{artifact_family}_SCHEMA"
    for artifact_family in ARTIFACT_FAMILIES
}


@dataclass(frozen=True)
class ConstructionArtifactReference:
    artifact_family: str
    schema_family: str
    artifact_hash: str
    producer_phase_label: str
    status_label: str

    def validate(self) -> None:
        require_text("S27 v2 construction artifact family", self.artifact_family)
        if self.artifact_family not in ARTIFACT_FAMILIES:
            raise CarverBlocked("S27 v2 construction artifact family is not locked")
        require_text("S27 v2 construction artifact schema family", self.schema_family)
        if self.schema_family != REQUIRED_SCHEMA_FAMILY_BY_ARTIFACT_FAMILY[self.artifact_family]:
            raise CarverBlocked("S27 v2 construction artifact schema family is not locked")
        require_hash("S27 v2 construction artifact hash", self.artifact_hash)
        require_text("S27 v2 construction artifact producer phase label", self.producer_phase_label)
        require_text("S27 v2 construction artifact status label", self.status_label)
        if self.status_label != "PLANNED_STRUCTURAL_ARTIFACT_ONLY":
            raise CarverBlocked("S27 v2 construction artifact must remain planned structural artifact only")


@dataclass(frozen=True)
class ConstructionPhaseBoundary:
    phase_index: int
    phase_label: str
    required_input_hashes: tuple[str, ...]
    planned_output_artifacts: tuple[ConstructionArtifactReference, ...]
    blocked_gate_statuses: tuple[str, ...]
    phase_contract_hash: str

    def validate(self) -> None:
        require_integer("S27 v2 construction phase index", self.phase_index)
        if self.phase_index < 1 or self.phase_index > len(PLANNED_CONSTRUCTION_PHASES):
            raise CarverBlocked("S27 v2 construction phase index is outside the planned phase range")
        expected_label = PLANNED_CONSTRUCTION_PHASES[self.phase_index - 1]
        require_text("S27 v2 construction phase label", self.phase_label)
        if self.phase_label != expected_label:
            raise CarverBlocked("S27 v2 construction phase label does not match the locked phase order")
        require_non_empty_tuple("S27 v2 construction phase required input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 construction phase required input hash", input_hash)
        if not isinstance(self.planned_output_artifacts, tuple):
            raise CarverBlocked("S27 v2 construction phase planned output artifacts must be a tuple")
        required_artifact_families = REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE[self.phase_label]
        if tuple(artifact.artifact_family for artifact in self.planned_output_artifacts) != required_artifact_families:
            raise CarverBlocked("S27 v2 construction phase artifacts must match locked artifact tuple")
        for artifact in self.planned_output_artifacts:
            artifact.validate()
            if artifact.producer_phase_label != self.phase_label:
                raise CarverBlocked("S27 v2 construction output artifact producer phase mismatch")
        require_non_empty_tuple("S27 v2 construction phase blocked gate statuses", self.blocked_gate_statuses)
        for blocked_status in self.blocked_gate_statuses:
            require_text("S27 v2 construction phase blocked gate status", blocked_status)
            if blocked_status not in REQUIRED_UNRESOLVED_GATE_LABELS:
                raise CarverBlocked("S27 v2 construction phase gate is not in the locked unresolved gate tuple")
        require_hash("S27 v2 construction phase contract hash", self.phase_contract_hash)


@dataclass(frozen=True)
class ParserFileReplayConstructionContract:
    status: str
    planning_config_hash: str
    parser_plan_bundle_hash: str
    input_directory_declaration_hash: str
    artifact_manifest_plan_hash: str
    construction_phases: tuple[ConstructionPhaseBoundary, ...]
    construction_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 parser/file replay construction status", self.status)
        if self.status != S27_V2_CONSTRUCTION_SCAFFOLD_ONLY_STATUS:
            raise CarverBlocked("S27 v2 construction contract must remain scaffold-only")
        require_hash("S27 v2 construction planning config hash", self.planning_config_hash)
        require_hash("S27 v2 construction parser plan bundle hash", self.parser_plan_bundle_hash)
        require_hash(
            "S27 v2 construction input directory declaration hash",
            self.input_directory_declaration_hash,
        )
        require_hash("S27 v2 construction artifact manifest plan hash", self.artifact_manifest_plan_hash)
        require_non_empty_tuple("S27 v2 construction phases", self.construction_phases)
        if len(self.construction_phases) != len(PLANNED_CONSTRUCTION_PHASES):
            raise CarverBlocked("S27 v2 construction contract must include every locked construction phase")
        previous_index = 0
        seen_labels: set[str] = set()
        for phase in self.construction_phases:
            phase.validate()
            if phase.phase_index <= previous_index:
                raise CarverBlocked("S27 v2 construction phases must be strictly ordered")
            if phase.phase_label in seen_labels:
                raise CarverBlocked("S27 v2 construction phase labels must be unique")
            previous_index = phase.phase_index
            seen_labels.add(phase.phase_label)
        if tuple(phase.phase_label for phase in self.construction_phases) != PLANNED_CONSTRUCTION_PHASES:
            raise CarverBlocked("S27 v2 construction phases must match the locked phase tuple")
        covered_gates = [
            blocked_status
            for phase in self.construction_phases
            for blocked_status in phase.blocked_gate_statuses
        ]
        if tuple(covered_gates) != REQUIRED_UNRESOLVED_GATE_LABELS:
            raise CarverBlocked("S27 v2 construction contract must cover every locked unresolved gate exactly once")
        covered_artifacts = tuple(
            artifact.artifact_family
            for phase in self.construction_phases
            for artifact in phase.planned_output_artifacts
        )
        if covered_artifacts != ARTIFACT_FAMILIES:
            raise CarverBlocked("S27 v2 construction contract must cover every locked artifact exactly once")
        require_hash("S27 v2 construction contract hash", self.construction_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 construction contract must preserve non-authorizations")

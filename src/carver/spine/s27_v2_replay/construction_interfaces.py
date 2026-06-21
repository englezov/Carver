from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .artifact_manifest_plan import ArtifactManifestPlan
from .constants import ARTIFACT_FAMILIES, S27_V2_REPLAY_NON_AUTHORIZATION
from .construction_contract import (
    PLANNED_CONSTRUCTION_PHASES,
    ParserFileReplayConstructionContract,
)
from .replay_builder_plan import TrustedReplayBuilderPlan
from .replay_config import S27ReplayPlanningConfig
from .validation import (
    require_hash,
    require_hash_map,
    require_integer,
    require_non_empty_tuple,
    require_text,
    require_tuple,
)


S27_V2_REPLAY_CONSTRUCTION_INTERFACE_ONLY_STATUS = (
    "S27_V2_REPLAY_CONSTRUCTION_INTERFACE_ONLY"
)

PLANNING_CONFIG_HASH = "PLANNING_CONFIG_HASH"
SOURCE_LOCK_HASH = "SOURCE_LOCK_HASH"
LOCAL_DATA_CONTRACT_HASH = "LOCAL_DATA_CONTRACT_HASH"
PROVENANCE_DESIGN_HASH = "PROVENANCE_DESIGN_HASH"
PARSER_PLAN_BUNDLE_HASH = "PARSER_PLAN_BUNDLE_HASH"
INPUT_DIRECTORY_DECLARATION_HASH = "INPUT_DIRECTORY_DECLARATION_HASH"
ARTIFACT_MANIFEST_PLAN_HASH = "ARTIFACT_MANIFEST_PLAN_HASH"
RAW_FILE_HASH_SET_HASH = "RAW_FILE_HASH_SET_HASH"
SOURCE_UNIVERSE_MANIFEST_HASH = "SOURCE_UNIVERSE_MANIFEST_HASH"
SOURCE_ROW_BATCH_CONTRACT_HASH = "SOURCE_ROW_BATCH_CONTRACT_HASH"
SOURCE_ROW_BATCH_SET_HASH = "SOURCE_ROW_BATCH_SET_HASH"
ROW_LOCATOR_HASH = "ROW_LOCATOR_HASH"
SOURCE_ROW_SELECTION_AUTHORITY_HASH = "SOURCE_ROW_SELECTION_AUTHORITY_HASH"
SESSION_CALENDAR_POLICY_HASH = "SESSION_CALENDAR_POLICY_HASH"
ROLL_CALENDAR_POLICY_HASH = "ROLL_CALENDAR_POLICY_HASH"
TICK_ROUNDING_POLICY_HASH = "TICK_ROUNDING_POLICY_HASH"
COMMISSION_POLICY_HASH = "COMMISSION_POLICY_HASH"
SPREAD_UNIT_POLICY_HASH = "SPREAD_UNIT_POLICY_HASH"
CONTRACT_MULTIPLIER_CURRENCY_POLICY_HASH = "CONTRACT_MULTIPLIER_CURRENCY_POLICY_HASH"
DAILY_HOURLY_COMPATIBILITY_POLICY_HASH = "DAILY_HOURLY_COMPATIBILITY_POLICY_HASH"
ACTIVE_EVIDENCE_MANIFEST_HASH = "ACTIVE_EVIDENCE_MANIFEST_HASH"
CANONICAL_SERIALIZATION_POLICY_HASH = "CANONICAL_SERIALIZATION_POLICY_HASH"
CONSTRUCTION_PHASE_CONTRACT_HASH = "CONSTRUCTION_PHASE_CONTRACT_HASH"
BUILDER_STEP_PLAN_HASH = "BUILDER_STEP_PLAN_HASH"
INTERFACE_ANCHOR_INPUT_LABELS = (
    CONSTRUCTION_PHASE_CONTRACT_HASH,
    BUILDER_STEP_PLAN_HASH,
)

ARTIFACT_HASH_LABEL_BY_FAMILY = {
    artifact_family: f"{artifact_family}_HASH"
    for artifact_family in ARTIFACT_FAMILIES
}

REQUIRED_INTERFACE_INPUT_LABELS_BY_PHASE = {
    "CANONICAL_SERIALIZATION_AND_HASH_POLICY_VALIDATION": (
        PLANNING_CONFIG_HASH,
        SOURCE_LOCK_HASH,
        PROVENANCE_DESIGN_HASH,
        CANONICAL_SERIALIZATION_POLICY_HASH,
        ARTIFACT_MANIFEST_PLAN_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "FILE_DECLARATION_AND_RAW_FILE_HASH_SET_BINDING": (
        PLANNING_CONFIG_HASH,
        INPUT_DIRECTORY_DECLARATION_HASH,
        LOCAL_DATA_CONTRACT_HASH,
        RAW_FILE_HASH_SET_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "SOURCE_UNIVERSE_AND_ROW_LOCATOR_CONSTRUCTION": (
        INPUT_DIRECTORY_DECLARATION_HASH,
        SOURCE_UNIVERSE_MANIFEST_HASH,
        RAW_FILE_HASH_SET_HASH,
        ROW_LOCATOR_HASH,
        SOURCE_ROW_BATCH_CONTRACT_HASH,
        SOURCE_ROW_BATCH_SET_HASH,
        SOURCE_ROW_SELECTION_AUTHORITY_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "DAILY_HOURLY_LEVEL_COMPATIBILITY_CONSTRUCTION": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["SOURCE_INPUT_MANIFEST"],
        DAILY_HOURLY_COMPATIBILITY_POLICY_HASH,
        ROW_LOCATOR_HASH,
        SOURCE_ROW_SELECTION_AUTHORITY_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "RUNTIME_HISTORY_CONSTRUCTION": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["SOURCE_INPUT_MANIFEST"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER"],
        SOURCE_ROW_BATCH_SET_HASH,
        ROW_LOCATOR_HASH,
        SESSION_CALENDAR_POLICY_HASH,
        ROLL_CALENDAR_POLICY_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "FORECAST_AND_DESIRED_POSITION_CONSTRUCTION": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM"],
        SOURCE_LOCK_HASH,
        TICK_ROUNDING_POLICY_HASH,
        CONTRACT_MULTIPLIER_CURRENCY_POLICY_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "ORDER_AND_TRANSITION_CONSTRUCTION": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["FORECAST_REPLAY_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["DESIRED_POSITION_LEDGER"],
        TICK_ROUNDING_POLICY_HASH,
        ROLL_CALENDAR_POLICY_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "FILL_CONSTRUCTION": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["SOURCE_INPUT_MANIFEST"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["LIMIT_ORDER_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["MARKET_ORDER_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["WORKING_ORDER_TRANSITION_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["REMAINING_LIMIT_ORDER_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["CANCELED_LIMIT_ORDER_LEDGER"],
        SOURCE_ROW_SELECTION_AUTHORITY_HASH,
        SESSION_CALENDAR_POLICY_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "COST_CONSTRUCTION": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["FILL_LEDGER"],
        COMMISSION_POLICY_HASH,
        SPREAD_UNIT_POLICY_HASH,
        CONTRACT_MULTIPLIER_CURRENCY_POLICY_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "PNL_CONSTRUCTION": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["FILL_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["COMMISSION_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["SPREAD_COST_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER"],
        CONTRACT_MULTIPLIER_CURRENCY_POLICY_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "VALIDATION_PROVENANCE_EVIDENCE_MANIFEST_CONSTRUCTION": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["SOURCE_INPUT_MANIFEST"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["FORECAST_REPLAY_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["DESIRED_POSITION_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["LIMIT_ORDER_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["MARKET_ORDER_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["WORKING_ORDER_TRANSITION_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["REMAINING_LIMIT_ORDER_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["CANCELED_LIMIT_ORDER_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["FILL_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["COMMISSION_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["SPREAD_COST_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["PNL_LEDGER"],
        ACTIVE_EVIDENCE_MANIFEST_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
    "FINAL_TRUSTED_REPLAY_BUNDLE_ASSEMBLY": (
        ARTIFACT_HASH_LABEL_BY_FAMILY["VALIDATION_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["PROVENANCE_AND_HASH_LEDGER"],
        ARTIFACT_HASH_LABEL_BY_FAMILY["LOCAL_HOSTILE_AUDIT_RESULT"],
        ACTIVE_EVIDENCE_MANIFEST_HASH,
        CONSTRUCTION_PHASE_CONTRACT_HASH,
        BUILDER_STEP_PLAN_HASH,
    ),
}


@dataclass(frozen=True)
class ReplayConstructionInputBinding:
    input_label: str
    bound_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 construction input binding requires bundle-derived active authority"
        )

    def _validate_against_bundle_authority(
        self,
        active_hash_by_input_label: dict[str, str],
    ) -> None:
        require_text("S27 v2 construction input label", self.input_label)
        require_hash("S27 v2 construction input bound hash", self.bound_hash)
        if self.input_label not in active_hash_by_input_label:
            raise CarverBlocked("S27 v2 construction input label is not active for this phase")
        if self.bound_hash != active_hash_by_input_label[self.input_label]:
            raise CarverBlocked("S27 v2 construction input must bind active authority")


@dataclass(frozen=True)
class ReplayConstructionOutputDeclaration:
    artifact_family: str
    output_hash_label: str
    planned_artifact_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 construction output declaration requires bundle-derived artifact authority"
        )

    def _validate_against_bundle_artifact_authority(
        self,
        active_hash_by_artifact_family: dict[str, str],
    ) -> None:
        require_text("S27 v2 construction output artifact family", self.artifact_family)
        if self.artifact_family not in ARTIFACT_FAMILIES:
            raise CarverBlocked("S27 v2 construction output artifact family is not locked")
        require_text("S27 v2 construction output hash label", self.output_hash_label)
        if self.output_hash_label != ARTIFACT_HASH_LABEL_BY_FAMILY[self.artifact_family]:
            raise CarverBlocked("S27 v2 construction output hash label must be locked")
        require_hash("S27 v2 construction planned artifact hash", self.planned_artifact_hash)
        if active_hash_by_artifact_family[self.artifact_family] != self.planned_artifact_hash:
            raise CarverBlocked("S27 v2 construction output must bind planned artifact authority")


@dataclass(frozen=True)
class ReplayConstructionPhaseInterface:
    phase_index: int
    phase_label: str
    input_bindings: tuple[ReplayConstructionInputBinding, ...]
    output_declarations: tuple[ReplayConstructionOutputDeclaration, ...]
    interface_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 construction phase interface requires bundle-derived active authority"
        )

    def _validate_against_bundle_phase_authority(
        self,
        phase_required_input_hashes: tuple[str, ...],
        phase_contract_hash: str,
        step_plan_hash: str,
        active_global_hash_by_label: dict[str, str],
        active_hash_by_artifact_family: dict[str, str],
        expected_output_families: tuple[str, ...],
    ) -> None:
        require_integer("S27 v2 construction interface phase index", self.phase_index)
        if self.phase_index < 1 or self.phase_index > len(PLANNED_CONSTRUCTION_PHASES):
            raise CarverBlocked("S27 v2 construction interface phase index is outside locked range")
        require_text("S27 v2 construction interface phase label", self.phase_label)
        if self.phase_label != PLANNED_CONSTRUCTION_PHASES[self.phase_index - 1]:
            raise CarverBlocked("S27 v2 construction interface phase label mismatch")
        required_labels = REQUIRED_INTERFACE_INPUT_LABELS_BY_PHASE[self.phase_label]
        active_phase_hash_by_label = {
            label: (
                phase_contract_hash
                if label == CONSTRUCTION_PHASE_CONTRACT_HASH
                else step_plan_hash
                if label == BUILDER_STEP_PLAN_HASH
                else active_global_hash_by_label[label]
            )
            for label in required_labels
        }
        require_hash_map(
            "S27 v2 construction phase active input authority",
            active_phase_hash_by_label,
            required_labels,
        )
        require_non_empty_tuple("S27 v2 construction input bindings", self.input_bindings)
        if tuple(binding.input_label for binding in self.input_bindings) != required_labels:
            raise CarverBlocked("S27 v2 construction input bindings must match locked phase inputs")
        for binding in self.input_bindings:
            binding._validate_against_bundle_authority(active_phase_hash_by_label)
        construction_input_hashes = tuple(
            binding.bound_hash
            for binding in self.input_bindings
            if binding.input_label not in INTERFACE_ANCHOR_INPUT_LABELS
        )
        if construction_input_hashes != phase_required_input_hashes:
            raise CarverBlocked("S27 v2 construction input bindings must match phase contract inputs")
        require_tuple("S27 v2 construction output declarations", self.output_declarations)
        if tuple(output.artifact_family for output in self.output_declarations) != expected_output_families:
            raise CarverBlocked("S27 v2 construction output declarations must match locked phase outputs")
        for output in self.output_declarations:
            output._validate_against_bundle_artifact_authority(active_hash_by_artifact_family)
        require_hash("S27 v2 construction phase interface hash", self.interface_hash)


@dataclass(frozen=True)
class ReplayConstructionInterfaceBundle:
    status: str
    planning_config: S27ReplayPlanningConfig
    construction_contract: ParserFileReplayConstructionContract
    builder_plan: TrustedReplayBuilderPlan
    artifact_manifest_plan: ArtifactManifestPlan
    phase_interfaces: tuple[ReplayConstructionPhaseInterface, ...]
    construction_interface_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 replay construction interface status", self.status)
        if self.status != S27_V2_REPLAY_CONSTRUCTION_INTERFACE_ONLY_STATUS:
            raise CarverBlocked("S27 v2 replay construction interface must remain scaffold-only")
        self.planning_config.validate()
        self.construction_contract.validate()
        self.builder_plan.validate()
        self.artifact_manifest_plan.validate()
        if tuple(REQUIRED_INTERFACE_INPUT_LABELS_BY_PHASE) != PLANNED_CONSTRUCTION_PHASES:
            raise CarverBlocked("S27 v2 construction interface input map must cover locked phases")
        self._validate_cross_contract_bindings()
        require_non_empty_tuple("S27 v2 replay construction phase interfaces", self.phase_interfaces)
        if len(self.phase_interfaces) != len(PLANNED_CONSTRUCTION_PHASES):
            raise CarverBlocked("S27 v2 replay construction interface must cover every phase")
        active_global_hash_by_label = self._active_global_hash_by_label()
        active_hash_by_artifact_family = self._active_hash_by_artifact_family()
        for phase_interface, phase_contract, step_plan in zip(
            self.phase_interfaces,
            self.construction_contract.construction_phases,
            self.builder_plan.construction_steps,
            strict=True,
        ):
            if phase_interface.phase_label != phase_contract.phase_label:
                raise CarverBlocked("S27 v2 construction interface phase-contract label mismatch")
            if phase_interface.phase_label != step_plan.step_label:
                raise CarverBlocked("S27 v2 construction interface builder-step label mismatch")
            for emission in step_plan.ledger_emissions:
                if emission.required_input_hashes != phase_contract.required_input_hashes:
                    raise CarverBlocked(
                        "S27 v2 construction interface builder emissions must bind phase inputs"
                    )
            phase_interface._validate_against_bundle_phase_authority(
                phase_contract.required_input_hashes,
                phase_contract.phase_contract_hash,
                step_plan.step_plan_hash,
                active_global_hash_by_label,
                active_hash_by_artifact_family,
                tuple(artifact.artifact_family for artifact in phase_contract.planned_output_artifacts),
            )
        require_hash(
            "S27 v2 replay construction interface bundle hash",
            self.construction_interface_bundle_hash,
        )
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 replay construction interface must preserve non-authorizations")

    def _validate_cross_contract_bindings(self) -> None:
        if self.construction_contract.planning_config_hash != self.planning_config.planning_config_hash:
            raise CarverBlocked("S27 v2 construction interface planning-config hash mismatch")
        if self.builder_plan.planning_config_hash != self.planning_config.planning_config_hash:
            raise CarverBlocked("S27 v2 construction interface builder planning-config hash mismatch")
        if self.construction_contract.parser_plan_bundle_hash != self.builder_plan.parser_plan_bundle_hash:
            raise CarverBlocked("S27 v2 construction interface parser plan hash mismatch")
        if (
            self.construction_contract.input_directory_declaration_hash
            != self.planning_config.input_directory.input_directory_declaration_hash
        ):
            raise CarverBlocked("S27 v2 construction interface input-directory hash mismatch")
        if (
            self.construction_contract.artifact_manifest_plan_hash
            != self.artifact_manifest_plan.artifact_manifest_plan_hash
        ):
            raise CarverBlocked("S27 v2 construction interface artifact manifest plan hash mismatch")

    def _active_global_hash_by_label(self) -> dict[str, str]:
        policy_hashes = self.planning_config.policy_hashes
        return {
            PLANNING_CONFIG_HASH: self.planning_config.planning_config_hash,
            SOURCE_LOCK_HASH: policy_hashes.source_lock_hash,
            LOCAL_DATA_CONTRACT_HASH: policy_hashes.local_data_contract_hash,
            PROVENANCE_DESIGN_HASH: policy_hashes.provenance_design_hash,
            PARSER_PLAN_BUNDLE_HASH: self.construction_contract.parser_plan_bundle_hash,
            INPUT_DIRECTORY_DECLARATION_HASH: (
                self.planning_config.input_directory.input_directory_declaration_hash
            ),
            ARTIFACT_MANIFEST_PLAN_HASH: self.artifact_manifest_plan.artifact_manifest_plan_hash,
            RAW_FILE_HASH_SET_HASH: policy_hashes.raw_file_hash_set_hash,
            SOURCE_UNIVERSE_MANIFEST_HASH: policy_hashes.source_universe_manifest_hash,
            SOURCE_ROW_BATCH_CONTRACT_HASH: policy_hashes.source_row_batch_contract_hash,
            SOURCE_ROW_BATCH_SET_HASH: policy_hashes.source_row_batch_set_hash,
            ROW_LOCATOR_HASH: policy_hashes.row_locator_hash,
            SOURCE_ROW_SELECTION_AUTHORITY_HASH: policy_hashes.source_row_selection_authority_hash,
            SESSION_CALENDAR_POLICY_HASH: policy_hashes.session_calendar_policy_hash,
            ROLL_CALENDAR_POLICY_HASH: policy_hashes.roll_calendar_policy_hash,
            TICK_ROUNDING_POLICY_HASH: policy_hashes.tick_rounding_policy_hash,
            COMMISSION_POLICY_HASH: policy_hashes.commission_policy_hash,
            SPREAD_UNIT_POLICY_HASH: policy_hashes.spread_unit_policy_hash,
            CONTRACT_MULTIPLIER_CURRENCY_POLICY_HASH: (
                policy_hashes.contract_multiplier_currency_policy_hash
            ),
            DAILY_HOURLY_COMPATIBILITY_POLICY_HASH: (
                policy_hashes.daily_hourly_compatibility_policy_hash
            ),
            ACTIVE_EVIDENCE_MANIFEST_HASH: policy_hashes.active_evidence_manifest_hash,
            CANONICAL_SERIALIZATION_POLICY_HASH: (
                policy_hashes.canonical_serialization_policy.canonical_serialization_policy_hash
            ),
            **{
                ARTIFACT_HASH_LABEL_BY_FAMILY[artifact_family]: artifact_hash
                for artifact_family, artifact_hash in self._active_hash_by_artifact_family().items()
            },
        }

    def _active_hash_by_artifact_family(self) -> dict[str, str]:
        active_hashes = {
            artifact.artifact_family: artifact.artifact_hash
            for phase in self.construction_contract.construction_phases
            for artifact in phase.planned_output_artifacts
        }
        if tuple(active_hashes) != ARTIFACT_FAMILIES:
            raise CarverBlocked("S27 v2 construction interface artifact authority must cover locked families")
        return active_hashes

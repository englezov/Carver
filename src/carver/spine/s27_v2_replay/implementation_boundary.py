from __future__ import annotations

from dataclasses import dataclass
from typing import NoReturn

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .construction_contract import (
    PLANNED_CONSTRUCTION_PHASES,
    REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE,
)
from .construction_interfaces import (
    REQUIRED_INTERFACE_INPUT_LABELS_BY_PHASE,
    ReplayConstructionInterfaceBundle,
)
from .runner import ReplayExecutionBlocked
from .validation import require_hash, require_integer, require_non_empty_tuple, require_text, require_tuple


S27_V2_IMPLEMENTATION_BOUNDARY_AND_PHASE_REGISTRY_STATUS = (
    "S27_V2_PARSER_FILE_REPLAY_IMPLEMENTATION_BOUNDARY_AND_PHASE_REGISTRY_ONLY"
)
S27_V2_EXECUTION_AUTHORIZATION_BOUNDARY_STATUS = (
    "S27_V2_PARSER_FILE_REPLAY_EXECUTION_AUTHORIZATION_BOUNDARY_ONLY"
)
S27_V2_FUTURE_BUILDER_SURFACE_DECLARATION_STATUS = (
    "S27_V2_FUTURE_BUILDER_SURFACE_DECLARATION_ONLY"
)

REQUIRED_FUTURE_BUILDER_SURFACE_BY_PHASE = {
    "CANONICAL_SERIALIZATION_AND_HASH_POLICY_VALIDATION": (
        "build_canonical_serialization_and_hash_policy_validation"
    ),
    "FILE_DECLARATION_AND_RAW_FILE_HASH_SET_BINDING": (
        "build_file_declaration_and_raw_file_hash_set_binding"
    ),
    "SOURCE_UNIVERSE_AND_ROW_LOCATOR_CONSTRUCTION": (
        "build_source_universe_and_row_locator"
    ),
    "DAILY_HOURLY_LEVEL_COMPATIBILITY_CONSTRUCTION": (
        "build_daily_hourly_level_compatibility"
    ),
    "RUNTIME_HISTORY_CONSTRUCTION": "build_runtime_history",
    "FORECAST_AND_DESIRED_POSITION_CONSTRUCTION": (
        "build_forecast_and_desired_position"
    ),
    "ORDER_AND_TRANSITION_CONSTRUCTION": "build_order_and_transition",
    "FILL_CONSTRUCTION": "build_fill",
    "COST_CONSTRUCTION": "build_cost",
    "PNL_CONSTRUCTION": "build_pnl",
    "VALIDATION_PROVENANCE_EVIDENCE_MANIFEST_CONSTRUCTION": (
        "build_validation_provenance_evidence_manifest"
    ),
    "FINAL_TRUSTED_REPLAY_BUNDLE_ASSEMBLY": "build_final_trusted_replay_bundle",
}


@dataclass(frozen=True)
class ParserFileReplayExecutionAuthorizationBoundary:
    status: str
    authorization_label: str
    authorization_scope_hash: str
    construction_interface_bundle_hash: str
    file_read_authorized: bool = False
    raw_file_hash_authorized: bool = False
    parser_execution_authorized: bool = False
    replay_execution_authorized: bool = False
    output_write_authorized: bool = False
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 execution authorization boundary status", self.status)
        if self.status != S27_V2_EXECUTION_AUTHORIZATION_BOUNDARY_STATUS:
            raise CarverBlocked("S27 v2 execution authorization boundary must remain scaffold-only")
        require_text("S27 v2 execution authorization label", self.authorization_label)
        require_hash("S27 v2 execution authorization scope hash", self.authorization_scope_hash)
        require_hash(
            "S27 v2 execution authorization construction-interface bundle hash",
            self.construction_interface_bundle_hash,
        )
        if any(
            flag is not False
            for flag in (
                self.file_read_authorized,
                self.raw_file_hash_authorized,
                self.parser_execution_authorized,
                self.replay_execution_authorized,
                self.output_write_authorized,
            )
        ):
            raise CarverBlocked("S27 v2 execution authorization boundary must remain non-executing")
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 execution authorization boundary must preserve non-authorizations")


@dataclass(frozen=True)
class FutureBuilderSurfaceDeclaration:
    phase_index: int
    phase_label: str
    builder_surface_name: str
    required_input_labels: tuple[str, ...]
    planned_output_artifact_families: tuple[str, ...]
    requires_execution_authorization_boundary: bool
    requires_replay_construction_interface_bundle: bool
    surface_hash: str
    status: str = S27_V2_FUTURE_BUILDER_SURFACE_DECLARATION_STATUS

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 future builder surface requires implementation-boundary registry authority"
        )

    def _validate_against_registry_authority(self) -> None:
        require_text("S27 v2 future builder surface status", self.status)
        if self.status != S27_V2_FUTURE_BUILDER_SURFACE_DECLARATION_STATUS:
            raise CarverBlocked("S27 v2 future builder surface must remain declaration-only")
        require_integer("S27 v2 future builder phase index", self.phase_index)
        if self.phase_index < 1 or self.phase_index > len(PLANNED_CONSTRUCTION_PHASES):
            raise CarverBlocked("S27 v2 future builder phase index is outside locked range")
        require_text("S27 v2 future builder phase label", self.phase_label)
        if self.phase_label != PLANNED_CONSTRUCTION_PHASES[self.phase_index - 1]:
            raise CarverBlocked("S27 v2 future builder phase label mismatch")
        require_text("S27 v2 future builder surface name", self.builder_surface_name)
        if self.builder_surface_name != REQUIRED_FUTURE_BUILDER_SURFACE_BY_PHASE[self.phase_label]:
            raise CarverBlocked("S27 v2 future builder surface name must match locked phase")
        require_non_empty_tuple("S27 v2 future builder required input labels", self.required_input_labels)
        if self.required_input_labels != REQUIRED_INTERFACE_INPUT_LABELS_BY_PHASE[self.phase_label]:
            raise CarverBlocked("S27 v2 future builder inputs must match construction-interface labels")
        require_tuple("S27 v2 future builder planned output artifacts", self.planned_output_artifact_families)
        if self.planned_output_artifact_families != REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE[self.phase_label]:
            raise CarverBlocked("S27 v2 future builder outputs must match locked construction artifacts")
        if self.requires_execution_authorization_boundary is not True:
            raise CarverBlocked("S27 v2 future builder must require execution authorization boundary")
        if self.requires_replay_construction_interface_bundle is not True:
            raise CarverBlocked("S27 v2 future builder must require construction-interface authority")
        require_hash("S27 v2 future builder surface hash", self.surface_hash)


@dataclass(frozen=True)
class ParserFileReplayImplementationBoundaryAndPhaseRegistry:
    status: str
    execution_authorization_boundary: ParserFileReplayExecutionAuthorizationBoundary
    construction_interface_bundle_hash: str
    future_builder_surfaces: tuple[FutureBuilderSurfaceDeclaration, ...]
    implementation_boundary_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 implementation boundary status", self.status)
        if self.status != S27_V2_IMPLEMENTATION_BOUNDARY_AND_PHASE_REGISTRY_STATUS:
            raise CarverBlocked("S27 v2 implementation boundary must remain scaffold-only")
        if tuple(REQUIRED_FUTURE_BUILDER_SURFACE_BY_PHASE) != PLANNED_CONSTRUCTION_PHASES:
            raise CarverBlocked("S27 v2 future builder surface map must cover locked phases")
        self.execution_authorization_boundary.validate()
        require_hash(
            "S27 v2 implementation boundary construction-interface bundle hash",
            self.construction_interface_bundle_hash,
        )
        if (
            self.construction_interface_bundle_hash
            != self.execution_authorization_boundary.construction_interface_bundle_hash
        ):
            raise CarverBlocked("S27 v2 implementation boundary must bind execution boundary to interface hash")
        require_non_empty_tuple("S27 v2 future builder surfaces", self.future_builder_surfaces)
        if len(self.future_builder_surfaces) != len(PLANNED_CONSTRUCTION_PHASES):
            raise CarverBlocked("S27 v2 future builder registry must cover every locked phase")
        if tuple(surface.phase_label for surface in self.future_builder_surfaces) != PLANNED_CONSTRUCTION_PHASES:
            raise CarverBlocked("S27 v2 future builder registry must match locked phase tuple")
        if tuple(surface.builder_surface_name for surface in self.future_builder_surfaces) != tuple(
            REQUIRED_FUTURE_BUILDER_SURFACE_BY_PHASE[phase]
            for phase in PLANNED_CONSTRUCTION_PHASES
        ):
            raise CarverBlocked("S27 v2 future builder registry must match locked surface tuple")
        for surface in self.future_builder_surfaces:
            surface._validate_against_registry_authority()
        require_hash("S27 v2 implementation boundary hash", self.implementation_boundary_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 implementation boundary must preserve non-authorizations")

    def block_future_builder_surface(
        self,
        construction_interface: ReplayConstructionInterfaceBundle,
        phase_label: str,
    ) -> NoReturn:
        self.validate()
        construction_interface.validate()
        require_text("S27 v2 future builder requested phase label", phase_label)
        if phase_label not in PLANNED_CONSTRUCTION_PHASES:
            raise CarverBlocked("S27 v2 future builder requested phase is not locked")
        if construction_interface.construction_interface_bundle_hash != self.construction_interface_bundle_hash:
            raise CarverBlocked("S27 v2 future builder must use active construction-interface authority")
        raise ReplayExecutionBlocked(
            "S27 v2 parser/file replay implementation is not authorized by boundary scaffold"
        )

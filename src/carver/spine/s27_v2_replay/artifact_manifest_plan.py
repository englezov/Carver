from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import (
    ACTIVE_EVIDENCE_STATUS_LABEL,
    REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES,
    SUPERSEDED_EVIDENCE_STATUS_LABEL,
)
from .validation import require_hash, require_non_empty_tuple, require_text, require_tuple


@dataclass(frozen=True)
class PlannedEvidenceArtifact:
    artifact_type: str
    planned_path_label: str
    planned_content_hash: str
    status_label: str

    def validate(self) -> None:
        require_text("S27 v2 planned evidence artifact type", self.artifact_type)
        require_text("S27 v2 planned evidence path label", self.planned_path_label)
        require_hash("S27 v2 planned evidence content hash", self.planned_content_hash)
        require_text("S27 v2 planned evidence status label", self.status_label)
        if self.status_label not in (ACTIVE_EVIDENCE_STATUS_LABEL, SUPERSEDED_EVIDENCE_STATUS_LABEL):
            raise CarverBlocked("S27 v2 planned evidence status label must be active or superseded")


@dataclass(frozen=True)
class PlannedEvidenceManifest:
    active_artifacts: tuple[PlannedEvidenceArtifact, ...]
    superseded_artifacts: tuple[PlannedEvidenceArtifact, ...]
    planned_manifest_hash: str

    def validate(self) -> None:
        require_non_empty_tuple("S27 v2 planned active evidence artifacts", self.active_artifacts)
        active_types: set[str] = set()
        for artifact in self.active_artifacts:
            artifact.validate()
            if artifact.status_label != ACTIVE_EVIDENCE_STATUS_LABEL:
                raise CarverBlocked("S27 v2 planned active artifact must use active evidence status")
            if artifact.artifact_type in active_types:
                raise CarverBlocked("S27 v2 planned active artifact types must be unique")
            active_types.add(artifact.artifact_type)
        missing = set(REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES) - active_types
        if missing:
            raise CarverBlocked("S27 v2 planned evidence manifest missing required artifact types")
        require_tuple("S27 v2 planned superseded evidence artifacts", self.superseded_artifacts)
        for artifact in self.superseded_artifacts:
            artifact.validate()
            if artifact.status_label != SUPERSEDED_EVIDENCE_STATUS_LABEL:
                raise CarverBlocked("S27 v2 planned superseded artifact must use superseded evidence status")
        require_hash("S27 v2 planned evidence manifest hash", self.planned_manifest_hash)


@dataclass(frozen=True)
class ArtifactManifestPlan:
    planned_evidence_manifest: PlannedEvidenceManifest
    manifest_policy_hash: str
    stale_evidence_gate_hash: str
    artifact_manifest_plan_hash: str

    def validate(self) -> None:
        self.planned_evidence_manifest.validate()
        require_hash("S27 v2 artifact manifest policy hash", self.manifest_policy_hash)
        require_hash("S27 v2 stale evidence gate hash", self.stale_evidence_gate_hash)
        require_hash("S27 v2 artifact manifest plan hash", self.artifact_manifest_plan_hash)

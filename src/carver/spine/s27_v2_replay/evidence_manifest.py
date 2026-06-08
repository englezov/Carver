from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..m0 import CarverBlocked
from .canonical_hash import HashedArtifact
from .constants import (
    ACTIVE_EVIDENCE_STATUS_LABEL,
    BLOCKED_EVIDENCE_MANIFEST,
    REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES,
    SUPERSEDED_EVIDENCE_STATUS_LABEL,
)
from .trust_root import ReplayTrustRoot
from .validation import require_hash, require_non_empty_tuple, require_text, require_tuple, require_utc_timestamp


@dataclass(frozen=True)
class SupersededArtifact:
    artifact: HashedArtifact
    supersession_reason: str
    superseding_artifact_hash: str
    effective_at_utc: datetime

    def validate(self) -> None:
        self.artifact.validate()
        if self.artifact.status_label != SUPERSEDED_EVIDENCE_STATUS_LABEL:
            raise CarverBlocked("S27 v2 superseded artifact must use superseded evidence status")
        require_text("S27 v2 supersession reason", self.supersession_reason)
        require_hash("S27 v2 superseding artifact hash", self.superseding_artifact_hash)
        require_utc_timestamp("S27 v2 supersession effective time", self.effective_at_utc)


@dataclass(frozen=True)
class EvidenceManifestEntry:
    artifact: HashedArtifact

    def validate(self) -> None:
        self.artifact.validate()
        if self.artifact.status_label != ACTIVE_EVIDENCE_STATUS_LABEL:
            raise CarverBlocked("S27 v2 active evidence entry must use active evidence status")


@dataclass(frozen=True)
class EvidenceManifest:
    active_entries: tuple[EvidenceManifestEntry, ...]
    superseded_artifacts: tuple[SupersededArtifact, ...]
    active_evidence_manifest_hash: str

    def validate(self) -> None:
        try:
            require_non_empty_tuple("S27 v2 active evidence manifest entries", self.active_entries)
            for entry in self.active_entries:
                entry.validate()
            active_types = tuple(entry.artifact.artifact_type for entry in self.active_entries)
            if active_types != REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES:
                raise CarverBlocked("S27 v2 active evidence manifest artifact types must match the locked tuple exactly")
            require_tuple("S27 v2 superseded evidence artifacts", self.superseded_artifacts)
            for artifact in self.superseded_artifacts:
                artifact.validate()
            require_hash("S27 v2 active evidence manifest hash", self.active_evidence_manifest_hash)
        except CarverBlocked as exc:
            raise CarverBlocked(BLOCKED_EVIDENCE_MANIFEST) from exc

    def active_hash_by_type(self, artifact_type: str) -> str:
        require_text("S27 v2 evidence manifest artifact type lookup", artifact_type)
        matches = [
            entry.artifact.content_hash
            for entry in self.active_entries
            if entry.artifact.artifact_type == artifact_type
        ]
        if len(matches) != 1:
            raise CarverBlocked(BLOCKED_EVIDENCE_MANIFEST)
        return matches[0]


def require_evidence_manifest_matches_trust_root(
    replay_trust_root: ReplayTrustRoot,
    evidence_manifest: EvidenceManifest,
) -> None:
    replay_trust_root.validate()
    evidence_manifest.validate()
    if replay_trust_root.active_evidence_manifest_hash != evidence_manifest.active_evidence_manifest_hash:
        raise CarverBlocked("S27 v2 trust root and evidence manifest hash mismatch")
    expected_manifest_hashes = (
        ("SOURCE_LOCK", replay_trust_root.source_lock_hash),
        ("LOCAL_DATA_CONTRACT", replay_trust_root.local_data_contract_hash),
        ("PROVENANCE_DESIGN", replay_trust_root.provenance_design_hash),
        ("RUNNER_IMPLEMENTATION", replay_trust_root.runner_implementation_hash),
        ("PARSER_EXTRACTOR_SOURCE", replay_trust_root.parser_extractor_source_hash),
        ("DEPENDENCY_RUNTIME_MANIFEST", replay_trust_root.dependency_runtime_manifest_hash),
        ("REPLAY_CONFIG", replay_trust_root.replay_config_hash),
        ("SOURCE_INPUT_UNIVERSE_MANIFEST", replay_trust_root.source_input_universe_manifest_hash),
        ("RAW_SOURCE_FILE_HASH_SET", replay_trust_root.raw_source_file_hash_set_hash),
        ("SOURCE_ROW_BATCH_CONTRACT", replay_trust_root.source_row_batch_contract_hash),
        ("SOURCE_ROW_BATCH_SET", replay_trust_root.source_row_batch_set_hash),
        ("SOURCE_ROW_LOCATOR", replay_trust_root.source_row_locator_hash),
        ("SOURCE_ROW_SELECTION_AUTHORITY", replay_trust_root.source_row_selection_authority_hash),
        (
            "CANONICAL_SERIALIZATION_POLICY",
            replay_trust_root.canonical_serialization_policy.canonical_serialization_policy_hash,
        ),
        ("CANONICAL_SERIALIZATION_SCHEMA", replay_trust_root.canonical_serialization_policy.schema_hash),
        (
            "HASH_ALGORITHM_VERSION",
            replay_trust_root.canonical_serialization_policy.hash_algorithm_version_hash,
        ),
        (
            "FIELD_ORDERING_POLICY",
            replay_trust_root.canonical_serialization_policy.field_ordering_policy_hash,
        ),
        (
            "DECIMAL_FLOAT_NORMALIZATION_POLICY",
            replay_trust_root.canonical_serialization_policy.decimal_float_normalization_policy_hash,
        ),
        (
            "TIMEZONE_NORMALIZATION_POLICY",
            replay_trust_root.canonical_serialization_policy.timezone_normalization_policy_hash,
        ),
        (
            "ROW_ORDERING_COLLATION_POLICY",
            replay_trust_root.canonical_serialization_policy.row_ordering_collation_policy_hash,
        ),
        (
            "NULL_MISSING_SENTINEL_POLICY",
            replay_trust_root.canonical_serialization_policy.null_missing_sentinel_policy_hash,
        ),
        (
            "STRING_ENCODING_POLICY",
            replay_trust_root.canonical_serialization_policy.string_encoding_policy_hash,
        ),
        (
            "HASH_PAYLOAD_VERSION_POLICY",
            replay_trust_root.canonical_serialization_policy.hash_payload_version_policy_hash,
        ),
        ("SESSION_CALENDAR_POLICY", replay_trust_root.session_calendar_policy_hash),
        ("ROLL_CALENDAR_POLICY", replay_trust_root.roll_calendar_policy_hash),
        ("TICK_ROUNDING_POLICY", replay_trust_root.tick_rounding_policy_hash),
        ("COMMISSION_POLICY", replay_trust_root.commission_policy_hash),
        ("SPREAD_UNIT_POLICY", replay_trust_root.spread_unit_policy_hash),
        (
            "CONTRACT_MULTIPLIER_CURRENCY_POLICY",
            replay_trust_root.contract_multiplier_currency_policy_hash,
        ),
        (
            "DAILY_HOURLY_COMPATIBILITY_POLICY",
            replay_trust_root.daily_hourly_level_compatibility_policy_hash,
        ),
        (
            "STALE_EVIDENCE_SUPERSESSION_MANIFEST",
            replay_trust_root.stale_evidence_supersession_manifest_hash,
        ),
    )
    for artifact_type, expected_hash in expected_manifest_hashes:
        if evidence_manifest.active_hash_by_type(artifact_type) != expected_hash:
            raise CarverBlocked("S27 v2 evidence manifest artifact hash must match trust root")

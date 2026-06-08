from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import BLOCKED_CANONICAL_SERIALIZATION, S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_hash_map, require_text


S27_V2_CANONICAL_SERIALIZATION_POLICY_CONTRACT_ONLY_STATUS = (
    "S27_V2_CANONICAL_SERIALIZATION_POLICY_CONTRACT_ONLY"
)
S27_V2_CANONICAL_ROW_HASH_CONTRACT_ONLY_STATUS = "S27_V2_CANONICAL_ROW_HASH_CONTRACT_ONLY"

CANONICAL_SERIALIZATION_COMPONENT_LABELS = (
    "CANONICAL_SERIALIZATION_SCHEMA",
    "HASH_ALGORITHM_VERSION",
    "FIELD_ORDERING_POLICY",
    "DECIMAL_FLOAT_NORMALIZATION_POLICY",
    "TIMEZONE_NORMALIZATION_POLICY",
    "ROW_ORDERING_COLLATION_POLICY",
    "NULL_MISSING_SENTINEL_POLICY",
    "STRING_ENCODING_POLICY",
    "HASH_PAYLOAD_VERSION_POLICY",
)


@dataclass(frozen=True)
class HashReference:
    name: str
    sha256: str

    def validate(self) -> None:
        require_text("S27 v2 hash reference name", self.name)
        require_hash(f"S27 v2 hash reference {self.name}", self.sha256)


@dataclass(frozen=True)
class HashedArtifact:
    artifact_type: str
    path: str
    content_hash: str
    status_label: str

    def validate(self) -> None:
        require_text("S27 v2 artifact type", self.artifact_type)
        require_text("S27 v2 artifact path", self.path)
        require_hash("S27 v2 artifact content hash", self.content_hash)
        require_text("S27 v2 artifact status label", self.status_label)


@dataclass(frozen=True)
class CanonicalSerializationPolicy:
    status_label: str
    schema_hash: str
    hash_algorithm_version_hash: str
    field_ordering_policy_hash: str
    decimal_float_normalization_policy_hash: str
    timezone_normalization_policy_hash: str
    row_ordering_collation_policy_hash: str
    null_missing_sentinel_policy_hash: str
    string_encoding_policy_hash: str
    hash_payload_version_policy_hash: str
    canonical_serialization_policy_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def active_component_hash_by_label(self) -> dict[str, str]:
        return {
            "CANONICAL_SERIALIZATION_SCHEMA": self.schema_hash,
            "HASH_ALGORITHM_VERSION": self.hash_algorithm_version_hash,
            "FIELD_ORDERING_POLICY": self.field_ordering_policy_hash,
            "DECIMAL_FLOAT_NORMALIZATION_POLICY": self.decimal_float_normalization_policy_hash,
            "TIMEZONE_NORMALIZATION_POLICY": self.timezone_normalization_policy_hash,
            "ROW_ORDERING_COLLATION_POLICY": self.row_ordering_collation_policy_hash,
            "NULL_MISSING_SENTINEL_POLICY": self.null_missing_sentinel_policy_hash,
            "STRING_ENCODING_POLICY": self.string_encoding_policy_hash,
            "HASH_PAYLOAD_VERSION_POLICY": self.hash_payload_version_policy_hash,
        }

    def validate(self) -> None:
        try:
            require_text("S27 v2 canonical serialization policy status", self.status_label)
            if self.status_label != S27_V2_CANONICAL_SERIALIZATION_POLICY_CONTRACT_ONLY_STATUS:
                raise CarverBlocked("S27 v2 canonical serialization policy must remain contract-only")
            require_hash("S27 v2 canonical serialization schema hash", self.schema_hash)
            require_hash("S27 v2 hash algorithm version hash", self.hash_algorithm_version_hash)
            require_hash("S27 v2 field ordering policy hash", self.field_ordering_policy_hash)
            require_hash(
                "S27 v2 decimal/float normalization policy hash",
                self.decimal_float_normalization_policy_hash,
            )
            require_hash("S27 v2 timezone normalization policy hash", self.timezone_normalization_policy_hash)
            require_hash(
                "S27 v2 row ordering/collation policy hash",
                self.row_ordering_collation_policy_hash,
            )
            require_hash("S27 v2 null/missing sentinel policy hash", self.null_missing_sentinel_policy_hash)
            require_hash("S27 v2 string encoding policy hash", self.string_encoding_policy_hash)
            require_hash("S27 v2 hash payload version policy hash", self.hash_payload_version_policy_hash)
            require_hash(
                "S27 v2 canonical serialization policy hash",
                self.canonical_serialization_policy_hash,
            )
            require_hash_map(
                "S27 v2 canonical serialization active component map",
                self.active_component_hash_by_label(),
                CANONICAL_SERIALIZATION_COMPONENT_LABELS,
            )
            if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
                raise CarverBlocked("S27 v2 canonical serialization policy must preserve non-authorizations")
        except CarverBlocked as exc:
            raise CarverBlocked(BLOCKED_CANONICAL_SERIALIZATION) from exc


@dataclass(frozen=True)
class CanonicalRowHashContract:
    status_label: str
    row_family: str
    row_schema_family: str
    canonical_serialization_policy_hash: str
    field_ordering_policy_hash: str
    hash_payload_version_policy_hash: str
    row_hash_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 canonical row hash contract requires active canonical policy authority")

    def validate_against_policy(self, policy: CanonicalSerializationPolicy) -> None:
        try:
            policy.validate()
            require_text("S27 v2 canonical row hash contract status", self.status_label)
            if self.status_label != S27_V2_CANONICAL_ROW_HASH_CONTRACT_ONLY_STATUS:
                raise CarverBlocked("S27 v2 canonical row hash contract must remain contract-only")
            require_text("S27 v2 canonical row family", self.row_family)
            require_text("S27 v2 canonical row schema family", self.row_schema_family)
            require_hash(
                "S27 v2 canonical row serialization policy hash",
                self.canonical_serialization_policy_hash,
            )
            if self.canonical_serialization_policy_hash != policy.canonical_serialization_policy_hash:
                raise CarverBlocked("S27 v2 canonical row hash contract must bind active canonical policy")
            require_hash("S27 v2 canonical row field ordering policy hash", self.field_ordering_policy_hash)
            if self.field_ordering_policy_hash != policy.field_ordering_policy_hash:
                raise CarverBlocked("S27 v2 canonical row hash contract must bind active field ordering policy")
            require_hash(
                "S27 v2 canonical row hash payload version policy hash",
                self.hash_payload_version_policy_hash,
            )
            if self.hash_payload_version_policy_hash != policy.hash_payload_version_policy_hash:
                raise CarverBlocked("S27 v2 canonical row hash contract must bind active payload version policy")
            require_hash("S27 v2 canonical row hash contract hash", self.row_hash_contract_hash)
            if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
                raise CarverBlocked("S27 v2 canonical row hash contract must preserve non-authorizations")
        except CarverBlocked as exc:
            raise CarverBlocked(BLOCKED_CANONICAL_SERIALIZATION) from exc

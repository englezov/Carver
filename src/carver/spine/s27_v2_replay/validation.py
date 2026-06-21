from __future__ import annotations

from datetime import date, datetime, timedelta
from math import isfinite
from numbers import Integral, Real

from ..m0 import CarverBlocked


def require_text(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked(f"{name} is unresolved")


def require_hash(name: str, value: str) -> None:
    require_text(name, value)
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise CarverBlocked(f"{name} must be a lowercase SHA256 hex hash")


def require_iso_date(name: str, value: str) -> None:
    require_text(name, value)
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be an ISO calendar date") from exc
    if parsed.isoformat() != value:
        raise CarverBlocked(f"{name} must be normalized ISO YYYY-MM-DD")


def require_utc_timestamp(name: str, value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise CarverBlocked(f"{name} must be timezone-aware")
    if value.utcoffset() != timedelta(0):
        raise CarverBlocked(f"{name} must be UTC")


def require_hour_aligned_utc(name: str, value: datetime) -> None:
    require_utc_timestamp(name, value)
    if value.minute or value.second or value.microsecond:
        raise CarverBlocked(f"{name} must be hour-aligned")


def require_positive_number(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"{name} must be finite and positive")


def require_finite_number(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")


def require_non_negative_number(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be finite and non-negative")


def require_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise CarverBlocked(f"{name} must be an integer")


def require_non_empty_tuple(name: str, value: tuple[object, ...]) -> None:
    if not isinstance(value, tuple) or not value:
        raise CarverBlocked(f"{name} must be a non-empty tuple")


def require_tuple(name: str, value: tuple[object, ...]) -> None:
    if not isinstance(value, tuple):
        raise CarverBlocked(f"{name} must be a tuple")


def require_hash_map(name: str, value: dict[str, str], required_labels: tuple[str, ...]) -> None:
    if not isinstance(value, dict):
        raise CarverBlocked(f"{name} must be a dictionary")
    if tuple(value) != required_labels:
        raise CarverBlocked(f"{name} must match the locked label tuple")
    for label, hash_value in value.items():
        require_text(f"{name} label", label)
        require_hash(f"{name} {label}", hash_value)


def require_hash_map_matches_active_authority(
    name: str,
    observed_hash_by_label: dict[str, str],
    active_hash_by_label: dict[str, str],
    required_labels: tuple[str, ...],
) -> None:
    require_hash_map(f"{name} observed map", observed_hash_by_label, required_labels)
    require_hash_map(f"{name} active authority map", active_hash_by_label, required_labels)
    if observed_hash_by_label != active_hash_by_label:
        raise CarverBlocked(f"{name} must match active upstream authority")


def require_expected_hash(
    name: str,
    label: str,
    observed_hash: str,
    expected_hash_by_label: dict[str, str],
) -> None:
    require_text(f"{name} label", label)
    require_hash(f"{name} observed hash", observed_hash)
    if label not in expected_hash_by_label:
        raise CarverBlocked(f"{name} missing expected hash for {label}")
    if observed_hash != expected_hash_by_label[label]:
        raise CarverBlocked(f"{name} must match active source authority for {label}")


def require_matching_dependency_hashes(
    name: str,
    required_labels: tuple[str, ...],
    observed_hashes: tuple[str, ...],
    expected_hash_by_label: dict[str, str],
) -> None:
    require_non_empty_tuple(f"{name} dependency labels", required_labels)
    require_non_empty_tuple(f"{name} dependency hashes", observed_hashes)
    if len(observed_hashes) != len(required_labels):
        raise CarverBlocked(f"{name} dependency hashes must match labels")
    expected_hashes: list[str] = []
    for label in required_labels:
        require_text(f"{name} dependency label", label)
        if label not in expected_hash_by_label:
            raise CarverBlocked(f"{name} missing dependency hash for {label}")
        expected_hashes.append(expected_hash_by_label[label])
    if observed_hashes != tuple(expected_hashes):
        raise CarverBlocked(f"{name} dependency hashes must match dependency contracts")

from __future__ import annotations

import csv
from copy import deepcopy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .local_replay import canonical_sha256


@dataclass(frozen=True)
class CachedFileRef:
    path: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class CacheSnapshot:
    status: str
    cached_file_refs: tuple[CachedFileRef, ...]
    cache_key: str


class Sha256ArtifactCache:
    """Small immutable cache keyed by current file bytes, never mtime."""

    def __init__(self) -> None:
        self._sha_by_path: dict[Path, str] = {}
        self._csv_by_key: dict[tuple[Path, str], list[dict[str, str]]] = {}
        self._json_by_key: dict[tuple[Path, str], dict[str, Any]] = {}

    def file_ref(self, path: Path | str) -> CachedFileRef:
        resolved = Path(path).resolve()
        digest = self._sha256(resolved)
        return CachedFileRef(
            path=str(resolved),
            sha256=digest,
            size_bytes=resolved.stat().st_size,
        )

    def read_csv_rows(self, path: Path | str) -> list[dict[str, str]]:
        resolved = Path(path).resolve()
        digest = self._sha256(resolved)
        key = (resolved, digest)
        if key not in self._csv_by_key:
            with resolved.open("r", encoding="ascii", newline="") as handle:
                self._csv_by_key[key] = list(csv.DictReader(handle))
        return [dict(row) for row in self._csv_by_key[key]]

    def read_json(self, path: Path | str) -> dict[str, Any]:
        resolved = Path(path).resolve()
        digest = self._sha256(resolved)
        key = (resolved, digest)
        if key not in self._json_by_key:
            self._json_by_key[key] = json.loads(resolved.read_text(encoding="ascii"))
        return deepcopy(self._json_by_key[key])

    def snapshot(self) -> CacheSnapshot:
        refs = tuple(
            CachedFileRef(
                path=str(path),
                sha256=sha,
                size_bytes=path.stat().st_size,
            )
            for path, sha in sorted(self._sha_by_path.items(), key=lambda item: str(item[0]))
        )
        return CacheSnapshot(
            status="LOCAL_SHA256_ARTIFACT_CACHE_SNAPSHOT_NOT_RESULT",
            cached_file_refs=refs,
            cache_key=canonical_sha256({"cached_file_refs": refs}),
        )

    def _sha256(self, path: Path) -> str:
        if not path.exists():
            raise CarverBlocked(f"S27 v2 cache missing artifact: {path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        self._sha_by_path[path] = digest
        return digest

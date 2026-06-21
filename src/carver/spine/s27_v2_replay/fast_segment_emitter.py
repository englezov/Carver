from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .fast_execution_state import (
    FastExecutionStateVerification,
    build_fast_execution_state_verification,
)
from .fast_test_runner import ARTIFACT_FAMILY_PLAN
from .local_replay import canonical_sha256
from .fast_validation_profiles import (
    CHECKPOINT_PROOF_VALIDATION_PROFILE,
    is_checkpoint_proof_profile,
    require_supported_validation_profile,
)
from .test_incremental_runner import (
    AUTHORIZATION,
    DEFAULT_OUTPUT_RELATIVE_PATH,
    DENSE_SEGMENT_LEDGER_FILES,
    NON_AUTHORIZATIONS,
    RUN_LEDGER_FILES,
    IncrementalSegmentBundle,
    _checkpoint_public_payload,
    _pack_exhausted_terminal_row,
    _read_csv_rows_in_range,
    _segment_csv_name,
    _segment_manifest_payload,
    _single_row_by_index,
    _validate_dense_segment_continuity,
    _validate_segment_rows,
    _validate_terminal_fail_row,
    _write_csv_rows,
    _write_json,
    build_incremental_segment_from_existing_artifacts,
)


STATUS = "LOCAL_2023_TEST_FAST_SEGMENT_ARTIFACTS_MATERIALIZED_NOT_RESULT"
EMISSION_MODE = "IN_MEMORY_SEGMENT_ARTIFACT_ROWS_VALIDATED_BEFORE_WRITE_NOT_FULL_REPLAY"
SOURCE_MODE = "TRUSTED_INCREMENTAL_SEGMENT_ROWS_PARITY_FIXTURE_NOT_OPERATIONAL_TEST_CONTINUATION"

_REPO_ROOT = Path(__file__).resolve().parents[4]


@dataclass(frozen=True)
class FastSegmentArtifacts:
    status: str
    authorization_label: str
    emission_mode: str
    source_mode: str
    segment_bundle_hash: str
    execution_state_verification_hash: str
    segment_start_row_index: int
    segment_end_row_index: int
    terminal_fail_row_index: int
    ledger_row_counts: Mapping[str, int]
    segment_ledger_hashes: Mapping[str, str]
    segment_rows_by_ledger: Mapping[str, tuple[dict[str, str], ...]]
    terminal_fail_row: Mapping[str, str]
    artifact_family_plan: tuple[str, ...]
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(
        self,
        *,
        segment_bundle: IncrementalSegmentBundle,
        execution_state_verification: FastExecutionStateVerification,
        validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
    ) -> None:
        require_supported_validation_profile(validation_profile)
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 fast segment artifacts status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast segment artifacts authorization mismatch")
        if self.emission_mode != EMISSION_MODE:
            raise CarverBlocked("S27 v2 fast segment artifacts emission mode drift")
        if self.source_mode != SOURCE_MODE:
            raise CarverBlocked("S27 v2 fast segment artifacts source mode drift")
        if self.segment_bundle_hash != segment_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast segment artifacts segment binding drift")
        if self.execution_state_verification_hash != execution_state_verification.verification_hash:
            raise CarverBlocked("S27 v2 fast segment artifacts execution-state binding drift")
        if self.segment_start_row_index != segment_bundle.segment_start_row_index:
            raise CarverBlocked("S27 v2 fast segment artifacts start row drift")
        if self.segment_end_row_index != segment_bundle.segment_end_row_index:
            raise CarverBlocked("S27 v2 fast segment artifacts end row drift")
        if self.terminal_fail_row_index != segment_bundle.terminal_fail_row_index:
            raise CarverBlocked("S27 v2 fast segment artifacts terminal row drift")
        if self.artifact_family_plan != ARTIFACT_FAMILY_PLAN:
            raise CarverBlocked("S27 v2 fast segment artifacts family plan drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast segment artifacts non-authorizations drift")
        if tuple(self.segment_rows_by_ledger.keys()) != RUN_LEDGER_FILES:
            raise CarverBlocked("S27 v2 fast segment artifacts ledger family drift")
        if str(self.terminal_fail_row.get("row_hash")) != segment_bundle.terminal_fail_row_hash:
            raise CarverBlocked("S27 v2 fast segment artifacts terminal fail hash drift")
        if is_checkpoint_proof_profile(validation_profile):
            segment_bundle.validate_against_active_files()
            active_execution, _execution_rows = build_fast_execution_state_verification(
                segment_bundle=segment_bundle,
                run_root=Path(segment_bundle.run_root),
                validation_profile=validation_profile,
            )
            if active_execution.verification_hash != execution_state_verification.verification_hash:
                raise CarverBlocked("S27 v2 fast segment artifacts active execution-state drift")
        else:
            segment_bundle.validate()
        _validate_terminal_fail_row(self.terminal_fail_row)
        if is_checkpoint_proof_profile(validation_profile):
            active_terminal = (
                _pack_exhausted_terminal_row(Path(segment_bundle.run_root))
                if segment_bundle.terminal_fail_row_index == 0
                else _single_row_by_index(
                    Path(segment_bundle.run_root) / "fail_closed_ledger.csv",
                    segment_bundle.terminal_fail_row_index,
                )
            )
            if dict(self.terminal_fail_row) != active_terminal:
                raise CarverBlocked("S27 v2 fast segment artifacts terminal fail content drift")
        _validate_artifact_rows(self, segment_bundle)
        execution_state_verification.validate(segment_bundle)
        if self.bundle_hash != canonical_sha256(_artifact_bundle_payload(self)):
            raise CarverBlocked("S27 v2 fast segment artifacts bundle hash drift")


def build_fast_segment_artifacts(
    *,
    segment_bundle: IncrementalSegmentBundle | None = None,
    run_root: Path | str | None = None,
    validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
) -> tuple[FastSegmentArtifacts, IncrementalSegmentBundle, FastExecutionStateVerification]:
    require_supported_validation_profile(validation_profile)
    run_root_path = _resolve_run_root(run_root)
    active_segment = segment_bundle or build_incremental_segment_from_existing_artifacts(run_root=run_root_path)
    if is_checkpoint_proof_profile(validation_profile):
        active_segment.validate_against_active_files()
    else:
        active_segment.validate()
    execution_state, _execution_rows = build_fast_execution_state_verification(
        segment_bundle=active_segment,
        run_root=run_root_path,
        validation_profile=validation_profile,
    )

    rows_by_ledger: dict[str, tuple[dict[str, str], ...]] = {}
    for ledger_name in RUN_LEDGER_FILES:
        rows = tuple(
            _read_csv_rows_in_range(
                run_root_path / ledger_name,
                active_segment.segment_start_row_index,
                active_segment.segment_end_row_index,
            )
        )
        _validate_segment_rows(ledger_name, list(rows))
        if ledger_name in DENSE_SEGMENT_LEDGER_FILES:
            _validate_dense_segment_continuity(
                ledger_name,
                list(rows),
                active_segment.segment_start_row_index,
                active_segment.segment_end_row_index,
            )
        rows_by_ledger[ledger_name] = rows

    terminal_fail = (
        _pack_exhausted_terminal_row(run_root_path)
        if active_segment.terminal_fail_row_index == 0
        else _single_row_by_index(run_root_path / "fail_closed_ledger.csv", active_segment.terminal_fail_row_index)
    )
    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "emission_mode": EMISSION_MODE,
        "source_mode": SOURCE_MODE,
        "segment_bundle_hash": active_segment.bundle_hash,
        "execution_state_verification_hash": execution_state.verification_hash,
        "segment_start_row_index": active_segment.segment_start_row_index,
        "segment_end_row_index": active_segment.segment_end_row_index,
        "terminal_fail_row_index": active_segment.terminal_fail_row_index,
        "ledger_row_counts": dict(active_segment.ledger_row_counts),
        "segment_ledger_hashes": dict(active_segment.segment_ledger_hashes),
        "segment_rows_by_ledger": rows_by_ledger,
        "terminal_fail_row": terminal_fail,
        "artifact_family_plan": ARTIFACT_FAMILY_PLAN,
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    artifacts = FastSegmentArtifacts(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        emission_mode=EMISSION_MODE,
        source_mode=SOURCE_MODE,
        segment_bundle_hash=active_segment.bundle_hash,
        execution_state_verification_hash=execution_state.verification_hash,
        segment_start_row_index=active_segment.segment_start_row_index,
        segment_end_row_index=active_segment.segment_end_row_index,
        terminal_fail_row_index=active_segment.terminal_fail_row_index,
        ledger_row_counts=dict(active_segment.ledger_row_counts),
        segment_ledger_hashes=dict(active_segment.segment_ledger_hashes),
        segment_rows_by_ledger=rows_by_ledger,
        terminal_fail_row=terminal_fail,
        artifact_family_plan=ARTIFACT_FAMILY_PLAN,
        bundle_hash=canonical_sha256(payload),
    )
    artifacts.validate(
        segment_bundle=active_segment,
        execution_state_verification=execution_state,
        validation_profile=validation_profile,
    )
    return artifacts, active_segment, execution_state


def write_fast_segment_artifacts(
    artifacts: FastSegmentArtifacts,
    *,
    segment_bundle: IncrementalSegmentBundle,
    execution_state_verification: FastExecutionStateVerification,
    output_root: Path | str,
) -> None:
    artifacts.validate(
        segment_bundle=segment_bundle,
        execution_state_verification=execution_state_verification,
    )
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    _write_json(root / "checkpoint_manifest.json", _checkpoint_public_payload(segment_bundle.baseline_checkpoint))
    _write_json(root / "segment_manifest.json", _segment_manifest_payload(segment_bundle))
    _write_json(root / "segment_ledger_hashes.json", dict(segment_bundle.segment_ledger_hashes))
    _write_json(root / "fast_segment_artifacts_manifest.json", _artifact_public_payload(artifacts))
    for ledger_name in RUN_LEDGER_FILES:
        _write_csv_rows(root / _segment_csv_name(ledger_name), list(artifacts.segment_rows_by_ledger[ledger_name]))
    _write_csv_rows(root / "fail_closed_ledger_terminal.csv", [dict(artifacts.terminal_fail_row)])


def _validate_artifact_rows(artifacts: FastSegmentArtifacts, segment_bundle: IncrementalSegmentBundle) -> None:
    for ledger_name, rows in artifacts.segment_rows_by_ledger.items():
        expected_count = segment_bundle.ledger_row_counts[ledger_name]
        if len(rows) != expected_count:
            raise CarverBlocked(f"S27 v2 fast segment artifacts row count drift for {ledger_name}")
        actual_hash = canonical_sha256(
            {
                "ledger_name": ledger_name,
                "segment_start_row_index": artifacts.segment_start_row_index,
                "segment_end_row_index": artifacts.segment_end_row_index,
                "rows": list(rows),
            }
        )
        if actual_hash != segment_bundle.segment_ledger_hashes[ledger_name]:
            raise CarverBlocked(f"S27 v2 fast segment artifacts row hash drift for {ledger_name}")
        _validate_segment_rows(ledger_name, list(rows))
        if ledger_name in DENSE_SEGMENT_LEDGER_FILES:
            _validate_dense_segment_continuity(
                ledger_name,
                list(rows),
                artifacts.segment_start_row_index,
                artifacts.segment_end_row_index,
            )


def _resolve_run_root(path: Path | str | None) -> Path:
    if path is None:
        return (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve()
    resolved = Path(path).resolve()
    if resolved != (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 fast segment artifacts run root is locked")
    return resolved


def _artifact_public_payload(artifacts: FastSegmentArtifacts) -> dict[str, Any]:
    data = asdict(artifacts)
    data.pop("segment_rows_by_ledger", None)
    data.pop("terminal_fail_row", None)
    return data


def _artifact_bundle_payload(artifacts: FastSegmentArtifacts) -> dict[str, Any]:
    data = asdict(artifacts)
    data.pop("bundle_hash", None)
    return data

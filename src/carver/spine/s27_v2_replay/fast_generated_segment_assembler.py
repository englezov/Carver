from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .fast_downstream_generator import (
    FastDownstreamGenerationBundle,
    FastDownstreamPolicyRegistry,
    FastGeneratedDownstreamRows,
)
from .fast_order_generator import (
    FastGeneratedOrderRows,
    FastOrderGenerationBundle,
    FastOrderPolicyRegistry,
)
from .fast_row_engine import FastPrimitiveEngineBundle, FastPrimitiveRows
from .fast_segment_emitter import FastSegmentArtifacts
from .fast_test_runner import ARTIFACT_FAMILY_PLAN
from .local_replay import canonical_sha256
from .fast_validation_profiles import (
    CHECKPOINT_PROOF_VALIDATION_PROFILE,
    is_checkpoint_proof_profile,
    require_supported_validation_profile,
)
from .test_incremental_runner import (
    AUTHORIZATION,
    DENSE_SEGMENT_LEDGER_FILES,
    NON_AUTHORIZATIONS,
    RUN_LEDGER_FILES,
    IncrementalSegmentBundle,
    _checkpoint_public_payload,
    _segment_csv_name,
    _validate_dense_segment_continuity,
    _validate_segment_rows,
    _validate_terminal_fail_row,
    _write_csv_rows,
    _write_json,
)


STATUS = "LOCAL_2023_TEST_FAST_GENERATED_SEGMENT_ASSEMBLED_NOT_RESULT"
ASSEMBLY_MODE = "GENERATED_PRIMITIVE_ORDER_DOWNSTREAM_ROWS_NOT_LEGACY_SLICE_COPY"


@dataclass(frozen=True)
class FastGeneratedSegmentAssembly:
    status: str
    authorization_label: str
    assembly_mode: str
    primitive_engine_bundle_hash: str
    order_generation_bundle_hash: str
    downstream_generation_bundle_hash: str
    segment_bundle_hash: str
    active_segment_artifacts_hash: str
    segment_start_row_index: int
    segment_end_row_index: int
    terminal_fail_row_index: int
    generated_ledger_hashes: Mapping[str, str]
    active_row_hash_parity_hash: str
    generated_rows_by_ledger: Mapping[str, tuple[dict[str, Any], ...]]
    terminal_fail_row: Mapping[str, Any]
    artifact_family_plan: tuple[str, ...]
    assembly_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(
        self,
        *,
        primitive_bundle: FastPrimitiveEngineBundle,
        primitive_rows: FastPrimitiveRows,
        segment_bundle: IncrementalSegmentBundle,
        active_artifacts: FastSegmentArtifacts,
        order_policy_registry: FastOrderPolicyRegistry,
        order_bundle: FastOrderGenerationBundle,
        order_rows: FastGeneratedOrderRows,
        downstream_policy_registry: FastDownstreamPolicyRegistry,
        downstream_bundle: FastDownstreamGenerationBundle,
        downstream_rows: FastGeneratedDownstreamRows,
        validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
    ) -> None:
        require_supported_validation_profile(validation_profile)
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 fast generated segment assembly status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast generated segment assembly authorization mismatch")
        if self.assembly_mode != ASSEMBLY_MODE:
            raise CarverBlocked("S27 v2 fast generated segment assembly mode drift")
        if self.primitive_engine_bundle_hash != primitive_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast generated segment primitive binding drift")
        if self.order_generation_bundle_hash != order_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast generated segment order binding drift")
        if self.downstream_generation_bundle_hash != downstream_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast generated segment downstream binding drift")
        if self.segment_bundle_hash != segment_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast generated segment segment binding drift")
        if self.active_segment_artifacts_hash != active_artifacts.bundle_hash:
            raise CarverBlocked("S27 v2 fast generated segment active artifact binding drift")
        if self.segment_start_row_index != segment_bundle.segment_start_row_index:
            raise CarverBlocked("S27 v2 fast generated segment start row drift")
        if self.segment_end_row_index != segment_bundle.segment_end_row_index:
            raise CarverBlocked("S27 v2 fast generated segment end row drift")
        if self.terminal_fail_row_index != segment_bundle.terminal_fail_row_index:
            raise CarverBlocked("S27 v2 fast generated segment terminal row drift")
        if self.artifact_family_plan != ARTIFACT_FAMILY_PLAN:
            raise CarverBlocked("S27 v2 fast generated segment artifact plan drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast generated segment non-authorizations drift")
        if tuple(self.generated_rows_by_ledger.keys()) != RUN_LEDGER_FILES:
            raise CarverBlocked("S27 v2 fast generated segment ledger family drift")

        if is_checkpoint_proof_profile(validation_profile):
            primitive_bundle.validate()
            _validate_primitive_rows_against_bundle(primitive_bundle, primitive_rows)
            order_bundle.validate(
                primitive_bundle=primitive_bundle,
                segment_bundle=segment_bundle,
                artifacts=active_artifacts,
                policy_registry=order_policy_registry,
                rows=order_rows,
                validation_profile=validation_profile,
            )
            downstream_bundle.validate(
                primitive_bundle=primitive_bundle,
                segment_bundle=segment_bundle,
                artifacts=active_artifacts,
                order_policy_registry=order_policy_registry,
                order_bundle=order_bundle,
                order_rows=order_rows,
                downstream_policy_registry=downstream_policy_registry,
                rows=downstream_rows,
                validation_profile=validation_profile,
            )
        _validate_terminal_fail_row(self.terminal_fail_row)
        if dict(self.terminal_fail_row) != dict(active_artifacts.terminal_fail_row):
            raise CarverBlocked("S27 v2 fast generated segment terminal fail content drift")

        expected_rows = _build_generated_rows_by_ledger(
            primitive_rows=primitive_rows,
            segment_bundle=segment_bundle,
            order_rows=order_rows,
            downstream_rows=downstream_rows,
        )
        if self.generated_rows_by_ledger != expected_rows:
            raise CarverBlocked("S27 v2 fast generated segment row content drift")
        expected_hashes = _generated_ledger_hashes(expected_rows, segment_bundle)
        if dict(self.generated_ledger_hashes) != expected_hashes:
            raise CarverBlocked("S27 v2 fast generated segment ledger hash drift")
        parity_hash = _validate_active_row_hash_parity(expected_rows, active_artifacts)
        if self.active_row_hash_parity_hash != parity_hash:
            raise CarverBlocked("S27 v2 fast generated segment active parity hash drift")
        _validate_generated_rows(expected_rows, segment_bundle)
        if self.assembly_hash != canonical_sha256(_assembly_payload(self)):
            raise CarverBlocked("S27 v2 fast generated segment assembly hash drift")


def build_fast_generated_segment_assembly(
    *,
    primitive_bundle: FastPrimitiveEngineBundle,
    primitive_rows: FastPrimitiveRows,
    segment_bundle: IncrementalSegmentBundle,
    active_artifacts: FastSegmentArtifacts,
    order_policy_registry: FastOrderPolicyRegistry,
    order_bundle: FastOrderGenerationBundle,
    order_rows: FastGeneratedOrderRows,
    downstream_policy_registry: FastDownstreamPolicyRegistry,
    downstream_bundle: FastDownstreamGenerationBundle,
    downstream_rows: FastGeneratedDownstreamRows,
    validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
) -> FastGeneratedSegmentAssembly:
    require_supported_validation_profile(validation_profile)
    generated_rows = _build_generated_rows_by_ledger(
        primitive_rows=primitive_rows,
        segment_bundle=segment_bundle,
        order_rows=order_rows,
        downstream_rows=downstream_rows,
    )
    generated_hashes = _generated_ledger_hashes(generated_rows, segment_bundle)
    parity_hash = _validate_active_row_hash_parity(generated_rows, active_artifacts)
    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "assembly_mode": ASSEMBLY_MODE,
        "primitive_engine_bundle_hash": primitive_bundle.bundle_hash,
        "order_generation_bundle_hash": order_bundle.bundle_hash,
        "downstream_generation_bundle_hash": downstream_bundle.bundle_hash,
        "segment_bundle_hash": segment_bundle.bundle_hash,
        "active_segment_artifacts_hash": active_artifacts.bundle_hash,
        "segment_start_row_index": segment_bundle.segment_start_row_index,
        "segment_end_row_index": segment_bundle.segment_end_row_index,
        "terminal_fail_row_index": segment_bundle.terminal_fail_row_index,
        "generated_ledger_hashes": generated_hashes,
        "active_row_hash_parity_hash": parity_hash,
        "generated_rows_by_ledger": generated_rows,
        "terminal_fail_row": dict(active_artifacts.terminal_fail_row),
        "artifact_family_plan": ARTIFACT_FAMILY_PLAN,
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    assembly = FastGeneratedSegmentAssembly(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        assembly_mode=ASSEMBLY_MODE,
        primitive_engine_bundle_hash=primitive_bundle.bundle_hash,
        order_generation_bundle_hash=order_bundle.bundle_hash,
        downstream_generation_bundle_hash=downstream_bundle.bundle_hash,
        segment_bundle_hash=segment_bundle.bundle_hash,
        active_segment_artifacts_hash=active_artifacts.bundle_hash,
        segment_start_row_index=segment_bundle.segment_start_row_index,
        segment_end_row_index=segment_bundle.segment_end_row_index,
        terminal_fail_row_index=segment_bundle.terminal_fail_row_index,
        generated_ledger_hashes=generated_hashes,
        active_row_hash_parity_hash=parity_hash,
        generated_rows_by_ledger=generated_rows,
        terminal_fail_row=dict(active_artifacts.terminal_fail_row),
        artifact_family_plan=ARTIFACT_FAMILY_PLAN,
        assembly_hash=canonical_sha256(payload),
    )
    assembly.validate(
        primitive_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        segment_bundle=segment_bundle,
        active_artifacts=active_artifacts,
        order_policy_registry=order_policy_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_policy_registry,
        downstream_bundle=downstream_bundle,
        downstream_rows=downstream_rows,
        validation_profile=validation_profile,
    )
    return assembly


def write_fast_generated_segment_artifacts(
    assembly: FastGeneratedSegmentAssembly,
    *,
    primitive_bundle: FastPrimitiveEngineBundle,
    primitive_rows: FastPrimitiveRows,
    segment_bundle: IncrementalSegmentBundle,
    active_artifacts: FastSegmentArtifacts,
    order_policy_registry: FastOrderPolicyRegistry,
    order_bundle: FastOrderGenerationBundle,
    order_rows: FastGeneratedOrderRows,
    downstream_policy_registry: FastDownstreamPolicyRegistry,
    downstream_bundle: FastDownstreamGenerationBundle,
    downstream_rows: FastGeneratedDownstreamRows,
    output_root: Path | str,
) -> None:
    assembly.validate(
        primitive_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        segment_bundle=segment_bundle,
        active_artifacts=active_artifacts,
        order_policy_registry=order_policy_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_policy_registry,
        downstream_bundle=downstream_bundle,
        downstream_rows=downstream_rows,
    )
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    _write_json(root / "checkpoint_manifest.json", _checkpoint_public_payload(segment_bundle.baseline_checkpoint))
    _write_json(root / "generated_segment_manifest.json", _assembly_public_payload(assembly))
    _write_json(root / "generated_segment_ledger_hashes.json", dict(assembly.generated_ledger_hashes))
    for ledger_name in RUN_LEDGER_FILES:
        _write_csv_rows(root / _segment_csv_name(ledger_name), list(assembly.generated_rows_by_ledger[ledger_name]))
    _write_csv_rows(root / "fail_closed_ledger_terminal.csv", [dict(assembly.terminal_fail_row)])


def _build_generated_rows_by_ledger(
    *,
    primitive_rows: FastPrimitiveRows,
    segment_bundle: IncrementalSegmentBundle,
    order_rows: FastGeneratedOrderRows,
    downstream_rows: FastGeneratedDownstreamRows,
) -> dict[str, tuple[dict[str, Any], ...]]:
    return {
        "runtime_history_ledger.csv": _rows_in_range(primitive_rows.runtime_rows, segment_bundle),
        "forecast_replay_ledger.csv": _rows_in_range(primitive_rows.forecast_rows, segment_bundle),
        "desired_position_ledger.csv": tuple(dict(row) for row in order_rows.desired_position_rows),
        "limit_order_ledger.csv": tuple(dict(row) for row in order_rows.limit_order_rows),
        "no_market_order_ledger.csv": tuple(dict(row) for row in order_rows.no_market_order_rows),
        "market_order_ledger.csv": tuple(dict(row) for row in order_rows.market_order_rows),
        "working_order_transition_ledger.csv": tuple(dict(row) for row in downstream_rows.transition_rows),
        "fill_ledger.csv": tuple(dict(row) for row in downstream_rows.fill_rows),
        "market_fill_metadata_ledger.csv": tuple(dict(row) for row in downstream_rows.market_fill_metadata_rows),
        "cost_ledger.csv": tuple(dict(row) for row in downstream_rows.cost_rows),
        "pnl_ledger.csv": tuple(dict(row) for row in downstream_rows.pnl_rows),
        "validation_ledger.csv": tuple(dict(row) for row in downstream_rows.validation_rows),
    }


def _rows_in_range(
    rows: tuple[dict[str, Any], ...],
    segment_bundle: IncrementalSegmentBundle,
) -> tuple[dict[str, Any], ...]:
    return tuple(
        dict(row)
        for row in rows
        if segment_bundle.segment_start_row_index <= int(row["row_index"]) <= segment_bundle.segment_end_row_index
    )


def _generated_ledger_hashes(
    rows_by_ledger: Mapping[str, tuple[dict[str, Any], ...]],
    segment_bundle: IncrementalSegmentBundle,
) -> dict[str, str]:
    return {
        ledger_name: canonical_sha256(
            {
                "ledger_name": ledger_name,
                "segment_start_row_index": segment_bundle.segment_start_row_index,
                "segment_end_row_index": segment_bundle.segment_end_row_index,
                "rows": list(rows),
            }
        )
        for ledger_name, rows in rows_by_ledger.items()
    }


def _validate_active_row_hash_parity(
    generated_rows_by_ledger: Mapping[str, tuple[dict[str, Any], ...]],
    active_artifacts: FastSegmentArtifacts,
) -> str:
    parity_rows: list[dict[str, Any]] = []
    for ledger_name in RUN_LEDGER_FILES:
        generated = _rows_by_index(generated_rows_by_ledger[ledger_name])
        active = _rows_by_index(active_artifacts.segment_rows_by_ledger[ledger_name])
        if set(generated) != set(active):
            raise CarverBlocked(f"S27 v2 fast generated segment row set drift for {ledger_name}")
        for row_index, generated_row in generated.items():
            if str(generated_row["row_hash"]) != str(active[row_index]["row_hash"]):
                raise CarverBlocked(f"S27 v2 fast generated segment row-hash parity drift for {ledger_name} row {row_index}")
        parity_rows.append(
            {
                "ledger_name": ledger_name,
                "row_count": len(generated),
                "generated_row_hashes_hash": canonical_sha256(
                    tuple({"row_index": index, "row_hash": generated[index]["row_hash"]} for index in sorted(generated))
                ),
            }
        )
    return canonical_sha256(parity_rows)


def _validate_generated_rows(
    rows_by_ledger: Mapping[str, tuple[dict[str, Any], ...]],
    segment_bundle: IncrementalSegmentBundle,
) -> None:
    if tuple(rows_by_ledger.keys()) != RUN_LEDGER_FILES:
        raise CarverBlocked("S27 v2 fast generated segment ledger family drift")
    for ledger_name, rows in rows_by_ledger.items():
        _validate_segment_rows(ledger_name, list(rows))
        if ledger_name in DENSE_SEGMENT_LEDGER_FILES:
            _validate_dense_segment_continuity(
                ledger_name,
                list(rows),
                segment_bundle.segment_start_row_index,
                segment_bundle.segment_end_row_index,
            )


def _validate_primitive_rows_against_bundle(
    primitive_bundle: FastPrimitiveEngineBundle,
    primitive_rows: FastPrimitiveRows,
) -> None:
    if canonical_sha256(primitive_rows.runtime_rows) != primitive_bundle.runtime_rows_hash:
        raise CarverBlocked("S27 v2 fast generated segment primitive runtime rows hash drift")
    if canonical_sha256(primitive_rows.forecast_rows) != primitive_bundle.forecast_rows_hash:
        raise CarverBlocked("S27 v2 fast generated segment primitive forecast rows hash drift")
    if canonical_sha256(primitive_rows.desired_absolute_rows) != primitive_bundle.desired_absolute_rows_hash:
        raise CarverBlocked("S27 v2 fast generated segment primitive desired rows hash drift")
    for ledger_name, rows in (
        ("runtime_history_ledger.csv", primitive_rows.runtime_rows),
        ("forecast_replay_ledger.csv", primitive_rows.forecast_rows),
        ("desired_absolute_rows", primitive_rows.desired_absolute_rows),
    ):
        for row in rows:
            payload = dict(row)
            observed_hash = payload.pop("row_hash", None)
            if observed_hash != canonical_sha256(payload):
                raise CarverBlocked(
                    f"S27 v2 fast generated segment primitive row hash content drift for {ledger_name} row {row.get('row_index')}"
                )


def _rows_by_index(rows: tuple[Mapping[str, Any], ...]) -> dict[int, Mapping[str, Any]]:
    indexes = [int(row["row_index"]) for row in rows]
    if len(indexes) != len(set(indexes)):
        raise CarverBlocked("S27 v2 fast generated segment duplicate row index drift")
    return {int(row["row_index"]): row for row in rows}


def _assembly_public_payload(assembly: FastGeneratedSegmentAssembly) -> dict[str, Any]:
    data = asdict(assembly)
    data.pop("generated_rows_by_ledger", None)
    data.pop("terminal_fail_row", None)
    return data


def _assembly_payload(assembly: FastGeneratedSegmentAssembly) -> dict[str, Any]:
    data = asdict(assembly)
    data.pop("assembly_hash", None)
    return data

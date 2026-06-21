from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .local_replay import canonical_sha256
from .fast_row_engine import (
    FastPrimitiveEngineBundle,
    FastPrimitiveParityReport,
    FastPrimitiveRows,
    build_fast_primitive_engine,
    validate_fast_primitive_parity,
)
from .fast_execution_state import (
    FastExecutionStateVerification,
    build_fast_execution_state_verification,
)
from .replay_artifact_cache import CacheSnapshot, Sha256ArtifactCache
from .fast_validation_profiles import (
    CHECKPOINT_PROOF_VALIDATION_PROFILE,
    OPERATIONAL_VALIDATION_PROFILE,
    is_checkpoint_proof_profile,
    require_supported_validation_profile,
)
from .test_incremental_runner import (
    AUTHORIZATION,
    DEFAULT_BASELINE_ROW_INDEX,
    DEFAULT_COMBINED_TBBO_RELATIVE_PATH,
    DEFAULT_OUTPUT_RELATIVE_PATH,
    DEFAULT_PACK_RELATIVE_PATH,
    DEFAULT_SEGMENT_END_ROW_INDEX,
    DEFAULT_SEGMENT_START_ROW_INDEX,
    DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH,
    DEFAULT_TERMINAL_FAIL_ROW_INDEX,
    EVIDENCE_MANIFEST_NAME,
    COMBINED_TBBO_REGISTRY_NAME,
    NON_AUTHORIZATIONS,
    RUN_MANIFEST_NAME,
    IncrementalSegmentBundle,
    MissingTBBOBatchPlan,
    build_incremental_segment_from_existing_artifacts,
    build_missing_tbbo_batch_plan,
)


_REPO_ROOT = Path(__file__).resolve().parents[4]
FAST_MODE = "fast_mode"
SEGMENT_MODE = "segment_mode"
PROOF_MODE = "proof_mode"
SUPPORTED_MODES = (FAST_MODE, SEGMENT_MODE, PROOF_MODE)

STATUS = "LOCAL_2023_TEST_FAST_RUNNER_SEGMENT_READY_NOT_RESULT"
PROOF_MODE_BLOCKED_STATUS = "FAIL_CLOSED_PROOF_MODE_REQUIRES_SEPARATE_EXPLICIT_CHECKPOINT_GATE_NOT_RESULT"
ENGINE_STAGE = "FAST_RUNNER_FACADE_INCREMENTAL_SEGMENT_PRIMITIVES_AND_EXECUTION_STATE_NOT_FULL_PROOF"

ARTIFACT_FAMILY_PLAN = (
    "checkpoint_manifest.json",
    "segment_manifest.json",
    "segment_ledger_hashes.json",
    "runtime_history_ledger_segment.csv",
    "forecast_replay_ledger_segment.csv",
    "desired_position_ledger_segment.csv",
    "limit_order_ledger_segment.csv",
    "no_market_order_ledger_segment.csv",
    "market_order_ledger_segment.csv",
    "working_order_transition_ledger_segment.csv",
    "fill_ledger_segment.csv",
    "market_fill_metadata_ledger_segment.csv",
    "cost_ledger_segment.csv",
    "pnl_ledger_segment.csv",
    "validation_ledger_segment.csv",
    "fail_closed_ledger_terminal.csv",
)

EXPECTED_CACHE_RELATIVE_FILES = (
    f"{DEFAULT_PACK_RELATIVE_PATH}/S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST.json",
    f"{DEFAULT_PACK_RELATIVE_PATH}/S27_V2_2023_TEST_DECLARED_INPUT_PACK_SHA256SUMS.txt",
    f"{DEFAULT_PACK_RELATIVE_PATH}/cost_parameter.csv",
    f"{DEFAULT_PACK_RELATIVE_PATH}/hourly_decision_completed_bar.csv",
    f"{DEFAULT_PACK_RELATIVE_PATH}/hourly_fill_completed_bar.csv",
    f"{DEFAULT_PACK_RELATIVE_PATH}/runtime_evidence_ledger.csv",
    f"{DEFAULT_PACK_RELATIVE_PATH}/valuation_mark_completed_bar.csv",
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_combined_market_order_tbbo_registry/combined_market_order_tbbo_registry.csv",
    f"{DEFAULT_OUTPUT_RELATIVE_PATH}/desired_position_ledger.csv",
    f"{DEFAULT_OUTPUT_RELATIVE_PATH}/evidence_manifest.json",
    f"{DEFAULT_OUTPUT_RELATIVE_PATH}/fail_closed_ledger.csv",
    f"{DEFAULT_OUTPUT_RELATIVE_PATH}/forecast_replay_ledger.csv",
    f"{DEFAULT_OUTPUT_RELATIVE_PATH}/pnl_ledger.csv",
    f"{DEFAULT_OUTPUT_RELATIVE_PATH}/run_manifest.json",
    f"{DEFAULT_OUTPUT_RELATIVE_PATH}/runtime_history_ledger.csv",
    f"{DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH}/market_order_tbbo_requirements.csv",
)


@dataclass(frozen=True)
class FastRunnerRequest:
    mode: str = SEGMENT_MODE
    baseline_row_index: int = DEFAULT_BASELINE_ROW_INDEX
    segment_start_row_index: int = DEFAULT_SEGMENT_START_ROW_INDEX
    segment_end_row_index: int = DEFAULT_SEGMENT_END_ROW_INDEX
    terminal_fail_row_index: int = DEFAULT_TERMINAL_FAIL_ROW_INDEX
    pack_root: str = str((Path(__file__).resolve().parents[4] / DEFAULT_PACK_RELATIVE_PATH).resolve())
    run_root: str = str((Path(__file__).resolve().parents[4] / DEFAULT_OUTPUT_RELATIVE_PATH).resolve())
    requirements_root: str = str((Path(__file__).resolve().parents[4] / DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH).resolve())
    validation_profile: str = OPERATIONAL_VALIDATION_PROFILE


@dataclass(frozen=True)
class FastRunnerResult:
    status: str
    authorization_label: str
    mode: str
    validation_profile: str
    engine_stage: str
    segment_bundle: IncrementalSegmentBundle
    primitive_engine_bundle: FastPrimitiveEngineBundle
    primitive_rows: FastPrimitiveRows
    primitive_parity_report: FastPrimitiveParityReport
    execution_state_verification: FastExecutionStateVerification
    segment_artifacts: Any
    order_policy_registry: Any
    order_generation_bundle: Any
    order_rows: Any
    downstream_policy_registry: Any
    downstream_generation_bundle: Any
    downstream_rows: Any
    generated_segment_assembly: Any
    tbbo_batch_plan: MissingTBBOBatchPlan
    cache_snapshot: CacheSnapshot
    artifact_family_plan: tuple[str, ...]
    result_interpretation: str
    source_faithful_evidence_claim: str
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self) -> None:
        require_supported_validation_profile(self.validation_profile)
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 fast runner status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast runner authorization mismatch")
        if self.mode not in {FAST_MODE, SEGMENT_MODE}:
            raise CarverBlocked("S27 v2 fast runner mode is not an operational segment mode")
        if self.engine_stage != ENGINE_STAGE:
            raise CarverBlocked("S27 v2 fast runner engine stage drift")
        if self.artifact_family_plan != ARTIFACT_FAMILY_PLAN:
            raise CarverBlocked("S27 v2 fast runner artifact family plan drift")
        if self.cache_snapshot.status != "LOCAL_SHA256_ARTIFACT_CACHE_SNAPSHOT_NOT_RESULT":
            raise CarverBlocked("S27 v2 fast runner cache snapshot status drift")
        if self.cache_snapshot.cache_key != canonical_sha256({"cached_file_refs": self.cache_snapshot.cached_file_refs}):
            raise CarverBlocked("S27 v2 fast runner cache snapshot hash drift")
        if not self.cache_snapshot.cached_file_refs:
            raise CarverBlocked("S27 v2 fast runner cache snapshot is empty")
        _validate_cache_snapshot_refs(self.cache_snapshot)
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast runner non-authorizations drift")
        if self.result_interpretation != "NO":
            raise CarverBlocked("S27 v2 fast runner result interpretation drift")
        if self.source_faithful_evidence_claim != "NO":
            raise CarverBlocked("S27 v2 fast runner source-faithful claim drift")
        self.primitive_engine_bundle.validate()
        if is_checkpoint_proof_profile(self.validation_profile):
            self.primitive_parity_report.validate(self.primitive_engine_bundle)
            self.segment_bundle.validate_against_active_files()
        else:
            self.segment_bundle.validate()
        self.execution_state_verification.validate(self.segment_bundle)
        self.segment_artifacts.validate(
            segment_bundle=self.segment_bundle,
            execution_state_verification=self.execution_state_verification,
            validation_profile=self.validation_profile,
        )
        self.order_generation_bundle.validate(
            primitive_bundle=self.primitive_engine_bundle,
            segment_bundle=self.segment_bundle,
            artifacts=self.segment_artifacts,
            policy_registry=self.order_policy_registry,
            rows=self.order_rows,
            validation_profile=self.validation_profile,
        )
        self.downstream_generation_bundle.validate(
            primitive_bundle=self.primitive_engine_bundle,
            segment_bundle=self.segment_bundle,
            artifacts=self.segment_artifacts,
            order_policy_registry=self.order_policy_registry,
            order_bundle=self.order_generation_bundle,
            order_rows=self.order_rows,
            downstream_policy_registry=self.downstream_policy_registry,
            rows=self.downstream_rows,
            validation_profile=self.validation_profile,
        )
        self.generated_segment_assembly.validate(
            primitive_bundle=self.primitive_engine_bundle,
            primitive_rows=self.primitive_rows,
            segment_bundle=self.segment_bundle,
            active_artifacts=self.segment_artifacts,
            order_policy_registry=self.order_policy_registry,
            order_bundle=self.order_generation_bundle,
            order_rows=self.order_rows,
            downstream_policy_registry=self.downstream_policy_registry,
            downstream_bundle=self.downstream_generation_bundle,
            downstream_rows=self.downstream_rows,
            validation_profile=self.validation_profile,
        )
        self.tbbo_batch_plan.validate()
        if self.bundle_hash != canonical_sha256(_result_payload(self)):
            raise CarverBlocked("S27 v2 fast runner bundle hash drift")


def run_2023_test_fast_runner(request: FastRunnerRequest | None = None) -> FastRunnerResult:
    from .fast_downstream_generator import build_fast_downstream_generation, build_fast_downstream_policy_registry
    from .fast_generated_segment_assembler import build_fast_generated_segment_assembly
    from .fast_order_generator import build_fast_order_generation, build_fast_order_policy_registry
    from .fast_segment_emitter import build_fast_segment_artifacts

    req = request or FastRunnerRequest()
    if req.mode not in SUPPORTED_MODES:
        raise CarverBlocked("S27 v2 fast runner mode is not recognized")
    if req.mode == PROOF_MODE:
        raise CarverBlocked(PROOF_MODE_BLOCKED_STATUS)
    require_supported_validation_profile(req.validation_profile)

    cache = Sha256ArtifactCache()
    pack_root = Path(req.pack_root).resolve()
    run_root = Path(req.run_root).resolve()
    requirements_root = Path(req.requirements_root).resolve()
    _require_locked_roots(pack_root, run_root, requirements_root)
    _prime_cache(cache, pack_root, run_root, requirements_root)

    primitive_bundle, primitive_rows = build_fast_primitive_engine(
        pack_root=pack_root,
        cache=cache,
    )
    primitive_parity = validate_fast_primitive_parity(
        primitive_bundle,
        primitive_rows,
        run_root=run_root,
    )
    segment = build_incremental_segment_from_existing_artifacts(
        baseline_row_index=req.baseline_row_index,
        segment_start_row_index=req.segment_start_row_index,
        segment_end_row_index=req.segment_end_row_index,
        terminal_fail_row_index=req.terminal_fail_row_index,
        pack_root=pack_root,
        run_root=run_root,
    )
    execution_state, _execution_rows = build_fast_execution_state_verification(
        segment_bundle=segment,
        run_root=run_root,
        validation_profile=req.validation_profile,
    )
    segment_artifacts, _active_segment, active_execution = build_fast_segment_artifacts(
        segment_bundle=segment,
        run_root=run_root,
        validation_profile=req.validation_profile,
    )
    if active_execution.verification_hash != execution_state.verification_hash:
        raise CarverBlocked("S27 v2 fast runner segment artifact execution verification drift")
    order_policy_registry = build_fast_order_policy_registry(artifacts=segment_artifacts)
    order_generation_bundle, order_rows = build_fast_order_generation(
        primitive_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        segment_bundle=segment,
        artifacts=segment_artifacts,
        policy_registry=order_policy_registry,
        pack_root=pack_root,
        validation_profile=req.validation_profile,
    )
    downstream_policy_registry = build_fast_downstream_policy_registry(
        primitive_bundle=primitive_bundle,
        segment_bundle=segment,
        artifacts=segment_artifacts,
        order_policy_registry=order_policy_registry,
        order_bundle=order_generation_bundle,
        order_rows=order_rows,
        validation_profile=req.validation_profile,
    )
    downstream_generation_bundle, downstream_rows = build_fast_downstream_generation(
        primitive_bundle=primitive_bundle,
        segment_bundle=segment,
        artifacts=segment_artifacts,
        order_policy_registry=order_policy_registry,
        order_bundle=order_generation_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_policy_registry,
        validation_profile=req.validation_profile,
    )
    generated_segment_assembly = build_fast_generated_segment_assembly(
        primitive_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        segment_bundle=segment,
        active_artifacts=segment_artifacts,
        order_policy_registry=order_policy_registry,
        order_bundle=order_generation_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_policy_registry,
        downstream_bundle=downstream_generation_bundle,
        downstream_rows=downstream_rows,
        validation_profile=req.validation_profile,
    )
    tbbo_plan = build_missing_tbbo_batch_plan(requirements_root=requirements_root)

    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "mode": req.mode,
        "validation_profile": req.validation_profile,
        "engine_stage": ENGINE_STAGE,
        "primitive_engine_bundle_hash": primitive_bundle.bundle_hash,
        "primitive_rows_hash": canonical_sha256(
            {
                "runtime_rows_hash": canonical_sha256(primitive_rows.runtime_rows),
                "forecast_rows_hash": canonical_sha256(primitive_rows.forecast_rows),
                "desired_absolute_rows_hash": canonical_sha256(primitive_rows.desired_absolute_rows),
            }
        ),
        "primitive_parity_report_hash": primitive_parity.report_hash,
        "segment_bundle_hash": segment.bundle_hash,
        "execution_state_verification_hash": execution_state.verification_hash,
        "segment_artifacts_hash": segment_artifacts.bundle_hash,
        "order_policy_registry_hash": order_policy_registry.registry_hash,
        "order_generation_bundle_hash": order_generation_bundle.bundle_hash,
        "downstream_policy_registry_hash": downstream_policy_registry.registry_hash,
        "downstream_generation_bundle_hash": downstream_generation_bundle.bundle_hash,
        "generated_segment_assembly_hash": generated_segment_assembly.assembly_hash,
        "tbbo_batch_plan_hash": tbbo_plan.plan_hash,
        "cache_snapshot": cache.snapshot(),
        "artifact_family_plan": ARTIFACT_FAMILY_PLAN,
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    result = FastRunnerResult(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        mode=req.mode,
        validation_profile=req.validation_profile,
        engine_stage=ENGINE_STAGE,
        segment_bundle=segment,
        primitive_engine_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        primitive_parity_report=primitive_parity,
        execution_state_verification=execution_state,
        segment_artifacts=segment_artifacts,
        order_policy_registry=order_policy_registry,
        order_generation_bundle=order_generation_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_policy_registry,
        downstream_generation_bundle=downstream_generation_bundle,
        downstream_rows=downstream_rows,
        generated_segment_assembly=generated_segment_assembly,
        tbbo_batch_plan=tbbo_plan,
        cache_snapshot=cache.snapshot(),
        artifact_family_plan=ARTIFACT_FAMILY_PLAN,
        result_interpretation="NO",
        source_faithful_evidence_claim="NO",
        bundle_hash=canonical_sha256(payload),
    )
    result.validate()
    return result


def _prime_cache(
    cache: Sha256ArtifactCache,
    pack_root: Path,
    run_root: Path,
    requirements_root: Path,
) -> None:
    cache.read_json(pack_root / "S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST.json")
    cache.file_ref(pack_root / "S27_V2_2023_TEST_DECLARED_INPUT_PACK_SHA256SUMS.txt")
    cache.read_csv_rows(pack_root / "cost_parameter.csv")
    cache.read_csv_rows(pack_root / "hourly_decision_completed_bar.csv")
    cache.read_csv_rows(pack_root / "hourly_fill_completed_bar.csv")
    cache.read_csv_rows(pack_root / "runtime_evidence_ledger.csv")
    cache.read_csv_rows(pack_root / "valuation_mark_completed_bar.csv")
    cache.read_csv_rows(_REPO_ROOT / DEFAULT_COMBINED_TBBO_RELATIVE_PATH / COMBINED_TBBO_REGISTRY_NAME)
    cache.read_json(run_root / RUN_MANIFEST_NAME)
    cache.read_json(run_root / EVIDENCE_MANIFEST_NAME)
    cache.read_csv_rows(run_root / "desired_position_ledger.csv")
    cache.read_csv_rows(run_root / "forecast_replay_ledger.csv")
    cache.read_csv_rows(run_root / "runtime_history_ledger.csv")
    cache.read_csv_rows(run_root / "pnl_ledger.csv")
    cache.read_csv_rows(run_root / "fail_closed_ledger.csv")
    cache.read_csv_rows(requirements_root / "market_order_tbbo_requirements.csv")


def _require_locked_roots(pack_root: Path, run_root: Path, requirements_root: Path) -> None:
    expected_pack = (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()
    expected_run = (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve()
    expected_requirements = (_REPO_ROOT / DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH).resolve()
    if pack_root != expected_pack:
        raise CarverBlocked("S27 v2 fast runner pack root is locked")
    if run_root != expected_run:
        raise CarverBlocked("S27 v2 fast runner run root is locked")
    if requirements_root != expected_requirements:
        raise CarverBlocked("S27 v2 fast runner TBBO requirements root is locked")


def _validate_cache_snapshot_refs(snapshot: CacheSnapshot) -> None:
    expected_paths = tuple(sorted(str((_REPO_ROOT / relative).resolve()) for relative in EXPECTED_CACHE_RELATIVE_FILES))
    observed_paths = tuple(ref.path for ref in snapshot.cached_file_refs)
    if observed_paths != expected_paths:
        raise CarverBlocked("S27 v2 fast runner cache snapshot path set drift")
    for ref in snapshot.cached_file_refs:
        path = Path(ref.path).resolve()
        if hashlib.sha256(path.read_bytes()).hexdigest() != ref.sha256:
            raise CarverBlocked("S27 v2 fast runner cache snapshot byte hash drift")
        if path.stat().st_size != ref.size_bytes:
            raise CarverBlocked("S27 v2 fast runner cache snapshot size drift")


def _result_payload(result: FastRunnerResult) -> Mapping[str, object]:
    data = asdict(result)
    data["primitive_engine_bundle_hash"] = result.primitive_engine_bundle.bundle_hash
    data["primitive_rows_hash"] = canonical_sha256(
        {
            "runtime_rows_hash": canonical_sha256(result.primitive_rows.runtime_rows),
            "forecast_rows_hash": canonical_sha256(result.primitive_rows.forecast_rows),
            "desired_absolute_rows_hash": canonical_sha256(result.primitive_rows.desired_absolute_rows),
        }
    )
    data["primitive_parity_report_hash"] = result.primitive_parity_report.report_hash
    data["segment_bundle_hash"] = result.segment_bundle.bundle_hash
    data["execution_state_verification_hash"] = result.execution_state_verification.verification_hash
    data["segment_artifacts_hash"] = result.segment_artifacts.bundle_hash
    data["order_policy_registry_hash"] = result.order_policy_registry.registry_hash
    data["order_generation_bundle_hash"] = result.order_generation_bundle.bundle_hash
    data["downstream_policy_registry_hash"] = result.downstream_policy_registry.registry_hash
    data["downstream_generation_bundle_hash"] = result.downstream_generation_bundle.bundle_hash
    data["generated_segment_assembly_hash"] = result.generated_segment_assembly.assembly_hash
    data["tbbo_batch_plan_hash"] = result.tbbo_batch_plan.plan_hash
    data.pop("primitive_engine_bundle", None)
    data.pop("primitive_rows", None)
    data.pop("primitive_parity_report", None)
    data.pop("segment_bundle", None)
    data.pop("execution_state_verification", None)
    data.pop("segment_artifacts", None)
    data.pop("order_policy_registry", None)
    data.pop("order_generation_bundle", None)
    data.pop("order_rows", None)
    data.pop("downstream_policy_registry", None)
    data.pop("downstream_generation_bundle", None)
    data.pop("downstream_rows", None)
    data.pop("generated_segment_assembly", None)
    data.pop("tbbo_batch_plan", None)
    data.pop("bundle_hash", None)
    return data

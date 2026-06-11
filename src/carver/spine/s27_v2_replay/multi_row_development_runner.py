from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

from ..m0 import CarverBlocked
from .constants import ARTIFACT_FAMILIES, S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .runner import ReplayExecutionBlocked
from .validation import require_hash, require_non_empty_tuple, require_text, require_tuple


S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_AUTHORIZATION = (
    "S27_V2_GENERALIZED_MULTI_ROW_CONTROLLED_LOCAL_ONLY_DEVELOPMENT_BACKTEST_RUNNER_MACHINERY"
)
S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_STATUS = (
    "S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_MACHINERY_PRE_RUN_NOT_EXECUTED"
)

WINDOW_ITERATION_PLAN_STATUS = "LOCKED_LOCAL_DEVELOPMENT_WINDOW_ITERATION_PLAN_PRE_RUN"
ARTIFACT_FAMILY_PLAN_STATUS = "RUN_ARTIFACT_FAMILY_REQUIRED_PRE_RUN_NOT_EMITTED"
STALE_RUNNER_EXCLUSION_STATUS = "STALE_DIAGNOSTIC_RUNNER_IMPORTS_EXCLUDED_PRE_RUN"

DEVELOPMENT_WINDOW_LABEL = "OLDEST_SUITABLE_LOCAL_ZN_POST_WARMUP_DEVELOPMENT_WINDOW_PENDING_RUN_AUTHORIZATION"
DEVELOPMENT_EVIDENCE_STAGE = "DEVELOPMENT_RECONCILIATION_ONLY"
DECLARED_ZN_INPUT_PACK_ROOT_RELATIVE_PATH = "docs/researchops/s27_v2_local_replay_inputs/ZN"
PLANNED_ROW_SELECTOR_SURFACE = "select_completed_s27_v2_rows_from_locked_declared_input_pack"

RUNNER_REQUIRED_ARTIFACT_FAMILIES = ARTIFACT_FAMILIES + (
    "RUN_LEVEL_EVIDENCE_MANIFEST",
    "RUN_LEVEL_TRUSTED_BUNDLE_METADATA",
)

STALE_DIAGNOSTIC_RUNNER_PATHS = (
    "tools/databento/carver_s27_zn_2024_corrected_validation_backtest.py",
    "tools/databento/carver_s27_zn_2024_corrected_full_ladder_validation_backtest.py",
    "tools/databento/carver_s27_zn_2025_2026_corrected_test3_backtest.py",
    "tools/databento/carver_s27_zn_m1_ladder_dev_recon_backtest.py",
    "tools/audit/carver_s27_zn_ladder_attribution.py",
    "tools/audit/carver_s27_zn_lockbox_readiness.py",
)

MULTI_ROW_RUNNER_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_CREDENTIAL_USE",
    "NO_PARSER_EXECUTION",
    "NO_FILE_REPLAY",
    "NO_DIAGNOSTICS",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_ACTUAL_BACKTEST_EXECUTION",
    "NO_RESULT_SCORED_RUN",
    "NO_RESULT_INTERPRETATION",
    "NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION",
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
_DECLARED_ZN_INPUT_PACK_ROOT = (_REPO_ROOT / DECLARED_ZN_INPUT_PACK_ROOT_RELATIVE_PATH).resolve()
_UPSTREAM_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_BUNDLE_HASH = (
    "5eb846c4fd83879c6648e9d4132d60f4fdc59ed8626453c9121496e307cacd9e"
)
_UPSTREAM_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_RECORD_RELATIVE_PATH = (
    "docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_IMPLEMENTATION_2026-06-11.md"
)
_UPSTREAM_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_RECORD_PATH = (
    _REPO_ROOT / _UPSTREAM_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_RECORD_RELATIVE_PATH
).resolve()


@dataclass(frozen=True)
class MultiRowDevelopmentWindowIterationPlan:
    status: str
    window_label: str
    evidence_stage_label: str
    declared_input_pack_root: str
    planned_row_selector_surface: str
    local_declared_packs_only: bool
    oldest_post_warmup_slice_required: bool
    completed_bars_only: bool
    strict_prior_per_row_required: bool
    no_oos_lockbox_forward: bool
    row_iteration_contract_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 multi-row window plan standalone validation is not authoritative")

    def _validate_against_active_root(self, active_input_pack_root: Path) -> None:
        if self.status != WINDOW_ITERATION_PLAN_STATUS:
            raise CarverBlocked("S27 v2 multi-row window plan status is not locked")
        if self.window_label != DEVELOPMENT_WINDOW_LABEL:
            raise CarverBlocked("S27 v2 multi-row window label is not locked")
        if self.evidence_stage_label != DEVELOPMENT_EVIDENCE_STAGE:
            raise CarverBlocked("S27 v2 multi-row window must remain Development/Reconciliation")
        if Path(self.declared_input_pack_root).resolve() != active_input_pack_root:
            raise CarverBlocked("S27 v2 multi-row window must bind the declared ZN input-pack root")
        if self.planned_row_selector_surface != PLANNED_ROW_SELECTOR_SURFACE:
            raise CarverBlocked("S27 v2 multi-row row-selector surface is not locked")
        if (
            self.local_declared_packs_only is not True
            or self.oldest_post_warmup_slice_required is not True
            or self.completed_bars_only is not True
            or self.strict_prior_per_row_required is not True
            or self.no_oos_lockbox_forward is not True
        ):
            raise CarverBlocked("S27 v2 multi-row window must preserve local strict-prior completed-bar gates")
        require_hash("S27 v2 multi-row row iteration contract", self.row_iteration_contract_hash)
        if self.row_iteration_contract_hash != _policy_hash(
            "multi_row_window_iteration_contract",
            self.window_label,
            self.evidence_stage_label,
            str(active_input_pack_root),
            self.planned_row_selector_surface,
            self.local_declared_packs_only,
            self.oldest_post_warmup_slice_required,
            self.completed_bars_only,
            self.strict_prior_per_row_required,
            self.no_oos_lockbox_forward,
        ):
            raise CarverBlocked("S27 v2 multi-row row-iteration contract hash must bind window gates")
        require_hash("S27 v2 multi-row window plan row", self.row_hash)
        if self.row_hash != canonical_sha256(_window_plan_hash_payload(self)):
            raise CarverBlocked("S27 v2 multi-row window plan row hash must be content-bound")


@dataclass(frozen=True)
class MultiRowRunnerArtifactFamilyPlanRow:
    artifact_family: str
    status: str
    per_row_artifacts_required: bool
    run_level_closure_required: bool
    fail_closed_when_evidence_insufficient: bool
    emitted_in_this_gate: bool
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 multi-row artifact family row standalone validation is not authoritative")

    def _validate_against_locked_family(self, expected_family: str) -> None:
        if self.artifact_family != expected_family:
            raise CarverBlocked("S27 v2 multi-row artifact family order must match locked run plan")
        if self.status != ARTIFACT_FAMILY_PLAN_STATUS:
            raise CarverBlocked("S27 v2 multi-row artifact family status is not locked")
        if self.per_row_artifacts_required is not True:
            raise CarverBlocked("S27 v2 multi-row artifact family must require per-row artifacts")
        if self.run_level_closure_required is not True:
            raise CarverBlocked("S27 v2 multi-row artifact family must require run-level closure")
        if self.fail_closed_when_evidence_insufficient is not True:
            raise CarverBlocked("S27 v2 multi-row artifact family must fail closed on insufficient evidence")
        if self.emitted_in_this_gate is not False:
            raise CarverBlocked("S27 v2 multi-row artifact family rows must not be emitted by pre-run machinery")
        require_hash("S27 v2 multi-row artifact family row", self.row_hash)
        if self.row_hash != canonical_sha256(_artifact_family_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 multi-row artifact family row hash must be content-bound")


@dataclass(frozen=True)
class StaleDiagnosticRunnerExclusionProof:
    status: str
    allowed_package_root_module: str
    allowed_pre_run_module: str
    forbidden_stale_runner_paths: tuple[str, ...]
    stale_runner_imports_allowed: bool
    repo_wide_scan_required_before_run: bool
    package_root_export_check_required: bool
    proof_policy_hash: str
    proof_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 stale-runner proof standalone validation is not authoritative")

    def _validate_against_locked_paths(self) -> None:
        if self.status != STALE_RUNNER_EXCLUSION_STATUS:
            raise CarverBlocked("S27 v2 stale-runner exclusion status is not locked")
        if self.allowed_package_root_module != "carver.spine.s27_v2_replay":
            raise CarverBlocked("S27 v2 stale-runner allowed package root is not locked")
        if self.allowed_pre_run_module != "carver.spine.s27_v2_replay.multi_row_development_runner":
            raise CarverBlocked("S27 v2 stale-runner allowed pre-run module is not locked")
        require_non_empty_tuple("S27 v2 forbidden stale runner paths", self.forbidden_stale_runner_paths)
        if self.forbidden_stale_runner_paths != STALE_DIAGNOSTIC_RUNNER_PATHS:
            raise CarverBlocked("S27 v2 stale-runner forbidden path tuple is not locked")
        if self.stale_runner_imports_allowed is not False:
            raise CarverBlocked("S27 v2 stale diagnostic runners must not be importable by the v2 runner")
        if self.repo_wide_scan_required_before_run is not True:
            raise CarverBlocked("S27 v2 stale-runner proof must require repo-wide scan before run")
        if self.package_root_export_check_required is not True:
            raise CarverBlocked("S27 v2 stale-runner proof must require package-root export check")
        require_hash("S27 v2 stale-runner proof policy", self.proof_policy_hash)
        if self.proof_policy_hash != _policy_hash(
            "stale_runner_import_exclusion_policy",
            self.allowed_package_root_module,
            self.allowed_pre_run_module,
            self.forbidden_stale_runner_paths,
            self.stale_runner_imports_allowed,
            self.repo_wide_scan_required_before_run,
            self.package_root_export_check_required,
        ):
            raise CarverBlocked("S27 v2 stale-runner proof policy hash must bind locked exclusions")
        require_hash("S27 v2 stale-runner proof", self.proof_hash)
        if self.proof_hash != canonical_sha256(_stale_runner_proof_hash_payload(self)):
            raise CarverBlocked("S27 v2 stale-runner proof hash must be content-bound")


@dataclass(frozen=True)
class MultiRowDevelopmentBacktestRunnerMachineryBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    window_plan: MultiRowDevelopmentWindowIterationPlan
    artifact_family_rows: tuple[MultiRowRunnerArtifactFamilyPlanRow, ...]
    stale_runner_exclusion_proof: StaleDiagnosticRunnerExclusionProof
    upstream_positive_action_closure_bundle_hash: str
    upstream_positive_action_closure_record_path: str
    runner_machinery_ready_for_external_audit: bool
    actual_backtest_execution_authorized: bool
    result_scored_run_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = MULTI_ROW_RUNNER_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_STATUS:
            raise CarverBlocked("S27 v2 multi-row runner status is not locked")
        if self.authorization_label != S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_AUTHORIZATION:
            raise CarverBlocked("S27 v2 multi-row runner authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 multi-row runner must remain S27_V2 ZN only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 multi-row runner must remain source-native futures")
        self.window_plan._validate_against_active_root(_DECLARED_ZN_INPUT_PACK_ROOT)
        require_non_empty_tuple("S27 v2 multi-row artifact family rows", self.artifact_family_rows)
        if tuple(row.artifact_family for row in self.artifact_family_rows) != RUNNER_REQUIRED_ARTIFACT_FAMILIES:
            raise CarverBlocked("S27 v2 multi-row artifact family tuple must match locked required families")
        for expected_family, row in zip(RUNNER_REQUIRED_ARTIFACT_FAMILIES, self.artifact_family_rows, strict=True):
            row._validate_against_locked_family(expected_family)
        self.stale_runner_exclusion_proof._validate_against_locked_paths()
        require_hash(
            "S27 v2 multi-row upstream positive-action closure bundle",
            self.upstream_positive_action_closure_bundle_hash,
        )
        if self.upstream_positive_action_closure_bundle_hash != _UPSTREAM_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_BUNDLE_HASH:
            raise CarverBlocked("S27 v2 multi-row runner must bind recorded positive-action closure checkpoint")
        require_text(
            "S27 v2 multi-row upstream positive-action closure record path",
            self.upstream_positive_action_closure_record_path,
        )
        if Path(self.upstream_positive_action_closure_record_path).resolve() != _UPSTREAM_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_RECORD_PATH:
            raise CarverBlocked("S27 v2 multi-row runner must bind the recorded closure process artifact")
        if self.runner_machinery_ready_for_external_audit is not True:
            raise CarverBlocked("S27 v2 multi-row runner machinery must be ready for external audit")
        if (
            self.actual_backtest_execution_authorized is not False
            or self.result_scored_run_emitted is not False
            or self.result_interpretation_emitted is not False
            or self.pnl_evaluation_emitted is not False
            or self.source_faithful_evidence_claimed is not False
        ):
            raise CarverBlocked("S27 v2 multi-row runner pre-run gate cannot emit run/result/evaluation evidence")
        if self.non_authorizations != MULTI_ROW_RUNNER_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 multi-row runner must preserve non-authorizations")
        require_hash("S27 v2 multi-row runner bundle", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_runner_machinery_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 multi-row runner bundle hash must be content-bound")


def build_s27_v2_multi_row_development_runner_machinery(
    declared_input_pack_root: str | Path = _DECLARED_ZN_INPUT_PACK_ROOT,
) -> MultiRowDevelopmentBacktestRunnerMachineryBundle:
    pack_root = Path(declared_input_pack_root).resolve()
    if pack_root != _DECLARED_ZN_INPUT_PACK_ROOT:
        raise CarverBlocked("S27 v2 multi-row runner is locked to the declared local ZN input-pack root")
    window_plan = _build_window_plan(pack_root)
    artifact_rows = tuple(_build_artifact_family_row(family) for family in RUNNER_REQUIRED_ARTIFACT_FAMILIES)
    stale_proof = _build_stale_runner_exclusion_proof()
    bundle = MultiRowDevelopmentBacktestRunnerMachineryBundle(
        status=S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_STATUS,
        authorization_label=S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        window_plan=window_plan,
        artifact_family_rows=artifact_rows,
        stale_runner_exclusion_proof=stale_proof,
        upstream_positive_action_closure_bundle_hash=_UPSTREAM_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_BUNDLE_HASH,
        upstream_positive_action_closure_record_path=str(_UPSTREAM_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_RECORD_PATH),
        runner_machinery_ready_for_external_audit=True,
        actual_backtest_execution_authorized=False,
        result_scored_run_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = MultiRowDevelopmentBacktestRunnerMachineryBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_runner_machinery_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def execute_s27_v2_multi_row_development_backtest() -> NoReturn:
    raise ReplayExecutionBlocked(
        "S27 v2 multi-row development backtest execution requires separate operator run authorization"
    )


def _build_window_plan(pack_root: Path) -> MultiRowDevelopmentWindowIterationPlan:
    contract_hash = _policy_hash(
        "multi_row_window_iteration_contract",
        DEVELOPMENT_WINDOW_LABEL,
        DEVELOPMENT_EVIDENCE_STAGE,
        str(pack_root),
        PLANNED_ROW_SELECTOR_SURFACE,
        True,
        True,
        True,
        True,
        True,
    )
    row = MultiRowDevelopmentWindowIterationPlan(
        status=WINDOW_ITERATION_PLAN_STATUS,
        window_label=DEVELOPMENT_WINDOW_LABEL,
        evidence_stage_label=DEVELOPMENT_EVIDENCE_STAGE,
        declared_input_pack_root=str(pack_root),
        planned_row_selector_surface=PLANNED_ROW_SELECTOR_SURFACE,
        local_declared_packs_only=True,
        oldest_post_warmup_slice_required=True,
        completed_bars_only=True,
        strict_prior_per_row_required=True,
        no_oos_lockbox_forward=True,
        row_iteration_contract_hash=contract_hash,
        row_hash="0" * 64,
    )
    return MultiRowDevelopmentWindowIterationPlan(
        **{**row.__dict__, "row_hash": canonical_sha256(_window_plan_hash_payload(row))}
    )


def _build_artifact_family_row(family: str) -> MultiRowRunnerArtifactFamilyPlanRow:
    row = MultiRowRunnerArtifactFamilyPlanRow(
        artifact_family=family,
        status=ARTIFACT_FAMILY_PLAN_STATUS,
        per_row_artifacts_required=True,
        run_level_closure_required=True,
        fail_closed_when_evidence_insufficient=True,
        emitted_in_this_gate=False,
        row_hash="0" * 64,
    )
    return MultiRowRunnerArtifactFamilyPlanRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_artifact_family_row_hash_payload(row))}
    )


def _build_stale_runner_exclusion_proof() -> StaleDiagnosticRunnerExclusionProof:
    policy_hash = _policy_hash(
        "stale_runner_import_exclusion_policy",
        "carver.spine.s27_v2_replay",
        "carver.spine.s27_v2_replay.multi_row_development_runner",
        STALE_DIAGNOSTIC_RUNNER_PATHS,
        False,
        True,
        True,
    )
    proof = StaleDiagnosticRunnerExclusionProof(
        status=STALE_RUNNER_EXCLUSION_STATUS,
        allowed_package_root_module="carver.spine.s27_v2_replay",
        allowed_pre_run_module="carver.spine.s27_v2_replay.multi_row_development_runner",
        forbidden_stale_runner_paths=STALE_DIAGNOSTIC_RUNNER_PATHS,
        stale_runner_imports_allowed=False,
        repo_wide_scan_required_before_run=True,
        package_root_export_check_required=True,
        proof_policy_hash=policy_hash,
        proof_hash="0" * 64,
    )
    return StaleDiagnosticRunnerExclusionProof(
        **{**proof.__dict__, "proof_hash": canonical_sha256(_stale_runner_proof_hash_payload(proof))}
    )


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_POLICY", "label": label, "values": values})


def _window_plan_hash_payload(row: MultiRowDevelopmentWindowIterationPlan) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _artifact_family_row_hash_payload(row: MultiRowRunnerArtifactFamilyPlanRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _stale_runner_proof_hash_payload(proof: StaleDiagnosticRunnerExclusionProof) -> dict[str, object]:
    return {key: value for key, value in proof.__dict__.items() if key != "proof_hash"}


def _runner_machinery_bundle_hash_payload(bundle: MultiRowDevelopmentBacktestRunnerMachineryBundle) -> dict[str, object]:
    return {
        "actual_backtest_execution_authorized": bundle.actual_backtest_execution_authorized,
        "artifact": "S27_V2_MULTI_ROW_DEVELOPMENT_BACKTEST_RUNNER_MACHINERY_BUNDLE",
        "artifact_family_row_hashes": tuple(row.row_hash for row in bundle.artifact_family_rows),
        "authorization_label": bundle.authorization_label,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "pnl_evaluation_emitted": bundle.pnl_evaluation_emitted,
        "result_interpretation_emitted": bundle.result_interpretation_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "runner_machinery_ready_for_external_audit": bundle.runner_machinery_ready_for_external_audit,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "stale_runner_exclusion_proof_hash": bundle.stale_runner_exclusion_proof.proof_hash,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "upstream_positive_action_closure_bundle_hash": bundle.upstream_positive_action_closure_bundle_hash,
        "upstream_positive_action_closure_record_path": bundle.upstream_positive_action_closure_record_path,
        "window_plan_hash": bundle.window_plan.row_hash,
    }

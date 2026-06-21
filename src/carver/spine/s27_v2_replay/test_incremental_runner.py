from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from ..m0 import CarverBlocked
from .local_replay import canonical_sha256


AUTHORIZATION = "S27_V2_TEST_RUNNER_PERFORMANCE_AND_INCREMENTAL_VALIDATION_REMEDIATION_GATE"
STATUS = "LOCAL_2023_TEST_INCREMENTAL_SEGMENT_VALIDATED_NOT_RESULT"
CHECKPOINT_STATUS = "LOCAL_2023_TEST_INCREMENTAL_CHECKPOINT_HASH_BOUND_NOT_RESULT"
TBBO_PLAN_STATUS = "LOCAL_2023_TEST_INCREMENTAL_TBBO_REQUIREMENTS_PLANNED_NOT_PROVIDER_NOT_RESULT"
VALIDATION_MODE = "INCREMENTAL_SEGMENT_ONLY_NOT_FULL_REPLAY"
SOURCE_MODE = "EXISTING_MECHANICAL_ARTIFACT_SEGMENT_REUSED_FOR_INCREMENTAL_REMEDIATION_NOT_RESULT"

RESULT_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
BACKTEST_STATUS = "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"
PNL_EVALUATION_STATUS = "MECHANICAL_PNL_ROW_CONSTRUCTION_ONLY_NOT_RESULT_INTERPRETATION"
SOURCE_FAITHFUL_FALSE_VALUES = {"FALSE", "False", "false", False}

DEFAULT_BASELINE_ROW_INDEX = 703
DEFAULT_SEGMENT_START_ROW_INDEX = 704
DEFAULT_SEGMENT_END_ROW_INDEX = 1378
DEFAULT_TERMINAL_FAIL_ROW_INDEX = 0
PACK_EXHAUSTED_TERMINAL_REASON = "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"
PACK_EXHAUSTED_TERMINAL_ROW_HASH = canonical_sha256(
    {
        "row_index": "0",
        "fail_closed_reason": PACK_EXHAUSTED_TERMINAL_REASON,
        "row_status": "LOCAL_2023_TEST_DECLARED_PACK_EXHAUSTED_TERMINAL_METADATA_NOT_RESULT",
    }
)
EXPECTED_BASELINE_PNL_ROW_HASH = "7130d2599a5571567ae416b38af0e81f19b72cf9c5237490c306568705dd85da"
EXPECTED_BASELINE_VALIDATION_ROW_HASH = "016f266c60cb34961e787e6bb1e5f8206e9139a024694988f7f4f87b799c9c3c"

DEFAULT_PACK_RELATIVE_PATH = "docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack"
DEFAULT_OUTPUT_RELATIVE_PATH = "docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run"
DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    "20260612_2023_test_market_order_tbbo_requirements_discovery"
)
DEFAULT_COMBINED_TBBO_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    "20260612_2023_test_combined_market_order_tbbo_registry"
)

INPUT_MANIFEST_NAME = "S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST.json"
INPUT_SHA256SUMS_NAME = "S27_V2_2023_TEST_DECLARED_INPUT_PACK_SHA256SUMS.txt"
RUN_MANIFEST_NAME = "run_manifest.json"
EVIDENCE_MANIFEST_NAME = "evidence_manifest.json"
TBBO_REQUIREMENTS_LEDGER_NAME = "market_order_tbbo_requirements.csv"
COMBINED_TBBO_REGISTRY_NAME = "combined_market_order_tbbo_registry.csv"
COMBINED_TBBO_MANIFEST_NAME = "combined_market_order_tbbo_registry_manifest.json"

RUN_LEDGER_FILES = (
    "runtime_history_ledger.csv",
    "forecast_replay_ledger.csv",
    "desired_position_ledger.csv",
    "limit_order_ledger.csv",
    "no_market_order_ledger.csv",
    "market_order_ledger.csv",
    "working_order_transition_ledger.csv",
    "fill_ledger.csv",
    "market_fill_metadata_ledger.csv",
    "cost_ledger.csv",
    "pnl_ledger.csv",
    "validation_ledger.csv",
)

DENSE_SEGMENT_LEDGER_FILES = tuple(
    name
    for name in RUN_LEDGER_FILES
    if name not in {"market_order_ledger.csv", "market_fill_metadata_ledger.csv"}
)

NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_VALIDATION_ACCESS",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
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


@dataclass(frozen=True)
class ImmutableFileRef:
    relative_path: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class IncrementalCheckpoint:
    status: str
    authorization_label: str
    row_index: int
    source_output_root: str
    pnl_row_hash: str
    validation_row_hash: str
    ending_position_contracts: str
    valuation_mark_close_price: str
    cumulative_gross_pnl_amount: str
    cumulative_commission_amount: str
    cumulative_spread_amount: str
    cumulative_net_pnl_amount: str
    source_run_manifest_hash: str
    source_evidence_manifest_hash: str
    source_pnl_ledger_hash: str
    trusted_checkpoint_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != CHECKPOINT_STATUS:
            raise CarverBlocked("S27 v2 incremental checkpoint status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 incremental checkpoint authorization mismatch")
        if self.row_index != DEFAULT_BASELINE_ROW_INDEX:
            raise CarverBlocked("S27 v2 incremental checkpoint must bind row 703 trust baseline")
        if self.pnl_row_hash != EXPECTED_BASELINE_PNL_ROW_HASH:
            raise CarverBlocked("S27 v2 incremental checkpoint row-703 PnL hash drift")
        if self.validation_row_hash != EXPECTED_BASELINE_VALIDATION_ROW_HASH:
            raise CarverBlocked("S27 v2 incremental checkpoint row-703 validation hash drift")
        if self.ending_position_contracts != "0":
            raise CarverBlocked("S27 v2 incremental checkpoint row-703 ending position drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 incremental checkpoint non-authorizations drift")
        if self.trusted_checkpoint_hash != canonical_sha256(_checkpoint_payload(self)):
            raise CarverBlocked("S27 v2 incremental checkpoint hash drift")


@dataclass(frozen=True)
class IncrementalSegmentBundle:
    status: str
    authorization_label: str
    validation_mode: str
    source_mode: str
    run_root: str
    pack_root: str
    baseline_checkpoint: IncrementalCheckpoint
    segment_start_row_index: int
    segment_end_row_index: int
    segment_row_count: int
    terminal_fail_row_index: int
    terminal_fail_reason: str
    terminal_fail_row_hash: str
    ledger_row_counts: Mapping[str, int]
    segment_ledger_hashes: Mapping[str, str]
    immutable_file_refs: tuple[ImmutableFileRef, ...]
    parity_rows_verified: tuple[int, ...]
    segment_manifest_hash: str
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 incremental segment status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 incremental segment authorization mismatch")
        if self.validation_mode != VALIDATION_MODE:
            raise CarverBlocked("S27 v2 incremental segment validation mode drift")
        if self.source_mode != SOURCE_MODE:
            raise CarverBlocked("S27 v2 incremental segment source mode drift")
        if self.baseline_checkpoint.row_index != DEFAULT_BASELINE_ROW_INDEX:
            raise CarverBlocked("S27 v2 incremental segment baseline must be row 703")
        if self.segment_start_row_index != DEFAULT_SEGMENT_START_ROW_INDEX:
            raise CarverBlocked("S27 v2 incremental segment start must be row 704")
        if self.segment_end_row_index != DEFAULT_SEGMENT_END_ROW_INDEX:
            raise CarverBlocked("S27 v2 incremental segment end must be row 1378")
        if self.segment_row_count != DEFAULT_SEGMENT_END_ROW_INDEX - DEFAULT_SEGMENT_START_ROW_INDEX + 1:
            raise CarverBlocked("S27 v2 incremental segment row count drift")
        if self.terminal_fail_row_index != DEFAULT_TERMINAL_FAIL_ROW_INDEX:
            raise CarverBlocked("S27 v2 incremental terminal state must be declared-pack exhaustion")
        if self.terminal_fail_reason != PACK_EXHAUSTED_TERMINAL_REASON:
            raise CarverBlocked("S27 v2 incremental terminal reason must be pack exhaustion")
        if self.terminal_fail_row_hash != PACK_EXHAUSTED_TERMINAL_ROW_HASH:
            raise CarverBlocked("S27 v2 incremental terminal pack-exhausted hash drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 incremental segment non-authorizations drift")
        self.baseline_checkpoint.validate()
        expected_manifest = canonical_sha256(_segment_manifest_payload(self))
        if self.segment_manifest_hash != expected_manifest:
            raise CarverBlocked("S27 v2 incremental segment manifest hash drift")
        if self.bundle_hash != canonical_sha256(_segment_bundle_payload(self)):
            raise CarverBlocked("S27 v2 incremental segment bundle hash drift")

    def validate_against_active_files(self) -> None:
        self.validate()
        active = build_incremental_segment_from_existing_artifacts(
            baseline_row_index=self.baseline_checkpoint.row_index,
            segment_start_row_index=self.segment_start_row_index,
            segment_end_row_index=self.segment_end_row_index,
            terminal_fail_row_index=self.terminal_fail_row_index,
            run_root=Path(self.run_root),
            pack_root=Path(self.pack_root),
        )
        if active.bundle_hash != self.bundle_hash:
            raise CarverBlocked("S27 v2 incremental segment does not match active local files")


@dataclass(frozen=True)
class MissingTBBOBatchPlan:
    status: str
    authorization_label: str
    requirements_ledger_path: str
    requirements_ledger_sha256: str
    missing_requirement_count: int
    first_missing_row_index: int | None
    last_missing_row_index: int | None
    grouped_missing_row_indexes_by_symbol: Mapping[str, tuple[int, ...]]
    plan_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != TBBO_PLAN_STATUS:
            raise CarverBlocked("S27 v2 incremental TBBO plan status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 incremental TBBO plan authorization mismatch")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 incremental TBBO plan non-authorizations drift")
        if self.requirements_ledger_sha256 != _sha256(Path(self.requirements_ledger_path)):
            raise CarverBlocked("S27 v2 incremental TBBO plan requirements hash drift")
        if self.last_missing_row_index is not None and self.last_missing_row_index > DEFAULT_TERMINAL_FAIL_ROW_INDEX:
            raise CarverBlocked("S27 v2 incremental TBBO plan crosses terminal blocker row")
        if self.plan_hash != canonical_sha256(_tbbo_plan_payload(self)):
            raise CarverBlocked("S27 v2 incremental TBBO plan hash drift")


def build_incremental_segment_from_existing_artifacts(
    *,
    baseline_row_index: int = DEFAULT_BASELINE_ROW_INDEX,
    segment_start_row_index: int = DEFAULT_SEGMENT_START_ROW_INDEX,
    segment_end_row_index: int = DEFAULT_SEGMENT_END_ROW_INDEX,
    terminal_fail_row_index: int = DEFAULT_TERMINAL_FAIL_ROW_INDEX,
    run_root: Path | str | None = None,
    pack_root: Path | str | None = None,
) -> IncrementalSegmentBundle:
    run_root_path = _resolve_root(run_root, DEFAULT_OUTPUT_RELATIVE_PATH)
    pack_root_path = _resolve_root(pack_root, DEFAULT_PACK_RELATIVE_PATH)
    _require_locked_root(pack_root_path, DEFAULT_PACK_RELATIVE_PATH, "input pack")
    _require_locked_root(run_root_path, DEFAULT_OUTPUT_RELATIVE_PATH, "run artifact")
    if baseline_row_index != DEFAULT_BASELINE_ROW_INDEX:
        raise CarverBlocked("S27 v2 incremental segment must resume from row 703 trust baseline")
    if segment_start_row_index != DEFAULT_SEGMENT_START_ROW_INDEX:
        raise CarverBlocked("S27 v2 incremental segment start must be locked to row 704")
    if segment_end_row_index != DEFAULT_SEGMENT_END_ROW_INDEX:
        raise CarverBlocked("S27 v2 incremental segment end must be locked to row 1378")
    if terminal_fail_row_index != DEFAULT_TERMINAL_FAIL_ROW_INDEX:
        raise CarverBlocked("S27 v2 incremental terminal state must be locked to pack exhaustion")
    if segment_start_row_index <= baseline_row_index:
        raise CarverBlocked("S27 v2 incremental segment must append after the baseline checkpoint")
    if segment_end_row_index < segment_start_row_index:
        raise CarverBlocked("S27 v2 incremental segment end precedes start")
    checkpoint = build_incremental_checkpoint(
        row_index=baseline_row_index,
        run_root=run_root_path,
    )
    _verify_run_and_evidence_manifests(run_root_path)

    segment_rows_by_ledger: dict[str, list[dict[str, str]]] = {}
    ledger_counts: dict[str, int] = {}
    ledger_hashes: dict[str, str] = {}
    for ledger_name in RUN_LEDGER_FILES:
        rows = list(_read_csv_rows_in_range(run_root_path / ledger_name, segment_start_row_index, segment_end_row_index))
        _validate_segment_rows(ledger_name, rows)
        if ledger_name in DENSE_SEGMENT_LEDGER_FILES:
            _validate_dense_segment_continuity(ledger_name, rows, segment_start_row_index, segment_end_row_index)
        segment_rows_by_ledger[ledger_name] = rows
        ledger_counts[ledger_name] = len(rows)
        ledger_hashes[ledger_name] = canonical_sha256(
            {
                "ledger_name": ledger_name,
                "segment_start_row_index": segment_start_row_index,
                "segment_end_row_index": segment_end_row_index,
                "rows": rows,
            }
        )

    terminal = _pack_exhausted_terminal_row(run_root_path)
    _validate_terminal_fail_row(terminal)
    terminal_reason = str(terminal["fail_closed_reason"])

    parity_rows = _validate_known_parity_rows(segment_rows_by_ledger, terminal)
    refs = _immutable_file_refs(pack_root_path, run_root_path)
    manifest_hash = canonical_sha256(
        {
            "status": STATUS,
            "authorization_label": AUTHORIZATION,
            "validation_mode": VALIDATION_MODE,
            "source_mode": SOURCE_MODE,
            "baseline_checkpoint_hash": checkpoint.trusted_checkpoint_hash,
            "segment_start_row_index": segment_start_row_index,
            "segment_end_row_index": segment_end_row_index,
            "terminal_fail_row_index": terminal_fail_row_index,
            "terminal_fail_reason": terminal_reason,
            "terminal_fail_row_hash": terminal["row_hash"],
            "ledger_row_counts": ledger_counts,
            "segment_ledger_hashes": ledger_hashes,
            "immutable_file_refs": refs,
            "parity_rows_verified": parity_rows,
            "non_authorizations": NON_AUTHORIZATIONS,
        }
    )
    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "validation_mode": VALIDATION_MODE,
        "source_mode": SOURCE_MODE,
        "run_root": str(run_root_path),
        "pack_root": str(pack_root_path),
        "baseline_checkpoint": checkpoint,
        "segment_start_row_index": segment_start_row_index,
        "segment_end_row_index": segment_end_row_index,
        "segment_row_count": segment_end_row_index - segment_start_row_index + 1,
        "terminal_fail_row_index": terminal_fail_row_index,
        "terminal_fail_reason": terminal_reason,
        "terminal_fail_row_hash": terminal["row_hash"],
        "ledger_row_counts": ledger_counts,
        "segment_ledger_hashes": ledger_hashes,
        "immutable_file_refs": refs,
        "parity_rows_verified": parity_rows,
        "segment_manifest_hash": manifest_hash,
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    bundle_hash = canonical_sha256(payload)
    bundle = IncrementalSegmentBundle(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        validation_mode=VALIDATION_MODE,
        source_mode=SOURCE_MODE,
        run_root=str(run_root_path),
        pack_root=str(pack_root_path),
        baseline_checkpoint=checkpoint,
        segment_start_row_index=segment_start_row_index,
        segment_end_row_index=segment_end_row_index,
        segment_row_count=segment_end_row_index - segment_start_row_index + 1,
        terminal_fail_row_index=terminal_fail_row_index,
        terminal_fail_reason=terminal_reason,
        terminal_fail_row_hash=str(terminal["row_hash"]),
        ledger_row_counts=ledger_counts,
        segment_ledger_hashes=ledger_hashes,
        immutable_file_refs=refs,
        parity_rows_verified=parity_rows,
        segment_manifest_hash=manifest_hash,
        bundle_hash=bundle_hash,
    )
    bundle.validate()
    return bundle


def build_incremental_checkpoint(
    *,
    row_index: int = DEFAULT_BASELINE_ROW_INDEX,
    run_root: Path | str | None = None,
) -> IncrementalCheckpoint:
    run_root_path = _resolve_root(run_root, DEFAULT_OUTPUT_RELATIVE_PATH)
    _require_locked_root(run_root_path, DEFAULT_OUTPUT_RELATIVE_PATH, "run artifact")
    if row_index != DEFAULT_BASELINE_ROW_INDEX:
        raise CarverBlocked("S27 v2 incremental checkpoint must bind row 703 trust baseline")
    _verify_run_and_evidence_manifests(run_root_path)
    pnl = _single_row_by_index(run_root_path / "pnl_ledger.csv", row_index)
    validation = _single_row_by_index(run_root_path / "validation_ledger.csv", row_index)
    _validate_non_result_row("pnl_ledger.csv", pnl)
    _validate_non_result_row("validation_ledger.csv", validation)
    payload = {
        "status": CHECKPOINT_STATUS,
        "authorization_label": AUTHORIZATION,
        "row_index": row_index,
        "source_output_root": str(run_root_path),
        "pnl_row_hash": pnl["row_hash"],
        "validation_row_hash": validation["row_hash"],
        "ending_position_contracts": pnl["ending_position_contracts"],
        "valuation_mark_close_price": pnl["valuation_mark_close_price"],
        "cumulative_gross_pnl_amount": pnl["cumulative_gross_pnl_amount"],
        "cumulative_commission_amount": pnl["cumulative_commission_amount"],
        "cumulative_spread_amount": pnl["cumulative_spread_amount"],
        "cumulative_net_pnl_amount": pnl["cumulative_net_pnl_amount"],
        "source_run_manifest_hash": _sha256(run_root_path / RUN_MANIFEST_NAME),
        "source_evidence_manifest_hash": _sha256(run_root_path / EVIDENCE_MANIFEST_NAME),
        "source_pnl_ledger_hash": _sha256(run_root_path / "pnl_ledger.csv"),
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    checkpoint = IncrementalCheckpoint(
        status=CHECKPOINT_STATUS,
        authorization_label=AUTHORIZATION,
        row_index=row_index,
        source_output_root=str(run_root_path),
        pnl_row_hash=str(pnl["row_hash"]),
        validation_row_hash=str(validation["row_hash"]),
        ending_position_contracts=str(pnl["ending_position_contracts"]),
        valuation_mark_close_price=str(pnl["valuation_mark_close_price"]),
        cumulative_gross_pnl_amount=str(pnl["cumulative_gross_pnl_amount"]),
        cumulative_commission_amount=str(pnl["cumulative_commission_amount"]),
        cumulative_spread_amount=str(pnl["cumulative_spread_amount"]),
        cumulative_net_pnl_amount=str(pnl["cumulative_net_pnl_amount"]),
        source_run_manifest_hash=str(payload["source_run_manifest_hash"]),
        source_evidence_manifest_hash=str(payload["source_evidence_manifest_hash"]),
        source_pnl_ledger_hash=str(payload["source_pnl_ledger_hash"]),
        trusted_checkpoint_hash=canonical_sha256(payload),
    )
    checkpoint.validate()
    return checkpoint


def build_missing_tbbo_batch_plan(
    *,
    requirements_root: Path | str | None = None,
) -> MissingTBBOBatchPlan:
    root = _resolve_root(requirements_root, DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH)
    _require_locked_root(root, DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH, "TBBO requirements")
    ledger = root / TBBO_REQUIREMENTS_LEDGER_NAME
    if not ledger.exists():
        raise CarverBlocked("S27 v2 incremental TBBO requirements ledger is missing")
    missing: list[dict[str, str]] = [
        row
        for row in _read_csv_rows(ledger)
        if row.get("tbbo_requirement_status") == "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"
        and int(row["row_index"]) <= DEFAULT_TERMINAL_FAIL_ROW_INDEX
    ]
    grouped: dict[str, list[int]] = {}
    for row in missing:
        _validate_requirement_row(row)
        grouped.setdefault(row["raw_symbol"], []).append(int(row["row_index"]))
    grouped_tuple = {symbol: tuple(rows) for symbol, rows in sorted(grouped.items())}
    payload = {
        "status": TBBO_PLAN_STATUS,
        "authorization_label": AUTHORIZATION,
        "requirements_ledger_path": str(ledger.resolve()),
        "requirements_ledger_sha256": _sha256(ledger),
        "missing_requirement_count": len(missing),
        "first_missing_row_index": int(missing[0]["row_index"]) if missing else None,
        "last_missing_row_index": int(missing[-1]["row_index"]) if missing else None,
        "grouped_missing_row_indexes_by_symbol": grouped_tuple,
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    plan = MissingTBBOBatchPlan(
        status=TBBO_PLAN_STATUS,
        authorization_label=AUTHORIZATION,
        requirements_ledger_path=str(ledger.resolve()),
        requirements_ledger_sha256=str(payload["requirements_ledger_sha256"]),
        missing_requirement_count=len(missing),
        first_missing_row_index=payload["first_missing_row_index"],
        last_missing_row_index=payload["last_missing_row_index"],
        grouped_missing_row_indexes_by_symbol=grouped_tuple,
        plan_hash=canonical_sha256(payload),
    )
    plan.validate()
    return plan


def write_segment_metadata(bundle: IncrementalSegmentBundle, output_root: Path | str) -> None:
    bundle.validate_against_active_files()
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    _write_json(root / "checkpoint_manifest.json", _checkpoint_public_payload(bundle.baseline_checkpoint))
    _write_json(root / "segment_manifest.json", _segment_manifest_payload(bundle))
    _write_json(root / "segment_ledger_hashes.json", dict(bundle.segment_ledger_hashes))
    run_root = Path(bundle.run_root).resolve()
    for ledger_name in RUN_LEDGER_FILES:
        rows = list(
            _read_csv_rows_in_range(
                run_root / ledger_name,
                bundle.segment_start_row_index,
                bundle.segment_end_row_index,
            )
        )
        _write_csv_rows(root / _segment_csv_name(ledger_name), rows)
    terminal_fail = _pack_exhausted_terminal_row(run_root)
    _write_csv_rows(root / "fail_closed_ledger_terminal.csv", [terminal_fail])


def _resolve_root(path: Path | str | None, default_relative_path: str) -> Path:
    if path is None:
        return (_REPO_ROOT / default_relative_path).resolve()
    return Path(path).resolve()


def _require_locked_root(path: Path, default_relative_path: str, label: str) -> None:
    expected = (_REPO_ROOT / default_relative_path).resolve()
    if path != expected:
        raise CarverBlocked(f"S27 v2 incremental {label} root is locked")


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise CarverBlocked(f"Missing CSV artifact: {path}")
    with path.open("r", encoding="ascii", newline="") as handle:
        return list(csv.DictReader(handle))


def _read_csv_rows_in_range(path: Path, start_row_index: int, end_row_index: int) -> Iterable[dict[str, str]]:
    if not path.exists():
        raise CarverBlocked(f"Missing CSV artifact: {path}")
    with path.open("r", encoding="ascii", newline="") as handle:
        for row in csv.DictReader(handle):
            raw_index = row.get("row_index")
            if raw_index is None or raw_index == "":
                raise CarverBlocked(f"CSV artifact lacks row_index: {path}")
            index = int(raw_index)
            if start_row_index <= index <= end_row_index:
                yield row


def _single_row_by_index(path: Path, row_index: int) -> dict[str, str]:
    matches = [row for row in _read_csv_rows_in_range(path, row_index, row_index)]
    if len(matches) != 1:
        raise CarverBlocked(f"Expected exactly one row {row_index} in {path.name}")
    return matches[0]


def _pack_exhausted_terminal_row(run_root: Path) -> dict[str, str]:
    fail_closed_rows = _read_csv_rows(run_root / "fail_closed_ledger.csv")
    if fail_closed_rows:
        raise CarverBlocked("S27 v2 incremental pack-exhausted terminal requires empty fail-closed ledger")
    return {
        "row_index": "0",
        "fail_closed_reason": PACK_EXHAUSTED_TERMINAL_REASON,
        "result_status": RESULT_STATUS,
        "backtest_status": BACKTEST_STATUS,
        "source_faithful_evidence_claimed": "FALSE",
        "row_status": "LOCAL_2023_TEST_DECLARED_PACK_EXHAUSTED_TERMINAL_METADATA_NOT_RESULT",
        "row_hash": PACK_EXHAUSTED_TERMINAL_ROW_HASH,
    }


def _validate_segment_rows(ledger_name: str, rows: list[dict[str, str]]) -> None:
    seen_hashes: set[str] = set()
    seen_row_indexes: set[str] = set()
    for row in rows:
        if not row.get("row_index"):
            raise CarverBlocked(f"{ledger_name} segment row is missing row_index")
        if row["row_index"] in seen_row_indexes:
            raise CarverBlocked(f"{ledger_name} segment row_index is duplicated")
        seen_row_indexes.add(row["row_index"])
        if not row.get("row_hash"):
            raise CarverBlocked(f"{ledger_name} segment row is missing row_hash")
        if row["row_hash"] in seen_hashes:
            raise CarverBlocked(f"{ledger_name} segment row hash is duplicated")
        seen_hashes.add(row["row_hash"])
        _validate_non_result_row(ledger_name, row)
        _validate_timestamp_boundaries(ledger_name, row)


def _validate_dense_segment_continuity(
    ledger_name: str,
    rows: list[dict[str, str]],
    start_row_index: int,
    end_row_index: int,
) -> None:
    observed = [int(row["row_index"]) for row in rows]
    expected = list(range(start_row_index, end_row_index + 1))
    if observed != expected:
        raise CarverBlocked(f"{ledger_name} dense segment rows are not contiguous")


def _validate_terminal_fail_row(row: Mapping[str, str]) -> None:
    _validate_non_result_row("fail_closed_ledger.csv", row)
    if row.get("fail_closed_reason") == PACK_EXHAUSTED_TERMINAL_REASON:
        if str(row.get("row_index")) != "0":
            raise CarverBlocked("S27 v2 incremental pack-exhausted terminal row index drift")
        if row.get("row_hash") != PACK_EXHAUSTED_TERMINAL_ROW_HASH:
            raise CarverBlocked("S27 v2 incremental pack-exhausted terminal hash drift")
        if row.get("row_status") != "LOCAL_2023_TEST_DECLARED_PACK_EXHAUSTED_TERMINAL_METADATA_NOT_RESULT":
            raise CarverBlocked("S27 v2 incremental pack-exhausted terminal status drift")
        return
    if row.get("fail_closed_reason") != "FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT":
        raise CarverBlocked("S27 v2 incremental terminal blocker reason drift")
    if row.get("market_order_required") != "TRUE":
        raise CarverBlocked("S27 v2 incremental terminal blocker must require market-order evidence")
    if row.get("market_order_rows_emitted") != "FALSE":
        raise CarverBlocked("S27 v2 incremental terminal blocker must not emit market order rows")
    if row.get("market_spread_cost_status") != "FAIL_CLOSED_BOUNDED_TBBO_SPREAD_EVIDENCE_REQUIRED_FOR_MARKET_ORDER":
        raise CarverBlocked("S27 v2 incremental terminal blocker must preserve missing-TBBO cost status")


def _validate_non_result_row(ledger_name: str, row: Mapping[str, Any]) -> None:
    if "result_status" in row and row["result_status"] != RESULT_STATUS:
        raise CarverBlocked(f"{ledger_name} result status is not fail-closed")
    if "backtest_status" in row and row["backtest_status"] != BACKTEST_STATUS:
        raise CarverBlocked(f"{ledger_name} backtest status is not fail-closed")
    if "pnl_evaluation_status" in row and row["pnl_evaluation_status"] != PNL_EVALUATION_STATUS:
        raise CarverBlocked(f"{ledger_name} PnL evaluation status drift")
    if "source_faithful_evidence_claimed" in row and row["source_faithful_evidence_claimed"] not in SOURCE_FAITHFUL_FALSE_VALUES:
        raise CarverBlocked(f"{ledger_name} source-faithful evidence claim is not false")


def _validate_timestamp_boundaries(ledger_name: str, row: Mapping[str, str]) -> None:
    for key, value in row.items():
        if not key.endswith("_timestamp_utc") or value in {"", "NOT_APPLICABLE"}:
            continue
        if not value.startswith("2023-"):
            raise CarverBlocked(f"{ledger_name} timestamp is outside the 2023 TEST window")


def _validate_known_parity_rows(
    segment_rows_by_ledger: Mapping[str, list[dict[str, str]]],
    terminal_fail: Mapping[str, str],
) -> tuple[int, ...]:
    verified: list[int] = []
    pnl_by_index = _rows_by_index(segment_rows_by_ledger["pnl_ledger.csv"])
    market_by_index = _rows_by_index(segment_rows_by_ledger["market_order_ledger.csv"])
    fill_meta_by_index = _rows_by_index(segment_rows_by_ledger["market_fill_metadata_ledger.csv"])
    cost_by_index = _rows_by_index(segment_rows_by_ledger["cost_ledger.csv"])

    _require_fields(
        pnl_by_index.get(704, {}),
        {
            "ending_position_contracts": "0",
            "row_status": "LOCAL_ENGINEERING_ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSED_ROW_EMITTED_NOT_RESULT",
        },
        "row 704 roll-boundary suppression parity",
    )
    verified.append(704)
    _require_fields(
        market_by_index.get(1374, {}),
        {
            "order_side": "SELL",
            "order_quantity": "2",
            "target_position_after_fill": "5",
        },
        "row 1374 market-order parity",
    )
    _require_fields(
        fill_meta_by_index.get(1374, {}),
        {
            "fill_timestamp_utc": "2023-03-30T18:00:00Z",
            "fill_price": "114.515625",
            "fill_quantity": "2",
        },
        "row 1374 fill parity",
    )
    _require_fields(
        cost_by_index.get(1374, {}),
        {
            "commission_amount": "4.6",
            "spread_cost_amount": "0.0",
            "total_cost_amount": "4.6",
            "tbbo_quote_ts_event": "2023-03-30T17:59:58.005200809Z",
            "tbbo_bid_px": "114.515625",
        },
        "row 1374 cost/TBBO parity",
    )
    _require_fields(
        pnl_by_index.get(1374, {}),
        {
            "row_net_pnl_amount": "386.025",
            "ending_position_contracts": "5",
        },
        "row 1374 PnL parity",
    )
    verified.append(1374)
    _require_fields(
        market_by_index.get(1378, {}),
        {
            "order_side": "SELL",
            "order_quantity": "2",
            "target_position_after_fill": "3",
        },
        "row 1378 market-order parity",
    )
    _require_fields(
        fill_meta_by_index.get(1378, {}),
        {
            "fill_timestamp_utc": "2023-03-31T00:00:00Z",
            "fill_price": "114.515625",
            "fill_quantity": "2",
        },
        "row 1378 fill parity",
    )
    _require_fields(
        cost_by_index.get(1378, {}),
        {
            "commission_amount": "4.6",
            "spread_cost_amount": "0.0",
            "total_cost_amount": "4.6",
            "tbbo_quote_ts_event": "2023-03-31T00:00:00.183796035Z",
            "tbbo_bid_px": "114.515625",
        },
        "row 1378 cost/TBBO parity",
    )
    _require_fields(
        pnl_by_index.get(1378, {}),
        {
            "row_net_pnl_amount": "-51.475",
            "ending_position_contracts": "3",
        },
        "row 1378 PnL parity",
    )
    if terminal_fail.get("fail_closed_reason") != PACK_EXHAUSTED_TERMINAL_REASON:
        raise CarverBlocked("S27 v2 incremental parity expects pack-exhausted terminal state")
    verified.append(1378)
    return tuple(sorted(set(verified)))


def _rows_by_index(rows: list[dict[str, str]]) -> dict[int, dict[str, str]]:
    return {int(row["row_index"]): row for row in rows}


def _require_fields(row: Mapping[str, str], expected: Mapping[str, str], label: str) -> None:
    for key, value in expected.items():
        if str(row.get(key)) != value:
            raise CarverBlocked(f"S27 v2 incremental {label} mismatch for {key}")


def _validate_requirement_row(row: Mapping[str, str]) -> None:
    if not str(row.get("decision_timestamp_utc", "")).startswith("2023-"):
        raise CarverBlocked("S27 v2 incremental TBBO requirement decision is outside 2023")
    if not str(row.get("fill_candidate_timestamp_utc", "")).startswith("2023-"):
        raise CarverBlocked("S27 v2 incremental TBBO requirement fill candidate is outside 2023")
    if row.get("result_interpretation_authorized") not in SOURCE_FAITHFUL_FALSE_VALUES:
        raise CarverBlocked("S27 v2 incremental TBBO plan must not authorize result interpretation")
    if row.get("source_faithful_evidence_claimed") not in SOURCE_FAITHFUL_FALSE_VALUES:
        raise CarverBlocked("S27 v2 incremental TBBO plan must not claim source-faithful evidence")


def _verify_run_and_evidence_manifests(run_root: Path) -> None:
    run_manifest = _read_json(run_root / RUN_MANIFEST_NAME)
    evidence_manifest = _read_json(run_root / EVIDENCE_MANIFEST_NAME)
    if run_manifest.get("result_interpretation") != "NO":
        raise CarverBlocked("S27 v2 incremental run manifest result interpretation drift")
    if run_manifest.get("source_faithful_evidence_claim") != "NO":
        raise CarverBlocked("S27 v2 incremental run manifest source-faithful claim drift")
    if tuple(run_manifest.get("non_authorizations", ())) != NON_AUTHORIZATIONS:
        raise CarverBlocked("S27 v2 incremental run manifest non-authorizations drift")
    if evidence_manifest.get("run_manifest_hash") != _sha256(run_root / RUN_MANIFEST_NAME):
        raise CarverBlocked("S27 v2 incremental evidence manifest run hash drift")
    for ledger_name, expected_hash in dict(evidence_manifest.get("ledger_hashes", {})).items():
        if _sha256(run_root / ledger_name) != expected_hash:
            raise CarverBlocked(f"S27 v2 incremental source ledger hash drift: {ledger_name}")


def _immutable_file_refs(pack_root: Path, run_root: Path) -> tuple[ImmutableFileRef, ...]:
    paths = [
        pack_root / INPUT_MANIFEST_NAME,
        pack_root / INPUT_SHA256SUMS_NAME,
        run_root / RUN_MANIFEST_NAME,
        run_root / EVIDENCE_MANIFEST_NAME,
        _REPO_ROOT / DEFAULT_COMBINED_TBBO_RELATIVE_PATH / COMBINED_TBBO_REGISTRY_NAME,
        _REPO_ROOT / DEFAULT_COMBINED_TBBO_RELATIVE_PATH / COMBINED_TBBO_MANIFEST_NAME,
    ]
    refs: list[ImmutableFileRef] = []
    for path in paths:
        artifact_hash = _sha256(path)
        refs.append(
            ImmutableFileRef(
                relative_path=str(path.resolve().relative_to(_REPO_ROOT)),
                sha256=artifact_hash,
                size_bytes=path.stat().st_size,
            )
        )
    return tuple(refs)


def _checkpoint_payload(checkpoint: IncrementalCheckpoint) -> dict[str, Any]:
    data = asdict(checkpoint)
    data.pop("trusted_checkpoint_hash", None)
    return data


def _checkpoint_public_payload(checkpoint: IncrementalCheckpoint) -> dict[str, Any]:
    checkpoint.validate()
    return asdict(checkpoint)


def _segment_manifest_payload(bundle: IncrementalSegmentBundle) -> dict[str, Any]:
    return {
        "status": bundle.status,
        "authorization_label": bundle.authorization_label,
        "validation_mode": bundle.validation_mode,
        "source_mode": bundle.source_mode,
        "baseline_checkpoint_hash": bundle.baseline_checkpoint.trusted_checkpoint_hash,
        "segment_start_row_index": bundle.segment_start_row_index,
        "segment_end_row_index": bundle.segment_end_row_index,
        "terminal_fail_row_index": bundle.terminal_fail_row_index,
        "terminal_fail_reason": bundle.terminal_fail_reason,
        "terminal_fail_row_hash": bundle.terminal_fail_row_hash,
        "ledger_row_counts": dict(bundle.ledger_row_counts),
        "segment_ledger_hashes": dict(bundle.segment_ledger_hashes),
        "immutable_file_refs": tuple(bundle.immutable_file_refs),
        "parity_rows_verified": bundle.parity_rows_verified,
        "non_authorizations": bundle.non_authorizations,
    }


def _segment_bundle_payload(bundle: IncrementalSegmentBundle) -> dict[str, Any]:
    data = asdict(bundle)
    data.pop("bundle_hash", None)
    return data


def _tbbo_plan_payload(plan: MissingTBBOBatchPlan) -> dict[str, Any]:
    data = asdict(plan)
    data.pop("plan_hash", None)
    return data


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CarverBlocked(f"Missing JSON artifact: {path}")
    return json.loads(path.read_text(encoding="ascii"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="ascii")


def _write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="ascii")
        return
    with path.open("w", encoding="ascii", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _segment_csv_name(ledger_name: str) -> str:
    stem = ledger_name.removesuffix(".csv")
    return f"{stem}_segment.csv"


def _jsonable(payload: Any) -> Any:
    if hasattr(payload, "__dataclass_fields__"):
        return _jsonable(asdict(payload))
    if isinstance(payload, dict):
        return {str(key): _jsonable(value) for key, value in payload.items()}
    if isinstance(payload, tuple):
        return [_jsonable(value) for value in payload]
    if isinstance(payload, list):
        return [_jsonable(value) for value in payload]
    return payload


def _sha256(path: Path) -> str:
    if not path.exists():
        raise CarverBlocked(f"Missing hash-bound artifact: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()

from __future__ import annotations

import hashlib
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .development_recon_run import (
    ANNUAL_TARGET_RISK,
    CAPITAL_ACCOUNT_VALUE,
    CONTRACT_POINT_VALUE,
    FORECAST_CAP_VALUE,
    FORECAST_SCALAR_VALUE,
    FORECAST_TO_POSITION_DIVISOR,
)
from .local_replay import canonical_sha256
from .replay_artifact_cache import Sha256ArtifactCache
from .test_incremental_runner import (
    AUTHORIZATION,
    DEFAULT_OUTPUT_RELATIVE_PATH,
    DEFAULT_PACK_RELATIVE_PATH,
    NON_AUTHORIZATIONS,
)


STATUS = "LOCAL_2023_TEST_FAST_PRIMITIVE_ROW_ENGINE_BUILT_NOT_RESULT"
PARITY_STATUS = "LOCAL_2023_TEST_FAST_PRIMITIVE_ROW_ENGINE_PARITY_VERIFIED_NOT_RESULT"
PRIMITIVE_ENGINE_STAGE = "FAST_DECLARED_PACK_RUNTIME_FORECAST_DESIRED_PRIMITIVES_NOT_EXECUTION"
DEFAULT_PARITY_ROWS = (1, 2, 303, 304, 547, 1374)

PACK_MANIFEST_NAME = "S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST.json"
RUNTIME_LEDGER_NAME = "runtime_evidence_ledger.csv"
DECISION_LEDGER_NAME = "hourly_decision_completed_bar.csv"

_REPO_ROOT = Path(__file__).resolve().parents[4]


@dataclass(frozen=True)
class FastPrimitiveEngineBundle:
    status: str
    authorization_label: str
    engine_stage: str
    input_pack_path: str
    input_manifest_hash: str
    row_count: int
    runtime_rows_hash: str
    forecast_rows_hash: str
    desired_absolute_rows_hash: str
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 fast primitive engine status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast primitive engine authorization mismatch")
        if self.engine_stage != PRIMITIVE_ENGINE_STAGE:
            raise CarverBlocked("S27 v2 fast primitive engine stage drift")
        pack_root = Path(self.input_pack_path).resolve()
        if pack_root != (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve():
            raise CarverBlocked("S27 v2 fast primitive engine input pack is locked")
        if self.input_manifest_hash != _sha256(pack_root / PACK_MANIFEST_NAME):
            raise CarverBlocked("S27 v2 fast primitive engine manifest hash drift")
        if self.row_count != 1378:
            raise CarverBlocked("S27 v2 fast primitive engine row count drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast primitive engine non-authorizations drift")
        if self.bundle_hash != canonical_sha256(_primitive_bundle_payload(self)):
            raise CarverBlocked("S27 v2 fast primitive engine bundle hash drift")


@dataclass(frozen=True)
class FastPrimitiveParityReport:
    status: str
    authorization_label: str
    primitive_engine_bundle_hash: str
    parity_row_indexes: tuple[int, ...]
    runtime_parity_hash: str
    forecast_parity_hash: str
    desired_absolute_parity_hash: str
    report_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self, bundle: FastPrimitiveEngineBundle) -> None:
        if self.status != PARITY_STATUS:
            raise CarverBlocked("S27 v2 fast primitive parity status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast primitive parity authorization mismatch")
        if self.primitive_engine_bundle_hash != bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast primitive parity bundle binding drift")
        if self.parity_row_indexes != DEFAULT_PARITY_ROWS:
            raise CarverBlocked("S27 v2 fast primitive parity rows are locked")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast primitive parity non-authorizations drift")
        if self.report_hash != canonical_sha256(_parity_report_payload(self)):
            raise CarverBlocked("S27 v2 fast primitive parity report hash drift")


@dataclass(frozen=True)
class FastPrimitiveRows:
    runtime_rows: tuple[dict[str, Any], ...]
    forecast_rows: tuple[dict[str, Any], ...]
    desired_absolute_rows: tuple[dict[str, Any], ...]


def build_fast_primitive_engine(
    *,
    pack_root: Path | str | None = None,
    cache: Sha256ArtifactCache | None = None,
) -> tuple[FastPrimitiveEngineBundle, FastPrimitiveRows]:
    pack_root_path = Path(pack_root).resolve() if pack_root is not None else (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()
    if pack_root_path != (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 fast primitive engine input pack is locked")
    active_cache = cache or Sha256ArtifactCache()
    manifest = active_cache.read_json(pack_root_path / PACK_MANIFEST_NAME)
    _verify_manifest_hashes(pack_root_path, manifest)
    runtime_source = active_cache.read_csv_rows(pack_root_path / RUNTIME_LEDGER_NAME)
    decision_source = active_cache.read_csv_rows(pack_root_path / DECISION_LEDGER_NAME)
    if len(runtime_source) != len(decision_source):
        raise CarverBlocked("S27 v2 fast primitive engine runtime/decision row count mismatch")

    runtime_rows: list[dict[str, Any]] = []
    forecast_rows: list[dict[str, Any]] = []
    desired_rows: list[dict[str, Any]] = []
    for runtime, decision in zip(runtime_source, decision_source, strict=True):
        row_index = int(runtime["row_index"])
        if row_index != int(decision["row_index"]):
            raise CarverBlocked("S27 v2 fast primitive engine row index mismatch")
        runtime_row, forecast_row, desired_row = _compute_primitive_rows(row_index, runtime, decision)
        runtime_rows.append(runtime_row)
        forecast_rows.append(forecast_row)
        desired_rows.append(desired_row)

    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "engine_stage": PRIMITIVE_ENGINE_STAGE,
        "input_pack_path": str(pack_root_path),
        "input_manifest_hash": _sha256(pack_root_path / PACK_MANIFEST_NAME),
        "row_count": len(runtime_rows),
        "runtime_rows_hash": canonical_sha256(runtime_rows),
        "forecast_rows_hash": canonical_sha256(forecast_rows),
        "desired_absolute_rows_hash": canonical_sha256(desired_rows),
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    bundle = FastPrimitiveEngineBundle(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        engine_stage=PRIMITIVE_ENGINE_STAGE,
        input_pack_path=str(pack_root_path),
        input_manifest_hash=str(payload["input_manifest_hash"]),
        row_count=len(runtime_rows),
        runtime_rows_hash=str(payload["runtime_rows_hash"]),
        forecast_rows_hash=str(payload["forecast_rows_hash"]),
        desired_absolute_rows_hash=str(payload["desired_absolute_rows_hash"]),
        bundle_hash=canonical_sha256(payload),
    )
    rows = FastPrimitiveRows(
        runtime_rows=tuple(runtime_rows),
        forecast_rows=tuple(forecast_rows),
        desired_absolute_rows=tuple(desired_rows),
    )
    bundle.validate()
    return bundle, rows


def validate_fast_primitive_parity(
    bundle: FastPrimitiveEngineBundle,
    rows: FastPrimitiveRows,
    *,
    run_root: Path | str | None = None,
    parity_row_indexes: tuple[int, ...] = DEFAULT_PARITY_ROWS,
) -> FastPrimitiveParityReport:
    bundle.validate()
    run_root_path = Path(run_root).resolve() if run_root is not None else (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve()
    if run_root_path != (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 fast primitive parity run root is locked")
    if parity_row_indexes != DEFAULT_PARITY_ROWS:
        raise CarverBlocked("S27 v2 fast primitive parity rows are locked")
    if canonical_sha256(rows.runtime_rows) != bundle.runtime_rows_hash:
        raise CarverBlocked("S27 v2 fast primitive runtime rows do not match bundle hash")
    if canonical_sha256(rows.forecast_rows) != bundle.forecast_rows_hash:
        raise CarverBlocked("S27 v2 fast primitive forecast rows do not match bundle hash")
    if canonical_sha256(rows.desired_absolute_rows) != bundle.desired_absolute_rows_hash:
        raise CarverBlocked("S27 v2 fast primitive desired rows do not match bundle hash")
    cache = Sha256ArtifactCache()
    _verify_run_ledger_hashes(
        run_root_path,
        (
            "runtime_history_ledger.csv",
            "forecast_replay_ledger.csv",
            "desired_position_ledger.csv",
        ),
        cache,
    )
    runtime_ledger = _index_rows(cache.read_csv_rows(run_root_path / "runtime_history_ledger.csv"))
    forecast_ledger = _index_rows(cache.read_csv_rows(run_root_path / "forecast_replay_ledger.csv"))
    desired_ledger = _index_rows(cache.read_csv_rows(run_root_path / "desired_position_ledger.csv"))
    runtime_rows = _index_rows(rows.runtime_rows)
    forecast_rows = _index_rows(rows.forecast_rows)
    desired_rows = _index_rows(rows.desired_absolute_rows)

    runtime_parity: list[dict[str, Any]] = []
    forecast_parity: list[dict[str, Any]] = []
    desired_parity: list[dict[str, Any]] = []
    for index in parity_row_indexes:
        runtime_expected = runtime_ledger[index]
        runtime_actual = runtime_rows[index]
        if runtime_expected["row_hash"] != runtime_actual["row_hash"]:
            raise CarverBlocked(f"S27 v2 fast primitive runtime parity drift at row {index}")
        forecast_expected = forecast_ledger[index]
        forecast_actual = forecast_rows[index]
        if forecast_expected["row_hash"] != forecast_actual["row_hash"]:
            raise CarverBlocked(f"S27 v2 fast primitive forecast parity drift at row {index}")
        desired_expected = desired_ledger[index]
        desired_actual = desired_rows[index]
        _validate_row_hash(desired_actual, f"desired primitive row {index}")
        if desired_actual["decision_timestamp_utc"] != forecast_expected["decision_timestamp_utc"]:
            raise CarverBlocked(f"S27 v2 fast primitive desired timestamp parity drift at row {index}")
        if not math.isclose(
            float(desired_actual["capped_forecast"]),
            float(forecast_expected["capped_forecast"]),
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise CarverBlocked(f"S27 v2 fast primitive desired capped forecast parity drift at row {index}")
        if int(desired_expected["desired_position_contracts"]) != int(desired_actual["desired_position_contracts"]):
            raise CarverBlocked(f"S27 v2 fast primitive desired-position parity drift at row {index}")
        if not math.isclose(
            float(desired_expected["base_position_contracts"]),
            float(desired_actual["base_position_contracts"]),
            rel_tol=0.0,
            abs_tol=1e-9,
        ):
            raise CarverBlocked(f"S27 v2 fast primitive base-position parity drift at row {index}")
        runtime_parity.append({"row_index": index, "row_hash": runtime_actual["row_hash"]})
        forecast_parity.append({"row_index": index, "row_hash": forecast_actual["row_hash"]})
        desired_parity.append(
            {
                "row_index": index,
                "decision_timestamp_utc": desired_actual["decision_timestamp_utc"],
                "desired_position_contracts": desired_actual["desired_position_contracts"],
                "base_position_contracts": desired_actual["base_position_contracts"],
                "capped_forecast": desired_actual["capped_forecast"],
                "row_status": desired_actual["row_status"],
                "row_hash": desired_actual["row_hash"],
            }
        )

    payload = {
        "status": PARITY_STATUS,
        "authorization_label": AUTHORIZATION,
        "primitive_engine_bundle_hash": bundle.bundle_hash,
        "parity_row_indexes": parity_row_indexes,
        "runtime_parity_hash": canonical_sha256(runtime_parity),
        "forecast_parity_hash": canonical_sha256(forecast_parity),
        "desired_absolute_parity_hash": canonical_sha256(desired_parity),
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    report = FastPrimitiveParityReport(
        status=PARITY_STATUS,
        authorization_label=AUTHORIZATION,
        primitive_engine_bundle_hash=bundle.bundle_hash,
        parity_row_indexes=parity_row_indexes,
        runtime_parity_hash=str(payload["runtime_parity_hash"]),
        forecast_parity_hash=str(payload["forecast_parity_hash"]),
        desired_absolute_parity_hash=str(payload["desired_absolute_parity_hash"]),
        report_hash=canonical_sha256(payload),
    )
    report.validate(bundle)
    return report


def _compute_primitive_rows(
    row_index: int,
    runtime: Mapping[str, str],
    decision: Mapping[str, str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    decision_price = float(decision["close_price"])
    ewma5 = float(runtime["ewma5_equilibrium"])
    trend = float(runtime["ewmac16_64_trend"])
    sigma = float(runtime["annual_percentage_sigma"])
    multiplier = float(runtime["vol_multiplier_m"])
    sigma_price = float(runtime["previous_daily_raw_close"]) * sigma / 16.0
    raw_forecast = ewma5 - decision_price
    risk_before_veto = raw_forecast / sigma_price
    risk_after_veto = 0.0 if risk_before_veto * trend < 0.0 else risk_before_veto
    capped_forecast = _clamp(risk_after_veto * multiplier * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)
    base_position = CAPITAL_ACCOUNT_VALUE * ANNUAL_TARGET_RISK / (decision_price * CONTRACT_POINT_VALUE * sigma)
    desired_position = _round_half_away_from_zero(base_position * capped_forecast / FORECAST_TO_POSITION_DIVISOR)

    runtime_row = _hash_row(
        {
            "row_index": row_index,
            "runtime_evidence_row_hash": runtime["row_hash"],
            "ewma5": ewma5,
            "trend": trend,
            "sigma": sigma,
            "vqm_multiplier_m": multiplier,
            "row_status": "LOCAL_RUNTIME_NUMERIC_ROW_EMITTED_NOT_RESULT",
        }
    )
    forecast_row = _hash_row(
        {
            "row_index": row_index,
            "decision_timestamp_utc": decision["completed_timestamp_utc"],
            "raw_forecast": raw_forecast,
            "risk_adjusted_forecast": risk_after_veto,
            "capped_forecast": capped_forecast,
            "row_status": "LOCAL_FORECAST_ROW_EMITTED_NOT_RESULT",
        }
    )
    desired_row = _hash_row(
        {
            "row_index": row_index,
            "decision_timestamp_utc": decision["completed_timestamp_utc"],
            "desired_position_contracts": desired_position,
            "base_position_contracts": base_position,
            "capped_forecast": capped_forecast,
            "row_status": "LOCAL_FAST_DESIRED_ABSOLUTE_PRIMITIVE_ROW_EMITTED_NOT_RESULT_NOT_EXECUTION_STATE",
        }
    )
    return runtime_row, forecast_row, desired_row


def _verify_manifest_hashes(pack_root: Path, manifest: Mapping[str, Any]) -> None:
    row_family = manifest.get("row_family_files", {})
    for name in (RUNTIME_LEDGER_NAME, DECISION_LEDGER_NAME):
        expected = row_family.get(name, {}).get("sha256")
        if expected != _sha256(pack_root / name):
            raise CarverBlocked(f"S27 v2 fast primitive engine pack hash drift for {name}")


def _verify_run_ledger_hashes(
    run_root: Path,
    ledger_names: tuple[str, ...],
    cache: Sha256ArtifactCache,
) -> None:
    evidence = cache.read_json(run_root / "evidence_manifest.json")
    ledger_hashes = dict(evidence.get("ledger_hashes", {}))
    for name in ledger_names:
        if ledger_hashes.get(name) != _sha256(run_root / name):
            raise CarverBlocked(f"S27 v2 fast primitive parity ledger hash drift for {name}")


def _validate_row_hash(row: Mapping[str, Any], label: str) -> None:
    payload = dict(row)
    row_hash = payload.pop("row_hash", None)
    if row_hash != canonical_sha256(payload):
        raise CarverBlocked(f"S27 v2 fast primitive {label} hash drift")


def _index_rows(rows: tuple[dict[str, Any], ...] | list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    return {int(row["row_index"]): row for row in rows}


def _hash_row(row: dict[str, Any]) -> dict[str, Any]:
    hashed = dict(row)
    hashed["row_hash"] = canonical_sha256(hashed)
    return hashed


def _primitive_bundle_payload(bundle: FastPrimitiveEngineBundle) -> dict[str, Any]:
    payload = asdict(bundle)
    payload.pop("bundle_hash", None)
    return payload


def _parity_report_payload(report: FastPrimitiveParityReport) -> dict[str, Any]:
    payload = asdict(report)
    payload.pop("report_hash", None)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _round_half_away_from_zero(value: float) -> int:
    return math.floor(value + 0.5) if value >= 0.0 else math.ceil(value - 0.5)


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))

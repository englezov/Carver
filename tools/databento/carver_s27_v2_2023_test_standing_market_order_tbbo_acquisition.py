from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
TOOLS = ROOT / "tools/databento"
for path in (SRC, TOOLS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from carver.spine.m0 import CarverBlocked  # noqa: E402
from carver.spine.s27_v2_replay.local_replay import canonical_sha256  # noqa: E402
from carver_s27_v2_2023_test_market_order_tbbo_batch_acquisition import (  # noqa: E402
    DATASET,
    PROVIDER,
    REQUIREMENTS_LEDGER,
    SCHEMA,
    STYPE_IN,
    _normalise_tbbo_rows,
    _provider_condition_row,
    _parse_z,
    _read_databento_key,
    _rel,
    _select_latest_non_crossed_quote_at_or_before_fill,
    _selected_spread_row,
    _sha256,
    _write_csv,
    _write_json,
    _write_sha256_manifest,
)


RUN_ID = "20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_BATCH"
AUTHORIZATION = "S27_V2_STANDING_BOUNDED_MARKET_ORDER_TBBO_SPREAD_EVIDENCE_POLICY"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260613_2023_test_standing_market_order_tbbo_batch_evidence"
)
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_BATCH_EVIDENCE_2026-06-13.md"
)


@dataclass(frozen=True)
class StandingTBBOConfig:
    execution_authorized: bool
    requirements_ledger: Path = REQUIREMENTS_LEDGER
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = run_standing_tbbo_acquisition(StandingTBBOConfig(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")
    print(f"failed_rows={status['failed_row_count']}")


def run_standing_tbbo_acquisition(config: StandingTBBOConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    requirements = _missing_requirements(config.requirements_ledger)
    client = db.Historical(_read_databento_key())

    _write_json(config.output_root / "manifest" / f"{RUN_ID}_request_manifest.json", _request_manifest(requirements))

    selected_rows: list[dict[str, Any]] = []
    provider_condition_rows: list[dict[str, Any]] = []
    raw_output_rows: list[dict[str, Any]] = []

    for requirement in requirements:
        row_index = requirement["row_index"]
        raw_dbn = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{row_index}.dbn"
        raw_csv = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{row_index}_tbbo_dataframe.csv"
        provider_errors: list[dict[str, str]] = []
        quote_rows: list[dict[str, Any]] = []
        selected_row: dict[str, Any] | None = None
        try:
            if raw_dbn.exists() or raw_csv.exists():
                raise CarverBlocked(f"Standing TBBO raw outputs already exist for row {row_index}; refusing duplicate provider request")
            store = client.timeseries.get_range(
                dataset=DATASET,
                schema=SCHEMA,
                symbols=[requirement["raw_symbol"]],
                stype_in=STYPE_IN,
                start=requirement["request_start_utc"],
                end=requirement["request_end_utc"],
                path=raw_dbn,
            )
            if not raw_dbn.exists() or raw_dbn.stat().st_size <= 0:
                raise RuntimeError(f"Databento returned no raw TBBO DBN bytes for row {row_index}")
            df = store.to_df()
            df.to_csv(raw_csv)
            quote_rows = _normalise_tbbo_rows(df, requirement)
            selected_row = _select_latest_non_crossed_quote_at_or_before_fill(quote_rows, requirement)
        except Exception as exc:  # noqa: BLE001 - failures must be ledgered and fail closed per-row.
            provider_errors.append({"error_type": type(exc).__name__, "message": str(exc)})
        provider_condition_rows.append(_provider_condition_row(requirement, quote_rows, selected_row, provider_errors))
        selected_rows.append(_selected_spread_row(requirement, selected_row, raw_dbn, raw_csv, provider_errors))
        raw_output_rows.append(
            {
                "row_index": row_index,
                "raw_dbn_relative_path": _rel(raw_dbn),
                "raw_dbn_sha256": _sha256(raw_dbn) if raw_dbn.exists() else "MISSING_RAW_DBN",
                "raw_csv_relative_path": _rel(raw_csv),
                "raw_csv_sha256": _sha256(raw_csv) if raw_csv.exists() else "MISSING_RAW_CSV",
            }
        )

    selected_path = config.output_root / "ledger" / f"{RUN_ID}_selected_spread_registry.csv"
    provider_path = config.output_root / "provider_condition" / f"{RUN_ID}_provider_condition_ledger.csv"
    raw_path = config.output_root / "raw_provider_output" / f"{RUN_ID}_raw_output_registry.csv"
    status_path = config.output_root / "status" / f"{RUN_ID}_status.json"
    provenance_path = config.output_root / "provenance" / f"{RUN_ID}_provenance.md"
    sha_path = config.output_root / "hashes" / f"{RUN_ID}_sha256.csv"

    selected_rows = _merge_existing_rows_by_index(selected_path, selected_rows)
    provider_condition_rows = _merge_existing_rows_by_index(provider_path, provider_condition_rows)
    raw_output_rows = _merge_existing_rows_by_index(raw_path, raw_output_rows)

    _write_csv(selected_path, selected_rows)
    _write_csv(provider_path, provider_condition_rows)
    _write_csv(raw_path, raw_output_rows)
    _write_json(config.output_root / "manifest" / f"{RUN_ID}_request_manifest.json", _request_manifest(requirements, selected_rows))
    status = _status_payload(requirements, selected_rows, provider_condition_rows)
    _write_json(status_path, status)
    provenance_path.write_text(_provenance_text(status), encoding="ascii")
    PROCESS_RECORD.write_text(_process_record(status), encoding="ascii")
    _write_sha256_manifest(sha_path, config.output_root)
    if status["status"] != "PASS_STANDING_BOUNDED_DATABENTO_TBBO_BATCH_SELECTED_NOT_RESULT":
        raise CarverBlocked("S27 v2 TEST standing TBBO batch evidence failed closed; see standing status ledger")
    return status


def _validate_config(config: StandingTBBOConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST standing TBBO acquisition is not authorized")
    if config.requirements_ledger.resolve() != REQUIREMENTS_LEDGER.resolve():
        raise CarverBlocked("S27 v2 TEST standing TBBO acquisition must use the locked requirements ledger")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST standing TBBO acquisition output root is locked")


def _missing_requirements(path: Path) -> list[dict[str, str]]:
    rows = _read_csv(path)
    missing = [row for row in rows if row["tbbo_requirement_status"] == "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"]
    if not missing:
        raise CarverBlocked("S27 v2 TEST standing TBBO acquisition found no missing requirements")
    for row in missing:
        if not _is_zn_quarterly_raw_symbol(row["raw_symbol"]):
            raise CarverBlocked("S27 v2 TEST standing TBBO requirement raw-symbol drift")
        if row["provider"] != PROVIDER or row["dataset"] != DATASET or row["schema"] != SCHEMA:
            raise CarverBlocked("S27 v2 TEST standing TBBO requirement provider/schema drift")
        if not row["decision_timestamp_utc"].startswith("2023-") or not row["fill_candidate_timestamp_utc"].startswith("2023-"):
            raise CarverBlocked("S27 v2 TEST standing TBBO requirements must stay in 2023")
        if row["source_faithful_evidence_claimed"] != "FALSE" or row["result_interpretation_authorized"] != "FALSE":
            raise CarverBlocked("S27 v2 TEST standing TBBO requirements must not claim result/source-faithful authority")
        _validate_request_window(row)
        if row["row_hash"] != canonical_sha256({key: value for key, value in row.items() if key != "row_hash"}):
            raise CarverBlocked("S27 v2 TEST standing TBBO requirement row hash drift")
    return missing


def _is_zn_quarterly_raw_symbol(raw_symbol: str) -> bool:
    return (
        len(raw_symbol) == 4
        and raw_symbol.startswith("ZN")
        and raw_symbol[2] in {"H", "M", "U", "Z"}
        and raw_symbol[3].isdigit()
    )


def _validate_request_window(row: dict[str, str]) -> None:
    fill_time = _parse_z(row["fill_candidate_timestamp_utc"])
    expected_start = _format_z(fill_time - timedelta(seconds=5))
    expected_end = _format_z(fill_time + timedelta(seconds=5))
    if row["request_start_utc"] != expected_start or row["request_end_utc"] != expected_end:
        raise CarverBlocked("S27 v2 TEST standing TBBO request window must equal fill timestamp +/- 5 seconds")


def _merge_existing_rows_by_index(path: Path, new_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[int, dict[str, Any]] = {}
    if path.exists():
        for row in _read_csv(path):
            merged[int(row["row_index"])] = row
    for row in new_rows:
        merged[int(row["row_index"])] = row
    return [merged[index] for index in sorted(merged)]


def _request_manifest(requirements: list[dict[str, str]], registry_rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    registry_rows = registry_rows or []
    return {
        "authorization": AUTHORIZATION,
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "requirements_ledger": _rel(REQUIREMENTS_LEDGER),
        "requirements_ledger_sha256": _sha256(REQUIREMENTS_LEDGER),
        "current_request_count": len(requirements),
        "current_request_row_indices": [row["row_index"] for row in requirements],
        "aggregate_registry_row_count": len(registry_rows),
        "aggregate_registry_row_indices": [row["row_index"] for row in registry_rows],
        "first_request_start_utc": requirements[0]["request_start_utc"],
        "last_request_end_utc": requirements[-1]["request_end_utc"],
        "scope": "STANDING_POLICY_BOUNDED_2023_TEST_MARKET_ORDER_TBBO_REQUIREMENTS_ONLY",
        "broader_provider_api_access": "NO",
        "general_historical_download": "NO",
        "validation_oos_lockbox_forward_access": "NO",
        "pnl_result_emission": "NO",
        "source_faithful_evidence_claim": "NO",
    }


def _status_payload(
    requirements: list[dict[str, str]],
    selected_rows: list[dict[str, Any]],
    provider_condition_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    failed = [row for row in selected_rows if not str(row["selection_status"]).startswith("PASS_")]
    return {
        "authorization": AUTHORIZATION,
        "status": (
            "PASS_STANDING_BOUNDED_DATABENTO_TBBO_BATCH_SELECTED_NOT_RESULT"
            if not failed
            else "FAIL_CLOSED_STANDING_BOUNDED_DATABENTO_TBBO_BATCH_INCOMPLETE_NOT_RESULT"
        ),
        "current_request_count": len(requirements),
        "current_request_row_indices": [row["row_index"] for row in requirements],
        "aggregate_registry_row_count": len(selected_rows),
        "selected_row_count": len(selected_rows) - len(failed),
        "failed_row_count": len(failed),
        "failed_row_indices": [row["row_index"] for row in failed],
        "provider_condition_pass_count": sum(
            1 for row in provider_condition_rows if row["provider_condition_status"] == "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED"
        ),
        "provider_api_access": "STANDING_POLICY_BOUNDED_DATABENTO_TBBO_ONLY",
        "downloads": "BOUNDED_LISTED_TBBO_WINDOWS_ONLY",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Standing Market-Order TBBO Batch Evidence Provenance

Status:

```text
{status['status']}
```

Current request rows: {status['current_request_count']}
Aggregate registry rows: {status['aggregate_registry_row_count']}
Selected rows: {status['selected_row_count']}
Failed rows: {status['failed_row_count']}

Provider access was limited to listed 2023 TEST market-order TBBO quote windows from the active requirements ledger. This is not broad provider access, not a general historical download, not result evidence, and not source-faithful evidence.
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# S27 V2 ZN 2023 TEST Standing Market-Order TBBO Batch Evidence

Date: 2026-06-13

Status:

```text
{status['status']}
```

This record is written under `S27_V2_STANDING_BOUNDED_MARKET_ORDER_TBBO_SPREAD_EVIDENCE_POLICY`.

Current request count: `{status['current_request_count']}`
Aggregate registry row count: `{status['aggregate_registry_row_count']}`
Selected row count: `{status['selected_row_count']}`
Failed row count: `{status['failed_row_count']}`
Failed row indices: `{','.join(status['failed_row_indices']) if status['failed_row_indices'] else 'NONE'}`

The provider request was bounded to rows listed in the active `market_order_tbbo_requirements.csv` ledger. This record does not authorize broad provider/API access, general downloads, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
"""


def _ensure_output_dirs(root: Path) -> None:
    for folder in ("raw_provider_output", "manifest", "provider_condition", "ledger", "status", "provenance", "hashes"):
        (root / folder).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _format_z(value: Any) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    main()

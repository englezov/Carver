from __future__ import annotations

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
    SCHEMA,
    STYPE_IN,
    _normalise_tbbo_rows,
    _parse_z,
    _provider_condition_row,
    _read_csv,
    _read_databento_key,
    _rel,
    _select_latest_non_crossed_quote_at_or_before_fill,
    _selected_spread_row,
    _sha256,
    _write_csv,
    _write_json,
    _write_sha256_manifest,
)


RUN_ID = "20260616_S27_V2_2023_TEST_ROW1356_MARKET_ORDER_TBBO"
AUTHORIZATION = "S27_V2_2023_TEST_ROW1356_BOUNDED_MARKET_ORDER_TBBO_EVIDENCE_AND_CONTINUATION_GATE"
ROW_INDEX = "1356"
RAW_SYMBOL = "ZNM3"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260616_2023_test_row1356_market_order_tbbo"
)
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW1356_MARKET_ORDER_TBBO_EVIDENCE_2026-06-16.md"
)
RUN_FAIL_CLOSED_LEDGER = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_runs/ZN/"
    / "20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv"
)


@dataclass(frozen=True)
class Row1356TBBOConfig:
    execution_authorized: bool
    fail_closed_ledger: Path = RUN_FAIL_CLOSED_LEDGER
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = run_row1356_tbbo_acquisition(Row1356TBBOConfig(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")
    print(f"failed_rows={status['failed_row_count']}")


def run_row1356_tbbo_acquisition(config: Row1356TBBOConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    requirement = _row1356_requirement(config.fail_closed_ledger)
    client = db.Historical(_read_databento_key())

    _write_json(config.output_root / "manifest" / f"{RUN_ID}_request_manifest.json", _request_manifest(requirement))

    raw_dbn = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{ROW_INDEX}.dbn"
    raw_csv = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{ROW_INDEX}_tbbo_dataframe.csv"
    provider_errors: list[dict[str, str]] = []
    quote_rows: list[dict[str, Any]] = []
    selected_row: dict[str, Any] | None = None

    try:
        if raw_dbn.exists() or raw_csv.exists():
            raise CarverBlocked("Row 1356 TBBO raw outputs already exist; refusing duplicate provider request")
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
            raise RuntimeError("Databento returned no row 1356 raw TBBO DBN bytes")
        df = store.to_df()
        df.to_csv(raw_csv)
        quote_rows = _normalise_tbbo_rows(df, requirement)
        selected_row = _select_latest_non_crossed_quote_at_or_before_fill(quote_rows, requirement)
    except Exception as exc:  # noqa: BLE001 - row evidence must ledger failures and fail closed.
        provider_errors.append({"error_type": type(exc).__name__, "message": str(exc)})

    selected_rows = [_selected_spread_row(requirement, selected_row, raw_dbn, raw_csv, provider_errors)]
    provider_condition_rows = [_provider_condition_row(requirement, quote_rows, selected_row, provider_errors)]
    raw_output_rows = [
        {
            "row_index": ROW_INDEX,
            "raw_dbn_relative_path": _rel(raw_dbn),
            "raw_dbn_sha256": _sha256(raw_dbn) if raw_dbn.exists() else "MISSING_RAW_DBN",
            "raw_csv_relative_path": _rel(raw_csv),
            "raw_csv_sha256": _sha256(raw_csv) if raw_csv.exists() else "MISSING_RAW_CSV",
        }
    ]

    selected_path = config.output_root / "ledger" / f"{RUN_ID}_selected_spread_registry.csv"
    provider_path = config.output_root / "provider_condition" / f"{RUN_ID}_provider_condition_ledger.csv"
    raw_path = config.output_root / "raw_provider_output" / f"{RUN_ID}_raw_output_registry.csv"
    status_path = config.output_root / "status" / f"{RUN_ID}_status.json"
    provenance_path = config.output_root / "provenance" / f"{RUN_ID}_provenance.md"
    sha_path = config.output_root / "hashes" / f"{RUN_ID}_sha256.csv"

    _write_csv(selected_path, selected_rows)
    _write_csv(provider_path, provider_condition_rows)
    _write_csv(raw_path, raw_output_rows)
    status = _status_payload(selected_rows, provider_condition_rows)
    _write_json(status_path, status)
    provenance_path.write_text(_provenance_text(status), encoding="ascii")
    PROCESS_RECORD.write_text(_process_record(status), encoding="ascii")
    _write_sha256_manifest(sha_path, config.output_root)

    if status["status"] != "PASS_ROW1356_BOUNDED_DATABENTO_TBBO_SELECTED_NOT_RESULT":
        raise CarverBlocked("S27 v2 TEST row 1356 TBBO evidence failed closed; see status ledger")
    return status


def _validate_config(config: Row1356TBBOConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST row 1356 TBBO acquisition is not authorized")
    if config.fail_closed_ledger.resolve() != RUN_FAIL_CLOSED_LEDGER.resolve():
        raise CarverBlocked("S27 v2 TEST row 1356 TBBO acquisition must use the locked fail-closed ledger")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST row 1356 TBBO acquisition output root is locked")


def _row1356_requirement(path: Path) -> dict[str, str]:
    rows = [row for row in _read_csv(path) if row["row_index"] == ROW_INDEX]
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 TEST row 1356 fail-closed ledger must contain exactly one active blocker row")
    fail_row = rows[0]
    expected = {
        "decision_timestamp_utc": "2023-03-29T23:00:00Z",
        "raw_symbol": RAW_SYMBOL,
        "starting_position_contracts": "8",
        "desired_position_contracts": "6",
        "position_change_contracts": "-2",
        "order_side": "SELL",
        "fill_candidate_timestamp_utc": "2023-03-30T00:00:00Z",
        "market_order_required": "TRUE",
        "market_order_rows_emitted": "FALSE",
        "market_order_reason": "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT",
        "market_spread_cost_status": "FAIL_CLOSED_BOUNDED_TBBO_SPREAD_EVIDENCE_REQUIRED_FOR_MARKET_ORDER",
        "fail_closed_reason": "FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT",
        "result_status": "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED",
        "backtest_status": "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED",
        "source_faithful_evidence_claimed": "FALSE",
    }
    for key, value in expected.items():
        if fail_row.get(key) != value:
            raise CarverBlocked(f"S27 v2 TEST row 1356 active blocker drift: {key}")
    if fail_row["row_hash"] != canonical_sha256(_row1356_fail_closed_hash_payload(fail_row)):
        raise CarverBlocked("S27 v2 TEST row 1356 active blocker row hash drift")
    fill_time = _parse_z(fail_row["fill_candidate_timestamp_utc"])
    requirement = {
        "row_index": ROW_INDEX,
        "decision_timestamp_utc": fail_row["decision_timestamp_utc"],
        "fill_candidate_timestamp_utc": fail_row["fill_candidate_timestamp_utc"],
        "raw_symbol": fail_row["raw_symbol"],
        "order_side": fail_row["order_side"],
        "order_quantity": str(abs(int(fail_row["position_change_contracts"]))),
        "market_order_reason": fail_row["market_order_reason"],
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "request_start_utc": _format_z(fill_time - timedelta(seconds=5)),
        "request_end_utc": _format_z(fill_time + timedelta(seconds=5)),
        "result_interpretation_authorized": "FALSE",
        "source_faithful_evidence_claimed": "FALSE",
    }
    requirement["row_hash"] = canonical_sha256(requirement)
    return requirement


def _row1356_fail_closed_hash_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "row_index": int(row["row_index"]),
        "decision_timestamp_utc": row["decision_timestamp_utc"],
        "raw_symbol": row["raw_symbol"],
        "starting_position_contracts": int(row["starting_position_contracts"]),
        "desired_position_contracts": int(row["desired_position_contracts"]),
        "position_change_contracts": int(row["position_change_contracts"]),
        "order_side": row["order_side"],
        "adjacent_target_position": int(row["adjacent_target_position"]),
        "trend": float(row["trend"]),
        "market_order_required": True,
        "market_order_rows_emitted": False,
        "market_order_reason": row["market_order_reason"],
        "market_fill_metadata_rows_emitted": False,
        "market_fill_price_provenance": row["market_fill_price_provenance"],
        "market_fill_price": float(row["market_fill_price"]),
        "commission_per_contract": float(row["commission_per_contract"]),
        "commission_amount": float(row["commission_amount"]),
        "market_spread_cost_status": row["market_spread_cost_status"],
        "secondary_fail_closed_reason": row["secondary_fail_closed_reason"],
        "fill_candidate_timestamp_utc": row["fill_candidate_timestamp_utc"],
        "fill_candidate_close": float(row["fill_candidate_close"]),
        "fill_executed": False,
        "same_session": True,
        "fail_closed_reason": row["fail_closed_reason"],
        "result_status": row["result_status"],
        "backtest_status": row["backtest_status"],
        "source_faithful_evidence_claimed": False,
        "row_status": row["row_status"],
    }


def _format_z(value: Any) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def _request_manifest(requirement: dict[str, str]) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "standing_authorization": "S27_V2_STANDING_BOUNDED_MARKET_ORDER_TBBO_SPREAD_EVIDENCE_POLICY",
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "active_fail_closed_ledger": _rel(RUN_FAIL_CLOSED_LEDGER),
        "active_fail_closed_ledger_sha256": _sha256(RUN_FAIL_CLOSED_LEDGER),
        "row_index": ROW_INDEX,
        "raw_symbol": RAW_SYMBOL,
        "request_start_utc": requirement["request_start_utc"],
        "request_end_utc": requirement["request_end_utc"],
        "requirement_row_hash": requirement["row_hash"],
        "scope": "ROW1356_ONLY_BOUNDED_2023_TEST_MARKET_ORDER_TBBO_REQUIREMENT",
        "broader_provider_api_access": "NO",
        "general_historical_download": "NO",
        "validation_oos_lockbox_forward_access": "NO",
        "broader_test_continuation": "NO",
        "pnl_result_emission": "NO",
        "source_faithful_evidence_claim": "NO",
    }


def _status_payload(
    selected_rows: list[dict[str, Any]],
    provider_condition_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    failed = [row for row in selected_rows if not str(row["selection_status"]).startswith("PASS_")]
    selected = selected_rows[0]
    provider = provider_condition_rows[0]
    return {
        "authorization": AUTHORIZATION,
        "standing_authorization": "S27_V2_STANDING_BOUNDED_MARKET_ORDER_TBBO_SPREAD_EVIDENCE_POLICY",
        "status": (
            "PASS_ROW1356_BOUNDED_DATABENTO_TBBO_SELECTED_NOT_RESULT"
            if not failed
            else "FAIL_CLOSED_ROW1356_BOUNDED_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT"
        ),
        "selected_row_count": len(selected_rows) - len(failed),
        "failed_row_count": len(failed),
        "failed_row_indices": [row["row_index"] for row in failed],
        "row_index": ROW_INDEX,
        "selected_quote_ts_event": selected.get("selected_quote_ts_event", ""),
        "quote_age_seconds": selected.get("quote_age_seconds", ""),
        "bid_px_00": selected.get("bid_px_00", ""),
        "ask_px_00": selected.get("ask_px_00", ""),
        "selected_executable_market_fill_price": selected.get("selected_executable_market_fill_price", ""),
        "selection_status": selected.get("selection_status", ""),
        "provider_condition_status": provider.get("provider_condition_status", ""),
        "provider_api_access": "ROW1356_ONLY_BOUNDED_DATABENTO_TBBO",
        "downloads": "ROW1356_ONLY_BOUNDED_TBBO_WINDOW",
        "broader_test_continuation": "NO",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 1356 Market-Order TBBO Evidence Provenance

Status:

```text
{status['status']}
```

Row: {status['row_index']}
Selected rows: {status['selected_row_count']}
Failed rows: {status['failed_row_count']}

Provider access was limited to the row-1356 ZNM3 TBBO quote window from the active fail-closed TEST artifact. This is not broad provider access, not a general historical download, not result evidence, and not source-faithful evidence.
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# S27 V2 ZN 2023 TEST Row 1356 Market-Order TBBO Evidence

Date: 2026-06-16

Status:

```text
{status['status']}
```

This record is written under `S27_V2_2023_TEST_ROW1356_BOUNDED_MARKET_ORDER_TBBO_EVIDENCE_AND_CONTINUATION_GATE` and the standing bounded market-order TBBO spread evidence policy.

Row index: `{status['row_index']}`
Selected quote timestamp: `{status['selected_quote_ts_event']}`
Quote age seconds: `{status['quote_age_seconds']}`
Bid: `{status['bid_px_00']}`
Ask: `{status['ask_px_00']}`
Selected executable SELL market fill price: `{status['selected_executable_market_fill_price']}`
Provider condition: `{status['provider_condition_status']}`

This evidence gate does not authorize broader provider/API access, general downloads, broader TEST continuation beyond the next mechanical blocker, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
"""


def _ensure_output_dirs(root: Path) -> None:
    for folder in ("raw_provider_output", "manifest", "provider_condition", "ledger", "status", "provenance", "hashes"):
        (root / folder).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()

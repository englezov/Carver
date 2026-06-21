from __future__ import annotations

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
    POINT_VALUE_USD,
    PROVIDER,
    RAW_SYMBOL,
    REQUIREMENTS_LEDGER,
    SCHEMA,
    STYPE_IN,
    _csv_value,
    _normalise_tbbo_rows,
    _parse_z,
    _provider_condition_row,
    _read_csv,
    _read_databento_key,
    _rel,
    _selected_spread_row,
    _sha256,
    _write_csv,
    _write_json,
    _write_sha256_manifest,
)


RUN_ID = "20260614_S27_V2_2023_TEST_ROW441_MARKET_ORDER_TBBO_EXTENDED_LOOKBACK"
AUTHORIZATION = "S27_V2_2023_TEST_ROW441_EMPTY_TBBO_EXTENDED_BOUND_REQUEST"
ROW_INDEX = "441"
LOOKBACK_SECONDS = 300
LOOKAHEAD_SECONDS = 5
MAX_SELECTED_QUOTE_AGE_SECONDS = 300.0
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260614_2023_test_row441_market_order_tbbo_extended_lookback"
)
POLICY_RECORD = (
    ROOT / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW441_EMPTY_TBBO_POLICY_DECISION_2026-06-14.md"
)
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW441_MARKET_ORDER_TBBO_EXTENDED_LOOKBACK_EVIDENCE_2026-06-14.md"
)


@dataclass(frozen=True)
class Row441ExtendedTBBOConfig:
    execution_authorized: bool
    requirements_ledger: Path = REQUIREMENTS_LEDGER
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = run_row441_extended_tbbo_acquisition(Row441ExtendedTBBOConfig(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")
    print(f"failed_rows={status['failed_row_count']}")
    if status["failed_row_count"]:
        print("row_441_fail_closed=TRUE")


def run_row441_extended_tbbo_acquisition(config: Row441ExtendedTBBOConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    requirement = _row441_requirement(config.requirements_ledger)
    client = db.Historical(_read_databento_key())

    manifest_path = config.output_root / "manifest" / f"{RUN_ID}_request_manifest.json"
    _write_json(manifest_path, _request_manifest(requirement))

    raw_dbn = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{ROW_INDEX}.dbn"
    raw_csv = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{ROW_INDEX}_tbbo_dataframe.csv"
    provider_errors: list[dict[str, str]] = []
    quote_rows: list[dict[str, Any]] = []
    selected_row: dict[str, Any] | None = None

    try:
        if raw_dbn.exists() or raw_csv.exists():
            raise CarverBlocked("Row 441 extended TBBO raw outputs already exist; refusing duplicate provider request")
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
            raise RuntimeError("Databento returned no row 441 extended raw TBBO DBN bytes")
        df = store.to_df()
        df.to_csv(raw_csv)
        quote_rows = _normalise_tbbo_rows(df, requirement)
        selected_row = _select_latest_non_crossed_quote_at_or_before_fill(quote_rows, requirement)
    except Exception as exc:  # noqa: BLE001 - evidence failures must be ledgered and fail closed.
        provider_errors.append({"error_type": type(exc).__name__, "message": str(exc)})

    selected_rows = [_selected_spread_row(requirement, selected_row, raw_dbn, raw_csv, provider_errors)]
    if selected_row is not None:
        selected_rows[0]["spread_source"] = "ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
        selected_rows[0]["cost_classification"] = "SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
        selected_rows[0]["selection_rule"] = "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP"
        selected_rows[0]["post_fill_quote_selection"] = "DISALLOWED_TO_AVOID_LOOKAHEAD"
        selected_rows[0]["selection_status"] = "PASS_ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT"
        selected_rows[0]["row_hash"] = canonical_sha256({key: _csv_value(value) for key, value in selected_rows[0].items() if key != "row_hash"})

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
    status = _status_payload(requirement, selected_rows, provider_condition_rows)
    _write_json(status_path, status)
    provenance_path.write_text(_provenance_text(status), encoding="ascii")
    PROCESS_RECORD.write_text(_process_record(status), encoding="ascii")
    _write_sha256_manifest(sha_path, config.output_root)
    return status


def _validate_config(config: Row441ExtendedTBBOConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST row 441 extended TBBO acquisition is not authorized")
    if config.requirements_ledger.resolve() != REQUIREMENTS_LEDGER.resolve():
        raise CarverBlocked("S27 v2 TEST row 441 extended TBBO acquisition must use the locked requirements ledger")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST row 441 extended TBBO acquisition output root is locked")
    if not POLICY_RECORD.exists():
        raise CarverBlocked("S27 v2 TEST row 441 policy decision record is missing")


def _row441_requirement(path: Path) -> dict[str, str]:
    rows = [row for row in _read_csv(path) if row["row_index"] == ROW_INDEX]
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 TEST row 441 TBBO requirement must contain exactly one row")
    row = dict(rows[0])
    expected = {
        "decision_timestamp_utc": "2023-01-31T04:00:00Z",
        "fill_candidate_timestamp_utc": "2023-01-31T05:00:00Z",
        "raw_symbol": RAW_SYMBOL,
        "order_side": "SELL",
        "order_quantity": "3",
        "starting_position_contracts": "17",
        "desired_position_contracts": "14",
        "position_change_contracts": "-3",
        "adjacent_target_position": "16",
        "market_order_reason": "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT",
        "tbbo_requirement_status": "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE",
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "request_start_utc": "2023-01-31T04:59:55Z",
        "request_end_utc": "2023-01-31T05:00:05Z",
        "result_interpretation_authorized": "FALSE",
        "source_faithful_evidence_claimed": "FALSE",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise CarverBlocked(f"S27 v2 TEST row 441 TBBO requirement drift: {key}")
    if row["row_hash"] != canonical_sha256({key: value for key, value in row.items() if key != "row_hash"}):
        raise CarverBlocked("S27 v2 TEST row 441 TBBO requirement row hash drift")
    fill_time = _parse_z(row["fill_candidate_timestamp_utc"])
    row["original_request_start_utc"] = row["request_start_utc"]
    row["original_request_end_utc"] = row["request_end_utc"]
    row["request_start_utc"] = _format_z(fill_time - timedelta(seconds=LOOKBACK_SECONDS))
    row["request_end_utc"] = _format_z(fill_time + timedelta(seconds=LOOKAHEAD_SECONDS))
    row["max_selected_quote_age_seconds"] = str(MAX_SELECTED_QUOTE_AGE_SECONDS)
    row["selection_rule"] = "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP"
    row["post_fill_quote_selection"] = "DISALLOWED_TO_AVOID_LOOKAHEAD"
    return row


def _select_latest_non_crossed_quote_at_or_before_fill(
    rows: list[dict[str, Any]], requirement: dict[str, str]
) -> dict[str, Any] | None:
    fill_time = _parse_z(requirement["fill_candidate_timestamp_utc"])
    eligible = []
    for row in rows:
        try:
            ts_event = _parse_z(str(row["ts_event"]))
        except ValueError:
            continue
        age_seconds = (fill_time - ts_event).total_seconds()
        if (
            0.0 <= age_seconds <= MAX_SELECTED_QUOTE_AGE_SECONDS
            and row["provider_condition_status"] == "PASS_NON_CROSSED_POSITIVE_TBBO_QUOTE"
        ):
            candidate = dict(row)
            candidate["quote_age_seconds"] = age_seconds
            eligible.append((ts_event, candidate))
    if not eligible:
        return None
    return sorted(eligible, key=lambda item: item[0])[-1][1]


def _request_manifest(requirement: dict[str, str]) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "requirements_ledger": _rel(REQUIREMENTS_LEDGER),
        "requirements_ledger_sha256": _sha256(REQUIREMENTS_LEDGER),
        "policy_record": _rel(POLICY_RECORD),
        "policy_record_sha256": _sha256(POLICY_RECORD),
        "row_index": ROW_INDEX,
        "raw_symbol": requirement["raw_symbol"],
        "request_start_utc": requirement["request_start_utc"],
        "request_end_utc": requirement["request_end_utc"],
        "lookback_seconds": LOOKBACK_SECONDS,
        "lookahead_seconds": LOOKAHEAD_SECONDS,
        "max_selected_quote_age_seconds": MAX_SELECTED_QUOTE_AGE_SECONDS,
        "selection_rule": requirement["selection_rule"],
        "post_fill_quote_selection": requirement["post_fill_quote_selection"],
        "scope": "ROW441_ONLY_EXTENDED_LOOKBACK_2023_TEST_MARKET_ORDER_TBBO_REQUIREMENT",
        "broader_provider_api_access": "NO",
        "general_historical_download": "NO",
        "validation_oos_lockbox_forward_access": "NO",
        "pnl_result_emission": "NO",
        "source_faithful_evidence_claim": "NO",
    }


def _status_payload(
    requirement: dict[str, str],
    selected_rows: list[dict[str, Any]],
    provider_condition_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    failed = [row for row in selected_rows if not str(row["selection_status"]).startswith("PASS_")]
    selected = selected_rows[0]
    provider = provider_condition_rows[0]
    return {
        "authorization": AUTHORIZATION,
        "status": (
            "PASS_ROW441_EXTENDED_LOOKBACK_DATABENTO_TBBO_SELECTED_NOT_RESULT"
            if not failed
            else "FAIL_CLOSED_ROW441_EXTENDED_LOOKBACK_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT"
        ),
        "row_index": ROW_INDEX,
        "request_start_utc": requirement["request_start_utc"],
        "request_end_utc": requirement["request_end_utc"],
        "selected_row_count": len(selected_rows) - len(failed),
        "failed_row_count": len(failed),
        "failed_row_indices": [row["row_index"] for row in failed],
        "selected_quote_ts_event": selected.get("selected_quote_ts_event", ""),
        "quote_age_seconds": selected.get("quote_age_seconds", ""),
        "bid_px_00": selected.get("bid_px_00", ""),
        "ask_px_00": selected.get("ask_px_00", ""),
        "selected_executable_market_fill_price": selected.get("selected_executable_market_fill_price", ""),
        "selection_status": selected.get("selection_status", ""),
        "provider_condition_status": provider.get("provider_condition_status", ""),
        "quote_rows_returned": provider.get("quote_rows_returned", ""),
        "provider_api_access": "ROW441_ONLY_BOUNDED_DATABENTO_TBBO_EXTENDED_LOOKBACK",
        "downloads": "ROW441_ONLY_BOUNDED_TBBO_WINDOW",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 441 Extended-Lookback TBBO Evidence Provenance

Status:

```text
{status['status']}
```

Row: {status['row_index']}
Request window: {status['request_start_utc']} through {status['request_end_utc']}
Selected rows: {status['selected_row_count']}
Failed rows: {status['failed_row_count']}

This evidence acquisition is row-441-only and does not authorize broader TEST continuation, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 441 Market-Order TBBO Extended-Lookback Evidence

Date: 2026-06-14

Status:

```text
{status['status']}
```

This process record was written by the row-441-only bounded DataBento TBBO extended-lookback evidence acquisition tool.

Scope:

- Row index: `441`
- Raw symbol: `ZNH3`
- Fill candidate timestamp: `2023-01-31T05:00:00Z`
- Request window: `{status['request_start_utc']}` through `{status['request_end_utc']}`
- Selection rule: latest non-crossed positive TBBO at or before fill timestamp
- Max selected quote age: `{MAX_SELECTED_QUOTE_AGE_SECONDS}` seconds
- Engineering label if selected: `ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT`

Selected row count: `{status['selected_row_count']}`
Failed row count: `{status['failed_row_count']}`
Quote rows returned: `{status['quote_rows_returned']}`
Selected quote timestamp: `{status['selected_quote_ts_event']}`
Quote age seconds: `{status['quote_age_seconds']}`
Bid: `{status['bid_px_00']}`
Ask: `{status['ask_px_00']}`
Executable fill price: `{status['selected_executable_market_fill_price']}`
Selection status: `{status['selection_status']}`
Provider condition status: `{status['provider_condition_status']}`

This evidence gate does not authorize broader TEST continuation, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
"""


def _ensure_output_dirs(root: Path) -> None:
    for folder in ("raw_provider_output", "manifest", "provider_condition", "ledger", "status", "provenance", "hashes"):
        (root / folder).mkdir(parents=True, exist_ok=True)


def _format_z(value: Any) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    main()

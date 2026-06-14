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
    POINT_VALUE_USD,
    PROVIDER,
    RAW_SYMBOL,
    REQUIREMENTS_LEDGER,
    SCHEMA,
    STYPE_IN,
    _csv_value,
    _first_present,
    _float_or_none,
    _parse_z,
    _quote_condition_status,
    _read_databento_key,
    _rel,
    _sha256,
    _string_timestamp,
    _write_csv,
    _write_json,
    _write_sha256_manifest,
)


RUN_ID = "20260613_S27_V2_2023_TEST_ROW438_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY"
AUTHORIZATION = "S27_V2_2023_TEST_ROW438_BOUNDED_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_GATE"
LOOKBACK_SECONDS = 60
LOOKAHEAD_SECONDS = 5
MAX_SELECTED_QUOTE_AGE_SECONDS = 60.0
ROW438_BOUNDED_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260613_2023_test_row438_market_order_tbbo"
)
ROW438_BOUNDED_STATUS = ROW438_BOUNDED_ROOT / "status/20260613_S27_V2_2023_TEST_ROW438_MARKET_ORDER_TBBO_status.json"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260613_2023_test_row438_market_order_tbbo_failed_window_retry"
)
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW438_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_2026-06-13.md"
)


@dataclass(frozen=True)
class Row438FailedWindowRetryConfig:
    execution_authorized: bool
    requirements_ledger: Path = REQUIREMENTS_LEDGER
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = run_row438_failed_window_retry(Row438FailedWindowRetryConfig(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")
    print(f"failed_rows={status['failed_row_count']}")


def run_row438_failed_window_retry(config: Row438FailedWindowRetryConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    requirements = _failed_requirements(config.requirements_ledger)
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
                raise CarverBlocked(f"Row 438 retry raw outputs already exist for row {row_index}; refusing duplicate provider request")
            store = client.timeseries.get_range(
                dataset=DATASET,
                schema=SCHEMA,
                symbols=[requirement["raw_symbol"]],
                stype_in=STYPE_IN,
                start=requirement["retry_request_start_utc"],
                end=requirement["retry_request_end_utc"],
                path=raw_dbn,
            )
            if not raw_dbn.exists() or raw_dbn.stat().st_size <= 0:
                raise RuntimeError(f"Databento returned no retry TBBO DBN bytes for row {row_index}")
            df = store.to_df()
            df.to_csv(raw_csv)
            quote_rows = _normalise_tbbo_rows(df, requirement)
            selected_row = _select_latest_non_crossed_quote_at_or_before_fill(quote_rows, requirement)
        except Exception as exc:  # noqa: BLE001 - failures must be ledgered and fail closed.
            provider_errors.append({"error_type": type(exc).__name__, "message": str(exc)})
        provider_condition_rows.append(_provider_condition_row(requirement, quote_rows, selected_row, provider_errors))
        selected_rows.append(_selected_spread_row(requirement, selected_row, raw_dbn, raw_csv, provider_errors))
        raw_output_rows.append(
            {
                "row_index": row_index,
                "retry_raw_dbn_relative_path": _rel(raw_dbn),
                "retry_raw_dbn_sha256": _sha256(raw_dbn) if raw_dbn.exists() else "MISSING_RAW_DBN",
                "retry_raw_csv_relative_path": _rel(raw_csv),
                "retry_raw_csv_sha256": _sha256(raw_csv) if raw_csv.exists() else "MISSING_RAW_CSV",
            }
        )

    selected_path = config.output_root / "ledger" / f"{RUN_ID}_selected_spread_registry.csv"
    provider_path = config.output_root / "provider_condition" / f"{RUN_ID}_provider_condition_ledger.csv"
    raw_path = config.output_root / "raw_provider_output" / f"{RUN_ID}_raw_output_registry.csv"
    status_path = config.output_root / "status" / f"{RUN_ID}_status.json"
    provenance_path = config.output_root / "provenance" / f"{RUN_ID}_provenance.md"
    sha_path = config.output_root / "hashes" / f"{RUN_ID}_sha256.csv"

    _write_csv(selected_path, selected_rows)
    _write_csv(provider_path, provider_condition_rows)
    _write_csv(raw_path, raw_output_rows)
    status = _status_payload(requirements, selected_rows, provider_condition_rows)
    _write_json(status_path, status)
    provenance_path.write_text(_provenance_text(status), encoding="ascii")
    PROCESS_RECORD.write_text(_process_record(status), encoding="ascii")
    _write_sha256_manifest(sha_path, config.output_root)
    if status["status"] != "PASS_ROW438_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_SELECTED_NOT_RESULT":
        raise CarverBlocked("S27 v2 TEST row 438 TBBO failed-window retry failed closed; see retry status ledger")
    return status


def _validate_config(config: Row438FailedWindowRetryConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST row 438 TBBO retry is not authorized")
    if config.requirements_ledger.resolve() != REQUIREMENTS_LEDGER.resolve():
        raise CarverBlocked("S27 v2 TEST row 438 TBBO retry must use the locked requirements ledger")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST row 438 TBBO retry output root is locked")


def _failed_requirements(path: Path) -> list[dict[str, str]]:
    status = _read_json(ROW438_BOUNDED_STATUS)
    failed_indices = tuple(str(index) for index in status.get("failed_row_indices", ()))
    if failed_indices != ("438",):
        raise CarverBlocked("S27 v2 TEST row 438 retry must be limited to row 438 only")
    if not failed_indices:
        raise CarverBlocked("S27 v2 TEST row 438 TBBO retry has no failed rows to retry")
    rows = {row["row_index"]: row for row in _read_csv(path)}
    requirements = []
    for row_index in failed_indices:
        row = dict(rows[row_index])
        if row["tbbo_requirement_status"] != "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE":
            raise CarverBlocked(f"S27 v2 TEST row 438 retry row {row_index} is not a missing-TBBO requirement")
        if row["raw_symbol"] != RAW_SYMBOL or row["provider"] != PROVIDER or row["dataset"] != DATASET or row["schema"] != SCHEMA:
            raise CarverBlocked("S27 v2 TEST row 438 retry provider/schema drift")
        if not row["decision_timestamp_utc"].startswith("2023-") or not row["fill_candidate_timestamp_utc"].startswith("2023-"):
            raise CarverBlocked("S27 v2 TEST row 438 retry rows must stay in 2023")
        if row["source_faithful_evidence_claimed"] != "FALSE" or row["result_interpretation_authorized"] != "FALSE":
            raise CarverBlocked("S27 v2 TEST row 438 retry requirements must not claim result/source-faithful authority")
        _validate_original_request_window(row)
        if row["row_hash"] != canonical_sha256({key: value for key, value in row.items() if key != "row_hash"}):
            raise CarverBlocked("S27 v2 TEST row 438 retry requirement row hash drift")
        fill_time = _parse_z(row["fill_candidate_timestamp_utc"])
        row["original_request_start_utc"] = row["request_start_utc"]
        row["original_request_end_utc"] = row["request_end_utc"]
        row["retry_request_start_utc"] = _format_z(fill_time - timedelta(seconds=LOOKBACK_SECONDS))
        row["retry_request_end_utc"] = _format_z(fill_time + timedelta(seconds=LOOKAHEAD_SECONDS))
        row["retry_lookback_seconds"] = str(LOOKBACK_SECONDS)
        row["retry_lookahead_seconds"] = str(LOOKAHEAD_SECONDS)
        row["max_selected_quote_age_seconds"] = str(MAX_SELECTED_QUOTE_AGE_SECONDS)
        requirements.append(row)
    return requirements


def _validate_original_request_window(row: dict[str, str]) -> None:
    fill_time = _parse_z(row["fill_candidate_timestamp_utc"])
    expected_start = _format_z(fill_time - timedelta(seconds=5))
    expected_end = _format_z(fill_time + timedelta(seconds=5))
    if row["request_start_utc"] != expected_start or row["request_end_utc"] != expected_end:
        raise CarverBlocked("S27 v2 TEST row 438 retry source request window must equal fill timestamp +/- 5 seconds")


def _request_manifest(requirements: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "standing_authorization": "S27_V2_STANDING_BOUNDED_MARKET_ORDER_TBBO_SPREAD_EVIDENCE_POLICY",
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "failed_row_indices": [row["row_index"] for row in requirements],
        "requirements_ledger": _rel(REQUIREMENTS_LEDGER),
        "requirements_ledger_sha256": _sha256(REQUIREMENTS_LEDGER),
        "standing_batch_status": _rel(ROW438_BOUNDED_STATUS),
        "standing_batch_status_sha256": _sha256(ROW438_BOUNDED_STATUS),
        "request_count": len(requirements),
        "lookback_seconds": LOOKBACK_SECONDS,
        "lookahead_seconds": LOOKAHEAD_SECONDS,
        "max_selected_quote_age_seconds": MAX_SELECTED_QUOTE_AGE_SECONDS,
        "selection_rule": "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP",
        "post_fill_quote_selection": "DISALLOWED_TO_AVOID_LOOKAHEAD",
        "broader_provider_api_access": "NO",
        "general_historical_download": "NO",
        "validation_oos_lockbox_forward_access": "NO",
        "pnl_result_emission": "NO",
        "source_faithful_evidence_claim": "NO",
    }


def _normalise_tbbo_rows(df: Any, requirement: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if df is None or len(df) == 0:
        return rows
    reset = df.reset_index()
    for _, frame_row in reset.iterrows():
        row_dict = {str(k): frame_row[k] for k in reset.columns}
        bid = _float_or_none(_first_present(row_dict, ("bid_px_00", "bid_px_0", "bid_px")))
        ask = _float_or_none(_first_present(row_dict, ("ask_px_00", "ask_px_0", "ask_px")))
        rows.append(
            {
                "row_index": requirement["row_index"],
                "ts_event": _string_timestamp(_first_present(row_dict, ("ts_event", "ts_recv", "index"))),
                "instrument_id": str(_first_present(row_dict, ("instrument_id",))),
                "publisher_id": str(_first_present(row_dict, ("publisher_id",))),
                "raw_symbol": requirement["raw_symbol"],
                "bid_px_00": bid,
                "ask_px_00": ask,
                "bid_sz_00": _float_or_none(_first_present(row_dict, ("bid_sz_00", "bid_sz_0", "bid_sz"))),
                "ask_sz_00": _float_or_none(_first_present(row_dict, ("ask_sz_00", "ask_sz_0", "ask_sz"))),
                "spread_points": None if bid is None or ask is None else ask - bid,
                "provider_condition_status": _quote_condition_status(bid, ask),
            }
        )
    return rows


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


def _provider_condition_row(
    requirement: dict[str, str],
    quote_rows: list[dict[str, Any]],
    selected_row: dict[str, Any] | None,
    provider_errors: list[dict[str, str]],
) -> dict[str, Any]:
    row = {
        "row_index": requirement["row_index"],
        "fill_candidate_timestamp_utc": requirement["fill_candidate_timestamp_utc"],
        "original_request_start_utc": requirement["original_request_start_utc"],
        "original_request_end_utc": requirement["original_request_end_utc"],
        "retry_request_start_utc": requirement["retry_request_start_utc"],
        "retry_request_end_utc": requirement["retry_request_end_utc"],
        "raw_symbol": requirement["raw_symbol"],
        "order_side": requirement["order_side"],
        "quote_rows_returned": len(quote_rows),
        "selected_quote_ts_event": "",
        "quote_age_seconds": "",
        "provider_condition_status": "",
        "provider_error_count": len(provider_errors),
        "provider_error_summary": "; ".join(f"{e['error_type']}: {e['message']}" for e in provider_errors),
    }
    if provider_errors:
        row["provider_condition_status"] = "FAIL_CLOSED_PROVIDER_ERROR_NO_SPREAD_LOCK"
    elif selected_row is None:
        row["provider_condition_status"] = "FAIL_CLOSED_NO_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED"
    else:
        row["selected_quote_ts_event"] = selected_row["ts_event"]
        row["quote_age_seconds"] = selected_row["quote_age_seconds"]
        row["provider_condition_status"] = "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED"
    row["row_hash"] = canonical_sha256({key: _csv_value(value) for key, value in row.items()})
    return row


def _selected_spread_row(
    requirement: dict[str, str],
    selected_row: dict[str, Any] | None,
    raw_dbn: Path,
    raw_csv: Path,
    provider_errors: list[dict[str, str]],
) -> dict[str, Any]:
    row = {
        "row_index": requirement["row_index"],
        "decision_timestamp_utc": requirement["decision_timestamp_utc"],
        "fill_timestamp_utc": requirement["fill_candidate_timestamp_utc"],
        "raw_symbol": requirement["raw_symbol"],
        "market_order_side": requirement["order_side"],
        "fill_quantity": requirement["order_quantity"],
        "selected_quote_ts_event": "",
        "quote_age_seconds": "",
        "bid_px_00": "",
        "ask_px_00": "",
        "selected_executable_market_fill_price": "",
        "executable_market_fill_price_source": "",
        "spread_points": "",
        "point_value_usd": POINT_VALUE_USD,
        "spread_cost_usd_per_contract": "",
        "spread_cost_amount_usd": "",
        "spread_source": "DATABENTO_TBBO_RETRY_SELECTED_QUOTE_AT_OR_BEFORE_MARKET_FILL",
        "selection_rule": "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP",
        "post_fill_quote_selection": "DISALLOWED_TO_AVOID_LOOKAHEAD",
        "cost_classification": "SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_NOT_BOOK_EXPLICIT",
        "actual_cost_emission_authorized": "FALSE",
        "pnl_result_emission_authorized": "FALSE",
        "retry_raw_dbn_sha256": _sha256(raw_dbn) if raw_dbn.exists() else "MISSING_RAW_DBN",
        "retry_raw_csv_sha256": _sha256(raw_csv) if raw_csv.exists() else "MISSING_RAW_CSV",
        "selection_status": "FAIL_CLOSED_NO_SELECTED_TBBO_QUOTE",
    }
    if provider_errors:
        row["selection_status"] = "FAIL_CLOSED_PROVIDER_ERROR_NO_SPREAD_LOCK"
    elif selected_row is not None:
        bid = float(selected_row["bid_px_00"])
        ask = float(selected_row["ask_px_00"])
        spread = ask - bid
        fill_price = ask if requirement["order_side"] == "BUY" else bid
        row.update(
            {
                "selected_quote_ts_event": selected_row["ts_event"],
                "quote_age_seconds": selected_row["quote_age_seconds"],
                "bid_px_00": bid,
                "ask_px_00": ask,
                "selected_executable_market_fill_price": fill_price,
                "executable_market_fill_price_source": (
                    "ASK_PRICE_FOR_BUY_MARKET_ORDER"
                    if requirement["order_side"] == "BUY"
                    else "BID_PRICE_FOR_SELL_MARKET_ORDER"
                ),
                "spread_points": spread,
                "spread_cost_usd_per_contract": spread * POINT_VALUE_USD,
                "spread_cost_amount_usd": spread * POINT_VALUE_USD * abs(int(requirement["order_quantity"])),
                "selection_status": "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT",
            }
        )
    row["row_hash"] = canonical_sha256({key: _csv_value(value) for key, value in row.items()})
    return row


def _status_payload(
    requirements: list[dict[str, str]],
    selected_rows: list[dict[str, Any]],
    provider_condition_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    failed = [row for row in selected_rows if not str(row["selection_status"]).startswith("PASS_")]
    return {
        "authorization": AUTHORIZATION,
        "status": (
            "PASS_ROW438_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_SELECTED_NOT_RESULT"
            if not failed
            else "FAIL_CLOSED_ROW438_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_INCOMPLETE_NOT_RESULT"
        ),
        "requirements_count": len(requirements),
        "selected_row_count": len(selected_rows) - len(failed),
        "failed_row_count": len(failed),
        "failed_row_indices": [row["row_index"] for row in failed],
        "provider_condition_pass_count": sum(
            1 for row in provider_condition_rows if row["provider_condition_status"] == "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED"
        ),
        "provider_api_access": "ROW438_ONLY_BOUNDED_DATABENTO_TBBO_RETRY",
        "downloads": "BOUNDED_FAILED_ROW_TBBO_WINDOWS_ONLY",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 438 Market-Order TBBO Failed-Window Retry Provenance

Status:

```text
{status['status']}
```

Requirements: {status['requirements_count']}
Selected rows: {status['selected_row_count']}
Failed rows: {status['failed_row_count']}

This retry was limited to failed rows from the row 438 bounded acquisition status. Selection remained at-or-before fill; post-fill quote selection stayed disallowed.
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# S27 V2 ZN 2023 TEST Row 438 Market-Order TBBO Failed-Window Retry

Date: 2026-06-13

Status:

```text
{status['status']}
```

Requirements count: `{status['requirements_count']}`
Selected row count: `{status['selected_row_count']}`
Failed row count: `{status['failed_row_count']}`
Failed row indices: `{','.join(status['failed_row_indices']) if status['failed_row_indices'] else 'NONE'}`

The retry is bounded to failed rows from the row 438 bounded acquisition, with `60` seconds pre-fill lookback, `5` seconds post-fill capture, and at-or-before-fill selection only. It does not authorize broad provider/API access, general downloads, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
"""


def _ensure_output_dirs(root: Path) -> None:
    for folder in ("raw_provider_output", "manifest", "provider_condition", "ledger", "status", "provenance", "hashes"):
        (root / folder).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="ascii"))
    if not isinstance(payload, dict):
        raise CarverBlocked("S27 v2 TEST row 438 retry JSON payload must be an object")
    return payload


def _format_z(value: Any) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    main()

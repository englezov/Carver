from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
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
    STYPE_IN,
    _csv_value,
    _first_present,
    _float_or_none,
    _parse_z,
    _read_databento_key,
    _rel,
    _sha256,
    _string_timestamp,
    _write_csv,
    _write_json,
    _write_sha256_manifest,
)


RUN_ID = "20260614_S27_V2_2023_TEST_ROW704_MBP1_TOP_OF_BOOK_EVIDENCE"
AUTHORIZATION = "S27_V2_TEST_ROW704_BOUNDED_MBP1_TOP_OF_BOOK_EVIDENCE_ACQUISITION"
ROW_INDEX = "704"
RAW_SYMBOL = "ZNM3"
SCHEMA = "mbp-1"
REQUEST_START_UTC = "2023-02-16T04:55:00Z"
FILL_TIMESTAMP_UTC = "2023-02-16T05:00:00Z"
REQUEST_END_UTC = "2023-02-16T05:00:05Z"
ORDER_SIDE = "SELL"
FILL_QUANTITY = "4"
MAX_SELECTED_QUOTE_AGE_SECONDS = 300.0
EVIDENCE_LABEL = "ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_EVIDENCE_NOT_BOOK_EXPLICIT_NOT_TBBO"
PASS_STATUS = "PASS_ROW704_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL_SELECTED_NOT_RESULT"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260614_2023_test_row704_mbp1_top_of_book_evidence"
)
POLICY_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_NO_ELIGIBLE_TBBO_MARKET_ORDER_POLICY_REMEDIATION_2026-06-14.md"
)
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW704_MBP1_TOP_OF_BOOK_EVIDENCE_2026-06-14.md"
)


@dataclass(frozen=True)
class Row704MBP1Config:
    execution_authorized: bool
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = run_row704_mbp1_top_of_book_acquisition(Row704MBP1Config(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")
    print(f"failed_rows={status['failed_row_count']}")


def run_row704_mbp1_top_of_book_acquisition(config: Row704MBP1Config) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    requirement = _row704_requirement()
    client = db.Historical(_read_databento_key())

    _write_json(config.output_root / "manifest" / f"{RUN_ID}_request_manifest.json", _request_manifest(requirement))

    raw_dbn = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{ROW_INDEX}.dbn"
    raw_csv = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{ROW_INDEX}_mbp1_dataframe.csv"
    provider_errors: list[dict[str, str]] = []
    quote_rows: list[dict[str, Any]] = []
    selected_row: dict[str, Any] | None = None

    try:
        if raw_dbn.exists() or raw_csv.exists():
            raise CarverBlocked("Row 704 MBP-1 raw outputs already exist; refusing duplicate provider request")
        store = client.timeseries.get_range(
            dataset=DATASET,
            schema=SCHEMA,
            symbols=[RAW_SYMBOL],
            stype_in=STYPE_IN,
            start=REQUEST_START_UTC,
            end=REQUEST_END_UTC,
            path=raw_dbn,
        )
        if not raw_dbn.exists() or raw_dbn.stat().st_size <= 0:
            raise RuntimeError("Databento returned no row 704 raw MBP-1 DBN bytes")
        df = store.to_df()
        df.to_csv(raw_csv)
        quote_rows = _normalise_mbp1_rows(df, requirement)
        selected_row = _select_latest_sell_bid_at_or_before_fill(quote_rows)
    except Exception as exc:  # noqa: BLE001 - evidence failures must be ledgered and fail closed.
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
    return status


def _validate_config(config: Row704MBP1Config) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST row 704 MBP-1 top-of-book acquisition is not authorized")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST row 704 MBP-1 output root is locked")
    if not POLICY_RECORD.exists():
        raise CarverBlocked("S27 v2 TEST no-eligible-TBBO policy remediation record is missing")


def _row704_requirement() -> dict[str, str]:
    row = {
        "row_index": ROW_INDEX,
        "decision_timestamp_utc": "2023-02-16T04:00:00Z",
        "fill_candidate_timestamp_utc": FILL_TIMESTAMP_UTC,
        "raw_symbol": RAW_SYMBOL,
        "order_side": ORDER_SIDE,
        "order_quantity": FILL_QUANTITY,
        "starting_position_contracts": "-10",
        "desired_position_contracts": "-14",
        "position_change_contracts": "-4",
        "market_order_reason": "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT",
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "request_start_utc": REQUEST_START_UTC,
        "request_end_utc": REQUEST_END_UTC,
        "max_selected_quote_age_seconds": str(MAX_SELECTED_QUOTE_AGE_SECONDS),
        "selection_rule": "LATEST_POSITIVE_NON_CROSSED_NON_DEGRADED_SELL_BID_AT_OR_BEFORE_FILL_TIMESTAMP",
        "post_fill_quote_selection": "DISALLOWED_TO_AVOID_LOOKAHEAD",
        "result_interpretation_authorized": "FALSE",
        "source_faithful_evidence_claimed": "FALSE",
    }
    row["row_hash"] = canonical_sha256(row)
    return row


def _normalise_mbp1_rows(df: Any, requirement: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if df is None or len(df) == 0:
        return rows
    reset = df.reset_index()
    for _, frame_row in reset.iterrows():
        row_dict = {str(k): frame_row[k] for k in reset.columns}
        bid_px = _first_present(row_dict, ("bid_px_00", "bid_px_0", "bid_px"))
        ask_px = _first_present(row_dict, ("ask_px_00", "ask_px_0", "ask_px"))
        bid_sz = _first_present(row_dict, ("bid_sz_00", "bid_sz_0", "bid_sz"))
        ask_sz = _first_present(row_dict, ("ask_sz_00", "ask_sz_0", "ask_sz"))
        bid = _float_or_none(bid_px)
        ask = _float_or_none(ask_px)
        ts_event = _string_timestamp(_first_present(row_dict, ("ts_event", "ts_recv", "index")))
        rows.append(
            {
                "row_index": requirement["row_index"],
                "ts_event": ts_event,
                "instrument_id": str(_first_present(row_dict, ("instrument_id",))),
                "publisher_id": str(_first_present(row_dict, ("publisher_id",))),
                "raw_symbol": requirement["raw_symbol"],
                "bid_px_00": bid,
                "ask_px_00": ask,
                "bid_sz_00": _float_or_none(bid_sz),
                "ask_sz_00": _float_or_none(ask_sz),
                "spread_points": None if bid is None or ask is None else ask - bid,
                "provider_condition_status": _quote_condition_status(bid, ask),
            }
        )
    return rows


def _select_latest_sell_bid_at_or_before_fill(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    fill_time = _parse_z(FILL_TIMESTAMP_UTC)
    eligible = []
    for row in rows:
        try:
            ts_event = _parse_z(str(row["ts_event"]))
        except ValueError:
            continue
        age_seconds = (fill_time - ts_event).total_seconds()
        if (
            0.0 <= age_seconds <= MAX_SELECTED_QUOTE_AGE_SECONDS
            and row["provider_condition_status"] == "PASS_NON_CROSSED_POSITIVE_MBP1_TOP_OF_BOOK_QUOTE"
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
        "request_start_utc": requirement["request_start_utc"],
        "request_end_utc": requirement["request_end_utc"],
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
        row["provider_condition_status"] = "FAIL_CLOSED_PROVIDER_ERROR_NO_MBP1_SPREAD_LOCK"
    elif selected_row is None:
        row["provider_condition_status"] = "FAIL_CLOSED_NO_FRESH_NON_CROSSED_MBP1_TOP_OF_BOOK_QUOTE_SELECTED"
    else:
        row["selected_quote_ts_event"] = selected_row["ts_event"]
        row["quote_age_seconds"] = selected_row["quote_age_seconds"]
        row["provider_condition_status"] = "PASS_FRESH_NON_CROSSED_MBP1_TOP_OF_BOOK_QUOTE_SELECTED"
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
        "spread_source": EVIDENCE_LABEL,
        "cost_classification": "ALTERNATIVE_SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_NOT_BOOK_EXPLICIT",
        "actual_cost_emission_authorized": "FALSE",
        "pnl_result_emission_authorized": "FALSE",
        "raw_dbn_sha256": _sha256(raw_dbn) if raw_dbn.exists() else "MISSING_RAW_DBN",
        "raw_csv_sha256": _sha256(raw_csv) if raw_csv.exists() else "MISSING_RAW_CSV",
        "selection_status": "FAIL_CLOSED_NO_SELECTED_MBP1_TOP_OF_BOOK_QUOTE",
        "selection_rule": requirement["selection_rule"],
        "post_fill_quote_selection": requirement["post_fill_quote_selection"],
    }
    if provider_errors:
        row["selection_status"] = "FAIL_CLOSED_PROVIDER_ERROR_NO_MBP1_SPREAD_LOCK"
    elif selected_row is not None:
        bid = float(selected_row["bid_px_00"])
        ask = float(selected_row["ask_px_00"])
        spread = ask - bid
        row.update(
            {
                "selected_quote_ts_event": selected_row["ts_event"],
                "quote_age_seconds": selected_row["quote_age_seconds"],
                "bid_px_00": bid,
                "ask_px_00": ask,
                "selected_executable_market_fill_price": bid,
                "executable_market_fill_price_source": "BID_PRICE_FOR_SELL_MARKET_ORDER_FROM_MBP1_TOP_OF_BOOK",
                "spread_points": spread,
                "spread_cost_usd_per_contract": spread * POINT_VALUE_USD,
                "spread_cost_amount_usd": spread * POINT_VALUE_USD * abs(int(requirement["order_quantity"])),
                "selection_status": PASS_STATUS,
            }
        )
    row["row_hash"] = canonical_sha256({key: _csv_value(value) for key, value in row.items()})
    return row


def _request_manifest(requirement: dict[str, str]) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "policy_record": _rel(POLICY_RECORD),
        "policy_record_sha256": _sha256(POLICY_RECORD),
        "row_index": ROW_INDEX,
        "raw_symbol": RAW_SYMBOL,
        "request_start_utc": REQUEST_START_UTC,
        "request_end_utc": REQUEST_END_UTC,
        "fill_timestamp_utc": FILL_TIMESTAMP_UTC,
        "requirement_row_hash": requirement["row_hash"],
        "scope": "ROW704_ONLY_BOUNDED_MBP1_TOP_OF_BOOK_EVIDENCE",
        "selection_rule": requirement["selection_rule"],
        "evidence_label": EVIDENCE_LABEL,
        "broader_provider_api_access": "NO",
        "general_historical_download": "NO",
        "validation_oos_lockbox_forward_access": "NO",
        "test_continuation": "NO",
        "market_order_fill_cost_pnl_result_emission": "NO",
        "source_faithful_evidence_claim": "NO",
    }


def _status_payload(
    selected_rows: list[dict[str, Any]],
    provider_condition_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    selected = selected_rows[0]
    provider = provider_condition_rows[0]
    passed = str(selected["selection_status"]).startswith("PASS_")
    return {
        "authorization": AUTHORIZATION,
        "status": (
            "PASS_ROW704_BOUNDED_MBP1_TOP_OF_BOOK_SELECTED_NOT_RESULT"
            if passed
            else "FAIL_CLOSED_ROW704_BOUNDED_MBP1_TOP_OF_BOOK_NO_SELECTED_QUOTE_NOT_RESULT"
        ),
        "row_index": ROW_INDEX,
        "raw_symbol": RAW_SYMBOL,
        "schema": SCHEMA,
        "request_start_utc": REQUEST_START_UTC,
        "request_end_utc": REQUEST_END_UTC,
        "fill_timestamp_utc": FILL_TIMESTAMP_UTC,
        "selected_row_count": 1 if passed else 0,
        "failed_row_count": 0 if passed else 1,
        "selected_quote_ts_event": selected.get("selected_quote_ts_event", ""),
        "quote_age_seconds": selected.get("quote_age_seconds", ""),
        "bid_px_00": selected.get("bid_px_00", ""),
        "ask_px_00": selected.get("ask_px_00", ""),
        "selected_executable_market_fill_price": selected.get("selected_executable_market_fill_price", ""),
        "selection_status": selected.get("selection_status", ""),
        "provider_condition_status": provider.get("provider_condition_status", ""),
        "quote_rows_returned": provider.get("quote_rows_returned", ""),
        "provider_error_count": provider.get("provider_error_count", ""),
        "provider_api_access": "ROW704_ONLY_BOUNDED_DATABENTO_MBP1_TOP_OF_BOOK",
        "downloads": "ROW704_ONLY_BOUNDED_MBP1_TOP_OF_BOOK_WINDOW",
        "test_continuation": "NO",
        "market_order_fill_cost_pnl_result_emission": "NO",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 704 MBP-1 Top-Of-Book Evidence Provenance

Status:

```text
{status['status']}
```

Row: {status['row_index']}
Raw symbol: {status['raw_symbol']}
Schema: {status['schema']}
Request: {status['request_start_utc']} through {status['request_end_utc']}
Selected rows: {status['selected_row_count']}
Failed rows: {status['failed_row_count']}

This is bounded row-704-only MBP-1/top-of-book evidence. It is not book-explicit authority, not TBBO evidence, not TEST continuation, not market-order/fill/cost/PnL/result emission, not result interpretation, and not a source-faithful evidence claim.
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 704 MBP-1 Top-Of-Book Evidence

Date: 2026-06-14

Status:

```text
{status['status']}
```

## Scope

Bounded row-704-only DataBento MBP-1/top-of-book evidence acquisition after no-eligible-TBBO policy remediation.

## Request

```text
provider: {PROVIDER}
dataset: {DATASET}
schema: {SCHEMA}
stype_in: {STYPE_IN}
raw_symbol: {RAW_SYMBOL}
request_start_utc: {REQUEST_START_UTC}
request_end_utc: {REQUEST_END_UTC}
fill_timestamp_utc: {FILL_TIMESTAMP_UTC}
```

## Evidence Label

```text
{EVIDENCE_LABEL}
```

## Selected Evidence

```text
selected_row_count: {status['selected_row_count']}
failed_row_count: {status['failed_row_count']}
quote_rows_returned: {status['quote_rows_returned']}
provider_error_count: {status['provider_error_count']}
provider_condition_status: {status['provider_condition_status']}
selection_status: {status['selection_status']}
selected_quote_ts_event: {status['selected_quote_ts_event']}
quote_age_seconds: {status['quote_age_seconds']}
bid_px_00: {status['bid_px_00']}
ask_px_00: {status['ask_px_00']}
selected_executable_market_fill_price: {status['selected_executable_market_fill_price']}
```

## Non-Authorization

This record does not authorize TEST continuation, market-order/fill/cost/PnL/result emission, result interpretation, PnL evaluation beyond mechanical construction, VALIDATION, OOS, Lockbox, Forward, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
"""


def _ensure_output_dirs(root: Path) -> None:
    for child in ("ledger", "provider_condition", "raw_provider_output", "manifest", "status", "provenance", "hashes"):
        (root / child).mkdir(parents=True, exist_ok=True)


def _quote_condition_status(bid: float | None, ask: float | None) -> str:
    if bid is None or ask is None:
        return "FAIL_CLOSED_MISSING_BID_OR_ASK"
    if bid <= 0.0 or ask <= 0.0:
        return "FAIL_CLOSED_NON_POSITIVE_BID_OR_ASK"
    if ask < bid:
        return "FAIL_CLOSED_CROSSED_MBP1_TOP_OF_BOOK_QUOTE"
    return "PASS_NON_CROSSED_POSITIVE_MBP1_TOP_OF_BOOK_QUOTE"


if __name__ == "__main__":
    main()

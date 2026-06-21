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
    _parse_z,
    _quote_condition_status,
    _read_csv,
    _read_databento_key,
    _rel,
    _sha256,
    _string_timestamp,
    _write_csv,
    _write_json,
    _write_sha256_manifest,
    _first_present,
    _float_or_none,
)


RUN_ID = "20260612_S27_V2_2023_TEST_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY"
AUTHORIZATION = "S27_V2_2023_TEST_MARKET_ORDER_TBBO_BATCH_FAILURE_REMEDIATION_GATE"
FAILED_ROW_INDICES = ("78", "208", "210", "212", "215", "220", "306", "328", "329", "335", "340")
LOOKBACK_SECONDS = 60
LOOKAHEAD_SECONDS = 5
MAX_SELECTED_QUOTE_AGE_SECONDS = 60.0
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260612_2023_test_market_order_tbbo_failed_window_retry"
)
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_2026-06-12.md"
)


@dataclass(frozen=True)
class FailedWindowRetryConfig:
    execution_authorized: bool
    requirements_ledger: Path = REQUIREMENTS_LEDGER
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = run_failed_window_retry(FailedWindowRetryConfig(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")
    print(f"failed_rows={status['failed_row_count']}")


def run_failed_window_retry(config: FailedWindowRetryConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    requirements = _failed_requirements(config.requirements_ledger)
    client = db.Historical(_read_databento_key())
    request_manifest = _request_manifest(requirements)
    _write_json(config.output_root / "manifest" / f"{RUN_ID}_request_manifest.json", request_manifest)

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
                raise CarverBlocked(f"Retry TBBO raw outputs already exist for row {row_index}; refusing duplicate provider request")
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
                raise RuntimeError(f"Databento returned no raw TBBO DBN bytes for row {row_index}")
            df = store.to_df()
            df.to_csv(raw_csv)
            quote_rows = _normalise_tbbo_rows(df, requirement)
            selected_row = _select_latest_non_crossed_quote_at_or_before_fill(quote_rows, requirement)
        except Exception as exc:  # noqa: BLE001 - provider failures must be ledgered and fail closed.
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
    if status["status"] != "PASS_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_SELECTED_NOT_RESULT":
        raise CarverBlocked("S27 v2 TEST failed-window TBBO retry failed closed; see retry status ledger")
    return status


def _validate_config(config: FailedWindowRetryConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST TBBO failed-window retry is not authorized")
    if config.requirements_ledger.resolve() != REQUIREMENTS_LEDGER.resolve():
        raise CarverBlocked("S27 v2 TEST TBBO failed-window retry must use the locked requirements ledger")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST TBBO failed-window retry output root is locked")


def _failed_requirements(path: Path) -> list[dict[str, str]]:
    rows = _read_csv(path)
    by_index = {row["row_index"]: row for row in rows}
    requirements = []
    for row_index in FAILED_ROW_INDICES:
        row = dict(by_index[row_index])
        if row["tbbo_requirement_status"] != "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE":
            raise CarverBlocked(f"S27 v2 TEST TBBO retry row {row_index} is not a missing-TBBO requirement")
        if row["raw_symbol"] != RAW_SYMBOL or row["provider"] != PROVIDER or row["dataset"] != DATASET or row["schema"] != SCHEMA:
            raise CarverBlocked("S27 v2 TEST TBBO retry requirement provider/schema drift")
        if not row["decision_timestamp_utc"].startswith("2023-") or not row["fill_candidate_timestamp_utc"].startswith("2023-"):
            raise CarverBlocked("S27 v2 TEST TBBO retry requirements must stay in 2023")
        if row["source_faithful_evidence_claimed"] != "FALSE":
            raise CarverBlocked("S27 v2 TEST TBBO retry requirements must not claim source-faithful evidence")
        if row["row_hash"] != canonical_sha256({key: value for key, value in row.items() if key != "row_hash"}):
            raise CarverBlocked("S27 v2 TEST TBBO retry requirement row hash drift")
        fill_time = _parse_z(row["fill_candidate_timestamp_utc"])
        retry_start = fill_time - timedelta(seconds=LOOKBACK_SECONDS)
        retry_end = fill_time + timedelta(seconds=LOOKAHEAD_SECONDS)
        row["original_request_start_utc"] = row["request_start_utc"]
        row["original_request_end_utc"] = row["request_end_utc"]
        row["retry_request_start_utc"] = _format_z(retry_start)
        row["retry_request_end_utc"] = _format_z(retry_end)
        row["retry_lookback_seconds"] = str(LOOKBACK_SECONDS)
        row["retry_lookahead_seconds"] = str(LOOKAHEAD_SECONDS)
        row["max_selected_quote_age_seconds"] = str(MAX_SELECTED_QUOTE_AGE_SECONDS)
        requirements.append(row)
    return requirements


def _request_manifest(requirements: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "raw_symbol": RAW_SYMBOL,
        "failed_row_indices": list(FAILED_ROW_INDICES),
        "requirements_ledger": _rel(REQUIREMENTS_LEDGER),
        "requirements_ledger_sha256": _sha256(REQUIREMENTS_LEDGER),
        "request_count": len(requirements),
        "lookback_seconds": LOOKBACK_SECONDS,
        "lookahead_seconds": LOOKAHEAD_SECONDS,
        "max_selected_quote_age_seconds": MAX_SELECTED_QUOTE_AGE_SECONDS,
        "selection_rule": "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP",
        "post_fill_quote_selection": "DISALLOWED_TO_AVOID_LOOKAHEAD",
        "broader_test_continuation": "NO",
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
            "PASS_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_SELECTED_NOT_RESULT"
            if not failed
            else "FAIL_CLOSED_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_INCOMPLETE_NOT_RESULT"
        ),
        "requirements_count": len(requirements),
        "selected_row_count": len(selected_rows) - len(failed),
        "failed_row_count": len(failed),
        "failed_row_indices": [row["row_index"] for row in failed],
        "provider_condition_pass_count": sum(
            1 for row in provider_condition_rows if row["provider_condition_status"] == "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED"
        ),
        "selection_rule": "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP",
        "post_fill_quote_selection": "DISALLOWED_TO_AVOID_LOOKAHEAD",
        "lookback_seconds": LOOKBACK_SECONDS,
        "lookahead_seconds": LOOKAHEAD_SECONDS,
        "max_selected_quote_age_seconds": MAX_SELECTED_QUOTE_AGE_SECONDS,
        "provider_api_access": "BOUNDED_DATABENTO_TBBO_FAILED_ROWS_ONLY",
        "downloads": "BOUNDED_TBBO_FAILED_ROW_WINDOWS_ONLY",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Market-Order TBBO Failed-Window Retry Provenance

Status:

```text
{status['status']}
```

Requirements: {status['requirements_count']}
Selected rows: {status['selected_row_count']}
Failed rows: {status['failed_row_count']}

Selection rule: `{status['selection_rule']}`
Post-fill quote selection: `{status['post_fill_quote_selection']}`
Lookback seconds: `{status['lookback_seconds']}`
Max selected quote age seconds: `{status['max_selected_quote_age_seconds']}`

This retry does not authorize broader TEST continuation, result interpretation, source-faithful evidence claim, VALIDATION, OOS, Lockbox, Forward, tuning, adapter work, deployment, trading, promotion, or Git action.
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# S27 V2 ZN 2023 TEST Market-Order TBBO Failed-Window Retry

Date: 2026-06-12

Status:

```text
{status['status']}
```

This process record was written by the bounded DataBento TBBO failed-window retry tool.

Scope:

- Failed row indices: `{', '.join(FAILED_ROW_INDICES)}`
- Retry lookback seconds: `{LOOKBACK_SECONDS}`
- Retry lookahead seconds: `{LOOKAHEAD_SECONDS}`
- Selection rule: `{status['selection_rule']}`
- Post-fill quote selection: `{status['post_fill_quote_selection']}`

Counts:

- Requirements count: `{status['requirements_count']}`
- Selected row count: `{status['selected_row_count']}`
- Failed row count: `{status['failed_row_count']}`
- Failed row indices after retry: `{', '.join(status['failed_row_indices']) if status['failed_row_indices'] else 'NONE'}`

This evidence gate does not authorize broader TEST continuation, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
"""


def _ensure_output_dirs(root: Path) -> None:
    for name in ("hashes", "ledger", "manifest", "provider_condition", "provenance", "raw_provider_output", "status"):
        (root / name).mkdir(parents=True, exist_ok=True)


def _format_z(value: Any) -> str:
    text = value.isoformat()
    if text.endswith("+00:00"):
        text = text[:-6] + "Z"
    return text


if __name__ == "__main__":
    main()

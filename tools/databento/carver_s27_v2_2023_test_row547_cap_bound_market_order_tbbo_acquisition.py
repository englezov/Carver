from __future__ import annotations

import sys
from dataclasses import dataclass
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
    RAW_SYMBOL,
    REQUIREMENTS_LEDGER,
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


RUN_ID = "20260614_S27_V2_2023_TEST_ROW547_CAP_BOUND_MARKET_ORDER_TBBO"
AUTHORIZATION = "S27_V2_2023_TEST_CAP_BOUND_MARKET_ORDER_CLASS_IMPLEMENTATION_AND_CONTINUATION_GATE"
ROW_INDEX = "547"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260614_2023_test_row547_cap_bound_market_order_tbbo"
)
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW547_CAP_BOUND_MARKET_ORDER_TBBO_EVIDENCE_2026-06-14.md"
)


@dataclass(frozen=True)
class Row547TBBOConfig:
    execution_authorized: bool
    requirements_ledger: Path = REQUIREMENTS_LEDGER
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = run_row547_tbbo_acquisition(Row547TBBOConfig(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")
    print(f"failed_rows={status['failed_row_count']}")


def run_row547_tbbo_acquisition(config: Row547TBBOConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    requirement = _row547_requirement(config.requirements_ledger)
    client = db.Historical(_read_databento_key())

    _write_json(config.output_root / "manifest" / f"{RUN_ID}_request_manifest.json", _request_manifest(requirement))

    raw_dbn = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{ROW_INDEX}.dbn"
    raw_csv = config.output_root / "raw_provider_output" / f"{RUN_ID}_row_{ROW_INDEX}_tbbo_dataframe.csv"
    provider_errors: list[dict[str, str]] = []
    quote_rows: list[dict[str, Any]] = []
    selected_row: dict[str, Any] | None = None

    try:
        if raw_dbn.exists() or raw_csv.exists():
            raise CarverBlocked("Row 547 TBBO raw outputs already exist; refusing duplicate provider request")
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
            raise RuntimeError("Databento returned no row 547 raw TBBO DBN bytes")
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

    if status["status"] != "PASS_ROW547_BOUNDED_DATABENTO_TBBO_SELECTED_NOT_RESULT":
        raise CarverBlocked("S27 v2 TEST row 547 TBBO evidence failed closed; see status ledger")
    return status


def _validate_config(config: Row547TBBOConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST row 547 TBBO acquisition is not authorized")
    if config.requirements_ledger.resolve() != REQUIREMENTS_LEDGER.resolve():
        raise CarverBlocked("S27 v2 TEST row 547 TBBO acquisition must use the locked requirements ledger")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST row 547 TBBO acquisition output root is locked")


def _row547_requirement(path: Path) -> dict[str, str]:
    rows = [row for row in _read_csv(path) if row["row_index"] == ROW_INDEX]
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 TEST row 547 TBBO requirement must contain exactly one row")
    row = rows[0]
    expected = {
        "decision_timestamp_utc": "2023-02-07T00:00:00Z",
        "fill_candidate_timestamp_utc": "2023-02-07T01:00:00Z",
        "raw_symbol": RAW_SYMBOL,
        "order_side": "SELL",
        "order_quantity": "1",
        "market_order_reason": "BOOK_REQUIRED_CAP_BOUND_LIMIT_SIDE_NOT_PLACED",
        "tbbo_requirement_status": "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE",
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "request_start_utc": "2023-02-07T00:59:55Z",
        "request_end_utc": "2023-02-07T01:00:05Z",
        "result_interpretation_authorized": "FALSE",
        "source_faithful_evidence_claimed": "FALSE",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise CarverBlocked(f"S27 v2 TEST row 547 TBBO requirement drift: {key}")
    _validate_request_window(row)
    if row["row_hash"] != canonical_sha256({key: value for key, value in row.items() if key != "row_hash"}):
        raise CarverBlocked("S27 v2 TEST row 547 TBBO requirement row hash drift")
    return row


def _validate_request_window(row: dict[str, str]) -> None:
    fill_time = _parse_z(row["fill_candidate_timestamp_utc"])
    expected_start = _format_z(fill_time, seconds=-5)
    expected_end = _format_z(fill_time, seconds=5)
    if row["request_start_utc"] != expected_start or row["request_end_utc"] != expected_end:
        raise CarverBlocked("S27 v2 TEST row 547 TBBO request window must equal fill timestamp +/- 5 seconds")


def _format_z(value: Any, *, seconds: int) -> str:
    from datetime import timedelta

    return (value + timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _request_manifest(requirement: dict[str, str]) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "standing_authorization": "S27_V2_STANDING_BOUNDED_MARKET_ORDER_TBBO_SPREAD_EVIDENCE_POLICY",
        "run_id": RUN_ID,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "requirements_ledger": _rel(REQUIREMENTS_LEDGER),
        "requirements_ledger_sha256": _sha256(REQUIREMENTS_LEDGER),
        "row_index": ROW_INDEX,
        "request_start_utc": requirement["request_start_utc"],
        "request_end_utc": requirement["request_end_utc"],
        "scope": "ROW547_ONLY_BOUNDED_CAP_BOUND_MARKET_ORDER_TBBO_REQUIREMENT",
        "broader_provider_api_access": "NO",
        "general_historical_download": "NO",
        "validation_oos_lockbox_forward_access": "NO",
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
            "PASS_ROW547_BOUNDED_DATABENTO_TBBO_SELECTED_NOT_RESULT"
            if not failed
            else "FAIL_CLOSED_ROW547_BOUNDED_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT"
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
        "provider_api_access": "ROW547_ONLY_BOUNDED_DATABENTO_TBBO",
        "downloads": "ROW547_ONLY_BOUNDED_TBBO_WINDOW",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 547 Cap-Bound Market-Order TBBO Evidence Provenance

Status:

```text
{status['status']}
```

Row: {status['row_index']}
Selected rows: {status['selected_row_count']}
Failed rows: {status['failed_row_count']}

No result interpretation, source-faithful evidence claim, VALIDATION, OOS, Lockbox, Forward, Git, adapter, deployment, trading, promotion, or tuning was authorized.
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# CARVER S27 ZN V2 - 2023 TEST Row 547 Cap-Bound Market-Order TBBO Evidence

Date: 2026-06-14

## Scope

Bounded row-547-only TBBO evidence acquisition under the cap-bound market-order implementation gate.

## Status

`{status['status']}`

## Selected Evidence

- row index: `{status['row_index']}`
- selected quote timestamp: `{status['selected_quote_ts_event']}`
- quote age seconds: `{status['quote_age_seconds']}`
- bid: `{status['bid_px_00']}`
- ask: `{status['ask_px_00']}`
- executable fill price: `{status['selected_executable_market_fill_price']}`
- selection status: `{status['selection_status']}`
- provider condition: `{status['provider_condition_status']}`

## Non-Authorizations

No broader provider/API access, general historical download, VALIDATION, OOS, Lockbox, Forward, result interpretation, source-faithful evidence claim, tuning, adapter/deployment/trading/promotion, Git action, or GPT packet preparation was authorized by this record.
"""


def _ensure_output_dirs(root: Path) -> None:
    for child in ("ledger", "provider_condition", "raw_provider_output", "manifest", "status", "provenance", "hashes"):
        (root / child).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()

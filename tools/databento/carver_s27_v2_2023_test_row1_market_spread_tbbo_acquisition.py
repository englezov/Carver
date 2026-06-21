from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked  # noqa: E402


RUN_ID = "20260612_S27_V2_2023_TEST_ROW1_ZNH3_MARKET_SPREAD_TBBO"
AUTHORIZATION = "S27_V2_BOUNDED_DATABENTO_ROW1_MARKET_SPREAD_EVIDENCE_ACQUISITION"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
SCHEMA = "tbbo"
STYPE_IN = "raw_symbol"
RAW_SYMBOL = "ZNH3"
FILL_TIMESTAMP_UTC = "2023-01-03T01:00:00Z"
REQUEST_START_UTC = "2023-01-03T00:59:55Z"
REQUEST_END_UTC = "2023-01-03T01:00:05Z"
TICK_SIZE_POINTS = 0.015625
POINT_VALUE_USD = 1000.0

OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_market_spread_evidence"
    / "ZN"
    / "20260612_2023_test_row1_znh3_tbbo"
)
PROCESS_RECORD = (
    ROOT
    / "docs"
    / "process"
    / "CARVER_S27_ZN_V2_2023_TEST_ROW1_MARKET_SPREAD_DATABENTO_TBBO_EVIDENCE_2026-06-12.md"
)

KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/apops/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/apops/Desktop/BENTO.txt"),
    Path("C:/Users/apops/Desktop/bento.txt"),
)


@dataclass(frozen=True)
class Row1MarketSpreadTBBOAcquisitionConfig:
    execution_authorized: bool
    lane_class: str
    provider: str
    dataset: str
    schema: str
    stype_in: str
    raw_symbol: str
    fill_timestamp_utc: str
    request_start_utc: str
    request_end_utc: str
    broader_test_continuation: bool
    result_or_pnl_emission: bool


def main() -> None:
    config = Row1MarketSpreadTBBOAcquisitionConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        provider=PROVIDER,
        dataset=DATASET,
        schema=SCHEMA,
        stype_in=STYPE_IN,
        raw_symbol=RAW_SYMBOL,
        fill_timestamp_utc=FILL_TIMESTAMP_UTC,
        request_start_utc=REQUEST_START_UTC,
        request_end_utc=REQUEST_END_UTC,
        broader_test_continuation=False,
        result_or_pnl_emission=False,
    )
    status = run_row1_tbbo_acquisition(config)
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_spread_cost_usd_per_contract={status.get('selected_spread_cost_usd_per_contract', 'NA')}")


def run_row1_tbbo_acquisition(config: Row1MarketSpreadTBBOAcquisitionConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs()
    client = db.Historical(_read_databento_key())

    raw_dbn = OUTPUT_ROOT / "raw_provider_output" / f"{RUN_ID}.dbn"
    raw_csv = OUTPUT_ROOT / "raw_provider_output" / f"{RUN_ID}_tbbo_dataframe.csv"
    request_manifest = OUTPUT_ROOT / "manifest" / f"{RUN_ID}_request_manifest.json"
    provider_condition_csv = OUTPUT_ROOT / "provider_condition" / f"{RUN_ID}_provider_condition_ledger.csv"
    selected_spread_csv = OUTPUT_ROOT / "ledger" / f"{RUN_ID}_selected_spread_ledger.csv"
    status_json = OUTPUT_ROOT / "status" / f"{RUN_ID}_status.json"
    provenance_md = OUTPUT_ROOT / "provenance" / f"{RUN_ID}_provenance.md"
    sha_manifest = OUTPUT_ROOT / "hashes" / f"{RUN_ID}_sha256.csv"

    _write_json(request_manifest, _request_manifest_payload(config))

    provider_errors: list[dict[str, str]] = []
    quote_rows: list[dict[str, Any]] = []
    selected_row: dict[str, Any] | None = None
    try:
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
            raise RuntimeError("Databento returned no raw TBBO DBN bytes")
        df = store.to_df()
        df.to_csv(raw_csv)
        quote_rows = _normalise_tbbo_rows(df)
        selected_row = _select_latest_non_crossed_quote_at_or_before_fill(quote_rows)
    except Exception as exc:  # noqa: BLE001 - provider failures must fail closed with evidence.
        provider_errors.append({"error_type": type(exc).__name__, "message": str(exc)})

    provider_condition_rows = _provider_condition_rows(quote_rows, provider_errors, selected_row)
    _write_csv(provider_condition_csv, provider_condition_rows)

    selected_spread_rows = _selected_spread_rows(selected_row)
    _write_csv(selected_spread_csv, selected_spread_rows)

    status = _status_payload(quote_rows, provider_errors, selected_row)
    _write_json(status_json, status)
    provenance_md.write_text(_provenance_text(status), encoding="ascii")
    PROCESS_RECORD.write_text(_process_record(status), encoding="ascii")
    _write_sha256_manifest(sha_manifest)
    return status


def _validate_config(config: Row1MarketSpreadTBBOAcquisitionConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 row-1 market-spread TBBO acquisition is not authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S27 v2 row-1 market-spread TBBO acquisition is source-native futures only")
    if config.provider != PROVIDER or config.dataset != DATASET or config.schema != SCHEMA:
        raise CarverBlocked("S27 v2 row-1 market-spread acquisition must use DataBento GLBX.MDP3 TBBO")
    if config.stype_in != STYPE_IN or config.raw_symbol != RAW_SYMBOL:
        raise CarverBlocked("S27 v2 row-1 market-spread acquisition is locked to raw symbol ZNH3")
    if config.fill_timestamp_utc != FILL_TIMESTAMP_UTC:
        raise CarverBlocked("S27 v2 row-1 market-spread acquisition is locked to the audited fill timestamp")
    if config.request_start_utc != REQUEST_START_UTC or config.request_end_utc != REQUEST_END_UTC:
        raise CarverBlocked("S27 v2 row-1 market-spread acquisition window drift")
    if config.broader_test_continuation or config.result_or_pnl_emission:
        raise CarverBlocked("S27 v2 row-1 market-spread acquisition must not continue TEST or emit PnL/results")


def _request_manifest_payload(config: Row1MarketSpreadTBBOAcquisitionConfig) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "run_id": RUN_ID,
        "lane_class": config.lane_class,
        "provider": config.provider,
        "dataset": config.dataset,
        "schema": config.schema,
        "stype_in": config.stype_in,
        "raw_symbol": config.raw_symbol,
        "fill_timestamp_utc": config.fill_timestamp_utc,
        "request_start_utc": config.request_start_utc,
        "request_end_utc": config.request_end_utc,
        "request_count": 1,
        "scope": "BOUNDED_ROW1_MARKET_ORDER_SPREAD_EVIDENCE_ONLY",
        "broader_test_continuation": "NO",
        "validation_oos_lockbox_forward_access": "NO",
        "cost_pnl_result_emission": "NO",
        "source_faithful_evidence_claim": "NO",
    }


def _normalise_tbbo_rows(df: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if df is None or len(df) == 0:
        return rows
    reset = df.reset_index()
    for _, row in reset.iterrows():
        row_dict = {str(k): row[k] for k in reset.columns}
        bid_px = _first_present(row_dict, ("bid_px_00", "bid_px_0", "bid_px"))
        ask_px = _first_present(row_dict, ("ask_px_00", "ask_px_0", "ask_px"))
        bid_sz = _first_present(row_dict, ("bid_sz_00", "bid_sz_0", "bid_sz"))
        ask_sz = _first_present(row_dict, ("ask_sz_00", "ask_sz_0", "ask_sz"))
        ts_event = _string_timestamp(_first_present(row_dict, ("ts_event", "ts_recv", "index")))
        instrument_id = str(_first_present(row_dict, ("instrument_id",)))
        publisher_id = str(_first_present(row_dict, ("publisher_id",)))
        bid = _float_or_none(bid_px)
        ask = _float_or_none(ask_px)
        rows.append(
            {
                "ts_event": ts_event,
                "instrument_id": instrument_id,
                "publisher_id": publisher_id,
                "raw_symbol": RAW_SYMBOL,
                "bid_px_00": bid,
                "ask_px_00": ask,
                "bid_sz_00": _float_or_none(bid_sz),
                "ask_sz_00": _float_or_none(ask_sz),
                "spread_points": None if bid is None or ask is None else ask - bid,
                "provider_condition_status": _quote_condition_status(bid, ask),
            }
        )
    return rows


def _select_latest_non_crossed_quote_at_or_before_fill(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    fill_time = _parse_z(FILL_TIMESTAMP_UTC)
    eligible = []
    for row in rows:
        try:
            ts_event = _parse_z(str(row["ts_event"]))
        except ValueError:
            continue
        if ts_event <= fill_time and row["provider_condition_status"] == "PASS_NON_CROSSED_POSITIVE_TBBO_QUOTE":
            eligible.append((ts_event, row))
    if not eligible:
        return None
    return sorted(eligible, key=lambda item: item[0])[-1][1]


def _provider_condition_rows(
    quote_rows: list[dict[str, Any]],
    provider_errors: list[dict[str, str]],
    selected_row: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if provider_errors:
        return [
            {
                "provider": PROVIDER,
                "dataset": DATASET,
                "schema": SCHEMA,
                "raw_symbol": RAW_SYMBOL,
                "fill_timestamp_utc": FILL_TIMESTAMP_UTC,
                "request_start_utc": REQUEST_START_UTC,
                "request_end_utc": REQUEST_END_UTC,
                "quote_rows_returned": len(quote_rows),
                "selected_quote_ts_event": "",
                "provider_condition_status": "FAIL_CLOSED_PROVIDER_ERROR_NO_SPREAD_LOCK",
                "provider_error_count": len(provider_errors),
                "provider_error_summary": "; ".join(f"{e['error_type']}: {e['message']}" for e in provider_errors),
            }
        ]
    if selected_row is None:
        return [
            {
                "provider": PROVIDER,
                "dataset": DATASET,
                "schema": SCHEMA,
                "raw_symbol": RAW_SYMBOL,
                "fill_timestamp_utc": FILL_TIMESTAMP_UTC,
                "request_start_utc": REQUEST_START_UTC,
                "request_end_utc": REQUEST_END_UTC,
                "quote_rows_returned": len(quote_rows),
                "selected_quote_ts_event": "",
                "provider_condition_status": "FAIL_CLOSED_NO_NON_CROSSED_QUOTE_AT_OR_BEFORE_FILL",
                "provider_error_count": 0,
                "provider_error_summary": "",
            }
        ]
    return [
        {
            "provider": PROVIDER,
            "dataset": DATASET,
            "schema": SCHEMA,
            "raw_symbol": RAW_SYMBOL,
            "fill_timestamp_utc": FILL_TIMESTAMP_UTC,
            "request_start_utc": REQUEST_START_UTC,
            "request_end_utc": REQUEST_END_UTC,
            "quote_rows_returned": len(quote_rows),
            "selected_quote_ts_event": selected_row["ts_event"],
            "provider_condition_status": "PASS_SELECTED_TBBO_QUOTE_AT_OR_BEFORE_FILL",
            "provider_error_count": 0,
            "provider_error_summary": "",
        }
    ]


def _selected_spread_rows(selected_row: dict[str, Any] | None) -> list[dict[str, Any]]:
    if selected_row is None:
        return []
    spread_points = float(selected_row["spread_points"])
    spread_cost_per_contract = spread_points * POINT_VALUE_USD
    row = {
        "row_index": 1,
        "fill_timestamp_utc": FILL_TIMESTAMP_UTC,
        "raw_symbol": RAW_SYMBOL,
        "selected_quote_ts_event": selected_row["ts_event"],
        "bid_px_00": selected_row["bid_px_00"],
        "ask_px_00": selected_row["ask_px_00"],
        "spread_points": spread_points,
        "point_value_usd": POINT_VALUE_USD,
        "spread_cost_usd_per_contract": spread_cost_per_contract,
        "fill_quantity": 2,
        "spread_cost_amount_usd": spread_cost_per_contract * 2,
        "spread_source": "DATABENTO_TBBO_SELECTED_QUOTE_AT_OR_BEFORE_MARKET_FILL",
        "cost_classification": "SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_NOT_BOOK_EXPLICIT",
        "actual_cost_emission_authorized": "FALSE",
        "pnl_result_emission_authorized": "FALSE",
    }
    row["row_hash"] = _hash_dict(row)
    return [row]


def _status_payload(
    quote_rows: list[dict[str, Any]],
    provider_errors: list[dict[str, str]],
    selected_row: dict[str, Any] | None,
) -> dict[str, Any]:
    selected = _selected_spread_rows(selected_row)
    status = (
        "PASS_BOUNDED_DATABENTO_TBBO_SPREAD_EVIDENCE_SELECTED_NOT_COST_EMISSION"
        if selected_row is not None and not provider_errors
        else "FAIL_CLOSED_BOUNDED_DATABENTO_TBBO_SPREAD_EVIDENCE_NOT_SELECTED"
    )
    payload: dict[str, Any] = {
        "authorization": AUTHORIZATION,
        "run_id": RUN_ID,
        "status": status,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "raw_symbol": RAW_SYMBOL,
        "fill_timestamp_utc": FILL_TIMESTAMP_UTC,
        "request_start_utc": REQUEST_START_UTC,
        "request_end_utc": REQUEST_END_UTC,
        "quote_rows_returned": len(quote_rows),
        "provider_errors": provider_errors,
        "request_count": 1,
        "raw_dbn_sha256": _sha256(OUTPUT_ROOT / "raw_provider_output" / f"{RUN_ID}.dbn")
        if (OUTPUT_ROOT / "raw_provider_output" / f"{RUN_ID}.dbn").exists()
        else "",
        "raw_csv_sha256": _sha256(OUTPUT_ROOT / "raw_provider_output" / f"{RUN_ID}_tbbo_dataframe.csv")
        if (OUTPUT_ROOT / "raw_provider_output" / f"{RUN_ID}_tbbo_dataframe.csv").exists()
        else "",
        "actual_cost_emission_authorized": False,
        "actual_pnl_result_emission_authorized": False,
        "source_faithful_evidence_claim": False,
    }
    if selected:
        payload.update(selected[0])
    return payload


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27_V2 2023 TEST Row-1 ZNH3 Market-Order Spread TBBO Provenance

Status:

```text
{status["status"]}
```

This is one bounded DataBento Historical `tbbo` request for ZNH3 around the audited row-1 market-fill timestamp `2023-01-03T01:00:00Z`.

The DataBento key was read from local credential storage and is not written to artifacts.

This artifact does not authorize broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, backtests, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.
"""


def _process_record(status: dict[str, Any]) -> str:
    if status["status"].startswith("PASS_"):
        evidence = f"""Selected TBBO spread evidence:

```text
selected_quote_ts_event = {status["selected_quote_ts_event"]}
bid_px_00 = {status["bid_px_00"]}
ask_px_00 = {status["ask_px_00"]}
spread_points = {status["spread_points"]}
point_value_usd = {status["point_value_usd"]}
spread_cost_usd_per_contract = {status["spread_cost_usd_per_contract"]}
fill_quantity = {status["fill_quantity"]}
spread_cost_amount_usd = {status["spread_cost_amount_usd"]}
row_hash = {status["row_hash"]}
```
"""
    else:
        evidence = "No accepted non-crossed TBBO quote was selected; market spread remains fail-closed.\n"
    return f"""# CARVER S27 ZN V2 2023 TEST Row-1 Market Spread DataBento TBBO Evidence

Date: 2026-06-12

Status:

```text
{status["status"]}
```

Authorization:

```text
{AUTHORIZATION}
```

Request:

```text
provider = {PROVIDER}
dataset = {DATASET}
schema = {SCHEMA}
stype_in = {STYPE_IN}
raw_symbol = {RAW_SYMBOL}
request_start_utc = {REQUEST_START_UTC}
request_end_utc = {REQUEST_END_UTC}
fill_timestamp_utc = {FILL_TIMESTAMP_UTC}
request_count = 1
```

{evidence}
Raw provider evidence:

```text
raw_dbn_sha256 = {status.get("raw_dbn_sha256", "")}
raw_csv_sha256 = {status.get("raw_csv_sha256", "")}
quote_rows_returned = {status.get("quote_rows_returned", 0)}
```

Boundary:

This is provider bid/ask spread evidence only. It is not book-explicit authority, not actual cost emission, not PnL, not a result, not a backtest, not result interpretation, not PnL evaluation, and not a source-faithful evidence claim.
"""


def _ensure_output_dirs() -> None:
    for child in ("raw_provider_output", "manifest", "provider_condition", "ledger", "status", "provenance", "hashes"):
        (OUTPUT_ROOT / child).mkdir(parents=True, exist_ok=True)


def _read_databento_key() -> str:
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if env_key:
        return env_key
    for path in KEY_CANDIDATES:
        if path and path.exists():
            key = path.read_text(encoding="utf-8").strip()
            if key:
                return key
    raise CarverBlocked("DataBento key not found in local credential storage")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        fieldnames = list(rows[0].keys())
    else:
        fieldnames = [
            "row_index",
            "fill_timestamp_utc",
            "raw_symbol",
            "selected_quote_ts_event",
            "bid_px_00",
            "ask_px_00",
            "spread_points",
            "point_value_usd",
            "spread_cost_usd_per_contract",
            "fill_quantity",
            "spread_cost_amount_usd",
            "spread_source",
            "cost_classification",
            "actual_cost_emission_authorized",
            "pnl_result_emission_authorized",
            "row_hash",
        ]
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_sha256_manifest(path: Path) -> None:
    rows = [
        {"relative_path": str(file.relative_to(OUTPUT_ROOT)).replace("\\", "/"), "sha256": _sha256(file)}
        for file in sorted(OUTPUT_ROOT.rglob("*"))
        if file.is_file() and file != path
    ]
    _write_csv(path, rows)


def _hash_dict(row: dict[str, Any]) -> str:
    canonical = json.dumps(row, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _quote_condition_status(bid: float | None, ask: float | None) -> str:
    if bid is None or ask is None:
        return "FAIL_CLOSED_MISSING_BID_OR_ASK"
    if bid <= 0.0 or ask <= 0.0:
        return "FAIL_CLOSED_NON_POSITIVE_BID_OR_ASK"
    if ask < bid:
        return "FAIL_CLOSED_CROSSED_TBBO_QUOTE"
    if ask == bid:
        return "FAIL_CLOSED_ZERO_SPREAD_TBBO_QUOTE"
    return "PASS_NON_CROSSED_POSITIVE_TBBO_QUOTE"


def _parse_z(value: str) -> datetime:
    value = value.replace("+00:00", "Z")
    if value.endswith("Z"):
        return datetime.fromisoformat(value[:-1] + "+00:00").astimezone(timezone.utc)
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def _string_timestamp(value: Any) -> str:
    if hasattr(value, "to_pydatetime"):
        value = value.to_pydatetime()
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    text = str(value)
    if text.endswith("+00:00"):
        return text[:-6] + "Z"
    return text


def _first_present(row: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        if name in row:
            return row[name]
    return ""


def _float_or_none(value: Any) -> float | None:
    try:
        if value == "":
            return None
        result = float(value)
    except (TypeError, ValueError):
        return None
    if result != result or result in (float("inf"), float("-inf")):
        return None
    return result


if __name__ == "__main__":
    main()

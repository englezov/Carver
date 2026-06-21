from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
TOOLS = ROOT / "tools/databento"
for path in (SRC, TOOLS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from carver.spine.m0 import CarverBlocked  # noqa: E402
from carver.spine.s27_v2_replay.local_replay import canonical_sha256  # noqa: E402
from carver_s27_v2_2023_test_market_order_tbbo_batch_acquisition import (  # noqa: E402
    POINT_VALUE_USD,
    _csv_value,
    _rel,
    _sha256,
    _write_csv,
    _write_json,
    _write_sha256_manifest,
)


RUN_ID = "20260616_S27_V2_2023_TEST_ROW1356_POST_FILL_TBBO_ENGINEERING"
AUTHORIZATION = "S27_V2_2023_TEST_ROW1356_POST_FILL_TBBO_ENGINEERING_CONVENTION_IMPLEMENTATION_AND_CONTINUATION_GATE"
ROW_INDEX = "1356"
RAW_SYMBOL = "ZNM3"
FILL_TIMESTAMP_UTC = "2023-03-30T00:00:00Z"
SELECTED_QUOTE_TS_EVENT = "2023-03-30T00:00:00.099806785Z"
QUOTE_LAG_SECONDS = "0.099806785"
BID_PX = "114.484375"
ASK_PX = "114.5"
ORDER_SIDE = "SELL"
FILL_QUANTITY = "2"
EVIDENCE_LABEL = "ROW1356_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
SELECTION_STATUS = "PASS_ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_QUOTE_SELECTED_NOT_RESULT"
SELECTION_RULE = EVIDENCE_LABEL
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260616_2023_test_row1356_post_fill_tbbo_engineering_convention"
)
STRICT_EVIDENCE_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260616_2023_test_row1356_market_order_tbbo"
)
POLICY_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW1356_TBBO_POLICY_DECISION_2026-06-16.md"
)
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW1356_POST_FILL_TBBO_ENGINEERING_BINDING_2026-06-16.md"
)


@dataclass(frozen=True)
class Row1356EngineeringBindingConfig:
    execution_authorized: bool
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = bind_row1356_engineering_convention(Row1356EngineeringBindingConfig(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")


def bind_row1356_engineering_convention(config: Row1356EngineeringBindingConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    raw_dbn, raw_csv = _strict_raw_paths()
    raw_row = _selected_raw_quote(raw_csv)

    selected_row = _selected_spread_row(raw_row, raw_dbn, raw_csv)
    provider_condition = _provider_condition_row(raw_row)
    raw_output = {
        "row_index": ROW_INDEX,
        "raw_dbn_relative_path": _rel(raw_dbn),
        "raw_dbn_sha256": _sha256(raw_dbn),
        "raw_csv_relative_path": _rel(raw_csv),
        "raw_csv_sha256": _sha256(raw_csv),
        "source_strict_evidence_root": _rel(STRICT_EVIDENCE_ROOT),
        "source_strict_evidence_status": "FAIL_CLOSED_ROW1356_BOUNDED_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT",
    }

    selected_path = config.output_root / "ledger" / f"{RUN_ID}_selected_spread_registry.csv"
    provider_path = config.output_root / "provider_condition" / f"{RUN_ID}_provider_condition_ledger.csv"
    raw_path = config.output_root / "raw_provider_output" / f"{RUN_ID}_raw_output_registry.csv"
    status_path = config.output_root / "status" / f"{RUN_ID}_status.json"
    provenance_path = config.output_root / "provenance" / f"{RUN_ID}_provenance.md"
    sha_path = config.output_root / "hashes" / f"{RUN_ID}_sha256.csv"

    _write_csv(selected_path, [selected_row])
    _write_csv(provider_path, [provider_condition])
    _write_csv(raw_path, [raw_output])
    status = _status_payload(selected_row, provider_condition)
    _write_json(config.output_root / "manifest" / f"{RUN_ID}_request_manifest.json", _manifest(selected_row))
    _write_json(status_path, status)
    provenance_path.write_text(_provenance_text(status), encoding="ascii")
    PROCESS_RECORD.write_text(_process_record(status), encoding="ascii")
    _write_sha256_manifest(sha_path, config.output_root)
    return status


def _validate_config(config: Row1356EngineeringBindingConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST row 1356 engineering TBBO binding is not authorized")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST row 1356 engineering TBBO binding output root is locked")
    if not POLICY_RECORD.exists():
        raise CarverBlocked("S27 v2 TEST row 1356 TBBO policy decision record is missing")
    text = POLICY_RECORD.read_text(encoding="ascii")
    if EVIDENCE_LABEL not in text:
        raise CarverBlocked("S27 v2 TEST row 1356 policy record must authorize exact engineering label")


def _strict_raw_paths() -> tuple[Path, Path]:
    raw_registry = (
        STRICT_EVIDENCE_ROOT
        / "raw_provider_output/20260616_S27_V2_2023_TEST_ROW1356_MARKET_ORDER_TBBO_raw_output_registry.csv"
    )
    rows = _read_csv(raw_registry)
    if len(rows) != 1 or rows[0]["row_index"] != ROW_INDEX:
        raise CarverBlocked("S27 v2 TEST row 1356 strict raw registry must contain exactly one row")
    raw_dbn = ROOT / rows[0]["raw_dbn_relative_path"]
    raw_csv = ROOT / rows[0]["raw_csv_relative_path"]
    if _sha256(raw_dbn).upper() != rows[0]["raw_dbn_sha256"].upper():
        raise CarverBlocked("S27 v2 TEST row 1356 strict raw DBN hash drift")
    if _sha256(raw_csv).upper() != rows[0]["raw_csv_sha256"].upper():
        raise CarverBlocked("S27 v2 TEST row 1356 strict raw CSV hash drift")
    return raw_dbn, raw_csv


def _selected_raw_quote(raw_csv: Path) -> dict[str, str]:
    rows = _read_csv(raw_csv)
    matches = [row for row in rows if _normalise_ts(row["ts_event"]) == SELECTED_QUOTE_TS_EVENT]
    if len(matches) != 1:
        raise CarverBlocked("S27 v2 TEST row 1356 selected post-fill raw quote must be present exactly once")
    row = matches[0]
    if row.get("symbol") != RAW_SYMBOL:
        raise CarverBlocked("S27 v2 TEST row 1356 selected raw quote symbol drift")
    if row.get("bid_px_00") != BID_PX or row.get("ask_px_00") != ASK_PX:
        raise CarverBlocked("S27 v2 TEST row 1356 selected raw quote bid/ask drift")
    if row.get("bid_sz_00") != "56" or row.get("ask_sz_00") != "468":
        raise CarverBlocked("S27 v2 TEST row 1356 selected raw quote size drift")
    if abs(_quote_lag_seconds_decimal(row["ts_event"]) - Decimal(QUOTE_LAG_SECONDS)) > Decimal("0.000000001"):
        raise CarverBlocked("S27 v2 TEST row 1356 selected raw quote lag drift")
    bid = float(row["bid_px_00"])
    ask = float(row["ask_px_00"])
    if bid <= 0.0 or ask <= 0.0 or ask < bid:
        raise CarverBlocked("S27 v2 TEST row 1356 selected raw quote must be positive and non-crossed")
    return row


def _selected_spread_row(raw_row: dict[str, str], raw_dbn: Path, raw_csv: Path) -> dict[str, Any]:
    bid = float(raw_row["bid_px_00"])
    ask = float(raw_row["ask_px_00"])
    spread = ask - bid
    row = {
        "row_index": ROW_INDEX,
        "decision_timestamp_utc": "2023-03-29T23:00:00Z",
        "fill_timestamp_utc": FILL_TIMESTAMP_UTC,
        "raw_symbol": RAW_SYMBOL,
        "market_order_side": ORDER_SIDE,
        "fill_quantity": FILL_QUANTITY,
        "selected_quote_ts_event": SELECTED_QUOTE_TS_EVENT,
        "quote_age_seconds": QUOTE_LAG_SECONDS,
        "bid_px_00": BID_PX,
        "ask_px_00": ASK_PX,
        "selected_executable_market_fill_price": BID_PX,
        "executable_market_fill_price_source": "BID_PRICE_FOR_SELL_MARKET_ORDER_FROM_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION",
        "spread_points": spread,
        "point_value_usd": POINT_VALUE_USD,
        "spread_cost_usd_per_contract": spread * POINT_VALUE_USD,
        "spread_cost_amount_usd": spread * POINT_VALUE_USD * abs(int(FILL_QUANTITY)),
        "spread_source": EVIDENCE_LABEL,
        "cost_classification": "SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT",
        "actual_cost_emission_authorized": "FALSE",
        "pnl_result_emission_authorized": "FALSE",
        "raw_dbn_sha256": _sha256(raw_dbn),
        "raw_csv_sha256": _sha256(raw_csv),
        "selection_status": SELECTION_STATUS,
        "selection_rule": SELECTION_RULE,
        "post_fill_quote_selection": EVIDENCE_LABEL,
        "policy_record_relative_path": _rel(POLICY_RECORD),
        "policy_record_sha256": _sha256(POLICY_RECORD),
    }
    row["row_hash"] = canonical_sha256({key: _csv_value(value) for key, value in row.items()})
    return row


def _provider_condition_row(raw_row: dict[str, str]) -> dict[str, Any]:
    row = {
        "row_index": ROW_INDEX,
        "fill_candidate_timestamp_utc": FILL_TIMESTAMP_UTC,
        "request_start_utc": "2023-03-29T23:59:55Z",
        "request_end_utc": "2023-03-30T00:00:05Z",
        "raw_symbol": RAW_SYMBOL,
        "order_side": ORDER_SIDE,
        "quote_rows_returned": "2",
        "selected_quote_ts_event": SELECTED_QUOTE_TS_EVENT,
        "quote_age_seconds": QUOTE_LAG_SECONDS,
        "provider_condition_status": "PASS_ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_QUOTE_SELECTED_NOT_RESULT",
        "provider_error_count": "0",
        "provider_error_summary": "",
        "source_raw_sequence": raw_row["sequence"],
    }
    row["row_hash"] = canonical_sha256({key: _csv_value(value) for key, value in row.items()})
    return row


def _manifest(selected_row: dict[str, Any]) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "run_id": RUN_ID,
        "row_index": ROW_INDEX,
        "raw_symbol": RAW_SYMBOL,
        "policy_record": _rel(POLICY_RECORD),
        "policy_record_sha256": _sha256(POLICY_RECORD),
        "strict_evidence_root": _rel(STRICT_EVIDENCE_ROOT),
        "strict_evidence_status": "FAIL_CLOSED_ROW1356_BOUNDED_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT",
        "selected_quote_ts_event": SELECTED_QUOTE_TS_EVENT,
        "selected_spread_row_hash": selected_row["row_hash"],
        "evidence_label": EVIDENCE_LABEL,
        "provider_api_access": "NO",
        "downloads_or_new_data": "NO",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
    }


def _status_payload(selected_row: dict[str, Any], provider_condition: dict[str, Any]) -> dict[str, Any]:
    return {
        "authorization": AUTHORIZATION,
        "status": "PASS_ROW1356_POST_FILL_TBBO_ENGINEERING_CONVENTION_BOUND_NOT_RESULT",
        "row_index": ROW_INDEX,
        "selected_row_count": 1,
        "selected_quote_ts_event": selected_row["selected_quote_ts_event"],
        "quote_lag_seconds": selected_row["quote_age_seconds"],
        "bid_px_00": selected_row["bid_px_00"],
        "ask_px_00": selected_row["ask_px_00"],
        "selected_executable_market_fill_price": selected_row["selected_executable_market_fill_price"],
        "selection_status": selected_row["selection_status"],
        "provider_condition_status": provider_condition["provider_condition_status"],
        "provider_api_access": "NO",
        "downloads_or_new_data": "NO",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 1356 Post-Fill TBBO Engineering Binding

Status:

```text
{status['status']}
```

This binding consumes already-acquired row-1356 TBBO bytes and the row-specific policy decision. It performs no provider/API access and no new data acquisition.

Selected quote: {status['selected_quote_ts_event']}
Bid: {status['bid_px_00']}
Ask: {status['ask_px_00']}
Quote lag seconds: {status['quote_lag_seconds']}
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST Row 1356 Post-Fill TBBO Engineering Binding

Date: 2026-06-16

Status:

```text
{status['status']}
```

## Bound Evidence

```text
row_index: {status['row_index']}
selected_quote_ts_event: {status['selected_quote_ts_event']}
quote_lag_seconds: {status['quote_lag_seconds']}
bid_px_00: {status['bid_px_00']}
ask_px_00: {status['ask_px_00']}
selected_executable_market_fill_price: {status['selected_executable_market_fill_price']}
selection_status: {status['selection_status']}
provider_condition_status: {status['provider_condition_status']}
```

## Label

```text
{EVIDENCE_LABEL}
```

This is a row-specific local-only engineering convention. It is not book-explicit, not source-faithful evidence, not result interpretation, and not a backtest/result claim.

No provider/API access, downloads, new data, protected-window access, Git action, GPT packet preparation, tuning, adapter/deployment/trading/promotion, or source-faithful evidence claim was authorized or performed by this binding record.
"""


def _ensure_output_dirs(root: Path) -> None:
    for child in ("ledger", "provider_condition", "raw_provider_output", "manifest", "status", "provenance", "hashes"):
        (root / child).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _normalise_ts(value: str) -> str:
    text = str(value).strip().replace(" ", "T")
    if text.endswith("+00:00"):
        text = text[: -len("+00:00")] + "Z"
    return text


def _quote_lag_seconds(value: str) -> float:
    return (_parse_ts(value) - _parse_ts(FILL_TIMESTAMP_UTC)).total_seconds()


def _quote_lag_seconds_decimal(value: str) -> Decimal:
    quote_seconds = _timestamp_epoch_seconds_decimal(value)
    fill_seconds = _timestamp_epoch_seconds_decimal(FILL_TIMESTAMP_UTC)
    return quote_seconds - fill_seconds


def _timestamp_epoch_seconds_decimal(value: str) -> Decimal:
    text = str(value).strip().replace(" ", "T")
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    if text.endswith("+00:00"):
        base = text[: -len("+00:00")]
    else:
        base = text
    date_part, time_part = base.split("T", 1)
    if "." in time_part:
        whole_time, fractional = time_part.split(".", 1)
    else:
        whole_time, fractional = time_part, "0"
    whole_dt = datetime.fromisoformat(f"{date_part}T{whole_time}+00:00").astimezone(timezone.utc)
    return Decimal(str(int(whole_dt.timestamp()))) + (Decimal(f"0.{fractional}") if fractional else Decimal("0"))


def _parse_ts(value: str) -> datetime:
    text = str(value).strip().replace(" ", "T")
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


if __name__ == "__main__":
    main()

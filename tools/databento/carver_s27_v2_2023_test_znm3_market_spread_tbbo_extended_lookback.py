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


RUN_ID = "20260614_S27_V2_2023_TEST_ZNM3_MARKET_ORDER_TBBO_EXTENDED_LOOKBACK"
AUTHORIZATION = "S27_V2_2023_TEST_ZNM3_EXTENDED_LOOKBACK_TBBO_EVIDENCE_AND_CONTINUATION_GATE"
AUTHORIZED_ROW_INDICES = ("702", "703", "704", "708", "829")
LOOKBACK_SECONDS = 300
LOOKAHEAD_SECONDS = 5
MAX_SELECTED_QUOTE_AGE_SECONDS = 300.0
EXTENDED_LOOKBACK_LABEL = "ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
PASS_STATUS = "PASS_ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    / "20260614_2023_test_znm3_market_order_tbbo_extended_lookback"
)
POLICY_RECORD = ROOT / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ZNM3_EMPTY_TBBO_POLICY_DECISION_2026-06-14.md"
PROCESS_RECORD = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_2023_TEST_ZNM3_MARKET_ORDER_TBBO_EXTENDED_LOOKBACK_EVIDENCE_2026-06-14.md"
)


@dataclass(frozen=True)
class ZNM3ExtendedTBBOConfig:
    execution_authorized: bool
    requirements_ledger: Path = REQUIREMENTS_LEDGER
    output_root: Path = OUTPUT_ROOT


def main() -> None:
    status = run_znm3_extended_tbbo_acquisition(ZNM3ExtendedTBBOConfig(execution_authorized=True))
    print(status["status"])
    print(f"output_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"selected_rows={status['selected_row_count']}")
    print(f"failed_rows={status['failed_row_count']}")
    if status["failed_row_count"]:
        print(f"failed_row_indices={','.join(status['failed_row_indices'])}")


def run_znm3_extended_tbbo_acquisition(config: ZNM3ExtendedTBBOConfig) -> dict[str, Any]:
    _validate_config(config)
    _ensure_output_dirs(config.output_root)
    requirements = _znm3_requirements(config.requirements_ledger)
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
                raise CarverBlocked(f"ZNM3 extended TBBO raw outputs already exist for row {row_index}")
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
                raise RuntimeError(f"Databento returned no ZNM3 extended raw TBBO DBN bytes for row {row_index}")
            df = store.to_df()
            df.to_csv(raw_csv)
            quote_rows = _normalise_tbbo_rows(df, requirement)
            selected_row = _select_latest_non_crossed_quote_at_or_before_fill(quote_rows, requirement)
        except Exception as exc:  # noqa: BLE001 - evidence failures must be ledgered and fail closed.
            provider_errors.append({"error_type": type(exc).__name__, "message": str(exc)})

        selected = _selected_spread_row(requirement, selected_row, raw_dbn, raw_csv, provider_errors)
        if selected_row is not None:
            selected["spread_source"] = EXTENDED_LOOKBACK_LABEL
            selected["cost_classification"] = "SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
            selected["selection_rule"] = "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP"
            selected["post_fill_quote_selection"] = "DISALLOWED_TO_AVOID_LOOKAHEAD"
            selected["selection_status"] = PASS_STATUS
            selected["row_hash"] = canonical_sha256({key: _csv_value(value) for key, value in selected.items() if key != "row_hash"})
        selected_rows.append(selected)
        provider_condition_rows.append(_provider_condition_row(requirement, quote_rows, selected_row, provider_errors))
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

    _write_csv(selected_path, selected_rows)
    _write_csv(provider_path, provider_condition_rows)
    _write_csv(raw_path, raw_output_rows)
    status = _status_payload(requirements, selected_rows, provider_condition_rows)
    _write_json(status_path, status)
    provenance_path.write_text(_provenance_text(status), encoding="ascii")
    PROCESS_RECORD.write_text(_process_record(status), encoding="ascii")
    _write_sha256_manifest(sha_path, config.output_root)
    return status


def _validate_config(config: ZNM3ExtendedTBBOConfig) -> None:
    if not config.execution_authorized:
        raise CarverBlocked("S27 v2 TEST ZNM3 extended TBBO acquisition is not authorized")
    if config.requirements_ledger.resolve() != REQUIREMENTS_LEDGER.resolve():
        raise CarverBlocked("S27 v2 TEST ZNM3 extended TBBO acquisition must use the locked requirements ledger")
    if config.output_root.resolve() != OUTPUT_ROOT.resolve():
        raise CarverBlocked("S27 v2 TEST ZNM3 extended TBBO acquisition output root is locked")
    if not POLICY_RECORD.exists():
        raise CarverBlocked("S27 v2 TEST ZNM3 empty-TBBO policy decision record is missing")


def _znm3_requirements(path: Path) -> list[dict[str, str]]:
    rows_by_index = {row["row_index"]: dict(row) for row in _read_csv(path)}
    requirements: list[dict[str, str]] = []
    expected_by_index = {
        "702": ("2023-02-16T02:00:00Z", "2023-02-16T03:00:00Z", "SELL", "7", "-1", "-8", "-7", "-2"),
        "703": ("2023-02-16T03:00:00Z", "2023-02-16T04:00:00Z", "SELL", "2", "-8", "-10", "-2", "-9"),
        "704": ("2023-02-16T04:00:00Z", "2023-02-16T05:00:00Z", "SELL", "4", "-10", "-14", "-4", "-11"),
        "708": ("2023-02-16T08:00:00Z", "2023-02-16T09:00:00Z", "SELL", "2", "-12", "-14", "-2", "-13"),
        "829": ("2023-02-24T01:00:00Z", "2023-02-24T02:00:00Z", "SELL", "7", "0", "-7", "-7", "-1"),
    }
    for row_index in AUTHORIZED_ROW_INDICES:
        row = rows_by_index.get(row_index)
        if row is None:
            raise CarverBlocked(f"S27 v2 TEST ZNM3 extended TBBO missing requirement row {row_index}")
        expected_decision, expected_fill, expected_side, expected_qty, expected_start, expected_desired, expected_change, expected_adjacent = expected_by_index[row_index]
        expected = {
            "decision_timestamp_utc": expected_decision,
            "fill_candidate_timestamp_utc": expected_fill,
            "raw_symbol": "ZNM3",
            "order_side": expected_side,
            "order_quantity": expected_qty,
            "starting_position_contracts": expected_start,
            "desired_position_contracts": expected_desired,
            "position_change_contracts": expected_change,
            "adjacent_target_position": expected_adjacent,
            "market_order_reason": "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT",
            "tbbo_requirement_status": "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE",
            "provider": PROVIDER,
            "dataset": DATASET,
            "schema": SCHEMA,
            "stype_in": STYPE_IN,
            "result_interpretation_authorized": "FALSE",
            "source_faithful_evidence_claimed": "FALSE",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                raise CarverBlocked(f"S27 v2 TEST ZNM3 TBBO requirement drift for row {row_index}: {key}")
        if row["row_hash"] != canonical_sha256({key: value for key, value in row.items() if key != "row_hash"}):
            raise CarverBlocked(f"S27 v2 TEST ZNM3 TBBO requirement row {row_index} hash drift")
        fill_time = _parse_z(row["fill_candidate_timestamp_utc"])
        row["original_request_start_utc"] = row["request_start_utc"]
        row["original_request_end_utc"] = row["request_end_utc"]
        row["request_start_utc"] = _format_z(fill_time - timedelta(seconds=LOOKBACK_SECONDS))
        row["request_end_utc"] = _format_z(fill_time + timedelta(seconds=LOOKAHEAD_SECONDS))
        row["max_selected_quote_age_seconds"] = str(MAX_SELECTED_QUOTE_AGE_SECONDS)
        row["selection_rule"] = "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP"
        row["post_fill_quote_selection"] = "DISALLOWED_TO_AVOID_LOOKAHEAD"
        requirements.append(row)
    return requirements


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


def _request_manifest(requirements: list[dict[str, str]]) -> dict[str, Any]:
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
        "row_indices": [row["row_index"] for row in requirements],
        "raw_symbol": "ZNM3",
        "request_windows": [
            {
                "row_index": row["row_index"],
                "request_start_utc": row["request_start_utc"],
                "request_end_utc": row["request_end_utc"],
            }
            for row in requirements
        ],
        "lookback_seconds": LOOKBACK_SECONDS,
        "lookahead_seconds": LOOKAHEAD_SECONDS,
        "max_selected_quote_age_seconds": MAX_SELECTED_QUOTE_AGE_SECONDS,
        "selection_rule": "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP",
        "post_fill_quote_selection": "DISALLOWED_TO_AVOID_LOOKAHEAD",
        "scope": "FIVE_ROW_ZNM3_ONLY_EXTENDED_LOOKBACK_2023_TEST_MARKET_ORDER_TBBO_REQUIREMENTS",
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
            "PASS_ZNM3_EXTENDED_LOOKBACK_DATABENTO_TBBO_SELECTED_NOT_RESULT"
            if not failed
            else "FAIL_CLOSED_ZNM3_EXTENDED_LOOKBACK_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT"
        ),
        "row_indices": [row["row_index"] for row in requirements],
        "selected_row_count": len(selected_rows) - len(failed),
        "failed_row_count": len(failed),
        "failed_row_indices": [row["row_index"] for row in failed],
        "selected_rows": [
            {
                "row_index": row["row_index"],
                "selected_quote_ts_event": row.get("selected_quote_ts_event", ""),
                "quote_age_seconds": row.get("quote_age_seconds", ""),
                "bid_px_00": row.get("bid_px_00", ""),
                "ask_px_00": row.get("ask_px_00", ""),
                "selection_status": row.get("selection_status", ""),
            }
            for row in selected_rows
            if str(row.get("selection_status", "")).startswith("PASS_")
        ],
        "provider_condition_pass_count": sum(
            1 for row in provider_condition_rows if row["provider_condition_status"] == "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED"
        ),
        "provider_api_access": "FIVE_ROW_ZNM3_BOUNDED_DATABENTO_TBBO_EXTENDED_LOOKBACK",
        "downloads": "FIVE_ROW_ZNM3_BOUNDED_TBBO_WINDOWS_ONLY",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST ZNM3 Extended-Lookback TBBO Evidence Provenance

Status:

```text
{status['status']}
```

Rows: {', '.join(status['row_indices'])}
Selected rows: {status['selected_row_count']}
Failed rows: {status['failed_row_count']}

This evidence acquisition is limited to the five authorized ZNM3 rows and does not authorize broader provider/API access, general downloads, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
"""


def _process_record(status: dict[str, Any]) -> str:
    return f"""# S27 V2 2023 TEST ZNM3 Market-Order TBBO Extended-Lookback Evidence

Date: 2026-06-14

Status:

```text
{status['status']}
```

This process record was written by the five-row ZNM3-only bounded DataBento TBBO extended-lookback evidence acquisition tool.

Rows:

```text
{', '.join(status['row_indices'])}
```

Selected row count: `{status['selected_row_count']}`
Failed row count: `{status['failed_row_count']}`
Failed rows: `{', '.join(status['failed_row_indices'])}`

Engineering label if quote age exceeds the prior 60-second retry policy:

```text
{EXTENDED_LOOKBACK_LABEL}
```

Selected rows:

```json
{json.dumps(status['selected_rows'], indent=2, sort_keys=True)}
```

This evidence gate does not authorize broader TEST continuation beyond a separate mechanical continuation step, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
"""


def _ensure_output_dirs(root: Path) -> None:
    for folder in ("raw_provider_output", "manifest", "provider_condition", "ledger", "status", "provenance", "hashes"):
        (root / folder).mkdir(parents=True, exist_ok=True)


def _format_z(value: Any) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    main()

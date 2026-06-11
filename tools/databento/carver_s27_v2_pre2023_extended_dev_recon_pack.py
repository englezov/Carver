from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PACK = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_oldest_dev_recon_2022_declared_pack"
)
SOURCE_LEDGER = (
    ROOT
    / "docs/researchops/s27_v2_databento_older_zn_history/"
    "20260611_pre2023_zn_dev_recon_download_build/ledger/"
    "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_strategy_facing_hourly_available_bars.csv"
)
OUTPUT_PACK = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_extended_dev_recon_2022_minimum_extended_declared_pack"
)
PROCESS_DOC = ROOT / "docs/process/CARVER_S27_ZN_V2_PRE2023_EXTENDED_DEV_RECON_PACK_BUILD_RESULT_2026-06-11.md"

AUTHORIZATION = "S27_V2_CONSOLIDATED_LOCAL_ONLY_PRE2023_EXTENDED_DEVELOPMENT_RECON_IMPLEMENTATION_AND_RUN_GATE"
STATUS = "LOCAL_PRE2023_EXTENDED_DEV_RECON_PACK_DECLARED_NOT_RESULT"
VALUATION_CONVENTION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"

DECISION_TIMESTAMPS = (
    "2022-01-03T01:00:00Z",
    "2022-01-03T03:00:00Z",
    "2022-01-03T05:00:00Z",
    "2022-01-03T07:00:00Z",
    "2022-01-04T00:00:00Z",
    "2022-01-04T02:00:00Z",
    "2022-01-04T04:00:00Z",
    "2022-01-04T06:00:00Z",
    "2022-01-04T08:00:00Z",
    "2022-01-04T10:00:00Z",
)
FILL_TIMESTAMPS = (
    "2022-01-03T02:00:00Z",
    "2022-01-03T04:00:00Z",
    "2022-01-03T06:00:00Z",
    "2022-01-03T08:00:00Z",
    "2022-01-04T01:00:00Z",
    "2022-01-04T03:00:00Z",
    "2022-01-04T05:00:00Z",
    "2022-01-04T07:00:00Z",
    "2022-01-04T09:00:00Z",
    "2022-01-04T11:00:00Z",
)
VALUATION_TIMESTAMPS = (
    "2022-01-03T03:00:00Z",
    "2022-01-03T05:00:00Z",
    "2022-01-03T07:00:00Z",
    "2022-01-03T09:00:00Z",
    "2022-01-04T02:00:00Z",
    "2022-01-04T04:00:00Z",
    "2022-01-04T06:00:00Z",
    "2022-01-04T08:00:00Z",
    "2022-01-04T10:00:00Z",
    "2022-01-04T12:00:00Z",
)
COPY_FAMILIES = (
    "daily_continuous_completed_bar.csv",
    "daily_current_contract_completed_bar.csv",
    "roll_calendar.csv",
    "cost_parameter.csv",
)
NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_TEST_ACCESS",
    "NO_VALIDATION_ACCESS",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_RESULT_INTERPRETATION",
    "NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION",
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)


def main() -> None:
    OUTPUT_PACK.mkdir(parents=True, exist_ok=True)
    for filename in COPY_FAMILIES:
        _write_csv(OUTPUT_PACK / filename, _read_csv(SOURCE_PACK / filename))
    hourly = _hourly_by_completed_timestamp()
    _write_csv(OUTPUT_PACK / "hourly_decision_completed_bar.csv", [_hourly_pack_row(hourly[ts], "DECISION", idx) for idx, ts in enumerate(DECISION_TIMESTAMPS, 1)])
    _write_csv(OUTPUT_PACK / "hourly_fill_completed_bar.csv", [_hourly_pack_row(hourly[ts], "FILL", idx) for idx, ts in enumerate(FILL_TIMESTAMPS, 1)])
    _write_csv(OUTPUT_PACK / "valuation_mark_completed_bar.csv", [_valuation_row(hourly[ts], idx) for idx, ts in enumerate(VALUATION_TIMESTAMPS, 1)])
    sessions = {_session_id(ts): _session_row(ts) for ts in DECISION_TIMESTAMPS + FILL_TIMESTAMPS + VALUATION_TIMESTAMPS}
    _write_csv(OUTPUT_PACK / "session_calendar.csv", list(sessions.values()))
    manifest = _manifest(hourly)
    _write_json(OUTPUT_PACK / "S27_V2_PRE2023_EXTENDED_DEV_RECON_DECLARED_INPUT_PACK_MANIFEST.json", manifest)
    _write_sha256s(OUTPUT_PACK / "S27_V2_PRE2023_EXTENDED_DEV_RECON_DECLARED_INPUT_PACK_SHA256SUMS.txt", OUTPUT_PACK)
    PROCESS_DOC.write_text(_process_doc(manifest), encoding="ascii")
    print(STATUS)
    print(f"declared_pack={OUTPUT_PACK.relative_to(ROOT)}")


def _hourly_by_completed_timestamp() -> dict[str, dict[str, str]]:
    rows = {
        row["derived_completed_bar_end_utc"]: row
        for row in _read_csv(SOURCE_LEDGER)
        if row["raw_symbol"] == "ZNH2" and row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
    }
    required = set(DECISION_TIMESTAMPS + FILL_TIMESTAMPS + VALUATION_TIMESTAMPS)
    missing = sorted(required - set(rows))
    if missing:
        raise SystemExit(f"fail closed: missing hourly timestamps {missing}")
    return rows


def _hourly_pack_row(row: dict[str, str], role: str, index: int) -> dict[str, Any]:
    return {
        "row_index": index,
        "completed_timestamp_utc": row["derived_completed_bar_end_utc"],
        "trading_date": row["completed_trading_date"],
        "raw_symbol": row["raw_symbol"],
        "session_id": _session_id(row["derived_completed_bar_end_utc"]),
        "row_locator": f"S27V2_PRE2023_EXTENDED_DEV_RECON_ZN_HOURLY_{role}_{index:04d}_{row['derived_completed_bar_end_utc'].replace('-', '').replace(':', '')}_{row['raw_symbol']}",
        "close_price": row["close"],
        "source_provider_csv": row["source_provider_csv"],
        "source_provider_csv_sha256": row["source_provider_csv_sha256"],
        "source_row_hash": _row_hash("strategy_facing_hourly_available_bars", row),
        "readiness_status": "READY_COMPLETED_BAR_DATABENTO_PRE2023_MULTI_ROW_DEV_RECON",
    }


def _valuation_row(row: dict[str, str], index: int) -> dict[str, Any]:
    packed = _hourly_pack_row(row, "VALUATION_MARK", index)
    return {
        "row_index": packed["row_index"],
        "completed_timestamp_utc": packed["completed_timestamp_utc"],
        "trading_date": packed["trading_date"],
        "raw_symbol": packed["raw_symbol"],
        "session_id": packed["session_id"],
        "row_locator": packed["row_locator"],
        "close_price": packed["close_price"],
        "valuation_convention_label": VALUATION_CONVENTION_LABEL,
        "source_provider_csv": packed["source_provider_csv"],
        "source_provider_csv_sha256": packed["source_provider_csv_sha256"],
        "source_row_hash": packed["source_row_hash"],
        "readiness_status": "READY_COMPLETED_BAR_DATABENTO_PRE2023_MULTI_ROW_VALUATION_MARK_DEV_RECON",
    }


def _session_row(completed_timestamp: str) -> dict[str, str]:
    session_id = _session_id(completed_timestamp)
    start, end = _session_bounds(completed_timestamp)
    return {
        "session_id": session_id,
        "session_start_utc": start,
        "session_end_utc": end,
        "calendar_status": "LOCAL_DATABENTO_PRE2023_COMPLETED_BAR_SESSION_CONTEXT",
        "readiness_status": "READY_SESSION_CONTEXT_DEV_RECON_ONLY",
    }


def _session_id(completed_timestamp: str) -> str:
    start, end = _session_bounds(completed_timestamp)
    return f"UTC_ZN_PRE2023_{start}_{end}"


def _session_bounds(completed_timestamp: str) -> tuple[str, str]:
    if completed_timestamp.startswith("2022-01-03T"):
        return "2022-01-02T22:00:00Z", "2022-01-03T21:00:00Z"
    if completed_timestamp.startswith("2022-01-04T"):
        return "2022-01-03T22:00:00Z", "2022-01-04T21:00:00Z"
    raise SystemExit(f"fail closed: timestamp outside selected extended sessions {completed_timestamp}")


def _manifest(hourly: dict[str, dict[str, str]]) -> dict[str, Any]:
    row_family_files = {
        path.name: {"row_count": _csv_row_count(path), "sha256": _sha256(path)}
        for path in sorted(OUTPUT_PACK.glob("*.csv"))
    }
    decision_fill_mark = []
    for index, (decision_ts, fill_ts, mark_ts) in enumerate(zip(DECISION_TIMESTAMPS, FILL_TIMESTAMPS, VALUATION_TIMESTAMPS, strict=True), 1):
        decision_fill_mark.append(
            {
                "row_index": index,
                "decision_timestamp_utc": decision_ts,
                "fill_timestamp_utc": fill_ts,
                "valuation_mark_timestamp_utc": mark_ts,
                "raw_symbol": "ZNH2",
                "decision_source_row_hash": _row_hash("strategy_facing_hourly_available_bars", hourly[decision_ts]),
                "fill_source_row_hash": _row_hash("strategy_facing_hourly_available_bars", hourly[fill_ts]),
                "valuation_source_row_hash": _row_hash("strategy_facing_hourly_available_bars", hourly[mark_ts]),
                "same_session": "YES",
                "strict_timestamp_order": "YES",
            }
        )
    return {
        "artifact": "S27_V2_PRE2023_EXTENDED_DEV_RECON_DECLARED_INPUT_PACK_MANIFEST",
        "authorization": AUTHORIZATION,
        "status": STATUS,
        "lane": "SOURCE_NATIVE_FUTURES",
        "selected_slice_rule": "MINIMUM_OLDEST_2022_EXTENDED_DEV_RECON_TWO_SESSION_SEGMENT_AFTER_WARMUPS_PRESERVE_2023_FOR_TEST",
        "source_one_row_pack": str(SOURCE_PACK.relative_to(ROOT)),
        "source_hourly_ledger": str(SOURCE_LEDGER.relative_to(ROOT)),
        "decision_fill_mark_plan": decision_fill_mark,
        "row_family_files": row_family_files,
        "history_evidence": {
            "daily_history_status": "COPIED_FROM_LOCALLY_AUDITED_PRE2023_ONE_ROW_PACK",
            "daily_continuous_rows": "64",
            "selected_previous_daily_timestamp_utc": "2021-12-31T00:00:00Z",
            "selected_sigma_percent_t": "0.04668909552506636",
            "selected_vqm_multiplier_m": "0.9047281454440286",
            "point_in_time_roll_cutoff_date": "2021-12-31",
            "future_roll_deltas_after_cutoff_excluded": "YES",
            "working_order_lifecycle_status": "FIRST_ROW_EMPTY_THEN_RUNNER_CARRIES_POSITION_AND_WORKING_STATE",
            "valuation_policy_status": VALUATION_CONVENTION_LABEL,
            "extension_stop_reason": "NEXT_STRICT_TWO_HOUR_DECISION_FILL_MARK_SEQUENCE_BREAKS_AFTER_2022-01-04T10:00:00Z_BECAUSE_2022-01-04T13:00:00Z_IS_MISSING",
        },
        "explicitly_excluded_data": ["NO_2023_TEST_DATA", "NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"],
        "non_authorizations": list(NON_AUTHORIZATIONS),
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"fail closed: empty csv {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _write_sha256s(path: Path, root: Path) -> None:
    lines = [
        f"{_sha256(file)}  {file.relative_to(root).as_posix()}"
        for file in sorted(root.iterdir())
        if file.is_file() and file != path
    ]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def _csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="ascii") as handle:
        return len(list(csv.DictReader(handle)))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _row_hash(label: str, row: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps({"artifact": label, "row": row}, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest().upper()


def _process_doc(manifest: dict[str, Any]) -> str:
    return f"""# S27_V2 Pre-2023 Extended Development/Reconciliation Pack Build Result

Date: 2026-06-11

Status:

```text
{STATUS}
```

Declared pack:

```text
{OUTPUT_PACK.relative_to(ROOT)}
```

This pack is local-only and pre-2023. It selects the minimum oldest 2022 extended
Development/Reconciliation two-session segment after warmups/evidence are
populated: ten decision rows, ten one-hour fill candidates, and ten
next-completed-hourly valuation marks. It preserves 2023 for TEST and does not emit a result,
interpretation, PnL evaluation beyond future mechanical row construction, or
source-faithful evidence claim.

Extension stop reason:

```text
{manifest['history_evidence']['extension_stop_reason']}
```

Non-authorizations:

```text
{chr(10).join(NON_AUTHORIZATIONS)}
```
"""


if __name__ == "__main__":
    main()

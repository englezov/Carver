from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

RUN_ID = "20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR"
INPUT = (
    ROOT
    / "docs"
    / "researchops"
    / "source_native_futures_daily_data_library"
    / "16_SYMBOL_DATED_CONTRACT_ROLL_CHAIN_EXPANSION"
    / "2026-05-30_PREV_CURRENT_NEXT_DEV_RECON_AVAILABLE_END_2026-05-30"
    / "provider_condition_join"
    / "CARVER_16_SYMBOL_DATED_CONTRACT_ROLL_CHAIN_PROVIDER_CONDITION_JOIN_2026-05-30.csv"
)
OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s26_s27_hourly_bridge"
    / "ZN_S27_EWMAC16_TREND_DEPENDENCY"
    / "local_continuous_daily_lineage_2026-05-31"
)

OLD_CONTRACT = "ZNH6"
NEW_CONTRACT = "ZNM6"
ROLL_TRANSITION_DATE = "2026-02-16"
OLD_FIRST_NOTICE_DATE = "2026-02-27"
OLD_FIRST_DELIVERY_DATE = "2026-03-02"
OLD_LAST_TRADE_DATE = "2026-03-20"
OLD_LAST_DELIVERY_DATE = "2026-03-31"
NEW_FIRST_NOTICE_DATE = "2026-05-29"
NEW_FIRST_DELIVERY_DATE = "2026-06-01"
NEW_LAST_TRADE_DATE = "2026-06-18"
NEW_LAST_DELIVERY_DATE = "2026-06-30"


def main() -> None:
    folders = {
        "ledger": OUTPUT_ROOT / "ledger",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    source_rows = _read_rows(INPUT)
    source_sha = _sha256(INPUT)
    zn_rows = _filter_zn_normal_rows(source_rows)

    by_contract_date = {
        (row["provider_symbol"], row["completed_trading_date"]): row
        for row in zn_rows
        if row["provider_symbol"] in (OLD_CONTRACT, NEW_CONTRACT)
    }
    old_roll = by_contract_date.get((OLD_CONTRACT, ROLL_TRANSITION_DATE))
    new_roll = by_contract_date.get((NEW_CONTRACT, ROLL_TRANSITION_DATE))
    if old_roll is None or new_roll is None:
        raise SystemExit("Fail closed: missing old/new normal-provider roll pair")

    old_close = float(old_roll["close"])
    new_close = float(new_roll["close"])
    old_adjustment_offset = new_close - old_close

    lifecycle_rows = _lifecycle_rows()
    roll_plan_rows = [
        {
            "book_symbol": "ZN",
            "product_family": "Treasury rates",
            "lifecycle_class": "physical delivery",
            "roll_rule_class": "STATIC_LIFECYCLE_BUFFER_ROLL",
            "roll_rule_parameters": "physical_delivery_roll_buffer=10_completed_trading_dates_before_earliest_lifecycle_blocker; completed_dates_are_source_completed_trading_dates_from_existing_normal_provider_rows_including_sunday_globex_sessions",
            "old_source_contract": OLD_CONTRACT,
            "new_source_contract": NEW_CONTRACT,
            "roll_transition_date": ROLL_TRANSITION_DATE,
            "earliest_lifecycle_blocker": OLD_FIRST_NOTICE_DATE,
            "buffer_count_source_completed_dates": "10",
            "first_notice_blocker_status": "LOCKED_OFFICIAL_CME_TREASURY_DELIVERY_PROCESS_AND_CBOT_RULEBOOK_CHAPTER_19",
            "last_trade_blocker_status": "LOCKED_OFFICIAL_CBOT_RULEBOOK_CHAPTER_19_AND_JUNETEENTH_HOLIDAY_ADJUSTMENT_FOR_ZNM6",
            "expiration_or_final_settlement_blocker_status": "LOCKED_DATABENTO_DEFINITION_EXPIRATION_CROSS_CHECK_ONLY_NOT_ROLL_SOURCE",
            "provider_condition_policy_status": "NORMAL_PROVIDER_CONDITION_ONLY_ENFORCED_ON_ROLL_CHAIN_EXPANSION; ADJACENT_ROWS_AVAILABLE",
            "roll_plan_status": "ROLL_PLAN_READY_FOR_LOCAL_DEV_RECON_CONSTRUCTION",
            "blocker": "",
        }
    ]
    adjustment_rows = [
        {
            "book_symbol": "ZN",
            "roll_transition_date": ROLL_TRANSITION_DATE,
            "old_source_contract": OLD_CONTRACT,
            "new_source_contract": NEW_CONTRACT,
            "old_contract_roll_date_close": f"{old_close:.10f}",
            "new_contract_roll_date_close": f"{new_close:.10f}",
            "roll_gap_or_offset": f"{old_adjustment_offset:.10f}",
            "adjustment_method": "LOCAL_ADDITIVE_BACK_ADJUSTMENT_OLD_HISTORY_TO_NEW_CONTRACT_LEVEL",
            "adjustment_offset_applied": f"{old_adjustment_offset:.10f}",
            "adjustment_factor_or_offset": f"{old_adjustment_offset:.10f}",
            "adjustment_applies_to_dates_before": ROLL_TRANSITION_DATE,
            "adjusted_close_before_roll": f"{old_close + old_adjustment_offset:.10f}",
            "adjusted_close_after_roll": f"{new_close:.10f}",
            "negative_adjusted_price_flag": "NO",
            "adjustment_policy_status": "ADJUSTMENT_READY_FOR_DEV_RECON_LINEAGE_ONLY",
            "blocker": "",
        }
    ]

    lineage_rows, series_rows = _build_lineage_and_series(zn_rows, source_sha, old_adjustment_offset)
    _assert_no_duplicate_dates(series_rows)

    status_rows = [
        ("execution_status", "PASS_ZN_LOCAL_CONTINUOUS_DAILY_LINEAGE_DEV_RECON_ONLY", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("source_rows_available", str(len(zn_rows)), "ZN_S27_EWMAC16_DEPENDENCY"),
        ("continuous_rows_emitted", str(len(series_rows)), "ZN_S27_EWMAC16_DEPENDENCY"),
        ("roll_transition_date", ROLL_TRANSITION_DATE, "ZN_S27_EWMAC16_DEPENDENCY"),
        ("daily_price_field", "DATABENTO_OHLCV_1D_CLOSE", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("daily_price_semantics", "TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("provider_timestamp_policy", "UTC_MIDNIGHT_PROVIDER_DAILY_BAR_TIMESTAMP_NOT_EXCHANGE_SESSION_END", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("completed_trading_date_policy", "CARRIED_FROM_SOURCE_QUARANTINE_COMPLETED_TRADING_DATE_INCLUDING_SUNDAY_GLOBEX_SESSIONS", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("settlement_policy", "BLOCKED_PENDING_OFFICIAL_SETTLEMENT_SOURCE_GATE", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("strategy_input_created", "NO_DEV_RECON_LINEAGE_ONLY", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("trend_computed", "NO", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("s27_computed", "NO", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("diagnostics_run", "NO", "ZN_S27_EWMAC16_DEPENDENCY"),
        ("backtests_run", "NO", "ZN_S27_EWMAC16_DEPENDENCY"),
    ]

    lifecycle_csv = folders["ledger"] / f"{RUN_ID}_lifecycle_evidence_lock.csv"
    roll_plan_csv = folders["ledger"] / f"{RUN_ID}_roll_plan.csv"
    adjustment_csv = folders["ledger"] / f"{RUN_ID}_adjustment_ledger.csv"
    lineage_csv = folders["ledger"] / f"{RUN_ID}_source_lineage.csv"
    series_csv = folders["ledger"] / f"{RUN_ID}_series_dev_recon_only.csv"
    status_csv = folders["status"] / f"{RUN_ID}_status.csv"
    provenance_json = folders["provenance"] / f"{RUN_ID}_provenance.json"
    hashes_json = folders["hashes"] / f"{RUN_ID}_sha256.json"

    _write_csv(lifecycle_csv, lifecycle_rows)
    _write_csv(roll_plan_csv, roll_plan_rows)
    _write_csv(adjustment_csv, adjustment_rows)
    _write_csv(lineage_csv, lineage_rows)
    _write_csv(series_csv, series_rows)
    _write_status_csv(status_csv, status_rows)
    _write_json(
        provenance_json,
        {
            "run_id": RUN_ID,
            "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "lane_class": "SOURCE_NATIVE_FUTURES",
            "purpose": "ZN local continuous daily lineage repair for the S27 EWMAC16 trend dependency.",
            "input": str(INPUT.relative_to(ROOT)),
            "input_sha256": source_sha,
            "official_static_sources": [
                "https://www.cmegroup.com/content/dam/cmegroup/rulebook/CBOT/II/19.pdf",
                "https://www.cmegroup.com/content/dam/cmegroup/trading/interest-rates/files/us-treasury-futures-delivery-process.pdf",
                "https://www.cmegroup.com/trading-hours.html",
            ],
            "databento_definition_cross_check": "docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/zn_lifecycle_databento_definition_probe_2026-05-31/",
            "roll_transition_date": ROLL_TRANSITION_DATE,
            "boundary": [
                "NO_PROVIDER_API_ACCESS",
                "NO_NEW_DATA_DOWNLOAD",
                "NO_MARKET_ROW_EXPANSION",
                "NO_PROVIDER_BUILT_CONTINUOUS_CONTRACT",
                "NO_TREND_COMPUTATION",
                "NO_S27_COMPUTATION",
                "NO_DIAGNOSTICS",
                "NO_BACKTESTS",
                "NO_POSITIONS",
                "NO_COSTS",
                "NO_CARRY",
                "NO_TRADING",
                "NO_PROMOTION",
            ],
        },
    )

    hashes = {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in (
            lifecycle_csv,
            roll_plan_csv,
            adjustment_csv,
            lineage_csv,
            series_csv,
            status_csv,
            provenance_json,
        )
    }
    _write_json(hashes_json, hashes)

    print("PASS_ZN_LOCAL_CONTINUOUS_DAILY_LINEAGE_DEV_RECON_ONLY")
    print(f"continuous_rows={len(series_rows)}")
    print(f"roll_transition_date={ROLL_TRANSITION_DATE}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _lifecycle_rows() -> list[dict[str, str]]:
    base = {
        "book_symbol": "ZN",
        "product_family": "10-Year U.S. Treasury Note Futures",
        "venue_normalization": "XCBT_CBOT_CME_GROUP",
        "currency": "USD",
        "contract_unit": "100000_USD_FACE_VALUE",
        "lifecycle_class": "PHYSICAL_DELIVERY",
        "official_rulebook_source": "CME_CBOT_RULEBOOK_CHAPTER_19",
        "official_delivery_process_source": "CME_TREASURY_FUTURES_DELIVERY_PROCESS",
        "holiday_source": "CME_GROUP_2026_HOLIDAY_AND_TRADING_HOURS",
        "roll_policy_status": "LOCKED_FOR_ZN_LOCAL_DEV_RECON_LINEAGE_ONLY_NOT_PRODUCTION",
    }
    return [
        {
            **base,
            "source_contract": OLD_CONTRACT,
            "first_notice_date": OLD_FIRST_NOTICE_DATE,
            "first_delivery_date": OLD_FIRST_DELIVERY_DATE,
            "last_trade_date": OLD_LAST_TRADE_DATE,
            "last_delivery_date": OLD_LAST_DELIVERY_DATE,
            "databento_definition_expiration_cross_check": "2026-03-20 17:01:00+00:00",
        },
        {
            **base,
            "source_contract": NEW_CONTRACT,
            "first_notice_date": NEW_FIRST_NOTICE_DATE,
            "first_delivery_date": NEW_FIRST_DELIVERY_DATE,
            "last_trade_date": NEW_LAST_TRADE_DATE,
            "last_delivery_date": NEW_LAST_DELIVERY_DATE,
            "databento_definition_expiration_cross_check": "2026-06-18 17:01:00+00:00",
        },
    ]


def _filter_zn_normal_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    filtered = [
        row
        for row in rows
        if row["book_symbol"] == "ZN"
        and row["provider_symbol"] in (OLD_CONTRACT, NEW_CONTRACT)
        and row["provider_condition_readiness_status"] == "ROW_READY_PROVIDER_CONDITION_NORMAL"
        and row["validation_status"] == "PASS_PROVIDER_ROWS_PRESENT_NO_DUPLICATES_NORMAL_PROVIDER_CONDITION"
        and row["timestamp_policy"] == "PASS_ALL_UTC_MIDNIGHT"
        and row["symbol_roundtrip"] == "PASS_RAW_SYMBOL_MATCH"
    ]
    if not filtered:
        raise SystemExit("Fail closed: no ZN normal provider rows available")
    return sorted(filtered, key=lambda row: (row["completed_trading_date"], row["provider_symbol"]))


def _build_lineage_and_series(rows: list[dict[str, str]], source_sha: str, old_offset: float) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    lineage: list[dict[str, str]] = []
    series: list[dict[str, str]] = []
    for row in rows:
        source_contract = row["provider_symbol"]
        date = row["completed_trading_date"]
        if source_contract == OLD_CONTRACT and date >= ROLL_TRANSITION_DATE:
            continue
        if source_contract == NEW_CONTRACT and date < ROLL_TRANSITION_DATE:
            continue
        offset = old_offset if source_contract == OLD_CONTRACT else 0.0
        adjusted = {
            "adjusted_open": float(row["open"]) + offset,
            "adjusted_high": float(row["high"]) + offset,
            "adjusted_low": float(row["low"]) + offset,
            "adjusted_close": float(row["close"]) + offset,
        }
        common = {
            "foundation_scope": "SOURCE_NATIVE_FUTURES_DAILY_DATA_FOUNDATION",
            "series_label": "ZN_LOCAL_CONTINUOUS_DAILY_LINEAGE_DEV_RECON_ONLY",
            "strategy_use_status": "DEV_RECON_ONLY_NOT_TEST_NOT_VALIDATION_NOT_BACKTEST_READY",
            "book_symbol": "ZN",
            "continuous_row_date": date,
            "continuous_timestamp_utc": row["provider_timestamp_utc"],
            "source_contract": source_contract,
            "source_provider_symbol": row["provider_symbol"],
            "source_instrument_id": row["instrument_id"],
            "source_completed_trading_date": date,
            "daily_price_semantics": "TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT",
            "daily_price_field": "DATABENTO_OHLCV_1D_CLOSE",
            "provider_timestamp_policy": "UTC_MIDNIGHT_PROVIDER_DAILY_BAR_TIMESTAMP_NOT_EXCHANGE_SESSION_END",
            "completed_trading_date_policy": "CARRIED_FROM_SOURCE_QUARANTINE_COMPLETED_TRADING_DATE_INCLUDING_SUNDAY_GLOBEX_SESSIONS",
            "adjustment_method": "LOCAL_ADDITIVE_BACK_ADJUSTMENT_OLD_HISTORY_TO_NEW_CONTRACT_LEVEL",
            "adjustment_factor_or_offset": f"{offset:.10f}",
            "provider_condition_readiness_status": row["provider_condition_readiness_status"],
            "lineage_policy_status": "PASS_ZN_LOCAL_LINEAGE_DEV_RECON_ONLY",
            "settlement_policy": "BLOCKED_PENDING_OFFICIAL_SETTLEMENT_SOURCE_GATE",
            "execution_status": "LOCAL_CONTINUOUS_CONSTRUCTION_DEV_RECON_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_PROMOTION",
        }
        lineage.append(
            {
                **common,
                "source_timestamp_utc": row["provider_timestamp_utc"],
                "source_open": row["open"],
                "source_high": row["high"],
                "source_low": row["low"],
                "source_close": row["close"],
                "source_volume": row["volume"],
                "adjusted_open": f"{adjusted['adjusted_open']:.10f}",
                "adjusted_high": f"{adjusted['adjusted_high']:.10f}",
                "adjusted_low": f"{adjusted['adjusted_low']:.10f}",
                "adjusted_close": f"{adjusted['adjusted_close']:.10f}",
                "source_fragment_table_sha256": source_sha,
                "source_archive_sha256": row["raw_provider_csv_sha256"],
                "roll_policy_status": "ROLL_POLICY_LOCKED_FOR_ZN_DEV_RECON_LINEAGE_ONLY",
            }
        )
        series.append(
            {
                **common,
                "adjusted_open": f"{adjusted['adjusted_open']:.10f}",
                "adjusted_high": f"{adjusted['adjusted_high']:.10f}",
                "adjusted_low": f"{adjusted['adjusted_low']:.10f}",
                "adjusted_close": f"{adjusted['adjusted_close']:.10f}",
            }
        )
    return lineage, series


def _assert_no_duplicate_dates(rows: list[dict[str, str]]) -> None:
    seen: set[str] = set()
    for row in rows:
        date = row["continuous_row_date"]
        if date in seen:
            raise SystemExit(f"Fail closed: duplicate continuous row date {date}")
        seen.add(date)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"Fail closed: no rows for {path.name}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_status_csv(path: Path, rows: list[tuple[str, str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["status_key", "status_value", "status_scope"])
        writer.writeheader()
        for key, value, scope in rows:
            writer.writerow({"status_key": key, "status_value": value, "status_scope": scope})


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


if __name__ == "__main__":
    main()

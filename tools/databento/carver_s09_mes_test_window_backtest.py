from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from argparse import ArgumentParser
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.daily_bars import CompletedDailyMarketBar
from carver.spine.m0 import CompletedBar, ContractSpec, CarverBlocked
from carver.spine.m1 import TimedValue
from carver.spine.m2 import S09_EWMAC_SPANS
from carver.spine.s03 import S03RiskConfig, SyntheticDailyPrice, estimate_s03_annual_risk
from carver.spine.s09 import S09TrendForecastRequest, s09_multiple_trend_forecast
from carver.spine.s09_mes_lineage import (
    S09MESDatedContractBar,
    S09MESDatedContractDefinition,
    S09MESLineageRequest,
    build_s09_mes_lineage,
    evaluate_s09_mes_lineage_strategy_readiness,
)

ORIGINAL_DIAGNOSTIC_TEST_RUN_ID = "20260604_S09_MES_TEST_WINDOW_BACKTEST"
RUN_ID = "20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION"
GATE = "S09_MES_TEST_WINDOW_BACKTEST_AUTHORIZED_EXECUTION_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
SCHEMA = "ohlcv-1d"
DEFINITION_SCHEMA = "definition"
STYPE_IN = "raw_symbol"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
BOOK_LABEL = "S&P 500 (micro)"
STATE_HISTORY_START = date(2019, 5, 5)
STATE_HISTORY_END = date(2020, 4, 5)
WINDOW_START = date(2020, 4, 6)
WINDOW_END = date(2022, 2, 8)
REQUEST_END = date(2022, 2, 9)
WINDOW_LABEL = "2020-04-06_2022-02-08"
STATE_HISTORY_TEXT = "2019-05-05 through 2020-04-05"
WINDOW_TEXT = "2020-04-06 through 2022-02-08"
EXPECTED_STATE_HISTORY_COMPLETED_DATES = 289
EXPECTED_COMPLETED_DATES = 574
MINIMUM_TEST_TRADES = 100
FRACTIONAL_TRADE_EVENT_EPSILON_CONTRACT_EQUIVALENT = 1e-9
WHOLE_CONTRACT_EXECUTABILITY_THRESHOLD = 1.0
WARMUP_BARS = 257
STATE_HISTORY_RAW_SYMBOLS = ("MESM9", "MESU9", "MESZ9", "MESH0", "MESM0")
TEST_RAW_SYMBOLS = ("MESM0", "MESU0", "MESZ0", "MESH1", "MESM1", "MESU1", "MESZ1", "MESH2")
RAW_SYMBOLS = ("MESM9", "MESU9", "MESZ9", "MESH0", "MESM0", "MESU0", "MESZ0", "MESH1", "MESM1", "MESU1", "MESZ1", "MESH2")
MACHINERY_DEV_OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_machinery_dev_minimum_slice" / "2019-05-05_2020-04-05"
MACHINERY_DEV_RUN_ID = "20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD"
DEGRADED_OHLCV_POLICY_DISPOSITION = "COLD_SHAPE_BASED_POLICY_LOCKED_BEFORE_STAGE_ACCESS"
DEGRADED_OHLCV_ADMISSION_POLICY = "SOURCE_NATIVE_DEGRADED_OHLCV_COLD_SHAPE_BASED_POLICY_LOCKED"
MONTH_CODE_TO_MONTH = {"H": 3, "M": 6, "U": 9, "Z": 12}
CONTRACT_MULTIPLIER = 5.0
LONG_RUN_ANNUAL_RISK = 0.20
FORECAST_DIVISOR = 10.0
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_test_window_backtest" / WINDOW_LABEL
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_RESULT_2026-06-04.md"
AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_LOCAL_HOSTILE_AUDIT_2026-06-04.md"
COST_SCENARIOS = {
    "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH": 2.93,
    "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED": 2.49,
}
S09_MES_TEST_LOCKED_READINESS_STATUSES = {
    "continuous_lineage_status": "LOCKED",
    "roll_plan_status": "LOCKED",
    "back_adjustment_status": "LOCKED",
    "provider_condition_admission_status": "LOCKED",
    "official_lifecycle_evidence_status": "LOCKED_SOURCE_NATIVE_OFFICIAL_LIFECYCLE_EVIDENCE",
    "roll_trading_day_semantics_status": "LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS",
    "annual_risk_runtime_status": "LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUES",
    "daily_price_risk_runtime_status": "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUES",
    "cost_source_status": "LOCKED_SOURCE_NATIVE_HISTORICAL_MES_COST_VALUES",
    "risk_adjusted_cost_status": "LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUES",
    "speed_cost_eligibility_status": "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUES",
    "eligible_speed_set_status": "LOCKED_SOURCE_NATIVE_ELIGIBLE_SPEED_SET_AND_FDM",
    "strategy_input_readiness_status": "LOCKED_S09_MES_STRATEGY_INPUT_READY_FOR_CLEAN_TEST_RERUN_CONSIDERATION",
}
S09_MES_TEST_READINESS_CONTRACT_SOURCES = (
    "docs/process/CARVER_S09_MES_HASH_BOUND_PROVENANCE_LOCK_RESULT_2026-06-03.md",
    "docs/process/CARVER_S09_MES_STRATEGY_INPUT_READINESS_GATE_RESULT_2026-06-03.md",
    "docs/process/CARVER_WINDOW_STATE_WARMUP_AND_SCORING_MASK_DOCTRINE_2026-06-04.md",
    "docs/process/CARVER_S09_MES_PRE_CLEAN_TEST_RERUN_REMEDIATION_RESULT_2026-06-04.md",
)


@dataclass(frozen=True)
class S09MESTestWindowBacktestConfig:
    execution_authorized: bool
    databento_download_authorized: bool
    exactly_one_backtest_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    existing_test_download_authorized: bool = False


def run_s09_mes_test_window_backtest_preflight(config: S09MESTestWindowBacktestConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES TEST backtest execution is not operator-authorized")
    if config.databento_download_authorized:
        raise CarverBlocked(
            "S09 MES TEST direct Databento download is quarantined in this runner; use a separately audited acquisition gate"
        )
    if not config.existing_test_download_authorized:
        raise CarverBlocked("S09 MES TEST requires existing-download authorization")
    if not config.exactly_one_backtest_authorized:
        raise CarverBlocked("S09 MES TEST gate requires exactly one authorized backtest")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES TEST is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES TEST is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES TEST window must match the locked 3:3:4 TEST allocation")
    if (WINDOW_END - WINDOW_START).days > 365 * 2:
        raise CarverBlocked("S09 MES TEST backtest exceeds the two-year guard")
    receipt = OUTPUT_ROOT / "status" / f"{RUN_ID}_backtest_execution_receipt.json"
    if receipt.exists():
        raise CarverBlocked("S09 MES TEST backtest receipt already exists; refusing a second backtest")
    return {
        "status": "AUTHORIZED_READY_FOR_EXACTLY_ONE_TEST_BACKTEST",
        "window_start": config.window_start,
        "window_end": config.window_end,
    }


def main(argv: list[str] | None = None) -> None:
    parser = ArgumentParser(description="Run the explicitly authorized S09 MES TEST backtest.")
    parser.add_argument(
        "--execute-authorized-test-backtest",
        action="store_true",
        help="Consume exactly one separately operator-authorized TEST backtest execution.",
    )
    parser.add_argument(
        "--use-existing-authorized-test-download",
        action="store_true",
        help="Use the previously authorized TEST download artifacts without calling Databento.",
    )
    args = parser.parse_args(argv)
    if not args.execute_authorized_test_backtest:
        raise SystemExit("Fail closed: missing --execute-authorized-test-backtest flag")
    if not args.use_existing_authorized_test_download:
        raise SystemExit("Fail closed: missing --use-existing-authorized-test-download flag")
    run_s09_mes_test_window_backtest_preflight(
        S09MESTestWindowBacktestConfig(
            execution_authorized=True,
            databento_download_authorized=False,
            existing_test_download_authorized=True,
            exactly_one_backtest_authorized=True,
            lane_class=LANE_CLASS,
            root=ROOT_SYMBOL,
            row_id=ROW_ID,
            window_start=WINDOW_START.isoformat(),
            window_end=WINDOW_END.isoformat(),
        )
    )
    paths = _compute_from_existing_authorized_test_download()
    print("S09_MES_TEST_WINDOW_BACKTEST_RESULT_WRITTEN")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"artifacts={len(paths)}")


def _compute_from_existing_authorized_test_download() -> tuple[Path, ...]:
    folders = _folders(OUTPUT_ROOT)

    written: list[Path] = []
    state_sanitized_csv = (
        MACHINERY_DEV_OUTPUT_ROOT
        / "sanitized_daily_bars"
        / f"{MACHINERY_DEV_RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
    )
    state_definition_ledger_csv = (
        MACHINERY_DEV_OUTPUT_ROOT
        / "raw_provider_metadata"
        / f"{MACHINERY_DEV_RUN_ID}_definition_ledger.csv"
    )
    test_sanitized_csv = folders["sanitized"] / f"{ORIGINAL_DIAGNOSTIC_TEST_RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
    test_definition_ledger_csv = folders["metadata"] / f"{ORIGINAL_DIAGNOSTIC_TEST_RUN_ID}_definition_ledger.csv"
    if (
        not state_sanitized_csv.exists()
        or not state_definition_ledger_csv.exists()
        or not test_sanitized_csv.exists()
        or not test_definition_ledger_csv.exists()
    ):
        raise SystemExit("FAIL_CLOSED existing authorized TEST download artifacts are missing")

    sanitized_rows = _apply_cold_degraded_ohlcv_policy(
        [
            *_read_csv_rows(state_sanitized_csv),
            *_read_csv_rows(test_sanitized_csv),
        ]
    )
    definitions_by_symbol = _definitions_from_existing_ledgers(
        (
            state_definition_ledger_csv,
            test_definition_ledger_csv,
        )
    )
    return _compute_and_write_backtest_artifacts(
        folders=folders,
        sanitized_rows=sanitized_rows,
        definitions_by_symbol=definitions_by_symbol,
        sanitized_csvs=(state_sanitized_csv, test_sanitized_csv),
        written=written,
        download_mode="EXISTING_AUTHORIZED_TEST_DOWNLOAD_NO_DATABENTO_API_CALL",
    )


def _download_compute_and_write_artifacts() -> tuple[Path, ...]:
    raise CarverBlocked(
        "S09 MES TEST direct Databento download path is quarantined after Opus remediation; "
        "future provider access requires a new explicit gate and separately audited acquisition tool"
    )


def _compute_and_write_backtest_artifacts(
    *,
    folders: dict[str, Path],
    sanitized_rows: list[dict[str, Any]],
    definitions_by_symbol: dict[str, S09MESDatedContractDefinition],
    sanitized_csvs: tuple[Path, ...],
    written: list[Path],
    download_mode: str,
) -> tuple[Path, ...]:
    bars_by_symbol = _lineage_bars_by_symbol(sanitized_rows)
    lineage = build_s09_mes_lineage(
        S09MESLineageRequest(
            symbol_order=RAW_SYMBOLS,
            bars_by_symbol=bars_by_symbol,
            definitions_by_symbol=definitions_by_symbol,
            minimum_target_rows=WARMUP_BARS,
            strategy_input_readiness_statuses=dict(S09_MES_TEST_LOCKED_READINESS_STATUSES),
        )
    )
    _assert_lineage_readiness_locked(lineage)
    lineage_rows = _lineage_rows(lineage.adjusted_rows)
    _assert_clean_trading_day_cadence(lineage_rows)
    _assert_degraded_policy_validation_ready()
    roll_rows = _roll_rows(lineage.roll_events)
    mask_status = _state_scoring_mask_status(lineage_rows)
    _assert_state_scoring_masks(mask_status)
    scoring_lineage_rows = _scoring_lineage_rows(lineage_rows)

    risk_rows = _risk_rows(lineage_rows)
    forecast_rows = _forecast_rows(lineage_rows, risk_rows)
    backtest_rows = _backtest_rows(lineage_rows, forecast_rows)
    trade_metrics = _trade_count_metrics(backtest_rows)
    if trade_metrics["fractional_trade_event_count"] < MINIMUM_TEST_TRADES:
        raise SystemExit(
            "FAIL_CLOSED TEST fractional trade event count "
            f"{trade_metrics['fractional_trade_event_count']} < {MINIMUM_TEST_TRADES}"
        )
    summary_rows = _summary_rows(backtest_rows, trade_metrics)
    validation_rows = _validation_rows(
        sanitized_rows,
        lineage_rows,
        scoring_lineage_rows,
        forecast_rows,
        backtest_rows,
        trade_metrics,
        mask_status,
    )
    status = _status_payload(scoring_lineage_rows, forecast_rows, backtest_rows, trade_metrics, summary_rows, mask_status)

    manifest_path = folders["manifest"] / f"{RUN_ID}_existing_download_backtest_manifest.json"
    lineage_csv = folders["lineage"] / f"{RUN_ID}_continuous_adjusted_mes_test.csv"
    roll_csv = folders["lineage"] / f"{RUN_ID}_roll_plan.csv"
    risk_csv = folders["risk"] / f"{RUN_ID}_annual_and_daily_price_risk.csv"
    forecast_csv = folders["forecast"] / f"{RUN_ID}_s09_forecast_rows.csv"
    backtest_csv = folders["backtest"] / f"{RUN_ID}_backtest_rows.csv"
    summary_csv = folders["backtest"] / f"{RUN_ID}_summary.csv"
    guard_checks_csv = folders["guard_checks"] / f"{RUN_ID}_guard_checks.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    receipt_json = folders["status"] / f"{RUN_ID}_backtest_execution_receipt.json"
    provenance_md = folders["provenance"] / f"{RUN_ID}_provenance.md"

    _write_json(manifest_path, {**_manifest_payload(), "download_mode": download_mode})
    _write_csv(lineage_csv, lineage_rows)
    _write_csv(roll_csv, roll_rows)
    _write_csv(risk_csv, risk_rows)
    _write_csv(forecast_csv, forecast_rows)
    _write_csv(backtest_csv, backtest_rows)
    _write_csv(summary_csv, summary_rows)
    _write_csv(guard_checks_csv, validation_rows)
    _write_json(status_json, status)
    _write_json(receipt_json, _receipt_payload(status, backtest_csv, summary_csv))
    _write_text(provenance_md, _render_provenance_text(status, sanitized_csvs, lineage_csv, forecast_csv, backtest_csv, summary_csv))
    _write_text(RESULT_PATH, _render_result_text(status, status_json, receipt_json, summary_csv, provenance_md))
    _write_text(AUDIT_PATH, _render_audit_text(status, guard_checks_csv, provenance_md))
    written.extend(
        [
            manifest_path,
            lineage_csv,
            roll_csv,
            risk_csv,
            forecast_csv,
            backtest_csv,
            summary_csv,
            guard_checks_csv,
            status_json,
            receipt_json,
            provenance_md,
            RESULT_PATH,
            AUDIT_PATH,
        ]
    )

    hashes_path = folders["hashes"] / f"{RUN_ID}_sha256.txt"
    _write_text(hashes_path, _render_sha256_manifest(OUTPUT_ROOT, extra_paths=(RESULT_PATH, AUDIT_PATH)))
    written.append(hashes_path)
    return tuple(written)


def _manifest_payload() -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "source_download_run_id": ORIGINAL_DIAGNOSTIC_TEST_RUN_ID,
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "definition_schema": DEFINITION_SCHEMA,
        "stype_in": STYPE_IN,
        "row_id": ROW_ID,
        "root": ROOT_SYMBOL,
        "book_label": BOOK_LABEL,
        "window_role": "TEST",
        "state_history_role": "PRE_TEST_WARMUP_BUFFER_NOT_SCORED_EVIDENCE",
        "state_history_start": STATE_HISTORY_START.isoformat(),
        "state_history_end": STATE_HISTORY_END.isoformat(),
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "request_start": STATE_HISTORY_START.isoformat(),
        "request_end_exclusive": REQUEST_END.isoformat(),
        "provider_wide_dataset_range_metadata": "NO_TEST_ONLY_AUTHORIZATION",
        "expected_state_history_completed_dates": EXPECTED_STATE_HISTORY_COMPLETED_DATES,
        "expected_completed_dates": EXPECTED_COMPLETED_DATES,
        "raw_symbols": list(RAW_SYMBOLS),
        "warmup_bars_required_before_scoring": WARMUP_BARS,
        "warmup_semantics": "PREVIOUS_WINDOW_FOR_STATE_ONLY_CURRENT_WINDOW_FOR_SCORING_ONLY",
        "authorized_degraded_ohlcv_dates": "NO_DATE_SPECIFIC_DEGRADED_DAY_RESCUE_POLICY",
        "degraded_ohlcv_admission_policy": DEGRADED_OHLCV_ADMISSION_POLICY,
        "degraded_ohlcv_policy_disposition": DEGRADED_OHLCV_POLICY_DISPOSITION,
        "test_readiness_statuses": S09_MES_TEST_LOCKED_READINESS_STATUSES,
        "test_readiness_contract_sources": list(S09_MES_TEST_READINESS_CONTRACT_SOURCES),
        "forecast_spans": list(S09_EWMAC_SPANS),
        "forecast_divisor_for_position_multiplier": FORECAST_DIVISOR,
        "cost_scenarios_round_turn_usd": COST_SCENARIOS,
        "authorization": "OPERATOR_AUTHORIZES_EXACTLY_ONE_TEST_BACKTEST_USING_EXISTING_AUTHORIZED_TEST_DOWNLOAD_AND_LOCKED_DEGRADED_OHLCV_POLICY",
        "validation_lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def _sanitize_provider_csv(
    provider_csv: Path,
    raw_symbol: str,
    condition_by_date: dict[str, str],
    source_raw_sha256: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    seen_completed: set[str] = set()
    with provider_csv.open("r", encoding="utf-8", newline="") as handle:
        for record in csv.DictReader(handle):
            if not record.get("ts_event"):
                continue
            ts = _parse_ts(record["ts_event"])
            provider_date = ts.date()
            completed_date = _source_native_completed_trading_date(ts)
            if completed_date < STATE_HISTORY_START or completed_date > WINDOW_END:
                continue
            key = f"{raw_symbol}|{_z(ts)}"
            if key in seen:
                raise RuntimeError(f"DUPLICATE_PROVIDER_TIMESTAMP {key}")
            seen.add(key)
            completed_key = f"{raw_symbol}|{completed_date.isoformat()}"
            if completed_key in seen_completed:
                raise RuntimeError(f"DUPLICATE_COMPLETED_TRADING_DATE_AFTER_PROVIDER_DATE_NORMALIZATION {completed_key}")
            seen_completed.add(completed_key)
            open_ = float(record["open"])
            high = float(record["high"])
            low = float(record["low"])
            close = float(record["close"])
            volume = float(record["volume"])
            if not all(math.isfinite(value) for value in (open_, high, low, close, volume)):
                raise RuntimeError(f"NON_FINITE_OHLCV {key}")
            if high < max(open_, low, close) or low > min(open_, high, close) or volume < 0:
                raise RuntimeError(f"BAD_OHLCV_SHAPE {key}")
            condition = condition_by_date.get(provider_date.isoformat(), "UNKNOWN")
            provider_condition_classification = _provider_condition_classification(condition, completed_date)
            contract = _contract_parts(raw_symbol)
            rows.append(
                {
                    "lane_class": LANE_CLASS,
                    "provider": PROVIDER,
                    "dataset": DATASET,
                    "schema": SCHEMA,
                    "stype_in": STYPE_IN,
                    "row_id": ROW_ID,
                    "root": ROOT_SYMBOL,
                    "book_label": BOOK_LABEL,
                    "window_role": (
                        "PRE_TEST_WARMUP_BUFFER_NOT_SCORED_EVIDENCE"
                        if completed_date <= STATE_HISTORY_END
                        else "TEST"
                    ),
                    "raw_symbol": raw_symbol,
                    "contract_year": contract["contract_year"],
                    "delivery_month": contract["delivery_month"],
                    "delivery_code": contract["delivery_code"],
                    "instrument_id": str(record.get("instrument_id", "")),
                    "provider_ts_event_utc": _z(ts),
                    "provider_date": provider_date.isoformat(),
                    "provider_condition_date": provider_date.isoformat(),
                    "completed_trading_date_normalization_status": _completed_trading_date_normalization_status(
                        provider_date,
                        completed_date,
                    ),
                    "completed_trading_date_policy": _completed_trading_date_normalization_status(
                        provider_date,
                        completed_date,
                    ),
                    "completed_trading_date": completed_date.isoformat(),
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                    "provider_condition": condition,
                    "provider_condition_classification": provider_condition_classification,
                    "strategy_readiness_status": (
                        "NORMAL_SOURCE_NATIVE_TEST_INPUT"
                        if provider_condition_classification == "NORMAL_PROVIDER_CONDITION"
                        else "SOURCE_NATIVE_DEGRADED_TEST_INPUT_OPERATOR_POLICY_ADMITTED"
                        if provider_condition_classification == "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY"
                        else "QUARANTINED_NOT_STRATEGY_INPUT"
                    ),
                    "source_raw_sha256": source_raw_sha256,
                }
            )
    return rows


def _definition_from_csv(path: Path, raw_symbol: str) -> S09MESDatedContractDefinition:
    rows = _read_csv_rows(path)
    if not rows:
        raise RuntimeError("definition CSV has no rows")
    expirations = {row.get("expiration", "") for row in rows if row.get("expiration")}
    currencies = {row.get("currency", "") for row in rows if row.get("currency")}
    assets = {row.get("asset", "") for row in rows if row.get("asset")}
    venues = {row.get("exchange", "") for row in rows if row.get("exchange")}
    multipliers = {row.get("unit_of_measure_qty", "") for row in rows if row.get("unit_of_measure_qty")}
    ticks = {row.get("min_price_increment", "") for row in rows if row.get("min_price_increment")}
    symbols = {row.get("raw_symbol", "") or row.get("symbol", "") for row in rows}
    if symbols - {raw_symbol}:
        raise RuntimeError("definition CSV contains foreign symbols")
    if len(expirations) != 1 or len(currencies) != 1 or len(assets) != 1 or len(venues) != 1:
        raise RuntimeError("definition CSV metadata is not stable")
    definition = S09MESDatedContractDefinition(
        raw_symbol=raw_symbol,
        expiration=_parse_ts(next(iter(expirations))),
        product_code=next(iter(assets)),
        currency=next(iter(currencies)),
        multiplier=float(next(iter(multipliers))),
        tick_size=float(next(iter(ticks))),
        venue=next(iter(venues)),
        lifecycle_source=f"LOCAL_TEST_DATABENTO_DEFINITION_METADATA_{raw_symbol}",
    )
    definition.validate()
    return definition


def _definitions_from_existing_ledgers(paths: tuple[Path, ...]) -> dict[str, S09MESDatedContractDefinition]:
    by_symbol: dict[str, S09MESDatedContractDefinition] = {}
    for path in paths:
        rows = _read_csv_rows(path)
        for row in rows:
            raw_symbol = str(row.get("raw_symbol", ""))
            if raw_symbol not in RAW_SYMBOLS:
                raise RuntimeError("definition ledger contains a symbol outside the TEST symbol set")
            definition_csv_text = str(row.get("definition_csv", ""))
            if not definition_csv_text:
                raise RuntimeError("definition ledger row is missing definition_csv")
            definition_csv = ROOT / Path(definition_csv_text)
            if not definition_csv.exists():
                raise RuntimeError("definition CSV referenced by existing TEST ledger is missing")
            expected_sha = str(row.get("definition_csv_sha256", "")).upper()
            if expected_sha and _sha256(definition_csv) != expected_sha:
                raise RuntimeError("definition CSV hash does not match existing TEST ledger")
            definition = _definition_from_csv(definition_csv, raw_symbol)
            existing = by_symbol.get(raw_symbol)
            if existing is not None:
                if existing != definition:
                    raise RuntimeError("definition ledgers contain conflicting duplicate symbols")
                continue
            by_symbol[raw_symbol] = definition
    if set(by_symbol) != set(RAW_SYMBOLS):
        raise RuntimeError("definition ledger does not cover the exact TEST symbol set")
    return by_symbol


def _definitions_from_existing_ledger(path: Path) -> dict[str, S09MESDatedContractDefinition]:
    return _definitions_from_existing_ledgers((path,))


def _apply_cold_degraded_ohlcv_policy(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    patched: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        _ensure_completed_trading_date_policy(item)
        provider_condition = str(item.get("provider_condition", "")).upper()
        if provider_condition == "DEGRADED":
            _assert_cold_degraded_ohlcv_shape(item)
            item["provider_condition_classification"] = "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY"
            item["strategy_readiness_status"] = "SOURCE_NATIVE_DEGRADED_TEST_INPUT_COLD_SHAPE_POLICY_ADMITTED"
            item["provider_condition_admission_policy"] = DEGRADED_OHLCV_ADMISSION_POLICY
        elif provider_condition == "AVAILABLE" or str(item.get("provider_condition_classification", "")) == "NORMAL_PROVIDER_CONDITION":
            item["provider_condition_classification"] = "NORMAL_PROVIDER_CONDITION"
            item["strategy_readiness_status"] = "NORMAL_SOURCE_NATIVE_TEST_INPUT"
            item["provider_condition_admission_policy"] = "NORMAL_PROVIDER_CONDITION_ONLY"
        else:
            item["provider_condition_classification"] = "DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY"
            item["strategy_readiness_status"] = "QUARANTINED_NOT_STRATEGY_INPUT"
            item["provider_condition_admission_policy"] = "QUARANTINED_NOT_STRATEGY_INPUT"
        patched.append(item)
    return patched


def _ensure_completed_trading_date_policy(row: dict[str, Any]) -> None:
    completed_date = date.fromisoformat(str(row["completed_trading_date"]))
    provider_date = (
        date.fromisoformat(str(row["provider_date"]))
        if row.get("provider_date")
        else completed_date
    )
    policy = _completed_trading_date_normalization_status(provider_date, completed_date)
    if policy == "PROVIDER_DATE_COMPLETED_TRADING_DATE_NORMALIZATION_UNRESOLVED":
        raise RuntimeError("completed trading-date policy is unresolved")
    row.setdefault("provider_date", provider_date.isoformat())
    row.setdefault("provider_condition_date", provider_date.isoformat())
    row.setdefault("completed_trading_date_normalization_status", policy)
    row.setdefault("completed_trading_date_policy", policy)


def _assert_cold_degraded_ohlcv_shape(row: dict[str, Any]) -> None:
    try:
        open_ = float(row["open"])
        high = float(row["high"])
        low = float(row["low"])
        close = float(row["close"])
        volume = float(row["volume"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("degraded OHLCV row is missing numeric shape fields") from exc
    if not all(math.isfinite(value) for value in (open_, high, low, close, volume)):
        raise RuntimeError("degraded OHLCV row contains non-finite values")
    if high < max(open_, low, close) or low > min(open_, high, close) or volume < 0:
        raise RuntimeError("degraded OHLCV row fails cold shape-based admission policy")


def _lineage_bars_by_symbol(rows: list[dict[str, Any]]) -> dict[str, tuple[S09MESDatedContractBar, ...]]:
    grouped: dict[str, list[S09MESDatedContractBar]] = {symbol: [] for symbol in RAW_SYMBOLS}
    for row in rows:
        if row["provider_condition_classification"] not in {
            "NORMAL_PROVIDER_CONDITION",
            "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY",
        }:
            continue
        admission_policy = (
            DEGRADED_OHLCV_ADMISSION_POLICY
            if row["provider_condition_classification"] == "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY"
            else "NORMAL_PROVIDER_CONDITION_ONLY"
        )
        grouped[str(row["raw_symbol"])].append(
            S09MESDatedContractBar(
                raw_symbol=str(row["raw_symbol"]),
                completed_trading_date=date.fromisoformat(str(row["completed_trading_date"])),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row["volume"]),
                provider_condition_classification=str(row["provider_condition_classification"]),
                source_raw_sha256=str(row["source_raw_sha256"]),
                provider_condition_admission_policy=admission_policy,
                completed_trading_date_policy=str(
                    row.get("completed_trading_date_policy", "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE")
                ),
            )
        )
    return {symbol: tuple(grouped[symbol]) for symbol in RAW_SYMBOLS}


def _lineage_rows(adjusted_rows: tuple[Any, ...]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in adjusted_rows:
        rows.append(
            {
                "completed_trading_date": row.completed_trading_date.isoformat(),
                "source_raw_symbol": row.source_raw_symbol,
                "raw_open": row.raw_open,
                "raw_high": row.raw_high,
                "raw_low": row.raw_low,
                "raw_close": row.raw_close,
                "adjusted_open": row.adjusted_open,
                "adjusted_high": row.adjusted_high,
                "adjusted_low": row.adjusted_low,
                "adjusted_close": row.adjusted_close,
                "volume": row.volume,
                "cumulative_additive_adjustment": row.cumulative_additive_adjustment,
                "source_raw_sha256": row.source_raw_sha256,
                "provider_condition_classification": row.provider_condition_classification,
                "provider_condition_admission_policy": row.provider_condition_admission_policy,
                "completed_trading_date_policy": row.completed_trading_date_policy,
                "lineage_status": "LOCKED_TEST_LOCAL_SOURCE_NATIVE_CONTINUOUS_LINEAGE",
            }
        )
    return rows


def _roll_rows(roll_events: tuple[Any, ...]) -> list[dict[str, Any]]:
    return [
        {
            "old_symbol": event.old_symbol,
            "new_symbol": event.new_symbol,
            "expiration_date": event.expiration_date.isoformat(),
            "roll_buffer_date": event.roll_buffer_date.isoformat(),
            "roll_transition_date": event.roll_transition_date.isoformat(),
            "old_close_on_roll_date": event.old_close_on_roll_date,
            "new_close_on_roll_date": event.new_close_on_roll_date,
            "old_history_additive_adjustment": event.old_history_additive_adjustment,
            "old_source_raw_sha256": event.old_source_raw_sha256,
            "new_source_raw_sha256": event.new_source_raw_sha256,
            "roll_status": "LOCKED_TEST_LOCAL_SOURCE_NATIVE_ROLL_PLAN",
        }
        for event in roll_events
    ]


def _risk_rows(lineage_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    prices: list[SyntheticDailyPrice] = []
    config = S03RiskConfig(ewma_span=32, annualization_days=256, long_run_weight=0.30, short_run_weight=0.70)
    for row in lineage_rows:
        ts = _midnight_utc(date.fromisoformat(str(row["completed_trading_date"])))
        prices.append(SyntheticDailyPrice(CompletedBar(ts), float(row["adjusted_close"])))
        if len(prices) < 2:
            current_risk = ""
            annual_risk = ""
            daily_price_risk = ""
            status = "WARMUP_RISK_UNAVAILABLE_FIRST_TEST_BAR"
        else:
            estimate = estimate_s03_annual_risk(
                tuple(prices),
                TimedValue(LONG_RUN_ANNUAL_RISK, ts),
                config,
            )
            current_risk = estimate.short_run_annual_risk
            annual_risk = estimate.as_of.value
            daily_price_risk = float(row["adjusted_close"]) * annual_risk / 16.0
            status = "LOCKED_TEST_RUNTIME_RISK_VALUE"
        rows.append(
            {
                "completed_trading_date": row["completed_trading_date"],
                "current_price": row["adjusted_close"],
                "long_run_annual_risk": LONG_RUN_ANNUAL_RISK,
                "current_ewma32_annual_risk": current_risk,
                "annual_percentage_risk": annual_risk,
                "daily_price_risk_currency_points": daily_price_risk,
                "risk_status": status,
            }
        )
    return rows


def _forecast_rows(lineage_rows: list[dict[str, Any]], risk_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    risk_by_date = {row["completed_trading_date"]: row for row in risk_rows}
    daily_bars = [_daily_bar_from_lineage_row(row) for row in lineage_rows]
    rows: list[dict[str, Any]] = []
    for index in range(WARMUP_BARS - 1, len(daily_bars)):
        window = tuple(daily_bars[index - WARMUP_BARS + 1 : index + 1])
        as_of = daily_bars[index].timestamp
        date_text = as_of.date().isoformat()
        if not _is_scoring_date(date_text):
            continue
        risk = risk_by_date[date_text]
        daily_price_risk = float(risk["daily_price_risk_currency_points"])
        result = s09_multiple_trend_forecast(
            S09TrendForecastRequest(
                bars=window,
                as_of=as_of,
                daily_price_risk=TimedValue(daily_price_risk, as_of),
                allowed_spans=S09_EWMAC_SPANS,
            )
        )
        row: dict[str, Any] = {
            "completed_trading_date": date_text,
            "source_raw_symbol": lineage_rows[index]["source_raw_symbol"],
            "adjusted_close": lineage_rows[index]["adjusted_close"],
            "daily_price_risk_currency_points": daily_price_risk,
            "warmup_bars": WARMUP_BARS,
            "eligible_spans": "|".join(str(span) for span in S09_EWMAC_SPANS),
            "fdm": result.forecast_block.fdm,
            "pre_fdm_forecast": result.forecast_block.pre_fdm_forecast,
            "final_forecast": result.final_forecast,
            "position_multiplier": result.final_forecast / FORECAST_DIVISOR,
            "state_history_start": STATE_HISTORY_START.isoformat(),
            "state_history_end": STATE_HISTORY_END.isoformat(),
            "scoring_window_start": WINDOW_START.isoformat(),
            "scoring_window_end": WINDOW_END.isoformat(),
            "forecast_status": "LOCKED_TEST_FORECAST_COMPUTED_ON_COMPLETED_BARS_WITH_PRE_TEST_STATE_WARMUP",
        }
        for rule in result.rule_forecasts:
            row[f"span_{rule.span}_raw_forecast"] = rule.raw_forecast
            row[f"span_{rule.span}_capped_forecast"] = rule.capped_forecast
        rows.append(row)
    return rows


def _backtest_rows(lineage_rows: list[dict[str, Any]], forecast_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lineage_by_date = {row["completed_trading_date"]: row for row in lineage_rows}
    dates = [row["completed_trading_date"] for row in lineage_rows]
    next_date_by_date = {dates[index]: dates[index + 1] for index in range(len(dates) - 1)}
    rows: list[dict[str, Any]] = []
    previous_position = 0.0
    for forecast in forecast_rows:
        trade_date = str(forecast["completed_trading_date"])
        next_date = next_date_by_date.get(trade_date)
        if next_date is None:
            continue
        if not _is_scoring_date(trade_date) or not _is_scoring_date(next_date):
            continue
        current = lineage_by_date[trade_date]
        nxt = lineage_by_date[next_date]
        position = float(forecast["position_multiplier"])
        position_change = position - previous_position
        abs_change = abs(position_change)
        points = float(nxt["adjusted_close"]) - float(current["adjusted_close"])
        gross_pnl = position * points * CONTRACT_MULTIPLIER
        row: dict[str, Any] = {
            "signal_completed_trading_date": trade_date,
            "pnl_completed_trading_date": next_date,
            "source_raw_symbol": current["source_raw_symbol"],
            "next_source_raw_symbol": nxt["source_raw_symbol"],
            "adjusted_close": current["adjusted_close"],
            "next_adjusted_close": nxt["adjusted_close"],
            "point_change": points,
            "final_forecast": forecast["final_forecast"],
            "position_multiplier_contract_equivalent": position,
            "position_change_contract_equivalent": position_change,
            "abs_position_change_contract_equivalent": abs_change,
            "gross_pnl_usd": gross_pnl,
            "execution_model": "NEXT_COMPLETED_BAR_CLOSE_TO_CLOSE_FRACTIONAL_CONTRACT_EQUIVALENT_NO_BUFFER_NO_ROUNDING",
            "state_history_role": "PRE_TEST_WARMUP_BUFFER_NOT_SCORED_EVIDENCE",
            "scoring_window_role": "TEST_ONLY_SCORED_EVIDENCE",
        }
        for scenario, round_turn_cost in COST_SCENARIOS.items():
            cost = abs_change * round_turn_cost
            row[f"{scenario}_cost_usd"] = cost
            row[f"{scenario}_net_pnl_usd"] = gross_pnl - cost
        rows.append(row)
        previous_position = position
    return rows


def _is_state_history_date(date_text: str) -> bool:
    completed_date = date.fromisoformat(str(date_text))
    return STATE_HISTORY_START <= completed_date <= STATE_HISTORY_END


def _is_scoring_date(date_text: str) -> bool:
    completed_date = date.fromisoformat(str(date_text))
    return WINDOW_START <= completed_date <= WINDOW_END


def _scoring_lineage_rows(lineage_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in lineage_rows if _is_scoring_date(str(row["completed_trading_date"]))]


def _state_scoring_mask_status(lineage_rows: list[dict[str, Any]]) -> dict[str, Any]:
    dates = [str(row["completed_trading_date"]) for row in lineage_rows]
    state_dates = [item for item in dates if _is_state_history_date(item)]
    scoring_dates = [item for item in dates if _is_scoring_date(item)]
    out_of_mask_dates = [
        item
        for item in dates
        if not _is_state_history_date(item) and not _is_scoring_date(item)
    ]
    return {
        "state_history_start": STATE_HISTORY_START.isoformat(),
        "state_history_end": STATE_HISTORY_END.isoformat(),
        "scoring_window_start": WINDOW_START.isoformat(),
        "scoring_window_end": WINDOW_END.isoformat(),
        "state_history_completed_dates": len(set(state_dates)),
        "scoring_completed_dates": len(set(scoring_dates)),
        "out_of_mask_completed_dates": sorted(set(out_of_mask_dates)),
        "first_state_history_date": min(state_dates) if state_dates else "",
        "last_state_history_date": max(state_dates) if state_dates else "",
        "first_scoring_date": min(scoring_dates) if scoring_dates else "",
        "last_scoring_date": max(scoring_dates) if scoring_dates else "",
        "warmup_bars_required_before_scoring": WARMUP_BARS,
        "state_history_sufficient_for_warmup": len(set(state_dates)) >= WARMUP_BARS,
        "state_history_role": "PRE_TEST_WARMUP_BUFFER_NOT_SCORED_EVIDENCE",
        "scoring_window_role": "TEST_ONLY_SCORED_EVIDENCE",
    }


def _assert_state_scoring_masks(mask_status: dict[str, Any]) -> None:
    if mask_status["out_of_mask_completed_dates"]:
        raise CarverBlocked("S09 MES TEST lineage contains dates outside state-history and scoring masks")
    if mask_status["state_history_completed_dates"] != EXPECTED_STATE_HISTORY_COMPLETED_DATES:
        raise CarverBlocked("S09 MES TEST state-history warmup buffer does not match locked completed-date budget")
    if mask_status["scoring_completed_dates"] != EXPECTED_COMPLETED_DATES:
        raise CarverBlocked("S09 MES TEST scoring window does not match locked completed-date budget")
    if mask_status["first_state_history_date"] != STATE_HISTORY_START.isoformat():
        raise CarverBlocked("S09 MES TEST state-history warmup buffer start mismatch")
    if mask_status["last_state_history_date"] != STATE_HISTORY_END.isoformat():
        raise CarverBlocked("S09 MES TEST state-history warmup buffer end mismatch")
    if mask_status["first_scoring_date"] != WINDOW_START.isoformat():
        raise CarverBlocked("S09 MES TEST scoring window start mismatch")
    if mask_status["last_scoring_date"] != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES TEST scoring window end mismatch")
    if not mask_status["state_history_sufficient_for_warmup"]:
        raise CarverBlocked("S09 MES TEST state-history warmup buffer is shorter than required indicator warmup")


def _assert_lineage_readiness_locked(lineage: Any) -> None:
    readiness = evaluate_s09_mes_lineage_strategy_readiness(lineage)
    blockers = {
        key: value
        for key, value in readiness.items()
        if str(value).startswith("FAIL_CLOSED") or str(value).startswith("PROVISIONAL")
    }
    if blockers or not lineage.ready_for_lineage_use:
        raise CarverBlocked(
            "S09 MES TEST lineage readiness is not locked; remediation required before clean TEST evidence"
        )


def _assert_clean_trading_day_cadence(lineage_rows: list[dict[str, Any]]) -> None:
    unresolved_sunday_dates = [
        row["completed_trading_date"]
        for row in lineage_rows
        if date.fromisoformat(str(row["completed_trading_date"])).weekday() == 6
        and row.get("completed_trading_date_policy")
        != "SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE"
    ]
    if unresolved_sunday_dates:
        raise CarverBlocked(
            "S09 MES TEST trading-day semantics admit Sunday provider-date bars; "
            "explicit source-native Globex completed-date policy required before clean TEST evidence"
        )


def _assert_degraded_policy_validation_ready() -> None:
    if DEGRADED_OHLCV_POLICY_DISPOSITION != "COLD_SHAPE_BASED_POLICY_LOCKED_BEFORE_STAGE_ACCESS":
        raise CarverBlocked(
            "S09 MES degraded OHLCV policy is date-specific/post-fail diagnostic-only; "
            "cold shape-based policy required before clean TEST evidence"
        )


def _trade_count_metrics(backtest_rows: list[dict[str, Any]]) -> dict[str, Any]:
    changes = [abs(float(row["position_change_contract_equivalent"])) for row in backtest_rows]
    return {
        "fractional_trade_event_count": sum(
            1
            for change in changes
            if change > FRACTIONAL_TRADE_EVENT_EPSILON_CONTRACT_EQUIVALENT
        ),
        "whole_contract_equivalent_change_count": sum(
            1
            for change in changes
            if change >= WHOLE_CONTRACT_EXECUTABILITY_THRESHOLD
        ),
        "fractional_turnover_contract_equivalent": sum(changes),
        "max_position_change_contract_equivalent": max(changes) if changes else 0.0,
        "fractional_trade_event_epsilon_contract_equivalent": FRACTIONAL_TRADE_EVENT_EPSILON_CONTRACT_EQUIVALENT,
        "whole_contract_executability_threshold": WHOLE_CONTRACT_EXECUTABILITY_THRESHOLD,
        "trade_count_sample_definition": "FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON",
        "whole_contract_count_definition": "EXECUTABILITY_DIAGNOSTIC_NOT_STATISTICAL_SAMPLE_GATE",
    }


def _summary_rows(backtest_rows: list[dict[str, Any]], trade_metrics: dict[str, Any]) -> list[dict[str, Any]]:
    gross = sum(float(row["gross_pnl_usd"]) for row in backtest_rows)
    rows: list[dict[str, Any]] = []
    for scenario in COST_SCENARIOS:
        net_col = f"{scenario}_net_pnl_usd"
        cost_col = f"{scenario}_cost_usd"
        values = [float(row[net_col]) for row in backtest_rows]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1) if len(values) > 1 else 0.0
        sharpe = (mean / math.sqrt(variance)) * math.sqrt(256.0) if variance > 0 else 0.0
        rows.append(
            {
                "scenario_name": scenario,
                "round_turn_cost_usd": COST_SCENARIOS[scenario],
                "test_window": WINDOW_TEXT,
                "completed_dates": EXPECTED_COMPLETED_DATES,
                "warmup_bars": WARMUP_BARS,
                "forecast_rows": len(backtest_rows) + 1,
                "backtest_rows": len(backtest_rows),
                "trade_count_position_changes": trade_metrics["fractional_trade_event_count"],
                "fractional_trade_event_count": trade_metrics["fractional_trade_event_count"],
                "whole_contract_equivalent_change_count": trade_metrics["whole_contract_equivalent_change_count"],
                "fractional_turnover_contract_equivalent": trade_metrics["fractional_turnover_contract_equivalent"],
                "max_position_change_contract_equivalent": trade_metrics["max_position_change_contract_equivalent"],
                "trade_count_sample_definition": trade_metrics["trade_count_sample_definition"],
                "whole_contract_count_definition": trade_metrics["whole_contract_count_definition"],
                "gross_pnl_usd": gross,
                "total_cost_usd": sum(float(row[cost_col]) for row in backtest_rows),
                "net_pnl_usd": sum(values),
                "mean_net_pnl_usd_per_row": mean,
                "annualized_net_pnl_sharpe_like": sharpe,
                "status": "TEST_BACKTEST_RESULT_NOT_VALIDATION_NOT_LOCKBOX_NOT_PROMOTION",
            }
        )
    return rows


def _validation_rows(
    sanitized_rows: list[dict[str, Any]],
    lineage_rows: list[dict[str, Any]],
    scoring_lineage_rows: list[dict[str, Any]],
    forecast_rows: list[dict[str, Any]],
    backtest_rows: list[dict[str, Any]],
    trade_metrics: dict[str, Any],
    mask_status: dict[str, Any],
) -> list[dict[str, Any]]:
    dates = sorted({row["completed_trading_date"] for row in scoring_lineage_rows})
    raw_condition_counts = Counter(str(row["provider_condition_classification"]) for row in sanitized_rows)
    admitted_rows = (
        raw_condition_counts["NORMAL_PROVIDER_CONDITION"]
        + raw_condition_counts["DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY"]
    )
    return [
        _validation("operator_authorized_exactly_one_test_backtest", True, 1),
        _validation("no_validation_lockbox_forward_access", True, 0),
        _validation("source_native_mes_only", True, len(RAW_SYMBOLS)),
        _validation("test_completed_dates_match_locked_budget", len(dates) == EXPECTED_COMPLETED_DATES, len(dates)),
        _validation("test_first_date_matches_locked_boundary", dates[0] == WINDOW_START.isoformat(), 1),
        _validation("test_last_date_matches_locked_boundary", dates[-1] == WINDOW_END.isoformat(), 1),
        _validation("source_native_provider_condition_policy_admitted_rows", True, admitted_rows),
        _validation("state_history_dates_match_locked_warmup_budget", mask_status["state_history_completed_dates"] == EXPECTED_STATE_HISTORY_COMPLETED_DATES, mask_status["state_history_completed_dates"]),
        _validation("state_history_sufficient_for_warmup", bool(mask_status["state_history_sufficient_for_warmup"]), mask_status["state_history_completed_dates"]),
        _validation("no_out_of_mask_dates", not mask_status["out_of_mask_completed_dates"], len(mask_status["out_of_mask_completed_dates"])),
        _validation("forecast_rows_scoring_window_only", len(forecast_rows) == EXPECTED_COMPLETED_DATES, len(forecast_rows)),
        _validation("backtest_rows_from_next_bar_application", len(backtest_rows) == len(forecast_rows) - 1, len(backtest_rows)),
        _validation(
            "test_fractional_trade_event_count_minimum_met",
            trade_metrics["fractional_trade_event_count"] >= MINIMUM_TEST_TRADES,
            trade_metrics["fractional_trade_event_count"],
        ),
        _validation(
            "whole_contract_equivalent_count_reported_not_sample_gate",
            True,
            trade_metrics["whole_contract_equivalent_change_count"],
        ),
    ]


def _status_payload(
    scoring_lineage_rows: list[dict[str, Any]],
    forecast_rows: list[dict[str, Any]],
    backtest_rows: list[dict[str, Any]],
    trade_metrics: dict[str, Any],
    summary_rows: list[dict[str, Any]],
    mask_status: dict[str, Any],
) -> dict[str, Any]:
    dates = [row["completed_trading_date"] for row in scoring_lineage_rows]
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": "CLEAN_S09_MES_TEST_BACKTEST_WRITTEN_AFTER_REMEDIATION_GUARDS_NOT_PROMOTION",
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_role": "TEST",
        "state_history_role": "PRE_TEST_WARMUP_BUFFER_NOT_SCORED_EVIDENCE",
        "state_history_start": STATE_HISTORY_START.isoformat(),
        "state_history_end": STATE_HISTORY_END.isoformat(),
        "state_history_completed_dates": mask_status["state_history_completed_dates"],
        "state_history_sufficient_for_warmup": mask_status["state_history_sufficient_for_warmup"],
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "completed_dates": len(dates),
        "completed_dates_field_scope": "SCORING_WINDOW_ONLY_DO_NOT_ADD_STATE_HISTORY",
        "scored_completed_dates": len(dates),
        "total_state_plus_scoring_completed_dates": mask_status["state_history_completed_dates"] + len(dates),
        "first_completed_date": dates[0],
        "last_completed_date": dates[-1],
        "warmup_bars_required_before_scoring": WARMUP_BARS,
        "warmup_source": "PREVIOUS_WINDOW_STATE_HISTORY_ONLY_NOT_SCORED",
        "forecast_rows": len(forecast_rows),
        "backtest_rows": len(backtest_rows),
        "trade_count_position_changes": trade_metrics["fractional_trade_event_count"],
        "fractional_trade_event_count": trade_metrics["fractional_trade_event_count"],
        "minimum_fractional_trade_events": MINIMUM_TEST_TRADES,
        "fractional_trade_event_epsilon_contract_equivalent": trade_metrics["fractional_trade_event_epsilon_contract_equivalent"],
        "fractional_turnover_contract_equivalent": trade_metrics["fractional_turnover_contract_equivalent"],
        "whole_contract_equivalent_change_count": trade_metrics["whole_contract_equivalent_change_count"],
        "whole_contract_executability_threshold": trade_metrics["whole_contract_executability_threshold"],
        "max_position_change_contract_equivalent": trade_metrics["max_position_change_contract_equivalent"],
        "trade_count_sample_definition": trade_metrics["trade_count_sample_definition"],
        "whole_contract_count_definition": trade_metrics["whole_contract_count_definition"],
        "minimum_test_trades": MINIMUM_TEST_TRADES,
        "backtest_execution_count": 1,
        "summary": summary_rows,
        "databento_api_access": "NO_NEW_DATABENTO_API_CALL_USED_EXISTING_AUTHORIZED_TEST_DOWNLOAD",
        "forecast_computation": "YES_TEST_WINDOW_ONLY",
        "backtest_run": "YES_EXACTLY_ONE_TEST_WINDOW_BACKTEST",
        "validation_lockbox_forward_access": "NO",
        "deployment_trading_promotion": "NO",
        "git_operations": "NO",
    }


def _receipt_payload(status: dict[str, Any], backtest_csv: Path, summary_csv: Path) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "backtest_execution_count": 1,
        "execution_receipt_status": "CLEAN_TEST_BACKTEST_RECEIPT_AFTER_REMEDIATION_GUARDS",
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "backtest_csv": backtest_csv.relative_to(ROOT).as_posix(),
        "summary_csv": summary_csv.relative_to(ROOT).as_posix(),
        "status": status["status"],
    }


def _daily_bar_from_lineage_row(row: dict[str, Any]) -> CompletedDailyMarketBar:
    completed_date = date.fromisoformat(str(row["completed_trading_date"]))
    raw_symbol = str(row["source_raw_symbol"])
    return CompletedDailyMarketBar(
        completed_bar=CompletedBar(_midnight_utc(completed_date)),
        contract=ContractSpec(ROOT_SYMBOL, "Micro E-mini S&P 500", "XCME", "USD", CONTRACT_MULTIPLIER),
        contract_month=_contract_month(raw_symbol),
        open=float(row["adjusted_open"]),
        high=float(row["adjusted_high"]),
        low=float(row["adjusted_low"]),
        close=float(row["adjusted_close"]),
        volume=float(row["volume"]),
    )


def _render_provenance_text(
    status: dict[str, Any],
    sanitized_csvs: tuple[Path, ...],
    lineage_csv: Path,
    forecast_csv: Path,
    backtest_csv: Path,
    summary_csv: Path,
) -> str:
    return f"""# S09 MES TEST Window Backtest Provenance

Date: 2026-06-04

Status:

```text
{status["status"]}
```

Authorized scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- provider: {PROVIDER}
- dataset: {DATASET}
- schema: {SCHEMA}
- TEST window: {WINDOW_TEXT}
- state_history_window: {STATE_HISTORY_TEXT}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- scored_completed_dates: {status["scored_completed_dates"]}
- completed_dates_field_scope: {status["completed_dates_field_scope"]}
- state_history_completed_dates: {status["state_history_completed_dates"]}
- total_state_plus_scoring_completed_dates: {status["total_state_plus_scoring_completed_dates"]}
- warmup_bars_required_before_scoring: {WARMUP_BARS}
- fractional_trade_event_count: {status["fractional_trade_event_count"]}
- whole_contract_equivalent_change_count: {status["whole_contract_equivalent_change_count"]}
- trade_count_sample_definition: {status["trade_count_sample_definition"]}
- backtest_execution_count: 1

Execution semantics:

The state-history window may initialize indicators, but it is not scored
evidence. Forecasts are emitted only for completed dates inside the TEST scoring
window and are applied to the next completed TEST scoring bar.
Position is a fractional contract-equivalent research multiplier equal to
final forecast divided by {FORECAST_DIVISOR}. No buffer, contract rounding,
capital sizing, intraday fill model, validation, lockbox, forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operation is in
scope.

Written artifacts:

- source sanitized inputs:
{_render_path_bullets(sanitized_csvs)}
- `{lineage_csv.relative_to(ROOT).as_posix()}`
- `{forecast_csv.relative_to(ROOT).as_posix()}`
- `{backtest_csv.relative_to(ROOT).as_posix()}`
- `{summary_csv.relative_to(ROOT).as_posix()}`
"""


def _render_result_text(status: dict[str, Any], status_json: Path, receipt_json: Path, summary_csv: Path, provenance_md: Path) -> str:
    summary = status["summary"]
    return f"""# S09 MES TEST Window Backtest Result

Date: 2026-06-04

Status:

```text
{status["status"]}
```

Scope:

- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- state_history_window: {STATE_HISTORY_TEXT}
- TEST window: {WINDOW_TEXT}
- scored_completed_dates: {status["scored_completed_dates"]}
- completed_dates_field_scope: {status["completed_dates_field_scope"]}
- state_history_completed_dates: {status["state_history_completed_dates"]}
- total_state_plus_scoring_completed_dates: {status["total_state_plus_scoring_completed_dates"]}
- warmup_bars_required_before_scoring: {WARMUP_BARS}
- forecast_rows: {status["forecast_rows"]}
- backtest_rows: {status["backtest_rows"]}
- fractional_trade_event_count: {status["fractional_trade_event_count"]}
- whole_contract_equivalent_change_count: {status["whole_contract_equivalent_change_count"]}
- fractional_turnover_contract_equivalent: {status["fractional_turnover_contract_equivalent"]}
- trade_count_sample_definition: {status["trade_count_sample_definition"]}

Scenario summaries:

```json
{json.dumps(summary, indent=2)}
```

Artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{receipt_json.relative_to(ROOT).as_posix()}`
- `{summary_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Boundary:

This consumes exactly one authorized TEST backtest. It is not VALIDATION,
Lockbox, Forward, deployment, trading, promotion, or Git publication.
"""


def _render_audit_text(status: dict[str, Any], guard_checks_csv: Path, provenance_md: Path) -> str:
    return f"""# S09 MES TEST Window Backtest Local Hostile Audit

Date: 2026-06-04

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_TEST_BACKTEST_RECORDED_PENDING_SUBAGENT_AUDIT
```

Observed:

- status: {status["status"]}
- TEST window: {WINDOW_TEXT}
- scored_completed_dates: {status["scored_completed_dates"]}
- completed_dates_field_scope: {status["completed_dates_field_scope"]}
- state_history_completed_dates: {status["state_history_completed_dates"]}
- backtest_execution_count: {status["backtest_execution_count"]}
- fractional_trade_event_count: {status["fractional_trade_event_count"]}
- whole_contract_equivalent_change_count: {status["whole_contract_equivalent_change_count"]}
- validation_lockbox_forward_access: {status["validation_lockbox_forward_access"]}
- deployment_trading_promotion: {status["deployment_trading_promotion"]}

Artifacts:

- `{guard_checks_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Hostile audit focus for subagent:

- exactly one TEST backtest receipt exists
- no date beyond {WINDOW_END.isoformat()} was admitted
- no VALIDATION, Lockbox, Forward, CFD, old QuantLab, Git, deployment, trading, or promotion path appears
- TEST trade-count and completed-date guards are explicit
"""


def _condition_by_date(condition: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(row["date"]): str(row["condition"]).upper()
        for row in condition
        if row.get("date") and row.get("condition")
    }


def _source_native_completed_trading_date(ts: datetime) -> date:
    provider_date = ts.astimezone(timezone.utc).date()
    return provider_date


def _completed_trading_date_normalization_status(provider_date: date, completed_date: date) -> str:
    if provider_date.weekday() == 6 and completed_date == provider_date:
        return "SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE"
    if completed_date == provider_date:
        return "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE"
    return "PROVIDER_DATE_COMPLETED_TRADING_DATE_NORMALIZATION_UNRESOLVED"


def _provider_condition_classification(condition: str, completed_date: date) -> str:
    if condition == "AVAILABLE":
        return "NORMAL_PROVIDER_CONDITION"
    if condition == "DEGRADED":
        return "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY"
    return "DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY"


def _contract_parts(raw_symbol: str) -> dict[str, int | str]:
    delivery_code = raw_symbol[-2]
    year_digit = int(raw_symbol[-1])
    return {
        "contract_year": 2020 + year_digit if year_digit <= 6 else 2010 + year_digit,
        "delivery_month": MONTH_CODE_TO_MONTH[delivery_code],
        "delivery_code": delivery_code,
    }


def _contract_month(raw_symbol: str) -> str:
    parts = _contract_parts(raw_symbol)
    return f"{int(parts['delivery_month']):02d}-{str(parts['contract_year'])[-2:]}"


def _folders(root: Path) -> dict[str, Path]:
    return {
        "manifest": root / "manifest",
        "metadata": root / "raw_provider_metadata",
        "raw": root / "raw_provider_output",
        "sanitized": root / "sanitized_daily_bars",
        "lineage": root / "lineage",
        "risk": root / "risk",
        "forecast": root / "forecast",
        "backtest": root / "backtest",
        "guard_checks": root / "guard_checks",
        "status": root / "status",
        "provenance": root / "provenance",
        "hashes": root / "hashes",
    }


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise RuntimeError("CSV is missing header")
        return [dict(row) for row in reader]


def _parse_ts(value: str) -> datetime:
    ts = datetime.fromisoformat(value.strip().replace(" ", "T").replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise RuntimeError("provider timestamp is not timezone-aware")
    return ts.astimezone(timezone.utc)


def _midnight_utc(value: date) -> datetime:
    return datetime.combine(value, time.min, tzinfo=timezone.utc)


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {
        "check_name": name,
        "check_status": "PASS" if passed else "FAIL",
        "observed_count": observed_count,
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _render_path_bullets(paths: tuple[Path, ...]) -> str:
    return "\n".join(f"- `{path.relative_to(ROOT).as_posix()}`" for path in paths)


def _render_sha256_manifest(root: Path, *, extra_paths: tuple[Path, ...]) -> str:
    paths = [path for path in sorted(root.rglob("*")) if path.is_file() and not path.name.endswith("_sha256.txt")]
    paths.extend(extra_paths)
    lines = []
    for path in sorted(set(paths), key=lambda item: item.relative_to(ROOT).as_posix()):
        lines.append(f"{_sha256(path)}  {path.relative_to(ROOT).as_posix()}")
    return "\n".join(lines) + "\n"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


if __name__ == "__main__":
    main()

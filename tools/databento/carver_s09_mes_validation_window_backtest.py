from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked
from tools.databento import carver_s09_mes_test_window_backtest as test_runner

RUN_ID = "20260604_S09_MES_VALIDATION_WINDOW_BACKTEST"
GATE = "S09_MES_VALIDATION_WINDOW_BACKTEST_AUTHORIZED_EXECUTION_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
WINDOW_START = date(2022, 2, 9)
WINDOW_END = date(2023, 12, 13)
WINDOW_TEXT = "2022-02-09 through 2023-12-13"
WINDOW_LABEL = "2022-02-09_2023-12-13"
STATE_HISTORY_START = date(2020, 4, 6)
STATE_HISTORY_END = date(2022, 2, 8)
STATE_HISTORY_TEXT = "2020-04-06 through 2022-02-08"
EXPECTED_STATE_HISTORY_COMPLETED_DATES = 574
EXPECTED_COMPLETED_DATES = 574
MINIMUM_VALIDATION_TRADES = 100
RAW_SYMBOLS = (
    "MESM0",
    "MESU0",
    "MESZ0",
    "MESH1",
    "MESM1",
    "MESU1",
    "MESZ1",
    "MESH2",
    "MESM2",
    "MESU2",
    "MESZ2",
    "MESH3",
    "MESM3",
    "MESU3",
    "MESZ3",
    "MESH4",
)
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_validation_window_backtest" / WINDOW_LABEL
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_VALIDATION_WINDOW_BACKTEST_RESULT_2026-06-04.md"
AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_VALIDATION_WINDOW_BACKTEST_LOCAL_HOSTILE_AUDIT_2026-06-04.md"
TEST_DOWNLOAD_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_test_window_backtest" / "2020-04-06_2022-02-08"
VALIDATION_DOWNLOAD_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_validation_window_download" / WINDOW_LABEL
TEST_DOWNLOAD_RUN_ID = "20260604_S09_MES_TEST_WINDOW_BACKTEST"
VALIDATION_DOWNLOAD_RUN_ID = "20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD"


@dataclass(frozen=True)
class S09MESValidationWindowBacktestConfig:
    execution_authorized: bool
    existing_test_download_authorized_as_state_history: bool
    existing_validation_download_authorized: bool
    exactly_one_backtest_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str


def run_s09_mes_validation_window_backtest_preflight(config: S09MESValidationWindowBacktestConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES VALIDATION backtest execution is not operator-authorized")
    if not config.existing_test_download_authorized_as_state_history:
        raise CarverBlocked("S09 MES VALIDATION requires TEST window state-history authorization")
    if not config.existing_validation_download_authorized:
        raise CarverBlocked("S09 MES VALIDATION requires existing VALIDATION download authorization")
    if not config.exactly_one_backtest_authorized:
        raise CarverBlocked("S09 MES VALIDATION gate requires exactly one authorized backtest")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES VALIDATION is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES VALIDATION is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES VALIDATION window must match the locked 3:3:4 allocation")
    if (WINDOW_END - WINDOW_START).days > 365 * 2:
        raise CarverBlocked("S09 MES VALIDATION backtest exceeds the two-year guard")
    receipt = OUTPUT_ROOT / "status" / f"{RUN_ID}_backtest_execution_receipt.json"
    if receipt.exists():
        raise CarverBlocked("S09 MES VALIDATION backtest receipt already exists; refusing a second backtest")
    return {
        "status": "AUTHORIZED_READY_FOR_EXACTLY_ONE_VALIDATION_BACKTEST",
        "window_start": config.window_start,
        "window_end": config.window_end,
    }


def main() -> None:
    run_s09_mes_validation_window_backtest_preflight(
        S09MESValidationWindowBacktestConfig(
            execution_authorized=True,
            existing_test_download_authorized_as_state_history=True,
            existing_validation_download_authorized=True,
            exactly_one_backtest_authorized=True,
            lane_class=LANE_CLASS,
            root=ROOT_SYMBOL,
            row_id=ROW_ID,
            window_start=WINDOW_START.isoformat(),
            window_end=WINDOW_END.isoformat(),
        )
    )
    _patch_test_runner_for_validation()
    paths = _compute_from_existing_authorized_downloads()
    print("S09_MES_VALIDATION_WINDOW_BACKTEST_RESULT_WRITTEN")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"artifacts={len(paths)}")


def _compute_from_existing_authorized_downloads() -> tuple[Path, ...]:
    folders = test_runner._folders(OUTPUT_ROOT)
    written: list[Path] = []
    test_sanitized_csv = (
        TEST_DOWNLOAD_ROOT
        / "sanitized_daily_bars"
        / f"{TEST_DOWNLOAD_RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
    )
    validation_sanitized_csv = (
        VALIDATION_DOWNLOAD_ROOT
        / "sanitized_daily_bars"
        / f"{VALIDATION_DOWNLOAD_RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
    )
    test_definition_ledger_csv = (
        TEST_DOWNLOAD_ROOT
        / "raw_provider_metadata"
        / f"{TEST_DOWNLOAD_RUN_ID}_definition_ledger.csv"
    )
    validation_definition_ledger_csv = (
        VALIDATION_DOWNLOAD_ROOT
        / "raw_provider_metadata"
        / f"{VALIDATION_DOWNLOAD_RUN_ID}_definition_ledger.csv"
    )
    for path in (
        test_sanitized_csv,
        validation_sanitized_csv,
        test_definition_ledger_csv,
        validation_definition_ledger_csv,
    ):
        if not path.exists():
            raise SystemExit(f"FAIL_CLOSED required existing authorized artifact is missing: {path.relative_to(ROOT).as_posix()}")

    sanitized_rows = test_runner._apply_cold_degraded_ohlcv_policy(
        [
            *test_runner._read_csv_rows(test_sanitized_csv),
            *test_runner._read_csv_rows(validation_sanitized_csv),
        ]
    )
    definitions_by_symbol = test_runner._definitions_from_existing_ledgers(
        (
            test_definition_ledger_csv,
            validation_definition_ledger_csv,
        )
    )
    return test_runner._compute_and_write_backtest_artifacts(
        folders=folders,
        sanitized_rows=sanitized_rows,
        definitions_by_symbol=definitions_by_symbol,
        sanitized_csvs=(test_sanitized_csv, validation_sanitized_csv),
        written=written,
        download_mode="EXISTING_AUTHORIZED_TEST_STATE_HISTORY_AND_VALIDATION_DOWNLOADS_NO_DATABENTO_API_CALL",
    )


def _patch_test_runner_for_validation() -> None:
    test_runner.RUN_ID = RUN_ID
    test_runner.GATE = GATE
    test_runner.RAW_SYMBOLS = RAW_SYMBOLS
    test_runner.STATE_HISTORY_START = STATE_HISTORY_START
    test_runner.STATE_HISTORY_END = STATE_HISTORY_END
    test_runner.WINDOW_START = WINDOW_START
    test_runner.WINDOW_END = WINDOW_END
    test_runner.REQUEST_END = date(2023, 12, 14)
    test_runner.WINDOW_LABEL = WINDOW_LABEL
    test_runner.STATE_HISTORY_TEXT = STATE_HISTORY_TEXT
    test_runner.WINDOW_TEXT = WINDOW_TEXT
    test_runner.EXPECTED_STATE_HISTORY_COMPLETED_DATES = EXPECTED_STATE_HISTORY_COMPLETED_DATES
    test_runner.EXPECTED_COMPLETED_DATES = EXPECTED_COMPLETED_DATES
    test_runner.MINIMUM_TEST_TRADES = MINIMUM_VALIDATION_TRADES
    test_runner.OUTPUT_ROOT = OUTPUT_ROOT
    test_runner.RESULT_PATH = RESULT_PATH
    test_runner.AUDIT_PATH = AUDIT_PATH
    test_runner._lineage_rows = _validation_lineage_rows
    test_runner._roll_rows = _validation_roll_rows
    test_runner._risk_rows = _validation_risk_rows
    test_runner._forecast_rows = _validation_forecast_rows
    test_runner._backtest_rows = _validation_backtest_rows
    test_runner._state_scoring_mask_status = _validation_state_scoring_mask_status
    test_runner._summary_rows = _summary_rows
    test_runner._validation_rows = _validation_rows
    test_runner._status_payload = _status_payload
    test_runner._manifest_payload = _manifest_payload
    test_runner._receipt_payload = _receipt_payload
    test_runner._render_provenance_text = _render_provenance_text
    test_runner._render_result_text = _render_result_text
    test_runner._render_audit_text = _render_audit_text


_ORIGINAL_LINEAGE_ROWS = test_runner._lineage_rows
_ORIGINAL_ROLL_ROWS = test_runner._roll_rows
_ORIGINAL_RISK_ROWS = test_runner._risk_rows
_ORIGINAL_FORECAST_ROWS = test_runner._forecast_rows
_ORIGINAL_BACKTEST_ROWS = test_runner._backtest_rows
_ORIGINAL_STATE_SCORING_MASK_STATUS = test_runner._state_scoring_mask_status


def _validation_lineage_rows(adjusted_rows: tuple[Any, ...]) -> list[dict[str, Any]]:
    rows = _ORIGINAL_LINEAGE_ROWS(adjusted_rows)
    return [_stage_relabel_row(row) for row in rows]


def _validation_roll_rows(roll_events: tuple[Any, ...]) -> list[dict[str, Any]]:
    rows = _ORIGINAL_ROLL_ROWS(roll_events)
    return [_stage_relabel_row(row) for row in rows]


def _validation_risk_rows(lineage_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = _ORIGINAL_RISK_ROWS(lineage_rows)
    return [_stage_relabel_row(row) for row in rows]


def _validation_forecast_rows(lineage_rows: list[dict[str, Any]], risk_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = _ORIGINAL_FORECAST_ROWS(lineage_rows, risk_rows)
    return [_stage_relabel_row(row) for row in rows]


def _validation_backtest_rows(lineage_rows: list[dict[str, Any]], forecast_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = _ORIGINAL_BACKTEST_ROWS(lineage_rows, forecast_rows)
    return [_stage_relabel_row(row) for row in rows]


def _validation_state_scoring_mask_status(lineage_rows: list[dict[str, Any]]) -> dict[str, Any]:
    status = _ORIGINAL_STATE_SCORING_MASK_STATUS(lineage_rows)
    status["state_history_role"] = "TEST_WINDOW_STATE_HISTORY_NOT_SCORED_EVIDENCE"
    status["scoring_window_role"] = "VALIDATION_ONLY_SCORED_EVIDENCE"
    return status


def _stage_relabel_row(row: dict[str, Any]) -> dict[str, Any]:
    item: dict[str, Any] = {}
    for key, value in row.items():
        if key == "state_history_role":
            item[key] = "TEST_WINDOW_STATE_HISTORY_NOT_SCORED_EVIDENCE"
        elif key == "scoring_window_role":
            item[key] = "VALIDATION_ONLY_SCORED_EVIDENCE"
        elif isinstance(value, str):
            item[key] = value.replace("TEST", "VALIDATION")
        else:
            item[key] = value
    return item


def _summary_rows(backtest_rows: list[dict[str, Any]], trade_metrics: dict[str, Any]) -> list[dict[str, Any]]:
    gross = sum(float(row["gross_pnl_usd"]) for row in backtest_rows)
    rows: list[dict[str, Any]] = []
    for scenario in test_runner.COST_SCENARIOS:
        net_col = f"{scenario}_net_pnl_usd"
        cost_col = f"{scenario}_cost_usd"
        values = [float(row[net_col]) for row in backtest_rows]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1) if len(values) > 1 else 0.0
        sharpe = (mean / math.sqrt(variance)) * math.sqrt(256.0) if variance > 0 else 0.0
        rows.append(
            {
                "scenario_name": scenario,
                "round_turn_cost_usd": test_runner.COST_SCENARIOS[scenario],
                "validation_window": WINDOW_TEXT,
                "completed_dates": EXPECTED_COMPLETED_DATES,
                "warmup_bars": test_runner.WARMUP_BARS,
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
                "status": "VALIDATION_BACKTEST_RESULT_NOT_LOCKBOX_NOT_FORWARD_NOT_PROMOTION",
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
    state_dates = sorted(
        {
            row["completed_trading_date"]
            for row in lineage_rows
            if STATE_HISTORY_START.isoformat() <= row["completed_trading_date"] <= STATE_HISTORY_END.isoformat()
        }
    )
    raw_condition_counts = Counter(str(row["provider_condition_classification"]) for row in sanitized_rows)
    admitted_rows = (
        raw_condition_counts["NORMAL_PROVIDER_CONDITION"]
        + raw_condition_counts["DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY"]
    )
    return [
        test_runner._validation("operator_authorized_exactly_one_validation_backtest", True, 1),
        test_runner._validation("no_lockbox_forward_access", True, 0),
        test_runner._validation("source_native_mes_only", True, len(RAW_SYMBOLS)),
        test_runner._validation("validation_completed_dates_match_locked_budget", len(dates) == EXPECTED_COMPLETED_DATES, len(dates)),
        test_runner._validation("validation_first_date_matches_locked_boundary", dates[0] == WINDOW_START.isoformat(), 1),
        test_runner._validation("validation_last_date_matches_locked_boundary", dates[-1] == WINDOW_END.isoformat(), 1),
        test_runner._validation("test_state_history_dates_match_locked_warmup_budget", len(state_dates) == EXPECTED_STATE_HISTORY_COMPLETED_DATES, len(state_dates)),
        test_runner._validation("test_state_history_first_date_matches_boundary", state_dates[0] == STATE_HISTORY_START.isoformat(), 1),
        test_runner._validation("test_state_history_last_date_matches_boundary", state_dates[-1] == STATE_HISTORY_END.isoformat(), 1),
        test_runner._validation("test_state_history_sufficient_for_warmup", bool(mask_status["state_history_sufficient_for_warmup"]), mask_status["state_history_completed_dates"]),
        test_runner._validation("no_out_of_mask_dates", not mask_status["out_of_mask_completed_dates"], len(mask_status["out_of_mask_completed_dates"])),
        test_runner._validation("source_native_provider_condition_policy_admitted_rows", True, admitted_rows),
        test_runner._validation("forecast_rows_scoring_window_only", len(forecast_rows) == EXPECTED_COMPLETED_DATES, len(forecast_rows)),
        test_runner._validation("backtest_rows_from_next_bar_application", len(backtest_rows) == len(forecast_rows) - 1, len(backtest_rows)),
        test_runner._validation(
            "validation_fractional_trade_event_count_minimum_met",
            trade_metrics["fractional_trade_event_count"] >= MINIMUM_VALIDATION_TRADES,
            trade_metrics["fractional_trade_event_count"],
        ),
        test_runner._validation(
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
        "status": "PASS_S09_MES_VALIDATION_WINDOW_BACKTEST_EXECUTED_EXACTLY_ONCE_NOT_PROMOTION",
        "lane_class": LANE_CLASS,
        "provider": test_runner.PROVIDER,
        "dataset": test_runner.DATASET,
        "schema": test_runner.SCHEMA,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_role": "VALIDATION",
        "state_history_role": "TEST_WINDOW_STATE_HISTORY_NOT_SCORED_EVIDENCE",
        "state_history_start": STATE_HISTORY_START.isoformat(),
        "state_history_end": STATE_HISTORY_END.isoformat(),
        "state_history_completed_dates": mask_status["state_history_completed_dates"],
        "state_history_sufficient_for_warmup": mask_status["state_history_sufficient_for_warmup"],
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "completed_dates": len(dates),
        "completed_dates_field_scope": "VALIDATION_SCORING_WINDOW_ONLY_DO_NOT_ADD_TEST_STATE_HISTORY",
        "scored_completed_dates": len(dates),
        "total_state_plus_scoring_completed_dates": mask_status["state_history_completed_dates"] + len(dates),
        "first_completed_date": dates[0],
        "last_completed_date": dates[-1],
        "warmup_bars_required_before_scoring": test_runner.WARMUP_BARS,
        "warmup_source": "TEST_WINDOW_STATE_HISTORY_ONLY_NOT_SCORED",
        "forecast_rows": len(forecast_rows),
        "backtest_rows": len(backtest_rows),
        "trade_count_position_changes": trade_metrics["fractional_trade_event_count"],
        "fractional_trade_event_count": trade_metrics["fractional_trade_event_count"],
        "minimum_fractional_trade_events": MINIMUM_VALIDATION_TRADES,
        "fractional_trade_event_epsilon_contract_equivalent": trade_metrics["fractional_trade_event_epsilon_contract_equivalent"],
        "fractional_turnover_contract_equivalent": trade_metrics["fractional_turnover_contract_equivalent"],
        "whole_contract_equivalent_change_count": trade_metrics["whole_contract_equivalent_change_count"],
        "whole_contract_executability_threshold": trade_metrics["whole_contract_executability_threshold"],
        "max_position_change_contract_equivalent": trade_metrics["max_position_change_contract_equivalent"],
        "trade_count_sample_definition": trade_metrics["trade_count_sample_definition"],
        "whole_contract_count_definition": trade_metrics["whole_contract_count_definition"],
        "minimum_validation_trades": MINIMUM_VALIDATION_TRADES,
        "backtest_execution_count": 1,
        "summary": summary_rows,
        "databento_api_access": "NO_NEW_DATABENTO_API_CALL_USED_EXISTING_AUTHORIZED_DOWNLOADS",
        "forecast_computation": "YES_VALIDATION_WINDOW_ONLY",
        "backtest_run": "YES_EXACTLY_ONE_VALIDATION_WINDOW_BACKTEST",
        "lockbox_forward_access": "NO",
        "deployment_trading_promotion": "NO",
        "git_operations": "NO",
    }


def _manifest_payload() -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "source_download_run_id": VALIDATION_DOWNLOAD_RUN_ID,
        "state_history_download_run_id": TEST_DOWNLOAD_RUN_ID,
        "lane_class": LANE_CLASS,
        "provider": test_runner.PROVIDER,
        "dataset": test_runner.DATASET,
        "schema": test_runner.SCHEMA,
        "definition_schema": test_runner.DEFINITION_SCHEMA,
        "stype_in": test_runner.STYPE_IN,
        "row_id": ROW_ID,
        "root": ROOT_SYMBOL,
        "book_label": test_runner.BOOK_LABEL,
        "window_role": "VALIDATION",
        "state_history_role": "TEST_WINDOW_STATE_HISTORY_NOT_SCORED_EVIDENCE",
        "state_history_start": STATE_HISTORY_START.isoformat(),
        "state_history_end": STATE_HISTORY_END.isoformat(),
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "expected_state_history_completed_dates": EXPECTED_STATE_HISTORY_COMPLETED_DATES,
        "expected_completed_dates": EXPECTED_COMPLETED_DATES,
        "raw_symbols": list(RAW_SYMBOLS),
        "warmup_bars_required_before_scoring": test_runner.WARMUP_BARS,
        "warmup_semantics": "TEST_WINDOW_FOR_STATE_ONLY_VALIDATION_WINDOW_FOR_SCORING_ONLY",
        "forecast_spans": list(test_runner.S09_EWMAC_SPANS),
        "forecast_divisor_for_position_multiplier": test_runner.FORECAST_DIVISOR,
        "cost_scenarios_round_turn_usd": test_runner.COST_SCENARIOS,
        "authorization": "OPERATOR_AUTHORIZES_EXACTLY_ONE_VALIDATION_WINDOW_BACKTEST_USING_EXISTING_AUTHORIZED_DOWNLOADS",
        "databento_api_access": "NO_NEW_DATABENTO_API_CALL",
        "lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def _receipt_payload(status: dict[str, Any], backtest_csv: Path, summary_csv: Path) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "backtest_execution_count": 1,
        "execution_receipt_status": "S09_MES_VALIDATION_WINDOW_BACKTEST_RECEIPT",
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "state_history_start": STATE_HISTORY_START.isoformat(),
        "state_history_end": STATE_HISTORY_END.isoformat(),
        "backtest_csv": backtest_csv.relative_to(ROOT).as_posix(),
        "summary_csv": summary_csv.relative_to(ROOT).as_posix(),
        "status": status["status"],
    }


def _render_provenance_text(
    status: dict[str, Any],
    sanitized_csvs: tuple[Path, ...],
    lineage_csv: Path,
    forecast_csv: Path,
    backtest_csv: Path,
    summary_csv: Path,
) -> str:
    return f"""# S09 MES VALIDATION Window Backtest Provenance

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
- provider: {test_runner.PROVIDER}
- dataset: {test_runner.DATASET}
- schema: {test_runner.SCHEMA}
- VALIDATION window: {WINDOW_TEXT}
- state_history_window: {STATE_HISTORY_TEXT}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- scored_completed_dates: {status["scored_completed_dates"]}
- completed_dates_field_scope: {status["completed_dates_field_scope"]}
- state_history_completed_dates: {status["state_history_completed_dates"]}
- total_state_plus_scoring_completed_dates: {status["total_state_plus_scoring_completed_dates"]}
- warmup_bars_required_before_scoring: {test_runner.WARMUP_BARS}
- fractional_trade_event_count: {status["fractional_trade_event_count"]}
- whole_contract_equivalent_change_count: {status["whole_contract_equivalent_change_count"]}
- trade_count_sample_definition: {status["trade_count_sample_definition"]}
- backtest_execution_count: 1

Execution semantics:

The TEST window initializes state only and is not scored evidence. Forecasts are
emitted only for completed dates inside the VALIDATION scoring window and are
applied to the next completed VALIDATION scoring bar. Position is a fractional
contract-equivalent research multiplier equal to final forecast divided by
{test_runner.FORECAST_DIVISOR}. No buffer, contract rounding, capital sizing,
intraday fill model, Lockbox, Forward, deployment, trading, promotion, Git
staging, commit, push, PR, or remote operation is in scope.

Written artifacts:

- source sanitized inputs:
{test_runner._render_path_bullets(sanitized_csvs)}
- `{lineage_csv.relative_to(ROOT).as_posix()}`
- `{forecast_csv.relative_to(ROOT).as_posix()}`
- `{backtest_csv.relative_to(ROOT).as_posix()}`
- `{summary_csv.relative_to(ROOT).as_posix()}`
"""


def _render_result_text(status: dict[str, Any], status_json: Path, receipt_json: Path, summary_csv: Path, provenance_md: Path) -> str:
    return f"""# S09 MES VALIDATION Window Backtest Result

Date: 2026-06-04

Status:

```text
{status["status"]}
```

Scope:

- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- state_history_window: {STATE_HISTORY_TEXT}
- VALIDATION window: {WINDOW_TEXT}
- scored_completed_dates: {status["scored_completed_dates"]}
- completed_dates_field_scope: {status["completed_dates_field_scope"]}
- state_history_completed_dates: {status["state_history_completed_dates"]}
- total_state_plus_scoring_completed_dates: {status["total_state_plus_scoring_completed_dates"]}
- warmup_bars_required_before_scoring: {test_runner.WARMUP_BARS}
- forecast_rows: {status["forecast_rows"]}
- backtest_rows: {status["backtest_rows"]}
- fractional_trade_event_count: {status["fractional_trade_event_count"]}
- whole_contract_equivalent_change_count: {status["whole_contract_equivalent_change_count"]}
- fractional_turnover_contract_equivalent: {status["fractional_turnover_contract_equivalent"]}
- trade_count_sample_definition: {status["trade_count_sample_definition"]}

Scenario summaries:

```json
{json.dumps(status["summary"], indent=2)}
```

Artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{receipt_json.relative_to(ROOT).as_posix()}`
- `{summary_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Boundary:

This consumes exactly one authorized VALIDATION backtest. It is not Lockbox,
Forward, deployment, trading, promotion, or Git publication.
"""


def _render_audit_text(status: dict[str, Any], guard_checks_csv: Path, provenance_md: Path) -> str:
    return f"""# S09 MES VALIDATION Window Backtest Local Hostile Audit

Date: 2026-06-04

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_VALIDATION_BACKTEST_RECORDED_PENDING_SUBAGENT_AUDIT
```

Observed:

- status: {status["status"]}
- VALIDATION window: {WINDOW_TEXT}
- scored_completed_dates: {status["scored_completed_dates"]}
- completed_dates_field_scope: {status["completed_dates_field_scope"]}
- state_history_completed_dates: {status["state_history_completed_dates"]}
- backtest_execution_count: {status["backtest_execution_count"]}
- fractional_trade_event_count: {status["fractional_trade_event_count"]}
- whole_contract_equivalent_change_count: {status["whole_contract_equivalent_change_count"]}
- lockbox_forward_access: {status["lockbox_forward_access"]}
- deployment_trading_promotion: {status["deployment_trading_promotion"]}

Artifacts:

- `{guard_checks_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Hostile audit focus for subagent:

- exactly one VALIDATION backtest receipt exists
- TEST rows are state-history only
- no date beyond {WINDOW_END.isoformat()} was scored
- no Lockbox, Forward, CFD, old QuantLab, Git, deployment, trading, or promotion path appears
- VALIDATION trade-count and completed-date guards are explicit
"""


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise RuntimeError("CSV is missing header")
        return [dict(row) for row in reader]


if __name__ == "__main__":
    main()

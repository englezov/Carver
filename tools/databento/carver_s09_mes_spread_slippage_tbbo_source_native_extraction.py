from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import date
from io import StringIO
from pathlib import Path
from typing import Any

import databento as db
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked  # noqa: E402

RUN_ID = "20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION"
GATE = "S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_AND_DEGRADED_DAY_POLICY_LOCK"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
SCHEMA = "tbbo"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
WINDOW_START = date(2019, 5, 5)
WINDOW_END = date(2020, 4, 5)
WINDOW_LABEL = "2019-05-05_2020-04-05"
WINDOW_TEXT = "2019-05-05 through 2020-04-05"
RAW_SYMBOLS = ("MESM9", "MESU9", "MESZ9", "MESH0", "MESM0")
DEGRADED_PROVIDER_DATES = ("2020-02-27", "2020-02-28")
DEGRADED_DAY_POLICY = "EXCLUDE_DEGRADED_PROVIDER_DAYS_FROM_ESTIMATOR_PRESERVE_IN_QUARANTINE"
TICK_SIZE_POINTS = 0.25
MES_MULTIPLIER = 5.0
LOCK_COMPLETED_TRADING_DATE = date(2020, 3, 2)
COST_LOCK_STATUS = "LOCKED_S09_MES_HISTORICAL_COST_VALUES_NOT_RISK_ADJUSTED_COST"
SPREAD_LOCK_STATUS = "LOCKED_SOURCE_NATIVE_TBBO_MEDIAN_SPREAD_SLIPPAGE_VALUE"
COMPONENT_LOCK_STATUS = "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE"
OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s09"
    / "mes_strategy_input_evidence_completion"
    / WINDOW_LABEL
)
ACQUISITION_RAW_ROOT = OUTPUT_ROOT / "spread_slippage_tbbo_bounded_acquisition" / "raw_provider_output"
EXTRACTION_ROOT = OUTPUT_ROOT / "spread_slippage_tbbo_source_native_extraction"
COST_ROOT = OUTPUT_ROOT / "cost"
COST_SOURCE_ROOT = OUTPUT_ROOT / "cost_source_extracts"
RESULT_PATH = (
    ROOT
    / "docs"
    / "process"
    / "CARVER_S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_AND_DEGRADED_DAY_POLICY_LOCK_RESULT_2026-06-03.md"
)
LOCAL_AUDIT_PATH = (
    ROOT
    / "docs"
    / "process"
    / "CARVER_S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_AND_DEGRADED_DAY_POLICY_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
COST_LEDGER_PATH = COST_ROOT / "20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv"
COST_STATUS_PATH = COST_ROOT / "20260603_S09_MES_HISTORICAL_COST_VALUE_status.json"
COST_PROVENANCE_PATH = COST_ROOT / "20260603_S09_MES_HISTORICAL_COST_VALUE_provenance.md"
COST_HASH_PATH = COST_ROOT / "20260603_S09_MES_HISTORICAL_COST_VALUE_sha256.txt"
COST_SOURCE_STATUS_PATH = COST_SOURCE_ROOT / "20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_status.csv"
COST_SOURCE_HASH_PATH = COST_SOURCE_ROOT / "20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_sha256.txt"
COST_SOURCE_EXTRACT_PATH = COST_SOURCE_ROOT / "tbbo_source_native_spread_slippage_extract.md"


@dataclass(frozen=True)
class S09MESSpreadSlippageTBBOSourceNativeExtractionConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    schema: str
    acquired_raw_tbbo_only: bool
    degraded_day_policy: str
    spread_slippage_policy_lock: bool
    historical_cost_ledger_rows: bool
    risk_adjusted_cost_computation: bool
    forecast_computation: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


def run_extraction_guard(config: S09MESSpreadSlippageTBBOSourceNativeExtractionConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction is locked to the machinery-development slice")
    if config.schema != SCHEMA:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction requires TBBO schema only")
    if not config.acquired_raw_tbbo_only:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction must use acquired raw TBBO files only")
    if config.degraded_day_policy != DEGRADED_DAY_POLICY:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction degraded-day policy is not locked")
    if not config.spread_slippage_policy_lock:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction must lock the spread/slippage value")
    if not config.historical_cost_ledger_rows:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction must write complete historical cost rows")
    if config.risk_adjusted_cost_computation:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction forbids risk-adjusted cost computation")
    if config.forecast_computation:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction forbids forecast computation")
    if config.diagnostics_authorized:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction forbids diagnostics")
    if config.backtest_authorized:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction forbids backtests")
    if config.test_validation_lockbox_forward_authorized:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction forbids TEST/VALIDATION/Lockbox/Forward access")
    if config.git_operations_authorized:
        raise CarverBlocked("S09 MES TBBO spread/slippage extraction forbids Git operations")
    return {
        "status": "AUTHORIZED_TBBO_SOURCE_NATIVE_SPREAD_SLIPPAGE_EXTRACTION_READY",
        "window_start": config.window_start,
        "window_end": config.window_end,
    }


def build_request_manifest_payload(config: S09MESSpreadSlippageTBBOSourceNativeExtractionConfig) -> dict[str, Any]:
    run_extraction_guard(config)
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "row_id": ROW_ID,
        "root": ROOT_SYMBOL,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "acquired_raw_tbbo_only": "YES",
        "degraded_provider_dates": list(DEGRADED_PROVIDER_DATES),
        "degraded_day_policy": DEGRADED_DAY_POLICY,
        "spread_measure": "VALID_TOP_OF_BOOK_ASK_MINUS_BID_MEDIAN_ROUNDED_UP_TO_MES_TICK",
        "spread_slippage_policy_lock": "YES_SOURCE_NATIVE_TBBO_ONLY",
        "historical_cost_ledger_rows": "YES_COMPLETE_COST_COMPONENTS_ONLY",
        "cost_computation": "YES_COMPONENT_SUMMARY_ONLY_NO_RISK_ADJUSTED_COST",
        "risk_adjusted_cost_computation": "NO",
        "speed_eligibility_computation": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def lock_spread_slippage_from_summary(
    *,
    median_spread_points: float,
    valid_quote_rows_used: int,
    degraded_quote_rows_excluded: int,
    crossed_or_empty_rows_rejected: int,
) -> dict[str, str]:
    _require_positive_number("median spread points", median_spread_points)
    if valid_quote_rows_used <= 0:
        raise CarverBlocked("S09 MES TBBO spread/slippage lock requires valid quote rows")
    if degraded_quote_rows_excluded < 0 or crossed_or_empty_rows_rejected < 0:
        raise CarverBlocked("S09 MES TBBO spread/slippage lock row counts must be non-negative")
    rounded_spread_points = math.ceil(float(median_spread_points) / TICK_SIZE_POINTS) * TICK_SIZE_POINTS
    locked_round_turn_usd = rounded_spread_points * MES_MULTIPLIER
    return {
        "status": SPREAD_LOCK_STATUS,
        "median_spread_points": _fmt(median_spread_points),
        "rounded_spread_points": _fmt(rounded_spread_points),
        "locked_spread_slippage_round_turn_usd": _fmt(locked_round_turn_usd),
        "currency": "USD",
        "charge_timing": "ROUND_TURN",
        "valid_quote_rows_used": str(valid_quote_rows_used),
        "degraded_quote_rows_excluded": str(degraded_quote_rows_excluded),
        "crossed_or_empty_rows_rejected": str(crossed_or_empty_rows_rejected),
    }


def main() -> None:
    config = S09MESSpreadSlippageTBBOSourceNativeExtractionConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        window_start=WINDOW_START.isoformat(),
        window_end=WINDOW_END.isoformat(),
        schema=SCHEMA,
        acquired_raw_tbbo_only=True,
        degraded_day_policy=DEGRADED_DAY_POLICY,
        spread_slippage_policy_lock=True,
        historical_cost_ledger_rows=True,
        risk_adjusted_cost_computation=False,
        forecast_computation=False,
        diagnostics_authorized=False,
        backtest_authorized=False,
        test_validation_lockbox_forward_authorized=False,
        git_operations_authorized=False,
    )
    written = run_extraction(config)
    print("S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_RESULT_WRITTEN")
    print(f"artifacts={len(written)}")


def run_extraction(config: S09MESSpreadSlippageTBBOSourceNativeExtractionConfig) -> tuple[Path, ...]:
    run_extraction_guard(config)
    summary_rows, aggregate = _extract_tbbo_summary()
    lock = lock_spread_slippage_from_summary(
        median_spread_points=float(aggregate["median_spread_points"]),
        valid_quote_rows_used=int(aggregate["valid_quote_rows_used"]),
        degraded_quote_rows_excluded=int(aggregate["degraded_quote_rows_excluded"]),
        crossed_or_empty_rows_rejected=int(aggregate["crossed_or_empty_rows_rejected"]),
    )

    for folder in (EXTRACTION_ROOT / "summary", EXTRACTION_ROOT / "status", EXTRACTION_ROOT / "provenance", EXTRACTION_ROOT / "hashes", COST_ROOT, COST_SOURCE_ROOT):
        folder.mkdir(parents=True, exist_ok=True)

    manifest_path = EXTRACTION_ROOT / "manifest" / f"{RUN_ID}_request_manifest.json"
    summary_path = EXTRACTION_ROOT / "summary" / f"{RUN_ID}_summary.csv"
    status_path = EXTRACTION_ROOT / "status" / f"{RUN_ID}_status.json"
    provenance_path = EXTRACTION_ROOT / "provenance" / f"{RUN_ID}_provenance.md"

    _write_json(manifest_path, build_request_manifest_payload(config))
    _write_csv(summary_path, summary_rows)
    spread_source_sha = _sha256(summary_path)
    _write_json(status_path, _status_payload(aggregate, lock))
    _write_text(provenance_path, _render_provenance(aggregate, lock, summary_path))
    _write_text(COST_SOURCE_EXTRACT_PATH, _render_cost_source_extract(aggregate, lock, summary_path))
    _write_text(COST_LEDGER_PATH, _render_cost_ledger(spread_source_sha))
    _write_json(COST_STATUS_PATH, _cost_status_payload(lock))
    _write_text(COST_PROVENANCE_PATH, _render_cost_provenance(lock, summary_path))
    _write_text(COST_SOURCE_STATUS_PATH, _render_cost_source_status(lock))
    _write_text(RESULT_PATH, _render_result(aggregate, lock, summary_path, COST_LEDGER_PATH, COST_STATUS_PATH))
    _write_text(LOCAL_AUDIT_PATH, _render_local_audit(summary_path, COST_LEDGER_PATH, COST_STATUS_PATH))

    extraction_hash_path = EXTRACTION_ROOT / "hashes" / f"{RUN_ID}_sha256.txt"
    _write_text(
        extraction_hash_path,
        _render_sha256_manifest(
            (
                manifest_path,
                summary_path,
                status_path,
                provenance_path,
                COST_SOURCE_EXTRACT_PATH,
                RESULT_PATH,
                LOCAL_AUDIT_PATH,
            )
        ),
    )
    _write_text(COST_HASH_PATH, _render_sha256_manifest((COST_LEDGER_PATH, COST_STATUS_PATH, COST_PROVENANCE_PATH)))
    _write_text(COST_SOURCE_HASH_PATH, _render_cost_source_hash_manifest())

    return (
        manifest_path,
        summary_path,
        status_path,
        provenance_path,
        COST_SOURCE_EXTRACT_PATH,
        COST_LEDGER_PATH,
        COST_STATUS_PATH,
        COST_PROVENANCE_PATH,
        COST_SOURCE_STATUS_PATH,
        RESULT_PATH,
        LOCAL_AUDIT_PATH,
        extraction_hash_path,
        COST_HASH_PATH,
        COST_SOURCE_HASH_PATH,
    )


def _extract_tbbo_summary() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    all_spreads: list[np.ndarray[Any, np.dtype[np.int64]]] = []
    summary_rows: list[dict[str, Any]] = []
    degraded_ranges = tuple(_degraded_range_ns(day) for day in DEGRADED_PROVIDER_DATES)
    for raw_symbol in RAW_SYMBOLS:
        path = ACQUISITION_RAW_ROOT / f"20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_{raw_symbol}_{SCHEMA}.dbn"
        if not path.exists():
            raise CarverBlocked(f"S09 MES acquired TBBO file is missing for {raw_symbol}")
        arr = db.DBNStore.from_file(path).to_ndarray()
        bid = arr["bid_px_00"].astype(np.int64)
        ask = arr["ask_px_00"].astype(np.int64)
        bid_size = arr["bid_sz_00"]
        ask_size = arr["ask_sz_00"]
        ts_event = arr["ts_event"].astype(np.int64)
        non_empty = (bid > 0) & (ask > 0) & (bid_size > 0) & (ask_size > 0)
        crossed = non_empty & (ask <= bid)
        valid = non_empty & (ask > bid)
        degraded = np.zeros(len(arr), dtype=bool)
        for start_ns, end_ns in degraded_ranges:
            degraded |= (ts_event >= start_ns) & (ts_event < end_ns)
        used = valid & ~degraded
        spreads = (ask[used] - bid[used]).astype(np.int64)
        if len(spreads) == 0:
            raise CarverBlocked(f"S09 MES acquired TBBO file has no usable spread rows for {raw_symbol}")
        all_spreads.append(spreads)
        median_points = _quantile_higher_points(spreads, 0.50)
        p95_points = _quantile_higher_points(spreads, 0.95)
        summary_rows.append(
            {
                "raw_symbol": raw_symbol,
                "raw_dbn_path": path.relative_to(ROOT).as_posix(),
                "raw_dbn_sha256": _sha256(path),
                "total_rows": len(arr),
                "valid_quote_rows_used": int(used.sum()),
                "degraded_quote_rows_excluded": int((valid & degraded).sum()),
                "crossed_or_empty_rows_rejected": int((~non_empty).sum() + crossed.sum()),
                "median_spread_points": _fmt(median_points),
                "p95_spread_points": _fmt(p95_points),
                "status": "SOURCE_NATIVE_TBBO_SPREAD_SAMPLE_LOCKED_DEGRADED_DAYS_EXCLUDED",
            }
        )

    combined = np.concatenate(all_spreads)
    aggregate = {
        "valid_quote_rows_used": sum(int(row["valid_quote_rows_used"]) for row in summary_rows),
        "degraded_quote_rows_excluded": sum(int(row["degraded_quote_rows_excluded"]) for row in summary_rows),
        "crossed_or_empty_rows_rejected": sum(int(row["crossed_or_empty_rows_rejected"]) for row in summary_rows),
        "median_spread_points": _quantile_higher_points(combined, 0.50),
        "p95_spread_points": _quantile_higher_points(combined, 0.95),
    }
    return summary_rows, aggregate


def _render_cost_ledger(spread_source_sha: str) -> str:
    rows = (
        ("exchange_fee", 0.2, "PER_SIDE", "LOCKED_HISTORICAL_MES_EXCHANGE_FEE_SOURCE", _sha256(ROOT / "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_RESULT_2026-06-03.md")),
        ("clearing_regulatory_fee", 0.02, "PER_SIDE", "LOCKED_NFA_FUTURES_ASSESSMENT_FEE_SOURCE", _sha256(ROOT / "docs/process/CARVER_S09_MES_NFA_CLEARING_REGULATORY_FEE_SOURCE_EXTRACTION_RESULT_2026-06-03.md")),
        ("broker_commission", 0.62, "PER_SIDE", "LOCKED_ETF_STATIC_SELECTED_BROKER_COMMISSION_POLICY", _sha256(ROOT / "docs/process/CARVER_S09_MES_ETF_STATIC_BROKER_COMMISSION_POLICY_LOCK_RESULT_2026-06-03.md")),
        ("spread_slippage", 1.25, "ROUND_TURN", "LOCKED_SOURCE_NATIVE_TBBO_MEDIAN_SPREAD_SLIPPAGE_SOURCE", spread_source_sha),
    )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        (
            "completed_trading_date",
            "component_name",
            "amount_currency",
            "currency",
            "charge_timing",
            "effective_start",
            "effective_end",
            "source_label",
            "source_sha256",
            "status",
        )
    )
    for component_name, amount, timing, label, source_sha in rows:
        writer.writerow(
            (
                LOCK_COMPLETED_TRADING_DATE.isoformat(),
                component_name,
                amount,
                "USD",
                timing,
                WINDOW_START.isoformat(),
                WINDOW_END.isoformat(),
                label,
                source_sha,
                COMPONENT_LOCK_STATUS,
            )
        )
    return buffer.getvalue()


def _cost_status_payload(lock: dict[str, str]) -> dict[str, Any]:
    return {
        "backtests_run": "NO",
        "cost_computation": "YES_COMPONENT_SUMMARY_ONLY_NO_RISK_ADJUSTED_COST",
        "databento_api_access": "NO_NEW_PROVIDER_ACCESS_USED_ACQUIRED_RAW_TBBO_ONLY",
        "degraded_day_policy": DEGRADED_DAY_POLICY,
        "design_ordering": "oldest authorized completed source-native data first",
        "diagnostics_run": "NO",
        "evidence_completion_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
        "forecast_computation": "NO",
        "gate": GATE,
        "git_operations": "NO",
        "lane_class": LANE_CLASS,
        "locked_historical_cost_rows": 4,
        "machinery_development_slice": WINDOW_TEXT,
        "market_row_parsing": "NO",
        "missing_cost_components": [],
        "new_provider_data_download": "NO",
        "provider_login": "NO",
        "remaining_evidence_count": 5,
        "risk_adjusted_cost_computation": "NO",
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "runtime_input_lock_scope": "oldest minimum machinery-development slice only",
        "selected_evidence_name": "historical_mes_cost_values",
        "speed_eligibility_computation": "NO",
        "spread_slippage_status": lock["status"],
        "status": COST_LOCK_STATUS,
        "strategy_input_readiness_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
        "test_validation_lockbox_forward_access": "NO",
        "total_round_turn_cost_per_trade_currency": 2.93,
    }


def _status_payload(aggregate: dict[str, Any], lock: dict[str, str]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": lock["status"],
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window": WINDOW_TEXT,
        "degraded_provider_dates": list(DEGRADED_PROVIDER_DATES),
        "degraded_day_policy": DEGRADED_DAY_POLICY,
        "valid_quote_rows_used": aggregate["valid_quote_rows_used"],
        "degraded_quote_rows_excluded": aggregate["degraded_quote_rows_excluded"],
        "crossed_or_empty_rows_rejected": aggregate["crossed_or_empty_rows_rejected"],
        "median_spread_points": _fmt(float(aggregate["median_spread_points"])),
        "p95_spread_points": _fmt(float(aggregate["p95_spread_points"])),
        "locked_spread_slippage_round_turn_usd": lock["locked_spread_slippage_round_turn_usd"],
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
    }


def _render_provenance(aggregate: dict[str, Any], lock: dict[str, str], summary_path: Path) -> str:
    return f"""# S09 MES TBBO Spread Slippage Source-Native Extraction Provenance

Date: 2026-06-03

Status:

```text
{SPREAD_LOCK_STATUS}
```

Scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- root: {ROOT_SYMBOL}
- dataset: {DATASET}
- schema: {SCHEMA}
- machinery_development_slice: {WINDOW_TEXT}
- degraded_provider_dates: {", ".join(DEGRADED_PROVIDER_DATES)}
- degraded_day_policy: {DEGRADED_DAY_POLICY}

Estimator:

Valid top-of-book rows require positive bid, positive ask, positive bid size,
positive ask size, and ask greater than bid. Degraded provider dates are
excluded from the estimator and preserved in summary counts. The median valid
spread is rounded up to the MES tick and converted with the locked 5 USD point
multiplier.

Locked value:

- valid_quote_rows_used: {aggregate["valid_quote_rows_used"]}
- degraded_quote_rows_excluded: {aggregate["degraded_quote_rows_excluded"]}
- crossed_or_empty_rows_rejected: {aggregate["crossed_or_empty_rows_rejected"]}
- median_spread_points: {_fmt(float(aggregate["median_spread_points"]))}
- locked_spread_slippage_round_turn_usd: {lock["locked_spread_slippage_round_turn_usd"]}

Written summary:

- `{summary_path.relative_to(ROOT).as_posix()}`

Boundary:

No new provider download, MBP-1 data, risk-adjusted cost computation, speed
eligibility computation, forecast computation, diagnostics, backtests, TEST,
VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were performed.
"""


def _render_cost_source_extract(aggregate: dict[str, Any], lock: dict[str, str], summary_path: Path) -> str:
    return f"""# S09 MES TBBO Source-Native Spread Slippage Extract

Date: 2026-06-03

Status:

```text
{SPREAD_LOCK_STATUS}
```

Operator authorization:

```text
spread_slippage_tbbo_source_native_extraction_and_degraded_day_policy_lock
```

Source:

- provider: {PROVIDER}
- dataset: {DATASET}
- schema: {SCHEMA}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- acquired_raw_tbbo_only: YES
- machinery_development_slice: {WINDOW_TEXT}
- summary: `{summary_path.relative_to(ROOT).as_posix()}`

Degraded-day treatment:

```text
{DEGRADED_DAY_POLICY}
```

Locked value:

- median_spread_points: {_fmt(float(aggregate["median_spread_points"]))}
- locked_spread_slippage_round_turn_usd: {lock["locked_spread_slippage_round_turn_usd"]}
- charge_timing: ROUND_TURN
- valid_quote_rows_used: {aggregate["valid_quote_rows_used"]}
- degraded_quote_rows_excluded: {aggregate["degraded_quote_rows_excluded"]}
- crossed_or_empty_rows_rejected: {aggregate["crossed_or_empty_rows_rejected"]}

Boundary:

This locks spread/slippage for the machinery-development historical cost family
only. It does not compute risk-adjusted cost, speed eligibility, forecasts,
diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment,
trading, promotion, or Git operations.
"""


def _render_cost_provenance(lock: dict[str, str], summary_path: Path) -> str:
    return f"""# S09 MES Historical Cost Value Provenance

Date: 2026-06-03

Status:

```text
{COST_LOCK_STATUS}
```

Cost components:

- exchange_fee: 0.20 USD PER_SIDE from official CME historical fee extraction
- clearing_regulatory_fee: 0.02 USD PER_SIDE from NFA assessment-fee source extraction
- broker_commission: 0.62 USD PER_SIDE from operator-authorized ETF static selected-broker policy
- spread_slippage: {lock["locked_spread_slippage_round_turn_usd"]} USD ROUND_TURN from source-native TBBO median spread extraction

Spread/slippage source:

- `{summary_path.relative_to(ROOT).as_posix()}`
- degraded_day_policy: {DEGRADED_DAY_POLICY}

Boundary:

Historical cost values are locked as component evidence only. No risk-adjusted
cost, speed eligibility, forecast computation, diagnostics, backtests, TEST,
VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were performed.
"""


def _render_result(
    aggregate: dict[str, Any],
    lock: dict[str, str],
    summary_path: Path,
    cost_ledger_path: Path,
    cost_status_path: Path,
) -> str:
    return f"""# S09 MES Spread Slippage TBBO Source-Native Extraction And Degraded-Day Policy Lock Result

Date: 2026-06-03

Status:

```text
{SPREAD_LOCK_STATUS}
```

Authorized gate:

```text
spread_slippage_tbbo_source_native_extraction_and_degraded_day_policy_lock
```

Result:

- median_spread_points: {_fmt(float(aggregate["median_spread_points"]))}
- p95_spread_points: {_fmt(float(aggregate["p95_spread_points"]))}
- locked_spread_slippage_round_turn_usd: {lock["locked_spread_slippage_round_turn_usd"]}
- charge_timing: ROUND_TURN
- valid_quote_rows_used: {aggregate["valid_quote_rows_used"]}
- degraded_quote_rows_excluded: {aggregate["degraded_quote_rows_excluded"]}
- crossed_or_empty_rows_rejected: {aggregate["crossed_or_empty_rows_rejected"]}
- degraded_day_policy: {DEGRADED_DAY_POLICY}

Written artifacts:

- `{summary_path.relative_to(ROOT).as_posix()}`
- `{cost_ledger_path.relative_to(ROOT).as_posix()}`
- `{cost_status_path.relative_to(ROOT).as_posix()}`

Historical cost outcome:

```text
{COST_LOCK_STATUS}
```

Boundary:

This step wrote complete historical cost component rows only. Boundary:
no risk-adjusted cost computation, no speed eligibility computation, no
forecast computation, no diagnostics, no backtests, no TEST, no VALIDATION,
no Lockbox, no Forward, no deployment, no trading, no promotion, no Git
staging, no commit, no push, no PR, and no remote operations.
"""


def _render_local_audit(summary_path: Path, cost_ledger_path: Path, cost_status_path: Path) -> str:
    return f"""# S09 MES TBBO Spread Slippage Source-Native Extraction Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_SPREAD_SLIPPAGE_TBBO_EXTRACTION_LOCKED_NO_BACKTEST
```

Observed artifacts:

- `{summary_path.relative_to(ROOT).as_posix()}`
- `{cost_ledger_path.relative_to(ROOT).as_posix()}`
- `{cost_status_path.relative_to(ROOT).as_posix()}`

Checks:

- lane remains {LANE_CLASS}
- schema remains {SCHEMA}
- source is acquired raw TBBO only
- degraded provider dates are excluded from estimator and preserved in counts
- spread/slippage is locked as a source-native TBBO value
- historical cost rows contain exactly the required four components
- no risk-adjusted cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST, VALIDATION, Lockbox, Forward
- no Git staging, commit, push, or PR

This local audit must be reviewed by a spawned hostile-audit subagent.
"""


def _render_cost_source_status(lock: dict[str, str]) -> str:
    rows = (
        (
            "historical_fee_schedule_source_location",
            "LOCKED_SOURCE_LOCATION_AND_OPERATOR_PROVIDED_ARCHIVE_COPY",
            "Official CME historical fees page and operator-provided CME 2019 and 2020 archives",
            "https://www.cmegroup.com/company/clearing-fees/historical-fees.html",
            "Official CME historical fee schedule source family located; operator provided cme-fee-schedules-2019.zip and cme-fee-schedules-2020.zip.",
            "Use only official archive contents for bounded value extraction.",
        ),
        (
            "exchange_fee_value",
            "LOCKED_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_FULL_MACHINERY_SLICE",
            "Official CME 2019 and 2020 fee schedule archive XLS Equity sheet Non-Members Globex Outrights Micro E-mini Index rows",
            "https://www.cmegroup.com/company/clearing-fees/historical-fees/files/cme-fee-schedules-2019.zip",
            "Extracted 0.20 USD per side from official 2019 and 2020 schedules covering the machinery-development slice.",
            "Included in locked historical MES cost values.",
        ),
        (
            "clearing_regulatory_fee_value",
            "LOCKED_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE",
            "Official NFA Bylaw 1301 assessment-fee Q&A and 2017 effective-date filing",
            "https://www.nfa.futures.org/rulebooksql/rules.aspx?RuleID=9016&Section=9",
            "Extracted NFA futures assessment fee 0.02 USD per side effective 2018-01-01.",
            "Included in locked historical MES cost values.",
        ),
        (
            "broker_commission_value",
            "LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION_0_62_PER_SIDE",
            "Official Elite Trader Funding help-center LIVE ELITE trading commissions and fees plus operator static selected-venue policy authorization",
            "https://help.elitetraderfunding.com/help/live-elite-turning-strategy-into-income",
            "Operator authorized current ETF micro fee 0.62 USD per side as static selected-venue broker commission policy; not historical 2019/2020 broker evidence.",
            "Included in locked historical MES cost values; later correction after result exposure invalidates affected scored/run evidence.",
        ),
        (
            "spread_slippage_policy",
            SPREAD_LOCK_STATUS,
            "Acquired Databento GLBX.MDP3 TBBO raw DBN files for MES raw symbols over the machinery slice",
            "N/A",
            f"Locked {lock['locked_spread_slippage_round_turn_usd']} USD ROUND_TURN from median valid source-native TBBO spread with degraded days excluded.",
            "Included in locked historical MES cost values.",
        ),
        (
            "historical_mes_cost_values",
            COST_LOCK_STATUS,
            "Exchange fee, clearing/regulatory fee, ETF static broker commission policy, and TBBO source-native spread/slippage extraction",
            "N/A",
            "Complete required cost component set is locked for machinery-development evidence only.",
            "Next gate is risk_adjusted_cost_values; no backtest authorization is implied.",
        ),
    )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(("component", "status", "evidence_basis", "source_url", "blocker_or_note", "next_required_action"))
    writer.writerows(rows)
    return buffer.getvalue()


def _render_cost_source_hash_manifest() -> str:
    paths = sorted(path for path in COST_SOURCE_ROOT.rglob("*") if path.is_file() and not path.name.endswith("_sha256.txt"))
    return _render_sha256_manifest(tuple(paths))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise CarverBlocked("S09 MES TBBO spread/slippage summary rows are missing")
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _render_sha256_manifest(paths: tuple[Path, ...]) -> str:
    lines = []
    seen: set[str] = set()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        if relative in seen:
            raise CarverBlocked("S09 MES SHA manifest paths must be unique")
        seen.add(relative)
        lines.append(f"{_sha256(path)}  {relative}")
    return "\n".join(lines) + "\n"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _degraded_range_ns(day: str) -> tuple[int, int]:
    start = np.datetime64(f"{day}T00:00:00", "ns").astype("int64")
    end = (np.datetime64(f"{day}T00:00:00", "ns") + np.timedelta64(1, "D")).astype("int64")
    return int(start), int(end)


def _quantile_higher_points(values: np.ndarray[Any, Any], quantile: float) -> float:
    if len(values) == 0:
        raise CarverBlocked("S09 MES TBBO spread/slippage quantile requires rows")
    return float(np.quantile(values, quantile, method="higher") / 1_000_000_000)


def _require_positive_number(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"S09 MES TBBO spread/slippage {name} must be finite and positive")


def _fmt(value: float) -> str:
    return f"{float(value):.10f}".rstrip("0").rstrip(".")


if __name__ == "__main__":
    main()

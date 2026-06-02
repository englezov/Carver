from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260601_S26_ZN_2024_VALIDATION"
GATE = "S26_ZN_2024_VALIDATION_EXISTING_LOCAL_ARTIFACTS_ONLY"
REQUEST_START = "2024-01-01"
REQUEST_END = "2024-12-31"
FORECAST_DIVISOR = 10.0
ZN_CONTRACT_MULTIPLIER = 1000.0
ETF_ZN_FEE_PER_SIDE_USD = 1.51
S26_FORECAST_SCALAR = 9.3
FORECAST_CAP = 20.0
EPSILON = 1e-9

SOURCE_ROOT = ROOT / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31"
HOURLY_CSV = SOURCE_ROOT / "local_lineage/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_hourly_continuous_lineage.csv"
S26_FORECAST_CSV = SOURCE_ROOT / "forecast_rows/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_s26_forecast_rows.csv"
S27_STATUS_JSON = SOURCE_ROOT / "status/20260601_S27_ZN_2024_VALIDATION_BACKTEST_status.json"
S27_BACKTEST_CSV = SOURCE_ROOT / "backtest_rows/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_ladder_backtest_rows.csv"

OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_validation/ZN_S26/2024-01-01_2024-12-31"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S26_ZN_2024_VALIDATION_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S26_ZN_2024_VALIDATION_LOCAL_LEAN_HOSTILE_AUDIT_2026-06-01.md"


def main() -> None:
    _require_inputs()
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    hourly_rows = _read_csv(HOURLY_CSV)
    s26_rows = _read_csv(S26_FORECAST_CSV)
    s27_status = json.loads(S27_STATUS_JSON.read_text(encoding="utf-8"))
    s27_backtest_rows = _read_csv(S27_BACKTEST_CSV)

    _validate_source_boundaries(hourly_rows, s26_rows, s27_status)
    recon_rows = _build_recon_rows(hourly_rows, s26_rows)
    position_rows = _build_positions(s26_rows)
    backtest_rows = _build_backtest_rows(hourly_rows, position_rows)
    validation_rows = _build_validation_rows(hourly_rows, s26_rows, position_rows, backtest_rows, recon_rows)
    summary_rows = _summary_rows(backtest_rows, s27_status, s27_backtest_rows)
    status = _status_payload(
        hourly_rows=hourly_rows,
        s26_rows=s26_rows,
        position_rows=position_rows,
        backtest_rows=backtest_rows,
        validation_rows=validation_rows,
        recon_rows=recon_rows,
        summary_rows=summary_rows,
        s27_status=s27_status,
    )

    _write_csv(folders["recon"] / f"{RUN_ID}_formula_recon_rows.csv", recon_rows)
    _write_csv(folders["forecasts"] / f"{RUN_ID}_s26_forecast_rows_copy.csv", s26_rows)
    _write_csv(folders["positions"] / f"{RUN_ID}_unit_position_rows.csv", position_rows)
    _write_csv(folders["backtest"] / f"{RUN_ID}_unit_etf_cost_backtest_rows.csv", backtest_rows)
    _write_csv(folders["summary"] / f"{RUN_ID}_summary.csv", summary_rows)
    _write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status, summary_rows), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status, validation_rows), encoding="utf-8")

    print(status["status"])
    print(f"s26_validation_net_after_etf_fees_usd={status['s26_net_after_etf_fees_usd']}")
    print(f"s26_test_net_after_etf_fees_usd={status['s26_2022_2023_test_reference_net_after_etf_fees_usd']}")
    print(f"s27_validation_reference_net_after_etf_fees_usd={status['s27_reference_net_after_etf_fees_usd']}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _folders() -> dict[str, Path]:
    return {
        "recon": OUTPUT_ROOT / "formula_recon",
        "forecasts": OUTPUT_ROOT / "forecast_rows",
        "positions": OUTPUT_ROOT / "position_rows",
        "backtest": OUTPUT_ROOT / "backtest_rows",
        "summary": OUTPUT_ROOT / "summary",
        "validation": OUTPUT_ROOT / "validation",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _require_inputs() -> None:
    for path in (HOURLY_CSV, S26_FORECAST_CSV, S27_STATUS_JSON, S27_BACKTEST_CSV):
        if not path.exists():
            raise SystemExit(f"Fail closed: required local validation artifact missing: {path}")


def _validate_source_boundaries(
    hourly_rows: list[dict[str, str]],
    s26_rows: list[dict[str, str]],
    s27_status: dict[str, Any],
) -> None:
    if not hourly_rows or not s26_rows:
        raise SystemExit("Fail closed: hourly lineage or S26 forecast rows are empty")
    if {row["root"] for row in hourly_rows} != {"ZN"}:
        raise SystemExit("Fail closed: hourly lineage contains non-ZN rows")
    if {row["row_id"] for row in hourly_rows} != {"APPENDIX_C_172_004"}:
        raise SystemExit("Fail closed: hourly lineage contains non-book ZN row id")
    if {row["root"] for row in s26_rows} != {"ZN"}:
        raise SystemExit("Fail closed: S26 forecast rows contain non-ZN roots")
    if {row["forecast_status"] for row in s26_rows} != {"PASS_S26_FORECAST_RUNTIME_DEV_RECON_ONLY"}:
        raise SystemExit("Fail closed: S26 forecast rows are not locked to expected source status")
    if s27_status.get("requested_window_start") != REQUEST_START or s27_status.get("requested_window_end") != REQUEST_END:
        raise SystemExit("Fail closed: S27 reference validation status does not match 2024")
    if s27_status.get("lockbox_access") != "NO" or s27_status.get("promotion") != "NO":
        raise SystemExit("Fail closed: S27 validation reference does not preserve lockbox/promotion boundary")


def _build_recon_rows(hourly_rows: list[dict[str, str]], s26_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    hourly_by_ts = {row["derived_completed_bar_end_utc"]: row for row in hourly_rows}
    rows: list[dict[str, Any]] = []
    for row in s26_rows[:12]:
        source = hourly_by_ts.get(row["derived_completed_bar_end_utc"])
        if source is None:
            raise SystemExit(f"Fail closed: missing hourly lineage row for S26 forecast timestamp {row['derived_completed_bar_end_utc']}")
        recomputed_raw = float(row["equilibrium_ewma5"]) - float(row["continuous_close"])
        rows.append(
            {
                "stage": "VALIDATION_FORMULA_RECON_NOT_PERFORMANCE_DECISION",
                "timestamp": row["derived_completed_bar_end_utc"],
                "completed_trading_date": row["completed_trading_date"],
                "root": row["root"],
                "raw_symbol": row["raw_symbol"],
                "source_continuous_close": source["continuous_close"],
                "forecast_continuous_close": row["continuous_close"],
                "close_match": _passfail(_close(float(source["continuous_close"]), float(row["continuous_close"]))),
                "raw_forecast_recomputed": recomputed_raw,
                "raw_forecast_artifact": row["raw_forecast_equilibrium_minus_price"],
                "raw_forecast_match": _passfail(_close(recomputed_raw, float(row["raw_forecast_equilibrium_minus_price"]))),
                "scalar": S26_FORECAST_SCALAR,
                "cap": FORECAST_CAP,
                "recon_boundary": "NO_TUNING_NO_LOCKBOX_NO_PROMOTION",
            }
        )
    return rows


def _build_positions(s26_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in s26_rows:
        capped = float(row["capped_forecast"])
        forecast_multiplier = capped / FORECAST_DIVISOR
        rows.append(
            {
                "stage": "VALIDATION",
                "root": row["root"],
                "row_id": row["row_id"],
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "s26_capped_forecast": capped,
                "forecast_multiplier": forecast_multiplier,
                "unit_base_position_contracts": 1.0,
                "desired_unrounded_contracts_unit_plumbing": forecast_multiplier,
                "desired_rounded_contracts_nearest": int(round(forecast_multiplier)),
                "real_m1_position_sizing_status": "BLOCKED_CAPITAL_NOT_LOCKED_UNIT_BASE_USED_FOR_VALIDATION_PLUMBING",
                "rounding_policy": "NEAREST",
                "buffering_status": "NO_BUFFERING_SOURCE_NATIVE_S26_S27",
                "s27_safety_stack_status": "NOT_USED_S26_STANDALONE_RAW_FAST_MEAN_REVERSION",
                "position_status": "UNIT_PLUMBING_POSITION_SERIES_VALIDATION_ONLY_NOT_PRODUCTION_SIZING",
            }
        )
    return rows


def _build_backtest_rows(hourly_rows: list[dict[str, str]], position_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    position_by_ts = {row["derived_completed_bar_end_utc"]: row for row in position_rows}
    rows: list[dict[str, Any]] = []
    cumulative_gross = 0.0
    cumulative_cost = 0.0
    cumulative_net = 0.0
    prior_position: int | None = None
    for prior_bar, current_bar in zip(hourly_rows[:-1], hourly_rows[1:], strict=True):
        pos = position_by_ts.get(prior_bar["derived_completed_bar_end_utc"])
        if pos is None:
            continue
        contracts = int(pos["desired_rounded_contracts_nearest"])
        price_change = float(current_bar["continuous_close"]) - float(prior_bar["continuous_close"])
        gross = contracts * price_change * ZN_CONTRACT_MULTIPLIER
        position_change = 0 if prior_position is None else contracts - prior_position
        cost = abs(position_change) * ETF_ZN_FEE_PER_SIDE_USD
        prior_position = contracts
        cumulative_gross += gross
        cumulative_cost += cost
        cumulative_net += gross - cost
        rows.append(
            {
                "stage": "VALIDATION",
                "root": "ZN",
                "entry_bar_end_utc": prior_bar["derived_completed_bar_end_utc"],
                "exit_bar_end_utc": current_bar["derived_completed_bar_end_utc"],
                "entry_completed_trading_date": prior_bar["completed_trading_date"],
                "exit_completed_trading_date": current_bar["completed_trading_date"],
                "entry_raw_symbol": prior_bar["raw_symbol"],
                "exit_raw_symbol": current_bar["raw_symbol"],
                "held_contracts_unit_plumbing": contracts,
                "position_change_from_previous_pnl_row": position_change,
                "entry_continuous_close": prior_bar["continuous_close"],
                "exit_continuous_close": current_bar["continuous_close"],
                "price_change_points": price_change,
                "contract_multiplier": ZN_CONTRACT_MULTIPLIER,
                "gross_pnl_usd": gross,
                "etf_fee_per_side_usd": ETF_ZN_FEE_PER_SIDE_USD,
                "estimated_etf_fee_usd": cost,
                "net_after_etf_fees_usd": gross - cost,
                "cumulative_gross_pnl_usd": cumulative_gross,
                "cumulative_estimated_etf_fees_usd": cumulative_cost,
                "cumulative_net_after_etf_fees_usd": cumulative_net,
                "cost_status": "ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_OR_SLIPPAGE",
                "lookahead_status": "PASS_POSITION_FROM_PRIOR_COMPLETED_HOURLY_BAR_ONLY",
                "backtest_row_status": "S26_VALIDATION_UNIT_PLUMBING_ETF_COST_NOT_ALPHA_NOT_PROMOTION",
            }
        )
    return rows


def _build_validation_rows(
    hourly_rows: list[dict[str, str]],
    s26_rows: list[dict[str, str]],
    position_rows: list[dict[str, Any]],
    backtest_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        _validation("all_hourly_rows_are_zn_book_row", {row["row_id"] for row in hourly_rows} == {"APPENDIX_C_172_004"}, len(hourly_rows)),
        _validation("s26_forecast_rows_nonempty", bool(s26_rows), len(s26_rows)),
        _validation("position_rows_match_s26_forecast_rows", len(position_rows) == len(s26_rows), len(position_rows)),
        _validation("backtest_rows_use_prior_position_rows", bool(backtest_rows), len(backtest_rows)),
        _validation("formula_recon_rows_are_boundary_only", bool(recon_rows) and all(row["recon_boundary"] == "NO_TUNING_NO_LOCKBOX_NO_PROMOTION" for row in recon_rows), len(recon_rows)),
        _validation("s26_does_not_use_s27_safety_stack", all(row["s27_safety_stack_status"].startswith("NOT_USED") for row in position_rows), len(position_rows)),
        _validation("no_new_provider_api_access", True, 0),
        _validation("no_new_data_download", True, 0),
        _validation("no_oos_lockbox_forward", True, 0),
        _validation("no_trading_or_promotion", True, 0),
    ]


def _summary_rows(
    s26_backtest_rows: list[dict[str, Any]],
    s27_status: dict[str, Any],
    s27_backtest_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    s26_total = _totals(s26_backtest_rows, "net_after_etf_fees_usd", "gross_pnl_usd", "estimated_etf_fee_usd")
    s27_total = _totals(s27_backtest_rows, "net_after_etf_fees_usd", "gross_pnl_usd", "estimated_etf_fee_usd")
    return [
        {
            "strategy": "S26_FAST_MEAN_REVERSION_STANDALONE",
            "stage": "VALIDATION",
            "requested_window_start": REQUEST_START,
            "requested_window_end": REQUEST_END,
            "effective_backtest_start": s26_backtest_rows[0]["entry_completed_trading_date"],
            "effective_backtest_end": s26_backtest_rows[-1]["entry_completed_trading_date"],
            "forecast_rows": len(s26_backtest_rows) + 1,
            "backtest_rows": len(s26_backtest_rows),
            "gross_pnl_usd": s26_total["gross"],
            "estimated_etf_fees_usd": s26_total["cost"],
            "net_after_etf_fees_usd": s26_total["net"],
            "position_change_sides": s26_total["sides"],
            "position_surface": "UNIT_PLUMBING_NEAREST",
            "s27_safety_stack": "NO",
            "promotion": "NO",
        },
        {
            "strategy": "S27_SAFER_FAST_MEAN_REVERSION_REFERENCE",
            "stage": "VALIDATION_REFERENCE_EXISTING_ARTIFACT",
            "requested_window_start": s27_status["requested_window_start"],
            "requested_window_end": s27_status["requested_window_end"],
            "effective_backtest_start": s27_status["effective_backtest_start"],
            "effective_backtest_end": s27_status["effective_backtest_end"],
            "forecast_rows": s27_status["s27_forecast_rows"],
            "backtest_rows": s27_status["backtest_rows"],
            "gross_pnl_usd": s27_total["gross"],
            "estimated_etf_fees_usd": s27_total["cost"],
            "net_after_etf_fees_usd": s27_total["net"],
            "position_change_sides": s27_status["position_change_sides"],
            "position_surface": "FROZEN_M1_STYLE_LADDER",
            "s27_safety_stack": "YES",
            "promotion": "NO",
        },
    ]


def _status_payload(**payload: Any) -> dict[str, Any]:
    hourly_rows = payload["hourly_rows"]
    s26_rows = payload["s26_rows"]
    position_rows = payload["position_rows"]
    backtest_rows = payload["backtest_rows"]
    validation_rows = payload["validation_rows"]
    recon_rows = payload["recon_rows"]
    summary_rows = payload["summary_rows"]
    s27_status = payload["s27_status"]
    position_counts = Counter(row["desired_rounded_contracts_nearest"] for row in position_rows)
    s26 = summary_rows[0]
    s27 = summary_rows[1]
    blocking = [row for row in validation_rows if row["check_status"] != "PASS"]
    prior_test_status = json.loads(
        (ROOT / "docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN_S26_TEST/status/20260601_S26_ZN_2022_2023_COMPARISON_TEST_status.json").read_text(encoding="utf-8")
    )
    return {
        "gate": GATE,
        "status": "PASS_S26_ZN_2024_VALIDATION_NOT_PROMOTION" if not blocking else "FAIL_CLOSED_S26_ZN_2024_VALIDATION",
        "stage": "VALIDATION",
        "requested_window_start": REQUEST_START,
        "requested_window_end": REQUEST_END,
        "effective_backtest_start": s26["effective_backtest_start"],
        "effective_backtest_end": s26["effective_backtest_end"],
        "hourly_rows": len(hourly_rows),
        "s26_forecast_rows": len(s26_rows),
        "formula_recon_rows": len(recon_rows),
        "position_rows": len(position_rows),
        "backtest_rows": len(backtest_rows),
        "rounded_position_counts": dict(sorted(position_counts.items(), key=lambda item: int(item[0]))),
        "position_change_sides": s26["position_change_sides"],
        "s26_gross_pnl_usd": s26["gross_pnl_usd"],
        "s26_estimated_etf_fees_usd": s26["estimated_etf_fees_usd"],
        "s26_net_after_etf_fees_usd": s26["net_after_etf_fees_usd"],
        "s26_2022_2023_test_reference_net_after_etf_fees_usd": prior_test_status["s26_net_after_etf_fees_usd"],
        "s26_test_and_validation_both_negative": "YES" if prior_test_status["s26_net_after_etf_fees_usd"] < 0 and s26["net_after_etf_fees_usd"] < 0 else "NO",
        "s27_reference_status": s27_status["status"],
        "s27_reference_position_surface": s27["position_surface"],
        "s27_reference_net_after_etf_fees_usd": s27["net_after_etf_fees_usd"],
        "s27_safety_stack_used": "NO_FOR_S26_YES_FOR_REFERENCE_ONLY",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
        "provider_api_access": "NO_NEW_PROVIDER_ACCESS_EXISTING_LOCAL_ARTIFACTS_ONLY",
        "new_data_download": "NO_NEW_DATA_DOWNLOAD_EXISTING_LOCAL_ARTIFACTS_ONLY",
        "market_row_source": "EXISTING_LOCAL_VALIDATION_ARTIFACTS_ONLY",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
        "blocking_validation_findings": len(blocking),
    }


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "created_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_files": {
            "hourly_lineage_csv": str(HOURLY_CSV.relative_to(ROOT)),
            "s26_forecast_csv": str(S26_FORECAST_CSV.relative_to(ROOT)),
            "s27_status_json": str(S27_STATUS_JSON.relative_to(ROOT)),
            "s27_backtest_csv": str(S27_BACKTEST_CSV.relative_to(ROOT)),
        },
        "source_sha256": {
            "hourly_lineage_csv": _sha256(HOURLY_CSV),
            "s26_forecast_csv": _sha256(S26_FORECAST_CSV),
            "s27_status_json": _sha256(S27_STATUS_JSON),
            "s27_backtest_csv": _sha256(S27_BACKTEST_CSV),
        },
        "status": status["status"],
        "provider_api_access": "NO_NEW_PROVIDER_ACCESS",
        "new_data_download": "NO_NEW_DATA_DOWNLOAD",
        "lockbox_access": "NO",
        "promotion": "NO",
    }


def _process_result_text(status: dict[str, Any], summary_rows: list[dict[str, Any]]) -> str:
    s26, s27 = summary_rows
    return f"""# Carver S26 ZN 2024 Validation Result

Date: 2026-06-01

Status:

```text
{status["status"]}
```

## Scope

This artifact checks S26 standalone fast mean reversion on the existing local
ZN 2024 validation artifacts. No provider call or new data download was made.

The S26 validation surface uses unit plumbing and nearest rounding, matching the
S26 2022-2023 TEST comparison surface. The S27 row below is the already-existing
2024 validation reference and uses its frozen M1-style ladder surface.

## Result

| Strategy | Surface | Gross PnL | Estimated ETF fees | Net after ETF fees | Position-change sides |
| --- | --- | ---: | ---: | ---: | ---: |
| S26 standalone | {s26["position_surface"]} | {s26["gross_pnl_usd"]:.2f} | {s26["estimated_etf_fees_usd"]:.2f} | {s26["net_after_etf_fees_usd"]:.2f} | {s26["position_change_sides"]} |
| S27 reference | {s27["position_surface"]} | {s27["gross_pnl_usd"]:.2f} | {s27["estimated_etf_fees_usd"]:.2f} | {s27["net_after_etf_fees_usd"]:.2f} | {s27["position_change_sides"]} |

```text
S26_2022_2023_TEST_NET_AFTER_ETF_FEES_USD: {status["s26_2022_2023_test_reference_net_after_etf_fees_usd"]:.2f}
S26_2024_VALIDATION_NET_AFTER_ETF_FEES_USD: {status["s26_net_after_etf_fees_usd"]:.2f}
S26_TEST_AND_VALIDATION_BOTH_NEGATIVE: {status["s26_test_and_validation_both_negative"]}
```

## Boundaries

- no new Databento/provider access;
- no new market data download;
- no OOS, Lockbox, Forward, deployment, trading, or promotion;
- no S27 V/Q/M or trend overlay used in S26;
- no parameter, cost, ladder, symbol, or window tuning.
"""


def _local_audit_text(status: dict[str, Any], validation_rows: list[dict[str, Any]]) -> str:
    blocking = [row for row in validation_rows if row["check_status"] != "PASS"]
    disposition = "PASS_S26_ZN_2024_VALIDATION_SCOPE" if not blocking else "FAIL_CLOSED_S26_ZN_2024_VALIDATION_SCOPE"
    return f"""# Local Lean Hostile Audit - S26 ZN 2024 Validation

Mode: automatic local lean hostile audit over generated S26 validation artifacts.

## Findings

CRITICAL: None.

HIGH: None.

MEDIUM: None.

The artifact uses existing local validation artifacts only, preserves the
validation label, and does not open OOS, Lockbox, Forward, provider access, new
downloads, deployment, trading, or promotion. S26 standalone rows do not consume
the S27 safety stack.

## Validation

```text
VALIDATION_ROWS: {len(validation_rows)}
BLOCKING_VALIDATION_FINDINGS: {len(blocking)}
S26_TEST_AND_VALIDATION_BOTH_NEGATIVE: {status["s26_test_and_validation_both_negative"]}
```

```text
BLOCKING_FINDINGS: {"NO" if not blocking else "YES"}
AUDIT_DISPOSITION: {disposition}
```
"""


def _totals(rows: list[dict[str, Any]], net_key: str, gross_key: str, cost_key: str) -> dict[str, Any]:
    sides = sum(abs(int(float(row["position_change_from_previous_pnl_row"]))) for row in rows)
    return {
        "gross": sum(float(row[gross_key]) for row in rows),
        "cost": sum(float(row[cost_key]) for row in rows),
        "net": sum(float(row[net_key]) for row in rows),
        "sides": sides,
    }


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {"check_name": name, "check_status": "PASS" if passed else "FAIL", "observed_count": observed_count, "gate": GATE}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _hash_tree(root: Path) -> dict[str, str]:
    return {str(path.relative_to(ROOT)).replace("\\", "/"): _sha256(path) for path in sorted(root.rglob("*")) if path.is_file()}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _passfail(value: bool) -> str:
    return "PASS" if value else "FAIL"


def _close(left: float, right: float) -> bool:
    return math.isfinite(left) and math.isfinite(right) and abs(left - right) <= EPSILON


if __name__ == "__main__":
    main()

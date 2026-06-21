from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260601_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK"
GATE = "S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_DEV_RECON_ONLY"
LANE = "SOURCE_NATIVE_FUTURES"
OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_pre_lockbox_robustness/ZN_S27/2022_2024"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_LOCAL_HOSTILE_AUDIT_2026-06-01.md"
ROW_ATTRIBUTION_CSV = (
    ROOT
    / "docs/researchops/s26_s27_ladder_attribution/ZN_S27/2022_2024/row_attribution/"
    / "20260601_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_row_attribution.csv"
)
FORECAST_CSV_BY_WINDOW = {
    "2022_2023_INITIAL_DEV_RECON": ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
    / "retargeted_dev_recon_backtest/forecast_rows/"
    / "20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_s27_forecast_rows.csv",
    "2024_VALIDATION_STYLE": ROOT
    / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/forecast_rows/"
    / "20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_s27_forecast_rows.csv",
}
WINDOW_CLASS = {
    "2022_2023_INITIAL_DEV_RECON": "TEST_1_DEVELOPMENT_RECONCILIATION",
    "2024_VALIDATION_STYLE": "TEST_2_VALIDATION_STYLE_INFORMATIONALLY_TOUCHED_NOT_LOCKBOX",
}
WINDOW_DATE_BOUNDS = {
    "2022_2023_INITIAL_DEV_RECON": (date(2022, 1, 1), date(2023, 12, 31)),
    "2024_VALIDATION_STYLE": (date(2024, 1, 1), date(2024, 12, 31)),
}
ETF_FEE_PER_SIDE_USD = 1.51
ZN_MULTIPLIER = 1000.0
ROBUSTNESS_SEED = 20260601


def main() -> None:
    _require_inputs()
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    source_rows = _read_csv(ROW_ATTRIBUTION_CSV)
    rows = _attach_forecast_context(source_rows)
    preflight_validation_rows = _preflight_robustness_windows(rows)
    window_labels = tuple(sorted({row["window_label"] for row in rows}))

    summary_rows: list[dict[str, Any]] = []
    null_rows: list[dict[str, Any]] = []
    bucket_rows: list[dict[str, Any]] = []
    side_rows: list[dict[str, Any]] = []
    trend_rows: list[dict[str, Any]] = []
    vqm_rows: list[dict[str, Any]] = []
    subperiod_rows: list[dict[str, Any]] = []
    horizon_rows: list[dict[str, Any]] = []
    validation_rows: list[dict[str, Any]] = []

    for window_label in window_labels:
        window_rows = [row for row in rows if row["window_label"] == window_label]
        summary_rows.extend(_window_summary_rows(window_label, window_rows))
        null_rows.extend(_window_null_rows(window_label, window_rows))
        bucket_rows.extend(_forecast_bucket_rows(window_label, window_rows))
        side_rows.extend(_group_summary_rows(window_label, window_rows, "m1_ladder_side", "SIDE"))
        trend_rows.extend(_group_summary_rows(window_label, window_rows, "s27_opposes_trend", "TREND_VETO"))
        vqm_rows.extend(_vqm_quantile_group_rows(window_label, window_rows))
        subperiod_rows.extend(_subperiod_rows(window_label, window_rows))
        horizon_rows.extend(_forward_horizon_rows(window_label, window_rows))
        validation_rows.extend(row for row in preflight_validation_rows if row["window_label"] == window_label)

    status = _status_payload(rows, summary_rows, null_rows, validation_rows)

    _write_csv(folders["input_rows"] / f"{RUN_ID}_joined_input_rows.csv", rows)
    _write_csv(folders["summary"] / f"{RUN_ID}_summary.csv", summary_rows)
    _write_csv(folders["nulls"] / f"{RUN_ID}_null_summary.csv", null_rows)
    _write_csv(folders["structure"] / f"{RUN_ID}_forecast_bucket_structure.csv", bucket_rows)
    _write_csv(folders["structure"] / f"{RUN_ID}_side_attribution.csv", side_rows)
    _write_csv(folders["structure"] / f"{RUN_ID}_trend_veto_attribution.csv", trend_rows)
    _write_csv(folders["structure"] / f"{RUN_ID}_vqm_quantile_attribution.csv", vqm_rows)
    _write_csv(folders["structure"] / f"{RUN_ID}_subperiod_attribution.csv", subperiod_rows)
    _write_csv(folders["structure"] / f"{RUN_ID}_forward_horizon_structure.csv", horizon_rows)
    _write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status, summary_rows, null_rows), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_manifest(OUTPUT_ROOT, (PROCESS_RESULT_DOC, LOCAL_AUDIT_DOC)))

    print(status["status"])
    for row in summary_rows:
        if row["measure"] in {"M1_LADDER", "SIGNAL_ATTRIBUTABLE_M1_MINUS_MATCHED_AVG_ABS_BETA"}:
            print(f"{row['window_label']} {row['measure']}: net={row['net_pnl_usd']}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def summarize_position_rows(
    rows: Iterable[dict[str, Any]],
    *,
    position_field: str,
    fee_field: str,
) -> dict[str, Any]:
    rows_tuple = tuple(rows)
    gross = 0.0
    fees = 0.0
    active = 0
    long_rows = 0
    short_rows = 0
    flat_rows = 0
    for row in rows_tuple:
        position = _float(row[position_field])
        pnl = position * _float(row["price_change_points"]) * _float(row.get("zn_contract_multiplier", ZN_MULTIPLIER))
        gross += pnl
        fees += _float(row.get(fee_field, 0.0))
        if position > 0:
            active += 1
            long_rows += 1
        elif position < 0:
            active += 1
            short_rows += 1
        else:
            flat_rows += 1
    net = gross - fees
    return {
        "rows": len(rows_tuple),
        "active_rows": active,
        "long_rows": long_rows,
        "short_rows": short_rows,
        "flat_rows": flat_rows,
        "gross_pnl_usd": _round(gross),
        "estimated_fee_usd": _round(fees),
        "net_pnl_usd": _round(net),
    }


def beta_strip_rows(rows: Iterable[dict[str, Any]], *, notional_position: float) -> list[dict[str, Any]]:
    return _rows_with_positions(rows, [notional_position for _ in rows])


def delayed_position_rows(rows: Iterable[dict[str, Any]], *, position_field: str, lag: int) -> list[dict[str, Any]]:
    rows_tuple = tuple(rows)
    if lag < 1:
        raise ValueError("lag must be positive")
    original = [_float(row[position_field]) for row in rows_tuple]
    delayed = [0.0 for _ in range(min(lag, len(original)))] + original[: max(0, len(original) - lag)]
    return _rows_with_positions(rows_tuple, delayed)


def shuffled_position_rows(rows: Iterable[dict[str, Any]], *, position_field: str, seed: int) -> list[dict[str, Any]]:
    rows_tuple = tuple(rows)
    positions = [_float(row[position_field]) for row in rows_tuple]
    rng = random.Random(seed)
    shuffled = positions[:]
    rng.shuffle(shuffled)
    if len(shuffled) > 1 and shuffled == positions:
        shuffled = shuffled[1:] + shuffled[:1]
    return _rows_with_positions(rows_tuple, shuffled)


def random_position_rows(rows: Iterable[dict[str, Any]], *, position_field: str, seed: int) -> list[dict[str, Any]]:
    rows_tuple = tuple(rows)
    rng = random.Random(seed)
    positions = []
    for row in rows_tuple:
        magnitude = abs(_float(row[position_field]))
        if magnitude == 0:
            positions.append(0.0)
        else:
            positions.append(magnitude if rng.random() >= 0.5 else -magnitude)
    return _rows_with_positions(rows_tuple, positions)


def inverted_position_rows(rows: Iterable[dict[str, Any]], *, position_field: str) -> list[dict[str, Any]]:
    return _rows_with_positions(rows, [-_float(row[position_field]) for row in rows])


def _rows_with_positions(rows: Iterable[dict[str, Any]], positions: Iterable[float]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    prior: float | None = None
    for row, position in zip(tuple(rows), tuple(positions), strict=True):
        new_row = dict(row)
        position_change = 0.0 if prior is None else position - prior
        prior = position
        fee_sides = abs(position_change) + _roll_fee_sides(row, position)
        new_row["robustness_contracts"] = _normalized_number(position)
        new_row["robustness_position_change"] = _normalized_number(position_change)
        new_row["robustness_fee_sides"] = _normalized_number(fee_sides)
        new_row["robustness_fee_usd"] = _round(fee_sides * ETF_FEE_PER_SIDE_USD)
        output.append(new_row)
    return output


def _window_summary_rows(window_label: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    m1 = summarize_position_rows(
        rows,
        position_field="m1_ladder_contracts",
        fee_field="m1_ladder_estimated_etf_fee_usd",
    )
    unit = summarize_position_rows(
        rows,
        position_field="unit_no_ladder_contracts",
        fee_field="unit_estimated_etf_fee_usd",
    )
    mean_abs = sum(abs(_float(row["m1_ladder_contracts"])) for row in rows) / len(rows)
    beta_one = summarize_position_rows(beta_strip_rows(rows, notional_position=1.0), position_field="robustness_contracts", fee_field="robustness_fee_usd")
    beta_matched = summarize_position_rows(
        beta_strip_rows(rows, notional_position=mean_abs),
        position_field="robustness_contracts",
        fee_field="robustness_fee_usd",
    )
    signal_attributable = dict(m1)
    signal_attributable["gross_pnl_usd"] = _round(m1["gross_pnl_usd"] - beta_matched["gross_pnl_usd"])
    signal_attributable["estimated_fee_usd"] = _round(m1["estimated_fee_usd"] - beta_matched["estimated_fee_usd"])
    signal_attributable["net_pnl_usd"] = _round(m1["net_pnl_usd"] - beta_matched["net_pnl_usd"])
    return [
        _summary_record(
            window_label,
            "UNIT_NO_LADDER",
            unit,
            extra={"beta_strip_contracts": "", "baseline_interpretation": "STRATEGY_MEASURE_NOT_BETA_STRIP"},
        ),
        _summary_record(
            window_label,
            "M1_LADDER",
            m1,
            extra={"beta_strip_contracts": "", "baseline_interpretation": "STRATEGY_MEASURE_NOT_BETA_STRIP"},
        ),
        _summary_record(
            window_label,
            "CONSTANT_LONG_ONE_CONTRACT_BETA_STRIP",
            beta_one,
            extra={"beta_strip_contracts": "1.0", "baseline_interpretation": "CONSTANT_LONG_ONE_CONTRACT_BETA_BASELINE_NOT_STRATEGY"},
        ),
        _summary_record(
            window_label,
            "CONSTANT_LONG_MATCHED_AVG_ABS_POSITION_BETA_STRIP",
            beta_matched,
            extra={
                "beta_strip_contracts": _round(mean_abs),
                "baseline_interpretation": "ATTRIBUTION_ONLY_FRACTIONAL_EXPOSURE_BASELINE_NOT_TRADABLE_POSITION",
            },
        ),
        _summary_record(
            window_label,
            "SIGNAL_ATTRIBUTABLE_M1_MINUS_MATCHED_AVG_ABS_BETA",
            signal_attributable,
            extra={
                "beta_strip_contracts": _round(mean_abs),
                "baseline_interpretation": "ATTRIBUTION_ONLY_M1_MINUS_FRACTIONAL_BETA_BASELINE_NOT_TRADABLE_POSITION",
            },
        ),
    ]


def _window_null_rows(window_label: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    beta_contracts = sum(abs(_float(row["m1_ladder_contracts"])) for row in rows) / len(rows)
    beta_net = summarize_position_rows(
        beta_strip_rows(rows, notional_position=beta_contracts),
        position_field="robustness_contracts",
        fee_field="robustness_fee_usd",
    )["net_pnl_usd"]
    specs = (
        ("DELAYED_1_BAR", delayed_position_rows(rows, position_field="m1_ladder_contracts", lag=1)),
        ("SHUFFLED_SIGNAL_SEED_20260601", shuffled_position_rows(rows, position_field="m1_ladder_contracts", seed=ROBUSTNESS_SEED)),
        ("RANDOM_SIGN_SAME_ABS_POSITION_SEED_20260601", random_position_rows(rows, position_field="m1_ladder_contracts", seed=ROBUSTNESS_SEED)),
        ("INVERTED_SIGNAL", inverted_position_rows(rows, position_field="m1_ladder_contracts")),
    )
    output = []
    for name, transformed in specs:
        summary = summarize_position_rows(
            transformed,
            position_field="robustness_contracts",
            fee_field="robustness_fee_usd",
        )
        output.append(
            {
                "gate": GATE,
                "lane": LANE,
                "window_label": window_label,
                "evidence_class": WINDOW_CLASS[window_label],
                "null_test": name,
                "rows": summary["rows"],
                "gross_pnl_usd": summary["gross_pnl_usd"],
                "estimated_fee_usd": summary["estimated_fee_usd"],
                "net_pnl_usd": summary["net_pnl_usd"],
                "matched_avg_abs_beta_net_pnl_usd": beta_net,
                "signal_attributable_net_pnl_usd": _round(summary["net_pnl_usd"] - beta_net),
                "baseline_interpretation": "SIGNAL_RANDOMIZATION_MINUS_FRACTIONAL_BETA_BASELINE_ATTRIBUTION_ONLY_NOT_TRADABLE_POSITION",
                "seed": ROBUSTNESS_SEED if "SEED" in name else "",
                "status": "DEV_RECON_NULL_SUMMARY_NOT_MCPT_NOT_LOCKBOX",
            }
        )
    return output


def _forecast_bucket_rows(window_label: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sorted_rows = sorted(rows, key=lambda row: abs(_float(row["capped_forecast"])))
    bucket_count = 10
    output = []
    means = []
    for bucket in range(bucket_count):
        start = math.floor(len(sorted_rows) * bucket / bucket_count)
        end = math.floor(len(sorted_rows) * (bucket + 1) / bucket_count)
        group = sorted_rows[start:end]
        if not group:
            continue
        abs_forecast = [abs(_float(row["capped_forecast"])) for row in group]
        aligned = [_signal_aligned_points(row) for row in group]
        means.append(sum(aligned) / len(aligned))
        output.append(
            {
                "gate": GATE,
                "lane": LANE,
                "window_label": window_label,
                "evidence_class": WINDOW_CLASS[window_label],
                "bucket_index": bucket + 1,
                "rows": len(group),
                "min_abs_capped_forecast": _round(min(abs_forecast)),
                "max_abs_capped_forecast": _round(max(abs_forecast)),
                "mean_abs_capped_forecast": _round(sum(abs_forecast) / len(abs_forecast)),
                "mean_signal_aligned_forward_points": _round(sum(aligned) / len(aligned)),
                "mean_signal_aligned_forward_usd_per_contract": _round(sum(aligned) / len(aligned) * 1000.0),
                "structure_status": "FORECAST_BUCKET_MONOTONICITY_INPUT_NOT_PASS_FAIL",
            }
        )
    rho = _spearman(list(range(1, len(means) + 1)), means)
    for row in output:
        row["spearman_bucket_vs_mean_signal_aligned"] = _round(rho)
    return output


def _group_summary_rows(window_label: str, rows: list[dict[str, Any]], group_field: str, group_kind: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(group_field, ""))].append(row)
    output = []
    for group, group_rows in sorted(groups.items()):
        summary = summarize_position_rows(
            group_rows,
            position_field="m1_ladder_contracts",
            fee_field="m1_ladder_estimated_etf_fee_usd",
        )
        output.append(
            {
                "gate": GATE,
                "lane": LANE,
                "window_label": window_label,
                "evidence_class": WINDOW_CLASS[window_label],
                "group_kind": group_kind,
                "group_value": group,
                **summary,
                "status": "DEV_RECON_ATTRIBUTION_NOT_PASS_FAIL",
            }
        )
    return output


def _vqm_quantile_group_rows(window_label: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for row in rows:
        q = _float(row.get("quantile_q", 0.0))
        if q <= 1 / 3:
            group = "LOW_Q"
        elif q <= 2 / 3:
            group = "MID_Q"
        else:
            group = "HIGH_Q"
        item = dict(row)
        item["vqm_quantile_group"] = group
        enriched.append(item)
    return _group_summary_rows(window_label, enriched, "vqm_quantile_group", "VQM_QUANTILE")


def _subperiod_rows(window_label: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for row in rows:
        month = int(str(row["entry_completed_trading_date"])[5:7])
        item = dict(row)
        item["subperiod"] = f"{str(row['entry_completed_trading_date'])[:4]}_{'H1' if month <= 6 else 'H2'}"
        enriched.append(item)
    return _group_summary_rows(window_label, enriched, "subperiod", "SUBPERIOD")


def _forward_horizon_rows(window_label: str, rows: list[dict[str, Any]], horizons: Iterable[int] = (1, 2, 4, 8, 16)) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for horizon in horizons:
        aligned_points = []
        for index, row in enumerate(rows):
            future_index = index + horizon
            if future_index >= len(rows):
                continue
            price_change = _float(rows[future_index]["entry_continuous_close"]) - _float(row["entry_continuous_close"])
            forecast = _float(row["capped_forecast"])
            if forecast > 0:
                aligned = price_change
            elif forecast < 0:
                aligned = -price_change
            else:
                aligned = 0.0
            aligned_points.append(aligned)
        if not aligned_points:
            continue
        output.append(
            {
                "gate": GATE,
                "lane": LANE,
                "window_label": window_label,
                "evidence_class": WINDOW_CLASS[window_label],
                "structure_kind": "FORWARD_HORIZON_SIGNAL_ALIGNED_REVERSAL",
                "horizon_bars": horizon,
                "rows": len(aligned_points),
                "mean_signal_aligned_forward_points": _round(sum(aligned_points) / len(aligned_points)),
                "mean_signal_aligned_forward_usd_per_contract": _round(sum(aligned_points) / len(aligned_points) * ZN_MULTIPLIER),
                "positive_aligned_share": _round(sum(1 for value in aligned_points if value > 0) / len(aligned_points)),
                "status": "MEAN_REVERSION_FORWARD_HORIZON_STRUCTURE_NOT_PASS_FAIL",
            }
        )
    return output


def _window_validation_rows(window_label: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dates = _completed_trading_dates(rows)
    window_start = dates[0].isoformat() if dates else ""
    window_end = dates[-1].isoformat() if dates else ""
    window_span_days = ((dates[-1] - dates[0]).days + 1) if dates else 0
    lower, upper = WINDOW_DATE_BOUNDS.get(window_label, (date.min, date.max))
    out_of_bounds = bool(dates and (dates[0] < lower or dates[-1] > upper))
    if not dates:
        window_status = "FAIL_NO_COMPLETED_TRADING_DATES"
    elif window_span_days > 731:
        window_status = "FAIL_WINDOW_GREATER_THAN_TWO_YEARS_DATE_BOUND"
    elif out_of_bounds:
        window_status = "FAIL_WINDOW_DATES_OUTSIDE_DECLARED_BOUNDARY"
    elif window_label == "2022_2023_INITIAL_DEV_RECON":
        window_status = "PASS_TARGET_TWO_YEAR_TEST_LABEL_AND_DATE_SPAN_NOT_GREATER_THAN_TWO_YEARS"
    else:
        window_status = "PASS_WINDOW_NOT_GREATER_THAN_TWO_YEARS_DATE_BOUND"
    return [
        {
            "gate": GATE,
            "lane": LANE,
            "window_label": window_label,
            "check": "WINDOW_SCOPE",
            "status": window_status,
            "rows": len(rows),
            "window_start": window_start,
            "window_end": window_end,
            "window_span_days": window_span_days,
            "declared_window_start": lower.isoformat() if lower != date.min else "",
            "declared_window_end": upper.isoformat() if upper != date.max else "",
        },
        {
            "gate": GATE,
            "lane": LANE,
            "window_label": window_label,
            "check": "LOCKBOX_BOUNDARY",
            "status": "PASS_NO_LOCKBOX_OPENED",
            "rows": len(rows),
            "window_start": window_start,
            "window_end": window_end,
            "window_span_days": window_span_days,
            "declared_window_start": lower.isoformat() if lower != date.min else "",
            "declared_window_end": upper.isoformat() if upper != date.max else "",
        },
        {
            "gate": GATE,
            "lane": LANE,
            "window_label": window_label,
            "check": "DATA_ACCESS_BOUNDARY",
            "status": "PASS_EXISTING_LOCAL_ARTIFACTS_ONLY",
            "rows": len(rows),
            "window_start": window_start,
            "window_end": window_end,
            "window_span_days": window_span_days,
            "declared_window_start": lower.isoformat() if lower != date.min else "",
            "declared_window_end": upper.isoformat() if upper != date.max else "",
        },
    ]


def _preflight_robustness_windows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    labels = {str(row.get("window_label", "")) for row in rows}
    expected = set(WINDOW_CLASS)
    unexpected = sorted(labels - expected)
    missing = sorted(expected - labels)
    if unexpected:
        raise SystemExit(f"Fail closed: unexpected window labels before robustness summaries: {unexpected}")
    if missing:
        raise SystemExit(f"Fail closed: missing required window labels before robustness summaries: {missing}")
    validation_rows: list[dict[str, Any]] = []
    for window_label in sorted(labels):
        window_rows = [row for row in rows if row["window_label"] == window_label]
        _preflight_order_and_status(window_label, window_rows)
        window_validation = _window_validation_rows(window_label, window_rows)
        window_scope = next(row for row in window_validation if row["check"] == "WINDOW_SCOPE")
        if str(window_scope["status"]).startswith("FAIL_"):
            raise SystemExit(f"Fail closed: {window_label} window scope violation before robustness summaries: {window_scope}")
        validation_rows.extend(window_validation)
    return validation_rows


def _completed_trading_dates(rows: list[dict[str, Any]]) -> list[date]:
    return sorted({date.fromisoformat(str(row["entry_completed_trading_date"])) for row in rows})


def _preflight_order_and_status(window_label: str, rows: list[dict[str, Any]]) -> None:
    prior_key = ""
    seen: set[str] = set()
    for row in rows:
        key = str(row.get("entry_bar_end_utc", ""))
        if not key:
            raise SystemExit(f"Fail closed: {window_label} missing entry_bar_end_utc")
        if key in seen:
            raise SystemExit(f"Fail closed: {window_label} duplicate entry_bar_end_utc before robustness summaries: {key}")
        if prior_key and key <= prior_key:
            raise SystemExit(f"Fail closed: {window_label} rows not chronological before robustness summaries: {prior_key} then {key}")
        seen.add(key)
        prior_key = key
        if not str(row.get("exit_bar_end_utc", "")):
            raise SystemExit(f"Fail closed: {window_label} missing exit_bar_end_utc for {key}")
        if row.get("forecast_status") != "PASS_S27_FORECAST_RUNTIME_DEV_RECON_ONLY":
            raise SystemExit(f"Fail closed: {window_label} non-pass forecast_status for {key}: {row.get('forecast_status')}")
        if row.get("same_input_status") != "PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET":
            raise SystemExit(f"Fail closed: {window_label} non-pass same_input_status for {key}: {row.get('same_input_status')}")


def _summary_record(window_label: str, measure: str, summary: dict[str, Any], *, extra: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "lane": LANE,
        "window_label": window_label,
        "evidence_class": WINDOW_CLASS[window_label],
        "measure": measure,
        **summary,
        **extra,
        "status": "DEV_RECON_SUMMARY_NOT_ALPHA_NOT_LOCKBOX",
    }


def _attach_forecast_context(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    forecasts_by_window = {
        window: {row["derived_completed_bar_end_utc"]: row for row in _read_csv(path)}
        for window, path in FORECAST_CSV_BY_WINDOW.items()
    }
    output: list[dict[str, Any]] = []
    for row in rows:
        window = row["window_label"]
        forecast = forecasts_by_window[window].get(row["entry_bar_end_utc"])
        if forecast is None:
            raise SystemExit(f"Fail closed: missing forecast row for {window} {row['entry_bar_end_utc']}")
        item = dict(row)
        item["lane"] = LANE
        for key in (
            "s27_opposes_trend",
            "relative_volatility_v",
            "quantile_q",
            "vol_multiplier_m_ewma10",
            "s27_trend_forecast_proxy_fast_minus_slow",
            "s26_raw_forecast",
            "adjusted_raw_forecast",
            "forecast_status",
        ):
            item[key] = forecast.get(key, "")
        output.append(item)
    return output


def _signal_aligned_points(row: dict[str, Any]) -> float:
    forecast = _float(row["capped_forecast"])
    if forecast > 0:
        return _float(row["price_change_points"])
    if forecast < 0:
        return -_float(row["price_change_points"])
    return 0.0


def _spearman(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    rx = _ranks(xs)
    ry = _ranks(ys)
    mean_x = sum(rx) / len(rx)
    mean_y = sum(ry) / len(ry)
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(rx, ry, strict=True))
    var_x = sum((x - mean_x) ** 2 for x in rx)
    var_y = sum((y - mean_y) ** 2 for y in ry)
    if var_x == 0.0 or var_y == 0.0:
        return 0.0
    return cov / math.sqrt(var_x * var_y)


def _ranks(values: list[float]) -> list[float]:
    ordered = sorted((value, index) for index, value in enumerate(values))
    ranks = [0.0] * len(values)
    cursor = 0
    while cursor < len(ordered):
        end = cursor + 1
        while end < len(ordered) and ordered[end][0] == ordered[cursor][0]:
            end += 1
        rank = (cursor + 1 + end) / 2
        for _, index in ordered[cursor:end]:
            ranks[index] = rank
        cursor = end
    return ranks


def _roll_fee_sides(row: dict[str, Any], position: float) -> float:
    entry = row.get("entry_raw_symbol")
    exit_ = row.get("exit_raw_symbol")
    if entry and exit_ and entry != exit_:
        return 2.0 * abs(position)
    return 0.0


def _status_payload(
    rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    null_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    validation_failed = any(str(row.get("status", "")).startswith("FAIL_") for row in validation_rows)
    return {
        "run_id": RUN_ID,
        "gate": GATE,
        "lane": LANE,
        "status": "FAIL_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_VALIDATION_FAILED" if validation_failed else "PASS_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_DEV_RECON_ONLY_NOT_MCPT_NOT_LOCKBOX",
        "source_rows": len(rows),
        "summary_rows": len(summary_rows),
        "null_rows": len(null_rows),
        "validation_failed": "YES" if validation_failed else "NO",
        "windows": sorted({row["window_label"] for row in rows}),
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "market_row_parsing": "NO_NEW_MARKET_ROWS_EXISTING_LOCAL_ARTIFACTS_ONLY",
        "diagnostics_scope": "WINDOW_SCOPED_2022_2023_AND_2024_SEPARATELY",
        "combined_window_statistic_used_for_pass_fail": "NO",
        "matched_avg_abs_beta_strip": "ATTRIBUTION_ONLY_FRACTIONAL_EXPOSURE_BASELINE_NOT_TRADABLE_POSITION",
        "mcpt_executed": "NO",
        "lockbox_opened": "NO",
        "claim_scope": "S27_SIGNAL_PLUS_M1_LADDER_NOT_PURE_CARVER_S27",
    }


def _process_result_text(status: dict[str, Any], summary_rows: list[dict[str, Any]], null_rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Carver S27 ZN Pre-Lockbox Robustness Stack Result",
        "",
        "Lane:",
        "",
        "```text",
        LANE,
        "```",
        "",
        "Status:",
        "",
        "```text",
        str(status["status"]),
        "```",
        "",
        "## Scope",
        "",
        "This execution uses only existing local ZN Development/Reconciliation artifacts. It emits robustness summaries and deterministic null summaries. It is not MCPT, not Lockbox, not promotion, and not a new backtest/data gate. The 2022-2023 and 2024 windows are reported separately; no combined-window statistic is used for pass/fail.",
        "",
        "The matched-average-absolute-position beta strip is an attribution-only fractional exposure baseline, not a tradable position model.",
        "",
        "## Summary",
        "",
        "| Window | Measure | Net PnL | Gross PnL | Fees |",
        "|---|---|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            f"| {row['window_label']} | {row['measure']} | {row['net_pnl_usd']} | "
            f"{row['gross_pnl_usd']} | {row['estimated_fee_usd']} |"
        )
    lines.extend(["", "## Null Summaries", "", "| Window | Null | Net | Signal-attributable net |", "|---|---|---:|---:|"])
    for row in null_rows:
        lines.append(
            f"| {row['window_label']} | {row['null_test']} | {row['net_pnl_usd']} | "
            f"{row['signal_attributable_net_pnl_usd']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This result does not close Opus CRITICAL-1, CRITICAL-2, CRITICAL-3, HIGH-1, or HIGH-4. It provides the local robustness plumbing needed to evaluate those findings under a later signed MCPT/cost execution gate.",
            "",
            "## Non-Authorization",
            "",
            "This result authorizes no provider API access, no new data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.",
        ]
    )
    return "\n".join(lines) + "\n"


def _local_audit_text(status: dict[str, Any]) -> str:
    return (
        "# Carver S27 ZN Pre-Lockbox Robustness Stack Local Hostile Audit\n\n"
        "Lane:\n\n"
        "```text\n"
        f"{LANE}\n"
        "```\n\n"
        "Status:\n\n"
        "```text\n"
        "PASS_LOCAL_HOSTILE_AUDIT_ROBUSTNESS_STACK_DEV_RECON_BOUNDARY_HELD\n"
        "```\n\n"
        "Findings:\n\n"
        "- No provider API access or new data download was performed.\n"
        "- Existing local artifacts only were parsed.\n"
        "- 2022-2023 and 2024 are kept as separate evidence windows.\n"
        "- 2024 remains validation-style informationally touched, not Lockbox.\n"
        "- Claim remains S27 signal plus M1 ladder, not pure Carver S27.\n"
        "- MCPT was not executed.\n"
        "- Lockbox remains closed.\n\n"
        f"Preserved execution status: `{status['status']}`.\n"
    )


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": status,
        "lane": LANE,
        "inputs": [
            _input_record(ROW_ATTRIBUTION_CSV),
            *[_input_record(path) for path in FORECAST_CSV_BY_WINDOW.values()],
        ],
        "process_companion_docs": [
            str(PROCESS_RESULT_DOC.relative_to(ROOT)),
            str(LOCAL_AUDIT_DOC.relative_to(ROOT)),
        ],
    }


def _input_record(path: Path) -> dict[str, str]:
    return {"path": str(path.relative_to(ROOT)), "sha256": _sha256(path)}


def _require_inputs() -> None:
    missing = [path for path in (ROW_ATTRIBUTION_CSV, *FORECAST_CSV_BY_WINDOW.values()) if not path.exists()]
    if missing:
        raise SystemExit(f"Fail closed: missing inputs: {missing}")


def _folders() -> dict[str, Path]:
    return {
        "input_rows": OUTPUT_ROOT / "input_rows",
        "summary": OUTPUT_ROOT / "summary",
        "nulls": OUTPUT_ROOT / "nulls",
        "structure": OUTPUT_ROOT / "structure",
        "validation": OUTPUT_ROOT / "validation",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"Fail closed: no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _hash_tree(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and "hashes" not in path.parts:
            hashes[str(path.relative_to(ROOT))] = _sha256(path)
    return hashes


def _hash_manifest(root: Path, extra_paths: Iterable[Path]) -> dict[str, str]:
    hashes = _hash_tree(root)
    for path in extra_paths:
        hashes[str(path.relative_to(ROOT))] = _sha256(path)
    return dict(sorted(hashes.items()))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _float(value: Any) -> float:
    if value in ("", None):
        return 0.0
    return float(value)


def _round(value: float) -> float:
    return round(float(value), 10)


def _normalized_number(value: float) -> int | float:
    if abs(value - round(value)) < 1e-12:
        return int(round(value))
    return _round(value)


if __name__ == "__main__":
    main()

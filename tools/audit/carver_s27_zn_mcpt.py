from __future__ import annotations

import csv
import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260601_S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK"
GATE = "S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK_DEV_RECON_ONLY"
LANE = "SOURCE_NATIVE_FUTURES"
INPUT_ROWS = (
    ROOT
    / "docs/researchops/s26_s27_pre_lockbox_robustness/ZN_S27/2022_2024/input_rows/"
    / "20260601_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_joined_input_rows.csv"
)
OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_pre_lockbox_mcpt/ZN_S27/2022_2024"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK_LOCAL_HOSTILE_AUDIT_2026-06-01.md"
PROTOCOL_DRAFT = ROOT / "docs/process/CARVER_S27_ZN_ROBUSTNESS_PROTOCOL_PREDECLARATION_DRAFT_2026-06-01.md"

WINDOW_CLASS = {
    "2022_2023_INITIAL_DEV_RECON": "TEST_1_DEVELOPMENT_RECONCILIATION",
    "2024_VALIDATION_STYLE": "TEST_2_VALIDATION_STYLE_INFORMATIONALLY_TOUCHED_NOT_LOCKBOX",
}
WINDOW_DATE_BOUNDS = {
    "2022_2023_INITIAL_DEV_RECON": (date(2022, 1, 1), date(2023, 12, 31)),
    "2024_VALIDATION_STYLE": (date(2024, 1, 1), date(2024, 12, 31)),
}
B_PRIMARY = 9999
STATIONARY_MEAN_BLOCK_LENGTH = 24
ETF_FEE_PER_SIDE_USD = 1.51
ZN_MULTIPLIER = 1000.0


def main() -> None:
    _require_inputs()
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    rows = _read_csv(INPUT_ROWS)
    preflight_rows(rows)
    seed = _seed_from_protocol()
    protocol_hash = _protocol_hash()
    primary_rows: list[dict[str, Any]] = []
    secondary_rows: list[dict[str, Any]] = []
    mcpt_rows: list[dict[str, Any]] = []

    labels = sorted({row["window_label"] for row in rows})

    for index, window_label in enumerate(labels):
        window_rows = [row for row in rows if row["window_label"] == window_label]
        result = run_window_mcpt(window_label, window_rows, seed + index)
        primary_rows.extend(result["primary_null_rows"])
        secondary_rows.extend(result["secondary_null_rows"])
        mcpt_rows.append(result["mcpt_summary"])

    status = _status_payload(rows, seed, protocol_hash, mcpt_rows)

    _write_csv(folders["primary_nulls"] / f"{RUN_ID}_primary_null_summary.csv", primary_rows)
    _write_csv(folders["secondary_nulls"] / f"{RUN_ID}_secondary_null_summary.csv", secondary_rows)
    _write_csv(folders["summary"] / f"{RUN_ID}_mcpt_summary.csv", mcpt_rows)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status, mcpt_rows), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_manifest(OUTPUT_ROOT, (PROCESS_RESULT_DOC, LOCAL_AUDIT_DOC)))

    print(status["status"])
    for row in mcpt_rows:
        print(
            f"{row['window_label']} observed={row['observed_signal_attributable_net_pnl_usd']} "
            f"min_primary_p={row['min_primary_unadjusted_p']} max_t_p={row['max_t_adjusted_p']}"
        )
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def run_window_mcpt(window_label: str, rows: list[dict[str, str]], seed: int) -> dict[str, Any]:
    data = _arrays(rows)
    rng = np.random.default_rng(seed)
    observed = signal_attributable_statistic(
        data["positions"],
        data["returns"],
        data["m1_fees"],
        data["beta_contracts"],
        data["beta_fees"],
    )
    primary_nulls = {
        "CIRCULAR_SHIFT_SIGNAL": circular_shift_null_statistics(data, rng, B_PRIMARY),
        "STATIONARY_BLOCK_BOOTSTRAP_RETURNS": stationary_block_bootstrap_null_statistics(data, rng, B_PRIMARY),
        "SHUFFLED_SIGNAL": shuffled_signal_null_statistics(data, rng, B_PRIMARY),
        "RANDOM_SIGN_SAME_ABS_POSITION": random_sign_null_statistics(data, rng, B_PRIMARY),
    }
    delayed = delayed_signal_statistic(data, lag=1)
    inverted = signal_attributable_statistic(
        -data["positions"],
        data["returns"],
        position_fee_usd(-data["positions"], data["roll_fee_side_units"]),
        data["beta_contracts"],
        data["beta_fees"],
    )
    max_t_p = max_t_adjusted_p_value(observed, primary_nulls)
    primary_rows = [
        _primary_null_record(window_label, name, observed, values, max_t_p)
        for name, values in primary_nulls.items()
    ]
    secondary_rows = [
        _secondary_null_record(window_label, "DELAYED_1_BAR", observed, delayed),
        _secondary_null_record(window_label, "INVERTED_SIGNAL", observed, inverted),
    ]
    min_p = min(row["unadjusted_p"] for row in primary_rows)
    summary = {
        "gate": GATE,
        "lane": LANE,
        "window_label": window_label,
        "evidence_class": WINDOW_CLASS[window_label],
        "rows": len(rows),
        "b_primary": B_PRIMARY,
        "stationary_mean_block_length": STATIONARY_MEAN_BLOCK_LENGTH,
        "observed_signal_attributable_net_pnl_usd": _round(observed),
        "min_primary_unadjusted_p": min_p,
        "max_t_adjusted_p": max_t_p,
        "mcpt_interpretation": mcpt_interpretation(window_label, max_t_p),
        "delayed_1_bar_signal_attributable_net_pnl_usd": _round(delayed),
        "inverted_signal_attributable_net_pnl_usd": _round(inverted),
        "status": "DEV_RECON_MCPT_NULL_STACK_NOT_LOCKBOX_NOT_PROMOTION",
    }
    return {
        "primary_null_rows": primary_rows,
        "secondary_null_rows": secondary_rows,
        "mcpt_summary": summary,
    }


def one_sided_upper_p_value(observed: float, null_values: np.ndarray) -> float:
    return _round((1.0 + float(np.sum(null_values >= observed))) / (len(null_values) + 1.0))


def max_t_adjusted_p_value(observed: float, nulls_by_family: dict[str, np.ndarray]) -> float:
    lengths = {len(values) for values in nulls_by_family.values()}
    if len(lengths) != 1:
        raise ValueError("all null families must have the same trial count")
    trialwise_max = np.maximum.reduce([values for values in nulls_by_family.values()])
    return one_sided_upper_p_value(observed, trialwise_max)


def preflight_rows(rows: list[dict[str, str]]) -> None:
    labels = {row.get("window_label", "") for row in rows}
    if labels != set(WINDOW_CLASS):
        raise SystemExit(f"Fail closed: unexpected MCPT windows {sorted(labels)}")
    for window_label, (lower, upper) in WINDOW_DATE_BOUNDS.items():
        window_rows = [row for row in rows if row["window_label"] == window_label]
        _preflight_order_and_status(window_label, window_rows)
        dates = sorted(date.fromisoformat(row["entry_completed_trading_date"]) for row in window_rows)
        if not dates:
            raise SystemExit(f"Fail closed: no MCPT rows for {window_label}")
        if dates[0] < lower or dates[-1] > upper:
            raise SystemExit(f"Fail closed: {window_label} outside declared MCPT bounds {dates[0]}..{dates[-1]}")
        if (dates[-1] - dates[0]).days + 1 > 731:
            raise SystemExit(f"Fail closed: {window_label} exceeds two-year diagnostic guard")


def _preflight_order_and_status(window_label: str, rows: list[dict[str, str]]) -> None:
    prior_key = ""
    seen: set[str] = set()
    for row in rows:
        key = str(row.get("entry_bar_end_utc", ""))
        if not key:
            raise SystemExit(f"Fail closed: {window_label} missing entry_bar_end_utc")
        if key in seen:
            raise SystemExit(f"Fail closed: {window_label} duplicate entry_bar_end_utc before MCPT: {key}")
        if prior_key and key <= prior_key:
            raise SystemExit(f"Fail closed: {window_label} rows not chronological before MCPT: {prior_key} then {key}")
        seen.add(key)
        prior_key = key
        if not str(row.get("exit_bar_end_utc", "")):
            raise SystemExit(f"Fail closed: {window_label} missing exit_bar_end_utc for {key}")
        if row.get("forecast_status") != "PASS_S27_FORECAST_RUNTIME_DEV_RECON_ONLY":
            raise SystemExit(f"Fail closed: {window_label} non-pass forecast_status for {key}: {row.get('forecast_status')}")
        if row.get("same_input_status") != "PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET":
            raise SystemExit(f"Fail closed: {window_label} non-pass same_input_status for {key}: {row.get('same_input_status')}")


def mcpt_interpretation(window_label: str, max_t_adjusted_p: float) -> str:
    if window_label == "2024_VALIDATION_STYLE" and max_t_adjusted_p <= 0.10:
        return "TOUCHED_2024_MCPT_THRESHOLD_HIT_INFORMATIONAL_NOT_LOCKBOX"
    if max_t_adjusted_p <= 0.10:
        return "PRIMARY_TEST_WINDOW_SIGNIFICANT_PRE_LOCKBOX_ONLY"
    return "PRIMARY_TEST_WINDOW_NOT_SIGNIFICANT_NOT_LOCKBOX"


def position_fee_usd(positions: np.ndarray, roll_fee_side_units: np.ndarray) -> float:
    changes = np.zeros_like(positions, dtype=float)
    if len(positions) > 1:
        changes[1:] = np.diff(positions)
    fee_sides = np.abs(changes) + (roll_fee_side_units * np.abs(positions))
    return _round(float(np.sum(fee_sides) * ETF_FEE_PER_SIDE_USD))


def stationary_block_bootstrap_indices(n: int, *, mean_block_length: int, rng: np.random.Generator) -> np.ndarray:
    if n <= 0:
        raise ValueError("n must be positive")
    if mean_block_length <= 0:
        raise ValueError("mean_block_length must be positive")
    indices = np.empty(n, dtype=np.int64)
    cursor = int(rng.integers(0, n))
    restart_probability = 1.0 / float(mean_block_length)
    for index in range(n):
        if index > 0:
            if rng.random() < restart_probability:
                cursor = int(rng.integers(0, n))
            else:
                cursor = (cursor + 1) % n
        indices[index] = cursor
    return indices


def signal_attributable_statistic(
    positions: np.ndarray,
    returns: np.ndarray,
    position_fees: float,
    beta_contracts: float,
    beta_fees: float,
) -> float:
    active_net = float(np.dot(positions, returns) - position_fees)
    beta_net = float(beta_contracts * np.sum(returns) - beta_fees)
    return _round(active_net - beta_net)


def circular_shift_null_statistics(data: dict[str, Any], rng: np.random.Generator, trials: int) -> np.ndarray:
    positions = data["positions"]
    returns = data["returns"]
    output = np.empty(trials, dtype=float)
    for trial in range(trials):
        shift = int(rng.integers(1, len(positions)))
        shifted = np.roll(positions, shift)
        output[trial] = signal_attributable_statistic(
            shifted,
            returns,
            position_fee_usd(shifted, data["roll_fee_side_units"]),
            data["beta_contracts"],
            data["beta_fees"],
        )
    return output


def stationary_block_bootstrap_null_statistics(data: dict[str, Any], rng: np.random.Generator, trials: int) -> np.ndarray:
    positions = data["positions"]
    output = np.empty(trials, dtype=float)
    for trial in range(trials):
        indices = stationary_block_bootstrap_indices(len(data["returns"]), mean_block_length=STATIONARY_MEAN_BLOCK_LENGTH, rng=rng)
        returns = data["returns"][indices]
        output[trial] = signal_attributable_statistic(
            positions,
            returns,
            data["m1_fees"],
            data["beta_contracts"],
            data["beta_fees"],
        )
    return output


def shuffled_signal_null_statistics(data: dict[str, Any], rng: np.random.Generator, trials: int) -> np.ndarray:
    positions = data["positions"]
    returns = data["returns"]
    output = np.empty(trials, dtype=float)
    for trial in range(trials):
        shuffled = rng.permutation(positions)
        output[trial] = signal_attributable_statistic(
            shuffled,
            returns,
            position_fee_usd(shuffled, data["roll_fee_side_units"]),
            data["beta_contracts"],
            data["beta_fees"],
        )
    return output


def random_sign_null_statistics(data: dict[str, Any], rng: np.random.Generator, trials: int) -> np.ndarray:
    magnitudes = np.abs(data["positions"])
    returns = data["returns"]
    output = np.empty(trials, dtype=float)
    for trial in range(trials):
        signs = np.where(rng.random(len(magnitudes)) >= 0.5, 1.0, -1.0)
        randomized = magnitudes * signs
        randomized[magnitudes == 0.0] = 0.0
        output[trial] = signal_attributable_statistic(
            randomized,
            returns,
            position_fee_usd(randomized, data["roll_fee_side_units"]),
            data["beta_contracts"],
            data["beta_fees"],
        )
    return output


def delayed_signal_statistic(data: dict[str, Any], *, lag: int) -> float:
    positions = data["positions"]
    delayed = np.zeros_like(positions)
    if lag < len(positions):
        delayed[lag:] = positions[:-lag]
    return signal_attributable_statistic(
        delayed,
        data["returns"],
        position_fee_usd(delayed, data["roll_fee_side_units"]),
        data["beta_contracts"],
        data["beta_fees"],
    )


def _arrays(rows: list[dict[str, str]]) -> dict[str, Any]:
    positions = np.array([_float(row["m1_ladder_contracts"]) for row in rows], dtype=float)
    returns = np.array([_float(row["price_change_points"]) * _float(row.get("zn_contract_multiplier", ZN_MULTIPLIER)) for row in rows], dtype=float)
    m1_fees = float(sum(_float(row["m1_ladder_estimated_etf_fee_usd"]) for row in rows))
    roll_fee_side_units = np.array([2.0 if row.get("entry_raw_symbol") and row.get("exit_raw_symbol") and row["entry_raw_symbol"] != row["exit_raw_symbol"] else 0.0 for row in rows], dtype=float)
    beta_contracts = float(np.mean(np.abs(positions)))
    beta_fees = position_fee_usd(np.full(len(positions), beta_contracts), roll_fee_side_units)
    return {
        "positions": positions,
        "returns": returns,
        "m1_fees": m1_fees,
        "roll_fee_side_units": roll_fee_side_units,
        "beta_contracts": beta_contracts,
        "beta_fees": beta_fees,
    }


def _primary_null_record(window_label: str, name: str, observed: float, values: np.ndarray, max_t_p: float) -> dict[str, Any]:
    return {
        "gate": GATE,
        "lane": LANE,
        "window_label": window_label,
        "evidence_class": WINDOW_CLASS[window_label],
        "null_family": name,
        "b": len(values),
        "observed_signal_attributable_net_pnl_usd": _round(observed),
        "null_mean": _round(float(np.mean(values))),
        "null_p50": _round(float(np.quantile(values, 0.50))),
        "null_p95": _round(float(np.quantile(values, 0.95))),
        "null_p99": _round(float(np.quantile(values, 0.99))),
        "null_max": _round(float(np.max(values))),
        "unadjusted_p": one_sided_upper_p_value(observed, values),
        "max_t_adjusted_p": max_t_p,
        "status": "PRIMARY_MCPT_NULL_NOT_LOCKBOX_NOT_PROMOTION",
    }


def _secondary_null_record(window_label: str, name: str, observed: float, value: float) -> dict[str, Any]:
    return {
        "gate": GATE,
        "lane": LANE,
        "window_label": window_label,
        "evidence_class": WINDOW_CLASS[window_label],
        "secondary_null": name,
        "observed_signal_attributable_net_pnl_usd": _round(observed),
        "secondary_signal_attributable_net_pnl_usd": _round(value),
        "status": "SECONDARY_DETERMINISTIC_NULL_NOT_MCPT_NOT_LOCKBOX",
    }


def _status_payload(rows: list[dict[str, str]], seed: int, protocol_hash: str, summary_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate": GATE,
        "lane": LANE,
        "status": "PASS_S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK_DEV_RECON_ONLY_NOT_LOCKBOX",
        "source_rows": len(rows),
        "windows": sorted({row["window_label"] for row in rows}),
        "b_primary": B_PRIMARY,
        "primary_null_families": [
            "CIRCULAR_SHIFT_SIGNAL",
            "STATIONARY_BLOCK_BOOTSTRAP_RETURNS",
            "SHUFFLED_SIGNAL",
            "RANDOM_SIGN_SAME_ABS_POSITION",
        ],
        "secondary_nulls": ["DELAYED_1_BAR", "INVERTED_SIGNAL"],
        "stationary_mean_block_length": STATIONARY_MEAN_BLOCK_LENGTH,
        "seed": seed,
        "protocol_hash": protocol_hash,
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "market_row_parsing": "NO_NEW_MARKET_ROWS_EXISTING_LOCAL_ARTIFACTS_ONLY",
        "diagnostics_scope": "WINDOW_SCOPED_2022_2023_AND_2024_SEPARATELY",
        "combined_window_statistic_used_for_pass_fail": "NO",
        "cost_model_closed": "NO_FUTURES_REALISTIC_COST_MODEL_REMAINS_REQUIRED_BEFORE_LOCKBOX",
        "lockbox_opened": "NO",
        "claim_scope": "S27_SIGNAL_PLUS_M1_LADDER_NOT_PURE_CARVER_S27",
        "summary_rows": summary_rows,
    }


def _process_result_text(status: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Carver S27 ZN Pre-Lockbox MCPT Null Stack Result",
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
        status["status"],
        "```",
        "",
        "## Scope",
        "",
        "This run uses only existing local S27 ZN robustness input rows. It performs window-scoped MCPT-style primary null tests on signal-attributable net PnL. It is not Lockbox, not promotion, not a new data gate, and not a cost-model closeout.",
        "",
        "## MCPT Summary",
        "",
        "| Window | Observed signal-attributable net | Min primary p | Max-T adjusted p | Interpretation |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['window_label']} | {row['observed_signal_attributable_net_pnl_usd']} | "
            f"{row['min_primary_unadjusted_p']} | {row['max_t_adjusted_p']} | {row['mcpt_interpretation']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "2022-2023 and 2024 remain separate evidence windows. 2024 remains informationally touched, not Lockbox. Futures-realistic costs remain unresolved and required before any Lockbox-facing interpretation.",
            "",
            "## Non-Authorization",
            "",
            "This result authorizes no provider API access, no new data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.",
        ]
    )
    return "\n".join(lines) + "\n"


def _local_audit_text(status: dict[str, Any]) -> str:
    return (
        "# Carver S27 ZN Pre-Lockbox MCPT Null Stack Local Hostile Audit\n\n"
        "Lane:\n\n"
        "```text\n"
        f"{LANE}\n"
        "```\n\n"
        "Status:\n\n"
        "```text\n"
        "PASS_LOCAL_HOSTILE_AUDIT_MCPT_NULL_STACK_DEV_RECON_BOUNDARY_HELD\n"
        "```\n\n"
        "Findings:\n\n"
        "- Existing local robustness rows only were parsed.\n"
        "- No provider API access or new data download was performed.\n"
        "- Primary MCPT nulls are window-scoped and deterministic from the protocol hash seed.\n"
        "- No combined-window pass/fail statistic was emitted.\n"
        "- Cost model remains explicitly unresolved before Lockbox.\n"
        "- Lockbox remains closed.\n\n"
        f"Preserved execution status: `{status['status']}`.\n"
    )


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": status,
        "lane": LANE,
        "inputs": [
            _input_record(INPUT_ROWS),
            _input_record(PROTOCOL_DRAFT),
        ],
        "process_companion_docs": [
            str(PROCESS_RESULT_DOC.relative_to(ROOT)),
            str(LOCAL_AUDIT_DOC.relative_to(ROOT)),
        ],
    }


def _seed_from_protocol() -> int:
    return int(_protocol_hash()[:16], 16) % (2**32)


def _protocol_hash() -> str:
    digest = hashlib.sha256()
    digest.update(RUN_ID.encode("utf-8"))
    for path in (INPUT_ROWS, PROTOCOL_DRAFT):
        digest.update(_sha256(path).encode("ascii"))
    return digest.hexdigest().upper()


def _require_inputs() -> None:
    missing = [path for path in (INPUT_ROWS, PROTOCOL_DRAFT) if not path.exists()]
    if missing:
        raise SystemExit(f"Fail closed: missing inputs: {missing}")


def _folders() -> dict[str, Path]:
    return {
        "summary": OUTPUT_ROOT / "summary",
        "primary_nulls": OUTPUT_ROOT / "primary_nulls",
        "secondary_nulls": OUTPUT_ROOT / "secondary_nulls",
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


def _input_record(path: Path) -> dict[str, str]:
    return {"path": str(path.relative_to(ROOT)), "sha256": _sha256(path)}


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


if __name__ == "__main__":
    main()

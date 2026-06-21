from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from hashlib import sha256
from math import floor, isclose
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .development_recon_run import (
    ACCEPTED_COMMISSION_PER_CONTRACT,
    ANNUAL_TARGET_RISK,
    CAPITAL_ACCOUNT_VALUE,
    CONTRACT_POINT_VALUE,
    FORECAST_CAP_VALUE,
    FORECAST_SCALAR_VALUE,
    FORECAST_TO_POSITION_DIVISOR,
    ZN_TICK_SIZE,
)
from .local_replay import canonical_sha256
from .pre2023_development_recon_actual_pnl import VALUATION_CONVENTION_LABEL
from .validation import require_hash


AUTHORIZATION = "S27_V2_CONSOLIDATED_LOCAL_ONLY_PRE2023_EXTENDED_DEVELOPMENT_RECON_IMPLEMENTATION_AND_RUN_GATE"
STATUS = "S27_V2_PRE2023_EXTENDED_DEVELOPMENT_RECON_RUN_EMITTED_NOT_RESULT"
RESULT_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
BACKTEST_STATUS = "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"
PNL_EVALUATION_STATUS = "NOT_EMITTED_MECHANICAL_LEDGER_ROWS_ONLY"

_REPO_ROOT = Path(__file__).resolve().parents[4]
PACK_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_extended_dev_recon_2022_minimum_extended_declared_pack"
)
OUTPUT_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_runs/ZN/"
    "20260611_pre2023_extended_dev_recon_2022_minimum_extended_run"
)
_PACK_PATH = (_REPO_ROOT / PACK_RELATIVE_PATH).resolve()
_OUTPUT_PATH = (_REPO_ROOT / OUTPUT_RELATIVE_PATH).resolve()
_MANIFEST_NAME = "S27_V2_PRE2023_EXTENDED_DEV_RECON_DECLARED_INPUT_PACK_MANIFEST.json"
_EXPECTED_MANIFEST_SHA256 = "A2DD529AFD54EA7783F0C3AE935999381909B759D924079A420EAADBEE770965"

ROW_FAMILY_FILES = (
    "daily_continuous_completed_bar.csv",
    "daily_current_contract_completed_bar.csv",
    "hourly_decision_completed_bar.csv",
    "hourly_fill_completed_bar.csv",
    "valuation_mark_completed_bar.csv",
    "session_calendar.csv",
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
    "NO_RESULT_SCORED_RUN",
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


@dataclass(frozen=True)
class Pre2023MultiRowDevelopmentReconRunBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    output_root: str
    row_count: int
    final_position_contracts: int
    cumulative_gross_pnl_amount: float
    cumulative_commission_amount: float
    cumulative_spread_amount: float
    cumulative_net_pnl_amount: float
    run_manifest_hash: str
    evidence_manifest_hash: str
    trusted_bundle_hash: str
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != STATUS or self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 pre-2023 multi-row run status/authorization is not locked")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT or self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 pre-2023 multi-row run must remain S27_V2 ZN source-native futures")
        if Path(self.input_pack_path).resolve() != _PACK_PATH or Path(self.output_root).resolve() != _OUTPUT_PATH:
            raise CarverBlocked("S27 v2 pre-2023 multi-row run paths are not locked")
        if self.row_count != 10 or self.final_position_contracts != 33:
            raise CarverBlocked("S27 v2 pre-2023 multi-row run expected state is not locked")
        if not isclose(self.cumulative_gross_pnl_amount, -30312.5, rel_tol=0.0, abs_tol=1e-9):
            raise CarverBlocked("S27 v2 pre-2023 multi-row cumulative gross PnL is not locked")
        if not isclose(self.cumulative_commission_amount, 75.9, rel_tol=0.0, abs_tol=1e-9):
            raise CarverBlocked("S27 v2 pre-2023 multi-row cumulative commission is not locked")
        if not isclose(self.cumulative_spread_amount, 0.0, rel_tol=0.0, abs_tol=1e-9):
            raise CarverBlocked("S27 v2 pre-2023 multi-row cumulative spread is not locked")
        if not isclose(self.cumulative_net_pnl_amount, -30388.4, rel_tol=0.0, abs_tol=1e-9):
            raise CarverBlocked("S27 v2 pre-2023 multi-row cumulative net PnL is not locked")
        for label, value in (
            ("run manifest", self.run_manifest_hash),
            ("evidence manifest", self.evidence_manifest_hash),
            ("trusted bundle", self.trusted_bundle_hash),
            ("bundle", self.bundle_hash),
        ):
            require_hash(f"S27 v2 pre-2023 multi-row {label} hash", value)
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 pre-2023 multi-row run must preserve non-authorizations")
        if self.run_manifest_hash != _sha256(_OUTPUT_PATH / "run_manifest.json"):
            raise CarverBlocked("S27 v2 pre-2023 multi-row run manifest hash must bind bytes")
        if self.evidence_manifest_hash != _sha256(_OUTPUT_PATH / "evidence_manifest.json"):
            raise CarverBlocked("S27 v2 pre-2023 multi-row evidence manifest hash must bind bytes")
        if self.trusted_bundle_hash != _sha256(_OUTPUT_PATH / "trusted_bundle.json"):
            raise CarverBlocked("S27 v2 pre-2023 multi-row trusted bundle hash must bind bytes")
        if self.bundle_hash != canonical_sha256(_bundle_payload(self)):
            raise CarverBlocked("S27 v2 pre-2023 multi-row bundle hash must be content-bound")


def run_pre2023_extended_development_recon(
    input_pack_path: str | Path = _PACK_PATH,
    output_root: str | Path = _OUTPUT_PATH,
) -> Pre2023MultiRowDevelopmentReconRunBundle:
    pack_path = Path(input_pack_path).resolve()
    out = Path(output_root).resolve()
    if pack_path != _PACK_PATH:
        raise CarverBlocked("S27 v2 pre-2023 multi-row run is locked to the audited multi-row pack")
    if out != _OUTPUT_PATH:
        raise CarverBlocked("S27 v2 pre-2023 multi-row output root is locked")
    manifest = _read_manifest(pack_path)
    rows = {filename: _read_csv_rows(pack_path / filename) for filename in ROW_FAMILY_FILES}
    _verify_manifest(manifest, rows, pack_path)
    computed = _compute_rows(pack_path, manifest, rows)
    _write_artifacts(out, pack_path, manifest, computed)
    bundle = Pre2023MultiRowDevelopmentReconRunBundle(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        output_root=str(out),
        row_count=len(computed["runtime"]),
        final_position_contracts=int(computed["pnl"][-1]["ending_position_contracts"]),
        cumulative_gross_pnl_amount=float(computed["pnl"][-1]["cumulative_gross_pnl_amount"]),
        cumulative_commission_amount=float(computed["pnl"][-1]["cumulative_commission_amount"]),
        cumulative_spread_amount=float(computed["pnl"][-1]["cumulative_spread_amount"]),
        cumulative_net_pnl_amount=float(computed["pnl"][-1]["cumulative_net_pnl_amount"]),
        run_manifest_hash=_sha256(out / "run_manifest.json"),
        evidence_manifest_hash=_sha256(out / "evidence_manifest.json"),
        trusted_bundle_hash=_sha256(out / "trusted_bundle.json"),
        bundle_hash="0" * 64,
    )
    bundle = Pre2023MultiRowDevelopmentReconRunBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_bundle_payload(bundle))}
    )
    bundle.validate()
    _write_json(out / "run_bundle.json", _plain(bundle))
    _write_sha256s(out)
    return bundle


def _read_manifest(pack_path: Path) -> dict[str, Any]:
    manifest_path = pack_path / _MANIFEST_NAME
    if _sha256(manifest_path).upper() != _EXPECTED_MANIFEST_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 multi-row manifest hash is not pinned")
    return json.loads(manifest_path.read_text(encoding="ascii"))


def _verify_manifest(manifest: dict[str, Any], rows: dict[str, list[dict[str, str]]], pack_path: Path) -> None:
    if manifest["status"] != "LOCAL_PRE2023_EXTENDED_DEV_RECON_PACK_DECLARED_NOT_RESULT":
        raise CarverBlocked("S27 v2 pre-2023 multi-row pack status is not locked")
    for forbidden in ("NO_2023_TEST_DATA", "NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"):
        if forbidden not in manifest["explicitly_excluded_data"]:
            raise CarverBlocked("S27 v2 pre-2023 multi-row protected window exclusion is missing")
    if len(manifest["decision_fill_mark_plan"]) != 10:
        raise CarverBlocked("S27 v2 pre-2023 extended pack must be the minimum ten-row two-session slice")
    for filename in ROW_FAMILY_FILES:
        expected = manifest["row_family_files"][filename]["sha256"]
        if str(expected).upper() != _sha256(pack_path / filename).upper():
            raise CarverBlocked("S27 v2 pre-2023 multi-row row-family bytes must match manifest")
    if len(rows["hourly_decision_completed_bar.csv"]) != 10 or len(rows["hourly_fill_completed_bar.csv"]) != 10:
        raise CarverBlocked("S27 v2 pre-2023 extended pack must contain ten decision/fill rows")
    if len(rows["valuation_mark_completed_bar.csv"]) != 10:
        raise CarverBlocked("S27 v2 pre-2023 extended pack must contain ten valuation marks")


def _compute_rows(pack_path: Path, manifest: dict[str, Any], rows: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, Any]]]:
    daily = rows["daily_continuous_completed_bar.csv"]
    current_daily = rows["daily_current_contract_completed_bar.csv"][0]
    decisions = rows["hourly_decision_completed_bar.csv"]
    fills = rows["hourly_fill_completed_bar.csv"]
    marks = rows["valuation_mark_completed_bar.csv"]
    cost = rows["cost_parameter.csv"][0]
    closes = tuple(float(row["close_price"]) for row in daily)
    ewma5 = _ewma(closes, 5)
    trend = _ewma(closes, 16) - _ewma(closes, 64)
    sigma = float(daily[-1]["annual_percentage_sigma"])
    sigma_price = float(current_daily["close_price"]) * sigma / 16.0
    multiplier_m = float(manifest["history_evidence"]["selected_vqm_multiplier_m"])
    current_position = 0
    last_mark_price: float | None = None
    cumulative_gross = 0.0
    cumulative_commission = 0.0
    cumulative_spread = 0.0
    out: dict[str, list[dict[str, Any]]] = {
        name: []
        for name in ("runtime", "forecast", "position", "order", "market", "transition", "fill", "cost", "pnl", "validation")
    }
    for index, (decision, fill, mark) in enumerate(zip(decisions, fills, marks, strict=True), 1):
        decision_price = float(decision["close_price"])
        raw_forecast = ewma5 - decision_price
        risk_before_veto = raw_forecast / sigma_price
        risk_after_veto = 0.0 if risk_before_veto * trend < 0.0 else risk_before_veto
        capped_forecast = _clamp(risk_after_veto * multiplier_m * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)
        base_position = CAPITAL_ACCOUNT_VALUE * ANNUAL_TARGET_RISK / (decision_price * CONTRACT_POINT_VALUE * sigma)
        desired_unrounded = base_position * capped_forecast / FORECAST_TO_POSITION_DIVISOR
        desired_position = _round_half_away_from_zero(desired_unrounded)
        starting_position = current_position
        position_change = desired_position - starting_position
        side = "BUY" if position_change > 0 else "SELL" if position_change < 0 else "NONE"
        order_quantity = abs(position_change)
        adjacent_target = starting_position + (1 if position_change > 0 else -1 if position_change < 0 else 0)
        formula_limit = _formula_limit(adjacent_target, base_position, ewma5, sigma_price, multiplier_m, trend) if side != "NONE" else 0.0
        limit_price = _round_limit(formula_limit, side) if side != "NONE" else 0.0
        fill_close = float(fill["close_price"])
        filled = _limit_fill(side, fill_close, limit_price)
        fill_quantity = order_quantity if filled else 0
        signed_fill = fill_quantity if side == "BUY" else -fill_quantity if side == "SELL" else 0
        current_position = starting_position + signed_fill
        mark_price = float(mark["close_price"])
        existing_gross = 0.0 if last_mark_price is None else starting_position * (mark_price - last_mark_price) * CONTRACT_POINT_VALUE
        fill_gross = signed_fill * (mark_price - limit_price) * CONTRACT_POINT_VALUE if filled else 0.0
        row_gross = existing_gross + fill_gross
        commission = ACCEPTED_COMMISSION_PER_CONTRACT * abs(fill_quantity)
        spread = 0.0
        row_net = row_gross - commission - spread
        cumulative_gross += row_gross
        cumulative_commission += commission
        cumulative_spread += spread
        cumulative_net = cumulative_gross - cumulative_commission - cumulative_spread
        last_mark_price = mark_price
        out["runtime"].append(_hash_row({"row_index": index, "ewma5": ewma5, "trend": trend, "sigma": sigma, "vqm_multiplier_m": multiplier_m, "row_status": "LOCAL_RUNTIME_NUMERIC_ROW_EMITTED_NOT_RESULT"}))
        out["forecast"].append(_hash_row({"row_index": index, "decision_timestamp_utc": decision["completed_timestamp_utc"], "raw_forecast": raw_forecast, "risk_adjusted_forecast": risk_after_veto, "capped_forecast": capped_forecast, "row_status": "LOCAL_FORECAST_ROW_EMITTED_NOT_RESULT"}))
        out["position"].append(_hash_row({"row_index": index, "starting_position_contracts": starting_position, "desired_position_contracts": desired_position, "position_change_contracts": position_change, "base_position_contracts": base_position, "row_status": "LOCAL_POSITION_ROW_EMITTED_NOT_RESULT"}))
        out["order"].append(_hash_row({"row_index": index, "order_side": side, "order_quantity": order_quantity, "adjacent_target_position": adjacent_target, "formula_limit_price": formula_limit, "limit_order_price": limit_price, "row_status": "LOCAL_LIMIT_ORDER_ROW_EMITTED_NOT_RESULT"}))
        out["market"].append(_hash_row({"row_index": index, "market_order_required": False, "market_order_rows_emitted": False, "market_fallback_status": "NOT_REQUIRED_LIMIT_ORDER_FILLED_OR_NO_MARKET_CASE_TRIGGERED", "row_status": "LOCAL_NO_MARKET_ORDER_METADATA_ROW_EMITTED_NOT_RESULT"}))
        out["transition"].append(_hash_row({"row_index": index, "starting_position_contracts": starting_position, "ending_position_contracts": current_position, "working_state_before": "EMPTY" if index == 1 else "NO_OPEN_WORKING_ORDER_CARRIED", "working_state_after": "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION", "same_session": decision["session_id"] == fill["session_id"] == mark["session_id"], "row_status": "LOCAL_WORKING_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT"}))
        out["fill"].append(_hash_row({"row_index": index, "fill_executed": filled, "fill_rule": "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL", "fill_candidate_close": fill_close, "fill_price": limit_price if filled else 0.0, "fill_quantity": fill_quantity, "position_after_fill": current_position, "row_status": "LOCAL_FILL_ROW_EMITTED_NOT_RESULT"}))
        out["cost"].append(_hash_row({"row_index": index, "cost_policy_id": cost["cost_policy_id"], "commission_amount": commission, "spread_cost_amount": spread, "total_cost_amount": commission + spread, "currency": "USD", "row_status": "LOCAL_COST_ROW_EMITTED_NOT_RESULT"}))
        out["pnl"].append(_hash_row({"row_index": index, "valuation_mark_timestamp_utc": mark["completed_timestamp_utc"], "valuation_mark_close_price": mark_price, "existing_position_gross_pnl": existing_gross, "fill_gross_pnl": fill_gross, "row_gross_pnl_amount": row_gross, "row_net_pnl_amount": row_net, "cumulative_gross_pnl_amount": cumulative_gross, "cumulative_commission_amount": cumulative_commission, "cumulative_spread_amount": cumulative_spread, "cumulative_net_pnl_amount": cumulative_net, "ending_position_contracts": current_position, "result_status": RESULT_STATUS, "backtest_status": BACKTEST_STATUS, "pnl_evaluation_status": PNL_EVALUATION_STATUS, "source_faithful_evidence_claimed": False, "row_status": "LOCAL_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"}))
        out["validation"].append(_hash_row({"row_index": index, "result_status": RESULT_STATUS, "source_faithful_evidence_claimed": False, "non_authorizations": NON_AUTHORIZATIONS, "row_status": "LOCAL_VALIDATION_ROW_EMITTED_NOT_RESULT"}))
    return out


def _write_artifacts(output_root: Path, pack_path: Path, manifest: dict[str, Any], computed: dict[str, list[dict[str, Any]]]) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    files = {
        "runtime_history_ledger.csv": computed["runtime"],
        "forecast_replay_ledger.csv": computed["forecast"],
        "desired_position_ledger.csv": computed["position"],
        "limit_order_ledger.csv": computed["order"],
        "no_market_order_ledger.csv": computed["market"],
        "working_order_transition_ledger.csv": computed["transition"],
        "fill_ledger.csv": computed["fill"],
        "cost_ledger.csv": computed["cost"],
        "pnl_ledger.csv": computed["pnl"],
        "validation_ledger.csv": computed["validation"],
    }
    for name, artifact_rows in files.items():
        _write_csv(output_root / name, artifact_rows)
    run_manifest = {
        "artifact": "S27_V2_PRE2023_EXTENDED_DEVELOPMENT_RECON_RUN_MANIFEST",
        "status": STATUS,
        "authorization": AUTHORIZATION,
        "input_pack_path": str(pack_path),
        "input_manifest_sha256": _EXPECTED_MANIFEST_SHA256,
        "row_count": len(computed["pnl"]),
        "artifact_files": tuple(files),
        "non_authorizations": NON_AUTHORIZATIONS,
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
    }
    _write_json(output_root / "run_manifest.json", run_manifest)
    evidence_manifest = {
        "artifact": "S27_V2_PRE2023_EXTENDED_DEVELOPMENT_RECON_EVIDENCE_MANIFEST",
        "status": "LOCAL_EXTENDED_DEV_RECON_EVIDENCE_MANIFEST_METADATA_NOT_RESULT",
        "run_manifest_hash": _sha256(output_root / "run_manifest.json"),
        "ledger_hashes": {name: _sha256(output_root / name) for name in files},
    }
    _write_json(output_root / "evidence_manifest.json", evidence_manifest)
    trusted_bundle = {
        "artifact": "S27_V2_PRE2023_EXTENDED_DEVELOPMENT_RECON_TRUSTED_BUNDLE_METADATA",
        "status": "LOCAL_EXTENDED_DEV_RECON_TRUSTED_BUNDLE_METADATA_NOT_RESULT_NOT_PROMOTION",
        "run_manifest_hash": _sha256(output_root / "run_manifest.json"),
        "evidence_manifest_hash": _sha256(output_root / "evidence_manifest.json"),
        "final_pnl_row_hash": computed["pnl"][-1]["row_hash"],
        "result_status": RESULT_STATUS,
        "source_faithful_evidence_claimed": False,
    }
    _write_json(output_root / "trusted_bundle.json", trusted_bundle)


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise CarverBlocked("S27 v2 pre-2023 multi-row refuses empty CSV artifacts")
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(value) for key, value in row.items()})


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _write_sha256s(output_root: Path) -> None:
    rows = [
        {"relative_path": path.relative_to(output_root).as_posix(), "sha256": _sha256(path)}
        for path in sorted(output_root.iterdir())
        if path.is_file() and path.name != "SHA256SUMS.csv"
    ]
    _write_csv(output_root / "SHA256SUMS.csv", rows)


def _hash_row(row: dict[str, Any]) -> dict[str, Any]:
    row = dict(row)
    row["row_hash"] = canonical_sha256(row)
    return row


def _ewma(values: tuple[float, ...], span: int) -> float:
    alpha = 2.0 / (span + 1.0)
    current = values[0]
    for value in values[1:]:
        current = alpha * value + (1.0 - alpha) * current
    return current


def _formula_limit(target_position: int, base_position: float, ewma5: float, sigma_price: float, multiplier_m: float, trend: float) -> float:
    if target_position <= 0 or trend <= 0.0:
        raise CarverBlocked("S27 v2 pre-2023 multi-row currently locks only positive trend-permitted buy targets")
    target_capped = target_position / base_position * FORECAST_TO_POSITION_DIVISOR
    target_risk = target_capped / FORECAST_SCALAR_VALUE
    pre_vol_risk = target_risk / multiplier_m
    return ewma5 - pre_vol_risk * sigma_price


def _round_limit(price: float, side: str) -> float:
    if side == "BUY":
        return floor((price + 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    raise CarverBlocked("S27 v2 pre-2023 multi-row currently locks only buy limit rounding")


def _limit_fill(side: str, close_price: float, limit_price: float) -> bool:
    return side == "BUY" and close_price <= limit_price


def _round_half_away_from_zero(value: float) -> int:
    magnitude = floor(abs(value) + 0.5)
    return magnitude if value >= 0.0 else -magnitude


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _plain(bundle: Pre2023MultiRowDevelopmentReconRunBundle) -> dict[str, Any]:
    return dict(bundle.__dict__)


def _bundle_payload(bundle: Pre2023MultiRowDevelopmentReconRunBundle) -> dict[str, Any]:
    return {key: value for key, value in bundle.__dict__.items() if key != "bundle_hash"}

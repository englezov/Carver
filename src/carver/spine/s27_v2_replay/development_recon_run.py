from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from hashlib import sha256
from math import ceil, floor, isclose
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .validation import require_hash, require_text


S27_V2_CONTROLLED_DEV_RECON_AUTHORIZATION = "S27_V2_CONTROLLED_LOCAL_ONLY_DEVELOPMENT_RECON_RUN_PRE2023_ZN"
S27_V2_CONTROLLED_DEV_RECON_STATUS = "S27_V2_CONTROLLED_DEV_RECON_RUN_EMITTED_NOT_RESULT_NOT_PROMOTION"

FORECAST_SCALAR_VALUE = 20.0
FORECAST_CAP_VALUE = 20.0
FORECAST_TO_POSITION_DIVISOR = 10.0
CAPITAL_ACCOUNT_VALUE = 500_000.0
ANNUAL_TARGET_RISK = 0.20
CONTRACT_POINT_VALUE = 1000.0
ZN_TICK_SIZE = 0.015625
ACCEPTED_COMMISSION_PER_CONTRACT = 2.30

PNL_BLOCKED_STATUS = "FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED_VALUATION_MARK_ROW_NOT_DECLARED"
RESULT_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"

RUN_NON_AUTHORIZATIONS = (
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

ROW_FAMILY_FILES = (
    "daily_continuous_completed_bar.csv",
    "daily_current_contract_completed_bar.csv",
    "hourly_decision_completed_bar.csv",
    "hourly_fill_completed_bar.csv",
    "session_calendar.csv",
    "roll_calendar.csv",
    "cost_parameter.csv",
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
PRE2023_PACK_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_oldest_dev_recon_2022_declared_pack"
)
_PRE2023_PACK_PATH = (_REPO_ROOT / PRE2023_PACK_RELATIVE_PATH).resolve()
_PRE2023_MANIFEST_NAME = "S27_V2_PRE2023_DATABENTO_DECLARED_INPUT_PACK_MANIFEST.json"
_EXPECTED_PRE2023_MANIFEST_SHA256 = "CB8CCD4B2433BAB8255246BDE84D406F994495E5880099D2F5AD7BF766BB0504"

CONTROLLED_RUN_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_runs/ZN/"
    "20260611_pre2023_oldest_dev_recon_2022_controlled_run"
)
_CONTROLLED_RUN_PATH = (_REPO_ROOT / CONTROLLED_RUN_RELATIVE_PATH).resolve()


@dataclass(frozen=True)
class ControlledDevelopmentReconRunBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    output_root: str
    selected_decision_timestamp_utc: str
    selected_fill_timestamp_utc: str
    selected_previous_daily_timestamp_utc: str
    raw_symbol: str
    forecast_value: float
    desired_position_contracts: int
    position_change_contracts: int
    order_side: str
    order_quantity: int
    limit_order_price: float
    fill_executed: bool
    fill_price: float
    commission_amount: float
    pnl_status: str
    result_status: str
    run_manifest_hash: str
    evidence_manifest_hash: str
    trusted_bundle_hash: str
    bundle_hash: str
    non_authorizations: tuple[str, ...] = RUN_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_CONTROLLED_DEV_RECON_STATUS:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation status is not locked")
        if self.authorization_label != S27_V2_CONTROLLED_DEV_RECON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation must remain S27_V2 ZN only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation lane must remain source-native futures")
        if Path(self.input_pack_path).resolve() != _PRE2023_PACK_PATH:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation is locked to the pre-2023 ZN pack")
        output_root = Path(self.output_root).resolve()
        if output_root != _CONTROLLED_RUN_PATH:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation output root is not locked")
        for label, value in (
            ("decision timestamp", self.selected_decision_timestamp_utc),
            ("fill timestamp", self.selected_fill_timestamp_utc),
            ("previous daily timestamp", self.selected_previous_daily_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("order side", self.order_side),
            ("PnL status", self.pnl_status),
            ("result status", self.result_status),
        ):
            require_text(f"S27 v2 controlled Development/Reconciliation {label}", value)
        for label, value in (
            ("run manifest", self.run_manifest_hash),
            ("evidence manifest", self.evidence_manifest_hash),
            ("trusted bundle", self.trusted_bundle_hash),
            ("bundle", self.bundle_hash),
        ):
            require_hash(f"S27 v2 controlled Development/Reconciliation {label} hash", value)
        if self.pnl_status != PNL_BLOCKED_STATUS:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation PnL must stay blocked without mark row")
        if self.result_status != RESULT_STATUS:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation result status must remain fail-closed")
        if self.non_authorizations != RUN_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation must preserve non-authorizations")
        if self.run_manifest_hash != _sha256(output_root / "run_manifest.json"):
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation run manifest hash must bind bytes")
        if self.evidence_manifest_hash != _sha256(output_root / "evidence_manifest.json"):
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation evidence manifest hash must bind bytes")
        if self.trusted_bundle_hash != _sha256(output_root / "trusted_bundle.json"):
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation trusted bundle hash must bind bytes")
        if self.bundle_hash != canonical_sha256(_run_bundle_payload(self)):
            raise CarverBlocked("S27 v2 controlled Development/Reconciliation bundle hash must be content-bound")


def run_s27_v2_controlled_pre2023_development_recon(
    input_pack_path: str | Path = _PRE2023_PACK_PATH,
    output_root: str | Path = _CONTROLLED_RUN_PATH,
) -> ControlledDevelopmentReconRunBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _PRE2023_PACK_PATH:
        raise CarverBlocked("S27 v2 controlled Development/Reconciliation run is locked to the audited pre-2023 pack")
    out = Path(output_root).resolve()
    if out != _CONTROLLED_RUN_PATH:
        raise CarverBlocked("S27 v2 controlled Development/Reconciliation output root is locked")

    manifest = _read_manifest(pack_path)
    rows = _read_pack_rows(pack_path)
    _verify_manifest_scope(manifest)
    _verify_row_family_hashes(pack_path, manifest)
    computed = _compute_run_rows(pack_path, manifest, rows)
    _write_run_artifacts(out, pack_path, manifest, rows, computed)

    run_manifest_hash = _sha256(out / "run_manifest.json")
    evidence_manifest_hash = _sha256(out / "evidence_manifest.json")
    trusted_bundle_hash = _sha256(out / "trusted_bundle.json")
    bundle = ControlledDevelopmentReconRunBundle(
        status=S27_V2_CONTROLLED_DEV_RECON_STATUS,
        authorization_label=S27_V2_CONTROLLED_DEV_RECON_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        output_root=str(out),
        selected_decision_timestamp_utc=str(manifest["selected_decision_timestamp_utc"]),
        selected_fill_timestamp_utc=str(manifest["selected_fill_timestamp_utc"]),
        selected_previous_daily_timestamp_utc=str(manifest["selected_previous_daily_timestamp_utc"]),
        raw_symbol=str(manifest["selected_raw_symbol"]),
        forecast_value=computed["forecast"]["capped_forecast_value"],
        desired_position_contracts=int(computed["position"]["desired_position_contracts"]),
        position_change_contracts=int(computed["position"]["position_change_contracts"]),
        order_side=str(computed["order"]["order_side"]),
        order_quantity=int(computed["order"]["order_quantity"]),
        limit_order_price=float(computed["order"]["limit_order_price"]),
        fill_executed=bool(computed["fill"]["fill_executed"]),
        fill_price=float(computed["fill"]["fill_price"]),
        commission_amount=float(computed["commission"]["commission_amount"]),
        pnl_status=str(computed["pnl"]["pnl_status"]),
        result_status=str(computed["validation"]["result_status"]),
        run_manifest_hash=run_manifest_hash,
        evidence_manifest_hash=evidence_manifest_hash,
        trusted_bundle_hash=trusted_bundle_hash,
        bundle_hash="0" * 64,
    )
    bundle = ControlledDevelopmentReconRunBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_run_bundle_payload(bundle))}
    )
    bundle.validate()
    _write_json(out / "run_bundle.json", _as_plain_dict(bundle))
    _write_sha256s(out)
    return bundle


def _read_manifest(pack_path: Path) -> dict[str, Any]:
    path = pack_path / _PRE2023_MANIFEST_NAME
    if _sha256(path).upper() != _EXPECTED_PRE2023_MANIFEST_SHA256:
        raise CarverBlocked("S27 v2 controlled run manifest hash must match the audited pre-2023 pack")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise CarverBlocked("S27 v2 controlled run manifest must be a JSON object")
    return manifest


def _verify_manifest_scope(manifest: dict[str, Any]) -> None:
    if manifest.get("status") != "LOCAL_INPUT_PACK_DECLARED_FOR_2022_DEVELOPMENT_RECON_ONLY_NOT_BACKTEST_NOT_RESULT":
        raise CarverBlocked("S27 v2 controlled run pack status is not locked")
    if manifest.get("selected_slice_rule") != (
        "PRESERVE_2023_FOR_TEST_USE_OLDEST_2022_ROW_AFTER_STRICT_PRIOR_VQM_AND_LEVEL_COMPATIBILITY_POPULATED"
    ):
        raise CarverBlocked("S27 v2 controlled run selected-slice rule is not locked")
    if manifest.get("selected_raw_symbol") != "ZNH2":
        raise CarverBlocked("S27 v2 controlled run is locked to ZNH2")
    excluded = tuple(manifest.get("explicitly_excluded_data", ()))
    for required in ("NO_2023_TEST_DATA", "NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"):
        if required not in excluded:
            raise CarverBlocked("S27 v2 controlled run must preserve protected windows")
    proof = manifest.get("level_bridge_proof")
    if not isinstance(proof, dict):
        raise CarverBlocked("S27 v2 controlled run level bridge proof is required")
    if proof.get("point_in_time_roll_cutoff_date") != "2021-12-31":
        raise CarverBlocked("S27 v2 controlled run must bind point-in-time roll cutoff")
    if proof.get("future_roll_deltas_after_cutoff_excluded") != "YES":
        raise CarverBlocked("S27 v2 controlled run must exclude future roll deltas")


def _verify_row_family_hashes(pack_path: Path, manifest: dict[str, Any]) -> None:
    declared = manifest.get("row_family_files")
    if not isinstance(declared, dict) or set(declared) != set(ROW_FAMILY_FILES):
        raise CarverBlocked("S27 v2 controlled run row-family declaration is not locked")
    for filename in ROW_FAMILY_FILES:
        observed = _sha256(pack_path / filename).upper()
        if str(declared[filename]["sha256"]).upper() != observed:
            raise CarverBlocked("S27 v2 controlled run row-family bytes must match manifest")


def _read_pack_rows(pack_path: Path) -> dict[str, list[dict[str, str]]]:
    return {filename: _read_csv_rows(pack_path / filename) for filename in ROW_FAMILY_FILES}


def _compute_run_rows(
    pack_path: Path,
    manifest: dict[str, Any],
    rows: dict[str, list[dict[str, str]]],
) -> dict[str, dict[str, Any]]:
    row_hashes = _row_hashes_by_file(rows)
    daily_rows = rows["daily_continuous_completed_bar.csv"]
    daily_current = rows["daily_current_contract_completed_bar.csv"][0]
    decision = rows["hourly_decision_completed_bar.csv"][0]
    fill_candidate = rows["hourly_fill_completed_bar.csv"][0]
    session = rows["session_calendar.csv"][0]
    cost = rows["cost_parameter.csv"][0]
    closes = tuple(_to_float(row["close_price"]) for row in daily_rows)
    ewma5 = _ewma(closes, 5)
    ewma16 = _ewma(closes, 16)
    ewma64 = _ewma(closes, 64)
    trend = ewma16 - ewma64
    hourly_price = _to_float(decision["close_price"])
    fill_candidate_close = _to_float(fill_candidate["close_price"])
    previous_close = _to_float(daily_current["close_price"])
    history = manifest["history_evidence"]
    sigma = _to_float(history["selected_sigma_percent_t"])
    raw_forecast = ewma5 - hourly_price
    sigma_price = previous_close * sigma / 16.0
    risk_before_veto = raw_forecast / sigma_price
    trend_decision, risk_after_veto = _trend_veto(risk_before_veto, trend)
    multiplier_m = _to_float(history["selected_vqm_multiplier_m"])
    capped_forecast = _clamp(risk_after_veto * multiplier_m * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)
    base_position = CAPITAL_ACCOUNT_VALUE * ANNUAL_TARGET_RISK / (hourly_price * CONTRACT_POINT_VALUE * sigma)
    desired_unrounded = base_position * capped_forecast / FORECAST_TO_POSITION_DIVISOR
    desired_position = _round_half_away_from_zero(desired_unrounded)
    current_position = int(manifest["working_order_lifecycle_context"]["initial_current_position_contracts"])
    position_change = desired_position - current_position
    order_side = "BUY" if position_change > 0 else "SELL" if position_change < 0 else "NONE"
    order_quantity = abs(position_change)
    adjacent_target = current_position + (1 if position_change > 0 else -1 if position_change < 0 else 0)
    formula_limit = _formula_implied_limit_price(adjacent_target, base_position, ewma5, sigma_price, multiplier_m, trend)
    limit_order_price = _round_limit_price_to_executable_tick(formula_limit, order_side, ZN_TICK_SIZE)
    fill_executed = _close_only_limit_fill(order_side, fill_candidate_close, limit_order_price)
    fill_quantity = order_quantity if fill_executed else 0
    filled_position = current_position + (fill_quantity if order_side == "BUY" else -fill_quantity)
    commission_amount = ACCEPTED_COMMISSION_PER_CONTRACT * abs(fill_quantity)
    spread_amount = 0.0
    total_cost = commission_amount + spread_amount
    daily_close = _to_float(daily_rows[-1]["close_price"])
    current_close = _to_float(daily_current["close_price"])
    level_pass = isclose(daily_close, current_close, rel_tol=0.0, abs_tol=1e-12) and isclose(
        daily_close,
        hourly_price,
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    source_input = {
        "ledger_label": "SOURCE_INPUT_MANIFEST",
        "row_status": "LOCAL_PRE2023_DECLARED_PACK_BOUND_NOT_RESULT",
        "input_pack_path": str(pack_path),
        "input_manifest_sha256": _EXPECTED_PRE2023_MANIFEST_SHA256,
        "selected_decision_timestamp_utc": manifest["selected_decision_timestamp_utc"],
        "selected_fill_timestamp_utc": manifest["selected_fill_timestamp_utc"],
        "selected_raw_symbol": manifest["selected_raw_symbol"],
        "row_family_hashes": {filename: _sha256(pack_path / filename) for filename in ROW_FAMILY_FILES},
    }
    level = {
        "ledger_label": "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER",
        "row_status": "PASS_LOCAL_POINT_IN_TIME_LEVEL_BRIDGE_NOT_PRICE_EQUALITY_NOT_RESULT",
        "daily_current_close": current_close,
        "daily_continuous_close": daily_close,
        "hourly_decision_close": hourly_price,
        "hourly_fill_close": fill_candidate_close,
        "level_compatibility_passed": level_pass,
        "point_in_time_roll_cutoff_date": manifest["level_bridge_proof"]["point_in_time_roll_cutoff_date"],
        "future_roll_deltas_after_cutoff_excluded": manifest["level_bridge_proof"][
            "future_roll_deltas_after_cutoff_excluded"
        ],
        "daily_continuous_row_hash": row_hashes["daily_continuous_completed_bar.csv"][-1],
        "daily_current_row_hash": row_hashes["daily_current_contract_completed_bar.csv"][0],
        "hourly_decision_row_hash": row_hashes["hourly_decision_completed_bar.csv"][0],
    }
    runtime = {
        "ledger_label": "RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM",
        "row_status": "LOCAL_RUNTIME_NUMERIC_ROW_EMITTED_NOT_RESULT",
        "observed_daily_rows": len(daily_rows),
        "ewma5_equilibrium_value": ewma5,
        "ewmac16_value": ewma16,
        "ewmac64_value": ewma64,
        "ewmac16_64_trend_value": trend,
        "annual_percentage_sigma_value": sigma,
        "relative_volatility_v_value": _to_float(history["selected_vqm_relative_volatility_v"]),
        "quantile_q_value": _to_float(history["selected_vqm_quantile_q"]),
        "ewma10_multiplier_m_value": multiplier_m,
    }
    forecast = {
        "ledger_label": "FORECAST_REPLAY_LEDGER",
        "row_status": "LOCAL_FORECAST_LEDGER_EMITTED_NOT_POSITION_RESULT_OR_EVIDENCE",
        "ewma5_equilibrium_value": ewma5,
        "hourly_current_price_value": hourly_price,
        "raw_mean_reversion_forecast_value": raw_forecast,
        "sigma_price_value": sigma_price,
        "risk_adjusted_forecast_before_veto_value": risk_before_veto,
        "ewmac16_64_trend_value": trend,
        "trend_veto_decision": trend_decision,
        "risk_adjusted_forecast_after_veto_value": risk_after_veto,
        "scalar_value": FORECAST_SCALAR_VALUE,
        "capped_forecast_value": capped_forecast,
    }
    position = {
        "ledger_label": "DESIRED_POSITION_LEDGER",
        "row_status": "LOCAL_DESIRED_POSITION_LEDGER_EMITTED_NOT_RESULT",
        "capital_account_value": CAPITAL_ACCOUNT_VALUE,
        "annual_target_risk": ANNUAL_TARGET_RISK,
        "contract_point_value": CONTRACT_POINT_VALUE,
        "forecast_to_position_divisor": FORECAST_TO_POSITION_DIVISOR,
        "base_position_contracts": base_position,
        "desired_unrounded_contracts": desired_unrounded,
        "rounding_policy": "ROUND_HALF_AWAY_FROM_ZERO",
        "current_position_contracts": current_position,
        "desired_position_contracts": desired_position,
        "position_change_contracts": position_change,
    }
    order = {
        "ledger_label": "LIMIT_ORDER_LEDGER",
        "row_status": "LOCAL_ADJACENT_LIMIT_ORDER_LEDGER_EMITTED_NOT_RESULT",
        "order_required": position_change != 0,
        "order_side": order_side,
        "order_quantity": order_quantity,
        "adjacent_target_position": adjacent_target,
        "formula_implied_limit_price": formula_limit,
        "limit_order_price": limit_order_price,
        "tick_size": ZN_TICK_SIZE,
        "tick_rounding_policy": "BUY_DOWN_SELL_UP_TO_EXECUTABLE_TICK",
    }
    market_order = {
        "ledger_label": "MARKET_ORDER_LEDGER",
        "row_status": "NOT_APPLICABLE_NO_MARKET_ORDER_EMITTED",
        "market_order_rows_emitted": False,
    }
    transition = {
        "ledger_label": "WORKING_ORDER_TRANSITION_LEDGER",
        "row_status": "LOCAL_ONE_HOUR_SAME_SESSION_TRANSITION_BOUND_NOT_RESULT",
        "session_id": decision["session_id"],
        "same_session": decision["session_id"] == fill_candidate["session_id"] == session["session_id"],
        "roll_boundary": "NO_ROLL_BOUNDARY_ON_SELECTED_DATE",
        "working_state_before": "FLAT_EMPTY_WORKING_ORDER_SET",
        "working_state_after_order": "LIMIT_ORDER_WORKING_PENDING_FILL_DECISION",
    }
    fill = {
        "ledger_label": "FILL_LEDGER",
        "row_status": "LOCAL_LIMIT_FILL_LEDGER_EMITTED_NOT_RESULT",
        "fill_rule": "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL",
        "order_side": order_side,
        "order_quantity": order_quantity,
        "fill_candidate_close": fill_candidate_close,
        "fill_executed": fill_executed,
        "fill_price": limit_order_price if fill_executed else 0.0,
        "fill_price_provenance": "LIMIT_ORDER_PRICE_FROM_FILLED_ORDER" if fill_executed else "NOT_APPLICABLE",
        "fill_quantity": fill_quantity,
        "position_after_fill": filled_position,
        "hourly_fill_row_hash": row_hashes["hourly_fill_completed_bar.csv"][0],
    }
    commission = {
        "ledger_label": "COMMISSION_LEDGER",
        "row_status": "LOCAL_INFERRED_RETAIL_COMMISSION_LEDGER_EMITTED_NOT_RESULT",
        "cost_policy_id": cost["cost_policy_id"],
        "commission_per_contract_per_side": ACCEPTED_COMMISSION_PER_CONTRACT,
        "commission_amount": commission_amount,
        "currency": cost["currency"],
        "cost_assumption_label": cost["cost_policy_status"],
    }
    spread = {
        "ledger_label": "SPREAD_COST_LEDGER",
        "row_status": "LOCAL_LIMIT_FILL_SPREAD_COST_ZERO_NOT_RESULT",
        "spread_cost_amount": spread_amount,
        "spread_cost_policy": cost["spread_cost_policy"],
        "currency": cost["currency"],
    }
    pnl = {
        "ledger_label": "PNL_LEDGER",
        "pnl_status": PNL_BLOCKED_STATUS,
        "filled_position_requires_future_mark": fill_executed,
        "valuation_mark_row_declared": False,
        "actual_pnl_rows_emitted": False,
        "commission_cost_amount": commission_amount,
        "spread_cost_amount": spread_amount,
        "total_cost_amount": total_cost,
        "currency": cost["currency"],
    }
    validation = {
        "ledger_label": "VALIDATION_LEDGER",
        "row_status": "PASS_CONTROLLED_DEV_RECON_MECHANICAL_RUN_ARTIFACTS_NOT_RESULT",
        "result_status": RESULT_STATUS,
        "source_faithful_evidence_claimed": False,
        "non_authorizations": RUN_NON_AUTHORIZATIONS,
    }
    for row in (
        source_input,
        level,
        runtime,
        forecast,
        position,
        order,
        market_order,
        transition,
        fill,
        commission,
        spread,
        pnl,
        validation,
    ):
        row["row_hash"] = canonical_sha256(row)
    provenance = {
        "ledger_label": "PROVENANCE_AND_HASH_LEDGER",
        "row_status": "LOCAL_PROVENANCE_HASH_LEDGER_EMITTED_NOT_RESULT",
        "input_manifest_sha256": _EXPECTED_PRE2023_MANIFEST_SHA256,
        "source_input_row_hash": source_input["row_hash"],
        "forecast_row_hash": forecast["row_hash"],
        "desired_position_row_hash": position["row_hash"],
        "fill_row_hash": fill["row_hash"],
        "commission_row_hash": commission["row_hash"],
        "pnl_row_hash": pnl["row_hash"],
    }
    provenance["row_hash"] = canonical_sha256(provenance)
    return {
        "source_input": source_input,
        "level": level,
        "runtime": runtime,
        "forecast": forecast,
        "position": position,
        "order": order,
        "market_order": market_order,
        "transition": transition,
        "fill": fill,
        "commission": commission,
        "spread": spread,
        "pnl": pnl,
        "validation": validation,
        "provenance": provenance,
    }


def _write_run_artifacts(
    output_root: Path,
    pack_path: Path,
    manifest: dict[str, Any],
    rows: dict[str, list[dict[str, str]]],
    computed: dict[str, dict[str, Any]],
) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "source_input_manifest.csv": [computed["source_input"]],
        "level_compatibility_ledger.csv": [computed["level"]],
        "runtime_history_ledger.csv": [computed["runtime"]],
        "forecast_replay_ledger.csv": [computed["forecast"]],
        "desired_position_ledger.csv": [computed["position"]],
        "limit_order_ledger.csv": [computed["order"]],
        "market_order_ledger.csv": [computed["market_order"]],
        "working_order_transition_ledger.csv": [computed["transition"]],
        "fill_ledger.csv": [computed["fill"]],
        "commission_ledger.csv": [computed["commission"]],
        "spread_cost_ledger.csv": [computed["spread"]],
        "pnl_ledger.csv": [computed["pnl"]],
        "validation_ledger.csv": [computed["validation"]],
        "provenance_and_hash_ledger.csv": [computed["provenance"]],
    }
    for name, artifact_rows in artifacts.items():
        _write_csv(output_root / name, artifact_rows)

    run_manifest = {
        "artifact": "S27_V2_CONTROLLED_LOCAL_ONLY_PRE2023_DEVELOPMENT_RECON_RUN_MANIFEST",
        "status": S27_V2_CONTROLLED_DEV_RECON_STATUS,
        "authorization": S27_V2_CONTROLLED_DEV_RECON_AUTHORIZATION,
        "strategy_id": S27_V2_STRATEGY_ID,
        "instrument": S27_V2_INSTRUMENT,
        "lane": S27_V2_LANE,
        "input_pack_path": str(pack_path),
        "input_manifest_sha256": _EXPECTED_PRE2023_MANIFEST_SHA256,
        "selected_decision_timestamp_utc": manifest["selected_decision_timestamp_utc"],
        "selected_fill_timestamp_utc": manifest["selected_fill_timestamp_utc"],
        "selected_raw_symbol": manifest["selected_raw_symbol"],
        "row_family_files": {
            filename: {"row_count": len(rows[filename]), "sha256": _sha256(pack_path / filename)}
            for filename in ROW_FAMILY_FILES
        },
        "artifact_files": tuple(artifacts),
        "non_authorizations": RUN_NON_AUTHORIZATIONS,
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
    }
    _write_json(output_root / "run_manifest.json", run_manifest)
    evidence_manifest = {
        "artifact": "S27_V2_CONTROLLED_LOCAL_ONLY_PRE2023_EVIDENCE_MANIFEST",
        "status": "LOCAL_EVIDENCE_MANIFEST_METADATA_NOT_SOURCE_FAITHFUL_CLAIM",
        "run_manifest_hash": _sha256(output_root / "run_manifest.json"),
        "ledger_hashes": {name: _sha256(output_root / name) for name in artifacts},
    }
    _write_json(output_root / "evidence_manifest.json", evidence_manifest)
    trusted_bundle = {
        "artifact": "S27_V2_CONTROLLED_LOCAL_ONLY_PRE2023_TRUSTED_BUNDLE_METADATA",
        "status": "LOCAL_TRUSTED_BUNDLE_METADATA_NOT_RESULT_NOT_PROMOTION",
        "run_manifest_hash": _sha256(output_root / "run_manifest.json"),
        "evidence_manifest_hash": _sha256(output_root / "evidence_manifest.json"),
        "provenance_row_hash": computed["provenance"]["row_hash"],
        "validation_row_hash": computed["validation"]["row_hash"],
        "result_status": RESULT_STATUS,
        "source_faithful_evidence_claimed": False,
    }
    _write_json(output_root / "trusted_bundle.json", trusted_bundle)


def _write_sha256s(output_root: Path) -> None:
    rows = [
        {"relative_path": path.relative_to(output_root).as_posix(), "sha256": _sha256(path)}
        for path in sorted(output_root.iterdir())
        if path.is_file() and path.name != "SHA256SUMS.csv"
    ]
    _write_csv(output_root / "SHA256SUMS.csv", rows)


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise CarverBlocked(f"S27 v2 controlled run file has no rows: {path.name}")
    return rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise CarverBlocked("S27 v2 controlled run refuses to write empty CSV artifacts")
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(value) for key, value in row.items()})


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _row_hashes_by_file(rows: dict[str, list[dict[str, str]]]) -> dict[str, list[str]]:
    return {
        filename: [
            canonical_sha256({"artifact": "S27_V2_CONTROLLED_DEV_RECON_SOURCE_ROW", "filename": filename, "row": row})
            for row in file_rows
        ]
        for filename, file_rows in rows.items()
    }


def _to_float(value: object) -> float:
    return float(str(value))


def _ewma(values: tuple[float, ...], span: int) -> float:
    if len(values) < span:
        raise CarverBlocked("S27 v2 controlled run EWMA history is insufficient")
    alpha = 2.0 / (span + 1.0)
    current = values[0]
    for value in values[1:]:
        current = alpha * value + (1.0 - alpha) * current
    return current


def _trend_veto(risk_adjusted_forecast: float, trend_forecast: float) -> tuple[str, float]:
    if isclose(risk_adjusted_forecast, 0.0, rel_tol=0.0, abs_tol=1e-12):
        return "ZERO_FORECAST_ALREADY_ZERO", 0.0
    if risk_adjusted_forecast * trend_forecast < 0.0:
        return "ZERO_FORECAST_BY_TREND_VETO", 0.0
    return "PERMIT_MEAN_REVERSION", risk_adjusted_forecast


def _formula_implied_limit_price(
    adjacent_target_position: int,
    base_position: float,
    ewma5: float,
    sigma_price: float,
    multiplier_m: float,
    trend: float,
) -> float:
    if adjacent_target_position == 0:
        raise CarverBlocked("S27 v2 controlled run adjacent target cannot be flat")
    if adjacent_target_position > 0 and trend <= 0.0:
        raise CarverBlocked("S27 v2 controlled run buy target must be trend-permitted by positive EWMAC")
    if adjacent_target_position < 0 and trend >= 0.0:
        raise CarverBlocked("S27 v2 controlled run sell target must be trend-permitted by negative EWMAC")
    target_capped_forecast = adjacent_target_position / base_position * FORECAST_TO_POSITION_DIVISOR
    if abs(target_capped_forecast) >= FORECAST_CAP_VALUE:
        raise CarverBlocked("S27 v2 controlled run adjacent target is not priceable")
    target_risk_adjusted = target_capped_forecast / FORECAST_SCALAR_VALUE
    pre_vol_risk_adjusted = target_risk_adjusted / multiplier_m
    return ewma5 - pre_vol_risk_adjusted * sigma_price


def _round_limit_price_to_executable_tick(price: float, side: str, tick_size: float) -> float:
    if side == "SELL":
        return ceil((price - 1e-12) / tick_size) * tick_size
    if side == "BUY":
        return floor((price + 1e-12) / tick_size) * tick_size
    raise CarverBlocked("S27 v2 controlled run cannot round a non-order side")


def _close_only_limit_fill(side: str, close_price: float, limit_price: float) -> bool:
    if side == "BUY":
        return close_price <= limit_price
    if side == "SELL":
        return close_price >= limit_price
    return False


def _round_half_away_from_zero(value: float) -> int:
    magnitude = floor(abs(value) + 0.5)
    return magnitude if value >= 0.0 else -magnitude


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _as_plain_dict(bundle: ControlledDevelopmentReconRunBundle) -> dict[str, Any]:
    return dict(bundle.__dict__)


def _run_bundle_payload(bundle: ControlledDevelopmentReconRunBundle) -> dict[str, Any]:
    return {key: value for key, value in bundle.__dict__.items() if key != "bundle_hash"}

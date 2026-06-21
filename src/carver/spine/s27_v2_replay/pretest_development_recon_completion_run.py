from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
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
from .pretest_machine_freeze import validate_pretest_machine_freeze_rows
from .validation import require_hash


AUTHORIZATION = "S27_V2_PRE_TEST_DEVELOPMENT_RECONCILIATION_COMPLETION_GATE"
STATUS = "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_RUN_EMITTED_NOT_RESULT"
RESULT_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
BACKTEST_STATUS = "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"
PNL_EVALUATION_STATUS = "NOT_EMITTED_MECHANICAL_LEDGER_ROWS_ONLY"
VALUATION_CONVENTION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"

_REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_PACK_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pretest_dev_recon_2022_filled_sell_completion_declared_pack"
)
DEFAULT_OUTPUT_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_runs/ZN/"
    "20260611_pretest_dev_recon_2022_filled_sell_completion_run"
)
DEFAULT_MANIFEST_NAME = "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_MANIFEST.json"
DEFAULT_SHA256SUMS_NAME = "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_SHA256SUMS.txt"

ROW_FAMILY_FILES = (
    "runtime_evidence_ledger.csv",
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
class PretestDevelopmentReconRunConfig:
    input_pack_path: str
    output_root: str
    manifest_name: str = DEFAULT_MANIFEST_NAME


@dataclass(frozen=True)
class PretestDevelopmentReconCompletionRunBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    output_root: str
    row_count: int
    first_filled_sell_row_index: int
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
            raise CarverBlocked("S27 v2 pre-TEST completion run status/authorization is not locked")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT or self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 pre-TEST completion run must remain S27_V2 ZN source-native futures")
        if self.row_count <= 0 or self.first_filled_sell_row_index <= 0:
            raise CarverBlocked("S27 v2 pre-TEST completion run must include a filled sell row")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 pre-TEST completion run must preserve non-authorizations")
        output_root = Path(self.output_root).resolve()
        manifest = _safe_read_json(output_root / "run_manifest.json", "S27 v2 pre-TEST completion run manifest")
        evidence = _safe_read_json(output_root / "evidence_manifest.json", "S27 v2 pre-TEST completion evidence manifest")
        trusted = _safe_read_json(output_root / "trusted_bundle.json", "S27 v2 pre-TEST completion trusted bundle")
        pnl_rows = _safe_read_csv_rows(output_root / "pnl_ledger.csv", "S27 v2 pre-TEST completion pnl ledger")
        for label, value in (
            ("run manifest", self.run_manifest_hash),
            ("evidence manifest", self.evidence_manifest_hash),
            ("trusted bundle", self.trusted_bundle_hash),
            ("bundle", self.bundle_hash),
        ):
            require_hash(f"S27 v2 pre-TEST completion {label} hash", value)
        if self.run_manifest_hash != _sha256(output_root / "run_manifest.json"):
            raise CarverBlocked("S27 v2 pre-TEST completion run manifest hash must bind bytes")
        if self.evidence_manifest_hash != _sha256(output_root / "evidence_manifest.json"):
            raise CarverBlocked("S27 v2 pre-TEST completion evidence manifest hash must bind bytes")
        if self.trusted_bundle_hash != _sha256(output_root / "trusted_bundle.json"):
            raise CarverBlocked("S27 v2 pre-TEST completion trusted bundle hash must bind bytes")
        if str(manifest.get("input_pack_path")) != self.input_pack_path:
            raise CarverBlocked("S27 v2 pre-TEST completion input pack path must bind run manifest")
        if int(manifest.get("row_count", 0)) != self.row_count:
            raise CarverBlocked("S27 v2 pre-TEST completion row count must bind run manifest")
        if int(manifest.get("first_filled_sell_row_index", 0)) != self.first_filled_sell_row_index:
            raise CarverBlocked("S27 v2 pre-TEST completion filled sell index must bind run manifest")
        if len(pnl_rows) != self.row_count:
            raise CarverBlocked("S27 v2 pre-TEST completion row count must bind pnl ledger length")
        final_pnl = pnl_rows[-1]
        if int(final_pnl["ending_position_contracts"]) != self.final_position_contracts:
            raise CarverBlocked("S27 v2 pre-TEST completion final position must bind final pnl row")
        if float(final_pnl["cumulative_gross_pnl_amount"]) != self.cumulative_gross_pnl_amount:
            raise CarverBlocked("S27 v2 pre-TEST completion gross pnl must bind final pnl row")
        if float(final_pnl["cumulative_commission_amount"]) != self.cumulative_commission_amount:
            raise CarverBlocked("S27 v2 pre-TEST completion commission must bind final pnl row")
        if float(final_pnl["cumulative_spread_amount"]) != self.cumulative_spread_amount:
            raise CarverBlocked("S27 v2 pre-TEST completion spread must bind final pnl row")
        if float(final_pnl["cumulative_net_pnl_amount"]) != self.cumulative_net_pnl_amount:
            raise CarverBlocked("S27 v2 pre-TEST completion net pnl must bind final pnl row")
        if str(evidence.get("run_manifest_hash")) != self.run_manifest_hash:
            raise CarverBlocked("S27 v2 pre-TEST completion evidence manifest must bind run manifest hash")
        if str(trusted.get("run_manifest_hash")) != self.run_manifest_hash:
            raise CarverBlocked("S27 v2 pre-TEST completion trusted bundle must bind run manifest hash")
        if str(trusted.get("evidence_manifest_hash")) != self.evidence_manifest_hash:
            raise CarverBlocked("S27 v2 pre-TEST completion trusted bundle must bind evidence manifest hash")
        if int(trusted.get("first_filled_sell_row_index", 0)) != self.first_filled_sell_row_index:
            raise CarverBlocked("S27 v2 pre-TEST completion trusted bundle must bind filled sell index")
        if self.bundle_hash != canonical_sha256(_bundle_payload(self)):
            raise CarverBlocked("S27 v2 pre-TEST completion bundle hash must be content-bound")


def run_pretest_development_recon_completion(
    config: PretestDevelopmentReconRunConfig | None = None,
) -> PretestDevelopmentReconCompletionRunBundle:
    if config is None:
        config = PretestDevelopmentReconRunConfig(
            input_pack_path=str((_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()),
            output_root=str((_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve()),
        )
    pack_path = Path(config.input_pack_path).resolve()
    output_root = Path(config.output_root).resolve()
    _validate_pretest_paths(pack_path, output_root)
    _validate_pack_checksums(pack_path, config.manifest_name, DEFAULT_SHA256SUMS_NAME)
    manifest = _read_json(pack_path / config.manifest_name)
    rows = {filename: _read_csv_rows(pack_path / filename) for filename in ROW_FAMILY_FILES}
    _validate_manifest(pack_path, manifest, rows)
    _validate_runtime_evidence_against_source(manifest, rows["runtime_evidence_ledger.csv"])
    _validate_selected_hourly_rows_against_source(
        manifest,
        rows["runtime_evidence_ledger.csv"],
        rows["hourly_decision_completed_bar.csv"],
        rows["hourly_fill_completed_bar.csv"],
        rows["valuation_mark_completed_bar.csv"],
    )
    computed = _compute_rows(manifest, rows)
    validate_pretest_machine_freeze_rows(rows, computed)
    _validate_manifest_summaries(manifest, rows, computed)
    _write_artifacts(output_root, pack_path, manifest, computed)
    bundle = PretestDevelopmentReconCompletionRunBundle(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        output_root=str(output_root),
        row_count=len(computed["pnl"]),
        first_filled_sell_row_index=_first_filled_sell_index(computed["order"], computed["fill"]),
        final_position_contracts=int(computed["pnl"][-1]["ending_position_contracts"]),
        cumulative_gross_pnl_amount=float(computed["pnl"][-1]["cumulative_gross_pnl_amount"]),
        cumulative_commission_amount=float(computed["pnl"][-1]["cumulative_commission_amount"]),
        cumulative_spread_amount=float(computed["pnl"][-1]["cumulative_spread_amount"]),
        cumulative_net_pnl_amount=float(computed["pnl"][-1]["cumulative_net_pnl_amount"]),
        run_manifest_hash=_sha256(output_root / "run_manifest.json"),
        evidence_manifest_hash=_sha256(output_root / "evidence_manifest.json"),
        trusted_bundle_hash=_sha256(output_root / "trusted_bundle.json"),
        bundle_hash="0" * 64,
    )
    bundle = PretestDevelopmentReconCompletionRunBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_bundle_payload(bundle))}
    )
    bundle.validate()
    _write_json(output_root / "run_bundle.json", dict(bundle.__dict__))
    _write_sha256s(output_root)
    return bundle


def _validate_pretest_paths(pack_path: Path, output_root: Path) -> None:
    expected_pack_path = (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()
    expected_output_root = (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve()
    if pack_path != expected_pack_path:
        raise CarverBlocked("S27 v2 pre-TEST runner is locked to the audited completion declared local ZN input pack")
    if output_root != expected_output_root:
        raise CarverBlocked("S27 v2 pre-TEST runner output root is locked to the audited completion local ZN replay run")


def _validate_pack_checksums(pack_path: Path, manifest_name: str, checksum_name: str) -> None:
    checksum_path = pack_path / checksum_name
    try:
        lines = checksum_path.read_text(encoding="ascii").splitlines()
    except FileNotFoundError as exc:
        raise CarverBlocked("S27 v2 pre-TEST completion declared pack checksum file is missing") from exc
    checksums: dict[str, str] = {}
    for line in lines:
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            raise CarverBlocked("S27 v2 pre-TEST completion declared pack checksum file is malformed")
        checksums[parts[1]] = parts[0].upper()
    for filename in (*ROW_FAMILY_FILES, manifest_name):
        digest = checksums.get(filename)
        if digest is None:
            raise CarverBlocked("S27 v2 pre-TEST completion declared pack checksum coverage is incomplete")
        if digest != _sha256(pack_path / filename).upper():
            raise CarverBlocked("S27 v2 pre-TEST completion declared pack checksum file must bind file bytes")


def _validate_manifest(pack_path: Path, manifest: dict[str, Any], rows: dict[str, list[dict[str, str]]]) -> None:
    if manifest.get("authorization") != AUTHORIZATION:
        raise CarverBlocked("S27 v2 pre-TEST completion pack authorization is not active")
    if manifest.get("status") != "LOCAL_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_PACK_DECLARED_NOT_RESULT":
        raise CarverBlocked("S27 v2 pre-TEST completion pack status is not locked")
    if manifest.get("lane") != S27_V2_LANE:
        raise CarverBlocked("S27 v2 pre-TEST completion pack must remain source-native futures")
    for forbidden in ("NO_2023_TEST_DATA", "NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"):
        if forbidden not in tuple(manifest.get("explicitly_excluded_data", ())):
            raise CarverBlocked("S27 v2 pre-TEST completion pack protected-window exclusion is missing")
    if tuple(manifest.get("non_authorizations", ())) != NON_AUTHORIZATIONS:
        raise CarverBlocked("S27 v2 pre-TEST completion pack must preserve non-authorizations")
    declared = manifest.get("row_family_files")
    if not isinstance(declared, dict) or set(declared) != set(ROW_FAMILY_FILES):
        raise CarverBlocked("S27 v2 pre-TEST completion row-family declaration is not locked")
    for filename in ROW_FAMILY_FILES:
        if str(declared[filename]["sha256"]).upper() != _sha256(pack_path / filename).upper():
            raise CarverBlocked("S27 v2 pre-TEST completion row-family bytes must match manifest")
    row_count = len(rows["hourly_decision_completed_bar.csv"])
    if row_count == 0:
        raise CarverBlocked("S27 v2 pre-TEST completion refuses empty decision rows")
    for family in ("hourly_fill_completed_bar.csv", "valuation_mark_completed_bar.csv", "runtime_evidence_ledger.csv"):
        if len(rows[family]) != row_count:
            raise CarverBlocked("S27 v2 pre-TEST completion row families must align one-to-one")
    for family in ("hourly_decision_completed_bar.csv", "hourly_fill_completed_bar.csv", "valuation_mark_completed_bar.csv"):
        for row in rows[family]:
            if not str(row["completed_timestamp_utc"]).startswith("2022-"):
                raise CarverBlocked("S27 v2 pre-TEST completion selected rows must stay in 2022")


def _validate_runtime_evidence_against_source(manifest: dict[str, Any], runtime_rows: list[dict[str, str]]) -> None:
    continuous = _read_csv_rows(_REPO_ROOT / manifest["source_continuous_daily_ledger"])
    rolls = _read_csv_rows(_REPO_ROOT / manifest["source_roll_ledger"])
    hourly = {
        row["derived_completed_bar_end_utc"]: row
        for row in _read_csv_rows(_REPO_ROOT / manifest["source_hourly_ledger"])
        if row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
    }
    continuous_by_date = {row["completed_trading_date"]: row for row in continuous}
    cache: dict[str, list[dict[str, Any]]] = {}
    for runtime in runtime_rows:
        decision_ts = runtime["decision_timestamp_utc"]
        decision = hourly.get(decision_ts)
        if decision is None:
            raise CarverBlocked("S27 v2 pre-TEST completion runtime decision must exist in source hourly ledger")
        previous_daily_date = max(day for day in continuous_by_date if day < decision["completed_trading_date"])
        if runtime["previous_daily_trading_date"] != previous_daily_date:
            raise CarverBlocked("S27 v2 pre-TEST completion runtime row must bind strict-prior previous daily date")
        if previous_daily_date not in cache:
            cache[previous_daily_date] = _point_in_time_continuous_series(continuous, rolls, previous_daily_date)
        pit = cache[previous_daily_date]
        sigma_rows = _build_sigma_rows(pit)
        vqm_rows = _build_vqm_rows(sigma_rows)
        sigma_by_date = {row["completed_trading_date"]: row for row in sigma_rows}
        vqm_by_date = {row["completed_trading_date"]: row for row in vqm_rows}
        prior_vqm_dates = [day for day in vqm_by_date if day < decision["completed_trading_date"]]
        if previous_daily_date not in sigma_by_date or not prior_vqm_dates:
            raise CarverBlocked("S27 v2 pre-TEST completion runtime evidence lacks strict-prior sigma/VQM")
        expected = _runtime_row_from_source(
            pit=pit,
            sigma=sigma_by_date[previous_daily_date],
            vqm=vqm_by_date[max(prior_vqm_dates)],
            decision=decision,
            row_index=int(runtime["row_index"]),
        )
        _require_rows_equal(runtime, expected, "S27 v2 pre-TEST completion runtime evidence")


def _validate_selected_hourly_rows_against_source(
    manifest: dict[str, Any],
    runtime_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    mark_rows: list[dict[str, str]],
) -> None:
    source_hourly = [
        row
        for row in _read_csv_rows(_REPO_ROOT / manifest["source_hourly_ledger"])
        if row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
    ]
    source_by_hash = {
        _row_hash("strategy_facing_hourly_available_bars", row): row for row in source_hourly
    }
    source_by_symbol = _group_source_hourly_by_symbol(source_hourly)
    for runtime, decision, fill, mark in zip(runtime_rows, decision_rows, fill_rows, mark_rows, strict=True):
        decision_source = _source_hourly_row_by_hash(source_by_hash, decision["source_row_hash"], "decision")
        fill_source = _source_hourly_row_by_hash(source_by_hash, fill["source_row_hash"], "fill")
        mark_source = _source_hourly_row_by_hash(source_by_hash, mark["source_row_hash"], "valuation mark")
        expected_decision = _hourly_row_from_source(decision_source, runtime, "DECISION", int(decision["row_index"]))
        expected_fill = _hourly_row_from_source(fill_source, runtime, "FILL", int(fill["row_index"]))
        expected_mark = _valuation_row_from_source(mark_source, runtime, int(mark["row_index"]))
        _require_rows_equal(decision, expected_decision, "S27 v2 pre-TEST completion decision row")
        _require_rows_equal(fill, expected_fill, "S27 v2 pre-TEST completion fill row")
        _require_rows_equal(mark, expected_mark, "S27 v2 pre-TEST completion valuation mark row")
        if decision_source["raw_symbol"] != fill_source["raw_symbol"] or decision_source["raw_symbol"] != mark_source["raw_symbol"]:
            raise CarverBlocked("S27 v2 pre-TEST completion decision/fill/valuation rows must stay on one raw-symbol path")
        expected_fill_ts = _z(_parse_timestamp(decision_source["derived_completed_bar_end_utc"]) + _one_hour())
        if fill_source["derived_completed_bar_end_utc"] != expected_fill_ts:
            raise CarverBlocked("S27 v2 pre-TEST completion fill row must be the one-hour same-symbol fill candidate")
        expected_mark = _next_same_symbol_source_row_after(
            source_by_symbol[decision_source["raw_symbol"]],
            fill_source["derived_completed_bar_end_utc"],
        )
        if expected_mark is None or _row_hash("strategy_facing_hourly_available_bars", expected_mark) != mark["source_row_hash"]:
            raise CarverBlocked("S27 v2 pre-TEST completion valuation mark row must be the next completed same-symbol source row after fill")


def _runtime_row_from_source(
    pit: list[dict[str, Any]],
    sigma: dict[str, Any],
    vqm: dict[str, Any],
    decision: dict[str, str],
    row_index: int,
) -> dict[str, str]:
    previous_daily = pit[-1]
    window = pit[-64:]
    closes = tuple(float(row["continuous_close"]) for row in window)
    row: dict[str, Any] = {
        "row_index": row_index,
        "decision_timestamp_utc": decision["derived_completed_bar_end_utc"],
        "decision_trading_date": decision["completed_trading_date"],
        "previous_daily_trading_date": previous_daily["completed_trading_date"],
        "point_in_time_roll_cutoff_date": previous_daily["completed_trading_date"],
        "daily_window_start": window[0]["completed_trading_date"],
        "daily_window_end": window[-1]["completed_trading_date"],
        "daily_window_row_count": 64,
        "previous_daily_raw_symbol": previous_daily["raw_symbol"],
        "previous_daily_raw_close": _num(previous_daily["raw_close"]),
        "previous_daily_additive_back_adjustment": _num(previous_daily["additive_back_adjustment"]),
        "ewma5_equilibrium": _num(_ewma(closes, 5)),
        "ewmac16_64_trend": _num(_ewma(closes, 16) - _ewma(closes, 64)),
        "annual_percentage_sigma": _num(sigma["sigma_i_t"]),
        "relative_volatility_v": _num(vqm["relative_volatility_v"]),
        "quantile_q": _num(vqm["quantile_q"]),
        "vol_multiplier_m": _num(vqm["vol_multiplier_m_ewma10"]),
        "runtime_status": "PASS_ROLLING_STRICT_PRIOR_DAILY_EVIDENCE_PRETEST_DEV_RECON_NOT_RESULT",
        "no_lookahead_status": "PASS_PRETEST_SELECTED_ROW_STRICT_PRIOR_DAILY_EVIDENCE",
    }
    row["row_hash"] = _row_hash("S27_V2_PRETEST_RUNTIME_EVIDENCE_ROW", row)
    return {key: str(value) for key, value in row.items()}


def _compute_rows(manifest: dict[str, Any], rows: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, Any]]]:
    cost = rows["cost_parameter.csv"][0]
    current_position = 0
    last_mark_price: float | None = None
    cumulative_gross = 0.0
    cumulative_commission = 0.0
    cumulative_spread = 0.0
    out: dict[str, list[dict[str, Any]]] = {
        name: []
        for name in ("runtime", "forecast", "position", "order", "market", "transition", "fill", "cost", "pnl", "validation")
    }
    for index, (runtime, decision, fill, mark) in enumerate(
        zip(
            rows["runtime_evidence_ledger.csv"],
            rows["hourly_decision_completed_bar.csv"],
            rows["hourly_fill_completed_bar.csv"],
            rows["valuation_mark_completed_bar.csv"],
            strict=True,
        ),
        1,
    ):
        if int(runtime["row_index"]) != index:
            raise CarverBlocked("S27 v2 pre-TEST completion runtime row index must be sequential")
        decision_price = float(decision["close_price"])
        fill_close = float(fill["close_price"])
        mark_price = float(mark["close_price"])
        ewma5 = float(runtime["ewma5_equilibrium"])
        trend = float(runtime["ewmac16_64_trend"])
        sigma = float(runtime["annual_percentage_sigma"])
        m = float(runtime["vol_multiplier_m"])
        sigma_price = float(runtime["previous_daily_raw_close"]) * sigma / 16.0
        raw_forecast = ewma5 - decision_price
        risk_before_veto = raw_forecast / sigma_price
        risk_after_veto = 0.0 if risk_before_veto * trend < 0.0 else risk_before_veto
        capped_forecast = _clamp(risk_after_veto * m * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)
        base_position = CAPITAL_ACCOUNT_VALUE * ANNUAL_TARGET_RISK / (decision_price * CONTRACT_POINT_VALUE * sigma)
        desired_position = _round_half_away_from_zero(base_position * capped_forecast / FORECAST_TO_POSITION_DIVISOR)
        starting_position = current_position
        position_change = desired_position - starting_position
        side = "BUY" if position_change > 0 else "SELL" if position_change < 0 else "NONE"
        order_quantity = abs(position_change)
        adjacent_target = starting_position + (1 if position_change > 0 else -1 if position_change < 0 else 0)
        formula_limit = _formula_limit(adjacent_target, base_position, ewma5, sigma_price, m, trend) if side != "NONE" else 0.0
        if formula_limit is None:
            raise CarverBlocked("S27 v2 pre-TEST completion selected row must have supported adjacent limit formula")
        limit_price = _round_limit(formula_limit, side) if side != "NONE" else 0.0
        fill_executed = _limit_fill(side, fill_close, limit_price)
        fill_quantity = order_quantity if fill_executed else 0
        signed_fill = fill_quantity if side == "BUY" else -fill_quantity if side == "SELL" else 0
        current_position = starting_position + signed_fill
        existing_gross = 0.0 if last_mark_price is None else starting_position * (mark_price - last_mark_price) * CONTRACT_POINT_VALUE
        fill_gross = signed_fill * (mark_price - limit_price) * CONTRACT_POINT_VALUE if fill_executed else 0.0
        row_gross = existing_gross + fill_gross
        commission = ACCEPTED_COMMISSION_PER_CONTRACT * abs(fill_quantity)
        spread = 0.0
        row_net = row_gross - commission
        cumulative_gross += row_gross
        cumulative_commission += commission
        cumulative_spread += spread
        cumulative_net = cumulative_gross - cumulative_commission - cumulative_spread
        last_mark_price = mark_price
        working_after = (
            "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
            if side == "NONE" or fill_executed
            else "UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE"
        )
        market_fallback_status = (
            "NOT_REQUIRED_NO_ORDER_POSITION_UNCHANGED"
            if side == "NONE"
            else "NOT_REQUIRED_LIMIT_ORDER_FILLED"
            if fill_executed
            else "FAIL_CLOSED_UNFILLED_LIMIT_ORDER_MARKET_FALLBACK_NOT_AUTHORIZED"
        )
        out["runtime"].append(_hash_row({"row_index": index, "runtime_evidence_row_hash": runtime["row_hash"], "ewma5": ewma5, "trend": trend, "sigma": sigma, "vqm_multiplier_m": m, "row_status": "LOCAL_RUNTIME_NUMERIC_ROW_EMITTED_NOT_RESULT"}))
        out["forecast"].append(_hash_row({"row_index": index, "decision_timestamp_utc": decision["completed_timestamp_utc"], "raw_forecast": raw_forecast, "risk_adjusted_forecast": risk_after_veto, "capped_forecast": capped_forecast, "row_status": "LOCAL_FORECAST_ROW_EMITTED_NOT_RESULT"}))
        out["position"].append(_hash_row({"row_index": index, "starting_position_contracts": starting_position, "desired_position_contracts": desired_position, "position_change_contracts": position_change, "base_position_contracts": base_position, "row_status": "LOCAL_POSITION_ROW_EMITTED_NOT_RESULT"}))
        out["order"].append(_hash_row({"row_index": index, "order_side": side, "order_quantity": order_quantity, "adjacent_target_position": adjacent_target, "formula_limit_price": formula_limit, "limit_order_price": limit_price, "row_status": "LOCAL_LIMIT_ORDER_ROW_EMITTED_NOT_RESULT"}))
        out["market"].append(_hash_row({"row_index": index, "market_order_required": False, "market_order_rows_emitted": False, "market_fallback_status": market_fallback_status, "row_status": "LOCAL_NO_MARKET_ORDER_METADATA_ROW_EMITTED_NOT_RESULT"}))
        out["transition"].append(_hash_row({"row_index": index, "starting_position_contracts": starting_position, "ending_position_contracts": current_position, "working_state_before": "EMPTY" if index == 1 else "NO_OPEN_WORKING_ORDER_CARRIED", "working_state_after": working_after, "same_session": decision["session_id"] == fill["session_id"] == mark["session_id"], "row_status": "LOCAL_WORKING_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT"}))
        out["fill"].append(_hash_row({"row_index": index, "fill_executed": fill_executed, "fill_rule": "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL", "fill_candidate_close": fill_close, "fill_price": limit_price if fill_executed else 0.0, "fill_quantity": fill_quantity, "position_after_fill": current_position, "row_status": "LOCAL_FILL_ROW_EMITTED_NOT_RESULT"}))
        out["cost"].append(_hash_row({"row_index": index, "cost_policy_id": cost["cost_policy_id"], "commission_amount": commission, "spread_cost_amount": spread, "total_cost_amount": commission + spread, "currency": "USD", "row_status": "LOCAL_COST_ROW_EMITTED_NOT_RESULT"}))
        out["pnl"].append(_hash_row({"row_index": index, "valuation_mark_timestamp_utc": mark["completed_timestamp_utc"], "valuation_mark_close_price": mark_price, "valuation_convention_label": VALUATION_CONVENTION_LABEL, "existing_position_gross_pnl": existing_gross, "fill_gross_pnl": fill_gross, "row_gross_pnl_amount": row_gross, "row_net_pnl_amount": row_net, "cumulative_gross_pnl_amount": cumulative_gross, "cumulative_commission_amount": cumulative_commission, "cumulative_spread_amount": cumulative_spread, "cumulative_net_pnl_amount": cumulative_net, "ending_position_contracts": current_position, "result_status": RESULT_STATUS, "backtest_status": BACKTEST_STATUS, "pnl_evaluation_status": PNL_EVALUATION_STATUS, "source_faithful_evidence_claimed": False, "row_status": "LOCAL_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"}))
        out["validation"].append(_hash_row({"row_index": index, "result_status": RESULT_STATUS, "backtest_status": BACKTEST_STATUS, "source_faithful_evidence_claimed": False, "non_authorizations": NON_AUTHORIZATIONS, "row_status": "LOCAL_VALIDATION_ROW_EMITTED_NOT_RESULT"}))
    if _first_filled_sell_index(out["order"], out["fill"]) <= 0:
        raise CarverBlocked("S27 v2 pre-TEST completion run must contain an organic filled sell")
    return out


def _validate_manifest_summaries(
    manifest: dict[str, Any],
    rows: dict[str, list[dict[str, str]]],
    computed: dict[str, list[dict[str, Any]]],
) -> None:
    expected_plan = []
    for runtime, decision, fill, mark, order, fill_row in zip(
        rows["runtime_evidence_ledger.csv"],
        rows["hourly_decision_completed_bar.csv"],
        rows["hourly_fill_completed_bar.csv"],
        rows["valuation_mark_completed_bar.csv"],
        computed["order"],
        computed["fill"],
        strict=True,
    ):
        expected_plan.append(
            {
                "row_index": int(decision["row_index"]),
                "decision_timestamp_utc": decision["completed_timestamp_utc"],
                "fill_timestamp_utc": fill["completed_timestamp_utc"],
                "valuation_mark_timestamp_utc": mark["completed_timestamp_utc"],
                "raw_symbol": decision["raw_symbol"],
                "previous_daily_trading_date": runtime["previous_daily_trading_date"],
                "runtime_evidence_row_hash": runtime["row_hash"],
                "selected_for_formula_status": "PASS_FORMULA_SUPPORTED",
                "order_side": order["order_side"],
                "fill_executed": "YES" if _is_true(fill_row["fill_executed"]) else "NO",
            }
        )
    if manifest.get("decision_fill_mark_plan") != expected_plan:
        raise CarverBlocked("S27 v2 pre-TEST completion manifest decision/fill/valuation summary must match active selected rows")
    first_filled_sell_index = _first_filled_sell_index(computed["order"], computed["fill"])
    order_row = computed["order"][first_filled_sell_index - 1]
    position_row = computed["position"][first_filled_sell_index - 1]
    fill_row = computed["fill"][first_filled_sell_index - 1]
    expected_completion = {
        "row_index": first_filled_sell_index,
        "decision_timestamp_utc": rows["hourly_decision_completed_bar.csv"][first_filled_sell_index - 1]["completed_timestamp_utc"],
        "fill_timestamp_utc": rows["hourly_fill_completed_bar.csv"][first_filled_sell_index - 1]["completed_timestamp_utc"],
        "raw_symbol": rows["hourly_decision_completed_bar.csv"][first_filled_sell_index - 1]["raw_symbol"],
        "starting_position_contracts": int(position_row["starting_position_contracts"]),
        "desired_position_contracts": int(position_row["desired_position_contracts"]),
        "position_change_contracts": int(position_row["position_change_contracts"]),
        "order_side": order_row["order_side"],
        "order_quantity": int(order_row["order_quantity"]),
        "limit_order_price": _num(order_row["limit_order_price"]),
        "fill_candidate_close": _num(fill_row["fill_candidate_close"]),
        "fill_executed": "YES",
    }
    if manifest.get("filled_sell_completion") != expected_completion:
        raise CarverBlocked("S27 v2 pre-TEST completion manifest filled-sell summary must match active selected rows")


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
        "artifact": "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_RUN_MANIFEST",
        "status": STATUS,
        "authorization": AUTHORIZATION,
        "input_pack_path": str(pack_path),
        "input_manifest_hash": _sha256(pack_path / DEFAULT_MANIFEST_NAME),
        "row_count": len(computed["pnl"]),
        "first_filled_sell_row_index": _first_filled_sell_index(computed["order"], computed["fill"]),
        "artifact_files": tuple(files),
        "source_continuous_daily_ledger": manifest["source_continuous_daily_ledger"],
        "source_hourly_ledger": manifest["source_hourly_ledger"],
        "non_authorizations": NON_AUTHORIZATIONS,
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
    }
    _write_json(output_root / "run_manifest.json", run_manifest)
    evidence_manifest = {
        "artifact": "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_EVIDENCE_MANIFEST",
        "status": "LOCAL_PRETEST_DEV_RECON_EVIDENCE_MANIFEST_METADATA_NOT_RESULT",
        "run_manifest_hash": _sha256(output_root / "run_manifest.json"),
        "ledger_hashes": {name: _sha256(output_root / name) for name in files},
        "input_manifest_hash": _sha256(pack_path / DEFAULT_MANIFEST_NAME),
    }
    _write_json(output_root / "evidence_manifest.json", evidence_manifest)
    trusted_bundle = {
        "artifact": "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_TRUSTED_BUNDLE_METADATA",
        "status": "LOCAL_PRETEST_DEV_RECON_TRUSTED_BUNDLE_METADATA_NOT_RESULT_NOT_PROMOTION",
        "run_manifest_hash": _sha256(output_root / "run_manifest.json"),
        "evidence_manifest_hash": _sha256(output_root / "evidence_manifest.json"),
        "final_pnl_row_hash": computed["pnl"][-1]["row_hash"],
        "first_filled_sell_row_index": _first_filled_sell_index(computed["order"], computed["fill"]),
        "result_status": RESULT_STATUS,
        "source_faithful_evidence_claimed": False,
    }
    _write_json(output_root / "trusted_bundle.json", trusted_bundle)


def _first_filled_sell_index(order_rows: list[dict[str, Any]], fill_rows: list[dict[str, Any]]) -> int:
    for order, fill in zip(order_rows, fill_rows, strict=True):
        if order["order_side"] == "SELL" and str(fill["fill_executed"]).upper() in ("TRUE", "True", "1") and int(fill["fill_quantity"]) > 0:
            return int(order["row_index"])
    return 0


def _point_in_time_continuous_series(
    continuous: list[dict[str, str]],
    rolls: list[dict[str, str]],
    cutoff_date: str,
) -> list[dict[str, Any]]:
    active_rows = [row for row in continuous if row["completed_trading_date"] <= cutoff_date]
    known_rolls = [row for row in rolls if row["roll_transition_date"] <= cutoff_date]
    current_contract_key = active_rows[-1]["active_contract_key"]
    offsets_by_contract = {current_contract_key: 0.0}
    for roll in reversed(known_rolls):
        if roll["new_contract_key"] in offsets_by_contract:
            offsets_by_contract[roll["old_contract_key"]] = (
                offsets_by_contract[roll["new_contract_key"]] + float(roll["additive_delta_to_prior_history"])
            )
    rows = []
    for row in active_rows:
        if row["active_contract_key"] not in offsets_by_contract:
            raise CarverBlocked("S27 v2 pre-TEST completion point-in-time offset missing")
        adjustment = offsets_by_contract[row["active_contract_key"]]
        rows.append({**row, "additive_back_adjustment": adjustment, "continuous_close": float(row["raw_close"]) + adjustment})
    return rows


def _build_sigma_rows(continuous: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    closes = [float(row["continuous_close"]) for row in continuous]
    dates = [row["completed_trading_date"] for row in continuous]
    alpha = 2.0 / (32 + 1.0)
    for index in range(34 - 1, len(continuous)):
        window = closes[index - 34 + 1 : index + 1]
        returns = [window[i] / window[i - 1] - 1.0 for i in range(1, len(window))]
        variance = returns[0] * returns[0]
        for value in returns[1:]:
            variance = alpha * value * value + (1.0 - alpha) * variance
        rows.append({"completed_trading_date": dates[index], "sigma_i_t": math.sqrt(variance) * math.sqrt(256.0)})
    return rows


def _build_vqm_rows(sigma_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    alpha = 2.0 / (10 + 1.0)
    smoothed = None
    sigma_values = [float(row["sigma_i_t"]) for row in sigma_rows]
    prefix = [0.0]
    for sigma in sigma_values:
        prefix.append(prefix[-1] + sigma)
    historical_v = []
    for index, sigma_row in enumerate(sigma_rows):
        if index < 2560:
            continue
        ten_year_avg = (prefix[index] - prefix[index - 2560]) / 2560
        sigma = sigma_values[index]
        v = sigma / ten_year_avg
        historical_v.append(v)
        q = sum(1 for value in historical_v if value <= v) / len(historical_v)
        raw_m = 2.0 - 1.5 * q
        smoothed = raw_m if smoothed is None else alpha * raw_m + (1.0 - alpha) * smoothed
        rows.append({"completed_trading_date": sigma_row["completed_trading_date"], "relative_volatility_v": v, "quantile_q": q, "vol_multiplier_m_ewma10": smoothed})
    return rows


def _ewma(values: tuple[float, ...], span: int) -> float:
    alpha = 2.0 / (span + 1.0)
    current = values[0]
    for value in values[1:]:
        current = alpha * value + (1.0 - alpha) * current
    return current


def _formula_limit(target_position: int, base_position: float, ewma5: float, sigma_price: float, multiplier_m: float, trend: float) -> float | None:
    if target_position <= 0 or trend <= 0.0:
        return None
    target_capped = target_position / base_position * FORECAST_TO_POSITION_DIVISOR
    target_risk = target_capped / FORECAST_SCALAR_VALUE
    pre_vol_risk = target_risk / multiplier_m
    return ewma5 - pre_vol_risk * sigma_price


def _round_limit(price: float, side: str) -> float:
    if side == "BUY":
        return math.floor((price + 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    if side == "SELL":
        return math.ceil((price - 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    return 0.0


def _limit_fill(side: str, close_price: float, limit_price: float) -> bool:
    return (side == "BUY" and close_price <= limit_price) or (side == "SELL" and close_price >= limit_price)


def _round_half_away_from_zero(value: float) -> int:
    magnitude = math.floor(abs(value) + 0.5)
    return magnitude if value >= 0.0 else -magnitude


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _require_rows_equal(observed: dict[str, str], expected: dict[str, str], label: str) -> None:
    normalized_observed = {key: str(value) for key, value in observed.items()}
    if normalized_observed != expected:
        raise CarverBlocked(f"{label} must be recomputed from active source ledgers")


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _safe_read_csv_rows(path: Path, label: str) -> list[dict[str, str]]:
    try:
        return _read_csv_rows(path)
    except FileNotFoundError as exc:
        raise CarverBlocked(f"{label} file is missing") from exc


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="ascii"))
    if not isinstance(payload, dict):
        raise CarverBlocked("S27 v2 pre-TEST completion JSON payload must be an object")
    return payload


def _safe_read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        return _read_json(path)
    except FileNotFoundError as exc:
        raise CarverBlocked(f"{label} file is missing") from exc


def _hourly_row_from_source(source_row: dict[str, str], runtime: dict[str, str], role: str, row_index: int) -> dict[str, str]:
    packed = _hourly_packed_row_from_source(source_row, runtime, role, row_index)
    return {key: str(value) for key, value in packed.items()}


def _hourly_packed_row_from_source(
    source_row: dict[str, str],
    runtime: dict[str, str],
    role: str,
    row_index: int,
) -> dict[str, Any]:
    adjustment = float(runtime["previous_daily_additive_back_adjustment"])
    packed: dict[str, Any] = {
        "row_index": row_index,
        "completed_timestamp_utc": source_row["derived_completed_bar_end_utc"],
        "trading_date": source_row["completed_trading_date"],
        "raw_symbol": source_row["raw_symbol"],
        "session_id": _session_id(source_row["derived_completed_bar_end_utc"]),
        "row_locator": f"20260611_S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_{role}_{row_index:04d}_{source_row['derived_completed_bar_end_utc'].replace('-', '').replace(':', '')}_{source_row['raw_symbol']}",
        "close_price": _num(float(source_row["close"]) + adjustment),
        "source_provider_csv": source_row["source_provider_csv"],
        "source_provider_csv_sha256": source_row["source_provider_csv_sha256"],
        "source_row_hash": _row_hash("strategy_facing_hourly_available_bars", source_row),
        "readiness_status": "READY_COMPLETED_BAR_DATABENTO_PRETEST_DEV_RECON",
    }
    packed["row_hash"] = _row_hash(f"S27_V2_PRETEST_{role}_ROW", packed)
    return packed


def _valuation_row_from_source(source_row: dict[str, str], runtime: dict[str, str], row_index: int) -> dict[str, str]:
    packed = _hourly_packed_row_from_source(source_row, runtime, "VALUATION_MARK", row_index)
    packed["valuation_convention_label"] = VALUATION_CONVENTION_LABEL
    packed["readiness_status"] = "READY_COMPLETED_BAR_DATABENTO_PRETEST_VALUATION_MARK_DEV_RECON"
    packed["row_hash"] = _row_hash("S27_V2_PRETEST_VALUATION_MARK_ROW", packed)
    return {key: str(value) for key, value in packed.items()}


def _source_hourly_row_by_hash(
    source_by_hash: dict[str, dict[str, str]],
    source_row_hash: str,
    label: str,
) -> dict[str, str]:
    row = source_by_hash.get(source_row_hash)
    if row is None:
        raise CarverBlocked(f"S27 v2 pre-TEST completion {label} row hash must resolve to active source hourly row")
    return row


def _group_source_hourly_by_symbol(source_rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in sorted(source_rows, key=lambda item: item["derived_completed_bar_end_utc"]):
        grouped.setdefault(row["raw_symbol"], []).append(row)
    return grouped


def _next_same_symbol_source_row_after(
    hourly_rows: list[dict[str, str]],
    completed_ts: str,
) -> dict[str, str] | None:
    for row in hourly_rows:
        if row["derived_completed_bar_end_utc"] > completed_ts:
            return row
    return None


def _parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _one_hour() -> timedelta:
    return timedelta(hours=1)


def _session_id(timestamp: str) -> str:
    start, end = _session_bounds(timestamp)
    return f"UTC_ZN_PRE2023_{start}_{end}"


def _session_bounds(timestamp: str) -> tuple[str, str]:
    completed = _parse_timestamp(timestamp)
    if completed.hour >= 22:
        start = completed.replace(hour=22, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=23)
    else:
        end = completed.replace(hour=21, minute=0, second=0, microsecond=0)
        start = end - timedelta(hours=23)
    return _z(start), _z(end)


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise CarverBlocked("S27 v2 pre-TEST completion refuses empty CSV artifacts")
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


def _row_hash(label: str, row: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps({"artifact": label, "row": row}, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest().upper()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _num(value: Any) -> str:
    return format(float(value), ".17g")


def _csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _is_true(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).upper() == "TRUE"


def _bundle_payload(bundle: PretestDevelopmentReconCompletionRunBundle) -> dict[str, Any]:
    return {key: value for key, value in bundle.__dict__.items() if key != "bundle_hash"}

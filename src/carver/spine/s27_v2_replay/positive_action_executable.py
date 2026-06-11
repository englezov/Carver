from __future__ import annotations

import csv
from dataclasses import dataclass
from hashlib import sha256
import json
from math import floor, isclose
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .desired_position_executable import (
    ANNUAL_TARGET_RISK,
    CAPITAL_ACCOUNT_VALUE,
    CONTRACT_POINT_VALUE,
    CONTRACT_POINT_VALUE_CURRENCY,
    FORECAST_TO_POSITION_DIVISOR,
)
from .forecast_executable import FORECAST_CAP_VALUE, FORECAST_SCALAR_VALUE
from .local_replay import canonical_sha256
from .runtime_evidence_gate import REMEDIATION_SOURCE_FILES
from .validation import require_finite_number, require_hash, require_integer, require_positive_number, require_text


S27_V2_POSITIVE_ACTION_AUTHORIZATION = "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_REPLAY_COMPLETION_LOOP"
S27_V2_POSITIVE_ACTION_STATUS = "S27_V2_POSITIVE_ACTION_EXECUTABLE_LOCAL_DEV_RECON_NOT_BACKTEST"
POSITIVE_ACTION_ROW_STATUS = "LOCAL_POSITIVE_ACTION_ORDER_NEEDED_EXECUTION_FAIL_CLOSED_NOT_RESULT"

POSITIVE_ACTION_PACK_RELATIVE_PATH = Path(
    "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260609_positive_action_recon_znm6_20260413T13_declared_pack"
)
POSITIVE_ACTION_MANIFEST_FILENAME = "S27_V2_POSITIVE_ACTION_DECLARED_INPUT_PACK_MANIFEST.json"
EXPECTED_POSITIVE_ACTION_MANIFEST_SHA256 = "c15f545b1a2d2bd046565fbca6d010660492c0ced02f6b35806fae88c81bf6c1"
EXPECTED_ROW_FAMILY_SHA256 = {
    "cost_parameter.csv": "e6b7c69a712fd7a5effbabbd4c809f24c1a6dfabbfb1ce317b387c923ac7f098",
    "daily_continuous_completed_bar.csv": "c3e04982ea9b15382a31c2aeed385197f52f94801fe7bb83fe5a4466fb67d4b6",
    "daily_current_contract_completed_bar.csv": "3907cc08c3245c1ffacd42436a9876c47ea8694039ad575290f7b1fac432973f",
    "hourly_decision_completed_bar.csv": "6ff9f432d2e5d0a692dcfb75bd5cca81eb75473aeb343d44448b01b56476c22e",
    "hourly_fill_completed_bar.csv": "b64990929f623971e62795087666e28eb042207841b2a8401df4eed3f2fad00d",
    "roll_calendar.csv": "0a8e2219c43e24e359642fcc9634cce540885de1751cca54ca6efeed436fef20",
    "session_calendar.csv": "8edfaac6d48450cae5f54d586d60bad982b85ad3bb5b05282b1e6b6b23d65d14",
}

EXPECTED_SELECTED_DECISION = "2026-04-13T13:00:00Z"
EXPECTED_SELECTED_FILL = "2026-04-13T14:00:00Z"
EXPECTED_SELECTED_PREVIOUS_DAILY = "2026-04-12T00:00:00Z"
EXPECTED_RAW_SYMBOL = "ZNM6"

PASS_POSITIVE_DESIRED_POSITION = "PASS_POSITIVE_DESIRED_POSITION_CHANGE_NOT_EXECUTION"
FAIL_CLOSED_EXECUTION_UNRESOLVED = "FAIL_CLOSED_EXECUTION_POLICY_UNRESOLVED_NOT_EMITTED"
FAIL_CLOSED_ACTUAL_FILL = "FAIL_CLOSED_ACTUAL_FILL_LEDGER_NOT_EMITTED"
FAIL_CLOSED_ACTUAL_COST = "FAIL_CLOSED_ACTUAL_COST_LEDGER_NOT_EMITTED"
FAIL_CLOSED_ACTUAL_PNL = "FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED"

POSITIVE_ACTION_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_RESULT_INTERPRETATION",
    "NO_PNL_EVALUATION",
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()


@dataclass(frozen=True)
class PositiveActionExecutableLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    input_pack_path: str
    input_manifest_sha256: str
    selected_decision_timestamp_utc: str
    selected_fill_timestamp_utc: str
    selected_previous_daily_timestamp_utc: str
    raw_symbol: str
    daily_continuous_row_hash: str
    daily_current_contract_row_hash: str
    hourly_decision_row_hash: str
    hourly_fill_row_hash: str
    sigma_source_row_hash: str
    ewmac_source_row_hash: str
    vqm_source_row_hash: str
    ewma5_equilibrium_value: float
    hourly_current_price_value: float
    fill_candidate_price_value: float
    previous_completed_daily_close_value: float
    annual_percentage_sigma_value: float
    raw_mean_reversion_forecast_value: float
    sigma_price_value: float
    risk_adjusted_forecast_before_veto_value: float
    ewmac16_64_trend_value: float
    trend_veto_decision: str
    risk_adjusted_forecast_after_veto_value: float
    relative_volatility_v_value: float
    quantile_q_value: float
    ewma10_multiplier_m_value: float
    capped_forecast_value: float
    base_unrounded_contracts: float
    desired_unrounded_contracts: float
    current_position_before_order: int
    desired_rounded_position: int
    position_change_contracts: int
    order_required: bool
    order_kind: str
    order_side: str
    order_quantity: int
    desired_position_status: str
    adjacent_limit_order_policy_status: str
    tick_rounding_policy_status: str
    working_order_lifecycle_status: str
    actual_limit_order_rows_emitted: bool
    actual_market_order_rows_emitted: bool
    actual_fill_ledger_status: str
    actual_fill_rows_emitted: bool
    actual_cost_ledger_status: str
    actual_cost_rows_emitted: bool
    actual_pnl_ledger_status: str
    actual_pnl_rows_emitted: bool
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_structural_formula(self) -> None:
        if self.ledger_label != "POSITIVE_ACTION_REPLAY_LEDGER":
            raise CarverBlocked("S27 v2 positive-action ledger label is not locked")
        if self.row_status != POSITIVE_ACTION_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action row status is not locked")
        if self.reason_code != "S27_POSITIVE_DESIRED_POSITION_ORDER_NEEDED_EXECUTION_FAIL_CLOSED":
            raise CarverBlocked("S27 v2 positive-action reason code is not locked")
        for name, hash_value in (
            ("manifest", self.input_manifest_sha256),
            ("daily continuous row", self.daily_continuous_row_hash),
            ("daily current-contract row", self.daily_current_contract_row_hash),
            ("hourly decision row", self.hourly_decision_row_hash),
            ("hourly fill row", self.hourly_fill_row_hash),
            ("sigma source row", self.sigma_source_row_hash),
            ("EWMAC source row", self.ewmac_source_row_hash),
            ("V/Q/M source row", self.vqm_source_row_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("decision timestamp", self.selected_decision_timestamp_utc),
            ("fill timestamp", self.selected_fill_timestamp_utc),
            ("previous daily timestamp", self.selected_previous_daily_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("trend veto decision", self.trend_veto_decision),
            ("order kind", self.order_kind),
            ("order side", self.order_side),
            ("desired position status", self.desired_position_status),
            ("adjacent limit policy status", self.adjacent_limit_order_policy_status),
            ("tick rounding policy status", self.tick_rounding_policy_status),
            ("working order lifecycle status", self.working_order_lifecycle_status),
            ("fill ledger status", self.actual_fill_ledger_status),
            ("cost ledger status", self.actual_cost_ledger_status),
            ("PnL ledger status", self.actual_pnl_ledger_status),
        ):
            require_text(f"S27 v2 positive-action {name}", value)
        if self.selected_decision_timestamp_utc != EXPECTED_SELECTED_DECISION:
            raise CarverBlocked("S27 v2 positive-action decision timestamp is not locked")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action fill candidate timestamp is not locked")
        if self.selected_previous_daily_timestamp_utc != EXPECTED_SELECTED_PREVIOUS_DAILY:
            raise CarverBlocked("S27 v2 positive-action previous daily timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 positive-action raw symbol is not locked")
        self._validate_numeric_chain()
        self._validate_position_and_fail_closed_execution()
        if self.row_hash != canonical_sha256(_positive_action_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action row hash must be content-bound")

    def _validate_numeric_chain(self) -> None:
        for name, value in (
            ("EWMA5 equilibrium", self.ewma5_equilibrium_value),
            ("hourly current price", self.hourly_current_price_value),
            ("fill candidate price", self.fill_candidate_price_value),
            ("previous daily close", self.previous_completed_daily_close_value),
            ("annual sigma", self.annual_percentage_sigma_value),
            ("raw forecast", self.raw_mean_reversion_forecast_value),
            ("sigma price", self.sigma_price_value),
            ("risk-adjusted forecast before veto", self.risk_adjusted_forecast_before_veto_value),
            ("EWMAC trend", self.ewmac16_64_trend_value),
            ("risk-adjusted forecast after veto", self.risk_adjusted_forecast_after_veto_value),
            ("relative volatility V", self.relative_volatility_v_value),
            ("quantile Q", self.quantile_q_value),
            ("EWMA10 multiplier M", self.ewma10_multiplier_m_value),
            ("capped forecast", self.capped_forecast_value),
            ("base unrounded contracts", self.base_unrounded_contracts),
            ("desired unrounded contracts", self.desired_unrounded_contracts),
        ):
            require_finite_number(f"S27 v2 positive-action {name}", value)
        require_positive_number("S27 v2 positive-action annual sigma", self.annual_percentage_sigma_value)
        require_positive_number("S27 v2 positive-action sigma price", self.sigma_price_value)
        expected_raw = self.ewma5_equilibrium_value - self.hourly_current_price_value
        _require_close("S27 v2 positive-action raw forecast", self.raw_mean_reversion_forecast_value, expected_raw)
        expected_sigma_price = self.previous_completed_daily_close_value * self.annual_percentage_sigma_value / 16.0
        _require_close("S27 v2 positive-action sigma price", self.sigma_price_value, expected_sigma_price)
        expected_before_veto = self.raw_mean_reversion_forecast_value / self.sigma_price_value
        _require_close(
            "S27 v2 positive-action risk-adjusted forecast before veto",
            self.risk_adjusted_forecast_before_veto_value,
            expected_before_veto,
        )
        expected_decision, expected_after_veto = _trend_veto(
            self.risk_adjusted_forecast_before_veto_value,
            self.ewmac16_64_trend_value,
        )
        if self.trend_veto_decision != expected_decision:
            raise CarverBlocked("S27 v2 positive-action trend veto decision must bind signs")
        _require_close(
            "S27 v2 positive-action forecast after veto",
            self.risk_adjusted_forecast_after_veto_value,
            expected_after_veto,
        )
        if self.trend_veto_decision != "PERMIT_MEAN_REVERSION":
            raise CarverBlocked("S27 v2 positive-action gate requires the earliest nonzero permitted forecast")
        if self.quantile_q_value < 0.0 or self.quantile_q_value > 1.0:
            raise CarverBlocked("S27 v2 positive-action quantile Q must be in [0, 1]")
        expected_capped = _clamp(
            self.risk_adjusted_forecast_after_veto_value
            * self.ewma10_multiplier_m_value
            * FORECAST_SCALAR_VALUE,
            -FORECAST_CAP_VALUE,
            FORECAST_CAP_VALUE,
        )
        _require_close("S27 v2 positive-action capped forecast", self.capped_forecast_value, expected_capped)
        expected_base = (
            CAPITAL_ACCOUNT_VALUE
            * ANNUAL_TARGET_RISK
            / (
                self.hourly_current_price_value
                * CONTRACT_POINT_VALUE
                * self.annual_percentage_sigma_value
            )
        )
        _require_close("S27 v2 positive-action base position", self.base_unrounded_contracts, expected_base)
        expected_desired = self.base_unrounded_contracts * self.capped_forecast_value / FORECAST_TO_POSITION_DIVISOR
        _require_close("S27 v2 positive-action desired unrounded", self.desired_unrounded_contracts, expected_desired)

    def _validate_position_and_fail_closed_execution(self) -> None:
        for name, value in (
            ("current position", self.current_position_before_order),
            ("desired rounded position", self.desired_rounded_position),
            ("position change", self.position_change_contracts),
            ("order quantity", self.order_quantity),
        ):
            require_integer(f"S27 v2 positive-action {name}", value)
        if self.current_position_before_order != 0:
            raise CarverBlocked("S27 v2 positive-action first-row current position must remain flat zero")
        expected_rounded = _round_half_away_from_zero(self.desired_unrounded_contracts)
        if self.desired_rounded_position != expected_rounded:
            raise CarverBlocked("S27 v2 positive-action desired rounded position must bind rounding policy")
        if self.desired_rounded_position == 0:
            raise CarverBlocked("S27 v2 positive-action gate requires nonzero desired rounded position")
        if self.position_change_contracts != self.desired_rounded_position - self.current_position_before_order:
            raise CarverBlocked("S27 v2 positive-action position change must bind desired minus current")
        if self.order_required is not True:
            raise CarverBlocked("S27 v2 positive-action nonzero position change must require an order intent")
        expected_side = "BUY" if self.position_change_contracts > 0 else "SELL"
        if self.order_kind != "ORDER_INTENT_EXECUTION_FAIL_CLOSED" or self.order_side != expected_side:
            raise CarverBlocked("S27 v2 positive-action order intent side must bind position change")
        if self.order_quantity != abs(self.position_change_contracts):
            raise CarverBlocked("S27 v2 positive-action order quantity must bind absolute position change")
        if self.desired_position_status != PASS_POSITIVE_DESIRED_POSITION:
            raise CarverBlocked("S27 v2 positive-action desired position status is not locked")
        for status in (
            self.adjacent_limit_order_policy_status,
            self.tick_rounding_policy_status,
            self.working_order_lifecycle_status,
        ):
            if status != FAIL_CLOSED_EXECUTION_UNRESOLVED:
                raise CarverBlocked("S27 v2 positive-action execution policies must remain fail-closed")
        if self.actual_fill_ledger_status != FAIL_CLOSED_ACTUAL_FILL:
            raise CarverBlocked("S27 v2 positive-action actual fill ledger must remain fail-closed")
        if self.actual_cost_ledger_status != FAIL_CLOSED_ACTUAL_COST:
            raise CarverBlocked("S27 v2 positive-action actual cost ledger must remain fail-closed")
        if self.actual_pnl_ledger_status != FAIL_CLOSED_ACTUAL_PNL:
            raise CarverBlocked("S27 v2 positive-action actual PnL ledger must remain fail-closed")
        if any(
            flag is not False
            for flag in (
                self.actual_limit_order_rows_emitted,
                self.actual_market_order_rows_emitted,
                self.actual_fill_rows_emitted,
                self.actual_cost_rows_emitted,
                self.actual_pnl_rows_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action gate cannot emit actual execution/cost/PnL rows")


@dataclass(frozen=True)
class PositiveActionExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    positive_action_row: PositiveActionExecutableLedgerRow
    desired_position_rows_emitted: bool
    order_intent_rows_emitted: bool
    order_transition_metadata_rows_emitted: bool
    actual_limit_order_rows_emitted: bool
    actual_market_order_rows_emitted: bool
    actual_fill_rows_emitted: bool
    actual_cost_rows_emitted: bool
    actual_pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = POSITIVE_ACTION_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_STATUS:
            raise CarverBlocked("S27 v2 positive-action bundle status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_AUTHORIZATION:
            raise CarverBlocked("S27 v2 positive-action authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 positive-action must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 positive-action lane must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action executable is locked to the declared positive-action pack")
        self.positive_action_row._validate_structural_formula()
        active_row = _build_active_positive_action_row(pack_path)
        if self.positive_action_row != active_row:
            raise CarverBlocked("S27 v2 positive-action row must match active local pack/source evidence")
        if any(
            flag is not True
            for flag in (
                self.desired_position_rows_emitted,
                self.order_intent_rows_emitted,
                self.order_transition_metadata_rows_emitted,
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action bundle must emit only authorized metadata surfaces")
        if any(
            flag is not False
            for flag in (
                self.actual_limit_order_rows_emitted,
                self.actual_market_order_rows_emitted,
                self.actual_fill_rows_emitted,
                self.actual_cost_rows_emitted,
                self.actual_pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action bundle cannot emit actual execution/cost/PnL/result/evidence")
        if self.non_authorizations != POSITIVE_ACTION_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 positive-action bundle must preserve non-authorizations")
        require_hash("S27 v2 positive-action bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_positive_action_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action bundle hash must be content-bound")


def build_positive_action_executable_replay(
    input_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
) -> PositiveActionExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action executable is locked to the declared positive-action pack")
    row = _build_active_positive_action_row(pack_path)
    bundle = PositiveActionExecutableBundle(
        status=S27_V2_POSITIVE_ACTION_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        positive_action_row=row,
        desired_position_rows_emitted=True,
        order_intent_rows_emitted=True,
        order_transition_metadata_rows_emitted=True,
        actual_limit_order_rows_emitted=False,
        actual_market_order_rows_emitted=False,
        actual_fill_rows_emitted=False,
        actual_cost_rows_emitted=False,
        actual_pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_positive_action_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_positive_action_row(pack_path: Path) -> PositiveActionExecutableLedgerRow:
    manifest = _read_manifest(pack_path)
    rows_by_file = _read_rows_by_file(pack_path)
    _verify_row_family_hashes(pack_path, manifest)
    source_rows = _locked_source_rows(manifest)
    daily_continuous_rows = rows_by_file["daily_continuous_completed_bar.csv"]
    selected_daily_continuous = daily_continuous_rows[0]
    selected_daily_current = rows_by_file["daily_current_contract_completed_bar.csv"][0]
    selected_hourly_decision = rows_by_file["hourly_decision_completed_bar.csv"][0]
    selected_hourly_fill = rows_by_file["hourly_fill_completed_bar.csv"][0]
    _validate_pack_rows_against_source_rows(
        manifest,
        selected_daily_continuous,
        selected_daily_current,
        selected_hourly_decision,
        selected_hourly_fill,
        source_rows,
    )
    _validate_manifest_runtime_values_against_source_rows(manifest, source_rows)
    chronological_daily = tuple(daily_continuous_rows[1:]) + (selected_daily_continuous,)
    ewma5 = _recursive_ewma(tuple(_as_float(row["close_price"], "daily close") for row in chronological_daily), 5)
    hourly_price = _as_float(selected_hourly_decision["close_price"], "hourly decision close")
    fill_price = _as_float(selected_hourly_fill["close_price"], "hourly fill close")
    previous_close = _as_float(selected_daily_current["close_price"], "previous current close")
    sigma = _as_float(source_rows["sigma_runtime_ledger"]["sigma_percent_t"], "selected sigma")
    raw_forecast = ewma5 - hourly_price
    sigma_price = previous_close * sigma / 16.0
    risk_before_veto = raw_forecast / sigma_price
    trend = _as_float(source_rows["ewmac_runtime_rows"]["trend_forecast"], "EWMAC trend")
    trend_decision, risk_after_veto = _trend_veto(risk_before_veto, trend)
    relative_v = _as_float(source_rows["vqm_runtime_rows"]["relative_volatility_v"], "V")
    quantile_q = _as_float(source_rows["vqm_runtime_rows"]["quantile_q"], "Q")
    multiplier_m = _as_float(source_rows["vqm_runtime_rows"]["vol_multiplier"], "M")
    capped_forecast = _clamp(risk_after_veto * multiplier_m * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)
    base_position = CAPITAL_ACCOUNT_VALUE * ANNUAL_TARGET_RISK / (hourly_price * CONTRACT_POINT_VALUE * sigma)
    desired_unrounded = base_position * capped_forecast / FORECAST_TO_POSITION_DIVISOR
    desired_rounded = _round_half_away_from_zero(desired_unrounded)
    position_change = desired_rounded
    row_hashes = _row_hashes_by_file(rows_by_file)
    row = PositiveActionExecutableLedgerRow(
        ledger_label="POSITIVE_ACTION_REPLAY_LEDGER",
        row_status=POSITIVE_ACTION_ROW_STATUS,
        reason_code="S27_POSITIVE_DESIRED_POSITION_ORDER_NEEDED_EXECUTION_FAIL_CLOSED",
        input_pack_path=str(pack_path),
        input_manifest_sha256=EXPECTED_POSITIVE_ACTION_MANIFEST_SHA256,
        selected_decision_timestamp_utc=manifest["selected_decision_timestamp_utc"],
        selected_fill_timestamp_utc=manifest["selected_fill_timestamp_utc"],
        selected_previous_daily_timestamp_utc=manifest["selected_previous_daily_timestamp_utc"],
        raw_symbol=manifest["selected_raw_symbol"],
        daily_continuous_row_hash=row_hashes["daily_continuous_completed_bar.csv"][0],
        daily_current_contract_row_hash=row_hashes["daily_current_contract_completed_bar.csv"][0],
        hourly_decision_row_hash=row_hashes["hourly_decision_completed_bar.csv"][0],
        hourly_fill_row_hash=row_hashes["hourly_fill_completed_bar.csv"][0],
        sigma_source_row_hash=_source_row_hash("sigma_runtime_ledger", source_rows["sigma_runtime_ledger"]),
        ewmac_source_row_hash=_source_row_hash("ewmac_runtime_rows", source_rows["ewmac_runtime_rows"]),
        vqm_source_row_hash=_source_row_hash("vqm_runtime_rows", source_rows["vqm_runtime_rows"]),
        ewma5_equilibrium_value=ewma5,
        hourly_current_price_value=hourly_price,
        fill_candidate_price_value=fill_price,
        previous_completed_daily_close_value=previous_close,
        annual_percentage_sigma_value=sigma,
        raw_mean_reversion_forecast_value=raw_forecast,
        sigma_price_value=sigma_price,
        risk_adjusted_forecast_before_veto_value=risk_before_veto,
        ewmac16_64_trend_value=trend,
        trend_veto_decision=trend_decision,
        risk_adjusted_forecast_after_veto_value=risk_after_veto,
        relative_volatility_v_value=relative_v,
        quantile_q_value=quantile_q,
        ewma10_multiplier_m_value=multiplier_m,
        capped_forecast_value=capped_forecast,
        base_unrounded_contracts=base_position,
        desired_unrounded_contracts=desired_unrounded,
        current_position_before_order=0,
        desired_rounded_position=desired_rounded,
        position_change_contracts=position_change,
        order_required=True,
        order_kind="ORDER_INTENT_EXECUTION_FAIL_CLOSED",
        order_side="BUY" if position_change > 0 else "SELL",
        order_quantity=abs(position_change),
        desired_position_status=PASS_POSITIVE_DESIRED_POSITION,
        adjacent_limit_order_policy_status=FAIL_CLOSED_EXECUTION_UNRESOLVED,
        tick_rounding_policy_status=FAIL_CLOSED_EXECUTION_UNRESOLVED,
        working_order_lifecycle_status=FAIL_CLOSED_EXECUTION_UNRESOLVED,
        actual_limit_order_rows_emitted=False,
        actual_market_order_rows_emitted=False,
        actual_fill_ledger_status=FAIL_CLOSED_ACTUAL_FILL,
        actual_fill_rows_emitted=False,
        actual_cost_ledger_status=FAIL_CLOSED_ACTUAL_COST,
        actual_cost_rows_emitted=False,
        actual_pnl_ledger_status=FAIL_CLOSED_ACTUAL_PNL,
        actual_pnl_rows_emitted=False,
        row_hash="0" * 64,
    )
    row = PositiveActionExecutableLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_positive_action_row_hash_payload(row))}
    )
    row._validate_structural_formula()
    return row


def _read_manifest(pack_path: Path) -> dict[str, Any]:
    manifest_path = pack_path / POSITIVE_ACTION_MANIFEST_FILENAME
    observed_hash = sha256(manifest_path.read_bytes()).hexdigest()
    if observed_hash != EXPECTED_POSITIVE_ACTION_MANIFEST_SHA256:
        raise CarverBlocked("S27 v2 positive-action manifest byte hash must match declared pack")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise CarverBlocked("S27 v2 positive-action manifest must be a JSON object")
    return manifest


def _verify_row_family_hashes(pack_path: Path, manifest: dict[str, Any]) -> None:
    declared = manifest.get("row_family_files")
    if not isinstance(declared, dict) or set(declared) != set(EXPECTED_ROW_FAMILY_SHA256):
        raise CarverBlocked("S27 v2 positive-action row-family declaration must match locked files")
    for filename, expected_hash in EXPECTED_ROW_FAMILY_SHA256.items():
        observed_hash = sha256((pack_path / filename).read_bytes()).hexdigest()
        if observed_hash != expected_hash:
            raise CarverBlocked("S27 v2 positive-action row-family bytes must match declared pack")
        if str(declared[filename]["sha256"]).lower() != expected_hash:
            raise CarverBlocked("S27 v2 positive-action manifest row-family hash must match bytes")


def _locked_source_rows(manifest: dict[str, Any]) -> dict[str, dict[str, str]]:
    declared_source_files = manifest.get("source_files")
    if not isinstance(declared_source_files, dict) or set(declared_source_files) != set(REMEDIATION_SOURCE_FILES):
        raise CarverBlocked("S27 v2 positive-action source files must match locked local source set")
    selected_decision = str(manifest["selected_decision_timestamp_utc"])
    source_rows: dict[str, dict[str, str]] = {}
    for label in REMEDIATION_SOURCE_FILES:
        _verify_declared_source_file(label, declared_source_files)
    for label in ("sigma_runtime_ledger", "ewmac_runtime_rows", "vqm_runtime_rows"):
        expected_relative_path = REMEDIATION_SOURCE_FILES[label]
        source_rows[label] = _row_by_value(_read_csv_rows(_REPO_ROOT / expected_relative_path), "as_of", selected_decision)
    source_rows["daily_risk_history"] = _row_by_value(
        _read_csv_rows(_REPO_ROOT / REMEDIATION_SOURCE_FILES["daily_risk_history"]),
        "completed_trading_date",
        str(manifest["selected_previous_daily_timestamp_utc"])[:10],
    )
    hourly_source = _read_csv_rows(_REPO_ROOT / REMEDIATION_SOURCE_FILES["hourly_sanitized_bars"])
    source_rows["hourly_decision_source"] = _row_by_value(
        hourly_source,
        "derived_completed_bar_end_utc",
        selected_decision,
    )
    source_rows["hourly_fill_source"] = _row_by_value(
        hourly_source,
        "derived_completed_bar_end_utc",
        str(manifest["selected_fill_timestamp_utc"]),
    )
    if source_rows["sigma_runtime_ledger"]["runtime_status"] != "PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 positive-action sigma source status is not locked")
    if source_rows["ewmac_runtime_rows"]["runtime_status"] != "PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 positive-action EWMAC source status is not locked")
    if source_rows["vqm_runtime_rows"]["runtime_status"] != "PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 positive-action V/Q/M source status is not locked")
    for label, row in source_rows.items():
        if label in ("daily_risk_history", "hourly_decision_source", "hourly_fill_source"):
            continue
        if row["no_lookahead_status"] != "PASS_NO_LOOKAHEAD":
            raise CarverBlocked(f"S27 v2 positive-action {label} source must be no-lookahead")
    return source_rows


def _verify_declared_source_file(label: str, declared_source_files: dict[str, Any]) -> None:
    expected_relative_path = REMEDIATION_SOURCE_FILES[label]
    declared = declared_source_files[label]
    if declared["path"].replace("\\", "/") != expected_relative_path.as_posix():
        raise CarverBlocked("S27 v2 positive-action source path must bind locked local source")
    observed_hash = sha256((_REPO_ROOT / expected_relative_path).read_bytes()).hexdigest()
    if observed_hash != str(declared["sha256"]).lower():
        raise CarverBlocked("S27 v2 positive-action source hash must match local bytes")


def _validate_pack_rows_against_source_rows(
    manifest: dict[str, Any],
    selected_daily_continuous: dict[str, str],
    selected_daily_current: dict[str, str],
    selected_hourly_decision: dict[str, str],
    selected_hourly_fill: dict[str, str],
    source_rows: dict[str, dict[str, str]],
) -> None:
    daily_source = source_rows["daily_risk_history"]
    if daily_source["raw_symbol"] != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 positive-action daily source row must bind ZNM6")
    if daily_source["additive_back_adjustment"] != "0.0":
        raise CarverBlocked("S27 v2 positive-action daily source row must bind zero adjustment")
    expected_daily_ts = str(manifest["selected_previous_daily_timestamp_utc"])
    for label, row in (
        ("daily continuous", selected_daily_continuous),
        ("daily current-contract", selected_daily_current),
    ):
        if row["completed_timestamp_utc"] != expected_daily_ts:
            raise CarverBlocked(f"S27 v2 positive-action {label} row must bind selected previous daily timestamp")
        if row["trading_date"] != daily_source["completed_trading_date"]:
            raise CarverBlocked(f"S27 v2 positive-action {label} row must bind daily source trading date")
        if row["raw_symbol"] != daily_source["raw_symbol"]:
            raise CarverBlocked(f"S27 v2 positive-action {label} row must bind daily source raw symbol")
        _require_close(
            f"S27 v2 positive-action {label} close",
            _as_float(row["close_price"], f"{label} close"),
            _as_float(daily_source["continuous_close"], "daily source continuous close"),
        )
    for label, row, source_key in (
        ("hourly decision", selected_hourly_decision, "hourly_decision_source"),
        ("hourly fill", selected_hourly_fill, "hourly_fill_source"),
    ):
        source = source_rows[source_key]
        if source["raw_symbol"] != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked(f"S27 v2 positive-action {label} source row must bind ZNM6")
        if source["provider_condition_status"] != "PROVIDER_CONDITION_AVAILABLE":
            raise CarverBlocked(f"S27 v2 positive-action {label} source row must be provider-available locally")
        if source["row_shape_status"] != "PASS_OHLCV_1H_ROW_SHAPE":
            raise CarverBlocked(f"S27 v2 positive-action {label} source row shape must pass")
        if row["completed_timestamp_utc"] != source["derived_completed_bar_end_utc"]:
            raise CarverBlocked(f"S27 v2 positive-action {label} row must bind source completed timestamp")
        if row["trading_date"] != source["completed_trading_date"]:
            raise CarverBlocked(f"S27 v2 positive-action {label} row must bind source trading date")
        if row["raw_symbol"] != source["raw_symbol"]:
            raise CarverBlocked(f"S27 v2 positive-action {label} row must bind source raw symbol")
        _require_close(
            f"S27 v2 positive-action {label} close",
            _as_float(row["close_price"], f"{label} close"),
            _as_float(source["close"], f"{label} source close"),
        )


def _validate_manifest_runtime_values_against_source_rows(
    manifest: dict[str, Any],
    source_rows: dict[str, dict[str, str]],
) -> None:
    history_evidence = manifest.get("history_evidence")
    if not isinstance(history_evidence, dict):
        raise CarverBlocked("S27 v2 positive-action history evidence must be a manifest object")
    comparisons = (
        (
            "selected sigma",
            history_evidence.get("selected_sigma_percent_t"),
            source_rows["sigma_runtime_ledger"]["sigma_percent_t"],
        ),
        (
            "selected V/Q/M relative volatility V",
            history_evidence.get("selected_vqm_relative_volatility_v"),
            source_rows["vqm_runtime_rows"]["relative_volatility_v"],
        ),
        (
            "selected V/Q/M quantile Q",
            history_evidence.get("selected_vqm_quantile_q"),
            source_rows["vqm_runtime_rows"]["quantile_q"],
        ),
        (
            "selected V/Q/M multiplier M",
            history_evidence.get("selected_vqm_multiplier_m"),
            source_rows["vqm_runtime_rows"]["vol_multiplier"],
        ),
    )
    for label, manifest_value, source_value in comparisons:
        _require_close(
            f"S27 v2 positive-action {label} manifest/source binding",
            _as_float(str(manifest_value), f"{label} manifest value"),
            _as_float(str(source_value), f"{label} source value"),
        )


def _read_rows_by_file(pack_path: Path) -> dict[str, tuple[dict[str, str], ...]]:
    return {filename: tuple(_read_csv_rows(pack_path / filename)) for filename in EXPECTED_ROW_FAMILY_SHA256}


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise CarverBlocked(f"S27 v2 positive-action file {path.name} has no rows")
    return rows


def _row_hashes_by_file(rows_by_file: dict[str, tuple[dict[str, str], ...]]) -> dict[str, tuple[str, ...]]:
    row_family_by_file = {
        "daily_continuous_completed_bar.csv": "DAILY_CONTINUOUS_COMPLETED_BAR",
        "daily_current_contract_completed_bar.csv": "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
        "hourly_decision_completed_bar.csv": "HOURLY_DECISION_COMPLETED_BAR",
        "hourly_fill_completed_bar.csv": "HOURLY_FILL_COMPLETED_BAR",
        "session_calendar.csv": "SESSION_CALENDAR",
        "roll_calendar.csv": "ROLL_CALENDAR",
        "cost_parameter.csv": "COST_PARAMETER",
    }
    return {
        filename: tuple(
            canonical_sha256(
                {
                    "artifact": "S27_V2_LOCAL_SOURCE_ROW",
                    "row_family": row_family_by_file[filename],
                    "row_number": row_number,
                    "row": row,
                }
            )
            for row_number, row in enumerate(rows, start=1)
        )
        for filename, rows in rows_by_file.items()
    }


def _row_by_value(rows: list[dict[str, str]], column: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(column) == value]
    if len(matches) != 1:
        raise CarverBlocked(f"S27 v2 positive-action source row must have exactly one {column}={value}")
    return matches[0]


def _as_float(value: str, label: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CarverBlocked(f"S27 v2 positive-action {label} must be numeric") from exc
    require_finite_number(f"S27 v2 positive-action {label}", parsed)
    return parsed


def _recursive_ewma(values: tuple[float, ...], span: int) -> float:
    if len(values) < span:
        raise CarverBlocked("S27 v2 positive-action EWMA history is insufficient")
    alpha = 2.0 / (span + 1.0)
    smoothed = values[0]
    for value in values[1:]:
        smoothed = alpha * value + (1.0 - alpha) * smoothed
    return smoothed


def _trend_veto(risk_adjusted_forecast: float, trend_forecast: float) -> tuple[str, float]:
    if isclose(risk_adjusted_forecast, 0.0, rel_tol=0.0, abs_tol=1e-12):
        return "FLAT_AT_EQUILIBRIUM", 0.0
    if risk_adjusted_forecast * trend_forecast < 0.0:
        return "ZERO_FORECAST_BY_TREND_VETO", 0.0
    return "PERMIT_MEAN_REVERSION", risk_adjusted_forecast


def _round_half_away_from_zero(value: float) -> int:
    require_finite_number("S27 v2 positive-action rounding input", value)
    if value > 0:
        return floor(value + 0.5)
    if value < 0:
        return -floor(abs(value) + 0.5)
    return 0


def _clamp(value: float, lower: float, upper: float) -> float:
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value


def _require_close(name: str, observed: float, expected: float) -> None:
    if not isclose(observed, expected, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked(f"{name} must bind source formula")


def _source_row_hash(label: str, row: dict[str, str]) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_LOCKED_SOURCE_ROW", "label": label, "row": row})


def _positive_action_row_hash_payload(row: PositiveActionExecutableLedgerRow) -> dict[str, object]:
    return {
        key: value
        for key, value in row.__dict__.items()
        if key != "row_hash"
    }


def _positive_action_bundle_hash_payload(bundle: PositiveActionExecutableBundle) -> dict[str, object]:
    return {
        "actual_cost_rows_emitted": bundle.actual_cost_rows_emitted,
        "actual_fill_rows_emitted": bundle.actual_fill_rows_emitted,
        "actual_limit_order_rows_emitted": bundle.actual_limit_order_rows_emitted,
        "actual_market_order_rows_emitted": bundle.actual_market_order_rows_emitted,
        "actual_pnl_rows_emitted": bundle.actual_pnl_rows_emitted,
        "artifact": "S27_V2_POSITIVE_ACTION_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "desired_position_rows_emitted": bundle.desired_position_rows_emitted,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "order_intent_rows_emitted": bundle.order_intent_rows_emitted,
        "order_transition_metadata_rows_emitted": bundle.order_transition_metadata_rows_emitted,
        "positive_action_row_hash": bundle.positive_action_row.row_hash,
        "provenance_metadata_rows_emitted": bundle.provenance_metadata_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "trusted_bundle_metadata_emitted": bundle.trusted_bundle_metadata_emitted,
        "validation_metadata_rows_emitted": bundle.validation_metadata_rows_emitted,
    }

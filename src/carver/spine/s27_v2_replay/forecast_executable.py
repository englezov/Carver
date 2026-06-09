from __future__ import annotations

import csv
from dataclasses import dataclass
from hashlib import sha256
import json
from math import isclose
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import (
    BLOCKED_COST_SCHEMA,
    BLOCKED_INITIAL_POSITION,
    BLOCKED_TICK,
    BLOCKED_WORKING_LIMIT_LIFECYCLE,
    REQUIRED_UNRESOLVED_GATE_LABELS,
    S27_V2_INSTRUMENT,
    S27_V2_LANE,
    S27_V2_STRATEGY_ID,
)
from .local_replay import canonical_sha256
from .runtime_evidence_gate import (
    REMEDIATION_SOURCE_FILES,
    RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH,
)
from .runtime_history_executable import (
    RuntimeHistoryRemediationExecutableBundle,
    build_runtime_history_executable_ledgers_on_remediation_pack,
)
from .validation import require_finite_number, require_hash, require_positive_number, require_text, require_tuple


S27_V2_FORECAST_EXECUTABLE_AUTHORIZATION = "S27_V2_LOCAL_ONLY_RUNTIME_NUMERIC_STATE_AND_FORECAST_LEDGER"
S27_V2_FORECAST_EXECUTABLE_STATUS = "S27_V2_FORECAST_EXECUTABLE_REMEDIATION_PACK_NON_RESULT_NOT_EVIDENCE"
FORECAST_LEDGER_ROW_STATUS = "LOCAL_FORECAST_LEDGER_EMITTED_NOT_POSITION_NOT_RESULT_NOT_EVIDENCE"
FORECAST_SCALAR_LABEL = "BOOK_APPROXIMATE_SCALAR_IMPLEMENTATION_FROZEN_AT_20_0"
FORECAST_SCALAR_VALUE = 20.0
FORECAST_CAP_VALUE = 20.0
EWMA5_SPAN = 5

FORECAST_EXECUTABLE_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_POSITION_ORDER_FILL_COST_PNL_RESULT_EMISSION",
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
_REMEDIATION_PACK_PATH = (_REPO_ROOT / RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH).resolve()


@dataclass(frozen=True)
class ForecastExecutableLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    runtime_history_bundle_hash: str
    runtime_evidence_bundle_hash: str
    level_compatibility_row_hash: str
    runtime_history_row_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    selected_previous_daily_timestamp_utc: str
    raw_symbol: str
    daily_continuous_row_hash: str
    daily_current_contract_row_hash: str
    hourly_decision_row_hash: str
    sigma_source_row_hash: str
    ewmac_source_row_hash: str
    vqm_source_row_hash: str
    ewma5_policy_hash: str
    ewma5_equilibrium_value: float
    ewma5_equilibrium_hash: str
    hourly_current_price_value: float
    hourly_current_price_hash: str
    previous_completed_daily_close_current_contract_value: float
    previous_completed_daily_close_current_contract_hash: str
    raw_mean_reversion_forecast_value: float
    raw_mean_reversion_forecast_hash: str
    annual_percentage_sigma_value: float
    annual_percentage_sigma_hash: str
    sigma_price_value: float
    sigma_price_hash: str
    risk_adjusted_forecast_before_veto_value: float
    risk_adjusted_forecast_before_veto_hash: str
    ewmac16_64_trend_value: float
    ewmac16_64_trend_sign: str
    ewmac16_64_trend_hash: str
    trend_veto_decision: str
    trend_veto_decision_hash: str
    risk_adjusted_forecast_after_veto_value: float
    risk_adjusted_forecast_after_veto_hash: str
    relative_volatility_v_value: float
    relative_volatility_v_hash: str
    quantile_q_value: float
    quantile_q_hash: str
    raw_volatility_multiplier_value: float
    raw_volatility_multiplier_hash: str
    ewma10_multiplier_m_value: float
    ewma10_multiplier_m_hash: str
    risk_adjusted_after_veto_times_m_before_scalar_value: float
    risk_adjusted_after_veto_times_m_before_scalar_hash: str
    scalar_label: str
    scalar_value: float
    scalar_value_hash: str
    capped_forecast_value: float
    capped_forecast_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 forecast executable row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_structural_formula(self) -> None:
        if self.ledger_label != "FORECAST_REPLAY_LEDGER":
            raise CarverBlocked("S27 v2 forecast executable ledger label is not locked")
        if self.row_status != FORECAST_LEDGER_ROW_STATUS:
            raise CarverBlocked("S27 v2 forecast executable row status is not locked")
        if self.reason_code != "S26_S27_NUMERIC_FORECAST_CHAIN_BOUND_TO_RUNTIME_EVIDENCE_NOT_POSITION":
            raise CarverBlocked("S27 v2 forecast executable reason is not locked")
        for name, hash_value in (
            ("runtime history bundle hash", self.runtime_history_bundle_hash),
            ("runtime evidence bundle hash", self.runtime_evidence_bundle_hash),
            ("level compatibility row hash", self.level_compatibility_row_hash),
            ("runtime history row hash", self.runtime_history_row_hash),
            ("daily continuous row hash", self.daily_continuous_row_hash),
            ("daily current-contract row hash", self.daily_current_contract_row_hash),
            ("hourly decision row hash", self.hourly_decision_row_hash),
            ("sigma source row hash", self.sigma_source_row_hash),
            ("EWMAC source row hash", self.ewmac_source_row_hash),
            ("V/Q/M source row hash", self.vqm_source_row_hash),
            ("EWMA5 policy hash", self.ewma5_policy_hash),
        ):
            require_hash(f"S27 v2 forecast executable {name}", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("selected previous daily timestamp", self.selected_previous_daily_timestamp_utc),
            ("raw symbol", self.raw_symbol),
        ):
            require_text(f"S27 v2 forecast executable {name}", value)
        self._validate_value_hash("EWMA5 equilibrium", self.ewma5_equilibrium_value, self.ewma5_equilibrium_hash)
        self._validate_value_hash("hourly current price", self.hourly_current_price_value, self.hourly_current_price_hash)
        self._validate_value_hash(
            "previous daily current contract close",
            self.previous_completed_daily_close_current_contract_value,
            self.previous_completed_daily_close_current_contract_hash,
        )
        expected_raw = self.ewma5_equilibrium_value - self.hourly_current_price_value
        self._validate_value_hash("raw mean-reversion forecast", self.raw_mean_reversion_forecast_value, self.raw_mean_reversion_forecast_hash)
        _require_close("S27 v2 raw forecast", self.raw_mean_reversion_forecast_value, expected_raw)
        self._validate_positive_value_hash("annual percentage sigma", self.annual_percentage_sigma_value, self.annual_percentage_sigma_hash)
        self._validate_positive_value_hash("sigma price", self.sigma_price_value, self.sigma_price_hash)
        expected_sigma_price = (
            self.previous_completed_daily_close_current_contract_value
            * self.annual_percentage_sigma_value
            / 16.0
        )
        _require_close("S27 v2 sigma price", self.sigma_price_value, expected_sigma_price)
        self._validate_value_hash(
            "risk-adjusted forecast before veto",
            self.risk_adjusted_forecast_before_veto_value,
            self.risk_adjusted_forecast_before_veto_hash,
        )
        expected_risk_adjusted = self.raw_mean_reversion_forecast_value / self.sigma_price_value
        _require_close("S27 v2 risk-adjusted forecast before veto", self.risk_adjusted_forecast_before_veto_value, expected_risk_adjusted)
        trend_sign = _nonzero_sign("S27 v2 EWMAC16/64 trend value", self.ewmac16_64_trend_value)
        if self.ewmac16_64_trend_sign != trend_sign:
            raise CarverBlocked("S27 v2 forecast executable trend sign must match trend value")
        self._validate_value_hash("EWMAC16/64 trend", self.ewmac16_64_trend_value, self.ewmac16_64_trend_hash)
        if self.trend_veto_decision not in (
            "PERMIT_MEAN_REVERSION",
            "ZERO_FORECAST_BY_TREND_VETO",
            "FLAT_AT_EQUILIBRIUM",
        ):
            raise CarverBlocked("S27 v2 forecast executable trend veto decision is not locked")
        require_hash("S27 v2 forecast executable trend veto decision hash", self.trend_veto_decision_hash)
        self._validate_value_hash(
            "risk-adjusted forecast after veto",
            self.risk_adjusted_forecast_after_veto_value,
            self.risk_adjusted_forecast_after_veto_hash,
        )
        expected_veto_decision, expected_after_veto = _trend_veto(
            self.risk_adjusted_forecast_before_veto_value,
            self.ewmac16_64_trend_value,
        )
        if self.trend_veto_decision != expected_veto_decision:
            raise CarverBlocked("S27 v2 forecast executable trend veto decision must bind signs")
        if self.trend_veto_decision_hash != _value_hash("trend_veto_decision", self.trend_veto_decision):
            raise CarverBlocked("S27 v2 forecast executable trend veto decision hash must bind decision")
        _require_close("S27 v2 forecast after veto", self.risk_adjusted_forecast_after_veto_value, expected_after_veto)
        self._validate_positive_value_hash("relative volatility V", self.relative_volatility_v_value, self.relative_volatility_v_hash)
        self._validate_value_hash("quantile Q", self.quantile_q_value, self.quantile_q_hash)
        if self.quantile_q_value < 0.0 or self.quantile_q_value > 1.0:
            raise CarverBlocked("S27 v2 forecast executable quantile Q must be in [0, 1]")
        self._validate_positive_value_hash(
            "raw volatility multiplier",
            self.raw_volatility_multiplier_value,
            self.raw_volatility_multiplier_hash,
        )
        _require_close(
            "S27 v2 raw volatility multiplier",
            self.raw_volatility_multiplier_value,
            2.0 - (1.5 * self.quantile_q_value),
        )
        self._validate_positive_value_hash("EWMA10 multiplier M", self.ewma10_multiplier_m_value, self.ewma10_multiplier_m_hash)
        self._validate_value_hash(
            "post-veto times M before scalar",
            self.risk_adjusted_after_veto_times_m_before_scalar_value,
            self.risk_adjusted_after_veto_times_m_before_scalar_hash,
        )
        _require_close(
            "S27 v2 post-veto times M",
            self.risk_adjusted_after_veto_times_m_before_scalar_value,
            self.risk_adjusted_forecast_after_veto_value * self.ewma10_multiplier_m_value,
        )
        if self.scalar_label != FORECAST_SCALAR_LABEL or self.scalar_value != FORECAST_SCALAR_VALUE:
            raise CarverBlocked("S27 v2 forecast executable scalar must preserve book-approximate 20.0 freeze")
        if self.scalar_value_hash != _value_hash("scalar_value", self.scalar_value):
            raise CarverBlocked("S27 v2 forecast executable scalar hash must bind value")
        self._validate_value_hash("capped forecast", self.capped_forecast_value, self.capped_forecast_hash)
        expected_capped = _clamp(
            self.risk_adjusted_after_veto_times_m_before_scalar_value * self.scalar_value,
            -FORECAST_CAP_VALUE,
            FORECAST_CAP_VALUE,
        )
        _require_close("S27 v2 capped forecast", self.capped_forecast_value, expected_capped)
        require_hash("S27 v2 forecast executable row hash", self.row_hash)
        if self.row_hash != canonical_sha256(_forecast_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 forecast executable row hash must be content-bound")

    def _validate_value_hash(self, name: str, value: float, hash_value: str) -> None:
        require_finite_number(f"S27 v2 forecast executable {name}", value)
        require_hash(f"S27 v2 forecast executable {name} hash", hash_value)
        if hash_value != _value_hash(name, value):
            raise CarverBlocked(f"S27 v2 forecast executable {name} hash must bind value")

    def _validate_positive_value_hash(self, name: str, value: float, hash_value: str) -> None:
        require_positive_number(f"S27 v2 forecast executable {name}", value)
        require_hash(f"S27 v2 forecast executable {name} hash", hash_value)
        if hash_value != _value_hash(name, value):
            raise CarverBlocked(f"S27 v2 forecast executable {name} hash must bind value")


@dataclass(frozen=True)
class ForecastExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    runtime_history_bundle: RuntimeHistoryRemediationExecutableBundle
    forecast_row: ForecastExecutableLedgerRow
    unresolved_gate_labels: tuple[str, ...]
    forecast_rows_emitted: bool
    position_rows_emitted: bool
    order_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = FORECAST_EXECUTABLE_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_FORECAST_EXECUTABLE_STATUS:
            raise CarverBlocked("S27 v2 forecast executable status is not locked")
        if self.authorization_label != S27_V2_FORECAST_EXECUTABLE_AUTHORIZATION:
            raise CarverBlocked("S27 v2 forecast executable authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 forecast executable must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 forecast executable must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 forecast executable is locked to the audited remediation pack")
        self.runtime_history_bundle.validate()
        active_runtime = build_runtime_history_executable_ledgers_on_remediation_pack(pack_path)
        if self.runtime_history_bundle != active_runtime:
            raise CarverBlocked("S27 v2 forecast executable must bind active runtime-history bundle")
        self.forecast_row._validate_structural_formula()
        active_row = _build_active_forecast_row(pack_path, active_runtime)
        if self.forecast_row != active_row:
            raise CarverBlocked("S27 v2 forecast executable row must match active local runtime evidence")
        expected_unresolved = (
            BLOCKED_TICK,
            BLOCKED_COST_SCHEMA,
            BLOCKED_WORKING_LIMIT_LIFECYCLE,
            BLOCKED_INITIAL_POSITION,
        )
        require_tuple("S27 v2 forecast executable unresolved gates", self.unresolved_gate_labels)
        if self.unresolved_gate_labels != expected_unresolved:
            raise CarverBlocked("S27 v2 forecast executable unresolved gates must preserve downstream blockers")
        for gate_label in self.unresolved_gate_labels:
            if gate_label not in REQUIRED_UNRESOLVED_GATE_LABELS:
                raise CarverBlocked("S27 v2 forecast executable unresolved gate is not source-locked")
        if self.forecast_rows_emitted is not True:
            raise CarverBlocked("S27 v2 forecast executable must mark forecast rows emitted")
        if any(
            flag is not False
            for flag in (
                self.position_rows_emitted,
                self.order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 forecast executable cannot emit position/order/fill/cost/PnL/result/evidence")
        if self.non_authorizations != FORECAST_EXECUTABLE_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 forecast executable must preserve non-authorizations")
        require_hash("S27 v2 forecast executable bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_forecast_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 forecast executable bundle hash must be content-bound")


def build_forecast_executable_ledgers_on_remediation_pack(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> ForecastExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 forecast executable run is locked to the audited remediation pack")
    runtime_bundle = build_runtime_history_executable_ledgers_on_remediation_pack(pack_path)
    forecast_row = _build_active_forecast_row(pack_path, runtime_bundle)
    bundle = ForecastExecutableBundle(
        status=S27_V2_FORECAST_EXECUTABLE_STATUS,
        authorization_label=S27_V2_FORECAST_EXECUTABLE_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        runtime_history_bundle=runtime_bundle,
        forecast_row=forecast_row,
        unresolved_gate_labels=(
            BLOCKED_TICK,
            BLOCKED_COST_SCHEMA,
            BLOCKED_WORKING_LIMIT_LIFECYCLE,
            BLOCKED_INITIAL_POSITION,
        ),
        forecast_rows_emitted=True,
        position_rows_emitted=False,
        order_rows_emitted=False,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = ForecastExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_forecast_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_forecast_row(
    pack_path: Path,
    runtime_bundle: RuntimeHistoryRemediationExecutableBundle,
) -> ForecastExecutableLedgerRow:
    manifest = _read_manifest(pack_path)
    rows_by_file = _read_rows_by_file(pack_path)
    row_hashes_by_file = _row_hashes_by_file(rows_by_file)
    selected_decision = manifest["selected_decision_timestamp_utc"]
    selected_previous_daily = manifest["selected_previous_daily_timestamp_utc"]
    selected_raw_symbol = manifest["selected_raw_symbol"]
    source_rows = _locked_source_rows(manifest, selected_decision)

    daily_continuous_rows = rows_by_file["daily_continuous_completed_bar.csv"]
    selected_daily_continuous = daily_continuous_rows[0]
    selected_daily_current = rows_by_file["daily_current_contract_completed_bar.csv"][0]
    selected_hourly_decision = rows_by_file["hourly_decision_completed_bar.csv"][0]
    history_evidence = manifest["history_evidence"]
    chronological_daily = tuple(daily_continuous_rows[1:]) + (selected_daily_continuous,)
    ewma5_equilibrium = _recursive_ewma(tuple(_as_float(row["close_price"], "daily continuous close") for row in chronological_daily), EWMA5_SPAN)
    hourly_current = _as_float(selected_hourly_decision["close_price"], "hourly decision close")
    previous_current_close = _as_float(selected_daily_current["close_price"], "daily current close")
    annual_sigma = _as_float(history_evidence["selected_sigma_percent_t"], "selected sigma")
    raw_forecast = ewma5_equilibrium - hourly_current
    sigma_price = previous_current_close * annual_sigma / 16.0
    if sigma_price <= 0.0:
        raise CarverBlocked("S27 v2 forecast executable sigma price must be positive")
    risk_adjusted_before_veto = raw_forecast / sigma_price
    ewmac_trend = _as_float(source_rows["ewmac_runtime_rows"]["trend_forecast"], "EWMAC trend forecast")
    trend_decision, risk_adjusted_after_veto = _trend_veto(risk_adjusted_before_veto, ewmac_trend)
    relative_v = _as_float(history_evidence["selected_vqm_relative_volatility_v"], "V/Q/M relative volatility")
    quantile_q = _as_float(history_evidence["selected_vqm_quantile_q"], "V/Q/M quantile")
    raw_multiplier = 2.0 - (1.5 * quantile_q)
    multiplier_m = _as_float(history_evidence["selected_vqm_multiplier_m"], "V/Q/M multiplier M")
    post_veto_times_m = risk_adjusted_after_veto * multiplier_m
    capped_forecast = _clamp(post_veto_times_m * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)

    row = ForecastExecutableLedgerRow(
        ledger_label="FORECAST_REPLAY_LEDGER",
        row_status=FORECAST_LEDGER_ROW_STATUS,
        reason_code="S26_S27_NUMERIC_FORECAST_CHAIN_BOUND_TO_RUNTIME_EVIDENCE_NOT_POSITION",
        runtime_history_bundle_hash=runtime_bundle.bundle_hash,
        runtime_evidence_bundle_hash=runtime_bundle.runtime_evidence_bundle.bundle_hash,
        level_compatibility_row_hash=runtime_bundle.level_compatibility_row.row_hash,
        runtime_history_row_hash=runtime_bundle.runtime_history_row.row_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=selected_decision,
        selected_previous_daily_timestamp_utc=selected_previous_daily,
        raw_symbol=selected_raw_symbol,
        daily_continuous_row_hash=row_hashes_by_file["daily_continuous_completed_bar.csv"][0],
        daily_current_contract_row_hash=row_hashes_by_file["daily_current_contract_completed_bar.csv"][0],
        hourly_decision_row_hash=row_hashes_by_file["hourly_decision_completed_bar.csv"][0],
        sigma_source_row_hash=_source_row_hash("sigma_runtime_ledger", source_rows["sigma_runtime_ledger"]),
        ewmac_source_row_hash=_source_row_hash("ewmac_runtime_rows", source_rows["ewmac_runtime_rows"]),
        vqm_source_row_hash=_source_row_hash("vqm_runtime_rows", source_rows["vqm_runtime_rows"]),
        ewma5_policy_hash=canonical_sha256(
            {
                "artifact": "S27_V2_EWMA5_EQUILIBRIUM_POLICY",
                "span": EWMA5_SPAN,
                "alpha": 2.0 / (EWMA5_SPAN + 1.0),
                "input_order": "STRICT_PRIOR_CHRONOLOGICAL_DAILY_CONTINUOUS_THEN_SELECTED_PREVIOUS_DAILY",
                "initialization": "FIRST_AVAILABLE_CLOSE",
            }
        ),
        ewma5_equilibrium_value=ewma5_equilibrium,
        ewma5_equilibrium_hash=_value_hash("EWMA5 equilibrium", ewma5_equilibrium),
        hourly_current_price_value=hourly_current,
        hourly_current_price_hash=_value_hash("hourly current price", hourly_current),
        previous_completed_daily_close_current_contract_value=previous_current_close,
        previous_completed_daily_close_current_contract_hash=_value_hash("previous daily current contract close", previous_current_close),
        raw_mean_reversion_forecast_value=raw_forecast,
        raw_mean_reversion_forecast_hash=_value_hash("raw mean-reversion forecast", raw_forecast),
        annual_percentage_sigma_value=annual_sigma,
        annual_percentage_sigma_hash=_value_hash("annual percentage sigma", annual_sigma),
        sigma_price_value=sigma_price,
        sigma_price_hash=_value_hash("sigma price", sigma_price),
        risk_adjusted_forecast_before_veto_value=risk_adjusted_before_veto,
        risk_adjusted_forecast_before_veto_hash=_value_hash("risk-adjusted forecast before veto", risk_adjusted_before_veto),
        ewmac16_64_trend_value=ewmac_trend,
        ewmac16_64_trend_sign=_nonzero_sign("S27 v2 EWMAC16/64 trend value", ewmac_trend),
        ewmac16_64_trend_hash=_value_hash("EWMAC16/64 trend", ewmac_trend),
        trend_veto_decision=trend_decision,
        trend_veto_decision_hash=_value_hash("trend_veto_decision", trend_decision),
        risk_adjusted_forecast_after_veto_value=risk_adjusted_after_veto,
        risk_adjusted_forecast_after_veto_hash=_value_hash("risk-adjusted forecast after veto", risk_adjusted_after_veto),
        relative_volatility_v_value=relative_v,
        relative_volatility_v_hash=_value_hash("relative volatility V", relative_v),
        quantile_q_value=quantile_q,
        quantile_q_hash=_value_hash("quantile Q", quantile_q),
        raw_volatility_multiplier_value=raw_multiplier,
        raw_volatility_multiplier_hash=_value_hash("raw volatility multiplier", raw_multiplier),
        ewma10_multiplier_m_value=multiplier_m,
        ewma10_multiplier_m_hash=_value_hash("EWMA10 multiplier M", multiplier_m),
        risk_adjusted_after_veto_times_m_before_scalar_value=post_veto_times_m,
        risk_adjusted_after_veto_times_m_before_scalar_hash=_value_hash("post-veto times M before scalar", post_veto_times_m),
        scalar_label=FORECAST_SCALAR_LABEL,
        scalar_value=FORECAST_SCALAR_VALUE,
        scalar_value_hash=_value_hash("scalar_value", FORECAST_SCALAR_VALUE),
        capped_forecast_value=capped_forecast,
        capped_forecast_hash=_value_hash("capped forecast", capped_forecast),
        row_hash="0" * 64,
    )
    row = ForecastExecutableLedgerRow(**{**row.__dict__, "row_hash": canonical_sha256(_forecast_row_hash_payload(row))})
    row._validate_structural_formula()
    return row


def _locked_source_rows(manifest: dict[str, Any], selected_decision: str) -> dict[str, dict[str, str]]:
    declared_source_files = manifest.get("source_files")
    if not isinstance(declared_source_files, dict) or set(declared_source_files) != set(REMEDIATION_SOURCE_FILES):
        raise CarverBlocked("S27 v2 forecast executable source files must match locked remediation set")
    source_rows: dict[str, dict[str, str]] = {}
    for label in ("sigma_runtime_ledger", "ewmac_runtime_rows", "vqm_runtime_rows"):
        expected_relative_path = REMEDIATION_SOURCE_FILES[label]
        declared = declared_source_files[label]
        if declared["path"].replace("\\", "/") != expected_relative_path.as_posix():
            raise CarverBlocked("S27 v2 forecast executable source path must bind locked remediation source")
        observed_hash = sha256((_REPO_ROOT / expected_relative_path).read_bytes()).hexdigest()
        if observed_hash != declared["sha256"].lower():
            raise CarverBlocked("S27 v2 forecast executable source hash must match local bytes")
        source_rows[label] = _row_by_value(_read_csv_rows(_REPO_ROOT / expected_relative_path), "as_of", selected_decision)
    if source_rows["sigma_runtime_ledger"]["runtime_status"] != "PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 forecast executable sigma source status is not locked")
    if source_rows["ewmac_runtime_rows"]["runtime_status"] != "PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 forecast executable EWMAC source status is not locked")
    if source_rows["vqm_runtime_rows"]["runtime_status"] != "PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 forecast executable V/Q/M source status is not locked")
    for label, row in source_rows.items():
        if row["no_lookahead_status"] != "PASS_NO_LOOKAHEAD":
            raise CarverBlocked(f"S27 v2 forecast executable {label} source must be no-lookahead")
    return source_rows


def _read_manifest(pack_path: Path) -> dict[str, Any]:
    manifest_path = pack_path / "S27_V2_RUNTIME_EVIDENCE_REMEDIATION_DECLARED_INPUT_PACK_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise CarverBlocked("S27 v2 forecast executable manifest must be a JSON object")
    history_evidence = manifest.get("history_evidence")
    if not isinstance(history_evidence, dict):
        raise CarverBlocked("S27 v2 forecast executable history evidence is unresolved")
    return manifest


def _read_rows_by_file(pack_path: Path) -> dict[str, tuple[dict[str, str], ...]]:
    filenames = (
        "daily_continuous_completed_bar.csv",
        "daily_current_contract_completed_bar.csv",
        "hourly_decision_completed_bar.csv",
        "hourly_fill_completed_bar.csv",
        "session_calendar.csv",
        "roll_calendar.csv",
        "cost_parameter.csv",
    )
    return {filename: tuple(_read_csv_rows(pack_path / filename)) for filename in filenames}


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise CarverBlocked(f"S27 v2 forecast executable file {path.name} has no rows")
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
        raise CarverBlocked(f"S27 v2 forecast executable source row must have exactly one {column}={value}")
    return matches[0]


def _source_row_hash(label: str, row: dict[str, str]) -> str:
    return canonical_sha256({"artifact": "S27_V2_FORECAST_EXECUTABLE_LOCKED_SOURCE_ROW", "label": label, "row": row})


def _as_float(value: str, label: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CarverBlocked(f"S27 v2 forecast executable {label} must be numeric") from exc
    require_finite_number(f"S27 v2 forecast executable {label}", parsed)
    return parsed


def _recursive_ewma(values: tuple[float, ...], span: int) -> float:
    if len(values) < span:
        raise CarverBlocked("S27 v2 forecast executable EWMA history is insufficient")
    alpha = 2.0 / (span + 1.0)
    smoothed = values[0]
    require_positive_number("S27 v2 forecast executable EWMA input", smoothed)
    for value in values[1:]:
        require_positive_number("S27 v2 forecast executable EWMA input", value)
        smoothed = alpha * value + (1.0 - alpha) * smoothed
    require_positive_number("S27 v2 forecast executable EWMA output", smoothed)
    return smoothed


def _trend_veto(risk_adjusted_forecast: float, trend_forecast: float) -> tuple[str, float]:
    require_finite_number("S27 v2 forecast executable risk-adjusted forecast", risk_adjusted_forecast)
    _nonzero_sign("S27 v2 forecast executable trend forecast", trend_forecast)
    if isclose(risk_adjusted_forecast, 0.0, rel_tol=0.0, abs_tol=1e-12):
        return "FLAT_AT_EQUILIBRIUM", 0.0
    if risk_adjusted_forecast * trend_forecast < 0.0:
        return "ZERO_FORECAST_BY_TREND_VETO", 0.0
    return "PERMIT_MEAN_REVERSION", risk_adjusted_forecast


def _nonzero_sign(name: str, value: float) -> str:
    require_finite_number(name, value)
    if isclose(value, 0.0, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked(f"{name} must be nonzero until a zero-policy is source-locked")
    return "POSITIVE" if value > 0.0 else "NEGATIVE"


def _clamp(value: float, lower: float, upper: float) -> float:
    require_finite_number("S27 v2 forecast executable clamp input", value)
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value


def _require_close(name: str, observed: float, expected: float) -> None:
    if not isclose(observed, expected, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked(f"{name} must bind source formula")


def _value_hash(label: str, value: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_FORECAST_EXECUTABLE_VALUE", "label": label, "value": value})


def _forecast_row_hash_payload(row: ForecastExecutableLedgerRow) -> dict[str, object]:
    return {
        "annual_percentage_sigma_hash": row.annual_percentage_sigma_hash,
        "annual_percentage_sigma_value": row.annual_percentage_sigma_value,
        "capped_forecast_hash": row.capped_forecast_hash,
        "capped_forecast_value": row.capped_forecast_value,
        "daily_continuous_row_hash": row.daily_continuous_row_hash,
        "daily_current_contract_row_hash": row.daily_current_contract_row_hash,
        "ewma10_multiplier_m_hash": row.ewma10_multiplier_m_hash,
        "ewma10_multiplier_m_value": row.ewma10_multiplier_m_value,
        "ewma5_equilibrium_hash": row.ewma5_equilibrium_hash,
        "ewma5_equilibrium_value": row.ewma5_equilibrium_value,
        "ewma5_policy_hash": row.ewma5_policy_hash,
        "ewmac16_64_trend_hash": row.ewmac16_64_trend_hash,
        "ewmac16_64_trend_sign": row.ewmac16_64_trend_sign,
        "ewmac16_64_trend_value": row.ewmac16_64_trend_value,
        "ewmac_source_row_hash": row.ewmac_source_row_hash,
        "hourly_current_price_hash": row.hourly_current_price_hash,
        "hourly_current_price_value": row.hourly_current_price_value,
        "hourly_decision_row_hash": row.hourly_decision_row_hash,
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "level_compatibility_row_hash": row.level_compatibility_row_hash,
        "previous_completed_daily_close_current_contract_hash": row.previous_completed_daily_close_current_contract_hash,
        "previous_completed_daily_close_current_contract_value": row.previous_completed_daily_close_current_contract_value,
        "quantile_q_hash": row.quantile_q_hash,
        "quantile_q_value": row.quantile_q_value,
        "raw_mean_reversion_forecast_hash": row.raw_mean_reversion_forecast_hash,
        "raw_mean_reversion_forecast_value": row.raw_mean_reversion_forecast_value,
        "raw_symbol": row.raw_symbol,
        "raw_volatility_multiplier_hash": row.raw_volatility_multiplier_hash,
        "raw_volatility_multiplier_value": row.raw_volatility_multiplier_value,
        "reason_code": row.reason_code,
        "relative_volatility_v_hash": row.relative_volatility_v_hash,
        "relative_volatility_v_value": row.relative_volatility_v_value,
        "risk_adjusted_after_veto_times_m_before_scalar_hash": row.risk_adjusted_after_veto_times_m_before_scalar_hash,
        "risk_adjusted_after_veto_times_m_before_scalar_value": row.risk_adjusted_after_veto_times_m_before_scalar_value,
        "risk_adjusted_forecast_after_veto_hash": row.risk_adjusted_forecast_after_veto_hash,
        "risk_adjusted_forecast_after_veto_value": row.risk_adjusted_forecast_after_veto_value,
        "risk_adjusted_forecast_before_veto_hash": row.risk_adjusted_forecast_before_veto_hash,
        "risk_adjusted_forecast_before_veto_value": row.risk_adjusted_forecast_before_veto_value,
        "row_status": row.row_status,
        "runtime_evidence_bundle_hash": row.runtime_evidence_bundle_hash,
        "runtime_history_bundle_hash": row.runtime_history_bundle_hash,
        "runtime_history_row_hash": row.runtime_history_row_hash,
        "scalar_label": row.scalar_label,
        "scalar_value": row.scalar_value,
        "scalar_value_hash": row.scalar_value_hash,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "selected_previous_daily_timestamp_utc": row.selected_previous_daily_timestamp_utc,
        "sigma_price_hash": row.sigma_price_hash,
        "sigma_price_value": row.sigma_price_value,
        "sigma_source_row_hash": row.sigma_source_row_hash,
        "trend_veto_decision": row.trend_veto_decision,
        "trend_veto_decision_hash": row.trend_veto_decision_hash,
        "vqm_source_row_hash": row.vqm_source_row_hash,
    }


def _forecast_bundle_hash_payload(bundle: ForecastExecutableBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_FORECAST_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "fill_rows_emitted": bundle.fill_rows_emitted,
        "forecast_row_hash": bundle.forecast_row.row_hash,
        "forecast_rows_emitted": bundle.forecast_rows_emitted,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "order_rows_emitted": bundle.order_rows_emitted,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "position_rows_emitted": bundle.position_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "runtime_history_bundle_hash": bundle.runtime_history_bundle.bundle_hash,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "unresolved_gate_labels": bundle.unresolved_gate_labels,
    }

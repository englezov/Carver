from __future__ import annotations

import csv
from io import StringIO
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from math import isfinite
from numbers import Real

from .m0 import LaneClass, SourceRuleStatus, CarverBlocked, require_finite_positive, require_non_empty_text, require_source_native
from .m1 import RoundingPolicy, TimedValue
from .m2 import FORECAST_CAP, cap_forecast


S26_EQUILIBRIUM_EWMA_SPAN = 5
S26_FORECAST_SCALAR = 9.3
S27_FORECAST_SCALAR = 20.0
S27_TREND_FAST_SPAN = 16
S27_TREND_SLOW_SPAN = 64
S27_VOL_ATTENUATION_SPAN = 10
S26_ZN_WORKED_EXAMPLE_ROW_ID = "APPENDIX_C_172_004"
S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE = "ZN"
S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID = 42000661
S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL = "ZNM6"
S26_FORECAST_ONLY_STATUS = "S26_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION"
S26_ZN_HOURLY_QUARANTINE_STATUS = "QUARANTINE_ONLY_NOT_FORECAST_READY"
S26_ZN_FORECAST_INPUT_STATUS = "S26_FORECAST_INPUT_READY_QUARANTINE_ONLY"
S26_ZN_SIGMA_RUNTIME_STATUS = "PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE"
S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS = "PREVALIDATED_S26_DAILY_BACK_ADJUSTED_EWMA5_EQUILIBRIUM_RUNTIME_VALUE"
S26_DAILY_EQUILIBRIUM_METHOD_STATUS = "LOCKED_DAILY_BACK_ADJUSTED_EWMA5_EQUILIBRIUM_RUNTIME"
S26_ZN_FORECAST_HANDOFF_STATUS = "PASS_G_R1B_S26_ZN_HOURLY_FORECAST_OUTPUT_ONLY"
S26_ZN_FORECAST_SERIES_STATUS = "PASS_G_R1C_S26_ZN_HOURLY_FORECAST_SERIES_ONLY"
S26_EXECUTION_SEMANTICS_SOURCE_LOCK_STATUS = "PASS_S26_EXECUTION_SEMANTICS_SOURCE_LOCK_DESIGN_ONLY_NOT_TEST_NOT_BACKTEST"
S27_FORECAST_ONLY_STATUS = "S27_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION"
S27_TREND_RUNTIME_STATUS = "PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE"
S27_VOL_ATTENUATION_RUNTIME_STATUS = "PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE"
S27_DAILY_TREND_METHOD_STATUS = "LOCKED_DAILY_EWMAC16_64_TREND_OVERLAY_RUNTIME"
S27_DAILY_VOL_ATTENUATION_METHOD_STATUS = "LOCKED_DAILY_S13_TEN_YEAR_V_Q_M_ATTENUATION_RUNTIME"
S27_FORECAST_HANDOFF_STATUS = "PASS_S27_REAL_HOURLY_FORECAST_ONLY_HANDOFF_PLUMBING"
S27_FORECAST_SERIES_STATUS = "PASS_S27_REAL_HOURLY_FORECAST_SERIES_ONLY_HANDOFF_PLUMBING"
S27_TREND_RUNTIME_LEDGER_STATUS = "PASS_S27_EWMAC16_TREND_RUNTIME_LEDGER_PLUMBING_PREVALIDATED_ONLY"
S27_VOL_ATTENUATION_RUNTIME_LEDGER_STATUS = "PASS_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_LEDGER_PLUMBING_PREVALIDATED_ONLY"
S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_STATUS = (
    "PASS_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_NOT_BACKTEST"
)
S27_STALE_BACKTEST_EXECUTABLES_STATUS = "FAIL_CLOSED_STALE_S27_EXECUTABLES_PENDING_DAILY_RUNTIME_CONVERSION"
S27_ZN_BACKTEST_READINESS_GATE_STATUS = "PASS_S27_ZN_SINGLE_INSTRUMENT_BACKTEST_READINESS_GATE_NOT_BACKTEST"
S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_STATUS = (
    "PROCESS_ONLY_S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_NOT_DATA_AUTHORIZATION"
)
S27_ZN_DESIRED_POSITION_PLUMBING_STATUS = "PASS_S27_ZN_DESIRED_POSITION_PLUMBING_PREVALIDATED_NOT_BACKTEST"
S26_ZN_DATABENTO_PROVIDER = "DATABENTO_HISTORICAL"
S26_ZN_DATABENTO_DATASET = "GLBX.MDP3"
S26_ZN_DATABENTO_SCHEMA = "ohlcv-1h"
S26_ZN_DATABENTO_STYPE_IN = "instrument_id"
S26_ZN_HOURLY_REQUEST_MANIFEST_STATUS = "PROCESS_ONLY_REQUEST_MANIFEST_NOT_AUTHORIZATION"
S26_ZN_HOURLY_REQUEST_START_UTC = datetime(2026, 5, 17, tzinfo=timezone.utc)
S26_ZN_HOURLY_REQUEST_END_UTC = datetime(2026, 5, 23, tzinfo=timezone.utc)
S26_ZN_TARGET_COMPLETED_TRADING_DATES = (
    "2026-05-18",
    "2026-05-19",
    "2026-05-20",
    "2026-05-21",
    "2026-05-22",
)
S26_ZN_HOURLY_REQUEST_OUTPUT_ROOT = (
    "docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/"
    "2026-05-18_2026-05-22/databento_ohlcv_1h_quarantine/"
)
S26_ZN_EXTENDED_HOURLY_REQUEST_MANIFEST_STATUS = "PROCESS_ONLY_EXTENDED_FORECAST_ONLY_COVERAGE_MANIFEST_NOT_AUTHORIZATION"
S26_ZN_EXTENDED_HOURLY_REQUEST_START_UTC = datetime(2026, 4, 12, tzinfo=timezone.utc)
S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC = datetime(2026, 5, 23, tzinfo=timezone.utc)
S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES = tuple(
    (datetime(2026, 4, 13, tzinfo=timezone.utc) + timedelta(days=offset)).date().isoformat()
    for offset in range(40)
    if (datetime(2026, 4, 13, tzinfo=timezone.utc) + timedelta(days=offset)).weekday() < 5
)
S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT = (
    "docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/"
    "2026-04-13_2026-05-22/databento_ohlcv_1h_extended_forecast_only_quarantine/"
)
S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START = "2022-01-01"
S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END = "2023-12-31"
S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_START_UTC = datetime(2021, 12, 31, tzinfo=timezone.utc)
S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_END_UTC = datetime(2024, 1, 1, tzinfo=timezone.utc)
S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS = (
    "ZNH2",
    "ZNM2",
    "ZNU2",
    "ZNZ2",
    "ZNH3",
    "ZNM3",
    "ZNU3",
    "ZNZ3",
    "ZNH4",
)
S27_ZN_BACKTEST_HOURLY_ARCHIVE_OUTPUT_ROOT = (
    "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/"
    "2022-01-01_2023-12-31/hourly_archive_quarantine/"
)
S26_ZN_DATABENTO_OHLCV_1H_REQUIRED_COLUMNS = (
    "ts_event",
    "instrument_id",
    "raw_symbol",
    "open",
    "high",
    "low",
    "close",
    "volume",
)


@dataclass(frozen=True)
class SyntheticHourlyPrice:
    label: str
    timestamp: datetime
    price: float

    def validate(self) -> None:
        require_non_empty_text("synthetic hourly price label", self.label)
        if not self.label.startswith("synthetic_"):
            raise CarverBlocked("S26/S27 hourly price label must be synthetic")
        _validate_hourly_timestamp(self.timestamp)
        require_finite_positive("synthetic hourly price", self.price)


@dataclass(frozen=True)
class SyntheticQuantilePoint:
    label: str
    timestamp: datetime
    quantile: float

    def validate(self) -> None:
        require_non_empty_text("synthetic quantile label", self.label)
        if not self.label.startswith("synthetic_"):
            raise CarverBlocked("S27 volatility quantile label must be synthetic")
        _validate_hourly_timestamp(self.timestamp)
        _require_finite("S27 volatility quantile", self.quantile)
        if self.quantile < 0.0 or self.quantile > 1.0:
            raise CarverBlocked("S27 volatility quantile must be in [0, 1]")


@dataclass(frozen=True)
class S26SourceLocks:
    hourly_price_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    equilibrium_span_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    sigma_price_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    scalar_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    cap_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    no_fdm_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    no_buffering_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    output_boundary_status: SourceRuleStatus = SourceRuleStatus.LOCKED

    def validate(self) -> None:
        for name, status in (
            ("hourly price input", self.hourly_price_status),
            ("EWMA(5) equilibrium span", self.equilibrium_span_status),
            ("sigma price relation", self.sigma_price_status),
            ("forecast scalar 9.3", self.scalar_status),
            ("forecast cap", self.cap_status),
            ("no FDM rule", self.no_fdm_status),
            ("no buffering rule", self.no_buffering_status),
            ("S26 output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"S26 {name} source is unresolved")


@dataclass(frozen=True)
class S26QuarantinedHourlySourceLocks:
    hourly_intake_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    session_mapping_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    provider_condition_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    sigma_percent_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    forecast_output_boundary_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    no_diagnostics_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    no_backtests_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    no_positions_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED

    def validate(self) -> None:
        for name, status in (
            ("ZN hourly Databento intake", self.hourly_intake_status),
            ("ZN hourly session mapping", self.session_mapping_status),
            ("ZN provider-condition policy", self.provider_condition_status),
            ("S26 sigma percent method", self.sigma_percent_status),
            ("S26 forecast-only output boundary", self.forecast_output_boundary_status),
            ("no diagnostics boundary", self.no_diagnostics_status),
            ("no backtests boundary", self.no_backtests_status),
            ("no positions boundary", self.no_positions_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"S26 real-hourly {name} source is unresolved")


@dataclass(frozen=True)
class S26DatabentoHourlyIntakeRequestManifest:
    status: str
    provider: str
    dataset: str
    schema: str
    stype_in: str
    symbols: tuple[int, ...]
    row_id: str
    author_market_code: str
    expected_raw_symbol: str
    request_start_utc: datetime
    request_end_utc: datetime
    target_completed_trading_dates: tuple[str, ...]
    continuous_contracts_status: str
    parent_symbols_status: str
    raw_symbol_selector_status: str
    output_root: str
    no_authorization: tuple[str, ...]

    def validate(self) -> None:
        _require_exact("S26 ZN request manifest status", self.status, S26_ZN_HOURLY_REQUEST_MANIFEST_STATUS)
        _require_exact("S26 ZN request provider", self.provider, S26_ZN_DATABENTO_PROVIDER)
        _require_exact("S26 ZN request dataset", self.dataset, S26_ZN_DATABENTO_DATASET)
        _require_exact("S26 ZN request schema", self.schema, S26_ZN_DATABENTO_SCHEMA)
        _require_exact("S26 ZN request stype_in", self.stype_in, S26_ZN_DATABENTO_STYPE_IN)
        if self.symbols != (S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,):
            raise CarverBlocked("S26 ZN request manifest must use only instrument_id 42000661")
        _require_exact("S26 ZN request row id", self.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        _require_exact("S26 ZN request author market code", self.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
        _require_exact("S26 ZN request expected raw symbol", self.expected_raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
        _require_exact_datetime(
            "S26 ZN request start UTC",
            self.request_start_utc,
            S26_ZN_HOURLY_REQUEST_START_UTC,
        )
        _require_exact_datetime("S26 ZN request end UTC", self.request_end_utc, S26_ZN_HOURLY_REQUEST_END_UTC)
        if self.target_completed_trading_dates != S26_ZN_TARGET_COMPLETED_TRADING_DATES:
            raise CarverBlocked("S26 ZN request target completed trading dates are not locked")
        _require_exact("S26 ZN continuous contract selector", self.continuous_contracts_status, "CLOSED")
        _require_exact("S26 ZN parent symbol selector", self.parent_symbols_status, "CLOSED")
        _require_exact("S26 ZN raw symbol selector", self.raw_symbol_selector_status, "CLOSED_CROSS_CHECK_ONLY")
        _require_exact("S26 ZN request output root", self.output_root, S26_ZN_HOURLY_REQUEST_OUTPUT_ROOT)
        _validate_no_authorization_manifest(self.no_authorization)


@dataclass(frozen=True)
class S26ExtendedHourlyForecastOnlyCoverageManifest:
    status: str
    provider: str
    dataset: str
    schema: str
    stype_in: str
    symbols: tuple[int, ...]
    row_id: str
    author_market_code: str
    expected_raw_symbol: str
    request_start_utc: datetime
    request_end_utc: datetime
    target_completed_trading_dates: tuple[str, ...]
    extended_window_purpose: str
    sigma_runtime_requirement: str
    output_boundary_status: str
    continuous_contracts_status: str
    parent_symbols_status: str
    raw_symbol_selector_status: str
    output_root: str
    no_authorization: tuple[str, ...]

    def validate(self) -> None:
        _require_exact("S26 ZN extended manifest status", self.status, S26_ZN_EXTENDED_HOURLY_REQUEST_MANIFEST_STATUS)
        _require_exact("S26 ZN extended provider", self.provider, S26_ZN_DATABENTO_PROVIDER)
        _require_exact("S26 ZN extended dataset", self.dataset, S26_ZN_DATABENTO_DATASET)
        _require_exact("S26 ZN extended schema", self.schema, S26_ZN_DATABENTO_SCHEMA)
        _require_exact("S26 ZN extended stype_in", self.stype_in, S26_ZN_DATABENTO_STYPE_IN)
        if self.symbols != (S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,):
            raise CarverBlocked("S26 ZN extended manifest must use only instrument_id 42000661")
        _require_exact("S26 ZN extended row id", self.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        _require_exact("S26 ZN extended author market code", self.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
        _require_exact("S26 ZN extended expected raw symbol", self.expected_raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
        _require_exact_datetime("S26 ZN extended request start UTC", self.request_start_utc, S26_ZN_EXTENDED_HOURLY_REQUEST_START_UTC)
        _require_exact_datetime("S26 ZN extended request end UTC", self.request_end_utc, S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC)
        if self.target_completed_trading_dates != S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES:
            raise CarverBlocked("S26 ZN extended target completed trading dates are not locked")
        if not set(S26_ZN_TARGET_COMPLETED_TRADING_DATES).issubset(set(self.target_completed_trading_dates)):
            raise CarverBlocked("S26 ZN extended target dates must preserve the original G_R1A target dates")
        _require_exact(
            "S26 ZN extended window purpose",
            self.extended_window_purpose,
            "EXPAND_S26_FORECAST_ONLY_COVERAGE_BEFORE_S27_TEST_GATE",
        )
        _require_exact(
            "S26 ZN extended sigma runtime requirement",
            self.sigma_runtime_requirement,
            "ONE_PREVALIDATED_NO_LOOKAHEAD_SIGMA_RUNTIME_PER_FORECAST_ROW_REQUIRED",
        )
        _require_exact(
            "S26 ZN extended output boundary",
            self.output_boundary_status,
            "FORECAST_ONLY_NO_DIAGNOSTIC_NO_BACKTEST_NO_POSITION",
        )
        _require_exact("S26 ZN extended continuous contract selector", self.continuous_contracts_status, "CLOSED")
        _require_exact("S26 ZN extended parent symbol selector", self.parent_symbols_status, "CLOSED")
        _require_exact("S26 ZN extended raw symbol selector", self.raw_symbol_selector_status, "CLOSED_CROSS_CHECK_ONLY")
        _require_exact("S26 ZN extended output root", self.output_root, S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT)
        _validate_no_authorization_manifest(self.no_authorization)


@dataclass(frozen=True)
class S26DatabentoHourlyOHLCVRawRow:
    provider: str
    dataset: str
    schema: str
    stype_in: str
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    provider_ts_event_start_utc: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    source_raw_sha256: str
    provider_condition_status: str = "PROVIDER_CONDITION_UNRESOLVED"

    def validate(self, manifest: S26DatabentoHourlyIntakeRequestManifest) -> None:
        manifest.validate()
        _require_exact("S26 raw row provider", self.provider, S26_ZN_DATABENTO_PROVIDER)
        _require_exact("S26 raw row dataset", self.dataset, S26_ZN_DATABENTO_DATASET)
        _require_exact("S26 raw row schema", self.schema, S26_ZN_DATABENTO_SCHEMA)
        _require_exact("S26 raw row stype_in", self.stype_in, S26_ZN_DATABENTO_STYPE_IN)
        _require_exact("S26 raw row id", self.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        _require_exact("S26 raw row author market code", self.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
        if self.instrument_id != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
            raise CarverBlocked("S26 raw row must use Databento instrument_id 42000661")
        _require_exact("S26 raw row symbol", self.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
        _validate_real_hourly_timestamp("S26 raw row ts_event start", self.provider_ts_event_start_utc)
        if self.provider_ts_event_start_utc < manifest.request_start_utc or self.provider_ts_event_start_utc >= manifest.request_end_utc:
            raise CarverBlocked("S26 raw row timestamp is outside the locked request envelope")
        _validate_ohlcv_shape(self.open, self.high, self.low, self.close, self.volume)
        _require_sha256_text("S26 raw row source sha256", self.source_raw_sha256)
        require_non_empty_text("S26 raw row provider condition status", self.provider_condition_status)


@dataclass(frozen=True)
class S26QuarantinedHourlyOHLCVBar:
    lane_class: LaneClass
    strategy_context: str
    provider: str
    dataset: str
    schema: str
    stype_in: str
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    provider_ts_event_start_utc: datetime
    derived_completed_bar_end_utc: datetime
    completed_trading_date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    provider_condition_status: str
    row_shape_status: str
    source_raw_sha256: str
    strategy_use_status: str

    def to_forecast_bar(self) -> S26QuarantinedHourlyZNBar:
        return S26QuarantinedHourlyZNBar(
            row_id=self.row_id,
            author_market_code=self.author_market_code,
            instrument_id=self.instrument_id,
            raw_symbol=self.raw_symbol,
            provider_ts_event_start_utc=self.provider_ts_event_start_utc,
            derived_completed_bar_end_utc=self.derived_completed_bar_end_utc,
            completed_trading_date=self.completed_trading_date,
            close=self.close,
            strategy_use_status=self.strategy_use_status,
        )


@dataclass(frozen=True)
class S26SigmaPercentRuntimeValue:
    value: float
    as_of: datetime
    runtime_status: str
    method_status: str
    no_lookahead_status: str
    source_artifact_sha256: str
    source_window_status: str

    def validate(self, forecast_as_of: datetime) -> TimedValue:
        require_finite_positive("S26 ZN sigma percent runtime value", self.value)
        _require_exact_datetime("S26 ZN sigma runtime as_of", self.as_of, forecast_as_of)
        _require_exact("S26 ZN sigma runtime status", self.runtime_status, S26_ZN_SIGMA_RUNTIME_STATUS)
        _require_exact("S26 ZN sigma method status", self.method_status, "LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY")
        _require_exact("S26 ZN sigma no-lookahead status", self.no_lookahead_status, "PASS_NO_LOOKAHEAD")
        _require_exact("S26 ZN sigma source window status", self.source_window_status, "PASS_SOURCE_WINDOW_PREVALIDATED")
        _require_sha256_text("S26 ZN sigma source artifact sha256", self.source_artifact_sha256)
        return TimedValue(self.value, self.as_of)


@dataclass(frozen=True)
class S26ExecutionSemanticsSourceLock:
    hourly_completed_bar_policy: str
    forecast_availability_policy: str
    limit_order_semantics_policy: str
    no_buffering_policy: str
    no_market_order_cost_assumption_policy: str
    execution_cadence_policy: str
    position_sizing_status: str
    cost_model_status: str
    test_boundary_status: str
    source_lock_status: str = S26_EXECUTION_SEMANTICS_SOURCE_LOCK_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()
    order_outputs: tuple[str, ...] = ()
    fill_outputs: tuple[str, ...] = ()
    cost_outputs: tuple[str, ...] = ()

    def validate(self) -> None:
        _require_exact("S26 execution semantics lock status", self.source_lock_status, S26_EXECUTION_SEMANTICS_SOURCE_LOCK_STATUS)
        _require_exact("S26 completed-bar policy", self.hourly_completed_bar_policy, "HOURLY_COMPLETED_BAR_ONLY")
        _require_exact(
            "S26 forecast availability policy",
            self.forecast_availability_policy,
            "FORECAST_AVAILABLE_AFTER_DERIVED_COMPLETED_BAR_END_UTC",
        )
        _require_exact(
            "S26 limit-order semantics policy",
            self.limit_order_semantics_policy,
            "LIMIT_ORDER_STYLE_SEMANTICS_ONLY_NOT_MARKET_ORDER_FILL_MODEL",
        )
        _require_exact("S26 no-buffering policy", self.no_buffering_policy, "NO_BUFFERING_USED")
        _require_exact(
            "S26 no-market-order-cost-assumption policy",
            self.no_market_order_cost_assumption_policy,
            "NO_MARKET_ORDER_COST_ASSUMPTION",
        )
        _require_exact(
            "S26 execution cadence policy",
            self.execution_cadence_policy,
            "SOURCE_FAITHFUL_HOURLY_CADENCE_NO_INTRABAR_LOOKAHEAD",
        )
        _require_exact(
            "S26 position sizing status",
            self.position_sizing_status,
            "POSITION_SIZING_CLOSED_SEPARATE_GATE_REQUIRED",
        )
        _require_exact("S26 cost model status", self.cost_model_status, "COST_MODEL_CLOSED_SEPARATE_GATE_REQUIRED")
        _require_exact(
            "S26 test boundary status",
            self.test_boundary_status,
            "NOT_TEST_NOT_BACKTEST_NOT_DIAGNOSTIC",
        )
        if (
            self.diagnostics_outputs
            or self.backtest_outputs
            or self.position_outputs
            or self.order_outputs
            or self.fill_outputs
            or self.cost_outputs
        ):
            raise CarverBlocked("S26 execution semantics source lock must not emit diagnostics, backtests, positions, orders, fills, or costs")


@dataclass(frozen=True)
class S27ZNPositionExecutionCostSemanticsLock:
    sizing_formula_policy: str
    target_risk_policy: str
    single_instrument_context_policy: str
    annual_risk_estimate_policy: str
    multiplier_fx_policy: str
    forecast_to_position_policy: str
    rounding_policy_status: str
    execution_policy: str
    cost_model_policy: str
    test_boundary_status: str
    source_lock_status: str = S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    return_outputs: tuple[str, ...] = ()
    pnl_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()
    order_outputs: tuple[str, ...] = ()
    fill_outputs: tuple[str, ...] = ()
    cost_outputs: tuple[str, ...] = ()

    def validate(self) -> None:
        _require_exact(
            "S27 ZN position/execution/cost semantics lock status",
            self.source_lock_status,
            S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_STATUS,
        )
        _require_exact(
            "S27 ZN sizing formula policy",
            self.sizing_formula_policy,
            "USE_M1_SIZE_CONTRACTS_BASE_POSITION_THEN_CAPPED_FORECAST_OVER_10",
        )
        _require_exact(
            "S27 ZN target risk policy",
            self.target_risk_policy,
            "ANNUAL_TARGET_RISK_20_PERCENT_BOOK_DEFAULT_LOCK_REQUIRED_AT_TEST_GATE",
        )
        _require_exact(
            "S27 ZN single-instrument context policy",
            self.single_instrument_context_policy,
            "SINGLE_INSTRUMENT_ZN_STANDALONE_DEV_RECON_WEIGHT_1_IDM_1",
        )
        _require_exact(
            "S27 ZN annual risk estimate policy",
            self.annual_risk_estimate_policy,
            "PREVALIDATED_S03_ANNUAL_PERCENTAGE_RISK_REQUIRED_NO_LOOKAHEAD",
        )
        _require_exact(
            "S27 ZN multiplier and FX policy",
            self.multiplier_fx_policy,
            "ZN_CONTRACT_MULTIPLIER_AND_USD_FX_LOCK_REQUIRED_BEFORE_POSITION_OUTPUT",
        )
        _require_exact(
            "S27 ZN forecast-to-position policy",
            self.forecast_to_position_policy,
            "FINAL_CAPPED_FORECAST_DIVIDED_BY_10_MULTIPLIES_BASE_POSITION",
        )
        _require_exact(
            "S27 ZN rounding policy status",
            self.rounding_policy_status,
            "ROUNDING_POLICY_MUST_BE_LOCKED_BEFORE_POSITION_OUTPUT",
        )
        _require_exact(
            "S27 ZN execution policy",
            self.execution_policy,
            "HOURLY_COMPLETED_BAR_NEXT_BAR_LIMIT_STYLE_NO_BUFFERING_NO_INTRABAR_LOOKAHEAD",
        )
        _require_exact(
            "S27 ZN cost model policy",
            self.cost_model_policy,
            "COMMISSION_ONLY_DEV_RECON_ALLOWED_SPREAD_AND_MARKET_ORDER_COSTS_UNRESOLVED_FAIL_CLOSED",
        )
        _require_exact(
            "S27 ZN strategy test boundary",
            self.test_boundary_status,
            "READINESS_ONLY_NOT_BACKTEST_NOT_DIAGNOSTIC_NOT_POSITION",
        )
        if (
            self.diagnostics_outputs
            or self.backtest_outputs
            or self.return_outputs
            or self.pnl_outputs
            or self.position_outputs
            or self.order_outputs
            or self.fill_outputs
            or self.cost_outputs
        ):
            raise CarverBlocked("S27 ZN readiness semantics lock must not emit diagnostics, backtests, returns, PnL, positions, orders, fills, or costs")


@dataclass(frozen=True)
class S27ZNBacktestHourlyArchiveWindowManifest:
    status: str
    provider: str
    dataset: str
    schema: str
    stype_in: str
    row_id: str
    author_market_code: str
    target_completed_trading_date_start: str
    target_completed_trading_date_end: str
    request_start_utc: datetime
    request_end_utc: datetime
    required_raw_symbols: tuple[str, ...]
    local_continuous_policy: str
    provider_condition_policy: str
    output_root: str
    no_authorization: tuple[str, ...]

    def validate(self) -> None:
        _require_exact("S27 ZN archive manifest status", self.status, S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_STATUS)
        _require_exact("S27 ZN archive provider", self.provider, S26_ZN_DATABENTO_PROVIDER)
        _require_exact("S27 ZN archive dataset", self.dataset, S26_ZN_DATABENTO_DATASET)
        _require_exact("S27 ZN archive schema", self.schema, S26_ZN_DATABENTO_SCHEMA)
        _require_exact("S27 ZN archive stype_in", self.stype_in, "raw_symbol")
        _require_exact("S27 ZN archive row id", self.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        _require_exact("S27 ZN archive author market code", self.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
        _require_exact(
            "S27 ZN target completed trading-date start",
            self.target_completed_trading_date_start,
            S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START,
        )
        _require_exact(
            "S27 ZN target completed trading-date end",
            self.target_completed_trading_date_end,
            S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END,
        )
        _require_exact_datetime(
            "S27 ZN archive request start UTC",
            self.request_start_utc,
            S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_START_UTC,
        )
        _require_exact_datetime(
            "S27 ZN archive request end UTC",
            self.request_end_utc,
            S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_END_UTC,
        )
        if self.required_raw_symbols != S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS:
            raise CarverBlocked("S27 ZN archive manifest raw-symbol chain drifted")
        _require_exact(
            "S27 ZN local continuous policy",
            self.local_continuous_policy,
            "LOCAL_DATED_CONTRACT_CHAIN_REQUIRED_NO_PROVIDER_CONTINUOUS_FALLBACK",
        )
        _require_exact(
            "S27 ZN provider condition policy",
            self.provider_condition_policy,
            "PROVIDER_CONDITION_AVAILABLE_ONLY_ZERO_SILENT_ROW_SKIP",
        )
        _require_exact("S27 ZN archive output root", self.output_root, S27_ZN_BACKTEST_HOURLY_ARCHIVE_OUTPUT_ROOT)
        _validate_no_authorization_manifest(self.no_authorization)


@dataclass(frozen=True)
class S27ZNSingleInstrumentBacktestReadinessGate:
    status: str
    strategy_id: str
    row_id: str
    author_market_code: str
    forecast_series_status: str
    daily_equilibrium_runtime_status: str
    trend_runtime_status: str
    trend_runtime_method_status: str
    vol_attenuation_runtime_status: str
    vol_attenuation_method_status: str
    hostile_audit_status: str
    stale_backtest_executables_status: str
    position_execution_cost_status: str
    hourly_archive_manifest_status: str
    first_backtest_scope: str
    promotion_boundary_status: str
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()
    performance_outputs: tuple[str, ...] = ()

    def validate(
        self,
        semantics_lock: S27ZNPositionExecutionCostSemanticsLock,
        archive_manifest: S27ZNBacktestHourlyArchiveWindowManifest,
    ) -> None:
        semantics_lock.validate()
        archive_manifest.validate()
        _require_exact("S27 ZN readiness gate status", self.status, S27_ZN_BACKTEST_READINESS_GATE_STATUS)
        _require_exact("S27 ZN readiness strategy id", self.strategy_id, "S27_SAFER_FAST_MEAN_REVERSION_ZN_DEV_RECON")
        _require_exact("S27 ZN readiness row id", self.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        _require_exact("S27 ZN readiness author market code", self.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
        _require_exact("S27 ZN readiness forecast series status", self.forecast_series_status, S27_FORECAST_SERIES_STATUS)
        _require_exact(
            "S27 ZN readiness daily EWMA5 equilibrium runtime status",
            self.daily_equilibrium_runtime_status,
            S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS,
        )
        _require_exact("S27 ZN readiness trend runtime status", self.trend_runtime_status, S27_TREND_RUNTIME_STATUS)
        _require_exact(
            "S27 ZN readiness trend runtime method status",
            self.trend_runtime_method_status,
            S27_DAILY_TREND_METHOD_STATUS,
        )
        _require_exact(
            "S27 ZN readiness volatility attenuation runtime status",
            self.vol_attenuation_runtime_status,
            S27_VOL_ATTENUATION_RUNTIME_STATUS,
        )
        _require_exact(
            "S27 ZN readiness volatility attenuation method status",
            self.vol_attenuation_method_status,
            S27_DAILY_VOL_ATTENUATION_METHOD_STATUS,
        )
        _require_exact("S27 ZN readiness hostile audit status", self.hostile_audit_status, "PASS_LOCAL_HOSTILE_AUDIT_NO_BLOCKING_FINDINGS")
        _require_exact(
            "S27 ZN readiness stale backtest executables status",
            self.stale_backtest_executables_status,
            S27_STALE_BACKTEST_EXECUTABLES_STATUS,
        )
        _require_exact(
            "S27 ZN readiness position/execution/cost status",
            self.position_execution_cost_status,
            S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_STATUS,
        )
        _require_exact(
            "S27 ZN readiness hourly archive manifest status",
            self.hourly_archive_manifest_status,
            S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_STATUS,
        )
        _require_exact(
            "S27 ZN first backtest scope",
            self.first_backtest_scope,
            "QUARANTINED_DEV_RECON_ZN_ONLY_S27_NO_OOS_NO_LOCKBOX_NO_PROMOTION",
        )
        _require_exact(
            "S27 ZN promotion boundary status",
            self.promotion_boundary_status,
            "NO_ALPHA_CLAIM_NO_DEPLOYMENT_NO_TRADING",
        )
        if self.diagnostics_outputs or self.backtest_outputs or self.position_outputs or self.performance_outputs:
            raise CarverBlocked("S27 ZN readiness gate must not emit diagnostics, backtests, positions, or performance outputs")


@dataclass(frozen=True)
class S27SourceLocks:
    s26_dependency_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    trend_overlay_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    vol_quantile_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    vol_attenuation_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    trend_interaction_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    s27_scalar_and_cap_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    no_forecast_combination_fdm_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    output_boundary_status: SourceRuleStatus = SourceRuleStatus.LOCKED

    def validate(self) -> None:
        for name, status in (
            ("S26 dependency", self.s26_dependency_status),
            ("EWMAC(16,64) trend overlay", self.trend_overlay_status),
            ("relative volatility quantile", self.vol_quantile_status),
            ("EWMA(10) volatility attenuation", self.vol_attenuation_status),
            ("does-not-oppose-trend interaction", self.trend_interaction_status),
            ("S27 scalar around 20 and forecast cap", self.s27_scalar_and_cap_status),
            ("no daily forecast-combination FDM", self.no_forecast_combination_fdm_status),
            ("S27 output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"S27 {name} source is unresolved")


@dataclass(frozen=True)
class S27RealHourlySourceLocks:
    s26_forecast_row_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    trend_overlay_runtime_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    vol_attenuation_runtime_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    s27_scalar_and_cap_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    no_fdm_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    no_buffering_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    output_boundary_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED

    def validate(self) -> None:
        for name, status in (
            ("S26 forecast row", self.s26_forecast_row_status),
            ("EWMAC16 trend overlay runtime", self.trend_overlay_runtime_status),
            ("V/Q/M volatility attenuation runtime", self.vol_attenuation_runtime_status),
            ("S27 scalar around 20 and forecast cap", self.s27_scalar_and_cap_status),
            ("no FDM rule", self.no_fdm_status),
            ("no buffering rule", self.no_buffering_status),
            ("S27 forecast-only output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"S27 real-hourly {name} source is unresolved")


@dataclass(frozen=True)
class S27TrendOverlayRuntimeLedgerSourceLocks:
    s26_forecast_series_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    trend_overlay_runtime_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    no_lookahead_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    output_boundary_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED

    def validate(self) -> None:
        for name, status in (
            ("S26 forecast series", self.s26_forecast_series_status),
            ("EWMAC16 trend overlay runtime", self.trend_overlay_runtime_status),
            ("no-lookahead runtime provenance", self.no_lookahead_status),
            ("trend runtime ledger output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"S27 trend runtime ledger {name} source is unresolved")


@dataclass(frozen=True)
class S27VolAttenuationRuntimeLedgerSourceLocks:
    s26_forecast_series_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    vol_attenuation_runtime_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    no_lookahead_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    output_boundary_status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED

    def validate(self) -> None:
        for name, status in (
            ("S26 forecast series", self.s26_forecast_series_status),
            ("V/Q/M volatility attenuation runtime", self.vol_attenuation_runtime_status),
            ("no-lookahead runtime provenance", self.no_lookahead_status),
            ("volatility runtime ledger output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"S27 V/Q/M runtime ledger {name} source is unresolved")


@dataclass(frozen=True)
class S27TrendOverlayRuntimeValue:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    as_of: datetime
    trend_fast_ewma: float
    trend_slow_ewma: float
    trend_forecast: float
    runtime_status: str
    method_status: str
    no_lookahead_status: str
    source_artifact_sha256: str

    def validate(self, forecast_as_of: datetime) -> None:
        _require_exact_datetime("S27 trend runtime as_of", self.as_of, forecast_as_of)
        _require_finite("S27 trend fast EWMA", self.trend_fast_ewma)
        _require_finite("S27 trend slow EWMA", self.trend_slow_ewma)
        _require_finite("S27 trend forecast", self.trend_forecast)
        _require_exact("S27 trend runtime status", self.runtime_status, S27_TREND_RUNTIME_STATUS)
        _require_exact("S27 trend method status", self.method_status, S27_DAILY_TREND_METHOD_STATUS)
        _require_exact("S27 trend no-lookahead status", self.no_lookahead_status, "PASS_NO_LOOKAHEAD")
        _require_sha256_text("S27 trend source artifact sha256", self.source_artifact_sha256)


@dataclass(frozen=True)
class S27VolAttenuationRuntimeValue:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    as_of: datetime
    vol_multiplier: float
    runtime_status: str
    method_status: str
    no_lookahead_status: str
    source_artifact_sha256: str

    def validate(self, forecast_as_of: datetime) -> None:
        _require_exact_datetime("S27 volatility runtime as_of", self.as_of, forecast_as_of)
        _require_finite("S27 volatility multiplier", self.vol_multiplier)
        if self.vol_multiplier < 0.5 or self.vol_multiplier > 2.0:
            raise CarverBlocked("S27 volatility multiplier must remain inside the V/Q/M [0.5, 2.0] envelope")
        _require_exact("S27 volatility runtime status", self.runtime_status, S27_VOL_ATTENUATION_RUNTIME_STATUS)
        _require_exact("S27 volatility method status", self.method_status, S27_DAILY_VOL_ATTENUATION_METHOD_STATUS)
        _require_exact("S27 volatility no-lookahead status", self.no_lookahead_status, "PASS_NO_LOOKAHEAD")
        _require_sha256_text("S27 volatility source artifact sha256", self.source_artifact_sha256)


@dataclass(frozen=True)
class S26DailyEquilibriumRuntimeValue:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    as_of: datetime
    equilibrium_ewma_5: float
    runtime_status: str
    method_status: str
    no_lookahead_status: str
    source_artifact_sha256: str

    def validate(self, forecast_as_of: datetime) -> None:
        _require_exact_datetime("S26 daily equilibrium runtime as_of", self.as_of, forecast_as_of)
        require_finite_positive("S26 daily EWMA5 equilibrium", self.equilibrium_ewma_5)
        _require_exact("S26 daily equilibrium runtime status", self.runtime_status, S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS)
        _require_exact("S26 daily equilibrium method status", self.method_status, S26_DAILY_EQUILIBRIUM_METHOD_STATUS)
        _require_exact("S26 daily equilibrium no-lookahead status", self.no_lookahead_status, "PASS_NO_LOOKAHEAD")
        _require_sha256_text("S26 daily equilibrium source artifact sha256", self.source_artifact_sha256)


@dataclass(frozen=True)
class S26FastMeanReversionRequest:
    current_price: SyntheticHourlyPrice
    as_of: datetime
    sigma_percent: TimedValue
    daily_equilibrium_runtime: S26DailyEquilibriumRuntimeValue
    source_locks: S26SourceLocks = S26SourceLocks()
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S26FastMeanReversionResult:
    as_of: datetime
    current_price: float
    equilibrium: float
    raw_forecast: float
    sigma_price: float
    risk_adjusted_forecast: float
    scalar: float
    scaled_forecast: float
    capped_forecast: float
    fdm_used: bool = False
    buffering_used: bool = False
    performance_metrics: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class S26QuarantinedHourlyZNBar:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    provider_ts_event_start_utc: datetime
    derived_completed_bar_end_utc: datetime
    completed_trading_date: str
    close: float
    strategy_use_status: str

    def validate(self) -> None:
        if self.row_id != S26_ZN_WORKED_EXAMPLE_ROW_ID:
            raise CarverBlocked("S26 first real-hourly bridge must use APPENDIX_C_172_004")
        if self.author_market_code != S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE:
            raise CarverBlocked("S26 first real-hourly bridge must use ZN")
        if self.instrument_id != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
            raise CarverBlocked("S26 first real-hourly bridge must use Databento instrument_id 42000661")
        if self.raw_symbol != S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL:
            raise CarverBlocked("S26 first real-hourly bridge must use Databento raw symbol ZNM6")
        _validate_real_hourly_timestamp("provider ts_event start", self.provider_ts_event_start_utc)
        _validate_real_hourly_timestamp("derived completed bar end", self.derived_completed_bar_end_utc)
        if self.derived_completed_bar_end_utc - self.provider_ts_event_start_utc != timedelta(hours=1):
            raise CarverBlocked("S26 hourly completed bar end must equal ts_event plus one hour")
        require_non_empty_text("completed trading date", self.completed_trading_date)
        require_finite_positive("S26 quarantined hourly close", self.close)
        if self.strategy_use_status != S26_ZN_FORECAST_INPUT_STATUS:
            raise CarverBlocked("S26 quarantined hourly bar is not forecast-input ready")


@dataclass(frozen=True)
class S26QuarantinedHourlyForecastRequest:
    bars: tuple[S26QuarantinedHourlyZNBar, ...]
    as_of: datetime
    sigma_percent: TimedValue
    daily_equilibrium_runtime: S26DailyEquilibriumRuntimeValue
    source_locks: S26QuarantinedHourlySourceLocks
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S26QuarantinedHourlyForecastResult:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    provider_ts_event_start_utc: datetime
    derived_completed_bar_end_utc: datetime
    completed_trading_date: str
    price_close: float
    equilibrium_ewma_5: float
    raw_forecast: float
    sigma_percent: float
    sigma_price: float
    risk_adjusted_forecast: float
    forecast_scalar: float
    scaled_forecast: float
    capped_forecast: float
    equilibrium_runtime_status: str
    equilibrium_method_status: str
    equilibrium_source_artifact_sha256: str
    source_locks_status: str
    forecast_output_status: str = S26_FORECAST_ONLY_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class S26QuarantinedHourlyForecastSeriesRequest:
    bars: tuple[S26QuarantinedHourlyOHLCVBar, ...]
    sigma_runtimes: tuple[S26SigmaPercentRuntimeValue, ...]
    daily_equilibrium_runtimes: tuple[S26DailyEquilibriumRuntimeValue, ...]
    source_locks: S26QuarantinedHourlySourceLocks
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S26QuarantinedHourlyForecastSeriesResult:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    first_forecast_as_of: datetime
    last_forecast_as_of: datetime
    input_hourly_rows: int
    forecast_rows: tuple[S26QuarantinedHourlyForecastResult, ...]
    series_output_status: str = S26_ZN_FORECAST_SERIES_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class S27SaferFastMeanReversionRequest:
    current_price: SyntheticHourlyPrice
    as_of: datetime
    sigma_percent: TimedValue
    daily_equilibrium_runtime: S26DailyEquilibriumRuntimeValue
    trend_runtime: S27TrendOverlayRuntimeValue
    vol_runtime: S27VolAttenuationRuntimeValue
    s26_source_locks: S26SourceLocks = S26SourceLocks()
    s27_source_locks: S27SourceLocks = S27SourceLocks()
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S27SaferFastMeanReversionResult:
    as_of: datetime
    s26_raw_forecast: float
    trend_fast_ewma: float
    trend_slow_ewma: float
    trend_forecast: float
    vol_multiplier: float
    opposes_trend: bool
    trend_interaction_policy: str
    adjusted_raw_forecast: float
    sigma_price: float
    risk_adjusted_forecast: float
    scalar: float
    scaled_forecast: float
    capped_forecast: float
    fdm_used: bool = False
    buffering_used: bool = False
    performance_metrics: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class S27QuarantinedHourlyForecastRequest:
    s26_forecast: S26QuarantinedHourlyForecastResult
    trend_runtime: S27TrendOverlayRuntimeValue
    vol_runtime: S27VolAttenuationRuntimeValue
    source_locks: S27RealHourlySourceLocks
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S27QuarantinedHourlyForecastResult:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    as_of: datetime
    completed_trading_date: str
    s26_raw_forecast: float
    trend_fast_ewma: float
    trend_slow_ewma: float
    trend_forecast: float
    vol_multiplier: float
    opposes_trend: bool
    trend_interaction_policy: str
    adjusted_raw_forecast: float
    sigma_price: float
    risk_adjusted_forecast: float
    forecast_scalar: float
    scaled_forecast: float
    capped_forecast: float
    source_locks_status: str
    forecast_output_status: str = S27_FORECAST_ONLY_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class S27ZNPrevalidatedBasePosition:
    row_id: str
    author_market_code: str
    as_of: datetime
    base_unrounded_contracts: float
    source_status: str
    capital_risk_status: str
    multiplier_fx_status: str
    source_artifact_sha256: str

    def validate(self, forecast_as_of: datetime) -> None:
        _require_exact("S27 ZN base position row id", self.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        _require_exact(
            "S27 ZN base position author market code",
            self.author_market_code,
            S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
        )
        _require_exact_datetime("S27 ZN base position as_of", self.as_of, forecast_as_of)
        require_finite_positive("S27 ZN prevalidated M1 base position", self.base_unrounded_contracts)
        _require_exact("S27 ZN base position source status", self.source_status, "PREVALIDATED_M1_BASE_POSITION_LOCKED")
        _require_exact(
            "S27 ZN base position capital/risk status",
            self.capital_risk_status,
            "CAPITAL_TARGET_RISK_ANNUAL_RISK_LOCKED_NO_LOOKAHEAD",
        )
        _require_exact(
            "S27 ZN base position multiplier/FX status",
            self.multiplier_fx_status,
            "ZN_MULTIPLIER_USD_FX_LOCKED",
        )
        _require_sha256_text("S27 ZN base position source artifact sha256", self.source_artifact_sha256)


@dataclass(frozen=True)
class S27ZNDesiredPositionRequest:
    forecast: S27QuarantinedHourlyForecastResult
    base_position: S27ZNPrevalidatedBasePosition
    rounding_policy: RoundingPolicy
    semantics_lock: S27ZNPositionExecutionCostSemanticsLock
    position_output_authorization_status: str
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S27ZNDesiredPositionResult:
    row_id: str
    author_market_code: str
    raw_symbol: str
    as_of: datetime
    completed_trading_date: str
    capped_forecast: float
    forecast_to_position_divisor: float
    forecast_multiplier: float
    base_unrounded_contracts: float
    desired_unrounded_contracts: float
    desired_rounded_contracts: int
    rounding_policy: RoundingPolicy
    position_output_status: str = S27_ZN_DESIRED_POSITION_PLUMBING_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    return_outputs: tuple[str, ...] = ()
    pnl_outputs: tuple[str, ...] = ()
    cost_outputs: tuple[str, ...] = ()

    def validate(self) -> None:
        _require_exact("S27 ZN desired position row id", self.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        _require_exact(
            "S27 ZN desired position author market code",
            self.author_market_code,
            S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
        )
        require_non_empty_text("S27 ZN desired position raw symbol", self.raw_symbol)
        _validate_real_hourly_timestamp("S27 ZN desired position as_of", self.as_of)
        require_non_empty_text("S27 ZN desired position completed trading date", self.completed_trading_date)
        _require_finite("S27 ZN desired position capped forecast", self.capped_forecast)
        if self.forecast_to_position_divisor != 10.0:
            raise CarverBlocked("S27 ZN forecast-to-position divisor must be 10.0")
        _require_finite("S27 ZN desired position forecast multiplier", self.forecast_multiplier)
        require_finite_positive("S27 ZN desired position base contracts", self.base_unrounded_contracts)
        _require_finite("S27 ZN desired unrounded contracts", self.desired_unrounded_contracts)
        if not isinstance(self.desired_rounded_contracts, int):
            raise CarverBlocked("S27 ZN desired rounded contracts must be an integer")
        _require_exact("S27 ZN desired position status", self.position_output_status, S27_ZN_DESIRED_POSITION_PLUMBING_STATUS)
        if self.diagnostics_outputs or self.backtest_outputs or self.return_outputs or self.pnl_outputs or self.cost_outputs:
            raise CarverBlocked("S27 ZN desired-position plumbing must not emit diagnostics, backtests, returns, PnL, or costs")


@dataclass(frozen=True)
class S27QuarantinedHourlyForecastSeriesRequest:
    s26_forecast_series: S26QuarantinedHourlyForecastSeriesResult
    trend_runtimes: tuple[S27TrendOverlayRuntimeValue, ...]
    vol_runtimes: tuple[S27VolAttenuationRuntimeValue, ...]
    source_locks: S27RealHourlySourceLocks
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S27QuarantinedHourlyForecastSeriesResult:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    first_forecast_as_of: datetime
    last_forecast_as_of: datetime
    input_s26_forecast_rows: int
    forecast_rows: tuple[S27QuarantinedHourlyForecastResult, ...]
    series_output_status: str = S27_FORECAST_SERIES_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class S27TrendOverlayRuntimeLedgerRequest:
    s26_forecast_series: S26QuarantinedHourlyForecastSeriesResult
    trend_runtimes: tuple[S27TrendOverlayRuntimeValue, ...]
    source_locks: S27TrendOverlayRuntimeLedgerSourceLocks
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S27TrendOverlayRuntimeLedgerResult:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    first_runtime_as_of: datetime
    last_runtime_as_of: datetime
    input_s26_forecast_rows: int
    trend_runtimes: tuple[S27TrendOverlayRuntimeValue, ...]
    ledger_status: str = S27_TREND_RUNTIME_LEDGER_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class S27VolAttenuationRuntimeLedgerRequest:
    s26_forecast_series: S26QuarantinedHourlyForecastSeriesResult
    vol_runtimes: tuple[S27VolAttenuationRuntimeValue, ...]
    source_locks: S27VolAttenuationRuntimeLedgerSourceLocks
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class S27VolAttenuationRuntimeLedgerResult:
    row_id: str
    author_market_code: str
    instrument_id: int
    raw_symbol: str
    first_runtime_as_of: datetime
    last_runtime_as_of: datetime
    input_s26_forecast_rows: int
    vol_runtimes: tuple[S27VolAttenuationRuntimeValue, ...]
    ledger_status: str = S27_VOL_ATTENUATION_RUNTIME_LEDGER_STATUS
    diagnostics_outputs: tuple[str, ...] = ()
    backtest_outputs: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


def s26_fast_mean_reversion_forecast(request: S26FastMeanReversionRequest) -> S26FastMeanReversionResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    _validate_hourly_timestamp(request.as_of)
    request.current_price.validate()
    _require_exact_datetime("S26 synthetic current price timestamp", request.current_price.timestamp, request.as_of)
    request.daily_equilibrium_runtime.validate(request.as_of)
    _validate_timed_sigma_percent(request.sigma_percent, request.as_of)

    result = _s26_result_from_equilibrium(
        current_price=request.current_price.price,
        equilibrium=request.daily_equilibrium_runtime.equilibrium_ewma_5,
        as_of=request.as_of,
        sigma_percent=request.sigma_percent.value,
    )
    _validate_no_strategy_outputs("S26", result.fdm_used, result.buffering_used, result.performance_metrics, result.position_outputs)
    return result


def validate_s26_zn_hourly_databento_request_manifest(
    manifest: S26DatabentoHourlyIntakeRequestManifest,
) -> S26DatabentoHourlyIntakeRequestManifest:
    manifest.validate()
    return manifest


def build_s26_zn_extended_hourly_forecast_only_coverage_manifest() -> S26ExtendedHourlyForecastOnlyCoverageManifest:
    manifest = S26ExtendedHourlyForecastOnlyCoverageManifest(
        status=S26_ZN_EXTENDED_HOURLY_REQUEST_MANIFEST_STATUS,
        provider=S26_ZN_DATABENTO_PROVIDER,
        dataset=S26_ZN_DATABENTO_DATASET,
        schema=S26_ZN_DATABENTO_SCHEMA,
        stype_in=S26_ZN_DATABENTO_STYPE_IN,
        symbols=(S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,),
        row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
        author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
        expected_raw_symbol=S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
        request_start_utc=S26_ZN_EXTENDED_HOURLY_REQUEST_START_UTC,
        request_end_utc=S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC,
        target_completed_trading_dates=S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES,
        extended_window_purpose="EXPAND_S26_FORECAST_ONLY_COVERAGE_BEFORE_S27_TEST_GATE",
        sigma_runtime_requirement="ONE_PREVALIDATED_NO_LOOKAHEAD_SIGMA_RUNTIME_PER_FORECAST_ROW_REQUIRED",
        output_boundary_status="FORECAST_ONLY_NO_DIAGNOSTIC_NO_BACKTEST_NO_POSITION",
        continuous_contracts_status="CLOSED",
        parent_symbols_status="CLOSED",
        raw_symbol_selector_status="CLOSED_CROSS_CHECK_ONLY",
        output_root=S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT,
        no_authorization=(
            "NO_PROVIDER_API_ACCESS",
            "NO_DATA_DOWNLOAD",
            "NO_MARKET_ROW_PARSING",
            "NO_DIAGNOSTICS",
            "NO_BACKTESTS",
            "NO_FORECAST_COMPUTATION",
            "NO_POSITIONS",
            "NO_GIT_OPERATIONS",
        ),
    )
    return validate_s26_zn_extended_hourly_forecast_only_coverage_manifest(manifest)


def validate_s26_zn_extended_hourly_forecast_only_coverage_manifest(
    manifest: S26ExtendedHourlyForecastOnlyCoverageManifest,
) -> S26ExtendedHourlyForecastOnlyCoverageManifest:
    manifest.validate()
    return manifest


def normalize_s26_zn_databento_hourly_ohlcv_raw_row(
    row: S26DatabentoHourlyOHLCVRawRow,
    manifest: S26DatabentoHourlyIntakeRequestManifest,
    *,
    completed_trading_date: str,
    strategy_use_status: str = S26_ZN_HOURLY_QUARANTINE_STATUS,
) -> S26QuarantinedHourlyOHLCVBar:
    row.validate(manifest)
    require_non_empty_text("S26 completed trading date", completed_trading_date)
    if completed_trading_date not in S26_ZN_TARGET_COMPLETED_TRADING_DATES:
        raise CarverBlocked("S26 normalized hourly bar must map to a locked target completed trading date")
    if strategy_use_status not in (S26_ZN_HOURLY_QUARANTINE_STATUS, S26_ZN_FORECAST_INPUT_STATUS):
        raise CarverBlocked("S26 normalized hourly bar has an unauthorized strategy-use status")
    return S26QuarantinedHourlyOHLCVBar(
        lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
        strategy_context="S26_FAST_MEAN_REVERSION_ZN_WORKED_EXAMPLE",
        provider=row.provider,
        dataset=row.dataset,
        schema=row.schema,
        stype_in=row.stype_in,
        row_id=row.row_id,
        author_market_code=row.author_market_code,
        instrument_id=row.instrument_id,
        raw_symbol=row.raw_symbol,
        provider_ts_event_start_utc=row.provider_ts_event_start_utc,
        derived_completed_bar_end_utc=row.provider_ts_event_start_utc + timedelta(hours=1),
        completed_trading_date=completed_trading_date,
        open=row.open,
        high=row.high,
        low=row.low,
        close=row.close,
        volume=row.volume,
        provider_condition_status=row.provider_condition_status,
        row_shape_status="PASS_OHLCV_1H_ROW_SHAPE",
        source_raw_sha256=row.source_raw_sha256,
        strategy_use_status=strategy_use_status,
    )


def parse_s26_zn_databento_hourly_ohlcv_csv_text(
    csv_text: str,
    manifest: S26DatabentoHourlyIntakeRequestManifest,
    *,
    completed_trading_dates_by_ts_event_start_utc: dict[datetime, str],
    source_raw_sha256: str,
    provider_condition_status_by_utc_date: dict[str, str] | None = None,
    strategy_use_status: str = S26_ZN_HOURLY_QUARANTINE_STATUS,
) -> tuple[S26QuarantinedHourlyOHLCVBar, ...]:
    manifest.validate()
    require_non_empty_text("S26 ZN hourly CSV text", csv_text)
    _require_sha256_text("S26 ZN source raw sha256", source_raw_sha256)
    reader = csv.DictReader(StringIO(csv_text))
    _validate_s26_zn_hourly_csv_header(reader.fieldnames)
    parsed: list[S26QuarantinedHourlyOHLCVBar] = []
    seen: set[datetime] = set()
    for row_number, record in enumerate(reader, start=2):
        timestamp = _parse_utc_hourly_timestamp(record["ts_event"], f"S26 ZN CSV row {row_number} ts_event")
        if timestamp in seen:
            raise CarverBlocked("S26 ZN CSV contains duplicate ts_event rows")
        seen.add(timestamp)
        if timestamp not in completed_trading_dates_by_ts_event_start_utc:
            raise CarverBlocked("S26 ZN CSV row lacks locked completed trading date mapping")
        raw = S26DatabentoHourlyOHLCVRawRow(
            provider=S26_ZN_DATABENTO_PROVIDER,
            dataset=S26_ZN_DATABENTO_DATASET,
            schema=S26_ZN_DATABENTO_SCHEMA,
            stype_in=S26_ZN_DATABENTO_STYPE_IN,
            row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
            author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
            instrument_id=_parse_int(record["instrument_id"], f"S26 ZN CSV row {row_number} instrument_id"),
            raw_symbol=record["raw_symbol"],
            provider_ts_event_start_utc=timestamp,
            open=_parse_float(record["open"], f"S26 ZN CSV row {row_number} open"),
            high=_parse_float(record["high"], f"S26 ZN CSV row {row_number} high"),
            low=_parse_float(record["low"], f"S26 ZN CSV row {row_number} low"),
            close=_parse_float(record["close"], f"S26 ZN CSV row {row_number} close"),
            volume=_parse_float(record["volume"], f"S26 ZN CSV row {row_number} volume"),
            source_raw_sha256=source_raw_sha256,
            provider_condition_status=(provider_condition_status_by_utc_date or {}).get(
                timestamp.date().isoformat(),
                "PROVIDER_CONDITION_PENDING_JOIN",
            ),
        )
        parsed.append(
            normalize_s26_zn_databento_hourly_ohlcv_raw_row(
                raw,
                manifest,
                completed_trading_date=completed_trading_dates_by_ts_event_start_utc[timestamp],
                strategy_use_status=strategy_use_status,
            )
        )
    if not parsed:
        raise CarverBlocked("S26 ZN CSV contains no hourly rows")
    _validate_quarantined_hourly_ohlcv_sequence(tuple(parsed))
    return tuple(parsed)


def s26_forecast_only_from_quarantined_zn_hourly_ohlcv_bars(
    bars: tuple[S26QuarantinedHourlyOHLCVBar, ...],
    *,
    sigma_runtime: S26SigmaPercentRuntimeValue,
    daily_equilibrium_runtime: S26DailyEquilibriumRuntimeValue,
    as_of: datetime,
    source_locks: S26QuarantinedHourlySourceLocks,
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
) -> S26QuarantinedHourlyForecastResult:
    source_locks.validate()
    _validate_quarantined_hourly_ohlcv_bars_for_handoff(bars, as_of)
    sigma_percent = sigma_runtime.validate(as_of)
    forecast_bars = tuple(
        S26QuarantinedHourlyZNBar(
            row_id=bar.row_id,
            author_market_code=bar.author_market_code,
            instrument_id=bar.instrument_id,
            raw_symbol=bar.raw_symbol,
            provider_ts_event_start_utc=bar.provider_ts_event_start_utc,
            derived_completed_bar_end_utc=bar.derived_completed_bar_end_utc,
            completed_trading_date=bar.completed_trading_date,
            close=bar.close,
            strategy_use_status=S26_ZN_FORECAST_INPUT_STATUS,
        )
        for bar in bars
    )
    result = s26_forecast_only_from_quarantined_zn_hourly_bars(
        S26QuarantinedHourlyForecastRequest(
            bars=forecast_bars,
            as_of=as_of,
            sigma_percent=sigma_percent,
            daily_equilibrium_runtime=daily_equilibrium_runtime,
            source_locks=source_locks,
            lane_class=lane_class,
        )
    )
    if result.forecast_output_status != S26_FORECAST_ONLY_STATUS:
        raise CarverBlocked("S26 G_R1B output status drifted away from forecast-only")
    return result


def s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars(
    request: S26QuarantinedHourlyForecastSeriesRequest,
) -> S26QuarantinedHourlyForecastSeriesResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    if len(request.bars) < S26_EQUILIBRIUM_EWMA_SPAN:
        raise CarverBlocked("S26 G_R1C hourly OHLCV history is insufficient")
    _validate_quarantined_hourly_ohlcv_sequence(request.bars)
    forecast_as_ofs = tuple(
        bar.derived_completed_bar_end_utc
        for bar in request.bars[S26_EQUILIBRIUM_EWMA_SPAN - 1 :]
    )
    if len(request.sigma_runtimes) != len(forecast_as_ofs):
        raise CarverBlocked("S26 G_R1C requires exactly one sigma runtime per forecast row")
    if len(request.daily_equilibrium_runtimes) != len(forecast_as_ofs):
        raise CarverBlocked("S26 G_R1C requires exactly one daily EWMA5 equilibrium runtime per forecast row")
    runtime_by_as_of = {}
    for runtime in request.sigma_runtimes:
        if runtime.as_of in runtime_by_as_of:
            raise CarverBlocked("S26 G_R1C sigma runtimes must be unique by as_of")
        runtime_by_as_of[runtime.as_of] = runtime
    if tuple(runtime_by_as_of) != forecast_as_ofs:
        raise CarverBlocked("S26 G_R1C sigma runtime timestamps must match forecast row timestamps in order")
    equilibrium_by_as_of = {}
    for runtime in request.daily_equilibrium_runtimes:
        if runtime.as_of in equilibrium_by_as_of:
            raise CarverBlocked("S26 G_R1C daily EWMA5 equilibrium runtimes must be unique by as_of")
        equilibrium_by_as_of[runtime.as_of] = runtime
    if tuple(equilibrium_by_as_of) != forecast_as_ofs:
        raise CarverBlocked("S26 G_R1C daily EWMA5 equilibrium runtime timestamps must match forecast row timestamps in order")

    forecasts = []
    for offset, as_of in enumerate(forecast_as_ofs, start=S26_EQUILIBRIUM_EWMA_SPAN):
        forecasts.append(
            s26_forecast_only_from_quarantined_zn_hourly_ohlcv_bars(
                request.bars[:offset],
                sigma_runtime=runtime_by_as_of[as_of],
                daily_equilibrium_runtime=equilibrium_by_as_of[as_of],
                as_of=as_of,
                source_locks=request.source_locks,
                lane_class=request.lane_class,
            )
        )
    result = S26QuarantinedHourlyForecastSeriesResult(
        row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
        author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
        instrument_id=S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
        raw_symbol=S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
        first_forecast_as_of=forecast_as_ofs[0],
        last_forecast_as_of=forecast_as_ofs[-1],
        input_hourly_rows=len(request.bars),
        forecast_rows=tuple(forecasts),
    )
    _validate_forecast_series_only_output(result)
    return result


def s26_execution_semantics_source_lock(
    lock: S26ExecutionSemanticsSourceLock,
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
) -> S26ExecutionSemanticsSourceLock:
    require_source_native(lane_class)
    lock.validate()
    return lock


def build_s26_execution_semantics_source_lock() -> S26ExecutionSemanticsSourceLock:
    lock = S26ExecutionSemanticsSourceLock(
        hourly_completed_bar_policy="HOURLY_COMPLETED_BAR_ONLY",
        forecast_availability_policy="FORECAST_AVAILABLE_AFTER_DERIVED_COMPLETED_BAR_END_UTC",
        limit_order_semantics_policy="LIMIT_ORDER_STYLE_SEMANTICS_ONLY_NOT_MARKET_ORDER_FILL_MODEL",
        no_buffering_policy="NO_BUFFERING_USED",
        no_market_order_cost_assumption_policy="NO_MARKET_ORDER_COST_ASSUMPTION",
        execution_cadence_policy="SOURCE_FAITHFUL_HOURLY_CADENCE_NO_INTRABAR_LOOKAHEAD",
        position_sizing_status="POSITION_SIZING_CLOSED_SEPARATE_GATE_REQUIRED",
        cost_model_status="COST_MODEL_CLOSED_SEPARATE_GATE_REQUIRED",
        test_boundary_status="NOT_TEST_NOT_BACKTEST_NOT_DIAGNOSTIC",
    )
    return s26_execution_semantics_source_lock(lock)


def s27_zn_position_execution_cost_semantics_lock(
    lock: S27ZNPositionExecutionCostSemanticsLock,
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
) -> S27ZNPositionExecutionCostSemanticsLock:
    require_source_native(lane_class)
    lock.validate()
    return lock


def build_s27_zn_position_execution_cost_semantics_lock() -> S27ZNPositionExecutionCostSemanticsLock:
    lock = S27ZNPositionExecutionCostSemanticsLock(
        sizing_formula_policy="USE_M1_SIZE_CONTRACTS_BASE_POSITION_THEN_CAPPED_FORECAST_OVER_10",
        target_risk_policy="ANNUAL_TARGET_RISK_20_PERCENT_BOOK_DEFAULT_LOCK_REQUIRED_AT_TEST_GATE",
        single_instrument_context_policy="SINGLE_INSTRUMENT_ZN_STANDALONE_DEV_RECON_WEIGHT_1_IDM_1",
        annual_risk_estimate_policy="PREVALIDATED_S03_ANNUAL_PERCENTAGE_RISK_REQUIRED_NO_LOOKAHEAD",
        multiplier_fx_policy="ZN_CONTRACT_MULTIPLIER_AND_USD_FX_LOCK_REQUIRED_BEFORE_POSITION_OUTPUT",
        forecast_to_position_policy="FINAL_CAPPED_FORECAST_DIVIDED_BY_10_MULTIPLIES_BASE_POSITION",
        rounding_policy_status="ROUNDING_POLICY_MUST_BE_LOCKED_BEFORE_POSITION_OUTPUT",
        execution_policy="HOURLY_COMPLETED_BAR_NEXT_BAR_LIMIT_STYLE_NO_BUFFERING_NO_INTRABAR_LOOKAHEAD",
        cost_model_policy="COMMISSION_ONLY_DEV_RECON_ALLOWED_SPREAD_AND_MARKET_ORDER_COSTS_UNRESOLVED_FAIL_CLOSED",
        test_boundary_status="READINESS_ONLY_NOT_BACKTEST_NOT_DIAGNOSTIC_NOT_POSITION",
    )
    return s27_zn_position_execution_cost_semantics_lock(lock)


def validate_s27_zn_backtest_hourly_archive_window_manifest(
    manifest: S27ZNBacktestHourlyArchiveWindowManifest,
) -> S27ZNBacktestHourlyArchiveWindowManifest:
    manifest.validate()
    return manifest


def build_s27_zn_backtest_hourly_archive_window_manifest() -> S27ZNBacktestHourlyArchiveWindowManifest:
    manifest = S27ZNBacktestHourlyArchiveWindowManifest(
        status=S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_STATUS,
        provider=S26_ZN_DATABENTO_PROVIDER,
        dataset=S26_ZN_DATABENTO_DATASET,
        schema=S26_ZN_DATABENTO_SCHEMA,
        stype_in="raw_symbol",
        row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
        author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
        target_completed_trading_date_start=S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START,
        target_completed_trading_date_end=S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END,
        request_start_utc=S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_START_UTC,
        request_end_utc=S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_END_UTC,
        required_raw_symbols=S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS,
        local_continuous_policy="LOCAL_DATED_CONTRACT_CHAIN_REQUIRED_NO_PROVIDER_CONTINUOUS_FALLBACK",
        provider_condition_policy="PROVIDER_CONDITION_AVAILABLE_ONLY_ZERO_SILENT_ROW_SKIP",
        output_root=S27_ZN_BACKTEST_HOURLY_ARCHIVE_OUTPUT_ROOT,
        no_authorization=(
            "NO_PROVIDER_API_ACCESS",
            "NO_DATA_DOWNLOAD",
            "NO_MARKET_ROW_PARSING",
            "NO_DIAGNOSTICS",
            "NO_BACKTESTS",
            "NO_FORECAST_COMPUTATION",
            "NO_POSITIONS",
            "NO_GIT_OPERATIONS",
        ),
    )
    return validate_s27_zn_backtest_hourly_archive_window_manifest(manifest)


def s27_zn_single_instrument_backtest_readiness_gate(
    gate: S27ZNSingleInstrumentBacktestReadinessGate,
    *,
    semantics_lock: S27ZNPositionExecutionCostSemanticsLock,
    archive_manifest: S27ZNBacktestHourlyArchiveWindowManifest,
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
) -> S27ZNSingleInstrumentBacktestReadinessGate:
    require_source_native(lane_class)
    gate.validate(semantics_lock, archive_manifest)
    return gate


def build_s27_zn_single_instrument_backtest_readiness_gate() -> S27ZNSingleInstrumentBacktestReadinessGate:
    semantics_lock = build_s27_zn_position_execution_cost_semantics_lock()
    archive_manifest = build_s27_zn_backtest_hourly_archive_window_manifest()
    gate = S27ZNSingleInstrumentBacktestReadinessGate(
        status=S27_ZN_BACKTEST_READINESS_GATE_STATUS,
        strategy_id="S27_SAFER_FAST_MEAN_REVERSION_ZN_DEV_RECON",
        row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
        author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
        forecast_series_status=S27_FORECAST_SERIES_STATUS,
        daily_equilibrium_runtime_status=S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS,
        trend_runtime_status=S27_TREND_RUNTIME_STATUS,
        trend_runtime_method_status=S27_DAILY_TREND_METHOD_STATUS,
        vol_attenuation_runtime_status=S27_VOL_ATTENUATION_RUNTIME_STATUS,
        vol_attenuation_method_status=S27_DAILY_VOL_ATTENUATION_METHOD_STATUS,
        hostile_audit_status="PASS_LOCAL_HOSTILE_AUDIT_NO_BLOCKING_FINDINGS",
        stale_backtest_executables_status=S27_STALE_BACKTEST_EXECUTABLES_STATUS,
        position_execution_cost_status=S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_STATUS,
        hourly_archive_manifest_status=S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_STATUS,
        first_backtest_scope="QUARANTINED_DEV_RECON_ZN_ONLY_S27_NO_OOS_NO_LOCKBOX_NO_PROMOTION",
        promotion_boundary_status="NO_ALPHA_CLAIM_NO_DEPLOYMENT_NO_TRADING",
    )
    return s27_zn_single_instrument_backtest_readiness_gate(
        gate,
        semantics_lock=semantics_lock,
        archive_manifest=archive_manifest,
    )


def s26_forecast_only_from_quarantined_zn_hourly_bars(
    request: S26QuarantinedHourlyForecastRequest,
) -> S26QuarantinedHourlyForecastResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    _validate_real_hourly_timestamp("S26 forecast as_of", request.as_of)
    _validate_timed_sigma_percent(request.sigma_percent, request.as_of)
    _validate_quarantined_hourly_zn_bars(request.bars, request.as_of)
    request.daily_equilibrium_runtime.validate(request.as_of)
    _validate_s26_daily_equilibrium_identity(request.daily_equilibrium_runtime, request.bars[-1])

    last = request.bars[-1]
    s26 = _s26_result_from_equilibrium(
        current_price=last.close,
        equilibrium=request.daily_equilibrium_runtime.equilibrium_ewma_5,
        as_of=request.as_of,
        sigma_percent=request.sigma_percent.value,
    )
    result = S26QuarantinedHourlyForecastResult(
        row_id=last.row_id,
        author_market_code=last.author_market_code,
        instrument_id=last.instrument_id,
        raw_symbol=last.raw_symbol,
        provider_ts_event_start_utc=last.provider_ts_event_start_utc,
        derived_completed_bar_end_utc=last.derived_completed_bar_end_utc,
        completed_trading_date=last.completed_trading_date,
        price_close=s26.current_price,
        equilibrium_ewma_5=s26.equilibrium,
        raw_forecast=s26.raw_forecast,
        sigma_percent=request.sigma_percent.value,
        sigma_price=s26.sigma_price,
        risk_adjusted_forecast=s26.risk_adjusted_forecast,
        forecast_scalar=s26.scalar,
        scaled_forecast=s26.scaled_forecast,
        capped_forecast=s26.capped_forecast,
        equilibrium_runtime_status=request.daily_equilibrium_runtime.runtime_status,
        equilibrium_method_status=request.daily_equilibrium_runtime.method_status,
        equilibrium_source_artifact_sha256=request.daily_equilibrium_runtime.source_artifact_sha256,
        source_locks_status="LOCKED_QUARANTINE_HOURLY_ZN_S26_FORECAST_ONLY",
    )
    _validate_forecast_only_output(result)
    return result


def s27_safer_fast_mean_reversion_forecast(
    request: S27SaferFastMeanReversionRequest,
) -> S27SaferFastMeanReversionResult:
    require_source_native(request.lane_class)
    request.s27_source_locks.validate()
    s26 = s26_fast_mean_reversion_forecast(
        S26FastMeanReversionRequest(
            current_price=request.current_price,
            as_of=request.as_of,
            sigma_percent=request.sigma_percent,
            daily_equilibrium_runtime=request.daily_equilibrium_runtime,
            source_locks=request.s26_source_locks,
            lane_class=request.lane_class,
        )
    )
    request.trend_runtime.validate(request.as_of)
    request.vol_runtime.validate(request.as_of)
    _validate_s27_runtime_identity("S27 synthetic trend runtime", request.trend_runtime, request.daily_equilibrium_runtime)
    _validate_s27_runtime_identity("S27 synthetic volatility runtime", request.vol_runtime, request.daily_equilibrium_runtime)

    opposes = s26.raw_forecast * request.trend_runtime.trend_forecast < 0.0
    adjusted_raw = 0.0 if opposes else s26.raw_forecast * request.vol_runtime.vol_multiplier
    risk_adjusted = adjusted_raw / s26.sigma_price
    _require_finite("S27 risk-adjusted forecast", risk_adjusted)
    scaled = risk_adjusted * S27_FORECAST_SCALAR
    capped = cap_forecast(scaled, FORECAST_CAP)
    result = S27SaferFastMeanReversionResult(
        as_of=request.as_of,
        s26_raw_forecast=s26.raw_forecast,
        trend_fast_ewma=request.trend_runtime.trend_fast_ewma,
        trend_slow_ewma=request.trend_runtime.trend_slow_ewma,
        trend_forecast=request.trend_runtime.trend_forecast,
        vol_multiplier=request.vol_runtime.vol_multiplier,
        opposes_trend=opposes,
        trend_interaction_policy="ZERO_OPPOSING_MEAN_REVERSION_FORECAST",
        adjusted_raw_forecast=adjusted_raw,
        sigma_price=s26.sigma_price,
        risk_adjusted_forecast=risk_adjusted,
        scalar=S27_FORECAST_SCALAR,
        scaled_forecast=scaled,
        capped_forecast=capped,
    )
    _validate_no_strategy_outputs("S27", result.fdm_used, result.buffering_used, result.performance_metrics, result.position_outputs)
    return result


def s27_forecast_only_from_s26_forecast_row(
    request: S27QuarantinedHourlyForecastRequest,
) -> S27QuarantinedHourlyForecastResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    _validate_s26_forecast_row_for_s27_handoff(request.s26_forecast)
    forecast_as_of = request.s26_forecast.derived_completed_bar_end_utc
    request.trend_runtime.validate(forecast_as_of)
    request.vol_runtime.validate(forecast_as_of)
    _validate_s27_runtime_identity("S27 trend runtime", request.trend_runtime, request.s26_forecast)
    _validate_s27_runtime_identity("S27 volatility runtime", request.vol_runtime, request.s26_forecast)

    opposes = request.s26_forecast.raw_forecast * request.trend_runtime.trend_forecast < 0.0
    adjusted_raw = 0.0 if opposes else request.s26_forecast.raw_forecast * request.vol_runtime.vol_multiplier
    risk_adjusted = adjusted_raw / request.s26_forecast.sigma_price
    _require_finite("S27 real-hourly risk-adjusted forecast", risk_adjusted)
    scaled = risk_adjusted * S27_FORECAST_SCALAR
    capped = cap_forecast(scaled, FORECAST_CAP)
    result = S27QuarantinedHourlyForecastResult(
        row_id=request.s26_forecast.row_id,
        author_market_code=request.s26_forecast.author_market_code,
        instrument_id=request.s26_forecast.instrument_id,
        raw_symbol=request.s26_forecast.raw_symbol,
        as_of=forecast_as_of,
        completed_trading_date=request.s26_forecast.completed_trading_date,
        s26_raw_forecast=request.s26_forecast.raw_forecast,
        trend_fast_ewma=request.trend_runtime.trend_fast_ewma,
        trend_slow_ewma=request.trend_runtime.trend_slow_ewma,
        trend_forecast=request.trend_runtime.trend_forecast,
        vol_multiplier=request.vol_runtime.vol_multiplier,
        opposes_trend=opposes,
        trend_interaction_policy="ZERO_OPPOSING_MEAN_REVERSION_FORECAST",
        adjusted_raw_forecast=adjusted_raw,
        sigma_price=request.s26_forecast.sigma_price,
        risk_adjusted_forecast=risk_adjusted,
        forecast_scalar=S27_FORECAST_SCALAR,
        scaled_forecast=scaled,
        capped_forecast=capped,
        source_locks_status=S27_FORECAST_HANDOFF_STATUS,
    )
    _validate_s27_forecast_only_output(result)
    return result


def s27_forecast_series_only_from_s26_forecast_series(
    request: S27QuarantinedHourlyForecastSeriesRequest,
) -> S27QuarantinedHourlyForecastSeriesResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    _validate_forecast_series_only_output(request.s26_forecast_series)
    forecast_as_ofs = tuple(row.derived_completed_bar_end_utc for row in request.s26_forecast_series.forecast_rows)
    if len(request.trend_runtimes) != len(forecast_as_ofs):
        raise CarverBlocked("S27 series requires exactly one trend runtime per S26 forecast row")
    if len(request.vol_runtimes) != len(forecast_as_ofs):
        raise CarverBlocked("S27 series requires exactly one V/Q/M runtime per S26 forecast row")

    trend_by_as_of = _runtime_map_by_as_of("S27 trend", request.trend_runtimes)
    vol_by_as_of = _runtime_map_by_as_of("S27 volatility", request.vol_runtimes)
    if tuple(trend_by_as_of) != forecast_as_ofs:
        raise CarverBlocked("S27 trend runtime timestamps must match S26 forecast row timestamps in order")
    if tuple(vol_by_as_of) != forecast_as_ofs:
        raise CarverBlocked("S27 volatility runtime timestamps must match S26 forecast row timestamps in order")

    forecasts = tuple(
        s27_forecast_only_from_s26_forecast_row(
            S27QuarantinedHourlyForecastRequest(
                s26_forecast=row,
                trend_runtime=trend_by_as_of[row.derived_completed_bar_end_utc],
                vol_runtime=vol_by_as_of[row.derived_completed_bar_end_utc],
                source_locks=request.source_locks,
                lane_class=request.lane_class,
            )
        )
        for row in request.s26_forecast_series.forecast_rows
    )
    result = S27QuarantinedHourlyForecastSeriesResult(
        row_id=request.s26_forecast_series.row_id,
        author_market_code=request.s26_forecast_series.author_market_code,
        instrument_id=request.s26_forecast_series.instrument_id,
        raw_symbol=request.s26_forecast_series.raw_symbol,
        first_forecast_as_of=forecast_as_ofs[0],
        last_forecast_as_of=forecast_as_ofs[-1],
        input_s26_forecast_rows=len(request.s26_forecast_series.forecast_rows),
        forecast_rows=forecasts,
    )
    _validate_s27_forecast_series_only_output(result)
    return result


def s27_zn_desired_position_from_prevalidated_base(
    request: S27ZNDesiredPositionRequest,
) -> S27ZNDesiredPositionResult:
    require_source_native(request.lane_class)
    request.semantics_lock.validate()
    _validate_s27_forecast_only_output(request.forecast)
    request.base_position.validate(request.forecast.as_of)
    _require_exact(
        "S27 ZN desired-position authorization status",
        request.position_output_authorization_status,
        "PREVALIDATED_POSITION_PLUMBING_ONLY",
    )
    if request.rounding_policy is not RoundingPolicy.NEAREST:
        raise CarverBlocked("S27 ZN first dev/recon position plumbing is locked to NEAREST rounding unless separately authorized")

    forecast_multiplier = request.forecast.capped_forecast / 10.0
    desired_unrounded = request.base_position.base_unrounded_contracts * forecast_multiplier
    result = S27ZNDesiredPositionResult(
        row_id=request.forecast.row_id,
        author_market_code=request.forecast.author_market_code,
        raw_symbol=request.forecast.raw_symbol,
        as_of=request.forecast.as_of,
        completed_trading_date=request.forecast.completed_trading_date,
        capped_forecast=request.forecast.capped_forecast,
        forecast_to_position_divisor=10.0,
        forecast_multiplier=forecast_multiplier,
        base_unrounded_contracts=request.base_position.base_unrounded_contracts,
        desired_unrounded_contracts=desired_unrounded,
        desired_rounded_contracts=round(desired_unrounded),
        rounding_policy=request.rounding_policy,
    )
    result.validate()
    return result


def s27_trend_overlay_runtime_ledger_from_prevalidated_rows(
    request: S27TrendOverlayRuntimeLedgerRequest,
) -> S27TrendOverlayRuntimeLedgerResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    _validate_forecast_series_only_output(request.s26_forecast_series)
    forecast_as_ofs = tuple(row.derived_completed_bar_end_utc for row in request.s26_forecast_series.forecast_rows)
    if len(request.trend_runtimes) != len(forecast_as_ofs):
        raise CarverBlocked("S27 EWMAC16 trend runtime ledger requires exactly one runtime row per S26 forecast row")
    trend_by_as_of = _runtime_map_by_as_of("S27 trend", request.trend_runtimes)
    if tuple(trend_by_as_of) != forecast_as_ofs:
        raise CarverBlocked("S27 EWMAC16 trend runtime ledger timestamps must match S26 forecast row timestamps in order")
    for row in request.s26_forecast_series.forecast_rows:
        runtime = trend_by_as_of[row.derived_completed_bar_end_utc]
        runtime.validate(row.derived_completed_bar_end_utc)
        _validate_s27_runtime_identity("S27 trend runtime ledger row", runtime, row)
    result = S27TrendOverlayRuntimeLedgerResult(
        row_id=request.s26_forecast_series.row_id,
        author_market_code=request.s26_forecast_series.author_market_code,
        instrument_id=request.s26_forecast_series.instrument_id,
        raw_symbol=request.s26_forecast_series.raw_symbol,
        first_runtime_as_of=forecast_as_ofs[0],
        last_runtime_as_of=forecast_as_ofs[-1],
        input_s26_forecast_rows=len(request.s26_forecast_series.forecast_rows),
        trend_runtimes=tuple(trend_by_as_of[as_of] for as_of in forecast_as_ofs),
    )
    _validate_s27_trend_runtime_ledger_output(result)
    return result


def s27_vol_attenuation_runtime_ledger_from_prevalidated_rows(
    request: S27VolAttenuationRuntimeLedgerRequest,
) -> S27VolAttenuationRuntimeLedgerResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    _validate_forecast_series_only_output(request.s26_forecast_series)
    forecast_as_ofs = tuple(row.derived_completed_bar_end_utc for row in request.s26_forecast_series.forecast_rows)
    if len(request.vol_runtimes) != len(forecast_as_ofs):
        raise CarverBlocked("S27 V/Q/M runtime ledger requires exactly one runtime row per S26 forecast row")
    vol_by_as_of = _runtime_map_by_as_of("S27 volatility", request.vol_runtimes)
    if tuple(vol_by_as_of) != forecast_as_ofs:
        raise CarverBlocked("S27 V/Q/M runtime ledger timestamps must match S26 forecast row timestamps in order")
    for row in request.s26_forecast_series.forecast_rows:
        runtime = vol_by_as_of[row.derived_completed_bar_end_utc]
        runtime.validate(row.derived_completed_bar_end_utc)
        _validate_s27_runtime_identity("S27 V/Q/M runtime ledger row", runtime, row)
    result = S27VolAttenuationRuntimeLedgerResult(
        row_id=request.s26_forecast_series.row_id,
        author_market_code=request.s26_forecast_series.author_market_code,
        instrument_id=request.s26_forecast_series.instrument_id,
        raw_symbol=request.s26_forecast_series.raw_symbol,
        first_runtime_as_of=forecast_as_ofs[0],
        last_runtime_as_of=forecast_as_ofs[-1],
        input_s26_forecast_rows=len(request.s26_forecast_series.forecast_rows),
        vol_runtimes=tuple(vol_by_as_of[as_of] for as_of in forecast_as_ofs),
    )
    _validate_s27_vol_runtime_ledger_output(result)
    return result


def _s26_result_from_prices(prices: tuple[float, ...], as_of: datetime, sigma_percent: float) -> S26FastMeanReversionResult:
    current_price = prices[-1]
    equilibrium = _recursive_ewma(prices, S26_EQUILIBRIUM_EWMA_SPAN)
    return _s26_result_from_equilibrium(
        current_price=current_price,
        equilibrium=equilibrium,
        as_of=as_of,
        sigma_percent=sigma_percent,
    )


def _s26_result_from_equilibrium(
    *,
    current_price: float,
    equilibrium: float,
    as_of: datetime,
    sigma_percent: float,
) -> S26FastMeanReversionResult:
    require_finite_positive("S26 current price", current_price)
    require_finite_positive("S26 daily EWMA5 equilibrium", equilibrium)
    raw_forecast = equilibrium - current_price
    _require_finite("S26 raw forecast", raw_forecast)
    sigma_price = current_price * sigma_percent / 16.0
    require_finite_positive("S26 sigma price", sigma_price)
    risk_adjusted = raw_forecast / sigma_price
    _require_finite("S26 risk-adjusted forecast", risk_adjusted)
    scaled = risk_adjusted * S26_FORECAST_SCALAR
    capped = cap_forecast(scaled, FORECAST_CAP)
    return S26FastMeanReversionResult(
        as_of=as_of,
        current_price=current_price,
        equilibrium=equilibrium,
        raw_forecast=raw_forecast,
        sigma_price=sigma_price,
        risk_adjusted_forecast=risk_adjusted,
        scalar=S26_FORECAST_SCALAR,
        scaled_forecast=scaled,
        capped_forecast=capped,
    )


def _validate_synthetic_prices(
    prices: tuple[SyntheticHourlyPrice, ...],
    as_of: datetime,
    *,
    minimum_count: int,
) -> None:
    if len(prices) < minimum_count:
        raise CarverBlocked("S26/S27 synthetic hourly price history is insufficient")
    previous: datetime | None = None
    for point in prices:
        point.validate()
        if previous is not None and point.timestamp <= previous:
            raise CarverBlocked("S26/S27 synthetic hourly prices must be strictly increasing")
        if point.timestamp > as_of:
            raise CarverBlocked("S26/S27 synthetic hourly price history includes future rows")
        previous = point.timestamp
    if prices[-1].timestamp != as_of:
        raise CarverBlocked("S26/S27 forecast timestamp must be the last synthetic hourly price")


def _validate_quarantined_hourly_zn_bars(
    bars: tuple[S26QuarantinedHourlyZNBar, ...],
    as_of: datetime,
) -> None:
    if len(bars) < S26_EQUILIBRIUM_EWMA_SPAN:
        raise CarverBlocked("S26 quarantined hourly ZN history is insufficient")
    previous: datetime | None = None
    for bar in bars:
        bar.validate()
        if previous is not None and bar.derived_completed_bar_end_utc <= previous:
            raise CarverBlocked("S26 quarantined hourly ZN bars must be strictly increasing")
        if bar.derived_completed_bar_end_utc > as_of:
            raise CarverBlocked("S26 quarantined hourly ZN bars include future rows")
        previous = bar.derived_completed_bar_end_utc
    if bars[-1].derived_completed_bar_end_utc != as_of:
        raise CarverBlocked("S26 forecast timestamp must be the last completed ZN hourly bar")


def _validate_synthetic_quantiles(
    quantiles: tuple[SyntheticQuantilePoint, ...],
    as_of: datetime,
    *,
    minimum_count: int,
) -> None:
    if len(quantiles) < minimum_count:
        raise CarverBlocked("S27 synthetic volatility quantile history is insufficient")
    previous: datetime | None = None
    for point in quantiles:
        point.validate()
        if previous is not None and point.timestamp <= previous:
            raise CarverBlocked("S27 synthetic volatility quantiles must be strictly increasing")
        if point.timestamp > as_of:
            raise CarverBlocked("S27 synthetic volatility quantile history includes future rows")
        previous = point.timestamp
    if quantiles[-1].timestamp != as_of:
        raise CarverBlocked("S27 volatility quantile timestamp must align to forecast timestamp")


def _validate_timed_sigma_percent(sigma_percent: TimedValue, as_of: datetime) -> None:
    if sigma_percent.as_of != as_of:
        raise CarverBlocked("S26/S27 sigma percent timestamp must align to forecast timestamp")
    require_finite_positive("S26/S27 sigma percent", sigma_percent.value)


def _recursive_ewma(
    values: tuple[float, ...],
    span: int,
    *,
    require_positive_inputs: bool = True,
) -> float:
    if span < 2:
        raise CarverBlocked("EWMA span must be at least 2")
    alpha = 2.0 / (span + 1.0)
    smoothed = values[0]
    _validate_ewma_input(smoothed, require_positive_inputs=require_positive_inputs)
    for value in values[1:]:
        _validate_ewma_input(value, require_positive_inputs=require_positive_inputs)
        smoothed = alpha * value + (1.0 - alpha) * smoothed
    _require_finite("EWMA output", smoothed)
    return smoothed


def _validate_ewma_input(value: float, *, require_positive_inputs: bool) -> None:
    if require_positive_inputs:
        require_finite_positive("EWMA input", value)
    else:
        _require_finite("EWMA input", value)


def _validate_hourly_timestamp(timestamp: datetime) -> None:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise CarverBlocked("S26/S27 synthetic hourly timestamp must be timezone-aware")
    if timestamp.minute or timestamp.second or timestamp.microsecond:
        raise CarverBlocked("S26/S27 synthetic timestamp must be hour-aligned")


def _validate_real_hourly_timestamp(name: str, timestamp: datetime) -> None:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise CarverBlocked(f"{name} must be timezone-aware")
    if timestamp.minute or timestamp.second or timestamp.microsecond:
        raise CarverBlocked(f"{name} must be hour-aligned")


def _validate_no_strategy_outputs(
    prefix: str,
    fdm_used: bool,
    buffering_used: bool,
    performance_metrics: tuple[str, ...],
    position_outputs: tuple[str, ...],
) -> None:
    if fdm_used:
        raise CarverBlocked(f"{prefix} fast mean reversion must not use FDM")
    if buffering_used:
        raise CarverBlocked(f"{prefix} fast mean reversion must not use buffering")
    if performance_metrics or position_outputs:
        raise CarverBlocked(f"{prefix} synthetic conformance must not emit performance or position outputs")


def _validate_forecast_only_output(result: S26QuarantinedHourlyForecastResult) -> None:
    if result.forecast_output_status != S26_FORECAST_ONLY_STATUS:
        raise CarverBlocked("S26 real-hourly output must remain forecast-only")
    if result.diagnostics_outputs or result.backtest_outputs or result.position_outputs:
        raise CarverBlocked("S26 real-hourly forecast output must not emit diagnostics, backtests, or positions")
    _require_exact("S26 daily equilibrium runtime status", result.equilibrium_runtime_status, S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS)
    _require_exact("S26 daily equilibrium method status", result.equilibrium_method_status, S26_DAILY_EQUILIBRIUM_METHOD_STATUS)
    _require_sha256_text("S26 daily equilibrium source artifact sha256", result.equilibrium_source_artifact_sha256)


def _validate_s26_forecast_row_for_s27_handoff(result: S26QuarantinedHourlyForecastResult) -> None:
    _validate_forecast_only_output(result)
    _require_exact("S27 handoff S26 row id", result.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
    _require_exact("S27 handoff S26 author market code", result.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
    if result.instrument_id != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
        raise CarverBlocked("S27 handoff S26 forecast row must use Databento instrument_id 42000661")
    _require_exact("S27 handoff S26 raw symbol", result.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
    _require_exact("S27 handoff S26 source lock status", result.source_locks_status, "LOCKED_QUARANTINE_HOURLY_ZN_S26_FORECAST_ONLY")
    _validate_real_hourly_timestamp("S27 handoff S26 forecast as_of", result.derived_completed_bar_end_utc)
    require_finite_positive("S27 handoff S26 close", result.price_close)
    require_finite_positive("S27 handoff S26 sigma price", result.sigma_price)
    _require_finite("S27 handoff S26 raw forecast", result.raw_forecast)


def _validate_forecast_series_only_output(result: S26QuarantinedHourlyForecastSeriesResult) -> None:
    if result.series_output_status != S26_ZN_FORECAST_SERIES_STATUS:
        raise CarverBlocked("S26 real-hourly series output must remain forecast-series-only")
    if not result.forecast_rows:
        raise CarverBlocked("S26 real-hourly series output must contain forecast rows")
    if result.diagnostics_outputs or result.backtest_outputs or result.position_outputs:
        raise CarverBlocked("S26 real-hourly forecast series must not emit diagnostics, backtests, or positions")
    _require_exact("S26 forecast series row id", result.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
    _require_exact("S26 forecast series author market code", result.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
    if result.instrument_id != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
        raise CarverBlocked("S26 forecast series must use Databento instrument_id 42000661")
    _require_exact("S26 forecast series raw symbol", result.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
    previous: datetime | None = None
    for row in result.forecast_rows:
        _validate_forecast_only_output(row)
        _validate_s26_forecast_row_for_s27_handoff(row)
        if previous is not None and row.derived_completed_bar_end_utc <= previous:
            raise CarverBlocked("S26 real-hourly forecast series rows must be strictly increasing")
        previous = row.derived_completed_bar_end_utc


def _validate_s27_forecast_only_output(result: S27QuarantinedHourlyForecastResult) -> None:
    if result.forecast_output_status != S27_FORECAST_ONLY_STATUS:
        raise CarverBlocked("S27 real-hourly output must remain forecast-only")
    if result.source_locks_status != S27_FORECAST_HANDOFF_STATUS:
        raise CarverBlocked("S27 real-hourly source lock status drifted")
    if result.diagnostics_outputs or result.backtest_outputs or result.position_outputs:
        raise CarverBlocked("S27 real-hourly forecast output must not emit diagnostics, backtests, or positions")
    _require_finite("S27 real-hourly adjusted raw forecast", result.adjusted_raw_forecast)
    _require_finite("S27 real-hourly scaled forecast", result.scaled_forecast)
    if abs(result.capped_forecast) > FORECAST_CAP:
        raise CarverBlocked("S27 real-hourly capped forecast exceeded Carver cap")


def _validate_s27_forecast_series_only_output(result: S27QuarantinedHourlyForecastSeriesResult) -> None:
    if result.series_output_status != S27_FORECAST_SERIES_STATUS:
        raise CarverBlocked("S27 real-hourly series output must remain forecast-series-only")
    if not result.forecast_rows:
        raise CarverBlocked("S27 real-hourly series output must contain forecast rows")
    if result.diagnostics_outputs or result.backtest_outputs or result.position_outputs:
        raise CarverBlocked("S27 real-hourly forecast series must not emit diagnostics, backtests, or positions")
    _require_exact("S27 forecast series row id", result.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
    _require_exact("S27 forecast series author market code", result.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
    if result.instrument_id != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
        raise CarverBlocked("S27 forecast series must use Databento instrument_id 42000661")
    _require_exact("S27 forecast series raw symbol", result.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
    previous: datetime | None = None
    for row in result.forecast_rows:
        _validate_s27_forecast_only_output(row)
        if previous is not None and row.as_of <= previous:
            raise CarverBlocked("S27 real-hourly forecast series rows must be strictly increasing")
        previous = row.as_of


def _validate_s27_trend_runtime_ledger_output(result: S27TrendOverlayRuntimeLedgerResult) -> None:
    if result.ledger_status != S27_TREND_RUNTIME_LEDGER_STATUS:
        raise CarverBlocked("S27 EWMAC16 trend runtime ledger status drifted")
    if not result.trend_runtimes:
        raise CarverBlocked("S27 EWMAC16 trend runtime ledger must contain runtime rows")
    if result.diagnostics_outputs or result.backtest_outputs or result.position_outputs:
        raise CarverBlocked("S27 EWMAC16 trend runtime ledger must not emit diagnostics, backtests, or positions")
    _require_exact("S27 trend runtime ledger row id", result.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
    _require_exact("S27 trend runtime ledger author market code", result.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
    if result.instrument_id != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
        raise CarverBlocked("S27 trend runtime ledger must use Databento instrument_id 42000661")
    _require_exact("S27 trend runtime ledger raw symbol", result.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
    previous: datetime | None = None
    for runtime in result.trend_runtimes:
        if previous is not None and runtime.as_of <= previous:
            raise CarverBlocked("S27 trend runtime ledger rows must be strictly increasing")
        previous = runtime.as_of


def _validate_s27_vol_runtime_ledger_output(result: S27VolAttenuationRuntimeLedgerResult) -> None:
    if result.ledger_status != S27_VOL_ATTENUATION_RUNTIME_LEDGER_STATUS:
        raise CarverBlocked("S27 V/Q/M runtime ledger status drifted")
    if not result.vol_runtimes:
        raise CarverBlocked("S27 V/Q/M runtime ledger must contain runtime rows")
    if result.diagnostics_outputs or result.backtest_outputs or result.position_outputs:
        raise CarverBlocked("S27 V/Q/M runtime ledger must not emit diagnostics, backtests, or positions")
    _require_exact("S27 V/Q/M runtime ledger row id", result.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
    _require_exact("S27 V/Q/M runtime ledger author market code", result.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
    if result.instrument_id != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
        raise CarverBlocked("S27 V/Q/M runtime ledger must use Databento instrument_id 42000661")
    _require_exact("S27 V/Q/M runtime ledger raw symbol", result.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
    previous: datetime | None = None
    for runtime in result.vol_runtimes:
        if previous is not None and runtime.as_of <= previous:
            raise CarverBlocked("S27 V/Q/M runtime ledger rows must be strictly increasing")
        previous = runtime.as_of


def _runtime_map_by_as_of(name: str, runtimes: tuple[S27TrendOverlayRuntimeValue | S27VolAttenuationRuntimeValue, ...]):
    runtime_by_as_of = {}
    for runtime in runtimes:
        if runtime.as_of in runtime_by_as_of:
            raise CarverBlocked(f"{name} runtimes must be unique by as_of")
        runtime_by_as_of[runtime.as_of] = runtime
    return runtime_by_as_of


def _validate_s27_runtime_identity(
    name: str,
    runtime: S27TrendOverlayRuntimeValue | S27VolAttenuationRuntimeValue,
    s26_forecast: S26QuarantinedHourlyForecastResult | S26DailyEquilibriumRuntimeValue,
) -> None:
    _require_exact(f"{name} row id", runtime.row_id, s26_forecast.row_id)
    _require_exact(f"{name} author market code", runtime.author_market_code, s26_forecast.author_market_code)
    if runtime.instrument_id != s26_forecast.instrument_id:
        raise CarverBlocked(f"{name} instrument id must match S26 forecast row")
    _require_exact(f"{name} raw symbol", runtime.raw_symbol, s26_forecast.raw_symbol)


def _validate_s26_daily_equilibrium_identity(
    runtime: S26DailyEquilibriumRuntimeValue,
    bar: S26QuarantinedHourlyZNBar,
) -> None:
    _require_exact("S26 daily equilibrium row id", runtime.row_id, bar.row_id)
    _require_exact("S26 daily equilibrium author market code", runtime.author_market_code, bar.author_market_code)
    if runtime.instrument_id != bar.instrument_id:
        raise CarverBlocked("S26 daily equilibrium instrument id must match S26 hourly forecast row")
    _require_exact("S26 daily equilibrium raw symbol", runtime.raw_symbol, bar.raw_symbol)


def _validate_ohlcv_shape(open_price: float, high: float, low: float, close: float, volume: float) -> None:
    require_finite_positive("S26 raw row open", open_price)
    require_finite_positive("S26 raw row high", high)
    require_finite_positive("S26 raw row low", low)
    require_finite_positive("S26 raw row close", close)
    _require_finite_nonnegative("S26 raw row volume", volume)
    if high < low:
        raise CarverBlocked("S26 raw row high must be greater than or equal to low")
    if high < open_price or high < close:
        raise CarverBlocked("S26 raw row high must bound open and close")
    if low > open_price or low > close:
        raise CarverBlocked("S26 raw row low must bound open and close")


def _validate_s26_zn_hourly_csv_header(fieldnames: list[str] | None) -> None:
    if fieldnames is None:
        raise CarverBlocked("S26 ZN CSV text is missing a header")
    missing = [column for column in S26_ZN_DATABENTO_OHLCV_1H_REQUIRED_COLUMNS if column not in fieldnames]
    if missing:
        raise CarverBlocked(f"S26 ZN CSV text is missing required columns: {', '.join(missing)}")


def _validate_quarantined_hourly_ohlcv_sequence(bars: tuple[S26QuarantinedHourlyOHLCVBar, ...]) -> None:
    previous: datetime | None = None
    for bar in bars:
        if previous is not None and bar.provider_ts_event_start_utc <= previous:
            raise CarverBlocked("S26 ZN normalized hourly bars must be strictly increasing by ts_event")
        previous = bar.provider_ts_event_start_utc


def _validate_quarantined_hourly_ohlcv_bars_for_handoff(
    bars: tuple[S26QuarantinedHourlyOHLCVBar, ...],
    as_of: datetime,
) -> None:
    if len(bars) < S26_EQUILIBRIUM_EWMA_SPAN:
        raise CarverBlocked("S26 G_R1B hourly OHLCV history is insufficient")
    _validate_real_hourly_timestamp("S26 G_R1B as_of", as_of)
    _validate_quarantined_hourly_ohlcv_sequence(bars)
    for bar in bars:
        if bar.lane_class is not LaneClass.SOURCE_NATIVE_FUTURES:
            raise CarverBlocked("S26 G_R1B requires SOURCE_NATIVE_FUTURES bars")
        _require_exact("S26 G_R1B row provider", bar.provider, S26_ZN_DATABENTO_PROVIDER)
        _require_exact("S26 G_R1B row dataset", bar.dataset, S26_ZN_DATABENTO_DATASET)
        _require_exact("S26 G_R1B row schema", bar.schema, S26_ZN_DATABENTO_SCHEMA)
        _require_exact("S26 G_R1B row id", bar.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        _require_exact("S26 G_R1B row author market code", bar.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
        if bar.instrument_id != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
            raise CarverBlocked("S26 G_R1B requires Databento instrument_id 42000661")
        _require_exact("S26 G_R1B row raw symbol", bar.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
        _require_exact("S26 G_R1B row shape status", bar.row_shape_status, "PASS_OHLCV_1H_ROW_SHAPE")
        _require_exact("S26 G_R1B provider condition", bar.provider_condition_status, "PROVIDER_CONDITION_AVAILABLE")
        if bar.strategy_use_status != S26_ZN_HOURLY_QUARANTINE_STATUS:
            raise CarverBlocked("S26 G_R1B only promotes quarantine-only rows")
        if bar.derived_completed_bar_end_utc - bar.provider_ts_event_start_utc != timedelta(hours=1):
            raise CarverBlocked("S26 G_R1B completed-bar end must equal ts_event plus one hour")
        _validate_ohlcv_shape(bar.open, bar.high, bar.low, bar.close, bar.volume)
    if bars[-1].derived_completed_bar_end_utc != as_of:
        raise CarverBlocked("S26 G_R1B as_of must match the last completed hourly bar")


def _parse_utc_hourly_timestamp(value: str, name: str) -> datetime:
    require_non_empty_text(name, value)
    timestamp = _parse_iso_utc_timestamp(value)
    _validate_real_hourly_timestamp(name, timestamp)
    if timestamp.utcoffset() != timedelta(0):
        raise CarverBlocked(f"{name} must be UTC")
    return timestamp


def _parse_iso_utc_timestamp(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    if "." in normalized:
        prefix, suffix = normalized.split(".", 1)
        if "+" in suffix:
            fractional, offset = suffix.split("+", 1)
            normalized = f"{prefix}.{fractional[:6].ljust(6, '0')}+{offset}"
        elif "-" in suffix:
            fractional, offset = suffix.split("-", 1)
            normalized = f"{prefix}.{fractional[:6].ljust(6, '0')}-{offset}"
    try:
        timestamp = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise CarverBlocked("S26 ZN CSV timestamp is not ISO-8601 UTC") from exc
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise CarverBlocked("S26 ZN CSV timestamp must be timezone-aware")
    return timestamp.astimezone(timezone.utc)


def _parse_int(value: str, name: str) -> int:
    require_non_empty_text(name, value)
    try:
        return int(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be an integer") from exc


def _parse_float(value: str, name: str) -> float:
    require_non_empty_text(name, value)
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be numeric") from exc
    _require_finite(name, parsed)
    return parsed


def _require_exact(name: str, actual: str, expected: str) -> None:
    require_non_empty_text(name, actual)
    if actual != expected:
        raise CarverBlocked(f"{name} must be {expected}")


def _require_exact_datetime(name: str, actual: datetime, expected: datetime) -> None:
    _validate_real_hourly_timestamp(name, actual)
    if actual != expected:
        raise CarverBlocked(f"{name} must be {expected.isoformat()}")


def _validate_no_authorization_manifest(no_authorization: tuple[str, ...]) -> None:
    required = {
        "NO_PROVIDER_API_ACCESS",
        "NO_DATA_DOWNLOAD",
        "NO_MARKET_ROW_PARSING",
        "NO_DIAGNOSTICS",
        "NO_BACKTESTS",
        "NO_FORECAST_COMPUTATION",
        "NO_POSITIONS",
        "NO_GIT_OPERATIONS",
    }
    observed = set(no_authorization)
    if not required.issubset(observed):
        missing = ", ".join(sorted(required - observed))
        raise CarverBlocked(f"S26 ZN request manifest no-authorization list is missing: {missing}")


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")


def _require_finite_nonnegative(name: str, value: float) -> None:
    _require_finite(name, value)
    if value < 0.0:
        raise CarverBlocked(f"{name} must be non-negative")


def _require_sha256_text(name: str, value: str) -> None:
    require_non_empty_text(name, value)
    normalized = value.strip()
    if len(normalized) != 64 or any(character not in "0123456789abcdefABCDEF" for character in normalized):
        raise CarverBlocked(f"{name} must be a SHA-256 hex digest")

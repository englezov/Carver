from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import StrEnum
from math import isfinite
from numbers import Integral, Real

from .m0 import CarverBlocked, LaneClass, require_finite_positive, require_non_empty_text, require_source_native
from .m1 import RoundingPolicy
from .m2 import FORECAST_CAP, cap_forecast


S27_V2_LANE_CLASS = LaneClass.SOURCE_NATIVE_FUTURES
S26_V2_EQUILIBRIUM_EWMA_SPAN = 5
S26_V2_FORECAST_SCALAR = 9.3
S27_V2_FORECAST_SCALAR_BOOK_TEXT = "AROUND_20"
S27_V2_FORECAST_SCALAR = 20.0
S27_V2_TREND_FAST_SPAN = 16
S27_V2_TREND_SLOW_SPAN = 64
S27_V2_VQM_EWMA_SPAN = 10
S27_V2_TEN_YEAR_SIGMA_ROWS = 2560
S27_V2_FORECAST_TO_POSITION_DIVISOR = 10.0
S27_V2_SOURCE_LOCK_STATUS = "S27_ZN_BOOK_SOURCE_LOCK_PASSED_FOR_V2_IMPLEMENTATION_EXERCISE"
S27_V2_DIAGNOSTIC_LABEL = "S27_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_NOT_BACKTEST"
S27_V2_DAILY_ROW_READY_STATUS = "LOCAL_SYNTHETIC_OR_PREVALIDATED_COMPLETED_DAILY_ROW"
S27_V2_HOURLY_ROW_READY_STATUS = "LOCAL_SYNTHETIC_OR_PREVALIDATED_COMPLETED_HOURLY_ROW"
S27_V2_LEVEL_COMPATIBILITY_STATUS = "DAILY_CONTINUOUS_HOURLY_CURRENT_LEVEL_COMPATIBILITY_PREVALIDATED"
S27_V2_UNSPECIFIED_DAILY_ROW_STATUS = "UNSPECIFIED_DAILY_ROW_STATUS_FAIL_CLOSED"
S27_V2_UNSPECIFIED_HOURLY_ROW_STATUS = "UNSPECIFIED_HOURLY_ROW_STATUS_FAIL_CLOSED"
S27_V2_UNSPECIFIED_LEVEL_COMPATIBILITY_STATUS = "UNSPECIFIED_LEVEL_COMPATIBILITY_STATUS_FAIL_CLOSED"
S27_V2_ANNUAL_PERCENTAGE_SIGMA_SOURCE_STATUS = "STRATEGY3_OR_PREVALIDATED_ANNUAL_PERCENTAGE_SIGMA_SOURCE_LOCKED"
S27_V2_UNSPECIFIED_SIGMA_SOURCE_STATUS = "UNSPECIFIED_ANNUAL_PERCENTAGE_SIGMA_SOURCE_FAIL_CLOSED"
S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS = (
    "CALLER_CERTIFIED_LATEST_STRICT_PRIOR_DAILY_RUNTIME"
)
S27_V2_UNSPECIFIED_DAILY_RUNTIME_SELECTION_STATUS = (
    "UNSPECIFIED_DAILY_RUNTIME_SELECTION_STATUS_FAIL_CLOSED"
)
S27_V2_FILL_SOURCE_STATUS = "S27_V2_FILL_FROM_VALIDATED_ORDER_PLAN_ONE_HOUR_LAG"
S27_V2_EXTERNAL_FILL_UNPROVEN_STATUS = "S27_V2_EXTERNAL_FILL_UNPROVEN"
S27_V2_COST_SOURCE_STATUS = "S27_V2_COST_FROM_VALIDATED_FILL_LEDGER"
S27_V2_EXTERNAL_COST_UNPROVEN_STATUS = "S27_V2_EXTERNAL_COST_UNPROVEN"
S27_V2_PNL_SOURCE_STATUS = "S27_V2_PNL_FROM_VALIDATED_REPLAY_STEP"
S27_V2_EXTERNAL_PNL_UNPROVEN_STATUS = "S27_V2_EXTERNAL_PNL_UNPROVEN"


class S27V2OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class S27V2OrderKind(StrEnum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"


class S27V2FillCostTreatment(StrEnum):
    COMMISSION_ONLY = "COMMISSION_ONLY"
    COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD = "COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD"


class S27V2SessionTransitionKind(StrEnum):
    NORMAL_ONE_HOUR = "NORMAL_ONE_HOUR"
    END_OF_DAY_CANCEL_RESET = "END_OF_DAY_CANCEL_RESET"
    OVERNIGHT_GAP_MARKET_RESET = "OVERNIGHT_GAP_MARKET_RESET"
    ROLL_BOUNDARY = "ROLL_BOUNDARY"


S27_V2_NO_ROLL_BOUNDARY_STATUS = "NO_ROLL_BOUNDARY"
S27_V2_ROLL_STATE_RESET_ASSUMPTION_STATUS = "ROLL_BOUNDARY_STATE_RESET_IMPLEMENTATION_ASSUMPTION_LOCKED"
S27_V2_ALLOWED_MARKET_ORDER_TRIGGERS = frozenset(
    {
        "DESIRED_POSITION_MORE_THAN_ONE_CONTRACT_FROM_CURRENT",
        "CAP_BOUND_NO_BUY_LIMIT_SIDE",
        "CAP_BOUND_NO_SELL_LIMIT_SIDE",
        "CAP_BOUND_NO_ADJACENT_LIMIT_SIDE",
        "ADJACENT_DESIRED_TARGET_UNPRICEABLE_AT_CAP",
    }
)


@dataclass(frozen=True)
class S27V2SourceLock:
    status: str = S27_V2_SOURCE_LOCK_STATUS
    lane_class: LaneClass = S27_V2_LANE_CLASS
    scalar_book_text: str = S27_V2_FORECAST_SCALAR_BOOK_TEXT
    scalar_implementation_freeze: float = S27_V2_FORECAST_SCALAR
    no_provider_api: bool = True
    no_data_download: bool = True
    no_backtest: bool = True
    no_oos_lockbox_forward: bool = True

    def validate(self) -> None:
        require_source_native(self.lane_class)
        _require_exact("S27 v2 source-lock status", self.status, S27_V2_SOURCE_LOCK_STATUS)
        _require_exact("S27 v2 scalar book text", self.scalar_book_text, S27_V2_FORECAST_SCALAR_BOOK_TEXT)
        _require_close("S27 v2 scalar implementation freeze", self.scalar_implementation_freeze, S27_V2_FORECAST_SCALAR)
        if not (self.no_provider_api and self.no_data_download and self.no_backtest and self.no_oos_lockbox_forward):
            raise CarverBlocked("S27 v2 implementation exercise must preserve non-authorization boundaries")


@dataclass(frozen=True)
class S27V2DailyRuntimeInput:
    completed_trading_date: str
    completed_bar_timestamp: datetime
    continuous_close: float
    current_traded_contract_close: float
    annual_percentage_sigma: float
    source_status: str = S27_V2_UNSPECIFIED_DAILY_ROW_STATUS
    level_compatibility_status: str = S27_V2_UNSPECIFIED_LEVEL_COMPATIBILITY_STATUS
    annual_percentage_sigma_source_status: str = S27_V2_UNSPECIFIED_SIGMA_SOURCE_STATUS

    def validate(self) -> None:
        require_non_empty_text("S27 v2 daily completed trading date", self.completed_trading_date)
        _validate_iso_date("S27 v2 daily completed trading date", self.completed_trading_date)
        _validate_utc_timestamp("S27 v2 daily completed bar timestamp", self.completed_bar_timestamp)
        if (
            self.completed_bar_timestamp.hour
            or self.completed_bar_timestamp.minute
            or self.completed_bar_timestamp.second
            or self.completed_bar_timestamp.microsecond
        ):
            raise CarverBlocked("S27 v2 daily row must be date-aligned")
        require_finite_positive("S27 v2 daily continuous close", self.continuous_close)
        require_finite_positive("S27 v2 current traded contract close", self.current_traded_contract_close)
        require_finite_positive("S27 v2 annual percentage sigma", self.annual_percentage_sigma)
        _require_exact("S27 v2 daily row source status", self.source_status, S27_V2_DAILY_ROW_READY_STATUS)
        _require_exact(
            "S27 v2 annual percentage sigma source status",
            self.annual_percentage_sigma_source_status,
            S27_V2_ANNUAL_PERCENTAGE_SIGMA_SOURCE_STATUS,
        )
        _require_exact(
            "S27 v2 daily/hourly level compatibility status",
            self.level_compatibility_status,
            S27_V2_LEVEL_COMPATIBILITY_STATUS,
        )


@dataclass(frozen=True)
class S27V2HourlyRuntimeInput:
    completed_bar_end_utc: datetime
    completed_trading_date: str
    raw_symbol: str
    open: float
    high: float
    low: float
    close: float
    provider_condition_status: str = S27_V2_UNSPECIFIED_HOURLY_ROW_STATUS

    def validate(self) -> None:
        _validate_utc_hour("S27 v2 hourly completed bar end", self.completed_bar_end_utc)
        require_non_empty_text("S27 v2 hourly completed trading date", self.completed_trading_date)
        _validate_iso_date("S27 v2 hourly completed trading date", self.completed_trading_date)
        require_non_empty_text("S27 v2 hourly raw symbol", self.raw_symbol)
        _validate_ohlc(self.open, self.high, self.low, self.close)
        _require_exact(
            "S27 v2 hourly provider condition status",
            self.provider_condition_status,
            S27_V2_HOURLY_ROW_READY_STATUS,
        )


@dataclass(frozen=True)
class S27V2DailyRuntimeRow:
    completed_trading_date: str
    current_traded_contract_close: float
    equilibrium_ewma5: float
    trend_fast_ewma16: float
    trend_slow_ewma64: float
    trend_forecast: float
    annual_percentage_sigma: float
    ten_year_sigma_mean: float
    relative_volatility_v: float
    quantile_q: float
    raw_vol_multiplier: float
    vol_multiplier_m: float
    sigma_source_observation_count: int
    q_source_observation_count: int
    level_compatibility_status: str
    annual_percentage_sigma_source_status: str


@dataclass(frozen=True)
class S27V2ForecastReplayRow:
    as_of: datetime
    completed_trading_date: str
    raw_symbol: str
    hourly_current_price: float
    equilibrium_ewma5: float
    raw_forecast: float
    previous_completed_daily_close_current_traded_contract: float
    annual_percentage_sigma: float
    sigma_price: float
    risk_adjusted_forecast_before_veto: float
    trend_forecast: float
    trend_veto_applied: bool
    risk_adjusted_forecast_after_veto: float
    vol_multiplier_m: float
    adjusted_risk_adjusted_forecast: float
    scalar_book_text: str
    scalar: float
    scaled_forecast: float
    capped_forecast: float
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2DesiredPositionRow:
    as_of: datetime
    capped_forecast: float
    base_position_contracts: float
    desired_unrounded_contracts: float
    desired_rounded_contracts: int
    rounding_policy: RoundingPolicy
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2ForecastContext:
    as_of: datetime
    equilibrium_ewma5: float
    sigma_price: float
    vol_multiplier_m: float
    scalar: float
    base_position_contracts: float
    capped_forecast: float
    trend_forecast: float

    def validate(self) -> None:
        _validate_utc_hour("S27 v2 forecast context as_of", self.as_of)
        require_finite_positive("S27 v2 forecast context equilibrium", self.equilibrium_ewma5)
        require_finite_positive("S27 v2 forecast context sigma price", self.sigma_price)
        require_finite_positive("S27 v2 forecast context volatility multiplier", self.vol_multiplier_m)
        require_finite_positive("S27 v2 forecast context scalar", self.scalar)
        require_finite_positive("S27 v2 forecast context base position", self.base_position_contracts)
        _require_finite("S27 v2 forecast context capped forecast", self.capped_forecast)
        _require_finite("S27 v2 forecast context trend forecast", self.trend_forecast)
        if self.trend_forecast == 0.0:
            raise CarverBlocked("S27 v2 forecast context zero trend is fail-closed")
        if abs(self.scalar - S27_V2_FORECAST_SCALAR) > 1e-12:
            raise CarverBlocked("S27 v2 forecast context scalar must match source lock")
        if abs(self.capped_forecast) > FORECAST_CAP:
            raise CarverBlocked("S27 v2 forecast context capped forecast exceeds cap")
        if self.trend_forecast > 0.0 and self.capped_forecast < 0.0:
            raise CarverBlocked("S27 v2 uptrend context cannot carry short capped forecast")
        if self.trend_forecast < 0.0 and self.capped_forecast > 0.0:
            raise CarverBlocked("S27 v2 downtrend context cannot carry long capped forecast")


@dataclass(frozen=True)
class S27V2LimitOrderRow:
    decision_as_of: datetime
    side: S27V2OrderSide
    quantity: int
    target_position_after_fill: int
    limit_price: float
    cost_treatment: S27V2FillCostTreatment = S27V2FillCostTreatment.COMMISSION_ONLY
    order_kind: S27V2OrderKind = S27V2OrderKind.LIMIT


@dataclass(frozen=True)
class S27V2MarketOrderRow:
    decision_as_of: datetime
    side: S27V2OrderSide
    quantity: int
    target_position_after_fill: int
    trigger: str
    cost_treatment: S27V2FillCostTreatment = S27V2FillCostTreatment.COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD
    order_kind: S27V2OrderKind = S27V2OrderKind.MARKET


@dataclass(frozen=True)
class S27V2OrderPlan:
    decision_as_of: datetime
    current_position: int
    desired_rounded_position: int
    limit_orders: tuple[S27V2LimitOrderRow, ...]
    market_orders: tuple[S27V2MarketOrderRow, ...]
    end_of_day_cancel_reset_required: bool
    forecast_context: S27V2ForecastContext | None = None
    raw_symbol: str | None = None
    session_id: str | None = None
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2WorkingOrderState:
    opened_as_of: datetime
    session_id: str
    raw_symbol: str
    current_position: int
    desired_rounded_position: int
    limit_orders: tuple[S27V2LimitOrderRow, ...]
    market_orders: tuple[S27V2MarketOrderRow, ...]
    forecast_context: S27V2ForecastContext | None = None
    state_status: str = "S27_V2_WORKING_ORDER_STATE_OPEN"


@dataclass(frozen=True)
class S27V2FillRow:
    decision_as_of: datetime
    fill_as_of: datetime
    side: S27V2OrderSide
    quantity: int
    fill_price: float
    order_kind: S27V2OrderKind
    cost_treatment: S27V2FillCostTreatment
    commission_cost: float
    spread_cost: float
    total_cost: float
    fill_source_status: str = S27_V2_EXTERNAL_FILL_UNPROVEN_STATUS


@dataclass(frozen=True)
class S27V2CostLedgerRow:
    as_of: datetime
    order_kind: S27V2OrderKind
    side: S27V2OrderSide
    quantity: int
    commission_cost: float
    spread_cost: float
    total_cost: float
    cost_treatment: S27V2FillCostTreatment
    cost_source_status: str = S27_V2_EXTERNAL_COST_UNPROVEN_STATUS


@dataclass(frozen=True)
class S27V2PnlLedgerRow:
    start_as_of: datetime
    end_as_of: datetime
    starting_position: int
    start_price: float
    end_price: float
    contract_multiplier: float
    gross_pnl: float
    total_cost: float
    net_pnl: float
    pnl_source_status: str = S27_V2_EXTERNAL_PNL_UNPROVEN_STATUS
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2SourceInputManifestRow:
    as_of: datetime
    daily_completed_trading_date: str
    daily_completed_bar_timestamp: datetime
    daily_continuous_close: float
    daily_current_traded_contract_close: float
    daily_annual_percentage_sigma: float
    daily_annual_percentage_sigma_source_status: str
    hourly_completed_trading_date: str
    hourly_completed_bar_end_utc: datetime
    raw_symbol: str
    hourly_open: float
    hourly_high: float
    hourly_low: float
    hourly_close: float
    fill_hourly_completed_trading_date: str
    fill_hourly_completed_bar_end_utc: datetime
    fill_raw_symbol: str
    fill_hourly_open: float
    fill_hourly_high: float
    fill_hourly_low: float
    fill_hourly_close: float
    daily_source_status: str
    hourly_provider_condition_status: str
    fill_hourly_provider_condition_status: str
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2LevelCompatibilityLedgerRow:
    as_of: datetime
    daily_completed_trading_date: str
    hourly_completed_trading_date: str
    daily_continuous_close: float
    daily_current_traded_contract_close: float
    hourly_current_price: float
    sigma_bridge_price: float
    annual_percentage_sigma: float
    annual_percentage_sigma_source_status: str
    level_compatibility_status: str
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2CostComponentLedgerRow:
    as_of: datetime
    order_kind: S27V2OrderKind
    side: S27V2OrderSide
    quantity: int
    cost_component: str
    amount: float
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2ValidationLedgerRow:
    as_of: datetime
    validation_name: str
    validation_status: str
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2ProvenanceHashLedgerRow:
    as_of: datetime
    artifact_family: str
    row_index: int
    sha256: str
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2ReplayStepLedgerBundle:
    source_input_manifest_rows: tuple[S27V2SourceInputManifestRow, ...]
    level_compatibility_ledger_rows: tuple[S27V2LevelCompatibilityLedgerRow, ...]
    daily_runtime_rows: tuple[S27V2DailyRuntimeRow, ...]
    forecast_replay_rows: tuple[S27V2ForecastReplayRow, ...]
    desired_position_rows: tuple[S27V2DesiredPositionRow, ...]
    order_plan_rows: tuple[S27V2OrderPlan, ...]
    working_transition_rows: tuple[S27V2WorkingOrderTransitionResult, ...]
    limit_order_rows: tuple[S27V2LimitOrderRow, ...]
    market_order_rows: tuple[S27V2MarketOrderRow, ...]
    remaining_limit_order_rows: tuple[S27V2LimitOrderRow, ...]
    canceled_limit_order_rows: tuple[S27V2LimitOrderRow, ...]
    fill_rows: tuple[S27V2FillRow, ...]
    cost_ledger_rows: tuple[S27V2CostLedgerRow, ...]
    commission_ledger_rows: tuple[S27V2CostComponentLedgerRow, ...]
    spread_cost_ledger_rows: tuple[S27V2CostComponentLedgerRow, ...]
    pnl_ledger_rows: tuple[S27V2PnlLedgerRow, ...]
    validation_ledger_rows: tuple[S27V2ValidationLedgerRow, ...]
    provenance_hash_ledger_rows: tuple[S27V2ProvenanceHashLedgerRow, ...]
    final_position: int
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2ReplayRunLedgerBundle:
    step_bundles: tuple[S27V2ReplayStepLedgerBundle, ...]
    source_input_manifest_rows: tuple[S27V2SourceInputManifestRow, ...]
    level_compatibility_ledger_rows: tuple[S27V2LevelCompatibilityLedgerRow, ...]
    daily_runtime_rows: tuple[S27V2DailyRuntimeRow, ...]
    forecast_replay_rows: tuple[S27V2ForecastReplayRow, ...]
    desired_position_rows: tuple[S27V2DesiredPositionRow, ...]
    order_plan_rows: tuple[S27V2OrderPlan, ...]
    working_transition_rows: tuple[S27V2WorkingOrderTransitionResult, ...]
    limit_order_rows: tuple[S27V2LimitOrderRow, ...]
    market_order_rows: tuple[S27V2MarketOrderRow, ...]
    remaining_limit_order_rows: tuple[S27V2LimitOrderRow, ...]
    canceled_limit_order_rows: tuple[S27V2LimitOrderRow, ...]
    fill_rows: tuple[S27V2FillRow, ...]
    cost_ledger_rows: tuple[S27V2CostLedgerRow, ...]
    commission_ledger_rows: tuple[S27V2CostComponentLedgerRow, ...]
    spread_cost_ledger_rows: tuple[S27V2CostComponentLedgerRow, ...]
    pnl_ledger_rows: tuple[S27V2PnlLedgerRow, ...]
    validation_ledger_rows: tuple[S27V2ValidationLedgerRow, ...]
    provenance_hash_ledger_rows: tuple[S27V2ProvenanceHashLedgerRow, ...]
    initial_position: int
    final_position: int
    replay_step_count: int
    row_status: str = S27_V2_DIAGNOSTIC_LABEL


@dataclass(frozen=True)
class S27V2WorkingOrderTransitionResult:
    transition_kind: S27V2SessionTransitionKind
    prior_state: S27V2WorkingOrderState
    fills: tuple[S27V2FillRow, ...]
    next_position: int
    remaining_limit_orders: tuple[S27V2LimitOrderRow, ...]
    canceled_limit_orders: tuple[S27V2LimitOrderRow, ...]
    market_orders: tuple[S27V2MarketOrderRow, ...]
    roll_handling_status: str
    transition_status: str = S27_V2_DIAGNOSTIC_LABEL


def build_s27_v2_daily_runtime_rows(
    daily_rows: tuple[S27V2DailyRuntimeInput, ...],
    *,
    source_lock: S27V2SourceLock = S27V2SourceLock(),
) -> tuple[S27V2DailyRuntimeRow, ...]:
    source_lock.validate()
    _validate_daily_sequence(daily_rows)
    closes = tuple(row.continuous_close for row in daily_rows)
    sigmas = tuple(row.annual_percentage_sigma for row in daily_rows)
    equilibrium = _ewma_series(closes, S26_V2_EQUILIBRIUM_EWMA_SPAN)
    trend_fast = _ewma_series(closes, S27_V2_TREND_FAST_SPAN)
    trend_slow = _ewma_series(closes, S27_V2_TREND_SLOW_SPAN)
    v_values: list[float] = []
    raw_multipliers: list[float] = []
    m_values: list[float] = []
    output: list[S27V2DailyRuntimeRow] = []
    for index, row in enumerate(daily_rows):
        sigma_window = sigmas[max(0, index - S27_V2_TEN_YEAR_SIGMA_ROWS + 1) : index + 1]
        ten_year_mean = sum(sigma_window) / len(sigma_window)
        require_finite_positive("S27 v2 ten-year sigma mean", ten_year_mean)
        v = row.annual_percentage_sigma / ten_year_mean
        require_finite_positive("S27 v2 relative volatility", v)
        v_values.append(v)
        q = _expanding_quantile(v_values, v)
        raw_m = 2.0 - 1.5 * q
        if raw_m <= 0.0:
            raise CarverBlocked("S27 v2 raw volatility multiplier must remain positive")
        raw_multipliers.append(raw_m)
        m_values = _ewma_series(tuple(raw_multipliers), S27_V2_VQM_EWMA_SPAN)
        output.append(
            S27V2DailyRuntimeRow(
                completed_trading_date=row.completed_trading_date,
                current_traded_contract_close=row.current_traded_contract_close,
                equilibrium_ewma5=equilibrium[index],
                trend_fast_ewma16=trend_fast[index],
                trend_slow_ewma64=trend_slow[index],
                trend_forecast=trend_fast[index] - trend_slow[index],
                annual_percentage_sigma=row.annual_percentage_sigma,
                ten_year_sigma_mean=ten_year_mean,
                relative_volatility_v=v,
                quantile_q=q,
                raw_vol_multiplier=raw_m,
                vol_multiplier_m=m_values[-1],
                sigma_source_observation_count=len(sigma_window),
                q_source_observation_count=len(v_values),
                level_compatibility_status=row.level_compatibility_status,
                annual_percentage_sigma_source_status=row.annual_percentage_sigma_source_status,
            )
        )
    return tuple(output)


def build_s27_v2_forecast_replay_row(
    *,
    hourly_row: S27V2HourlyRuntimeInput,
    daily_input: S27V2DailyRuntimeInput,
    daily_runtime: S27V2DailyRuntimeRow,
    daily_runtime_selection_status: str = S27_V2_UNSPECIFIED_DAILY_RUNTIME_SELECTION_STATUS,
    source_lock: S27V2SourceLock = S27V2SourceLock(),
) -> S27V2ForecastReplayRow:
    source_lock.validate()
    hourly_row.validate()
    daily_input.validate()
    _require_exact(
        "S27 v2 latest strict-prior daily runtime selection status",
        daily_runtime_selection_status,
        S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
    )
    _require_exact("S27 v2 forecast daily runtime date", daily_runtime.completed_trading_date, daily_input.completed_trading_date)
    _require_exact(
        "S27 v2 daily runtime level compatibility status",
        daily_runtime.level_compatibility_status,
        S27_V2_LEVEL_COMPATIBILITY_STATUS,
    )
    _require_close(
        "S27 v2 daily runtime current traded contract close",
        daily_runtime.current_traded_contract_close,
        daily_input.current_traded_contract_close,
    )
    _require_close(
        "S27 v2 daily runtime annual percentage sigma",
        daily_runtime.annual_percentage_sigma,
        daily_input.annual_percentage_sigma,
    )
    _require_exact(
        "S27 v2 daily runtime annual percentage sigma source status",
        daily_runtime.annual_percentage_sigma_source_status,
        daily_input.annual_percentage_sigma_source_status,
    )
    if daily_input.completed_bar_timestamp >= hourly_row.completed_bar_end_utc:
        raise CarverBlocked("S27 v2 forecast requires strict-prior completed daily runtime")
    if daily_input.completed_trading_date >= hourly_row.completed_trading_date:
        raise CarverBlocked("S27 v2 daily runtime must be prior to the hourly completed trading date")

    raw_forecast = daily_runtime.equilibrium_ewma5 - hourly_row.close
    sigma_price = (
        daily_input.current_traded_contract_close
        * daily_runtime.annual_percentage_sigma
        / 16.0
    )
    require_finite_positive("S27 v2 sigma price", sigma_price)
    risk_adjusted = raw_forecast / sigma_price
    _require_finite("S27 v2 risk-adjusted forecast before veto", risk_adjusted)
    if daily_runtime.trend_forecast == 0.0:
        raise CarverBlocked("S27 v2 zero trend case is fail-closed")
    veto = risk_adjusted * daily_runtime.trend_forecast < 0.0
    after_veto = 0.0 if veto else risk_adjusted
    adjusted = after_veto * daily_runtime.vol_multiplier_m
    scaled = adjusted * source_lock.scalar_implementation_freeze
    capped = cap_forecast(scaled, FORECAST_CAP)
    return S27V2ForecastReplayRow(
        as_of=hourly_row.completed_bar_end_utc,
        completed_trading_date=hourly_row.completed_trading_date,
        raw_symbol=hourly_row.raw_symbol,
        hourly_current_price=hourly_row.close,
        equilibrium_ewma5=daily_runtime.equilibrium_ewma5,
        raw_forecast=raw_forecast,
        previous_completed_daily_close_current_traded_contract=daily_input.current_traded_contract_close,
        annual_percentage_sigma=daily_runtime.annual_percentage_sigma,
        sigma_price=sigma_price,
        risk_adjusted_forecast_before_veto=risk_adjusted,
        trend_forecast=daily_runtime.trend_forecast,
        trend_veto_applied=veto,
        risk_adjusted_forecast_after_veto=after_veto,
        vol_multiplier_m=daily_runtime.vol_multiplier_m,
        adjusted_risk_adjusted_forecast=adjusted,
        scalar_book_text=source_lock.scalar_book_text,
        scalar=source_lock.scalar_implementation_freeze,
        scaled_forecast=scaled,
        capped_forecast=capped,
    )


def build_s27_v2_desired_position_row(
    forecast: S27V2ForecastReplayRow,
    *,
    base_position_contracts: float,
    rounding_policy: RoundingPolicy,
    source_lock: S27V2SourceLock = S27V2SourceLock(),
) -> S27V2DesiredPositionRow:
    source_lock.validate()
    require_finite_positive("S27 v2 base position contracts", base_position_contracts)
    if rounding_policy is not RoundingPolicy.NEAREST:
        raise CarverBlocked("S27 v2 source-faithful path requires nearest whole-contract rounding")
    desired_unrounded = forecast.capped_forecast / S27_V2_FORECAST_TO_POSITION_DIVISOR * base_position_contracts
    rounded = _round_contracts(desired_unrounded, rounding_policy)
    return S27V2DesiredPositionRow(
        as_of=forecast.as_of,
        capped_forecast=forecast.capped_forecast,
        base_position_contracts=base_position_contracts,
        desired_unrounded_contracts=desired_unrounded,
        desired_rounded_contracts=rounded,
        rounding_policy=rounding_policy,
    )


def build_s27_v2_order_plan(
    *,
    forecast_context: S27V2ForecastContext,
    current_position: int,
    desired_rounded_position: int,
    source_lock: S27V2SourceLock = S27V2SourceLock(),
) -> S27V2OrderPlan:
    source_lock.validate()
    forecast_context.validate()
    _require_int("S27 v2 current position", current_position)
    _require_int("S27 v2 desired rounded position", desired_rounded_position)
    expected_desired = _source_faithful_desired_position_from_context(forecast_context)
    if desired_rounded_position != expected_desired:
        raise CarverBlocked("S27 v2 order plan desired position must match forecast context")
    gap = desired_rounded_position - current_position
    _require_target_position_allowed_by_trend(desired_rounded_position, forecast_context.trend_forecast)
    if abs(gap) > 1:
        side = S27V2OrderSide.BUY if gap > 0 else S27V2OrderSide.SELL
        return S27V2OrderPlan(
            decision_as_of=forecast_context.as_of,
            current_position=current_position,
            desired_rounded_position=desired_rounded_position,
            limit_orders=(),
            market_orders=(
                S27V2MarketOrderRow(
                    decision_as_of=forecast_context.as_of,
                    side=side,
                    quantity=abs(gap),
                    target_position_after_fill=desired_rounded_position,
                    trigger="DESIRED_POSITION_MORE_THAN_ONE_CONTRACT_FROM_CURRENT",
                ),
            ),
            end_of_day_cancel_reset_required=True,
            forecast_context=forecast_context,
        )

    limit_orders: list[S27V2LimitOrderRow] = []
    if forecast_context.capped_forecast >= FORECAST_CAP and gap > 0:
        return _single_market_order_plan(
            forecast_context=forecast_context,
            current_position=current_position,
            desired_rounded_position=desired_rounded_position,
            side=S27V2OrderSide.BUY,
            quantity=gap,
            trigger="CAP_BOUND_NO_BUY_LIMIT_SIDE",
        )
    if forecast_context.capped_forecast <= -FORECAST_CAP and gap < 0:
        return _single_market_order_plan(
            forecast_context=forecast_context,
            current_position=current_position,
            desired_rounded_position=desired_rounded_position,
            side=S27V2OrderSide.SELL,
            quantity=abs(gap),
            trigger="CAP_BOUND_NO_SELL_LIMIT_SIDE",
        )
    if (
        forecast_context.capped_forecast < FORECAST_CAP
        and _adjacent_limit_target_is_priceable(forecast_context, current_position + 1)
    ):
        buy_price = implied_price_for_target_position(
            forecast_context,
            target_position=current_position + 1,
        )
        limit_orders.append(
            S27V2LimitOrderRow(
                decision_as_of=forecast_context.as_of,
                side=S27V2OrderSide.BUY,
                quantity=1,
                target_position_after_fill=current_position + 1,
                limit_price=buy_price,
            )
        )
    if (
        forecast_context.capped_forecast > -FORECAST_CAP
        and _adjacent_limit_target_is_priceable(forecast_context, current_position - 1)
    ):
        sell_price = implied_price_for_target_position(
            forecast_context,
            target_position=current_position - 1,
        )
        limit_orders.append(
            S27V2LimitOrderRow(
                decision_as_of=forecast_context.as_of,
                side=S27V2OrderSide.SELL,
                quantity=1,
                target_position_after_fill=current_position - 1,
                limit_price=sell_price,
            )
        )
    if gap != 0 and not any(order.target_position_after_fill == desired_rounded_position for order in limit_orders):
        side = S27V2OrderSide.BUY if gap > 0 else S27V2OrderSide.SELL
        return S27V2OrderPlan(
            decision_as_of=forecast_context.as_of,
            current_position=current_position,
            desired_rounded_position=desired_rounded_position,
            limit_orders=(),
            market_orders=(
                S27V2MarketOrderRow(
                    decision_as_of=forecast_context.as_of,
                    side=side,
                    quantity=abs(gap),
                    target_position_after_fill=desired_rounded_position,
                    trigger="ADJACENT_DESIRED_TARGET_UNPRICEABLE_AT_CAP",
                ),
            ),
            end_of_day_cancel_reset_required=True,
            forecast_context=forecast_context,
        )
    if not limit_orders:
        if gap == 0:
            return S27V2OrderPlan(
                decision_as_of=forecast_context.as_of,
                current_position=current_position,
                desired_rounded_position=desired_rounded_position,
                limit_orders=(),
                market_orders=(),
                end_of_day_cancel_reset_required=True,
                forecast_context=forecast_context,
            )
        side = S27V2OrderSide.BUY if gap > 0 else S27V2OrderSide.SELL
        return S27V2OrderPlan(
            decision_as_of=forecast_context.as_of,
            current_position=current_position,
            desired_rounded_position=desired_rounded_position,
            limit_orders=(),
            market_orders=(
                S27V2MarketOrderRow(
                    decision_as_of=forecast_context.as_of,
                    side=side,
                    quantity=abs(gap),
                    target_position_after_fill=desired_rounded_position,
                    trigger="CAP_BOUND_NO_ADJACENT_LIMIT_SIDE",
                ),
            ) if gap else (),
            end_of_day_cancel_reset_required=True,
            forecast_context=forecast_context,
        )
    return S27V2OrderPlan(
        decision_as_of=forecast_context.as_of,
        current_position=current_position,
        desired_rounded_position=desired_rounded_position,
        limit_orders=tuple(limit_orders),
        market_orders=(),
        end_of_day_cancel_reset_required=True,
        forecast_context=forecast_context,
    )


def open_s27_v2_working_order_state(
    order_plan: S27V2OrderPlan,
    *,
    raw_symbol: str,
    session_id: str,
) -> S27V2WorkingOrderState:
    _validate_utc_hour("S27 v2 working order opened as_of", order_plan.decision_as_of)
    _validate_order_plan_internal_consistency(order_plan)
    require_non_empty_text("S27 v2 working order raw symbol", raw_symbol)
    require_non_empty_text("S27 v2 working order session id", session_id)
    if order_plan.limit_orders and order_plan.market_orders:
        raise CarverBlocked("S27 v2 order plan cannot mix working limit and market orders")
    if order_plan.raw_symbol is not None and order_plan.raw_symbol != raw_symbol:
        raise CarverBlocked("S27 v2 working state raw symbol must match order plan")
    if order_plan.session_id is not None and order_plan.session_id != session_id:
        raise CarverBlocked("S27 v2 working state session id must match order plan")
    return S27V2WorkingOrderState(
        opened_as_of=order_plan.decision_as_of,
        session_id=session_id,
        raw_symbol=raw_symbol,
        current_position=order_plan.current_position,
        desired_rounded_position=order_plan.desired_rounded_position,
        limit_orders=order_plan.limit_orders,
        market_orders=order_plan.market_orders,
        forecast_context=order_plan.forecast_context,
    )


def transition_s27_v2_working_order_state_one_hour(
    state: S27V2WorkingOrderState,
    next_hourly_row: S27V2HourlyRuntimeInput,
    *,
    transition_kind: S27V2SessionTransitionKind,
    next_session_id: str,
    commission_per_contract: float,
    normal_bid_ask_spread: float,
    roll_handling_status: str = S27_V2_NO_ROLL_BOUNDARY_STATUS,
) -> S27V2WorkingOrderTransitionResult:
    next_hourly_row.validate()
    _validate_utc_hour("S27 v2 working order state opened as_of", state.opened_as_of)
    _validate_working_order_state_internal_consistency(state)
    require_non_empty_text("S27 v2 working order state session id", state.session_id)
    require_non_empty_text("S27 v2 next session id", next_session_id)
    require_non_empty_text("S27 v2 roll handling status", roll_handling_status)
    _require_int("S27 v2 working order current position", state.current_position)
    _require_int("S27 v2 working order desired position", state.desired_rounded_position)
    if next_hourly_row.completed_bar_end_utc - state.opened_as_of != timedelta(hours=1):
        raise CarverBlocked("S27 v2 working order transition requires exactly one-hour lag")
    _validate_direct_transition_facts(
        state=state,
        next_hourly_row=next_hourly_row,
        transition_kind=transition_kind,
        next_session_id=next_session_id,
    )
    if transition_kind is S27V2SessionTransitionKind.ROLL_BOUNDARY:
        if roll_handling_status != S27_V2_ROLL_STATE_RESET_ASSUMPTION_STATUS:
            raise CarverBlocked("S27 v2 roll boundary requires explicit state-reset implementation assumption")
        if state.current_position != 0:
            raise CarverBlocked("S27 v2 direct roll boundary with nonzero position requires source-locked roll bridge")
        return S27V2WorkingOrderTransitionResult(
            transition_kind=transition_kind,
            prior_state=state,
            fills=(),
            next_position=state.current_position,
            remaining_limit_orders=(),
            canceled_limit_orders=state.limit_orders,
            market_orders=(),
            roll_handling_status=roll_handling_status,
        )
    if roll_handling_status != S27_V2_NO_ROLL_BOUNDARY_STATUS:
        raise CarverBlocked("S27 v2 non-roll transition must not carry roll handling status")
    if next_hourly_row.raw_symbol != state.raw_symbol:
        raise CarverBlocked("S27 v2 raw symbol changed outside an explicit roll boundary")
    if transition_kind is S27V2SessionTransitionKind.END_OF_DAY_CANCEL_RESET:
        if state.market_orders:
            raise CarverBlocked("S27 v2 EOD cancel reset with pending market orders is unresolved")
        return S27V2WorkingOrderTransitionResult(
            transition_kind=transition_kind,
            prior_state=state,
            fills=(),
            next_position=state.current_position,
            remaining_limit_orders=(),
            canceled_limit_orders=state.limit_orders,
            market_orders=(),
            roll_handling_status=roll_handling_status,
        )
    if transition_kind is S27V2SessionTransitionKind.OVERNIGHT_GAP_MARKET_RESET:
        raise CarverBlocked(
            "S27 v2 overnight reset requires recomputed next-session desired position"
        )
    fills = fill_s27_v2_order_plan_one_hour_lag(
        S27V2OrderPlan(
            decision_as_of=state.opened_as_of,
            current_position=state.current_position,
            desired_rounded_position=state.desired_rounded_position,
            limit_orders=state.limit_orders,
            market_orders=state.market_orders,
            end_of_day_cancel_reset_required=True,
            forecast_context=state.forecast_context,
            raw_symbol=state.raw_symbol,
            session_id=state.session_id,
        ),
        next_hourly_row,
        current_raw_symbol=state.raw_symbol,
        current_session_id=state.session_id,
        next_session_id=next_session_id,
        transition_kind=transition_kind,
        commission_per_contract=commission_per_contract,
        normal_bid_ask_spread=normal_bid_ask_spread,
    )
    filled_limit_orders = _filled_limit_orders_from_fills(state.limit_orders, fills)
    remaining = tuple(order for order in state.limit_orders if order not in filled_limit_orders)
    canceled: tuple[S27V2LimitOrderRow, ...] = ()
    if transition_kind is not S27V2SessionTransitionKind.NORMAL_ONE_HOUR:
        raise CarverBlocked("S27 v2 session transition kind is unresolved")
    if next_session_id != state.session_id:
        raise CarverBlocked("S27 v2 session id changed without EOD/overnight transition")
    return S27V2WorkingOrderTransitionResult(
        transition_kind=transition_kind,
        prior_state=state,
        fills=fills,
        next_position=_position_after_fills(state.current_position, fills),
        remaining_limit_orders=remaining,
        canceled_limit_orders=canceled,
        market_orders=state.market_orders,
        roll_handling_status=roll_handling_status,
    )


def build_s27_v2_replay_step_ledger_bundle(
    *,
    hourly_row: S27V2HourlyRuntimeInput,
    next_hourly_row: S27V2HourlyRuntimeInput,
    daily_input: S27V2DailyRuntimeInput,
    daily_runtime: S27V2DailyRuntimeRow,
    current_position: int,
    base_position_contracts: float,
    rounding_policy: RoundingPolicy,
    transition_kind: S27V2SessionTransitionKind,
    next_session_id: str,
    commission_per_contract: float,
    normal_bid_ask_spread: float,
    contract_multiplier: float,
    daily_runtime_selection_status: str = S27_V2_UNSPECIFIED_DAILY_RUNTIME_SELECTION_STATUS,
    session_id: str | None = None,
    roll_handling_status: str = S27_V2_NO_ROLL_BOUNDARY_STATUS,
    source_lock: S27V2SourceLock = S27V2SourceLock(),
) -> S27V2ReplayStepLedgerBundle:
    source_lock.validate()
    hourly_row.validate()
    next_hourly_row.validate()
    daily_input.validate()
    _require_int("S27 v2 replay current position", current_position)
    require_finite_positive("S27 v2 replay base position", base_position_contracts)
    require_finite_positive("S27 v2 replay commission per contract", commission_per_contract)
    require_finite_positive("S27 v2 replay normal bid-ask spread", normal_bid_ask_spread)
    require_finite_positive("S27 v2 replay contract multiplier", contract_multiplier)
    if next_hourly_row.completed_bar_end_utc <= hourly_row.completed_bar_end_utc:
        raise CarverBlocked("S27 v2 replay next hourly row must follow decision row")
    _validate_transition_facts(
        hourly_row=hourly_row,
        next_hourly_row=next_hourly_row,
        transition_kind=transition_kind,
        session_id=session_id or hourly_row.completed_trading_date,
        next_session_id=next_session_id,
    )

    manifest = S27V2SourceInputManifestRow(
        as_of=hourly_row.completed_bar_end_utc,
        daily_completed_trading_date=daily_input.completed_trading_date,
        daily_completed_bar_timestamp=daily_input.completed_bar_timestamp,
        daily_continuous_close=daily_input.continuous_close,
        daily_current_traded_contract_close=daily_input.current_traded_contract_close,
        daily_annual_percentage_sigma=daily_input.annual_percentage_sigma,
        daily_annual_percentage_sigma_source_status=daily_input.annual_percentage_sigma_source_status,
        hourly_completed_trading_date=hourly_row.completed_trading_date,
        hourly_completed_bar_end_utc=hourly_row.completed_bar_end_utc,
        raw_symbol=hourly_row.raw_symbol,
        hourly_open=hourly_row.open,
        hourly_high=hourly_row.high,
        hourly_low=hourly_row.low,
        hourly_close=hourly_row.close,
        fill_hourly_completed_trading_date=next_hourly_row.completed_trading_date,
        fill_hourly_completed_bar_end_utc=next_hourly_row.completed_bar_end_utc,
        fill_raw_symbol=next_hourly_row.raw_symbol,
        fill_hourly_open=next_hourly_row.open,
        fill_hourly_high=next_hourly_row.high,
        fill_hourly_low=next_hourly_row.low,
        fill_hourly_close=next_hourly_row.close,
        daily_source_status=daily_input.source_status,
        hourly_provider_condition_status=hourly_row.provider_condition_status,
        fill_hourly_provider_condition_status=next_hourly_row.provider_condition_status,
    )
    compatibility = S27V2LevelCompatibilityLedgerRow(
        as_of=hourly_row.completed_bar_end_utc,
        daily_completed_trading_date=daily_input.completed_trading_date,
        hourly_completed_trading_date=hourly_row.completed_trading_date,
        daily_continuous_close=daily_input.continuous_close,
        daily_current_traded_contract_close=daily_input.current_traded_contract_close,
        hourly_current_price=hourly_row.close,
        sigma_bridge_price=daily_input.current_traded_contract_close,
        annual_percentage_sigma=daily_input.annual_percentage_sigma,
        annual_percentage_sigma_source_status=daily_input.annual_percentage_sigma_source_status,
        level_compatibility_status=daily_input.level_compatibility_status,
    )
    forecast = build_s27_v2_forecast_replay_row(
        hourly_row=hourly_row,
        daily_input=daily_input,
        daily_runtime=daily_runtime,
        daily_runtime_selection_status=daily_runtime_selection_status,
        source_lock=source_lock,
    )
    desired = build_s27_v2_desired_position_row(
        forecast,
        base_position_contracts=base_position_contracts,
        rounding_policy=rounding_policy,
        source_lock=source_lock,
    )
    forecast_context = S27V2ForecastContext(
        as_of=forecast.as_of,
        equilibrium_ewma5=forecast.equilibrium_ewma5,
        sigma_price=forecast.sigma_price,
        vol_multiplier_m=forecast.vol_multiplier_m,
        scalar=forecast.scalar,
        base_position_contracts=base_position_contracts,
        capped_forecast=forecast.capped_forecast,
        trend_forecast=forecast.trend_forecast,
    )
    order_plan = build_s27_v2_order_plan(
        forecast_context=forecast_context,
        current_position=current_position,
        desired_rounded_position=desired.desired_rounded_contracts,
        source_lock=source_lock,
    )
    state = open_s27_v2_working_order_state(
        order_plan,
        raw_symbol=hourly_row.raw_symbol,
        session_id=session_id or hourly_row.completed_trading_date,
    )
    transition = transition_s27_v2_working_order_state_one_hour(
        state,
        next_hourly_row,
        transition_kind=transition_kind,
        next_session_id=next_session_id,
        commission_per_contract=commission_per_contract,
        normal_bid_ask_spread=normal_bid_ask_spread,
        roll_handling_status=roll_handling_status,
    )
    if transition_kind is S27V2SessionTransitionKind.ROLL_BOUNDARY and current_position != 0:
        raise CarverBlocked("S27 v2 roll-boundary PnL requires source-locked nonzero-position roll bridge")
    costs = build_s27_v2_cost_ledger_rows(transition.fills)
    pnl = build_s27_v2_pnl_ledger_row(
        start_as_of=hourly_row.completed_bar_end_utc,
        end_as_of=next_hourly_row.completed_bar_end_utc,
        starting_position=current_position,
        start_price=hourly_row.close,
        end_price=next_hourly_row.close,
        contract_multiplier=contract_multiplier,
        cost_rows=costs,
    )
    executed_market_orders = transition.market_orders if transition.market_orders else order_plan.market_orders
    if transition_kind is S27V2SessionTransitionKind.ROLL_BOUNDARY:
        executed_market_orders = transition.market_orders
    commission_rows, spread_rows = _build_cost_component_rows(costs)
    validation_rows = _build_replay_validation_rows(
        hourly_row=hourly_row,
        next_hourly_row=next_hourly_row,
        daily_input=daily_input,
        transition_kind=transition_kind,
    )
    row_groups: tuple[tuple[str, tuple[object, ...]], ...] = (
        ("SOURCE_INPUT_MANIFEST", (manifest,)),
        ("DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER", (compatibility,)),
        ("RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM", (daily_runtime,)),
        ("FORECAST_REPLAY_LEDGER", (forecast,)),
        ("DESIRED_POSITION_LEDGER", (desired,)),
        ("WORKING_ORDER_TRANSITION_LEDGER", (transition,)),
        ("LIMIT_ORDER_LEDGER", order_plan.limit_orders),
        ("MARKET_ORDER_LEDGER", executed_market_orders),
        ("REMAINING_LIMIT_ORDER_LEDGER", transition.remaining_limit_orders),
        ("CANCELED_LIMIT_ORDER_LEDGER", transition.canceled_limit_orders),
        ("FILL_LEDGER", transition.fills),
        ("COMMISSION_LEDGER", commission_rows),
        ("SPREAD_COST_LEDGER", spread_rows),
        ("PNL_LEDGER", (pnl,)),
        ("VALIDATION_LEDGER", validation_rows),
    )
    return S27V2ReplayStepLedgerBundle(
        source_input_manifest_rows=(manifest,),
        level_compatibility_ledger_rows=(compatibility,),
        daily_runtime_rows=(daily_runtime,),
        forecast_replay_rows=(forecast,),
        desired_position_rows=(desired,),
        order_plan_rows=(order_plan,),
        working_transition_rows=(transition,),
        limit_order_rows=order_plan.limit_orders,
        market_order_rows=executed_market_orders,
        remaining_limit_order_rows=transition.remaining_limit_orders,
        canceled_limit_order_rows=transition.canceled_limit_orders,
        fill_rows=transition.fills,
        cost_ledger_rows=costs,
        commission_ledger_rows=commission_rows,
        spread_cost_ledger_rows=spread_rows,
        pnl_ledger_rows=(pnl,),
        validation_ledger_rows=validation_rows,
        provenance_hash_ledger_rows=_build_provenance_hash_rows(hourly_row.completed_bar_end_utc, row_groups),
        final_position=transition.next_position,
    )


def build_s27_v2_multi_row_replay_ledger_bundle(
    *,
    daily_rows: tuple[S27V2DailyRuntimeInput, ...],
    hourly_rows: tuple[S27V2HourlyRuntimeInput, ...],
    initial_position: int,
    base_position_contracts: float,
    rounding_policy: RoundingPolicy,
    transition_kinds: tuple[S27V2SessionTransitionKind, ...],
    session_ids: tuple[str, ...],
    commission_per_contract: float,
    normal_bid_ask_spread: float,
    contract_multiplier: float,
    roll_handling_statuses: tuple[str, ...] | None = None,
    source_lock: S27V2SourceLock = S27V2SourceLock(),
) -> S27V2ReplayRunLedgerBundle:
    source_lock.validate()
    _require_int("S27 v2 multi-row initial position", initial_position)
    require_finite_positive("S27 v2 multi-row base position", base_position_contracts)
    require_finite_positive("S27 v2 multi-row commission per contract", commission_per_contract)
    require_finite_positive("S27 v2 multi-row normal bid-ask spread", normal_bid_ask_spread)
    require_finite_positive("S27 v2 multi-row contract multiplier", contract_multiplier)
    if len(hourly_rows) < 2:
        raise CarverBlocked("S27 v2 multi-row replay requires at least two hourly rows")
    if len(transition_kinds) != len(hourly_rows) - 1:
        raise CarverBlocked("S27 v2 multi-row transition kinds must cover each hourly step")
    if len(session_ids) != len(hourly_rows):
        raise CarverBlocked("S27 v2 multi-row session ids must cover each hourly row")
    roll_statuses = (
        (S27_V2_NO_ROLL_BOUNDARY_STATUS,) * (len(hourly_rows) - 1)
        if roll_handling_statuses is None
        else roll_handling_statuses
    )
    if len(roll_statuses) != len(hourly_rows) - 1:
        raise CarverBlocked("S27 v2 multi-row roll statuses must cover each hourly step")

    runtime_rows = build_s27_v2_daily_runtime_rows(daily_rows, source_lock=source_lock)
    position = initial_position
    step_bundles: list[S27V2ReplayStepLedgerBundle] = []
    for index in range(len(hourly_rows) - 1):
        hourly_rows[index].validate()
        hourly_rows[index + 1].validate()
        daily_input, daily_runtime = _select_strict_prior_daily_runtime(
            daily_rows,
            runtime_rows,
            hourly_rows[index],
        )
        step = build_s27_v2_replay_step_ledger_bundle(
            hourly_row=hourly_rows[index],
            next_hourly_row=hourly_rows[index + 1],
            daily_input=daily_input,
            daily_runtime=daily_runtime,
            daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
            current_position=position,
            base_position_contracts=base_position_contracts,
            rounding_policy=rounding_policy,
            transition_kind=transition_kinds[index],
            next_session_id=session_ids[index + 1],
            commission_per_contract=commission_per_contract,
            normal_bid_ask_spread=normal_bid_ask_spread,
            contract_multiplier=contract_multiplier,
            session_id=session_ids[index],
            roll_handling_status=roll_statuses[index],
            source_lock=source_lock,
        )
        if (
            transition_kinds[index] is S27V2SessionTransitionKind.NORMAL_ONE_HOUR
            and step.remaining_limit_order_rows
        ):
            raise CarverBlocked(
                "S27 v2 multi-row replay fails closed on unresolved carried working limits"
            )
        step_bundles.append(step)
        position = step.final_position

    return S27V2ReplayRunLedgerBundle(
        step_bundles=tuple(step_bundles),
        source_input_manifest_rows=_collect_step_rows(step_bundles, "source_input_manifest_rows"),
        level_compatibility_ledger_rows=_collect_step_rows(step_bundles, "level_compatibility_ledger_rows"),
        daily_runtime_rows=_collect_step_rows(step_bundles, "daily_runtime_rows"),
        forecast_replay_rows=_collect_step_rows(step_bundles, "forecast_replay_rows"),
        desired_position_rows=_collect_step_rows(step_bundles, "desired_position_rows"),
        order_plan_rows=_collect_step_rows(step_bundles, "order_plan_rows"),
        working_transition_rows=_collect_step_rows(step_bundles, "working_transition_rows"),
        limit_order_rows=_collect_step_rows(step_bundles, "limit_order_rows"),
        market_order_rows=_collect_step_rows(step_bundles, "market_order_rows"),
        remaining_limit_order_rows=_collect_step_rows(step_bundles, "remaining_limit_order_rows"),
        canceled_limit_order_rows=_collect_step_rows(step_bundles, "canceled_limit_order_rows"),
        fill_rows=_collect_step_rows(step_bundles, "fill_rows"),
        cost_ledger_rows=_collect_step_rows(step_bundles, "cost_ledger_rows"),
        commission_ledger_rows=_collect_step_rows(step_bundles, "commission_ledger_rows"),
        spread_cost_ledger_rows=_collect_step_rows(step_bundles, "spread_cost_ledger_rows"),
        pnl_ledger_rows=_collect_step_rows(step_bundles, "pnl_ledger_rows"),
        validation_ledger_rows=_collect_step_rows(step_bundles, "validation_ledger_rows"),
        provenance_hash_ledger_rows=_collect_step_rows(step_bundles, "provenance_hash_ledger_rows"),
        initial_position=initial_position,
        final_position=position,
        replay_step_count=len(step_bundles),
    )


def fill_s27_v2_order_plan_one_hour_lag(
    order_plan: S27V2OrderPlan,
    next_hourly_row: S27V2HourlyRuntimeInput,
    *,
    current_raw_symbol: str,
    current_session_id: str,
    next_session_id: str,
    transition_kind: S27V2SessionTransitionKind,
    commission_per_contract: float,
    normal_bid_ask_spread: float,
) -> tuple[S27V2FillRow, ...]:
    next_hourly_row.validate()
    _validate_order_plan_internal_consistency(order_plan)
    if next_hourly_row.completed_bar_end_utc - order_plan.decision_as_of != timedelta(hours=1):
        raise CarverBlocked("S27 v2 fill simulation requires exactly one-hour lag")
    require_finite_positive("S27 v2 commission per contract", commission_per_contract)
    require_finite_positive("S27 v2 normal bid-ask spread", normal_bid_ask_spread)
    _validate_direct_fill_session_binding(
        order_plan=order_plan,
        next_hourly_row=next_hourly_row,
        current_raw_symbol=current_raw_symbol,
        current_session_id=current_session_id,
        next_session_id=next_session_id,
        transition_kind=transition_kind,
    )
    fills: list[S27V2FillRow] = []
    for market in order_plan.market_orders:
        fills.append(
            _fill_row(
                decision_as_of=market.decision_as_of,
                fill_as_of=next_hourly_row.completed_bar_end_utc,
                side=market.side,
                quantity=market.quantity,
                fill_price=next_hourly_row.close,
                order_kind=market.order_kind,
                cost_treatment=market.cost_treatment,
                commission_per_contract=commission_per_contract,
                normal_bid_ask_spread=normal_bid_ask_spread,
            )
        )
    if fills:
        return tuple(fills)
    touched_limits: list[S27V2LimitOrderRow] = []
    for limit in order_plan.limit_orders:
        touched = (
            next_hourly_row.close <= limit.limit_price
            if limit.side is S27V2OrderSide.BUY
            else next_hourly_row.close >= limit.limit_price
        )
        if touched:
            touched_limits.append(limit)
    if len(touched_limits) > 1:
        raise CarverBlocked("S27 v2 next completed close crossed multiple limit orders; sequence is fail-closed")
    for limit in touched_limits:
        fills.append(
            _fill_row(
                decision_as_of=limit.decision_as_of,
                fill_as_of=next_hourly_row.completed_bar_end_utc,
                side=limit.side,
                quantity=limit.quantity,
                fill_price=limit.limit_price,
                order_kind=limit.order_kind,
                cost_treatment=limit.cost_treatment,
                commission_per_contract=commission_per_contract,
                normal_bid_ask_spread=normal_bid_ask_spread,
            )
        )
    return tuple(fills)


def _overnight_gap_market_fills(
    state: S27V2WorkingOrderState,
    next_hourly_row: S27V2HourlyRuntimeInput,
    *,
    commission_per_contract: float,
    normal_bid_ask_spread: float,
) -> tuple[S27V2FillRow, ...]:
    raise CarverBlocked("S27 v2 overnight market fills require next-session recomputed desired position")


def _position_after_fills(current_position: int, fills: tuple[S27V2FillRow, ...]) -> int:
    position = current_position
    for fill in fills:
        position += fill.quantity if fill.side is S27V2OrderSide.BUY else -fill.quantity
    return position


def _filled_limit_orders_from_fills(
    limit_orders: tuple[S27V2LimitOrderRow, ...],
    fills: tuple[S27V2FillRow, ...],
) -> tuple[S27V2LimitOrderRow, ...]:
    filled: list[S27V2LimitOrderRow] = []
    for fill in fills:
        if fill.order_kind is not S27V2OrderKind.LIMIT:
            continue
        for order in limit_orders:
            if (
                order.side is fill.side
                and order.quantity == fill.quantity
                and abs(order.limit_price - fill.fill_price) <= 1e-12
            ):
                filled.append(order)
                break
    return tuple(filled)


def _single_market_order_plan(
    *,
    forecast_context: S27V2ForecastContext,
    current_position: int,
    desired_rounded_position: int,
    side: S27V2OrderSide,
    quantity: int,
    trigger: str,
) -> S27V2OrderPlan:
    if quantity <= 0:
        raise CarverBlocked("S27 v2 market order quantity must be positive")
    return S27V2OrderPlan(
        decision_as_of=forecast_context.as_of,
        current_position=current_position,
        desired_rounded_position=desired_rounded_position,
        limit_orders=(),
        market_orders=(
            S27V2MarketOrderRow(
                decision_as_of=forecast_context.as_of,
                side=side,
                quantity=quantity,
                target_position_after_fill=desired_rounded_position,
                trigger=trigger,
            ),
        ),
        end_of_day_cancel_reset_required=True,
        forecast_context=forecast_context,
    )


def build_s27_v2_cost_ledger_rows(fills: tuple[S27V2FillRow, ...]) -> tuple[S27V2CostLedgerRow, ...]:
    rows: list[S27V2CostLedgerRow] = []
    for fill in fills:
        _require_exact("S27 v2 fill source status", fill.fill_source_status, S27_V2_FILL_SOURCE_STATUS)
        _require_finite_nonnegative("S27 v2 fill commission cost", fill.commission_cost)
        _require_finite_nonnegative("S27 v2 fill spread cost", fill.spread_cost)
        _require_finite_nonnegative("S27 v2 fill total cost", fill.total_cost)
        if fill.order_kind is S27V2OrderKind.LIMIT:
            if fill.cost_treatment is not S27V2FillCostTreatment.COMMISSION_ONLY:
                raise CarverBlocked("S27 v2 limit fill must use commission-only cost treatment")
            if fill.commission_cost <= 0.0:
                raise CarverBlocked("S27 v2 limit fill must include positive commission")
        elif fill.order_kind is S27V2OrderKind.MARKET:
            if fill.cost_treatment is not S27V2FillCostTreatment.COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD:
                raise CarverBlocked("S27 v2 market fill must include commission plus normal bid-ask spread")
            if fill.commission_cost <= 0.0 or fill.spread_cost <= 0.0:
                raise CarverBlocked("S27 v2 market fill must include positive commission and spread")
        else:
            raise CarverBlocked("S27 v2 fill order kind is unresolved")
        if abs(fill.total_cost - (fill.commission_cost + fill.spread_cost)) > 1e-12:
            raise CarverBlocked("S27 v2 fill total cost must equal commission plus spread")
        if fill.cost_treatment is S27V2FillCostTreatment.COMMISSION_ONLY and fill.spread_cost != 0.0:
            raise CarverBlocked("S27 v2 limit fill cost ledger must not include spread")
        rows.append(
            S27V2CostLedgerRow(
                as_of=fill.fill_as_of,
                order_kind=fill.order_kind,
                side=fill.side,
                quantity=fill.quantity,
                commission_cost=fill.commission_cost,
                spread_cost=fill.spread_cost,
                total_cost=fill.total_cost,
                cost_treatment=fill.cost_treatment,
                cost_source_status=S27_V2_COST_SOURCE_STATUS,
            )
        )
    return tuple(rows)


def build_s27_v2_pnl_ledger_row(
    *,
    start_as_of: datetime,
    end_as_of: datetime,
    starting_position: int,
    start_price: float,
    end_price: float,
    contract_multiplier: float,
    cost_rows: tuple[S27V2CostLedgerRow, ...],
) -> S27V2PnlLedgerRow:
    _validate_utc_hour("S27 v2 PnL start", start_as_of)
    _validate_utc_hour("S27 v2 PnL end", end_as_of)
    if end_as_of <= start_as_of:
        raise CarverBlocked("S27 v2 PnL end must be after start")
    _require_int("S27 v2 PnL starting position", starting_position)
    require_finite_positive("S27 v2 PnL start price", start_price)
    require_finite_positive("S27 v2 PnL end price", end_price)
    require_finite_positive("S27 v2 PnL contract multiplier", contract_multiplier)
    total_cost = 0.0
    for cost in cost_rows:
        _require_exact("S27 v2 PnL cost source status", cost.cost_source_status, S27_V2_COST_SOURCE_STATUS)
        if cost.as_of != end_as_of:
            raise CarverBlocked("S27 v2 PnL cost rows must align to PnL end timestamp")
        _require_finite_nonnegative("S27 v2 PnL cost", cost.total_cost)
        total_cost += cost.total_cost
    gross = starting_position * (end_price - start_price) * contract_multiplier
    return S27V2PnlLedgerRow(
        start_as_of=start_as_of,
        end_as_of=end_as_of,
        starting_position=starting_position,
        start_price=start_price,
        end_price=end_price,
        contract_multiplier=contract_multiplier,
        gross_pnl=gross,
        total_cost=total_cost,
        net_pnl=gross - total_cost,
        pnl_source_status=S27_V2_PNL_SOURCE_STATUS,
    )


def _build_cost_component_rows(
    cost_rows: tuple[S27V2CostLedgerRow, ...],
) -> tuple[tuple[S27V2CostComponentLedgerRow, ...], tuple[S27V2CostComponentLedgerRow, ...]]:
    commission_rows: list[S27V2CostComponentLedgerRow] = []
    spread_rows: list[S27V2CostComponentLedgerRow] = []
    for cost in cost_rows:
        _require_finite_nonnegative("S27 v2 commission ledger amount", cost.commission_cost)
        _require_finite_nonnegative("S27 v2 spread ledger amount", cost.spread_cost)
        if cost.commission_cost > 0.0:
            commission_rows.append(
                S27V2CostComponentLedgerRow(
                    as_of=cost.as_of,
                    order_kind=cost.order_kind,
                    side=cost.side,
                    quantity=cost.quantity,
                    cost_component="COMMISSION",
                    amount=cost.commission_cost,
                )
            )
        if cost.spread_cost > 0.0:
            spread_rows.append(
                S27V2CostComponentLedgerRow(
                    as_of=cost.as_of,
                    order_kind=cost.order_kind,
                    side=cost.side,
                    quantity=cost.quantity,
                    cost_component="NORMAL_BID_ASK_SPREAD",
                    amount=cost.spread_cost,
                )
            )
    return tuple(commission_rows), tuple(spread_rows)


def _select_strict_prior_daily_runtime(
    daily_rows: tuple[S27V2DailyRuntimeInput, ...],
    runtime_rows: tuple[S27V2DailyRuntimeRow, ...],
    hourly_row: S27V2HourlyRuntimeInput,
) -> tuple[S27V2DailyRuntimeInput, S27V2DailyRuntimeRow]:
    hourly_row.validate()
    if len(daily_rows) != len(runtime_rows):
        raise CarverBlocked("S27 v2 daily inputs and runtime rows must align")
    selected: tuple[S27V2DailyRuntimeInput, S27V2DailyRuntimeRow] | None = None
    hourly_trading_date = _parse_iso_date("S27 v2 hourly completed trading date", hourly_row.completed_trading_date)
    for daily_input, daily_runtime in zip(daily_rows, runtime_rows):
        daily_input.validate()
        daily_trading_date = _parse_iso_date("S27 v2 daily completed trading date", daily_input.completed_trading_date)
        if daily_input.completed_bar_timestamp < hourly_row.completed_bar_end_utc and daily_trading_date < hourly_trading_date:
            selected = (daily_input, daily_runtime)
    if selected is None:
        raise CarverBlocked("S27 v2 multi-row replay requires strict-prior daily runtime for each hourly decision")
    return selected


def _validate_transition_facts(
    *,
    hourly_row: S27V2HourlyRuntimeInput,
    next_hourly_row: S27V2HourlyRuntimeInput,
    transition_kind: S27V2SessionTransitionKind,
    session_id: str,
    next_session_id: str,
) -> None:
    require_non_empty_text("S27 v2 transition session id", session_id)
    require_non_empty_text("S27 v2 transition next session id", next_session_id)
    current_trading_date = _parse_iso_date("S27 v2 transition trading date", hourly_row.completed_trading_date)
    next_trading_date = _parse_iso_date("S27 v2 transition next trading date", next_hourly_row.completed_trading_date)
    same_session = session_id == next_session_id
    trading_date_advanced = next_trading_date > current_trading_date
    if transition_kind is S27V2SessionTransitionKind.NORMAL_ONE_HOUR:
        if not same_session or trading_date_advanced:
            raise CarverBlocked("S27 v2 normal transition requires unchanged session and trading date")
        return
    if transition_kind is S27V2SessionTransitionKind.END_OF_DAY_CANCEL_RESET:
        if same_session or not trading_date_advanced:
            raise CarverBlocked("S27 v2 EOD reset requires advanced session and trading date")
        return
    if transition_kind is S27V2SessionTransitionKind.OVERNIGHT_GAP_MARKET_RESET:
        if same_session or not trading_date_advanced:
            raise CarverBlocked("S27 v2 overnight reset requires advanced session and trading date")
        return
    if transition_kind is S27V2SessionTransitionKind.ROLL_BOUNDARY:
        if next_hourly_row.raw_symbol == hourly_row.raw_symbol:
            raise CarverBlocked("S27 v2 roll boundary requires raw symbol change")
        return
    raise CarverBlocked("S27 v2 transition kind is unresolved")


def _validate_direct_transition_facts(
    *,
    state: S27V2WorkingOrderState,
    next_hourly_row: S27V2HourlyRuntimeInput,
    transition_kind: S27V2SessionTransitionKind,
    next_session_id: str,
) -> None:
    _validate_iso_date("S27 v2 direct transition current session id", state.session_id)
    _validate_iso_date("S27 v2 direct transition next session id", next_session_id)
    if transition_kind is S27V2SessionTransitionKind.NORMAL_ONE_HOUR:
        if next_session_id != state.session_id:
            raise CarverBlocked("S27 v2 normal direct transition requires unchanged session id")
        if next_hourly_row.completed_trading_date != state.session_id:
            raise CarverBlocked("S27 v2 normal direct transition requires unchanged trading date")
        if next_hourly_row.raw_symbol != state.raw_symbol:
            raise CarverBlocked("S27 v2 normal direct transition requires unchanged raw symbol")
        return
    if transition_kind is S27V2SessionTransitionKind.END_OF_DAY_CANCEL_RESET:
        if next_session_id <= state.session_id:
            raise CarverBlocked("S27 v2 EOD direct transition requires advanced session id")
        if next_hourly_row.completed_trading_date <= state.session_id:
            raise CarverBlocked("S27 v2 EOD direct transition requires advanced trading date")
        if next_hourly_row.raw_symbol != state.raw_symbol:
            raise CarverBlocked("S27 v2 EOD direct transition requires unchanged raw symbol")
        return
    if transition_kind is S27V2SessionTransitionKind.OVERNIGHT_GAP_MARKET_RESET:
        if next_session_id <= state.session_id:
            raise CarverBlocked("S27 v2 overnight direct transition requires advanced session id")
        if next_hourly_row.completed_trading_date <= state.session_id:
            raise CarverBlocked("S27 v2 overnight direct transition requires advanced trading date")
        if next_hourly_row.raw_symbol != state.raw_symbol:
            raise CarverBlocked("S27 v2 overnight direct transition requires unchanged raw symbol")
        return
    if transition_kind is S27V2SessionTransitionKind.ROLL_BOUNDARY:
        if next_hourly_row.raw_symbol == state.raw_symbol:
            raise CarverBlocked("S27 v2 direct roll boundary requires raw-symbol change")
        return
    raise CarverBlocked("S27 v2 direct transition kind is unresolved")


def _validate_direct_fill_session_binding(
    *,
    order_plan: S27V2OrderPlan,
    next_hourly_row: S27V2HourlyRuntimeInput,
    current_raw_symbol: str,
    current_session_id: str,
    next_session_id: str,
    transition_kind: S27V2SessionTransitionKind,
) -> None:
    require_non_empty_text("S27 v2 direct fill current raw symbol", current_raw_symbol)
    _validate_iso_date("S27 v2 direct fill current session id", current_session_id)
    _validate_iso_date("S27 v2 direct fill next session id", next_session_id)
    if transition_kind is not S27V2SessionTransitionKind.NORMAL_ONE_HOUR:
        raise CarverBlocked("S27 v2 direct fill only supports normal one-hour transitions")
    require_non_empty_text("S27 v2 direct fill order-plan raw symbol", order_plan.raw_symbol)
    _validate_iso_date("S27 v2 direct fill order-plan session id", order_plan.session_id or "")
    if order_plan.raw_symbol != current_raw_symbol:
        raise CarverBlocked("S27 v2 direct fill raw symbol must match order plan")
    if order_plan.session_id != current_session_id:
        raise CarverBlocked("S27 v2 direct fill current session must match order plan")
    if next_session_id != current_session_id:
        raise CarverBlocked("S27 v2 direct fill requires unchanged session id")
    if next_hourly_row.completed_trading_date != current_session_id:
        raise CarverBlocked("S27 v2 direct fill requires unchanged trading date")
    if next_hourly_row.raw_symbol != current_raw_symbol:
        raise CarverBlocked("S27 v2 direct fill requires unchanged raw symbol")
    if order_plan.decision_as_of.date().isoformat() != current_session_id:
        raise CarverBlocked("S27 v2 direct fill decision date must match current session")


def _collect_step_rows(step_bundles: list[S27V2ReplayStepLedgerBundle], attribute: str) -> tuple:
    rows: list[object] = []
    for bundle in step_bundles:
        value = getattr(bundle, attribute)
        if not isinstance(value, tuple):
            raise CarverBlocked("S27 v2 replay bundle row collection requires tuple attributes")
        rows.extend(value)
    return tuple(rows)


def _build_replay_validation_rows(
    *,
    hourly_row: S27V2HourlyRuntimeInput,
    next_hourly_row: S27V2HourlyRuntimeInput,
    daily_input: S27V2DailyRuntimeInput,
    transition_kind: S27V2SessionTransitionKind,
) -> tuple[S27V2ValidationLedgerRow, ...]:
    return (
        S27V2ValidationLedgerRow(
            as_of=hourly_row.completed_bar_end_utc,
            validation_name="SOURCE_LOCK_GATE",
            validation_status=S27_V2_SOURCE_LOCK_STATUS,
        ),
        S27V2ValidationLedgerRow(
            as_of=hourly_row.completed_bar_end_utc,
            validation_name="LANE_CLASS",
            validation_status=S27_V2_LANE_CLASS.value,
        ),
        S27V2ValidationLedgerRow(
            as_of=hourly_row.completed_bar_end_utc,
            validation_name="DAILY_ROW_READY",
            validation_status=daily_input.source_status,
        ),
        S27V2ValidationLedgerRow(
            as_of=hourly_row.completed_bar_end_utc,
            validation_name="HOURLY_ROW_READY",
            validation_status=hourly_row.provider_condition_status,
        ),
        S27V2ValidationLedgerRow(
            as_of=hourly_row.completed_bar_end_utc,
            validation_name="FILL_HOURLY_ROW_READY",
            validation_status=next_hourly_row.provider_condition_status,
        ),
        S27V2ValidationLedgerRow(
            as_of=hourly_row.completed_bar_end_utc,
            validation_name="LEVEL_COMPATIBILITY",
            validation_status=daily_input.level_compatibility_status,
        ),
        S27V2ValidationLedgerRow(
            as_of=hourly_row.completed_bar_end_utc,
            validation_name="SESSION_TRANSITION_KIND",
            validation_status=transition_kind.value,
        ),
    )


def _build_provenance_hash_rows(
    as_of: datetime,
    row_groups: tuple[tuple[str, tuple[object, ...]], ...],
) -> tuple[S27V2ProvenanceHashLedgerRow, ...]:
    rows: list[S27V2ProvenanceHashLedgerRow] = []
    for artifact_family, artifacts in row_groups:
        require_non_empty_text("S27 v2 artifact family", artifact_family)
        if not artifacts:
            rows.append(
                S27V2ProvenanceHashLedgerRow(
                    as_of=as_of,
                    artifact_family=artifact_family,
                    row_index=-1,
                    sha256=_stable_row_hash(artifact_family, "EMPTY_ARTIFACT_FAMILY"),
                )
            )
            continue
        for index, artifact in enumerate(artifacts):
            rows.append(
                S27V2ProvenanceHashLedgerRow(
                    as_of=as_of,
                    artifact_family=artifact_family,
                    row_index=index,
                    sha256=_stable_row_hash(artifact_family, artifact),
                )
            )
    return tuple(rows)


def _stable_row_hash(artifact_family: str, artifact: object) -> str:
    from hashlib import sha256

    payload = f"{artifact_family}|{repr(artifact)}"
    return sha256(payload.encode("utf-8")).hexdigest().upper()


def implied_price_for_target_position(
    forecast_context: S27V2ForecastContext,
    *,
    target_position: int,
) -> float:
    forecast_context.validate()
    _require_int("S27 v2 implied price target position", target_position)
    target_capped_forecast = _target_capped_forecast_for_position(forecast_context, target_position)
    _require_target_position_allowed_by_trend(target_position, forecast_context.trend_forecast)
    if abs(target_capped_forecast) >= FORECAST_CAP:
        raise CarverBlocked("S27 v2 adjacent target position is at or beyond forecast cap")
    target_risk_adjusted = target_capped_forecast / forecast_context.scalar
    pre_vol_risk_adjusted = target_risk_adjusted / forecast_context.vol_multiplier_m
    implied = forecast_context.equilibrium_ewma5 - pre_vol_risk_adjusted * forecast_context.sigma_price
    require_finite_positive("S27 v2 implied adjacent limit price", implied)
    return implied


def _target_capped_forecast_for_position(forecast_context: S27V2ForecastContext, target_position: int) -> float:
    _require_int("S27 v2 target capped forecast position", target_position)
    target_capped_forecast = (
        target_position
        / forecast_context.base_position_contracts
        * S27_V2_FORECAST_TO_POSITION_DIVISOR
    )
    _require_finite("S27 v2 target capped forecast", target_capped_forecast)
    return target_capped_forecast


def _adjacent_limit_target_is_priceable(forecast_context: S27V2ForecastContext, target_position: int) -> bool:
    if not _target_position_allowed_by_trend(target_position, forecast_context.trend_forecast):
        return False
    target_capped_forecast = _target_capped_forecast_for_position(forecast_context, target_position)
    return abs(target_capped_forecast) < FORECAST_CAP


def _source_faithful_desired_position_from_context(forecast_context: S27V2ForecastContext) -> int:
    desired_unrounded = (
        forecast_context.capped_forecast
        / S27_V2_FORECAST_TO_POSITION_DIVISOR
        * forecast_context.base_position_contracts
    )
    return _round_contracts(desired_unrounded, RoundingPolicy.NEAREST)


def _target_position_allowed_by_trend(target_position: int, trend_forecast: float) -> bool:
    _require_int("S27 v2 trend-permission target position", target_position)
    _require_finite("S27 v2 trend forecast", trend_forecast)
    if trend_forecast == 0.0:
        raise CarverBlocked("S27 v2 zero trend target-position permission is fail-closed")
    if target_position == 0:
        return True
    return target_position > 0 if trend_forecast > 0.0 else target_position < 0


def _require_target_position_allowed_by_trend(target_position: int, trend_forecast: float) -> None:
    if not _target_position_allowed_by_trend(target_position, trend_forecast):
        raise CarverBlocked("S27 v2 target position is vetoed by EWMAC trend")


def _validate_order_plan_internal_consistency(order_plan: S27V2OrderPlan) -> None:
    _validate_utc_hour("S27 v2 order plan decision as_of", order_plan.decision_as_of)
    _require_int("S27 v2 order plan current position", order_plan.current_position)
    _require_int("S27 v2 order plan desired position", order_plan.desired_rounded_position)
    _validate_order_plan_forecast_context(order_plan)
    if order_plan.limit_orders and order_plan.market_orders:
        raise CarverBlocked("S27 v2 order plan cannot mix limit and market orders")
    gap = order_plan.desired_rounded_position - order_plan.current_position
    if not order_plan.limit_orders and not order_plan.market_orders and gap != 0:
        raise CarverBlocked("S27 v2 order plan with nonzero desired gap requires an order")
    if order_plan.limit_orders:
        if abs(gap) > 1:
            raise CarverBlocked("S27 v2 limit order plan cannot carry desired gap greater than one")
        if gap != 0 and not any(order.target_position_after_fill == order_plan.desired_rounded_position for order in order_plan.limit_orders):
            raise CarverBlocked("S27 v2 limit order plan must include an order toward desired position")
    for limit in order_plan.limit_orders:
        if limit.decision_as_of != order_plan.decision_as_of:
            raise CarverBlocked("S27 v2 limit order decision time must match order plan")
        if limit.order_kind is not S27V2OrderKind.LIMIT:
            raise CarverBlocked("S27 v2 limit order row has wrong order kind")
        if limit.cost_treatment is not S27V2FillCostTreatment.COMMISSION_ONLY:
            raise CarverBlocked("S27 v2 limit order must be commission-only")
        _validate_order_side_quantity_and_target(
            side=limit.side,
            quantity=limit.quantity,
            current_position=order_plan.current_position,
            target_position_after_fill=limit.target_position_after_fill,
        )
        if limit.quantity != 1:
            raise CarverBlocked("S27 v2 adjacent limit orders must be one contract")
        require_finite_positive("S27 v2 limit order price", limit.limit_price)
        _validate_limit_order_source_condition(order_plan, limit)
    _validate_limit_order_completeness(order_plan)
    if len(order_plan.market_orders) > 1:
        raise CarverBlocked("S27 v2 order plan supports one market order per decision")
    for market in order_plan.market_orders:
        if market.decision_as_of != order_plan.decision_as_of:
            raise CarverBlocked("S27 v2 market order decision time must match order plan")
        if market.order_kind is not S27V2OrderKind.MARKET:
            raise CarverBlocked("S27 v2 market order row has wrong order kind")
        if market.cost_treatment is not S27V2FillCostTreatment.COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD:
            raise CarverBlocked("S27 v2 market order must include normal spread treatment")
        require_non_empty_text("S27 v2 market order trigger", market.trigger)
        if market.trigger not in S27_V2_ALLOWED_MARKET_ORDER_TRIGGERS:
            raise CarverBlocked("S27 v2 market order trigger is not source-locked")
        _validate_order_side_quantity_and_target(
            side=market.side,
            quantity=market.quantity,
            current_position=order_plan.current_position,
            target_position_after_fill=market.target_position_after_fill,
        )
        if market.target_position_after_fill != order_plan.desired_rounded_position:
            raise CarverBlocked("S27 v2 market order target must match desired position")
        _validate_market_trigger_source_condition(order_plan, market)


def _validate_order_plan_forecast_context(order_plan: S27V2OrderPlan) -> None:
    if order_plan.forecast_context is None:
        raise CarverBlocked("S27 v2 order plan requires forecast-context provenance")
    order_plan.forecast_context.validate()
    if order_plan.forecast_context.as_of != order_plan.decision_as_of:
        raise CarverBlocked("S27 v2 order plan forecast context must match decision time")
    expected_desired = _source_faithful_desired_position_from_context(order_plan.forecast_context)
    if expected_desired != order_plan.desired_rounded_position:
        raise CarverBlocked("S27 v2 order plan desired position must match forecast context")
    _require_target_position_allowed_by_trend(
        order_plan.desired_rounded_position,
        order_plan.forecast_context.trend_forecast,
    )


def _validate_limit_order_source_condition(
    order_plan: S27V2OrderPlan,
    limit: S27V2LimitOrderRow,
) -> None:
    context = order_plan.forecast_context
    if context is None:
        raise CarverBlocked("S27 v2 limit order validation requires forecast context")
    expected_price = implied_price_for_target_position(
        context,
        target_position=limit.target_position_after_fill,
    )
    if abs(limit.limit_price - expected_price) > 1e-9:
        raise CarverBlocked("S27 v2 limit order price must match source-implied target price")


def _validate_limit_order_completeness(order_plan: S27V2OrderPlan) -> None:
    if order_plan.market_orders:
        return
    context = order_plan.forecast_context
    if context is None:
        raise CarverBlocked("S27 v2 limit completeness validation requires forecast context")
    expected_limits = _source_required_adjacent_limit_orders(
        context,
        current_position=order_plan.current_position,
    )
    if _limit_order_signature_tuple(order_plan.limit_orders) != _limit_order_signature_tuple(expected_limits):
        raise CarverBlocked("S27 v2 limit order plan must equal source-required adjacent limit set")


def _source_required_adjacent_limit_orders(
    forecast_context: S27V2ForecastContext,
    *,
    current_position: int,
) -> tuple[S27V2LimitOrderRow, ...]:
    _require_int("S27 v2 adjacent limit current position", current_position)
    required: list[S27V2LimitOrderRow] = []
    if (
        forecast_context.capped_forecast < FORECAST_CAP
        and _adjacent_limit_target_is_priceable(forecast_context, current_position + 1)
    ):
        required.append(
            S27V2LimitOrderRow(
                decision_as_of=forecast_context.as_of,
                side=S27V2OrderSide.BUY,
                quantity=1,
                target_position_after_fill=current_position + 1,
                limit_price=implied_price_for_target_position(
                    forecast_context,
                    target_position=current_position + 1,
                ),
            )
        )
    if (
        forecast_context.capped_forecast > -FORECAST_CAP
        and _adjacent_limit_target_is_priceable(forecast_context, current_position - 1)
    ):
        required.append(
            S27V2LimitOrderRow(
                decision_as_of=forecast_context.as_of,
                side=S27V2OrderSide.SELL,
                quantity=1,
                target_position_after_fill=current_position - 1,
                limit_price=implied_price_for_target_position(
                    forecast_context,
                    target_position=current_position - 1,
                ),
            )
        )
    return tuple(required)


def _limit_order_signature_tuple(
    limits: tuple[S27V2LimitOrderRow, ...],
) -> tuple[tuple[S27V2OrderSide, int, int, float], ...]:
    return tuple(
        sorted(
            (
                limit.side.value,
                limit.quantity,
                limit.target_position_after_fill,
                round(limit.limit_price, 12),
            )
            for limit in limits
        )
    )


def _validate_market_trigger_source_condition(
    order_plan: S27V2OrderPlan,
    market: S27V2MarketOrderRow,
) -> None:
    context = order_plan.forecast_context
    if context is None:
        raise CarverBlocked("S27 v2 market trigger validation requires forecast context")
    gap = order_plan.desired_rounded_position - order_plan.current_position
    if market.quantity != abs(gap):
        raise CarverBlocked("S27 v2 market order quantity must equal desired position gap")
    if market.trigger == "DESIRED_POSITION_MORE_THAN_ONE_CONTRACT_FROM_CURRENT":
        if abs(gap) <= 1:
            raise CarverBlocked("S27 v2 large-gap market trigger requires gap greater than one")
        return
    if market.trigger == "CAP_BOUND_NO_BUY_LIMIT_SIDE":
        if not (gap > 0 and abs(gap) == 1 and context.capped_forecast >= FORECAST_CAP):
            raise CarverBlocked("S27 v2 buy cap-bound market trigger does not match forecast context")
        return
    if market.trigger == "CAP_BOUND_NO_SELL_LIMIT_SIDE":
        if not (gap < 0 and abs(gap) == 1 and context.capped_forecast <= -FORECAST_CAP):
            raise CarverBlocked("S27 v2 sell cap-bound market trigger does not match forecast context")
        return
    if market.trigger == "CAP_BOUND_NO_ADJACENT_LIMIT_SIDE":
        if abs(gap) != 1:
            raise CarverBlocked("S27 v2 no-adjacent-limit market trigger requires one-contract gap")
        if _adjacent_limit_target_is_priceable(context, order_plan.desired_rounded_position):
            raise CarverBlocked("S27 v2 no-adjacent-limit trigger has a priceable desired target")
        return
    if market.trigger == "ADJACENT_DESIRED_TARGET_UNPRICEABLE_AT_CAP":
        if abs(gap) != 1:
            raise CarverBlocked("S27 v2 adjacent-cap market trigger requires one-contract gap")
        if _adjacent_limit_target_is_priceable(context, order_plan.desired_rounded_position):
            raise CarverBlocked("S27 v2 adjacent-cap market trigger has a priceable desired target")
        return
    raise CarverBlocked("S27 v2 market trigger source condition is unresolved")


def _validate_working_order_state_internal_consistency(state: S27V2WorkingOrderState) -> None:
    _validate_order_plan_internal_consistency(
        S27V2OrderPlan(
            decision_as_of=state.opened_as_of,
            current_position=state.current_position,
            desired_rounded_position=state.desired_rounded_position,
            limit_orders=state.limit_orders,
            market_orders=state.market_orders,
            end_of_day_cancel_reset_required=True,
            forecast_context=state.forecast_context,
            raw_symbol=state.raw_symbol,
            session_id=state.session_id,
        )
    )


def _validate_order_side_quantity_and_target(
    *,
    side: S27V2OrderSide,
    quantity: int,
    current_position: int,
    target_position_after_fill: int,
) -> None:
    _require_int("S27 v2 order quantity", quantity)
    _require_int("S27 v2 order target position", target_position_after_fill)
    if quantity <= 0:
        raise CarverBlocked("S27 v2 order quantity must be positive")
    if side is S27V2OrderSide.BUY:
        expected = current_position + quantity
    elif side is S27V2OrderSide.SELL:
        expected = current_position - quantity
    else:
        raise CarverBlocked("S27 v2 order side is unresolved")
    if target_position_after_fill != expected:
        raise CarverBlocked("S27 v2 order side/quantity/target position are inconsistent")


def _fill_row(
    *,
    decision_as_of: datetime,
    fill_as_of: datetime,
    side: S27V2OrderSide,
    quantity: int,
    fill_price: float,
    order_kind: S27V2OrderKind,
    cost_treatment: S27V2FillCostTreatment,
    commission_per_contract: float,
    normal_bid_ask_spread: float,
) -> S27V2FillRow:
    require_finite_positive("S27 v2 fill price", fill_price)
    _require_int("S27 v2 fill quantity", quantity)
    if quantity <= 0:
        raise CarverBlocked("S27 v2 fill quantity must be positive")
    commission = commission_per_contract * quantity
    spread = 0.0
    if cost_treatment is S27V2FillCostTreatment.COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD:
        spread = normal_bid_ask_spread * quantity
    return S27V2FillRow(
        decision_as_of=decision_as_of,
        fill_as_of=fill_as_of,
        side=side,
        quantity=quantity,
        fill_price=fill_price,
        order_kind=order_kind,
        cost_treatment=cost_treatment,
        commission_cost=commission,
        spread_cost=spread,
        total_cost=commission + spread,
        fill_source_status=S27_V2_FILL_SOURCE_STATUS,
    )


def _ewma_series(values: tuple[float, ...], span: int) -> list[float]:
    if not values:
        raise CarverBlocked("S27 v2 EWMA series requires values")
    if isinstance(span, bool) or not isinstance(span, Integral) or span < 2:
        raise CarverBlocked("S27 v2 EWMA span must be an integer at least 2")
    alpha = 2.0 / (span + 1.0)
    first = values[0]
    _require_finite("S27 v2 EWMA input", first)
    smoothed = first
    output = [smoothed]
    for value in values[1:]:
        _require_finite("S27 v2 EWMA input", value)
        smoothed = alpha * value + (1.0 - alpha) * smoothed
        output.append(smoothed)
    return output


def _expanding_quantile(values: list[float], current_value: float) -> float:
    if not values:
        raise CarverBlocked("S27 v2 quantile requires history")
    _require_finite("S27 v2 quantile current value", current_value)
    for value in values:
        _require_finite("S27 v2 quantile history value", value)
    count_less_or_equal = sum(1 for value in values if value <= current_value)
    return count_less_or_equal / len(values)


def _round_contracts(value: float, policy: RoundingPolicy) -> int:
    _require_finite("S27 v2 desired contracts", value)
    if policy is RoundingPolicy.NEAREST:
        return int(round(value))
    if policy is RoundingPolicy.FLOOR:
        from math import floor

        return floor(value)
    if policy is RoundingPolicy.CEILING:
        from math import ceil

        return ceil(value)
    if policy is RoundingPolicy.TRUNCATE:
        return int(value)
    raise CarverBlocked("S27 v2 rounding policy is unresolved")


def _validate_daily_sequence(rows: tuple[S27V2DailyRuntimeInput, ...]) -> None:
    if not rows:
        raise CarverBlocked("S27 v2 daily runtime rows are required")
    previous_timestamp: datetime | None = None
    previous_date: date | None = None
    for row in rows:
        row.validate()
        row_date = _parse_iso_date("S27 v2 completed trading date", row.completed_trading_date)
        if previous_timestamp is not None and row.completed_bar_timestamp <= previous_timestamp:
            raise CarverBlocked("S27 v2 daily rows must be strictly increasing")
        if previous_date is not None and row_date <= previous_date:
            raise CarverBlocked("S27 v2 completed trading dates must be strictly increasing")
        previous_timestamp = row.completed_bar_timestamp
        previous_date = row_date


def _validate_ohlc(open_price: float, high: float, low: float, close: float) -> None:
    require_finite_positive("S27 v2 hourly open", open_price)
    require_finite_positive("S27 v2 hourly high", high)
    require_finite_positive("S27 v2 hourly low", low)
    require_finite_positive("S27 v2 hourly close", close)
    if high < low:
        raise CarverBlocked("S27 v2 hourly high must be greater than low")
    if high < open_price or high < close:
        raise CarverBlocked("S27 v2 hourly high must bound open and close")
    if low > open_price or low > close:
        raise CarverBlocked("S27 v2 hourly low must bound open and close")


def _validate_utc_hour(name: str, timestamp: datetime) -> None:
    _validate_utc_timestamp(name, timestamp)
    if timestamp.minute or timestamp.second or timestamp.microsecond:
        raise CarverBlocked(f"{name} must be hour-aligned")


def _validate_utc_timestamp(name: str, timestamp: datetime) -> None:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise CarverBlocked(f"{name} must be timezone-aware")
    if timestamp.utcoffset() != timedelta(0):
        raise CarverBlocked(f"{name} must be UTC")


def _validate_iso_date(name: str, value: str) -> None:
    _parse_iso_date(name, value)


def _parse_iso_date(name: str, value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be an ISO calendar date") from exc
    if parsed.isoformat() != value:
        raise CarverBlocked(f"{name} must be an ISO calendar date")
    return parsed


def _require_exact(name: str, actual: str, expected: str) -> None:
    require_non_empty_text(name, actual)
    if actual != expected:
        raise CarverBlocked(f"{name} must be {expected}")


def _require_close(name: str, actual: float, expected: float) -> None:
    _require_finite(name, actual)
    if abs(actual - expected) > 1e-12:
        raise CarverBlocked(f"{name} must be {expected}")


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")


def _require_finite_nonnegative(name: str, value: float) -> None:
    _require_finite(name, value)
    if value < 0.0:
        raise CarverBlocked(f"{name} must be non-negative")


def _require_int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise CarverBlocked(f"{name} must be an integer")

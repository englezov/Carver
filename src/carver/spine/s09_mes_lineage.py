from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from math import isfinite
from numbers import Real

from .m0 import CarverBlocked


S09_MES_LINEAGE_READINESS_KEYS = (
    "continuous_lineage_status",
    "roll_plan_status",
    "back_adjustment_status",
    "provider_condition_admission_status",
    "official_lifecycle_evidence_status",
    "roll_trading_day_semantics_status",
    "annual_risk_runtime_status",
    "daily_price_risk_runtime_status",
    "cost_source_status",
    "risk_adjusted_cost_status",
    "speed_cost_eligibility_status",
    "eligible_speed_set_status",
    "strategy_input_readiness_status",
)


def default_s09_mes_lineage_readiness_statuses() -> dict[str, str]:
    return {
        "continuous_lineage_status": "PROVISIONAL_LOCAL_LINEAGE_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_LOCKED",
        "roll_plan_status": "PROVISIONAL_PROVIDER_DATE_ROLL_PLAN_TRADING_DAY_SEMANTICS_NOT_LOCKED",
        "back_adjustment_status": "PROVISIONAL_LOCAL_BACK_ADJUSTMENT_NOT_STRATEGY_INPUT",
        "provider_condition_admission_status": "LOCKED",
        "official_lifecycle_evidence_status": "FAIL_CLOSED_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_HASH_BOUND",
        "roll_trading_day_semantics_status": "FAIL_CLOSED_S09_MES_PROVIDER_DATE_ROLL_SEMANTICS_NOT_SOURCE_LOCKED",
        "annual_risk_runtime_status": "FAIL_CLOSED_S09_MES_ANNUAL_RISK_RUNTIME_NOT_LOCKED",
        "daily_price_risk_runtime_status": "FAIL_CLOSED_S09_MES_DAILY_PRICE_RISK_RUNTIME_NOT_LOCKED",
        "cost_source_status": "FAIL_CLOSED_S09_MES_COST_SOURCE_NOT_LOCKED",
        "risk_adjusted_cost_status": "FAIL_CLOSED_S09_MES_RISK_ADJUSTED_COST_NOT_LOCKED",
        "speed_cost_eligibility_status": "FAIL_CLOSED_S09_MES_SPEED_COST_ELIGIBILITY_NOT_LOCKED",
        "eligible_speed_set_status": "FAIL_CLOSED_S09_MES_ELIGIBLE_SPEED_SET_NOT_LOCKED",
        "strategy_input_readiness_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
    }


@dataclass(frozen=True)
class S09MESDatedContractBar:
    raw_symbol: str
    completed_trading_date: date
    open: float
    high: float
    low: float
    close: float
    volume: float
    provider_condition_classification: str
    source_raw_sha256: str
    provider_condition_admission_policy: str = "NORMAL_PROVIDER_CONDITION_ONLY"
    completed_trading_date_policy: str = "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE"

    def validate(self) -> None:
        _require_mes_symbol(self.raw_symbol)
        if not isinstance(self.completed_trading_date, date):
            raise CarverBlocked("S09 MES bar requires a completed trading date")
        _require_positive("S09 MES open", self.open)
        _require_positive("S09 MES high", self.high)
        _require_positive("S09 MES low", self.low)
        _require_positive("S09 MES close", self.close)
        _require_non_negative("S09 MES volume", self.volume)
        if self.high < max(self.open, self.low, self.close):
            raise CarverBlocked("S09 MES high is inconsistent with OHLC")
        if self.low > min(self.open, self.high, self.close):
            raise CarverBlocked("S09 MES low is inconsistent with OHLC")
        if self.provider_condition_classification == "NORMAL_PROVIDER_CONDITION":
            if self.provider_condition_admission_policy not in {
                "NORMAL_PROVIDER_CONDITION_ONLY",
            }:
                raise CarverBlocked("S09 MES normal provider-condition row has an unresolved admission policy")
        elif self.provider_condition_classification == "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY":
            if self.provider_condition_admission_policy not in {
                "SOURCE_NATIVE_DEGRADED_OHLCV_COLD_SHAPE_BASED_POLICY_LOCKED",
            }:
                raise CarverBlocked("S09 MES degraded provider-condition row requires an explicit locked admission policy")
        else:
            raise CarverBlocked("S09 MES lineage admits only normal rows or explicitly policy-admitted degraded OHLCV rows")
        if not self.source_raw_sha256:
            raise CarverBlocked("S09 MES source raw SHA256 is missing")
        if self.completed_trading_date_policy not in {
            "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE",
            "SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE",
        }:
            raise CarverBlocked("S09 MES completed trading-date policy is unresolved")


@dataclass(frozen=True)
class S09MESDatedContractDefinition:
    raw_symbol: str
    expiration: datetime
    product_code: str
    currency: str
    multiplier: float
    tick_size: float
    venue: str
    lifecycle_source: str

    def validate(self) -> None:
        _require_mes_symbol(self.raw_symbol)
        if self.expiration.tzinfo is None or self.expiration.utcoffset() is None:
            raise CarverBlocked("S09 MES expiration must be timezone-aware")
        if self.product_code != "MES":
            raise CarverBlocked("S09 MES definition product code must be MES")
        if self.currency != "USD":
            raise CarverBlocked("S09 MES definition currency must be USD")
        if self.venue not in {"XCME", "CME", "GLBX"}:
            raise CarverBlocked("S09 MES definition venue is unresolved")
        _require_positive("S09 MES multiplier", self.multiplier)
        if self.multiplier != 5.0:
            raise CarverBlocked("S09 MES multiplier must be locked to 5")
        _require_positive("S09 MES tick size", self.tick_size)
        if self.tick_size != 0.25:
            raise CarverBlocked("S09 MES tick size must be locked to 0.25")
        if not self.lifecycle_source:
            raise CarverBlocked("S09 MES lifecycle source is missing")


@dataclass(frozen=True)
class S09MESRollDateNormalizationAuthority:
    provider_date: date
    completed_trading_date: date
    authority_source: str
    authority_sha256: str

    def validate(self) -> None:
        if type(self.provider_date) is not date:
            raise CarverBlocked("S09 MES roll normalization provider date is missing")
        if type(self.completed_trading_date) is not date:
            raise CarverBlocked("S09 MES roll normalization completed trading date is missing")
        if not self.authority_source:
            raise CarverBlocked("S09 MES roll normalization authority source is missing")
        if not isinstance(self.authority_sha256, str) or len(self.authority_sha256) != 64:
            raise CarverBlocked("S09 MES roll normalization authority hash is missing")
        try:
            int(self.authority_sha256, 16)
        except ValueError as exc:
            raise CarverBlocked("S09 MES roll normalization authority hash is invalid") from exc


@dataclass(frozen=True)
class S09MESLineageRequest:
    symbol_order: tuple[str, ...]
    bars_by_symbol: dict[str, tuple[S09MESDatedContractBar, ...]]
    definitions_by_symbol: dict[str, S09MESDatedContractDefinition]
    minimum_target_rows: int
    roll_buffer_completed_days: int = 5
    strategy_input_readiness_statuses: dict[str, str] | None = None

    def validate(self) -> None:
        if not self.symbol_order:
            raise CarverBlocked("S09 MES lineage requires at least one contract")
        if len(set(self.symbol_order)) != len(self.symbol_order):
            raise CarverBlocked("S09 MES symbol order contains duplicates")
        if self.roll_buffer_completed_days <= 0:
            raise CarverBlocked("S09 MES roll buffer must be positive")
        if self.minimum_target_rows <= 0:
            raise CarverBlocked("S09 MES minimum target rows must be positive")
        if set(self.bars_by_symbol) != set(self.symbol_order):
            raise CarverBlocked("S09 MES bars must exactly match symbol order")
        if set(self.definitions_by_symbol) != set(self.symbol_order):
            raise CarverBlocked("S09 MES definitions must exactly match symbol order")
        _validate_readiness_statuses(self.strategy_input_readiness_statuses)

        previous_month_key: tuple[int, int] | None = None
        for symbol in self.symbol_order:
            _require_mes_symbol(symbol)
            month_key = _symbol_month_key(symbol)
            if previous_month_key is not None and month_key <= previous_month_key:
                raise CarverBlocked("S09 MES symbols must be in increasing contract-month order")
            previous_month_key = month_key
            self.definitions_by_symbol[symbol].validate()
            bars = self.bars_by_symbol[symbol]
            if not bars:
                raise CarverBlocked("S09 MES contract has no bars")
            previous_date: date | None = None
            for bar in bars:
                bar.validate()
                if bar.raw_symbol != symbol:
                    raise CarverBlocked("S09 MES bar symbol does not match its group")
                if previous_date is not None and bar.completed_trading_date <= previous_date:
                    raise CarverBlocked("S09 MES bars must be strictly increasing inside a contract")
                previous_date = bar.completed_trading_date


@dataclass(frozen=True)
class S09MESRollEvent:
    old_symbol: str
    new_symbol: str
    expiration_date: date
    roll_buffer_date: date
    roll_transition_date: date
    old_close_on_roll_date: float
    new_close_on_roll_date: float
    old_history_additive_adjustment: float
    old_source_raw_sha256: str
    new_source_raw_sha256: str


@dataclass(frozen=True)
class S09MESAdjustedDailyRow:
    completed_trading_date: date
    source_raw_symbol: str
    raw_open: float
    raw_high: float
    raw_low: float
    raw_close: float
    adjusted_open: float
    adjusted_high: float
    adjusted_low: float
    adjusted_close: float
    volume: float
    cumulative_additive_adjustment: float
    source_raw_sha256: str
    provider_condition_classification: str
    provider_condition_admission_policy: str
    completed_trading_date_policy: str


@dataclass(frozen=True)
class S09MESLineageResult:
    adjusted_rows: tuple[S09MESAdjustedDailyRow, ...]
    roll_events: tuple[S09MESRollEvent, ...]
    source_contracts: tuple[str, ...]
    continuous_lineage_status: str
    roll_plan_status: str
    back_adjustment_status: str
    provider_condition_admission_status: str
    minimum_target_rows: int
    strategy_input_readiness_statuses: dict[str, str]

    @property
    def ready_for_lineage_use(self) -> bool:
        blockers = tuple(
            value for value in self.strategy_input_readiness_statuses.values()
            if value.startswith("FAIL_CLOSED") or value.startswith("PROVISIONAL")
        )
        return (
            self.continuous_lineage_status == "LOCKED"
            and self.roll_plan_status == "LOCKED"
            and self.back_adjustment_status == "LOCKED"
            and self.provider_condition_admission_status == "LOCKED"
            and not blockers
            and len(self.adjusted_rows) >= self.minimum_target_rows
        )


def build_s09_mes_lineage(request: S09MESLineageRequest) -> S09MESLineageResult:
    request.validate()
    readiness_statuses = _readiness_statuses_for_request(request)
    raw_segments: list[tuple[S09MESDatedContractBar, ...]] = []
    roll_events: list[S09MESRollEvent] = []
    current_cutoff: date | None = None

    for index, symbol in enumerate(request.symbol_order):
        bars = request.bars_by_symbol[symbol]
        segment_end: date | None = None
        if index < len(request.symbol_order) - 1:
            next_symbol = request.symbol_order[index + 1]
            event = _select_roll_event(
                old_symbol=symbol,
                new_symbol=next_symbol,
                old_bars=bars,
                new_bars=request.bars_by_symbol[next_symbol],
                old_definition=request.definitions_by_symbol[symbol],
                buffer_completed_days=request.roll_buffer_completed_days,
            )
            roll_events.append(event)
            segment_end = event.roll_transition_date

        segment = tuple(
            bar for bar in bars
            if (current_cutoff is None or bar.completed_trading_date > current_cutoff)
            and (segment_end is None or bar.completed_trading_date <= segment_end)
        )
        if not segment:
            raise CarverBlocked("S09 MES roll segmentation produced an empty segment")
        raw_segments.append(segment)

        if index < len(request.symbol_order) - 1:
            current_cutoff = event.roll_transition_date

    adjusted_rows: list[S09MESAdjustedDailyRow] = []
    cumulative_adjustments_by_segment = _old_history_adjustments_by_segment(tuple(roll_events))
    for segment_index, segment in enumerate(raw_segments):
        adjustment = cumulative_adjustments_by_segment[segment_index]
        for bar in segment:
            adjusted_rows.append(_adjust_row(bar, adjustment))

    result = S09MESLineageResult(
        adjusted_rows=tuple(adjusted_rows),
        roll_events=tuple(roll_events),
        source_contracts=request.symbol_order,
        continuous_lineage_status=readiness_statuses["continuous_lineage_status"],
        roll_plan_status=readiness_statuses["roll_plan_status"],
        back_adjustment_status=readiness_statuses["back_adjustment_status"],
        provider_condition_admission_status=readiness_statuses["provider_condition_admission_status"],
        minimum_target_rows=request.minimum_target_rows,
        strategy_input_readiness_statuses=readiness_statuses,
    )
    _validate_result(result)
    return result


def evaluate_s09_mes_lineage_strategy_readiness(result: S09MESLineageResult) -> dict[str, str]:
    return dict(result.strategy_input_readiness_statuses)


def _readiness_statuses_for_request(request: S09MESLineageRequest) -> dict[str, str]:
    if request.strategy_input_readiness_statuses is None:
        return default_s09_mes_lineage_readiness_statuses()
    return dict(request.strategy_input_readiness_statuses)


def _validate_readiness_statuses(statuses: dict[str, str] | None) -> None:
    if statuses is None:
        return
    if set(statuses) != set(S09_MES_LINEAGE_READINESS_KEYS):
        raise CarverBlocked("S09 MES lineage readiness status contract is incomplete")
    for key, value in statuses.items():
        if not isinstance(value, str) or not value:
            raise CarverBlocked(f"S09 MES lineage readiness status is invalid for {key}")
    for key in (
        "continuous_lineage_status",
        "roll_plan_status",
        "back_adjustment_status",
        "provider_condition_admission_status",
    ):
        if statuses[key] != "LOCKED" and not statuses[key].startswith("PROVISIONAL"):
            raise CarverBlocked(f"S09 MES lineage core readiness status is invalid for {key}")


def normalize_s09_mes_roll_provider_date(
    *,
    provider_date: date,
    authority_rows: tuple[S09MESRollDateNormalizationAuthority, ...],
) -> date:
    if type(provider_date) is not date:
        raise CarverBlocked("S09 MES roll provider date is missing")
    if not authority_rows:
        raise CarverBlocked("S09 MES roll provider date requires explicit completed-date authority")

    mapping: dict[date, date] = {}
    for row in authority_rows:
        row.validate()
        existing = mapping.get(row.provider_date)
        if existing is not None and existing != row.completed_trading_date:
            raise CarverBlocked("S09 MES roll provider date has conflicting completed-date authorities")
        mapping[row.provider_date] = row.completed_trading_date

    normalized = mapping.get(provider_date)
    if normalized is None:
        raise CarverBlocked("S09 MES roll provider date is not covered by completed-date authority")
    return normalized


def _select_roll_event(
    *,
    old_symbol: str,
    new_symbol: str,
    old_bars: tuple[S09MESDatedContractBar, ...],
    new_bars: tuple[S09MESDatedContractBar, ...],
    old_definition: S09MESDatedContractDefinition,
    buffer_completed_days: int,
) -> S09MESRollEvent:
    expiration_date = old_definition.expiration.date()
    old_pre_expiry_dates = tuple(
        bar.completed_trading_date
        for bar in old_bars
        if bar.completed_trading_date < expiration_date
    )
    if len(old_pre_expiry_dates) < buffer_completed_days:
        raise CarverBlocked("S09 MES lifecycle buffer has insufficient old-contract dates")
    roll_buffer_date = old_pre_expiry_dates[-buffer_completed_days]
    old_by_date = {bar.completed_trading_date: bar for bar in old_bars}
    new_by_date = {bar.completed_trading_date: bar for bar in new_bars}
    common_dates = sorted(date_ for date_ in old_by_date if date_ in new_by_date and date_ <= roll_buffer_date)
    if not common_dates:
        raise CarverBlocked("S09 MES roll pair has no normal-provider overlap on or before buffer date")
    roll_date = common_dates[-1]
    old_bar = old_by_date[roll_date]
    new_bar = new_by_date[roll_date]
    return S09MESRollEvent(
        old_symbol=old_symbol,
        new_symbol=new_symbol,
        expiration_date=expiration_date,
        roll_buffer_date=roll_buffer_date,
        roll_transition_date=roll_date,
        old_close_on_roll_date=old_bar.close,
        new_close_on_roll_date=new_bar.close,
        old_history_additive_adjustment=new_bar.close - old_bar.close,
        old_source_raw_sha256=old_bar.source_raw_sha256,
        new_source_raw_sha256=new_bar.source_raw_sha256,
    )


def _adjust_row(bar: S09MESDatedContractBar, offset: float) -> S09MESAdjustedDailyRow:
    return S09MESAdjustedDailyRow(
        completed_trading_date=bar.completed_trading_date,
        source_raw_symbol=bar.raw_symbol,
        raw_open=bar.open,
        raw_high=bar.high,
        raw_low=bar.low,
        raw_close=bar.close,
        adjusted_open=bar.open + offset,
        adjusted_high=bar.high + offset,
        adjusted_low=bar.low + offset,
        adjusted_close=bar.close + offset,
        volume=bar.volume,
        cumulative_additive_adjustment=offset,
        source_raw_sha256=bar.source_raw_sha256,
        provider_condition_classification=bar.provider_condition_classification,
        provider_condition_admission_policy=bar.provider_condition_admission_policy,
        completed_trading_date_policy=bar.completed_trading_date_policy,
    )


def _old_history_adjustments_by_segment(roll_events: tuple[S09MESRollEvent, ...]) -> tuple[float, ...]:
    if not roll_events:
        return (0.0,)
    adjustments: list[float] = []
    cumulative = 0.0
    for event in reversed(roll_events):
        adjustments.append(cumulative)
        cumulative += event.old_history_additive_adjustment
    adjustments.append(cumulative)
    return tuple(reversed(adjustments))


def _validate_result(result: S09MESLineageResult) -> None:
    if not result.adjusted_rows:
        raise CarverBlocked("S09 MES lineage produced no adjusted rows")
    previous: date | None = None
    for row in result.adjusted_rows:
        if previous is not None and row.completed_trading_date <= previous:
            raise CarverBlocked("S09 MES adjusted rows must be strictly increasing")
        previous = row.completed_trading_date


def _require_mes_symbol(value: str) -> None:
    if not isinstance(value, str) or not value.startswith("MES") or len(value) < 5:
        raise CarverBlocked("S09 MES lineage is locked to MES dated contracts only")


def _symbol_month_key(symbol: str) -> tuple[int, int]:
    month_codes = {"F": 1, "G": 2, "H": 3, "J": 4, "K": 5, "M": 6, "N": 7, "Q": 8, "U": 9, "V": 10, "X": 11, "Z": 12}
    month_code = symbol[3]
    if month_code not in month_codes:
        raise CarverBlocked("S09 MES raw symbol has unresolved month code")
    year_digits = symbol[4:]
    if not year_digits.isdigit():
        raise CarverBlocked("S09 MES raw symbol has unresolved year code")
    year = int(year_digits)
    if year < 100:
        year = 2020 + year if year <= 6 else 2010 + year
    return year, month_codes[month_code]


def _require_positive(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"{name} must be positive")


def _require_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be non-negative")

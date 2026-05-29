from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from .daily_bars import CompletedDailyMarketBar
from .m0 import BackAdjustmentSpec, CostSourceSpec, RollRuleSpec, SessionCalendarSpec, CarverBlocked


@dataclass(frozen=True)
class ContinuousContractRuleSet:
    session_calendar: SessionCalendarSpec
    roll_rule: RollRuleSpec
    back_adjustment: BackAdjustmentSpec
    cost_source: CostSourceSpec

    def require_locked(self) -> None:
        self.session_calendar.require_locked()
        self.roll_rule.require_locked()
        self.back_adjustment.require_locked()
        self.cost_source.require_locked()


@dataclass(frozen=True)
class ContinuousSeriesRequest:
    rules: ContinuousContractRuleSet
    bars: tuple[CompletedDailyMarketBar, ...]

    def validate(self) -> None:
        if not self.bars:
            raise CarverBlocked("continuous series request requires completed daily bars")
        self.rules.require_locked()
        previous = None
        contract_code = self.bars[0].code
        for bar in self.bars:
            bar.validate()
            if bar.code != contract_code:
                raise CarverBlocked("continuous series request cannot mix contract codes")
            if previous is not None and bar.timestamp <= previous:
                raise CarverBlocked("continuous series bars must be strictly increasing")
            previous = bar.timestamp


@dataclass(frozen=True)
class ContinuousChainRequest:
    rules: ContinuousContractRuleSet
    contract_bars: tuple[tuple[CompletedDailyMarketBar, ...], ...]
    minimum_rows: int

    def validate(self) -> None:
        self.rules.require_locked()
        _require_positive_int("continuous chain minimum rows", self.minimum_rows)
        if not self.contract_bars:
            raise CarverBlocked("continuous chain request requires at least one contract")
        contract_code = ""
        previous_contract_month_key: tuple[int, int] | None = None
        for bars in self.contract_bars:
            if not bars:
                raise CarverBlocked("continuous chain request contains an empty contract")
            first = bars[0]
            first.validate()
            if not contract_code:
                contract_code = first.code
            elif first.code != contract_code:
                raise CarverBlocked("continuous chain request cannot mix contract codes")
            contract_month_key = _contract_month_key(first.contract_month)
            if previous_contract_month_key is not None and contract_month_key <= previous_contract_month_key:
                raise CarverBlocked("continuous chain contract months must be strictly increasing")
            previous_contract_month_key = contract_month_key
            previous_timestamp: datetime | None = None
            for bar in bars:
                bar.validate()
                if bar.code != contract_code:
                    raise CarverBlocked("continuous chain request cannot mix contract codes")
                if bar.contract_month != first.contract_month:
                    raise CarverBlocked("continuous chain bars must be grouped by contract month")
                if previous_timestamp is not None and bar.timestamp <= previous_timestamp:
                    raise CarverBlocked("continuous chain bars must be strictly increasing inside each contract")
                previous_timestamp = bar.timestamp


@dataclass(frozen=True)
class ContinuousChainBuildResult:
    adjusted_bars: tuple[CompletedDailyMarketBar, ...]
    roll_dates: tuple[str, ...]
    source_contract_months: tuple[str, ...]
    minimum_rows: int
    ready: bool

    def validate(self) -> None:
        if not self.adjusted_bars:
            raise CarverBlocked("continuous chain result requires adjusted bars")
        _require_positive_int("continuous chain result minimum rows", self.minimum_rows)
        if len(self.source_contract_months) == 0:
            raise CarverBlocked("continuous chain result requires source contract months")
        previous_timestamp: datetime | None = None
        for bar in self.adjusted_bars:
            bar.validate()
            if previous_timestamp is not None and bar.timestamp <= previous_timestamp:
                raise CarverBlocked("continuous chain adjusted bars must be strictly increasing")
            previous_timestamp = bar.timestamp
        if self.ready != (len(self.adjusted_bars) >= self.minimum_rows):
            raise CarverBlocked("continuous chain readiness flag does not match row count")


def build_continuous_back_adjusted_series(request: ContinuousSeriesRequest) -> tuple[CompletedDailyMarketBar, ...]:
    request.validate()
    raise CarverBlocked("continuous single-series roll/back-adjustment requires a contract chain request")


def build_back_adjusted_continuous_chain(request: ContinuousChainRequest) -> ContinuousChainBuildResult:
    request.validate()
    adjusted_bars: list[CompletedDailyMarketBar] = []
    roll_dates: list[str] = []
    source_contract_months = tuple(bars[0].contract_month for bars in request.contract_bars)
    previous_cutoff: datetime | None = None
    offset = 0.0

    for chain_index, bars in enumerate(request.contract_bars):
        segment = tuple(bar for bar in bars if previous_cutoff is None or bar.timestamp > previous_cutoff)
        if not segment:
            raise CarverBlocked("continuous chain roll segmentation produced an empty segment")
        if chain_index > 0:
            if not adjusted_bars:
                raise CarverBlocked("continuous chain missing prior adjusted bar at roll")
            overlap = _bar_at_timestamp(bars, previous_cutoff)
            roll_dates.append(segment[0].timestamp.date().isoformat())
            offset = adjusted_bars[-1].close - overlap.close
        for bar in segment:
            adjusted_bars.append(_apply_additive_offset(bar, offset))
        previous_cutoff = segment[-1].timestamp

    result = ContinuousChainBuildResult(
        adjusted_bars=tuple(adjusted_bars),
        roll_dates=tuple(roll_dates),
        source_contract_months=source_contract_months,
        minimum_rows=request.minimum_rows,
        ready=len(adjusted_bars) >= request.minimum_rows,
    )
    result.validate()
    return result


def _apply_additive_offset(bar: CompletedDailyMarketBar, offset: float) -> CompletedDailyMarketBar:
    return replace(
        bar,
        open=bar.open + offset,
        high=bar.high + offset,
        low=bar.low + offset,
        close=bar.close + offset,
    )


def _require_positive_int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CarverBlocked(f"{name} must be a positive integer")


def _contract_month_key(value: str) -> tuple[int, int]:
    if not isinstance(value, str) or len(value) != 5 or value[2] != "-":
        raise CarverBlocked("contract month must use MM-YY")
    month, year = value.split("-")
    if not (month.isdigit() and year.isdigit()):
        raise CarverBlocked("contract month must use MM-YY")
    month_number = int(month)
    if month_number < 1 or month_number > 12:
        raise CarverBlocked("contract month has invalid month")
    return (2000 + int(year), month_number)


def _bar_at_timestamp(bars: tuple[CompletedDailyMarketBar, ...], timestamp: datetime | None) -> CompletedDailyMarketBar:
    if timestamp is None:
        raise CarverBlocked("continuous chain overlap timestamp is missing")
    for bar in bars:
        if bar.timestamp == timestamp:
            return bar
    raise CarverBlocked("continuous chain requires overlapping roll date for additive back-adjustment")

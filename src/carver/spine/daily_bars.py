from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from math import isfinite
from numbers import Real

from .m0 import CompletedBar, ContractSpec, CarverBlocked, require_finite_positive
from .minute_export import MinuteBar, MinuteExportSpec
from .web_chart_api import ChartBarType, WebChartBar, WebChartRequest


@dataclass(frozen=True)
class DailyDerivationSession:
    session_start: time
    session_end: time

    def validate(self) -> None:
        if self.session_start >= self.session_end:
            raise CarverBlocked("daily derivation session window is invalid")

    @property
    def expected_minute_count(self) -> int:
        self.validate()
        start = datetime.combine(datetime(2000, 1, 1).date(), self.session_start)
        end = datetime.combine(datetime(2000, 1, 1).date(), self.session_end)
        minutes = int((end - start).total_seconds() // 60)
        if minutes <= 0:
            raise CarverBlocked("daily derivation session has no completed minutes")
        return minutes


@dataclass(frozen=True)
class CompletedDailyMarketBar:
    completed_bar: CompletedBar
    contract: ContractSpec
    contract_month: str
    open: float
    high: float
    low: float
    close: float
    volume: float

    @property
    def timestamp(self) -> datetime:
        return self.completed_bar.timestamp

    @property
    def code(self) -> str:
        return self.contract.code

    def validate(self) -> None:
        self.completed_bar.validate()
        self.contract.validate()
        _require_contract_month(self.contract_month)
        require_finite_positive("completed daily open", self.open)
        require_finite_positive("completed daily high", self.high)
        require_finite_positive("completed daily low", self.low)
        require_finite_positive("completed daily close", self.close)
        _require_finite_non_negative("completed daily volume", self.volume)
        if self.high < max(self.open, self.low, self.close):
            raise CarverBlocked("completed daily high is inconsistent with OHLC")
        if self.low > min(self.open, self.high, self.close):
            raise CarverBlocked("completed daily low is inconsistent with OHLC")


def derive_completed_daily_from_minute_export(
    bars: tuple[MinuteBar, ...],
    spec: MinuteExportSpec,
) -> CompletedDailyMarketBar:
    spec.validate()
    session = DailyDerivationSession(spec.session_start, spec.session_end)
    for bar in bars:
        bar.validate(spec)
    return _derive_completed_daily(
        contract=spec.contract,
        contract_month=spec.contract_month,
        session=session,
        rows=tuple(
            _MinuteLike(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)
            for bar in bars
        ),
    )


def derive_completed_daily_from_web_chart(
    bars: tuple[WebChartBar, ...],
    request: WebChartRequest,
    session: DailyDerivationSession,
) -> CompletedDailyMarketBar:
    request.validate()
    session.validate()
    if request.bar_type is not ChartBarType.MINUTE or request.element_size != 1:
        raise CarverBlocked("daily derivation requires one-minute web chart bars")
    for bar in bars:
        bar.validate(request)
    return _derive_completed_daily(
        contract=request.symbol.contract,
        contract_month=request.symbol.contract_month,
        session=session,
        rows=tuple(
            _MinuteLike(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)
            for bar in bars
        ),
    )


@dataclass(frozen=True)
class _MinuteLike:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def _derive_completed_daily(
    contract: ContractSpec,
    contract_month: str,
    session: DailyDerivationSession,
    rows: tuple[_MinuteLike, ...],
) -> CompletedDailyMarketBar:
    contract.validate()
    _require_contract_month(contract_month)
    session.validate()
    if len(rows) != session.expected_minute_count:
        raise CarverBlocked("minute bars do not cover the full locked session")
    if not rows:
        raise CarverBlocked("daily derivation requires minute bars")

    first_timestamp = rows[0].timestamp
    _validate_timestamp(first_timestamp)
    expected_start = datetime.combine(first_timestamp.date(), session.session_start, tzinfo=first_timestamp.tzinfo)
    expected_last = datetime.combine(first_timestamp.date(), session.session_end, tzinfo=first_timestamp.tzinfo) - timedelta(minutes=1)
    if first_timestamp != expected_start:
        raise CarverBlocked("minute bars do not start at the locked session open")
    if rows[-1].timestamp != expected_last:
        raise CarverBlocked("minute bars do not end at the locked completed session close")

    previous: datetime | None = None
    highs: list[float] = []
    lows: list[float] = []
    volume = 0.0
    for row in rows:
        _validate_timestamp(row.timestamp)
        if row.timestamp.tzinfo != first_timestamp.tzinfo or row.timestamp.date() != first_timestamp.date():
            raise CarverBlocked("minute bars must share one timezone-aware session date")
        if previous is not None and row.timestamp - previous != timedelta(minutes=1):
            raise CarverBlocked("minute bars must be contiguous for daily derivation")
        require_finite_positive("minute open", row.open)
        require_finite_positive("minute high", row.high)
        require_finite_positive("minute low", row.low)
        require_finite_positive("minute close", row.close)
        _require_finite_non_negative("minute volume", row.volume)
        if row.high < max(row.open, row.low, row.close):
            raise CarverBlocked("minute high is inconsistent with OHLC")
        if row.low > min(row.open, row.high, row.close):
            raise CarverBlocked("minute low is inconsistent with OHLC")
        highs.append(row.high)
        lows.append(row.low)
        volume += row.volume
        previous = row.timestamp

    daily_timestamp = datetime.combine(first_timestamp.date(), time(0), tzinfo=first_timestamp.tzinfo)
    daily = CompletedDailyMarketBar(
        completed_bar=CompletedBar(daily_timestamp),
        contract=contract,
        contract_month=contract_month,
        open=rows[0].open,
        high=max(highs),
        low=min(lows),
        close=rows[-1].close,
        volume=volume,
    )
    daily.validate()
    return daily


def _validate_timestamp(timestamp: datetime) -> None:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise CarverBlocked("minute timestamp must be timezone-aware")
    if timestamp.second or timestamp.microsecond:
        raise CarverBlocked("minute timestamp must be minute-aligned")


def _require_contract_month(value: str) -> None:
    if not isinstance(value, str) or len(value) != 5 or value[2] != "-":
        raise CarverBlocked("contract month must use MM-YY")
    month, year = value.split("-")
    if not (month.isdigit() and year.isdigit()):
        raise CarverBlocked("contract month must use MM-YY")
    month_number = int(month)
    if month_number < 1 or month_number > 12:
        raise CarverBlocked("contract month has invalid month")


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be non-negative")

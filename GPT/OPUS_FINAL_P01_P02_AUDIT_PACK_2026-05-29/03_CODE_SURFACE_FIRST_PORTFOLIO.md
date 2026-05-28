# 03 First-Portfolio Code Surface

Use this file to audit the implemented source-native first-spine code. It is synthetic/process code only. Real data execution remains fail-closed until separate authorization and artifact-bound readiness.

---

# FILE: src\carver\spine\m0.py

```text
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from math import isfinite
from numbers import Real


class CarverBlocked(ValueError):
    """Raised when a source-native gate fails closed."""


class LaneClass(StrEnum):
    SOURCE_NATIVE_FUTURES = "SOURCE_NATIVE_FUTURES"
    CFD_DIRECT = "CFD_DIRECT"
    CFD_ADAPTER = "CFD_ADAPTER"


class BarConvention(StrEnum):
    DAILY_COMPLETED = "DAILY_COMPLETED"


class SourceRuleStatus(StrEnum):
    UNRESOLVED = "UNRESOLVED"
    LOCKED = "LOCKED"


@dataclass(frozen=True)
class CompletedBar:
    timestamp: datetime
    convention: BarConvention = BarConvention.DAILY_COMPLETED
    is_complete: bool = True

    def validate(self) -> None:
        if not self.is_complete:
            raise CarverBlocked("bar is not completed")
        if self.convention is not BarConvention.DAILY_COMPLETED:
            raise CarverBlocked("only completed daily bars are authorized in this gate")
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise CarverBlocked("completed daily bar timestamp must be timezone-aware")
        if (
            self.timestamp.hour
            or self.timestamp.minute
            or self.timestamp.second
            or self.timestamp.microsecond
        ):
            raise CarverBlocked("completed daily bar timestamp must be date-aligned")


@dataclass(frozen=True)
class ContractSpec:
    code: str
    name: str
    exchange: str
    currency: str
    multiplier: float
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    def validate(self) -> None:
        require_source_native(self.lane_class)
        require_non_empty_text("contract code", self.code)
        require_non_empty_text("contract name", self.name)
        require_non_empty_text("contract exchange", self.exchange)
        require_non_empty_text("contract currency", self.currency)
        if self.currency != self.currency.upper() or len(self.currency) != 3:
            raise CarverBlocked("contract currency must be an uppercase ISO-style code")
        require_finite_positive("contract multiplier", self.multiplier)


@dataclass(frozen=True)
class SourceRulePlaceholder:
    rule_name: str
    status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED

    def require_locked(self) -> None:
        require_non_empty_text("source rule name", self.rule_name)
        if self.status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked(f"{self.rule_name} source rule is unresolved")


@dataclass(frozen=True)
class SessionCalendarSpec(SourceRulePlaceholder):
    timezone: str = ""

    def require_locked(self) -> None:
        super().require_locked()
        require_non_empty_text("session calendar timezone", self.timezone)


@dataclass(frozen=True)
class RollRuleSpec(SourceRulePlaceholder):
    pass


@dataclass(frozen=True)
class BackAdjustmentSpec(SourceRulePlaceholder):
    pass


@dataclass(frozen=True)
class CostSourceSpec(SourceRulePlaceholder):
    path_hint: str = "config/costs.json"

    def require_locked(self) -> None:
        super().require_locked()
        if self.path_hint != "config/costs.json":
            raise CarverBlocked("cost source must remain config/costs.json")


def require_source_native(lane_class: LaneClass) -> None:
    if lane_class is not LaneClass.SOURCE_NATIVE_FUTURES:
        raise CarverBlocked("lane class must be SOURCE_NATIVE_FUTURES")


def require_finite_positive(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"{name} must be positive")


def require_non_empty_text(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked(f"{name} is unresolved")

```

# FILE: src\carver\spine\m1.py

```text
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from math import ceil, floor

from .m0 import CompletedBar, LaneClass, CarverBlocked, require_finite_positive, require_source_native


class RoundingPolicy(StrEnum):
    NEAREST = "NEAREST"
    FLOOR = "FLOOR"
    CEILING = "CEILING"
    TRUNCATE = "TRUNCATE"


@dataclass(frozen=True)
class TimedValue:
    value: float
    as_of: datetime


@dataclass(frozen=True)
class SizingInput:
    lane_class: LaneClass
    completed_bar: CompletedBar
    capital: TimedValue
    target_risk: TimedValue
    current_held_price: TimedValue
    annual_risk_estimate: TimedValue
    multiplier: float
    fx_rate: TimedValue
    risk_estimate_prevalidated: bool
    instrument_weight: TimedValue | None = None
    idm: TimedValue | None = None
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST


@dataclass(frozen=True)
class SizingResult:
    unrounded_contracts: float
    rounded_contracts: int


def size_contracts(sizing: SizingInput) -> SizingResult:
    require_source_native(sizing.lane_class)
    sizing.completed_bar.validate()
    _validate_timestamps(sizing)
    require_finite_positive("capital", sizing.capital.value)
    require_finite_positive("target_risk", sizing.target_risk.value)
    require_finite_positive("current_held_price", sizing.current_held_price.value)
    require_finite_positive("annual_risk_estimate", sizing.annual_risk_estimate.value)
    require_finite_positive("multiplier", sizing.multiplier)
    require_finite_positive("fx_rate", sizing.fx_rate.value)

    if not sizing.risk_estimate_prevalidated:
        raise CarverBlocked("risk estimate is not pre-validated")

    weight = _context_value("instrument_weight", sizing.instrument_weight, default=1.0)
    idm = _context_value("idm", sizing.idm, default=1.0)

    contract_risk = (
        sizing.current_held_price.value
        * sizing.multiplier
        * sizing.fx_rate.value
        * sizing.annual_risk_estimate.value
    )
    require_finite_positive("contract_risk", contract_risk)

    target_currency_risk = sizing.capital.value * sizing.target_risk.value
    unrounded = target_currency_risk * weight * idm / contract_risk
    return SizingResult(
        unrounded_contracts=unrounded,
        rounded_contracts=_round_contracts(unrounded, sizing.rounding_policy),
    )


def _validate_timestamps(sizing: SizingInput) -> None:
    expected = sizing.completed_bar.timestamp
    inputs = {
        "capital": sizing.capital,
        "target_risk": sizing.target_risk,
        "current_held_price": sizing.current_held_price,
        "annual_risk_estimate": sizing.annual_risk_estimate,
        "fx_rate": sizing.fx_rate,
        "instrument_weight": sizing.instrument_weight,
        "idm": sizing.idm,
    }
    for name, timed in inputs.items():
        if timed is not None and timed.as_of != expected:
            raise CarverBlocked(f"{name} timestamp is not aligned to completed bar")


def _context_value(name: str, timed: TimedValue | None, default: float) -> float:
    if timed is None:
        return default
    require_finite_positive(name, timed.value)
    return timed.value


def _round_contracts(value: float, policy: RoundingPolicy) -> int:
    if policy is RoundingPolicy.NEAREST:
        return int(round(value))
    if policy is RoundingPolicy.FLOOR:
        return floor(value)
    if policy is RoundingPolicy.CEILING:
        return ceil(value)
    if policy is RoundingPolicy.TRUNCATE:
        return int(value)
    raise CarverBlocked("rounding policy is unresolved")

```

# FILE: src\carver\spine\m3.py

```text
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isclose

from .m0 import CompletedBar, ContractSpec, LaneClass, CarverBlocked, require_finite_positive, require_source_native
from .m1 import RoundingPolicy, SizingInput, SizingResult, TimedValue, size_contracts


@dataclass(frozen=True)
class PortfolioLeg:
    contract: ContractSpec
    weight: float

    @property
    def code(self) -> str:
        return self.contract.code

    @property
    def name(self) -> str:
        return self.contract.name

    @property
    def multiplier(self) -> float:
        return self.contract.multiplier

    @property
    def currency(self) -> str:
        return self.contract.currency


@dataclass(frozen=True)
class PortfolioSpec:
    portfolio_id: str
    lane_class: LaneClass
    legs: tuple[PortfolioLeg, ...]
    capital: float
    target_risk: float
    idm: float

    def validate(self) -> None:
        require_source_native(self.lane_class)
        if not self.legs:
            raise CarverBlocked("portfolio requires at least one leg")
        require_finite_positive("portfolio capital", self.capital)
        require_finite_positive("portfolio target risk", self.target_risk)
        require_finite_positive("portfolio IDM", self.idm)
        if not isclose(sum(leg.weight for leg in self.legs), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise CarverBlocked("portfolio weights must sum to 1")
        seen_codes: set[str] = set()
        for leg in self.legs:
            leg.contract.validate()
            require_finite_positive("portfolio leg weight", leg.weight)
            if leg.code in seen_codes:
                raise CarverBlocked(f"duplicate portfolio leg {leg.code}")
            seen_codes.add(leg.code)

    def size_legs(
        self,
        completed_bar: CompletedBar,
        market_inputs: dict[str, "LegMarketInput"],
        rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST,
    ) -> dict[str, SizingResult]:
        self.validate()
        completed_bar.validate()
        expected_codes = {leg.code for leg in self.legs}
        provided_codes = set(market_inputs)
        if provided_codes != expected_codes:
            raise CarverBlocked("synthetic market inputs must exactly match portfolio legs")
        results: dict[str, SizingResult] = {}
        as_of = completed_bar.timestamp
        for leg in self.legs:
            market = market_inputs.get(leg.code)
            if market is None:
                raise CarverBlocked(f"missing synthetic market input for {leg.code}")
            sizing = SizingInput(
                lane_class=self.lane_class,
                completed_bar=completed_bar,
                capital=TimedValue(self.capital, as_of),
                target_risk=TimedValue(self.target_risk, as_of),
                current_held_price=market.current_held_price,
                annual_risk_estimate=market.annual_risk_estimate,
                multiplier=leg.multiplier,
                fx_rate=market.fx_rate,
                risk_estimate_prevalidated=market.risk_estimate_prevalidated,
                instrument_weight=TimedValue(leg.weight, as_of),
                idm=TimedValue(self.idm, as_of),
                rounding_policy=rounding_policy,
            )
            results[leg.code] = size_contracts(sizing)
        return results


@dataclass(frozen=True)
class LegMarketInput:
    current_held_price: TimedValue
    annual_risk_estimate: TimedValue
    fx_rate: TimedValue
    risk_estimate_prevalidated: bool = True


def p01_risk_parity(capital: float, target_risk: float, idm: float) -> PortfolioSpec:
    return PortfolioSpec(
        portfolio_id="P01_RISK_PARITY_EXAMPLE",
        lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
        capital=capital,
        target_risk=target_risk,
        idm=idm,
        legs=(
            PortfolioLeg(mes_contract(), 0.50),
            PortfolioLeg(zn_contract(), 0.50),
        ),
    )


def p02_all_weather(capital: float, target_risk: float, idm: float) -> PortfolioSpec:
    return PortfolioSpec(
        portfolio_id="P02_ALL_WEATHER_EXAMPLE",
        lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
        capital=capital,
        target_risk=target_risk,
        idm=idm,
        legs=(
            PortfolioLeg(mes_contract(), 0.25),
            PortfolioLeg(zn_contract(), 0.125),
            PortfolioLeg(zf_contract(), 0.125),
            PortfolioLeg(qm_contract(), 0.125),
            PortfolioLeg(zc_contract(), 0.125),
            PortfolioLeg(mgc_contract(), 0.25),
        ),
    )


def synthetic_market_inputs(timestamp: datetime, values: dict[str, tuple[float, float, float]]) -> dict[str, LegMarketInput]:
    return {
        code: LegMarketInput(
            current_held_price=TimedValue(price, timestamp),
            annual_risk_estimate=TimedValue(risk, timestamp),
            fx_rate=TimedValue(fx, timestamp),
        )
        for code, (price, risk, fx) in values.items()
    }


def mes_contract() -> ContractSpec:
    return ContractSpec("MES", "S&P 500 micro future", "CME", "USD", 5)


def zn_contract() -> ContractSpec:
    return ContractSpec("ZN", "US 10-year bond future", "CBOT", "USD", 1000)


def zf_contract() -> ContractSpec:
    return ContractSpec("ZF", "US 5-year bond future", "CBOT", "USD", 1000)


def qm_contract() -> ContractSpec:
    return ContractSpec("QM", "WTI Crude Oil mini future", "NYMEX", "USD", 500)


def zc_contract() -> ContractSpec:
    return ContractSpec("ZC", "Corn future", "CBOT", "USD", 5000)


def mgc_contract() -> ContractSpec:
    return ContractSpec("MGC", "Gold micro future", "COMEX", "USD", 10)

```

# FILE: src\carver\spine\first_spine.py

```text
from __future__ import annotations

from .m0 import CompletedBar, LaneClass, CarverBlocked, require_source_native
from .m1 import RoundingPolicy, SizingInput, SizingResult, size_contracts
from .m3 import LegMarketInput, PortfolioSpec, p01_risk_parity, p02_all_weather


def s01_buy_and_hold_single_contract(lane_class: LaneClass, completed_bar: CompletedBar) -> int:
    require_source_native(lane_class)
    completed_bar.validate()
    return 1


def s02_buy_and_hold_with_risk_scaling(sizing: SizingInput) -> SizingResult:
    return size_contracts(sizing)


def s03_buy_and_hold_with_variable_risk_scaling(sizing: SizingInput) -> SizingResult:
    if not sizing.risk_estimate_prevalidated:
        raise CarverBlocked("S03 requires pre-validated variable risk")
    return size_contracts(sizing)


def s04_portfolio_with_variable_risk_position_sizing(
    portfolio: PortfolioSpec,
    completed_bar: CompletedBar,
    market_inputs: dict[str, LegMarketInput],
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST,
) -> dict[str, SizingResult]:
    return portfolio.size_legs(completed_bar, market_inputs, rounding_policy)


def p01_synthetic_conformance(
    portfolio: PortfolioSpec,
    completed_bar: CompletedBar,
    market_inputs: dict[str, LegMarketInput],
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST,
) -> dict[str, SizingResult]:
    _require_same_portfolio(portfolio, p01_risk_parity(portfolio.capital, portfolio.target_risk, portfolio.idm))
    return s04_portfolio_with_variable_risk_position_sizing(portfolio, completed_bar, market_inputs, rounding_policy)


def p02_synthetic_conformance(
    portfolio: PortfolioSpec,
    completed_bar: CompletedBar,
    market_inputs: dict[str, LegMarketInput],
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST,
) -> dict[str, SizingResult]:
    _require_same_portfolio(portfolio, p02_all_weather(portfolio.capital, portfolio.target_risk, portfolio.idm))
    return s04_portfolio_with_variable_risk_position_sizing(portfolio, completed_bar, market_inputs, rounding_policy)


def _require_same_portfolio(actual: PortfolioSpec, expected: PortfolioSpec) -> None:
    actual.validate()
    if actual.portfolio_id != expected.portfolio_id or len(actual.legs) != len(expected.legs):
        raise CarverBlocked(f"{expected.portfolio_id} conformance requires the exact source portfolio spec")
    for actual_leg, expected_leg in zip(actual.legs, expected.legs, strict=True):
        if (
            actual_leg.code != expected_leg.code
            or actual_leg.name != expected_leg.name
            or actual_leg.contract.exchange != expected_leg.contract.exchange
            or actual_leg.currency != expected_leg.currency
            or actual_leg.weight != expected_leg.weight
            or actual_leg.multiplier != expected_leg.multiplier
        ):
            raise CarverBlocked(f"{expected.portfolio_id} conformance requires exact legs, weights, and multipliers")

```

# FILE: src\carver\spine\s03.py

```text
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from numbers import Integral

from .m0 import CompletedBar, CarverBlocked, require_finite_positive
from .m1 import TimedValue


@dataclass(frozen=True)
class SyntheticDailyPrice:
    completed_bar: CompletedBar
    price: float

    def validate(self) -> None:
        self.completed_bar.validate()
        require_finite_positive("synthetic daily price", self.price)


@dataclass(frozen=True)
class S03RiskConfig:
    ewma_span: int = 32
    annualization_days: int = 256
    long_run_weight: float = 0.30
    short_run_weight: float = 0.70

    @property
    def ewma_alpha(self) -> float:
        return 2.0 / (self.ewma_span + 1.0)

    def validate(self) -> None:
        if isinstance(self.ewma_span, bool) or not isinstance(self.ewma_span, Integral):
            raise CarverBlocked("S03 EWMA span must be an integer")
        if self.ewma_span < 2:
            raise CarverBlocked("S03 EWMA span must be at least 2")
        if isinstance(self.annualization_days, bool) or not isinstance(self.annualization_days, Integral):
            raise CarverBlocked("S03 annualization days must be an integer")
        if self.annualization_days <= 0:
            raise CarverBlocked("S03 annualization days must be positive")
        require_finite_positive("S03 long-run blend weight", self.long_run_weight)
        require_finite_positive("S03 short-run blend weight", self.short_run_weight)
        if abs((self.long_run_weight + self.short_run_weight) - 1.0) > 1e-12:
            raise CarverBlocked("S03 blend weights must sum to 1")


@dataclass(frozen=True)
class S03RiskEstimate:
    as_of: TimedValue
    short_run_annual_risk: float
    long_run_annual_risk: float
    observation_count: int


def estimate_s03_annual_risk(
    prices: tuple[SyntheticDailyPrice, ...],
    long_run_annual_risk: TimedValue,
    config: S03RiskConfig = S03RiskConfig(),
) -> S03RiskEstimate:
    config.validate()
    require_finite_positive("S03 long-run annual risk", long_run_annual_risk.value)
    if len(prices) < 2:
        raise CarverBlocked("S03 synthetic risk estimate requires at least two completed prices")

    previous_timestamp = None
    for price in prices:
        price.validate()
        timestamp = price.completed_bar.timestamp
        if previous_timestamp is not None and timestamp <= previous_timestamp:
            raise CarverBlocked("S03 synthetic prices must be strictly increasing completed bars")
        previous_timestamp = timestamp

    as_of = prices[-1].completed_bar.timestamp
    if long_run_annual_risk.as_of != as_of:
        raise CarverBlocked("S03 long-run annual risk timestamp must align to final completed bar")

    returns = tuple(
        (current.price / previous.price) - 1.0
        for previous, current in zip(prices[:-1], prices[1:], strict=True)
    )
    ewma_variance = returns[0] * returns[0]
    alpha = config.ewma_alpha
    for daily_return in returns[1:]:
        ewma_variance = alpha * daily_return * daily_return + (1.0 - alpha) * ewma_variance

    short_run_annual_risk = sqrt(ewma_variance * config.annualization_days)
    blended = (
        config.long_run_weight * long_run_annual_risk.value
        + config.short_run_weight * short_run_annual_risk
    )
    return S03RiskEstimate(
        as_of=TimedValue(blended, as_of),
        short_run_annual_risk=short_run_annual_risk,
        long_run_annual_risk=long_run_annual_risk.value,
        observation_count=len(prices),
    )

```

# FILE: src\carver\spine\minute_export.py

```text
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from io import StringIO
from math import isfinite
from numbers import Real
from pathlib import Path

from .m0 import ContractSpec, CarverBlocked, require_finite_positive


EXPECTED_MINUTE_EXPORT_HEADER = (
    "instrument",
    "contract_month",
    "bar_type",
    "timeframe",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
)

DEFAULT_MINUTE_EXPORT_QUARANTINE = Path("data/quarantine/ninjatrader/minute_exports")


@dataclass(frozen=True)
class MinuteExportSpec:
    contract: ContractSpec
    contract_month: str
    bar_type: str = "Last"
    timeframe: str = "1 Minute"
    session_start: time = time(13, 30)
    session_end: time = time(20, 0)
    timezone_offset_seconds: int = 0
    allowed_contract_months: tuple[str, ...] = ("03", "06", "09", "12")

    def validate(self) -> None:
        self.contract.validate()
        _require_contract_month(self.contract_month, self.allowed_contract_months)
        if self.bar_type != "Last":
            raise CarverBlocked("minute export bar_type must be Last")
        if self.timeframe != "1 Minute":
            raise CarverBlocked("minute export timeframe must be 1 Minute")
        if self.session_start >= self.session_end:
            raise CarverBlocked("minute export session window is invalid")
        _require_offset_seconds(self.timezone_offset_seconds)
        for month in self.allowed_contract_months:
            if not isinstance(month, str) or len(month) != 2 or not month.isdigit():
                raise CarverBlocked("allowed contract months must use MM strings")


@dataclass(frozen=True)
class MinuteBar:
    instrument: str
    contract_month: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def validate(self, spec: MinuteExportSpec) -> None:
        spec.validate()
        if self.instrument != spec.contract.code:
            raise CarverBlocked("minute bar instrument does not match expected contract")
        if self.contract_month != spec.contract_month:
            raise CarverBlocked("minute bar contract month does not match expected contract month")
        _validate_completed_minute(self.timestamp, spec)
        require_finite_positive("minute open", self.open)
        require_finite_positive("minute high", self.high)
        require_finite_positive("minute low", self.low)
        require_finite_positive("minute close", self.close)
        _require_finite_non_negative("minute volume", self.volume)
        if self.high < max(self.open, self.low, self.close):
            raise CarverBlocked("minute high is inconsistent with OHLC")
        if self.low > min(self.open, self.high, self.close):
            raise CarverBlocked("minute low is inconsistent with OHLC")


def parse_minute_export_text(text: str, spec: MinuteExportSpec) -> tuple[MinuteBar, ...]:
    spec.validate()
    if not isinstance(text, str) or not text.strip():
        raise CarverBlocked("minute export text is empty")

    reader = csv.DictReader(StringIO(text), strict=True)
    if tuple(reader.fieldnames or ()) != EXPECTED_MINUTE_EXPORT_HEADER:
        raise CarverBlocked("minute export header does not match expected schema")

    bars: list[MinuteBar] = []
    previous_timestamp: datetime | None = None
    seen_timestamps: set[datetime] = set()
    for row in reader:
        if set(row) != set(EXPECTED_MINUTE_EXPORT_HEADER):
            raise CarverBlocked("minute export row does not match expected schema")
        if row["bar_type"] != spec.bar_type:
            raise CarverBlocked("minute export row has wrong bar_type")
        if row["timeframe"] != spec.timeframe:
            raise CarverBlocked("minute export row has wrong timeframe")
        if any(value is None for value in row.values()):
            raise CarverBlocked("minute export row has extra fields")
        if any(row[column] is None or row[column] == "" for column in EXPECTED_MINUTE_EXPORT_HEADER):
            raise CarverBlocked("minute export row has missing fields")
        bar = MinuteBar(
            instrument=row["instrument"],
            contract_month=row["contract_month"],
            timestamp=_parse_timestamp(row["timestamp"]),
            open=_parse_float("open", row["open"]),
            high=_parse_float("high", row["high"]),
            low=_parse_float("low", row["low"]),
            close=_parse_float("close", row["close"]),
            volume=_parse_float("volume", row["volume"]),
        )
        bar.validate(spec)
        if bar.timestamp in seen_timestamps:
            raise CarverBlocked("minute export contains duplicate timestamp")
        if previous_timestamp is not None:
            if bar.timestamp <= previous_timestamp:
                raise CarverBlocked("minute export rows must be strictly increasing")
            if bar.timestamp - previous_timestamp != timedelta(minutes=1):
                raise CarverBlocked("minute export rows must be contiguous one-minute bars")
        seen_timestamps.add(bar.timestamp)
        previous_timestamp = bar.timestamp
        bars.append(bar)

    if not bars:
        raise CarverBlocked("minute export contains no rows")
    return tuple(bars)


def parse_minute_export_file(
    file_path: Path | str,
    spec: MinuteExportSpec,
    quarantine_root: Path | str = DEFAULT_MINUTE_EXPORT_QUARANTINE,
) -> tuple[MinuteBar, ...]:
    try:
        root = Path(quarantine_root).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("minute export quarantine root does not exist") from exc
    try:
        path = Path(file_path).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("minute export file does not exist") from exc
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CarverBlocked("minute export file must be inside the quarantine root") from exc
    if not path.is_file():
        raise CarverBlocked("minute export path must be a file")
    if path.suffix.lower() not in {".csv", ".txt"}:
        raise CarverBlocked("minute export file must be CSV/text, not platform cache")
    return parse_minute_export_text(path.read_text(encoding="utf-8-sig"), spec)


def _parse_timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked("minute timestamp is missing")
    try:
        timestamp = datetime.fromisoformat(value)
    except ValueError as exc:
        raise CarverBlocked("minute timestamp must be ISO-8601") from exc
    _validate_completed_minute(timestamp)
    return timestamp


def _validate_completed_minute(timestamp: datetime, spec: MinuteExportSpec | None = None) -> None:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise CarverBlocked("minute timestamp must be timezone-aware")
    if timestamp.second or timestamp.microsecond:
        raise CarverBlocked("minute timestamp must be minute-aligned")
    if spec is not None:
        if int(timestamp.utcoffset().total_seconds()) != spec.timezone_offset_seconds:
            raise CarverBlocked("minute timestamp timezone offset does not match export spec")
        minute_time = timestamp.timetz().replace(tzinfo=None)
        if minute_time < spec.session_start or minute_time >= spec.session_end:
            raise CarverBlocked("minute timestamp is outside locked session window")


def _parse_float(name: str, value: str) -> float:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked(f"{name} is missing")
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be numeric") from exc
    if not isfinite(parsed):
        raise CarverBlocked(f"{name} must be finite")
    return parsed


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be non-negative")


def _require_contract_month(value: str, allowed_months: tuple[str, ...]) -> None:
    if not isinstance(value, str) or len(value) != 5 or value[2] != "-":
        raise CarverBlocked("contract month must use MM-YY")
    month, year = value.split("-")
    if not (month.isdigit() and year.isdigit()):
        raise CarverBlocked("contract month must use MM-YY")
    month_number = int(month)
    if month_number < 1 or month_number > 12:
        raise CarverBlocked("contract month has invalid month")
    if month not in allowed_months:
        raise CarverBlocked("contract month is not allowed for this source-native contract")


def _require_offset_seconds(value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CarverBlocked("timezone offset must be integer seconds")

```

# FILE: src\carver\spine\web_chart_api.py

```text
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
import json
from math import isfinite
from numbers import Real
from pathlib import Path
from typing import Any

from .m0 import ContractSpec, LaneClass, CarverBlocked, require_finite_positive, require_source_native


ALLOWED_CHART_ENDPOINTS = frozenset({"md/getChart", "md/cancelChart"})
MAX_SYNTHETIC_CHART_ELEMENTS = 500
DEFAULT_WEB_CHART_QUARANTINE = Path("data/quarantine/ninjatrader/web_chart")
LOCKED_WEB_CHART_PROVIDER_SYMBOLS = {
    ("ES", "06-26", "ES JUN26"): "3570919",
    ("ZN", "06-26", "ZN JUN26"): "4470301",
}


class ChartBarType(StrEnum):
    MINUTE = "MinuteBar"
    DAILY = "DailyBar"


@dataclass(frozen=True)
class LockedWebChartSymbol:
    contract: ContractSpec
    contract_month: str
    provider_symbol_id: str
    display_symbol: str
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    def validate(self) -> None:
        require_source_native(self.lane_class)
        self.contract.validate()
        if not isinstance(self.provider_symbol_id, str) or not self.provider_symbol_id.isdigit():
            raise CarverBlocked("web chart provider symbol id must be a numeric string")
        expected_display = f"{self.contract.code} {_display_contract_month(self.contract_month)}"
        if self.display_symbol != expected_display:
            raise CarverBlocked("web chart display symbol does not match source-native contract month")
        _require_contract_month(self.contract_month)
        locked_id = LOCKED_WEB_CHART_PROVIDER_SYMBOLS.get((self.contract.code, self.contract_month, self.display_symbol))
        if locked_id is None or self.provider_symbol_id != locked_id:
            raise CarverBlocked("web chart symbol is not in the locked provider mapping")


@dataclass(frozen=True)
class WebChartSymbol:
    locked: LockedWebChartSymbol
    provider_symbol_id: str
    display_symbol: str
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    @property
    def contract(self) -> ContractSpec:
        return self.locked.contract

    @property
    def contract_month(self) -> str:
        return self.locked.contract_month

    def validate(self) -> None:
        require_source_native(self.lane_class)
        self.locked.validate()
        if self.provider_symbol_id != self.locked.provider_symbol_id:
            raise CarverBlocked("web chart provider symbol id does not match locked mapping")
        if self.display_symbol != self.locked.display_symbol:
            raise CarverBlocked("web chart display symbol does not match locked mapping")


@dataclass(frozen=True)
class WebChartRequest:
    symbol: WebChartSymbol
    bar_type: ChartBarType
    element_size: int
    element_count: int
    endpoint: str = "md/getChart"
    element_size_unit: str = "UnderlyingUnits"
    with_histogram: bool = False

    def validate(self) -> None:
        if self.endpoint not in ALLOWED_CHART_ENDPOINTS:
            raise CarverBlocked("web chart endpoint is not allow-listed")
        if self.endpoint != "md/getChart":
            raise CarverBlocked("only md/getChart request normalization is authorized")
        if not isinstance(self.bar_type, ChartBarType):
            raise CarverBlocked("web chart bar type must be a locked ChartBarType")
        self.symbol.validate()
        if self.element_size_unit != "UnderlyingUnits":
            raise CarverBlocked("web chart element size unit must be UnderlyingUnits")
        if self.with_histogram:
            raise CarverBlocked("web chart histogram requests are not authorized")
        _require_positive_int("web chart element size", self.element_size)
        _require_positive_int("web chart element count", self.element_count)
        if self.element_count > MAX_SYNTHETIC_CHART_ELEMENTS:
            raise CarverBlocked("web chart element count exceeds synthetic gate maximum")
        if self.bar_type is ChartBarType.DAILY and self.element_size != 1:
            raise CarverBlocked("daily web chart requests must use element size 1")

    def payload(self) -> dict[str, Any]:
        self.validate()
        return {
            "symbol": self.symbol.locked.provider_symbol_id,
            "chartDescription": {
                "underlyingType": self.bar_type.value,
                "elementSizeUnit": self.element_size_unit,
                "elementSize": self.element_size,
                "withHistogram": self.with_histogram,
            },
            "timeRange": {"asMuchAsElements": self.element_count},
        }


@dataclass(frozen=True)
class WebChartBar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    complete: bool
    request_fingerprint: str

    def validate(self, request: WebChartRequest) -> None:
        request.validate()
        if self.request_fingerprint != web_chart_request_fingerprint(request):
            raise CarverBlocked("web chart bar request binding does not match locked request")
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise CarverBlocked("web chart bar timestamp must be timezone-aware")
        if request.bar_type is ChartBarType.MINUTE and (self.timestamp.second or self.timestamp.microsecond):
            raise CarverBlocked("minute web chart timestamp must be minute-aligned")
        if request.bar_type is ChartBarType.DAILY and (
            self.timestamp.hour or self.timestamp.minute or self.timestamp.second or self.timestamp.microsecond
        ):
            raise CarverBlocked("daily web chart timestamp must be date-aligned")
        require_finite_positive("web chart open", self.open)
        require_finite_positive("web chart high", self.high)
        require_finite_positive("web chart low", self.low)
        require_finite_positive("web chart close", self.close)
        _require_finite_non_negative("web chart volume", self.volume)
        if self.high < max(self.open, self.low, self.close):
            raise CarverBlocked("web chart high is inconsistent with OHLC")
        if self.low > min(self.open, self.high, self.close):
            raise CarverBlocked("web chart low is inconsistent with OHLC")
        if not self.complete:
            raise CarverBlocked("web chart bar is not complete")


@dataclass(frozen=True)
class BoundWebChartResponse:
    request: WebChartRequest
    bars: tuple[WebChartBar, ...]

    def validate(self) -> None:
        self.request.validate()
        if not self.bars:
            raise CarverBlocked("bound web chart response contains no bars")
        previous_timestamp: datetime | None = None
        seen_timestamps: set[datetime] = set()
        for bar in self.bars:
            bar.validate(self.request)
            if bar.timestamp in seen_timestamps:
                raise CarverBlocked("bound web chart response contains duplicate timestamp")
            if previous_timestamp is not None and bar.timestamp <= previous_timestamp:
                raise CarverBlocked("bound web chart response bars must be strictly increasing")
            seen_timestamps.add(bar.timestamp)
            previous_timestamp = bar.timestamp


@dataclass(frozen=True)
class WebChartProbePlan:
    request: WebChartRequest
    execution_authorized: bool = False

    def require_authorized(self) -> None:
        self.request.validate()
        if not self.execution_authorized:
            raise CarverBlocked("real web chart probe execution is not authorized")


def normalize_web_chart_response(payload: dict[str, Any], request: WebChartRequest) -> tuple[WebChartBar, ...]:
    return normalize_bound_web_chart_response(payload, request).bars


def normalize_bound_web_chart_response(payload: dict[str, Any], request: WebChartRequest) -> BoundWebChartResponse:
    request.validate()
    if not isinstance(payload, dict):
        raise CarverBlocked("web chart response must be an object")
    _require_response_request_binding(payload, request)
    if not payload.get("ok", False):
        raise CarverBlocked("web chart response is not ok")
    body = payload.get("body")
    if not isinstance(body, dict):
        raise CarverBlocked("web chart response body is missing")
    raw_bars = body.get("items")
    if not isinstance(raw_bars, list):
        raise CarverBlocked("web chart response body items are missing")
    if len(raw_bars) > request.element_count:
        raise CarverBlocked("web chart response contains more bars than requested")
    if not raw_bars:
        raise CarverBlocked("web chart response contains no bars")

    bars: list[WebChartBar] = []
    previous_timestamp: datetime | None = None
    seen_timestamps: set[datetime] = set()
    for raw in raw_bars:
        bar = _normalize_raw_bar(raw, request)
        bar.validate(request)
        if bar.timestamp in seen_timestamps:
            raise CarverBlocked("web chart response contains duplicate timestamp")
        if previous_timestamp is not None and bar.timestamp <= previous_timestamp:
            raise CarverBlocked("web chart response bars must be strictly increasing")
        seen_timestamps.add(bar.timestamp)
        previous_timestamp = bar.timestamp
        bars.append(bar)
    bound = BoundWebChartResponse(request, tuple(bars))
    bound.validate()
    return bound


def web_chart_response_request_binding(request: WebChartRequest) -> dict[str, Any]:
    request_payload = request.payload()
    return {
        "endpoint": request.endpoint,
        "payload": request_payload,
        "identity": {
            "contractCode": request.symbol.contract.code,
            "contractMonth": request.symbol.contract_month,
            "displaySymbol": request.symbol.display_symbol,
            "providerSymbolId": request.symbol.provider_symbol_id,
        },
    }


def web_chart_request_fingerprint(request: WebChartRequest) -> str:
    return json.dumps(web_chart_response_request_binding(request), sort_keys=True, separators=(",", ":"))


def normalize_web_chart_response_file(
    file_path: Path | str,
    request: WebChartRequest,
    quarantine_root: Path | str = DEFAULT_WEB_CHART_QUARANTINE,
) -> tuple[WebChartBar, ...]:
    return normalize_bound_web_chart_response_file(file_path, request, quarantine_root).bars


def normalize_bound_web_chart_response_file(
    file_path: Path | str,
    request: WebChartRequest,
    quarantine_root: Path | str = DEFAULT_WEB_CHART_QUARANTINE,
) -> BoundWebChartResponse:
    try:
        root = Path(quarantine_root).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("web chart quarantine root does not exist") from exc
    try:
        path = Path(file_path).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("web chart response file does not exist") from exc
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CarverBlocked("web chart response file must be inside the quarantine root") from exc
    if not path.is_file():
        raise CarverBlocked("web chart response path must be a file")
    if path.suffix.lower() != ".json":
        raise CarverBlocked("web chart response file must be JSON")
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise CarverBlocked("web chart response file must contain JSON") from exc
    return normalize_bound_web_chart_response(payload, request)


def assert_safe_web_chart_endpoint(endpoint: str) -> None:
    if endpoint not in ALLOWED_CHART_ENDPOINTS:
        raise CarverBlocked("endpoint is not an allowed read-only chart endpoint")


def _require_response_request_binding(payload: dict[str, Any], request: WebChartRequest) -> None:
    binding = payload.get("request")
    if not isinstance(binding, dict):
        raise CarverBlocked("web chart response request binding is missing")
    if binding != web_chart_response_request_binding(request):
        raise CarverBlocked("web chart response request binding does not match locked request")


def _normalize_raw_bar(raw: Any, request: WebChartRequest) -> WebChartBar:
    if not isinstance(raw, dict):
        raise CarverBlocked("web chart bar must be an object")
    request.validate()
    timestamp = _parse_timestamp(raw.get("timestamp"))
    open_price = _parse_float("open", raw.get("open"))
    high = _parse_float("high", raw.get("high"))
    low = _parse_float("low", raw.get("low"))
    close = _parse_float("close", raw.get("close"))
    volume = _parse_volume(raw)
    if "complete" not in raw:
        raise CarverBlocked("web chart bar complete flag is missing")
    complete = raw["complete"]
    if not isinstance(complete, bool):
        raise CarverBlocked("web chart bar complete flag must be boolean")
    return WebChartBar(
        timestamp,
        open_price,
        high,
        low,
        close,
        volume,
        complete,
        web_chart_request_fingerprint(request),
    )


def _parse_volume(raw: dict[str, Any]) -> float:
    if "volume" in raw:
        return _parse_float("volume", raw["volume"])
    if "upVolume" not in raw or "downVolume" not in raw:
        raise CarverBlocked("web chart bar volume evidence is missing")
    up = raw["upVolume"]
    down = raw["downVolume"]
    return _parse_float("upVolume", up) + _parse_float("downVolume", down)


def _parse_timestamp(value: Any) -> datetime:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(float(value)):
        raise CarverBlocked("web chart timestamp must be finite epoch milliseconds")
    return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc)


def _parse_float(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")
    return float(value)


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be non-negative")


def _require_positive_int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CarverBlocked(f"{name} must be a positive integer")


def _require_contract_month(value: str) -> None:
    if not isinstance(value, str) or len(value) != 5 or value[2] != "-":
        raise CarverBlocked("web chart contract month must use MM-YY")
    month, year = value.split("-")
    if not (month.isdigit() and year.isdigit()):
        raise CarverBlocked("web chart contract month must use MM-YY")
    month_number = int(month)
    if month_number < 1 or month_number > 12:
        raise CarverBlocked("web chart contract month has invalid month")


def _display_contract_month(value: str) -> str:
    month, year = value.split("-")
    month_names = {
        "01": "JAN",
        "02": "FEB",
        "03": "MAR",
        "04": "APR",
        "05": "MAY",
        "06": "JUN",
        "07": "JUL",
        "08": "AUG",
        "09": "SEP",
        "10": "OCT",
        "11": "NOV",
        "12": "DEC",
    }
    if month not in month_names:
        raise CarverBlocked("web chart contract month has invalid display month")
    return f"{month_names[month]}{year}"

```

# FILE: src\carver\spine\daily_bars.py

```text
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from math import isfinite
from numbers import Real

from .m0 import CompletedBar, ContractSpec, CarverBlocked, require_finite_positive
from .minute_export import MinuteBar, MinuteExportSpec
from .web_chart_api import BoundWebChartResponse, ChartBarType, WebChartBar, WebChartRequest


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
    raise CarverBlocked("loose web chart bars are not authorized for daily derivation; use a bound web chart response")


def derive_completed_daily_from_bound_web_chart(
    response: BoundWebChartResponse,
    session: DailyDerivationSession,
) -> CompletedDailyMarketBar:
    response.validate()
    request = response.request
    request.validate()
    session.validate()
    if request.bar_type is not ChartBarType.MINUTE or request.element_size != 1:
        raise CarverBlocked("daily derivation requires one-minute web chart bars")
    for bar in response.bars:
        bar.validate(request)
    return _derive_completed_daily(
        contract=request.symbol.contract,
        contract_month=request.symbol.contract_month,
        session=session,
        rows=tuple(
            _MinuteLike(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)
            for bar in response.bars
        ),
    )


def normalize_direct_daily_web_chart_bar(
    bar: WebChartBar,
    request: WebChartRequest,
) -> CompletedDailyMarketBar:
    raise CarverBlocked("loose web chart bars are not authorized for direct daily normalization; use a bound web chart response")


def normalize_direct_daily_bound_web_chart(
    response: BoundWebChartResponse,
) -> CompletedDailyMarketBar:
    response.validate()
    if len(response.bars) != 1:
        raise CarverBlocked("direct daily normalization requires exactly one bound daily bar")
    request = response.request
    bar = response.bars[0]
    request.validate()
    if request.bar_type is not ChartBarType.DAILY or request.element_size != 1:
        raise CarverBlocked("direct daily normalization requires one-day web chart bars")
    bar.validate(request)
    daily = CompletedDailyMarketBar(
        completed_bar=CompletedBar(bar.timestamp),
        contract=request.symbol.contract,
        contract_month=request.symbol.contract_month,
        open=bar.open,
        high=bar.high,
        low=bar.low,
        close=bar.close,
        volume=bar.volume,
    )
    daily.validate()
    return daily


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

```

# FILE: src\carver\spine\continuous.py

```text
from __future__ import annotations

from dataclasses import dataclass

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


def build_continuous_back_adjusted_series(request: ContinuousSeriesRequest) -> tuple[CompletedDailyMarketBar, ...]:
    request.validate()
    raise CarverBlocked("continuous roll/back-adjustment implementation requires a separately locked source rule artifact")

```

# FILE: src\carver\spine\portfolio_conformance.py

```text
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .daily_bars import CompletedDailyMarketBar
from .first_spine import p01_synthetic_conformance, p02_synthetic_conformance
from .m0 import CarverBlocked, ContractSpec
from .m1 import RoundingPolicy, SizingResult, TimedValue
from .m3 import LegMarketInput, PortfolioSpec
from .web_chart_api import LOCKED_WEB_CHART_PROVIDER_SYMBOLS


class ProviderMappingStatus(StrEnum):
    LOCKED = "LOCKED"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class PortfolioProviderMappingRow:
    contract_code: str
    contract_month: str
    display_symbol: str
    status: ProviderMappingStatus
    provider_symbol_id: str | None = None


@dataclass(frozen=True)
class LockedPortfolioProviderMapping:
    contract: ContractSpec
    contract_month: str
    display_symbol: str
    provider_symbol_id: str

    @property
    def code(self) -> str:
        return self.contract.code

    def validate(self) -> None:
        self.contract.validate()
        if self.display_symbol != _display_symbol(self.contract.code, self.contract_month):
            raise CarverBlocked("provider mapping display symbol does not match contract month")
        if not isinstance(self.provider_symbol_id, str) or not self.provider_symbol_id.isdigit():
            raise CarverBlocked("provider mapping id must be a numeric string")
        locked_id = LOCKED_WEB_CHART_PROVIDER_SYMBOLS.get((self.contract.code, self.contract_month, self.display_symbol))
        if locked_id != self.provider_symbol_id:
            raise CarverBlocked("provider mapping is not locked in the observed mapping registry")


@dataclass(frozen=True)
class PortfolioProviderMappingSet:
    portfolio: PortfolioSpec
    mappings: tuple[LockedPortfolioProviderMapping, ...]

    def validate(self) -> None:
        self.portfolio.validate()
        expected_codes = {leg.code for leg in self.portfolio.legs}
        provided_codes = {mapping.code for mapping in self.mappings}
        if provided_codes != expected_codes:
            raise CarverBlocked("locked provider mappings must exactly match portfolio legs")
        leg_by_code = {leg.code: leg for leg in self.portfolio.legs}
        seen_ids: set[str] = set()
        for mapping in self.mappings:
            mapping.validate()
            leg = leg_by_code[mapping.code]
            if mapping.contract != leg.contract:
                raise CarverBlocked("provider mapping contract does not match portfolio leg")
            if mapping.provider_symbol_id in seen_ids:
                raise CarverBlocked("provider mapping ids must be unique")
            seen_ids.add(mapping.provider_symbol_id)

    @property
    def contract_months(self) -> dict[str, str]:
        self.validate()
        return {mapping.code: mapping.contract_month for mapping in self.mappings}


def portfolio_web_chart_mapping_status(
    portfolio: PortfolioSpec,
    contract_months: dict[str, str],
) -> tuple[PortfolioProviderMappingRow, ...]:
    portfolio.validate()
    expected_codes = {leg.code for leg in portfolio.legs}
    if set(contract_months) != expected_codes:
        raise CarverBlocked("portfolio mapping status requires exact contract months for all legs")
    rows: list[PortfolioProviderMappingRow] = []
    for leg in portfolio.legs:
        contract_month = contract_months[leg.code]
        display_symbol = _display_symbol(leg.code, contract_month)
        provider_symbol_id = LOCKED_WEB_CHART_PROVIDER_SYMBOLS.get((leg.code, contract_month, display_symbol))
        rows.append(
            PortfolioProviderMappingRow(
                contract_code=leg.code,
                contract_month=contract_month,
                display_symbol=display_symbol,
                status=ProviderMappingStatus.LOCKED if provider_symbol_id else ProviderMappingStatus.UNRESOLVED,
                provider_symbol_id=provider_symbol_id,
            )
        )
    return tuple(rows)


def require_locked_portfolio_web_chart_mapping(rows: tuple[PortfolioProviderMappingRow, ...]) -> None:
    if not rows:
        raise CarverBlocked("portfolio web chart mapping rows are missing")
    for row in rows:
        if row.status is not ProviderMappingStatus.LOCKED or not row.provider_symbol_id:
            raise CarverBlocked(f"web chart mapping for {row.contract_code} {row.contract_month} is unresolved")


def require_locked_provider_mapping_set(mapping_set: PortfolioProviderMappingSet) -> None:
    mapping_set.validate()


def portfolio_conformance_from_daily_bars(
    portfolio: PortfolioSpec,
    daily_bars: dict[str, CompletedDailyMarketBar],
    annual_risk_estimates: dict[str, TimedValue],
    fx_rates: dict[str, TimedValue],
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST,
) -> dict[str, SizingResult]:
    portfolio.validate()
    expected_codes = {leg.code for leg in portfolio.legs}
    if set(daily_bars) != expected_codes:
        raise CarverBlocked("portfolio daily bars must exactly match portfolio legs")
    if set(annual_risk_estimates) != expected_codes:
        raise CarverBlocked("portfolio risk estimates must exactly match portfolio legs")
    if set(fx_rates) != expected_codes:
        raise CarverBlocked("portfolio FX rates must exactly match portfolio legs")

    timestamps = {daily_bars[code].timestamp for code in expected_codes}
    if len(timestamps) != 1:
        raise CarverBlocked("portfolio daily bars must share one completed date")
    as_of = next(iter(timestamps))

    market_inputs: dict[str, LegMarketInput] = {}
    for leg in portfolio.legs:
        bar = daily_bars[leg.code]
        bar.validate()
        if bar.contract != leg.contract:
            raise CarverBlocked("portfolio daily bar contract does not match portfolio leg")
        risk = annual_risk_estimates[leg.code]
        fx = fx_rates[leg.code]
        if risk.as_of != as_of or fx.as_of != as_of:
            raise CarverBlocked("portfolio risk and FX timestamps must align to completed date")
        market_inputs[leg.code] = LegMarketInput(
            current_held_price=TimedValue(bar.close, as_of),
            annual_risk_estimate=risk,
            fx_rate=fx,
            risk_estimate_prevalidated=True,
        )

    if portfolio.portfolio_id == "P01_RISK_PARITY_EXAMPLE":
        return p01_synthetic_conformance(
            portfolio,
            next(iter(daily_bars.values())).completed_bar,
            market_inputs,
            rounding_policy,
        )
    if portfolio.portfolio_id == "P02_ALL_WEATHER_EXAMPLE":
        return p02_synthetic_conformance(
            portfolio,
            next(iter(daily_bars.values())).completed_bar,
            market_inputs,
            rounding_policy,
        )
    raise CarverBlocked("portfolio conformance is locked only for P01/P02")


def _display_symbol(contract_code: str, contract_month: str) -> str:
    if len(contract_month) != 5 or contract_month[2] != "-":
        raise CarverBlocked("contract month must use MM-YY")
    month, year = contract_month.split("-")
    month_names = {
        "01": "JAN",
        "02": "FEB",
        "03": "MAR",
        "04": "APR",
        "05": "MAY",
        "06": "JUN",
        "07": "JUL",
        "08": "AUG",
        "09": "SEP",
        "10": "OCT",
        "11": "NOV",
        "12": "DEC",
    }
    if month not in month_names:
        raise CarverBlocked("contract month has invalid display month")
    return f"{contract_code} {month_names[month]}{year}"

```

# FILE: src\carver\spine\portfolio_completion.py

```text
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from .m0 import BackAdjustmentSpec, CarverBlocked, RollRuleSpec, SessionCalendarSpec, SourceRuleStatus, require_non_empty_text
from .m3 import PortfolioSpec
from .portfolio_conformance import (
    PortfolioProviderMappingSet,
    PortfolioProviderMappingRow,
    ProviderMappingStatus,
    portfolio_web_chart_mapping_status,
    require_locked_provider_mapping_set,
)


@dataclass(frozen=True)
class SourceArtifactRef:
    path: str

    def validate(self, name: str) -> None:
        require_non_empty_text(name, self.path)
        path = Path(self.path)
        if path.is_absolute() or ".." in path.parts:
            raise CarverBlocked(f"{name} must be a repo-local relative path")
        if len(path.parts) < 3 or path.parts[0] != "docs" or path.parts[1] not in {"process", "researchops"}:
            raise CarverBlocked(f"{name} must point to a repo-local markdown process/researchops artifact")
        if path.suffix.lower() != ".md":
            raise CarverBlocked(f"{name} must point to a markdown artifact")
        repo_root = Path(__file__).resolve().parents[3]
        try:
            resolved = (repo_root / path).resolve(strict=True)
        except FileNotFoundError as exc:
            raise CarverBlocked(f"{name} does not exist") from exc
        try:
            resolved.relative_to(repo_root)
        except ValueError as exc:
            raise CarverBlocked(f"{name} must stay inside the Carver workspace") from exc
        if not resolved.is_file():
            raise CarverBlocked(f"{name} must be a file")


class PortfolioIntakeMode(StrEnum):
    DIRECT_DAILY_PRIMARY = "DIRECT_DAILY_PRIMARY"
    MINUTE_DERIVED_FALLBACK = "MINUTE_DERIVED_FALLBACK"


class PortfolioCompletionStatus(StrEnum):
    SYNTHETIC_READY_REAL_DATA_BLOCKED = "SYNTHETIC_READY_REAL_DATA_BLOCKED"
    REAL_DATA_READY_NOT_BACKTEST_AUTHORIZATION = "REAL_DATA_READY_NOT_BACKTEST_AUTHORIZATION"


@dataclass(frozen=True)
class RiskFxInputContract:
    as_of: datetime
    annual_risk_status: SourceRuleStatus
    fx_status: SourceRuleStatus
    annual_risk_artifact: SourceArtifactRef | None = None
    fx_artifact: SourceArtifactRef | None = None

    def validate(self) -> None:
        if self.as_of.tzinfo is None or self.as_of.utcoffset() is None:
            raise CarverBlocked("risk/FX contract timestamp must be timezone-aware")
        if self.as_of.hour or self.as_of.minute or self.as_of.second or self.as_of.microsecond:
            raise CarverBlocked("risk/FX contract timestamp must be date-aligned")
        if self.annual_risk_status is SourceRuleStatus.LOCKED:
            if not isinstance(self.annual_risk_artifact, SourceArtifactRef):
                raise CarverBlocked("annual risk artifact is unresolved")
            self.annual_risk_artifact.validate("annual risk artifact")
        if self.fx_status is SourceRuleStatus.LOCKED:
            if not isinstance(self.fx_artifact, SourceArtifactRef):
                raise CarverBlocked("FX artifact is unresolved")
            self.fx_artifact.validate("FX artifact")

    def blockers(self) -> tuple[str, ...]:
        self.validate()
        items: list[str] = []
        if self.annual_risk_status is not SourceRuleStatus.LOCKED:
            items.append("annual risk input contract is unresolved")
        if self.fx_status is not SourceRuleStatus.LOCKED:
            items.append("FX input contract is unresolved")
        return tuple(items)


@dataclass(frozen=True)
class IntakeRouteContract:
    mode: PortfolioIntakeMode
    status: SourceRuleStatus = SourceRuleStatus.UNRESOLVED
    source_artifact: SourceArtifactRef | None = None

    def validate(self) -> None:
        if not isinstance(self.mode, PortfolioIntakeMode):
            raise CarverBlocked("portfolio intake mode must be locked")
        if self.status is SourceRuleStatus.LOCKED:
            if not isinstance(self.source_artifact, SourceArtifactRef):
                raise CarverBlocked("intake route source artifact is unresolved")
            self.source_artifact.validate("intake route source artifact")

    def blockers(self) -> tuple[str, ...]:
        self.validate()
        if self.status is not SourceRuleStatus.LOCKED:
            return ("intake route contract is unresolved",)
        return ()


@dataclass(frozen=True)
class PortfolioCompletionReport:
    portfolio_id: str
    intake_contract: IntakeRouteContract
    mapping_rows: tuple[PortfolioProviderMappingRow, ...]
    session_calendar: SessionCalendarSpec
    roll_rule: RollRuleSpec
    back_adjustment: BackAdjustmentSpec
    session_artifact: SourceArtifactRef | None
    roll_artifact: SourceArtifactRef | None
    back_adjustment_artifact: SourceArtifactRef | None
    risk_fx_contract: RiskFxInputContract
    blockers: tuple[str, ...]

    @property
    def intake_mode(self) -> PortfolioIntakeMode:
        return self.intake_contract.mode

    @property
    def status(self) -> PortfolioCompletionStatus:
        if self.blockers:
            return PortfolioCompletionStatus.SYNTHETIC_READY_REAL_DATA_BLOCKED
        return PortfolioCompletionStatus.REAL_DATA_READY_NOT_BACKTEST_AUTHORIZATION

    def require_real_data_ready(self) -> None:
        if self.status is not PortfolioCompletionStatus.REAL_DATA_READY_NOT_BACKTEST_AUTHORIZATION:
            raise CarverBlocked("; ".join(self.blockers))


def require_real_data_conformance_preflight(report: PortfolioCompletionReport) -> None:
    report.require_real_data_ready()


def build_portfolio_completion_report(
    portfolio: PortfolioSpec,
    contract_months: dict[str, str],
    risk_fx_contract: RiskFxInputContract,
    provider_mapping_set: PortfolioProviderMappingSet | None = None,
    intake_contract: IntakeRouteContract | None = None,
    session_calendar: SessionCalendarSpec | None = None,
    roll_rule: RollRuleSpec | None = None,
    back_adjustment: BackAdjustmentSpec | None = None,
    session_artifact: SourceArtifactRef | None = None,
    roll_artifact: SourceArtifactRef | None = None,
    back_adjustment_artifact: SourceArtifactRef | None = None,
) -> PortfolioCompletionReport:
    portfolio.validate()
    if intake_contract is None:
        intake_contract = IntakeRouteContract(PortfolioIntakeMode.DIRECT_DAILY_PRIMARY)
    if session_calendar is None:
        session_calendar = SessionCalendarSpec("P01/P02 session calendar")
    if roll_rule is None:
        roll_rule = RollRuleSpec("P01/P02 roll rule")
    if back_adjustment is None:
        back_adjustment = BackAdjustmentSpec("P01/P02 back-adjustment rule")
    intake_contract.validate()
    risk_fx_contract.validate()
    if provider_mapping_set is not None:
        require_locked_provider_mapping_set(provider_mapping_set)
        if provider_mapping_set.portfolio != portfolio:
            raise CarverBlocked("provider mapping set portfolio does not match completion portfolio")
        if provider_mapping_set.contract_months != contract_months:
            raise CarverBlocked("provider mapping set months do not match completion months")
    mapping_rows = portfolio_web_chart_mapping_status(portfolio, contract_months)
    blockers: list[str] = []
    for row in mapping_rows:
        if row.status is not ProviderMappingStatus.LOCKED:
            blockers.append(f"provider mapping unresolved for {row.contract_code} {row.contract_month}")
    try:
        session_calendar.require_locked()
    except CarverBlocked:
        blockers.append("session calendar is unresolved")
    try:
        roll_rule.require_locked()
    except CarverBlocked:
        blockers.append("roll rule is unresolved")
    try:
        back_adjustment.require_locked()
    except CarverBlocked:
        blockers.append("back-adjustment rule is unresolved")
    blockers.extend(
        locked_rule_artifact_blockers(
            session_calendar,
            roll_rule,
            back_adjustment,
            session_artifact,
            roll_artifact,
            back_adjustment_artifact,
        )
    )
    blockers.extend(intake_contract.blockers())
    blockers.extend(risk_fx_contract.blockers())
    return PortfolioCompletionReport(
        portfolio_id=portfolio.portfolio_id,
        intake_contract=intake_contract,
        mapping_rows=mapping_rows,
        session_calendar=session_calendar,
        roll_rule=roll_rule,
        back_adjustment=back_adjustment,
        session_artifact=session_artifact,
        roll_artifact=roll_artifact,
        back_adjustment_artifact=back_adjustment_artifact,
        risk_fx_contract=risk_fx_contract,
        blockers=tuple(blockers),
    )


def locked_rule_artifact_blockers(
    session_calendar: SessionCalendarSpec,
    roll_rule: RollRuleSpec,
    back_adjustment: BackAdjustmentSpec,
    session_artifact: SourceArtifactRef | None,
    roll_artifact: SourceArtifactRef | None,
    back_adjustment_artifact: SourceArtifactRef | None,
) -> tuple[str, ...]:
    blockers: list[str] = []
    if session_calendar.status is SourceRuleStatus.LOCKED:
        if not isinstance(session_artifact, SourceArtifactRef):
            blockers.append("session calendar artifact is unresolved")
        else:
            try:
                session_artifact.validate("session calendar artifact")
            except CarverBlocked:
                blockers.append("session calendar artifact is unresolved")
    if roll_rule.status is SourceRuleStatus.LOCKED:
        if not isinstance(roll_artifact, SourceArtifactRef):
            blockers.append("roll rule artifact is unresolved")
        else:
            try:
                roll_artifact.validate("roll rule artifact")
            except CarverBlocked:
                blockers.append("roll rule artifact is unresolved")
    if back_adjustment.status is SourceRuleStatus.LOCKED:
        if not isinstance(back_adjustment_artifact, SourceArtifactRef):
            blockers.append("back-adjustment artifact is unresolved")
        else:
            try:
                back_adjustment_artifact.validate("back-adjustment artifact")
            except CarverBlocked:
                blockers.append("back-adjustment artifact is unresolved")
    return tuple(blockers)

```

# FILE: src\carver\spine\__init__.py

```text
"""First-spine machinery for synthetic conformance tests."""

from .m0 import (
    BackAdjustmentSpec,
    BarConvention,
    CarverBlocked,
    CompletedBar,
    ContractSpec,
    CostSourceSpec,
    LaneClass,
    RollRuleSpec,
    SessionCalendarSpec,
    SourceRulePlaceholder,
    SourceRuleStatus,
)
from .m1 import RoundingPolicy, SizingInput, SizingResult, TimedValue, size_contracts
from .continuous import ContinuousContractRuleSet, ContinuousSeriesRequest, build_continuous_back_adjusted_series
from .daily_bars import (
    CompletedDailyMarketBar,
    DailyDerivationSession,
    derive_completed_daily_from_bound_web_chart,
    derive_completed_daily_from_minute_export,
    derive_completed_daily_from_web_chart,
    normalize_direct_daily_bound_web_chart,
    normalize_direct_daily_web_chart_bar,
)
from .m3 import PortfolioLeg, PortfolioSpec, p01_risk_parity, p02_all_weather
from .minute_export import (
    DEFAULT_MINUTE_EXPORT_QUARANTINE,
    EXPECTED_MINUTE_EXPORT_HEADER,
    MinuteBar,
    MinuteExportSpec,
    parse_minute_export_file,
    parse_minute_export_text,
)
from .s03 import S03RiskConfig, S03RiskEstimate, SyntheticDailyPrice, estimate_s03_annual_risk
from .web_chart_api import (
    ALLOWED_CHART_ENDPOINTS,
    DEFAULT_WEB_CHART_QUARANTINE,
    LOCKED_WEB_CHART_PROVIDER_SYMBOLS,
    MAX_SYNTHETIC_CHART_ELEMENTS,
    ChartBarType,
    BoundWebChartResponse,
    LockedWebChartSymbol,
    WebChartBar,
    WebChartProbePlan,
    WebChartRequest,
    WebChartSymbol,
    assert_safe_web_chart_endpoint,
    normalize_bound_web_chart_response,
    normalize_bound_web_chart_response_file,
    normalize_web_chart_response_file,
    normalize_web_chart_response,
    web_chart_response_request_binding,
)
from .portfolio_conformance import (
    LockedPortfolioProviderMapping,
    PortfolioProviderMappingSet,
    PortfolioProviderMappingRow,
    ProviderMappingStatus,
    portfolio_conformance_from_daily_bars,
    portfolio_web_chart_mapping_status,
    require_locked_provider_mapping_set,
    require_locked_portfolio_web_chart_mapping,
)
from .portfolio_completion import (
    PortfolioCompletionReport,
    PortfolioCompletionStatus,
    IntakeRouteContract,
    PortfolioIntakeMode,
    RiskFxInputContract,
    SourceArtifactRef,
    build_portfolio_completion_report,
    require_real_data_conformance_preflight,
)

__all__ = [
    "BackAdjustmentSpec",
    "BarConvention",
    "BoundWebChartResponse",
    "CarverBlocked",
    "CompletedBar",
    "CompletedDailyMarketBar",
    "ContractSpec",
    "ContinuousContractRuleSet",
    "ContinuousSeriesRequest",
    "CostSourceSpec",
    "DailyDerivationSession",
    "DEFAULT_MINUTE_EXPORT_QUARANTINE",
    "DEFAULT_WEB_CHART_QUARANTINE",
    "ALLOWED_CHART_ENDPOINTS",
    "ChartBarType",
    "LaneClass",
    "LOCKED_WEB_CHART_PROVIDER_SYMBOLS",
    "MAX_SYNTHETIC_CHART_ELEMENTS",
    "LockedPortfolioProviderMapping",
    "LockedWebChartSymbol",
    "EXPECTED_MINUTE_EXPORT_HEADER",
    "MinuteBar",
    "MinuteExportSpec",
    "PortfolioLeg",
    "PortfolioCompletionReport",
    "PortfolioCompletionStatus",
    "IntakeRouteContract",
    "PortfolioIntakeMode",
    "PortfolioProviderMappingRow",
    "PortfolioProviderMappingSet",
    "PortfolioSpec",
    "ProviderMappingStatus",
    "RoundingPolicy",
    "RiskFxInputContract",
    "SourceArtifactRef",
    "RollRuleSpec",
    "S03RiskConfig",
    "S03RiskEstimate",
    "SessionCalendarSpec",
    "SourceRulePlaceholder",
    "SourceRuleStatus",
    "SyntheticDailyPrice",
    "SizingInput",
    "SizingResult",
    "TimedValue",
    "WebChartBar",
    "WebChartProbePlan",
    "WebChartRequest",
    "WebChartSymbol",
    "assert_safe_web_chart_endpoint",
    "build_continuous_back_adjusted_series",
    "build_portfolio_completion_report",
    "require_real_data_conformance_preflight",
    "derive_completed_daily_from_minute_export",
    "derive_completed_daily_from_web_chart",
    "derive_completed_daily_from_bound_web_chart",
    "estimate_s03_annual_risk",
    "normalize_web_chart_response",
    "normalize_bound_web_chart_response",
    "normalize_web_chart_response_file",
    "normalize_bound_web_chart_response_file",
    "normalize_direct_daily_web_chart_bar",
    "normalize_direct_daily_bound_web_chart",
    "web_chart_response_request_binding",
    "p01_risk_parity",
    "p02_all_weather",
    "portfolio_conformance_from_daily_bars",
    "portfolio_web_chart_mapping_status",
    "parse_minute_export_file",
    "parse_minute_export_text",
    "require_locked_portfolio_web_chart_mapping",
    "require_locked_provider_mapping_set",
    "size_contracts",
]

```

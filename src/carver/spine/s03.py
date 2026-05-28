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

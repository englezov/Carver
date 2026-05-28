from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isclose, isfinite
from numbers import Real

from .m0 import CompletedBar, LaneClass, CarverBlocked, require_source_native
from .m1 import RoundingPolicy, SizingInput, SizingResult, TimedValue, size_contracts


@dataclass(frozen=True)
class PortfolioLeg:
    code: str
    name: str
    weight: float
    multiplier: float
    currency: str = "USD"


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
        _validate_positive("portfolio capital", self.capital)
        _validate_positive("portfolio target risk", self.target_risk)
        _validate_positive("portfolio IDM", self.idm)
        if not isclose(sum(leg.weight for leg in self.legs), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise CarverBlocked("portfolio weights must sum to 1")
        for leg in self.legs:
            if not leg.code or not leg.name:
                raise CarverBlocked("portfolio leg identity is unresolved")
            _validate_positive("portfolio leg weight", leg.weight)
            _validate_positive("portfolio leg multiplier", leg.multiplier)

    def size_legs(
        self,
        completed_bar: CompletedBar,
        market_inputs: dict[str, "LegMarketInput"],
        rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST,
    ) -> dict[str, SizingResult]:
        self.validate()
        completed_bar.validate()
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
            PortfolioLeg("MES", "S&P 500 micro future", 0.50, 5),
            PortfolioLeg("ZN", "US 10-year bond future", 0.50, 1000),
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
            PortfolioLeg("MES", "S&P 500 micro future", 0.25, 5),
            PortfolioLeg("ZN", "US 10-year bond future", 0.125, 1000),
            PortfolioLeg("ZF", "US 5-year bond future", 0.125, 1000),
            PortfolioLeg("QM", "WTI Crude Oil mini future", 0.125, 500),
            PortfolioLeg("ZC", "Corn future", 0.125, 5000),
            PortfolioLeg("MGC", "Gold micro future", 0.25, 10),
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


def _validate_positive(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"{name} must be positive")

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

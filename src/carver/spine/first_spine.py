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

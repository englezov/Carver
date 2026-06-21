from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor, isclose, isfinite
from numbers import Real

from .m0 import (
    CompletedBar,
    ContractSpec,
    LaneClass,
    SourceRuleStatus,
    CarverBlocked,
    require_finite_positive,
    require_non_empty_text,
    require_source_native,
)
from .m1 import RoundingPolicy, SizingInput, SizingResult, TimedValue, size_contracts
from .m2 import FORECAST_CAP


P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_ID = (
    "P07_SYNTHETIC_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_NOT_PRODUCTION"
)
P07_FORECAST_DIVISOR = 10.0
P07_JUMBO_REFERENCE_IDM = 2.47
P07_BOOK_REFERENCE_TARGET_RISK = 0.20
P07_STRATEGY_ELEVEN_COST_LIMIT_SR = 0.15


@dataclass(frozen=True)
class P07CompleteCombinedPortfolioSourceLocks:
    s11_input_provenance_status: SourceRuleStatus
    member_identity_status: SourceRuleStatus
    member_taxonomy_status: SourceRuleStatus
    instrument_weight_status: SourceRuleStatus
    idm_status: SourceRuleStatus
    target_risk_capital_status: SourceRuleStatus
    price_risk_status: SourceRuleStatus
    fx_status: SourceRuleStatus
    cost_eligibility_status: SourceRuleStatus
    forecast_cap_status: SourceRuleStatus
    position_input_status: SourceRuleStatus
    output_boundary_status: SourceRuleStatus

    def validate(self) -> None:
        for name, status in (
            ("P07 S11 input provenance", self.s11_input_provenance_status),
            ("P07 member identity", self.member_identity_status),
            ("P07 member taxonomy", self.member_taxonomy_status),
            ("P07 instrument weight", self.instrument_weight_status),
            ("P07 IDM", self.idm_status),
            ("P07 target risk and capital", self.target_risk_capital_status),
            ("P07 price risk", self.price_risk_status),
            ("P07 FX", self.fx_status),
            ("P07 cost eligibility", self.cost_eligibility_status),
            ("P07 forecast cap", self.forecast_cap_status),
            ("P07 position input", self.position_input_status),
            ("P07 output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"{name} source is unresolved")


@dataclass(frozen=True)
class P07SyntheticMember:
    member_id: str
    contract: ContractSpec
    asset_class: str
    group: str
    identity_status: SourceRuleStatus
    taxonomy_status: SourceRuleStatus

    def validate(self) -> None:
        require_non_empty_text("P07 member id", self.member_id)
        require_non_empty_text("P07 member asset class", self.asset_class)
        require_non_empty_text("P07 member group", self.group)
        self.contract.validate()
        if self.contract.code != self.member_id:
            raise CarverBlocked("P07 member id must match contract code")
        if self.identity_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("P07 member identity source is unresolved")
        if self.taxonomy_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("P07 member taxonomy source is unresolved")


@dataclass(frozen=True)
class P07SyntheticMarketInput:
    member_id: str
    current_held_price: TimedValue
    annual_risk_estimate: TimedValue
    daily_price_risk: TimedValue
    fx_rate: TimedValue
    risk_adjusted_cost_per_trade: TimedValue
    price_risk_prevalidated: bool = True
    fx_prevalidated: bool = True
    cost_eligibility_prevalidated: bool = True

    def validate(self, completed_bar: CompletedBar) -> None:
        require_non_empty_text("P07 market input member id", self.member_id)
        for name, value in (
            ("current held price", self.current_held_price),
            ("annual risk estimate", self.annual_risk_estimate),
            ("daily price risk", self.daily_price_risk),
            ("FX rate", self.fx_rate),
            ("risk-adjusted cost per trade", self.risk_adjusted_cost_per_trade),
        ):
            if value.as_of != completed_bar.timestamp:
                raise CarverBlocked(f"P07 {name} timestamp must align to completed bar")
            require_finite_positive(f"P07 {name}", value.value)
        if not self.price_risk_prevalidated:
            raise CarverBlocked("P07 price risk must be prevalidated")
        if not self.fx_prevalidated:
            raise CarverBlocked("P07 FX must be prevalidated")
        if not self.cost_eligibility_prevalidated:
            raise CarverBlocked("P07 cost eligibility must be prevalidated")


@dataclass(frozen=True)
class P07SyntheticS11CombinedForecastInput:
    member_id: str
    final_capped_s11_forecast: TimedValue
    label: str
    input_status: SourceRuleStatus

    def validate(self, completed_bar: CompletedBar) -> None:
        require_non_empty_text("P07 S11 forecast member id", self.member_id)
        require_non_empty_text("P07 S11 forecast label", self.label)
        if not self.label.startswith("synthetic_s11_"):
            raise CarverBlocked("P07 S11 forecast input label must be synthetic")
        if self.input_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("P07 S11 forecast input source is unresolved")
        if self.final_capped_s11_forecast.as_of != completed_bar.timestamp:
            raise CarverBlocked("P07 S11 forecast timestamp must align to completed bar")
        _require_finite("P07 S11 final capped forecast", self.final_capped_s11_forecast.value)
        if abs(float(self.final_capped_s11_forecast.value)) > FORECAST_CAP:
            raise CarverBlocked("P07 S11 forecast input must already be capped")


@dataclass(frozen=True)
class P07CompleteCombinedPortfolioRequest:
    completed_bar: CompletedBar
    members: tuple[P07SyntheticMember, ...]
    market_inputs: tuple[P07SyntheticMarketInput, ...]
    s11_forecast_inputs: tuple[P07SyntheticS11CombinedForecastInput, ...]
    capital: TimedValue
    target_risk: TimedValue
    idm: TimedValue
    source_locks: P07CompleteCombinedPortfolioSourceLocks
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class P07MemberDesiredPositionInput:
    member_id: str
    contract: ContractSpec
    asset_class: str
    group: str
    instrument_weight: float
    final_capped_s11_combined_forecast: float
    forecast_multiplier: float
    base_sizing: SizingResult
    desired_unrounded_contracts: float
    desired_rounded_contracts: int


@dataclass(frozen=True)
class P07CompleteCombinedPortfolioResult:
    portfolio_id: str
    completed_bar: CompletedBar
    member_results: tuple[P07MemberDesiredPositionInput, ...]
    source_native_lane: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES
    is_synthetic_conformance: bool = True
    production_source_locked: bool = False
    interpretable_performance: bool = False
    performance_metrics: tuple[str, ...] = ()
    return_outputs: tuple[str, ...] = ()
    pnl_outputs: tuple[str, ...] = ()
    trading_orders: tuple[str, ...] = ()

    @property
    def member_ids(self) -> tuple[str, ...]:
        return tuple(result.member_id for result in self.member_results)


def p07_complete_combined_trend_carry_portfolio_conformance(
    request: P07CompleteCombinedPortfolioRequest,
) -> P07CompleteCombinedPortfolioResult:
    require_source_native(request.lane_class)
    request.completed_bar.validate()
    request.source_locks.validate()
    _validate_context_values(request)

    members = _validate_members(request.members)
    market_inputs = _validate_market_inputs(request, members)
    forecasts = _validate_s11_forecast_inputs(request, members)
    weights = p07_handcrafted_instrument_weights(request.members)

    outputs: list[P07MemberDesiredPositionInput] = []
    for member in request.members:
        market = market_inputs[member.member_id]
        base_sizing = size_contracts(
            SizingInput(
                lane_class=request.lane_class,
                completed_bar=request.completed_bar,
                capital=request.capital,
                target_risk=request.target_risk,
                current_held_price=market.current_held_price,
                annual_risk_estimate=market.annual_risk_estimate,
                multiplier=member.contract.multiplier,
                fx_rate=market.fx_rate,
                risk_estimate_prevalidated=market.price_risk_prevalidated,
                instrument_weight=TimedValue(weights[member.member_id], request.completed_bar.timestamp),
                idm=request.idm,
                rounding_policy=request.rounding_policy,
            )
        )
        final_forecast = forecasts[member.member_id].final_capped_s11_forecast.value
        _require_finite("P07 final capped S11 combined forecast", final_forecast)
        if abs(float(final_forecast)) > FORECAST_CAP:
            raise CarverBlocked("P07 final S11 combined forecast must be capped")
        forecast_multiplier = final_forecast / P07_FORECAST_DIVISOR
        desired_unrounded = base_sizing.unrounded_contracts * forecast_multiplier
        _require_finite("P07 desired unrounded contracts", desired_unrounded)
        outputs.append(
            P07MemberDesiredPositionInput(
                member_id=member.member_id,
                contract=member.contract,
                asset_class=member.asset_class,
                group=member.group,
                instrument_weight=weights[member.member_id],
                final_capped_s11_combined_forecast=final_forecast,
                forecast_multiplier=forecast_multiplier,
                base_sizing=base_sizing,
                desired_unrounded_contracts=desired_unrounded,
                desired_rounded_contracts=_round_contracts(desired_unrounded, request.rounding_policy),
            )
        )

    result = P07CompleteCombinedPortfolioResult(
        portfolio_id=P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_ID,
        completed_bar=request.completed_bar,
        member_results=tuple(outputs),
    )
    if result.member_ids != tuple(members):
        raise CarverBlocked("P07 result member order drifted")
    if result.source_native_lane is not LaneClass.SOURCE_NATIVE_FUTURES:
        raise CarverBlocked("P07 result lane drifted")
    if (
        not result.is_synthetic_conformance
        or result.production_source_locked
        or result.interpretable_performance
        or result.performance_metrics
        or result.return_outputs
        or result.pnl_outputs
        or result.trading_orders
    ):
        raise CarverBlocked("P07 complete combined conformance must emit desired position inputs only")
    return result


def p07_handcrafted_instrument_weights(members: tuple[P07SyntheticMember, ...]) -> dict[str, float]:
    member_ids = _validate_members(members)
    asset_classes = _ordered_unique(member.asset_class for member in members)
    weights: dict[str, float] = {}
    asset_weight = 1.0 / len(asset_classes)
    for asset_class in asset_classes:
        asset_members = tuple(member for member in members if member.asset_class == asset_class)
        groups = _ordered_unique(member.group for member in asset_members)
        group_weight = asset_weight / len(groups)
        for group in groups:
            group_members = tuple(member for member in asset_members if member.group == group)
            member_weight = group_weight / len(group_members)
            for member in group_members:
                weights[member.member_id] = member_weight
    if tuple(weights) != member_ids:
        raise CarverBlocked("P07 handcrafted weights drifted from member order")
    if not isclose(sum(weights.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked("P07 handcrafted instrument weights must sum to 1")
    return weights


def _validate_context_values(request: P07CompleteCombinedPortfolioRequest) -> None:
    for name, timed in (
        ("capital", request.capital),
        ("target risk", request.target_risk),
        ("IDM", request.idm),
    ):
        if timed.as_of != request.completed_bar.timestamp:
            raise CarverBlocked(f"P07 {name} timestamp must align to completed bar")
        require_finite_positive(f"P07 {name}", timed.value)


def _validate_members(members: tuple[P07SyntheticMember, ...]) -> tuple[str, ...]:
    if not members:
        raise CarverBlocked("P07 requires at least one synthetic member")
    member_ids: list[str] = []
    for member in members:
        member.validate()
        if member.member_id in member_ids:
            raise CarverBlocked("P07 member identities must be unique")
        member_ids.append(member.member_id)
    return tuple(member_ids)


def _validate_market_inputs(
    request: P07CompleteCombinedPortfolioRequest,
    member_ids: tuple[str, ...],
) -> dict[str, P07SyntheticMarketInput]:
    if not request.market_inputs:
        raise CarverBlocked("P07 market inputs are required")
    inputs: dict[str, P07SyntheticMarketInput] = {}
    for market in request.market_inputs:
        market.validate(request.completed_bar)
        if market.member_id in inputs:
            raise CarverBlocked("P07 market inputs must be unique")
        inputs[market.member_id] = market
    if tuple(inputs) != member_ids:
        raise CarverBlocked("P07 market inputs must exactly match member order")
    return inputs


def _validate_s11_forecast_inputs(
    request: P07CompleteCombinedPortfolioRequest,
    member_ids: tuple[str, ...],
) -> dict[str, P07SyntheticS11CombinedForecastInput]:
    if not request.s11_forecast_inputs:
        raise CarverBlocked("P07 S11 forecast inputs are required")
    inputs: dict[str, P07SyntheticS11CombinedForecastInput] = {}
    for forecast in request.s11_forecast_inputs:
        forecast.validate(request.completed_bar)
        if forecast.member_id in inputs:
            raise CarverBlocked("P07 S11 forecast inputs must be unique")
        inputs[forecast.member_id] = forecast
    if tuple(inputs) != member_ids:
        raise CarverBlocked("P07 S11 forecast inputs must exactly match member order")
    return inputs


def _ordered_unique(values) -> tuple[str, ...]:
    seen: list[str] = []
    for value in values:
        require_non_empty_text("P07 taxonomy value", value)
        if value not in seen:
            seen.append(value)
    if not seen:
        raise CarverBlocked("P07 taxonomy cannot be empty")
    return tuple(seen)


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")


def _round_contracts(value: float, policy: RoundingPolicy) -> int:
    _require_finite("P07 rounded contract input", value)
    if policy is RoundingPolicy.NEAREST:
        return int(round(value))
    if policy is RoundingPolicy.FLOOR:
        return floor(value)
    if policy is RoundingPolicy.CEILING:
        return ceil(value)
    if policy is RoundingPolicy.TRUNCATE:
        return int(value)
    raise CarverBlocked("P07 rounding policy is unresolved")

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
from .m2 import FORECAST_CAP, ForecastBlockRequest, ForecastBlockResult, ForecastRuleInput, combine_forecast_block
from .s10 import s10_carry_fdm_for_eligible_spans, s10_carry_rule_id


P06_COMPLETE_CARRY_PORTFOLIO_ID = "P06_SYNTHETIC_COMPLETE_CARRY_PORTFOLIO_CONFORMANCE_NOT_PRODUCTION"
P06_FORECAST_DIVISOR = 10.0
P06_JUMBO_REFERENCE_IDM = 2.47
P06_BOOK_REFERENCE_TARGET_RISK = 0.20
P06_STRATEGY_TEN_COST_LIMIT_SR = 0.15
P06_CARRY_TURNOVER_BY_SPAN = {
    5: 5.75,
    20: 3.12,
    60: 1.82,
    120: 1.22,
}


@dataclass(frozen=True)
class P06CompleteCarryPortfolioSourceLocks:
    s10_input_provenance_status: SourceRuleStatus
    member_identity_status: SourceRuleStatus
    member_taxonomy_status: SourceRuleStatus
    instrument_weight_status: SourceRuleStatus
    idm_status: SourceRuleStatus
    target_risk_capital_status: SourceRuleStatus
    price_risk_status: SourceRuleStatus
    fx_status: SourceRuleStatus
    cost_eligibility_status: SourceRuleStatus
    eligible_carry_span_set_status: SourceRuleStatus
    forecast_weight_status: SourceRuleStatus
    carry_fdm_status: SourceRuleStatus
    forecast_cap_status: SourceRuleStatus
    position_input_status: SourceRuleStatus
    output_boundary_status: SourceRuleStatus

    def validate(self) -> None:
        for name, status in (
            ("P06 S10 input provenance", self.s10_input_provenance_status),
            ("P06 member identity", self.member_identity_status),
            ("P06 member taxonomy", self.member_taxonomy_status),
            ("P06 instrument weight", self.instrument_weight_status),
            ("P06 IDM", self.idm_status),
            ("P06 target risk and capital", self.target_risk_capital_status),
            ("P06 price risk", self.price_risk_status),
            ("P06 FX", self.fx_status),
            ("P06 cost eligibility", self.cost_eligibility_status),
            ("P06 eligible carry span set", self.eligible_carry_span_set_status),
            ("P06 forecast weight", self.forecast_weight_status),
            ("P06 carry FDM", self.carry_fdm_status),
            ("P06 forecast cap", self.forecast_cap_status),
            ("P06 position input", self.position_input_status),
            ("P06 output boundary", self.output_boundary_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"{name} source is unresolved")


@dataclass(frozen=True)
class P06SyntheticMember:
    member_id: str
    contract: ContractSpec
    asset_class: str
    group: str
    identity_status: SourceRuleStatus
    taxonomy_status: SourceRuleStatus

    def validate(self) -> None:
        require_non_empty_text("P06 member id", self.member_id)
        require_non_empty_text("P06 member asset class", self.asset_class)
        require_non_empty_text("P06 member group", self.group)
        self.contract.validate()
        if self.contract.code != self.member_id:
            raise CarverBlocked("P06 member id must match contract code")
        if self.identity_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("P06 member identity source is unresolved")
        if self.taxonomy_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("P06 member taxonomy source is unresolved")


@dataclass(frozen=True)
class P06SyntheticMarketInput:
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
        require_non_empty_text("P06 market input member id", self.member_id)
        for name, value in (
            ("current held price", self.current_held_price),
            ("annual risk estimate", self.annual_risk_estimate),
            ("daily price risk", self.daily_price_risk),
            ("FX rate", self.fx_rate),
            ("risk-adjusted cost per trade", self.risk_adjusted_cost_per_trade),
        ):
            if value.as_of != completed_bar.timestamp:
                raise CarverBlocked(f"P06 {name} timestamp must align to completed bar")
            require_finite_positive(f"P06 {name}", value.value)
        if not self.price_risk_prevalidated:
            raise CarverBlocked("P06 price risk must be prevalidated")
        if not self.fx_prevalidated:
            raise CarverBlocked("P06 FX must be prevalidated")
        if not self.cost_eligibility_prevalidated:
            raise CarverBlocked("P06 cost eligibility must be prevalidated")


@dataclass(frozen=True)
class P06SyntheticS10CarryForecastInput:
    member_id: str
    span: int
    capped_forecast: TimedValue
    label: str
    input_status: SourceRuleStatus

    @property
    def rule_id(self) -> str:
        return s10_carry_rule_id(self.span)

    def validate(self, completed_bar: CompletedBar) -> None:
        require_non_empty_text("P06 S10 forecast member id", self.member_id)
        require_non_empty_text("P06 S10 forecast label", self.label)
        if not self.label.startswith("synthetic_s10_"):
            raise CarverBlocked("P06 S10 forecast input label must be synthetic")
        if self.input_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("P06 S10 forecast input source is unresolved")
        if self.capped_forecast.as_of != completed_bar.timestamp:
            raise CarverBlocked("P06 S10 forecast timestamp must align to completed bar")
        _require_finite("P06 S10 capped forecast", self.capped_forecast.value)
        if abs(float(self.capped_forecast.value)) > FORECAST_CAP:
            raise CarverBlocked("P06 S10 forecast input must already be capped")
        if self.span not in P06_CARRY_TURNOVER_BY_SPAN:
            raise CarverBlocked("P06 carry span is not source-locked")


@dataclass(frozen=True)
class P06EligibleCarrySet:
    member_id: str
    spans: tuple[int, ...]
    eligibility_status: SourceRuleStatus

    def validate(self) -> None:
        require_non_empty_text("P06 eligible carry member id", self.member_id)
        if self.eligibility_status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("P06 eligible carry span set source is unresolved")
        _validate_eligible_carry_spans(self.spans)

    @property
    def rule_ids(self) -> tuple[str, ...]:
        return tuple(s10_carry_rule_id(span) for span in self.spans)

    @property
    def fdm(self) -> float:
        return s10_carry_fdm_for_eligible_spans(self.spans)


@dataclass(frozen=True)
class P06CompleteCarryPortfolioRequest:
    completed_bar: CompletedBar
    members: tuple[P06SyntheticMember, ...]
    market_inputs: tuple[P06SyntheticMarketInput, ...]
    forecast_inputs: tuple[P06SyntheticS10CarryForecastInput, ...]
    eligible_carry_sets: tuple[P06EligibleCarrySet, ...]
    capital: TimedValue
    target_risk: TimedValue
    idm: TimedValue
    source_locks: P06CompleteCarryPortfolioSourceLocks
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class P06MemberDesiredPositionInput:
    member_id: str
    contract: ContractSpec
    asset_class: str
    group: str
    instrument_weight: float
    eligible_spans: tuple[int, ...]
    s10_forecast_block: ForecastBlockResult
    final_capped_p06_forecast: float
    forecast_multiplier: float
    base_sizing: SizingResult
    desired_unrounded_contracts: float
    desired_rounded_contracts: int


@dataclass(frozen=True)
class P06CompleteCarryPortfolioResult:
    portfolio_id: str
    completed_bar: CompletedBar
    member_results: tuple[P06MemberDesiredPositionInput, ...]
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


def p06_complete_carry_portfolio_conformance(
    request: P06CompleteCarryPortfolioRequest,
) -> P06CompleteCarryPortfolioResult:
    require_source_native(request.lane_class)
    request.completed_bar.validate()
    request.source_locks.validate()
    _validate_context_values(request)

    members = _validate_members(request.members)
    market_inputs = _validate_market_inputs(request, members)
    eligible_sets = _validate_eligible_sets(request.eligible_carry_sets, members)
    forecast_inputs = _validate_forecast_inputs(request, members)
    weights = p06_handcrafted_instrument_weights(request.members)

    outputs: list[P06MemberDesiredPositionInput] = []
    for member in request.members:
        eligible = eligible_sets[member.member_id]
        member_forecasts = forecast_inputs[member.member_id]
        if tuple(member_forecasts) != eligible.spans:
            raise CarverBlocked("P06 forecast inputs must exactly match eligible carry spans")

        rule_inputs = tuple(
            ForecastRuleInput(
                rule_id=s10_carry_rule_id(span),
                raw_forecast=member_forecasts[span].capped_forecast,
                scalar=1.0,
                scalar_status=request.source_locks.s10_input_provenance_status,
                cap=FORECAST_CAP,
                cap_status=request.source_locks.forecast_cap_status,
                lane_class=request.lane_class,
            )
            for span in eligible.spans
        )
        block = _combine_s10_outputs(request, eligible, rule_inputs)
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
        final_forecast = block.final_forecast
        _require_finite("P06 final capped forecast", final_forecast)
        if abs(float(final_forecast)) > FORECAST_CAP:
            raise CarverBlocked("P06 final forecast must be capped")
        forecast_multiplier = final_forecast / P06_FORECAST_DIVISOR
        desired_unrounded = base_sizing.unrounded_contracts * forecast_multiplier
        _require_finite("P06 desired unrounded contracts", desired_unrounded)
        outputs.append(
            P06MemberDesiredPositionInput(
                member_id=member.member_id,
                contract=member.contract,
                asset_class=member.asset_class,
                group=member.group,
                instrument_weight=weights[member.member_id],
                eligible_spans=eligible.spans,
                s10_forecast_block=block,
                final_capped_p06_forecast=final_forecast,
                forecast_multiplier=forecast_multiplier,
                base_sizing=base_sizing,
                desired_unrounded_contracts=desired_unrounded,
                desired_rounded_contracts=_round_contracts(desired_unrounded, request.rounding_policy),
            )
        )

    result = P06CompleteCarryPortfolioResult(
        portfolio_id=P06_COMPLETE_CARRY_PORTFOLIO_ID,
        completed_bar=request.completed_bar,
        member_results=tuple(outputs),
    )
    if result.member_ids != tuple(members):
        raise CarverBlocked("P06 result member order drifted")
    if result.source_native_lane is not LaneClass.SOURCE_NATIVE_FUTURES:
        raise CarverBlocked("P06 result lane drifted")
    if (
        not result.is_synthetic_conformance
        or result.production_source_locked
        or result.interpretable_performance
        or result.performance_metrics
        or result.return_outputs
        or result.pnl_outputs
        or result.trading_orders
    ):
        raise CarverBlocked("P06 complete carry conformance must emit desired position inputs only")
    return result


def p06_handcrafted_instrument_weights(members: tuple[P06SyntheticMember, ...]) -> dict[str, float]:
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
        raise CarverBlocked("P06 handcrafted weights drifted from member order")
    if not isclose(sum(weights.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked("P06 handcrafted instrument weights must sum to 1")
    return weights


def _combine_s10_outputs(
    request: P06CompleteCarryPortfolioRequest,
    eligible: P06EligibleCarrySet,
    rule_inputs: tuple[ForecastRuleInput, ...],
) -> ForecastBlockResult:
    return combine_forecast_block(
        ForecastBlockRequest(
            completed_bar=request.completed_bar,
            rule_inputs=rule_inputs,
            allowed_rule_ids=eligible.rule_ids,
            fdm=eligible.fdm,
            weight_status=request.source_locks.forecast_weight_status,
            fdm_status=request.source_locks.carry_fdm_status,
            speed_rule_status=request.source_locks.eligible_carry_span_set_status,
            combined_cap=FORECAST_CAP,
            combined_cap_status=request.source_locks.forecast_cap_status,
            lane_class=request.lane_class,
        )
    )


def _validate_context_values(request: P06CompleteCarryPortfolioRequest) -> None:
    for name, timed in (
        ("capital", request.capital),
        ("target risk", request.target_risk),
        ("IDM", request.idm),
    ):
        if timed.as_of != request.completed_bar.timestamp:
            raise CarverBlocked(f"P06 {name} timestamp must align to completed bar")
        require_finite_positive(f"P06 {name}", timed.value)


def _validate_members(members: tuple[P06SyntheticMember, ...]) -> tuple[str, ...]:
    if not members:
        raise CarverBlocked("P06 requires at least one synthetic member")
    member_ids: list[str] = []
    for member in members:
        member.validate()
        if member.member_id in member_ids:
            raise CarverBlocked("P06 member identities must be unique")
        member_ids.append(member.member_id)
    return tuple(member_ids)


def _validate_market_inputs(
    request: P06CompleteCarryPortfolioRequest,
    member_ids: tuple[str, ...],
) -> dict[str, P06SyntheticMarketInput]:
    if not request.market_inputs:
        raise CarverBlocked("P06 market inputs are required")
    inputs: dict[str, P06SyntheticMarketInput] = {}
    for market in request.market_inputs:
        market.validate(request.completed_bar)
        if market.member_id in inputs:
            raise CarverBlocked("P06 market inputs must be unique")
        inputs[market.member_id] = market
    if tuple(inputs) != member_ids:
        raise CarverBlocked("P06 market inputs must exactly match member order")
    return inputs


def _validate_eligible_sets(
    eligible_sets: tuple[P06EligibleCarrySet, ...],
    member_ids: tuple[str, ...],
) -> dict[str, P06EligibleCarrySet]:
    if not eligible_sets:
        raise CarverBlocked("P06 eligible carry span sets are required")
    by_member: dict[str, P06EligibleCarrySet] = {}
    for eligible in eligible_sets:
        eligible.validate()
        if eligible.member_id in by_member:
            raise CarverBlocked("P06 eligible carry span sets must be unique")
        by_member[eligible.member_id] = eligible
    if tuple(by_member) != member_ids:
        raise CarverBlocked("P06 eligible carry span sets must exactly match member order")
    return by_member


def _validate_forecast_inputs(
    request: P06CompleteCarryPortfolioRequest,
    member_ids: tuple[str, ...],
) -> dict[str, dict[int, P06SyntheticS10CarryForecastInput]]:
    if not request.forecast_inputs:
        raise CarverBlocked("P06 S10 forecast inputs are required")
    by_member: dict[str, dict[int, P06SyntheticS10CarryForecastInput]] = {member_id: {} for member_id in member_ids}
    for forecast in request.forecast_inputs:
        forecast.validate(request.completed_bar)
        if forecast.member_id not in by_member:
            raise CarverBlocked("P06 S10 forecast input references an unknown member")
        if forecast.span in by_member[forecast.member_id]:
            raise CarverBlocked("P06 S10 forecast inputs must be unique by member and span")
        by_member[forecast.member_id][forecast.span] = forecast
    if any(not spans for spans in by_member.values()):
        raise CarverBlocked("P06 every member requires S10 forecast inputs")
    return by_member


def _validate_eligible_carry_spans(spans: tuple[int, ...]) -> None:
    s10_carry_fdm_for_eligible_spans(spans)


def _ordered_unique(values) -> tuple[str, ...]:
    seen: list[str] = []
    for value in values:
        require_non_empty_text("P06 taxonomy value", value)
        if value not in seen:
            seen.append(value)
    if not seen:
        raise CarverBlocked("P06 taxonomy cannot be empty")
    return tuple(seen)


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")


def _round_contracts(value: float, policy: RoundingPolicy) -> int:
    _require_finite("P06 rounded contract input", value)
    if policy is RoundingPolicy.NEAREST:
        return int(round(value))
    if policy is RoundingPolicy.FLOOR:
        return floor(value)
    if policy is RoundingPolicy.CEILING:
        return ceil(value)
    if policy is RoundingPolicy.TRUNCATE:
        return int(value)
    raise CarverBlocked("P06 rounding policy is unresolved")

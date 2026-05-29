from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor, isclose, isfinite
from numbers import Real

from .m0 import CompletedBar, LaneClass, SourceRuleStatus, CarverBlocked, ContractSpec, require_finite_positive, require_source_native
from .m1 import RoundingPolicy, SizingInput, SizingResult, TimedValue, size_contracts
from .m3 import PortfolioLeg, PortfolioSpec, mes_contract, zf_contract, zn_contract
from .s09 import S09DailyPriceRiskRequest, s09_daily_price_risk
from .s09_phase1 import (
    S09_PHASE1_CONTRACT_MONTHS,
    S09_PHASE1_REQUIRED_DAILY_BARS,
    S09_PHASE1_ROOTS,
    S09Phase1MultiInstrumentConformanceResult,
)


P05_PHASE1_CONSTRUCTION_ID = "P05_PHASE1_MES_ZN_ZF_SEED_CONSTRUCTION_NOT_COMPLETE_PORTFOLIO"
P05_PHASE1_FORECAST_DIVISOR = 10.0
P05_PHASE1_EQUAL_SEED_WEIGHT = 1.0 / 3.0


@dataclass(frozen=True)
class P05Phase1ConstructionSourceLocks:
    capital_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    target_risk_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    instrument_weight_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    idm_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    daily_price_risk_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    risk_input_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    fx_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    contract_identity_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    forecast_to_position_scale_status: SourceRuleStatus = SourceRuleStatus.LOCKED

    def validate(self) -> None:
        for name, status in (
            ("capital", self.capital_status),
            ("target risk", self.target_risk_status),
            ("instrument weight", self.instrument_weight_status),
            ("IDM", self.idm_status),
            ("daily price risk", self.daily_price_risk_status),
            ("risk input", self.risk_input_status),
            ("FX", self.fx_status),
            ("contract identity", self.contract_identity_status),
            ("forecast-to-position scale", self.forecast_to_position_scale_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"P05 phase-1 {name} source is unresolved")


@dataclass(frozen=True)
class P05Phase1LegConstructionInput:
    root: str
    current_held_price: TimedValue
    annual_risk_estimate: TimedValue
    daily_price_risk: TimedValue
    fx_rate: TimedValue
    risk_estimate_prevalidated: bool = True

    def validate(self, as_of) -> None:
        if self.root not in S09_PHASE1_ROOTS:
            raise CarverBlocked("P05 phase-1 construction input root must be MES, ZN, or ZF")
        for name, value in (
            ("current held price", self.current_held_price),
            ("annual risk estimate", self.annual_risk_estimate),
            ("daily price risk", self.daily_price_risk),
            ("FX rate", self.fx_rate),
        ):
            if value.as_of != as_of:
                raise CarverBlocked(f"P05 phase-1 {name} timestamp must align to construction timestamp")
            require_finite_positive(f"P05 phase-1 {name}", value.value)
        if not self.risk_estimate_prevalidated:
            raise CarverBlocked("P05 phase-1 risk estimate must be prevalidated")


@dataclass(frozen=True)
class P05Phase1ConstructionRequest:
    forecast_conformance: S09Phase1MultiInstrumentConformanceResult
    portfolio: PortfolioSpec
    leg_inputs: tuple[P05Phase1LegConstructionInput, ...]
    capital: TimedValue
    target_risk: TimedValue
    idm: TimedValue
    source_locks: P05Phase1ConstructionSourceLocks = P05Phase1ConstructionSourceLocks()
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class P05Phase1InstrumentConstructionResult:
    root: str
    contract: ContractSpec
    weight: float
    final_forecast: float
    forecast_multiplier: float
    base_sizing: SizingResult
    desired_unrounded_contracts: float
    desired_rounded_contracts: int


@dataclass(frozen=True)
class P05Phase1ConstructionResult:
    construction_id: str
    instrument_results: tuple[P05Phase1InstrumentConstructionResult, ...]
    is_complete_p02: bool = False
    is_complete_p05: bool = False
    interpretable_performance: bool = False
    performance_metrics: tuple[str, ...] = ()

    @property
    def roots(self) -> tuple[str, ...]:
        return tuple(result.root for result in self.instrument_results)


def p05_phase1_seed_portfolio_spec(
    capital: float,
    target_risk: float,
    idm: float,
) -> PortfolioSpec:
    portfolio = PortfolioSpec(
        portfolio_id=P05_PHASE1_CONSTRUCTION_ID,
        lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
        capital=capital,
        target_risk=target_risk,
        idm=idm,
        legs=tuple(
            PortfolioLeg(contract, weight)
            for contract, weight in zip(
                (mes_contract(), zn_contract(), zf_contract()),
                (P05_PHASE1_EQUAL_SEED_WEIGHT, P05_PHASE1_EQUAL_SEED_WEIGHT, P05_PHASE1_EQUAL_SEED_WEIGHT),
                strict=True,
            )
        ),
    )
    portfolio.validate()
    return portfolio


def p05_phase1_portfolio_construction_conformance(
    request: P05Phase1ConstructionRequest,
) -> P05Phase1ConstructionResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    _validate_phase1_forecast_conformance(request.forecast_conformance)
    _validate_phase1_portfolio(request.portfolio)
    _validate_construction_timestamps(request)
    if tuple(leg.root for leg in request.leg_inputs) != S09_PHASE1_ROOTS:
        raise CarverBlocked("P05 phase-1 construction inputs must cover MES, ZN, and ZF in order")

    by_root = {result.root: result for result in request.forecast_conformance.instrument_results}
    outputs: list[P05Phase1InstrumentConstructionResult] = []
    construction_timestamp = request.forecast_conformance.instrument_results[0].forecast_result.as_of
    completed_bar = CompletedBar(construction_timestamp)

    for portfolio_leg, leg_input in zip(request.portfolio.legs, request.leg_inputs, strict=True):
        leg_input.validate(construction_timestamp)
        if portfolio_leg.code != leg_input.root:
            raise CarverBlocked("P05 phase-1 construction portfolio leg order does not match input root")
        forecast_result = by_root[leg_input.root].forecast_result
        if forecast_result.contract_code != leg_input.root:
            raise CarverBlocked("P05 phase-1 forecast contract code does not match construction input")

        expected_daily_risk = s09_daily_price_risk(
            S09DailyPriceRiskRequest(
                completed_bar=completed_bar,
                current_price=leg_input.current_held_price,
                annual_percentage_risk=leg_input.annual_risk_estimate,
                conversion_source_status=request.source_locks.daily_price_risk_status,
                lane_class=request.lane_class,
            )
        )
        if not isclose(expected_daily_risk.value, leg_input.daily_price_risk.value, rel_tol=0.0, abs_tol=1e-12):
            raise CarverBlocked("P05 phase-1 daily price risk does not match locked S09 conversion")

        base_sizing = size_contracts(
            SizingInput(
                lane_class=request.lane_class,
                completed_bar=completed_bar,
                capital=request.capital,
                target_risk=request.target_risk,
                current_held_price=leg_input.current_held_price,
                annual_risk_estimate=leg_input.annual_risk_estimate,
                multiplier=portfolio_leg.multiplier,
                fx_rate=leg_input.fx_rate,
                risk_estimate_prevalidated=leg_input.risk_estimate_prevalidated,
                instrument_weight=TimedValue(portfolio_leg.weight, construction_timestamp),
                idm=request.idm,
                rounding_policy=request.rounding_policy,
            )
        )
        final_forecast = forecast_result.final_forecast
        _require_finite("P05 phase-1 final forecast", final_forecast)
        if abs(final_forecast) > 20.0:
            raise CarverBlocked("P05 phase-1 final forecast must already be capped at +/-20")
        forecast_multiplier = final_forecast / P05_PHASE1_FORECAST_DIVISOR
        desired_unrounded = base_sizing.unrounded_contracts * forecast_multiplier
        _require_finite("P05 phase-1 desired unrounded contracts", desired_unrounded)
        outputs.append(
            P05Phase1InstrumentConstructionResult(
                root=leg_input.root,
                contract=portfolio_leg.contract,
                weight=portfolio_leg.weight,
                final_forecast=final_forecast,
                forecast_multiplier=forecast_multiplier,
                base_sizing=base_sizing,
                desired_unrounded_contracts=desired_unrounded,
                desired_rounded_contracts=_round_contracts(desired_unrounded, request.rounding_policy),
            )
        )

    result = P05Phase1ConstructionResult(P05_PHASE1_CONSTRUCTION_ID, tuple(outputs))
    if result.roots != S09_PHASE1_ROOTS:
        raise CarverBlocked("P05 phase-1 construction result roots drifted")
    if result.is_complete_p02 or result.is_complete_p05:
        raise CarverBlocked("P05 phase-1 construction seed must not be marked as a complete book portfolio")
    if result.interpretable_performance or result.performance_metrics:
        raise CarverBlocked("P05 phase-1 construction must not emit performance interpretation")
    return result


def _validate_phase1_forecast_conformance(result: S09Phase1MultiInstrumentConformanceResult) -> None:
    if result.roots != S09_PHASE1_ROOTS:
        raise CarverBlocked("P05 phase-1 construction requires MES, ZN, and ZF forecasts in order")
    if result.interpretable_portfolio_signal or result.performance_metrics:
        raise CarverBlocked("P05 phase-1 construction requires forecast-only S09 input")
    timestamp = result.instrument_results[0].forecast_result.as_of
    for instrument_result in result.instrument_results:
        if instrument_result.forecast_result.as_of != timestamp:
            raise CarverBlocked("P05 phase-1 forecasts must share one completed-bar timestamp")
        if instrument_result.input_row_count != S09_PHASE1_REQUIRED_DAILY_BARS:
            raise CarverBlocked("P05 phase-1 S09 input row count does not match the locked requirement")
        if instrument_result.source_contract_months != S09_PHASE1_CONTRACT_MONTHS:
            raise CarverBlocked("P05 phase-1 S09 source months do not match the locked phase-1 chain")


def _validate_phase1_portfolio(portfolio: PortfolioSpec) -> None:
    portfolio.validate()
    if portfolio.portfolio_id != P05_PHASE1_CONSTRUCTION_ID:
        raise CarverBlocked("P05 phase-1 construction requires the locked seed portfolio id")
    if tuple(leg.code for leg in portfolio.legs) != S09_PHASE1_ROOTS:
        raise CarverBlocked("P05 phase-1 construction portfolio must be MES, ZN, and ZF in order")
    expected_contracts = (mes_contract(), zn_contract(), zf_contract())
    for leg, expected in zip(portfolio.legs, expected_contracts, strict=True):
        if leg.contract != expected:
            raise CarverBlocked("P05 phase-1 construction portfolio has contract identity drift")


def _validate_construction_timestamps(request: P05Phase1ConstructionRequest) -> None:
    construction_timestamp = request.forecast_conformance.instrument_results[0].forecast_result.as_of
    for name, timed in (
        ("capital", request.capital),
        ("target risk", request.target_risk),
        ("IDM", request.idm),
    ):
        if timed.as_of != construction_timestamp:
            raise CarverBlocked(f"P05 phase-1 {name} timestamp must align to construction timestamp")
        require_finite_positive(f"P05 phase-1 {name}", timed.value)
    if not isclose(request.capital.value, request.portfolio.capital, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked("P05 phase-1 capital does not match portfolio spec")
    if not isclose(request.target_risk.value, request.portfolio.target_risk, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked("P05 phase-1 target risk does not match portfolio spec")
    if not isclose(request.idm.value, request.portfolio.idm, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked("P05 phase-1 IDM does not match portfolio spec")


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")


def _round_contracts(value: float, policy: RoundingPolicy) -> int:
    _require_finite("P05 phase-1 rounded contract input", value)
    if policy is RoundingPolicy.NEAREST:
        return int(round(value))
    if policy is RoundingPolicy.FLOOR:
        return floor(value)
    if policy is RoundingPolicy.CEILING:
        return ceil(value)
    if policy is RoundingPolicy.TRUNCATE:
        return int(value)
    raise CarverBlocked("P05 phase-1 rounding policy is unresolved")

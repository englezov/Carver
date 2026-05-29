from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isclose, isfinite
from numbers import Real

from .daily_bars import CompletedDailyMarketBar
from .m0 import (
    ContractSpec,
    LaneClass,
    SourceRuleStatus,
    CarverBlocked,
    require_finite_positive,
    require_non_empty_text,
    require_source_native,
)
from .m1 import TimedValue


@dataclass(frozen=True)
class M5CarryConstructionSourceLocks:
    instrument_identity_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    held_contract_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    comparison_contract_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    completed_price_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    sign_convention_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    expiry_distance_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    price_risk_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    seasonal_wrong_sign_policy_status: SourceRuleStatus = SourceRuleStatus.LOCKED

    def validate(self) -> None:
        for name, status in (
            ("instrument identity", self.instrument_identity_status),
            ("held contract", self.held_contract_status),
            ("comparison contract", self.comparison_contract_status),
            ("completed price", self.completed_price_status),
            ("raw-carry sign convention", self.sign_convention_status),
            ("expiry distance annualization", self.expiry_distance_status),
            ("price risk", self.price_risk_status),
            ("seasonal/wrong-sign policy", self.seasonal_wrong_sign_policy_status),
        ):
            if status is not SourceRuleStatus.LOCKED:
                raise CarverBlocked(f"M5 {name} source is unresolved")


@dataclass(frozen=True)
class M5RawCarrySignConvention:
    label: str
    multiplier: float
    status: SourceRuleStatus = SourceRuleStatus.LOCKED

    def validate(self) -> None:
        if self.status is not SourceRuleStatus.LOCKED:
            raise CarverBlocked("M5 raw-carry sign convention is unresolved")
        require_non_empty_text("M5 raw-carry sign convention label", self.label)
        if isinstance(self.multiplier, bool) or not isinstance(self.multiplier, Real) or not isfinite(float(self.multiplier)):
            raise CarverBlocked("M5 raw-carry sign multiplier must be finite")
        if not isclose(abs(float(self.multiplier)), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise CarverBlocked("M5 raw-carry sign multiplier must be +1 or -1")


@dataclass(frozen=True)
class M5CarryConstructionRequest:
    instrument: ContractSpec
    held_bar: CompletedDailyMarketBar
    comparison_bar: CompletedDailyMarketBar
    sign_convention: M5RawCarrySignConvention
    expiry_distance_years: TimedValue
    price_risk: TimedValue
    source_locks: M5CarryConstructionSourceLocks = M5CarryConstructionSourceLocks()
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES


@dataclass(frozen=True)
class M5CarryConstructionResult:
    instrument: ContractSpec
    held_contract_month: str
    comparison_contract_month: str
    sign_convention_label: str
    raw_carry: float
    expiry_distance_years: float
    annualization_factor: float
    annualized_carry: float
    risk_adjusted_carry: float
    carry_timestamp: datetime
    held_price_timestamp: datetime
    comparison_price_timestamp: datetime
    interpretable_trading_signal: bool = False
    performance_metrics: tuple[str, ...] = ()
    position_outputs: tuple[str, ...] = ()


def m5_synthetic_carry_construction_conformance(
    request: M5CarryConstructionRequest,
) -> M5CarryConstructionResult:
    require_source_native(request.lane_class)
    request.source_locks.validate()
    request.sign_convention.validate()
    request.instrument.validate()
    request.held_bar.validate()
    request.comparison_bar.validate()
    _validate_curve_identity(request)
    _validate_timed_inputs(request)

    raw_carry = request.sign_convention.multiplier * (request.comparison_bar.close - request.held_bar.close)
    _require_finite("M5 raw carry", raw_carry)
    annualization_factor = 1.0 / request.expiry_distance_years.value
    require_finite_positive("M5 annualization factor", annualization_factor)
    annualized_carry = raw_carry * annualization_factor
    _require_finite("M5 annualized carry", annualized_carry)
    risk_adjusted_carry = annualized_carry / request.price_risk.value
    _require_finite("M5 risk-adjusted carry", risk_adjusted_carry)

    result = M5CarryConstructionResult(
        instrument=request.instrument,
        held_contract_month=request.held_bar.contract_month,
        comparison_contract_month=request.comparison_bar.contract_month,
        sign_convention_label=request.sign_convention.label,
        raw_carry=raw_carry,
        expiry_distance_years=request.expiry_distance_years.value,
        annualization_factor=annualization_factor,
        annualized_carry=annualized_carry,
        risk_adjusted_carry=risk_adjusted_carry,
        carry_timestamp=request.held_bar.timestamp,
        held_price_timestamp=request.held_bar.timestamp,
        comparison_price_timestamp=request.comparison_bar.timestamp,
    )
    if result.interpretable_trading_signal or result.performance_metrics or result.position_outputs:
        raise CarverBlocked("M5 carry construction must not emit performance, trading, or position outputs")
    return result


def _validate_curve_identity(request: M5CarryConstructionRequest) -> None:
    if request.held_bar.contract != request.instrument:
        raise CarverBlocked("M5 held contract identity does not match the requested instrument")
    if request.comparison_bar.contract != request.instrument:
        raise CarverBlocked("M5 comparison contract identity does not match the requested instrument")
    if request.held_bar.contract_month == request.comparison_bar.contract_month:
        raise CarverBlocked("M5 held and comparison contract months must be distinct")


def _validate_timed_inputs(request: M5CarryConstructionRequest) -> None:
    expected = request.held_bar.timestamp
    if request.comparison_bar.timestamp != expected:
        raise CarverBlocked("M5 held and comparison prices must share one completed-bar timestamp")
    for name, timed in (
        ("expiry distance", request.expiry_distance_years),
        ("price risk", request.price_risk),
    ):
        if timed.as_of != expected:
            raise CarverBlocked(f"M5 {name} timestamp must align to completed bar")
        require_finite_positive(f"M5 {name}", timed.value)


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from math import ceil, floor, isfinite
from numbers import Real

from .m0 import CompletedBar, LaneClass, CarverBlocked, require_source_native


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
    _validate_positive("capital", sizing.capital.value)
    _validate_positive("target_risk", sizing.target_risk.value)
    _validate_positive("current_held_price", sizing.current_held_price.value)
    _validate_positive("annual_risk_estimate", sizing.annual_risk_estimate.value)
    _validate_positive("multiplier", sizing.multiplier)
    _validate_positive("fx_rate", sizing.fx_rate.value)

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
    _validate_positive("contract_risk", contract_risk)

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


def _validate_positive(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"{name} must be positive")


def _context_value(name: str, timed: TimedValue | None, default: float) -> float:
    if timed is None:
        return default
    _validate_positive(name, timed.value)
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

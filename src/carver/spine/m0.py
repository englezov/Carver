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

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from ..m0 import CarverBlocked
from .constants import BLOCKED_TICK
from .identity import ReplayIdentity
from .validation import (
    require_hash,
    require_hour_aligned_utc,
    require_integer,
    require_positive_number,
    require_text,
)


class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderKind(StrEnum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"


@dataclass(frozen=True)
class LimitOrderLedgerRow:
    identity: ReplayIdentity
    decision_timestamp: datetime
    side: OrderSide
    quantity: int
    current_position_before_order: int
    target_position_after_fill: int
    formula_implied_price: float
    executable_tick_price: float
    tick_rounding_direction: str
    tick_policy_hash: str
    order_plan_hash: str
    limit_order_hash: str

    def validate(self) -> None:
        self.identity.validate()
        require_hour_aligned_utc("S27 v2 limit decision timestamp", self.decision_timestamp)
        if self.decision_timestamp != self.identity.decision_as_of_utc:
            raise CarverBlocked("S27 v2 limit row decision timestamp must match replay identity")
        if not isinstance(self.side, OrderSide):
            raise CarverBlocked("S27 v2 limit order side must be an OrderSide value")
        require_integer("S27 v2 limit quantity", self.quantity)
        if self.quantity != 1:
            raise CarverBlocked("S27 v2 limit quantity must be adjacent single lot")
        require_integer("S27 v2 limit current position", self.current_position_before_order)
        require_integer("S27 v2 limit target position", self.target_position_after_fill)
        expected_target = self.current_position_before_order + (1 if self.side is OrderSide.BUY else -1)
        if self.target_position_after_fill != expected_target:
            raise CarverBlocked("S27 v2 limit target must be adjacent to current position and agree with side")
        require_positive_number("S27 v2 formula-implied limit price", self.formula_implied_price)
        require_positive_number("S27 v2 executable tick limit price", self.executable_tick_price)
        require_text("S27 v2 tick rounding direction", self.tick_rounding_direction)
        try:
            require_hash("S27 v2 tick policy hash", self.tick_policy_hash)
        except CarverBlocked as exc:
            raise CarverBlocked(BLOCKED_TICK) from exc
        require_hash("S27 v2 order-plan hash", self.order_plan_hash)
        require_hash("S27 v2 limit-order hash", self.limit_order_hash)


@dataclass(frozen=True)
class MarketOrderLedgerRow:
    identity: ReplayIdentity
    decision_timestamp: datetime
    side: OrderSide
    quantity: int
    current_position_before_order: int
    target_position_after_fill: int
    trigger_source_condition: str
    market_order_trigger_hash: str
    order_plan_hash: str
    market_order_hash: str

    def validate(self) -> None:
        self.identity.validate()
        require_hour_aligned_utc("S27 v2 market decision timestamp", self.decision_timestamp)
        if self.decision_timestamp != self.identity.decision_as_of_utc:
            raise CarverBlocked("S27 v2 market row decision timestamp must match replay identity")
        if not isinstance(self.side, OrderSide):
            raise CarverBlocked("S27 v2 market order side must be an OrderSide value")
        require_integer("S27 v2 market quantity", self.quantity)
        if self.quantity <= 0:
            raise CarverBlocked("S27 v2 market quantity must be positive")
        require_integer("S27 v2 market current position", self.current_position_before_order)
        require_integer("S27 v2 market target position", self.target_position_after_fill)
        delta = self.target_position_after_fill - self.current_position_before_order
        if self.quantity != abs(delta):
            raise CarverBlocked("S27 v2 market quantity must equal current-to-target position delta")
        if delta > 0 and self.side is not OrderSide.BUY:
            raise CarverBlocked("S27 v2 market buy side must match positive target delta")
        if delta < 0 and self.side is not OrderSide.SELL:
            raise CarverBlocked("S27 v2 market sell side must match negative target delta")
        if delta == 0:
            raise CarverBlocked("S27 v2 market order must change position")
        require_text("S27 v2 market trigger source condition", self.trigger_source_condition)
        require_hash("S27 v2 market-order trigger hash", self.market_order_trigger_hash)
        require_hash("S27 v2 order-plan hash", self.order_plan_hash)
        require_hash("S27 v2 market-order hash", self.market_order_hash)

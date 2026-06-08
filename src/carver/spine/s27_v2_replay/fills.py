from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from ..m0 import CarverBlocked
from .identity import ReplayIdentity
from .orders import OrderKind, OrderSide
from .validation import require_hash, require_hour_aligned_utc, require_integer, require_positive_number


class FillPriceProvenance(StrEnum):
    LIMIT_ORDER_PRICE_FROM_FILLED_ORDER = "LIMIT_ORDER_PRICE_FROM_FILLED_ORDER"
    MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE = "MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE"


@dataclass(frozen=True)
class FillLedgerRow:
    identity: ReplayIdentity
    fill_timestamp: datetime
    order_plan_hash: str
    filled_order_hash: str
    order_hash: str
    transition_hash: str
    next_completed_hourly_fill_row_hash: str
    fill_decision_source_row_hash: str
    fill_condition_hash: str
    fill_price_provenance: FillPriceProvenance
    order_kind: OrderKind
    side: OrderSide
    quantity: int
    fill_price: float
    fill_hash: str
    submitted_limit_price: float | None = None
    market_order_trigger_hash: str | None = None

    def validate(self) -> None:
        self.identity.validate()
        require_hour_aligned_utc("S27 v2 fill timestamp", self.fill_timestamp)
        if self.fill_timestamp != self.identity.fill_as_of_utc:
            raise CarverBlocked("S27 v2 fill timestamp must match replay identity")
        require_hash("S27 v2 fill order-plan hash", self.order_plan_hash)
        require_hash("S27 v2 filled-order hash", self.filled_order_hash)
        require_hash("S27 v2 fill order hash", self.order_hash)
        require_hash("S27 v2 transition hash", self.transition_hash)
        require_hash("S27 v2 next completed hourly fill-row hash", self.next_completed_hourly_fill_row_hash)
        require_hash("S27 v2 fill decision source row hash", self.fill_decision_source_row_hash)
        if self.fill_decision_source_row_hash != self.next_completed_hourly_fill_row_hash:
            raise CarverBlocked("S27 v2 fill decision source must be the next completed hourly fill row")
        require_hash("S27 v2 fill condition hash", self.fill_condition_hash)
        if not isinstance(self.fill_price_provenance, FillPriceProvenance):
            raise CarverBlocked("S27 v2 fill price provenance must be a FillPriceProvenance value")
        if not isinstance(self.order_kind, OrderKind):
            raise CarverBlocked("S27 v2 fill order kind must be an OrderKind value")
        if not isinstance(self.side, OrderSide):
            raise CarverBlocked("S27 v2 fill side must be an OrderSide value")
        require_integer("S27 v2 fill quantity", self.quantity)
        if self.quantity <= 0:
            raise CarverBlocked("S27 v2 fill quantity must be positive")
        require_positive_number("S27 v2 fill price", self.fill_price)
        require_hash("S27 v2 fill hash", self.fill_hash)
        if self.order_kind is OrderKind.LIMIT:
            if self.fill_price_provenance is not FillPriceProvenance.LIMIT_ORDER_PRICE_FROM_FILLED_ORDER:
                raise CarverBlocked("S27 v2 limit fill must use limit-order fill-price provenance")
            if self.submitted_limit_price is None:
                raise CarverBlocked("S27 v2 limit fill requires submitted limit price")
            require_positive_number("S27 v2 submitted limit price", self.submitted_limit_price)
            if abs(self.fill_price - self.submitted_limit_price) > 1e-12:
                raise CarverBlocked("S27 v2 limit fill price must equal submitted executable limit price")
            if self.market_order_trigger_hash is not None:
                raise CarverBlocked("S27 v2 limit fill must not carry market trigger hash")
        elif self.order_kind is OrderKind.MARKET:
            if self.fill_price_provenance is not FillPriceProvenance.MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE:
                raise CarverBlocked("S27 v2 market fill must use next completed close provenance")
            if self.submitted_limit_price is not None:
                raise CarverBlocked("S27 v2 market fill must not carry submitted limit price")
            if self.market_order_trigger_hash is None:
                raise CarverBlocked("S27 v2 market fill requires trigger hash")
            require_hash("S27 v2 market trigger hash", self.market_order_trigger_hash)
        else:
            raise CarverBlocked("S27 v2 fill order kind is unresolved")

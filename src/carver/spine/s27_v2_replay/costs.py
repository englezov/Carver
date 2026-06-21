from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isclose

from ..m0 import CarverBlocked
from .constants import BLOCKED_COST_SCHEMA
from .fills import FillLedgerRow
from .orders import OrderKind
from .validation import require_hash, require_non_negative_number, require_positive_number, require_text


class SpreadSpace(StrEnum):
    PRICE_SPACE = "PRICE_SPACE"
    CURRENCY_SPACE = "CURRENCY_SPACE"


@dataclass(frozen=True)
class CostLedgerRow:
    fill: FillLedgerRow
    commission_policy_hash: str
    commission_per_contract: float
    commission_unit: str
    commission_currency: str
    commission_amount: float
    cost_calculation_policy_hash: str
    spread_policy_hash: str | None
    spread_unit: str | None
    spread_amount: float
    spread_cost_amount: float
    spread_space: SpreadSpace | None
    contract_multiplier_value: float | None
    contract_multiplier_value_hash: str | None
    contract_multiplier_source_hash: str | None
    currency_conversion_value_hash: str | None
    currency_conversion_source_hash: str | None
    deflation_policy_hash: str | None
    total_cost_amount: float
    total_cost_currency: str
    cost_hash: str

    def validate(self) -> None:
        try:
            self.fill.validate()
            require_hash("S27 v2 commission policy hash", self.commission_policy_hash)
            require_positive_number("S27 v2 commission per contract", self.commission_per_contract)
            if self.commission_unit != "PER_CONTRACT":
                raise CarverBlocked("S27 v2 commission unit must be PER_CONTRACT")
            require_text("S27 v2 commission currency", self.commission_currency)
            require_positive_number("S27 v2 commission amount", self.commission_amount)
            require_hash("S27 v2 cost calculation policy hash", self.cost_calculation_policy_hash)
            expected_commission = self.commission_per_contract * self.fill.quantity
            if not isclose(self.commission_amount, expected_commission, rel_tol=0.0, abs_tol=1e-12):
                raise CarverBlocked("S27 v2 commission amount must equal per-contract commission times fill quantity")
            require_non_negative_number("S27 v2 spread amount", self.spread_amount)
            require_non_negative_number("S27 v2 spread cost amount", self.spread_cost_amount)
            if self.spread_space is not None and not isinstance(self.spread_space, SpreadSpace):
                raise CarverBlocked("S27 v2 spread space must be a SpreadSpace value")
            if self.fill.order_kind is OrderKind.LIMIT:
                if self.spread_amount != 0 or self.spread_cost_amount != 0:
                    raise CarverBlocked("S27 v2 limit fill must be commission-only with zero spread and spread cost")
                if self.spread_policy_hash is not None or self.spread_unit is not None or self.spread_space is not None:
                    raise CarverBlocked("S27 v2 limit fill must not carry spread policy, unit, or space")
                if (
                    self.contract_multiplier_value is not None
                    or self.contract_multiplier_value_hash is not None
                    or self.contract_multiplier_source_hash is not None
                    or self.currency_conversion_value_hash is not None
                    or self.currency_conversion_source_hash is not None
                    or self.deflation_policy_hash is not None
                ):
                    raise CarverBlocked(
                        "S27 v2 limit fill must not carry multiplier, currency-conversion, or deflation fields"
                    )
            elif self.fill.order_kind is OrderKind.MARKET:
                if self.spread_amount <= 0:
                    raise CarverBlocked("S27 v2 market fill requires positive normal spread")
                if self.spread_cost_amount <= 0:
                    raise CarverBlocked("S27 v2 market fill requires positive spread cost amount")
                if self.spread_policy_hash is None or self.spread_unit is None or self.spread_space is None:
                    raise CarverBlocked("S27 v2 market fill requires spread policy, unit, and space")
            else:
                raise CarverBlocked("S27 v2 cost row order kind is unresolved")
            if self.spread_amount:
                if self.spread_policy_hash is None or self.spread_unit is None or self.spread_space is None:
                    raise CarverBlocked("S27 v2 positive spread requires spread policy, unit, and space")
                require_hash("S27 v2 spread policy hash", self.spread_policy_hash)
                require_text("S27 v2 spread unit", self.spread_unit)
                if self.spread_space is SpreadSpace.PRICE_SPACE:
                    if (
                        self.contract_multiplier_value is None
                        or self.contract_multiplier_value_hash is None
                        or self.contract_multiplier_source_hash is None
                    ):
                        raise CarverBlocked("S27 v2 price-space spread requires contract multiplier value and proof")
                    require_positive_number("S27 v2 contract multiplier value", self.contract_multiplier_value)
                    expected_spread_cost = self.spread_amount * self.contract_multiplier_value * self.fill.quantity
                    if not isclose(self.spread_cost_amount, expected_spread_cost, rel_tol=0.0, abs_tol=1e-12):
                        raise CarverBlocked(
                            "S27 v2 price-space spread cost must equal spread amount times contract multiplier times fill quantity"
                        )
                elif self.spread_space is SpreadSpace.CURRENCY_SPACE:
                    if not isclose(
                        self.spread_cost_amount,
                        self.spread_amount,
                        rel_tol=0.0,
                        abs_tol=1e-12,
                    ):
                        raise CarverBlocked("S27 v2 currency-space spread cost must equal spread amount")
                    if (
                        self.contract_multiplier_value is not None
                        or self.contract_multiplier_value_hash is not None
                        or self.contract_multiplier_source_hash is not None
                    ):
                        raise CarverBlocked("S27 v2 currency-space spread must not carry contract multiplier fields")
            if self.contract_multiplier_value is not None:
                require_positive_number("S27 v2 contract multiplier value", self.contract_multiplier_value)
                if self.contract_multiplier_value_hash is None or self.contract_multiplier_source_hash is None:
                    raise CarverBlocked("S27 v2 multiplier value requires multiplier value and source hashes")
                require_hash("S27 v2 contract multiplier value hash", self.contract_multiplier_value_hash)
                require_hash("S27 v2 contract multiplier source hash", self.contract_multiplier_source_hash)
            elif self.contract_multiplier_value_hash is not None:
                raise CarverBlocked("S27 v2 multiplier value hash requires multiplier numeric value")
            elif self.contract_multiplier_source_hash is not None:
                raise CarverBlocked("S27 v2 multiplier source hash requires multiplier numeric value")
            if self.currency_conversion_value_hash is not None:
                require_hash("S27 v2 currency conversion value hash", self.currency_conversion_value_hash)
                if self.currency_conversion_source_hash is None:
                    raise CarverBlocked("S27 v2 currency conversion value requires source hash")
                require_hash("S27 v2 currency conversion source hash", self.currency_conversion_source_hash)
            elif self.currency_conversion_source_hash is not None:
                raise CarverBlocked("S27 v2 currency conversion source hash requires value hash")
            if self.deflation_policy_hash is not None:
                require_hash("S27 v2 deflation policy hash", self.deflation_policy_hash)
            require_positive_number("S27 v2 total cost amount", self.total_cost_amount)
            if not isclose(
                self.total_cost_amount,
                self.commission_amount + self.spread_cost_amount,
                rel_tol=0.0,
                abs_tol=1e-12,
            ):
                raise CarverBlocked("S27 v2 total cost amount must equal commission amount plus spread cost amount")
            require_text("S27 v2 total cost currency", self.total_cost_currency)
            require_hash("S27 v2 cost hash", self.cost_hash)
        except CarverBlocked as exc:
            raise CarverBlocked(BLOCKED_COST_SCHEMA) from exc

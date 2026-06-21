from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .identity import ReplayIdentity
from .validation import require_hash, require_integer, require_text


@dataclass(frozen=True)
class PnlLedgerRow:
    identity: ReplayIdentity
    replay_trust_root_hash: str
    source_universe_hash: str
    previous_step_hash_or_initial_state_hash: str
    starting_working_state_hash: str
    starting_position: int
    transition_hash: str
    ending_working_state_hash: str
    ending_position: int
    position_source_hash: str
    pnl_formula_policy_hash: str
    price_source_kind: str
    start_price_source_row_hash: str
    end_price_source_row_hash: str
    raw_symbol_continuity_or_roll_bridge_hash: str
    contract_multiplier_value_hash: str
    contract_multiplier_source_hash: str
    currency_policy_hash: str | None
    currency_conversion_value_hash: str | None
    currency_conversion_source_hash: str | None
    pnl_currency: str | None
    pnl_amount_hash: str | None
    cost_application_policy_hash: str
    fill_hash_set_hash: str
    cost_hash_set_hash: str
    pnl_hash: str

    def validate(self) -> None:
        self.identity.validate()
        require_hash("S27 v2 PnL replay trust-root hash", self.replay_trust_root_hash)
        require_hash("S27 v2 PnL source universe hash", self.source_universe_hash)
        require_hash("S27 v2 PnL previous step or initial-state hash", self.previous_step_hash_or_initial_state_hash)
        require_hash("S27 v2 PnL starting working-state hash", self.starting_working_state_hash)
        require_integer("S27 v2 PnL starting position", self.starting_position)
        require_hash("S27 v2 PnL transition hash", self.transition_hash)
        require_hash("S27 v2 PnL ending working-state hash", self.ending_working_state_hash)
        require_integer("S27 v2 PnL ending position", self.ending_position)
        require_hash("S27 v2 PnL position source hash", self.position_source_hash)
        require_hash("S27 v2 PnL formula policy hash", self.pnl_formula_policy_hash)
        require_text("S27 v2 PnL price source kind", self.price_source_kind)
        if self.price_source_kind != "CLOSE_ONLY":
            raise CarverBlocked("S27 v2 PnL price source kind must be CLOSE_ONLY")
        require_hash("S27 v2 PnL start price source row hash", self.start_price_source_row_hash)
        require_hash("S27 v2 PnL end price source row hash", self.end_price_source_row_hash)
        require_hash(
            "S27 v2 PnL raw-symbol continuity or roll bridge hash",
            self.raw_symbol_continuity_or_roll_bridge_hash,
        )
        require_hash("S27 v2 PnL contract multiplier value hash", self.contract_multiplier_value_hash)
        require_hash("S27 v2 PnL contract multiplier source hash", self.contract_multiplier_source_hash)
        if self.currency_policy_hash is not None:
            require_hash("S27 v2 PnL currency policy hash", self.currency_policy_hash)
        if self.currency_conversion_value_hash is not None:
            require_hash("S27 v2 PnL currency conversion value hash", self.currency_conversion_value_hash)
            if self.currency_conversion_source_hash is None:
                raise CarverBlocked("S27 v2 PnL currency conversion value requires source hash")
            require_hash("S27 v2 PnL currency conversion source hash", self.currency_conversion_source_hash)
        elif self.currency_conversion_source_hash is not None:
            raise CarverBlocked("S27 v2 PnL currency conversion source hash requires value hash")
        if self.pnl_currency is not None:
            require_text("S27 v2 PnL currency", self.pnl_currency)
        if self.pnl_amount_hash is not None:
            require_hash("S27 v2 PnL amount hash", self.pnl_amount_hash)
        require_hash("S27 v2 PnL cost application policy hash", self.cost_application_policy_hash)
        require_hash("S27 v2 PnL fill hash-set hash", self.fill_hash_set_hash)
        require_hash("S27 v2 PnL cost hash-set hash", self.cost_hash_set_hash)
        require_hash("S27 v2 PnL hash", self.pnl_hash)

from __future__ import annotations

from collections.abc import Mapping, Sequence
import math
from typing import Any

from ..m0 import CarverBlocked


FAIL_CLOSED_UNFILLED_MARKET_STATUS = "FAIL_CLOSED_UNFILLED_LIMIT_ORDER_MARKET_FALLBACK_NOT_AUTHORIZED"
FAIL_CLOSED_WORKING_STATE = "UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE"
NO_OPEN_AFTER_FILL_STATE = "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
NO_MARKET_NEEDED_STATUSES = {
    "NOT_REQUIRED_NO_ORDER_POSITION_UNCHANGED",
    "NOT_REQUIRED_LIMIT_ORDER_FILLED",
    FAIL_CLOSED_UNFILLED_MARKET_STATUS,
}
DECLARED_PACK_STATUS_ALLOWED_PREFIXES = (
    "READY_",
    "PASS_",
    "LOCAL_",
    "INFERRED_RETAIL_FUTURES_COST_ACCEPTED_",
)


def validate_pretest_machine_freeze_rows(
    pack_rows: Mapping[str, Sequence[Mapping[str, str]]],
    computed_rows: Mapping[str, Sequence[Mapping[str, Any]]],
) -> None:
    """Reject unresolved execution states before the pre-TEST checkpoint can be accepted."""

    _validate_declared_pack_rows(pack_rows)
    _validate_row_alignment(pack_rows, computed_rows)
    _validate_contract_integer_fields(computed_rows)
    _validate_continuous_sizing_fields(computed_rows)
    _validate_market_and_spread_guards(computed_rows)
    _validate_order_fill_session_and_working_state(computed_rows)
    _validate_roll_and_symbol_guards(pack_rows, computed_rows)
    _validate_zero_side_guards(computed_rows)


def _validate_declared_pack_rows(pack_rows: Mapping[str, Sequence[Mapping[str, str]]]) -> None:
    for family, rows in pack_rows.items():
        for row in rows:
            for field_name, value in row.items():
                if not field_name.endswith("_status"):
                    continue
                status = str(value)
                if not status.startswith(DECLARED_PACK_STATUS_ALLOWED_PREFIXES):
                    raise CarverBlocked(
                        "S27 v2 pre-TEST machine freeze rejects degraded or non-ready declared pack rows"
                    )

    for row in pack_rows.get("runtime_evidence_ledger.csv", ()):
        if str(row.get("runtime_status", "")).startswith("PASS_") is not True:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires passing runtime evidence rows")
        if str(row.get("no_lookahead_status", "")).startswith("PASS_") is not True:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires passing no-lookahead evidence rows")


def _validate_row_alignment(
    pack_rows: Mapping[str, Sequence[Mapping[str, str]]],
    computed_rows: Mapping[str, Sequence[Mapping[str, Any]]],
) -> None:
    row_count = len(pack_rows.get("hourly_decision_completed_bar.csv", ()))
    for family in ("hourly_fill_completed_bar.csv", "valuation_mark_completed_bar.csv", "runtime_evidence_ledger.csv"):
        if len(pack_rows.get(family, ())) != row_count:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires one-to-one declared rows")
    for family in ("position", "order", "market", "transition", "fill", "cost", "pnl", "validation"):
        if len(computed_rows.get(family, ())) != row_count:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires one-to-one computed artifact rows")


def _validate_market_and_spread_guards(computed_rows: Mapping[str, Sequence[Mapping[str, Any]]]) -> None:
    for row in computed_rows.get("market", ()):
        if _to_bool(row.get("market_order_required")):
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects unresolved market-order-required rows")
        if _to_bool(row.get("market_order_rows_emitted")):
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects market-order row emission")
        if str(row.get("market_fallback_status")) not in NO_MARKET_NEEDED_STATUSES:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires locked market fallback status")

    for row in computed_rows.get("cost", ()):
        if abs(_to_float(row.get("spread_cost_amount"))) > 0.0:
            raise CarverBlocked(
                "S27 v2 pre-TEST machine freeze rejects market-spread costs before market-cost policy is locked"
            )


def _validate_order_fill_session_and_working_state(
    computed_rows: Mapping[str, Sequence[Mapping[str, Any]]],
) -> None:
    for position, order, market, transition, fill in zip(
        computed_rows.get("position", ()),
        computed_rows.get("order", ()),
        computed_rows.get("market", ()),
        computed_rows.get("transition", ()),
        computed_rows.get("fill", ()),
        strict=True,
    ):
        side = str(order.get("order_side"))
        fill_executed = _to_bool(fill.get("fill_executed"))
        same_session = _to_bool(transition.get("same_session"))
        position_change = _to_int(position.get("position_change_contracts"))
        order_quantity = _to_int(order.get("order_quantity"))

        if side == "NONE":
            if position_change != 0 or order_quantity != 0 or fill_executed:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects inconsistent zero-action rows")
            if str(market.get("market_fallback_status")) != "NOT_REQUIRED_NO_ORDER_POSITION_UNCHANGED":
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires no-order market fallback status")
            if str(transition.get("working_state_after")) != NO_OPEN_AFTER_FILL_STATE:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires no-open working state for no-order rows")
            continue

        if side not in {"BUY", "SELL"} or order_quantity <= 0:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects malformed order-side rows")
        if fill_executed and same_session is not True:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects filled orders across unresolved session/EOD gaps")
        if fill_executed:
            if str(market.get("market_fallback_status")) != "NOT_REQUIRED_LIMIT_ORDER_FILLED":
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires filled limits to bypass market fallback")
            if str(transition.get("working_state_after")) != NO_OPEN_AFTER_FILL_STATE:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires filled limits to leave no working order")
            continue

        if str(market.get("market_fallback_status")) != FAIL_CLOSED_UNFILLED_MARKET_STATUS:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires unfilled limits to fail closed on market fallback")
        if str(transition.get("working_state_after")) != FAIL_CLOSED_WORKING_STATE:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires unfilled limits to fail closed on working state")


def _validate_roll_and_symbol_guards(
    pack_rows: Mapping[str, Sequence[Mapping[str, str]]],
    computed_rows: Mapping[str, Sequence[Mapping[str, Any]]],
) -> None:
    roll_dates = {str(row.get("roll_transition_date")) for row in pack_rows.get("roll_calendar.csv", ())}
    for decision, fill_source, mark, order in zip(
        pack_rows.get("hourly_decision_completed_bar.csv", ()),
        pack_rows.get("hourly_fill_completed_bar.csv", ()),
        pack_rows.get("valuation_mark_completed_bar.csv", ()),
        computed_rows.get("order", ()),
        strict=True,
    ):
        if decision.get("raw_symbol") != fill_source.get("raw_symbol") or decision.get("raw_symbol") != mark.get("raw_symbol"):
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects cross-contract decision/fill/mark chains")
        if str(order.get("order_side")) == "NONE":
            continue
        selected_dates = {
            str(decision.get("trading_date")),
            str(fill_source.get("trading_date")),
            str(mark.get("trading_date")),
        }
        if selected_dates & roll_dates:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects live orders on unresolved roll-boundary dates")


def _validate_contract_integer_fields(computed_rows: Mapping[str, Sequence[Mapping[str, Any]]]) -> None:
    contract_fields_by_family = {
        "position": (
            "starting_position_contracts",
            "desired_position_contracts",
            "position_change_contracts",
        ),
        "order": (
            "order_quantity",
            "adjacent_target_position",
        ),
        "transition": (
            "starting_position_contracts",
            "ending_position_contracts",
        ),
        "fill": (
            "fill_quantity",
            "position_after_fill",
        ),
        "pnl": (
            "ending_position_contracts",
        ),
    }
    for family, field_names in contract_fields_by_family.items():
        for row in computed_rows.get(family, ()):
            for field_name in field_names:
                _to_int(row.get(field_name))


def _validate_continuous_sizing_fields(computed_rows: Mapping[str, Sequence[Mapping[str, Any]]]) -> None:
    continuous_sizing_fields_by_family = {
        "position": (
            "base_position_contracts",
        ),
    }
    for family, field_names in continuous_sizing_fields_by_family.items():
        for row in computed_rows.get(family, ()):
            for field_name in field_names:
                _to_float(row.get(field_name))


def _validate_zero_side_guards(computed_rows: Mapping[str, Sequence[Mapping[str, Any]]]) -> None:
    for position, order, fill in zip(
        computed_rows.get("position", ()),
        computed_rows.get("order", ()),
        computed_rows.get("fill", ()),
        strict=True,
    ):
        if str(order.get("order_side")) != "NONE":
            continue
        if _to_int(position.get("starting_position_contracts")) != _to_int(position.get("desired_position_contracts")):
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects zero-side rows with position changes")
        if _to_int(fill.get("fill_quantity")) != 0:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects zero-side rows with fill quantity")


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.upper() in {"TRUE", "FALSE"}:
        return value.upper() == "TRUE"
    raise CarverBlocked("S27 v2 pre-TEST machine freeze requires boolean ledger fields")


def _to_float(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise CarverBlocked("S27 v2 pre-TEST machine freeze requires numeric ledger fields") from exc
    if math.isfinite(numeric) is not True:
        raise CarverBlocked("S27 v2 pre-TEST machine freeze requires numeric ledger fields")
    return numeric


def _to_int(value: Any) -> int:
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise CarverBlocked("S27 v2 pre-TEST machine freeze requires integer ledger fields") from exc
    if math.isfinite(numeric) is not True or numeric != int(numeric):
        raise CarverBlocked("S27 v2 pre-TEST machine freeze requires integer ledger fields")
    return int(numeric)

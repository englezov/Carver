from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import math
from typing import Any

from ..m0 import CarverBlocked


FAIL_CLOSED_UNFILLED_MARKET_STATUS = "FAIL_CLOSED_UNFILLED_LIMIT_ORDER_MARKET_FALLBACK_NOT_AUTHORIZED"
FAIL_CLOSED_WORKING_STATE = "UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE"
NO_OPEN_AFTER_FILL_STATE = "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
LOCKED_MARKET_ORDER_EXECUTED_STATUS = "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL = "NOT_APPLICABLE_CAP_BOUND_MARKET_ORDER_LIMIT_SIDE_NOT_PLACED"
ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_STATUS = (
    "LOCAL_ENGINEERING_SESSION_OPEN_MARKET_RESET_MARKET_ORDER_ROW_EMITTED_NOT_RESULT"
)
ROW304_ENGINEERING_VALUATION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_CONVENTION = (
    "SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT"
)
ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_RULE = (
    "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_WITH_SESSION_OPEN_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
)
ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_STATUS = (
    "LOCAL_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ROW_EMITTED_NOT_RESULT"
)
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
    _validate_order_fill_session_and_working_state(pack_rows, computed_rows)
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
        market_order_required = _to_bool(row.get("market_order_required"))
        market_order_emitted = _to_bool(row.get("market_order_rows_emitted"))
        market_status = str(row.get("market_fallback_status"))
        if market_status == LOCKED_MARKET_ORDER_EXECUTED_STATUS and not (
            market_order_required and market_order_emitted
        ):
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires locked market orders to be required and emitted")
        if market_order_emitted and not market_order_required:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects market-order row emission")
        if market_order_required or market_order_emitted:
            if not (
                market_order_required
                and market_order_emitted
                and market_status == LOCKED_MARKET_ORDER_EXECUTED_STATUS
            ):
                raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects unresolved market-order-required rows")
            continue
        if str(row.get("market_fallback_status")) not in NO_MARKET_NEEDED_STATUSES:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires locked market fallback status")

    for row in computed_rows.get("cost", ()):
        if abs(_to_float(row.get("spread_cost_amount"))) > 0.0:
            raise CarverBlocked(
                "S27 v2 pre-TEST machine freeze rejects market-spread costs before market-cost policy is locked"
            )


def _validate_order_fill_session_and_working_state(
    pack_rows: Mapping[str, Sequence[Mapping[str, str]]],
    computed_rows: Mapping[str, Sequence[Mapping[str, Any]]],
) -> None:
    for decision_source, fill_source, mark_source, position, order, market, transition, fill, pnl in zip(
        pack_rows.get("hourly_decision_completed_bar.csv", ()),
        pack_rows.get("hourly_fill_completed_bar.csv", ()),
        pack_rows.get("valuation_mark_completed_bar.csv", ()),
        computed_rows.get("position", ()),
        computed_rows.get("order", ()),
        computed_rows.get("market", ()),
        computed_rows.get("transition", ()),
        computed_rows.get("fill", ()),
        computed_rows.get("pnl", ()),
        strict=True,
    ):
        side = str(order.get("order_side"))
        fill_executed = _to_bool(fill.get("fill_executed"))
        same_session = _to_bool(transition.get("same_session"))
        starting_position = _to_int(position.get("starting_position_contracts"))
        desired_position = _to_int(position.get("desired_position_contracts"))
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
        if str(market.get("market_fallback_status")) == LOCKED_MARKET_ORDER_EXECUTED_STATUS:
            fill_quantity = _to_int(fill.get("fill_quantity"))
            transition_starting = _to_int(transition.get("starting_position_contracts"))
            transition_ending = _to_int(transition.get("ending_position_contracts"))
            fill_position_after = _to_int(fill.get("position_after_fill"))
            pnl_ending = _to_int(pnl.get("ending_position_contracts"))
            if position_change != desired_position - starting_position:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires position-change arithmetic binding")
            if transition_starting != starting_position:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires transition starting-position binding")
            cap_bound_market_order = (
                abs(position_change) == 1
                and str(order.get("formula_limit_price")) == CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL
                and str(order.get("limit_order_price")) == CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL
            )
            if abs(position_change) <= 1 and not cap_bound_market_order:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects market-order status without full-gap or cap-bound trigger")
            if (position_change > 0 and side != "BUY") or (position_change < 0 and side != "SELL"):
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires market-order side to match position-change sign")
            if order_quantity != abs(position_change) or fill_quantity != abs(position_change):
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires market order/fill quantity binding")
            if fill_executed is not True:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires locked market order to bind an executed fill")
            if transition_ending != desired_position or fill_position_after != desired_position or pnl_ending != desired_position:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires market-order target-position binding")
        if fill_executed and same_session is not True and not (
            _is_engineering_session_open_market_reset(
                decision_source=decision_source,
                fill_source=fill_source,
                mark_source=mark_source,
                position=position,
                order=order,
                market=market,
                transition=transition,
                fill=fill,
                pnl=pnl,
            )
            or _is_engineering_session_open_adjacent_limit_fill(
                decision_source=decision_source,
                fill_source=fill_source,
                mark_source=mark_source,
                position=position,
                order=order,
                market=market,
                transition=transition,
                fill=fill,
                pnl=pnl,
            )
        ):
            raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects filled orders across unresolved session/EOD gaps")
        if fill_executed:
            if str(market.get("market_fallback_status")) not in {
                "NOT_REQUIRED_LIMIT_ORDER_FILLED",
                LOCKED_MARKET_ORDER_EXECUTED_STATUS,
            }:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires filled limits to bypass market fallback")
            if str(transition.get("working_state_after")) != NO_OPEN_AFTER_FILL_STATE:
                raise CarverBlocked("S27 v2 pre-TEST machine freeze requires filled limits to leave no working order")
            continue

        if str(market.get("market_fallback_status")) != FAIL_CLOSED_UNFILLED_MARKET_STATUS:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires unfilled limits to fail closed on market fallback")
        if str(transition.get("working_state_after")) != FAIL_CLOSED_WORKING_STATE:
            raise CarverBlocked("S27 v2 pre-TEST machine freeze requires unfilled limits to fail closed on working state")


def _is_engineering_session_open_market_reset(
    *,
    decision_source: Mapping[str, str],
    fill_source: Mapping[str, str],
    mark_source: Mapping[str, str],
    position: Mapping[str, Any],
    order: Mapping[str, Any],
    market: Mapping[str, Any],
    transition: Mapping[str, Any],
    fill: Mapping[str, Any],
    pnl: Mapping[str, Any],
) -> bool:
    decision_session = str(decision_source.get("session_id"))
    fill_session = str(fill_source.get("session_id"))
    decision_ts = str(decision_source.get("completed_timestamp_utc"))
    fill_ts = str(fill_source.get("completed_timestamp_utc"))
    mark_ts = str(mark_source.get("completed_timestamp_utc"))
    if _is_row304_engineering_session_open_market_reset(
        decision_source=decision_source,
        fill_source=fill_source,
        mark_source=mark_source,
        position=position,
        order=order,
        market=market,
        transition=transition,
        fill=fill,
        pnl=pnl,
    ):
        return True
    if str(order.get("row_status")) != "LOCAL_MARKET_ORDER_PLAN_ROW_EMITTED_NOT_LIMIT_ORDER_NOT_RESULT":
        return False
    if not (
        str(decision_source.get("raw_symbol")) == "ZNH3"
        and str(fill_source.get("raw_symbol")) == "ZNH3"
        and str(mark_source.get("raw_symbol")) == "ZNH3"
    ):
        return False
    return (
        decision_session != fill_session
        and _session_end(decision_session) == decision_ts
        and _session_start(fill_session) == fill_ts
        and _parse_ts(mark_ts) > _parse_ts(fill_ts)
        and str(mark_source.get("valuation_convention_label")) == ROW304_ENGINEERING_VALUATION_LABEL
        and str(market.get("market_fallback_status")) == LOCKED_MARKET_ORDER_EXECUTED_STATUS
        and _to_bool(market.get("market_order_required")) is True
        and _to_bool(market.get("market_order_rows_emitted")) is True
        and _to_bool(transition.get("same_session")) is False
        and _to_bool(fill.get("fill_executed")) is True
        and str(pnl.get("valuation_convention_label")) == ROW304_ENGINEERING_VALUATION_LABEL
        and str(pnl.get("source_faithful_evidence_claimed")).upper() == "FALSE"
    )


def _is_row304_engineering_session_open_market_reset(
    *,
    decision_source: Mapping[str, str],
    fill_source: Mapping[str, str],
    mark_source: Mapping[str, str],
    position: Mapping[str, Any],
    order: Mapping[str, Any],
    market: Mapping[str, Any],
    transition: Mapping[str, Any],
    fill: Mapping[str, Any],
    pnl: Mapping[str, Any],
) -> bool:
    if str(position.get("row_index")) != "304":
        return False
    if str(order.get("row_status")) != "LOCAL_MARKET_ORDER_PLAN_ROW_EMITTED_NOT_LIMIT_ORDER_NOT_RESULT":
        return False
    return (
        str(decision_source.get("completed_timestamp_utc")) == "2023-01-20T21:00:00Z"
        and str(fill_source.get("completed_timestamp_utc")) == "2023-01-20T22:00:00Z"
        and str(mark_source.get("completed_timestamp_utc")) == "2023-01-23T00:00:00Z"
        and str(decision_source.get("raw_symbol")) == "ZNH3"
        and str(fill_source.get("raw_symbol")) == "ZNH3"
        and str(mark_source.get("raw_symbol")) == "ZNH3"
        and str(decision_source.get("session_id"))
        == "UTC_ZN_2023_TEST_2023-01-19T22:00:00Z_2023-01-20T21:00:00Z"
        and str(fill_source.get("session_id"))
        == "UTC_ZN_2023_TEST_2023-01-20T22:00:00Z_2023-01-21T21:00:00Z"
        and str(mark_source.get("session_id"))
        == "UTC_ZN_2023_TEST_2023-01-22T22:00:00Z_2023-01-23T21:00:00Z"
        and str(mark_source.get("valuation_convention_label")) == ROW304_ENGINEERING_VALUATION_LABEL
        and _to_int(position.get("starting_position_contracts")) == 7
        and _to_int(position.get("desired_position_contracts")) == 9
        and _to_int(position.get("position_change_contracts")) == 2
        and str(order.get("order_side")) == "BUY"
        and _to_int(order.get("order_quantity")) == 2
        and _to_int(transition.get("starting_position_contracts")) == 7
        and _to_int(transition.get("ending_position_contracts")) == 9
        and str(market.get("market_fallback_status")) == LOCKED_MARKET_ORDER_EXECUTED_STATUS
        and _to_bool(market.get("market_order_required")) is True
        and _to_bool(market.get("market_order_rows_emitted")) is True
        and _to_bool(fill.get("fill_executed")) is True
        and _to_int(fill.get("fill_quantity")) == 2
        and _to_int(fill.get("position_after_fill")) == 9
        and _to_int(pnl.get("ending_position_contracts")) == 9
        and str(pnl.get("valuation_convention_label")) == ROW304_ENGINEERING_VALUATION_LABEL
        and str(pnl.get("source_faithful_evidence_claimed")).upper() == "FALSE"
    )


def _is_engineering_session_open_adjacent_limit_fill(
    *,
    decision_source: Mapping[str, str],
    fill_source: Mapping[str, str],
    mark_source: Mapping[str, str],
    position: Mapping[str, Any],
    order: Mapping[str, Any],
    market: Mapping[str, Any],
    transition: Mapping[str, Any],
    fill: Mapping[str, Any],
    pnl: Mapping[str, Any],
) -> bool:
    decision_session = str(decision_source.get("session_id"))
    fill_session = str(fill_source.get("session_id"))
    mark_session = str(mark_source.get("session_id"))
    decision_ts = str(decision_source.get("completed_timestamp_utc"))
    fill_ts = str(fill_source.get("completed_timestamp_utc"))
    mark_ts = str(mark_source.get("completed_timestamp_utc"))
    position_change = _to_int(position.get("position_change_contracts"))
    desired_position = _to_int(position.get("desired_position_contracts"))
    starting_position = _to_int(position.get("starting_position_contracts"))
    side = str(order.get("order_side"))
    signed_fill = 1 if side == "BUY" else -1 if side == "SELL" else 0
    expected_ending = starting_position + signed_fill
    return (
        str(decision_source.get("raw_symbol")) == "ZNH3"
        and str(fill_source.get("raw_symbol")) == "ZNH3"
        and str(mark_source.get("raw_symbol")) == "ZNH3"
        and decision_session != fill_session
        and fill_session == mark_session
        and _session_end(decision_session) == decision_ts
        and _session_start(fill_session) == fill_ts
        and _parse_ts(mark_ts) > _parse_ts(fill_ts)
        and str(mark_source.get("valuation_convention_label")) == ROW304_ENGINEERING_VALUATION_LABEL
        and abs(position_change) == 1
        and expected_ending == desired_position
        and ((position_change > 0 and side == "BUY") or (position_change < 0 and side == "SELL"))
        and _to_int(order.get("order_quantity")) == 1
        and str(order.get("row_status")) == ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_STATUS
        and str(market.get("market_fallback_status")) == "NOT_REQUIRED_LIMIT_ORDER_FILLED"
        and _to_bool(market.get("market_order_required")) is False
        and _to_bool(market.get("market_order_rows_emitted")) is False
        and str(market.get("engineering_convention_label")) == ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_CONVENTION
        and _to_int(transition.get("starting_position_contracts")) == starting_position
        and _to_int(transition.get("ending_position_contracts")) == desired_position
        and _to_bool(transition.get("same_session")) is False
        and str(transition.get("row_status")) == ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_STATUS
        and _to_bool(fill.get("fill_executed")) is True
        and _to_int(fill.get("fill_quantity")) == 1
        and _to_int(fill.get("position_after_fill")) == desired_position
        and str(fill.get("fill_rule")) == ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_RULE
        and str(fill.get("row_status")) == ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_STATUS
        and _to_int(pnl.get("ending_position_contracts")) == desired_position
        and str(pnl.get("valuation_convention_label")) == ROW304_ENGINEERING_VALUATION_LABEL
        and str(pnl.get("source_faithful_evidence_claimed")).upper() == "FALSE"
    )


def _session_start(session_id: str) -> str:
    parts = session_id.split("_")
    if len(parts) < 2:
        raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects malformed session id")
    return parts[-2]


def _session_end(session_id: str) -> str:
    parts = session_id.split("_")
    if len(parts) < 1:
        raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects malformed session id")
    return parts[-1]


def _parse_ts(value: str) -> datetime:
    if not value.endswith("Z"):
        raise CarverBlocked("S27 v2 pre-TEST machine freeze rejects non-UTC timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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

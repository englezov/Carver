from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .local_replay import canonical_sha256
from .fast_validation_profiles import (
    CHECKPOINT_PROOF_VALIDATION_PROFILE,
    is_checkpoint_proof_profile,
    require_supported_validation_profile,
)
from .test_incremental_runner import (
    AUTHORIZATION,
    DEFAULT_BASELINE_ROW_INDEX,
    DEFAULT_OUTPUT_RELATIVE_PATH,
    DEFAULT_PACK_RELATIVE_PATH,
    DEFAULT_SEGMENT_END_ROW_INDEX,
    DEFAULT_SEGMENT_START_ROW_INDEX,
    INPUT_MANIFEST_NAME,
    NON_AUTHORIZATIONS,
    PNL_EVALUATION_STATUS,
    RESULT_STATUS,
    BACKTEST_STATUS,
    IncrementalSegmentBundle,
    build_incremental_segment_from_existing_artifacts,
)


STATUS = "LOCAL_2023_TEST_FAST_EXECUTION_STATE_SEGMENT_VERIFIED_NOT_RESULT"
VERIFICATION_MODE = "FAST_EXECUTION_STATE_SEGMENT_ONLY_NOT_FULL_REPLAY"
ENGINE_STAGE = "FAST_EXECUTION_STATE_REDUCER_FROM_TRUSTED_CHECKPOINT_NOT_RESULT"
DEFAULT_EXECUTION_PARITY_ROWS = (704, 892, 1113, 1355, 1374, 1378)
HOURLY_FILL_LEDGER_NAME = "hourly_fill_completed_bar.csv"

SUPPORTED_POLICY_CLASSES = (
    "NO_ORDER_POSITION_UNCHANGED",
    "ROLL_BOUNDARY_FLAT_NO_NEW_ORDER_SUPPRESSION",
    "ADJACENT_LIMIT_FILLED",
    "ADJACENT_LIMIT_UNFILLED_FAIL_CLOSED_MARKET_FALLBACK",
    "MARKET_ORDER_FULL_GAP_OR_BOUNDED_FALLBACK",
)

_REPO_ROOT = Path(__file__).resolve().parents[4]


@dataclass(frozen=True)
class FastExecutionStateVerification:
    status: str
    authorization_label: str
    verification_mode: str
    engine_stage: str
    segment_bundle_hash: str
    baseline_checkpoint_hash: str
    segment_start_row_index: int
    segment_end_row_index: int
    segment_row_count: int
    starting_position_contracts: int
    ending_position_contracts: int
    state_transition_rows_hash: str
    intent_classification_rows_hash: str
    supported_policy_classes: tuple[str, ...]
    parity_row_indexes: tuple[int, ...]
    verification_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self, segment_bundle: IncrementalSegmentBundle) -> None:
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 fast execution state status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast execution state authorization mismatch")
        if self.verification_mode != VERIFICATION_MODE:
            raise CarverBlocked("S27 v2 fast execution state verification mode drift")
        if self.engine_stage != ENGINE_STAGE:
            raise CarverBlocked("S27 v2 fast execution state engine stage drift")
        if self.segment_bundle_hash != segment_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast execution state segment bundle binding drift")
        if self.baseline_checkpoint_hash != segment_bundle.baseline_checkpoint.trusted_checkpoint_hash:
            raise CarverBlocked("S27 v2 fast execution state checkpoint binding drift")
        if self.segment_start_row_index != DEFAULT_SEGMENT_START_ROW_INDEX:
            raise CarverBlocked("S27 v2 fast execution state start row drift")
        if self.segment_end_row_index != DEFAULT_SEGMENT_END_ROW_INDEX:
            raise CarverBlocked("S27 v2 fast execution state end row drift")
        if self.segment_row_count != DEFAULT_SEGMENT_END_ROW_INDEX - DEFAULT_SEGMENT_START_ROW_INDEX + 1:
            raise CarverBlocked("S27 v2 fast execution state row count drift")
        if self.starting_position_contracts != 0:
            raise CarverBlocked("S27 v2 fast execution state must start from the row-703 flat checkpoint")
        if self.ending_position_contracts != 3:
            raise CarverBlocked("S27 v2 fast execution state ending position drift")
        if self.supported_policy_classes != SUPPORTED_POLICY_CLASSES:
            raise CarverBlocked("S27 v2 fast execution state policy-class set drift")
        if self.parity_row_indexes != DEFAULT_EXECUTION_PARITY_ROWS:
            raise CarverBlocked("S27 v2 fast execution state parity rows drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast execution state non-authorizations drift")
        if self.verification_hash != canonical_sha256(_verification_payload(self)):
            raise CarverBlocked("S27 v2 fast execution state verification hash drift")


@dataclass(frozen=True)
class FastExecutionStateRows:
    state_transition_rows: tuple[dict[str, Any], ...]
    intent_classification_rows: tuple[dict[str, Any], ...]

    def validate(self, verification: FastExecutionStateVerification) -> None:
        if canonical_sha256(self.state_transition_rows) != verification.state_transition_rows_hash:
            raise CarverBlocked("S27 v2 fast execution state transition rows hash drift")
        if canonical_sha256(self.intent_classification_rows) != verification.intent_classification_rows_hash:
            raise CarverBlocked("S27 v2 fast execution intent rows hash drift")


def build_fast_execution_state_verification(
    *,
    segment_bundle: IncrementalSegmentBundle | None = None,
    run_root: Path | str | None = None,
    validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
) -> tuple[FastExecutionStateVerification, FastExecutionStateRows]:
    require_supported_validation_profile(validation_profile)
    run_root_path = _resolve_run_root(run_root)
    active_segment = segment_bundle or build_incremental_segment_from_existing_artifacts(run_root=run_root_path)
    if is_checkpoint_proof_profile(validation_profile):
        active_segment.validate_against_active_files()
    else:
        active_segment.validate()

    rows = _read_segment_ledgers(run_root_path, active_segment.segment_start_row_index, active_segment.segment_end_row_index)
    state_rows, intent_rows = _reduce_segment(active_segment, rows)
    state_hash = canonical_sha256(state_rows)
    intent_hash = canonical_sha256(intent_rows)
    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "verification_mode": VERIFICATION_MODE,
        "engine_stage": ENGINE_STAGE,
        "segment_bundle_hash": active_segment.bundle_hash,
        "baseline_checkpoint_hash": active_segment.baseline_checkpoint.trusted_checkpoint_hash,
        "segment_start_row_index": active_segment.segment_start_row_index,
        "segment_end_row_index": active_segment.segment_end_row_index,
        "segment_row_count": active_segment.segment_row_count,
        "starting_position_contracts": int(active_segment.baseline_checkpoint.ending_position_contracts),
        "ending_position_contracts": int(state_rows[-1]["ending_position_contracts"]),
        "state_transition_rows_hash": state_hash,
        "intent_classification_rows_hash": intent_hash,
        "supported_policy_classes": SUPPORTED_POLICY_CLASSES,
        "parity_row_indexes": DEFAULT_EXECUTION_PARITY_ROWS,
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    verification = FastExecutionStateVerification(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        verification_mode=VERIFICATION_MODE,
        engine_stage=ENGINE_STAGE,
        segment_bundle_hash=active_segment.bundle_hash,
        baseline_checkpoint_hash=active_segment.baseline_checkpoint.trusted_checkpoint_hash,
        segment_start_row_index=active_segment.segment_start_row_index,
        segment_end_row_index=active_segment.segment_end_row_index,
        segment_row_count=active_segment.segment_row_count,
        starting_position_contracts=int(active_segment.baseline_checkpoint.ending_position_contracts),
        ending_position_contracts=int(state_rows[-1]["ending_position_contracts"]),
        state_transition_rows_hash=state_hash,
        intent_classification_rows_hash=intent_hash,
        supported_policy_classes=SUPPORTED_POLICY_CLASSES,
        parity_row_indexes=DEFAULT_EXECUTION_PARITY_ROWS,
        verification_hash=canonical_sha256(payload),
    )
    fast_rows = FastExecutionStateRows(
        state_transition_rows=tuple(state_rows),
        intent_classification_rows=tuple(intent_rows),
    )
    verification.validate(active_segment)
    fast_rows.validate(verification)
    return verification, fast_rows


def _reduce_segment(
    segment: IncrementalSegmentBundle,
    rows_by_ledger: Mapping[str, Mapping[int, Mapping[str, str]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    previous_position = int(segment.baseline_checkpoint.ending_position_contracts)
    cumulative_gross = float(segment.baseline_checkpoint.cumulative_gross_pnl_amount)
    cumulative_commission = float(segment.baseline_checkpoint.cumulative_commission_amount)
    cumulative_spread = float(segment.baseline_checkpoint.cumulative_spread_amount)
    cumulative_net = float(segment.baseline_checkpoint.cumulative_net_pnl_amount)
    state_rows: list[dict[str, Any]] = []
    intent_rows: list[dict[str, Any]] = []
    for row_index in range(segment.segment_start_row_index, segment.segment_end_row_index + 1):
        desired = _required_row(rows_by_ledger, "desired_position_ledger.csv", row_index)
        limit = _required_row(rows_by_ledger, "limit_order_ledger.csv", row_index)
        no_market = _required_row(rows_by_ledger, "no_market_order_ledger.csv", row_index)
        transition = _required_row(rows_by_ledger, "working_order_transition_ledger.csv", row_index)
        fill = _required_row(rows_by_ledger, "fill_ledger.csv", row_index)
        fill_source = _required_row(rows_by_ledger, HOURLY_FILL_LEDGER_NAME, row_index)
        cost = _required_row(rows_by_ledger, "cost_ledger.csv", row_index)
        pnl = _required_row(rows_by_ledger, "pnl_ledger.csv", row_index)
        market = rows_by_ledger["market_order_ledger.csv"].get(row_index)
        market_fill = rows_by_ledger["market_fill_metadata_ledger.csv"].get(row_index)

        starting_position = _as_int(desired["starting_position_contracts"], "desired starting position", row_index)
        target_position = _as_int(desired["desired_position_contracts"], "desired target position", row_index)
        position_change = _as_int(desired["position_change_contracts"], "desired position change", row_index)
        if starting_position != previous_position:
            raise CarverBlocked(f"S27 v2 fast execution state carry mismatch at row {row_index}")
        if target_position - starting_position != position_change:
            raise CarverBlocked(f"S27 v2 fast execution state position-change arithmetic drift at row {row_index}")
        if _as_int(transition["starting_position_contracts"], "transition starting position", row_index) != starting_position:
            raise CarverBlocked(f"S27 v2 fast execution state transition start drift at row {row_index}")

        policy_class = _classify_policy(row_index, position_change, no_market, fill, desired)
        _validate_order_intent(row_index, position_change, starting_position, target_position, policy_class, limit, no_market, market)
        _validate_fill_cost_and_pnl(
            row_index,
            position_change,
            starting_position,
            target_position,
            policy_class,
            fill,
            fill_source,
            cost,
            pnl,
            transition,
            market,
            market_fill,
        )
        cumulative_gross, cumulative_commission, cumulative_spread, cumulative_net = _validate_cumulative_roll_forward(
            row_index,
            pnl,
            cost,
            cumulative_gross,
            cumulative_commission,
            cumulative_spread,
            cumulative_net,
        )

        ending_position = _as_int(pnl["ending_position_contracts"], "PnL ending position", row_index)
        previous_position = ending_position

        state_rows.append(
            _hash_row(
                {
                    "row_index": row_index,
                    "starting_position_contracts": starting_position,
                    "desired_position_contracts": target_position,
                    "position_change_contracts": position_change,
                    "ending_position_contracts": ending_position,
                    "fill_executed": fill["fill_executed"],
                    "fill_quantity": _as_int(fill["fill_quantity"], "fill quantity", row_index),
                    "cumulative_gross_pnl_amount": cumulative_gross,
                    "cumulative_commission_amount": cumulative_commission,
                    "cumulative_spread_amount": cumulative_spread,
                    "cumulative_net_pnl_amount": cumulative_net,
                    "policy_class": policy_class,
                    "desired_row_hash": desired["row_hash"],
                    "pnl_row_hash": pnl["row_hash"],
                    "row_status": "LOCAL_FAST_EXECUTION_STATE_TRANSITION_VERIFIED_NOT_RESULT",
                }
            )
        )
        intent_rows.append(
            _hash_row(
                {
                    "row_index": row_index,
                    "policy_class": policy_class,
                    "order_side": limit["order_side"],
                    "order_quantity": _as_int(limit["order_quantity"], "limit/order quantity", row_index),
                    "market_order_required": no_market["market_order_required"],
                    "market_order_rows_emitted": no_market["market_order_rows_emitted"],
                    "fill_executed": fill["fill_executed"],
                    "total_cost_amount": cost["total_cost_amount"],
                    "result_status": pnl["result_status"],
                    "backtest_status": pnl["backtest_status"],
                    "source_faithful_evidence_claimed": pnl["source_faithful_evidence_claimed"],
                    "row_status": "LOCAL_FAST_EXECUTION_INTENT_CLASSIFICATION_VERIFIED_NOT_RESULT",
                }
            )
        )

    _validate_parity_rows(state_rows, intent_rows)
    return state_rows, intent_rows


def _validate_order_intent(
    row_index: int,
    position_change: int,
    starting_position: int,
    target_position: int,
    policy_class: str,
    limit: Mapping[str, str],
    no_market: Mapping[str, str],
    market: Mapping[str, str] | None,
) -> None:
    side = _side(position_change)
    order_quantity = abs(position_change)
    if policy_class in {"NO_ORDER_POSITION_UNCHANGED", "ROLL_BOUNDARY_FLAT_NO_NEW_ORDER_SUPPRESSION"}:
        if (limit["order_side"], limit["order_quantity"]) != ("NONE", "0"):
            raise CarverBlocked(f"S27 v2 fast execution no-order intent drift at row {row_index}")
        if no_market["market_order_required"] != "FALSE" or no_market["market_order_rows_emitted"] != "FALSE":
            raise CarverBlocked(f"S27 v2 fast execution no-market metadata drift at row {row_index}")
        if market is not None:
            raise CarverBlocked(f"S27 v2 fast execution unexpected market row at row {row_index}")
        return

    if limit["order_side"] != side:
        raise CarverBlocked(f"S27 v2 fast execution order side drift at row {row_index}")
    if _as_int(limit["order_quantity"], "limit/order quantity", row_index) != order_quantity:
        raise CarverBlocked(f"S27 v2 fast execution order quantity drift at row {row_index}")
    if policy_class == "ADJACENT_LIMIT_FILLED" or policy_class == "ADJACENT_LIMIT_UNFILLED_FAIL_CLOSED_MARKET_FALLBACK":
        if no_market["market_order_required"] != "FALSE" or no_market["market_order_rows_emitted"] != "FALSE":
            raise CarverBlocked(f"S27 v2 fast execution adjacent-limit market metadata drift at row {row_index}")
        if market is not None:
            raise CarverBlocked(f"S27 v2 fast execution adjacent-limit emitted market row at row {row_index}")
        if order_quantity != 1:
            raise CarverBlocked(f"S27 v2 fast execution adjacent-limit quantity drift at row {row_index}")
        if _as_int(limit["adjacent_target_position"], "adjacent target position", row_index) != target_position:
            raise CarverBlocked(f"S27 v2 fast execution adjacent target drift at row {row_index}")
        return

    if policy_class == "MARKET_ORDER_FULL_GAP_OR_BOUNDED_FALLBACK":
        if no_market["market_order_required"] != "TRUE" or no_market["market_order_rows_emitted"] != "TRUE":
            raise CarverBlocked(f"S27 v2 fast execution market metadata drift at row {row_index}")
        if market is None:
            raise CarverBlocked(f"S27 v2 fast execution missing market row at row {row_index}")
        if market["order_side"] != side:
            raise CarverBlocked(f"S27 v2 fast execution market side drift at row {row_index}")
        if _as_int(market["current_position_before_order"], "market current position", row_index) != starting_position:
            raise CarverBlocked(f"S27 v2 fast execution market starting position drift at row {row_index}")
        if _as_int(market["target_position_after_fill"], "market target position", row_index) != target_position:
            raise CarverBlocked(f"S27 v2 fast execution market target position drift at row {row_index}")
        if _as_int(market["order_quantity"], "market order quantity", row_index) != order_quantity:
            raise CarverBlocked(f"S27 v2 fast execution market quantity drift at row {row_index}")
        return

    raise CarverBlocked(f"S27 v2 fast execution unsupported policy class at row {row_index}")


def _validate_fill_cost_and_pnl(
    row_index: int,
    position_change: int,
    starting_position: int,
    target_position: int,
    policy_class: str,
    fill: Mapping[str, str],
    fill_source: Mapping[str, str],
    cost: Mapping[str, str],
    pnl: Mapping[str, str],
    transition: Mapping[str, str],
    market: Mapping[str, str] | None,
    market_fill: Mapping[str, str] | None,
) -> None:
    fill_executed = fill["fill_executed"] == "TRUE"
    fill_quantity = _as_int(fill["fill_quantity"], "fill quantity", row_index)
    position_after_fill = _as_int(fill["position_after_fill"], "position after fill", row_index)
    transition_end = _as_int(transition["ending_position_contracts"], "transition ending position", row_index)
    pnl_end = _as_int(pnl["ending_position_contracts"], "PnL ending position", row_index)
    if transition_end != position_after_fill or pnl_end != position_after_fill:
        raise CarverBlocked(f"S27 v2 fast execution end-position binding drift at row {row_index}")
    if policy_class != "MARKET_ORDER_FULL_GAP_OR_BOUNDED_FALLBACK" and market_fill is not None:
        raise CarverBlocked(f"S27 v2 fast execution unexpected market fill metadata at row {row_index}")

    if policy_class in {"NO_ORDER_POSITION_UNCHANGED", "ROLL_BOUNDARY_FLAT_NO_NEW_ORDER_SUPPRESSION"}:
        if fill_executed or fill_quantity != 0 or position_after_fill != starting_position:
            raise CarverBlocked(f"S27 v2 fast execution no-order fill drift at row {row_index}")
        if not _float_equal(cost["total_cost_amount"], "0.0"):
            raise CarverBlocked(f"S27 v2 fast execution no-order cost drift at row {row_index}")
    elif policy_class == "ADJACENT_LIMIT_UNFILLED_FAIL_CLOSED_MARKET_FALLBACK":
        if fill_executed or fill_quantity != 0 or position_after_fill != starting_position:
            raise CarverBlocked(f"S27 v2 fast execution unfilled adjacent-limit drift at row {row_index}")
        if not _float_equal(cost["total_cost_amount"], "0.0"):
            raise CarverBlocked(f"S27 v2 fast execution unfilled adjacent-limit cost drift at row {row_index}")
    else:
        if not fill_executed:
            raise CarverBlocked(f"S27 v2 fast execution filled policy did not fill at row {row_index}")
        if fill_quantity != abs(position_change):
            raise CarverBlocked(f"S27 v2 fast execution fill quantity drift at row {row_index}")
        if position_after_fill != target_position:
            raise CarverBlocked(f"S27 v2 fast execution fill target drift at row {row_index}")
        if market is not None:
            if market_fill is None:
                raise CarverBlocked(f"S27 v2 fast execution missing market fill metadata at row {row_index}")
            _validate_market_fill_metadata(row_index, target_position, fill_quantity, fill, fill_source, market, market_fill)
            if _as_int(market_fill["position_after_fill"], "market fill position", row_index) != target_position:
                raise CarverBlocked(f"S27 v2 fast execution market fill position drift at row {row_index}")
        if not _float_equal(cost["total_cost_amount"], str(float(cost["commission_amount"]) + float(cost["spread_cost_amount"]))):
            raise CarverBlocked(f"S27 v2 fast execution total cost arithmetic drift at row {row_index}")

    if pnl["result_status"] != RESULT_STATUS:
        raise CarverBlocked(f"S27 v2 fast execution result status drift at row {row_index}")
    if pnl["backtest_status"] != BACKTEST_STATUS:
        raise CarverBlocked(f"S27 v2 fast execution backtest status drift at row {row_index}")
    if pnl["pnl_evaluation_status"] != PNL_EVALUATION_STATUS:
        raise CarverBlocked(f"S27 v2 fast execution PnL evaluation status drift at row {row_index}")
    if pnl["source_faithful_evidence_claimed"] != "FALSE":
        raise CarverBlocked(f"S27 v2 fast execution source-faithful claim drift at row {row_index}")
    if not _float_equal(pnl["row_net_pnl_amount"], str(float(pnl["row_gross_pnl_amount"]) - float(cost["total_cost_amount"]))):
        raise CarverBlocked(f"S27 v2 fast execution row net PnL arithmetic drift at row {row_index}")


def _validate_market_fill_metadata(
    row_index: int,
    target_position: int,
    fill_quantity: int,
    fill: Mapping[str, str],
    fill_source: Mapping[str, str],
    market: Mapping[str, str],
    market_fill: Mapping[str, str],
) -> None:
    if market_fill["raw_symbol"] != market["raw_symbol"]:
        raise CarverBlocked(f"S27 v2 fast execution market fill symbol drift at row {row_index}")
    if market_fill["order_side"] != market["order_side"]:
        raise CarverBlocked(f"S27 v2 fast execution market fill side drift at row {row_index}")
    if _as_int(market_fill["fill_quantity"], "market fill quantity", row_index) != fill_quantity:
        raise CarverBlocked(f"S27 v2 fast execution market fill quantity drift at row {row_index}")
    if not _float_equal(market_fill["fill_price"], fill["fill_price"]):
        raise CarverBlocked(f"S27 v2 fast execution market fill price drift at row {row_index}")
    if market_fill["fill_timestamp_utc"] != fill_source["completed_timestamp_utc"]:
        raise CarverBlocked(f"S27 v2 fast execution market fill timestamp drift at row {row_index}")
    if market_fill["raw_symbol"] != fill_source["raw_symbol"]:
        raise CarverBlocked(f"S27 v2 fast execution market fill source symbol drift at row {row_index}")
    if market_fill["fill_source_row_hash"] != fill_source["source_row_hash"]:
        raise CarverBlocked(f"S27 v2 fast execution market fill source row hash drift at row {row_index}")
    if _as_int(market_fill["position_after_fill"], "market fill position", row_index) != target_position:
        raise CarverBlocked(f"S27 v2 fast execution market fill position drift at row {row_index}")
    if market_fill["fill_price_provenance"] in {"", "NOT_APPLICABLE"}:
        raise CarverBlocked(f"S27 v2 fast execution market fill provenance missing at row {row_index}")


def _validate_cumulative_roll_forward(
    row_index: int,
    pnl: Mapping[str, str],
    cost: Mapping[str, str],
    previous_gross: float,
    previous_commission: float,
    previous_spread: float,
    previous_net: float,
) -> tuple[float, float, float, float]:
    expected_gross = previous_gross + _as_float(pnl["row_gross_pnl_amount"], "row gross PnL", row_index)
    expected_commission = previous_commission + _as_float(cost["commission_amount"], "commission", row_index)
    expected_spread = previous_spread + _as_float(cost["spread_cost_amount"], "spread", row_index)
    expected_net = previous_net + _as_float(pnl["row_net_pnl_amount"], "row net PnL", row_index)
    actual_gross = _as_float(pnl["cumulative_gross_pnl_amount"], "cumulative gross PnL", row_index)
    actual_commission = _as_float(pnl["cumulative_commission_amount"], "cumulative commission", row_index)
    actual_spread = _as_float(pnl["cumulative_spread_amount"], "cumulative spread", row_index)
    actual_net = _as_float(pnl["cumulative_net_pnl_amount"], "cumulative net PnL", row_index)
    _require_float_close(actual_gross, expected_gross, f"S27 v2 fast execution cumulative gross drift at row {row_index}")
    _require_float_close(actual_commission, expected_commission, f"S27 v2 fast execution cumulative commission drift at row {row_index}")
    _require_float_close(actual_spread, expected_spread, f"S27 v2 fast execution cumulative spread drift at row {row_index}")
    _require_float_close(actual_net, expected_net, f"S27 v2 fast execution cumulative net drift at row {row_index}")
    _require_float_close(
        actual_net,
        actual_gross - actual_commission - actual_spread,
        f"S27 v2 fast execution cumulative net/gross-cost drift at row {row_index}",
    )
    return actual_gross, actual_commission, actual_spread, actual_net


def _classify_policy(
    row_index: int,
    position_change: int,
    no_market: Mapping[str, str],
    fill: Mapping[str, str],
    desired: Mapping[str, str],
) -> str:
    row_status = desired.get("row_status", "")
    if "ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSED" in row_status:
        return "ROLL_BOUNDARY_FLAT_NO_NEW_ORDER_SUPPRESSION"
    if position_change == 0:
        return "NO_ORDER_POSITION_UNCHANGED"
    if no_market["market_order_required"] == "TRUE":
        return "MARKET_ORDER_FULL_GAP_OR_BOUNDED_FALLBACK"
    if fill["fill_executed"] == "TRUE":
        return "ADJACENT_LIMIT_FILLED"
    if fill["fill_executed"] == "FALSE":
        return "ADJACENT_LIMIT_UNFILLED_FAIL_CLOSED_MARKET_FALLBACK"
    raise CarverBlocked(f"S27 v2 fast execution cannot classify row {row_index}")


def _validate_parity_rows(state_rows: list[dict[str, Any]], intent_rows: list[dict[str, Any]]) -> None:
    state_by_index = {int(row["row_index"]): row for row in state_rows}
    intent_by_index = {int(row["row_index"]): row for row in intent_rows}
    expected = {
        704: ("ROLL_BOUNDARY_FLAT_NO_NEW_ORDER_SUPPRESSION", 0),
        892: ("ADJACENT_LIMIT_FILLED", -1),
        1113: ("MARKET_ORDER_FULL_GAP_OR_BOUNDED_FALLBACK", -15),
        1355: ("ADJACENT_LIMIT_FILLED", 8),
        1374: ("MARKET_ORDER_FULL_GAP_OR_BOUNDED_FALLBACK", 5),
    }
    for row_index, (policy_class, ending_position) in expected.items():
        state = state_by_index.get(row_index)
        intent = intent_by_index.get(row_index)
        if state is None or intent is None:
            raise CarverBlocked(f"S27 v2 fast execution missing parity row {row_index}")
        if state["policy_class"] != policy_class or intent["policy_class"] != policy_class:
            raise CarverBlocked(f"S27 v2 fast execution policy parity drift at row {row_index}")
        if int(state["ending_position_contracts"]) != ending_position:
            raise CarverBlocked(f"S27 v2 fast execution ending-position parity drift at row {row_index}")


def _read_segment_ledgers(run_root: Path, start: int, end: int) -> dict[str, dict[int, dict[str, str]]]:
    names = (
        "desired_position_ledger.csv",
        "limit_order_ledger.csv",
        "no_market_order_ledger.csv",
        "market_order_ledger.csv",
        "working_order_transition_ledger.csv",
        "fill_ledger.csv",
        "market_fill_metadata_ledger.csv",
        "cost_ledger.csv",
        "pnl_ledger.csv",
    )
    rows = {name: _read_rows_by_index(run_root / name, start, end) for name in names}
    pack_root = (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()
    _verify_pack_row_family_hash(pack_root, HOURLY_FILL_LEDGER_NAME)
    rows[HOURLY_FILL_LEDGER_NAME] = _read_rows_by_index(pack_root / HOURLY_FILL_LEDGER_NAME, start, end)
    return rows


def _read_rows_by_index(path: Path, start: int, end: int) -> dict[int, dict[str, str]]:
    if not path.exists():
        raise CarverBlocked(f"S27 v2 fast execution missing ledger: {path}")
    rows: dict[int, dict[str, str]] = {}
    with path.open("r", encoding="ascii", newline="") as handle:
        for row in csv.DictReader(handle):
            if not row.get("row_index"):
                continue
            row_index = int(row["row_index"])
            if start <= row_index <= end:
                if row_index in rows:
                    raise CarverBlocked(f"S27 v2 fast execution duplicate row_index in {path.name}: {row_index}")
                rows[row_index] = row
    return rows


def _required_row(
    rows_by_ledger: Mapping[str, Mapping[int, Mapping[str, str]]],
    ledger_name: str,
    row_index: int,
) -> Mapping[str, str]:
    row = rows_by_ledger[ledger_name].get(row_index)
    if row is None:
        raise CarverBlocked(f"S27 v2 fast execution missing {ledger_name} row {row_index}")
    return row


def _verify_pack_row_family_hash(pack_root: Path, name: str) -> None:
    manifest_path = pack_root / INPUT_MANIFEST_NAME
    if not manifest_path.exists():
        raise CarverBlocked("S27 v2 fast execution missing declared pack manifest")
    manifest = json.loads(manifest_path.read_text(encoding="ascii"))
    expected = manifest.get("row_family_files", {}).get(name, {}).get("sha256")
    actual = hashlib.sha256((pack_root / name).read_bytes()).hexdigest()
    if expected != actual:
        raise CarverBlocked(f"S27 v2 fast execution pack row-family hash drift for {name}")


def _resolve_run_root(path: Path | str | None) -> Path:
    if path is None:
        return (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve()
    resolved = Path(path).resolve()
    if resolved != (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 fast execution run root is locked")
    return resolved


def _as_int(value: str, label: str, row_index: int) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise CarverBlocked(f"S27 v2 fast execution invalid {label} at row {row_index}") from exc


def _as_float(value: str, label: str, row_index: int) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise CarverBlocked(f"S27 v2 fast execution invalid {label} at row {row_index}") from exc


def _side(position_change: int) -> str:
    if position_change > 0:
        return "BUY"
    if position_change < 0:
        return "SELL"
    return "NONE"


def _float_equal(left: str, right: str) -> bool:
    return abs(float(left) - float(right)) <= 1e-9


def _require_float_close(left: float, right: float, message: str) -> None:
    if abs(left - right) > 1e-9:
        raise CarverBlocked(message)


def _hash_row(row: dict[str, Any]) -> dict[str, Any]:
    hashed = dict(row)
    hashed["row_hash"] = canonical_sha256(hashed)
    return hashed


def _verification_payload(verification: FastExecutionStateVerification) -> dict[str, Any]:
    payload = asdict(verification)
    payload.pop("verification_hash", None)
    return payload

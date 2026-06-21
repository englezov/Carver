from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .positive_action_executable import (
    EXPECTED_RAW_SYMBOL,
    EXPECTED_SELECTED_DECISION,
    EXPECTED_SELECTED_FILL,
    POSITIVE_ACTION_PACK_RELATIVE_PATH,
)
from .positive_action_order_plan_executable import (
    ORDER_QUANTITY,
    ORDER_SIDE,
    TARGET_POSITION_AFTER_FILL,
    PositiveActionOrderPlanExecutableBundle,
    _read_pack_rows,
    _row_hashes_by_file,
    build_positive_action_limit_order_plan,
)
from .validation import require_finite_number, require_hash, require_integer, require_positive_number, require_text


S27_V2_POSITIVE_ACTION_FILL_AUTHORIZATION = "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_FILL_DECISION_AND_FILL_LEDGER"
S27_V2_POSITIVE_ACTION_FILL_STATUS = "S27_V2_POSITIVE_ACTION_LIMIT_FILL_LOCAL_DEV_RECON_NOT_COST_NOT_PNL_NOT_RESULT"

FILL_DECISION_ROW_STATUS = "LOCAL_POSITIVE_ACTION_LIMIT_FILL_DECISION_METADATA_EMITTED_NOT_COST_NOT_RESULT"
LIMIT_FILL_ROW_STATUS = "LOCAL_POSITIVE_ACTION_LIMIT_FILL_LEDGER_ROW_EMITTED_NOT_COST_NOT_RESULT"

FILL_DECISION_REASON_CODE = "S27_POSITIVE_ACTION_SELL_LIMIT_FILLED_BY_NEXT_COMPLETED_CLOSE"
LIMIT_FILL_REASON_CODE = "S27_POSITIVE_ACTION_ACTUAL_LIMIT_FILL_AT_SUBMITTED_LIMIT_PRICE"

FILL_CONDITION_LABEL = "SELL_LIMIT_FILLS_WHEN_NEXT_COMPLETED_CLOSE_AT_OR_ABOVE_LIMIT"
ONE_HOUR_LAG_PROOF_LABEL = "PASS_NEXT_COMPLETED_HOURLY_FILL_ROW_ONE_HOUR_AFTER_DECISION"
FILL_PRICE_PROVENANCE = "LIMIT_ORDER_PRICE_FROM_FILLED_ORDER"
INTRABAR_AUTHORITY_REJECTION_LABEL = "REJECT_INTRABAR_HIGH_LOW_FILL_AUTHORITY_CLOSE_ONLY"
LIMIT_FILL_COST_STATUS = "FAIL_CLOSED_COST_LEDGER_NOT_EMITTED_LIMIT_FILL_COMMISSION_ONLY_POLICY_UNRESOLVED"
MARKET_FILL_STATUS = "NOT_APPLICABLE_NO_MARKET_ORDER_IN_ACTIVE_ORDER_PLAN"

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()

FILL_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_MARKET_ORDER_FILL_EMISSION",
    "NO_COST_EMISSION",
    "NO_PNL_RESULT_EMISSION",
    "NO_RESULT_INTERPRETATION",
    "NO_PNL_EVALUATION",
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)


@dataclass(frozen=True)
class PositiveActionFillDecisionRow:
    ledger_label: str
    row_status: str
    reason_code: str
    order_plan_bundle_hash: str
    limit_order_hash: str
    transition_plan_row_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    order_side: str
    order_quantity: int
    executable_tick_limit_price: float
    next_completed_close_price: float
    hourly_fill_row_hash: str
    one_hour_lag_proof_label: str
    one_hour_lag_proof_hash: str
    fill_condition_label: str
    fill_condition_hash: str
    intrabar_authority_rejection_label: str
    fill_executed: bool
    fill_price: float
    fill_quantity: int
    fill_price_provenance: str
    market_fill_status: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action fill-decision row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_against_order_plan(self, order_plan_bundle: PositiveActionOrderPlanExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_FILL_DECISION_LEDGER":
            raise CarverBlocked("S27 v2 positive-action fill-decision ledger label is not locked")
        if self.row_status != FILL_DECISION_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action fill-decision row status is not locked")
        if self.reason_code != FILL_DECISION_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action fill-decision reason code is not locked")
        for name, hash_value in (
            ("order-plan bundle", self.order_plan_bundle_hash),
            ("limit order", self.limit_order_hash),
            ("transition plan row", self.transition_plan_row_hash),
            ("hourly fill row", self.hourly_fill_row_hash),
            ("one-hour lag proof", self.one_hour_lag_proof_hash),
            ("fill condition", self.fill_condition_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action fill-decision {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("decision timestamp", self.selected_decision_timestamp_utc),
            ("fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("order side", self.order_side),
            ("one-hour lag proof", self.one_hour_lag_proof_label),
            ("fill condition", self.fill_condition_label),
            ("intrabar rejection", self.intrabar_authority_rejection_label),
            ("fill price provenance", self.fill_price_provenance),
            ("market fill status", self.market_fill_status),
        ):
            require_text(f"S27 v2 positive-action fill-decision {name}", value)
        require_integer("S27 v2 positive-action fill-decision order quantity", self.order_quantity)
        require_integer("S27 v2 positive-action fill-decision fill quantity", self.fill_quantity)
        require_positive_number("S27 v2 positive-action fill-decision limit price", self.executable_tick_limit_price)
        require_positive_number("S27 v2 positive-action fill-decision next close", self.next_completed_close_price)
        require_positive_number("S27 v2 positive-action fill-decision fill price", self.fill_price)
        self._validate_locked_identity(order_plan_bundle)
        self._validate_fill_condition(order_plan_bundle)
        if self.row_hash != canonical_sha256(_fill_decision_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action fill-decision row hash must be content-bound")

    def _validate_locked_identity(self, order_plan_bundle: PositiveActionOrderPlanExecutableBundle) -> None:
        limit_row = order_plan_bundle.limit_order_row
        transition = order_plan_bundle.transition_plan_row
        if self.order_plan_bundle_hash != order_plan_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action fill-decision must bind active order-plan bundle")
        if self.limit_order_hash != limit_row.limit_order_hash:
            raise CarverBlocked("S27 v2 positive-action fill-decision must bind active limit order")
        if self.transition_plan_row_hash != transition.row_hash:
            raise CarverBlocked("S27 v2 positive-action fill-decision must bind active transition plan")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action fill-decision is locked to the positive-action pack")
        if self.selected_decision_timestamp_utc != EXPECTED_SELECTED_DECISION:
            raise CarverBlocked("S27 v2 positive-action fill-decision decision timestamp is not locked")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action fill-decision fill timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 positive-action fill-decision raw symbol is not locked")
        if self.order_side != ORDER_SIDE or self.order_quantity != ORDER_QUANTITY:
            raise CarverBlocked("S27 v2 positive-action fill-decision must bind SELL 1 order")
        if self.executable_tick_limit_price != limit_row.executable_tick_limit_price:
            raise CarverBlocked("S27 v2 positive-action fill-decision must bind submitted executable limit")
        if self.hourly_fill_row_hash != transition.hourly_fill_row_hash:
            raise CarverBlocked("S27 v2 positive-action fill-decision must bind transition fill-candidate row")

    def _validate_fill_condition(self, order_plan_bundle: PositiveActionOrderPlanExecutableBundle) -> None:
        if self.one_hour_lag_proof_label != ONE_HOUR_LAG_PROOF_LABEL:
            raise CarverBlocked("S27 v2 positive-action fill-decision one-hour proof label is not locked")
        if self.one_hour_lag_proof_hash != _policy_hash(
            "one_hour_lag_proof",
            ONE_HOUR_LAG_PROOF_LABEL,
            EXPECTED_SELECTED_DECISION,
            EXPECTED_SELECTED_FILL,
            self.hourly_fill_row_hash,
        ):
            raise CarverBlocked("S27 v2 positive-action fill-decision one-hour proof hash must bind fill row")
        if self.fill_condition_label != FILL_CONDITION_LABEL:
            raise CarverBlocked("S27 v2 positive-action fill condition label is not locked")
        if self.fill_condition_hash != _policy_hash(
            "close_only_sell_limit_fill_condition",
            FILL_CONDITION_LABEL,
            self.limit_order_hash,
            self.executable_tick_limit_price,
            self.next_completed_close_price,
            self.hourly_fill_row_hash,
        ):
            raise CarverBlocked("S27 v2 positive-action fill condition hash must bind close-only crossing")
        if self.intrabar_authority_rejection_label != INTRABAR_AUTHORITY_REJECTION_LABEL:
            raise CarverBlocked("S27 v2 positive-action fill-decision must reject intrabar high/low authority")
        if self.next_completed_close_price < self.executable_tick_limit_price:
            raise CarverBlocked("S27 v2 positive-action sell limit is not crossed by next completed close")
        if self.fill_executed is not True:
            raise CarverBlocked("S27 v2 positive-action fill-decision must emit the crossed limit fill")
        if self.fill_price != order_plan_bundle.limit_order_row.executable_tick_limit_price:
            raise CarverBlocked("S27 v2 positive-action limit fill price must be submitted limit price")
        if self.fill_quantity != ORDER_QUANTITY:
            raise CarverBlocked("S27 v2 positive-action fill quantity must bind order quantity")
        if self.fill_price_provenance != FILL_PRICE_PROVENANCE:
            raise CarverBlocked("S27 v2 positive-action fill price provenance is not locked")
        if self.market_fill_status != MARKET_FILL_STATUS:
            raise CarverBlocked("S27 v2 positive-action market fill status must remain not applicable")


@dataclass(frozen=True)
class PositiveActionLimitFillLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    order_plan_bundle_hash: str
    fill_decision_row_hash: str
    limit_order_hash: str
    input_pack_path: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    filled_order_side: str
    filled_order_quantity: int
    fill_price: float
    fill_price_provenance: str
    position_before_fill: int
    position_after_fill: int
    working_order_state_before_fill_hash: str
    working_order_state_after_fill_hash: str
    cost_ledger_status: str
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    fill_ledger_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action limit-fill row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_against_decision(
        self,
        order_plan_bundle: PositiveActionOrderPlanExecutableBundle,
        decision_row: PositiveActionFillDecisionRow,
    ) -> None:
        if self.ledger_label != "POSITIVE_ACTION_LIMIT_FILL_LEDGER":
            raise CarverBlocked("S27 v2 positive-action limit-fill ledger label is not locked")
        if self.row_status != LIMIT_FILL_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action limit-fill row status is not locked")
        if self.reason_code != LIMIT_FILL_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action limit-fill reason code is not locked")
        for name, hash_value in (
            ("order-plan bundle", self.order_plan_bundle_hash),
            ("fill decision row", self.fill_decision_row_hash),
            ("limit order", self.limit_order_hash),
            ("working state before", self.working_order_state_before_fill_hash),
            ("working state after", self.working_order_state_after_fill_hash),
            ("fill ledger", self.fill_ledger_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action limit-fill {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("filled order side", self.filled_order_side),
            ("fill price provenance", self.fill_price_provenance),
            ("cost ledger status", self.cost_ledger_status),
        ):
            require_text(f"S27 v2 positive-action limit-fill {name}", value)
        require_integer("S27 v2 positive-action limit-fill quantity", self.filled_order_quantity)
        require_integer("S27 v2 positive-action limit-fill position before", self.position_before_fill)
        require_integer("S27 v2 positive-action limit-fill position after", self.position_after_fill)
        require_finite_number("S27 v2 positive-action limit-fill price", self.fill_price)
        if self.order_plan_bundle_hash != order_plan_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action limit-fill must bind active order-plan bundle")
        if self.fill_decision_row_hash != decision_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action limit-fill must bind active fill decision row")
        if self.limit_order_hash != order_plan_bundle.limit_order_row.limit_order_hash:
            raise CarverBlocked("S27 v2 positive-action limit-fill must bind active limit order")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action limit-fill is locked to the positive-action pack")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action limit-fill timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 positive-action limit-fill raw symbol is not locked")
        if self.filled_order_side != ORDER_SIDE or self.filled_order_quantity != ORDER_QUANTITY:
            raise CarverBlocked("S27 v2 positive-action limit-fill must bind SELL 1 order")
        if self.fill_price != decision_row.fill_price:
            raise CarverBlocked("S27 v2 positive-action limit-fill price must bind decision")
        if self.fill_price_provenance != FILL_PRICE_PROVENANCE:
            raise CarverBlocked("S27 v2 positive-action limit-fill provenance is not locked")
        if self.position_before_fill != order_plan_bundle.limit_order_row.current_position_before_order:
            raise CarverBlocked("S27 v2 positive-action limit-fill position-before must bind order-plan current position")
        if self.position_after_fill != TARGET_POSITION_AFTER_FILL:
            raise CarverBlocked("S27 v2 positive-action limit-fill must transition to target position")
        if self.working_order_state_before_fill_hash != order_plan_bundle.transition_plan_row.working_order_state_after_planned_hash:
            raise CarverBlocked("S27 v2 positive-action limit-fill must bind pending working-order state")
        if self.working_order_state_after_fill_hash != _policy_hash(
            "working_state_after_limit_fill",
            "LIMIT_ORDER_FILLED_AND_CLEARED",
            self.limit_order_hash,
            self.selected_fill_timestamp_utc,
            self.fill_price,
            self.filled_order_quantity,
        ):
            raise CarverBlocked("S27 v2 positive-action limit-fill working-state-after hash must bind fill")
        if self.cost_ledger_status != LIMIT_FILL_COST_STATUS:
            raise CarverBlocked("S27 v2 positive-action limit-fill cost status must remain fail-closed")
        if any(
            flag is not False
            for flag in (
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action limit-fill cannot emit cost/PnL/result/evidence")
        if self.fill_ledger_hash != _limit_fill_hash(self):
            raise CarverBlocked("S27 v2 positive-action limit-fill hash must bind fill fields")
        if self.row_hash != canonical_sha256(_limit_fill_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action limit-fill row hash must be content-bound")


@dataclass(frozen=True)
class PositiveActionFillExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    order_plan_bundle: PositiveActionOrderPlanExecutableBundle
    fill_decision_row: PositiveActionFillDecisionRow
    limit_fill_row: PositiveActionLimitFillLedgerRow
    fill_decision_metadata_rows_emitted: bool
    actual_limit_fill_rows_emitted: bool
    actual_market_fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = FILL_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_FILL_STATUS:
            raise CarverBlocked("S27 v2 positive-action fill bundle status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_FILL_AUTHORIZATION:
            raise CarverBlocked("S27 v2 positive-action fill authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 positive-action fill must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 positive-action fill lane must remain source-native futures")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action fill is locked to the declared positive-action pack")
        active_order_plan = build_positive_action_limit_order_plan(_POSITIVE_ACTION_PACK_PATH)
        self.order_plan_bundle.validate()
        if self.order_plan_bundle != active_order_plan:
            raise CarverBlocked("S27 v2 positive-action fill must bind active order-plan bundle")
        self.fill_decision_row._validate_against_order_plan(active_order_plan)
        self.limit_fill_row._validate_against_decision(active_order_plan, self.fill_decision_row)
        active_decision, active_fill = _build_active_fill_rows(_POSITIVE_ACTION_PACK_PATH, active_order_plan)
        if self.fill_decision_row != active_decision:
            raise CarverBlocked("S27 v2 positive-action fill-decision row must match active local evidence")
        if self.limit_fill_row != active_fill:
            raise CarverBlocked("S27 v2 positive-action limit-fill row must match active local evidence")
        if any(
            flag is not True
            for flag in (
                self.fill_decision_metadata_rows_emitted,
                self.actual_limit_fill_rows_emitted,
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action fill must emit only authorized fill metadata/surface")
        if any(
            flag is not False
            for flag in (
                self.actual_market_fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action fill cannot emit market/cost/PnL/result/evidence")
        if self.non_authorizations != FILL_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 positive-action fill must preserve non-authorizations")
        require_hash("S27 v2 positive-action fill bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_fill_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action fill bundle hash must be content-bound")


def build_positive_action_fill_executable(
    input_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
) -> PositiveActionFillExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action fill is locked to the declared positive-action pack")
    order_plan_bundle = build_positive_action_limit_order_plan(pack_path)
    decision_row, fill_row = _build_active_fill_rows(pack_path, order_plan_bundle)
    bundle = PositiveActionFillExecutableBundle(
        status=S27_V2_POSITIVE_ACTION_FILL_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_FILL_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        order_plan_bundle=order_plan_bundle,
        fill_decision_row=decision_row,
        limit_fill_row=fill_row,
        fill_decision_metadata_rows_emitted=True,
        actual_limit_fill_rows_emitted=True,
        actual_market_fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionFillExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_fill_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_fill_rows(
    pack_path: Path,
    order_plan_bundle: PositiveActionOrderPlanExecutableBundle,
) -> tuple[PositiveActionFillDecisionRow, PositiveActionLimitFillLedgerRow]:
    fill_row = _locked_hourly_fill_row(pack_path)
    close_price = _parse_close_price(fill_row)
    hourly_fill_hash = _row_hashes_by_file(_read_pack_rows(pack_path))["hourly_fill_completed_bar.csv"][0]
    transition = order_plan_bundle.transition_plan_row
    limit_row = order_plan_bundle.limit_order_row
    if hourly_fill_hash != transition.hourly_fill_row_hash:
        raise CarverBlocked("S27 v2 positive-action fill must bind transition fill-candidate row")
    decision = PositiveActionFillDecisionRow(
        ledger_label="POSITIVE_ACTION_FILL_DECISION_LEDGER",
        row_status=FILL_DECISION_ROW_STATUS,
        reason_code=FILL_DECISION_REASON_CODE,
        order_plan_bundle_hash=order_plan_bundle.bundle_hash,
        limit_order_hash=limit_row.limit_order_hash,
        transition_plan_row_hash=transition.row_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=EXPECTED_SELECTED_DECISION,
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        order_side=ORDER_SIDE,
        order_quantity=ORDER_QUANTITY,
        executable_tick_limit_price=limit_row.executable_tick_limit_price,
        next_completed_close_price=close_price,
        hourly_fill_row_hash=hourly_fill_hash,
        one_hour_lag_proof_label=ONE_HOUR_LAG_PROOF_LABEL,
        one_hour_lag_proof_hash=_policy_hash(
            "one_hour_lag_proof",
            ONE_HOUR_LAG_PROOF_LABEL,
            EXPECTED_SELECTED_DECISION,
            EXPECTED_SELECTED_FILL,
            hourly_fill_hash,
        ),
        fill_condition_label=FILL_CONDITION_LABEL,
        fill_condition_hash=_policy_hash(
            "close_only_sell_limit_fill_condition",
            FILL_CONDITION_LABEL,
            limit_row.limit_order_hash,
            limit_row.executable_tick_limit_price,
            close_price,
            hourly_fill_hash,
        ),
        intrabar_authority_rejection_label=INTRABAR_AUTHORITY_REJECTION_LABEL,
        fill_executed=True,
        fill_price=limit_row.executable_tick_limit_price,
        fill_quantity=ORDER_QUANTITY,
        fill_price_provenance=FILL_PRICE_PROVENANCE,
        market_fill_status=MARKET_FILL_STATUS,
        row_hash="0" * 64,
    )
    decision = PositiveActionFillDecisionRow(
        **{**decision.__dict__, "row_hash": canonical_sha256(_fill_decision_row_hash_payload(decision))}
    )
    decision._validate_against_order_plan(order_plan_bundle)
    limit_fill = PositiveActionLimitFillLedgerRow(
        ledger_label="POSITIVE_ACTION_LIMIT_FILL_LEDGER",
        row_status=LIMIT_FILL_ROW_STATUS,
        reason_code=LIMIT_FILL_REASON_CODE,
        order_plan_bundle_hash=order_plan_bundle.bundle_hash,
        fill_decision_row_hash=decision.row_hash,
        limit_order_hash=limit_row.limit_order_hash,
        input_pack_path=str(pack_path),
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        filled_order_side=ORDER_SIDE,
        filled_order_quantity=ORDER_QUANTITY,
        fill_price=decision.fill_price,
        fill_price_provenance=FILL_PRICE_PROVENANCE,
        position_before_fill=limit_row.current_position_before_order,
        position_after_fill=TARGET_POSITION_AFTER_FILL,
        working_order_state_before_fill_hash=transition.working_order_state_after_planned_hash,
        working_order_state_after_fill_hash=_policy_hash(
            "working_state_after_limit_fill",
            "LIMIT_ORDER_FILLED_AND_CLEARED",
            limit_row.limit_order_hash,
            EXPECTED_SELECTED_FILL,
            decision.fill_price,
            ORDER_QUANTITY,
        ),
        cost_ledger_status=LIMIT_FILL_COST_STATUS,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        fill_ledger_hash="0" * 64,
        row_hash="0" * 64,
    )
    limit_fill = PositiveActionLimitFillLedgerRow(
        **{**limit_fill.__dict__, "fill_ledger_hash": _limit_fill_hash(limit_fill)}
    )
    limit_fill = PositiveActionLimitFillLedgerRow(
        **{**limit_fill.__dict__, "row_hash": canonical_sha256(_limit_fill_row_hash_payload(limit_fill))}
    )
    limit_fill._validate_against_decision(order_plan_bundle, decision)
    return decision, limit_fill


def _locked_hourly_fill_row(pack_path: Path) -> dict[str, str]:
    rows = _read_pack_rows(pack_path)["hourly_fill_completed_bar.csv"]
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 positive-action fill candidate must have exactly one hourly fill row")
    row = rows[0]
    if row.get("completed_timestamp_utc") != EXPECTED_SELECTED_FILL:
        raise CarverBlocked("S27 v2 positive-action fill candidate timestamp is not locked")
    if row.get("trading_date") != EXPECTED_SELECTED_FILL[:10]:
        raise CarverBlocked("S27 v2 positive-action fill candidate trading date is not locked")
    if row.get("raw_symbol") != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 positive-action fill candidate raw symbol is not locked")
    if row.get("readiness_status") != "READY_COMPLETED_BAR_LOCAL_POSITIVE_ACTION_RECON":
        raise CarverBlocked("S27 v2 positive-action fill candidate readiness status is not locked")
    return row


def _parse_close_price(row: dict[str, str]) -> float:
    try:
        close_price = float(row.get("close_price", "nan"))
    except ValueError as exc:
        raise CarverBlocked("S27 v2 positive-action fill candidate close price must be numeric") from exc
    require_positive_number("S27 v2 positive-action fill candidate close price", close_price)
    return close_price


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_FILL_POLICY", "label": label, "values": values})


def _limit_fill_hash(row: PositiveActionLimitFillLedgerRow) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_POSITIVE_ACTION_LIMIT_FILL",
            "limit_order_hash": row.limit_order_hash,
            "fill_timestamp": row.selected_fill_timestamp_utc,
            "raw_symbol": row.raw_symbol,
            "side": row.filled_order_side,
            "quantity": row.filled_order_quantity,
            "fill_price": row.fill_price,
            "fill_price_provenance": row.fill_price_provenance,
            "position_before_fill": row.position_before_fill,
            "position_after_fill": row.position_after_fill,
            "working_order_state_before_fill_hash": row.working_order_state_before_fill_hash,
            "working_order_state_after_fill_hash": row.working_order_state_after_fill_hash,
        }
    )


def _fill_decision_row_hash_payload(row: PositiveActionFillDecisionRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _limit_fill_row_hash_payload(row: PositiveActionLimitFillLedgerRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _fill_bundle_hash_payload(bundle: PositiveActionFillExecutableBundle) -> dict[str, object]:
    return {
        "actual_limit_fill_rows_emitted": bundle.actual_limit_fill_rows_emitted,
        "actual_market_fill_rows_emitted": bundle.actual_market_fill_rows_emitted,
        "artifact": "S27_V2_POSITIVE_ACTION_FILL_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "bundle_hashes": {
            "fill_decision_row": bundle.fill_decision_row.row_hash,
            "limit_fill_row": bundle.limit_fill_row.row_hash,
            "order_plan_bundle": bundle.order_plan_bundle.bundle_hash,
        },
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "fill_decision_metadata_rows_emitted": bundle.fill_decision_metadata_rows_emitted,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "provenance_metadata_rows_emitted": bundle.provenance_metadata_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "trusted_bundle_metadata_emitted": bundle.trusted_bundle_metadata_emitted,
        "validation_metadata_rows_emitted": bundle.validation_metadata_rows_emitted,
    }

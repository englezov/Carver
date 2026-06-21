from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .desired_position_executable import (
    DesiredPositionExecutableBundle,
    build_desired_position_executable_ledger,
)
from .local_replay import canonical_sha256
from .runtime_evidence_gate import RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH
from .validation import require_hash, require_integer, require_text


S27_V2_ORDER_TRANSITION_AUTHORIZATION = "S27_V2_NON_RESULT_ORDER_TRANSITION_EXECUTABLE_LEDGER"
S27_V2_ORDER_TRANSITION_STATUS = "S27_V2_ORDER_TRANSITION_EXECUTABLE_REMEDIATION_PACK_NON_RESULT"
ORDER_INTENT_LEDGER_ROW_STATUS = "LOCAL_ORDER_INTENT_ZERO_DELTA_NO_ORDER_REQUIRED_NOT_FILL"
ORDER_TRANSITION_LEDGER_ROW_STATUS = "LOCAL_ORDER_TRANSITION_ZERO_DELTA_POSITION_UNCHANGED_NOT_FILL"

ORDER_INTENT_REASON_CODE = "S27_ORDER_INTENT_BOUND_TO_ACTIVE_DESIRED_POSITION_ZERO_DELTA_NOT_EXECUTION"
ORDER_TRANSITION_REASON_CODE = "S27_ORDER_TRANSITION_NO_POSITION_CHANGE_NO_WORKING_ORDER_NO_FILL"

NO_ORDER_KIND = "NO_ORDER"
NO_ORDER_SIDE = "NONE"
NO_POSITION_CHANGE_TRANSITION_KIND = "NO_POSITION_CHANGE_NO_ORDER"

PASS_ACTIVE_DESIRED_POSITION = "PASS_ACTIVE_DESIRED_POSITION_BUNDLE_NOT_ORDER_RESULT"
PASS_INITIAL_FLAT_CURRENT_POSITION = "PASS_FIRST_ROW_FLAT_ZERO_CURRENT_POSITION_CONTEXT"
PASS_ZERO_DELTA_NO_ORDER = "PASS_ZERO_DELTA_NO_ORDER_REQUIRED"
FAIL_CLOSED_UNRESOLVED_NOT_EMITTED = "FAIL_CLOSED_UNRESOLVED_NOT_EMITTED"

ORDER_EVIDENCE_CHECK_LABELS = (
    "ACTIVE_DESIRED_POSITION_AUTHORITY",
    "CURRENT_POSITION_CONTEXT",
    "POSITION_CHANGE_CALCULATION",
    "ADJACENT_LIMIT_ORDER_POLICY",
    "MARKET_FALLBACK_POLICY",
    "TICK_ROUNDING_POLICY",
    "WORKING_ORDER_LIFECYCLE",
)

REQUIRED_STATUS_BY_ORDER_CHECK = {
    "ACTIVE_DESIRED_POSITION_AUTHORITY": PASS_ACTIVE_DESIRED_POSITION,
    "CURRENT_POSITION_CONTEXT": PASS_INITIAL_FLAT_CURRENT_POSITION,
    "POSITION_CHANGE_CALCULATION": PASS_ZERO_DELTA_NO_ORDER,
    "ADJACENT_LIMIT_ORDER_POLICY": FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
    "MARKET_FALLBACK_POLICY": FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
    "TICK_ROUNDING_POLICY": FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
    "WORKING_ORDER_LIFECYCLE": FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
}

ORDER_TRANSITION_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_FILL_EMISSION",
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

_REPO_ROOT = Path(__file__).resolve().parents[4]
_REMEDIATION_PACK_PATH = (_REPO_ROOT / RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH).resolve()


@dataclass(frozen=True)
class OrderTransitionEvidenceCheck:
    label: str
    status: str
    summary: str
    observed_value_hash: str
    check_hash: str

    def validate(self) -> None:
        require_text("S27 v2 order evidence check label", self.label)
        if self.label not in ORDER_EVIDENCE_CHECK_LABELS:
            raise CarverBlocked("S27 v2 order evidence check label is not locked")
        require_text("S27 v2 order evidence check status", self.status)
        if self.status != REQUIRED_STATUS_BY_ORDER_CHECK[self.label]:
            raise CarverBlocked("S27 v2 order evidence check status must match locked gate")
        require_text("S27 v2 order evidence check summary", self.summary)
        require_hash("S27 v2 order evidence observed value hash", self.observed_value_hash)
        require_hash("S27 v2 order evidence check hash", self.check_hash)
        if self.check_hash != _check_hash(self.label, self.status, self.summary, self.observed_value_hash):
            raise CarverBlocked("S27 v2 order evidence check hash must bind content")


@dataclass(frozen=True)
class OrderIntentExecutableLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    desired_position_bundle_hash: str
    desired_position_row_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    raw_symbol: str
    current_position_before_order: int
    desired_rounded_position: int
    position_change_contracts: int
    order_required: bool
    order_kind: str
    order_side: str
    order_quantity: int
    adjacent_limit_order_policy_status: str
    market_fallback_policy_status: str
    tick_rounding_policy_status: str
    working_order_lifecycle_status: str
    evidence_check_bundle_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 order-intent row standalone validation is not authoritative; validate the bundle")

    def _validate_structural_formula(self) -> None:
        if self.ledger_label != "ORDER_INTENT_LEDGER":
            raise CarverBlocked("S27 v2 order-intent ledger label is not locked")
        if self.row_status != ORDER_INTENT_LEDGER_ROW_STATUS:
            raise CarverBlocked("S27 v2 order-intent row status is not locked")
        if self.reason_code != ORDER_INTENT_REASON_CODE:
            raise CarverBlocked("S27 v2 order-intent reason code is not locked")
        for name, hash_value in (
            ("desired position bundle hash", self.desired_position_bundle_hash),
            ("desired position row hash", self.desired_position_row_hash),
            ("evidence check bundle hash", self.evidence_check_bundle_hash),
            ("row hash", self.row_hash),
        ):
            require_hash(f"S27 v2 order-intent {name}", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("order kind", self.order_kind),
            ("order side", self.order_side),
            ("adjacent limit policy status", self.adjacent_limit_order_policy_status),
            ("market fallback policy status", self.market_fallback_policy_status),
            ("tick rounding policy status", self.tick_rounding_policy_status),
            ("working order lifecycle status", self.working_order_lifecycle_status),
        ):
            require_text(f"S27 v2 order-intent {name}", value)
        for name, value in (
            ("current position before order", self.current_position_before_order),
            ("desired rounded position", self.desired_rounded_position),
            ("position change contracts", self.position_change_contracts),
            ("order quantity", self.order_quantity),
        ):
            require_integer(f"S27 v2 order-intent {name}", value)
        if self.position_change_contracts != self.desired_rounded_position - self.current_position_before_order:
            raise CarverBlocked("S27 v2 order-intent position change must bind desired minus current")
        if self.position_change_contracts != 0:
            raise CarverBlocked("S27 v2 order-intent gate only authorizes zero-delta no-order row")
        if self.order_required is not False:
            raise CarverBlocked("S27 v2 order-intent zero-delta row must not require an order")
        if self.order_kind != NO_ORDER_KIND or self.order_side != NO_ORDER_SIDE or self.order_quantity != 0:
            raise CarverBlocked("S27 v2 order-intent zero-delta row must carry no executable order")
        self._validate_fail_closed_execution_policy_statuses()
        if self.row_hash != canonical_sha256(_order_intent_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 order-intent row hash must be content-bound")

    def _validate_fail_closed_execution_policy_statuses(self) -> None:
        if self.adjacent_limit_order_policy_status != FAIL_CLOSED_UNRESOLVED_NOT_EMITTED:
            raise CarverBlocked("S27 v2 adjacent limit policy must remain fail-closed in this gate")
        if self.market_fallback_policy_status != FAIL_CLOSED_UNRESOLVED_NOT_EMITTED:
            raise CarverBlocked("S27 v2 market fallback policy must remain fail-closed in this gate")
        if self.tick_rounding_policy_status != FAIL_CLOSED_UNRESOLVED_NOT_EMITTED:
            raise CarverBlocked("S27 v2 tick rounding policy must remain fail-closed in this gate")
        if self.working_order_lifecycle_status != FAIL_CLOSED_UNRESOLVED_NOT_EMITTED:
            raise CarverBlocked("S27 v2 working-order lifecycle must remain fail-closed in this gate")


@dataclass(frozen=True)
class OrderTransitionExecutableLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    order_intent_row_hash: str
    desired_position_bundle_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    raw_symbol: str
    current_position_before_transition: int
    desired_position_after_transition: int
    ending_position_without_fill: int
    position_change_contracts: int
    transition_required: bool
    transition_kind: str
    working_order_state_before_hash: str
    working_order_state_after_hash: str
    working_order_lifecycle_status: str
    fill_rows_emitted: bool
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 order-transition row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_structural_formula(self) -> None:
        if self.ledger_label != "ORDER_TRANSITION_LEDGER":
            raise CarverBlocked("S27 v2 order-transition ledger label is not locked")
        if self.row_status != ORDER_TRANSITION_LEDGER_ROW_STATUS:
            raise CarverBlocked("S27 v2 order-transition row status is not locked")
        if self.reason_code != ORDER_TRANSITION_REASON_CODE:
            raise CarverBlocked("S27 v2 order-transition reason code is not locked")
        for name, hash_value in (
            ("order intent row hash", self.order_intent_row_hash),
            ("desired position bundle hash", self.desired_position_bundle_hash),
            ("working state before hash", self.working_order_state_before_hash),
            ("working state after hash", self.working_order_state_after_hash),
            ("row hash", self.row_hash),
        ):
            require_hash(f"S27 v2 order-transition {name}", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("transition kind", self.transition_kind),
            ("working-order lifecycle status", self.working_order_lifecycle_status),
        ):
            require_text(f"S27 v2 order-transition {name}", value)
        for name, value in (
            ("current position before transition", self.current_position_before_transition),
            ("desired position after transition", self.desired_position_after_transition),
            ("ending position without fill", self.ending_position_without_fill),
            ("position change contracts", self.position_change_contracts),
        ):
            require_integer(f"S27 v2 order-transition {name}", value)
        if self.position_change_contracts != self.desired_position_after_transition - self.current_position_before_transition:
            raise CarverBlocked("S27 v2 order-transition position change must bind desired minus current")
        if self.position_change_contracts != 0:
            raise CarverBlocked("S27 v2 order-transition gate only authorizes zero-delta no-order transition")
        if self.ending_position_without_fill != self.current_position_before_transition:
            raise CarverBlocked("S27 v2 zero-delta transition must leave position unchanged without fill")
        if self.transition_required is not False:
            raise CarverBlocked("S27 v2 zero-delta order transition must not require transition execution")
        if self.transition_kind != NO_POSITION_CHANGE_TRANSITION_KIND:
            raise CarverBlocked("S27 v2 order-transition kind must be no-position-change")
        if self.working_order_lifecycle_status != FAIL_CLOSED_UNRESOLVED_NOT_EMITTED:
            raise CarverBlocked("S27 v2 order-transition working-order lifecycle must remain fail-closed")
        if self.working_order_state_after_hash != self.working_order_state_before_hash:
            raise CarverBlocked("S27 v2 no-order transition must not mutate working-order state")
        if self.fill_rows_emitted is not False:
            raise CarverBlocked("S27 v2 order-transition gate cannot emit fill rows")
        if self.row_hash != canonical_sha256(_order_transition_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 order-transition row hash must be content-bound")


@dataclass(frozen=True)
class OrderTransitionExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    desired_position_bundle: DesiredPositionExecutableBundle
    evidence_checks: tuple[OrderTransitionEvidenceCheck, ...]
    order_intent_row: OrderIntentExecutableLedgerRow
    order_transition_row: OrderTransitionExecutableLedgerRow
    order_intent_rows_emitted: bool
    order_transition_rows_emitted: bool
    limit_order_rows_emitted: bool
    market_order_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = ORDER_TRANSITION_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_ORDER_TRANSITION_STATUS:
            raise CarverBlocked("S27 v2 order-transition executable status is not locked")
        if self.authorization_label != S27_V2_ORDER_TRANSITION_AUTHORIZATION:
            raise CarverBlocked("S27 v2 order-transition executable authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 order-transition executable must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 order-transition executable must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 order-transition executable is locked to the audited remediation pack")
        self.desired_position_bundle.validate()
        active_desired = build_desired_position_executable_ledger(pack_path)
        if self.desired_position_bundle != active_desired:
            raise CarverBlocked("S27 v2 order-transition executable must bind active desired-position bundle")
        active_checks = _build_active_evidence_checks(active_desired)
        if self.evidence_checks != active_checks:
            raise CarverBlocked("S27 v2 order-transition checks must match active desired-position authority")
        for check in self.evidence_checks:
            check.validate()
        active_intent = _build_active_order_intent_row(pack_path, active_desired, active_checks)
        self.order_intent_row._validate_structural_formula()
        if self.order_intent_row != active_intent:
            raise CarverBlocked("S27 v2 order-intent row must match active desired-position authority")
        active_transition = _build_active_order_transition_row(pack_path, active_desired, active_intent)
        self.order_transition_row._validate_structural_formula()
        if self.order_transition_row != active_transition:
            raise CarverBlocked("S27 v2 order-transition row must match active no-order intent")
        if self.order_intent_rows_emitted is not True or self.order_transition_rows_emitted is not True:
            raise CarverBlocked("S27 v2 order-transition executable must emit order-intent and transition rows")
        if any(
            flag is not False
            for flag in (
                self.limit_order_rows_emitted,
                self.market_order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 order-transition executable cannot emit limit/market/fill/cost/PnL/result/evidence")
        if self.non_authorizations != ORDER_TRANSITION_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 order-transition executable must preserve non-authorizations")
        require_hash("S27 v2 order-transition executable bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_order_transition_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 order-transition executable bundle hash must be content-bound")


def build_order_transition_executable_ledger(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> OrderTransitionExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 order-transition executable is locked to the audited remediation pack")
    desired_bundle = build_desired_position_executable_ledger(pack_path)
    evidence_checks = _build_active_evidence_checks(desired_bundle)
    order_intent = _build_active_order_intent_row(pack_path, desired_bundle, evidence_checks)
    order_transition = _build_active_order_transition_row(pack_path, desired_bundle, order_intent)
    bundle = OrderTransitionExecutableBundle(
        status=S27_V2_ORDER_TRANSITION_STATUS,
        authorization_label=S27_V2_ORDER_TRANSITION_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        desired_position_bundle=desired_bundle,
        evidence_checks=evidence_checks,
        order_intent_row=order_intent,
        order_transition_row=order_transition,
        order_intent_rows_emitted=True,
        order_transition_rows_emitted=True,
        limit_order_rows_emitted=False,
        market_order_rows_emitted=False,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = OrderTransitionExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_order_transition_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_evidence_checks(
    desired_bundle: DesiredPositionExecutableBundle,
) -> tuple[OrderTransitionEvidenceCheck, ...]:
    row = desired_bundle.desired_position_row
    position_change = row.desired_rounded_contracts - row.initial_current_position_contracts
    checks = (
        _check(
            "ACTIVE_DESIRED_POSITION_AUTHORITY",
            PASS_ACTIVE_DESIRED_POSITION,
            "active desired-position bundle rebuilt from audited remediation pack",
            desired_bundle.bundle_hash,
        ),
        _check(
            "CURRENT_POSITION_CONTEXT",
            PASS_INITIAL_FLAT_CURRENT_POSITION,
            "first remediation-pack row uses operator-fixed flat zero current position",
            _value_hash("current_position", row.initial_current_position_contracts),
        ),
        _check(
            "POSITION_CHANGE_CALCULATION",
            PASS_ZERO_DELTA_NO_ORDER,
            "desired rounded position minus current position equals zero; no executable order is required",
            _value_hash("position_change", position_change),
        ),
        _check(
            "ADJACENT_LIMIT_ORDER_POLICY",
            FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
            "adjacent limit-order price ladder remains unresolved and no limit order is emitted",
            _policy_hash("adjacent_limit_order_policy", FAIL_CLOSED_UNRESOLVED_NOT_EMITTED),
        ),
        _check(
            "MARKET_FALLBACK_POLICY",
            FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
            "market-order fallback policy remains unresolved and no market order is emitted",
            _policy_hash("market_fallback_policy", FAIL_CLOSED_UNRESOLVED_NOT_EMITTED),
        ),
        _check(
            "TICK_ROUNDING_POLICY",
            FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
            "tick rounding for executable order prices remains unresolved and no price order is emitted",
            _policy_hash("tick_rounding_policy", FAIL_CLOSED_UNRESOLVED_NOT_EMITTED),
        ),
        _check(
            "WORKING_ORDER_LIFECYCLE",
            FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
            "working-order lifecycle remains unresolved and no working order is opened, filled, canceled, or carried",
            _policy_hash("working_order_lifecycle", FAIL_CLOSED_UNRESOLVED_NOT_EMITTED),
        ),
    )
    if tuple(check.label for check in checks) != ORDER_EVIDENCE_CHECK_LABELS:
        raise CarverBlocked("S27 v2 order-transition evidence checks must match locked tuple")
    for check in checks:
        check.validate()
    return checks


def _build_active_order_intent_row(
    pack_path: Path,
    desired_bundle: DesiredPositionExecutableBundle,
    evidence_checks: tuple[OrderTransitionEvidenceCheck, ...],
) -> OrderIntentExecutableLedgerRow:
    desired_row = desired_bundle.desired_position_row
    current_position = desired_row.initial_current_position_contracts
    desired_position = desired_row.desired_rounded_contracts
    position_change = desired_position - current_position
    if position_change != 0:
        raise CarverBlocked("S27 v2 order-transition gate only authorizes zero-delta no-order intent")
    evidence_bundle_hash = _evidence_check_bundle_hash(evidence_checks)
    row = OrderIntentExecutableLedgerRow(
        ledger_label="ORDER_INTENT_LEDGER",
        row_status=ORDER_INTENT_LEDGER_ROW_STATUS,
        reason_code=ORDER_INTENT_REASON_CODE,
        desired_position_bundle_hash=desired_bundle.bundle_hash,
        desired_position_row_hash=desired_row.row_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=desired_row.selected_decision_timestamp_utc,
        raw_symbol=desired_row.raw_symbol,
        current_position_before_order=current_position,
        desired_rounded_position=desired_position,
        position_change_contracts=position_change,
        order_required=False,
        order_kind=NO_ORDER_KIND,
        order_side=NO_ORDER_SIDE,
        order_quantity=0,
        adjacent_limit_order_policy_status=FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
        market_fallback_policy_status=FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
        tick_rounding_policy_status=FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
        working_order_lifecycle_status=FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
        evidence_check_bundle_hash=evidence_bundle_hash,
        row_hash="0" * 64,
    )
    row = OrderIntentExecutableLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_order_intent_row_hash_payload(row))}
    )
    row._validate_structural_formula()
    return row


def _build_active_order_transition_row(
    pack_path: Path,
    desired_bundle: DesiredPositionExecutableBundle,
    order_intent: OrderIntentExecutableLedgerRow,
) -> OrderTransitionExecutableLedgerRow:
    desired_row = desired_bundle.desired_position_row
    working_state_hash = _policy_hash(
        "working_order_state_context",
        "FIRST_ROW_NO_WORKING_ORDER_OPENED_FAIL_CLOSED_LIFECYCLE",
        desired_row.initial_current_position_contracts,
        order_intent.row_hash,
    )
    row = OrderTransitionExecutableLedgerRow(
        ledger_label="ORDER_TRANSITION_LEDGER",
        row_status=ORDER_TRANSITION_LEDGER_ROW_STATUS,
        reason_code=ORDER_TRANSITION_REASON_CODE,
        order_intent_row_hash=order_intent.row_hash,
        desired_position_bundle_hash=desired_bundle.bundle_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=desired_row.selected_decision_timestamp_utc,
        raw_symbol=desired_row.raw_symbol,
        current_position_before_transition=order_intent.current_position_before_order,
        desired_position_after_transition=order_intent.desired_rounded_position,
        ending_position_without_fill=order_intent.current_position_before_order,
        position_change_contracts=order_intent.position_change_contracts,
        transition_required=False,
        transition_kind=NO_POSITION_CHANGE_TRANSITION_KIND,
        working_order_state_before_hash=working_state_hash,
        working_order_state_after_hash=working_state_hash,
        working_order_lifecycle_status=FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
        fill_rows_emitted=False,
        row_hash="0" * 64,
    )
    row = OrderTransitionExecutableLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_order_transition_row_hash_payload(row))}
    )
    row._validate_structural_formula()
    return row


def _check(label: str, status: str, summary: str, observed_value_hash: str) -> OrderTransitionEvidenceCheck:
    check = OrderTransitionEvidenceCheck(
        label=label,
        status=status,
        summary=summary,
        observed_value_hash=observed_value_hash,
        check_hash="0" * 64,
    )
    check = OrderTransitionEvidenceCheck(
        **{**check.__dict__, "check_hash": _check_hash(label, status, summary, observed_value_hash)}
    )
    check.validate()
    return check


def _check_hash(label: str, status: str, summary: str, observed_value_hash: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_ORDER_TRANSITION_EVIDENCE_CHECK",
            "label": label,
            "observed_value_hash": observed_value_hash,
            "status": status,
            "summary": summary,
        }
    )


def _evidence_check_bundle_hash(checks: tuple[OrderTransitionEvidenceCheck, ...]) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_ORDER_TRANSITION_EVIDENCE_CHECK_BUNDLE",
            "checks": tuple((check.label, check.status, check.check_hash) for check in checks),
        }
    )


def _value_hash(label: str, value: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_ORDER_TRANSITION_VALUE", "label": label, "value": value})


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_ORDER_TRANSITION_POLICY", "label": label, "values": values})


def _order_intent_row_hash_payload(row: OrderIntentExecutableLedgerRow) -> dict[str, object]:
    return {
        "adjacent_limit_order_policy_status": row.adjacent_limit_order_policy_status,
        "current_position_before_order": row.current_position_before_order,
        "desired_position_bundle_hash": row.desired_position_bundle_hash,
        "desired_position_row_hash": row.desired_position_row_hash,
        "desired_rounded_position": row.desired_rounded_position,
        "evidence_check_bundle_hash": row.evidence_check_bundle_hash,
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "market_fallback_policy_status": row.market_fallback_policy_status,
        "order_kind": row.order_kind,
        "order_quantity": row.order_quantity,
        "order_required": row.order_required,
        "order_side": row.order_side,
        "position_change_contracts": row.position_change_contracts,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "tick_rounding_policy_status": row.tick_rounding_policy_status,
        "working_order_lifecycle_status": row.working_order_lifecycle_status,
    }


def _order_transition_row_hash_payload(row: OrderTransitionExecutableLedgerRow) -> dict[str, object]:
    return {
        "current_position_before_transition": row.current_position_before_transition,
        "desired_position_after_transition": row.desired_position_after_transition,
        "desired_position_bundle_hash": row.desired_position_bundle_hash,
        "ending_position_without_fill": row.ending_position_without_fill,
        "fill_rows_emitted": row.fill_rows_emitted,
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "order_intent_row_hash": row.order_intent_row_hash,
        "position_change_contracts": row.position_change_contracts,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "transition_kind": row.transition_kind,
        "transition_required": row.transition_required,
        "working_order_lifecycle_status": row.working_order_lifecycle_status,
        "working_order_state_after_hash": row.working_order_state_after_hash,
        "working_order_state_before_hash": row.working_order_state_before_hash,
    }


def _order_transition_bundle_hash_payload(bundle: OrderTransitionExecutableBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_ORDER_TRANSITION_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "bundle_hashes": {
            "desired_position_bundle_hash": bundle.desired_position_bundle.bundle_hash,
            "evidence_check_bundle_hash": _evidence_check_bundle_hash(bundle.evidence_checks),
            "order_intent_row_hash": bundle.order_intent_row.row_hash,
            "order_transition_row_hash": bundle.order_transition_row.row_hash,
        },
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "fill_rows_emitted": bundle.fill_rows_emitted,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "limit_order_rows_emitted": bundle.limit_order_rows_emitted,
        "market_order_rows_emitted": bundle.market_order_rows_emitted,
        "non_authorizations": bundle.non_authorizations,
        "order_intent_rows_emitted": bundle.order_intent_rows_emitted,
        "order_transition_rows_emitted": bundle.order_transition_rows_emitted,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
    }

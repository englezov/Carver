from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .order_transition_executable import (
    NO_ORDER_KIND,
    NO_POSITION_CHANGE_TRANSITION_KIND,
    OrderTransitionExecutableBundle,
    build_order_transition_executable_ledger,
)
from .runtime_evidence_gate import RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH
from .validation import require_hash, require_integer, require_text


S27_V2_NO_FILL_AUTHORIZATION = "S27_V2_NON_RESULT_NO_FILL_EXECUTABLE_METADATA"
S27_V2_NO_FILL_STATUS = "S27_V2_NO_FILL_EXECUTABLE_REMEDIATION_PACK_NON_RESULT"
NO_FILL_METADATA_ROW_STATUS = "LOCAL_NO_FILL_METADATA_NO_ORDER_NO_POSITION_CHANGE_NOT_ACTUAL_FILL"

NO_FILL_REASON_CODE = "S27_NO_FILL_BOUND_TO_ACTIVE_NO_ORDER_TRANSITION_NOT_FILL_LEDGER"
NOT_APPLICABLE = "NOT_APPLICABLE"
ACTUAL_FILL_LEDGER_STATUS = "FAIL_CLOSED_ACTUAL_FILL_LEDGER_NOT_EMITTED"

NO_FILL_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_ACTUAL_POSITIVE_FILL_EMISSION",
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
class NoFillExecutableMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    order_transition_bundle_hash: str
    order_intent_row_hash: str
    order_transition_row_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    raw_symbol: str
    order_kind: str
    order_quantity: int
    transition_kind: str
    fill_required: bool
    fill_rows_emitted: bool
    actual_fill_ledger_emitted: bool
    actual_fill_ledger_status: str
    filled_order_hash: str
    fill_price: str
    fill_quantity: int
    fill_price_provenance: str
    no_fill_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 no-fill row standalone validation is not authoritative; validate the bundle")

    def _validate_structural_formula(self) -> None:
        if self.ledger_label != "NO_FILL_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 no-fill ledger label is not locked")
        if self.row_status != NO_FILL_METADATA_ROW_STATUS:
            raise CarverBlocked("S27 v2 no-fill row status is not locked")
        if self.reason_code != NO_FILL_REASON_CODE:
            raise CarverBlocked("S27 v2 no-fill reason code is not locked")
        for name, hash_value in (
            ("order transition bundle hash", self.order_transition_bundle_hash),
            ("order intent row hash", self.order_intent_row_hash),
            ("order transition row hash", self.order_transition_row_hash),
            ("no-fill policy hash", self.no_fill_policy_hash),
            ("row hash", self.row_hash),
        ):
            require_hash(f"S27 v2 no-fill {name}", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("order kind", self.order_kind),
            ("transition kind", self.transition_kind),
            ("actual fill ledger status", self.actual_fill_ledger_status),
            ("filled order hash", self.filled_order_hash),
            ("fill price", self.fill_price),
            ("fill price provenance", self.fill_price_provenance),
        ):
            require_text(f"S27 v2 no-fill {name}", value)
        require_integer("S27 v2 no-fill order quantity", self.order_quantity)
        require_integer("S27 v2 no-fill quantity", self.fill_quantity)
        if self.order_kind != NO_ORDER_KIND:
            raise CarverBlocked("S27 v2 no-fill metadata must bind NO_ORDER")
        if self.order_quantity != 0:
            raise CarverBlocked("S27 v2 no-fill metadata must bind zero order quantity")
        if self.transition_kind != NO_POSITION_CHANGE_TRANSITION_KIND:
            raise CarverBlocked("S27 v2 no-fill metadata must bind no-position-change transition")
        if self.fill_required is not False:
            raise CarverBlocked("S27 v2 no-fill metadata must not require a fill")
        if self.fill_rows_emitted is not False:
            raise CarverBlocked("S27 v2 no-fill metadata must not emit fill rows")
        if self.actual_fill_ledger_emitted is not False:
            raise CarverBlocked("S27 v2 no-fill metadata must not emit an actual FillLedgerRow")
        if self.actual_fill_ledger_status != ACTUAL_FILL_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 no-fill actual fill ledger status must remain fail-closed")
        if self.filled_order_hash != NOT_APPLICABLE:
            raise CarverBlocked("S27 v2 no-fill metadata must not carry a filled-order hash")
        if self.fill_price != NOT_APPLICABLE:
            raise CarverBlocked("S27 v2 no-fill metadata must not carry a fill price")
        if self.fill_quantity != 0:
            raise CarverBlocked("S27 v2 no-fill metadata must bind zero fill quantity")
        if self.fill_price_provenance != NOT_APPLICABLE:
            raise CarverBlocked("S27 v2 no-fill metadata must not carry fill price provenance")
        if self.no_fill_policy_hash != _policy_hash(
            "no_fill_policy",
            self.order_kind,
            self.order_quantity,
            self.transition_kind,
            self.fill_required,
            self.actual_fill_ledger_status,
        ):
            raise CarverBlocked("S27 v2 no-fill policy hash must bind no-fill policy")
        if self.row_hash != canonical_sha256(_no_fill_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-fill row hash must be content-bound")


@dataclass(frozen=True)
class NoFillExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    order_transition_bundle: OrderTransitionExecutableBundle
    no_fill_row: NoFillExecutableMetadataRow
    no_fill_metadata_rows_emitted: bool
    actual_fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NO_FILL_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_NO_FILL_STATUS:
            raise CarverBlocked("S27 v2 no-fill executable status is not locked")
        if self.authorization_label != S27_V2_NO_FILL_AUTHORIZATION:
            raise CarverBlocked("S27 v2 no-fill executable authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 no-fill executable must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 no-fill executable must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 no-fill executable is locked to the audited remediation pack")
        self.order_transition_bundle.validate()
        active_order_transition = build_order_transition_executable_ledger(pack_path)
        if self.order_transition_bundle != active_order_transition:
            raise CarverBlocked("S27 v2 no-fill executable must bind active order/transition bundle")
        self.no_fill_row._validate_structural_formula()
        active_row = _build_active_no_fill_row(pack_path, active_order_transition)
        if self.no_fill_row != active_row:
            raise CarverBlocked("S27 v2 no-fill row must match active no-order transition")
        if self.no_fill_metadata_rows_emitted is not True:
            raise CarverBlocked("S27 v2 no-fill executable must emit no-fill metadata")
        if any(
            flag is not False
            for flag in (
                self.actual_fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 no-fill executable cannot emit fill/cost/PnL/result/evidence")
        if self.non_authorizations != NO_FILL_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 no-fill executable must preserve non-authorizations")
        require_hash("S27 v2 no-fill executable bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_no_fill_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-fill executable bundle hash must be content-bound")


def build_no_fill_executable_metadata(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> NoFillExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 no-fill executable is locked to the audited remediation pack")
    order_transition_bundle = build_order_transition_executable_ledger(pack_path)
    no_fill_row = _build_active_no_fill_row(pack_path, order_transition_bundle)
    bundle = NoFillExecutableBundle(
        status=S27_V2_NO_FILL_STATUS,
        authorization_label=S27_V2_NO_FILL_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        order_transition_bundle=order_transition_bundle,
        no_fill_row=no_fill_row,
        no_fill_metadata_rows_emitted=True,
        actual_fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = NoFillExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_no_fill_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_no_fill_row(
    pack_path: Path,
    order_transition_bundle: OrderTransitionExecutableBundle,
) -> NoFillExecutableMetadataRow:
    order_intent = order_transition_bundle.order_intent_row
    transition = order_transition_bundle.order_transition_row
    if order_intent.order_kind != NO_ORDER_KIND or order_intent.order_quantity != 0:
        raise CarverBlocked("S27 v2 no-fill executable requires active no-order intent")
    if transition.transition_kind != NO_POSITION_CHANGE_TRANSITION_KIND:
        raise CarverBlocked("S27 v2 no-fill executable requires active no-position-change transition")
    if transition.fill_rows_emitted is not False:
        raise CarverBlocked("S27 v2 no-fill executable requires active transition with no fill rows")
    row = NoFillExecutableMetadataRow(
        ledger_label="NO_FILL_METADATA_LEDGER",
        row_status=NO_FILL_METADATA_ROW_STATUS,
        reason_code=NO_FILL_REASON_CODE,
        order_transition_bundle_hash=order_transition_bundle.bundle_hash,
        order_intent_row_hash=order_intent.row_hash,
        order_transition_row_hash=transition.row_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=order_intent.selected_decision_timestamp_utc,
        raw_symbol=order_intent.raw_symbol,
        order_kind=order_intent.order_kind,
        order_quantity=order_intent.order_quantity,
        transition_kind=transition.transition_kind,
        fill_required=False,
        fill_rows_emitted=False,
        actual_fill_ledger_emitted=False,
        actual_fill_ledger_status=ACTUAL_FILL_LEDGER_STATUS,
        filled_order_hash=NOT_APPLICABLE,
        fill_price=NOT_APPLICABLE,
        fill_quantity=0,
        fill_price_provenance=NOT_APPLICABLE,
        no_fill_policy_hash=_policy_hash(
            "no_fill_policy",
            order_intent.order_kind,
            order_intent.order_quantity,
            transition.transition_kind,
            False,
            ACTUAL_FILL_LEDGER_STATUS,
        ),
        row_hash="0" * 64,
    )
    row = NoFillExecutableMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_no_fill_row_hash_payload(row))}
    )
    row._validate_structural_formula()
    return row


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_NO_FILL_POLICY", "label": label, "values": values})


def _no_fill_row_hash_payload(row: NoFillExecutableMetadataRow) -> dict[str, object]:
    return {
        "actual_fill_ledger_emitted": row.actual_fill_ledger_emitted,
        "actual_fill_ledger_status": row.actual_fill_ledger_status,
        "fill_price": row.fill_price,
        "fill_price_provenance": row.fill_price_provenance,
        "fill_quantity": row.fill_quantity,
        "fill_required": row.fill_required,
        "fill_rows_emitted": row.fill_rows_emitted,
        "filled_order_hash": row.filled_order_hash,
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "no_fill_policy_hash": row.no_fill_policy_hash,
        "order_intent_row_hash": row.order_intent_row_hash,
        "order_kind": row.order_kind,
        "order_quantity": row.order_quantity,
        "order_transition_bundle_hash": row.order_transition_bundle_hash,
        "order_transition_row_hash": row.order_transition_row_hash,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "transition_kind": row.transition_kind,
    }


def _no_fill_bundle_hash_payload(bundle: NoFillExecutableBundle) -> dict[str, object]:
    return {
        "actual_fill_rows_emitted": bundle.actual_fill_rows_emitted,
        "artifact": "S27_V2_NO_FILL_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "no_fill_metadata_rows_emitted": bundle.no_fill_metadata_rows_emitted,
        "no_fill_row_hash": bundle.no_fill_row.row_hash,
        "non_authorizations": bundle.non_authorizations,
        "order_transition_bundle_hash": bundle.order_transition_bundle.bundle_hash,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
    }

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .no_fill_executable import (
    ACTUAL_FILL_LEDGER_STATUS,
    NOT_APPLICABLE,
    NoFillExecutableBundle,
    build_no_fill_executable_metadata,
)
from .order_transition_executable import NO_ORDER_KIND, NO_POSITION_CHANGE_TRANSITION_KIND
from .runtime_evidence_gate import RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH
from .validation import require_hash, require_integer, require_non_negative_number, require_text


S27_V2_NO_COST_AUTHORIZATION = "S27_V2_NON_RESULT_NO_COST_EXECUTABLE_METADATA"
S27_V2_NO_COST_STATUS = "S27_V2_NO_COST_EXECUTABLE_REMEDIATION_PACK_NON_RESULT"
NO_COST_METADATA_ROW_STATUS = "LOCAL_NO_COST_METADATA_NO_ORDER_NO_FILL_NOT_ACTUAL_COST"

NO_COST_REASON_CODE = "S27_NO_COST_BOUND_TO_ACTIVE_NO_FILL_METADATA_NOT_COST_LEDGER"
NO_COST_PROVENANCE = "NO_ORDER_NO_FILL_NO_COST"
ACTUAL_COST_LEDGER_STATUS = "FAIL_CLOSED_ACTUAL_COST_LEDGER_NOT_EMITTED"

NO_COST_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_ACTUAL_POSITIVE_FILL_EMISSION",
    "NO_ACTUAL_COMMISSION_SPREAD_COST_EMISSION",
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
class NoCostExecutableMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    no_fill_bundle_hash: str
    no_fill_row_hash: str
    order_transition_bundle_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    raw_symbol: str
    order_kind: str
    order_quantity: int
    transition_kind: str
    fill_required: bool
    actual_fill_ledger_emitted: bool
    actual_fill_ledger_status: str
    cost_required: bool
    cost_rows_emitted: bool
    actual_commission_ledger_emitted: bool
    actual_spread_cost_ledger_emitted: bool
    actual_cost_ledger_emitted: bool
    actual_cost_ledger_status: str
    commission_amount: float
    spread_amount: float
    spread_cost_amount: float
    total_cost_amount: float
    total_cost_currency: str
    cost_provenance: str
    no_cost_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 no-cost row standalone validation is not authoritative; validate the bundle")

    def _validate_structural_formula(self) -> None:
        if self.ledger_label != "NO_COST_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 no-cost ledger label is not locked")
        if self.row_status != NO_COST_METADATA_ROW_STATUS:
            raise CarverBlocked("S27 v2 no-cost row status is not locked")
        if self.reason_code != NO_COST_REASON_CODE:
            raise CarverBlocked("S27 v2 no-cost reason code is not locked")
        for name, hash_value in (
            ("no-fill bundle hash", self.no_fill_bundle_hash),
            ("no-fill row hash", self.no_fill_row_hash),
            ("order transition bundle hash", self.order_transition_bundle_hash),
            ("no-cost policy hash", self.no_cost_policy_hash),
            ("row hash", self.row_hash),
        ):
            require_hash(f"S27 v2 no-cost {name}", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("order kind", self.order_kind),
            ("transition kind", self.transition_kind),
            ("actual fill ledger status", self.actual_fill_ledger_status),
            ("actual cost ledger status", self.actual_cost_ledger_status),
            ("total cost currency", self.total_cost_currency),
            ("cost provenance", self.cost_provenance),
        ):
            require_text(f"S27 v2 no-cost {name}", value)
        require_integer("S27 v2 no-cost order quantity", self.order_quantity)
        for name, value in (
            ("commission amount", self.commission_amount),
            ("spread amount", self.spread_amount),
            ("spread cost amount", self.spread_cost_amount),
            ("total cost amount", self.total_cost_amount),
        ):
            require_non_negative_number(f"S27 v2 no-cost {name}", value)
        if self.order_kind != NO_ORDER_KIND:
            raise CarverBlocked("S27 v2 no-cost metadata must bind NO_ORDER")
        if self.order_quantity != 0:
            raise CarverBlocked("S27 v2 no-cost metadata must bind zero order quantity")
        if self.transition_kind != NO_POSITION_CHANGE_TRANSITION_KIND:
            raise CarverBlocked("S27 v2 no-cost metadata must bind no-position-change transition")
        if self.fill_required is not False:
            raise CarverBlocked("S27 v2 no-cost metadata must not require a fill")
        if self.actual_fill_ledger_emitted is not False:
            raise CarverBlocked("S27 v2 no-cost metadata must bind fail-closed fill ledger")
        if self.actual_fill_ledger_status != ACTUAL_FILL_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 no-cost fill ledger status must remain fail-closed")
        if self.cost_required is not False:
            raise CarverBlocked("S27 v2 no-cost metadata must not require cost accounting")
        if self.cost_rows_emitted is not False:
            raise CarverBlocked("S27 v2 no-cost metadata must not emit cost rows")
        if self.actual_commission_ledger_emitted is not False:
            raise CarverBlocked("S27 v2 no-cost metadata must not emit commission ledger rows")
        if self.actual_spread_cost_ledger_emitted is not False:
            raise CarverBlocked("S27 v2 no-cost metadata must not emit spread-cost ledger rows")
        if self.actual_cost_ledger_emitted is not False:
            raise CarverBlocked("S27 v2 no-cost metadata must not emit an actual CostLedgerRow")
        if self.actual_cost_ledger_status != ACTUAL_COST_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 no-cost actual cost ledger status must remain fail-closed")
        if any(
            amount != 0
            for amount in (
                self.commission_amount,
                self.spread_amount,
                self.spread_cost_amount,
                self.total_cost_amount,
            )
        ):
            raise CarverBlocked("S27 v2 no-cost metadata must bind zero cost amounts")
        if self.total_cost_currency != NOT_APPLICABLE:
            raise CarverBlocked("S27 v2 no-cost metadata must not carry a cost currency")
        if self.cost_provenance != NO_COST_PROVENANCE:
            raise CarverBlocked("S27 v2 no-cost provenance must bind no-order/no-fill")
        if self.no_cost_policy_hash != _policy_hash(
            "no_cost_policy",
            self.order_kind,
            self.order_quantity,
            self.transition_kind,
            self.fill_required,
            self.actual_fill_ledger_status,
            self.cost_required,
            self.actual_cost_ledger_status,
            self.total_cost_amount,
        ):
            raise CarverBlocked("S27 v2 no-cost policy hash must bind no-cost policy")
        if self.row_hash != canonical_sha256(_no_cost_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-cost row hash must be content-bound")


@dataclass(frozen=True)
class NoCostExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    no_fill_bundle: NoFillExecutableBundle
    no_cost_row: NoCostExecutableMetadataRow
    no_cost_metadata_rows_emitted: bool
    actual_cost_rows_emitted: bool
    actual_commission_rows_emitted: bool
    actual_spread_cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NO_COST_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_NO_COST_STATUS:
            raise CarverBlocked("S27 v2 no-cost executable status is not locked")
        if self.authorization_label != S27_V2_NO_COST_AUTHORIZATION:
            raise CarverBlocked("S27 v2 no-cost executable authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 no-cost executable must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 no-cost executable must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 no-cost executable is locked to the audited remediation pack")
        active_no_fill = build_no_fill_executable_metadata(pack_path)
        if self.no_fill_bundle != active_no_fill:
            raise CarverBlocked("S27 v2 no-cost executable must bind active no-fill bundle")
        self.no_cost_row._validate_structural_formula()
        active_row = _build_active_no_cost_row(pack_path, active_no_fill)
        if self.no_cost_row != active_row:
            raise CarverBlocked("S27 v2 no-cost row must match active no-fill metadata")
        if self.no_cost_metadata_rows_emitted is not True:
            raise CarverBlocked("S27 v2 no-cost executable must emit no-cost metadata")
        if any(
            flag is not False
            for flag in (
                self.actual_cost_rows_emitted,
                self.actual_commission_rows_emitted,
                self.actual_spread_cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 no-cost executable cannot emit cost/PnL/result/evidence")
        if self.non_authorizations != NO_COST_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 no-cost executable must preserve non-authorizations")
        require_hash("S27 v2 no-cost executable bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_no_cost_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-cost executable bundle hash must be content-bound")


def build_no_cost_executable_metadata(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> NoCostExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 no-cost executable is locked to the audited remediation pack")
    no_fill_bundle = build_no_fill_executable_metadata(pack_path)
    no_cost_row = _build_active_no_cost_row(pack_path, no_fill_bundle)
    bundle = NoCostExecutableBundle(
        status=S27_V2_NO_COST_STATUS,
        authorization_label=S27_V2_NO_COST_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        no_fill_bundle=no_fill_bundle,
        no_cost_row=no_cost_row,
        no_cost_metadata_rows_emitted=True,
        actual_cost_rows_emitted=False,
        actual_commission_rows_emitted=False,
        actual_spread_cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = NoCostExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_no_cost_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_no_cost_row(
    pack_path: Path,
    no_fill_bundle: NoFillExecutableBundle,
) -> NoCostExecutableMetadataRow:
    no_fill_row = no_fill_bundle.no_fill_row
    if no_fill_row.order_kind != NO_ORDER_KIND or no_fill_row.order_quantity != 0:
        raise CarverBlocked("S27 v2 no-cost executable requires active no-order metadata")
    if no_fill_row.transition_kind != NO_POSITION_CHANGE_TRANSITION_KIND:
        raise CarverBlocked("S27 v2 no-cost executable requires active no-position-change metadata")
    if no_fill_row.fill_required is not False or no_fill_row.actual_fill_ledger_emitted is not False:
        raise CarverBlocked("S27 v2 no-cost executable requires active no-fill metadata")
    row = NoCostExecutableMetadataRow(
        ledger_label="NO_COST_METADATA_LEDGER",
        row_status=NO_COST_METADATA_ROW_STATUS,
        reason_code=NO_COST_REASON_CODE,
        no_fill_bundle_hash=no_fill_bundle.bundle_hash,
        no_fill_row_hash=no_fill_row.row_hash,
        order_transition_bundle_hash=no_fill_row.order_transition_bundle_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=no_fill_row.selected_decision_timestamp_utc,
        raw_symbol=no_fill_row.raw_symbol,
        order_kind=no_fill_row.order_kind,
        order_quantity=no_fill_row.order_quantity,
        transition_kind=no_fill_row.transition_kind,
        fill_required=no_fill_row.fill_required,
        actual_fill_ledger_emitted=no_fill_row.actual_fill_ledger_emitted,
        actual_fill_ledger_status=no_fill_row.actual_fill_ledger_status,
        cost_required=False,
        cost_rows_emitted=False,
        actual_commission_ledger_emitted=False,
        actual_spread_cost_ledger_emitted=False,
        actual_cost_ledger_emitted=False,
        actual_cost_ledger_status=ACTUAL_COST_LEDGER_STATUS,
        commission_amount=0.0,
        spread_amount=0.0,
        spread_cost_amount=0.0,
        total_cost_amount=0.0,
        total_cost_currency=NOT_APPLICABLE,
        cost_provenance=NO_COST_PROVENANCE,
        no_cost_policy_hash=_policy_hash(
            "no_cost_policy",
            no_fill_row.order_kind,
            no_fill_row.order_quantity,
            no_fill_row.transition_kind,
            no_fill_row.fill_required,
            no_fill_row.actual_fill_ledger_status,
            False,
            ACTUAL_COST_LEDGER_STATUS,
            0.0,
        ),
        row_hash="0" * 64,
    )
    row = NoCostExecutableMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_no_cost_row_hash_payload(row))}
    )
    row._validate_structural_formula()
    return row


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_NO_COST_POLICY", "label": label, "values": values})


def _no_cost_row_hash_payload(row: NoCostExecutableMetadataRow) -> dict[str, object]:
    return {
        "actual_commission_ledger_emitted": row.actual_commission_ledger_emitted,
        "actual_cost_ledger_emitted": row.actual_cost_ledger_emitted,
        "actual_cost_ledger_status": row.actual_cost_ledger_status,
        "actual_fill_ledger_emitted": row.actual_fill_ledger_emitted,
        "actual_fill_ledger_status": row.actual_fill_ledger_status,
        "actual_spread_cost_ledger_emitted": row.actual_spread_cost_ledger_emitted,
        "commission_amount": row.commission_amount,
        "cost_provenance": row.cost_provenance,
        "cost_required": row.cost_required,
        "cost_rows_emitted": row.cost_rows_emitted,
        "fill_required": row.fill_required,
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "no_cost_policy_hash": row.no_cost_policy_hash,
        "no_fill_bundle_hash": row.no_fill_bundle_hash,
        "no_fill_row_hash": row.no_fill_row_hash,
        "order_kind": row.order_kind,
        "order_quantity": row.order_quantity,
        "order_transition_bundle_hash": row.order_transition_bundle_hash,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "spread_amount": row.spread_amount,
        "spread_cost_amount": row.spread_cost_amount,
        "total_cost_amount": row.total_cost_amount,
        "total_cost_currency": row.total_cost_currency,
        "transition_kind": row.transition_kind,
    }


def _no_cost_bundle_hash_payload(bundle: NoCostExecutableBundle) -> dict[str, object]:
    return {
        "actual_commission_rows_emitted": bundle.actual_commission_rows_emitted,
        "actual_cost_rows_emitted": bundle.actual_cost_rows_emitted,
        "actual_spread_cost_rows_emitted": bundle.actual_spread_cost_rows_emitted,
        "artifact": "S27_V2_NO_COST_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "no_cost_metadata_rows_emitted": bundle.no_cost_metadata_rows_emitted,
        "no_cost_row_hash": bundle.no_cost_row.row_hash,
        "no_fill_bundle_hash": bundle.no_fill_bundle.bundle_hash,
        "non_authorizations": bundle.non_authorizations,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
    }

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .no_cost_executable import (
    ACTUAL_COST_LEDGER_STATUS,
    NoCostExecutableBundle,
    build_no_cost_executable_metadata,
)
from .no_fill_executable import ACTUAL_FILL_LEDGER_STATUS, NOT_APPLICABLE
from .order_transition_executable import NO_ORDER_KIND, NO_POSITION_CHANGE_TRANSITION_KIND
from .runtime_evidence_gate import RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH
from .validation import require_hash, require_integer, require_text


S27_V2_NO_PNL_AUTHORIZATION = "S27_V2_NON_RESULT_NO_PNL_EXECUTABLE_METADATA"
S27_V2_NO_PNL_STATUS = "S27_V2_NO_PNL_EXECUTABLE_REMEDIATION_PACK_NON_RESULT"
NO_PNL_METADATA_ROW_STATUS = "LOCAL_NO_PNL_METADATA_NO_ORDER_NO_FILL_NO_COST_NOT_ACTUAL_PNL"

NO_PNL_REASON_CODE = "S27_NO_PNL_BOUND_TO_ACTIVE_NO_COST_METADATA_NOT_PNL_LEDGER"
NO_PNL_PROVENANCE = "NO_ORDER_NO_FILL_NO_COST_NO_PNL"
ACTUAL_PNL_LEDGER_STATUS = "FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED"

NO_PNL_NON_AUTHORIZATIONS = (
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
    "NO_ACTUAL_PNL_LEDGER_EMISSION",
    "NO_RESULT_EMISSION",
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
class NoPnlExecutableMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    no_cost_bundle_hash: str
    no_cost_row_hash: str
    no_fill_bundle_hash: str
    no_fill_row_hash: str
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
    actual_cost_ledger_emitted: bool
    actual_cost_ledger_status: str
    pnl_required: bool
    pnl_rows_emitted: bool
    actual_pnl_ledger_emitted: bool
    actual_pnl_ledger_status: str
    actual_result_row_emitted: bool
    actual_backtest_result_emitted: bool
    result_interpretation_emitted: bool
    pnl_amount: str
    pnl_currency: str
    pnl_provenance: str
    no_pnl_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 no-PnL row standalone validation is not authoritative; validate the bundle")

    def _validate_structural_formula(self) -> None:
        if self.ledger_label != "NO_PNL_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 no-PnL ledger label is not locked")
        if self.row_status != NO_PNL_METADATA_ROW_STATUS:
            raise CarverBlocked("S27 v2 no-PnL row status is not locked")
        if self.reason_code != NO_PNL_REASON_CODE:
            raise CarverBlocked("S27 v2 no-PnL reason code is not locked")
        for name, hash_value in (
            ("no-cost bundle hash", self.no_cost_bundle_hash),
            ("no-cost row hash", self.no_cost_row_hash),
            ("no-fill bundle hash", self.no_fill_bundle_hash),
            ("no-fill row hash", self.no_fill_row_hash),
            ("no-PnL policy hash", self.no_pnl_policy_hash),
            ("row hash", self.row_hash),
        ):
            require_hash(f"S27 v2 no-PnL {name}", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("order kind", self.order_kind),
            ("transition kind", self.transition_kind),
            ("actual fill ledger status", self.actual_fill_ledger_status),
            ("actual cost ledger status", self.actual_cost_ledger_status),
            ("actual PnL ledger status", self.actual_pnl_ledger_status),
            ("PnL amount", self.pnl_amount),
            ("PnL currency", self.pnl_currency),
            ("PnL provenance", self.pnl_provenance),
        ):
            require_text(f"S27 v2 no-PnL {name}", value)
        require_integer("S27 v2 no-PnL order quantity", self.order_quantity)
        if self.order_kind != NO_ORDER_KIND:
            raise CarverBlocked("S27 v2 no-PnL metadata must bind NO_ORDER")
        if self.order_quantity != 0:
            raise CarverBlocked("S27 v2 no-PnL metadata must bind zero order quantity")
        if self.transition_kind != NO_POSITION_CHANGE_TRANSITION_KIND:
            raise CarverBlocked("S27 v2 no-PnL metadata must bind no-position-change transition")
        if self.fill_required is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must not require a fill")
        if self.actual_fill_ledger_emitted is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must bind fail-closed fill ledger")
        if self.actual_fill_ledger_status != ACTUAL_FILL_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 no-PnL fill ledger status must remain fail-closed")
        if self.cost_required is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must not require cost accounting")
        if self.actual_cost_ledger_emitted is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must bind fail-closed cost ledger")
        if self.actual_cost_ledger_status != ACTUAL_COST_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 no-PnL cost ledger status must remain fail-closed")
        if self.pnl_required is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must not require PnL accounting")
        if self.pnl_rows_emitted is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must not emit PnL rows")
        if self.actual_pnl_ledger_emitted is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must not emit an actual PnlLedgerRow")
        if self.actual_pnl_ledger_status != ACTUAL_PNL_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 no-PnL actual PnL ledger status must remain fail-closed")
        if self.actual_result_row_emitted is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must not emit result rows")
        if self.actual_backtest_result_emitted is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must not emit backtest result rows")
        if self.result_interpretation_emitted is not False:
            raise CarverBlocked("S27 v2 no-PnL metadata must not emit result interpretation")
        if self.pnl_amount != NOT_APPLICABLE:
            raise CarverBlocked("S27 v2 no-PnL metadata must not carry a PnL amount")
        if self.pnl_currency != NOT_APPLICABLE:
            raise CarverBlocked("S27 v2 no-PnL metadata must not carry a PnL currency")
        if self.pnl_provenance != NO_PNL_PROVENANCE:
            raise CarverBlocked("S27 v2 no-PnL provenance must bind no-order/no-fill/no-cost")
        if self.no_pnl_policy_hash != _policy_hash(
            "no_pnl_policy",
            self.order_kind,
            self.order_quantity,
            self.transition_kind,
            self.fill_required,
            self.actual_fill_ledger_status,
            self.cost_required,
            self.actual_cost_ledger_status,
            self.pnl_required,
            self.actual_pnl_ledger_status,
            self.pnl_amount,
            self.pnl_currency,
            self.pnl_provenance,
        ):
            raise CarverBlocked("S27 v2 no-PnL policy hash must bind no-PnL policy")
        if self.row_hash != canonical_sha256(_no_pnl_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-PnL row hash must be content-bound")


@dataclass(frozen=True)
class NoPnlExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    no_cost_bundle: NoCostExecutableBundle
    no_pnl_row: NoPnlExecutableMetadataRow
    no_pnl_metadata_rows_emitted: bool
    actual_pnl_rows_emitted: bool
    actual_result_rows_emitted: bool
    actual_backtest_result_emitted: bool
    result_interpretation_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NO_PNL_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_NO_PNL_STATUS:
            raise CarverBlocked("S27 v2 no-PnL executable status is not locked")
        if self.authorization_label != S27_V2_NO_PNL_AUTHORIZATION:
            raise CarverBlocked("S27 v2 no-PnL executable authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 no-PnL executable must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 no-PnL executable must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 no-PnL executable is locked to the audited remediation pack")
        active_no_cost = build_no_cost_executable_metadata(pack_path)
        if self.no_cost_bundle != active_no_cost:
            raise CarverBlocked("S27 v2 no-PnL executable must bind active no-cost bundle")
        self.no_pnl_row._validate_structural_formula()
        active_row = _build_active_no_pnl_row(pack_path, active_no_cost)
        if self.no_pnl_row != active_row:
            raise CarverBlocked("S27 v2 no-PnL row must match active no-cost metadata")
        if self.no_pnl_metadata_rows_emitted is not True:
            raise CarverBlocked("S27 v2 no-PnL executable must emit no-PnL metadata")
        if any(
            flag is not False
            for flag in (
                self.actual_pnl_rows_emitted,
                self.actual_result_rows_emitted,
                self.actual_backtest_result_emitted,
                self.result_interpretation_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 no-PnL executable cannot emit PnL/result/evidence")
        if self.non_authorizations != NO_PNL_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 no-PnL executable must preserve non-authorizations")
        require_hash("S27 v2 no-PnL executable bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_no_pnl_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-PnL executable bundle hash must be content-bound")


def build_no_pnl_executable_metadata(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> NoPnlExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 no-PnL executable is locked to the audited remediation pack")
    no_cost_bundle = build_no_cost_executable_metadata(pack_path)
    no_pnl_row = _build_active_no_pnl_row(pack_path, no_cost_bundle)
    bundle = NoPnlExecutableBundle(
        status=S27_V2_NO_PNL_STATUS,
        authorization_label=S27_V2_NO_PNL_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        no_cost_bundle=no_cost_bundle,
        no_pnl_row=no_pnl_row,
        no_pnl_metadata_rows_emitted=True,
        actual_pnl_rows_emitted=False,
        actual_result_rows_emitted=False,
        actual_backtest_result_emitted=False,
        result_interpretation_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = NoPnlExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_no_pnl_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_no_pnl_row(
    pack_path: Path,
    no_cost_bundle: NoCostExecutableBundle,
) -> NoPnlExecutableMetadataRow:
    no_cost_row = no_cost_bundle.no_cost_row
    if no_cost_row.order_kind != NO_ORDER_KIND or no_cost_row.order_quantity != 0:
        raise CarverBlocked("S27 v2 no-PnL executable requires active no-order metadata")
    if no_cost_row.transition_kind != NO_POSITION_CHANGE_TRANSITION_KIND:
        raise CarverBlocked("S27 v2 no-PnL executable requires active no-position-change metadata")
    if no_cost_row.fill_required is not False or no_cost_row.actual_fill_ledger_emitted is not False:
        raise CarverBlocked("S27 v2 no-PnL executable requires active no-fill metadata")
    if no_cost_row.cost_required is not False or no_cost_row.actual_cost_ledger_emitted is not False:
        raise CarverBlocked("S27 v2 no-PnL executable requires active no-cost metadata")
    row = NoPnlExecutableMetadataRow(
        ledger_label="NO_PNL_METADATA_LEDGER",
        row_status=NO_PNL_METADATA_ROW_STATUS,
        reason_code=NO_PNL_REASON_CODE,
        no_cost_bundle_hash=no_cost_bundle.bundle_hash,
        no_cost_row_hash=no_cost_row.row_hash,
        no_fill_bundle_hash=no_cost_row.no_fill_bundle_hash,
        no_fill_row_hash=no_cost_row.no_fill_row_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=no_cost_row.selected_decision_timestamp_utc,
        raw_symbol=no_cost_row.raw_symbol,
        order_kind=no_cost_row.order_kind,
        order_quantity=no_cost_row.order_quantity,
        transition_kind=no_cost_row.transition_kind,
        fill_required=no_cost_row.fill_required,
        actual_fill_ledger_emitted=no_cost_row.actual_fill_ledger_emitted,
        actual_fill_ledger_status=no_cost_row.actual_fill_ledger_status,
        cost_required=no_cost_row.cost_required,
        actual_cost_ledger_emitted=no_cost_row.actual_cost_ledger_emitted,
        actual_cost_ledger_status=no_cost_row.actual_cost_ledger_status,
        pnl_required=False,
        pnl_rows_emitted=False,
        actual_pnl_ledger_emitted=False,
        actual_pnl_ledger_status=ACTUAL_PNL_LEDGER_STATUS,
        actual_result_row_emitted=False,
        actual_backtest_result_emitted=False,
        result_interpretation_emitted=False,
        pnl_amount=NOT_APPLICABLE,
        pnl_currency=NOT_APPLICABLE,
        pnl_provenance=NO_PNL_PROVENANCE,
        no_pnl_policy_hash=_policy_hash(
            "no_pnl_policy",
            no_cost_row.order_kind,
            no_cost_row.order_quantity,
            no_cost_row.transition_kind,
            no_cost_row.fill_required,
            no_cost_row.actual_fill_ledger_status,
            no_cost_row.cost_required,
            no_cost_row.actual_cost_ledger_status,
            False,
            ACTUAL_PNL_LEDGER_STATUS,
            NOT_APPLICABLE,
            NOT_APPLICABLE,
            NO_PNL_PROVENANCE,
        ),
        row_hash="0" * 64,
    )
    row = NoPnlExecutableMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_no_pnl_row_hash_payload(row))}
    )
    row._validate_structural_formula()
    return row


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_NO_PNL_POLICY", "label": label, "values": values})


def _no_pnl_row_hash_payload(row: NoPnlExecutableMetadataRow) -> dict[str, object]:
    return {
        "actual_backtest_result_emitted": row.actual_backtest_result_emitted,
        "actual_cost_ledger_emitted": row.actual_cost_ledger_emitted,
        "actual_cost_ledger_status": row.actual_cost_ledger_status,
        "actual_fill_ledger_emitted": row.actual_fill_ledger_emitted,
        "actual_fill_ledger_status": row.actual_fill_ledger_status,
        "actual_pnl_ledger_emitted": row.actual_pnl_ledger_emitted,
        "actual_pnl_ledger_status": row.actual_pnl_ledger_status,
        "actual_result_row_emitted": row.actual_result_row_emitted,
        "cost_required": row.cost_required,
        "fill_required": row.fill_required,
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "no_cost_bundle_hash": row.no_cost_bundle_hash,
        "no_cost_row_hash": row.no_cost_row_hash,
        "no_fill_bundle_hash": row.no_fill_bundle_hash,
        "no_fill_row_hash": row.no_fill_row_hash,
        "no_pnl_policy_hash": row.no_pnl_policy_hash,
        "order_kind": row.order_kind,
        "order_quantity": row.order_quantity,
        "pnl_amount": row.pnl_amount,
        "pnl_currency": row.pnl_currency,
        "pnl_provenance": row.pnl_provenance,
        "pnl_required": row.pnl_required,
        "pnl_rows_emitted": row.pnl_rows_emitted,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "result_interpretation_emitted": row.result_interpretation_emitted,
        "row_status": row.row_status,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "transition_kind": row.transition_kind,
    }


def _no_pnl_bundle_hash_payload(bundle: NoPnlExecutableBundle) -> dict[str, object]:
    return {
        "actual_backtest_result_emitted": bundle.actual_backtest_result_emitted,
        "actual_pnl_rows_emitted": bundle.actual_pnl_rows_emitted,
        "actual_result_rows_emitted": bundle.actual_result_rows_emitted,
        "artifact": "S27_V2_NO_PNL_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "no_cost_bundle_hash": bundle.no_cost_bundle.bundle_hash,
        "no_pnl_metadata_rows_emitted": bundle.no_pnl_metadata_rows_emitted,
        "no_pnl_row_hash": bundle.no_pnl_row.row_hash,
        "non_authorizations": bundle.non_authorizations,
        "result_interpretation_emitted": bundle.result_interpretation_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
    }

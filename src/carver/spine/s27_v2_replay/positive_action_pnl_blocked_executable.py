from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .positive_action_cost_executable import (
    ACTUAL_COST_LEDGER_STATUS,
    INFERRED_RETAIL_COST_STATUS,
    NUMERIC_COST_POLICY_STATUS,
    NOT_APPLICABLE,
    PositiveActionCostExecutableBundle,
    build_positive_action_cost_executable,
)
from .positive_action_executable import EXPECTED_RAW_SYMBOL, EXPECTED_SELECTED_FILL, POSITIVE_ACTION_PACK_RELATIVE_PATH
from .validation import require_finite_number, require_hash, require_integer, require_text


S27_V2_POSITIVE_ACTION_PNL_BLOCKED_AUTHORIZATION = "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_PNL_BLOCKED_METADATA"
S27_V2_POSITIVE_ACTION_PNL_BLOCKED_STATUS = "S27_V2_POSITIVE_ACTION_PNL_BLOCKED_METADATA_NOT_RESULT"

PNL_BLOCKED_ROW_STATUS = "LOCAL_POSITIVE_ACTION_PNL_ACCOUNTING_REQUIRED_BUT_BLOCKED"
PNL_BLOCKED_REASON_CODE = "S27_POSITIVE_ACTION_FILLED_POSITION_PNL_BLOCKED_BY_COST_AND_VALUATION_POLICY"

PNL_ACCOUNTING_REQUIRED_LABEL = "PNL_ACCOUNTING_REQUIRED_BY_FILLED_POSITION"
VALUATION_END_MARK_POLICY_STATUS = "FAIL_CLOSED_VALUATION_END_MARK_POLICY_UNRESOLVED"
ACTUAL_PNL_LEDGER_STATUS = "FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED_COST_AND_VALUATION_UNRESOLVED"
RESULT_EMISSION_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
BACKTEST_RESULT_STATUS = "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()

PNL_BLOCKED_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_ACTUAL_COST_EMISSION",
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


@dataclass(frozen=True)
class PositiveActionPnlBlockedMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    cost_bundle_hash: str
    cost_evidence_row_hash: str
    fill_bundle_hash: str
    limit_fill_row_hash: str
    input_pack_path: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    fill_quantity: int
    fill_price: float
    position_before_fill: int
    position_after_fill: int
    pnl_accounting_required_label: str
    pnl_accounting_required_by_filled_position: bool
    numeric_cost_policy_status: str
    inferred_retail_cost_status: str
    actual_cost_ledger_status: str
    actual_cost_rows_emitted: bool
    valuation_end_mark_policy_status: str
    actual_pnl_ledger_status: str
    actual_pnl_rows_emitted: bool
    pnl_rows_emitted: bool
    result_emission_status: str
    result_rows_emitted: bool
    backtest_result_status: str
    backtest_result_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    pnl_amount: str
    pnl_currency: str
    pnl_blocked_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action PnL-blocked row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_against_cost(self, cost_bundle: PositiveActionCostExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_PNL_BLOCKED_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 positive-action PnL-blocked ledger label is not locked")
        if self.row_status != PNL_BLOCKED_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked row status is not locked")
        if self.reason_code != PNL_BLOCKED_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked reason code is not locked")
        for name, hash_value in (
            ("cost bundle", self.cost_bundle_hash),
            ("cost evidence row", self.cost_evidence_row_hash),
            ("fill bundle", self.fill_bundle_hash),
            ("limit fill row", self.limit_fill_row_hash),
            ("PnL-blocked policy", self.pnl_blocked_policy_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action PnL-blocked {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("PnL accounting required label", self.pnl_accounting_required_label),
            ("numeric cost policy status", self.numeric_cost_policy_status),
            ("inferred retail cost status", self.inferred_retail_cost_status),
            ("actual cost ledger status", self.actual_cost_ledger_status),
            ("valuation end-mark policy status", self.valuation_end_mark_policy_status),
            ("actual PnL ledger status", self.actual_pnl_ledger_status),
            ("result emission status", self.result_emission_status),
            ("backtest result status", self.backtest_result_status),
            ("PnL amount", self.pnl_amount),
            ("PnL currency", self.pnl_currency),
        ):
            require_text(f"S27 v2 positive-action PnL-blocked {name}", value)
        for name, value in (
            ("fill quantity", self.fill_quantity),
            ("position before fill", self.position_before_fill),
            ("position after fill", self.position_after_fill),
        ):
            require_integer(f"S27 v2 positive-action PnL-blocked {name}", value)
        require_finite_number("S27 v2 positive-action PnL-blocked fill price", self.fill_price)
        self._validate_locked_identity(cost_bundle)
        self._validate_blocked_policy()
        if self.row_hash != canonical_sha256(_pnl_blocked_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action PnL-blocked row hash must be content-bound")

    def _validate_locked_identity(self, cost_bundle: PositiveActionCostExecutableBundle) -> None:
        cost_row = cost_bundle.cost_evidence_row
        fill_bundle = cost_bundle.fill_bundle
        fill_row = fill_bundle.limit_fill_row
        if self.cost_bundle_hash != cost_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked metadata must bind active cost bundle")
        if self.cost_evidence_row_hash != cost_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked metadata must bind active cost row")
        if self.fill_bundle_hash != fill_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked metadata must bind active fill bundle")
        if self.limit_fill_row_hash != fill_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked metadata must bind active limit-fill row")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked metadata is locked to the positive-action pack")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked fill timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked raw symbol is not locked")
        if self.fill_quantity != fill_row.filled_order_quantity:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked fill quantity must bind fill row")
        if self.fill_price != fill_row.fill_price:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked fill price must bind fill row")
        if self.position_before_fill != fill_row.position_before_fill:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked position-before must bind fill row")
        if self.position_after_fill != fill_row.position_after_fill:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked position-after must bind fill row")
        if self.actual_cost_ledger_status != cost_row.actual_cost_ledger_status:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked cost status must bind cost row")
        if self.numeric_cost_policy_status != cost_row.numeric_cost_policy_status:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked numeric cost status must bind cost row")
        if self.inferred_retail_cost_status != cost_row.inferred_retail_cost_status:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked inferred cost status must bind cost row")
        if self.actual_cost_rows_emitted != cost_row.actual_cost_rows_emitted:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked actual-cost flag must bind cost row")

    def _validate_blocked_policy(self) -> None:
        if self.pnl_accounting_required_label != PNL_ACCOUNTING_REQUIRED_LABEL:
            raise CarverBlocked("S27 v2 positive-action PnL accounting-required label is not locked")
        if self.pnl_accounting_required_by_filled_position is not True:
            raise CarverBlocked("S27 v2 positive-action filled position requires PnL accounting")
        if self.numeric_cost_policy_status != NUMERIC_COST_POLICY_STATUS:
            raise CarverBlocked("S27 v2 positive-action numeric cost policy must remain unresolved")
        if self.inferred_retail_cost_status != INFERRED_RETAIL_COST_STATUS:
            raise CarverBlocked("S27 v2 positive-action inferred retail cost must remain not accepted")
        if self.actual_cost_ledger_status != ACTUAL_COST_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual cost ledger must remain fail-closed")
        if self.actual_cost_rows_emitted is not False:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked metadata cannot emit actual cost rows")
        if self.valuation_end_mark_policy_status != VALUATION_END_MARK_POLICY_STATUS:
            raise CarverBlocked("S27 v2 positive-action valuation/end-mark policy must remain unresolved")
        if self.actual_pnl_ledger_status != ACTUAL_PNL_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual PnL ledger status must remain fail-closed")
        if any(
            flag is not False
            for flag in (
                self.actual_pnl_rows_emitted,
                self.pnl_rows_emitted,
                self.result_rows_emitted,
                self.backtest_result_emitted,
                self.result_interpretation_emitted,
                self.pnl_evaluation_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action PnL-blocked metadata cannot emit PnL/result/evidence")
        if self.result_emission_status != RESULT_EMISSION_STATUS:
            raise CarverBlocked("S27 v2 positive-action result emission status must remain fail-closed")
        if self.backtest_result_status != BACKTEST_RESULT_STATUS:
            raise CarverBlocked("S27 v2 positive-action backtest result status must remain fail-closed")
        if self.pnl_amount != NOT_APPLICABLE or self.pnl_currency != NOT_APPLICABLE:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked metadata must not carry PnL amount/currency")
        if self.pnl_blocked_policy_hash != _policy_hash(
            "positive_action_pnl_blocked_policy",
            self.pnl_accounting_required_label,
            self.pnl_accounting_required_by_filled_position,
            self.numeric_cost_policy_status,
            self.inferred_retail_cost_status,
            self.actual_cost_ledger_status,
            self.actual_cost_rows_emitted,
            self.valuation_end_mark_policy_status,
            self.actual_pnl_ledger_status,
            self.result_emission_status,
            self.backtest_result_status,
            self.pnl_amount,
            self.pnl_currency,
        ):
            raise CarverBlocked("S27 v2 positive-action PnL-blocked policy hash must bind blocked policy")


@dataclass(frozen=True)
class PositiveActionPnlBlockedExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    cost_bundle: PositiveActionCostExecutableBundle
    pnl_blocked_row: PositiveActionPnlBlockedMetadataRow
    pnl_blocked_metadata_rows_emitted: bool
    actual_cost_rows_emitted: bool
    actual_pnl_rows_emitted: bool
    result_rows_emitted: bool
    backtest_result_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = PNL_BLOCKED_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_PNL_BLOCKED_STATUS:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked bundle status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_PNL_BLOCKED_AUTHORIZATION:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked lane must remain source-native futures")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked is locked to the declared positive-action pack")
        active_cost = build_positive_action_cost_executable(_POSITIVE_ACTION_PACK_PATH)
        self.cost_bundle.validate()
        if self.cost_bundle != active_cost:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked must bind active cost bundle")
        self.pnl_blocked_row._validate_against_cost(active_cost)
        active_row = _build_active_pnl_blocked_row(_POSITIVE_ACTION_PACK_PATH, active_cost)
        if self.pnl_blocked_row != active_row:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked row must match active local evidence")
        if any(
            flag is not True
            for flag in (
                self.pnl_blocked_metadata_rows_emitted,
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action PnL-blocked must emit only authorized metadata")
        if any(
            flag is not False
            for flag in (
                self.actual_cost_rows_emitted,
                self.actual_pnl_rows_emitted,
                self.result_rows_emitted,
                self.backtest_result_emitted,
                self.result_interpretation_emitted,
                self.pnl_evaluation_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action PnL-blocked cannot emit cost/PnL/result/evidence")
        if self.non_authorizations != PNL_BLOCKED_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 positive-action PnL-blocked must preserve non-authorizations")
        require_hash("S27 v2 positive-action PnL-blocked bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_pnl_blocked_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action PnL-blocked bundle hash must be content-bound")


def build_positive_action_pnl_blocked_metadata(
    input_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
) -> PositiveActionPnlBlockedExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action PnL-blocked is locked to the declared positive-action pack")
    cost_bundle = build_positive_action_cost_executable(pack_path)
    pnl_row = _build_active_pnl_blocked_row(pack_path, cost_bundle)
    bundle = PositiveActionPnlBlockedExecutableBundle(
        status=S27_V2_POSITIVE_ACTION_PNL_BLOCKED_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_PNL_BLOCKED_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        cost_bundle=cost_bundle,
        pnl_blocked_row=pnl_row,
        pnl_blocked_metadata_rows_emitted=True,
        actual_cost_rows_emitted=False,
        actual_pnl_rows_emitted=False,
        result_rows_emitted=False,
        backtest_result_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionPnlBlockedExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_pnl_blocked_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_pnl_blocked_row(
    pack_path: Path,
    cost_bundle: PositiveActionCostExecutableBundle,
) -> PositiveActionPnlBlockedMetadataRow:
    cost_row = cost_bundle.cost_evidence_row
    fill_bundle = cost_bundle.fill_bundle
    fill_row = fill_bundle.limit_fill_row
    row = PositiveActionPnlBlockedMetadataRow(
        ledger_label="POSITIVE_ACTION_PNL_BLOCKED_METADATA_LEDGER",
        row_status=PNL_BLOCKED_ROW_STATUS,
        reason_code=PNL_BLOCKED_REASON_CODE,
        cost_bundle_hash=cost_bundle.bundle_hash,
        cost_evidence_row_hash=cost_row.row_hash,
        fill_bundle_hash=fill_bundle.bundle_hash,
        limit_fill_row_hash=fill_row.row_hash,
        input_pack_path=str(pack_path),
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        fill_quantity=fill_row.filled_order_quantity,
        fill_price=fill_row.fill_price,
        position_before_fill=fill_row.position_before_fill,
        position_after_fill=fill_row.position_after_fill,
        pnl_accounting_required_label=PNL_ACCOUNTING_REQUIRED_LABEL,
        pnl_accounting_required_by_filled_position=True,
        numeric_cost_policy_status=cost_row.numeric_cost_policy_status,
        inferred_retail_cost_status=cost_row.inferred_retail_cost_status,
        actual_cost_ledger_status=cost_row.actual_cost_ledger_status,
        actual_cost_rows_emitted=cost_row.actual_cost_rows_emitted,
        valuation_end_mark_policy_status=VALUATION_END_MARK_POLICY_STATUS,
        actual_pnl_ledger_status=ACTUAL_PNL_LEDGER_STATUS,
        actual_pnl_rows_emitted=False,
        pnl_rows_emitted=False,
        result_emission_status=RESULT_EMISSION_STATUS,
        result_rows_emitted=False,
        backtest_result_status=BACKTEST_RESULT_STATUS,
        backtest_result_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        pnl_amount=NOT_APPLICABLE,
        pnl_currency=NOT_APPLICABLE,
        pnl_blocked_policy_hash=_policy_hash(
            "positive_action_pnl_blocked_policy",
            PNL_ACCOUNTING_REQUIRED_LABEL,
            True,
            cost_row.numeric_cost_policy_status,
            cost_row.inferred_retail_cost_status,
            cost_row.actual_cost_ledger_status,
            cost_row.actual_cost_rows_emitted,
            VALUATION_END_MARK_POLICY_STATUS,
            ACTUAL_PNL_LEDGER_STATUS,
            RESULT_EMISSION_STATUS,
            BACKTEST_RESULT_STATUS,
            NOT_APPLICABLE,
            NOT_APPLICABLE,
        ),
        row_hash="0" * 64,
    )
    row = PositiveActionPnlBlockedMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_pnl_blocked_row_hash_payload(row))}
    )
    row._validate_against_cost(cost_bundle)
    return row


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_PNL_BLOCKED_POLICY", "label": label, "values": values})


def _pnl_blocked_row_hash_payload(row: PositiveActionPnlBlockedMetadataRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _pnl_blocked_bundle_hash_payload(bundle: PositiveActionPnlBlockedExecutableBundle) -> dict[str, object]:
    return {
        "actual_cost_rows_emitted": bundle.actual_cost_rows_emitted,
        "actual_pnl_rows_emitted": bundle.actual_pnl_rows_emitted,
        "artifact": "S27_V2_POSITIVE_ACTION_PNL_BLOCKED_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "backtest_result_emitted": bundle.backtest_result_emitted,
        "cost_bundle_hash": bundle.cost_bundle.bundle_hash,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "pnl_blocked_metadata_rows_emitted": bundle.pnl_blocked_metadata_rows_emitted,
        "pnl_blocked_row_hash": bundle.pnl_blocked_row.row_hash,
        "pnl_evaluation_emitted": bundle.pnl_evaluation_emitted,
        "provenance_metadata_rows_emitted": bundle.provenance_metadata_rows_emitted,
        "result_interpretation_emitted": bundle.result_interpretation_emitted,
        "result_rows_emitted": bundle.result_rows_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "trusted_bundle_metadata_emitted": bundle.trusted_bundle_metadata_emitted,
        "validation_metadata_rows_emitted": bundle.validation_metadata_rows_emitted,
    }

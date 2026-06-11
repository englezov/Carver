from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .positive_action_cost_executable import (
    LIMIT_FILL_COST_TREATMENT_LABEL,
    PROP_CFD_ADAPTER_COST_REJECTION_LABEL,
    SOURCE_COST_TREATMENT_LABEL,
    _cost_parameter_row_hash,
    _policy_hash as cost_policy_hash,
    _verify_cost_parameter_file_hash,
)
from .positive_action_executable import EXPECTED_RAW_SYMBOL, EXPECTED_SELECTED_FILL, POSITIVE_ACTION_PACK_RELATIVE_PATH
from .positive_action_fill_executable import (
    FILL_PRICE_PROVENANCE,
    PositiveActionFillExecutableBundle,
    build_positive_action_fill_executable,
)
from .validation import require_finite_number, require_hash, require_integer, require_positive_number, require_text


S27_V2_POSITIVE_ACTION_ACTUAL_COST_AUTHORIZATION = (
    "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_ACTUAL_COST_LEDGER_ACCEPTED_INFERRED_RETAIL_COST"
)
S27_V2_POSITIVE_ACTION_ACTUAL_COST_STATUS = (
    "S27_V2_POSITIVE_ACTION_ACTUAL_COST_LEDGER_EMITTED_NOT_PNL_NOT_RESULT"
)

ACTUAL_COST_ROW_STATUS = "LOCAL_POSITIVE_ACTION_ACTUAL_COST_LEDGER_ROW_EMITTED_NOT_PNL_NOT_RESULT"
ACTUAL_COST_REASON_CODE = "S27_POSITIVE_ACTION_LIMIT_FILL_COMMISSION_ONLY_ACCEPTED_INFERRED_RETAIL_COST"

ACCEPTED_COST_POLICY_LABEL = "NINJATRADER_FREE_PLAN_ALL_IN_ZN_2_30_USD_PER_CONTRACT_PER_SIDE"
ACCEPTED_COST_CLASSIFICATION = "SOURCE_NATIVE_INFERRED_RETAIL_FUTURES_COSTS"
REJECTED_COST_CLASSIFICATION = "BOOK_EXPLICIT_COSTS"
ACCEPTED_COMMISSION_PER_CONTRACT = 2.30
ACCEPTED_COMMISSION_UNIT = "USD_PER_CONTRACT_PER_SIDE_ALL_IN_RETAIL_FUTURES_TRANSACTION_FEE"
ACCEPTED_COST_DECISION_BLOCK_SHA256 = "68cfd732aa2b38ef0aa88c686690ad98c25bf3a1a597835bf706a6354eaefa58"
VALUATION_FAIL_CLOSED_DECISION_BLOCK_SHA256 = "580a20ac566b48e0591bf55100bb47d24aca6dea6a0b4260650f0eb0056c1b7d"

NO_SPREAD_COST_REASON = "LIMIT_FILL_NO_MARKET_SPREAD_COST_BY_SOURCE_LOCK"
PNL_LEDGER_STATUS = "FAIL_CLOSED_VALUATION_END_MARK_POLICY_NOT_SOURCE_LOCKED"
RESULT_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
BACKTEST_STATUS = "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()
_ACCEPTANCE_RECORD_PATH = (
    _REPO_ROOT
    / "docs"
    / "process"
    / "CARVER_S27_ZN_V2_INFERRED_RETAIL_COST_ACCEPTANCE_AND_VALUATION_SOURCE_LOCK_GATE_2026-06-09.md"
).resolve()
_EXPECTED_ACCEPTANCE_RECORD_SHA256 = "fe3bde381260c5e9022ab52632d0aff73133293835676baa205bf916690a005d"

ACTUAL_COST_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
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
class PositiveActionActualCostLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    fill_bundle_hash: str
    limit_fill_row_hash: str
    input_pack_path: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    fill_price: float
    fill_quantity: int
    fill_price_provenance: str
    cost_parameter_file_hash: str
    cost_parameter_row_hash: str
    accepted_cost_policy_label: str
    accepted_cost_policy_hash: str
    accepted_cost_decision_record_hash: str
    accepted_cost_decision_block_sha256: str
    cost_classification: str
    rejected_cost_classification: str
    commission_per_contract: float
    commission_unit: str
    commission_amount: float
    spread_cost_amount: float
    spread_cost_reason: str
    total_cost_amount: float
    total_cost_currency: str
    source_cost_treatment_label: str
    source_cost_treatment_hash: str
    limit_fill_cost_treatment_label: str
    limit_fill_cost_treatment_hash: str
    prop_cfd_adapter_cost_rejection_label: str
    prop_cfd_adapter_cost_rejection_hash: str
    valuation_fail_closed_decision_block_sha256: str
    pnl_ledger_status: str
    result_status: str
    backtest_status: str
    pnl_rows_emitted: bool
    result_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action actual cost row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_against_fill(self, fill_bundle: PositiveActionFillExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_ACTUAL_COST_LEDGER":
            raise CarverBlocked("S27 v2 positive-action actual cost ledger label is not locked")
        if self.row_status != ACTUAL_COST_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual cost row status is not locked")
        if self.reason_code != ACTUAL_COST_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action actual cost reason code is not locked")
        for name, hash_value in (
            ("fill bundle", self.fill_bundle_hash),
            ("limit fill row", self.limit_fill_row_hash),
            ("cost parameter file", self.cost_parameter_file_hash),
            ("cost parameter row", self.cost_parameter_row_hash),
            ("accepted cost policy", self.accepted_cost_policy_hash),
            ("accepted cost decision record", self.accepted_cost_decision_record_hash),
            ("accepted cost decision block", self.accepted_cost_decision_block_sha256),
            ("source cost treatment", self.source_cost_treatment_hash),
            ("limit fill treatment", self.limit_fill_cost_treatment_hash),
            ("prop/CFD/adapter cost rejection", self.prop_cfd_adapter_cost_rejection_hash),
            ("valuation fail-closed decision block", self.valuation_fail_closed_decision_block_sha256),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action actual cost {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("fill price provenance", self.fill_price_provenance),
            ("accepted cost policy label", self.accepted_cost_policy_label),
            ("cost classification", self.cost_classification),
            ("rejected cost classification", self.rejected_cost_classification),
            ("commission unit", self.commission_unit),
            ("spread cost reason", self.spread_cost_reason),
            ("total cost currency", self.total_cost_currency),
            ("source cost treatment label", self.source_cost_treatment_label),
            ("limit fill cost treatment label", self.limit_fill_cost_treatment_label),
            ("prop/CFD/adapter cost rejection label", self.prop_cfd_adapter_cost_rejection_label),
            ("PnL ledger status", self.pnl_ledger_status),
            ("result status", self.result_status),
            ("backtest status", self.backtest_status),
        ):
            require_text(f"S27 v2 positive-action actual cost {name}", value)
        require_integer("S27 v2 positive-action actual cost fill quantity", self.fill_quantity)
        require_positive_number("S27 v2 positive-action actual cost fill price", self.fill_price)
        require_positive_number("S27 v2 positive-action commission per contract", self.commission_per_contract)
        for name, amount in (
            ("commission amount", self.commission_amount),
            ("spread cost amount", self.spread_cost_amount),
            ("total cost amount", self.total_cost_amount),
        ):
            require_finite_number(f"S27 v2 positive-action actual cost {name}", amount)
        self._validate_locked_identity(fill_bundle)
        self._validate_policy_and_arithmetic()
        if self.row_hash != canonical_sha256(_actual_cost_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action actual cost row hash must be content-bound")

    def _validate_locked_identity(self, fill_bundle: PositiveActionFillExecutableBundle) -> None:
        fill_row = fill_bundle.limit_fill_row
        if self.fill_bundle_hash != fill_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action actual cost must bind active fill bundle")
        if self.limit_fill_row_hash != fill_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action actual cost must bind active limit fill row")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action actual cost is locked to the positive-action pack")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action actual cost fill timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 positive-action actual cost raw symbol is not locked")
        if self.fill_price != fill_row.fill_price:
            raise CarverBlocked("S27 v2 positive-action actual cost fill price must bind limit fill")
        if self.fill_quantity != fill_row.filled_order_quantity:
            raise CarverBlocked("S27 v2 positive-action actual cost fill quantity must bind limit fill")
        if self.fill_price_provenance != FILL_PRICE_PROVENANCE:
            raise CarverBlocked("S27 v2 positive-action actual cost fill provenance is not locked")
        if self.cost_parameter_file_hash != _verify_cost_parameter_file_hash(_POSITIVE_ACTION_PACK_PATH):
            raise CarverBlocked("S27 v2 positive-action actual cost parameter file hash mismatch")
        if self.cost_parameter_row_hash != _cost_parameter_row_hash(_POSITIVE_ACTION_PACK_PATH):
            raise CarverBlocked("S27 v2 positive-action actual cost must bind active cost parameter row")

    def _validate_policy_and_arithmetic(self) -> None:
        if self.accepted_cost_policy_label != ACCEPTED_COST_POLICY_LABEL:
            raise CarverBlocked("S27 v2 positive-action actual cost accepted policy label is not locked")
        if self.accepted_cost_policy_hash != _accepted_cost_policy_hash():
            raise CarverBlocked("S27 v2 positive-action actual cost policy hash must bind accepted inferred cost")
        if self.accepted_cost_decision_record_hash != _verify_acceptance_record_hash():
            raise CarverBlocked("S27 v2 positive-action actual cost must bind accepted cost decision record")
        if self.accepted_cost_decision_block_sha256 != ACCEPTED_COST_DECISION_BLOCK_SHA256:
            raise CarverBlocked("S27 v2 positive-action actual cost decision block hash is not locked")
        if self.cost_classification != ACCEPTED_COST_CLASSIFICATION:
            raise CarverBlocked("S27 v2 positive-action actual cost must be inferred retail futures cost")
        if self.rejected_cost_classification != REJECTED_COST_CLASSIFICATION:
            raise CarverBlocked("S27 v2 positive-action actual cost must not be book-explicit cost")
        if self.commission_per_contract != ACCEPTED_COMMISSION_PER_CONTRACT:
            raise CarverBlocked("S27 v2 positive-action actual cost commission per contract is not locked")
        if self.commission_unit != ACCEPTED_COMMISSION_UNIT:
            raise CarverBlocked("S27 v2 positive-action actual cost commission unit is not locked")
        expected_commission = ACCEPTED_COMMISSION_PER_CONTRACT * abs(self.fill_quantity)
        if self.commission_amount != expected_commission:
            raise CarverBlocked("S27 v2 positive-action commission amount must equal 2.30 times absolute fill quantity")
        if self.spread_cost_amount != 0.0:
            raise CarverBlocked("S27 v2 positive-action limit fill spread cost must be zero")
        if self.spread_cost_reason != NO_SPREAD_COST_REASON:
            raise CarverBlocked("S27 v2 positive-action limit fill spread-cost reason is not locked")
        if self.total_cost_amount != self.commission_amount + self.spread_cost_amount:
            raise CarverBlocked("S27 v2 positive-action total cost must equal commission plus spread cost")
        if self.total_cost_currency != "USD":
            raise CarverBlocked("S27 v2 positive-action actual cost currency must be USD")
        if self.source_cost_treatment_label != SOURCE_COST_TREATMENT_LABEL:
            raise CarverBlocked("S27 v2 positive-action source cost treatment label is not locked")
        if self.source_cost_treatment_hash != cost_policy_hash(
            "source_cost_treatment",
            SOURCE_COST_TREATMENT_LABEL,
            "COMMISSION_FOR_ALL_ORDERS",
            self.accepted_cost_policy_hash,
        ):
            raise CarverBlocked("S27 v2 positive-action source cost treatment hash must bind accepted policy")
        if self.limit_fill_cost_treatment_label != LIMIT_FILL_COST_TREATMENT_LABEL:
            raise CarverBlocked("S27 v2 positive-action limit-fill cost treatment label is not locked")
        if self.limit_fill_cost_treatment_hash != cost_policy_hash(
            "limit_fill_cost_treatment",
            LIMIT_FILL_COST_TREATMENT_LABEL,
            "COMMISSION_ONLY",
            self.limit_fill_row_hash,
            self.accepted_cost_policy_hash,
        ):
            raise CarverBlocked("S27 v2 positive-action limit-fill cost treatment hash must bind fill and accepted policy")
        if self.prop_cfd_adapter_cost_rejection_label != PROP_CFD_ADAPTER_COST_REJECTION_LABEL:
            raise CarverBlocked("S27 v2 positive-action cost rejection label is not locked")
        if self.prop_cfd_adapter_cost_rejection_hash != cost_policy_hash(
            "cost_rejection",
            PROP_CFD_ADAPTER_COST_REJECTION_LABEL,
            "NO_PROP_FIRM_FEES",
            "NO_CFD_SPREADS_OR_SWAPS",
            "NO_ADAPTER_OR_PERSONAL_TRADING_COSTS",
            self.accepted_cost_policy_hash,
        ):
            raise CarverBlocked("S27 v2 positive-action cost rejection hash must bind accepted policy")
        if self.valuation_fail_closed_decision_block_sha256 != VALUATION_FAIL_CLOSED_DECISION_BLOCK_SHA256:
            raise CarverBlocked("S27 v2 positive-action actual cost must bind valuation fail-closed decision")
        if self.pnl_ledger_status != PNL_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual cost must keep PnL fail-closed")
        if self.result_status != RESULT_STATUS or self.backtest_status != BACKTEST_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual cost must keep result/backtest fail-closed")
        if any(
            flag is not False
            for flag in (
                self.pnl_rows_emitted,
                self.result_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action actual cost cannot emit PnL/result/evidence")


@dataclass(frozen=True)
class PositiveActionActualCostExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    fill_bundle: PositiveActionFillExecutableBundle
    actual_cost_row: PositiveActionActualCostLedgerRow
    actual_commission_rows_emitted: bool
    actual_spread_cost_rows_emitted: bool
    actual_cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = ACTUAL_COST_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_ACTUAL_COST_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual cost bundle status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_ACTUAL_COST_AUTHORIZATION:
            raise CarverBlocked("S27 v2 positive-action actual cost authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 positive-action actual cost must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 positive-action actual cost lane must remain source-native futures")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action actual cost is locked to the positive-action pack")
        active_fill = build_positive_action_fill_executable(_POSITIVE_ACTION_PACK_PATH)
        self.fill_bundle.validate()
        if self.fill_bundle != active_fill:
            raise CarverBlocked("S27 v2 positive-action actual cost must bind active fill bundle")
        self.actual_cost_row._validate_against_fill(active_fill)
        active_cost_row = _build_active_actual_cost_row(_POSITIVE_ACTION_PACK_PATH, active_fill)
        if self.actual_cost_row != active_cost_row:
            raise CarverBlocked("S27 v2 positive-action actual cost row must match active local evidence")
        if any(
            flag is not True
            for flag in (
                self.actual_commission_rows_emitted,
                self.actual_cost_rows_emitted,
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action actual cost must emit authorized cost/metadata rows")
        if self.actual_spread_cost_rows_emitted is not False:
            raise CarverBlocked("S27 v2 positive-action limit fill must not emit spread cost rows")
        if any(
            flag is not False
            for flag in (
                self.pnl_rows_emitted,
                self.result_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action actual cost cannot emit PnL/result/evidence")
        if self.non_authorizations != ACTUAL_COST_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 positive-action actual cost must preserve non-authorizations")
        require_hash("S27 v2 positive-action actual cost bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_actual_cost_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action actual cost bundle hash must be content-bound")


def build_positive_action_actual_cost_executable(
    input_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
) -> PositiveActionActualCostExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action actual cost is locked to the declared positive-action pack")
    fill_bundle = build_positive_action_fill_executable(pack_path)
    actual_cost_row = _build_active_actual_cost_row(pack_path, fill_bundle)
    bundle = PositiveActionActualCostExecutableBundle(
        status=S27_V2_POSITIVE_ACTION_ACTUAL_COST_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_ACTUAL_COST_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        fill_bundle=fill_bundle,
        actual_cost_row=actual_cost_row,
        actual_commission_rows_emitted=True,
        actual_spread_cost_rows_emitted=False,
        actual_cost_rows_emitted=True,
        pnl_rows_emitted=False,
        result_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionActualCostExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_actual_cost_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_actual_cost_row(
    pack_path: Path,
    fill_bundle: PositiveActionFillExecutableBundle,
) -> PositiveActionActualCostLedgerRow:
    fill_row = fill_bundle.limit_fill_row
    accepted_cost_policy_hash = _accepted_cost_policy_hash()
    row = PositiveActionActualCostLedgerRow(
        ledger_label="POSITIVE_ACTION_ACTUAL_COST_LEDGER",
        row_status=ACTUAL_COST_ROW_STATUS,
        reason_code=ACTUAL_COST_REASON_CODE,
        fill_bundle_hash=fill_bundle.bundle_hash,
        limit_fill_row_hash=fill_row.row_hash,
        input_pack_path=str(pack_path),
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        fill_price=fill_row.fill_price,
        fill_quantity=fill_row.filled_order_quantity,
        fill_price_provenance=FILL_PRICE_PROVENANCE,
        cost_parameter_file_hash=_verify_cost_parameter_file_hash(pack_path),
        cost_parameter_row_hash=_cost_parameter_row_hash(pack_path),
        accepted_cost_policy_label=ACCEPTED_COST_POLICY_LABEL,
        accepted_cost_policy_hash=accepted_cost_policy_hash,
        accepted_cost_decision_record_hash=_verify_acceptance_record_hash(),
        accepted_cost_decision_block_sha256=ACCEPTED_COST_DECISION_BLOCK_SHA256,
        cost_classification=ACCEPTED_COST_CLASSIFICATION,
        rejected_cost_classification=REJECTED_COST_CLASSIFICATION,
        commission_per_contract=ACCEPTED_COMMISSION_PER_CONTRACT,
        commission_unit=ACCEPTED_COMMISSION_UNIT,
        commission_amount=ACCEPTED_COMMISSION_PER_CONTRACT * abs(fill_row.filled_order_quantity),
        spread_cost_amount=0.0,
        spread_cost_reason=NO_SPREAD_COST_REASON,
        total_cost_amount=ACCEPTED_COMMISSION_PER_CONTRACT * abs(fill_row.filled_order_quantity),
        total_cost_currency="USD",
        source_cost_treatment_label=SOURCE_COST_TREATMENT_LABEL,
        source_cost_treatment_hash=cost_policy_hash(
            "source_cost_treatment",
            SOURCE_COST_TREATMENT_LABEL,
            "COMMISSION_FOR_ALL_ORDERS",
            accepted_cost_policy_hash,
        ),
        limit_fill_cost_treatment_label=LIMIT_FILL_COST_TREATMENT_LABEL,
        limit_fill_cost_treatment_hash=cost_policy_hash(
            "limit_fill_cost_treatment",
            LIMIT_FILL_COST_TREATMENT_LABEL,
            "COMMISSION_ONLY",
            fill_row.row_hash,
            accepted_cost_policy_hash,
        ),
        prop_cfd_adapter_cost_rejection_label=PROP_CFD_ADAPTER_COST_REJECTION_LABEL,
        prop_cfd_adapter_cost_rejection_hash=cost_policy_hash(
            "cost_rejection",
            PROP_CFD_ADAPTER_COST_REJECTION_LABEL,
            "NO_PROP_FIRM_FEES",
            "NO_CFD_SPREADS_OR_SWAPS",
            "NO_ADAPTER_OR_PERSONAL_TRADING_COSTS",
            accepted_cost_policy_hash,
        ),
        valuation_fail_closed_decision_block_sha256=VALUATION_FAIL_CLOSED_DECISION_BLOCK_SHA256,
        pnl_ledger_status=PNL_LEDGER_STATUS,
        result_status=RESULT_STATUS,
        backtest_status=BACKTEST_STATUS,
        pnl_rows_emitted=False,
        result_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        row_hash="0" * 64,
    )
    row = PositiveActionActualCostLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_actual_cost_row_hash_payload(row))}
    )
    row._validate_against_fill(fill_bundle)
    return row


def _verify_acceptance_record_hash() -> str:
    observed = sha256(_ACCEPTANCE_RECORD_PATH.read_bytes()).hexdigest()
    if observed != _EXPECTED_ACCEPTANCE_RECORD_SHA256:
        raise CarverBlocked("S27 v2 positive-action actual cost acceptance record hash is not pinned")
    return observed


def _accepted_cost_policy_hash() -> str:
    return canonical_sha256(
        {
            "accepted_cost_decision_block_sha256": ACCEPTED_COST_DECISION_BLOCK_SHA256,
            "artifact": "S27_V2_ACCEPTED_INFERRED_RETAIL_COST_POLICY",
            "classification": ACCEPTED_COST_CLASSIFICATION,
            "commission_per_contract": ACCEPTED_COMMISSION_PER_CONTRACT,
            "commission_unit": ACCEPTED_COMMISSION_UNIT,
            "label": ACCEPTED_COST_POLICY_LABEL,
            "not_classification": REJECTED_COST_CLASSIFICATION,
        }
    )


def _actual_cost_row_hash_payload(row: PositiveActionActualCostLedgerRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _actual_cost_bundle_hash_payload(bundle: PositiveActionActualCostExecutableBundle) -> dict[str, object]:
    return {
        "actual_commission_rows_emitted": bundle.actual_commission_rows_emitted,
        "actual_cost_row_hash": bundle.actual_cost_row.row_hash,
        "actual_cost_rows_emitted": bundle.actual_cost_rows_emitted,
        "actual_spread_cost_rows_emitted": bundle.actual_spread_cost_rows_emitted,
        "artifact": "S27_V2_POSITIVE_ACTION_ACTUAL_COST_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "fill_bundle_hash": bundle.fill_bundle.bundle_hash,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "provenance_metadata_rows_emitted": bundle.provenance_metadata_rows_emitted,
        "result_rows_emitted": bundle.result_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "trusted_bundle_metadata_emitted": bundle.trusted_bundle_metadata_emitted,
        "validation_metadata_rows_emitted": bundle.validation_metadata_rows_emitted,
    }

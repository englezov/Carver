from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .positive_action_executable import EXPECTED_RAW_SYMBOL, EXPECTED_SELECTED_FILL, POSITIVE_ACTION_PACK_RELATIVE_PATH
from .positive_action_fill_executable import (
    PositiveActionFillExecutableBundle,
    build_positive_action_fill_executable,
)
from .positive_action_order_plan_executable import _read_pack_rows, _row_hashes_by_file
from .validation import require_finite_number, require_hash, require_integer, require_text


S27_V2_POSITIVE_ACTION_COST_AUTHORIZATION = "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_COST_POLICY_EVIDENCE"
S27_V2_POSITIVE_ACTION_COST_STATUS = "S27_V2_POSITIVE_ACTION_COST_POLICY_FAIL_CLOSED_NOT_PNL_NOT_RESULT"

COST_EVIDENCE_ROW_STATUS = "LOCAL_POSITIVE_ACTION_COST_POLICY_EVIDENCE_NUMERIC_COST_FAIL_CLOSED"
COST_EVIDENCE_REASON_CODE = "S27_POSITIVE_ACTION_LIMIT_FILL_REQUIRES_COMMISSION_NUMERIC_POLICY_UNRESOLVED"

SOURCE_COST_TREATMENT_LABEL = "SOURCE_LOCK_ALL_ORDERS_INCUR_COMMISSIONS"
LIMIT_FILL_COST_TREATMENT_LABEL = "SOURCE_LOCK_LIMIT_FILL_COMMISSION_ONLY_NO_SPREAD_COST"
NUMERIC_COST_POLICY_STATUS = "FAIL_CLOSED_NUMERIC_ZN_COMMISSION_POLICY_UNRESOLVED"
INFERRED_RETAIL_COST_STATUS = "NOT_AUTHORIZED_INFERRED_RETAIL_FUTURES_COST_REQUIRES_OPERATOR_ACCEPTANCE"
PROP_CFD_ADAPTER_COST_REJECTION_LABEL = "REJECT_PROP_FIRM_CFD_ADAPTER_PERSONAL_COSTS"
ACTUAL_COST_LEDGER_STATUS = "FAIL_CLOSED_ACTUAL_COST_LEDGER_NOT_EMITTED_NUMERIC_COST_POLICY_UNRESOLVED"
NO_SPREAD_COST_REASON = "LIMIT_FILL_NO_MARKET_SPREAD_COST_BY_SOURCE_LOCK"
NOT_APPLICABLE = "NOT_APPLICABLE"

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()
_COST_PARAMETER_FILENAME = "cost_parameter.csv"
_EXPECTED_COST_PARAMETER_SHA256 = "e6b7c69a712fd7a5effbabbd4c809f24c1a6dfabbfb1ce317b387c923ac7f098"
_EXPECTED_COST_ROW_STATUS = "READY_COST_PARAMETER_HASHES_LOCAL_ONLY_FAIL_CLOSED_FOR_EXECUTION"

COST_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_ACTUAL_COST_EMISSION",
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
class PositiveActionCostEvidenceRow:
    ledger_label: str
    row_status: str
    reason_code: str
    fill_bundle_hash: str
    limit_fill_row_hash: str
    input_pack_path: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    fill_quantity: int
    fill_price: float
    cost_parameter_file_hash: str
    cost_parameter_row_hash: str
    commission_policy_hash: str
    spread_policy_hash: str
    contract_multiplier_value_hash: str
    currency_policy_hash: str
    cost_parameter_readiness_status: str
    source_cost_treatment_label: str
    source_cost_treatment_hash: str
    limit_fill_cost_treatment_label: str
    limit_fill_cost_treatment_hash: str
    numeric_cost_policy_status: str
    inferred_retail_cost_status: str
    prop_cfd_adapter_cost_rejection_label: str
    prop_cfd_adapter_cost_rejection_hash: str
    cost_accounting_required_by_source: bool
    actual_commission_rows_emitted: bool
    actual_spread_cost_rows_emitted: bool
    actual_cost_rows_emitted: bool
    actual_cost_ledger_status: str
    commission_amount: float
    spread_cost_amount: float
    total_cost_amount: float
    total_cost_currency: str
    no_spread_cost_reason: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action cost evidence row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_against_fill(self, fill_bundle: PositiveActionFillExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_COST_EVIDENCE_LEDGER":
            raise CarverBlocked("S27 v2 positive-action cost evidence ledger label is not locked")
        if self.row_status != COST_EVIDENCE_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action cost evidence row status is not locked")
        if self.reason_code != COST_EVIDENCE_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action cost evidence reason code is not locked")
        for name, hash_value in (
            ("fill bundle", self.fill_bundle_hash),
            ("limit fill row", self.limit_fill_row_hash),
            ("cost parameter file", self.cost_parameter_file_hash),
            ("cost parameter row", self.cost_parameter_row_hash),
            ("commission policy", self.commission_policy_hash),
            ("spread policy", self.spread_policy_hash),
            ("contract multiplier value", self.contract_multiplier_value_hash),
            ("currency policy", self.currency_policy_hash),
            ("source cost treatment", self.source_cost_treatment_hash),
            ("limit fill cost treatment", self.limit_fill_cost_treatment_hash),
            ("prop/CFD/adapter cost rejection", self.prop_cfd_adapter_cost_rejection_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action cost evidence {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("cost parameter readiness", self.cost_parameter_readiness_status),
            ("source cost treatment", self.source_cost_treatment_label),
            ("limit fill cost treatment", self.limit_fill_cost_treatment_label),
            ("numeric cost policy status", self.numeric_cost_policy_status),
            ("inferred retail cost status", self.inferred_retail_cost_status),
            ("prop/CFD/adapter rejection", self.prop_cfd_adapter_cost_rejection_label),
            ("actual cost ledger status", self.actual_cost_ledger_status),
            ("total cost currency", self.total_cost_currency),
            ("no spread cost reason", self.no_spread_cost_reason),
        ):
            require_text(f"S27 v2 positive-action cost evidence {name}", value)
        require_integer("S27 v2 positive-action cost evidence fill quantity", self.fill_quantity)
        require_finite_number("S27 v2 positive-action cost evidence fill price", self.fill_price)
        for name, amount in (
            ("commission amount", self.commission_amount),
            ("spread cost amount", self.spread_cost_amount),
            ("total cost amount", self.total_cost_amount),
        ):
            require_finite_number(f"S27 v2 positive-action cost evidence {name}", amount)
        self._validate_locked_identity(fill_bundle)
        self._validate_cost_policy_binding()
        if self.row_hash != canonical_sha256(_cost_evidence_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action cost evidence row hash must be content-bound")

    def _validate_locked_identity(self, fill_bundle: PositiveActionFillExecutableBundle) -> None:
        fill_row = fill_bundle.limit_fill_row
        if self.fill_bundle_hash != fill_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action cost evidence must bind active fill bundle")
        if self.limit_fill_row_hash != fill_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action cost evidence must bind active limit fill row")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action cost evidence is locked to the positive-action pack")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action cost evidence fill timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 positive-action cost evidence raw symbol is not locked")
        if self.fill_quantity != fill_row.filled_order_quantity:
            raise CarverBlocked("S27 v2 positive-action cost evidence fill quantity must bind fill row")
        if self.fill_price != fill_row.fill_price:
            raise CarverBlocked("S27 v2 positive-action cost evidence fill price must bind fill row")

    def _validate_cost_policy_binding(self) -> None:
        cost_row = _locked_cost_parameter_row(_POSITIVE_ACTION_PACK_PATH)
        if self.cost_parameter_file_hash != _verify_cost_parameter_file_hash(_POSITIVE_ACTION_PACK_PATH):
            raise CarverBlocked("S27 v2 positive-action cost parameter file hash mismatch")
        if self.cost_parameter_row_hash != _cost_parameter_row_hash(_POSITIVE_ACTION_PACK_PATH):
            raise CarverBlocked("S27 v2 positive-action cost evidence must bind active cost parameter row")
        for field in (
            "commission_policy_hash",
            "spread_policy_hash",
            "contract_multiplier_value_hash",
            "currency_policy_hash",
        ):
            if getattr(self, field) != cost_row[field]:
                raise CarverBlocked(f"S27 v2 positive-action cost evidence must bind {field}")
        if self.cost_parameter_readiness_status != _EXPECTED_COST_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action cost parameter readiness must remain fail-closed")
        if self.source_cost_treatment_label != SOURCE_COST_TREATMENT_LABEL:
            raise CarverBlocked("S27 v2 positive-action source cost treatment is not locked")
        if self.source_cost_treatment_hash != _policy_hash(
            "source_cost_treatment",
            SOURCE_COST_TREATMENT_LABEL,
            "COMMISSION_FOR_ALL_ORDERS",
            self.commission_policy_hash,
        ):
            raise CarverBlocked("S27 v2 positive-action source cost treatment hash must bind commission policy")
        if self.limit_fill_cost_treatment_label != LIMIT_FILL_COST_TREATMENT_LABEL:
            raise CarverBlocked("S27 v2 positive-action limit-fill cost treatment is not locked")
        if self.limit_fill_cost_treatment_hash != _policy_hash(
            "limit_fill_cost_treatment",
            LIMIT_FILL_COST_TREATMENT_LABEL,
            "COMMISSION_ONLY",
            self.spread_policy_hash,
            self.limit_fill_row_hash,
        ):
            raise CarverBlocked("S27 v2 positive-action limit-fill cost treatment hash must bind fill and spread policy")
        if self.numeric_cost_policy_status != NUMERIC_COST_POLICY_STATUS:
            raise CarverBlocked("S27 v2 positive-action numeric cost policy must remain fail-closed")
        if self.inferred_retail_cost_status != INFERRED_RETAIL_COST_STATUS:
            raise CarverBlocked("S27 v2 positive-action inferred retail cost assumption is not authorized")
        if self.prop_cfd_adapter_cost_rejection_label != PROP_CFD_ADAPTER_COST_REJECTION_LABEL:
            raise CarverBlocked("S27 v2 positive-action prop/CFD/adapter cost rejection is not locked")
        if self.prop_cfd_adapter_cost_rejection_hash != _policy_hash(
            "cost_rejection",
            PROP_CFD_ADAPTER_COST_REJECTION_LABEL,
            "NO_PROP_FIRM_FEES",
            "NO_CFD_SPREADS_OR_SWAPS",
            "NO_ADAPTER_OR_PERSONAL_TRADING_COSTS",
        ):
            raise CarverBlocked("S27 v2 positive-action cost rejection hash must bind rejected cost sources")
        if self.cost_accounting_required_by_source is not True:
            raise CarverBlocked("S27 v2 positive-action fill requires cost accounting by source treatment")
        if any(
            flag is not False
            for flag in (
                self.actual_commission_rows_emitted,
                self.actual_spread_cost_rows_emitted,
                self.actual_cost_rows_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action cost evidence cannot emit actual cost rows")
        if self.actual_cost_ledger_status != ACTUAL_COST_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual cost ledger status must remain fail-closed")
        if any(amount != 0.0 for amount in (self.commission_amount, self.spread_cost_amount, self.total_cost_amount)):
            raise CarverBlocked("S27 v2 positive-action unresolved numeric cost must not carry positive amounts")
        if self.total_cost_currency != NOT_APPLICABLE:
            raise CarverBlocked("S27 v2 positive-action unresolved cost must not carry cost currency")
        if self.no_spread_cost_reason != NO_SPREAD_COST_REASON:
            raise CarverBlocked("S27 v2 positive-action limit fill spread-cost reason is not locked")


@dataclass(frozen=True)
class PositiveActionCostExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    fill_bundle: PositiveActionFillExecutableBundle
    cost_evidence_row: PositiveActionCostEvidenceRow
    cost_evidence_metadata_rows_emitted: bool
    actual_commission_rows_emitted: bool
    actual_spread_cost_rows_emitted: bool
    actual_cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = COST_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_COST_STATUS:
            raise CarverBlocked("S27 v2 positive-action cost bundle status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_COST_AUTHORIZATION:
            raise CarverBlocked("S27 v2 positive-action cost authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 positive-action cost must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 positive-action cost lane must remain source-native futures")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action cost is locked to the declared positive-action pack")
        active_fill = build_positive_action_fill_executable(_POSITIVE_ACTION_PACK_PATH)
        self.fill_bundle.validate()
        if self.fill_bundle != active_fill:
            raise CarverBlocked("S27 v2 positive-action cost must bind active fill bundle")
        self.cost_evidence_row._validate_against_fill(active_fill)
        active_cost_row = _build_active_cost_evidence_row(_POSITIVE_ACTION_PACK_PATH, active_fill)
        if self.cost_evidence_row != active_cost_row:
            raise CarverBlocked("S27 v2 positive-action cost evidence row must match active local evidence")
        if any(
            flag is not True
            for flag in (
                self.cost_evidence_metadata_rows_emitted,
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action cost must emit only authorized metadata surfaces")
        if any(
            flag is not False
            for flag in (
                self.actual_commission_rows_emitted,
                self.actual_spread_cost_rows_emitted,
                self.actual_cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action cost cannot emit cost/PnL/result/evidence")
        if self.non_authorizations != COST_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 positive-action cost must preserve non-authorizations")
        require_hash("S27 v2 positive-action cost bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_cost_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action cost bundle hash must be content-bound")


def build_positive_action_cost_executable(
    input_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
) -> PositiveActionCostExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action cost is locked to the declared positive-action pack")
    fill_bundle = build_positive_action_fill_executable(pack_path)
    cost_row = _build_active_cost_evidence_row(pack_path, fill_bundle)
    bundle = PositiveActionCostExecutableBundle(
        status=S27_V2_POSITIVE_ACTION_COST_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_COST_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        fill_bundle=fill_bundle,
        cost_evidence_row=cost_row,
        cost_evidence_metadata_rows_emitted=True,
        actual_commission_rows_emitted=False,
        actual_spread_cost_rows_emitted=False,
        actual_cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionCostExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_cost_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_cost_evidence_row(
    pack_path: Path,
    fill_bundle: PositiveActionFillExecutableBundle,
) -> PositiveActionCostEvidenceRow:
    cost_row = _locked_cost_parameter_row(pack_path)
    fill_row = fill_bundle.limit_fill_row
    row = PositiveActionCostEvidenceRow(
        ledger_label="POSITIVE_ACTION_COST_EVIDENCE_LEDGER",
        row_status=COST_EVIDENCE_ROW_STATUS,
        reason_code=COST_EVIDENCE_REASON_CODE,
        fill_bundle_hash=fill_bundle.bundle_hash,
        limit_fill_row_hash=fill_row.row_hash,
        input_pack_path=str(pack_path),
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        fill_quantity=fill_row.filled_order_quantity,
        fill_price=fill_row.fill_price,
        cost_parameter_file_hash=_verify_cost_parameter_file_hash(pack_path),
        cost_parameter_row_hash=_cost_parameter_row_hash(pack_path),
        commission_policy_hash=cost_row["commission_policy_hash"],
        spread_policy_hash=cost_row["spread_policy_hash"],
        contract_multiplier_value_hash=cost_row["contract_multiplier_value_hash"],
        currency_policy_hash=cost_row["currency_policy_hash"],
        cost_parameter_readiness_status=cost_row["readiness_status"],
        source_cost_treatment_label=SOURCE_COST_TREATMENT_LABEL,
        source_cost_treatment_hash=_policy_hash(
            "source_cost_treatment",
            SOURCE_COST_TREATMENT_LABEL,
            "COMMISSION_FOR_ALL_ORDERS",
            cost_row["commission_policy_hash"],
        ),
        limit_fill_cost_treatment_label=LIMIT_FILL_COST_TREATMENT_LABEL,
        limit_fill_cost_treatment_hash=_policy_hash(
            "limit_fill_cost_treatment",
            LIMIT_FILL_COST_TREATMENT_LABEL,
            "COMMISSION_ONLY",
            cost_row["spread_policy_hash"],
            fill_row.row_hash,
        ),
        numeric_cost_policy_status=NUMERIC_COST_POLICY_STATUS,
        inferred_retail_cost_status=INFERRED_RETAIL_COST_STATUS,
        prop_cfd_adapter_cost_rejection_label=PROP_CFD_ADAPTER_COST_REJECTION_LABEL,
        prop_cfd_adapter_cost_rejection_hash=_policy_hash(
            "cost_rejection",
            PROP_CFD_ADAPTER_COST_REJECTION_LABEL,
            "NO_PROP_FIRM_FEES",
            "NO_CFD_SPREADS_OR_SWAPS",
            "NO_ADAPTER_OR_PERSONAL_TRADING_COSTS",
        ),
        cost_accounting_required_by_source=True,
        actual_commission_rows_emitted=False,
        actual_spread_cost_rows_emitted=False,
        actual_cost_rows_emitted=False,
        actual_cost_ledger_status=ACTUAL_COST_LEDGER_STATUS,
        commission_amount=0.0,
        spread_cost_amount=0.0,
        total_cost_amount=0.0,
        total_cost_currency=NOT_APPLICABLE,
        no_spread_cost_reason=NO_SPREAD_COST_REASON,
        row_hash="0" * 64,
    )
    row = PositiveActionCostEvidenceRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_cost_evidence_row_hash_payload(row))}
    )
    row._validate_against_fill(fill_bundle)
    return row


def _locked_cost_parameter_row(pack_path: Path) -> dict[str, str]:
    rows = _read_pack_rows(pack_path)[_COST_PARAMETER_FILENAME]
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 positive-action cost parameter file must have one row")
    row = rows[0]
    if row.get("effective_trading_date") != EXPECTED_SELECTED_FILL[:10]:
        raise CarverBlocked("S27 v2 positive-action cost parameter trading date is not locked")
    if row.get("raw_symbol") != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 positive-action cost parameter raw symbol is not locked")
    if row.get("readiness_status") != _EXPECTED_COST_ROW_STATUS:
        raise CarverBlocked("S27 v2 positive-action cost parameter readiness must remain fail-closed")
    for field in (
        "commission_policy_hash",
        "spread_policy_hash",
        "contract_multiplier_value_hash",
        "currency_policy_hash",
    ):
        require_hash(f"S27 v2 positive-action cost parameter {field}", row.get(field, ""))
    return row


def _verify_cost_parameter_file_hash(pack_path: Path) -> str:
    path = pack_path / _COST_PARAMETER_FILENAME
    observed = sha256(path.read_bytes()).hexdigest()
    if observed != _EXPECTED_COST_PARAMETER_SHA256:
        raise CarverBlocked("S27 v2 positive-action cost parameter file hash must match audited pack")
    return observed


def _cost_parameter_row_hash(pack_path: Path) -> str:
    return _row_hashes_by_file(_read_pack_rows(pack_path))[_COST_PARAMETER_FILENAME][0]


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_COST_POLICY", "label": label, "values": values})


def _cost_evidence_row_hash_payload(row: PositiveActionCostEvidenceRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _cost_bundle_hash_payload(bundle: PositiveActionCostExecutableBundle) -> dict[str, object]:
    return {
        "actual_commission_rows_emitted": bundle.actual_commission_rows_emitted,
        "actual_cost_rows_emitted": bundle.actual_cost_rows_emitted,
        "actual_spread_cost_rows_emitted": bundle.actual_spread_cost_rows_emitted,
        "artifact": "S27_V2_POSITIVE_ACTION_COST_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "cost_evidence_metadata_rows_emitted": bundle.cost_evidence_metadata_rows_emitted,
        "cost_evidence_row_hash": bundle.cost_evidence_row.row_hash,
        "fill_bundle_hash": bundle.fill_bundle.bundle_hash,
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

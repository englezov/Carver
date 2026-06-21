from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .desired_position_executable import CONTRACT_POINT_VALUE, CONTRACT_POINT_VALUE_CURRENCY, CONTRACT_POINT_VALUE_SOURCE_LABEL
from .local_replay import canonical_sha256
from .positive_action_actual_cost_executable import (
    PositiveActionActualCostExecutableBundle,
    build_positive_action_actual_cost_executable,
)
from .positive_action_executable import EXPECTED_RAW_SYMBOL, EXPECTED_SELECTED_FILL, POSITIVE_ACTION_PACK_RELATIVE_PATH
from .validation import require_finite_number, require_hash, require_integer, require_positive_number, require_text


S27_V2_POSITIVE_ACTION_ACTUAL_PNL_AUTHORIZATION = "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_ACTUAL_PNL_LEDGER"
S27_V2_POSITIVE_ACTION_ACTUAL_PNL_STATUS = "S27_V2_POSITIVE_ACTION_ACTUAL_PNL_LEDGER_EMITTED_NOT_RESULT"

ACTUAL_PNL_ROW_STATUS = "LOCAL_POSITIVE_ACTION_ACTUAL_PNL_LEDGER_ROW_EMITTED_NOT_RESULT"
ACTUAL_PNL_REASON_CODE = "S27_POSITIVE_ACTION_SHORT_MARK_TO_NEXT_COMPLETED_HOURLY_CLOSE_MINUS_ACCEPTED_COST"

VALUATION_CONVENTION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
VALUATION_CONVENTION_NAME = "NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL"
VALUATION_MARK_READINESS_STATUS = "READY_COMPLETED_BAR_LOCAL_POSITIVE_ACTION_VALUATION_MARK_DEV_RECON_ONLY"
PNL_DIRECTION_LABEL = "SHORT_POSITION_MARK_TO_MARKET_FILL_MINUS_MARK"
RESULT_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
BACKTEST_STATUS = "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"
PNL_EVALUATION_STATUS = "NOT_EMITTED_MECHANICAL_LEDGER_ROW_ONLY"

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()
VALUATION_MARK_PACK_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260609_positive_action_valuation_mark_znm6_20260413T15_declared_pack"
)
_VALUATION_MARK_PACK_PATH = (_REPO_ROOT / VALUATION_MARK_PACK_RELATIVE_PATH).resolve()
_VALUATION_MARK_MANIFEST_FILENAME = "S27_V2_POSITIVE_ACTION_VALUATION_MARK_DECLARED_INPUT_PACK_MANIFEST.json"
_VALUATION_MARK_CSV_FILENAME = "valuation_mark_completed_bar.csv"
_VALUATION_MARK_LOCAL_AUDIT_RECORD_PATH = (
    _REPO_ROOT
    / "docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_VALUATION_MARK_DECLARED_PACK_LOCAL_AUDIT_RESULT_2026-06-09.md"
).resolve()

_EXPECTED_VALUATION_MARK_MANIFEST_SHA256 = "f5a5eb85ee5acfb13e914e2cfc0d3583c41f8c133ee79c188c70881d3e23b90e"
_EXPECTED_VALUATION_MARK_CSV_SHA256 = "b859f397e62ed3e8acef743003e3a543929d246d5bb98d95fa9f2fbd08758e26"
_EXPECTED_VALUATION_MARK_LOCAL_AUDIT_SHA256 = "550dcff7234d43691f0ce9ecdda674df7897de96fe4de177b8ce97f8d22b86c8"
_EXPECTED_VALUATION_MARK_SOURCE_ROW_TEXT_SHA256 = "f39f5056c9d1e122e6f62d82e8918745e10233aa95abef9949ac5f50be6f98da"
_EXPECTED_VALUATION_MARK_SOURCE_ROW_CANONICAL_JSON_SHA256 = (
    "a8d60ee8a26ee10b8460fea2f46c656eba0eeb7be507badd4fe44434de8b413a"
)
_EXPECTED_VALUATION_MARK_COMPLETED_TIMESTAMP = "2026-04-13T15:00:00Z"
_EXPECTED_VALUATION_MARK_CLOSE = 111.046875

ACTUAL_PNL_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_MARKET_DATA_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_RESULT_EMISSION",
    "NO_RESULT_INTERPRETATION",
    "NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION",
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)


@dataclass(frozen=True)
class PositiveActionActualPnlLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    actual_cost_bundle_hash: str
    actual_cost_row_hash: str
    fill_bundle_hash: str
    limit_fill_row_hash: str
    positive_action_pack_path: str
    valuation_mark_pack_path: str
    valuation_mark_manifest_sha256: str
    valuation_mark_csv_sha256: str
    valuation_mark_local_audit_sha256: str
    selected_fill_timestamp_utc: str
    valuation_mark_completed_timestamp_utc: str
    raw_symbol: str
    filled_order_side: str
    fill_quantity: int
    position_after_fill: int
    fill_price: float
    valuation_mark_close_price: float
    contract_point_value: float
    contract_point_value_currency: str
    contract_point_value_source_label: str
    valuation_convention_label: str
    valuation_convention_name: str
    valuation_convention_hash: str
    valuation_mark_source_row_text_sha256: str
    valuation_mark_source_row_canonical_json_sha256: str
    pnl_direction_label: str
    gross_pnl_amount: float
    commission_cost_amount: float
    spread_cost_amount: float
    total_cost_amount: float
    net_pnl_amount: float
    pnl_currency: str
    pnl_formula_hash: str
    result_status: str
    backtest_status: str
    pnl_evaluation_status: str
    result_rows_emitted: bool
    result_scored_run_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action actual PnL row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_against_active_evidence(
        self,
        actual_cost_bundle: PositiveActionActualCostExecutableBundle,
        valuation_mark: dict[str, object],
    ) -> None:
        if self.ledger_label != "POSITIVE_ACTION_ACTUAL_PNL_LEDGER":
            raise CarverBlocked("S27 v2 positive-action actual PnL ledger label is not locked")
        if self.row_status != ACTUAL_PNL_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual PnL row status is not locked")
        if self.reason_code != ACTUAL_PNL_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action actual PnL reason code is not locked")
        for name, hash_value in (
            ("actual cost bundle", self.actual_cost_bundle_hash),
            ("actual cost row", self.actual_cost_row_hash),
            ("fill bundle", self.fill_bundle_hash),
            ("limit fill row", self.limit_fill_row_hash),
            ("valuation mark manifest", self.valuation_mark_manifest_sha256),
            ("valuation mark CSV", self.valuation_mark_csv_sha256),
            ("valuation mark local audit", self.valuation_mark_local_audit_sha256),
            ("valuation convention", self.valuation_convention_hash),
            ("valuation mark source row text", self.valuation_mark_source_row_text_sha256),
            ("valuation mark canonical row", self.valuation_mark_source_row_canonical_json_sha256),
            ("PnL formula", self.pnl_formula_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action actual PnL {name} hash", hash_value)
        for name, value in (
            ("positive-action pack path", self.positive_action_pack_path),
            ("valuation mark pack path", self.valuation_mark_pack_path),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("valuation mark timestamp", self.valuation_mark_completed_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("filled order side", self.filled_order_side),
            ("contract point value currency", self.contract_point_value_currency),
            ("contract point value source label", self.contract_point_value_source_label),
            ("valuation convention label", self.valuation_convention_label),
            ("valuation convention name", self.valuation_convention_name),
            ("PnL direction label", self.pnl_direction_label),
            ("PnL currency", self.pnl_currency),
            ("result status", self.result_status),
            ("backtest status", self.backtest_status),
            ("PnL evaluation status", self.pnl_evaluation_status),
        ):
            require_text(f"S27 v2 positive-action actual PnL {name}", value)
        for name, value in (
            ("fill quantity", self.fill_quantity),
            ("position after fill", self.position_after_fill),
        ):
            require_integer(f"S27 v2 positive-action actual PnL {name}", value)
        require_positive_number("S27 v2 positive-action actual PnL fill price", self.fill_price)
        require_positive_number("S27 v2 positive-action actual PnL valuation mark", self.valuation_mark_close_price)
        require_positive_number("S27 v2 positive-action actual PnL point value", self.contract_point_value)
        for name, amount in (
            ("gross PnL", self.gross_pnl_amount),
            ("commission cost", self.commission_cost_amount),
            ("spread cost", self.spread_cost_amount),
            ("total cost", self.total_cost_amount),
            ("net PnL", self.net_pnl_amount),
        ):
            require_finite_number(f"S27 v2 positive-action actual PnL {name}", amount)
        self._validate_locked_identity(actual_cost_bundle, valuation_mark)
        self._validate_arithmetic_and_boundaries(actual_cost_bundle)
        if self.row_hash != canonical_sha256(_actual_pnl_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action actual PnL row hash must be content-bound")

    def _validate_locked_identity(
        self,
        actual_cost_bundle: PositiveActionActualCostExecutableBundle,
        valuation_mark: dict[str, object],
    ) -> None:
        cost_row = actual_cost_bundle.actual_cost_row
        fill_bundle = actual_cost_bundle.fill_bundle
        fill_row = fill_bundle.limit_fill_row
        if self.actual_cost_bundle_hash != actual_cost_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind active actual-cost bundle")
        if self.actual_cost_row_hash != cost_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind active actual-cost row")
        if self.fill_bundle_hash != fill_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind active fill bundle")
        if self.limit_fill_row_hash != fill_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind active limit-fill row")
        if Path(self.positive_action_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action actual PnL is locked to the positive-action pack")
        if Path(self.valuation_mark_pack_path).resolve() != _VALUATION_MARK_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action actual PnL is locked to the valuation mark pack")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action actual PnL fill timestamp is not locked")
        if self.valuation_mark_completed_timestamp_utc != valuation_mark["completed_timestamp_utc"]:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind valuation mark timestamp")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL or self.raw_symbol != valuation_mark["raw_symbol"]:
            raise CarverBlocked("S27 v2 positive-action actual PnL raw symbol must bind active rows")
        if self.filled_order_side != fill_row.filled_order_side or self.filled_order_side != "SELL":
            raise CarverBlocked("S27 v2 positive-action actual PnL is locked to the SELL limit fill")
        if self.fill_quantity != fill_row.filled_order_quantity:
            raise CarverBlocked("S27 v2 positive-action actual PnL fill quantity must bind fill row")
        if self.position_after_fill != fill_row.position_after_fill:
            raise CarverBlocked("S27 v2 positive-action actual PnL position-after must bind fill row")
        if self.fill_price != fill_row.fill_price:
            raise CarverBlocked("S27 v2 positive-action actual PnL fill price must bind fill row")
        if self.valuation_mark_close_price != valuation_mark["close_price"]:
            raise CarverBlocked("S27 v2 positive-action actual PnL mark close must bind declared mark row")
        if self.valuation_mark_manifest_sha256 != valuation_mark["manifest_sha256"]:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind valuation manifest bytes")
        if self.valuation_mark_csv_sha256 != valuation_mark["csv_sha256"]:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind valuation CSV bytes")
        if self.valuation_mark_local_audit_sha256 != valuation_mark["local_audit_sha256"]:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind valuation local audit bytes")
        if self.valuation_mark_source_row_text_sha256 != valuation_mark["source_row_text_sha256"]:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind valuation source row bytes")
        if self.valuation_mark_source_row_canonical_json_sha256 != valuation_mark["source_row_canonical_json_sha256"]:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind valuation canonical row hash")

    def _validate_arithmetic_and_boundaries(self, actual_cost_bundle: PositiveActionActualCostExecutableBundle) -> None:
        cost_row = actual_cost_bundle.actual_cost_row
        if self.contract_point_value != CONTRACT_POINT_VALUE:
            raise CarverBlocked("S27 v2 positive-action actual PnL point value must bind static ZN point value")
        if self.contract_point_value_currency != CONTRACT_POINT_VALUE_CURRENCY or self.pnl_currency != "USD":
            raise CarverBlocked("S27 v2 positive-action actual PnL currency must be USD")
        if self.contract_point_value_source_label != CONTRACT_POINT_VALUE_SOURCE_LABEL:
            raise CarverBlocked("S27 v2 positive-action actual PnL point-value source label is not locked")
        if self.valuation_convention_label != VALUATION_CONVENTION_LABEL:
            raise CarverBlocked("S27 v2 positive-action actual PnL valuation convention label is not locked")
        if self.valuation_convention_name != VALUATION_CONVENTION_NAME:
            raise CarverBlocked("S27 v2 positive-action actual PnL valuation convention name is not locked")
        if self.valuation_convention_hash != _policy_hash(
            "valuation_convention",
            VALUATION_CONVENTION_LABEL,
            VALUATION_CONVENTION_NAME,
            self.valuation_mark_manifest_sha256,
            self.valuation_mark_csv_sha256,
            self.valuation_mark_local_audit_sha256,
        ):
            raise CarverBlocked("S27 v2 positive-action actual PnL valuation convention hash must bind mark pack")
        if self.pnl_direction_label != PNL_DIRECTION_LABEL:
            raise CarverBlocked("S27 v2 positive-action actual PnL direction label is not locked")
        expected_gross = (self.fill_price - self.valuation_mark_close_price) * abs(self.fill_quantity) * self.contract_point_value
        if self.gross_pnl_amount != expected_gross:
            raise CarverBlocked("S27 v2 positive-action actual PnL gross amount must equal short mark-to-market formula")
        if self.commission_cost_amount != cost_row.commission_amount:
            raise CarverBlocked("S27 v2 positive-action actual PnL commission must bind active cost row")
        if self.spread_cost_amount != cost_row.spread_cost_amount:
            raise CarverBlocked("S27 v2 positive-action actual PnL spread cost must bind active cost row")
        if self.total_cost_amount != cost_row.total_cost_amount:
            raise CarverBlocked("S27 v2 positive-action actual PnL total cost must bind active cost row")
        if self.net_pnl_amount != self.gross_pnl_amount - self.total_cost_amount:
            raise CarverBlocked("S27 v2 positive-action actual PnL net amount must equal gross minus total cost")
        if self.pnl_formula_hash != _policy_hash(
            "actual_pnl_formula",
            self.pnl_direction_label,
            self.fill_price,
            self.valuation_mark_close_price,
            self.fill_quantity,
            self.contract_point_value,
            self.gross_pnl_amount,
            self.total_cost_amount,
            self.net_pnl_amount,
            self.pnl_currency,
        ):
            raise CarverBlocked("S27 v2 positive-action actual PnL formula hash must bind arithmetic")
        if self.result_status != RESULT_STATUS or self.backtest_status != BACKTEST_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual PnL must keep result/backtest fail-closed")
        if self.pnl_evaluation_status != PNL_EVALUATION_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual PnL evaluation status is not locked")
        if any(
            flag is not False
            for flag in (
                self.result_rows_emitted,
                self.result_scored_run_emitted,
                self.result_interpretation_emitted,
                self.pnl_evaluation_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action actual PnL cannot emit result/evaluation/source-faithful evidence")


@dataclass(frozen=True)
class PositiveActionActualPnlExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    positive_action_pack_path: str
    valuation_mark_pack_path: str
    actual_cost_bundle: PositiveActionActualCostExecutableBundle
    actual_pnl_row: PositiveActionActualPnlLedgerRow
    actual_cost_rows_emitted: bool
    actual_pnl_rows_emitted: bool
    result_rows_emitted: bool
    result_scored_run_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = ACTUAL_PNL_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_ACTUAL_PNL_STATUS:
            raise CarverBlocked("S27 v2 positive-action actual PnL bundle status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_ACTUAL_PNL_AUTHORIZATION:
            raise CarverBlocked("S27 v2 positive-action actual PnL authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 positive-action actual PnL must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 positive-action actual PnL lane must remain source-native futures")
        if Path(self.positive_action_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action actual PnL is locked to the positive-action pack")
        if Path(self.valuation_mark_pack_path).resolve() != _VALUATION_MARK_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action actual PnL is locked to the valuation mark pack")
        active_cost = build_positive_action_actual_cost_executable(_POSITIVE_ACTION_PACK_PATH)
        self.actual_cost_bundle.validate()
        if self.actual_cost_bundle != active_cost:
            raise CarverBlocked("S27 v2 positive-action actual PnL must bind active actual-cost bundle")
        valuation_mark = _load_and_verify_valuation_mark(_VALUATION_MARK_PACK_PATH)
        self.actual_pnl_row._validate_against_active_evidence(active_cost, valuation_mark)
        active_row = _build_active_actual_pnl_row(_POSITIVE_ACTION_PACK_PATH, _VALUATION_MARK_PACK_PATH, active_cost, valuation_mark)
        if self.actual_pnl_row != active_row:
            raise CarverBlocked("S27 v2 positive-action actual PnL row must match active local evidence")
        if any(
            flag is not True
            for flag in (
                self.actual_cost_rows_emitted,
                self.actual_pnl_rows_emitted,
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action actual PnL must emit authorized cost/PnL/metadata rows")
        if any(
            flag is not False
            for flag in (
                self.result_rows_emitted,
                self.result_scored_run_emitted,
                self.result_interpretation_emitted,
                self.pnl_evaluation_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action actual PnL cannot emit result/evaluation/source-faithful evidence")
        if self.non_authorizations != ACTUAL_PNL_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 positive-action actual PnL must preserve non-authorizations")
        require_hash("S27 v2 positive-action actual PnL bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_actual_pnl_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action actual PnL bundle hash must be content-bound")


def build_positive_action_actual_pnl_executable(
    positive_action_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
    valuation_mark_pack_path: str | Path = _VALUATION_MARK_PACK_PATH,
) -> PositiveActionActualPnlExecutableBundle:
    pack_path = Path(positive_action_pack_path).resolve()
    mark_path = Path(valuation_mark_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action actual PnL is locked to the declared positive-action pack")
    if mark_path != _VALUATION_MARK_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action actual PnL is locked to the declared valuation mark pack")
    actual_cost_bundle = build_positive_action_actual_cost_executable(pack_path)
    valuation_mark = _load_and_verify_valuation_mark(mark_path)
    actual_pnl_row = _build_active_actual_pnl_row(pack_path, mark_path, actual_cost_bundle, valuation_mark)
    bundle = PositiveActionActualPnlExecutableBundle(
        status=S27_V2_POSITIVE_ACTION_ACTUAL_PNL_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_ACTUAL_PNL_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        positive_action_pack_path=str(pack_path),
        valuation_mark_pack_path=str(mark_path),
        actual_cost_bundle=actual_cost_bundle,
        actual_pnl_row=actual_pnl_row,
        actual_cost_rows_emitted=True,
        actual_pnl_rows_emitted=True,
        result_rows_emitted=False,
        result_scored_run_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionActualPnlExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_actual_pnl_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_actual_pnl_row(
    positive_action_pack_path: Path,
    valuation_mark_pack_path: Path,
    actual_cost_bundle: PositiveActionActualCostExecutableBundle,
    valuation_mark: dict[str, object],
) -> PositiveActionActualPnlLedgerRow:
    cost_row = actual_cost_bundle.actual_cost_row
    fill_bundle = actual_cost_bundle.fill_bundle
    fill_row = fill_bundle.limit_fill_row
    gross_pnl = (fill_row.fill_price - valuation_mark["close_price"]) * abs(fill_row.filled_order_quantity) * CONTRACT_POINT_VALUE
    total_cost = cost_row.total_cost_amount
    net_pnl = gross_pnl - total_cost
    valuation_convention_hash = _policy_hash(
        "valuation_convention",
        VALUATION_CONVENTION_LABEL,
        VALUATION_CONVENTION_NAME,
        valuation_mark["manifest_sha256"],
        valuation_mark["csv_sha256"],
        valuation_mark["local_audit_sha256"],
    )
    pnl_formula_hash = _policy_hash(
        "actual_pnl_formula",
        PNL_DIRECTION_LABEL,
        fill_row.fill_price,
        valuation_mark["close_price"],
        fill_row.filled_order_quantity,
        CONTRACT_POINT_VALUE,
        gross_pnl,
        total_cost,
        net_pnl,
        "USD",
    )
    row = PositiveActionActualPnlLedgerRow(
        ledger_label="POSITIVE_ACTION_ACTUAL_PNL_LEDGER",
        row_status=ACTUAL_PNL_ROW_STATUS,
        reason_code=ACTUAL_PNL_REASON_CODE,
        actual_cost_bundle_hash=actual_cost_bundle.bundle_hash,
        actual_cost_row_hash=cost_row.row_hash,
        fill_bundle_hash=fill_bundle.bundle_hash,
        limit_fill_row_hash=fill_row.row_hash,
        positive_action_pack_path=str(positive_action_pack_path),
        valuation_mark_pack_path=str(valuation_mark_pack_path),
        valuation_mark_manifest_sha256=valuation_mark["manifest_sha256"],
        valuation_mark_csv_sha256=valuation_mark["csv_sha256"],
        valuation_mark_local_audit_sha256=valuation_mark["local_audit_sha256"],
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        valuation_mark_completed_timestamp_utc=valuation_mark["completed_timestamp_utc"],
        raw_symbol=EXPECTED_RAW_SYMBOL,
        filled_order_side=fill_row.filled_order_side,
        fill_quantity=fill_row.filled_order_quantity,
        position_after_fill=fill_row.position_after_fill,
        fill_price=fill_row.fill_price,
        valuation_mark_close_price=valuation_mark["close_price"],
        contract_point_value=CONTRACT_POINT_VALUE,
        contract_point_value_currency=CONTRACT_POINT_VALUE_CURRENCY,
        contract_point_value_source_label=CONTRACT_POINT_VALUE_SOURCE_LABEL,
        valuation_convention_label=VALUATION_CONVENTION_LABEL,
        valuation_convention_name=VALUATION_CONVENTION_NAME,
        valuation_convention_hash=valuation_convention_hash,
        valuation_mark_source_row_text_sha256=valuation_mark["source_row_text_sha256"],
        valuation_mark_source_row_canonical_json_sha256=valuation_mark["source_row_canonical_json_sha256"],
        pnl_direction_label=PNL_DIRECTION_LABEL,
        gross_pnl_amount=gross_pnl,
        commission_cost_amount=cost_row.commission_amount,
        spread_cost_amount=cost_row.spread_cost_amount,
        total_cost_amount=total_cost,
        net_pnl_amount=net_pnl,
        pnl_currency="USD",
        pnl_formula_hash=pnl_formula_hash,
        result_status=RESULT_STATUS,
        backtest_status=BACKTEST_STATUS,
        pnl_evaluation_status=PNL_EVALUATION_STATUS,
        result_rows_emitted=False,
        result_scored_run_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        row_hash="0" * 64,
    )
    row = PositiveActionActualPnlLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_actual_pnl_row_hash_payload(row))}
    )
    row._validate_against_active_evidence(actual_cost_bundle, valuation_mark)
    return row


def _load_and_verify_valuation_mark(mark_path: Path) -> dict[str, object]:
    if mark_path.resolve() != _VALUATION_MARK_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation mark pack path is not locked")
    manifest_path = mark_path / _VALUATION_MARK_MANIFEST_FILENAME
    csv_path = mark_path / _VALUATION_MARK_CSV_FILENAME
    manifest_hash = _verify_file_hash(manifest_path, _EXPECTED_VALUATION_MARK_MANIFEST_SHA256, "valuation mark manifest")
    csv_hash = _verify_file_hash(csv_path, _EXPECTED_VALUATION_MARK_CSV_SHA256, "valuation mark CSV")
    local_audit_hash = _verify_file_hash(
        _VALUATION_MARK_LOCAL_AUDIT_RECORD_PATH,
        _EXPECTED_VALUATION_MARK_LOCAL_AUDIT_SHA256,
        "valuation mark local audit record",
    )
    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    rows = _read_mark_rows(csv_path)
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation mark CSV must contain exactly one row")
    row = rows[0]
    selected = manifest.get("selected_valuation_mark", {})
    source_file = manifest.get("source_file", {})
    if manifest.get("artifact") != "S27_V2_POSITIVE_ACTION_VALUATION_MARK_DECLARED_INPUT_PACK_MANIFEST":
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation manifest artifact is not locked")
    if manifest.get("status") != "LOCAL_INPUT_PACK_DECLARED_FOR_POSITIVE_ACTION_VALUATION_MARK_DEV_RECON_ONLY_NOT_PNL_NOT_BACKTEST_NOT_RESULT":
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation manifest status is not locked")
    if manifest.get("strategy_id") != "S27_V2" or manifest.get("instrument") != S27_V2_INSTRUMENT:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation manifest strategy/instrument mismatch")
    if manifest.get("raw_symbol") != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation manifest raw symbol mismatch")
    convention = manifest.get("valuation_convention", {})
    if convention.get("label") != VALUATION_CONVENTION_LABEL or convention.get("convention") != VALUATION_CONVENTION_NAME:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation convention is not locked")
    if convention.get("book_explicit_authority") is not False or convention.get("source_faithful_evidence_claim") is not False:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation convention must remain non-book-explicit")
    if selected.get("completed_timestamp_utc") != _EXPECTED_VALUATION_MARK_COMPLETED_TIMESTAMP:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation mark timestamp is not locked")
    if selected.get("strictly_after_fill_timestamp_utc") is not True:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation mark must be strictly after fill")
    if selected.get("is_pnl_row") is not False or selected.get("is_result_row") is not False:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation mark declaration cannot be PnL/result")
    if row.get("completed_timestamp_utc") != selected.get("completed_timestamp_utc"):
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation CSV timestamp must bind manifest")
    if row.get("raw_symbol") != selected.get("raw_symbol") or row.get("raw_symbol") != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation CSV raw symbol must bind manifest")
    if row.get("readiness_status") != VALUATION_MARK_READINESS_STATUS:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation row readiness is not locked")
    if row.get("valuation_convention_label") != VALUATION_CONVENTION_LABEL:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation CSV convention label mismatch")
    close_price = float(row["close_price"])
    if close_price != _EXPECTED_VALUATION_MARK_CLOSE or close_price != float(selected["close_price"]):
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation close is not locked")
    if row.get("source_row_text_sha256", "").lower() != _EXPECTED_VALUATION_MARK_SOURCE_ROW_TEXT_SHA256:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation source-row byte hash mismatch")
    if source_file.get("source_row_text_sha256", "").lower() != _EXPECTED_VALUATION_MARK_SOURCE_ROW_TEXT_SHA256:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation manifest source-row byte hash mismatch")
    if row.get("source_row_canonical_json_sha256", "").lower() != _EXPECTED_VALUATION_MARK_SOURCE_ROW_CANONICAL_JSON_SHA256:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation canonical source-row hash mismatch")
    if source_file.get("source_row_canonical_json_sha256", "").lower() != _EXPECTED_VALUATION_MARK_SOURCE_ROW_CANONICAL_JSON_SHA256:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation manifest canonical source-row hash mismatch")
    row_family_files = manifest.get("row_family_files", {})
    if row_family_files.get(_VALUATION_MARK_CSV_FILENAME, {}).get("sha256", "").lower() != csv_hash:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation manifest must bind CSV bytes")
    non_authorizations = tuple(manifest.get("non_authorizations", ()))
    if "NO_RESULT_EMISSION" not in non_authorizations or "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM" not in non_authorizations:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation manifest must preserve non-authorizations")
    return {
        "close_price": close_price,
        "completed_timestamp_utc": row["completed_timestamp_utc"],
        "csv_sha256": csv_hash,
        "local_audit_sha256": local_audit_hash,
        "manifest_sha256": manifest_hash,
        "raw_symbol": row["raw_symbol"],
        "source_row_canonical_json_sha256": row["source_row_canonical_json_sha256"].lower(),
        "source_row_text_sha256": row["source_row_text_sha256"].lower(),
    }


def _read_mark_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise CarverBlocked("S27 v2 positive-action actual PnL valuation mark CSV has no rows")
    return rows


def _verify_file_hash(path: Path, expected_hash: str, label: str) -> str:
    observed = sha256(path.read_bytes()).hexdigest()
    if observed != expected_hash:
        raise CarverBlocked(f"S27 v2 positive-action actual PnL {label} byte hash is not pinned")
    return observed


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_ACTUAL_PNL_POLICY", "label": label, "values": values})


def _actual_pnl_row_hash_payload(row: PositiveActionActualPnlLedgerRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _actual_pnl_bundle_hash_payload(bundle: PositiveActionActualPnlExecutableBundle) -> dict[str, object]:
    return {
        "actual_cost_bundle_hash": bundle.actual_cost_bundle.bundle_hash,
        "actual_cost_rows_emitted": bundle.actual_cost_rows_emitted,
        "actual_pnl_row_hash": bundle.actual_pnl_row.row_hash,
        "actual_pnl_rows_emitted": bundle.actual_pnl_rows_emitted,
        "artifact": "S27_V2_POSITIVE_ACTION_ACTUAL_PNL_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "pnl_evaluation_emitted": bundle.pnl_evaluation_emitted,
        "positive_action_pack_path": bundle.positive_action_pack_path,
        "provenance_metadata_rows_emitted": bundle.provenance_metadata_rows_emitted,
        "result_interpretation_emitted": bundle.result_interpretation_emitted,
        "result_rows_emitted": bundle.result_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "trusted_bundle_metadata_emitted": bundle.trusted_bundle_metadata_emitted,
        "validation_metadata_rows_emitted": bundle.validation_metadata_rows_emitted,
        "valuation_mark_pack_path": bundle.valuation_mark_pack_path,
    }

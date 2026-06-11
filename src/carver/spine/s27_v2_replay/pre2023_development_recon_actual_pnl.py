from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .development_recon_run import (
    CONTROLLED_RUN_RELATIVE_PATH,
    RUN_NON_AUTHORIZATIONS,
    ControlledDevelopmentReconRunBundle,
    _run_bundle_payload,
)
from .desired_position_executable import CONTRACT_POINT_VALUE, CONTRACT_POINT_VALUE_CURRENCY, CONTRACT_POINT_VALUE_SOURCE_LABEL
from .local_replay import canonical_sha256
from .validation import require_finite_number, require_hash, require_integer, require_positive_number, require_text


S27_V2_PRE2023_ACTUAL_PNL_AUTHORIZATION = "S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER_IMPLEMENTATION_GATE"
S27_V2_PRE2023_ACTUAL_PNL_STATUS = "S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER_EMITTED_NOT_RESULT"

ACTUAL_PNL_ROW_STATUS = "LOCAL_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER_ROW_EMITTED_NOT_RESULT"
ACTUAL_PNL_REASON_CODE = "S27_PRE2023_DEV_RECON_LONG_MARK_TO_NEXT_COMPLETED_HOURLY_CLOSE_MINUS_ACCEPTED_COST"

VALUATION_CONVENTION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
VALUATION_CONVENTION_NAME = "NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL"
PNL_DIRECTION_LABEL = "LONG_POSITION_MARK_MINUS_FILL"
RESULT_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
BACKTEST_STATUS = "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"
PNL_EVALUATION_STATUS = "NOT_EMITTED_MECHANICAL_LEDGER_ROW_ONLY"

_REPO_ROOT = Path(__file__).resolve().parents[4]
_CONTROLLED_RUN_PATH = (_REPO_ROOT / CONTROLLED_RUN_RELATIVE_PATH).resolve()
VALUATION_MARK_PACK_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_dev_recon_valuation_mark_znh2_20220103T03_declared_pack"
)
_VALUATION_MARK_PACK_PATH = (_REPO_ROOT / VALUATION_MARK_PACK_RELATIVE_PATH).resolve()
_VALUATION_MARK_MANIFEST_NAME = "S27_V2_PRE2023_VALUATION_MARK_DECLARED_INPUT_PACK_MANIFEST.json"
_VALUATION_MARK_CSV_NAME = "valuation_mark_completed_bar.csv"
_VALUATION_MARK_LOCAL_AUDIT_RECORD_PATH = (
    _REPO_ROOT / "docs/process/CARVER_S27_ZN_V2_PRE2023_VALUATION_MARK_DECLARED_PACK_LOCAL_AUDIT_RESULT_2026-06-11.md"
).resolve()

PRE2023_ACTUAL_PNL_OUTPUT_RELATIVE_PATH = (
    "docs/researchops/s27_v2_local_replay_runs/ZN/"
    "20260611_pre2023_oldest_dev_recon_2022_actual_pnl_completion"
)
_PRE2023_ACTUAL_PNL_OUTPUT_PATH = (_REPO_ROOT / PRE2023_ACTUAL_PNL_OUTPUT_RELATIVE_PATH).resolve()

_EXPECTED_CONTROLLED_RUN_BUNDLE_SHA256 = "7668d2f2212d382355efc00ca80e2345e7418b32661fc4c4612ede9ef6a0ad30"
_EXPECTED_FILL_LEDGER_SHA256 = "6f6fcec85335f550cb33ce5278051a152ee8bd9a872cc9dcaefdc535637c7d55"
_EXPECTED_COMMISSION_LEDGER_SHA256 = "310283aef814594dfd780c6576d11e1b37a0376a62a5200efc90dbae1116d560"
_EXPECTED_SPREAD_LEDGER_SHA256 = "ee4dd7216c5fd6cb8a802fb1883a9cd4ec3b802cfe208b6fab2b091f885b65ba"
_EXPECTED_VALUATION_MARK_MANIFEST_SHA256 = "735955f1e44e1107dbc64dd786fe7af7b52f88f17b75c7bd91708933a9e5c159"
_EXPECTED_VALUATION_MARK_CSV_SHA256 = "9aa8b3999a80058342c8e40236b2a926a500355d6d5fed6f6877de4147961031"
_EXPECTED_VALUATION_MARK_LOCAL_AUDIT_SHA256 = "2e98d465b1db6b097888f7962cb011199a24da138c190025b59a3b30f3cd7797"

EXPECTED_FILL_TIMESTAMP = "2022-01-03T02:00:00Z"
EXPECTED_VALUATION_MARK_TIMESTAMP = "2022-01-03T03:00:00Z"
EXPECTED_RAW_SYMBOL = "ZNH2"

ACTUAL_PNL_NON_AUTHORIZATIONS = RUN_NON_AUTHORIZATIONS


@dataclass(frozen=True)
class Pre2023DevelopmentReconActualPnlLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    controlled_run_bundle_hash: str
    fill_row_hash: str
    commission_row_hash: str
    spread_row_hash: str
    valuation_mark_manifest_sha256: str
    valuation_mark_csv_sha256: str
    valuation_mark_local_audit_sha256: str
    valuation_mark_strategy_ledger_line_sha256: str
    valuation_mark_raw_provider_line_sha256: str
    controlled_run_path: str
    valuation_mark_pack_path: str
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
        raise CarverBlocked("S27 v2 pre-2023 actual PnL row standalone validation is not authoritative")

    def _validate_against_active_evidence(
        self,
        controlled_run: ControlledDevelopmentReconRunBundle,
        active: dict[str, Any],
    ) -> None:
        if self.ledger_label != "PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER":
            raise CarverBlocked("S27 v2 pre-2023 actual PnL ledger label is not locked")
        if self.row_status != ACTUAL_PNL_ROW_STATUS:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL row status is not locked")
        if self.reason_code != ACTUAL_PNL_REASON_CODE:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL reason code is not locked")
        for name, hash_value in (
            ("controlled run bundle", self.controlled_run_bundle_hash),
            ("fill row", self.fill_row_hash),
            ("commission row", self.commission_row_hash),
            ("spread row", self.spread_row_hash),
            ("valuation manifest", self.valuation_mark_manifest_sha256),
            ("valuation CSV", self.valuation_mark_csv_sha256),
            ("valuation local audit", self.valuation_mark_local_audit_sha256),
            ("valuation strategy ledger line", self.valuation_mark_strategy_ledger_line_sha256),
            ("valuation raw provider line", self.valuation_mark_raw_provider_line_sha256),
            ("valuation convention", self.valuation_convention_hash),
            ("PnL formula", self.pnl_formula_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 pre-2023 actual PnL {name} hash", hash_value)
        for name, value in (
            ("controlled run path", self.controlled_run_path),
            ("valuation mark pack path", self.valuation_mark_pack_path),
            ("fill timestamp", self.selected_fill_timestamp_utc),
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
            require_text(f"S27 v2 pre-2023 actual PnL {name}", value)
        require_integer("S27 v2 pre-2023 actual PnL fill quantity", self.fill_quantity)
        require_integer("S27 v2 pre-2023 actual PnL position after fill", self.position_after_fill)
        require_positive_number("S27 v2 pre-2023 actual PnL fill price", self.fill_price)
        require_positive_number("S27 v2 pre-2023 actual PnL valuation mark", self.valuation_mark_close_price)
        require_positive_number("S27 v2 pre-2023 actual PnL point value", self.contract_point_value)
        for name, amount in (
            ("gross PnL", self.gross_pnl_amount),
            ("commission cost", self.commission_cost_amount),
            ("spread cost", self.spread_cost_amount),
            ("total cost", self.total_cost_amount),
            ("net PnL", self.net_pnl_amount),
        ):
            require_finite_number(f"S27 v2 pre-2023 actual PnL {name}", amount)
        self._validate_locked_identity(controlled_run, active)
        self._validate_arithmetic()
        if self.row_hash != canonical_sha256(_actual_pnl_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL row hash must be content-bound")

    def _validate_locked_identity(self, controlled_run: ControlledDevelopmentReconRunBundle, active: dict[str, Any]) -> None:
        fill = active["fill_row"]
        commission = active["commission_row"]
        spread = active["spread_row"]
        valuation = active["valuation_mark"]
        if self.controlled_run_bundle_hash != controlled_run.bundle_hash:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind active controlled-run bundle")
        if self.fill_row_hash != fill["row_hash"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind fill row")
        if self.commission_row_hash != commission["row_hash"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind commission row")
        if self.spread_row_hash != spread["row_hash"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind spread row")
        if Path(self.controlled_run_path).resolve() != _CONTROLLED_RUN_PATH:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL controlled-run path is not locked")
        if Path(self.valuation_mark_pack_path).resolve() != _VALUATION_MARK_PACK_PATH:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation mark pack path is not locked")
        if self.selected_fill_timestamp_utc != EXPECTED_FILL_TIMESTAMP or controlled_run.selected_fill_timestamp_utc != EXPECTED_FILL_TIMESTAMP:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL fill timestamp is not locked")
        if self.valuation_mark_completed_timestamp_utc != valuation["completed_timestamp_utc"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind valuation mark timestamp")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL or self.raw_symbol != valuation["raw_symbol"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL raw symbol must bind active rows")
        if self.filled_order_side != fill["order_side"] or self.filled_order_side != "BUY":
            raise CarverBlocked("S27 v2 pre-2023 actual PnL is locked to the BUY fill")
        if self.fill_quantity != int(fill["fill_quantity"]) or self.position_after_fill != int(fill["position_after_fill"]):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL fill quantity/position must bind fill row")
        if self.fill_price != float(fill["fill_price"]):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL fill price must bind fill row")
        if self.valuation_mark_close_price != float(valuation["close_price"]):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation mark close must bind declared mark row")
        if self.valuation_mark_manifest_sha256 != active["valuation_manifest_sha256"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind valuation manifest bytes")
        if self.valuation_mark_csv_sha256 != active["valuation_csv_sha256"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind valuation CSV bytes")
        if self.valuation_mark_local_audit_sha256 != active["valuation_local_audit_sha256"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind valuation local-audit bytes")
        if self.valuation_mark_strategy_ledger_line_sha256 != active["valuation_strategy_ledger_line_sha256"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind valuation source-ledger line bytes")
        if self.valuation_mark_raw_provider_line_sha256 != active["valuation_raw_provider_line_sha256"]:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind valuation raw-provider line bytes")

    def _validate_arithmetic(self) -> None:
        if self.contract_point_value != CONTRACT_POINT_VALUE:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL point value must bind static ZN point value")
        if self.contract_point_value_currency != CONTRACT_POINT_VALUE_CURRENCY or self.pnl_currency != "USD":
            raise CarverBlocked("S27 v2 pre-2023 actual PnL currency must be USD")
        if self.contract_point_value_source_label != CONTRACT_POINT_VALUE_SOURCE_LABEL:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL point-value source label is not locked")
        if self.valuation_convention_label != VALUATION_CONVENTION_LABEL:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation convention label is not locked")
        if self.valuation_convention_name != VALUATION_CONVENTION_NAME:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation convention name is not locked")
        if self.valuation_convention_hash != _policy_hash(
            "valuation_convention",
            VALUATION_CONVENTION_LABEL,
            VALUATION_CONVENTION_NAME,
            self.valuation_mark_manifest_sha256,
            self.valuation_mark_csv_sha256,
            self.valuation_mark_local_audit_sha256,
        ):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation convention hash must bind mark evidence")
        if self.pnl_direction_label != PNL_DIRECTION_LABEL:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL direction label is not locked")
        expected_gross = (self.valuation_mark_close_price - self.fill_price) * abs(self.fill_quantity) * CONTRACT_POINT_VALUE
        expected_total_cost = self.commission_cost_amount + self.spread_cost_amount
        expected_net = expected_gross - expected_total_cost
        if self.gross_pnl_amount != expected_gross:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL gross amount must bind long mark-to-market formula")
        if self.total_cost_amount != expected_total_cost:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL total cost must equal commission plus spread")
        if self.net_pnl_amount != expected_net:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL net amount must equal gross minus cost")
        if self.pnl_formula_hash != _policy_hash(
            "actual_pnl_formula",
            PNL_DIRECTION_LABEL,
            self.fill_price,
            self.valuation_mark_close_price,
            self.fill_quantity,
            CONTRACT_POINT_VALUE,
            self.gross_pnl_amount,
            self.total_cost_amount,
            self.net_pnl_amount,
            "USD",
        ):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL formula hash must bind arithmetic")
        if self.result_status != RESULT_STATUS or self.backtest_status != BACKTEST_STATUS:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL result/backtest gates must stay fail-closed")
        if self.pnl_evaluation_status != PNL_EVALUATION_STATUS:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL evaluation status is not locked")
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
            raise CarverBlocked("S27 v2 pre-2023 actual PnL cannot emit result/evaluation/source-faithful evidence")


@dataclass(frozen=True)
class Pre2023DevelopmentReconActualPnlBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    controlled_run_path: str
    valuation_mark_pack_path: str
    output_root: str
    controlled_run_bundle: ControlledDevelopmentReconRunBundle
    actual_pnl_row: Pre2023DevelopmentReconActualPnlLedgerRow
    actual_pnl_rows_emitted: bool
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    evidence_manifest_metadata_emitted: bool
    trusted_bundle_metadata_emitted: bool
    result_rows_emitted: bool
    result_scored_run_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = ACTUAL_PNL_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_PRE2023_ACTUAL_PNL_STATUS:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL bundle status is not locked")
        if self.authorization_label != S27_V2_PRE2023_ACTUAL_PNL_AUTHORIZATION:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must remain S27_V2 ZN only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL lane must remain source-native futures")
        if Path(self.controlled_run_path).resolve() != _CONTROLLED_RUN_PATH:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL controlled-run path is not locked")
        if Path(self.valuation_mark_pack_path).resolve() != _VALUATION_MARK_PACK_PATH:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation mark pack path is not locked")
        if Path(self.output_root).resolve() != _PRE2023_ACTUAL_PNL_OUTPUT_PATH:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL output root is not locked")
        active_run = _load_and_verify_controlled_run()
        if self.controlled_run_bundle != active_run:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must bind active controlled run")
        active = _load_active_evidence()
        self.actual_pnl_row._validate_against_active_evidence(active_run, active)
        if self.actual_pnl_row != _build_active_actual_pnl_row(active_run, active):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL row must match active local evidence")
        if any(
            flag is not True
            for flag in (
                self.actual_pnl_rows_emitted,
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.evidence_manifest_metadata_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must emit authorized PnL/metadata rows")
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
            raise CarverBlocked("S27 v2 pre-2023 actual PnL cannot emit result/evaluation/source-faithful evidence")
        if self.non_authorizations != ACTUAL_PNL_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 pre-2023 actual PnL must preserve non-authorizations")
        require_hash("S27 v2 pre-2023 actual PnL bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_actual_pnl_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 pre-2023 actual PnL bundle hash must be content-bound")


def build_pre2023_development_recon_actual_pnl(
    output_root: str | Path = _PRE2023_ACTUAL_PNL_OUTPUT_PATH,
) -> Pre2023DevelopmentReconActualPnlBundle:
    out = Path(output_root).resolve()
    if out != _PRE2023_ACTUAL_PNL_OUTPUT_PATH:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL output root is locked")
    controlled_run = _load_and_verify_controlled_run()
    active = _load_active_evidence()
    actual_pnl_row = _build_active_actual_pnl_row(controlled_run, active)
    bundle = Pre2023DevelopmentReconActualPnlBundle(
        status=S27_V2_PRE2023_ACTUAL_PNL_STATUS,
        authorization_label=S27_V2_PRE2023_ACTUAL_PNL_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        controlled_run_path=str(_CONTROLLED_RUN_PATH),
        valuation_mark_pack_path=str(_VALUATION_MARK_PACK_PATH),
        output_root=str(out),
        controlled_run_bundle=controlled_run,
        actual_pnl_row=actual_pnl_row,
        actual_pnl_rows_emitted=True,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        evidence_manifest_metadata_emitted=True,
        trusted_bundle_metadata_emitted=True,
        result_rows_emitted=False,
        result_scored_run_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = Pre2023DevelopmentReconActualPnlBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_actual_pnl_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    _write_output_artifacts(out, bundle)
    return bundle


def _load_and_verify_controlled_run() -> ControlledDevelopmentReconRunBundle:
    bundle_path = _CONTROLLED_RUN_PATH / "run_bundle.json"
    if _sha256(bundle_path) != _EXPECTED_CONTROLLED_RUN_BUNDLE_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL controlled-run bundle byte hash is not pinned")
    payload = json.loads(bundle_path.read_text(encoding="ascii"))
    payload["non_authorizations"] = tuple(payload["non_authorizations"])
    bundle = ControlledDevelopmentReconRunBundle(**payload)
    bundle.validate()
    if bundle.bundle_hash != canonical_sha256(_run_bundle_payload(bundle)):
        raise CarverBlocked("S27 v2 pre-2023 actual PnL controlled-run bundle hash is not content-bound")
    return bundle


def _load_active_evidence() -> dict[str, Any]:
    if _sha256(_CONTROLLED_RUN_PATH / "fill_ledger.csv") != _EXPECTED_FILL_LEDGER_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL fill ledger byte hash is not pinned")
    if _sha256(_CONTROLLED_RUN_PATH / "commission_ledger.csv") != _EXPECTED_COMMISSION_LEDGER_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL commission ledger byte hash is not pinned")
    if _sha256(_CONTROLLED_RUN_PATH / "spread_cost_ledger.csv") != _EXPECTED_SPREAD_LEDGER_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL spread ledger byte hash is not pinned")
    valuation_manifest_path = _VALUATION_MARK_PACK_PATH / _VALUATION_MARK_MANIFEST_NAME
    valuation_csv_path = _VALUATION_MARK_PACK_PATH / _VALUATION_MARK_CSV_NAME
    if _sha256(valuation_manifest_path) != _EXPECTED_VALUATION_MARK_MANIFEST_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation manifest byte hash is not pinned")
    if _sha256(valuation_csv_path) != _EXPECTED_VALUATION_MARK_CSV_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation CSV byte hash is not pinned")
    if _sha256(_VALUATION_MARK_LOCAL_AUDIT_RECORD_PATH) != _EXPECTED_VALUATION_MARK_LOCAL_AUDIT_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation local-audit byte hash is not pinned")
    fill_rows = _read_csv_rows(_CONTROLLED_RUN_PATH / "fill_ledger.csv")
    commission_rows = _read_csv_rows(_CONTROLLED_RUN_PATH / "commission_ledger.csv")
    spread_rows = _read_csv_rows(_CONTROLLED_RUN_PATH / "spread_cost_ledger.csv")
    valuation_rows = _read_csv_rows(valuation_csv_path)
    if len(fill_rows) != 1 or len(commission_rows) != 1 or len(spread_rows) != 1 or len(valuation_rows) != 1:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL expects one active fill/cost/mark row")
    manifest = json.loads(valuation_manifest_path.read_text(encoding="ascii"))
    _validate_valuation_manifest(manifest, valuation_rows[0])
    return {
        "fill_row": fill_rows[0],
        "commission_row": commission_rows[0],
        "spread_row": spread_rows[0],
        "valuation_mark": valuation_rows[0],
        "valuation_manifest_sha256": _EXPECTED_VALUATION_MARK_MANIFEST_SHA256,
        "valuation_csv_sha256": _EXPECTED_VALUATION_MARK_CSV_SHA256,
        "valuation_local_audit_sha256": _EXPECTED_VALUATION_MARK_LOCAL_AUDIT_SHA256,
        "valuation_strategy_ledger_line_sha256": str(
            manifest["source_files"]["strategy_facing_hourly_available_bars"]["selected_line_sha256"]
        ).lower(),
        "valuation_raw_provider_line_sha256": str(
            manifest["source_files"]["raw_provider_hourly_csv"]["selected_line_sha256"]
        ).lower(),
    }


def _validate_valuation_manifest(manifest: dict[str, Any], mark_row: dict[str, str]) -> None:
    if manifest.get("status") != "LOCAL_PRE2023_VALUATION_MARK_ROW_DECLARED_NOT_PNL_NOT_RESULT":
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation mark status is not locked")
    if manifest.get("source_fill_timestamp_utc") != EXPECTED_FILL_TIMESTAMP:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation mark fill timestamp is not locked")
    if manifest.get("valuation_mark_completed_timestamp_utc") != EXPECTED_VALUATION_MARK_TIMESTAMP:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation mark timestamp is not locked")
    if manifest.get("valuation_mark_is_strictly_after_fill") != "YES":
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation mark must be strictly after fill")
    if manifest.get("raw_symbol") != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation mark raw symbol is not locked")
    if manifest.get("valuation_convention_label") != VALUATION_CONVENTION_LABEL:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation convention label is not locked")
    if mark_row["completed_timestamp_utc"] != EXPECTED_VALUATION_MARK_TIMESTAMP:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL mark CSV timestamp is not locked")
    if mark_row["raw_symbol"] != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL mark CSV raw symbol is not locked")
    if mark_row["valuation_convention_label"] != VALUATION_CONVENTION_LABEL:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL mark CSV convention label is not locked")
    if str(manifest["row_family_files"][_VALUATION_MARK_CSV_NAME]["sha256"]).lower() != _EXPECTED_VALUATION_MARK_CSV_SHA256:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL valuation CSV hash must bind manifest")


def _build_active_actual_pnl_row(
    controlled_run: ControlledDevelopmentReconRunBundle,
    active: dict[str, Any],
) -> Pre2023DevelopmentReconActualPnlLedgerRow:
    fill = active["fill_row"]
    commission = active["commission_row"]
    spread = active["spread_row"]
    valuation = active["valuation_mark"]
    fill_price = float(fill["fill_price"])
    mark_price = float(valuation["close_price"])
    fill_quantity = int(fill["fill_quantity"])
    gross_pnl = (mark_price - fill_price) * abs(fill_quantity) * CONTRACT_POINT_VALUE
    commission_amount = float(commission["commission_amount"])
    spread_amount = float(spread["spread_cost_amount"])
    total_cost = commission_amount + spread_amount
    net_pnl = gross_pnl - total_cost
    valuation_convention_hash = _policy_hash(
        "valuation_convention",
        VALUATION_CONVENTION_LABEL,
        VALUATION_CONVENTION_NAME,
        active["valuation_manifest_sha256"],
        active["valuation_csv_sha256"],
        active["valuation_local_audit_sha256"],
    )
    pnl_formula_hash = _policy_hash(
        "actual_pnl_formula",
        PNL_DIRECTION_LABEL,
        fill_price,
        mark_price,
        fill_quantity,
        CONTRACT_POINT_VALUE,
        gross_pnl,
        total_cost,
        net_pnl,
        "USD",
    )
    row = Pre2023DevelopmentReconActualPnlLedgerRow(
        ledger_label="PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER",
        row_status=ACTUAL_PNL_ROW_STATUS,
        reason_code=ACTUAL_PNL_REASON_CODE,
        controlled_run_bundle_hash=controlled_run.bundle_hash,
        fill_row_hash=fill["row_hash"],
        commission_row_hash=commission["row_hash"],
        spread_row_hash=spread["row_hash"],
        valuation_mark_manifest_sha256=active["valuation_manifest_sha256"],
        valuation_mark_csv_sha256=active["valuation_csv_sha256"],
        valuation_mark_local_audit_sha256=active["valuation_local_audit_sha256"],
        valuation_mark_strategy_ledger_line_sha256=active["valuation_strategy_ledger_line_sha256"],
        valuation_mark_raw_provider_line_sha256=active["valuation_raw_provider_line_sha256"],
        controlled_run_path=str(_CONTROLLED_RUN_PATH),
        valuation_mark_pack_path=str(_VALUATION_MARK_PACK_PATH),
        selected_fill_timestamp_utc=controlled_run.selected_fill_timestamp_utc,
        valuation_mark_completed_timestamp_utc=valuation["completed_timestamp_utc"],
        raw_symbol=controlled_run.raw_symbol,
        filled_order_side=fill["order_side"],
        fill_quantity=fill_quantity,
        position_after_fill=int(fill["position_after_fill"]),
        fill_price=fill_price,
        valuation_mark_close_price=mark_price,
        contract_point_value=CONTRACT_POINT_VALUE,
        contract_point_value_currency=CONTRACT_POINT_VALUE_CURRENCY,
        contract_point_value_source_label=CONTRACT_POINT_VALUE_SOURCE_LABEL,
        valuation_convention_label=VALUATION_CONVENTION_LABEL,
        valuation_convention_name=VALUATION_CONVENTION_NAME,
        valuation_convention_hash=valuation_convention_hash,
        pnl_direction_label=PNL_DIRECTION_LABEL,
        gross_pnl_amount=gross_pnl,
        commission_cost_amount=commission_amount,
        spread_cost_amount=spread_amount,
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
    row = Pre2023DevelopmentReconActualPnlLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_actual_pnl_row_hash_payload(row))}
    )
    row._validate_against_active_evidence(controlled_run, active)
    return row


def _write_output_artifacts(output_root: Path, bundle: Pre2023DevelopmentReconActualPnlBundle) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    validation_row = _validation_metadata_row(bundle)
    provenance_row = _provenance_metadata_row(bundle)
    _write_csv(output_root / "actual_pnl_ledger.csv", [_as_plain_dict(bundle.actual_pnl_row)])
    _write_csv(output_root / "validation_metadata_ledger.csv", [validation_row])
    _write_csv(output_root / "provenance_hash_metadata_ledger.csv", [provenance_row])
    _write_json(output_root / "actual_pnl_bundle.json", _actual_pnl_bundle_json(bundle))
    evidence_manifest = {
        "artifact": "S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_EVIDENCE_MANIFEST_METADATA",
        "status": "LOCAL_ACTUAL_PNL_EVIDENCE_MANIFEST_METADATA_NOT_RESULT_NOT_SOURCE_FAITHFUL",
        "actual_pnl_bundle_hash": bundle.bundle_hash,
        "actual_pnl_row_hash": bundle.actual_pnl_row.row_hash,
        "validation_metadata_row_hash": validation_row["row_hash"],
        "provenance_metadata_row_hash": provenance_row["row_hash"],
        "ledger_hashes": {
            "actual_pnl_ledger.csv": _sha256(output_root / "actual_pnl_ledger.csv"),
            "validation_metadata_ledger.csv": _sha256(output_root / "validation_metadata_ledger.csv"),
            "provenance_hash_metadata_ledger.csv": _sha256(output_root / "provenance_hash_metadata_ledger.csv"),
            "actual_pnl_bundle.json": _sha256(output_root / "actual_pnl_bundle.json"),
        },
        "result_rows_emitted": False,
        "source_faithful_evidence_claimed": False,
    }
    _write_json(output_root / "evidence_manifest.json", evidence_manifest)
    trusted_bundle = {
        "artifact": "S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_TRUSTED_BUNDLE_METADATA",
        "status": "LOCAL_ACTUAL_PNL_TRUSTED_BUNDLE_METADATA_NOT_RESULT_NOT_PROMOTION",
        "actual_pnl_bundle_hash": bundle.bundle_hash,
        "actual_pnl_row_hash": bundle.actual_pnl_row.row_hash,
        "evidence_manifest_hash": _sha256(output_root / "evidence_manifest.json"),
        "result_status": RESULT_STATUS,
        "backtest_status": BACKTEST_STATUS,
        "pnl_evaluation_status": PNL_EVALUATION_STATUS,
        "result_rows_emitted": False,
        "source_faithful_evidence_claimed": False,
        "non_authorizations": ACTUAL_PNL_NON_AUTHORIZATIONS,
    }
    _write_json(output_root / "trusted_bundle.json", trusted_bundle)
    _write_sha256s(output_root)


def _validation_metadata_row(bundle: Pre2023DevelopmentReconActualPnlBundle) -> dict[str, Any]:
    row = {
        "ledger_label": "PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_VALIDATION_METADATA",
        "row_status": "LOCAL_ACTUAL_PNL_VALIDATION_METADATA_NOT_RESULT",
        "actual_pnl_bundle_hash": bundle.bundle_hash,
        "actual_pnl_row_hash": bundle.actual_pnl_row.row_hash,
        "controlled_run_bundle_hash": bundle.controlled_run_bundle.bundle_hash,
        "valuation_mark_manifest_sha256": bundle.actual_pnl_row.valuation_mark_manifest_sha256,
        "result_status": RESULT_STATUS,
        "backtest_status": BACKTEST_STATUS,
        "pnl_evaluation_status": PNL_EVALUATION_STATUS,
        "result_rows_emitted": False,
        "result_scored_run_emitted": False,
        "result_interpretation_emitted": False,
        "pnl_evaluation_emitted": False,
        "source_faithful_evidence_claimed": False,
    }
    row["row_hash"] = canonical_sha256(row)
    return row


def _provenance_metadata_row(bundle: Pre2023DevelopmentReconActualPnlBundle) -> dict[str, Any]:
    row = {
        "ledger_label": "PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_PROVENANCE_HASH_METADATA",
        "row_status": "LOCAL_ACTUAL_PNL_PROVENANCE_HASH_METADATA_NOT_RESULT",
        "controlled_run_path": bundle.controlled_run_path,
        "valuation_mark_pack_path": bundle.valuation_mark_pack_path,
        "output_root": bundle.output_root,
        "controlled_run_bundle_hash": bundle.controlled_run_bundle.bundle_hash,
        "fill_row_hash": bundle.actual_pnl_row.fill_row_hash,
        "commission_row_hash": bundle.actual_pnl_row.commission_row_hash,
        "spread_row_hash": bundle.actual_pnl_row.spread_row_hash,
        "valuation_mark_manifest_sha256": bundle.actual_pnl_row.valuation_mark_manifest_sha256,
        "valuation_mark_csv_sha256": bundle.actual_pnl_row.valuation_mark_csv_sha256,
        "valuation_mark_local_audit_sha256": bundle.actual_pnl_row.valuation_mark_local_audit_sha256,
        "actual_pnl_row_hash": bundle.actual_pnl_row.row_hash,
        "actual_pnl_bundle_hash": bundle.bundle_hash,
    }
    row["row_hash"] = canonical_sha256(row)
    return row


def _actual_pnl_bundle_json(bundle: Pre2023DevelopmentReconActualPnlBundle) -> dict[str, Any]:
    return {
        "artifact": "S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_BUNDLE",
        "status": bundle.status,
        "authorization_label": bundle.authorization_label,
        "strategy_id": bundle.strategy_id,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "controlled_run_path": bundle.controlled_run_path,
        "valuation_mark_pack_path": bundle.valuation_mark_pack_path,
        "output_root": bundle.output_root,
        "controlled_run_bundle_hash": bundle.controlled_run_bundle.bundle_hash,
        "actual_pnl_row_hash": bundle.actual_pnl_row.row_hash,
        "gross_pnl_amount": bundle.actual_pnl_row.gross_pnl_amount,
        "commission_cost_amount": bundle.actual_pnl_row.commission_cost_amount,
        "spread_cost_amount": bundle.actual_pnl_row.spread_cost_amount,
        "net_pnl_amount": bundle.actual_pnl_row.net_pnl_amount,
        "pnl_currency": bundle.actual_pnl_row.pnl_currency,
        "result_status": RESULT_STATUS,
        "backtest_status": BACKTEST_STATUS,
        "pnl_evaluation_status": PNL_EVALUATION_STATUS,
        "result_rows_emitted": False,
        "source_faithful_evidence_claimed": False,
        "bundle_hash": bundle.bundle_hash,
        "non_authorizations": bundle.non_authorizations,
    }


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_POLICY", "label": label, "values": values})


def _actual_pnl_row_hash_payload(row: Pre2023DevelopmentReconActualPnlLedgerRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _actual_pnl_bundle_hash_payload(bundle: Pre2023DevelopmentReconActualPnlBundle) -> dict[str, object]:
    return {
        "actual_pnl_row_hash": bundle.actual_pnl_row.row_hash,
        "actual_pnl_rows_emitted": bundle.actual_pnl_rows_emitted,
        "artifact": "S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "controlled_run_bundle_hash": bundle.controlled_run_bundle.bundle_hash,
        "controlled_run_path": bundle.controlled_run_path,
        "evidence_manifest_metadata_emitted": bundle.evidence_manifest_metadata_emitted,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "output_root": bundle.output_root,
        "pnl_evaluation_emitted": bundle.pnl_evaluation_emitted,
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


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise CarverBlocked(f"S27 v2 pre-2023 actual PnL refuses empty CSV: {path.name}")
    return rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise CarverBlocked("S27 v2 pre-2023 actual PnL refuses empty CSV artifacts")
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(value) for key, value in row.items()})


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _write_sha256s(output_root: Path) -> None:
    rows = [
        {"relative_path": path.relative_to(output_root).as_posix(), "sha256": _sha256(path)}
        for path in sorted(output_root.iterdir())
        if path.is_file() and path.name != "SHA256SUMS.csv"
    ]
    _write_csv(output_root / "SHA256SUMS.csv", rows)


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _as_plain_dict(row: object) -> dict[str, Any]:
    return dict(row.__dict__)

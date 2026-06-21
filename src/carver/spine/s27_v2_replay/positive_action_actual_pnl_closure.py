from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .positive_action_actual_pnl_executable import (
    PositiveActionActualPnlExecutableBundle,
    build_positive_action_actual_pnl_executable,
)
from .positive_action_executable import EXPECTED_RAW_SYMBOL, EXPECTED_SELECTED_FILL, POSITIVE_ACTION_PACK_RELATIVE_PATH
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_AUTHORIZATION = (
    "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_ACTUAL_PNL_VALIDATION_PROVENANCE_TRUSTED_BUNDLE_CLOSURE"
)
S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_STATUS = (
    "S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_METADATA_ONLY_NOT_RESULT"
)

ACTUAL_PNL_CLOSURE_VALIDATION_ROW_STATUS = "LOCAL_POSITIVE_ACTION_ACTUAL_PNL_VALIDATION_METADATA_NOT_RESULT"
ACTUAL_PNL_CLOSURE_PROVENANCE_ROW_STATUS = "LOCAL_POSITIVE_ACTION_ACTUAL_PNL_PROVENANCE_HASH_METADATA_NOT_RESULT"
ACTUAL_PNL_CLOSURE_EVIDENCE_ROW_STATUS = "LOCAL_POSITIVE_ACTION_ACTUAL_PNL_EVIDENCE_MANIFEST_METADATA_NOT_RESULT"

ACTUAL_PNL_CLOSURE_VALIDATION_REASON_CODE = "S27_POSITIVE_ACTION_ACTUAL_PNL_VALIDATION_BINDS_LOCAL_PASSED_CHAIN_NOT_RESULT"
ACTUAL_PNL_CLOSURE_PROVENANCE_REASON_CODE = "S27_POSITIVE_ACTION_ACTUAL_PNL_PROVENANCE_BINDS_EXECUTABLE_HASH_CHAIN"
ACTUAL_PNL_CLOSURE_EVIDENCE_REASON_CODE = (
    "S27_POSITIVE_ACTION_ACTUAL_PNL_EVIDENCE_DISTINGUISHES_LEDGER_MECHANICS_FROM_RESULT_EVIDENCE"
)

LOCAL_HOSTILE_AUDIT_PASS_STATUS = "LOCAL_HOSTILE_AUDIT_PASS_ACTUAL_PNL_LEDGER_NOT_RESULT"
MECHANICAL_PNL_LEDGER_STATUS = "MECHANICAL_LOCAL_DEV_RECON_PNL_LEDGER_EMITTED_NOT_RESULT"
METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE = "METADATA_ONLY_NOT_SOURCE_FAITHFUL_REPLAY_EVIDENCE"
FAIL_CLOSED_RESULT_GATE_STATUS = "FAIL_CLOSED_NOT_EMITTED_NOT_AUTHORIZED"
PNL_EVALUATION_NOT_EMITTED_STATUS = "NOT_EMITTED_MECHANICAL_LEDGER_ROW_ONLY"

ACTUAL_PNL_CLOSURE_PASSED_GATE_LABELS = (
    "POSITIVE_ACTION_EXECUTABLE",
    "POSITIVE_ACTION_DESIRED_POSITION",
    "POSITIVE_ACTION_ORDER_PLAN",
    "POSITIVE_ACTION_FILL",
    "POSITIVE_ACTION_ACTUAL_COST",
    "POSITIVE_ACTION_ACTUAL_PNL",
)

ACTUAL_PNL_CLOSURE_FAIL_CLOSED_GATE_LABELS = (
    "RESULT_ROW",
    "BACKTEST_RESULT",
    "RESULT_INTERPRETATION",
    "PNL_EVALUATION",
    "SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)

ACTUAL_PNL_CLOSURE_NON_AUTHORIZATIONS = (
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

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()
_ACTUAL_PNL_LOCAL_AUDIT_RECORD_PATH = (
    _REPO_ROOT / "docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_ACTUAL_PNL_LEDGER_LOCAL_AUDIT_RESULT_2026-06-11.md"
).resolve()
_EXPECTED_ACTUAL_PNL_LOCAL_AUDIT_RECORD_SHA256 = (
    "164fdb2d739afa924cb4be0f17aba697004f1f5153f4362bd2141fc98a504b3b"
)


@dataclass(frozen=True)
class PositiveActionActualPnlClosureValidationMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    actual_pnl_bundle_hash: str
    actual_pnl_row_hash: str
    input_pack_path: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    passed_gate_labels: tuple[str, ...]
    passed_gate_status: str
    fail_closed_gate_labels: tuple[str, ...]
    fail_closed_gate_status: str
    actual_pnl_local_audit_record_sha256: str
    actual_pnl_ledger_emitted: bool
    result_rows_emitted: bool
    backtest_result_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 positive-action actual-PnL closure validation row standalone validation is not authoritative")

    def _validate_against_actual_pnl(self, active_actual_pnl: PositiveActionActualPnlExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_ACTUAL_PNL_VALIDATION_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 actual-PnL closure validation ledger label is not locked")
        if self.row_status != ACTUAL_PNL_CLOSURE_VALIDATION_ROW_STATUS:
            raise CarverBlocked("S27 v2 actual-PnL closure validation row status is not locked")
        if self.reason_code != ACTUAL_PNL_CLOSURE_VALIDATION_REASON_CODE:
            raise CarverBlocked("S27 v2 actual-PnL closure validation reason code is not locked")
        for name, hash_value in (
            ("actual PnL bundle", self.actual_pnl_bundle_hash),
            ("actual PnL row", self.actual_pnl_row_hash),
            ("actual PnL local audit record", self.actual_pnl_local_audit_record_sha256),
            ("validation policy", self.validation_policy_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 actual-PnL closure validation {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("passed gate status", self.passed_gate_status),
            ("fail-closed gate status", self.fail_closed_gate_status),
        ):
            require_text(f"S27 v2 actual-PnL closure validation {name}", value)
        require_non_empty_tuple("S27 v2 actual-PnL closure passed gates", self.passed_gate_labels)
        require_non_empty_tuple("S27 v2 actual-PnL closure fail-closed gates", self.fail_closed_gate_labels)
        if self.actual_pnl_bundle_hash != active_actual_pnl.bundle_hash:
            raise CarverBlocked("S27 v2 actual-PnL closure validation must bind active actual-PnL bundle")
        if self.actual_pnl_row_hash != active_actual_pnl.actual_pnl_row.row_hash:
            raise CarverBlocked("S27 v2 actual-PnL closure validation must bind active actual-PnL row")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 actual-PnL closure validation is locked to the positive-action pack")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL or self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 actual-PnL closure validation fill/raw symbol is not locked")
        if self.passed_gate_labels != ACTUAL_PNL_CLOSURE_PASSED_GATE_LABELS:
            raise CarverBlocked("S27 v2 actual-PnL closure passed gate tuple is not locked")
        if self.passed_gate_status != LOCAL_HOSTILE_AUDIT_PASS_STATUS:
            raise CarverBlocked("S27 v2 actual-PnL closure passed status is not locked")
        if self.fail_closed_gate_labels != ACTUAL_PNL_CLOSURE_FAIL_CLOSED_GATE_LABELS:
            raise CarverBlocked("S27 v2 actual-PnL closure fail-closed gate tuple is not locked")
        if self.fail_closed_gate_status != FAIL_CLOSED_RESULT_GATE_STATUS:
            raise CarverBlocked("S27 v2 actual-PnL closure fail-closed status is not locked")
        if self.actual_pnl_local_audit_record_sha256 != _actual_pnl_local_audit_record_sha256():
            raise CarverBlocked("S27 v2 actual-PnL closure must bind actual-PnL local audit bytes")
        if self.actual_pnl_ledger_emitted is not True:
            raise CarverBlocked("S27 v2 actual-PnL closure must acknowledge actual PnL ledger emission")
        _require_no_result_flags(
            self.result_rows_emitted,
            self.backtest_result_emitted,
            self.result_interpretation_emitted,
            self.pnl_evaluation_emitted,
            self.source_faithful_evidence_claimed,
        )
        if self.validation_policy_hash != _policy_hash(
            "actual_pnl_closure_validation_policy",
            self.actual_pnl_bundle_hash,
            self.actual_pnl_row_hash,
            self.passed_gate_labels,
            self.passed_gate_status,
            self.fail_closed_gate_labels,
            self.fail_closed_gate_status,
            self.actual_pnl_local_audit_record_sha256,
            self.actual_pnl_ledger_emitted,
        ):
            raise CarverBlocked("S27 v2 actual-PnL closure validation policy hash must bind validation state")
        if self.row_hash != canonical_sha256(_validation_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 actual-PnL closure validation row hash must be content-bound")


@dataclass(frozen=True)
class PositiveActionActualPnlClosureProvenanceHashMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    input_pack_path: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    positive_action_bundle_hash: str
    positive_action_row_hash: str
    forecast_component_hash: str
    desired_position_component_hash: str
    order_plan_bundle_hash: str
    limit_order_row_hash: str
    transition_plan_row_hash: str
    fill_bundle_hash: str
    fill_decision_row_hash: str
    limit_fill_row_hash: str
    actual_cost_bundle_hash: str
    actual_cost_row_hash: str
    actual_pnl_bundle_hash: str
    actual_pnl_row_hash: str
    valuation_mark_manifest_sha256: str
    valuation_mark_csv_sha256: str
    valuation_mark_local_audit_sha256: str
    actual_pnl_local_audit_record_sha256: str
    hash_chain_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 positive-action actual-PnL closure provenance row standalone validation is not authoritative")

    def _validate_against_actual_pnl(self, active_actual_pnl: PositiveActionActualPnlExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_ACTUAL_PNL_PROVENANCE_HASH_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 actual-PnL closure provenance ledger label is not locked")
        if self.row_status != ACTUAL_PNL_CLOSURE_PROVENANCE_ROW_STATUS:
            raise CarverBlocked("S27 v2 actual-PnL closure provenance row status is not locked")
        if self.reason_code != ACTUAL_PNL_CLOSURE_PROVENANCE_REASON_CODE:
            raise CarverBlocked("S27 v2 actual-PnL closure provenance reason code is not locked")
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
        ):
            require_text(f"S27 v2 actual-PnL closure provenance {name}", value)
        for name, hash_value in _provenance_hash_items(self):
            require_hash(f"S27 v2 actual-PnL closure provenance {name}", hash_value)
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 actual-PnL closure provenance is locked to the positive-action pack")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL or self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 actual-PnL closure provenance fill/raw symbol is not locked")
        active_hashes = _active_chain_hashes(active_actual_pnl)
        if _provenance_observed_hashes(self) != active_hashes:
            raise CarverBlocked("S27 v2 actual-PnL closure provenance must bind active hash chain")
        if self.actual_pnl_local_audit_record_sha256 != _actual_pnl_local_audit_record_sha256():
            raise CarverBlocked("S27 v2 actual-PnL closure provenance must bind actual-PnL local audit bytes")
        if self.hash_chain_policy_hash != _policy_hash(
            "actual_pnl_closure_hash_chain_policy",
            tuple(active_hashes.items()),
            self.actual_pnl_local_audit_record_sha256,
        ):
            raise CarverBlocked("S27 v2 actual-PnL closure provenance policy hash must bind hash chain")
        if self.row_hash != canonical_sha256(_provenance_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 actual-PnL closure provenance row hash must be content-bound")


@dataclass(frozen=True)
class PositiveActionActualPnlClosureEvidenceManifestMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    actual_pnl_bundle_hash: str
    actual_pnl_row_hash: str
    validation_row_hash: str
    provenance_row_hash: str
    metadata_evidence_status: str
    actual_pnl_ledger_status: str
    result_evidence_status: str
    backtest_evidence_status: str
    pnl_evaluation_status: str
    source_faithful_evidence_status: str
    source_faithful_evidence_claimed: bool
    evidence_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 positive-action actual-PnL closure evidence row standalone validation is not authoritative")

    def _validate_against_actual_pnl(
        self,
        active_actual_pnl: PositiveActionActualPnlExecutableBundle,
        validation_row: PositiveActionActualPnlClosureValidationMetadataRow,
        provenance_row: PositiveActionActualPnlClosureProvenanceHashMetadataRow,
    ) -> None:
        if self.ledger_label != "POSITIVE_ACTION_ACTUAL_PNL_EVIDENCE_MANIFEST_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 actual-PnL closure evidence ledger label is not locked")
        if self.row_status != ACTUAL_PNL_CLOSURE_EVIDENCE_ROW_STATUS:
            raise CarverBlocked("S27 v2 actual-PnL closure evidence row status is not locked")
        if self.reason_code != ACTUAL_PNL_CLOSURE_EVIDENCE_REASON_CODE:
            raise CarverBlocked("S27 v2 actual-PnL closure evidence reason code is not locked")
        for name, hash_value in (
            ("actual PnL bundle", self.actual_pnl_bundle_hash),
            ("actual PnL row", self.actual_pnl_row_hash),
            ("validation row", self.validation_row_hash),
            ("provenance row", self.provenance_row_hash),
            ("evidence policy", self.evidence_policy_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 actual-PnL closure evidence {name} hash", hash_value)
        for name, value in (
            ("metadata status", self.metadata_evidence_status),
            ("actual PnL ledger status", self.actual_pnl_ledger_status),
            ("result evidence status", self.result_evidence_status),
            ("backtest evidence status", self.backtest_evidence_status),
            ("PnL evaluation status", self.pnl_evaluation_status),
            ("source-faithful evidence status", self.source_faithful_evidence_status),
        ):
            require_text(f"S27 v2 actual-PnL closure evidence {name}", value)
        if self.actual_pnl_bundle_hash != active_actual_pnl.bundle_hash:
            raise CarverBlocked("S27 v2 actual-PnL closure evidence must bind active actual-PnL bundle")
        if self.actual_pnl_row_hash != active_actual_pnl.actual_pnl_row.row_hash:
            raise CarverBlocked("S27 v2 actual-PnL closure evidence must bind active actual-PnL row")
        if self.validation_row_hash != validation_row.row_hash or self.provenance_row_hash != provenance_row.row_hash:
            raise CarverBlocked("S27 v2 actual-PnL closure evidence must bind closure rows")
        if self.metadata_evidence_status != METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE:
            raise CarverBlocked("S27 v2 actual-PnL closure metadata status must remain non-source-faithful")
        if self.actual_pnl_ledger_status != MECHANICAL_PNL_LEDGER_STATUS:
            raise CarverBlocked("S27 v2 actual-PnL closure actual-PnL ledger status is not locked")
        for status in (
            self.result_evidence_status,
            self.backtest_evidence_status,
            self.pnl_evaluation_status,
            self.source_faithful_evidence_status,
        ):
            if status != FAIL_CLOSED_RESULT_GATE_STATUS:
                raise CarverBlocked("S27 v2 actual-PnL closure result/evaluation/evidence status must remain fail-closed")
        if self.source_faithful_evidence_claimed is not False:
            raise CarverBlocked("S27 v2 actual-PnL closure cannot claim source-faithful evidence")
        if self.evidence_policy_hash != _policy_hash(
            "actual_pnl_closure_evidence_policy",
            self.metadata_evidence_status,
            self.actual_pnl_ledger_status,
            self.result_evidence_status,
            self.backtest_evidence_status,
            self.pnl_evaluation_status,
            self.source_faithful_evidence_status,
            self.source_faithful_evidence_claimed,
        ):
            raise CarverBlocked("S27 v2 actual-PnL closure evidence policy hash must bind evidence statuses")
        if self.row_hash != canonical_sha256(_evidence_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 actual-PnL closure evidence row hash must be content-bound")


@dataclass(frozen=True)
class PositiveActionActualPnlClosureTrustedBundleMetadata:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    actual_pnl_bundle: PositiveActionActualPnlExecutableBundle
    validation_row: PositiveActionActualPnlClosureValidationMetadataRow
    provenance_row: PositiveActionActualPnlClosureProvenanceHashMetadataRow
    evidence_row: PositiveActionActualPnlClosureEvidenceManifestMetadataRow
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    evidence_manifest_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    actual_pnl_rows_emitted: bool
    result_rows_emitted: bool
    backtest_result_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = ACTUAL_PNL_CLOSURE_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_STATUS:
            raise CarverBlocked("S27 v2 actual-PnL closure status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_AUTHORIZATION:
            raise CarverBlocked("S27 v2 actual-PnL closure authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 actual-PnL closure must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 actual-PnL closure lane must remain source-native futures")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 actual-PnL closure is locked to the positive-action pack")
        active_actual_pnl = build_positive_action_actual_pnl_executable()
        if self.actual_pnl_bundle != active_actual_pnl:
            raise CarverBlocked("S27 v2 actual-PnL closure must bind active actual-PnL bundle")
        active_validation = _build_active_validation_row(_POSITIVE_ACTION_PACK_PATH, active_actual_pnl)
        self.validation_row._validate_against_actual_pnl(active_actual_pnl)
        if self.validation_row != active_validation:
            raise CarverBlocked("S27 v2 actual-PnL closure validation row must match active metadata")
        active_provenance = _build_active_provenance_row(_POSITIVE_ACTION_PACK_PATH, active_actual_pnl)
        self.provenance_row._validate_against_actual_pnl(active_actual_pnl)
        if self.provenance_row != active_provenance:
            raise CarverBlocked("S27 v2 actual-PnL closure provenance row must match active hash chain")
        active_evidence = _build_active_evidence_row(active_actual_pnl, active_validation, active_provenance)
        self.evidence_row._validate_against_actual_pnl(active_actual_pnl, active_validation, active_provenance)
        if self.evidence_row != active_evidence:
            raise CarverBlocked("S27 v2 actual-PnL closure evidence row must match active metadata")
        if any(
            flag is not True
            for flag in (
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.evidence_manifest_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
                self.actual_pnl_rows_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 actual-PnL closure must emit actual-PnL and closure metadata rows")
        _require_no_result_flags(
            self.result_rows_emitted,
            self.backtest_result_emitted,
            self.result_interpretation_emitted,
            self.pnl_evaluation_emitted,
            self.source_faithful_evidence_claimed,
        )
        if self.non_authorizations != ACTUAL_PNL_CLOSURE_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 actual-PnL closure must preserve non-authorizations")
        require_hash("S27 v2 actual-PnL closure bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_trusted_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 actual-PnL closure bundle hash must be content-bound")


def build_positive_action_actual_pnl_closure_metadata(
    input_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
) -> PositiveActionActualPnlClosureTrustedBundleMetadata:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 actual-PnL closure is locked to the positive-action pack")
    actual_pnl_bundle = build_positive_action_actual_pnl_executable()
    validation_row = _build_active_validation_row(pack_path, actual_pnl_bundle)
    provenance_row = _build_active_provenance_row(pack_path, actual_pnl_bundle)
    evidence_row = _build_active_evidence_row(actual_pnl_bundle, validation_row, provenance_row)
    bundle = PositiveActionActualPnlClosureTrustedBundleMetadata(
        status=S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        actual_pnl_bundle=actual_pnl_bundle,
        validation_row=validation_row,
        provenance_row=provenance_row,
        evidence_row=evidence_row,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        evidence_manifest_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        actual_pnl_rows_emitted=True,
        result_rows_emitted=False,
        backtest_result_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionActualPnlClosureTrustedBundleMetadata(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_trusted_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_validation_row(
    pack_path: Path,
    actual_pnl_bundle: PositiveActionActualPnlExecutableBundle,
) -> PositiveActionActualPnlClosureValidationMetadataRow:
    row = PositiveActionActualPnlClosureValidationMetadataRow(
        ledger_label="POSITIVE_ACTION_ACTUAL_PNL_VALIDATION_METADATA_LEDGER",
        row_status=ACTUAL_PNL_CLOSURE_VALIDATION_ROW_STATUS,
        reason_code=ACTUAL_PNL_CLOSURE_VALIDATION_REASON_CODE,
        actual_pnl_bundle_hash=actual_pnl_bundle.bundle_hash,
        actual_pnl_row_hash=actual_pnl_bundle.actual_pnl_row.row_hash,
        input_pack_path=str(pack_path),
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        passed_gate_labels=ACTUAL_PNL_CLOSURE_PASSED_GATE_LABELS,
        passed_gate_status=LOCAL_HOSTILE_AUDIT_PASS_STATUS,
        fail_closed_gate_labels=ACTUAL_PNL_CLOSURE_FAIL_CLOSED_GATE_LABELS,
        fail_closed_gate_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        actual_pnl_local_audit_record_sha256=_actual_pnl_local_audit_record_sha256(),
        actual_pnl_ledger_emitted=True,
        result_rows_emitted=False,
        backtest_result_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = PositiveActionActualPnlClosureValidationMetadataRow(
        **{
            **row.__dict__,
            "validation_policy_hash": _policy_hash(
                "actual_pnl_closure_validation_policy",
                row.actual_pnl_bundle_hash,
                row.actual_pnl_row_hash,
                row.passed_gate_labels,
                row.passed_gate_status,
                row.fail_closed_gate_labels,
                row.fail_closed_gate_status,
                row.actual_pnl_local_audit_record_sha256,
                row.actual_pnl_ledger_emitted,
            ),
        }
    )
    row = PositiveActionActualPnlClosureValidationMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_validation_row_hash_payload(row))}
    )
    row._validate_against_actual_pnl(actual_pnl_bundle)
    return row


def _build_active_provenance_row(
    pack_path: Path,
    actual_pnl_bundle: PositiveActionActualPnlExecutableBundle,
) -> PositiveActionActualPnlClosureProvenanceHashMetadataRow:
    hashes = _active_chain_hashes(actual_pnl_bundle)
    row = PositiveActionActualPnlClosureProvenanceHashMetadataRow(
        ledger_label="POSITIVE_ACTION_ACTUAL_PNL_PROVENANCE_HASH_METADATA_LEDGER",
        row_status=ACTUAL_PNL_CLOSURE_PROVENANCE_ROW_STATUS,
        reason_code=ACTUAL_PNL_CLOSURE_PROVENANCE_REASON_CODE,
        input_pack_path=str(pack_path),
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        positive_action_bundle_hash=hashes["positive_action_bundle_hash"],
        positive_action_row_hash=hashes["positive_action_row_hash"],
        forecast_component_hash=hashes["forecast_component_hash"],
        desired_position_component_hash=hashes["desired_position_component_hash"],
        order_plan_bundle_hash=hashes["order_plan_bundle_hash"],
        limit_order_row_hash=hashes["limit_order_row_hash"],
        transition_plan_row_hash=hashes["transition_plan_row_hash"],
        fill_bundle_hash=hashes["fill_bundle_hash"],
        fill_decision_row_hash=hashes["fill_decision_row_hash"],
        limit_fill_row_hash=hashes["limit_fill_row_hash"],
        actual_cost_bundle_hash=hashes["actual_cost_bundle_hash"],
        actual_cost_row_hash=hashes["actual_cost_row_hash"],
        actual_pnl_bundle_hash=hashes["actual_pnl_bundle_hash"],
        actual_pnl_row_hash=hashes["actual_pnl_row_hash"],
        valuation_mark_manifest_sha256=hashes["valuation_mark_manifest_sha256"],
        valuation_mark_csv_sha256=hashes["valuation_mark_csv_sha256"],
        valuation_mark_local_audit_sha256=hashes["valuation_mark_local_audit_sha256"],
        actual_pnl_local_audit_record_sha256=_actual_pnl_local_audit_record_sha256(),
        hash_chain_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = PositiveActionActualPnlClosureProvenanceHashMetadataRow(
        **{
            **row.__dict__,
            "hash_chain_policy_hash": _policy_hash(
                "actual_pnl_closure_hash_chain_policy",
                tuple(hashes.items()),
                row.actual_pnl_local_audit_record_sha256,
            ),
        }
    )
    row = PositiveActionActualPnlClosureProvenanceHashMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_provenance_row_hash_payload(row))}
    )
    row._validate_against_actual_pnl(actual_pnl_bundle)
    return row


def _build_active_evidence_row(
    actual_pnl_bundle: PositiveActionActualPnlExecutableBundle,
    validation_row: PositiveActionActualPnlClosureValidationMetadataRow,
    provenance_row: PositiveActionActualPnlClosureProvenanceHashMetadataRow,
) -> PositiveActionActualPnlClosureEvidenceManifestMetadataRow:
    row = PositiveActionActualPnlClosureEvidenceManifestMetadataRow(
        ledger_label="POSITIVE_ACTION_ACTUAL_PNL_EVIDENCE_MANIFEST_METADATA_LEDGER",
        row_status=ACTUAL_PNL_CLOSURE_EVIDENCE_ROW_STATUS,
        reason_code=ACTUAL_PNL_CLOSURE_EVIDENCE_REASON_CODE,
        actual_pnl_bundle_hash=actual_pnl_bundle.bundle_hash,
        actual_pnl_row_hash=actual_pnl_bundle.actual_pnl_row.row_hash,
        validation_row_hash=validation_row.row_hash,
        provenance_row_hash=provenance_row.row_hash,
        metadata_evidence_status=METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE,
        actual_pnl_ledger_status=MECHANICAL_PNL_LEDGER_STATUS,
        result_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        backtest_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        pnl_evaluation_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        source_faithful_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        source_faithful_evidence_claimed=False,
        evidence_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = PositiveActionActualPnlClosureEvidenceManifestMetadataRow(
        **{
            **row.__dict__,
            "evidence_policy_hash": _policy_hash(
                "actual_pnl_closure_evidence_policy",
                row.metadata_evidence_status,
                row.actual_pnl_ledger_status,
                row.result_evidence_status,
                row.backtest_evidence_status,
                row.pnl_evaluation_status,
                row.source_faithful_evidence_status,
                row.source_faithful_evidence_claimed,
            ),
        }
    )
    row = PositiveActionActualPnlClosureEvidenceManifestMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_evidence_row_hash_payload(row))}
    )
    row._validate_against_actual_pnl(actual_pnl_bundle, validation_row, provenance_row)
    return row


def _active_chain_hashes(actual_pnl_bundle: PositiveActionActualPnlExecutableBundle) -> dict[str, str]:
    actual_cost_bundle = actual_pnl_bundle.actual_cost_bundle
    fill_bundle = actual_cost_bundle.fill_bundle
    order_plan_bundle = fill_bundle.order_plan_bundle
    positive_action_bundle = order_plan_bundle.positive_action_bundle
    positive_row = positive_action_bundle.positive_action_row
    pnl_row = actual_pnl_bundle.actual_pnl_row
    return {
        "positive_action_bundle_hash": positive_action_bundle.bundle_hash,
        "positive_action_row_hash": positive_row.row_hash,
        "forecast_component_hash": _forecast_component_hash(positive_row),
        "desired_position_component_hash": _desired_position_component_hash(positive_row),
        "order_plan_bundle_hash": order_plan_bundle.bundle_hash,
        "limit_order_row_hash": order_plan_bundle.limit_order_row.row_hash,
        "transition_plan_row_hash": order_plan_bundle.transition_plan_row.row_hash,
        "fill_bundle_hash": fill_bundle.bundle_hash,
        "fill_decision_row_hash": fill_bundle.fill_decision_row.row_hash,
        "limit_fill_row_hash": fill_bundle.limit_fill_row.row_hash,
        "actual_cost_bundle_hash": actual_cost_bundle.bundle_hash,
        "actual_cost_row_hash": actual_cost_bundle.actual_cost_row.row_hash,
        "actual_pnl_bundle_hash": actual_pnl_bundle.bundle_hash,
        "actual_pnl_row_hash": pnl_row.row_hash,
        "valuation_mark_manifest_sha256": pnl_row.valuation_mark_manifest_sha256,
        "valuation_mark_csv_sha256": pnl_row.valuation_mark_csv_sha256,
        "valuation_mark_local_audit_sha256": pnl_row.valuation_mark_local_audit_sha256,
    }


def _forecast_component_hash(positive_row: object) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_POSITIVE_ACTION_FORECAST_COMPONENT",
            "positive_action_row_hash": positive_row.row_hash,
            "sigma_source_row_hash": positive_row.sigma_source_row_hash,
            "ewmac_source_row_hash": positive_row.ewmac_source_row_hash,
            "vqm_source_row_hash": positive_row.vqm_source_row_hash,
            "raw_mean_reversion_forecast_value": positive_row.raw_mean_reversion_forecast_value,
            "risk_adjusted_forecast_after_veto_value": positive_row.risk_adjusted_forecast_after_veto_value,
            "capped_forecast_value": positive_row.capped_forecast_value,
        }
    )


def _desired_position_component_hash(positive_row: object) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_POSITIVE_ACTION_DESIRED_POSITION_COMPONENT",
            "positive_action_row_hash": positive_row.row_hash,
            "base_unrounded_contracts": positive_row.base_unrounded_contracts,
            "desired_unrounded_contracts": positive_row.desired_unrounded_contracts,
            "current_position_before_order": positive_row.current_position_before_order,
            "desired_rounded_position": positive_row.desired_rounded_position,
            "position_change_contracts": positive_row.position_change_contracts,
            "order_required": positive_row.order_required,
            "order_side": positive_row.order_side,
            "order_quantity": positive_row.order_quantity,
        }
    )


def _actual_pnl_local_audit_record_sha256() -> str:
    if not _ACTUAL_PNL_LOCAL_AUDIT_RECORD_PATH.is_file():
        raise CarverBlocked("S27 v2 actual-PnL closure local audit record is missing")
    text = _ACTUAL_PNL_LOCAL_AUDIT_RECORD_PATH.read_text(encoding="utf-8")
    if "LOCAL_HOSTILE_AUDIT_PASS_POSITIVE_ACTION_ACTUAL_PNL_LEDGER" not in text:
        raise CarverBlocked("S27 v2 actual-PnL closure local audit record content is not locked")
    observed = sha256(_ACTUAL_PNL_LOCAL_AUDIT_RECORD_PATH.read_bytes()).hexdigest()
    if observed != _EXPECTED_ACTUAL_PNL_LOCAL_AUDIT_RECORD_SHA256:
        raise CarverBlocked("S27 v2 actual-PnL closure local audit record hash is not pinned")
    return observed


def _provenance_hash_items(row: PositiveActionActualPnlClosureProvenanceHashMetadataRow) -> tuple[tuple[str, str], ...]:
    observed = _provenance_observed_hashes(row)
    return tuple(observed.items()) + (
        ("actual PnL local audit record", row.actual_pnl_local_audit_record_sha256),
        ("hash-chain policy", row.hash_chain_policy_hash),
        ("row", row.row_hash),
    )


def _provenance_observed_hashes(row: PositiveActionActualPnlClosureProvenanceHashMetadataRow) -> dict[str, str]:
    return {
        "positive_action_bundle_hash": row.positive_action_bundle_hash,
        "positive_action_row_hash": row.positive_action_row_hash,
        "forecast_component_hash": row.forecast_component_hash,
        "desired_position_component_hash": row.desired_position_component_hash,
        "order_plan_bundle_hash": row.order_plan_bundle_hash,
        "limit_order_row_hash": row.limit_order_row_hash,
        "transition_plan_row_hash": row.transition_plan_row_hash,
        "fill_bundle_hash": row.fill_bundle_hash,
        "fill_decision_row_hash": row.fill_decision_row_hash,
        "limit_fill_row_hash": row.limit_fill_row_hash,
        "actual_cost_bundle_hash": row.actual_cost_bundle_hash,
        "actual_cost_row_hash": row.actual_cost_row_hash,
        "actual_pnl_bundle_hash": row.actual_pnl_bundle_hash,
        "actual_pnl_row_hash": row.actual_pnl_row_hash,
        "valuation_mark_manifest_sha256": row.valuation_mark_manifest_sha256,
        "valuation_mark_csv_sha256": row.valuation_mark_csv_sha256,
        "valuation_mark_local_audit_sha256": row.valuation_mark_local_audit_sha256,
    }


def _require_no_result_flags(*flags: bool) -> None:
    if any(flag is not False for flag in flags):
        raise CarverBlocked("S27 v2 actual-PnL closure cannot emit result/backtest/evaluation/source-faithful evidence")


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_POLICY", "label": label, "values": values})


def _validation_row_hash_payload(row: PositiveActionActualPnlClosureValidationMetadataRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _provenance_row_hash_payload(row: PositiveActionActualPnlClosureProvenanceHashMetadataRow) -> dict[str, object]:
    return {
        "actual_pnl_local_audit_record_sha256": row.actual_pnl_local_audit_record_sha256,
        "hash_chain": _provenance_observed_hashes(row),
        "hash_chain_policy_hash": row.hash_chain_policy_hash,
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "selected_fill_timestamp_utc": row.selected_fill_timestamp_utc,
    }


def _evidence_row_hash_payload(row: PositiveActionActualPnlClosureEvidenceManifestMetadataRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _trusted_bundle_hash_payload(bundle: PositiveActionActualPnlClosureTrustedBundleMetadata) -> dict[str, object]:
    return {
        "actual_pnl_bundle_hash": bundle.actual_pnl_bundle.bundle_hash,
        "actual_pnl_rows_emitted": bundle.actual_pnl_rows_emitted,
        "artifact": "S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_TRUSTED_BUNDLE_METADATA",
        "authorization_label": bundle.authorization_label,
        "backtest_result_emitted": bundle.backtest_result_emitted,
        "evidence_manifest_metadata_rows_emitted": bundle.evidence_manifest_metadata_rows_emitted,
        "evidence_row_hash": bundle.evidence_row.row_hash,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "pnl_evaluation_emitted": bundle.pnl_evaluation_emitted,
        "provenance_metadata_rows_emitted": bundle.provenance_metadata_rows_emitted,
        "provenance_row_hash": bundle.provenance_row.row_hash,
        "result_interpretation_emitted": bundle.result_interpretation_emitted,
        "result_rows_emitted": bundle.result_rows_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "trusted_bundle_metadata_emitted": bundle.trusted_bundle_metadata_emitted,
        "validation_metadata_rows_emitted": bundle.validation_metadata_rows_emitted,
        "validation_row_hash": bundle.validation_row.row_hash,
    }

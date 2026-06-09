from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .no_pnl_executable import (
    NoPnlExecutableBundle,
    build_no_pnl_executable_metadata,
)
from .runtime_evidence_gate import RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH
from .validation import require_hash, require_integer, require_non_empty_tuple, require_text


S27_V2_NO_RESULT_CLOSURE_AUTHORIZATION = "S27_V2_NO_RESULT_VALIDATION_PROVENANCE_TRUSTED_BUNDLE_CLOSURE"
S27_V2_NO_RESULT_CLOSURE_STATUS = "S27_V2_NO_RESULT_CLOSURE_REMEDIATION_PACK_METADATA_ONLY"

NO_RESULT_VALIDATION_ROW_STATUS = "LOCAL_NO_RESULT_VALIDATION_METADATA_ZERO_ACTION_CHAIN"
NO_RESULT_PROVENANCE_ROW_STATUS = "LOCAL_NO_RESULT_PROVENANCE_HASH_METADATA_ZERO_ACTION_CHAIN"
NO_RESULT_EVIDENCE_ROW_STATUS = "LOCAL_NO_RESULT_EVIDENCE_MANIFEST_METADATA_ZERO_ACTION_CHAIN"

NO_RESULT_VALIDATION_REASON_CODE = "S27_NO_RESULT_VALIDATION_BINDS_EXTERNAL_PASS_ZERO_ACTION_CHAIN"
NO_RESULT_PROVENANCE_REASON_CODE = "S27_NO_RESULT_PROVENANCE_BINDS_EXECUTABLE_METADATA_HASH_CHAIN"
NO_RESULT_EVIDENCE_REASON_CODE = "S27_NO_RESULT_EVIDENCE_MANIFEST_DISTINGUISHES_METADATA_FROM_REPLAY_EVIDENCE"

NO_RESULT_CLOSURE_NON_AUTHORIZATIONS = (
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

EXTERNALLY_PASSED_GATE_LABELS = (
    "FORECAST_EXECUTABLE",
    "DESIRED_POSITION_EXECUTABLE",
    "ORDER_TRANSITION_EXECUTABLE",
    "NO_FILL_EXECUTABLE",
    "NO_COST_EXECUTABLE",
    "NO_PNL_EXECUTABLE",
)

FAIL_CLOSED_RESULT_GATE_LABELS = (
    "ACTUAL_FILL_LEDGER",
    "ACTUAL_COST_LEDGER",
    "ACTUAL_PNL_LEDGER",
    "RESULT_ROW",
    "BACKTEST_RESULT",
    "RESULT_INTERPRETATION",
    "SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)

EXTERNALLY_PASSED_GATE_STATUS = "EXTERNAL_HOSTILE_AUDIT_PASS_NO_RESULT_METADATA_ONLY"
FAIL_CLOSED_RESULT_GATE_STATUS = "FAIL_CLOSED_NOT_EMITTED_NOT_AUTHORIZED"
METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE = "METADATA_ONLY_NOT_SOURCE_FAITHFUL_REPLAY_EVIDENCE"

_REPO_ROOT = Path(__file__).resolve().parents[4]
_REMEDIATION_PACK_PATH = (_REPO_ROOT / RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH).resolve()

_EXTERNAL_PASS_SYNTHESIS_RELATIVE_PATHS = (
    "docs/process/CARVER_S27_ZN_V2_FORECAST_EXECUTABLE_REMEDIATION_PACK_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md",
    "docs/process/CARVER_S27_ZN_V2_DESIRED_POSITION_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md",
    "docs/process/CARVER_S27_ZN_V2_ORDER_TRANSITION_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md",
    "docs/process/CARVER_S27_ZN_V2_NO_FILL_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md",
    "docs/process/CARVER_S27_ZN_V2_NO_COST_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md",
    "docs/process/CARVER_S27_ZN_V2_NO_PNL_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md",
)


@dataclass(frozen=True)
class NoResultValidationMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    no_pnl_bundle_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    raw_symbol: str
    externally_passed_gate_labels: tuple[str, ...]
    externally_passed_gate_status: str
    external_pass_synthesis_hashes: tuple[str, ...]
    fail_closed_result_gate_labels: tuple[str, ...]
    fail_closed_result_gate_status: str
    actual_fill_ledger_emitted: bool
    actual_cost_ledger_emitted: bool
    actual_pnl_ledger_emitted: bool
    result_rows_emitted: bool
    backtest_result_emitted: bool
    result_interpretation_emitted: bool
    source_faithful_evidence_claimed: bool
    no_result_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 no-result validation row standalone validation is not authoritative")

    def _validate_structural_formula(self, active_no_pnl_bundle: NoPnlExecutableBundle) -> None:
        if self.ledger_label != "NO_RESULT_VALIDATION_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 no-result validation ledger label is not locked")
        if self.row_status != NO_RESULT_VALIDATION_ROW_STATUS:
            raise CarverBlocked("S27 v2 no-result validation row status is not locked")
        if self.reason_code != NO_RESULT_VALIDATION_REASON_CODE:
            raise CarverBlocked("S27 v2 no-result validation reason code is not locked")
        require_hash("S27 v2 no-result validation no-PnL bundle hash", self.no_pnl_bundle_hash)
        require_hash("S27 v2 no-result validation policy hash", self.no_result_policy_hash)
        require_hash("S27 v2 no-result validation row hash", self.row_hash)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("external gate status", self.externally_passed_gate_status),
            ("fail-closed result gate status", self.fail_closed_result_gate_status),
        ):
            require_text(f"S27 v2 no-result validation {name}", value)
        require_non_empty_tuple(
            "S27 v2 no-result validation external gate labels",
            self.externally_passed_gate_labels,
        )
        if self.externally_passed_gate_labels != EXTERNALLY_PASSED_GATE_LABELS:
            raise CarverBlocked("S27 v2 no-result validation external gate labels must match locked tuple")
        if self.externally_passed_gate_status != EXTERNALLY_PASSED_GATE_STATUS:
            raise CarverBlocked("S27 v2 no-result validation external gate status is not locked")
        _validate_hash_tuple("S27 v2 no-result validation external synthesis hashes", self.external_pass_synthesis_hashes)
        if self.external_pass_synthesis_hashes != _external_pass_synthesis_hashes():
            raise CarverBlocked("S27 v2 no-result validation must bind active external PASS syntheses")
        require_non_empty_tuple(
            "S27 v2 no-result validation fail-closed gate labels",
            self.fail_closed_result_gate_labels,
        )
        if self.fail_closed_result_gate_labels != FAIL_CLOSED_RESULT_GATE_LABELS:
            raise CarverBlocked("S27 v2 no-result validation fail-closed gates must match locked tuple")
        if self.fail_closed_result_gate_status != FAIL_CLOSED_RESULT_GATE_STATUS:
            raise CarverBlocked("S27 v2 no-result validation fail-closed status is not locked")
        _require_no_result_flags(
            self.actual_fill_ledger_emitted,
            self.actual_cost_ledger_emitted,
            self.actual_pnl_ledger_emitted,
            self.result_rows_emitted,
            self.backtest_result_emitted,
            self.result_interpretation_emitted,
            self.source_faithful_evidence_claimed,
        )
        if self.no_pnl_bundle_hash != active_no_pnl_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 no-result validation must bind active no-PnL bundle")
        if self.input_pack_path != active_no_pnl_bundle.input_pack_path:
            raise CarverBlocked("S27 v2 no-result validation input pack must match active no-PnL bundle")
        if self.selected_decision_timestamp_utc != active_no_pnl_bundle.no_pnl_row.selected_decision_timestamp_utc:
            raise CarverBlocked("S27 v2 no-result validation timestamp must match active no-PnL row")
        if self.raw_symbol != active_no_pnl_bundle.no_pnl_row.raw_symbol:
            raise CarverBlocked("S27 v2 no-result validation raw symbol must match active no-PnL row")
        if self.no_result_policy_hash != _policy_hash(
            "no_result_validation_policy",
            self.externally_passed_gate_labels,
            self.externally_passed_gate_status,
            self.external_pass_synthesis_hashes,
            self.fail_closed_result_gate_labels,
            self.fail_closed_result_gate_status,
        ):
            raise CarverBlocked("S27 v2 no-result validation policy hash must bind gate policy")
        if self.row_hash != canonical_sha256(_validation_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-result validation row hash must be content-bound")


@dataclass(frozen=True)
class NoResultProvenanceHashMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    raw_symbol: str
    forecast_bundle_hash: str
    desired_position_bundle_hash: str
    order_transition_bundle_hash: str
    no_fill_bundle_hash: str
    no_cost_bundle_hash: str
    no_pnl_bundle_hash: str
    forecast_row_hash: str
    desired_position_row_hash: str
    order_intent_row_hash: str
    order_transition_row_hash: str
    no_fill_row_hash: str
    no_cost_row_hash: str
    no_pnl_row_hash: str
    external_pass_synthesis_bundle_hash: str
    no_result_hash_chain_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 no-result provenance row standalone validation is not authoritative")

    def _validate_structural_formula(self, active_no_pnl_bundle: NoPnlExecutableBundle) -> None:
        if self.ledger_label != "NO_RESULT_PROVENANCE_HASH_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 no-result provenance ledger label is not locked")
        if self.row_status != NO_RESULT_PROVENANCE_ROW_STATUS:
            raise CarverBlocked("S27 v2 no-result provenance row status is not locked")
        if self.reason_code != NO_RESULT_PROVENANCE_REASON_CODE:
            raise CarverBlocked("S27 v2 no-result provenance reason code is not locked")
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("raw symbol", self.raw_symbol),
        ):
            require_text(f"S27 v2 no-result provenance {name}", value)
        for name, hash_value in _provenance_hash_items(self):
            require_hash(f"S27 v2 no-result provenance {name}", hash_value)
        active_hashes = _active_chain_hashes(active_no_pnl_bundle)
        observed_hashes = _provenance_observed_hashes(self)
        if observed_hashes != active_hashes:
            raise CarverBlocked("S27 v2 no-result provenance must bind active executable hash chain")
        if self.external_pass_synthesis_bundle_hash != _external_pass_synthesis_bundle_hash():
            raise CarverBlocked("S27 v2 no-result provenance must bind external PASS synthesis bundle")
        if self.no_result_hash_chain_policy_hash != _policy_hash(
            "no_result_provenance_hash_chain_policy",
            tuple(active_hashes.items()),
            self.external_pass_synthesis_bundle_hash,
        ):
            raise CarverBlocked("S27 v2 no-result provenance policy hash must bind hash chain")
        if self.row_hash != canonical_sha256(_provenance_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-result provenance row hash must be content-bound")


@dataclass(frozen=True)
class NoResultEvidenceManifestMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    no_pnl_bundle_hash: str
    validation_row_hash: str
    provenance_row_hash: str
    external_pass_synthesis_bundle_hash: str
    metadata_evidence_status: str
    actual_fill_evidence_status: str
    actual_cost_evidence_status: str
    actual_pnl_evidence_status: str
    result_evidence_status: str
    source_faithful_evidence_status: str
    source_faithful_evidence_claimed: bool
    no_result_evidence_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 no-result evidence row standalone validation is not authoritative")

    def _validate_structural_formula(
        self,
        active_no_pnl_bundle: NoPnlExecutableBundle,
        validation_row: NoResultValidationMetadataRow,
        provenance_row: NoResultProvenanceHashMetadataRow,
    ) -> None:
        if self.ledger_label != "NO_RESULT_EVIDENCE_MANIFEST_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 no-result evidence ledger label is not locked")
        if self.row_status != NO_RESULT_EVIDENCE_ROW_STATUS:
            raise CarverBlocked("S27 v2 no-result evidence row status is not locked")
        if self.reason_code != NO_RESULT_EVIDENCE_REASON_CODE:
            raise CarverBlocked("S27 v2 no-result evidence reason code is not locked")
        for name, hash_value in (
            ("no-PnL bundle hash", self.no_pnl_bundle_hash),
            ("validation row hash", self.validation_row_hash),
            ("provenance row hash", self.provenance_row_hash),
            ("external PASS synthesis bundle hash", self.external_pass_synthesis_bundle_hash),
            ("evidence policy hash", self.no_result_evidence_policy_hash),
            ("row hash", self.row_hash),
        ):
            require_hash(f"S27 v2 no-result evidence {name}", hash_value)
        for name, value in (
            ("metadata evidence status", self.metadata_evidence_status),
            ("actual fill evidence status", self.actual_fill_evidence_status),
            ("actual cost evidence status", self.actual_cost_evidence_status),
            ("actual PnL evidence status", self.actual_pnl_evidence_status),
            ("result evidence status", self.result_evidence_status),
            ("source-faithful evidence status", self.source_faithful_evidence_status),
        ):
            require_text(f"S27 v2 no-result evidence {name}", value)
        if self.no_pnl_bundle_hash != active_no_pnl_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 no-result evidence must bind active no-PnL bundle")
        if self.validation_row_hash != validation_row.row_hash:
            raise CarverBlocked("S27 v2 no-result evidence must bind validation row")
        if self.provenance_row_hash != provenance_row.row_hash:
            raise CarverBlocked("S27 v2 no-result evidence must bind provenance row")
        if self.external_pass_synthesis_bundle_hash != _external_pass_synthesis_bundle_hash():
            raise CarverBlocked("S27 v2 no-result evidence must bind external PASS synthesis bundle")
        if self.metadata_evidence_status != METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE:
            raise CarverBlocked("S27 v2 no-result evidence metadata status must remain non-source-faithful")
        for status in (
            self.actual_fill_evidence_status,
            self.actual_cost_evidence_status,
            self.actual_pnl_evidence_status,
            self.result_evidence_status,
        ):
            if status != FAIL_CLOSED_RESULT_GATE_STATUS:
                raise CarverBlocked("S27 v2 no-result evidence actual-result status must remain fail-closed")
        if self.source_faithful_evidence_status != FAIL_CLOSED_RESULT_GATE_STATUS:
            raise CarverBlocked("S27 v2 no-result evidence source-faithful status must remain fail-closed")
        if self.source_faithful_evidence_claimed is not False:
            raise CarverBlocked("S27 v2 no-result evidence cannot claim source-faithful evidence")
        if self.no_result_evidence_policy_hash != _policy_hash(
            "no_result_evidence_manifest_policy",
            self.metadata_evidence_status,
            self.actual_fill_evidence_status,
            self.actual_cost_evidence_status,
            self.actual_pnl_evidence_status,
            self.result_evidence_status,
            self.source_faithful_evidence_status,
        ):
            raise CarverBlocked("S27 v2 no-result evidence policy hash must bind evidence statuses")
        if self.row_hash != canonical_sha256(_evidence_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-result evidence row hash must be content-bound")


@dataclass(frozen=True)
class NoResultTrustedBundleMetadata:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    no_pnl_bundle: NoPnlExecutableBundle
    validation_row: NoResultValidationMetadataRow
    provenance_row: NoResultProvenanceHashMetadataRow
    evidence_row: NoResultEvidenceManifestMetadataRow
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    evidence_manifest_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    actual_fill_rows_emitted: bool
    actual_cost_rows_emitted: bool
    actual_pnl_rows_emitted: bool
    result_rows_emitted: bool
    backtest_result_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NO_RESULT_CLOSURE_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_NO_RESULT_CLOSURE_STATUS:
            raise CarverBlocked("S27 v2 no-result closure status is not locked")
        if self.authorization_label != S27_V2_NO_RESULT_CLOSURE_AUTHORIZATION:
            raise CarverBlocked("S27 v2 no-result closure authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 no-result closure must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 no-result closure must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 no-result closure is locked to the audited remediation pack")
        active_no_pnl = build_no_pnl_executable_metadata(pack_path)
        if self.no_pnl_bundle != active_no_pnl:
            raise CarverBlocked("S27 v2 no-result closure must bind active no-PnL bundle")
        active_validation = _build_active_validation_row(pack_path, active_no_pnl)
        self.validation_row._validate_structural_formula(active_no_pnl)
        if self.validation_row != active_validation:
            raise CarverBlocked("S27 v2 no-result validation row must match active no-PnL authority")
        active_provenance = _build_active_provenance_row(pack_path, active_no_pnl)
        self.provenance_row._validate_structural_formula(active_no_pnl)
        if self.provenance_row != active_provenance:
            raise CarverBlocked("S27 v2 no-result provenance row must match active hash chain")
        active_evidence = _build_active_evidence_row(active_no_pnl, active_validation, active_provenance)
        self.evidence_row._validate_structural_formula(active_no_pnl, active_validation, active_provenance)
        if self.evidence_row != active_evidence:
            raise CarverBlocked("S27 v2 no-result evidence row must match active closure metadata")
        if any(
            flag is not True
            for flag in (
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.evidence_manifest_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 no-result closure must emit all closure metadata rows")
        _require_no_result_flags(
            self.actual_fill_rows_emitted,
            self.actual_cost_rows_emitted,
            self.actual_pnl_rows_emitted,
            self.result_rows_emitted,
            self.backtest_result_emitted,
            self.result_interpretation_emitted,
            self.pnl_evaluation_emitted,
            self.source_faithful_evidence_claimed,
        )
        if self.non_authorizations != NO_RESULT_CLOSURE_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 no-result closure must preserve non-authorizations")
        require_hash("S27 v2 no-result closure bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_trusted_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 no-result closure bundle hash must be content-bound")


def build_no_result_closure_metadata(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> NoResultTrustedBundleMetadata:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 no-result closure is locked to the audited remediation pack")
    no_pnl_bundle = build_no_pnl_executable_metadata(pack_path)
    validation_row = _build_active_validation_row(pack_path, no_pnl_bundle)
    provenance_row = _build_active_provenance_row(pack_path, no_pnl_bundle)
    evidence_row = _build_active_evidence_row(no_pnl_bundle, validation_row, provenance_row)
    bundle = NoResultTrustedBundleMetadata(
        status=S27_V2_NO_RESULT_CLOSURE_STATUS,
        authorization_label=S27_V2_NO_RESULT_CLOSURE_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        no_pnl_bundle=no_pnl_bundle,
        validation_row=validation_row,
        provenance_row=provenance_row,
        evidence_row=evidence_row,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        evidence_manifest_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        actual_fill_rows_emitted=False,
        actual_cost_rows_emitted=False,
        actual_pnl_rows_emitted=False,
        result_rows_emitted=False,
        backtest_result_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = NoResultTrustedBundleMetadata(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_trusted_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_validation_row(
    pack_path: Path,
    no_pnl_bundle: NoPnlExecutableBundle,
) -> NoResultValidationMetadataRow:
    row = NoResultValidationMetadataRow(
        ledger_label="NO_RESULT_VALIDATION_METADATA_LEDGER",
        row_status=NO_RESULT_VALIDATION_ROW_STATUS,
        reason_code=NO_RESULT_VALIDATION_REASON_CODE,
        no_pnl_bundle_hash=no_pnl_bundle.bundle_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=no_pnl_bundle.no_pnl_row.selected_decision_timestamp_utc,
        raw_symbol=no_pnl_bundle.no_pnl_row.raw_symbol,
        externally_passed_gate_labels=EXTERNALLY_PASSED_GATE_LABELS,
        externally_passed_gate_status=EXTERNALLY_PASSED_GATE_STATUS,
        external_pass_synthesis_hashes=_external_pass_synthesis_hashes(),
        fail_closed_result_gate_labels=FAIL_CLOSED_RESULT_GATE_LABELS,
        fail_closed_result_gate_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        actual_fill_ledger_emitted=False,
        actual_cost_ledger_emitted=False,
        actual_pnl_ledger_emitted=False,
        result_rows_emitted=False,
        backtest_result_emitted=False,
        result_interpretation_emitted=False,
        source_faithful_evidence_claimed=False,
        no_result_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = NoResultValidationMetadataRow(
        **{**row.__dict__, "no_result_policy_hash": _policy_hash(
            "no_result_validation_policy",
            row.externally_passed_gate_labels,
            row.externally_passed_gate_status,
            row.external_pass_synthesis_hashes,
            row.fail_closed_result_gate_labels,
            row.fail_closed_result_gate_status,
        )}
    )
    row = NoResultValidationMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_validation_row_hash_payload(row))}
    )
    row._validate_structural_formula(no_pnl_bundle)
    return row


def _build_active_provenance_row(
    pack_path: Path,
    no_pnl_bundle: NoPnlExecutableBundle,
) -> NoResultProvenanceHashMetadataRow:
    hashes = _active_chain_hashes(no_pnl_bundle)
    row = NoResultProvenanceHashMetadataRow(
        ledger_label="NO_RESULT_PROVENANCE_HASH_METADATA_LEDGER",
        row_status=NO_RESULT_PROVENANCE_ROW_STATUS,
        reason_code=NO_RESULT_PROVENANCE_REASON_CODE,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=no_pnl_bundle.no_pnl_row.selected_decision_timestamp_utc,
        raw_symbol=no_pnl_bundle.no_pnl_row.raw_symbol,
        forecast_bundle_hash=hashes["forecast_bundle_hash"],
        desired_position_bundle_hash=hashes["desired_position_bundle_hash"],
        order_transition_bundle_hash=hashes["order_transition_bundle_hash"],
        no_fill_bundle_hash=hashes["no_fill_bundle_hash"],
        no_cost_bundle_hash=hashes["no_cost_bundle_hash"],
        no_pnl_bundle_hash=hashes["no_pnl_bundle_hash"],
        forecast_row_hash=hashes["forecast_row_hash"],
        desired_position_row_hash=hashes["desired_position_row_hash"],
        order_intent_row_hash=hashes["order_intent_row_hash"],
        order_transition_row_hash=hashes["order_transition_row_hash"],
        no_fill_row_hash=hashes["no_fill_row_hash"],
        no_cost_row_hash=hashes["no_cost_row_hash"],
        no_pnl_row_hash=hashes["no_pnl_row_hash"],
        external_pass_synthesis_bundle_hash=_external_pass_synthesis_bundle_hash(),
        no_result_hash_chain_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = NoResultProvenanceHashMetadataRow(
        **{**row.__dict__, "no_result_hash_chain_policy_hash": _policy_hash(
            "no_result_provenance_hash_chain_policy",
            tuple(hashes.items()),
            row.external_pass_synthesis_bundle_hash,
        )}
    )
    row = NoResultProvenanceHashMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_provenance_row_hash_payload(row))}
    )
    row._validate_structural_formula(no_pnl_bundle)
    return row


def _build_active_evidence_row(
    no_pnl_bundle: NoPnlExecutableBundle,
    validation_row: NoResultValidationMetadataRow,
    provenance_row: NoResultProvenanceHashMetadataRow,
) -> NoResultEvidenceManifestMetadataRow:
    row = NoResultEvidenceManifestMetadataRow(
        ledger_label="NO_RESULT_EVIDENCE_MANIFEST_METADATA_LEDGER",
        row_status=NO_RESULT_EVIDENCE_ROW_STATUS,
        reason_code=NO_RESULT_EVIDENCE_REASON_CODE,
        no_pnl_bundle_hash=no_pnl_bundle.bundle_hash,
        validation_row_hash=validation_row.row_hash,
        provenance_row_hash=provenance_row.row_hash,
        external_pass_synthesis_bundle_hash=_external_pass_synthesis_bundle_hash(),
        metadata_evidence_status=METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE,
        actual_fill_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        actual_cost_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        actual_pnl_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        result_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        source_faithful_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        source_faithful_evidence_claimed=False,
        no_result_evidence_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = NoResultEvidenceManifestMetadataRow(
        **{**row.__dict__, "no_result_evidence_policy_hash": _policy_hash(
            "no_result_evidence_manifest_policy",
            row.metadata_evidence_status,
            row.actual_fill_evidence_status,
            row.actual_cost_evidence_status,
            row.actual_pnl_evidence_status,
            row.result_evidence_status,
            row.source_faithful_evidence_status,
        )}
    )
    row = NoResultEvidenceManifestMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_evidence_row_hash_payload(row))}
    )
    row._validate_structural_formula(no_pnl_bundle, validation_row, provenance_row)
    return row


def _active_chain_hashes(no_pnl_bundle: NoPnlExecutableBundle) -> dict[str, str]:
    no_cost_bundle = no_pnl_bundle.no_cost_bundle
    no_fill_bundle = no_cost_bundle.no_fill_bundle
    order_transition_bundle = no_fill_bundle.order_transition_bundle
    desired_position_bundle = order_transition_bundle.desired_position_bundle
    forecast_bundle = desired_position_bundle.forecast_bundle
    return {
        "forecast_bundle_hash": forecast_bundle.bundle_hash,
        "desired_position_bundle_hash": desired_position_bundle.bundle_hash,
        "order_transition_bundle_hash": order_transition_bundle.bundle_hash,
        "no_fill_bundle_hash": no_fill_bundle.bundle_hash,
        "no_cost_bundle_hash": no_cost_bundle.bundle_hash,
        "no_pnl_bundle_hash": no_pnl_bundle.bundle_hash,
        "forecast_row_hash": forecast_bundle.forecast_row.row_hash,
        "desired_position_row_hash": desired_position_bundle.desired_position_row.row_hash,
        "order_intent_row_hash": order_transition_bundle.order_intent_row.row_hash,
        "order_transition_row_hash": order_transition_bundle.order_transition_row.row_hash,
        "no_fill_row_hash": no_fill_bundle.no_fill_row.row_hash,
        "no_cost_row_hash": no_cost_bundle.no_cost_row.row_hash,
        "no_pnl_row_hash": no_pnl_bundle.no_pnl_row.row_hash,
    }


def _external_pass_synthesis_hashes() -> tuple[str, ...]:
    hashes: list[str] = []
    for relative_path in _EXTERNAL_PASS_SYNTHESIS_RELATIVE_PATHS:
        path = (_REPO_ROOT / relative_path).resolve()
        if not path.is_file():
            raise CarverBlocked("S27 v2 no-result closure external PASS synthesis file is missing")
        hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
    return tuple(hashes)


def _external_pass_synthesis_bundle_hash() -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_NO_RESULT_EXTERNAL_PASS_SYNTHESIS_BUNDLE",
            "labels": EXTERNALLY_PASSED_GATE_LABELS,
            "paths": _EXTERNAL_PASS_SYNTHESIS_RELATIVE_PATHS,
            "sha256": _external_pass_synthesis_hashes(),
        }
    )


def _validate_hash_tuple(name: str, values: tuple[str, ...]) -> None:
    require_non_empty_tuple(name, values)
    if len(values) != len(EXTERNALLY_PASSED_GATE_LABELS):
        raise CarverBlocked(f"{name} must match external PASS gate count")
    for value in values:
        require_hash(name, value)


def _require_no_result_flags(*flags: bool) -> None:
    if any(flag is not False for flag in flags):
        raise CarverBlocked("S27 v2 no-result closure cannot emit result/PnL/backtest/evidence")


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_NO_RESULT_CLOSURE_POLICY", "label": label, "values": values})


def _provenance_hash_items(row: NoResultProvenanceHashMetadataRow) -> tuple[tuple[str, str], ...]:
    observed = _provenance_observed_hashes(row)
    return tuple(observed.items()) + (
        ("external PASS synthesis bundle hash", row.external_pass_synthesis_bundle_hash),
        ("no-result hash-chain policy hash", row.no_result_hash_chain_policy_hash),
        ("row hash", row.row_hash),
    )


def _provenance_observed_hashes(row: NoResultProvenanceHashMetadataRow) -> dict[str, str]:
    return {
        "forecast_bundle_hash": row.forecast_bundle_hash,
        "desired_position_bundle_hash": row.desired_position_bundle_hash,
        "order_transition_bundle_hash": row.order_transition_bundle_hash,
        "no_fill_bundle_hash": row.no_fill_bundle_hash,
        "no_cost_bundle_hash": row.no_cost_bundle_hash,
        "no_pnl_bundle_hash": row.no_pnl_bundle_hash,
        "forecast_row_hash": row.forecast_row_hash,
        "desired_position_row_hash": row.desired_position_row_hash,
        "order_intent_row_hash": row.order_intent_row_hash,
        "order_transition_row_hash": row.order_transition_row_hash,
        "no_fill_row_hash": row.no_fill_row_hash,
        "no_cost_row_hash": row.no_cost_row_hash,
        "no_pnl_row_hash": row.no_pnl_row_hash,
    }


def _validation_row_hash_payload(row: NoResultValidationMetadataRow) -> dict[str, object]:
    return {
        "actual_cost_ledger_emitted": row.actual_cost_ledger_emitted,
        "actual_fill_ledger_emitted": row.actual_fill_ledger_emitted,
        "actual_pnl_ledger_emitted": row.actual_pnl_ledger_emitted,
        "backtest_result_emitted": row.backtest_result_emitted,
        "external_pass_synthesis_hashes": row.external_pass_synthesis_hashes,
        "externally_passed_gate_labels": row.externally_passed_gate_labels,
        "externally_passed_gate_status": row.externally_passed_gate_status,
        "fail_closed_result_gate_labels": row.fail_closed_result_gate_labels,
        "fail_closed_result_gate_status": row.fail_closed_result_gate_status,
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "no_pnl_bundle_hash": row.no_pnl_bundle_hash,
        "no_result_policy_hash": row.no_result_policy_hash,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "result_interpretation_emitted": row.result_interpretation_emitted,
        "result_rows_emitted": row.result_rows_emitted,
        "row_status": row.row_status,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "source_faithful_evidence_claimed": row.source_faithful_evidence_claimed,
    }


def _provenance_row_hash_payload(row: NoResultProvenanceHashMetadataRow) -> dict[str, object]:
    return {
        "external_pass_synthesis_bundle_hash": row.external_pass_synthesis_bundle_hash,
        "hash_chain": _provenance_observed_hashes(row),
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "no_result_hash_chain_policy_hash": row.no_result_hash_chain_policy_hash,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
    }


def _evidence_row_hash_payload(row: NoResultEvidenceManifestMetadataRow) -> dict[str, object]:
    return {
        "actual_cost_evidence_status": row.actual_cost_evidence_status,
        "actual_fill_evidence_status": row.actual_fill_evidence_status,
        "actual_pnl_evidence_status": row.actual_pnl_evidence_status,
        "evidence_manifest_policy_hash": row.no_result_evidence_policy_hash,
        "external_pass_synthesis_bundle_hash": row.external_pass_synthesis_bundle_hash,
        "ledger_label": row.ledger_label,
        "metadata_evidence_status": row.metadata_evidence_status,
        "no_pnl_bundle_hash": row.no_pnl_bundle_hash,
        "provenance_row_hash": row.provenance_row_hash,
        "reason_code": row.reason_code,
        "result_evidence_status": row.result_evidence_status,
        "row_status": row.row_status,
        "source_faithful_evidence_claimed": row.source_faithful_evidence_claimed,
        "source_faithful_evidence_status": row.source_faithful_evidence_status,
        "validation_row_hash": row.validation_row_hash,
    }


def _trusted_bundle_hash_payload(bundle: NoResultTrustedBundleMetadata) -> dict[str, object]:
    return {
        "actual_cost_rows_emitted": bundle.actual_cost_rows_emitted,
        "actual_fill_rows_emitted": bundle.actual_fill_rows_emitted,
        "actual_pnl_rows_emitted": bundle.actual_pnl_rows_emitted,
        "artifact": "S27_V2_NO_RESULT_TRUSTED_BUNDLE_METADATA",
        "authorization_label": bundle.authorization_label,
        "backtest_result_emitted": bundle.backtest_result_emitted,
        "evidence_manifest_metadata_rows_emitted": bundle.evidence_manifest_metadata_rows_emitted,
        "evidence_row_hash": bundle.evidence_row.row_hash,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "no_pnl_bundle_hash": bundle.no_pnl_bundle.bundle_hash,
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

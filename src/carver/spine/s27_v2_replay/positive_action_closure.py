from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .local_replay import canonical_sha256
from .positive_action_executable import EXPECTED_RAW_SYMBOL, EXPECTED_SELECTED_FILL, POSITIVE_ACTION_PACK_RELATIVE_PATH
from .positive_action_pnl_blocked_executable import (
    BACKTEST_RESULT_STATUS,
    RESULT_EMISSION_STATUS,
    PositiveActionPnlBlockedExecutableBundle,
    build_positive_action_pnl_blocked_metadata,
)
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_POSITIVE_ACTION_CLOSURE_AUTHORIZATION = "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_VALIDATION_PROVENANCE_TRUSTED_BUNDLE_CLOSURE"
S27_V2_POSITIVE_ACTION_CLOSURE_STATUS = "S27_V2_POSITIVE_ACTION_CLOSURE_METADATA_ONLY_NOT_RESULT"

POSITIVE_ACTION_VALIDATION_ROW_STATUS = "LOCAL_POSITIVE_ACTION_VALIDATION_METADATA_PNL_BLOCKED_CHAIN"
POSITIVE_ACTION_PROVENANCE_ROW_STATUS = "LOCAL_POSITIVE_ACTION_PROVENANCE_HASH_METADATA_PNL_BLOCKED_CHAIN"
POSITIVE_ACTION_EVIDENCE_ROW_STATUS = "LOCAL_POSITIVE_ACTION_EVIDENCE_MANIFEST_METADATA_PNL_BLOCKED_CHAIN"

POSITIVE_ACTION_VALIDATION_REASON_CODE = "S27_POSITIVE_ACTION_VALIDATION_BINDS_LOCAL_PASSED_CHAIN_NOT_RESULT"
POSITIVE_ACTION_PROVENANCE_REASON_CODE = "S27_POSITIVE_ACTION_PROVENANCE_BINDS_EXECUTABLE_HASH_CHAIN"
POSITIVE_ACTION_EVIDENCE_REASON_CODE = "S27_POSITIVE_ACTION_EVIDENCE_MANIFEST_DISTINGUISHES_METADATA_FROM_REPLAY_EVIDENCE"

DEFERRED_COST_PACKET_STATUS = "PREPARED_PACKET_DEFERRED_FOR_POST_BACKTEST_FINAL_AUDIT_ECONOMY"
DEFERRED_COST_PACKET_LIST_HASH = "7c7ec75349fd82a1bebb68b75d729b8396fe591a99dd4c61ff1cebfa27a6751a"
EXPECTED_DEFERRED_COST_PACKET_RECORD_SHA256 = "d498bd437d022dd231db4addfff72d37135de9dff07f40e2c0d8280692da64c7"
METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE = "METADATA_ONLY_NOT_SOURCE_FAITHFUL_REPLAY_EVIDENCE"
FAIL_CLOSED_RESULT_GATE_STATUS = "FAIL_CLOSED_NOT_EMITTED_NOT_AUTHORIZED"

POSITIVE_ACTION_PASSED_GATE_LABELS = (
    "POSITIVE_ACTION_EXECUTABLE",
    "POSITIVE_ACTION_ORDER_PLAN",
    "POSITIVE_ACTION_FILL",
    "POSITIVE_ACTION_COST_POLICY_EVIDENCE_LOCAL_ONLY",
    "POSITIVE_ACTION_PNL_BLOCKED_METADATA",
)

POSITIVE_ACTION_FAIL_CLOSED_GATE_LABELS = (
    "ACTUAL_COST_LEDGER",
    "ACTUAL_PNL_LEDGER",
    "RESULT_ROW",
    "BACKTEST_RESULT",
    "RESULT_INTERPRETATION",
    "PNL_EVALUATION",
    "SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)

POSITIVE_ACTION_CLOSURE_NON_AUTHORIZATIONS = (
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

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()
_DEFERRED_COST_PACKET_RECORD_PATH = (
    _REPO_ROOT / "docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_COST_EXTERNAL_AUDIT_HANDOFF_2026-06-09.md"
).resolve()


@dataclass(frozen=True)
class PositiveActionClosureValidationMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    pnl_blocked_bundle_hash: str
    input_pack_path: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    passed_gate_labels: tuple[str, ...]
    passed_gate_status: str
    fail_closed_gate_labels: tuple[str, ...]
    fail_closed_gate_status: str
    deferred_cost_packet_status: str
    deferred_cost_packet_list_hash: str
    deferred_cost_packet_record_sha256: str
    actual_cost_ledger_emitted: bool
    actual_pnl_ledger_emitted: bool
    result_rows_emitted: bool
    backtest_result_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    positive_action_validation_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 positive-action closure validation row standalone validation is not authoritative")

    def _validate_structural_formula(self, active_pnl_blocked: PositiveActionPnlBlockedExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_VALIDATION_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 positive-action closure validation ledger label is not locked")
        if self.row_status != POSITIVE_ACTION_VALIDATION_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action closure validation row status is not locked")
        if self.reason_code != POSITIVE_ACTION_VALIDATION_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action closure validation reason code is not locked")
        for name, hash_value in (
            ("PnL-blocked bundle", self.pnl_blocked_bundle_hash),
            ("deferred cost packet list", self.deferred_cost_packet_list_hash),
            ("deferred cost packet record", self.deferred_cost_packet_record_sha256),
            ("validation policy", self.positive_action_validation_policy_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action closure validation {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("passed gate status", self.passed_gate_status),
            ("fail-closed gate status", self.fail_closed_gate_status),
            ("deferred cost packet status", self.deferred_cost_packet_status),
        ):
            require_text(f"S27 v2 positive-action closure validation {name}", value)
        require_non_empty_tuple("S27 v2 positive-action closure passed gates", self.passed_gate_labels)
        require_non_empty_tuple("S27 v2 positive-action closure fail-closed gates", self.fail_closed_gate_labels)
        if self.passed_gate_labels != POSITIVE_ACTION_PASSED_GATE_LABELS:
            raise CarverBlocked("S27 v2 positive-action closure passed gates must match locked tuple")
        if self.passed_gate_status != "LOCAL_HOSTILE_AUDIT_PASS_METADATA_ONLY":
            raise CarverBlocked("S27 v2 positive-action closure passed gate status is not locked")
        if self.fail_closed_gate_labels != POSITIVE_ACTION_FAIL_CLOSED_GATE_LABELS:
            raise CarverBlocked("S27 v2 positive-action closure fail-closed gates must match locked tuple")
        if self.fail_closed_gate_status != FAIL_CLOSED_RESULT_GATE_STATUS:
            raise CarverBlocked("S27 v2 positive-action closure fail-closed status is not locked")
        if self.deferred_cost_packet_status != DEFERRED_COST_PACKET_STATUS:
            raise CarverBlocked("S27 v2 positive-action closure deferred cost packet status is not locked")
        if self.deferred_cost_packet_list_hash != DEFERRED_COST_PACKET_LIST_HASH:
            raise CarverBlocked("S27 v2 positive-action closure deferred cost packet list hash mismatch")
        if self.deferred_cost_packet_record_sha256 != _deferred_cost_packet_record_sha256():
            raise CarverBlocked("S27 v2 positive-action closure must bind deferred cost packet record bytes")
        _require_no_result_flags(
            self.actual_cost_ledger_emitted,
            self.actual_pnl_ledger_emitted,
            self.result_rows_emitted,
            self.backtest_result_emitted,
            self.result_interpretation_emitted,
            self.pnl_evaluation_emitted,
            self.source_faithful_evidence_claimed,
        )
        if self.pnl_blocked_bundle_hash != active_pnl_blocked.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action closure validation must bind active PnL-blocked bundle")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action closure validation is locked to the positive-action pack")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action closure validation fill timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 positive-action closure validation raw symbol is not locked")
        if self.positive_action_validation_policy_hash != _policy_hash(
            "positive_action_validation_policy",
            self.passed_gate_labels,
            self.passed_gate_status,
            self.fail_closed_gate_labels,
            self.fail_closed_gate_status,
            self.deferred_cost_packet_status,
            self.deferred_cost_packet_list_hash,
            self.deferred_cost_packet_record_sha256,
        ):
            raise CarverBlocked("S27 v2 positive-action closure validation policy hash must bind gate policy")
        if self.row_hash != canonical_sha256(_validation_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action closure validation row hash must be content-bound")


@dataclass(frozen=True)
class PositiveActionClosureProvenanceHashMetadataRow:
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
    cost_bundle_hash: str
    cost_evidence_row_hash: str
    pnl_blocked_bundle_hash: str
    pnl_blocked_row_hash: str
    deferred_cost_packet_record_sha256: str
    positive_action_hash_chain_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 positive-action closure provenance row standalone validation is not authoritative")

    def _validate_structural_formula(self, active_pnl_blocked: PositiveActionPnlBlockedExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_PROVENANCE_HASH_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 positive-action closure provenance ledger label is not locked")
        if self.row_status != POSITIVE_ACTION_PROVENANCE_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action closure provenance row status is not locked")
        if self.reason_code != POSITIVE_ACTION_PROVENANCE_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action closure provenance reason code is not locked")
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
        ):
            require_text(f"S27 v2 positive-action closure provenance {name}", value)
        for name, hash_value in _provenance_hash_items(self):
            require_hash(f"S27 v2 positive-action closure provenance {name}", hash_value)
        active_hashes = _active_chain_hashes(active_pnl_blocked)
        if _provenance_observed_hashes(self) != active_hashes:
            raise CarverBlocked("S27 v2 positive-action closure provenance must bind active positive-action hash chain")
        if self.deferred_cost_packet_record_sha256 != _deferred_cost_packet_record_sha256():
            raise CarverBlocked("S27 v2 positive-action closure provenance must bind deferred cost packet bytes")
        if self.positive_action_hash_chain_policy_hash != _policy_hash(
            "positive_action_provenance_hash_chain_policy",
            tuple(active_hashes.items()),
            self.deferred_cost_packet_record_sha256,
        ):
            raise CarverBlocked("S27 v2 positive-action closure provenance policy hash must bind hash chain")
        if self.row_hash != canonical_sha256(_provenance_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action closure provenance row hash must be content-bound")


@dataclass(frozen=True)
class PositiveActionClosureEvidenceManifestMetadataRow:
    ledger_label: str
    row_status: str
    reason_code: str
    pnl_blocked_bundle_hash: str
    validation_row_hash: str
    provenance_row_hash: str
    metadata_evidence_status: str
    actual_cost_evidence_status: str
    actual_pnl_evidence_status: str
    result_evidence_status: str
    backtest_evidence_status: str
    pnl_evaluation_status: str
    source_faithful_evidence_status: str
    source_faithful_evidence_claimed: bool
    deferred_cost_packet_status: str
    positive_action_evidence_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked("S27 v2 positive-action closure evidence row standalone validation is not authoritative")

    def _validate_structural_formula(
        self,
        active_pnl_blocked: PositiveActionPnlBlockedExecutableBundle,
        validation_row: PositiveActionClosureValidationMetadataRow,
        provenance_row: PositiveActionClosureProvenanceHashMetadataRow,
    ) -> None:
        if self.ledger_label != "POSITIVE_ACTION_EVIDENCE_MANIFEST_METADATA_LEDGER":
            raise CarverBlocked("S27 v2 positive-action closure evidence ledger label is not locked")
        if self.row_status != POSITIVE_ACTION_EVIDENCE_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action closure evidence row status is not locked")
        if self.reason_code != POSITIVE_ACTION_EVIDENCE_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action closure evidence reason code is not locked")
        for name, hash_value in (
            ("PnL-blocked bundle", self.pnl_blocked_bundle_hash),
            ("validation row", self.validation_row_hash),
            ("provenance row", self.provenance_row_hash),
            ("evidence policy", self.positive_action_evidence_policy_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action closure evidence {name} hash", hash_value)
        for name, value in (
            ("metadata evidence status", self.metadata_evidence_status),
            ("actual cost evidence status", self.actual_cost_evidence_status),
            ("actual PnL evidence status", self.actual_pnl_evidence_status),
            ("result evidence status", self.result_evidence_status),
            ("backtest evidence status", self.backtest_evidence_status),
            ("PnL evaluation status", self.pnl_evaluation_status),
            ("source-faithful evidence status", self.source_faithful_evidence_status),
            ("deferred cost packet status", self.deferred_cost_packet_status),
        ):
            require_text(f"S27 v2 positive-action closure evidence {name}", value)
        if self.pnl_blocked_bundle_hash != active_pnl_blocked.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action closure evidence must bind active PnL-blocked bundle")
        if self.validation_row_hash != validation_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action closure evidence must bind validation row")
        if self.provenance_row_hash != provenance_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action closure evidence must bind provenance row")
        if self.metadata_evidence_status != METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE:
            raise CarverBlocked("S27 v2 positive-action closure metadata status must remain non-source-faithful")
        for status in (
            self.actual_cost_evidence_status,
            self.actual_pnl_evidence_status,
            self.result_evidence_status,
            self.backtest_evidence_status,
            self.pnl_evaluation_status,
            self.source_faithful_evidence_status,
        ):
            if status != FAIL_CLOSED_RESULT_GATE_STATUS:
                raise CarverBlocked("S27 v2 positive-action closure evidence status must remain fail-closed")
        if self.source_faithful_evidence_claimed is not False:
            raise CarverBlocked("S27 v2 positive-action closure evidence cannot claim source-faithful evidence")
        if self.deferred_cost_packet_status != DEFERRED_COST_PACKET_STATUS:
            raise CarverBlocked("S27 v2 positive-action closure evidence must bind deferred cost packet status")
        if self.positive_action_evidence_policy_hash != _policy_hash(
            "positive_action_evidence_manifest_policy",
            self.metadata_evidence_status,
            self.actual_cost_evidence_status,
            self.actual_pnl_evidence_status,
            self.result_evidence_status,
            self.backtest_evidence_status,
            self.pnl_evaluation_status,
            self.source_faithful_evidence_status,
            self.deferred_cost_packet_status,
        ):
            raise CarverBlocked("S27 v2 positive-action closure evidence policy hash must bind evidence statuses")
        if self.row_hash != canonical_sha256(_evidence_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action closure evidence row hash must be content-bound")


@dataclass(frozen=True)
class PositiveActionClosureTrustedBundleMetadata:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    pnl_blocked_bundle: PositiveActionPnlBlockedExecutableBundle
    validation_row: PositiveActionClosureValidationMetadataRow
    provenance_row: PositiveActionClosureProvenanceHashMetadataRow
    evidence_row: PositiveActionClosureEvidenceManifestMetadataRow
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    evidence_manifest_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    actual_cost_rows_emitted: bool
    actual_pnl_rows_emitted: bool
    result_rows_emitted: bool
    backtest_result_emitted: bool
    result_interpretation_emitted: bool
    pnl_evaluation_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = POSITIVE_ACTION_CLOSURE_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_CLOSURE_STATUS:
            raise CarverBlocked("S27 v2 positive-action closure status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_CLOSURE_AUTHORIZATION:
            raise CarverBlocked("S27 v2 positive-action closure authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 positive-action closure must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 positive-action closure must remain source-native futures")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action closure is locked to the positive-action pack")
        active_pnl_blocked = build_positive_action_pnl_blocked_metadata(_POSITIVE_ACTION_PACK_PATH)
        if self.pnl_blocked_bundle != active_pnl_blocked:
            raise CarverBlocked("S27 v2 positive-action closure must bind active PnL-blocked bundle")
        active_validation = _build_active_validation_row(_POSITIVE_ACTION_PACK_PATH, active_pnl_blocked)
        self.validation_row._validate_structural_formula(active_pnl_blocked)
        if self.validation_row != active_validation:
            raise CarverBlocked("S27 v2 positive-action closure validation row must match active authority")
        active_provenance = _build_active_provenance_row(_POSITIVE_ACTION_PACK_PATH, active_pnl_blocked)
        self.provenance_row._validate_structural_formula(active_pnl_blocked)
        if self.provenance_row != active_provenance:
            raise CarverBlocked("S27 v2 positive-action closure provenance row must match active hash chain")
        active_evidence = _build_active_evidence_row(active_pnl_blocked, active_validation, active_provenance)
        self.evidence_row._validate_structural_formula(active_pnl_blocked, active_validation, active_provenance)
        if self.evidence_row != active_evidence:
            raise CarverBlocked("S27 v2 positive-action closure evidence row must match active metadata")
        if any(
            flag is not True
            for flag in (
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.evidence_manifest_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action closure must emit all closure metadata rows")
        _require_no_result_flags(
            self.actual_cost_rows_emitted,
            self.actual_pnl_rows_emitted,
            self.result_rows_emitted,
            self.backtest_result_emitted,
            self.result_interpretation_emitted,
            self.pnl_evaluation_emitted,
            self.source_faithful_evidence_claimed,
        )
        if self.non_authorizations != POSITIVE_ACTION_CLOSURE_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 positive-action closure must preserve non-authorizations")
        require_hash("S27 v2 positive-action closure bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_trusted_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action closure bundle hash must be content-bound")


def build_positive_action_closure_metadata(
    input_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
) -> PositiveActionClosureTrustedBundleMetadata:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action closure is locked to the positive-action pack")
    pnl_blocked_bundle = build_positive_action_pnl_blocked_metadata(pack_path)
    validation_row = _build_active_validation_row(pack_path, pnl_blocked_bundle)
    provenance_row = _build_active_provenance_row(pack_path, pnl_blocked_bundle)
    evidence_row = _build_active_evidence_row(pnl_blocked_bundle, validation_row, provenance_row)
    bundle = PositiveActionClosureTrustedBundleMetadata(
        status=S27_V2_POSITIVE_ACTION_CLOSURE_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_CLOSURE_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        pnl_blocked_bundle=pnl_blocked_bundle,
        validation_row=validation_row,
        provenance_row=provenance_row,
        evidence_row=evidence_row,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        evidence_manifest_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        actual_cost_rows_emitted=False,
        actual_pnl_rows_emitted=False,
        result_rows_emitted=False,
        backtest_result_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionClosureTrustedBundleMetadata(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_trusted_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_validation_row(
    pack_path: Path,
    pnl_blocked_bundle: PositiveActionPnlBlockedExecutableBundle,
) -> PositiveActionClosureValidationMetadataRow:
    row = PositiveActionClosureValidationMetadataRow(
        ledger_label="POSITIVE_ACTION_VALIDATION_METADATA_LEDGER",
        row_status=POSITIVE_ACTION_VALIDATION_ROW_STATUS,
        reason_code=POSITIVE_ACTION_VALIDATION_REASON_CODE,
        pnl_blocked_bundle_hash=pnl_blocked_bundle.bundle_hash,
        input_pack_path=str(pack_path),
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        passed_gate_labels=POSITIVE_ACTION_PASSED_GATE_LABELS,
        passed_gate_status="LOCAL_HOSTILE_AUDIT_PASS_METADATA_ONLY",
        fail_closed_gate_labels=POSITIVE_ACTION_FAIL_CLOSED_GATE_LABELS,
        fail_closed_gate_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        deferred_cost_packet_status=DEFERRED_COST_PACKET_STATUS,
        deferred_cost_packet_list_hash=DEFERRED_COST_PACKET_LIST_HASH,
        deferred_cost_packet_record_sha256=_deferred_cost_packet_record_sha256(),
        actual_cost_ledger_emitted=False,
        actual_pnl_ledger_emitted=False,
        result_rows_emitted=False,
        backtest_result_emitted=False,
        result_interpretation_emitted=False,
        pnl_evaluation_emitted=False,
        source_faithful_evidence_claimed=False,
        positive_action_validation_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = PositiveActionClosureValidationMetadataRow(
        **{**row.__dict__, "positive_action_validation_policy_hash": _policy_hash(
            "positive_action_validation_policy",
            row.passed_gate_labels,
            row.passed_gate_status,
            row.fail_closed_gate_labels,
            row.fail_closed_gate_status,
            row.deferred_cost_packet_status,
            row.deferred_cost_packet_list_hash,
            row.deferred_cost_packet_record_sha256,
        )}
    )
    row = PositiveActionClosureValidationMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_validation_row_hash_payload(row))}
    )
    row._validate_structural_formula(pnl_blocked_bundle)
    return row


def _build_active_provenance_row(
    pack_path: Path,
    pnl_blocked_bundle: PositiveActionPnlBlockedExecutableBundle,
) -> PositiveActionClosureProvenanceHashMetadataRow:
    hashes = _active_chain_hashes(pnl_blocked_bundle)
    row = PositiveActionClosureProvenanceHashMetadataRow(
        ledger_label="POSITIVE_ACTION_PROVENANCE_HASH_METADATA_LEDGER",
        row_status=POSITIVE_ACTION_PROVENANCE_ROW_STATUS,
        reason_code=POSITIVE_ACTION_PROVENANCE_REASON_CODE,
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
        cost_bundle_hash=hashes["cost_bundle_hash"],
        cost_evidence_row_hash=hashes["cost_evidence_row_hash"],
        pnl_blocked_bundle_hash=hashes["pnl_blocked_bundle_hash"],
        pnl_blocked_row_hash=hashes["pnl_blocked_row_hash"],
        deferred_cost_packet_record_sha256=_deferred_cost_packet_record_sha256(),
        positive_action_hash_chain_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = PositiveActionClosureProvenanceHashMetadataRow(
        **{**row.__dict__, "positive_action_hash_chain_policy_hash": _policy_hash(
            "positive_action_provenance_hash_chain_policy",
            tuple(hashes.items()),
            row.deferred_cost_packet_record_sha256,
        )}
    )
    row = PositiveActionClosureProvenanceHashMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_provenance_row_hash_payload(row))}
    )
    row._validate_structural_formula(pnl_blocked_bundle)
    return row


def _build_active_evidence_row(
    pnl_blocked_bundle: PositiveActionPnlBlockedExecutableBundle,
    validation_row: PositiveActionClosureValidationMetadataRow,
    provenance_row: PositiveActionClosureProvenanceHashMetadataRow,
) -> PositiveActionClosureEvidenceManifestMetadataRow:
    row = PositiveActionClosureEvidenceManifestMetadataRow(
        ledger_label="POSITIVE_ACTION_EVIDENCE_MANIFEST_METADATA_LEDGER",
        row_status=POSITIVE_ACTION_EVIDENCE_ROW_STATUS,
        reason_code=POSITIVE_ACTION_EVIDENCE_REASON_CODE,
        pnl_blocked_bundle_hash=pnl_blocked_bundle.bundle_hash,
        validation_row_hash=validation_row.row_hash,
        provenance_row_hash=provenance_row.row_hash,
        metadata_evidence_status=METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE,
        actual_cost_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        actual_pnl_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        result_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        backtest_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        pnl_evaluation_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        source_faithful_evidence_status=FAIL_CLOSED_RESULT_GATE_STATUS,
        source_faithful_evidence_claimed=False,
        deferred_cost_packet_status=DEFERRED_COST_PACKET_STATUS,
        positive_action_evidence_policy_hash="0" * 64,
        row_hash="0" * 64,
    )
    row = PositiveActionClosureEvidenceManifestMetadataRow(
        **{**row.__dict__, "positive_action_evidence_policy_hash": _policy_hash(
            "positive_action_evidence_manifest_policy",
            row.metadata_evidence_status,
            row.actual_cost_evidence_status,
            row.actual_pnl_evidence_status,
            row.result_evidence_status,
            row.backtest_evidence_status,
            row.pnl_evaluation_status,
            row.source_faithful_evidence_status,
            row.deferred_cost_packet_status,
        )}
    )
    row = PositiveActionClosureEvidenceManifestMetadataRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_evidence_row_hash_payload(row))}
    )
    row._validate_structural_formula(pnl_blocked_bundle, validation_row, provenance_row)
    return row


def _active_chain_hashes(pnl_blocked_bundle: PositiveActionPnlBlockedExecutableBundle) -> dict[str, str]:
    cost_bundle = pnl_blocked_bundle.cost_bundle
    fill_bundle = cost_bundle.fill_bundle
    order_plan_bundle = fill_bundle.order_plan_bundle
    positive_action_bundle = order_plan_bundle.positive_action_bundle
    positive_row = positive_action_bundle.positive_action_row
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
        "cost_bundle_hash": cost_bundle.bundle_hash,
        "cost_evidence_row_hash": cost_bundle.cost_evidence_row.row_hash,
        "pnl_blocked_bundle_hash": pnl_blocked_bundle.bundle_hash,
        "pnl_blocked_row_hash": pnl_blocked_bundle.pnl_blocked_row.row_hash,
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


def _deferred_cost_packet_record_sha256() -> str:
    if not _DEFERRED_COST_PACKET_RECORD_PATH.is_file():
        raise CarverBlocked("S27 v2 positive-action closure deferred cost packet record is missing")
    text = _DEFERRED_COST_PACKET_RECORD_PATH.read_text(encoding="utf-8")
    if DEFERRED_COST_PACKET_STATUS not in text or DEFERRED_COST_PACKET_LIST_HASH not in text:
        raise CarverBlocked("S27 v2 positive-action closure deferred cost packet record content is not locked")
    observed = sha256(_DEFERRED_COST_PACKET_RECORD_PATH.read_bytes()).hexdigest()
    if observed != EXPECTED_DEFERRED_COST_PACKET_RECORD_SHA256:
        raise CarverBlocked("S27 v2 positive-action closure deferred cost packet record hash is not pinned")
    return observed


def _provenance_hash_items(row: PositiveActionClosureProvenanceHashMetadataRow) -> tuple[tuple[str, str], ...]:
    observed = _provenance_observed_hashes(row)
    return tuple(observed.items()) + (
        ("deferred cost packet record", row.deferred_cost_packet_record_sha256),
        ("positive-action hash-chain policy", row.positive_action_hash_chain_policy_hash),
        ("row", row.row_hash),
    )


def _provenance_observed_hashes(row: PositiveActionClosureProvenanceHashMetadataRow) -> dict[str, str]:
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
        "cost_bundle_hash": row.cost_bundle_hash,
        "cost_evidence_row_hash": row.cost_evidence_row_hash,
        "pnl_blocked_bundle_hash": row.pnl_blocked_bundle_hash,
        "pnl_blocked_row_hash": row.pnl_blocked_row_hash,
    }


def _require_no_result_flags(*flags: bool) -> None:
    if any(flag is not False for flag in flags):
        raise CarverBlocked("S27 v2 positive-action closure cannot emit cost/PnL/result/backtest/evidence")


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_CLOSURE_POLICY", "label": label, "values": values})


def _validation_row_hash_payload(row: PositiveActionClosureValidationMetadataRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _provenance_row_hash_payload(row: PositiveActionClosureProvenanceHashMetadataRow) -> dict[str, object]:
    return {
        "deferred_cost_packet_record_sha256": row.deferred_cost_packet_record_sha256,
        "hash_chain": _provenance_observed_hashes(row),
        "input_pack_path": row.input_pack_path,
        "ledger_label": row.ledger_label,
        "positive_action_hash_chain_policy_hash": row.positive_action_hash_chain_policy_hash,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "selected_fill_timestamp_utc": row.selected_fill_timestamp_utc,
    }


def _evidence_row_hash_payload(row: PositiveActionClosureEvidenceManifestMetadataRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _trusted_bundle_hash_payload(bundle: PositiveActionClosureTrustedBundleMetadata) -> dict[str, object]:
    return {
        "actual_cost_rows_emitted": bundle.actual_cost_rows_emitted,
        "actual_pnl_rows_emitted": bundle.actual_pnl_rows_emitted,
        "artifact": "S27_V2_POSITIVE_ACTION_CLOSURE_TRUSTED_BUNDLE_METADATA",
        "authorization_label": bundle.authorization_label,
        "backtest_result_emitted": bundle.backtest_result_emitted,
        "evidence_manifest_metadata_rows_emitted": bundle.evidence_manifest_metadata_rows_emitted,
        "evidence_row_hash": bundle.evidence_row.row_hash,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "pnl_blocked_bundle_hash": bundle.pnl_blocked_bundle.bundle_hash,
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

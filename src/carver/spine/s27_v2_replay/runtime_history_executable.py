from __future__ import annotations

import csv
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import (
    BLOCKED_COST_SCHEMA,
    BLOCKED_TICK,
    BLOCKED_WORKING_LIMIT_LIFECYCLE,
    REQUIRED_UNRESOLVED_GATE_LABELS,
    S27_V2_INSTRUMENT,
    S27_V2_LANE,
    S27_V2_STRATEGY_ID,
)
from .local_replay import canonical_sha256
from .runtime_evidence_gate import (
    FAIL_CLOSED,
    PASS_COUNT_ONLY,
    PASS_LOCAL_BRIDGE_PROOF,
    PASS_LOCAL_DECLARED_ONLY,
    PASS_LOCAL_PREVALIDATED,
    REQUIRED_ROW_FAMILY_FILES,
    REMEDIATION_REQUIRED_GATE_BY_LABEL,
    REMEDIATION_REQUIRED_STATUS_BY_LABEL,
    RUNTIME_EVIDENCE_NON_AUTHORIZATIONS,
    RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH,
    RuntimeEvidenceGateBundle,
    build_runtime_evidence_gate,
)
from .validation import require_hash, require_non_empty_tuple, require_text, require_tuple


S27_V2_RUNTIME_HISTORY_EXECUTABLE_AUTHORIZATION = (
    "S27_V2_LOCAL_ONLY_RUNTIME_HISTORY_EXECUTABLE_LEDGER_ON_REMEDIATION_PACK"
)
S27_V2_RUNTIME_HISTORY_EXECUTABLE_STATUS = (
    "S27_V2_RUNTIME_HISTORY_EXECUTABLE_REMEDIATION_NON_RESULT_NOT_EVIDENCE"
)
RUNTIME_HISTORY_LEVEL_BRIDGE_PASS_STATUS = "LOCAL_LEVEL_SPACE_BRIDGE_PROVED_NON_RESULT"
RUNTIME_HISTORY_READY_STATUS = "LOCAL_RUNTIME_HISTORY_INPUTS_SUFFICIENT_VALUES_NOT_EMITTED"
RUNTIME_HISTORY_MINIMUM_DAILY_ROWS = 64
RUNTIME_HISTORY_EXECUTABLE_NON_AUTHORIZATIONS = RUNTIME_EVIDENCE_NON_AUTHORIZATIONS

_REPO_ROOT = Path(__file__).resolve().parents[4]
_REMEDIATION_PACK_PATH = (_REPO_ROOT / RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH).resolve()
_REQUIRED_REMEDIATION_PASS_CHECKS = (
    "STRICT_PRIOR_DAILY_ADMISSIBILITY",
    "HOURLY_DECISION_FILL_ADMISSIBILITY",
    "EWMA5_EVIDENCE",
    "EWMAC_16_64_EVIDENCE",
    "STRATEGY3_SIGMA_EVIDENCE",
    "VQM_EVIDENCE",
    "DAILY_HOURLY_LEVEL_BRIDGE",
    "SESSION_ROLL_COVERAGE",
)
_REQUIRED_REMEDIATION_FAIL_CHECKS = (
    "TICK_ROUNDING_POLICY",
    "MULTIPLIER_CURRENCY_POLICY",
    "COMMISSION_SPREAD_POLICY",
    "WORKING_ORDER_LIFECYCLE",
)


@dataclass(frozen=True)
class RuntimeHistoryRemediationLevelLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    runtime_evidence_bundle_hash: str
    manifest_hash: str
    level_bridge_proof_hash: str
    selected_decision_timestamp_utc: str
    selected_fill_timestamp_utc: str
    selected_previous_daily_timestamp_utc: str
    daily_continuous_row_hash: str
    daily_current_contract_row_hash: str
    hourly_decision_row_hash: str
    hourly_fill_row_hash: str
    daily_continuous_close_price: str
    daily_current_contract_close_price: str
    hourly_decision_close_price: str
    hourly_fill_close_price: str
    row_hash: str

    def validate(self) -> None:
        if self.ledger_label != "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER":
            raise CarverBlocked("S27 v2 runtime-history remediation level ledger label is not locked")
        if self.row_status != RUNTIME_HISTORY_LEVEL_BRIDGE_PASS_STATUS:
            raise CarverBlocked("S27 v2 runtime-history remediation level row must bind local bridge pass")
        if self.reason_code != "LOCAL_LEVEL_SPACE_BRIDGE_PROOF_BOUND_NOT_PRICE_EQUALITY":
            raise CarverBlocked("S27 v2 runtime-history remediation level reason is not locked")
        for name, hash_value in (
            ("runtime evidence bundle hash", self.runtime_evidence_bundle_hash),
            ("manifest hash", self.manifest_hash),
            ("level bridge proof hash", self.level_bridge_proof_hash),
            ("daily continuous row hash", self.daily_continuous_row_hash),
            ("daily current-contract row hash", self.daily_current_contract_row_hash),
            ("hourly decision row hash", self.hourly_decision_row_hash),
            ("hourly fill row hash", self.hourly_fill_row_hash),
        ):
            require_hash(f"S27 v2 runtime-history remediation level {name}", hash_value)
        for name, value in (
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("selected fill timestamp", self.selected_fill_timestamp_utc),
            ("selected previous daily timestamp", self.selected_previous_daily_timestamp_utc),
            ("daily continuous close", self.daily_continuous_close_price),
            ("daily current-contract close", self.daily_current_contract_close_price),
            ("hourly decision close", self.hourly_decision_close_price),
            ("hourly fill close", self.hourly_fill_close_price),
        ):
            require_text(f"S27 v2 runtime-history remediation level {name}", value)
        require_hash("S27 v2 runtime-history remediation level row hash", self.row_hash)
        if self.row_hash != canonical_sha256(_level_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 runtime-history remediation level row hash must be content-bound")


@dataclass(frozen=True)
class RuntimeHistoryRemediationRuntimeLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    runtime_evidence_bundle_hash: str
    level_compatibility_row_hash: str
    observed_daily_continuous_rows: int
    required_minimum_daily_continuous_rows: int
    daily_continuous_row_hashes: tuple[str, ...]
    hourly_decision_row_hashes: tuple[str, ...]
    strict_prior_daily_check_hash: str
    hourly_admissibility_check_hash: str
    ewma5_check_hash: str
    ewmac_16_64_check_hash: str
    strategy3_sigma_check_hash: str
    vqm_check_hash: str
    session_roll_check_hash: str
    runtime_numeric_values_emitted: bool
    row_hash: str

    def validate(self) -> None:
        if self.ledger_label != "RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM":
            raise CarverBlocked("S27 v2 runtime-history remediation runtime ledger label is not locked")
        if self.row_status != RUNTIME_HISTORY_READY_STATUS:
            raise CarverBlocked("S27 v2 runtime-history remediation runtime row must bind sufficient local inputs")
        if self.reason_code != (
            "STRICT_PRIOR_RUNTIME_HISTORY_AND_LOCAL_PREVALIDATED_SIGMA_EWMAC_VQM_BOUND_VALUES_NOT_EMITTED"
        ):
            raise CarverBlocked("S27 v2 runtime-history remediation runtime reason is not locked")
        require_hash("S27 v2 runtime-history remediation runtime evidence bundle hash", self.runtime_evidence_bundle_hash)
        require_hash("S27 v2 runtime-history remediation level row hash", self.level_compatibility_row_hash)
        if (
            not isinstance(self.observed_daily_continuous_rows, int)
            or isinstance(self.observed_daily_continuous_rows, bool)
        ):
            raise CarverBlocked("S27 v2 runtime-history remediation observed daily row count must be integer")
        if self.required_minimum_daily_continuous_rows != RUNTIME_HISTORY_MINIMUM_DAILY_ROWS:
            raise CarverBlocked("S27 v2 runtime-history remediation minimum daily history is locked")
        require_non_empty_tuple("S27 v2 runtime-history remediation daily row hashes", self.daily_continuous_row_hashes)
        require_non_empty_tuple("S27 v2 runtime-history remediation hourly row hashes", self.hourly_decision_row_hashes)
        if self.observed_daily_continuous_rows != len(self.daily_continuous_row_hashes):
            raise CarverBlocked("S27 v2 runtime-history remediation daily row count must bind row hashes")
        if self.observed_daily_continuous_rows < self.required_minimum_daily_continuous_rows:
            raise CarverBlocked("S27 v2 runtime-history remediation row must bind sufficient daily history")
        for row_hash in (*self.daily_continuous_row_hashes, *self.hourly_decision_row_hashes):
            require_hash("S27 v2 runtime-history remediation source row hash", row_hash)
        for name, hash_value in (
            ("strict-prior daily check", self.strict_prior_daily_check_hash),
            ("hourly admissibility check", self.hourly_admissibility_check_hash),
            ("EWMA5 check", self.ewma5_check_hash),
            ("EWMAC16/64 check", self.ewmac_16_64_check_hash),
            ("Strategy 3 sigma check", self.strategy3_sigma_check_hash),
            ("V/Q/M check", self.vqm_check_hash),
            ("session/roll check", self.session_roll_check_hash),
        ):
            require_hash(f"S27 v2 runtime-history remediation runtime {name}", hash_value)
        if self.runtime_numeric_values_emitted is not False:
            raise CarverBlocked("S27 v2 runtime-history remediation cannot emit runtime numeric values")
        require_hash("S27 v2 runtime-history remediation runtime row hash", self.row_hash)
        if self.row_hash != canonical_sha256(_runtime_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 runtime-history remediation runtime row hash must be content-bound")


@dataclass(frozen=True)
class RuntimeHistoryRemediationExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    runtime_evidence_bundle: RuntimeEvidenceGateBundle
    level_compatibility_row: RuntimeHistoryRemediationLevelLedgerRow
    runtime_history_row: RuntimeHistoryRemediationRuntimeLedgerRow
    unresolved_gate_labels: tuple[str, ...]
    forecast_rows_emitted: bool
    order_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = RUNTIME_HISTORY_EXECUTABLE_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_RUNTIME_HISTORY_EXECUTABLE_STATUS:
            raise CarverBlocked("S27 v2 runtime-history remediation executable status is not locked")
        if self.authorization_label != S27_V2_RUNTIME_HISTORY_EXECUTABLE_AUTHORIZATION:
            raise CarverBlocked("S27 v2 runtime-history remediation authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 runtime-history remediation must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 runtime-history remediation must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 runtime-history remediation is locked to the audited remediation pack")
        self.runtime_evidence_bundle.validate()
        active_evidence = build_runtime_evidence_gate(pack_path)
        if self.runtime_evidence_bundle != active_evidence:
            raise CarverBlocked("S27 v2 runtime-history remediation must bind active runtime evidence bundle")
        self.level_compatibility_row.validate()
        self.runtime_history_row.validate()
        active_manifest = _read_manifest(pack_path)
        active_rows_by_file = _read_rows_by_file(pack_path)
        active_row_hashes_by_file = _row_hashes_by_file(active_rows_by_file)
        active_level_row = _build_active_level_row(
            active_evidence,
            active_manifest,
            active_rows_by_file,
            active_row_hashes_by_file,
        )
        active_runtime_row = _build_active_runtime_row(
            active_evidence,
            active_row_hashes_by_file,
            active_level_row,
        )
        active_history_evidence = active_manifest["history_evidence"]
        if self.level_compatibility_row.level_bridge_proof_hash != active_history_evidence["level_bridge_proof_hash"]:
            raise CarverBlocked("S27 v2 runtime-history remediation level row must bind active bridge proof")
        if self.level_compatibility_row != active_level_row:
            raise CarverBlocked("S27 v2 runtime-history remediation level row must match active pack rows")
        if self.runtime_history_row != active_runtime_row:
            raise CarverBlocked("S27 v2 runtime-history remediation runtime row must match active evidence and pack rows")
        if self.level_compatibility_row.runtime_evidence_bundle_hash != self.runtime_evidence_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 runtime-history remediation level row must bind active evidence")
        if self.runtime_history_row.runtime_evidence_bundle_hash != self.runtime_evidence_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 runtime-history remediation runtime row must bind active evidence")
        if self.runtime_history_row.level_compatibility_row_hash != self.level_compatibility_row.row_hash:
            raise CarverBlocked("S27 v2 runtime-history remediation runtime row must bind active level row")
        expected_unresolved = (BLOCKED_TICK, BLOCKED_COST_SCHEMA, BLOCKED_WORKING_LIMIT_LIFECYCLE)
        require_tuple("S27 v2 runtime-history remediation unresolved gates", self.unresolved_gate_labels)
        if self.unresolved_gate_labels != expected_unresolved:
            raise CarverBlocked("S27 v2 runtime-history remediation unresolved gates must preserve blocked policies")
        for gate_label in self.unresolved_gate_labels:
            if gate_label not in REQUIRED_UNRESOLVED_GATE_LABELS:
                raise CarverBlocked("S27 v2 runtime-history remediation unresolved gate is not source-locked")
        if any(
            flag is not False
            for flag in (
                self.forecast_rows_emitted,
                self.order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 runtime-history remediation cannot emit downstream result surfaces")
        if self.non_authorizations != RUNTIME_HISTORY_EXECUTABLE_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 runtime-history remediation must preserve non-authorizations")
        require_hash("S27 v2 runtime-history remediation bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 runtime-history remediation bundle hash must be content-bound")


def build_runtime_history_executable_ledgers_on_remediation_pack(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> RuntimeHistoryRemediationExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 runtime-history executable run is locked to the audited remediation pack")
    evidence = build_runtime_evidence_gate(pack_path)
    _validate_remediation_evidence_for_runtime_history(evidence)
    manifest = _read_manifest(pack_path)
    rows_by_file = _read_rows_by_file(pack_path)
    row_hashes_by_file = _row_hashes_by_file(rows_by_file)

    level_row = _build_active_level_row(evidence, manifest, rows_by_file, row_hashes_by_file)
    runtime_row = _build_active_runtime_row(evidence, row_hashes_by_file, level_row)
    bundle = RuntimeHistoryRemediationExecutableBundle(
        status=S27_V2_RUNTIME_HISTORY_EXECUTABLE_STATUS,
        authorization_label=S27_V2_RUNTIME_HISTORY_EXECUTABLE_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        runtime_evidence_bundle=evidence,
        level_compatibility_row=level_row,
        runtime_history_row=runtime_row,
        unresolved_gate_labels=(BLOCKED_TICK, BLOCKED_COST_SCHEMA, BLOCKED_WORKING_LIMIT_LIFECYCLE),
        forecast_rows_emitted=False,
        order_rows_emitted=False,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = RuntimeHistoryRemediationExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_level_row(
    evidence: RuntimeEvidenceGateBundle,
    manifest: dict[str, Any],
    rows_by_file: dict[str, tuple[dict[str, str], ...]],
    row_hashes_by_file: dict[str, tuple[str, ...]],
) -> RuntimeHistoryRemediationLevelLedgerRow:
    history_evidence = manifest["history_evidence"]
    row = RuntimeHistoryRemediationLevelLedgerRow(
        ledger_label="DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER",
        row_status=RUNTIME_HISTORY_LEVEL_BRIDGE_PASS_STATUS,
        reason_code="LOCAL_LEVEL_SPACE_BRIDGE_PROOF_BOUND_NOT_PRICE_EQUALITY",
        runtime_evidence_bundle_hash=evidence.bundle_hash,
        manifest_hash=evidence.manifest_hash,
        level_bridge_proof_hash=history_evidence["level_bridge_proof_hash"],
        selected_decision_timestamp_utc=evidence.selected_decision_timestamp_utc,
        selected_fill_timestamp_utc=evidence.selected_fill_timestamp_utc,
        selected_previous_daily_timestamp_utc=evidence.selected_previous_daily_timestamp_utc,
        daily_continuous_row_hash=row_hashes_by_file["daily_continuous_completed_bar.csv"][0],
        daily_current_contract_row_hash=row_hashes_by_file["daily_current_contract_completed_bar.csv"][0],
        hourly_decision_row_hash=row_hashes_by_file["hourly_decision_completed_bar.csv"][0],
        hourly_fill_row_hash=row_hashes_by_file["hourly_fill_completed_bar.csv"][0],
        daily_continuous_close_price=rows_by_file["daily_continuous_completed_bar.csv"][0]["close_price"],
        daily_current_contract_close_price=rows_by_file["daily_current_contract_completed_bar.csv"][0]["close_price"],
        hourly_decision_close_price=rows_by_file["hourly_decision_completed_bar.csv"][0]["close_price"],
        hourly_fill_close_price=rows_by_file["hourly_fill_completed_bar.csv"][0]["close_price"],
        row_hash="0" * 64,
    )
    row = RuntimeHistoryRemediationLevelLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_level_row_hash_payload(row))}
    )
    row.validate()
    return row


def _build_active_runtime_row(
    evidence: RuntimeEvidenceGateBundle,
    row_hashes_by_file: dict[str, tuple[str, ...]],
    level_row: RuntimeHistoryRemediationLevelLedgerRow,
) -> RuntimeHistoryRemediationRuntimeLedgerRow:
    checks = _checks_by_label(evidence)
    row = RuntimeHistoryRemediationRuntimeLedgerRow(
        ledger_label="RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM",
        row_status=RUNTIME_HISTORY_READY_STATUS,
        reason_code="STRICT_PRIOR_RUNTIME_HISTORY_AND_LOCAL_PREVALIDATED_SIGMA_EWMAC_VQM_BOUND_VALUES_NOT_EMITTED",
        runtime_evidence_bundle_hash=evidence.bundle_hash,
        level_compatibility_row_hash=level_row.row_hash,
        observed_daily_continuous_rows=len(row_hashes_by_file["daily_continuous_completed_bar.csv"]),
        required_minimum_daily_continuous_rows=RUNTIME_HISTORY_MINIMUM_DAILY_ROWS,
        daily_continuous_row_hashes=row_hashes_by_file["daily_continuous_completed_bar.csv"],
        hourly_decision_row_hashes=row_hashes_by_file["hourly_decision_completed_bar.csv"],
        strict_prior_daily_check_hash=checks["STRICT_PRIOR_DAILY_ADMISSIBILITY"].observed_value_hash,
        hourly_admissibility_check_hash=checks["HOURLY_DECISION_FILL_ADMISSIBILITY"].observed_value_hash,
        ewma5_check_hash=checks["EWMA5_EVIDENCE"].observed_value_hash,
        ewmac_16_64_check_hash=checks["EWMAC_16_64_EVIDENCE"].observed_value_hash,
        strategy3_sigma_check_hash=checks["STRATEGY3_SIGMA_EVIDENCE"].observed_value_hash,
        vqm_check_hash=checks["VQM_EVIDENCE"].observed_value_hash,
        session_roll_check_hash=checks["SESSION_ROLL_COVERAGE"].observed_value_hash,
        runtime_numeric_values_emitted=False,
        row_hash="0" * 64,
    )
    row = RuntimeHistoryRemediationRuntimeLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_runtime_row_hash_payload(row))}
    )
    row.validate()
    return row


def _validate_remediation_evidence_for_runtime_history(bundle: RuntimeEvidenceGateBundle) -> None:
    checks = _checks_by_label(bundle)
    for label in _REQUIRED_REMEDIATION_PASS_CHECKS:
        if checks[label].status != REMEDIATION_REQUIRED_STATUS_BY_LABEL[label]:
            raise CarverBlocked("S27 v2 runtime-history remediation pass check status is not active")
        if checks[label].gate_label != REMEDIATION_REQUIRED_GATE_BY_LABEL[label]:
            raise CarverBlocked("S27 v2 runtime-history remediation pass check gate is not active")
        if checks[label].status not in (
            PASS_LOCAL_DECLARED_ONLY,
            PASS_COUNT_ONLY,
            PASS_LOCAL_PREVALIDATED,
            PASS_LOCAL_BRIDGE_PROOF,
        ):
            raise CarverBlocked("S27 v2 runtime-history remediation pass check is not sufficient")
    for label in _REQUIRED_REMEDIATION_FAIL_CHECKS:
        if checks[label].status != FAIL_CLOSED:
            raise CarverBlocked("S27 v2 runtime-history remediation policy check must remain fail-closed")
        if checks[label].gate_label != REMEDIATION_REQUIRED_GATE_BY_LABEL[label]:
            raise CarverBlocked("S27 v2 runtime-history remediation fail check gate is not active")
    if bundle.fail_closed_gate_labels != (BLOCKED_TICK, BLOCKED_COST_SCHEMA, BLOCKED_WORKING_LIMIT_LIFECYCLE):
        raise CarverBlocked("S27 v2 runtime-history remediation fail gates must be policy-only")


def _read_manifest(pack_path: Path) -> dict[str, Any]:
    manifest_path = pack_path / "S27_V2_RUNTIME_EVIDENCE_REMEDIATION_DECLARED_INPUT_PACK_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise CarverBlocked("S27 v2 runtime-history remediation manifest must be a JSON object")
    history_evidence = manifest.get("history_evidence")
    if not isinstance(history_evidence, dict):
        raise CarverBlocked("S27 v2 runtime-history remediation history evidence is unresolved")
    return manifest


def _read_rows_by_file(pack_path: Path) -> dict[str, tuple[dict[str, str], ...]]:
    rows_by_file: dict[str, tuple[dict[str, str], ...]] = {}
    for filename in REQUIRED_ROW_FAMILY_FILES:
        with (pack_path / filename).open("r", encoding="utf-8", newline="") as handle:
            rows = tuple(csv.DictReader(handle))
        if not rows:
            raise CarverBlocked("S27 v2 runtime-history remediation declared row family is empty")
        rows_by_file[filename] = rows
    return rows_by_file


def _row_hashes_by_file(rows_by_file: dict[str, tuple[dict[str, str], ...]]) -> dict[str, tuple[str, ...]]:
    row_family_by_file = {
        "daily_continuous_completed_bar.csv": "DAILY_CONTINUOUS_COMPLETED_BAR",
        "daily_current_contract_completed_bar.csv": "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
        "hourly_decision_completed_bar.csv": "HOURLY_DECISION_COMPLETED_BAR",
        "hourly_fill_completed_bar.csv": "HOURLY_FILL_COMPLETED_BAR",
        "session_calendar.csv": "SESSION_CALENDAR",
        "roll_calendar.csv": "ROLL_CALENDAR",
        "cost_parameter.csv": "COST_PARAMETER",
    }
    return {
        filename: tuple(
            canonical_sha256(
                {
                    "artifact": "S27_V2_LOCAL_SOURCE_ROW",
                    "row_family": row_family_by_file[filename],
                    "row_number": row_number,
                    "row": row,
                }
            )
            for row_number, row in enumerate(rows, start=1)
        )
        for filename, rows in rows_by_file.items()
    }


def _checks_by_label(bundle: RuntimeEvidenceGateBundle) -> dict[str, object]:
    checks = {check.check_label: check for check in bundle.checks}
    if tuple(checks) != tuple(check.check_label for check in bundle.checks):
        raise CarverBlocked("S27 v2 runtime-history remediation checks must have unique labels")
    return checks


def _level_row_hash_payload(row: RuntimeHistoryRemediationLevelLedgerRow) -> dict[str, object]:
    return {
        "artifact": "S27_V2_RUNTIME_HISTORY_REMEDIATION_LEVEL_COMPATIBILITY_ROW",
        "daily_continuous_close_price": row.daily_continuous_close_price,
        "daily_continuous_row_hash": row.daily_continuous_row_hash,
        "daily_current_contract_close_price": row.daily_current_contract_close_price,
        "daily_current_contract_row_hash": row.daily_current_contract_row_hash,
        "hourly_decision_close_price": row.hourly_decision_close_price,
        "hourly_decision_row_hash": row.hourly_decision_row_hash,
        "hourly_fill_close_price": row.hourly_fill_close_price,
        "hourly_fill_row_hash": row.hourly_fill_row_hash,
        "ledger_label": row.ledger_label,
        "level_bridge_proof_hash": row.level_bridge_proof_hash,
        "manifest_hash": row.manifest_hash,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "runtime_evidence_bundle_hash": row.runtime_evidence_bundle_hash,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "selected_fill_timestamp_utc": row.selected_fill_timestamp_utc,
        "selected_previous_daily_timestamp_utc": row.selected_previous_daily_timestamp_utc,
    }


def _runtime_row_hash_payload(row: RuntimeHistoryRemediationRuntimeLedgerRow) -> dict[str, object]:
    return {
        "artifact": "S27_V2_RUNTIME_HISTORY_REMEDIATION_RUNTIME_ROW",
        "daily_continuous_row_hashes": row.daily_continuous_row_hashes,
        "ewma5_check_hash": row.ewma5_check_hash,
        "ewmac_16_64_check_hash": row.ewmac_16_64_check_hash,
        "hourly_admissibility_check_hash": row.hourly_admissibility_check_hash,
        "hourly_decision_row_hashes": row.hourly_decision_row_hashes,
        "ledger_label": row.ledger_label,
        "level_compatibility_row_hash": row.level_compatibility_row_hash,
        "observed_daily_continuous_rows": row.observed_daily_continuous_rows,
        "reason_code": row.reason_code,
        "required_minimum_daily_continuous_rows": row.required_minimum_daily_continuous_rows,
        "row_status": row.row_status,
        "runtime_evidence_bundle_hash": row.runtime_evidence_bundle_hash,
        "runtime_numeric_values_emitted": row.runtime_numeric_values_emitted,
        "session_roll_check_hash": row.session_roll_check_hash,
        "strategy3_sigma_check_hash": row.strategy3_sigma_check_hash,
        "strict_prior_daily_check_hash": row.strict_prior_daily_check_hash,
        "vqm_check_hash": row.vqm_check_hash,
    }


def _bundle_hash_payload(bundle: RuntimeHistoryRemediationExecutableBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_RUNTIME_HISTORY_REMEDIATION_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "fill_rows_emitted": bundle.fill_rows_emitted,
        "forecast_rows_emitted": bundle.forecast_rows_emitted,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "level_compatibility_row_hash": bundle.level_compatibility_row.row_hash,
        "non_authorizations": bundle.non_authorizations,
        "order_rows_emitted": bundle.order_rows_emitted,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "runtime_evidence_bundle_hash": bundle.runtime_evidence_bundle.bundle_hash,
        "runtime_history_row_hash": bundle.runtime_history_row.row_hash,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "unresolved_gate_labels": bundle.unresolved_gate_labels,
    }

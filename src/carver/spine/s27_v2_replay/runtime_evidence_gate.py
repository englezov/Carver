from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import (
    BLOCKED_COST_SCHEMA,
    BLOCKED_LEVEL_COMPATIBILITY,
    BLOCKED_RUNTIME_HISTORY,
    BLOCKED_SIGMA,
    BLOCKED_TICK,
    BLOCKED_WORKING_LIMIT_LIFECYCLE,
    S27_V2_INSTRUMENT,
    S27_V2_LANE,
    S27_V2_STRATEGY_ID,
)
from .validation import require_hash, require_text


S27_V2_RUNTIME_EVIDENCE_GATE_STATUS = (
    "S27_V2_RUNTIME_EVIDENCE_GATE_FAIL_CLOSED_NOT_RESULT_NOT_EVIDENCE"
)
S27_V2_RUNTIME_EVIDENCE_GATE_AUTHORIZATION = "S27_V2_LOCAL_ONLY_RUNTIME_EVIDENCE_GATE"

PASS_LOCAL_DECLARED_ONLY = "PASS_LOCAL_DECLARED_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE"
PASS_COUNT_ONLY = "PASS_COUNT_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE"
PASS_LOCAL_PREVALIDATED = "PASS_LOCAL_PREVALIDATED_RUNTIME_EVIDENCE_NOT_SOURCE_FAITHFUL"
PASS_LOCAL_BRIDGE_PROOF = "PASS_LOCAL_LEVEL_BRIDGE_PROOF_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE"
FAIL_CLOSED = "FAIL_CLOSED_RUNTIME_EVIDENCE_INSUFFICIENT"

RUNTIME_EVIDENCE_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_FORECAST_ORDER_FILL_COST_PNL_RESULT_EVIDENCE_EMISSION",
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

REQUIRED_ROW_FAMILY_FILES = (
    "daily_continuous_completed_bar.csv",
    "daily_current_contract_completed_bar.csv",
    "hourly_decision_completed_bar.csv",
    "hourly_fill_completed_bar.csv",
    "session_calendar.csv",
    "roll_calendar.csv",
    "cost_parameter.csv",
)
FIRST_POPULATED_RUNTIME_EVIDENCE_PACK_RELATIVE_PATH = Path(
    "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260609_first_populated_dev_recon_znh2_20220103_multirow_declared_pack"
)
RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH = Path(
    "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260609_runtime_evidence_recon_znm6_20260413_declared_pack"
)
_REPO_ROOT = Path(__file__).resolve().parents[4]

RUNTIME_EVIDENCE_CHECK_LABELS = (
    "DECLARED_FILE_HASHES",
    "SELECTED_ROW_AUTHORITY",
    "STRICT_PRIOR_DAILY_ADMISSIBILITY",
    "HOURLY_DECISION_FILL_ADMISSIBILITY",
    "EWMA5_EVIDENCE",
    "EWMAC_16_64_EVIDENCE",
    "STRATEGY3_SIGMA_EVIDENCE",
    "VQM_EVIDENCE",
    "DAILY_HOURLY_LEVEL_BRIDGE",
    "SESSION_ROLL_COVERAGE",
    "TICK_ROUNDING_POLICY",
    "MULTIPLIER_CURRENCY_POLICY",
    "COMMISSION_SPREAD_POLICY",
    "WORKING_ORDER_LIFECYCLE",
)

FIRST_POPULATED_REQUIRED_STATUS_BY_LABEL = {
    "DECLARED_FILE_HASHES": PASS_LOCAL_DECLARED_ONLY,
    "SELECTED_ROW_AUTHORITY": PASS_LOCAL_DECLARED_ONLY,
    "STRICT_PRIOR_DAILY_ADMISSIBILITY": FAIL_CLOSED,
    "HOURLY_DECISION_FILL_ADMISSIBILITY": PASS_LOCAL_DECLARED_ONLY,
    "EWMA5_EVIDENCE": PASS_COUNT_ONLY,
    "EWMAC_16_64_EVIDENCE": PASS_COUNT_ONLY,
    "STRATEGY3_SIGMA_EVIDENCE": FAIL_CLOSED,
    "VQM_EVIDENCE": FAIL_CLOSED,
    "DAILY_HOURLY_LEVEL_BRIDGE": FAIL_CLOSED,
    "SESSION_ROLL_COVERAGE": PASS_LOCAL_DECLARED_ONLY,
    "TICK_ROUNDING_POLICY": FAIL_CLOSED,
    "MULTIPLIER_CURRENCY_POLICY": FAIL_CLOSED,
    "COMMISSION_SPREAD_POLICY": FAIL_CLOSED,
    "WORKING_ORDER_LIFECYCLE": FAIL_CLOSED,
}

FIRST_POPULATED_REQUIRED_GATE_BY_LABEL = {
    "DECLARED_FILE_HASHES": "DECLARED_LOCAL_PACK_FILES_HASHED",
    "SELECTED_ROW_AUTHORITY": "LOCAL_CONSTRUCTION_SELECTED_ROWS_BOUND_NOT_RUNTIME_EVIDENCE",
    "STRICT_PRIOR_DAILY_ADMISSIBILITY": "STRICT_PRIOR_DAILY_HISTORY_ADMISSIBILITY",
    "HOURLY_DECISION_FILL_ADMISSIBILITY": "STRICT_PRIOR_HOURLY_DECISION_FILL_ADMISSIBILITY",
    "EWMA5_EVIDENCE": "EWMA5_COUNT_ONLY_BLOCKED_BY_ADMISSIBILITY",
    "EWMAC_16_64_EVIDENCE": "EWMAC_16_64_COUNT_ONLY_BLOCKED_BY_ADMISSIBILITY",
    "STRATEGY3_SIGMA_EVIDENCE": BLOCKED_SIGMA,
    "VQM_EVIDENCE": BLOCKED_RUNTIME_HISTORY,
    "DAILY_HOURLY_LEVEL_BRIDGE": BLOCKED_LEVEL_COMPATIBILITY,
    "SESSION_ROLL_COVERAGE": "DECLARED_LOCAL_SESSION_ROLL_ROWS_HASHED_NOT_EXECUTION_POLICY",
    "TICK_ROUNDING_POLICY": BLOCKED_TICK,
    "MULTIPLIER_CURRENCY_POLICY": BLOCKED_COST_SCHEMA,
    "COMMISSION_SPREAD_POLICY": BLOCKED_COST_SCHEMA,
    "WORKING_ORDER_LIFECYCLE": BLOCKED_WORKING_LIMIT_LIFECYCLE,
}

REMEDIATION_REQUIRED_STATUS_BY_LABEL = {
    "DECLARED_FILE_HASHES": PASS_LOCAL_DECLARED_ONLY,
    "SELECTED_ROW_AUTHORITY": PASS_LOCAL_DECLARED_ONLY,
    "STRICT_PRIOR_DAILY_ADMISSIBILITY": PASS_LOCAL_DECLARED_ONLY,
    "HOURLY_DECISION_FILL_ADMISSIBILITY": PASS_LOCAL_DECLARED_ONLY,
    "EWMA5_EVIDENCE": PASS_COUNT_ONLY,
    "EWMAC_16_64_EVIDENCE": PASS_LOCAL_PREVALIDATED,
    "STRATEGY3_SIGMA_EVIDENCE": PASS_LOCAL_PREVALIDATED,
    "VQM_EVIDENCE": PASS_LOCAL_PREVALIDATED,
    "DAILY_HOURLY_LEVEL_BRIDGE": PASS_LOCAL_BRIDGE_PROOF,
    "SESSION_ROLL_COVERAGE": PASS_LOCAL_DECLARED_ONLY,
    "TICK_ROUNDING_POLICY": FAIL_CLOSED,
    "MULTIPLIER_CURRENCY_POLICY": FAIL_CLOSED,
    "COMMISSION_SPREAD_POLICY": FAIL_CLOSED,
    "WORKING_ORDER_LIFECYCLE": FAIL_CLOSED,
}

REMEDIATION_REQUIRED_GATE_BY_LABEL = {
    "DECLARED_FILE_HASHES": "DECLARED_LOCAL_PACK_FILES_HASHED",
    "SELECTED_ROW_AUTHORITY": "LOCAL_CONSTRUCTION_SELECTED_ROWS_BOUND_NOT_RUNTIME_EVIDENCE",
    "STRICT_PRIOR_DAILY_ADMISSIBILITY": "STRICT_PRIOR_DAILY_HISTORY_ADMISSIBILITY",
    "HOURLY_DECISION_FILL_ADMISSIBILITY": "STRICT_PRIOR_HOURLY_DECISION_FILL_ADMISSIBILITY",
    "EWMA5_EVIDENCE": "EWMA5_COUNT_ONLY_BLOCKED_BY_EXECUTION_POLICY",
    "EWMAC_16_64_EVIDENCE": "LOCAL_PREVALIDATED_EWMAC16_RUNTIME_EVIDENCE_BOUND_NOT_RESULT",
    "STRATEGY3_SIGMA_EVIDENCE": "LOCAL_PREVALIDATED_STRATEGY3_SIGMA_RUNTIME_EVIDENCE_BOUND_NOT_RESULT",
    "VQM_EVIDENCE": "LOCAL_PREVALIDATED_VQM_RUNTIME_EVIDENCE_BOUND_NOT_RESULT",
    "DAILY_HOURLY_LEVEL_BRIDGE": "LOCAL_LEVEL_SPACE_BRIDGE_PROOF_BOUND_NOT_PRICE_EQUALITY_NOT_RESULT",
    "SESSION_ROLL_COVERAGE": "DECLARED_LOCAL_SESSION_ROLL_ROWS_HASHED_NOT_EXECUTION_POLICY",
    "TICK_ROUNDING_POLICY": BLOCKED_TICK,
    "MULTIPLIER_CURRENCY_POLICY": BLOCKED_COST_SCHEMA,
    "COMMISSION_SPREAD_POLICY": BLOCKED_COST_SCHEMA,
    "WORKING_ORDER_LIFECYCLE": BLOCKED_WORKING_LIMIT_LIFECYCLE,
}

AUTHORIZED_RUNTIME_EVIDENCE_PACK_PROFILES = (
    {
        "profile": "FIRST_POPULATED",
        "relative_path": FIRST_POPULATED_RUNTIME_EVIDENCE_PACK_RELATIVE_PATH,
        "manifest_filename": "S27_V2_FIRST_POPULATED_DECLARED_INPUT_PACK_MANIFEST.json",
        "required_status_by_label": FIRST_POPULATED_REQUIRED_STATUS_BY_LABEL,
        "required_gate_by_label": FIRST_POPULATED_REQUIRED_GATE_BY_LABEL,
    },
    {
        "profile": "RUNTIME_EVIDENCE_REMEDIATION",
        "relative_path": RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH,
        "manifest_filename": "S27_V2_RUNTIME_EVIDENCE_REMEDIATION_DECLARED_INPUT_PACK_MANIFEST.json",
        "required_status_by_label": REMEDIATION_REQUIRED_STATUS_BY_LABEL,
        "required_gate_by_label": REMEDIATION_REQUIRED_GATE_BY_LABEL,
    },
)

REMEDIATION_SOURCE_FILES = {
    "daily_risk_history": Path(
        "docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/"
        "ten_year_vol_history_runtime_2026-05-31/ledger/"
        "20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_local_continuous_daily_risk_history.csv"
    ),
    "vqm_daily_ledger": Path(
        "docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/"
        "ten_year_vol_history_runtime_2026-05-31/ledger/"
        "20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_relative_vol_v_q_m_daily_ledger.csv"
    ),
    "vqm_runtime_rows": Path(
        "docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/"
        "ten_year_vol_history_runtime_2026-05-31/runtime_rows/"
        "20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_runtime_rows.csv"
    ),
    "sigma_runtime_ledger": Path(
        "docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/"
        "2026-04-13_2026-05-22/forecast_series_only_output/2026-05-31/"
        "sigma_runtime_ledger/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_runtime_ledger.csv"
    ),
    "ewmac_runtime_rows": Path(
        "docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/"
        "ewmac16_trend_runtime_ledger_2026-05-31/runtime_rows/"
        "20260531_ZN_S27_EWMAC16_TREND_RUNTIME_LEDGER_runtime_rows.csv"
    ),
    "hourly_sanitized_bars": Path(
        "docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/"
        "2026-04-13_2026-05-22/databento_ohlcv_1h_extended_forecast_only_quarantine/"
        "sanitized_bars/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_sanitized_quarantine_ohlcv_1h.csv"
    ),
    "roll_plan": Path(
        "docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/"
        "local_continuous_daily_lineage_2026-05-31/ledger/"
        "20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_roll_plan.csv"
    ),
    "symbology": Path(
        "docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/"
        "zn_lifecycle_databento_definition_probe_2026-05-31/raw_provider_metadata/"
        "20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_symbology_raw_symbol_to_instrument_id.json"
    ),
}


@dataclass(frozen=True)
class RuntimeEvidenceGateCheck:
    check_label: str
    status: str
    gate_label: str
    summary: str
    observed_value_hash: str

    def validate(self) -> None:
        require_text("S27 v2 runtime evidence check label", self.check_label)
        if self.check_label not in RUNTIME_EVIDENCE_CHECK_LABELS:
            raise CarverBlocked("S27 v2 runtime evidence check label is not locked")
        require_text("S27 v2 runtime evidence check status", self.status)
        if self.status not in (
            PASS_LOCAL_DECLARED_ONLY,
            PASS_COUNT_ONLY,
            PASS_LOCAL_PREVALIDATED,
            PASS_LOCAL_BRIDGE_PROOF,
            FAIL_CLOSED,
        ):
            raise CarverBlocked("S27 v2 runtime evidence check status is not locked")
        require_text("S27 v2 runtime evidence gate label", self.gate_label)
        require_text("S27 v2 runtime evidence check summary", self.summary)
        require_hash("S27 v2 runtime evidence observed value hash", self.observed_value_hash)


@dataclass(frozen=True)
class RuntimeEvidenceGateBundle:
    status: str
    authorization: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    manifest_hash: str
    declared_file_hashes: tuple[tuple[str, str], ...]
    selected_decision_timestamp_utc: str
    selected_fill_timestamp_utc: str
    selected_previous_daily_timestamp_utc: str
    checks: tuple[RuntimeEvidenceGateCheck, ...]
    fail_closed_gate_labels: tuple[str, ...]
    runtime_evidence_ready: bool
    forecast_rows_emitted: bool
    order_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_rows_emitted: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = RUNTIME_EVIDENCE_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_RUNTIME_EVIDENCE_GATE_STATUS:
            raise CarverBlocked("S27 v2 runtime evidence gate must remain fail-closed")
        if self.authorization != S27_V2_RUNTIME_EVIDENCE_GATE_AUTHORIZATION:
            raise CarverBlocked("S27 v2 runtime evidence gate authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 runtime evidence gate must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 runtime evidence gate must remain source-native futures")
        require_text("S27 v2 runtime evidence input pack path", self.input_pack_path)
        require_hash("S27 v2 runtime evidence manifest hash", self.manifest_hash)
        if tuple(name for name, _hash_value in self.declared_file_hashes) != REQUIRED_ROW_FAMILY_FILES:
            raise CarverBlocked("S27 v2 runtime evidence declared files must match locked row families")
        for name, hash_value in self.declared_file_hashes:
            require_text("S27 v2 runtime evidence declared file name", name)
            require_hash(f"S27 v2 runtime evidence declared file {name}", hash_value)
        if tuple(check.check_label for check in self.checks) != RUNTIME_EVIDENCE_CHECK_LABELS:
            raise CarverBlocked("S27 v2 runtime evidence checks must match locked coverage labels")
        profile = _runtime_evidence_pack_profile_for_path(Path(self.input_pack_path))
        required_status_by_label = profile["required_status_by_label"]
        required_gate_by_label = profile["required_gate_by_label"]
        for check in self.checks:
            check.validate()
            if check.status != required_status_by_label[check.check_label]:
                raise CarverBlocked("S27 v2 runtime evidence check status must bind locked gate semantics")
            if check.gate_label != required_gate_by_label[check.check_label]:
                raise CarverBlocked("S27 v2 runtime evidence check gate label must bind locked gate semantics")
        expected_fail_closed_gate_labels = tuple(
            dict.fromkeys(
                check.gate_label
                for check in self.checks
                if check.status == FAIL_CLOSED
            )
        )
        if self.fail_closed_gate_labels != expected_fail_closed_gate_labels:
            raise CarverBlocked("S27 v2 runtime evidence fail-closed gates must bind failed checks exactly")
        for gate_label in self.fail_closed_gate_labels:
            require_text("S27 v2 runtime evidence fail-closed gate label", gate_label)
        if self.runtime_evidence_ready:
            raise CarverBlocked("S27 v2 runtime evidence gate cannot claim runtime readiness")
        if any(
            (
                self.forecast_rows_emitted,
                self.order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_rows_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 runtime evidence gate cannot emit downstream result surfaces")
        if self.non_authorizations != RUNTIME_EVIDENCE_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 runtime evidence gate must preserve non-authorizations")
        require_hash("S27 v2 runtime evidence bundle hash", self.bundle_hash)
        if self.bundle_hash != _runtime_evidence_bundle_hash(self):
            raise CarverBlocked("S27 v2 runtime evidence bundle hash must bind gate contents")
        active_bundle = build_runtime_evidence_gate(self.input_pack_path, _skip_validate=True)
        if (
            self.manifest_hash != active_bundle.manifest_hash
            or self.declared_file_hashes != active_bundle.declared_file_hashes
            or self.selected_decision_timestamp_utc != active_bundle.selected_decision_timestamp_utc
            or self.selected_fill_timestamp_utc != active_bundle.selected_fill_timestamp_utc
            or self.selected_previous_daily_timestamp_utc != active_bundle.selected_previous_daily_timestamp_utc
            or self.checks != active_bundle.checks
            or self.fail_closed_gate_labels != active_bundle.fail_closed_gate_labels
        ):
            raise CarverBlocked("S27 v2 runtime evidence bundle must match active local pack evidence")


def build_runtime_evidence_gate(
    input_pack_path: str | Path,
    *,
    _skip_validate: bool = False,
) -> RuntimeEvidenceGateBundle:
    pack_path = Path(input_pack_path).resolve()
    profile = _runtime_evidence_pack_profile_for_path(pack_path)
    required_status_by_label = profile["required_status_by_label"]
    required_gate_by_label = profile["required_gate_by_label"]
    if not pack_path.is_dir():
        raise CarverBlocked("S27 v2 runtime evidence input pack directory is missing")

    manifest_path = pack_path / str(profile["manifest_filename"])
    manifest_bytes = manifest_path.read_bytes()
    manifest_hash = sha256(manifest_bytes).hexdigest()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    row_family_files = manifest.get("row_family_files")
    if not isinstance(row_family_files, dict):
        raise CarverBlocked("S27 v2 runtime evidence manifest row family map is unresolved")

    declared_file_hashes = tuple(
        (filename, _verify_declared_file_hash(pack_path, filename, row_family_files))
        for filename in REQUIRED_ROW_FAMILY_FILES
    )
    rows_by_file = {
        filename: _read_csv_rows(pack_path / filename)
        for filename in REQUIRED_ROW_FAMILY_FILES
    }
    source_evidence = _runtime_source_evidence(profile, manifest, rows_by_file)

    selected_daily = rows_by_file["daily_continuous_completed_bar.csv"][0]
    selected_daily_current = rows_by_file["daily_current_contract_completed_bar.csv"][0]
    selected_hourly_decision = rows_by_file["hourly_decision_completed_bar.csv"][0]
    selected_hourly_fill = rows_by_file["hourly_fill_completed_bar.csv"][0]

    selected_decision_timestamp = _manifest_text(manifest, "selected_decision_timestamp_utc")
    selected_fill_timestamp = _manifest_text(manifest, "selected_fill_timestamp_utc")
    selected_previous_daily_timestamp = _manifest_text(manifest, "selected_previous_daily_timestamp_utc")

    daily_admissible, daily_summary = _strict_prior_daily_admissibility(
        selected_previous_daily_timestamp,
        rows_by_file["daily_continuous_completed_bar.csv"],
    )
    hourly_admissible, hourly_summary = _hourly_decision_fill_admissibility(
        selected_decision_timestamp,
        selected_fill_timestamp,
        rows_by_file["hourly_decision_completed_bar.csv"],
        rows_by_file["hourly_fill_completed_bar.csv"],
    )
    same_level, level_summary = _level_bridge_summary(
        selected_daily,
        selected_daily_current,
        selected_hourly_decision,
        selected_hourly_fill,
    )
    history_evidence = manifest.get("history_evidence", {})
    if not isinstance(history_evidence, dict):
        raise CarverBlocked("S27 v2 runtime evidence history evidence is unresolved")

    checks = (
        _check(
            "DECLARED_FILE_HASHES",
            PASS_LOCAL_DECLARED_ONLY,
            "DECLARED_LOCAL_PACK_FILES_HASHED",
            f"{len(declared_file_hashes)} declared row-family files byte-SHA verified against manifest",
            declared_file_hashes,
        ),
        _check(
            "SELECTED_ROW_AUTHORITY",
            PASS_LOCAL_DECLARED_ONLY,
            "LOCAL_CONSTRUCTION_SELECTED_ROWS_BOUND_NOT_RUNTIME_EVIDENCE",
            "selected daily/current/hourly rows are present in hashed declared files; authority remains construction-only",
            (
                selected_daily.get("row_locator", ""),
                selected_daily_current.get("row_locator", ""),
                selected_hourly_decision.get("row_locator", ""),
                selected_hourly_fill.get("row_locator", ""),
            ),
        ),
        _check(
            "STRICT_PRIOR_DAILY_ADMISSIBILITY",
            required_status_by_label["STRICT_PRIOR_DAILY_ADMISSIBILITY"] if daily_admissible else FAIL_CLOSED,
            required_gate_by_label["STRICT_PRIOR_DAILY_ADMISSIBILITY"],
            daily_summary,
            tuple(row.get("completed_timestamp_utc", "") for row in rows_by_file["daily_continuous_completed_bar.csv"]),
        ),
        _check(
            "HOURLY_DECISION_FILL_ADMISSIBILITY",
            required_status_by_label["HOURLY_DECISION_FILL_ADMISSIBILITY"] if hourly_admissible else FAIL_CLOSED,
            required_gate_by_label["HOURLY_DECISION_FILL_ADMISSIBILITY"],
            hourly_summary,
            (
                tuple(row.get("completed_timestamp_utc", "") for row in rows_by_file["hourly_decision_completed_bar.csv"]),
                tuple(row.get("completed_timestamp_utc", "") for row in rows_by_file["hourly_fill_completed_bar.csv"]),
            ),
        ),
        _check(
            "EWMA5_EVIDENCE",
            PASS_COUNT_ONLY if len(rows_by_file["daily_continuous_completed_bar.csv"]) >= 5 else FAIL_CLOSED,
            required_gate_by_label["EWMA5_EVIDENCE"],
            source_evidence["ewma5_summary"],
            len(rows_by_file["daily_continuous_completed_bar.csv"]),
        ),
        _check(
            "EWMAC_16_64_EVIDENCE",
            required_status_by_label["EWMAC_16_64_EVIDENCE"]
            if len(rows_by_file["daily_continuous_completed_bar.csv"]) >= 64
            else FAIL_CLOSED,
            required_gate_by_label["EWMAC_16_64_EVIDENCE"],
            source_evidence["ewmac_summary"],
            source_evidence["ewmac_observed"],
        ),
        _check(
            "STRATEGY3_SIGMA_EVIDENCE",
            required_status_by_label["STRATEGY3_SIGMA_EVIDENCE"],
            required_gate_by_label["STRATEGY3_SIGMA_EVIDENCE"],
            source_evidence["sigma_summary"],
            source_evidence["sigma_observed"],
        ),
        _check(
            "VQM_EVIDENCE",
            required_status_by_label["VQM_EVIDENCE"],
            required_gate_by_label["VQM_EVIDENCE"],
            source_evidence["vqm_summary"],
            source_evidence["vqm_observed"],
        ),
        _check(
            "DAILY_HOURLY_LEVEL_BRIDGE",
            required_status_by_label["DAILY_HOURLY_LEVEL_BRIDGE"],
            required_gate_by_label["DAILY_HOURLY_LEVEL_BRIDGE"],
            source_evidence["level_bridge_summary"] if source_evidence["level_bridge_summary"] else level_summary,
            source_evidence["level_bridge_observed"]
            if source_evidence["level_bridge_observed"]
            else (
                selected_daily.get("close_price", ""),
                selected_daily_current.get("close_price", ""),
                selected_hourly_decision.get("close_price", ""),
                selected_hourly_fill.get("close_price", ""),
                same_level,
            ),
        ),
        _check(
            "SESSION_ROLL_COVERAGE",
            PASS_LOCAL_DECLARED_ONLY,
            "DECLARED_LOCAL_SESSION_ROLL_ROWS_HASHED_NOT_EXECUTION_POLICY",
            "declared session and roll rows are present and hashed, but do not authorize execution-policy evidence",
            (
                rows_by_file["session_calendar.csv"][0].get("row_locator", ""),
                rows_by_file["roll_calendar.csv"][0].get("row_locator", ""),
            ),
        ),
        _check(
            "TICK_ROUNDING_POLICY",
            FAIL_CLOSED,
            BLOCKED_TICK,
            "declared pack does not bind a source-locked ZN tick/rounding executable policy",
            rows_by_file["cost_parameter.csv"][0].get("raw_symbol", ""),
        ),
        _check(
            "MULTIPLIER_CURRENCY_POLICY",
            FAIL_CLOSED,
            BLOCKED_COST_SCHEMA,
            "declared multiplier/currency policy hashes are present but not source-locked executable cost evidence",
            (
                rows_by_file["cost_parameter.csv"][0].get("contract_multiplier_value_hash", ""),
                rows_by_file["cost_parameter.csv"][0].get("currency_policy_hash", ""),
            ),
        ),
        _check(
            "COMMISSION_SPREAD_POLICY",
            FAIL_CLOSED,
            BLOCKED_COST_SCHEMA,
            "declared commission/spread policy hashes are present but not source-locked executable cost evidence",
            (
                rows_by_file["cost_parameter.csv"][0].get("commission_policy_hash", ""),
                rows_by_file["cost_parameter.csv"][0].get("spread_policy_hash", ""),
            ),
        ),
        _check(
            "WORKING_ORDER_LIFECYCLE",
            FAIL_CLOSED,
            BLOCKED_WORKING_LIMIT_LIFECYCLE,
            "declared pack does not contain source-locked working limit-order lifecycle evidence",
            selected_decision_timestamp,
        ),
    )

    fail_closed_gate_labels = tuple(
        dict.fromkeys(
            check.gate_label
            for check in checks
            if check.status == FAIL_CLOSED
        )
    )
    bundle = RuntimeEvidenceGateBundle(
        status=S27_V2_RUNTIME_EVIDENCE_GATE_STATUS,
        authorization=S27_V2_RUNTIME_EVIDENCE_GATE_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        manifest_hash=manifest_hash,
        declared_file_hashes=declared_file_hashes,
        selected_decision_timestamp_utc=selected_decision_timestamp,
        selected_fill_timestamp_utc=selected_fill_timestamp,
        selected_previous_daily_timestamp_utc=selected_previous_daily_timestamp,
        checks=checks,
        fail_closed_gate_labels=fail_closed_gate_labels,
        runtime_evidence_ready=False,
        forecast_rows_emitted=False,
        order_rows_emitted=False,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_rows_emitted=False,
        bundle_hash="0" * 64,
    )
    bundle = RuntimeEvidenceGateBundle(
        **{
            **bundle.__dict__,
            "bundle_hash": _runtime_evidence_bundle_hash(bundle),
        }
    )
    if not _skip_validate:
        bundle.validate()
    return bundle


def _verify_declared_file_hash(
    pack_path: Path,
    filename: str,
    row_family_files: dict[str, Any],
) -> str:
    declared = row_family_files.get(filename)
    if not isinstance(declared, dict):
        raise CarverBlocked(f"S27 v2 runtime evidence manifest missing {filename}")
    expected = declared.get("sha256")
    if not isinstance(expected, str):
        raise CarverBlocked(f"S27 v2 runtime evidence manifest hash missing {filename}")
    observed = sha256((pack_path / filename).read_bytes()).hexdigest()
    if observed != expected.lower():
        raise CarverBlocked(f"S27 v2 runtime evidence declared file hash mismatch for {filename}")
    return observed


def _runtime_evidence_pack_profile_for_path(pack_path: Path) -> dict[str, Any]:
    resolved_pack = pack_path.resolve()
    for profile in AUTHORIZED_RUNTIME_EVIDENCE_PACK_PROFILES:
        expected_path = (_REPO_ROOT / profile["relative_path"]).resolve()
        if resolved_pack == expected_path:
            return profile
    raise CarverBlocked("S27 v2 runtime evidence gate is locked to authorized runtime evidence packs")


def _runtime_source_evidence(
    profile: dict[str, Any],
    manifest: dict[str, Any],
    rows_by_file: dict[str, list[dict[str, str]]],
) -> dict[str, object]:
    if profile["profile"] == "RUNTIME_EVIDENCE_REMEDIATION":
        return _remediation_source_evidence(manifest, rows_by_file)
    history_evidence = manifest.get("history_evidence", {})
    if not isinstance(history_evidence, dict):
        raise CarverBlocked("S27 v2 runtime evidence history evidence is unresolved")
    return {
        "ewmac_summary": (
            "daily continuous count is sufficient for EWMAC(16,64), but runtime use remains blocked "
            "until strict-prior continuity is proved"
        ),
        "ewma5_summary": (
            "daily continuous count is sufficient for EWMA5, but runtime use remains blocked until "
            "strict-prior continuity is proved"
        ),
        "ewmac_observed": len(rows_by_file["daily_continuous_completed_bar.csv"]),
        "sigma_summary": (
            "selected sigma source is not source-faithful runtime evidence: "
            f"{history_evidence.get('selected_sigma_source', '')}"
        ),
        "sigma_observed": history_evidence.get("selected_sigma_source", ""),
        "vqm_summary": (
            "V/Q/M evidence is stale for selected decision timestamp; "
            f"latest local V/Q/M date {history_evidence.get('vqm_source_latest_completed_trading_date', '')}"
        ),
        "vqm_observed": (
            history_evidence.get("vqm_source_latest_completed_trading_date", ""),
            manifest.get("selected_decision_timestamp_utc", ""),
        ),
        "level_bridge_summary": "",
        "level_bridge_observed": (),
    }


def _remediation_source_evidence(
    manifest: dict[str, Any],
    rows_by_file: dict[str, list[dict[str, str]]],
) -> dict[str, object]:
    history_evidence = manifest.get("history_evidence")
    if not isinstance(history_evidence, dict):
        raise CarverBlocked("S27 v2 remediation history evidence is unresolved")
    source_files = manifest.get("source_files")
    if not isinstance(source_files, dict) or set(source_files) != set(REMEDIATION_SOURCE_FILES):
        raise CarverBlocked("S27 v2 remediation source files must match locked local evidence set")
    for source_label, expected_relative_path in REMEDIATION_SOURCE_FILES.items():
        declared = source_files.get(source_label)
        if not isinstance(declared, dict):
            raise CarverBlocked("S27 v2 remediation source declaration is unresolved")
        declared_path = declared.get("path")
        if not isinstance(declared_path, str):
            raise CarverBlocked("S27 v2 remediation source path is unresolved")
        if declared_path.replace("\\", "/") != expected_relative_path.as_posix():
            raise CarverBlocked("S27 v2 remediation source path must bind locked local evidence")
        declared_hash = declared.get("sha256")
        if not isinstance(declared_hash, str):
            raise CarverBlocked("S27 v2 remediation source hash is unresolved")
        require_hash("S27 v2 remediation source hash", declared_hash.lower())
        observed_hash = sha256((_REPO_ROOT / expected_relative_path).read_bytes()).hexdigest()
        if observed_hash != declared_hash.lower():
            raise CarverBlocked("S27 v2 remediation source hash must match local bytes")

    selected_decision = _manifest_text(manifest, "selected_decision_timestamp_utc")
    selected_fill = _manifest_text(manifest, "selected_fill_timestamp_utc")
    selected_previous_daily = _manifest_text(manifest, "selected_previous_daily_timestamp_utc")
    selected_date = selected_previous_daily[:10]
    selected_raw_symbol = _manifest_text(manifest, "selected_raw_symbol")

    source_rows = {
        label: _read_csv_rows(_REPO_ROOT / path)
        for label, path in REMEDIATION_SOURCE_FILES.items()
        if path.suffix.lower() == ".csv"
    }
    daily_risk = _row_by_value(source_rows["daily_risk_history"], "completed_trading_date", selected_date)
    vqm_daily = _row_by_value(source_rows["vqm_daily_ledger"], "completed_trading_date", selected_date)
    vqm_runtime = _row_by_value(source_rows["vqm_runtime_rows"], "as_of", selected_decision)
    sigma_runtime = _row_by_value(source_rows["sigma_runtime_ledger"], "as_of", selected_decision)
    ewmac_runtime = _row_by_value(source_rows["ewmac_runtime_rows"], "as_of", selected_decision)
    hourly_decision_source = _row_by_value(
        source_rows["hourly_sanitized_bars"],
        "derived_completed_bar_end_utc",
        selected_decision,
    )
    hourly_fill_source = _row_by_value(
        source_rows["hourly_sanitized_bars"],
        "derived_completed_bar_end_utc",
        selected_fill,
    )

    selected_daily_continuous = rows_by_file["daily_continuous_completed_bar.csv"][0]
    selected_daily_current = rows_by_file["daily_current_contract_completed_bar.csv"][0]
    selected_hourly_decision = rows_by_file["hourly_decision_completed_bar.csv"][0]
    selected_hourly_fill = rows_by_file["hourly_fill_completed_bar.csv"][0]

    _require_equal(daily_risk["raw_symbol"], selected_raw_symbol, "daily risk raw symbol")
    _require_equal(daily_risk["raw_close"], selected_daily_current["close_price"], "daily current close")
    _require_equal(daily_risk["continuous_close"], selected_daily_continuous["close_price"], "daily continuous close")
    _require_equal(vqm_daily["sigma_i_t"], selected_daily_continuous["annual_percentage_sigma"], "daily sigma")
    _require_equal(vqm_daily["sigma_i_t"], selected_daily_current["annual_percentage_sigma"], "current daily sigma")
    _require_equal(sigma_runtime["sigma_percent_t"], selected_daily_continuous["annual_percentage_sigma"], "sigma runtime")
    _require_equal(vqm_runtime["source_vqm_completed_trading_date"], selected_date, "V/Q/M source date")
    _require_equal(vqm_runtime["vol_multiplier"], history_evidence.get("selected_vqm_multiplier_m"), "V/Q/M multiplier")
    _require_equal(vqm_runtime["quantile_q"], history_evidence.get("selected_vqm_quantile_q"), "V/Q/M quantile")
    _require_equal(
        vqm_runtime["relative_volatility_v"],
        history_evidence.get("selected_vqm_relative_volatility_v"),
        "V/Q/M relative volatility",
    )
    _require_equal(
        vqm_daily["historical_v_observation_count"],
        history_evidence.get("selected_vqm_daily_historical_observation_count"),
        "V/Q/M observation count",
    )
    _require_equal(
        vqm_runtime["source_artifact_sha256"].lower(),
        sha256((_REPO_ROOT / REMEDIATION_SOURCE_FILES["vqm_daily_ledger"]).read_bytes()).hexdigest(),
        "V/Q/M source artifact hash",
    )
    _require_equal(
        ewmac_runtime["daily_rows_used"],
        str(len(rows_by_file["daily_continuous_completed_bar.csv"])),
        "EWMAC daily rows used",
    )
    _require_equal(ewmac_runtime["first_daily_row_used"], history_evidence.get("daily_history_first_prior_trading_date"), "EWMAC first daily")
    _require_equal(ewmac_runtime["last_daily_row_used"], selected_date, "EWMAC last daily")
    _require_equal(hourly_decision_source["raw_symbol"], selected_hourly_decision["raw_symbol"], "hourly decision raw symbol")
    _require_equal(hourly_decision_source["close"], selected_hourly_decision["close_price"], "hourly decision close")
    _require_equal(hourly_fill_source["raw_symbol"], selected_hourly_fill["raw_symbol"], "hourly fill raw symbol")
    _require_equal(hourly_fill_source["close"], selected_hourly_fill["close_price"], "hourly fill close")
    if sigma_runtime["runtime_status"] != "PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 remediation sigma status must bind local prevalidated source row")
    if sigma_runtime["method_status"] != "LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY":
        raise CarverBlocked("S27 v2 remediation sigma method must bind Strategy 3 source family")
    if sigma_runtime["no_lookahead_status"] != "PASS_NO_LOOKAHEAD":
        raise CarverBlocked("S27 v2 remediation sigma row must be no-lookahead")
    if ewmac_runtime["runtime_status"] != "PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 remediation EWMAC status must bind local prevalidated source row")
    if ewmac_runtime["no_lookahead_status"] != "PASS_NO_LOOKAHEAD":
        raise CarverBlocked("S27 v2 remediation EWMAC row must be no-lookahead")
    if vqm_runtime["runtime_status"] != "PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE":
        raise CarverBlocked("S27 v2 remediation V/Q/M status must bind local prevalidated source row")
    if vqm_runtime["no_lookahead_status"] != "PASS_NO_LOOKAHEAD":
        raise CarverBlocked("S27 v2 remediation V/Q/M row must be no-lookahead")

    level_bridge_proof = manifest.get("level_bridge_proof")
    if not isinstance(level_bridge_proof, dict):
        raise CarverBlocked("S27 v2 remediation level bridge proof is unresolved")
    if _json_hash(level_bridge_proof) != history_evidence.get("level_bridge_proof_hash"):
        raise CarverBlocked("S27 v2 remediation level bridge proof hash must bind manifest proof")
    if level_bridge_proof.get("daily_active_contract") != selected_raw_symbol:
        raise CarverBlocked("S27 v2 remediation level bridge must bind daily active contract")
    if level_bridge_proof.get("hourly_active_contract") != selected_raw_symbol:
        raise CarverBlocked("S27 v2 remediation level bridge must bind hourly active contract")
    if level_bridge_proof.get("daily_additive_back_adjustment") != "0.0":
        raise CarverBlocked("S27 v2 remediation level bridge must bind zero daily adjustment")
    if level_bridge_proof.get("hourly_additive_back_adjustment_applied_for_bridge") != "0.0":
        raise CarverBlocked("S27 v2 remediation level bridge must bind zero hourly adjustment")
    if level_bridge_proof.get("source_daily_risk_history_sha256") != source_files["daily_risk_history"]["sha256"]:
        raise CarverBlocked("S27 v2 remediation level bridge must bind daily source hash")
    if level_bridge_proof.get("source_hourly_sanitized_bars_sha256") != source_files["hourly_sanitized_bars"]["sha256"]:
        raise CarverBlocked("S27 v2 remediation level bridge must bind hourly source hash")
    if history_evidence.get("tick_rounding_policy_status") != "FAIL_CLOSED_UNRESOLVED":
        raise CarverBlocked("S27 v2 remediation tick policy must remain fail-closed")
    if history_evidence.get("commission_spread_policy_status") != "FAIL_CLOSED_UNRESOLVED":
        raise CarverBlocked("S27 v2 remediation commission/spread policy must remain fail-closed")
    if history_evidence.get("working_order_lifecycle_status") != "FAIL_CLOSED_UNRESOLVED":
        raise CarverBlocked("S27 v2 remediation working-order lifecycle must remain fail-closed")

    return {
        "ewmac_summary": (
            "local EWMAC(16,64) runtime evidence is bound to the selected decision timestamp, "
            "135 named strict-prior daily rows, and no-lookahead source status; not result evidence"
        ),
        "ewma5_summary": (
            "daily continuous count and strict-prior ordering are sufficient for local EWMA5 evidence; "
            "this remains count/local evidence only and does not emit forecasts or results"
        ),
        "ewmac_observed": (
            ewmac_runtime["as_of"],
            ewmac_runtime["daily_rows_used"],
            ewmac_runtime["first_daily_row_used"],
            ewmac_runtime["last_daily_row_used"],
            ewmac_runtime["source_artifact_sha256"],
        ),
        "sigma_summary": (
            "local Strategy 3 sigma runtime evidence is bound to the selected decision timestamp "
            "and selected previous daily sigma; not result evidence"
        ),
        "sigma_observed": (
            sigma_runtime["as_of"],
            sigma_runtime["sigma_percent_t"],
            sigma_runtime["method_status"],
            sigma_runtime["source_window_ledger_sha256"],
        ),
        "vqm_summary": (
            "local V/Q/M runtime evidence is bound to selected decision timestamp, source completed date, "
            "V, Q, M, and daily ledger artifact hash; not result evidence"
        ),
        "vqm_observed": (
            vqm_runtime["as_of"],
            vqm_runtime["source_vqm_completed_trading_date"],
            vqm_runtime["relative_volatility_v"],
            vqm_runtime["quantile_q"],
            vqm_runtime["vol_multiplier"],
            vqm_runtime["source_artifact_sha256"],
        ),
        "level_bridge_summary": (
            "local level-space bridge proof binds ZNM6 daily continuous/current rows and ZNM6 hourly rows "
            "through zero additive adjustment; this is not price equality across different hours and not result evidence"
        ),
        "level_bridge_observed": (
            level_bridge_proof.get("bridge_disposition"),
            selected_daily_continuous.get("close_price", ""),
            selected_daily_current.get("close_price", ""),
            selected_hourly_decision.get("close_price", ""),
            selected_hourly_fill.get("close_price", ""),
            history_evidence.get("level_bridge_proof_hash", ""),
        ),
    }


def _row_by_value(rows: list[dict[str, str]], column: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(column) == value]
    if len(matches) != 1:
        raise CarverBlocked(f"S27 v2 remediation source row must have exactly one {column}={value}")
    return matches[0]


def _require_equal(left: object, right: object, label: str) -> None:
    if left != right:
        raise CarverBlocked(f"S27 v2 remediation evidence mismatch for {label}")


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise CarverBlocked(f"S27 v2 runtime evidence file {path.name} has no rows")
    return rows


def _manifest_text(manifest: dict[str, Any], label: str) -> str:
    value = manifest.get(label)
    if not isinstance(value, str) or not value:
        raise CarverBlocked(f"S27 v2 runtime evidence manifest {label} is unresolved")
    return value


def _parse_z_timestamp(value: str) -> datetime:
    if not value.endswith("Z"):
        raise CarverBlocked("S27 v2 runtime evidence timestamp must be UTC Z-normalized")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.tzinfo != timezone.utc:
        parsed = parsed.astimezone(timezone.utc)
    return parsed


def _strict_prior_daily_admissibility(
    selected_previous_daily_timestamp: str,
    daily_rows: list[dict[str, str]],
) -> tuple[bool, str]:
    selected = _parse_z_timestamp(selected_previous_daily_timestamp)
    timestamps = [_parse_z_timestamp(row.get("completed_timestamp_utc", "")) for row in daily_rows]
    if timestamps[0] != selected:
        return False, "first daily continuous row does not match selected previous completed daily timestamp"
    prior = timestamps[1:]
    if any(timestamp >= selected for timestamp in prior):
        return False, "daily history contains non-strict-prior rows after the selected row"
    if prior != sorted(prior):
        return False, "daily strict-prior rows are not chronological after the selected row"
    if prior and selected - prior[-1] > timedelta(days=10):
        return False, (
            "daily strict-prior history has a large gap before the selected row "
            f"({prior[-1].date()} to {selected.date()})"
        )
    return True, "daily strict-prior rows are chronological and adjacent enough for local evidence"


def _hourly_decision_fill_admissibility(
    selected_decision_timestamp: str,
    selected_fill_timestamp: str,
    decision_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
) -> tuple[bool, str]:
    selected_decision = _parse_z_timestamp(selected_decision_timestamp)
    selected_fill = _parse_z_timestamp(selected_fill_timestamp)
    decision_timestamps = [_parse_z_timestamp(row.get("completed_timestamp_utc", "")) for row in decision_rows]
    fill_timestamps = [_parse_z_timestamp(row.get("completed_timestamp_utc", "")) for row in fill_rows]
    if decision_timestamps[0] != selected_decision:
        return False, "first hourly decision row does not match selected decision timestamp"
    if fill_timestamps[0] != selected_fill:
        return False, "first hourly fill row does not match selected fill timestamp"
    if selected_fill - selected_decision != timedelta(hours=1):
        return False, "selected fill timestamp is not exactly one completed hour after decision timestamp"
    if decision_timestamps != sorted(decision_timestamps) or fill_timestamps != sorted(fill_timestamps):
        return False, "hourly decision/fill rows are not chronological"
    return True, "hourly decision/fill rows are chronological with selected one-hour fill lag"


def _level_bridge_summary(
    daily_continuous: dict[str, str],
    daily_current: dict[str, str],
    hourly_decision: dict[str, str],
    hourly_fill: dict[str, str],
) -> tuple[bool, str]:
    closes = (
        daily_continuous.get("close_price", ""),
        daily_current.get("close_price", ""),
        hourly_decision.get("close_price", ""),
        hourly_fill.get("close_price", ""),
    )
    if len(set(closes)) == 1:
        return True, "daily/hourly close prices share an identical declared level"
    return False, (
        "daily/hourly level bridge is not proved by identical closes or source-locked bridge proof: "
        f"daily_continuous={closes[0]}, daily_current={closes[1]}, "
        f"hourly_decision={closes[2]}, hourly_fill={closes[3]}"
    )


def _check(
    check_label: str,
    status: str,
    gate_label: str,
    summary: str,
    observed: object,
) -> RuntimeEvidenceGateCheck:
    check = RuntimeEvidenceGateCheck(
        check_label=check_label,
        status=status,
        gate_label=gate_label,
        summary=summary,
        observed_value_hash=_json_hash(observed),
    )
    check.validate()
    return check


def _runtime_evidence_bundle_hash(bundle: RuntimeEvidenceGateBundle) -> str:
    return _json_hash(
        {
            "status": bundle.status,
            "authorization": bundle.authorization,
            "strategy_id": bundle.strategy_id,
            "instrument": bundle.instrument,
            "lane": bundle.lane,
            "input_pack_path": bundle.input_pack_path,
            "manifest_hash": bundle.manifest_hash,
            "declared_file_hashes": bundle.declared_file_hashes,
            "selected_decision_timestamp_utc": bundle.selected_decision_timestamp_utc,
            "selected_fill_timestamp_utc": bundle.selected_fill_timestamp_utc,
            "selected_previous_daily_timestamp_utc": bundle.selected_previous_daily_timestamp_utc,
            "checks": tuple(check.__dict__ for check in bundle.checks),
            "fail_closed_gate_labels": bundle.fail_closed_gate_labels,
            "runtime_evidence_ready": bundle.runtime_evidence_ready,
            "forecast_rows_emitted": bundle.forecast_rows_emitted,
            "order_rows_emitted": bundle.order_rows_emitted,
            "fill_rows_emitted": bundle.fill_rows_emitted,
            "cost_rows_emitted": bundle.cost_rows_emitted,
            "pnl_rows_emitted": bundle.pnl_rows_emitted,
            "result_rows_emitted": bundle.result_rows_emitted,
            "non_authorizations": bundle.non_authorizations,
        }
    )


def _json_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(payload.encode("utf-8")).hexdigest()

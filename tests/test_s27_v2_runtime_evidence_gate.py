from __future__ import annotations

from dataclasses import replace
import csv
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.constants import (
    BLOCKED_COST_SCHEMA,
    BLOCKED_LEVEL_COMPATIBILITY,
    BLOCKED_RUNTIME_HISTORY,
    BLOCKED_SIGMA,
    BLOCKED_TICK,
    BLOCKED_WORKING_LIMIT_LIFECYCLE,
)
from carver.spine.s27_v2_replay.runtime_evidence_gate import (
    FAIL_CLOSED,
    PASS_COUNT_ONLY,
    PASS_LOCAL_BRIDGE_PROOF,
    PASS_LOCAL_DECLARED_ONLY,
    PASS_LOCAL_PREVALIDATED,
    REQUIRED_ROW_FAMILY_FILES,
    _runtime_evidence_bundle_hash,
    _json_hash,
    _remediation_source_evidence,
    build_runtime_evidence_gate,
)


PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_first_populated_dev_recon_znh2_20220103_multirow_declared_pack"
)
REMEDIATION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_runtime_evidence_recon_znm6_20260413_declared_pack"
)


def _checks_by_label(bundle):
    return {check.check_label: check for check in bundle.checks}


def _remediation_manifest_and_rows():
    manifest_path = REMEDIATION_PACK_PATH / "S27_V2_RUNTIME_EVIDENCE_REMEDIATION_DECLARED_INPUT_PACK_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows_by_file = {}
    for filename in REQUIRED_ROW_FAMILY_FILES:
        with (REMEDIATION_PACK_PATH / filename).open("r", encoding="utf-8", newline="") as handle:
            rows_by_file[filename] = list(csv.DictReader(handle))
    return manifest, rows_by_file


def test_runtime_evidence_gate_fails_closed_on_first_populated_pack():
    bundle = build_runtime_evidence_gate(PACK_PATH)
    checks = _checks_by_label(bundle)

    assert not bundle.runtime_evidence_ready
    assert not bundle.forecast_rows_emitted
    assert not bundle.order_rows_emitted
    assert not bundle.fill_rows_emitted
    assert not bundle.cost_rows_emitted
    assert not bundle.pnl_rows_emitted
    assert not bundle.result_rows_emitted

    assert checks["DECLARED_FILE_HASHES"].status == PASS_LOCAL_DECLARED_ONLY
    assert checks["SELECTED_ROW_AUTHORITY"].status == PASS_LOCAL_DECLARED_ONLY
    assert checks["HOURLY_DECISION_FILL_ADMISSIBILITY"].status == PASS_LOCAL_DECLARED_ONLY
    assert checks["EWMA5_EVIDENCE"].status == PASS_COUNT_ONLY
    assert checks["EWMAC_16_64_EVIDENCE"].status == PASS_COUNT_ONLY

    assert checks["STRICT_PRIOR_DAILY_ADMISSIBILITY"].status == FAIL_CLOSED
    assert "large gap" in checks["STRICT_PRIOR_DAILY_ADMISSIBILITY"].summary
    assert checks["STRATEGY3_SIGMA_EVIDENCE"].gate_label == BLOCKED_SIGMA
    assert checks["VQM_EVIDENCE"].gate_label == BLOCKED_RUNTIME_HISTORY
    assert "2020-12-21" in checks["VQM_EVIDENCE"].summary
    assert checks["DAILY_HOURLY_LEVEL_BRIDGE"].gate_label == BLOCKED_LEVEL_COMPATIBILITY
    assert "daily_continuous=132.53125" in checks["DAILY_HOURLY_LEVEL_BRIDGE"].summary
    assert checks["TICK_ROUNDING_POLICY"].gate_label == BLOCKED_TICK
    assert checks["MULTIPLIER_CURRENCY_POLICY"].gate_label == BLOCKED_COST_SCHEMA
    assert checks["COMMISSION_SPREAD_POLICY"].gate_label == BLOCKED_COST_SCHEMA
    assert checks["WORKING_ORDER_LIFECYCLE"].gate_label == BLOCKED_WORKING_LIMIT_LIFECYCLE


def test_runtime_evidence_gate_rejects_forged_ready_claim():
    bundle = build_runtime_evidence_gate(PACK_PATH)

    with pytest.raises(CarverBlocked, match="cannot claim runtime readiness"):
        replace(bundle, runtime_evidence_ready=True).validate()


def test_runtime_evidence_gate_rejects_downstream_emission_claim():
    bundle = build_runtime_evidence_gate(PACK_PATH)

    with pytest.raises(CarverBlocked, match="cannot emit downstream result surfaces"):
        replace(bundle, forecast_rows_emitted=True).validate()


def test_runtime_evidence_gate_rejects_content_hash_forgery():
    bundle = build_runtime_evidence_gate(PACK_PATH)
    forged_check = replace(
        bundle.checks[0],
        summary="forged pass summary",
    )
    forged = replace(
        bundle,
        checks=(forged_check, *bundle.checks[1:]),
    )

    with pytest.raises(CarverBlocked, match="bundle hash must bind gate contents"):
        forged.validate()


def test_runtime_evidence_gate_rejects_self_consistent_status_forgery():
    bundle = build_runtime_evidence_gate(PACK_PATH)
    checks = list(bundle.checks)
    vqm_index = next(
        index
        for index, check in enumerate(checks)
        if check.check_label == "VQM_EVIDENCE"
    )
    checks[vqm_index] = replace(
        checks[vqm_index],
        status=PASS_LOCAL_DECLARED_ONLY,
        gate_label="FORGED_VQM_PASS",
    )
    forged = replace(bundle, checks=tuple(checks))
    forged = replace(
        forged,
        bundle_hash=_runtime_evidence_bundle_hash(forged),
    )

    with pytest.raises(CarverBlocked, match="check status must bind locked gate semantics"):
        forged.validate()


def test_runtime_evidence_gate_rejects_self_consistent_fail_label_forgery():
    bundle = build_runtime_evidence_gate(PACK_PATH)
    forged = replace(
        bundle,
        fail_closed_gate_labels=("FORGED_SINGLE_FAIL_LABEL",),
    )
    forged = replace(
        forged,
        bundle_hash=_runtime_evidence_bundle_hash(forged),
    )

    with pytest.raises(CarverBlocked, match="fail-closed gates must bind failed checks exactly"):
        forged.validate()


def test_runtime_evidence_gate_rejects_self_consistent_check_gate_label_forgery():
    bundle = build_runtime_evidence_gate(PACK_PATH)
    checks = list(bundle.checks)
    sigma_index = next(
        index
        for index, check in enumerate(checks)
        if check.check_label == "STRATEGY3_SIGMA_EVIDENCE"
    )
    checks[sigma_index] = replace(
        checks[sigma_index],
        gate_label="FORGED_SIGMA_GATE",
    )
    forged = replace(
        bundle,
        checks=tuple(checks),
        fail_closed_gate_labels=tuple(
            dict.fromkeys(
                check.gate_label
                for check in checks
                if check.status == FAIL_CLOSED
            )
        ),
    )
    forged = replace(
        forged,
        bundle_hash=_runtime_evidence_bundle_hash(forged),
    )

    with pytest.raises(CarverBlocked, match="check gate label must bind locked gate semantics"):
        forged.validate()


def test_runtime_evidence_gate_rejects_out_of_scope_pack_path(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to authorized runtime evidence packs"):
        build_runtime_evidence_gate(tmp_path)


def test_runtime_evidence_remediation_gate_binds_local_prevalidated_sources():
    bundle = build_runtime_evidence_gate(REMEDIATION_PACK_PATH)
    checks = _checks_by_label(bundle)

    assert bundle.selected_decision_timestamp_utc == "2026-04-13T03:00:00Z"
    assert bundle.selected_fill_timestamp_utc == "2026-04-13T04:00:00Z"
    assert bundle.selected_previous_daily_timestamp_utc == "2026-04-12T00:00:00Z"
    assert not bundle.runtime_evidence_ready
    assert not bundle.forecast_rows_emitted
    assert not bundle.order_rows_emitted
    assert not bundle.fill_rows_emitted
    assert not bundle.cost_rows_emitted
    assert not bundle.pnl_rows_emitted
    assert not bundle.result_rows_emitted

    assert checks["DECLARED_FILE_HASHES"].status == PASS_LOCAL_DECLARED_ONLY
    assert checks["SELECTED_ROW_AUTHORITY"].status == PASS_LOCAL_DECLARED_ONLY
    assert checks["STRICT_PRIOR_DAILY_ADMISSIBILITY"].status == PASS_LOCAL_DECLARED_ONLY
    assert checks["HOURLY_DECISION_FILL_ADMISSIBILITY"].status == PASS_LOCAL_DECLARED_ONLY
    assert checks["EWMA5_EVIDENCE"].status == PASS_COUNT_ONLY
    assert checks["EWMAC_16_64_EVIDENCE"].status == PASS_LOCAL_PREVALIDATED
    assert checks["STRATEGY3_SIGMA_EVIDENCE"].status == PASS_LOCAL_PREVALIDATED
    assert checks["VQM_EVIDENCE"].status == PASS_LOCAL_PREVALIDATED
    assert checks["DAILY_HOURLY_LEVEL_BRIDGE"].status == PASS_LOCAL_BRIDGE_PROOF

    assert "135 named strict-prior daily rows" in checks["EWMAC_16_64_EVIDENCE"].summary
    assert "selected previous daily sigma" in checks["STRATEGY3_SIGMA_EVIDENCE"].summary
    assert "V, Q, M" in checks["VQM_EVIDENCE"].summary
    assert "not price equality" in checks["DAILY_HOURLY_LEVEL_BRIDGE"].summary

    assert checks["TICK_ROUNDING_POLICY"].gate_label == BLOCKED_TICK
    assert checks["MULTIPLIER_CURRENCY_POLICY"].gate_label == BLOCKED_COST_SCHEMA
    assert checks["COMMISSION_SPREAD_POLICY"].gate_label == BLOCKED_COST_SCHEMA
    assert checks["WORKING_ORDER_LIFECYCLE"].gate_label == BLOCKED_WORKING_LIMIT_LIFECYCLE


def test_runtime_evidence_remediation_gate_rejects_self_consistent_vqm_downgrade():
    bundle = build_runtime_evidence_gate(REMEDIATION_PACK_PATH)
    checks = list(bundle.checks)
    vqm_index = next(
        index
        for index, check in enumerate(checks)
        if check.check_label == "VQM_EVIDENCE"
    )
    checks[vqm_index] = replace(
        checks[vqm_index],
        status=FAIL_CLOSED,
        gate_label=BLOCKED_RUNTIME_HISTORY,
    )
    forged = replace(
        bundle,
        checks=tuple(checks),
        fail_closed_gate_labels=tuple(
            dict.fromkeys(
                check.gate_label
                for check in checks
                if check.status == FAIL_CLOSED
            )
        ),
    )
    forged = replace(forged, bundle_hash=_runtime_evidence_bundle_hash(forged))

    with pytest.raises(CarverBlocked, match="check status must bind locked gate semantics"):
        forged.validate()


def test_runtime_evidence_remediation_gate_rejects_ready_claim():
    bundle = build_runtime_evidence_gate(REMEDIATION_PACK_PATH)

    with pytest.raises(CarverBlocked, match="cannot claim runtime readiness"):
        replace(bundle, runtime_evidence_ready=True).validate()


def test_runtime_evidence_remediation_source_verifier_rejects_manifest_source_hash_forgery():
    manifest, rows_by_file = _remediation_manifest_and_rows()
    manifest["source_files"]["vqm_daily_ledger"]["sha256"] = "0" * 64

    with pytest.raises(CarverBlocked, match="source hash must match local bytes"):
        _remediation_source_evidence(
            manifest,
            rows_by_file,
        )


def test_runtime_evidence_remediation_source_verifier_rejects_level_bridge_hash_forgery():
    manifest, rows_by_file = _remediation_manifest_and_rows()
    manifest["history_evidence"]["level_bridge_proof_hash"] = "0" * 64

    with pytest.raises(CarverBlocked, match="level bridge proof hash must bind manifest proof"):
        _remediation_source_evidence(
            manifest,
            rows_by_file,
        )


def test_runtime_evidence_remediation_gate_rejects_self_consistent_summary_observed_hash_mutation():
    bundle = build_runtime_evidence_gate(REMEDIATION_PACK_PATH)
    checks = list(bundle.checks)
    sigma_index = next(
        index
        for index, check in enumerate(checks)
        if check.check_label == "STRATEGY3_SIGMA_EVIDENCE"
    )
    checks[sigma_index] = replace(
        checks[sigma_index],
        summary="forged but self-consistent sigma summary",
        observed_value_hash=_json_hash(("forged", "sigma", "payload")),
    )
    forged = replace(bundle, checks=tuple(checks))
    forged = replace(forged, bundle_hash=_runtime_evidence_bundle_hash(forged))

    with pytest.raises(CarverBlocked, match="must match active local pack evidence"):
        forged.validate()

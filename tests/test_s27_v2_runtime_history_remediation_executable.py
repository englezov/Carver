from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.constants import (
    BLOCKED_COST_SCHEMA,
    BLOCKED_TICK,
    BLOCKED_WORKING_LIMIT_LIFECYCLE,
)
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.runtime_evidence_gate import (
    _runtime_evidence_bundle_hash,
    build_runtime_evidence_gate,
)
from carver.spine.s27_v2_replay.runtime_history_executable import (
    RUNTIME_HISTORY_LEVEL_BRIDGE_PASS_STATUS,
    RUNTIME_HISTORY_READY_STATUS,
    S27_V2_RUNTIME_HISTORY_EXECUTABLE_AUTHORIZATION,
    S27_V2_RUNTIME_HISTORY_EXECUTABLE_STATUS,
    _bundle_hash_payload,
    _level_row_hash_payload,
    _runtime_row_hash_payload,
    build_runtime_history_executable_ledgers_on_remediation_pack,
)


REMEDIATION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_runtime_evidence_recon_znm6_20260413_declared_pack"
)


def test_runtime_history_remediation_executable_builds_non_result_rows():
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)

    assert bundle.status == S27_V2_RUNTIME_HISTORY_EXECUTABLE_STATUS
    assert bundle.authorization_label == S27_V2_RUNTIME_HISTORY_EXECUTABLE_AUTHORIZATION
    assert bundle.level_compatibility_row.row_status == RUNTIME_HISTORY_LEVEL_BRIDGE_PASS_STATUS
    assert bundle.level_compatibility_row.reason_code == "LOCAL_LEVEL_SPACE_BRIDGE_PROOF_BOUND_NOT_PRICE_EQUALITY"
    assert bundle.level_compatibility_row.level_bridge_proof_hash == (
        "b27d940dc13152a0b753ccf51ec61f60473a29f1d097e9ab5c2b055562dc64c7"
    )
    assert bundle.runtime_history_row.row_status == RUNTIME_HISTORY_READY_STATUS
    assert bundle.runtime_history_row.observed_daily_continuous_rows == 135
    assert bundle.runtime_history_row.required_minimum_daily_continuous_rows == 64
    assert bundle.runtime_history_row.runtime_numeric_values_emitted is False
    assert bundle.unresolved_gate_labels == (
        BLOCKED_TICK,
        BLOCKED_COST_SCHEMA,
        BLOCKED_WORKING_LIMIT_LIFECYCLE,
    )
    assert not bundle.forecast_rows_emitted
    assert not bundle.order_rows_emitted
    assert not bundle.fill_rows_emitted
    assert not bundle.cost_rows_emitted
    assert not bundle.pnl_rows_emitted
    assert not bundle.result_scored_run_emitted
    assert not bundle.source_faithful_evidence_claimed


def test_runtime_history_remediation_executable_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_runtime_history_executable_ledgers_on_remediation_pack(tmp_path)


def test_runtime_history_remediation_executable_rejects_forged_evidence_bundle():
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    evidence = bundle.runtime_evidence_bundle
    forged_evidence = replace(evidence, manifest_hash="0" * 64)
    forged_evidence = replace(forged_evidence, bundle_hash=_runtime_evidence_bundle_hash(forged_evidence))
    forged = replace(bundle, runtime_evidence_bundle=forged_evidence)
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must match active local pack evidence"):
        forged.validate()


def test_runtime_history_remediation_executable_rejects_forged_level_proof_hash():
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    level_row = replace(bundle.level_compatibility_row, level_bridge_proof_hash="0" * 64)
    level_row = replace(level_row, row_hash=canonical_sha256(_level_row_hash_payload(level_row)))
    forged = replace(bundle, level_compatibility_row=level_row)
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="level row must bind active bridge proof"):
        forged.validate()


def test_runtime_history_remediation_executable_rejects_runtime_numeric_emission():
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    runtime_row = replace(bundle.runtime_history_row, runtime_numeric_values_emitted=True)
    runtime_row = replace(runtime_row, row_hash=canonical_sha256(_runtime_row_hash_payload(runtime_row)))
    forged = replace(bundle, runtime_history_row=runtime_row)
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit runtime numeric values"):
        forged.validate()


@pytest.mark.parametrize(
    "field_name",
    (
        "daily_continuous_row_hash",
        "daily_current_contract_row_hash",
        "hourly_decision_row_hash",
        "hourly_fill_row_hash",
    ),
)
def test_runtime_history_remediation_executable_rejects_self_consistent_level_row_hash_forgery(field_name):
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    level_row = replace(bundle.level_compatibility_row, **{field_name: "0" * 64})
    level_row = replace(level_row, row_hash=canonical_sha256(_level_row_hash_payload(level_row)))
    runtime_row = replace(bundle.runtime_history_row, level_compatibility_row_hash=level_row.row_hash)
    runtime_row = replace(runtime_row, row_hash=canonical_sha256(_runtime_row_hash_payload(runtime_row)))
    forged = replace(bundle, level_compatibility_row=level_row, runtime_history_row=runtime_row)
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="level row must match active pack rows"):
        forged.validate()


@pytest.mark.parametrize(
    "field_name",
    (
        "daily_continuous_close_price",
        "daily_current_contract_close_price",
        "hourly_decision_close_price",
        "hourly_fill_close_price",
    ),
)
def test_runtime_history_remediation_executable_rejects_self_consistent_level_close_forgery(field_name):
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    level_row = replace(bundle.level_compatibility_row, **{field_name: "999.0"})
    level_row = replace(level_row, row_hash=canonical_sha256(_level_row_hash_payload(level_row)))
    runtime_row = replace(bundle.runtime_history_row, level_compatibility_row_hash=level_row.row_hash)
    runtime_row = replace(runtime_row, row_hash=canonical_sha256(_runtime_row_hash_payload(runtime_row)))
    forged = replace(bundle, level_compatibility_row=level_row, runtime_history_row=runtime_row)
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="level row must match active pack rows"):
        forged.validate()


def test_runtime_history_remediation_executable_rejects_self_consistent_runtime_check_hash_forgery():
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    runtime_row = replace(bundle.runtime_history_row, vqm_check_hash="0" * 64)
    runtime_row = replace(runtime_row, row_hash=canonical_sha256(_runtime_row_hash_payload(runtime_row)))
    forged = replace(bundle, runtime_history_row=runtime_row)
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="runtime row must match active evidence and pack rows"):
        forged.validate()


def test_runtime_history_remediation_executable_rejects_self_consistent_runtime_row_hash_forgery():
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    daily_hashes = ("0" * 64, *bundle.runtime_history_row.daily_continuous_row_hashes[1:])
    runtime_row = replace(
        bundle.runtime_history_row,
        daily_continuous_row_hashes=daily_hashes,
    )
    runtime_row = replace(runtime_row, row_hash=canonical_sha256(_runtime_row_hash_payload(runtime_row)))
    forged = replace(bundle, runtime_history_row=runtime_row)
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="runtime row must match active evidence and pack rows"):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "forecast_rows_emitted",
        "order_rows_emitted",
        "fill_rows_emitted",
        "cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_runtime_history_remediation_executable_rejects_downstream_result_emission(flag_name):
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit downstream result surfaces"):
        forged.validate()


def test_runtime_history_remediation_executable_rejects_policy_gate_removal():
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    forged = replace(bundle, unresolved_gate_labels=(BLOCKED_TICK,))
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="unresolved gates must preserve blocked policies"):
        forged.validate()


def test_runtime_history_remediation_executable_binds_active_runtime_evidence_check_hashes():
    bundle = build_runtime_history_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    evidence = build_runtime_evidence_gate(REMEDIATION_PACK_PATH)
    checks = {check.check_label: check for check in evidence.checks}

    assert bundle.runtime_history_row.strict_prior_daily_check_hash == (
        checks["STRICT_PRIOR_DAILY_ADMISSIBILITY"].observed_value_hash
    )
    assert bundle.runtime_history_row.ewmac_16_64_check_hash == checks["EWMAC_16_64_EVIDENCE"].observed_value_hash
    assert bundle.runtime_history_row.strategy3_sigma_check_hash == (
        checks["STRATEGY3_SIGMA_EVIDENCE"].observed_value_hash
    )
    assert bundle.runtime_history_row.vqm_check_hash == checks["VQM_EVIDENCE"].observed_value_hash

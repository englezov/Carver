from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.forecast_executable import (
    _forecast_bundle_hash_payload,
    build_forecast_executable_ledgers_on_remediation_pack,
)
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.position_evidence_gate import (
    POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
    POSITION_EVIDENCE_CHECK_STATUS_PASS,
    POSITION_EVIDENCE_GATE_BY_LABEL,
    POSITION_EVIDENCE_LABELS,
    S27_V2_POSITION_EVIDENCE_AUTHORIZATION,
    S27_V2_POSITION_EVIDENCE_STATUS,
    _position_evidence_bundle_hash_payload,
    _position_evidence_check_hash_payload,
    build_position_evidence_fail_closed_gate,
)


REMEDIATION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_runtime_evidence_recon_znm6_20260413_declared_pack"
)


def test_position_evidence_gate_builds_forecast_pass_and_position_fail_closed_checks():
    bundle = build_position_evidence_fail_closed_gate(REMEDIATION_PACK_PATH)

    assert bundle.status == S27_V2_POSITION_EVIDENCE_STATUS
    assert bundle.authorization_label == S27_V2_POSITION_EVIDENCE_AUTHORIZATION
    assert bundle.forecast_authority_accepted is True
    assert bundle.position_evidence_ready is False
    assert bundle.desired_position_rows_emitted is False
    assert bundle.order_rows_emitted is False
    assert bundle.fill_rows_emitted is False
    assert bundle.cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert tuple(check.evidence_label for check in bundle.evidence_checks) == POSITION_EVIDENCE_LABELS
    assert bundle.evidence_checks[0].evidence_label == "FORECAST_AUTHORITY"
    assert bundle.evidence_checks[0].evidence_status == POSITION_EVIDENCE_CHECK_STATUS_PASS
    assert bundle.evidence_checks[0].observed_value_hash == bundle.forecast_bundle.forecast_row.row_hash
    for check in bundle.evidence_checks[1:]:
        assert check.evidence_status == POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED
        assert check.gate_label == POSITION_EVIDENCE_GATE_BY_LABEL[check.evidence_label]
    assert bundle.fail_closed_gate_labels == tuple(
        POSITION_EVIDENCE_GATE_BY_LABEL[label]
        for label in POSITION_EVIDENCE_LABELS
        if label != "FORECAST_AUTHORITY"
    )


def test_position_evidence_gate_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_position_evidence_fail_closed_gate(tmp_path)


def test_position_evidence_gate_rejects_forged_forecast_bundle_even_with_recomputed_hashes():
    bundle = build_position_evidence_fail_closed_gate(REMEDIATION_PACK_PATH)
    forecast = replace(bundle.forecast_bundle, source_faithful_evidence_claimed=True)
    forecast = replace(forecast, bundle_hash=canonical_sha256(_forecast_bundle_hash_payload(forecast)))
    forged = replace(bundle, forecast_bundle=forecast)
    forged = replace(forged, bundle_hash=canonical_sha256(_position_evidence_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit position/order/fill/cost/PnL/result/evidence"):
        forged.validate()


@pytest.mark.parametrize(
    "label",
    (
        "FORECAST_TO_POSITION_DIVISOR",
        "BASE_POSITION",
        "CAPITAL_ACCOUNT_VALUE",
        "RISK_TARGET",
        "MULTIPLIER_CURRENCY",
        "ROUNDING_POLICY",
        "INITIAL_CURRENT_POSITION_CONTEXT",
    ),
)
def test_position_evidence_gate_rejects_self_consistent_unresolved_check_promoted_to_pass(label):
    bundle = build_position_evidence_fail_closed_gate(REMEDIATION_PACK_PATH)
    checks = list(bundle.evidence_checks)
    index = POSITION_EVIDENCE_LABELS.index(label)
    checks[index] = replace(
        checks[index],
        evidence_status=POSITION_EVIDENCE_CHECK_STATUS_PASS,
        gate_label="PASS_FORGED_POSITION_EVIDENCE",
    )
    checks[index] = replace(
        checks[index],
        check_hash=canonical_sha256(_position_evidence_check_hash_payload(checks[index])),
    )
    forged = replace(bundle, evidence_checks=tuple(checks))
    forged = replace(forged, bundle_hash=canonical_sha256(_position_evidence_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "field_name",
    (
        "summary",
        "observed_value_hash",
        "upstream_forecast_bundle_hash",
    ),
)
def test_position_evidence_gate_rejects_self_consistent_check_content_mutation(field_name):
    bundle = build_position_evidence_fail_closed_gate(REMEDIATION_PACK_PATH)
    checks = list(bundle.evidence_checks)
    replacement = "0" * 64 if field_name.endswith("hash") else "forged but internally hashed summary"
    checks[0] = replace(checks[0], **{field_name: replacement})
    checks[0] = replace(
        checks[0],
        check_hash=canonical_sha256(_position_evidence_check_hash_payload(checks[0])),
    )
    forged = replace(bundle, evidence_checks=tuple(checks))
    forged = replace(forged, bundle_hash=canonical_sha256(_position_evidence_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "position_evidence_ready",
        "desired_position_rows_emitted",
        "order_rows_emitted",
        "fill_rows_emitted",
        "cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_position_evidence_gate_rejects_readiness_or_downstream_emission_flags(flag_name):
    bundle = build_position_evidence_fail_closed_gate(REMEDIATION_PACK_PATH)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_position_evidence_bundle_hash_payload(forged)))

    if flag_name == "position_evidence_ready":
        expected = "cannot be ready"
    else:
        expected = "cannot emit desired-position/order/fill/cost/PnL/result/evidence"
    with pytest.raises(CarverBlocked, match=expected):
        forged.validate()


def test_position_evidence_gate_rejects_missing_forecast_authority_acceptance():
    bundle = build_position_evidence_fail_closed_gate(REMEDIATION_PACK_PATH)
    forged = replace(bundle, forecast_authority_accepted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_position_evidence_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must accept active forecast authority"):
        forged.validate()


def test_position_evidence_gate_rejects_fail_closed_gate_drift():
    bundle = build_position_evidence_fail_closed_gate(REMEDIATION_PACK_PATH)
    forged = replace(bundle, fail_closed_gate_labels=bundle.fail_closed_gate_labels[:-1])
    forged = replace(forged, bundle_hash=canonical_sha256(_position_evidence_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="fail-closed gates must remain unresolved"):
        forged.validate()

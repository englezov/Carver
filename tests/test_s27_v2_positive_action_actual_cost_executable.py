from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.positive_action_actual_cost_executable as actual_cost_module
from carver.spine.s27_v2_replay.positive_action_actual_cost_executable import (
    ACCEPTED_COMMISSION_PER_CONTRACT,
    ACCEPTED_COMMISSION_UNIT,
    ACCEPTED_COST_CLASSIFICATION,
    ACCEPTED_COST_DECISION_BLOCK_SHA256,
    ACCEPTED_COST_POLICY_LABEL,
    ACTUAL_COST_NON_AUTHORIZATIONS,
    BACKTEST_STATUS,
    NO_SPREAD_COST_REASON,
    PNL_LEDGER_STATUS,
    REJECTED_COST_CLASSIFICATION,
    RESULT_STATUS,
    S27_V2_POSITIVE_ACTION_ACTUAL_COST_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_ACTUAL_COST_STATUS,
    VALUATION_FAIL_CLOSED_DECISION_BLOCK_SHA256,
    _actual_cost_bundle_hash_payload,
    _actual_cost_row_hash_payload,
    _accepted_cost_policy_hash,
    build_positive_action_actual_cost_executable,
)
from carver.spine.s27_v2_replay.positive_action_fill_executable import _fill_bundle_hash_payload


POSITIVE_ACTION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_positive_action_recon_znm6_20260413T13_declared_pack"
)


@pytest.fixture(scope="module")
def active_actual_cost_bundle():
    return build_positive_action_actual_cost_executable(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_actual_cost_builds_limit_fill_commission_only_cost(active_actual_cost_bundle):
    bundle = active_actual_cost_bundle
    row = bundle.actual_cost_row

    assert bundle.status == S27_V2_POSITIVE_ACTION_ACTUAL_COST_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_ACTUAL_COST_AUTHORIZATION
    assert row.raw_symbol == "ZNM6"
    assert row.selected_fill_timestamp_utc == "2026-04-13T14:00:00Z"
    assert row.fill_price == pytest.approx(111.046875)
    assert row.fill_quantity == 1
    assert row.accepted_cost_policy_label == ACCEPTED_COST_POLICY_LABEL
    assert row.accepted_cost_policy_hash == _accepted_cost_policy_hash()
    assert row.accepted_cost_decision_block_sha256 == ACCEPTED_COST_DECISION_BLOCK_SHA256
    assert row.cost_classification == ACCEPTED_COST_CLASSIFICATION
    assert row.rejected_cost_classification == REJECTED_COST_CLASSIFICATION
    assert row.commission_per_contract == pytest.approx(ACCEPTED_COMMISSION_PER_CONTRACT)
    assert row.commission_unit == ACCEPTED_COMMISSION_UNIT
    assert row.commission_amount == pytest.approx(2.30)
    assert row.spread_cost_amount == pytest.approx(0.0)
    assert row.spread_cost_reason == NO_SPREAD_COST_REASON
    assert row.total_cost_amount == pytest.approx(2.30)
    assert row.total_cost_currency == "USD"
    assert row.valuation_fail_closed_decision_block_sha256 == VALUATION_FAIL_CLOSED_DECISION_BLOCK_SHA256
    assert row.pnl_ledger_status == PNL_LEDGER_STATUS
    assert row.result_status == RESULT_STATUS
    assert row.backtest_status == BACKTEST_STATUS
    assert row.pnl_rows_emitted is False
    assert row.result_rows_emitted is False
    assert row.result_scored_run_emitted is False
    assert row.source_faithful_evidence_claimed is False

    assert bundle.actual_commission_rows_emitted is True
    assert bundle.actual_spread_cost_rows_emitted is False
    assert bundle.actual_cost_rows_emitted is True
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.non_authorizations == ACTUAL_COST_NON_AUTHORIZATIONS


def test_positive_action_actual_cost_row_is_not_standalone_authority(active_actual_cost_bundle):
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        active_actual_cost_bundle.actual_cost_row.validate()


def test_positive_action_actual_cost_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared positive-action pack"):
        build_positive_action_actual_cost_executable(tmp_path)


def test_positive_action_actual_cost_rejects_forged_fill_bundle(active_actual_cost_bundle):
    fill_bundle = replace(active_actual_cost_bundle.fill_bundle, source_faithful_evidence_claimed=True)
    fill_bundle = replace(fill_bundle, bundle_hash=canonical_sha256(_fill_bundle_hash_payload(fill_bundle)))
    forged = replace(active_actual_cost_bundle, fill_bundle=fill_bundle)
    forged = replace(forged, bundle_hash=canonical_sha256(_actual_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("fill_quantity", 2),
        ("cost_parameter_file_hash", "a" * 64),
        ("cost_parameter_row_hash", "b" * 64),
        ("accepted_cost_policy_label", "PROP_FIRM_FREE_COMMISSION"),
        ("accepted_cost_policy_hash", "c" * 64),
        ("accepted_cost_decision_record_hash", "d" * 64),
        ("accepted_cost_decision_block_sha256", "e" * 64),
        ("cost_classification", "PROP_FIRM_EVALUATION_COSTS"),
        ("rejected_cost_classification", "CFD_ADAPTER_COSTS"),
        ("commission_per_contract", 0.0),
        ("commission_unit", "USD_PER_ROUND_TURN"),
        ("commission_amount", 0.0),
        ("spread_cost_amount", 0.25),
        ("spread_cost_reason", "MARKET_SPREAD_FROM_ADAPTER"),
        ("total_cost_amount", 0.25),
        ("total_cost_currency", "EUR"),
        ("source_cost_treatment_label", "FORGED_NO_COMMISSION_FOR_LIMIT"),
        ("limit_fill_cost_treatment_label", "FORGED_MARKET_SPREAD_ON_LIMIT"),
        ("prop_cfd_adapter_cost_rejection_label", "ALLOW_PROP_FIRM_COSTS"),
        ("valuation_fail_closed_decision_block_sha256", "f" * 64),
        ("pnl_ledger_status", "PASS_PNL_READY"),
        ("result_status", "PASS_RESULT_READY"),
        ("backtest_status", "PASS_BACKTEST_READY"),
        ("pnl_rows_emitted", True),
        ("result_rows_emitted", True),
        ("result_scored_run_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_positive_action_actual_cost_rejects_self_consistent_cost_row_forgery(
    active_actual_cost_bundle,
    field_name,
    forged_value,
):
    row = replace(active_actual_cost_bundle.actual_cost_row, **{field_name: forged_value})
    row = replace(row, row_hash=canonical_sha256(_actual_cost_row_hash_payload(row)))
    forged = replace(active_actual_cost_bundle, actual_cost_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_actual_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("flag_name", "forged_value"),
    (
        ("actual_commission_rows_emitted", False),
        ("actual_cost_rows_emitted", False),
        ("validation_metadata_rows_emitted", False),
        ("provenance_metadata_rows_emitted", False),
        ("trusted_bundle_metadata_emitted", False),
        ("actual_spread_cost_rows_emitted", True),
        ("pnl_rows_emitted", True),
        ("result_rows_emitted", True),
        ("result_scored_run_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_positive_action_actual_cost_rejects_forbidden_bundle_flag_forgery(
    active_actual_cost_bundle,
    flag_name,
    forged_value,
):
    forged = replace(active_actual_cost_bundle, **{flag_name: forged_value})
    forged = replace(forged, bundle_hash=canonical_sha256(_actual_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_positive_action_actual_cost_rejects_unpinned_acceptance_record(monkeypatch):
    monkeypatch.setattr(actual_cost_module, "_EXPECTED_ACCEPTANCE_RECORD_SHA256", "0" * 64)

    with pytest.raises(CarverBlocked, match="acceptance record hash is not pinned"):
        build_positive_action_actual_cost_executable(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_actual_cost_is_not_package_root_exported():
    assert "build_positive_action_actual_cost_executable" not in getattr(package_root, "__all__", ())
    assert not hasattr(package_root, "build_positive_action_actual_cost_executable")

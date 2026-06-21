from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.positive_action_cost_executable as cost_module
from carver.spine.s27_v2_replay.positive_action_cost_executable import (
    ACTUAL_COST_LEDGER_STATUS,
    COST_EVIDENCE_ROW_STATUS,
    COST_NON_AUTHORIZATIONS,
    INFERRED_RETAIL_COST_STATUS,
    LIMIT_FILL_COST_TREATMENT_LABEL,
    NO_SPREAD_COST_REASON,
    NUMERIC_COST_POLICY_STATUS,
    PROP_CFD_ADAPTER_COST_REJECTION_LABEL,
    S27_V2_POSITIVE_ACTION_COST_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_COST_STATUS,
    SOURCE_COST_TREATMENT_LABEL,
    _cost_bundle_hash_payload,
    _cost_evidence_row_hash_payload,
    _policy_hash,
    build_positive_action_cost_executable,
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
def active_cost_bundle():
    return build_positive_action_cost_executable(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_cost_builds_fail_closed_cost_evidence(active_cost_bundle):
    bundle = active_cost_bundle
    row = bundle.cost_evidence_row

    assert bundle.status == S27_V2_POSITIVE_ACTION_COST_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_COST_AUTHORIZATION
    assert row.row_status == COST_EVIDENCE_ROW_STATUS
    assert row.raw_symbol == "ZNM6"
    assert row.selected_fill_timestamp_utc == "2026-04-13T14:00:00Z"
    assert row.fill_quantity == 1
    assert row.fill_price == pytest.approx(111.046875)
    assert row.cost_parameter_file_hash == "e6b7c69a712fd7a5effbabbd4c809f24c1a6dfabbfb1ce317b387c923ac7f098"
    assert row.cost_parameter_readiness_status == "READY_COST_PARAMETER_HASHES_LOCAL_ONLY_FAIL_CLOSED_FOR_EXECUTION"
    assert row.source_cost_treatment_label == SOURCE_COST_TREATMENT_LABEL
    assert row.limit_fill_cost_treatment_label == LIMIT_FILL_COST_TREATMENT_LABEL
    assert row.numeric_cost_policy_status == NUMERIC_COST_POLICY_STATUS
    assert row.inferred_retail_cost_status == INFERRED_RETAIL_COST_STATUS
    assert row.prop_cfd_adapter_cost_rejection_label == PROP_CFD_ADAPTER_COST_REJECTION_LABEL
    assert row.cost_accounting_required_by_source is True
    assert row.actual_commission_rows_emitted is False
    assert row.actual_spread_cost_rows_emitted is False
    assert row.actual_cost_rows_emitted is False
    assert row.actual_cost_ledger_status == ACTUAL_COST_LEDGER_STATUS
    assert row.commission_amount == 0.0
    assert row.spread_cost_amount == 0.0
    assert row.total_cost_amount == 0.0
    assert row.total_cost_currency == "NOT_APPLICABLE"
    assert row.no_spread_cost_reason == NO_SPREAD_COST_REASON

    assert bundle.cost_evidence_metadata_rows_emitted is True
    assert bundle.actual_commission_rows_emitted is False
    assert bundle.actual_spread_cost_rows_emitted is False
    assert bundle.actual_cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.non_authorizations == COST_NON_AUTHORIZATIONS


def test_positive_action_cost_row_is_not_standalone_authority(active_cost_bundle):
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        active_cost_bundle.cost_evidence_row.validate()


def test_positive_action_cost_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared positive-action pack"):
        build_positive_action_cost_executable(tmp_path)


def test_positive_action_cost_rejects_forged_fill_bundle(active_cost_bundle):
    fill_bundle = replace(active_cost_bundle.fill_bundle, source_faithful_evidence_claimed=True)
    fill_bundle = replace(fill_bundle, bundle_hash=canonical_sha256(_fill_bundle_hash_payload(fill_bundle)))
    forged = replace(active_cost_bundle, fill_bundle=fill_bundle)
    forged = replace(forged, bundle_hash=canonical_sha256(_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("commission_policy_hash", "a" * 64),
        ("spread_policy_hash", "b" * 64),
        ("contract_multiplier_value_hash", "c" * 64),
        ("currency_policy_hash", "d" * 64),
        ("cost_parameter_readiness_status", "PASS_FORGED_COST_READY"),
        ("source_cost_treatment_label", "FORGED_NO_COMMISSION"),
        ("limit_fill_cost_treatment_label", "FORGED_SPREAD_COST_ON_LIMIT"),
        ("numeric_cost_policy_status", "PASS_FORGED_NUMERIC_COST"),
        ("inferred_retail_cost_status", "PASS_FORGED_INFERRED_RETAIL_COST"),
        ("prop_cfd_adapter_cost_rejection_label", "ALLOW_PROP_FIRM_COSTS"),
        ("cost_accounting_required_by_source", False),
        ("actual_commission_rows_emitted", True),
        ("actual_spread_cost_rows_emitted", True),
        ("actual_cost_rows_emitted", True),
        ("actual_cost_ledger_status", "PASS_FORGED_COST_LEDGER"),
        ("commission_amount", 1.25),
        ("spread_cost_amount", 15.625),
        ("total_cost_amount", 16.875),
        ("total_cost_currency", "USD"),
        ("no_spread_cost_reason", "FORGED_MARKET_SPREAD_ON_LIMIT_FILL"),
    ),
)
def test_positive_action_cost_rejects_self_consistent_cost_row_forgery(
    active_cost_bundle,
    field_name,
    forged_value,
):
    row = replace(active_cost_bundle.cost_evidence_row, **{field_name: forged_value})
    row = replace(
        row,
        source_cost_treatment_hash=_policy_hash(
            "source_cost_treatment",
            row.source_cost_treatment_label,
            "COMMISSION_FOR_ALL_ORDERS",
            row.commission_policy_hash,
        ),
        limit_fill_cost_treatment_hash=_policy_hash(
            "limit_fill_cost_treatment",
            row.limit_fill_cost_treatment_label,
            "COMMISSION_ONLY",
            row.spread_policy_hash,
            row.limit_fill_row_hash,
        ),
        prop_cfd_adapter_cost_rejection_hash=_policy_hash(
            "cost_rejection",
            row.prop_cfd_adapter_cost_rejection_label,
            "NO_PROP_FIRM_FEES",
            "NO_CFD_SPREADS_OR_SWAPS",
            "NO_ADAPTER_OR_PERSONAL_TRADING_COSTS",
        ),
    )
    row = replace(row, row_hash=canonical_sha256(_cost_evidence_row_hash_payload(row)))
    forged = replace(active_cost_bundle, cost_evidence_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "actual_commission_rows_emitted",
        "actual_spread_cost_rows_emitted",
        "actual_cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_positive_action_cost_rejects_forbidden_downstream_flags(active_cost_bundle, flag_name):
    forged = replace(active_cost_bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit cost/PnL/result/evidence"):
        forged.validate()


def test_positive_action_cost_requires_metadata_emission_flag(active_cost_bundle):
    forged = replace(active_cost_bundle, cost_evidence_metadata_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must emit only authorized metadata"):
        forged.validate()


def test_positive_action_cost_rejects_mutated_cost_parameter_readiness(monkeypatch):
    active_row = dict(cost_module._locked_cost_parameter_row(POSITIVE_ACTION_PACK_PATH))
    active_row["readiness_status"] = "PASS_FORGED_NUMERIC_COST_READY"
    monkeypatch.setattr(cost_module, "_locked_cost_parameter_row", lambda _pack_path: active_row)

    with pytest.raises(CarverBlocked, match="readiness must remain fail-closed"):
        build_positive_action_cost_executable(POSITIVE_ACTION_PACK_PATH)

from __future__ import annotations

from dataclasses import replace
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.positive_action_executable as positive
from carver.spine.s27_v2_replay.positive_action_executable import (
    EXPECTED_SELECTED_DECISION,
    EXPECTED_SELECTED_FILL,
    FAIL_CLOSED_ACTUAL_COST,
    FAIL_CLOSED_ACTUAL_FILL,
    FAIL_CLOSED_ACTUAL_PNL,
    FAIL_CLOSED_EXECUTION_UNRESOLVED,
    PASS_POSITIVE_DESIRED_POSITION,
    POSITIVE_ACTION_ROW_STATUS,
    S27_V2_POSITIVE_ACTION_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_STATUS,
    _positive_action_bundle_hash_payload,
    _positive_action_row_hash_payload,
    _round_half_away_from_zero,
    build_positive_action_executable_replay,
)


POSITIVE_ACTION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_positive_action_recon_znm6_20260413T13_declared_pack"
)


def test_positive_action_executable_builds_first_nonzero_order_intent_metadata():
    bundle = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)
    row = bundle.positive_action_row

    assert bundle.status == S27_V2_POSITIVE_ACTION_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_AUTHORIZATION
    assert row.row_status == POSITIVE_ACTION_ROW_STATUS
    assert row.selected_decision_timestamp_utc == EXPECTED_SELECTED_DECISION
    assert row.selected_fill_timestamp_utc == EXPECTED_SELECTED_FILL
    assert row.raw_symbol == "ZNM6"
    assert row.trend_veto_decision == "PERMIT_MEAN_REVERSION"
    assert row.capped_forecast_value == pytest.approx(-0.35105404856990824)
    assert row.desired_unrounded_contracts == pytest.approx(-0.5016120637629121)
    assert row.desired_rounded_position == -1
    assert row.current_position_before_order == 0
    assert row.position_change_contracts == -1
    assert row.order_required is True
    assert row.order_side == "SELL"
    assert row.order_quantity == 1
    assert row.desired_position_status == PASS_POSITIVE_DESIRED_POSITION
    assert row.adjacent_limit_order_policy_status == FAIL_CLOSED_EXECUTION_UNRESOLVED
    assert row.tick_rounding_policy_status == FAIL_CLOSED_EXECUTION_UNRESOLVED
    assert row.working_order_lifecycle_status == FAIL_CLOSED_EXECUTION_UNRESOLVED
    assert row.actual_fill_ledger_status == FAIL_CLOSED_ACTUAL_FILL
    assert row.actual_cost_ledger_status == FAIL_CLOSED_ACTUAL_COST
    assert row.actual_pnl_ledger_status == FAIL_CLOSED_ACTUAL_PNL
    assert bundle.desired_position_rows_emitted is True
    assert bundle.order_intent_rows_emitted is True
    assert bundle.order_transition_metadata_rows_emitted is True
    assert bundle.actual_fill_rows_emitted is False
    assert bundle.actual_cost_rows_emitted is False
    assert bundle.actual_pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False


def test_positive_action_formula_chain_binds_local_pack_values():
    row = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH).positive_action_row

    assert row.raw_mean_reversion_forecast_value == pytest.approx(
        row.ewma5_equilibrium_value - row.hourly_current_price_value
    )
    assert row.sigma_price_value == pytest.approx(
        row.previous_completed_daily_close_value * row.annual_percentage_sigma_value / 16.0
    )
    assert row.risk_adjusted_forecast_before_veto_value == pytest.approx(
        row.raw_mean_reversion_forecast_value / row.sigma_price_value
    )
    assert row.risk_adjusted_forecast_after_veto_value == row.risk_adjusted_forecast_before_veto_value
    assert row.desired_rounded_position == _round_half_away_from_zero(row.desired_unrounded_contracts)


def test_positive_action_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared positive-action pack"):
        build_positive_action_executable_replay(tmp_path)


def test_positive_action_row_standalone_validate_is_not_authoritative():
    row = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH).positive_action_row

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("capped_forecast_value", 0.0),
        ("desired_unrounded_contracts", 0.0),
        ("desired_rounded_position", 0),
        ("position_change_contracts", 0),
        ("order_required", False),
        ("order_side", "BUY"),
        ("order_quantity", 2),
        ("actual_fill_ledger_status", "PASS_FORGED_FILL"),
        ("actual_cost_ledger_status", "PASS_FORGED_COST"),
        ("actual_pnl_ledger_status", "PASS_FORGED_PNL"),
    ),
)
def test_positive_action_rejects_self_consistent_row_forgery(field_name, forged_value):
    bundle = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)
    row = replace(bundle.positive_action_row, **{field_name: forged_value})
    row = replace(row, row_hash=canonical_sha256(_positive_action_row_hash_payload(row)))
    forged = replace(bundle, positive_action_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_positive_action_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "actual_limit_order_rows_emitted",
        "actual_market_order_rows_emitted",
        "actual_fill_rows_emitted",
        "actual_cost_rows_emitted",
        "actual_pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_positive_action_rejects_forbidden_actual_or_result_flags(flag_name):
    bundle = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_positive_action_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit actual execution/cost/PnL/result/evidence"):
        forged.validate()


def test_positive_action_requires_metadata_surface_flags():
    bundle = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)
    forged = replace(bundle, validation_metadata_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_positive_action_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must emit only authorized metadata surfaces"):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value", "message"),
    (
        ("status", "FORGED_STATUS", "status is not locked"),
        ("authorization_label", "FORGED_AUTHORIZATION", "authorization is not active"),
        ("lane", "CFD_ADAPTER", "lane must remain source-native futures"),
        ("input_pack_path", str(ROOT), "locked to the declared positive-action pack"),
    ),
)
def test_positive_action_rejects_forged_bundle_identity_fields(field_name, forged_value, message):
    bundle = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)
    forged = replace(bundle, **{field_name: forged_value})
    forged = replace(forged, bundle_hash=canonical_sha256(_positive_action_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match=message):
        forged.validate()


def test_positive_action_rejects_non_authorization_mutation():
    bundle = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)
    forged = replace(bundle, non_authorizations=bundle.non_authorizations[:-1])
    forged = replace(forged, bundle_hash=canonical_sha256(_positive_action_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="preserve non-authorizations"):
        forged.validate()


def test_positive_action_rejects_bundle_hash_tampering():
    bundle = build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)
    forged = replace(bundle, bundle_hash="f" * 64)

    with pytest.raises(CarverBlocked, match="bundle hash must be content-bound"):
        forged.validate()


def test_positive_action_rejects_manifest_row_family_hash_forgery(monkeypatch):
    manifest = json.loads((POSITIVE_ACTION_PACK_PATH / positive.POSITIVE_ACTION_MANIFEST_FILENAME).read_text())
    forged_manifest = copy.deepcopy(manifest)
    forged_manifest["row_family_files"]["hourly_decision_completed_bar.csv"]["sha256"] = "f" * 64
    monkeypatch.setattr(positive, "_read_manifest", lambda _pack_path: forged_manifest)

    with pytest.raises(CarverBlocked, match="manifest row-family hash must match bytes"):
        build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)


@pytest.mark.parametrize(
    "source_label",
    (
        "daily_risk_history",
        "ewmac_runtime_rows",
        "hourly_sanitized_bars",
        "roll_plan",
        "sigma_runtime_ledger",
        "symbology",
        "vqm_daily_ledger",
        "vqm_runtime_rows",
    ),
)
def test_positive_action_rejects_manifest_source_hash_forgery(monkeypatch, source_label):
    manifest = json.loads((POSITIVE_ACTION_PACK_PATH / positive.POSITIVE_ACTION_MANIFEST_FILENAME).read_text())
    forged_manifest = copy.deepcopy(manifest)
    forged_manifest["source_files"][source_label]["sha256"] = "f" * 64
    monkeypatch.setattr(positive, "_read_manifest", lambda _pack_path: forged_manifest)

    with pytest.raises(CarverBlocked, match="source hash must match local bytes"):
        build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_rejects_pack_hourly_close_that_does_not_match_source(monkeypatch):
    active_rows = positive._read_rows_by_file(POSITIVE_ACTION_PACK_PATH)
    forged_rows = dict(active_rows)
    decision_rows = [dict(row) for row in active_rows["hourly_decision_completed_bar.csv"]]
    decision_rows[0]["close_price"] = "109.0"
    forged_rows["hourly_decision_completed_bar.csv"] = tuple(decision_rows)
    monkeypatch.setattr(positive, "_read_rows_by_file", lambda _pack_path: forged_rows)

    with pytest.raises(CarverBlocked, match="hourly decision close must bind source formula"):
        build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_rejects_pack_daily_close_that_does_not_match_source(monkeypatch):
    active_rows = positive._read_rows_by_file(POSITIVE_ACTION_PACK_PATH)
    forged_rows = dict(active_rows)
    daily_rows = [dict(row) for row in active_rows["daily_current_contract_completed_bar.csv"]]
    daily_rows[0]["close_price"] = "109.0"
    forged_rows["daily_current_contract_completed_bar.csv"] = tuple(daily_rows)
    monkeypatch.setattr(positive, "_read_rows_by_file", lambda _pack_path: forged_rows)

    with pytest.raises(CarverBlocked, match="daily current-contract close must bind source formula"):
        build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)


@pytest.mark.parametrize(
    ("history_key", "forged_value", "message"),
    (
        (
            "selected_sigma_percent_t",
            "0.05000000000000000",
            "selected sigma manifest/source binding must bind source formula",
        ),
        (
            "selected_vqm_relative_volatility_v",
            "1.1111111111111111",
            "selected V/Q/M relative volatility V manifest/source binding must bind source formula",
        ),
        (
            "selected_vqm_quantile_q",
            "0.1111111111111111",
            "selected V/Q/M quantile Q manifest/source binding must bind source formula",
        ),
        (
            "selected_vqm_multiplier_m",
            "1.5000000000000000",
            "selected V/Q/M multiplier M manifest/source binding must bind source formula",
        ),
    ),
)
def test_positive_action_rejects_manifest_runtime_value_forgery_against_source_rows(
    monkeypatch,
    history_key,
    forged_value,
    message,
):
    manifest = json.loads((POSITIVE_ACTION_PACK_PATH / positive.POSITIVE_ACTION_MANIFEST_FILENAME).read_text())
    forged_manifest = copy.deepcopy(manifest)
    forged_manifest["history_evidence"][history_key] = forged_value
    monkeypatch.setattr(positive, "_read_manifest", lambda _pack_path: forged_manifest)

    with pytest.raises(CarverBlocked, match=message):
        build_positive_action_executable_replay(POSITIVE_ACTION_PACK_PATH)

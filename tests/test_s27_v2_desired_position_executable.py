from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.desired_position_executable import (
    ANNUAL_TARGET_RISK,
    CAPITAL_ACCOUNT_VALUE,
    CONTRACT_POINT_VALUE,
    DESIRED_POSITION_LEDGER_ROW_STATUS,
    FORECAST_TO_POSITION_DIVISOR,
    S27_V2_DESIRED_POSITION_AUTHORIZATION,
    S27_V2_DESIRED_POSITION_STATUS,
    _desired_position_bundle_hash_payload,
    _desired_position_row_hash_payload,
    _round_half_away_from_zero,
    _value_hash,
    build_desired_position_executable_ledger,
)
from carver.spine.s27_v2_replay.forecast_executable import _forecast_bundle_hash_payload
from carver.spine.s27_v2_replay.local_replay import canonical_sha256


REMEDIATION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_runtime_evidence_recon_znm6_20260413_declared_pack"
)


def test_desired_position_executable_builds_non_result_position_row():
    bundle = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH)
    row = bundle.desired_position_row

    assert bundle.status == S27_V2_DESIRED_POSITION_STATUS
    assert bundle.authorization_label == S27_V2_DESIRED_POSITION_AUTHORIZATION
    assert row.row_status == DESIRED_POSITION_LEDGER_ROW_STATUS
    assert row.raw_symbol == "ZNM6"
    assert row.selected_decision_timestamp_utc == "2026-04-13T03:00:00Z"
    assert row.capital_account_value == CAPITAL_ACCOUNT_VALUE
    assert row.annual_target_risk == ANNUAL_TARGET_RISK
    assert row.forecast_to_position_divisor == FORECAST_TO_POSITION_DIVISOR
    assert row.contract_point_value == CONTRACT_POINT_VALUE
    assert row.contract_point_value_currency == "USD"
    assert row.provider_instrument_id == "42000661"
    assert row.provider_activation == "2025-09-19 21:30:00+00:00"
    assert row.provider_expiration == "2026-06-18 17:01:00+00:00"
    assert row.provider_contract_multiplier_field_value == "2147483647"
    assert row.static_spec_source_file_hash == "908d9c147babf839ff4475f4286bf9e7828921f274f2d1a4a7a4cb5c2b7ead1d"
    assert row.provider_definition_source_file_hash == "cb1908e05cd41037a681a1a9aede56eb93001ad7c4576b048b15c87b0ec00742"
    assert row.desired_unrounded_contracts == pytest.approx(0.0)
    assert row.desired_rounded_contracts == 0
    assert row.initial_current_position_contracts == 0
    assert bundle.desired_position_rows_emitted is True
    assert bundle.order_rows_emitted is False
    assert bundle.fill_rows_emitted is False
    assert bundle.cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False


def test_desired_position_executable_formula_chain_matches_locked_policy():
    row = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH).desired_position_row

    expected_base = (
        row.capital_account_value
        * row.annual_target_risk
        * row.instrument_weight
        * row.instrument_diversification_multiplier
        / (
            row.current_price_value
            * row.contract_point_value
            * row.fx_rate
            * row.annual_percentage_risk_value
        )
    )
    expected_unrounded = expected_base * row.capped_forecast_value / row.forecast_to_position_divisor

    assert row.base_unrounded_contracts == pytest.approx(expected_base)
    assert row.desired_unrounded_contracts == pytest.approx(expected_unrounded)
    assert row.desired_rounded_contracts == _round_half_away_from_zero(expected_unrounded)


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        (0.0, 0),
        (0.49, 0),
        (0.5, 1),
        (1.5, 2),
        (-0.49, 0),
        (-0.5, -1),
        (-1.5, -2),
    ),
)
def test_round_half_away_from_zero_policy(value, expected):
    assert _round_half_away_from_zero(value) == expected


def test_desired_position_executable_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_desired_position_executable_ledger(tmp_path)


def test_desired_position_row_standalone_validate_is_not_authoritative():
    row = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH).desired_position_row

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


def test_desired_position_rejects_forged_forecast_bundle_even_with_recomputed_hashes():
    bundle = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH)
    forecast = replace(bundle.forecast_bundle, source_faithful_evidence_claimed=True)
    forecast = replace(forecast, bundle_hash=canonical_sha256(_forecast_bundle_hash_payload(forecast)))
    forged = replace(bundle, forecast_bundle=forecast)
    forged = replace(forged, bundle_hash=canonical_sha256(_desired_position_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit position/order/fill/cost/PnL/result/evidence"):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "hash_name", "hash_label", "forged_value"),
    (
        ("capital_account_value", "capital_policy_hash", None, 250000.0),
        ("annual_target_risk", "risk_target_policy_hash", None, 0.10),
        ("contract_point_value", None, None, 2147483647.0),
        ("forecast_to_position_divisor", "divisor_policy_hash", None, 20.0),
        ("current_price_value", "current_price_hash", "current price", 100.0),
        ("annual_percentage_risk_value", "annual_percentage_risk_hash", "annual percentage risk", 0.01),
        ("capped_forecast_value", "capped_forecast_hash", "capped forecast", 1.0),
    ),
)
def test_desired_position_rejects_self_consistent_policy_or_numeric_forgery(
    field_name,
    hash_name,
    hash_label,
    forged_value,
):
    bundle = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH)
    replacements = {field_name: forged_value}
    if hash_name and hash_label:
        replacements[hash_name] = _value_hash(hash_label, forged_value)
    row = replace(bundle.desired_position_row, **replacements)
    row = replace(row, row_hash=canonical_sha256(_desired_position_row_hash_payload(row)))
    forged = replace(bundle, desired_position_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_desired_position_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_desired_position_rejects_provider_multiplier_as_point_value_even_with_hashes():
    bundle = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH)
    row = replace(
        bundle.desired_position_row,
        contract_point_value=2147483647.0,
        base_unrounded_contracts=0.001,
        desired_unrounded_contracts=0.0,
        desired_rounded_contracts=0,
    )
    row = replace(row, row_hash=canonical_sha256(_desired_position_row_hash_payload(row)))
    forged = replace(bundle, desired_position_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_desired_position_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_desired_position_provider_definition_binds_latest_prior_selected_row():
    row = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH).desired_position_row

    assert row.provider_instrument_id == "42000661"
    assert row.provider_activation == "2025-09-19 21:30:00+00:00"
    assert row.provider_expiration == "2026-06-18 17:01:00+00:00"
    assert row.provider_definition_source_file_hash
    assert row.provider_definition_znm6_row_hash
    assert row.provider_contract_multiplier_field_value == "2147483647"


@pytest.mark.parametrize(
    "flag_name",
    (
        "order_rows_emitted",
        "fill_rows_emitted",
        "cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_desired_position_rejects_downstream_emission_flags(flag_name):
    bundle = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_desired_position_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit order/fill/cost/PnL/result/evidence"):
        forged.validate()


def test_desired_position_rejects_desired_position_emission_removed():
    bundle = build_desired_position_executable_ledger(REMEDIATION_PACK_PATH)
    forged = replace(bundle, desired_position_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_desired_position_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must mark desired-position rows emitted"):
        forged.validate()

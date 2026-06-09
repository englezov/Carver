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
    BLOCKED_INITIAL_POSITION,
    BLOCKED_TICK,
    BLOCKED_WORKING_LIMIT_LIFECYCLE,
)
from carver.spine.s27_v2_replay.forecast_executable import (
    FORECAST_LEDGER_ROW_STATUS,
    FORECAST_SCALAR_LABEL,
    FORECAST_SCALAR_VALUE,
    S27_V2_FORECAST_EXECUTABLE_AUTHORIZATION,
    S27_V2_FORECAST_EXECUTABLE_STATUS,
    _forecast_bundle_hash_payload,
    _forecast_row_hash_payload,
    _value_hash,
    build_forecast_executable_ledgers_on_remediation_pack,
)
from carver.spine.s27_v2_replay.local_replay import canonical_sha256


REMEDIATION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_runtime_evidence_recon_znm6_20260413_declared_pack"
)


def test_forecast_executable_builds_forecast_only_row_from_remediation_pack():
    bundle = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    row = bundle.forecast_row

    assert bundle.status == S27_V2_FORECAST_EXECUTABLE_STATUS
    assert bundle.authorization_label == S27_V2_FORECAST_EXECUTABLE_AUTHORIZATION
    assert row.row_status == FORECAST_LEDGER_ROW_STATUS
    assert row.raw_symbol == "ZNM6"
    assert row.selected_decision_timestamp_utc == "2026-04-13T03:00:00Z"
    assert row.selected_previous_daily_timestamp_utc == "2026-04-12T00:00:00Z"
    assert row.scalar_label == FORECAST_SCALAR_LABEL
    assert row.scalar_value == FORECAST_SCALAR_VALUE
    assert row.ewmac16_64_trend_sign == "NEGATIVE"
    assert row.trend_veto_decision == "ZERO_FORECAST_BY_TREND_VETO"
    assert bundle.forecast_rows_emitted is True
    assert bundle.position_rows_emitted is False
    assert bundle.order_rows_emitted is False
    assert bundle.fill_rows_emitted is False
    assert bundle.cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.unresolved_gate_labels == (
        BLOCKED_TICK,
        BLOCKED_COST_SCHEMA,
        BLOCKED_WORKING_LIMIT_LIFECYCLE,
        BLOCKED_INITIAL_POSITION,
    )


def test_forecast_executable_formula_chain_matches_book_locked_arithmetic():
    row = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH).forecast_row

    raw = row.ewma5_equilibrium_value - row.hourly_current_price_value
    sigma_price = (
        row.previous_completed_daily_close_current_contract_value
        * row.annual_percentage_sigma_value
        / 16.0
    )
    pre_veto = raw / sigma_price
    post_veto = 0.0
    post_vqm = post_veto * row.ewma10_multiplier_m_value
    capped = max(-20.0, min(20.0, post_vqm * 20.0))

    assert row.raw_mean_reversion_forecast_value == pytest.approx(raw)
    assert row.sigma_price_value == pytest.approx(sigma_price)
    assert row.risk_adjusted_forecast_before_veto_value == pytest.approx(pre_veto)
    assert row.risk_adjusted_forecast_after_veto_value == pytest.approx(post_veto)
    assert row.risk_adjusted_after_veto_times_m_before_scalar_value == pytest.approx(post_vqm)
    assert row.capped_forecast_value == pytest.approx(capped)
    assert row.capped_forecast_value == pytest.approx(0.0)


def test_forecast_executable_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_forecast_executable_ledgers_on_remediation_pack(tmp_path)


def test_forecast_executable_row_standalone_validate_is_not_authoritative():
    row = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH).forecast_row

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


@pytest.mark.parametrize(
    "field_name",
    (
        "sigma_source_row_hash",
        "ewmac_source_row_hash",
        "vqm_source_row_hash",
        "daily_continuous_row_hash",
        "daily_current_contract_row_hash",
        "hourly_decision_row_hash",
    ),
)
def test_forecast_executable_rejects_self_consistent_source_hash_forgery(field_name):
    bundle = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    row = replace(bundle.forecast_row, **{field_name: "0" * 64})
    row = replace(row, row_hash=canonical_sha256(_forecast_row_hash_payload(row)))
    forged = replace(bundle, forecast_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_forecast_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="forecast executable row must match active local runtime evidence"):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "hash_name", "value_hash_label"),
    (
        ("ewma5_equilibrium_value", "ewma5_equilibrium_hash", "EWMA5 equilibrium"),
        ("hourly_current_price_value", "hourly_current_price_hash", "hourly current price"),
        (
            "previous_completed_daily_close_current_contract_value",
            "previous_completed_daily_close_current_contract_hash",
            "previous daily current contract close",
        ),
        ("annual_percentage_sigma_value", "annual_percentage_sigma_hash", "annual percentage sigma"),
        ("ewmac16_64_trend_value", "ewmac16_64_trend_hash", "EWMAC16/64 trend"),
        ("relative_volatility_v_value", "relative_volatility_v_hash", "relative volatility V"),
        ("quantile_q_value", "quantile_q_hash", "quantile Q"),
        ("ewma10_multiplier_m_value", "ewma10_multiplier_m_hash", "EWMA10 multiplier M"),
    ),
)
def test_forecast_executable_rejects_self_consistent_numeric_forgery(field_name, hash_name, value_hash_label):
    bundle = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    forged_value = getattr(bundle.forecast_row, field_name) + 0.125
    row = replace(
        bundle.forecast_row,
        **{
            field_name: forged_value,
            hash_name: _value_hash(value_hash_label, forged_value),
        },
    )
    row = replace(row, row_hash=canonical_sha256(_forecast_row_hash_payload(row)))
    forged = replace(bundle, forecast_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_forecast_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_forecast_executable_rejects_self_consistent_capped_forecast_forgery():
    bundle = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    row = replace(
        bundle.forecast_row,
        capped_forecast_value=1.0,
        capped_forecast_hash=_value_hash("capped forecast", 1.0),
    )
    row = replace(row, row_hash=canonical_sha256(_forecast_row_hash_payload(row)))
    forged = replace(bundle, forecast_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_forecast_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="capped forecast must bind source formula"):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "position_rows_emitted",
        "order_rows_emitted",
        "fill_rows_emitted",
        "cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_forecast_executable_rejects_downstream_result_emission(flag_name):
    bundle = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_forecast_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit position/order/fill/cost/PnL/result/evidence"):
        forged.validate()


def test_forecast_executable_rejects_forecast_emission_removed():
    bundle = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    forged = replace(bundle, forecast_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_forecast_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must mark forecast rows emitted"):
        forged.validate()


def test_forecast_executable_rejects_runtime_history_bundle_forgery():
    bundle = build_forecast_executable_ledgers_on_remediation_pack(REMEDIATION_PACK_PATH)
    runtime = replace(bundle.runtime_history_bundle, bundle_hash="0" * 64)
    forged = replace(bundle, runtime_history_bundle=runtime)
    forged = replace(forged, bundle_hash=canonical_sha256(_forecast_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="runtime-history remediation bundle hash must be content-bound"):
        forged.validate()

from __future__ import annotations

import csv
import json
from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.pretest_development_recon_completion_run import (
    DEFAULT_OUTPUT_RELATIVE_PATH,
    DEFAULT_PACK_RELATIVE_PATH,
    NON_AUTHORIZATIONS,
    PretestDevelopmentReconRunConfig,
    _compute_rows,
    _bundle_payload,
    _read_csv_rows,
    _read_json,
    _validate_manifest_summaries,
    run_pretest_development_recon_completion,
)
from carver.spine.s27_v2_replay.pretest_machine_freeze import validate_pretest_machine_freeze_rows


PACK_ROOT = ROOT / DEFAULT_PACK_RELATIVE_PATH
RUN_ROOT = ROOT / DEFAULT_OUTPUT_RELATIVE_PATH


@pytest.fixture(scope="module")
def completion_bundle():
    return run_pretest_development_recon_completion()


def _rows(root: Path, name: str) -> list[dict[str, str]]:
    with (root / name).open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _json(root: Path, name: str) -> dict[str, object]:
    return json.loads((root / name).read_text(encoding="ascii"))


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_bundle_payload(bundle)))


def _active_pack_and_computed_rows():
    manifest = _read_json(
        PACK_ROOT / "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_MANIFEST.json"
    )
    rows = {
        name: _read_csv_rows(PACK_ROOT / name)
        for name in (
            "runtime_evidence_ledger.csv",
            "daily_continuous_completed_bar.csv",
            "daily_current_contract_completed_bar.csv",
            "hourly_decision_completed_bar.csv",
            "hourly_fill_completed_bar.csv",
            "valuation_mark_completed_bar.csv",
            "session_calendar.csv",
            "roll_calendar.csv",
            "cost_parameter.csv",
        )
    }
    return rows, _compute_rows(manifest, rows)


def _clone(value):
    return json.loads(json.dumps(value))


def test_completion_pack_declares_first_organic_filled_sell_completion():
    manifest = _json(PACK_ROOT, "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_MANIFEST.json")
    decisions = _rows(PACK_ROOT, "hourly_decision_completed_bar.csv")
    fills = _rows(PACK_ROOT, "hourly_fill_completed_bar.csv")
    marks = _rows(PACK_ROOT, "valuation_mark_completed_bar.csv")
    runtime = _rows(PACK_ROOT, "runtime_evidence_ledger.csv")

    assert manifest["status"] == "LOCAL_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_PACK_DECLARED_NOT_RESULT"
    assert manifest["selected_slice_rule"] == "EARLIEST_ALREADY_LOCAL_2022_ORGANIC_FILLED_SELL_REDUCTION_AFTER_STRICT_PRIOR_WARMUPS_PRESERVE_2023_FOR_TEST"
    assert len(decisions) == len(fills) == len(marks) == len(runtime) == 46
    assert decisions[0]["completed_timestamp_utc"] == "2022-01-03T01:00:00Z"
    assert decisions[-1]["completed_timestamp_utc"] == "2022-07-05T23:00:00Z"
    assert fills[-1]["completed_timestamp_utc"] == "2022-07-06T00:00:00Z"
    assert marks[-1]["completed_timestamp_utc"] == "2022-07-06T02:00:00Z"
    assert decisions[-1]["raw_symbol"] == "ZNU2"
    assert fills[-1]["raw_symbol"] == "ZNU2"
    assert marks[-1]["raw_symbol"] == "ZNU2"
    assert all(
        decision["raw_symbol"] == fill["raw_symbol"] == mark["raw_symbol"]
        for decision, fill, mark in zip(decisions, fills, marks, strict=True)
    )
    assert runtime[-1]["previous_daily_trading_date"] == "2022-07-05"
    assert runtime[-1]["daily_window_row_count"] == "64"
    assert runtime[-1]["runtime_status"] == "PASS_ROLLING_STRICT_PRIOR_DAILY_EVIDENCE_PRETEST_DEV_RECON_NOT_RESULT"
    assert manifest["filled_sell_completion"] == {
        "decision_timestamp_utc": "2022-07-05T23:00:00Z",
        "desired_position_contracts": 0,
        "fill_candidate_close": "119.8125",
        "fill_executed": "YES",
        "fill_timestamp_utc": "2022-07-06T00:00:00Z",
        "limit_order_price": "117.390625",
        "order_quantity": 39,
        "order_side": "SELL",
        "position_change_contracts": -39,
        "raw_symbol": "ZNU2",
        "row_index": 46,
        "starting_position_contracts": 39,
    }
    assert manifest["history_evidence"]["rolling_strict_prior_daily_evidence"] == "PASS_RECOMPUTED_PER_SELECTED_ROW_FROM_ALREADY_LOCAL_PRE2023_SOURCE_LEDGERS"
    for required in ("NO_2023_TEST_DATA", "NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"):
        assert required in manifest["explicitly_excluded_data"]


def test_completion_pack_hashes_bind_file_bytes():
    manifest = _json(PACK_ROOT, "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_MANIFEST.json")

    for filename, declared in manifest["row_family_files"].items():
        assert declared["sha256"].lower() == _sha256(PACK_ROOT / filename)


def test_completion_run_emits_filled_sell_completion_and_flattens_position(completion_bundle):
    positions = _rows(RUN_ROOT, "desired_position_ledger.csv")
    orders = _rows(RUN_ROOT, "limit_order_ledger.csv")
    no_market = _rows(RUN_ROOT, "no_market_order_ledger.csv")
    fills = _rows(RUN_ROOT, "fill_ledger.csv")
    transitions = _rows(RUN_ROOT, "working_order_transition_ledger.csv")
    pnl = _rows(RUN_ROOT, "pnl_ledger.csv")

    assert completion_bundle.row_count == 46
    assert completion_bundle.first_filled_sell_row_index == 46
    assert completion_bundle.final_position_contracts == 0

    assert positions[0]["starting_position_contracts"] == "0"
    assert positions[0]["desired_position_contracts"] == "8"
    assert positions[0]["position_change_contracts"] == "8"
    assert float(orders[0]["limit_order_price"]) == pytest.approx(130.421875)
    assert fills[0]["fill_executed"] == "TRUE"
    assert fills[0]["position_after_fill"] == "8"

    assert positions[8]["starting_position_contracts"] == "18"
    assert positions[8]["desired_position_contracts"] == "24"
    assert positions[8]["position_change_contracts"] == "6"
    assert orders[8]["order_side"] == "BUY"
    assert orders[8]["order_quantity"] == "6"
    assert fills[8]["fill_executed"] == "FALSE"
    assert transitions[8]["working_state_after"] == "UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE"
    assert no_market[8]["market_fallback_status"] == "FAIL_CLOSED_UNFILLED_LIMIT_ORDER_MARKET_FALLBACK_NOT_AUTHORIZED"

    assert positions[-1]["starting_position_contracts"] == "39"
    assert positions[-1]["desired_position_contracts"] == "0"
    assert positions[-1]["position_change_contracts"] == "-39"
    assert orders[-1]["order_side"] == "SELL"
    assert orders[-1]["order_quantity"] == "39"
    assert orders[-1]["adjacent_target_position"] == "38"
    assert float(orders[-1]["formula_limit_price"]) == pytest.approx(117.38163453280157)
    assert float(orders[-1]["limit_order_price"]) == pytest.approx(117.390625)
    assert fills[-1]["fill_executed"] == "TRUE"
    assert fills[-1]["fill_rule"] == "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL"
    assert float(fills[-1]["fill_candidate_close"]) == pytest.approx(119.8125)
    assert float(fills[-1]["fill_price"]) == pytest.approx(117.390625)
    assert fills[-1]["fill_quantity"] == "39"
    assert fills[-1]["position_after_fill"] == "0"
    assert transitions[-1]["working_state_before"] == "NO_OPEN_WORKING_ORDER_CARRIED"
    assert transitions[-1]["working_state_after"] == "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
    assert transitions[-1]["same_session"] == "TRUE"
    assert [row["market_order_required"] for row in no_market] == ["FALSE"] * 46
    assert [row["market_order_rows_emitted"] for row in no_market] == ["FALSE"] * 46
    assert no_market[-1]["market_fallback_status"] == "NOT_REQUIRED_LIMIT_ORDER_FILLED"

    assert float(pnl[0]["row_net_pnl_amount"]) == pytest.approx(-1018.4)
    assert pnl[-1]["valuation_mark_timestamp_utc"] == "2022-07-06T02:00:00Z"
    assert pnl[-1]["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert float(pnl[-1]["existing_position_gross_pnl"]) == pytest.approx(-344906.25)
    assert float(pnl[-1]["fill_gross_pnl"]) == pytest.approx(-93234.375)
    assert float(pnl[-1]["row_gross_pnl_amount"]) == pytest.approx(-438140.625)
    assert float(pnl[-1]["row_net_pnl_amount"]) == pytest.approx(-438230.325)
    assert float(pnl[-1]["cumulative_gross_pnl_amount"]) == pytest.approx(-498734.375)
    assert float(pnl[-1]["cumulative_commission_amount"]) == pytest.approx(179.4)
    assert float(pnl[-1]["cumulative_spread_amount"]) == pytest.approx(0.0)
    assert float(pnl[-1]["cumulative_net_pnl_amount"]) == pytest.approx(-498913.775)
    assert completion_bundle.cumulative_net_pnl_amount == pytest.approx(-498913.775)


def test_completion_run_writes_hash_bound_metadata(completion_bundle):
    manifest = _json(RUN_ROOT, "run_manifest.json")
    evidence = _json(RUN_ROOT, "evidence_manifest.json")
    trusted = _json(RUN_ROOT, "trusted_bundle.json")
    sha_rows = _rows(RUN_ROOT, "SHA256SUMS.csv")
    sha_by_path = {row["relative_path"]: row["sha256"] for row in sha_rows}

    assert manifest["status"] == "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_RUN_EMITTED_NOT_RESULT"
    assert manifest["row_count"] == 46
    assert manifest["first_filled_sell_row_index"] == 46
    assert manifest["result_interpretation"] == "NO"
    assert manifest["source_faithful_evidence_claim"] == "NO"
    assert evidence["run_manifest_hash"] == _sha256(RUN_ROOT / "run_manifest.json")
    assert trusted["result_status"] == "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
    assert trusted["source_faithful_evidence_claimed"] is False
    assert completion_bundle.run_manifest_hash == _sha256(RUN_ROOT / "run_manifest.json")
    assert completion_bundle.evidence_manifest_hash == _sha256(RUN_ROOT / "evidence_manifest.json")
    assert completion_bundle.trusted_bundle_hash == _sha256(RUN_ROOT / "trusted_bundle.json")
    for relative_path, digest in sha_by_path.items():
        assert digest == _sha256(RUN_ROOT / relative_path)


def test_completion_run_rejects_out_of_scope_paths(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited completion declared local ZN input pack"):
        run_pretest_development_recon_completion(
            PretestDevelopmentReconRunConfig(input_pack_path=str(tmp_path), output_root=str(RUN_ROOT))
        )
    with pytest.raises(CarverBlocked, match="output root is locked"):
        run_pretest_development_recon_completion(
            PretestDevelopmentReconRunConfig(input_pack_path=str(PACK_ROOT), output_root=str(tmp_path))
        )

    sibling_pack = ROOT / "docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_broader_dev_recon_2022_first_session_declared_pack"
    sibling_run = ROOT / "docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_broader_dev_recon_2022_first_session_run"
    with pytest.raises(CarverBlocked, match="locked to the audited completion declared local ZN input pack"):
        run_pretest_development_recon_completion(
            PretestDevelopmentReconRunConfig(input_pack_path=str(sibling_pack), output_root=str(RUN_ROOT))
        )
    with pytest.raises(CarverBlocked, match="output root is locked"):
        run_pretest_development_recon_completion(
            PretestDevelopmentReconRunConfig(input_pack_path=str(PACK_ROOT), output_root=str(sibling_run))
        )


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("row_count", 1),
        ("first_filled_sell_row_index", 1),
        ("final_position_contracts", 39),
        ("status", "FORGED_STATUS"),
        ("authorization_label", "FORGED_AUTHORIZATION"),
        ("strategy_id", "FORGED_STRATEGY"),
        ("instrument", "FORGED_INSTRUMENT"),
        ("lane", "FORGED_LANE"),
        ("input_pack_path", str(ROOT)),
        ("output_root", str(ROOT)),
        ("run_manifest_hash", "a" * 64),
        ("evidence_manifest_hash", "b" * 64),
        ("trusted_bundle_hash", "c" * 64),
        ("cumulative_gross_pnl_amount", 0.0),
        ("cumulative_commission_amount", 0.0),
        ("cumulative_spread_amount", 1.0),
        ("cumulative_net_pnl_amount", 1.0),
    ),
)
def test_completion_run_rejects_bundle_forgery(completion_bundle, field_name, forged_value):
    forged = _rehash_bundle(replace(completion_bundle, **{field_name: forged_value}))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_completion_run_preserves_non_authorizations(completion_bundle):
    assert completion_bundle.non_authorizations == NON_AUTHORIZATIONS
    for required in ("NO_TEST_ACCESS", "NO_VALIDATION_ACCESS", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD", "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM"):
        assert required in completion_bundle.non_authorizations

    forged = _rehash_bundle(
        replace(
            completion_bundle,
            non_authorizations=tuple(
                x for x in NON_AUTHORIZATIONS if x != "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM"
            ),
        )
    )
    with pytest.raises(CarverBlocked):
        forged.validate()


def test_completion_run_is_not_package_root_exported():
    assert "run_pretest_development_recon_completion" not in getattr(package_root, "__all__", ())
    assert not hasattr(package_root, "run_pretest_development_recon_completion")


def test_completion_run_rejects_manifest_summary_forgery():
    manifest = _read_json(
        PACK_ROOT / "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_MANIFEST.json"
    )
    rows = {
        name: _read_csv_rows(PACK_ROOT / name)
        for name in (
            "runtime_evidence_ledger.csv",
            "daily_continuous_completed_bar.csv",
            "daily_current_contract_completed_bar.csv",
            "hourly_decision_completed_bar.csv",
            "hourly_fill_completed_bar.csv",
            "valuation_mark_completed_bar.csv",
            "session_calendar.csv",
            "roll_calendar.csv",
            "cost_parameter.csv",
        )
    }
    computed = _compute_rows(manifest, rows)

    forged_manifest = json.loads(json.dumps(manifest))
    forged_manifest["decision_fill_mark_plan"][8]["valuation_mark_timestamp_utc"] = "2099-01-01T00:00:00Z"
    with pytest.raises(CarverBlocked, match="decision/fill/valuation summary must match active selected rows"):
        _validate_manifest_summaries(forged_manifest, rows, computed)


def test_pretest_machine_freeze_accepts_current_repaired_checkpoint():
    rows, computed = _active_pack_and_computed_rows()

    validate_pretest_machine_freeze_rows(rows, computed)


@pytest.mark.parametrize(
    ("family", "field_name", "forged_value", "message"),
    (
        ("market", "market_order_required", True, "market-order-required"),
        ("market", "market_order_rows_emitted", True, "market-order row emission"),
        ("cost", "spread_cost_amount", 1.0, "market-spread costs"),
    ),
)
def test_pretest_machine_freeze_rejects_unresolved_market_and_spread_states(
    family, field_name, forged_value, message
):
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    forged[family][0][field_name] = forged_value

    with pytest.raises(CarverBlocked, match=message):
        validate_pretest_machine_freeze_rows(rows, forged)


def test_pretest_machine_freeze_rejects_filled_order_cross_session_state():
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    filled_index = next(index for index, row in enumerate(forged["fill"]) if row["fill_executed"] is True)
    forged["transition"][filled_index]["same_session"] = False

    with pytest.raises(CarverBlocked, match="session/EOD"):
        validate_pretest_machine_freeze_rows(rows, forged)


def test_pretest_machine_freeze_rejects_unfilled_limit_without_fail_closed_working_state():
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    unfilled_index = next(
        index
        for index, (order, fill) in enumerate(zip(forged["order"], forged["fill"], strict=True))
        if order["order_side"] != "NONE" and fill["fill_executed"] is False
    )
    forged["transition"][unfilled_index]["working_state_after"] = "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"

    with pytest.raises(CarverBlocked, match="working state"):
        validate_pretest_machine_freeze_rows(rows, forged)


def test_pretest_machine_freeze_rejects_roll_boundary_live_order():
    rows, computed = _active_pack_and_computed_rows()
    forged_rows = _clone(rows)
    unfilled_index = next(
        index
        for index, (order, fill) in enumerate(zip(computed["order"], computed["fill"], strict=True))
        if order["order_side"] != "NONE" and fill["fill_executed"] is False
    )
    forged_rows["roll_calendar.csv"][0]["roll_transition_date"] = forged_rows["hourly_decision_completed_bar.csv"][
        unfilled_index
    ]["trading_date"]

    with pytest.raises(CarverBlocked, match="roll-boundary"):
        validate_pretest_machine_freeze_rows(forged_rows, computed)


def test_pretest_machine_freeze_rejects_cross_contract_row_chain():
    rows, computed = _active_pack_and_computed_rows()
    forged_rows = _clone(rows)
    forged_rows["hourly_fill_completed_bar.csv"][0]["raw_symbol"] = "FORGED"

    with pytest.raises(CarverBlocked, match="cross-contract"):
        validate_pretest_machine_freeze_rows(forged_rows, computed)


def test_pretest_machine_freeze_rejects_degraded_declared_rows():
    rows, computed = _active_pack_and_computed_rows()
    forged_rows = _clone(rows)
    forged_rows["hourly_decision_completed_bar.csv"][0]["readiness_status"] = "DEGRADED_PROVIDER_CONDITION"

    with pytest.raises(CarverBlocked, match="degraded"):
        validate_pretest_machine_freeze_rows(forged_rows, computed)


@pytest.mark.parametrize(
    ("family", "field_name"),
    (
        ("daily_continuous_completed_bar.csv", "provider_condition_status"),
        ("daily_current_contract_completed_bar.csv", "readiness_status"),
        ("cost_parameter.csv", "cost_policy_status"),
    ),
)
def test_pretest_machine_freeze_rejects_degraded_status_in_any_declared_family(family, field_name):
    rows, computed = _active_pack_and_computed_rows()
    forged_rows = _clone(rows)
    forged_rows[family][0][field_name] = "DEGRADED_PROVIDER_CONDITION"

    with pytest.raises(CarverBlocked, match="degraded"):
        validate_pretest_machine_freeze_rows(forged_rows, computed)


def test_pretest_machine_freeze_rejects_pending_declared_status():
    rows, computed = _active_pack_and_computed_rows()
    forged_rows = _clone(rows)
    forged_rows["session_calendar.csv"][0]["calendar_status"] = "PENDING_SESSION_EVIDENCE"

    with pytest.raises(CarverBlocked, match="degraded"):
        validate_pretest_machine_freeze_rows(forged_rows, computed)


def test_pretest_machine_freeze_rejects_zero_side_position_change():
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    no_order_index = next(index for index, row in enumerate(forged["order"]) if row["order_side"] == "NONE")
    forged["position"][no_order_index]["desired_position_contracts"] = (
        forged["position"][no_order_index]["starting_position_contracts"] + 1
    )

    with pytest.raises(CarverBlocked, match="zero-side"):
        validate_pretest_machine_freeze_rows(rows, forged)


def test_pretest_machine_freeze_rejects_zero_side_market_fallback_drift():
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    no_order_index = next(index for index, row in enumerate(forged["order"]) if row["order_side"] == "NONE")
    forged["market"][no_order_index]["market_fallback_status"] = "NOT_REQUIRED_LIMIT_ORDER_FILLED"

    with pytest.raises(CarverBlocked, match="no-order market fallback"):
        validate_pretest_machine_freeze_rows(rows, forged)


def test_pretest_machine_freeze_rejects_fractional_contract_fields():
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    no_order_index = next(index for index, row in enumerate(forged["order"]) if row["order_side"] == "NONE")
    forged["order"][no_order_index]["order_quantity"] = "0.5"

    with pytest.raises(CarverBlocked, match="integer ledger fields"):
        validate_pretest_machine_freeze_rows(rows, forged)


@pytest.mark.parametrize(
    ("family", "field_name"),
    (
        ("position", "starting_position_contracts"),
        ("position", "desired_position_contracts"),
        ("position", "position_change_contracts"),
        ("order", "order_quantity"),
        ("order", "adjacent_target_position"),
        ("transition", "starting_position_contracts"),
        ("transition", "ending_position_contracts"),
        ("fill", "fill_quantity"),
        ("fill", "position_after_fill"),
        ("pnl", "ending_position_contracts"),
    ),
)
def test_pretest_machine_freeze_rejects_fractional_contract_fields_globally(family, field_name):
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    forged[family][0][field_name] = "1.5"

    with pytest.raises(CarverBlocked, match="integer ledger fields"):
        validate_pretest_machine_freeze_rows(rows, forged)


def test_pretest_machine_freeze_allows_fractional_base_position_as_finite_continuous_sizing_field():
    rows, computed = _active_pack_and_computed_rows()

    assert computed["position"][0]["base_position_contracts"] == pytest.approx(16.432147617721743)
    validate_pretest_machine_freeze_rows(rows, computed)


@pytest.mark.parametrize("forged_value", ("nan", "inf", "-inf", "NOT_NUMERIC"))
def test_pretest_machine_freeze_rejects_non_finite_base_position_continuous_sizing_field(forged_value):
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    forged["position"][0]["base_position_contracts"] = forged_value

    with pytest.raises(CarverBlocked, match="numeric ledger fields"):
        validate_pretest_machine_freeze_rows(rows, forged)


@pytest.mark.parametrize(
    ("family", "field_name", "forged_value"),
    (
        ("market", "market_order_required", "YES"),
        ("market", "market_order_rows_emitted", "1"),
        ("fill", "fill_executed", "PENDING"),
        ("transition", "same_session", "YES"),
    ),
)
def test_pretest_machine_freeze_rejects_malformed_boolean_fields(family, field_name, forged_value):
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    forged[family][0][field_name] = forged_value

    with pytest.raises(CarverBlocked, match="boolean ledger fields"):
        validate_pretest_machine_freeze_rows(rows, forged)


def test_pretest_machine_freeze_rejects_non_finite_spread_cost():
    rows, computed = _active_pack_and_computed_rows()
    forged = _clone(computed)
    forged["cost"][0]["spread_cost_amount"] = "nan"

    with pytest.raises(CarverBlocked, match="numeric ledger fields"):
        validate_pretest_machine_freeze_rows(rows, forged)

from __future__ import annotations

import csv
import json
from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools" / "databento"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.test_mechanical_run import (
    BACKTEST_STATUS,
    COMBINED_MARKET_TBBO_REGISTRY_NAME,
    COMBINED_MARKET_TBBO_REGISTRY_RELATIVE_PATH,
    DEFAULT_MANIFEST_NAME,
    DEFAULT_OUTPUT_RELATIVE_PATH,
    DEFAULT_PACK_RELATIVE_PATH,
    DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH,
    FAIL_CLOSED_BLOCKER_STATUS,
    NON_AUTHORIZATIONS,
    RESULT_STATUS,
    _bundle_payload,
    _expected_market_spread_evidence,
    _tbbo_requirements_bundle_payload,
    build_2023_test_declared_pack,
    build_2023_test_combined_market_tbbo_registry,
    discover_2023_test_market_order_tbbo_requirements,
    run_2023_test_mechanical_artifacts,
)


PACK_ROOT = ROOT / DEFAULT_PACK_RELATIVE_PATH
RUN_ROOT = ROOT / DEFAULT_OUTPUT_RELATIVE_PATH
TBBO_REQUIREMENTS_ROOT = ROOT / DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH
COMBINED_TBBO_ROOT = ROOT / COMBINED_MARKET_TBBO_REGISTRY_RELATIVE_PATH


@pytest.fixture(scope="module")
def test_manifest():
    return build_2023_test_declared_pack()


@pytest.fixture(scope="module")
def test_bundle(test_manifest):
    del test_manifest
    return run_2023_test_mechanical_artifacts()


def _rows(root: Path, name: str) -> list[dict[str, str]]:
    with (root / name).open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _json(root: Path, name: str) -> dict[str, object]:
    return json.loads((root / name).read_text(encoding="ascii"))


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_csv_header_only(path: Path, fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()


def _rehash_csv_row(row: dict[str, str]) -> None:
    row.pop("row_hash", None)
    row["row_hash"] = canonical_sha256(row)


def _write_json_file(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _refresh_evidence_and_trusted_hashes(root: Path) -> tuple[str, str]:
    evidence = _json(root, "evidence_manifest.json")
    ledger_hashes = evidence["ledger_hashes"]
    assert isinstance(ledger_hashes, dict)
    for filename in list(ledger_hashes):
        ledger_hashes[filename] = _sha256(root / filename).lower()
    _write_json_file(root / "evidence_manifest.json", evidence)
    trusted = _json(root, "trusted_bundle.json")
    trusted["evidence_manifest_hash"] = _sha256(root / "evidence_manifest.json")
    _write_json_file(root / "trusted_bundle.json", trusted)
    return _sha256(root / "evidence_manifest.json"), _sha256(root / "trusted_bundle.json")


def test_2023_test_pack_is_declared_and_exhausts_authorized_1378_row_slice(test_manifest):
    decisions = _rows(PACK_ROOT, "hourly_decision_completed_bar.csv")
    runtime = _rows(PACK_ROOT, "runtime_evidence_ledger.csv")

    assert test_manifest["status"] == "LOCAL_2023_TEST_DECLARED_INPUT_PACK_BUILT_FROM_ALREADY_LOCAL_SOURCE_NOT_RESULT"
    assert test_manifest["test_window_start"] == "2023-01-03T00:00:00Z"
    assert test_manifest["test_window_fail_closed_timestamp"] == "NOT_APPLICABLE_DECLARED_PACK_EXHAUSTED_NO_FAIL_CLOSED_BLOCKER"
    assert test_manifest["test_window_terminal_timestamp"] == "2023-03-30T23:00:00Z"
    assert test_manifest["test_window_end_status"] == "DECLARED_PACK_EXHAUSTED_NO_FAIL_CLOSED_BLOCKER_NOT_RESULT"
    assert test_manifest["candidate_row_count"] == 1378
    assert test_manifest["supported_mechanical_row_count"] == 1378
    assert len(decisions) == len(runtime) == 1378
    assert decisions[0]["completed_timestamp_utc"] == "2023-01-03T00:00:00Z"
    assert decisions[-1]["completed_timestamp_utc"] == "2023-03-30T23:00:00Z"
    assert all(row["completed_timestamp_utc"].startswith("2023-") for row in decisions)
    assert all(row["runtime_status"] == "PASS_ROLLING_STRICT_PRIOR_DAILY_EVIDENCE_2023_TEST_NOT_RESULT" for row in runtime)
    assert test_manifest["fail_closed_blocker"] == {
        "adjacent_target_position": 4,
        "decision_timestamp_utc": "NOT_APPLICABLE_DECLARED_PACK_EXHAUSTED",
        "desired_position_contracts": 3,
        "formula_status": "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT",
        "order_side": "SELL",
        "position_change_contracts": -2,
        "raw_symbol": "ZNM3",
        "row_index": 0,
        "starting_position_contracts": 5,
    }
    assert "NO_VALIDATION" in test_manifest["explicitly_excluded_data"]
    assert "NO_LOCKBOX" in test_manifest["explicitly_excluded_data"]


def test_2023_test_pack_hashes_bind_file_bytes(test_manifest):
    for filename, declared in test_manifest["row_family_files"].items():
        assert declared["sha256"].lower() == _sha256(PACK_ROOT / filename)


def test_2023_test_mechanical_run_fails_closed_without_result_claim(test_bundle):
    manifest = _json(RUN_ROOT, "run_manifest.json")
    fail_rows = _rows(RUN_ROOT, "fail_closed_ledger.csv")
    runtime_rows = _rows(RUN_ROOT, "runtime_history_ledger.csv")
    forecast_rows = _rows(RUN_ROOT, "forecast_replay_ledger.csv")
    position_rows = _rows(RUN_ROOT, "desired_position_ledger.csv")
    pnl_rows = _rows(RUN_ROOT, "pnl_ledger.csv")
    orders = _rows(RUN_ROOT, "limit_order_ledger.csv")
    no_market_rows = _rows(RUN_ROOT, "no_market_order_ledger.csv")
    market_order_rows = _rows(RUN_ROOT, "market_order_ledger.csv")
    market_fill_metadata_rows = _rows(RUN_ROOT, "market_fill_metadata_ledger.csv")
    transitions = _rows(RUN_ROOT, "working_order_transition_ledger.csv")
    fills = _rows(RUN_ROOT, "fill_ledger.csv")
    costs = _rows(RUN_ROOT, "cost_ledger.csv")

    assert test_bundle.candidate_row_count == 1378
    assert test_bundle.supported_mechanical_row_count == 1378
    assert test_bundle.fail_closed_row_index == 0
    assert test_bundle.fail_closed_reason == "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"
    assert manifest["status"] == "LOCAL_2023_TEST_MECHANICAL_ARTIFACT_RUN_FAIL_CLOSED_NOT_RESULT"
    assert manifest["result_interpretation"] == "NO"
    assert manifest["source_faithful_evidence_claim"] == "NO"
    assert len(runtime_rows) == len(forecast_rows) == len(position_rows) == 1378
    assert len(pnl_rows) == len(orders) == len(no_market_rows) == len(fills) == 1378
    assert len(costs) == 1378
    assert len(market_order_rows) == 256
    assert len(market_fill_metadata_rows) == 256
    assert len(fail_rows) == 0
    assert orders[0]["order_side"] == "BUY"
    assert orders[0]["order_quantity"] == "2"
    assert orders[0]["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert orders[0]["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert orders[0]["row_status"] == "LOCAL_MARKET_ORDER_PLAN_ROW_EMITTED_NOT_LIMIT_ORDER_NOT_RESULT"
    assert position_rows[0]["position_change_contracts"] == "2"
    assert no_market_rows[0]["market_order_required"] == "TRUE"
    assert no_market_rows[0]["market_order_rows_emitted"] == "TRUE"
    assert no_market_rows[0]["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert fills[0]["fill_executed"] == "TRUE"
    assert fills[0]["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert fills[0]["fill_price"] == "112.5625"
    assert fills[0]["fill_quantity"] == "2"
    assert fills[0]["position_after_fill"] == "2"
    assert fills[1]["fill_executed"] == "TRUE"
    assert fills[1]["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert fills[1]["fill_candidate_close"] == "112.59375"
    assert fills[1]["fill_price"] == "112.578125"
    assert fills[1]["fill_quantity"] == "2"
    assert fills[1]["position_after_fill"] == "0"
    row701_position = next(row for row in position_rows if row["row_index"] == "701")
    row701_order = next(row for row in orders if row["row_index"] == "701")
    row701_no_market = next(row for row in no_market_rows if row["row_index"] == "701")
    row701_transition = next(row for row in transitions if row["row_index"] == "701")
    row701_fill = next(row for row in fills if row["row_index"] == "701")
    row701_cost = next(row for row in costs if row["row_index"] == "701")
    row701_pnl = next(row for row in pnl_rows if row["row_index"] == "701")
    roll_suppression_label = (
        "LOCAL_ONLY_ENGINEERING_ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ASSUMPTION_NOT_BOOK_EXPLICIT_NOT_SOURCE_FAITHFUL"
    )
    roll_suppression_status = "LOCAL_ENGINEERING_ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSED_ROW_EMITTED_NOT_RESULT"
    assert row701_position["starting_position_contracts"] == "0"
    assert row701_position["desired_position_contracts"] == "0"
    assert row701_position["position_change_contracts"] == "0"
    assert row701_position["row_status"] == roll_suppression_status
    assert row701_order["order_side"] == "NONE"
    assert row701_order["order_quantity"] == "0"
    assert row701_order["formula_limit_price"] == roll_suppression_label
    assert row701_order["limit_order_price"] == roll_suppression_label
    assert row701_no_market["market_order_required"] == "FALSE"
    assert row701_no_market["market_order_rows_emitted"] == "FALSE"
    assert row701_no_market["market_fallback_status"] == "NOT_REQUIRED_NO_ORDER_POSITION_UNCHANGED"
    assert row701_no_market["engineering_convention_label"] == roll_suppression_label
    assert row701_transition["starting_position_contracts"] == "0"
    assert row701_transition["ending_position_contracts"] == "0"
    assert row701_transition["working_state_after"] == "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
    assert row701_fill["fill_executed"] == "FALSE"
    assert row701_fill["fill_rule"] == roll_suppression_label
    assert row701_fill["fill_quantity"] == "0"
    assert row701_fill["position_after_fill"] == "0"
    assert row701_cost["commission_amount"] == "0.0"
    assert row701_cost["spread_cost_amount"] == "0.0"
    assert row701_cost["total_cost_amount"] == "0.0"
    assert row701_pnl["row_gross_pnl_amount"] == "0.0"
    assert row701_pnl["row_net_pnl_amount"] == "0.0"
    assert row701_pnl["ending_position_contracts"] == "0"
    row892_order = next(row for row in orders if row["row_index"] == "892")
    row892_no_market = next(row for row in no_market_rows if row["row_index"] == "892")
    row892_transition = next(row for row in transitions if row["row_index"] == "892")
    row892_fill = next(row for row in fills if row["row_index"] == "892")
    row892_cost = next(row for row in costs if row["row_index"] == "892")
    row892_pnl = next(row for row in pnl_rows if row["row_index"] == "892")
    assert row892_order["order_side"] == "SELL"
    assert row892_order["order_quantity"] == "1"
    assert row892_order["adjacent_target_position"] == "-1"
    assert row892_order["formula_limit_price"] == "111.6707138465356"
    assert row892_order["limit_order_price"] == "111.671875"
    assert row892_order["row_status"] == "LOCAL_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ROW_EMITTED_NOT_RESULT"
    assert row892_no_market["market_order_required"] == "FALSE"
    assert row892_no_market["market_order_rows_emitted"] == "FALSE"
    assert row892_no_market["market_fallback_status"] == "NOT_REQUIRED_LIMIT_ORDER_FILLED"
    assert (
        row892_no_market["engineering_convention_label"]
        == "SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT"
    )
    assert row892_transition["starting_position_contracts"] == "0"
    assert row892_transition["ending_position_contracts"] == "-1"
    assert row892_transition["same_session"] == "FALSE"
    assert row892_fill["fill_executed"] == "TRUE"
    assert (
        row892_fill["fill_rule"]
        == "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_SESSION_VALUATION_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
    )
    assert row892_fill["fill_candidate_close"] == "111.671875"
    assert row892_fill["fill_price"] == "111.671875"
    assert row892_fill["fill_quantity"] == "1"
    assert row892_fill["position_after_fill"] == "-1"
    assert row892_cost["commission_amount"] == "2.3"
    assert row892_cost["spread_cost_amount"] == "0.0"
    assert row892_cost["total_cost_amount"] == "2.3"
    assert row892_pnl["valuation_mark_timestamp_utc"] == "2023-02-28T22:00:00Z"
    assert row892_pnl["valuation_mark_close_price"] == "111.546875"
    assert row892_pnl["row_gross_pnl_amount"] == "125.0"
    assert row892_pnl["row_net_pnl_amount"] == "122.7"
    assert row892_pnl["ending_position_contracts"] == "-1"
    assert row892_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row1355_order = next(row for row in orders if row["row_index"] == "1355")
    row1355_no_market = next(row for row in no_market_rows if row["row_index"] == "1355")
    row1355_transition = next(row for row in transitions if row["row_index"] == "1355")
    row1355_fill = next(row for row in fills if row["row_index"] == "1355")
    row1355_cost = next(row for row in costs if row["row_index"] == "1355")
    row1355_pnl = next(row for row in pnl_rows if row["row_index"] == "1355")
    assert row1355_order["order_side"] == "BUY"
    assert row1355_order["order_quantity"] == "1"
    assert row1355_order["adjacent_target_position"] == "8"
    assert row1355_order["formula_limit_price"] == "114.49366645867451"
    assert row1355_order["limit_order_price"] == "114.484375"
    assert row1355_order["row_status"] == "LOCAL_ENGINEERING_SESSION_END_ADJACENT_LIMIT_VALUATION_GAP_ROW_EMITTED_NOT_RESULT"
    assert row1355_no_market["market_order_required"] == "FALSE"
    assert row1355_no_market["market_order_rows_emitted"] == "FALSE"
    assert row1355_no_market["market_fallback_status"] == "NOT_REQUIRED_LIMIT_ORDER_FILLED"
    assert (
        row1355_no_market["engineering_convention_label"]
        == "SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT"
    )
    assert row1355_transition["starting_position_contracts"] == "7"
    assert row1355_transition["ending_position_contracts"] == "8"
    assert row1355_transition["same_session"] == "FALSE"
    assert row1355_fill["fill_executed"] == "TRUE"
    assert (
        row1355_fill["fill_rule"]
        == "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_AVAILABLE_VALUATION_GAP_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
    )
    assert row1355_fill["fill_candidate_close"] == "114.46875"
    assert row1355_fill["fill_price"] == "114.484375"
    assert row1355_fill["fill_quantity"] == "1"
    assert row1355_fill["position_after_fill"] == "8"
    assert row1355_cost["commission_amount"] == "2.3"
    assert row1355_cost["spread_cost_amount"] == "0.0"
    assert row1355_cost["total_cost_amount"] == "2.3"
    assert row1355_pnl["valuation_mark_timestamp_utc"] == "2023-03-29T23:00:00Z"
    assert row1355_pnl["valuation_mark_close_price"] == "114.5"
    assert row1355_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row1355_pnl["row_gross_pnl_amount"] == "234.375"
    assert row1355_pnl["row_net_pnl_amount"] == "232.075"
    assert row1355_pnl["ending_position_contracts"] == "8"
    assert row1355_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row1356_order = next(row for row in orders if row["row_index"] == "1356")
    row1356_no_market = next(row for row in no_market_rows if row["row_index"] == "1356")
    row1356_transition = next(row for row in transitions if row["row_index"] == "1356")
    row1356_fill = next(row for row in fills if row["row_index"] == "1356")
    row1356_market_order = next(row for row in market_order_rows if row["row_index"] == "1356")
    row1356_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "1356")
    row1356_cost = next(row for row in costs if row["row_index"] == "1356")
    row1356_pnl = next(row for row in pnl_rows if row["row_index"] == "1356")
    assert row1356_order["order_side"] == "SELL"
    assert row1356_order["order_quantity"] == "2"
    assert row1356_order["adjacent_target_position"] == "7"
    assert row1356_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1356_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1356_no_market["market_order_required"] == "TRUE"
    assert row1356_no_market["market_order_rows_emitted"] == "TRUE"
    assert row1356_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row1356_transition["starting_position_contracts"] == "8"
    assert row1356_transition["ending_position_contracts"] == "6"
    assert row1356_transition["same_session"] == "TRUE"
    assert row1356_fill["fill_executed"] == "TRUE"
    assert row1356_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1356_fill["fill_candidate_close"] == "114.484375"
    assert row1356_fill["fill_price"] == "114.484375"
    assert row1356_fill["fill_quantity"] == "2"
    assert row1356_fill["position_after_fill"] == "6"
    assert row1356_market_order["current_position_before_order"] == "8"
    assert row1356_market_order["target_position_after_fill"] == "6"
    assert row1356_market_order["order_side"] == "SELL"
    assert row1356_market_order["order_quantity"] == "2"
    assert row1356_market_fill["fill_timestamp_utc"] == "2023-03-30T00:00:00Z"
    assert row1356_market_fill["fill_price"] == "114.484375"
    assert row1356_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1356_market_fill["fill_quantity"] == "2"
    assert row1356_market_fill["commission_amount"] == "4.6"
    assert row1356_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row1356_cost["order_cost_type"] == "MARKET_ORDER_SELL_BID_FILL_ACTUAL_COST_NOT_PNL"
    assert row1356_cost["commission_amount"] == "4.6"
    assert row1356_cost["spread_cost_amount"] == "0.0"
    assert row1356_cost["total_cost_amount"] == "4.6"
    assert row1356_cost["market_cost_accounting_convention"] == "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row1356_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_BID"
    assert row1356_cost["tbbo_quote_ts_event"] == "2023-03-30T00:00:00.099806785Z"
    assert row1356_cost["tbbo_bid_px"] == "114.484375"
    assert row1356_cost["tbbo_ask_px"] == "114.5"
    assert row1356_cost["tbbo_full_spread_points"] == "0.015625"
    assert row1356_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row1356_cost["tbbo_selected_spread_row_hash"] == "b64709b5d1d37a78c6a4507208d3ca0b159bb268eb5bd39d5b3be51fdcf8eaae"
    assert row1356_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row1356_pnl["valuation_mark_timestamp_utc"] == "2023-03-30T01:00:00Z"
    assert row1356_pnl["valuation_mark_close_price"] == "114.4375"
    assert row1356_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row1356_pnl["row_gross_pnl_amount"] == "-406.25"
    assert row1356_pnl["row_net_pnl_amount"] == "-410.85"
    assert row1356_pnl["ending_position_contracts"] == "6"
    assert row1356_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row1364_order = next(row for row in orders if row["row_index"] == "1364")
    row1364_no_market = next(row for row in no_market_rows if row["row_index"] == "1364")
    row1364_transition = next(row for row in transitions if row["row_index"] == "1364")
    row1364_fill = next(row for row in fills if row["row_index"] == "1364")
    row1364_market_order = next(row for row in market_order_rows if row["row_index"] == "1364")
    row1364_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "1364")
    row1364_cost = next(row for row in costs if row["row_index"] == "1364")
    row1364_pnl = next(row for row in pnl_rows if row["row_index"] == "1364")
    assert row1364_order["order_side"] == "SELL"
    assert row1364_order["order_quantity"] == "2"
    assert row1364_order["adjacent_target_position"] == "5"
    assert row1364_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1364_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1364_no_market["market_order_required"] == "TRUE"
    assert row1364_no_market["market_order_rows_emitted"] == "TRUE"
    assert row1364_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row1364_transition["starting_position_contracts"] == "6"
    assert row1364_transition["ending_position_contracts"] == "4"
    assert row1364_transition["same_session"] == "TRUE"
    assert row1364_fill["fill_executed"] == "TRUE"
    assert row1364_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1364_fill["fill_candidate_close"] == "114.640625"
    assert row1364_fill["fill_price"] == "114.640625"
    assert row1364_fill["fill_quantity"] == "2"
    assert row1364_fill["position_after_fill"] == "4"
    assert row1364_market_order["current_position_before_order"] == "6"
    assert row1364_market_order["target_position_after_fill"] == "4"
    assert row1364_market_order["order_side"] == "SELL"
    assert row1364_market_order["order_quantity"] == "2"
    assert row1364_market_fill["fill_timestamp_utc"] == "2023-03-30T08:00:00Z"
    assert row1364_market_fill["fill_price"] == "114.640625"
    assert row1364_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1364_market_fill["fill_quantity"] == "2"
    assert row1364_market_fill["commission_amount"] == "4.6"
    assert row1364_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row1364_cost["order_cost_type"] == "MARKET_ORDER_SELL_BID_FILL_ACTUAL_COST_NOT_PNL"
    assert row1364_cost["commission_amount"] == "4.6"
    assert row1364_cost["spread_cost_amount"] == "0.0"
    assert row1364_cost["total_cost_amount"] == "4.6"
    assert row1364_cost["market_cost_accounting_convention"] == "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row1364_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_BID"
    assert row1364_cost["tbbo_quote_ts_event"] == "2023-03-30T07:59:58.203532779Z"
    assert row1364_cost["tbbo_bid_px"] == "114.640625"
    assert row1364_cost["tbbo_ask_px"] == "114.65625"
    assert row1364_cost["tbbo_full_spread_points"] == "0.015625"
    assert row1364_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row1364_cost["tbbo_selected_spread_row_hash"] == "80dd0dd1dc186292ef56dab2d4802e553a95a20ea71e72b6317d64c0db64732e"
    assert row1364_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row1364_pnl["valuation_mark_timestamp_utc"] == "2023-03-30T09:00:00Z"
    assert row1364_pnl["valuation_mark_close_price"] == "114.453125"
    assert row1364_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row1364_pnl["row_gross_pnl_amount"] == "-750.0"
    assert row1364_pnl["row_net_pnl_amount"] == "-754.6"
    assert row1364_pnl["ending_position_contracts"] == "4"
    assert row1364_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row1366_order = next(row for row in orders if row["row_index"] == "1366")
    row1366_no_market = next(row for row in no_market_rows if row["row_index"] == "1366")
    row1366_transition = next(row for row in transitions if row["row_index"] == "1366")
    row1366_fill = next(row for row in fills if row["row_index"] == "1366")
    row1366_market_order = next(row for row in market_order_rows if row["row_index"] == "1366")
    row1366_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "1366")
    row1366_cost = next(row for row in costs if row["row_index"] == "1366")
    row1366_pnl = next(row for row in pnl_rows if row["row_index"] == "1366")
    assert row1366_order["order_side"] == "BUY"
    assert row1366_order["order_quantity"] == "2"
    assert row1366_order["adjacent_target_position"] == "5"
    assert row1366_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1366_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1366_no_market["market_order_required"] == "TRUE"
    assert row1366_no_market["market_order_rows_emitted"] == "TRUE"
    assert row1366_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row1366_transition["starting_position_contracts"] == "4"
    assert row1366_transition["ending_position_contracts"] == "6"
    assert row1366_transition["same_session"] == "TRUE"
    assert row1366_fill["fill_executed"] == "TRUE"
    assert row1366_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1366_fill["fill_candidate_close"] == "114.453125"
    assert row1366_fill["fill_price"] == "114.46875"
    assert row1366_fill["fill_quantity"] == "2"
    assert row1366_fill["position_after_fill"] == "6"
    assert row1366_market_order["current_position_before_order"] == "4"
    assert row1366_market_order["target_position_after_fill"] == "6"
    assert row1366_market_order["order_side"] == "BUY"
    assert row1366_market_order["order_quantity"] == "2"
    assert row1366_market_fill["fill_timestamp_utc"] == "2023-03-30T10:00:00Z"
    assert row1366_market_fill["fill_price"] == "114.46875"
    assert row1366_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1366_market_fill["fill_quantity"] == "2"
    assert row1366_market_fill["commission_amount"] == "4.6"
    assert row1366_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_ASK_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row1366_cost["order_cost_type"] == "MARKET_ORDER_BUY_ASK_FILL_ACTUAL_COST_NOT_PNL"
    assert row1366_cost["commission_amount"] == "4.6"
    assert row1366_cost["spread_cost_amount"] == "0.0"
    assert row1366_cost["total_cost_amount"] == "4.6"
    assert row1366_cost["market_cost_accounting_convention"] == "ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row1366_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_ASK"
    assert row1366_cost["tbbo_quote_ts_event"] == "2023-03-30T09:59:58.009461457Z"
    assert row1366_cost["tbbo_bid_px"] == "114.453125"
    assert row1366_cost["tbbo_ask_px"] == "114.46875"
    assert row1366_cost["tbbo_full_spread_points"] == "0.015625"
    assert row1366_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row1366_cost["tbbo_selected_spread_row_hash"] == "ee5b5d7473e19018e90ec87261355c89fe16bd2a25fcbd44e29f9208e1339fa6"
    assert row1366_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row1366_pnl["valuation_mark_timestamp_utc"] == "2023-03-30T11:00:00Z"
    assert row1366_pnl["valuation_mark_close_price"] == "114.484375"
    assert row1366_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row1366_pnl["row_gross_pnl_amount"] == "156.25"
    assert row1366_pnl["row_net_pnl_amount"] == "151.65"
    assert row1366_pnl["ending_position_contracts"] == "6"
    assert row1366_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row1369_order = next(row for row in orders if row["row_index"] == "1369")
    row1369_no_market = next(row for row in no_market_rows if row["row_index"] == "1369")
    row1369_transition = next(row for row in transitions if row["row_index"] == "1369")
    row1369_fill = next(row for row in fills if row["row_index"] == "1369")
    row1369_market_order = next(row for row in market_order_rows if row["row_index"] == "1369")
    row1369_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "1369")
    row1369_cost = next(row for row in costs if row["row_index"] == "1369")
    row1369_pnl = next(row for row in pnl_rows if row["row_index"] == "1369")
    assert row1369_order["order_side"] == "SELL"
    assert row1369_order["order_quantity"] == "2"
    assert row1369_order["adjacent_target_position"] == "5"
    assert row1369_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1369_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1369_no_market["market_order_required"] == "TRUE"
    assert row1369_no_market["market_order_rows_emitted"] == "TRUE"
    assert row1369_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row1369_transition["starting_position_contracts"] == "6"
    assert row1369_transition["ending_position_contracts"] == "4"
    assert row1369_transition["same_session"] == "TRUE"
    assert row1369_fill["fill_executed"] == "TRUE"
    assert row1369_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1369_fill["fill_candidate_close"] == "114.328125"
    assert row1369_fill["fill_price"] == "114.3125"
    assert row1369_fill["fill_quantity"] == "2"
    assert row1369_fill["position_after_fill"] == "4"
    assert row1369_market_order["current_position_before_order"] == "6"
    assert row1369_market_order["target_position_after_fill"] == "4"
    assert row1369_market_order["order_side"] == "SELL"
    assert row1369_market_order["order_quantity"] == "2"
    assert row1369_market_fill["fill_timestamp_utc"] == "2023-03-30T13:00:00Z"
    assert row1369_market_fill["fill_price"] == "114.3125"
    assert row1369_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1369_market_fill["fill_quantity"] == "2"
    assert row1369_market_fill["commission_amount"] == "4.6"
    assert row1369_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row1369_cost["order_cost_type"] == "MARKET_ORDER_SELL_BID_FILL_ACTUAL_COST_NOT_PNL"
    assert row1369_cost["commission_amount"] == "4.6"
    assert row1369_cost["spread_cost_amount"] == "0.0"
    assert row1369_cost["total_cost_amount"] == "4.6"
    assert row1369_cost["market_cost_accounting_convention"] == "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row1369_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_BID"
    assert row1369_cost["tbbo_quote_ts_event"] == "2023-03-30T12:59:58.996330651Z"
    assert row1369_cost["tbbo_bid_px"] == "114.3125"
    assert row1369_cost["tbbo_ask_px"] == "114.328125"
    assert row1369_cost["tbbo_full_spread_points"] == "0.015625"
    assert row1369_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row1369_cost["tbbo_selected_spread_row_hash"] == "1b8b50fe5aed31312922f4d0bbc19e3c79e6dd6b8bf63aff90b43c7f4ba7f447"
    assert row1369_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row1369_pnl["valuation_mark_timestamp_utc"] == "2023-03-30T14:00:00Z"
    assert row1369_pnl["valuation_mark_close_price"] == "114.390625"
    assert row1369_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row1369_pnl["row_gross_pnl_amount"] == "218.75"
    assert row1369_pnl["row_net_pnl_amount"] == "214.15"
    assert row1369_pnl["ending_position_contracts"] == "4"
    assert row1369_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row1370_order = next(row for row in orders if row["row_index"] == "1370")
    row1370_no_market = next(row for row in no_market_rows if row["row_index"] == "1370")
    row1370_transition = next(row for row in transitions if row["row_index"] == "1370")
    row1370_fill = next(row for row in fills if row["row_index"] == "1370")
    row1370_market_order = next(row for row in market_order_rows if row["row_index"] == "1370")
    row1370_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "1370")
    row1370_cost = next(row for row in costs if row["row_index"] == "1370")
    row1370_pnl = next(row for row in pnl_rows if row["row_index"] == "1370")
    assert row1370_order["order_side"] == "BUY"
    assert row1370_order["order_quantity"] == "4"
    assert row1370_order["adjacent_target_position"] == "5"
    assert row1370_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1370_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1370_no_market["market_order_required"] == "TRUE"
    assert row1370_no_market["market_order_rows_emitted"] == "TRUE"
    assert row1370_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row1370_transition["starting_position_contracts"] == "4"
    assert row1370_transition["ending_position_contracts"] == "8"
    assert row1370_transition["same_session"] == "TRUE"
    assert row1370_fill["fill_executed"] == "TRUE"
    assert row1370_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1370_fill["fill_candidate_close"] == "114.390625"
    assert row1370_fill["fill_price"] == "114.40625"
    assert row1370_fill["fill_quantity"] == "4"
    assert row1370_fill["position_after_fill"] == "8"
    assert row1370_market_order["current_position_before_order"] == "4"
    assert row1370_market_order["target_position_after_fill"] == "8"
    assert row1370_market_order["order_side"] == "BUY"
    assert row1370_market_order["order_quantity"] == "4"
    assert row1370_market_fill["fill_timestamp_utc"] == "2023-03-30T14:00:00Z"
    assert row1370_market_fill["fill_price"] == "114.40625"
    assert row1370_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1370_market_fill["fill_quantity"] == "4"
    assert row1370_market_fill["commission_amount"] == "9.2"
    assert row1370_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_ASK_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row1370_cost["order_cost_type"] == "MARKET_ORDER_BUY_ASK_FILL_ACTUAL_COST_NOT_PNL"
    assert row1370_cost["commission_amount"] == "9.2"
    assert row1370_cost["spread_cost_amount"] == "0.0"
    assert row1370_cost["total_cost_amount"] == "9.2"
    assert row1370_cost["market_cost_accounting_convention"] == "ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row1370_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_ASK"
    assert row1370_cost["tbbo_quote_ts_event"] == "2023-03-30T13:59:59.466320757Z"
    assert row1370_cost["tbbo_bid_px"] == "114.390625"
    assert row1370_cost["tbbo_ask_px"] == "114.40625"
    assert row1370_cost["tbbo_full_spread_points"] == "0.015625"
    assert row1370_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row1370_cost["tbbo_selected_spread_row_hash"] == "c5360ecad0ad1b2afef1decafa17ce630484078a60c5b54d1eeb23c336f7aae3"
    assert row1370_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row1370_pnl["valuation_mark_timestamp_utc"] == "2023-03-30T15:00:00Z"
    assert row1370_pnl["valuation_mark_close_price"] == "114.46875"
    assert row1370_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row1370_pnl["row_gross_pnl_amount"] == "562.5"
    assert row1370_pnl["row_net_pnl_amount"] == "553.3"
    assert row1370_pnl["ending_position_contracts"] == "8"
    assert row1370_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row1374_order = next(row for row in orders if row["row_index"] == "1374")
    row1374_no_market = next(row for row in no_market_rows if row["row_index"] == "1374")
    row1374_transition = next(row for row in transitions if row["row_index"] == "1374")
    row1374_fill = next(row for row in fills if row["row_index"] == "1374")
    row1374_market_order = next(row for row in market_order_rows if row["row_index"] == "1374")
    row1374_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "1374")
    row1374_cost = next(row for row in costs if row["row_index"] == "1374")
    row1374_pnl = next(row for row in pnl_rows if row["row_index"] == "1374")
    assert row1374_order["order_side"] == "SELL"
    assert row1374_order["order_quantity"] == "2"
    assert row1374_order["adjacent_target_position"] == "6"
    assert row1374_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1374_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row1374_no_market["market_order_required"] == "TRUE"
    assert row1374_no_market["market_order_rows_emitted"] == "TRUE"
    assert row1374_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row1374_transition["starting_position_contracts"] == "7"
    assert row1374_transition["ending_position_contracts"] == "5"
    assert row1374_transition["same_session"] == "TRUE"
    assert row1374_fill["fill_executed"] == "TRUE"
    assert row1374_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1374_fill["fill_candidate_close"] == "114.515625"
    assert row1374_fill["fill_price"] == "114.515625"
    assert row1374_fill["fill_quantity"] == "2"
    assert row1374_fill["position_after_fill"] == "5"
    assert row1374_market_order["current_position_before_order"] == "7"
    assert row1374_market_order["target_position_after_fill"] == "5"
    assert row1374_market_order["order_side"] == "SELL"
    assert row1374_market_order["order_quantity"] == "2"
    assert row1374_market_fill["fill_timestamp_utc"] == "2023-03-30T18:00:00Z"
    assert row1374_market_fill["fill_price"] == "114.515625"
    assert row1374_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1374_market_fill["fill_quantity"] == "2"
    assert row1374_market_fill["commission_amount"] == "4.6"
    assert row1374_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row1374_cost["order_cost_type"] == "MARKET_ORDER_SELL_BID_FILL_ACTUAL_COST_NOT_PNL"
    assert row1374_cost["commission_amount"] == "4.6"
    assert row1374_cost["spread_cost_amount"] == "0.0"
    assert row1374_cost["total_cost_amount"] == "4.6"
    assert row1374_cost["market_cost_accounting_convention"] == "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row1374_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_BID"
    assert row1374_cost["tbbo_quote_ts_event"] == "2023-03-30T17:59:58.005200809Z"
    assert row1374_cost["tbbo_bid_px"] == "114.515625"
    assert row1374_cost["tbbo_ask_px"] == "114.53125"
    assert row1374_cost["tbbo_full_spread_points"] == "0.015625"
    assert row1374_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row1374_cost["tbbo_selected_spread_row_hash"] == "96731f4b012c9dcd8fb1fb5b3066902d14a8deb9b3b31da81b7e8d558a51a290"
    assert row1374_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row1374_pnl["valuation_mark_timestamp_utc"] == "2023-03-30T19:00:00Z"
    assert row1374_pnl["valuation_mark_close_price"] == "114.59375"
    assert row1374_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row1374_pnl["row_gross_pnl_amount"] == "390.625"
    assert row1374_pnl["row_net_pnl_amount"] == "386.025"
    assert row1374_pnl["ending_position_contracts"] == "5"
    assert row1374_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row959_market_order = next(row for row in market_order_rows if row["row_index"] == "959")
    row959_no_market = next(row for row in no_market_rows if row["row_index"] == "959")
    row959_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "959")
    row959_transition = next(row for row in transitions if row["row_index"] == "959")
    row959_fill = next(row for row in fills if row["row_index"] == "959")
    row959_cost = next(row for row in costs if row["row_index"] == "959")
    row959_pnl = next(row for row in pnl_rows if row["row_index"] == "959")
    assert row959_market_order["decision_timestamp_utc"] == "2023-03-03T21:00:00Z"
    assert row959_market_order["raw_symbol"] == "ZNM3"
    assert row959_market_order["current_position_before_order"] == "0"
    assert row959_market_order["target_position_after_fill"] == "-2"
    assert row959_market_order["order_side"] == "SELL"
    assert row959_market_order["order_quantity"] == "2"
    assert (
        row959_market_order["engineering_convention_label"]
        == "SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT"
    )
    assert row959_no_market["market_order_required"] == "TRUE"
    assert row959_no_market["market_order_rows_emitted"] == "TRUE"
    assert row959_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row959_market_fill["fill_timestamp_utc"] == "2023-03-03T22:00:00Z"
    assert row959_market_fill["fill_price"] == "111.140625"
    assert row959_market_fill["same_session"] == "FALSE"
    assert row959_market_fill["position_after_fill"] == "-2"
    assert row959_transition["same_session"] == "FALSE"
    assert row959_transition["ending_position_contracts"] == "-2"
    assert row959_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row959_fill["fill_price"] == "111.140625"
    assert row959_fill["position_after_fill"] == "-2"
    assert row959_cost["tbbo_quote_ts_event"] == "2023-03-03T21:59:59.523101291Z"
    assert row959_cost["tbbo_bid_px"] == "111.140625"
    assert row959_cost["tbbo_ask_px"] == "111.15625"
    assert row959_cost["commission_amount"] == "4.6"
    assert row959_pnl["valuation_mark_timestamp_utc"] == "2023-03-06T00:00:00Z"
    assert row959_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row959_pnl["row_gross_pnl_amount"] == "125.0"
    assert row959_pnl["row_net_pnl_amount"] == "120.4"
    assert row959_pnl["ending_position_contracts"] == "-2"
    row346_order = next(row for row in orders if row["row_index"] == "346")
    row346_no_market = next(row for row in no_market_rows if row["row_index"] == "346")
    row346_transition = next(row for row in transitions if row["row_index"] == "346")
    row346_fill = next(row for row in fills if row["row_index"] == "346")
    row346_cost = next(row for row in costs if row["row_index"] == "346")
    row346_pnl = next(row for row in pnl_rows if row["row_index"] == "346")
    assert row346_order["order_side"] == "SELL"
    assert row346_order["order_quantity"] == "1"
    assert row346_order["adjacent_target_position"] == "0"
    assert row346_order["formula_limit_price"] == "114.99998579656148"
    assert row346_order["limit_order_price"] == "115.0"
    assert row346_no_market["market_order_required"] == "FALSE"
    assert row346_no_market["market_order_rows_emitted"] == "FALSE"
    assert row346_no_market["market_fallback_status"] == "NOT_REQUIRED_LIMIT_ORDER_FILLED"
    assert row346_transition["starting_position_contracts"] == "1"
    assert row346_transition["ending_position_contracts"] == "0"
    assert row346_transition["same_session"] == "TRUE"
    assert row346_fill["fill_executed"] == "TRUE"
    assert row346_fill["fill_rule"] == "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL"
    assert row346_fill["fill_candidate_close"] == "115.03125"
    assert row346_fill["fill_price"] == "115.0"
    assert row346_fill["fill_quantity"] == "1"
    assert row346_fill["position_after_fill"] == "0"
    assert row346_cost["commission_amount"] == "2.3"
    assert row346_cost["spread_cost_amount"] == "0.0"
    assert row346_cost["total_cost_amount"] == "2.3"
    assert row346_pnl["valuation_mark_timestamp_utc"] == "2023-01-24T21:00:00Z"
    assert row346_pnl["valuation_mark_close_price"] == "115.0625"
    assert row346_pnl["row_gross_pnl_amount"] == "-31.25"
    assert row346_pnl["row_net_pnl_amount"] == "-33.55"
    assert row346_pnl["ending_position_contracts"] == "0"
    row436_order = next(row for row in orders if row["row_index"] == "436")
    row436_no_market = next(row for row in no_market_rows if row["row_index"] == "436")
    row436_transition = next(row for row in transitions if row["row_index"] == "436")
    row436_fill = next(row for row in fills if row["row_index"] == "436")
    row436_cost = next(row for row in costs if row["row_index"] == "436")
    row436_pnl = next(row for row in pnl_rows if row["row_index"] == "436")
    assert row436_order["order_side"] == "SELL"
    assert row436_order["order_quantity"] == "1"
    assert row436_order["adjacent_target_position"] == "23"
    assert row436_order["formula_limit_price"] == "114.29396275895618"
    assert row436_order["limit_order_price"] == "114.296875"
    assert row436_order["row_status"] == "LOCAL_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ROW_EMITTED_NOT_RESULT"
    assert row436_no_market["market_order_required"] == "FALSE"
    assert row436_no_market["market_order_rows_emitted"] == "FALSE"
    assert row436_no_market["market_fallback_status"] == "NOT_REQUIRED_LIMIT_ORDER_FILLED"
    assert (
        row436_no_market["engineering_convention_label"]
        == "SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT"
    )
    assert row436_transition["starting_position_contracts"] == "24"
    assert row436_transition["ending_position_contracts"] == "23"
    assert row436_transition["same_session"] == "FALSE"
    assert row436_fill["fill_executed"] == "TRUE"
    assert row436_fill["fill_rule"] == "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_WITH_SESSION_OPEN_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
    assert row436_fill["fill_candidate_close"] == "114.40625"
    assert row436_fill["fill_price"] == "114.296875"
    assert row436_fill["fill_quantity"] == "1"
    assert row436_fill["position_after_fill"] == "23"
    assert row436_cost["commission_amount"] == "2.3"
    assert row436_cost["spread_cost_amount"] == "0.0"
    assert row436_cost["total_cost_amount"] == "2.3"
    assert row436_pnl["valuation_mark_timestamp_utc"] == "2023-01-31T00:00:00Z"
    assert row436_pnl["valuation_mark_close_price"] == "114.34375"
    assert row436_pnl["ending_position_contracts"] == "23"
    assert row436_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row437_order = next(row for row in orders if row["row_index"] == "437")
    row437_no_market = next(row for row in no_market_rows if row["row_index"] == "437")
    row437_transition = next(row for row in transitions if row["row_index"] == "437")
    row437_fill = next(row for row in fills if row["row_index"] == "437")
    row437_market_order = next(row for row in market_order_rows if row["row_index"] == "437")
    row437_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "437")
    row437_cost = next(row for row in costs if row["row_index"] == "437")
    row437_pnl = next(row for row in pnl_rows if row["row_index"] == "437")
    assert row437_order["order_side"] == "SELL"
    assert row437_order["order_quantity"] == "4"
    assert row437_order["adjacent_target_position"] == "22"
    assert row437_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row437_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row437_no_market["market_order_required"] == "TRUE"
    assert row437_no_market["market_order_rows_emitted"] == "TRUE"
    assert row437_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row437_transition["starting_position_contracts"] == "23"
    assert row437_transition["ending_position_contracts"] == "19"
    assert row437_transition["same_session"] == "TRUE"
    assert row437_fill["fill_executed"] == "TRUE"
    assert row437_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row437_fill["fill_candidate_close"] == "114.390625"
    assert row437_fill["fill_price"] == "114.390625"
    assert row437_fill["fill_quantity"] == "4"
    assert row437_fill["position_after_fill"] == "19"
    assert row437_market_order["current_position_before_order"] == "23"
    assert row437_market_order["target_position_after_fill"] == "19"
    assert row437_market_order["order_side"] == "SELL"
    assert row437_market_order["order_quantity"] == "4"
    assert row437_market_fill["fill_timestamp_utc"] == "2023-01-31T01:00:00Z"
    assert row437_market_fill["fill_price"] == "114.390625"
    assert row437_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row437_market_fill["fill_quantity"] == "4"
    assert row437_market_fill["commission_amount"] == "9.2"
    assert row437_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row437_cost["order_cost_type"] == "MARKET_ORDER_SELL_BID_FILL_ACTUAL_COST_NOT_PNL"
    assert row437_cost["commission_amount"] == "9.2"
    assert row437_cost["spread_cost_amount"] == "0.0"
    assert row437_cost["total_cost_amount"] == "9.2"
    assert row437_cost["market_cost_accounting_convention"] == "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row437_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_BID"
    assert row437_cost["tbbo_quote_ts_event"] == "2023-01-31T00:59:58.560246105Z"
    assert row437_cost["tbbo_bid_px"] == "114.390625"
    assert row437_cost["tbbo_ask_px"] == "114.40625"
    assert row437_cost["tbbo_full_spread_points"] == "0.015625"
    assert row437_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row437_pnl["valuation_mark_timestamp_utc"] == "2023-01-31T02:00:00Z"
    assert row437_pnl["valuation_mark_close_price"] == "114.359375"
    assert row437_pnl["row_gross_pnl_amount"] == "484.375"
    assert row437_pnl["row_net_pnl_amount"] == "475.175"
    assert row437_pnl["ending_position_contracts"] == "19"
    assert row437_pnl["result_status"] == RESULT_STATUS
    assert row437_pnl["backtest_status"] == BACKTEST_STATUS
    assert row437_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row438_order = next(row for row in orders if row["row_index"] == "438")
    row438_no_market = next(row for row in no_market_rows if row["row_index"] == "438")
    row438_transition = next(row for row in transitions if row["row_index"] == "438")
    row438_fill = next(row for row in fills if row["row_index"] == "438")
    row438_market_order = next(row for row in market_order_rows if row["row_index"] == "438")
    row438_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "438")
    row438_cost = next(row for row in costs if row["row_index"] == "438")
    row438_pnl = next(row for row in pnl_rows if row["row_index"] == "438")
    assert row438_order["order_side"] == "SELL"
    assert row438_order["order_quantity"] == "3"
    assert row438_order["adjacent_target_position"] == "18"
    assert row438_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row438_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row438_no_market["market_order_required"] == "TRUE"
    assert row438_no_market["market_order_rows_emitted"] == "TRUE"
    assert row438_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row438_transition["starting_position_contracts"] == "19"
    assert row438_transition["ending_position_contracts"] == "16"
    assert row438_transition["same_session"] == "TRUE"
    assert row438_fill["fill_executed"] == "TRUE"
    assert row438_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row438_fill["fill_candidate_close"] == "114.359375"
    assert row438_fill["fill_price"] == "114.359375"
    assert row438_fill["fill_quantity"] == "3"
    assert row438_fill["position_after_fill"] == "16"
    assert row438_market_order["current_position_before_order"] == "19"
    assert row438_market_order["target_position_after_fill"] == "16"
    assert row438_market_order["order_side"] == "SELL"
    assert row438_market_order["order_quantity"] == "3"
    assert row438_market_fill["fill_timestamp_utc"] == "2023-01-31T02:00:00Z"
    assert row438_market_fill["fill_price"] == "114.359375"
    assert row438_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row438_market_fill["fill_quantity"] == "3"
    assert row438_market_fill["commission_amount"] == "6.8999999999999995"
    assert row438_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row438_cost["order_cost_type"] == "MARKET_ORDER_SELL_BID_FILL_ACTUAL_COST_NOT_PNL"
    assert row438_cost["commission_amount"] == "6.8999999999999995"
    assert row438_cost["spread_cost_amount"] == "0.0"
    assert row438_cost["total_cost_amount"] == "6.8999999999999995"
    assert row438_cost["market_cost_accounting_convention"] == "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row438_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_BID"
    assert row438_cost["tbbo_quote_ts_event"] == "2023-01-31T01:59:47.160185221Z"
    assert row438_cost["tbbo_bid_px"] == "114.359375"
    assert row438_cost["tbbo_ask_px"] == "114.375"
    assert row438_cost["tbbo_full_spread_points"] == "0.015625"
    assert row438_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row438_pnl["valuation_mark_timestamp_utc"] == "2023-01-31T03:00:00Z"
    assert row438_pnl["valuation_mark_close_price"] == "114.375"
    assert row438_pnl["row_gross_pnl_amount"] == "250.0"
    assert row438_pnl["row_net_pnl_amount"] == "243.1"
    assert row438_pnl["ending_position_contracts"] == "16"
    assert row438_pnl["result_status"] == RESULT_STATUS
    assert row438_pnl["backtest_status"] == BACKTEST_STATUS
    assert row438_pnl["source_faithful_evidence_claimed"] == "FALSE"
    row441_order = next(row for row in orders if row["row_index"] == "441")
    row441_no_market = next(row for row in no_market_rows if row["row_index"] == "441")
    row441_transition = next(row for row in transitions if row["row_index"] == "441")
    row441_fill = next(row for row in fills if row["row_index"] == "441")
    row441_market_order = next(row for row in market_order_rows if row["row_index"] == "441")
    row441_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "441")
    row441_cost = next(row for row in costs if row["row_index"] == "441")
    row441_pnl = next(row for row in pnl_rows if row["row_index"] == "441")
    assert row441_order["order_side"] == "SELL"
    assert row441_order["order_quantity"] == "3"
    assert row441_order["adjacent_target_position"] == "16"
    assert row441_order["formula_limit_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row441_order["limit_order_price"] == "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
    assert row441_no_market["market_order_required"] == "TRUE"
    assert row441_no_market["market_order_rows_emitted"] == "TRUE"
    assert row441_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row441_transition["starting_position_contracts"] == "17"
    assert row441_transition["ending_position_contracts"] == "14"
    assert row441_transition["same_session"] == "TRUE"
    assert row441_fill["fill_executed"] == "TRUE"
    assert row441_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row441_fill["fill_candidate_close"] == "114.359375"
    assert row441_fill["fill_price"] == "114.359375"
    assert row441_fill["fill_quantity"] == "3"
    assert row441_fill["position_after_fill"] == "14"
    assert row441_market_order["current_position_before_order"] == "17"
    assert row441_market_order["target_position_after_fill"] == "14"
    assert row441_market_order["order_side"] == "SELL"
    assert row441_market_order["order_quantity"] == "3"
    assert row441_market_fill["fill_timestamp_utc"] == "2023-01-31T05:00:00Z"
    assert row441_market_fill["fill_price"] == "114.359375"
    assert row441_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row441_market_fill["fill_quantity"] == "3"
    assert row441_market_fill["commission_amount"] == "6.8999999999999995"
    assert row441_market_fill["market_spread_cost_status"] == "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
    assert row441_cost["order_cost_type"] == "MARKET_ORDER_SELL_BID_FILL_ACTUAL_COST_NOT_PNL"
    assert row441_cost["commission_amount"] == "6.8999999999999995"
    assert row441_cost["spread_cost_amount"] == "0.0"
    assert row441_cost["total_cost_amount"] == "6.8999999999999995"
    assert row441_cost["market_cost_accounting_convention"] == "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
    assert row441_cost["spread_cost_reason"] == "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_BID"
    assert row441_cost["tbbo_quote_ts_event"] == "2023-01-31T04:57:05.652860819Z"
    assert row441_cost["tbbo_bid_px"] == "114.359375"
    assert row441_cost["tbbo_ask_px"] == "114.375"
    assert row441_cost["tbbo_full_spread_points"] == "0.015625"
    assert row441_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row441_cost["tbbo_selected_spread_row_hash"] == "7e3f3b721a197c7a49a0f26f854ab2978b67c2080b5941bbed12075c3c0530fc"
    assert row441_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    row547_order = next(row for row in orders if row["row_index"] == "547")
    row547_no_market = next(row for row in no_market_rows if row["row_index"] == "547")
    row547_market_order = next(row for row in market_order_rows if row["row_index"] == "547")
    row547_fill = next(row for row in fills if row["row_index"] == "547")
    row547_cost = next(row for row in costs if row["row_index"] == "547")
    row547_pnl = next(row for row in pnl_rows if row["row_index"] == "547")
    assert row547_order["order_side"] == "SELL"
    assert row547_order["order_quantity"] == "1"
    assert row547_order["adjacent_target_position"] == "25"
    assert row547_order["formula_limit_price"] == "NOT_APPLICABLE_CAP_BOUND_MARKET_ORDER_LIMIT_SIDE_NOT_PLACED"
    assert row547_order["limit_order_price"] == "NOT_APPLICABLE_CAP_BOUND_MARKET_ORDER_LIMIT_SIDE_NOT_PLACED"
    assert row547_no_market["market_order_required"] == "TRUE"
    assert row547_no_market["market_order_rows_emitted"] == "TRUE"
    assert row547_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row547_market_order["current_position_before_order"] == "26"
    assert row547_market_order["target_position_after_fill"] == "25"
    assert row547_market_order["order_side"] == "SELL"
    assert row547_market_order["order_quantity"] == "1"
    assert row547_market_order["trigger_source_condition"] == "BOOK_REQUIRED_CAP_BOUND_LIMIT_SIDE_NOT_PLACED"
    assert row547_fill["fill_executed"] == "TRUE"
    assert row547_fill["fill_rule"] == "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row547_fill["fill_candidate_close"] == "113.5625"
    assert row547_fill["fill_price"] == "113.546875"
    assert row547_fill["fill_quantity"] == "1"
    assert row547_fill["position_after_fill"] == "25"
    assert row547_cost["commission_amount"] == "2.3"
    assert row547_cost["spread_cost_amount"] == "0.0"
    assert row547_cost["total_cost_amount"] == "2.3"
    assert row547_cost["tbbo_quote_ts_event"] == "2023-02-07T00:59:55.061867017Z"
    assert row547_cost["tbbo_bid_px"] == "113.546875"
    assert row547_cost["tbbo_ask_px"] == "113.5625"
    assert row547_cost["tbbo_full_spread_points"] == "0.015625"
    assert row547_cost["tbbo_full_spread_value_per_contract"] == "15.625"
    assert row547_cost["tbbo_selected_spread_row_hash"] == "bdae1f6afb23c5b679e3ff560f9295ae36b3c753f7e7dc14713464a20ed1c13d"
    assert row547_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row547_pnl["valuation_mark_timestamp_utc"] == "2023-02-07T02:00:00Z"
    assert row547_pnl["ending_position_contracts"] == "25"
    assert row547_pnl["result_status"] == RESULT_STATUS
    assert row441_pnl["valuation_mark_timestamp_utc"] == "2023-01-31T06:00:00Z"
    assert row441_pnl["valuation_mark_close_price"] == "114.359375"
    assert row441_pnl["row_gross_pnl_amount"] == "0.0"
    assert row441_pnl["row_net_pnl_amount"] == "-6.8999999999999995"
    assert row441_pnl["ending_position_contracts"] == "14"
    assert row441_pnl["result_status"] == RESULT_STATUS
    assert row441_pnl["backtest_status"] == BACKTEST_STATUS
    assert row441_pnl["source_faithful_evidence_claimed"] == "FALSE"
    assert market_order_rows[:2] == [
        {
            "row_index": "1",
            "decision_timestamp_utc": "2023-01-03T00:00:00Z",
            "raw_symbol": "ZNH3",
            "current_position_before_order": "0",
            "target_position_after_fill": "2",
            "order_side": "BUY",
            "order_quantity": "2",
            "trigger_source_condition": "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT",
            "market_order_rows_emitted": "TRUE",
            "engineering_convention_label": "NOT_APPLICABLE",
            "order_status": "LOCAL_MARKET_ORDER_ROW_EMITTED_NOT_RESULT",
            "row_status": "LOCAL_MARKET_ORDER_ROW_EMITTED_NOT_RESULT",
            "row_hash": market_order_rows[0]["row_hash"],
        },
        {
            "row_index": "2",
            "decision_timestamp_utc": "2023-01-03T01:00:00Z",
            "raw_symbol": "ZNH3",
            "current_position_before_order": "2",
            "target_position_after_fill": "0",
            "order_side": "SELL",
            "order_quantity": "2",
            "trigger_source_condition": "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT",
            "market_order_rows_emitted": "TRUE",
            "engineering_convention_label": "NOT_APPLICABLE",
            "order_status": "LOCAL_MARKET_ORDER_ROW_EMITTED_NOT_RESULT",
            "row_status": "LOCAL_MARKET_ORDER_ROW_EMITTED_NOT_RESULT",
            "row_hash": market_order_rows[1]["row_hash"],
        },
    ]
    assert {
        key: market_fill_metadata_rows[0][key]
        for key in (
            "row_index",
            "fill_timestamp_utc",
            "raw_symbol",
            "order_side",
            "fill_quantity",
            "fill_price",
            "fill_price_provenance",
            "same_session",
            "roll_boundary_status",
            "working_state_before",
            "position_after_fill",
            "commission_per_contract",
            "commission_amount",
            "market_spread_cost_status",
            "pnl_emission_status",
            "row_status",
        )
    } == {
        "row_index": "1",
        "fill_timestamp_utc": "2023-01-03T01:00:00Z",
        "raw_symbol": "ZNH3",
        "order_side": "BUY",
        "fill_quantity": "2",
        "fill_price": "112.5625",
        "fill_price_provenance": "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE",
        "same_session": "TRUE",
        "roll_boundary_status": "NO_ROLL_BOUNDARY_SAME_RAW_SYMBOL",
        "working_state_before": "EMPTY_INITIAL_WORKING_STATE",
        "position_after_fill": "2",
        "commission_per_contract": "2.3",
        "commission_amount": "4.6",
        "market_spread_cost_status": "PASS_DATABENTO_TBBO_ASK_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL",
        "pnl_emission_status": "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
        "row_status": "LOCAL_MARKET_FILL_METADATA_ROW_EMITTED_NOT_RESULT",
    }
    assert {
        key: market_fill_metadata_rows[1][key]
        for key in (
            "row_index",
            "fill_timestamp_utc",
            "raw_symbol",
            "order_side",
            "fill_quantity",
            "fill_price",
            "fill_price_provenance",
            "same_session",
            "roll_boundary_status",
            "working_state_before",
            "position_after_fill",
            "commission_per_contract",
            "commission_amount",
            "market_spread_cost_status",
            "pnl_emission_status",
            "row_status",
        )
    } == {
        "row_index": "2",
        "fill_timestamp_utc": "2023-01-03T02:00:00Z",
        "raw_symbol": "ZNH3",
        "order_side": "SELL",
        "fill_quantity": "2",
        "fill_price": "112.578125",
        "fill_price_provenance": "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE",
        "same_session": "TRUE",
        "roll_boundary_status": "NO_ROLL_BOUNDARY_SAME_RAW_SYMBOL",
        "working_state_before": "EMPTY_INITIAL_WORKING_STATE",
        "position_after_fill": "0",
        "commission_per_contract": "2.3",
        "commission_amount": "4.6",
        "market_spread_cost_status": "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL",
        "pnl_emission_status": "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
        "row_status": "LOCAL_MARKET_FILL_METADATA_ROW_EMITTED_NOT_RESULT",
    }
    assert {
        key: costs[0][key]
        for key in (
            "row_index",
            "cost_policy_id",
            "order_cost_type",
            "commission_amount",
            "spread_cost_amount",
            "total_cost_amount",
            "currency",
            "market_cost_accounting_convention",
            "spread_cost_reason",
            "tbbo_quote_ts_event",
            "tbbo_bid_px",
            "tbbo_ask_px",
            "tbbo_full_spread_points",
            "tbbo_full_spread_value_per_contract",
            "tbbo_selected_spread_row_hash",
            "tbbo_selected_spread_ledger_sha256",
            "row_status",
        )
    } == {
        "row_index": "1",
        "cost_policy_id": "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11",
        "order_cost_type": "MARKET_ORDER_BUY_ASK_FILL_ACTUAL_COST_NOT_PNL",
        "commission_amount": "4.6",
        "spread_cost_amount": "0.0",
        "total_cost_amount": "4.6",
        "currency": "USD",
        "market_cost_accounting_convention": "ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST",
        "spread_cost_reason": "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_ASK",
        "tbbo_quote_ts_event": "2023-01-03T00:59:57.009985Z",
        "tbbo_bid_px": "112.546875",
        "tbbo_ask_px": "112.5625",
        "tbbo_full_spread_points": "0.015625",
        "tbbo_full_spread_value_per_contract": "15.625",
        "tbbo_selected_spread_row_hash": "7f1ad53f2345815abed6a4ce3ff9ef7f94fbafd5ed9a779ab72ab79dc8e9277c",
                "tbbo_selected_spread_ledger_sha256": _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME),
        "row_status": "LOCAL_MARKET_ORDER_ACTUAL_COST_ROW_EMITTED_NOT_PNL_NOT_RESULT",
    }
    assert {
        key: costs[1][key]
        for key in (
            "row_index",
            "cost_policy_id",
            "order_cost_type",
            "commission_amount",
            "spread_cost_amount",
            "total_cost_amount",
            "currency",
            "market_cost_accounting_convention",
            "spread_cost_reason",
            "tbbo_quote_ts_event",
            "tbbo_bid_px",
            "tbbo_ask_px",
            "tbbo_full_spread_points",
            "tbbo_full_spread_value_per_contract",
            "tbbo_selected_spread_row_hash",
            "tbbo_selected_spread_ledger_sha256",
            "row_status",
        )
    } == {
        "row_index": "2",
        "cost_policy_id": "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11",
        "order_cost_type": "MARKET_ORDER_SELL_BID_FILL_ACTUAL_COST_NOT_PNL",
        "commission_amount": "4.6",
        "spread_cost_amount": "0.0",
        "total_cost_amount": "4.6",
        "currency": "USD",
        "market_cost_accounting_convention": "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST",
        "spread_cost_reason": "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_BID",
        "tbbo_quote_ts_event": "2023-01-03T01:59:56.651440427Z",
        "tbbo_bid_px": "112.578125",
        "tbbo_ask_px": "112.59375",
        "tbbo_full_spread_points": "0.015625",
        "tbbo_full_spread_value_per_contract": "15.625",
        "tbbo_selected_spread_row_hash": "6b466a09838fe4aa0745bc7d3bae9c30c6f28f2966e407aae3b742f69db506b6",
        "tbbo_selected_spread_ledger_sha256": _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME),
        "row_status": "LOCAL_MARKET_ORDER_ACTUAL_COST_ROW_EMITTED_NOT_PNL_NOT_RESULT",
    }
    row303_market_order = next(row for row in market_order_rows if row["row_index"] == "303")
    row303_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "303")
    assert row303_market_order["decision_timestamp_utc"] == "2023-01-20T20:00:00Z"
    assert row303_market_order["current_position_before_order"] == "5"
    assert row303_market_order["target_position_after_fill"] == "7"
    assert row303_market_order["order_side"] == "BUY"
    assert row303_market_order["order_quantity"] == "2"
    assert row303_market_fill["fill_timestamp_utc"] == "2023-01-20T21:00:00Z"
    assert row303_market_fill["fill_price"] == "115.03125"
    assert row303_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row303_market_fill["same_session"] == "TRUE"
    row304_market_order = next(row for row in market_order_rows if row["row_index"] == "304")
    row304_no_market = next(row for row in no_market_rows if row["row_index"] == "304")
    row304_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "304")
    row304_transition = next(row for row in transitions if row["row_index"] == "304")
    row304_fill = next(row for row in fills if row["row_index"] == "304")
    row304_cost = next(row for row in costs if row["row_index"] == "304")
    row304_pnl = next(row for row in pnl_rows if row["row_index"] == "304")
    assert row304_market_order["decision_timestamp_utc"] == "2023-01-20T21:00:00Z"
    assert row304_market_order["current_position_before_order"] == "7"
    assert row304_market_order["target_position_after_fill"] == "9"
    assert row304_market_order["order_side"] == "BUY"
    assert row304_market_order["order_quantity"] == "2"
    assert row304_market_order["engineering_convention_label"] == "SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row304_market_order["order_status"] == "LOCAL_ENGINEERING_SESSION_OPEN_MARKET_RESET_MARKET_ORDER_ROW_EMITTED_NOT_RESULT"
    assert row304_no_market["market_order_required"] == "TRUE"
    assert row304_no_market["market_order_rows_emitted"] == "TRUE"
    assert row304_no_market["engineering_convention_label"] == "SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row304_market_fill["fill_timestamp_utc"] == "2023-01-20T22:00:00Z"
    assert row304_market_fill["fill_price"] == "115.0625"
    assert row304_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row304_market_fill["same_session"] == "FALSE"
    assert row304_market_fill["position_after_fill"] == "9"
    assert row304_transition["same_session"] == "FALSE"
    assert row304_transition["ending_position_contracts"] == "9"
    assert row304_fill["fill_price"] == "115.0625"
    assert row304_fill["position_after_fill"] == "9"
    assert row304_cost["tbbo_quote_ts_event"] == "2023-01-20T21:59:59.924187905Z"
    assert row304_cost["tbbo_bid_px"] == "115.046875"
    assert row304_cost["tbbo_ask_px"] == "115.0625"
    assert row304_cost["commission_amount"] == "4.6"
    assert row304_pnl["valuation_mark_timestamp_utc"] == "2023-01-23T00:00:00Z"
    assert row304_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row304_pnl["existing_position_gross_pnl"] == "-109.375"
    assert row304_pnl["fill_gross_pnl"] == "-62.5"
    assert row304_pnl["row_gross_pnl_amount"] == "-171.875"
    assert row304_pnl["row_net_pnl_amount"] == "-176.475"
    assert row304_pnl["cumulative_net_pnl_amount"] == "5897.225"
    row391_market_order = next(row for row in market_order_rows if row["row_index"] == "391")
    row391_no_market = next(row for row in no_market_rows if row["row_index"] == "391")
    row391_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "391")
    row391_transition = next(row for row in transitions if row["row_index"] == "391")
    row391_fill = next(row for row in fills if row["row_index"] == "391")
    row391_cost = next(row for row in costs if row["row_index"] == "391")
    row391_pnl = next(row for row in pnl_rows if row["row_index"] == "391")
    assert row391_market_order["decision_timestamp_utc"] == "2023-01-26T20:00:00Z"
    assert row391_market_order["current_position_before_order"] == "4"
    assert row391_market_order["target_position_after_fill"] == "12"
    assert row391_market_order["order_side"] == "BUY"
    assert row391_market_order["order_quantity"] == "8"
    assert row391_market_order["engineering_convention_label"] == "NOT_APPLICABLE"
    assert row391_no_market["market_order_required"] == "TRUE"
    assert row391_no_market["market_order_rows_emitted"] == "TRUE"
    assert row391_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert row391_no_market["engineering_convention_label"] == "NOT_APPLICABLE"
    assert row391_market_fill["fill_timestamp_utc"] == "2023-01-26T21:00:00Z"
    assert row391_market_fill["fill_price"] == "114.828125"
    assert row391_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row391_market_fill["same_session"] == "TRUE"
    assert row391_market_fill["fill_quantity"] == "8"
    assert row391_market_fill["position_after_fill"] == "12"
    assert row391_market_fill["commission_amount"] == "18.4"
    assert row391_transition["starting_position_contracts"] == "4"
    assert row391_transition["ending_position_contracts"] == "12"
    assert row391_transition["same_session"] == "TRUE"
    assert row391_fill["fill_price"] == "114.828125"
    assert row391_fill["fill_quantity"] == "8"
    assert row391_fill["position_after_fill"] == "12"
    assert row391_cost["tbbo_quote_ts_event"] == "2023-01-26T20:59:59.902217027Z"
    assert row391_cost["tbbo_bid_px"] == "114.8125"
    assert row391_cost["tbbo_ask_px"] == "114.828125"
    assert row391_cost["commission_amount"] == "18.4"
    assert row391_cost["spread_cost_amount"] == "0.0"
    assert row391_cost["total_cost_amount"] == "18.4"
    assert row391_cost["tbbo_selected_spread_row_hash"] == "3d2b58d698092b8f1971462ab84233025254f318a9fb1b95536ca8de7b5088ec"
    assert row391_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row391_pnl["valuation_mark_timestamp_utc"] == "2023-01-26T22:00:00Z"
    assert row391_pnl["valuation_mark_close_price"] == "114.8125"
    assert row391_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row391_pnl["fill_gross_pnl"] == "-125.0"
    assert row391_pnl["row_net_pnl_amount"] == "-143.4"
    assert row391_pnl["cumulative_net_pnl_amount"] == "8060.075"
    assert row391_pnl["ending_position_contracts"] == "12"
    row1113_market_order = next(row for row in market_order_rows if row["row_index"] == "1113")
    row1113_no_market = next(row for row in no_market_rows if row["row_index"] == "1113")
    row1113_market_fill = next(row for row in market_fill_metadata_rows if row["row_index"] == "1113")
    row1113_transition = next(row for row in transitions if row["row_index"] == "1113")
    row1113_fill = next(row for row in fills if row["row_index"] == "1113")
    row1113_cost = next(row for row in costs if row["row_index"] == "1113")
    row1113_pnl = next(row for row in pnl_rows if row["row_index"] == "1113")
    assert row1113_market_order["decision_timestamp_utc"] == "2023-03-14T20:00:00Z"
    assert row1113_market_order["current_position_before_order"] == "-17"
    assert row1113_market_order["target_position_after_fill"] == "-15"
    assert row1113_market_order["order_side"] == "BUY"
    assert row1113_market_order["order_quantity"] == "2"
    assert (
        row1113_market_order["engineering_convention_label"]
        == "SOURCE_NATIVE_ENGINEERING_SESSION_END_MARKET_ORDER_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT"
    )
    assert row1113_no_market["market_order_required"] == "TRUE"
    assert row1113_no_market["market_order_rows_emitted"] == "TRUE"
    assert row1113_no_market["market_fallback_status"] == "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    assert (
        row1113_no_market["engineering_convention_label"]
        == "SOURCE_NATIVE_ENGINEERING_SESSION_END_MARKET_ORDER_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT"
    )
    assert row1113_market_fill["fill_timestamp_utc"] == "2023-03-14T21:00:00Z"
    assert row1113_market_fill["fill_price"] == "113.46875"
    assert row1113_market_fill["fill_price_provenance"] == "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
    assert row1113_market_fill["same_session"] == "TRUE"
    assert row1113_market_fill["fill_quantity"] == "2"
    assert row1113_market_fill["position_after_fill"] == "-15"
    assert row1113_transition["starting_position_contracts"] == "-17"
    assert row1113_transition["ending_position_contracts"] == "-15"
    assert row1113_transition["same_session"] == "TRUE"
    assert row1113_fill["fill_price"] == "113.46875"
    assert row1113_fill["fill_quantity"] == "2"
    assert row1113_fill["position_after_fill"] == "-15"
    assert row1113_cost["tbbo_quote_ts_event"] == "2023-03-14T20:59:59.840382723Z"
    assert row1113_cost["tbbo_bid_px"] == "113.453125"
    assert row1113_cost["tbbo_ask_px"] == "113.46875"
    assert row1113_cost["commission_amount"] == "4.6"
    assert row1113_cost["spread_cost_amount"] == "0.0"
    assert row1113_cost["total_cost_amount"] == "4.6"
    assert row1113_cost["tbbo_selected_spread_row_hash"] == "e7fd6c0b749fcb1669ab0692e34b050b0e361180e429a39551a2ba9d8c2b9ee0"
    assert row1113_cost["tbbo_selected_spread_ledger_sha256"] == _sha256(COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME)
    assert row1113_pnl["valuation_mark_timestamp_utc"] == "2023-03-14T23:00:00Z"
    assert row1113_pnl["valuation_mark_close_price"] == "113.515625"
    assert row1113_pnl["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
    assert row1113_pnl["fill_gross_pnl"] == "93.75"
    assert row1113_pnl["row_net_pnl_amount"] == "-707.725"
    assert row1113_pnl["ending_position_contracts"] == "-15"
    assert {
        key: pnl_rows[0][key]
        for key in (
            "row_index",
            "valuation_mark_timestamp_utc",
            "valuation_mark_close_price",
            "valuation_convention_label",
            "existing_position_gross_pnl",
            "fill_gross_pnl",
            "row_gross_pnl_amount",
            "row_net_pnl_amount",
            "cumulative_gross_pnl_amount",
            "cumulative_commission_amount",
            "cumulative_spread_amount",
            "cumulative_net_pnl_amount",
            "ending_position_contracts",
            "result_status",
            "backtest_status",
            "pnl_evaluation_status",
            "source_faithful_evidence_claimed",
            "row_status",
        )
    } == {
        "row_index": "1",
        "valuation_mark_timestamp_utc": "2023-01-03T02:00:00Z",
        "valuation_mark_close_price": "112.59375",
        "valuation_convention_label": "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT",
        "existing_position_gross_pnl": "0.0",
        "fill_gross_pnl": "62.5",
        "row_gross_pnl_amount": "62.5",
        "row_net_pnl_amount": "57.9",
        "cumulative_gross_pnl_amount": "62.5",
        "cumulative_commission_amount": "4.6",
        "cumulative_spread_amount": "0.0",
        "cumulative_net_pnl_amount": "57.9",
        "ending_position_contracts": "2",
        "result_status": RESULT_STATUS,
        "backtest_status": BACKTEST_STATUS,
        "pnl_evaluation_status": "MECHANICAL_PNL_ROW_CONSTRUCTION_ONLY_NOT_RESULT_INTERPRETATION",
        "source_faithful_evidence_claimed": "FALSE",
        "row_status": "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
    }
    assert {
        key: pnl_rows[1][key]
        for key in (
            "row_index",
            "valuation_mark_timestamp_utc",
            "valuation_mark_close_price",
            "valuation_convention_label",
            "existing_position_gross_pnl",
            "fill_gross_pnl",
            "row_gross_pnl_amount",
            "row_net_pnl_amount",
            "cumulative_gross_pnl_amount",
            "cumulative_commission_amount",
            "cumulative_spread_amount",
            "cumulative_net_pnl_amount",
            "ending_position_contracts",
            "result_status",
            "backtest_status",
            "pnl_evaluation_status",
            "source_faithful_evidence_claimed",
            "row_status",
        )
    } == {
        "row_index": "2",
        "valuation_mark_timestamp_utc": "2023-01-03T03:00:00Z",
        "valuation_mark_close_price": "112.625",
        "valuation_convention_label": "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT",
        "existing_position_gross_pnl": "62.5",
        "fill_gross_pnl": "-93.75",
        "row_gross_pnl_amount": "-31.25",
        "row_net_pnl_amount": "-35.85",
        "cumulative_gross_pnl_amount": "31.25",
        "cumulative_commission_amount": "9.2",
        "cumulative_spread_amount": "0.0",
        "cumulative_net_pnl_amount": "22.05",
        "ending_position_contracts": "0",
        "result_status": RESULT_STATUS,
        "backtest_status": BACKTEST_STATUS,
        "pnl_evaluation_status": "MECHANICAL_PNL_ROW_CONSTRUCTION_ONLY_NOT_RESULT_INTERPRETATION",
        "source_faithful_evidence_claimed": "FALSE",
        "row_status": "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
    }
    assert test_bundle.final_position_contracts == 3
    assert test_bundle.cumulative_gross_pnl_amount == -98750.0
    assert test_bundle.cumulative_commission_amount == 2881.9000000000005
    assert test_bundle.cumulative_spread_amount == 0.0
    assert test_bundle.cumulative_net_pnl_amount == -101631.9


def test_2023_test_run_writes_hash_bound_metadata(test_bundle):
    evidence = _json(RUN_ROOT, "evidence_manifest.json")
    trusted = _json(RUN_ROOT, "trusted_bundle.json")
    sha_rows = _rows(RUN_ROOT, "SHA256SUMS.csv")

    assert evidence["run_manifest_hash"] == _sha256(RUN_ROOT / "run_manifest.json")
    assert trusted["run_manifest_hash"] == _sha256(RUN_ROOT / "run_manifest.json")
    assert trusted["evidence_manifest_hash"] == _sha256(RUN_ROOT / "evidence_manifest.json")
    assert trusted["source_faithful_evidence_claimed"] is False
    assert test_bundle.run_manifest_hash == _sha256(RUN_ROOT / "run_manifest.json")
    assert test_bundle.evidence_manifest_hash == _sha256(RUN_ROOT / "evidence_manifest.json")
    assert test_bundle.trusted_bundle_hash == _sha256(RUN_ROOT / "trusted_bundle.json")
    for row in sha_rows:
        assert row["sha256"] == _sha256(RUN_ROOT / row["relative_path"])


def test_2023_test_run_rejects_out_of_scope_paths(tmp_path, test_manifest):
    del test_manifest
    from carver.spine.s27_v2_replay.test_mechanical_run import TestMechanicalRunConfig

    with pytest.raises(CarverBlocked, match="locked to the declared local 2023 TEST pack"):
        run_2023_test_mechanical_artifacts(TestMechanicalRunConfig(input_pack_path=str(tmp_path), output_root=str(RUN_ROOT)))
    with pytest.raises(CarverBlocked, match="output root is locked"):
        run_2023_test_mechanical_artifacts(TestMechanicalRunConfig(input_pack_path=str(PACK_ROOT), output_root=str(tmp_path)))


def test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only():
    bundle = discover_2023_test_market_order_tbbo_requirements()
    manifest = _json(TBBO_REQUIREMENTS_ROOT, "market_order_tbbo_requirements_manifest.json")
    rows = _rows(TBBO_REQUIREMENTS_ROOT, "market_order_tbbo_requirements.csv")
    sha_rows = _rows(TBBO_REQUIREMENTS_ROOT, "market_order_tbbo_requirements_sha256.csv")

    bundle.validate()
    assert manifest["provider_api_access"] == "NO"
    assert manifest["downloads"] == "NO"
    assert manifest["result_interpretation"] == "NO"
    assert manifest["source_faithful_evidence_claim"] == "NO"
    assert bundle.total_market_order_rows == len(rows)
    assert bundle.total_market_order_rows == 272
    assert bundle.missing_tbbo_requirement_count == 17
    assert bundle.already_bound_tbbo_count == 255
    assert rows[0]["row_index"] == "1"
    assert rows[0]["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE"
    assert rows[1]["row_index"] == "2"
    assert rows[1]["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE"
    assert any(row["row_index"] == "353" and row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE" for row in rows)
    assert any(row["row_index"] == "437" and row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE" for row in rows)
    assert any(row["row_index"] == "438" and row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE" for row in rows)
    assert any(row["row_index"] == "439" and row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE" for row in rows)
    assert any(row["row_index"] == "547" and row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE" for row in rows)
    assert any(row["row_index"] == "554" and row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE" for row in rows)
    assert {row["tbbo_requirement_status"] for row in rows} == {
        "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE",
        "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE",
    }
    assert all(row["decision_timestamp_utc"].startswith("2023-") for row in rows)
    assert all(row["fill_candidate_timestamp_utc"].startswith("2023-") for row in rows)
    assert all(row["source_faithful_evidence_claimed"] == "FALSE" for row in rows)
    bound_rows = [row for row in rows if row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE"]
    missing_rows = [row for row in rows if row["tbbo_requirement_status"] == "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"]
    assert [row["row_index"] for row in missing_rows] == [
        "1378",
        "1390",
        "1395",
        "1400",
        "1402",
        "1409",
        "1503",
        "1504",
        "1505",
        "1519",
        "1520",
        "1527",
        "1535",
        "1536",
        "1540",
        "1542",
        "1544",
    ]
    assert all(row["bound_tbbo_selected_spread_row_hash"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in bound_rows)
    assert all(row["bound_tbbo_selected_spread_ledger_sha256"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in bound_rows)
    assert all(row["bound_tbbo_source_evidence_type"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in bound_rows)
    assert all(row["bound_tbbo_selected_quote_ts_event"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in bound_rows)
    assert all(row["bound_tbbo_quote_age_seconds"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in bound_rows)
    assert all(row["bound_tbbo_selected_spread_row_hash"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in missing_rows)
    assert all(row["bound_tbbo_selected_spread_ledger_sha256"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in missing_rows)
    assert all(row["bound_tbbo_source_evidence_type"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in missing_rows)
    assert all(row["bound_tbbo_selected_quote_ts_event"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in missing_rows)
    assert all(row["bound_tbbo_quote_age_seconds"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE" for row in missing_rows)
    row438 = next(row for row in rows if row["row_index"] == "438")
    assert row438["bound_tbbo_source_evidence_type"] == "ROW438_RETRY_AT_OR_BEFORE_FILL_TBBO"
    assert row438["max_selected_quote_age_seconds"] == "60.0"
    assert row438["bound_tbbo_quote_age_seconds"] == "12.839815"
    row441 = next(row for row in rows if row["row_index"] == "441")
    assert row441["bound_tbbo_source_evidence_type"] == "ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO"
    assert row441["max_selected_quote_age_seconds"] == "300.0"
    assert row441["bound_tbbo_quote_age_seconds"] == "174.34714"
    assert row441["bound_tbbo_selection_status"] == "PASS_ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT"
    row547 = next(row for row in rows if row["row_index"] == "547")
    assert row547["market_order_reason"] == "BOOK_REQUIRED_CAP_BOUND_LIMIT_SIDE_NOT_PLACED"
    assert row547["bound_tbbo_source_evidence_type"] == "ROW547_CAP_BOUND_AT_OR_BEFORE_FILL_TBBO"
    assert row547["bound_tbbo_selected_quote_ts_event"] == "2023-02-07T00:59:55.061867017Z"
    assert row547["bound_tbbo_quote_age_seconds"] == "4.9381329999999997"
    row554 = next(row for row in rows if row["row_index"] == "554")
    assert row554["market_order_reason"] == "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT"
    assert row554["bound_tbbo_source_evidence_type"] == "STANDING_RETRY_AT_OR_BEFORE_FILL_TBBO"
    assert row554["bound_tbbo_selected_quote_ts_event"] == "2023-02-07T07:59:42.813084237Z"
    assert row554["bound_tbbo_quote_age_seconds"] == "17.186916"
    row959 = next(row for row in rows if row["row_index"] == "959")
    assert row959["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE"
    assert row959["order_side"] == "SELL"
    assert row959["order_quantity"] == "2"
    assert row959["fill_candidate_timestamp_utc"] == "2023-03-03T22:00:00Z"
    assert row959["market_order_reason"] == "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT"
    assert row959["bound_tbbo_source_evidence_type"] == "STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO"
    assert row959["bound_tbbo_selected_quote_ts_event"] == "2023-03-03T21:59:59.523101291Z"
    assert row959["bound_tbbo_quote_age_seconds"] == "0.47689900000000002"
    row962 = next(row for row in rows if row["row_index"] == "962")
    assert row962["bound_tbbo_source_evidence_type"] == "STANDING_RETRY_AT_OR_BEFORE_FILL_TBBO"
    assert row962["bound_tbbo_selected_quote_ts_event"] == "2023-03-06T02:59:41.988599197Z"
    assert row962["bound_tbbo_quote_age_seconds"] == "18.011400999999999"
    assert all(int(row["row_index"]) != 892 for row in rows)
    for row in sha_rows:
        assert row["sha256"] == _sha256(TBBO_REQUIREMENTS_ROOT / row["relative_path"])


def test_2023_test_row547_cap_bound_market_order_is_bounded_and_row1378_completes_pack(test_bundle):
    del test_bundle
    runtime = next(row for row in _rows(PACK_ROOT, "runtime_evidence_ledger.csv") if row["row_index"] == "547")
    order = next(row for row in _rows(RUN_ROOT, "limit_order_ledger.csv") if row["row_index"] == "547")
    market_order = next(row for row in _rows(RUN_ROOT, "market_order_ledger.csv") if row["row_index"] == "547")
    cost = next(row for row in _rows(RUN_ROOT, "cost_ledger.csv") if row["row_index"] == "547")
    row1113_market = next(row for row in _rows(RUN_ROOT, "market_order_ledger.csv") if row["row_index"] == "1113")
    run_manifest = _json(RUN_ROOT, "run_manifest.json")

    decision_price = float(next(row for row in _rows(PACK_ROOT, "hourly_decision_completed_bar.csv") if row["row_index"] == "547")["close_price"])
    sigma = float(runtime["annual_percentage_sigma"])
    base_position = 500000 * 0.2 / (decision_price * 1000 * sigma)
    target_capped_forecast = int(order["adjacent_target_position"]) / base_position * 10.0

    assert order["formula_limit_price"] == "NOT_APPLICABLE_CAP_BOUND_MARKET_ORDER_LIMIT_SIDE_NOT_PLACED"
    assert order["limit_order_price"] == "NOT_APPLICABLE_CAP_BOUND_MARKET_ORDER_LIMIT_SIDE_NOT_PLACED"
    assert market_order["trigger_source_condition"] == "BOOK_REQUIRED_CAP_BOUND_LIMIT_SIDE_NOT_PLACED"
    assert cost["tbbo_bid_px"] == "113.546875"
    assert target_capped_forecast >= 20.0
    assert cost["tbbo_selected_spread_ledger_sha256"] == _sha256(
        COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME
    )
    assert (
        row1113_market["engineering_convention_label"]
        == "SOURCE_NATIVE_ENGINEERING_SESSION_END_MARKET_ORDER_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT"
    )
    assert _rows(RUN_ROOT, "fail_closed_ledger.csv") == []
    assert run_manifest["candidate_row_count"] == 1378
    assert run_manifest["supported_mechanical_row_count"] == 1378
    assert run_manifest["fail_closed_row_index"] == 0
    assert run_manifest["fail_closed_reason"] == "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"


def test_2023_test_market_order_tbbo_requirements_discovery_rejects_forged_row():
    bundle = discover_2023_test_market_order_tbbo_requirements()
    rows = _rows(TBBO_REQUIREMENTS_ROOT, "market_order_tbbo_requirements.csv")
    rows[0]["order_quantity"] = "999"
    _write_csv_rows(TBBO_REQUIREMENTS_ROOT / "market_order_tbbo_requirements.csv", rows)

    with pytest.raises(CarverBlocked, match="ledger hash drift|row hash drift"):
        bundle.validate()

    discover_2023_test_market_order_tbbo_requirements()


def test_2023_test_market_order_tbbo_requirements_rejects_bound_row_without_bound_hashes():
    bundle = discover_2023_test_market_order_tbbo_requirements()
    rows = _rows(TBBO_REQUIREMENTS_ROOT, "market_order_tbbo_requirements.csv")
    row437 = next(row for row in rows if row["row_index"] == "437")
    row437["bound_tbbo_selected_spread_row_hash"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    row437["bound_tbbo_selected_spread_ledger_sha256"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    row437["bound_tbbo_source_evidence_type"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    row437["bound_tbbo_selected_quote_ts_event"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    row437["bound_tbbo_quote_age_seconds"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    row437["bound_tbbo_selection_status"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    _rehash_csv_row(row437)
    _write_csv_rows(TBBO_REQUIREMENTS_ROOT / "market_order_tbbo_requirements.csv", rows)
    manifest = _json(TBBO_REQUIREMENTS_ROOT, "market_order_tbbo_requirements_manifest.json")
    manifest["requirements_ledger_hash"] = _sha256(TBBO_REQUIREMENTS_ROOT / "market_order_tbbo_requirements.csv")
    (TBBO_REQUIREMENTS_ROOT / "market_order_tbbo_requirements_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    forged = replace(
        bundle,
        requirements_ledger_hash=manifest["requirements_ledger_hash"],
        manifest_hash=_sha256(TBBO_REQUIREMENTS_ROOT / "market_order_tbbo_requirements_manifest.json"),
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_tbbo_requirements_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="bound TBBO requirement row hash"):
        forged.validate()

    discover_2023_test_market_order_tbbo_requirements()


def test_standing_tbbo_acquisition_rejects_self_consistent_broadened_request_window(tmp_path):
    from carver_s27_v2_2023_test_standing_market_order_tbbo_acquisition import _missing_requirements

    rows = _rows(TBBO_REQUIREMENTS_ROOT, "market_order_tbbo_requirements.csv")
    forged = dict(next(row for row in rows if row["row_index"] == "353"))
    forged["tbbo_requirement_status"] = "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"
    forged["request_start_utc"] = "2023-01-25T00:00:00Z"
    forged["request_end_utc"] = "2023-01-25T23:59:59Z"
    forged["bound_tbbo_selected_spread_row_hash"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    forged["bound_tbbo_selected_spread_ledger_sha256"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    forged["bound_tbbo_source_evidence_type"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    forged["bound_tbbo_selected_quote_ts_event"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    forged["bound_tbbo_quote_age_seconds"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    forged["bound_tbbo_selection_status"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    _rehash_csv_row(forged)
    path = tmp_path / "forged_standing_requirements.csv"
    _write_csv_rows(path, [forged])

    with pytest.raises(CarverBlocked, match="request window"):
        _missing_requirements(path)


@pytest.mark.parametrize("forged_flag", ("source_faithful_evidence_claimed", "result_interpretation_authorized"))
def test_standing_tbbo_retry_rejects_result_or_source_faithful_claim(tmp_path, forged_flag):
    from carver_s27_v2_2023_test_standing_market_order_tbbo_failed_window_retry import (
        STANDING_BATCH_STATUS,
        _failed_requirements,
    )

    failed_indices = {str(index) for index in json.loads(STANDING_BATCH_STATUS.read_text(encoding="ascii"))["failed_row_indices"]}
    rows = []
    for row in _rows(TBBO_REQUIREMENTS_ROOT, "market_order_tbbo_requirements.csv"):
        if row["row_index"] not in failed_indices:
            continue
        forged = dict(row)
        forged["tbbo_requirement_status"] = "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"
        forged["bound_tbbo_selected_spread_row_hash"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
        forged["bound_tbbo_selected_spread_ledger_sha256"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
        forged["bound_tbbo_source_evidence_type"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
        forged["bound_tbbo_selected_quote_ts_event"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
        forged["bound_tbbo_quote_age_seconds"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
        forged["bound_tbbo_selection_status"] = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
        _rehash_csv_row(forged)
        rows.append(forged)
    rows[0][forged_flag] = "TRUE"
    _rehash_csv_row(rows[0])
    path = tmp_path / "forged_retry_requirements.csv"
    _write_csv_rows(path, rows)

    with pytest.raises(CarverBlocked, match="result/source-faithful"):
        _failed_requirements(path)


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("candidate_row_count", 999),
        ("supported_mechanical_row_count", 999),
        ("fail_closed_row_index", 999),
        ("fail_closed_reason", "FORGED_REASON"),
        ("status", "FORGED_STATUS"),
        ("authorization_label", "FORGED_AUTHORIZATION"),
        ("strategy_id", "FORGED_STRATEGY"),
        ("instrument", "FORGED_INSTRUMENT"),
        ("lane", "FORGED_LANE"),
        ("run_manifest_hash", "a" * 64),
        ("evidence_manifest_hash", "b" * 64),
        ("trusted_bundle_hash", "c" * 64),
        ("non_authorizations", tuple()),
    ),
)
def test_2023_test_bundle_rejects_forgery(test_bundle, field_name, forged_value):
    forged = replace(test_bundle, **{field_name: forged_value})
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        ("market_order_ledger.csv", "order_quantity", "1", "BUY 2"),
        ("market_fill_metadata_ledger.csv", "position_after_fill", "1", "target position"),
        ("cost_ledger.csv", "tbbo_selected_spread_row_hash", "0" * 64, "TBBO row hash"),
        ("cost_ledger.csv", "tbbo_selected_spread_ledger_sha256", "0" * 64, "TBBO ledger hash"),
        ("cost_ledger.csv", "spread_cost_amount", "1.0", "authorized row-1 cost amounts"),
    ),
)
def test_2023_test_bundle_rejects_supported_market_artifact_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    rows[0][field_name] = forged_value
    _write_csv_rows(tmp_path / filename, rows)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=_sha256(tmp_path / "evidence_manifest.json"),
        trusted_bundle_hash=_sha256(tmp_path / "trusted_bundle.json"),
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    del message
    with pytest.raises(CarverBlocked, match="evidence manifest ledger hash"):
        forged.validate()


def test_2023_test_bundle_rejects_self_consistent_supported_market_ledger_omission(tmp_path, test_bundle):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    for filename in ("market_order_ledger.csv", "market_fill_metadata_ledger.csv"):
        rows = _rows(tmp_path, filename)
        _write_csv_header_only(tmp_path / filename, list(rows[0].keys()))
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="supported market state"):
        forged.validate()


def test_2023_test_bundle_rejects_self_consistent_no_market_state_downgrade_with_market_omission(
    tmp_path,
    test_bundle,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    no_market_rows = _rows(tmp_path, "no_market_order_ledger.csv")
    no_market_rows[0]["market_order_required"] = "FALSE"
    no_market_rows[0]["market_order_rows_emitted"] = "FALSE"
    no_market_rows[0]["market_fallback_status"] = "NOT_REQUIRED_NO_ORDER_POSITION_UNCHANGED"
    _write_csv_rows(tmp_path / "no_market_order_ledger.csv", no_market_rows)
    for filename in ("market_order_ledger.csv", "market_fill_metadata_ledger.csv"):
        rows = _rows(tmp_path, filename)
        _write_csv_header_only(tmp_path / filename, list(rows[0].keys()))
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="row-1 no-market state"):
        forged.validate()


def test_2023_test_bundle_rejects_self_consistent_supported_market_order_quantity_forgery(
    tmp_path,
    test_bundle,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, "market_order_ledger.csv")
    rows[0]["order_quantity"] = "1"
    _write_csv_rows(tmp_path / "market_order_ledger.csv", rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="full-gap quantity"):
        forged.validate()


def test_2023_test_bundle_rejects_self_consistent_row547_cap_bound_trigger_forgery(
    tmp_path,
    test_bundle,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, "market_order_ledger.csv")
    row547 = next(row for row in rows if row["row_index"] == "547")
    row547["trigger_source_condition"] = "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT"
    _rehash_csv_row(row547)
    _write_csv_rows(tmp_path / "market_order_ledger.csv", rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="market-order trigger"):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value"),
    (
        ("desired_position_ledger.csv", "desired_position_contracts", "-1"),
        ("limit_order_ledger.csv", "order_side", "SELL"),
        ("no_market_order_ledger.csv", "engineering_convention_label", "NOT_APPLICABLE"),
        ("working_order_transition_ledger.csv", "working_state_before", "OPEN_WORKING_ORDER_CARRIED"),
        ("fill_ledger.csv", "fill_executed", "TRUE"),
        ("cost_ledger.csv", "total_cost_amount", "2.3"),
        ("pnl_ledger.csv", "ending_position_contracts", "-1"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row701_roll_suppression_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row701 = next(row for row in rows if row["row_index"] == "701")
    row701[field_name] = forged_value
    _rehash_csv_row(row701)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="row-701 suppression"):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        ("market_fill_metadata_ledger.csv", "fill_price", "112.59375", "fill price"),
        ("cost_ledger.csv", "order_cost_type", "MARKET_ORDER_BUY_ASK_FILL_ACTUAL_COST_NOT_PNL", "side-specific order cost type"),
        ("cost_ledger.csv", "currency", "EUR", "USD currency"),
        ("cost_ledger.csv", "tbbo_quote_ts_event", "2023-01-03T01:59:59.000000Z", "quote timestamp"),
        ("cost_ledger.csv", "tbbo_bid_px", "112.5625", "TBBO bid"),
        ("cost_ledger.csv", "tbbo_ask_px", "112.609375", "TBBO ask"),
        ("cost_ledger.csv", "tbbo_full_spread_points", "0.03125", "spread points"),
        ("cost_ledger.csv", "tbbo_full_spread_value_per_contract", "31.25", "spread value"),
        ("cost_ledger.csv", "tbbo_selected_spread_row_hash", "0" * 64, "TBBO row hash"),
        ("cost_ledger.csv", "tbbo_selected_spread_ledger_sha256", "0" * 64, "TBBO ledger hash"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row2_market_tbbo_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    rows[1][field_name] = forged_value
    _rehash_csv_row(rows[1])
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match=f"{message}|market execution|market fill metadata"):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        ("market_order_ledger.csv", "decision_timestamp_utc", "2023-01-26T19:00:00Z", "row-391 session-end"),
        ("market_order_ledger.csv", "order_quantity", "7", "full-gap quantity"),
        ("market_order_ledger.csv", "target_position_after_fill", "11", "target position"),
        ("market_fill_metadata_ledger.csv", "fill_timestamp_utc", "2023-01-26T22:00:00Z", "row-391 market spread evidence fill timestamp drift"),
        ("market_fill_metadata_ledger.csv", "fill_price", "114.8125", "fill price"),
        (
            "working_order_transition_ledger.csv",
            "same_session",
            "FALSE",
            "session-end market execution class",
        ),
        ("fill_ledger.csv", "position_after_fill", "11", "session-end market execution class|target position"),
        ("cost_ledger.csv", "tbbo_ask_px", "114.8125", "selected TBBO ask"),
        ("pnl_ledger.csv", "valuation_convention_label", "FORGED_VALUATION_LABEL", "row-391 session-end"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row391_session_end_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row391 = next(row for row in rows if row["row_index"] == "391")
    row391[field_name] = forged_value
    _rehash_csv_row(row391)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match=f"{message}|market execution|market fill metadata"):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        (
            "market_order_ledger.csv",
            "engineering_convention_label",
            "NOT_APPLICABLE",
            "row-1113 valuation-gap|market execution",
        ),
        (
            "no_market_order_ledger.csv",
            "engineering_convention_label",
            "NOT_APPLICABLE",
            "row-1113 valuation-gap|market execution",
        ),
        (
            "market_fill_metadata_ledger.csv",
            "fill_timestamp_utc",
            "2023-03-14T22:00:00Z",
            "row-1113 valuation-gap|fill timestamp",
        ),
        (
            "market_fill_metadata_ledger.csv",
            "fill_price",
            "113.453125",
            "fill price",
        ),
        (
            "working_order_transition_ledger.csv",
            "same_session",
            "FALSE",
            "row-1113 valuation-gap|market execution",
        ),
        (
            "cost_ledger.csv",
            "tbbo_ask_px",
            "113.453125",
            "selected TBBO ask",
        ),
        (
            "pnl_ledger.csv",
            "valuation_mark_timestamp_utc",
            "2023-03-14T22:00:00Z",
            "row-1113 valuation-gap|market execution",
        ),
        (
            "pnl_ledger.csv",
            "valuation_convention_label",
            "FORGED_VALUATION_LABEL",
            "engineering valuation label",
        ),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row1113_valuation_gap_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row1113 = next(row for row in rows if row["row_index"] == "1113")
    row1113[field_name] = forged_value
    _rehash_csv_row(row1113)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match=f"{message}|market execution|PnL metadata"):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value"),
    (
        ("market_order_ledger.csv", "order_quantity", "3"),
        ("market_order_ledger.csv", "target_position_after_fill", "20"),
        ("market_fill_metadata_ledger.csv", "fill_timestamp_utc", "2023-01-31T02:00:00Z"),
        ("market_fill_metadata_ledger.csv", "fill_price", "114.40625"),
        ("market_fill_metadata_ledger.csv", "position_after_fill", "20"),
        ("working_order_transition_ledger.csv", "ending_position_contracts", "20"),
        ("fill_ledger.csv", "fill_price", "114.40625"),
        ("fill_ledger.csv", "position_after_fill", "20"),
        ("cost_ledger.csv", "tbbo_bid_px", "114.375"),
        ("cost_ledger.csv", "tbbo_selected_spread_row_hash", "0" * 64),
        ("pnl_ledger.csv", "valuation_mark_close_price", "114.390625"),
        ("pnl_ledger.csv", "ending_position_contracts", "20"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row437_market_tbbo_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row437 = next(row for row in rows if row["row_index"] == "437")
    row437[field_name] = forged_value
    _rehash_csv_row(row437)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="S27 v2 2023 TEST"):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value"),
    (
        ("market_order_ledger.csv", "order_quantity", "4"),
        ("market_order_ledger.csv", "target_position_after_fill", "17"),
        ("market_fill_metadata_ledger.csv", "fill_timestamp_utc", "2023-01-31T03:00:00Z"),
        ("market_fill_metadata_ledger.csv", "fill_price", "114.375"),
        ("market_fill_metadata_ledger.csv", "position_after_fill", "17"),
        ("working_order_transition_ledger.csv", "ending_position_contracts", "17"),
        ("fill_ledger.csv", "fill_price", "114.375"),
        ("fill_ledger.csv", "position_after_fill", "17"),
        ("cost_ledger.csv", "tbbo_bid_px", "114.34375"),
        ("cost_ledger.csv", "tbbo_selected_spread_row_hash", "0" * 64),
        ("pnl_ledger.csv", "valuation_mark_close_price", "114.359375"),
        ("pnl_ledger.csv", "ending_position_contracts", "17"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row438_market_tbbo_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row438 = next(row for row in rows if row["row_index"] == "438")
    row438[field_name] = forged_value
    _rehash_csv_row(row438)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="S27 v2 2023 TEST"):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        (
            "no_market_order_ledger.csv",
            "engineering_convention_label",
            "NOT_APPLICABLE",
            "market execution convention labels must agree",
        ),
        ("no_market_order_ledger.csv", "market_order_rows_emitted", "FALSE", "row-304 engineering session-open"),
        ("no_market_order_ledger.csv", "row_status", "FORGED_ROW_STATUS", "row-304 engineering session-open"),
        (
            "market_order_ledger.csv",
            "order_status",
            "LOCAL_MARKET_ORDER_ROW_EMITTED_NOT_RESULT",
            "row-304 engineering session-open",
        ),
        ("market_order_ledger.csv", "raw_symbol", "ZNM3", "row-304 engineering session-open"),
        ("market_order_ledger.csv", "decision_timestamp_utc", "2023-01-20T20:00:00Z", "row-304 engineering session-open"),
        (
            "market_order_ledger.csv",
            "engineering_convention_label",
            "NOT_APPLICABLE",
            "market execution convention labels must agree",
        ),
        ("market_fill_metadata_ledger.csv", "same_session", "TRUE", "session-open market reset class"),
        ("market_fill_metadata_ledger.csv", "raw_symbol", "ZNM3", "row-304 engineering session-open"),
        (
            "market_fill_metadata_ledger.csv",
            "fill_source_row_hash",
            "0" * 64,
            "market execution fill must bind declared fill source row",
        ),
        ("market_fill_metadata_ledger.csv", "commission_per_contract", "1.0", "row-304 engineering session-open"),
        ("market_fill_metadata_ledger.csv", "commission_amount", "1.0", "row-304 engineering session-open"),
        ("market_fill_metadata_ledger.csv", "pnl_emission_status", "FORGED_PNL_STATUS", "row-304 engineering session-open"),
        ("market_fill_metadata_ledger.csv", "row_status", "FORGED_ROW_STATUS", "row-304 engineering session-open"),
        ("working_order_transition_ledger.csv", "working_state_after", "FORGED_WORKING_STATE", "row-304 engineering session-open"),
        ("working_order_transition_ledger.csv", "row_status", "FORGED_ROW_STATUS", "row-304 engineering session-open"),
        ("fill_ledger.csv", "fill_rule", "FORGED_FILL_RULE", "row-304 engineering session-open"),
        ("fill_ledger.csv", "fill_price", "115.046875", "row-304 engineering session-open"),
        ("fill_ledger.csv", "fill_quantity", "1", "row-304 engineering session-open"),
        ("fill_ledger.csv", "row_status", "FORGED_ROW_STATUS", "row-304 engineering session-open"),
        ("cost_ledger.csv", "cost_policy_id", "FORGED_COST_POLICY", "row-304 engineering session-open"),
        ("cost_ledger.csv", "spread_cost_reason", "FORGED_SPREAD_REASON", "row-304 engineering session-open"),
        ("cost_ledger.csv", "tbbo_ask_px", "115.046875", "selected TBBO ask"),
        ("cost_ledger.csv", "row_status", "FORGED_ROW_STATUS", "row-304 engineering session-open"),
        ("pnl_ledger.csv", "valuation_mark_close_price", "115.046875", "row-304 engineering session-open"),
        ("pnl_ledger.csv", "valuation_convention_label", "FORGED_VALUATION_LABEL", "row-304 engineering session-open"),
        ("pnl_ledger.csv", "row_status", "FORGED_ROW_STATUS", "row-304 engineering session-open"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row304_engineering_session_open_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row304 = next(row for row in rows if row["row_index"] == "304")
    row304[field_name] = forged_value
    _rehash_csv_row(row304)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match=f"{message}|market execution|market fill metadata"):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        ("limit_order_ledger.csv", "order_side", "BUY", "row-346 target-zero"),
        ("limit_order_ledger.csv", "formula_limit_price", "115.0", "row-346 target-zero"),
        ("limit_order_ledger.csv", "limit_order_price", "114.984375", "row-346 target-zero"),
        (
            "no_market_order_ledger.csv",
            "market_fallback_status",
            "FAIL_CLOSED_UNFILLED_LIMIT_ORDER_MARKET_FALLBACK_NOT_AUTHORIZED",
            "row-346 target-zero",
        ),
        ("working_order_transition_ledger.csv", "ending_position_contracts", "1", "row-346 target-zero"),
        ("fill_ledger.csv", "fill_price", "114.984375", "row-346 target-zero"),
        ("fill_ledger.csv", "fill_quantity", "0", "row-346 target-zero"),
        ("cost_ledger.csv", "commission_amount", "0.0", "row-346 target-zero"),
        ("pnl_ledger.csv", "row_net_pnl_amount", "-31.25", "row-346 target-zero"),
        ("pnl_ledger.csv", "ending_position_contracts", "1", "row-346 target-zero"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row346_target_zero_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row346 = next(row for row in rows if row["row_index"] == "346")
    row346[field_name] = forged_value
    _rehash_csv_row(row346)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match=message):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        ("limit_order_ledger.csv", "row_status", "LOCAL_LIMIT_ORDER_ROW_EMITTED_NOT_RESULT", "row-436 session-open limit order"),
        ("limit_order_ledger.csv", "limit_order_price", "114.28125", "row-436 session-open limit order"),
        ("no_market_order_ledger.csv", "engineering_convention_label", "NOT_APPLICABLE", "row-436 session-open limit no-market"),
        ("working_order_transition_ledger.csv", "same_session", "TRUE", "row-436 session-open limit transition"),
        ("working_order_transition_ledger.csv", "ending_position_contracts", "24", "row-436 session-open limit transition"),
        ("fill_ledger.csv", "fill_rule", "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL", "row-436 session-open limit fill"),
        ("fill_ledger.csv", "position_after_fill", "24", "row-436 session-open limit fill"),
        ("cost_ledger.csv", "commission_amount", "0.0", "row-436 session-open limit cost"),
        ("pnl_ledger.csv", "valuation_mark_close_price", "114.421875", "row-436 session-open limit pnl"),
        ("pnl_ledger.csv", "ending_position_contracts", "24", "row-436 session-open limit pnl"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row436_session_open_limit_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row436 = next(row for row in rows if row["row_index"] == "436")
    row436[field_name] = forged_value
    _rehash_csv_row(row436)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match=message):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        ("limit_order_ledger.csv", "limit_order_price", "111.65625", "row-892 session-end limit order"),
        ("no_market_order_ledger.csv", "engineering_convention_label", "NOT_APPLICABLE", "row-892 session-end limit no-market"),
        ("working_order_transition_ledger.csv", "same_session", "TRUE", "row-892 session-end limit transition"),
        ("fill_ledger.csv", "fill_rule", "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL", "row-892 session-end limit fill"),
        ("cost_ledger.csv", "commission_amount", "0.0", "row-892 session-end limit cost"),
        ("pnl_ledger.csv", "ending_position_contracts", "0", "row-892 session-end limit pnl"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row892_session_end_limit_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row892 = next(row for row in rows if row["row_index"] == "892")
    row892[field_name] = forged_value
    _rehash_csv_row(row892)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match=message):
        forged.validate()


@pytest.mark.parametrize(
    ("filename", "field_name", "forged_value", "message"),
    (
        ("limit_order_ledger.csv", "limit_order_price", "114.5", "row-1355 valuation-gap limit order"),
        ("no_market_order_ledger.csv", "engineering_convention_label", "NOT_APPLICABLE", "row-1355 valuation-gap limit no-market"),
        ("working_order_transition_ledger.csv", "same_session", "TRUE", "row-1355 valuation-gap limit transition"),
        ("fill_ledger.csv", "fill_rule", "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL", "row-1355 valuation-gap limit fill"),
        ("cost_ledger.csv", "commission_amount", "0.0", "row-1355 valuation-gap limit cost"),
        ("pnl_ledger.csv", "valuation_mark_timestamp_utc", "2023-03-29T22:00:00Z", "row-1355 valuation-gap limit pnl"),
    ),
)
def test_2023_test_bundle_rejects_self_consistent_row1355_session_end_limit_valuation_gap_forgery(
    tmp_path,
    test_bundle,
    filename,
    field_name,
    forged_value,
    message,
):
    for source in RUN_ROOT.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    rows = _rows(tmp_path, filename)
    row1355 = next(row for row in rows if row["row_index"] == "1355")
    row1355[field_name] = forged_value
    _rehash_csv_row(row1355)
    _write_csv_rows(tmp_path / filename, rows)
    evidence_hash, trusted_hash = _refresh_evidence_and_trusted_hashes(tmp_path)
    forged = replace(
        test_bundle,
        output_root=str(tmp_path.resolve()),
        run_manifest_hash=_sha256(tmp_path / "run_manifest.json"),
        evidence_manifest_hash=evidence_hash,
        trusted_bundle_hash=trusted_hash,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match=message):
        forged.validate()


def test_2023_test_runner_not_exported_from_package_root():
    package_init = (ROOT / "src" / "carver" / "spine" / "s27_v2_replay" / "__init__.py").read_text()

    assert "test_mechanical_run" not in package_init
    assert "run_2023_test_mechanical_artifacts" not in package_init
    assert not hasattr(package_root, "run_2023_test_mechanical_artifacts")
    assert not hasattr(package_root, "build_2023_test_declared_pack")


def test_2023_test_non_authorizations_preserved(test_bundle):
    assert test_bundle.non_authorizations == NON_AUTHORIZATIONS
    assert "NO_VALIDATION_ACCESS" in test_bundle.non_authorizations
    assert "NO_LOCKBOX" in test_bundle.non_authorizations
    assert "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM" in test_bundle.non_authorizations


def test_2023_test_combined_tbbo_registry_rejects_self_consistent_row215_drift(test_bundle):
    del test_bundle
    build_2023_test_combined_market_tbbo_registry()
    registry = COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME
    rows = _rows(COMBINED_TBBO_ROOT, COMBINED_MARKET_TBBO_REGISTRY_NAME)
    row215 = next(row for row in rows if row["row_index"] == "215")
    row215["bid_px_00"] = "114.609375"
    row215["selected_executable_market_fill_price"] = "114.609375"
    _rehash_csv_row(row215)
    _write_csv_rows(registry, rows)

    with pytest.raises(CarverBlocked, match="combined market TBBO registry drift"):
        _expected_market_spread_evidence(215)

    build_2023_test_combined_market_tbbo_registry()


def test_2023_test_combined_tbbo_registry_rejects_self_consistent_row437_drift(test_bundle):
    del test_bundle
    build_2023_test_combined_market_tbbo_registry()
    registry = COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME
    rows = _rows(COMBINED_TBBO_ROOT, COMBINED_MARKET_TBBO_REGISTRY_NAME)
    row437 = next(row for row in rows if row["row_index"] == "437")
    row437["bid_px_00"] = "114.375"
    row437["selected_executable_market_fill_price"] = "114.375"
    _rehash_csv_row(row437)
    _write_csv_rows(registry, rows)

    with pytest.raises(CarverBlocked, match="combined market TBBO registry drift"):
        _expected_market_spread_evidence(437)

    build_2023_test_combined_market_tbbo_registry()


def test_2023_test_combined_tbbo_registry_rejects_self_consistent_row438_drift(test_bundle):
    del test_bundle
    build_2023_test_combined_market_tbbo_registry()
    registry = COMBINED_TBBO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_NAME
    rows = _rows(COMBINED_TBBO_ROOT, COMBINED_MARKET_TBBO_REGISTRY_NAME)
    row438 = next(row for row in rows if row["row_index"] == "438")
    row438["bid_px_00"] = "114.34375"
    row438["selected_executable_market_fill_price"] = "114.34375"
    _rehash_csv_row(row438)
    _write_csv_rows(registry, rows)

    with pytest.raises(CarverBlocked, match="combined market TBBO registry drift"):
        _expected_market_spread_evidence(438)

    build_2023_test_combined_market_tbbo_registry()


def test_2023_test_combined_tbbo_registry_rejects_self_consistent_row441_source_drift(test_bundle):
    del test_bundle
    source = (
        ROOT
        / "docs/researchops/s27_v2_market_spread_evidence/ZN/20260614_2023_test_row441_market_order_tbbo_extended_lookback/"
        / "ledger/20260614_S27_V2_2023_TEST_ROW441_MARKET_ORDER_TBBO_EXTENDED_LOOKBACK_selected_spread_registry.csv"
    )
    original_bytes = source.read_bytes()
    rows = _rows(source.parent, source.name)
    try:
        row441 = next(row for row in rows if row["row_index"] == "441")
        row441["bid_px_00"] = "114.34375"
        row441["selected_executable_market_fill_price"] = "114.34375"
        _rehash_csv_row(row441)
        _write_csv_rows(source, rows)

        with pytest.raises(CarverBlocked, match="selected TBBO bid_px_00 drift"):
            build_2023_test_combined_market_tbbo_registry()
    finally:
        source.write_bytes(original_bytes)
        build_2023_test_combined_market_tbbo_registry()


def test_standing_tbbo_status_and_manifest_distinguish_current_request_from_aggregate_registry():
    batch_root = ROOT / "docs/researchops/s27_v2_market_spread_evidence/ZN/20260613_2023_test_standing_market_order_tbbo_batch_evidence"
    retry_root = ROOT / "docs/researchops/s27_v2_market_spread_evidence/ZN/20260613_2023_test_standing_market_order_tbbo_failed_window_retry"
    batch_manifest = _json(batch_root / "manifest", "20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_BATCH_request_manifest.json")
    batch_status = _json(batch_root / "status", "20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_BATCH_status.json")
    retry_manifest = _json(
        retry_root / "manifest",
        "20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_request_manifest.json",
    )
    retry_status = _json(
        retry_root / "status",
        "20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_status.json",
    )

    assert batch_status["current_request_count"] == batch_manifest["current_request_count"] == 97
    assert batch_status["current_request_row_indices"] == batch_manifest["current_request_row_indices"]
    assert batch_status["aggregate_registry_row_count"] == batch_manifest["aggregate_registry_row_count"] == 200
    assert batch_status["selected_row_count"] == 156
    assert set(batch_status["current_request_row_indices"]) & set(batch_status["failed_row_indices"]) == {
        "962",
        "964",
        "969",
        "970",
        "986",
        "991",
        "992",
        "993",
        "1070",
        "1118",
        "1136",
        "1158",
        "1160",
        "1162",
        "1168",
        "1180",
        "1301",
        "1312",
        "1322",
        "1346",
    }
    assert retry_status["current_retry_request_count"] == retry_manifest["current_retry_request_count"] == 20
    assert retry_status["current_retry_row_indices"] == retry_manifest["current_retry_row_indices"]
    assert retry_status["aggregate_registry_row_count"] == retry_manifest["aggregate_registry_row_count"] == 44
    assert retry_status["selected_row_count"] == 38
    assert set(retry_status["current_retry_row_indices"]).isdisjoint(set(retry_status["failed_row_indices"]))


def test_2023_test_combined_tbbo_registry_rejects_source_selected_registry_drift():
    source = (
        ROOT
        / "docs/researchops/s27_v2_market_spread_evidence/ZN/20260613_2023_test_standing_market_order_tbbo_failed_window_retry/"
        / "ledger/20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_selected_spread_registry.csv"
    )
    rows = _rows(source.parent, source.name)
    original_rows = [dict(row) for row in rows]
    try:
        row439 = next(row for row in rows if row["row_index"] == "439")
        row439["selected_quote_ts_event"] = "2023-01-31T02:59:44.000000000Z"
        _rehash_csv_row(row439)
        _write_csv_rows(source, rows)
        with pytest.raises(CarverBlocked, match="selected TBBO selected_quote_ts_event drift"):
            build_2023_test_combined_market_tbbo_registry()
    finally:
        _write_csv_rows(source, original_rows)
        build_2023_test_combined_market_tbbo_registry()


def test_2023_test_combined_tbbo_registry_rejects_source_selected_registry_missing_raw_hashes():
    source = (
        ROOT
        / "docs/researchops/s27_v2_market_spread_evidence/ZN/20260613_2023_test_standing_market_order_tbbo_failed_window_retry/"
        / "ledger/20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_selected_spread_registry.csv"
    )
    rows = _rows(source.parent, source.name)
    original_rows = [dict(row) for row in rows]
    try:
        row439 = next(row for row in rows if row["row_index"] == "439")
        row439["retry_raw_csv_sha256"] = ""
        row439["retry_raw_dbn_sha256"] = ""
        _rehash_csv_row(row439)
        _write_csv_rows(source, rows)
        with pytest.raises(CarverBlocked, match="selected row must bind raw CSV bytes"):
            build_2023_test_combined_market_tbbo_registry()
    finally:
        _write_csv_rows(source, original_rows)
        build_2023_test_combined_market_tbbo_registry()


def _machine_freeze_pack_rows() -> dict[str, list[dict[str, str]]]:
    return {
        filename: _rows(PACK_ROOT, filename)[:1]
        for filename in (
            "hourly_decision_completed_bar.csv",
            "hourly_fill_completed_bar.csv",
            "valuation_mark_completed_bar.csv",
            "runtime_evidence_ledger.csv",
            "roll_calendar.csv",
        )
    }


def _locked_market_freeze_rows() -> dict[str, list[dict[str, object]]]:
    return {
        "position": [
            {
                "starting_position_contracts": 0,
                "desired_position_contracts": 2,
                "position_change_contracts": 2,
                "base_position_contracts": 1.0,
            }
        ],
        "order": [{"order_side": "BUY", "order_quantity": 2, "adjacent_target_position": 1}],
        "market": [
            {
                "market_order_required": True,
                "market_order_rows_emitted": True,
                "market_fallback_status": "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP",
            }
        ],
        "transition": [
            {
                "starting_position_contracts": 0,
                "ending_position_contracts": 2,
                "working_state_after": "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION",
                "same_session": True,
            }
        ],
        "fill": [{"fill_executed": True, "fill_quantity": 2, "position_after_fill": 2}],
        "cost": [{"spread_cost_amount": 0.0}],
        "pnl": [{"ending_position_contracts": 2}],
        "validation": [{"source_faithful_evidence_claimed": False}],
    }


def test_2023_test_market_order_freeze_rejects_forged_non_full_gap_status():
    from carver.spine.s27_v2_replay.pretest_machine_freeze import validate_pretest_machine_freeze_rows

    rows = _machine_freeze_pack_rows()
    computed = {
        "position": [{"starting_position_contracts": 0, "desired_position_contracts": 1, "position_change_contracts": 1, "base_position_contracts": 1.0}],
        "order": [{"order_side": "BUY", "order_quantity": 1, "adjacent_target_position": 1}],
        "market": [{"market_order_required": True, "market_order_rows_emitted": True, "market_fallback_status": "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"}],
        "transition": [{"starting_position_contracts": 0, "ending_position_contracts": 1, "working_state_after": "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION", "same_session": True}],
        "fill": [{"fill_executed": True, "fill_quantity": 1, "position_after_fill": 1}],
        "cost": [{"spread_cost_amount": 0.0}],
        "pnl": [{"ending_position_contracts": 1}],
        "validation": [{"source_faithful_evidence_claimed": False}],
    }

    with pytest.raises(CarverBlocked, match="without full-gap or cap-bound trigger"):
        validate_pretest_machine_freeze_rows(rows, computed)


def test_2023_test_market_order_freeze_rejects_mismatched_full_gap_quantity():
    from carver.spine.s27_v2_replay.pretest_machine_freeze import validate_pretest_machine_freeze_rows

    rows = _machine_freeze_pack_rows()
    computed = {
        "position": [{"starting_position_contracts": 0, "desired_position_contracts": 2, "position_change_contracts": 2, "base_position_contracts": 1.0}],
        "order": [{"order_side": "BUY", "order_quantity": 2, "adjacent_target_position": 1}],
        "market": [{"market_order_required": True, "market_order_rows_emitted": True, "market_fallback_status": "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"}],
        "transition": [{"starting_position_contracts": 0, "ending_position_contracts": 2, "working_state_after": "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION", "same_session": True}],
        "fill": [{"fill_executed": True, "fill_quantity": 1, "position_after_fill": 2}],
        "cost": [{"spread_cost_amount": 0.0}],
        "pnl": [{"ending_position_contracts": 2}],
        "validation": [{"source_faithful_evidence_claimed": False}],
    }

    with pytest.raises(CarverBlocked, match="quantity binding"):
        validate_pretest_machine_freeze_rows(rows, computed)


def test_2023_test_market_order_freeze_rejects_locked_status_without_required_emitted_flags():
    from carver.spine.s27_v2_replay.pretest_machine_freeze import validate_pretest_machine_freeze_rows

    rows = _machine_freeze_pack_rows()
    computed = _locked_market_freeze_rows()
    computed["market"][0]["market_order_required"] = False
    computed["market"][0]["market_order_rows_emitted"] = False

    with pytest.raises(CarverBlocked, match="required and emitted"):
        validate_pretest_machine_freeze_rows(rows, computed)


def test_2023_test_market_order_freeze_rejects_wrong_side_for_position_change():
    from carver.spine.s27_v2_replay.pretest_machine_freeze import validate_pretest_machine_freeze_rows

    rows = _machine_freeze_pack_rows()
    computed = _locked_market_freeze_rows()
    computed["order"][0]["order_side"] = "SELL"

    with pytest.raises(CarverBlocked, match="side to match position-change sign"):
        validate_pretest_machine_freeze_rows(rows, computed)


@pytest.mark.parametrize(
    ("family", "field_name", "forged_value"),
    (
        ("transition", "ending_position_contracts", 1),
        ("fill", "position_after_fill", 1),
        ("pnl", "ending_position_contracts", 1),
    ),
)
def test_2023_test_market_order_freeze_rejects_target_position_mismatch(family, field_name, forged_value):
    from carver.spine.s27_v2_replay.pretest_machine_freeze import validate_pretest_machine_freeze_rows

    rows = _machine_freeze_pack_rows()
    computed = _locked_market_freeze_rows()
    computed[family][0][field_name] = forged_value

    with pytest.raises(CarverBlocked, match="target-position binding"):
        validate_pretest_machine_freeze_rows(rows, computed)

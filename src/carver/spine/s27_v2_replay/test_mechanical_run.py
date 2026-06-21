from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .development_recon_run import (
    ACCEPTED_COMMISSION_PER_CONTRACT,
    ANNUAL_TARGET_RISK,
    CAPITAL_ACCOUNT_VALUE,
    CONTRACT_POINT_VALUE,
    FORECAST_CAP_VALUE,
    FORECAST_SCALAR_VALUE,
    FORECAST_TO_POSITION_DIVISOR,
    ZN_TICK_SIZE,
)
from .local_replay import canonical_sha256
from .pretest_machine_freeze import validate_pretest_machine_freeze_rows
from .validation import require_hash


AUTHORIZATION = "S27_V2_CONTROLLED_LOCAL_ONLY_2023_TEST_INPUT_PACK_AND_MECHANICAL_ARTIFACT_RUN_GATE"
PACK_STATUS = "LOCAL_2023_TEST_DECLARED_INPUT_PACK_BUILT_FROM_ALREADY_LOCAL_SOURCE_NOT_RESULT"
RUN_STATUS = "LOCAL_2023_TEST_MECHANICAL_ARTIFACT_RUN_FAIL_CLOSED_NOT_RESULT"
RESULT_STATUS = "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
BACKTEST_STATUS = "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"
PNL_EVALUATION_STATUS = "MECHANICAL_PNL_ROW_CONSTRUCTION_ONLY_NOT_RESULT_INTERPRETATION"
VALUATION_CONVENTION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
MARKET_ORDER_TRIGGER_SOURCE_CONDITION = "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT"
CAP_BOUND_MARKET_ORDER_TRIGGER_SOURCE_CONDITION = "BOOK_REQUIRED_CAP_BOUND_LIMIT_SIDE_NOT_PLACED"
MARKET_FILL_PRICE_PROVENANCE = "MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE"
MARKET_FILL_PRICE_PROVENANCE_BY_SIDE = {
    "BUY": "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE",
    "SELL": "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE",
}
MARKET_COST_ACCOUNTING_CONVENTION = "ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
MARKET_COST_ACCOUNTING_CONVENTION_BY_SIDE = {
    "BUY": MARKET_COST_ACCOUNTING_CONVENTION,
    "SELL": "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST",
}
MARKET_SPREAD_COST_STATUS = "PASS_DATABENTO_TBBO_ASK_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL"
MARKET_SPREAD_COST_STATUS_BY_SIDE = {
    "BUY": "PASS_DATABENTO_TBBO_ASK_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL",
    "SELL": "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL",
}
FAIL_CLOSED_BLOCKER_STATUS = "FAIL_CLOSED_RESULT_NOT_AUTHORIZED_AFTER_MARKET_ORDER_PNL_EMITTED_NOT_RESULT"
FAIL_CLOSED_UNSUPPORTED_MARKET_CONTINUATION_STATUS = (
    "FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT"
)
FAIL_CLOSED_CAP_BOUND_MARKET_CONTINUATION_STATUS = (
    "FAIL_CLOSED_CAP_BOUND_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT"
)
FAIL_CLOSED_STALE_MARKET_SPREAD_EVIDENCE_STATUS = (
    "FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_STALE_OR_SIDE_MISMATCH_FOR_CONTINUATION_NOT_RESULT"
)
FAIL_CLOSED_LIVE_ORDER_ROLL_BOUNDARY_STATUS = (
    "FAIL_CLOSED_LIVE_ORDER_ON_UNRESOLVED_ROLL_BOUNDARY_DATE_NOT_RESULT"
)
ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION = (
    "LOCAL_ONLY_ENGINEERING_ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ASSUMPTION_NOT_BOOK_EXPLICIT_NOT_SOURCE_FAITHFUL"
)
ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS = (
    "LOCAL_ENGINEERING_ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSED_ROW_EMITTED_NOT_RESULT"
)
CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL = "NOT_APPLICABLE_CAP_BOUND_MARKET_ORDER_LIMIT_SIDE_NOT_PLACED"
MARKET_TBBO_SPREAD_EVIDENCE_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_row1_znh3_tbbo/"
    "ledger/20260612_S27_V2_2023_TEST_ROW1_ZNH3_MARKET_SPREAD_TBBO_selected_spread_ledger.csv"
)
ROW2_MARKET_TBBO_SPREAD_EVIDENCE_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_row2_znh3_tbbo/"
    "ledger/20260612_S27_V2_2023_TEST_ROW2_ZNH3_MARKET_SPREAD_TBBO_selected_spread_ledger.csv"
)
MARKET_TBBO_BATCH_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_batch_evidence/"
    "ledger/20260612_S27_V2_2023_TEST_MARKET_ORDER_TBBO_BATCH_selected_spread_registry.csv"
)
MARKET_TBBO_FAILED_RETRY_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_failed_window_retry/"
    "ledger/20260612_S27_V2_2023_TEST_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_selected_spread_registry.csv"
)
MARKET_TBBO_ROW215_POLICY_RECORD_RELATIVE_PATH = (
    "docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW215_TBBO_POLICY_DECISION_2026-06-12.md"
)
COMBINED_MARKET_TBBO_REGISTRY_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_combined_market_order_tbbo_registry"
)
COMBINED_MARKET_TBBO_REGISTRY_NAME = "combined_market_order_tbbo_registry.csv"
COMBINED_MARKET_TBBO_MANIFEST_NAME = "combined_market_order_tbbo_registry_manifest.json"
COMBINED_MARKET_TBBO_SHA256_NAME = "combined_market_order_tbbo_registry_sha256.csv"
STANDING_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260613_2023_test_standing_market_order_tbbo_batch_evidence/"
    "ledger/20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_BATCH_selected_spread_registry.csv"
)
STANDING_MARKET_TBBO_RETRY_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260613_2023_test_standing_market_order_tbbo_failed_window_retry/"
    "ledger/20260613_S27_V2_2023_TEST_STANDING_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_selected_spread_registry.csv"
)
ROW437_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260613_2023_test_row437_market_order_tbbo/"
    "ledger/20260613_S27_V2_2023_TEST_ROW437_MARKET_ORDER_TBBO_selected_spread_registry.csv"
)
ROW438_MARKET_TBBO_RETRY_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260613_2023_test_row438_market_order_tbbo_failed_window_retry/"
    "ledger/20260613_S27_V2_2023_TEST_ROW438_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_selected_spread_registry.csv"
)
ROW441_MARKET_TBBO_EXTENDED_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260614_2023_test_row441_market_order_tbbo_extended_lookback/"
    "ledger/20260614_S27_V2_2023_TEST_ROW441_MARKET_ORDER_TBBO_EXTENDED_LOOKBACK_selected_spread_registry.csv"
)
ROW547_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260614_2023_test_row547_cap_bound_market_order_tbbo/"
    "ledger/20260614_S27_V2_2023_TEST_ROW547_CAP_BOUND_MARKET_ORDER_TBBO_selected_spread_registry.csv"
)
ZNM3_EXTENDED_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260614_2023_test_znm3_market_order_tbbo_extended_lookback/"
    "ledger/20260614_S27_V2_2023_TEST_ZNM3_MARKET_ORDER_TBBO_EXTENDED_LOOKBACK_selected_spread_registry.csv"
)
ROW704_MBP1_TOP_OF_BOOK_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260614_2023_test_row704_mbp1_top_of_book_evidence/"
    "ledger/20260614_S27_V2_2023_TEST_ROW704_MBP1_TOP_OF_BOOK_EVIDENCE_selected_spread_registry.csv"
)
ROW1356_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260616_2023_test_row1356_post_fill_tbbo_engineering_convention/"
    "ledger/20260616_S27_V2_2023_TEST_ROW1356_POST_FILL_TBBO_ENGINEERING_selected_spread_registry.csv"
)
ROW1364_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260617_2023_test_row1364_market_order_tbbo/"
    "ledger/20260617_S27_V2_2023_TEST_ROW1364_MARKET_ORDER_TBBO_selected_spread_registry.csv"
)
ROW1366_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260617_2023_test_row1366_market_order_tbbo/"
    "ledger/20260617_S27_V2_2023_TEST_ROW1366_MARKET_ORDER_TBBO_selected_spread_registry.csv"
)
ROW1369_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260617_2023_test_row1369_market_order_tbbo/"
    "ledger/20260617_S27_V2_2023_TEST_ROW1369_MARKET_ORDER_TBBO_selected_spread_registry.csv"
)
ROW1370_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260620_2023_test_row1370_market_order_tbbo/"
    "ledger/20260620_S27_V2_2023_TEST_ROW1370_MARKET_ORDER_TBBO_selected_spread_registry.csv"
)
ROW1374_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260620_2023_test_row1374_market_order_tbbo/"
    "ledger/20260620_S27_V2_2023_TEST_ROW1374_MARKET_ORDER_TBBO_selected_spread_registry.csv"
)
ROW1378_MARKET_TBBO_SELECTED_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/20260621_2023_test_row1378_post_fill_tbbo_engineering_convention/"
    "ledger/20260621_S27_V2_2023_TEST_ROW1378_POST_FILL_TBBO_ENGINEERING_selected_spread_registry.csv"
)
MARKET_TBBO_SPREAD_EVIDENCE_BY_ROW = {
    1: {
        "path": MARKET_TBBO_SPREAD_EVIDENCE_RELATIVE_PATH,
        "row_index": "1",
        "fill_timestamp_utc": "2023-01-03T01:00:00Z",
        "raw_symbol": "ZNH3",
        "market_order_side": "",
        "selected_quote_ts_event": "2023-01-03T00:59:57.009985Z",
        "bid_px_00": "112.546875",
        "ask_px_00": "112.5625",
        "selected_executable_market_fill_price": "112.5625",
        "executable_market_fill_price_source": "ASK_PRICE_FOR_BUY_MARKET_ORDER",
        "spread_points": "0.015625",
        "point_value_usd": "1000.0",
        "spread_cost_usd_per_contract": "15.625",
        "fill_quantity": "2",
        "spread_cost_amount_usd": "31.25",
        "spread_source": "DATABENTO_TBBO_SELECTED_QUOTE_AT_OR_BEFORE_MARKET_FILL",
        "cost_classification": "SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_NOT_BOOK_EXPLICIT",
        "actual_cost_emission_authorized": "FALSE",
        "pnl_result_emission_authorized": "FALSE",
        "row_hash": "c910df21177b2e1aa0cfcd5edadd03be38f130e8b06cb8f4b2bca79bf8390d0b",
        "selected_spread_ledger_sha256": "c3a2a0bdd59e03e8c362f63d791b870609d1af1177144d7e78406daec6ca8343",
    },
    2: {
        "path": ROW2_MARKET_TBBO_SPREAD_EVIDENCE_RELATIVE_PATH,
        "row_index": "2",
        "fill_timestamp_utc": "2023-01-03T02:00:00Z",
        "raw_symbol": "ZNH3",
        "market_order_side": "SELL",
        "selected_quote_ts_event": "2023-01-03T01:59:56.651440427Z",
        "quote_age_seconds": "3.34856",
        "bid_px_00": "112.578125",
        "ask_px_00": "112.59375",
        "selected_executable_market_fill_price": "112.578125",
        "executable_market_fill_price_source": "BID_PRICE_FOR_SELL_MARKET_ORDER",
        "spread_points": "0.015625",
        "point_value_usd": "1000.0",
        "spread_cost_usd_per_contract": "15.625",
        "fill_quantity": "2",
        "spread_cost_amount_usd": "31.25",
        "spread_source": "DATABENTO_TBBO_SELECTED_QUOTE_AT_OR_BEFORE_MARKET_FILL",
        "cost_classification": "SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_NOT_BOOK_EXPLICIT",
        "actual_cost_emission_authorized": "FALSE",
        "pnl_result_emission_authorized": "FALSE",
        "row_hash": "0785dcfa6525897f07344c9f016cf832217e94cd79e2e6e4c3220b7f70d6d0b7",
        "selected_spread_ledger_sha256": "aa1240a937ef7a4be30c1851ee708c26b2a4d7d6e7c30f518efa85e008079be8",
    },
}
_EXPECTED_MARKET_SPREAD_EVIDENCE_CACHE: dict[str, Any] | None = None
ROW215_ENGINEERING_TBBO_EVIDENCE = {
    "path": MARKET_TBBO_FAILED_RETRY_SELECTED_RELATIVE_PATH,
    "policy_record_path": MARKET_TBBO_ROW215_POLICY_RECORD_RELATIVE_PATH,
    "row_index": "215",
    "decision_timestamp_utc": "2023-01-16T16:00:00Z",
    "fill_timestamp_utc": "2023-01-16T17:00:00Z",
    "raw_symbol": "ZNH3",
    "market_order_side": "SELL",
    "selected_quote_ts_event": "2023-01-16T17:00:00.681503831Z",
    "quote_age_seconds": "-0.681503831",
    "bid_px_00": "114.625",
    "ask_px_00": "114.640625",
    "selected_executable_market_fill_price": "114.625",
    "executable_market_fill_price_source": "BID_PRICE_FOR_SELL_MARKET_ORDER_ROW215_ENGINEERING_AFTER_FILL",
    "spread_points": "0.015625",
    "point_value_usd": "1000.0",
    "spread_cost_usd_per_contract": "15.625",
    "fill_quantity": "2",
    "spread_cost_amount_usd": "31.25",
    "spread_source": "ROW215_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT",
    "selection_rule": "ROW215_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT",
    "post_fill_quote_selection": "ROW215_ONLY_ACCEPTED_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT",
    "cost_classification": "SOURCE_NATIVE_PROVIDER_BID_ASK_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT",
    "actual_cost_emission_authorized": "FALSE",
    "pnl_result_emission_authorized": "FALSE",
    "raw_dbn_sha256": "D0E90468C0B3DE8449BE1A3EC1F00E86B58E9BEA070692701D09D3807D558854",
    "raw_csv_sha256": "E61AF6FE47224E084AFDFC8CEA381463C93D869F5E36E35EAC0A29E62DCF65D0",
}
SECONDARY_SESSION_EOD_BLOCKER_STATUS = "SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT"
ROW303_SESSION_END_MARKET_FILL_POLICY_STATUS = (
    "ROW303_SESSION_END_MARKET_FILL_ALLOWED_WITH_NEXT_SESSION_ENGINEERING_VALUATION_NOT_RESULT"
)
ROW391_SESSION_END_MARKET_FILL_POLICY_STATUS = (
    "ROW391_SESSION_END_MARKET_FILL_ALLOWED_WITH_NEXT_SESSION_ENGINEERING_VALUATION_NOT_RESULT"
)
ROW1113_SESSION_END_MARKET_VALUATION_GAP_CONVENTION = (
    "SOURCE_NATIVE_ENGINEERING_SESSION_END_MARKET_ORDER_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT"
)
ROW1113_SESSION_END_MARKET_VALUATION_GAP_POLICY_STATUS = (
    "ROW1113_SESSION_END_MARKET_FILL_ALLOWED_WITH_NEXT_AVAILABLE_VALUATION_GAP_ENGINEERING_VALUATION_NOT_RESULT"
)
ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_CONVENTION = (
    "SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT"
)
ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_ROW_STATUS = (
    "LOCAL_ENGINEERING_SESSION_OPEN_MARKET_RESET_MARKET_ORDER_ROW_EMITTED_NOT_RESULT"
)
ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_CONVENTION = (
    "SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT"
)
ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_RULE = (
    "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_WITH_SESSION_OPEN_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
)
ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_ROW_STATUS = (
    "LOCAL_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ROW_EMITTED_NOT_RESULT"
)
ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_CONVENTION = (
    "SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT"
)
ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_RULE = (
    "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_SESSION_VALUATION_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
)
ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_ROW_STATUS = (
    "LOCAL_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ROW_EMITTED_NOT_RESULT"
)
ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_CONVENTION = (
    "SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT"
)
ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_RULE = (
    "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_AVAILABLE_VALUATION_GAP_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
)
ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS = (
    "LOCAL_ENGINEERING_SESSION_END_ADJACENT_LIMIT_VALUATION_GAP_ROW_EMITTED_NOT_RESULT"
)
SESSION_MARKET_TBBO_EVIDENCE_TYPES = (
    "BATCH_AT_OR_BEFORE_FILL_TBBO",
    "DIRECT_AT_OR_BEFORE_FILL_TBBO",
    "PREBOUND_ROW_1_TBBO",
    "PREBOUND_ROW_2_TBBO",
    "RETRY_AT_OR_BEFORE_FILL_TBBO",
    "STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO",
    "STANDING_RETRY_AT_OR_BEFORE_FILL_TBBO",
    "ROW437_BOUNDED_AT_OR_BEFORE_FILL_TBBO",
    "ROW438_RETRY_AT_OR_BEFORE_FILL_TBBO",
    "ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO",
    "ROW547_CAP_BOUND_AT_OR_BEFORE_FILL_TBBO",
    "ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO",
    "ROW704_ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL",
    "ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION",
    "ROW1364_AT_OR_BEFORE_FILL_TBBO",
    "ROW1366_AT_OR_BEFORE_FILL_TBBO",
    "ROW1369_AT_OR_BEFORE_FILL_TBBO",
    "ROW1370_AT_OR_BEFORE_FILL_TBBO",
    "ROW1374_AT_OR_BEFORE_FILL_TBBO",
    "ROW1378_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION",
)
MARKET_TBBO_SELECTION_STATUSES = (
    "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT",
    "PASS_PREBOUND_TBBO_QUOTE_SELECTED_NOT_RESULT",
    "PASS_ROW215_ENGINEERING_AFTER_FILL_TBBO_QUOTE_SELECTED_NOT_RESULT",
    "PASS_ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT",
    "PASS_ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT",
    "PASS_ROW704_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL_SELECTED_NOT_RESULT",
    "PASS_ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_QUOTE_SELECTED_NOT_RESULT",
    "PASS_ROW1378_FIRST_POST_FILL_TBBO_ENGINEERING_QUOTE_SELECTED_NOT_RESULT",
)
FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_STATUS = (
    "FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_TARGET_POSITION_ZERO_NOT_RESULT"
)
FAIL_CLOSED_ADJACENT_LIMIT_CAP_BOUND_STATUS = (
    "FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_CAP_BOUND_TARGET_NOT_RESULT"
)
NO_FAIL_CLOSED_BLOCKER_PACK_EXHAUSTED_STATUS = (
    "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
RUN_ID = "20260612_S27_V2_2023_TEST_MECHANICAL"

PRE2023_SOURCE_ROOT = (
    _REPO_ROOT
    / "docs/researchops/s27_v2_databento_older_zn_history/20260611_pre2023_zn_dev_recon_download_build/ledger"
)
PRE2023_CONTINUOUS = PRE2023_SOURCE_ROOT / (
    "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_local_continuous_daily_risk_history.csv"
)
PRE2023_ROLLS = PRE2023_SOURCE_ROOT / "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_roll_plan.csv"

LOCAL_2023_RAW_ROOT = (
    _REPO_ROOT / "docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN"
)
LOCAL_2023_ROLL_PLAN = LOCAL_2023_RAW_ROOT / "local_lineage/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_ZN_daily_roll_plan.csv"
LOCAL_2023_HOURLY_CONDITION = _REPO_ROOT / (
    "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
    "hourly_archive_quarantine/provider_condition_resolution/strategy_facing_hourly_bars/"
    "20260531_S27_ZN_2022_2023_PROVIDER_CONDITION_OPTION_C_strategy_facing_available_ohlcv_1h.csv"
)

SOURCE_BUILD_RELATIVE_PATH = (
    "docs/researchops/s27_v2_2023_test_local_source_build/"
    "20260612_2023_test_from_already_local_2022_2023_source"
)
DEFAULT_PACK_RELATIVE_PATH = "docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack"
DEFAULT_OUTPUT_RELATIVE_PATH = "docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run"
DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH = (
    "docs/researchops/s27_v2_market_spread_evidence/ZN/"
    "20260612_2023_test_market_order_tbbo_requirements_discovery"
)
DEFAULT_MANIFEST_NAME = "S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST.json"
DEFAULT_SHA256SUMS_NAME = "S27_V2_2023_TEST_DECLARED_INPUT_PACK_SHA256SUMS.txt"
TBBO_REQUIREMENTS_AUTHORIZATION = "S27_V2_LOCAL_ONLY_2023_TEST_MARKET_ORDER_TBBO_REQUIREMENTS_DISCOVERY_GATE"
TBBO_REQUIREMENTS_STATUS = "LOCAL_ONLY_2023_TEST_MARKET_ORDER_TBBO_REQUIREMENTS_DISCOVERED_NOT_PROVIDER_NOT_RESULT"
TBBO_REQUIREMENT_LEDGER_NAME = "market_order_tbbo_requirements.csv"
TBBO_REQUIREMENT_MANIFEST_NAME = "market_order_tbbo_requirements_manifest.json"
TBBO_REQUIREMENT_SHA256_NAME = "market_order_tbbo_requirements_sha256.csv"

SOURCE_CONTINUOUS_NAME = f"{RUN_ID}_continuous_daily.csv"
SOURCE_ROLL_NAME = f"{RUN_ID}_roll_plan.csv"
SOURCE_HOURLY_NAME = f"{RUN_ID}_hourly_available.csv"
SOURCE_EXCLUSION_NAME = f"{RUN_ID}_source_exclusions.csv"

ROW_FAMILY_FILES = (
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

AUTHORIZED_2023_TEST_DECLARED_PACK_ROW_LIMIT = 1378

RUN_LEDGER_FIELDNAMES = {
    "runtime_history_ledger.csv": ("row_index", "runtime_evidence_row_hash", "ewma5", "trend", "sigma", "vqm_multiplier_m", "row_status", "row_hash"),
    "forecast_replay_ledger.csv": ("row_index", "decision_timestamp_utc", "raw_forecast", "risk_adjusted_forecast", "capped_forecast", "row_status", "row_hash"),
    "desired_position_ledger.csv": ("row_index", "starting_position_contracts", "desired_position_contracts", "position_change_contracts", "base_position_contracts", "row_status", "row_hash"),
    "limit_order_ledger.csv": ("row_index", "order_side", "order_quantity", "adjacent_target_position", "formula_limit_price", "limit_order_price", "row_status", "row_hash"),
    "no_market_order_ledger.csv": ("row_index", "market_order_required", "market_order_rows_emitted", "market_fallback_status", "engineering_convention_label", "row_status", "row_hash"),
    "market_order_ledger.csv": ("row_index", "decision_timestamp_utc", "raw_symbol", "current_position_before_order", "target_position_after_fill", "order_side", "order_quantity", "trigger_source_condition", "market_order_rows_emitted", "engineering_convention_label", "order_status", "row_status", "row_hash"),
    "working_order_transition_ledger.csv": ("row_index", "starting_position_contracts", "ending_position_contracts", "working_state_before", "working_state_after", "same_session", "row_status", "row_hash"),
    "fill_ledger.csv": ("row_index", "fill_executed", "fill_rule", "fill_candidate_close", "fill_price", "fill_quantity", "position_after_fill", "row_status", "row_hash"),
    "market_fill_metadata_ledger.csv": ("row_index", "fill_timestamp_utc", "raw_symbol", "order_side", "fill_quantity", "fill_price", "fill_price_provenance", "fill_source_row_hash", "same_session", "roll_boundary_status", "working_state_before", "position_after_fill", "commission_per_contract", "commission_amount", "market_spread_cost_status", "pnl_emission_status", "row_status", "row_hash"),
    "cost_ledger.csv": ("row_index", "cost_policy_id", "order_cost_type", "commission_amount", "spread_cost_amount", "total_cost_amount", "currency", "market_cost_accounting_convention", "spread_cost_reason", "tbbo_quote_ts_event", "tbbo_bid_px", "tbbo_ask_px", "tbbo_full_spread_points", "tbbo_full_spread_value_per_contract", "tbbo_selected_spread_row_hash", "tbbo_selected_spread_ledger_sha256", "row_status", "row_hash"),
    "pnl_ledger.csv": ("row_index", "valuation_mark_timestamp_utc", "valuation_mark_close_price", "valuation_convention_label", "existing_position_gross_pnl", "fill_gross_pnl", "row_gross_pnl_amount", "row_net_pnl_amount", "cumulative_gross_pnl_amount", "cumulative_commission_amount", "cumulative_spread_amount", "cumulative_net_pnl_amount", "ending_position_contracts", "result_status", "backtest_status", "pnl_evaluation_status", "source_faithful_evidence_claimed", "row_status", "row_hash"),
    "validation_ledger.csv": ("row_index", "result_status", "backtest_status", "source_faithful_evidence_claimed", "non_authorizations", "row_status", "row_hash"),
    "fail_closed_ledger.csv": ("row_index", "decision_timestamp_utc", "raw_symbol", "starting_position_contracts", "desired_position_contracts", "position_change_contracts", "order_side", "adjacent_target_position", "trend", "market_order_required", "market_order_rows_emitted", "market_order_reason", "market_fill_metadata_rows_emitted", "market_fill_price_provenance", "market_fill_price", "commission_per_contract", "commission_amount", "market_spread_cost_status", "secondary_fail_closed_reason", "formula_limit_price", "limit_order_price", "fill_candidate_timestamp_utc", "fill_candidate_close", "fill_executed", "same_session", "fail_closed_reason", "result_status", "backtest_status", "source_faithful_evidence_claimed", "row_status", "row_hash"),
}

NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_VALIDATION_ACCESS",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_RESULT_INTERPRETATION",
    "NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION",
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)


@dataclass(frozen=True)
class TestMechanicalRunConfig:
    input_pack_path: str
    output_root: str
    manifest_name: str = DEFAULT_MANIFEST_NAME


@dataclass(frozen=True)
class TestMechanicalRunBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    output_root: str
    candidate_row_count: int
    supported_mechanical_row_count: int
    fail_closed_row_index: int
    fail_closed_reason: str
    final_position_contracts: int
    cumulative_gross_pnl_amount: float
    cumulative_commission_amount: float
    cumulative_spread_amount: float
    cumulative_net_pnl_amount: float
    run_manifest_hash: str
    evidence_manifest_hash: str
    trusted_bundle_hash: str
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != RUN_STATUS or self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 2023 TEST mechanical run status/authorization is not locked")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT or self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 2023 TEST run must remain S27_V2 ZN source-native futures")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 2023 TEST run must preserve non-authorizations")
        if self.fail_closed_row_index != 0 and self.fail_closed_row_index < self.supported_mechanical_row_count:
            raise CarverBlocked("S27 v2 2023 TEST fail-closed row must not precede supported rows")
        output_root = Path(self.output_root).resolve()
        manifest = _safe_read_json(output_root / "run_manifest.json", "S27 v2 2023 TEST run manifest")
        evidence = _safe_read_json(output_root / "evidence_manifest.json", "S27 v2 2023 TEST evidence manifest")
        trusted = _safe_read_json(output_root / "trusted_bundle.json", "S27 v2 2023 TEST trusted bundle")
        pnl_rows = _safe_read_csv_rows(output_root / "pnl_ledger.csv", "S27 v2 2023 TEST pnl ledger")
        position_rows = _safe_read_csv_rows(
            output_root / "desired_position_ledger.csv",
            "S27 v2 2023 TEST desired-position ledger",
        )
        market_order_rows = _safe_read_csv_rows(
            output_root / "market_order_ledger.csv",
            "S27 v2 2023 TEST market-order ledger",
        )
        market_fill_metadata_rows = _safe_read_csv_rows(
            output_root / "market_fill_metadata_ledger.csv",
            "S27 v2 2023 TEST market-fill metadata ledger",
        )
        no_market_rows = _safe_read_csv_rows(
            output_root / "no_market_order_ledger.csv",
            "S27 v2 2023 TEST no-market-order ledger",
        )
        order_rows = _safe_read_csv_rows(output_root / "limit_order_ledger.csv", "S27 v2 2023 TEST order ledger")
        cost_rows = _safe_read_csv_rows(output_root / "cost_ledger.csv", "S27 v2 2023 TEST cost ledger")
        transition_rows = _safe_read_csv_rows(
            output_root / "working_order_transition_ledger.csv",
            "S27 v2 2023 TEST working-order transition ledger",
        )
        fill_rows = _safe_read_csv_rows(output_root / "fill_ledger.csv", "S27 v2 2023 TEST fill ledger")
        fail_rows = _safe_read_csv_rows(output_root / "fail_closed_ledger.csv", "S27 v2 2023 TEST fail-closed ledger")
        for label, value in (
            ("run manifest", self.run_manifest_hash),
            ("evidence manifest", self.evidence_manifest_hash),
            ("trusted bundle", self.trusted_bundle_hash),
            ("bundle", self.bundle_hash),
        ):
            require_hash(f"S27 v2 2023 TEST {label} hash", value)
        if self.run_manifest_hash != _sha256(output_root / "run_manifest.json"):
            raise CarverBlocked("S27 v2 2023 TEST run manifest hash must bind bytes")
        if self.evidence_manifest_hash != _sha256(output_root / "evidence_manifest.json"):
            raise CarverBlocked("S27 v2 2023 TEST evidence manifest hash must bind bytes")
        if self.trusted_bundle_hash != _sha256(output_root / "trusted_bundle.json"):
            raise CarverBlocked("S27 v2 2023 TEST trusted bundle hash must bind bytes")
        if str(manifest.get("input_pack_path")) != self.input_pack_path:
            raise CarverBlocked("S27 v2 2023 TEST input pack path must bind run manifest")
        if int(manifest.get("candidate_row_count", 0)) != self.candidate_row_count:
            raise CarverBlocked("S27 v2 2023 TEST candidate row count must bind run manifest")
        if int(manifest.get("supported_mechanical_row_count", 0)) != self.supported_mechanical_row_count:
            raise CarverBlocked("S27 v2 2023 TEST supported row count must bind run manifest")
        ledger_hashes = evidence.get("ledger_hashes")
        if not isinstance(ledger_hashes, dict):
            raise CarverBlocked("S27 v2 2023 TEST evidence manifest must bind ledger hashes")
        for filename in manifest.get("artifact_files", ()):
            declared_hash = str(ledger_hashes.get(str(filename), "")).lower()
            if declared_hash != _sha256(output_root / str(filename)).lower():
                raise CarverBlocked("S27 v2 2023 TEST evidence manifest ledger hash must bind current bytes")
        if len(pnl_rows) != self.supported_mechanical_row_count:
            raise CarverBlocked("S27 v2 2023 TEST supported row count must bind pnl ledger length")
        if len(no_market_rows) != self.supported_mechanical_row_count:
            raise CarverBlocked("S27 v2 2023 TEST supported row count must bind no-market ledger length")
        if self.supported_mechanical_row_count >= 1:
            first_market_state = no_market_rows[0]
            if (
                str(first_market_state.get("row_index")) != "1"
                or str(first_market_state.get("market_order_required")).upper() != "TRUE"
                or str(first_market_state.get("market_order_rows_emitted")).upper() != "TRUE"
                or str(first_market_state.get("market_fallback_status")) != "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
            ):
                raise CarverBlocked("S27 v2 2023 TEST row-1 no-market state must bind locked market execution")
        if self.fail_closed_row_index == 0:
            if fail_rows or self.fail_closed_reason != NO_FAIL_CLOSED_BLOCKER_PACK_EXHAUSTED_STATUS:
                raise CarverBlocked("S27 v2 2023 TEST pack-exhausted terminal state must bind header-only fail ledger")
            if self.supported_mechanical_row_count != self.candidate_row_count:
                raise CarverBlocked("S27 v2 2023 TEST pack-exhausted terminal state must support every declared row")
        else:
            if len(fail_rows) != 1 or int(fail_rows[0]["row_index"]) != self.fail_closed_row_index:
                raise CarverBlocked("S27 v2 2023 TEST fail-closed ledger must bind blocker row")
            if str(fail_rows[0]["fail_closed_reason"]) != self.fail_closed_reason:
                raise CarverBlocked("S27 v2 2023 TEST fail-closed reason must bind bundle")
        emitted_market_indices = {
            str(row["row_index"])
            for row in no_market_rows
            if str(row.get("market_order_required")).upper() == "TRUE"
            or str(row.get("market_order_rows_emitted")).upper() == "TRUE"
        }
        actual_market_indices = {str(row["row_index"]) for row in market_order_rows}
        actual_fill_metadata_indices = {str(row["row_index"]) for row in market_fill_metadata_rows}
        actual_cost_indices = {str(row["row_index"]) for row in cost_rows}
        if emitted_market_indices != actual_market_indices or emitted_market_indices != actual_fill_metadata_indices:
            raise CarverBlocked("S27 v2 2023 TEST supported market state must bind market order and fill metadata rows")
        if emitted_market_indices - actual_cost_indices:
            raise CarverBlocked("S27 v2 2023 TEST supported market state must bind same-row cost rows")
        position_by_index = {str(row["row_index"]): row for row in position_rows}
        no_market_by_index = {str(row["row_index"]): row for row in no_market_rows}
        order_by_index = {str(row["row_index"]): row for row in order_rows}
        cost_by_index = {str(row["row_index"]): row for row in cost_rows}
        transition_by_index = {str(row["row_index"]): row for row in transition_rows}
        fill_by_index = {str(row["row_index"]): row for row in fill_rows}
        pnl_by_index = {str(row["row_index"]): row for row in pnl_rows}
        if market_order_rows or market_fill_metadata_rows:
            if len(market_order_rows) != len(emitted_market_indices) or len(market_fill_metadata_rows) != len(emitted_market_indices):
                raise CarverBlocked("S27 v2 2023 TEST supported market rows must bind every emitted market order and fill metadata row")
            if len(cost_rows) < 1:
                raise CarverBlocked("S27 v2 2023 TEST supported market rows must bind at least one cost row")
            market_order_by_index = {str(row["row_index"]): row for row in market_order_rows}
            market_fill_by_index = {str(row["row_index"]): row for row in market_fill_metadata_rows}
            for row_index in sorted(emitted_market_indices, key=int):
                market_order = market_order_by_index[row_index]
                market_fill = market_fill_by_index[row_index]
                cost_row = cost_by_index.get(row_index)
                if cost_row is None:
                    raise CarverBlocked("S27 v2 2023 TEST supported market rows must bind a same-row cost row")
                side = str(market_order["order_side"])
                quantity = str(market_order["order_quantity"])
                target_position = str(market_order["target_position_after_fill"])
                if str(market_fill["fill_quantity"]) != quantity:
                    raise CarverBlocked("S27 v2 2023 TEST market order must bind full-gap quantity")
                if str(market_fill["position_after_fill"]) != target_position:
                    raise CarverBlocked("S27 v2 2023 TEST market fill must bind target position")
                expected_trigger = _expected_market_trigger_source_condition(order_by_index.get(row_index, {}))
                if str(market_order["trigger_source_condition"]) != expected_trigger:
                    raise CarverBlocked("S27 v2 2023 TEST market-order trigger must bind source condition")
                if str(market_fill["fill_price_provenance"]) != MARKET_FILL_PRICE_PROVENANCE_BY_SIDE[side]:
                    raise CarverBlocked("S27 v2 2023 TEST market-fill provenance must bind side-specific market-fill policy")
                if str(market_fill["market_spread_cost_status"]) != MARKET_SPREAD_COST_STATUS_BY_SIDE[side]:
                    raise CarverBlocked("S27 v2 2023 TEST market-fill metadata must bind side-specific market spread cost accounting")
                active_evidence = _load_market_spread_evidence(int(row_index), side, str(market_fill["fill_timestamp_utc"]))
                expected_fill_price = _market_fill_price_from_evidence(active_evidence, side)
                if float(market_fill["fill_price"]) != expected_fill_price:
                    raise CarverBlocked("S27 v2 2023 TEST market-fill price must bind selected side-specific TBBO executable price")
                expected_order_cost_type = f"MARKET_ORDER_{side}_{'ASK' if side == 'BUY' else 'BID'}_FILL_ACTUAL_COST_NOT_PNL"
                if str(cost_row["order_cost_type"]) != expected_order_cost_type:
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind side-specific order cost type")
                if str(cost_row["market_cost_accounting_convention"]) != MARKET_COST_ACCOUNTING_CONVENTION_BY_SIDE[side]:
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind no-double-counting accounting")
                if str(cost_row["currency"]) != "USD":
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind USD currency")
                if str(cost_row["tbbo_quote_ts_event"]) != active_evidence["selected_quote_ts_event"]:
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind selected TBBO quote timestamp")
                if float(cost_row["tbbo_bid_px"]) != float(active_evidence["bid_px_00"]):
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind selected TBBO bid")
                if float(cost_row["tbbo_ask_px"]) != float(active_evidence["ask_px_00"]):
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind selected TBBO ask")
                if float(cost_row["tbbo_full_spread_points"]) != float(active_evidence["spread_points"]):
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind selected TBBO spread points")
                if float(cost_row["tbbo_full_spread_value_per_contract"]) != float(active_evidence["spread_cost_usd_per_contract"]):
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind selected TBBO spread value")
                if str(cost_row["tbbo_selected_spread_row_hash"]) != active_evidence["row_hash"]:
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind selected TBBO row hash")
                if str(cost_row["tbbo_selected_spread_ledger_sha256"]).lower() != active_evidence["selected_spread_ledger_sha256"].lower():
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind selected TBBO ledger hash")
                expected_commission = ACCEPTED_COMMISSION_PER_CONTRACT * int(quantity)
                if float(cost_row["commission_amount"]) != expected_commission or float(cost_row["spread_cost_amount"]) != 0.0:
                    raise CarverBlocked("S27 v2 2023 TEST market-order cost row must bind authorized cost amounts")
                if float(cost_row["total_cost_amount"]) != expected_commission:
                    raise CarverBlocked("S27 v2 2023 TEST market-order total cost must equal commission under no-double-counting accounting")
                _validate_market_execution_session_class(
                    input_pack_root=Path(self.input_pack_path).resolve(),
                    row_index=row_index,
                    no_market=no_market_by_index.get(row_index, {}),
                    market_order=market_order,
                    market_fill=market_fill,
                    transition=transition_by_index.get(row_index, {}),
                    fill=fill_by_index.get(row_index, {}),
                    pnl=pnl_by_index.get(row_index, {}),
                    market_spread_evidence=active_evidence,
                )
            if "304" in emitted_market_indices:
                _validate_row304_engineering_session_open_artifacts(
                    input_pack_root=Path(self.input_pack_path).resolve(),
                    no_market=no_market_by_index.get("304", {}),
                    market_order=market_order_by_index["304"],
                    market_fill=market_fill_by_index["304"],
                    transition=transition_by_index.get("304", {}),
                    fill=fill_by_index.get("304", {}),
                    cost=cost_by_index.get("304", {}),
                    pnl=pnl_by_index.get("304", {}),
                )
            if self.supported_mechanical_row_count >= 346:
                _validate_row346_target_zero_adjacent_limit_artifacts(
                    input_pack_root=Path(self.input_pack_path).resolve(),
                    order=order_by_index.get("346", {}),
                    no_market=no_market_by_index.get("346", {}),
                    transition=transition_by_index.get("346", {}),
                    fill=fill_by_index.get("346", {}),
                    cost=cost_by_index.get("346", {}),
                    pnl=pnl_by_index.get("346", {}),
                )
            if self.supported_mechanical_row_count >= 436:
                _validate_row436_session_open_adjacent_limit_artifacts(
                    input_pack_root=Path(self.input_pack_path).resolve(),
                    order=order_by_index.get("436", {}),
                    no_market=no_market_by_index.get("436", {}),
                    transition=transition_by_index.get("436", {}),
                    fill=fill_by_index.get("436", {}),
                    cost=cost_by_index.get("436", {}),
                    pnl=pnl_by_index.get("436", {}),
                )
            if "391" in emitted_market_indices:
                _validate_row391_session_end_market_artifacts(
                    input_pack_root=Path(self.input_pack_path).resolve(),
                    no_market=no_market_by_index.get("391", {}),
                    market_order=market_order_by_index["391"],
                    market_fill=market_fill_by_index["391"],
                    transition=transition_by_index.get("391", {}),
                    fill=fill_by_index.get("391", {}),
                    cost=cost_by_index.get("391", {}),
                    pnl=pnl_by_index.get("391", {}),
                )
        if self.supported_mechanical_row_count >= 701:
            _validate_row701_roll_boundary_no_new_order_suppression_artifacts(
                input_pack_root=Path(self.input_pack_path).resolve(),
                position=position_by_index.get("701", {}),
                order=order_by_index.get("701", {}),
                no_market=no_market_by_index.get("701", {}),
                transition=transition_by_index.get("701", {}),
                fill=fill_by_index.get("701", {}),
                cost=cost_by_index.get("701", {}),
                pnl=pnl_by_index.get("701", {}),
                market_order_present="701" in actual_market_indices,
                market_fill_present="701" in actual_fill_metadata_indices,
            )
        if self.supported_mechanical_row_count >= 892:
            _validate_row892_session_end_adjacent_limit_artifacts(
                input_pack_root=Path(self.input_pack_path).resolve(),
                position=position_by_index.get("892", {}),
                order=order_by_index.get("892", {}),
                no_market=no_market_by_index.get("892", {}),
                transition=transition_by_index.get("892", {}),
                fill=fill_by_index.get("892", {}),
                cost=cost_by_index.get("892", {}),
                pnl=pnl_by_index.get("892", {}),
                market_order_present="892" in actual_market_indices,
                market_fill_present="892" in actual_fill_metadata_indices,
            )
        if self.supported_mechanical_row_count >= 1355:
            _validate_row1355_session_end_adjacent_limit_valuation_gap_artifacts(
                input_pack_root=Path(self.input_pack_path).resolve(),
                position=position_by_index.get("1355", {}),
                order=order_by_index.get("1355", {}),
                no_market=no_market_by_index.get("1355", {}),
                transition=transition_by_index.get("1355", {}),
                fill=fill_by_index.get("1355", {}),
                cost=cost_by_index.get("1355", {}),
                pnl=pnl_by_index.get("1355", {}),
                market_order_present="1355" in actual_market_indices,
                market_fill_present="1355" in actual_fill_metadata_indices,
            )
        if fail_rows and self.fail_closed_reason == FAIL_CLOSED_BLOCKER_STATUS:
            if str(fail_rows[0]["market_order_rows_emitted"]) != "TRUE":
                raise CarverBlocked("S27 v2 2023 TEST fail row must bind emitted market-order row")
            if str(fail_rows[0]["market_fill_metadata_rows_emitted"]) != "TRUE":
                raise CarverBlocked("S27 v2 2023 TEST fail row must bind emitted fill metadata row")
            if str(fail_rows[0]["market_spread_cost_status"]) != MARKET_SPREAD_COST_STATUS:
                raise CarverBlocked("S27 v2 2023 TEST fail row must bind market spread cost accounting status")
        if pnl_rows:
            final_pnl = pnl_rows[-1]
            if int(final_pnl["ending_position_contracts"]) != self.final_position_contracts:
                raise CarverBlocked("S27 v2 2023 TEST final position must bind final pnl row")
            if float(final_pnl["cumulative_gross_pnl_amount"]) != self.cumulative_gross_pnl_amount:
                raise CarverBlocked("S27 v2 2023 TEST gross pnl must bind final pnl row")
            if float(final_pnl["cumulative_commission_amount"]) != self.cumulative_commission_amount:
                raise CarverBlocked("S27 v2 2023 TEST commission must bind final pnl row")
            if float(final_pnl["cumulative_spread_amount"]) != self.cumulative_spread_amount:
                raise CarverBlocked("S27 v2 2023 TEST spread must bind final pnl row")
            if float(final_pnl["cumulative_net_pnl_amount"]) != self.cumulative_net_pnl_amount:
                raise CarverBlocked("S27 v2 2023 TEST net pnl must bind final pnl row")
        elif (
            self.final_position_contracts != 0
            or self.cumulative_gross_pnl_amount != 0.0
            or self.cumulative_commission_amount != 0.0
            or self.cumulative_spread_amount != 0.0
            or self.cumulative_net_pnl_amount != 0.0
        ):
            raise CarverBlocked("S27 v2 2023 TEST zero-supported-row bundle must bind zero final totals")
        if str(evidence.get("run_manifest_hash")) != self.run_manifest_hash:
            raise CarverBlocked("S27 v2 2023 TEST evidence manifest must bind run manifest hash")
        if str(trusted.get("run_manifest_hash")) != self.run_manifest_hash:
            raise CarverBlocked("S27 v2 2023 TEST trusted bundle must bind run manifest hash")
        if str(trusted.get("evidence_manifest_hash")) != self.evidence_manifest_hash:
            raise CarverBlocked("S27 v2 2023 TEST trusted bundle must bind evidence manifest hash")
        if self.bundle_hash != canonical_sha256(_bundle_payload(self)):
            raise CarverBlocked("S27 v2 2023 TEST bundle hash must be content-bound")


@dataclass(frozen=True)
class MarketOrderTBBORequirementsDiscoveryBundle:
    status: str
    authorization_label: str
    output_root: str
    total_market_order_rows: int
    missing_tbbo_requirement_count: int
    already_bound_tbbo_count: int
    terminal_status: str
    requirements_ledger_hash: str
    manifest_hash: str
    bundle_hash: str

    def validate(self) -> None:
        if self.status != TBBO_REQUIREMENTS_STATUS:
            raise CarverBlocked("S27 v2 2023 TEST TBBO requirements status mismatch")
        if self.authorization_label != TBBO_REQUIREMENTS_AUTHORIZATION:
            raise CarverBlocked("S27 v2 2023 TEST TBBO requirements authorization mismatch")
        output_root = Path(self.output_root).resolve()
        if output_root != (_REPO_ROOT / DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH).resolve():
            raise CarverBlocked("S27 v2 2023 TEST TBBO requirements output root is locked")
        ledger = output_root / TBBO_REQUIREMENT_LEDGER_NAME
        manifest = output_root / TBBO_REQUIREMENT_MANIFEST_NAME
        if self.requirements_ledger_hash != _sha256(ledger):
            raise CarverBlocked("S27 v2 2023 TEST TBBO requirements ledger hash drift")
        if self.manifest_hash != _sha256(manifest):
            raise CarverBlocked("S27 v2 2023 TEST TBBO requirements manifest hash drift")
        rows = _read_csv_rows(ledger)
        missing = [row for row in rows if row["tbbo_requirement_status"] == "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"]
        bound = [row for row in rows if row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE"]
        if len(rows) != self.total_market_order_rows:
            raise CarverBlocked("S27 v2 2023 TEST TBBO requirements row count mismatch")
        if len(missing) != self.missing_tbbo_requirement_count:
            raise CarverBlocked("S27 v2 2023 TEST TBBO missing requirement count mismatch")
        if len(bound) != self.already_bound_tbbo_count:
            raise CarverBlocked("S27 v2 2023 TEST TBBO bound requirement count mismatch")
        for row in rows:
            if not row["decision_timestamp_utc"].startswith("2023-") or not row["fill_candidate_timestamp_utc"].startswith("2023-"):
                raise CarverBlocked("S27 v2 2023 TEST TBBO requirements must stay in 2023")
            if row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE":
                require_hash(
                    "S27 v2 2023 TEST bound TBBO requirement row hash",
                    row["bound_tbbo_selected_spread_row_hash"],
                )
                require_hash(
                    "S27 v2 2023 TEST bound TBBO requirement ledger hash",
                    row["bound_tbbo_selected_spread_ledger_sha256"],
                )
                if row["bound_tbbo_source_evidence_type"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST bound TBBO requirement must bind source evidence type")
                if row["bound_tbbo_selected_quote_ts_event"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST bound TBBO requirement must bind quote timestamp")
                if row["bound_tbbo_quote_age_seconds"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST bound TBBO requirement must bind quote age")
                if row["bound_tbbo_selection_status"] == "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST bound TBBO requirement must bind selection status")
                if "RETRY" in row["bound_tbbo_source_evidence_type"] and row["max_selected_quote_age_seconds"] != "60.0":
                    raise CarverBlocked("S27 v2 2023 TEST retry-bound TBBO requirement must bind retry max quote age")
            elif row["tbbo_requirement_status"] == "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE":
                if row["bound_tbbo_selected_spread_row_hash"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST missing TBBO requirement must not carry bound row hash")
                if row["bound_tbbo_selected_spread_ledger_sha256"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST missing TBBO requirement must not carry bound ledger hash")
                if row["bound_tbbo_source_evidence_type"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST missing TBBO requirement must not carry source evidence type")
                if row["bound_tbbo_selected_quote_ts_event"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST missing TBBO requirement must not carry quote timestamp")
                if row["bound_tbbo_quote_age_seconds"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST missing TBBO requirement must not carry quote age")
                if row["bound_tbbo_selection_status"] != "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE":
                    raise CarverBlocked("S27 v2 2023 TEST missing TBBO requirement must not carry selection status")
            else:
                raise CarverBlocked("S27 v2 2023 TEST TBBO requirement status is not locked")
            payload = {key: value for key, value in row.items() if key != "row_hash"}
            if row["row_hash"] != canonical_sha256(payload):
                raise CarverBlocked("S27 v2 2023 TEST TBBO requirements row hash drift")
        if self.bundle_hash != canonical_sha256(_tbbo_requirements_bundle_payload(self)):
            raise CarverBlocked("S27 v2 2023 TEST TBBO requirements bundle hash drift")


def _validate_row304_engineering_session_open_artifacts(
    *,
    input_pack_root: Path,
    no_market: Mapping[str, str],
    market_order: Mapping[str, str],
    market_fill: Mapping[str, str],
    transition: Mapping[str, str],
    fill: Mapping[str, str],
    cost: Mapping[str, str],
    pnl: Mapping[str, str],
) -> None:
    decisions = _safe_read_csv_rows(
        input_pack_root / "hourly_decision_completed_bar.csv",
        "S27 v2 2023 TEST hourly decision pack rows",
    )
    fills = _safe_read_csv_rows(
        input_pack_root / "hourly_fill_completed_bar.csv",
        "S27 v2 2023 TEST hourly fill pack rows",
    )
    marks = _safe_read_csv_rows(
        input_pack_root / "valuation_mark_completed_bar.csv",
        "S27 v2 2023 TEST valuation mark pack rows",
    )
    if len(decisions) < 304 or len(fills) < 304 or len(marks) < 304:
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open guard requires declared source rows")
    decision_source = decisions[303]
    fill_source = fills[303]
    mark_source = marks[303]
    if (
        str(decision_source.get("completed_timestamp_utc")) != "2023-01-20T21:00:00Z"
        or str(fill_source.get("completed_timestamp_utc")) != "2023-01-20T22:00:00Z"
        or str(mark_source.get("completed_timestamp_utc")) != "2023-01-23T00:00:00Z"
        or str(decision_source.get("raw_symbol")) != "ZNH3"
        or str(fill_source.get("raw_symbol")) != "ZNH3"
        or str(mark_source.get("raw_symbol")) != "ZNH3"
        or str(decision_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-19T22:00:00Z_2023-01-20T21:00:00Z"
        or str(fill_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-20T22:00:00Z_2023-01-21T21:00:00Z"
        or str(mark_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-22T22:00:00Z_2023-01-23T21:00:00Z"
        or str(mark_source.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open source rows must bind exact bounded case")
    if (
        str(no_market.get("market_order_required")).upper() != "TRUE"
        or str(no_market.get("market_order_rows_emitted")).upper() != "TRUE"
        or str(no_market.get("market_fallback_status")) != "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
        or str(no_market.get("engineering_convention_label")) != ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_CONVENTION
        or str(no_market.get("row_status")) != "LOCAL_MARKET_ORDER_EXECUTION_STATUS_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open market state must bind accepted convention")
    if (
        str(market_order.get("decision_timestamp_utc")) != "2023-01-20T21:00:00Z"
        or str(market_order.get("raw_symbol")) != "ZNH3"
        or str(market_order.get("order_status")) != ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_ROW_STATUS
        or str(market_order.get("row_status")) != ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_ROW_STATUS
        or str(market_order.get("engineering_convention_label")) != ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_CONVENTION
        or str(market_order.get("current_position_before_order")) != "7"
        or str(market_order.get("target_position_after_fill")) != "9"
        or str(market_order.get("order_side")) != "BUY"
        or str(market_order.get("order_quantity")) != "2"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open market order must bind exact full-gap BUY 2")
    active_evidence = _load_market_spread_evidence(304, "BUY", "2023-01-20T22:00:00Z")
    if (
        str(active_evidence.get("selected_quote_ts_event")) != "2023-01-20T21:59:59.924187905Z"
        or float(active_evidence.get("ask_px_00", "nan")) != 115.0625
        or str(active_evidence.get("selection_status")) != "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open TBBO evidence must bind selected ask")
    if (
        str(market_fill.get("fill_timestamp_utc")) != "2023-01-20T22:00:00Z"
        or str(market_fill.get("raw_symbol")) != "ZNH3"
        or str(market_fill.get("order_side")) != "BUY"
        or str(market_fill.get("fill_quantity")) != "2"
        or float(market_fill.get("fill_price", "nan")) != 115.0625
        or str(market_fill.get("same_session")).upper() != "FALSE"
        or str(market_fill.get("fill_source_row_hash")) != str(fill_source.get("source_row_hash"))
        or str(market_fill.get("roll_boundary_status")) != "NO_ROLL_BOUNDARY_SAME_RAW_SYMBOL"
        or str(market_fill.get("working_state_before")) != "EMPTY_INITIAL_WORKING_STATE"
        or str(market_fill.get("position_after_fill")) != "9"
        or float(market_fill.get("commission_per_contract", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or float(market_fill.get("commission_amount", "nan")) != 4.6
        or str(market_fill.get("pnl_emission_status")) != "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"
        or str(market_fill.get("row_status")) != "LOCAL_MARKET_FILL_METADATA_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open fill metadata must bind exact next-session fill")
    if (
        str(transition.get("starting_position_contracts")) != "7"
        or str(transition.get("ending_position_contracts")) != "9"
        or str(transition.get("working_state_before")) != "EMPTY_INITIAL_WORKING_STATE"
        or str(transition.get("working_state_after")) != "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
        or str(transition.get("same_session")).upper() != "FALSE"
        or str(transition.get("row_status")) != "LOCAL_MARKET_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT"
        or str(fill.get("fill_executed")).upper() != "TRUE"
        or str(fill.get("fill_rule")) != "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
        or float(fill.get("fill_price", "nan")) != 115.0625
        or str(fill.get("fill_quantity")) != "2"
        or str(fill.get("position_after_fill")) != "9"
        or str(fill.get("row_status")) != "LOCAL_MARKET_ORDER_FILL_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open transition/fill must bind target position")
    if (
        str(cost.get("cost_policy_id")) != "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11"
        or str(cost.get("order_cost_type")) != "MARKET_ORDER_BUY_ASK_FILL_ACTUAL_COST_NOT_PNL"
        or str(cost.get("currency")) != "USD"
        or str(cost.get("market_cost_accounting_convention")) != "ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST"
        or str(cost.get("spread_cost_reason")) != "NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_ASK"
        or str(cost.get("tbbo_quote_ts_event")) != active_evidence["selected_quote_ts_event"]
        or float(cost.get("tbbo_bid_px", "nan")) != 115.046875
        or float(cost.get("tbbo_ask_px", "nan")) != 115.0625
        or float(cost.get("tbbo_full_spread_points", "nan")) != 0.015625
        or float(cost.get("tbbo_full_spread_value_per_contract", "nan")) != 15.625
        or str(cost.get("tbbo_selected_spread_row_hash")) != active_evidence["row_hash"]
        or str(cost.get("tbbo_selected_spread_ledger_sha256")).lower() != active_evidence["selected_spread_ledger_sha256"].lower()
        or float(cost.get("commission_amount", "nan")) != 4.6
        or float(cost.get("spread_cost_amount", "nan")) != 0.0
        or float(cost.get("total_cost_amount", "nan")) != 4.6
        or str(cost.get("row_status")) != "LOCAL_MARKET_ORDER_ACTUAL_COST_ROW_EMITTED_NOT_PNL_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open cost must bind TBBO ask accounting")
    if (
        str(pnl.get("valuation_mark_timestamp_utc")) != "2023-01-23T00:00:00Z"
        or float(pnl.get("valuation_mark_close_price", "nan")) != 115.03125
        or str(pnl.get("valuation_convention_label")) != "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
        or str(pnl.get("ending_position_contracts")) != "9"
        or str(pnl.get("result_status")) != RESULT_STATUS
        or str(pnl.get("backtest_status")) != BACKTEST_STATUS
        or str(pnl.get("pnl_evaluation_status")) != PNL_EVALUATION_STATUS
        or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
        or str(pnl.get("row_status")) != "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-304 engineering session-open pnl must bind valuation and non-result boundary")


def _validate_row701_roll_boundary_no_new_order_suppression_artifacts(
    *,
    input_pack_root: Path,
    position: Mapping[str, str],
    order: Mapping[str, str],
    no_market: Mapping[str, str],
    transition: Mapping[str, str],
    fill: Mapping[str, str],
    cost: Mapping[str, str],
    pnl: Mapping[str, str],
    market_order_present: bool,
    market_fill_present: bool,
) -> None:
    decisions = _safe_read_csv_rows(
        input_pack_root / "hourly_decision_completed_bar.csv",
        "S27 v2 2023 TEST hourly decision pack rows",
    )
    fills = _safe_read_csv_rows(
        input_pack_root / "hourly_fill_completed_bar.csv",
        "S27 v2 2023 TEST hourly fill pack rows",
    )
    marks = _safe_read_csv_rows(
        input_pack_root / "valuation_mark_completed_bar.csv",
        "S27 v2 2023 TEST valuation mark pack rows",
    )
    rolls = _safe_read_csv_rows(
        input_pack_root / "roll_calendar.csv",
        "S27 v2 2023 TEST roll-calendar rows",
    )
    if len(decisions) < 701 or len(fills) < 701 or len(marks) < 701:
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression guard requires declared source rows")
    decision_source = decisions[700]
    fill_source = fills[700]
    mark_source = marks[700]
    roll_source = next((row for row in rolls if str(row.get("roll_transition_date")) == "2023-02-16"), None)
    if roll_source is None:
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression requires declared roll-transition date")
    if (
        str(decision_source.get("completed_timestamp_utc")) != "2023-02-16T01:00:00Z"
        or str(fill_source.get("completed_timestamp_utc")) != "2023-02-16T02:00:00Z"
        or str(mark_source.get("completed_timestamp_utc")) != "2023-02-16T03:00:00Z"
        or str(decision_source.get("trading_date")) != "2023-02-16"
        or str(fill_source.get("trading_date")) != "2023-02-16"
        or str(mark_source.get("trading_date")) != "2023-02-16"
        or str(decision_source.get("raw_symbol")) != "ZNM3"
        or str(fill_source.get("raw_symbol")) != "ZNM3"
        or str(mark_source.get("raw_symbol")) != "ZNM3"
        or str(decision_source.get("session_id")) != "UTC_ZN_2023_TEST_2023-02-15T22:00:00Z_2023-02-16T21:00:00Z"
        or str(fill_source.get("session_id")) != "UTC_ZN_2023_TEST_2023-02-15T22:00:00Z_2023-02-16T21:00:00Z"
        or str(mark_source.get("session_id")) != "UTC_ZN_2023_TEST_2023-02-15T22:00:00Z_2023-02-16T21:00:00Z"
        or not str(decision_source.get("readiness_status", "")).startswith("READY_")
        or not str(fill_source.get("readiness_status", "")).startswith("READY_")
        or not str(mark_source.get("readiness_status", "")).startswith("READY_")
        or str(mark_source.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression source rows must bind exact same-symbol roll-date case")
    if (
        str(roll_source.get("roll_id")) != "20260612_S27_V2_2023_TEST_MECHANICAL_ROLL_0051_20230216"
        or str(roll_source.get("old_contract_key")) != "ZNH3_2023"
        or str(roll_source.get("new_contract_key")) != "ZNM3_2023"
        or str(roll_source.get("additive_delta_to_prior_history")) != "0.484375"
        or str(roll_source.get("readiness_status")) != "READY_DATABENTO_2023_TEST_ROLL_CONTEXT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression roll calendar must bind declared transition")
    if market_order_present or market_fill_present:
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression must not emit market-order rows")
    if (
        str(position.get("starting_position_contracts")) != "0"
        or str(position.get("desired_position_contracts")) != "0"
        or str(position.get("position_change_contracts")) != "0"
        or str(position.get("row_status")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression position must remain flat")
    if (
        str(order.get("order_side")) != "NONE"
        or str(order.get("order_quantity")) != "0"
        or str(order.get("adjacent_target_position")) != "0"
        or str(order.get("formula_limit_price")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION
        or str(order.get("limit_order_price")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION
        or str(order.get("row_status")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression order must bind no-new-order convention")
    if (
        str(no_market.get("market_order_required")).upper() != "FALSE"
        or str(no_market.get("market_order_rows_emitted")).upper() != "FALSE"
        or str(no_market.get("market_fallback_status")) != "NOT_REQUIRED_NO_ORDER_POSITION_UNCHANGED"
        or str(no_market.get("engineering_convention_label")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION
        or str(no_market.get("row_status")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression no-market state must bind convention")
    if (
        str(transition.get("starting_position_contracts")) != "0"
        or str(transition.get("ending_position_contracts")) != "0"
        or str(transition.get("working_state_before")) != "NO_OPEN_WORKING_ORDER_CARRIED"
        or str(transition.get("working_state_after")) != "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
        or str(transition.get("same_session")).upper() != "TRUE"
        or str(transition.get("row_status")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression transition must bind empty working state")
    if (
        str(fill.get("fill_executed")).upper() != "FALSE"
        or str(fill.get("fill_rule")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION
        or float(fill.get("fill_candidate_close", "nan")) != 112.671875
        or float(fill.get("fill_price", "nan")) != 0.0
        or str(fill.get("fill_quantity")) != "0"
        or str(fill.get("position_after_fill")) != "0"
        or str(fill.get("row_status")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression fill must bind no-fill metadata")
    if (
        str(cost.get("cost_policy_id")) != "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11"
        or float(cost.get("commission_amount", "nan")) != 0.0
        or float(cost.get("spread_cost_amount", "nan")) != 0.0
        or float(cost.get("total_cost_amount", "nan")) != 0.0
        or str(cost.get("currency")) != "USD"
        or str(cost.get("row_status")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression cost must bind zero cost")
    if (
        str(pnl.get("valuation_mark_timestamp_utc")) != "2023-02-16T03:00:00Z"
        or float(pnl.get("valuation_mark_close_price", "nan")) != 112.71875
        or str(pnl.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or float(pnl.get("row_gross_pnl_amount", "nan")) != 0.0
        or float(pnl.get("row_net_pnl_amount", "nan")) != 0.0
        or str(pnl.get("ending_position_contracts")) != "0"
        or str(pnl.get("result_status")) != RESULT_STATUS
        or str(pnl.get("backtest_status")) != BACKTEST_STATUS
        or str(pnl.get("pnl_evaluation_status")) != PNL_EVALUATION_STATUS
        or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
        or str(pnl.get("row_status")) != ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-701 suppression pnl must bind zero mechanical non-result row")


def _validate_row892_session_end_adjacent_limit_artifacts(
    *,
    input_pack_root: Path,
    position: Mapping[str, str],
    order: Mapping[str, str],
    no_market: Mapping[str, str],
    transition: Mapping[str, str],
    fill: Mapping[str, str],
    cost: Mapping[str, str],
    pnl: Mapping[str, str],
    market_order_present: bool,
    market_fill_present: bool,
) -> None:
    decisions = _safe_read_csv_rows(
        input_pack_root / "hourly_decision_completed_bar.csv",
        "S27 v2 2023 TEST hourly decision pack rows",
    )
    fills = _safe_read_csv_rows(
        input_pack_root / "hourly_fill_completed_bar.csv",
        "S27 v2 2023 TEST hourly fill pack rows",
    )
    marks = _safe_read_csv_rows(
        input_pack_root / "valuation_mark_completed_bar.csv",
        "S27 v2 2023 TEST valuation mark pack rows",
    )
    sessions = _safe_read_csv_rows(
        input_pack_root / "session_calendar.csv",
        "S27 v2 2023 TEST session-calendar rows",
    )
    rolls = _safe_read_csv_rows(
        input_pack_root / "roll_calendar.csv",
        "S27 v2 2023 TEST roll-calendar rows",
    )
    if len(decisions) < 892 or len(fills) < 892 or len(marks) < 892:
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit guard requires declared source rows")
    decision_source = decisions[891]
    fill_source = fills[891]
    mark_source = marks[891]
    execution_session = next(
        (
            row
            for row in sessions
            if str(row.get("session_id")) == "UTC_ZN_2023_TEST_2023-02-27T22:00:00Z_2023-02-28T21:00:00Z"
        ),
        None,
    )
    next_session = next(
        (
            row
            for row in sessions
            if str(row.get("session_id")) == "UTC_ZN_2023_TEST_2023-02-28T22:00:00Z_2023-03-01T21:00:00Z"
        ),
        None,
    )
    if execution_session is None or next_session is None:
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit requires declared sessions")
    if any(str(row.get("roll_transition_date")) == "2023-02-28" for row in rolls):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit rejects roll-boundary rows")
    if (
        str(decision_source.get("completed_timestamp_utc")) != "2023-02-28T20:00:00Z"
        or str(fill_source.get("completed_timestamp_utc")) != "2023-02-28T21:00:00Z"
        or str(mark_source.get("completed_timestamp_utc")) != "2023-02-28T22:00:00Z"
        or str(decision_source.get("raw_symbol")) != "ZNM3"
        or str(fill_source.get("raw_symbol")) != "ZNM3"
        or str(mark_source.get("raw_symbol")) != "ZNM3"
        or str(decision_source.get("session_id")) != str(execution_session.get("session_id"))
        or str(fill_source.get("session_id")) != str(execution_session.get("session_id"))
        or str(mark_source.get("session_id")) != str(next_session.get("session_id"))
        or str(execution_session.get("session_end_utc")) != "2023-02-28T21:00:00Z"
        or str(next_session.get("session_start_utc")) != "2023-02-28T22:00:00Z"
        or str(mark_source.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or not str(decision_source.get("readiness_status", "")).startswith("READY_")
        or not str(fill_source.get("readiness_status", "")).startswith("READY_")
        or not str(mark_source.get("readiness_status", "")).startswith("READY_")
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit source rows must bind exact bounded case")
    if market_order_present or market_fill_present:
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit must not emit market rows")
    if (
        str(position.get("starting_position_contracts")) != "0"
        or str(position.get("desired_position_contracts")) != "-1"
        or str(position.get("position_change_contracts")) != "-1"
        or str(position.get("row_status")) != "LOCAL_POSITION_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit position must bind SELL 1")
    if (
        str(order.get("order_side")) != "SELL"
        or str(order.get("order_quantity")) != "1"
        or str(order.get("adjacent_target_position")) != "-1"
        or abs(float(order.get("formula_limit_price", "nan")) - 111.6707138465356) > 1e-12
        or float(order.get("limit_order_price", "nan")) != 111.671875
        or str(order.get("row_status")) != ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit order must bind exact SELL 1")
    if (
        str(no_market.get("market_order_required")).upper() != "FALSE"
        or str(no_market.get("market_order_rows_emitted")).upper() != "FALSE"
        or str(no_market.get("market_fallback_status")) != "NOT_REQUIRED_LIMIT_ORDER_FILLED"
        or str(no_market.get("engineering_convention_label")) != ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_CONVENTION
        or str(no_market.get("row_status")) != "LOCAL_NO_MARKET_ORDER_METADATA_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit no-market state must bind convention")
    if (
        str(transition.get("starting_position_contracts")) != "0"
        or str(transition.get("ending_position_contracts")) != "-1"
        or str(transition.get("working_state_before")) != "NO_OPEN_WORKING_ORDER_CARRIED"
        or str(transition.get("working_state_after")) != "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
        or str(transition.get("same_session")).upper() != "FALSE"
        or str(transition.get("row_status")) != ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit transition must bind next-session valuation boundary")
    if (
        str(fill.get("fill_executed")).upper() != "TRUE"
        or str(fill.get("fill_rule")) != ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_RULE
        or float(fill.get("fill_candidate_close", "nan")) != 111.671875
        or float(fill.get("fill_price", "nan")) != 111.671875
        or str(fill.get("fill_quantity")) != "1"
        or str(fill.get("position_after_fill")) != "-1"
        or str(fill.get("row_status")) != ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit fill must bind session-end close-only fill")
    if (
        str(cost.get("cost_policy_id")) != "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11"
        or float(cost.get("commission_amount", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or float(cost.get("spread_cost_amount", "nan")) != 0.0
        or float(cost.get("total_cost_amount", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or str(cost.get("currency")) != "USD"
        or str(cost.get("row_status")) != "LOCAL_COST_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit cost must bind commission-only limit fill")
    if (
        str(pnl.get("valuation_mark_timestamp_utc")) != "2023-02-28T22:00:00Z"
        or float(pnl.get("valuation_mark_close_price", "nan")) != 111.546875
        or str(pnl.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or str(pnl.get("ending_position_contracts")) != "-1"
        or str(pnl.get("result_status")) != RESULT_STATUS
        or str(pnl.get("backtest_status")) != BACKTEST_STATUS
        or str(pnl.get("pnl_evaluation_status")) != PNL_EVALUATION_STATUS
        or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
        or str(pnl.get("row_status")) != "LOCAL_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-892 session-end limit pnl must bind next-session valuation and non-result boundary")


def _validate_row1355_session_end_adjacent_limit_valuation_gap_artifacts(
    *,
    input_pack_root: Path,
    position: Mapping[str, str],
    order: Mapping[str, str],
    no_market: Mapping[str, str],
    transition: Mapping[str, str],
    fill: Mapping[str, str],
    cost: Mapping[str, str],
    pnl: Mapping[str, str],
    market_order_present: bool,
    market_fill_present: bool,
) -> None:
    decisions = _safe_read_csv_rows(
        input_pack_root / "hourly_decision_completed_bar.csv",
        "S27 v2 2023 TEST hourly decision pack rows",
    )
    fills = _safe_read_csv_rows(
        input_pack_root / "hourly_fill_completed_bar.csv",
        "S27 v2 2023 TEST hourly fill pack rows",
    )
    marks = _safe_read_csv_rows(
        input_pack_root / "valuation_mark_completed_bar.csv",
        "S27 v2 2023 TEST valuation mark pack rows",
    )
    sessions = _safe_read_csv_rows(
        input_pack_root / "session_calendar.csv",
        "S27 v2 2023 TEST session-calendar rows",
    )
    rolls = _safe_read_csv_rows(
        input_pack_root / "roll_calendar.csv",
        "S27 v2 2023 TEST roll-calendar rows",
    )
    if len(decisions) < 1355 or len(fills) < 1355 or len(marks) < 1355:
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit guard requires declared source rows")
    decision_source = decisions[1354]
    fill_source = fills[1354]
    mark_source = marks[1354]
    execution_session = next(
        (
            row
            for row in sessions
            if str(row.get("session_id")) == "UTC_ZN_2023_TEST_2023-03-28T22:00:00Z_2023-03-29T21:00:00Z"
        ),
        None,
    )
    next_session = next(
        (
            row
            for row in sessions
            if str(row.get("session_id")) == "UTC_ZN_2023_TEST_2023-03-29T22:00:00Z_2023-03-30T21:00:00Z"
        ),
        None,
    )
    same_symbol_marks_after_fill = sorted(
        (
            str(row.get("completed_timestamp_utc"))
            for row in marks
            if str(row.get("raw_symbol")) == "ZNM3"
            and _parse_timestamp(str(row.get("completed_timestamp_utc"))) > _parse_timestamp("2023-03-29T21:00:00Z")
        ),
        key=_parse_timestamp,
    )
    if execution_session is None or next_session is None:
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit requires declared sessions")
    if any(str(row.get("roll_transition_date")) in {"2023-03-29", "2023-03-30"} for row in rolls):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit rejects roll-boundary rows")
    if (
        str(decision_source.get("completed_timestamp_utc")) != "2023-03-29T20:00:00Z"
        or str(fill_source.get("completed_timestamp_utc")) != "2023-03-29T21:00:00Z"
        or str(mark_source.get("completed_timestamp_utc")) != "2023-03-29T23:00:00Z"
        or "2023-03-29T22:00:00Z" in same_symbol_marks_after_fill
        or not same_symbol_marks_after_fill
        or same_symbol_marks_after_fill[0] != "2023-03-29T23:00:00Z"
        or str(decision_source.get("raw_symbol")) != "ZNM3"
        or str(fill_source.get("raw_symbol")) != "ZNM3"
        or str(mark_source.get("raw_symbol")) != "ZNM3"
        or str(decision_source.get("session_id")) != str(execution_session.get("session_id"))
        or str(fill_source.get("session_id")) != str(execution_session.get("session_id"))
        or str(mark_source.get("session_id")) != str(next_session.get("session_id"))
        or str(execution_session.get("session_end_utc")) != "2023-03-29T21:00:00Z"
        or str(next_session.get("session_start_utc")) != "2023-03-29T22:00:00Z"
        or str(mark_source.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or not str(decision_source.get("readiness_status", "")).startswith("READY_")
        or not str(fill_source.get("readiness_status", "")).startswith("READY_")
        or not str(mark_source.get("readiness_status", "")).startswith("READY_")
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit source rows must bind exact bounded case")
    if market_order_present or market_fill_present:
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit must not emit market rows")
    if (
        str(position.get("starting_position_contracts")) != "7"
        or str(position.get("desired_position_contracts")) != "8"
        or str(position.get("position_change_contracts")) != "1"
        or str(position.get("row_status")) != "LOCAL_POSITION_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit position must bind BUY 1")
    if (
        str(order.get("order_side")) != "BUY"
        or str(order.get("order_quantity")) != "1"
        or str(order.get("adjacent_target_position")) != "8"
        or abs(float(order.get("formula_limit_price", "nan")) - 114.49366645867451) > 1e-12
        or float(order.get("limit_order_price", "nan")) != 114.484375
        or str(order.get("row_status")) != ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit order must bind exact BUY 1")
    if (
        str(no_market.get("market_order_required")).upper() != "FALSE"
        or str(no_market.get("market_order_rows_emitted")).upper() != "FALSE"
        or str(no_market.get("market_fallback_status")) != "NOT_REQUIRED_LIMIT_ORDER_FILLED"
        or str(no_market.get("engineering_convention_label")) != ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_CONVENTION
        or str(no_market.get("row_status")) != "LOCAL_NO_MARKET_ORDER_METADATA_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit no-market state must bind convention")
    if (
        str(transition.get("starting_position_contracts")) != "7"
        or str(transition.get("ending_position_contracts")) != "8"
        or str(transition.get("working_state_before")) != "NO_OPEN_WORKING_ORDER_CARRIED"
        or str(transition.get("working_state_after")) != "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
        or str(transition.get("same_session")).upper() != "FALSE"
        or str(transition.get("row_status")) != ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit transition must bind next-available valuation boundary")
    if (
        str(fill.get("fill_executed")).upper() != "TRUE"
        or str(fill.get("fill_rule")) != ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_RULE
        or float(fill.get("fill_candidate_close", "nan")) != 114.46875
        or float(fill.get("fill_price", "nan")) != 114.484375
        or str(fill.get("fill_quantity")) != "1"
        or str(fill.get("position_after_fill")) != "8"
        or str(fill.get("row_status")) != ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit fill must bind session-end close-only fill")
    if (
        str(cost.get("cost_policy_id")) != "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11"
        or float(cost.get("commission_amount", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or float(cost.get("spread_cost_amount", "nan")) != 0.0
        or float(cost.get("total_cost_amount", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or str(cost.get("currency")) != "USD"
        or str(cost.get("row_status")) != "LOCAL_COST_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit cost must bind commission-only limit fill")
    if (
        str(pnl.get("valuation_mark_timestamp_utc")) != "2023-03-29T23:00:00Z"
        or float(pnl.get("valuation_mark_close_price", "nan")) != 114.5
        or str(pnl.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or str(pnl.get("ending_position_contracts")) != "8"
        or str(pnl.get("result_status")) != RESULT_STATUS
        or str(pnl.get("backtest_status")) != BACKTEST_STATUS
        or str(pnl.get("pnl_evaluation_status")) != PNL_EVALUATION_STATUS
        or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
        or str(pnl.get("row_status")) != "LOCAL_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-1355 valuation-gap limit pnl must bind next-available valuation and non-result boundary")


def _validate_row346_target_zero_adjacent_limit_artifacts(
    *,
    input_pack_root: Path,
    order: Mapping[str, str],
    no_market: Mapping[str, str],
    transition: Mapping[str, str],
    fill: Mapping[str, str],
    cost: Mapping[str, str],
    pnl: Mapping[str, str],
) -> None:
    decisions = _safe_read_csv_rows(
        input_pack_root / "hourly_decision_completed_bar.csv",
        "S27 v2 2023 TEST hourly decision pack rows",
    )
    fills = _safe_read_csv_rows(
        input_pack_root / "hourly_fill_completed_bar.csv",
        "S27 v2 2023 TEST hourly fill pack rows",
    )
    marks = _safe_read_csv_rows(
        input_pack_root / "valuation_mark_completed_bar.csv",
        "S27 v2 2023 TEST valuation mark pack rows",
    )
    runtime_rows = _safe_read_csv_rows(
        input_pack_root / "runtime_evidence_ledger.csv",
        "S27 v2 2023 TEST runtime evidence rows",
    )
    if len(decisions) < 346 or len(fills) < 346 or len(marks) < 346 or len(runtime_rows) < 346:
        raise CarverBlocked("S27 v2 2023 TEST row-346 target-zero guard requires declared source rows")
    decision_source = decisions[345]
    fill_source = fills[345]
    mark_source = marks[345]
    runtime = runtime_rows[345]
    expected_formula_limit = float(runtime["ewma5_equilibrium"])
    if (
        str(decision_source.get("completed_timestamp_utc")) != "2023-01-24T19:00:00Z"
        or str(fill_source.get("completed_timestamp_utc")) != "2023-01-24T20:00:00Z"
        or str(mark_source.get("completed_timestamp_utc")) != "2023-01-24T21:00:00Z"
        or str(decision_source.get("raw_symbol")) != "ZNH3"
        or str(fill_source.get("raw_symbol")) != "ZNH3"
        or str(mark_source.get("raw_symbol")) != "ZNH3"
        or str(decision_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-23T22:00:00Z_2023-01-24T21:00:00Z"
        or str(fill_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-23T22:00:00Z_2023-01-24T21:00:00Z"
        or str(mark_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-23T22:00:00Z_2023-01-24T21:00:00Z"
        or str(mark_source.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or float(runtime.get("ewmac16_64_trend", "nan")) <= 0.0
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-346 target-zero source rows must bind exact same-session SELL-to-flat case")
    if (
        str(order.get("order_side")) != "SELL"
        or str(order.get("order_quantity")) != "1"
        or str(order.get("adjacent_target_position")) != "0"
        or abs(float(order.get("formula_limit_price", "nan")) - expected_formula_limit) > 1e-12
        or float(order.get("limit_order_price", "nan")) != 115.0
        or str(order.get("row_status")) != "LOCAL_LIMIT_ORDER_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-346 target-zero order must bind source-implied SELL 1 to flat")
    if (
        str(no_market.get("market_order_required")).upper() != "FALSE"
        or str(no_market.get("market_order_rows_emitted")).upper() != "FALSE"
        or str(no_market.get("market_fallback_status")) != "NOT_REQUIRED_LIMIT_ORDER_FILLED"
        or str(no_market.get("engineering_convention_label")) != "NOT_APPLICABLE"
        or str(no_market.get("row_status")) != "LOCAL_NO_MARKET_ORDER_METADATA_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-346 target-zero no-market state must bind filled adjacent limit")
    if (
        str(transition.get("starting_position_contracts")) != "1"
        or str(transition.get("ending_position_contracts")) != "0"
        or str(transition.get("working_state_before")) != "NO_OPEN_WORKING_ORDER_CARRIED"
        or str(transition.get("working_state_after")) != "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
        or str(transition.get("same_session")).upper() != "TRUE"
        or str(transition.get("row_status")) != "LOCAL_WORKING_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-346 target-zero transition must bind same-session flat exit")
    if (
        str(fill.get("fill_executed")).upper() != "TRUE"
        or str(fill.get("fill_rule")) != "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL"
        or float(fill.get("fill_candidate_close", "nan")) != 115.03125
        or float(fill.get("fill_price", "nan")) != 115.0
        or str(fill.get("fill_quantity")) != "1"
        or str(fill.get("position_after_fill")) != "0"
        or str(fill.get("row_status")) != "LOCAL_FILL_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-346 target-zero fill must bind close-only SELL 1 fill")
    if (
        str(cost.get("cost_policy_id")) != "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11"
        or float(cost.get("commission_amount", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or float(cost.get("spread_cost_amount", "nan")) != 0.0
        or float(cost.get("total_cost_amount", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or str(cost.get("currency")) != "USD"
        or str(cost.get("row_status")) != "LOCAL_COST_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-346 target-zero cost must bind commission-only limit fill")
    if (
        str(pnl.get("valuation_mark_timestamp_utc")) != "2023-01-24T21:00:00Z"
        or float(pnl.get("valuation_mark_close_price", "nan")) != 115.0625
        or str(pnl.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or float(pnl.get("existing_position_gross_pnl", "nan")) != 31.25
        or float(pnl.get("fill_gross_pnl", "nan")) != -62.5
        or float(pnl.get("row_gross_pnl_amount", "nan")) != -31.25
        or float(pnl.get("row_net_pnl_amount", "nan")) != -33.55
        or str(pnl.get("ending_position_contracts")) != "0"
        or str(pnl.get("result_status")) != RESULT_STATUS
        or str(pnl.get("backtest_status")) != BACKTEST_STATUS
        or str(pnl.get("pnl_evaluation_status")) != PNL_EVALUATION_STATUS
        or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
        or str(pnl.get("row_status")) != "LOCAL_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-346 target-zero pnl must bind mechanical non-result flat exit")


def _validate_row436_session_open_adjacent_limit_artifacts(
    *,
    input_pack_root: Path,
    order: Mapping[str, str],
    no_market: Mapping[str, str],
    transition: Mapping[str, str],
    fill: Mapping[str, str],
    cost: Mapping[str, str],
    pnl: Mapping[str, str],
) -> None:
    decisions = _safe_read_csv_rows(
        input_pack_root / "hourly_decision_completed_bar.csv",
        "S27 v2 2023 TEST hourly decision pack rows",
    )
    fills = _safe_read_csv_rows(
        input_pack_root / "hourly_fill_completed_bar.csv",
        "S27 v2 2023 TEST hourly fill pack rows",
    )
    marks = _safe_read_csv_rows(
        input_pack_root / "valuation_mark_completed_bar.csv",
        "S27 v2 2023 TEST valuation mark pack rows",
    )
    if len(decisions) < 436 or len(fills) < 436 or len(marks) < 436:
        raise CarverBlocked("S27 v2 2023 TEST row-436 session-open limit guard requires declared source rows")
    decision_source = decisions[435]
    fill_source = fills[435]
    mark_source = marks[435]
    if (
        str(decision_source.get("completed_timestamp_utc")) != "2023-01-30T21:00:00Z"
        or str(fill_source.get("completed_timestamp_utc")) != "2023-01-30T22:00:00Z"
        or str(mark_source.get("completed_timestamp_utc")) != "2023-01-31T00:00:00Z"
        or str(decision_source.get("raw_symbol")) != "ZNH3"
        or str(fill_source.get("raw_symbol")) != "ZNH3"
        or str(mark_source.get("raw_symbol")) != "ZNH3"
        or str(decision_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-29T22:00:00Z_2023-01-30T21:00:00Z"
        or str(fill_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-30T22:00:00Z_2023-01-31T21:00:00Z"
        or str(mark_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-30T22:00:00Z_2023-01-31T21:00:00Z"
        or str(mark_source.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-436 session-open limit source rows must bind exact bounded case")
    if (
        str(order.get("order_side")) != "SELL"
        or str(order.get("order_quantity")) != "1"
        or str(order.get("adjacent_target_position")) != "23"
        or abs(float(order.get("formula_limit_price", "nan")) - 114.29396275895618) > 1e-12
        or float(order.get("limit_order_price", "nan")) != 114.296875
        or str(order.get("row_status")) != ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-436 session-open limit order must bind exact bounded SELL 1")
    if (
        str(no_market.get("market_order_required")).upper() != "FALSE"
        or str(no_market.get("market_order_rows_emitted")).upper() != "FALSE"
        or str(no_market.get("market_fallback_status")) != "NOT_REQUIRED_LIMIT_ORDER_FILLED"
        or str(no_market.get("engineering_convention_label")) != ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_CONVENTION
        or str(no_market.get("row_status")) != "LOCAL_NO_MARKET_ORDER_METADATA_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-436 session-open limit no-market state must bind accepted convention")
    if (
        str(transition.get("starting_position_contracts")) != "24"
        or str(transition.get("ending_position_contracts")) != "23"
        or str(transition.get("working_state_before")) != "NO_OPEN_WORKING_ORDER_CARRIED"
        or str(transition.get("working_state_after")) != "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
        or str(transition.get("same_session")).upper() != "FALSE"
        or str(transition.get("row_status")) != ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-436 session-open limit transition must bind cross-session filled exit")
    if (
        str(fill.get("fill_executed")).upper() != "TRUE"
        or str(fill.get("fill_rule")) != ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_RULE
        or float(fill.get("fill_candidate_close", "nan")) != 114.40625
        or float(fill.get("fill_price", "nan")) != 114.296875
        or str(fill.get("fill_quantity")) != "1"
        or str(fill.get("position_after_fill")) != "23"
        or str(fill.get("row_status")) != ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_ROW_STATUS
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-436 session-open limit fill must bind close-only SELL 1 fill")
    if (
        str(cost.get("cost_policy_id")) != "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11"
        or float(cost.get("commission_amount", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or float(cost.get("spread_cost_amount", "nan")) != 0.0
        or float(cost.get("total_cost_amount", "nan")) != ACCEPTED_COMMISSION_PER_CONTRACT
        or str(cost.get("currency")) != "USD"
        or str(cost.get("row_status")) != "LOCAL_COST_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-436 session-open limit cost must bind commission-only limit fill")
    if (
        str(pnl.get("valuation_mark_timestamp_utc")) != "2023-01-31T00:00:00Z"
        or float(pnl.get("valuation_mark_close_price", "nan")) != 114.34375
        or str(pnl.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or str(pnl.get("ending_position_contracts")) != "23"
        or str(pnl.get("result_status")) != RESULT_STATUS
        or str(pnl.get("backtest_status")) != BACKTEST_STATUS
        or str(pnl.get("pnl_evaluation_status")) != PNL_EVALUATION_STATUS
        or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
        or str(pnl.get("row_status")) != "LOCAL_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-436 session-open limit pnl must bind mechanical non-result valuation")


def _validate_row391_session_end_market_artifacts(
    *,
    input_pack_root: Path,
    no_market: Mapping[str, str],
    market_order: Mapping[str, str],
    market_fill: Mapping[str, str],
    transition: Mapping[str, str],
    fill: Mapping[str, str],
    cost: Mapping[str, str],
    pnl: Mapping[str, str],
) -> None:
    decisions = _safe_read_csv_rows(
        input_pack_root / "hourly_decision_completed_bar.csv",
        "S27 v2 2023 TEST hourly decision pack rows",
    )
    fills = _safe_read_csv_rows(
        input_pack_root / "hourly_fill_completed_bar.csv",
        "S27 v2 2023 TEST hourly fill pack rows",
    )
    marks = _safe_read_csv_rows(
        input_pack_root / "valuation_mark_completed_bar.csv",
        "S27 v2 2023 TEST valuation mark pack rows",
    )
    if len(decisions) < 391 or len(fills) < 391 or len(marks) < 391:
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end guard requires declared source rows")
    decision_source = decisions[390]
    fill_source = fills[390]
    mark_source = marks[390]
    if (
        str(decision_source.get("completed_timestamp_utc")) != "2023-01-26T20:00:00Z"
        or str(fill_source.get("completed_timestamp_utc")) != "2023-01-26T21:00:00Z"
        or str(mark_source.get("completed_timestamp_utc")) != "2023-01-26T22:00:00Z"
        or str(decision_source.get("raw_symbol")) != "ZNH3"
        or str(fill_source.get("raw_symbol")) != "ZNH3"
        or str(mark_source.get("raw_symbol")) != "ZNH3"
        or str(decision_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-25T22:00:00Z_2023-01-26T21:00:00Z"
        or str(fill_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-25T22:00:00Z_2023-01-26T21:00:00Z"
        or str(mark_source.get("session_id"))
        != "UTC_ZN_2023_TEST_2023-01-26T22:00:00Z_2023-01-27T21:00:00Z"
        or str(mark_source.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end source rows must bind exact bounded case")
    if (
        str(no_market.get("market_order_required")).upper() != "TRUE"
        or str(no_market.get("market_order_rows_emitted")).upper() != "TRUE"
        or str(no_market.get("market_fallback_status")) != "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
        or str(no_market.get("engineering_convention_label")) != "NOT_APPLICABLE"
        or str(no_market.get("row_status")) != "LOCAL_MARKET_ORDER_EXECUTION_STATUS_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end no-market state must bind locked market execution")
    if (
        str(market_order.get("decision_timestamp_utc")) != "2023-01-26T20:00:00Z"
        or str(market_order.get("raw_symbol")) != "ZNH3"
        or str(market_order.get("current_position_before_order")) != "4"
        or str(market_order.get("target_position_after_fill")) != "12"
        or str(market_order.get("order_side")) != "BUY"
        or str(market_order.get("order_quantity")) != "8"
        or str(market_order.get("engineering_convention_label")) != "NOT_APPLICABLE"
        or str(market_order.get("order_status")) != "LOCAL_MARKET_ORDER_ROW_EMITTED_NOT_RESULT"
        or str(market_order.get("row_status")) != "LOCAL_MARKET_ORDER_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end market order must bind exact full-gap BUY 8")
    active_evidence = _load_market_spread_evidence(391, "BUY", "2023-01-26T21:00:00Z")
    if (
        str(active_evidence.get("source_evidence_type")) != "STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO"
        or str(active_evidence.get("selected_quote_ts_event")) != "2023-01-26T20:59:59.902217027Z"
        or float(active_evidence.get("ask_px_00", "nan")) != 114.828125
        or str(active_evidence.get("selection_status")) != "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end TBBO evidence must bind selected ask")
    if (
        str(market_fill.get("fill_timestamp_utc")) != "2023-01-26T21:00:00Z"
        or str(market_fill.get("raw_symbol")) != "ZNH3"
        or str(market_fill.get("order_side")) != "BUY"
        or str(market_fill.get("fill_quantity")) != "8"
        or float(market_fill.get("fill_price", "nan")) != 114.828125
        or str(market_fill.get("same_session")).upper() != "TRUE"
        or str(market_fill.get("fill_source_row_hash")) != str(fill_source.get("source_row_hash"))
        or str(market_fill.get("position_after_fill")) != "12"
        or float(market_fill.get("commission_amount", "nan")) != 18.4
        or str(market_fill.get("row_status")) != "LOCAL_MARKET_FILL_METADATA_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end fill metadata must bind exact session-end fill")
    if (
        str(transition.get("starting_position_contracts")) != "4"
        or str(transition.get("ending_position_contracts")) != "12"
        or str(transition.get("same_session")).upper() != "TRUE"
        or str(fill.get("fill_executed")).upper() != "TRUE"
        or str(fill.get("fill_rule")) != "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE"
        or float(fill.get("fill_price", "nan")) != 114.828125
        or str(fill.get("fill_quantity")) != "8"
        or str(fill.get("position_after_fill")) != "12"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end transition/fill must bind target position")
    if (
        str(cost.get("cost_policy_id")) != "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11"
        or str(cost.get("order_cost_type")) != "MARKET_ORDER_BUY_ASK_FILL_ACTUAL_COST_NOT_PNL"
        or str(cost.get("currency")) != "USD"
        or str(cost.get("tbbo_quote_ts_event")) != active_evidence["selected_quote_ts_event"]
        or float(cost.get("tbbo_bid_px", "nan")) != 114.8125
        or float(cost.get("tbbo_ask_px", "nan")) != 114.828125
        or str(cost.get("tbbo_selected_spread_row_hash")) != active_evidence["row_hash"]
        or str(cost.get("tbbo_selected_spread_ledger_sha256")).lower() != active_evidence["selected_spread_ledger_sha256"].lower()
        or float(cost.get("commission_amount", "nan")) != 18.4
        or float(cost.get("spread_cost_amount", "nan")) != 0.0
        or float(cost.get("total_cost_amount", "nan")) != 18.4
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end cost must bind TBBO ask accounting")
    if (
        str(pnl.get("valuation_mark_timestamp_utc")) != "2023-01-26T22:00:00Z"
        or float(pnl.get("valuation_mark_close_price", "nan")) != 114.8125
        or str(pnl.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or float(pnl.get("fill_gross_pnl", "nan")) != -125.0
        or float(pnl.get("row_net_pnl_amount", "nan")) != -143.4
        or str(pnl.get("ending_position_contracts")) != "12"
        or str(pnl.get("result_status")) != RESULT_STATUS
        or str(pnl.get("backtest_status")) != BACKTEST_STATUS
        or str(pnl.get("pnl_evaluation_status")) != PNL_EVALUATION_STATUS
        or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-391 session-end pnl must bind mechanical non-result valuation")


def _validate_market_execution_session_class(
    *,
    input_pack_root: Path,
    row_index: str,
    no_market: Mapping[str, str],
    market_order: Mapping[str, str],
    market_fill: Mapping[str, str],
    transition: Mapping[str, str],
    fill: Mapping[str, str],
    pnl: Mapping[str, str],
    market_spread_evidence: Mapping[str, str],
) -> None:
    index = int(row_index)
    decisions = _safe_read_csv_rows(
        input_pack_root / "hourly_decision_completed_bar.csv",
        "S27 v2 2023 TEST hourly decision pack rows",
    )
    fills = _safe_read_csv_rows(
        input_pack_root / "hourly_fill_completed_bar.csv",
        "S27 v2 2023 TEST hourly fill pack rows",
    )
    marks = _safe_read_csv_rows(
        input_pack_root / "valuation_mark_completed_bar.csv",
        "S27 v2 2023 TEST valuation mark pack rows",
    )
    if len(decisions) < index or len(fills) < index or len(marks) < index:
        raise CarverBlocked("S27 v2 2023 TEST market execution session class requires declared source rows")
    decision_source = decisions[index - 1]
    fill_source = fills[index - 1]
    mark_source = marks[index - 1]
    decision_ts = str(decision_source.get("completed_timestamp_utc"))
    fill_ts = str(fill_source.get("completed_timestamp_utc"))
    mark_ts = str(mark_source.get("completed_timestamp_utc"))
    decision_session = str(decision_source.get("session_id"))
    fill_session = str(fill_source.get("session_id"))
    mark_session = str(mark_source.get("session_id"))
    _, decision_session_end = _session_bounds(decision_ts)
    fill_session_start, _ = _session_bounds(fill_ts)
    engineering_label = str(no_market.get("engineering_convention_label"))
    if str(decision_source.get("raw_symbol")) != str(fill_source.get("raw_symbol")):
        raise CarverBlocked("S27 v2 2023 TEST market execution session class must preserve raw symbol")
    if str(fill_source.get("raw_symbol")) != str(mark_source.get("raw_symbol")):
        raise CarverBlocked("S27 v2 2023 TEST market execution valuation class must preserve raw symbol")
    if str(mark_source.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL:
        raise CarverBlocked("S27 v2 2023 TEST market execution valuation class must preserve engineering valuation label")
    if str(market_order.get("engineering_convention_label")) != engineering_label:
        raise CarverBlocked("S27 v2 2023 TEST market execution convention labels must agree")
    if str(market_fill.get("fill_timestamp_utc")) != fill_ts:
        raise CarverBlocked("S27 v2 2023 TEST market execution fill timestamp must bind declared fill source row")
    if str(market_fill.get("fill_source_row_hash")) != str(fill_source.get("source_row_hash")):
        raise CarverBlocked("S27 v2 2023 TEST market execution fill must bind declared fill source row")
    selection_status = str(market_spread_evidence.get("selection_status"))
    if selection_status not in MARKET_TBBO_SELECTION_STATUSES:
        raise CarverBlocked("S27 v2 2023 TEST market execution must bind fresh non-crossed TBBO evidence")
    if selection_status == "PASS_PREBOUND_TBBO_QUOTE_SELECTED_NOT_RESULT" and index not in {1, 2}:
        raise CarverBlocked("S27 v2 2023 TEST market execution prebound TBBO status is limited to rows 1 and 2")
    if selection_status == "PASS_ROW215_ENGINEERING_AFTER_FILL_TBBO_QUOTE_SELECTED_NOT_RESULT" and index != 215:
        raise CarverBlocked("S27 v2 2023 TEST market execution row-215 engineering TBBO status is row-bounded")
    if str(market_spread_evidence.get("source_evidence_type")) not in SESSION_MARKET_TBBO_EVIDENCE_TYPES and index != 215:
        raise CarverBlocked("S27 v2 2023 TEST market execution session class must use at-or-before-fill TBBO evidence")
    order_side = str(market_order.get("order_side"))
    target_position = str(market_order.get("target_position_after_fill"))
    quantity = str(market_order.get("order_quantity"))
    expected_fill_price = _market_fill_price_from_evidence(dict(market_spread_evidence), order_side)
    expected_same_session = "TRUE" if decision_session == fill_session else "FALSE"
    if (
        str(no_market.get("market_order_required")).upper() != "TRUE"
        or str(no_market.get("market_order_rows_emitted")).upper() != "TRUE"
        or str(no_market.get("market_fallback_status")) != "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP"
    ):
        raise CarverBlocked("S27 v2 2023 TEST market execution no-market state must bind locked market execution")
    if (
        str(transition.get("starting_position_contracts")) != str(market_order.get("current_position_before_order"))
        or str(transition.get("ending_position_contracts")) != target_position
        or str(transition.get("same_session")).upper() != expected_same_session
        or str(transition.get("row_status")) != "LOCAL_MARKET_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST market execution transition must bind target position and session state")
    if (
        str(market_fill.get("order_side")) != order_side
        or str(market_fill.get("fill_quantity")) != quantity
        or float(market_fill.get("fill_price", "nan")) != expected_fill_price
        or str(market_fill.get("fill_price_provenance")) != MARKET_FILL_PRICE_PROVENANCE_BY_SIDE[order_side]
        or str(market_fill.get("same_session")).upper() != expected_same_session
        or str(market_fill.get("position_after_fill")) != target_position
        or str(market_fill.get("market_spread_cost_status")) != MARKET_SPREAD_COST_STATUS_BY_SIDE[order_side]
        or str(market_fill.get("pnl_emission_status")) != "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"
        or str(market_fill.get("row_status")) != "LOCAL_MARKET_FILL_METADATA_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST market fill metadata must bind TBBO price, side, quantity, and target position")
    if (
        str(fill.get("fill_executed")).upper() != "TRUE"
        or str(fill.get("fill_rule")) != MARKET_FILL_PRICE_PROVENANCE_BY_SIDE[order_side]
        or float(fill.get("fill_candidate_close", "nan")) != float(fill_source.get("close_price"))
        or float(fill.get("fill_price", "nan")) != expected_fill_price
        or str(fill.get("fill_quantity")) != quantity
        or str(fill.get("position_after_fill")) != target_position
        or str(fill.get("row_status")) != "LOCAL_MARKET_ORDER_FILL_ROW_EMITTED_NOT_RESULT"
    ):
        raise CarverBlocked("S27 v2 2023 TEST market execution fill ledger must bind active fill source and target position")
    if (
        str(pnl.get("valuation_mark_timestamp_utc")) != mark_ts
        or float(pnl.get("valuation_mark_close_price", "nan")) != float(mark_source.get("close_price"))
        or str(pnl.get("valuation_convention_label")) != VALUATION_CONVENTION_LABEL
        or str(pnl.get("ending_position_contracts")) != target_position
        or str(pnl.get("result_status")) != RESULT_STATUS
        or str(pnl.get("backtest_status")) != BACKTEST_STATUS
        or str(pnl.get("pnl_evaluation_status")) != PNL_EVALUATION_STATUS
        or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
    ):
        raise CarverBlocked("S27 v2 2023 TEST market execution PnL metadata must bind active valuation source and non-result gates")
    if decision_session == fill_session == mark_session:
        if engineering_label != "NOT_APPLICABLE":
            raise CarverBlocked("S27 v2 2023 TEST same-session market execution must not claim engineering session reset")
        return
    if decision_session == fill_session and mark_session != fill_session:
        expected_immediate_mark_ts = _z(_parse_timestamp(fill_ts) + timedelta(hours=1))
        same_symbol_marks_after_fill = sorted(
            (
                str(row.get("completed_timestamp_utc"))
                for row in marks
                if str(row.get("raw_symbol")) == str(decision_source.get("raw_symbol"))
                and _parse_timestamp(str(row.get("completed_timestamp_utc"))) > _parse_timestamp(fill_ts)
            ),
            key=_parse_timestamp,
        )
        row1113_valuation_gap_case = (
            index == 1113
            and engineering_label == ROW1113_SESSION_END_MARKET_VALUATION_GAP_CONVENTION
            and str(decision_source.get("completed_timestamp_utc")) == "2023-03-14T20:00:00Z"
            and fill_ts == "2023-03-14T21:00:00Z"
            and mark_ts == "2023-03-14T23:00:00Z"
            and str(decision_source.get("raw_symbol")) == "ZNM3"
            and fill_ts == decision_session_end
            and expected_immediate_mark_ts == "2023-03-14T22:00:00Z"
            and expected_immediate_mark_ts not in same_symbol_marks_after_fill
            and same_symbol_marks_after_fill
            and same_symbol_marks_after_fill[0] == mark_ts
            and str(market_spread_evidence.get("source_evidence_type")) == "STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO"
            and str(market_spread_evidence.get("selected_quote_ts_event")) == "2023-03-14T20:59:59.840382723Z"
            and float(market_spread_evidence.get("ask_px_00", "nan")) == 113.46875
        )
        if row1113_valuation_gap_case:
            if (
                str(market_order.get("current_position_before_order")) != "-17"
                or str(market_order.get("target_position_after_fill")) != "-15"
                or str(market_order.get("order_side")) != "BUY"
                or str(market_order.get("order_quantity")) != "2"
                or str(market_fill.get("same_session")).upper() != "TRUE"
                or str(transition.get("same_session")).upper() != "TRUE"
                or str(fill.get("position_after_fill")) != str(market_order.get("target_position_after_fill"))
                or str(pnl.get("result_status")) != RESULT_STATUS
                or str(pnl.get("backtest_status")) != BACKTEST_STATUS
                or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
            ):
                raise CarverBlocked("S27 v2 2023 TEST row-1113 valuation-gap market execution must bind bounded facts")
            return
        if (
            engineering_label != "NOT_APPLICABLE"
            or str(market_fill.get("same_session")).upper() != "TRUE"
            or str(transition.get("same_session")).upper() != "TRUE"
            or fill_ts != decision_session_end
            or _z(_parse_timestamp(fill_ts) + timedelta(hours=1)) != mark_ts
            or str(fill.get("position_after_fill")) != str(market_order.get("target_position_after_fill"))
            or str(pnl.get("result_status")) != RESULT_STATUS
            or str(pnl.get("backtest_status")) != BACKTEST_STATUS
            or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
        ):
            raise CarverBlocked("S27 v2 2023 TEST session-end market execution class must bind bounded facts")
        return
    if decision_session != fill_session:
        if (
            engineering_label != ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_CONVENTION
            or str(market_fill.get("same_session")).upper() != "FALSE"
            or str(transition.get("same_session")).upper() != "FALSE"
            or decision_ts != decision_session_end
            or fill_ts != fill_session_start
            or _parse_timestamp(mark_ts) <= _parse_timestamp(fill_ts)
            or str(fill.get("position_after_fill")) != str(market_order.get("target_position_after_fill"))
            or str(pnl.get("result_status")) != RESULT_STATUS
            or str(pnl.get("backtest_status")) != BACKTEST_STATUS
            or str(pnl.get("source_faithful_evidence_claimed")).upper() != "FALSE"
        ):
            raise CarverBlocked("S27 v2 2023 TEST session-open market reset class must bind bounded facts")
        return
    raise CarverBlocked("S27 v2 2023 TEST market execution session class is unresolved")


def build_2023_test_declared_pack() -> dict[str, Any]:
    source_root = (_REPO_ROOT / SOURCE_BUILD_RELATIVE_PATH).resolve()
    pack_root = (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()
    source_root.mkdir(parents=True, exist_ok=True)
    pack_root.mkdir(parents=True, exist_ok=True)

    continuous = _build_2023_continuous_source(source_root)
    rolls = _build_2023_roll_source(source_root)
    hourly, exclusions = _build_2023_active_hourly_source(source_root, rolls)
    build_2023_test_combined_market_tbbo_registry()
    selection = _select_2023_test_rows(continuous, rolls, hourly, exclusions)
    _write_pack(pack_root, source_root, selection, rolls)
    manifest = _manifest(pack_root, source_root, selection)
    _write_json(pack_root / DEFAULT_MANIFEST_NAME, manifest)
    _write_sha256s_txt(pack_root / DEFAULT_SHA256SUMS_NAME, pack_root)
    return manifest


def discover_2023_test_market_order_tbbo_requirements() -> MarketOrderTBBORequirementsDiscoveryBundle:
    output_root = (_REPO_ROOT / DEFAULT_TBBO_REQUIREMENTS_RELATIVE_PATH).resolve()
    source_root = (_REPO_ROOT / SOURCE_BUILD_RELATIVE_PATH).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    source_root.mkdir(parents=True, exist_ok=True)

    continuous = _build_2023_continuous_source(source_root)
    rolls = _build_2023_roll_source(source_root)
    hourly, exclusions = _build_2023_active_hourly_source(source_root, rolls)
    rows, terminal_status = _discover_market_order_tbbo_requirement_rows(continuous, rolls, hourly, exclusions)
    _write_csv(output_root / TBBO_REQUIREMENT_LEDGER_NAME, rows or [_empty_tbbo_requirement_row()])
    manifest = _tbbo_requirements_manifest(output_root, source_root, rows, terminal_status)
    _write_json(output_root / TBBO_REQUIREMENT_MANIFEST_NAME, manifest)
    _write_sha256s_csv_for_files(
        output_root / TBBO_REQUIREMENT_SHA256_NAME,
        output_root,
        (TBBO_REQUIREMENT_LEDGER_NAME, TBBO_REQUIREMENT_MANIFEST_NAME),
    )
    bundle = MarketOrderTBBORequirementsDiscoveryBundle(
        status=TBBO_REQUIREMENTS_STATUS,
        authorization_label=TBBO_REQUIREMENTS_AUTHORIZATION,
        output_root=str(output_root),
        total_market_order_rows=len(rows),
        missing_tbbo_requirement_count=sum(
            1 for row in rows if row["tbbo_requirement_status"] == "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"
        ),
        already_bound_tbbo_count=sum(
            1 for row in rows if row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE"
        ),
        terminal_status=terminal_status,
        requirements_ledger_hash=_sha256(output_root / TBBO_REQUIREMENT_LEDGER_NAME),
        manifest_hash=_sha256(output_root / TBBO_REQUIREMENT_MANIFEST_NAME),
        bundle_hash="0" * 64,
    )
    bundle = MarketOrderTBBORequirementsDiscoveryBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_tbbo_requirements_bundle_payload(bundle))}
    )
    bundle.validate()
    return bundle


def run_2023_test_mechanical_artifacts(
    config: TestMechanicalRunConfig | None = None,
) -> TestMechanicalRunBundle:
    if config is None:
        config = TestMechanicalRunConfig(
            input_pack_path=str((_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()),
            output_root=str((_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve()),
        )
    pack_path = Path(config.input_pack_path).resolve()
    output_root = Path(config.output_root).resolve()
    _validate_paths(pack_path, output_root)
    _validate_pack_checksums(pack_path, config.manifest_name, DEFAULT_SHA256SUMS_NAME)
    manifest = _read_json(pack_path / config.manifest_name)
    rows = {filename: _read_csv_rows(pack_path / filename) for filename in ROW_FAMILY_FILES}
    _validate_manifest(pack_path, manifest, rows)
    _validate_runtime_evidence_against_source(manifest, rows["runtime_evidence_ledger.csv"])
    _validate_selected_hourly_rows_against_source(
        manifest,
        rows["runtime_evidence_ledger.csv"],
        rows["hourly_decision_completed_bar.csv"],
        rows["hourly_fill_completed_bar.csv"],
        rows["valuation_mark_completed_bar.csv"],
    )
    build_2023_test_combined_market_tbbo_registry()
    computed = _compute_rows_until_fail_closed(rows)
    _validate_supported_rows_with_machine_freeze(rows, computed)
    _write_artifacts(output_root, pack_path, manifest, computed)
    fail_row = computed["fail_closed"][0] if computed["fail_closed"] else {
        "row_index": 0,
        "fail_closed_reason": NO_FAIL_CLOSED_BLOCKER_PACK_EXHAUSTED_STATUS,
    }
    final_pnl = computed["pnl"][-1] if computed["pnl"] else {}
    bundle = TestMechanicalRunBundle(
        status=RUN_STATUS,
        authorization_label=AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        output_root=str(output_root),
        candidate_row_count=len(rows["hourly_decision_completed_bar.csv"]),
        supported_mechanical_row_count=len(computed["pnl"]),
        fail_closed_row_index=int(fail_row["row_index"]),
        fail_closed_reason=str(fail_row["fail_closed_reason"]),
        final_position_contracts=int(final_pnl.get("ending_position_contracts", 0)),
        cumulative_gross_pnl_amount=float(final_pnl.get("cumulative_gross_pnl_amount", 0.0)),
        cumulative_commission_amount=float(final_pnl.get("cumulative_commission_amount", 0.0)),
        cumulative_spread_amount=float(final_pnl.get("cumulative_spread_amount", 0.0)),
        cumulative_net_pnl_amount=float(final_pnl.get("cumulative_net_pnl_amount", 0.0)),
        run_manifest_hash=_sha256(output_root / "run_manifest.json"),
        evidence_manifest_hash=_sha256(output_root / "evidence_manifest.json"),
        trusted_bundle_hash=_sha256(output_root / "trusted_bundle.json"),
        bundle_hash="0" * 64,
    )
    bundle = TestMechanicalRunBundle(**{**bundle.__dict__, "bundle_hash": canonical_sha256(_bundle_payload(bundle))})
    bundle.validate()
    _write_json(output_root / "run_bundle.json", dict(bundle.__dict__))
    _write_sha256s_csv(output_root)
    return bundle


def build_2023_test_combined_market_tbbo_registry() -> dict[str, Any]:
    global _EXPECTED_MARKET_SPREAD_EVIDENCE_CACHE
    _EXPECTED_MARKET_SPREAD_EVIDENCE_CACHE = None
    output_root = (_REPO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_RELATIVE_PATH).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    rows = _active_combined_market_tbbo_rows()
    registry = output_root / COMBINED_MARKET_TBBO_REGISTRY_NAME
    manifest = output_root / COMBINED_MARKET_TBBO_MANIFEST_NAME
    sha256s = output_root / COMBINED_MARKET_TBBO_SHA256_NAME
    _write_csv(registry, rows)
    payload = {
        "artifact": "S27_V2_2023_TEST_COMBINED_MARKET_ORDER_TBBO_REGISTRY",
        "status": "LOCAL_2023_TEST_COMBINED_MARKET_ORDER_TBBO_REGISTRY_BUILT_NOT_RESULT",
        "authorization": "S27_V2_2023_TEST_COMBINED_MARKET_ORDER_TBBO_REGISTRY_AND_MECHANICAL_CONTINUATION_GATE",
        "registry": COMBINED_MARKET_TBBO_REGISTRY_NAME,
        "registry_sha256": _sha256(registry),
        "row_count": len(rows),
        "row_index_min": rows[0]["row_index"],
        "row_index_max": rows[-1]["row_index"],
        "row215_policy": ROW215_ENGINEERING_TBBO_EVIDENCE["selection_rule"],
        "row215_policy_record": MARKET_TBBO_ROW215_POLICY_RECORD_RELATIVE_PATH,
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "validation_oos_lockbox_forward_access": "NO",
    }
    _write_json(manifest, payload)
    _write_sha256s_csv_for_files(sha256s, output_root, (COMBINED_MARKET_TBBO_REGISTRY_NAME, COMBINED_MARKET_TBBO_MANIFEST_NAME))
    return payload


def _build_2023_roll_source(source_root: Path) -> list[dict[str, str]]:
    rows = _read_csv_rows(PRE2023_ROLLS)
    for row in _read_csv_rows(LOCAL_2023_ROLL_PLAN):
        if row["roll_transition_date"].startswith("2023-"):
            rows.append(
                {
                    "old_contract_key": row["old_contract_key"],
                    "new_contract_key": row["new_contract_key"],
                    "first_notice_proxy": row["first_notice_proxy"],
                    "roll_transition_date": row["roll_transition_date"],
                    "old_close": row["old_close"],
                    "new_close": row["new_close"],
                    "additive_delta_to_prior_history": row["additive_delta_to_prior_history"],
                }
            )
    rows = sorted(rows, key=lambda item: item["roll_transition_date"])
    _write_csv(source_root / SOURCE_ROLL_NAME, rows)
    return rows


def _build_2023_continuous_source(source_root: Path) -> list[dict[str, Any]]:
    pre_rows = [row for row in _read_csv_rows(PRE2023_CONTINUOUS) if row["completed_trading_date"] < "2023-01-01"]
    rolls = _build_2023_roll_source(source_root)
    daily: dict[tuple[str, str], dict[str, str]] = {}
    for raw_symbol in ("ZNH3", "ZNM3", "ZNU3", "ZNZ3", "ZNH4"):
        path = LOCAL_2023_RAW_ROOT / "raw_provider_output" / (
            f"20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_ZN_daily_{raw_symbol}_provider.csv"
        )
        digest = _sha256(path).upper()
        for record in _read_csv_rows(path):
            day = record["ts_event"][:10]
            if day.startswith("2023-"):
                daily[(raw_symbol, day)] = {**record, "source_provider_csv": str(path.relative_to(_REPO_ROOT)), "source_provider_csv_sha256": digest}
    rows: list[dict[str, Any]] = []
    for day in sorted({day for _, day in daily}):
        active_key = _active_contract_key(day, rolls)
        raw_symbol = active_key.split("_", 1)[0]
        record = daily.get((raw_symbol, day))
        if record is None:
            raise CarverBlocked(f"S27 v2 2023 TEST daily source is missing active row {raw_symbol} {day}")
        rows.append(
            {
                "completed_trading_date": day,
                "active_contract_key": active_key,
                "raw_symbol": raw_symbol,
                "instrument_id": record.get("instrument_id", ""),
                "raw_close": record["close"],
                "additive_back_adjustment": "0.0",
                "continuous_close": record["close"],
                "lineage_status": "LOCAL_2023_TEST_DAILY_SOURCE_ROW_PENDING_POINT_IN_TIME_ADJUSTMENT",
                "source_provider_csv": record["source_provider_csv"],
                "source_provider_csv_sha256": record["source_provider_csv_sha256"],
            }
        )
    combined = pre_rows + rows
    _write_csv(source_root / SOURCE_CONTINUOUS_NAME, combined)
    return combined


def _build_2023_active_hourly_source(source_root: Path, rolls: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    digest = _sha256(LOCAL_2023_HOURLY_CONDITION).upper()
    selected: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    for row in _read_csv_rows(LOCAL_2023_HOURLY_CONDITION):
        if not row["completed_trading_date"].startswith("2023-"):
            continue
        if row["provider_condition_status"] != "PROVIDER_CONDITION_AVAILABLE":
            exclusions.append(_exclusion(row, "EXCLUDED_PROVIDER_CONDITION_NOT_AVAILABLE"))
            continue
        active_symbol = _active_contract_key(row["completed_trading_date"], rolls).split("_", 1)[0]
        if row["raw_symbol"] != active_symbol:
            exclusions.append(_exclusion(row, "EXCLUDED_INACTIVE_CONTRACT_FOR_COMPLETED_TRADING_DATE"))
            continue
        selected.append(
            {
                "raw_symbol": row["raw_symbol"],
                "contract_year": "",
                "delivery_month": "",
                "delivery_code": "",
                "provider_ts_event_start_utc": row["provider_ts_event_start_utc"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "completed_trading_date": row["completed_trading_date"],
                "instrument_id": row["instrument_id"],
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": row["volume"],
                "provider_condition_status": row["provider_condition_status"],
                "source_provider_csv": str(LOCAL_2023_HOURLY_CONDITION.relative_to(_REPO_ROOT)),
                "source_provider_csv_sha256": digest,
            }
        )
    selected.sort(key=lambda item: item["derived_completed_bar_end_utc"])
    _write_csv(source_root / SOURCE_HOURLY_NAME, selected)
    _write_csv(source_root / SOURCE_EXCLUSION_NAME, exclusions or [{"status": "NO_EXCLUSIONS_RECORDED"}])
    return selected, exclusions


def _select_2023_test_rows(
    continuous: list[dict[str, Any]],
    rolls: list[dict[str, str]],
    hourly: list[dict[str, Any]],
    exclusions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    del exclusions
    continuous_by_date = {row["completed_trading_date"]: row for row in continuous}
    hourly_by_symbol_ts = {(row["raw_symbol"], row["derived_completed_bar_end_utc"]): row for row in hourly}
    hourly_by_symbol = _group_hourly_by_symbol(hourly)
    cache: dict[str, tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]] = {}
    current_position = 0
    selected: list[dict[str, Any]] = []
    roll_dates = {row["roll_transition_date"] for row in rolls}
    for decision in sorted(hourly, key=lambda row: row["derived_completed_bar_end_utc"]):
        fill_ts = _z(_parse_timestamp(decision["derived_completed_bar_end_utc"]) + timedelta(hours=1))
        fill = hourly_by_symbol_ts.get((decision["raw_symbol"], fill_ts))
        if fill is None:
            continue
        mark = _next_same_symbol_source_row_after(hourly_by_symbol[decision["raw_symbol"]], fill_ts)
        if mark is None:
            continue
        previous_daily_date = max(day for day in continuous_by_date if day < decision["completed_trading_date"])
        if previous_daily_date not in cache:
            pit = _point_in_time_continuous_series(continuous, rolls, previous_daily_date)
            sigma_rows = _build_sigma_rows(pit)
            vqm_rows = _build_vqm_rows(sigma_rows)
            cache[previous_daily_date] = (
                pit,
                {row["completed_trading_date"]: row for row in sigma_rows},
                {row["completed_trading_date"]: row for row in vqm_rows},
            )
        pit, sigma_by_date, vqm_by_date = cache[previous_daily_date]
        prior_vqm_dates = [day for day in vqm_by_date if day < decision["completed_trading_date"]]
        if previous_daily_date not in sigma_by_date or not prior_vqm_dates:
            continue
        runtime = _runtime_row_from_source(
            pit=pit,
            sigma=sigma_by_date[previous_daily_date],
            vqm=vqm_by_date[max(prior_vqm_dates)],
            decision=decision,
            row_index=len(selected) + 1,
        )
        mechanics = _row_mechanics(
            row_index=len(selected) + 1,
            current_position=current_position,
            decision=decision,
            fill=fill,
            mark=mark,
            runtime=runtime,
        )
        live_order_roll_dates = _live_order_roll_boundary_dates(
            decision,
            fill,
            mark,
            mechanics.get("order_side", "NONE"),
            roll_dates,
        )
        if live_order_roll_dates and _roll_boundary_no_new_order_suppression_applies(
            decision=decision,
            fill=fill,
            mark=mark,
            mechanics=mechanics,
            roll_boundary_dates=live_order_roll_dates,
        ):
            mechanics = _suppressed_roll_boundary_mechanics(mechanics, live_order_roll_dates)
        elif live_order_roll_dates:
            mechanics = {
                **mechanics,
                "formula_status": FAIL_CLOSED_LIVE_ORDER_ROLL_BOUNDARY_STATUS,
                "roll_boundary_dates": sorted(live_order_roll_dates),
                "signed_fill_quantity": 0,
            }
        selected.append({"decision": decision, "fill": fill, "mark": mark, "runtime": runtime, "mechanics": mechanics})
        if mechanics["formula_status"] != "PASS_FORMULA_SUPPORTED":
            return selected
        current_position += int(mechanics["signed_fill_quantity"])
        if len(selected) >= AUTHORIZED_2023_TEST_DECLARED_PACK_ROW_LIMIT:
            return selected
    raise CarverBlocked("S27 v2 2023 TEST did not encounter the expected fail-closed blocker")


def _discover_market_order_tbbo_requirement_rows(
    continuous: list[dict[str, Any]],
    rolls: list[dict[str, str]],
    hourly: list[dict[str, Any]],
    exclusions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], str]:
    del exclusions
    continuous_by_date = {row["completed_trading_date"]: row for row in continuous}
    hourly_by_symbol_ts = {(row["raw_symbol"], row["derived_completed_bar_end_utc"]): row for row in hourly}
    hourly_by_symbol = _group_hourly_by_symbol(hourly)
    cache: dict[str, tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]] = {}
    current_position = 0
    requirements: list[dict[str, Any]] = []
    processed_rows = 0
    roll_dates = {row["roll_transition_date"] for row in rolls}
    for decision in sorted(hourly, key=lambda row: row["derived_completed_bar_end_utc"]):
        fill_ts = _z(_parse_timestamp(decision["derived_completed_bar_end_utc"]) + timedelta(hours=1))
        fill = hourly_by_symbol_ts.get((decision["raw_symbol"], fill_ts))
        if fill is None:
            continue
        mark = _next_same_symbol_source_row_after(hourly_by_symbol[decision["raw_symbol"]], fill_ts)
        if mark is None:
            continue
        previous_daily_date = max(day for day in continuous_by_date if day < decision["completed_trading_date"])
        if previous_daily_date not in cache:
            pit = _point_in_time_continuous_series(continuous, rolls, previous_daily_date)
            sigma_rows = _build_sigma_rows(pit)
            vqm_rows = _build_vqm_rows(sigma_rows)
            cache[previous_daily_date] = (
                pit,
                {row["completed_trading_date"]: row for row in sigma_rows},
                {row["completed_trading_date"]: row for row in vqm_rows},
            )
        pit, sigma_by_date, vqm_by_date = cache[previous_daily_date]
        prior_vqm_dates = [day for day in vqm_by_date if day < decision["completed_trading_date"]]
        if previous_daily_date not in sigma_by_date or not prior_vqm_dates:
            continue
        row_index = processed_rows + 1
        runtime = _runtime_row_from_source(
            pit=pit,
            sigma=sigma_by_date[previous_daily_date],
            vqm=vqm_by_date[max(prior_vqm_dates)],
            decision=decision,
            row_index=row_index,
        )
        mechanics = _row_mechanics(
            row_index=row_index,
            current_position=current_position,
            decision=decision,
            fill=fill,
            mark=mark,
            runtime=runtime,
        )
        processed_rows += 1
        live_order_roll_dates = _live_order_roll_boundary_dates(
            decision,
            fill,
            mark,
            mechanics.get("order_side", "NONE"),
            roll_dates,
        )
        if live_order_roll_dates and _roll_boundary_no_new_order_suppression_applies(
            decision=decision,
            fill=fill,
            mark=mark,
            mechanics=mechanics,
            roll_boundary_dates=live_order_roll_dates,
        ):
            current_position += 0
            continue
        if live_order_roll_dates:
            return requirements, f"STOPPED_ON_NEW_BLOCKER_CLASS_{FAIL_CLOSED_LIVE_ORDER_ROLL_BOUNDARY_STATUS}"
        if bool(mechanics.get("market_order_required")):
            requirements.append(
                _tbbo_requirement_row(
                    row_index=row_index,
                    decision=decision,
                    fill=fill,
                    mechanics=mechanics,
                    evidence_status=(
                        "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE"
                        if _market_spread_evidence_matches(row_index, str(mechanics["order_side"]), fill["derived_completed_bar_end_utc"])
                        else "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"
                    ),
                )
            )
            current_position += int(mechanics["position_change_contracts"])
            continue
        if mechanics["formula_status"] != "PASS_FORMULA_SUPPORTED":
            return requirements, f"STOPPED_ON_NEW_BLOCKER_CLASS_{mechanics['formula_status']}"
        current_position += int(mechanics["signed_fill_quantity"])
    return requirements, "COMPLETED_AVAILABLE_2023_SOURCE_ROWS_NO_NEW_BLOCKER_CLASS"


def _tbbo_requirement_row(
    *,
    row_index: int,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mechanics: dict[str, Any],
    evidence_status: str,
) -> dict[str, Any]:
    fill_ts = _parse_timestamp(fill["derived_completed_bar_end_utc"])
    request_start = _z(fill_ts - timedelta(seconds=5))
    request_end = _z(fill_ts + timedelta(seconds=5))
    try:
        known = _expected_market_spread_evidence(row_index)
    except CarverBlocked:
        known = {}
    bound_missing = "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE"
    row: dict[str, Any] = {
        "row_index": row_index,
        "decision_timestamp_utc": decision["derived_completed_bar_end_utc"],
        "fill_candidate_timestamp_utc": fill["derived_completed_bar_end_utc"],
        "raw_symbol": decision["raw_symbol"],
        "order_side": mechanics["order_side"],
        "order_quantity": mechanics["order_quantity"],
        "starting_position_contracts": mechanics["starting_position_contracts"],
        "desired_position_contracts": mechanics["desired_position_contracts"],
        "position_change_contracts": mechanics["position_change_contracts"],
        "adjacent_target_position": mechanics["adjacent_target_position"],
        "market_order_reason": mechanics.get("market_order_reason", MARKET_ORDER_TRIGGER_SOURCE_CONDITION),
        "tbbo_requirement_status": evidence_status,
        "provider": "DATABENTO_HISTORICAL",
        "dataset": "GLBX.MDP3",
        "schema": "tbbo",
        "stype_in": "raw_symbol",
        "request_start_utc": request_start,
        "request_end_utc": request_end,
        "max_selected_quote_age_seconds": _tbbo_requirement_max_selected_quote_age(known),
        "fill_source_row_hash": _row_hash("strategy_facing_hourly_available_bars", fill),
        "bound_tbbo_selected_spread_row_hash": known.get("row_hash", bound_missing),
        "bound_tbbo_selected_spread_ledger_sha256": known.get(
            "source_selected_spread_ledger_sha256",
            known.get("selected_spread_ledger_sha256", bound_missing),
        ),
        "bound_tbbo_source_evidence_type": known.get("source_evidence_type", bound_missing),
        "bound_tbbo_selected_quote_ts_event": known.get("selected_quote_ts_event", bound_missing),
        "bound_tbbo_quote_age_seconds": known.get("quote_age_seconds", bound_missing),
        "bound_tbbo_selection_status": known.get("selection_status", bound_missing),
        "result_interpretation_authorized": "FALSE",
        "source_faithful_evidence_claimed": "FALSE",
    }
    text_row = {key: _csv_value(value) for key, value in row.items()}
    text_row["row_hash"] = canonical_sha256(text_row)
    return text_row


def _tbbo_requirement_max_selected_quote_age(known: Mapping[str, str]) -> str:
    if not known:
        return "5.0"
    evidence_type = str(known.get("source_evidence_type", ""))
    if "RETRY" in evidence_type:
        return "60.0"
    if (
        "ROW441_EXTENDED_LOOKBACK" in evidence_type
        or "ZNM3_EXTENDED_LOOKBACK" in evidence_type
        or "ROW704_ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK" in evidence_type
    ):
        return "300.0"
    if "ROW215_ENGINEERING_AFTER_FILL" in evidence_type:
        return "ROW215_ENGINEERING_AFTER_FILL_POLICY_NOT_AT_OR_BEFORE_FILL"
    return "5.0"


def _live_order_roll_boundary_dates(
    decision: Mapping[str, Any],
    fill: Mapping[str, Any],
    mark: Mapping[str, Any],
    side: Any,
    roll_dates: set[str],
) -> set[str]:
    if str(side) == "NONE":
        return set()
    selected_dates = {
        str(decision.get("completed_trading_date") or decision.get("trading_date")),
        str(fill.get("completed_trading_date") or fill.get("trading_date")),
        str(mark.get("completed_trading_date") or mark.get("trading_date")),
    }
    return {date for date in selected_dates if date in roll_dates}


def _roll_boundary_no_new_order_suppression_applies(
    *,
    decision: Mapping[str, Any],
    fill: Mapping[str, Any],
    mark: Mapping[str, Any],
    mechanics: Mapping[str, Any],
    roll_boundary_dates: set[str],
) -> bool:
    if not roll_boundary_dates:
        return False
    if str(mechanics.get("order_side")) not in {"BUY", "SELL"}:
        return False
    if int(mechanics.get("starting_position_contracts", 0)) != 0:
        return False
    if int(mechanics.get("position_change_contracts", 0)) == 0:
        return False
    if str(decision.get("raw_symbol")) != str(fill.get("raw_symbol")):
        return False
    if str(decision.get("raw_symbol")) != str(mark.get("raw_symbol")):
        return False
    if not _row_has_available_provider_condition(decision):
        return False
    if not _row_has_available_provider_condition(fill):
        return False
    if not _row_has_available_provider_condition(mark):
        return False
    return True


def _row_has_available_provider_condition(row: Mapping[str, Any]) -> bool:
    if str(row.get("provider_condition_status")) == "PROVIDER_CONDITION_AVAILABLE":
        return True
    return str(row.get("readiness_status", "")).startswith("READY_")


def _suppressed_roll_boundary_mechanics(
    mechanics: Mapping[str, Any],
    roll_boundary_dates: set[str],
) -> dict[str, Any]:
    starting_position = int(mechanics["starting_position_contracts"])
    return {
        **mechanics,
        "formula_status": "PASS_FORMULA_SUPPORTED",
        "desired_position_contracts": starting_position,
        "position_change_contracts": 0,
        "order_side": "NONE",
        "order_quantity": 0,
        "adjacent_target_position": starting_position,
        "formula_limit_price": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION,
        "limit_order_price": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION,
        "fill_executed": False,
        "fill_quantity": 0,
        "roll_boundary_dates": sorted(roll_boundary_dates),
        "roll_boundary_no_new_order_suppression": True,
        "signed_fill_quantity": 0,
    }


def _empty_tbbo_requirement_row() -> dict[str, Any]:
    row = {
        "row_index": "NO_MARKET_ORDER_REQUIREMENTS",
        "decision_timestamp_utc": "NOT_APPLICABLE",
        "fill_candidate_timestamp_utc": "NOT_APPLICABLE",
        "raw_symbol": "NOT_APPLICABLE",
        "order_side": "NOT_APPLICABLE",
        "order_quantity": "0",
        "starting_position_contracts": "0",
        "desired_position_contracts": "0",
        "position_change_contracts": "0",
        "adjacent_target_position": "0",
        "market_order_reason": "NOT_APPLICABLE",
        "tbbo_requirement_status": "NO_MARKET_ORDER_REQUIREMENTS_DISCOVERED",
        "provider": "DATABENTO_HISTORICAL",
        "dataset": "GLBX.MDP3",
        "schema": "tbbo",
        "stype_in": "raw_symbol",
        "request_start_utc": "NOT_APPLICABLE",
        "request_end_utc": "NOT_APPLICABLE",
        "max_selected_quote_age_seconds": "5.0",
        "fill_source_row_hash": "NOT_APPLICABLE",
        "bound_tbbo_selected_spread_row_hash": "NOT_APPLICABLE",
        "bound_tbbo_selected_spread_ledger_sha256": "NOT_APPLICABLE",
        "bound_tbbo_source_evidence_type": "NOT_APPLICABLE",
        "bound_tbbo_selected_quote_ts_event": "NOT_APPLICABLE",
        "bound_tbbo_quote_age_seconds": "NOT_APPLICABLE",
        "bound_tbbo_selection_status": "NOT_APPLICABLE",
        "result_interpretation_authorized": "FALSE",
        "source_faithful_evidence_claimed": "FALSE",
    }
    row = {key: _csv_value(value) for key, value in row.items()}
    row["row_hash"] = canonical_sha256(row)
    return row


def _row_mechanics(
    *,
    row_index: int,
    current_position: int,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    runtime: dict[str, Any],
) -> dict[str, Any]:
    decision_price = float(decision["close"]) + float(runtime["previous_daily_additive_back_adjustment"])
    fill_close = float(fill["close"]) + float(runtime["previous_daily_additive_back_adjustment"])
    ewma5 = float(runtime["ewma5_equilibrium"])
    trend = float(runtime["ewmac16_64_trend"])
    sigma = float(runtime["annual_percentage_sigma"])
    multiplier = float(runtime["vol_multiplier_m"])
    sigma_price = float(runtime["previous_daily_raw_close"]) * sigma / 16.0
    risk_before_veto = (ewma5 - decision_price) / sigma_price
    risk_after_veto = 0.0 if risk_before_veto * trend < 0.0 else risk_before_veto
    capped_forecast = _clamp(risk_after_veto * multiplier * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)
    base_position = CAPITAL_ACCOUNT_VALUE * ANNUAL_TARGET_RISK / (decision_price * CONTRACT_POINT_VALUE * sigma)
    desired_position = _round_half_away_from_zero(base_position * capped_forecast / FORECAST_TO_POSITION_DIVISOR)
    position_change = desired_position - current_position
    side = "BUY" if position_change > 0 else "SELL" if position_change < 0 else "NONE"
    adjacent_target = current_position + (1 if position_change > 0 else -1 if position_change < 0 else 0)
    cap_bound_market_case = _is_cap_bound_market_order_case(
        position_change=position_change,
        adjacent_target=adjacent_target,
        base_position=base_position,
        trend=trend,
    )
    market_order_required = abs(position_change) > 1 or cap_bound_market_case
    market_order_reason = (
        CAP_BOUND_MARKET_ORDER_TRIGGER_SOURCE_CONDITION
        if cap_bound_market_case
        else MARKET_ORDER_TRIGGER_SOURCE_CONDITION
    )
    if market_order_required:
        if _market_spread_evidence_is_bound(row_index):
            try:
                market_spread_evidence = _load_market_spread_evidence(
                    row_index,
                    side,
                    fill["derived_completed_bar_end_utc"],
                )
            except CarverBlocked:
                return {
                    "formula_status": FAIL_CLOSED_STALE_MARKET_SPREAD_EVIDENCE_STATUS,
                    "starting_position_contracts": current_position,
                    "desired_position_contracts": desired_position,
                    "position_change_contracts": position_change,
                    "order_side": side,
                    "order_quantity": abs(position_change),
                    "adjacent_target_position": adjacent_target,
                    "market_order_required": True,
                    "market_order_rows_emitted": False,
                    "market_order_reason": market_order_reason,
                    "signed_fill_quantity": 0,
                }
            same_session = _same_execution_and_valuation_session(decision, fill, mark)
            session_end_market_case = _is_session_end_market_case(
                decision=decision,
                fill=fill,
                mark=mark,
                market_spread_evidence=market_spread_evidence,
            )
            session_open_market_reset_case = _is_session_open_market_reset_case(
                decision=decision,
                fill=fill,
                mark=mark,
                market_spread_evidence=market_spread_evidence,
            )
            row303_session_end_case = _is_row303_session_end_market_case(
                row_index=row_index,
                decision=decision,
                fill=fill,
                mark=mark,
                position_change=position_change,
                side=side,
            )
            row304_engineering_session_open_case = _is_row304_engineering_session_open_market_reset_case(
                row_index=row_index,
                decision=decision,
                fill=fill,
                mark=mark,
                position_change=position_change,
                side=side,
                market_spread_evidence=market_spread_evidence,
            )
            row391_session_end_case = _is_row391_session_end_market_case(
                row_index=row_index,
                decision=decision,
                fill=fill,
                mark=mark,
                position_change=position_change,
                side=side,
                market_spread_evidence=market_spread_evidence,
            )
            row1113_valuation_gap_case = _is_row1113_session_end_market_valuation_gap_case(
                row_index=row_index,
                decision=decision,
                fill=fill,
                mark=mark,
                position_change=position_change,
                side=side,
                market_spread_evidence=market_spread_evidence,
            )
            if (
                not same_session
                and not session_end_market_case
                and not session_open_market_reset_case
                and not row1113_valuation_gap_case
            ):
                return {
                    "formula_status": SECONDARY_SESSION_EOD_BLOCKER_STATUS,
                    "starting_position_contracts": current_position,
                    "desired_position_contracts": desired_position,
                    "position_change_contracts": position_change,
                    "order_side": side,
                    "order_quantity": abs(position_change),
                    "adjacent_target_position": adjacent_target,
                    "market_order_required": True,
                    "market_order_rows_emitted": False,
                    "market_order_reason": MARKET_ORDER_TRIGGER_SOURCE_CONDITION,
                    "fill_candidate_close": fill_close,
                    "fill_executed": False,
                    "same_session": False,
                    "signed_fill_quantity": 0,
                }
            execution_same_session = _same_execution_session(decision, fill)
            return {
                "formula_status": "PASS_FORMULA_SUPPORTED",
                "execution_mode": f"MARKET_ORDER_ROW{row_index}_SUPPORTED_WITH_BOUND_TBBO_EVIDENCE",
                "session_end_market_policy_status": (
                    ROW303_SESSION_END_MARKET_FILL_POLICY_STATUS
                    if row303_session_end_case
                    else ROW391_SESSION_END_MARKET_FILL_POLICY_STATUS
                    if row391_session_end_case
                    else ROW1113_SESSION_END_MARKET_VALUATION_GAP_POLICY_STATUS
                    if row1113_valuation_gap_case
                    else ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_CONVENTION
                    if session_open_market_reset_case
                    else "CLASS_LEVEL_SESSION_END_MARKET_FILL_ALLOWED_WITH_NEXT_COMPLETED_ENGINEERING_VALUATION_NOT_RESULT"
                    if session_end_market_case
                    else "NOT_APPLICABLE_NORMAL_SAME_SESSION_MARKET_ORDER"
                ),
                "starting_position_contracts": current_position,
                "desired_position_contracts": desired_position,
                "position_change_contracts": position_change,
                "order_side": side,
                "order_quantity": abs(position_change),
                "adjacent_target_position": adjacent_target,
                "market_order_required": True,
                "market_order_rows_emitted": True,
                "market_order_reason": market_order_reason,
                "same_session": execution_same_session,
                "signed_fill_quantity": position_change,
            }
        return {
            "formula_status": FAIL_CLOSED_UNSUPPORTED_MARKET_CONTINUATION_STATUS,
            "starting_position_contracts": current_position,
            "desired_position_contracts": desired_position,
            "position_change_contracts": position_change,
            "order_side": side,
            "order_quantity": abs(position_change),
            "adjacent_target_position": adjacent_target,
            "market_order_required": True,
            "market_order_rows_emitted": False,
            "market_order_reason": market_order_reason,
            "signed_fill_quantity": 0,
        }
    formula_limit = _formula_limit(adjacent_target, base_position, ewma5, sigma_price, multiplier, trend) if side != "NONE" else 0.0
    if formula_limit is None:
        formula_status = _adjacent_limit_formula_fail_status(adjacent_target, base_position)
        return {
            "formula_status": formula_status,
            "starting_position_contracts": current_position,
            "desired_position_contracts": desired_position,
            "position_change_contracts": position_change,
            "order_side": side,
            "adjacent_target_position": adjacent_target,
            "trend": trend,
            "signed_fill_quantity": 0,
        }
    limit_price = _round_limit(formula_limit, side) if side != "NONE" else 0.0
    fill_executed = _limit_fill(side, fill_close, limit_price)
    fill_quantity = abs(position_change) if fill_executed else 0
    signed_fill_quantity = fill_quantity if side == "BUY" else -fill_quantity if side == "SELL" else 0
    same_session = _session_id(decision["derived_completed_bar_end_utc"]) == _session_id(
        fill["derived_completed_bar_end_utc"]
    ) == _session_id(
        mark["derived_completed_bar_end_utc"]
    )
    session_open_limit_fill_case = _is_session_open_adjacent_limit_fill_case(
        decision=decision,
        fill=fill,
        mark=mark,
        position_change=position_change,
        side=side,
        fill_executed=fill_executed,
    )
    row892_session_end_limit_fill_case = _is_row892_session_end_adjacent_limit_fill_case(
        row_index=row_index,
        decision=decision,
        fill=fill,
        mark=mark,
        position_change=position_change,
        side=side,
        fill_executed=fill_executed,
        fill_close=fill_close,
        formula_limit=formula_limit,
        limit_price=limit_price,
    )
    row1355_session_end_limit_valuation_gap_case = _is_row1355_session_end_adjacent_limit_valuation_gap_case(
        row_index=row_index,
        decision=decision,
        fill=fill,
        mark=mark,
        position_change=position_change,
        side=side,
        fill_executed=fill_executed,
        fill_close=fill_close,
        formula_limit=formula_limit,
        limit_price=limit_price,
    )
    if (
        fill_executed
        and not same_session
        and not session_open_limit_fill_case
        and not row892_session_end_limit_fill_case
        and not row1355_session_end_limit_valuation_gap_case
    ):
        return {
            "formula_status": SECONDARY_SESSION_EOD_BLOCKER_STATUS,
            "starting_position_contracts": current_position,
            "desired_position_contracts": desired_position,
            "position_change_contracts": position_change,
            "order_side": side,
            "order_quantity": abs(position_change),
            "adjacent_target_position": adjacent_target,
            "formula_limit_price": formula_limit,
            "limit_order_price": limit_price,
            "fill_candidate_close": fill_close,
            "fill_executed": fill_executed,
            "same_session": same_session,
            "signed_fill_quantity": 0,
        }
    return {
        "formula_status": "PASS_FORMULA_SUPPORTED",
        "starting_position_contracts": current_position,
        "desired_position_contracts": desired_position,
        "position_change_contracts": position_change,
        "order_side": side,
        "order_quantity": abs(position_change),
        "adjacent_target_position": adjacent_target,
        "formula_limit_price": formula_limit,
        "limit_order_price": limit_price,
        "fill_candidate_close": fill_close,
        "fill_executed": fill_executed,
        "fill_quantity": fill_quantity,
        "session_open_limit_fill_policy_status": (
            ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_CONVENTION
            if session_open_limit_fill_case
            else ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_CONVENTION
            if row892_session_end_limit_fill_case
            else ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_CONVENTION
            if row1355_session_end_limit_valuation_gap_case
            else "NOT_APPLICABLE"
        ),
        "signed_fill_quantity": signed_fill_quantity,
    }


def _write_pack(pack_root: Path, source_root: Path, selection: list[dict[str, Any]], rolls: list[dict[str, str]]) -> None:
    _write_csv(pack_root / "runtime_evidence_ledger.csv", [row["runtime"] for row in selection])
    _write_csv(pack_root / "hourly_decision_completed_bar.csv", [_hourly_row_from_source(row["decision"], row["runtime"], "DECISION", index) for index, row in enumerate(selection, 1)])
    _write_csv(pack_root / "hourly_fill_completed_bar.csv", [_hourly_row_from_source(row["fill"], row["runtime"], "FILL", index) for index, row in enumerate(selection, 1)])
    _write_csv(pack_root / "valuation_mark_completed_bar.csv", [_valuation_row_from_source(row["mark"], row["runtime"], index) for index, row in enumerate(selection, 1)])
    _write_csv(pack_root / "daily_continuous_completed_bar.csv", _daily_summary_rows(selection))
    _write_csv(pack_root / "daily_current_contract_completed_bar.csv", _daily_current_rows(selection))
    _write_csv(pack_root / "session_calendar.csv", _session_rows(selection))
    cutoff = selection[-1]["runtime"]["previous_daily_trading_date"]
    roll_boundary_dates = selection[-1]["mechanics"].get("roll_boundary_dates", ())
    if roll_boundary_dates:
        cutoff = max([cutoff, *roll_boundary_dates])
    _write_csv(pack_root / "roll_calendar.csv", _roll_rows(rolls, cutoff))
    _write_csv(pack_root / "cost_parameter.csv", _cost_rows())
    del source_root


def _manifest(pack_root: Path, source_root: Path, selection: list[dict[str, Any]]) -> dict[str, Any]:
    row_family_files = {
        path.name: {"row_count": _csv_row_count(path), "sha256": _sha256(path)}
        for path in sorted(pack_root.glob("*.csv"))
    }
    blocker = selection[-1]
    pack_exhausted = (
        len(selection) >= AUTHORIZED_2023_TEST_DECLARED_PACK_ROW_LIMIT
        and blocker["mechanics"]["formula_status"] == "PASS_FORMULA_SUPPORTED"
    )
    return {
        "artifact": "S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST",
        "authorization": AUTHORIZATION,
        "status": PACK_STATUS,
        "lane": S27_V2_LANE,
        "selected_slice_rule": (
            "CONTROLLED_LOCAL_ONLY_2023_TEST_COMPLETED_ROWS_TO_AUTHORIZED_DECLARED_PACK_LIMIT"
            if pack_exhausted
            else "CONTROLLED_LOCAL_ONLY_2023_TEST_COMPLETED_ROWS_UNTIL_FIRST_AUDITED_FAIL_CLOSED_EXECUTION_BLOCKER"
        ),
        "test_window_start": selection[0]["decision"]["derived_completed_bar_end_utc"],
        "test_window_fail_closed_timestamp": (
            "NOT_APPLICABLE_DECLARED_PACK_EXHAUSTED_NO_FAIL_CLOSED_BLOCKER"
            if pack_exhausted
            else blocker["decision"]["derived_completed_bar_end_utc"]
        ),
        "test_window_terminal_timestamp": blocker["decision"]["derived_completed_bar_end_utc"],
        "test_window_end_status": (
            "DECLARED_PACK_EXHAUSTED_NO_FAIL_CLOSED_BLOCKER_NOT_RESULT"
            if pack_exhausted
            else "FAIL_CLOSED_BEFORE_FULL_2023_COMPLETION_NO_RESULT"
        ),
        "source_continuous_daily_ledger": str((source_root / SOURCE_CONTINUOUS_NAME).relative_to(_REPO_ROOT)),
        "source_roll_ledger": str((source_root / SOURCE_ROLL_NAME).relative_to(_REPO_ROOT)),
        "source_hourly_ledger": str((source_root / SOURCE_HOURLY_NAME).relative_to(_REPO_ROOT)),
        "source_selection_exclusion_ledger": str((source_root / SOURCE_EXCLUSION_NAME).relative_to(_REPO_ROOT)),
        "row_family_files": row_family_files,
        "candidate_row_count": len(selection),
        "supported_mechanical_row_count": len(selection) if pack_exhausted else len(selection) - 1,
        "fail_closed_blocker": {
            "row_index": 0 if pack_exhausted else len(selection),
            "decision_timestamp_utc": (
                "NOT_APPLICABLE_DECLARED_PACK_EXHAUSTED"
                if pack_exhausted
                else blocker["decision"]["derived_completed_bar_end_utc"]
            ),
            "raw_symbol": blocker["decision"]["raw_symbol"],
            "starting_position_contracts": blocker["mechanics"]["starting_position_contracts"],
            "desired_position_contracts": blocker["mechanics"]["desired_position_contracts"],
            "position_change_contracts": blocker["mechanics"]["position_change_contracts"],
            "order_side": blocker["mechanics"]["order_side"],
            "adjacent_target_position": blocker["mechanics"]["adjacent_target_position"],
            "formula_status": (
                NO_FAIL_CLOSED_BLOCKER_PACK_EXHAUSTED_STATUS
                if pack_exhausted
                else blocker["mechanics"]["formula_status"]
            ),
        },
        "explicitly_excluded_data": ["NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"],
        "non_authorizations": list(NON_AUTHORIZATIONS),
    }


def _validate_paths(pack_path: Path, output_root: Path) -> None:
    if pack_path != (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 2023 TEST runner is locked to the declared local 2023 TEST pack")
    if output_root != (_REPO_ROOT / DEFAULT_OUTPUT_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 2023 TEST runner output root is locked to the local 2023 TEST run")


def _validate_pack_checksums(pack_path: Path, manifest_name: str, checksum_name: str) -> None:
    checksums: dict[str, str] = {}
    for line in (pack_path / checksum_name).read_text(encoding="ascii").splitlines():
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            raise CarverBlocked("S27 v2 2023 TEST checksum file is malformed")
        checksums[parts[1]] = parts[0].upper()
    for filename in (*ROW_FAMILY_FILES, manifest_name):
        if checksums.get(filename) != _sha256(pack_path / filename).upper():
            raise CarverBlocked("S27 v2 2023 TEST checksum file must bind file bytes")


def _validate_manifest(pack_path: Path, manifest: dict[str, Any], rows: dict[str, list[dict[str, str]]]) -> None:
    if manifest.get("authorization") != AUTHORIZATION or manifest.get("status") != PACK_STATUS:
        raise CarverBlocked("S27 v2 2023 TEST pack status/authorization is not locked")
    if manifest.get("lane") != S27_V2_LANE:
        raise CarverBlocked("S27 v2 2023 TEST pack must remain source-native futures")
    if tuple(manifest.get("non_authorizations", ())) != NON_AUTHORIZATIONS:
        raise CarverBlocked("S27 v2 2023 TEST pack must preserve non-authorizations")
    for forbidden in ("NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"):
        if forbidden not in tuple(manifest.get("explicitly_excluded_data", ())):
            raise CarverBlocked("S27 v2 2023 TEST protected-window exclusion is missing")
    declared = manifest.get("row_family_files")
    if not isinstance(declared, dict) or set(declared) != set(ROW_FAMILY_FILES):
        raise CarverBlocked("S27 v2 2023 TEST row-family declaration is not locked")
    for filename in ROW_FAMILY_FILES:
        if str(declared[filename]["sha256"]).upper() != _sha256(pack_path / filename).upper():
            raise CarverBlocked("S27 v2 2023 TEST row-family bytes must match manifest")
    row_count = len(rows["hourly_decision_completed_bar.csv"])
    if row_count < 1:
        raise CarverBlocked("S27 v2 2023 TEST refuses empty pack")
    for family in ("hourly_fill_completed_bar.csv", "valuation_mark_completed_bar.csv", "runtime_evidence_ledger.csv"):
        if len(rows[family]) != row_count:
            raise CarverBlocked("S27 v2 2023 TEST row families must align one-to-one")
    for family in ("hourly_decision_completed_bar.csv", "hourly_fill_completed_bar.csv", "valuation_mark_completed_bar.csv"):
        for row in rows[family]:
            if not str(row["completed_timestamp_utc"]).startswith("2023-"):
                raise CarverBlocked("S27 v2 2023 TEST selected rows must stay in 2023")


def _validate_runtime_evidence_against_source(manifest: dict[str, Any], runtime_rows: list[dict[str, str]]) -> None:
    continuous = _read_csv_rows(_REPO_ROOT / manifest["source_continuous_daily_ledger"])
    rolls = _read_csv_rows(_REPO_ROOT / manifest["source_roll_ledger"])
    hourly = {
        row["derived_completed_bar_end_utc"]: row
        for row in _read_csv_rows(_REPO_ROOT / manifest["source_hourly_ledger"])
        if row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
    }
    continuous_by_date = {row["completed_trading_date"]: row for row in continuous}
    cache: dict[str, list[dict[str, Any]]] = {}
    for runtime in runtime_rows:
        decision = hourly.get(runtime["decision_timestamp_utc"])
        if decision is None:
            raise CarverBlocked("S27 v2 2023 TEST runtime decision must exist in source hourly ledger")
        previous_daily_date = max(day for day in continuous_by_date if day < decision["completed_trading_date"])
        if runtime["previous_daily_trading_date"] != previous_daily_date:
            raise CarverBlocked("S27 v2 2023 TEST runtime row must bind strict-prior previous daily date")
        if previous_daily_date not in cache:
            cache[previous_daily_date] = _point_in_time_continuous_series(continuous, rolls, previous_daily_date)
        pit = cache[previous_daily_date]
        sigma_rows = _build_sigma_rows(pit)
        vqm_rows = _build_vqm_rows(sigma_rows)
        sigma_by_date = {row["completed_trading_date"]: row for row in sigma_rows}
        vqm_by_date = {row["completed_trading_date"]: row for row in vqm_rows}
        prior_vqm_dates = [day for day in vqm_by_date if day < decision["completed_trading_date"]]
        if previous_daily_date not in sigma_by_date or not prior_vqm_dates:
            raise CarverBlocked("S27 v2 2023 TEST runtime evidence lacks strict-prior sigma/VQM")
        expected = _runtime_row_from_source(
            pit=pit,
            sigma=sigma_by_date[previous_daily_date],
            vqm=vqm_by_date[max(prior_vqm_dates)],
            decision=decision,
            row_index=int(runtime["row_index"]),
        )
        _require_rows_equal(runtime, expected, "S27 v2 2023 TEST runtime evidence")


def _validate_selected_hourly_rows_against_source(
    manifest: dict[str, Any],
    runtime_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    mark_rows: list[dict[str, str]],
) -> None:
    source_hourly = [
        row
        for row in _read_csv_rows(_REPO_ROOT / manifest["source_hourly_ledger"])
        if row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
    ]
    source_by_hash = {_row_hash("strategy_facing_hourly_available_bars", row): row for row in source_hourly}
    source_by_symbol = _group_hourly_by_symbol(source_hourly)
    for runtime, decision, fill, mark in zip(runtime_rows, decision_rows, fill_rows, mark_rows, strict=True):
        decision_source = _source_hourly_row_by_hash(source_by_hash, decision["source_row_hash"], "decision")
        fill_source = _source_hourly_row_by_hash(source_by_hash, fill["source_row_hash"], "fill")
        mark_source = _source_hourly_row_by_hash(source_by_hash, mark["source_row_hash"], "valuation mark")
        _require_rows_equal(decision, _hourly_row_from_source(decision_source, runtime, "DECISION", int(decision["row_index"])), "S27 v2 2023 TEST decision row")
        _require_rows_equal(fill, _hourly_row_from_source(fill_source, runtime, "FILL", int(fill["row_index"])), "S27 v2 2023 TEST fill row")
        _require_rows_equal(mark, _valuation_row_from_source(mark_source, runtime, int(mark["row_index"])), "S27 v2 2023 TEST valuation mark row")
        if decision_source["raw_symbol"] != fill_source["raw_symbol"] or decision_source["raw_symbol"] != mark_source["raw_symbol"]:
            raise CarverBlocked("S27 v2 2023 TEST decision/fill/valuation rows must stay on one raw-symbol path")
        expected_fill_ts = _z(_parse_timestamp(decision_source["derived_completed_bar_end_utc"]) + timedelta(hours=1))
        if fill_source["derived_completed_bar_end_utc"] != expected_fill_ts:
            raise CarverBlocked("S27 v2 2023 TEST fill row must be the one-hour same-symbol fill candidate")
        expected_mark = _next_same_symbol_source_row_after(source_by_symbol[decision_source["raw_symbol"]], fill_source["derived_completed_bar_end_utc"])
        if expected_mark is None or _row_hash("strategy_facing_hourly_available_bars", expected_mark) != mark["source_row_hash"]:
            raise CarverBlocked("S27 v2 2023 TEST valuation mark row must be next completed same-symbol source row after fill")


def _active_combined_market_tbbo_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(_prebound_market_tbbo_rows())
    rows.extend(_selected_registry_rows(MARKET_TBBO_BATCH_SELECTED_RELATIVE_PATH, "BATCH_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(_selected_registry_rows(MARKET_TBBO_FAILED_RETRY_SELECTED_RELATIVE_PATH, "RETRY_AT_OR_BEFORE_FILL_TBBO"))
    rows.append(_row215_engineering_market_tbbo_row())
    rows.extend(_optional_selected_registry_rows(STANDING_MARKET_TBBO_SELECTED_RELATIVE_PATH, "STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(_optional_selected_registry_rows(STANDING_MARKET_TBBO_RETRY_SELECTED_RELATIVE_PATH, "STANDING_RETRY_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(_optional_selected_registry_rows(ROW437_MARKET_TBBO_SELECTED_RELATIVE_PATH, "ROW437_BOUNDED_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(_optional_selected_registry_rows(ROW438_MARKET_TBBO_RETRY_SELECTED_RELATIVE_PATH, "ROW438_RETRY_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(
        _optional_selected_registry_rows(
            ROW441_MARKET_TBBO_EXTENDED_SELECTED_RELATIVE_PATH,
            "ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO",
        )
    )
    rows.extend(
        _optional_selected_registry_rows(
            ROW547_MARKET_TBBO_SELECTED_RELATIVE_PATH,
            "ROW547_CAP_BOUND_AT_OR_BEFORE_FILL_TBBO",
        )
    )
    rows.extend(
        _optional_selected_registry_rows(
            ZNM3_EXTENDED_MARKET_TBBO_SELECTED_RELATIVE_PATH,
            "ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO",
        )
    )
    rows.extend(
        _optional_selected_registry_rows(
            ROW704_MBP1_TOP_OF_BOOK_SELECTED_RELATIVE_PATH,
            "ROW704_ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL",
        )
    )
    rows.extend(
        _optional_selected_registry_rows(
            ROW1356_MARKET_TBBO_SELECTED_RELATIVE_PATH,
            "ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION",
        )
    )
    rows.extend(_optional_selected_registry_rows(ROW1364_MARKET_TBBO_SELECTED_RELATIVE_PATH, "ROW1364_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(_optional_selected_registry_rows(ROW1366_MARKET_TBBO_SELECTED_RELATIVE_PATH, "ROW1366_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(_optional_selected_registry_rows(ROW1369_MARKET_TBBO_SELECTED_RELATIVE_PATH, "ROW1369_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(_optional_selected_registry_rows(ROW1370_MARKET_TBBO_SELECTED_RELATIVE_PATH, "ROW1370_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(_optional_selected_registry_rows(ROW1374_MARKET_TBBO_SELECTED_RELATIVE_PATH, "ROW1374_AT_OR_BEFORE_FILL_TBBO"))
    rows.extend(
        _optional_selected_registry_rows(
            ROW1378_MARKET_TBBO_SELECTED_RELATIVE_PATH,
            "ROW1378_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION",
        )
    )
    dedup: dict[int, dict[str, str]] = {}
    for row in rows:
        row_index = int(row["row_index"])
        if row_index in dedup:
            raise CarverBlocked(f"S27 v2 2023 TEST duplicate combined TBBO row {row_index}")
        dedup[row_index] = row
    expected_indices = (
        {1, 2}
        | _selected_registry_indices(MARKET_TBBO_BATCH_SELECTED_RELATIVE_PATH)
        | _selected_registry_indices(MARKET_TBBO_FAILED_RETRY_SELECTED_RELATIVE_PATH)
        | _selected_registry_indices(STANDING_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(STANDING_MARKET_TBBO_RETRY_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW437_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW438_MARKET_TBBO_RETRY_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW441_MARKET_TBBO_EXTENDED_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW547_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ZNM3_EXTENDED_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW704_MBP1_TOP_OF_BOOK_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW1356_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW1364_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW1366_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW1369_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW1370_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW1374_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | _selected_registry_indices(ROW1378_MARKET_TBBO_SELECTED_RELATIVE_PATH, optional=True)
        | {215}
    )
    if set(dedup) != expected_indices:
        raise CarverBlocked("S27 v2 2023 TEST combined TBBO registry active row coverage drift")
    return [dedup[index] for index in sorted(dedup)]


def _prebound_market_tbbo_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row_index, expected in sorted(MARKET_TBBO_SPREAD_EVIDENCE_BY_ROW.items()):
        path = _REPO_ROOT / expected["path"]
        ledger_rows = _safe_read_csv_rows(path, f"S27 v2 2023 TEST row-{row_index} prebound TBBO evidence")
        if len(ledger_rows) != 1:
            raise CarverBlocked(f"S27 v2 2023 TEST row-{row_index} prebound TBBO evidence must contain one row")
        row = dict(ledger_rows[0])
        for key, value in expected.items():
            if key == "path" or key not in row:
                continue
            if str(row[key]) != str(value):
                raise CarverBlocked(f"S27 v2 2023 TEST row-{row_index} prebound TBBO evidence drift: {key}")
        rows.append(_combined_market_tbbo_row(row, path, f"PREBOUND_ROW_{row_index}_TBBO"))
    return rows


def _selected_registry_rows(relative_path: str, evidence_type: str) -> list[dict[str, str]]:
    path = _REPO_ROOT / relative_path
    rows = []
    for row in _safe_read_csv_rows(path, f"S27 v2 2023 TEST {evidence_type} registry"):
        if not row["selection_status"].startswith("PASS_"):
            continue
        rows.append(_combined_market_tbbo_row(row, path, evidence_type))
    return rows


def _selected_registry_indices(relative_path: str, *, optional: bool = False) -> set[int]:
    path = _REPO_ROOT / relative_path
    if optional and not path.exists():
        return set()
    return {int(row["row_index"]) for row in _read_csv_rows(path) if row["selection_status"].startswith("PASS_")}


def _optional_selected_registry_rows(relative_path: str, evidence_type: str) -> list[dict[str, str]]:
    path = _REPO_ROOT / relative_path
    if not path.exists():
        return []
    return _selected_registry_rows(relative_path, evidence_type)


def _row215_engineering_market_tbbo_row() -> dict[str, str]:
    policy_path = _REPO_ROOT / MARKET_TBBO_ROW215_POLICY_RECORD_RELATIVE_PATH
    if not policy_path.exists():
        raise CarverBlocked("S27 v2 TEST row-215 TBBO policy record is missing")
    raw_csv = (
        _REPO_ROOT
        / "docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_failed_window_retry/"
        / "raw_provider_output/20260612_S27_V2_2023_TEST_MARKET_ORDER_TBBO_FAILED_WINDOW_RETRY_row_215_tbbo_dataframe.csv"
    )
    raw_rows = _safe_read_csv_rows(raw_csv, "S27 v2 2023 TEST row-215 retry raw TBBO CSV")
    if len(raw_rows) != 2:
        raise CarverBlocked("S27 v2 2023 TEST row-215 retry raw TBBO row count drift")
    first = raw_rows[0]
    if (
        str(first["ts_event"]) != "2023-01-16 17:00:00.681503831+00:00"
        or str(first["bid_px_00"]) != ROW215_ENGINEERING_TBBO_EVIDENCE["bid_px_00"]
        or str(first["ask_px_00"]) != ROW215_ENGINEERING_TBBO_EVIDENCE["ask_px_00"]
    ):
        raise CarverBlocked("S27 v2 2023 TEST row-215 engineering TBBO source row drift")
    row = dict(ROW215_ENGINEERING_TBBO_EVIDENCE)
    row["source_selected_spread_row_hash"] = canonical_sha256(
        {key: value for key, value in row.items() if key not in {"path", "policy_record_path"}}
    )
    row["source_selected_spread_ledger_sha256"] = _sha256(policy_path)
    row["source_evidence_path"] = MARKET_TBBO_ROW215_POLICY_RECORD_RELATIVE_PATH
    row["source_evidence_type"] = "ROW215_ENGINEERING_AFTER_FILL_TBBO_POLICY"
    row["selection_status"] = "PASS_ROW215_ENGINEERING_AFTER_FILL_TBBO_QUOTE_SELECTED_NOT_RESULT"
    return _finalise_combined_market_tbbo_row(row)


def _combined_market_tbbo_row(row: dict[str, str], source_path: Path, evidence_type: str) -> dict[str, str]:
    _validate_selected_tbbo_row_against_raw(row, source_path, evidence_type)
    side = row.get("market_order_side") or ("BUY" if row["row_index"] == "1" else row.get("order_side", ""))
    executable_price = row.get("selected_executable_market_fill_price", "")
    if not executable_price and side == "BUY":
        executable_price = row["ask_px_00"]
    if not executable_price and side == "SELL":
        executable_price = row["bid_px_00"]
    executable_source = row.get("executable_market_fill_price_source", "")
    if not executable_source and side == "BUY":
        executable_source = "ASK_PRICE_FOR_BUY_MARKET_ORDER"
    if not executable_source and side == "SELL":
        executable_source = "BID_PRICE_FOR_SELL_MARKET_ORDER"
    combined = {
        "row_index": row["row_index"],
        "decision_timestamp_utc": row.get("decision_timestamp_utc", ""),
        "fill_timestamp_utc": row["fill_timestamp_utc"],
        "raw_symbol": row["raw_symbol"],
        "market_order_side": side,
        "fill_quantity": row["fill_quantity"],
        "selected_quote_ts_event": row["selected_quote_ts_event"],
        "quote_age_seconds": row.get("quote_age_seconds", ""),
        "bid_px_00": row["bid_px_00"],
        "ask_px_00": row["ask_px_00"],
        "selected_executable_market_fill_price": executable_price,
        "executable_market_fill_price_source": executable_source,
        "spread_points": row["spread_points"],
        "point_value_usd": row["point_value_usd"],
        "spread_cost_usd_per_contract": row["spread_cost_usd_per_contract"],
        "spread_cost_amount_usd": row["spread_cost_amount_usd"],
        "spread_source": row["spread_source"],
        "selection_rule": row.get("selection_rule", "LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP"),
        "post_fill_quote_selection": row.get("post_fill_quote_selection", "DISALLOWED_TO_AVOID_LOOKAHEAD"),
        "cost_classification": row["cost_classification"],
        "actual_cost_emission_authorized": row["actual_cost_emission_authorized"],
        "pnl_result_emission_authorized": row["pnl_result_emission_authorized"],
        "source_selected_spread_row_hash": row["row_hash"],
        "source_selected_spread_ledger_sha256": _sha256(source_path),
        "source_evidence_path": str(source_path.relative_to(_REPO_ROOT)).replace("\\", "/"),
        "source_evidence_type": evidence_type,
        "raw_dbn_sha256": row.get("raw_dbn_sha256", row.get("retry_raw_dbn_sha256", "")),
        "raw_csv_sha256": row.get("raw_csv_sha256", row.get("retry_raw_csv_sha256", "")),
        "selection_status": row.get("selection_status", "PASS_PREBOUND_TBBO_QUOTE_SELECTED_NOT_RESULT"),
    }
    return _finalise_combined_market_tbbo_row(combined)


def _validate_selected_tbbo_row_against_raw(row: dict[str, str], source_path: Path, evidence_type: str) -> None:
    if evidence_type.startswith("PREBOUND_ROW_"):
        return
    if not row.get("raw_csv_sha256") and not row.get("retry_raw_csv_sha256"):
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} selected row must bind raw CSV bytes")
    if not row.get("raw_dbn_sha256") and not row.get("retry_raw_dbn_sha256"):
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} selected row must bind raw DBN bytes")
    raw_registry = _raw_output_registry_for_selected_registry(source_path)
    if raw_registry is None:
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} raw output registry is missing")
    raw_row = _raw_output_registry_row(raw_registry, row["row_index"])
    raw_csv_path = _raw_path_from_registry(raw_row, "raw_csv_relative_path", "retry_raw_csv_relative_path")
    raw_dbn_path = _raw_path_from_registry(raw_row, "raw_dbn_relative_path", "retry_raw_dbn_relative_path")
    expected_csv_hash = row.get("raw_csv_sha256", row.get("retry_raw_csv_sha256", ""))
    expected_dbn_hash = row.get("raw_dbn_sha256", row.get("retry_raw_dbn_sha256", ""))
    if not expected_csv_hash or expected_csv_hash.startswith("MISSING"):
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} selected row must bind raw CSV bytes")
    if not expected_dbn_hash or expected_dbn_hash.startswith("MISSING"):
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} selected row must bind raw DBN bytes")
    if _sha256(raw_csv_path).upper() != str(expected_csv_hash).upper():
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} raw CSV hash drift")
    if _sha256(raw_dbn_path).upper() != str(expected_dbn_hash).upper():
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} raw DBN hash drift")
    selected = (
        _select_first_post_fill_tbbo_from_raw_csv(raw_csv_path, row, evidence_type)
        if evidence_type
        in {
            "ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION",
            "ROW1378_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION",
        }
        else _select_tbbo_from_raw_csv(raw_csv_path, row, _max_quote_age_for_evidence(evidence_type))
    )
    if selected is None:
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} raw CSV does not support selected quote")
    _require_tbbo_selected_value(row, "selected_quote_ts_event", selected["selected_quote_ts_event"], evidence_type)
    _require_tbbo_selected_value(row, "bid_px_00", selected["bid_px_00"], evidence_type)
    _require_tbbo_selected_value(row, "ask_px_00", selected["ask_px_00"], evidence_type)
    _require_tbbo_selected_value(row, "quote_age_seconds", selected["quote_age_seconds"], evidence_type)
    if evidence_type == "ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION":
        if str(row.get("row_index")) != "1356":
            raise CarverBlocked("S27 v2 2023 TEST row-1356 engineering TBBO evidence is row-bounded")
        if str(row.get("spread_source")) != "ROW1356_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT":
            raise CarverBlocked("S27 v2 2023 TEST row-1356 engineering TBBO label drift")
        if str(row.get("post_fill_quote_selection")) != "ROW1356_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT":
            raise CarverBlocked("S27 v2 2023 TEST row-1356 engineering TBBO post-fill policy label drift")
        if str(row.get("selected_executable_market_fill_price")) != "114.484375":
            raise CarverBlocked("S27 v2 2023 TEST row-1356 engineering TBBO must bind selected SELL bid")
    if evidence_type == "ROW1378_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION":
        if str(row.get("row_index")) != "1378":
            raise CarverBlocked("S27 v2 2023 TEST row-1378 engineering TBBO evidence is row-bounded")
        if str(row.get("spread_source")) != "ROW1378_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT":
            raise CarverBlocked("S27 v2 2023 TEST row-1378 engineering TBBO label drift")
        if str(row.get("post_fill_quote_selection")) != "ROW1378_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT":
            raise CarverBlocked("S27 v2 2023 TEST row-1378 engineering TBBO post-fill policy label drift")
        if str(row.get("selected_executable_market_fill_price")) != "114.515625":
            raise CarverBlocked("S27 v2 2023 TEST row-1378 engineering TBBO must bind selected SELL bid")


def _raw_output_registry_for_selected_registry(source_path: Path) -> Path | None:
    root = source_path.parent.parent
    stem = source_path.name
    if stem.endswith("_selected_spread_registry.csv"):
        run_id = stem[: -len("_selected_spread_registry.csv")]
    elif stem.endswith("_selected_spread_ledger.csv"):
        run_id = stem[: -len("_selected_spread_ledger.csv")]
    else:
        return None
    raw_registry = root / "raw_provider_output" / f"{run_id}_raw_output_registry.csv"
    return raw_registry if raw_registry.exists() else None


def _raw_output_registry_row(raw_registry: Path, row_index: str) -> dict[str, str]:
    for raw_row in _safe_read_csv_rows(raw_registry, "S27 v2 2023 TEST raw TBBO output registry"):
        if raw_row["row_index"] == str(row_index):
            return raw_row
    raise CarverBlocked(f"S27 v2 2023 TEST raw TBBO output registry missing row {row_index}")


def _raw_path_from_registry(row: dict[str, str], *keys: str) -> Path:
    for key in keys:
        value = row.get(key, "")
        if value and not value.startswith("MISSING"):
            path = _REPO_ROOT / value
            if not path.exists():
                raise CarverBlocked(f"S27 v2 2023 TEST raw TBBO file is missing: {value}")
            return path
    raise CarverBlocked("S27 v2 2023 TEST raw TBBO registry must bind file paths")


def _max_quote_age_for_evidence(evidence_type: str) -> float:
    if (
        "ROW441_EXTENDED_LOOKBACK" in evidence_type
        or "ZNM3_EXTENDED_LOOKBACK" in evidence_type
        or "ROW704_ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK" in evidence_type
    ):
        return 300.0
    if "RETRY" in evidence_type:
        return 60.0
    return 5.0


def _select_tbbo_from_raw_csv(raw_csv_path: Path, selected_row: dict[str, str], max_age_seconds: float) -> dict[str, str] | None:
    fill_time = _parse_timestamp(selected_row["fill_timestamp_utc"])
    candidates: list[tuple[datetime, dict[str, str]]] = []
    for raw_row in _safe_read_csv_rows(raw_csv_path, "S27 v2 2023 TEST raw TBBO CSV"):
        bid = _float_from_raw_tbbo(raw_row.get("bid_px_00", raw_row.get("bid_px_0", raw_row.get("bid_px", ""))))
        ask = _float_from_raw_tbbo(raw_row.get("ask_px_00", raw_row.get("ask_px_0", raw_row.get("ask_px", ""))))
        if bid is None or ask is None or bid <= 0.0 or ask <= 0.0 or ask < bid:
            continue
        ts_event = _parse_raw_tbbo_timestamp(raw_row.get("ts_event", ""))
        age_seconds = (fill_time - ts_event).total_seconds()
        if 0.0 <= age_seconds <= max_age_seconds:
            candidates.append(
                (
                    ts_event,
                    {
                        "selected_quote_ts_event": _normalise_raw_tbbo_timestamp_text(raw_row.get("ts_event", "")),
                        "quote_age_seconds": _csv_value(age_seconds),
                        "bid_px_00": _csv_value(bid),
                        "ask_px_00": _csv_value(ask),
                    },
                )
            )
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: item[0])[-1][1]


_FIRST_POST_FILL_TBBO_EXPECTED_FACTS = {
    "ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION": {
        "row_index": "1356",
        "fill_timestamp_utc": "2023-03-30T00:00:00Z",
        "selected_quote_ts_event": "2023-03-30T00:00:00.099806785Z",
        "bid_px_00": "114.484375",
        "ask_px_00": "114.5",
    },
    "ROW1378_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION": {
        "row_index": "1378",
        "fill_timestamp_utc": "2023-03-31T00:00:00Z",
        "selected_quote_ts_event": "2023-03-31T00:00:00.183796035Z",
        "bid_px_00": "114.515625",
        "ask_px_00": "114.53125",
    },
}


def _select_first_post_fill_tbbo_from_raw_csv(
    raw_csv_path: Path,
    selected_row: dict[str, str],
    evidence_type: str,
) -> dict[str, str] | None:
    expected = _FIRST_POST_FILL_TBBO_EXPECTED_FACTS[evidence_type]
    row_index = expected["row_index"]
    if str(selected_row.get("row_index")) != row_index:
        raise CarverBlocked(f"S27 v2 2023 TEST row-{row_index} engineering TBBO selector is row-bounded")
    if str(selected_row.get("fill_timestamp_utc")) != expected["fill_timestamp_utc"]:
        raise CarverBlocked(f"S27 v2 2023 TEST row-{row_index} engineering TBBO fill timestamp drift")
    fill_time = _parse_timestamp(expected["fill_timestamp_utc"])
    candidates: list[tuple[datetime, dict[str, str]]] = []
    for raw_row in _safe_read_csv_rows(raw_csv_path, f"S27 v2 2023 TEST row-{row_index} raw TBBO CSV"):
        bid = _float_from_raw_tbbo(raw_row.get("bid_px_00", raw_row.get("bid_px_0", raw_row.get("bid_px", ""))))
        ask = _float_from_raw_tbbo(raw_row.get("ask_px_00", raw_row.get("ask_px_0", raw_row.get("ask_px", ""))))
        if bid is None or ask is None or bid <= 0.0 or ask <= 0.0 or ask < bid:
            continue
        ts_event = _parse_raw_tbbo_timestamp(raw_row.get("ts_event", ""))
        lag_seconds = (ts_event - fill_time).total_seconds()
        if 0.0 < lag_seconds <= 1.0:
            candidates.append(
                (
                    ts_event,
                    {
                        "selected_quote_ts_event": _normalise_raw_tbbo_timestamp_text(raw_row.get("ts_event", "")),
                        "quote_age_seconds": _csv_value(lag_seconds),
                        "bid_px_00": _csv_value(bid),
                        "ask_px_00": _csv_value(ask),
                    },
                )
            )
    if not candidates:
        return None
    selected = sorted(candidates, key=lambda item: item[0])[0][1]
    if (
        selected["selected_quote_ts_event"] != expected["selected_quote_ts_event"]
        or selected["bid_px_00"] != expected["bid_px_00"]
        or selected["ask_px_00"] != expected["ask_px_00"]
    ):
        raise CarverBlocked(f"S27 v2 2023 TEST row-{row_index} engineering TBBO selected quote drift")
    return selected


def _parse_raw_tbbo_timestamp(value: str) -> datetime:
    text = str(value).strip()
    if not text:
        raise CarverBlocked("S27 v2 2023 TEST raw TBBO timestamp is empty")
    text = text.replace(" ", "T")
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _normalise_raw_tbbo_timestamp_text(value: str) -> str:
    text = str(value).strip().replace(" ", "T")
    if text.endswith("+00:00"):
        text = text[: -len("+00:00")] + "Z"
    if text.endswith("Z") and "." in text:
        base = text[:-1].rstrip("0").rstrip(".")
        text = f"{base}Z"
    return text


def _float_from_raw_tbbo(value: str | None) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def _require_tbbo_selected_value(row: dict[str, str], key: str, expected: str, evidence_type: str) -> None:
    observed = _csv_value(row.get(key, ""))
    if key in {"quote_age_seconds", "bid_px_00", "ask_px_00"}:
        if abs(float(observed) - float(expected)) <= 0.000001:
            return
    if observed != _csv_value(expected):
        raise CarverBlocked(f"S27 v2 2023 TEST {evidence_type} row {row.get('row_index', '')} selected TBBO {key} drift")


def _finalise_combined_market_tbbo_row(row: dict[str, str]) -> dict[str, str]:
    final = {key: _csv_value(value) for key, value in row.items() if key not in {"path", "policy_record_path"}}
    final["row_hash"] = canonical_sha256(final)
    return final


def _expected_market_spread_evidence(row_index: int) -> dict[str, str]:
    registry = (_REPO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_RELATIVE_PATH / COMBINED_MARKET_TBBO_REGISTRY_NAME).resolve()
    if not registry.exists():
        build_2023_test_combined_market_tbbo_registry()
    registry_sha = _sha256(registry)
    global _EXPECTED_MARKET_SPREAD_EVIDENCE_CACHE
    if (
        _EXPECTED_MARKET_SPREAD_EVIDENCE_CACHE is not None
        and _EXPECTED_MARKET_SPREAD_EVIDENCE_CACHE["registry_sha"] == registry_sha
    ):
        try:
            return dict(_EXPECTED_MARKET_SPREAD_EVIDENCE_CACHE["rows_by_index"][row_index])
        except KeyError as exc:
            raise CarverBlocked(f"S27 v2 2023 TEST market TBBO spread evidence is not bound for row {row_index}") from exc
    active = _active_combined_market_tbbo_rows()
    registry_rows = _safe_read_csv_rows(registry, "S27 v2 2023 TEST combined market TBBO registry")
    active_by_index = {int(row["row_index"]): row for row in active}
    registry_by_index = {int(row["row_index"]): row for row in registry_rows}
    if registry_by_index != active_by_index:
        raise CarverBlocked("S27 v2 2023 TEST combined market TBBO registry drift")
    _EXPECTED_MARKET_SPREAD_EVIDENCE_CACHE = {
        "registry_sha": registry_sha,
        "rows_by_index": registry_by_index,
    }
    try:
        return dict(registry_by_index[row_index])
    except KeyError as exc:
        raise CarverBlocked(f"S27 v2 2023 TEST market TBBO spread evidence is not bound for row {row_index}") from exc


def _market_spread_evidence_is_bound(row_index: int) -> bool:
    try:
        _expected_market_spread_evidence(row_index)
    except CarverBlocked:
        return False
    return True


def _market_spread_evidence_matches(row_index: int, side: str, fill_timestamp_utc: str) -> bool:
    try:
        _load_market_spread_evidence(row_index, side, fill_timestamp_utc)
    except CarverBlocked:
        return False
    return True


def _load_market_spread_evidence(row_index: int, side: str, fill_timestamp_utc: str) -> dict[str, str]:
    expected = _expected_market_spread_evidence(row_index)
    row = dict(expected)
    if str(row["fill_timestamp_utc"]) != fill_timestamp_utc:
        raise CarverBlocked(f"S27 v2 2023 TEST row-{row_index} market spread evidence fill timestamp drift")
    if str(row.get("market_order_side", "")) != side:
        raise CarverBlocked(f"S27 v2 2023 TEST row-{row_index} market spread evidence must bind order side")
    require_hash(f"S27 v2 2023 TEST row-{row_index} market spread evidence row hash", row["row_hash"])
    if row_index in {1, 2}:
        row.setdefault("selection_status", "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT")
        row.setdefault("source_evidence_type", "DIRECT_AT_OR_BEFORE_FILL_TBBO")
    return {
        **row,
        "selected_spread_ledger_sha256": _sha256(
            _REPO_ROOT / COMBINED_MARKET_TBBO_REGISTRY_RELATIVE_PATH / COMBINED_MARKET_TBBO_REGISTRY_NAME
        ),
    }


def _market_fill_price_from_evidence(evidence: dict[str, str], side: str) -> float:
    if "selected_executable_market_fill_price" in evidence:
        return float(evidence["selected_executable_market_fill_price"])
    if side == "BUY":
        return float(evidence["ask_px_00"])
    if side == "SELL":
        return float(evidence["bid_px_00"])
    raise CarverBlocked("S27 v2 2023 TEST market fill price requires BUY or SELL side")


def _row_timestamp(row: dict[str, Any]) -> str:
    return str(row.get("derived_completed_bar_end_utc") or row.get("completed_timestamp_utc") or "")


def _same_execution_session(decision: dict[str, Any], fill: dict[str, Any]) -> bool:
    decision_session = str(decision.get("session_id") or _session_id(_row_timestamp(decision)))
    fill_session = str(fill.get("session_id") or _session_id(_row_timestamp(fill)))
    return decision_session == fill_session


def _same_execution_and_valuation_session(
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
) -> bool:
    decision_session = str(decision.get("session_id") or _session_id(_row_timestamp(decision)))
    fill_session = str(fill.get("session_id") or _session_id(_row_timestamp(fill)))
    mark_session = str(mark.get("session_id") or _session_id(_row_timestamp(mark)))
    return decision_session == fill_session == mark_session


def _is_row303_session_end_market_case(
    *,
    row_index: int,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    position_change: int,
    side: str,
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    return (
        row_index == 303
        and str(decision.get("raw_symbol")) == "ZNH3"
        and str(fill.get("raw_symbol")) == "ZNH3"
        and str(mark.get("raw_symbol")) == "ZNH3"
        and decision_ts == "2023-01-20T20:00:00Z"
        and fill_ts == "2023-01-20T21:00:00Z"
        and mark_ts == "2023-01-20T22:00:00Z"
        and position_change == 2
        and side == "BUY"
        and _same_execution_session(decision, fill)
        and fill_ts == decision_session_end
        and _z(_parse_timestamp(fill_ts) + timedelta(hours=1)) == mark_ts
        and valuation_label == VALUATION_CONVENTION_LABEL
    )


def _has_fresh_at_or_before_fill_tbbo(market_spread_evidence: dict[str, str]) -> bool:
    return (
        str(market_spread_evidence.get("selection_status")) == "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT"
        and str(market_spread_evidence.get("source_evidence_type")) in SESSION_MARKET_TBBO_EVIDENCE_TYPES
    )


def _is_zn_quarterly_raw_symbol(raw_symbol: str) -> bool:
    return (
        len(raw_symbol) == 4
        and raw_symbol.startswith("ZN")
        and raw_symbol[2] in {"H", "M", "U", "Z"}
        and raw_symbol[3].isdigit()
    )


def _is_session_end_market_case(
    *,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    market_spread_evidence: dict[str, str],
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    same_raw_symbol = str(decision.get("raw_symbol")) == str(fill.get("raw_symbol")) == str(mark.get("raw_symbol"))
    return (
        same_raw_symbol
        and _is_zn_quarterly_raw_symbol(str(decision.get("raw_symbol")))
        and _same_execution_session(decision, fill)
        and not _same_execution_and_valuation_session(decision, fill, mark)
        and fill_ts == decision_session_end
        and _z(_parse_timestamp(fill_ts) + timedelta(hours=1)) == mark_ts
        and valuation_label == VALUATION_CONVENTION_LABEL
        and _has_fresh_at_or_before_fill_tbbo(market_spread_evidence)
    )


def _is_row1113_session_end_market_valuation_gap_case(
    *,
    row_index: int,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    position_change: int,
    side: str,
    market_spread_evidence: dict[str, str],
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    return (
        row_index == 1113
        and str(decision.get("raw_symbol")) == "ZNM3"
        and str(fill.get("raw_symbol")) == "ZNM3"
        and str(mark.get("raw_symbol")) == "ZNM3"
        and decision_ts == "2023-03-14T20:00:00Z"
        and fill_ts == "2023-03-14T21:00:00Z"
        and mark_ts == "2023-03-14T23:00:00Z"
        and position_change == 2
        and side == "BUY"
        and _same_execution_session(decision, fill)
        and not _same_execution_and_valuation_session(decision, fill, mark)
        and fill_ts == decision_session_end
        and _z(_parse_timestamp(fill_ts) + timedelta(hours=1)) != mark_ts
        and valuation_label == VALUATION_CONVENTION_LABEL
        and _has_fresh_at_or_before_fill_tbbo(market_spread_evidence)
    )


def _is_session_open_market_reset_case(
    *,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    market_spread_evidence: dict[str, str],
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    fill_session_start, _ = _session_bounds(fill_ts)
    decision_session = str(decision.get("session_id") or _session_id(decision_ts))
    fill_session = str(fill.get("session_id") or _session_id(fill_ts))
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    same_raw_symbol = str(decision.get("raw_symbol")) == str(fill.get("raw_symbol")) == str(mark.get("raw_symbol"))
    return (
        same_raw_symbol
        and _is_zn_quarterly_raw_symbol(str(decision.get("raw_symbol")))
        and decision_ts == decision_session_end
        and fill_ts == fill_session_start
        and decision_session != fill_session
        and _parse_timestamp(mark_ts) > _parse_timestamp(fill_ts)
        and valuation_label == VALUATION_CONVENTION_LABEL
        and _has_fresh_at_or_before_fill_tbbo(market_spread_evidence)
    )


def _is_session_open_adjacent_limit_fill_case(
    *,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    position_change: int,
    side: str,
    fill_executed: bool,
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    fill_session_start, _ = _session_bounds(fill_ts)
    decision_session = str(decision.get("session_id") or _session_id(decision_ts))
    fill_session = str(fill.get("session_id") or _session_id(fill_ts))
    mark_session = str(mark.get("session_id") or _session_id(mark_ts))
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    return (
        fill_executed
        and abs(position_change) == 1
        and side in {"BUY", "SELL"}
        and str(decision.get("raw_symbol")) == str(fill.get("raw_symbol")) == str(mark.get("raw_symbol")) == "ZNH3"
        and decision_ts == decision_session_end
        and fill_ts == fill_session_start
        and decision_session != fill_session
        and fill_session == mark_session
        and _parse_timestamp(mark_ts) > _parse_timestamp(fill_ts)
        and valuation_label == VALUATION_CONVENTION_LABEL
    )


def _is_row892_session_end_adjacent_limit_fill_case(
    *,
    row_index: int,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    position_change: int,
    side: str,
    fill_executed: bool,
    fill_close: float,
    formula_limit: float,
    limit_price: float,
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    decision_session = str(decision.get("session_id") or _session_id(decision_ts))
    fill_session = str(fill.get("session_id") or _session_id(fill_ts))
    mark_session = str(mark.get("session_id") or _session_id(mark_ts))
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    return (
        row_index == 892
        and fill_executed
        and position_change == -1
        and side == "SELL"
        and str(decision.get("raw_symbol")) == "ZNM3"
        and str(fill.get("raw_symbol")) == "ZNM3"
        and str(mark.get("raw_symbol")) == "ZNM3"
        and decision_ts == "2023-02-28T20:00:00Z"
        and fill_ts == "2023-02-28T21:00:00Z"
        and mark_ts == "2023-02-28T22:00:00Z"
        and decision_session == fill_session
        and fill_ts == decision_session_end
        and mark_session != fill_session
        and _z(_parse_timestamp(fill_ts) + timedelta(hours=1)) == mark_ts
        and valuation_label == VALUATION_CONVENTION_LABEL
        and abs(formula_limit - 111.6707138465356) <= 1e-12
        and limit_price == 111.671875
        and fill_close == 111.671875
    )


def _is_row1355_session_end_adjacent_limit_valuation_gap_case(
    *,
    row_index: int,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    position_change: int,
    side: str,
    fill_executed: bool,
    fill_close: float,
    formula_limit: float,
    limit_price: float,
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    decision_session = str(decision.get("session_id") or _session_id(decision_ts))
    fill_session = str(fill.get("session_id") or _session_id(fill_ts))
    mark_session = str(mark.get("session_id") or _session_id(mark_ts))
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    return (
        row_index == 1355
        and fill_executed
        and position_change == 1
        and side == "BUY"
        and str(decision.get("raw_symbol")) == "ZNM3"
        and str(fill.get("raw_symbol")) == "ZNM3"
        and str(mark.get("raw_symbol")) == "ZNM3"
        and decision_ts == "2023-03-29T20:00:00Z"
        and fill_ts == "2023-03-29T21:00:00Z"
        and mark_ts == "2023-03-29T23:00:00Z"
        and decision_session == fill_session
        and fill_ts == decision_session_end
        and mark_session != fill_session
        and _z(_parse_timestamp(fill_ts) + timedelta(hours=1)) != mark_ts
        and valuation_label == VALUATION_CONVENTION_LABEL
        and abs(formula_limit - 114.49366645867451) <= 1e-12
        and limit_price == 114.484375
        and fill_close == 114.46875
    )


def _is_row391_session_end_market_case(
    *,
    row_index: int,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    position_change: int,
    side: str,
    market_spread_evidence: dict[str, str],
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    return (
        row_index == 391
        and str(decision.get("raw_symbol")) == "ZNH3"
        and str(fill.get("raw_symbol")) == "ZNH3"
        and str(mark.get("raw_symbol")) == "ZNH3"
        and decision_ts == "2023-01-26T20:00:00Z"
        and fill_ts == "2023-01-26T21:00:00Z"
        and mark_ts == "2023-01-26T22:00:00Z"
        and position_change == 8
        and side == "BUY"
        and _same_execution_session(decision, fill)
        and fill_ts == decision_session_end
        and _z(_parse_timestamp(fill_ts) + timedelta(hours=1)) == mark_ts
        and valuation_label == VALUATION_CONVENTION_LABEL
        and str(market_spread_evidence.get("selection_status")) == "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT"
        and str(market_spread_evidence.get("source_evidence_type")) == "STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO"
        and str(market_spread_evidence.get("selected_quote_ts_event")) == "2023-01-26T20:59:59.902217027Z"
        and float(market_spread_evidence.get("ask_px_00", "nan")) == 114.828125
    )


def _is_row304_engineering_session_open_market_reset_case(
    *,
    row_index: int,
    decision: dict[str, Any],
    fill: dict[str, Any],
    mark: dict[str, Any],
    position_change: int,
    side: str,
    market_spread_evidence: dict[str, str],
) -> bool:
    decision_ts = _row_timestamp(decision)
    fill_ts = _row_timestamp(fill)
    mark_ts = _row_timestamp(mark)
    _, decision_session_end = _session_bounds(decision_ts)
    fill_session_start, _ = _session_bounds(fill_ts)
    decision_session = str(decision.get("session_id") or _session_id(decision_ts))
    fill_session = str(fill.get("session_id") or _session_id(fill_ts))
    mark_session = str(mark.get("session_id") or _session_id(mark_ts))
    valuation_label = str(mark.get("valuation_convention_label", VALUATION_CONVENTION_LABEL))
    return (
        row_index == 304
        and str(decision.get("raw_symbol")) == "ZNH3"
        and str(fill.get("raw_symbol")) == "ZNH3"
        and str(mark.get("raw_symbol")) == "ZNH3"
        and decision_ts == "2023-01-20T21:00:00Z"
        and fill_ts == "2023-01-20T22:00:00Z"
        and mark_ts == "2023-01-23T00:00:00Z"
        and position_change == 2
        and side == "BUY"
        and decision_ts == decision_session_end
        and fill_ts == fill_session_start
        and decision_session != fill_session
        and fill_session != mark_session
        and valuation_label == VALUATION_CONVENTION_LABEL
        and str(market_spread_evidence.get("selection_status")) == "PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT"
        and str(market_spread_evidence.get("source_evidence_type")) == "BATCH_AT_OR_BEFORE_FILL_TBBO"
        and str(market_spread_evidence.get("selected_quote_ts_event")) == "2023-01-20T21:59:59.924187905Z"
        and float(market_spread_evidence.get("ask_px_00", "nan")) == 115.0625
    )


def _compute_rows_until_fail_closed(rows: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, Any]]]:
    cost = rows["cost_parameter.csv"][0]
    roll_dates = {row["roll_transition_date"] for row in rows["roll_calendar.csv"]}
    current_position = 0
    last_mark_price: float | None = None
    cumulative_gross = 0.0
    cumulative_commission = 0.0
    cumulative_spread = 0.0
    out: dict[str, list[dict[str, Any]]] = {
        name: []
        for name in (
            "runtime",
            "forecast",
            "position",
            "order",
            "market",
            "market_order",
            "transition",
            "fill",
            "market_fill_metadata",
            "cost",
            "pnl",
            "validation",
            "fail_closed",
        )
    }
    for index, (runtime, decision, fill, mark) in enumerate(zip(rows["runtime_evidence_ledger.csv"], rows["hourly_decision_completed_bar.csv"], rows["hourly_fill_completed_bar.csv"], rows["valuation_mark_completed_bar.csv"], strict=True), 1):
        decision_price = float(decision["close_price"])
        fill_close = float(fill["close_price"])
        mark_price = float(mark["close_price"])
        ewma5 = float(runtime["ewma5_equilibrium"])
        trend = float(runtime["ewmac16_64_trend"])
        sigma = float(runtime["annual_percentage_sigma"])
        multiplier = float(runtime["vol_multiplier_m"])
        sigma_price = float(runtime["previous_daily_raw_close"]) * sigma / 16.0
        raw_forecast = ewma5 - decision_price
        risk_before_veto = raw_forecast / sigma_price
        risk_after_veto = 0.0 if risk_before_veto * trend < 0.0 else risk_before_veto
        capped_forecast = _clamp(risk_after_veto * multiplier * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)
        base_position = CAPITAL_ACCOUNT_VALUE * ANNUAL_TARGET_RISK / (decision_price * CONTRACT_POINT_VALUE * sigma)
        desired_position = _round_half_away_from_zero(base_position * capped_forecast / FORECAST_TO_POSITION_DIVISOR)
        starting_position = current_position
        position_change = desired_position - starting_position
        side = "BUY" if position_change > 0 else "SELL" if position_change < 0 else "NONE"
        adjacent_target = starting_position + (1 if position_change > 0 else -1 if position_change < 0 else 0)
        cap_bound_market_case = _is_cap_bound_market_order_case(
            position_change=position_change,
            adjacent_target=adjacent_target,
            base_position=base_position,
            trend=trend,
        )
        market_order_required = abs(position_change) > 1 or cap_bound_market_case
        market_order_reason = (
            CAP_BOUND_MARKET_ORDER_TRIGGER_SOURCE_CONDITION
            if cap_bound_market_case
            else MARKET_ORDER_TRIGGER_SOURCE_CONDITION
        )
        live_order_roll_dates = _live_order_roll_boundary_dates(decision, fill, mark, side, roll_dates)
        if live_order_roll_dates and _roll_boundary_no_new_order_suppression_applies(
            decision=decision,
            fill=fill,
            mark=mark,
            mechanics={
                "starting_position_contracts": starting_position,
                "desired_position_contracts": desired_position,
                "position_change_contracts": position_change,
                "order_side": side,
            },
            roll_boundary_dates=live_order_roll_dates,
        ):
            existing_gross = (
                0.0
                if last_mark_price is None
                else starting_position * (mark_price - last_mark_price) * CONTRACT_POINT_VALUE
            )
            row_gross = existing_gross
            row_net = row_gross
            cumulative_gross += row_gross
            cumulative_net = cumulative_gross - cumulative_commission - cumulative_spread
            current_position = starting_position
            last_mark_price = mark_price
            same_session = decision["session_id"] == fill["session_id"] == mark["session_id"]
            out["runtime"].append(_hash_row({
                "row_index": index,
                "runtime_evidence_row_hash": runtime["row_hash"],
                "ewma5": ewma5,
                "trend": trend,
                "sigma": sigma,
                "vqm_multiplier_m": multiplier,
                "row_status": "LOCAL_RUNTIME_NUMERIC_ROW_EMITTED_NOT_RESULT",
            }))
            out["forecast"].append(_hash_row({
                "row_index": index,
                "decision_timestamp_utc": decision["completed_timestamp_utc"],
                "raw_forecast": raw_forecast,
                "risk_adjusted_forecast": risk_after_veto,
                "capped_forecast": capped_forecast,
                "row_status": "LOCAL_FORECAST_ROW_EMITTED_NOT_RESULT",
            }))
            out["position"].append(_hash_row({
                "row_index": index,
                "starting_position_contracts": starting_position,
                "desired_position_contracts": starting_position,
                "position_change_contracts": 0,
                "base_position_contracts": base_position,
                "row_status": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS,
            }))
            out["order"].append(_hash_row({
                "row_index": index,
                "order_side": "NONE",
                "order_quantity": 0,
                "adjacent_target_position": starting_position,
                "formula_limit_price": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION,
                "limit_order_price": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION,
                "row_status": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS,
            }))
            out["market"].append(_hash_row({
                "row_index": index,
                "market_order_required": False,
                "market_order_rows_emitted": False,
                "market_fallback_status": "NOT_REQUIRED_NO_ORDER_POSITION_UNCHANGED",
                "engineering_convention_label": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION,
                "row_status": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS,
            }))
            out["transition"].append(_hash_row({
                "row_index": index,
                "starting_position_contracts": starting_position,
                "ending_position_contracts": current_position,
                "working_state_before": "NO_OPEN_WORKING_ORDER_CARRIED",
                "working_state_after": "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION",
                "same_session": same_session,
                "row_status": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS,
            }))
            out["fill"].append(_hash_row({
                "row_index": index,
                "fill_executed": False,
                "fill_rule": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_CONVENTION,
                "fill_candidate_close": fill_close,
                "fill_price": 0.0,
                "fill_quantity": 0,
                "position_after_fill": current_position,
                "row_status": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS,
            }))
            out["cost"].append(_hash_row({
                "row_index": index,
                "cost_policy_id": cost["cost_policy_id"],
                "commission_amount": 0.0,
                "spread_cost_amount": 0.0,
                "total_cost_amount": 0.0,
                "currency": "USD",
                "row_status": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS,
            }))
            out["pnl"].append(_hash_row({
                "row_index": index,
                "valuation_mark_timestamp_utc": mark["completed_timestamp_utc"],
                "valuation_mark_close_price": mark_price,
                "valuation_convention_label": VALUATION_CONVENTION_LABEL,
                "existing_position_gross_pnl": existing_gross,
                "fill_gross_pnl": 0.0,
                "row_gross_pnl_amount": row_gross,
                "row_net_pnl_amount": row_net,
                "cumulative_gross_pnl_amount": cumulative_gross,
                "cumulative_commission_amount": cumulative_commission,
                "cumulative_spread_amount": cumulative_spread,
                "cumulative_net_pnl_amount": cumulative_net,
                "ending_position_contracts": current_position,
                "result_status": RESULT_STATUS,
                "backtest_status": BACKTEST_STATUS,
                "pnl_evaluation_status": PNL_EVALUATION_STATUS,
                "source_faithful_evidence_claimed": False,
                "row_status": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS,
            }))
            out["validation"].append(_hash_row({
                "row_index": index,
                "result_status": RESULT_STATUS,
                "backtest_status": BACKTEST_STATUS,
                "source_faithful_evidence_claimed": False,
                "non_authorizations": NON_AUTHORIZATIONS,
                "row_status": ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS,
            }))
            continue
        if live_order_roll_dates:
            formula_limit = (
                _formula_limit(adjacent_target, base_position, ewma5, sigma_price, multiplier, trend)
                if not market_order_required and side != "NONE"
                else None
            )
            limit_price = _round_limit(formula_limit, side) if formula_limit is not None and side != "NONE" else 0.0
            fill_executed = _limit_fill(side, fill_close, limit_price) if formula_limit is not None and side != "NONE" else False
            out["fail_closed"].append(_hash_row({
                "row_index": index,
                "decision_timestamp_utc": decision["completed_timestamp_utc"],
                "raw_symbol": decision["raw_symbol"],
                "starting_position_contracts": starting_position,
                "desired_position_contracts": desired_position,
                "position_change_contracts": position_change,
                "order_side": side,
                "adjacent_target_position": adjacent_target,
                "trend": trend,
                "market_order_required": market_order_required,
                "market_order_rows_emitted": False,
                "market_order_reason": market_order_reason,
                "market_fill_metadata_rows_emitted": False,
                "market_fill_price_provenance": "FAIL_CLOSED_LIVE_ORDER_ON_UNRESOLVED_ROLL_BOUNDARY_DATE",
                "market_fill_price": 0.0,
                "commission_per_contract": ACCEPTED_COMMISSION_PER_CONTRACT,
                "commission_amount": 0.0,
                "market_spread_cost_status": "FAIL_CLOSED_LIVE_ORDER_ON_UNRESOLVED_ROLL_BOUNDARY_DATE",
                "secondary_fail_closed_reason": ",".join(sorted(live_order_roll_dates)),
                "formula_limit_price": formula_limit if formula_limit is not None else "NOT_APPLICABLE_MARKET_ORDER_OR_UNRESOLVED_FORMULA",
                "limit_order_price": limit_price if formula_limit is not None else "NOT_APPLICABLE_MARKET_ORDER_OR_UNRESOLVED_FORMULA",
                "fill_candidate_timestamp_utc": fill["completed_timestamp_utc"],
                "fill_candidate_close": fill_close,
                "fill_executed": fill_executed,
                "same_session": decision["session_id"] == fill["session_id"] == mark["session_id"],
                "fail_closed_reason": FAIL_CLOSED_LIVE_ORDER_ROLL_BOUNDARY_STATUS,
                "result_status": RESULT_STATUS,
                "backtest_status": BACKTEST_STATUS,
                "source_faithful_evidence_claimed": False,
                "row_status": "LOCAL_2023_TEST_LIVE_ORDER_ROLL_BOUNDARY_FAIL_CLOSED_NOT_RESULT",
            }))
            break
        if market_order_required and not _market_spread_evidence_is_bound(index):
            fail_closed_reason = (
                FAIL_CLOSED_CAP_BOUND_MARKET_CONTINUATION_STATUS
                if cap_bound_market_case
                else FAIL_CLOSED_UNSUPPORTED_MARKET_CONTINUATION_STATUS
            )
            out["fail_closed"].append(_hash_row({
                "row_index": index,
                "decision_timestamp_utc": decision["completed_timestamp_utc"],
                "raw_symbol": decision["raw_symbol"],
                "starting_position_contracts": starting_position,
                "desired_position_contracts": desired_position,
                "position_change_contracts": position_change,
                "order_side": side,
                "adjacent_target_position": adjacent_target,
                "trend": trend,
                "market_order_required": True,
                "market_order_rows_emitted": False,
                "market_order_reason": market_order_reason,
                "market_fill_metadata_rows_emitted": False,
                "market_fill_price_provenance": "FAIL_CLOSED_NO_BOUND_MARKET_FILL_METADATA_FOR_CONTINUATION",
                "market_fill_price": 0.0,
                "commission_per_contract": ACCEPTED_COMMISSION_PER_CONTRACT,
                "commission_amount": 0.0,
                "market_spread_cost_status": "FAIL_CLOSED_BOUNDED_TBBO_SPREAD_EVIDENCE_REQUIRED_FOR_MARKET_ORDER",
                "secondary_fail_closed_reason": "MARKET_ORDER_CONTINUATION_REQUIRES_SEPARATE_BOUNDED_SPREAD_EVIDENCE",
                "fill_candidate_timestamp_utc": fill["completed_timestamp_utc"],
                "fill_candidate_close": fill_close,
                "fill_executed": False,
                "same_session": decision["session_id"] == fill["session_id"] == mark["session_id"],
                "fail_closed_reason": fail_closed_reason,
                "result_status": RESULT_STATUS,
                "backtest_status": BACKTEST_STATUS,
                "source_faithful_evidence_claimed": False,
                "row_status": "LOCAL_2023_TEST_MARKET_ORDER_CONTINUATION_FAIL_CLOSED_NOT_RESULT",
            }))
            break
        if market_order_required:
            fill_quantity = abs(position_change)
            try:
                market_spread_evidence = _load_market_spread_evidence(index, side, fill["completed_timestamp_utc"])
            except CarverBlocked:
                out["fail_closed"].append(_hash_row({
                    "row_index": index,
                    "decision_timestamp_utc": decision["completed_timestamp_utc"],
                    "raw_symbol": decision["raw_symbol"],
                    "starting_position_contracts": starting_position,
                    "desired_position_contracts": desired_position,
                    "position_change_contracts": position_change,
                    "order_side": side,
                    "adjacent_target_position": adjacent_target,
                    "trend": trend,
                    "market_order_required": True,
                    "market_order_rows_emitted": False,
                    "market_order_reason": market_order_reason,
                    "market_fill_metadata_rows_emitted": False,
                    "market_fill_price_provenance": "FAIL_CLOSED_STALE_OR_SIDE_MISMATCH_MARKET_SPREAD_EVIDENCE",
                    "market_fill_price": 0.0,
                    "commission_per_contract": ACCEPTED_COMMISSION_PER_CONTRACT,
                    "commission_amount": 0.0,
                    "market_spread_cost_status": "FAIL_CLOSED_STALE_OR_SIDE_MISMATCH_MARKET_SPREAD_EVIDENCE",
                    "secondary_fail_closed_reason": "BOUND_MARKET_SPREAD_EVIDENCE_DOES_NOT_MATCH_CURRENT_POSITION_PATH",
                    "fill_candidate_timestamp_utc": fill["completed_timestamp_utc"],
                    "fill_candidate_close": fill_close,
                    "fill_executed": False,
                    "same_session": decision["session_id"] == fill["session_id"] == mark["session_id"],
                    "fail_closed_reason": FAIL_CLOSED_STALE_MARKET_SPREAD_EVIDENCE_STATUS,
                    "result_status": RESULT_STATUS,
                    "backtest_status": BACKTEST_STATUS,
                    "source_faithful_evidence_claimed": False,
                    "row_status": "LOCAL_2023_TEST_STALE_MARKET_SPREAD_EVIDENCE_FAIL_CLOSED_NOT_RESULT",
                }))
                break
            market_fill_price = _market_fill_price_from_evidence(market_spread_evidence, side)
            commission = ACCEPTED_COMMISSION_PER_CONTRACT * fill_quantity
            spread = 0.0
            total_cost = commission + spread
            same_session = decision["session_id"] == fill["session_id"] == mark["session_id"]
            session_end_market_case = _is_session_end_market_case(
                decision=decision,
                fill=fill,
                mark=mark,
                market_spread_evidence=market_spread_evidence,
            )
            session_open_market_reset_case = _is_session_open_market_reset_case(
                decision=decision,
                fill=fill,
                mark=mark,
                market_spread_evidence=market_spread_evidence,
            )
            row304_engineering_session_open_case = _is_row304_engineering_session_open_market_reset_case(
                row_index=index,
                decision=decision,
                fill=fill,
                mark=mark,
                position_change=position_change,
                side=side,
                market_spread_evidence=market_spread_evidence,
            )
            row391_session_end_case = _is_row391_session_end_market_case(
                row_index=index,
                decision=decision,
                fill=fill,
                mark=mark,
                position_change=position_change,
                side=side,
                market_spread_evidence=market_spread_evidence,
            )
            row1113_valuation_gap_case = _is_row1113_session_end_market_valuation_gap_case(
                row_index=index,
                decision=decision,
                fill=fill,
                mark=mark,
                position_change=position_change,
                side=side,
                market_spread_evidence=market_spread_evidence,
            )
            if (
                not same_session
                and not session_end_market_case
                and not session_open_market_reset_case
                and not row1113_valuation_gap_case
            ):
                out["fail_closed"].append(_hash_row({
                    "row_index": index,
                    "decision_timestamp_utc": decision["completed_timestamp_utc"],
                    "raw_symbol": decision["raw_symbol"],
                    "starting_position_contracts": starting_position,
                    "desired_position_contracts": desired_position,
                    "position_change_contracts": position_change,
                    "order_side": side,
                    "adjacent_target_position": adjacent_target,
                    "trend": trend,
                "market_order_required": True,
                "market_order_rows_emitted": False,
                "market_order_reason": market_order_reason,
                    "market_fill_metadata_rows_emitted": False,
                    "market_fill_price_provenance": "FAIL_CLOSED_MARKET_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP",
                    "market_fill_price": 0.0,
                    "commission_per_contract": ACCEPTED_COMMISSION_PER_CONTRACT,
                    "commission_amount": 0.0,
                    "market_spread_cost_status": "FAIL_CLOSED_MARKET_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP",
                    "secondary_fail_closed_reason": SECONDARY_SESSION_EOD_BLOCKER_STATUS,
                    "fill_candidate_timestamp_utc": fill["completed_timestamp_utc"],
                    "fill_candidate_close": fill_close,
                    "fill_executed": False,
                    "same_session": same_session,
                    "fail_closed_reason": SECONDARY_SESSION_EOD_BLOCKER_STATUS,
                    "result_status": RESULT_STATUS,
                    "backtest_status": BACKTEST_STATUS,
                    "source_faithful_evidence_claimed": False,
                    "row_status": "LOCAL_2023_TEST_MARKET_ORDER_SESSION_EOD_FAIL_CLOSED_NOT_RESULT",
                }))
                break
            execution_same_session = decision["session_id"] == fill["session_id"]
            market_order_row_status = (
                ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_ROW_STATUS
                if session_open_market_reset_case
                else "LOCAL_MARKET_ORDER_ROW_EMITTED_NOT_RESULT"
            )
            engineering_convention_label = (
                ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_CONVENTION
                if session_open_market_reset_case
                else ROW1113_SESSION_END_MARKET_VALUATION_GAP_CONVENTION
                if row1113_valuation_gap_case
                else "NOT_APPLICABLE"
            )
            if side == "BUY" and market_fill_price != float(market_spread_evidence["ask_px_00"]):
                raise CarverBlocked("S27 v2 2023 TEST buy market no-double-counting requires selected TBBO ask fill")
            if side == "SELL" and market_fill_price != float(market_spread_evidence["bid_px_00"]):
                raise CarverBlocked("S27 v2 2023 TEST sell market no-double-counting requires selected TBBO bid fill")
            out["market_order"].append(_hash_row({
                "row_index": index,
                "decision_timestamp_utc": decision["completed_timestamp_utc"],
                "raw_symbol": decision["raw_symbol"],
                "current_position_before_order": starting_position,
                "target_position_after_fill": desired_position,
                "order_side": side,
                "order_quantity": fill_quantity,
                "trigger_source_condition": market_order_reason,
                "market_order_rows_emitted": True,
                "engineering_convention_label": engineering_convention_label,
                "order_status": market_order_row_status,
                "row_status": market_order_row_status,
            }))
            out["market_fill_metadata"].append(_hash_row({
                "row_index": index,
                "fill_timestamp_utc": fill["completed_timestamp_utc"],
                "raw_symbol": fill["raw_symbol"],
                "order_side": side,
                "fill_quantity": fill_quantity,
                "fill_price": market_fill_price,
                "fill_price_provenance": MARKET_FILL_PRICE_PROVENANCE_BY_SIDE[side],
                "fill_source_row_hash": fill["source_row_hash"],
                "same_session": execution_same_session,
                "roll_boundary_status": "NO_ROLL_BOUNDARY_SAME_RAW_SYMBOL",
                "working_state_before": "EMPTY_INITIAL_WORKING_STATE",
                "position_after_fill": desired_position,
                "commission_per_contract": ACCEPTED_COMMISSION_PER_CONTRACT,
                "commission_amount": commission,
                "market_spread_cost_status": MARKET_SPREAD_COST_STATUS_BY_SIDE[side],
                "pnl_emission_status": "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
                "row_status": "LOCAL_MARKET_FILL_METADATA_ROW_EMITTED_NOT_RESULT",
            }))
            out["cost"].append(_hash_row({
                "row_index": index,
                "cost_policy_id": cost["cost_policy_id"],
                "order_cost_type": f"MARKET_ORDER_{side}_{'ASK' if side == 'BUY' else 'BID'}_FILL_ACTUAL_COST_NOT_PNL",
                "commission_amount": commission,
                "spread_cost_amount": spread,
                "total_cost_amount": total_cost,
                "currency": "USD",
                "market_cost_accounting_convention": MARKET_COST_ACCOUNTING_CONVENTION_BY_SIDE[side],
                "spread_cost_reason": f"NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_{'ASK' if side == 'BUY' else 'BID'}",
                "tbbo_quote_ts_event": market_spread_evidence["selected_quote_ts_event"],
                "tbbo_bid_px": market_spread_evidence["bid_px_00"],
                "tbbo_ask_px": market_spread_evidence["ask_px_00"],
                "tbbo_full_spread_points": market_spread_evidence["spread_points"],
                "tbbo_full_spread_value_per_contract": market_spread_evidence["spread_cost_usd_per_contract"],
                "tbbo_selected_spread_row_hash": market_spread_evidence["row_hash"],
                "tbbo_selected_spread_ledger_sha256": market_spread_evidence["selected_spread_ledger_sha256"],
                "row_status": "LOCAL_MARKET_ORDER_ACTUAL_COST_ROW_EMITTED_NOT_PNL_NOT_RESULT",
            }))
            signed_fill = fill_quantity if side == "BUY" else -fill_quantity
            current_position = desired_position
            existing_gross = 0.0 if last_mark_price is None else starting_position * (mark_price - last_mark_price) * CONTRACT_POINT_VALUE
            fill_gross = signed_fill * (mark_price - market_fill_price) * CONTRACT_POINT_VALUE
            row_gross = existing_gross + fill_gross
            row_net = row_gross - total_cost
            cumulative_gross += row_gross
            cumulative_commission += commission
            cumulative_spread += spread
            cumulative_net = cumulative_gross - cumulative_commission - cumulative_spread
            last_mark_price = mark_price
            out["runtime"].append(_hash_row({
                "row_index": index,
                "runtime_evidence_row_hash": runtime["row_hash"],
                "ewma5": ewma5,
                "trend": trend,
                "sigma": sigma,
                "vqm_multiplier_m": multiplier,
                "row_status": "LOCAL_RUNTIME_NUMERIC_ROW_EMITTED_NOT_RESULT",
            }))
            out["forecast"].append(_hash_row({
                "row_index": index,
                "decision_timestamp_utc": decision["completed_timestamp_utc"],
                "raw_forecast": raw_forecast,
                "risk_adjusted_forecast": risk_after_veto,
                "capped_forecast": capped_forecast,
                "row_status": "LOCAL_FORECAST_ROW_EMITTED_NOT_RESULT",
            }))
            out["position"].append(_hash_row({
                "row_index": index,
                "starting_position_contracts": starting_position,
                "desired_position_contracts": desired_position,
                "position_change_contracts": position_change,
                "base_position_contracts": base_position,
                "row_status": "LOCAL_POSITION_ROW_EMITTED_NOT_RESULT",
            }))
            out["order"].append(_hash_row({
                "row_index": index,
                "order_side": side,
                "order_quantity": fill_quantity,
                "adjacent_target_position": adjacent_target,
                "formula_limit_price": (
                    CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL
                    if cap_bound_market_case
                    else "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
                ),
                "limit_order_price": (
                    CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL
                    if cap_bound_market_case
                    else "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
                ),
                "row_status": "LOCAL_MARKET_ORDER_PLAN_ROW_EMITTED_NOT_LIMIT_ORDER_NOT_RESULT",
            }))
            out["market"].append(_hash_row({
                "row_index": index,
                "market_order_required": True,
                "market_order_rows_emitted": True,
                "market_fallback_status": "LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP",
                "engineering_convention_label": engineering_convention_label,
                "row_status": "LOCAL_MARKET_ORDER_EXECUTION_STATUS_ROW_EMITTED_NOT_RESULT",
            }))
            out["transition"].append(_hash_row({
                "row_index": index,
                "starting_position_contracts": starting_position,
                "ending_position_contracts": current_position,
                "working_state_before": "EMPTY_INITIAL_WORKING_STATE",
                "working_state_after": "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION",
                "same_session": execution_same_session,
                "row_status": "LOCAL_MARKET_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT",
            }))
            out["fill"].append(_hash_row({
                "row_index": index,
                "fill_executed": True,
                "fill_rule": MARKET_FILL_PRICE_PROVENANCE_BY_SIDE[side],
                "fill_candidate_close": fill_close,
                "fill_price": market_fill_price,
                "fill_quantity": fill_quantity,
                "position_after_fill": current_position,
                "row_status": "LOCAL_MARKET_ORDER_FILL_ROW_EMITTED_NOT_RESULT",
            }))
            out["pnl"].append(_hash_row({
                "row_index": index,
                "valuation_mark_timestamp_utc": mark["completed_timestamp_utc"],
                "valuation_mark_close_price": mark_price,
                "valuation_convention_label": VALUATION_CONVENTION_LABEL,
                "existing_position_gross_pnl": existing_gross,
                "fill_gross_pnl": fill_gross,
                "row_gross_pnl_amount": row_gross,
                "row_net_pnl_amount": row_net,
                "cumulative_gross_pnl_amount": cumulative_gross,
                "cumulative_commission_amount": cumulative_commission,
                "cumulative_spread_amount": cumulative_spread,
                "cumulative_net_pnl_amount": cumulative_net,
                "ending_position_contracts": current_position,
                "result_status": RESULT_STATUS,
                "backtest_status": BACKTEST_STATUS,
                "pnl_evaluation_status": PNL_EVALUATION_STATUS,
                "source_faithful_evidence_claimed": False,
                "row_status": "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
            }))
            out["validation"].append(_hash_row({
                "row_index": index,
                "result_status": RESULT_STATUS,
                "backtest_status": BACKTEST_STATUS,
                "source_faithful_evidence_claimed": False,
                "non_authorizations": NON_AUTHORIZATIONS,
                "row_status": "LOCAL_MARKET_ORDER_PNL_VALIDATION_ROW_EMITTED_NOT_RESULT",
            }))
            continue
        formula_limit = _formula_limit(adjacent_target, base_position, ewma5, sigma_price, multiplier, trend) if side != "NONE" else 0.0
        if formula_limit is None:
            formula_status = _adjacent_limit_formula_fail_status(adjacent_target, base_position)
            out["fail_closed"].append(_hash_row({"row_index": index, "decision_timestamp_utc": decision["completed_timestamp_utc"], "raw_symbol": decision["raw_symbol"], "starting_position_contracts": starting_position, "desired_position_contracts": desired_position, "position_change_contracts": position_change, "order_side": side, "adjacent_target_position": adjacent_target, "trend": trend, "fill_executed": False, "same_session": True, "fail_closed_reason": formula_status, "result_status": RESULT_STATUS, "backtest_status": BACKTEST_STATUS, "source_faithful_evidence_claimed": False, "row_status": "LOCAL_2023_TEST_FAIL_CLOSED_BLOCKER_ROW_EMITTED_NOT_RESULT"}))
            break
        limit_price = _round_limit(formula_limit, side) if side != "NONE" else 0.0
        fill_executed = _limit_fill(side, fill_close, limit_price)
        same_session = decision["session_id"] == fill["session_id"] == mark["session_id"]
        session_open_limit_fill_case = _is_session_open_adjacent_limit_fill_case(
            decision=decision,
            fill=fill,
            mark=mark,
            position_change=position_change,
            side=side,
            fill_executed=fill_executed,
        )
        row892_session_end_limit_fill_case = _is_row892_session_end_adjacent_limit_fill_case(
            row_index=index,
            decision=decision,
            fill=fill,
            mark=mark,
            position_change=position_change,
            side=side,
            fill_executed=fill_executed,
            fill_close=fill_close,
            formula_limit=formula_limit,
            limit_price=limit_price,
        )
        row1355_session_end_limit_valuation_gap_case = _is_row1355_session_end_adjacent_limit_valuation_gap_case(
            row_index=index,
            decision=decision,
            fill=fill,
            mark=mark,
            position_change=position_change,
            side=side,
            fill_executed=fill_executed,
            fill_close=fill_close,
            formula_limit=formula_limit,
            limit_price=limit_price,
        )
        if (
            fill_executed
            and not same_session
            and not session_open_limit_fill_case
            and not row892_session_end_limit_fill_case
            and not row1355_session_end_limit_valuation_gap_case
        ):
            out["fail_closed"].append(_hash_row({"row_index": index, "decision_timestamp_utc": decision["completed_timestamp_utc"], "raw_symbol": decision["raw_symbol"], "starting_position_contracts": starting_position, "desired_position_contracts": desired_position, "position_change_contracts": position_change, "order_side": side, "adjacent_target_position": adjacent_target, "trend": trend, "formula_limit_price": formula_limit, "limit_order_price": limit_price, "fill_candidate_timestamp_utc": fill["completed_timestamp_utc"], "fill_candidate_close": fill_close, "fill_executed": True, "same_session": False, "fail_closed_reason": SECONDARY_SESSION_EOD_BLOCKER_STATUS, "result_status": RESULT_STATUS, "backtest_status": BACKTEST_STATUS, "source_faithful_evidence_claimed": False, "row_status": "LOCAL_2023_TEST_FAIL_CLOSED_BLOCKER_ROW_EMITTED_NOT_RESULT"}))
            break
        fill_quantity = abs(position_change) if fill_executed else 0
        signed_fill = fill_quantity if side == "BUY" else -fill_quantity if side == "SELL" else 0
        current_position = starting_position + signed_fill
        existing_gross = 0.0 if last_mark_price is None else starting_position * (mark_price - last_mark_price) * CONTRACT_POINT_VALUE
        fill_gross = signed_fill * (mark_price - limit_price) * CONTRACT_POINT_VALUE if fill_executed else 0.0
        row_gross = existing_gross + fill_gross
        commission = ACCEPTED_COMMISSION_PER_CONTRACT * abs(fill_quantity)
        spread = 0.0
        row_net = row_gross - commission
        cumulative_gross += row_gross
        cumulative_commission += commission
        cumulative_spread += spread
        cumulative_net = cumulative_gross - cumulative_commission - cumulative_spread
        last_mark_price = mark_price
        working_after = "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION" if side == "NONE" or fill_executed else "UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE"
        market_fallback_status = "NOT_REQUIRED_NO_ORDER_POSITION_UNCHANGED" if side == "NONE" else "NOT_REQUIRED_LIMIT_ORDER_FILLED" if fill_executed else "FAIL_CLOSED_UNFILLED_LIMIT_ORDER_MARKET_FALLBACK_NOT_AUTHORIZED"
        engineering_convention_label = (
            ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_CONVENTION
            if session_open_limit_fill_case
            else ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_CONVENTION
            if row892_session_end_limit_fill_case
            else ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_CONVENTION
            if row1355_session_end_limit_valuation_gap_case
            else "NOT_APPLICABLE"
        )
        limit_fill_rule = (
            ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_RULE
            if session_open_limit_fill_case
            else ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_RULE
            if row892_session_end_limit_fill_case
            else ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_RULE
            if row1355_session_end_limit_valuation_gap_case
            else "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL"
        )
        limit_row_status = (
            ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_ROW_STATUS
            if session_open_limit_fill_case
            else ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_ROW_STATUS
            if row892_session_end_limit_fill_case
            else ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS
            if row1355_session_end_limit_valuation_gap_case
            else "LOCAL_LIMIT_ORDER_ROW_EMITTED_NOT_RESULT"
        )
        transition_row_status = (
            ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_ROW_STATUS
            if session_open_limit_fill_case
            else ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_ROW_STATUS
            if row892_session_end_limit_fill_case
            else ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS
            if row1355_session_end_limit_valuation_gap_case
            else "LOCAL_WORKING_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT"
        )
        fill_row_status = (
            ROW436_ENGINEERING_SESSION_OPEN_LIMIT_FILL_ROW_STATUS
            if session_open_limit_fill_case
            else ROW892_ENGINEERING_SESSION_END_LIMIT_FILL_ROW_STATUS
            if row892_session_end_limit_fill_case
            else ROW1355_ENGINEERING_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS
            if row1355_session_end_limit_valuation_gap_case
            else "LOCAL_FILL_ROW_EMITTED_NOT_RESULT"
        )
        out["runtime"].append(_hash_row({"row_index": index, "runtime_evidence_row_hash": runtime["row_hash"], "ewma5": ewma5, "trend": trend, "sigma": sigma, "vqm_multiplier_m": multiplier, "row_status": "LOCAL_RUNTIME_NUMERIC_ROW_EMITTED_NOT_RESULT"}))
        out["forecast"].append(_hash_row({"row_index": index, "decision_timestamp_utc": decision["completed_timestamp_utc"], "raw_forecast": raw_forecast, "risk_adjusted_forecast": risk_after_veto, "capped_forecast": capped_forecast, "row_status": "LOCAL_FORECAST_ROW_EMITTED_NOT_RESULT"}))
        out["position"].append(_hash_row({"row_index": index, "starting_position_contracts": starting_position, "desired_position_contracts": desired_position, "position_change_contracts": position_change, "base_position_contracts": base_position, "row_status": "LOCAL_POSITION_ROW_EMITTED_NOT_RESULT"}))
        out["order"].append(_hash_row({"row_index": index, "order_side": side, "order_quantity": abs(position_change), "adjacent_target_position": adjacent_target, "formula_limit_price": formula_limit, "limit_order_price": limit_price, "row_status": limit_row_status}))
        out["market"].append(_hash_row({"row_index": index, "market_order_required": False, "market_order_rows_emitted": False, "market_fallback_status": market_fallback_status, "engineering_convention_label": engineering_convention_label, "row_status": "LOCAL_NO_MARKET_ORDER_METADATA_ROW_EMITTED_NOT_RESULT"}))
        out["transition"].append(_hash_row({"row_index": index, "starting_position_contracts": starting_position, "ending_position_contracts": current_position, "working_state_before": "EMPTY" if index == 1 else "NO_OPEN_WORKING_ORDER_CARRIED", "working_state_after": working_after, "same_session": same_session, "row_status": transition_row_status}))
        out["fill"].append(_hash_row({"row_index": index, "fill_executed": fill_executed, "fill_rule": limit_fill_rule, "fill_candidate_close": fill_close, "fill_price": limit_price if fill_executed else 0.0, "fill_quantity": fill_quantity, "position_after_fill": current_position, "row_status": fill_row_status}))
        out["cost"].append(_hash_row({"row_index": index, "cost_policy_id": cost["cost_policy_id"], "commission_amount": commission, "spread_cost_amount": spread, "total_cost_amount": commission + spread, "currency": "USD", "row_status": "LOCAL_COST_ROW_EMITTED_NOT_RESULT"}))
        out["pnl"].append(_hash_row({"row_index": index, "valuation_mark_timestamp_utc": mark["completed_timestamp_utc"], "valuation_mark_close_price": mark_price, "valuation_convention_label": VALUATION_CONVENTION_LABEL, "existing_position_gross_pnl": existing_gross, "fill_gross_pnl": fill_gross, "row_gross_pnl_amount": row_gross, "row_net_pnl_amount": row_net, "cumulative_gross_pnl_amount": cumulative_gross, "cumulative_commission_amount": cumulative_commission, "cumulative_spread_amount": cumulative_spread, "cumulative_net_pnl_amount": cumulative_net, "ending_position_contracts": current_position, "result_status": RESULT_STATUS, "backtest_status": BACKTEST_STATUS, "pnl_evaluation_status": PNL_EVALUATION_STATUS, "source_faithful_evidence_claimed": False, "row_status": "LOCAL_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT"}))
        out["validation"].append(_hash_row({"row_index": index, "result_status": RESULT_STATUS, "backtest_status": BACKTEST_STATUS, "source_faithful_evidence_claimed": False, "non_authorizations": NON_AUTHORIZATIONS, "row_status": "LOCAL_VALIDATION_ROW_EMITTED_NOT_RESULT"}))
    if len(out["fail_closed"]) > 1:
        raise CarverBlocked("S27 v2 2023 TEST must emit at most one fail-closed blocker row")
    return out


def _validate_supported_rows_with_machine_freeze(
    pack_rows: dict[str, list[dict[str, str]]],
    computed: dict[str, list[dict[str, Any]]],
) -> None:
    supported_count = len(computed["pnl"])
    supported_pack = {
        key: value[:supported_count] if key in {"runtime_evidence_ledger.csv", "hourly_decision_completed_bar.csv", "hourly_fill_completed_bar.csv", "valuation_mark_completed_bar.csv"} else value
        for key, value in pack_rows.items()
    }
    supported_computed = {
        key: value[:supported_count] for key, value in computed.items() if key != "fail_closed"
    }
    validate_pretest_machine_freeze_rows(supported_pack, supported_computed)


def _write_artifacts(output_root: Path, pack_path: Path, manifest: dict[str, Any], computed: dict[str, list[dict[str, Any]]]) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    files = {
        "runtime_history_ledger.csv": computed["runtime"],
        "forecast_replay_ledger.csv": computed["forecast"],
        "desired_position_ledger.csv": computed["position"],
        "limit_order_ledger.csv": computed["order"],
        "no_market_order_ledger.csv": computed["market"],
        "market_order_ledger.csv": computed["market_order"],
        "working_order_transition_ledger.csv": computed["transition"],
        "fill_ledger.csv": computed["fill"],
        "market_fill_metadata_ledger.csv": computed["market_fill_metadata"],
        "cost_ledger.csv": computed["cost"],
        "pnl_ledger.csv": computed["pnl"],
        "validation_ledger.csv": computed["validation"],
        "fail_closed_ledger.csv": computed["fail_closed"],
    }
    for name, rows in files.items():
        _write_csv(output_root / name, rows, fieldnames=RUN_LEDGER_FIELDNAMES[name])
    run_manifest = {
        "artifact": "S27_V2_2023_TEST_MECHANICAL_RUN_MANIFEST",
        "status": RUN_STATUS,
        "authorization": AUTHORIZATION,
        "input_pack_path": str(pack_path),
        "input_manifest_hash": _sha256(pack_path / DEFAULT_MANIFEST_NAME),
        "candidate_row_count": int(manifest["candidate_row_count"]),
        "supported_mechanical_row_count": len(computed["pnl"]),
        "fail_closed_row_index": int(computed["fail_closed"][0]["row_index"]) if computed["fail_closed"] else 0,
        "fail_closed_reason": (
            computed["fail_closed"][0]["fail_closed_reason"]
            if computed["fail_closed"]
            else NO_FAIL_CLOSED_BLOCKER_PACK_EXHAUSTED_STATUS
        ),
        "artifact_files": tuple(files),
        "source_continuous_daily_ledger": manifest["source_continuous_daily_ledger"],
        "source_hourly_ledger": manifest["source_hourly_ledger"],
        "non_authorizations": NON_AUTHORIZATIONS,
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
    }
    _write_json(output_root / "run_manifest.json", run_manifest)
    evidence_manifest = {
        "artifact": "S27_V2_2023_TEST_EVIDENCE_MANIFEST_METADATA",
        "status": "LOCAL_2023_TEST_EVIDENCE_MANIFEST_METADATA_FAIL_CLOSED_NOT_RESULT",
        "run_manifest_hash": _sha256(output_root / "run_manifest.json"),
        "ledger_hashes": {name: _sha256(output_root / name) for name in files},
        "input_manifest_hash": _sha256(pack_path / DEFAULT_MANIFEST_NAME),
    }
    _write_json(output_root / "evidence_manifest.json", evidence_manifest)
    trusted_bundle = {
        "artifact": "S27_V2_2023_TEST_TRUSTED_BUNDLE_METADATA",
        "status": "LOCAL_2023_TEST_TRUSTED_BUNDLE_METADATA_FAIL_CLOSED_NOT_RESULT_NOT_PROMOTION",
        "run_manifest_hash": _sha256(output_root / "run_manifest.json"),
        "evidence_manifest_hash": _sha256(output_root / "evidence_manifest.json"),
        "final_supported_pnl_row_hash": computed["pnl"][-1]["row_hash"] if computed["pnl"] else "NO_SUPPORTED_PNL_ROWS_FAIL_CLOSED_AT_FIRST_TEST_ROW",
        "fail_closed_row_hash": (
            computed["fail_closed"][0]["row_hash"]
            if computed["fail_closed"]
            else "NO_FAIL_CLOSED_ROW_DECLARED_PACK_EXHAUSTED_NOT_RESULT"
        ),
        "result_status": RESULT_STATUS,
        "source_faithful_evidence_claimed": False,
    }
    _write_json(output_root / "trusted_bundle.json", trusted_bundle)


def _active_contract_key(day: str, rolls: list[dict[str, str]]) -> str:
    key = "ZNH3_2023"
    for row in rolls:
        if day >= row["roll_transition_date"]:
            key = row["new_contract_key"]
    return key


def _point_in_time_continuous_series(
    continuous: list[dict[str, Any]],
    rolls: list[dict[str, str]],
    cutoff_date: str,
) -> list[dict[str, Any]]:
    active_rows = [row for row in continuous if row["completed_trading_date"] <= cutoff_date]
    known_rolls = [row for row in rolls if row["roll_transition_date"] <= cutoff_date]
    current_contract_key = active_rows[-1]["active_contract_key"]
    offsets_by_contract = {current_contract_key: 0.0}
    for roll in reversed(known_rolls):
        if roll["new_contract_key"] in offsets_by_contract:
            offsets_by_contract[roll["old_contract_key"]] = offsets_by_contract[roll["new_contract_key"]] + float(roll["additive_delta_to_prior_history"])
    rows = []
    for row in active_rows:
        if row["active_contract_key"] not in offsets_by_contract:
            raise CarverBlocked("S27 v2 2023 TEST point-in-time offset missing")
        adjustment = offsets_by_contract[row["active_contract_key"]]
        rows.append({**row, "additive_back_adjustment": adjustment, "continuous_close": float(row["raw_close"]) + adjustment})
    return rows


def _build_sigma_rows(continuous: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    closes = [float(row["continuous_close"]) for row in continuous]
    dates = [row["completed_trading_date"] for row in continuous]
    alpha = 2.0 / (32 + 1.0)
    for index in range(34 - 1, len(continuous)):
        window = closes[index - 34 + 1 : index + 1]
        returns = [window[i] / window[i - 1] - 1.0 for i in range(1, len(window))]
        variance = returns[0] * returns[0]
        for value in returns[1:]:
            variance = alpha * value * value + (1.0 - alpha) * variance
        rows.append({"completed_trading_date": dates[index], "sigma_i_t": math.sqrt(variance) * math.sqrt(256.0)})
    return rows


def _build_vqm_rows(sigma_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    alpha = 2.0 / (10 + 1.0)
    smoothed = None
    sigma_values = [float(row["sigma_i_t"]) for row in sigma_rows]
    prefix = [0.0]
    for sigma in sigma_values:
        prefix.append(prefix[-1] + sigma)
    historical_v = []
    for index, sigma_row in enumerate(sigma_rows):
        if index < 2560:
            continue
        ten_year_avg = (prefix[index] - prefix[index - 2560]) / 2560
        sigma = sigma_values[index]
        v = sigma / ten_year_avg
        historical_v.append(v)
        q = sum(1 for value in historical_v if value <= v) / len(historical_v)
        raw_m = 2.0 - 1.5 * q
        smoothed = raw_m if smoothed is None else alpha * raw_m + (1.0 - alpha) * smoothed
        rows.append({"completed_trading_date": sigma_row["completed_trading_date"], "relative_volatility_v": v, "quantile_q": q, "vol_multiplier_m_ewma10": smoothed})
    return rows


def _runtime_row_from_source(
    pit: list[dict[str, Any]],
    sigma: dict[str, Any],
    vqm: dict[str, Any],
    decision: dict[str, Any],
    row_index: int,
) -> dict[str, str]:
    previous_daily = pit[-1]
    window = pit[-64:]
    row: dict[str, Any] = {
        "row_index": row_index,
        "decision_timestamp_utc": decision["derived_completed_bar_end_utc"],
        "decision_trading_date": decision["completed_trading_date"],
        "previous_daily_trading_date": previous_daily["completed_trading_date"],
        "point_in_time_roll_cutoff_date": previous_daily["completed_trading_date"],
        "daily_window_start": window[0]["completed_trading_date"],
        "daily_window_end": window[-1]["completed_trading_date"],
        "daily_window_row_count": 64,
        "previous_daily_raw_symbol": previous_daily["raw_symbol"],
        "previous_daily_raw_close": _num(previous_daily["raw_close"]),
        "previous_daily_additive_back_adjustment": _num(previous_daily["additive_back_adjustment"]),
        "ewma5_equilibrium": _num(_ewma(tuple(float(item["continuous_close"]) for item in window), 5)),
        "ewmac16_64_trend": _num(_ewma(tuple(float(item["continuous_close"]) for item in window), 16) - _ewma(tuple(float(item["continuous_close"]) for item in window), 64)),
        "annual_percentage_sigma": _num(sigma["sigma_i_t"]),
        "relative_volatility_v": _num(vqm["relative_volatility_v"]),
        "quantile_q": _num(vqm["quantile_q"]),
        "vol_multiplier_m": _num(vqm["vol_multiplier_m_ewma10"]),
        "runtime_status": "PASS_ROLLING_STRICT_PRIOR_DAILY_EVIDENCE_2023_TEST_NOT_RESULT",
        "no_lookahead_status": "PASS_2023_TEST_SELECTED_ROW_STRICT_PRIOR_DAILY_EVIDENCE",
    }
    row["row_hash"] = _row_hash("S27_V2_2023_TEST_RUNTIME_EVIDENCE_ROW", row)
    return {key: str(value) for key, value in row.items()}


def _hourly_row_from_source(source_row: dict[str, Any], runtime: dict[str, Any], role: str, row_index: int) -> dict[str, str]:
    adjustment = float(runtime["previous_daily_additive_back_adjustment"])
    packed: dict[str, Any] = {
        "row_index": row_index,
        "completed_timestamp_utc": source_row["derived_completed_bar_end_utc"],
        "trading_date": source_row["completed_trading_date"],
        "raw_symbol": source_row["raw_symbol"],
        "session_id": _session_id(source_row["derived_completed_bar_end_utc"]),
        "row_locator": f"{RUN_ID}_{role}_{row_index:04d}_{source_row['derived_completed_bar_end_utc'].replace('-', '').replace(':', '')}_{source_row['raw_symbol']}",
        "close_price": _num(float(source_row["close"]) + adjustment),
        "source_provider_csv": source_row["source_provider_csv"],
        "source_provider_csv_sha256": source_row["source_provider_csv_sha256"],
        "source_row_hash": _row_hash("strategy_facing_hourly_available_bars", source_row),
        "readiness_status": "READY_COMPLETED_BAR_DATABENTO_2023_TEST",
    }
    packed["row_hash"] = _row_hash(f"S27_V2_2023_TEST_{role}_ROW", packed)
    return {key: str(value) for key, value in packed.items()}


def _valuation_row_from_source(source_row: dict[str, Any], runtime: dict[str, Any], row_index: int) -> dict[str, str]:
    packed = _hourly_row_from_source(source_row, runtime, "VALUATION_MARK", row_index)
    packed["valuation_convention_label"] = VALUATION_CONVENTION_LABEL
    packed["readiness_status"] = "READY_COMPLETED_BAR_DATABENTO_2023_TEST_VALUATION_MARK"
    packed["row_hash"] = _row_hash("S27_V2_2023_TEST_VALUATION_MARK_ROW", packed)
    return {key: str(value) for key, value in packed.items()}


def _daily_summary_rows(selection: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for row in selection:
        runtime = row["runtime"]
        seen[runtime["previous_daily_trading_date"]] = {
            "completed_timestamp_utc": f"{runtime['previous_daily_trading_date']}T00:00:00Z",
            "trading_date": runtime["previous_daily_trading_date"],
            "raw_symbol": runtime["previous_daily_raw_symbol"],
            "row_locator": f"{RUN_ID}_DAILY_CONTINUOUS_{runtime['previous_daily_trading_date'].replace('-', '')}",
            "close_price": _num(float(runtime["previous_daily_raw_close"]) + float(runtime["previous_daily_additive_back_adjustment"])),
            "annual_percentage_sigma": runtime["annual_percentage_sigma"],
            "runtime_evidence_row_hash": runtime["row_hash"],
            "readiness_status": "READY_ROLLING_STRICT_PRIOR_DAILY_EVIDENCE_SUMMARY",
        }
    return list(seen.values())


def _daily_current_rows(selection: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, row in enumerate(selection, 1):
        runtime = row["runtime"]
        rows.append(
            {
                "row_index": index,
                "completed_timestamp_utc": f"{runtime['previous_daily_trading_date']}T00:00:00Z",
                "trading_date": runtime["previous_daily_trading_date"],
                "raw_symbol": runtime["previous_daily_raw_symbol"],
                "row_locator": f"{RUN_ID}_DAILY_CURRENT_{index:04d}_{runtime['previous_daily_trading_date'].replace('-', '')}",
                "close_price": runtime["previous_daily_raw_close"],
                "runtime_evidence_row_hash": runtime["row_hash"],
                "readiness_status": "READY_ROLLING_STRICT_PRIOR_CURRENT_CONTRACT_DAILY_EVIDENCE",
            }
        )
    return rows


def _session_rows(selection: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for selected in selection:
        for role in ("decision", "fill", "mark"):
            timestamp = selected[role]["derived_completed_bar_end_utc"]
            session_id = _session_id(timestamp)
            start, end = _session_bounds(timestamp)
            rows[session_id] = {
                "session_id": session_id,
                "session_start_utc": start,
                "session_end_utc": end,
                "calendar_status": "LOCAL_DATABENTO_2023_TEST_COMPLETED_BAR_SESSION_CONTEXT",
                "readiness_status": "READY_SESSION_CONTEXT_2023_TEST",
            }
    return list(rows.values())


def _roll_rows(rolls: list[dict[str, str]], cutoff: str) -> list[dict[str, str]]:
    rows = []
    for index, row in enumerate([roll for roll in rolls if roll["roll_transition_date"] <= cutoff], 1):
        rows.append(
            {
                "roll_id": f"{RUN_ID}_ROLL_{index:04d}_{row['roll_transition_date'].replace('-', '')}",
                "old_contract_key": row["old_contract_key"],
                "new_contract_key": row["new_contract_key"],
                "roll_transition_date": row["roll_transition_date"],
                "additive_delta_to_prior_history": row["additive_delta_to_prior_history"],
                "readiness_status": "READY_DATABENTO_2023_TEST_ROLL_CONTEXT",
            }
        )
    return rows


def _cost_rows() -> list[dict[str, str]]:
    return [
        {
            "cost_policy_id": "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11",
            "instrument": "ZN",
            "currency": "USD",
            "commission_per_contract_per_side": "2.30",
            "spread_cost_policy": "LIMIT_FILL_COMMISSION_ONLY_NO_MARKET_SPREAD",
            "cost_policy_status": "INFERRED_RETAIL_FUTURES_COST_ACCEPTED_FOR_LOCAL_TEST_MECHANICAL_ONLY_NOT_BOOK_EXPLICIT",
            "readiness_status": "READY_COST_PARAMETER_FOR_LOCAL_TEST_MECHANICAL_ONLY",
        }
    ]


def _group_hourly_by_symbol(hourly_rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in sorted(hourly_rows, key=lambda item: item["derived_completed_bar_end_utc"]):
        grouped.setdefault(row["raw_symbol"], []).append(row)
    return grouped


def _next_same_symbol_source_row_after(hourly_rows: list[dict[str, Any]], completed_ts: str) -> dict[str, Any] | None:
    for row in hourly_rows:
        if row["derived_completed_bar_end_utc"] > completed_ts:
            return row
    return None


def _source_hourly_row_by_hash(source_by_hash: dict[str, dict[str, Any]], source_row_hash: str, label: str) -> dict[str, Any]:
    row = source_by_hash.get(source_row_hash)
    if row is None:
        raise CarverBlocked(f"S27 v2 2023 TEST {label} row hash must resolve to active source hourly row")
    return row


def _session_id(timestamp: str) -> str:
    start, end = _session_bounds(timestamp)
    return f"UTC_ZN_2023_TEST_{start}_{end}"


def _session_bounds(timestamp: str) -> tuple[str, str]:
    completed = _parse_timestamp(timestamp)
    if completed.hour >= 22:
        start = completed.replace(hour=22, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=23)
    else:
        end = completed.replace(hour=21, minute=0, second=0, microsecond=0)
        start = end - timedelta(hours=23)
    return _z(start), _z(end)


def _parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ewma(values: tuple[float, ...], span: int) -> float:
    alpha = 2.0 / (span + 1.0)
    current = values[0]
    for value in values[1:]:
        current = alpha * value + (1.0 - alpha) * current
    return current


def _formula_limit(target_position: int, base_position: float, ewma5: float, sigma_price: float, multiplier_m: float, trend: float) -> float | None:
    if trend == 0.0:
        return None
    if target_position > 0 and trend <= 0.0:
        return None
    if target_position < 0 and trend >= 0.0:
        return None
    target_capped = target_position / base_position * FORECAST_TO_POSITION_DIVISOR
    if abs(target_capped) >= FORECAST_CAP_VALUE:
        return None
    target_risk = target_capped / FORECAST_SCALAR_VALUE
    pre_vol_risk = target_risk / multiplier_m
    return ewma5 - pre_vol_risk * sigma_price


def _adjacent_limit_formula_fail_status(target_position: int, base_position: float) -> str:
    target_capped = target_position / base_position * FORECAST_TO_POSITION_DIVISOR
    if abs(target_capped) >= FORECAST_CAP_VALUE:
        return FAIL_CLOSED_ADJACENT_LIMIT_CAP_BOUND_STATUS
    return FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_STATUS


def _is_cap_bound_market_order_case(
    *,
    position_change: int,
    adjacent_target: int,
    base_position: float,
    trend: float,
) -> bool:
    if abs(position_change) != 1 or adjacent_target == 0 or base_position <= 0.0:
        return False
    target_capped = adjacent_target / base_position * FORECAST_TO_POSITION_DIVISOR
    if abs(target_capped) < FORECAST_CAP_VALUE:
        return False
    return (target_capped > 0.0 and trend > 0.0) or (target_capped < 0.0 and trend < 0.0)


def _expected_market_trigger_source_condition(order_row: Mapping[str, Any]) -> str:
    if str(order_row.get("formula_limit_price")) == CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL:
        if str(order_row.get("limit_order_price")) != CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL:
            raise CarverBlocked("S27 v2 2023 TEST cap-bound market order must not emit a limit price")
        return CAP_BOUND_MARKET_ORDER_TRIGGER_SOURCE_CONDITION
    return MARKET_ORDER_TRIGGER_SOURCE_CONDITION


def _round_limit(price: float, side: str) -> float:
    if side == "BUY":
        return math.floor((price + 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    if side == "SELL":
        return math.ceil((price - 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    return 0.0


def _limit_fill(side: str, close_price: float, limit_price: float) -> bool:
    return (side == "BUY" and close_price <= limit_price) or (side == "SELL" and close_price >= limit_price)


def _round_half_away_from_zero(value: float) -> int:
    magnitude = math.floor(abs(value) + 0.5)
    return magnitude if value >= 0.0 else -magnitude


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _exclusion(row: dict[str, str], reason: str) -> dict[str, str]:
    return {
        "completed_timestamp_utc": row.get("derived_completed_bar_end_utc", ""),
        "trading_date": row.get("completed_trading_date", ""),
        "raw_symbol": row.get("raw_symbol", ""),
        "exclusion_reason": reason,
        "row_status": "LOCAL_2023_TEST_SOURCE_ROW_EXCLUDED_NOT_SILENT",
    }


def _require_rows_equal(observed: dict[str, str], expected: dict[str, str], label: str) -> None:
    if {key: str(value) for key, value in observed.items()} != expected:
        raise CarverBlocked(f"{label} must be recomputed from active source ledgers")


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _safe_read_csv_rows(path: Path, label: str) -> list[dict[str, str]]:
    try:
        return _read_csv_rows(path)
    except FileNotFoundError as exc:
        raise CarverBlocked(f"{label} file is missing") from exc


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="ascii"))
    if not isinstance(payload, dict):
        raise CarverBlocked("S27 v2 2023 TEST JSON payload must be an object")
    return payload


def _safe_read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        return _read_json(path)
    except FileNotFoundError as exc:
        raise CarverBlocked(f"{label} file is missing") from exc


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: tuple[str, ...] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    resolved_fieldnames: list[str] = list(fieldnames or ())
    for row in rows:
        for key in row:
            if key not in resolved_fieldnames:
                resolved_fieldnames.append(key)
    if not resolved_fieldnames:
        raise CarverBlocked("S27 v2 2023 TEST refuses empty CSV artifacts without declared headers")
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=resolved_fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(row.get(key, "")) for key in resolved_fieldnames})


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _write_sha256s_txt(path: Path, root: Path) -> None:
    lines = [f"{_sha256(item).upper()} {item.name}" for item in sorted(root.iterdir()) if item.is_file() and item.name != path.name]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def _write_sha256s_csv(output_root: Path) -> None:
    rows = [
        {"relative_path": path.relative_to(output_root).as_posix(), "sha256": _sha256(path)}
        for path in sorted(output_root.iterdir())
        if path.is_file() and path.name != "SHA256SUMS.csv"
    ]
    _write_csv(output_root / "SHA256SUMS.csv", rows)


def _write_sha256s_csv_for_files(path: Path, root: Path, filenames: tuple[str, ...]) -> None:
    rows = [{"relative_path": filename, "sha256": _sha256(root / filename)} for filename in filenames]
    _write_csv(path, rows)


def _tbbo_requirements_manifest(
    output_root: Path,
    source_root: Path,
    rows: list[dict[str, Any]],
    terminal_status: str,
) -> dict[str, Any]:
    missing = [row for row in rows if row["tbbo_requirement_status"] == "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"]
    bound = [row for row in rows if row["tbbo_requirement_status"] == "ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE"]
    return {
        "artifact": "S27_V2_2023_TEST_MARKET_ORDER_TBBO_REQUIREMENTS_DISCOVERY_MANIFEST",
        "authorization": TBBO_REQUIREMENTS_AUTHORIZATION,
        "status": TBBO_REQUIREMENTS_STATUS,
        "lane": S27_V2_LANE,
        "source_continuous_daily_ledger": str((source_root / SOURCE_CONTINUOUS_NAME).relative_to(_REPO_ROOT)),
        "source_roll_ledger": str((source_root / SOURCE_ROLL_NAME).relative_to(_REPO_ROOT)),
        "source_hourly_ledger": str((source_root / SOURCE_HOURLY_NAME).relative_to(_REPO_ROOT)),
        "requirements_ledger": TBBO_REQUIREMENT_LEDGER_NAME,
        "requirements_ledger_sha256": _sha256(output_root / TBBO_REQUIREMENT_LEDGER_NAME),
        "total_market_order_rows": len(rows),
        "missing_tbbo_requirement_count": len(missing),
        "already_bound_tbbo_count": len(bound),
        "first_missing_row_index": missing[0]["row_index"] if missing else "NO_MISSING_TBBO_REQUIREMENTS",
        "last_missing_row_index": missing[-1]["row_index"] if missing else "NO_MISSING_TBBO_REQUIREMENTS",
        "terminal_status": terminal_status,
        "provider_api_access": "NO",
        "downloads": "NO",
        "result_interpretation": "NO",
        "source_faithful_evidence_claim": "NO",
        "non_authorizations": list(NON_AUTHORIZATIONS),
    }


def _csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def _hash_row(row: dict[str, Any]) -> dict[str, Any]:
    row = dict(row)
    row["row_hash"] = canonical_sha256(row)
    return row


def _row_hash(label: str, row: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps({"artifact": label, "row": row}, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest().upper()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _num(value: Any) -> str:
    return format(float(value), ".17g")


def _csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _bundle_payload(bundle: TestMechanicalRunBundle) -> dict[str, Any]:
    return {key: value for key, value in bundle.__dict__.items() if key != "bundle_hash"}


def _tbbo_requirements_bundle_payload(bundle: MarketOrderTBBORequirementsDiscoveryBundle) -> dict[str, Any]:
    return {key: value for key, value in bundle.__dict__.items() if key != "bundle_hash"}

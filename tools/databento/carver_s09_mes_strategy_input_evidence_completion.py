from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from io import StringIO
from math import isfinite
from numbers import Real
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked
from carver.spine.m2 import S09_EWMAC_SPANS, s09_fdm_for_allowed_spans

GATE = "S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
MACHINERY_DEVELOPMENT_SLICE_START = "2019-05-05"
MACHINERY_DEVELOPMENT_SLICE_END = "2020-04-05"
MACHINERY_DEVELOPMENT_SLICE_TEXT = "2019-05-05 through 2020-04-05"
RUNTIME_INPUT_LOCK_SCOPE = "oldest minimum machinery-development slice only"
DESIGN_ORDERING = "oldest authorized completed source-native data first"
RUN_ID = "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION"
OUTPUT_ROOT_RELATIVE = "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05"
RESULT_RELATIVE_PATH = "docs/process/CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_RESULT_2026-06-03.md"
AUDIT_RELATIVE_PATH = "docs/process/CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
NEXT_EVIDENCE_AUTHORIZATION_PACKET_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_STRATEGY_INPUT_NEXT_EVIDENCE_AUTHORIZATION_PACKET_2026-06-03.md"
)
NEXT_EVIDENCE_AUTHORIZATION_AUDIT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_STRATEGY_INPUT_NEXT_EVIDENCE_AUTHORIZATION_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
NEXT_EVIDENCE_AUTHORIZATION_HASH_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_STRATEGY_INPUT_NEXT_EVIDENCE_AUTHORIZATION_PACKET_sha256.txt"
)
HISTORICAL_COST_SOURCE_ACQUISITION_AUTHORIZATION_PACKET_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_PACKET_2026-06-03.md"
)
HISTORICAL_COST_SOURCE_ACQUISITION_AUTHORIZATION_AUDIT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
HISTORICAL_COST_SOURCE_ACQUISITION_AUTHORIZATION_HASH_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_PACKET_sha256.txt"
)
HISTORICAL_COST_BLOCKER_DECISION_AUTHORIZATION_PACKET_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_PACKET_2026-06-03.md"
)
HISTORICAL_COST_BLOCKER_DECISION_AUTHORIZATION_AUDIT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
HISTORICAL_COST_BLOCKER_DECISION_AUTHORIZATION_HASH_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_PACKET_sha256.txt"
)
HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_PACKET_RELATIVE_PATH = (
    "docs/process/"
    "CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUTHORIZATION_READY_PACKET_2026-06-03.md"
)
HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUDIT_RELATIVE_PATH = (
    "docs/process/"
    "CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_HASH_RELATIVE_PATH = (
    "docs/process/"
    "CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUTHORIZATION_READY_PACKET_sha256.txt"
)
HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_ETF_PACKET_RELATIVE_PATH = (
    "docs/process/"
    "CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_AUTHORIZATION_READY_PACKET_2026-06-03.md"
)
HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_ETF_AUDIT_RELATIVE_PATH = (
    "docs/process/"
    "CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_ETF_HASH_RELATIVE_PATH = (
    "docs/process/"
    "CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_AUTHORIZATION_READY_PACKET_sha256.txt"
)
SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_RESULT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_RESULT_2026-06-03.md"
)
SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_AUDIT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_HASH_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_sha256.txt"
)
OFFICIAL_LIFECYCLE_CONTRACT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_ARTIFACT_CONTRACT_2026-06-03.md"
)
OFFICIAL_LIFECYCLE_CONTRACT_AUDIT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_ARTIFACT_CONTRACT_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
OFFICIAL_LIFECYCLE_CONTRACT_HASH_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_ARTIFACT_CONTRACT_sha256.txt"
)
OFFICIAL_LIFECYCLE_LEDGER_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv"
)
OFFICIAL_LIFECYCLE_STATUS_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_status.json"
)
OFFICIAL_LIFECYCLE_PROVENANCE_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_provenance.md"
)
OFFICIAL_LIFECYCLE_HASH_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_sha256.txt"
)
ROLL_SEMANTICS_CONTRACT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_2026-06-03.md"
)
ROLL_SEMANTICS_CONTRACT_AUDIT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
ROLL_SEMANTICS_CONTRACT_HASH_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_sha256.txt"
)
ROLL_SEMANTICS_LEDGER_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv"
)
ROLL_SEMANTICS_STATUS_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_status.json"
)
ROLL_SEMANTICS_PROVENANCE_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_provenance.md"
)
ROLL_SEMANTICS_HASH_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_sha256.txt"
)
ANNUAL_RISK_CONTRACT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_2026-06-03.md"
)
ANNUAL_RISK_CONTRACT_AUDIT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
ANNUAL_RISK_CONTRACT_HASH_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_sha256.txt"
)
ANNUAL_RISK_LEDGER_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv"
)
ANNUAL_RISK_STATUS_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_status.json"
)
ANNUAL_RISK_PROVENANCE_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_provenance.md"
)
ANNUAL_RISK_HASH_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_sha256.txt"
)
DAILY_PRICE_RISK_CONTRACT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_2026-06-03.md"
)
DAILY_PRICE_RISK_CONTRACT_AUDIT_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
)
DAILY_PRICE_RISK_CONTRACT_HASH_RELATIVE_PATH = (
    "docs/process/CARVER_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_sha256.txt"
)
DAILY_PRICE_RISK_LEDGER_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv"
)
DAILY_PRICE_RISK_STATUS_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_DAILY_PRICE_RISK_status.json"
)
DAILY_PRICE_RISK_PROVENANCE_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_DAILY_PRICE_RISK_provenance.md"
)
DAILY_PRICE_RISK_HASH_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_DAILY_PRICE_RISK_sha256.txt"
)
HISTORICAL_COST_LEDGER_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv"
)
HISTORICAL_COST_STATUS_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_status.json"
)
HISTORICAL_COST_PROVENANCE_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_provenance.md"
)
HISTORICAL_COST_HASH_RELATIVE_PATH = (
    f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_sha256.txt"
)
MACHINERY_DEV_MINIMUM_SLICE_DEFINITION_LEDGER_RELATIVE_PATH = (
    "docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/raw_provider_metadata/"
    "20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_definition_ledger.csv"
)
MACHINERY_DEV_LINEAGE_DEFINITION_CROSSCHECK_LEDGER_RELATIVE_PATH = (
    "docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/lifecycle/"
    "20260603_S09_MES_MACHINERY_DEV_LINEAGE_definition_crosscheck_ledger.csv"
)
MACHINERY_DEV_LINEAGE_ROLL_PLAN_RELATIVE_PATH = (
    "docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/roll_plan/"
    "20260603_S09_MES_MACHINERY_DEV_LINEAGE_roll_plan.csv"
)
MACHINERY_DEV_LINEAGE_CONTINUOUS_SERIES_RELATIVE_PATH = (
    "docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/continuous_series/"
    "20260603_S09_MES_MACHINERY_DEV_LINEAGE_continuous_daily_mes_machinery_only.csv"
)
MACHINERY_DEV_LINEAGE_HASH_RELATIVE_PATH = (
    "docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/hashes/"
    "20260603_S09_MES_MACHINERY_DEV_LINEAGE_sha256.json"
)
READINESS_HANDOFF_NEXT_GATE = "S09_MES_STRATEGY_INPUT_READINESS_GATE"
NEXT_EVIDENCE_AUTHORIZATION_PACKET_STATUS = (
    "PROCESS_ONLY_S09_MES_STRATEGY_INPUT_NEXT_EVIDENCE_AUTHORIZATION_PACKET_NOT_AUTHORIZATION_NOT_DATA_NOT_BACKTEST"
)
EVIDENCE_FAMILY_PREFLIGHT_STATUS = "AUTHORIZED_EVIDENCE_FAMILY_PREFLIGHT_ONLY_NOT_EXECUTED"
OFFICIAL_LIFECYCLE_CONTRACT_STATUS = (
    "PROCESS_ONLY_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION"
)
EVIDENCE_LEDGER_COLUMNS = ("evidence_name", "required_status", "current_status", "blocking_reason", "next_action")
LIFECYCLE_LEDGER_COLUMNS = (
    "raw_symbol",
    "first_completed_trading_date",
    "last_completed_trading_date",
    "expiration_completed_trading_date",
    "source_label",
    "source_sha256",
    "status",
)
ROLL_SEMANTICS_LEDGER_COLUMNS = (
    "old_symbol",
    "new_symbol",
    "provider_roll_date",
    "completed_roll_date",
    "source_label",
    "source_sha256",
    "status",
)
ANNUAL_RISK_LEDGER_COLUMNS = (
    "completed_trading_date",
    "long_run_annual_risk",
    "current_ewma32_annual_risk",
    "annual_percentage_risk",
    "source_label",
    "source_sha256",
    "status",
)
DAILY_PRICE_RISK_LEDGER_COLUMNS = (
    "completed_trading_date",
    "current_price",
    "annual_percentage_risk",
    "daily_price_risk_currency",
    "source_label",
    "source_sha256",
    "status",
)
COST_VALUE_LEDGER_COLUMNS = (
    "completed_trading_date",
    "component_name",
    "amount_currency",
    "currency",
    "charge_timing",
    "effective_start",
    "effective_end",
    "source_label",
    "source_sha256",
    "status",
)
RISK_ADJUSTED_COST_LEDGER_COLUMNS = (
    "completed_trading_date",
    "total_cost_per_trade_currency",
    "daily_price_risk_currency",
    "risk_adjusted_cost_per_trade_sr",
    "source_label",
    "source_sha256",
    "status",
)
SPEED_ELIGIBILITY_LEDGER_COLUMNS = (
    "span",
    "turnover",
    "risk_adjusted_cost_per_trade_sr",
    "threshold_sr",
    "eligible",
    "source_label",
    "source_sha256",
    "status",
)
ELIGIBLE_SPEED_SET_FDM_LEDGER_COLUMNS = (
    "eligible_spans",
    "table36_fdm",
    "source_label",
    "source_sha256",
    "status",
)
EVIDENCE_NOT_LOCKED_STATUS = "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_NOT_LOCKED"
EVIDENCE_COMPLETION_NOT_READY_STATUS = "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY"
EVIDENCE_COMPLETION_LOCKED_STATUS = "LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION"
STRATEGY_INPUT_NOT_READY_STATUS = "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY"
STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_STATUS = "S09_MES_STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_GATE"
LIFECYCLE_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE"
ROLL_SEMANTICS_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS"
ANNUAL_RISK_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE"
DAILY_PRICE_RISK_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE"
COST_VALUE_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE"
HISTORICAL_COST_FAIL_CLOSED_STATUS = "FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED"
RISK_ADJUSTED_COST_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE"
SPEED_ELIGIBILITY_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"
ELIGIBLE_SPEED_SET_FDM_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM"
ANNUAL_RISK_LONG_RUN_WEIGHT = 0.30
ANNUAL_RISK_CURRENT_WEIGHT = 0.70
ANNUAL_RISK_EWMA_SPAN = 32
ANNUAL_RISK_WINDOW_ROWS = 33
ANNUAL_RISK_ANNUALIZATION_DAYS = 256.0
SPEED_ELIGIBILITY_THRESHOLD_SR = 0.15
DAILY_TO_ANNUAL_RISK_SCALAR = 16
MES_CONTRACT_MULTIPLIER_USD_PER_POINT = 5.0
REQUIRED_COST_COMPONENTS = (
    "exchange_fee",
    "clearing_regulatory_fee",
    "broker_commission",
    "spread_slippage",
)
COST_CHARGE_TIMINGS = ("PER_SIDE", "ROUND_TURN")
EWMAC_TURNOVER_BY_SPAN = {
    2: 98.5,
    4: 50.2,
    8: 25.4,
    16: 13.2,
    32: 7.6,
    64: 5.2,
}
REQUIRED_EVIDENCE_NAMES = (
    "official_lifecycle_evidence",
    "roll_trading_day_semantics",
    "annual_risk_runtime_values",
    "daily_price_risk_values",
    "historical_mes_cost_values",
    "risk_adjusted_cost_values",
    "speed_eligibility_values",
    "eligible_speed_set",
    "table36_fdm_row",
    "hash_bound_provenance",
)


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice_start: str
    machinery_development_slice_end: str
    runtime_input_lock_scope: str
    design_ordering: str
    databento_api_access_authorized: bool
    market_row_parsing_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceFamilyAuthorizationConfig:
    execution_authorized: bool
    selected_evidence_name: str
    evidence_completion_status: str
    remaining_evidence_count: int
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    runtime_input_lock_scope: str
    design_ordering: str
    databento_api_access_authorized: bool
    market_row_parsing_authorized: bool
    risk_runtime_computation_authorized: bool
    cost_computation_authorized: bool
    speed_eligibility_computation_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool


@dataclass(frozen=True)
class S09MESOfficialLifecycleEvidenceLockConfig:
    execution_authorized: bool
    selected_evidence_name: str
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    runtime_input_lock_scope: str
    design_ordering: str
    local_metadata_root: Path
    databento_api_access_authorized: bool
    provider_login_authorized: bool
    market_row_parsing_authorized: bool
    risk_runtime_computation_authorized: bool
    cost_computation_authorized: bool
    speed_eligibility_computation_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


@dataclass(frozen=True)
class S09MESRollTradingDaySemanticsLockConfig:
    execution_authorized: bool
    selected_evidence_name: str
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    runtime_input_lock_scope: str
    design_ordering: str
    local_metadata_root: Path
    databento_api_access_authorized: bool
    provider_login_authorized: bool
    market_row_parsing_authorized: bool
    risk_runtime_computation_authorized: bool
    cost_computation_authorized: bool
    speed_eligibility_computation_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


@dataclass(frozen=True)
class S09MESAnnualRiskRuntimeValuesLockConfig:
    execution_authorized: bool
    selected_evidence_name: str
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    runtime_input_lock_scope: str
    design_ordering: str
    local_metadata_root: Path
    annual_risk_runtime_computation_authorized: bool
    databento_api_access_authorized: bool
    provider_login_authorized: bool
    market_row_parsing_authorized: bool
    cost_computation_authorized: bool
    speed_eligibility_computation_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


@dataclass(frozen=True)
class S09MESDailyPriceRiskValuesLockConfig:
    execution_authorized: bool
    selected_evidence_name: str
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    runtime_input_lock_scope: str
    design_ordering: str
    local_metadata_root: Path
    daily_price_risk_computation_authorized: bool
    databento_api_access_authorized: bool
    provider_login_authorized: bool
    market_row_parsing_authorized: bool
    risk_runtime_computation_authorized: bool
    cost_computation_authorized: bool
    speed_eligibility_computation_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


@dataclass(frozen=True)
class S09MESHistoricalMESCostValuesAttemptConfig:
    execution_authorized: bool
    selected_evidence_name: str
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    runtime_input_lock_scope: str
    design_ordering: str
    local_metadata_root: Path
    historical_cost_values_authorized: bool
    databento_api_access_authorized: bool
    provider_login_authorized: bool
    market_row_parsing_authorized: bool
    risk_runtime_computation_authorized: bool
    cost_computation_authorized: bool
    speed_eligibility_computation_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow:
    raw_symbol: str
    first_completed_trading_date: date
    last_completed_trading_date: date
    expiration_completed_trading_date: date
    source_label: str
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionRollSemanticsRow:
    old_symbol: str
    new_symbol: str
    provider_roll_date: date
    completed_roll_date: date
    source_label: str
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionAnnualRiskRow:
    completed_trading_date: date
    long_run_annual_risk: float
    current_ewma32_annual_risk: float
    annual_percentage_risk: float
    source_label: str
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow:
    completed_trading_date: date
    current_price: float
    annual_percentage_risk: float
    daily_price_risk_currency: float
    source_label: str
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionCostValueRow:
    completed_trading_date: date
    component_name: str
    amount_currency: float
    currency: str
    charge_timing: str
    effective_start: date
    effective_end: date
    source_label: str
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionRiskAdjustedCostRow:
    completed_trading_date: date
    total_cost_per_trade_currency: float
    daily_price_risk_currency: float
    risk_adjusted_cost_per_trade_sr: float
    source_label: str
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow:
    span: int
    turnover: float
    risk_adjusted_cost_per_trade_sr: float
    threshold_sr: float
    eligible: bool
    source_label: str
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow:
    eligible_spans: tuple[int, ...]
    table36_fdm: float
    source_label: str
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionHashManifestEntry:
    relative_path: str
    artifact_text: str


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionLockedBundleRequest:
    lifecycle_rows: tuple[S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow, ...]
    roll_semantics_rows: tuple[S09MESStrategyInputEvidenceCompletionRollSemanticsRow, ...]
    annual_risk_rows: tuple[S09MESStrategyInputEvidenceCompletionAnnualRiskRow, ...]
    daily_price_risk_rows: tuple[S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow, ...]
    cost_value_rows: tuple[S09MESStrategyInputEvidenceCompletionCostValueRow, ...]
    risk_adjusted_cost_rows: tuple[S09MESStrategyInputEvidenceCompletionRiskAdjustedCostRow, ...]
    speed_eligibility_rows: tuple[S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow, ...]
    eligible_speed_set_fdm_rows: tuple[S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow, ...]


@dataclass(frozen=True)
class S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest:
    evidence_completion_status: str
    strategy_input_readiness_status: str
    remaining_evidence_count: int
    next_gate: str
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    databento_api_access: str
    market_row_parsing: str
    forecast_computation: str
    diagnostics_run: str
    backtests_run: str
    test_validation_lockbox_forward_access: str


def run_s09_mes_strategy_input_evidence_completion(
    config: S09MESStrategyInputEvidenceCompletionConfig,
) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES strategy-input evidence completion is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES strategy-input evidence completion is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES strategy-input evidence completion is locked to Appendix C MES row")
    if (
        config.machinery_development_slice_start != MACHINERY_DEVELOPMENT_SLICE_START
        or config.machinery_development_slice_end != MACHINERY_DEVELOPMENT_SLICE_END
    ):
        raise CarverBlocked("S09 MES strategy-input evidence completion must use the oldest machinery-development slice")
    if config.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES strategy-input evidence completion scope is not locked")
    if config.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES strategy-input evidence completion must use oldest authorized data first")
    if config.databento_api_access_authorized:
        raise CarverBlocked("S09 MES strategy-input evidence completion forbids Databento API access unless separately restated")
    if config.market_row_parsing_authorized:
        raise CarverBlocked("S09 MES strategy-input evidence completion forbids market-row parsing in the guard preflight")
    if config.forecast_computation_authorized:
        raise CarverBlocked("S09 MES strategy-input evidence completion forbids forecast computation")
    if config.diagnostics_authorized:
        raise CarverBlocked("S09 MES strategy-input evidence completion forbids diagnostics")
    if config.backtest_authorized:
        raise CarverBlocked("S09 MES strategy-input evidence completion forbids backtests")
    if config.test_validation_lockbox_forward_authorized:
        raise CarverBlocked("S09 MES strategy-input evidence completion forbids TEST/VALIDATION/Lockbox/Forward access")

    return {
        "status": "AUTHORIZED_PREFLIGHT_ONLY_NOT_EXECUTED",
        "gate": GATE,
        "lane_class": LANE_CLASS,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
        "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
        "design_ordering": DESIGN_ORDERING,
        "databento_api_access": "NO",
        "market_row_parsing": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
    }


def run_s09_mes_strategy_input_evidence_family_authorization_preflight(
    config: S09MESStrategyInputEvidenceFamilyAuthorizationConfig,
) -> dict[str, str]:
    if config.execution_authorized is not True:
        raise CarverBlocked("S09 MES evidence-family preflight requires explicit operator authorization")
    if config.selected_evidence_name not in REQUIRED_EVIDENCE_NAMES:
        raise CarverBlocked("S09 MES evidence-family preflight must select exactly one required evidence family")
    if config.evidence_completion_status != EVIDENCE_COMPLETION_NOT_READY_STATUS:
        raise CarverBlocked("S09 MES evidence-family preflight requires fail-closed evidence completion status")
    if isinstance(config.remaining_evidence_count, bool) or config.remaining_evidence_count not in (
        len(REQUIRED_EVIDENCE_NAMES),
        len(REQUIRED_EVIDENCE_NAMES) - 1,
        len(REQUIRED_EVIDENCE_NAMES) - 2,
        len(REQUIRED_EVIDENCE_NAMES) - 3,
        len(REQUIRED_EVIDENCE_NAMES) - 4,
    ):
        raise CarverBlocked("S09 MES evidence-family preflight requires the current evidence gap count")
    locked_by_remaining_count = {
        len(REQUIRED_EVIDENCE_NAMES): (),
        len(REQUIRED_EVIDENCE_NAMES) - 1: ("official_lifecycle_evidence",),
        len(REQUIRED_EVIDENCE_NAMES) - 2: ("official_lifecycle_evidence", "roll_trading_day_semantics"),
        len(REQUIRED_EVIDENCE_NAMES) - 3: (
            "official_lifecycle_evidence",
            "roll_trading_day_semantics",
            "annual_risk_runtime_values",
        ),
        len(REQUIRED_EVIDENCE_NAMES) - 4: (
            "official_lifecycle_evidence",
            "roll_trading_day_semantics",
            "annual_risk_runtime_values",
            "daily_price_risk_values",
        ),
    }
    if config.selected_evidence_name in locked_by_remaining_count[config.remaining_evidence_count]:
        raise CarverBlocked("S09 MES evidence-family preflight cannot reselect an already locked evidence family")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES evidence-family preflight is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES evidence-family preflight is locked to Appendix C MES")
    if config.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES evidence-family preflight must use the oldest machinery-development slice")
    if config.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES evidence-family preflight runtime scope is not locked")
    if config.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES evidence-family preflight must preserve oldest-data-first ordering")

    for label, authorized in (
        ("Databento API access", config.databento_api_access_authorized),
        ("market-row parsing", config.market_row_parsing_authorized),
        ("risk runtime computation", config.risk_runtime_computation_authorized),
        ("cost computation", config.cost_computation_authorized),
        ("speed eligibility computation", config.speed_eligibility_computation_authorized),
        ("forecast computation", config.forecast_computation_authorized),
        ("diagnostics", config.diagnostics_authorized),
        ("backtest", config.backtest_authorized),
        ("TEST/VALIDATION/Lockbox/Forward access", config.test_validation_lockbox_forward_authorized),
    ):
        if authorized is not False:
            raise CarverBlocked(f"S09 MES evidence-family preflight forbids {label}")

    return {
        "status": EVIDENCE_FAMILY_PREFLIGHT_STATUS,
        "selected_evidence_name": config.selected_evidence_name,
        "evidence_completion_status": EVIDENCE_COMPLETION_NOT_READY_STATUS,
        "remaining_evidence_count": str(config.remaining_evidence_count),
        "lane_class": LANE_CLASS,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
        "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
        "design_ordering": DESIGN_ORDERING,
        "blocking_reason": _blocking_reason_for_evidence(config.selected_evidence_name),
        "next_action": _next_action_for_evidence(config.selected_evidence_name),
        "databento_api_access": "NO",
        "market_row_parsing": "NO",
        "risk_runtime_computation": "NO",
        "cost_computation": "NO",
        "speed_eligibility_computation": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
    }


def build_s09_mes_strategy_input_evidence_completion_artifact_bundle() -> dict[str, str]:
    evidence_csv = render_s09_mes_strategy_input_evidence_completion_required_evidence_ledger_csv()
    status_json = render_s09_mes_strategy_input_evidence_completion_status_json()
    provenance_md = render_s09_mes_strategy_input_evidence_completion_provenance_md()
    artifact_text_by_path = {
        f"{OUTPUT_ROOT_RELATIVE}/evidence/{RUN_ID}_required_evidence_ledger.csv": evidence_csv,
        f"{OUTPUT_ROOT_RELATIVE}/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv": _header_csv(LIFECYCLE_LEDGER_COLUMNS),
        f"{OUTPUT_ROOT_RELATIVE}/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv": _header_csv(ROLL_SEMANTICS_LEDGER_COLUMNS),
        f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv": _header_csv(ANNUAL_RISK_LEDGER_COLUMNS),
        f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv": _header_csv(DAILY_PRICE_RISK_LEDGER_COLUMNS),
        f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv": _header_csv(COST_VALUE_LEDGER_COLUMNS),
        f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_RISK_ADJUSTED_COST_ledger.csv": _header_csv(RISK_ADJUSTED_COST_LEDGER_COLUMNS),
        f"{OUTPUT_ROOT_RELATIVE}/speed/20260603_S09_MES_SPEED_ELIGIBILITY_ledger.csv": _header_csv(SPEED_ELIGIBILITY_LEDGER_COLUMNS),
        f"{OUTPUT_ROOT_RELATIVE}/speed/20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv": _header_csv(ELIGIBLE_SPEED_SET_FDM_LEDGER_COLUMNS),
        f"{OUTPUT_ROOT_RELATIVE}/status/{RUN_ID}_status.json": status_json,
        f"{OUTPUT_ROOT_RELATIVE}/provenance/{RUN_ID}_provenance.md": provenance_md,
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        if not isinstance(text, str) or not text.strip():
            raise CarverBlocked("S09 MES evidence completion artifact text is missing")
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES evidence completion artifact text must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text:
            raise CarverBlocked("S09 MES evidence completion artifacts must not promote backtest or lockbox readiness")
    artifact_text_by_path[f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt"] = _render_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def build_s09_mes_strategy_input_evidence_completion_partial_bookkeeping_bundle(
    *,
    locked_evidence_names: tuple[str, ...],
) -> dict[str, str]:
    _validate_partial_bookkeeping_locked_evidence_names(locked_evidence_names)
    artifact_text_by_path = {
        f"{OUTPUT_ROOT_RELATIVE}/evidence/{RUN_ID}_required_evidence_ledger.csv": render_s09_mes_strategy_input_evidence_completion_partial_required_evidence_ledger_csv(locked_evidence_names),
        f"{OUTPUT_ROOT_RELATIVE}/status/{RUN_ID}_status.json": render_s09_mes_strategy_input_evidence_completion_partial_status_json(locked_evidence_names),
        f"{OUTPUT_ROOT_RELATIVE}/provenance/{RUN_ID}_provenance.md": render_s09_mes_strategy_input_evidence_completion_partial_provenance_md(locked_evidence_names),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES partial evidence bookkeeping text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES partial evidence bookkeeping must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES partial evidence bookkeeping must not promote forbidden scope")
    artifact_text_by_path[f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt"] = _render_sha256_manifest(
        artifact_text_by_path
    )
    return artifact_text_by_path


def build_s09_mes_strategy_input_evidence_completion_locked_artifact_bundle(
    request: S09MESStrategyInputEvidenceCompletionLockedBundleRequest,
) -> dict[str, str]:
    artifact_text_by_path = {
        f"{OUTPUT_ROOT_RELATIVE}/evidence/{RUN_ID}_required_evidence_ledger.csv": render_s09_mes_strategy_input_evidence_completion_locked_evidence_ledger_csv(),
        f"{OUTPUT_ROOT_RELATIVE}/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv": render_s09_mes_strategy_input_evidence_completion_lifecycle_ledger_csv(request.lifecycle_rows),
        f"{OUTPUT_ROOT_RELATIVE}/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv": render_s09_mes_strategy_input_evidence_completion_roll_semantics_ledger_csv(request.roll_semantics_rows),
        f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv": render_s09_mes_strategy_input_evidence_completion_annual_risk_ledger_csv(request.annual_risk_rows),
        f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv": render_s09_mes_strategy_input_evidence_completion_daily_price_risk_ledger_csv(request.daily_price_risk_rows),
        f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv": render_s09_mes_strategy_input_evidence_completion_cost_value_ledger_csv(request.cost_value_rows),
        f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_RISK_ADJUSTED_COST_ledger.csv": render_s09_mes_strategy_input_evidence_completion_risk_adjusted_cost_ledger_csv(request.risk_adjusted_cost_rows),
        f"{OUTPUT_ROOT_RELATIVE}/speed/20260603_S09_MES_SPEED_ELIGIBILITY_ledger.csv": render_s09_mes_strategy_input_evidence_completion_speed_eligibility_ledger_csv(request.speed_eligibility_rows),
        f"{OUTPUT_ROOT_RELATIVE}/speed/20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv": render_s09_mes_strategy_input_evidence_completion_eligible_speed_set_fdm_ledger_csv(request.eligible_speed_set_fdm_rows),
        f"{OUTPUT_ROOT_RELATIVE}/status/{RUN_ID}_status.json": render_s09_mes_strategy_input_evidence_completion_locked_status_json(),
        f"{OUTPUT_ROOT_RELATIVE}/provenance/{RUN_ID}_provenance.md": render_s09_mes_strategy_input_evidence_completion_locked_provenance_md(),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES locked evidence completion artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES locked evidence completion artifact text must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text:
            raise CarverBlocked("S09 MES locked evidence completion artifacts must not promote backtest or lockbox readiness")
    artifact_text_by_path[f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt"] = _render_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def build_s09_mes_strategy_input_evidence_completion_readiness_handoff_bundle(
    request: S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest,
) -> dict[str, str]:
    _validate_readiness_handoff_request(request)
    json_text = render_s09_mes_strategy_input_evidence_completion_readiness_handoff_json(request)
    md_text = render_s09_mes_strategy_input_evidence_completion_readiness_handoff_md(request)
    artifact_text_by_path = {
        f"{OUTPUT_ROOT_RELATIVE}/handoff/{RUN_ID}_readiness_handoff.json": json_text,
        f"{OUTPUT_ROOT_RELATIVE}/handoff/{RUN_ID}_readiness_handoff.md": md_text,
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES evidence completion readiness handoff artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES evidence completion readiness handoff must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text:
            raise CarverBlocked("S09 MES evidence completion readiness handoff must not promote backtest or lockbox readiness")
    artifact_text_by_path[f"{OUTPUT_ROOT_RELATIVE}/handoff/{RUN_ID}_readiness_handoff_sha256.txt"] = _render_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def build_s09_mes_strategy_input_next_evidence_authorization_packet_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        NEXT_EVIDENCE_AUTHORIZATION_PACKET_RELATIVE_PATH: render_s09_mes_strategy_input_next_evidence_authorization_packet_md(),
        NEXT_EVIDENCE_AUTHORIZATION_AUDIT_RELATIVE_PATH: render_s09_mes_strategy_input_next_evidence_authorization_packet_audit_md(),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES next-evidence authorization packet text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES next-evidence authorization packet must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text:
            raise CarverBlocked("S09 MES next-evidence authorization packet must not promote readiness")
    artifact_text_by_path[NEXT_EVIDENCE_AUTHORIZATION_HASH_RELATIVE_PATH] = _render_process_sha256_manifest(
        artifact_text_by_path
    )
    return artifact_text_by_path


def build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle(
    config: S09MESStrategyInputEvidenceFamilyAuthorizationConfig,
) -> dict[str, str]:
    preflight = run_s09_mes_strategy_input_evidence_family_authorization_preflight(config)
    stem = _selected_evidence_packet_stem(preflight["selected_evidence_name"])
    packet_path = f"docs/process/{stem}_2026-06-03.md"
    audit_path = f"docs/process/{stem}_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
    hash_path = f"docs/process/{stem}_sha256.txt"
    artifact_text_by_path = {
        packet_path: render_s09_mes_strategy_input_selected_evidence_authorization_packet_md(preflight),
        audit_path: render_s09_mes_strategy_input_selected_evidence_authorization_packet_audit_md(preflight),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES selected-evidence authorization packet text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES selected-evidence authorization packet must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text:
            raise CarverBlocked("S09 MES selected-evidence authorization packet must not promote readiness")
    artifact_text_by_path[hash_path] = _render_process_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def build_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        HISTORICAL_COST_SOURCE_ACQUISITION_AUTHORIZATION_PACKET_RELATIVE_PATH: (
            render_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_md()
        ),
        HISTORICAL_COST_SOURCE_ACQUISITION_AUTHORIZATION_AUDIT_RELATIVE_PATH: (
            render_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_audit_md()
        ),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES historical cost source acquisition authorization packet text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES historical cost source acquisition packet must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES historical cost source acquisition packet must not promote forbidden scope")
    artifact_text_by_path[HISTORICAL_COST_SOURCE_ACQUISITION_AUTHORIZATION_HASH_RELATIVE_PATH] = (
        _render_process_sha256_manifest(artifact_text_by_path)
    )
    return artifact_text_by_path


def build_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        HISTORICAL_COST_BLOCKER_DECISION_AUTHORIZATION_PACKET_RELATIVE_PATH: (
            render_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_md()
        ),
        HISTORICAL_COST_BLOCKER_DECISION_AUTHORIZATION_AUDIT_RELATIVE_PATH: (
            render_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_audit_md()
        ),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES historical cost blocker decision packet text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES historical cost blocker decision packet must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES historical cost blocker decision packet must not promote forbidden scope")
        if COST_VALUE_LOCKED_STATUS in text:
            raise CarverBlocked("S09 MES historical cost blocker decision packet must not lock cost values")
    artifact_text_by_path[HISTORICAL_COST_BLOCKER_DECISION_AUTHORIZATION_HASH_RELATIVE_PATH] = (
        _render_process_sha256_manifest(artifact_text_by_path)
    )
    return artifact_text_by_path


def build_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_PACKET_RELATIVE_PATH: (
            render_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_md()
        ),
        HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUDIT_RELATIVE_PATH: (
            render_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_audit_md()
        ),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(
            f"S09 MES historical cost remaining blockers after exchange and NFA packet text for {relative_path}",
            text,
        )
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked(
                "S09 MES historical cost remaining blockers after exchange and NFA packet must not contain the retired window"
            )
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked(
                "S09 MES historical cost remaining blockers after exchange and NFA packet must not promote forbidden scope"
            )
        if COST_VALUE_LOCKED_STATUS in text:
            raise CarverBlocked(
                "S09 MES historical cost remaining blockers after exchange and NFA packet must not lock cost values"
            )
    artifact_text_by_path[HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_HASH_RELATIVE_PATH] = (
        _render_process_sha256_manifest(artifact_text_by_path)
    )
    return artifact_text_by_path


def build_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_ETF_PACKET_RELATIVE_PATH: (
            render_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_md()
        ),
        HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_ETF_AUDIT_RELATIVE_PATH: (
            render_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_audit_md()
        ),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(
            f"S09 MES historical cost remaining blockers after ETF packet text for {relative_path}",
            text,
        )
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES historical cost remaining blockers after ETF packet must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES historical cost remaining blockers after ETF packet must not promote forbidden scope")
        if COST_VALUE_LOCKED_STATUS in text:
            raise CarverBlocked("S09 MES historical cost remaining blockers after ETF packet must not lock cost values")
    artifact_text_by_path[HISTORICAL_COST_REMAINING_BLOCKERS_AFTER_ETF_HASH_RELATIVE_PATH] = (
        _render_process_sha256_manifest(artifact_text_by_path)
    )
    return artifact_text_by_path


def build_s09_mes_spread_slippage_source_or_policy_gate_result_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_RESULT_RELATIVE_PATH: (
            render_s09_mes_spread_slippage_source_or_policy_gate_result_md()
        ),
        SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_AUDIT_RELATIVE_PATH: (
            render_s09_mes_spread_slippage_source_or_policy_gate_audit_md()
        ),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES spread/slippage source-or-policy gate text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES spread/slippage gate result must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES spread/slippage gate result must not promote forbidden scope")
        if COST_VALUE_LOCKED_STATUS in text:
            raise CarverBlocked("S09 MES spread/slippage gate result must not lock cost values")
    artifact_text_by_path[SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_HASH_RELATIVE_PATH] = _render_process_sha256_manifest(
        artifact_text_by_path
    )
    return artifact_text_by_path


def build_s09_mes_official_lifecycle_evidence_artifact_contract_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        OFFICIAL_LIFECYCLE_CONTRACT_RELATIVE_PATH: render_s09_mes_official_lifecycle_evidence_artifact_contract_md(),
        OFFICIAL_LIFECYCLE_CONTRACT_AUDIT_RELATIVE_PATH: render_s09_mes_official_lifecycle_evidence_artifact_contract_audit_md(),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES official lifecycle artifact contract text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES official lifecycle artifact contract must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES official lifecycle artifact contract must not promote forbidden scope")
    artifact_text_by_path[OFFICIAL_LIFECYCLE_CONTRACT_HASH_RELATIVE_PATH] = _render_process_sha256_manifest(
        artifact_text_by_path
    )
    return artifact_text_by_path


def build_s09_mes_roll_trading_day_semantics_artifact_contract_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        ROLL_SEMANTICS_CONTRACT_RELATIVE_PATH: render_s09_mes_roll_trading_day_semantics_artifact_contract_md(),
        ROLL_SEMANTICS_CONTRACT_AUDIT_RELATIVE_PATH: render_s09_mes_roll_trading_day_semantics_artifact_contract_audit_md(),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES roll semantics artifact contract text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES roll semantics artifact contract must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES roll semantics artifact contract must not promote forbidden scope")
    artifact_text_by_path[ROLL_SEMANTICS_CONTRACT_HASH_RELATIVE_PATH] = _render_process_sha256_manifest(
        artifact_text_by_path
    )
    return artifact_text_by_path


def build_s09_mes_annual_risk_runtime_artifact_contract_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        ANNUAL_RISK_CONTRACT_RELATIVE_PATH: render_s09_mes_annual_risk_runtime_artifact_contract_md(),
        ANNUAL_RISK_CONTRACT_AUDIT_RELATIVE_PATH: render_s09_mes_annual_risk_runtime_artifact_contract_audit_md(),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES annual-risk artifact contract text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES annual-risk artifact contract must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES annual-risk artifact contract must not promote forbidden scope")
    artifact_text_by_path[ANNUAL_RISK_CONTRACT_HASH_RELATIVE_PATH] = _render_process_sha256_manifest(
        artifact_text_by_path
    )
    return artifact_text_by_path


def build_s09_mes_daily_price_risk_artifact_contract_bundle() -> dict[str, str]:
    artifact_text_by_path = {
        DAILY_PRICE_RISK_CONTRACT_RELATIVE_PATH: render_s09_mes_daily_price_risk_artifact_contract_md(),
        DAILY_PRICE_RISK_CONTRACT_AUDIT_RELATIVE_PATH: render_s09_mes_daily_price_risk_artifact_contract_audit_md(),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_process_relative_path(relative_path)
        _require_non_empty(f"S09 MES daily price-risk artifact contract text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES daily price-risk artifact contract must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES daily price-risk artifact contract must not promote forbidden scope")
    artifact_text_by_path[DAILY_PRICE_RISK_CONTRACT_HASH_RELATIVE_PATH] = _render_process_sha256_manifest(
        artifact_text_by_path
    )
    return artifact_text_by_path


def build_s09_mes_official_lifecycle_evidence_lock_bundle_from_local_metadata(
    config: S09MESOfficialLifecycleEvidenceLockConfig,
) -> dict[str, str]:
    _validate_official_lifecycle_evidence_lock_config(config)
    rows = _load_official_lifecycle_rows_from_local_metadata(Path(config.local_metadata_root).resolve())
    artifact_text_by_path = {
        OFFICIAL_LIFECYCLE_LEDGER_RELATIVE_PATH: render_s09_mes_strategy_input_evidence_completion_lifecycle_ledger_csv(rows),
        OFFICIAL_LIFECYCLE_STATUS_RELATIVE_PATH: render_s09_mes_official_lifecycle_evidence_lock_status_json(len(rows)),
        OFFICIAL_LIFECYCLE_PROVENANCE_RELATIVE_PATH: render_s09_mes_official_lifecycle_evidence_lock_provenance_md(rows),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES official lifecycle lock artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES official lifecycle lock artifacts must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES official lifecycle lock artifacts must not promote forbidden scope")
        if any(token in text for token in ("/roll/", "/risk/", "/cost/", "/speed/")):
            raise CarverBlocked("S09 MES official lifecycle lock artifacts must contain lifecycle scope only")
    artifact_text_by_path[OFFICIAL_LIFECYCLE_HASH_RELATIVE_PATH] = _render_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def write_s09_mes_official_lifecycle_evidence_lock_artifacts(
    *,
    execution_authorized: bool,
    bundle: dict[str, str],
    root: Path = ROOT,
) -> tuple[Path, ...]:
    if not execution_authorized:
        raise CarverBlocked("S09 MES official lifecycle evidence lock artifact write is not operator-authorized")
    root = Path(root).resolve()
    _validate_official_lifecycle_evidence_lock_bundle_for_write(bundle)
    return tuple(_write_text(root / relative_path, text) for relative_path, text in bundle.items())


def build_s09_mes_roll_trading_day_semantics_lock_bundle_from_local_roll_plan(
    config: S09MESRollTradingDaySemanticsLockConfig,
) -> dict[str, str]:
    _validate_roll_trading_day_semantics_lock_config(config)
    rows = _load_roll_trading_day_semantics_rows_from_local_roll_plan(Path(config.local_metadata_root).resolve())
    artifact_text_by_path = {
        ROLL_SEMANTICS_LEDGER_RELATIVE_PATH: render_s09_mes_strategy_input_evidence_completion_roll_semantics_ledger_csv(rows),
        ROLL_SEMANTICS_STATUS_RELATIVE_PATH: render_s09_mes_roll_trading_day_semantics_lock_status_json(len(rows)),
        ROLL_SEMANTICS_PROVENANCE_RELATIVE_PATH: render_s09_mes_roll_trading_day_semantics_lock_provenance_md(rows),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES roll semantics lock artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES roll semantics lock artifacts must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES roll semantics lock artifacts must not promote forbidden scope")
        if any(token in text for token in ("/risk/", "/cost/", "/speed/")):
            raise CarverBlocked("S09 MES roll semantics lock artifacts must contain roll scope only")
    artifact_text_by_path[ROLL_SEMANTICS_HASH_RELATIVE_PATH] = _render_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def write_s09_mes_roll_trading_day_semantics_lock_artifacts(
    *,
    execution_authorized: bool,
    bundle: dict[str, str],
    root: Path = ROOT,
) -> tuple[Path, ...]:
    if not execution_authorized:
        raise CarverBlocked("S09 MES roll semantics evidence lock artifact write is not operator-authorized")
    root = Path(root).resolve()
    _validate_roll_trading_day_semantics_lock_bundle_for_write(bundle)
    return tuple(_write_text(root / relative_path, text) for relative_path, text in bundle.items())


def build_s09_mes_annual_risk_runtime_values_lock_bundle_from_local_lineage(
    config: S09MESAnnualRiskRuntimeValuesLockConfig,
) -> dict[str, str]:
    _validate_annual_risk_runtime_values_lock_config(config)
    rows, source_sha256 = _load_annual_risk_runtime_rows_from_local_lineage(Path(config.local_metadata_root).resolve())
    artifact_text_by_path = {
        ANNUAL_RISK_LEDGER_RELATIVE_PATH: render_s09_mes_strategy_input_evidence_completion_annual_risk_ledger_csv(rows),
        ANNUAL_RISK_STATUS_RELATIVE_PATH: render_s09_mes_annual_risk_runtime_values_lock_status_json(len(rows)),
        ANNUAL_RISK_PROVENANCE_RELATIVE_PATH: render_s09_mes_annual_risk_runtime_values_lock_provenance_md(rows, source_sha256),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES annual-risk lock artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES annual-risk lock artifacts must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES annual-risk lock artifacts must not promote forbidden scope")
        if any(token in text for token in ("/cost/", "/speed/")):
            raise CarverBlocked("S09 MES annual-risk lock artifacts must contain annual-risk scope only")
    artifact_text_by_path[ANNUAL_RISK_HASH_RELATIVE_PATH] = _render_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def write_s09_mes_annual_risk_runtime_values_lock_artifacts(
    *,
    execution_authorized: bool,
    bundle: dict[str, str],
    root: Path = ROOT,
) -> tuple[Path, ...]:
    if not execution_authorized:
        raise CarverBlocked("S09 MES annual-risk evidence lock artifact write is not operator-authorized")
    root = Path(root).resolve()
    _validate_annual_risk_runtime_values_lock_bundle_for_write(bundle)
    return tuple(_write_text(root / relative_path, text) for relative_path, text in bundle.items())


def build_s09_mes_daily_price_risk_values_lock_bundle_from_locked_annual_risk(
    config: S09MESDailyPriceRiskValuesLockConfig,
) -> dict[str, str]:
    _validate_daily_price_risk_values_lock_config(config)
    rows, continuous_source_sha256, annual_risk_source_sha256, combined_source_sha256 = (
        _load_daily_price_risk_rows_from_locked_annual_risk(Path(config.local_metadata_root).resolve())
    )
    artifact_text_by_path = {
        DAILY_PRICE_RISK_LEDGER_RELATIVE_PATH: render_s09_mes_strategy_input_evidence_completion_daily_price_risk_ledger_csv(rows),
        DAILY_PRICE_RISK_STATUS_RELATIVE_PATH: render_s09_mes_daily_price_risk_values_lock_status_json(len(rows)),
        DAILY_PRICE_RISK_PROVENANCE_RELATIVE_PATH: render_s09_mes_daily_price_risk_values_lock_provenance_md(
            rows,
            continuous_source_sha256,
            annual_risk_source_sha256,
            combined_source_sha256,
        ),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES daily price-risk lock artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES daily price-risk lock artifacts must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES daily price-risk lock artifacts must not promote forbidden scope")
        if any(token in text for token in ("/cost/", "/speed/")):
            raise CarverBlocked("S09 MES daily price-risk lock artifacts must contain daily price-risk scope only")
    artifact_text_by_path[DAILY_PRICE_RISK_HASH_RELATIVE_PATH] = _render_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def write_s09_mes_daily_price_risk_values_lock_artifacts(
    *,
    execution_authorized: bool,
    bundle: dict[str, str],
    root: Path = ROOT,
) -> tuple[Path, ...]:
    if not execution_authorized:
        raise CarverBlocked("S09 MES daily price-risk evidence lock artifact write is not operator-authorized")
    root = Path(root).resolve()
    _validate_daily_price_risk_values_lock_bundle_for_write(bundle)
    return tuple(_write_text(root / relative_path, text) for relative_path, text in bundle.items())


def build_s09_mes_historical_mes_cost_values_fail_closed_bundle_from_active_evidence(
    config: S09MESHistoricalMESCostValuesAttemptConfig,
) -> dict[str, str]:
    _validate_historical_mes_cost_values_attempt_config(config)
    blocker = _inspect_active_historical_cost_ledger_for_fail_closed(Path(config.local_metadata_root).resolve())
    artifact_text_by_path = {
        HISTORICAL_COST_LEDGER_RELATIVE_PATH: _header_csv(COST_VALUE_LEDGER_COLUMNS),
        HISTORICAL_COST_STATUS_RELATIVE_PATH: render_s09_mes_historical_mes_cost_values_fail_closed_status_json(blocker),
        HISTORICAL_COST_PROVENANCE_RELATIVE_PATH: render_s09_mes_historical_mes_cost_values_fail_closed_provenance_md(blocker),
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES historical cost fail-closed artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES historical cost fail-closed artifacts must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES historical cost fail-closed artifacts must not promote forbidden scope")
        if "/speed/" in text:
            raise CarverBlocked("S09 MES historical cost fail-closed artifacts must contain cost scope only")
    artifact_text_by_path[HISTORICAL_COST_HASH_RELATIVE_PATH] = _render_sha256_manifest(artifact_text_by_path)
    return artifact_text_by_path


def write_s09_mes_historical_mes_cost_values_fail_closed_artifacts(
    *,
    execution_authorized: bool,
    bundle: dict[str, str],
    root: Path = ROOT,
) -> tuple[Path, ...]:
    if not execution_authorized:
        raise CarverBlocked("S09 MES historical cost fail-closed artifact write is not operator-authorized")
    root = Path(root).resolve()
    _validate_historical_mes_cost_values_fail_closed_bundle_for_write(bundle)
    return tuple(_write_text(root / relative_path, text) for relative_path, text in bundle.items())


def write_s09_mes_strategy_input_evidence_completion_artifacts(
    *,
    execution_authorized: bool,
    bundle: dict[str, str],
    root: Path = ROOT,
) -> tuple[Path, ...]:
    if not execution_authorized:
        raise CarverBlocked("S09 MES strategy-input evidence completion artifact write is not operator-authorized")
    root = Path(root).resolve()
    _validate_evidence_completion_bundle_for_write(bundle)
    written_artifact_paths = tuple(
        _write_text(root / relative_path, text)
        for relative_path, text in bundle.items()
        if "/hashes/" not in relative_path
    )
    status_path = root / f"{OUTPUT_ROOT_RELATIVE}/status/{RUN_ID}_status.json"
    provenance_path = root / f"{OUTPUT_ROOT_RELATIVE}/provenance/{RUN_ID}_provenance.md"
    result_path = _write_text(
        root / RESULT_RELATIVE_PATH,
        _render_result_text(root, status_path, provenance_path, written_artifact_paths),
    )
    audit_path = _write_text(
        root / AUDIT_RELATIVE_PATH,
        _render_audit_text(root, status_path, provenance_path, written_artifact_paths, result_path),
    )
    paths_without_hashes = (*written_artifact_paths, result_path, audit_path)
    hashes_path = _write_text(
        root / f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt",
        _render_written_sha256_manifest(root, paths_without_hashes),
    )
    return (*paths_without_hashes, hashes_path)


def _header_csv(columns: tuple[str, ...]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(columns)
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_required_evidence_ledger_csv() -> str:
    rows = tuple(
        (
            evidence_name,
            "LOCKED_SOURCE_NATIVE_EVIDENCE",
            EVIDENCE_NOT_LOCKED_STATUS,
            _blocking_reason_for_evidence(evidence_name),
            _next_action_for_evidence(evidence_name),
        )
        for evidence_name in REQUIRED_EVIDENCE_NAMES
    )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(EVIDENCE_LEDGER_COLUMNS)
    writer.writerows(rows)
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_partial_required_evidence_ledger_csv(
    locked_evidence_names: tuple[str, ...],
) -> str:
    _validate_partial_bookkeeping_locked_evidence_names(locked_evidence_names)
    locked = set(locked_evidence_names)
    rows = []
    for evidence_name in REQUIRED_EVIDENCE_NAMES:
        current_status = "LOCKED_SOURCE_NATIVE_EVIDENCE" if evidence_name in locked else EVIDENCE_NOT_LOCKED_STATUS
        if evidence_name in locked:
            blocking_reason = "Evidence family is locked from authorized source-native machinery-slice evidence."
            next_action = "Preserve locked evidence; continue to the next separately authorized evidence family."
        else:
            blocking_reason = _blocking_reason_for_evidence(evidence_name)
            next_action = _next_action_for_evidence(evidence_name)
        rows.append(
            (
                evidence_name,
                "LOCKED_SOURCE_NATIVE_EVIDENCE",
                current_status,
                blocking_reason,
                next_action,
            )
        )

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(EVIDENCE_LEDGER_COLUMNS)
    writer.writerows(rows)
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_partial_status_json(
    locked_evidence_names: tuple[str, ...],
) -> str:
    _validate_partial_bookkeeping_locked_evidence_names(locked_evidence_names)
    return json.dumps(
        {
            "backtests_run": "NO",
            "databento_api_access": "NO",
            "design_ordering": DESIGN_ORDERING,
            "diagnostics_run": "NO",
            "forecast_computation": "NO",
            "gate": GATE,
            "lane_class": LANE_CLASS,
            "locked_evidence_names": list(locked_evidence_names),
            "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
            "market_row_parsing": "NO",
            "new_provider_data_download": "NO",
            "remaining_evidence_count": len(REQUIRED_EVIDENCE_NAMES) - len(locked_evidence_names),
            "root": ROOT_SYMBOL,
            "row_id": ROW_ID,
            "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
            "status": EVIDENCE_COMPLETION_NOT_READY_STATUS,
            "strategy_input_readiness_status": STRATEGY_INPUT_NOT_READY_STATUS,
            "test_validation_lockbox_forward_access": "NO",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_strategy_input_evidence_completion_partial_provenance_md(
    locked_evidence_names: tuple[str, ...],
) -> str:
    _validate_partial_bookkeeping_locked_evidence_names(locked_evidence_names)
    locked_text = ", ".join(locked_evidence_names)
    return f"""# S09 MES Strategy Input Evidence Completion Partial Provenance

Status:

```text
{EVIDENCE_COMPLETION_NOT_READY_STATUS}
```

Scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Outcome:

This is partial evidence bookkeeping after an authorized source-native evidence
lock. The following evidence families are locked:

{locked_text}

The packet remains fail-closed for strategy input because the remaining evidence
families are not locked. No readiness, forecast, diagnostic, TEST, VALIDATION,
Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR,
or remote operation is authorized by this bookkeeping artifact.
"""


def render_s09_mes_strategy_input_evidence_completion_locked_evidence_ledger_csv() -> str:
    rows = tuple(
        (
            evidence_name,
            "LOCKED_SOURCE_NATIVE_EVIDENCE",
            "LOCKED_SOURCE_NATIVE_EVIDENCE",
            "Evidence supplied and renderer-validated by caller-provided locked rows.",
            "Proceed only to the separate strategy-input readiness gate; no backtest authorization is implied.",
        )
        for evidence_name in REQUIRED_EVIDENCE_NAMES
    )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(EVIDENCE_LEDGER_COLUMNS)
    writer.writerows(rows)
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_lifecycle_ledger_csv(
    rows: tuple[S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES lifecycle evidence ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(LIFECYCLE_LEDGER_COLUMNS)
    for row in rows:
        _validate_lifecycle_row(row)
        writer.writerow(
            (
                row.raw_symbol,
                row.first_completed_trading_date.isoformat(),
                row.last_completed_trading_date.isoformat(),
                row.expiration_completed_trading_date.isoformat(),
                row.source_label,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_roll_semantics_ledger_csv(
    rows: tuple[S09MESStrategyInputEvidenceCompletionRollSemanticsRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES roll semantics evidence ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(ROLL_SEMANTICS_LEDGER_COLUMNS)
    for row in rows:
        _validate_roll_semantics_row(row)
        writer.writerow(
            (
                row.old_symbol,
                row.new_symbol,
                row.provider_roll_date.isoformat(),
                row.completed_roll_date.isoformat(),
                row.source_label,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_annual_risk_ledger_csv(
    rows: tuple[S09MESStrategyInputEvidenceCompletionAnnualRiskRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES annual-risk evidence ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(ANNUAL_RISK_LEDGER_COLUMNS)
    for row in rows:
        _validate_annual_risk_row(row)
        writer.writerow(
            (
                row.completed_trading_date.isoformat(),
                row.long_run_annual_risk,
                row.current_ewma32_annual_risk,
                row.annual_percentage_risk,
                row.source_label,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_daily_price_risk_ledger_csv(
    rows: tuple[S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES daily price-risk evidence ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(DAILY_PRICE_RISK_LEDGER_COLUMNS)
    for row in rows:
        _validate_daily_price_risk_row(row)
        writer.writerow(
            (
                row.completed_trading_date.isoformat(),
                row.current_price,
                row.annual_percentage_risk,
                row.daily_price_risk_currency,
                row.source_label,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_cost_value_ledger_csv(
    rows: tuple[S09MESStrategyInputEvidenceCompletionCostValueRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES cost value evidence ledger requires at least one row")
    if tuple(row.component_name for row in rows) != REQUIRED_COST_COMPONENTS:
        raise CarverBlocked("S09 MES cost value evidence ledger must contain the complete locked cost component set")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(COST_VALUE_LEDGER_COLUMNS)
    for row in rows:
        _validate_cost_value_row(row)
        writer.writerow(
            (
                row.completed_trading_date.isoformat(),
                row.component_name,
                row.amount_currency,
                row.currency,
                row.charge_timing,
                row.effective_start.isoformat(),
                row.effective_end.isoformat(),
                row.source_label,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_risk_adjusted_cost_ledger_csv(
    rows: tuple[S09MESStrategyInputEvidenceCompletionRiskAdjustedCostRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES risk-adjusted cost evidence ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(RISK_ADJUSTED_COST_LEDGER_COLUMNS)
    for row in rows:
        _validate_risk_adjusted_cost_row(row)
        writer.writerow(
            (
                row.completed_trading_date.isoformat(),
                row.total_cost_per_trade_currency,
                row.daily_price_risk_currency,
                row.risk_adjusted_cost_per_trade_sr,
                row.source_label,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_speed_eligibility_ledger_csv(
    rows: tuple[S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES speed eligibility evidence ledger requires at least one row")
    if tuple(row.span for row in rows) != S09_EWMAC_SPANS:
        raise CarverBlocked("S09 MES speed eligibility evidence ledger must contain the complete locked EWMAC span set")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(SPEED_ELIGIBILITY_LEDGER_COLUMNS)
    for row in rows:
        _validate_speed_eligibility_row(row)
        writer.writerow(
            (
                row.span,
                row.turnover,
                row.risk_adjusted_cost_per_trade_sr,
                row.threshold_sr,
                row.eligible,
                row.source_label,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_eligible_speed_set_fdm_ledger_csv(
    rows: tuple[S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow, ...],
) -> str:
    if len(rows) != 1:
        raise CarverBlocked("S09 MES eligible speed set and FDM evidence ledger requires exactly one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(ELIGIBLE_SPEED_SET_FDM_LEDGER_COLUMNS)
    for row in rows:
        _validate_eligible_speed_set_fdm_row(row)
        writer.writerow(
            (
                _format_spans(row.eligible_spans),
                row.table36_fdm,
                row.source_label,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_strategy_input_evidence_completion_hash_manifest(
    entries: tuple[S09MESStrategyInputEvidenceCompletionHashManifestEntry, ...],
) -> str:
    if not entries:
        raise CarverBlocked("S09 MES strategy-input evidence completion SHA256 manifest requires at least one artifact")

    seen_paths: set[str] = set()
    lines: list[str] = []
    for entry in sorted(entries, key=lambda item: item.relative_path):
        _validate_hash_manifest_entry(entry)
        if entry.relative_path in seen_paths:
            raise CarverBlocked("S09 MES strategy-input evidence completion SHA256 manifest paths must be unique")
        seen_paths.add(entry.relative_path)
        digest = hashlib.sha256(entry.artifact_text.encode("utf-8")).hexdigest().upper()
        lines.append(f"{digest}  {entry.relative_path}")
    return "\n".join(lines) + "\n"


def render_s09_mes_strategy_input_evidence_completion_status_json() -> str:
    return json.dumps(
        {
            "backtests_run": "NO",
            "databento_api_access": "NO",
            "design_ordering": DESIGN_ORDERING,
            "diagnostics_run": "NO",
            "forecast_computation": "NO",
            "gate": GATE,
            "lane_class": LANE_CLASS,
            "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
            "market_row_parsing": "NO",
            "new_provider_data_download": "NO",
            "remaining_evidence_count": len(REQUIRED_EVIDENCE_NAMES),
            "root": ROOT_SYMBOL,
            "row_id": ROW_ID,
            "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
            "status": EVIDENCE_COMPLETION_NOT_READY_STATUS,
            "strategy_input_readiness_status": STRATEGY_INPUT_NOT_READY_STATUS,
            "test_validation_lockbox_forward_access": "NO",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_strategy_input_evidence_completion_locked_status_json() -> str:
    return json.dumps(
        {
            "backtests_run": "NO",
            "databento_api_access": "NO",
            "design_ordering": DESIGN_ORDERING,
            "diagnostics_run": "NO",
            "forecast_computation": "NO",
            "gate": GATE,
            "lane_class": LANE_CLASS,
            "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
            "market_row_parsing": "NO",
            "new_provider_data_download": "NO",
            "remaining_evidence_count": 0,
            "root": ROOT_SYMBOL,
            "row_id": ROW_ID,
            "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
            "status": EVIDENCE_COMPLETION_LOCKED_STATUS,
            "strategy_input_readiness_status": STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_STATUS,
            "test_validation_lockbox_forward_access": "NO",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_official_lifecycle_evidence_lock_status_json(row_count: int) -> str:
    if isinstance(row_count, bool) or row_count <= 0:
        raise CarverBlocked("S09 MES official lifecycle lock status requires at least one lifecycle row")
    return json.dumps(
        {
            "backtests_run": "NO",
            "cost_computation": "NO",
            "databento_api_access": "NO",
            "design_ordering": DESIGN_ORDERING,
            "diagnostics_run": "NO",
            "evidence_completion_status": EVIDENCE_COMPLETION_NOT_READY_STATUS,
            "forecast_computation": "NO",
            "gate": GATE,
            "git_operations": "NO",
            "lane_class": LANE_CLASS,
            "locked_lifecycle_rows": row_count,
            "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
            "market_row_parsing": "NO",
            "new_provider_data_download": "NO",
            "provider_login": "NO",
            "remaining_evidence_count": len(REQUIRED_EVIDENCE_NAMES) - 1,
            "risk_runtime_computation": "NO",
            "root": ROOT_SYMBOL,
            "row_id": ROW_ID,
            "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
            "selected_evidence_name": "official_lifecycle_evidence",
            "speed_eligibility_computation": "NO",
            "status": LIFECYCLE_LOCKED_STATUS,
            "strategy_input_readiness_status": STRATEGY_INPUT_NOT_READY_STATUS,
            "test_validation_lockbox_forward_access": "NO",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_roll_trading_day_semantics_lock_status_json(row_count: int) -> str:
    if isinstance(row_count, bool) or row_count <= 0:
        raise CarverBlocked("S09 MES roll semantics lock status requires at least one roll row")
    return json.dumps(
        {
            "backtests_run": "NO",
            "cost_computation": "NO",
            "databento_api_access": "NO",
            "design_ordering": DESIGN_ORDERING,
            "diagnostics_run": "NO",
            "evidence_completion_status": EVIDENCE_COMPLETION_NOT_READY_STATUS,
            "forecast_computation": "NO",
            "gate": GATE,
            "git_operations": "NO",
            "lane_class": LANE_CLASS,
            "locked_roll_semantics_rows": row_count,
            "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
            "market_row_parsing": "NO",
            "new_provider_data_download": "NO",
            "provider_login": "NO",
            "remaining_evidence_count": len(REQUIRED_EVIDENCE_NAMES) - 2,
            "risk_runtime_computation": "NO",
            "root": ROOT_SYMBOL,
            "row_id": ROW_ID,
            "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
            "selected_evidence_name": "roll_trading_day_semantics",
            "speed_eligibility_computation": "NO",
            "status": ROLL_SEMANTICS_LOCKED_STATUS,
            "strategy_input_readiness_status": STRATEGY_INPUT_NOT_READY_STATUS,
            "test_validation_lockbox_forward_access": "NO",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_annual_risk_runtime_values_lock_status_json(row_count: int) -> str:
    if isinstance(row_count, bool) or row_count <= 0:
        raise CarverBlocked("S09 MES annual-risk lock status requires at least one risk row")
    return json.dumps(
        {
            "annual_risk_runtime_computation": "YES_ANNUAL_RISK_ONLY",
            "annualization_days": int(ANNUAL_RISK_ANNUALIZATION_DAYS),
            "backtests_run": "NO",
            "cost_computation": "NO",
            "databento_api_access": "NO",
            "design_ordering": DESIGN_ORDERING,
            "diagnostics_run": "NO",
            "evidence_completion_status": EVIDENCE_COMPLETION_NOT_READY_STATUS,
            "ewma_span": ANNUAL_RISK_EWMA_SPAN,
            "forecast_computation": "NO",
            "gate": GATE,
            "git_operations": "NO",
            "lane_class": LANE_CLASS,
            "locked_annual_risk_rows": row_count,
            "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
            "market_row_parsing": "NO",
            "new_provider_data_download": "NO",
            "provider_login": "NO",
            "remaining_evidence_count": len(REQUIRED_EVIDENCE_NAMES) - 3,
            "root": ROOT_SYMBOL,
            "row_id": ROW_ID,
            "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
            "selected_evidence_name": "annual_risk_runtime_values",
            "speed_eligibility_computation": "NO",
            "status": ANNUAL_RISK_LOCKED_STATUS,
            "strategy_input_readiness_status": STRATEGY_INPUT_NOT_READY_STATUS,
            "test_validation_lockbox_forward_access": "NO",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_daily_price_risk_values_lock_status_json(row_count: int) -> str:
    if isinstance(row_count, bool) or row_count <= 0:
        raise CarverBlocked("S09 MES daily price-risk lock status requires at least one daily price-risk row")
    return json.dumps(
        {
            "backtests_run": "NO",
            "cost_computation": "NO",
            "daily_price_risk_computation": "YES_DAILY_PRICE_ONLY",
            "databento_api_access": "NO",
            "design_ordering": DESIGN_ORDERING,
            "diagnostics_run": "NO",
            "evidence_completion_status": EVIDENCE_COMPLETION_NOT_READY_STATUS,
            "forecast_computation": "NO",
            "gate": GATE,
            "git_operations": "NO",
            "lane_class": LANE_CLASS,
            "locked_daily_price_risk_rows": row_count,
            "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
            "market_row_parsing": "NO",
            "new_provider_data_download": "NO",
            "provider_login": "NO",
            "remaining_evidence_count": len(REQUIRED_EVIDENCE_NAMES) - 4,
            "risk_runtime_computation": "NO",
            "root": ROOT_SYMBOL,
            "row_id": ROW_ID,
            "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
            "selected_evidence_name": "daily_price_risk_values",
            "speed_eligibility_computation": "NO",
            "status": DAILY_PRICE_RISK_LOCKED_STATUS,
            "strategy_input_readiness_status": STRATEGY_INPUT_NOT_READY_STATUS,
            "test_validation_lockbox_forward_access": "NO",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_historical_mes_cost_values_fail_closed_status_json(blocker: str) -> str:
    _require_non_empty("S09 MES historical cost fail-closed blocker", blocker)
    return json.dumps(
        {
            "active_cost_evidence_observation": blocker,
            "backtests_run": "NO",
            "cost_computation": "NO",
            "databento_api_access": "NO",
            "design_ordering": DESIGN_ORDERING,
            "diagnostics_run": "NO",
            "evidence_completion_status": EVIDENCE_COMPLETION_NOT_READY_STATUS,
            "forecast_computation": "NO",
            "gate": GATE,
            "git_operations": "NO",
            "lane_class": LANE_CLASS,
            "locked_historical_cost_rows": 0,
            "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
            "market_row_parsing": "NO",
            "missing_cost_components": list(REQUIRED_COST_COMPONENTS),
            "new_provider_data_download": "NO",
            "provider_login": "NO",
            "remaining_evidence_count": len(REQUIRED_EVIDENCE_NAMES) - 4,
            "risk_runtime_computation": "NO",
            "root": ROOT_SYMBOL,
            "row_id": ROW_ID,
            "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
            "selected_evidence_name": "historical_mes_cost_values",
            "speed_eligibility_computation": "NO",
            "status": HISTORICAL_COST_FAIL_CLOSED_STATUS,
            "strategy_input_readiness_status": STRATEGY_INPUT_NOT_READY_STATUS,
            "test_validation_lockbox_forward_access": "NO",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_strategy_input_evidence_completion_provenance_md() -> str:
    return f"""# S09 MES Strategy Input Evidence Completion Provenance

Status:

```text
{EVIDENCE_COMPLETION_NOT_READY_STATUS}
```

Scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Outcome:

This is a header-only/preflight evidence completion bundle. It records the
source-native evidence still required before S09/MES can become strategy-input
ready. It does not parse market rows, compute risk, compute cost, compute
forecasts, run diagnostics, or run backtests.

Boundary:

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations were performed.
"""


def render_s09_mes_official_lifecycle_evidence_lock_provenance_md(
    rows: tuple[S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES official lifecycle provenance requires locked lifecycle rows")
    symbols = ", ".join(row.raw_symbol for row in rows)
    return f"""# S09 MES Official Lifecycle Evidence Lock Provenance

Status:

```text
{LIFECYCLE_LOCKED_STATUS}
```

Scope:

- gate: {GATE}
- selected_evidence_name: official_lifecycle_evidence
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Locked lifecycle symbols:

{symbols}

Source-native evidence basis:

- local provider definition metadata ledger:
  `{MACHINERY_DEV_MINIMUM_SLICE_DEFINITION_LEDGER_RELATIVE_PATH}`
- local lineage definition cross-check ledger:
  `{MACHINERY_DEV_LINEAGE_DEFINITION_CROSSCHECK_LEDGER_RELATIVE_PATH}`
- source SHA256 values are verified against the local definition CSV bytes

Boundary preserved:

This is official_lifecycle_evidence source-native evidence locking only. It does
not lock roll semantics, risk runtime values, daily price risk, historical cost
values, risk-adjusted cost, speed eligibility, eligible speed set, Table 36 FDM,
or global hash-bound strategy-input readiness.

no Databento API access, no provider login, no new provider download, no market-row parsing, no risk runtime computation, no cost computation, no speed eligibility computation, no forecast computation, no diagnostics, no returns, no PnL, no positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations were performed.
"""


def render_s09_mes_roll_trading_day_semantics_lock_provenance_md(
    rows: tuple[S09MESStrategyInputEvidenceCompletionRollSemanticsRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES roll semantics provenance requires locked roll rows")
    pairs = ", ".join(f"{row.old_symbol}->{row.new_symbol}" for row in rows)
    return f"""# S09 MES Roll Trading-Day Semantics Evidence Lock Provenance

Status:

```text
{ROLL_SEMANTICS_LOCKED_STATUS}
```

Scope:

- gate: {GATE}
- selected_evidence_name: roll_trading_day_semantics
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Locked roll pairs:

{pairs}

Source-native evidence basis:

- local machinery lineage roll plan:
  `{MACHINERY_DEV_LINEAGE_ROLL_PLAN_RELATIVE_PATH}`
- local machinery lineage SHA256 manifest:
  `{MACHINERY_DEV_LINEAGE_HASH_RELATIVE_PATH}`
- official lifecycle evidence ledger must already be locked before roll semantics lock

Boundary preserved:

This is roll_trading_day_semantics source-native evidence locking only. It does
not lock annual risk runtime values, daily price risk, historical cost values,
risk-adjusted cost, speed eligibility, eligible speed set, Table 36 FDM, or
global hash-bound strategy-input readiness.

no Databento API access, no provider login, no new provider download, no market-row parsing, no risk runtime computation, no cost computation, no speed eligibility computation, no forecast computation, no diagnostics, no returns, no PnL, no positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations were performed.
"""


def render_s09_mes_annual_risk_runtime_values_lock_provenance_md(
    rows: tuple[S09MESStrategyInputEvidenceCompletionAnnualRiskRow, ...],
    source_sha256: str,
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES annual-risk provenance requires locked annual-risk rows")
    _require_sha256("S09 MES annual-risk provenance source SHA256", source_sha256)
    first_date = rows[0].completed_trading_date.isoformat()
    last_date = rows[-1].completed_trading_date.isoformat()
    return f"""# S09 MES Annual-Risk Runtime Values Evidence Lock Provenance

Status:

```text
{ANNUAL_RISK_LOCKED_STATUS}
```

Scope:

- gate: {GATE}
- selected_evidence_name: annual_risk_runtime_values
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Locked annual-risk rows:

- row_count: {len(rows)}
- first_completed_trading_date: {first_date}
- last_completed_trading_date: {last_date}

Source-native evidence basis:

- local machinery-development continuous lineage:
  `{MACHINERY_DEV_LINEAGE_CONTINUOUS_SERIES_RELATIVE_PATH}`
- local machinery lineage SHA256 manifest:
  `{MACHINERY_DEV_LINEAGE_HASH_RELATIVE_PATH}`
- continuous lineage SHA256:
  `{source_sha256}`
- official lifecycle evidence and roll_trading_day_semantics evidence must already be locked

Runtime rule:

- current risk component: EWMA32 annualized percentage-return sigma
- long-run component: no-lookahead equal-weight annualized percentage-return RMS using history through each completed date
- annualization convention: 256 trading days
- blend: 30/70 long-run/current EWMA32 annual-risk blend
- completed bars only

Boundary preserved:

This is annual_risk_runtime_values source-native evidence locking only. It does
not lock daily price risk, historical cost values, risk-adjusted cost, speed
eligibility, eligible speed set, Table 36 FDM, or global hash-bound
strategy-input readiness.

no Databento API access, no provider login, no new provider download, no market-row parsing, no cost computation, no speed eligibility computation, no forecast computation, no diagnostics, no returns, no PnL, no positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations were performed.
"""


def render_s09_mes_daily_price_risk_values_lock_provenance_md(
    rows: tuple[S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow, ...],
    continuous_source_sha256: str,
    annual_risk_source_sha256: str,
    combined_source_sha256: str,
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES daily price-risk provenance requires locked daily price-risk rows")
    _require_sha256("S09 MES daily price-risk continuous source SHA256", continuous_source_sha256)
    _require_sha256("S09 MES daily price-risk annual-risk source SHA256", annual_risk_source_sha256)
    _require_sha256("S09 MES daily price-risk combined source SHA256", combined_source_sha256)
    first_date = rows[0].completed_trading_date.isoformat()
    last_date = rows[-1].completed_trading_date.isoformat()
    return f"""# S09 MES Daily Price-Risk Values Evidence Lock Provenance

Status:

```text
{DAILY_PRICE_RISK_LOCKED_STATUS}
```

Scope:

- gate: {GATE}
- selected_evidence_name: daily_price_risk_values
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Locked daily price-risk rows:

- row_count: {len(rows)}
- first_completed_trading_date: {first_date}
- last_completed_trading_date: {last_date}

Source-native evidence basis:

- local machinery-development continuous lineage:
  `{MACHINERY_DEV_LINEAGE_CONTINUOUS_SERIES_RELATIVE_PATH}`
- locked annual-risk runtime ledger:
  `{ANNUAL_RISK_LEDGER_RELATIVE_PATH}`
- continuous lineage SHA256:
  `{continuous_source_sha256}`
- annual-risk ledger SHA256:
  `{annual_risk_source_sha256}`
- combined daily-price source SHA256:
  `{combined_source_sha256}`
- official lifecycle evidence, roll_trading_day_semantics evidence, and annual_risk_runtime_values evidence must already be locked

Runtime rule:

- daily_price_risk_currency = current_price * annual_percentage_risk / 16
- current_price is the same completed-bar adjusted_close from local machinery lineage
- annual_percentage_risk is the same completed-bar locked annual-risk runtime value
- completed bars only

Boundary preserved:

This is daily_price_risk_values source-native evidence locking only. It does
not lock historical cost values, risk-adjusted cost, speed eligibility,
eligible speed set, Table 36 FDM, or global hash-bound strategy-input readiness.

no Databento API access, no provider login, no new provider download, no market-row parsing, no risk runtime computation, no cost computation, no speed eligibility computation, no forecast computation, no diagnostics, no returns, no PnL, no positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations were performed.
"""


def render_s09_mes_historical_mes_cost_values_fail_closed_provenance_md(blocker: str) -> str:
    _require_non_empty("S09 MES historical cost fail-closed provenance blocker", blocker)
    components = ", ".join(REQUIRED_COST_COMPONENTS)
    return f"""# S09 MES Historical MES Cost Values Evidence Attempt Provenance

Status:

```text
{HISTORICAL_COST_FAIL_CLOSED_STATUS}
```

Scope:

- gate: {GATE}
- selected_evidence_name: historical_mes_cost_values
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Outcome:

This is a historical_mes_cost_values authorized evidence attempt, not a cost
lock. The active cost ledger is header-only, so no source-native historical MES
cost component rows were locked.

Observed blocker:

- {blocker}

Required cost components still missing:

{components}

Boundary preserved:

No current-fee default, retired-window packet, broker assumption, spread/slippage
assumption, CFD adapter value, or old workspace state was promoted into this
machinery-development slice.

no Databento API access, no provider login, no new provider download, no market-row parsing, no risk runtime computation, no cost computation, no speed eligibility computation, no forecast computation, no diagnostics, no returns, no PnL, no positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations were performed.
"""


def render_s09_mes_strategy_input_evidence_completion_locked_provenance_md() -> str:
    return f"""# S09 MES Strategy Input Evidence Completion Locked Provenance

Status:

```text
{EVIDENCE_COMPLETION_LOCKED_STATUS}
```

Scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Outcome:

This in-memory packet contains caller-supplied locked evidence rows for all
required S09/MES strategy-input evidence families. It is a packaging and
validation handoff only. It does not authorize a Development/Reconciliation
backtest and does not access TEST, VALIDATION, OOS, Lockbox, or Forward data.

Boundary:

No Databento API access, provider download, market-row parsing, forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations were performed.
"""


def render_s09_mes_strategy_input_evidence_completion_readiness_handoff_json(
    request: S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest,
) -> str:
    _validate_readiness_handoff_request(request)
    return json.dumps(
        {
            "backtests_run": request.backtests_run,
            "databento_api_access": request.databento_api_access,
            "diagnostics_run": request.diagnostics_run,
            "evidence_completion_status": request.evidence_completion_status,
            "forecast_computation": request.forecast_computation,
            "handoff_status": "S09_MES_EVIDENCE_COMPLETION_HANDOFF_READY_FOR_READINESS_GATE_NOT_BACKTEST",
            "lane_class": request.lane_class,
            "machinery_development_slice": request.machinery_development_slice,
            "market_row_parsing": request.market_row_parsing,
            "next_gate": request.next_gate,
            "remaining_evidence_count": request.remaining_evidence_count,
            "root": request.root,
            "row_id": request.row_id,
            "strategy_input_readiness_status": request.strategy_input_readiness_status,
            "test_validation_lockbox_forward_access": request.test_validation_lockbox_forward_access,
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_strategy_input_evidence_completion_readiness_handoff_md(
    request: S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest,
) -> str:
    _validate_readiness_handoff_request(request)
    return f"""# S09 MES Strategy Input Evidence Completion Readiness Handoff

Status:

```text
S09_MES_EVIDENCE_COMPLETION_HANDOFF_READY_FOR_READINESS_GATE_NOT_BACKTEST
```

Scope:

- evidence_completion_status: {request.evidence_completion_status}
- strategy_input_readiness_status: {request.strategy_input_readiness_status}
- next_gate: {request.next_gate}
- lane_class: {request.lane_class}
- root: {request.root}
- row_id: {request.row_id}
- machinery_development_slice: {request.machinery_development_slice}

Outcome:

The evidence completion state is evidence locked; readiness gate next. This
handoff does not authorize Development/Reconciliation backtesting, diagnostics,
forecast computation, TEST, VALIDATION, OOS, Lockbox, Forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operations.

Boundary:

- Databento API access: {request.databento_api_access}
- market-row parsing: {request.market_row_parsing}
- forecast computation: {request.forecast_computation}
- diagnostics run: {request.diagnostics_run}
- backtests run: {request.backtests_run}
- TEST/VALIDATION/Lockbox/Forward access: {request.test_validation_lockbox_forward_access}
"""


def render_s09_mes_strategy_input_next_evidence_authorization_packet_md() -> str:
    evidence_rows = "\n".join(
        "- `{name}`: {reason} Next action: {action}".format(
            name=evidence_name,
            reason=_blocking_reason_for_evidence(evidence_name),
            action=_next_action_for_evidence(evidence_name),
        )
        for evidence_name in REQUIRED_EVIDENCE_NAMES
    )
    return f"""# S09 MES Strategy Input Next Evidence Authorization Packet

Date: 2026-06-03

Status:

```text
{NEXT_EVIDENCE_AUTHORIZATION_PACKET_STATUS}
```

Scope:

- gate_upstream: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}
- current_evidence_completion_status: {EVIDENCE_COMPLETION_NOT_READY_STATUS}
- remaining_evidence_count: {len(REQUIRED_EVIDENCE_NAMES)}

This packet is not authorization.

Purpose:

Prepare the next operator decision by listing the exact strategy-input
evidence families that still require source-native locking before S09/MES can
enter the separate strategy-input readiness gate.

Remaining evidence:

{evidence_rows}

Authorization boundary:

Each remaining evidence family requires separate explicit operator authorization
before any source access, source extraction, data access, market row parsing,
risk runtime computation, cost computation, speed eligibility computation, or
hash-bound evidence write is performed.

Non-authorization:

This packet performs:

- no Databento API access
- no provider login
- no new data download
- no market-row parsing
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_strategy_input_next_evidence_authorization_packet_audit_md() -> str:
    return f"""# S09 MES Strategy Input Next Evidence Authorization Packet Local Hostile Audit

Date: 2026-06-03

Status:

```text
{NEXT_EVIDENCE_AUTHORIZATION_PACKET_STATUS}
```

Audited helper:

```text
build_s09_mes_strategy_input_next_evidence_authorization_packet_bundle
```

Checks:

- packet is process-only and not authorization;
- evidence list is derived from the current required evidence names;
- remaining_evidence_count is {len(REQUIRED_EVIDENCE_NAMES)};
- machinery-development slice is {MACHINERY_DEVELOPMENT_SLICE_TEXT};
- lane remains {LANE_CLASS};
- root remains {ROOT_SYMBOL};
- row remains {ROW_ID};
- no Databento API access, market-row parsing, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers packet and audit only.

Result:

Fail-closed boundary preserved. The next executable stage remains blocked until
the operator explicitly authorizes the relevant evidence-source locking work.
"""


def render_s09_mes_strategy_input_selected_evidence_authorization_packet_md(
    preflight: dict[str, str],
) -> str:
    evidence_name = preflight["selected_evidence_name"]
    status = f"PROCESS_ONLY_S09_MES_STRATEGY_INPUT_{evidence_name.upper()}_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION"
    return f"""# S09 MES Strategy Input {evidence_name} Authorization Ready Packet

Date: 2026-06-03

Status:

```text
{status}
```

Scope:

- selected_evidence_name: {evidence_name}
- evidence_completion_status: {preflight["evidence_completion_status"]}
- remaining_evidence_count: {preflight["remaining_evidence_count"]}
- lane_class: {preflight["lane_class"]}
- root: {preflight["root"]}
- row_id: {preflight["row_id"]}
- machinery_development_slice: {preflight["machinery_development_slice"]}
- runtime_input_lock_scope: {preflight["runtime_input_lock_scope"]}
- design_ordering: {preflight["design_ordering"]}

This packet is not authorization.

Evidence family:

- blocking_reason: {preflight["blocking_reason"]}
- next_action: {preflight["next_action"]}

operator authorization wording:

Operator authorizes only `{evidence_name}` source-native evidence locking for
S09 MES Appendix C row `APPENDIX_C_174_006` on the machinery-development slice
`2019-05-05 through 2020-04-05`. This does not authorize any other evidence
family, forecast computation, diagnostics, backtests, TEST, VALIDATION,
Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push,
PR, or remote operations.

Non-authorization:

This packet performs:

- no Databento API access
- no provider login
- no new data download
- no market-row parsing
- no risk runtime computation
- no cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_strategy_input_selected_evidence_authorization_packet_audit_md(
    preflight: dict[str, str],
) -> str:
    evidence_name = preflight["selected_evidence_name"]
    status = f"PROCESS_ONLY_S09_MES_STRATEGY_INPUT_{evidence_name.upper()}_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION"
    return f"""# S09 MES Strategy Input {evidence_name} Authorization Ready Packet Local Hostile Audit

Date: 2026-06-03

Status:

```text
{status}
```

Audited helper:

```text
build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle
```

Checks:

- selected_evidence_name is {evidence_name};
- packet is process-only and not authorization;
- packet scopes exactly one evidence family;
- machinery-development slice is {preflight["machinery_development_slice"]};
- lane remains {preflight["lane_class"]};
- root remains {preflight["root"]};
- row remains {preflight["row_id"]};
- no Databento API access, market-row parsing, risk runtime computation, cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers selected packet and audit only.

Result:

Fail-closed selected-evidence boundary preserved. Execution remains blocked
until the operator explicitly authorizes this selected evidence family.
"""


def render_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_md() -> str:
    components = ", ".join(REQUIRED_COST_COMPONENTS)
    status = (
        "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_"
        "NOT_AUTHORIZATION_NOT_EXECUTION"
    )
    return f"""# S09 MES Historical MES Cost Source Acquisition Extraction Authorization Ready Packet

Date: 2026-06-03

Status:

```text
{status}
```

Scope:

- next_gate: source-native historical MES cost source acquisition/extraction
- selected_evidence_name: historical_mes_cost_values
- current_historical_cost_status: {HISTORICAL_COST_FAIL_CLOSED_STATUS}
- evidence_completion_status: {EVIDENCE_COMPLETION_NOT_READY_STATUS}
- remaining_evidence_count: {len(REQUIRED_EVIDENCE_NAMES) - 4}
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

This packet is not authorization.

Missing cost components:

{components}

Authorization wording:

Operator authorizes only source-native historical MES cost source
acquisition/extraction for S09 MES Appendix C row `APPENDIX_C_174_006` on the
machinery-development slice `2019-05-05 through 2020-04-05`. The execution may
locate, fetch, quote minimally, hash-bind, and summarize source-native cost
source material needed to determine whether exchange_fee,
clearing_regulatory_fee, broker_commission, and spread_slippage can be locked.

Non-authorization:

This packet performs:

- no Databento API access
- no provider login
- no web access
- no source extraction
- no market-row parsing
- no risk runtime computation
- no cost computation
- no risk-adjusted cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_audit_md() -> str:
    status = (
        "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_"
        "NOT_AUTHORIZATION_NOT_EXECUTION"
    )
    return f"""# S09 MES Historical MES Cost Source Acquisition Extraction Authorization Ready Packet Local Hostile Audit

Date: 2026-06-03

Status:

```text
{status}
```

Audited helper:

```text
build_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_bundle
```

Checks:

- packet is process-only and not authorization;
- packet identifies source-native historical MES cost source acquisition/extraction as the next gate;
- selected_evidence_name is historical_mes_cost_values;
- current status remains {HISTORICAL_COST_FAIL_CLOSED_STATUS};
- remaining_evidence_count is {len(REQUIRED_EVIDENCE_NAMES) - 4};
- machinery-development slice is {MACHINERY_DEVELOPMENT_SLICE_TEXT};
- lane remains {LANE_CLASS};
- root remains {ROOT_SYMBOL};
- row remains {ROW_ID};
- required components remain exchange_fee, clearing_regulatory_fee, broker_commission, and spread_slippage;
- no Databento API access, provider login, web access, source extraction, market-row parsing, risk runtime computation, cost computation, risk-adjusted cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized by this packet;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers packet and audit only;
- this packet must be reviewed by a spawned hostile-audit subagent before being treated as ready for operator use.

Result:

Fail-closed cost-source boundary preserved. Execution remains blocked until the
operator explicitly authorizes source-native historical MES cost source
acquisition/extraction.
"""


def render_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_md() -> str:
    status = "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION"
    return f"""# S09 MES Historical MES Cost Blocker Decision Authorization Ready Packet

Date: 2026-06-03

Status:

```text
{status}
```

Scope:

- next_gate: historical MES cost blocker decision
- selected_evidence_name: historical_mes_cost_values
- current_historical_cost_status: {HISTORICAL_COST_FAIL_CLOSED_STATUS}
- evidence_completion_status: {EVIDENCE_COMPLETION_NOT_READY_STATUS}
- remaining_evidence_count: {len(REQUIRED_EVIDENCE_NAMES) - 4}
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

This packet is not authorization.

No default choice is selected by this packet.

Open blocker decisions:

- official_cme_2019_fee_schedule_archive_permitted_route: operator may provide or authorize a permitted official CME 2019 fee schedule archive route before exchange_fee and clearing_regulatory_fee extraction.
- broker_commission_source_or_policy: operator may name a broker commission source, provide an official/contractual commission schedule, or explicitly authorize a fail-closed/no-broker-cost policy for this research lane.
- spread_slippage_source_or_policy: operator may name a source-native spread/slippage evidence source, provide an explicit conservative policy, or keep spread/slippage fail-closed.

Non-authorization:

This packet performs:

- no Databento API access
- no provider login
- no web access
- no source extraction
- no market-row parsing
- no risk runtime computation
- no cost computation
- no risk-adjusted cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_audit_md() -> str:
    status = "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION"
    return f"""# S09 MES Historical MES Cost Blocker Decision Authorization Ready Packet Local Hostile Audit

Date: 2026-06-03

Status:

```text
{status}
```

Audited helper:

```text
build_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_bundle
```

Checks:

- packet is process-only and not authorization;
- packet identifies historical MES cost blocker decision as the next gate;
- selected_evidence_name is historical_mes_cost_values;
- current status remains {HISTORICAL_COST_FAIL_CLOSED_STATUS};
- remaining_evidence_count is {len(REQUIRED_EVIDENCE_NAMES) - 4};
- no default decision is selected;
- blocker choices cover official_cme_2019_fee_schedule_archive_permitted_route, broker_commission_source_or_policy, and spread_slippage_source_or_policy;
- no cost component values are locked by this packet;
- no Databento API access, provider login, web access, source extraction, market-row parsing, risk runtime computation, cost computation, risk-adjusted cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers packet and audit only;
- this packet must be reviewed by a spawned hostile-audit subagent before being treated as ready for operator use.

Result:

Fail-closed cost-blocker boundary preserved. Execution remains blocked until
the operator explicitly chooses and authorizes one or more blocker-resolution
routes.
"""


def render_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_md() -> str:
    status = (
        "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_"
        "AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION"
    )
    return f"""# S09 MES Historical MES Cost Remaining Blockers After Exchange And NFA Authorization Ready Packet

Date: 2026-06-03

Status:

```text
{status}
```

Scope:

- next_gate: historical MES cost remaining blocker decision after exchange and NFA extraction
- selected_evidence_name: historical_mes_cost_values
- exchange_fee_value: PARTIAL_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
- clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
- historical_mes_cost_values: {HISTORICAL_COST_FAIL_CLOSED_STATUS}
- evidence_completion_status: {EVIDENCE_COMPLETION_NOT_READY_STATUS}
- remaining_evidence_count: {len(REQUIRED_EVIDENCE_NAMES) - 4}
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

This packet is not authorization.

No default choice is selected by this packet.

Current partial source state:

- exchange_fee_value: 0.20 USD per side extracted from official CME 2019 fee schedule archive rows for 2019 schedules only.
- clearing_regulatory_fee_value: 0.02 USD per side extracted from official NFA assessment-fee sources effective 2018-01-01.

Open remaining blocker decisions:

- broker_commission_source_or_policy: operator may name a broker/source, provide an official/contractual commission schedule, or explicitly authorize a selected-venue/static broker commission policy.
- spread_slippage_source_or_policy: operator may name a source-native spread/slippage evidence source, provide an explicit conservative policy, or keep spread/slippage fail-closed.
- official_cme_2020_fee_schedule_coverage_permitted_route: operator may provide or authorize a permitted official CME 2020 fee schedule coverage route for the 2020-01-01 through 2020-04-05 exchange-fee portion of the machinery-development slice.

Non-authorization:

This packet performs:

- no Databento API access
- no provider login
- no web access
- no source extraction
- no market-row parsing
- no risk runtime computation
- no cost computation
- no risk-adjusted cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_audit_md() -> str:
    status = (
        "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_"
        "AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION"
    )
    return f"""# S09 MES Historical MES Cost Remaining Blockers After Exchange And NFA Authorization Ready Packet Local Hostile Audit

Date: 2026-06-03

Status:

```text
{status}
```

Audited helper:

```text
build_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_bundle
```

Checks:

- packet is process-only and not authorization;
- packet identifies historical MES cost remaining blocker decision after exchange and NFA extraction as the next gate;
- selected_evidence_name is historical_mes_cost_values;
- exchange_fee and clearing/regulatory fee are marked partial source extractions only;
- current status remains {HISTORICAL_COST_FAIL_CLOSED_STATUS};
- remaining_evidence_count is {len(REQUIRED_EVIDENCE_NAMES) - 4};
- no default decision is selected;
- blocker choices cover broker_commission_source_or_policy, spread_slippage_source_or_policy, and official_cme_2020_fee_schedule_coverage_permitted_route;
- no cost component values are locked by this packet;
- no Databento API access, provider login, web access, source extraction, market-row parsing, risk runtime computation, cost computation, risk-adjusted cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers packet and audit only;
- this packet must be reviewed by a spawned hostile-audit subagent before being treated as ready for operator use.

Result:

Fail-closed cost-blocker boundary preserved. Execution remains blocked until
the operator explicitly chooses and authorizes remaining blocker-resolution
routes.
"""


def render_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_md() -> str:
    status = (
        "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_"
        "AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION"
    )
    return f"""# S09 MES Historical MES Cost Remaining Blockers After ETF Authorization Ready Packet

Date: 2026-06-03

Status:

```text
{status}
```

Scope:

- next_gate: historical MES cost remaining blocker decision after ETF selected broker fee extraction
- selected_evidence_name: historical_mes_cost_values
- exchange_fee_value: SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_FULL_MACHINERY_SLICE_NOT_FULL_COST_LOCK
- clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
- broker_commission_value: PARTIAL_SELECTED_BROKER_VENUE_CURRENT_MICRO_COMMISSION_SOURCE_EXTRACTED_NOT_FULL_COST_LOCK
- official_cme_2020_fee_schedule_coverage: PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED
- historical_mes_cost_values: {HISTORICAL_COST_FAIL_CLOSED_STATUS}
- evidence_completion_status: {EVIDENCE_COMPLETION_NOT_READY_STATUS}
- remaining_evidence_count: {len(REQUIRED_EVIDENCE_NAMES) - 4}
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

This packet is not authorization.

No default choice is selected by this packet.

Current partial source state:

- exchange_fee_value: 0.20 USD per side extracted from official CME 2019 and 2020 fee schedule archive rows covering the machinery-development slice.
- clearing_regulatory_fee_value: 0.02 USD per side extracted from official NFA assessment-fee sources effective 2018-01-01.
- Elite Trader Funding current micro fee source: 0.62 USD per side, captured as selected-broker-venue current evidence only.
- official_cme_2020_fee_schedule_coverage: PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED

Open remaining blocker decisions:

- broker_current_fee_static_historical_policy: operator may authorize whether the current Elite Trader Funding 0.62 USD per-side micro fee may be applied as a static selected-venue broker commission over the historical machinery-development slice.
- spread_slippage_source_or_policy: operator may name a source-native spread/slippage evidence source, provide an explicit conservative policy, or keep spread/slippage fail-closed.

Non-authorization:

This packet performs:

- no Databento API access
- no provider login
- no web access
- no source extraction
- no market-row parsing
- no risk runtime computation
- no cost computation
- no risk-adjusted cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_audit_md() -> str:
    status = (
        "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_"
        "AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION"
    )
    return f"""# S09 MES Historical MES Cost Remaining Blockers After ETF Authorization Ready Packet Local Hostile Audit

Date: 2026-06-03

Status:

```text
{status}
```

Audited helper:

```text
build_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_bundle
```

Checks:

- packet is process-only and not authorization;
- packet identifies historical MES cost remaining blocker decision after ETF selected broker fee extraction as the next gate;
- selected_evidence_name is historical_mes_cost_values;
- exchange_fee is marked source-extracted for the full machinery slice while clearing/regulatory fee and ETF broker fee are marked partial source extractions only;
- current status remains {HISTORICAL_COST_FAIL_CLOSED_STATUS};
- remaining_evidence_count is {len(REQUIRED_EVIDENCE_NAMES) - 4};
- no default decision is selected;
- blocker choices cover broker_current_fee_static_historical_policy and spread_slippage_source_or_policy;
- no cost component values are locked by this packet;
- no Databento API access, provider login, web access, source extraction, market-row parsing, risk runtime computation, cost computation, risk-adjusted cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers packet and audit only;
- this packet must be reviewed by a spawned hostile-audit subagent before being treated as ready for operator use.

Result:

Fail-closed cost-blocker boundary preserved. Execution remains blocked until
the operator explicitly chooses and authorizes remaining blocker-resolution
routes.
"""


def render_s09_mes_spread_slippage_source_or_policy_gate_result_md() -> str:
    status = "AUTHORIZED_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_OPENED_FAIL_CLOSED_NO_SOURCE_OR_POLICY_SELECTED"
    return f"""# S09 MES Spread Slippage Source Or Policy Gate Result

Date: 2026-06-03

Status:

```text
{status}
```

Authorized gate:

```text
spread_slippage_source_or_policy gate
```

Scope:

- operator_authorization: spread_slippage_source_or_policy gate
- selected_evidence_name: historical_mes_cost_values
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}
- exchange_fee_value: SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_FULL_MACHINERY_SLICE_NOT_FULL_COST_LOCK
- clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
- broker_commission_value: PARTIAL_SELECTED_BROKER_VENUE_CURRENT_MICRO_COMMISSION_SOURCE_EXTRACTED_NOT_FULL_COST_LOCK
- spread_slippage_policy: FAIL_CLOSED_S09_MES_SPREAD_SLIPPAGE_POLICY_NOT_LOCKED
- historical_mes_cost_values: {HISTORICAL_COST_FAIL_CLOSED_STATUS}
- evidence_completion_status: {EVIDENCE_COMPLETION_NOT_READY_STATUS}
- remaining_evidence_count: {len(REQUIRED_EVIDENCE_NAMES) - 4}

Gate outcome:

- spread_slippage_source_or_policy: no source-native spread/slippage source or explicit numeric conservative policy was selected by this authorization alone.
- no default one-tick, half-spread, full-spread, slippage, or market-impact assumption is selected.
- no old CFD, adapter, broker-clock, or QuantLab assumption is imported.
- spread/slippage remains fail-closed until the operator names a source-native source, provides an explicit numeric conservative policy, or authorizes keeping this component fail-closed.

Remaining blocker decisions:

- broker_current_fee_static_historical_policy: operator may authorize whether the current Elite Trader Funding 0.62 USD per-side micro fee may be applied as a static selected-venue broker commission over the historical machinery-development slice.
- spread_slippage_source_or_policy: operator may name a source-native spread/slippage evidence source, provide an explicit numeric conservative policy, or keep spread/slippage fail-closed.

Non-authorization:

This gate result performs:

- no Databento API access
- no provider login
- no web access
- no source extraction
- no market-row parsing
- no cost ledger rows
- no risk runtime computation
- no cost computation
- no risk-adjusted cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_spread_slippage_source_or_policy_gate_audit_md() -> str:
    status = "AUTHORIZED_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_OPENED_FAIL_CLOSED_NO_SOURCE_OR_POLICY_SELECTED"
    return f"""# S09 MES Spread Slippage Source Or Policy Gate Local Hostile Audit

Date: 2026-06-03

Status:

```text
{status}
```

Audited helper:

```text
build_s09_mes_spread_slippage_source_or_policy_gate_result_bundle
```

Checks:

- operator authorization is recorded as spread_slippage_source_or_policy gate;
- selected_evidence_name is historical_mes_cost_values;
- lane remains {LANE_CLASS};
- machinery-development slice remains {MACHINERY_DEVELOPMENT_SLICE_TEXT};
- spread_slippage_policy remains FAIL_CLOSED_S09_MES_SPREAD_SLIPPAGE_POLICY_NOT_LOCKED because no source-native source or explicit numeric conservative policy was selected by this authorization alone;
- current status remains {HISTORICAL_COST_FAIL_CLOSED_STATUS};
- remaining_evidence_count is {len(REQUIRED_EVIDENCE_NAMES) - 4};
- remaining blockers cover broker_current_fee_static_historical_policy and spread_slippage_source_or_policy;
- no default one-tick, half-spread, full-spread, slippage, or market-impact assumption is selected;
- no old CFD, adapter, broker-clock, or QuantLab assumption is imported;
- no cost component values are locked by this gate result;
- no Databento API access, provider login, web access, source extraction, market-row parsing, risk runtime computation, cost computation, risk-adjusted cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers result and local audit only;
- this gate result must be reviewed by a spawned hostile-audit subagent before being treated as ready for operator use.

Result:

Fail-closed spread/slippage boundary preserved. Execution remains blocked until
the operator explicitly chooses a source-native spread/slippage source, provides
an explicit numeric conservative policy, or authorizes keeping spread/slippage
fail-closed.
"""


def render_s09_mes_official_lifecycle_evidence_artifact_contract_md() -> str:
    lifecycle_path = (
        f"{OUTPUT_ROOT_RELATIVE}/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv"
    )
    lifecycle_schema = ",".join(LIFECYCLE_LEDGER_COLUMNS)
    return f"""# S09 MES Official Lifecycle Evidence Artifact Contract

Date: 2026-06-03

Status:

```text
{OFFICIAL_LIFECYCLE_CONTRACT_STATUS}
```

Scope:

- selected_evidence_name: official_lifecycle_evidence
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

This contract is not authorization and is not execution.

Required artifact:

- relative_path: `{lifecycle_path}`
- schema: `{lifecycle_schema}`
- required_status: `{LIFECYCLE_LOCKED_STATUS}`

Validation contract:

- completed bars only
- MES symbols only
- first_completed_trading_date <= last_completed_trading_date
- expiration_completed_trading_date > last_completed_trading_date
- source_label must be non-empty
- source_sha256 must be a valid SHA256 hex string
- status must equal `{LIFECYCLE_LOCKED_STATUS}`

Non-authorization:

This contract performs:

- no Databento API access
- no provider login
- no source extraction
- no new data download
- no market-row parsing
- no risk runtime computation
- no cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_official_lifecycle_evidence_artifact_contract_audit_md() -> str:
    return f"""# S09 MES Official Lifecycle Evidence Artifact Contract Local Hostile Audit

Date: 2026-06-03

Status:

```text
{OFFICIAL_LIFECYCLE_CONTRACT_STATUS}
```

Audited helper:

```text
build_s09_mes_official_lifecycle_evidence_artifact_contract_bundle
```

Checks:

- selected_evidence_name is official_lifecycle_evidence;
- contract is process-only and not authorization;
- output root stays under `{OUTPUT_ROOT_RELATIVE}`;
- schema is `{",".join(LIFECYCLE_LEDGER_COLUMNS)}`;
- required row status is `{LIFECYCLE_LOCKED_STATUS}`;
- completed bars only and MES symbols only are required;
- no Databento API access, provider login, source extraction, market-row parsing, risk runtime computation, cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers contract and audit only.

Result:

Fail-closed artifact contract recorded. Execution remains blocked until the
operator explicitly authorizes official_lifecycle_evidence source-native
evidence locking.
"""


def render_s09_mes_roll_trading_day_semantics_artifact_contract_md() -> str:
    roll_path = ROLL_SEMANTICS_LEDGER_RELATIVE_PATH
    roll_schema = ",".join(ROLL_SEMANTICS_LEDGER_COLUMNS)
    return f"""# S09 MES Roll Trading-Day Semantics Evidence Artifact Contract

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION
```

Scope:

- selected_evidence_name: roll_trading_day_semantics
- official_lifecycle_evidence_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- remaining_evidence_count: 9
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Contracted artifact:

- relative_path: `{roll_path}`
- schema: `{roll_schema}`
- required_status: `{ROLL_SEMANTICS_LOCKED_STATUS}`

Validation rules:

- completed bars only
- MES symbols only
- old_symbol and new_symbol must differ
- provider_roll_date must be exact source-native provider roll date
- completed_roll_date must be exact completed trading date
- completed_roll_date must not precede provider_roll_date
- source_label must be non-empty
- source_sha256 must be valid SHA256
- no duplicate old_symbol/new_symbol roll pairs

Non-authorization:

This contract performs:

- no Databento API access
- no provider login
- no source extraction
- no market-row parsing
- no risk runtime computation
- no cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_roll_trading_day_semantics_artifact_contract_audit_md() -> str:
    return f"""# S09 MES Roll Trading-Day Semantics Evidence Artifact Contract Local Hostile Audit

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION
```

Audited helper:

```text
build_s09_mes_roll_trading_day_semantics_artifact_contract_bundle
```

Checks:

- selected_evidence_name is roll_trading_day_semantics;
- official lifecycle evidence is assumed locked before this contract applies;
- remaining_evidence_count is 9;
- artifact path stays inside the S09 MES machinery-slice evidence-completion root;
- schema matches the roll semantics ledger renderer;
- status is {ROLL_SEMANTICS_LOCKED_STATUS};
- packet is process-only and not authorization;
- no Databento API access, provider login, source extraction, market-row parsing, risk runtime computation, cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers contract and audit only.

Result:

Fail-closed artifact contract recorded. Execution remains blocked until the
operator explicitly authorizes roll_trading_day_semantics source-native evidence
locking.
"""


def render_s09_mes_annual_risk_runtime_artifact_contract_md() -> str:
    annual_schema = ",".join(ANNUAL_RISK_LEDGER_COLUMNS)
    return f"""# S09 MES Annual-Risk Runtime Values Evidence Artifact Contract

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION
```

Scope:

- selected_evidence_name: annual_risk_runtime_values
- official_lifecycle_evidence_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- roll_trading_day_semantics_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- remaining_evidence_count: 8
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Contracted artifact:

- relative_path: `{ANNUAL_RISK_LEDGER_RELATIVE_PATH}`
- schema: `{annual_schema}`
- required_status: `{ANNUAL_RISK_LOCKED_STATUS}`

Validation rules:

- completed bars only
- completed_trading_date must be exact date values
- long_run_annual_risk must be finite and positive
- current_ewma32_annual_risk must be finite and positive
- annual_percentage_risk must equal the locked 30/70 annual-risk blend
- source_label must be non-empty
- source_sha256 must be valid SHA256
- status must equal `{ANNUAL_RISK_LOCKED_STATUS}`

Non-authorization:

This contract performs:

- no Databento API access
- no provider login
- no source extraction
- no market-row parsing
- no cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_annual_risk_runtime_artifact_contract_audit_md() -> str:
    return f"""# S09 MES Annual-Risk Runtime Values Evidence Artifact Contract Local Hostile Audit

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION
```

Audited helper:

```text
build_s09_mes_annual_risk_runtime_artifact_contract_bundle
```

Checks:

- selected_evidence_name is annual_risk_runtime_values;
- official lifecycle evidence and roll trading-day semantics are assumed locked before this contract applies;
- remaining_evidence_count is 8;
- artifact path stays inside the S09 MES machinery-slice evidence-completion root;
- schema matches the annual-risk ledger renderer;
- status is {ANNUAL_RISK_LOCKED_STATUS};
- packet is process-only and not authorization;
- no Databento API access, provider login, source extraction, market-row parsing, cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers contract and audit only.

Result:

Fail-closed artifact contract recorded. Execution remains blocked until the
operator explicitly authorizes annual_risk_runtime_values source-native
evidence locking.
"""


def render_s09_mes_daily_price_risk_artifact_contract_md() -> str:
    daily_schema = ",".join(DAILY_PRICE_RISK_LEDGER_COLUMNS)
    return f"""# S09 MES Daily Price-Risk Values Evidence Artifact Contract

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION
```

Scope:

- selected_evidence_name: daily_price_risk_values
- official_lifecycle_evidence_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- roll_trading_day_semantics_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- annual_risk_runtime_values_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- remaining_evidence_count: 7
- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Contracted artifact:

- relative_path: `{DAILY_PRICE_RISK_LEDGER_RELATIVE_PATH}`
- schema: `{daily_schema}`
- required_status: `{DAILY_PRICE_RISK_LOCKED_STATUS}`

Validation rules:

- completed bars only
- completed_trading_date must be exact date values
- current_price must be finite and positive
- annual_percentage_risk must be finite and positive
- annual_percentage_risk must come from a locked annual-risk runtime value on the same completed bar
- daily_price_risk_currency must equal current_price * annual_percentage_risk / 16
- source_label must be non-empty
- source_sha256 must be valid SHA256
- status must equal `{DAILY_PRICE_RISK_LOCKED_STATUS}`

Non-authorization:

This contract performs:

- no Databento API access
- no provider login
- no source extraction
- no market-row parsing
- no risk runtime computation
- no cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def render_s09_mes_daily_price_risk_artifact_contract_audit_md() -> str:
    return f"""# S09 MES Daily Price-Risk Values Evidence Artifact Contract Local Hostile Audit

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION
```

Audited helper:

```text
build_s09_mes_daily_price_risk_artifact_contract_bundle
```

Checks:

- selected_evidence_name is daily_price_risk_values;
- official lifecycle evidence, roll trading-day semantics, and annual-risk runtime values are assumed locked before this contract applies;
- remaining_evidence_count is 7;
- artifact path stays inside the S09 MES machinery-slice evidence-completion root;
- schema matches the daily price-risk ledger renderer;
- status is {DAILY_PRICE_RISK_LOCKED_STATUS};
- packet is process-only and not authorization;
- no Databento API access, provider login, source extraction, market-row parsing, risk runtime computation, cost computation, speed eligibility computation, forecast computation, diagnostics, or backtests are authorized;
- no TEST, VALIDATION, Lockbox, or Forward access is authorized;
- no Git staging, commit, push, PR, or remote operation is authorized;
- hash manifest covers contract and audit only.

Result:

Fail-closed artifact contract recorded. Execution remains blocked until the
operator explicitly authorizes daily_price_risk_values source-native evidence
locking.
"""


def _render_sha256_manifest(artifact_text_by_path: dict[str, str]) -> str:
    lines: list[str] = []
    for relative_path, artifact_text in sorted(artifact_text_by_path.items()):
        _require_evidence_completion_relative_path(relative_path)
        if "/hashes/" in relative_path:
            raise CarverBlocked("S09 MES evidence completion hash manifest must not include itself")
        digest = hashlib.sha256(artifact_text.encode("utf-8")).hexdigest().upper()
        lines.append(f"{digest}  {relative_path}")
    return "\n".join(lines) + "\n"


def _render_process_sha256_manifest(artifact_text_by_path: dict[str, str]) -> str:
    lines: list[str] = []
    for relative_path, artifact_text in sorted(artifact_text_by_path.items()):
        _require_process_relative_path(relative_path)
        if relative_path == NEXT_EVIDENCE_AUTHORIZATION_HASH_RELATIVE_PATH:
            raise CarverBlocked("S09 MES process packet hash manifest must not include itself")
        digest = hashlib.sha256(artifact_text.encode("utf-8")).hexdigest().upper()
        lines.append(f"{digest}  {relative_path}")
    return "\n".join(lines) + "\n"


def _validate_partial_bookkeeping_locked_evidence_names(locked_evidence_names: tuple[str, ...]) -> None:
    if locked_evidence_names not in (
        ("official_lifecycle_evidence",),
        ("official_lifecycle_evidence", "roll_trading_day_semantics"),
        ("official_lifecycle_evidence", "roll_trading_day_semantics", "annual_risk_runtime_values"),
        (
            "official_lifecycle_evidence",
            "roll_trading_day_semantics",
            "annual_risk_runtime_values",
            "daily_price_risk_values",
        ),
    ):
        raise CarverBlocked("S09 MES partial evidence bookkeeping has an unsupported locked evidence set")


def _validate_official_lifecycle_evidence_lock_config(
    config: S09MESOfficialLifecycleEvidenceLockConfig,
) -> None:
    if config.execution_authorized is not True:
        raise CarverBlocked("S09 MES official lifecycle evidence lock requires explicit operator authorization")
    if config.selected_evidence_name != "official_lifecycle_evidence":
        raise CarverBlocked("S09 MES official lifecycle evidence lock is scoped to one evidence family")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES official lifecycle evidence lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES official lifecycle evidence lock is locked to Appendix C MES")
    if config.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES official lifecycle evidence lock must use the oldest machinery-development slice")
    if config.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES official lifecycle evidence lock runtime scope is not locked")
    if config.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES official lifecycle evidence lock must preserve oldest-data-first ordering")
    for label, authorized in (
        ("Databento API access", config.databento_api_access_authorized),
        ("provider login", config.provider_login_authorized),
        ("market-row parsing", config.market_row_parsing_authorized),
        ("risk runtime computation", config.risk_runtime_computation_authorized),
        ("cost computation", config.cost_computation_authorized),
        ("speed eligibility computation", config.speed_eligibility_computation_authorized),
        ("forecast computation", config.forecast_computation_authorized),
        ("diagnostics", config.diagnostics_authorized),
        ("backtest", config.backtest_authorized),
        ("TEST/VALIDATION/Lockbox/Forward access", config.test_validation_lockbox_forward_authorized),
        ("Git operations", config.git_operations_authorized),
    ):
        if authorized is not False:
            raise CarverBlocked(f"S09 MES official lifecycle evidence lock forbids {label}")
    metadata_root = Path(config.local_metadata_root)
    if not metadata_root.exists() or not metadata_root.is_dir():
        raise CarverBlocked("S09 MES official lifecycle evidence lock local metadata root is missing")


def _validate_roll_trading_day_semantics_lock_config(
    config: S09MESRollTradingDaySemanticsLockConfig,
) -> None:
    if config.execution_authorized is not True:
        raise CarverBlocked("S09 MES roll semantics evidence lock requires explicit operator authorization")
    if config.selected_evidence_name != "roll_trading_day_semantics":
        raise CarverBlocked("S09 MES roll semantics evidence lock is scoped to one evidence family")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES roll semantics evidence lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES roll semantics evidence lock is locked to Appendix C MES")
    if config.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES roll semantics evidence lock must use the oldest machinery-development slice")
    if config.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES roll semantics evidence lock runtime scope is not locked")
    if config.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES roll semantics evidence lock must preserve oldest-data-first ordering")
    for label, authorized in (
        ("Databento API access", config.databento_api_access_authorized),
        ("provider login", config.provider_login_authorized),
        ("market-row parsing", config.market_row_parsing_authorized),
        ("risk runtime computation", config.risk_runtime_computation_authorized),
        ("cost computation", config.cost_computation_authorized),
        ("speed eligibility computation", config.speed_eligibility_computation_authorized),
        ("forecast computation", config.forecast_computation_authorized),
        ("diagnostics", config.diagnostics_authorized),
        ("backtest", config.backtest_authorized),
        ("TEST/VALIDATION/Lockbox/Forward access", config.test_validation_lockbox_forward_authorized),
        ("Git operations", config.git_operations_authorized),
    ):
        if authorized is not False:
            raise CarverBlocked(f"S09 MES roll semantics evidence lock forbids {label}")
    metadata_root = Path(config.local_metadata_root)
    if not metadata_root.exists() or not metadata_root.is_dir():
        raise CarverBlocked("S09 MES roll semantics evidence lock local metadata root is missing")


def _validate_annual_risk_runtime_values_lock_config(
    config: S09MESAnnualRiskRuntimeValuesLockConfig,
) -> None:
    if config.execution_authorized is not True:
        raise CarverBlocked("S09 MES annual-risk evidence lock requires explicit operator authorization")
    if config.selected_evidence_name != "annual_risk_runtime_values":
        raise CarverBlocked("S09 MES annual-risk evidence lock is scoped to one evidence family")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES annual-risk evidence lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES annual-risk evidence lock is locked to Appendix C MES")
    if config.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES annual-risk evidence lock must use the oldest machinery-development slice")
    if config.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES annual-risk evidence lock runtime scope is not locked")
    if config.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES annual-risk evidence lock must preserve oldest-data-first ordering")
    if config.annual_risk_runtime_computation_authorized is not True:
        raise CarverBlocked("S09 MES annual-risk evidence lock requires annual-risk runtime computation authorization")
    for label, authorized in (
        ("Databento API access", config.databento_api_access_authorized),
        ("provider login", config.provider_login_authorized),
        ("market-row parsing", config.market_row_parsing_authorized),
        ("cost computation", config.cost_computation_authorized),
        ("speed eligibility computation", config.speed_eligibility_computation_authorized),
        ("forecast computation", config.forecast_computation_authorized),
        ("diagnostics", config.diagnostics_authorized),
        ("backtest", config.backtest_authorized),
        ("TEST/VALIDATION/Lockbox/Forward access", config.test_validation_lockbox_forward_authorized),
        ("Git operations", config.git_operations_authorized),
    ):
        if authorized is not False:
            raise CarverBlocked(f"S09 MES annual-risk evidence lock forbids {label}")
    metadata_root = Path(config.local_metadata_root)
    if not metadata_root.exists() or not metadata_root.is_dir():
        raise CarverBlocked("S09 MES annual-risk evidence lock local metadata root is missing")


def _validate_daily_price_risk_values_lock_config(
    config: S09MESDailyPriceRiskValuesLockConfig,
) -> None:
    if config.execution_authorized is not True:
        raise CarverBlocked("S09 MES daily price-risk evidence lock requires explicit operator authorization")
    if config.selected_evidence_name != "daily_price_risk_values":
        raise CarverBlocked("S09 MES daily price-risk evidence lock is scoped to one evidence family")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES daily price-risk evidence lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES daily price-risk evidence lock is locked to Appendix C MES")
    if config.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES daily price-risk evidence lock must use the oldest machinery-development slice")
    if config.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES daily price-risk evidence lock runtime scope is not locked")
    if config.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES daily price-risk evidence lock must preserve oldest-data-first ordering")
    if config.daily_price_risk_computation_authorized is not True:
        raise CarverBlocked("S09 MES daily price-risk evidence lock requires daily price-risk computation authorization")
    for label, authorized in (
        ("Databento API access", config.databento_api_access_authorized),
        ("provider login", config.provider_login_authorized),
        ("market-row parsing", config.market_row_parsing_authorized),
        ("risk runtime computation", config.risk_runtime_computation_authorized),
        ("cost computation", config.cost_computation_authorized),
        ("speed eligibility computation", config.speed_eligibility_computation_authorized),
        ("forecast computation", config.forecast_computation_authorized),
        ("diagnostics", config.diagnostics_authorized),
        ("backtest", config.backtest_authorized),
        ("TEST/VALIDATION/Lockbox/Forward access", config.test_validation_lockbox_forward_authorized),
        ("Git operations", config.git_operations_authorized),
    ):
        if authorized is not False:
            raise CarverBlocked(f"S09 MES daily price-risk evidence lock forbids {label}")
    metadata_root = Path(config.local_metadata_root)
    if not metadata_root.exists() or not metadata_root.is_dir():
        raise CarverBlocked("S09 MES daily price-risk evidence lock local metadata root is missing")


def _validate_historical_mes_cost_values_attempt_config(
    config: S09MESHistoricalMESCostValuesAttemptConfig,
) -> None:
    if config.execution_authorized is not True:
        raise CarverBlocked("S09 MES historical cost evidence attempt requires explicit operator authorization")
    if config.selected_evidence_name != "historical_mes_cost_values":
        raise CarverBlocked("S09 MES historical cost evidence attempt is scoped to one evidence family")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES historical cost evidence attempt is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES historical cost evidence attempt is locked to Appendix C MES")
    if config.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES historical cost evidence attempt must use the oldest machinery-development slice")
    if config.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES historical cost evidence attempt runtime scope is not locked")
    if config.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES historical cost evidence attempt must preserve oldest-data-first ordering")
    if config.historical_cost_values_authorized is not True:
        raise CarverBlocked("S09 MES historical cost evidence attempt requires historical cost values authorization")
    for label, authorized in (
        ("Databento API access", config.databento_api_access_authorized),
        ("provider login", config.provider_login_authorized),
        ("market-row parsing", config.market_row_parsing_authorized),
        ("risk runtime computation", config.risk_runtime_computation_authorized),
        ("cost computation", config.cost_computation_authorized),
        ("speed eligibility computation", config.speed_eligibility_computation_authorized),
        ("forecast computation", config.forecast_computation_authorized),
        ("diagnostics", config.diagnostics_authorized),
        ("backtest", config.backtest_authorized),
        ("TEST/VALIDATION/Lockbox/Forward access", config.test_validation_lockbox_forward_authorized),
        ("Git operations", config.git_operations_authorized),
    ):
        if authorized is not False:
            raise CarverBlocked(f"S09 MES historical cost evidence attempt forbids {label}")
    metadata_root = Path(config.local_metadata_root)
    if not metadata_root.exists() or not metadata_root.is_dir():
        raise CarverBlocked("S09 MES historical cost evidence attempt local metadata root is missing")


def _load_official_lifecycle_rows_from_local_metadata(
    root: Path,
) -> tuple[S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow, ...]:
    definition_ledger_rows = _read_repo_csv_rows(root, MACHINERY_DEV_MINIMUM_SLICE_DEFINITION_LEDGER_RELATIVE_PATH)
    crosscheck_rows = _read_repo_csv_rows(root, MACHINERY_DEV_LINEAGE_DEFINITION_CROSSCHECK_LEDGER_RELATIVE_PATH)
    if not definition_ledger_rows or not crosscheck_rows:
        raise CarverBlocked("S09 MES official lifecycle evidence requires local definition ledgers")

    definition_ledger_by_symbol: dict[str, dict[str, str]] = {}
    for row in definition_ledger_rows:
        raw_symbol = row.get("raw_symbol", "")
        _require_mes_symbol("S09 MES lifecycle definition ledger raw symbol", raw_symbol)
        if raw_symbol in definition_ledger_by_symbol:
            raise CarverBlocked("S09 MES lifecycle definition ledger raw symbols must be unique")
        if row.get("definition_status") != "DATABENTO_DEFINITION_ROWS_PRESENT":
            raise CarverBlocked("S09 MES lifecycle definition ledger row is not present")
        _require_positive_integer_text("S09 MES lifecycle definition row count", row.get("definition_rows", ""))
        definition_ledger_by_symbol[raw_symbol] = row

    lifecycle_rows: list[S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow] = []
    seen_symbols: set[str] = set()
    for row in sorted(crosscheck_rows, key=lambda item: item.get("raw_symbol", "")):
        raw_symbol = row.get("raw_symbol", "")
        _require_mes_symbol("S09 MES lifecycle crosscheck raw symbol", raw_symbol)
        if raw_symbol in seen_symbols:
            raise CarverBlocked("S09 MES lifecycle crosscheck raw symbols must be unique")
        seen_symbols.add(raw_symbol)
        if raw_symbol not in definition_ledger_by_symbol:
            raise CarverBlocked("S09 MES lifecycle crosscheck symbol is missing from the definition ledger")
        if row.get("product_code") != ROOT_SYMBOL or row.get("currency") != "USD" or row.get("venue") != "XCME":
            raise CarverBlocked("S09 MES lifecycle crosscheck row is not locked to MES/USD/XCME")
        if row.get("multiplier") != "5.0" or row.get("tick_size") != "0.25":
            raise CarverBlocked("S09 MES lifecycle crosscheck row does not match MES multiplier/tick")
        if row.get("lifecycle_source_status") != "PROVIDER_DEFINITION_CROSSCHECK_ONLY_NOT_OFFICIAL_ROLL_SEMANTICS_LOCK":
            raise CarverBlocked("S09 MES lifecycle crosscheck row has unexpected source status")

        definition_csv_relative = _normalize_repo_relative_path(row.get("definition_csv", ""))
        ledger_csv_relative = _normalize_repo_relative_path(definition_ledger_by_symbol[raw_symbol].get("definition_csv", ""))
        if definition_csv_relative != ledger_csv_relative:
            raise CarverBlocked("S09 MES lifecycle definition ledger and crosscheck paths disagree")
        _require_source_native_metadata_relative_path(definition_csv_relative)
        definition_csv_path = root / definition_csv_relative
        if not definition_csv_path.exists() or not definition_csv_path.is_file():
            raise CarverBlocked("S09 MES lifecycle definition CSV is missing")
        expected_sha256 = row.get("definition_csv_sha256", "").upper()
        _require_sha256("S09 MES lifecycle definition CSV SHA256", expected_sha256)
        actual_sha256 = hashlib.sha256(definition_csv_path.read_bytes()).hexdigest().upper()
        if actual_sha256 != expected_sha256:
            raise CarverBlocked("S09 MES lifecycle definition CSV SHA256 mismatch")

        expiration_completed_date = _parse_date_prefix(row.get("expiration_utc", ""))
        first_completed_date, last_completed_date = _first_last_definition_metadata_dates(
            definition_csv_path,
            raw_symbol,
            expiration_completed_date,
        )
        lifecycle_rows.append(
            S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow(
                raw_symbol=raw_symbol,
                first_completed_trading_date=first_completed_date,
                last_completed_trading_date=last_completed_date,
                expiration_completed_trading_date=expiration_completed_date,
                source_label=f"LOCAL_DATABENTO_DEFINITION_CROSSCHECK_{raw_symbol}",
                source_sha256=expected_sha256,
                status=LIFECYCLE_LOCKED_STATUS,
            )
        )

    if not lifecycle_rows:
        raise CarverBlocked("S09 MES official lifecycle evidence requires at least one locked lifecycle row")
    return tuple(lifecycle_rows)


def _load_roll_trading_day_semantics_rows_from_local_roll_plan(
    root: Path,
) -> tuple[S09MESStrategyInputEvidenceCompletionRollSemanticsRow, ...]:
    lifecycle_rows = _read_repo_csv_rows(root, OFFICIAL_LIFECYCLE_LEDGER_RELATIVE_PATH)
    lifecycle_expiration_by_symbol: dict[str, date] = {}
    for row in lifecycle_rows:
        raw_symbol = row.get("raw_symbol", "")
        _require_mes_symbol("S09 MES roll semantics lifecycle raw symbol", raw_symbol)
        if row.get("status") != LIFECYCLE_LOCKED_STATUS:
            raise CarverBlocked("S09 MES roll semantics lock requires locked lifecycle evidence")
        lifecycle_expiration_by_symbol[raw_symbol] = _parse_date_prefix(row.get("expiration_completed_trading_date", ""))
    if not lifecycle_expiration_by_symbol:
        raise CarverBlocked("S09 MES roll semantics lock requires lifecycle rows")

    roll_plan_rows = _read_repo_csv_rows(root, MACHINERY_DEV_LINEAGE_ROLL_PLAN_RELATIVE_PATH)
    if not roll_plan_rows:
        raise CarverBlocked("S09 MES roll semantics lock requires local roll plan rows")
    roll_plan_sha256 = _verified_local_sha256_from_json_manifest(
        root,
        MACHINERY_DEV_LINEAGE_ROLL_PLAN_RELATIVE_PATH,
        MACHINERY_DEV_LINEAGE_HASH_RELATIVE_PATH,
    )

    locked_rows: list[S09MESStrategyInputEvidenceCompletionRollSemanticsRow] = []
    seen_pairs: set[tuple[str, str]] = set()
    for row in roll_plan_rows:
        old_symbol = row.get("old_symbol", "")
        new_symbol = row.get("new_symbol", "")
        _require_mes_symbol("S09 MES roll semantics old symbol", old_symbol)
        _require_mes_symbol("S09 MES roll semantics new symbol", new_symbol)
        if old_symbol == new_symbol:
            raise CarverBlocked("S09 MES roll semantics old and new symbols must differ")
        pair = (old_symbol, new_symbol)
        if pair in seen_pairs:
            raise CarverBlocked("S09 MES roll semantics roll pairs must be unique")
        seen_pairs.add(pair)
        if old_symbol not in lifecycle_expiration_by_symbol or new_symbol not in lifecycle_expiration_by_symbol:
            raise CarverBlocked("S09 MES roll semantics symbols must be covered by locked lifecycle evidence")
        if row.get("roll_rule") != "STATIC_LIFECYCLE_BUFFER_ROLL_5_PROVIDER_DATES_MACHINERY_ONLY":
            raise CarverBlocked("S09 MES roll semantics row has unexpected roll rule")
        if row.get("adjustment_method") != "LOCAL_ADDITIVE_BACK_ADJUSTMENT_NOT_STRATEGY_INPUT":
            raise CarverBlocked("S09 MES roll semantics row has unexpected adjustment method")
        _require_sha256("S09 MES roll semantics old source SHA256", row.get("old_source_raw_sha256", ""))
        _require_sha256("S09 MES roll semantics new source SHA256", row.get("new_source_raw_sha256", ""))
        expiration_date = _parse_date_prefix(row.get("expiration_date", ""))
        if expiration_date != lifecycle_expiration_by_symbol[old_symbol]:
            raise CarverBlocked("S09 MES roll semantics expiration disagrees with locked lifecycle evidence")
        provider_roll_date = _parse_date_prefix(row.get("roll_transition_date", ""))
        if _parse_date_prefix(row.get("roll_buffer_date", "")) != provider_roll_date:
            raise CarverBlocked("S09 MES roll semantics roll buffer and transition dates disagree")
        completed_roll_date = _completed_trading_date_for_provider_roll_date(provider_roll_date)
        if completed_roll_date >= expiration_date:
            raise CarverBlocked("S09 MES roll semantics completed roll date must precede expiration")
        locked_rows.append(
            S09MESStrategyInputEvidenceCompletionRollSemanticsRow(
                old_symbol=old_symbol,
                new_symbol=new_symbol,
                provider_roll_date=provider_roll_date,
                completed_roll_date=completed_roll_date,
                source_label="LOCAL_MACHINERY_DEV_ROLL_PLAN_COMPLETED_BAR_NORMALIZATION",
                source_sha256=roll_plan_sha256,
                status=ROLL_SEMANTICS_LOCKED_STATUS,
            )
        )

    return tuple(locked_rows)


def _load_annual_risk_runtime_rows_from_local_lineage(
    root: Path,
) -> tuple[tuple[S09MESStrategyInputEvidenceCompletionAnnualRiskRow, ...], str]:
    lifecycle_rows = _read_repo_csv_rows(root, OFFICIAL_LIFECYCLE_LEDGER_RELATIVE_PATH)
    if not lifecycle_rows or any(row.get("status") != LIFECYCLE_LOCKED_STATUS for row in lifecycle_rows):
        raise CarverBlocked("S09 MES annual-risk lock requires locked lifecycle evidence")
    roll_rows = _read_repo_csv_rows(root, ROLL_SEMANTICS_LEDGER_RELATIVE_PATH)
    if not roll_rows or any(row.get("status") != ROLL_SEMANTICS_LOCKED_STATUS for row in roll_rows):
        raise CarverBlocked("S09 MES annual-risk lock requires locked roll semantics evidence")

    source_sha256 = _verified_local_sha256_from_json_manifest(
        root,
        MACHINERY_DEV_LINEAGE_CONTINUOUS_SERIES_RELATIVE_PATH,
        MACHINERY_DEV_LINEAGE_HASH_RELATIVE_PATH,
    )
    source_rows = _read_repo_csv_rows(root, MACHINERY_DEV_LINEAGE_CONTINUOUS_SERIES_RELATIVE_PATH)
    if len(source_rows) < ANNUAL_RISK_WINDOW_ROWS:
        raise CarverBlocked("S09 MES annual-risk runtime requires enough continuous rows for EWMA32")

    start = date.fromisoformat(MACHINERY_DEVELOPMENT_SLICE_START)
    end = date.fromisoformat(MACHINERY_DEVELOPMENT_SLICE_END)
    parsed_rows: list[tuple[date, float]] = []
    seen_dates: set[date] = set()
    previous_date: date | None = None
    for row in source_rows:
        completed_date = _parse_date_prefix(row.get("completed_trading_date", ""))
        if completed_date < start or completed_date > end:
            raise CarverBlocked("S09 MES annual-risk continuous row is outside the machinery slice")
        if previous_date is not None and completed_date <= previous_date:
            raise CarverBlocked("S09 MES annual-risk continuous rows must be oldest-first and unique")
        previous_date = completed_date
        if completed_date in seen_dates:
            raise CarverBlocked("S09 MES annual-risk continuous rows must not duplicate dates")
        seen_dates.add(completed_date)
        _require_mes_symbol("S09 MES annual-risk continuous source symbol", row.get("source_raw_symbol", ""))
        _require_sha256("S09 MES annual-risk continuous source raw SHA256", row.get("source_raw_sha256", ""))
        if row.get("lineage_status") != "PROVISIONAL_LOCAL_MACHINERY_LINEAGE_NOT_STRATEGY_INPUT":
            raise CarverBlocked("S09 MES annual-risk continuous lineage row has unexpected status")
        adjusted_close = _parse_positive_float("S09 MES annual-risk adjusted close", row.get("adjusted_close", ""))
        parsed_rows.append((completed_date, adjusted_close))

    if len(parsed_rows) < ANNUAL_RISK_WINDOW_ROWS:
        raise CarverBlocked("S09 MES annual-risk runtime requires enough parsed continuous rows for EWMA32")

    returns = [
        (parsed_rows[index][1] / parsed_rows[index - 1][1]) - 1.0
        for index in range(1, len(parsed_rows))
    ]
    locked_rows: list[S09MESStrategyInputEvidenceCompletionAnnualRiskRow] = []
    alpha = 2.0 / (ANNUAL_RISK_EWMA_SPAN + 1.0)
    for index in range(ANNUAL_RISK_WINDOW_ROWS - 1, len(parsed_rows)):
        window_returns = returns[index - (ANNUAL_RISK_WINDOW_ROWS - 1) : index]
        if len(window_returns) != ANNUAL_RISK_EWMA_SPAN:
            raise CarverBlocked("S09 MES annual-risk EWMA window has unexpected size")
        variance = window_returns[0] * window_returns[0]
        for value in window_returns[1:]:
            variance = alpha * value * value + (1.0 - alpha) * variance
        current_ewma32 = math.sqrt(variance) * math.sqrt(ANNUAL_RISK_ANNUALIZATION_DAYS)

        long_run_returns = returns[:index]
        long_run_variance = sum(value * value for value in long_run_returns) / len(long_run_returns)
        long_run = math.sqrt(long_run_variance) * math.sqrt(ANNUAL_RISK_ANNUALIZATION_DAYS)
        annual_risk = ANNUAL_RISK_LONG_RUN_WEIGHT * long_run + ANNUAL_RISK_CURRENT_WEIGHT * current_ewma32
        locked_rows.append(
            S09MESStrategyInputEvidenceCompletionAnnualRiskRow(
                completed_trading_date=parsed_rows[index][0],
                long_run_annual_risk=long_run,
                current_ewma32_annual_risk=current_ewma32,
                annual_percentage_risk=annual_risk,
                source_label="LOCAL_MACHINERY_DEV_CONTINUOUS_LINEAGE_EWMA32_ANNUAL_RISK",
                source_sha256=source_sha256,
                status=ANNUAL_RISK_LOCKED_STATUS,
            )
        )

    if not locked_rows:
        raise CarverBlocked("S09 MES annual-risk runtime produced no locked rows")
    return tuple(locked_rows), source_sha256


def _load_daily_price_risk_rows_from_locked_annual_risk(
    root: Path,
) -> tuple[tuple[S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow, ...], str, str, str]:
    lifecycle_rows = _read_repo_csv_rows(root, OFFICIAL_LIFECYCLE_LEDGER_RELATIVE_PATH)
    if not lifecycle_rows or any(row.get("status") != LIFECYCLE_LOCKED_STATUS for row in lifecycle_rows):
        raise CarverBlocked("S09 MES daily price-risk lock requires locked lifecycle evidence")
    roll_rows = _read_repo_csv_rows(root, ROLL_SEMANTICS_LEDGER_RELATIVE_PATH)
    if not roll_rows or any(row.get("status") != ROLL_SEMANTICS_LOCKED_STATUS for row in roll_rows):
        raise CarverBlocked("S09 MES daily price-risk lock requires locked roll semantics evidence")
    annual_rows = _read_repo_csv_rows(root, ANNUAL_RISK_LEDGER_RELATIVE_PATH)
    if not annual_rows:
        raise CarverBlocked("S09 MES daily price-risk lock requires locked annual-risk evidence")

    continuous_source_sha256 = _verified_local_sha256_from_json_manifest(
        root,
        MACHINERY_DEV_LINEAGE_CONTINUOUS_SERIES_RELATIVE_PATH,
        MACHINERY_DEV_LINEAGE_HASH_RELATIVE_PATH,
    )
    annual_risk_source_sha256 = hashlib.sha256(
        (root / _normalize_repo_relative_path(ANNUAL_RISK_LEDGER_RELATIVE_PATH)).read_bytes()
    ).hexdigest().upper()
    combined_source_sha256 = hashlib.sha256(
        (continuous_source_sha256 + annual_risk_source_sha256).encode("utf-8")
    ).hexdigest().upper()

    continuous_price_by_date = _load_continuous_adjusted_close_by_completed_date(root)
    locked_rows: list[S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow] = []
    seen_dates: set[date] = set()
    previous_date: date | None = None
    for row in annual_rows:
        completed_date = _parse_date_prefix(row.get("completed_trading_date", ""))
        if previous_date is not None and completed_date <= previous_date:
            raise CarverBlocked("S09 MES daily price-risk annual-risk rows must be oldest-first and unique")
        previous_date = completed_date
        if completed_date in seen_dates:
            raise CarverBlocked("S09 MES daily price-risk annual-risk rows must not duplicate dates")
        seen_dates.add(completed_date)
        if row.get("status") != ANNUAL_RISK_LOCKED_STATUS:
            raise CarverBlocked("S09 MES daily price-risk lock requires locked annual-risk rows")
        annual_percentage_risk = _parse_positive_float(
            "S09 MES daily price-risk annual percentage risk",
            row.get("annual_percentage_risk", ""),
        )
        current_price = continuous_price_by_date.get(completed_date)
        if current_price is None:
            raise CarverBlocked("S09 MES daily price-risk current price is missing for annual-risk date")
        daily_price_risk = current_price * annual_percentage_risk / 16
        locked_rows.append(
            S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow(
                completed_trading_date=completed_date,
                current_price=current_price,
                annual_percentage_risk=annual_percentage_risk,
                daily_price_risk_currency=daily_price_risk,
                source_label="LOCAL_MACHINERY_DEV_CONTINUOUS_LINEAGE_AND_ANNUAL_RISK_DAILY_PRICE_RISK",
                source_sha256=combined_source_sha256,
                status=DAILY_PRICE_RISK_LOCKED_STATUS,
            )
        )

    if not locked_rows:
        raise CarverBlocked("S09 MES daily price-risk runtime produced no locked rows")
    return tuple(locked_rows), continuous_source_sha256, annual_risk_source_sha256, combined_source_sha256


def _load_continuous_adjusted_close_by_completed_date(root: Path) -> dict[date, float]:
    source_rows = _read_repo_csv_rows(root, MACHINERY_DEV_LINEAGE_CONTINUOUS_SERIES_RELATIVE_PATH)
    if not source_rows:
        raise CarverBlocked("S09 MES daily price-risk requires local continuous rows")
    start = date.fromisoformat(MACHINERY_DEVELOPMENT_SLICE_START)
    end = date.fromisoformat(MACHINERY_DEVELOPMENT_SLICE_END)
    prices: dict[date, float] = {}
    previous_date: date | None = None
    for row in source_rows:
        completed_date = _parse_date_prefix(row.get("completed_trading_date", ""))
        if completed_date < start or completed_date > end:
            raise CarverBlocked("S09 MES daily price-risk continuous row is outside the machinery slice")
        if previous_date is not None and completed_date <= previous_date:
            raise CarverBlocked("S09 MES daily price-risk continuous rows must be oldest-first and unique")
        previous_date = completed_date
        _require_mes_symbol("S09 MES daily price-risk continuous source symbol", row.get("source_raw_symbol", ""))
        _require_sha256("S09 MES daily price-risk continuous source raw SHA256", row.get("source_raw_sha256", ""))
        if row.get("lineage_status") != "PROVISIONAL_LOCAL_MACHINERY_LINEAGE_NOT_STRATEGY_INPUT":
            raise CarverBlocked("S09 MES daily price-risk continuous lineage row has unexpected status")
        prices[completed_date] = _parse_positive_float(
            "S09 MES daily price-risk current price",
            row.get("adjusted_close", ""),
        )
    return prices


def _read_repo_csv_rows(root: Path, relative_path: str) -> list[dict[str, str]]:
    normalized = _normalize_repo_relative_path(relative_path)
    path = root / normalized
    if not path.exists() or not path.is_file():
        raise CarverBlocked("S09 MES local metadata CSV is missing")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise CarverBlocked("S09 MES local metadata CSV is missing a header")
        return [dict(row) for row in reader]


def _first_last_definition_metadata_dates(path: Path, raw_symbol: str, expiration_completed_date: date) -> tuple[date, date]:
    rows = _read_absolute_csv_rows(path)
    dates: list[date] = []
    for row in rows:
        if row.get("raw_symbol") not in ("", raw_symbol) and row.get("symbol") not in ("", raw_symbol):
            raise CarverBlocked("S09 MES lifecycle definition CSV contains a foreign symbol")
        row_expiration = row.get("expiration", "")
        if row_expiration:
            if _parse_date_prefix(row_expiration) != expiration_completed_date:
                raise CarverBlocked("S09 MES lifecycle definition CSV expiration disagrees with crosscheck ledger")
        ts_recv = row.get("ts_recv", "")
        if not ts_recv:
            raise CarverBlocked("S09 MES lifecycle definition CSV is missing ts_recv metadata")
        completed_date = _parse_date_prefix(ts_recv)
        if completed_date < date.fromisoformat(MACHINERY_DEVELOPMENT_SLICE_START):
            raise CarverBlocked("S09 MES lifecycle definition metadata predates the machinery slice")
        if completed_date > date.fromisoformat(MACHINERY_DEVELOPMENT_SLICE_END):
            raise CarverBlocked("S09 MES lifecycle definition metadata exceeds the machinery slice")
        dates.append(completed_date)
    if not dates:
        raise CarverBlocked("S09 MES lifecycle definition CSV has no metadata rows")
    usable_dates = tuple(sorted(day for day in set(dates) if day < expiration_completed_date))
    if not usable_dates:
        raise CarverBlocked("S09 MES lifecycle definition CSV has no completed date before expiration")
    return usable_dates[0], usable_dates[-1]


def _read_absolute_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise CarverBlocked("S09 MES local metadata CSV is missing a header")
        return [dict(row) for row in reader]


def _validate_official_lifecycle_evidence_lock_bundle_for_write(bundle: dict[str, str]) -> None:
    expected_paths = (
        OFFICIAL_LIFECYCLE_LEDGER_RELATIVE_PATH,
        OFFICIAL_LIFECYCLE_STATUS_RELATIVE_PATH,
        OFFICIAL_LIFECYCLE_PROVENANCE_RELATIVE_PATH,
        OFFICIAL_LIFECYCLE_HASH_RELATIVE_PATH,
    )
    if tuple(bundle) != expected_paths:
        raise CarverBlocked("S09 MES official lifecycle evidence lock write bundle has unexpected paths")
    for relative_path, text in bundle.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES official lifecycle lock artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES official lifecycle lock write bundle must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES official lifecycle lock write bundle must not promote forbidden scope")
    expected_manifest = _render_sha256_manifest({path: bundle[path] for path in expected_paths[:-1]})
    if bundle[OFFICIAL_LIFECYCLE_HASH_RELATIVE_PATH] != expected_manifest:
        raise CarverBlocked("S09 MES official lifecycle evidence lock SHA256 manifest is invalid")


def _validate_roll_trading_day_semantics_lock_bundle_for_write(bundle: dict[str, str]) -> None:
    expected_paths = (
        ROLL_SEMANTICS_LEDGER_RELATIVE_PATH,
        ROLL_SEMANTICS_STATUS_RELATIVE_PATH,
        ROLL_SEMANTICS_PROVENANCE_RELATIVE_PATH,
        ROLL_SEMANTICS_HASH_RELATIVE_PATH,
    )
    if tuple(bundle) != expected_paths:
        raise CarverBlocked("S09 MES roll semantics evidence lock write bundle has unexpected paths")
    for relative_path, text in bundle.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES roll semantics lock artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES roll semantics lock write bundle must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES roll semantics lock write bundle must not promote forbidden scope")
    expected_manifest = _render_sha256_manifest({path: bundle[path] for path in expected_paths[:-1]})
    if bundle[ROLL_SEMANTICS_HASH_RELATIVE_PATH] != expected_manifest:
        raise CarverBlocked("S09 MES roll semantics evidence lock SHA256 manifest is invalid")


def _validate_annual_risk_runtime_values_lock_bundle_for_write(bundle: dict[str, str]) -> None:
    expected_paths = (
        ANNUAL_RISK_LEDGER_RELATIVE_PATH,
        ANNUAL_RISK_STATUS_RELATIVE_PATH,
        ANNUAL_RISK_PROVENANCE_RELATIVE_PATH,
        ANNUAL_RISK_HASH_RELATIVE_PATH,
    )
    if tuple(bundle) != expected_paths:
        raise CarverBlocked("S09 MES annual-risk evidence lock write bundle has unexpected paths")
    for relative_path, text in bundle.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES annual-risk lock artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES annual-risk lock write bundle must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES annual-risk lock write bundle must not promote forbidden scope")
    expected_manifest = _render_sha256_manifest({path: bundle[path] for path in expected_paths[:-1]})
    if bundle[ANNUAL_RISK_HASH_RELATIVE_PATH] != expected_manifest:
        raise CarverBlocked("S09 MES annual-risk evidence lock SHA256 manifest is invalid")


def _validate_daily_price_risk_values_lock_bundle_for_write(bundle: dict[str, str]) -> None:
    expected_paths = (
        DAILY_PRICE_RISK_LEDGER_RELATIVE_PATH,
        DAILY_PRICE_RISK_STATUS_RELATIVE_PATH,
        DAILY_PRICE_RISK_PROVENANCE_RELATIVE_PATH,
        DAILY_PRICE_RISK_HASH_RELATIVE_PATH,
    )
    if tuple(bundle) != expected_paths:
        raise CarverBlocked("S09 MES daily price-risk evidence lock write bundle has unexpected paths")
    for relative_path, text in bundle.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES daily price-risk lock artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES daily price-risk lock write bundle must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES daily price-risk lock write bundle must not promote forbidden scope")
    expected_manifest = _render_sha256_manifest({path: bundle[path] for path in expected_paths[:-1]})
    if bundle[DAILY_PRICE_RISK_HASH_RELATIVE_PATH] != expected_manifest:
        raise CarverBlocked("S09 MES daily price-risk evidence lock SHA256 manifest is invalid")


def _validate_historical_mes_cost_values_fail_closed_bundle_for_write(bundle: dict[str, str]) -> None:
    expected_paths = (
        HISTORICAL_COST_LEDGER_RELATIVE_PATH,
        HISTORICAL_COST_STATUS_RELATIVE_PATH,
        HISTORICAL_COST_PROVENANCE_RELATIVE_PATH,
        HISTORICAL_COST_HASH_RELATIVE_PATH,
    )
    if tuple(bundle) != expected_paths:
        raise CarverBlocked("S09 MES historical cost fail-closed write bundle has unexpected paths")
    for relative_path, text in bundle.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES historical cost fail-closed artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES historical cost fail-closed write bundle must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text or "CFD_ADAPTER" in text:
            raise CarverBlocked("S09 MES historical cost fail-closed write bundle must not promote forbidden scope")
        if "/speed/" in text:
            raise CarverBlocked("S09 MES historical cost fail-closed write bundle must contain cost scope only")
    if HISTORICAL_COST_FAIL_CLOSED_STATUS not in bundle[HISTORICAL_COST_STATUS_RELATIVE_PATH]:
        raise CarverBlocked("S09 MES historical cost fail-closed write bundle status must remain fail-closed")
    expected_manifest = _render_sha256_manifest({path: bundle[path] for path in expected_paths[:-1]})
    if bundle[HISTORICAL_COST_HASH_RELATIVE_PATH] != expected_manifest:
        raise CarverBlocked("S09 MES historical cost fail-closed SHA256 manifest is invalid")


def _inspect_active_historical_cost_ledger_for_fail_closed(root: Path) -> str:
    ledger_path = root / HISTORICAL_COST_LEDGER_RELATIVE_PATH
    if not ledger_path.exists() or not ledger_path.is_file():
        return "active cost ledger is missing"
    ledger_text = ledger_path.read_text(encoding="utf-8")
    if "2022-01-03_2023-12-29" in ledger_text:
        raise CarverBlocked("S09 MES active historical cost ledger must not contain the retired window")
    reader = csv.DictReader(StringIO(ledger_text))
    if tuple(reader.fieldnames or ()) != COST_VALUE_LEDGER_COLUMNS:
        raise CarverBlocked("S09 MES active historical cost ledger has an unexpected schema")
    rows = list(reader)
    if rows:
        raise CarverBlocked("S09 MES active historical cost ledger contains rows requiring a separate source-native cost lock")
    return "active cost ledger is header-only"


def _verified_local_sha256_from_json_manifest(root: Path, artifact_relative_path: str, manifest_relative_path: str) -> str:
    artifact_path_text = _normalize_repo_relative_path(artifact_relative_path)
    manifest_path_text = _normalize_repo_relative_path(manifest_relative_path)
    artifact_path = root / artifact_path_text
    manifest_path = root / manifest_path_text
    if not artifact_path.exists() or not artifact_path.is_file():
        raise CarverBlocked("S09 MES hash-bound local artifact is missing")
    if not manifest_path.exists() or not manifest_path.is_file():
        raise CarverBlocked("S09 MES local SHA256 manifest is missing")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CarverBlocked("S09 MES local SHA256 manifest is invalid JSON") from exc
    if not isinstance(manifest, dict):
        raise CarverBlocked("S09 MES local SHA256 manifest must be a JSON object")
    expected_sha256 = None
    for key, value in manifest.items():
        if _normalize_repo_relative_path(str(key)) == artifact_path_text:
            expected_sha256 = str(value).upper()
            break
    if expected_sha256 is None:
        raise CarverBlocked("S09 MES local SHA256 manifest does not cover the required artifact")
    _require_sha256("S09 MES local artifact SHA256", expected_sha256)
    actual_sha256 = hashlib.sha256(artifact_path.read_bytes()).hexdigest().upper()
    if actual_sha256 != expected_sha256:
        raise CarverBlocked("S09 MES local artifact SHA256 mismatch")
    return expected_sha256


def _completed_trading_date_for_provider_roll_date(provider_roll_date: date) -> date:
    _require_exact_date("S09 MES provider roll date", provider_roll_date)
    if provider_roll_date.weekday() != 6:
        raise CarverBlocked("S09 MES provider roll date must be the Sunday provider date needing completed-bar normalization")
    return provider_roll_date + timedelta(days=1)


def _normalize_repo_relative_path(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked("S09 MES repo-relative path is missing")
    normalized = value.strip().replace("\\", "/")
    if Path(normalized).is_absolute() or ":" in normalized:
        raise CarverBlocked("S09 MES repo-relative path must not be absolute")
    if any(part in {"", ".", ".."} for part in normalized.split("/")):
        raise CarverBlocked("S09 MES repo-relative path must not traverse directories")
    if "2022-01-03_2023-12-29" in normalized:
        raise CarverBlocked("S09 MES repo-relative path must not use the retired window")
    return normalized


def _require_source_native_metadata_relative_path(value: str) -> None:
    normalized = _normalize_repo_relative_path(value)
    required_prefix = (
        "docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/raw_provider_metadata/"
    )
    if not normalized.startswith(required_prefix):
        raise CarverBlocked("S09 MES lifecycle source metadata path is outside the authorized machinery slice")
    if not normalized.endswith("_definition.csv"):
        raise CarverBlocked("S09 MES lifecycle source metadata path must be a definition CSV")


def _parse_date_prefix(value: str) -> date:
    if not isinstance(value, str) or len(value.strip()) < 10:
        raise CarverBlocked("S09 MES lifecycle date value is missing")
    try:
        return date.fromisoformat(value.strip()[:10])
    except ValueError as exc:
        raise CarverBlocked("S09 MES lifecycle date value is invalid") from exc


def _require_positive_integer_text(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.isdigit() or int(value) <= 0:
        raise CarverBlocked(f"{name} must be a positive integer")


def _validate_evidence_completion_bundle_for_write(bundle: dict[str, str]) -> None:
    if not isinstance(bundle, dict) or not bundle:
        raise CarverBlocked("S09 MES strategy-input evidence completion write bundle is missing")
    expected_hash_path = f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt"
    if expected_hash_path not in bundle:
        raise CarverBlocked("S09 MES strategy-input evidence completion write bundle is missing SHA256 manifest")
    for relative_path, text in bundle.items():
        _require_evidence_completion_relative_path(relative_path)
        _require_non_empty(f"S09 MES evidence completion artifact text for {relative_path}", text)
        if "2022-01-03_2023-12-29" in text:
            raise CarverBlocked("S09 MES evidence completion write bundle must not contain the retired window")
        if "READY_FOR_BACKTEST" in text or "READY_FOR_LOCKBOX" in text:
            raise CarverBlocked("S09 MES evidence completion write bundle must not promote readiness")
    status_text = bundle.get(f"{OUTPUT_ROOT_RELATIVE}/status/{RUN_ID}_status.json", "")
    if EVIDENCE_COMPLETION_NOT_READY_STATUS not in status_text:
        raise CarverBlocked("S09 MES evidence completion write bundle status must remain fail-closed")


def _validate_readiness_handoff_request(
    request: S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest,
) -> None:
    if request.evidence_completion_status != EVIDENCE_COMPLETION_LOCKED_STATUS:
        raise CarverBlocked("S09 MES readiness handoff requires locked evidence completion status")
    if request.strategy_input_readiness_status != STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_STATUS:
        raise CarverBlocked("S09 MES readiness handoff must await the separate readiness gate")
    if isinstance(request.remaining_evidence_count, bool) or request.remaining_evidence_count != 0:
        raise CarverBlocked("S09 MES readiness handoff requires zero remaining evidence items")
    if request.next_gate != READINESS_HANDOFF_NEXT_GATE:
        raise CarverBlocked("S09 MES readiness handoff must point to the strategy-input readiness gate")
    if request.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES readiness handoff is source-native futures only")
    if request.root != ROOT_SYMBOL or request.row_id != ROW_ID:
        raise CarverBlocked("S09 MES readiness handoff is locked to Appendix C MES row")
    if request.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES readiness handoff must use the oldest machinery-development slice")
    for label, value in (
        ("Databento API access", request.databento_api_access),
        ("market-row parsing", request.market_row_parsing),
        ("forecast computation", request.forecast_computation),
        ("diagnostics run", request.diagnostics_run),
        ("backtests run", request.backtests_run),
        ("TEST/VALIDATION/Lockbox/Forward access", request.test_validation_lockbox_forward_access),
    ):
        if value != "NO":
            raise CarverBlocked(f"S09 MES readiness handoff requires {label} to remain NO")


def _write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _render_result_text(
    root: Path,
    status_path: Path,
    provenance_path: Path,
    artifact_paths: tuple[Path, ...],
) -> str:
    explicitly_listed = {status_path, provenance_path}
    relative_artifacts = "\n".join(
        f"- `{path.relative_to(root).as_posix()}`" for path in artifact_paths if path not in explicitly_listed
    )
    return f"""# S09 MES Strategy Input Evidence Completion Result

Date: 2026-06-03

Status:

```text
{EVIDENCE_COMPLETION_NOT_READY_STATUS}
```

Authorized execution scope:

```text
{GATE}
```

- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

This helper materializes the local evidence-completion packet only when
explicitly called by an authorized gate. It does not include Databento API
access, provider login, OHLCV request, new data download, market-row parsing,
CFD adapter work, or old QuantLab active-pipeline use.

Outcome:

The evidence-completion packet remains fail-closed because the strategy-input
evidence rows are header-only fail-closed ledgers. Downstream steps must not
mistake this packet for ready strategy input.

Written artifacts:

- `{status_path.relative_to(root).as_posix()}`
- `{provenance_path.relative_to(root).as_posix()}`
{relative_artifacts}

Boundary preserved:

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations were performed.
"""


def _render_audit_text(
    root: Path,
    status_path: Path,
    provenance_path: Path,
    artifact_paths: tuple[Path, ...],
    result_path: Path,
) -> str:
    explicitly_listed = {status_path, provenance_path, result_path}
    relative_artifacts = "\n".join(
        f"- `{path.relative_to(root).as_posix()}`" for path in artifact_paths if path not in explicitly_listed
    )
    hashes_path = root / f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt"
    return f"""# S09 MES Strategy Input Evidence Completion Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_FAIL_CLOSED_NO_BACKTEST
```

Audit scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- root: {ROOT_SYMBOL}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- runtime_input_lock_scope: {RUNTIME_INPUT_LOCK_SCOPE}
- design_ordering: {DESIGN_ORDERING}

Observed artifacts:

- `{result_path.relative_to(root).as_posix()}`
- `{status_path.relative_to(root).as_posix()}`
- `{provenance_path.relative_to(root).as_posix()}`
- `{hashes_path.relative_to(root).as_posix()}`
{relative_artifacts}

Hostile checks:

- no Databento API access
- no provider download
- no market-row parsing
- header-only fail-closed ledgers
- no fabricated lifecycle evidence
- no fabricated roll semantics
- no fabricated risk values
- no fabricated cost values
- no default all-six-speed assumption
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no OOS
- no Lockbox
- no Forward
- no Git staging
"""


def _render_written_sha256_manifest(root: Path, paths: tuple[Path, ...]) -> str:
    seen: set[str] = set()
    lines: list[str] = []
    for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix()):
        relative_path = path.relative_to(root).as_posix()
        if relative_path in seen:
            raise CarverBlocked("S09 MES evidence completion written artifact manifest paths must be unique")
        seen.add(relative_path)
        if "2022-01-03_2023-12-29" in relative_path:
            raise CarverBlocked("S09 MES evidence completion written artifact manifest must not use the retired window")
        if "/hashes/" in relative_path:
            raise CarverBlocked("S09 MES evidence completion written artifact manifest must not hash itself")
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        lines.append(f"{digest}  {relative_path}")
    return "\n".join(lines) + "\n"


def _require_evidence_completion_relative_path(value: str) -> None:
    normalized = value.replace("\\", "/")
    if Path(normalized).is_absolute() or ":" in normalized:
        raise CarverBlocked("S09 MES evidence completion artifact path must be repo-relative")
    if any(part in {"", ".", ".."} for part in normalized.split("/")):
        raise CarverBlocked("S09 MES evidence completion artifact path must not traverse directories")
    if "2022-01-03_2023-12-29" in normalized:
        raise CarverBlocked("S09 MES evidence completion artifact path must not use the retired 2022-2023 window")
    if any(token in normalized.lower() for token in ("/test/", "validation", "lockbox", "forward", "oos")):
        raise CarverBlocked("S09 MES evidence completion artifact path must not access scored or locked-out windows")
    if not normalized.startswith(f"{OUTPUT_ROOT_RELATIVE}/"):
        raise CarverBlocked("S09 MES evidence completion artifact path must stay inside the evidence completion root")


def _require_process_relative_path(value: str) -> None:
    normalized = value.replace("\\", "/")
    if Path(normalized).is_absolute() or ":" in normalized:
        raise CarverBlocked("S09 MES process packet path must be repo-relative")
    if any(part in {"", ".", ".."} for part in normalized.split("/")):
        raise CarverBlocked("S09 MES process packet path must not traverse directories")
    if "2022-01-03_2023-12-29" in normalized:
        raise CarverBlocked("S09 MES process packet path must not use the retired 2022-2023 window")
    if not normalized.startswith("docs/process/"):
        raise CarverBlocked("S09 MES process packet path must stay inside docs/process")


def _selected_evidence_packet_stem(evidence_name: str) -> str:
    if evidence_name not in REQUIRED_EVIDENCE_NAMES:
        raise CarverBlocked("S09 MES selected evidence packet stem requires a known evidence family")
    return f"CARVER_S09_MES_STRATEGY_INPUT_{evidence_name.upper()}_AUTHORIZATION_READY_PACKET"


def _validate_lifecycle_row(row: S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow) -> None:
    _require_mes_symbol("S09 MES lifecycle evidence raw symbol", row.raw_symbol)
    _require_exact_date("S09 MES lifecycle first completed trading date", row.first_completed_trading_date)
    _require_exact_date("S09 MES lifecycle last completed trading date", row.last_completed_trading_date)
    _require_exact_date("S09 MES lifecycle expiration completed trading date", row.expiration_completed_trading_date)
    if row.first_completed_trading_date > row.last_completed_trading_date:
        raise CarverBlocked("S09 MES lifecycle evidence first date must not be after last date")
    if row.expiration_completed_trading_date <= row.last_completed_trading_date:
        raise CarverBlocked("S09 MES lifecycle evidence expiration completed date must follow last trading date")
    _require_non_empty("S09 MES lifecycle evidence source label", row.source_label)
    _require_sha256("S09 MES lifecycle evidence source SHA256", row.source_sha256)
    if row.status != LIFECYCLE_LOCKED_STATUS:
        raise CarverBlocked("S09 MES lifecycle evidence status is not locked")


def _validate_roll_semantics_row(row: S09MESStrategyInputEvidenceCompletionRollSemanticsRow) -> None:
    _require_mes_symbol("S09 MES roll semantics old symbol", row.old_symbol)
    _require_mes_symbol("S09 MES roll semantics new symbol", row.new_symbol)
    if row.old_symbol == row.new_symbol:
        raise CarverBlocked("S09 MES roll semantics old and new symbols must differ")
    _require_exact_date("S09 MES roll semantics provider roll date", row.provider_roll_date)
    _require_exact_date("S09 MES roll semantics completed roll date", row.completed_roll_date)
    if row.completed_roll_date < row.provider_roll_date:
        raise CarverBlocked("S09 MES roll semantics completed roll date must not precede provider roll date")
    _require_non_empty("S09 MES roll semantics source label", row.source_label)
    _require_sha256("S09 MES roll semantics source SHA256", row.source_sha256)
    if row.status != ROLL_SEMANTICS_LOCKED_STATUS:
        raise CarverBlocked("S09 MES roll semantics status is not locked")


def _validate_annual_risk_row(row: S09MESStrategyInputEvidenceCompletionAnnualRiskRow) -> None:
    _require_exact_date("S09 MES annual-risk completed trading date", row.completed_trading_date)
    _require_finite_positive("S09 MES long-run annual risk", row.long_run_annual_risk)
    _require_finite_positive("S09 MES current EWMA32 annual risk", row.current_ewma32_annual_risk)
    _require_finite_positive("S09 MES annual percentage risk", row.annual_percentage_risk)
    expected = (
        ANNUAL_RISK_LONG_RUN_WEIGHT * float(row.long_run_annual_risk)
        + ANNUAL_RISK_CURRENT_WEIGHT * float(row.current_ewma32_annual_risk)
    )
    if abs(float(row.annual_percentage_risk) - expected) > 1e-12:
        raise CarverBlocked("S09 MES annual-risk row does not match locked 30/70 annual-risk blend")
    _require_non_empty("S09 MES annual-risk source label", row.source_label)
    _require_sha256("S09 MES annual-risk source SHA256", row.source_sha256)
    if row.status != ANNUAL_RISK_LOCKED_STATUS:
        raise CarverBlocked("S09 MES annual-risk status is not locked")


def _validate_daily_price_risk_row(row: S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow) -> None:
    _require_exact_date("S09 MES daily price-risk completed trading date", row.completed_trading_date)
    _require_finite_positive("S09 MES current price", row.current_price)
    _require_finite_positive("S09 MES annual percentage risk", row.annual_percentage_risk)
    _require_finite_positive("S09 MES daily price risk", row.daily_price_risk_currency)
    expected = float(row.current_price) * float(row.annual_percentage_risk) / 16
    if abs(float(row.daily_price_risk_currency) - expected) > 1e-12:
        raise CarverBlocked("S09 MES daily price-risk row does not match locked current-price risk formula")
    _require_non_empty("S09 MES daily price-risk source label", row.source_label)
    _require_sha256("S09 MES daily price-risk source SHA256", row.source_sha256)
    if row.status != DAILY_PRICE_RISK_LOCKED_STATUS:
        raise CarverBlocked("S09 MES daily price-risk status is not locked")


def _validate_cost_value_row(row: S09MESStrategyInputEvidenceCompletionCostValueRow) -> None:
    _require_exact_date("S09 MES cost value completed trading date", row.completed_trading_date)
    _require_non_empty("S09 MES cost value component name", row.component_name)
    if row.component_name not in REQUIRED_COST_COMPONENTS:
        raise CarverBlocked("S09 MES cost value component is not in the locked component set")
    _require_finite_positive("S09 MES cost value amount", row.amount_currency)
    if row.currency != "USD":
        raise CarverBlocked("S09 MES cost value currency must be USD")
    if row.charge_timing not in COST_CHARGE_TIMINGS:
        raise CarverBlocked("S09 MES cost value charge timing is not locked")
    _require_exact_date("S09 MES cost value effective start", row.effective_start)
    _require_exact_date("S09 MES cost value effective end", row.effective_end)
    if row.effective_start > row.completed_trading_date or row.effective_end < row.completed_trading_date:
        raise CarverBlocked("S09 MES cost value effective dates must contain the completed trading date")
    _require_non_empty("S09 MES cost value source label", row.source_label)
    _require_sha256("S09 MES cost value source SHA256", row.source_sha256)
    if row.status != COST_VALUE_LOCKED_STATUS:
        raise CarverBlocked("S09 MES cost value status is not locked")


def _validate_risk_adjusted_cost_row(row: S09MESStrategyInputEvidenceCompletionRiskAdjustedCostRow) -> None:
    _require_exact_date("S09 MES risk-adjusted cost completed trading date", row.completed_trading_date)
    _require_finite_positive("S09 MES total cost per trade", row.total_cost_per_trade_currency)
    _require_finite_positive("S09 MES risk-adjusted cost daily price risk", row.daily_price_risk_currency)
    _require_finite_positive("S09 MES risk-adjusted cost per trade", row.risk_adjusted_cost_per_trade_sr)
    expected = float(row.total_cost_per_trade_currency) / (
        float(row.daily_price_risk_currency)
        * DAILY_TO_ANNUAL_RISK_SCALAR
        * MES_CONTRACT_MULTIPLIER_USD_PER_POINT
    )
    if abs(float(row.risk_adjusted_cost_per_trade_sr) - expected) > 1e-12:
        raise CarverBlocked("S09 MES risk-adjusted cost row does not match total cost over annualized USD price risk")
    _require_non_empty("S09 MES risk-adjusted cost source label", row.source_label)
    _require_sha256("S09 MES risk-adjusted cost source SHA256", row.source_sha256)
    if row.status != RISK_ADJUSTED_COST_LOCKED_STATUS:
        raise CarverBlocked("S09 MES risk-adjusted cost status is not locked")


def _validate_speed_eligibility_row(row: S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow) -> None:
    if isinstance(row.span, bool) or row.span not in EWMAC_TURNOVER_BY_SPAN:
        raise CarverBlocked("S09 MES speed eligibility span is not locked")
    _require_finite_positive("S09 MES speed eligibility turnover", row.turnover)
    if abs(float(row.turnover) - EWMAC_TURNOVER_BY_SPAN[row.span]) > 1e-12:
        raise CarverBlocked("S09 MES speed eligibility turnover does not match the locked turnover table")
    _require_finite_positive("S09 MES speed eligibility risk-adjusted cost", row.risk_adjusted_cost_per_trade_sr)
    _require_finite_positive("S09 MES speed eligibility threshold", row.threshold_sr)
    if abs(float(row.threshold_sr) - SPEED_ELIGIBILITY_THRESHOLD_SR) > 1e-12:
        raise CarverBlocked("S09 MES speed eligibility threshold must be the locked 0.15 SR threshold")
    if type(row.eligible) is not bool:
        raise CarverBlocked("S09 MES speed eligibility flag must be boolean")
    expected_eligible = float(row.turnover) * float(row.risk_adjusted_cost_per_trade_sr) <= float(row.threshold_sr)
    if row.eligible is not expected_eligible:
        raise CarverBlocked("S09 MES speed eligibility flag does not match the locked cost threshold")
    _require_non_empty("S09 MES speed eligibility source label", row.source_label)
    _require_sha256("S09 MES speed eligibility source SHA256", row.source_sha256)
    if row.status != SPEED_ELIGIBILITY_LOCKED_STATUS:
        raise CarverBlocked("S09 MES speed eligibility status is not locked")


def _validate_eligible_speed_set_fdm_row(row: S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow) -> None:
    if not isinstance(row.eligible_spans, tuple) or not row.eligible_spans:
        raise CarverBlocked("S09 MES eligible speed set must be a non-empty tuple")
    if tuple(sorted(row.eligible_spans)) != row.eligible_spans or len(set(row.eligible_spans)) != len(row.eligible_spans):
        raise CarverBlocked("S09 MES eligible speed set must be ordered and unique")
    if any(isinstance(span, bool) or span not in S09_EWMAC_SPANS for span in row.eligible_spans):
        raise CarverBlocked("S09 MES eligible speed set contains an unsupported EWMAC span")
    _require_finite_positive("S09 MES Table 36 FDM", row.table36_fdm)
    expected = s09_fdm_for_allowed_spans(row.eligible_spans)
    if abs(float(row.table36_fdm) - expected) > 1e-12:
        raise CarverBlocked("S09 MES Table 36 FDM does not match the locked eligible speed set")
    _require_non_empty("S09 MES Table 36 FDM source label", row.source_label)
    _require_sha256("S09 MES Table 36 FDM source SHA256", row.source_sha256)
    if row.status != ELIGIBLE_SPEED_SET_FDM_LOCKED_STATUS:
        raise CarverBlocked("S09 MES eligible speed set and Table 36 FDM status is not locked")


def _validate_hash_manifest_entry(entry: S09MESStrategyInputEvidenceCompletionHashManifestEntry) -> None:
    _require_evidence_completion_relative_path(entry.relative_path)
    if "/hashes/" in entry.relative_path.replace("\\", "/"):
        raise CarverBlocked("S09 MES evidence completion hash manifest must not include hash files")
    _require_non_empty("S09 MES evidence completion artifact text", entry.artifact_text)
    if "2022-01-03_2023-12-29" in entry.artifact_text:
        raise CarverBlocked("S09 MES evidence completion manifest artifact text must not contain the retired window")
    if "READY_FOR_BACKTEST" in entry.artifact_text or "READY_FOR_LOCKBOX" in entry.artifact_text:
        raise CarverBlocked("S09 MES evidence completion manifest artifact text must not promote readiness")


def _require_mes_symbol(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.startswith("MES") or len(value) < 5 or any(token in value.upper() for token in ("CFD", "/", "\\")):
        raise CarverBlocked(f"{name} must be an MES dated contract symbol")


def _require_exact_date(name: str, value: date) -> None:
    if type(value) is not date:
        raise CarverBlocked(f"{name} must be an exact date")


def _require_non_empty(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked(f"{name} is missing")


def _require_sha256(name: str, value: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise CarverBlocked(f"{name} is missing")
    try:
        int(value, 16)
    except ValueError as exc:
            raise CarverBlocked(f"{name} is invalid") from exc


def _require_finite_positive(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"{name} must be finite and positive")


def _parse_positive_float(name: str, value: str) -> float:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked(f"{name} is missing")
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be numeric") from exc
    _require_finite_positive(name, parsed)
    return parsed


def _format_spans(spans: tuple[int, ...]) -> str:
    return "|".join(str(span) for span in spans)


def _blocking_reason_for_evidence(evidence_name: str) -> str:
    reasons = {
        "official_lifecycle_evidence": "Official per-contract lifecycle evidence is not locked for the machinery slice.",
        "roll_trading_day_semantics": "Roll trading-day semantics are not locked to completed bars.",
        "annual_risk_runtime_values": "Annual-risk runtime values are not locked from authorized source-native inputs.",
        "daily_price_risk_values": "Daily price-risk values are blocked until annual-risk runtime is locked.",
        "historical_mes_cost_values": "Historical MES cost components are not locked from source-native evidence.",
        "risk_adjusted_cost_values": "Risk-adjusted cost is blocked until cost and daily price risk are locked.",
        "speed_eligibility_values": "Speed eligibility is blocked until risk-adjusted cost is locked.",
        "eligible_speed_set": "Eligible speed set is not locked; all-six-speed assumption remains forbidden.",
        "table36_fdm_row": "Table 36 FDM row is blocked until eligible speed set is locked.",
        "hash_bound_provenance": "Hash-bound provenance tying evidence to the machinery slice is incomplete.",
    }
    return reasons[evidence_name]


def _next_action_for_evidence(evidence_name: str) -> str:
    actions = {
        "official_lifecycle_evidence": "Lock per-contract lifecycle evidence from explicitly authorized source-native sources.",
        "roll_trading_day_semantics": "Lock provider dates to completed trading dates before strategy computation.",
        "annual_risk_runtime_values": "Compute only from hash-bound authorized source-native machinery-slice inputs.",
        "daily_price_risk_values": "Compute from locked current price and locked annual percentage risk only.",
        "historical_mes_cost_values": "Lock exchange, clearing/regulatory, broker, and spread/slippage cost evidence.",
        "risk_adjusted_cost_values": "Compute total cost over locked annualized USD price risk only.",
        "speed_eligibility_values": "Apply the locked 0.15 SR threshold against the locked turnover table.",
        "eligible_speed_set": "Select eligible spans only after cost eligibility passes.",
        "table36_fdm_row": "Select the FDM row only after eligible speed set is locked.",
        "hash_bound_provenance": "Emit a deterministic SHA256 manifest for every evidence artifact.",
    }
    return actions[evidence_name]

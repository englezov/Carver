from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from math import isfinite
from numbers import Integral, Real

from .m0 import CarverBlocked, CompletedBar, LaneClass, SourceRuleStatus, require_non_empty_text, require_source_native
from .m1 import TimedValue
from .m2 import S09_EWMAC_SPANS, s09_fdm_for_allowed_spans
from .s09 import S09DailyPriceRiskRequest, s09_daily_price_risk


MES_ROOT = "MES"
MES_ROW_ID = "APPENDIX_C_174_006"
MES_EXPANSION_PASS_STATUS = "PASS_S09_MES_DAILY_EXPANSION_QUARANTINE_ONLY_NOT_LINEAGE_NOT_BACKTEST"
MES_STRATEGY_READY_STATUS = "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY"
S09_MES_STRATEGY_INPUT_READINESS_GATE = "S09_MES_STRATEGY_INPUT_READINESS_GATE"
S09_MES_EVIDENCE_COMPLETION_LOCKED_STATUS = (
    "LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION"
)
S09_MES_EVIDENCE_COMPLETION_HANDOFF_STATUS = (
    "S09_MES_EVIDENCE_COMPLETION_HANDOFF_READY_FOR_READINESS_GATE_NOT_BACKTEST"
)
S09_MES_EVIDENCE_AWAITING_READINESS_STATUS = "S09_MES_STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_GATE"
S09_MES_MACHINERY_DEVELOPMENT_SLICE_TEXT = "2019-05-05 through 2020-04-05"
S09_MES_READINESS_PREFLIGHT_ONLY_STATUS = "AUTHORIZED_READINESS_PREFLIGHT_ONLY_NOT_EXECUTED"
S09_MES_COST_THRESHOLD_SR = 0.15
S09_MES_EWMAC_TURNOVER_BY_SPAN = {
    2: 98.5,
    4: 50.2,
    8: 25.4,
    16: 13.2,
    32: 7.6,
    64: 5.2,
}
S09_MES_ANNUAL_RISK_EWMA_SPAN = 32
S09_MES_ANNUAL_RISK_LONG_RUN_WEIGHT = 0.30
S09_MES_ANNUAL_RISK_CURRENT_WEIGHT = 0.70
S09_MES_DAILY_TO_ANNUAL_RISK_SCALAR = 16
S09_MES_CONTRACT_MULTIPLIER_USD_PER_POINT = 5.0
S09_MES_REQUIRED_COST_COMPONENTS = (
    "exchange_fee",
    "clearing_regulatory_fee",
    "broker_commission",
    "spread_slippage",
)
S09_MES_COST_CHARGE_TIMINGS = ("PER_SIDE", "ROUND_TURN")
S09_MES_DEV_RECON_PHASE_LABEL = "DEVELOPMENT_RECONCILIATION"
S09_MES_MAX_DEV_RECON_WINDOW_SPAN_DAYS = 731
S09_MES_ROLL_RISK_COST_EXECUTION_GATE_NAME = "S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE"
S09_MES_ROLL_RISK_COST_PROCESS_GATE_STATUS = (
    "PROCESS_ONLY_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_GATE_NOT_EXECUTION"
)
S09_MES_EXECUTION_AUTHORIZATION_REQUEST_READY_STATUS = (
    "READY_FOR_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_AUTHORIZATION_REQUEST_NOT_EXECUTION"
)
S09_MES_ROLL_RISK_COST_OUTPUT_ROOT = (
    "docs/researchops/s09/mes_roll_date_normalization_runtime_risk_cost_execution/2022-01-03_2023-12-29"
)
S09_MES_ROLL_RISK_COST_OUTPUT_MANIFEST_READY_STATUS = (
    "S09_MES_ROLL_RISK_COST_EXECUTION_OUTPUT_MANIFEST_READY_NOT_EXECUTION"
)
S09_MES_ROLL_RISK_COST_EXPECTED_ARTIFACT_SCHEMAS = (
    (
        "roll_date_normalization/<STAMP>_S09_MES_ROLL_DATE_NORMALIZATION_ledger.csv",
        (
            "provider_date",
            "completed_trading_date",
            "old_symbol",
            "new_symbol",
            "authority_source",
            "authority_sha256",
            "status",
        ),
    ),
    (
        "risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
        (
            "completed_trading_date",
            "long_run_annual_risk",
            "current_ewma32_annual_risk",
            "annual_percentage_risk",
            "source_sha256",
            "status",
        ),
    ),
    (
        "risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv",
        (
            "completed_trading_date",
            "current_price",
            "annual_percentage_risk",
            "daily_price_risk_currency",
            "source_sha256",
            "status",
        ),
    ),
    (
        "cost/<STAMP>_S09_MES_COST_VALUE_ledger.csv",
        (
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
        ),
    ),
    (
        "cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv",
        (
            "completed_trading_date",
            "total_cost_per_trade_currency",
            "daily_price_risk_currency",
            "risk_adjusted_cost_per_trade_sr",
            "status",
        ),
    ),
    (
        "speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv",
        (
            "span",
            "turnover",
            "risk_adjusted_cost_per_trade_sr",
            "threshold_sr",
            "eligible",
            "status",
        ),
    ),
    (
        "status/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_status.json",
        (
            "status",
            "databento_api_access",
            "new_provider_data_download",
            "market_row_parsing",
            "strategy_input_readiness_status",
        ),
    ),
    (
        "provenance/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_provenance.md",
        ("scope", "inputs", "non_authorization", "oldest_authorized_ordering"),
    ),
    (
        "hashes/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_sha256.txt",
        ("sha256", "relative_path"),
    ),
)


@dataclass(frozen=True)
class S09MESStrategyInputReadinessRequest:
    lane_class: LaneClass
    root: str
    row_id: str
    expansion_status: str
    continuous_lineage_status: SourceRuleStatus
    roll_plan_status: SourceRuleStatus
    roll_date_normalization_status: SourceRuleStatus
    back_adjustment_status: SourceRuleStatus
    provider_condition_admission_status: SourceRuleStatus
    oldest_authorized_data_ordering_status: SourceRuleStatus
    development_reconciliation_window_status: SourceRuleStatus
    annual_risk_runtime_status: SourceRuleStatus
    daily_price_risk_runtime_status: SourceRuleStatus
    cost_source_status: SourceRuleStatus
    historical_cost_values_status: SourceRuleStatus
    risk_adjusted_cost_status: SourceRuleStatus
    speed_cost_eligibility_status: SourceRuleStatus
    eligible_speed_set_status: SourceRuleStatus
    table36_fdm_row_status: SourceRuleStatus
    hash_bound_provenance_status: SourceRuleStatus
    speed_eligibility_basis: str
    eligible_spans: tuple[int, ...]
    fdm: float


@dataclass(frozen=True)
class S09MESStrategyInputReadinessResult:
    root: str
    row_id: str
    ready: bool
    readiness_status: str
    eligible_spans: tuple[int, ...]
    fdm: float
    blockers: tuple[str, ...]


@dataclass(frozen=True)
class S09MESAnnualRiskBlendRequest:
    lane_class: LaneClass
    completed_bar: CompletedBar
    long_run_annual_risk: TimedValue
    long_run_status: SourceRuleStatus
    current_ewma32_annual_risk: TimedValue
    current_risk_status: SourceRuleStatus
    blend_status: SourceRuleStatus
    ewma_span: int = S09_MES_ANNUAL_RISK_EWMA_SPAN
    long_run_weight: float = S09_MES_ANNUAL_RISK_LONG_RUN_WEIGHT
    current_risk_weight: float = S09_MES_ANNUAL_RISK_CURRENT_WEIGHT


@dataclass(frozen=True)
class S09MESAnnualRiskBlendResult:
    annual_percentage_risk: float
    as_of: datetime
    long_run_annual_risk: float
    current_ewma32_annual_risk: float
    long_run_weight: float
    current_risk_weight: float
    blend_basis: str

    @property
    def ready_for_daily_price_risk(self) -> bool:
        return self.annual_percentage_risk > 0


@dataclass(frozen=True)
class S09MESDailyPriceRiskRequest:
    lane_class: LaneClass
    completed_bar: CompletedBar
    current_price: TimedValue
    current_price_status: SourceRuleStatus
    annual_percentage_risk: TimedValue
    annual_risk_runtime_status: SourceRuleStatus
    conversion_source_status: SourceRuleStatus
    annualization_days: int = 256


@dataclass(frozen=True)
class S09MESDailyPriceRiskResult:
    daily_price_risk_currency: float
    as_of: datetime
    current_price: float
    annual_percentage_risk: float
    conversion_basis: str

    @property
    def ready_for_risk_adjusted_cost(self) -> bool:
        return self.daily_price_risk_currency > 0


@dataclass(frozen=True)
class S09MESOldestAuthorizedDesignOrderingRequest:
    lane_class: LaneClass
    root: str
    row_id: str
    authorized_completed_dates: tuple[date, ...]
    admitted_completed_dates: tuple[date, ...]
    authorization_status: SourceRuleStatus
    provenance_status: SourceRuleStatus


@dataclass(frozen=True)
class S09MESOldestAuthorizedDesignOrderingResult:
    first_authorized_completed_date: date
    first_admitted_completed_date: date
    admitted_completed_dates: tuple[date, ...]
    ordering_basis: str

    @property
    def ready_for_runtime_gate(self) -> bool:
        return bool(self.admitted_completed_dates)


@dataclass(frozen=True)
class S09MESDevelopmentReconciliationWindowRequest:
    lane_class: LaneClass
    root: str
    row_id: str
    phase_label: str
    authorized_completed_dates: tuple[date, ...]
    window_completed_dates: tuple[date, ...]
    window_status: SourceRuleStatus
    authorization_status: SourceRuleStatus
    provenance_status: SourceRuleStatus
    oldest_authorized_data_ordering_status: SourceRuleStatus
    no_oos_lockbox_forward_status: SourceRuleStatus


@dataclass(frozen=True)
class S09MESDevelopmentReconciliationWindowResult:
    window_start: date
    window_end: date
    completed_dates: tuple[date, ...]
    window_span_days: int
    window_basis: str

    @property
    def ready_for_readiness_gate(self) -> bool:
        return bool(self.completed_dates)


@dataclass(frozen=True)
class S09MESExecutionPreflightRequest:
    lane_class: LaneClass
    root: str
    row_id: str
    gate_name: str
    process_gate_status: str
    oldest_authorized_completed_date: date
    target_completed_date_start: date
    target_completed_date_end: date
    development_reconciliation_window_status: SourceRuleStatus
    oldest_authorized_data_ordering_status: SourceRuleStatus
    no_data_execution_status: SourceRuleStatus
    no_backtest_status: SourceRuleStatus
    no_oos_lockbox_forward_status: SourceRuleStatus
    no_cfd_quantlab_status: SourceRuleStatus


@dataclass(frozen=True)
class S09MESStrategyInputReadinessGateConfig:
    execution_authorized: bool
    lane_class: LaneClass
    root: str
    row_id: str
    evidence_completion_status: str
    evidence_handoff_status: str
    strategy_input_readiness_status: str
    next_gate: str
    machinery_development_slice: str
    databento_api_access_authorized: bool
    market_row_parsing_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool


@dataclass(frozen=True)
class S09MESExecutionPreflightResult:
    preflight_status: str
    window_start: date
    window_end: date
    window_span_days: int

    @property
    def ready_for_authorization_request(self) -> bool:
        return self.preflight_status == S09_MES_EXECUTION_AUTHORIZATION_REQUEST_READY_STATUS


@dataclass(frozen=True)
class S09MESRollRiskCostExecutionArtifactSchema:
    relative_path: str
    fields: tuple[str, ...]
    status: SourceRuleStatus


@dataclass(frozen=True)
class S09MESRollRiskCostExecutionOutputManifestRequest:
    lane_class: LaneClass
    root: str
    row_id: str
    gate_name: str
    output_root: str
    artifact_schemas: tuple[S09MESRollRiskCostExecutionArtifactSchema, ...]
    manifest_status: SourceRuleStatus
    authorization_request_status: SourceRuleStatus
    no_execution_status: SourceRuleStatus


@dataclass(frozen=True)
class S09MESRollRiskCostExecutionOutputManifestResult:
    manifest_status: str
    output_root: str
    artifact_schemas: tuple[S09MESRollRiskCostExecutionArtifactSchema, ...]

    @property
    def ready_for_authorized_runner_contract(self) -> bool:
        return self.manifest_status == S09_MES_ROLL_RISK_COST_OUTPUT_MANIFEST_READY_STATUS


@dataclass(frozen=True)
class S09MESLockedCostComponent:
    component_name: str
    amount_currency: float
    currency: str
    charge_timing: str
    effective_start: date
    effective_end: date
    source_label: str
    source_sha256: str
    status: SourceRuleStatus


@dataclass(frozen=True)
class S09MESCostComponentSetRequest:
    lane_class: LaneClass
    root: str
    row_id: str
    completed_trading_date: date
    components: tuple[S09MESLockedCostComponent, ...]
    component_set_status: SourceRuleStatus


@dataclass(frozen=True)
class S09MESCostComponentSetResult:
    total_cost_per_trade_currency: float
    currency: str
    component_round_turn_costs: tuple[tuple[str, float], ...]
    cost_basis: str

    @property
    def ready_for_risk_adjusted_cost(self) -> bool:
        return self.total_cost_per_trade_currency > 0


@dataclass(frozen=True)
class S09MESRiskAdjustedCostRequest:
    lane_class: LaneClass
    total_cost_per_trade_currency: float
    total_cost_status: SourceRuleStatus
    daily_price_risk_currency: float
    daily_price_risk_status: SourceRuleStatus
    contract_multiplier_usd_per_point: float = S09_MES_CONTRACT_MULTIPLIER_USD_PER_POINT


@dataclass(frozen=True)
class S09MESRiskAdjustedCostResult:
    total_cost_per_trade_currency: float
    daily_price_risk_currency: float
    annualized_price_risk_currency: float
    risk_adjusted_cost_per_trade_sr: float
    cost_basis: str

    @property
    def ready_for_speed_eligibility(self) -> bool:
        return self.risk_adjusted_cost_per_trade_sr > 0


@dataclass(frozen=True)
class S09MESRiskAdjustedCostSpeedEligibilityRequest:
    lane_class: LaneClass
    risk_adjusted_cost_per_trade_sr: float
    risk_adjusted_cost_status: SourceRuleStatus
    threshold_sr: float = S09_MES_COST_THRESHOLD_SR
    threshold_status: SourceRuleStatus = SourceRuleStatus.LOCKED
    turnover_status: SourceRuleStatus = SourceRuleStatus.LOCKED


@dataclass(frozen=True)
class S09MESRiskAdjustedCostSpeedEligibilityResult:
    eligible_spans: tuple[int, ...]
    rejected_spans: tuple[int, ...]
    fdm: float
    threshold_sr: float
    risk_adjusted_cost_per_trade_sr: float
    eligibility_basis: str

    @property
    def ready_for_readiness_gate(self) -> bool:
        return bool(self.eligible_spans)


def evaluate_s09_mes_strategy_input_readiness(
    request: S09MESStrategyInputReadinessRequest,
) -> S09MESStrategyInputReadinessResult:
    blockers = _blockers(request)
    if blockers:
        raise CarverBlocked("; ".join(blockers))
    return S09MESStrategyInputReadinessResult(
        root=MES_ROOT,
        row_id=MES_ROW_ID,
        ready=True,
        readiness_status=MES_STRATEGY_READY_STATUS,
        eligible_spans=request.eligible_spans,
        fdm=request.fdm,
        blockers=(),
    )


def s09_mes_annual_risk_from_locked_components(
    request: S09MESAnnualRiskBlendRequest,
) -> S09MESAnnualRiskBlendResult:
    require_source_native(request.lane_class)
    request.completed_bar.validate()
    if request.long_run_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES long-run annual risk must be locked before annual risk blend")
    if request.current_risk_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES EWMA32 current annual risk must be locked before annual risk blend")
    if request.blend_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES annual risk blend source is unresolved")
    if isinstance(request.ewma_span, bool) or not isinstance(request.ewma_span, Integral):
        raise CarverBlocked("S09 MES annual risk EWMA span must be an integer")
    if request.ewma_span != S09_MES_ANNUAL_RISK_EWMA_SPAN:
        raise CarverBlocked("S09 MES annual risk EWMA span must be source-locked to 32")
    _require_finite_positive("S09 MES annual risk long-run weight", request.long_run_weight)
    _require_finite_positive("S09 MES annual risk current weight", request.current_risk_weight)
    if request.long_run_weight != S09_MES_ANNUAL_RISK_LONG_RUN_WEIGHT or request.current_risk_weight != S09_MES_ANNUAL_RISK_CURRENT_WEIGHT:
        raise CarverBlocked("S09 MES annual risk blend weights must be source-locked to 30/70")
    if abs((request.long_run_weight + request.current_risk_weight) - 1.0) > 1e-12:
        raise CarverBlocked("S09 MES annual risk blend weights must sum to 1")
    if request.long_run_annual_risk.as_of != request.completed_bar.timestamp:
        raise CarverBlocked("S09 MES long-run annual risk timestamp must align to completed bar")
    if request.current_ewma32_annual_risk.as_of != request.completed_bar.timestamp:
        raise CarverBlocked("S09 MES EWMA32 current risk timestamp must align to completed bar")
    _require_finite_positive("S09 MES long-run annual risk", request.long_run_annual_risk.value)
    _require_finite_positive("S09 MES EWMA32 current annual risk", request.current_ewma32_annual_risk.value)

    blended = (
        request.long_run_weight * request.long_run_annual_risk.value
        + request.current_risk_weight * request.current_ewma32_annual_risk.value
    )
    return S09MESAnnualRiskBlendResult(
        annual_percentage_risk=blended,
        as_of=request.completed_bar.timestamp,
        long_run_annual_risk=request.long_run_annual_risk.value,
        current_ewma32_annual_risk=request.current_ewma32_annual_risk.value,
        long_run_weight=request.long_run_weight,
        current_risk_weight=request.current_risk_weight,
        blend_basis="LOCKED_30_70_LONG_RUN_CURRENT_EWMA32_ANNUAL_PERCENTAGE_RISK",
    )


def s09_mes_daily_price_risk_from_locked_inputs(
    request: S09MESDailyPriceRiskRequest,
) -> S09MESDailyPriceRiskResult:
    require_source_native(request.lane_class)
    if request.current_price_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES current price must be locked before daily price risk")
    if request.annual_risk_runtime_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES annual risk runtime must be locked before daily price risk")
    daily_price_risk = s09_daily_price_risk(
        S09DailyPriceRiskRequest(
            completed_bar=request.completed_bar,
            current_price=request.current_price,
            annual_percentage_risk=request.annual_percentage_risk,
            annualization_days=request.annualization_days,
            conversion_source_status=request.conversion_source_status,
            lane_class=request.lane_class,
        )
    )
    return S09MESDailyPriceRiskResult(
        daily_price_risk_currency=daily_price_risk.value,
        as_of=daily_price_risk.as_of,
        current_price=request.current_price.value,
        annual_percentage_risk=request.annual_percentage_risk.value,
        conversion_basis="LOCKED_CURRENT_PRICE_TIMES_LOCKED_ANNUAL_PERCENTAGE_RISK_OVER_16",
    )


def s09_mes_oldest_authorized_design_ordering(
    request: S09MESOldestAuthorizedDesignOrderingRequest,
) -> S09MESOldestAuthorizedDesignOrderingResult:
    require_source_native(request.lane_class)
    if request.root != MES_ROOT:
        raise CarverBlocked("S09 MES oldest-data ordering forbids non-MES substitution")
    if request.row_id != MES_ROW_ID:
        raise CarverBlocked("S09 MES oldest-data ordering requires Appendix C MES row id")
    if request.authorization_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES oldest authorized completed-date set is unresolved")
    if request.provenance_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES oldest authorized data provenance is unresolved")

    authorized_dates = _require_strict_completed_date_sequence(
        "S09 MES authorized completed dates",
        request.authorized_completed_dates,
    )
    admitted_dates = _require_strict_completed_date_sequence(
        "S09 MES admitted completed dates",
        request.admitted_completed_dates,
    )
    authorized_set = set(authorized_dates)
    if any(completed_date not in authorized_set for completed_date in admitted_dates):
        raise CarverBlocked("S09 MES admitted completed dates must be a subset of authorized dates")
    if admitted_dates[0] != authorized_dates[0]:
        raise CarverBlocked("S09 MES strategy design must start with the oldest authorized completed date")

    admitted_set = set(admitted_dates)
    latest_admitted = admitted_dates[-1]
    missing_older_dates = tuple(
        completed_date
        for completed_date in authorized_dates
        if completed_date <= latest_admitted and completed_date not in admitted_set
    )
    if missing_older_dates:
        raise CarverBlocked("S09 MES strategy design may not skip older authorized completed dates")

    return S09MESOldestAuthorizedDesignOrderingResult(
        first_authorized_completed_date=authorized_dates[0],
        first_admitted_completed_date=admitted_dates[0],
        admitted_completed_dates=admitted_dates,
        ordering_basis="LOCKED_OLDEST_AUTHORIZED_COMPLETED_SOURCE_NATIVE_DATA_FIRST",
    )


def s09_mes_development_reconciliation_window(
    request: S09MESDevelopmentReconciliationWindowRequest,
) -> S09MESDevelopmentReconciliationWindowResult:
    require_source_native(request.lane_class)
    if request.root != MES_ROOT:
        raise CarverBlocked("S09 MES Development/Reconciliation window forbids non-MES substitution")
    if request.row_id != MES_ROW_ID:
        raise CarverBlocked("S09 MES Development/Reconciliation window requires Appendix C MES row id")
    if request.phase_label.upper().strip() != S09_MES_DEV_RECON_PHASE_LABEL:
        raise CarverBlocked("S09 MES window must be Development/Reconciliation only")
    if request.window_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES Development/Reconciliation window is unresolved")
    if request.authorization_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES Development/Reconciliation window authorization is unresolved")
    if request.provenance_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES Development/Reconciliation window provenance is unresolved")
    if request.oldest_authorized_data_ordering_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES Development/Reconciliation window must lock oldest authorized data ordering")
    if request.no_oos_lockbox_forward_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES Development/Reconciliation window must exclude OOS, Lockbox, and Forward")

    authorized_dates = _require_strict_completed_date_sequence(
        "S09 MES Development/Reconciliation authorized completed dates",
        request.authorized_completed_dates,
    )
    window_dates = _require_strict_completed_date_sequence(
        "S09 MES Development/Reconciliation window completed dates",
        request.window_completed_dates,
    )
    authorized_set = set(authorized_dates)
    if any(completed_date not in authorized_set for completed_date in window_dates):
        raise CarverBlocked("S09 MES Development/Reconciliation window dates must be authorized")
    if window_dates[0] != authorized_dates[0]:
        raise CarverBlocked("S09 MES Development/Reconciliation strategy design must start with the oldest authorized completed date")

    window_set = set(window_dates)
    latest_window_date = window_dates[-1]
    missing_older_dates = tuple(
        completed_date
        for completed_date in authorized_dates
        if completed_date <= latest_window_date and completed_date not in window_set
    )
    if missing_older_dates:
        raise CarverBlocked("S09 MES Development/Reconciliation window may not skip older authorized completed dates")

    window_span_days = (latest_window_date - window_dates[0]).days
    if window_span_days > S09_MES_MAX_DEV_RECON_WINDOW_SPAN_DAYS:
        raise CarverBlocked("S09 MES Development/Reconciliation window exceeds the unauthorised two-year limit")

    return S09MESDevelopmentReconciliationWindowResult(
        window_start=window_dates[0],
        window_end=latest_window_date,
        completed_dates=window_dates,
        window_span_days=window_span_days,
        window_basis="LOCKED_S09_MES_DEV_RECON_OLDEST_AUTHORIZED_SOURCE_NATIVE_COMPLETED_DATES",
    )


def s09_mes_execution_preflight(
    request: S09MESExecutionPreflightRequest,
) -> S09MESExecutionPreflightResult:
    require_source_native(request.lane_class)
    if request.root != MES_ROOT:
        raise CarverBlocked("S09 MES execution preflight forbids non-MES substitution")
    if request.row_id != MES_ROW_ID:
        raise CarverBlocked("S09 MES execution preflight requires Appendix C MES row id")
    if request.gate_name != S09_MES_ROLL_RISK_COST_EXECUTION_GATE_NAME:
        raise CarverBlocked("S09 MES execution preflight gate name is not locked")
    if request.process_gate_status != S09_MES_ROLL_RISK_COST_PROCESS_GATE_STATUS:
        raise CarverBlocked("S09 MES execution preflight must remain process-only and not execution")

    _require_locked_status(
        "S09 MES Development/Reconciliation window",
        request.development_reconciliation_window_status,
    )
    _require_locked_status(
        "S09 MES oldest authorized data ordering",
        request.oldest_authorized_data_ordering_status,
    )
    _require_locked_status("S09 MES no-data-execution preflight", request.no_data_execution_status)
    _require_locked_status("S09 MES no-backtest preflight", request.no_backtest_status)
    _require_locked_status(
        "S09 MES no-OOS-Lockbox-Forward preflight",
        request.no_oos_lockbox_forward_status,
    )
    _require_locked_status("S09 MES no-CFD-QuantLab preflight", request.no_cfd_quantlab_status)

    if type(request.oldest_authorized_completed_date) is not date:
        raise CarverBlocked("S09 MES oldest authorized completed date must be an exact date")
    if type(request.target_completed_date_start) is not date or type(request.target_completed_date_end) is not date:
        raise CarverBlocked("S09 MES execution preflight target window dates must be exact dates")
    if request.target_completed_date_start != request.oldest_authorized_completed_date:
        raise CarverBlocked("S09 MES execution preflight must start at the oldest authorized completed date")
    if request.target_completed_date_end < request.target_completed_date_start:
        raise CarverBlocked("S09 MES execution preflight target window is inverted")

    window_span_days = (request.target_completed_date_end - request.target_completed_date_start).days
    if window_span_days > S09_MES_MAX_DEV_RECON_WINDOW_SPAN_DAYS:
        raise CarverBlocked("S09 MES execution preflight exceeds the unauthorised two-year limit")

    return S09MESExecutionPreflightResult(
        preflight_status=S09_MES_EXECUTION_AUTHORIZATION_REQUEST_READY_STATUS,
        window_start=request.target_completed_date_start,
        window_end=request.target_completed_date_end,
        window_span_days=window_span_days,
    )


def run_s09_mes_strategy_input_readiness_gate(
    config: S09MESStrategyInputReadinessGateConfig,
) -> dict[str, str]:
    if config.execution_authorized is not True:
        raise CarverBlocked("S09 MES strategy-input readiness gate requires explicit operator authorization")
    require_source_native(config.lane_class)
    if config.root != MES_ROOT:
        raise CarverBlocked("S09 MES strategy-input readiness gate forbids non-MES substitution")
    if config.row_id != MES_ROW_ID:
        raise CarverBlocked("S09 MES strategy-input readiness gate requires Appendix C MES row id")
    if config.evidence_completion_status != S09_MES_EVIDENCE_COMPLETION_LOCKED_STATUS:
        raise CarverBlocked("S09 MES strategy-input evidence completion is not locked")
    if config.evidence_handoff_status != S09_MES_EVIDENCE_COMPLETION_HANDOFF_STATUS:
        raise CarverBlocked("S09 MES evidence handoff is not locked for readiness preflight only")
    if config.strategy_input_readiness_status != S09_MES_EVIDENCE_AWAITING_READINESS_STATUS:
        raise CarverBlocked("S09 MES strategy-input readiness status must remain awaiting readiness gate")
    if config.next_gate != S09_MES_STRATEGY_INPUT_READINESS_GATE:
        raise CarverBlocked("S09 MES next gate must be the strategy-input readiness gate")
    if config.machinery_development_slice != S09_MES_MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES machinery development slice must be the locked oldest minimum slice")

    _require_no_preflight_access("Databento API", config.databento_api_access_authorized)
    _require_no_preflight_access("market-row parsing", config.market_row_parsing_authorized)
    _require_no_preflight_access("forecast computation", config.forecast_computation_authorized)
    _require_no_preflight_access("diagnostics", config.diagnostics_authorized)
    _require_no_preflight_access("backtest", config.backtest_authorized)
    _require_no_preflight_access(
        "TEST/VALIDATION/LOCKBOX/Forward",
        config.test_validation_lockbox_forward_authorized,
    )

    return {
        "status": S09_MES_READINESS_PREFLIGHT_ONLY_STATUS,
        "gate": S09_MES_STRATEGY_INPUT_READINESS_GATE,
        "lane_class": config.lane_class.value,
        "root": MES_ROOT,
        "row_id": MES_ROW_ID,
        "evidence_completion_status": S09_MES_EVIDENCE_COMPLETION_LOCKED_STATUS,
        "evidence_handoff_status": S09_MES_EVIDENCE_COMPLETION_HANDOFF_STATUS,
        "strategy_input_readiness_status": S09_MES_EVIDENCE_AWAITING_READINESS_STATUS,
        "machinery_development_slice": S09_MES_MACHINERY_DEVELOPMENT_SLICE_TEXT,
        "databento_api_access": "NO",
        "market_row_parsing": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
    }


def s09_mes_roll_risk_cost_execution_output_manifest(
    request: S09MESRollRiskCostExecutionOutputManifestRequest,
) -> S09MESRollRiskCostExecutionOutputManifestResult:
    require_source_native(request.lane_class)
    if request.root != MES_ROOT:
        raise CarverBlocked("S09 MES roll-risk-cost output manifest forbids non-MES substitution")
    if request.row_id != MES_ROW_ID:
        raise CarverBlocked("S09 MES roll-risk-cost output manifest requires Appendix C MES row id")
    if request.gate_name != S09_MES_ROLL_RISK_COST_EXECUTION_GATE_NAME:
        raise CarverBlocked("S09 MES roll-risk-cost output manifest gate name is not locked")
    if request.output_root != S09_MES_ROLL_RISK_COST_OUTPUT_ROOT:
        raise CarverBlocked("S09 MES roll-risk-cost output root must match the locked oldest-authorized window")

    _require_locked_status("S09 MES roll-risk-cost output manifest", request.manifest_status)
    _require_locked_status(
        "S09 MES roll-risk-cost authorization request",
        request.authorization_request_status,
    )
    _require_locked_status("S09 MES roll-risk-cost no-execution status", request.no_execution_status)

    actual_schemas: list[tuple[str, tuple[str, ...]]] = []
    seen_paths: set[str] = set()
    for artifact in request.artifact_schemas:
        require_non_empty_text("S09 MES roll-risk-cost artifact relative path", artifact.relative_path)
        if artifact.relative_path in seen_paths:
            raise CarverBlocked("S09 MES roll-risk-cost artifact paths must be unique")
        seen_paths.add(artifact.relative_path)
        _require_locked_status("S09 MES roll-risk-cost artifact schema", artifact.status)
        if not artifact.fields:
            raise CarverBlocked("S09 MES roll-risk-cost artifact fields must be non-empty")
        for field in artifact.fields:
            require_non_empty_text("S09 MES roll-risk-cost artifact field", field)
        actual_schemas.append((artifact.relative_path, artifact.fields))

    if tuple(actual_schemas) != S09_MES_ROLL_RISK_COST_EXPECTED_ARTIFACT_SCHEMAS:
        raise CarverBlocked("S09 MES roll-risk-cost output manifest does not match the locked artifact schema")

    return S09MESRollRiskCostExecutionOutputManifestResult(
        manifest_status=S09_MES_ROLL_RISK_COST_OUTPUT_MANIFEST_READY_STATUS,
        output_root=S09_MES_ROLL_RISK_COST_OUTPUT_ROOT,
        artifact_schemas=request.artifact_schemas,
    )


def s09_mes_total_cost_from_locked_components(
    request: S09MESCostComponentSetRequest,
) -> S09MESCostComponentSetResult:
    require_source_native(request.lane_class)
    if request.root != MES_ROOT:
        raise CarverBlocked("S09 MES cost lock forbids non-MES substitution")
    if request.row_id != MES_ROW_ID:
        raise CarverBlocked("S09 MES cost lock requires Appendix C MES row id")
    if type(request.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES cost lock requires an exact completed trading date")
    if request.component_set_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES cost component set is unresolved")

    components_by_name: dict[str, S09MESLockedCostComponent] = {}
    for component in request.components:
        _validate_cost_component(component, request.completed_trading_date)
        if component.component_name in components_by_name:
            raise CarverBlocked("S09 MES cost component names must be unique")
        components_by_name[component.component_name] = component

    if tuple(components_by_name) != S09_MES_REQUIRED_COST_COMPONENTS:
        raise CarverBlocked("S09 MES cost components must include the complete required source-native set")

    round_turn_costs = tuple(
        (name, _round_turn_cost(components_by_name[name]))
        for name in S09_MES_REQUIRED_COST_COMPONENTS
    )
    total = sum(cost for _, cost in round_turn_costs)
    _require_finite_positive("S09 MES total cost per trade", total)
    return S09MESCostComponentSetResult(
        total_cost_per_trade_currency=total,
        currency="USD",
        component_round_turn_costs=round_turn_costs,
        cost_basis="LOCKED_MES_COST_COMPONENTS_ROUND_TURN_PER_TRADE_USD",
    )


def s09_mes_risk_adjusted_cost_from_locked_inputs(
    request: S09MESRiskAdjustedCostRequest,
) -> S09MESRiskAdjustedCostResult:
    require_source_native(request.lane_class)
    if request.total_cost_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES total cost per trade must be locked before risk-adjusted cost")
    if request.daily_price_risk_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES daily price risk must be locked before risk-adjusted cost")
    _require_finite_positive("S09 MES total cost per trade", request.total_cost_per_trade_currency)
    _require_finite_positive("S09 MES daily price risk", request.daily_price_risk_currency)
    _require_finite_positive("S09 MES contract multiplier", request.contract_multiplier_usd_per_point)
    if request.contract_multiplier_usd_per_point != S09_MES_CONTRACT_MULTIPLIER_USD_PER_POINT:
        raise CarverBlocked("S09 MES contract multiplier must be locked to 5 USD per index point")
    annualized_price_risk = (
        request.daily_price_risk_currency
        * S09_MES_DAILY_TO_ANNUAL_RISK_SCALAR
        * request.contract_multiplier_usd_per_point
    )
    return S09MESRiskAdjustedCostResult(
        total_cost_per_trade_currency=request.total_cost_per_trade_currency,
        daily_price_risk_currency=request.daily_price_risk_currency,
        annualized_price_risk_currency=annualized_price_risk,
        risk_adjusted_cost_per_trade_sr=request.total_cost_per_trade_currency / annualized_price_risk,
        cost_basis="LOCKED_TOTAL_COST_PER_TRADE_OVER_LOCKED_ANNUALIZED_USD_PRICE_RISK_FROM_DAILY_X16_X_MES_MULTIPLIER",
    )


def s09_mes_speed_eligibility_from_risk_adjusted_cost(
    request: S09MESRiskAdjustedCostSpeedEligibilityRequest,
) -> S09MESRiskAdjustedCostSpeedEligibilityResult:
    require_source_native(request.lane_class)
    if request.risk_adjusted_cost_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES risk-adjusted cost must be locked before speed eligibility")
    if request.threshold_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES cost threshold source is unresolved")
    if request.turnover_status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES turnover table source is unresolved")
    _require_finite_positive("S09 MES risk-adjusted cost per trade", request.risk_adjusted_cost_per_trade_sr)
    _require_finite_positive("S09 MES cost threshold", request.threshold_sr)
    if request.threshold_sr != S09_MES_COST_THRESHOLD_SR:
        raise CarverBlocked("S09 MES cost threshold must be the source-locked 0.15 SR")

    eligible_spans = tuple(
        span
        for span in S09_EWMAC_SPANS
        if S09_MES_EWMAC_TURNOVER_BY_SPAN[span] * request.risk_adjusted_cost_per_trade_sr <= request.threshold_sr
    )
    if not eligible_spans:
        raise CarverBlocked("S09 MES cost screen leaves no eligible EWMAC speeds")
    rejected_spans = tuple(span for span in S09_EWMAC_SPANS if span not in eligible_spans)
    fdm = s09_fdm_for_allowed_spans(eligible_spans)
    return S09MESRiskAdjustedCostSpeedEligibilityResult(
        eligible_spans=eligible_spans,
        rejected_spans=rejected_spans,
        fdm=fdm,
        threshold_sr=request.threshold_sr,
        risk_adjusted_cost_per_trade_sr=request.risk_adjusted_cost_per_trade_sr,
        eligibility_basis="LOCKED_COST_SCREEN_0_15_SR_THRESHOLD_PRECOMPUTED_RISK_ADJUSTED_COST",
    )


def _blockers(request: S09MESStrategyInputReadinessRequest) -> tuple[str, ...]:
    blockers: list[str] = []
    try:
        require_source_native(request.lane_class)
    except CarverBlocked as exc:
        blockers.append(str(exc))
    try:
        require_non_empty_text("S09 MES root", request.root)
        require_non_empty_text("S09 MES row id", request.row_id)
        require_non_empty_text("S09 MES expansion status", request.expansion_status)
        require_non_empty_text("S09 MES speed eligibility basis", request.speed_eligibility_basis)
    except CarverBlocked as exc:
        blockers.append(str(exc))
    if request.root != MES_ROOT:
        blockers.append("S09 MES readiness forbids ES/NQ/full-size substitution")
    if request.row_id != MES_ROW_ID:
        blockers.append("S09 MES readiness requires Appendix C MES row id")
    if request.expansion_status != MES_EXPANSION_PASS_STATUS:
        blockers.append("S09 MES Databento daily expansion must pass before readiness")
    for name, status in _status_items(request):
        if status is not SourceRuleStatus.LOCKED:
            blockers.append(f"{name} is not locked")
    expected_fdm = _expected_fdm(request.eligible_spans, blockers)
    if expected_fdm is not None and request.fdm != expected_fdm:
        blockers.append("S09 MES FDM must match Table 36 row for eligible speed set")
    normalized_basis = request.speed_eligibility_basis.upper().strip()
    if normalized_basis.startswith("ASSUMED_") or normalized_basis in {"ASSUMED", "ASSUMPTION", "ASSUMED_ALL_SIX_SPEEDS"}:
        blockers.append("S09 MES readiness may not assume all six speeds survive cost filtering")
    return tuple(blockers)


def _status_items(request: S09MESStrategyInputReadinessRequest) -> tuple[tuple[str, SourceRuleStatus], ...]:
    return (
        ("continuous lineage", request.continuous_lineage_status),
        ("roll plan", request.roll_plan_status),
        ("roll date normalization", request.roll_date_normalization_status),
        ("back adjustment", request.back_adjustment_status),
        ("provider condition admission", request.provider_condition_admission_status),
        ("oldest authorized data ordering", request.oldest_authorized_data_ordering_status),
        ("Development/Reconciliation window", request.development_reconciliation_window_status),
        ("annual risk runtime", request.annual_risk_runtime_status),
        ("daily price risk runtime", request.daily_price_risk_runtime_status),
        ("cost source", request.cost_source_status),
        ("historical cost values", request.historical_cost_values_status),
        ("risk-adjusted cost", request.risk_adjusted_cost_status),
        ("speed cost eligibility", request.speed_cost_eligibility_status),
        ("eligible speed set", request.eligible_speed_set_status),
        ("Table 36 FDM row", request.table36_fdm_row_status),
        ("hash-bound provenance", request.hash_bound_provenance_status),
    )


def _expected_fdm(spans: tuple[int, ...], blockers: list[str]) -> float | None:
    try:
        return s09_fdm_for_allowed_spans(spans)
    except CarverBlocked as exc:
        blockers.append(str(exc))
        return None


def _require_finite_positive(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"{name} must be finite and positive")


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be finite and non-negative")


def _require_locked_status(name: str, status: SourceRuleStatus) -> None:
    if status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked(f"{name} is not locked")


def _require_no_preflight_access(name: str, authorized: bool) -> None:
    if authorized is not False:
        raise CarverBlocked(f"S09 MES strategy-input readiness preflight forbids {name} access")


def _require_strict_completed_date_sequence(name: str, values: tuple[date, ...]) -> tuple[date, ...]:
    if not values:
        raise CarverBlocked(f"{name} must be non-empty")
    previous: date | None = None
    for value in values:
        if type(value) is not date:
            raise CarverBlocked(f"{name} must contain exact completed dates")
        if previous is not None and value <= previous:
            raise CarverBlocked(f"{name} must be strictly increasing")
        previous = value
    return values


def _validate_cost_component(component: S09MESLockedCostComponent, completed_trading_date: date) -> None:
    if component.status is not SourceRuleStatus.LOCKED:
        raise CarverBlocked("S09 MES cost component is unresolved")
    if component.component_name not in S09_MES_REQUIRED_COST_COMPONENTS:
        raise CarverBlocked("S09 MES cost component name is not in the required set")
    _require_finite_non_negative(f"S09 MES {component.component_name}", component.amount_currency)
    if component.currency != "USD":
        raise CarverBlocked("S09 MES cost component currency must be USD")
    if component.charge_timing not in S09_MES_COST_CHARGE_TIMINGS:
        raise CarverBlocked("S09 MES cost component charge timing must be PER_SIDE or ROUND_TURN")
    if type(component.effective_start) is not date or type(component.effective_end) is not date:
        raise CarverBlocked("S09 MES cost component effective dates must be exact dates")
    if component.effective_start > completed_trading_date or component.effective_end < completed_trading_date:
        raise CarverBlocked("S09 MES cost component effective range must cover completed trading date")
    require_non_empty_text("S09 MES cost component source label", component.source_label)
    if not isinstance(component.source_sha256, str) or len(component.source_sha256) != 64:
        raise CarverBlocked("S09 MES cost component source hash is missing")
    try:
        int(component.source_sha256, 16)
    except ValueError as exc:
        raise CarverBlocked("S09 MES cost component source hash is invalid") from exc


def _round_turn_cost(component: S09MESLockedCostComponent) -> float:
    if component.charge_timing == "PER_SIDE":
        return component.amount_currency * 2
    return component.amount_currency

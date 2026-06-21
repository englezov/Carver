from __future__ import annotations

import csv
import hashlib
import json
import sys
from io import StringIO
from dataclasses import dataclass
from datetime import date
from math import isfinite
from numbers import Real
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked

STAMP = "20260603"
DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE = (
    "DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE: this executable targets the superseded "
    "2022-01-03 through 2023-12-29 development window. Use the oldest minimum machinery-development "
    "slice 2019-05-05 through 2020-04-05 via the authorized machinery-dev/evidence-completion path."
)
TARGET_WINDOW = "2022-01-03_2023-12-29"
TARGET_WINDOW_TEXT = "2022-01-03 through 2023-12-29"
EXECUTION_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_roll_date_normalization_runtime_risk_cost_execution" / TARGET_WINDOW
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_RESULT_2026-06-03.md"
AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_LOCAL_HOSTILE_AUDIT_2026-06-03.md"

S09_MES_ROLL_NORMALIZATION_LEDGER_COLUMNS = (
    "provider_date",
    "completed_trading_date",
    "old_symbol",
    "new_symbol",
    "authority_source",
    "authority_sha256",
    "status",
)
S09_MES_ROLL_NORMALIZATION_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_COMPLETED_TRADING_DATE"
S09_MES_ANNUAL_RISK_RUNTIME_LEDGER_COLUMNS = (
    "completed_trading_date",
    "long_run_annual_risk",
    "current_ewma32_annual_risk",
    "annual_percentage_risk",
    "source_sha256",
    "status",
)
S09_MES_DAILY_PRICE_RISK_RUNTIME_LEDGER_COLUMNS = (
    "completed_trading_date",
    "current_price",
    "annual_percentage_risk",
    "daily_price_risk_currency",
    "source_sha256",
    "status",
)
S09_MES_COST_VALUE_LEDGER_COLUMNS = (
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
S09_MES_RISK_ADJUSTED_COST_LEDGER_COLUMNS = (
    "completed_trading_date",
    "total_cost_per_trade_currency",
    "daily_price_risk_currency",
    "risk_adjusted_cost_per_trade_sr",
    "status",
)
S09_MES_SPEED_ELIGIBILITY_LEDGER_COLUMNS = (
    "span",
    "turnover",
    "risk_adjusted_cost_per_trade_sr",
    "threshold_sr",
    "eligible",
    "status",
)
S09_MES_ANNUAL_RISK_RUNTIME_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE"
S09_MES_DAILY_PRICE_RISK_RUNTIME_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE"
S09_MES_COST_VALUE_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE"
S09_MES_RISK_ADJUSTED_COST_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE"
S09_MES_SPEED_ELIGIBILITY_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"
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
S09_MES_EWMAC_TURNOVER_BY_SPAN = {
    2: 98.5,
    4: 50.2,
    8: 25.4,
    16: 13.2,
    32: 7.6,
    64: 5.2,
}
S09_MES_COST_THRESHOLD_SR = 0.15
S09_MES_EXECUTION_STATUS_READY = "READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST"
S09_MES_EXECUTION_STATUS_FAIL_CLOSED = "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY"
S09_MES_READY_READINESS_STATUS = "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY"
S09_MES_ALLOWED_FAIL_CLOSED_READINESS_STATUS = "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY"


@dataclass(frozen=True)
class S09MESRollRiskCostExecutionConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    target_start: str
    target_end: str


@dataclass(frozen=True)
class S09MESRollNormalizationLedgerRow:
    provider_date: date
    completed_trading_date: date
    old_symbol: str
    new_symbol: str
    authority_source: str
    authority_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESAnnualRiskRuntimeLedgerRow:
    completed_trading_date: date
    long_run_annual_risk: float
    current_ewma32_annual_risk: float
    annual_percentage_risk: float
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESDailyPriceRiskRuntimeLedgerRow:
    completed_trading_date: date
    current_price: float
    annual_percentage_risk: float
    daily_price_risk_currency: float
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESCostValueLedgerRow:
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
class S09MESRiskAdjustedCostLedgerRow:
    completed_trading_date: date
    total_cost_per_trade_currency: float
    daily_price_risk_currency: float
    risk_adjusted_cost_per_trade_sr: float
    status: str


@dataclass(frozen=True)
class S09MESSpeedEligibilityLedgerRow:
    span: int
    turnover: float
    risk_adjusted_cost_per_trade_sr: float
    threshold_sr: float
    eligible: bool
    status: str


@dataclass(frozen=True)
class S09MESRollRiskCostExecutionStatus:
    status: str
    databento_api_access: str
    new_provider_data_download: str
    market_row_parsing: str
    strategy_input_readiness_status: str


def run_s09_mes_roll_risk_cost_execution(config: S09MESRollRiskCostExecutionConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES roll risk cost execution is not operator-authorized")
    if config.lane_class != "SOURCE_NATIVE_FUTURES":
        raise CarverBlocked("S09 MES execution is source-native futures only")
    if config.root != "MES" or config.row_id != "APPENDIX_C_174_006":
        raise CarverBlocked("S09 MES execution is locked to Appendix C MES row")
    if config.target_start != "2022-01-03" or config.target_end != "2023-12-29":
        raise CarverBlocked("S09 MES execution target window is not locked")
    return {"status": "AUTHORIZED_PREFLIGHT_ONLY_NOT_EXECUTED"}


def render_s09_mes_roll_normalization_ledger_csv(rows: tuple[S09MESRollNormalizationLedgerRow, ...]) -> str:
    if not rows:
        raise CarverBlocked("S09 MES roll normalization ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(S09_MES_ROLL_NORMALIZATION_LEDGER_COLUMNS)
    for row in rows:
        _validate_roll_normalization_ledger_row(row)
        writer.writerow(
            (
                row.provider_date.isoformat(),
                row.completed_trading_date.isoformat(),
                row.old_symbol,
                row.new_symbol,
                row.authority_source,
                row.authority_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_annual_risk_runtime_ledger_csv(rows: tuple[S09MESAnnualRiskRuntimeLedgerRow, ...]) -> str:
    if not rows:
        raise CarverBlocked("S09 MES annual risk runtime ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(S09_MES_ANNUAL_RISK_RUNTIME_LEDGER_COLUMNS)
    for row in rows:
        _validate_annual_risk_runtime_ledger_row(row)
        writer.writerow(
            (
                row.completed_trading_date.isoformat(),
                row.long_run_annual_risk,
                row.current_ewma32_annual_risk,
                row.annual_percentage_risk,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_daily_price_risk_runtime_ledger_csv(rows: tuple[S09MESDailyPriceRiskRuntimeLedgerRow, ...]) -> str:
    if not rows:
        raise CarverBlocked("S09 MES daily price-risk runtime ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(S09_MES_DAILY_PRICE_RISK_RUNTIME_LEDGER_COLUMNS)
    for row in rows:
        _validate_daily_price_risk_runtime_ledger_row(row)
        writer.writerow(
            (
                row.completed_trading_date.isoformat(),
                row.current_price,
                row.annual_percentage_risk,
                row.daily_price_risk_currency,
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_cost_value_ledger_csv(rows: tuple[S09MESCostValueLedgerRow, ...]) -> str:
    if not rows:
        raise CarverBlocked("S09 MES cost value ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(S09_MES_COST_VALUE_LEDGER_COLUMNS)
    for row in rows:
        _validate_cost_value_ledger_row(row)
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


def render_s09_mes_risk_adjusted_cost_ledger_csv(rows: tuple[S09MESRiskAdjustedCostLedgerRow, ...]) -> str:
    if not rows:
        raise CarverBlocked("S09 MES risk-adjusted cost ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(S09_MES_RISK_ADJUSTED_COST_LEDGER_COLUMNS)
    for row in rows:
        _validate_risk_adjusted_cost_ledger_row(row)
        writer.writerow(
            (
                row.completed_trading_date.isoformat(),
                row.total_cost_per_trade_currency,
                row.daily_price_risk_currency,
                row.risk_adjusted_cost_per_trade_sr,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_speed_eligibility_ledger_csv(rows: tuple[S09MESSpeedEligibilityLedgerRow, ...]) -> str:
    if not rows:
        raise CarverBlocked("S09 MES speed eligibility ledger requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(S09_MES_SPEED_ELIGIBILITY_LEDGER_COLUMNS)
    for row in rows:
        _validate_speed_eligibility_ledger_row(row)
        writer.writerow(
            (
                row.span,
                row.turnover,
                row.risk_adjusted_cost_per_trade_sr,
                row.threshold_sr,
                row.eligible,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_roll_risk_cost_execution_status_json(payload: S09MESRollRiskCostExecutionStatus) -> str:
    _validate_roll_risk_cost_execution_status(payload)
    return json.dumps(
        {
            "databento_api_access": payload.databento_api_access,
            "market_row_parsing": payload.market_row_parsing,
            "new_provider_data_download": payload.new_provider_data_download,
            "status": payload.status,
            "strategy_input_readiness_status": payload.strategy_input_readiness_status,
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def _validate_roll_normalization_ledger_row(row: S09MESRollNormalizationLedgerRow) -> None:
    if type(row.provider_date) is not date:
        raise CarverBlocked("S09 MES roll normalization ledger provider date must be an exact date")
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES roll normalization ledger completed trading date must be an exact date")
    _require_mes_symbol("S09 MES roll normalization old symbol", row.old_symbol)
    _require_mes_symbol("S09 MES roll normalization new symbol", row.new_symbol)
    if row.old_symbol >= row.new_symbol:
        raise CarverBlocked("S09 MES roll normalization symbols must advance in contract order")
    if not row.authority_source:
        raise CarverBlocked("S09 MES roll normalization authority source is missing")
    if not isinstance(row.authority_sha256, str) or len(row.authority_sha256) != 64:
        raise CarverBlocked("S09 MES roll normalization authority hash is missing")
    try:
        int(row.authority_sha256, 16)
    except ValueError as exc:
        raise CarverBlocked("S09 MES roll normalization authority hash is invalid") from exc
    if row.status != S09_MES_ROLL_NORMALIZATION_LOCKED_STATUS:
        raise CarverBlocked("S09 MES roll normalization ledger row status is not locked")


def _validate_annual_risk_runtime_ledger_row(row: S09MESAnnualRiskRuntimeLedgerRow) -> None:
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES annual risk runtime ledger completed trading date must be an exact date")
    _require_finite_positive("S09 MES long-run annual risk", row.long_run_annual_risk)
    _require_finite_positive("S09 MES EWMA32 current annual risk", row.current_ewma32_annual_risk)
    _require_finite_positive("S09 MES annual percentage risk", row.annual_percentage_risk)
    expected = (
        S09_MES_ANNUAL_RISK_LONG_RUN_WEIGHT * float(row.long_run_annual_risk)
        + S09_MES_ANNUAL_RISK_CURRENT_WEIGHT * float(row.current_ewma32_annual_risk)
    )
    if abs(float(row.annual_percentage_risk) - expected) > 1e-12:
        raise CarverBlocked("S09 MES annual risk runtime ledger does not match locked 30/70 blend")
    _require_sha256("S09 MES annual risk runtime source hash", row.source_sha256)
    if row.status != S09_MES_ANNUAL_RISK_RUNTIME_LOCKED_STATUS:
        raise CarverBlocked("S09 MES annual risk runtime ledger row status is not locked")


def _validate_daily_price_risk_runtime_ledger_row(row: S09MESDailyPriceRiskRuntimeLedgerRow) -> None:
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES daily price-risk runtime ledger completed trading date must be an exact date")
    _require_finite_positive("S09 MES current price", row.current_price)
    _require_finite_positive("S09 MES annual percentage risk", row.annual_percentage_risk)
    _require_finite_positive("S09 MES daily price risk", row.daily_price_risk_currency)
    expected = float(row.current_price) * float(row.annual_percentage_risk) / 16
    if abs(float(row.daily_price_risk_currency) - expected) > 1e-12:
        raise CarverBlocked("S09 MES daily price-risk runtime ledger does not match locked price-risk formula")
    _require_sha256("S09 MES daily price-risk runtime source hash", row.source_sha256)
    if row.status != S09_MES_DAILY_PRICE_RISK_RUNTIME_LOCKED_STATUS:
        raise CarverBlocked("S09 MES daily price-risk runtime ledger row status is not locked")


def _validate_cost_value_ledger_row(row: S09MESCostValueLedgerRow) -> None:
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES cost value ledger completed trading date must be an exact date")
    if row.component_name not in S09_MES_REQUIRED_COST_COMPONENTS:
        raise CarverBlocked("S09 MES cost value ledger component name is not in the required set")
    _require_finite_non_negative(f"S09 MES {row.component_name} cost value", row.amount_currency)
    if row.currency != "USD":
        raise CarverBlocked("S09 MES cost value ledger currency must be USD")
    if row.charge_timing not in S09_MES_COST_CHARGE_TIMINGS:
        raise CarverBlocked("S09 MES cost value ledger charge timing must be PER_SIDE or ROUND_TURN")
    if type(row.effective_start) is not date or type(row.effective_end) is not date:
        raise CarverBlocked("S09 MES cost value ledger effective dates must be exact dates")
    if row.effective_start > row.completed_trading_date or row.effective_end < row.completed_trading_date:
        raise CarverBlocked("S09 MES cost value ledger effective range must cover completed trading date")
    if not row.source_label:
        raise CarverBlocked("S09 MES cost value ledger source label is missing")
    _require_sha256("S09 MES cost value ledger source hash", row.source_sha256)
    if row.status != S09_MES_COST_VALUE_LOCKED_STATUS:
        raise CarverBlocked("S09 MES cost value ledger row status is not locked")


def _validate_risk_adjusted_cost_ledger_row(row: S09MESRiskAdjustedCostLedgerRow) -> None:
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES risk-adjusted cost ledger completed trading date must be an exact date")
    _require_finite_positive("S09 MES total cost per trade", row.total_cost_per_trade_currency)
    _require_finite_positive("S09 MES daily price risk", row.daily_price_risk_currency)
    _require_finite_positive("S09 MES risk-adjusted cost per trade", row.risk_adjusted_cost_per_trade_sr)
    expected = float(row.total_cost_per_trade_currency) / (
        float(row.daily_price_risk_currency)
        * S09_MES_DAILY_TO_ANNUAL_RISK_SCALAR
        * S09_MES_CONTRACT_MULTIPLIER_USD_PER_POINT
    )
    if abs(float(row.risk_adjusted_cost_per_trade_sr) - expected) > 1e-12:
        raise CarverBlocked("S09 MES risk-adjusted cost ledger does not match locked total-cost-over-annualized-USD-risk formula")
    if row.status != S09_MES_RISK_ADJUSTED_COST_LOCKED_STATUS:
        raise CarverBlocked("S09 MES risk-adjusted cost ledger row status is not locked")


def _validate_speed_eligibility_ledger_row(row: S09MESSpeedEligibilityLedgerRow) -> None:
    if isinstance(row.span, bool) or row.span not in S09_MES_EWMAC_TURNOVER_BY_SPAN:
        raise CarverBlocked("S09 MES speed eligibility ledger span is not in the locked EWMAC set")
    _require_finite_positive("S09 MES turnover", row.turnover)
    if row.turnover != S09_MES_EWMAC_TURNOVER_BY_SPAN[row.span]:
        raise CarverBlocked("S09 MES speed eligibility ledger turnover does not match locked table")
    _require_finite_positive("S09 MES risk-adjusted cost per trade", row.risk_adjusted_cost_per_trade_sr)
    _require_finite_positive("S09 MES speed eligibility threshold", row.threshold_sr)
    if row.threshold_sr != S09_MES_COST_THRESHOLD_SR:
        raise CarverBlocked("S09 MES speed eligibility threshold must be locked to 0.15 SR")
    if type(row.eligible) is not bool:
        raise CarverBlocked("S09 MES speed eligibility flag must be boolean")
    expected_eligible = row.turnover * row.risk_adjusted_cost_per_trade_sr <= row.threshold_sr
    if row.eligible is not expected_eligible:
        raise CarverBlocked("S09 MES speed eligibility flag does not match locked cost screen")
    if row.status != S09_MES_SPEED_ELIGIBILITY_LOCKED_STATUS:
        raise CarverBlocked("S09 MES speed eligibility ledger row status is not locked")


def _validate_roll_risk_cost_execution_status(payload: S09MESRollRiskCostExecutionStatus) -> None:
    if payload.status not in {S09_MES_EXECUTION_STATUS_READY, S09_MES_EXECUTION_STATUS_FAIL_CLOSED}:
        raise CarverBlocked("S09 MES execution status JSON has an unauthorized status")
    if payload.databento_api_access != "NO":
        raise CarverBlocked("S09 MES execution status JSON must not record Databento API access")
    if payload.new_provider_data_download != "NO":
        raise CarverBlocked("S09 MES execution status JSON must not record provider download")
    if payload.market_row_parsing != "NO":
        raise CarverBlocked("S09 MES execution status JSON must not record market-row parsing")
    if payload.status == S09_MES_EXECUTION_STATUS_READY:
        if payload.strategy_input_readiness_status != S09_MES_READY_READINESS_STATUS:
            raise CarverBlocked("S09 MES ready status JSON requires locked strategy input readiness")
    if payload.status == S09_MES_EXECUTION_STATUS_FAIL_CLOSED:
        if payload.strategy_input_readiness_status != S09_MES_ALLOWED_FAIL_CLOSED_READINESS_STATUS:
            raise CarverBlocked("S09 MES fail-closed status JSON requires fail-closed strategy input readiness")


def _require_mes_symbol(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.startswith("MES") or len(value) < 5:
        raise CarverBlocked(f"{name} must be an MES dated contract")


def _require_finite_positive(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"{name} must be finite and positive")


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be finite and non-negative")


def _require_sha256(name: str, value: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise CarverBlocked(f"{name} is missing")
    try:
        int(value, 16)
    except ValueError as exc:
        raise CarverBlocked(f"{name} is invalid") from exc


def _write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _render_header_only_csv(columns: tuple[str, ...]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(columns)
    return buffer.getvalue()


def _write_header_only_fail_closed_ledgers() -> tuple[Path, ...]:
    return (
        _write_text(
            EXECUTION_ROOT
            / "roll_date_normalization"
            / f"{STAMP}_S09_MES_ROLL_DATE_NORMALIZATION_ledger.csv",
            _render_header_only_csv(S09_MES_ROLL_NORMALIZATION_LEDGER_COLUMNS),
        ),
        _write_text(
            EXECUTION_ROOT / "risk" / f"{STAMP}_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
            _render_header_only_csv(S09_MES_ANNUAL_RISK_RUNTIME_LEDGER_COLUMNS),
        ),
        _write_text(
            EXECUTION_ROOT / "risk" / f"{STAMP}_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv",
            _render_header_only_csv(S09_MES_DAILY_PRICE_RISK_RUNTIME_LEDGER_COLUMNS),
        ),
        _write_text(
            EXECUTION_ROOT / "cost" / f"{STAMP}_S09_MES_COST_VALUE_ledger.csv",
            _render_header_only_csv(S09_MES_COST_VALUE_LEDGER_COLUMNS),
        ),
        _write_text(
            EXECUTION_ROOT / "cost" / f"{STAMP}_S09_MES_RISK_ADJUSTED_COST_ledger.csv",
            _render_header_only_csv(S09_MES_RISK_ADJUSTED_COST_LEDGER_COLUMNS),
        ),
        _write_text(
            EXECUTION_ROOT / "speed" / f"{STAMP}_S09_MES_SPEED_ELIGIBILITY_ledger.csv",
            _render_header_only_csv(S09_MES_SPEED_ELIGIBILITY_LEDGER_COLUMNS),
        ),
    )


def _write_fail_closed_execution_artifacts() -> tuple[Path, ...]:
    status_path = _write_text(
        EXECUTION_ROOT / "status" / f"{STAMP}_S09_MES_ROLL_RISK_COST_EXECUTION_status.json",
        render_s09_mes_roll_risk_cost_execution_status_json(
            S09MESRollRiskCostExecutionStatus(
                status=S09_MES_EXECUTION_STATUS_FAIL_CLOSED,
                databento_api_access="NO",
                new_provider_data_download="NO",
                market_row_parsing="NO",
                strategy_input_readiness_status=S09_MES_ALLOWED_FAIL_CLOSED_READINESS_STATUS,
            )
        ),
    )
    ledger_paths = _write_header_only_fail_closed_ledgers()
    provenance_path = _write_text(
        EXECUTION_ROOT / "provenance" / f"{STAMP}_S09_MES_ROLL_RISK_COST_EXECUTION_provenance.md",
        _render_provenance_text(),
    )
    result_path = _write_text(RESULT_PATH, _render_result_text(status_path, ledger_paths, provenance_path))
    audit_path = _write_text(AUDIT_PATH, _render_audit_text(status_path, ledger_paths, provenance_path, result_path))
    paths_without_hashes = (*ledger_paths, status_path, provenance_path, result_path, audit_path)
    hashes_path = _write_text(
        EXECUTION_ROOT / "hashes" / f"{STAMP}_S09_MES_ROLL_RISK_COST_EXECUTION_sha256.txt",
        _render_sha256_manifest(paths_without_hashes),
    )
    return (*paths_without_hashes, hashes_path)


def _render_provenance_text() -> str:
    return f"""# S09 MES Roll Risk Cost Execution Provenance

Date: 2026-06-03

Status:

```text
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
```

Authorized bounded gate:

```text
S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE
```

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- target_window: {TARGET_WINDOW_TEXT}
- design_ordering: oldest authorized completed source-native data first
- Databento API access: NO
- new provider data download: NO
- market-row parsing: NO

Execution result:

The gate was executed only against local locked/process artifacts. Required
source-native runtime annual-risk values, daily price-risk values, historical MES
cost values, risk-adjusted cost values, and speed eligibility values were not
all locked as executable inputs. The gate therefore emitted fail-closed status
and header-only ledger files rather than fabricating values.

Boundary:

There was no forecast computation, no diagnostics, no backtests, no OOS, no
Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging,
no commit, no push, no PR, and no remote operation.
"""


def _render_result_text(status_path: Path, ledger_paths: tuple[Path, ...], provenance_path: Path) -> str:
    relative_ledgers = "\n".join(f"- `{path.relative_to(ROOT).as_posix()}`" for path in ledger_paths)
    return f"""# S09 MES Roll Date Normalization Runtime Risk Cost Execution Result

Date: 2026-06-03

Status:

```text
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
```

Authorized execution scope:

```text
S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE
```

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- target_window: {TARGET_WINDOW_TEXT}
- design_ordering: oldest authorized completed source-native data first

Operator authorization received for the bounded execution step. This execution
did not include Databento API access, provider login, OHLCV request, new data
download, market-row parsing, CFD adapter work, or old QuantLab active-pipeline
use.

Outcome:

The gate executed and failed closed because executable source-native runtime
risk values and historical cost values are not locked as strategy-input values.
Ledger families were emitted as header-only fail-closed artifacts so downstream
steps cannot mistake this packet for ready strategy input.

Written artifacts:

- `{status_path.relative_to(ROOT).as_posix()}`
- `{provenance_path.relative_to(ROOT).as_posix()}`
{relative_ledgers}

Boundary preserved:

- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no OOS
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
"""


def _render_audit_text(status_path: Path, ledger_paths: tuple[Path, ...], provenance_path: Path, result_path: Path) -> str:
    relative_ledgers = "\n".join(f"- `{path.relative_to(ROOT).as_posix()}`" for path in ledger_paths)
    return f"""# S09 MES Roll Risk Cost Execution Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_ROLL_RISK_COST_EXECUTION_FAIL_CLOSED_NO_BACKTEST
```

Audit scope:

- gate: S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- root: MES
- target_window: {TARGET_WINDOW_TEXT}
- design_ordering: oldest authorized completed source-native data first

Observed artifacts:

- `{result_path.relative_to(ROOT).as_posix()}`
- `{status_path.relative_to(ROOT).as_posix()}`
- `{provenance_path.relative_to(ROOT).as_posix()}`
{relative_ledgers}

Hostile checks:

- no Databento API access
- no provider download
- no market-row parsing
- no fabricated risk values
- no fabricated cost values
- no default all-six-speed assumption
- no forecast computation
- no diagnostics
- no backtests
- no OOS
- no Lockbox
- no Forward
- no Git staging
"""


def _render_sha256_manifest(paths: tuple[Path, ...]) -> str:
    lines = []
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    return "\n".join(lines) + "\n"


def main() -> None:
    raise CarverBlocked(DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE)
    run_s09_mes_roll_risk_cost_execution(
        S09MESRollRiskCostExecutionConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            target_start="2022-01-03",
            target_end="2023-12-29",
        )
    )
    _write_fail_closed_execution_artifacts()
    print("S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_RESULT_WRITTEN")


if __name__ == "__main__":
    main()

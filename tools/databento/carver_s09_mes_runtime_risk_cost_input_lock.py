from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import date
from io import StringIO
from math import isfinite
from numbers import Real
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked

GATE = "S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
MACHINERY_DEVELOPMENT_SLICE_START = "2019-05-05"
MACHINERY_DEVELOPMENT_SLICE_END = "2020-04-05"
RUNTIME_INPUT_LOCK_SCOPE = "oldest minimum machinery-development slice only"
DESIGN_ORDERING = "oldest authorized completed source-native data first"
RUN_ID = "20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK"
OUTPUT_ROOT_RELATIVE = "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05"
OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s09"
    / "mes_runtime_risk_cost_input_lock"
    / "2019-05-05_2020-04-05"
)
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_RESULT_2026-06-03.md"
AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
INPUT_MANIFEST_COLUMNS = ("input_name", "relative_path", "required_status", "sha256", "status")
INPUT_MANIFEST_LOCKED_STATUS = "HASH_BOUND_LOCAL_MACHINERY_SLICE_INPUT"
MACHINERY_SLICE_PATH_TOKEN = "2019-05-05_2020-04-05"
ANNUAL_RISK_LEDGER_COLUMNS = (
    "completed_trading_date",
    "long_run_annual_risk",
    "current_ewma32_annual_risk",
    "annual_percentage_risk",
    "source_sha256",
    "status",
)
DAILY_PRICE_RISK_LEDGER_COLUMNS = (
    "completed_trading_date",
    "current_price",
    "annual_percentage_risk",
    "daily_price_risk_currency",
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
    "status",
)
SPEED_ELIGIBILITY_LEDGER_COLUMNS = (
    "span",
    "turnover",
    "risk_adjusted_cost_per_trade_sr",
    "threshold_sr",
    "eligible",
    "status",
)
ANNUAL_RISK_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE"
DAILY_PRICE_RISK_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE"
COST_VALUE_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE"
RISK_ADJUSTED_COST_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE"
SPEED_ELIGIBILITY_LOCKED_STATUS = "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"
INPUT_LOCK_FAIL_CLOSED_STATUS = "FAIL_CLOSED_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_NOT_STRATEGY_READY"
STRATEGY_INPUT_NOT_READY_STATUS = "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY"
MACHINERY_DEVELOPMENT_SLICE_TEXT = "2019-05-05 through 2020-04-05"
ANNUAL_RISK_LONG_RUN_WEIGHT = 0.30
ANNUAL_RISK_CURRENT_WEIGHT = 0.70
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


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice_start: str
    machinery_development_slice_end: str
    runtime_input_lock_scope: str
    design_ordering: str
    databento_api_access_authorized: bool


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockInputManifestRow:
    input_name: str
    relative_path: str
    required_status: str
    sha256: str
    status: str


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockAnnualRiskLedgerRow:
    completed_trading_date: date
    long_run_annual_risk: float
    current_ewma32_annual_risk: float
    annual_percentage_risk: float
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockDailyPriceRiskLedgerRow:
    completed_trading_date: date
    current_price: float
    annual_percentage_risk: float
    daily_price_risk_currency: float
    source_sha256: str
    status: str


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockCostValueLedgerRow:
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
class S09MESRuntimeRiskCostInputLockRiskAdjustedCostLedgerRow:
    completed_trading_date: date
    total_cost_per_trade_currency: float
    daily_price_risk_currency: float
    risk_adjusted_cost_per_trade_sr: float
    status: str


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow:
    span: int
    turnover: float
    risk_adjusted_cost_per_trade_sr: float
    threshold_sr: float
    eligible: bool
    status: str


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockStatus:
    status: str
    gate: str
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    runtime_input_lock_scope: str
    design_ordering: str
    databento_api_access: str
    new_provider_data_download: str
    market_row_parsing: str
    forecast_computation: str
    diagnostics_run: str
    backtests_run: str
    test_validation_lockbox_forward_access: str
    strategy_input_readiness_status: str


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockHashManifestEntry:
    relative_path: str
    artifact_text: str


@dataclass(frozen=True)
class S09MESRuntimeRiskCostInputLockArtifactBundleRequest:
    input_manifest_csv: str
    annual_risk_csv: str
    daily_price_risk_csv: str
    cost_value_csv: str
    risk_adjusted_cost_csv: str
    speed_eligibility_csv: str
    status_json: str
    provenance_md: str


def run_s09_mes_runtime_risk_cost_input_lock(
    config: S09MESRuntimeRiskCostInputLockConfig,
) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES runtime risk/cost input lock is not operator-authorized")
    if config.databento_api_access_authorized:
        raise CarverBlocked("S09 MES runtime risk/cost input lock forbids Databento API access unless separately restated")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES runtime risk/cost input lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES runtime risk/cost input lock is locked to Appendix C MES row")
    if (
        config.machinery_development_slice_start != MACHINERY_DEVELOPMENT_SLICE_START
        or config.machinery_development_slice_end != MACHINERY_DEVELOPMENT_SLICE_END
    ):
        raise CarverBlocked("S09 MES runtime risk/cost input lock must use the oldest machinery-development slice")
    if config.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES runtime risk/cost input lock scope is not locked")
    if config.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES runtime risk/cost input lock must use oldest authorized data first")
    return build_s09_mes_runtime_risk_cost_input_lock_artifact_bundle(
        S09MESRuntimeRiskCostInputLockArtifactBundleRequest(
            input_manifest_csv=_header_csv(INPUT_MANIFEST_COLUMNS),
            annual_risk_csv=_header_csv(ANNUAL_RISK_LEDGER_COLUMNS),
            daily_price_risk_csv=_header_csv(DAILY_PRICE_RISK_LEDGER_COLUMNS),
            cost_value_csv=_header_csv(COST_VALUE_LEDGER_COLUMNS),
            risk_adjusted_cost_csv=_header_csv(RISK_ADJUSTED_COST_LEDGER_COLUMNS),
            speed_eligibility_csv=_header_csv(SPEED_ELIGIBILITY_LEDGER_COLUMNS),
            status_json=render_s09_mes_runtime_risk_cost_input_lock_status_json(_fail_closed_status_payload()),
            provenance_md=render_s09_mes_runtime_risk_cost_input_lock_provenance_md(_fail_closed_status_payload()),
        )
    )


def render_s09_mes_runtime_risk_cost_input_manifest_csv(
    rows: tuple[S09MESRuntimeRiskCostInputLockInputManifestRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES runtime risk/cost input manifest requires at least one row")

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(INPUT_MANIFEST_COLUMNS)
    for row in rows:
        _validate_input_manifest_row(row)
        writer.writerow(
            (
                row.input_name,
                row.relative_path,
                row.required_status,
                row.sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_runtime_risk_cost_annual_risk_ledger_csv(
    rows: tuple[S09MESRuntimeRiskCostInputLockAnnualRiskLedgerRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES annual risk runtime ledger requires at least one row")

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
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_runtime_risk_cost_daily_price_risk_ledger_csv(
    rows: tuple[S09MESRuntimeRiskCostInputLockDailyPriceRiskLedgerRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES daily price-risk runtime ledger requires at least one row")

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
                row.source_sha256,
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_runtime_risk_cost_cost_value_ledger_csv(
    rows: tuple[S09MESRuntimeRiskCostInputLockCostValueLedgerRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES cost value ledger requires at least one row")
    if tuple(row.component_name for row in rows) != REQUIRED_COST_COMPONENTS:
        raise CarverBlocked("S09 MES cost value ledger must contain the complete required component set in locked order")

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


def render_s09_mes_runtime_risk_cost_risk_adjusted_cost_ledger_csv(
    rows: tuple[S09MESRuntimeRiskCostInputLockRiskAdjustedCostLedgerRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES risk-adjusted cost ledger requires at least one row")

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
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_runtime_risk_cost_speed_eligibility_ledger_csv(
    rows: tuple[S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow, ...],
) -> str:
    if not rows:
        raise CarverBlocked("S09 MES speed eligibility ledger requires at least one row")
    if tuple(row.span for row in rows) != tuple(EWMAC_TURNOVER_BY_SPAN):
        raise CarverBlocked("S09 MES speed eligibility ledger must contain the complete locked EWMAC span set in order")

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
                row.status,
            )
        )
    return buffer.getvalue()


def render_s09_mes_runtime_risk_cost_input_lock_status_json(
    payload: S09MESRuntimeRiskCostInputLockStatus,
) -> str:
    _validate_status_payload(payload)
    return json.dumps(
        {
            "backtests_run": payload.backtests_run,
            "databento_api_access": payload.databento_api_access,
            "design_ordering": payload.design_ordering,
            "diagnostics_run": payload.diagnostics_run,
            "forecast_computation": payload.forecast_computation,
            "gate": payload.gate,
            "lane_class": payload.lane_class,
            "machinery_development_slice": payload.machinery_development_slice,
            "market_row_parsing": payload.market_row_parsing,
            "new_provider_data_download": payload.new_provider_data_download,
            "root": payload.root,
            "row_id": payload.row_id,
            "runtime_input_lock_scope": payload.runtime_input_lock_scope,
            "status": payload.status,
            "strategy_input_readiness_status": payload.strategy_input_readiness_status,
            "test_validation_lockbox_forward_access": payload.test_validation_lockbox_forward_access,
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_s09_mes_runtime_risk_cost_input_lock_provenance_md(
    payload: S09MESRuntimeRiskCostInputLockStatus,
) -> str:
    _validate_status_payload(payload)
    return f"""# S09 MES Runtime Risk Cost Input Lock Provenance

Status:

```text
{payload.status}
```

Scope:

- gate: {payload.gate}
- lane_class: {payload.lane_class}
- source_row: {payload.row_id}
- author_market_code: {payload.root}
- machinery_development_slice: {payload.machinery_development_slice}
- runtime_input_lock_scope: {payload.runtime_input_lock_scope}
- design_ordering: {payload.design_ordering}

Outcome:

The runtime risk/cost input-lock packet remains fail-closed and is not strategy
input ready. Any future execution must use hash-bound local machinery-slice
inputs only and must not consume TEST, VALIDATION, Lockbox, OOS, or Forward
data.

Boundary:

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations were performed.
"""


def render_s09_mes_runtime_risk_cost_input_lock_sha256_manifest(
    entries: tuple[S09MESRuntimeRiskCostInputLockHashManifestEntry, ...],
) -> str:
    if not entries:
        raise CarverBlocked("S09 MES input-lock SHA256 manifest requires at least one artifact")

    seen_paths: set[str] = set()
    lines: list[str] = []
    for entry in sorted(entries, key=lambda item: item.relative_path):
        _validate_hash_manifest_entry(entry)
        if entry.relative_path in seen_paths:
            raise CarverBlocked("S09 MES input-lock SHA256 manifest paths must be unique")
        seen_paths.add(entry.relative_path)
        digest = hashlib.sha256(entry.artifact_text.encode("utf-8")).hexdigest().upper()
        lines.append(f"{digest}  {entry.relative_path}")
    return "\n".join(lines) + "\n"


def build_s09_mes_runtime_risk_cost_input_lock_artifact_bundle(
    request: S09MESRuntimeRiskCostInputLockArtifactBundleRequest,
) -> dict[str, str]:
    artifact_text_by_path = {
        f"{OUTPUT_ROOT_RELATIVE}/input_manifest/{RUN_ID}_input_manifest.csv": request.input_manifest_csv,
        f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv": request.annual_risk_csv,
        f"{OUTPUT_ROOT_RELATIVE}/risk/20260603_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv": request.daily_price_risk_csv,
        f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_COST_VALUE_ledger.csv": request.cost_value_csv,
        f"{OUTPUT_ROOT_RELATIVE}/cost/20260603_S09_MES_RISK_ADJUSTED_COST_ledger.csv": request.risk_adjusted_cost_csv,
        f"{OUTPUT_ROOT_RELATIVE}/speed/20260603_S09_MES_SPEED_ELIGIBILITY_ledger.csv": request.speed_eligibility_csv,
        f"{OUTPUT_ROOT_RELATIVE}/status/{RUN_ID}_status.json": request.status_json,
        f"{OUTPUT_ROOT_RELATIVE}/provenance/{RUN_ID}_provenance.md": request.provenance_md,
    }
    for relative_path, text in artifact_text_by_path.items():
        _require_relative_local_machinery_path(relative_path)
        _require_non_empty(f"S09 MES input-lock artifact text for {relative_path}", text)
        if "2022-01-03" in text or "2023-12-29" in text:
            raise CarverBlocked("S09 MES input-lock artifact bundle must not contain stale 2022-2023 window text")
    if STRATEGY_INPUT_NOT_READY_STATUS not in request.status_json and INPUT_LOCK_FAIL_CLOSED_STATUS not in request.status_json:
        raise CarverBlocked("S09 MES input-lock artifact bundle status JSON must remain fail-closed")
    if "READY" in request.status_json and INPUT_LOCK_FAIL_CLOSED_STATUS not in request.status_json:
        raise CarverBlocked("S09 MES input-lock artifact bundle status JSON must not promote readiness")

    hash_manifest = render_s09_mes_runtime_risk_cost_input_lock_sha256_manifest(
        tuple(
            S09MESRuntimeRiskCostInputLockHashManifestEntry(relative_path=path, artifact_text=text)
            for path, text in artifact_text_by_path.items()
        )
    )
    artifact_text_by_path[f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt"] = hash_manifest
    return artifact_text_by_path


def main() -> None:
    _write_fail_closed_input_lock_artifacts(
        run_s09_mes_runtime_risk_cost_input_lock(
            S09MESRuntimeRiskCostInputLockConfig(
                execution_authorized=True,
                lane_class=LANE_CLASS,
                root=ROOT_SYMBOL,
                row_id=ROW_ID,
                machinery_development_slice_start=MACHINERY_DEVELOPMENT_SLICE_START,
                machinery_development_slice_end=MACHINERY_DEVELOPMENT_SLICE_END,
                runtime_input_lock_scope=RUNTIME_INPUT_LOCK_SCOPE,
                design_ordering=DESIGN_ORDERING,
                databento_api_access_authorized=False,
            )
        )
    )
    print("S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_RESULT_WRITTEN")


def _fail_closed_status_payload() -> S09MESRuntimeRiskCostInputLockStatus:
    return S09MESRuntimeRiskCostInputLockStatus(
        status=INPUT_LOCK_FAIL_CLOSED_STATUS,
        gate=GATE,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        machinery_development_slice=MACHINERY_DEVELOPMENT_SLICE_TEXT,
        runtime_input_lock_scope=RUNTIME_INPUT_LOCK_SCOPE,
        design_ordering=DESIGN_ORDERING,
        databento_api_access="NO",
        new_provider_data_download="NO",
        market_row_parsing="NO",
        forecast_computation="NO",
        diagnostics_run="NO",
        backtests_run="NO",
        test_validation_lockbox_forward_access="NO",
        strategy_input_readiness_status=STRATEGY_INPUT_NOT_READY_STATUS,
    )


def _header_csv(columns: tuple[str, ...]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(columns)
    return buffer.getvalue()


def _write_fail_closed_input_lock_artifacts(bundle: dict[str, str]) -> tuple[Path, ...]:
    written_paths = tuple(_write_text(ROOT / relative_path, text) for relative_path, text in bundle.items() if "/hashes/" not in relative_path)
    status_path = ROOT / f"{OUTPUT_ROOT_RELATIVE}/status/{RUN_ID}_status.json"
    provenance_path = ROOT / f"{OUTPUT_ROOT_RELATIVE}/provenance/{RUN_ID}_provenance.md"
    result_path = _write_text(RESULT_PATH, _render_result_text(status_path, provenance_path, written_paths))
    audit_path = _write_text(AUDIT_PATH, _render_audit_text(status_path, provenance_path, written_paths, result_path))
    paths_without_hashes = (*written_paths, result_path, audit_path)
    hashes_path = _write_text(
        ROOT / f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt",
        _render_written_sha256_manifest(paths_without_hashes),
    )
    return (*paths_without_hashes, hashes_path)


def _write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _render_result_text(status_path: Path, provenance_path: Path, artifact_paths: tuple[Path, ...]) -> str:
    explicitly_listed = {status_path, provenance_path}
    relative_artifacts = "\n".join(
        f"- `{path.relative_to(ROOT).as_posix()}`" for path in artifact_paths if path not in explicitly_listed
    )
    return f"""# S09 MES Runtime Risk Cost Input Lock Result

Date: 2026-06-03

Status:

```text
{INPUT_LOCK_FAIL_CLOSED_STATUS}
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

Operator authorization received for the bounded runtime risk/cost input-lock
artifact write. This execution did not include Databento API access, provider
login, OHLCV request, new data download, market-row parsing, CFD adapter work,
or old QuantLab active-pipeline use.

Outcome:

The input-lock gate executed and failed closed because executable
source-native annual-risk runtime values, daily price-risk values, historical
MES cost values, risk-adjusted cost values, and speed eligibility values are
not locked as strategy-input values. Ledger families were emitted as
header-only fail-closed ledgers so downstream steps cannot mistake this packet
for ready strategy input.

3:3:4 TEST/VALIDATION/LOCKBOX windows are separately locked and separately gated.

Written artifacts:

- `{status_path.relative_to(ROOT).as_posix()}`
- `{provenance_path.relative_to(ROOT).as_posix()}`
{relative_artifacts}

Boundary preserved:

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations were performed.
"""


def _render_audit_text(
    status_path: Path,
    provenance_path: Path,
    artifact_paths: tuple[Path, ...],
    result_path: Path,
) -> str:
    explicitly_listed = {status_path, provenance_path, result_path}
    relative_artifacts = "\n".join(
        f"- `{path.relative_to(ROOT).as_posix()}`" for path in artifact_paths if path not in explicitly_listed
    )
    hashes_path = ROOT / f"{OUTPUT_ROOT_RELATIVE}/hashes/{RUN_ID}_sha256.txt"
    return f"""# S09 MES Runtime Risk Cost Input Lock Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_FAIL_CLOSED_NO_BACKTEST
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

- `{result_path.relative_to(ROOT).as_posix()}`
- `{status_path.relative_to(ROOT).as_posix()}`
- `{provenance_path.relative_to(ROOT).as_posix()}`
- `{hashes_path.relative_to(ROOT).as_posix()}`
{relative_artifacts}

Hostile checks:

- no Databento API access
- no provider download
- no market-row parsing
- header-only fail-closed ledgers
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


def _render_written_sha256_manifest(paths: tuple[Path, ...]) -> str:
    seen: set[str] = set()
    lines: list[str] = []
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative_path = path.relative_to(ROOT).as_posix()
        if relative_path in seen:
            raise CarverBlocked("S09 MES input-lock written artifact manifest paths must be unique")
        seen.add(relative_path)
        if "2022-01-03_2023-12-29" in relative_path:
            raise CarverBlocked("S09 MES input-lock written artifact manifest must not use the retired 2022-2023 window")
        if "/hashes/" in relative_path:
            raise CarverBlocked("S09 MES input-lock written artifact manifest must not hash itself")
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        lines.append(f"{digest}  {relative_path}")
    return "\n".join(lines) + "\n"


def _validate_input_manifest_row(row: S09MESRuntimeRiskCostInputLockInputManifestRow) -> None:
    _require_non_empty("S09 MES runtime risk/cost input name", row.input_name)
    _require_non_empty("S09 MES runtime risk/cost input required status", row.required_status)
    _require_non_empty("S09 MES runtime risk/cost input relative path", row.relative_path)
    _require_relative_local_machinery_path(row.relative_path)
    _require_sha256("S09 MES runtime risk/cost input SHA256", row.sha256)
    if row.status != INPUT_MANIFEST_LOCKED_STATUS:
        raise CarverBlocked("S09 MES runtime risk/cost input manifest row status is not locked")


def _validate_annual_risk_row(row: S09MESRuntimeRiskCostInputLockAnnualRiskLedgerRow) -> None:
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES annual risk runtime ledger completed trading date must be exact")
    _require_finite_positive("S09 MES long-run annual risk", row.long_run_annual_risk)
    _require_finite_positive("S09 MES EWMA32 current annual risk", row.current_ewma32_annual_risk)
    _require_finite_positive("S09 MES annual percentage risk", row.annual_percentage_risk)
    expected = (
        ANNUAL_RISK_LONG_RUN_WEIGHT * float(row.long_run_annual_risk)
        + ANNUAL_RISK_CURRENT_WEIGHT * float(row.current_ewma32_annual_risk)
    )
    if abs(float(row.annual_percentage_risk) - expected) > 1e-12:
        raise CarverBlocked("S09 MES annual risk runtime ledger does not match locked 30/70 blend")
    _require_sha256("S09 MES annual risk runtime source SHA256", row.source_sha256)
    if row.status != ANNUAL_RISK_LOCKED_STATUS:
        raise CarverBlocked("S09 MES annual risk runtime ledger row status is not locked")


def _validate_daily_price_risk_row(row: S09MESRuntimeRiskCostInputLockDailyPriceRiskLedgerRow) -> None:
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES daily price-risk runtime ledger completed trading date must be exact")
    _require_finite_positive("S09 MES current price", row.current_price)
    _require_finite_positive("S09 MES annual percentage risk", row.annual_percentage_risk)
    _require_finite_positive("S09 MES daily price risk", row.daily_price_risk_currency)
    expected = float(row.current_price) * float(row.annual_percentage_risk) / 16
    if abs(float(row.daily_price_risk_currency) - expected) > 1e-12:
        raise CarverBlocked("S09 MES daily price-risk runtime ledger does not match locked price-risk formula")
    _require_sha256("S09 MES daily price-risk runtime source SHA256", row.source_sha256)
    if row.status != DAILY_PRICE_RISK_LOCKED_STATUS:
        raise CarverBlocked("S09 MES daily price-risk runtime ledger row status is not locked")


def _validate_cost_value_row(row: S09MESRuntimeRiskCostInputLockCostValueLedgerRow) -> None:
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES cost value ledger completed trading date must be exact")
    if row.component_name not in REQUIRED_COST_COMPONENTS:
        raise CarverBlocked("S09 MES cost value ledger component name is not in the required set")
    _require_finite_non_negative(f"S09 MES {row.component_name} cost value", row.amount_currency)
    if row.currency != "USD":
        raise CarverBlocked("S09 MES cost value ledger currency must be USD")
    if row.charge_timing not in COST_CHARGE_TIMINGS:
        raise CarverBlocked("S09 MES cost value ledger charge timing must be PER_SIDE or ROUND_TURN")
    if type(row.effective_start) is not date or type(row.effective_end) is not date:
        raise CarverBlocked("S09 MES cost value ledger effective dates must be exact")
    if row.effective_start > row.completed_trading_date or row.effective_end < row.completed_trading_date:
        raise CarverBlocked("S09 MES cost value ledger effective range must cover completed trading date")
    _require_non_empty("S09 MES cost value ledger source label", row.source_label)
    _require_sha256("S09 MES cost value ledger source SHA256", row.source_sha256)
    if row.status != COST_VALUE_LOCKED_STATUS:
        raise CarverBlocked("S09 MES cost value ledger row status is not locked")


def _validate_risk_adjusted_cost_row(row: S09MESRuntimeRiskCostInputLockRiskAdjustedCostLedgerRow) -> None:
    if type(row.completed_trading_date) is not date:
        raise CarverBlocked("S09 MES risk-adjusted cost ledger completed trading date must be exact")
    _require_finite_positive("S09 MES total cost per trade", row.total_cost_per_trade_currency)
    _require_finite_positive("S09 MES daily price risk", row.daily_price_risk_currency)
    _require_finite_positive("S09 MES risk-adjusted cost per trade", row.risk_adjusted_cost_per_trade_sr)
    expected = float(row.total_cost_per_trade_currency) / (
        float(row.daily_price_risk_currency)
        * DAILY_TO_ANNUAL_RISK_SCALAR
        * MES_CONTRACT_MULTIPLIER_USD_PER_POINT
    )
    if abs(float(row.risk_adjusted_cost_per_trade_sr) - expected) > 1e-12:
        raise CarverBlocked("S09 MES risk-adjusted cost ledger does not match locked total-cost-over-annualized-USD-risk formula")
    if row.status != RISK_ADJUSTED_COST_LOCKED_STATUS:
        raise CarverBlocked("S09 MES risk-adjusted cost ledger row status is not locked")


def _validate_speed_eligibility_row(row: S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow) -> None:
    if isinstance(row.span, bool) or row.span not in EWMAC_TURNOVER_BY_SPAN:
        raise CarverBlocked("S09 MES speed eligibility ledger span is not in the locked EWMAC set")
    _require_finite_positive("S09 MES EWMAC turnover", row.turnover)
    if row.turnover != EWMAC_TURNOVER_BY_SPAN[row.span]:
        raise CarverBlocked("S09 MES speed eligibility ledger turnover does not match the locked table")
    _require_finite_positive("S09 MES risk-adjusted cost per trade", row.risk_adjusted_cost_per_trade_sr)
    _require_finite_positive("S09 MES speed eligibility threshold", row.threshold_sr)
    if row.threshold_sr != SPEED_ELIGIBILITY_THRESHOLD_SR:
        raise CarverBlocked("S09 MES speed eligibility threshold must be locked to 0.15 SR")
    if type(row.eligible) is not bool:
        raise CarverBlocked("S09 MES speed eligibility flag must be boolean")
    expected = row.turnover * row.risk_adjusted_cost_per_trade_sr <= row.threshold_sr
    if row.eligible is not expected:
        raise CarverBlocked("S09 MES speed eligibility flag does not match locked cost screen")
    if row.status != SPEED_ELIGIBILITY_LOCKED_STATUS:
        raise CarverBlocked("S09 MES speed eligibility ledger row status is not locked")


def _validate_status_payload(payload: S09MESRuntimeRiskCostInputLockStatus) -> None:
    if payload.status != INPUT_LOCK_FAIL_CLOSED_STATUS:
        raise CarverBlocked("S09 MES input-lock status must remain fail-closed")
    if payload.gate != GATE:
        raise CarverBlocked("S09 MES input-lock status gate is not locked")
    if payload.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES input-lock status must remain source-native futures")
    if payload.root != ROOT_SYMBOL or payload.row_id != ROW_ID:
        raise CarverBlocked("S09 MES input-lock status is locked to Appendix C MES row")
    if payload.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES input-lock status must use the oldest machinery-development slice")
    if payload.runtime_input_lock_scope != RUNTIME_INPUT_LOCK_SCOPE:
        raise CarverBlocked("S09 MES input-lock status scope is not locked")
    if payload.design_ordering != DESIGN_ORDERING:
        raise CarverBlocked("S09 MES input-lock status must preserve oldest-data ordering")
    for name, value in (
        ("Databento API access", payload.databento_api_access),
        ("new provider data download", payload.new_provider_data_download),
        ("market-row parsing", payload.market_row_parsing),
        ("forecast computation", payload.forecast_computation),
        ("diagnostics", payload.diagnostics_run),
        ("backtests", payload.backtests_run),
        ("TEST/VALIDATION/Lockbox/Forward access", payload.test_validation_lockbox_forward_access),
    ):
        if value != "NO":
            raise CarverBlocked(f"S09 MES input-lock status must record no {name}")
    if payload.strategy_input_readiness_status != STRATEGY_INPUT_NOT_READY_STATUS:
        raise CarverBlocked("S09 MES input-lock status must not promote strategy input readiness")


def _validate_hash_manifest_entry(entry: S09MESRuntimeRiskCostInputLockHashManifestEntry) -> None:
    _require_non_empty("S09 MES input-lock hash manifest relative path", entry.relative_path)
    _require_relative_local_machinery_path(entry.relative_path)
    _require_non_empty("S09 MES input-lock hash manifest artifact text", entry.artifact_text)


def _require_relative_local_machinery_path(value: str) -> None:
    normalized = value.replace("\\", "/")
    path = Path(normalized)
    lowered = normalized.lower()
    if path.is_absolute() or ":" in normalized:
        raise CarverBlocked("S09 MES runtime risk/cost input path must be repo-relative")
    if any(part in {"", ".", ".."} for part in normalized.split("/")):
        raise CarverBlocked("S09 MES runtime risk/cost input path must not traverse directories")
    if "2022-01-03_2023-12-29" in normalized:
        raise CarverBlocked("S09 MES runtime risk/cost input path must not use the retired 2022-2023 window")
    if any(token in lowered for token in ("/test/", "validation", "lockbox", "forward", "oos")):
        raise CarverBlocked("S09 MES runtime risk/cost input path must not access scored or locked-out windows")
    if MACHINERY_SLICE_PATH_TOKEN not in normalized:
        raise CarverBlocked("S09 MES runtime risk/cost input path must stay inside the machinery-development slice")
    if not normalized.startswith("docs/researchops/s09/"):
        raise CarverBlocked("S09 MES runtime risk/cost input path must stay inside S09 researchops")


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


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be finite and non-negative")


if __name__ == "__main__":
    main()

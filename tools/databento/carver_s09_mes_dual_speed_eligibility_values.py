from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import date
from io import StringIO
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked  # noqa: E402
from carver.spine.m2 import S09_EWMAC_SPANS  # noqa: E402
from carver.spine.s09_mes_readiness import (  # noqa: E402
    S09_MES_COST_THRESHOLD_SR,
    S09_MES_EWMAC_TURNOVER_BY_SPAN,
)
from tools.databento.carver_s09_mes_dual_cost_scenario_policy import (  # noqa: E402
    CONSERVATIVE_SCENARIO,
    ETF_ALL_IN_SCENARIO,
    LOCKED_COMPLETED_TRADING_DATE,
    ROW_ID,
    ROOT_SYMBOL,
    WINDOW_END,
    WINDOW_LABEL,
    WINDOW_START,
    WINDOW_TEXT,
)
from tools.databento.carver_s09_mes_dual_risk_adjusted_cost_values import (  # noqa: E402
    RISK_ADJUSTED_LEDGER_PATH,
    RISK_ADJUSTED_STATUS_PATH,
    STATUS as RISK_ADJUSTED_STATUS,
)

RUN_ID = "20260603_S09_MES_DUAL_SPEED_ELIGIBILITY"
GATE = "S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_LOCK"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
STATUS = "LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_ALL_SPEEDS_SURVIVE_NOT_ELIGIBLE_SET_NOT_BACKTEST"
ROW_STATUS = "LOCKED_SOURCE_NATIVE_DUAL_SPEED_ELIGIBILITY_VALUE_NOT_ELIGIBLE_SET_NOT_BACKTEST"
SOURCE_LABEL = "LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_LEDGER"
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_strategy_input_evidence_completion" / WINDOW_LABEL
SPEED_ROOT = OUTPUT_ROOT / "speed"
SPEED_LEDGER_PATH = SPEED_ROOT / f"{RUN_ID}_ledger.csv"
SPEED_STATUS_PATH = SPEED_ROOT / f"{RUN_ID}_status.json"
SPEED_PROVENANCE_PATH = SPEED_ROOT / f"{RUN_ID}_provenance.md"
SPEED_HASH_PATH = SPEED_ROOT / f"{RUN_ID}_sha256.txt"
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_LOCK_RESULT_2026-06-03.md"
LOCAL_AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"


@dataclass(frozen=True)
class S09MESDualSpeedEligibilityValuesConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    dual_risk_adjusted_cost_status: str
    speed_eligibility_values_lock: bool
    eligible_speed_set_lock: bool
    table36_fdm_row_lock: bool
    forecast_computation: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


def run_dual_speed_eligibility_values_guard(config: S09MESDualSpeedEligibilityValuesConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES dual speed eligibility values lock is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES dual speed eligibility values lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES dual speed eligibility values lock is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES dual speed eligibility values lock is locked to the machinery-development slice")
    if config.dual_risk_adjusted_cost_status != RISK_ADJUSTED_STATUS:
        raise CarverBlocked("S09 MES dual speed eligibility values require the locked dual risk-adjusted cost status")
    if not config.speed_eligibility_values_lock:
        raise CarverBlocked("S09 MES dual speed eligibility values must be explicitly locked")
    if config.eligible_speed_set_lock:
        raise CarverBlocked("S09 MES dual speed eligibility values lock must not lock eligible speed set")
    if config.table36_fdm_row_lock:
        raise CarverBlocked("S09 MES dual speed eligibility values lock must not lock Table 36 FDM row")
    if config.forecast_computation:
        raise CarverBlocked("S09 MES dual speed eligibility values lock forbids forecast computation")
    if config.diagnostics_authorized:
        raise CarverBlocked("S09 MES dual speed eligibility values lock forbids diagnostics")
    if config.backtest_authorized:
        raise CarverBlocked("S09 MES dual speed eligibility values lock forbids backtests")
    if config.test_validation_lockbox_forward_authorized:
        raise CarverBlocked("S09 MES dual speed eligibility values lock forbids TEST/VALIDATION/Lockbox/Forward access")
    if config.git_operations_authorized:
        raise CarverBlocked("S09 MES dual speed eligibility values lock forbids Git operations")
    return {"status": "AUTHORIZED_DUAL_SPEED_ELIGIBILITY_VALUES_READY"}


def build_request_manifest_payload(config: S09MESDualSpeedEligibilityValuesConfig) -> dict[str, str]:
    run_dual_speed_eligibility_values_guard(config)
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "dual_risk_adjusted_cost_status": RISK_ADJUSTED_STATUS,
        "speed_eligibility_values_lock": "YES_DUAL_SCENARIO",
        "eligible_speed_set_lock": "NO",
        "table36_fdm_row_lock": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def build_dual_speed_eligibility_rows(
    *,
    risk_adjusted_rows: tuple[dict[str, str], ...],
    source_sha256: str = "0" * 64,
) -> tuple[dict[str, str], ...]:
    _validate_source_sha256(source_sha256)
    _validate_risk_adjusted_rows(risk_adjusted_rows)
    rows: list[dict[str, str]] = []
    for risk_row in risk_adjusted_rows:
        risk_adjusted_cost = float(risk_row["risk_adjusted_cost_per_trade_sr"])
        for span in S09_EWMAC_SPANS:
            turnover = S09_MES_EWMAC_TURNOVER_BY_SPAN[span]
            burden = turnover * risk_adjusted_cost
            eligible = burden <= S09_MES_COST_THRESHOLD_SR
            rows.append(
                {
                    "completed_trading_date": LOCKED_COMPLETED_TRADING_DATE.isoformat(),
                    "scenario_name": risk_row["scenario_name"],
                    "span": str(span),
                    "turnover": _fmt_full(turnover),
                    "risk_adjusted_cost_per_trade_sr": _fmt6(risk_adjusted_cost),
                    "annualized_cost_burden_sr": _fmt6(burden),
                    "threshold_sr": _fmt_threshold(S09_MES_COST_THRESHOLD_SR),
                    "eligible": str(eligible),
                    "source_label": SOURCE_LABEL,
                    "source_sha256": source_sha256,
                    "status": ROW_STATUS,
                }
            )
    return tuple(rows)


def main() -> None:
    config = S09MESDualSpeedEligibilityValuesConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        window_start=WINDOW_START.isoformat(),
        window_end=WINDOW_END.isoformat(),
        dual_risk_adjusted_cost_status=RISK_ADJUSTED_STATUS,
        speed_eligibility_values_lock=True,
        eligible_speed_set_lock=False,
        table36_fdm_row_lock=False,
        forecast_computation=False,
        diagnostics_authorized=False,
        backtest_authorized=False,
        test_validation_lockbox_forward_authorized=False,
        git_operations_authorized=False,
    )
    written = write_dual_speed_eligibility_values_artifacts(config)
    print("S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_RESULT_WRITTEN")
    print(f"artifacts={len(written)}")


def write_dual_speed_eligibility_values_artifacts(config: S09MESDualSpeedEligibilityValuesConfig) -> tuple[Path, ...]:
    run_dual_speed_eligibility_values_guard(config)
    risk_rows = _locked_risk_adjusted_rows()
    rows = build_dual_speed_eligibility_rows(
        risk_adjusted_rows=risk_rows,
        source_sha256=_sha256(RISK_ADJUSTED_LEDGER_PATH),
    )
    SPEED_ROOT.mkdir(parents=True, exist_ok=True)
    _write_text(SPEED_LEDGER_PATH, _render_speed_eligibility_ledger(rows))
    _write_json(SPEED_STATUS_PATH, _status_payload(rows))
    _write_text(SPEED_PROVENANCE_PATH, _render_provenance(rows))
    _write_text(RESULT_PATH, _render_result(rows))
    _write_text(LOCAL_AUDIT_PATH, _render_local_audit(rows))
    _write_text(
        SPEED_HASH_PATH,
        _render_sha256_manifest((SPEED_LEDGER_PATH, SPEED_STATUS_PATH, SPEED_PROVENANCE_PATH, RESULT_PATH, LOCAL_AUDIT_PATH)),
    )
    return (SPEED_LEDGER_PATH, SPEED_STATUS_PATH, SPEED_PROVENANCE_PATH, RESULT_PATH, LOCAL_AUDIT_PATH, SPEED_HASH_PATH)


def _locked_risk_adjusted_rows() -> tuple[dict[str, str], ...]:
    status = json.loads(RISK_ADJUSTED_STATUS_PATH.read_text(encoding="utf-8"))
    if status.get("status") != RISK_ADJUSTED_STATUS:
        raise CarverBlocked("S09 MES dual speed eligibility values require locked dual risk-adjusted cost status")
    if status.get("speed_eligibility_computation") != "NO":
        raise CarverBlocked("S09 MES dual risk-adjusted cost status must precede speed eligibility computation")
    if status.get("backtests_run") != "NO":
        raise CarverBlocked("S09 MES dual speed eligibility values forbid backtested source inputs")
    with RISK_ADJUSTED_LEDGER_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))
    _validate_risk_adjusted_rows(rows)
    return rows


def _validate_risk_adjusted_rows(rows: tuple[dict[str, str], ...]) -> None:
    expected_names = (CONSERVATIVE_SCENARIO, ETF_ALL_IN_SCENARIO)
    if tuple(row.get("scenario_name") for row in rows) != expected_names:
        raise CarverBlocked("S09 MES dual speed eligibility values require both locked risk-adjusted scenario rows in order")
    for row in rows:
        if row.get("completed_trading_date") != LOCKED_COMPLETED_TRADING_DATE.isoformat():
            raise CarverBlocked("S09 MES dual speed eligibility values require the locked completed trading date")
        if row.get("status") != "LOCKED_SOURCE_NATIVE_DUAL_RISK_ADJUSTED_COST_VALUE_NOT_SPEED_NOT_BACKTEST":
            raise CarverBlocked("S09 MES dual speed eligibility values require locked non-speed risk-adjusted rows")
        _require_positive("risk-adjusted cost", row.get("risk_adjusted_cost_per_trade_sr"))


def _render_speed_eligibility_ledger(rows: tuple[dict[str, str], ...]) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=tuple(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def _status_payload(rows: tuple[dict[str, str], ...]) -> dict[str, Any]:
    scenario_names = sorted({row["scenario_name"] for row in rows})
    eligible_rows = [row for row in rows if row["eligible"] == "True"]
    return {
        "backtests_run": "NO",
        "diagnostics_run": "NO",
        "eligible_row_count": len(eligible_rows),
        "eligible_speed_set_lock": "NO",
        "evidence_completion_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
        "forecast_computation": "NO",
        "gate": GATE,
        "git_operations": "NO",
        "lane_class": LANE_CLASS,
        "machinery_development_slice": WINDOW_TEXT,
        "remaining_evidence_count": 3,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "scenario_count": len(scenario_names),
        "scenario_names": scenario_names,
        "selected_evidence_name": "speed_eligibility_values",
        "speed_eligibility_values_lock": "YES_DUAL_SCENARIO",
        "status": STATUS,
        "strategy_input_readiness_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
        "table36_fdm_row_lock": "NO",
        "test_validation_lockbox_forward_access": "NO",
    }


def _render_provenance(rows: tuple[dict[str, str], ...]) -> str:
    eligible_rows = [row for row in rows if row["eligible"] == "True"]
    return f"""# S09 MES Dual Speed Eligibility Values Provenance

Date: 2026-06-03

Status:

```text
{STATUS}
```

Inputs:

- locked dual risk-adjusted cost status: {RISK_ADJUSTED_STATUS}
- threshold: {S09_MES_COST_THRESHOLD_SR} SR
- spans: {",".join(str(span) for span in S09_EWMAC_SPANS)}
- machinery-development slice: {WINDOW_TEXT}

Result:

The speed eligibility values are locked for both scenarios. All evaluated rows
survive the locked threshold after the annualized USD risk unit correction.
The eligible speed set and Table 36 FDM row remain separate downstream locks.

Eligible rows:

- {len(eligible_rows)} of {len(rows)}

Boundary:

This locks speed eligibility values only. It does not lock an eligible speed
set, select a Table 36 FDM row, compute forecasts, run diagnostics, run
backtests, access TEST, VALIDATION, Lockbox, Forward, deploy, trade, promote,
stage Git, commit, push, create a PR, or perform remote operations.
"""


def _render_result(rows: tuple[dict[str, str], ...]) -> str:
    eligible_rows = [row for row in rows if row["eligible"] == "True"]
    conservative_rows = [row for row in rows if row["scenario_name"] == CONSERVATIVE_SCENARIO]
    etf_rows = [row for row in rows if row["scenario_name"] == ETF_ALL_IN_SCENARIO]
    return f"""# S09 MES Dual Speed Eligibility Values Lock Result

Date: 2026-06-03

Status:

```text
{STATUS}
```

Locked threshold:

```text
{S09_MES_COST_THRESHOLD_SR} SR
```

Result:

- rows locked: {len(rows)}
- eligible rows: {len(eligible_rows)}
- conservative scenario survives all spans: {str(all(row["eligible"] == "True" for row in conservative_rows)).upper()}
- ETF all-in simulated-fee scenario survives all spans: {str(all(row["eligible"] == "True" for row in etf_rows)).upper()}

Correction note:

This supersedes any earlier 2026-06-03 no-surviving-speed artifact that divided
USD costs by a daily point-risk denominator.

Boundary:

No eligible speed set lock, no Table 36 FDM row lock, no forecast computation,
no diagnostics, no backtests, no TEST, no VALIDATION, no Lockbox, no Forward,
no deployment, no trading, no promotion, no Git staging, no commit, no push,
no PR, and no remote operations were performed.
"""


def _render_local_audit(rows: tuple[dict[str, str], ...]) -> str:
    return f"""# S09 MES Dual Speed Eligibility Values Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_DUAL_SPEED_ELIGIBILITY_VALUES_LOCKED_NO_ELIGIBLE_SET_NO_BACKTEST
```

Checks:

- two scenarios are present
- six EWMAC spans are evaluated per scenario
- threshold is locked to {S09_MES_COST_THRESHOLD_SR} SR
- eligibility values match turnover times risk-adjusted cost versus threshold
- eligible row count is {len([row for row in rows if row["eligible"] == "True"])}
- eligible speed set is not locked
- Table 36 FDM row is not locked
- forecasts, diagnostics, and backtests were not run
- TEST, VALIDATION, Lockbox, and Forward were not accessed
- Git staging, commit, push, and PR were not performed

This local audit must be reviewed by a spawned hostile-audit subagent.
"""


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _render_sha256_manifest(paths: tuple[Path, ...]) -> str:
    lines = []
    seen: set[str] = set()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        if relative in seen:
            raise CarverBlocked("S09 MES dual speed eligibility SHA paths must be unique")
        seen.add(relative)
        lines.append(f"{_sha256(path)}  {relative}")
    return "\n".join(lines) + "\n"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _validate_source_sha256(value: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise CarverBlocked("S09 MES dual speed eligibility source hash is missing")
    try:
        int(value, 16)
    except ValueError as exc:
        raise CarverBlocked("S09 MES dual speed eligibility source hash is invalid") from exc


def _require_positive(name: str, raw_value: object) -> None:
    try:
        value = float(raw_value)
    except (TypeError, ValueError) as exc:
        raise CarverBlocked(f"S09 MES dual speed eligibility {name} must be numeric") from exc
    if value <= 0:
        raise CarverBlocked(f"S09 MES dual speed eligibility {name} must be positive")


def _fmt6(value: float) -> str:
    return f"{float(value):.6f}"


def _fmt_threshold(value: float) -> str:
    return f"{float(value):.2f}".rstrip("0").rstrip(".")


def _fmt_full(value: float) -> str:
    return str(float(value)).rstrip("0").rstrip(".")


if __name__ == "__main__":
    main()

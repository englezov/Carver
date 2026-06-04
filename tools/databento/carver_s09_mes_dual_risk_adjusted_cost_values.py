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

from carver.spine.m0 import CarverBlocked, LaneClass, SourceRuleStatus  # noqa: E402
from carver.spine.s09_mes_readiness import (  # noqa: E402
    S09MESRiskAdjustedCostRequest,
    s09_mes_risk_adjusted_cost_from_locked_inputs,
)
from tools.databento.carver_s09_mes_dual_cost_scenario_policy import (  # noqa: E402
    CONSERVATIVE_SCENARIO,
    ETF_ALL_IN_SCENARIO,
    LOCKED_COMPLETED_TRADING_DATE,
    ROW_ID,
    ROOT_SYMBOL,
    SCENARIO_LEDGER_PATH,
    SCENARIO_STATUS_PATH,
    STATUS as POLICY_STATUS,
    WINDOW_END,
    WINDOW_LABEL,
    WINDOW_START,
    WINDOW_TEXT,
)

RUN_ID = "20260603_S09_MES_DUAL_RISK_ADJUSTED_COST"
GATE = "S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_LOCK"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
STATUS = "LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_NOT_SPEED_NOT_BACKTEST"
ROW_STATUS = "LOCKED_SOURCE_NATIVE_DUAL_RISK_ADJUSTED_COST_VALUE_NOT_SPEED_NOT_BACKTEST"
SOURCE_LABEL = "LOCKED_S09_MES_DUAL_COST_SCENARIO_POLICY_LEDGER"
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_strategy_input_evidence_completion" / WINDOW_LABEL
COST_ROOT = OUTPUT_ROOT / "cost"
RISK_ADJUSTED_LEDGER_PATH = COST_ROOT / f"{RUN_ID}_ledger.csv"
RISK_ADJUSTED_STATUS_PATH = COST_ROOT / f"{RUN_ID}_status.json"
RISK_ADJUSTED_PROVENANCE_PATH = COST_ROOT / f"{RUN_ID}_provenance.md"
RISK_ADJUSTED_HASH_PATH = COST_ROOT / f"{RUN_ID}_sha256.txt"
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_LOCK_RESULT_2026-06-03.md"
LOCAL_AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"


@dataclass(frozen=True)
class S09MESDualRiskAdjustedCostValuesConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    dual_cost_scenario_policy_status: str
    risk_adjusted_cost_values_lock: bool
    speed_eligibility_computation: bool
    forecast_computation: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


def run_dual_risk_adjusted_cost_values_guard(config: S09MESDualRiskAdjustedCostValuesConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock is locked to the machinery-development slice")
    if config.dual_cost_scenario_policy_status != POLICY_STATUS:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values require the locked dual cost scenario policy")
    if not config.risk_adjusted_cost_values_lock:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values must be explicitly locked")
    if config.speed_eligibility_computation:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock forbids speed eligibility computation")
    if config.forecast_computation:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock forbids forecast computation")
    if config.diagnostics_authorized:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock forbids diagnostics")
    if config.backtest_authorized:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock forbids backtests")
    if config.test_validation_lockbox_forward_authorized:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock forbids TEST/VALIDATION/Lockbox/Forward access")
    if config.git_operations_authorized:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values lock forbids Git operations")
    return {"status": "AUTHORIZED_DUAL_RISK_ADJUSTED_COST_VALUES_READY"}


def build_request_manifest_payload(config: S09MESDualRiskAdjustedCostValuesConfig) -> dict[str, str]:
    run_dual_risk_adjusted_cost_values_guard(config)
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "dual_cost_scenario_policy_status": POLICY_STATUS,
        "risk_adjusted_cost_values_lock": "YES_DUAL_SCENARIO",
        "speed_eligibility_computation": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def build_dual_risk_adjusted_cost_rows(
    *,
    policy_rows: tuple[dict[str, str], ...],
    source_sha256: str = "0" * 64,
) -> tuple[dict[str, str], ...]:
    _validate_source_sha256(source_sha256)
    _validate_policy_rows(policy_rows)
    rows: list[dict[str, str]] = []
    for policy_row in policy_rows:
        result = s09_mes_risk_adjusted_cost_from_locked_inputs(
            S09MESRiskAdjustedCostRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                total_cost_per_trade_currency=float(policy_row["total_round_turn_cost_per_trade_currency"]),
                total_cost_status=SourceRuleStatus.LOCKED,
                daily_price_risk_currency=float(policy_row["daily_price_risk_currency"]),
                daily_price_risk_status=SourceRuleStatus.LOCKED,
            )
        )
        rows.append(
            {
                "completed_trading_date": LOCKED_COMPLETED_TRADING_DATE.isoformat(),
                "scenario_name": policy_row["scenario_name"],
                "total_cost_per_trade_currency": _fmt2(result.total_cost_per_trade_currency),
                "daily_price_risk_currency": _fmt_full(result.daily_price_risk_currency),
                "annualized_price_risk_currency": _fmt_full(result.annualized_price_risk_currency),
                "risk_adjusted_cost_per_trade_sr": _fmt6(result.risk_adjusted_cost_per_trade_sr),
                "cost_basis": result.cost_basis,
                "source_label": SOURCE_LABEL,
                "source_sha256": source_sha256,
                "status": ROW_STATUS,
            }
        )
    return tuple(rows)


def main() -> None:
    config = S09MESDualRiskAdjustedCostValuesConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        window_start=WINDOW_START.isoformat(),
        window_end=WINDOW_END.isoformat(),
        dual_cost_scenario_policy_status=POLICY_STATUS,
        risk_adjusted_cost_values_lock=True,
        speed_eligibility_computation=False,
        forecast_computation=False,
        diagnostics_authorized=False,
        backtest_authorized=False,
        test_validation_lockbox_forward_authorized=False,
        git_operations_authorized=False,
    )
    written = write_dual_risk_adjusted_cost_values_artifacts(config)
    print("S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_RESULT_WRITTEN")
    print(f"artifacts={len(written)}")


def write_dual_risk_adjusted_cost_values_artifacts(config: S09MESDualRiskAdjustedCostValuesConfig) -> tuple[Path, ...]:
    run_dual_risk_adjusted_cost_values_guard(config)
    policy_rows = _locked_policy_rows()
    rows = build_dual_risk_adjusted_cost_rows(
        policy_rows=policy_rows,
        source_sha256=_sha256(SCENARIO_LEDGER_PATH),
    )
    COST_ROOT.mkdir(parents=True, exist_ok=True)
    _write_text(RISK_ADJUSTED_LEDGER_PATH, _render_risk_adjusted_ledger(rows))
    _write_json(RISK_ADJUSTED_STATUS_PATH, _status_payload(rows))
    _write_text(RISK_ADJUSTED_PROVENANCE_PATH, _render_provenance(rows))
    _write_text(RESULT_PATH, _render_result(rows))
    _write_text(LOCAL_AUDIT_PATH, _render_local_audit(rows))
    _write_text(
        RISK_ADJUSTED_HASH_PATH,
        _render_sha256_manifest(
            (
                RISK_ADJUSTED_LEDGER_PATH,
                RISK_ADJUSTED_STATUS_PATH,
                RISK_ADJUSTED_PROVENANCE_PATH,
                RESULT_PATH,
                LOCAL_AUDIT_PATH,
            )
        ),
    )
    return (
        RISK_ADJUSTED_LEDGER_PATH,
        RISK_ADJUSTED_STATUS_PATH,
        RISK_ADJUSTED_PROVENANCE_PATH,
        RESULT_PATH,
        LOCAL_AUDIT_PATH,
        RISK_ADJUSTED_HASH_PATH,
    )


def _locked_policy_rows() -> tuple[dict[str, str], ...]:
    status = json.loads(SCENARIO_STATUS_PATH.read_text(encoding="utf-8"))
    if status.get("status") != POLICY_STATUS:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values require locked dual cost scenario status")
    if status.get("risk_adjusted_cost_values_lock") != "NO":
        raise CarverBlocked("S09 MES dual cost scenario policy must precede formal risk-adjusted cost lock")
    if status.get("backtests_run") != "NO":
        raise CarverBlocked("S09 MES dual risk-adjusted cost values forbid backtested source policy")
    with SCENARIO_LEDGER_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))
    _validate_policy_rows(rows)
    return rows


def _validate_policy_rows(rows: tuple[dict[str, str], ...]) -> None:
    expected_names = (CONSERVATIVE_SCENARIO, ETF_ALL_IN_SCENARIO)
    if tuple(row.get("scenario_name") for row in rows) != expected_names:
        raise CarverBlocked("S09 MES dual risk-adjusted cost values require both locked scenario rows in order")
    daily_risk_values = {row.get("daily_price_risk_currency") for row in rows}
    if len(daily_risk_values) != 1:
        raise CarverBlocked("S09 MES dual risk-adjusted cost scenarios must share one locked daily risk value")
    for row in rows:
        if row.get("status") != "LOCKED_COST_SCENARIO_POLICY_VALUE_NOT_BACKTEST":
            raise CarverBlocked("S09 MES dual risk-adjusted cost requires locked non-backtest scenario rows")
        _require_positive("total scenario cost", row.get("total_round_turn_cost_per_trade_currency"))
        _require_positive("daily price risk", row.get("daily_price_risk_currency"))


def _render_risk_adjusted_ledger(rows: tuple[dict[str, str], ...]) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=tuple(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def _status_payload(rows: tuple[dict[str, str], ...]) -> dict[str, Any]:
    return {
        "backtests_run": "NO",
        "diagnostics_run": "NO",
        "evidence_completion_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
        "forecast_computation": "NO",
        "gate": GATE,
        "git_operations": "NO",
        "lane_class": LANE_CLASS,
        "machinery_development_slice": WINDOW_TEXT,
        "remaining_evidence_count": 4,
        "risk_adjusted_cost_values_lock": "YES_DUAL_SCENARIO",
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "scenario_count": len(rows),
        "scenario_names": [row["scenario_name"] for row in rows],
        "selected_evidence_name": "risk_adjusted_cost_values",
        "speed_eligibility_computation": "NO",
        "status": STATUS,
        "strategy_input_readiness_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
        "test_validation_lockbox_forward_access": "NO",
    }


def _render_provenance(rows: tuple[dict[str, str], ...]) -> str:
    return f"""# S09 MES Dual Risk-Adjusted Cost Values Provenance

Date: 2026-06-03

Status:

```text
{STATUS}
```

Inputs:

- locked dual cost scenario policy: {POLICY_STATUS}
- machinery-development slice: {WINDOW_TEXT}
- completed trading date: {LOCKED_COMPLETED_TRADING_DATE.isoformat()}

Locked values:

- {rows[0]["scenario_name"]}: {rows[0]["risk_adjusted_cost_per_trade_sr"]} SR cost per trade, using {rows[0]["annualized_price_risk_currency"]} annualized USD risk per contract
- {rows[1]["scenario_name"]}: {rows[1]["risk_adjusted_cost_per_trade_sr"]} SR cost per trade, using {rows[1]["annualized_price_risk_currency"]} annualized USD risk per contract

Boundary:

This locks formal dual-scenario risk-adjusted cost values only. It does not
compute speed eligibility, forecasts, diagnostics, backtests, TEST,
VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations.
"""


def _render_result(rows: tuple[dict[str, str], ...]) -> str:
    return f"""# S09 MES Dual Risk-Adjusted Cost Values Lock Result

Date: 2026-06-03

Status:

```text
{STATUS}
```

Formal risk-adjusted cost values:

- {rows[0]["scenario_name"]}: {rows[0]["total_cost_per_trade_currency"]} USD / {rows[0]["annualized_price_risk_currency"]} annualized USD risk per contract = {rows[0]["risk_adjusted_cost_per_trade_sr"]} SR cost per trade.
- {rows[1]["scenario_name"]}: {rows[1]["total_cost_per_trade_currency"]} USD / {rows[1]["annualized_price_risk_currency"]} annualized USD risk per contract = {rows[1]["risk_adjusted_cost_per_trade_sr"]} SR cost per trade.

Unit bridge:

- daily price-risk field remains the locked daily index-point risk
- annualized USD risk per contract = daily point risk * 16 * MES 5 USD/point multiplier
- this supersedes any daily-denominator cost-screen artifact emitted earlier on 2026-06-03

Boundary:

No speed eligibility computation, no forecast computation, no diagnostics, no
backtests, no TEST, no VALIDATION, no Lockbox, no Forward, no deployment, no
trading, no promotion, no Git staging, no commit, no push, no PR, and no
remote operations were performed.
"""


def _render_local_audit(rows: tuple[dict[str, str], ...]) -> str:
    return f"""# S09 MES Dual Risk-Adjusted Cost Values Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_DUAL_RISK_ADJUSTED_COST_VALUES_LOCKED_NO_SPEED_NO_BACKTEST
```

Checks:

- both scenarios are present: {rows[0]["scenario_name"]}; {rows[1]["scenario_name"]}
- conservative risk-adjusted cost is {rows[0]["risk_adjusted_cost_per_trade_sr"]}
- ETF all-in simulated-fee risk-adjusted cost is {rows[1]["risk_adjusted_cost_per_trade_sr"]}
- speed eligibility was not computed
- forecasts were not computed
- diagnostics were not run
- backtests were not run
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
            raise CarverBlocked("S09 MES dual risk-adjusted cost SHA paths must be unique")
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
        raise CarverBlocked("S09 MES dual risk-adjusted cost source hash is missing")
    try:
        int(value, 16)
    except ValueError as exc:
        raise CarverBlocked("S09 MES dual risk-adjusted cost source hash is invalid") from exc


def _require_positive(name: str, raw_value: object) -> None:
    try:
        value = float(raw_value)
    except (TypeError, ValueError) as exc:
        raise CarverBlocked(f"S09 MES dual risk-adjusted cost {name} must be numeric") from exc
    if value <= 0:
        raise CarverBlocked(f"S09 MES dual risk-adjusted cost {name} must be positive")


def _fmt2(value: float) -> str:
    return f"{float(value):.2f}".rstrip("0").rstrip(".")


def _fmt6(value: float) -> str:
    return f"{float(value):.6f}"


def _fmt_full(value: float) -> str:
    return str(float(value)).rstrip("0").rstrip(".")


if __name__ == "__main__":
    main()

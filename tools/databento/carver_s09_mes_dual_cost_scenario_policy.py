from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import date
from io import StringIO
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked  # noqa: E402

RUN_ID = "20260603_S09_MES_COST_SCENARIO_POLICY"
GATE = "S09_MES_DUAL_COST_SCENARIO_POLICY_LOCK"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
WINDOW_START = date(2019, 5, 5)
WINDOW_END = date(2020, 4, 5)
WINDOW_LABEL = "2019-05-05_2020-04-05"
WINDOW_TEXT = "2019-05-05 through 2020-04-05"
LOCKED_COMPLETED_TRADING_DATE = date(2020, 3, 2)
STATUS = "LOCKED_S09_MES_DUAL_COST_SCENARIO_POLICY_NOT_RISK_ADJUSTED_COST"
ROW_STATUS = "LOCKED_COST_SCENARIO_POLICY_VALUE_NOT_BACKTEST"
MES_MULTIPLIER = 5.0
DAILY_TO_ANNUAL_RISK_SCALAR = 16
CONSERVATIVE_SCENARIO = "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH"
ETF_ALL_IN_SCENARIO = "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED"
EXCHANGE_FEE_PER_SIDE = 0.20
NFA_FEE_PER_SIDE = 0.02
ETF_BROKER_COMMISSION_PER_SIDE = 0.62
SPREAD_SLIPPAGE_ROUND_TURN = 1.25
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_strategy_input_evidence_completion" / WINDOW_LABEL
COST_ROOT = OUTPUT_ROOT / "cost"
DAILY_RISK_LEDGER_PATH = OUTPUT_ROOT / "risk" / "20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv"
SCENARIO_LEDGER_PATH = COST_ROOT / f"{RUN_ID}_ledger.csv"
SCENARIO_STATUS_PATH = COST_ROOT / f"{RUN_ID}_status.json"
SCENARIO_PROVENANCE_PATH = COST_ROOT / f"{RUN_ID}_provenance.md"
SCENARIO_HASH_PATH = COST_ROOT / f"{RUN_ID}_sha256.txt"
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_DUAL_COST_SCENARIO_POLICY_LOCK_RESULT_2026-06-03.md"
LOCAL_AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_DUAL_COST_SCENARIO_POLICY_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"


@dataclass(frozen=True)
class S09MESDualCostScenarioPolicyConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    dual_scenario_policy: bool
    conservative_pass_through_scenario: bool
    etf_all_in_sim_fee_scenario: bool
    risk_adjusted_cost_values_lock: bool
    speed_eligibility_computation: bool
    forecast_computation: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


def run_dual_cost_scenario_policy_guard(config: S09MESDualCostScenarioPolicyConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES dual cost scenario policy is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES dual cost scenario policy is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES dual cost scenario policy is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES dual cost scenario policy is locked to the machinery-development slice")
    if not config.dual_scenario_policy:
        raise CarverBlocked("S09 MES dual cost scenario policy must run both scenarios")
    if not config.conservative_pass_through_scenario:
        raise CarverBlocked("S09 MES dual cost scenario policy requires conservative pass-through scenario")
    if not config.etf_all_in_sim_fee_scenario:
        raise CarverBlocked("S09 MES dual cost scenario policy requires ETF all-in simulated-fee scenario")
    if config.risk_adjusted_cost_values_lock:
        raise CarverBlocked("S09 MES dual cost scenario policy must not lock formal risk-adjusted cost values")
    if config.speed_eligibility_computation:
        raise CarverBlocked("S09 MES dual cost scenario policy forbids speed eligibility computation")
    if config.forecast_computation:
        raise CarverBlocked("S09 MES dual cost scenario policy forbids forecast computation")
    if config.diagnostics_authorized:
        raise CarverBlocked("S09 MES dual cost scenario policy forbids diagnostics")
    if config.backtest_authorized:
        raise CarverBlocked("S09 MES dual cost scenario policy forbids backtests")
    if config.test_validation_lockbox_forward_authorized:
        raise CarverBlocked("S09 MES dual cost scenario policy forbids TEST/VALIDATION/Lockbox/Forward access")
    if config.git_operations_authorized:
        raise CarverBlocked("S09 MES dual cost scenario policy forbids Git operations")
    return {"status": "AUTHORIZED_DUAL_COST_SCENARIO_POLICY_READY"}


def build_request_manifest_payload(config: S09MESDualCostScenarioPolicyConfig) -> dict[str, str]:
    run_dual_cost_scenario_policy_guard(config)
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "dual_scenario_policy": "YES",
        "conservative_pass_through_scenario": "YES",
        "etf_all_in_sim_fee_scenario": "YES",
        "risk_adjusted_cost_values_lock": "NO",
        "speed_eligibility_computation": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def build_cost_scenario_rows(*, daily_price_risk_currency: float, current_price: float) -> tuple[dict[str, str], ...]:
    _require_positive("daily price risk", daily_price_risk_currency)
    _require_positive("current price", current_price)
    notional = float(current_price) * MES_MULTIPLIER
    annualized_usd_price_risk = float(daily_price_risk_currency) * DAILY_TO_ANNUAL_RISK_SCALAR * MES_MULTIPLIER
    scenarios = (
        (
            CONSERVATIVE_SCENARIO,
            (EXCHANGE_FEE_PER_SIDE * 2) + (NFA_FEE_PER_SIDE * 2) + (ETF_BROKER_COMMISSION_PER_SIDE * 2) + SPREAD_SLIPPAGE_ROUND_TURN,
            "exchange_fee|clearing_regulatory_fee|broker_commission|spread_slippage",
            "Conservative live-futures pass-through: includes CME and NFA as separate per-side charges.",
        ),
        (
            ETF_ALL_IN_SCENARIO,
            (ETF_BROKER_COMMISSION_PER_SIDE * 2) + SPREAD_SLIPPAGE_ROUND_TURN,
            "broker_commission|spread_slippage",
            "ETF simulated-fee sensitivity: treats ETF micro commission as all-in for exchange/NFA pass-through.",
        ),
    )
    rows: list[dict[str, str]] = []
    for scenario_name, total_cost, included_components, note in scenarios:
        ratio = total_cost / annualized_usd_price_risk
        notional_pct = total_cost / notional * 100.0
        rows.append(
            {
                "scenario_name": scenario_name,
                "total_round_turn_cost_per_trade_currency": _fmt2(total_cost),
                "daily_price_risk_currency": _fmt_full(daily_price_risk_currency),
                "annualized_price_risk_currency": _fmt_full(annualized_usd_price_risk),
                "cost_to_annualized_price_risk_ratio": _fmt6(ratio),
                "cost_to_annualized_price_risk_pct": _fmt6(ratio * 100.0),
                "current_price": _fmt_full(current_price),
                "notional_currency": _fmt2(notional),
                "cost_to_notional_pct": _fmt6(notional_pct),
                "included_components": included_components,
                "policy_note": note,
                "status": ROW_STATUS,
            }
        )
    return tuple(rows)


def main() -> None:
    config = S09MESDualCostScenarioPolicyConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        window_start=WINDOW_START.isoformat(),
        window_end=WINDOW_END.isoformat(),
        dual_scenario_policy=True,
        conservative_pass_through_scenario=True,
        etf_all_in_sim_fee_scenario=True,
        risk_adjusted_cost_values_lock=False,
        speed_eligibility_computation=False,
        forecast_computation=False,
        diagnostics_authorized=False,
        backtest_authorized=False,
        test_validation_lockbox_forward_authorized=False,
        git_operations_authorized=False,
    )
    written = write_dual_cost_scenario_policy_artifacts(config)
    print("S09_MES_DUAL_COST_SCENARIO_POLICY_RESULT_WRITTEN")
    print(f"artifacts={len(written)}")


def write_dual_cost_scenario_policy_artifacts(config: S09MESDualCostScenarioPolicyConfig) -> tuple[Path, ...]:
    run_dual_cost_scenario_policy_guard(config)
    current_price, daily_risk = _locked_daily_price_risk_for_cost_lock()
    rows = build_cost_scenario_rows(daily_price_risk_currency=daily_risk, current_price=current_price)
    COST_ROOT.mkdir(parents=True, exist_ok=True)
    _write_text(SCENARIO_LEDGER_PATH, _render_scenario_ledger(rows))
    _write_json(SCENARIO_STATUS_PATH, _status_payload(rows))
    _write_text(SCENARIO_PROVENANCE_PATH, _render_provenance(rows))
    _write_text(RESULT_PATH, _render_result(rows))
    _write_text(LOCAL_AUDIT_PATH, _render_local_audit(rows))
    _write_text(SCENARIO_HASH_PATH, _render_sha256_manifest((SCENARIO_LEDGER_PATH, SCENARIO_STATUS_PATH, SCENARIO_PROVENANCE_PATH, RESULT_PATH, LOCAL_AUDIT_PATH)))
    return (SCENARIO_LEDGER_PATH, SCENARIO_STATUS_PATH, SCENARIO_PROVENANCE_PATH, RESULT_PATH, LOCAL_AUDIT_PATH, SCENARIO_HASH_PATH)


def _locked_daily_price_risk_for_cost_lock() -> tuple[float, float]:
    with DAILY_RISK_LEDGER_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        if row["completed_trading_date"] == LOCKED_COMPLETED_TRADING_DATE.isoformat():
            if row["status"] != "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE":
                raise CarverBlocked("S09 MES dual cost scenario policy requires locked daily price risk")
            return float(row["current_price"]), float(row["daily_price_risk_currency"])
    raise CarverBlocked("S09 MES dual cost scenario policy could not find locked cost date daily price risk")


def _render_scenario_ledger(rows: tuple[dict[str, str], ...]) -> str:
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
        "remaining_evidence_count": 5,
        "risk_adjusted_cost_values_lock": "NO",
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "scenario_count": len(rows),
        "scenario_names": [row["scenario_name"] for row in rows],
        "selected_evidence_name": "cost_scenario_policy",
        "speed_eligibility_computation": "NO",
        "status": STATUS,
        "strategy_input_readiness_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
        "test_validation_lockbox_forward_access": "NO",
    }


def _render_provenance(rows: tuple[dict[str, str], ...]) -> str:
    return f"""# S09 MES Dual Cost Scenario Policy Provenance

Date: 2026-06-03

Status:

```text
{STATUS}
```

Operator decision:

Run both cost models and calculate based on both before any backtest result is
seen.

Scenarios:

- {rows[0]["scenario_name"]}: {rows[0]["total_round_turn_cost_per_trade_currency"]} USD round turn, {rows[0]["cost_to_annualized_price_risk_pct"]}% of locked annualized USD price risk
- {rows[1]["scenario_name"]}: {rows[1]["total_round_turn_cost_per_trade_currency"]} USD round turn, {rows[1]["cost_to_annualized_price_risk_pct"]}% of locked annualized USD price risk

Unit bridge:

- annualized USD price risk = locked daily point risk * 16 * MES 5 USD/point multiplier
- this policy remains pre-backtest and does not itself lock formal risk-adjusted cost values

Boundary:

This is a cost-scenario policy lock. It does not lock formal risk-adjusted
cost values, speed eligibility, forecasts, diagnostics, backtests, TEST,
VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations.
"""


def _render_result(rows: tuple[dict[str, str], ...]) -> str:
    return f"""# S09 MES Dual Cost Scenario Policy Lock Result

Date: 2026-06-03

Status:

```text
{STATUS}
```

Decision:

Both cost models are locked for all future S09 MES calculations until replaced
by a new pre-result operator policy:

- {rows[0]["scenario_name"]}: {rows[0]["total_round_turn_cost_per_trade_currency"]} USD round turn; {rows[0]["cost_to_annualized_price_risk_pct"]}% of locked annualized USD price risk.
- {rows[1]["scenario_name"]}: {rows[1]["total_round_turn_cost_per_trade_currency"]} USD round turn; {rows[1]["cost_to_annualized_price_risk_pct"]}% of locked annualized USD price risk.

Correction note:

The policy ratio is expressed against annualized USD price risk to avoid
reintroducing the superseded daily-denominator cost-screen mistake.

Boundary:

No formal risk-adjusted cost value lock, no speed eligibility computation, no
forecast computation, no diagnostics, no backtests, no TEST, no VALIDATION, no
Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging,
no commit, no push, no PR, and no remote operations were performed.
"""


def _render_local_audit(rows: tuple[dict[str, str], ...]) -> str:
    return f"""# S09 MES Dual Cost Scenario Policy Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_DUAL_COST_SCENARIO_POLICY_LOCKED_NO_BACKTEST
```

Checks:

- both scenarios are present: {rows[0]["scenario_name"]}; {rows[1]["scenario_name"]}
- conservative total is {rows[0]["total_round_turn_cost_per_trade_currency"]} USD round turn
- ETF all-in simulated-fee total is {rows[1]["total_round_turn_cost_per_trade_currency"]} USD round turn
- no formal risk-adjusted cost value lock
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST, VALIDATION, Lockbox, Forward
- no Git staging, commit, push, or PR

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
            raise CarverBlocked("S09 MES dual cost scenario SHA paths must be unique")
        seen.add(relative)
        lines.append(f"{_sha256(path)}  {relative}")
    return "\n".join(lines) + "\n"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _require_positive(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)) or value <= 0:
        raise CarverBlocked(f"S09 MES dual cost scenario {name} must be finite and positive")


def _fmt2(value: float) -> str:
    return f"{float(value):.2f}".rstrip("0").rstrip(".")


def _fmt6(value: float) -> str:
    return f"{float(value):.6f}"


def _fmt_full(value: float) -> str:
    return str(float(value)).rstrip("0").rstrip(".")


if __name__ == "__main__":
    main()

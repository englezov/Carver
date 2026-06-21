from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import dataclass
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
from carver.spine.m2 import S09_EWMAC_SPANS, s09_fdm_for_allowed_spans  # noqa: E402
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
from tools.databento.carver_s09_mes_dual_speed_eligibility_values import (  # noqa: E402
    SPEED_LEDGER_PATH,
    SPEED_STATUS_PATH,
    STATUS as DUAL_SPEED_STATUS,
)
from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: E402
    S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow,
    render_s09_mes_strategy_input_evidence_completion_eligible_speed_set_fdm_ledger_csv,
)

RUN_ID = "20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM"
GATE = "S09_MES_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM_ROW_LOCK"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
STATUS = "LOCKED_S09_MES_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM_ROW_NOT_BACKTEST"
ROW_STATUS = "LOCKED_SOURCE_NATIVE_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM"
SOURCE_LABEL = "LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_LEDGER"
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_strategy_input_evidence_completion" / WINDOW_LABEL
SPEED_ROOT = OUTPUT_ROOT / "speed"
LEDGER_PATH = SPEED_ROOT / f"{RUN_ID}_ledger.csv"
STATUS_PATH = SPEED_ROOT / f"{RUN_ID}_status.json"
PROVENANCE_PATH = SPEED_ROOT / f"{RUN_ID}_provenance.md"
HASH_PATH = SPEED_ROOT / f"{RUN_ID}_sha256.txt"
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM_ROW_LOCK_RESULT_2026-06-03.md"
LOCAL_AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM_ROW_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"


@dataclass(frozen=True)
class S09MESEligibleSpeedSetTable36FDMLockConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    dual_speed_eligibility_status: str
    eligible_speed_set_lock: bool
    table36_fdm_row_lock: bool
    hash_bound_provenance_lock: bool
    forecast_computation: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


def run_eligible_speed_set_table36_fdm_lock_guard(
    config: S09MESEligibleSpeedSetTable36FDMLockConfig,
) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES eligible speed set and Table 36 FDM lock is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES eligible speed set and Table 36 FDM lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES eligible speed set and Table 36 FDM lock is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES eligible speed set and Table 36 FDM lock is locked to the machinery-development slice")
    if config.dual_speed_eligibility_status != DUAL_SPEED_STATUS:
        raise CarverBlocked("S09 MES eligible speed set and Table 36 FDM lock requires corrected dual speed eligibility")
    if not config.eligible_speed_set_lock:
        raise CarverBlocked("S09 MES eligible speed set must be explicitly locked")
    if not config.table36_fdm_row_lock:
        raise CarverBlocked("S09 MES Table 36 FDM row must be explicitly locked")
    if config.hash_bound_provenance_lock:
        raise CarverBlocked("S09 MES eligible/FDM lock must not lock final hash-bound provenance")
    if config.forecast_computation:
        raise CarverBlocked("S09 MES eligible/FDM lock forbids forecast computation")
    if config.diagnostics_authorized:
        raise CarverBlocked("S09 MES eligible/FDM lock forbids diagnostics")
    if config.backtest_authorized:
        raise CarverBlocked("S09 MES eligible/FDM lock forbids backtests")
    if config.test_validation_lockbox_forward_authorized:
        raise CarverBlocked("S09 MES eligible/FDM lock forbids TEST/VALIDATION/Lockbox/Forward access")
    if config.git_operations_authorized:
        raise CarverBlocked("S09 MES eligible/FDM lock forbids Git operations")
    return {"status": "AUTHORIZED_ELIGIBLE_SPEED_SET_TABLE36_FDM_LOCK_READY"}


def build_request_manifest_payload(config: S09MESEligibleSpeedSetTable36FDMLockConfig) -> dict[str, str]:
    run_eligible_speed_set_table36_fdm_lock_guard(config)
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "dual_speed_eligibility_status": DUAL_SPEED_STATUS,
        "eligible_speed_set_lock": "YES",
        "table36_fdm_row_lock": "YES",
        "hash_bound_provenance_lock": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def build_eligible_speed_set_table36_fdm_row(
    *,
    speed_rows: tuple[dict[str, str], ...],
    source_sha256: str = "0" * 64,
) -> S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow:
    _validate_source_sha256(source_sha256)
    _validate_speed_rows(speed_rows)
    eligible_by_scenario: dict[str, set[int]] = {}
    for row in speed_rows:
        scenario = row["scenario_name"]
        eligible_by_scenario.setdefault(scenario, set())
        if row["eligible"] == "True":
            eligible_by_scenario[scenario].add(int(row["span"]))

    common_spans = set(S09_EWMAC_SPANS)
    for scenario in (CONSERVATIVE_SCENARIO, ETF_ALL_IN_SCENARIO):
        common_spans &= eligible_by_scenario[scenario]
    eligible_spans = tuple(span for span in S09_EWMAC_SPANS if span in common_spans)
    if not eligible_spans:
        raise CarverBlocked("S09 MES eligible/FDM lock found no common surviving speed set")
    return S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow(
        eligible_spans=eligible_spans,
        table36_fdm=s09_fdm_for_allowed_spans(eligible_spans),
        source_label=SOURCE_LABEL,
        source_sha256=source_sha256,
        status=ROW_STATUS,
    )


def main() -> None:
    config = S09MESEligibleSpeedSetTable36FDMLockConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        window_start=WINDOW_START.isoformat(),
        window_end=WINDOW_END.isoformat(),
        dual_speed_eligibility_status=DUAL_SPEED_STATUS,
        eligible_speed_set_lock=True,
        table36_fdm_row_lock=True,
        hash_bound_provenance_lock=False,
        forecast_computation=False,
        diagnostics_authorized=False,
        backtest_authorized=False,
        test_validation_lockbox_forward_authorized=False,
        git_operations_authorized=False,
    )
    written = write_eligible_speed_set_table36_fdm_lock_artifacts(config)
    print("S09_MES_ELIGIBLE_SPEED_SET_TABLE36_FDM_LOCK_RESULT_WRITTEN")
    print(f"artifacts={len(written)}")


def write_eligible_speed_set_table36_fdm_lock_artifacts(
    config: S09MESEligibleSpeedSetTable36FDMLockConfig,
) -> tuple[Path, ...]:
    run_eligible_speed_set_table36_fdm_lock_guard(config)
    speed_rows = _locked_speed_rows()
    row = build_eligible_speed_set_table36_fdm_row(
        speed_rows=speed_rows,
        source_sha256=_sha256(SPEED_LEDGER_PATH),
    )
    SPEED_ROOT.mkdir(parents=True, exist_ok=True)
    _write_text(LEDGER_PATH, render_s09_mes_strategy_input_evidence_completion_eligible_speed_set_fdm_ledger_csv((row,)))
    _write_json(STATUS_PATH, _status_payload(row))
    _write_text(PROVENANCE_PATH, _render_provenance(row))
    _write_text(RESULT_PATH, _render_result(row))
    _write_text(LOCAL_AUDIT_PATH, _render_local_audit(row))
    _write_text(HASH_PATH, _render_sha256_manifest((LEDGER_PATH, STATUS_PATH, PROVENANCE_PATH, RESULT_PATH, LOCAL_AUDIT_PATH)))
    return (LEDGER_PATH, STATUS_PATH, PROVENANCE_PATH, RESULT_PATH, LOCAL_AUDIT_PATH, HASH_PATH)


def _locked_speed_rows() -> tuple[dict[str, str], ...]:
    status = json.loads(SPEED_STATUS_PATH.read_text(encoding="utf-8"))
    if status.get("status") != DUAL_SPEED_STATUS:
        raise CarverBlocked("S09 MES eligible/FDM lock requires corrected dual speed status")
    if status.get("eligible_speed_set_lock") != "NO" or status.get("table36_fdm_row_lock") != "NO":
        raise CarverBlocked("S09 MES eligible/FDM lock must consume pre-eligible-set speed values")
    if status.get("backtests_run") != "NO":
        raise CarverBlocked("S09 MES eligible/FDM lock forbids backtested source inputs")
    with SPEED_LEDGER_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))
    _validate_speed_rows(rows)
    return rows


def _validate_speed_rows(rows: tuple[dict[str, str], ...]) -> None:
    expected_pairs = tuple((scenario, str(span)) for scenario in (CONSERVATIVE_SCENARIO, ETF_ALL_IN_SCENARIO) for span in S09_EWMAC_SPANS)
    actual_pairs = tuple((row.get("scenario_name"), row.get("span")) for row in rows)
    if actual_pairs != expected_pairs:
        raise CarverBlocked("S09 MES eligible/FDM lock requires both scenarios and all six spans in locked order")
    for row in rows:
        if row.get("completed_trading_date") != LOCKED_COMPLETED_TRADING_DATE.isoformat():
            raise CarverBlocked("S09 MES eligible/FDM lock requires the locked completed trading date")
        if row.get("status") != "LOCKED_SOURCE_NATIVE_DUAL_SPEED_ELIGIBILITY_VALUE_NOT_ELIGIBLE_SET_NOT_BACKTEST":
            raise CarverBlocked("S09 MES eligible/FDM lock requires locked non-FDM speed rows")
        if row.get("eligible") != "True":
            raise CarverBlocked("S09 MES eligible/FDM lock requires every dual-scenario speed row to survive")
        _require_positive("risk-adjusted cost", row.get("risk_adjusted_cost_per_trade_sr"))
        _require_positive("annualized cost burden", row.get("annualized_cost_burden_sr"))
        _require_positive("threshold", row.get("threshold_sr"))


def _status_payload(row: S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow) -> dict[str, Any]:
    return {
        "backtests_run": "NO",
        "diagnostics_run": "NO",
        "eligible_speed_set_lock": "YES",
        "eligible_spans": list(row.eligible_spans),
        "evidence_completion_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
        "forecast_computation": "NO",
        "gate": GATE,
        "git_operations": "NO",
        "hash_bound_provenance_lock": "NO",
        "lane_class": LANE_CLASS,
        "machinery_development_slice": WINDOW_TEXT,
        "remaining_evidence_count": 1,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "selected_evidence_names": ["eligible_speed_set", "table36_fdm_row"],
        "source_dual_speed_status": DUAL_SPEED_STATUS,
        "status": STATUS,
        "strategy_input_readiness_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
        "table36_fdm": row.table36_fdm,
        "table36_fdm_row_lock": "YES",
        "test_validation_lockbox_forward_access": "NO",
    }


def _render_provenance(row: S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow) -> str:
    spans = _format_spans(row.eligible_spans)
    return f"""# S09 MES Eligible Speed Set And Table 36 FDM Provenance

Date: 2026-06-03

Status:

```text
{STATUS}
```

Inputs:

- corrected dual speed eligibility status: {DUAL_SPEED_STATUS}
- machinery-development slice: {WINDOW_TEXT}
- completed trading date: {LOCKED_COMPLETED_TRADING_DATE.isoformat()}

Locked values:

- eligible_spans: {spans}
- table36_fdm: {row.table36_fdm}

Boundary:

This locks only the eligible EWMAC speed set and matching Table 36 FDM row. It
does not lock final hash-bound provenance, compute forecasts, run diagnostics,
run backtests, access TEST, VALIDATION, Lockbox, Forward, deploy, trade,
promote, stage Git, commit, push, create a PR, or perform remote operations.
"""


def _render_result(row: S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow) -> str:
    spans = _format_spans(row.eligible_spans)
    return f"""# S09 MES Eligible Speed Set And Table 36 FDM Lock Result

Date: 2026-06-03

Status:

```text
{STATUS}
```

Formal locks:

- eligible_spans: {spans}
- table36_fdm: {row.table36_fdm}
- source: corrected dual speed eligibility ledger

Remaining evidence:

- hash_bound_provenance remains unlocked
- strategy input readiness remains fail-closed

Boundary:

No forecast computation, diagnostics, backtests, TEST, VALIDATION, Lockbox,
Forward, deployment, trading, promotion, Git staging, commit, push, PR, or
remote operations were performed.
"""


def _render_local_audit(row: S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow) -> str:
    return f"""# S09 MES Eligible Speed Set And Table 36 FDM Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_ELIGIBLE_SPEED_SET_TABLE36_FDM_LOCKED_NO_BACKTEST
```

Checks:

- corrected dual speed eligibility status is consumed
- both cost scenarios survive all six spans
- eligible speed set is {_format_spans(row.eligible_spans)}
- Table 36 FDM is {row.table36_fdm}
- hash-bound provenance remains unlocked
- strategy input readiness remains fail-closed
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
    lines: list[str] = []
    seen: set[str] = set()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        if relative in seen:
            raise CarverBlocked("S09 MES eligible/FDM SHA paths must be unique")
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
        raise CarverBlocked("S09 MES eligible/FDM source hash is missing")
    try:
        int(value, 16)
    except ValueError as exc:
        raise CarverBlocked("S09 MES eligible/FDM source hash is invalid") from exc


def _require_positive(name: str, raw_value: object) -> None:
    try:
        value = float(raw_value)
    except (TypeError, ValueError) as exc:
        raise CarverBlocked(f"S09 MES eligible/FDM {name} must be numeric") from exc
    if value <= 0:
        raise CarverBlocked(f"S09 MES eligible/FDM {name} must be positive")


def _format_spans(spans: tuple[int, ...]) -> str:
    return "|".join(str(span) for span in spans)


if __name__ == "__main__":
    main()

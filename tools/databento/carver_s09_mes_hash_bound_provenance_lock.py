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
from tools.databento.carver_s09_mes_dual_risk_adjusted_cost_values import STATUS as DUAL_RISK_STATUS  # noqa: E402
from tools.databento.carver_s09_mes_dual_speed_eligibility_values import STATUS as DUAL_SPEED_STATUS  # noqa: E402
from tools.databento.carver_s09_mes_eligible_speed_set_table36_fdm_lock import STATUS as ELIGIBLE_FDM_STATUS  # noqa: E402
from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: E402
    DESIGN_ORDERING,
    EVIDENCE_COMPLETION_LOCKED_STATUS,
    GATE,
    LANE_CLASS,
    MACHINERY_DEVELOPMENT_SLICE_END,
    MACHINERY_DEVELOPMENT_SLICE_START,
    MACHINERY_DEVELOPMENT_SLICE_TEXT,
    OUTPUT_ROOT_RELATIVE,
    READINESS_HANDOFF_NEXT_GATE,
    REQUIRED_EVIDENCE_NAMES,
    ROOT_SYMBOL,
    ROW_ID,
    RUNTIME_INPUT_LOCK_SCOPE,
    STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_STATUS,
)

RUN_ID = "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION"
STATUS = EVIDENCE_COMPLETION_LOCKED_STATUS
HASH_BOUND_STATUS = "LOCKED_SOURCE_NATIVE_HASH_BOUND_PROVENANCE"
OUTPUT_ROOT = ROOT / OUTPUT_ROOT_RELATIVE
EVIDENCE_LEDGER_PATH = OUTPUT_ROOT / "evidence" / f"{RUN_ID}_required_evidence_ledger.csv"
STATUS_PATH = OUTPUT_ROOT / "status" / f"{RUN_ID}_status.json"
PROVENANCE_PATH = OUTPUT_ROOT / "provenance" / f"{RUN_ID}_provenance.md"
HASH_PATH = OUTPUT_ROOT / "hashes" / f"{RUN_ID}_sha256.txt"
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_HASH_BOUND_PROVENANCE_LOCK_RESULT_2026-06-03.md"
LOCAL_AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_HASH_BOUND_PROVENANCE_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"


@dataclass(frozen=True)
class S09MESHashBoundProvenanceLockConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    hash_bound_provenance_lock: bool
    strategy_input_readiness_gate: bool
    forecast_computation: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


def run_hash_bound_provenance_lock_guard(config: S09MESHashBoundProvenanceLockConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES hash-bound provenance lock is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES hash-bound provenance lock is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES hash-bound provenance lock is locked to Appendix C MES row")
    if config.window_start != MACHINERY_DEVELOPMENT_SLICE_START or config.window_end != MACHINERY_DEVELOPMENT_SLICE_END:
        raise CarverBlocked("S09 MES hash-bound provenance lock is locked to the machinery-development slice")
    if not config.hash_bound_provenance_lock:
        raise CarverBlocked("S09 MES hash-bound provenance must be explicitly locked")
    if config.strategy_input_readiness_gate:
        raise CarverBlocked("S09 MES hash-bound provenance lock must not run the strategy-input readiness gate")
    if config.forecast_computation:
        raise CarverBlocked("S09 MES hash-bound provenance lock forbids forecast computation")
    if config.diagnostics_authorized:
        raise CarverBlocked("S09 MES hash-bound provenance lock forbids diagnostics")
    if config.backtest_authorized:
        raise CarverBlocked("S09 MES hash-bound provenance lock forbids backtests")
    if config.test_validation_lockbox_forward_authorized:
        raise CarverBlocked("S09 MES hash-bound provenance lock forbids TEST/VALIDATION/Lockbox/Forward access")
    if config.git_operations_authorized:
        raise CarverBlocked("S09 MES hash-bound provenance lock forbids Git operations")
    _validate_upstream_locks()
    return {"status": "AUTHORIZED_HASH_BOUND_PROVENANCE_LOCK_READY"}


def build_request_manifest_payload(config: S09MESHashBoundProvenanceLockConfig) -> dict[str, str]:
    run_hash_bound_provenance_lock_guard(config)
    return {
        "gate": "S09_MES_HASH_BOUND_PROVENANCE_LOCK",
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_start": MACHINERY_DEVELOPMENT_SLICE_START,
        "window_end": MACHINERY_DEVELOPMENT_SLICE_END,
        "hash_bound_provenance_lock": "YES",
        "strategy_input_readiness_gate": "NO",
        "next_gate": READINESS_HANDOFF_NEXT_GATE,
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def main() -> None:
    config = S09MESHashBoundProvenanceLockConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        window_start=MACHINERY_DEVELOPMENT_SLICE_START,
        window_end=MACHINERY_DEVELOPMENT_SLICE_END,
        hash_bound_provenance_lock=True,
        strategy_input_readiness_gate=False,
        forecast_computation=False,
        diagnostics_authorized=False,
        backtest_authorized=False,
        test_validation_lockbox_forward_authorized=False,
        git_operations_authorized=False,
    )
    written = write_hash_bound_provenance_lock_artifacts(config)
    print("S09_MES_HASH_BOUND_PROVENANCE_LOCK_RESULT_WRITTEN")
    print(f"artifacts={len(written)}")


def write_hash_bound_provenance_lock_artifacts(config: S09MESHashBoundProvenanceLockConfig) -> tuple[Path, ...]:
    run_hash_bound_provenance_lock_guard(config)
    EVIDENCE_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    HASH_PATH.parent.mkdir(parents=True, exist_ok=True)

    _write_text(EVIDENCE_LEDGER_PATH, _render_locked_required_evidence_ledger())
    _write_json(STATUS_PATH, _status_payload())
    _write_text(PROVENANCE_PATH, _render_provenance())
    _write_text(RESULT_PATH, _render_result())
    _write_text(LOCAL_AUDIT_PATH, _render_local_audit())

    paths_without_hashes = _manifest_paths()
    _write_text(HASH_PATH, _render_sha256_manifest(paths_without_hashes))
    return (*paths_without_hashes, HASH_PATH)


def _validate_upstream_locks() -> None:
    expected_statuses = {
        "official_lifecycle_evidence": (
            OUTPUT_ROOT / "lifecycle" / "20260603_S09_MES_LIFECYCLE_EVIDENCE_status.json",
            "LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE",
        ),
        "roll_trading_day_semantics": (
            OUTPUT_ROOT / "roll" / "20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_status.json",
            "LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS",
        ),
        "annual_risk_runtime_values": (
            OUTPUT_ROOT / "risk" / "20260603_S09_MES_ANNUAL_RISK_RUNTIME_status.json",
            "LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE",
        ),
        "daily_price_risk_values": (
            OUTPUT_ROOT / "risk" / "20260603_S09_MES_DAILY_PRICE_RISK_status.json",
            "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE",
        ),
        "historical_mes_cost_values": (
            OUTPUT_ROOT / "cost" / "20260603_S09_MES_HISTORICAL_COST_VALUE_status.json",
            "LOCKED_S09_MES_HISTORICAL_COST_VALUES_NOT_RISK_ADJUSTED_COST",
        ),
        "risk_adjusted_cost_values": (
            OUTPUT_ROOT / "cost" / "20260603_S09_MES_DUAL_RISK_ADJUSTED_COST_status.json",
            DUAL_RISK_STATUS,
        ),
        "speed_eligibility_values": (
            OUTPUT_ROOT / "speed" / "20260603_S09_MES_DUAL_SPEED_ELIGIBILITY_status.json",
            DUAL_SPEED_STATUS,
        ),
        "eligible_speed_set_and_table36_fdm": (
            OUTPUT_ROOT / "speed" / "20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_status.json",
            ELIGIBLE_FDM_STATUS,
        ),
    }
    for name, (path, expected_status) in expected_statuses.items():
        payload = _read_json(path)
        if payload.get("status") != expected_status:
            raise CarverBlocked(f"S09 MES hash-bound provenance upstream {name} is not locked")
        _require_no_execution_flags(payload, name)


def _require_no_execution_flags(payload: dict[str, Any], name: str) -> None:
    for key in ("forecast_computation", "diagnostics_run", "backtests_run", "test_validation_lockbox_forward_access", "git_operations"):
        if payload.get(key) not in (None, "NO"):
            raise CarverBlocked(f"S09 MES hash-bound provenance upstream {name} has non-NO {key}")


def _render_locked_required_evidence_ledger() -> str:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(("evidence_name", "required_status", "current_status", "blocking_reason", "next_action"))
    for evidence_name in REQUIRED_EVIDENCE_NAMES:
        writer.writerow(
            (
                evidence_name,
                "LOCKED_SOURCE_NATIVE_EVIDENCE",
                "LOCKED_SOURCE_NATIVE_EVIDENCE",
                "Evidence family is locked and hash-bound to the machinery-development slice.",
                "Proceed only to the separately authorized strategy-input readiness gate.",
            )
        )
    return buffer.getvalue()


def _status_payload() -> dict[str, Any]:
    return {
        "backtests_run": "NO",
        "databento_api_access": "NO",
        "design_ordering": DESIGN_ORDERING,
        "diagnostics_run": "NO",
        "forecast_computation": "NO",
        "gate": GATE,
        "hash_bound_provenance_status": HASH_BOUND_STATUS,
        "lane_class": LANE_CLASS,
        "locked_evidence_names": list(REQUIRED_EVIDENCE_NAMES),
        "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
        "market_row_parsing": "NO",
        "new_provider_data_download": "NO",
        "next_gate": READINESS_HANDOFF_NEXT_GATE,
        "remaining_evidence_count": 0,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "runtime_input_lock_scope": RUNTIME_INPUT_LOCK_SCOPE,
        "status": STATUS,
        "strategy_input_readiness_status": STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_STATUS,
        "test_validation_lockbox_forward_access": "NO",
    }


def _render_provenance() -> str:
    return f"""# S09 MES Strategy Input Evidence Completion Hash-Bound Provenance

Date: 2026-06-03

Status:

```text
{STATUS}
```

Scope:

- lane_class: {LANE_CLASS}
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- design_ordering: {DESIGN_ORDERING}

Locked evidence:

- official_lifecycle_evidence
- roll_trading_day_semantics
- annual_risk_runtime_values
- daily_price_risk_values
- historical_mes_cost_values
- risk_adjusted_cost_values
- speed_eligibility_values
- eligible_speed_set
- table36_fdm_row
- hash_bound_provenance

Next gate:

```text
{READINESS_HANDOFF_NEXT_GATE}
```

Boundary:

This locks hash-bound provenance and evidence completion only. It does not run
the strategy-input readiness gate, compute forecasts, run diagnostics, run
backtests, access TEST, VALIDATION, Lockbox, Forward, deploy, trade, promote,
stage Git, commit, push, create a PR, or perform remote operations.
"""


def _render_result() -> str:
    return f"""# S09 MES Hash-Bound Provenance Lock Result

Date: 2026-06-03

Status:

```text
{STATUS}
```

Result:

- hash_bound_provenance: LOCKED
- remaining_evidence_count: 0
- strategy_input_readiness_status: {STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_STATUS}
- next_gate: {READINESS_HANDOFF_NEXT_GATE}

Boundary:

No strategy-input readiness gate, forecast computation, diagnostics, backtests,
TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were performed.
"""


def _render_local_audit() -> str:
    return f"""# S09 MES Hash-Bound Provenance Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_HASH_BOUND_PROVENANCE_LOCKED_NO_READINESS_NO_BACKTEST
```

Checks:

- every required evidence family has a locked source-native status
- required evidence ledger marks all required rows locked
- final SHA256 manifest excludes hash files and hashes the current packet files
- remaining_evidence_count is 0
- strategy input readiness remains only awaiting the readiness gate
- forecasts, diagnostics, and backtests were not run
- TEST, VALIDATION, Lockbox, and Forward were not accessed
- Git staging, commit, push, and PR were not performed

This local audit must be reviewed by a spawned hostile-audit subagent.
"""


def _manifest_paths() -> tuple[Path, ...]:
    paths = []
    for path in OUTPUT_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if "/hashes/" in relative or relative.endswith("_sha256.txt"):
            continue
        paths.append(path)
    paths.extend((RESULT_PATH, LOCAL_AUDIT_PATH))
    unique = sorted(set(paths), key=lambda item: item.relative_to(ROOT).as_posix())
    return tuple(unique)


def _render_sha256_manifest(paths: tuple[Path, ...]) -> str:
    lines: list[str] = []
    seen: set[str] = set()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        if relative in seen:
            raise CarverBlocked("S09 MES hash-bound provenance manifest paths must be unique")
        seen.add(relative)
        if "/hashes/" in relative or relative.endswith("_sha256.txt"):
            raise CarverBlocked("S09 MES hash-bound provenance manifest must not hash hash files")
        lines.append(f"{_sha256(path)}  {relative}")
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CarverBlocked(f"S09 MES hash-bound provenance missing upstream status: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


if __name__ == "__main__":
    main()

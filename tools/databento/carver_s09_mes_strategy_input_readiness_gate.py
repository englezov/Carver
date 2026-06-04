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

from carver.spine.m0 import CarverBlocked, LaneClass  # noqa: E402
from carver.spine.s09_mes_readiness import (  # noqa: E402
    S09_MES_EVIDENCE_COMPLETION_HANDOFF_STATUS,
    S09_MES_EVIDENCE_COMPLETION_LOCKED_STATUS,
    S09_MES_EVIDENCE_AWAITING_READINESS_STATUS,
    S09_MES_MACHINERY_DEVELOPMENT_SLICE_TEXT,
    S09_MES_STRATEGY_INPUT_READINESS_GATE,
    S09MESStrategyInputReadinessGateConfig,
    run_s09_mes_strategy_input_readiness_gate,
)
from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: E402
    DESIGN_ORDERING,
    MACHINERY_DEVELOPMENT_SLICE_TEXT,
    OUTPUT_ROOT_RELATIVE,
    ROOT_SYMBOL,
    ROW_ID,
    RUN_ID as EVIDENCE_RUN_ID,
    S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest,
    build_s09_mes_strategy_input_evidence_completion_readiness_handoff_bundle,
)

RUN_ID = "20260603_S09_MES_STRATEGY_INPUT_READINESS"
GATE = S09_MES_STRATEGY_INPUT_READINESS_GATE
STATUS = "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY_NOT_BACKTEST_AUTHORIZATION"
STRATEGY_INPUT_STATUS = "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY"
NEXT_GATE = "S09_MES_FIRST_DEV_RECON_BACKTEST_AUTHORIZATION_GATE"
OUTPUT_ROOT_RELATIVE = "docs/researchops/s09/mes_strategy_input_readiness/2019-05-05_2020-04-05"
OUTPUT_ROOT = ROOT / OUTPUT_ROOT_RELATIVE
EVIDENCE_OUTPUT_ROOT = ROOT / OUTPUT_ROOT_RELATIVE.replace("mes_strategy_input_readiness", "mes_strategy_input_evidence_completion")
EVIDENCE_STATUS_PATH = (
    ROOT
    / "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/"
    f"{EVIDENCE_RUN_ID}_status.json"
)
EVIDENCE_HASH_PATH = (
    ROOT
    / "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/hashes/"
    f"{EVIDENCE_RUN_ID}_sha256.txt"
)
STATUS_PATH = OUTPUT_ROOT / "status" / f"{RUN_ID}_status.json"
LEDGER_PATH = OUTPUT_ROOT / "readiness" / f"{RUN_ID}_readiness_ledger.csv"
PROVENANCE_PATH = OUTPUT_ROOT / "provenance" / f"{RUN_ID}_provenance.md"
HASH_PATH = OUTPUT_ROOT / "hashes" / f"{RUN_ID}_sha256.txt"
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_STRATEGY_INPUT_READINESS_GATE_RESULT_2026-06-03.md"
LOCAL_AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_STRATEGY_INPUT_READINESS_GATE_LOCAL_HOSTILE_AUDIT_2026-06-03.md"


@dataclass(frozen=True)
class S09MESStrategyInputReadinessGateExecutionConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    machinery_development_slice: str
    evidence_status_path: Path
    evidence_hash_path: Path
    databento_api_access_authorized: bool
    market_row_parsing_authorized: bool
    forecast_computation_authorized: bool
    diagnostics_authorized: bool
    backtest_authorized: bool
    test_validation_lockbox_forward_authorized: bool
    git_operations_authorized: bool


def main() -> None:
    config = S09MESStrategyInputReadinessGateExecutionConfig(
        execution_authorized=True,
        lane_class="SOURCE_NATIVE_FUTURES",
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        machinery_development_slice=MACHINERY_DEVELOPMENT_SLICE_TEXT,
        evidence_status_path=EVIDENCE_STATUS_PATH,
        evidence_hash_path=EVIDENCE_HASH_PATH,
        databento_api_access_authorized=False,
        market_row_parsing_authorized=False,
        forecast_computation_authorized=False,
        diagnostics_authorized=False,
        backtest_authorized=False,
        test_validation_lockbox_forward_authorized=False,
        git_operations_authorized=False,
    )
    written = write_s09_mes_strategy_input_readiness_gate_artifacts(config)
    print("S09_MES_STRATEGY_INPUT_READINESS_GATE_RESULT_WRITTEN")
    print(f"artifacts={len(written)}")


def run_strategy_input_readiness_gate_guard(
    config: S09MESStrategyInputReadinessGateExecutionConfig,
) -> dict[str, str]:
    if config.execution_authorized is not True:
        raise CarverBlocked("S09 MES strategy-input readiness gate requires explicit operator authorization")
    if config.lane_class != "SOURCE_NATIVE_FUTURES":
        raise CarverBlocked("S09 MES strategy-input readiness gate is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES strategy-input readiness gate is locked to Appendix C MES row")
    if config.machinery_development_slice != MACHINERY_DEVELOPMENT_SLICE_TEXT:
        raise CarverBlocked("S09 MES strategy-input readiness gate must use the oldest machinery-development slice")
    for label, authorized in (
        ("Databento API access", config.databento_api_access_authorized),
        ("market-row parsing", config.market_row_parsing_authorized),
        ("forecast computation", config.forecast_computation_authorized),
        ("diagnostics", config.diagnostics_authorized),
        ("backtest", config.backtest_authorized),
        ("TEST/VALIDATION/Lockbox/Forward access", config.test_validation_lockbox_forward_authorized),
        ("Git operations", config.git_operations_authorized),
    ):
        if authorized is not False:
            raise CarverBlocked(f"S09 MES strategy-input readiness gate forbids {label}")

    evidence_status = _validated_evidence_status(config.evidence_status_path)
    _verify_hash_manifest(config.evidence_hash_path)
    spine_result = run_s09_mes_strategy_input_readiness_gate(
        S09MESStrategyInputReadinessGateConfig(
            execution_authorized=True,
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            root=ROOT_SYMBOL,
            row_id=ROW_ID,
            evidence_completion_status=evidence_status["status"],
            evidence_handoff_status=S09_MES_EVIDENCE_COMPLETION_HANDOFF_STATUS,
            strategy_input_readiness_status=evidence_status["strategy_input_readiness_status"],
            next_gate=evidence_status["next_gate"],
            machinery_development_slice=evidence_status["machinery_development_slice"],
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )
    )
    return {
        "status": STATUS,
        "spine_status": spine_result["status"],
        "gate": GATE,
        "next_gate": NEXT_GATE,
    }


def build_readiness_manifest_payload(config: S09MESStrategyInputReadinessGateExecutionConfig) -> dict[str, str]:
    guard = run_strategy_input_readiness_gate_guard(config)
    return {
        "gate": GATE,
        "status": guard["status"],
        "strategy_input_readiness_status": STRATEGY_INPUT_STATUS,
        "spine_status": guard["spine_status"],
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "machinery_development_slice": MACHINERY_DEVELOPMENT_SLICE_TEXT,
        "design_ordering": DESIGN_ORDERING,
        "evidence_completion_status": S09_MES_EVIDENCE_COMPLETION_LOCKED_STATUS,
        "evidence_handoff_status": S09_MES_EVIDENCE_COMPLETION_HANDOFF_STATUS,
        "next_gate": NEXT_GATE,
        "databento_api_access": "NO",
        "market_row_parsing": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def write_s09_mes_strategy_input_readiness_gate_artifacts(
    config: S09MESStrategyInputReadinessGateExecutionConfig,
) -> tuple[Path, ...]:
    manifest = build_readiness_manifest_payload(config)
    _write_handoff_bundle()
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    HASH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)

    _write_json(STATUS_PATH, _status_payload(manifest))
    _write_text(LEDGER_PATH, _render_readiness_ledger())
    _write_text(PROVENANCE_PATH, _render_provenance())
    _write_text(RESULT_PATH, _render_result())
    _write_text(LOCAL_AUDIT_PATH, _render_local_audit())
    manifest_paths = _manifest_paths()
    _write_text(HASH_PATH, _render_sha256_manifest(manifest_paths))
    return (*manifest_paths, HASH_PATH)


def _validated_evidence_status(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    if payload.get("status") != S09_MES_EVIDENCE_COMPLETION_LOCKED_STATUS:
        raise CarverBlocked("S09 MES strategy-input readiness requires locked evidence completion")
    if payload.get("remaining_evidence_count") != 0:
        raise CarverBlocked("S09 MES strategy-input readiness requires zero remaining evidence")
    if payload.get("strategy_input_readiness_status") != S09_MES_EVIDENCE_AWAITING_READINESS_STATUS:
        raise CarverBlocked("S09 MES evidence packet must be awaiting readiness gate")
    if payload.get("next_gate") != S09_MES_STRATEGY_INPUT_READINESS_GATE:
        raise CarverBlocked("S09 MES evidence packet next gate is not the readiness gate")
    if payload.get("hash_bound_provenance_status") != "LOCKED_SOURCE_NATIVE_HASH_BOUND_PROVENANCE":
        raise CarverBlocked("S09 MES strategy-input readiness requires hash-bound provenance")
    if payload.get("lane_class") != "SOURCE_NATIVE_FUTURES" or payload.get("root") != ROOT_SYMBOL or payload.get("row_id") != ROW_ID:
        raise CarverBlocked("S09 MES evidence packet does not match source-native MES row")
    for key in ("databento_api_access", "market_row_parsing", "forecast_computation", "diagnostics_run", "backtests_run", "test_validation_lockbox_forward_access"):
        if payload.get(key) != "NO":
            raise CarverBlocked(f"S09 MES evidence packet has non-NO {key}")
    return payload


def _verify_hash_manifest(path: Path) -> None:
    if not path.exists():
        raise CarverBlocked("S09 MES evidence hash manifest is missing")
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        expected, relative_path = line.split("  ", 1)
        if "/hashes/" in relative_path or relative_path.endswith("_sha256.txt"):
            raise CarverBlocked("S09 MES evidence hash manifest must not hash hash files")
        actual_path = ROOT / relative_path
        if not actual_path.exists():
            raise CarverBlocked(f"S09 MES evidence hash manifest line {line_number} points to a missing file")
        actual = _sha256(actual_path)
        if actual != expected:
            raise CarverBlocked(f"S09 MES evidence hash manifest line {line_number} does not match current artifact hash")


def _write_handoff_bundle() -> None:
    request = S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest(
        evidence_completion_status=S09_MES_EVIDENCE_COMPLETION_LOCKED_STATUS,
        strategy_input_readiness_status=S09_MES_EVIDENCE_AWAITING_READINESS_STATUS,
        remaining_evidence_count=0,
        next_gate=S09_MES_STRATEGY_INPUT_READINESS_GATE,
        lane_class="SOURCE_NATIVE_FUTURES",
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        machinery_development_slice=MACHINERY_DEVELOPMENT_SLICE_TEXT,
        databento_api_access="NO",
        market_row_parsing="NO",
        forecast_computation="NO",
        diagnostics_run="NO",
        backtests_run="NO",
        test_validation_lockbox_forward_access="NO",
    )
    for relative_path, text in build_s09_mes_strategy_input_evidence_completion_readiness_handoff_bundle(request).items():
        _write_text(ROOT / relative_path, text)


def _status_payload(manifest: dict[str, str]) -> dict[str, Any]:
    return {
        **manifest,
        "ready_scope": "DEVELOPMENT_RECONCILIATION_ONLY",
        "first_backtest_authorization_required": "YES",
        "readiness_gate_executed": "YES",
        "strategy_computation": "NO",
        "position_computation": "NO",
        "cost_computation": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
    }


def _render_readiness_ledger() -> str:
    rows = (
        ("evidence_completion_status", S09_MES_EVIDENCE_COMPLETION_LOCKED_STATUS, "LOCKED", "Evidence packet hash-bound on machinery-development slice."),
        ("evidence_handoff_status", S09_MES_EVIDENCE_COMPLETION_HANDOFF_STATUS, "LOCKED", "Handoff is readiness-gate only and not backtest authorization."),
        ("hash_bound_provenance_status", "LOCKED_SOURCE_NATIVE_HASH_BOUND_PROVENANCE", "LOCKED", "Evidence SHA256 manifest recomputed before readiness status write."),
        ("source_native_lane", "SOURCE_NATIVE_FUTURES", "LOCKED", "No CFD adapter or old QuantLab active pipeline used."),
        ("strategy_input_readiness_status", STRATEGY_INPUT_STATUS, "READY_DEV_RECON_ONLY", "Inputs are ready only for a separately authorized Development/Reconciliation backtest."),
        ("next_gate", NEXT_GATE, "AUTHORIZATION_REQUIRED", "Operator must separately authorize the first backtest."),
    )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(("check_name", "value", "status", "notes"))
    writer.writerows(rows)
    return buffer.getvalue()


def _render_provenance() -> str:
    return f"""# S09 MES Strategy Input Readiness Gate Provenance

Date: 2026-06-03

Status:

```text
{STATUS}
```

Scope:

- gate: {GATE}
- lane_class: SOURCE_NATIVE_FUTURES
- root: {ROOT_SYMBOL}
- row_id: {ROW_ID}
- machinery_development_slice: {MACHINERY_DEVELOPMENT_SLICE_TEXT}
- design_ordering: {DESIGN_ORDERING}

Inputs:

- evidence_status: `{EVIDENCE_STATUS_PATH.relative_to(ROOT).as_posix()}`
- evidence_hash_manifest: `{EVIDENCE_HASH_PATH.relative_to(ROOT).as_posix()}`
- evidence_handoff_status: {S09_MES_EVIDENCE_COMPLETION_HANDOFF_STATUS}

Next gate:

```text
{NEXT_GATE}
```

Boundary:

This readiness gate does not compute forecasts, run diagnostics, run a
backtest, access TEST, VALIDATION, Lockbox, Forward, stage Git, commit, push,
open a PR, deploy, trade, or promote.
"""


def _render_result() -> str:
    return f"""# S09 MES Strategy Input Readiness Gate Result

Date: 2026-06-03

Status:

```text
{STATUS}
```

Result:

- strategy_input_readiness_status: {STRATEGY_INPUT_STATUS}
- ready_scope: DEVELOPMENT_RECONCILIATION_ONLY
- first_backtest_authorization_required: YES
- next_gate: {NEXT_GATE}

Boundary:

No Databento API access, market-row parsing, forecast computation,
diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operations were
performed.
"""


def _render_local_audit() -> str:
    return f"""# S09 MES Strategy Input Readiness Gate Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_STRATEGY_INPUT_READINESS_GATE_NO_BACKTEST
```

Checks:

- locked evidence completion status is present
- remaining evidence count is zero
- hash-bound provenance is locked
- evidence SHA256 manifest recomputes before readiness write
- readiness handoff is readiness-gate only
- strategy input is marked ready only for Development/Reconciliation scope
- first backtest still requires separate operator authorization
- no forecasts, diagnostics, or backtests were run
- no TEST, VALIDATION, Lockbox, or Forward access occurred
- no Git staging, commit, push, PR, deployment, trading, or promotion occurred

This local audit must be reviewed by a spawned hostile-audit subagent.
"""


def _manifest_paths() -> tuple[Path, ...]:
    paths = (STATUS_PATH, LEDGER_PATH, PROVENANCE_PATH, RESULT_PATH, LOCAL_AUDIT_PATH)
    return tuple(sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()))


def _render_sha256_manifest(paths: tuple[Path, ...]) -> str:
    lines: list[str] = []
    seen: set[str] = set()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        if relative in seen:
            raise CarverBlocked("S09 MES readiness manifest paths must be unique")
        seen.add(relative)
        if "/hashes/" in relative or relative.endswith("_sha256.txt"):
            raise CarverBlocked("S09 MES readiness manifest must not hash hash files")
        lines.append(f"{_sha256(path)}  {relative}")
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CarverBlocked(f"S09 MES strategy-input readiness missing required JSON: {path}")
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

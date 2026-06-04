from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked  # noqa: E402

RUN_ID = "20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION"
GATE = "S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_TBBO_BOUNDED_ACQUISITION_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
SCHEMA = "tbbo"
STYPE_IN = "raw_symbol"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
WINDOW_START = date(2019, 5, 5)
WINDOW_END = date(2020, 4, 5)
REQUEST_END = date(2020, 4, 6)
WINDOW_LABEL = "2019-05-05_2020-04-05"
WINDOW_TEXT = "2019-05-05 through 2020-04-05"
RAW_SYMBOLS = ("MESM9", "MESU9", "MESZ9", "MESH0", "MESM0")
PROVIDER_QUALITY_WARNINGS = ("2020-02-27 degraded", "2020-02-28 degraded")
OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s09"
    / "mes_strategy_input_evidence_completion"
    / WINDOW_LABEL
    / "spread_slippage_tbbo_bounded_acquisition"
)
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_RESULT_2026-06-03.md"
AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)


@dataclass(frozen=True)
class S09MESSpreadSlippageTBBBOBoundedAcquisitionConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    schema: str
    raw_quote_download: bool
    spread_slippage_policy_lock: bool
    cost_ledger_rows: bool


def run_acquisition_guard(config: S09MESSpreadSlippageTBBBOBoundedAcquisitionConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES tbbo bounded acquisition is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES tbbo bounded acquisition is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES tbbo bounded acquisition is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES tbbo bounded acquisition is locked to the machinery-development slice")
    if config.schema != SCHEMA:
        raise CarverBlocked("S09 MES bounded raw quote acquisition is tbbo only")
    if not config.raw_quote_download:
        raise CarverBlocked("S09 MES tbbo bounded acquisition must explicitly download raw tbbo DBN")
    if config.spread_slippage_policy_lock:
        raise CarverBlocked("S09 MES tbbo acquisition must not lock spread/slippage policy")
    if config.cost_ledger_rows:
        raise CarverBlocked("S09 MES tbbo acquisition must not write cost ledger rows")
    return {
        "status": "AUTHORIZED_TBBO_BOUNDED_RAW_ACQUISITION_READY",
        "window_start": config.window_start,
        "window_end": config.window_end,
    }


def build_request_manifest_payload(config: S09MESSpreadSlippageTBBBOBoundedAcquisitionConfig) -> dict[str, Any]:
    run_acquisition_guard(config)
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "row_id": ROW_ID,
        "root": ROOT_SYMBOL,
        "window_role": "MACHINERY_DEVELOPMENT_SPREAD_SLIPPAGE_RAW_TBBO_ACQUISITION_NOT_COST_LOCK",
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "request_start": WINDOW_START.isoformat(),
        "request_end_exclusive": REQUEST_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "raw_quote_download": "YES_TBBO_ONLY",
        "mbp_1_download": "NO",
        "spread_slippage_policy_lock": "NO",
        "cost_ledger_rows": "NO",
        "cost_computation": "NO",
        "risk_adjusted_cost_computation": "NO",
        "speed_eligibility_computation": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
    }


def main() -> None:
    config = S09MESSpreadSlippageTBBBOBoundedAcquisitionConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        window_start=WINDOW_START.isoformat(),
        window_end=WINDOW_END.isoformat(),
        schema=SCHEMA,
        raw_quote_download=True,
        spread_slippage_policy_lock=False,
        cost_ledger_rows=False,
    )
    run_acquisition_guard(config)
    paths = _run_tbbo_acquisition(config)
    print("S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_RESULT_WRITTEN")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"artifacts={len(paths)}")


def _run_tbbo_acquisition(config: S09MESSpreadSlippageTBBBOBoundedAcquisitionConfig) -> tuple[Path, ...]:
    folders = _folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    client = db.Historical(_read_databento_key())
    written: list[Path] = []
    provider_errors: list[dict[str, Any]] = []
    raw_rows: list[dict[str, Any]] = []

    manifest_path = folders["manifest"] / f"{RUN_ID}_request_manifest.json"
    _write_json(manifest_path, build_request_manifest_payload(config))
    written.append(manifest_path)

    for raw_symbol in RAW_SYMBOLS:
        raw_dbn = folders["raw"] / f"{RUN_ID}_{raw_symbol}_{SCHEMA}.dbn"
        try:
            client.timeseries.get_range(
                dataset=DATASET,
                schema=SCHEMA,
                symbols=[raw_symbol],
                stype_in=STYPE_IN,
                start=WINDOW_START.isoformat(),
                end=REQUEST_END.isoformat(),
                path=raw_dbn,
            )
            if not raw_dbn.exists() or raw_dbn.stat().st_size <= 0:
                raise RuntimeError("Databento returned no raw tbbo DBN bytes")
            written.append(raw_dbn)
            raw_rows.append(_raw_receipt_row(raw_symbol, raw_dbn, "RAW_TBBO_DBN_ACQUIRED_NO_SPREAD_LOCK"))
        except Exception as exc:  # noqa: BLE001 - preserve provider failure without partial policy lock.
            provider_errors.append(
                {
                    "raw_symbol": raw_symbol,
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )
            if raw_dbn.exists() and raw_dbn.stat().st_size > 0:
                written.append(raw_dbn)
                raw_rows.append(_raw_receipt_row(raw_symbol, raw_dbn, "PARTIAL_RAW_TBBO_DBN_PRESENT_PROVIDER_ERROR"))

    receipt_csv = folders["raw"] / f"{RUN_ID}_raw_tbbo_receipt_ledger.csv"
    provider_errors_csv = folders["status"] / f"{RUN_ID}_provider_errors.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    provenance_md = folders["provenance"] / f"{RUN_ID}_provenance.md"
    _write_csv(receipt_csv, raw_rows)
    written.append(receipt_csv)
    if provider_errors:
        _write_csv(provider_errors_csv, provider_errors)
        written.append(provider_errors_csv)
    elif provider_errors_csv.exists():
        provider_errors_csv.unlink()

    status = _status_payload(raw_rows, provider_errors)
    _write_json(status_json, status)
    _write_text(provenance_md, _render_provenance(status, receipt_csv))
    _write_text(RESULT_PATH, _render_result(status, receipt_csv, status_json, provenance_md))
    _write_text(AUDIT_PATH, _render_audit(status_json, receipt_csv, provenance_md))
    written.extend([status_json, provenance_md, RESULT_PATH, AUDIT_PATH])

    hash_path = folders["hashes"] / f"{RUN_ID}_sha256.txt"
    _write_text(hash_path, _render_sha256_manifest(OUTPUT_ROOT, extra_paths=(RESULT_PATH, AUDIT_PATH)))
    written.append(hash_path)

    if provider_errors:
        raise SystemExit("FAIL_CLOSED provider errors preserved")
    return tuple(written)


def _raw_receipt_row(raw_symbol: str, raw_dbn: Path, status: str) -> dict[str, Any]:
    return {
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "stype_in": STYPE_IN,
        "raw_symbol": raw_symbol,
        "request_start": WINDOW_START.isoformat(),
        "request_end_exclusive": REQUEST_END.isoformat(),
        "raw_dbn_path": raw_dbn.relative_to(ROOT).as_posix(),
        "raw_dbn_size_bytes": raw_dbn.stat().st_size,
        "raw_dbn_sha256": _sha256(raw_dbn),
        "acquisition_status": status,
    }


def _status_payload(raw_rows: list[dict[str, Any]], provider_errors: list[dict[str, Any]]) -> dict[str, Any]:
    status = (
        "PASS_TBBO_BOUNDED_RAW_ACQUISITION_WITH_PROVIDER_DEGRADED_DAYS_NO_SPREAD_LOCK"
        if len(raw_rows) == len(RAW_SYMBOLS) and not provider_errors
        else "FAIL_CLOSED_TBBO_BOUNDED_RAW_ACQUISITION_INCOMPLETE_NO_SPREAD_LOCK"
    )
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": status,
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "raw_dbn_files": len(raw_rows),
        "raw_dbn_total_size_bytes": sum(int(row["raw_dbn_size_bytes"]) for row in raw_rows),
        "provider_errors": len(provider_errors),
        "provider_quality_warnings": list(PROVIDER_QUALITY_WARNINGS),
        "databento_api_access": "YES_OPERATOR_AUTHORIZED_TBBO_BOUNDED_RAW_ACQUISITION",
        "new_provider_data_download": "YES_TBBO_BOUNDED_RAW_DBN_ONLY",
        "raw_quote_download": "YES_TBBO_ONLY",
        "mbp_1_download": "NO",
        "spread_slippage_policy_lock": "NO",
        "cost_ledger_rows": "NO",
        "cost_computation": "NO",
        "risk_adjusted_cost_computation": "NO",
        "speed_eligibility_computation": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
    }


def _render_provenance(status: dict[str, Any], receipt_csv: Path) -> str:
    return f"""# S09 MES Spread Slippage TBBO Bounded Acquisition Provenance

Date: 2026-06-03

Status:

```text
{status["status"]}
```

Authorized scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- provider: {PROVIDER}
- dataset: {DATASET}
- schema: {SCHEMA}
- stype_in: {STYPE_IN}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- window: {WINDOW_TEXT}
- route: raw tbbo DBN acquisition only
- provider_quality_warnings: {"; ".join(PROVIDER_QUALITY_WARNINGS)}

Written receipt:

- `{receipt_csv.relative_to(ROOT).as_posix()}`

Boundary:

Raw TBBO DBN files were acquired for later source-native spread/slippage
extraction. No MBP-1 data was downloaded. No spread/slippage policy or value
was selected or locked. No cost ledger rows, cost computation, risk-adjusted
cost computation, speed eligibility computation, forecast computation,
diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operations were
performed.
"""


def _render_result(status: dict[str, Any], receipt_csv: Path, status_json: Path, provenance_md: Path) -> str:
    return f"""# S09 MES Spread Slippage TBBO Bounded Acquisition Result

Date: 2026-06-03

Status:

```text
{status["status"]}
```

Result:

Databento raw TBBO DBN data was requested for the authorized bounded
source-native spread/slippage route. This is a raw data acquisition, not a
spread/slippage value extraction and not a cost lock.

Scope:

- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- root: {ROOT_SYMBOL}
- dataset: {DATASET}
- schema: {SCHEMA}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- window: {WINDOW_TEXT}
- raw_dbn_files: {status["raw_dbn_files"]}
- raw_dbn_total_size_bytes: {status["raw_dbn_total_size_bytes"]}
- provider_quality_warnings: {"; ".join(PROVIDER_QUALITY_WARNINGS)}

Written artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{receipt_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Next decision:

Authorize source-native extraction from the acquired TBBO files to produce a
predeclared spread/slippage policy or keep spread/slippage fail-closed. Any
extraction must explicitly account for the degraded provider days listed above.

Boundary:

No MBP-1 data, spread/slippage value lock, cost ledger rows, cost computation,
diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operations were
performed.
"""


def _render_audit(status_json: Path, receipt_csv: Path, provenance_md: Path) -> str:
    return f"""# S09 MES Spread Slippage TBBO Bounded Acquisition Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_TBBO_BOUNDED_RAW_ACQUISITION_NO_SPREAD_LOCK
```

Observed artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{receipt_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Checks:

- lane remains {LANE_CLASS}
- dataset remains {DATASET}
- schema is limited to {SCHEMA}
- raw symbols are limited to {", ".join(RAW_SYMBOLS)}
- window remains {WINDOW_TEXT}
- no MBP-1 data
- no spread/slippage policy lock
- no cost ledger rows
- no forecast, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, or Git operations
"""


def _folders(root: Path) -> dict[str, Path]:
    return {
        "manifest": root / "manifest",
        "raw": root / "raw_provider_output",
        "status": root / "status",
        "provenance": root / "provenance",
        "hashes": root / "hashes",
    }


def _read_databento_key() -> str:
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if env_key.startswith("db-"):
        return env_key
    for path in KEY_CANDIDATES:
        if path is None or not path.exists():
            continue
        key = path.read_text(encoding="utf-8").strip()
        if key.startswith("db-"):
            return key
    raise SystemExit("Fail closed: no valid-shaped Databento key found")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _render_sha256_manifest(root: Path, *, extra_paths: tuple[Path, ...]) -> str:
    paths = [path for path in sorted(root.rglob("*")) if path.is_file() and not path.name.endswith("_sha256.txt")]
    paths.extend(extra_paths)
    lines = []
    for path in sorted(set(paths), key=lambda item: item.relative_to(ROOT).as_posix()):
        lines.append(f"{_sha256(path)}  {path.relative_to(ROOT).as_posix()}")
    return "\n".join(lines) + "\n"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


if __name__ == "__main__":
    main()

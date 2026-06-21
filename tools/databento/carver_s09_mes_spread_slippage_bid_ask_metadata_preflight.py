from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked  # noqa: E402

RUN_ID = "20260603_S09_MES_SPREAD_SLIPPAGE_BID_ASK_METADATA_PREFLIGHT"
GATE = "S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_HISTORICAL_BID_ASK_DATA_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
STYPE_IN = "raw_symbol"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
WINDOW_START = date(2019, 5, 5)
WINDOW_END = date(2020, 4, 5)
REQUEST_END = date(2020, 4, 6)
WINDOW_LABEL = "2019-05-05_2020-04-05"
WINDOW_TEXT = "2019-05-05 through 2020-04-05"
RAW_SYMBOLS = ("MESM9", "MESU9", "MESZ9", "MESH0", "MESM0")
ALLOWED_SCHEMAS = ("mbp-1", "tbbo")
OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s09"
    / "mes_strategy_input_evidence_completion"
    / WINDOW_LABEL
    / "spread_slippage_bid_ask_metadata_preflight"
)
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_SPREAD_SLIPPAGE_BID_ASK_METADATA_PREFLIGHT_RESULT_2026-06-03.md"
AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_SPREAD_SLIPPAGE_BID_ASK_METADATA_PREFLIGHT_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)


@dataclass(frozen=True)
class S09MESSpreadSlippageBidAskMetadataPreflightConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str
    metadata_only: bool
    raw_quote_download: bool
    schemas: tuple[str, ...]


def run_preflight_guard(config: S09MESSpreadSlippageBidAskMetadataPreflightConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES spread/slippage bid/ask metadata preflight is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES spread/slippage bid/ask route is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES spread/slippage bid/ask route is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES spread/slippage bid/ask route is locked to the machinery-development slice")
    if not config.metadata_only:
        raise CarverBlocked("S09 MES spread/slippage preflight allows metadata estimation only")
    if config.raw_quote_download:
        raise CarverBlocked("S09 MES spread/slippage preflight must not download raw bid/ask records")
    if tuple(config.schemas) != ALLOWED_SCHEMAS:
        raise CarverBlocked("S09 MES spread/slippage preflight must estimate mbp-1 and tbbo only")
    return {
        "status": "AUTHORIZED_METADATA_PREFLIGHT_ONLY_READY",
        "window_start": config.window_start,
        "window_end": config.window_end,
    }


def build_request_manifest_payload(config: S09MESSpreadSlippageBidAskMetadataPreflightConfig) -> dict[str, Any]:
    run_preflight_guard(config)
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schemas": list(config.schemas),
        "stype_in": STYPE_IN,
        "row_id": ROW_ID,
        "root": ROOT_SYMBOL,
        "window_role": "MACHINERY_DEVELOPMENT_SPREAD_SLIPPAGE_SOURCE_PREFLIGHT_NOT_COST_LOCK",
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "request_start": WINDOW_START.isoformat(),
        "request_end_exclusive": REQUEST_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "metadata_only": "YES",
        "raw_quote_download": "NO",
        "spread_slippage_policy_lock": "NO",
        "cost_ledger_rows": "NO",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
    }


def main() -> None:
    config = S09MESSpreadSlippageBidAskMetadataPreflightConfig(
        execution_authorized=True,
        lane_class=LANE_CLASS,
        root=ROOT_SYMBOL,
        row_id=ROW_ID,
        window_start=WINDOW_START.isoformat(),
        window_end=WINDOW_END.isoformat(),
        metadata_only=True,
        raw_quote_download=False,
        schemas=ALLOWED_SCHEMAS,
    )
    run_preflight_guard(config)
    paths = _run_metadata_preflight(config)
    print("S09_MES_SPREAD_SLIPPAGE_BID_ASK_METADATA_PREFLIGHT_RESULT_WRITTEN")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"artifacts={len(paths)}")


def _run_metadata_preflight(config: S09MESSpreadSlippageBidAskMetadataPreflightConfig) -> tuple[Path, ...]:
    folders = _folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    client = db.Historical(_read_databento_key())
    written: list[Path] = []
    provider_errors: list[dict[str, Any]] = []

    manifest_path = folders["manifest"] / f"{RUN_ID}_request_manifest.json"
    _write_json(manifest_path, build_request_manifest_payload(config))
    written.append(manifest_path)

    rows: list[dict[str, Any]] = []
    for schema in config.schemas:
        try:
            rows.append(_estimate_schema(client, schema))
        except Exception as exc:  # noqa: BLE001 - preserve provider/API failure without falling through to download.
            provider_errors.append(
                {
                    "schema": schema,
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )

    estimate_csv = folders["metadata"] / f"{RUN_ID}_cost_record_estimates.csv"
    provider_errors_csv = folders["status"] / f"{RUN_ID}_provider_errors.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    provenance_md = folders["provenance"] / f"{RUN_ID}_provenance.md"
    _write_csv(estimate_csv, rows)
    written.append(estimate_csv)
    if provider_errors:
        _write_csv(provider_errors_csv, provider_errors)
        written.append(provider_errors_csv)
    elif provider_errors_csv.exists():
        provider_errors_csv.unlink()

    status = _status_payload(rows, provider_errors)
    _write_json(status_json, status)
    _write_text(provenance_md, _render_provenance(status, estimate_csv))
    _write_text(RESULT_PATH, _render_result(status, estimate_csv, status_json, provenance_md))
    _write_text(AUDIT_PATH, _render_audit(status_json, estimate_csv, provenance_md))
    written.extend([status_json, provenance_md, RESULT_PATH, AUDIT_PATH])

    hash_path = folders["hashes"] / f"{RUN_ID}_sha256.txt"
    _write_text(hash_path, _render_sha256_manifest(OUTPUT_ROOT, extra_paths=(RESULT_PATH, AUDIT_PATH)))
    written.append(hash_path)
    return tuple(written)


def _estimate_schema(client: db.Historical, schema: str) -> dict[str, Any]:
    record_count = client.metadata.get_record_count(
        dataset=DATASET,
        symbols=list(RAW_SYMBOLS),
        schema=schema,
        stype_in=STYPE_IN,
        start=WINDOW_START.isoformat(),
        end=REQUEST_END.isoformat(),
    )
    estimated_cost_usd = client.metadata.get_cost(
        dataset=DATASET,
        symbols=list(RAW_SYMBOLS),
        schema=schema,
        stype_in=STYPE_IN,
        start=WINDOW_START.isoformat(),
        end=REQUEST_END.isoformat(),
    )
    return {
        "dataset": DATASET,
        "schema": schema,
        "stype_in": STYPE_IN,
        "raw_symbols": " ".join(RAW_SYMBOLS),
        "request_start": WINDOW_START.isoformat(),
        "request_end_exclusive": REQUEST_END.isoformat(),
        "record_count": int(record_count),
        "estimated_cost_usd": float(estimated_cost_usd),
        "metadata_status": "METADATA_ESTIMATE_RETURNED_NO_RAW_QUOTE_DOWNLOAD",
    }


def _status_payload(rows: list[dict[str, Any]], provider_errors: list[dict[str, Any]]) -> dict[str, Any]:
    status = (
        "PASS_METADATA_PREFLIGHT_ESTIMATED_NO_RAW_BID_ASK_DOWNLOAD"
        if rows and not provider_errors
        else "FAIL_CLOSED_METADATA_PREFLIGHT_NO_BID_ASK_DOWNLOAD"
    )
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": status,
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schemas": list(ALLOWED_SCHEMAS),
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "estimate_rows": len(rows),
        "provider_errors": len(provider_errors),
        "databento_api_access": "YES_OPERATOR_AUTHORIZED_METADATA_COST_RECORD_PREFLIGHT_ONLY",
        "new_provider_data_download": "NO",
        "raw_quote_download": "NO",
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


def _render_provenance(status: dict[str, Any], estimate_csv: Path) -> str:
    return f"""# S09 MES Spread Slippage Bid Ask Metadata Preflight Provenance

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
- schemas: {", ".join(ALLOWED_SCHEMAS)}
- stype_in: {STYPE_IN}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- window: {WINDOW_TEXT}
- route: metadata get_record_count and get_cost only

Written data:

- `{estimate_csv.relative_to(ROOT).as_posix()}`

Boundary:

No raw bid/ask records were downloaded. No spread/slippage policy was selected
or locked. No cost ledger rows, cost computation, risk-adjusted cost
computation, speed eligibility computation, forecast computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
"""


def _render_result(status: dict[str, Any], estimate_csv: Path, status_json: Path, provenance_md: Path) -> str:
    return f"""# S09 MES Spread Slippage Bid Ask Metadata Preflight Result

Date: 2026-06-03

Status:

```text
{status["status"]}
```

Result:

Databento metadata cost and record-count estimates were requested for the
authorized historical bid/ask route only. This is not a raw quote download and
not a spread/slippage cost lock.

Scope:

- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- root: {ROOT_SYMBOL}
- dataset: {DATASET}
- schemas: {", ".join(ALLOWED_SCHEMAS)}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- window: {WINDOW_TEXT}

Written artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{estimate_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Next decision:

Use the metadata estimates to choose between a bounded sampled bid/ask request,
a smaller pilot day request, or keeping spread/slippage fail-closed.

Boundary:

No raw bid/ask records, cost ledger rows, cost computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
"""


def _render_audit(status_json: Path, estimate_csv: Path, provenance_md: Path) -> str:
    return f"""# S09 MES Spread Slippage Bid Ask Metadata Preflight Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_METADATA_PREFLIGHT_ONLY_NO_RAW_BID_ASK_DOWNLOAD
```

Observed artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{estimate_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Checks:

- lane remains {LANE_CLASS}
- dataset remains {DATASET}
- schemas are limited to {", ".join(ALLOWED_SCHEMAS)}
- raw symbols are limited to {", ".join(RAW_SYMBOLS)}
- window remains {WINDOW_TEXT}
- metadata API access only
- no raw bid/ask download
- no spread/slippage policy lock
- no cost ledger rows
- no forecast, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, or Git operations
"""


def _folders(root: Path) -> dict[str, Path]:
    return {
        "manifest": root / "manifest",
        "metadata": root / "metadata",
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

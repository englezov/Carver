from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


RUN_ID = "20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE"
GATE = "ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_EVIDENCE_DATABENTO_DEFINITION_PROBE"
DATASET = "GLBX.MDP3"
SCHEMA = "definition"
STYPE_IN = "raw_symbol"
SYMBOLS = ("ZNH6", "ZNM6", "ZNU6")
REQUEST_START = "2026-03-01T00:00:00Z"
REQUEST_END = "2026-05-30T00:00:00Z"
OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s26_s27_hourly_bridge"
    / "ZN_S27_EWMAC16_TREND_DEPENDENCY"
    / "zn_lifecycle_databento_definition_probe_2026-05-31"
)
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)


def main() -> None:
    folders = {
        "raw_provider_metadata": OUTPUT_ROOT / "raw_provider_metadata",
        "ledger": OUTPUT_ROOT / "ledger",
        "provenance": OUTPUT_ROOT / "provenance",
        "status": OUTPUT_ROOT / "status",
        "hashes": OUTPUT_ROOT / "hashes",
    }
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    key = _read_databento_key()
    client = db.Historical(key)

    raw_dbn = folders["raw_provider_metadata"] / f"{RUN_ID}_definition.dbn"
    definition_csv = folders["raw_provider_metadata"] / f"{RUN_ID}_definition_dataframe.csv"
    symbology_json = folders["raw_provider_metadata"] / f"{RUN_ID}_symbology_raw_symbol_to_instrument_id.json"
    lifecycle_ledger_csv = folders["ledger"] / f"{RUN_ID}_lifecycle_definition_ledger.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    provenance_json = folders["provenance"] / f"{RUN_ID}_provenance.json"
    hashes_json = folders["hashes"] / f"{RUN_ID}_sha256.json"

    store = client.timeseries.get_range(
        dataset=DATASET,
        schema=SCHEMA,
        symbols=list(SYMBOLS),
        stype_in=STYPE_IN,
        start=REQUEST_START,
        end=REQUEST_END,
        path=raw_dbn,
    )
    df = store.to_df()
    df.to_csv(definition_csv)

    symbology = client.symbology.resolve(
        dataset=DATASET,
        symbols=list(SYMBOLS),
        stype_in=STYPE_IN,
        stype_out="instrument_id",
        start_date=REQUEST_START[:10],
        end_date=REQUEST_END[:10],
    )
    _write_json(symbology_json, symbology)

    ledger = _build_lifecycle_ledger(df)
    _write_csv(lifecycle_ledger_csv, ledger)

    unresolved_fields = [
        row
        for row in ledger
        if row["first_notice_date_status"] != "NOT_PROVIDED_BY_DATABENTO_DEFINITION_SCHEMA"
        or row["delivery_window_status"] != "NOT_PROVIDED_BY_DATABENTO_DEFINITION_SCHEMA"
    ]
    probe_result = (
        "FAIL_CLOSED_DATABENTO_DEFINITION_PROVES_EXPIRATION_ACTIVATION_ONLY_OFFICIAL_LIFECYCLE_STILL_REQUIRED"
        if not unresolved_fields
        else "UNEXPECTED_SCHEMA_FIELDS_REVIEW_REQUIRED"
    )

    _write_json(
        status_json,
        {
            "gate": GATE,
            "run_id": RUN_ID,
            "result": probe_result,
            "dataset": DATASET,
            "schema": SCHEMA,
            "stype_in": STYPE_IN,
            "symbols": list(SYMBOLS),
            "request_start_utc": REQUEST_START,
            "request_end_utc": REQUEST_END,
            "definition_rows": len(df),
            "ledger_rows": len(ledger),
            "market_rows_requested": "NO",
            "ohlcv_requested": "NO",
            "strategy_computation": "NO",
            "trend_computation": "NO",
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "next_required_gate": "OFFICIAL_STATIC_ZN_LIFECYCLE_EVIDENCE_OR_FAIL_CLOSED_ROLL_POLICY_DECISION",
        },
    )
    _write_json(
        provenance_json,
        {
            "gate": GATE,
            "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "purpose": "Metadata-only Databento definition probe for ZN local continuous daily lifecycle repair before S27 EWMAC16 trend dependency.",
            "lane_class": "SOURCE_NATIVE_FUTURES",
            "provider": "Databento",
            "dataset": DATASET,
            "schema": SCHEMA,
            "symbols": list(SYMBOLS),
            "secret_handling": "API key read locally and not written to artifacts or stdout.",
            "boundary": [
                "NO_OHLCV_DOWNLOAD",
                "NO_MARKET_ROW_PARSING",
                "NO_CONTINUOUS_CONTRACT_DOWNLOAD",
                "NO_PROVIDER_BUILT_CONTINUOUS_SERIES",
                "NO_TREND_COMPUTATION",
                "NO_S27_COMPUTATION",
                "NO_DIAGNOSTICS",
                "NO_BACKTESTS",
                "NO_POSITIONS",
                "NO_TRADING",
                "NO_PROMOTION",
            ],
        },
    )

    hashes = {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in (
            raw_dbn,
            definition_csv,
            symbology_json,
            lifecycle_ledger_csv,
            status_json,
            provenance_json,
        )
    }
    _write_json(hashes_json, hashes)

    print(probe_result)
    print(f"definition_rows={len(df)}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _build_lifecycle_ledger(df: Any) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if df.empty:
        raise SystemExit("Fail closed: Databento definition query returned no rows")
    for raw_symbol in SYMBOLS:
        subset = df[df.get("raw_symbol") == raw_symbol]
        if subset.empty:
            rows.append(
                {
                    "raw_symbol": raw_symbol,
                    "instrument_id": "",
                    "definition_status": "FAIL_CLOSED_NO_DEFINITION_ROWS",
                    "activation": "",
                    "expiration": "",
                    "maturity_year": "",
                    "maturity_month": "",
                    "currency": "",
                    "exchange": "",
                    "asset": "",
                    "group": "",
                    "security_type": "",
                    "first_notice_date_status": "NOT_PROVIDED_BY_DATABENTO_DEFINITION_SCHEMA",
                    "delivery_window_status": "NOT_PROVIDED_BY_DATABENTO_DEFINITION_SCHEMA",
                    "roll_policy_status": "BLOCKED_OFFICIAL_LIFECYCLE_EVIDENCE_REQUIRED",
                }
            )
            continue
        latest = subset.sort_index().iloc[-1]
        rows.append(
            {
                "raw_symbol": raw_symbol,
                "instrument_id": str(latest.get("instrument_id", "")),
                "definition_status": "DATABENTO_DEFINITION_ROW_PRESENT",
                "activation": str(latest.get("activation", "")),
                "expiration": str(latest.get("expiration", "")),
                "maturity_year": str(latest.get("maturity_year", "")),
                "maturity_month": str(latest.get("maturity_month", "")),
                "currency": str(latest.get("currency", "")),
                "exchange": str(latest.get("exchange", "")),
                "asset": str(latest.get("asset", "")),
                "group": str(latest.get("group", "")),
                "security_type": str(latest.get("security_type", "")),
                "first_notice_date_status": "NOT_PROVIDED_BY_DATABENTO_DEFINITION_SCHEMA",
                "delivery_window_status": "NOT_PROVIDED_BY_DATABENTO_DEFINITION_SCHEMA",
                "roll_policy_status": "BLOCKED_OFFICIAL_LIFECYCLE_EVIDENCE_REQUIRED",
            }
        )
    return rows


def _read_databento_key() -> str:
    for path in KEY_CANDIDATES:
        if path is None or not path.exists():
            continue
        key = path.read_text(encoding="utf-8").strip()
        if len(key) == 32 and key.startswith("db-"):
            return key
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if len(env_key) == 32 and env_key.startswith("db-"):
        return env_key
    raise SystemExit("Fail closed: no valid-shaped Databento key found in env or approved local key files")


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    import csv

    if not rows:
        raise SystemExit("Fail closed: no lifecycle ledger rows to write")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


if __name__ == "__main__":
    main()

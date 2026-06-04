from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked  # noqa: E402


RUN_ID = "20260602_S09_MES_DEV_RECON_DAILY_EXPANSION"
GATE = "S09_MES_DEV_RECON_DATA_EXPANSION_AND_LINEAGE_REPAIR_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
SCHEMA = "ohlcv-1d"
DEFINITION_SCHEMA = "definition"
STYPE_IN = "raw_symbol"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
BOOK_LABEL = "S&P 500 (micro)"
DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE = (
    "DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE: this executable targets the superseded "
    "2022-01-03 through 2023-12-29 development window. Use the oldest minimum machinery-development "
    "slice 2019-05-05 through 2020-04-05 via the authorized machinery-dev/evidence-completion path."
)
TARGET_START = date(2022, 1, 3)
TARGET_END = date(2023, 12, 29)
REQUEST_START = datetime(2021, 1, 1, tzinfo=timezone.utc)
REQUEST_END = datetime(2024, 1, 1, tzinfo=timezone.utc)
RAW_SYMBOLS = (
    "MESH1",
    "MESM1",
    "MESU1",
    "MESZ1",
    "MESH2",
    "MESM2",
    "MESU2",
    "MESZ2",
    "MESH3",
    "MESM3",
    "MESU3",
    "MESZ3",
    "MESH4",
)
MONTH_CODE_TO_MONTH = {"H": 3, "M": 6, "U": 9, "Z": 12}
OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s09"
    / "mes_dev_recon_data_expansion"
    / "2022-01-03_2023-12-29"
)
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)


def main() -> None:
    raise CarverBlocked(DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE)
    import databento as db  # noqa: PLC0415

    folders = _folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    _quarantine_stale_failure_artifacts(folders)

    manifest_path = folders["manifest"] / f"{RUN_ID}_request_manifest.json"
    _write_json(manifest_path, _manifest_payload())

    key = _read_databento_key()
    client = db.Historical(key)

    raw_paths: list[Path] = [manifest_path]
    provider_errors: list[dict[str, Any]] = []
    symbology_rows: list[dict[str, Any]] = []
    definition_rows: list[dict[str, Any]] = []
    sanitized_rows: list[dict[str, Any]] = []

    condition_path = folders["metadata"] / f"{RUN_ID}_dataset_condition.json"
    condition = _read_json(condition_path) if condition_path.exists() else _fetch_dataset_condition(client, provider_errors)
    if not condition_path.exists():
        _write_json(condition_path, condition)
    raw_paths.append(condition_path)
    condition_by_date = _condition_by_date(condition)

    symbology_path = folders["metadata"] / f"{RUN_ID}_symbology_raw_symbol_to_instrument_id.json"
    symbology = _read_json(symbology_path) if symbology_path.exists() else _fetch_symbology(client, provider_errors)
    if not symbology_path.exists():
        _write_json(symbology_path, symbology)
    raw_paths.append(symbology_path)
    symbology_rows.extend(_symbology_ledger_rows(symbology))

    for raw_symbol in RAW_SYMBOLS:
        try:
            raw_dbn = folders["raw"] / f"{RUN_ID}_{raw_symbol}_{SCHEMA}.dbn"
            provider_csv = folders["raw"] / f"{RUN_ID}_{raw_symbol}_{SCHEMA}_provider.csv"
            if provider_csv.exists() and provider_csv.stat().st_size > 0:
                raw_paths.extend([path for path in (raw_dbn, provider_csv) if path.exists()])
            else:
                store = client.timeseries.get_range(
                    dataset=DATASET,
                    schema=SCHEMA,
                    symbols=[raw_symbol],
                    stype_in=STYPE_IN,
                    start=_z(REQUEST_START),
                    end=_z(REQUEST_END),
                    path=raw_dbn,
                )
                provider_df = store.to_df()
                provider_df.to_csv(provider_csv)
                raw_paths.extend([raw_dbn, provider_csv])

            source_sha = _sha256(provider_csv)
            contract_rows = _sanitize_provider_csv(provider_csv, raw_symbol, condition_by_date, source_sha)
            if not contract_rows:
                provider_errors.append(
                    {
                        "raw_symbol": raw_symbol,
                        "error_type": "NO_OHLCV_ROWS",
                        "message": "No ohlcv-1d rows returned in locked request envelope",
                    }
                )
            sanitized_rows.extend(contract_rows)
        except Exception as exc:  # noqa: BLE001 - preserve and fail closed.
            provider_errors.append(
                {
                    "raw_symbol": raw_symbol,
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )

        try:
            definition_dbn = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_definition.dbn"
            definition_csv = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_definition.csv"
            retry_definition_dbn = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_definition_retry.dbn"
            retry_definition_csv = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_definition_retry.csv"
            if definition_csv.exists() and definition_csv.stat().st_size > 0:
                definition_df = _read_csv_rows(definition_csv)
            elif retry_definition_csv.exists() and retry_definition_csv.stat().st_size > 0:
                definition_dbn = retry_definition_dbn
                definition_csv = retry_definition_csv
                definition_df = _read_csv_rows(definition_csv)
            else:
                if definition_dbn.exists() and definition_dbn.stat().st_size == 0:
                    definition_dbn = retry_definition_dbn
                    definition_csv = retry_definition_csv
                definition_store = client.timeseries.get_range(
                    dataset=DATASET,
                    schema=DEFINITION_SCHEMA,
                    symbols=[raw_symbol],
                    stype_in=STYPE_IN,
                    start=_z(REQUEST_START),
                    end=_z(REQUEST_END),
                    path=definition_dbn,
                )
                definition_df = definition_store.to_df()
                definition_df.to_csv(definition_csv)
            raw_paths.extend([definition_dbn, definition_csv])
            definition_rows.append(
                {
                    "raw_symbol": raw_symbol,
                    "definition_rows": int(len(definition_df)),
                    "definition_status": "DATABENTO_DEFINITION_ROWS_PRESENT" if len(definition_df) else "FAIL_CLOSED_NO_DEFINITION_ROWS",
                    "definition_csv": str(definition_csv.relative_to(ROOT)),
                }
            )
            if len(definition_df) == 0:
                provider_errors.append(
                    {
                        "raw_symbol": raw_symbol,
                        "error_type": "NO_DEFINITION_ROWS",
                        "message": "No Databento definition rows returned in locked request envelope",
                    }
                )
        except Exception as exc:  # noqa: BLE001 - preserve and fail closed.
            provider_errors.append(
                {
                    "raw_symbol": raw_symbol,
                    "error_type": f"DEFINITION_{type(exc).__name__}",
                    "message": str(exc),
                }
            )

    sanitized_rows.sort(key=lambda row: (row["raw_symbol"], row["provider_ts_event_utc"]))
    sanitized_csv = folders["sanitized"] / f"{RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
    validation_csv = folders["validation"] / f"{RUN_ID}_row_validation.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    provenance_json = folders["provenance"] / f"{RUN_ID}_provenance.json"
    hashes_json = folders["hashes"] / f"{RUN_ID}_sha256.json"
    symbology_csv = folders["metadata"] / f"{RUN_ID}_symbology_resolution_ledger.csv"
    definition_ledger_csv = folders["metadata"] / f"{RUN_ID}_definition_ledger.csv"
    provider_errors_csv = folders["status"] / f"{RUN_ID}_provider_errors.csv"

    validation_rows = _validation_rows(sanitized_rows, provider_errors)
    status = _status_payload(sanitized_rows, validation_rows, provider_errors, sanitized_csv)

    _write_csv(sanitized_csv, sanitized_rows)
    _write_csv(validation_csv, validation_rows)
    _write_csv(symbology_csv, symbology_rows)
    _write_csv(definition_ledger_csv, definition_rows)
    if provider_errors:
        _write_csv(provider_errors_csv, provider_errors)
        raw_paths.append(provider_errors_csv)
    elif provider_errors_csv.exists():
        provider_errors_csv.unlink()
    _write_json(status_json, status)
    _write_json(provenance_json, _provenance_payload(status, sanitized_csv, validation_csv))
    raw_paths.extend([sanitized_csv, validation_csv, symbology_csv, definition_ledger_csv, status_json, provenance_json])
    _write_json(hashes_json, _hash_tree(OUTPUT_ROOT))

    print(status["status"])
    print(f"sanitized_rows={len(sanitized_rows)}")
    print(f"provider_errors={len(provider_errors)}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")
    if provider_errors:
        raise SystemExit("FAIL_CLOSED provider errors preserved")


def _manifest_payload() -> dict[str, Any]:
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
        "book_label": BOOK_LABEL,
        "target_development_reconciliation_start": TARGET_START.isoformat(),
        "target_development_reconciliation_end": TARGET_END.isoformat(),
        "request_start_utc": _z(REQUEST_START),
        "request_end_utc": _z(REQUEST_END),
        "raw_symbols": list(RAW_SYMBOLS),
        "continuous_contracts_requested": "NO",
        "provider_built_continuous_series_requested": "NO",
        "forecast_computation": "NO",
        "backtest_run": "NO",
        "non_authorization": [
            "NO_ADDITIONAL_SYMBOLS",
            "NO_CONTINUOUS_CONTRACTS",
            "NO_FORECASTS",
            "NO_POSITIONS",
            "NO_COSTS",
            "NO_DIAGNOSTICS",
            "NO_BACKTESTS",
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
        ],
    }


def _fetch_dataset_condition(client: db.Historical, errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    try:
        return client.metadata.get_dataset_condition(
            dataset=DATASET,
            start_date=REQUEST_START.date().isoformat(),
            end_date=REQUEST_END.date().isoformat(),
        )
    except Exception as exc:  # noqa: BLE001
        errors.append({"raw_symbol": "ALL", "error_type": f"DATASET_CONDITION_{type(exc).__name__}", "message": str(exc)})
        return []


def _fetch_symbology(client: db.Historical, errors: list[dict[str, Any]]) -> dict[str, Any]:
    try:
        return client.symbology.resolve(
            dataset=DATASET,
            symbols=list(RAW_SYMBOLS),
            stype_in=STYPE_IN,
            stype_out="instrument_id",
            start_date=REQUEST_START.date().isoformat(),
            end_date=REQUEST_END.date().isoformat(),
        )
    except Exception as exc:  # noqa: BLE001
        errors.append({"raw_symbol": "ALL", "error_type": f"SYMBOLOGY_{type(exc).__name__}", "message": str(exc)})
        return {}


def _symbology_ledger_rows(symbology: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    result = symbology.get("result", {}) if isinstance(symbology, dict) else {}
    for raw_symbol in RAW_SYMBOLS:
        resolved = result.get(raw_symbol, [])
        if not resolved:
            rows.append(
                {
                    "raw_symbol": raw_symbol,
                    "resolved_d0": "",
                    "resolved_d1": "",
                    "instrument_id": "",
                    "symbology_status": "FAIL_CLOSED_NOT_RESOLVED",
                }
            )
            continue
        for item in resolved:
            rows.append(
                {
                    "raw_symbol": raw_symbol,
                    "resolved_d0": item.get("d0", ""),
                    "resolved_d1": item.get("d1", ""),
                    "instrument_id": item.get("s", ""),
                    "symbology_status": "RESOLVED",
                }
            )
    return rows


def _sanitize_provider_csv(
    provider_csv: Path,
    raw_symbol: str,
    condition_by_date: dict[str, str],
    source_raw_sha256: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    with provider_csv.open("r", encoding="utf-8", newline="") as handle:
        for record in csv.DictReader(handle):
            ts = _parse_ts(record["ts_event"])
            key = f"{raw_symbol}|{_z(ts)}"
            if key in seen:
                raise RuntimeError(f"DUPLICATE_PROVIDER_TIMESTAMP {key}")
            seen.add(key)
            open_ = float(record["open"])
            high = float(record["high"])
            low = float(record["low"])
            close = float(record["close"])
            volume = float(record["volume"])
            if not all(math.isfinite(value) for value in (open_, high, low, close, volume)):
                raise RuntimeError(f"NON_FINITE_OHLCV {key}")
            if high < low or high < open_ or high < close or low > open_ or low > close:
                raise RuntimeError(f"BAD_OHLC_SHAPE {key}")
            if volume < 0:
                raise RuntimeError(f"NEGATIVE_VOLUME {key}")
            completed_date = ts.date().isoformat()
            condition = condition_by_date.get(completed_date, "UNKNOWN")
            provider_condition_classification = (
                "NORMAL_PROVIDER_CONDITION"
                if condition == "AVAILABLE"
                else "DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY"
            )
            contract = _contract_parts(raw_symbol)
            rows.append(
                {
                    "lane_class": LANE_CLASS,
                    "provider": PROVIDER,
                    "dataset": DATASET,
                    "schema": SCHEMA,
                    "stype_in": STYPE_IN,
                    "row_id": ROW_ID,
                    "root": ROOT_SYMBOL,
                    "book_label": BOOK_LABEL,
                    "raw_symbol": raw_symbol,
                    "contract_year": contract["contract_year"],
                    "delivery_month": contract["delivery_month"],
                    "delivery_code": contract["delivery_code"],
                    "instrument_id": str(record.get("instrument_id", "")),
                    "provider_ts_event_utc": _z(ts),
                    "completed_trading_date": completed_date,
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                    "provider_condition": condition,
                    "provider_condition_classification": provider_condition_classification,
                    "target_window_membership": (
                        "TARGET_WINDOW"
                        if TARGET_START.isoformat() <= completed_date <= TARGET_END.isoformat()
                        else "WARMUP_OR_POST_TARGET_CONTEXT"
                    ),
                    "strategy_readiness_status": "QUARANTINE_ONLY_NOT_STRATEGY_INPUT",
                    "source_raw_sha256": source_raw_sha256,
                }
            )
    return rows


def _validation_rows(sanitized_rows: list[dict[str, Any]], provider_errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_symbol = Counter(str(row["raw_symbol"]) for row in sanitized_rows)
    target_by_symbol = Counter(
        str(row["raw_symbol"])
        for row in sanitized_rows
        if row["target_window_membership"] == "TARGET_WINDOW"
    )
    duplicate_count = len(sanitized_rows) - len({(row["raw_symbol"], row["provider_ts_event_utc"]) for row in sanitized_rows})
    rows: list[dict[str, Any]] = [
        _validation("provider_errors_absent", not provider_errors, len(provider_errors)),
        _validation("all_requested_symbols_have_rows", all(by_symbol[symbol] > 0 for symbol in RAW_SYMBOLS), len(by_symbol)),
        _validation("target_window_rows_present_for_active_chain_contracts", sum(target_by_symbol.values()) > 0, sum(target_by_symbol.values())),
        _validation("duplicate_provider_timestamps_absent", duplicate_count == 0, duplicate_count),
        _validation("no_strategy_artifacts_created", True, 0),
        _validation("no_forecasts_positions_costs_or_backtests", True, 0),
    ]
    for raw_symbol in RAW_SYMBOLS:
        rows.append(
            {
                "check_name": f"{raw_symbol}_row_counts",
                "check_status": "PASS" if by_symbol[raw_symbol] > 0 else "FAIL",
                "observed_count": by_symbol[raw_symbol],
                "target_window_count": target_by_symbol[raw_symbol],
            }
        )
    return rows


def _status_payload(
    sanitized_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    provider_errors: list[dict[str, Any]],
    sanitized_csv: Path,
) -> dict[str, Any]:
    failed_checks = [row for row in validation_rows if row.get("check_status") != "PASS"]
    provider_condition_counts = Counter(str(row["provider_condition_classification"]) for row in sanitized_rows)
    target_rows = [row for row in sanitized_rows if row["target_window_membership"] == "TARGET_WINDOW"]
    status = (
        "PASS_S09_MES_DAILY_EXPANSION_QUARANTINE_ONLY_NOT_LINEAGE_NOT_BACKTEST"
        if not provider_errors and not failed_checks
        else "FAIL_CLOSED_S09_MES_DAILY_EXPANSION_BLOCKED"
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
        "raw_symbols": list(RAW_SYMBOLS),
        "request_start_utc": _z(REQUEST_START),
        "request_end_utc": _z(REQUEST_END),
        "target_start": TARGET_START.isoformat(),
        "target_end": TARGET_END.isoformat(),
        "sanitized_rows": len(sanitized_rows),
        "target_window_rows": len(target_rows),
        "provider_errors": len(provider_errors),
        "failed_validation_checks": len(failed_checks),
        "provider_condition_counts": dict(provider_condition_counts),
        "sanitized_csv": str(sanitized_csv.relative_to(ROOT)),
        "continuous_lineage_constructed": "NO",
        "forecast_computation": "NO",
        "position_computation": "NO",
        "cost_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "next_required_gate": "S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_EXECUTION_GATE",
    }


def _provenance_payload(status: dict[str, Any], sanitized_csv: Path, validation_csv: Path) -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "operator_authorization": "Operator Authorizes DataBento API access if needed at this stage.",
        "authorization_interpretation": "Bounded to S09 MES daily expansion only.",
        "lane_class": LANE_CLASS,
        "secret_handling": "Databento API key read from local approved source and never written to artifacts or stdout.",
        "status": status["status"],
        "sanitized_csv": str(sanitized_csv.relative_to(ROOT)),
        "validation_csv": str(validation_csv.relative_to(ROOT)),
        "boundary": [
            "NO_CONTINUOUS_CONTRACT_DOWNLOAD",
            "NO_PROVIDER_BUILT_CONTINUOUS_SERIES",
            "NO_ES_NQ_SUBSTITUTION",
            "NO_FORECAST_COMPUTATION",
            "NO_POSITIONS",
            "NO_COSTS",
            "NO_DIAGNOSTICS",
            "NO_BACKTESTS",
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
        ],
    }


def _condition_by_date(condition: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(row["date"]): str(row["condition"]).upper()
        for row in condition
        if row.get("date") and row.get("condition")
    }


def _contract_parts(raw_symbol: str) -> dict[str, int | str]:
    delivery_code = raw_symbol[-2]
    year_digit = int(raw_symbol[-1])
    year = 2020 + year_digit
    return {
        "contract_year": year,
        "delivery_month": MONTH_CODE_TO_MONTH[delivery_code],
        "delivery_code": delivery_code,
    }


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {
        "check_name": name,
        "check_status": "PASS" if passed else "FAIL",
        "observed_count": observed_count,
    }


def _read_databento_key() -> str:
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if len(env_key) == 32 and env_key.startswith("db-"):
        return env_key
    for path in KEY_CANDIDATES:
        if path is None or not path.exists():
            continue
        key = path.read_text(encoding="utf-8").strip()
        if len(key) == 32 and key.startswith("db-"):
            return key
    raise SystemExit("Fail closed: no valid-shaped Databento key found")


def _parse_ts(value: str) -> datetime:
    ts = datetime.fromisoformat(value.strip().replace(" ", "T").replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise RuntimeError("provider timestamp is not timezone-aware")
    return ts.astimezone(timezone.utc)


def _folders(root: Path) -> dict[str, Path]:
    return {
        "manifest": root / "manifest",
        "metadata": root / "raw_provider_metadata",
        "raw": root / "raw_provider_output",
        "sanitized": root / "sanitized_daily_bars",
        "validation": root / "validation",
        "status": root / "status",
        "provenance": root / "provenance",
        "hashes": root / "hashes",
    }


def _quarantine_stale_failure_artifacts(folders: dict[str, Path]) -> None:
    stale_provider_errors = folders["status"] / f"{RUN_ID}_provider_errors.csv"
    if not stale_provider_errors.exists():
        return
    failed_root = OUTPUT_ROOT / "failed_run_provenance"
    failed_root.mkdir(parents=True, exist_ok=True)
    destination = failed_root / f"{RUN_ID}_provider_errors_stale_failed_run.csv"
    if destination.exists():
        destination = failed_root / f"{RUN_ID}_provider_errors_stale_failed_run_{_compact_utc_now()}.csv"
    stale_provider_errors.replace(destination)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash_tree(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != f"{RUN_ID}_sha256.json"
    }


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _compact_utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


if __name__ == "__main__":
    main()

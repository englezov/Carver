# Carver Databento 16-Symbol Daily OHLCV Quarantine Intake Execution Fail-Closed

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_DATABENTO_16_SYMBOL_DAILY_OHLCV_QUARANTINE_INTAKE_EXECUTION_FAIL_CLOSED_AUTHENTICATION_401_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the bounded Databento execution gate result for the locked 16-symbol daily futures OHLCV quarantine pilot.

This follows:

```text
docs/process/CARVER_DATABENTO_16_SYMBOL_DAILY_FUTURES_QUARANTINE_INTAKE_SHAPE_GATE_DRAFT_2026-05-30.md
```

## Authorized Request

```text
dataset: GLBX.MDP3
schema: ohlcv-1d
symbols: ZTM6, ZFM6, ZNM6, MESM6, MNQM6, M2KM6, MYMM6, QMN6, RBN6, ZCN6, ZSN6, ZMN6, ZLN6, ZWN6, HEM6, LEM6
start: 2026-05-18T00:00:00Z
end: 2026-05-23T00:00:00Z
```

## Execution Result

Result:

```text
FAIL_CLOSED_DATABENTO_SYMBOLOGY_HTTP_401
```

Observed blockers:

```text
DATABENTO_API_KEY_AVAILABLE: YES
PROVIDER_API_ACCESSED: YES
FIRST_PROVIDER_ENDPOINT: https://hist.databento.com/v0/symbology.resolve
HTTP_STATUS: 401
ERROR_CASE: auth_authentication_failed
```

Actions taken:

```text
REQUEST_MANIFEST_CREATED: YES
PROVENANCE_RECORD_CREATED: YES
INTAKE_STATUS_CREATED: YES
PROVIDER_API_ACCESSED: YES
DATA_DOWNLOADED: NO
RAW_PROVIDER_OUTPUT_CREATED: NO
MARKET_ROWS_PARSED: NO
SANITIZED_OHLCV_CREATED: NO
DIAGNOSTICS_RUN: NO
BACKTESTS_RUN: NO
FORECASTS_COMPUTED: NO
POSITIONS_COMPUTED: NO
```

## Created Artifacts

```text
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/raw_provider_metadata/databento_request_manifest_2026-05-18_2026-05-22.json
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/raw_provider_metadata/databento_symbology_resolution_2026-05-18_2026-05-22.json
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_PROVENANCE.md
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_INTAKE_STATUS.csv
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/provenance/databento_error_body_redacted.txt
```

## Interpretation

This is an authentication failure, not a data-quality failure, not a symbol-mapping failure, not a provider-content failure, and not evidence that any of the 16 dated contracts are unavailable from Databento.

The key was present in the process environment, but Databento rejected it with HTTP 401 before any market-row output was returned. No key value was printed or recorded.

The next clean action is to verify the Databento portal API key value/permissions locally, without pasting the secret into chat or any repo artifact, then retry the exact same locked request. No symbol, date, schema, dataset, or contract change is justified by this failure.

## Metadata Auth Ping

A follow-up secret-safe metadata-only check confirmed that the failure is independent of the 16-symbol request shape:

```text
KEY_PRESENT: YES
KEY_EMPTY: NO
LEADING_OR_TRAILING_WHITESPACE: NO
EMBEDDED_NEWLINE: NO
WRAPPED_IN_QUOTES: NO
METADATA_LIST_SCHEMAS_STATUS: 401 auth_authentication_failed
METADATA_LIST_UNIT_PRICES_STATUS: 401 auth_authentication_failed
MARKET_DATA_REQUESTED: NO
MARKET_ROWS_PARSED: NO
```

This confirms the current blocker is Databento API key/account authentication, not the locked manifest, not the dated-contract symbols, not the date window, and not the quarantine parser.

## Full-Line Desktop Key Retry

The operator supplied a fresh `BENTO.txt` on the desktop and stated it was copied with the Databento portal copy button. The retry read the entire first non-empty line as the key, not a regex subset, then deleted the file.

```text
BENTO_FILE_FOUND: YES
NONEMPTY_LINE_FOUND: YES
KEY_EMPTY: NO
KEY_LENGTH_BUCKET: 20to39
BENTO_FILE_DELETED: YES
METADATA_LIST_SCHEMAS_STATUS: 401 auth_authentication_failed
METADATA_LIST_UNIT_PRICES_STATUS: 401 auth_authentication_failed
MARKET_DATA_REQUESTED: NO
MARKET_ROWS_PARSED: NO
```

No key value was printed or recorded. The repeated 401 after a full-line copy-button key indicates the remaining issue is Databento portal/key/account validity or API-auth method, not local extraction truncation.

## New Portal Key Retry

The operator created a new Databento API key, supplied it in a new desktop `BENTO.txt`, and the retry again read the entire first non-empty line, set it as `DATABENTO_API_KEY`, and deleted the file.

```text
BENTO_FILE_FOUND: YES
NONEMPTY_LINE_FOUND: YES
KEY_EMPTY: NO
KEY_LENGTH_BUCKET: 20to39
BENTO_FILE_DELETED: YES
METADATA_LIST_SCHEMAS_STATUS: 401 auth_authentication_failed
METADATA_LIST_UNIT_PRICES_STATUS: 401 auth_authentication_failed
MARKET_DATA_REQUESTED: NO
MARKET_ROWS_PARSED: NO
```

This second full-line copy-button/new-key retry still failed at Databento metadata authentication. The exact 16-symbol OHLCV request was not retried because metadata authentication did not pass.

## Rotated Key Retry

The operator rotated the exposed Databento keys and supplied a fresh desktop `BENTO.txt`. The retry read the entire first non-empty line, set it as `DATABENTO_API_KEY`, and deleted the file.

```text
BENTO_FILE_FOUND: YES
NONEMPTY_LINE_FOUND: YES
KEY_EMPTY: NO
KEY_LENGTH_BUCKET: 20to39
BENTO_FILE_DELETED: YES
METADATA_LIST_SCHEMAS_STATUS: 401 auth_authentication_failed
METADATA_LIST_UNIT_PRICES_STATUS: 401 auth_authentication_failed
MARKET_DATA_REQUESTED: NO
MARKET_ROWS_PARSED: NO
```

The rotated key was still rejected by Databento metadata authentication. The exact 16-symbol OHLCV request remained closed.

## Verified 32-Character Key Retry

The operator supplied a new desktop `BENTO.txt` that was checked before consumption and confirmed to contain exactly one plausible Databento API key.

```text
BENTO_FILE_FOUND: YES
KEY_SHAPE_VALID: YES
KEY_LENGTH: 32
KEY_STARTS_WITH_DB_DASH: YES
BENTO_FILE_DELETED: YES
METADATA_LIST_SCHEMAS_STATUS: 401 auth_authentication_failed
METADATA_LIST_UNIT_PRICES_STATUS: 401 auth_authentication_failed
AUTH_METADATA_OK: NO
MARKET_DATA_REQUESTED: NO
MARKET_ROWS_PARSED: NO
```

This removes the prior ambiguity around regex truncation, concatenated keys, visible-table copies, and malformed local file shape. The remaining blocker is Databento-side authentication/account/API activation for a valid-shaped portal key.

## Closed Boundaries

Still closed:

```text
provider API access
data download
market-row parsing
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility or risk calculations
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
GitHub staging
commit
push
PR update/opening
remote repository operations
```

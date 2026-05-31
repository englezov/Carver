# Carver S26 ZN Hourly Request Manifest Plumbing Lean Hostile Audit

Date: 2026-05-30

Status:

```text
LOCAL_LEAN_HOSTILE_AUDIT_RESULT_REQUEST_MANIFEST_PLUMBING_PASS_PROCESS_ONLY
```

Audited artifacts:

```text
src/carver/spine/s26_s27.py
src/carver/spine/__init__.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
docs/process/CARVER_S26_ZN_HOURLY_DATABENTO_TINY_INTAKE_EXECUTION_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_REQUEST_MANIFEST_PLUMBING_RESULT_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_ROW_NORMALIZATION_PLUMBING_RESULT_2026-05-30.md
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/request_manifest/CARVER_S26_ZN_DATABENTO_OHLCV_1H_REQUEST_MANIFEST_2026-05-30.json
```

## Findings

### Critical

None.

No Databento client, API key file, HTTP request library, CSV writer, CSV reader, provider download function, market-row parser, diagnostic, backtest, forecast-on-real-data execution, position output, cost/carry/trend computation, Git operation, or remote operation was added.

### High

None.

The manifest is process-only and locked to the S26 worked-example source path:

```text
APPENDIX_C_172_004 / ZN / Databento instrument_id 42000661 / ZNM6 / GLBX.MDP3 / ohlcv-1h
```

The request-manifest validator fails closed on dataset, schema, selector, symbol, raw-symbol, window, output-root, and no-authorization drift before any future provider call.

The row normalizer is in-memory only and fails closed on wrong provider/dataset/schema/symbol, timestamp envelope drift, non-hour timestamps, OHLCV shape errors, and unauthorized strategy-use status. Its default output status is `QUARANTINE_ONLY_NOT_FORECAST_READY`, which cannot feed the S26 forecast function.

### Medium

None.

The current chapter remains incomplete by design: the manifest creates a clean future execution envelope, but it does not authorize or perform provider access, data download, market-row parsing, or S26 forecast execution on real rows.

## Verification

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic
Ran 16 tests
OK

python -m unittest discover -s tests
Ran 171 tests
OK
```

Scope scan over the touched S26/S27 files found no active provider/client/request/CSV IO hook.

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_S26_ZN_HOURLY_REQUEST_MANIFEST_PLUMBING_NOT_DATA_AUTHORIZATION
GOAL_STATUS: PROGRESS_ONLY_NOT_COMPLETE
NEXT_REQUIRED_OPERATOR_GATE_AFTER_G_R1A_COMPLETION: G_R1B_ZN_S26_HOURLY_SIGMA_PERCENT_AND_FORECAST_ONLY_HANDOFF
```

## Non-Authorization

This audit authorizes no provider API access, no data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

# Carver Source-Native Data Acquisition Layer Hostile Audit

Date: 2026-05-29

Status:

```text
PROCESS_SAFE_FOR_CURRENT_GATE_NOT_BULK_EXECUTION_AUTHORIZATION
```

## Scope

Hostile audit of the manifest-driven source-native daily futures data acquisition layer:

```text
src/carver/spine/data_acquisition.py
tests/test_data_acquisition_synthetic.py
config/carver_daily_futures_manifest_parts_1_3_seed.json
docs/process/CARVER_SOURCE_NATIVE_DATA_ACQUISITION_LAYER_GATE_2026-05-29.md
src/carver/spine/__init__.py
tools/nt8/CarverDailyBarExporter.cs
docs/process/CARVER_NINJATRADER_DESKTOP_DAILY_EXPORT_BRIDGE_GATE_2026-05-29.md
docs/process/CARVER_S09_ZN_NINJATRADER_DESKTOP_EXPORT_EXECUTION_GATE_2026-05-29.md
```

## Initial Findings

The first hostile audit found two blockers:

1. Parser entry was not actually manifest-bound. A caller could supply a source-native request for an undeclared root and parse rows if the request was internally consistent.
2. The JSON manifest was inert relative to the code-built manifest; config drift would not fail tests.

## First Patch

Patches applied:

- Parser entry now requires `NinjaTraderNativeDailyExportRequest` membership in `SourceNativeDailyAcquisitionManifest`.
- Default parser calls bind to `build_parts_1_3_daily_seed_manifest()`.
- ES/MES non-manifest parser attempts fail closed in tests.
- JSON seed config is loaded from the locked config path.
- JSON seed config is compared against the code-built manifest.
- Drift in request fields fails closed.

Re-audit found one remaining blocker:

- root comparison used a dictionary keyed by root, which could hide duplicate root rows or ignore non-dict rows.

## Second Patch

Patches applied:

- JSON root list is now compared as an exact ordered list.
- Non-dict root rows fail.
- Duplicate root rows fail.
- Reordered root rows fail through exact-list mismatch.
- Targeted tests pass.

## Final Re-Audit Verdict

```text
Blockers: None.
```

Confirmed:

- Config roots are compared as exact ordered list.
- Non-dict root rows fail.
- Duplicate root rows fail.
- Reordered root rows fail.
- Parser membership blocker is resolved.
- JSON/config drift blocker is resolved.
- No synthetic files were left behind under `data/`.

## Verification

Local verification after patches:

```text
python -m unittest tests.test_data_acquisition_synthetic -v
8 passed

python -m unittest discover -s tests -v
82 passed

python -m compileall -q src tests
passed

git diff --check
passed, with expected CRLF warnings on Windows-touched text files
```

## Non-Authorization

This audit authorizes no bulk data download execution, no NinjaTrader batch run, no strategy computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

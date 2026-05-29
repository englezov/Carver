# Carver NinjaTrader Manifest Daily Export Helper Hostile Audit

Date: 2026-05-29

Status:

```text
PROCESS_SAFE_FOR_HELPER_GATE_NOT_RUN_NOT_BULK_DOWNLOAD_AUTHORIZATION
```

## Scope

Subagent hostile audit of the prepared NinjaTrader manifest daily export helper gate:

```text
src/carver/spine/data_acquisition.py
tests/test_data_acquisition_synthetic.py
tools/nt8/CarverManifestDailyExporter.cs
docs/process/CARVER_NINJATRADER_MANIFEST_DAILY_EXPORT_HELPER_GATE_2026-05-29.md
docs/process/CARVER_SOURCE_NATIVE_DATA_ACQUISITION_LAYER_GATE_2026-05-29.md
```

The audit checked for hidden bulk-run authorization, helper arming by default, manifest drift, non-ZN symbols, ES/MES substitution, output-path leakage, strategy/backtest/diagnostic/performance leakage, account/order/position usage, CFD leakage, old QuantLab contamination, and missing synthetic witnesses.

## Findings

Blockers:

```text
None.
```

Confirmed:

- `ExecutionArmed = false` by default.
- The disarmed path returns before manifest requests begin.
- The helper rows are exactly:

```text
ZN SEP25
ZN DEC25
ZN MAR26
ZN JUN26
```

- Output is locked to:

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports
```

- Tests assert exact row membership, no `ES`, no `MES`, no account/order fragments, `BarsPeriodType.Day`, `LookupPolicies.Provider`, and manifest-derived Python export-plan rows.
- No strategy, signal, backtest, diagnostic, performance, PnL, Sharpe, OOS, Lockbox, Forward, CFD adapter, old QuantLab, deployment, trading, or promotion path was found in the scoped helper.

## Non-Blocking Notes

- NinjaScript compile/runtime correctness inside NinjaTrader Desktop is not proven by Python tests. It remains a future desktop compile gate.
- The helper duplicates the seed manifest rows in C# rather than reading JSON inside NinjaTrader. Synthetic tests now pin the exact C# rows to the Python manifest, so this is acceptable for the current seed gate but should be revisited when the manifest expands.

## Verification

Local verification:

```text
python -m unittest tests.test_data_acquisition_synthetic -v
10 passed

python -m compileall -q src tests
passed

python -m unittest discover -s tests -v
84 passed

git diff --check
passed, with expected CRLF warnings on Windows-touched text files
```

## Non-Authorization

This audit authorizes no helper import, no NinjaTrader compile, no chart attachment, no `ExecutionArmed = true`, no bulk export/download execution, no parser run on real files, no continuous roll/back-adjustment construction, no strategy computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

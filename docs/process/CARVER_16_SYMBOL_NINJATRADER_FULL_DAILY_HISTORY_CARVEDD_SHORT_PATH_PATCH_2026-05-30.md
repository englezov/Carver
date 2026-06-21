# Carver 16-Symbol NinjaTrader Full Daily History CarveDD Short-Path Patch

Date: 2026-05-30

Status:

```text
PROCESS_LOCAL_CARVER_CARVEDD_SHORT_PATH_OUTPUT_PATCH_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Scope

This record preserves the process/helper patch after the first `CarveDD` full-history attempt failed before writing files because NinjaTrader/Windows rejected the long output path.

No NinjaTrader execution, data export, provider API access, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, OOS, Lockbox, Forward, CFD adapter work, deployment, trading, promotion, Git staging, commit, push, PR update, or remote operation was performed by this patch.

## Patch

The locked physical helper output root was shortened to:

```text
C:\Users\openclaw\Desktop\Carver\q\nt16fh
```

This short path is the physical quarantine alias for the longer governance chapter path:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\NINJATRADER\20260530_FULL_HISTORY_HELPER_ATTEMPT
```

The helper still writes only these subfolders under the short root:

```text
raw_market_files
provider_metadata
```

The helper remains locked to:

- exact 16-symbol manifest only;
- exact dated contracts only;
- `1 Day` bars only;
- `Last` only;
- NinjaTrader helper raw output with template-derived UTC session-end timestamps;
- zero-silent-row-skip availability reporting;
- replacement disabled;
- disarmed-by-default source file.

## Helper Files

Repo helper:

```text
C:\Users\openclaw\Desktop\Carver\tools\nt8\CarveDD.cs
```

Imported NinjaTrader helper copy:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\CarveDD.cs
```

Repo helper SHA256:

```text
A44E2D406BCBDE58A4CAE28DF07EE42383E70A702D445239CFEE084CD71CAFB1
```

Imported NinjaTrader helper copy SHA256:

```text
AD45925E8C91E7F26D98391D76F6832B894A5489E8DCDBD5D86687766C3BDEBB
```

The imported copy can differ from the repo helper hash after NinjaTrader adds generated cache/wrapper regions. The checked locked fields are the operational controls for this patch.

Both files are currently disarmed:

```text
private const bool ExecutionArmed = false;
```

## Next Authorized Execution Surface

A later execution gate may arm only the imported NinjaTrader copy by changing:

```text
private const bool ExecutionArmed = true;
```

The chart parameter must still use:

```text
OPERATOR_AUTHORIZED_16_SYMBOL_FULL_DAILY_HISTORY_DAILY_LAST_QUARANTINE
```

The chart must still be a `1 Day` / `Last` chart for one locked manifest contract, with maximum bars look back set to `Infinite`.

## Non-Authorization

This patch does not authorize any new data export, any wider symbol set, any diagnostics, any backtest, any forecast computation, any position sizing, any costs, any carry, any trend, any OOS, any Lockbox, any Forward, any deployment, any trading, any promotion, any Git operation, or any remote operation.

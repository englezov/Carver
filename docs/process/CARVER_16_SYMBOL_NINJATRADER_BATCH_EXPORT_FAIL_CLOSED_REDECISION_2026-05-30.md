# Carver 16-Symbol NinjaTrader Batch Export Fail-Closed Redecision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_NINJATRADER_BATCH_EXPORT_FAIL_CLOSED_REDECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the result of the first locked 16-symbol NinjaTrader helper execution attempt and decide the next clean gate.

This decision follows:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_LOCKED_MANIFEST_DAILY_EXPORT_HELPER_2026-05-30.md
```

The execution attempt was authorized only for the exact 16-symbol manifest, exact dated contracts, `1 Day` / `Last` bars, and completed trading dates `2026-05-18` through `2026-05-22`.

This artifact records process state only. It does not export data, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active pipelines, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Execution Evidence

Repo helper:

```text
tools/nt8/Carver16SymbolDailyExporterSessionEndUtc.cs
SHA256: 25DE90BFF6A87435E3699CE1849B30E3F76CACC6F317902C0FBD1E957B91AA03
repo default: ExecutionArmed = false
```

Imported NinjaTrader helper copy:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\Carver16SymbolDailyExporterSessionEndUtc.cs
ExecutionArmed = true
AllowReplaceExistingFiles = false
LockedOutputRoot = C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22
```

Observed NinjaTrader log file:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\log\log.20260530.00001.en.txt
```

Observed failure class:

```text
BATCH_EXPORT_FAIL_CLOSED_PROVIDER_BARS_UNAVAILABLE
```

Representative log message:

```text
Carver 16-symbol export blocked: missing completed daily bar for <contract> date=2026-05-18
```

Unique contracts observed with the missing first-date failure:

```text
HE JUN26
LE JUN26
M2K JUN26
MES JUN26
MNQ JUN26
MYM JUN26
QM JUL26
RB JUL26
ZC JUL26
ZF JUN26
ZL JUL26
ZM JUL26
ZN JUN26
ZS JUL26
ZT JUN26
ZW JUL26
```

Quarantine output check:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22
MISSING_16_SYMBOL_QUARANTINE_ROOT
```

Interpretation:

```text
NO_HELPER_RAW_OUTPUT_FILES_WRITTEN
NO_PARTIAL_BATCH_OUTPUT
NO_MARKET_ROW_PARSING
NO_DIAGNOSTICS
NO_BACKTESTS
NO_FORECASTS
NO_POSITIONS
```

## What The Failure Means

This is a provider/data-availability or helper-request-path failure, not a Carver source-universe failure and not a portfolio construction failure.

The failure occurred before any quarantine raw-output file was written. The helper's all-or-nothing boundary held: no subset was accepted, no missing member was dropped, no substitute was selected, and no weights were changed.

The visible popup showed a single contract because NinjaTrader surfaced one exception at a time. The logs show the same first required completed date missing across the manifest, which indicates the issue is broader than one bad row.

## Options Considered

### Option A: Immediately authorize exact 16-row provider-backed historical retrieval again

Disposition:

```text
NOT_SELECTED_AS_NEXT_GATE
```

Reason:

The just-attempted helper path already requested the exact 16 rows through NinjaTrader `BarsRequest` with provider lookup. Repeating the same path without better failure accounting would likely reproduce the same cascade of exceptions and would not improve governance evidence.

### Option B: Reduce to a smaller cache-proven subset

Disposition:

```text
NOT_SELECTED_AS_NEXT_GATE
```

Reason:

The logs show first-date missing failures across the full manifest, including the previously successful MES family. That makes this look like a retrieval/cache/request-path issue rather than evidence that only a smaller subset is valid. Shrinking now would prematurely weaken the 16-symbol pilot without first proving which rows are genuinely unavailable.

### Option C: Patch the helper path for availability preflight and clean failure accounting

Disposition:

```text
SELECTED_NEXT_GATE
```

Reason:

The next useful step is to harden the helper so future authorized runs can report row-level availability cleanly before any helper raw-output file is written. The patch should preserve the 16-row manifest and fail-closed rules, but avoid treating the first missing bar as an ambiguous single-row popup.

## Decision

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_HELPER_AVAILABILITY_PREFLIGHT_PATCH
```

The patch gate should update only the locked helper and process handoff. It should not execute NinjaTrader, export data, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, or perform remote operations.

Required patch properties:

- keep the repo helper disarmed by default;
- keep the exact 16-symbol manifest unchanged;
- keep `1 Day` / `Last` and `2026-05-18` through `2026-05-22` unchanged;
- keep replacement disabled;
- keep output locked under the 16-symbol quarantine root;
- preflight and report all row/date availability failures before any helper raw-output write;
- preserve all-or-nothing semantics;
- avoid silently dropping unavailable rows;
- avoid silently selecting substitute contracts;
- avoid silently changing the target date window;
- avoid silently switching to continuous contracts;
- avoid writing sanitized bars or any downstream market-row artifact.

After that patch is created and lean-audited, a separate operator gate may authorize a renewed local NinjaTrader execution. That later execution may choose between:

```text
EXACT_16_ROW_AVAILABILITY_PREFLIGHT_ONLY
EXACT_16_ROW_EXPORT_IF_AND_ONLY_IF_ALL_ROWS_AVAILABLE
SMALLER_SUBSET_REDECISION_AFTER_AVAILABILITY_EVIDENCE
```

No such later execution is authorized by this artifact.

## Closed Boundaries

Still closed:

```text
new data export
provider API access beyond separately authorized NinjaTrader local execution
market-row parsing
diagnostics
backtests
forecasts
positions
costs
carry
trend
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
remote operations
```

## Non-Authorization

This decision authorizes no new data export, no provider API access, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.

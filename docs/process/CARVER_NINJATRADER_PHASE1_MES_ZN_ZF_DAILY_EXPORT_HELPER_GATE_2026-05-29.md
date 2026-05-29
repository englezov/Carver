# Carver NinjaTrader Phase-1 MES/ZN/ZF Daily Export Helper Gate

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_NINJATRADER_PHASE1_MES_ZN_ZF_DAILY_EXPORT_HELPER_NOT_EXECUTED_NOT_DIAGNOSTIC
```

## Purpose

Prepare the NinjaTrader Desktop export helper needed for the next phase-1 daily chain export.

This helper is the execution-side companion to:

```text
docs/process/CARVER_MULTI_ASSET_DAILY_MANIFEST_PHASE1_GATE_2026-05-29.md
```

It is prepared but not executed.

## Helper

```text
tools/nt8/CarverManifestDailyExporterPhase1.cs
```

The helper defaults to:

```text
ExecutionArmed = false
AllowReplaceExistingFiles = false
```

It prints a prepared-not-armed message and returns unless a future operator execution gate explicitly arms it inside NinjaTrader Desktop.

## Locked Manifest

```text
CARVER_PARTS_1_3_DAILY_SEED_MULTI_ASSET_PHASE1_MES_ZN_ZF
```

## Locked Output Root

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports
```

## Prepared Rows

The helper contains exactly these source-native daily `Last` rows:

```text
MES SEP25  2025-05-29 -> 2026-05-28  MES\MES 09-25.Last.txt
MES DEC25  2025-05-29 -> 2026-05-28  MES\MES 12-25.Last.txt
MES MAR26  2025-05-29 -> 2026-05-28  MES\MES 03-26.Last.txt
MES JUN26  2025-05-29 -> 2026-05-28  MES\MES 06-26.Last.txt
ZN  SEP25  2025-05-29 -> 2026-05-28  ZN\ZN 09-25.Last.txt
ZN  DEC25  2025-05-29 -> 2026-05-28  ZN\ZN 12-25.Last.txt
ZN  MAR26  2025-05-29 -> 2026-05-28  ZN\ZN 03-26.Last.txt
ZN  JUN26  2025-05-29 -> 2026-05-28  ZN\ZN 06-26.Last.txt
ZF  SEP25  2025-05-29 -> 2026-05-28  ZF\ZF 09-25.Last.txt
ZF  DEC25  2025-05-29 -> 2026-05-28  ZF\ZF 12-25.Last.txt
ZF  MAR26  2025-05-29 -> 2026-05-28  ZF\ZF 03-26.Last.txt
ZF  JUN26  2025-05-29 -> 2026-05-28  ZF\ZF 06-26.Last.txt
```

No `ES`, `QM`, `ZC`, or `MGC` rows are admitted in this helper. Commodity roots remain pending separate chain-month convention locks.

## Boundary

This gate prepares a helper only. It does not:

- import the helper into NinjaTrader;
- compile the helper in NinjaTrader;
- arm or execute the helper;
- overwrite existing ZN export files;
- validate newly exported files;
- build continuous chains for MES or ZF;
- compute forecasts, returns, PnL, Sharpe, drawdown, hit rate, costs, turnover, diagnostics, or backtests.

The existing ZN-only helper remains in place for the historical ZN execution gate:

```text
tools/nt8/CarverManifestDailyExporter.cs
```

## Next Execution Gate

A future operator authorization may run `CarverManifestDailyExporterPhase1` with `ExecutionArmed = true` for the prepared rows only, writing only under the locked quarantine root.

That future execution gate must explicitly choose one overwrite policy:

```text
ALLOW_REPLACE_LOCKED_TARGET_FILES by setting AllowReplaceExistingFiles = true
```

or:

```text
REQUIRE_CLEAN_OR_RUN_STAMPED_OUTPUT_PATH by leaving AllowReplaceExistingFiles = false
```

The prepared helper currently writes via a temporary file and refuses to replace an existing target unless `AllowReplaceExistingFiles = true`. That replacement behavior is not executed or authorized by this helper-preparation gate.

After that execution, the next process steps are:

1. Parser-only validation of the phase-1 export files.
2. Continuous-readiness construction for `MES`, `ZN`, and `ZF`.
3. S09 multi-instrument forecast conformance without returns or diagnostics.

The code now has a phase-1 readiness report surface that can summarize all three roots after export:

```text
build_phase1_continuous_readiness_report
render_phase1_continuous_readiness_markdown
```

## Verification

```text
python -m unittest tests.test_data_acquisition_synthetic -v
```

Full-suite verification and hostile audit are required before local commit.

## Non-Authorization

This artifact authorizes no NinjaTrader execution, no bulk data download execution, no strategy computation, no returns, no PnL, no Sharpe, no drawdown, no hit rate, no costs, no turnover, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

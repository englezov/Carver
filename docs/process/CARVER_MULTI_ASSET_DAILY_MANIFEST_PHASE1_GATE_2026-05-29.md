# Carver Multi-Asset Daily Manifest Phase 1 Gate

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_MULTI_ASSET_DAILY_MANIFEST_PHASE1_NOT_BULK_DOWNLOAD_NOT_DIAGNOSTIC
```

## Purpose

Extend the source-native daily acquisition framework beyond the already-executed ZN chain, without running new exports or downloads.

This phase prepares the first small multi-asset daily seed for movement toward portfolio construction:

```text
MES  S&P 500 micro future
ZN   US 10-year bond future
ZF   US 5-year bond future
```

The remaining P02 seed roots remain declared but not chain-locked in this phase:

```text
QM   WTI Crude Oil mini future
ZC   Corn future
MGC  Gold micro future
```

Commodity chain selection is intentionally not inferred here because contract-month cycles and seasonal roll handling need their own lock before export execution.

## Implemented Surface

Code:

```text
src/carver/spine/data_acquisition.py
```

Public objects:

```text
build_parts_1_3_multi_asset_phase1_manifest
manifest_export_requests_for_root
build_continuous_readiness_for_root_from_native_exports
```

The phase-1 manifest id is:

```text
CARVER_PARTS_1_3_DAILY_SEED_MULTI_ASSET_PHASE1_MES_ZN_ZF
```

Each phase-1 root uses daily `Last` requests over:

```text
start date: 2025-05-29
end date: 2026-05-28
contract months: 09-25, 12-25, 03-26, 06-26
```

This creates 12 prepared request rows:

```text
MES SEP25, MES DEC25, MES MAR26, MES JUN26
ZN  SEP25, ZN  DEC25, ZN  MAR26, ZN  JUN26
ZF  SEP25, ZF  DEC25, ZF  MAR26, ZF  JUN26
```

No `ES` row is admitted.

## Continuous-Readiness Framework Extension

The prior ZN readiness helper remains available:

```text
build_zn_continuous_readiness_from_native_exports
```

It now delegates to the generic root-filtered entrypoint:

```text
build_continuous_readiness_for_root_from_native_exports
```

The generic entrypoint parses only the manifest-declared export requests for the requested root and then applies the same continuous-chain fail-closed checks. It fails closed if the manifest has no export requests for that root.

## Explicitly Not Done

This gate does not:

- edit the already-executed ZN quarantine files;
- run NinjaTrader;
- execute the phase-1 export rows;
- infer commodity contract chains;
- stitch any newly exported real data;
- compute S09 forecasts for MES or ZF;
- compute returns, PnL, Sharpe, drawdown, hit rate, costs, turnover, diagnostics, or backtests.

## Verification

```text
python -m unittest tests.test_data_acquisition_synthetic -v
12 passed

python -m unittest tests.test_continuous_synthetic -v
5 passed
```

Full-suite verification belongs to the broader portfolio-construction bridge goal before commit.

## Next Gate

The next execution-style gate should authorize a specific NinjaTrader Desktop export helper update or run for the phase-1 `MES/ZN/ZF` rows only, still writing only to the Git-ignored native daily quarantine.

The next process-only gate should separately lock commodity chain month conventions for `QM`, `ZC`, and `MGC` before they are added to an executable export helper.

## Non-Authorization

This artifact authorizes no bulk data download execution, no NinjaTrader export execution, no strategy computation, no returns, no PnL, no Sharpe, no drawdown, no hit rate, no costs, no turnover, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

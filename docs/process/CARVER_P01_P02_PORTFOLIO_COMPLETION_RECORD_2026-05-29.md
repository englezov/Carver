# Carver P01/P02 Portfolio Completion Record

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P01_P02_PORTFOLIO_PACKAGE_COMPLETE_REAL_DATA_BLOCKED
```

## Purpose

Record the first complete source-native portfolio package boundary for Carver P01/P02.

This is not a backtest and not a data run. It is the lean gate that says how P01/P02 connect from source-native instruments through completed daily bars into portfolio sizing, and which facts still block real-data conformance.

## Completed Package

The package now contains:

- P01 exact portfolio definition: `MES` and `ZN`, 50/50 risk weights.
- P02 exact portfolio definition: `MES`, `ZN`, `ZF`, `QM`, `ZC`, `MGC`, weights 25 / 12.5 / 12.5 / 12.5 / 12.5 / 25.
- Direct daily bars as the preferred first intake path because NinjaTrader can provide daily candles.
- Direct daily Web Chart normalization is represented in code as a first-class path; minute-to-daily derivation remains fallback only.
- Minute-to-completed-daily derivation as a tested fallback only, requiring a full contiguous locked session.
- Quarantined JSON chart response normalization with exact request/provider binding.
- P01/P02 conformance orchestration from completed daily bars, prevalidated annual risk, and aligned FX inputs.
- A completion report object that fails closed until all real-data prerequisites are locked as artifacts, not as bare status flags.
- A named real-data conformance preflight that blocks future real-data sizing until the completion report is ready.
- Continuous/roll/back-adjustment placeholders that intentionally refuse to build a series until separate source rules are locked.

## Current Mapping Status

Observed and locked:

```text
ZN 06-26 ZN JUN26 -> 4470301
```

Observed but not a book-contract substitute for P01/P02:

```text
ES 06-26 ES JUN26 -> 3570919
```

Still unresolved for P01/P02:

```text
MES 06-26
ZF  06-26
QM  06-26
ZC  06-26
MGC 06-26
```

`ES` must not be used as a silent replacement for `MES`.

## Real-Data Blockers

Before any real P01/P02 conformance run:

- Lock exact provider IDs for `MES`, `ZN`, `ZF`, `QM`, `ZC`, and `MGC`.
- Lock the intake-route contract as a source artifact: direct daily primary or minute-derived fallback.
- Lock session calendars/timezones as `SessionCalendarSpec` artifacts for the selected route.
- Lock roll and back-adjustment rules as `RollRuleSpec` and `BackAdjustmentSpec` artifacts for continuous futures use.
- Lock the annual risk input source and FX input source as prevalidated facts.
- Keep raw responses inside quarantine and require exact request/provider binding.

## Non-Authorization

This record authorizes no real WebSocket call, no token/cookie/storage extraction, no NinjaTrader export, no `.ncd` decoding, no bulk download, no data diagnostic, no backtest, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.

## Audit Note

After this package is locally stable, an external Opus audit is appropriate for a higher-level source-faithfulness check:

```text
Did the Carver P01/P02 portfolio package preserve the book's instrument set,
portfolio weights, completed-bar assumptions, source-native futures boundary,
and no-substitution/no-tuning/no-backtest discipline?
```

That audit should inspect the book, the module specs, the P01/P02 briefs, this completion record, and the synthetic code/tests. It should not run data or code unless separately authorized.

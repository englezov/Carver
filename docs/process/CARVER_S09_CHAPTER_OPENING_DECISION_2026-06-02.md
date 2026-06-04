# Carver S09 Chapter Opening Decision

Date: 2026-06-02

Status:

```text
PROCESS_ONLY_S09_CHAPTER_OPENING_DECISION_NOT_DATA_AUTHORIZATION
```

## Decision

Open the next Carver source-native research chapter as:

```text
S09_DEV_RECON_DAILY_SINGLE_INSTRUMENT
```

Strategy:

```text
S09_MULTIPLE_TREND_FOLLOWING_RULES
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

This follows the preserved Opus hostile audit recommendation after S26/S27 parking:

```text
docs/process/CARVER_NEXT_CANDIDATE_AFTER_S26_S27_PARK_OPUS_HOSTILE_AUDIT_RAW_2026-06-02.md
SHA256: 82EDF4A5A067AD25EBFC11BBD63D9BFC1C65880C898BBEE0719996A622A71AE2
```

## Source-Framing Summary

S09 is the next clean book-ordered candidate because it is the first Part One chapter that combines the individual EWMAC trend sleeves into a complete multiple-rule trend forecast.

The opening gate is daily and source-native. It does not inherit S26/S27 hourly machinery, V/Q/M attenuation, M1 ladder behavior, CFD adapter assumptions, or old QuantLab state.

## Initial Scope

The first S09 chapter work should lock and perform process/synthetic conformance checks only for the source-native trend forecast machinery:

- EWMAC speeds: 2, 4, 8, 16, 32, 64, with slow span equal to 4x fast span.
- Per-speed Carver forecast scalars.
- Individual rule cap at +/-20.
- Combined trend forecast with source-locked rule weights and FDM.
- Daily completed bars only.
- Development/Reconciliation labels only.

## Known Preconditions

Before any real S09 strategy test:

- re-instantiate EWMAC source-clean rather than assuming S27 dependency code is reusable;
- keep S09 independent from S13-style volatility attenuation and S26/S27 hourly context;
- preserve cost-filter and active-rule behavior as an explicit source atom rather than silently using all rules everywhere;
- keep Appendix C and Databento data foundations as background only until a new data/parsing gate is opened.

## Non-Authorization

This decision authorizes no provider access, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts on real data, no positions, no costs, no carry, no CFD adapter work, no old QuantLab pipeline use, no tuning, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR update.

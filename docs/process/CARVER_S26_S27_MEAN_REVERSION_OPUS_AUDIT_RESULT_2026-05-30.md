# Carver S26/S27 Mean-Reversion Opus Audit Result

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_S26_S27_OPUS_AUDIT_RESULT_NOT_DATA_NOT_IMPLEMENTATION_NOT_BACKTEST
```

## Purpose

Preserve the Opus hostile source-faithful design audit result for Carver Strategies 26 and 27:

```text
S26: Strategy twenty-six: Fast mean reversion
S27: Strategy twenty-seven: Safer fast mean reversion
```

This record opens the next chapter as:

```text
G_SYN_S26_S27_SOURCE_ATOM_LOCK_AND_SYNTHETIC_CONFORMANCE
```

The chapter is source atom and synthetic conformance only. It does not authorize real data, provider access, market-row parsing, diagnostics, backtests, forecasts on real data, positions, costs, carry, trend-sleeve computation, risk calculations, deployment, trading, promotion, Git operations, or remote operations.

## Preserved Opus Verdict

```text
AUDIT_DISPOSITION: SOURCE_PATH_DEFINED_BUT_BLOCKED_AT_FIRST_REAL_DATA_GATE_BY_FREQUENCY
RECOMMENDED_NEXT_GATE: G_SYN_S26_S27_SOURCE_ATOM_LOCK_AND_SYNTHETIC_CONFORMANCE
```

## Strategy Classification

| Strategy | Research classification | Book-performance classification | Current real-data posture |
| --- | --- | --- | --- |
| S26 | `STANDALONE_CANDIDATE` | `SOURCE_NATIVE_PORTFOLIO_SLEEVE` | `BLOCKED_SOURCE_UNRESOLVED` |
| S27 | `STANDALONE_CANDIDATE_WITH_DEPENDENCIES` | `SOURCE_NATIVE_PORTFOLIO_SLEEVE` | `BLOCKED_SOURCE_UNRESOLVED` |

S26 is a standalone fast mean-reversion forecast candidate at the rule level, but the book reports it at Jumbo aggregate level.

S27 is a safer fast mean-reversion candidate with explicit dependencies on S26, EWMAC(16,64), and the S13-style relative-volatility attenuation mechanism. It is not self-contained.

## Blocking Findings Preserved

### 1. Data-Frequency Mismatch

The controlling source atom is hourly data. Part Four states that these strategies generate forecasts more frequently than the daily strategies and are backtested on hourly data. The current Appendix C daily data foundation certified only `ohlcv-1d` daily bars for the Development/Reconciliation subset.

Disposition:

```text
CURRENT_DAILY_DATA_FOUNDATION_NOT_SOURCE_FREQUENCY_COMPATIBLE_WITH_S26_S27
```

### 2. ALI Fail-Closed Row

`APPENDIX_C_181_001 / ALI / Aluminium` remains fail-closed in the daily Appendix C foundation. This blocks any full aggregate Jumbo conformance claim.

Disposition:

```text
ALI_FAIL_CLOSED_PRESERVED_NO_FILL_DROP_SUBSTITUTE_REWEIGHT
```

### 3. S27 Dependency Chain Not Fully Locked

S27 depends on:

```text
S26_FAST_MEAN_REVERSION
S07_FAMILY_EWMAC16_TREND_RULE
S13_RELATIVE_VOLATILITY_V_Q_M_ATTENUATION
```

S27 cannot be locked from Chapter 27 alone because the chapter is a delta over S26 plus additional safety mechanics.

### 4. Cross-Sleeve Combination Warning

Carver warns that fast mean reversion does not fit cleanly inside the daily Parts One through Three forecast-combination framework because of frequency, buffering, and execution differences.

Disposition:

```text
NO_DAILY_FORECAST_BLOCK_COMBINATION_FOR_S26_S27_WITHOUT_SEPARATE_GATE
```

### 5. Universe Specification Is Implicit

Chapters 26 and 27 score the rules at aggregate Jumbo level, but do not enumerate a per-instrument S26/S27 trading list. No local implementation may silently invent, drop, substitute, or reweight instruments.

Disposition:

```text
UNIVERSE_BLOCKED_UNTIL_ELIGIBILITY_AND_HOURLY_LIQUIDITY_RULES_LOCKED
```

## Immediate Next Step

The next step is source atom and synthetic conformance only:

```text
G_SYN_S26_S27_SOURCE_ATOM_LOCK_AND_SYNTHETIC_CONFORMANCE
```

This step must stop before:

- Databento access;
- Appendix C row access;
- NinjaTrader access;
- real OHLCV parsing;
- real forecasts;
- diagnostics;
- backtests;
- positions;
- costs;
- carry;
- trend-sleeve computation;
- risk calculations;
- OOS, Lockbox, Forward;
- deployment, trading, promotion;
- Git or remote operations.

## Standing Non-Authorization

This file authorizes no code edits beyond process documentation, no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts on real data, no positions, no costs, no carry, no trend computation on real data, no volatility/risk calculations on real data, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

# Carver S26/S27 Synthetic Conformance Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_S26_S27_SYNTHETIC_CONFORMANCE_GATE_DRAFT_NOT_DATA_NOT_BACKTEST
```

## Purpose

Define the next clean synthetic-only conformance gate for S26/S27 after the Opus source audit and source atom sheet.

Gate name:

```text
G_SYN_S26_S27_SOURCE_ATOM_LOCK_AND_SYNTHETIC_CONFORMANCE
```

This gate is designed to prove formula mechanics against deterministic hourly synthetic series only. The synthetic implementation result is recorded separately in `CARVER_S26_S27_SYNTHETIC_CONFORMANCE_IMPLEMENTATION_RESULT_2026-05-30.md`. This gate does not authorize real data, provider access, diagnostics, backtests, positions, costs, carry, trend sleeves, portfolio integration, deployment, trading, promotion, Git operations, or remote operations.

## Scope Boundary

Allowed in a later implementation gate:

- generated in-memory hourly synthetic price paths;
- deterministic synthetic volatility paths;
- deterministic synthetic trend paths;
- deterministic synthetic relative-volatility quantile paths;
- formula conformance tests for S26 and S27 only;
- structural assertions that FDM and buffering are absent.

Forbidden:

- Databento access;
- NinjaTrader access;
- Appendix C row access;
- local real OHLCV CSV reads;
- full-history archive reads;
- provider metadata reads;
- market-row parsing;
- diagnostics;
- backtests;
- real forecasts;
- positions;
- costs;
- carry;
- real trend computation;
- risk calculations on real data;
- OOS, Lockbox, Forward;
- CFD adapters;
- old QuantLab active-pipeline use;
- deployment, trading, promotion;
- Git or remote operations.

## Required Synthetic Surfaces

| Surface | Purpose | Must prove |
| --- | --- | --- |
| Mean-reverting hourly path | S26 equilibrium and raw forecast | EWMA(5), `equilibrium - price`, sign, magnitude |
| Constant-vol hourly path | S26 risk adjustment | `sigma_p_t = p_t * sigma_percent_t / 16` |
| Extreme raw-forecast path | S26 cap | hard cap at `[-20, +20]` |
| Uptrend/downtrend path | S27 EWMAC overlay | EWMAC(16,64) sign agrees with constructed trend |
| Relative-volatility path | S27 attenuation | `Q_t` and `M_t = EWMA_10(2 - 1.5 * Q_t)` behavior |
| Sign-combination table | S27 trend interaction | mean-reversion forecast does not oppose trend forecast |

## S26 Conformance Checks

The synthetic S26 tests must verify:

```text
S26_EWMA_5_EQUILIBRIUM_REPRODUCES_EXPECTED_VALUES
S26_RAW_FORECAST_EQUALS_EQUILIBRIUM_MINUS_PRICE
S26_RAW_FORECAST_SIGN_IS_CORRECT_FOR_ABOVE_BELOW_EQUILIBRIUM
S26_SIGMA_PRICE_EQUALS_PRICE_TIMES_SIGMA_PERCENT_DIVIDED_BY_16
S26_SCALED_FORECAST_EQUALS_RISK_ADJUSTED_FORECAST_TIMES_9_3
S26_CAP_SATURATES_AT_PLUS_20_AND_MINUS_20
S26_HAS_NO_FDM
S26_HAS_NO_BUFFERING
S26_SYNTHETIC_ONLY_NO_REAL_DATA_PATHS
```

## S27 Conformance Checks

The synthetic S27 tests must verify:

```text
S27_EWMAC_16_64_SIGN_MATCHES_CONSTRUCTED_TREND
S27_VOL_Q_IS_SYNTHETIC_QUANTILE_ONLY
S27_VOL_MULTIPLIER_USES_EWMA_10_OF_2_MINUS_1_5_TIMES_Q
S27_ADJUSTED_RAW_FORECAST_EQUALS_S26_RAW_TIMES_VOL_MULTIPLIER
S27_INHERITS_SCALAR_9_3
S27_INHERITS_CAP_PLUS_MINUS_20
S27_HAS_NO_FDM
S27_DOES_NOT_USE_DAILY_FORECAST_COMBINATION
```

The four required trend-interaction cases are:

| Mean-reversion sign | Trend sign | Expected S27 behavior |
| ---: | ---: | --- |
| Positive | Positive | Allow positive forecast |
| Negative | Negative | Allow negative forecast |
| Positive | Negative | Zero the mean-reversion forecast because it opposes trend |
| Negative | Positive | Zero the mean-reversion forecast because it opposes trend |

The locked synthetic convention is `ZERO_OPPOSING_MEAN_REVERSION_FORECAST`. It may not infer a position, trade, order type, or cost from the sign table.

## Exit Criteria

This gate can pass only if:

- every implemented formula has a source atom citation back to `CARVER_S26_S27_SOURCE_ATOM_SHEET_2026-05-30.md`;
- every test input is deterministic and synthetic;
- no code path opens Databento, NinjaTrader, Appendix C CSVs, full-history archives, provider metadata, or old QuantLab state;
- no diagnostics or backtests are run;
- no real-data forecast artifact is produced;
- no position, cost, carry, portfolio, or promotion artifact is produced;
- the local lean hostile audit records no blocking findings.

## First Real-Data Gate After This Gate

The first possible real-data gate remains blocked and separate:

```text
G_R1_SINGLE_INSTRUMENT_HOURLY_INTAKE_CONFORMANCE
```

Recommended source-aligned first S26 candidate:

```text
US 10-year Note future
```

Reason:

```text
Fig. 81 uses the US 10-year future example on p. 480.
```

Instrument guardrail:

```text
FIRST_S26_REAL_DATA_INSTRUMENT_ANCHOR: BOOK_US_10_YEAR_FUTURE_FIG_81
EXPECTED_APPENDIX_C_IDENTITY_PATH: US_10_YEAR / ZN AFTER SEPARATE LOCK
FORBIDDEN_SUBSTITUTES: ZT, T_BILLS, 2_YEAR_TREASURY_NOTES, 16_SYMBOL_PILOT_CONVENIENCE_ROWS, ADJACENT_TREASURY_RATE_SUBSTITUTES
S27_SP500_MES_NATIVE_WORKED_EXAMPLE_LOCK: NOT_LOCKED_FROM_CHAPTER_27
```

This future gate must use hourly bars, not the current daily Appendix C foundation, and requires a fresh explicit authorization. S27 may only reuse this surface as an inherited S26 single-instrument overlay check; it must not be described as S27's native SP500/MES surface unless a separate source atom lock proves that from the book.

## Standing Non-Authorization

This file authorizes no provider API access, no data download, no market-row parsing, no code implementation by itself, no tests by itself, no diagnostics, no backtests, no real-data forecasts, no positions, no costs, no carry, no trend computation on real data, no volatility/risk calculations on real data, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

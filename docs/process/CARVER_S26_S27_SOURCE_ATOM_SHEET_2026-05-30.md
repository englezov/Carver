# Carver S26/S27 Source Atom Sheet

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_S26_S27_SOURCE_ATOM_SHEET_NOT_DATA_NOT_IMPLEMENTATION_NOT_BACKTEST
```

## Purpose

Lock the source atoms for Carver Strategies 26 and 27 before any synthetic implementation or real-data gate.

Source authority:

```text
00_Carver.pdf
```

This atom sheet records the Opus-verified source path. It is not a code specification, data authorization, diagnostic authorization, backtest authorization, strategy-readiness claim, or promotion claim.

## Source Locations

| Item | Source location |
| --- | --- |
| Part Four framing | p. 475 |
| S26 title | "Strategy twenty-six: Fast mean reversion", Chapter 26, pp. 476-489 body |
| S27 title | "Strategy twenty-seven: Safer fast mean reversion", Chapter 27, pp. 499-509 |
| Fig. 81 | p. 480 |
| Table 131 | p. 491 |
| Fig. 82 | p. 494 |
| Table 132 | p. 503 |
| Table 133 | p. 503 |
| Table 134 | p. 504 |
| Fig. 83 | p. 506 |
| Table 135 | p. 507 |

## Shared Part Four Frame

| Atom | Locked value | Source |
| --- | --- | --- |
| Lane class | `SOURCE_NATIVE_FUTURES` | Workspace governance |
| Forecast frequency | Hourly, not daily | p. 475 |
| First real-data implication | Existing daily `ohlcv-1d` foundation is not sufficient | Opus audit result |
| Portfolio-combination posture | Fast strategies sit outside the daily buffered forecast-combination path unless separately gated | Ch. 26/27 transition material |
| First S26 real-data instrument anchor | Book worked example: US 10-year future from Fig. 81 | p. 480 |
| S27 instrument-specific worked example | No separate S27-native instrument example locked from pp. 499-509; S27 is presented as deltas over S26 plus aggregate/asset-class results | pp. 499-509 |

The first S26 real-data gate must be sourced from the book's worked example. It must not use `ZT`, T-bills, 2-year Treasury notes, the 16-symbol daily pilot convenience set, or any adjacent Treasury-rate substitute unless a later source-faithful gate proves that substitution directly from the book and provider evidence.

S27 does not currently have a separate source-native SP500/MES worked-example anchor in this chapter. A first S27 single-instrument overlay check may reuse the S26 US 10-year worked-example surface only as an inherited S26 test surface, not as a claim that S27 is natively a US 10-year-only strategy. A source-faithful S27 aggregate reproduction remains a later eligible-Jumbo/instrument-universe gate.

## S26 Fast Mean-Reversion Atoms

| Atom | Locked value | Source |
| --- | --- | --- |
| Strategy ID | S26 | Ch. 26 |
| Book heading | Strategy twenty-six: Fast mean reversion | p. 476 |
| Classification | `STANDALONE_CANDIDATE` for rule research; `SOURCE_NATIVE_PORTFOLIO_SLEEVE` for book aggregate performance | Opus audit |
| Source data frequency | Hourly | pp. 475, 478 |
| Equilibrium | EWMA over price with span 5 | p. 479 |
| Raw forecast | `equilibrium - p_t` | p. 480 |
| Price-risk adjustment | `raw_forecast / sigma_p_t` | Ch. 26 risk-adjusted forecast block |
| sigma price relation | `sigma_p_t = p_t * sigma_percent_t / 16` | Ch. 26 risk-adjusted forecast block |
| Forecast scalar | `9.3` | p. 480 |
| Forecast cap | `[-20, +20]` | p. 480 |
| FDM | None. Single rule. | Ch. 26 |
| Buffering | None for S26 fast strategy path | p. 481 |
| Execution note | Limit orders are part of the source execution discussion | p. 481 |
| Holding period context | Approximately one or two days | pp. 476-478 |
| Turnover context | Around 140/year for S26 | p. 481 context |
| Risk target in worked example | 20% | p. 480 |

S26 formula skeleton:

```text
equilibrium_t = EWMA_span_5(price_t)
raw_forecast_t = equilibrium_t - price_t
risk_adjusted_forecast_t = raw_forecast_t / sigma_p_t
scaled_forecast_t = risk_adjusted_forecast_t * 9.3
capped_forecast_t = max(min(scaled_forecast_t, 20), -20)
```

## S27 Safer Fast Mean-Reversion Atoms

| Atom | Locked value | Source |
| --- | --- | --- |
| Strategy ID | S27 | Ch. 27 |
| Book heading | Strategy twenty-seven: Safer fast mean reversion | p. 499 |
| Classification | `STANDALONE_CANDIDATE_WITH_DEPENDENCIES` for rule research; `SOURCE_NATIVE_PORTFOLIO_SLEEVE` for book aggregate performance | Opus audit |
| Base dependency | S26 in full | p. 508 |
| Trend dependency | EWMAC(16,64), shorthand EWMAC16 | p. 500 |
| Trend role | Overlay/condition; not a co-weighted forecast block | pp. 500, 508 |
| Trend interaction | Mean-reversion forecast must not oppose the trend forecast | p. 508 |
| Volatility attenuation dependency | Relative volatility `V`, quantile `Q`, multiplier `M` from S13-family mechanism | p. 501-502; S13 p. 301 context |
| Vol attenuation formula | `M_i_t = EWMA_span_10(2 - 1.5 * Q_i_t)` | p. 501-502 |
| Adjusted raw forecast | `raw_forecast_i_t * M_i_t` before inherited S26 later stages | p. 501-502 |
| Forecast scalar | Around `20` after the S27 trend overlay and volatility multiplier | p. 502 |
| Forecast cap | Inherits `[-20, +20]` from S26 | p. 508 |
| FDM | None inside S27 fast rule. Do not introduce daily forecast-combination FDM. | Opus audit |

S27 formula skeleton:

```text
s26_raw_forecast_t = equilibrium_t - price_t
trend_forecast_t = EWMAC(16, 64) trend forecast
vol_multiplier_t = EWMA_span_10(2 - 1.5 * Q_t)
adjusted_raw_forecast_t = s26_raw_forecast_t * vol_multiplier_t
only_allow_adjusted_raw_forecast_if_it_does_not_oppose_trend_forecast
risk_adjusted_forecast_t = adjusted_raw_forecast_t / sigma_p_t
scaled_forecast_t = risk_adjusted_forecast_t * 20
capped_forecast_t = max(min(scaled_forecast_t, 20), -20)
```

## Dependencies To Preserve

S27 cannot be locked without these atom families:

```text
S26_FAST_MEAN_REVERSION
S07_FAMILY_EWMAC16_TREND_RULE
S13_RELATIVE_VOLATILITY_V_Q_M_ATTENUATION
```

S26/S27 cannot proceed to real data without:

```text
HOURLY_COMPLETED_BAR_INTAKE
HOURLY_SESSION_AND_TIMESTAMP_POLICY
HOURLY_CONTINUOUS_CONTRACT_ROLL_AND_BACK_ADJUSTMENT_POLICY
HOURLY_SIGMA_PERCENT_ESTIMATION_LOCK
HOURLY_COST_AND_LIQUIDITY_ELIGIBILITY_LOCK
S26_BOOK_WORKED_EXAMPLE_US_10_YEAR_FUTURE_IDENTITY_LOCK
S27_INSTRUMENT_UNIVERSE_OR_INHERITED_SINGLE_INSTRUMENT_TEST_SURFACE_DECISION_LOCK
```

## Explicitly Blocked By This Atom Sheet

```text
NO_DAILY_OHLCV_SUBSTITUTION_FOR_HOURLY_SOURCE_REQUIREMENT
NO_APPENDIX_C_DAILY_ROW_USAGE_FOR_S26_S27_FORECASTS
NO_DATABENTO_PROVIDER_CALL
NO_NINJATRADER_PATH
NO_REAL_SIGMA_PERCENT_ESTIMATION
NO_REAL_EWMAC_TREND_COMPUTATION
NO_REAL_VOL_ATTENUATION_COMPUTATION
NO_POSITIONS
NO_COSTS
NO_BACKTEST
NO_DIAGNOSTIC
NO_PORTFOLIO_INTEGRATION
NO_ZT_TBILL_2_YEAR_OR_ADJACENT_TREASURY_SUBSTITUTE_FOR_THE_S26_BOOK_US_10_YEAR_EXAMPLE
NO_SP500_OR_MES_CLAIM_AS_S27_NATIVE_WORKED_EXAMPLE_WITHOUT_SEPARATE_SOURCE_ATOM
NO_GIT_OR_REMOTE_OPERATIONS
```

## Unresolved Production Atoms

- Hourly Databento or other provider intake is not certified.
- The first S26 real-data instrument must be the source-native US 10-year future from the book's Fig. 81 example, expected to map through the Appendix C US 10-year/`ZN` identity path after static and hourly-data readiness are separately locked.
- S27 has no separate SP500/MES native worked-example lock in the current source atoms; using SP500/MES for S27 requires a separate source-faithful instrument/universe gate.
- `APPENDIX_C_181_001 / ALI / Aluminium` remains fail-closed in the daily foundation.
- Thirty-six Appendix C rows remain outside the 66-row identity-hardened set.
- S27 dependency atoms from S7 and S13 require their own source locks before real-data work.
- S27 scalar handling was corrected on 2026-05-31: p. 502 states the trend overlay requires a higher forecast scalar, estimated around 20. Do not use the S26 scalar `9.3` for S27.
- The exact S26/S27 eligible instrument universe is not enumerated by the book.
- Hourly liquidity and cost eligibility rules remain unresolved.
- Hourly `sigma_percent_t` estimation details require separate lock before real-data computation.
- Cross-sleeve combination with daily Parts One through Three remains blocked.

## Standing Non-Authorization

This file authorizes no provider API access, no data download, no market-row parsing, no implementation, no synthetic test execution by itself, no diagnostics, no backtests, no real-data forecasts, no positions, no costs, no carry, no trend computation on real data, no volatility/risk calculations on real data, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

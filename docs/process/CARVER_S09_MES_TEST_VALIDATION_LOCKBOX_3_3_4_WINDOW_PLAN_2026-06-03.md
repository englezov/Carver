# S09 MES TEST VALIDATION LOCKBOX 3:3:4 Window Plan

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_TEST_VALIDATION_LOCKBOX_3_3_4_WINDOW_PLAN_NOT_DATA_NOT_BACKTEST
```

## Scope

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: ohlcv-1d
- total_observed_provider_completed_dates: 2203
- machinery_development_slice: 2019-05-05 through 2020-04-05
- machinery_development_slice_completed_dates: 289
- remaining_scored_pool_completed_dates: 1914
- split_ratio: 3:3:4

The machinery-development slice is an oldest-first construction slice and is
not scored evidence. Stage data must be downloaded separately only when that stage is reached and authorized.

## Locked Window Allocation

TEST completed dates: 574

TEST window: 2020-04-06 through 2022-02-08

VALIDATION completed dates: 574

VALIDATION window: 2022-02-09 through 2023-12-13

LOCKBOX completed dates: 766

LOCKBOX window: 2023-12-14 through 2026-05-29

## Trade Sample Rationale

The 3:3:4 split implements the operator target ratio:

- TEST: minimum 100 trades, ideal 150 trades.
- VALIDATION: minimum 100 trades, ideal 150 trades.
- LOCKBOX: minimum 150 trades, ideal 200 trades.

The date allocation does not guarantee realized trade counts. Each stage must
fail closed if the downloaded, completed-bar, source-native rows do not match
the locked date-count budget or if the strategy's realized trade count is below
the stage's predeclared minimum.

## Stage Gates

TEST access remains separately gated.

VALIDATION access remains separately gated.

Lockbox access remains separately gated.

The Lockbox span is longer than two calendar years and therefore requires explicit operator authorization before any Lockbox diagnostic or backtest.

Each future stage download must confirm:

- source-native MES dated-contract rows only;
- completed bars only;
- no CFD adapter substitution;
- no old QuantLab active-pipeline state;
- exact stage date boundaries and completed-date counts;
- no post-result tuning of parameters, thresholds, filters, exits, symbols, costs, or windows.

## Boundary

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations are authorized by this plan.

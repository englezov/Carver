# Carver Mean Reversion Prior Failure Interpretation Record

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_MEAN_REVERSION_PRIOR_FAILURE_INTERPRETATION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the operator interpretation of prior mean-reversion rejection history before any future clean Carver source-native futures candidate work.

This record preserves the distinction between:

- a source-native futures strategy failure;
- a failed or obsolete test design;
- insufficient test resolution for the question being asked;
- a CFD adapter or contaminated process failure.

## Interpretation

Prior mean-reversion rejection is classified as:

```text
TEST_DESIGN_FAILURE_NOT_STRATEGY_FAILURE
```

and/or:

```text
TEST_RESOLUTION_FAILURE_NOT_STRATEGY_FAILURE
```

and/or:

```text
ADAPTER_OR_PROCESS_FAILURE_NOT_SOURCE_NATIVE_STRATEGY_DEATH
```

The prior rejection does not constitute evidence that a source-native futures mean-reversion strategy failed.

## Rationale

Carver discovery is source-native futures first.

A prior failed CFD adapter, broker-venue translation, stale statistical-robustness gate, obsolete process rule, contaminated QuantLab workflow, or mismatched test design can reject the test setup without rejecting the book-native or source-native hypothesis.

The prior four-window test design, with roughly 30 trades per window, was too coarse to adjudicate the mean-reversion hypothesis it attempted to answer. That design may record that the test framing was inconclusive or under-resolved, but it may not be promoted into a strategy-failure conclusion.

Such history may remain useful as a caution record, but it is not active authority for blocking a clean Carver source-native futures candidate.

## Future Mean-Reversion Eligibility

Mean reversion remains eligible for a future clean Carver source-native futures candidate brief if separately authorized.

Any future mean-reversion candidate must:

- declare its lane before data work;
- prefer source-native futures interpretation where the source supports it;
- lock instrument, bar, session, roll, cost, and evidence-window assumptions before computation;
- avoid old CFD broker-clock assumptions, old adapter code, old QuantLab data-prep scripts, and stale pipeline state;
- treat prior CFD or obsolete-test failures as historical context only;
- avoid tuning parameters, thresholds, filters, exits, symbols, costs, or windows after seeing results.

## Non-Authorization

This record authorizes no code edits, no tests, no real data, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

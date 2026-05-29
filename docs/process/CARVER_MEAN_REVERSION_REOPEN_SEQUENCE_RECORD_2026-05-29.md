# Carver Mean Reversion Reopen Sequence Record

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_MEAN_REVERSION_REOPEN_SEQUENCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the preferred Carver sequencing for future mean-reversion work while preserving the current Part One portfolio build as the near-term priority.

This is a process-only sequencing record. It does not authorize implementation, testing, data access, diagnostics, backtests, portfolio computation, or adapter work.

## Mean-Reversion Standing

Mean reversion remains a future reopenable source-native futures standalone candidate.

Prior rejection history remains classified under:

```text
TEST_DESIGN_FAILURE_NOT_STRATEGY_FAILURE
TEST_RESOLUTION_FAILURE_NOT_STRATEGY_FAILURE
ADAPTER_OR_PROCESS_FAILURE_NOT_SOURCE_NATIVE_STRATEGY_DEATH
```

Those labels preserve the candidate from being blocked by an obsolete test design, insufficient test resolution, CFD adapter failure, or contaminated process failure.

## Preferred Near-Term Sequence

The preferred near-term sequence is to finish the core Part One portfolio graph before opening mean-reversion implementation or testing:

```text
S11 combined carry/trend process gate
-> P05/P06/P07 portfolio shape or readiness gates as appropriate
-> later separately authorized mean-reversion candidate gate
```

This sequence keeps the Carver spine focused on the source-native daily forecast and portfolio machinery already in progress before entering the separate fast-stack or mean-reversion path.

## Mean-Reversion Reopen Boundary

When reopened, mean reversion must be treated as a clean Carver source-native futures candidate, not as a rescue of old QuantLab or CFD-adapter work.

Any future mean-reversion gate must separately lock:

- lane classification;
- source chapter and candidate framing;
- instrument and market family;
- bar timeframe and completed-bar semantics;
- session, roll, cost, and data-source rules;
- evaluation question and evidence-window design;
- failure-interpretation rules before results are known.

No prior CFD adapter failure, obsolete robustness gate, or under-resolved window split may be used as source-native strategy death.

## Non-Authorization

This record authorizes no code edits, no tests, no real data, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

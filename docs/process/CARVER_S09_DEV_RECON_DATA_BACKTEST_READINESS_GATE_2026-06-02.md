# Carver S09 Development/Reconciliation Data And Backtest Readiness Gate

Date: 2026-06-02

Status:

```text
PROCESS_ONLY_S09_DEV_RECON_DATA_BACKTEST_READINESS_GATE_NOT_DATA_NOT_BACKTEST
```

## Purpose

Define the next clean gate after S09 source-atom and synthetic conformance:

```text
S09_DEV_RECON_DAILY_SINGLE_INSTRUMENT_DATA_AND_BACKTEST_READINESS
```

This gate prepares the path toward a later separately authorized S09 Development/Reconciliation backtest. It does not open data access, market-row parsing, forecast computation on real rows, diagnostics, backtests, positions, costs, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Prior Gate Status

S09 source atoms and synthetic conformance are closed for the current scope:

```text
docs/process/CARVER_S09_SOURCE_ATOM_LOCK_AND_SYNTHETIC_CONFORMANCE_GATE_2026-06-02.md
docs/process/CARVER_S09_SOURCE_ATOM_LOCK_AND_SYNTHETIC_CONFORMANCE_LOCAL_HOSTILE_AUDIT_2026-06-02.md

AUDIT_DISPOSITION: PASS_SYNTHETIC_CONFORMANCE_REAUDIT_CLOSED
```

Synthetic verification:

```text
python -m unittest tests.test_s09_full_source_atom_synthetic tests.test_s09_m2_synthetic tests.test_s09_phase1_synthetic tests.test_s09_readiness_synthetic tests.test_s09_zn_package_synthetic
Ran 35 tests - OK
```

## Lane Declaration

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened.

## Preferred First Candidate Family

Because the operator wants to explore whether S09 trend following can work on indices, the preferred first S09 single-instrument candidate family is the source-native Appendix C / Databento-supported US equity index futures subset:

```text
MES  - S&P 500 micro
MNQ  - Nasdaq 100 micro
M2K  - Russell 2000 micro
MYM  - Dow micro
```

The first executable backtest gate should choose exactly one root from this family, preferably `MES`, unless a preflight artifact proves another root has stronger continuous-lineage readiness.

`ES` or `NQ` may not silently substitute for `MES` or `MNQ`. Full-size signal lanes require a separate source-native signal/execution-lane decision.

## Existing Data Foundation Evidence

The daily data foundation currently supports only Development/Reconciliation readiness, not strategy readiness:

```text
docs/process/CARVER_APPENDIX_C_DAILY_DATA_FOUNDATION_AND_OPUS_HANDOFF_CLOSEOUT_2026-05-30.md
FINAL_DEV_RECON_DATA_READY_ROWS: 65
FINAL_FAIL_CLOSED_ROW: APPENDIX_C_181_001 / ALI / Aluminium
YES_DEV_RECON_DATA_READY_NOT_STRATEGY_READY
```

The 16-symbol daily library is a useful candidate source but remains non-strategy by itself:

```text
docs/process/CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_PROMOTION_READINESS_CHAPTER_CLOSEOUT_2026-05-30.md
MANIFEST_ROWS: 16
ARCHIVE_ROWS: 4568
NORMAL_PROVIDER_CONDITION_CANDIDATE_ROWS: 4483
DEGRADED_QUARANTINED_ROWS: 85
PASS_16_SYMBOL_DAILY_DATA_LIBRARY_PROMOTION_READINESS_NOT_DIAGNOSTIC_NOT_BACKTEST
```

The 16-symbol local continuous daily lineage rerun cleared adjacent-pair availability but failed closed before continuous construction because lifecycle evidence was not locked:

```text
docs/process/CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_LINEAGE_RERUN_AFTER_ROLL_CHAIN_EXPANSION_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md
AUDIT_DISPOSITION: PASS_FAIL_CLOSED_AFTER_ROLL_CHAIN_EXPANSION_ORIGINAL_ADJACENT_CONTRACT_BLOCKER_CLEARED_LIFECYCLE_EVIDENCE_GATE_REQUIRED_SCOPE
```

Therefore S09 cannot yet treat the 16-symbol library as a strategy-facing continuous input.

## Required Locks Before Real-Data Forecast Or Backtest

For the selected single root, a later execution gate must lock or fail-close all of:

1. Appendix C source identity and Databento/provider identity.
2. Exact source-native root and dated-contract chain over the requested window.
3. Completed daily bar policy, timestamp policy, publisher-condition policy, and degraded-row exclusion.
4. Local continuous daily lineage from dated-contract rows.
5. Official or otherwise pre-authorized lifecycle evidence for roll blockers.
6. Deterministic roll rule and additive back-adjustment ledger.
7. S09 EWMAC input series: adjusted close for forecast, raw/current price source for sizing if positions are opened later.
8. Daily price risk source, timestamp alignment, and warm-up policy.
9. Cost source and risk-adjusted cost calculation.
10. S09 speed/cost eligibility rule, including the `0.15` SR threshold as a machine-readable lock.
11. Buffering and trade/no-trade rule inherited from S08/S09 before any position backtest.
12. Backtest window label and evidence budget.

## Backtest-Readiness Boundary

This gate prepares a later backtest authorization but does not itself authorize one.

A later S09 Dev/Reconciliation backtest gate must specify:

```text
selected_root: EXACTLY_ONE_OF(MES, MNQ, M2K, MYM) unless separately justified
lane: SOURCE_NATIVE_FUTURES
window: <= 2 years unless separately operator-approved
frequency: daily completed bars
strategy: S09 multiple trend following
outputs: forecast, position, returns, cost, and PnL only if explicitly authorized
labels: DEVELOPMENT_RECONCILIATION_ONLY_NOT_TEST_NOT_VALIDATION_NOT_LOCKBOX_NOT_PROMOTION
```

No TEST, VALIDATION, Lockbox, Forward, or promotion surface is opened by this gate.

## Fail-Closed Rules

The later execution path must fail closed if:

- the selected root is not in the locked source-native candidate set;
- any contract-chain row is missing without a source-approved explanation;
- degraded provider-condition rows fall inside the strategy-facing window and no predeclared exclusion/retarget rule exists;
- lifecycle evidence is missing for any roll transition;
- continuous lineage cannot be hash-bound from dated source rows;
- daily price risk or cost evidence is unresolved;
- the speed/cost eligibility row set is not machine-locked before viewing results;
- any signal/execution substitution is proposed after seeing results;
- any CFD or old QuantLab assumption is introduced.

## Recommended Next Gate

The next clean step is:

```text
S09_SINGLE_INDEX_ROOT_CONTINUOUS_LINEAGE_AND_COST_ELIGIBILITY_PREFLIGHT
```

Scope of that future gate:

- choose exactly one index root, preferably `MES`;
- inspect only existing local process/source artifacts unless provider access is separately authorized;
- determine whether existing local daily data can support a 2-year Development/Reconciliation backtest window;
- identify the exact additional data/lifecycle/cost evidence required;
- stop before market-row parsing and before any forecast on real data.

## Non-Authorization

This gate authorizes no provider API access, no new data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no costs, no carry, no CFD adapter work, no old QuantLab pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update, and no remote operations.


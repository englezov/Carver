# Carver Lean Implementation And Backtest Deferral Rule

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_LEAN_IMPLEMENTATION_BACKTEST_DEFERRAL_RULE_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

This rule defines the lean working posture after accepting the Carver source-native translation architecture goal.

The project should now move toward implementation readiness, but not by rushing into historical backtesting. A source/process brief must be locked first, and implementation work still requires its own separate explicit implementation authorization. Once authorized, implementation must first prove mechanical and source-conformance correctness.

## Core Rule

Backtesting is deferred until the relevant machinery fits together.

The allowed implementation ladder is:

```text
source/process brief
-> separate implementation authorization
-> formula/module implementation
-> synthetic conformance tests
-> source-example conformance checks where the book provides numeric examples
-> dry-run pipeline/schema checks on synthetic data
-> separate operator authorization for any historical diagnostic or backtest
```

Historical data is not needed to prove that the code follows the rule. Historical data is needed only later to evaluate behavior under a locked evidence window.

## What Counts As Implementation Testing

The following are allowed only when explicitly authorized by a future implementation brief:

- Unit tests on formulas using tiny synthetic arrays.
- Golden toy examples written by hand.
- Invariant tests, including no lookahead, completed bars only, forecast caps, fail-closed missing inputs, and source-native lane guards.
- Book example conformance checks when the book gives enough numeric detail.
- Dry-run pipeline checks on synthetic data only.

These tests are not alpha evidence, not diagnostics, not historical backtests, not TEST, not VALIDATION, not OOS, not Lockbox, and not Forward.

## What Is Still Deferred

The following remain forbidden without separate explicit operator authorization:

- Market-row parsing.
- Historical diagnostics.
- Historical backtests.
- Any diagnostic or backtest over 2 years.
- OOS, Lockbox, or Forward access.
- CFD adapter execution.
- Deployment, trading, or promotion.
- Any tuning after results.

## Prior Backtest Context

The two prior futures-native backtests are accepted only as parked operator memory for the lesson:

```text
NON_POSITIVE_STANDALONE_DOES_NOT_ADVANCE
```

They are not promotion evidence, not source authority for the clean Carver workspace, and not permission to tune, rescue, or import old pipeline state. If they are ever cited beyond this general lesson, they must first be named or hash-bound in a separate process-only archaeology memo.

Interpretation rule:

- A non-positive standalone candidate does not advance.
- A non-positive sleeve in standalone isolation is not family death if the book frames it as portfolio material.
- A portfolio-only component is judged only in its proper portfolio context.
- A parked/not-standalone strategy is not failed alpha.

## Hostile Audit Rule

Any process artifact, candidate brief, portfolio brief, implementation attestation, diagnostic result, backtest result, or gate memo that may influence a lane decision must receive a hostile audit before it is treated as locked.

Required hostile-audit method:

```text
USE_SUBAGENT_FOR_HOSTILE_AUDIT
```

Hostile audits must use a subagent unless the operator explicitly waives that requirement for a specific artifact.

The hostile audit must look for:

- Governance conflicts.
- Stage-transition leakage.
- Data access or backtest leakage.
- OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion leakage.
- Page-reference or source-faithfulness errors.
- Standalone versus sleeve/portfolio misclassification.
- Tuning-after-results risk.
- Old QuantLab_v3 contamination.
- Missing unresolved atoms.

The audit itself is process-only unless separately authorized otherwise.

## NinjaTrader Note

NinjaTrader is not required for M0, source/process briefs, architecture records, or synthetic implementation tests.

NinjaTrader may become relevant only if a future explicitly authorized source-native futures data lane requires NinjaTrader-hosted futures data or export. At that point, the need must be recorded in a separate data-surface or source-native data-lane gate memo before any subscription, export, parsing, diagnostic, or backtest work.

No NinjaTrader brokerage connection, order-routing setup, account file handling, credential handling, live trading configuration, or broker/account integration is authorized by this note.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

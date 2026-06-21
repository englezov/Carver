# Carver S27 GPT 5.5 Extended Pro Source-Faithfulness Audit Result

Date: 2026-06-05

Status:

```text
FAIL_CLOSED_CURRENT_S27_RESULTS_NOT_BOOK_FAITHFUL_BACKTEST_EVIDENCE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

External hostile audit by GPT 5.5 Extended Pro over Strategy 27 source
faithfulness, GitHub visibility, handoff packet reproducibility, corrected
runner machinery, and old-versus-corrected result interpretation.

The audit treated `Carver.pdf` as controlling source authority.

## High-Level Disposition

The audit does not support treating any current S27 ZN result as alpha,
promotion, OOS, Lockbox, Forward, deployment, or trading evidence.

The audit separates three categories:

- old S27 results: invalid as source-faithful S27 evidence;
- corrected S27 results: unresolved as arithmetic artifacts and not credible
  as book-faithful execution backtests;
- corrected signal formula: directionally source-faithful only conditional on
  independently verified runtime ledgers.

## Critical Findings Recorded

1. The corrected 2026-06-04 machinery was not visible on GitHub `master` during
   the audit, so repository-level stale-path replacement was not established.
2. The GPT handoff packet was incomplete for mechanical replay because it did
   not include the local daily-runtime builder and the full row artifacts needed
   to recompute corrected outputs end to end.
3. The corrected "full ladder" label is not book-source-faithful. The audited
   runners model target-position close-to-close PnL with per-side fees, not the
   Carver limit-order ladder with working orders, one-hour-lag fill logic,
   market-order handling, and spread costs.
4. Cost accounting is not book-source-faithful. Current corrected artifacts use
   no-cost unit plumbing or ETF/public per-side commission only, while spread,
   slippage, market-order costs, and futures-realistic cost readiness remain
   unresolved or fail-closed.

## High Findings Recorded

- The row-level S27 forecast formula is directionally aligned with the book only
  if the runtime ledgers are correct; the current validators do not independently
  recompute EWMA5, EWMAC16/64, sigma, V/Q/M, or strict-prior alignment.
- Provider-condition fail-closed handling is runner-local, not a universal core
  invariant.
- Some readiness/status gates can appear green while still carrying stale
  executable replacement risk.
- Old S27 results are diagnostic or stale and are not source-faithful S27
  backtest evidence.

## Required Next Gates

Before any S27 result can be described as a book-faithful backtest, Carver must
open and pass separate gates for:

1. GitHub/repo reproducibility of the corrected machinery and artifact snapshot.
2. Deterministic no-provider replay from raw/local row artifacts through
   runtime ledgers, forecasts, positions, orders/fills, costs, and PnL.
3. Book-faithful S26/S27 execution machinery, including limit-order ladder
   state, one-hour-lag fill logic, market-order handling, commission, and spread
   treatment.
4. Row-level runtime recomputation audit for EWMA5 equilibrium, EWMAC16/64
   trend, sigma bridge, V/Q/M, and strict-prior completed-bar alignment.
5. Data-lineage audit covering provider condition, raw rows, continuous roll,
   inactive row exclusion, additive adjustments, missing/degraded rows,
   duplicate rows, and next-bar PnL masks.

## Current Evidence Boundary

Current corrected S27 ZN artifacts may be used only as diagnostic machinery
evidence and failure-map material.

They must not be labeled as:

```text
BOOK_FAITHFUL_S27_BACKTEST
SOURCE_FAITHFUL_FULL_LADDER
ALPHA
PROMOTION
OOS
LOCKBOX
FORWARD
DEPLOYMENT
TRADING
```

## Non-Authorization

This audit record authorizes no provider API access, no data download, no
market-row parsing, no diagnostic, no backtest, no OOS, no Lockbox, no Forward,
no tuning, no deployment, no trading, no promotion, no Git staging, no commit,
no push, no PR update, and no remote operation.

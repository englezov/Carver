# Carver S27 Opus 4.8 Max Source-Faithfulness Audit Result

Date: 2026-06-05

Status:

```text
FAIL_CLOSED_S27_NOT_YET_REPRODUCIBLE_OR_BOOK_FAITHFUL_BACKTEST_EVIDENCE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

External hostile audit by Opus 4.8 Max over Strategy 27 source faithfulness,
GitHub reproducibility, handoff packet completeness, corrected runner
machinery, and old-versus-corrected result interpretation.

The audit treated `Carver.pdf` as controlling source authority.

## High-Level Disposition

Opus independently agrees that no current S27 result should be treated as
alpha, promotion, OOS, Lockbox, Forward, deployment, or trading evidence.

It classifies:

- old positive S27 results as not admissible source-faithful evidence;
- corrected negative/collapsed S27 results as unresolved and not valid evidence
  that book-faithful S27 fails;
- visible signal algebra as broadly source-faithful, while surrounding runtime,
  data, execution, cost, scalar, and reproducibility questions remain blocking.

## Critical Findings Recorded

1. S27 machinery and results were absent from GitHub `master` during the audit,
   so repository reproducibility was not established.
2. The handoff packet was non-executable against the repository and did not
   include every local dependency needed for end-to-end replay.
3. The no-lookahead proof for sigma and V/Q/M depends on runtime values computed
   outside the packet; date-label checks alone do not prove in-value
   no-lookahead.
4. The headline old-versus-corrected 2024 collapse was not reproducible from the
   four-file Opus packet.

## High Findings Recorded

- Daily equilibrium and hourly current-price series may be built from separate
  continuous/back-adjusted constructions, creating possible additive-level
  mismatch in `equilibrium - price`.
- Execution and cost mechanics are not book-source-faithful. The current
  diagnostic runners use close-to-close target-position PnL and per-side fee
  treatment, not the book's limit-order execution machinery.
- Opus flagged a potential scalar error: the local spine currently defines
  `S26_FORECAST_SCALAR = 9.3` and `S27_FORECAST_SCALAR = 20.0`, while Opus's
  reading of the book says S27 should proceed with the S26 scalar after the
  trend and volatility overlays.
- The old 2024 positive result used live/provider-capable pre-correction
  machinery and is not admissible validation evidence.

## Medium Findings Recorded

- V/Q/M definition and windowing require direct source-faithfulness verification
  from the local builder and row artifacts.
- The ten-day stale-runtime tolerance may be too loose for an hourly fast mean
  reversion strategy.
- The 2025-2026 corrected TEST_3 run reused touched daily runtime material as
  the close source, so it is not pristine evidence.
- Capital, target risk, IDM, and weight constants in diagnostic runners are
  plumbing choices unless separately book-locked.

## Local Clarification After Audit

After receiving the audit, local inspection found:

```text
src/carver/spine/s26_s27.py:
S26_FORECAST_SCALAR = 9.3
S27_FORECAST_SCALAR = 20.0
```

and the local V/Q/M builder exists at:

```text
tools/databento/carver_s27_zn_local_extended_daily_runtime_2022_2023.py
```

The builder uses:

```text
TEN_YEAR_SIGMA_ROWS = 2560
VQM_EWMA_SPAN = 10
```

and appends historical relative-volatility observations before computing the
current quantile. These local facts reduce some handoff-packet uncertainty but
do not close the book-source-faithfulness blockers without a dedicated row-level
replay audit and a direct scalar/source decision.

## Required Next Gates

Before any S27 result can be described as a book-faithful backtest, Carver must:

1. Decide and source-lock the S27 forecast scalar from `Carver.pdf`.
2. Prove the daily equilibrium close and hourly current price share one
   compatible back-adjusted price level for every forecast row.
3. Prove sigma, ten-year V/Q/M, and quantile rows are computed strictly from
   admissible prior/current history according to the book.
4. Replace target-position close-to-close diagnostic PnL with book-faithful
   S26/S27 execution machinery or explicitly relabel current outputs as
   non-book-faithful diagnostics.
5. Build a deterministic no-provider replay packet with raw/local rows, runtime
   ledgers, forecast rows, order/fill rows, cost rows, PnL rows, and hashes.
6. Commit or otherwise make the corrected machinery and replay dependencies
   visible to the external GitHub-connected auditors before asking for
   repository-level reproducibility claims.

## Current Evidence Boundary

Current S27 artifacts are diagnostic and failure-map material only.

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

# CARVER S27 ZN V2 Pre-Run GPT 5.5 Machinery Audit Result

Date: 2026-06-11

Status: EXTERNAL_GPT55_PRE_RUN_MACHINERY_AUDIT_FAIL_RUN_NOT_AUTHORIZED

This record captures the GPT 5.5 Extended Pro pre-run hostile machinery audit
after the scoped GitHub push at commit
`9850bf41492d90a5c46a03b367fa8ba3268bea1e`.

The audit used GitHub access to inspect branch
`codex/carver-strategy-portfolio-opus-checkpoint`. Direct `Carver.pdf` access
was unavailable in that chat, so direct book verification remained
`UNKNOWN / FAIL_CLOSED`; the audit relied on the repo source-lock and process
records for book interpretation.

## Verdict

`FAIL`

The pushed repository contains the S27_V2 positive-action machinery checkpoint
through actual-PnL closure, and the inspected S27_V2 surfaces remain strongly
fail-closed for provider/API/download/OOS/Lockbox/Forward/result/tuning/adapter/
deployment/trading/promotion paths.

The checkpoint is not ready for a controlled local-only development backtest run
because it is hard-bound to one audited ZNM6 positive-action
Development/Reconciliation row and does not implement or prove a generalized
multi-row controlled development backtest runner.

## Blocking Findings

### P1-1 - Generalized Multi-Row Runner Missing

No generalized multi-row controlled local-only development backtest runner is
implemented/proven. The next gate is multi-row runner implementation/planning,
not backtest execution.

Required future machinery includes:

- deterministic iteration over a locked local development window;
- strict-prior/completed-bar gating for every row;
- no OOS/Lockbox/Forward access;
- no provider/API/download path;
- no stale or diagnostic runner import path;
- deterministic artifacts for every row family and executable ledger;
- complete validation/provenance/evidence/trusted-bundle closure;
- separation of mechanical Development/Reconciliation PnL from any future
  source-faithful evidence claim.

### P1-2 - Repo-Wide Stale Runner Exclusion Not Proven For Run

The inspected S27_V2 package root is fail-closed and safe, but full repo-wide
exclusion of stale/diagnostic runners has not yet been proven for a controlled
run. The next runner gate must include an explicit stale-runner exclusion proof.

### P1-3 - Tests Are Single-Row Hostile Tests, Not Run-Readiness Proof

The focused tests are meaningful for the one-row checkpoint and include forged
row, bundle, source-hash, provenance, and downstream-flag rejection. They do not
yet prove multi-row deterministic iteration, per-row strict-prior gating,
generalized session/roll/working-order lifecycle, full run artifact families, or
run-level closure.

## Non-Blocking Notes

- Direct `Carver.pdf` verification was unavailable in the GPT chat and remains
  `UNKNOWN / FAIL_CLOSED` for that audit.
- The actual-PnL surface is correctly labeled as mechanical
  Development/Reconciliation only.
- Inferred retail cost and inferred valuation convention remain assumptions,
  not book-explicit Carver authority.
- Package-root exports were judged safe for the inspected S27_V2 checkpoint.

## Gate Decision

Backtest execution may not proceed from this audit.

The exact next gate is:

`S27_V2 generalized multi-row controlled local-only development backtest-runner machinery gate`

That gate should implement or fail-close:

- locked-window iteration;
- per-row strict-prior/completed-bar gates;
- stale-runner exclusion proof;
- deterministic artifact families;
- run-level validation/provenance/evidence/trusted-bundle closure;
- continued no-provider/no-download/no-OOS/no-Lockbox/no-Forward boundaries;
- continued no-result-interpretation/no-PnL-evaluation/no-source-faithful-claim
  boundaries.

## Non-Authorization

This audit result record does not authorize:

- provider/API access;
- downloads or new data acquisition;
- OOS, Lockbox, or Forward access;
- backtests or result-scored runs;
- result interpretation;
- PnL evaluation;
- tuning;
- adapter work;
- deployment, trading, or promotion;
- Git actions;
- source-faithful evidence claims.

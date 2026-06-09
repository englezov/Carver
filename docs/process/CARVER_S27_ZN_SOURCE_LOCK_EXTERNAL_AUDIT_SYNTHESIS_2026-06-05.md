# Carver S27 ZN Source Lock External Audit Synthesis

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_SOURCE_LOCK_AUDIT_SYNTHESIS_SUPERSEDED_BY_REAUDIT_PASS_WITH_EDITS
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the operator-supplied external hostile-audit results for the S27 ZN v2
source-lock gate and the resulting process decision. This is a process record
only. It authorizes no implementation, no parsing, no provider/API access, no
data download, no diagnostic, no backtest, no OOS, no Lockbox, no Forward, no
adapter work, no deployment, no trading, no Git staging, no commit, no push,
and no PR.

## Audit Inputs

Operator specified audit order:

```text
OPUS_FIRST_GPT_5_5_EXTENDED_PRO_SECOND
```

| Order | Auditor | Attachment | SHA256 |
|---:|---|---|---|
| 1 | Opus | `C:\Users\apops\.codex\attachments\144fc1f3-00b9-42c1-a9a5-a8de94f790e4\pasted-text.txt` | `5285335013F1547517649B0F1BE905D73C983057E340415D80B88B8975311F68` |
| 2 | GPT 5.5 Extended Pro | `C:\Users\apops\.codex\attachments\d4958cde-808e-4b73-8047-47deba69c6a8\pasted-text.txt` | `957C16F44D6F76B83C9033D52304311E09B8C6F31F41F829447A47B92B3EAF3C` |

## External Verdicts

Opus verdict:

```text
PASS_WITH_REQUIRED_EDITS
```

Opus found the broad S26/S27 structure source-faithful but rejected the source
lock's `S27_FORECAST_SCALAR = 20.0` claim, arguing S27 should inherit the S26
`9.3` scalar. Opus also required tighter cost, execution, V/Q/M, same-series,
roll, quantile-causality, sigma-estimator, and speed-limit gates.

GPT 5.5 Extended Pro verdict:

```text
FAIL
```

GPT could not inspect the exact Markdown artifact in its active file set, so it
failed artifact auditability. Against `Carver.pdf`, GPT agreed with S27
inheritance from S26, S26 scalar `9.3`, S27 trend veto, V/Q/M, adjacent-position
limit-order execution, cost distinctions, and diagnostic-only treatment for old
target-position runners. GPT disagreed with treating `20.0` as a source-exact
constant, but supported the book statement that S27 requires a higher scalar
estimated around `20`.

## Local PDF Check On Scalar Conflict

Because the external auditors disagreed on the central scalar gate, the local
PDF was rechecked before source-lock revision.

Local extraction found:

- PDF page 480: S26 scalar is `9.3`.
- PDF page 500: S27 first computes a mean-reversion forecast using the previous
  chapter's approach.
- PDF page 502: after the forecast overlay turns off mean reversion about half
  the time, a higher scalar is required and is estimated around `20`.
- PDF page 504: S27 roughly doubles the forecast scalar to compensate for the
  overlay being off about half the time.

Disposition:

```text
S26_SCALAR_9_3_LOCKED
S27_SCALAR_AROUND_20_BOOK_ESTIMATE_ACCEPTED
S27_IMPLEMENTATION_FREEZE_20_0_ACCEPTED_AS_CONVENTION_NOT_SOURCE_EXACT_CONSTANT
OPUS_INHERIT_9_3_FOR_S27_REJECTED_PENDING_REAUDIT
GPT_EXACT_20_CONCERN_ACCEPTED
```

## Required Source-Lock Edits Applied

The source lock was revised in:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
```

Applied changes:

- Status changed to revised-after-audits and awaiting re-audit.
- S27 scalar now distinguishes book text from implementation convention:
  `S27_FORECAST_SCALAR_BOOK_TEXT = AROUND_20` and
  `S27_FORECAST_SCALAR_V2_IMPLEMENTATION_FREEZE = 20.0`.
- The lock no longer describes `20.0` as a source-exact constant.
- V/Q/M now specifies percentage volatility, 2560-day ten-year mean where
  available, expanding/admissible quantile history for `Q`, and EWMA span 10
  smoothing for `M`.
- Execution now requires adjacent-position single-lot limit orders, working
  order state, end-of-day cancellation/reset, one-hour-lag limit fills,
  market-order triggers, and one-hour-lag market fills.
- Cost lock now separates limit-order commission-only fills from market-order
  commission-plus-normal-spread fills.
- Roll, session, fill realism, zero-sign edge cases, sigma-estimator source,
  capacity/speed-limit eligibility, and daily/hourly continuous-level
  compatibility remain fail-closed before scoring.

## Gate Decision

This synthesis was superseded by:

```text
docs/process/CARVER_S27_ZN_SOURCE_LOCK_REAUDIT_RESULT_2026-06-05.md
```

That re-audit returned `PASS_WITH_REQUIRED_EDITS`; the two required edits were
applied to:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
```

Current gate:

```text
S27_ZN_BOOK_SOURCE_LOCK_PASSED_FOR_V2_IMPLEMENTATION_EXERCISE
```

This does not authorize provider/API access, downloads, diagnostics, backtests,
OOS, Lockbox, Forward, tuning, alpha claims, promotion, Git staging, commit,
push, PR, deployment, or trading.

Previous stop line:

```text
S27_V2_IMPLEMENTATION_BLOCKED_BY_REVISED_SOURCE_LOCK_REAUDIT_GATE
```

Existing S27 result artifacts remain:

```text
DIAGNOSTIC_ONLY_FAILURE_MAP_MATERIAL
```

## Non-Authorization

This synthesis authorizes no provider API access, no data download, no
market-row parsing, no implementation, no diagnostic, no backtest, no OOS, no
Lockbox, no Forward, no CFD adapter work, no tuning, no deployment, no trading,
no promotion, no Git staging, no commit, no push, no PR update, and no remote
operation.

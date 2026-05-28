# 01 Governance, Scope, and Remote Isolation

Use this file to audit the non-negotiable Carver boundaries: clean workspace only, source-native futures first, no CFD adapter leakage, no OOS/Lockbox/Forward, no promotion, no real data/backtest authorization, and distinct GitHub remote isolation from QuantLab_v3.

---

# FILE: AGENTS.md

```text
# Carver Agent Rules

Before any task in this folder, read:

1. `README.md`
2. `docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md`
3. `docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md`
4. `docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md`

Core rules:

- This folder is the clean active Carver research workspace.
- The old `C:\Users\openclaw\Desktop\QuantLab_v3` folder is archived and must not be used for active pipelines.
- Do not copy or resurrect old adapter code, old CFD broker-clock assumptions, old data-prep scripts, or stale pipeline state.
- Every future lane must declare `SOURCE_NATIVE_FUTURES`, `CFD_DIRECT`, or `CFD_ADAPTER` before data work.
- Source-native futures discovery must remain source-native and must not borrow CFD assumptions.
- CFD adapter work requires a separate explicit adapter gate after source-native behavior exists.
- Strategies from the book must be labeled as standalone candidates or source-native portfolio sleeves before interpretation.
- A portfolio sleeve failing standalone is not family death if the book frames it as portfolio material.
- Reconstruct complete book portfolios separately from individual strategy tests.
- Do not access OOS, Lockbox, or Forward data without explicit operator authorization.
- Do not run any backtest or diagnostic over 2 years without explicit operator approval.
- Use completed bars only.
- Do not tune parameters, thresholds, filters, exits, symbols, costs, or windows after seeing results.
- Do not trade, deploy, promote, or claim alpha from this workspace without explicit locked authorization.
- Carver must use a distinct GitHub repository. Do not push to or reuse the old `QuantLab_v3` remote, branches, PRs, Actions state, releases, tags, deployment environments, or secrets. See `docs/process/CARVER_REMOTE_ISOLATION_RULE_2026-05-29.md`.

For any risky action, ambiguous stage transition, data-window question, destructive operation, credential exposure risk, GitHub push, or governance conflict, stop and ask the operator.

```

# FILE: README.md

```text
# Carver Research Workspace

Status:

```text
CARVER_CLEAN_WORKSPACE_LOCAL_MISSION_SHELL_NOT_PIPELINE_AUTHORIZATION
```

This folder is the clean local workspace for dissecting the Carver book and turning its strategies into disciplined source-native research candidates.

The old workspace at `C:\Users\openclaw\Desktop\QuantLab_v3` is archived as an operationally contaminated blob. It may be used only as read-only archaeology. No active pipeline work should run there.

## Mission

The project mission is to extract, record, and test Carver strategies professionally:

- record approximately 30 book strategies as source-native futures research candidates where possible;
- test each strategy individually with correct interpretation labels;
- label book portfolio components as `SOURCE_NATIVE_PORTFOLIO_SLEEVE` instead of treating every sleeve as standalone;
- reconstruct and test each complete portfolio described in the book as its own portfolio candidate;
- preserve failure information as a map of where mechanisms fail and where to search next;
- use CFD only as a later deployment adapter after source-native behavior is understood.

## Hard Rules

- Do not import old adapters, old CFD broker-clock plumbing, old data-prep scripts, or old pipeline state as authority.
- Every lane must declare exactly one class before data work: `SOURCE_NATIVE_FUTURES`, `CFD_DIRECT`, or `CFD_ADAPTER`.
- Source-native futures discovery must not use CFD assumptions.
- CFD adapter work requires a separate explicit adapter gate after source-native pulse exists.
- No OOS, Lockbox, or Forward access without explicit operator authorization.
- No backtest or diagnostic over 2 years without explicit operator approval.
- Completed bars only.
- No tuning after seeing results.
- No promotion from Development/Reconciliation.

## Local Book

`Carver.pdf` is present locally as a reference copy and is intentionally ignored by Git.

Use small, cited source extracts and repo-local summary artifacts rather than copying large passages from the book.

```

# FILE: docs\mission\CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md

```text
# Carver Source-Native Research Charter

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_NOT_PIPELINE_AUTHORIZATION
```

## Purpose

This charter defines the clean Carver research mission after retiring the messy local `QuantLab_v3` workspace from active pipeline use.

The mission is not to rescue old candidates. The mission is to dissect the Carver book systematically, map its strategies and portfolios, and test them through a clean source-native futures-first process.

## Mission Objectives

1. Extract and record the book strategy set, targeting approximately 30 futures strategies where the source supports that scope.
2. Build each individual strategy as a source-native futures candidate where possible.
3. Label each strategy before interpretation as one of:
   - `STANDALONE_CANDIDATE`
   - `SOURCE_NATIVE_PORTFOLIO_SLEEVE`
   - `PORTFOLIO_ONLY_COMPONENT`
   - `BLOCKED_SOURCE_UNRESOLVED`
4. Test standalone strategies individually only when the book/source framing supports standalone interpretation.
5. Treat source-described portfolio sleeves as sleeves, not as standalone family deaths.
6. Reconstruct each complete book portfolio as its own portfolio candidate after its member sleeves are source-locked.
7. Record failures as useful research output: mechanism failure, instrument mismatch, regime sensitivity, implementation ambiguity, source-data limitation, portfolio-dependency, or adapter/deployment mismatch.

## Source-Native First Rule

Discovery is source-native futures first.

CFD work is not discovery unless the source itself is CFD-native. A CFD translation may be opened later only as an explicit adapter lane after source-native behavior exists.

## Book-Instrument Preference

Prefer the instrument or market family named in the book. When a direct local source-native futures dataset is unavailable, record the blockage rather than silently substituting a CFD or adjacent ticker.

## Evidence Windows

The default research sequence is:

```text
Development/Reconciliation -> TEST -> VALIDATION -> LOCKBOX -> Forward
```

Development/Reconciliation is process/readiness work and not promotion evidence.

Any diagnostic or backtest over 2 years requires explicit operator approval.

## Portfolio Rule

A complete book portfolio is tested as a portfolio candidate, not inferred from isolated sleeve results.

Portfolio work must lock:

- member strategies;
- source-native instruments;
- rebalance and weighting rules;
- costs and target units;
- calendar/session conventions;
- window budget;
- sleeve fail-closed behavior;
- no post-result sleeve selection or rescue.

## Non-Authorization

This charter authorizes no data export, no parsing, no implementation, no tests/backtests, no strategy computation, no OOS, no Lockbox, no Forward, no deployment, no trading, and no promotion.

```

# FILE: docs\process\CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md

```text
# Clean Workspace Migration Record

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_CLEAN_WORKSPACE_MIGRATION_LOCAL_RECORD_NOT_PIPELINE_AUTHORIZATION
```

## Old Workspace

Old local workspace:

```text
C:\Users\openclaw\Desktop\QuantLab_v3
```

Disposition:

```text
ARCHIVED_OPERATIONAL_BLOB_DO_NOT_PIPELINE
```

Archive marker created:

```text
C:\Users\openclaw\Desktop\QuantLab_v3\ARCHIVED_WORKSPACE_DO_NOT_PIPELINE_2026-05-28.md
```

Latest known commit at archive time:

```text
1078ea8 Park ES VWAP reversion discovery lane
```

Old branch at archive time:

```text
codex/s23-acceleration-test-park-record
```

Old remote at archive time:

```text
origin https://github.com/englezov/QuantLab_v3.git
```

## New Workspace

Clean local workspace:

```text
C:\Users\openclaw\Desktop\Carver
```

This workspace starts as a mission shell only. It does not import old code, old adapters, old data-prep scripts, old data folders, old runtime state, or old pipeline state.

Local reference book:

```text
C:\Users\openclaw\Desktop\Carver\Carver.pdf
```

The PDF is local reference material and is ignored by Git.

## Migration Rule

Nothing from the old workspace becomes active authority unless it is deliberately selected, hash-bound, and reintroduced through a clean Carver artifact.

The old workspace may answer historical questions, but it must not be used to run pipelines.

## Next Clean Step

Recommended next clean step:

```text
CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY
```

That step should inspect the local book reference and produce a strategy/portfolio inventory without running data, code, tests, backtests, or adapters.

```

# FILE: docs\process\LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md

```text
# Lane Classification And Adapter Quarantine Rules

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_LANE_CLASSIFICATION_ADAPTER_QUARANTINE_RULES_NOT_PIPELINE_AUTHORIZATION
```

## Required Lane Classification

Before any data work, each lane must declare exactly one:

```text
SOURCE_NATIVE_FUTURES
CFD_DIRECT
CFD_ADAPTER
```

## Source-Native Futures

`SOURCE_NATIVE_FUTURES` means:

- source signal logic is interpreted on the book/source-native futures instrument where possible;
- futures data, sessions, rolls, timestamps, bar semantics, and contract rules must be locked before strategy computation;
- CFD broker sessions, CFD spreads, CFD symbols, and CFD timestamps are not discovery authority.

## CFD Direct

`CFD_DIRECT` means:

- the source hypothesis is directly about a CFD/broker venue;
- broker symbol specs, sessions, spreads, swaps, and fills are primary source fields;
- this class must not be confused with a futures source translated to CFD.

## CFD Adapter

`CFD_ADAPTER` means:

- source-native behavior already exists or is explicitly being compared;
- the adapter asks whether source-native behavior survives target broker translation;
- adapter work requires its own gate memo;
- adapter results may not tune or rescue source-native rules.

## Old Plumbing Quarantine

The following are rejected as default authority:

- old CFD broker-clock assumptions;
- old ICMarkets/The5ers adapter scripts;
- old mixed futures/CFD translation scripts;
- old data-prep scripts not rebuilt under this workspace's rules;
- old TEST/VALIDATION/Lockbox state;
- old contaminated results;
- old pipeline convenience shortcuts.

## Backtest Length Guard

No backtest or diagnostic over 2 years may be run without explicit operator approval.

## Non-Authorization

This rule file authorizes no data access, no export, no parsing, no implementation, no tests/backtests, no strategy computation, no OOS, no Lockbox, no Forward, no deployment, no trading, and no promotion.

```

# FILE: docs\process\CARVER_REMOTE_ISOLATION_RULE_2026-05-29.md

```text
# Carver Remote Isolation Rule

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_REMOTE_ISOLATION_RULE_NOT_REMOTE_PUSH_AUTHORIZATION
```

## Rule

Carver must use a distinct GitHub repository.

The Carver workspace must not push to, reuse, or depend on the old QuantLab remote:

```text
https://github.com/englezov/QuantLab_v3.git
```

## Forbidden

- Do not add the old QuantLab remote to this repository.
- Do not push Carver commits to `englezov/QuantLab_v3`.
- Do not reuse old QuantLab branches, PRs, issues, GitHub Actions state, releases, tags, deployment environments, or repository secrets as Carver authority.
- Do not use old QuantLab CI or remote status as evidence for Carver.
- Do not create a remote or push Carver until the operator explicitly authorizes the final remote action.

## Required Future Remote Gate

Before the first Carver remote push:

- Confirm the local workspace is `C:\Users\openclaw\Desktop\Carver`.
- Confirm `git remote -v` does not point to `QuantLab_v3`.
- Create or select a distinct Carver GitHub repository.
- Record the chosen remote in a repo-local process artifact.
- Run the final package/source-faithfulness audit first.
- Commit all approved audit patches locally.
- Ask the operator for explicit remote-push authorization.

## Non-Authorization

This rule authorizes no remote creation, no remote configuration, no push, no PR, no deployment, no trading, no data work, no tests/backtests, no OOS, no Lockbox, no Forward, and no CFD adapter activity.

```

# FILE: docs\process\CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md

```text
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

```

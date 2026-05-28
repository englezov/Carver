# Governance And Non-Authorization Context

Generated: 2026-05-28

Status:

```text
PROCESS_ONLY_OPUS_UPLOAD_CONTEXT_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

This file is an upload-context bundle generated from clean Carver repo-local artifacts. It authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, and no promotion.

---

## Source File: `AGENTS.md`

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

For any risky action, ambiguous stage transition, data-window question, destructive operation, credential exposure risk, GitHub push, or governance conflict, stop and ask the operator.


---

## Source File: `README.md`

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


---

## Source File: `docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md`

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


---

## Source File: `docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md`

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


---

## Source File: `docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md`

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


---

## Source File: `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`

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


---

## Source File: `docs/process/CARVER_PRE_OPUS_DEFINITION_COMPLETION_RECORD_2026-05-28.md`

# Carver Pre-Opus Definition Completion Record

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_PRE_OPUS_DEFINITION_COMPLETION_RECORD_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Record that the current clean Carver daily source-native definition layer is complete enough to submit to a separate source-faithfulness audit, before any Opus audit execution, data work, implementation, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab import, tuning, deployment, trading, or promotion.

This record is a process artifact only. It does not approve code, data inspection, NinjaTrader export, market-row parsing, historical evaluation, strategy computation, or portfolio reconstruction beyond the already drafted process briefs.

## Scope

This completion record covers the current first-spine definition set:

- M0 source-native futures foundation.
- M1 position sizing and risk scaling.
- M2 forecast-block architecture.
- M3 multi-instrument portfolio construction.
- M5 futures curve and carry construction.
- S01 buy-and-hold single contract.
- S02 buy-and-hold with risk scaling.
- S03 buy-and-hold with variable risk scaling.
- S04 buy-and-hold portfolio with variable risk position sizing.
- P01 risk parity example portfolio.
- P02 All Weather example portfolio.
- S09 multiple trend following.
- S10 basic carry.
- S11 combined carry and trend.

The record does not cover Part Two and Part Three extensions after S11, Part Four fast-stack strategies, Part Five relative-value strategies, later Jumbo portfolios, CFD adapter work, or implementation/data gates.

## Definition Coverage Matrix

| Artifact | Role | Definition disposition before Opus audit |
| --- | --- | --- |
| `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md` | Foundation defaults and hard boundaries | Present; declares `SOURCE_NATIVE_FUTURES`, completed-bar rule, source-native instrument identity, data-surface non-authorization, old workspace quarantine, and no-code/no-data posture. |
| `docs/process/CARVER_M1_POSITION_SIZING_AND_RISK_SCALING_MODULE_SPEC_2026-05-28.md` | Shared sizing/risk module | Present; hostile-audited and patched; pre-validates risk estimates, timestamp alignment, context-applicable portfolio/forecast inputs, and M1/M2 trade-decision boundary. |
| `docs/process/CARVER_M2_FORECAST_BLOCK_ARCHITECTURE_MODULE_SPEC_2026-05-28.md` | Shared forecast-block module | Present; hostile-audited and patched; now explicitly declares `SOURCE_NATIVE_FUTURES`; keeps S07/S08 as forecast-building components rather than standalone advancements. |
| `docs/process/CARVER_M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION_MODULE_SPEC_2026-05-28.md` | Shared portfolio construction module | Present; hostile-audited and patched; enforces portfolio independence, source-native lane class, local mapping caution, and no silent substitution. |
| `docs/process/CARVER_M5_FUTURES_CURVE_AND_CARRY_CONSTRUCTION_MODULE_SPEC_2026-05-28.md` | Shared futures curve/carry module | Present; hostile-audited and patched; requires source-native lane class, raw carry sign convention, synchronized completed curve legs, and seasonal/wrong-sign fail-closed rules. |
| `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md` | First standalone baseline candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; establishes single-contract futures identity and excess-return/back-adjustment atoms. |
| `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md` | Risk-scaled standalone candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; adds target risk, current held-contract price, multiplier, FX, fixed-risk sizing, rounding, and minimum-capital atoms. |
| `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md` | Variable-risk standalone candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; adds non-leaking variable risk estimate and S03 volatility atoms. |
| `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md` | Portfolio construction candidate gateway | Present; `SOURCE_NATIVE_FUTURES`; process-only; adds instrument weights, IDM, portfolio breadth, and complete-portfolio separation. |
| `docs/researchops/portfolios/CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md` | First complete book portfolio | Present; `SOURCE_NATIVE_FUTURES`; process-only; locks the two-instrument risk-parity example as a separate portfolio brief. |
| `docs/researchops/portfolios/CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md` | Second complete book portfolio | Present; `SOURCE_NATIVE_FUTURES`; process-only; locks the six-instrument All Weather example as a separate portfolio brief. |
| `docs/researchops/candidates/CARVER_S09_MULTIPLE_TREND_FOLLOWING_CANDIDATE_BRIEF_2026-05-28.md` | First core trend forecast candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; captures EWMAC variations, forecast scalars, speed eligibility, FDM, caps, and S07/S08 sleeve treatment. |
| `docs/researchops/candidates/CARVER_S10_BASIC_CARRY_CANDIDATE_BRIEF_2026-05-28.md` | First core carry forecast candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; captures carry curve construction, carry smoothing, scalar/cap/FDM, seasonality, and wrong-sign blockages. |
| `docs/researchops/candidates/CARVER_S11_COMBINED_CARRY_AND_TREND_CANDIDATE_BRIEF_2026-05-28.md` | First combined trend/carry candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; combines S09 and S10 forecast blocks while blocking P07 and later parts. |

## Gap Assessment

No missing definition artifact remains for the current daily first spine listed above.

The following are intentionally unresolved gates, not definition-completion blockers:

- Local source-native data-surface acceptance.
- Local symbol mapping between Appendix C broker codes and NinjaTrader or other local data labels.
- Roll calendar and exchange-session lock.
- Cost-source file creation and lane-specific cost lock.
- Concrete target-risk and capital-base choices for any future executable run.
- Rounding, buffering, and trade/no-trade implementation details.
- EWMA warm-up, Table 51 row selection, Table 52 interpolation policy, and synthetic conformance examples.
- Carry curve leg availability, raw carry sign convention per instrument, expiry calendar source, fixed-month commodity table, and wrong-sign/seasonal blockage table.

These gates must remain closed before data work or implementation. They are suitable questions for later implementation-gate or data-surface artifacts, not for the Opus source-faithfulness audit itself.

## Out-Of-Scope Definitions

The following definitions are intentionally not complete under this record:

- M4 normalised-price and asset-class module for later Part Three variants.
- M6 synthetic-instrument module for relative-value spreads/triplets.
- M7 hourly/fast-stack module for S26/S27.
- M8 risk-management overlay module.
- S05-S08 as standalone candidate briefs; they remain forecast/sleeve components under S09/M2 framing.
- S12-S30 and P03-P14.
- Any CFD adapter or broker translation work.
- Any implementation skeleton, source code, tests, diagnostics, backtests, or local data inspection.

## Pre-Opus Completion Claim

The current first-spine definition layer is complete enough to ask an external source-faithfulness auditor whether the translation is faithful to Carver's book.

The next clean gate should be a separate Opus source-faithfulness audit gate. That future gate should inspect the book and the artifacts listed in this record, then answer whether the definitions describe the strategies, portfolios, labels, stack boundaries, unresolved atoms, and non-authorization rules faithfully.

This record does not authorize the Opus audit execution by itself.

## Required Hostile Audit

Before this definition-completion record and the material M2 lane-class patch are treated as process-safe, a subagent hostile audit must verify:

- The current definition set is complete only for the stated first spine.
- The record does not smuggle in implementation, data, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab imports, tuning, deployment, trading, or promotion.
- M2's new lane-class language is consistent with the source-native spine and does not open a data lane.
- Out-of-scope modules and later strategies remain blocked rather than silently treated as complete.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition:

- No blocking findings.
- The record is process-safe and truthful for the stated first spine only: M0/M1/M2/M3/M5, S01/S02/S03/S04, P01/P02, S09/S10/S11.
- The record does not authorize Opus audit execution; a separate future Opus audit gate remains required.
- The record does not authorize code, data, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab imports, tuning, deployment, trading, or promotion.
- Later modules, strategies, portfolios, fast-stack work, RV-stack work, and CFD adapter work remain out of scope.
- The M2 lane-class patch is consistent with the source-native spine and does not open data or adapter work.

Verdict: the first-spine definition layer is process-safe before creating the separate Opus audit gate.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


---

## Source File: `docs/process/CARVER_OPUS_SECTION_B_DEFINITION_PATCH_RECORD_2026-05-28.md`

# Carver Opus Section B Definition Patch Record

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_OPUS_SECTION_B_DEFINITION_PATCH_RECORD_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Record the process-only patch pass applied after the external Opus hostile source-faithfulness audit returned:

```text
PROCESS_SAFE_FOR_IMPLEMENTATION_GATE_AFTER_PATCHES
```

This patch pass addresses the audit's non-blocking Section B findings without opening data work, implementation, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab imports, tuning, deployment, trading, or promotion.

## Patch Scope

The patch pass updated only clean Carver definition artifacts and the generated Opus upload context.

Patched source artifacts:

- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/process/CARVER_M2_FORECAST_BLOCK_ARCHITECTURE_MODULE_SPEC_2026-05-28.md`
- `docs/process/CARVER_M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION_MODULE_SPEC_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S09_MULTIPLE_TREND_FOLLOWING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S11_COMBINED_CARRY_AND_TREND_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/portfolios/CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md`

Generated upload context refreshed:

- `GPT/OPUS_SOURCE_FAITHFULNESS_AUDIT_PACK_2026-05-28/01_GOVERNANCE_AND_NON_AUTHORIZATION_CONTEXT_2026-05-28.md`
- `GPT/OPUS_SOURCE_FAITHFULNESS_AUDIT_PACK_2026-05-28/02_BOOK_INVENTORY_AND_TRANSLATION_ARCHITECTURE_2026-05-28.md`
- `GPT/OPUS_SOURCE_FAITHFULNESS_AUDIT_PACK_2026-05-28/03_SHARED_MODULE_DEFINITIONS_M0_M1_M2_M3_M5_2026-05-28.md`
- `GPT/OPUS_SOURCE_FAITHFULNESS_AUDIT_PACK_2026-05-28/04_FIRST_SPINE_CANDIDATE_AND_PORTFOLIO_BRIEFS_2026-05-28.md`

The local `Carver.pdf` remains ignored by Git and is not part of this process commit.

## Section B Patch Mapping

| Opus finding | Patch disposition |
| --- | --- |
| S09/M2 0.15 SR speed-limit page citation not directly verified | M2, S09, and S11 now record 0.15 SR units as source context pending exact quote/page re-audit before implementation. |
| S11 Table 51/Table 52 table-number/page labels not directly verified | M2 and S11 now require exact table-number, row, and page-label verification before implementation. |
| S11 Eurodollar allocation example could be confused with later normalised-trend example | S11 no longer treats the previously recorded Eurodollar 30%/30% example as locked authority; exact worked-example rows/pages must be re-page-audited before implementation. |
| P02 IDM 1.81 and Jumbo IDM 2.47 not directly verified by extraction | M3, S04, and P02 now record those IDM numbers as source context pending exact value/page re-audit before implementation. |
| First inventory label vocabulary lacked `PARKED_NOT_STANDALONE` | The first inventory now includes the added label and an amendment note explaining the later architecture/M0 update. |
| M2 wording "trading rule = anything that produces a forecast" not directly verified | M2 now says S07 establishes forecast/trading-rule terminology, while preserving the directly verified forecast definition. |
| First inventory still labeled S29/S30 standalone | S29 and S30 rows in the first inventory now use `PARKED_NOT_STANDALONE` with an amended-label explanation. |

## Remaining Blocks

The patch intentionally does not solve the following by inference:

- Exact S09 0.15 SR quote/page verification.
- Exact S11 Table 51 and Table 52 table-number/page-label verification.
- Exact S11 worked-example row/page verification.
- Exact P02 IDM 1.81 quote/page verification.
- Exact Jumbo IDM 2.47 quote/page verification.

These items remain blocked before implementation or data work.

## Non-Authorization

This patch record authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


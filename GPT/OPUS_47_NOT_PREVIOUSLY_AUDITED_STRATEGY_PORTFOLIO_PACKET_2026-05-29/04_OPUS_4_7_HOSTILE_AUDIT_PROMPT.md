# Opus 4.7 Hostile Audit Prompt

Use Opus 4.7 for a hostile source-faithfulness and governance audit of the Carver strategy and portfolio work not previously covered by a recorded Opus result.

## Input Files

You have five audit-input files:

```text
00_Carver.pdf
01_GOVERNANCE_AND_PRIOR_OPUS_SCOPE.md
02_STRATEGY_SIGNAL_GRAPH_S09_S10_S11.md
03_PORTFOLIO_GRAPH_P01_P02_P05_P06_P07.md
04_OPUS_4_7_HOSTILE_AUDIT_PROMPT.md
```

Treat `00_Carver.pdf` as the source authority. Treat the markdown files as Carver's audit packet and summary of repo-local process/code artifacts.

## Declared Audit Scope

Audit the not-yet-Opus-audited Carver strategy and portfolio graph:

```text
P01/P02 final package if no Opus result exists
S09 synthetic trend conformance
S10 carry forecast-block extension after M5
S11 combined carry/trend conformance
P05 complete trend portfolio synthetic conformance
P06 complete carry portfolio synthetic conformance
P07 complete combined trend/carry portfolio synthetic conformance
lean hostile audit results
unresolved production atoms
post-P07 Appendix C/readiness decision
```

Prior recorded Opus coverage must be respected:

- Early definition architecture/patch trail covered first-spine definitions, not later implementation surfaces.
- S10/M5 Opus 4.7 audit covered only M5 synthetic carry construction and the post-M5 next-step decision.
- P01/P02 final Opus packet exists, but this packet found no separate stored Opus result.

## Allowed Audit Activity

Read-only audit only.

You may inspect the provided files and the included book. Do not request or assume real data. Do not run tests. Do not execute code. Do not infer source locks from implementation names or passing synthetic tests.

## Forbidden

No file edits. No code execution. No tests. No real-data execution. No market-row parsing. No NinjaTrader export. No diagnostics. No backtests. No returns. No PnL. No Sharpe. No drawdown. No OOS. No Lockbox. No Forward. No CFD adapters. No old QuantLab active-pipeline use. No tuning. No deployment. No trading. No promotion. No remote operations.

## Required Audit Questions

### Prior Scope

1. Is the packet's statement of prior Opus coverage accurate?
2. Is S10/M5 correctly treated as already Opus-audited while S10 forecast-block-after-M5 remains in scope?
3. Is P01/P02 correctly treated as not covered by a recorded Opus result unless an external result exists outside the repo?

### Strategy Graph

4. Is S09 synthetic trend conformance source-faithful at process-and-synthetic scope?
5. Does S09 correctly preserve unresolved production atoms, especially production use of the book-verified `0.15 SR` threshold and real-data cost eligibility?
6. Is S10 carry forecast-block-after-M5 source-faithful and consistent with the prior M5 Opus constraints?
7. Does S10 stop at final capped carry forecast output without position, performance, diagnostic, backtest, or production carry claims?
8. Is S11 combined carry/trend source-faithful at synthetic conformance scope?
9. Does S11 correctly consume S09 and S10 forecast-block outputs and avoid production Table 51/Table 52 locks?
10. Are S09/S10/S11 correctly separated from P05/P06/P07 portfolio surfaces?

### Portfolio Graph

11. Is P01/P02 final package source-faithful and governance-safe?
12. Are P05/P06/P07 correctly described as Carver process aliases rather than book-native labels?
13. Is P05 correctly tied to Strategy Nine over the Jumbo source frame?
14. Is P06 correctly tied to Strategy Ten over the Jumbo source frame?
15. Is P07 correctly tied to Strategy Eleven over the Jumbo source frame?
16. Does P07 correctly consume S11 combined forecasts directly rather than combining P05 and P06 desired-position outputs?
17. Are P05/P06/P07 synthetic outputs correctly limited to desired position inputs only?
18. Is Appendix C correctly treated as complete universe source but not local provider readiness?
19. Are weights, IDM, target risk, capital, price risk, FX, costs, trend/carry eligibility, and missing-member policy separated from production readiness?
20. Does the post-P07 decision correctly select a Part One Jumbo universe/readiness shape gate before any real-data work?

### Governance

21. Does any wording smuggle authorization for real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, or promotion?
22. Does any artifact imply local alpha, performance evidence, executable readiness, or production source locks from synthetic tests?
23. Are lean hostile audit results used appropriately as code/process boundary checks, without being treated as Opus source-faithfulness audits?
24. Are unresolved production atoms explicitly preserved rather than silently solved by synthetic conformance?

## Severity Format

Report findings ordered by severity.

For each finding use:

```text
Severity: CRITICAL | HIGH | MEDIUM | LOW | INFORMATIONAL
File:
Issue:
Why it matters:
Required fix:
```

Use `CRITICAL` or `HIGH` for anything that:

- misstates book source or portfolio identity;
- treats a synthetic surface as production readiness;
- opens or implies real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, deployment, trading, or promotion;
- hides missing Appendix C/readiness/source locks;
- silently combines the wrong dependencies, especially P07 from P05/P06 desired-position outputs.

Use `LOW` or `INFORMATIONAL` for presentation risks, packet hygiene, or forward constraints that do not block current source-faithfulness disposition.

## Required Verdict

After findings, provide:

```text
BLOCKING_FINDINGS: YES | NO
AUDIT_DISPOSITION: PASS_NOT_PREVIOUSLY_OPUS_AUDITED_STRATEGY_PORTFOLIO_SCOPE
```

or:

```text
BLOCKING_FINDINGS: YES
AUDIT_DISPOSITION: BLOCKED_REQUIRES_FIX
```

or:

```text
BLOCKING_FINDINGS: UNKNOWN
AUDIT_DISPOSITION: INSUFFICIENT_SOURCE_CONTEXT
```

If insufficient source context, name the exact missing narrow book pages, tables, or repo artifacts needed. Do not infer missing source locks.

## Non-Authorization

This prompt authorizes no file edits, no tests, no code execution, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no remote operations, and no Opus execution by itself.

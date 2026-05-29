# Opus 4.7 Audit Prompt

Use Opus 4.7 for a hostile source-faithfulness and governance audit of the Carver S10/M5 carry packet.

## Files To Review

Review exactly these five audit-input files:

```text
01_POST_S10_M5_NEXT_STEP_DECISION.md
02_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE.md
03_M5_SYNTHETIC_CODE.py
04_M5_SYNTHETIC_TESTS.py
05_S10_CARRY_SOURCE_EXTRACT_PACK.md
```

The entire book is intentionally not included in this packet. Treat `05_S10_CARRY_SOURCE_EXTRACT_PACK.md` as the bounded source summary for this audit. If that source pack is insufficient for any source-faithfulness conclusion, say exactly what additional narrow page-cited source excerpt is required. Do not infer missing source locks.

## Audit Objective

Determine whether the current Carver S10/M5 surface and next-step decision are source-faithful and governance-safe at the current scope:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

The M5 surface is allowed to convert locked toy held/comparison futures contract prices, locked toy sign convention, locked expiry annualization, and prevalidated price risk into a synthetic risk-adjusted carry forecast input.

The post-S10/M5 next-step decision is allowed to select a future S10 carry forecast-block extension before S11, but must not itself authorize implementation.

## Required Checks

Check whether:

1. The current M5 code stops at a risk-adjusted carry forecast input and does not emit a trading signal, position, performance metric, return, PnL, Sharpe, drawdown, backtest, diagnostic, or portfolio output.
2. The current M5 implementation keeps production source locks unresolved where they should remain unresolved: raw-carry sign, held/comparison contract role, expiry calendar/day-count, roll-day handling, fixed-month commodity rules, seasonal policy, wrong-sign policy, cost eligibility, scalar, caps, FDM, forecast weighting, position sizing, and buffering.
3. The synthetic implementation is compatible with the source-pack framing of carry measurement, annualization, and risk adjustment, without claiming production source authority.
4. The next-step decision to extend S10 carry forecast-block machinery before S11 is source-faithful and governance-safe.
5. S10 smoothing spans of 5, 20, 60, and 120 business days are correctly treated as future S10 atoms and not current M5 outputs.
6. Carry scalar 30, caps, cost eligibility, equal forecast weights, and carry FDM are correctly treated as future S10 atoms and not current M5 outputs.
7. S11 trend/carry combination, P06, P07, real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, promotion, tuning, remote operations, and old QuantLab active-pipeline use remain closed.
8. The packet does not smuggle authorization through documentation wording, tests, names, status labels, or code exports.
9. The source pack is narrow enough to avoid copying the entire book while still sufficient for this audit stage.

## Forbidden During Audit

Do not run:

- real data;
- market-row parsing;
- NinjaTrader export;
- diagnostics;
- backtests;
- returns/PnL/performance calculations;
- OOS, Lockbox, or Forward;
- CFD adapters;
- deployment, trading, or promotion;
- remote pushes or GitHub actions;
- old `C:\Users\openclaw\Desktop\QuantLab_v3` active pipelines.

Do not suggest tuning parameters after seeing results. Do not treat synthetic tests as evidence of alpha.

## Output Format

Return findings ordered by severity.

For each finding include:

```text
Severity:
File:
Issue:
Why it matters:
Required fix:
```

If there are no blocking findings, say:

```text
NO BLOCKING FINDINGS
```

Then list non-blocking residual risks, especially any source facts that require a narrower page-cited extract before future production source locks.

End with one of:

```text
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_SCOPE
AUDIT_DISPOSITION: BLOCKED_REQUIRES_FIX
AUDIT_DISPOSITION: INSUFFICIENT_SOURCE_CONTEXT
```

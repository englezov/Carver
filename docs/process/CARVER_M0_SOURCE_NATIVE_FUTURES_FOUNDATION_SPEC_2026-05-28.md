# Carver M0 Source-Native Futures Foundation Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M0_FOUNDATION_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

M0 is the lean foundation layer for future Carver source-native futures briefs.

It locks the process defaults and unresolved atoms that every later candidate or portfolio brief must inherit before any data work, implementation, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion.

M0 is not a strategy, not a backtest plan, not a data-surface acceptance, and not implementation authorization.

## Source Anchors

- The book is futures-specific and describes 30 futures strategies over a 100+ instrument universe. See `Carver.pdf`, PDF pages 11-17.
- The book uses closing prices for the relevant time period, not OHLC/candlestick inputs. See `Carver.pdf`, PDF page 15.
- Parts One, Two, and Three are daily/once-a-day strategies that share a position-management and forecast framework. See `Carver.pdf`, PDF page 17.
- Part Four uses faster intraday data and must remain a separate fast-stack lane. See `Carver.pdf`, PDF pages 475-476.
- Part Five uses relative-value synthetic instruments and must remain a separate RV-stack lane. See `Carver.pdf`, PDF pages 511-512.
- Appendix C lists the book's 102-instrument Jumbo futures universe and warns that broker market codes may vary. See `Carver.pdf`, PDF pages 690-695.

Page references in M0 are process anchors. Every future candidate or portfolio brief must re-check its own source pages before lock.

## Lane Class

Default Carver book strategy lane class:

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened by M0.

Any later CFD adapter work requires a separate explicit adapter gate after source-native behavior exists.

## Data Surface Posture

Operator-reported local data surface:

```text
NINJATRADER_SOURCE_NATIVE_FUTURES_DATA_SURFACE_CANDIDATE
```

Operator reports that local NinjaTrader futures data is available for broad futures coverage, including futures indices, metals, Bitcoin, and Ether, with resolution/coverage reported down to 1-minute bars and daily candles available where needed.

This is availability context only. It is not data-quality acceptance, not data acceptance, not export authorization, not parsing authorization, not diagnostic authorization, and not backtest authorization.

### Local Native Timeframe First

When a future data lane is explicitly authorized, prefer local NinjaTrader source-native futures data at the native timeframe required by the strategy.

- Use native completed daily candles for daily Carver strategies where available.
- Use native completed hourly or smaller intraday bars only for fast-stack strategies that require them.
- Do not reconstruct daily or hourly bars from 1-minute data by default.
- Reconstruct from 1-minute data only if local native timeframe data is missing, invalid, or a separate data-quality gate justifies reconstruction.
- Download or fetch external data only if local NinjaTrader data is missing, insufficient, or materially less efficient than obtaining a native source timeframe.

### NinjaTrader Non-Authorization

M0 authorizes no NinjaTrader subscription, export, parsing, brokerage connection, order-routing setup, account file handling, credential handling, live trading configuration, or broker/account integration.

Any NinjaTrader use must first pass a separate source-native data-surface gate.

## Completed-Bar Rule

All future lanes must use completed bars only.

- Daily strategies: completed daily bars.
- Fast-stack strategies: completed intraday bars at the authorized timeframe.
- RV-stack strategies: completed bars for every leg, synchronized according to the locked synthetic-instrument rule.

No lane may use partial bars or future information.

## Source-Native Instrument Identity

Each future candidate or portfolio brief must lock, before data work:

- Book instrument name.
- Book/broker code from Appendix C where applicable.
- Exchange.
- Currency.
- Multiplier.
- First source-usable date or first data date.
- Micro, mini, or full-size contract identity.
- Any substitution rule.

Book-preferred instruments must be used where available. If the exact source-native instrument is unavailable, record blockage rather than silently substituting a CFD, index proxy, ETF, adjacent ticker, or old QuantLab symbol.

## Timeframe Families

M0 recognizes three Carver source-native futures stacks:

| Stack | Scope | Default data posture |
| --- | --- | --- |
| Daily directional stack | Parts One, Two, Three | Native completed daily candles. |
| Fast stack | Part Four, S26-S27 | Separate intraday gate; use native completed intraday bars. |
| RV stack | Part Five, S28-S30 | Separate synthetic-instrument gate; use completed bars for all legs. |

No fast-stack or RV-stack lane is opened by M0.

## Foundation Atoms To Lock Per Candidate

Every candidate or portfolio brief must explicitly resolve or mark unresolved:

- Contract identity and source-native instrument mapping.
- Data surface and native timeframe.
- Exchange session definition.
- Timezone.
- Bar close timestamp semantics.
- Holiday calendar.
- Daily candle cut convention.
- Intraday bar timestamp convention when applicable.
- Continuous-contract construction.
- Contract selection and rolling rule.
- Back-adjusted price construction.
- Cost source.
- FX/currency conversion.
- Target risk and capital base.
- Volatility estimate.
- Position sizing.
- Rounding.
- Buffering.
- Instrument eligibility.
- Evidence-window budget.
- Fail-closed behavior for missing or invalid inputs.

If a required atom is unresolved, the lane remains process-only and cannot proceed to implementation or data work.

## Costs

Execution costs must come from:

```text
config/costs.json
```

once such a file exists and is explicitly authorized for the relevant lane.

No hardcoded ad hoc cost dictionaries are allowed.

If costs are unavailable, the candidate or portfolio brief must record the cost-source blockage.

## Evidence Window Guard

The default evidence sequence remains:

```text
Development/Reconciliation -> TEST -> VALIDATION -> LOCKBOX -> Forward
```

Development/Reconciliation is process/readiness work and not promotion evidence.

No diagnostic or backtest over 2 years may be run without explicit operator approval.

M0 authorizes no diagnostics and no backtests.

## Implementation And Test Posture

M0 does not authorize implementation.

After a candidate or module brief is locked, implementation still requires separate explicit implementation authorization.

When implementation is later authorized, the first tests must be synthetic/source-conformance tests, not historical backtests:

- Tiny formula/unit tests.
- Hand-built golden toy examples.
- Invariant tests.
- Book numeric example checks where available.
- Synthetic dry-run/schema checks.

Historical data evaluation requires a later separate operator authorization.

## Strategy And Portfolio Interpretation

Each strategy must be labeled before interpretation:

```text
STANDALONE_CANDIDATE
SOURCE_NATIVE_PORTFOLIO_SLEEVE
PORTFOLIO_ONLY_COMPONENT
BLOCKED_SOURCE_UNRESOLVED
PARKED_NOT_STANDALONE
```

Complete book portfolios must be reconstructed separately from individual sleeve results.

A sleeve failing standalone is not family death if the book frames it as portfolio material.

A parked/not-standalone strategy is not failed alpha.

S29 and S30 remain parked/not-standalone unless a future page-audited process artifact, direct Carver source justification, and explicit operator approval changes that classification.

## Old Workspace Quarantine

The old `C:\Users\openclaw\Desktop\QuantLab_v3` workspace is archived and must not be used for active pipelines.

M0 rejects as active authority:

- Old CFD adapters.
- Old broker-clock assumptions.
- Old data-prep scripts.
- Old mixed futures/CFD translation scripts.
- Old TEST/VALIDATION/Lockbox state.
- Old contaminated results.
- Old pipeline convenience shortcuts.

The two prior backtests remain parked operator memory for this lesson only:

```text
NON_POSITIVE_STANDALONE_DOES_NOT_ADVANCE
```

If cited beyond that general lesson, they must first be named or hash-bound in a separate process-only archaeology memo.

## Hostile Audit Requirement

Any process artifact, candidate brief, portfolio brief, implementation attestation, diagnostic result, backtest result, or gate memo that may influence a lane decision must receive a hostile audit before it is treated as locked.

Required hostile-audit method:

```text
USE_SUBAGENT_FOR_HOSTILE_AUDIT
```

Hostile audits must use a subagent unless the operator explicitly waives that requirement for a specific artifact.

## M0 Output

M0 produces only this process foundation.

The next process step, if explicitly authorized, is S01 candidate-brief drafting:

```text
PROCESS_ONLY_CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

S01 must inherit M0 and may not open implementation, data work, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, or promotion.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

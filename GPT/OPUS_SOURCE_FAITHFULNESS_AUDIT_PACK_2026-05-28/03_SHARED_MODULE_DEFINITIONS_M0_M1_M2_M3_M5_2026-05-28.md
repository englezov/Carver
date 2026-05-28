# Shared Module Definitions M0 M1 M2 M3 M5

Generated: 2026-05-28

Status:

```text
PROCESS_ONLY_OPUS_UPLOAD_CONTEXT_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

This file is an upload-context bundle generated from clean Carver repo-local artifacts. It authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, and no promotion.

---

## Source File: `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`

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


---

## Source File: `docs/process/CARVER_M1_POSITION_SIZING_AND_RISK_SCALING_MODULE_SPEC_2026-05-28.md`

# Carver M1 Position Sizing And Risk Scaling Module Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M1_POSITION_SIZING_RISK_SCALING_MODULE_SPEC_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Define the process-only implementation-ready contract for Carver Module M1:

```text
M1_POSITION_SIZING_AND_RISK_SCALING
```

M1 specifies the source-native futures atoms needed to transform capital, target risk, instrument risk, futures contract identity, FX, instrument weights, IDM, and optional forecast strength into desired futures contract exposure.

This module spec is not code, not a data lane, not a test lane, not a diagnostic lane, not a backtest lane, not an OOS lane, not a Lockbox lane, not a Forward lane, not a CFD adapter lane, not deployment, not trading, and not promotion.

## Scope

M1 owns:

- Capital-first position sizing.
- Instrument risk in annual percentage or daily price-point units.
- Target risk in annualized percentage standard deviation.
- Futures multiplier, current held-contract raw price, and FX conversion.
- Pre-validated variable volatility estimate as an input from S03/M0-locked atoms.
- Instrument weight for portfolio contexts.
- IDM as an input for portfolio contexts.
- Optional forecast strength as an input from M2.
- Whole-contract rounding policy as an unresolved atom.
- Minimum capital and indivisible-contract constraints.
- Fail-closed behavior for invalid sizing inputs.

M1 does not own:

- Forecast construction, forecast scalars, forecast caps, forecast weights, or FDM. Those belong to M2.
- Instrument universe selection, portfolio weights, IDM estimation, or portfolio aggregation. Those belong to M3.
- Futures curve/carry construction. That belongs to M5.
- Data loading, market-row parsing, NinjaTrader export, or historical evaluation.

## Source Anchors

- S02 reverses the S01 order: given capital first, calculate position size second, with instrument risk as the key input. See `Carver.pdf`, PDF page 67.
- S02 measures single-contract risk as annualized standard deviation of returns and translates it into currency terms using current price, futures multiplier, and notional exposure. See PDF pages 68-70.
- S02 states that the price used for sizing should be the price of the expiry currently held, not the back-adjusted price, and includes FX conversion. See PDF page 70.
- S02 defines target risk as annualized percentage standard deviation on capital and derives the required contract count by equating target currency risk with position risk. See PDF pages 70-71.
- S02 gives a daily price-point risk formulation based on daily back-adjusted price differences, useful when the current futures price is negative. See PDF page 72.
- S02 recalculates optimal position daily from current futures price and FX rate, then rounds contract count. See PDF pages 79-81.
- S02 uses fixed notional capital for performance reporting but warns real-money sizing should reduce after losses by using current account value as notional capital. See PDF pages 82-84.
- S02 introduces minimum capital because futures contracts are indivisible and recommends enough capital to start with at least four contracts. See PDF pages 85-87.
- S03 replaces S02 fixed instrument risk with a variable volatility estimate and reduces/increases positions as volatility rises/falls. See PDF pages 95-98.
- S04 generalizes position sizing by multiplying capital by instrument weight and later by IDM for diversification correction. See PDF pages 119-123.
- S09, S10, and S11 plug capped combined forecasts into the familiar position-sizing equations. See PDF pages 221-222, 253, and 270.

## Implementation-Ready Contract

M1 should later expose these process-level transformations once implementation is separately authorized:

1. Resolve sizing context.
   Required inputs: lane class, instrument identity, completed-bar timestamp, active stack bar convention, capital base, target risk, current held-contract raw price, multiplier, FX rate, pre-validated risk estimate, and source stack.

2. Resolve optional portfolio context.
   Required inputs when applicable: instrument weight and IDM from M3.

3. Resolve optional forecast context.
   Required input when applicable: capped combined forecast from M2. Forecast value must already be capped and source-valid before M1 receives it.

4. Produce desired unrounded contract exposure.
   Output is an unrounded desired contract count in futures contracts.

5. Apply rounding policy.
   Output is desired rounded contract count or fail-closed blockage if rounding policy is unresolved.

6. Emit sizing audit fields.
   Output must preserve all source inputs, timestamp semantics, and blockage reasons for later review.

This is an interface contract only. No executable formula, code path, or test is authorized here.

## Required Inputs

M1 requires these inputs to be locked before implementation or data work:

- Lane class: `SOURCE_NATIVE_FUTURES`.
- Instrument identity and source-native contract mapping.
- Completed-bar timestamp and active stack bar convention.
- Capital base.
- Target risk.
- Current held-contract raw price for sizing.
- Back-adjusted price-difference input if using daily price-point risk.
- Futures multiplier.
- Instrument currency and base/account currency.
- FX conversion value and timestamp convention.
- Risk estimate in annual percentage terms or daily price-point terms.
- Risk-estimate construction lock: fixed S02 risk or S03 variable-risk atoms, including EWMA/span/blend/warm-up/no-lookahead convention where applicable.
- Risk estimate timestamp and no-lookahead proof: only returns completed before sizing timestamp.
- Optional instrument weight.
- Optional IDM.
- Optional capped forecast from M2.
- Contract rounding rule.
- Minimum capital and minimum starting contract-count policy.

## Required Outputs

M1 later implementation must be able to produce:

- Desired unrounded contracts.
- Desired rounded contracts after the locked rounding rule.
- Sizing unit convention used: percentage risk or daily price-point risk.
- Capital, target risk, risk estimate, price, multiplier, FX, weight, IDM, and forecast inputs used.
- Completed-bar timestamp used for every input.
- Blockage reason if any required input is missing, stale, invalid, or unresolved.

## Fail-Closed Rules

M1 must fail closed if any of these are unresolved or invalid:

- Lane class is not `SOURCE_NATIVE_FUTURES`.
- Current held-contract price source is missing when percentage-risk sizing is used.
- Risk estimate is missing, zero, negative, stale, or uses future information.
- The risk estimate has not been pre-validated against the active source atoms before M1 consumes it.
- Current held-contract price, FX, capital, target risk, multiplier metadata, risk estimate, and any applicable weight, IDM, or forecast input are not timestamp-aligned to the sizing timestamp.
- Multiplier, FX, capital, target risk, or any context-applicable weight, IDM, or forecast input is missing or invalid.
- Rounding rule is unresolved.
- Instrument identity or roll/contract mapping is unresolved.
- Minimum-capital rule fails where the downstream lane requires tradable contract granularity.
- Any CFD proxy, adjacent symbol, ETF proxy, or old QuantLab symbol is introduced.

## Open Atoms

These atoms remain unresolved until a later authorized implementation or data-surface gate:

- Exact capital-base policy: fixed notional, current account value, or source-example capital.
- Exact target-risk policy per candidate or portfolio breadth.
- Exact annualization convention where source references differ by context.
- Exact percentage-risk versus daily-price-point sizing form by stack.
- Exact rounding rule. M1 stops at desired exposure; buffer and trade/no-trade decisions must remain in M2 or a separately authorized downstream trade-decision module.
- Exact minimum-capital rule and minimum starting contract-count rule.
- Exact FX timestamp convention.
- Exact handling of negative current futures prices.
- Exact synthetic conformance examples for later authorized implementation tests.

## Downstream Users

M1 is used by:

- S02 fixed-risk single-instrument sizing.
- S03 variable-risk single-instrument sizing.
- S04/P01/P02 multi-instrument portfolio sizing.
- S09 trend forecast-scaled sizing.
- S10 carry forecast-scaled sizing.
- S11 combined trend/carry forecast-scaled sizing.

## Hostile Audit Requirement

Before M1 is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- Source-page faithfulness.
- Correct separation from M2, M3, and M5.
- No formula implementation or code leakage.
- No data, test, diagnostic, backtest, or promotion leakage.
- No CFD, NinjaTrader operational, or old QuantLab contamination.
- Completeness of inputs, outputs, unresolved atoms, and fail-closed rules.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition after patch:

- Blocking finding patched: M1 now requires the risk estimate to be pre-validated against S02/S03 source atoms before M1 consumes it.
- Medium findings patched: optional weight, IDM, and forecast inputs now fail closed only when applicable to the active context; M1 explicitly stops at desired exposure and leaves buffer/trade-decision ownership outside M1.
- Timestamp finding patched: all sizing inputs must be timestamp-aligned to the sizing timestamp.
- Daily over-specificity patched: the spec now uses active stack bar convention while the current clean spine remains daily for S02-S11.

No data, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab, tuning, deployment, trading, or promotion leakage remains authorized by this artifact.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


---

## Source File: `docs/process/CARVER_M2_FORECAST_BLOCK_ARCHITECTURE_MODULE_SPEC_2026-05-28.md`

# Carver M2 Forecast Block Architecture Module Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M2_FORECAST_BLOCK_ARCHITECTURE_MODULE_SPEC_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Define the process-only implementation-ready contract for Carver Module M2:

```text
M2_FORECAST_BLOCK_ARCHITECTURE
```

M2 specifies the common forecast-block architecture used by S09, S10, and S11: raw forecasts, risk normalization, forecast scalars, forecast caps, cost/speed eligibility, forecast weights, forecast diversification multiplier, combined forecast cap, and buffer/trade-decision atoms.

This module spec is not code, not a data lane, not a test lane, not a diagnostic lane, not a backtest lane, not an OOS lane, not a Lockbox lane, not a Forward lane, not a CFD adapter lane, not deployment, not trading, and not promotion.

## Lane Class

Current Carver spine lane class for M2:

```text
SOURCE_NATIVE_FUTURES
```

M2 does not open `CFD_DIRECT` or `CFD_ADAPTER`. Any future adapter use of forecast outputs requires a separate adapter gate after source-native behavior exists.

## Scope

M2 owns:

- Trading-rule forecast identity and style grouping.
- Raw forecast input contract.
- Risk-normalized forecast contract.
- Forecast scalar source tables.
- Individual forecast cap.
- Forecast variation eligibility by cost/speed limit.
- Forecast weights.
- FDM lookup and row-selection rules.
- Combined forecast cap.
- Buffer-zone and trade/no-trade source atoms where inherited by forecast strategies.
- No-lookahead and completed-bar forecast timestamp rules.

M2 does not own:

- Futures position-size arithmetic from capital/risk/multiplier/FX. That belongs to M1.
- Instrument weights, IDM, portfolio aggregation, or universe selection. Those belong to M3.
- Carry curve construction. That belongs to M5.
- Data loading, code implementation, tests, diagnostics, or backtests.

## Source Anchors

- S07 defines a forecast as a value proportional to expected risk-adjusted return and establishes the forecast/trading-rule terminology used by later forecast-block strategies. See `Carver.pdf`, PDF pages 179-180.
- S07 uses daily price-point risk to normalize trend crossover forecasts so forecast values can be compared across time and instruments. See PDF pages 179-180.
- S09 selects EWMAC trend variations 2, 4, 8, 16, 32, and 64 and uses forecast scalars, caps, optimal unrounded position, buffer zone, and trade/no-trade decision. See PDF pages 202-204.
- S09 combines capped forecasts with non-negative forecast weights that sum to 1. See PDF pages 208-209.
- S09 uses a trading-rule cost/speed eligibility rule before allocating forecast weights. The current definition pack records 0.15 SR units as source context, but the exact quote and page reference must be re-page-audited before implementation. See PDF pages 216-218 and the general cost-speed rule on PDF page 112.
- S09 applies FDM to combined trend forecasts, then caps the combined forecast again at absolute value 20. See PDF pages 221-222.
- S10 treats risk-adjusted carry as a forecast because it is expected annual return divided by annualized risk. See PDF page 241.
- S10 smooths carry forecasts over spans 5, 20, 60, and 120 business days, uses forecast scalar 30, caps forecasts, weights eligible spans equally, and applies carry FDM. See PDF pages 247-253.
- S11 states that scaled trading-rule forecasts are building blocks that can be combined because they share a common scale. See PDF pages 264-265.
- S11 uses top-down forecast weighting by style, rule, and variation; trend is divergent, carry is convergent, and the source example uses 60% trend and 40% carry. See PDF pages 265-268.
- S11 provides source table examples for combined trend/carry weights and approximate FDM by number of trading rules. The table-number/page labels for Tables 51 and 52 must be re-page-audited before implementation; interpolation remains blocked unless separately operator-locked before data work.

## Implementation-Ready Contract

M2 should later expose these process-level transformations once implementation is separately authorized:

1. Receive completed-bar source inputs for one instrument and one timestamp.
2. Construct or receive raw forecast values according to the locked rule family.
3. Normalize raw forecasts to risk-adjusted forecast units.
4. Apply source-locked forecast scalar.
5. Apply individual forecast cap.
6. Apply pre-locked cost/speed eligibility to decide which forecast variations are allowed.
7. Assign forecast weights by the locked top-down or table rule.
8. Combine capped forecasts.
9. Apply source-locked FDM.
10. Apply final combined forecast cap.
11. Emit capped combined forecast to M1.
12. Emit buffer/trade-decision atoms when the future implementation lane opens.

This is an interface contract only. No executable forecast implementation, code path, or test is authorized here.

## Source Tables To Lock

S09 trend forecast scalars:

| Filter | Scalar |
| --- | ---: |
| EWMAC2 | 12.1 |
| EWMAC4 | 8.53 |
| EWMAC8 | 5.95 |
| EWMAC16 | 4.10 |
| EWMAC32 | 2.79 |
| EWMAC64 | 1.91 |

S09 trend turnover estimates:

| Filter | Turnover per year |
| --- | ---: |
| EWMAC2 | 98.5 |
| EWMAC4 | 50.2 |
| EWMAC8 | 25.4 |
| EWMAC16 | 13.2 |
| EWMAC32 | 7.6 |
| EWMAC64 | 5.2 |

S09 trend FDM rows:

| Allowed filters | Forecast weight per filter | FDM |
| --- | ---: | ---: |
| EWMAC2, 4, 8, 16, 32, 64 | 0.167 | 1.26 |
| EWMAC4, 8, 16, 32, 64 | 0.2 | 1.19 |
| EWMAC8, 16, 32, 64 | 0.25 | 1.13 |
| EWMAC16, 32, 64 | 0.333 | 1.08 |
| EWMAC32, 64 | 0.50 | 1.03 |
| EWMAC64 | 1.0 | 1.0 |

S10 carry source values:

| Item | Value |
| --- | ---: |
| Carry forecast scalar | 30 |
| Carry spans | 5, 20, 60, 120 business days |
| Carry5 turnover | 5.75 |
| Carry20 turnover | 3.12 |
| Carry60 turnover | 1.82 |
| Carry120 turnover | 1.22 |

S10 carry FDM rows:

| Allowed carry spans | Forecast weight per span | FDM |
| --- | ---: | ---: |
| Carry5, 20, 60, 120 | 0.25 | 1.04 |
| Carry20, 60, 120 | 0.333 | 1.03 |
| Carry60, 120 | 0.5 | 1.02 |
| Carry120 | 1.0 | 1.0 |

S11 shared source values:

- Trend style: divergent.
- Carry style: convergent.
- Source style mix: 60% trend, 40% carry.
- Table 51 weights: source example rows to re-page-audit and lock before implementation.
- Table 52 FDM: approximate FDM by number of trading rules, with table-number/page labels to re-page-audit before implementation; interpolation is not authorized unless separately operator-locked before data work.

## Required Inputs

M2 requires these inputs to be locked before implementation or data work:

- Lane class: `SOURCE_NATIVE_FUTURES`.
- Completed-bar timestamp.
- Instrument identity.
- Forecast family: EWMAC trend, carry, or combined trend/carry.
- Input price series convention.
- Risk normalization convention.
- Forecast scalar source.
- Individual forecast cap.
- Cost-per-trade source and speed-limit rule.
- Turnover table or locked turnover source.
- Forecast variation set.
- Forecast weight rule.
- FDM table and row-selection rule.
- Combined forecast cap.
- Buffer rule and buffer-size source, if the downstream strategy uses buffered trading.

## Required Outputs

M2 later implementation must be able to produce:

- Raw forecast per rule variation.
- Scaled forecast per rule variation.
- Individually capped forecast per rule variation.
- Eligibility status per variation.
- Forecast weight per retained variation.
- Pre-FDM combined forecast.
- FDM used.
- Post-FDM combined forecast.
- Final capped combined forecast for M1.
- Blockage reason if forecast construction, eligibility, weighting, FDM, cap, or buffer rule is unresolved.

## Fail-Closed Rules

M2 must fail closed if:

- Lane class is missing or is not exactly `SOURCE_NATIVE_FUTURES`.
- Any forecast uses incomplete bars or future information.
- Forecast scalar, cap, speed limit, turnover, weight, or FDM source is unresolved.
- Cost eligibility cannot be determined but is required for the strategy.
- A required carry forecast needs M5 output that is unavailable or blocked.
- No eligible forecast variation remains and the candidate has no pre-locked fallback.
- S07/S08 trend components are promoted as standalone candidates through this module.
- Any parameter is changed after seeing results.

## Open Atoms

These atoms remain unresolved until a later authorized implementation gate:

- Exact EWMA calculation convention and warm-up behavior.
- Exact buffer-zone formula and trade/no-trade boundary.
- Exact handling of instruments with partial forecast-family availability.
- Exact Table 51 row-selection rule.
- Exact Table 51 table-number/page-label verification.
- Exact Table 52 interpolation policy.
- Exact Table 52 table-number/page-label verification.
- Exact synthetic conformance examples for later authorized implementation tests.

## Downstream Users

M2 is used by:

- S09 multiple trend following.
- S10 basic carry, where raw carry comes from M5.
- S11 combined carry and trend.
- Later Part Two and Part Three forecast-block extensions, only if separately authorized.

## Hostile Audit Requirement

Before M2 is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- Source-page faithfulness.
- Correct separation from M1, M3, and M5.
- Correct non-advancement of S07/S08 standalone status.
- No code, data, test, diagnostic, backtest, or promotion leakage.
- No tuning leakage after results.
- Completeness of inputs, outputs, unresolved atoms, and fail-closed rules.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition:

- No blocking findings against the M2 artifact.
- Source tables, S07/S08 sleeve non-advancement, module boundaries, and sensitive-stage non-authorization language were found process-safe.
- Residual watch items remain open atoms: EWMA convention/warm-up, buffer-zone formula, partial forecast-family handling, Table 51 row selection, Table 52 interpolation policy, and synthetic conformance examples.

No data, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab, tuning, deployment, trading, or promotion leakage remains authorized by this artifact.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


---

## Source File: `docs/process/CARVER_M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION_MODULE_SPEC_2026-05-28.md`

# Carver M3 Multi-Instrument Portfolio Construction Module Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION_MODULE_SPEC_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Define the process-only implementation-ready contract for Carver Module M3:

```text
M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION
```

M3 specifies the shared portfolio construction atoms for S04, P01, P02, and future Jumbo portfolios: instrument universe, instrument weights, top-down allocation, IDM, portfolio breadth target-risk rules, eligibility, portfolio synchronization, and aggregation boundaries.

This module spec is not code, not a data lane, not a test lane, not a diagnostic lane, not a backtest lane, not an OOS lane, not a Lockbox lane, not a Forward lane, not a CFD adapter lane, not deployment, not trading, and not promotion.

## Scope

M3 owns:

- Portfolio instrument universe declaration.
- Instrument weights as risk-capital weights.
- Top-down asset-class/group/instrument weight construction.
- Portfolio-level capital and target-risk policy atoms.
- Instrument diversification multiplier.
- Portfolio minimum-capital constraints.
- Instrument eligibility: cost, liquidity, source availability, and minimum capital.
- Completed-bar synchronization across instruments.
- Portfolio aggregation boundary and fail-closed rules.

M3 does not own:

- Single-instrument contract sizing arithmetic. That belongs to M1.
- Forecast construction and FDM. That belongs to M2.
- Carry curve construction. That belongs to M5.
- Data loading, code implementation, tests, diagnostics, or backtests.

## Source Anchors

- S04 moves from single-instrument S03 to portfolios where each sub-strategy is a version of S03 trading a different instrument. See `Carver.pdf`, PDF page 118.
- S04 says capital chunks become instrument risk allocations because each sub-strategy has approximately the same risk. See PDF page 118.
- Risk parity P01 splits capital 50/50 between S&P 500 micro futures and US 10-year bond futures. See PDF pages 119-120.
- S04 introduces IDM to correct for diversification and scale aggregate portfolio risk toward the target. See PDF pages 122-123.
- P02 All Weather uses instrument weights as risk allocations: 25% S&P 500 micro, 12.5% US 10-year, 12.5% US 5-year, 12.5% WTI Crude Oil mini, 12.5% Corn, and 25% Gold micro. See PDF page 125.
- S04 generalized risk premia uses cost, liquidity, and minimum-capital eligibility rules. See PDF page 127.
- S04 modifies minimum capital for instrument weights and IDM. See PDF pages 127-128.
- S04 handcrafting allocates first by asset class, then group, then instrument. See PDF pages 130-135.
- S04 Table 16 supplies approximate IDM values by number of instruments and warns the table assumes a relatively diversified instrument set. See PDF page 135.
- S04 gives an automatic selection procedure based on possible instruments, lowest-cost first instrument, trial portfolios, weights, IDM, minimum-capital checks, expected SR from costs/correlations, and a 10% stop rule. See PDF pages 135-140.
- S04 defines the Jumbo portfolio as 102 instruments meeting cost/liquidity thresholds and at least one year of data, using USD 50 million capital and handcrafted weights. The definition pack records IDM 2.47 as source context for the book example, but the exact value/page quote must be re-page-audited before implementation. See PDF page 141.
- S04 advises target-risk levels by portfolio breadth: 10% for one instrument, interpolate 10%-20% for two to six instruments, 20% only with all seven asset classes, and up to 25% only with at least two instruments from each asset class. See PDF pages 143-144.

## Implementation-Ready Contract

M3 should later expose these process-level transformations once implementation is separately authorized:

1. Receive an authorized portfolio intent.
2. Validate source-native instrument identities and local mapping lock status.
3. Apply the locked universe/eligibility rules.
4. Construct or validate instrument weights.
5. Resolve portfolio target-risk policy and capital base.
6. Resolve IDM source and value/rule.
7. Emit per-instrument portfolio context for M1: weight, IDM, capital base, and target risk.
8. Emit synchronization and aggregation rules for future child lanes.
9. Fail closed on missing/ineligible instruments or unresolved weight/IDM/eligibility atoms.

This is an interface contract only. No executable portfolio implementation, selection run, data query, or backtest is authorized here.

## Source Tables And Examples

P01 source example:

| Instrument | Weight | Appendix C code |
| --- | ---: | --- |
| S&P 500 micro future | 50% | `MES` |
| US 10-year bond future | 50% | `ZN` |

P02 source example:

| Instrument | Weight | Appendix C code |
| --- | ---: | --- |
| S&P 500 micro future | 25.0% | `MES` |
| US 10-year bond future | 12.5% | `ZN` |
| US 5-year bond future | 12.5% | `ZF` |
| WTI Crude Oil mini future | 12.5% | `QM` |
| Corn future | 12.5% | `ZC` |
| Gold micro future | 25.0% | `MGC` |

Appendix C broker codes may differ from local or official exchange codes. They are source-reference labels, not data-lane authorization; every future local symbol mapping, source-native contract identity, roll rule, and no-silent-substitution decision must be locked before data work.

## Required Inputs

M3 requires these inputs to be locked before implementation or data work:

- Portfolio ID and source pages.
- Lane class: `SOURCE_NATIVE_FUTURES`.
- Instrument universe.
- Source-native instrument identity for every member.
- Local symbol mapping status for every member.
- Asset class, group, and instrument classification when using handcrafted weights.
- Instrument weights or deterministic weight-construction rule.
- Portfolio capital base.
- Portfolio target-risk rule.
- IDM source and exact value/rule.
- IDM table validity check for diversification breadth.
- Cost eligibility rule.
- Liquidity eligibility rule.
- Minimum-capital rule.
- Completed-bar synchronization rule across instruments.
- Fail-closed behavior for unavailable or ineligible members.

## Required Outputs

M3 later implementation must be able to produce:

- Locked portfolio member list.
- Instrument weight per member.
- Instrument eligibility status and blockage reason.
- Portfolio target risk and capital base.
- IDM used and source.
- Per-instrument context for M1.
- Portfolio synchronization rule.
- Portfolio aggregation convention for completed daily PnL, only after separately authorized.

## Fail-Closed Rules

M3 must fail closed if:

- Lane class is missing or is not exactly `SOURCE_NATIVE_FUTURES`.
- Any instrument identity is unresolved.
- Any local mapping is silently substituted.
- M3 is used as a substitute for a separately locked complete portfolio brief, member list, and portfolio-specific source-page lock.
- Instrument weights do not sum according to the locked rule.
- IDM source or applicability is unresolved.
- Portfolio breadth does not support requested target risk.
- Cost, liquidity, or minimum-capital eligibility cannot be evaluated once required.
- Correlation matrices or expected-SR inputs are inspected before being pre-locked.
- A portfolio drops, rescues, reweights, or adds members after seeing results.
- Any old QuantLab symbol, CFD proxy, ETF proxy, or adjacent ticker is used as authority.

## Open Atoms

These atoms remain unresolved until a later authorized implementation or data-surface gate:

- Exact source-native universe for P03/P04 and later portfolios.
- Exact local symbol mapping for Appendix C broker codes.
- Exact asset-class/group taxonomy for all 102 Jumbo instruments.
- Exact IDM policy: source examples, Table 16, calculated IDM, or blocked.
- Exact source-example IDM value/page verification for P02 and Jumbo before those values are quoted as locked authority.
- Exact correlation matrix source if automatic selection is ever authorized.
- Exact expected-SR assumption if automatic selection is ever authorized.
- Exact portfolio aggregation convention for missing instruments and staggered first usable dates.
- Exact synthetic conformance examples for later authorized implementation tests.

## Downstream Users

M3 is used by:

- S04 buy-and-hold portfolio construction.
- P01 risk parity.
- P02 All Weather.
- P03/P04 and later Jumbo portfolio briefs if separately authorized.
- S09/S10/S11 portfolio children if separately authorized.

## Hostile Audit Requirement

Before M3 is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- Source-page faithfulness.
- Correct separation from M1, M2, and M5.
- No portfolio execution, data selection, or backtest leakage.
- No post-result instrument selection or reweighting leakage.
- Correct Appendix C code warning.
- Completeness of inputs, outputs, unresolved atoms, and fail-closed rules.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition after patch:

- No blocking findings against the M3 artifact.
- Non-blocking lane-class finding patched: M3 now fails closed unless lane class is exactly `SOURCE_NATIVE_FUTURES`.
- Non-blocking portfolio-independence finding patched: M3 cannot substitute for a separately locked portfolio brief, member list, and source-page lock.
- Appendix C warning strengthened to require later local mapping, source-native identity, roll-rule, and no-silent-substitution locks before data work.

No data, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab, tuning, deployment, trading, or promotion leakage remains authorized by this artifact.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


---

## Source File: `docs/process/CARVER_M5_FUTURES_CURVE_AND_CARRY_CONSTRUCTION_MODULE_SPEC_2026-05-28.md`

# Carver M5 Futures Curve And Carry Construction Module Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M5_FUTURES_CURVE_CARRY_CONSTRUCTION_MODULE_SPEC_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Define the process-only implementation-ready contract for Carver Module M5:

```text
M5_FUTURES_CURVE_AND_CARRY_CONSTRUCTION
```

M5 specifies the futures-curve and carry-construction atoms needed by S10 and later carry variants: held-contract selection, comparison-contract selection, raw carry, annualization, risk adjustment, seasonality/wrong-sign blockages, carry smoothing inputs, and fail-closed rules.

This module spec is not code, not a data lane, not a test lane, not a diagnostic lane, not a backtest lane, not an OOS lane, not a Lockbox lane, not a Forward lane, not a CFD adapter lane, not deployment, not trading, and not promotion.

## Scope

M5 owns:

- Futures curve contract identity requirements.
- Held-contract versus comparison-contract rules.
- Nearer versus further-out carry comparison.
- Expiry-distance annualization atoms.
- Raw carry from synchronized futures contract prices.
- Risk-adjusted carry as forecast input for M2.
- Fixed-month commodity rules where source requires them.
- Sparse second-contract history and roll-day-only carry blockages.
- Seasonal and wrong-sign carry blockages.
- Fail-closed behavior for missing curve data.

M5 does not own:

- Carry forecast smoothing, scalar, cap, weights, or FDM. Those belong to M2 after M5 emits raw/risk-adjusted carry.
- Position sizing. That belongs to M1.
- Portfolio construction. That belongs to M3.
- Data loading, market-row parsing, code implementation, tests, diagnostics, or backtests.

## Source Anchors

- S10 defines carry as the component of futures excess return beyond spot price changes. See `Carver.pdf`, PDF pages 232-233.
- S10 identifies carry sources by asset class: equities, bonds, FX, STIR/volatility, metals, and other commodities. See PDF pages 233-237.
- S10 warns that carry can be hazardous due to spot drag and negative-skew risks. See PDF page 237.
- Expected carry can be measured by comparing futures prices instead of spot prices, using two synchronized contracts on the same exchange. See PDF page 238.
- If holding a further-out contract, carry can be calculated against a nearer contract. If holding the front contract, carry may require a further-out contract. See PDF pages 238-239.
- Raw carry must be annualized by the time between expiries, approximated by month differences. See PDF page 240.
- Annualized carry is risk-adjusted by dividing by annualized standard deviation in price units or equivalent percentage form. See PDF pages 240-241.
- Risk-adjusted carry naturally produces a forecast because it is expected annual return divided by annualized risk. See PDF page 241.
- Sparse second-contract history, noisy curve differences, and poor data feed behavior are source risks. See PDF pages 242-243.
- Natural Gas illustrates real seasonal carry while WTI Crude uses a fixed December contract to avoid some seasonality. See PDF pages 243 and 252.
- Bund/Bobl/Bono and some non-US equity futures illustrate wrong-sign seasonal carry when first/second contract comparisons are imprecise. See PDF pages 244-246.
- S10 uses smoothing to reduce noise and seasonal effects, but the smoothing belongs to the forecast block after M5 emits carry inputs. See PDF pages 246-248.

## Implementation-Ready Contract

M5 should later expose these process-level transformations once implementation is separately authorized:

1. Receive one instrument, one completed-bar timestamp, and the locked contract selection context.
2. Resolve the held contract.
3. Resolve the comparison contract: nearer, further-out, or fail-closed blockage.
4. Validate synchronized completed prices for held and comparison contracts.
5. Calculate raw carry source value according to the locked source convention.
6. Annualize raw carry using the locked expiry-distance convention.
7. Risk-adjust annualized carry using the locked price-risk input.
8. Emit risk-adjusted carry forecast input to M2.
9. Emit carry audit fields and blockage reasons.

This is an interface contract only. No executable carry implementation, curve query, data export, or test is authorized here.

## Required Inputs

M5 requires these inputs to be locked before implementation or data work:

- Lane class: `SOURCE_NATIVE_FUTURES`.
- Instrument identity.
- Contract calendar and expiry calendar.
- Held-contract selection rule.
- Comparison-contract selection rule.
- Raw carry sign convention for nearer-versus-further comparisons.
- Completed daily bar timestamp for every curve contract.
- Price source for raw contract prices.
- Synchronization rule for held and comparison contracts.
- Expiry month-distance convention.
- Price-risk estimate from M1/S03 risk machinery.
- Fixed-month rule where applicable.
- Sparse-history rule.
- Seasonal/wrong-sign carry policy.
- Fail-closed policy for missing, stale, or illiquid curve contracts.

## Required Outputs

M5 later implementation must be able to produce:

- Held contract identity.
- Comparison contract identity.
- Raw carry price difference with sign convention.
- Expiry distance used.
- Annualized carry.
- Risk-adjusted carry.
- Carry timestamp and input timestamps.
- Seasonal/wrong-sign warning or blockage status.
- Blockage reason if carry cannot be constructed.

## Fail-Closed Rules

M5 must fail closed if:

- Lane class is missing or is not exactly `SOURCE_NATIVE_FUTURES`.
- Held contract identity is unresolved.
- Comparison contract identity is unresolved.
- Held and comparison prices are not synchronized completed bars.
- Contract expiry dates or month-distance convention are missing.
- Carry calculation would use spot data without a locked source rule.
- Carry calculation would use stale, missing, or partial curve prices.
- A known wrong-sign seasonal carry issue is unresolved.
- Fixed-month commodity rule is required but unresolved.
- Any curve leg is silently substituted with a CFD, ETF, adjacent proxy, or old QuantLab symbol.

## Open Atoms

These atoms remain unresolved until a later authorized implementation or data-surface gate:

- Exact curve contract availability in local source-native data.
- Exact held-contract rule by asset class/instrument.
- Exact comparison-contract rule by asset class/instrument.
- Exact raw carry sign convention for nearer-versus-further comparisons.
- Exact handling of roll days and roll-day-only carry readings.
- Exact expiry calendar source.
- Exact seasonality classification table.
- Exact wrong-sign carry blockage list.
- Exact fixed-month commodity table.
- Exact synthetic conformance examples for later authorized implementation tests.

## Downstream Users

M5 is used by:

- S10 basic carry.
- S11 combined carry and trend through S10 carry blocks.
- Future accurate carry, cross-sectional carry, and calendar/RV lanes only if separately authorized.

## Hostile Audit Requirement

Before M5 is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- Source-page faithfulness.
- Correct separation from M1, M2, and M3.
- No curve data access, implementation, test, diagnostic, backtest, or promotion leakage.
- Correct handling of seasonal/wrong-sign carry as unresolved or fail-closed.
- Completeness of inputs, outputs, unresolved atoms, and fail-closed rules.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition after patch:

- No blocking findings against the M5 artifact.
- Non-blocking raw-carry-sign finding patched: raw carry sign convention is now an explicit required input, output qualifier, and open atom.
- Non-blocking lane-class finding patched: M5 now requires and fails closed on exact `SOURCE_NATIVE_FUTURES` lane class.
- Source faithfulness, M1/M2/M3 boundaries, smoothing ownership, seasonal/wrong-sign handling, and sensitive-stage non-authorization language were found process-safe.

No data, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab, tuning, deployment, trading, or promotion leakage remains authorized by this artifact.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


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

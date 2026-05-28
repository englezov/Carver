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

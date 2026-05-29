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
- S09 uses a trading-rule cost/speed eligibility rule before allocating forecast weights. Opus 4.7 later verified the `0.15 SR` cost-units threshold at PDF page 216, but it has not yet been transcribed as a hash-bound machine-readable production lock. Per-instrument cost eligibility from prevalidated costs and turnover policy remains closed. See PDF pages 216-218 and the general cost-speed rule on PDF page 112.
- S09 applies FDM to combined trend forecasts, then caps the combined forecast again at absolute value 20. See PDF pages 221-222.
- S10 treats risk-adjusted carry as a forecast because it is expected annual return divided by annualized risk. See PDF page 241.
- S10 smooths carry forecasts over spans 5, 20, 60, and 120 business days, uses forecast scalar 30, caps forecasts, weights eligible spans equally, and applies carry FDM. See PDF pages 247-253.
- S11 states that scaled trading-rule forecasts are building blocks that can be combined because they share a common scale. See PDF pages 264-265.
- S11 uses top-down forecast weighting by style, rule, and variation; trend is divergent, carry is convergent, and the source example uses 60% trend and 40% carry. See PDF pages 265-268.
- S11 provides source table examples for combined trend/carry weights and approximate FDM by number of trading rules. Opus 4.7 later verified Table 51 at PDF page 268 and Table 52 plus interpolation policy at PDF page 269, but they have not yet been transcribed as hash-bound machine-readable production locks; production row selection and interpolation use remain blocked unless separately operator-locked before data work.

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

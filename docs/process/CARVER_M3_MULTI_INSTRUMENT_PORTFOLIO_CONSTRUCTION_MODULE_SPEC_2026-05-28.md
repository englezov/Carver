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

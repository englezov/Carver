# Portfolio Graph: P01, P02, P05, P06, P07

Date: 2026-05-29

Status:

```text
OPUS_47_AUDIT_INPUT_PORTFOLIO_GRAPH_P01_P02_P05_P06_P07_NOT_DATA_NOT_BACKTEST
```

## Purpose

Summarize the not-yet-Opus-audited Carver portfolio graph: P01/P02 final package if no Opus result exists, plus P05/P06/P07 complete Part One synthetic portfolio surfaces.

This file is an audit input only. It authorizes no implementation, tests, data work, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, or promotion.

## Source Areas To Inspect

Use `00_Carver.pdf` as source authority.

| Area | PDF pages | Audit use |
| --- | ---: | --- |
| Strategy Four portfolio construction | 118-144 | P01/P02 examples, instrument weights, IDM, target risk, Jumbo portfolio construction. |
| Strategy Nine multiple trend | 201-227 | P05 trend portfolio source dependency. |
| Strategy Ten basic carry | 232-259 | P06 carry portfolio source dependency. |
| Strategy Eleven combined carry/trend | 264-275 | P07 combined trend/carry portfolio source dependency. |
| Appendix C Jumbo universe | 690-695 | P05/P06/P07 complete 102-instrument Jumbo universe source. |
| Strategy Two/Three preliminaries | 70-88, 95-115 | Risk target, annual risk, risk-adjusted cost, liquidity, minimum capital. |

## P01/P02 Final Package

Completion record:

```text
docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md
```

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P01_P02_PORTFOLIO_PACKAGE_COMPLETE_REAL_DATA_BLOCKED
```

Prepared Opus packet:

```text
GPT/OPUS_FINAL_P01_P02_AUDIT_PACK_2026-05-29
```

Repo finding:

No separate stored Opus result file was found for this packet during preparation of the current audit packet. Treat P01/P02 final package as not covered by a recorded Opus result unless the operator supplies an external result.

P01 package facts:

- P01 book identity: Strategy Four risk-parity example using S&P 500 micro future and US 10-year bond future.
- P01 exact process tickers: `MES` and `ZN`.
- P01 weights: 50/50 risk allocation.
- `ES` must not substitute for `MES`.

P02 package facts:

- P02 book identity: Carver's take on the "All Weather" portfolio.
- P02 book descriptive labels: S&P 500 micro futures, US 10-year bond futures, US 5-year bond futures, WTI Crude Oil mini futures, Corn futures, and Gold micro futures.
- P02 exact process tickers: `MES`, `ZN`, `ZF`, `QM`, `ZC`, `MGC`.
- P02 weights: `25 / 12.5 / 12.5 / 12.5 / 12.5 / 25`.

Ticker mapping provenance:

| Process ticker | Book descriptive label | Strategy Four source | Appendix C source |
| --- | --- | --- | --- |
| `MES` | S&P 500 micro future(s) | PDF pages 120 and 125 | Table 174, PDF pages 691-692 |
| `ZN` | US 10-year bond future(s) | PDF pages 120 and 125 | Table 172, PDF pages 690-691 |
| `ZF` | US 5-year bond futures | PDF page 125 | Table 172, PDF pages 690-691 |
| `QM` | WTI Crude Oil mini futures | PDF page 125 | Table 182, PDF page 695 |
| `ZC` | Corn futures | PDF page 125 | Table 183, PDF page 695 |
| `MGC` | Gold micro futures | PDF page 125 | Table 181, PDF page 694 |

The descriptive-label-to-ticker mapping is a source-lock atom. It is not a book-native equation and must remain explicit in any future P01/P02 real-data readiness packet.

Current provider mapping state:

```text
ZN 06-26 ZN JUN26 -> 4470301
```

Observed but non-portfolio archaeology:

```text
ES 06-26 ES JUN26 -> 3570919
```

Unresolved:

```text
MES 06-26
ZF  06-26
QM  06-26
ZC  06-26
MGC 06-26
```

P01/P02 boundaries:

- Direct daily bars are preferred when future data is authorized.
- Minute-to-daily derivation is fallback only and requires a direct-daily-blocked artifact.
- Quarantined JSON chart response normalization must be request-bound.
- Completion report fails closed until all real-data prerequisites are artifact-locked.
- Continuous/roll/back-adjustment placeholders refuse to build a production series until separate source rules are locked.

Opus should verify:

- P01/P02 instrument sets and weights match source.
- No ES-for-MES substitution is smuggled.
- Completed-bar assumptions and direct-daily preference are source/governance safe.
- P01/P02 real-data blockers are honestly stated.

## P05 Complete Trend Portfolio

Source packet:

```text
docs/process/CARVER_P05_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
```

Conformance artifact:

```text
docs/process/CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_2026-05-29.md
```

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Implementation surface:

```text
src/carver/spine/p05.py
tests/test_p05_complete_trend_portfolio_synthetic.py
```

P05 identity:

P05 is a Carver process alias for Strategy Nine multiple trend following applied over the Jumbo futures portfolio source frame. It is not a book-native label.

Source basis:

- Strategy Four portfolio construction machinery.
- Strategy Nine multiple trend following.
- Appendix C Jumbo universe.
- Strategy Two/Three risk, cost, liquidity, and minimum-capital vocabulary.

Synthetic pipeline:

```text
locked synthetic P05 member identity and taxonomy
locked synthetic S09 EWMAC forecast-block outputs
locked synthetic or source-cited capital, target risk, IDM, price risk, FX, and cost eligibility inputs
-> source-shaped top-down handcrafted instrument weights
-> per-member eligible EWMAC speed set
-> Strategy Nine equal forecast weights
-> Strategy Nine FDM row
-> final forecast cap
-> M1 position-sizing input arithmetic
-> complete-P05 desired position inputs only
```

Verification:

```text
Focused P05 synthetic tests: 8/8 passed
Full synthetic regression at that gate: 139/139 passed
```

Lean hostile audit:

```text
docs/process/CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_HOSTILE_AUDIT_RESULT_2026-05-29.md
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_CODE_SCOPE
```

## P06 Complete Carry Portfolio

Source packet:

```text
docs/process/CARVER_P06_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
```

Conformance artifact:

```text
docs/process/CARVER_P06_COMPLETE_CARRY_PORTFOLIO_CONFORMANCE_2026-05-29.md
```

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P06_COMPLETE_CARRY_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Implementation surface:

```text
src/carver/spine/p06.py
tests/test_p06_complete_carry_portfolio_synthetic.py
```

P06 identity:

P06 is a Carver process alias for Strategy Ten basic carry applied over the Jumbo futures portfolio source frame. It is not a book-native label.

Source basis:

- Strategy Ten basic carry.
- Strategy Four portfolio construction machinery.
- Appendix C Jumbo universe.
- Strategy Nine multiple-rule weighting/FDM framework where Strategy Ten reuses it.
- Strategy Two/Three risk, cost, liquidity, and minimum-capital vocabulary.

Synthetic pipeline:

```text
locked synthetic P06 member identity and taxonomy
locked synthetic S10 carry forecast-block outputs
locked synthetic or source-shaped capital, target risk, IDM, price risk, FX, and cost eligibility inputs
-> source-shaped top-down handcrafted instrument weights
-> per-member eligible carry span set
-> Strategy Ten equal forecast weights
-> Strategy Ten carry FDM row
-> final forecast cap
-> M1 position-sizing input arithmetic
-> complete-P06 desired position inputs only
```

Verification:

```text
Focused P06 synthetic tests: 8/8 passed
Full synthetic regression at that gate: 147/147 passed
```

Lean hostile audit:

```text
docs/process/CARVER_P06_COMPLETE_CARRY_PORTFOLIO_CONFORMANCE_HOSTILE_AUDIT_RESULT_2026-05-29.md
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_CODE_SCOPE
```

## P07 Complete Combined Trend/Carry Portfolio

Source packet:

```text
docs/process/CARVER_P07_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
```

Conformance artifact:

```text
docs/process/CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_2026-05-29.md
```

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Implementation surface:

```text
src/carver/spine/p07.py
tests/test_p07_complete_combined_trend_carry_portfolio_synthetic.py
```

P07 identity:

P07 is a Carver process alias for Strategy Eleven combined carry and trend applied over the Jumbo futures portfolio source frame. It is not a book-native label.

Source basis:

- Strategy Eleven combined carry and trend.
- Strategy Nine multiple trend following.
- Strategy Ten basic carry.
- Strategy Four portfolio construction machinery.
- Appendix C Jumbo universe.
- Strategy Two/Three risk, cost, liquidity, and minimum-capital vocabulary.

Synthetic pipeline:

```text
locked synthetic P07 member identity and taxonomy
locked synthetic S11 combined carry/trend forecast outputs
locked synthetic or source-shaped capital, target risk, IDM, price risk, FX, and cost eligibility inputs
-> source-shaped top-down handcrafted instrument weights
-> final forecast cap validation
-> M1 position-sizing input arithmetic
-> complete-P07 desired position inputs only
```

P07 explicitly consumes locked synthetic S11 combined forecasts. It does not combine P05 and P06 desired-position outputs.

Verification:

```text
Focused P07 synthetic tests: 8/8 passed
Full synthetic regression at that gate: 155/155 passed
```

Lean hostile audit:

```text
docs/process/CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_HOSTILE_AUDIT_RESULT_2026-05-29.md
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_CODE_SCOPE
```

## Shared P05/P06/P07 Source Commitments

P05/P06/P07 share these source-shaped claims:

- All are `SOURCE_NATIVE_FUTURES`.
- All use the Jumbo futures portfolio source frame.
- Appendix C Tables 172-183, PDF pages 690-695, are the complete 102-instrument universe source.
- Instrument weighting method is top-down handcrafting inherited from Strategy Four.
- Jumbo IDM reference is 2.47, but production use still requires exact value/page verification or a separate lock.
- Book reference target risk is 20 percent annual standard deviation, but operator capital remains closed.
- Synthetic surfaces may use locked toy members and taxonomy.
- Production complete-portfolio claims require Appendix C transcription and readiness locks.

## Shared Production Blocks

The following remain blocked for P05/P06/P07 production claims:

- Exact complete 102-member Appendix C transcription or hash-bound machine-readable universe.
- Local provider mapping for every member.
- Source-native contract identity for every member.
- Session calendar and completed-bar rule for every member.
- Roll and back-adjustment artifacts.
- Annual risk and daily price-risk source for every member.
- FX source for non-USD members.
- Cost source and risk-adjusted cost for every member.
- Per-member trend and/or carry eligibility.
- Carry curve-leg availability and production carry construction where needed.
- Production raw-carry sign convention, fixed-month policy, seasonal policy, and wrong-sign policy where relevant.
- Liquidity validation.
- Minimum-capital validation.
- Exact group taxonomy for complete 102-member handcrafting weights.
- Production IDM policy.
- Operator capital base if any non-toy capital is used.
- Missing-member behavior beyond fail-closed rejection.
- Rounding and buffering.
- Trade/no-trade decisions.
- Aggregation, returns, PnL, Sharpe, drawdown, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Post-P07 Decision

Decision artifact:

```text
docs/process/CARVER_POST_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_NEXT_STEP_DECISION_2026-05-29.md
```

Selected next gate:

```text
PART_ONE_JUMBO_PORTFOLIO_UNIVERSE_AND_READINESS_SHAPE_GATE_DRAFT
```

Reason:

P05/P06/P07 synthetic portfolio shape is complete. The common blocker is now the shared production-readiness map: Appendix C transcription, provider mapping, contract identity, roll/session/completed-bar rules, risk/FX/cost readiness, trend/carry eligibility readiness, missing-member policy, and audit requirements before any data or implementation gate.

## Opus Questions For Portfolio Graph

1. Is P01/P02 final package source-faithful and governance-safe if no stored Opus result exists?
2. Are P05/P06/P07 correctly described as Carver process aliases rather than book-native labels?
3. Are P05/P06/P07 dependencies source-faithful: S09 for P05, S10 for P06, S11 direct combined forecasts for P07?
4. Does P07 correctly avoid combining P05/P06 desired-position outputs?
5. Are Appendix C, weights, IDM, target risk, eligibility, cost, risk, FX, and readiness atoms separated from synthetic conformance?
6. Does the post-P07 decision correctly choose Appendix C/readiness mapping before data work?

## Non-Authorization

This file authorizes no code edits, no tests, no data access, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Opus execution by itself, no remote push, and no GitHub action.

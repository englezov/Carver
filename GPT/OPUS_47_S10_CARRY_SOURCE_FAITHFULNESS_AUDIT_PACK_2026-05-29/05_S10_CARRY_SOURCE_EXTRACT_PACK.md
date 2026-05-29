# S10 Carry Source Extract Pack

Date: 2026-05-29

Status:

```text
SOURCE_SUMMARY_FOR_OPUS_AUDIT_NOT_PIPELINE_AUTHORIZATION
```

## Purpose

This file is the bounded source pack for an Opus 4.7 source-faithfulness audit of the Carver S10/M5 carry surface and the post-S10/M5 next-step decision.

The entire book is not copied into this audit packet. `Carver.pdf` remains the local reference copy in the Carver workspace and is intentionally excluded from Git-oriented artifacts. This source pack records only narrow, page-cited S10 carry facts needed for audit triage.

Page references below are PDF page numbers from:

```text
C:\Users\openclaw\Desktop\Carver\Carver.pdf
```

## Source Points For Audit

### S10 Framing

- PDF page 232 introduces Strategy Ten as basic carry and frames carry as a risk premium distinct from trend following.
- PDF page 232 says carry should be used carefully and is later combined with trend following in Strategy Eleven.
- PDF page 233 frames Strategy Ten as trading one or more instruments with variable-risk-scaled positions, scaled by forecasted carry strength.
- Audit implication: S10/M5 may construct a carry forecast input, but S11 combination must remain closed until the full S10 carry forecast block is source-locked.

### Futures-Curve Carry Measurement

- PDF pages 234-238 explain carry through the futures curve and motivate using different contract expiries to estimate expected carry.
- PDF page 238 says expected carry can be measured by comparing the current future and spot, but spot data is often difficult or inconvenient.
- PDF page 238 says comparing two futures contracts is useful because the contracts trade on the same exchange and daily closing prices are synchronized.
- PDF pages 238-239 describe using a further-out contract when holding the front contract and using a nearer contract when holding a further-out contract.
- Audit implication: production M5 must lock held/comparison contract roles and sign convention from the source. The current synthetic M5 implementation deliberately does not claim the production sign convention.

### Annualization

- PDF page 240 says the price difference between two contracts reflects carry over the time between expiries.
- PDF page 240 says raw carry should be annualized so instruments with monthly, quarterly, or irregular roll spacing can be compared.
- PDF page 240 says the time between expiries can be approximated using the difference in months as a fraction of a year, even though exact days could be used.
- Audit implication: the current synthetic M5 requirement for a locked expiry distance in years is source-compatible as a construction atom, but it does not lock production expiry calendar rules.

### Risk Adjustment And Forecast Interpretation

- PDF pages 240-241 say annualized carry in price units should be divided by annualized standard deviation of returns in price units to compare carry across instruments.
- PDF page 241 says the risk-adjusted carry measure naturally produces a forecast because carry is an expected annual return divided by annualized standard deviation.
- Audit implication: a synthetic output named `risk_adjusted_carry` is compatible with an input into later forecast machinery, but should not be treated as a complete trading signal, position, or performance result.

### Noise, Seasonality, And Wrong-Sign Risk

- PDF page 242 describes carry estimates as noisy and sometimes affected by poor data.
- PDF page 243 describes a persistent seasonal pattern in Natural Gas carry and notes that fixed-month trading can reduce seasonal effects when possible.
- PDF pages 244-246 describe examples where carry estimates for certain bond and equity futures can be systematically misleading or seasonally biased when front/second-contract approximations are used.
- PDF page 246 identifies two broad problems: noisy carry estimates and instrument-specific seasonal issues.
- Audit implication: production source locks must explicitly resolve seasonal, fixed-month, and wrong-sign policies before any real-data S10 carry implementation. The current M5 toy surface must remain synthetic-only.

### Carry Smoothing Spans

- PDF pages 246-247 say smoothing can reduce noisy carry forecasts and may help with seasonal issues.
- PDF page 247 selects four carry trading rule variations: 5, 20, 60, and 120 business days.
- PDF page 247 says intermediate spans such as 40 business days are highly correlated with adjacent variations, and longer smooths did not meaningfully reduce costs or improve performance in the source discussion.
- Audit implication: the post-S10/M5 decision to draft a future S10 carry forecast-block extension with Carry5/20/60/120 spans is source-aligned at the process level.

### Forecast Scalar And Caps

- PDF page 247 says the carry forecast is in Sharpe-ratio units and uses a forecast scalar of 30 for all four carry variations.
- PDF page 248 says forecasts are capped for previously discussed reasons, then position sizing and buffering would normally follow.
- Audit implication: a future S10 carry block must lock scalar and cap mechanics before implementation. The current M5 code correctly stops before scalar, caps, position sizing, and buffering.

### Cost Eligibility And Forecast Weights

- PDF page 248 says multiple carry rule variations should be selected for a given instrument based on whether they are cheap enough to trade.
- PDF page 248 says forecast weights determine how variation forecasts are averaged into a combined forecast.
- PDF pages 248-253 discuss using equal forecast weights across carry variations that pass the cost/turnover eligibility test.
- PDF page 253 concludes with equal forecast weights across carry variations cheap enough for the instrument.
- Audit implication: the post-S10/M5 decision correctly treats cost eligibility and equal weights as future S10 atoms, not as M5 construction output.

### Carry FDM

- PDF page 253 says the combined carry forecast needs a forecast diversification multiplier.
- PDF page 253 provides FDM values for eligible carry-span sets:
  - Carry5, Carry20, Carry60, Carry120: equal 0.25 weights, FDM 1.04.
  - Carry20, Carry60, Carry120: equal one-third weights, FDM 1.03.
  - Carry60, Carry120: equal 0.5 weights, FDM 1.02.
  - Carry120 only: weight 1.0, FDM 1.0.
- Audit implication: FDM belongs in the future S10 carry forecast-block extension, not in current M5.

### S11 Boundary

- PDF pages 269-270 move into combined trend and carry mechanics and broader forecast diversification.
- Audit implication: S11 should remain closed until S10 carry forecast construction is source-locked. The current post-S10/M5 decision to extend S10 before opening S11 is governance-safe if no S11 implementation is smuggled in.

## Known Non-Locks

This source pack does not lock:

- exact production raw-carry sign convention;
- production contract-selection rule for every asset class;
- production expiry calendars or exact day-count rules;
- production roll-day handling;
- fixed-month commodity universe;
- seasonal or wrong-sign treatment by instrument;
- cost/turnover eligibility formula;
- cap value and cap timing;
- position sizing or buffering;
- S11 trend/carry weights or style allocation.

Those require explicit future source-lock work and Opus source-faithfulness review before implementation.

## Non-Authorization

This file authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no remote operations, and no Opus execution by itself.

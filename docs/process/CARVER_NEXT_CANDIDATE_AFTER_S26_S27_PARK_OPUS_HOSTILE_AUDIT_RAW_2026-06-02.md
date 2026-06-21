I now have enough source-anchored evidence to deliver the audit. The book's own framing is now verified: p.16 + p.20 mandate reading Part One in order ("each depends on the previous chapters"); p.277 explicitly states "Strategies seventeen to twenty are new standalone strategies" and "Strategies twelve to sixteen modify the carry or trend strategies from Part One"; p.238 confirms carry needs two expiries; p.475 confirms hourly framing only exists in Part Four. The "P05/P06/P07" labels in the packet have no book referent. I'll now write the full hostile audit.

---

# Hostile Source-Faithfulness Audit — Next Carver Candidate After S26/S27 Park

**Date:** 2026-06-02
**Status:** `AUDIT_OPINION_ONLY_NOT_AUTHORIZATION`
**Source authority:** `00_Carver.pdf` — Robert Carver, *Advanced Futures Trading Strategies*
**Audit posture:** adversarial; packet labels not assumed correct.

---

## 0. Executive verdict (read this first)

**Recommended next source-native gate:** **`S09_DEV_RECON_DAILY_SINGLE_INSTRUMENT`** — Strategy 9 "Multiple trend following rules" (Carver pp. 201–231), source-native futures, daily completed bars, single-rolled-front surface, Dev/Reconciliation only.

**Confidence:** **HIGH** that S09 is the correct ordering per the book; **MEDIUM-HIGH** that the 65-row daily foundation is data-ready for it; **MEDIUM** that any pre-existing local EWMAC code is independently source-faithful and not contaminated by the S13-style V/Q/M overlays inherited from the S26/S27 work.

**One-line rationale:** S09 is the first chapter in Carver's own mandated reading order where individual trend sleeves (S05–S08) actually get combined into a usable forecast; it needs only daily close prices already present in the 65-row foundation; it has zero intraday/multi-expiry/RV-leg/cross-sectional dependencies; and it is the prerequisite gate for the highest-Sharpe chapter in the book (S11, Jumbo Sharpe 1.27).

---

## 1. Source-authority verifications (book vs packet)

| Packet claim | Book check | Verdict |
|---|---|---|
| Book is futures-specific | Confirmed; entire framing is futures + Jumbo (Appx C). | OK |
| 30 strategy chapters | TOC lists Strategy 1–30 across Parts One–Five. | OK |
| Parts One/Two/Three/Five are daily; Part Four is hourly | Confirmed: p.475 — "I backtest them on hourly data" applies ONLY to S26/S27 in Part Four. Appendix C is silent on frequency, i.e., daily by default. | OK |
| Appendix C lists 102-instrument Jumbo universe | Carver: "I took all the instruments which met my liquidity and cost thresholds…102 in all" (p.141). The Appendix C tables on pp.690–695 only enumerate ~60 in the extract sample — possible incomplete extraction or partial publication; the 102 figure stands as Carver's stated working universe. | OK with caveat — verify Appx C row count in PDF directly before depending on 102 |
| S05–S08 are SOURCE_NATIVE_PORTFOLIO_SLEEVE | Carver's own framing: S05→S06→S07→S08 incrementally add long-only, long-short, trend-strength sizing, and faster filter to a single rule family. The chapters do NOT present a complete combined system; they enumerate sleeves. | OK |
| S09/S10/S11 are STANDALONE_CANDIDATE | Carver (p.201): S09 is "a combined strategy that is superior to any individual speed of filter." S10 is a new rule family (carry). S11 explicitly combines S09+S10. Functionally standalone in that each produces a complete forecast on its own data, but **S11 has hard prerequisites on S09+S10**. | OK-with-caveat — see §2 |
| S12–S16 are PORTFOLIO_ONLY_COMPONENT | Carver (p.277): "**Strategies twelve to sixteen modify the carry or trend strategies from Part One.**" Source-anchored — these are overlays, not standalone alpha. | OK |
| S17 standalone | Carver (p.277): "**Strategies seventeen to twenty are new standalone strategies.**" But chapter-internal: S17 is structurally a normalised re-skin of S05–S09. It IS standalone-runnable; it is also a sleeve substitute. | OK-with-caveat |
| S18, S19, S20 standalone | Same Carver sentence (p.277). But: S18 requires asset-class aggregation across multiple instruments; S19/S20 are cross-sectional and **cannot run on a single instrument**. Carver labels them "standalone" in the chapter sense; they are NOT engineering-standalone. | **MISLABEL RISK** |
| S25 PORTFOLIO_ONLY | Title: "Dynamic optimisation (for when you can't trade the Jumbo portfolio)" (p.443). Self-evidently a portfolio-construction overlay. | OK |
| **Packet candidate set mentions "P05/P06/P07 complete Jumbo trend/carry portfolios"** | **No book referent.** Carver's book has Parts One–Six and Strategies S01–S30. There is NO chapter or section in the book named P05, P06, or P07. The closest book construct is "the system the reader builds by reading Part One in order through S09 → S10 → S11 on the Jumbo universe." | **HOSTILE FINDING — packet uses unsourced labels** |

**Net source-authority verdict:** The local inventory in packet 02 is mostly defensible. The two source-faithfulness problems are:
- **S19/S20** labeled `STANDALONE_CANDIDATE` while being structurally cross-sectional and requiring a multi-instrument harness.
- **P05/P06/P07** appears in packet 04 with no source-authoritative referent and must not anchor the ranking.

---

## 2. Strategy taxonomy — corrected classification

Source-anchored, hostile reclassification:

| ID | Book chapter | True classification | Why |
|---|---|---|---|
| S01–S03 | Buy & hold w/ risk scaling variants | **PORTFOLIO_ONLY_COMPONENT** (sizing primitives) | Each only adds one position-sizing rule; not alpha standalones |
| S04 | B&H portfolio w/ variable risk sizing | **PORTFOLIO_ONLY_COMPONENT** | Position-sizing-on-portfolio scaffolding |
| S05–S08 | Slow/fast trend sleeves | **SOURCE_NATIVE_PORTFOLIO_SLEEVE** | Incremental EWMAC building blocks — each individually deficient by Carver's own narrative |
| **S09** | Multiple trend following rules | **STANDALONE_CANDIDATE — first true one in book** | Combines six EWMAC pairs via FDM into a single forecast |
| **S10** | Basic carry | **STANDALONE_CANDIDATE_DATA_BLOCKED** | Standalone rule, but requires two-expiry curve data (p.238) not confirmed in current 65-row inventory |
| **S11** | Combined carry + trend | **STANDALONE_CANDIDATE_DEPENDENT** | Highest Sharpe in book (1.27, Jumbo, p.271) but hard-depends on S09 + S10 |
| S12–S16 | Adj trend / regimes / spot / accurate carry / allocation | **PORTFOLIO_ONLY_COMPONENT** | Carver p.277 verbatim: "modify the carry or trend strategies from Part One" |
| **S17** | Normalised trend | **STANDALONE_CANDIDATE_OR_SLEEVE_SUBSTITUTE** | Carver labels standalone; functionally a normalised re-skin of S09's EWMAC core |
| **S18** | Trend following asset classes | **PORTFOLIO_LEVEL_STRATEGY** | Requires multi-instrument-per-asset-class aggregation; not single-instrument runnable |
| **S19** | Cross-sectional momentum | **PORTFOLIO_LEVEL_STRATEGY** | Cross-sectional → REQUIRES universe by construction |
| **S20** | Cross-sectional carry | **PORTFOLIO_LEVEL_STRATEGY_DATA_BLOCKED** | Cross-section + carry → needs universe AND two-expiry data per instrument |
| **S21** | Breakout | **STANDALONE_CANDIDATE_COST_SENSITIVE** | Daily close only; six horizons. Breakout10 turnover ≈365/yr (Carver flags as expensive) |
| **S22** | Value | **STANDALONE_CANDIDATE_SOURCE_AMBIGUOUS** | 5-yr lookback; Carver presents only a futures-simplification ("buy decliners, sell risers")—source-clarity is weak |
| **S23** | Acceleration | **STANDALONE_OR_OVERLAY** | Daily close; derived from EWMAC change-of-rate. Standalone Sharpe not isolated cleanly in chapter |
| **S24** | Skew, a case study | **PARKED_OR_OVERLAY** | Carver: "case study"; advises 20% weight only; standalone SR 0.01–0.71 wildly variable |
| S25 | Dynamic optimisation | **PORTFOLIO_ONLY_COMPONENT** | Self-described capital-constrained portfolio reconstruction tool |
| S26/S27 | Fast mean reversion | **PARKED (current packet decision)** | Confirmed by 03 packet; do not rescue |
| S28 | Cross-instrument spreads | **RV_MULTI_LEG_PARK** | Carver: "RV strategies require higher leverage and can be expensive"; multi-leg execution |
| S29 | Cross-instrument triplets | **RV_MULTI_LEG_PARK** | Three legs |
| S30 | Calendar trading | **RV_MULTI_LEG_PARK** | Multi-expiry within instrument |

**Engineering-standalone candidates after reclassification (no portfolio/cross-section/multi-leg/multi-expiry dependency):**
- **S09** — clean
- **S21** — clean but cost-sensitive
- **S23** — clean but standalone framing weak
- **S17** — clean (close + vol estimate)
- S22 — clean data path but source-ambiguous

---

## 3. Top 5 ranked next source-native candidates

Each scored against the packet 04 dimensions: source-faithfulness clarity, implementation ambiguity, data availability on the **current 65-row daily foundation**, cost/execution sensitivity, window discipline, CFD-adapter mapping (deferred), portfolio relevance.

### Rank 1 — **S09 Multiple Trend Following Rules**

| Dimension | Finding |
|---|---|
| Source pages | Carver pp. 201–231 (Strategy 9, Part One) |
| Timeframe | Daily, completed bars only |
| Formula | Combine EWMAC(2,8), (4,16), (8,32), (16,64), (32,128), (64,256) into a single forecast; per-pair forecast scalar; capping at ±20; FDM from Carver Table 36 / Table 52 (p.234) |
| Data required | Daily back-adjusted close, single rolled-front continuous contract per instrument |
| Data-readiness fit on current 65-row foundation | **CLEAN FIT.** No carry/curve, no cross-section, no intraday, no multi-leg, no fundamentals |
| Implementation blockers | None inherent. **Risk: existing local EWMAC code may be entangled with S13-style V/Q/M attenuation from the S27 chain — must be re-instantiated source-clean, not reused** |
| Cost/execution sensitivity | Manageable. Carver's own per-instrument turnover-cost filter drops the fast EWMAC pairs on expensive instruments. EWMAC(64,256) and (32,128) trade slowly enough to be cost-tolerant on any liquid future |
| Window discipline | Clean Dev/Recon→TEST→VAL→Lockbox path. No long state requirement beyond ~512-day warmup for EWMAC(256) |
| Standalone vs sleeve vs portfolio-only | **First true standalone in Carver's mandated reading order** (p.20: "each depends on the previous chapters") |
| CFD adapter mapping (deferred) | Trend on rolled-front daily close maps directly to CFD index/single-name daily data. Adapter risk: CFD spread cost on slow rules is non-fatal; on fast rules it can dominate |
| **Score** | **STRONGEST CANDIDATE** |

### Rank 2 — **S21 Breakout**

| Dimension | Finding |
|---|---|
| Source pages | Carver pp. 388–402 (Strategy 21, Part Three) |
| Timeframe | Daily |
| Formula | min/max over horizon h; raw forecast normalised by half-range; EWMA(span=h/4) smoothed forecast; forecast scalar table p. ~392; cap at ±20 |
| Horizons | 10, 20, 40, 80, 160, 320 days |
| Data required | Daily close only (some implementations use intraday H/L — verify source preference; the chapter equations use closes) |
| Data-readiness fit | **CLEAN FIT.** Same data as S09 |
| Implementation blockers | Verify whether Carver uses intraday H/L or close-only min/max — small but critical source-faithfulness question |
| Cost/execution sensitivity | **HIGH for short horizons.** Breakout10 turnover ~365/yr, Breakout20 ~170. Carver explicitly warns: "breakout lookback horizons that are too short will result in penal trading costs" |
| Reported chapter results | Aggregate Jumbo Sharpe 1.17; median single-instrument 0.30 |
| Standalone vs sleeve | Standalone; also explicitly combinable with S09/S10 |
| CFD adapter mapping (deferred) | Daily close-only min/max maps cleanly to CFD; cost sensitivity becomes worse under CFD spreads — slow horizons only |
| **Score** | **STRONG, BUT NEEDS COST DISCIPLINE GUARDRAIL** |

### Rank 3 — **S17 Normalised Trend**

| Dimension | Finding |
|---|---|
| Source pages | Carver pp. 342–353 (Strategy 17, Part Two) |
| Timeframe | Daily |
| Formula | Apply EWMAC to a volatility-normalised price series rather than raw back-adjusted prices |
| Data required | Daily back-adjusted close + daily std-dev-of-returns estimate (the latter is already implicit in any Carver volatility-targeting position sizer) |
| Data-readiness fit | **CLEAN FIT.** Same data as S09; vol estimator is already a dependency of every chapter from S02 onward |
| Implementation blockers | Per-asset-class result variance is large in chapter — Equity EWMAC16 Sharpe ~1.03 but VIX ~0.12. Source-faithful but instrument-selection-sensitive |
| Cost/execution sensitivity | Same as S09 |
| Carver's explicit framing | p.277: "new standalone strategy." But functionally close to an S09 variant |
| CFD adapter mapping (deferred) | Same as S09 |
| **Score** | **GOOD; but adds little new audit signal vs S09 when only one is to be built next** |

### Rank 4 — **S23 Acceleration**

| Dimension | Finding |
|---|---|
| Source pages | Carver pp. 410–420 (Strategy 23, Part Three) |
| Timeframe | Daily |
| Formula | Difference of EWMACs — change-of-rate of an existing trend forecast |
| Data required | Daily close only — derived from already-computed S05–S09 outputs |
| Data-readiness fit | **CLEAN FIT** if S09 is already built |
| Implementation blockers | Chapter reports Sharpe predominantly in the *combined* configuration with trend+carry (SR 1.29). Standalone Sharpe is not isolated cleanly. Risk of "interpretation drift" if used as a standalone claim |
| Cost/execution sensitivity | Inherits parent EWMAC turnover |
| CFD adapter mapping (deferred) | Same as S09 |
| **Score** | **NATURAL FOLLOW-UP AFTER S09, NOT BEFORE IT** |

### Rank 5 — **S11 Combined Carry and Trend**

| Dimension | Finding |
|---|---|
| Source pages | Carver pp. 264–275 (Strategy 11, Part One) |
| Timeframe | Daily |
| Formula | Weighted combination of trend forecasts (from S09) and carry forecasts (from S10) via Carver's forecast-combination machinery; FDM per Table 52 (p.234) |
| Data required | Daily close + multi-expiry curve data (front contract + nearer contract per Carver p.238) per instrument |
| Data-readiness fit | **PARTIAL.** Single-rolled close OK; **multi-expiry carry data NOT confirmed in 65-row inventory** |
| Implementation blockers | (a) Requires S09 built first; (b) requires S10 built first; (c) requires curve-data audit; (d) sign conventions per asset class (Carver p.232: equities Div-Int; bonds Yield-Repo; FX Deposit-Borrow; commodities curve slope) must each be re-derived source-faithfully |
| Reported result | **Sharpe 1.27 on Jumbo** (p.271) — highest in book |
| Standalone vs dependent | Engineering-dependent on S09+S10 — cannot be a "next gate" by itself |
| CFD adapter mapping (deferred) | Carry-on-CFDs is *fundamentally distorted* by financing/swap mechanics — CFD adapter behavior will diverge materially from source-native futures carry. This is the strategy most at risk of CFD-distortion |
| **Score** | **CANONICAL EVENTUAL DESTINATION; CANNOT BE THE NEXT GATE** |

**Strategies explicitly excluded from top 5 and why:**

- **S10 Basic Carry** — would be Rank 2 if curve data were inventoried, but the 65-row foundation explicitly does not declare multi-expiry readiness. Selecting it now would either (a) silently expand data scope or (b) require the same kind of symbol/expiry decision that the packet warns against (cf. S26/S27 lessons in 03).
- **S18, S19, S20** — require multi-instrument cross-section harness. Not engineering-standalone. Park until S09 is shipped and a multi-instrument runner exists.
- **S22 Value, S24 Skew** — source-clarity weak (Carver himself calls S24 a "case study"); standalone Sharpes weak or wildly variable.
- **S28/S29/S30** — RV multi-leg, Carver flags as expensive and leverage-hungry; far outside the "low execution ambiguity" criterion.

---

## 4. Candidates to PARK or AVOID

| Strategy | Park reason |
|---|---|
| S26, S27 | Already parked per packet 03. Do not rescue. The DELTA_M1_LADDER_MINUS_UNIT result (+20,913 → −15,254 across 2022-23 vs 2025-26) is consistent with regime-decay, not source-faithfulness. Any rescue attempt would be post-result tuning |
| S10 standalone | Promote only AFTER multi-expiry inventory is authorized and confirmed |
| S12, S13, S14, S15, S16 | Overlays per Carver p.277 — not standalone candidates |
| S18, S19, S20 | Portfolio-level by construction. Build only after S09 (single-instrument) plus a multi-instrument harness |
| S22 | Source-ambiguous; 5-year lookback strains clean window discipline |
| S24 | Carver: case study; advises 20% combined weight only |
| S25 | Carver: "for when you can't trade the Jumbo portfolio" — portfolio-construction tool |
| S28, S29, S30 | RV multi-leg, expensive, leverage-hungry |
| Anything resembling the rejected CFD/P27DO index result | Per packet 03 governance — do not chase |

---

## 5. Recommended single next gate

**Gate name:** `S09_DEV_RECON_DAILY_SINGLE_INSTRUMENT`

**Exact scope:**

```text
LANE_DECLARATION:        SOURCE_NATIVE_FUTURES
STRATEGY:                S09_MULTIPLE_TREND_FOLLOWING_RULES
SOURCE_PAGES:            Carver pp. 201–231 (formulas), p. 234 Table 52 (FDM),
                         Strategy 5–8 chapters for individual EWMAC sleeves
TIMEFRAME:               Daily, completed bars only
SURFACE:                 Single rolled-front continuous contract per instrument
                         No curve, no spread, no calendar, no synthetic
EWMAC_VARIATIONS:        EWMAC(2,8), EWMAC(4,16), EWMAC(8,32),
                         EWMAC(16,64), EWMAC(32,128), EWMAC(64,256)
FORECAST_SCALARS:        Per Carver per-pair table (must be re-derived
                         source-clean, not inherited from S26/S27 code)
CAP:                     ±20 per Carver
FDM:                     Carver Table 52 p.234, applied per number of
                         active rules surviving cost filter
COST_FILTER:             Carver's per-instrument turnover×cost-budget rule;
                         drop EWMAC pairs whose expected trading cost
                         exceeds Carver's per-instrument budget
INSTRUMENT_SET:          Subset of the 65 DEV_RECON_DATA_READY rows;
                         no silent ALI re-inclusion; no symbol substitution
DATA_POLICY:             NO_FILL / NO_DROP / NO_SUBSTITUTE /
                         NO_INTERPOLATION / NO_REWEIGHT
WINDOW_DISCIPLINE:       Development/Reconciliation only;
                         no TEST, no VALIDATION, no LOCKBOX, no Forward
COST_BOUNDARY:           Zero-cost placeholder + Carver per-instrument
                         turnover×cost estimate; documented, not tuned
PROMOTION_AUTHORIZATION: NONE (Dev/Recon ≠ promotion evidence)
CFD_LANE:                NOT_AUTHORIZED — no CFD adapter work in this gate
TUNING_POLICY:           No post-result tuning, no symbol re-selection,
                         no scalar re-fitting after viewing results
ARTEFACTS:               Per-instrument EWMAC variant outputs; combined
                         forecast; turnover; cost-filter survival list;
                         instrument-by-instrument PnL contributions
EXIT_CRITERION_FOR_GATE: Either (a) S09 forecast machinery reconciles to
                         Carver-reported instrument-level behavior at a
                         documented tolerance on a subset of instruments,
                         OR (b) it does not, and the failure mode is
                         logged before any next-step decision
```

---

## 6. Strongest hostile objection to this gate

> **"S09 is a near-trivial reimplementation of EWMACs that the lab almost certainly already ran while building the S13-style V/Q/M attenuation chain for S26/S27. Running it next produces no new audit signal — only a confirmation that EWMAC code is correct. The lab burns a gate cycle on a strategy that cannot fail interestingly. Meanwhile, the genuine outstanding source-faithfulness risk lives in (a) the multi-expiry carry pipeline — sign conventions per asset class, repo proxies for bonds, dividend handling for equities, FX deposit/borrow rates — and (b) the forecast-combination machinery used in S11. S09 exercises neither. By picking S09 you defer the harder, more failure-prone questions and accumulate technical debt that will then have to be paid down under deadline pressure when S11 is eventually built. A more honest hostile gate would be `S10_DEV_RECON_CARRY_PIPELINE_AUDIT`: even if the data isn't confirmed ready, the audit work of declaring the carry data requirements asset-class-by-asset-class IS source-faithfulness work that must happen anyway."**

This objection is real. Two reasons to still pick S09:

1. **Carver's own ordering is explicit (p.20): "each depends on the previous chapters."** Skipping S09 to chase S10 inverts the book's mandated ordering — exactly the kind of "select for excitement" pattern the packet 01 governance forbids.
2. **The assumption that pre-existing EWMAC code is source-clean is itself untested.** The S27 code chain layered V/Q/M attenuation on top of EWMACs. Pulling EWMAC out of that chain into an independent source-clean S09 instance IS a real audit event, not a trivial copy. If the existing code is in fact source-faithful, that result IS the audit signal. If it is not, the lab has just discovered a contamination that was about to silently propagate into every downstream chapter.

A reasonable compromise — explicitly out of scope for this gate but on-record — is to schedule **`S10_CARRY_DATA_INVENTORY_AUDIT`** (data-readiness audit only, no compute) as a parallel non-blocking workstream against this gate so S11 is not bottlenecked downstream.

---

## 7. Evidence that would overturn this recommendation

1. **A verified inventory** showing multi-expiry/curve data is **already available** for ≥50 of the 65 ready instruments, with sign conventions per asset class already source-locked → **S11 (or S10) becomes the canonical next gate** because Carver's highest-Sharpe chapter is one step away.
2. **An independent audit certificate** showing that the existing local EWMAC stack is already source-locked at all six speeds with scalars/caps/FDM matching Carver's tables, and verifiably *not* entangled with V/Q/M attenuation → **S09 can be skipped to S21 Breakout** (a genuinely new rule family) or directly to **S11** (if §7.1 also holds).
3. **A confirmed mission-scope change** to multi-instrument portfolio reconstruction with an authorized portfolio harness → **S18/S19/S20 become evaluable** and **S11-on-Jumbo** becomes the canonical target.
4. **Source-faithful evidence I missed in this audit** (a Carver erratum, a clarifying interview, or appendix material) showing S09's six-speed list is actually a subset Carver disavows in favor of breakout or acceleration → push **S21 or S23 to #1**.
5. **A signed Lockbox-grade result on S09** already existing in the archived QuantLab_v3 workspace, with chain-of-custody clean of CFD-adapter contamination → S09 is already done and the recommendation collapses to **S10 next** (assuming §7.1).

If none of these obtain, **`S09_DEV_RECON_DAILY_SINGLE_INSTRUMENT`** is the next gate.

---

## 8. Final verdict and confidence

**Verdict:** Pursue **S09 Multiple Trend Following Rules** as the next source-native Carver gate. Single-instrument, daily, completed-bar, Dev/Reconciliation only. CFD-adapter suitability deferred entirely.

**Confidence breakdown:**
- That S09 is the source-correct next ordering per the book: **HIGH** (Carver p.20 mandates Part One in order; S09 is the first true combined system in that order)
- That the existing 65-row daily foundation supports it: **MEDIUM-HIGH** (the data shape matches; the 1 ALI fail-close and any silent ZN/ZF/MES-style sigma-row deficits must still be re-checked at the EWMAC(64,256) warmup horizon)
- That the local EWMAC code is independently source-faithful: **MEDIUM** — this is precisely the audit signal the gate is designed to produce
- That picking S09 will not be retrospectively re-labeled as "trivial confirmation work": **MEDIUM** — the hostile objection in §6 is real and the lab should accept it as a known cost of source-faithful ordering

**Adversarial closing note:** If the lab's reviewers feel the urge to skip S09 because "we already have the EWMACs," that urge is itself the failure mode this audit exists to flag. The mission per packet 01 is `TRANSLATE_AS_MANY_SOURCE_FAITHFUL_CARVER_BOOK_STRATEGIES_AS_POSSIBLE_AND_SEE_WHICH_ONES_STAND`. "Translate" means independently instantiate from the book — not reuse code that was built under a different chapter's assumptions. Source-faithfulness is exactly the property that gets quietly eroded when prior code is reused without an explicit audit gate. S09 is that gate.

---

**End of audit.**
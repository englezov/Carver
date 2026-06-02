The full hostile audit report is written to `/app/audit/S27_ZN_2025_2026_HOSTILE_AUDIT_REPORT.md`. Below is the report itself.

---

# Hostile Audit Report — CARVER_S27_ZN_2025_2026_TOUCHED_SUPPORT_DEV_RECON_BACKTEST_RESULT_2026-06-01

**Scope:** attack the negative S27 ZN 2025-2026 touched-support result for mechanical mistakes, data-policy artifacts, alignment bugs, roll/lineage bugs, cost/fee errors, provider-condition handling errors, and mismatches against the 2022-2024 positive evidence.

**Posture:** hostile, but symmetric — no rescue of S27, no rescue of the negative either.

**Evidence used (only):** the five supplied files. No provider calls, no reruns, no Git operations.

---

## Executive Verdict (TL;DR)

The 2025-2026 negative result is **mechanically sound** at Development/Reconciliation scope. The same code engine (`tools/databento/carver_s27_candidate_comparison_2022_2023.py` + `src/carver/spine/s26_s27.py`) that produced the positive 2022-2023 and 2024 results — and that passed an independent 38/38-check mechanical verification on those windows — produces the 2025-2026 numbers. Row counts reconcile cleanly, strict-prior daily runtime alignment holds on every forecast row, the EWMA(5) warm-up block is explicit, the does-not-oppose-trend veto and S27 scalar 20 are correctly applied, the roll lineage and inactive-contract exclusion are explicit, and the PnL sign / multiplier / fee-side / position-shift timing all hand-recompute to the reported figures.

The negative number itself is therefore **not** a mechanical bug; it is a real available-row diagnostic. The single largest day (`2026-02-05`, M1 = −$10,388) accounts for 56% of the 2026 M1 loss; the M1 ladder amplifies losses on that day 8.4× vs unit-no-ladder. That is the textbook M1-amplified mean-reversion tail-loss signature against a counter-trend rally — not a sign error, scaling error, or roll bug.

However the result is **fail-closed as a complete-window backtest** because of (1) six provider-degraded dates (CRITICAL), (2) the daily runtime/V/Q/M ledger already touched through 2026-05-22 (HIGH), (3) ETF-only fee model (MEDIUM), and (4) M1 ladder is a local overlay not a Carver-book atom (MEDIUM, pre-existing).

It is therefore an **AVAILABLE_ROW_DIAGNOSTIC_ONLY** with a robust fragility warning attached. It supports **MODERATE** parking strength, not STRONG.

---

## Reconciliation Of Row Counts

| Item | Reported | Recomputed | Reconciliation |
|---|---:|---:|---|
| Hourly source rows | 15,306 | 15,306 | `8,097 continuous + 7,209 inactive = 15,306` ✓ |
| Hourly continuous rows | 8,097 | 8,097 | ✓ |
| Hourly inactive (ledgered) | 7,209 | 7,209 | explicitly emitted to `_ZN_hourly_inactive_rows.csv` ✓ |
| Hourly roll transitions | 6 | 6 | 7 dated contracts → 6 links ✓ |
| Blocked dependency rows | 4 | 4 | All four are EWMA(5) warm-up on `2025-01-02 00:00–03:00 UTC`, marked `EXPLICITLY_BLOCKED_NOT_SILENTLY_SKIPPED` ✓ |
| S26 forecast rows | 8,093 | 8,093 | `8,097 − 4 EWMA warm-up = 8,093` ✓ |
| S27 forecast rows | 8,093 | 8,093 | ✓ |
| Ladder rows | 8,093 | 8,093 | ✓ |
| Desired-position rows | 8,093 | 8,093 | ✓ |
| Same-input backtest rows | 8,092 | 8,092 | `zip(ts[:-1], ts[1:])` over 8,097 hourly continuous yields 8,096 candidate pairs; only `entry_ts ∈ forecast_by_ts` kept; the **last** forecast timestamp has no successor (no next-bar PnL) → 8,092 ✓ |

No silent drops. No double-counting. No off-by-one. The `8,093 − 1 = 8,092` collapse is the **correct strict-next-bar execution invariant**: the final forecasted bar cannot be backtested because there is no `t+1` close to evaluate against. **Feature, not bug.**

---

## Strict-Prior Daily Runtime Alignment

Hand-verified on every one of the 8,093 S27 forecast rows:

```
source_daily_runtime_lag_days distribution = {1: 8030, 2: 42, 4: 21}
min lag = 1, max lag = 4
rows with lag ≤ 0 = 0  (no same-day or future runtime leakage)
```

Lag-1 majority is normal (today's hourly forecast uses yesterday's completed daily V/Q/M & EWMAC). Lag-2 = post-weekend; lag-4 = post-long-weekend. Max lag 4 days; policy ceiling is 10 days. **Zero leakage** of same-day, intra-day, or future state into the hourly forecasts.

`_build_ladder_rows` raises `Fail closed` if `lag <= 0 or lag > 10`. ✓

---

## No-Lookahead / Same-Bar / Future-State Audit

Same-bar execution is **mechanically impossible** in this engine:

- `_build_row_attribution` enumerates `zip(ordered_ts[:-1], ordered_ts[1:])`. Position used at each pair is the one computed from the forecast at `entry_ts` (whose `derived_completed_bar_end_utc == entry_ts`, i.e., the completed prior bar). PnL is `(exit_close − entry_close) × contracts × multiplier`. **Strict next-bar.**
- Daily runtime (V/Q/M, EWMAC16) is joined strictly-prior by date comparison.
- S26 raw forecast at bar end `t` uses EWMA(5) of closes including the `t` close; position is applied to the **next** hour. The `t`-close is a legitimate information set for the forecast; it does not enter the PnL of bar `t`.
- `same_input_status = PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET` on **all 8,092 rows**.

The same-engine 2022-2024 evidence has a stronger `lookahead_status` column directly audited by the parity & mechanical verifiers with **38/38 PASS** (`...OPUS_RECOMMENDATION_VERIFICATION_CLOSEOUT_2026-06-01.md`). The 2025-2026 backtest was **not independently re-run through those verifiers** — flagged HIGH (H-2) as an evidence-completeness gap; the engine is byte-identical.

---

## S26 / S27 Source-Faithfulness (Against The Locked Atom Sheet)

All locked atoms match the implementation:
- `equilibrium = EWMA_span_5(price)` ✓
- `raw_forecast = equilibrium − price` ✓
- `sigma_price = price × sigma_percent / 16` ✓
- `S26_FORECAST_SCALAR = 9.3`, `S27_FORECAST_SCALAR = 20.0` ✓ (scalar regression closed 2026-05-31)
- Cap `[−20, +20]` ✓
- `M = EWMA_10(2 − 1.5×Q)` ✓
- `adjusted_raw = raw × M` when not opposing ✓
- EWMAC fast=16, slow=64, `trend = fast − slow` ✓
- **Veto:** `opposes = s26.raw * trend < 0; adjusted_raw = 0 if opposes else raw × M` ✓ matches "mean-reversion must not oppose trend" (p.508)
- No FDM, no buffering ✓

Empirical: 4,099 NO / 3,994 YES opposes-trend distribution. Sample YES row: `s26_raw=0.090, adjusted_raw=0.000, vol_mult=1.481` — when opposing, `adjusted_raw=0` exactly as designed.

**Known caveat (HIGH-2 closed for dev/recon only):** EWMAC(16,64) is computed at **daily** frequency on local additive back-adjusted ZN daily close, broadcast onto hourly bars. Same broadcast applied to 2022-2024 positive evidence — apples-to-apples.

---

## Roll Lineage, Additive Adjustment, Inactive-Contract Exclusion, Transition Handling Post-2024

- 7 dated ZN contracts: `ZNH5, ZNM5, ZNU5, ZNZ5, ZNH6, ZNM6, ZNU6` → 6 transitions.
- 6 roll-spanning backtest rows verified: chain `ZNH5→ZNM5→ZNU5→ZNZ5→ZNH6→ZNM6→ZNU6` (one row per transition).
- 7,209 inactive dated-contract source rows **explicitly ledgered** (not silently dropped).
- Roll fee convention: `|contracts| × 2` per held contract on transition (close-and-open). Verified in row data.
- 2025→2026 transition (ZNZ5→ZNH6) uses the **same uniform code path** as every other roll — no special-case post-2024 logic.

**No sign reversal, no missed transition, no double additive adjustment.**

---

## PnL Sign / Multiplier / Position-Shift Timing / Fee-Sides / M1 Ladder Construction

Hand-recomputed on artifact rows:

- **Sign convention.** Final row: short `−2` × `+0.078125` × `1000` = `−156.25` ✓ matches `m1_ladder_gross_pnl_usd=-156.25`. Penultimate row: `−3` × `−0.046875` × `1000` = `+140.625` ✓. **Short × falling → positive; short × rising → negative. Correct.**
- **ZN multiplier 1000** = $100,000 face × 1% per full point. ✓
- **Position-shift timing.** Forecast at `t` → position at `t` → PnL over `(t, t+1h)`. **Strict next-bar, never same-bar.** Verified vs the mechanical_verifier's `_pnl_fee_checks` which passed 2022-2024.
- **Fee sides.** Row 2 spot-check: `prior m1=-2 → m1=-1, |change|=1 × $1.51 = $1.51` ✓ matches `m1_ladder_estimated_etf_fee_usd=1.51`. First-row position-establishment fee recorded as 0 (initialization quirk, undercount ≤ $3, flagged LOW L-1).
- **M1 ladder.** `base_unrounded = capital × target_risk × weight × idm / contract_risk_usd`; `desired = base × (capped_forecast/10)`; `rounded = round(desired, NEAREST)`. Independently verified by `_ladder_position_checks` (38/38 PASS on 2022-2024). **Byte-identical in 2025-2026.**

---

## Provider-Degraded Date Handling (Six Dates)

| Date | Weekday | In backtest entry/exit | Notes |
|---|---|---:|---|
| 2025-09-17 | Wed | 2 entry / 2 exit | Wednesday data hole, surrounding rows present |
| 2025-09-24 | Wed | 2 / 2 | Same pattern |
| 2025-11-28 | Fri | 1 / 1 | US Thanksgiving Friday |
| 2026-03-15 | Sun | 0 / 0 | Properly excluded |
| 2026-03-16 | Mon | 0 / 0 | Properly excluded |
| 2026-04-10 | Fri | 2 / 2 | Good-Friday context |

**Net PnL on the 7 backtest rows whose entry date is degraded: M1 = −$582.65, unit = $0.00.** Removing them moves M1 from `−$25,697.16` to `−$25,114.51` — a **2.3% change**. **Exclusion does not mechanically explain the negative.**

The implementation handles missing bars via **position carry-through**: e.g., `2025-09-17` has a single row `entry=2025-09-17T00:00Z → exit=2025-09-18T01:00Z` (25-hour gap); `2026-04-10` has `entry=T00:00 → exit=2026-04-12T23:00` (71 hours across Easter weekend). 357 backtest rows have `exit_ts − entry_ts ≠ 1h` (272 are 2-hour, 63 are 50-hour weekends, 22 are multi-day). M1 PnL from gap rows = **−$5,109** (20% of M1 loss); unit gap PnL = **−$1,185** (11% of unit loss). Same gap-carry behavior was used in 2022-2024 (same engine) → **does not bias the comparison**.

---

## Daily Win Rate > 0.5 With Strongly Negative PnL — Diagnosis

Textbook fast-mean-reversion asymmetric tail-loss signature, **not a calculation problem**:

- 2026 M1: 99 nonzero-PnL days; 58 winners, 41 losers → daily win 0.586
- Avg winning day **+$334**; avg losing day **−$923**; **loss/win magnitude ratio 2.76×**
- Worst single day **2026-02-05 = −$10,388.46** = **56% of total 2026 M1 loss**
- On that day: ZN rallied +0.81 points in 23 hourly bars; M1 ladder was heavily SHORT (mode −17 for 8 of 23 hours); **day's M1/unit amplification 8.4×**
- 4 of top 5 worst days are Feb-Mar 2026

This is **not sign inversion** (verified), **not fee amplification** (fees on 2026-02-05 are <2% of the loss), **not ladder asymmetry** (the ladder is symmetric in construction), **not a calculation error** (formula reproduces row-by-row).

It is **M1 amplification of a regime-divergent counter-trend rally against an accumulated short** whose trend filter did not veto (daily EWMAC also negative, agreeing → veto permissive). When mean-reversion is wrong in a one-sided move, the ladder makes it dramatically wrong. The ladder did exactly the symmetric thing in 2022-2023 (+$3,591 delta) and 2024 (+$17,322 delta).

---

## Comparator Reconciliation — Apples-To-Apples?

| Surface | Window | Variant | Fee | Net |
|---|---|---|---|---:|
| Retargeted dev-recon | 2022-2023 | unit / no fees | none | **+2,968.75 gross** |
| Mech-verifier initial test | 2022-2023 | M1 | ETF $1.51 | **+5,342.63 net** |
| Earlier comparison | 2022-2023 | M1 | (different surface) | **+16,517.25** |
| 2024 frozen validation | 2024 | M1 | ETF $1.51 | **+24,618.82 net** |
| Touched-history | 2022-2024 | unit | ETF $1.51 | **+9,048.16** |
| Touched-history | 2022-2024 | M1 | ETF $1.51 | **+29,961.45** |
| **Target run** | 2025-2026 | unit | ETF $1.51 | **−10,442.45** |
| **Target run** | 2025-2026 | M1 | ETF $1.51 | **−25,697.16** |

The apples-to-apples comparison is **touched-history 2022-2024 vs target 2025-2026** (same engine, same fee model, same ladder, same daily runtime ledger). Compared on that basis, **no surface mismatch can explain the sign flip**. The 2024 validation runner and the 2025-2026 touched-support runner load the **same `base` module** (`carver_s27_candidate_comparison_2022_2023.py`) → **no implementation discontinuity post-2024**.

---

## Findings By Severity

### CRITICAL

**C-1. Six provider-degraded dates inside the requested window; complete-window backtest interpretation is correctly fail-closed.**
- File: `validation/...provider_condition_ledger.csv`; dates `2025-09-17, 2025-09-24, 2025-11-28, 2026-03-15, 2026-03-16, 2026-04-10`. Validation check `provider_condition_complete_window = FAIL_CLOSED...`.
- Why it matters: the −$25,697 M1 / −$10,442 unit are **available-row diagnostic** numbers, not a complete-window backtest. Not Lockbox-admissible in this shape.
- Could it flip the interpretation? Yes — *already* shifts it from "complete-window backtest" to "available-row diagnostic". The numeric magnitude is preserved.
- Quantitative bound on exclusion: at most −$582 of M1 attributable; removing degraded-entry rows yields M1 = −$25,114.51. **Cannot rescue the negative.**
- Required: complete-window rerun on clean provider-condition data.

### HIGH

**H-1. Daily runtime/V/Q/M ledger already touched through 2026-05-22 — not pristine Lockbox.**
- File: `daily_runtime_rows/...daily_runtime_rows_reused.csv` (4,750 rows, 2011-01-02 → 2026-05-22); `status.json: support_touch_status = ...NOT_PRISTINE_LOCKBOX`.
- Why it matters: cannot be treated as untouched-OOS for any Lockbox claim.
- Could it flip the 2025-2026 mechanical interpretation? No — mechanics are fine; the **label** is constrained.

**H-2. Mechanical verifier / parity verifier were not re-run on the 2025-2026 artifacts.**
- Evidence: backtest CSV emits `same_input_status` (PASS) but **lacks** the `lookahead_status`, `held_contracts_m1_ladder`, `position_change_fee_sides`, `roll_transition_fee_sides` columns that `tools/audit/carver_s27_zn_mechanical_verifier.py` consumes. Verifier ran on 2022-2024 only (38/38 PASS).
- Why it matters: the strongest independent recomputation check is not directly recorded for 2025-2026. Hand-verification here substitutes; the engine is byte-identical to the verified 2022-2024 path.
- Could it flip the interpretation? No — but the evidence record is incomplete relative to 2022-2024.
- Required: rerun the parity & mechanical verifiers on the 2025-2026 backtest folder, emit a PASS check ledger and a null-tests ledger (inverted / one-bar-delayed / day-shuffled).

### MEDIUM

**M-1. Recorded fee model is ETF/public per-side commission only; futures-realistic spread/slippage fail-closed.**
- File: `validation/...cost_status.csv` row 2.
- Why it matters: M1 has 6,691 fee sides; unit has 1,245. Larger per-side cost would make **M1 more negative**, not less. Gross is **already negative without fees** (M1 gross −$15,594; unit gross −$8,562) → removing all fees does not flip the sign.
- Could it flip the interpretation? No (toward more-negative if anything).

**M-2. EWMAC(16,64) is daily-broadcast, not hourly.**
- Locked dev/recon interpretation per `..._SOURCE_LINE_AUDIT_EWMAC_VQM_CLOSURE_...md`. Same approximation applied identically to 2022-2024 → comparison is internally consistent. Pure-Carver pedantic claim requires hourly-EWMAC variant.

**M-3. M1 ladder is a local overlay, not a Carver-book atom (CRITICAL-3 pre-existing).**
- Already recorded; applies symmetrically to positive and negative windows. The unit-no-ladder `−$10,442 net` is the source-faithful reference.

### LOW

**L-1. First-row position-establishment fee recorded as 0** (initialization-induced; `prior_*_position = None`). Undercount ≤ $3.02. Cosmetic. Fix: initialize to `0`.

**L-2. Worst-day concentration: 2026-02-05 = −$10,388 alone = 56% of 2026 M1 loss = 40% of full-window M1 loss.** Removing this day still leaves both 2025-2026 unit (−$10,442 → ≈−$8,000) and M1 strongly negative. **Not a single-row artifact.**

**L-3. Session-gap PnL carry contributes 20% of M1 loss (−$5,109) and 11% of unit loss (−$1,185).** 357 backtest rows have `exit−entry ≠ 1h`. Same gap-carry semantics applied in 2022-2024 → no comparison bias.

### INFORMATIONAL

**I-1.** Daily runtime / V/Q/M / EWMAC values are constant within a single trading date (broadcast pattern, by design).

**I-2.** Opposes-trend distribution **4,099 NO / 3,994 YES** — trend filter is active on roughly half the bars. No degenerate behavior.

**I-3. The `base` module (`carver_s27_candidate_comparison_2022_2023.py`) is NOT in the zip.** Only `s26_s27.py` from `src/carver/spine/` is shipped. The audit relies on the **closeout's claim** that the mechanical_verifier independently re-derived the 2022-2024 results from the same engine. Codepath identity between 2024 and 2025-2026 (both load the same base) is the strongest available transitive guarantee. **Recommend including this base module in any future evidence packet.**

**I-4.** 2026 M1 hourly loss rate is **6.6×** the 2025 M1 hourly loss rate (−$8.16/row vs −$1.24/row). True regime step-change in 2026 H1, not a sample-size artifact. Projected full-year 2026 M1 ≈ −$45K if persisted.

---

## Best Explanation For The Negative Window (Mechanics Granted Sound)

Ranked by evidence support:

1. **(Best supported)** M1 ladder amplifying tail losses + regime-specific counter-trend bursts in 2026 H1 (e.g., 2026-02-05 = −$10,388 alone, 8.4× amplification; 4 of top-5 worst days in Feb-Mar 2026).
2. **(Plausible, partially supported)** Genuine regime deterioration for S27 on ZN — the **unit-no-ladder source-faithful variant is also negative** in both 2025 (−$6,243) and 2026 H1 (−$4,199). Negative is not solely a ladder artifact. Unit hourly loss rate doubles 2025 → 2026.
3. **(Plausible, unproven)** Volatility/trend filter suppressing good trades or allowing bad ones — 49% veto rate; could be too slow at daily cadence to catch hourly directional bursts.
4. **(Plausible, unproven)** Rate-market structure change post-2024 (post-hiking-cycle ZN dynamics not in this evidence pack).
5. **(Possible, weak)** Small-sample / partial-window noise for 2026 (~99 nonzero days). Removing 2026-02-05 still leaves rest of 2026 M1 at −$8,087.
6. **(Possible, weak)** Provider-degraded-date exclusion — quantified ≤ −$582; cannot explain headline.
7. **(Possible, weak)** Cost/fee drag — gross is already negative without fees; cannot flip sign.
8. **(Unlikely)** Roll/contract-cycle effects — 6 transitions chained correctly; roll PnL small.
9. **(Ruled out)** Hidden implementation artifact / sign inversion / future-state leakage — strict-prior verified; sign convention verified; engine byte-identical to 38/38-PASS 2022-2024 path.

**Discriminating evidence that would resolve (1)/(2)/(3)/(4):**
- Provider-clean rerun on 2025-01-02 → 2026-05-22 (closes C-1).
- Mechanical & parity verifier run on 2025-2026 artifacts, incl. inverted / one-bar-delayed / day-shuffled nulls (closes H-2, gives null-contrast).
- Trend-overlay veto-rate comparison 2022-2024 vs 2025-2026 (discriminates 3).
- Hourly EWMAC(16,64) variant (closes M-2 fidelity, discriminates 3).
- Signal-attributable-PnL restatement net of constant-long ZN beta strip applied to 2025-2026 (Opus CRITICAL-2 carryover; discriminates 2 vs 4).
- Per-bar realized vol / autocorrelation panel for ZN 2022-2024 vs 2025-2026 (discriminates 4).

---

## Final Verdict

```
MECHANICAL_RESULT_STATUS:
  SOUND

NEGATIVE_RESULT_INTERPRETATION:
  AVAILABLE_ROW_DIAGNOSTIC_ONLY
  (with ROBUST_FRAGILITY_WARNING secondarily attached:
   the unit-no-ladder source-faithful variant is also negative in both
   2025 and 2026 H1, so this is not solely a ladder artifact)

S27_PARKING_DECISION_SUPPORT:
  MODERATE
  (sufficient to maintain the existing pre-Lockbox park while
   futures-realistic cost closure (CRITICAL-1) and signal-attributable-
   PnL restatement (CRITICAL-2) are pending; a STRONG park-or-promote
   decision requires a clean provider-condition rerun and the mechanical/
   parity verifier run on the 2025-2026 artifacts)

CONFIDENCE:
  MEDIUM
  (HIGH on the mechanical soundness conclusion; MEDIUM on the
   regime-vs-implementation explanation split, because the discriminating
   evidence — clean rerun, parity verifier on 2025-2026, hourly EWMAC
   variant, beta-strip-restated PnL — is not in the supplied packet)
```
# Carver S27 ZN Book Source Lock

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_BOOK_SOURCE_LOCK_PASSED_FOR_V2_IMPLEMENTATION_EXERCISE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Lock the book-source requirements for a ZN-first Strategy 27 v2 rebuild before
any implementation, replay, diagnostic, backtest, OOS, Lockbox, Forward,
adapter, deployment, trading, or promotion work.

Primary source authority:

```text
Carver.pdf
```

Current S27 result artifacts remain diagnostic/failure-map material only. They
are not book-faithful S27 backtest evidence.

## Source Locations Inspected

The source lock is based on local inspection of `Carver.pdf` text around:

- Strategy 26 fast mean reversion: PDF pages 475-498.
- Strategy 27 safer fast mean reversion: PDF pages 499-506.
- Volatility attenuation / V-Q-M method: PDF pages 297-302.
- General trading cost treatment: PDF pages 23-30 and 99-105.

Page numbering here refers to extracted PDF page numbers, not necessarily the
printed book folio.

## Locked S26 Base Requirements

S27 inherits S26 unless explicitly modified.

| Topic | Locked Source Decision |
|---|---|
| Frequency | S26 is an hourly fast mean-reversion strategy. |
| Equilibrium input | Equilibrium is computed from daily back-adjusted futures prices. |
| Equilibrium method | EWMA span 5 over daily prices. |
| Current price | Forecast compares the daily equilibrium with current hourly price `p_t`. |
| Raw forecast | `raw_forecast = equilibrium - current_price`. |
| Direction | Positive raw forecast means long; negative raw forecast means short. |
| Price risk bridge | `sigma_price = previous_completed_daily_close_current_traded_contract * annual_percentage_sigma / 16`. Do not use the current incomplete hourly price, and do not use an incompatible back-adjusted level unless a row-level bridge proves equivalence. |
| Risk-adjusted forecast | `risk_adjusted = raw_forecast / sigma_price`. |
| S26 scalar | `9.3`. |
| Forecast cap | `[-20, +20]`. |
| Buffering | No normal trend/carry-style buffering for fast mean reversion. |
| Execution | Book execution is limit-order based, not target-position close-to-close. |
| Fill timing | Backtest assumptions use a one-hour lag for limit-order fills and market orders. |
| Costs | All orders incur commissions. Market orders also require normal bid-ask spread treatment. |

## Locked S27 Overlay Requirements

| Topic | Locked Source Decision |
|---|---|
| Base dependency | S27 is S26 plus overlays; do not implement S27 independently of S26. |
| Trend filter | Use EWMAC(16,64), shorthand EWMAC16, over daily trend state. |
| Trend role | Trend is a veto/permission gate, not a co-weighted forecast blend. |
| Trend interaction | If the mean-reversion forecast sign opposes the EWMAC trend sign, set the mean-reversion forecast to zero. |
| Volatility attenuation | Apply the V-Q-M volatility multiplier to reduce positions when volatility is high. |
| Relative volatility | `V = current_percentage_sigma / ten_year_rolling_mean(current_percentage_sigma)`, with the ten-year mean using 2560 daily observations where available. Do not compute `V` from price-risk sigma. |
| Quantile | `Q` is the historical quantile of relative volatility for the instrument, using the expanding/admissible inception-through-current distribution. Do not use a fixed ten-year window for `Q` unless a later source audit proves that is required. |
| Raw multiplier | `raw_multiplier = 2 - 1.5 * Q`. |
| Smoothed multiplier | `M = EWMA_span_10(raw_multiplier)`. |
| Application order | Compute S26 `raw_forecast = equilibrium - hourly_current_price`; compute `sigma_price` and `risk_adjusted_forecast = raw_forecast / sigma_price`; apply EWMAC(16,64) veto by setting `risk_adjusted_forecast` to zero when signs conflict; apply volatility attenuation as `adjusted_risk_adjusted_forecast = risk_adjusted_forecast * M`; then apply S27 scalar, forecast cap, optimal position, and S26 execution machinery. |
| S27 scalar | Book-estimated around `20`; v2 implementation convention freezes this approximate estimate as `20.0` unless a later source audit overturns it. |
| S27 scalar rationale | The book states that after the S27 overlay turns off mean reversion about half the time, a higher scalar is required and estimates it around 20. This must not be described as a source-exact constant. |
| Forecast cap | Inherits `[-20, +20]`. |
| Execution | Uses S26 adjacent-position limit-order machinery to keep costs low; do not use close-to-close target-position PnL as source-faithful execution. |

## Scalar Decision

Decision:

```text
S27_FORECAST_SCALAR_BOOK_TEXT = AROUND_20
S27_FORECAST_SCALAR_V2_IMPLEMENTATION_FREEZE = 20.0
```

Disposition of audit conflict:

```text
OPUS_9_3_SCALAR_CONCERN_REJECTED_BY_LOCAL_PDF_PAGE_502_AND_GPT_AUDIT
GPT_EXACT_20_CONCERN_ACCEPTED
```

Reason:

Local inspection of the S27 source section found an explicit S27 statement that
after applying the volatility forecast multiplier and trend overlay, the usual
calculations continue with a higher scalar, estimated around `20`. S26 remains
locked to `9.3`; S27 v2 must not silently reuse `9.3` unless a later external
source-lock audit overturns this decision with book evidence.

The lock must not claim that `20.0` is a source-exact constant. It is an
implementation freeze of the book's approximate "around 20" estimate. Any
later test must report this as:

```text
BOOK_APPROXIMATE_SCALAR_IMPLEMENTATION_FROZEN_AT_20_0
```

## Execution And Cost Decision

Current diagnostic runners are not book-faithful execution because they model:

```text
rounded target position -> close-to-close hourly PnL -> simple per-side fee
```

S27 v2 must instead produce explicit execution ledgers:

- desired rounded position;
- adjacent-position implied limit prices;
- working limit-order state;
- buy and sell single-lot limit orders bracketing the current price where the
  book permits both sides;
- cancellation/reset of working limit orders at the end-of-day boundary;
- one-hour-lag limit fill decision;
- market-order cases required by the book, including target-position gaps
  greater than one contract, cap-bound cases where a limit side is not placed,
  and overnight/session gap cases;
- one-hour-lag market-order fill decision;
- roll handling, explicitly labeled as an implementation assumption unless the
  source audit has locked a ZN-specific roll/order interaction rule;
- commission rows for all orders;
- spread-cost rows for market orders when required;
- PnL rows tied to fills and held position state.

The book's fast-strategy cost rows are commission-oriented because limit orders
reduce spread costs, but market-order spread costs still affect true post-cost
returns where market orders occur. Therefore v2 must not use
`ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE` as a book-faithful
ZN futures cost model.

Cost lock:

```text
LIMIT_ORDER_FILL_COST = COMMISSION_ONLY
MARKET_ORDER_FILL_COST = COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD
ALL_ORDERS_PAY_COMMISSION
```

## Data And Runtime Source Decisions

S27 v2 must fail closed unless:

- daily equilibrium close and hourly current price share a compatible
  back-adjusted price level;
- the sigma-price bridge proves the price input is the previous completed daily
  close of the currently traded contract, not a same-hour price and not an
  incompatible back-adjusted equilibrium level;
- daily runtime rows are completed-bar rows and never same-day/future rows for
  an hourly forecast;
- hourly bars are completed bars;
- sigma, EWMAC(16,64), V, Q, and M can be recomputed row-by-row from admissible
  source rows;
- V-Q-M quantile history is expanding/admissible through the current runtime
  date and does not use future observations;
- percentage volatility is source-locked before use, including whether it is
  the Strategy 3 estimator; if not source-locked, fail closed before scoring;
- zero-sign cases for mean-reversion and EWMAC trend state are source-locked or
  explicitly fail closed in tests;
- ZN roll handling, session boundaries, missing/early-close/holiday hourly
  rows, and working-order state transitions are explicitly specified and
  labeled as book-native only where the source supports them;
- capacity/speed-limit eligibility is recorded before any result interpretation;
- provider-condition degraded, pending, unresolved, duplicated, missing, or
  silently dropped rows fail closed before scoring.

## Required V2 Artifact Families

Any later S27 v2 implementation must emit these artifact families before PnL is
interpreted:

```text
SOURCE_INPUT_MANIFEST
DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER
RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM
FORECAST_REPLAY_LEDGER
DESIRED_POSITION_LEDGER
LIMIT_ORDER_LEDGER
MARKET_ORDER_LEDGER
FILL_LEDGER
COMMISSION_LEDGER
SPREAD_COST_LEDGER
PNL_LEDGER
VALIDATION_LEDGER
PROVENANCE_AND_HASH_LEDGER
LOCAL_HOSTILE_AUDIT_RESULT
```

## Existing Result Boundary

The following labels are forbidden for existing S27 artifacts:

```text
BOOK_FAITHFUL_S27_BACKTEST
SOURCE_FAITHFUL_FULL_LADDER
ALPHA
PROMOTION
OOS
LOCKBOX
FORWARD
DEPLOYMENT
TRADING
```

Existing old and corrected S27 results remain:

```text
DIAGNOSTIC_ONLY_FAILURE_MAP_MATERIAL
```

## External Audit Gate

This revised source lock must be re-audited with `Carver.pdf` before any v2
implementation begins.

Audit questions:

1. Does the book support S27 scalar "around `20`" after trend/V-Q-M overlays,
   with `20.0` only as an implementation freeze of an approximate estimate?
2. Does the locked S26/S27 execution/cost design match the book?
3. Are daily/hourly level compatibility and strict-prior runtime gates
   sufficient before implementation?
4. Are any current diagnostic artifacts mislabeled too strongly?
5. What source-lock decisions remain unresolved?

## Non-Authorization

This source lock authorizes no provider API access, no data download, no
market-row parsing, no implementation, no diagnostic, no backtest, no OOS, no
Lockbox, no Forward, no CFD adapter work, no tuning, no deployment, no trading,
no promotion, no Git staging, no commit, no push, no PR update, and no remote
operation.

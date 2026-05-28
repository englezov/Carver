# Carver First Portfolio Spine Implementation Gate

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_FIRST_PORTFOLIO_SPINE_IMPLEMENTATION_GATE_SYNTHETIC_CONFORMANCE_ONLY
```

## Purpose

Open a narrow implementation gate for the first Carver daily source-native futures portfolio spine:

```text
M0 minimal conventions -> M1 sizing/risk scaling -> M3 portfolio construction -> S01/S02/S03/S04 -> P01/P02 synthetic conformance
```

This gate exists to prove that the machinery connects and fails closed under controlled synthetic inputs. It does not authorize market data, NinjaTrader export/parsing, diagnostics, historical backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab imports, tuning, deployment, trading, or promotion.

## Authorized Implementation Surface

Authorized code may include only:

- Minimal M0 source-native lane and completed-bar guardrails.
- M1 percentage-risk position sizing from pre-validated synthetic inputs.
- M1 is percentage-risk sizing only in this chapter. Negative-price daily price-point sizing remains an unresolved source atom for a later gate, not an implicit fallback here.
- M3 portfolio member/weight validation and per-leg sizing context emission.
- Thin S01/S02/S03/S04/P01/P02 orchestration over M0/M1/M3.
- Synthetic fixtures and focused conformance tests.

M2, M5, S09, S10, and S11 are not opened by this gate. Interface placeholders are allowed only if needed to keep M1/M3 boundaries explicit, but no forecast, carry, or historical strategy logic is authorized.

## Synthetic-Only Rule

All tests under this gate must be synthetic and hand-built.

Allowed examples:

- A completed daily synthetic timestamp.
- Toy instrument metadata with source-native futures symbols.
- Toy price, FX, risk, capital, target-risk, weight, and IDM values.
- Invariant checks such as doubling capital doubling unrounded contracts.

Forbidden examples:

- Reading local or remote market rows.
- Exporting or parsing NinjaTrader data.
- Loading CSV, database, platform cache, API, brokerage, account, credential, or order-routing files.
- Comparing against historical realised performance.
- Running diagnostics or backtests.

## Conformance Obligations

The first implementation must prove:

- Non-`SOURCE_NATIVE_FUTURES` lanes fail closed.
- Incomplete bars fail closed.
- Timestamp-misaligned synthetic inputs fail closed.
- Missing or invalid price, risk, FX, multiplier, capital, target risk, weight, or IDM fail closed.
- M1 produces unrounded and rounded desired contract counts from pre-validated synthetic inputs.
- M1 stops at desired exposure and does not decide execution, buffering, or trade/no-trade.
- M3 validates P01 50/50 weights and P02 25/12.5/12.5/12.5/12.5/25 weights.
- M3 does not calculate IDM from data.
- P01 and P02 synthetic sizing uses completed daily inputs only.
- No source-native contract is silently substituted.

## Deliverables

- `src/carver/` package with minimal M0/M1/M3 and first-spine orchestration.
- `tests/` synthetic conformance tests.
- This implementation gate memo.
- Hostile audit after tests pass.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no NinjaTrader export, no implementation beyond the synthetic first-spine surface above, no diagnostics, no historical backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

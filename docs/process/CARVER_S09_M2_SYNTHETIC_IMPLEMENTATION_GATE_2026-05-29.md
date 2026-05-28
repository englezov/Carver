# Carver S09/M2 Synthetic Implementation Gate

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S09_M2_FORECAST_GATE_NOT_DATA_NOT_BACKTEST
```

## Purpose

Open the first Carver trend-alpha code surface without opening real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, deployment, trading, or promotion.

This gate covers:

- M2 forecast-block arithmetic: raw forecast input, scalar, individual cap, equal weights across locked eligible rules, FDM, and final cap.
- S09 EWMAC trend forecasts from completed daily close inputs.
- A P05 shape record for the later Jumbo multiple-trend portfolio, without implementing or running that portfolio.

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` work is opened by this gate.

## Source-Locked For Synthetic Code

- S09 EWMAC speed set: `2, 4, 8, 16, 32, 64`, where `EWMACn = EWMAC(n, 4n)`.
- S09 forecast scalars from Table 29: `12.1, 8.53, 5.95, 4.10, 2.79, 1.91`.
- Individual forecast cap: absolute value `20`.
- S09 Table 36 FDM rows for allowed speed sets.
- Combined forecast cap after FDM: absolute value `20`.
- Completed daily bars only.

## Explicit Synthetic Convention

The synthetic code uses recursive EWMA with:

```text
alpha = 2 / (span + 1)
initial EWMA = first completed close
minimum observations = slowest admitted span + 1
```

This convention is locked only for synthetic conformance tests. It is not a real-data/backtest authorization and does not settle the future production-data warm-up policy.

## Still Blocked For Real Data

Real S09 data work remains blocked until separate artifacts lock:

- exact source-native instrument universe;
- provider mapping for each instrument;
- completed daily session and timestamp convention;
- continuous-contract and roll/back-adjustment rules;
- daily price-point risk source;
- cost source and exact speed/cost eligibility rule;
- buffer zone and trade/no-trade rule;
- evidence window budget.

The prior Opus finding on the `0.15 SR` speed-limit citation remains unresolved for real data. Therefore this gate does not compute eligibility from costs. It accepts only an explicitly locked eligible EWMAC speed set and fails closed otherwise.

## P05 Boundary

P05 Jumbo multiple trend is recorded only as a future portfolio shape:

```text
S09 over a source-locked Jumbo futures universe with per-instrument eligible EWMAC speed sets.
```

No P05 universe, data pull, computation, diagnostic, backtest, or performance interpretation is authorized by this gate.

## Non-Authorization

This gate authorizes no real data/API/WebSocket access, no NinjaTrader export, no market-row parsing, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

# Carver S09 ZN Direct-Daily API Probe Gate

Date: 2026-05-29

Status:

```text
CARVER_S09_ZN_DIRECT_DAILY_API_PROBE_AUTHORIZED_NOT_BACKTEST_NOT_DIAGNOSTIC_AWAITING_LOCAL_CREDENTIALS
```

## Purpose

Record the single authorized read-only NinjaTrader/Tradovate market-data API probe for S09 ZN.

This gate authorizes only one market-data chart request:

```text
endpoint: md/getChart
contract: ZN
contract month: 06-26
display symbol: ZN JUN26
provider symbol id: 4470301
bar type: DailyBar
element size: 1
element count: 257
intake route: DIRECT_DAILY_PRIMARY
```

The 257-bar request is the locked warm-up boundary for EWMAC64: the slow leg is `64 * 4 = 256`, and the synthetic convention requires one additional completed daily bar.

## Allowed Local Credential Sources

Credentials or access tokens must be supplied only through local ignored state:

```text
runtime/tradovate_api_probe.env
```

or equivalent process environment variables:

```text
CARVER_TRADOVATE_MD_ACCESS_TOKEN
```

Only a pre-supplied market-data token is admitted by this gate. Username/password login and REST token generation are intentionally not implemented here, because that would open another API endpoint outside the one-probe market-data boundary.

No credential value belongs in Git, chat, terminal output, docs, screenshots, or committed artifacts.

Official credential requirements were investigated separately in:

```text
docs/process/CARVER_TRADOVATE_API_CREDENTIAL_REQUIREMENTS_INVESTIGATION_2026-05-29.md
```

That investigation keeps this gate as `CARVER_TRADOVATE_MD_ACCESS_TOKEN` only. Implementing `/auth/accesstokenrequest` would require a separate explicit credential/auth gate and hostile audit before use.

## Implemented Client Boundary

The local client is:

```text
src/carver/spine/tradovate_api_probe.py
```

It permits only these WebSocket endpoints:

```text
authorize
md/getChart
md/cancelChart
```

It rejects order, account, report, arbitrary market-data, bulk, histogram, non-ZN, non-DailyBar, non-257, and non-source-native request shapes before execution.

It also atomically claims a single-probe sentinel in the locked quarantine directory before the WebSocket request is sent. After one started probe, repeated execution is blocked unless a future operator gate explicitly resets the ignored sentinel/output state.

The intended command, after local ignored credentials are supplied, is:

```powershell
$env:PYTHONPATH="src"; python -c "from carver.spine.tradovate_api_probe import main; raise SystemExit(main())"
```

The command may print only a status line and the ignored quarantine output path. It must not print secrets.

## Quarantine Output

The only allowed output location is Git-ignored:

```text
data/quarantine/ninjatrader/web_chart/
```

The output JSON must retain the exact request binding and raw market-data messages inside the same quarantined envelope, so existing request-bound normalizers can reject cross-request replay.

## Current Execution State

Local credential check on 2026-05-29 found:

```text
runtime/tradovate_api_probe.env: absent
CARVER_TRADOVATE_* environment credential source: absent
```

Therefore the real API probe was not executed in this pass.

## Non-Authorization

This gate authorizes no order/account/report endpoints, no trading, no deployment, no backtest, no diagnostics, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab imports, no tuning, no bulk download, no credential printing, no credential committing, and no remote push by inference.

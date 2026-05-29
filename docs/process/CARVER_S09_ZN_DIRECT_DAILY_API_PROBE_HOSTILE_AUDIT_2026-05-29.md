# Carver S09 ZN Direct-Daily API Probe Hostile Audit

Date: 2026-05-29

Status:

```text
PROCESS_SAFE_FOR_LOCAL_COMMIT_API_PROBE_NOT_EXECUTED_AWAITING_LOCAL_MD_TOKEN
```

## Scope

Hostile audit inspected the S09 ZN direct-daily Tradovate API probe package:

- `src/carver/spine/tradovate_api_probe.py`
- `src/carver/spine/__init__.py`
- `tests/test_tradovate_api_probe_synthetic.py`
- `docs/process/CARVER_S09_ZN_DIRECT_DAILY_API_PROBE_GATE_2026-05-29.md`

No real API probe, market-row parsing, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab import, deployment, trading, promotion, credential extraction, credential printing, or remote push was authorized or performed by the audit.

## Initial Findings Patched

The first hostile audit found and the implementation patched:

- REST token generation was removed; the gate now accepts only a pre-supplied local `CARVER_TRADOVATE_MD_ACCESS_TOKEN`.
- The WebSocket URL was restricted to the market-data endpoint `wss://md.tradovateapi.com/v1/websocket`.
- The quarantine root was hard-bound to the clean Carver workspace path `data/quarantine/ninjatrader/web_chart`.
- A single-probe sentinel was added.
- The `websockets>=16.0` dependency was declared.

The second hostile audit found the sentinel needed to be claimed before any network call. The implementation then changed the sentinel into an atomic pre-network claim using exclusive file creation. A partially consumed probe leaves the sentinel in `STARTED` state and blocks reruns unless a future operator gate explicitly resets ignored runtime/quarantine state.

## Final Hostile Audit Verdict

The final re-audit found no remaining blockers in the scoped files.

Confirmed clean:

- request locked to ZN provider id `4470301`;
- request locked to `DailyBar`, element size `1`, element count `257`;
- only `authorize`, `md/getChart`, and `md/cancelChart` WebSocket endpoints are framed;
- no REST token generation remains;
- no browser storage, cookie, password, or credential extraction exists;
- no order, account, or report endpoint path exists;
- no returns, PnL, Sharpe, drawdown, diagnostic, backtest, OOS, Lockbox, Forward, deployment, trading, or promotion logic exists;
- no old `QuantLab_v3` import or active-pipeline dependency exists;
- the single-probe sentinel is claimed before the WebSocket call and completed only after output write;
- `md/cancelChart` is attempted in a `finally` block once chart ids exist.

## Execution State

The real API probe remains unexecuted because no local credential source is present:

```text
runtime/tradovate_api_probe.env: absent
CARVER_TRADOVATE_MD_ACCESS_TOKEN: absent
```

The client fails closed with:

```text
CARVER_S09_ZN_DIRECT_DAILY_API_PROBE_BLOCKED
```

## Non-Authorization

This audit authorizes no real API execution by inference, no additional instrument, no additional endpoint, no second probe, no data diagnostics, no backtest, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.

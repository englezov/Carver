# Carver NinjaTrader Tradovate Web Chart API Gate

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_TRADOVATE_WEB_CHART_API_GATE_SYNTHETIC_ONLY
```

## Purpose

Define a controlled Web Chart API intake path so Carver does not depend on manual NinjaTrader UI exports.

The NinjaTrader web app was observed issuing chart requests through the Tradovate-compatible market-data WebSocket API. This gate documents the observed/public chart shape and implements synthetic-only request/response normalization. It does not authorize real API calls.

## Observed Web-App Surface

Read-only browser inspection of the logged-in web app observed chart request logs shaped like:

```json
{
  "symbol": "3570919",
  "chartDescription": {
    "underlyingType": "MinuteBar",
    "elementSizeUnit": "UnderlyingUnits",
    "elementSize": 5,
    "withHistogram": false
  },
  "timeRange": {
    "asMuchAsElements": 300
  }
}
```

The public Tradovate API documents endpoint `md/getChart`, chart types `MinuteBar` and `DailyBar`, and chart payloads containing OHLC bars plus up/down volume fields.

The synthetic response envelope assumed by this gate is:

```json
{
  "ok": true,
  "body": {
    "items": [
      {
        "timestamp": 1780000000000,
        "open": 1,
        "high": 1,
        "low": 1,
        "close": 1,
        "volume": 1,
        "complete": true
      }
    ]
  }
}
```

Each symbol must be locked by contract identity, contract month, display symbol, and provider numeric symbol id before any request payload can be built. The initial locked observed mappings are:

```text
ES 06-26 ES JUN26 -> 3570919
ZN 06-26 ZN JUN26 -> 4470301
```

No other provider symbol id is admitted by this synthetic gate.

## Authorized Implementation Surface

Authorized code may include only:

- Synthetic request objects for `md/getChart`.
- Endpoint allow-listing for `md/getChart` and `md/cancelChart` only.
- Read-only chart response normalization from synthetic payloads.
- Minute and daily OHLCV bar validation.
- Guardrails rejecting order/trading/report/account endpoints, arbitrary symbols, non-source-native lanes, and bulk requests.
- A disabled probe descriptor documenting what a future one-symbol probe would need, without executing it.

## Explicit Non-Authorization

This gate authorizes no real API download, no WebSocket connection, no token/cookie extraction, no browser storage inspection, no order endpoint, no account endpoint, no report endpoint, no bulk download, no market diagnostic, no historical backtest, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.

## Future Probe Boundary

A future probe, if separately authorized, must be one explicit read-only `md/getChart` request for one visible source-native contract and a small element count. It must cancel its chart subscription immediately after receipt and save any raw response only under a Git-ignored quarantine path.

No such probe is authorized by this file.

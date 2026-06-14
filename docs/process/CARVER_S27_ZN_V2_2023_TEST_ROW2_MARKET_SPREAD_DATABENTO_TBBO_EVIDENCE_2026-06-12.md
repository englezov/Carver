# CARVER S27 ZN V2 2023 TEST Row-2 Market Spread DataBento TBBO Evidence

Date: 2026-06-12

Status:

```text
PASS_BOUNDED_DATABENTO_TBBO_ROW2_SELL_BID_SIDE_SPREAD_EVIDENCE_SELECTED_NOT_COST_EMISSION
```

Authorization:

```text
S27_V2_BOUNDED_DATABENTO_ROW2_MARKET_SPREAD_EVIDENCE_ACQUISITION
```

Request:

```text
provider = DATABENTO_HISTORICAL
dataset = GLBX.MDP3
schema = tbbo
stype_in = raw_symbol
raw_symbol = ZNH3
market_order_side = SELL
request_start_utc = 2023-01-03T01:59:55Z
request_end_utc = 2023-01-03T02:00:05Z
fill_timestamp_utc = 2023-01-03T02:00:00Z
request_count = 1
```

Selected TBBO spread evidence:

```text
selected_quote_ts_event = 2023-01-03T01:59:56.651440427Z
quote_age_seconds = 3.34856
bid_px_00 = 112.578125
ask_px_00 = 112.59375
selected_executable_market_fill_price = 112.578125
executable_market_fill_price_source = BID_PRICE_FOR_SELL_MARKET_ORDER
spread_points = 0.015625
point_value_usd = 1000.0
spread_cost_usd_per_contract = 15.625
fill_quantity = 2
spread_cost_amount_usd = 31.25
row_hash = 0785dcfa6525897f07344c9f016cf832217e94cd79e2e6e4c3220b7f70d6d0b7
```

Raw provider evidence:

```text
raw_dbn_sha256 = 4A2697D54982E520B2A8114EDD78BA75705BB208EF5C7C72184919F2B737D15D
raw_csv_sha256 = 0669FC7595BE6BDE657B56D910E30EA3C3777EC1F58825CA2C23B1DAA4E83E1F
quote_rows_returned = 2
```

Boundary:

This is provider bid/ask spread and bid-side executable market-fill evidence only. It is not book-explicit authority, not actual cost emission, not PnL, not a result, not a backtest, not result interpretation, not PnL evaluation, and not a source-faithful evidence claim.

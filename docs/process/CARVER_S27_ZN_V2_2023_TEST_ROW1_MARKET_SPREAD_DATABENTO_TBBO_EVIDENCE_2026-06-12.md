# CARVER S27 ZN V2 2023 TEST Row-1 Market Spread DataBento TBBO Evidence

Date: 2026-06-12

Status:

```text
PASS_BOUNDED_DATABENTO_TBBO_SPREAD_EVIDENCE_SELECTED_NOT_COST_EMISSION
```

Authorization:

```text
S27_V2_BOUNDED_DATABENTO_ROW1_MARKET_SPREAD_EVIDENCE_ACQUISITION
```

Request:

```text
provider = DATABENTO_HISTORICAL
dataset = GLBX.MDP3
schema = tbbo
stype_in = raw_symbol
raw_symbol = ZNH3
request_start_utc = 2023-01-03T00:59:55Z
request_end_utc = 2023-01-03T01:00:05Z
fill_timestamp_utc = 2023-01-03T01:00:00Z
request_count = 1
```

Selected TBBO spread evidence:

```text
selected_quote_ts_event = 2023-01-03T00:59:57.009985Z
bid_px_00 = 112.546875
ask_px_00 = 112.5625
spread_points = 0.015625
point_value_usd = 1000.0
spread_cost_usd_per_contract = 15.625
fill_quantity = 2
spread_cost_amount_usd = 31.25
row_hash = c910df21177b2e1aa0cfcd5edadd03be38f130e8b06cb8f4b2bca79bf8390d0b
```

Raw provider evidence:

```text
raw_dbn_sha256 = 560417500AD827716F4623FABAA5AF6FE401285780B9E4730F3272636624D7D2
raw_csv_sha256 = 98F8A17AE9C136ED41A2A17B7ABB1E60AA17EB2D97FF212BD11347C6A2F37C61
quote_rows_returned = 10
```

Boundary:

This is provider bid/ask spread evidence only. It is not book-explicit authority, not actual cost emission, not PnL, not a result, not a backtest, not result interpretation, not PnL evaluation, and not a source-faithful evidence claim.

## Interpretation Boundary

The selected DataBento TBBO quote proves the observed full top-of-book spread:

```text
ask_px_00 - bid_px_00 = 112.5625 - 112.546875 = 0.015625 points
full_spread_value = 0.015625 * 1000.0 = 15.625 USD per contract
```

The current market fill metadata uses:

```text
market fill price = 112.5625
fill price provenance = MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE
```

Because the selected TBBO ask equals the current market-fill price, a future actual-cost gate must explicitly choose and justify the accounting convention before emitting cost or PnL. Two possible conventions are:

```text
ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
MID_OR_CLOSE_PROXY_WITH_SEPARATE_HALF_SPREAD_COST
```

This evidence gate does not choose either convention. It only binds the source-native quote spread and keeps actual cost/PnL fail-closed.

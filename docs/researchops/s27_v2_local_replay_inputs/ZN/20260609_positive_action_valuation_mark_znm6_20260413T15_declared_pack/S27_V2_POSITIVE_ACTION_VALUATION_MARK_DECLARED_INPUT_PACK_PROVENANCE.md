# S27_V2 Positive-Action Valuation Mark Declared Input Pack Provenance

Date: 2026-06-09

Status:

```text
LOCAL_INPUT_PACK_DECLARED_FOR_POSITIVE_ACTION_VALUATION_MARK_DEV_RECON_ONLY_NOT_PNL_NOT_BACKTEST_NOT_RESULT
```

## Scope

This pack declares the exact next completed local hourly valuation mark row after the audited `ZNM6` positive-action limit fill:

```text
fill_timestamp_utc = 2026-04-13T14:00:00Z
valuation_mark_completed_timestamp_utc = 2026-04-13T15:00:00Z
raw_symbol = ZNM6
close_price = 111.046875
```

The valuation convention is:

```text
SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL
```

## Source Row

Already-local source file:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/databento_ohlcv_1h_extended_forecast_only_quarantine/sanitized_bars/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_sanitized_quarantine_ohlcv_1h.csv
```

Source file SHA256:

```text
EF3425BD6A093D76B4073DCDFEE6E7E9A7E27618EEEAB41024DE39B6FDA6D511
```

Source row line number:

```text
18
```

Source row text SHA256, including the source file's current CRLF newline bytes:

```text
F39F5056C9D1E122E6F62D82E8918745E10233AA95ABEF9949AC5F50BE6F98DA
```

Canonical source-row JSON SHA256:

```text
A8D60EE8A26EE10B8460FEA2F46C656EBA0EEB7BE507BADD4FE44434DE8B413A
```

## Boundary

This pack is local Development/Reconciliation input only. It is not an actual PnL ledger, not a result, not a backtest, not backtest readiness, not result interpretation, not PnL evaluation, not promotion, and not a source-faithful evidence claim.

Provider/API access, market-data downloads, new data acquisition, OOS/Lockbox/Forward access, actual PnL emission, result emission, Git actions, adapter/deployment/trading/promotion, and tuning remain unauthorized.

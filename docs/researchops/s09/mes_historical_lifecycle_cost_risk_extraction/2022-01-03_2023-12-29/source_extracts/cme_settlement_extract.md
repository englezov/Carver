# CME Equity Index Settlement Static Extract

Date captured: 2026-06-03

Source URL:

```text
https://www.cmegroup.com/trading/equity-index/settlement.html
```

Use in this S09 MES gate:

```text
OFFICIAL_STATIC_GENERIC_FINAL_SETTLEMENT_SOURCE
```

Extracted static facts for this process packet:

- CME describes S&P 500/e-mini style final settlement using a Special Opening Quotation on expiration Friday.
- Open expiring positions are cash settled after the final settlement price is determined.
- This supports classifying MES as a cash-settled equity-index lifecycle family for this process packet.

Boundary:

This local extract supports generic cash/final-settlement family evidence only. It does not settle provider-date versus exchange-session roll semantics, and it does not authorize any market-row parsing, strategy computation, or backtest.

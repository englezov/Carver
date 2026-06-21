# CME Historical Fees Source Location Extract

Date captured: 2026-06-03

Source URL:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees.html
```

Use in this S09 MES gate:

```text
OFFICIAL_STATIC_HISTORICAL_FEE_SOURCE_LOCATION_ONLY
```

Extracted static facts for this process packet:

- CME publishes historical exchange fee schedules.
- The page provides source locations for historical years including the 2021-2024 period relevant to the MES chain.
- This pass records source availability only; it does not extract or lock actual MES fee values.

Boundary:

Actual historical MES cost values, membership/customer class, broker commission, NFA/regulatory fees, spread/slippage, and per-side versus round-turn convention remain fail-closed.

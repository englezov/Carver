# Carver S27 Scalar Source Correction

Date: 2026-05-31

Status:

```text
PROCESS_AND_CODE_S27_SCALAR_SOURCE_CORRECTION_NOT_TEST_NOT_BACKTEST_NOT_PROMOTION
```

## Scope

This record corrects the S27 scalar atom and the S27 forecast-only machinery.

Previous local wording treated S27 as inheriting the S26 forecast scalar `9.3`.
That wording is not source-faithful once the S27 Chapter 27 scalar paragraph is read directly.

## Source Finding

Source authority:

```text
Carver.pdf
```

S26 source atom:

```text
S26 forecast scalar = 9.3
Source: p. 480
```

S27 source atom:

```text
S27 applies the trend overlay and V/Q/M volatility multiplier, then uses a higher forecast scalar estimated around 20.
Source: p. 502
```

The S27 cap remains the common forecast cap:

```text
S27 forecast cap = +/-20
```

## Code Boundary Correction

Corrected code:

```text
src/carver/spine/s26_s27.py
src/carver/spine/__init__.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
```

Corrected constant:

```text
S27_FORECAST_SCALAR = 20.0
```

Corrected paths:

```text
s27_safer_fast_mean_reversion_forecast
s27_forecast_only_from_s26_forecast_row
```

Both S27 paths now scale the S27 risk-adjusted forecast with `S27_FORECAST_SCALAR`, not `S26_FORECAST_SCALAR`.

## Documentation Correction

Corrected documentation:

```text
docs/process/CARVER_S26_S27_SOURCE_ATOM_SHEET_2026-05-30.md
docs/process/CARVER_S27_REAL_HOURLY_FORECAST_ONLY_MACHINERY_SHAPE_GATE_DRAFT_2026-05-31.md
```

## Governance Boundary

This correction does not authorize:

```text
NO_PROVIDER_API_ACCESS
NO_NEW_DATA_DOWNLOAD
NO_NEW_MARKET_ROW_PARSING
NO_DIAGNOSTICS
NO_BACKTESTS
NO_FORECAST_TEST
NO_POSITIONS
NO_COSTS
NO_CARRY
NO_TREND_SLEEVE_INTEGRATION
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_DEPLOYMENT
NO_TRADING
NO_PROMOTION
NO_GIT_OPERATIONS
```

## Result

```text
S27_SCALAR_SOURCE_STATUS: CORRECTED_TO_AROUND_20_PER_CHAPTER_27
S26_SCALAR_SOURCE_STATUS: UNCHANGED_9_3
S27_FORECAST_ONLY_MACHINERY_STATUS: PATCHED_TO_USE_S27_SCALAR
```

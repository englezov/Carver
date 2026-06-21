# S27 ZN V2 Replay Scaffold Cost Arithmetic And Transition Exclusivity Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_COST_ARITHMETIC_AND_TRANSITION_EXCLUSIVITY_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffold cost-arithmetic binding patch and transition optional-field exclusivity patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow scaffold patch only. It authorizes and performed no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Source Finding

Local hostile audit result:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_SCHEMA_HARDENING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

Open findings patched:

```text
P1_COST_ARITHMETIC_BINDING_UNDER_CONSTRAINED
P2_TRANSITION_OPTIONAL_FIELDS_NOT_FULLY_EXCLUSIVE_BY_TRANSITION_KIND
```

## Patched Files

```text
src/carver/spine/s27_v2_replay/costs.py
src/carver/spine/s27_v2_replay/transitions.py
```

## Patch Summary

Cost arithmetic binding:

- Added `spread_cost_amount` as the cost-currency amount produced by the spread calculation.
- Required `commission_amount == commission_per_contract * fill.quantity`.
- Required limit fills to have zero `spread_amount` and zero `spread_cost_amount`.
- Required market fills to have positive `spread_amount` and positive `spread_cost_amount`.
- Required `total_cost_amount == commission_amount + spread_cost_amount`.
- Preserved positive price-space spread multiplier proof.
- Required currency-space `spread_cost_amount` to equal `spread_amount`.

Transition optional-field exclusivity:

- `NORMAL_ONE_HOUR_LAG` rejects roll-boundary and overnight policy hashes.
- `EOD_OVERNIGHT_RECOMPUTE` now rejects roll-boundary hashes.
- `ROLL_BOUNDARY` now rejects overnight recompute policy hashes.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
COST_ARITHMETIC_BINDING_MARKERS_PRESENT
TRANSITION_OPTIONAL_FIELD_EXCLUSIVITY_MARKERS_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run under this authorization.

## Next Gate

The next step is a local hostile re-audit of this narrow cost-arithmetic and transition-exclusivity patch if the operator authorizes it.

Recommended authorization text:

```text
Operator authorizes local hostile re-audit of S27_V2 replay scaffold cost-arithmetic binding and transition optional-field exclusivity patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

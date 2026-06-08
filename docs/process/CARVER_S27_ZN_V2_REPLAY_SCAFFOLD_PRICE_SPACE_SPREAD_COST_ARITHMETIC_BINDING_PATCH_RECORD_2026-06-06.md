# S27 ZN V2 Replay Scaffold Price-Space Spread-Cost Arithmetic Binding Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_PRICE_SPACE_SPREAD_COST_ARITHMETIC_BINDING_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffold price-space spread-cost arithmetic binding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow scaffold patch only. It authorizes and performed no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Source Finding

Local hostile re-audit result:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_COST_ARITHMETIC_AND_TRANSITION_EXCLUSIVITY_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

Open finding patched:

```text
P1_PRICE_SPACE_SPREAD_COST_NOT_ARITHMETICALLY_BOUND_TO_NUMERIC_MULTIPLIER_AND_FILL_QUANTITY
```

## Patched File

```text
src/carver/spine/s27_v2_replay/costs.py
```

## Patch Summary

Price-space spread-cost arithmetic binding:

- Added numeric `contract_multiplier_value` to `CostLedgerRow`.
- Required positive `contract_multiplier_value` for positive `PRICE_SPACE` spread rows.
- Preserved required `contract_multiplier_value_hash` and `contract_multiplier_source_hash` provenance anchors.
- Required `PRICE_SPACE` spread cost to satisfy:

```text
spread_cost_amount == spread_amount * contract_multiplier_value * fill.quantity
```

- Required `CURRENCY_SPACE` spread rows not to carry contract-multiplier fields.
- Required contract-multiplier hashes not to appear without the numeric multiplier value.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
PRICE_SPACE_SPREAD_COST_ARITHMETIC_BINDING_MARKERS_PRESENT
CONTRACT_MULTIPLIER_VALUE_AND_PROOF_MARKERS_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

Package file count remained:

```text
19
```

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run under this authorization.

## Next Gate

The next step is a local hostile re-audit of this narrow price-space spread-cost arithmetic binding patch if the operator authorizes it.

Recommended authorization text:

```text
Operator authorizes local hostile re-audit of S27_V2 replay scaffold price-space spread-cost arithmetic binding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

# S27 ZN V2 Replay Scaffold Limit Cost-Row Optional-Field Exclusivity Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_LIMIT_COST_ROW_OPTIONAL_FIELD_EXCLUSIVITY_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffold LIMIT cost-row optional-field exclusivity patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow scaffold patch only. It authorizes and performed no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Source Finding

Local hostile re-audit result:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_PRICE_SPACE_SPREAD_COST_ARITHMETIC_BINDING_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

Open finding patched:

```text
P2_LIMIT_COST_ROW_OPTIONAL_COST_FIELDS_NOT_FULLY_EXCLUSIVE
```

## Patched File

```text
src/carver/spine/s27_v2_replay/costs.py
```

## Patch Summary

`LIMIT` cost rows remain commission-only. The patch preserves existing requirements that `LIMIT` fills have zero `spread_amount`, zero `spread_cost_amount`, and no spread policy/unit/space fields.

The patch additionally rejects irrelevant optional cost fields on `LIMIT` rows:

```text
contract_multiplier_value
contract_multiplier_value_hash
contract_multiplier_source_hash
currency_conversion_value_hash
currency_conversion_source_hash
deflation_policy_hash
```

This keeps multiplier, currency-conversion, and deflation provenance from appearing on commission-only rows where it is not part of the row's cost calculation.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
LIMIT_OPTIONAL_FIELD_EXCLUSIVITY_MARKERS_PRESENT
PRICE_SPACE_SPREAD_COST_ARITHMETIC_BINDING_MARKERS_STILL_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

Package file count remained:

```text
19
```

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run under this authorization.

## Next Gate

The standing local hostile-audit pre-approval rule permits a local hostile re-audit of this narrow patch. Any external audit handoff, parser/file replay work, diagnostics, backtests, data access, Git actions, adapter work, deployment, trading, promotion, or result interpretation still requires its own proper gate.

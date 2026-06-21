# S27 ZN V2 Replay Scaffolding Cost Schema Re-Audit Finding Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLDING_COST_SCHEMA_REAUDIT_FINDING_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffolding cost-schema re-audit finding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow cost-schema scaffold patch only. It authorizes and performed no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Re-Audit Finding Patched

Source re-audit result:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_PATCH_REAUDIT_RESULT_2026-06-06.md
```

Patched file:

```text
src/carver/spine/s27_v2_replay/costs.py
```

Patch details:

- Added explicit runtime validation that `spread_space`, when present, is a `SpreadSpace` enum value.
- Added fail-closed validation that a positive `PRICE_SPACE` spread requires contract multiplier value and source hashes.
- Preserved currency conversion as optional and paired: a conversion value requires a source hash, and a source hash requires a value hash.
- Preserved the existing fail-closed cost-schema block wrapper.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
COST_SCHEMA_PRICE_SPACE_SPREAD_MULTIPLIER_PROOF_GUARD_PRESENT
COST_SCHEMA_SPREAD_SPACE_ENUM_MEMBERSHIP_GUARD_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

The scan looked only at text and file inventory. Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run under this authorization.

## Remaining Gate

The next step is a local hostile re-audit of the cost-schema patch if the operator authorizes it. That audit may inspect the patch and process artifacts, but it must not run parser/file replay, diagnostics, backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation unless separately authorized.

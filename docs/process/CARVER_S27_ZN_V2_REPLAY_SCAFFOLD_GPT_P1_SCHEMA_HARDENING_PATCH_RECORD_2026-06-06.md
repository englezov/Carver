# S27 ZN V2 Replay Scaffold GPT P1 Schema Hardening Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_SCHEMA_HARDENING_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffold GPT P1 schema-hardening patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow schema-hardening scaffold patch only. It authorizes and performed no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Source Finding

External audit synthesis:

```text
docs/process/CARVER_S27_ZN_V2_GPT_REPLAY_SCAFFOLD_PATCHED_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

GPT verdict:

```text
PASS_WITH_REQUIRED_EDITS
```

Patch scope:

```text
GPT_P1_SCHEMA_HARDENING_ONLY
```

## Patched Files

```text
src/carver/spine/s27_v2_replay/validation.py
src/carver/spine/s27_v2_replay/identity.py
src/carver/spine/s27_v2_replay/source_universe.py
src/carver/spine/s27_v2_replay/orders.py
src/carver/spine/s27_v2_replay/fills.py
src/carver/spine/s27_v2_replay/position.py
src/carver/spine/s27_v2_replay/costs.py
src/carver/spine/s27_v2_replay/forecast.py
src/carver/spine/s27_v2_replay/transitions.py
src/carver/spine/s27_v2_replay/pnl.py
src/carver/spine/s27_v2_replay/runner.py
src/carver/spine/s27_v2_replay/source_rows.py
src/carver/spine/s27_v2_replay/level_compatibility.py
src/carver/spine/s27_v2_replay/__init__.py
```

## Patch Summary

Patched GPT P1 categories:

- added ISO date validation helpers and applied them to replay identity and source-universe bounds;
- added finite-number validation helper for value-bearing schema rows;
- added explicit local daily, hourly, session, roll, and cost-parameter source-row schemas;
- added explicit source-row exports;
- required `OrderSide` enum membership for limit orders, market orders, and fills;
- required adjacent single-lot limit orders with current-position and target-position consistency;
- required market order quantity and side to match the current-to-target position delta;
- required `rounding_policy == NEAREST` for desired positions;
- required order-kind-specific cost rules: limit fills commission-only, market fills positive normal spread;
- added `cost_calculation_policy_hash`;
- exposed forecast arithmetic values alongside hashes and required scalar value `20.0` with the book-approximate scalar label;
- constrained EWMAC trend sign, trend-veto decision, and quantile range;
- added transition proof fields for one-hour lag, session transition, raw-symbol/session/date continuity, roll boundary, and overnight recompute policy;
- added PnL close-only price-source guard, multiplier value hash, and currency/FX policy/value/source fields with fail-closed pairing;
- required equality between trust-root and evidence-manifest active manifest hashes;
- constrained daily/hourly compatibility verdict and reason codes.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
GPT_P1_SCHEMA_HARDENING_MARKERS_PRESENT
S27_V2_REPLAY_SCAFFOLD_FILE_COUNT_REMAINS_19
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run under this authorization.

## Handoff Folder Note

The existing GPT handoff folder packet predates this local patch. It must be treated as superseded if a new external audit is requested.

## Next Gate

The next step is a local hostile audit of the GPT P1 schema-hardening patch if the operator authorizes it.

Recommended authorization text:

```text
Operator authorizes local hostile audit of S27_V2 replay scaffold GPT P1 schema-hardening patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

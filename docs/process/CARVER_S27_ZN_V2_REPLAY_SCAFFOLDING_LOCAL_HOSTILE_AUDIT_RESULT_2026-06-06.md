# S27 ZN V2 Replay Scaffolding Local Hostile Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLDING_LOCAL_HOSTILE_AUDIT_RESULT_NOT_PATCH_OR_REPLAY_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes local hostile audit of S27_V2 replay schema/code scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This audit performed static code/process inspection only. It authorized and performed no code patches, no Python import/compile/test execution, no parser execution, no file replay, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Audit Method

Audit method:

```text
LOCAL_STATIC_HOSTILE_AUDIT_WITH_SUBAGENT_REVIEW
```

Inspected scope:

```text
src/carver/spine/s27_v2_replay/
docs/process/CARVER_S27_ZN_V2_LOCAL_ROW_REPLAY_IMPLEMENTATION_PLAN_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_NON_FORGEABLE_REPLAY_PROVENANCE_DESIGN_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_REPLAY_SCHEMA_CODE_SCAFFOLDING_RECORD_2026-06-06.md
```

## Verdict

```text
P0: none
P1: present
P2: present
P3: no accidental execution authorization found
```

## P0 Findings

No P0 found.

The scaffold remains isolated from:

```text
src/carver/spine/s27_v2.py
```

Static text inspection found no provider/API/download, parser/file replay execution, diagnostic/backtest entry point, subprocess/CLI, Git, adapter, deployment, trading, or promotion surface in:

```text
src/carver/spine/s27_v2_replay/
```

The runner-facing function:

```text
build_trusted_replay_bundle
```

fails closed by raising:

```text
ReplayExecutionBlocked
```

## P1 Findings

### P1: Forecast Schema Is Too Opaque

The approved implementation plan requires the forecast payload to expose EWMA5, raw mean-reversion forecast, sigma bridge, trend veto, V/Q/M, post-veto-times-M-before-scalar, scalar, cap, and desired-position fields.

Current scaffold:

```text
src/carver/spine/s27_v2_replay/forecast.py
```

only carries:

```text
forecast_payload_hash
scalar_label
forecast_hash
```

This reintroduces an opaque forecast payload risk that the trust-root design explicitly closed.

### P1: Source-Universe Schema Is Too Thin

The approved plan requires daily, hourly, session, roll, and cost universes; inclusion/exclusion reasons; duplicate policy; missing-row proof; repair/rejection proof; and canonical row-locator serialization.

Current scaffold:

```text
src/carver/spine/s27_v2_replay/source_universe.py
```

has core hashes, requested bounds, instrument universe, and raw-symbol universe, but lacks explicit hashes/fields for daily/hourly/session/roll/cost universes and reason/duplicate/canonical locator schemas.

### P1: Daily/Hourly Compatibility Schema Is Missing Explicit Proof Fields

The accepted design requires raw symbols for the current-contract and hourly rows plus explicit proofs for:

- sigma bridge;
- same raw-symbol/current price level;
- bridged daily continuous equilibrium.

Current scaffold:

```text
src/carver/spine/s27_v2_replay/level_compatibility.py
```

has row hashes and bridge hashes, but not explicit raw-symbol fields or separate proof hashes for same-level and bridged-equilibrium checks.

### P1: Cost Schema Omits Multiplier/Currency Conversion And Deflation Policy Fields

The approved plan requires multiplier/currency conversion and deflation policy where applicable.

Current scaffold:

```text
src/carver/spine/s27_v2_replay/costs.py
```

includes commission, spread, total amount/currency, and fill/order binding, but lacks explicit multiplier conversion, currency conversion, and deflation-policy fields.

## P2 Findings

### P2: Package Exports Are Incomplete

The modules exist, but:

```text
src/carver/spine/s27_v2_replay/__init__.py
```

does not export these key scaffold types:

```text
RuntimeHistoryLedgerRow
CostLedgerRow
SpreadSpace
TrustedReplayBundleScaffold
```

This is not an execution-risk P1, but it leaves the public scaffold surface incomplete.

## Next Gate

The next step is a narrow patch authorization for the audit findings only.

Recommended authorization text:

```text
Operator authorizes S27_V2 replay scaffolding audit-finding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

Patch scope should be limited to:

- expand `forecast.py` to expose required non-opaque forecast fields;
- expand `source_universe.py` to include the missing universe/reason/duplicate/canonical locator fields;
- expand `level_compatibility.py` to include raw symbols and separate proof hashes;
- expand `costs.py` to include multiplier/currency conversion and deflation-policy fields;
- export missing scaffold types from `__init__.py`;
- update the scaffolding record after patching.

No patch is authorized by this audit result.

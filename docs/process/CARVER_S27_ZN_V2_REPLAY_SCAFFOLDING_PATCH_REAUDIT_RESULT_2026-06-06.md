# S27 ZN V2 Replay Scaffolding Patch Re-Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLDING_PATCH_REAUDIT_RESULT_NOT_PATCH_OR_REPLAY_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes local hostile re-audit of S27_V2 replay scaffolding audit-finding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This re-audit performed static code/process inspection only. It authorized and performed no code patches, no Python import/compile/test execution, no parser execution, no file replay, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Audit Method

Audit method:

```text
LOCAL_STATIC_HOSTILE_REAUDIT_WITH_SUBAGENT_REVIEW
```

Inspected scope:

```text
src/carver/spine/s27_v2_replay/forecast.py
src/carver/spine/s27_v2_replay/source_universe.py
src/carver/spine/s27_v2_replay/level_compatibility.py
src/carver/spine/s27_v2_replay/costs.py
src/carver/spine/s27_v2_replay/__init__.py
src/carver/spine/s27_v2_replay/runner.py
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_AUDIT_FINDING_PATCH_RECORD_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_REPLAY_SCHEMA_CODE_SCAFFOLDING_RECORD_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_TRUST_ROOT_DESIGN_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_2026-06-06.md
```

## Verdict

```text
P0: none
P1: present
P2: none open from prior audit
P3: substantial patch progress confirmed
```

## P0 Findings

No P0 found.

The runner-facing function remains fail-closed:

```text
src/carver/spine/s27_v2_replay/runner.py
build_trusted_replay_bundle
ReplayExecutionBlocked
```

Static inspection found no provider/API/download, parser/file replay execution, diagnostic/backtest entry point, subprocess/CLI, Git, adapter, deployment, trading, or promotion surface in the inspected patch files.

## P1 Findings

### P1: Cost Schema Patch Only Partially Closes The Prior Cost Finding

File:

```text
src/carver/spine/s27_v2_replay/costs.py
```

The patch added multiplier, currency-conversion, and deflation-policy fields, but those fields remain optional and are only validated if present.

The remaining schema risk is:

- positive spread in `PRICE_SPACE` does not require contract multiplier evidence;
- `spread_space` presence is required for positive spread, but enum membership/type is not explicitly validated;
- the scaffold can therefore still represent price-space spread cost without proving the conversion basis needed by the source-faithful cost ledger.

This means the prior cost-schema P1 is partially closed but not fully closed.

## P2 Findings

No open P2 from the prior audit.

The prior package export gap is closed for:

```text
RuntimeHistoryLedgerRow
CostLedgerRow
SpreadSpace
TrustedReplayBundleScaffold
```

## P3 Findings

The other prior P1 findings appear closed at schema level:

- forecast opacity is closed by explicit forecast-path hashes;
- source-universe thinness is closed by explicit daily/hourly/session/roll/cost/reason/duplicate/canonical-locator fields;
- daily/hourly compatibility proof thinness is closed by explicit raw-symbol and proof fields.

## Next Gate

The next step is a narrow cost-schema patch authorization only.

Recommended authorization text:

```text
Operator authorizes S27_V2 replay scaffolding cost-schema re-audit finding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

Patch scope should be limited to:

- require explicit `SpreadSpace` membership validation;
- require multiplier value/source evidence when a positive spread is recorded in `PRICE_SPACE`;
- preserve optional currency conversion only when currency conversion is genuinely applicable, but keep value/source pairing fail-closed;
- update the process record after patching.

No patch is authorized by this re-audit result.

# S27 ZN V2 Replay Scaffold GPT P1 Schema Hardening Local Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_SCHEMA_HARDENING_LOCAL_AUDIT_RESULT_NOT_PATCH_OR_REPLAY_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes local hostile audit of S27_V2 replay scaffold GPT P1 schema-hardening patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This audit performed static code/process inspection only. It authorized and performed no code patches, no Python import/compile/test execution, no parser execution, no file replay, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Audit Method

Audit method:

```text
LOCAL_STATIC_HOSTILE_AUDIT_WITH_SUBAGENT_REVIEW
```

Audited source finding:

```text
docs/process/CARVER_S27_ZN_V2_GPT_REPLAY_SCAFFOLD_PATCHED_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

Audited patch record:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_SCHEMA_HARDENING_PATCH_RECORD_2026-06-06.md
```

## Verdict

```text
P0: none
P1: present
P2: present
P3: most GPT P1 categories closed at static schema level
```

## P0 Findings

No P0 found.

The runner-facing function remains fail-closed:

```text
src/carver/spine/s27_v2_replay/runner.py
build_trusted_replay_bundle
ReplayExecutionBlocked
```

Static inspection found no provider/API/download, parser/file replay execution, diagnostic/backtest entry point, subprocess/CLI, Git, adapter, deployment, trading, or promotion surface in the inspected scaffold package.

## P1 Findings

### P1: Cost Arithmetic Binding Still Under-Constrained

File:

```text
src/carver/spine/s27_v2_replay/costs.py
```

GPT required cost calculation binding so commission, spread, and total cost are not mutually arbitrary.

The patch added and validates:

```text
cost_calculation_policy_hash
```

but the row still does not cross-check:

- `commission_amount` against `commission_per_contract * fill.quantity`;
- `total_cost_amount` against `commission_amount + spread_amount`;
- spread and total amount consistency for both limit and market rows.

Therefore the GPT P1 cost-arithmetic finding is only partially closed and remains P1.

## P2 Findings

### P2: Transition Optional Fields Are Not Fully Exclusive By Transition Kind

File:

```text
src/carver/spine/s27_v2_replay/transitions.py
```

The patch rejects roll/overnight hashes on `NORMAL_ONE_HOUR_LAG`, but does not reject:

- `roll_boundary_row_hash` on `EOD_OVERNIGHT_RECOMPUTE`;
- `overnight_recomputed_target_policy_hash` on `ROLL_BOUNDARY`.

This is not the remaining P1 blocker, but exact transition-kind schemas should fail closed on non-applicable optional fields.

## P3 Findings

The remaining GPT P1 categories appear closed at static schema level:

- order side/kind validation and adjacent limit logic;
- fill enum/provenance checks;
- `NEAREST` rounding;
- scalar value `20.0`;
- trust-root/evidence-manifest equality;
- source-row schemas and ISO date checks;
- PnL close-only/multiplier/currency field additions;
- forecast value fields;
- compatibility exact verdict/reason labels.

Python import/compile/test execution was intentionally not run under this authorization, so syntax/import assurance remains unproven.

## Next Gate

The next step is a narrow cost-arithmetic binding patch, optionally including transition optional-field exclusivity, if the operator authorizes it.

Recommended authorization text:

```text
Operator authorizes S27_V2 replay scaffold cost-arithmetic binding patch and transition optional-field exclusivity patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

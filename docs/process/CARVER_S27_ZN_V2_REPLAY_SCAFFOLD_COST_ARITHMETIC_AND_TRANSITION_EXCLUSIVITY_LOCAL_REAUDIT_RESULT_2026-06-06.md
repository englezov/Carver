# S27 ZN V2 Replay Scaffold Cost Arithmetic And Transition Exclusivity Local Re-Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_COST_ARITHMETIC_AND_TRANSITION_EXCLUSIVITY_LOCAL_REAUDIT_RESULT_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes local hostile re-audit of S27_V2 replay scaffold cost-arithmetic binding and transition optional-field exclusivity patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a local hostile re-audit only. It authorizes and performed no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Method

Static inspection only:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Reviewed files:

```text
src/carver/spine/s27_v2_replay/costs.py
src/carver/spine/s27_v2_replay/transitions.py
src/carver/spine/s27_v2_replay/fills.py
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_COST_ARITHMETIC_AND_TRANSITION_EXCLUSIVITY_PATCH_RECORD_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_REPLAY_SCHEMA_CODE_SCAFFOLDING_RECORD_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_TRUST_ROOT_DESIGN_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_2026-06-06.md
```

Independent subagent hostile audit was used as a parallel read-only reviewer. The subagent made no edits and ran no Python/import/compile/tests/replay.

Package file count remained:

```text
19
```

Forbidden-surface text scan found no matches for provider/API/download/backtest/diagnostic/subprocess/CLI/file-open/Git surfaces in the replay scaffold package.

## Verdict

```text
NOT_PASSED_YET
```

P0:

```text
NONE_FOUND
```

P1:

```text
P1_PRICE_SPACE_SPREAD_COST_NOT_ARITHMETICALLY_BOUND_TO_NUMERIC_MULTIPLIER_AND_FILL_QUANTITY
```

The patch now binds:

- `commission_amount == commission_per_contract * fill.quantity`;
- limit fills to zero `spread_amount` and zero `spread_cost_amount`;
- market fills to positive `spread_amount` and positive `spread_cost_amount`;
- `CURRENCY_SPACE` spread cost to `spread_amount`;
- `total_cost_amount == commission_amount + spread_cost_amount`.

However, `PRICE_SPACE` spread cost remains provenance-bound rather than arithmetic-bound. The row requires multiplier proof hashes, but it does not carry a numeric multiplier value or equivalent arithmetic commitment that validates:

```text
spread_cost_amount == spread_amount * contract_multiplier_value * fill.quantity
```

or another source-locked equivalent.

As written, a `PRICE_SPACE` market fill can carry an arbitrary positive `spread_cost_amount` if multiplier hashes are present and total cost equals commission plus that arbitrary spread cost. This leaves the cost-arithmetic binding finding partially open.

P2:

```text
NONE_FOUND
```

Transition optional-field exclusivity appears closed in the narrow static scope:

- `NORMAL_ONE_HOUR_LAG` rejects roll-boundary and overnight policy hashes;
- `EOD_OVERNIGHT_RECOMPUTE` rejects roll-boundary hash and requires overnight recomputed-target policy hash;
- `ROLL_BOUNDARY` rejects overnight recompute policy hash and requires roll-boundary hash.

P3:

```text
PROCESS_DOCS_UPDATED_BY_THIS_RECORD_ONLY
```

## Next Gate

The next step is a narrow patch of the remaining P1 price-space spread-cost arithmetic binding if separately authorized.

Recommended authorization text:

```text
Operator authorizes S27_V2 replay scaffold price-space spread-cost arithmetic binding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This re-audit does not authorize an external GPT packet, parser/file replay implementation, local-row parser work, diagnostics, backtests, data access, Git actions, adapter work, deployment, trading, promotion, or result interpretation.

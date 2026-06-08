# S27 ZN V2 Replay Scaffold Price-Space Spread-Cost Arithmetic Binding Local Re-Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_PRICE_SPACE_SPREAD_COST_ARITHMETIC_BINDING_LOCAL_REAUDIT_RESULT_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Standing local hostile-audit rule applied:

```text
Local hostile audits are pre-approved.
```

Audit boundary preserved:

```text
S27_V2 replay scaffold price-space spread-cost arithmetic binding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a local hostile re-audit only. It authorizes and performed no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git staging/commit/push/PR action, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Method

Static inspection only:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Reviewed files:

```text
src/carver/spine/s27_v2_replay/costs.py
src/carver/spine/s27_v2_replay/fills.py
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_PRICE_SPACE_SPREAD_COST_ARITHMETIC_BINDING_PATCH_RECORD_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_COST_ARITHMETIC_AND_TRANSITION_EXCLUSIVITY_LOCAL_REAUDIT_RESULT_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_REPLAY_SCHEMA_CODE_SCAFFOLDING_RECORD_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_TRUST_ROOT_DESIGN_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_2026-06-06.md
```

Independent subagent hostile audit was used as a parallel read-only reviewer. The subagent made no edits and reported no parser/file replay execution, Python import/compile/tests, diagnostics, backtests, provider/API calls, downloads, OOS/Lockbox/Forward access, adapter work, deployment, trading, promotion, or result interpretation.

Process note:

```text
SUBAGENT_REPORTED_ONE_INADVERTENT_READ_ONLY_GIT_DIFF_DESPITE_NO_GIT_ACTION_BOUNDARY
```

This was recorded as a process deviation. No Git staging, commit, push, PR, checkout, reset, branch, or destructive Git action was performed.

Package file count remained:

```text
19
```

Source-code forbidden-surface text scan found no matches for provider/API/download/backtest/diagnostic/subprocess/CLI/file-open/Git surfaces in the replay scaffold package.

## Verdict

```text
SCOPED_P1_CLOSED_WITH_REMAINING_P2_OPTIONAL_FIELD_EXCLUSIVITY_FINDING
```

P0:

```text
NONE_FOUND
```

P1:

```text
NONE_FOUND
```

The prior P1 is closed. `PRICE_SPACE` rows now require:

- positive numeric `contract_multiplier_value`;
- `contract_multiplier_value_hash`;
- `contract_multiplier_source_hash`;
- `spread_cost_amount == spread_amount * contract_multiplier_value * fill.quantity`.

P2:

```text
P2_LIMIT_COST_ROW_OPTIONAL_COST_FIELDS_NOT_FULLY_EXCLUSIVE
```

`LIMIT` cost rows are forced to zero `spread_amount` and zero `spread_cost_amount`, and they reject `spread_policy_hash`, `spread_unit`, and `spread_space`.

However, `LIMIT` rows may still carry irrelevant optional cost fields:

```text
contract_multiplier_value
contract_multiplier_value_hash
contract_multiplier_source_hash
currency_conversion_value_hash
currency_conversion_source_hash
deflation_policy_hash
```

Those fields are shape-validated later if present, but the commission-only `LIMIT` branch does not reject them. This does not reopen the closed price-space arithmetic P1, but it can leave stale or misleading optional provenance on commission-only rows.

P3:

```text
P3_SUBAGENT_READ_ONLY_GIT_DIFF_BOUNDARY_DEVIATION_RECORDED
```

The parent audit did not run Git commands. The subagent reported one inadvertent read-only `git diff` despite the no-Git boundary. No Git state change occurred.

## Next Gate

The next step is a narrow patch of the remaining P2 `LIMIT` cost-row optional-field exclusivity issue if the operator authorizes code changes.

Recommended authorization text:

```text
Operator authorizes S27_V2 replay scaffold LIMIT cost-row optional-field exclusivity patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

Local hostile re-audits remain pre-approved under the project hostile-audit rule. Code patches, parser/file replay, diagnostics, backtests, data access, Git actions, adapter work, deployment, trading, promotion, and result interpretation still require their own proper gates.

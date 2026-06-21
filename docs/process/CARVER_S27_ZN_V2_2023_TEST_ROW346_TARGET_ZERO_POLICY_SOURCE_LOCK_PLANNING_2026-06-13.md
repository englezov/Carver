# S27_V2 2023 TEST Row-346 Target-Zero Policy Source-Lock Planning

Date: 2026-06-13

## Scope

This record covers the local-only target-position-zero adjacent-limit policy/source-lock and implementation-planning gate after local PASS on the 2023 TEST continuation to row 346.

Scope is limited to row 346 / the target-position-zero class:

```text
raw_symbol = ZNH3
decision_timestamp_utc = 2023-01-24T19:00:00Z
starting_position_contracts = 1
desired_position_contracts = 0
position_change_contracts = -1
order_side = SELL
adjacent_target_position = 0
current fail-closed reason = FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_TARGET_POSITION_ZERO_NOT_RESULT
```

This gate used current S27_V2 code/tests/process records, already-recorded Carver/source-lock execution notes, and already-local 2023 TEST artifacts only. It did not use provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, broader TEST continuation, result interpretation, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.

## Evidence Reviewed

The earlier source-lock remediation record `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_TARGET_POSITION_REMEDIATION_2026-06-06.md` states that S27 trend permission is target-position/sign based, not raw order-side based, and records:

```text
target 0 is allowed for either nonzero trend direction
positive target positions require positive EWMAC trend
negative target positions require negative EWMAC trend
adjacent limit generation now checks the post-fill target position
```

The cap-edge remediation record `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_CAP_EDGE_REMEDIATION_2026-06-06.md` records the bounded target-zero cases explicitly:

```text
uptrend current_position=1, base_position_contracts=1, target 0 emits sell-to-flat
downtrend current_position=-1, base_position_contracts=1, target 0 emits buy-to-flat
```

The active primitive implementation in `src/carver/spine/s27_v2.py` matches that policy:

```text
_target_position_allowed_by_trend(target_position=0, nonzero_trend) returns True
implied_price_for_target_position(...) computes target_capped_forecast from the target position
target_position=0 implies target_capped_forecast=0 and an implied limit at equilibrium_ewma5
```

The local-row replay runners have not fully carried this source-lock forward:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py::_formula_limit
```

currently returns `None` when `target_position <= 0`, which incorrectly blocks a source-locked sell-to-flat target-zero exit.

The older development/reconciliation runner also has a stale guard:

```text
src/carver/spine/s27_v2_replay/development_recon_run.py::_formula_implied_limit_price
```

raises on `adjacent_target_position == 0`. That stale guard explains why the local-row surfaces still treat target zero as unsupported even though the synthetic primitive source-lock was remediated earlier.

Structural order validation in `src/carver/spine/s27_v2_replay/orders.py` does not forbid target position zero. It requires an adjacent one-lot order whose side and target agree with the current position. A `SELL 1` from current position `1` to target position `0` is structurally valid.

## Planning Decision

Decision:

```text
ROW346_TARGET_ZERO_EXIT_SOURCE_LOCKED_FOR_TARGET_PERMISSION_PENDING_TEST_RUNNER_IMPLEMENTATION_NOT_RESULT
```

The row-346 blocker is not a new unsupported strategy rule. Existing source-lock/process evidence supports target position zero as a valid target-position permission class for nonzero trend, including sell-to-flat and buy-to-flat adjacent exits.

The current TEST runner is stale for this class because it rejects all `target_position <= 0` before applying the source-locked target-position permission rule.

Row 346 must remain stopped until a separate implementation gate patches the TEST mechanical runner to carry forward the source-locked target-zero logic and verifies that the patch is bounded. This planning gate does not itself authorize code changes, TEST continuation, order/fill/cost/PnL/result interpretation, GPT packet preparation, Git actions, or source-faithful evidence claims.

## Required Implementation Boundary

The next implementation gate should be limited to row 346 / target-zero adjacent-limit behavior and should require:

- active TEST input-pack/run artifact binding;
- existing row-346 facts exactly matching `ZNH3`, decision `2023-01-24T19:00:00Z`, current position `1`, desired position `0`, position change `SELL 1`, adjacent target `0`;
- nonzero trend permission for target position zero;
- formula-implied target-zero limit price derived from the source-locked implied-price inversion, not an ad hoc exit price;
- conservative ZN SELL tick rounding;
- same-session/no-roll/no-degraded-provider proof;
- no market-order fallback for this one-lot adjacent class;
- limit fill/cost/mechanical PnL metadata only if the already-local fill-candidate, cost, and valuation evidence are sufficient;
- result/backtest/source-faithful evidence gates remaining fail-closed;
- regression tests that reject forged target-zero rows, wrong-side target-zero rows, stale formula-limit rows, forged fill/transition/cost/PnL fields, and downstream result/source-faithful evidence flags.

## Proposed Next Authorization

```text
Operator authorizes S27_V2 2023 TEST row-346 target-position-zero adjacent-limit implementation gate, after the row-346 policy/source-lock planning gate, limited to already-local 2023 TEST artifacts and the audited S27_V2 machinery.

This authorizes Codex to patch the stale TEST mechanical runner target-zero guard so it carries forward the already source-locked S27_V2 target-position permission rule: target position 0 is allowed for either nonzero trend direction, and row 346 may emit a bounded SELL 1 adjacent limit toward flat only if all exact row-346 facts match.

Scope is limited to row 346 / the target-position-zero class: ZNH3, decision 2023-01-24T19:00:00Z, starting position 1, desired position 0, position change SELL 1, adjacent target 0, nonzero positive trend, same-session/no-roll/no-degraded-provider evidence, formula-implied target-zero limit price from source-locked implied-price inversion, conservative ZN SELL tick rounding, and deterministic local-only order/fill/cost/mechanical-PnL metadata where existing evidence is sufficient.

This authorizes focused tests, one local hostile audit with subagents, process/current-state records, and continuation only until the next genuine fail-closed blocker.

No provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If row facts drift, target-zero permission cannot be bounded to the already source-locked rule, fill/cost/valuation evidence is insufficient, or implementation requires provider/API/download/new data/protected-window access/Git/adapter/deployment/trading/promotion, Codex must fail closed and ask the operator.
```

## Non-Authorizations

This record does not authorize:

- provider/API access;
- downloads;
- new data acquisition;
- broader TEST continuation beyond row 346;
- VALIDATION;
- OOS;
- Lockbox;
- Forward;
- result interpretation;
- PnL evaluation beyond mechanical construction;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git staging, commit, push, or PR;
- GPT packet preparation;
- source-faithful evidence claims.

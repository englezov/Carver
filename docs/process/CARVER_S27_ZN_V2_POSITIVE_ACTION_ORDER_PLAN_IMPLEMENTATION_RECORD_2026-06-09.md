# S27 V2 Positive-Action Order-Plan Implementation Record

Date: 2026-06-09

Status:

```text
LOCAL_POSITIVE_ACTION_LIMIT_ORDER_PLAN_IMPLEMENTED_NOT_FILL_NOT_COST_NOT_PNL_NOT_RESULT
```

## Authorization

Operator authorized the `S27_V2 local-only positive-action limit-order policy source-lock and executable order-plan gate` after external PASS on the positive-action executable packet and completion of the execution-policy planning gate.

Scope was limited to the audited `ZNM6` positive-action row at:

```text
decision_timestamp_utc = 2026-04-13T13:00:00Z
fill_candidate_timestamp_utc = 2026-04-13T14:00:00Z
```

## Non-Authorization

This implementation authorizes no provider/API access, no downloads, no new data acquisition, no OOS, no Lockbox, no Forward, no backtests, no result-scored runs, no actual fill emission, no actual cost emission, no actual PnL/result emission, no result interpretation, no PnL evaluation, no tuning, no adapter work, no deployment, no trading, no promotion, no Git actions, and no source-faithful evidence claim.

## Files Added

- `src/carver/spine/s27_v2_replay/positive_action_order_plan_executable.py`
- `tests/test_s27_v2_positive_action_order_plan_executable.py`

The package root export list was not expanded. This avoids creating a package-root authority leak.

## Implemented Surface

The builder:

```text
build_positive_action_limit_order_plan(...)
```

is locked to:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack
```

It rebuilds and validates the active positive-action bundle before accepting any order-plan row. Standalone row validation is fail-closed.

## Emitted Local-Only Metadata

The bundle emits:

- one positive-action limit-order row;
- one normal same-session transition-planning metadata row;
- validation/provenance/trusted-bundle metadata flags.

The bundle does not emit:

- market-order rows;
- fill rows;
- cost rows;
- PnL rows;
- result rows;
- backtest/result-scored rows;
- source-faithful evidence claims.

## Active Order Plan

```text
current_position = 0
target_position_after_fill = -1
position_change = -1
order_kind = LIMIT
order_side = SELL
order_quantity = 1
formula_implied_limit_price = 111.03763969794181
executable_tick_limit_price = 111.046875
tick_size = 0.015625
tick_rounding_direction = ROUND_UP_TO_NEAREST_ZN_TICK_FOR_SELL_LIMIT
```

The executable sell limit is rounded up to the nearest ZN tick under:

```text
LOCAL_ONLY_CONSERVATIVE_ZN_LIMIT_ROUNDING_BUY_DOWN_SELL_UP_TO_EXECUTABLE_TICK
```

This keeps the executable sell limit at or above the formula-implied price, so the local dev/recon executable price does not improve the fill condition relative to the formula price.

## Evidence Bound

The implementation binds:

- active positive-action bundle hash and row hash;
- positive-action manifest SHA256;
- Appendix C/static ZN row and file SHA256;
- ZN point value `1000`, tick size `0.015625`, tick value `15.625`, and USD currency;
- active prior `ZNM6` provider definition row and file SHA256;
- explicit rejection of provider `contract_multiplier = 2147483647` as point-value authority;
- first-row flat/empty working-state hash;
- no-market proof for one-contract, priceable, non-cap adjacent target;
- session row proof for same-session decision/fill-candidate timestamps;
- roll row proof that the selected date is not a roll boundary;
- next completed hourly fill-candidate row hash as transition-planning metadata only.

## Hashes

```text
bundle_hash = f027de8af3536a22fa9ae3f6a58a63086eea3708e334b26612e6c7b4729320cd
limit_row_hash = b381c3b797db313e2e00e5f0d5b854b15f7054fae0a3280165aef668e3f731fc
order_plan_hash = 57d25dc2df281c9ebc2525c6c2bca8ca8b4b006226fb9a7605360ae0bc4a02a4
limit_order_hash = 13a6346e3b047b132a7376f1af960ff279462fb82990f7b657ab68eaa1b0346e
transition_row_hash = 37074b3319ded3315450d656942c1022e135312de538cad493688e4f66400160
session_proof_hash = 6cb7601cc0a4b02c53821d4d66afefaf533616f054ef906f12cd3707258d9103
roll_proof_hash = bed07241975e57a395f07ff3918f9f659e5d524c3caa5b00a844ae3ce6aa0a9e
```

## Verification

Focused local verification passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\positive_action_order_plan_executable.py
python -m pytest tests\test_s27_v2_positive_action_order_plan_executable.py -q
33 passed
python -m pytest tests\test_s27_v2_positive_action_executable.py tests\test_s27_v2_positive_action_order_plan_executable.py -q
76 passed
```

Tests cover:

- active positive-action bundle binding;
- formula-implied price arithmetic;
- conservative sell-limit tick rounding;
- static ZN tick/point-value evidence binding;
- provider multiplier sentinel rejection;
- same-session transition-planning proof;
- no-roll-boundary proof;
- standalone row non-authority;
- self-consistent row/bundle forgery rejection;
- forbidden market/fill/cost/PnL/result/source-faithful evidence flags.

## Remaining Gates

Actual fill emission remains blocked until separately authorized and audited. The next gate should decide whether to construct the one-hour close-only fill decision for this already-emitted `SELL 1` limit, or fail closed if the submitted executable limit price is not crossed by the next completed hourly close.

Actual cost, PnL, result, backtest, result interpretation, PnL evaluation, tuning, adapter/deployment/trading/promotion, Git actions, and source-faithful evidence claims remain unauthorized.

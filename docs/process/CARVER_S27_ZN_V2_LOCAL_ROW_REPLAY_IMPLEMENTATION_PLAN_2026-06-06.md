# S27 ZN V2 Local-Row Replay Implementation Plan

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_LOCAL_ROW_REPLAY_IMPLEMENTATION_PLAN_NOT_CODE_OR_REPLAY_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 local-row replay implementation planning artifact only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This artifact is a process-only implementation plan. It authorizes no code changes, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Governing Inputs

The future implementation must satisfy these active artifacts:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_NON_FORGEABLE_REPLAY_PROVENANCE_DESIGN_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_GPT_TRUST_ROOT_DESIGN_FINAL_NARROW_REAUDIT_SYNTHESIS_2026-06-06.md
```

Planning-ready state:

```text
S27_ZN_V2_TRUST_ROOT_PROVENANCE_DESIGN_PLANNING_READY_ONLY
```

## Future Public Boundary

The future source-faithful public boundary must be one replay-owned output:

```text
S27_V2_TRUSTED_REPLAY_BUNDLE
```

Low-level helpers may exist only as internal structural primitives. They must not be treated as source-faithful evidence unless called inside the trusted replay bundle and bound to the active replay trust root.

## Future Package Shape

A future implementation should be isolated from old S27 diagnostic runners and old target-position close-to-close PnL paths.

Recommended future module family:

```text
src/carver/spine/s27_v2_replay/
```

Recommended future internal modules:

```text
identity.py
canonical_hash.py
trust_root.py
source_universe.py
source_rows.py
level_compatibility.py
runtime_history.py
forecast.py
position.py
orders.py
transitions.py
fills.py
costs.py
pnl.py
evidence_manifest.py
validation.py
runner.py
```

This plan does not create those modules. Creating or editing code requires separate explicit operator authorization.

## Replay Identity Plan

Every future row emitted by the trusted runner must carry:

```text
replay_id
step_index
strategy_id = S27_V2_ZN
lane = SOURCE_NATIVE_FUTURES
instrument = ZN
raw_symbol
session_id
completed_trading_date
decision_as_of_utc
fill_as_of_utc
```

Every non-initial step must bind the previous trusted step hash. The initial step must bind an audited initial-state hash and initial-position policy.

Fail-closed status:

```text
BLOCKED_SOURCE_UNRESOLVED_INITIAL_POSITION_POLICY
```

## Canonical Serialization And Hash Plan

Future implementation must define canonical serialization before any row can be trusted:

- hash algorithm and version;
- field ordering;
- row ordering and collation;
- decimal normalization;
- finite-float rejection;
- timezone normalization to UTC;
- null/missing sentinel policy;
- string encoding;
- hash payload versioning.

Trust-root components:

```text
canonical_serialization_schema_hash
hash_algorithm_version_hash
decimal_float_normalization_policy_hash
timezone_normalization_policy_hash
row_ordering_collation_policy_hash
```

Fail-closed status:

```text
BLOCKED_SOURCE_UNRESOLVED_CANONICAL_SERIALIZATION_AND_HASH_POLICY
```

## Replay Trust Root Plan

The future runner must compute:

```text
replay_trust_root_hash
```

The trust root must bind the active source-lock, local data-contract gate, provenance design, runner implementation hash, parser/extractor source hash, dependency/runtime manifest, replay config, source universe manifest, raw file hashes, row locator hash, canonical serialization/hash policies, session/roll policies, tick/cost/multiplier/currency policies, daily/hourly compatibility policy, and active evidence manifest.

Externally supplied trusted-looking bundles, row hashes, statuses, dataclasses, or payloads are never authority.

Fail-closed status:

```text
BLOCKED_SOURCE_UNRESOLVED_NON_FORGEABLE_TRUST_ROOT
```

## Source Universe And Row Locator Plan

Before a future replay step is admissible, the runner must bind the complete local source universe for the requested run:

```text
source_universe_hash
raw_file_hash_set
row_locator_hash
strict_prior_candidate_set_hash
no_future_rows_proof_hash
missing_row_proof_hash
repair_rejection_proof_hash
```

The source universe must define:

- replay requested start/end bounds;
- ZN instrument universe;
- raw-symbol universe;
- daily row universe;
- hourly decision/fill row universe;
- session row universe;
- roll row universe;
- cost parameter row universe;
- inclusion/exclusion reason codes;
- duplicate policy;
- missing-row proof;
- repair/rejection proof;
- canonical row-locator serialization.

Fail-closed status:

```text
BLOCKED_SOURCE_UNRESOLVED_SOURCE_UNIVERSE_AND_ROW_LOCATOR_HASHES
```

## Source Input Manifest Plan

Every trusted step must emit:

```text
SOURCE_INPUT_MANIFEST
```

The manifest must bind daily completed rows, hourly decision/fill rows, raw symbols, session ids, provider/readiness status, row hashes, strict-prior proof, runtime-history proof, no-future-row proof, and daily/hourly level compatibility proof.

Open/high/low may be carried as row-integrity fields only. They are not fill or execution authority.

## Daily/Hourly Level Compatibility Plan

Every trusted step must emit:

```text
DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER
```

Required hashes:

```text
daily_hourly_level_compatibility_hash
sigma_bridge_level_source_hash
continuous_to_current_contract_level_bridge_hash
```

The ledger must prove that:

- daily continuous equilibrium input is on a compatible level with hourly current price after the locked bridge;
- sigma-price bridge uses the previous completed daily close of the currently traded contract;
- daily current-contract close and hourly current/fill rows share the same raw-symbol price level;
- raw symbols, row hashes, and bridge policy are explicit;
- compatibility verdict and reason code are deterministic.

Fail-closed status:

```text
BLOCKED_SOURCE_UNRESOLVED_DAILY_HOURLY_LEVEL_COMPATIBILITY_PROOF
```

## Runtime History Plan

Every trusted step must emit:

```text
RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM
```

Runtime history must recompute from admissible completed bars:

- EWMA5 equilibrium;
- EWMAC(16,64) trend value and sign;
- Strategy 3 annual percentage sigma;
- ten-year rolling mean of current percentage sigma where available;
- V;
- expanding/admissible historical quantile Q;
- raw volatility multiplier;
- EWMA10-smoothed M.

Required hashes:

```text
runtime_history_hash
EWMA5_state_hash
EWMAC16_64_state_hash
sigma_estimator_state_hash
VQM_history_hash
```

Fail-closed statuses:

```text
BLOCKED_SOURCE_UNRESOLVED_FORECAST_HISTORY_STATE_HASHES
BLOCKED_SOURCE_UNRESOLVED_STRATEGY3_SIGMA_PROVENANCE
```

## Forecast And Desired Position Plan

Every trusted step must emit:

```text
FORECAST_REPLAY_LEDGER
DESIRED_POSITION_LEDGER
```

Forecast payload must expose:

- EWMA5 equilibrium;
- raw mean-reversion forecast;
- sigma bridge price;
- annual percentage sigma;
- sigma-price value;
- risk-adjusted forecast before trend veto;
- EWMAC(16,64) trend value/sign;
- trend-veto decision;
- risk-adjusted forecast after veto;
- V;
- Q;
- raw volatility multiplier;
- EWMA10 multiplier M;
- risk-adjusted forecast after veto times M before scalar;
- S27 scalar with label `BOOK_APPROXIMATE_SCALAR_IMPLEMENTATION_FROZEN_AT_20_0`;
- capped forecast;
- desired unrounded position;
- desired rounded position using nearest rounding.

Zero EWMAC trend, unsupported rounding, future daily rows, incompatible sigma source, or opaque forecast hashes fail closed.

## Order Plan

Every trusted step must emit:

```text
LIMIT_ORDER_LEDGER
MARKET_ORDER_LEDGER
```

Order plan must bind:

- current position from prior trusted step;
- desired rounded position;
- adjacent-position limit set;
- market-order trigger source condition where required;
- formula-implied limit price;
- executable tick price;
- side-specific tick rounding direction;
- tick policy hash or fail-closed tick status;
- order-plan hash.

Real-row replay must fail closed until the ZN tick-size and side-specific executable limit rounding policy are source-locked.

Fail-closed status:

```text
BLOCKED_SOURCE_UNRESOLVED_ZN_TICK_ROUNDING_POLICY
```

## Working State And Transition Plan

Every trusted step must emit:

```text
WORKING_ORDER_TRANSITION_LEDGER
REMAINING_LIMIT_ORDER_LEDGER
CANCELED_LIMIT_ORDER_LEDGER
```

Transitions must bind:

- starting working state;
- starting position;
- order-plan hash;
- previous step hash or initial-state hash;
- one-hour lag;
- unchanged raw symbol/session/trading date for normal transitions;
- explicit EOD/overnight/roll row facts for non-normal transitions;
- ending working state;
- ending position;
- transition hash.

Persistent working-limit lifecycle remains unresolved for multi-hour/day replay until source-locked:

```text
BLOCKED_SOURCE_UNRESOLVED_WORKING_LIMIT_LIFECYCLE
```

Overnight recompute and nonzero roll bridge remain fail-closed:

```text
BLOCKED_SOURCE_UNRESOLVED_OVERNIGHT_RECOMPUTED_TARGET
BLOCKED_SOURCE_UNRESOLVED_NONZERO_ROLL_BRIDGE
```

## Fill Plan

Every trusted step must emit:

```text
FILL_LEDGER
```

Fill rows must bind:

- filled order hash;
- limit-order hash or market-order hash;
- fill decision source row hash;
- submitted limit price for limit orders;
- market-order trigger hash for market orders;
- fill condition hash;
- fill price provenance;
- order kind;
- side;
- quantity;
- fill hash.

Limit fills use the submitted executable limit price from the filled order row when the next completed close crosses the limit under the locked one-hour-lag primitive. Market fills use the next completed close under the locked market-order primitive.

## Cost Plan

Every trusted step with fills must emit:

```text
COMMISSION_LEDGER
SPREAD_COST_LEDGER
```

Trusted cost rows must bind:

- fill hash;
- order kind;
- side;
- quantity;
- commission policy hash;
- commission per contract;
- commission unit `PER_CONTRACT`;
- commission currency;
- commission amount;
- spread policy hash where applicable;
- spread unit and amount where applicable;
- spread space as `PRICE_SPACE` or `CURRENCY_SPACE`;
- multiplier/currency conversion where applicable;
- deflation policy where applicable;
- total cost amount;
- total cost currency;
- cost hash.

Cost treatment remains:

```text
LIMIT_ORDER_FILL_COST = COMMISSION_ONLY
MARKET_ORDER_FILL_COST = COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD
ALL_ORDERS_PAY_COMMISSION
```

Fail-closed status:

```text
BLOCKED_SOURCE_UNRESOLVED_TRUSTED_COST_ROW_AMOUNT_UNIT_SCHEMA
```

## PnL Plan

Every trusted step must emit:

```text
PNL_LEDGER
```

PnL rows must bind:

- replay trust root hash;
- source universe hash;
- previous step hash or initial-state hash;
- starting and ending positions;
- starting and ending working-state hashes;
- transition hash;
- position source hash;
- PnL formula policy hash;
- price source kind `CLOSE_ONLY`;
- start/end price source row hashes;
- raw-symbol continuity proof or roll-bridge proof;
- contract multiplier value/source hash;
- currency value/source hash if applicable;
- cost application policy hash;
- fill hash set;
- cost hash set;
- PnL hash.

Close-to-close target-position shortcuts are diagnostic only and must not be accepted as source-faithful S27 V2 PnL.

## Evidence Manifest And Validation Plan

Every trusted run must emit:

```text
VALIDATION_LEDGER
PROVENANCE_AND_HASH_LEDGER
LOCAL_HOSTILE_AUDIT_RESULT
```

The active evidence manifest must bind:

- artifact type;
- file path;
- content hash;
- status label;
- active source lock;
- active data contract;
- active provenance design;
- active implementation hash;
- active test/audit evidence hashes;
- superseded artifacts;
- supersession reason;
- superseding artifact hash;
- effective date/time.

Fail-closed status:

```text
BLOCKED_SOURCE_UNRESOLVED_STALE_EVIDENCE_SUPERSESSION_MANIFEST
```

## Future Implementation Sequence

Future code work, if separately authorized, should be staged in this order:

1. Define schema-only dataclasses and canonical serialization policy.
2. Define trust-root and evidence-manifest construction.
3. Define source-universe and row-locator validation.
4. Define daily/hourly compatibility ledger construction.
5. Define runtime history recomputation for EWMA5, EWMAC(16,64), Strategy 3 sigma, V/Q/M.
6. Define forecast and desired-position replay rows.
7. Define order-plan rows with tick rounding fail-closed until source-locked.
8. Define working-state and transition rows with unresolved lifecycle gates fail-closed.
9. Define fill rows.
10. Define cost rows.
11. Define PnL rows.
12. Define validation/provenance ledgers and local hostile-audit checks.

No implementation stage may silently borrow old diagnostic S27 runners, close-to-close target-position PnL, CFD assumptions, adapter code, provider/API code, or old contaminated pipeline state.

## Future Audit Checkpoints

Before any future parser/replay execution:

1. Local hostile audit of schema and trust-root code.
2. Local hostile audit of fail-closed paths for missing/degraded/duplicated/future rows.
3. Local hostile audit of daily/hourly level compatibility and sigma bridge.
4. Local hostile audit of forecast arithmetic and trend/vulnerability gates.
5. Local hostile audit of order/fill/cost/PnL provenance.
6. External audit packet after implementation artifacts exist.

## Next Required Authorization

The next step after this planning artifact is not automatically authorized.

If the operator wants code scaffolding, the next authorization must be separate and narrow, for example:

```text
Operator authorizes S27_V2 replay schema/code scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

That authorization would still not allow parser execution, file replay, diagnostics, backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, or result interpretation.

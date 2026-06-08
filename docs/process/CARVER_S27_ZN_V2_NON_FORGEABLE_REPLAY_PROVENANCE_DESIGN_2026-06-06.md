# Carver S27 ZN V2 Non-Forgeable Replay Provenance Design

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_V2_NON_FORGEABLE_REPLAY_PROVENANCE_DESIGN_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

## Scope

This artifact resolves the design direction after the GPT Extended Pro 54-test re-audit stop-rule decision.

It does not implement local-row replay. It defines the provenance boundary that any future S27 V2 ZN local-row replay implementation must satisfy before diagnostics, backtests, OOS, Lockbox, Forward, tuning, alpha claims, promotion, or deployment are considered.

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Non-authorization:

```text
NO_PROVIDER_API
NO_DOWNLOAD
NO_FILE_PARSING_OR_REPLAY_RUNNER_EXECUTION
NO_DIAGNOSTIC
NO_BACKTEST
NO_OOS_LOCKBOX_FORWARD
NO_GIT_STAGING_COMMIT_PUSH
```

## Background

The S27 V2 synthetic implementation slice has been hardened through repeated hostile audits. The latest local synthetic state is:

```text
python -m pytest tests\test_s27_v2_source_lock_synthetic.py -q
54 passed
```

The GPT 54-test re-audit found no P0 in the intended bundled replay path, but correctly identified that mutable dataclasses and public helpers cannot provide non-forgeable source provenance by themselves. The patch loop is therefore stopped by:

```text
STOP_SYNTHETIC_PUBLIC_BOUNDARY_PATCH_LOOP
MOVE_TO_NON_FORGEABLE_REPLAY_PROVENANCE_DESIGN
```

## Boundary Decision

The only future source-faithful execution boundary is:

```text
S27_V2_TRUSTED_REPLAY_BUNDLE
```

Low-level helpers are not source-faithful public APIs. They are structural/internal primitives unless called by a trusted replay bundle that has already bound source rows, hashes, sessions, raw symbols, forecast rows, order rows, fill rows, cost rows, and PnL rows into one replay lineage.

This means:

- `S27V2ForecastContext` is not proof of provenance by itself;
- `S27V2OrderPlan` is not proof of provenance by itself;
- `S27V2FillRow` is not proof of provenance by itself;
- `S27V2CostLedgerRow` is not proof of provenance by itself;
- `S27V2PnlLedgerRow` is not proof of provenance by itself;
- string source statuses are not non-forgeable provenance;
- any future public runner must expose only trusted replay-bundle outputs, not free-form helper outputs.

## Trusted Replay Bundle Contract

A trusted replay bundle must be produced from one bounded replay step at a time:

```text
source rows -> strict-prior daily runtime -> forecast -> desired position -> order plan -> working transition -> fills -> costs -> PnL -> validation/provenance rows
```

Every replay step must carry a single replay identity:

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

Every output row must carry that identity. If any row cannot be tied back to the same identity, the replay step fails closed.

## Non-Forgeable Provenance Requirement

Future implementation must replace mutable string-only provenance with deterministic replay-lineage proof bound to a replay trust root.

Deterministic hashes alone are not enough. Hashing forged payloads only makes forged payloads internally consistent. A trusted replay bundle is source-faithful only if every trusted row is recomputed by the trusted replay runner from local raw/source rows, locked source artifacts, locked code/config artifacts, and locked policy artifacts.

Imported trusted-looking bundles, externally supplied row hashes, externally supplied trusted dataclasses, and caller-supplied source statuses are never authority.

For this design, "non-forgeable" means non-forgeable relative to the active replay trust root and recomputed local source universe. It does not mean cryptographically impossible for a malicious operator to change raw files, parser code, runner code, policy artifacts, or the active trust-root declaration.

## Replay Trust Root

Every trusted replay run must start from a replay trust root:

```text
replay_trust_root_hash
```

The trust root must bind:

- active Carver source-lock artifact hash;
- active local data-contract artifact hash;
- active replay provenance design artifact hash;
- implementation source hash for the trusted replay runner;
- parser/extractor source hash;
- dependency/runtime hash or pinned environment manifest hash;
- replay config hash;
- source input universe manifest hash;
- raw source file hashes;
- source row locator hash;
- canonical serialization schema hash;
- hash algorithm/version hash;
- decimal/float normalization policy hash;
- timezone normalization policy hash;
- row ordering/collation policy hash;
- session calendar policy hash;
- roll calendar/policy hash;
- tick-size and limit-price rounding policy hash when unlocked;
- commission policy hash;
- spread-unit policy hash;
- contract multiplier/currency policy hash;
- daily/hourly level compatibility policy hash;
- stale-evidence supersession manifest hash.

If any trust-root component is missing, stale, contradictory, or caller-supplied rather than recomputed from local files/artifacts, the replay fails closed:

```text
BLOCKED_SOURCE_UNRESOLVED_NON_FORGEABLE_TRUST_ROOT
```

If canonical serialization, hash algorithm/version, decimal/float normalization, timezone normalization, or row ordering/collation policy is missing or not bound into the trust root:

```text
BLOCKED_SOURCE_UNRESOLVED_CANONICAL_SERIALIZATION_AND_HASH_POLICY
```

## Source Universe And Strict-Prior Proof

Each replay run must bind the complete admissible source universe for the run, not only the selected rows used in a step.

The run must compute:

```text
source_universe_hash
raw_file_hash_set
row_locator_hash
strict_prior_candidate_set_hash
no_future_rows_proof_hash
missing_row_proof_hash
repair_rejection_proof_hash
```

The strict-prior proof must show that the selected daily row is the latest admissible completed daily row before the hourly decision timestamp. It must also show that no later daily row, no incomplete bar, and no future row entered EWMA5, EWMAC, sigma, V/Q/M, forecast, desired position, order, fill, cost, or PnL computation.

The source-universe schema must explicitly define:

- replay requested start/end bounds;
- instrument universe and raw-symbol universe;
- daily row universe;
- hourly decision/fill row universe;
- session row universe;
- roll row universe;
- cost parameter row universe;
- row inclusion/exclusion reason codes;
- row ordering and duplicate policy;
- missing-row proof;
- repair/rejection proof;
- canonical row-locator serialization.

If the complete candidate set cannot be reconstructed from local source rows, the replay fails closed:

```text
BLOCKED_SOURCE_UNRESOLVED_SOURCE_UNIVERSE_AND_ROW_LOCATOR_HASHES
```

At minimum, each trusted step must compute:

```text
source_input_hash
source_universe_hash
strict_prior_candidate_set_hash
daily_runtime_hash
forecast_hash
desired_position_hash
order_plan_hash
working_state_hash
transition_hash
fill_hash
cost_hash
pnl_hash
step_bundle_hash
```

Hashes must be computed from canonical serialized row payloads, not from caller-supplied status strings alone.

The step bundle hash must include the ordered child hashes, the replay trust root hash, and the previous step hash or initial-state hash. A downstream row is trusted only if it can be recomputed from local inputs and verified against the same step bundle hash.

## Source Row Binding

The source input manifest for each step must bind:

- daily completed trading date;
- daily completed timestamp;
- daily continuous close;
- daily current traded contract close;
- annual percentage sigma value;
- annual percentage sigma source status;
- hourly completed bar end UTC;
- hourly completed trading date;
- hourly close used for decision;
- fill hourly completed bar end UTC;
- fill hourly completed trading date;
- fill close used for one-hour-lag fill;
- raw symbol before fill;
- raw symbol after fill;
- session id before fill;
- session id after fill;
- provider/readiness status;
- row hash for every source row.

Open/high/low may remain row-integrity fields only. They are not execution authority.

The source input manifest must also reference:

```text
source_universe_hash
strict_prior_candidate_set_hash
runtime_history_hash
no_future_rows_proof_hash
daily_hourly_level_compatibility_hash
sigma_bridge_level_source_hash
continuous_to_current_contract_level_bridge_hash
```

Those hashes prove row selection and admissible history, not merely the selected row payload.

## Daily/Hourly Level Compatibility Proof

S27 V2 mixes daily source rows and hourly source rows. A trusted replay must prove that the daily continuous price level used for EWMA5/equilibrium and the hourly current price level used for decisions/fills are compatible under a locked level bridge.

The compatibility proof must compute:

```text
daily_hourly_level_compatibility_hash
sigma_bridge_level_source_hash
continuous_to_current_contract_level_bridge_hash
```

The compatibility ledger schema must bind:

- daily continuous row hash;
- daily current traded contract row hash;
- previous completed daily close for the currently traded contract;
- hourly decision row hash;
- hourly fill-decision row hash;
- raw symbol used by the current traded contract row;
- raw symbol used by the hourly decision/fill rows;
- continuous adjustment or bridge policy hash;
- sigma-price bridge level source hash;
- proof that the sigma-price bridge uses the previous completed daily close of the currently traded contract;
- proof that the hourly current price and daily current-contract close are on the same raw-symbol price level;
- proof that the daily continuous equilibrium is bridged to the current traded contract level before comparison with hourly current price;
- compatibility verdict and reason code.

Open/high/low are not compatibility authority. If the daily continuous level, daily current-contract level, and hourly current level cannot be reconciled from local source rows and locked bridge policy, replay fails closed:

```text
BLOCKED_SOURCE_UNRESOLVED_DAILY_HOURLY_LEVEL_COMPATIBILITY_PROOF
```

## Runtime History State Binding

S27 V2 runtime rows must bind the full admissible history required to recompute:

- EWMA5 equilibrium;
- EWMAC(16,64) trend value and sign;
- Strategy 3 annual percentage sigma;
- ten-year rolling sigma average used for V;
- expanding quantile Q;
- raw volatility multiplier;
- EWMA10-smoothed M.

Each step must compute:

```text
runtime_history_hash
EWMA5_state_hash
EWMAC16_64_state_hash
sigma_estimator_state_hash
VQM_history_hash
```

Precomputed provider/runtime values are not source-faithful unless their source rows and estimator state can be recomputed and hashed inside the trusted runner.

If any runtime history state cannot be reconstructed from admissible completed bars, replay fails closed:

```text
BLOCKED_SOURCE_UNRESOLVED_FORECAST_HISTORY_STATE_HASHES
```

## Forecast Context Binding

`S27V2ForecastContext` may continue to exist as a structural object, but a trusted replay step must prove it was derived from:

- a validated source input manifest row;
- a strict-prior daily runtime row;
- a forecast replay row;
- a desired-position row;
- the S27 scalar source lock;
- completed bars only.

A future implementation should introduce a replay-owned forecast context artifact, for example:

```text
S27V2TrustedForecastContext
```

That artifact must include or reference:

```text
replay_id
step_index
forecast_hash
source_input_hash
daily_runtime_hash
```

Free-form caller-created forecast contexts must never be accepted as source-faithful replay evidence.

The trusted forecast replay payload must expose all intermediate arithmetic needed for hostile audit:

- EWMA5 equilibrium value and state hash;
- raw mean-reversion forecast before sigma bridge;
- sigma bridge price;
- annual percentage sigma value;
- sigma source/provenance hash;
- sigma-price value;
- risk-adjusted forecast before trend veto;
- EWMAC(16,64) trend value and sign;
- trend-veto decision;
- risk-adjusted forecast after veto;
- relative volatility V;
- expanding quantile Q;
- raw volatility multiplier;
- EWMA10 multiplier M;
- risk-adjusted forecast after veto times M before scalar;
- scalar;
- capped forecast;
- desired unrounded position;
- desired rounded position.

A single opaque `forecast_hash` is insufficient unless it hashes this locked schema.

## Order Plan Binding

A trusted order plan must bind:

- replay id;
- step index;
- raw symbol;
- session id;
- completed trading date;
- decision timestamp;
- current position from prior trusted step;
- desired rounded position from trusted desired-position row;
- source-required adjacent limit set;
- market-order trigger source condition if market order is required;
- formula-implied price for each limit order;
- executable tick price for each limit order;
- tick rounding direction by side;
- tick policy hash or explicit tick-policy fail-closed status;
- order-plan hash.

The complete adjacent limit set must be recomputed from the trusted forecast context and current position. Omitted or extra limit orders fail closed.

The current synthetic exact formula price is not sufficient for local-row replay. Before replay over real ZN rows, ZN tick size and rounding direction must be source-locked:

```text
BLOCKED_SOURCE_UNRESOLVED_ZN_TICK_ROUNDING_POLICY
```

Until then, real-row replay must fail closed before executable limit prices are emitted.

Synthetic formula-only limit prices must remain labeled as synthetic structural evidence, not executable local-row replay evidence.

## Working State And Transition Binding

Working state must not be caller-created source evidence.

A trusted working state must bind:

- replay id;
- step index;
- raw symbol;
- session id;
- current position;
- desired position;
- order-plan hash;
- previous trusted step hash if any.

The phrase "if any" applies only to the first replay step. Every non-initial step must bind the previous step hash. The first step must bind an audited initial-state hash.

Initial position must not be caller-chosen by convenience. It must be locked by:

```text
initial_position_policy_hash
initial_state_hash
```

Default initial state is flat unless a separate source-locked carry-in position artifact exists. If the initial state is missing or ambiguous:

```text
BLOCKED_SOURCE_UNRESOLVED_INITIAL_POSITION_POLICY
```

Normal one-hour transition must prove:

- one-hour lag;
- unchanged raw symbol;
- unchanged session id;
- unchanged completed trading date;
- completed-bar close-only fill authority.

EOD cancel/reset remains structural only until full day/session lifecycle is source-locked.

Overnight reset must remain fail-closed until next-session desired-position recomputation is implemented:

```text
BLOCKED_SOURCE_UNRESOLVED_OVERNIGHT_RECOMPUTED_TARGET
```

Nonzero-position roll remains fail-closed until a source-locked roll bridge exists:

```text
BLOCKED_SOURCE_UNRESOLVED_NONZERO_ROLL_BRIDGE
```

## Fill, Cost, And PnL Binding

Trusted fills must be emitted only by the trusted transition step. They must include:

- replay id;
- step index;
- order-plan hash;
- filled order hash;
- limit-order hash or market-order hash;
- transition hash;
- fill timestamp;
- fill decision source row hash;
- submitted limit price if order kind is limit;
- market-order trigger hash if order kind is market;
- fill condition hash;
- fill price provenance, exactly one of `LIMIT_ORDER_PRICE_FROM_FILLED_ORDER` or `MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE`;
- order kind;
- side;
- quantity;
- fill hash.

For limit orders, the next completed close is fill-decision authority under the locked one-hour-lag primitive, but the fill price is the submitted executable limit price from the filled order row. For market orders, the fill price source is the next completed close under the locked market-order primitive.

Trusted cost rows must include:

- replay id;
- step index;
- fill hash;
- order kind;
- side;
- quantity;
- commission policy hash;
- commission per contract;
- commission unit, locked as `PER_CONTRACT`;
- commission currency;
- commission amount;
- spread policy hash if applicable;
- spread unit if applicable;
- spread amount if applicable;
- spread space if applicable, exactly one of `PRICE_SPACE` or `CURRENCY_SPACE`;
- contract multiplier value and source hash if spread/cost conversion uses multiplier;
- currency conversion value and source hash if applicable;
- deflation policy hash if applicable;
- total cost amount;
- total cost currency;
- cost hash.

All trusted cost rows must prove positive commission for every filled order. Market-order cost rows must prove commission plus normal bid/ask spread under the locked spread-unit policy. Limit-fill cost rows must prove commission only unless the source lock is revised to require spread costs for limit fills. Cost rows with missing amount, missing unit, missing currency, negative cost, zero commission, ambiguous spread space, or policy/payload mismatch fail closed:

```text
BLOCKED_SOURCE_UNRESOLVED_TRUSTED_COST_ROW_AMOUNT_UNIT_SCHEMA
```

Trusted PnL rows must include:

- replay id;
- step index;
- replay trust root hash;
- source universe hash;
- previous step hash or initial-state hash;
- starting working-state hash;
- starting position;
- transition hash;
- ending working-state/position hash;
- ending position;
- prior position source;
- position source hash;
- PnL formula policy hash;
- price source kind, locked as `CLOSE_ONLY`;
- start price source row hash;
- end price source row hash;
- raw-symbol continuity proof or roll-bridge proof;
- contract multiplier source hash;
- contract multiplier value and source hash;
- currency/FX policy hash if applicable;
- currency value and source hash if applicable;
- cost application policy hash;
- fill hash set;
- cost hash set;
- PnL hash.

PnL helpers must not be treated as source-faithful if called with arbitrary starting position, arbitrary prices, or empty cost/fill lineage.

An empty fill or cost set is trusted only if it is an explicit output of a trusted transition hash. Caller omission of fills/costs is never accepted as source evidence.

## Persistent Working Limit Lifecycle Gate

Current synthetic replay fails closed when normal one-hour no-fill transitions leave working limits unresolved. That is correct for the current slice but incomplete relative to the book.

Before local-row replay can run over a multi-hour/day window, design must define:

- how unfilled limits persist;
- how existing working orders are modified after a fill;
- how new adjacent orders are created after a fill;
- when orders cancel at EOD;
- how a new session recomputes desired position and orders.

Until that lifecycle is implemented and audited:

```text
BLOCKED_SOURCE_UNRESOLVED_WORKING_LIMIT_LIFECYCLE
```

## Strategy 3 Sigma Gate

The current annual percentage sigma status is sufficient only for synthetic/prevalidated rows.

Before local-row replay, Strategy 3 sigma provenance must prove:

- estimator definition;
- exact estimator formula;
- lookback;
- decay/half-life convention if applicable;
- annualization;
- daily return construction;
- missing-row behavior;
- history-window serialization;
- source rows;
- completed-bar causality;
- row hashes;
- strict-prior use by S27.

The sigma proof must include:

```text
sigma_estimator_definition_hash
sigma_input_window_hash
sigma_annualization_policy_hash
sigma_estimator_state_hash
```

Provider/precomputed sigma may not be substituted unless its row-level construction can be reconstructed or independently source-locked for this lane.

Until then:

```text
BLOCKED_SOURCE_UNRESOLVED_STRATEGY3_SIGMA_PROVENANCE
```

## Capacity And Speed Eligibility Gate

Before any result interpretation, the replay evidence must carry capacity and speed-limit eligibility.

Carver's single-lot limit-order assumptions can break down when order sizes bunch or cease to be single-lot orders. Mechanical replay may proceed only after separate authorization and only as mechanical evidence; performance interpretation remains blocked until:

```text
capacity_speed_eligibility_hash
```

is source-locked.

Gate distinction:

```text
mechanical_replay_design_gate = separate operator authorization required
performance_interpretation_gate = capacity_speed_eligibility_hash required
```

Until then:

```text
BLOCKED_SOURCE_UNRESOLVED_CAPACITY_SPEED_ELIGIBILITY
```

## Stale Evidence Supersession Manifest

Every trusted replay bundle must carry an active evidence manifest:

```text
active_evidence_manifest_hash
```

The manifest must list:

- artifact type;
- file path;
- content hash;
- status label;
- active source-lock artifact hash;
- active data-contract artifact hash;
- active provenance design artifact hash;
- active implementation hash;
- active test/audit evidence hashes;
- superseded source-lock, test, remediation, and audit artifacts;
- supersession reason for each superseded artifact;
- superseding artifact hash;
- effective date/time.

Stale unit-test counts, stale hashes, or superseded audit labels must not be accepted as readiness proof.

Until this manifest exists:

```text
BLOCKED_SOURCE_UNRESOLVED_STALE_EVIDENCE_SUPERSESSION_MANIFEST
```

## Local-Row Replay Readiness Checklist

Local-row replay design is not complete until the following are specified and externally audited:

- trusted replay identity schema;
- replay trust root schema;
- canonical row serialization and hash rules;
- hash algorithm/version rules;
- decimal/float, timezone, and row ordering/collation normalization rules;
- source universe and row locator schema;
- source universe inclusion/exclusion, missing-row, repair/rejection, duplicate, and row-ordering schemas;
- source input manifest schema;
- daily/hourly continuous/current level compatibility proof schema;
- sigma bridge level source schema;
- runtime history state hash schema;
- trusted forecast context schema;
- forecast intermediate arithmetic schema;
- trusted order-plan schema;
- formula-implied price vs executable tick-price schema;
- initial position policy;
- trusted working-state schema;
- trusted transition/fill schema;
- order-level filled-order and fill-condition binding schema;
- trusted cost/PnL schema;
- trusted cost row amount/unit schema;
- PnL formula, position-field, multiplier, currency, and cost-application schemas;
- ZN tick rounding rule or fail-closed policy;
- working-limit lifecycle policy;
- overnight recomputed-target policy;
- nonzero roll bridge policy;
- Strategy 3 sigma provenance policy;
- session/roll calendar source policy;
- spread-unit and commission policy;
- capacity/speed eligibility policy;
- stale evidence supersession policy.

## Next Authorized Step Recommendation

Recommended next step:

```text
PREPARE_EXTERNAL_AUDIT_PACKET_FOR_THIS_PROVENANCE_DESIGN
```

The audit should ask whether this design is sufficient to stop the synthetic patch loop and safely guide local-row replay implementation.

No implementation, parser work, replay execution, diagnostics, backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git staging, commit, or push are authorized by this artifact.

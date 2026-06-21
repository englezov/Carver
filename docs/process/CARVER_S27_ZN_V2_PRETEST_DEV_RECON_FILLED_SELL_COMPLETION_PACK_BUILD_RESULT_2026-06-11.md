# S27_V2 Pre-TEST Development/Reconciliation Filled Sell Completion Pack Build Result

Date: 2026-06-11

Status:

```text
LOCAL_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_PACK_DECLARED_NOT_RESULT
```

Declared pack:

```text
docs\researchops\s27_v2_local_replay_inputs\ZN\20260611_pretest_dev_recon_2022_filled_sell_completion_declared_pack
```

This pack is local-only, pre-2023, and built only from already-local ZN source
ledgers. It selects the earliest 2022 organic filled sell-side reduction found
after strict-prior warmups/evidence are populated. The pack preserves 2023 for
TEST and emits no result interpretation, no promotion evidence, and no
source-faithful evidence claim.

Selected row count:

```text
46
```

Filled sell completion:

```text
row_index = 46
decision_timestamp_utc = 2022-07-05T23:00:00Z
fill_timestamp_utc = 2022-07-06T00:00:00Z
valuation_mark_timestamp_utc = 2022-07-06T02:00:00Z
raw_symbol = ZNU2
starting_position_contracts = 39
desired_position_contracts = 0
position_change_contracts = -39
order_side = SELL
order_quantity = 39
limit_order_price = 117.390625
fill_candidate_close = 119.8125
fill_executed = YES
```

Rolling strict-prior evidence:

```text
PASS_RECOMPUTED_PER_SELECTED_ROW_FROM_ALREADY_LOCAL_PRE2023_SOURCE_LEDGERS
PASS_NO_FUTURE_ROLL_DELTAS_PER_SELECTED_ROW_CUTOFF
```

Post-patch symbol-path rule:

```text
decision/fill/valuation rows remain on one raw-symbol path per selected row
valuation mark is the next completed same-symbol row strictly after fill
```

Non-authorizations:

```text
NO_PROVIDER_API
NO_DOWNLOADS
NO_NEW_DATA_ACQUISITION
NO_TEST_ACCESS
NO_VALIDATION_ACCESS
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_RESULT_SCORED_RUN
NO_RESULT_INTERPRETATION
NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION
NO_TUNING
NO_ADAPTER_WORK
NO_DEPLOYMENT
NO_TRADING
NO_PROMOTION
NO_GIT_ACTIONS
NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM
```

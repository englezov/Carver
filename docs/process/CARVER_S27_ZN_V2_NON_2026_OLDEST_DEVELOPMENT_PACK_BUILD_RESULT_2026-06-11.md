# S27_V2 Non-2026 Oldest Development Pack Build Result

Date: 2026-06-11

Status:

```text
LOCAL_NON_2026_DECLARED_INPUT_PACK_BUILT_NOT_RUN_NOT_RESULT
```

Authorization:

```text
S27_V2_NON_2026_OLDEST_LOCAL_DEVELOPMENT_PACK_BUILD_GATE
```

## Scope

This gate built a minimum oldest suitable non-2026 ZN Development/Reconciliation declared input pack from already-local files only.

It did not run a parser/file replay, diagnostic, backtest, scored result, result interpretation, PnL evaluation, provider/API call, download, OOS/Lockbox/Forward access, Git action, adapter/deployment/trading/promotion action, or source-faithful evidence claim.

## Pack

Declared input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_non_2026_oldest_dev_recon_znu3_20230522_declared_pack
```

Manifest:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_non_2026_oldest_dev_recon_znu3_20230522_declared_pack/S27_V2_NON_2026_OLDEST_DECLARED_INPUT_PACK_MANIFEST.json
```

Manifest SHA256:

```text
B7DFF0830615E2ED8DB9A34A319C0DAA1F75665C10FE2907FA0C4693DE091BD7
```

## Selected Slice

```text
selected_decision_timestamp_utc = 2023-05-22T00:00:00Z
selected_fill_timestamp_utc = 2023-05-22T01:00:00Z
selected_previous_daily_timestamp_utc = 2023-05-21T00:00:00Z
raw_symbol = ZNU3
lane = SOURCE_NATIVE_FUTURES
```

Selection rationale:

```text
MINIMUM_OLDEST_LOCAL_NON_2026_SLICE_AFTER_STRICT_PRIOR_VQM_AND_POST_ROLL_LEVEL_COMPATIBILITY_POPULATED
```

The 2026 ZNM6 packs were explicitly excluded by operator instruction. The existing 2022 ZNH2 pack remains fail-closed because its own manifest records stale V/Q/M evidence before the selected 2022 decision row.

The first local ten-year V/Q/M daily evidence begins on `2023-05-18`; the selected slice uses the `2023-05-21` V/Q/M row strictly prior to the `2023-05-22T00:00:00Z` decision and avoids the 2023-05-19 roll-transition mismatch.

## Row Families

```text
daily_continuous_completed_bar.csv = 64 rows, chronological ascending, selected previous daily row last
daily_current_contract_completed_bar.csv = 1 row
hourly_decision_completed_bar.csv = 1 row
hourly_fill_completed_bar.csv = 1 row
session_calendar.csv = 1 row
roll_calendar.csv = 1 row
cost_parameter.csv = 1 row
```

## Level Bridge

The older candidate-comparison hourly continuous lineage uses additive adjustment `0.84375` around the 2023 `ZNM3`/`ZNU3` roll. This pack rejects that lineage as level authority for this gate.

The pack instead reads already-local raw `ZNU3` hourly bars and normalizes the selected decision/fill rows onto the ten-year V/Q/M daily roll level using additive adjustment:

```text
2.28125
```

Selected values:

```text
daily_current_raw_close = 114.546875
daily_continuous_close = 116.828125
hourly_decision_continuous_close = 116.828125
hourly_fill_continuous_close = 116.921875
```

This is a local level-space bridge, not price-equality evidence, not execution evidence, and not result evidence.

## Evidence Notes

Selected V/Q/M evidence:

```text
completed_trading_date = 2023-05-21
relative_volatility_v = 1.3831478154868233
quantile_q = 0.0
vol_multiplier_m_ewma10 = 1.2747933884297518
historical_v_observation_count = 3
```

Selected Strategy 3 sigma evidence:

```text
completed_trading_date = 2023-05-21
sigma_i_t = 0.061240880678963244
method = STRATEGY_3_STYLE_EWMA32_PERCENT_RETURN_SIGMA_ANNUALIZED_256
```

Working-order lifecycle remains explicitly fail-closed for actual multi-row execution until the runner binds state row by row.

After local hostile audit P1 review, the pack was patched to declare first-row empty working-order state only:

```text
initial_current_position_contracts = 0
open_working_orders = 0
state_scope = FIRST_ROW_CONTEXT_ONLY_NOT_FULL_MULTI_ROW_LIFECYCLE_EVIDENCE
runner_must_bind_subsequent_state = YES
```

This closes the pack-level first-row context requirement without claiming full multi-row lifecycle evidence.

## Verification

Focused local verification passed:

```text
python -m pytest tests\test_s27_v2_non_2026_oldest_pack.py tests\test_s27_v2_multi_row_development_runner.py -q
36 passed
```

The tests verify:

- manifest authorization/status/non-authorization binding;
- no 2026 row-family selected data;
- row-family SHA256 and row-count binding;
- chronological daily continuous row order;
- strict-prior V/Q/M date;
- daily/hourly level bridge arithmetic;
- first-row empty working-order context without full lifecycle overclaim;
- no run/result/source-faithful claim surface.

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, 2026 data, TEST/VALIDATION access, OOS/Lockbox/Forward access, parser/file replay execution, diagnostics, backtests, result-scored runs, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

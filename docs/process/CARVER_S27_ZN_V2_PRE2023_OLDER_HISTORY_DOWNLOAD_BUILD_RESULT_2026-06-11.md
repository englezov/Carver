# Carver S27_V2 ZN Pre-2023 Older-History Download/Build Result

Date: 2026-06-11

Status:

```text
PASS_S27_V2_PRE2023_ZN_HISTORY_DOWNLOADED_AND_2022_PACK_DECLARED_NOT_BACKTEST_NOT_RESULT
```

Authorization:

```text
S27_V2_EXACTLY_ONE_DATABENTO_ZN_OLDER_HISTORY_DOWNLOAD_BUILD_GATE
```

Window preservation:

- 2022 is Development/Reconciliation.
- 2023 is preserved for TEST.
- 2024+ remains unopened by this gate.

Output root:

```text
docs\researchops\s27_v2_databento_older_zn_history\20260611_pre2023_zn_dev_recon_download_build
```

Declared pack:

```text
docs\researchops\s27_v2_local_replay_inputs\ZN\20260611_pre2023_oldest_dev_recon_2022_declared_pack
```

Selected Development/Reconciliation row:

```text
raw_symbol = ZNH2
selected_decision_timestamp_utc = 2022-01-03T01:00:00Z
selected_fill_timestamp_utc = 2022-01-03T02:00:00Z
selected_previous_daily_timestamp_utc = 2021-12-31T00:00:00Z
```

Strict-prior point-in-time level rule:

```text
point_in_time_roll_cutoff_date = 2021-12-31
future_roll_deltas_after_cutoff_excluded = YES
daily_current_raw_close = 130.34375
daily_continuous_close = 130.34375
daily_additive_back_adjustment = 0.0
hourly_additive_back_adjustment_applied_for_bridge = 0.0
```

Local hostile audit disposition:

```text
INITIAL_FAIL_FOR_FUTURE_2022_ROLL_LEAK_PATCHED_AND_REAUDITED_PASS
```

The initial declared-pack build was rejected by local hostile audit because
future 2022 roll deltas leaked into the selected row's continuous/V/Q/M level
authority. The patched build uses a point-in-time continuous risk history cut
off at the selected previous completed daily row. Re-audit returned `PASS` with
no P0/P1/P2/P3 findings.

Non-authorization: no backtests, result-scored runs, result interpretation, PnL evaluation, tuning,
adapter work, deployment, trading, promotion, Git actions, OOS, Lockbox, Forward, or source-faithful
evidence claim.

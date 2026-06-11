# Local Hostile Audit - S27_V2 ZN Pre-2023 Older-History Download/Build

Date: 2026-06-11

Final verdict:

```text
PASS_AFTER_POINT_IN_TIME_ROLL_CUTOFF_PATCH
```

## Scope

This audit covers the authorized DataBento source-native ZN older-history
download/build gate for a 2022 Development/Reconciliation input pack.

Provider/API use was restricted to DataBento ZN pre-2023 history for this gate.
No 2023 TEST, VALIDATION, OOS, Lockbox, or Forward data was opened by the
declared pack. No backtest, result-scored run, result interpretation, PnL
evaluation, tuning, Git action, deployment, trading, promotion, or
source-faithful evidence claim was made.

## Initial Local Hostile Audit

Initial verdict:

```text
FAIL
```

The initial hostile audit found one material strict-prior issue:

```text
P1 - future 2022 roll deltas leaked into the selected 2022 row's daily
continuous/V/Q/M level authority.
```

The audit observed that the selected `2022-01-03` row used a continuous close
that had incorporated future 2022 roll deltas after the selected previous daily
row. This was incompatible with the strict-prior/completed-bar requirement for
Development/Reconciliation replay construction.

## Patch

The builder was patched so the selected 2022 declared pack uses a
point-in-time continuous risk history cut off at the selected previous completed
daily row:

```text
point_in_time_roll_cutoff_date = 2021-12-31
future_roll_deltas_after_cutoff_excluded = YES
```

The selected declared pack now binds:

```text
selected_raw_symbol = ZNH2
selected_decision_timestamp_utc = 2022-01-03T01:00:00Z
selected_fill_timestamp_utc = 2022-01-03T02:00:00Z
selected_previous_daily_timestamp_utc = 2021-12-31T00:00:00Z
daily_current_raw_close = 130.34375
daily_continuous_close = 130.34375
daily_additive_back_adjustment = 0.0
hourly_additive_back_adjustment_applied_for_bridge = 0.0
```

The declared pack roll calendar now stops before future 2022 roll transitions;
its last roll transition is the pre-cutoff roll into `ZNH2`:

```text
roll_transition_date = 2021-11-18
old_contract_key = ZNZ1_2021
new_contract_key = ZNH2_2022
```

## Verification

Focused verification passed:

```text
python -m py_compile tools\databento\carver_s27_v2_zn_pre2023_history_download_build.py
python -m pytest tests\test_s27_v2_pre2023_databento_pack.py tests\test_s27_v2_multi_row_development_runner.py -q
36 passed
```

## Local Hostile Re-Audit

Re-audit verdict:

```text
PASS
```

Findings:

```text
P0: none
P1: none
P2: none
P3: none
```

The re-audit confirmed that the future-2022-roll/V/Q/M strict-prior leak is
closed. It specifically checked that the selected 2022 pack uses the
point-in-time cutoff at `2021-12-31`, the daily continuous close equals the
current raw close, bridge adjustment is `0.0`, and the declared pack roll
calendar stops before 2022 future rolls.

Status hash evidence is in:

```text
docs\researchops\s27_v2_databento_older_zn_history\20260611_pre2023_zn_dev_recon_download_build\hashes\20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_sha256.json
```

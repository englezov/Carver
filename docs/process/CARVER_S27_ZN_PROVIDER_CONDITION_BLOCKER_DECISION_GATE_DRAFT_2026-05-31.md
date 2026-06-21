# Carver S27 ZN Provider-Condition Blocker Decision Gate Draft

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_DECISION_GATE_DRAFT_NOT_BACKTEST_AUTHORIZATION
```

## Purpose

Decide how to handle the single degraded Databento provider-condition row found in the S27 ZN 2022-2023 hourly quarantine archive before any backtest execution.

## Blocking Evidence

Current intake status:

```text
FAIL_CLOSED_PROVIDER_CONDITION_BLOCKERS_PRESENT_NOT_BACKTEST_READY
```

Affected evidence:

```text
provider_condition_date: 2022-01-02
provider_condition_status: PROVIDER_CONDITION_DEGRADED
affected_quarantine_rows: 1
archive_root: docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/
```

The degraded row is preserved in quarantine and explicitly marked:

```text
QUARANTINE_PRESERVED_PROVIDER_CONDITION_BLOCKED_NOT_BACKTEST_READY
```

## Allowed Future Decision Shapes

A later separately authorized execution gate may choose exactly one:

```text
OPTION_A_FAIL_CLOSED_FULL_BACKTEST_BLOCKED
```

No backtest is run until the archive has only provider-condition-available rows.

```text
OPTION_B_EXCLUDE_DEGRADED_ROW_AND_RECORD_GAP
```

Exclude the single degraded row from strategy-facing lineage, preserve it in quarantine, record a one-row provider-condition exclusion ledger, and fail closed if exclusion creates missing completed-bar or roll-lineage gaps.

```text
OPTION_C_REDUCE_BACKTEST_START_AFTER_BLOCKER
```

Retarget the backtest start after the affected completed trading date if this avoids all degraded provider-condition rows without silent row skipping.

## Prohibited Decisions

```text
silent use of degraded row
silent row drop
fill/interpolate/synthesize the affected row
substitute another contract or provider row
treat degraded provider condition as normal without explicit audit record
expand symbol set or date window
run diagnostics/backtest/forecast/position/cost before the provider-condition decision is locked
```

## Non-Authorization

This draft authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

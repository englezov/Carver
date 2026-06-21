# Carver ZN Local Continuous Daily Lifecycle Repair Result

Date: 2026-05-31

Status:

```text
PASS_ZN_LOCAL_CONTINUOUS_DAILY_LINEAGE_DEV_RECON_ONLY
```

## Scope

This result repairs the ZN local continuous daily lineage needed by the S27 EWMAC16 trend dependency.

It uses only existing local Carver CSV artifacts plus official static lifecycle rules already identified for ZN. It does not request new provider data, parse expanded market rows, compute EWMAC16, compute S27, run diagnostics, or run a backtest.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

## Official Static Evidence Basis

Official static sources used as lifecycle rule authority:

```text
CME / CBOT Rulebook Chapter 19: https://www.cmegroup.com/content/dam/cmegroup/rulebook/CBOT/II/19.pdf
CME Treasury Futures Delivery Process: https://www.cmegroup.com/content/dam/cmegroup/trading/interest-rates/files/us-treasury-futures-delivery-process.pdf
CME Group 2026 holiday/trading-hours page: https://www.cmegroup.com/trading-hours.html
```

Rule atoms locked:

```text
ZN is CBOT Chapter 19 U.S. Treasury Note futures, 6 1/2 to 8 year.
Trading terminates before the last seven business days of the named expiration month.
Delivery month runs from the first business day through the last business day of the named month.
First intention is the second business day before the first business day of delivery month.
First notice is the next business day after first intention.
For ZN, last intention is the second business day before the last business day of delivery month; last notice is the next-to-last business day; last delivery is the last business day.
Juneteenth 2026 is a CME/CBOT holiday schedule date, so ZNM6 last trade falls on 2026-06-18 rather than 2026-06-19.
```

## Locked Lifecycle Dates

| Contract | First notice | First delivery | Last trade | Last delivery | Databento expiration cross-check |
|---|---|---|---|---|---|
| ZNH6 | 2026-02-27 | 2026-03-02 | 2026-03-20 | 2026-03-31 | 2026-03-20 17:01:00+00:00 |
| ZNM6 | 2026-05-29 | 2026-06-01 | 2026-06-18 | 2026-06-30 | 2026-06-18 17:01:00+00:00 |

## Roll Decision

Existing deterministic rule:

```text
physical_delivery_roll_buffer = 10 completed trading dates before earliest lifecycle blocker
roll_transition_date = latest completed trading date on or before that buffer date where old and new contracts both have normal-provider-condition rows
```

For ZNH6 -> ZNM6:

```text
earliest_lifecycle_blocker = ZNH6 first_notice_date = 2026-02-27
completed_trading_date_policy = source completed trading dates from the existing normal-provider row set, including Sunday Globex sessions
roll_transition_date = 2026-02-16
```

Roll pair:

```text
ZNH6 close on 2026-02-16 = 113.21875
ZNM6 close on 2026-02-16 = 113.140625
old-history additive offset = -0.078125
```

Adjustment method:

```text
LOCAL_ADDITIVE_BACK_ADJUSTMENT_OLD_HISTORY_TO_NEW_CONTRACT_LEVEL
```

## Output

Artifact root:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/local_continuous_daily_lineage_2026-05-31/
```

Core files:

```text
ledger/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_lifecycle_evidence_lock.csv
ledger/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_roll_plan.csv
ledger/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_adjustment_ledger.csv
ledger/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_source_lineage.csv
ledger/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_series_dev_recon_only.csv
status/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_status.csv
provenance/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_provenance.json
hashes/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_sha256.json
```

Counts:

```text
continuous_rows_emitted = 175
source_rows_available = 281
```

## Boundary

This local continuous series is Development/Reconciliation-only lineage for S27 dependency construction. It is not TEST, VALIDATION, OOS, Lockbox, Forward, strategy input, backtest input, or promotion evidence.

## Non-Authorization

This result authorizes no additional provider API access, no new data download, no market-row expansion, no provider-built continuous contract, no EWMAC16 trend computation by itself, no S27 computation, no diagnostics, no backtests, no positions, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, and no Git operation.

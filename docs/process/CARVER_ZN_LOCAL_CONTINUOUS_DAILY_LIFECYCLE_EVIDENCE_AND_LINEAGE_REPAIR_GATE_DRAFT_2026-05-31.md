# Carver ZN Local Continuous Daily Lifecycle Evidence And Lineage Repair Gate Draft

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_EVIDENCE_AND_LINEAGE_REPAIR_GATE_DRAFT_NOT_DATA_NOT_TREND_NOT_S27_EXECUTION
```

## Purpose

Define the exact gate required to unblock, or explicitly keep blocked, the S27 EWMAC16 trend dependency for the ZN worked-example path.

S27 requires a source-faithful daily EWMAC(16,64) trend forecast. The book input is a back-adjusted continuous daily price series, not a single dated contract close series. The current ZN EWMAC16 source gate failed closed because the local continuous daily ZN lineage is not source-locked.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

## Current Evidence State

Known locally:

```text
ZNH6 -> ZNM6 adjacent daily rows exist
ZNH6 Databento instrument id = 42004475
ZNM6 Databento instrument id = 42000661
ZNU6 Databento instrument id = 42001136
Databento definition metadata locks activation / expiration / maturity / venue / currency / family fields
```

Still missing:

```text
official first_notice_date
official delivery-window blocker dates
official last-trade or last-delivery blocker dates
official lifecycle blocker precedence for the roll rule
```

## Required Static Evidence

The execution gate must use hash-bound official static source/provider evidence for 10-Year U.S. Treasury Note futures sufficient to lock:

```text
product family = ZN / 10-Year U.S. Treasury Note futures
venue normalization = XCBT / CBOT / CME Globex relationship
currency = USD
contract months = quarterly Treasury cycle
ZNH6 first notice / delivery / last trade / final settlement blockers
ZNM6 first notice / delivery / last trade / final settlement blockers
roll blocker precedence
daily settlement versus close policy for roll-alignment labeling
```

Databento definition metadata alone is not sufficient because it does not provide first-notice or delivery-window dates.

## Repair Execution Shape

If official lifecycle evidence is locked, the repair execution must produce:

```text
ZN lifecycle evidence lock ledger
ZNH6 -> ZNM6 roll transition decision
roll-plan update
additive adjustment ledger
source-lineage ledger
local continuous daily ZN Development/Reconciliation-only series
status/provenance/SHA artifacts
```

The roll decision must use the existing deterministic policy:

```text
physical_delivery_roll_buffer = 10 completed trading days before the earliest locked lifecycle blocker
roll_transition_date = latest completed trading date on or before the buffer date where old and new contracts both have normal-provider-condition rows
```

## Fail-Closed Rules

The gate must fail closed if any of the following occurs:

```text
official lifecycle evidence is unavailable or ambiguous
first-notice/delivery/last-trade blockers conflict
ZNH6 and ZNM6 cannot be proven same source-native product family
old/new overlap is missing at the selected roll date
provider condition is not normal on required old/new roll rows
roll date is selected from volume, open interest, convenience, or after-the-fact performance
single dated ZNM6 is substituted for continuous daily ZN
provider-built continuous contract is substituted for local lineage
```

## Explicit Non-Authorization

This gate draft authorizes no Databento access, no official web/PDF download, no market-row parsing, no new OHLCV request, no continuous-contract download, no provider-built continuous source authority, no EWMAC16 trend computation, no S27 computation, no diagnostics, no backtests, no positions, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR update/opening.

## Next Gate

```text
OFFICIAL_STATIC_ZN_LIFECYCLE_EVIDENCE_OR_FAIL_CLOSED_ROLL_POLICY_DECISION
```

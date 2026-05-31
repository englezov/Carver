# Local Lean Hostile Audit - S27 ZN EWMAC16 Trend Runtime

Date: 2026-05-31

Mode:

```text
LOCAL_LEAN_HOSTILE_AUDIT
```

## Audited Artifacts

```text
docs/process/CARVER_ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_RESULT_2026-05-31.md
docs/process/CARVER_S27_ZN_EWMAC16_TREND_RUNTIME_EXECUTION_RESULT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/local_continuous_daily_lineage_2026-05-31/
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/ewmac16_trend_runtime_ledger_2026-05-31/
tools/databento/carver_zn_local_continuous_lifecycle_repair.py
tools/databento/carver_s27_zn_ewmac16_trend_runtime.py
```

## Findings

### Critical

None.

### High

None.

### Medium

None.

## Checks

Lifecycle repair:

```text
PASS
```

The ZN local continuous series uses official static lifecycle rule evidence and existing local ZNH6/ZNM6 normal-provider rows. It does not use a provider-built continuous contract.

No-lookahead:

```text
PASS
```

Each EWMAC16 runtime row uses only daily continuous rows strictly before the paired S26 hourly row's completed trading date.

Runtime alignment:

```text
PASS
```

The runtime ledger emits 686 rows, matching the 686 S26 forecast-series-only rows one-for-one by timestamp and identity.

Governance:

```text
PASS
```

No provider API access, new data download, market-row expansion, S27 forecast computation, diagnostic, backtest, position, cost, carry, trading, promotion, or Git operation is authorized or recorded.

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_EWMAC16_TREND_RUNTIME_DEPENDENCY_DEV_RECON_ONLY
```

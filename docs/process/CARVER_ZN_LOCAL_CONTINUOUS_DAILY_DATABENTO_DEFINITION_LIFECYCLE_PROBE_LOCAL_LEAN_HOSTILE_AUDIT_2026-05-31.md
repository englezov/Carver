# Local Lean Hostile Audit - ZN Databento Definition Lifecycle Probe

Date: 2026-05-31

Mode:

```text
LOCAL_LEAN_HOSTILE_AUDIT
```

## Audited Artifact

```text
docs/process/CARVER_ZN_LOCAL_CONTINUOUS_DAILY_DATABENTO_DEFINITION_LIFECYCLE_PROBE_RESULT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/zn_lifecycle_databento_definition_probe_2026-05-31/
tools/databento/carver_zn_lifecycle_definition_probe.py
```

## Findings

### Critical

None.

### High

None.

### Medium

None.

## Checks

Provider scope:

```text
PASS_METADATA_ONLY_DATABENTO_DEFINITION_SCHEMA
```

The probe requested `GLBX.MDP3 / definition` for `ZNH6`, `ZNM6`, and `ZNU6`. It did not request OHLCV rows, continuous contracts, parent futures, or expanded symbols.

Source blocker preservation:

```text
PASS_FAIL_CLOSED_FIRST_NOTICE_AND_DELIVERY_WINDOW_NOT_LOCKED
```

The result does not pretend that Databento definition metadata is official first-notice or delivery-window evidence. The S27 EWMAC16 dependency remains blocked until official lifecycle evidence or an explicit fail-closed roll-policy decision exists.

No strategy smuggle:

```text
PASS_NO_TREND_NO_S27_NO_DIAGNOSTIC_NO_BACKTEST
```

No EWMAC16 trend, S27 forecast, diagnostic, backtest, position, cost, carry, or performance artifact was emitted.

Secret handling:

```text
PASS_NO_API_KEY_IN_ARTIFACTS
```

The API key was read locally and was not printed or written to artifacts.

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_METADATA_ONLY_PROBE_PRESERVED_FAIL_CLOSED_FOR_LIFECYCLE_LOCK
```

The chapter remains blocked at the intended boundary:

```text
S27_EWMAC16_REAL_TREND_RUNTIME_LEDGER = NOT_AVAILABLE
NEXT_REQUIRED_GATE = OFFICIAL_STATIC_ZN_LIFECYCLE_EVIDENCE_OR_FAIL_CLOSED_ROLL_POLICY_DECISION
```

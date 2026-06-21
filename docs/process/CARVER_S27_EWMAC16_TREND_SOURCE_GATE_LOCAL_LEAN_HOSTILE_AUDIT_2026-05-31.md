# Carver S27 EWMAC16 Trend Source Gate Local Lean Hostile Audit

Date: 2026-05-31

Mode: local hostile audit. No provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no trend computation, no S27 forecast execution, no positions, no costs, no carry, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git operation.

Audited artifact:

```text
docs/process/CARVER_S27_EWMAC16_TREND_SOURCE_GATE_RESULT_2026-05-31.md
```

## Findings

Critical: none.

High: none.

Medium: none.

Low:

```text
L-1: This gate is a fail-closed source dependency result, not an implementation result. It advances the buildout by preventing an incorrect dated-contract trend substitution, but it does not produce an S27 trend runtime ledger.
```

## Scope Checks

The result correctly preserves the source hierarchy:

```text
S27 requires EWMAC(16,64)
EWMAC16 trend input requires back-adjusted continuous daily prices
current local continuous lineage says no continuous series constructed
provider-built continuous remains reference-only
dated ZNM6 closes are rejected as direct trend substitute
```

The ZN blocker is explicit:

```text
ROLL_PLAN_BLOCKED_LIFECYCLE_EVIDENCE_MISSING
BLOCKED_NO_ROLL_TRANSITION_DATE
ZNH6 -> ZNM6 lifecycle blocker dates not locked
```

No prohibited output is claimed:

```text
trend_runtime_ledger: NOT_EMITTED
S27 forecast: NOT_EMITTED
diagnostics/backtests/positions/costs/carry: NO
```

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_FAIL_CLOSED_S27_EWMAC16_SOURCE_GATE_NO_SUBSTITUTION_SCOPE
NEXT_REQUIRED_GATE: ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_EVIDENCE_AND_LINEAGE_REPAIR_GATE
```

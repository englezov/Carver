# Carver S26 ZN Hourly G_R1C Forecast-Series-Only Local Lean Hostile Audit

Date: 2026-05-31

Mode:

```text
LOCAL_LEAN_HOSTILE_AUDIT_RESULT_G_R1C_PLUMBING_PASS_NO_REAL_SERIES_EXECUTION
```

## Scope Audited

Audited:

```text
src/carver/spine/s26_s27.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
docs/process/CARVER_S26_ZN_HOURLY_G_R1C_FORECAST_SERIES_ONLY_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S26_S27_FORECAST_MACHINERY_BUILDOUT_SEQUENCE_2026-05-31.md
```

## Findings

### Critical

None.

### High

None.

### Medium

M-1. G_R1C is plumbing-complete, not real-series complete.

The code now supports forecast-series-only output, but no real 115-row G_R1A forecast series was emitted. This is correct under the current boundary because real series execution requires one prevalidated no-lookahead sigma runtime per forecast row.

### Low

L-1. S27 remains synthetic-only in code.

S27 forecast logic exists for synthetic conformance, but no real-hourly S27 input/handoff surface exists yet. This is expected and is preserved by the buildout sequence.

L-2. Sigma runtime provenance must remain hash-shaped.

The G_R1C plumbing depends on one prevalidated no-lookahead sigma runtime per forecast row. The implementation now fail-closes malformed `source_artifact_sha256` values for `S26SigmaPercentRuntimeValue`; tests include an explicit malformed-SHA rejection. This is a provenance hardening note, not a blocker.

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_G_R1C_FORECAST_SERIES_ONLY_PLUMBING_SCOPE
```

## Non-Authorization

This audit authorizes no provider API access, no new data download, no market-row expansion, no real forecast-series execution, no diagnostics, no backtests, no returns, no PnL, no positions, no costs, no carry, no trend computation, no S27 real-data computation, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

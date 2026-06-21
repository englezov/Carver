# Carver S27 Real-Hourly Forecast-Series-Only Handoff Local Lean Hostile Audit

Date: 2026-05-31

Mode:

```text
LOCAL_LEAN_HOSTILE_AUDIT_RESULT_S27_SERIES_HANDOFF_PASS_AFTER_INSTRUMENT_BOUND_HARDENING_NO_REAL_EXECUTION
```

## Scope Audited

Audited:

```text
src/carver/spine/s26_s27.py
src/carver/spine/__init__.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
docs/process/CARVER_S27_REAL_HOURLY_FORECAST_SERIES_ONLY_HANDOFF_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S27_REAL_HOURLY_FORECAST_ONLY_HANDOFF_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S26_S27_FORECAST_MACHINERY_BUILDOUT_SEQUENCE_2026-05-31.md
```

## Findings

### Critical

None.

### High

H-1. S27 runtime dependencies were not instrument-bound.

Patch:

```text
S27TrendOverlayRuntimeValue and S27VolAttenuationRuntimeValue now carry row_id, author_market_code, instrument_id, and raw_symbol.
S27 row handoff validates trend and V/Q/M runtime identity against the paired S26 forecast row.
Wrong trend-runtime and V/Q/M-runtime raw symbols have explicit fail-closed tests.
```

### Medium

M-1. S27 series top-level identity could drift from validated row payload.

Patch:

```text
S26 forecast-series validation now verifies locked ZN top-level identity and each S26 row identity/source-lock contract.
S27 forecast-series validation verifies locked ZN top-level identity and each S27 row output boundary.
Forged S26 series wrapper identity has an explicit fail-closed test.
```

### Low

L-1. V/Q/M series runtime tests were incomplete.

Patch:

```text
Missing V/Q/M runtime rows, shifted V/Q/M runtime timestamps, and duplicate V/Q/M runtime as_of values now fail closed in tests.
```

L-2. Documentation overstated identity coverage before hardening.

Patch:

```text
The series result now explicitly states S27 runtime identity fields and the paired-runtime identity drift fail-closed rule.
```

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_REAL_HOURLY_FORECAST_SERIES_ONLY_HANDOFF_AFTER_INSTRUMENT_BOUND_HARDENING
```

## Follow-Up Sub-Agent Audit

Follow-up read-only sub-agent audit disposition:

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_SERIES_PRIOR_FINDINGS_FIXED_READ_ONLY_AUDIT
```

Verified:

```text
S27 trend and V/Q/M runtime rows are instrument-bound.
S27 row handoff validates runtime identity against the paired S26 row.
S26/S27 series wrapper identity drift is blocked.
V/Q/M missing, shifted, and duplicate as_of tests exist.
No provider access, data work, diagnostics, backtests, positions, costs, carry, promotion, or Git operations were found.
```

## Non-Authorization

This audit authorizes no provider API access, no new data download, no market-row expansion, no real S27 execution, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

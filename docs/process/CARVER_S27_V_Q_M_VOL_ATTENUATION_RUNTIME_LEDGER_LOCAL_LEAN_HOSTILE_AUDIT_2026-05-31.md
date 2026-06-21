# Carver S27 V/Q/M Vol Attenuation Runtime Ledger Local Lean Hostile Audit

Date: 2026-05-31

Status:

```text
LOCAL_LEAN_HOSTILE_AUDIT_COMPLETE_SUBAGENT_ATTEMPT_ERRORED_USAGE_LIMIT
```

## Scope

Audited artifacts:

```text
src/carver/spine/s26_s27.py
src/carver/spine/__init__.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
docs/process/CARVER_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_LEDGER_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S26_S27_FORECAST_MACHINERY_BUILDOUT_SEQUENCE_2026-05-31.md
docs/process/CARVER_S27_REAL_HOURLY_FORECAST_ONLY_MACHINERY_SHAPE_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S27_EWMAC16_TREND_RUNTIME_LEDGER_PLUMBING_RESULT_2026-05-31.md
```

Subagent hostile audit was attempted automatically, but the subagent returned a usage-limit error before producing findings. This record therefore preserves a local lean hostile audit only.

## Findings

### Critical

None.

No inspected artifact performs provider access, data download, market-row parsing, real S13-style V/Q/M computation, diagnostics, backtests, returns, positions, costs, carry, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote operations.

### High

None.

The V/Q/M runtime ledger consumes prevalidated volatility-attenuation runtime rows only. The implementation validates locked source status, requires `SOURCE_NATIVE_FUTURES`, validates the paired S26 forecast-series-only output, and does not calculate relative volatility, quantile ranks, or attenuation multipliers from real market rows.

### Medium

None.

The ledger fail-closes unless there is exactly one V/Q/M runtime row per S26 forecast-only row, with timestamps matching the S26 forecast timestamps in order. Duplicate runtime timestamps, shifted timestamps, missing runtime rows, wrong instrument identity, wrong raw symbol, and unresolved source locks are covered by unit tests.

### Low

None.

The multiplier envelope is explicitly locked to `[0.5, 2.0]`; malformed provenance SHA, wrong runtime status, wrong method status, or wrong no-lookahead status are rejected by runtime-row validation.

## Verification

Focused verification:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
```

Result:

```text
30 focused S26/S27 tests passed
```

Full repository verification:

```text
python -m unittest discover -s tests
```

Result:

```text
186 tests passed
```

Compile verification:

```text
python -m py_compile src\carver\spine\s26_s27.py src\carver\spine\__init__.py
```

Result:

```text
PASS
```

Secret scan:

```text
rg -n "db-[A-Za-z0-9]{20,}" docs\process docs\researchops src tests
```

Result:

```text
NO_MATCHES
```

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_LEDGER_PLUMBING_READ_ONLY_AUDIT
```

## Non-Authorization

This audit authorizes no provider API access, no new data download, no market-row expansion, no real V/Q/M volatility computation, no real S27 execution, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

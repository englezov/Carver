# Carver S26 ZN Extended Hourly Forecast-Only Coverage Manifest Local Lean Hostile Audit

Date: 2026-05-31

Status:

```text
LOCAL_LEAN_HOSTILE_AUDIT_COMPLETE
```

## Scope

Audited artifacts:

```text
src/carver/spine/s26_s27.py
src/carver/spine/__init__.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_SHAPE_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_MANIFEST_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S26_S27_FORECAST_MACHINERY_BUILDOUT_SEQUENCE_2026-05-31.md
```

## Findings

### Critical

None.

No inspected artifact authorizes provider API access, new data download, market-row parsing, real forecast-series execution, diagnostics, backtests, returns, PnL, positions, orders, fills, costs, carry, trend computation, S27 real-data computation, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote operations.

### High

None.

The extended manifest remains source-native and exact-contract locked: `ZNM6`, Databento `instrument_id` 42000661, `GLBX.MDP3`, `ohlcv-1h`, and `stype_in=instrument_id`. Continuous contracts, parent symbols, and replacement symbols remain closed.

### Medium

None.

The extended request envelope is locked to `2026-04-12T00:00:00Z` through `2026-05-23T00:00:00Z`, targeting 30 weekday completed trading dates from `2026-04-13` through `2026-05-22`. The original G_R1A five-day target window remains included as a required subset.

### Low

None.

The manifest explicitly requires one prevalidated no-lookahead sigma runtime per future forecast row before any real forecast-series artifact can be emitted. This prevents the extended hourly window from silently becoming a volatility-estimation shortcut.

## Verification

Focused verification:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
```

Result:

```text
34 focused S26/S27 tests passed
```

Full repository verification:

```text
python -m unittest discover -s tests
```

Result:

```text
190 tests passed
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
AUDIT_DISPOSITION: PASS_S26_ZN_EXTENDED_FORECAST_ONLY_COVERAGE_MANIFEST_PLUMBING_READ_ONLY_AUDIT
```

## Non-Authorization

This audit authorizes no provider API access, no new data download, no market-row parsing, no real forecast-series execution, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no trend computation, no S27 real-data computation, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.


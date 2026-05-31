# Carver S26 ZN Hourly Databento Bridge Local Hostile Audit

Date: 2026-05-30

Status:

```text
LOCAL_LEAN_HOSTILE_AUDIT_RESULT_PROCESS_ONLY_NO_DATA_NO_BACKTEST
```

Audited artifact:

```text
docs/process/CARVER_S26_ZN_HOURLY_DATABENTO_BRIDGE_SHAPE_GATE_2026-05-30.md
```

Audit mode:

```text
LOCAL_HOSTILE_AUDIT
NO_PROVIDER_API_ACCESS
NO_DATA_DOWNLOAD
NO_MARKET_ROW_PARSING
NO_DIAGNOSTICS
NO_BACKTESTS
NO_REAL_FORECASTS
NO_POSITIONS
NO_GIT_OPERATIONS
```

## Findings

### Critical

None.

The bridge shape does not authorize Databento access, market-row parsing, diagnostics, backtests, positions, costs, carry, trend, S27 overlay, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations, or remote operations.

### High

None.

The first S26 real-data candidate is correctly anchored to the book's US 10-year future worked example and the local Appendix C `ZN` identity path. The document explicitly blocks `ZT`, T-bills, 2-year Treasury notes, MES/SP500, and the 16-symbol daily pilot as substitutes for the S26 worked-example gate.

### Medium

None blocking.

The request envelope is deliberately wider than the target completed trading-date window so a future hourly execution can capture overnight session rows. This is acceptable because the gate requires explicit row-level trading-date mapping, raw preservation, and labeling of non-target envelope rows. The future execution must not silently discard envelope rows.

### Low

The ZN dated contract currently has a prior static contract identity review note because the Appendix C multiplier semantics and Databento unit quantity need product-spec reconciliation. The bridge keeps this visible and does not promote the row to strategy-ready status.

## Source-Faithfulness Checks

| Check | Result |
| --- | --- |
| S26 uses hourly data, not daily data | PASS |
| First instrument follows book worked example | PASS |
| `ZN` is used instead of `ZT` or adjacent Treasury substitutes | PASS |
| Databento path uses `GLBX.MDP3` and `ohlcv-1h` as a future shape only | PASS |
| Continuous contracts remain closed | PASS |
| No daily Appendix C rows are used as S26 forecast input | PASS |
| S27 remains closed for first real-data bridge | PASS |
| Sigma-percent estimation remains a prerequisite before real forecast output | PASS |
| No diagnostics/backtests/positions are opened | PASS |

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_S26_ZN_HOURLY_DATABENTO_BRIDGE_SHAPE_GATE
NEXT_EXPLICIT_DATA_GATE_REQUIRED: G_R1A_ZN_S26_WORKED_EXAMPLE_DATABENTO_OHLCV_1H_TINY_QUARANTINE_INTAKE
```

## Non-Authorization

This audit authorizes no provider API access, no data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

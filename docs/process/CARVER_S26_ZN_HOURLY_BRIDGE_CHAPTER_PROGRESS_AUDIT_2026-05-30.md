# Carver S26 ZN Hourly Bridge Chapter Progress Audit

Date: 2026-05-30

Status:

```text
LOCAL_LEAN_HOSTILE_AUDIT_RESULT_PROGRESS_ONLY_GOAL_NOT_COMPLETE
```

Audited artifacts:

```text
docs/process/CARVER_S26_ZN_HOURLY_DATABENTO_BRIDGE_SHAPE_GATE_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_DATABENTO_TINY_INTAKE_EXECUTION_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_FORECAST_ONLY_HANDOFF_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_FORECAST_ONLY_PLUMBING_RESULT_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_SIGMA_PERCENT_SOURCE_GATE_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_REQUEST_MANIFEST_PLUMBING_RESULT_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_ROW_NORMALIZATION_PLUMBING_RESULT_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_REQUEST_MANIFEST_PLUMBING_LEAN_HOSTILE_AUDIT_2026-05-30.md
docs/process/CARVER_S26_ZN_HOURLY_DATABENTO_TINY_INTAKE_RESULT_2026-05-31.md
docs/process/CARVER_S26_ZN_HOURLY_DATABENTO_TINY_INTAKE_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_S26_ZN_HOURLY_G_R1B_SIGMA_HANDOFF_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S26_ZN_HOURLY_G_R1B_SIGMA_HANDOFF_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE_EXECUTION_GATE_DRAFT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/request_manifest/CARVER_S26_ZN_DATABENTO_OHLCV_1H_REQUEST_MANIFEST_2026-05-30.json
```

## Objective Audit

Active objective:

```text
Complete the next S26/S27 real-hourly-data bridge in five steps:
1. source-anchor ZN from the book;
2. define hourly Databento request shape;
3. lock hourly completed-bar semantics;
4. prepare a tiny authorized intake path;
5. feed quarantined ZN hourly bars into S26 forecast output only with no diagnostics/backtests/positions.
```

## Requirement Status

| Requirement | Status | Evidence |
| --- | --- | --- |
| Source-anchor ZN from the book | COMPLETE | S26 bridge shape anchors Fig. 81 p. 480 US 10-year future to `APPENDIX_C_172_004 / ZN` |
| Define hourly Databento request shape | COMPLETE / MACHINE-READABLE | `GLBX.MDP3`, `ohlcv-1h`, `instrument_id`, `42000661`, `ZNM6`, exact UTC envelope recorded and locked in request manifest |
| Lock hourly completed-bar semantics | COMPLETE FOR G_R1A TINY SLICE | `ts_event` preserved as interval start; completed-bar end = `ts_event + 1 hour`; observed ZN slice maps 23 rows into each completed trading date |
| Prepare tiny authorized intake path | COMPLETE AND EXECUTED FOR G_R1A | G_R1A execution preserved raw provider output, metadata, sanitized quarantine rows, validation, provenance, status, and hashes |
| Feed quarantined ZN hourly bars into S26 forecast output only | HANDOFF PLUMBING COMPLETE / FORECAST EXECUTION NOT COMPLETE | Source-locked forecast-only function exists and local tests pass; G_R1B handoff contract requires `PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE`; runtime-value execution gate draft exists; runtime `sigma_percent_t` value remains unavailable |

## Findings

### Critical

None. One bounded operator-authorized Databento G_R1A request was executed for `GLBX.MDP3 / ohlcv-1h / instrument_id 42000661 / 2026-05-17T00:00:00Z through 2026-05-23T00:00:00Z`. No artifact opens additional provider API access, additional data download, wider market-row parsing, real-data forecast execution, diagnostics, backtests, positions, costs, carry, trend, S27 overlay, deployment, trading, promotion, Git operations, or remote operations.

### High

None. The goal is not complete. The remaining blocker is a prevalidated runtime `sigma_percent_t` value, correctly preserved.

### Medium

M-1. The bridge has passed hourly price quarantine, but forecast output remains blocked.

The objective includes feeding quarantined ZN hourly bars into S26 forecast output. G_R1A has now passed as quarantine-only, but the objective cannot be honestly marked complete until:

```text
S26 sigma_percent_t runtime value with timestamp/no-lookahead provenance
```

is available for forecast-output use and G_R1B explicitly promotes rows from `QUARANTINE_ONLY_NOT_FORECAST_READY` to `S26_FORECAST_INPUT_READY_QUARANTINE_ONLY`.

Current local verification:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic
Ran 20 tests
OK

python -m unittest discover -s tests
Ran 175 tests
OK
```

This is not a process flaw; it is the correct boundary between preparation and data access.

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_PROGRESS_TOWARD_S26_ZN_HOURLY_BRIDGE_GOAL_G_R1A_COMPLETE_GOAL_NOT_COMPLETE
NEXT_REQUIRED_GATE: PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
THEN: G_R1B_ZN_S26_HOURLY_SIGMA_PERCENT_AND_FORECAST_ONLY_HANDOFF
```

## Non-Authorization

This audit authorizes no additional Databento access, no additional data download, no wider market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

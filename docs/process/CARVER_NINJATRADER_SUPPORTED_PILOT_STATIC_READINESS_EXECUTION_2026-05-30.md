# Carver NinjaTrader-Supported Pilot Static Readiness Execution

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_READINESS_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Execute the static readiness check for the selected 16-row NinjaTrader-supported pilot universe:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

The gate asks whether current Carver static artifacts are sufficient to mark any selected row:

```text
STATIC_READY_FOR_TINY_HISTORICAL_BAR_INTAKE
```

This is not a historical-bar intake gate. It does not authorize NinjaTrader export, provider API access, market-row parsing, diagnostics, backtests, deployment, trading, or promotion.

## Inputs

Pilot shape gate draft:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_UNIVERSE_SHAPE_STATIC_READINESS_GATE_DRAFT_2026-05-30.md
```

Contract identity static hardening update:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv
```

Session/roll/completed-bar readiness status:

```text
docs/researchops/session_roll/CARVER_APPENDIX_C_SESSION_ROLL_COMPLETED_BAR_READINESS_STATUS_2026-05-29.csv
```

Risk/FX/cost/carry-leg readiness status:

```text
docs/researchops/risk_fx_cost_carry_leg/CARVER_APPENDIX_C_RISK_FX_COST_CARRY_LEG_READINESS_STATUS_2026-05-29.csv
```

No market rows, historical bars, NinjaTrader historical exports, provider APIs, diagnostics, or backtests were used.

## Output

Machine-readable static readiness ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_READINESS_STATUS_2026-05-30.csv
Rows: 16
SHA256: 879705AC049C95C307344E49FEE75913875AF549A683F5273DDB665B51D1A514
```

## Row Preservation

```text
selected_rows: 16
output_rows: 16
unique_output_row_ids: 16
selected_row_id_set_preserved: YES
```

## Result

Final static readiness:

```text
STATIC_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 0
STATIC_READINESS_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
```

Upstream final-status checks:

```text
CONTRACT_IDENTITY_FAIL_CLOSED_NOT_LOCKED: 16
SESSION_ROLL_COMPLETED_BAR_FAIL_CLOSED_NOT_LOCKED: 16
RISK_FX_COST_CARRY_LEG_FAIL_CLOSED_NOT_LOCKED: 16
```

Boundary checks:

```text
NO_MARKET_ROW_ACCESS: 16
provider_api_accessed NO: 16
ninjatrader_historical_export_used NO: 16
diagnostics_or_backtests_run NO: 16
```

## Interpretation

No selected pilot row is ready for historical-bar intake using current static artifacts.

The selected pilot universe remains viable as a future source-native NinjaTrader branch, but the current static evidence is not sufficient for first data intake because:

- production contract identity is still `NOT_LOCKED` for all 16 selected rows;
- completed-bar policy is blocked for all 16 selected rows;
- roll rule evidence is blocked for all 16 selected rows;
- back-adjustment policy is blocked for all 16 selected rows;
- stale-bar, missing-bar, and alignment policies are blocked for all 16 selected rows;
- risk/FX/cost/carry-leg readiness is blocked downstream of session/roll/completed-bar readiness for all 16 selected rows.

The gate therefore fails closed before any market-row access.

## Selected Row Classes

Contract identity status among selected rows:

```text
CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY: 9
CONTRACT_IDENTITY_STATIC_UNRESOLVED_QUOTE_UNIT_LOCK_REQUIRED: 6
CONTRACT_IDENTITY_STATIC_UNRESOLVED_DELIVERY_CYCLE_LOCK_REQUIRED: 1
```

Session/roll/completed-bar status among selected rows:

```text
SESSION_ROLL_BLOCKED_NO_COMPLETED_BAR_POLICY: 16
```

Risk/FX/cost/carry-leg status among selected rows:

```text
RISK_FX_COST_CARRY_LEG_BLOCKED_SESSION_ROLL_COMPLETED_BAR: 16
```

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_EVIDENCE_PACKET
```

That gate should gather or define static policy evidence for the selected 16 rows only, without touching market rows:

- final contract identity locks;
- completed-bar timestamp policy;
- session calendar or trading-hours template interpretation;
- timezone and daily close policy;
- holiday and early-close policy;
- roll rule;
- back-adjustment policy;
- stale/missing-bar policy;
- alignment policy;
- risk/FX/cost/carry-leg policy evidence.

Only after a later static readiness execution produces at least one:

```text
STATIC_READY_FOR_TINY_HISTORICAL_BAR_INTAKE
```

should a separate operator decision consider authorizing a tiny NinjaTrader historical-bar intake pilot.

## Non-Authorization

This record authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

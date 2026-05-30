# Carver NinjaTrader-Supported Pilot Explicit Contract Month And Contract Identity Final Static Lock

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_EXPLICIT_CONTRACT_MONTH_CONTRACT_IDENTITY_FINAL_STATIC_LOCK_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Decide, or fail-close, explicit dated contract month selection and final static contract identity readiness for the selected 16-row NinjaTrader-supported pilot universe:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

This is a process/source static lock gate only. It does not authorize real market data, NinjaTrader historical export, provider API access, market-row parsing, diagnostics, backtests, trading, deployment, or promotion.

## Inputs

Static artifacts inspected:

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_2026-05-30.csv
```

No market rows, historical bars, NinjaTrader exports, provider APIs, diagnostics, or backtests were used.

## Output

Machine-readable final static lock ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_EXPLICIT_CONTRACT_MONTH_CONTRACT_IDENTITY_FINAL_STATIC_LOCK_2026-05-30.csv
```

SHA256:

```text
1502A0B83B65F91F77F97AD34AEC3523BB3C3B1B72D95F616915E9D5E9779608
```

## Row Preservation

```text
SELECTED_ROWS_EXPECTED: 16
SELECTED_ROWS_PRESERVED: 16
```

## Dimension-Level Decisions

The following static dimensions are locked for all 16 selected rows from current Carver static artifacts:

```text
VENUE_NORMALIZATION_LOCKED: 16
CURRENCY_NORMALIZATION_LOCKED: 16
MULTIPLIER_OR_QUOTE_UNIT_SEMANTICS_LOCKED: 16
POINT_TICK_RECONCILIATION_LOCKED: 16
CONTRACT_FAMILY_VARIANT_LOCKED: 16
LOCAL_CANONICAL_ID_PRESENT: 16
```

Delivery-cycle readiness remains incomplete:

```text
DELIVERY_CYCLE_LOCKED: 1
DELIVERY_CYCLE_FAIL_CLOSED: 15
```

Active/listed readiness remains closed:

```text
ACTIVE_LISTED_STATUS_LOCKED: 0
ACTIVE_LISTED_STATUS_FAIL_CLOSED: 16
```

## Explicit Contract Month Decision

No explicit dated contract month was selected for any row:

```text
EXPLICIT_DATED_CONTRACT_MONTH_SELECTED: 0
EXPLICIT_DATED_CONTRACT_MONTH_FAIL_CLOSED: 16
```

Reason:

- no authorized as-of date or target historical-bar intake window exists;
- no row-level roll or delivery-cycle application decision has been authorized;
- no market row or NinjaTrader historical export is authorized;
- choosing a dated contract without those constraints would create a silent intake assumption.

## Final Row-Level Result

```text
FINAL_STATIC_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 0
FINAL_STATIC_CONTRACT_IDENTITY_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
```

All 16 rows remain fail-closed for first historical-bar intake.

This is not a rejection of the 16-symbol pilot. It is a static readiness result: the pilot has useful static identity scaffolding, but it still lacks the final active/listed and explicit dated contract month locks needed before any historical-bar extraction.

## Still Closed

The following remain closed:

- real market data;
- NinjaTrader historical export;
- provider API access;
- market-row parsing;
- diagnostics;
- backtests;
- OOS, Lockbox, Forward;
- CFD adapters;
- old QuantLab active-pipeline use;
- tuning;
- deployment;
- trading;
- promotion;
- remote operations.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_FIRST_HISTORICAL_BAR_INTAKE_DECISION_GATE
```

That gate should decide whether to:

- keep the 16-row pilot blocked until a static active/listed and explicit-contract-month evidence source is named;
- reduce the pilot further to one or a few rows with a named as-of date and explicit dated contract-month selection rule;
- or authorize a tiny historical-bar intake pilot with an exact row set, exact dated contract(s), exact date window, and completed-bar parser boundary.

It must not smuggle diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, or promotion.

## Non-Authorization

This final static lock gate authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

# Carver NinjaTrader-Supported Pilot Static Policy Readiness Refresh

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Refresh the static readiness status for the selected 16-row NinjaTrader-supported pilot universe after the completed-bar and holiday-precedence policy decision.

Selected pilot rows:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

This is a process/source readiness refresh only. It does not authorize real market data, NinjaTrader historical export, provider API access, market-row parsing, diagnostics, backtests, trading, deployment, or promotion.

## Inputs

Policy decision:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_COMPLETED_BAR_HOLIDAY_PRECEDENCE_POLICY_DECISION_2026-05-30.md
```

Static ledgers:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_LEDGER_2026-05-30.csv
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_ROW_POLICY_LEDGER_2026-05-30.csv
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv
```

No market rows, historical bars, NinjaTrader exports, provider APIs, diagnostics, or backtests were used.

## Output

Machine-readable readiness refresh:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_2026-05-30.csv
```

SHA256:

```text
733B8F0ADBA8051DB6724CF4077CD4D322507DD76E841D4084751523C7F052BC
```

## Applied Policy Decisions

The refresh applies the following completed-bar and policy decisions to all 16 selected rows:

- canonical completed trading date equals the local NinjaTrader Trading Hours template `TradingDay`;
- local NinjaTrader template `TradingDay` is the first-intake row-level trading-date authority;
- local NinjaTrader template is the operational filter, while CME holiday and trading-hours evidence is a conflict check;
- future rows must use UTC end-of-bar timestamps aligned back to the local template `TradingDay`;
- first intake uses the NinjaTrader/provider-recorded daily bar close only, with official settlement reconciliation closed;
- stale, missing, duplicate, non-UTC, non-end-of-bar, future-session, and session-misaligned rows fail closed.

## Refresh Result

Row preservation:

```text
SELECTED_ROWS_EXPECTED: 16
SELECTED_ROWS_PRESERVED: 16
```

Readiness:

```text
STATIC_POLICY_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 0
STATIC_POLICY_READINESS_REFRESH_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
```

All 16 rows remain fail-closed. The policy ambiguity is reduced, but no row is ready for historical-bar intake because the remaining blockers are still material:

- production contract identity is not locked;
- explicit dated contract month has not been selected;
- CME conflict checks cannot be evaluated without an authorized intake date/window;
- no market-row access is authorized;
- no NinjaTrader historical export is authorized.

## Boundary Status

For every refreshed row:

```text
market_row_access_status: NO_MARKET_ROW_ACCESS
provider_api_accessed: NO
ninjatrader_historical_export_used: NO
diagnostics_or_backtests_run: NO
substitution_status: FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
```

No row was dropped, substituted, reweighted, promoted, or treated as executable.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_EXPLICIT_CONTRACT_MONTH_AND_CONTRACT_IDENTITY_FINAL_STATIC_LOCK_GATE
```

That gate should decide, or fail-close, the explicit dated contract month and final static contract identity readiness for the 16 selected rows using only static source/provider evidence. It must not export NinjaTrader historical data, parse market rows, access provider APIs, run diagnostics, or run backtests.

Only after at least one row is statically ready should the operator consider a separate tiny historical-bar intake pilot.

## Non-Authorization

This refresh authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

# Carver NinjaTrader-Supported Pilot Completed-Bar And Holiday-Precedence Policy Decision

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_COMPLETED_BAR_HOLIDAY_PRECEDENCE_POLICY_DECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Decide, or fail-close, the completed-bar and holiday-precedence policy for the selected 16-row NinjaTrader-supported pilot universe:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

This is a process/source policy decision only. It does not authorize real market data, NinjaTrader historical export, provider API access, market-row parsing, diagnostics, backtests, trading, deployment, or promotion.

## Inputs

Trading-hours template evidence intake:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_TEMPLATE_STATIC_EVIDENCE_INTAKE_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_TEMPLATE_EVIDENCE_2026-05-30.csv
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_ROW_POLICY_LEDGER_2026-05-30.csv
```

Prior static policy evidence execution:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_EVIDENCE_INTAKE_EXECUTION_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_LEDGER_2026-05-30.csv
```

Official static policy references:

```text
https://ninjatrader.com/support/helpguides/nt8/trading_hours.htm
https://ninjatrader.com/support/helpguides/nt8/using_the_trading_hours_window.htm
https://ninjatrader.com/support/helpguides/nt8/how_bars_are_built.htm
https://ninjatrader.com/support/helpguides/nt8/bar_types.htm
https://ninjatrader.com/support/helpguides/nt8/exporting.htm
https://www.cmegroup.com/trading-hours.html
https://www.cmegroup.com/market-data/daily-settlements.html
https://www.cmegroup.com/trading/about-settlements.html
```

No market rows, historical bars, NinjaTrader exports, provider APIs, diagnostics, or backtests were used.

## Evidence Summary

Local static NinjaTrader Trading Hours templates were extracted for all 16 selected rows.

Observed template families:

```text
CBOT Interest Rate ETH
CME US Index Futures ETH
Nymex Metals - Energy ETH
CBOT Agriculturals ETH
CME Commodities ETH
```

Extracted fields include:

- template timezone;
- regular session begin day/time;
- regular session end day/time;
- regular session `TradingDay`;
- local full-holiday definitions;
- local partial-holiday definitions;
- local early-end/late-begin flags where present.

The extraction does not include a separate explicit EOD field. It does include a `TradingDay` field on each regular session.

## Decisions

### Decision 1: Canonical Completed Trading Date

Decision:

```text
FIRST_INTAKE_CANONICAL_COMPLETED_TRADING_DATE_EQUALS_LOCAL_NINJATRADER_TEMPLATE_TRADINGDAY
```

For the future first historical-bar intake pilot only, the canonical completed trading date is the local NinjaTrader Trading Hours template `TradingDay` associated with the completed session that produced the bar.

Reason:

- the local NinjaTrader Trading Hours XML provides a `TradingDay` field for all extracted regular sessions;
- NinjaTrader static documentation describes Trading Hours templates as session definitions used by the platform;
- this policy follows the practical source-native data source branch rather than inventing a separate calendar.

Boundary:

This does not authorize treating any bar as complete. A future intake must still verify that each exported row timestamp maps to exactly one completed local template session and one `TradingDay`.

### Decision 2: Row-Level Trading-Date Authority

Decision:

```text
LOCAL_NINJATRADER_TEMPLATE_TRADINGDAY_IS_FIRST_INTAKE_ROW_LEVEL_TRADING_DATE_AUTHORITY
```

For the first price-bar intake pilot, the local NinjaTrader template `TradingDay` is the row-level trading-date authority, provided that:

- the row's template file hash matches the extracted static evidence ledger;
- the row's timestamp is an end-of-bar timestamp;
- the timestamp falls within one and only one template session or permitted partial-holiday session;
- no CME holiday/early-close cross-check conflict is present.

If any condition fails, the affected row and date fail closed.

### Decision 3: CME Versus Local Holiday Precedence

Decision:

```text
LOCAL_NINJATRADER_TEMPLATE_IS_OPERATIONAL_FILTER_CME_HOLIDAY_PAGE_IS_CONFLICT_CHECK
```

For the first price-bar intake pilot:

- local NinjaTrader full holidays and partial holidays are the operational template filter because they are the actual static configuration used by the local data source branch;
- CME Group holiday/trading-hours pages are a source-native conflict check;
- if the local template and CME Group static holiday/trading-hours evidence conflict for a selected instrument/date, the row/date fails closed;
- no row may be accepted by choosing the more convenient of local NinjaTrader or CME evidence after seeing data.

This policy avoids silently overriding the local source-native data source while still requiring exchange-source consistency.

### Decision 4: UTC End-Of-Bar Alignment

Decision:

```text
FUTURE_NINJATRADER_EXPORT_ROWS_MUST_BE_UTC_END_OF_BAR_TIMESTAMPS_ALIGNED_TO_LOCAL_TEMPLATE_TRADINGDAY
```

NinjaTrader static documentation identifies exported historical rows as end-of-bar timestamped and UTC. A future intake parser, if separately authorized, must therefore:

- require UTC timestamps;
- require end-of-bar interpretation;
- map each UTC timestamp back through the extracted template timezone and session definition;
- assign the local template `TradingDay`;
- reject ambiguous, duplicate, naive, non-UTC, intraday-incomplete, future-session, or session-misaligned rows.

No parser or export is authorized by this decision.

### Decision 5: Daily Close Versus Settlement

Decision:

```text
FIRST_PRICE_BAR_INTAKE_USES_NINJATRADER_PROVIDER_RECORDED_DAILY_BAR_CLOSE_ONLY_OFFICIAL_SETTLEMENT_VALIDATION_CLOSED
```

For the first tiny historical-bar intake pilot, the close field is interpreted only as the NinjaTrader/provider-recorded daily bar close supplied through the platform. Official CME settlement is not used as a replacement, correction, validation target, or performance evidence in the first intake pilot.

Reason:

- NinjaTrader static documentation notes that daily bars are governed by provider-recorded data and may use official settlement where provider support exists;
- CME settlement pages define official settlement concepts, but using them to validate or correct provider daily bars would be a separate reconciliation gate;
- the first intake chapter is about safe source-native bar intake, not settlement reconciliation.

Boundary:

If the future operator wants settlement reconciliation, it must be separately gated.

### Decision 6: Stale And Missing Bar Policy

Decision:

```text
STRICT_FAIL_CLOSED_STALE_AND_MISSING_BAR_POLICY_FOR_FIRST_INTAKE
```

For the future first intake pilot:

- missing expected completed trading dates fail the row/date closed unless the date is a full holiday or explicitly non-trading day in the extracted local template and does not conflict with CME static holiday evidence;
- partial-holiday dates are permitted only if the extracted local template defines the partial-holiday session and no CME conflict is present;
- duplicate rows for the same row ID and completed trading date fail closed;
- stale rows, future rows, non-monotonic rows, non-UTC rows, non-end-of-bar rows, and rows outside the extracted template session fail closed;
- no imputation, forward-fill, substitution, reweighting, or calendar repair is allowed.

### Decision 7: Historical-Bar Intake Readiness

Decision:

```text
POLICY_DECISION_COMPLETE_BUT_HISTORICAL_BAR_INTAKE_NOT_AUTHORIZED
```

This decision reduces policy ambiguity, but it does not make the 16-row pilot ready for data intake by itself.

The pilot remains blocked until a later readiness refresh confirms:

- row identities are still preserved;
- template hashes match the extracted static ledgers;
- explicit dated contract-month selection is decided;
- current static policy ledgers are updated with these decisions;
- at least one row is marked ready by a separate process/source readiness gate;
- the operator separately authorizes the tiny historical-bar intake pilot.

## Row-Level Effect

This policy applies to all selected rows:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

The immediate row-level status remains:

```text
READY_FOR_HISTORICAL_BAR_INTAKE: 0
FAIL_CLOSED_PENDING_READINESS_REFRESH: 16
```

No row is promoted to executable readiness by this document.

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
NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_GATE
```

That gate should create a machine-readable readiness refresh for the 16 selected rows using current static ledgers and this decision artifact. It should mark whether each row is ready or fail-closed after applying:

- canonical completed trading-date policy;
- local-template/CME conflict policy;
- UTC end-of-bar alignment policy;
- daily-close provider-close-only policy;
- strict stale/missing policy.

It must not export historical bars, parse market rows, access provider APIs, run diagnostics, or run backtests.

Only if that refresh marks at least one row:

```text
STATIC_POLICY_READY_FOR_TINY_HISTORICAL_BAR_INTAKE
```

should a separate operator decision consider a tiny historical-bar intake pilot.

## Non-Authorization

This decision authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

# Carver NinjaTrader-Supported Pilot Trading-Hours Template Static Evidence Intake

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_TEMPLATE_STATIC_EVIDENCE_INTAKE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Extract or fail-close local static NinjaTrader Trading Hours template evidence for the selected 16-row NinjaTrader-supported pilot universe:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

This gate inspects only static local NinjaTrader configuration evidence and official static NinjaTrader/CME policy references. It does not inspect historical bars, export data from NinjaTrader, access provider APIs, parse market rows, run diagnostics, or run backtests.

## Inputs

Current Carver policy execution:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_EVIDENCE_INTAKE_EXECUTION_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_LEDGER_2026-05-30.csv
```

Local static NinjaTrader configuration source:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\templates\TradingHours\CBOT Interest Rate ETH.xml
C:\Users\openclaw\Documents\NinjaTrader 8\templates\TradingHours\CME US Index Futures ETH.xml
C:\Users\openclaw\Documents\NinjaTrader 8\templates\TradingHours\Nymex Metals - Energy ETH.xml
C:\Users\openclaw\Documents\NinjaTrader 8\templates\TradingHours\CBOT Agriculturals ETH.xml
C:\Users\openclaw\Documents\NinjaTrader 8\templates\TradingHours\CME Commodities ETH.xml
```

Official static policy references:

```text
https://ninjatrader.com/support/helpguides/nt8/trading_hours.htm
https://ninjatrader.com/support/helpguides/nt8/using_the_trading_hours_window.htm
https://ninjatrader.com/support/helpguides/nt8/how_bars_are_built.htm
https://ninjatrader.com/support/helpguides/nt8/exporting.htm
https://www.cmegroup.com/trading-hours.html
```

## Outputs

Template-level evidence ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_TEMPLATE_EVIDENCE_2026-05-30.csv
Rows: 5
SHA256: A2B0151C8069C5C07ADF1275D10C45F9C7D870F2AFA877EE7E54D5BC28F4ED48
```

Row-level policy ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_ROW_POLICY_LEDGER_2026-05-30.csv
Rows: 16
SHA256: 34C31FFB12AFCE834CAD4FA83DAADC391B7AF2EF4197F77E9EC9B05A34037D7C
```

## Local Template Evidence Extracted

Observed templates:

```text
CBOT Interest Rate ETH
CME US Index Futures ETH
Nymex Metals - Energy ETH
CBOT Agriculturals ETH
CME Commodities ETH
```

For each observed template, the ledger extracts:

- local XML source path;
- local XML SHA256;
- NinjaTrader template version;
- template name;
- timezone;
- session count;
- session definitions with begin day/time, end day/time, and TradingDay;
- full holiday count and coverage range;
- partial holiday count and coverage range;
- sample partial-holiday definitions;
- no-market-row/no-export boundary flags.

## Static Evidence Result

The intake partially improves the static policy layer:

```text
LOCAL_TRADING_HOURS_TEMPLATE_STATIC_EVIDENCE_EXTRACTED: 16
```

But the row-level status remains fail-closed:

```text
TRADING_HOURS_TEMPLATE_EVIDENCE_PARTIAL_FAIL_CLOSED_NOT_READY_FOR_HISTORICAL_BAR_INTAKE: 16
```

No selected row is ready for historical-bar intake.

## What Is Resolved

The following are now extracted from local static NinjaTrader template XML:

- template file identity;
- template file hash;
- template timezone;
- regular session definitions;
- TradingDay fields on regular sessions;
- local full-holiday definitions;
- local partial-holiday definitions;
- local early-end/late-begin flags where present.

This is better than the prior state, where only the template names were preserved from the static provider master.

## What Remains Fail-Closed

The following remain unresolved:

```text
separate explicit EOD marker:
  The inspected XML records session begin/end and TradingDay fields, but no separate explicit EOD field was observed.

CME/local holiday precedence:
  Local NinjaTrader template holiday and partial-holiday definitions are extracted, but precedence versus CME Group holiday/trading-hours pages is not locked.

canonical completed trading-date policy:
  TradingDay fields are extracted, but the canonical Carver trading-date alignment rule is not yet locked.

UTC end-of-bar timestamp alignment:
  NinjaTrader static documentation identifies end-of-bar timestamps and UTC historical export timestamps, but no export is authorized and no row is intake-ready.

daily close/settlement policy:
  The gate does not decide whether a future daily bar close is provider daily close, official exchange settlement, or blocked.

stale/missing bar policy:
  The gate does not decide how a future ledger treats missing rows, provider outages, exchange holidays, partial holidays, or stale bars.
```

## Interpretation

This is progress toward first real-data intake readiness, but not a data gate.

The Carver pilot can now point to concrete local NinjaTrader template XML for the five templates used by the 16 pilot rows. However, source-native readiness still requires a separate policy decision before any historical-bar intake:

- define canonical completed trading date;
- define local-vs-CME holiday precedence;
- define UTC timestamp alignment;
- define daily close/settlement policy;
- define stale/missing bar treatment.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_COMPLETED_BAR_AND_HOLIDAY_PRECEDENCE_POLICY_GATE
```

That gate should create a process/source decision artifact that chooses or fail-closes:

- canonical completed trading-date interpretation;
- whether the local NinjaTrader TradingDay field is the row-level trading-date authority for first intake;
- precedence between local NinjaTrader holidays/partial holidays and CME Group trading-hours/holiday pages;
- UTC end-of-bar timestamp alignment rule;
- daily close versus settlement policy for the first price-bar pilot;
- stale/missing bar policy.

It must not export historical data, parse market rows, use provider APIs, run diagnostics, or run backtests.

## Non-Authorization

This record authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

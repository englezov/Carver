# Carver NinjaTrader Manifest ZN Daily Export Execution Gate

Date: 2026-05-29

Status:

```text
CARVER_NINJATRADER_MANIFEST_ZN_DAILY_EXPORT_EXECUTION_AUTHORIZED_NOT_BACKTEST_NOT_DIAGNOSTIC
```

## Operator Authorization

The operator authorized exactly one NinjaTrader Desktop manifest export execution for the Carver ZN daily chain.

Allowed helper:

```text
tools/nt8/CarverManifestDailyExporter.cs
```

Allowed manifest rows:

```text
ZN SEP25
ZN DEC25
ZN MAR26
ZN JUN26
```

Allowed output root:

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports
```

## File Placement

The audited helper was copied to NinjaTrader's custom indicator folder:

```text
source: C:\Users\openclaw\Desktop\Carver\tools\nt8\CarverManifestDailyExporter.cs
target: C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\CarverManifestDailyExporter.cs
sha256: 4F1532B38E57E0276B4A7A6AC2ABCA878D73DA2133186157E76BFD80154C1699
```

The target hash matched the source hash after copy.

After the first copy, the helper was patched to fully qualify `NinjaTrader.Cbi.Instrument.GetInstrument(...)` to reduce NinjaScript compile ambiguity risk. The hash above is the post-patch hash present in both source and target.

## Delta Hostile Check

A subagent hostile-audit follow-up reviewed the one-line helper patch and confirmed:

```text
PRIOR_VERDICT_STANDS_PROCESS_SAFE_FOR_HELPER_GATE_DELTA_NOT_EXECUTION_PROOF
```

The delta audit found no new blocker and confirmed the helper still defaults disarmed, returns before requests while disarmed, remains locked to the four ZN rows, writes only to `native_daily_exports`, and contains no strategy/backtest/diagnostic/account/order/PnL/Sharpe/OOS/Lockbox/Forward/CFD/old QuantLab/trading/deployment/promotion leakage.

## Execution State

At the time this gate file was created:

```text
helper copied: yes
NinjaTrader compile confirmed: no
ExecutionArmed=true run confirmed: no
export files confirmed: no
parser validation confirmed: no
```

## Expected Output Files

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports\ZN\ZN 09-25.Last.txt
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports\ZN\ZN 12-25.Last.txt
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports\ZN\ZN 03-26.Last.txt
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports\ZN\ZN 06-26.Last.txt
```

## Forbidden

This gate authorizes no strategy computation, no continuous stitching, no roll/back-adjustment, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

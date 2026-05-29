# Carver NinjaTrader Manifest Daily Export Helper Gate

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_MANIFEST_DAILY_EXPORT_HELPER_IMPLEMENTED_NOT_RUN_NOT_BULK_DOWNLOAD
```

## Purpose

Build the NinjaTrader Desktop end of the manifest-driven source-native futures acquisition layer, without executing a download.

This replaces the one-chart `ZN JUN26` pain point with a prepared helper that can later request the manifest-declared ZN chain:

```text
ZN SEP25
ZN DEC25
ZN MAR26
ZN JUN26
```

## Implemented Surface

Python manifest-to-export-plan contract:

```text
src/carver/spine/data_acquisition.py
```

NinjaTrader helper artifact:

```text
tools/nt8/CarverManifestDailyExporter.cs
```

Synthetic tests:

```text
tests/test_data_acquisition_synthetic.py
```

## Source API Basis

NinjaTrader's official `BarsRequest` documentation says a request can be constructed for an instrument and date range, parametrized with a `BarsPeriod`, and requested with a callback. It also warns that the last returned bar may be in progress and that callers must manage their own update/request logic.

Official references:

- <https://ninjatrader.com/support/helpguides/nt8/barsrequest.htm>
- <https://ninjatrader.com/support/helpguides/nt8/request.htm>

The helper uses this only as a data-export mechanism. It contains no strategy, signal, account, order, position, PnL, or performance logic.

## Helper Behavior

The helper is an indicator-style NinjaScript artifact because that is the easiest operator path in NinjaTrader Desktop.

Default state:

```text
ExecutionArmed = false
```

When imported or attached while disarmed, it only prints that it is prepared and does not request data.

Future separately authorized run behavior:

- validate locked manifest id;
- validate output root:

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports
```

- request daily `Last` bars for the four declared ZN contracts only;
- write NinjaTrader-native semicolon text rows:

```text
YYYYMMDD;open;high;low;close;volume
```

- write only to:

```text
data/quarantine/ninjatrader/native_daily_exports/ZN/
```

Expected files:

```text
ZN/ZN 09-25.Last.txt
ZN/ZN 12-25.Last.txt
ZN/ZN 03-26.Last.txt
ZN/ZN 06-26.Last.txt
```

## Explicit Non-Authorization

This gate authorizes no helper import, no NinjaTrader compile, no chart attachment, no `ExecutionArmed = true`, no bulk export/download execution, no parser run on real files, no continuous roll/back-adjustment construction, no strategy computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

## Next Gate

Before any real run:

1. hostile-audit the helper artifact and tests;
2. optionally copy the helper into NinjaTrader's custom indicator folder;
3. compile in NinjaTrader Desktop;
4. only then open a separate operator execution gate for `ExecutionArmed = true`.

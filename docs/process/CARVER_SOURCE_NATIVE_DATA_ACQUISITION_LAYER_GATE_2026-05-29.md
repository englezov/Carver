# Carver Source-Native Data Acquisition Layer Gate

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_DATA_ACQUISITION_LAYER_IMPLEMENTED_NOT_BULK_DOWNLOAD_NOT_DIAGNOSTIC
```

## Purpose

Create the first manifest-driven source-native futures data acquisition layer for Carver book data, with the first practical focus on daily futures data for Parts One-Three and S09 ZN continuous-readiness.

This gate responds to the operator conclusion that manual one-contract exports are not enough for the book. `ZN JUN26` exported only a short outright history and cannot supply the 257 completed daily bars required for the S09 EWMAC64 warm-up boundary.

## Implemented Surface

Manifest/config seed:

```text
config/carver_daily_futures_manifest_parts_1_3_seed.json
```

Python contracts and validators:

```text
src/carver/spine/data_acquisition.py
```

Synthetic tests:

```text
tests/test_data_acquisition_synthetic.py
```

The acquisition layer is execution-free. It creates request/manifest objects, quarantine paths, and native NinjaTrader text-export parsing/validation. It does not click NinjaTrader, run bulk downloads, compute a continuous series, compute a strategy, or compute performance.

## Seed Manifest

The seed manifest declares the daily source-native roots needed by the first portfolio spine and initial daily-stack work:

```text
MES  S&P 500 micro future
ZN   US 10-year bond future
ZF   US 5-year bond future
QM   WTI Crude Oil mini future
ZC   Corn future
MGC  Gold micro future
```

The first export chain is ZN continuous-readiness:

```text
ZN SEP25
ZN DEC25
ZN MAR26
ZN JUN26
```

Each request is daily `Last`, start date `2025-05-29`, end date `2026-05-28`, with files expected under:

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports\ZN\
```

The minimum continuous-readiness target is:

```text
257 completed daily bars
```

This does not authorize stitching those contracts into a continuous series. Roll/back-adjustment remains separately blocked by M0/continuous-series rules.

## Native NinjaTrader Export Shape

NinjaTrader's built-in historical export writes semicolon text rows shaped as:

```text
YYYYMMDD;open;high;low;close;volume
```

The Carver parser binds identity from the locked export request and file path because the native rows do not include symbol identity.

Parser entry is manifest-bound. A native export request must be declared in the active acquisition manifest before any rows are parsed. The JSON seed manifest is also checked against the code-built manifest in tests so config drift fails closed.

Validation requires:

- source-native lane only;
- declared futures root in the manifest;
- `Day` interval;
- `Last` data type;
- exact NinjaTrader symbol matching the contract month, e.g. `ZN JUN26`;
- exact platform filename matching the request, e.g. `ZN 06-26.Last.txt`;
- file under the Carver native-daily quarantine;
- completed date-aligned UTC daily bars;
- finite positive OHLC;
- finite non-negative volume;
- strict increasing dates;
- no duplicate dates;
- no rows outside the locked request date range.

## Quarantine Layout

```text
data/quarantine/ninjatrader/native_daily_exports/<ROOT>/<ROOT> <MM-YY>.Last.txt
```

Example:

```text
data/quarantine/ninjatrader/native_daily_exports/ZN/ZN 06-26.Last.txt
```

The `data/` tree remains Git-ignored.

## Explicit Blockages

Still blocked after this gate:

- bulk export/download execution;
- continuous roll/back-adjustment construction;
- strategy computation;
- S09 forecast run on real data;
- diagnostics/backtests/performance;
- OOS/Lockbox/Forward;
- CFD adapter work;
- old QuantLab imports;
- tuning;
- deployment/trading/promotion.

## Next Gate

The next gate should authorize one of:

1. A narrow manual export placement for the four ZN chain files into the native-daily quarantine, followed by parser-only validation; or
2. A NinjaTrader Desktop helper that exports a manifest row or manifest batch, with hostile audit before any run.

No real data run is authorized by this gate.

## Non-Authorization

This gate authorizes no bulk data download execution, no strategy computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

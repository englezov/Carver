# Carver Phase-1 MES/ZN/ZF Continuous Readiness Report Surface

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_PHASE1_CONTINUOUS_READINESS_REPORT_SURFACE_NOT_DATA_NOT_DIAGNOSTIC
```

## Purpose

Prepare the report surface that will prove continuous-readiness for the first phase-1 multi-asset seed roots after their NinjaTrader daily exports exist.

Phase-1 roots:

```text
MES
ZN
ZF
```

This surface does not run NinjaTrader, export data, compute forecasts, compute returns, or run diagnostics.

## Implemented Surface

Code:

```text
src/carver/spine/data_acquisition.py
```

Public objects:

```text
Phase1ContinuousReadinessSummary
Phase1ContinuousReadinessReport
build_phase1_continuous_readiness_report
render_phase1_continuous_readiness_markdown
```

The report covers exactly:

```text
MES, ZN, ZF
```

in that order.

## Behavior

For each root, the report attempts to build continuous-readiness from the phase-1 manifest and native daily quarantine files. It records:

```text
root
ready flag
adjusted row count
minimum row count
first date
last date
source contract months
blockers
```

If a root is missing files or has too few rows, the report records a blocker for that root rather than treating the whole phase-1 package as silently ready.

The readiness surface does not commit raw market rows.

## Why This Matters

The active portfolio-construction bridge requires continuous-readiness for each seed instrument before multi-instrument S09 forecast conformance.

This report is the bridge between:

```text
NinjaTrader phase-1 export helper
-> parser-only validation
-> root-filtered continuous readiness
-> S09 multi-instrument conformance
```

## Verification

```text
python -m unittest tests.test_continuous_synthetic -v
```

Full-suite verification and hostile audit are required before local commit.

## Non-Authorization

This artifact authorizes no NinjaTrader execution, no bulk data download execution, no data export, no strategy computation, no returns, no PnL, no Sharpe, no drawdown, no hit rate, no costs, no turnover, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

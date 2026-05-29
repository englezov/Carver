# Carver S09 Real-Data Readiness Gate

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S09_REAL_DATA_READINESS_GATE_NOT_DATA_NOT_BACKTEST
```

## Purpose

Define the artifact-bound readiness checks required before any future S09 real-data execution.

This gate does not execute real data. It records the shape of the readiness contract only:

```text
source-native contract identity
-> exact provider mapping
-> direct daily intake route
-> completed daily session convention
-> roll/back-adjustment rules
-> daily price-risk source
-> eligible EWMAC speed-set source
-> S09/M2 synthetic forecast code
```

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` work is opened.

## Direct-Daily Intake

S09 real-data readiness defaults to:

```text
DIRECT_DAILY_PRIMARY
```

Minute-derived fallback remains blocked unless a separate direct-daily-blocked artifact is attached to the intake route.

## First Provider-Mapping Posture

The current locked Web Chart provider registry contains only:

```text
ZN 06-26 ZN JUN26 -> 4470301
```

`MES` remains unresolved for S09 readiness. No `ES` substitution is allowed.

## Artifact Locks Required

Before any future S09 real-data execution, each instrument must have repo-local markdown artifacts for:

- provider mapping;
- direct-daily intake route;
- session calendar/timezone and completed daily cut;
- roll rule;
- back-adjustment rule;
- daily price-risk source;
- eligible EWMAC speed set.

The eligible speed set must match one of the source-locked S09 Table 36 rows. The unresolved `0.15 SR` speed/cost citation is still not treated as solved by this gate; readiness can only consume an already locked eligible speed-set artifact.

## Non-Authorization

This gate authorizes no real data/API/WebSocket access, no NinjaTrader export, no market-row parsing, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

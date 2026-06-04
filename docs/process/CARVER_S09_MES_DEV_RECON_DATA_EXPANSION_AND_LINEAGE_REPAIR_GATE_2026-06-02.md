# Carver S09 MES Dev/Reconciliation Data Expansion And Lineage Repair Gate

Date: 2026-06-02

Status:

```text
PROCESS_SOURCE_S09_MES_DATABENTO_DAILY_EXPANSION_AUTHORIZED_NOT_BACKTEST
```

## Purpose

Open the next bounded gate after:

```text
docs/process/CARVER_S09_MES_SINGLE_INDEX_ROOT_CONTINUOUS_LINEAGE_AND_COST_ELIGIBILITY_PREFLIGHT_2026-06-02.md
```

The prior preflight selected `MES` for the first S09 index-root path and failed closed because the local artifacts only held a current 2026 dated-contract fragment, not a complete Development/Reconciliation input.

This gate authorizes only the minimum Databento daily expansion needed to repair the MES dated-contract evidence surface for a future S09 continuous-lineage attempt.

## Operator Authorization

Operator authorization:

```text
Operator Authorizes DataBento API access if needed at this stage.
```

Interpretation:

```text
DATABENTO_ACCESS_ALLOWED_ONLY_FOR_S09_MES_DAILY_EXPANSION_GATE
```

This is not a blanket provider lane and does not authorize S09 forecast computation or backtesting.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

No CFD assumptions, CFD symbols, CFD costs, CFD sessions, or old `QuantLab_v3` active-pipeline state may be used.

## Locked Request

Provider:

```text
DATABENTO_HISTORICAL
```

Dataset/schema:

```text
GLBX.MDP3
ohlcv-1d
raw_symbol
```

Root:

```text
MES
```

Target Development/Reconciliation comparison window:

```text
2022-01-03 through 2023-12-29
```

Request/warmup envelope:

```text
2021-01-01T00:00:00Z through 2024-01-01T00:00:00Z
```

Required dated contracts:

```text
MESH1
MESM1
MESU1
MESZ1
MESH2
MESM2
MESU2
MESZ2
MESH3
MESM3
MESU3
MESZ3
MESH4
```

Allowed metadata:

```text
Databento dataset-condition metadata
Databento symbology resolution
Databento definition schema cross-check
```

No continuous-contract symbol, provider-built continuous series, ES/NQ substitution, additional root, additional schema, or wider request window is authorized by this gate.

## Required Artifacts

Create artifacts under:

```text
docs/researchops/s09/mes_dev_recon_data_expansion/2022-01-03_2023-12-29/
```

Required artifact classes:

- request manifest;
- raw provider DBN/CSV output for each requested dated contract;
- raw provider metadata, symbology, definition, and dataset-condition records;
- sanitized daily quarantine OHLCV rows;
- row-shape/date/duplicate/provider-condition validation records;
- provenance/status/hash records.

## Validation Boundary

Allowed checks:

- raw-symbol resolution;
- provider row count;
- finite OHLCV fields;
- high/low/open/close shape;
- non-negative volume;
- duplicate timestamp detection per raw symbol;
- dataset-condition classification by provider date;
- zero silent drop: every excluded row must carry an explicit condition or blocker status.

Forbidden checks:

- S09 forecast computation;
- EWMAC computation;
- price-risk computation;
- cost computation;
- speed eligibility decision;
- position sizing;
- returns, PnL, Sharpe, drawdown, diagnostics, or backtest.

## Expected Result

Pass result:

```text
PASS_S09_MES_DAILY_EXPANSION_QUARANTINE_ONLY_NOT_LINEAGE_NOT_BACKTEST
```

Fail result:

```text
FAIL_CLOSED_S09_MES_DAILY_EXPANSION_BLOCKED
```

Either result remains Development/Reconciliation only and is not strategy-ready.

## Required Next Gate After This One

If the data expansion succeeds, the next gate remains separate:

```text
S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_EXECUTION_GATE
```

That later gate must still lock or fail-close:

- lifecycle/roll evidence;
- local continuous lineage construction;
- additive back-adjustment;
- daily annual percentage risk runtime;
- cost source and risk-adjusted cost per trade;
- S09 speed/cost eligibility;
- strategy-facing input creation.

## Non-Authorization

This gate authorizes no provider access outside the exact Databento request above, no additional symbols, no additional contracts, no additional schemas, no continuous-contract download, no market-row use outside quarantine expansion/validation, no real-data forecast computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no costs, no carry, no CFD adapter work, no old QuantLab pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update, and no remote repository operations.

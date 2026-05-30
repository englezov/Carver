# Databento 16-Symbol Dated-Contract Full-History Daily OHLCV Quarantine Archive Provenance

Date: 2026-05-30

Status:

```text
FAIL_CLOSED_DATABENTO_FULL_HISTORY_REQUEST_OR_VALIDATION_ERROR
```

## Request

```text
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1d
definition schema: definition
stype_in: raw_symbol
stype_out: instrument_id
symbols: ZTM6, ZFM6, ZNM6, MESM6, MNQM6, M2KM6, MYMM6, QMN6, RBN6, ZCN6, ZSN6, ZMN6, ZLN6, ZWN6, HEM6, LEM6
start: 2018-01-01T00:00:00Z
end: 2026-05-30T00:00:00Z
```

The wide start is used only to capture provider-available individual dated-contract history for the exact locked symbols. No continuous contracts were requested.

## Boundaries

Quarantine-only market-row parsing was performed only on the exact provider output from this request. No diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk calculations, OOS, Lockbox, Forward, CFD adapter work, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update, or remote repository operation was performed.

## Secret Handling

The Databento API key was read from the local desktop key file and was not printed or recorded in any artifact.

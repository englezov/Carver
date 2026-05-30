# Databento 16-Symbol Daily OHLCV Quarantine Intake Provenance

Date: 2026-05-30

Status:

```text
PASS_EXACT_16_SYMBOL_5_DAILY_ROWS_QUARANTINE_ONLY
```

## Request

```text
dataset: GLBX.MDP3
schema: ohlcv-1d
stype_in: raw_symbol
stype_out: instrument_id
symbols: ZTM6, ZFM6, ZNM6, MESM6, MNQM6, M2KM6, MYMM6, QMN6, RBN6, ZCN6, ZSN6, ZMN6, ZLN6, ZWN6, HEM6, LEM6
start: 2026-05-18T00:00:00Z
end: 2026-05-23T00:00:00Z
```

## Boundaries

Quarantine-only market-row parsing was performed only on the exact provider output from this request. No diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk calculations, OOS, Lockbox, Forward, CFD adapter work, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update, or remote repository operation was performed.

## Secret Handling

The Databento API key was read from the local desktop key file and was not printed or recorded in any artifact.

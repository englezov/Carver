# Carver Databento 16-Symbol Daily OHLCV Quarantine Intake Execution Pass

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_DATABENTO_16_SYMBOL_DAILY_OHLCV_QUARANTINE_INTAKE_EXECUTION_PASS_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the successful bounded Databento Historical quarantine intake for the locked 16-symbol dated futures daily pilot.

This follows:

```text
docs/process/CARVER_DATABENTO_16_SYMBOL_DAILY_FUTURES_QUARANTINE_INTAKE_SHAPE_GATE_DRAFT_2026-05-30.md
```

It supersedes only the earlier Databento authentication-fail result for this same locked request. It does not supersede any broader provider, full-history, strategy, diagnostic, or backtest gate.

## Authorized Request

```text
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1d
stype_in: raw_symbol
stype_out: instrument_id
symbols: ZTM6, ZFM6, ZNM6, MESM6, MNQM6, M2KM6, MYMM6, QMN6, RBN6, ZCN6, ZSN6, ZMN6, ZLN6, ZWN6, HEM6, LEM6
start: 2026-05-18T00:00:00Z
end: 2026-05-23T00:00:00Z
```

## Execution Result

Result:

```text
PASS_EXACT_16_SYMBOL_5_DAILY_ROWS_QUARANTINE_ONLY
```

Observed summary:

```text
PROVIDER_API_ACCESSED: YES
DATA_DOWNLOADED: YES
MARKET_ROWS_PARSED: YES_QUARANTINE_ROW_SHAPE_ONLY
ACCEPTED_MARKET_ROWS: 80
SYMBOLS_VALIDATED: 16
ROWS_PER_SYMBOL: 5
COMPLETED_TRADING_DATE_WINDOW: 2026-05-18 through 2026-05-22
DIAGNOSTICS_RUN: NO
BACKTESTS_RUN: NO
FORECASTS_COMPUTED: NO
POSITIONS_COMPUTED: NO
```

Each locked raw symbol passed exact five-row date coverage:

```text
ZTM6, ZFM6, ZNM6, MESM6, MNQM6, M2KM6, MYMM6, QMN6,
RBN6, ZCN6, ZSN6, ZMN6, ZLN6, ZWN6, HEM6, LEM6
```

## Created Artifacts

Root:

```text
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/attempt_2026-05-30_auth_ok
```

Key artifacts:

```text
raw_provider_output/databento_GLBX-MDP3_ohlcv-1d_16_symbols_2026-05-18_2026-05-23.dbn
raw_provider_output/databento_GLBX-MDP3_ohlcv-1d_16_symbols_2026-05-18_2026-05-23_provider.csv
sanitized_bars/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_SANITIZED.csv
validation/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_ROW_VALIDATION.csv
provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_INTAKE_STATUS.csv
provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_PROVENANCE.md
provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_SHA256SUMS.txt
```

## Hashes

```text
D245F704F9926B346745215A373BA684A84C82F29317959ABA18C0B63AE54A73  provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_INTAKE_STATUS.csv
4B476C6389D7F506DB6A56B5D04BE92BB4A50F6566F9EC983D52F6BCDEE738AE  provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_PROVENANCE.md
F220A83BA0F17128A34A838183D782DF7CFC602C559F5DCF7CF3A5DA552A8B9C  raw_provider_output/databento_GLBX-MDP3_ohlcv-1d_16_symbols_2026-05-18_2026-05-23.dbn
17497DBA5F047E79BCFA641749CF735EB1456EEB38D24E20FB5EDD03A133E815  raw_provider_output/databento_GLBX-MDP3_ohlcv-1d_16_symbols_2026-05-18_2026-05-23_provider.csv
2B7C789DF0EEE658E8DFC0E32F186D6C9CC610B6506E812BB737D61A7EE48A6E  sanitized_bars/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_SANITIZED.csv
49B77E4315B71E19748C94B5358338BB723A35D0D3D8FF269D438EE190849863  validation/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_ROW_VALIDATION.csv
```

The complete hash manifest is preserved in the artifact root.

## Secret Handling

The Databento API key was read from the local desktop key file. The key value was not printed, copied into process artifacts, committed, or recorded.

## Interpretation

This proves that the Databento Historical path can satisfy the exact locked 16-symbol dated futures daily OHLCV quarantine request for the five completed trading dates under audit.

This is not evidence of full-history availability, continuous-contract readiness, cost readiness, carry-leg readiness, strategy readiness, diagnostic validity, backtest validity, or production readiness.

## Closed Boundaries

Still closed:

```text
symbols outside the locked 16
contracts outside the locked dated contracts
schemas outside ohlcv-1d
datasets outside GLBX.MDP3
date windows outside the locked request
continuous contracts
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility or risk calculations
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
GitHub staging
commit
push
PR update/opening
remote repository operations
```

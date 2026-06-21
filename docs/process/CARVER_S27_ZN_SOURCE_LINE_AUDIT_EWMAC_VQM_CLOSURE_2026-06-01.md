# Carver S27 ZN Source-Line Audit EWMAC/VQM Closure

Status:

```text
PASS_S27_ZN_SOURCE_LINE_AUDIT_EWMAC_VQM_CLOSED_FOR_DEV_RECON_MACHINE_PATH
```

## Scope

This process record closes the Opus pre-Lockbox HIGH-2 and HIGH-3 source-line ambiguities for the current ZN Development/Reconciliation machine path only.

It performs no provider API access, no new data download, no market-row parsing, no new diagnostics, no backtest, no new forecast execution, no position execution, no cost computation, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, and no Git operation.

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Opus Findings Addressed

```text
HIGH-2: EWMAC(16,64) trend-overlay frame ambiguous versus Carver S27
HIGH-3: V/Q/M attenuation atom not fully specified locally
```

## Source Authority

Primary source:

```text
Carver.pdf
```

Existing source atom sheet:

```text
docs/process/CARVER_S26_S27_SOURCE_ATOM_SHEET_2026-05-30.md
```

Relevant locked source atoms from the atom sheet:

| Atom | Locked interpretation | Source citation |
|---|---|---|
| S27 trend dependency | EWMAC(16,64), shorthand EWMAC16 | p. 500 |
| Trend role | overlay/condition, not co-weighted forecast block | pp. 500, 508 |
| Trend interaction | mean-reversion forecast must not oppose trend forecast | p. 508 |
| V/Q/M dependency | relative volatility `V`, quantile `Q`, multiplier `M` from S13-family mechanism | pp. 501-502; S13 p. 301 context |
| V/Q/M formula | `M_i_t = EWMA_span_10(2 - 1.5 * Q_i_t)` | pp. 501-502 |
| Adjusted raw forecast | S26 raw forecast times `M_i_t` before inherited later stages | pp. 501-502 |
| S27 scalar | around `20` after S27 overlay and V/Q/M | p. 502 |
| S27 cap | inherits `[-20, +20]` | p. 508 |

## HIGH-2 Closure - EWMAC(16,64) Frame And Veto Logic

### Decision

```text
EWMAC16_FRAME_AND_VETO_LOGIC_LOCKED_FOR_ZN_DEV_RECON_MACHINE_PATH
```

The local machine path uses S27 EWMAC(16,64) as a daily trend overlay computed over a source-native, local additive back-adjusted ZN daily close lineage. It does not compute EWMAC(16,64) on hourly bars.

Evidence:

```text
docs/process/CARVER_ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_RESULT_2026-05-31.md
Status: PASS_ZN_LOCAL_CONTINUOUS_DAILY_LINEAGE_DEV_RECON_ONLY

docs/process/CARVER_S27_ZN_EWMAC16_TREND_RUNTIME_EXECUTION_RESULT_2026-05-31.md
Status: PASS_S27_EWMAC16_TREND_RUNTIME_LEDGER_REAL_ZN_DEV_RECON_ONLY
```

Machine implementation:

```text
tools/databento/carver_s27_zn_ewmac16_trend_runtime.py
```

Implementation facts:

- `FAST_SPAN = 16`
- `SLOW_SPAN = 64`
- input file is the ZN local continuous daily lineage;
- daily input column is `adjusted_close`;
- for each S26 hourly row, eligible daily rows must satisfy `continuous_row_date < completed_trading_date`;
- fewer than 64 strict-prior daily rows fail closed;
- emitted trend forecast is `trend_fast_ewma - trend_slow_ewma`;
- output boundary is runtime ledger only, not S27, diagnostics, or backtest.

The forecast handoff applies the trend as a veto/permission rule:

```text
opposes = s26_raw_forecast * trend_forecast < 0
adjusted_raw = 0 if opposes else s26_raw_forecast * vol_multiplier
```

Machine implementation:

```text
src/carver/spine/s26_s27.py
function: s27_forecast_only_from_s26_forecast_row
```

This is not a direction blender and not a co-weighted forecast-combination block. Opposing mean-reversion forecasts are zeroed before risk adjustment, scalar, and cap.

## HIGH-3 Closure - V/Q/M Atom And Runtime Alignment

### Decision

```text
V_Q_M_FORMULA_ALIGNMENT_AND_RUNTIME_LOCKED_FOR_ZN_DEV_RECON_MACHINE_PATH
```

The local machine path now carries a full S27 V/Q/M runtime dependency ledger for ZN Development/Reconciliation.

Evidence:

```text
docs/process/CARVER_S27_ZN_V_Q_M_TEN_YEAR_VOL_RUNTIME_EXECUTION_RESULT_2026-05-31.md
Status: PASS_S27_ZN_V_Q_M_TEN_YEAR_VOL_RUNTIME_LEDGER_DEV_RECON_ONLY
```

Machine implementation:

```text
tools/databento/carver_s27_zn_vqm_ten_year_vol_runtime.py
```

Implementation facts:

- risk history source is ZN dated-contract daily `ohlcv-1d` rows;
- local additive back-adjusted dated-contract chain is used;
- provider-condition `AVAILABLE` rows only are used;
- Strategy-3-style annualized percentage sigma uses EWMA(32);
- ten-year average uses 2560 prior daily sigma observations;
- `V = sigma_i_t / ten_year_average_sigma`;
- `Q` is the historical quantile rank of `V`;
- raw multiplier is `2 - 1.5 * Q`;
- `M` is EWMA(10) of the raw multiplier;
- each S26 hourly row consumes the latest V/Q/M daily row strictly before the S26 completed trading date;
- runtime count matches the S26 forecast row count.

Runtime output:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/runtime_rows/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_runtime_rows.csv
```

The forecast handoff applies V/Q/M before risk adjustment:

```text
adjusted_raw = 0 if opposes_trend else s26_raw_forecast * vol_multiplier
risk_adjusted = adjusted_raw / sigma_price
scaled = risk_adjusted * 20.0
capped = cap(scaled, +/-20)
```

Machine implementation:

```text
src/carver/spine/s26_s27.py
function: s27_forecast_only_from_s26_forecast_row
```

## Closure Boundary

This closes the Opus ambiguity at the source-line and local machine-path level:

```text
HIGH-2: CLOSED_FOR_ZN_DEV_RECON_MACHINE_PATH
HIGH-3: CLOSED_FOR_ZN_DEV_RECON_MACHINE_PATH
```

It does not close:

```text
CRITICAL-1 futures-realistic cost model
CRITICAL-2 shuffled-null contamination on 2022-2023
CRITICAL-3 claim must remain S27 signal + M1 ladder
HIGH-1 delayed-null contamination on 2024
HIGH-4 2024 informationally touched
```

It also does not authorize or prove:

```text
Lockbox readiness
portfolio/Jumbo readiness
pure Carver S27 result
strategy promotion
tradability
cost realism
CFD adapter readiness
```

## Required Next Pre-Lockbox Work

Continue with:

1. futures-realistic cost-model shape and later execution;
2. signal-attributable PnL restatement net of constant-long ZN beta strip;
3. shuffled/delayed/random-position/circular-shift/block-bootstrap null protocol;
4. mean-reversion structural checks;
5. locked MCPT predeclaration before any new statistical run.

## Non-Authorization

This record authorizes no:

```text
provider API access
new data download
market-row parsing
new diagnostics
new backtests
new forecasts
new positions
new cost computation
carry
trend sleeve combination
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
Git staging
commit
push
PR update
remote operations
```

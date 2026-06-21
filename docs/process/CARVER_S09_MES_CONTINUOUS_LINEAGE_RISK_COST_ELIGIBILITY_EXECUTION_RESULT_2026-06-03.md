# Carver S09 MES Continuous Lineage Risk Cost Eligibility Execution Result

Date: 2026-06-03

Status:

```text
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY_LIFECYCLE_RISK_COST_SPEED_NOT_LOCKED
```

## Purpose

Execute the shaped local S09 MES continuous-lineage/risk/cost eligibility gate after the successful MES Databento daily expansion.

The execution used only the existing local S09 MES quarantine expansion:

```text
docs/researchops/s09/mes_dev_recon_data_expansion/2022-01-03_2023-12-29/
```

No Databento API call, provider login, new data download, new symbol request, continuous-contract download, forecast computation, diagnostic, backtest, position computation, cost computation, CFD adapter work, old QuantLab pipeline use, Git operation, remote operation, deployment, trading, or promotion occurred.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

## Output Root

```text
docs/researchops/s09/mes_continuous_lineage_risk_cost_eligibility/2022-01-03_2023-12-29/
```

## Execution Surface

Local execution script:

```text
tools/databento/carver_s09_mes_continuous_lineage_risk_cost_eligibility.py
```

Pure source-native spine module:

```text
src/carver/spine/s09_mes_lineage.py
```

Synthetic and artifact sentinel tests:

```text
tests/test_s09_mes_lineage_synthetic.py
```

## Inputs

Source expansion status:

```text
PASS_S09_MES_DAILY_EXPANSION_QUARANTINE_ONLY_NOT_LINEAGE_NOT_BACKTEST
```

Locked MES raw-symbol chain:

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

Local static MES source extract:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_SOURCE_EXTRACT_2026-05-30.md
```

Databento definition CSVs were used as source/provider lifecycle cross-checks for expiration timestamps, product code, venue, currency, multiplier, and tick size. The local CME/NinjaTrader MES extract supplies generic MES static facts plus the narrow MES 06-26 pilot lock, but it does not hash-bind official 2021-2024 lifecycle evidence for every roll transition. This does not lock roll semantics, cost, or S03 annual-risk runtime.

## Results

```text
admitted_normal_rows: 3013
rejected_degraded_or_unresolved_rows: 5
total_adjusted_rows: 929
target_window_adjusted_rows: 619
roll_events: 12
continuous_lineage_status: PROVISIONAL_LOCAL_LINEAGE_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_LOCKED
roll_plan_status: PROVISIONAL_PROVIDER_DATE_ROLL_PLAN_TRADING_DAY_SEMANTICS_NOT_LOCKED
back_adjustment_status: PROVISIONAL_LOCAL_BACK_ADJUSTMENT_NOT_STRATEGY_INPUT
provider_condition_admission_status: LOCKED
```

Roll policy:

```text
STATIC_LIFECYCLE_BUFFER_ROLL_5_COMPLETED_PROVIDER_DATES
```

Back-adjustment policy:

```text
LOCAL_ADDITIVE_BACK_ADJUSTMENT_OLD_HISTORY_TO_NEW_CONTRACT_LEVEL
```

The local continuous rows are labeled:

```text
LOCAL_CONTINUOUS_DEV_RECON_ONLY_NOT_BACKTEST_NOT_PRODUCTION
```

The roll transitions use Databento provider trading-date rows, including Sunday session labels where present. This is a provisional provider-date roll plan, not a final Carver/S09 completed-trading-day semantic lock.

## Fail-Closed Strategy Readiness

The lineage execution does not make MES ready for S09 forecasts or backtests.

Remaining blockers:

```text
official_lifecycle_evidence_status: FAIL_CLOSED_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_HASH_BOUND
roll_trading_day_semantics_status: FAIL_CLOSED_S09_MES_PROVIDER_DATE_ROLL_SEMANTICS_NOT_SOURCE_LOCKED
annual_risk_runtime_status: FAIL_CLOSED_S09_MES_ANNUAL_RISK_RUNTIME_NOT_LOCKED
daily_price_risk_runtime_status: FAIL_CLOSED_S09_MES_DAILY_PRICE_RISK_RUNTIME_NOT_LOCKED
cost_source_status: FAIL_CLOSED_S09_MES_COST_SOURCE_NOT_LOCKED
risk_adjusted_cost_status: FAIL_CLOSED_S09_MES_RISK_ADJUSTED_COST_NOT_LOCKED
speed_cost_eligibility_status: FAIL_CLOSED_S09_MES_SPEED_COST_ELIGIBILITY_NOT_LOCKED
eligible_speed_set_status: FAIL_CLOSED_S09_MES_ELIGIBLE_SPEED_SET_NOT_LOCKED
strategy_input_readiness_status: FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
```

Next required gate:

```text
S09_MES_OFFICIAL_LIFECYCLE_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_SOURCE_LOCK_GATE
```

That gate must lock or fail-close official 2021-2024 lifecycle evidence for the MES roll chain, provider trading-date versus Carver completed-trading-day semantics, the S03 annual-risk runtime, S09 daily price-risk runtime, MES source-native cost source, risk-adjusted cost per trade, 0.15 SR speed-cost eligibility, and the resulting eligible EWMAC speed set before any S09 forecast or backtest gate.

## Non-Authorization

This result authorizes no provider API access, no new data download, no new market-row expansion, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no cost computation, no carry, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

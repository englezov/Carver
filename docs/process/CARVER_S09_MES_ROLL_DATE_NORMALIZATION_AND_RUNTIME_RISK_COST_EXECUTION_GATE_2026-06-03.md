# Carver S09 MES Roll Date Normalization And Runtime Risk Cost Execution Gate

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_GATE_NOT_EXECUTION
```

## Purpose

Define the next executable gate required before MES can become a Strategy 9 Development/Reconciliation forecast-input candidate.

The immediately prior packet is:

```text
docs/process/CARVER_S09_MES_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_VALUE_LOCK_RESULT_2026-06-03.md
```

That packet partially locked lifecycle dates and the Part One/S03 annual-risk source method family, but left strategy input fail-closed.

## Gate Name

```text
S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE
```

## Lane And Scope

```text
lane_class: SOURCE_NATIVE_FUTURES
source_row: APPENDIX_C_174_006
author_market_code: MES
target_window: 2022-01-03 through 2023-12-29
```

This gate is limited to MES. It does not authorize ES, NQ, MNQ, broader Appendix C rows, CFD adapters, old QuantLab pipelines, or any portfolio-level reconstruction.

## Strategy Design Data Ordering

The execution must use the oldest authorized completed source-native data first for any Strategy 9 design decision.

Required rules:

- the execution must begin from the earliest available authorized MES completed-bar evidence inside the named Development/Reconciliation scope;
- later data must not shape parameters, thresholds, filters, costs, speed selection, FDM selection, or rescue choices;
- later data may be consumed only after the older authorized evidence has been admitted, normalized, and hash-bound or explicitly failed closed;
- if the oldest available authorized MES data is insufficient, fail closed rather than silently designing on newer data;
- no newer sample may be used to tune or rescue a decision made on the older sample.

## Required Inputs For A Future Execution

A later execution gate must consume only locked local Carver artifacts or separately authorized Databento/static-provider evidence named in that execution. The minimum input set is:

```text
docs/researchops/s09/mes_continuous_lineage_risk_cost_eligibility/2022-01-03_2023-12-29/**
docs/researchops/s09/mes_historical_lifecycle_cost_risk_extraction/2022-01-03_2023-12-29/**
docs/researchops/s09/mes_roll_risk_cost_value_lock/2022-01-03_2023-12-29/**
docs/process/CARVER_S09_MES_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_VALUE_LOCK_RESULT_2026-06-03.md
docs/process/CARVER_S09_MES_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_VALUE_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md
```

If the later execution needs Databento metadata or data access to settle provider-date semantics, it must state the exact endpoint/request surface before use. This shape gate itself performs no Databento API access and no OHLCV request.

## Roll Date Normalization Requirements

The execution must resolve or fail-close the prior Sunday provider-date labels in the MES roll plan, including examples such as:

```text
2022-03-13
2022-06-12
2022-09-11
2022-12-11
```

The output must declare the exchange completed trading-date authority used for roll decisions.

Required rules:

- no silent date shifting;
- no silent substitution of provider date, exchange session date, calendar date, or completed trading date;
- no Sunday provider-date labels may be treated as strategy-ready unless the mapping to source-native completed trading dates is explicit and hash-bound;
- holidays and non-trading days must fail closed unless the mapping authority proves them;
- roll transition rows must preserve old/new contract lineage and source hashes.

Expected output artifact:

```text
roll_date_normalization/<STAMP>_S09_MES_ROLL_DATE_NORMALIZATION_ledger.csv
```

## Runtime Annual Risk Requirements

The execution must resolve or fail-close MES runtime annual-risk values using the already locked source method:

```text
annualized percentage-return risk
EWMA32 current-risk component
30/70 long-run/current-risk blend family
daily_price_risk = current_price * annual_percentage_risk / 16
```

Required rules:

- completed-bar only;
- no lookahead beyond each completed trading date;
- explicit long-run risk source, value, timestamp, and hash;
- explicit warm-up and first usable date;
- no runtime values estimated from future rows;
- no reuse of S26/Zn-specific runtime values;
- no daily price-risk rows unless annual percentage risk is valid for the same completed date.

Expected output artifacts:

```text
risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv
risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv
```

## Cost Value Requirements

The execution must resolve or fail-close source-native MES costs for the target window.

Required historical MES exchange/clearing/regulatory/broker/spread/slippage evidence:

- CME/exchange fee value;
- clearing/regulatory/NFA-style fee value if applicable;
- broker commission value or explicit no-broker-cost sensitivity label;
- spread/slippage policy;
- currency;
- per-side versus round-turn semantics;
- effective date range;
- source/provenance/hash for every value.

No ETF, CFD, prop-firm, NinjaTrader-default, or old QuantLab cost assumption may be substituted.

Expected output artifact:

```text
cost/<STAMP>_S09_MES_COST_VALUE_ledger.csv
```

## Risk-Adjusted Cost And Speed Eligibility

The execution must compute or fail-close risk-adjusted cost per trade only after both cost values and daily price-risk runtime values are locked.

The S09 speed eligibility step must apply the source cost threshold:

```text
0.15 SR
```

to the Strategy 9 turnover table:

```text
EWMAC2  98.5
EWMAC4  50.2
EWMAC8  25.4
EWMAC16 13.2
EWMAC32 7.6
EWMAC64 5.2
```

Required rules:

- no default all-six-speed assumption;
- no missing-cost pass-through;
- no post-result speed selection;
- no FDM row selection until the eligible span set is locked;
- Table 36 FDM must match the eligible EWMAC speed set exactly.

Expected output artifacts:

```text
cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv
speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv
```

## Pass And Fail Semantics

The execution may emit:

```text
READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST
```

only if all of the following are locked:

- roll date normalization;
- annual-risk runtime values;
- daily price-risk runtime values;
- historical cost values;
- risk-adjusted cost per trade;
- eligible EWMAC speed set;
- Table 36 FDM row;
- oldest-authorized-data-first ordering for strategy design;
- hash-bound provenance.

Otherwise it must emit:

```text
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
```

## Non-Authorization

This process-only gate authorizes no Databento API access, no provider login, no OHLCV request, no new data download, no market-row parsing, no risk runtime execution, no cost computation, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no positions, no carry, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

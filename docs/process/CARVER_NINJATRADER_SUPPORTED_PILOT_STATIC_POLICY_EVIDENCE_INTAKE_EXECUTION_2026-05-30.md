# Carver NinjaTrader-Supported Pilot Static Policy Evidence Intake Execution

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_EVIDENCE_INTAKE_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Create a machine-readable static policy ledger for the selected 16-row NinjaTrader-supported pilot universe:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

The ledger resolves or fail-closes the static policy layer needed before any future tiny historical-bar intake can be considered. This execution did not touch market rows, did not export historical data from NinjaTrader, did not access provider APIs, and did not run diagnostics or backtests.

## Inputs

Policy evidence packet:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_EVIDENCE_PACKET_2026-05-30.md
```

Current pilot static readiness ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_READINESS_STATUS_2026-05-30.csv
```

Current contract identity hardening update:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv
```

Current session/roll/completed-bar readiness ledger:

```text
docs/researchops/session_roll/CARVER_APPENDIX_C_SESSION_ROLL_COMPLETED_BAR_READINESS_STATUS_2026-05-29.csv
```

Current risk/FX/cost/carry-leg readiness ledger:

```text
docs/researchops/risk_fx_cost_carry_leg/CARVER_APPENDIX_C_RISK_FX_COST_CARRY_LEG_READINESS_STATUS_2026-05-29.csv
```

Official static source families referenced:

```text
NinjaTrader Help Guide static pages
CME Group static policy/specification pages
```

## Output

Machine-readable static policy ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_LEDGER_2026-05-30.csv
Rows: 16
SHA256: 6CFD6AABDA913A8DF3DE865273A58DBDA0A658143073094AA93F912539ADFD5F
```

## Row Preservation

```text
selected_rows: 16
output_rows: 16
unique_output_row_ids: 16
selected_row_id_set_preserved: YES
selected_code_set_preserved: YES
```

## Static Policy Result

Final row policy status:

```text
STATIC_POLICY_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 0
STATIC_POLICY_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
```

No row is ready for historical-bar intake yet.

## Policy Atoms Resolved As Static Shape Only

The ledger records the following static policy shapes:

```text
completed_bar_timestamp_policy:
  PARTIAL_STATIC_POLICY_IDENTIFIED_NINJATRADER_EXPORT_END_OF_BAR_UTC_NOT_ROW_READY

explicit_contract_policy:
  POLICY_SHAPE_SELECTED_EXPLICIT_DATED_CONTRACT_MONTH_REQUIRED_BEFORE_EXPORT

merge_policy:
  POLICY_SHAPE_SELECTED_NO_CONTINUOUS_MERGE_FOR_FIRST_PRICE_INTAKE

back_adjustment_policy:
  POLICY_SHAPE_SELECTED_NOT_USED_FOR_FIRST_EXPLICIT_CONTRACT_PRICE_INTAKE_CONTINUOUS_BACK_ADJUSTMENT_CLOSED

risk_fx_cost_carry_leg_policy_classification:
  PRICE_BAR_INTAKE_ONLY_RISK_FX_COST_CARRY_LEG_NOT_REQUIRED_FOR_EXPORT_BUT_NOT_STRATEGY_READY
```

These are not production trading locks. They only narrow the future first intake shape to explicit dated contract-month price bars, with continuous merge, continuous roll construction, and back-adjustment closed for the first price-intake pilot.

## Policy Atoms Still Fail-Closed

Every selected row remains fail-closed because the following are not fully locked:

```text
full NinjaTrader trading-hours template sessions
template timezone
EOD marker and exchange trading-date boundary
local template holiday definitions
CME holiday/early-close precedence versus local template holidays
daily close versus official settlement policy
explicit dated contract month for the future pilot request
rollover evidence for any later continuous-series work
stale-bar policy
missing-bar policy
canonical trading-date and UTC alignment policy
operator capital/base-currency policy
commission/fee account plan
spread/slippage/turnover policy
risk-adjusted cost readiness
trend/carry eligibility
carry curve-leg readiness
```

## Interpretation

The gate successfully converted the static policy evidence packet into a row-preserving machine-readable ledger, but it did not open data intake.

The important improvement is that the first historical-bar pilot shape is now constrained:

- use explicit dated contract months only;
- do not use continuous merged instruments for the first price intake;
- do not use roll/back-adjusted continuous series in the first price intake;
- treat NinjaTrader historical exports, if separately authorized later, as end-of-bar timestamped and UTC-exported;
- keep strategy readiness, risk, costs, trend/carry eligibility, and carry-curve work closed.

This is enough to define the next evidence target, but not enough to run any NinjaTrader historical-bar export.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_TEMPLATE_STATIC_EVIDENCE_INTAKE_GATE
```

That gate should use only static local NinjaTrader configuration evidence and official static NinjaTrader/CME policy references to extract or fail-close, for the 16 selected pilot rows:

- full session definitions for each observed template;
- template timezone;
- EOD markers;
- holiday and partial-holiday definitions;
- CME holiday/early-close precedence;
- canonical completed trading date policy;
- UTC end-of-bar timestamp alignment policy.

It must not export historical data, parse market rows, use provider APIs, run diagnostics, or run backtests.

Only after a later static policy/readiness execution marks at least one row:

```text
STATIC_POLICY_READY_FOR_TINY_HISTORICAL_BAR_INTAKE
```

should a separate operator decision consider a tiny historical-bar intake pilot.

## Non-Authorization

This record authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

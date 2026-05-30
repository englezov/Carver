# Carver NinjaTrader-Supported Pilot Universe Shape And Static Readiness Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_SUPPORTED_PILOT_UNIVERSE_SHAPE_STATIC_READINESS_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the future static-readiness boundary for a tiny NinjaTrader-supported source-native futures pilot universe after the Appendix C/NinjaTrader data-source finalization decision.

This draft selects a small candidate universe from exact NinjaTrader-supported Appendix C rows and defines the locks required before any NinjaTrader historical-bar intake can be considered.

This is not a data gate. It does not authorize historical bars, market-row parsing, diagnostics, backtests, trading, or promotion.

## Inputs

Appendix C/NinjaTrader finalization decision:

```text
docs/process/CARVER_APPENDIX_C_NINJATRADER_DATA_SOURCE_FINALIZATION_DECISION_2026-05-30.md
```

NinjaTrader provider mapping artifact:

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
```

Contract identity static hardening update:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv
```

Session/roll/completed-bar readiness status:

```text
docs/researchops/session_roll/CARVER_APPENDIX_C_SESSION_ROLL_COMPLETED_BAR_READINESS_STATUS_2026-05-29.csv
```

Risk/FX/cost/carry-leg readiness status:

```text
docs/researchops/risk_fx_cost_carry_leg/CARVER_APPENDIX_C_RISK_FX_COST_CARRY_LEG_READINESS_STATUS_2026-05-29.csv
```

No market rows, historical bars, NinjaTrader historical exports, provider APIs, diagnostics, or backtests were used.

## Selected Pilot Shape

Selected pilot universe:

```text
ZT, ZF, ZN,
MES, MNQ, M2K, MYM,
QM, RB,
ZC, ZS, ZM, ZL, ZW,
HE, LE
```

Count:

```text
16
```

Pilot lane:

```text
SOURCE_NATIVE_FUTURES
```

Universe status:

```text
NINJATRADER_SUPPORTED_PILOT_CANDIDATE_NOT_DATA_READY
```

## Pilot Composition

| Sleeve | Selected rows | Reason |
|---|---|---|
| Rates | `ZT`, `ZF`, `ZN` | Core CME/CBOT Treasury futures, exact NinjaTrader static candidates, no current blocked status. |
| Equity index | `MES`, `MNQ`, `M2K`, `MYM` | Micro/e-mini equity index futures, exact NinjaTrader static candidates, diversified across S&P 500, Nasdaq, Russell, and Dow. |
| Energy | `QM`, `RB` | WTI mini crude and RBOB gasoline, exact NinjaTrader static candidates, avoids currently blocked/ambiguous gas rows. |
| Grains and oilseeds | `ZC`, `ZS`, `ZM`, `ZL`, `ZW` | Core CBOT agriculture/oilseed futures, exact NinjaTrader static candidates, quote-unit semantics still need final lock. |
| Livestock | `HE`, `LE` | CME livestock futures, exact NinjaTrader static candidates, quote-unit semantics still need final lock. |

This is a deliberately small, CME Group-heavy subset. It is diversified enough for a first source-native futures intake shape, but it is not the complete Appendix C Jumbo universe.

## Current Static Status Of Selected Rows

| Code | Current hardening status | Required before any historical bars |
|---|---|---|
| `ZT` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `ZF` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `ZN` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `MES` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `MNQ` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `M2K` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `MYM` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `QM` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `RB` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_SUPPORTED_NOT_DATA_READY` | Final static venue, active/listed, delivery-cycle, and completed-bar policy locks. |
| `ZC` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_QUOTE_UNIT_LOCK_REQUIRED` | Final quote-unit/multiplier semantics lock, delivery-cycle lock, and completed-bar policy locks. |
| `ZS` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_QUOTE_UNIT_LOCK_REQUIRED` | Final quote-unit/multiplier semantics lock, delivery-cycle lock, and completed-bar policy locks. |
| `ZM` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_DELIVERY_CYCLE_LOCK_REQUIRED` | Final delivery-cycle lock and completed-bar policy locks. |
| `ZL` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_QUOTE_UNIT_LOCK_REQUIRED` | Final quote-unit/multiplier semantics lock, delivery-cycle lock, and completed-bar policy locks. |
| `ZW` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_QUOTE_UNIT_LOCK_REQUIRED` | Final quote-unit/multiplier semantics lock, delivery-cycle lock, and completed-bar policy locks. |
| `HE` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_QUOTE_UNIT_LOCK_REQUIRED` | Final quote-unit/multiplier semantics lock, delivery-cycle lock, and completed-bar policy locks. |
| `LE` | `CONTRACT_IDENTITY_STATIC_UNRESOLVED_QUOTE_UNIT_LOCK_REQUIRED` | Final quote-unit/multiplier semantics lock, delivery-cycle lock, and completed-bar policy locks. |

Current selected-row data status:

```text
production_contract_identity_lock_status: NOT_LOCKED
data_intake_readiness_status: NOT_READY_FOR_MARKET_ROW_INTAKE
```

## Required Static Locks Before Historical-Bar Intake

Before any future NinjaTrader historical-bar intake pilot, every selected row must have:

- exact NinjaTrader master instrument identity lock;
- official exchange/venue normalization lock;
- currency normalization lock;
- contract unit and point-value lock;
- quote-unit and multiplier semantics lock;
- tick size and tick value lock;
- active/listed or explicitly historical-only status lock;
- contract family and variant lock;
- delivery-cycle/listed-contract-month lock;
- session calendar or trading-hours template policy lock;
- completed-bar timestamp policy lock;
- stale-bar and missing-bar policy lock;
- roll rule lock;
- back-adjustment policy lock;
- timestamp/timezone alignment lock;
- risk/FX/cost/carry-leg status for the chosen pilot purpose.

If any selected row cannot satisfy these locks, it must be excluded from the first historical-bar pilot or the whole pilot must fail closed.

## Alias Rows

Alias-required rows remain closed in this gate.

Closed alias rows:

```text
AUD -> 6A or M6A
CAD -> 6C or M6C or MICD
CHF -> 6S or M6S or MISF
EUR -> 6E or E7 or M6E
GBP -> 6B or M6B
JPY -> 6J or M6J or MIJY
MXP -> 6M
NZD -> 6N
ESTX50 -> FESX or FSXE
```

Alias rows need a separate process/source alias readiness gate. They are not part of the first pilot shape selected here.

## Fail-Closed Exclusions

The following remain excluded from this pilot:

- `BLOCKED_UNAVAILABLE` Appendix C rows;
- `BLOCKED_CONTRACT_VARIANT_MISMATCH` rows;
- alias-required rows;
- exact-code rows currently marked `BLOCKED_FAIL_CLOSED`;
- exact-code rows with active/retired ambiguity such as `GE` and `N1U`;
- exact-code rows with provider tick mismatch such as `Z3N`, `NOK`, and `SEK`;
- exact-code rows with unresolved source/provider variant risk such as `NIFTY`;
- rows requiring product-code or rulebook reconciliation such as `HH`;
- rows requiring full-versus-small contract reconciliation such as `SI`;
- rows outside the selected 16-row pilot set.

No row may be silently substituted, dropped from a claimed Appendix C universe, reweighted, or treated as executable because it is convenient.

## Relationship To Session/Roll And Risk Readiness

Current downstream ledgers remain closed:

```text
SESSION_ROLL_BLOCKED_CONTRACT_IDENTITY: 61
SESSION_ROLL_BLOCKED_NO_COMPLETED_BAR_POLICY: 41
RISK_FX_COST_CARRY_LEG_BLOCKED_CONTRACT_IDENTITY: 61
RISK_FX_COST_CARRY_LEG_BLOCKED_SESSION_ROLL_COMPLETED_BAR: 41
```

This draft does not update those ledgers. It defines the future shape of the pilot so that the next static readiness gates can target a deliberately small set of rows.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_STATIC_READINESS_EXECUTION_GATE
```

That gate should create a machine-readable readiness ledger for the selected 16 rows only, using current static artifacts, and should resolve or fail-close:

- contract identity final static locks;
- session/calendar/completed-bar policy;
- roll/back-adjustment/stale/missing-bar policy;
- risk/FX/cost/carry-leg readiness status.

It must not touch historical bars.

Only after that execution gate produces at least one row with all required static readiness locks should a separate operator decision consider a tiny NinjaTrader historical-bar intake pilot.

## Non-Authorization

This draft authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

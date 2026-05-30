# Carver NinjaTrader-Supported Pilot Static Dated Contract Selection Execution

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Execute the static dated-contract selection gate for the first tiny NinjaTrader-supported pilot candidate set:

```text
ZN, MES, QM, ZC
```

This gate uses only current Carver static artifacts. It does not use real market data, NinjaTrader historical export, provider API access, market-row parsing, diagnostics, backtests, trading, deployment, or promotion.

## Inputs

Shape gate:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_SHAPE_GATE_DRAFT_2026-05-30.md
```

Static ledgers:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_EXPLICIT_CONTRACT_MONTH_CONTRACT_IDENTITY_FINAL_STATIC_LOCK_2026-05-30.csv
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_ROW_POLICY_LEDGER_2026-05-30.csv
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv
```

No external provider API, NinjaTrader export, historical bar availability check, market-row parsing, diagnostic, or backtest was used.

## Output

Machine-readable dated-contract selection ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_EXECUTION_2026-05-30.csv
```

SHA256:

```text
AD6DAFF1CD683132B4CC329201FA849FB413375F9F77E7D0FBD3F5B78711A4CD
```

## Target Shape

As-of date:

```text
2026-05-30
```

Target completed trading-date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

Candidate rows:

```text
ZN, MES, QM, ZC
```

## Execution Result

Row preservation:

```text
CANDIDATE_ROWS_EXPECTED: 4
CANDIDATE_ROWS_PRESERVED: 4
```

Dated-contract selection:

```text
DATED_CONTRACT_SELECTED: 0
DATED_CONTRACT_FAIL_CLOSED: 4
STATIC_READY_FOR_LATER_TINY_HISTORICAL_BAR_INTAKE: 0
```

All four rows fail closed.

## Row Outcomes

```text
ZN: FAIL_CLOSED_NO_DATED_CONTRACT_SELECTED
MES: FAIL_CLOSED_NO_DATED_CONTRACT_SELECTED
QM: FAIL_CLOSED_NO_DATED_CONTRACT_SELECTED
ZC: FAIL_CLOSED_NO_DATED_CONTRACT_SELECTED
```

Reason by row:

- `ZN`: quarterly June 2026 candidate is visible from the existing quarterly-cycle summary, but active/listed status, final rulebook delivery-cycle lock, last-trade/first-notice/delivery constraints, and NinjaTrader dated-contract syntax are not locked.
- `MES`: quarterly June 2026 candidate is visible from the existing quarterly-cycle summary, but active/listed status, final rulebook/cash-settlement constraints, expiration constraints, and NinjaTrader dated-contract syntax are not locked.
- `QM`: NYMEX energy delivery cycle is not extracted in the current static artifact, and active/listed status, last-trade/expiration/delivery constraints, and NinjaTrader dated-contract syntax are not locked.
- `ZC`: May versus July 2026 cannot be resolved from current static artifacts without final grain delivery-cycle hash, last-trade/first-notice/delivery constraints, active/listed status, and NinjaTrader dated-contract syntax.

## Interpretation

This is a successful fail-closed execution, not a data-source failure.

The current Carver static artifacts are sufficient to preserve row identity and identify why the first four-row pilot cannot yet touch historical bars. They are not sufficient to select exact dated contracts.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_EVIDENCE_INTAKE_GATE
```

That gate should ingest or create a static evidence packet for the four candidate rows that locks:

- active/listed status as of `2026-05-30`;
- official listed contract months covering `2026-05-18` through `2026-05-22`;
- last-trade, first-notice, expiration, delivery, and cash-settlement constraints as applicable;
- NinjaTrader local dated-contract syntax for each selected contract;
- row-level conflict policy if local NinjaTrader and official static exchange evidence disagree.

It must not export historical bars, parse market rows, access provider APIs, run diagnostics, or run backtests.

## Non-Authorization

This execution authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

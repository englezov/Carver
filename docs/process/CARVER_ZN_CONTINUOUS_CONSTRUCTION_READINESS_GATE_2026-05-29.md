# Carver ZN Continuous Construction Readiness Gate

Date: 2026-05-29

Status:

```text
CARVER_ZN_CONTINUOUS_CONSTRUCTION_READINESS_PARSER_ONLY_NOT_STRATEGY_NOT_DIAGNOSTIC
```

## Purpose

Lock the first narrow ZN continuous-construction readiness rule and prove that the manifest-exported ZN daily files can produce enough completed daily bars for the S09 warm-up boundary.

This is not a strategy gate, not an S09 forecast gate, not a diagnostic, and not a backtest.

## Source And Process Anchors

Carver S01 introduces futures expiry, rolling, and back-adjusted futures prices as the mechanical substrate for later daily strategies. The S01 candidate brief records the relevant source anchors:

```text
docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md
```

M0 records that continuous-contract construction, contract selection, rolling rule, and back-adjustment must be locked before strategy computation:

```text
docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md
```

The ZN native daily export parser validation records the exact source files and file hashes:

```text
docs/process/CARVER_ZN_NATIVE_DAILY_EXPORT_PARSER_VALIDATION_2026-05-29.md
```

## Locked Narrow Readiness Rule

For this ZN readiness gate only:

```text
lane class: SOURCE_NATIVE_FUTURES
instrument: ZN
frequency: completed daily bars
source files: manifest-declared ZN 09-25, 12-25, 03-26, 06-26 native daily Last exports
contract order: increasing contract month
roll segmentation: use each contract until its observed final completed date, then use the next contract from the first completed date after that cutoff
overlap requirement: the next contract must contain a completed bar on the previous contract cutoff date
back-adjustment: additive close-gap offset using the overlapping cutoff date
minimum readiness rows: 257
```

The additive offset is computed at each roll boundary as:

```text
offset = previous_adjusted_close_on_cutoff_date - next_contract_raw_close_on_cutoff_date
```

The offset is applied to the next contract's OHLC values for dates after the cutoff.

This construction is a readiness artifact. It does not settle the final production roll calendar for every Carver instrument, and it does not authorize use in a backtest.

## Implemented Surface

Code:

```text
src/carver/spine/continuous.py
src/carver/spine/data_acquisition.py
```

Tests:

```text
tests/test_continuous_synthetic.py
tests/test_daily_portfolio_conformance_synthetic.py
```

The implementation fails closed if:

- source rules are unresolved;
- contract codes are mixed;
- contract months are not strictly increasing;
- bars are not grouped by contract month;
- dates are unsorted or duplicated inside a contract;
- a roll boundary lacks an overlapping cutoff-date bar in the next contract;
- roll segmentation creates an empty segment;
- the adjusted result is not strictly increasing by completed date.

Hostile-audit follow-up noted that the code already failed closed on unresolved rules, contract-month ordering, grouped contract months, and duplicate dates; tests were expanded to witness those cases directly.

## ZN Readiness Result

Using the exported, Git-ignored ZN files:

```text
source_contract_months: 09-25, 12-25, 03-26, 06-26
roll_dates: 2025-09-22, 2025-12-22, 2026-03-23
first_date: 2025-05-29
last_date: 2026-05-28
adjusted_rows: 259
minimum_rows: 257
ready: TRUE
```

First and last adjusted closes are recorded as parser/construction metadata only:

```text
first_adjusted_close: 110.688
last_adjusted_close: 110.625
```

No adjusted row series is committed.

## Interpretation

The manifest-exported ZN chain is ready for a future, separately authorized S09 tiny-slice real-data conformance gate because it has at least 257 completed daily continuous-construction rows.

This does not mean:

- S09 has been run;
- any forecast has been computed;
- any return, PnL, Sharpe, drawdown, or diagnostic has been computed;
- the roll/back-adjustment rule is globally accepted for every futures market;
- the data is promoted to TEST, VALIDATION, Lockbox, Forward, deployment, or trading.

## Verification

```text
subagent hostile audit:
PROCESS_SAFE_FOR_ZN_CONTINUOUS_READINESS_NOT_STRATEGY_NOT_DIAGNOSTIC

python -m unittest tests.test_continuous_synthetic -v
4 passed

python -m unittest tests.test_daily_portfolio_conformance_synthetic.DailyPortfolioConformanceSyntheticTests.test_continuous_roll_and_back_adjustment_gate_fails_closed -v
1 passed

python -m compileall -q src tests
passed

python -m unittest discover -s tests -v
89 passed

git ls-files -- data/**
no tracked data files
```

## Non-Authorization

This gate authorizes no S09 forecast, no strategy computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.

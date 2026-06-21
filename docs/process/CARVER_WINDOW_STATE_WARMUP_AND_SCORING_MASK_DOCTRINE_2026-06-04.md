# Carver Window State Warmup And Scoring Mask Doctrine

Date: 2026-06-04

Status:

```text
PROCESS_ONLY_WINDOW_STATE_WARMUP_AND_SCORING_MASK_DOCTRINE_NOT_BACKTEST
```

## Doctrine

Each evidence stage must separate state history from scored evidence.

The universal rule is:

```text
previous_window_for_state_warmup_only -> current_window_for_scoring_only
```

Previous-window bars may initialize indicator state, volatility/risk state,
carry state, roll state, and other source-native runtime machinery. They must
not emit counted forecasts, trades, PnL, costs, Sharpe, drawdown, hit rate,
trade count, eligibility decisions, promotion decisions, or alpha claims for
the current stage.

Current-window bars alone define scored evidence. A bar is admissible for
scored evidence only when its signal date and its realized next-bar PnL date
both remain inside the current stage scoring window.

## Stage Application

TEST may use the Development/Reconciliation or machinery-development slice only
as state-history warmup.

VALIDATION may use TEST only as state-history warmup.

LOCKBOX may use VALIDATION only as state-history warmup.

Forward may use the locked prior stage or live prior completed bars only as
state-history warmup under the separately authorized Forward protocol.

## Required Masks

Every stage execution tool must expose and audit two masks:

- `state_history_mask`: prior bars allowed to build state only.
- `scoring_window_mask`: current-stage bars allowed to emit counted evidence.

The tool must fail closed if:

- scored forecasts are emitted before the scoring window starts;
- scored PnL includes a next bar outside the scoring window;
- previous-window bars appear in trade count, costs, PnL, or performance
  summaries;
- current-window bars are silently burned as indicator warmup when an authorized
  previous-window state-history buffer exists;
- the state-history buffer is too short for the predeclared indicator warmup;
- any future-stage data is accessed as state history or scored evidence.

## S09 MES Current Application

For the current S09 MES TEST remediation, the state-history buffer is the
previously authorized machinery-development slice:

```text
2019-05-05 through 2020-04-05
```

The TEST scoring window remains:

```text
2020-04-06 through 2022-02-08
```

The old S09 MES TEST backtest result remains diagnostic-only because it used
the TEST window itself for warmup and therefore shortened the scored TEST
evidence surface.

## Boundary

This doctrine authorizes no provider API access, no new market-data request, no
data download, no market-row parsing, no diagnostics, no backtests, no
forecasts, no positions, no costs, no carry, no trend, no OOS, no VALIDATION,
no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active
pipeline use, no tuning, no deployment, no trading, no promotion, no Git
staging, no commit, no push, no PR, and no remote operation.

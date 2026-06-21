# S09 MES Pre-Backtest Usable History After Warmup Discussion

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_PRE_BACKTEST_USABLE_HISTORY_AFTER_WARMUP_DISCUSSION_NOT_BACKTEST
```

## Scope

This document records the required discussion before any S09/MES
Development/Reconciliation backtest may run.

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- current observed artifact window: 2022-01-03 through 2023-12-29

The `2022-01-03 through 2023-12-29` window was used as a bounded artifact
window for data expansion, provisional continuous-lineage counts, and
readiness/status artifacts. It is not the default Development/Reconciliation backtest window.
It was not used as forecast, diagnostic, position, return, PnL, or backtest
evidence.

Default Dev/Reconciliation selection must start from oldest authorized source-native data first.
Then explicitly lock the usable window after warmup, completed-bar
normalization, source-native roll semantics, data availability, and operator
approval limits are known. Do not default to a convenient two-year window.

## Current Row Evidence

Current metadata-only evidence records:

```text
target_window_rows = 2065
target_window_adjusted_rows = 619
total_adjusted_rows = 929
pre_target_context_rows = 310
```

Interpretation:

- `target_window_rows = 2065` is the raw active-chain target-window row count
  across dated contracts.
- `target_window_adjusted_rows = 619` is the provisional continuous target
  window row count.
- `total_adjusted_rows = 929` is the provisional continuous row count including
  pre-target context.
- `pre_target_context_rows = 310` is `929 - 619`.

These counts are not backtest evidence. They are row-availability evidence for
the warmup discussion.

## EWMAC Warmup

The current S09 source atom includes EWMAC spans:

```text
2, 4, 8, 16, 32, 64
```

If EWMAC64 survives the cost screen:

```text
EWMAC64
slow_span = 256
minimum_completed_bars = 257
```

Current rough scenarios:

- 619 usable target rows if pre-target context is authorized for warmup only.
- approximately 362 usable target rows if warmup must be consumed inside the target window.

These are not locked first-usable-date claims. They are planning arithmetic
from current metadata and the current synthetic EWMAC warmup rule.

## Unresolved Before Backtest

The following remain unresolved before any Development/Reconciliation backtest:

- annual-risk warmup and first usable date remain not locked.
- provider-date Sunday rows and exchange completed-bar normalization remain unresolved.
- roll/completed-trading-day semantics remain not source-locked.
- eligible speed set remains not locked.
- risk/cost input lock remains not complete.

No Dev/Reconciliation backtest may run until a first_usable_date, warmup_rows_consumed, usable_rows_remaining, and warmup policy are locked.

## Boundary

This document authorizes no data access, no provider API access, no new provider
download, no market-row parsing, no runtime risk execution, no cost extraction,
no forecast computation, no diagnostics, no backtests, no returns, no PnL, no
positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no
deployment, no trading, no promotion, no Git staging, commit, push, PR, or
remote operation.

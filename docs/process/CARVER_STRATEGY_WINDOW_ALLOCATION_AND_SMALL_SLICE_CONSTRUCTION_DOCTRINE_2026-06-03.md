# Carver Strategy Window Allocation And Small Slice Construction Doctrine

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_STRATEGY_WINDOW_ALLOCATION_SMALL_SLICE_CONSTRUCTION_DOCTRINE_NOT_BACKTEST
```

## Doctrine

Dev/Reconciliation is not a default two-year window.

Each strategy has a different expected trade count and statistical sample requirement.
TEST, VALIDATION, and Lockbox windows must be allocated per strategy rather
than inherited from an old fixed-window lab pattern.

The window allocation must be based on expected trade count, bar frequency, warmup loss, and source-native data availability.

If data is needed only to construct the strategy, use the smallest source-native construction slice that satisfies the construction dependency.
Construction slices are not scored evidence windows.

Do not burn two years of data to construct a strategy when a smaller source-native slice is sufficient.

Use oldest authorized source-native data first.

This doctrine supersedes any old-lab fixed Dev-window relic.

## Boundary

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations are authorized by this doctrine.

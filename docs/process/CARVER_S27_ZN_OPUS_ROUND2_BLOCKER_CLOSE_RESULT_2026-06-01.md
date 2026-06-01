# Carver S27 ZN Opus Round 2 Blocker Close Result

Status:

```text
PASS_OPUS_ROUND2_MECHANICAL_BLOCKERS_CLOSED_WITH_SCALAR_HEURISTIC_CAVEAT
```

## Scope

This artifact answers Opus Round 2 blockers using existing local Carver artifacts only. It performs no provider access, no new data download, no market-row expansion, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, and no Git operation.

## Summary

| Period | Scalar heuristic | Mean abs capped nonzero | Cap saturation | Lag min/median/max | Lag zero rows | Largest positive null | Constant-long net | Random-position mean | Roll sides | Roll status |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| ZN_2022_2023_INITIAL_TEST | FAILS_OPUS_HEURISTIC_RECORDED_NO_TUNING | 2.5111951146934763 | 0.0014442273383739699 | 1/1/1 | 0 | DAY_SHUFFLED 3494.020000000003 | -6072.578589634664 | -9024.523046875744 | 6/6 | PASS |
| ZN_2024_VALIDATION | FAILS_OPUS_HEURISTIC_RECORDED_NO_TUNING | 3.636256459488514 | 0.0059131610069268455 | 1/1/1 | 0 | ONE_BAR_DELAYED 9151.580000000002 | -3701.155373436972 | -11506.910156250546 | 2/2 | PASS |

## Findings

- Verifier import independence is SHA-anchored and contains no imports from `src/carver/spine/s26_s27.py`, `carver`, `tools/databento`, or the implementation scripts.
- Runtime lag distribution is surfaced; every forecast row in both periods has `min_runtime_lag_days == 1` and zero lag-0 rows.
- Roll-transition fee events are surfaced with paired close/open two-side fee semantics and reconcile to reported fee sides.
- Constant-long-ZN and deterministic random-position baselines are recorded as null-attribution evidence only, not alpha statistics.
- The Opus scalar heuristic is recorded honestly: final capped S27 ZN forecasts are materially below the [9, 11] mean-absolute heuristic on this single-instrument sample. No retuning was performed.

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_OPUS_ROUND2_MECHANICAL_BLOCKERS_CLOSED_WITH_SCALAR_HEURISTIC_CAVEAT
SCALAR_HEURISTIC_FAILURES_RECORDED: 2
```

This closes the mechanical evidence gaps requested by Opus Round 2. It does not convert the result into an alpha claim or authorize promotion. The scalar calibration evidence is a caveat: it weakens a strong source-faithful scalar claim for single-instrument ZN, but it was not treated as a reason to tune or rewrite the result.

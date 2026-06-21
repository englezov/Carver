# CARVER S27 ZN V2 2023 TEST Fast Order-Intent Generator

Date: 2026-06-20

Status: LOCAL_PASS_FAST_ORDER_INTENT_GENERATOR_AFTER_LOCAL_REAUDIT_REMEDIATION_NOT_RESULT

## Scope

This record closes the fast order-intent generator slice of the S27_V2 TEST runner performance remediation.

The implemented surface is:

- `src/carver/spine/s27_v2_replay/fast_order_generator.py`
- `tests/test_s27_v2_fast_order_generator.py`

The slice generates desired-position, adjacent-limit/no-limit metadata, no-market metadata, and market-order intent rows for the validated row `704` through row `1377` segment. It consumes:

- the fast primitive row engine bundle;
- validated primitive rows;
- the active incremental segment bundle;
- validated fast segment artifacts;
- a bounded order-policy registry re-derived from active segment artifacts.

It does not generate fill, transition, cost, PnL, result, backtest, or source-faithful evidence rows. Until fill/transition/cost/PnL generation is extracted, state carry is explicitly bounded to the validated `fill_ledger.csv` `position_after_fill` values from the active segment artifacts.

## Implementation Notes

`FastOrderPolicyRegistry` is rebuilt from active segment artifacts. It binds desired-position, limit-order, no-market, market-order, and fill row hashes per row, and rejects:

- artifact binding drift;
- policy row-count drift;
- self-consistent policy row-hash drift;
- registry hash drift;
- non-authorization drift.

`FastOrderGenerationBundle.validate()` now revalidates `FastSegmentArtifacts` against the active incremental segment and active fast execution-state verification before using artifacts as parity authority.

Generated row validation now recomputes every row's `row_hash` from row payload content before comparing generated rows with active artifact row hashes. This closes stale-row-hash payload forgery where a caller mutates row content but preserves the original `row_hash`.

Exact row-hash parity is enforced for:

- `desired_position_ledger.csv`;
- `limit_order_ledger.csv`;
- `no_market_order_ledger.csv`;
- `market_order_ledger.csv`.

The generator remains intentionally excluded from the package-root `__all__`.

## Verification

Focused verification passed:

```text
python -m py_compile src/carver/spine/s27_v2_replay/fast_order_generator.py tests/test_s27_v2_fast_order_generator.py
```

```text
python -m pytest tests/test_s27_v2_fast_order_generator.py
9 passed in 61.48s
```

Broader focused remediation suite passed:

```text
python -m pytest tests/test_s27_v2_test_incremental_runner.py tests/test_s27_v2_fast_runner_cache.py tests/test_s27_v2_fast_row_engine.py tests/test_s27_v2_fast_execution_state.py tests/test_s27_v2_fast_segment_emitter.py tests/test_s27_v2_fast_evidence_planner.py tests/test_s27_v2_fast_order_generator.py
68 passed in 130.31s
```

Forbidden-surface scan returned no matches for proof-heavy runner use, provider/API/download surfaces, result/source-faithful claims, or Git surfaces in the new module/test.

## Local Hostile Audit

A read-only local hostile audit initially found two P1 issues:

1. Generated-row forgery could pass if row content was mutated while the stale original `row_hash` was preserved and bundle/check hashes were recomputed.
2. `FastOrderGenerationBundle.validate()` accepted caller-supplied `FastSegmentArtifacts` as parity authority without revalidating artifacts against active files.

Remediation added:

- per-row generated `row_hash` payload recomputation inside `_validate_generated_row_hashes()`;
- active `FastSegmentArtifacts.validate()` anchoring inside `FastOrderGenerationBundle.validate()`;
- stale-row-hash payload mutation regression;
- forged artifact authority regression.

The local re-audit returned:

- P0: none;
- P1: none;
- P2: none;
- P3: none.

The re-audit explicitly confirmed the two prior P1s are closed and that local continuation may proceed.

## Non-Authorizations Preserved

This slice did not authorize or perform:

- provider/API access;
- downloads or new data acquisition;
- TEST continuation;
- VALIDATION, OOS, Lockbox, or Forward access;
- result interpretation;
- PnL evaluation beyond mechanical construction;
- tuning;
- Git staging, commit, push, or PR;
- GPT/Opus packet preparation;
- adapter work;
- deployment;
- trading;
- promotion;
- source-faithful evidence claims.

## Next Work

The next remediation slice is fast fill/transition/cost/PnL generation from generated order-intent rows and bounded policy/evidence registries, followed by incremental validation against the active segment artifacts. The existing proof-heavy runner remains checkpoint-only and is not the operational continuation path.

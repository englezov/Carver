# CARVER S27 ZN V2 2023 TEST Fast Downstream Generator

Date: 2026-06-20

Status: LOCAL_PASS_FAST_DOWNSTREAM_GENERATOR_AFTER_LOCAL_REAUDIT_REMEDIATION_NOT_RESULT

## Scope

This record closes the fast downstream generator slice of the S27_V2 TEST runner performance remediation.

The implemented surface is:

- `src/carver/spine/s27_v2_replay/fast_downstream_generator.py`
- `tests/test_s27_v2_fast_downstream_generator.py`

This slice binds and validates downstream row families for the row `704` through row `1377` segment:

- `working_order_transition_ledger.csv`;
- `fill_ledger.csv`;
- `market_fill_metadata_ledger.csv`;
- `cost_ledger.csv`;
- `pnl_ledger.csv`;
- `validation_ledger.csv`.

It consumes the fast primitive bundle, active incremental segment bundle, validated segment artifacts, fast order-intent generation bundle, generated order-intent rows, and a bounded downstream policy registry. It does not call the proof-heavy `test_mechanical_run.py` runner.

This is mechanical row construction/parity and incremental verification only. It is not result interpretation, not PnL evaluation, not promotion, and not a source-faithful evidence claim.

## Implementation Notes

`FastDownstreamPolicyRegistry` is re-derived from active segment artifacts and generated order-intent rows. Its validation requires:

- active segment artifact authority validation;
- full upstream `FastOrderGenerationBundle.validate()` with primitive, segment, artifact, and order-policy context;
- policy row hash validation;
- registry hash validation;
- non-authorization preservation.

`FastDownstreamGenerationBundle.validate()` checks:

- primitive, segment, artifact, order, and downstream registry binding;
- dense row-family counts for transition, fill, cost, PnL, and validation rows;
- sparse market-fill metadata row count;
- unique row indexes across all downstream row families, including sparse `market_fill_metadata_rows`;
- full-row parity against active segment artifacts for all downstream row families;
- position carry from the row-703 checkpoint through the segment;
- transition/fill/PnL ending-position coherence;
- market-fill metadata side, quantity, fill price, position, timestamp/symbol presence, provenance, and source-hash presence;
- commission plus spread equals total cost;
- row gross PnL less total cost equals row net PnL;
- cumulative gross, commission, spread, and net PnL roll-forward from the row-703 checkpoint;
- result/backtest/source-faithful fail-closed flags.

The upstream fast order generator was also hardened during this checkpoint. `FastOrderGenerationBundle.validate()` now rejects duplicate row indexes and row-count drift across desired, limit, no-market, and sparse market-order generated rows before parity can collapse duplicate indexes.

## Verification

Focused verification passed:

```text
python -m py_compile src/carver/spine/s27_v2_replay/fast_order_generator.py src/carver/spine/s27_v2_replay/fast_downstream_generator.py tests/test_s27_v2_fast_order_generator.py tests/test_s27_v2_fast_downstream_generator.py
```

```text
python -m pytest tests/test_s27_v2_fast_order_generator.py tests/test_s27_v2_fast_downstream_generator.py
23 passed in 328.39s
```

Broader focused remediation suite passed:

```text
python -m pytest tests/test_s27_v2_test_incremental_runner.py tests/test_s27_v2_fast_runner_cache.py tests/test_s27_v2_fast_row_engine.py tests/test_s27_v2_fast_execution_state.py tests/test_s27_v2_fast_segment_emitter.py tests/test_s27_v2_fast_evidence_planner.py tests/test_s27_v2_fast_order_generator.py tests/test_s27_v2_fast_downstream_generator.py
82 passed in 394.87s
```

Forbidden-surface scan returned no matches for proof-heavy runner use, provider/API/download surfaces, result/source-faithful claims, or Git surfaces in the order/downstream modules and tests.

## Local Hostile Audit

A read-only local hostile audit initially found:

- P1: duplicate row-index forgery could bypass downstream parity by appending duplicate generated rows before `_rows_by_index()` collapse.
- P2: registry-only validation did not fully validate upstream order-bundle authority.
- P2: market-fill metadata coherence was thinner than the named requirement.

Remediation added:

- dense generated row-family count validation;
- unique row-index validation across downstream row families including sparse market-fill metadata;
- strict downstream registry validation requiring full upstream order-bundle validation context;
- market-fill metadata side/quantity/price/position/timestamp/symbol/provenance/source-hash checks;
- duplicate dense row-index and duplicate sparse market-fill row-index regressions;
- forged order-bundle authority regression;
- forged artifact authority regression;
- market-fill metadata binding drift regression.

The second re-audit found one inherited upstream P2 in `fast_order_generator.py`: duplicate order rows could collapse by row index. Remediation added:

- dense generated order row-count checks;
- sparse market-order row-count checks;
- unique row-index checks across desired, limit, no-market, and market-order generated rows;
- duplicate dense order-row and duplicate sparse market-order regressions.

Final local re-audit returned:

- P0: none;
- P1: none;
- P2: none;
- P3: none.

The final audit confirmed local continuation may proceed.

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

The next remediation slice is integration of generated order/downstream rows into compact segment artifact assembly and incremental checkpoint verification, so continuation can use generated segment rows rather than existing full-run artifact slices. The proof-heavy runner remains checkpoint-only and is not the operational continuation path.

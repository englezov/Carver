# CARVER S27 ZN V2 - 2023 TEST Row 547 Cap-Bound Adjacent-Limit Policy And Local Audit

Date: 2026-06-14

## Scope

Operator authorized the S27_V2 2023 TEST row-547 adjacent-limit formula policy/source-lock and implementation gate after local PASS on row-441 extended-lookback TBBO implementation and continuation to row 547.

Scope was limited to already-local 2023 TEST artifacts and audited S27_V2 machinery. No provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Row 547 Facts

- row index: `547`
- decision timestamp: `2023-02-07T00:00:00Z`
- raw symbol: `ZNH3`
- starting position: `26`
- desired position: `25`
- position change: `SELL 1`
- adjacent target: `25`
- same session: `TRUE`
- trend: `0.43902119250205374`
- base position: `12.363067774093599`
- target capped forecast implied by adjacent target 25: `20.221518199865148`
- forecast cap: `20.0`

## Decision

Row 547 is not a target-zero policy case. It is a cap-bound adjacent-limit formula case.

The adjacent target position `25` implies a capped forecast above the source-locked cap. The inverse adjacent-limit price is therefore not uniquely priceable by the existing source-locked formula. Current source/process evidence does not authorize extending the formula across the capped forecast plateau.

Therefore row 547 remains fail-closed under the explicit status:

`FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_CAP_BOUND_TARGET_NOT_RESULT`

No continuation past row 547 is authorized by this record.

## Implementation

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` now distinguishes cap-bound adjacent targets from the older target-zero fail-closed label.

The prior generic/stale label:

`FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_TARGET_POSITION_ZERO_NOT_RESULT`

is no longer used for row 547. Row 547 now emits:

`FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_CAP_BOUND_TARGET_NOT_RESULT`

The patch does not relax the adjacent-limit formula. It only classifies the fail-closed blocker accurately.

## Verification

Passed:

`python -m pytest tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_pack_is_declared_and_stops_at_first_fail_closed_blocker tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_row547_cap_bound_adjacent_limit_remains_fail_closed tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_self_consistent_row441_source_drift -q`

Result: `5 passed in 436.83s`.

## Artifact Hashes

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`: `030A2A282A36B6052426A79227D5CD14A6DF0B8453EC08AAF41F56E60A5E17F9`
- `tests/test_s27_v2_2023_test_mechanical_run.py`: `FA23FE5F70718834A3F21295D82AD919F8C575C387A9A5A179E036B271B8C869`
- declared TEST pack manifest: `694B00E0AEA3F75DB6EBA99D341F7EFB8958D59E4FA832F39148C12145149357`
- run manifest: `6B03C968B092432616853EC48ADD85D0264A594A53B7490720C23F2A2825DF1F`
- evidence manifest: `FAE27F7E593403ACC499C03D4EA0FEB0F5AA0804E1F05E3F33EB62D8886CDEB0`
- trusted bundle: `C1E5617109CCEBB2427C242775DA1655871776E2027DA48AE71E4165EB312414`
- TBBO requirements ledger: `23A2542B22FAA14713902F0B5BDF058D0AA98852FAED74A2F103B9B1DEC03601`

## Local Hostile Audit

P0 findings: none.

P1 findings: none.

P2 findings: none.

Audit checks:

- row 547 remains the terminal row;
- no rows after row 547 were consumed;
- the cap-bound adjacent target is not silently priced;
- result/backtest/source-faithful gates remain fail closed;
- package root still exports only the fail-closed replay boundary;
- no provider/API/download/new-data/protected-window/Git/tuning/adapter/deployment/trading/promotion surface was introduced;
- the status change is classification-only and does not authorize result interpretation or continuation.

## Current Status

`LOCAL_PASS_2023_TEST_ROW547_CAP_BOUND_ADJACENT_LIMIT_FAIL_CLOSED_NOT_RESULT`

The next useful gate is an explicit cap-bound adjacent-limit policy decision gate. That gate must decide whether to keep cap-bound adjacent targets fail-closed or accept a narrowly labeled local-only engineering convention for pricing orders whose adjacent target is inside the forecast-cap plateau.

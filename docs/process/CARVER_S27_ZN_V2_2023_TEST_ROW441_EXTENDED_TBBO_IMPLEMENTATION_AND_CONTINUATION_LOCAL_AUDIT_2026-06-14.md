# CARVER S27 ZN V2 - 2023 TEST Row 441 Extended TBBO Implementation And Continuation Local Audit

Date: 2026-06-14

## Scope

Operator authorized the S27_V2 2023 TEST row-441 extended-lookback TBBO implementation and mechanical continuation gate after PASS on bounded row-441 extended TBBO evidence.

Scope was limited to already-local 2023 TEST artifacts and the selected row-441 quote. No provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Implementation

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` now includes the row-441 extended-lookback selected spread registry in the active combined market-order TBBO registry.

The row-441 evidence type is explicit:

`ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO`

The accepted selection status is explicit:

`PASS_ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT`

The row-specific max selected quote age is `300.0` seconds only for the row-441 extended-lookback evidence type. Normal selected TBBO rows remain limited to `5.0` seconds and retry rows remain limited to `60.0` seconds.

The selected row-441 quote remains labeled:

`ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT`

## Row 441 Mechanical Construction

Row 441 emitted deterministic local-only market-order/fill/cost/mechanical-PnL metadata:

- row index: `441`
- decision timestamp: `2023-01-31T04:00:00Z`
- fill timestamp: `2023-01-31T05:00:00Z`
- raw symbol: `ZNH3`
- starting position: `17`
- desired position: `14`
- position change: `SELL 3`
- selected TBBO quote timestamp: `2023-01-31T04:57:05.652860819Z`
- quote age: `174.34714`
- selected bid: `114.359375`
- selected ask: `114.375`
- executable SELL market fill price: `114.359375`
- full spread: `0.015625` points
- commission: `6.8999999999999995 USD`
- spread cost: `0.0 USD` under bid-fill/no-separate-spread accounting
- total cost: `6.8999999999999995 USD`
- valuation mark timestamp: `2023-01-31T06:00:00Z`
- valuation mark close: `114.359375`
- ending position: `14`
- row gross PnL: `0.0`
- row net PnL: `-6.8999999999999995`

This is mechanical construction only. Result/backtest/source-faithful evidence gates remain fail closed.

## Continuation Result

The regenerated controlled 2023 TEST mechanical artifact run now supports rows `1` through `546` and fails closed at row `547`.

Row 547 blocker:

- row index: `547`
- decision timestamp: `2023-02-07T00:00:00Z`
- raw symbol: `ZNH3`
- starting position: `26`
- desired position: `25`
- position change: `SELL 1`
- adjacent target: `25`
- same session: `TRUE`
- fail-closed reason: `FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_TARGET_POSITION_ZERO_NOT_RESULT`

No TEST rows after row 547 were consumed.

## Artifact Hashes

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`: `63A0E3B9DFAF130324AEE0AA398ABC8750A8F0C4EC889E59D4CD91845F763832`
- `tests/test_s27_v2_2023_test_mechanical_run.py`: `5E6325FCFAF91261D9737780BA50383DBB8963017854EE418D3C905C9387CC87`
- row-441 selected spread registry: `0A2EC015D252A08E2AC6BFE5BBE8FFD60969C97E6C409609DC6CAF593E3E379F`
- combined market TBBO registry: `5C3C8095B8A41B39D802F3D3CFBCCDCF8D419F24C2343B0D0F07E45D20EAD01E`
- combined market TBBO registry manifest: `160F857E8286660C8D36B7FCFE70C258BF224B258B8F58CF7EE1DBEBEB52D88B`
- combined market TBBO SHA256 manifest: `2E6F241BC8D728B2AD355F1D137CCE6CD3B9012FBEFDD8209F629CC6EB0AF6A6`
- TBBO requirements ledger: `23A2542B22FAA14713902F0B5BDF058D0AA98852FAED74A2F103B9B1DEC03601`
- run manifest: `1710E9D8559A7AA7526E23CF6920DC67E3B56BB70012F03D565C1D63F1D5CEDA`
- evidence manifest: `DE6725B0B56AE0D0EEAB3713FDC580E86B421D8386EA116BFD18151C91B2D276`
- trusted bundle: `4CE0DF032249B58114D013E1FE73CCAEE97F83DC1490CE517A4100FDC13EB730`
- run `SHA256SUMS.csv`: `18B7717D395FDE196BB1D8CF63318E69411AFC038E4EA4483A148F1C42BA8711`

## Verification

Passed:

`python -m py_compile src/carver/spine/s27_v2_replay/test_mechanical_run.py tests/test_s27_v2_2023_test_mechanical_run.py`

Passed:

`python -m pytest tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_pack_is_declared_and_stops_at_first_fail_closed_blocker tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_self_consistent_row441_source_drift -q`

Result: `4 passed in 404.14s`.

## Local Hostile Audit

P0 findings: none.

P1 findings: none.

P2 findings: none.

Audit checks:

- row-441 evidence is explicit and row-specific;
- the 300-second quote-age allowance is confined to `ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO`;
- source selected registry bytes hash to `0A2EC015D252A08E2AC6BFE5BBE8FFD60969C97E6C409609DC6CAF593E3E379F`;
- combined registry row 441 binds source selected row hash `ba1cb81b085b3b6ea2badc6ec01852ab4222d679047625ff0bc46dde17e83051`;
- active combined registry row 441 hash is `7e3f3b721a197c7a49a0f26f854ab2978b67c2080b5941bbed12075c3c0530fc`;
- row-441 cost row binds active combined registry hash `5c3c8095b8a41b39d802f3d3cfbccdcf8d419f24c2343b0d0f07e45d20ead01e`;
- TBBO requirements discovery reports `110` total market-order requirements, `110` already bound, and `0` missing;
- package root still exports only the fail-closed replay boundary;
- validation rows preserve result/backtest/source-faithful gates fail closed;
- no provider/API/download/new-data/protected-window/Git/tuning/adapter/deployment/trading/promotion surface was introduced.

## Current Status

`LOCAL_PASS_2023_TEST_ROW441_EXTENDED_TBBO_IMPLEMENTED_AND_CONTINUED_TO_ROW547_ADJACENT_LIMIT_FORMULA_BLOCKER_NOT_RESULT`

The next useful gate is a row-547 adjacent-limit formula policy/source-lock gate. External GPT/Opus audits remain deferred until a consolidated checkpoint unless separately authorized.

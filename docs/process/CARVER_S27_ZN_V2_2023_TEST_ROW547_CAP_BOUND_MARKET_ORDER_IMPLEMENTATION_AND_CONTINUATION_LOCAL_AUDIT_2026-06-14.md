# CARVER S27 ZN V2 - 2023 TEST Row 547 Cap-Bound Market-Order Implementation And Continuation Local Audit

Date: 2026-06-14

## Scope

Operator authorized the S27_V2 2023 TEST cap-bound market-order class implementation and mechanical continuation gate after the cap-bound adjacent-limit policy decision gate.

Scope was limited to already-local 2023 TEST artifacts, audited S27_V2 machinery, and bounded TBBO evidence only where required. Provider access was authorized only for the row-547 fill-candidate quote window if row-547 bid/ask evidence was missing.

No broad provider/API access, downloads, new data acquisition outside bounded row-547 TBBO evidence, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Row 547 Implementation

Row 547 facts:

- raw symbol: `ZNH3`
- decision timestamp: `2023-02-07T00:00:00Z`
- fill candidate timestamp: `2023-02-07T01:00:00Z`
- starting position: `26`
- desired position: `25`
- position change: `SELL 1`
- adjacent target: `25`
- implied target capped forecast: `20.221518199865148`
- forecast cap: `20.0`
- same-session: `TRUE`

The runner now treats this exact cap-bound class as market-order required under:

`BOOK_REQUIRED_CAP_BOUND_LIMIT_SIDE_NOT_PLACED`

The runner does not emit a cap-edge limit price. The row-547 order plan uses:

`NOT_APPLICABLE_CAP_BOUND_MARKET_ORDER_LIMIT_SIDE_NOT_PLACED`

for both formula limit price and limit order price.

## Bounded TBBO Evidence

Added row-specific acquisition tool:

`tools/databento/carver_s27_v2_2023_test_row547_cap_bound_market_order_tbbo_acquisition.py`

The tool is locked to row `547`, `ZNH3`, and request window:

`2023-02-07T00:59:55Z` through `2023-02-07T01:00:05Z`

Selected TBBO evidence:

- selected quote timestamp: `2023-02-07T00:59:55.061867017Z`
- quote age: `4.9381329999999997`
- bid: `113.546875`
- ask: `113.5625`
- side: `SELL`
- executable fill price: `113.546875`
- spread points: `0.015625`
- selected spread registry SHA256: `18D974D5EEDE3C99521D2043C2B76470458E1B59450AFCDAF74B703C5C72D22C`
- raw DBN SHA256: `A0F66D0EB9D0B4ED489BA72B999E31951C41D78CE915D73E59950C9771185F8A`
- raw CSV SHA256: `A4568804C1FC7EA2723E40B6913F41BF8F568E031C57DDADEC83D17AE0042EFA`

## Mechanical Continuation Result

The regenerated controlled 2023 TEST mechanical artifact run supports rows `1` through `553` and fails closed at row `554`.

Row 547 emitted local-only mechanical metadata:

- market order: `SELL 1`
- fill price: `113.546875`
- fill rule: `MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE`
- commission: `2.3 USD`
- spread cost: `0.0 USD` under bid-fill/no-separate-spread accounting
- valuation mark: `2023-02-07T02:00:00Z`
- ending position: `25`

Row 554 blocker:

- decision timestamp: `2023-02-07T07:00:00Z`
- starting position: `25`
- desired position: `23`
- position change: `SELL 2`
- fail-closed reason: `FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT`

No rows after row 554 were consumed by the mechanical run.

## Artifact Hashes

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`: `742EA20007D6BF7B65CA35C63D3DEA187728571F805292766E6F6AAF43BB4416`
- `src/carver/spine/s27_v2_replay/pretest_machine_freeze.py`: `A97EDF263EC1DA4FD652289550E0648ECA627F6C6DB71C7A32B3452F9FA115A3`
- `tests/test_s27_v2_2023_test_mechanical_run.py`: `93B2DE062BD29CAA25549E062C520E193B0F9B8A0D731FB0394E9C7882AC08AC`
- row-547 TBBO acquisition tool: `6B824147DF3185035597DEE2AD668535D91480021334370B1B556E5EEE59DAFB`
- row-547 TBBO evidence process record: `28E12E140EEF70486E43B24E70080018BB878AD729311CCEED26978B9AA77CEA`
- combined market-order TBBO registry: `F40056CD0159AB6BB573C4D258EC5867EC9466424C837EB6B37C0DC98B9D5A62`
- run manifest: `E50AB6DA52446A6F0179F296BC0184CAECF1A9226EA74671F3C17FFC20D8F290`
- evidence manifest: `21E85700A0951351018BBC9B8386A4D65DED53309B8EA44B6F2737B85F341D79`
- trusted bundle: `BB7F93E8DD322E13D4CBD8CAC19AB38B54258D247B7DB054040E0DAACEB25ED7`
- TBBO requirements ledger: `97538DD5ECE18A6876F36DAD628C81B8128C4B7BB5D8218A69D0732433D4C2EE`

Run bundle:

- bundle hash: `95288540F9E251CF1B3A130FA9A4A0A97938476F21DA06A1CA6F51A7CBB71D98`
- final position: `25`
- cumulative gross PnL metadata: `-19562.5`
- cumulative commission metadata: `1184.5000000000002`
- cumulative spread metadata: `0.0`
- cumulative net PnL metadata: `-20747.0`

These are mechanical ledger fields only, not result interpretation, performance evaluation, source-faithful evidence, promotion, deployment, or trading.

## Verification

Passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py src\carver\spine\s27_v2_replay\pretest_machine_freeze.py tests\test_s27_v2_2023_test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_row547_cap_bound_market_order_tbbo_acquisition.py
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_pack_is_declared_and_stops_at_first_fail_closed_blocker tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_row547_cap_bound_market_order_is_bounded_and_row554_blocks tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_bundle_rejects_self_consistent_row547_cap_bound_trigger_forgery -q
```

Result:

```text
5 passed in 552.23s
```

A broader `pytest -k` guard selection was attempted but timed out before completion and produced no pass/fail result. It is not claimed as passing.

## Local Hostile Audit

P0 findings: none.

P1 findings: none.

P2 findings: none.

Audit checks:

- row 547 does not emit a fabricated cap-edge adjacent-limit price;
- row 547 market-order trigger is `BOOK_REQUIRED_CAP_BOUND_LIMIT_SIDE_NOT_PLACED`, not the gap-greater-than-one trigger;
- the pretest machine-freeze guard allows a one-contract market order only when the cap-bound no-limit-price marker is present;
- row 547 TBBO evidence is row-specific, fresh, non-crossed, source-byte/hash bound, and selected at or before the fill timestamp;
- self-consistent row-547 trigger forgery is rejected by bundle validation;
- result/backtest/source-faithful gates remain fail closed;
- the run stops at row 554 and does not consume rows after row 554;
- package-root exports remain narrow;
- no broad provider/API/download/new-data/protected-window/Git/GPT/tuning/adapter/deployment/trading/promotion/source-faithful surface was introduced.

## Current Status

`LOCAL_PASS_2023_TEST_ROW547_CAP_BOUND_MARKET_ORDER_IMPLEMENTED_AND_CONTINUED_TO_ROW554_MARKET_TBBO_BLOCKER_NOT_RESULT`

The next useful gate is bounded TBBO evidence and mechanical continuation for row `554`, or a consolidated bounded market-order TBBO acquisition gate for the currently missing TEST requirements. External GPT/Opus audits remain deferred until a consolidated checkpoint unless separately authorized.

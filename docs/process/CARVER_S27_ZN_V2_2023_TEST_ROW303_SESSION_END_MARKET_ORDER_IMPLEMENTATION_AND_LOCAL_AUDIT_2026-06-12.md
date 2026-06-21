# S27 V2 ZN 2023 TEST Row 303 Session-End Market-Order Implementation And Local Audit

Date: 2026-06-12

Status:

```text
LOCAL_PASS_ROW303_SESSION_END_MARKET_ORDER_IMPLEMENTATION_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the authorized local-only S27_V2 2023 TEST row-303
session-end market-order implementation gate.

The gate is limited to already-local 2023 TEST artifacts and already-acquired
TBBO evidence. It authorizes no provider/API access, downloads, new data,
broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox,
Forward, result interpretation, PnL evaluation beyond mechanical row
construction, tuning, adapter/deployment/trading/promotion, Git action, GPT
packet preparation, or source-faithful evidence claim.

## Implementation

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` now contains a bounded
row-303 session-end market-order policy helper.

The exception is accepted only when all of the following row facts match:

```text
row_index = 303
raw_symbol = ZNH3
order_side = BUY
position_change_contracts = 2
decision_timestamp_utc = 2023-01-20T20:00:00Z
fill_timestamp_utc = 2023-01-20T21:00:00Z
valuation_mark_timestamp_utc = 2023-01-20T22:00:00Z
decision/fill same session = TRUE
fill timestamp equals declared session end = TRUE
valuation mark is exact next completed hourly row after fill = TRUE
valuation label = SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
```

If any fact drifts, the runner keeps the existing session/EOD fail-closed path.
The exception does not authorize broader EOD/overnight handling, deferred fills,
working-order carry, roll-boundary execution, result rows, backtest rows,
promotion, or source-faithful evidence claims.

## Row 303 Emission

Row 303 now emits deterministic local-only mechanical metadata:

```text
market_order: BUY 2, current position 5, target position 7
fill timestamp: 2023-01-20T21:00:00Z
fill price: 115.03125
fill provenance: MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE
TBBO quote timestamp: 2023-01-20T20:59:59.951210763Z
TBBO bid/ask: 115.015625 / 115.03125
commission amount: 4.6 USD
spread cost amount: 0.0 USD
valuation mark: 2023-01-20T22:00:00Z close 115.046875
row gross mechanical PnL: 187.5
row net mechanical PnL: 182.9
```

The row preserves:

```text
result_status = FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status = FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
pnl_evaluation_status = MECHANICAL_PNL_ROW_CONSTRUCTION_ONLY_NOT_RESULT_INTERPRETATION
source_faithful_evidence_claimed = FALSE
```

## Current Mechanical Run State

Current artifact root:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run
```

Current state:

```text
candidate rows = 304
supported mechanical rows = 303
emitted market-order rows = 34
terminal fail-closed row = 304
terminal timestamp = 2023-01-20T21:00:00Z
terminal reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
final supported position = 7
cumulative gross mechanical PnL = 6375.0
cumulative commission = 301.3
cumulative spread = 0.0
cumulative net mechanical PnL = 6073.7
```

The current terminal fail-closed row 304 is:

```text
raw_symbol = ZNH3
starting_position_contracts = 7
desired_position_contracts = 9
position_change_contracts = 2
order_side = BUY
fill_candidate_timestamp_utc = 2023-01-20T22:00:00Z
same_session = FALSE
```

Row 304 emits no market order, fill, cost, PnL, result, backtest, or
source-faithful evidence row.

## Hashes

```text
input_manifest_sha256 = 72A65157E2B5BF2E519CBFABFE84C7B9F9737D3C2572A65F9EDACD88D6F361AB
run_manifest_sha256 = C7975059AC4AFE593D57DD0F9ED2BE83A694B019BA956CBDAB65CB17E1574796
evidence_manifest_sha256 = 9B03D35D83AEB1DE3BE2E5C4B5501FF30E5E88AC4D3E201322A01DDC6693FBDE
trusted_bundle_sha256 = 728354DE79D44BEB4A92B5BD9D250E0F979F80A6C3977230B44BAA9399BBDF40
combined_tbbo_registry_sha256 = BD3BA4E2C0ACC8A13C50D5F24410D852522F8127FFF66980A0D35D1AE72ACDEA
```

## Verification

Commands:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

```text
48 passed
109 passed
```

Additional local hash verification:

```text
run SHA256SUMS.csv = PASS, 17 files
evidence_manifest ledger hashes = PASS
trusted_bundle evidence hash = PASS
```

## Local Hostile Audit

One read-only local hostile-audit subagent returned:

```text
PASS_NO_P0_P1_P2
```

Audit checks:

- row 303 is exactly bounded to the authorized facts;
- row 303 emits only market/fill/cost/mechanical PnL metadata;
- result/backtest/source-faithful evidence remains fail-closed;
- row 303 consumes combined TBBO registry evidence;
- row 304 remains the single fail-closed blocker;
- no provider/API/download/new-data/VALIDATION/OOS/Lockbox/Forward/Git/tuning/
  adapter/deployment/trading/promotion/source-faithful surface was introduced.

## Current Status

```text
LOCAL_PASS_2023_TEST_ROW303_SESSION_END_MARKET_ORDER_CONTINUATION_TO_ROW304_SESSION_EOD_BLOCKER_NOT_RESULT
```

The next useful gate is a narrow row-304 session/EOD policy or implementation
decision. VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL
evaluation beyond mechanical row construction, tuning, adapter/deployment/
trading/promotion, Git actions, GPT packet preparation, and source-faithful
evidence claims remain unauthorized.

## Non-Authorization

This record authorizes no provider/API access, no downloads, no new data, no
VALIDATION, no OOS, no Lockbox, no Forward, no result interpretation, no PnL
evaluation beyond mechanical row construction, no tuning, no adapter work, no
deployment, no trading, no promotion, no Git actions, no GPT packet
preparation, and no source-faithful evidence claim.

# S27 V2 ZN 2023 TEST Row 391 Session-End Market-Order Implementation And Local Audit

Date: 2026-06-13

Status:

```text
LOCAL_PASS_2023_TEST_ROW391_SESSION_END_MARKET_ORDER_IMPLEMENTED_TO_ROW392_SESSION_EOD_BLOCKER_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the authorized local-only S27_V2 2023 TEST row-391
session/EOD market-order policy and implementation gate.

The gate was limited to already-local 2023 TEST artifacts and already-bound
TBBO evidence. It authorized no provider/API access, downloads, new data,
broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox,
Forward, result interpretation, PnL evaluation beyond mechanical construction,
tuning, adapter/deployment/trading/promotion, Git action, GPT packet
preparation, or source-faithful evidence claim.

## Implementation

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` now contains a bounded
row-391 session-end market-order helper and accepting-path validator.

The row-391 exception is accepted only when all of the following facts match:

```text
row_index = 391
raw_symbol = ZNH3
order_side = BUY
position_change_contracts = 8
decision_timestamp_utc = 2023-01-26T20:00:00Z
fill_timestamp_utc = 2023-01-26T21:00:00Z
valuation_mark_timestamp_utc = 2023-01-26T22:00:00Z
decision/fill same session = TRUE
fill timestamp equals declared session end = TRUE
valuation mark is exact next completed hourly row after fill = TRUE
valuation label = SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
standing TBBO source = STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO
selected quote timestamp = 2023-01-26T20:59:59.902217027Z
selected ask = 114.828125
```

If any fact drifts, the runner keeps the session/EOD fail-closed path or the
accepting validator rejects the artifact bundle. The exception does not
authorize broader EOD/overnight behavior, deferred fills, working-order carry,
roll-boundary execution, result rows, backtest rows, promotion, or
source-faithful evidence claims.

## Row 391 Emission

Row 391 emits deterministic local-only mechanical metadata:

```text
market_order: BUY 8, current position 4, target position 12
fill timestamp: 2023-01-26T21:00:00Z
fill price: 114.828125
fill provenance: MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE
TBBO quote timestamp: 2023-01-26T20:59:59.902217027Z
TBBO bid/ask: 114.8125 / 114.828125
commission amount: 18.4 USD
spread cost amount: 0.0 USD
valuation mark: 2023-01-26T22:00:00Z close 114.8125
row gross mechanical PnL: -125.0
row net mechanical PnL: -143.4
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
candidate rows = 392
supported mechanical rows = 391
emitted market-order rows = 62
terminal fail-closed row = 392
terminal timestamp = 2023-01-26T21:00:00Z
terminal reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
final supported position = 12
cumulative gross mechanical PnL = 8671.875
cumulative commission = 611.8
cumulative spread = 0.0
cumulative net mechanical PnL = 8060.075
```

The current terminal fail-closed row 392 is:

```text
raw_symbol = ZNH3
decision_timestamp_utc = 2023-01-26T21:00:00Z
starting_position_contracts = 12
desired_position_contracts = 15
position_change_contracts = 3
order_side = BUY
fill_candidate_timestamp_utc = 2023-01-26T22:00:00Z
same_session = FALSE
```

Row 392 emits no market order, fill, cost, PnL, result, backtest, or
source-faithful evidence row.

## Hashes

```text
input_manifest_sha256 = 921F0F19BAD0A5F898407D0C7C3F2A63A7DABB2812B584476AE15B61B64BA540
run_manifest_sha256 = C6AF3D88E9254124AAFB911409302A2F952C4E0DD9CEDACB2568857BF1582685
evidence_manifest_sha256 = C43FF54774F961E08BE241F440105DFA45EEE69D6D07346FF6FD67414FCBD8F2
trusted_bundle_sha256 = 6910F53D82D65FE72D5F5D529C095A8C50E098C49A8FB0F84D212C9531F60D40
run_bundle_sha256 = 9821A42E787CE6F74B6C625F04813CA7B892CCC470891A8F4D95DEF9473AACD2
combined_tbbo_registry_sha256 = BB0B7E50E713E63701F1BCE83CB974DADD4DA419E2387006018623470756B367
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
97 passed
158 passed
```

Focused tests now bind row-391 emitted market-order, fill, cost, and
mechanical PnL rows, and reject self-consistent forged row-391 mutations after
row/evidence/trusted/bundle hash refresh across timestamp, quantity, target,
fill timestamp/price, same-session flag, TBBO ask, and valuation-label fields.

## Local Hostile Audit

One read-only local hostile-audit subagent returned:

```text
PASS_NO_P0_P1_P2
```

P3:

```text
The standing-TBBO process memo is stale as a historical pre-row-391 record.
This record supersedes that memo for current row-391 status.
```

Audit checks:

- row 391 is exactly bounded to the authorized facts;
- row 391 emits only market/fill/cost/mechanical PnL metadata;
- result/backtest/source-faithful evidence remains fail-closed;
- row 391 consumes standing TBBO registry evidence;
- row 392 remains the single fail-closed blocker;
- package-root export and forbidden provider/API/download/new-data/
  VALIDATION/OOS/Lockbox/Forward/Git/tuning/adapter/deployment/trading/
  promotion/source-faithful surfaces remain absent.

## Current Status

```text
LOCAL_PASS_2023_TEST_ROW391_SESSION_END_MARKET_ORDER_IMPLEMENTED_TO_ROW392_SESSION_EOD_BLOCKER_NOT_RESULT
```

The next useful gate is a narrow row-392 session/EOD market-order policy or
implementation decision. External GPT/Opus audits remain deferred until a
consolidated phase checkpoint unless a genuinely new machinery class or final
audit requires them. VALIDATION, OOS, Lockbox, Forward, result interpretation,
PnL evaluation beyond mechanical construction, source-faithful evidence claims,
tuning, adapter/deployment/trading/promotion, Git actions, GPT packet
preparation, and promotion remain unauthorized.

## Non-Authorization

This record authorizes no provider/API access, no downloads, no new data, no
VALIDATION, no OOS, no Lockbox, no Forward, no result interpretation, no PnL
evaluation beyond mechanical row construction, no tuning, no adapter work, no
deployment, no trading, no promotion, no Git actions, no GPT packet
preparation, and no source-faithful evidence claim.

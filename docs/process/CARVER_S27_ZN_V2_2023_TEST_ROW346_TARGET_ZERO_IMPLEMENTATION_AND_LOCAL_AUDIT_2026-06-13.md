# S27_V2 2023 TEST Row-346 Target-Zero Implementation And Local Audit

Date: 2026-06-13

Status:

```text
LOCAL_PASS_2023_TEST_ROW346_TARGET_ZERO_ADJACENT_LIMIT_IMPLEMENTED_TO_ROW353_NOT_RESULT
```

## Scope

This record covers the authorized local-only row-346 target-position-zero adjacent-limit implementation gate.

Scope was limited to already-local 2023 TEST artifacts and the audited S27_V2 machinery. The row-346 class is:

```text
raw_symbol = ZNH3
decision_timestamp_utc = 2023-01-24T19:00:00Z
starting_position_contracts = 1
desired_position_contracts = 0
position_change_contracts = -1
order_side = SELL
adjacent_target_position = 0
```

This gate did not use provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.

## Implementation

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` was patched so `_formula_limit(...)` carries forward the already source-locked S27_V2 target-position permission rule:

```text
target position 0 is allowed for either nonzero trend direction
positive target positions require positive EWMAC trend
negative target positions require negative EWMAC trend
target positions at or beyond the forecast cap remain fail-closed
```

This removes the stale `target_position <= 0` blocker for the TEST mechanical runner without authorizing negative-target exits beyond the existing trend-permission rule.

The accepting path now includes `_validate_row346_target_zero_adjacent_limit_artifacts(...)`, which binds the exact row-346 source rows and emitted artifacts:

- decision row `2023-01-24T19:00:00Z`, `ZNH3`;
- fill row `2023-01-24T20:00:00Z`, `ZNH3`;
- valuation mark row `2023-01-24T21:00:00Z`, `ZNH3`;
- same declared session for decision, fill, and mark;
- positive nonzero EWMAC trend;
- formula-implied target-zero limit price equal to active EWMA5/equilibrium `114.99998579656148`;
- conservative SELL tick-rounded limit price `115.0`;
- no market-order requirement or market-order emission;
- close-only limit fill;
- commission-only limit cost using the accepted inferred retail futures cost `2.30 USD`;
- mechanical PnL metadata only, with result/backtest/source-faithful evidence gates fail-closed.

`tests/test_s27_v2_2023_test_mechanical_run.py` was updated to bind the new terminal state and add self-consistent forged-row regressions for row 346 across order, no-market, transition, fill, cost, and PnL ledgers.

## Row-346 Emitted Facts

Row 346 now emits deterministic local-only mechanical metadata:

```text
order_side = SELL
order_quantity = 1
adjacent_target_position = 0
formula_limit_price = 114.99998579656148
limit_order_price = 115.0
fill_candidate_timestamp_utc = 2023-01-24T20:00:00Z
fill_candidate_close = 115.03125
fill_executed = TRUE
fill_quantity = 1
position_after_fill = 0
commission_amount = 2.3
spread_cost_amount = 0.0
valuation_mark_timestamp_utc = 2023-01-24T21:00:00Z
valuation_mark_close_price = 115.0625
row_gross_pnl_amount = -31.25
row_net_pnl_amount = -33.55
ending_position_contracts = 0
```

These are mechanical construction fields only. They are not result interpretation, performance evaluation, source-faithful evidence, promotion evidence, or trading evidence.

## New Terminal State

After row 346 is supported, the controlled 2023 TEST mechanical run advances to the next blocker:

```text
candidate_row_count = 353
supported_mechanical_row_count = 352
fail_closed_row_index = 353
fail_closed_reason = FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

Row 353 blocker facts:

```text
decision_timestamp_utc = 2023-01-25T04:00:00Z
raw_symbol = ZNH3
starting_position_contracts = 1
desired_position_contracts = 4
position_change_contracts = 3
order_side = BUY
adjacent_target_position = 2
market_order_required = TRUE
market_order_rows_emitted = FALSE
market_spread_cost_status = FAIL_CLOSED_BOUNDED_TBBO_SPREAD_EVIDENCE_REQUIRED_FOR_NON_ROW1_MARKET_ORDER
```

Broader TEST continuation beyond row 353 remains unauthorized until a separate gate resolves or fail-closes the row-353 market-order spread evidence requirement.

## Current Hashes

Current run artifact hashes:

- `run_manifest.json`: `9d133b99d5f8ad47c67369c7b6da76b4038d42cf5d69693bf589e67241acef0b`;
- `evidence_manifest.json`: `2553fc8355e251548ea8d952822231144775a13e982665f3b7a62326ba9f9c08`;
- `trusted_bundle.json`: `fb8d84a87262624edf3717a10a0a2f7b5cc6d234d58bc2f99afeb8ad983014d6`;
- `run_bundle.json`: `695335f4713ca017dcaeccd0ee348906b437fe51c527e9bbf28f3b27dea6dc70`;
- `SHA256SUMS.csv`: `ea9cc6212ec215b5830a98184b4a32a4a9c7bc428d7006800e551ff75138bba1`;
- `fail_closed_ledger.csv`: `0735a78dd440cc68da717ae88f06fdbfe07cc479aec60afef97e573e24661739`;
- `pnl_ledger.csv`: `24b19e1fadf9feff5ce25e7dab3d05e28c312978289154a6cd81f582ef621601`;
- `limit_order_ledger.csv`: `309ba7770d601de5813e558569f4ab0ed32776150d4297cc72e96b9b407352c8`.

Local hash binding verification passed for:

- `SHA256SUMS.csv`;
- `evidence_manifest.json`;
- `trusted_bundle.json`.

## Verification

Commands run:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

```text
85 passed in 175.46s
146 passed in 165.13s
HASH_BIND_PASS
```

## Local Hostile Audit

One read-only local hostile-audit subagent returned:

```text
P0: None
P1: None
P2: None
P3: None
```

The audit confirmed:

- target-zero permission remains bounded to nonzero-trend target-position rules;
- positive targets still require positive trend and negative targets still require negative trend;
- row 346 binds exact `ZNH3` source rows, `SELL 1`, adjacent target `0`, formula limit `114.99998579656148`, SELL tick price `115.0`, same-session fill/cost/PnL metadata, and non-result boundary;
- self-consistent forged row/hash mutations for row 346 are rejected by focused tests;
- current artifacts show row 346 supported and row 353 fail-closed on missing market-order spread evidence;
- no provider/API/download/new data/VALIDATION/OOS/Lockbox/Forward/result interpretation/tuning/Git/adapter/deployment/trading/promotion/source-faithful evidence surface was found.

## Current Status

Current status:

```text
LOCAL_PASS_2023_TEST_ROW346_TARGET_ZERO_ADJACENT_LIMIT_IMPLEMENTED_TO_ROW353_NOT_RESULT
```

The next unresolved class is:

```text
FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

The next useful gate is a bounded row-353 market-order TBBO/spread evidence gate if the operator wants to continue the TEST mechanical artifact run.

## Non-Authorizations

This record does not authorize:

- provider/API access;
- downloads;
- new data acquisition;
- broader TEST continuation beyond row 353;
- VALIDATION;
- OOS;
- Lockbox;
- Forward;
- result interpretation;
- PnL evaluation beyond mechanical construction;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git staging, commit, push, or PR;
- GPT packet preparation;
- source-faithful evidence claims.

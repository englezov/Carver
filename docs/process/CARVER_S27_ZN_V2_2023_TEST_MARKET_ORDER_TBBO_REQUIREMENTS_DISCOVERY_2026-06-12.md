# S27 V2 ZN 2023 TEST Market-Order TBBO Requirements Discovery

Date: 2026-06-12

Status:

```text
LOCAL_PASS_MARKET_ORDER_TBBO_REQUIREMENTS_DISCOVERY_NOT_PROVIDER_NOT_RESULT
```

## Authorization

Operator authorized a local-only 2023 TEST market-order TBBO requirements discovery gate.

Scope was limited to already-local 2023 TEST declared/source files and audited S27_V2 mechanical runner machinery. No provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Implementation

Patched:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

Added a discovery-only entrypoint:

```text
discover_2023_test_market_order_tbbo_requirements()
```

This entrypoint:

- uses already-local 2023 TEST source rows and pre-2023 strict-prior warmup/evidence;
- does not call DataBento or any provider/API;
- does not emit result rows or source-faithful evidence;
- records every full-gap market-order row that requires bounded TBBO bid/ask evidence;
- treats rows with already-bound row-1/row-2 TBBO evidence as `ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE`;
- treats repeated missing market-order TBBO rows as requirements rather than one-row blockers;
- stops when a new non-market blocker class appears.

Discovery-only state progression assumes full-gap market orders move current position to target position so future market-order evidence requirements can be enumerated. This is not a fill/cost/PnL authorization and is not result evidence.

## Output

Output root:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_requirements_discovery
```

Files:

```text
market_order_tbbo_requirements.csv
market_order_tbbo_requirements_manifest.json
market_order_tbbo_requirements_sha256.csv
```

Manifest summary:

```text
total_market_order_rows = 52
already_bound_tbbo_count = 2
missing_tbbo_requirement_count = 50
first_missing_row_index = 59
last_missing_row_index = 343
terminal_status = STOPPED_ON_NEW_BLOCKER_CLASS_FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_TARGET_POSITION_ZERO_NOT_RESULT
provider_api_access = NO
downloads = NO
result_interpretation = NO
source_faithful_evidence_claim = NO
```

Missing requirement breakdown:

```text
ZNH3 BUY missing TBBO windows = 26
ZNH3 SELL missing TBBO windows = 24
```

First missing requirement:

```text
row_index = 59
decision_timestamp_utc = 2023-01-05T14:00:00Z
fill_candidate_timestamp_utc = 2023-01-05T15:00:00Z
raw_symbol = ZNH3
order_side = BUY
order_quantity = 10
request_start_utc = 2023-01-05T14:59:55Z
request_end_utc = 2023-01-05T15:00:05Z
```

Last missing requirement before the next blocker class:

```text
row_index = 343
decision_timestamp_utc = 2023-01-24T16:00:00Z
fill_candidate_timestamp_utc = 2023-01-24T17:00:00Z
raw_symbol = ZNH3
order_side = SELL
order_quantity = 20
request_start_utc = 2023-01-24T16:59:55Z
request_end_utc = 2023-01-24T17:00:05Z
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
py_compile PASS
47 passed
108 passed
```

Focused tests verify:

- local-only/no-provider/no-download manifest semantics;
- requirements ledger hash binding;
- manifest hash binding;
- first two market rows are already-bound row-1/row-2 TBBO evidence;
- row 59 appears as a missing bounded TBBO requirement;
- all requirements stay in 2023;
- source-faithful evidence claim remains false;
- forged requirements ledger rows are rejected.

## Local Hostile Audit

Local hostile review found no P0/P1/P2 findings after the row-hash normalization patch.

Observed and closed during implementation:

- initial requirement row hashes were computed before CSV stringification, causing validator drift; fixed by hashing the exact string-form payload written to disk;
- forged-row test initially expected row-level hash drift, but the bundle correctly rejects earlier at ledger hash drift; test was adjusted to accept either ledger-level or row-level rejection.

No provider/API, download, new data, protected-window, result interpretation, tuning, adapter/deployment/trading/promotion, Git, or source-faithful evidence surface was introduced.

## Next Gate

The next useful gate is a single bounded DataBento TBBO batch acquisition for the 50 missing ZNH3 market-order windows listed in:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_requirements_discovery/market_order_tbbo_requirements.csv
```

This next gate should remain evidence acquisition only. It should not authorize result interpretation, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

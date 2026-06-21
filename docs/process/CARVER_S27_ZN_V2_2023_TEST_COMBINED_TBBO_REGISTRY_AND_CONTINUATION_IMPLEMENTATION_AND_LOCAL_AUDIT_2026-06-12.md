# S27 V2 ZN 2023 TEST Combined TBBO Registry And Mechanical Continuation

Date: 2026-06-12

Status:

```text
LOCAL_PASS_2023_TEST_COMBINED_TBBO_REGISTRY_AND_MECHANICAL_CONTINUATION_NOT_RESULT
```

## Scope

This record covers the authorized local-only S27_V2 2023 TEST combined market-order TBBO registry and mechanical continuation gate.

No provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, adapter/deployment/trading/promotion, Git action, GPT packet preparation, or source-faithful evidence claim was authorized or performed by this gate.

## Implementation

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` now builds a deterministic combined market-order TBBO registry before 2023 TEST mechanical artifact construction.

Combined registry source composition:

- row 1 prebound TBBO evidence;
- row 2 prebound TBBO evidence;
- 39 original batch-selected at-or-before-fill TBBO rows;
- 10 retry-selected at-or-before-fill TBBO rows;
- row 215 engineering policy evidence.

The row 215 convention remains explicitly labeled:

```text
ROW215_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

The combined registry has 52 rows, covering market-order rows from row 1 through row 343 where market orders occur.

Combined registry SHA256:

```text
BD3BA4E2C0ACC8A13C50D5F24410D852522F8127FFF66980A0D35D1AE72ACDEA
```

## Mechanical Continuation Result

The 2023 TEST mechanical artifact run now continues past the prior row 59 TBBO blocker.

Current artifact state:

- candidate rows: `303`
- supported mechanical rows: `302`
- emitted market-order rows: `33`
- terminal fail-closed row: `303`
- terminal timestamp: `2023-01-20T20:00:00Z`
- terminal reason: `SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT`

Terminal row 303:

- raw symbol: `ZNH3`
- starting position: `5`
- desired position: `7`
- position change: `2`
- order side: `BUY`
- market order required: `TRUE`
- market order rows emitted: `FALSE`
- fill candidate timestamp: `2023-01-20T21:00:00Z`
- same session: `FALSE`
- source-faithful evidence claimed: `FALSE`

Run artifact hashes:

- run manifest SHA256: `3B10772E89823D1759551A711776633EBEAEEEF7D9F61C1F6D279DD7C03B1984`
- evidence manifest SHA256: `DAAD0698BE0931213827CA4DC4BAF93F87D791FCC2DD26C3FA57D700BA6C80BB`
- trusted bundle SHA256: `B810FB1C1DBD17C44DA77C85318302D16B346ECFC878DBE6BA359BBCBFE10120`

The run remains mechanical artifact construction only. It is not result interpretation, not performance evaluation, not tuning evidence, not promotion, and not source-faithful evidence.

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

Additional local hash checks:

- combined TBBO registry SHA manifest: PASS;
- 2023 TEST run SHA256SUMS: PASS;
- package-root export check: PASS.

## Local Hostile Audit

Two read-only local hostile-audit subagents returned `PASS_NO_P0_P1_P2`.

Registry/hash-binding audit:

- verified 52 unique combined registry rows;
- verified persisted registry equals active in-memory re-derivation;
- verified row source composition: 1 + 1 + 39 + 10 + row 215 engineering policy;
- verified no provider/API/download path in `test_mechanical_run.py`;
- verified row 215 is not book-explicit and not source-faithful evidence.

Mechanical continuation audit:

- verified the runner consumes already-local registry evidence only;
- verified rows 1-302 are supported and row 303 fails closed;
- verified row 303 is an unresolved session/EOD market-order blocker;
- verified non-authorizations and package-root boundary remain preserved.

One P3 note from the registry audit requested a dedicated combined-registry regression. A focused regression was added:

```text
test_2023_test_combined_tbbo_registry_rejects_self_consistent_row215_drift
```

## Current Status

```text
LOCAL_PASS_2023_TEST_COMBINED_TBBO_REGISTRY_CONTINUATION_TO_ROW303_SESSION_EOD_BLOCKER_NOT_RESULT
```

The next useful gate is a narrow session/EOD market-order policy planning or implementation gate for row 303. That gate must decide whether a market order whose fill candidate is at the session end and whose valuation mark is in the next session may be emitted, deferred, canceled, or fail-closed under a source-native rule.

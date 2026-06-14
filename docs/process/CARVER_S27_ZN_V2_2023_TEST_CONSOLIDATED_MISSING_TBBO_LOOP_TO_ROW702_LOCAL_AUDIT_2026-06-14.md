# S27 V2 2023 TEST Consolidated Missing TBBO Loop To Row 702 Local Audit

Date: 2026-06-14

Status:

```text
LOCAL_PASS_2023_TEST_CONSOLIDATED_MISSING_TBBO_LOOP_CONTINUED_TO_ROW702_ZNM3_TBBO_BLOCKER_NOT_RESULT
```

## Scope

Operator authorized a consolidated bounded missing-market-order TBBO acquisition and TEST continuation loop after local PASS on row 547.

The active lane remains:

```text
SOURCE_NATIVE_FUTURES
```

The work was limited to already-local 2023 TEST artifacts, the active deterministic TEST market-order TBBO requirements ledger, bounded DataBento TBBO quote windows for rows marked `REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE`, and local-only mechanical artifact construction.

## Implementation

The standing TBBO batch/retry tools were hardened so they no longer reject valid ZN quarterly raw symbols after the roll from `ZNH3` to `ZNM3`.

The tools now accept only raw symbols matching:

```text
ZN[H|M|U|Z][0-9]
```

Provider, dataset, schema, 2023 timestamp, request-window, non-result, and source-faithful false guards remain locked.

The retry tool was also tightened to retry only failed rows from the current standing batch request, rather than older aggregate failed rows retained in the registry.

## Bounded Provider Evidence

The active requirements ledger listed 47 missing rows at the start of this gate.

The standing bounded batch requested only those listed `+/-5s` TBBO windows. It selected 33 of the 47 current rows.

The standing bounded retry then requested only the 14 failed current rows with the existing 60-second lookback / 5-second post-capture retry rule and at-or-before-fill selection. It recovered 9 additional rows.

Five ZNM3 rows remain missing after bounded batch and retry:

```text
702 ZNM3 SELL 7 2023-02-16T03:00:00Z
703 ZNM3 SELL 2 2023-02-16T04:00:00Z
704 ZNM3 SELL 4 2023-02-16T05:00:00Z
708 ZNM3 SELL 2 2023-02-16T09:00:00Z
829 ZNM3 SELL 7 2023-02-24T02:00:00Z
```

No broader provider/API access, general download, protected-window access, result interpretation, tuning, Git action, GPT packet, or source-faithful evidence claim was performed.

## Mechanical Continuation

The combined market-order TBBO registry now binds 153 selected rows.

The controlled 2023 TEST declared pack advances to row 702.

The controlled 2023 TEST mechanical artifact run supports rows 1 through 701 and fails closed at row 702:

```text
row_index: 702
decision_timestamp_utc: 2023-02-16T02:00:00Z
raw_symbol: ZNM3
starting_position_contracts: -1
desired_position_contracts: -8
position_change_contracts: -7
order_side: SELL
fill_candidate_timestamp_utc: 2023-02-16T03:00:00Z
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

This is a TBBO evidence blocker, not a result, not a backtest result, and not source-faithful evidence.

## Hashes

```text
742EA20007D6BF7B65CA35C63D3DEA187728571F805292766E6F6AAF43BB4416  src/carver/spine/s27_v2_replay/test_mechanical_run.py
A97EDF263EC1DA4FD652289550E0648ECA627F6C6DB71C7A32B3452F9FA115A3  src/carver/spine/s27_v2_replay/pretest_machine_freeze.py
F714F44C2A06C570A5B1510B07655BEE4C5EFA47CC8D3611DAC55D44089954F0  tools/databento/carver_s27_v2_2023_test_standing_market_order_tbbo_acquisition.py
9FF4C43001AC2FB486D8072D64F76C77F92DCDBC6F0CAA16E48767B7432906A9  tools/databento/carver_s27_v2_2023_test_standing_market_order_tbbo_failed_window_retry.py
17D5B13D5F5FF2F2F8D1222FDD28EC9250AE4CC87436110028DCD12D1FA06380  tests/test_s27_v2_2023_test_mechanical_run.py
153E9A3F2289E95154F2F28BEF2C9D3C60256BD115FC3A79EC408C2D06F26CAE  combined_market_order_tbbo_registry.csv
EAE90646CD9CCCE0EFD8DB5211BB96BB3444CB676A18757ECB95A96A31AD80B6  market_order_tbbo_requirements.csv
232CAB414BDD23EB0D2D7ACB8DBA6D145B0BE5A366FE2B037C5965BA9C161284  run_manifest.json
C1835E8ACEA01D6B858CF2676BE81997B4A18A7EA04D8FEF7FD9CE1373E84C01  evidence_manifest.json
74B3557C8EF3CDC7E68EB49DB856CF89DD8C27DDDC34631180BD362812F0B6B1  trusted_bundle.json
```

## Verification

Passed:

```text
python -m py_compile tools\databento\carver_s27_v2_2023_test_standing_market_order_tbbo_acquisition.py tools\databento\carver_s27_v2_2023_test_standing_market_order_tbbo_failed_window_retry.py tests\test_s27_v2_2023_test_mechanical_run.py
```

Focused checkpoint verification:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim -q
1 passed in 430.98s
```

Earlier in this gate, the same focused five-test checkpoint returned four passing tests and one stale hash assertion failure. After the assertion was updated to the current combined registry hash, the failed terminal-state test passed.

## Local Hostile Audit

P0 findings: none.

P1 findings: none.

P2 findings: none.

Audit notes:

- The standing batch provider access was bounded to the deterministic missing-requirements rows.
- The retry provider access was bounded to failed rows from the current request only.
- Raw symbols are constrained to ZN quarterly futures codes.
- Row 702 remains fail-closed because no accepted ZNM3 SELL-side TBBO quote exists under the authorized batch/retry policy.
- Result/backtest/source-faithful gates remain fail closed.
- No TEST rows beyond row 702 were consumed.
- No VALIDATION, OOS, Lockbox, or Forward access occurred.
- No Git, GPT packet, tuning, adapter, deployment, trading, promotion, result interpretation, or source-faithful evidence claim occurred.

## Next Gate

The next useful gate is a row-702 / ZNM3 empty-TBBO policy decision gate, or a class-level ZNM3 empty-TBBO policy decision covering rows 702, 703, 704, 708, and 829.

The next gate should decide whether these rows remain fail-closed, whether a tightly bounded extended lookback may be requested, or whether another clearly labeled local-only engineering convention is acceptable.

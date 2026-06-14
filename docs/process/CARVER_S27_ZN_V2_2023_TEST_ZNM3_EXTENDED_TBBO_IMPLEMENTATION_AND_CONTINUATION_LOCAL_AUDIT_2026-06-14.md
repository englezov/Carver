# S27 V2 2023 TEST ZNM3 Extended TBBO Implementation And Continuation Local Audit

Date: 2026-06-14

Status:

```text
LOCAL_PASS_2023_TEST_ZNM3_EXTENDED_TBBO_IMPLEMENTED_AND_CONTINUED_TO_ROW704_TBBO_BLOCKER_NOT_RESULT
```

## Scope

Operator authorized exactly one bounded ZNM3 extended-lookback TBBO evidence acquisition and mechanical continuation gate, limited to rows `702`, `703`, `704`, `708`, and `829`.

The active lane remains:

```text
SOURCE_NATIVE_FUTURES
```

No provider/API access outside those five bounded ZNM3 quote windows was authorized or performed.

## Evidence Acquisition

Tool:

```text
tools/databento/carver_s27_v2_2023_test_znm3_market_spread_tbbo_extended_lookback.py
```

Request shape:

```text
fill_timestamp - 5 minutes through fill_timestamp + 5 seconds
```

Selection rule:

```text
LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP
```

Engineering label:

```text
ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

Result:

```text
FAIL_CLOSED_ZNM3_EXTENDED_LOOKBACK_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT
```

Selected rows:

```text
702 2023-02-16T02:57:32.859964579Z age 147.140036 bid 112.703125 ask 112.71875
703 2023-02-16T03:55:23.986777151Z age 276.013223 bid 112.765625 ask 112.78125
708 2023-02-16T08:58:52.420198009Z age 67.579802 bid 112.765625 ask 112.78125
829 2023-02-24T01:58:55.083678217Z age 64.916322 bid 111.96875 ask 111.984375
```

Failed row:

```text
704 no eligible at-or-before-fill quote in the authorized five-minute lookback window
```

## Mechanical Continuation

The active combined market-order TBBO registry now binds 157 rows.

The controlled 2023 TEST declared pack and mechanical run now support rows `1` through `703` and fail closed at row `704`.

Terminal row:

```text
row_index: 704
decision_timestamp_utc: 2023-02-16T04:00:00Z
raw_symbol: ZNM3
starting_position_contracts: -10
desired_position_contracts: -14
position_change_contracts: -4
order_side: SELL
fill_candidate_timestamp_utc: 2023-02-16T05:00:00Z
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

No rows after row `704` were consumed.

This is mechanical artifact construction only, not result interpretation, not a result-scored run, and not a source-faithful evidence claim.

## Hashes

```text
04FB6B24C1AE1EA07872EFEADBE4BF2A115A30EAA0BF3784316CE74A3E4FB3FF  src/carver/spine/s27_v2_replay/test_mechanical_run.py
258E07300C1E8D877362D5D22CA377F8D7001035BE1F12EE593C060B76201384  tools/databento/carver_s27_v2_2023_test_znm3_market_spread_tbbo_extended_lookback.py
B9C6320F430CBCF2EAC009810EF2A102B961235CD8E62824920D6A1C19EDAD5B  tests/test_s27_v2_2023_test_mechanical_run.py
1250D8490305DA6F680B87B6B8BE62F2F6B5A98C9C7579BAB3FC13B98C89DC46  ZNM3 extended selected registry
7F53E0AEA45C70268FC6977F4851E0E6DCAF7EC590A87BDFF08F7DD0386C2F1F  combined_market_order_tbbo_registry.csv
2EA9BABF1AC40FDFFD6DBDE2CD9BA993B18C53E17E763E53E95012E4705B3518  market_order_tbbo_requirements.csv
D6494E86973164006CD2381577CEC5390F8B528E4D78C28C2174CE34A51EE17F  run_manifest.json
1953CF9F40B89418FBC6CCB36FB5BE9A5437F2A0491DED27F5B25B7D6CBADC73  evidence_manifest.json
1C1D2F4C741E4F2CDF14A05A781CC02D073AFADB4B09DD2D951DE1751C4A7F51  trusted_bundle.json
```

## Verification

Passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_znm3_market_spread_tbbo_extended_lookback.py
python -m py_compile tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim -q
```

The final focused terminal-state test returned:

```text
1 passed in 477.42s
```

Earlier in this gate, the five-test checkpoint returned four passing tests and one stale mechanical-total assertion; after correcting the assertion to current artifact totals, the terminal-state test passed.

## Local Hostile Audit

P0 findings: none.

P1 findings: none.

P2 findings: none.

Audit notes:

- Provider access was bounded to the five authorized ZNM3 windows only.
- Selection is at-or-before-fill only.
- Four selected rows carry the engineering-not-book-explicit ZNM3 extended-lookback label.
- Row `704` remains fail-closed because no eligible quote exists in the authorized five-minute lookback window.
- Result/backtest/source-faithful gates remain fail closed.
- No VALIDATION, OOS, Lockbox, or Forward access occurred.
- No Git, GPT packet, tuning, adapter, deployment, trading, promotion, result interpretation, or source-faithful evidence claim occurred.

## Next Gate

The next useful gate is a row-704 ZNM3 no-quote policy decision gate.

The gate should decide whether row `704` remains fail-closed, whether another strictly bounded source-native evidence request is justified, or whether the 2023 TEST run should stop at row `704` pending a later consolidated audit.

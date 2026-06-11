# S27_V2 Pre-TEST Development/Reconciliation Completion Run Implementation

Date: 2026-06-11

Status:

```text
S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_RUN_EMITTED_NOT_RESULT
```

Authorization:

```text
S27_V2_PRE_TEST_DEVELOPMENT_RECONCILIATION_COMPLETION_GATE
```

## Scope

This record covers the repaired pre-TEST Development/Reconciliation completion
checkpoint built and run from already-local pre-2023 ZN files only.

The scoped patch closed the local hostile-audit findings inside this exact
checkpoint:

- stable same-symbol decision/fill/valuation selection;
- source re-derivation of decision/fill/valuation rows rather than runtime-only;
- clearer fail-closed no-market metadata on unfilled limit rows;
- exact pack/output-root lock for the audited checkpoint;
- manifest checksum and summary binding.

The run remains local mechanical ledger construction only. It is not a TEST,
VALIDATION, OOS, Lockbox, Forward, result-scored run, result interpretation,
PnL evaluation beyond mechanical row construction, promotion, or source-faithful
evidence claim.

## Files

Code:

```text
tools/databento/carver_s27_v2_pretest_completion_dev_recon_pack.py
src/carver/spine/s27_v2_replay/pretest_development_recon_completion_run.py
tests/test_s27_v2_pretest_development_recon_completion.py
```

Declared input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pretest_dev_recon_2022_filled_sell_completion_declared_pack
```

Run artifact root:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pretest_dev_recon_2022_filled_sell_completion_run
```

## Selection

Selected slice rule:

```text
EARLIEST_ALREADY_LOCAL_2022_ORGANIC_FILLED_SELL_REDUCTION_AFTER_STRICT_PRIOR_WARMUPS_PRESERVE_2023_FOR_TEST
```

Repair note:

```text
The original timestamp-only chain could stitch different raw symbols across
decision/fill/valuation.

The repaired checkpoint now requires:
- fill row = same raw symbol, exactly one hour after decision
- valuation mark row = next completed same-symbol row strictly after fill
```

Selected row count:

```text
46
```

Filled sell completion:

```text
row_index = 46
decision_timestamp_utc = 2022-07-05T23:00:00Z
fill_timestamp_utc = 2022-07-06T00:00:00Z
valuation_mark_timestamp_utc = 2022-07-06T02:00:00Z
raw_symbol = ZNU2
starting_position_contracts = 39
desired_position_contracts = 0
position_change_contracts = -39
order_side = SELL
order_quantity = 39
limit_order_price = 117.390625
fill_candidate_close = 119.8125
fill_executed = TRUE
```

## Pack Hash

```text
E2977B8667DA225B431E42A381BA3F06676D0A05B8BDDE0E0C2D7282A5AA172E  S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_MANIFEST.json
```

## Run Summary

Mechanical ledger summary:

```text
row_count = 46
first_filled_sell_row_index = 46
final_position_contracts = 0
cumulative_gross_pnl_amount = -498734.375
cumulative_commission_amount = 179.4
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = -498913.775
```

Boundary row details:

```text
limit_order_price = 117.390625
fill_rule = ONE_HOUR_CLOSE_ONLY_LIMIT_FILL
fill_quantity = 39
position_after_fill = 0
market_fallback_status = NOT_REQUIRED_LIMIT_ORDER_FILLED
valuation_mark_close_price = 119.78125
existing_position_gross_pnl = -344906.25
fill_gross_pnl = -93234.375
row_gross_pnl_amount = -438140.625
row_net_pnl_amount = -438230.325
```

Run hashes:

```text
8d62199a75f7661d7a37cf8270d948229c728b6104da32357df53756cf0870c2  internal bundle hash
FAAD248FBA2DBC1BD6124521A8175F0C6BB7B496D64838209F27262779F34526  run_bundle.json byte SHA256
18061E34FE965F6A43C57190E3D16CE8606E86DAAF9B4B014571F34BA4088F9B  run_manifest.json
DF167D8D303A439B707440052FA2FB628C6FA467DC26195D5FBCD6450BBE30E1  evidence_manifest.json
5967B265180CB9EAABF30C558686122CBD42A63D4C733517BD393E378BFB5499  trusted_bundle.json
```

## Verification

Commands:

```text
python tools\databento\carver_s27_v2_pretest_completion_dev_recon_pack.py
python -m py_compile tools\databento\carver_s27_v2_pretest_completion_dev_recon_pack.py src\carver\spine\s27_v2_replay\pretest_development_recon_completion_run.py
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py -q
python -m pytest tests\test_s27_v2_pre2023_extended_development_recon.py tests\test_s27_v2_pre2023_sell_reduction_development_recon.py tests\test_s27_v2_pretest_development_recon_completion.py -q
```

Results:

```text
pack rebuild PASS
py_compile PASS
25 passed
68 passed
```

## Non-Authorization

This checkpoint does not authorize or perform provider/API access, downloads,
new data acquisition, TEST, VALIDATION, OOS, Lockbox, Forward, result
interpretation, PnL evaluation beyond mechanical row construction, tuning,
adapter work, deployment, trading, promotion, Git actions, or source-faithful
evidence claims.

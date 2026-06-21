# S27 V2 ZN 2023 TEST Row-2 Market-Order Cost Accounting And Continuation Implementation And Local Audit

Date: 2026-06-12

Status:

```text
LOCAL_PASS_ROW2_MARKET_ORDER_COST_ACCOUNTING_AND_CONTINUATION_NOT_RESULT
```

## Authorization

Operator authorized the S27_V2 TEST row-2 market-order cost-accounting and mechanical continuation gate after bounded DataBento TBBO row-2 SELL bid-side evidence PASS.

Scope was limited to the audited 2023 TEST row-2 `SELL 2` market order, using the selected TBBO quote at `2023-01-03T01:59:56.651440427Z` with bid `112.578125`, ask `112.59375`, full spread `0.015625` points, ZN point value `1000 USD`, and row-2 quantity `2`.

## Implementation

Patched:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

The row-2 `SELL 2` market order now binds:

- selected DataBento TBBO quote timestamp: `2023-01-03T01:59:56.651440427Z`;
- selected bid-side executable market-fill price: `112.578125`;
- selected ask: `112.59375`;
- full spread: `0.015625` points;
- full spread value: `15.625 USD` per contract;
- selected row hash: `0785dcfa6525897f07344c9f016cf832217e94cd79e2e6e4c3220b7f70d6d0b7`;
- selected spread ledger SHA256: `AA1240A937EF7A4BE30C1851EE708C26B2A4D7D6E7C30F518EFA85E008079BE8`.

Accepted no-double-counting convention:

```text
BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
```

Because the market fill uses the selected executable bid, the emitted row-2 cost row records:

```text
commission_amount = 4.6
spread_cost_amount = 0.0
total_cost_amount = 4.6
currency = USD
```

## Produced Mechanical Artifacts

Run root:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run
```

The run now supports mechanical rows 1 through 58 and fails closed at row 59.

Run manifest:

```text
candidate_row_count = 59
supported_mechanical_row_count = 58
fail_closed_row_index = 59
fail_closed_reason = FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

Row 2 market order:

```text
decision_timestamp_utc = 2023-01-03T01:00:00Z
raw_symbol = ZNH3
current_position_before_order = 2
target_position_after_fill = 0
order_side = SELL
order_quantity = 2
trigger_source_condition = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
```

Row 2 fill metadata:

```text
fill_timestamp_utc = 2023-01-03T02:00:00Z
fill_price = 112.578125
fill_price_provenance = MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE
position_after_fill = 0
market_spread_cost_status = PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL
```

Row 2 mechanical PnL metadata was emitted as local mechanical construction only, not as result interpretation:

```text
valuation_mark_timestamp_utc = 2023-01-03T03:00:00Z
valuation_mark_close_price = 112.625
existing_position_gross_pnl = 62.5
fill_gross_pnl = -93.75
row_gross_pnl_amount = -31.25
row_net_pnl_amount = -35.85
cumulative_gross_pnl_amount = 31.25
cumulative_commission_amount = 9.2
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = 22.05
ending_position_contracts = 0
```

The row-59 next blocker is:

```text
decision_timestamp_utc = 2023-01-05T14:00:00Z
starting_position_contracts = 0
desired_position_contracts = 10
position_change_contracts = 10
order_side = BUY
market_order_required = TRUE
market_order_rows_emitted = FALSE
secondary_fail_closed_reason = MARKET_ORDER_CONTINUATION_REQUIRES_SEPARATE_BOUNDED_SPREAD_EVIDENCE
```

## Local Hostile Audit

Initial local hostile review found a validation hardening gap: the bundle validation bound row-2 TBBO row hash and ledger hash but did not directly re-check the row-2 market-fill price and cost-row TBBO quote fields against the selected side-specific active TBBO evidence.

Patch applied before local PASS:

- validates market-fill price equals the selected side-specific executable TBBO price;
- validates side-specific order-cost type;
- validates USD currency;
- validates selected TBBO quote timestamp;
- validates selected bid, ask, full-spread points, and spread value;
- adds self-consistent row-2 forgery regressions for fill price, cost type, currency, quote timestamp, bid, ask, spread points, and spread value.

Subagent tooling was not available in this Codex thread during the audit pass, so the hostile audit was performed locally in-process with focused byte/hash checks and regression tests.

## Verification

Commands:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

```text
43 passed
104 passed
```

Additional local hash audit verified:

- every `SHA256SUMS.csv` row matches current run artifact bytes;
- every `evidence_manifest.json` ledger hash matches current ledger bytes;
- `evidence_manifest.json` binds current `run_manifest.json`;
- `trusted_bundle.json` binds current `run_manifest.json` and `evidence_manifest.json`.

Package-root export check remains closed: `src/carver/spine/s27_v2_replay/__init__.py` does not export the TEST mechanical runner.

## Non-Authorizations Preserved

No provider/API access beyond completed row-2 TBBO evidence, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim was introduced.

Current status:

```text
LOCAL_PASS_ROW2_MARKET_ORDER_COST_ACCOUNTING_AND_CONTINUATION_PENDING_EXTERNAL_AUDIT_NOT_RESULT
```

Next useful step is GPT 5.5 Extended Pro external hostile audit of this row-2 market-order cost-accounting and continuation packet before any further TEST continuation.

## External Packet Repair Note

The first GPT 5.5 packet audit of ZIP SHA256 `13FC793BAFBB9EC21BDE961CB90519AE9DB7A94EB568682241AEA619C1A97AC2` returned `FAIL` for packet self-sufficiency, not for row-2 arithmetic or ledger binding.

Findings:

- packet did not include enough imported support modules for byte-local pytest execution;
- packet included row-2 TBBO evidence but omitted row-1 TBBO evidence, while validator checks every emitted market row;
- explicit self-consistent row-2 TBBO row-hash and ledger-SHA forgery regression cases were useful to add.

Remediation:

- added explicit row-2 TBBO row-hash and selected-ledger-SHA self-consistent forgery tests;
- rebuilt the GPT packet with the full `src/carver` tree, row-1 and row-2 TBBO evidence folders, local 2022-2023 ZN source files needed by the fixture, declared TEST pack, run artifacts, and process records;
- verified the repaired packet from extracted bytes with absolute packet-local `PYTHONPATH`.

Repaired packet:

```text
C:\Users\apops\Desktop\GPT\S27_V2_2023_TEST_ROW2_MARKET_ORDER_COST_CONTINUATION_REPAIRED_AUDIT_PACKET_2026-06-12.zip
SHA256 = 85265DB4D37662422F5FE0387B7D450E2370FB95A1242B89517B1732B531D3BE
```

Packet-local verification:

```text
PYTHONPATH=<extracted_packet>\src python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
45 passed
```

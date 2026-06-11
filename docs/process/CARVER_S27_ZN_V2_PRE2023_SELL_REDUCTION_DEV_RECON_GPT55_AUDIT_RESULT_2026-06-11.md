# S27_V2 Pre-2023 Sell-Side/Reduction Development/Reconciliation GPT 5.5 Audit Result

Date: 2026-06-11

Status:

```text
GPT55_EXTENDED_PRO_EXTERNAL_HOSTILE_AUDIT_PASS
```

Scope:

```text
S27_V2 local-only pre-2023 sell-side/reduction Development/Reconciliation checkpoint
```

Audit basis:

```text
Attached GPT packet, including source-lock, sell-reduction pack zip, sell-reduction run artifact zip, code, focused tests, process records, current-state record, and minimal dependencies.
```

Carver.pdf status:

```text
NOT_ATTACHED_IN_GPT_CHAT_DIRECT_BOOK_REDERIVATION_NOT_PERFORMED
```

GPT used:

```text
01_CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
```

as the locked local interpretation. Direct book re-derivation remains reserved for a later book-attached final audit.

## Verdict

GPT returned:

```text
PASS
```

P0 findings:

```text
None
```

P1 findings:

```text
None
```

P2 findings:

```text
None
```

## P3 Notes

GPT recorded:

```text
Carver.pdf was not attached, so this is a packet/local-artifact/code/process audit against the attached source-lock, not a fresh direct book audit.
```

and:

```text
This PASS does not authorize TEST, VALIDATION, OOS, Lockbox, Forward, provider/API, download/new-data, Git, tuning, adapter/deployment/trading/promotion, result interpretation, PnL evaluation beyond mechanical row construction, or source-faithful evidence claims.
```

## Confirmed

GPT audited the attached packet only and did not use internet search, GitHub, provider/API paths, downloads, or new data.

GPT recomputed the attached ZIP artifacts locally and confirmed:

- forty-four pre-2023 `ZNH2` decision/fill/valuation triples;
- all triples completed-bar ordered as `decision < fill < valuation`;
- 2023 preserved for TEST;
- no TEST, VALIDATION, OOS, Lockbox, or Forward selected data;
- input manifest byte SHA256 `611DF2F8A6AB08A2B2B62E39FDFC3FA883F0196A2A0FA9CE0572FAA1131045F6`;
- all row-family byte hashes match the manifest and SHA file;
- run bundle canonical hash, run/evidence/trusted hashes, and SHA256 ledger binding all match.

Confirmed run hashes:

```text
8cd3fcb3626522c27287e659ddd81c8a6ab4217ce6eb502ce07089f94bb617e8  internal bundle hash
2D01A1A3540CECAF34CE33CB4C915D012E3D1139A2354117735E9DE5223B62B6  run_bundle.json byte SHA256
FDA1EA56ACFA253C6804B15F8F018668904A1040B1CFD4879334BE9819F1708C  run_manifest.json
ED497B806447E3C6741E881C3ED5DE430B4147BA4D60D80491F83503DC8DE3C2  evidence_manifest.json
A7B29AA3652683B3FD38BAC1C1BA869938873D2C292145D91F246973B13EB978  trusted_bundle.json
7ABC28DE55B87B11A18229F9E59E6EC37CB030E1461AE3FDB2289DD7A90455AD  SHA256SUMS.csv
```

## Sell-Side Boundary

GPT confirmed row `44` is the first carried-position reduction intent:

```text
starting_position_contracts = 34
desired_position_contracts = 33
position_change_contracts = -1
order_side = SELL
order_quantity = 1
adjacent_target_position = 33
formula_limit_price = 130.03172667686832
limit_order_price = 130.046875
fill_candidate_close = 128.0625
fill_executed = FALSE
ending_position_contracts = 34
working_state_after = UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE
```

GPT confirmed the packet does not falsely claim a filled sell reduction. It proves sell-side order-intent generation and conservative no-fill/fail-closed lifecycle handling.

## Mechanical Totals

GPT confirmed:

```text
row_count = 44
final_position_contracts = 34
cumulative_gross_pnl_amount = -74515.625
cumulative_commission_amount = 78.2
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = -74593.825
```

## Boundary

This PASS does not authorize:

- provider/API access;
- downloads;
- new data;
- TEST;
- VALIDATION;
- OOS;
- Lockbox;
- Forward;
- result interpretation;
- PnL evaluation beyond mechanical row construction;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git actions;
- source-faithful evidence claim.

## Next

GPT stated the next gate may proceed only with separate operator authorization.

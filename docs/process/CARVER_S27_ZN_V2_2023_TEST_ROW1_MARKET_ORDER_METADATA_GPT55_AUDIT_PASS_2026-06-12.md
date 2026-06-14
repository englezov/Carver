# CARVER S27 ZN V2 2023 TEST Row-1 Market-Order Metadata GPT 5.5 Audit PASS

Date: 2026-06-12

Status: GPT55_EXTERNAL_AUDIT_PASS_NOT_RESULT_NOT_SOURCE_FAITHFUL_EVIDENCE

## Audit Packet

Audited packet:

`S27_V2_2023_TEST_ROW1_MARKET_ORDER_METADATA_FAIL_CLOSED_PACKET_2026-06-12.zip`

Observed ZIP SHA256:

`FEA4FA460DCB9FE1EFE79FF2213767DD10E59E305C5449A08BC9C5B58F919671`

GPT noted that `Carver.pdf` was not used as authority for this narrow packet gate; the packet was audited as byte-visible machinery/artifact evidence.

## Verdict

GPT 5.5 Extended Pro verdict: PASS.

Findings:

- P0: none
- P1: none
- P2: none

## Closed Scope

GPT confirmed:

- row-1 target-position gap is classified before adjacent-limit logic;
- declared blocker is current position `0`, desired position `2`, change `2`, side `BUY`, adjacent target `1`;
- `market_order_ledger.csv` contains exactly one `BUY 2` market-order metadata row;
- trigger source condition is `BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT`;
- `market_fill_metadata_ledger.csv` binds the exact next completed hourly fill row at `2023-01-03T01:00:00Z`, `ZNH3`, close/fill price `112.5625`;
- fill provenance is `MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE`;
- same-session, no-roll, and initial-empty-working-state proofs are bound;
- accepted commission is bound from `cost_parameter.csv` as `2.30 USD` per contract per side, quantity `2`, commission amount `4.6`;
- numeric market spread cost remains unresolved and fail-closed;
- actual cost, PnL, validation/result, backtest result, and source-faithful evidence rows are not emitted;
- package-root exports do not expose runnable TEST/backtest machinery;
- forbidden provider/API/download/new-data/VALIDATION/OOS/Lockbox/Forward/tuning/Git/adapter/deployment/trading/promotion/result-interpretation/source-faithful surfaces were not introduced.

## P3 Note

GPT recorded a non-blocking packet reproducibility note: the ZIP was sufficient for byte-level hostile audit, but not self-contained for packet-only pytest reproduction because the included tests import repository modules outside the ZIP. GPT therefore audited the ZIP bytes, emitted ledgers, manifests, and included source directly rather than relying on claimed pytest output.

## Next Gate

GPT stated that the next gate may proceed, limited to a separately authorized local-only gate.

This PASS does not authorize PnL/result/backtest emission, result interpretation, source-faithful evidence claims, provider/API/download/new-data access, VALIDATION/OOS/Lockbox/Forward access, tuning, adapter/deployment/trading/promotion work, or Git actions.

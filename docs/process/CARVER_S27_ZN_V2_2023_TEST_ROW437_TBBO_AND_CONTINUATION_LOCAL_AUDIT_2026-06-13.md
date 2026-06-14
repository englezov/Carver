# S27 V2 ZN 2023 TEST Row 437 TBBO And Continuation Local Audit

Date: 2026-06-13

Status:

```text
LOCAL_PASS_2023_TEST_ROW437_MARKET_ORDER_TBBO_AND_CONTINUATION_TO_ROW438_MARKET_TBBO_BLOCKER_NOT_RESULT
```

## Scope

Operator authorized a bounded row-437 market-order TBBO evidence and mechanical continuation gate after local PASS on row 436. Scope was limited to already-local 2023 TEST artifacts and bounded DataBento TBBO evidence for the row-437 ZNH3 market-order blocker only.

Forbidden surfaces remained closed: no broader provider/API access, no downloads, no new data acquisition, no VALIDATION, no OOS, no Lockbox, no Forward, no result interpretation, no PnL evaluation beyond mechanical construction, no tuning, no adapter/deployment/trading/promotion, no Git actions, no GPT packet preparation, and no source-faithful evidence claim.

## Row 437 TBBO Evidence

Evidence record:

```text
docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW437_MARKET_ORDER_TBBO_EVIDENCE_2026-06-13.md
```

Bounded provider request:

- Row index: `437`
- Raw symbol: `ZNH3`
- Order side: `SELL`
- Order quantity: `4`
- Decision timestamp: `2023-01-31T00:00:00Z`
- Fill-candidate timestamp: `2023-01-31T01:00:00Z`
- Request window: `2023-01-31T00:59:55Z` through `2023-01-31T01:00:05Z`
- Provider/dataset/schema: `DATABENTO_HISTORICAL` / `GLBX.MDP3` / `tbbo`

Selected quote:

- Selected quote timestamp: `2023-01-31T00:59:58.560246105Z`
- Quote age seconds: `1.439754`
- Bid: `114.390625`
- Ask: `114.40625`
- Executable SELL market fill price: `114.390625`
- Spread points: `0.015625`
- Point value: `1000`
- Spread value per contract: `15.625 USD`
- Accounting convention: `BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST`
- Separate spread cost emitted: `0.0 USD`

Key evidence hashes:

- Row-437 selected spread registry: `8BE6C82C09A69A64D260C9A572F97330B36A61047B8E4494F0154B60989B93C5`
- Row-437 raw DBN: `82972DEE54B585BAF3242D0CF0E2C1FF52991D0D9FDA775EAE82633A2AE663A4`
- Row-437 raw CSV: `0C19D1F0DA6DEA006665DC45F6326D87D4D7B641278637386B118592D26EC80B`
- Row-437 provider-condition ledger: `8B8264D38D8F6732E34D669E044E9B09B064C5347719A1161C153D1FDD1B2163`
- Row-437 status JSON: `B7BB6E85740536AF78164A16728183DA07F6BECC6BE23050002A742531EF3803`

## Implementation

Added row-specific bounded acquisition script:

```text
tools/databento/carver_s27_v2_2023_test_row437_market_spread_tbbo_acquisition.py
```

Patched:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

Changes:

- Added row-437 selected registry path and evidence type to the combined TBBO registry.
- Combined market-order TBBO registry now has `86` rows and includes row `437`; row `438` remains absent.
- Hardened generic market-execution accepting validation so self-consistent forged row/hash mutations are rejected across no-market, transition, fill, cost, and PnL artifacts.
- Added row-437 regression coverage for market-order, market-fill, transition, fill, cost, PnL, and TBBO-registry drift.
- Remediated local-audit P2: already-bound TBBO requirements rows now carry real bound selected-row and selected-ledger hashes rather than `MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE` placeholders. Missing rows still carry the missing placeholders.

Provenance repair:

- Requirements ledger: `ED3B80586A33B6ECB4E31813A699DFB1D33C7CDBCE82F61F726D1BA1A192FE1A`
- Requirements manifest: `DF79115EC985992B7E2ABB195D335561EA9A6A0AD5528D54748CC9AB4F3B6BFB`
- Combined TBBO registry: `87A80EF3F229960EF66472134BD22BC23349C9EE4963DC6E50BA21CE1D391E99`
- Combined TBBO registry manifest: `172B53BDE4ED47C954B13D9FF3661CBAFC2E8DB59A8CA5027727863A219AD058`
- Combined TBBO SHA256 ledger: `DFB7BAD7B12A276AC8B0A0FF1A29A6759B487F87157195E4C6007F844E9B4896`

## Mechanical Run State

The regenerated controlled 2023 TEST mechanical artifact run supports rows `1` through `437` and fails closed at row `438`.

Row 437 emitted local-only market/fill/cost/mechanical-PnL metadata:

- Starting position: `23`
- Desired position: `19`
- Position change: `SELL 4`
- Fill candidate: `2023-01-31T01:00:00Z`
- Fill price: `114.390625`
- Commission: `9.2 USD`
- Spread cost: `0.0 USD`
- Valuation mark: `2023-01-31T02:00:00Z`
- Valuation mark close: `114.359375`
- Row gross mechanical PnL: `484.375`
- Row net mechanical PnL: `475.175`
- Ending position: `19`

Mechanical construction totals are recorded only as artifact fields. They are not result interpretation, performance evaluation, source-faithful evidence, promotion, or trading evidence.

Run hashes:

- Run manifest: `F83E598B907A2C7A444973F37B11E6BA911B348D0884081C06FA417DF1AE29B8`
- Evidence manifest: `5739457763C0C044F5E35210157FFEADAE7490028F3691AF2CA1ACB28B1A7507`
- Trusted bundle: `BCE3E2EA53CB8133B1563101A02A23169E97CC290FD366BC50B3E7538952FEAD`
- Run bundle file: `BAC5C9F264FC309A7C5F079DFAAAC69BF091758B438E289043552B8B3BB88A39`
- Run SHA256SUMS: `1D89A23C3F6F09AE43C95D918F08D67A3FBADD149EB289D1BDFBB210AC549CB3`

Next blocker:

- Row index: `438`
- Decision timestamp: `2023-01-31T01:00:00Z`
- Fill-candidate timestamp: `2023-01-31T02:00:00Z`
- Raw symbol: `ZNH3`
- Starting position: `19`
- Desired position: `16`
- Position change: `SELL 3`
- Fail-closed reason: `FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT`

## Verification

Passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_rejects_bound_row_without_bound_hashes tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_self_consistent_row437_drift -q
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

- Focused provenance tests: `3 passed`
- Focused TEST suite: `121 passed`
- Paired pretest/TEST suite: `182 passed`

## Local Hostile Audit

One read-only local hostile-audit subagent initially found one P2: already-bound TBBO requirement rows still carried the missing selected-ledger placeholder. This weakened the requirements-discovery artifact provenance, although the mechanical run itself already bound the combined registry.

After remediation, the same local hostile-audit subagent re-audited and returned:

```text
P0: none
P1: none
P2: none
P3: none
```

The re-audit confirmed:

- Bound requirement rows: `86`
- Missing requirement rows: `24`
- Bad bound placeholders: `0`
- Bad missing rows: `0`
- Row 437 bound selected registry SHA matches the actual row-437 selected spread registry file hash.
- Row 438 remains the first missing TBBO blocker.
- Run manifest still reports `supported_mechanical_row_count = 437` and `fail_closed_row_index = 438`.

## Current Status

```text
LOCAL_PASS_2023_TEST_ROW437_MARKET_ORDER_TBBO_AND_CONTINUATION_TO_ROW438_MARKET_TBBO_BLOCKER_NOT_RESULT
```

The next useful gate is row-438 bounded market-order TBBO evidence and mechanical continuation under the standing bounded TBBO policy or an equivalent fresh authorization.

External GPT/Opus audits remain deferred until a consolidated checkpoint unless separately authorized.

This record does not authorize broader provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.

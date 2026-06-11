# S27_V2 Positive-Action Actual-PnL Closure Implementation

Date: 2026-06-11

Status:

```text
LOCAL_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_METADATA_IMPLEMENTED_NOT_RESULT_NOT_BACKTEST_NOT_SOURCE_FAITHFUL_EVIDENCE
```

## Authorization

Operator authorized the `S27_V2 positive-action actual-PnL validation/provenance/trusted-bundle closure implementation gate` after local PASS on the positive-action actual PnL ledger surface.

Scope was limited to deterministic non-result closure metadata for the locally passed positive-action chain through actual PnL.

## Non-Authorization

This implementation authorizes no provider/API access, no market-data downloads, no new data acquisition, no OOS, no Lockbox, no Forward, no backtests, no result-scored runs, no result emission, no result interpretation, no PnL evaluation beyond mechanical row construction, no tuning, no adapter work, no deployment, no trading, no promotion, no Git actions, and no source-faithful evidence claim.

## Files

Implemented:

```text
src/carver/spine/s27_v2_replay/positive_action_actual_pnl_closure.py
```

Focused tests:

```text
tests/test_s27_v2_positive_action_actual_pnl_closure.py
```

File SHA256:

```text
positive_action_actual_pnl_closure.py = E878C81817D9C23E74014EF38AD984ACBE862ADF51C19EFC504BC3EC64239BEE
test_s27_v2_positive_action_actual_pnl_closure.py = 834658ED9F761C35AD190E77F7FE8E0C99B4A675EAA0CC0BF0FEF53BB468984E
```

## Closure Build

Build output:

```text
ACTUAL_PNL_CLOSURE_BUILD_PASS
bundle_hash 5eb846c4fd83879c6648e9d4132d60f4fdc59ed8626453c9121496e307cacd9e
actual_pnl_bundle_hash e0a5e01d1a944822c0af107f3b65e1c7ec90e2c7a8e0b40dff722cef3472a80e
actual_pnl_row_hash 709c2dac4a586dd7d41843bddba6fbb71685d09162cf471089bd0377a8ab8c90
validation_row_hash e3a02f0226ad8861b0c547e5eba03debfec1bca0c01921cafb665e82bff62909
provenance_row_hash 55e0e1840586b82903d30fd8f0d341a76f2e7cf8d9380b0f872af56a48145be4
evidence_row_hash 5b9142a1cd8a4e47a4d7d6889c0bdc02ba523479e5c62a763575fd0c96873ef8
actual_pnl_ledger_status MECHANICAL_LOCAL_DEV_RECON_PNL_LEDGER_EMITTED_NOT_RESULT
result_evidence_status FAIL_CLOSED_NOT_EMITTED_NOT_AUTHORIZED
backtest_evidence_status FAIL_CLOSED_NOT_EMITTED_NOT_AUTHORIZED
pnl_evaluation_status FAIL_CLOSED_NOT_EMITTED_NOT_AUTHORIZED
source_faithful_evidence_claimed False
```

## Active Binding

The closure bundle rebuilds and validates the active actual-PnL bundle before accepting closure metadata.

The provenance row binds the hash chain through:

- positive-action bundle and row;
- forecast component;
- desired-position component;
- order-plan bundle, limit-order row, and transition row;
- fill bundle, fill-decision row, and limit-fill row;
- actual-cost bundle and actual-cost row;
- actual-PnL bundle and actual-PnL row;
- declared valuation mark manifest, CSV, and local-audit hashes;
- actual-PnL local-audit record hash.

The evidence row records actual PnL only as:

```text
MECHANICAL_LOCAL_DEV_RECON_PNL_LEDGER_EMITTED_NOT_RESULT
```

Result evidence, backtest evidence, PnL evaluation, and source-faithful evidence remain:

```text
FAIL_CLOSED_NOT_EMITTED_NOT_AUTHORIZED
```

## Tests

Focused closure tests:

```text
python -m pytest tests\test_s27_v2_positive_action_actual_pnl_closure.py -q --tb=short
55 passed in 28.87s
```

Adjacent regression tests:

```text
python -m pytest tests\test_s27_v2_positive_action_actual_pnl_executable.py tests\test_s27_v2_positive_action_closure.py -q --tb=short
107 passed in 311.74s (0:05:11)
```

## Boundary

The module is not exported from package root. Standalone closure rows raise `CarverBlocked`; only the bundle path accepts, and only after rebuilding active actual-PnL evidence and closure metadata.

This closure is not a result row, not a backtest, not result interpretation, not PnL evaluation beyond mechanical row construction, not promotion, and not a source-faithful evidence claim.

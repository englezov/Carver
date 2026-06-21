# CARVER S27_V2 Pre-2023 Multi-Row Development/Reconciliation Run Implementation

Date: 2026-06-11

Status: `LOCAL_PRE2023_MULTI_ROW_DEV_RECON_RUN_IMPLEMENTED_NOT_RESULT`

## Scope

This record covers the local-only S27_V2 pre-2023 multi-row Development/Reconciliation pack and executable runner implementation authorized after GPT 5.5 external PASS on the one-row controlled 2022 run through actual PnL completion.

The implementation is limited to already-local pre-2023 ZN source/provider/process files. It does not access provider/API, downloads, 2023 TEST, VALIDATION, OOS, Lockbox, Forward, Git, adapter, deployment, trading, promotion, tuning, or source-faithful evidence surfaces.

## Declared Input Pack

Pack path:

`docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_multi_row_dev_recon_2022_minimum_declared_pack`

Pack manifest:

`S27_V2_PRE2023_MULTI_ROW_DECLARED_INPUT_PACK_MANIFEST.json`

Manifest SHA256:

`362A9C7F9E06737169703383C868C11682A41C3310FAFC917097ADA46806268F`

Selected rule:

`MINIMUM_OLDEST_2022_MULTI_ROW_DEV_RECON_AFTER_WARMUPS_PRESERVE_2023_FOR_TEST`

The pack contains the minimum oldest two-row 2022 Development/Reconciliation slice built from already-local ZNH2 source/provider files after the existing warmup/evidence gates.

Selected rows:

| Row | Decision completed bar | Fill completed bar | Valuation mark completed bar | Raw symbol |
| --- | --- | --- | --- | --- |
| 1 | `2022-01-03T01:00:00Z` | `2022-01-03T02:00:00Z` | `2022-01-03T03:00:00Z` | `ZNH2` |
| 2 | `2022-01-03T03:00:00Z` | `2022-01-03T04:00:00Z` | `2022-01-03T05:00:00Z` | `ZNH2` |

The valuation mark convention remains labeled:

`SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT`

Explicit exclusions:

- `NO_2023_TEST_DATA`
- `NO_VALIDATION`
- `NO_OOS`
- `NO_LOCKBOX`
- `NO_FORWARD`

## Implementation Files

Pack builder:

`tools/databento/carver_s27_v2_pre2023_multi_row_pack.py`

Executable runner:

`src/carver/spine/s27_v2_replay/pre2023_multi_row_development_recon_run.py`

Focused tests:

`tests/test_s27_v2_pre2023_multi_row_development_recon.py`

The executable runner is locked to the declared pack path and locked output path. It is not exported from the package root.

## Run Artifacts

Run output path:

`docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_multi_row_dev_recon_2022_minimum_run`

Run status:

`S27_V2_PRE2023_MULTI_ROW_DEVELOPMENT_RECON_RUN_EMITTED_NOT_RESULT`

Bundle hash:

`aebcaaa60381d0e271822fd038e3bbf7e19b9bf839b2503b089a7c162015d9a9`

Run manifest hash:

`df80a2ee5b4215ba67d370e02cc893c71857525794fbfa9094fc7a6f707b4b07`

Evidence manifest hash:

`a467223fbe6306c3f9629ec3c7293feb301967700b370deadcd67cdbecf0d8c2`

Trusted bundle hash:

`ca8bdfb2154a2c5519f6d527fd1ca9dad68afeabab3e215e7c8518ec39f7f9dd`

## Mechanical Ledger Summary

This is mechanical local ledger construction only. It is not a result-scored run, not result interpretation, not promotion, and not a source-faithful evidence claim.

Final row count: `2`

Final position: `12` contracts

Cumulative gross PnL: `-1500.0` USD

Cumulative commission: `27.6` USD

Cumulative spread cost: `0.0` USD

Cumulative net PnL: `-1527.6` USD

Row mechanics:

| Row | Start position | Desired position | Change | Fill quantity | End position | Row gross PnL | Row commission | Row net PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 8 | 8 | 8 | 8 | -1000.0 | 18.4 | -1018.4 |
| 2 | 8 | 12 | 4 | 4 | 12 | -500.0 | 9.2 | -509.2 |

## Verification

Commands run:

```powershell
python -m py_compile tools\databento\carver_s27_v2_pre2023_multi_row_pack.py src\carver\spine\s27_v2_replay\pre2023_multi_row_development_recon_run.py
python -m pytest tests\test_s27_v2_pre2023_multi_row_development_recon.py tests\test_s27_v2_pre2023_actual_pnl.py tests\test_s27_v2_development_recon_run.py -q
```

Result:

`78 passed`

## Non-Authorization Boundary

This implementation preserves:

- `NO_PROVIDER_API`
- `NO_DOWNLOADS`
- `NO_NEW_DATA_ACQUISITION`
- `NO_TEST_ACCESS`
- `NO_VALIDATION_ACCESS`
- `NO_OOS`
- `NO_LOCKBOX`
- `NO_FORWARD`
- `NO_RESULT_SCORED_RUN`
- `NO_RESULT_INTERPRETATION`
- `NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION`
- `NO_TUNING`
- `NO_ADAPTER_WORK`
- `NO_DEPLOYMENT`
- `NO_TRADING`
- `NO_PROMOTION`
- `NO_GIT_ACTIONS`
- `NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM`

Next required gate:

Local hostile audit result recording for this exact multi-row Development/Reconciliation pack and executable runner. External GPT/Opus hostile audit remains separate operator-mediated work.

# CARVER S27_V2 Pre-2023 Broader Development/Reconciliation Run Implementation

Date: 2026-06-11

Status:

```text
LOCAL_PRE2023_BROADER_DEV_RECON_RUN_IMPLEMENTED_NOT_RESULT
```

Authorization:

```text
S27_V2_CONSOLIDATED_LOCAL_ONLY_PRE2023_BROADER_DEVELOPMENT_RECON_IMPLEMENTATION_AND_RUN_GATE
```

This record covers the controlled local-only S27_V2 pre-2023 broader Development/Reconciliation implementation and run gate after GPT 5.5 GitHub-head PASS on commit `d02626adcc938135f67d5b872d0b23962fed3685`.

This is mechanical Development/Reconciliation ledger construction only. It is not a result-scored run, not result interpretation, not PnL evaluation beyond mechanical row construction, not promotion, and not a source-faithful evidence claim.

## Scope Boundary

Allowed scope:

```text
already-local pre-2023 ZN files
minimum oldest suitable 2022 Development/Reconciliation slice
pre-2022 strict-prior warmup/evidence only
local-only declared input pack construction
local-only deterministic ledger construction
focused verification tests
local hostile audit
GPT external audit packet preparation after local PASS
```

Non-authorized scope:

```text
NO_PROVIDER_API
NO_DOWNLOADS
NO_NEW_DATA_ACQUISITION
NO_TEST_ACCESS
NO_VALIDATION_ACCESS
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_RESULT_INTERPRETATION
NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION
NO_TUNING
NO_ADAPTER_WORK
NO_DEPLOYMENT
NO_TRADING
NO_PROMOTION
NO_GIT_ACTIONS
NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM
```

## Declared Input Pack

Pack path:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_broader_dev_recon_2022_first_session_declared_pack
```

Manifest:

```text
S27_V2_PRE2023_BROADER_DEV_RECON_DECLARED_INPUT_PACK_MANIFEST.json
```

Manifest SHA256:

```text
0937B1F499A67C488B0F02B7CD998D21D1DD74797BB02001D0E8AFBB581CEC86
```

Selected rule:

```text
MINIMUM_OLDEST_2022_BROADER_DEV_RECON_FIRST_SESSION_SEGMENT_AFTER_WARMUPS_PRESERVE_2023_FOR_TEST
```

Selected rows:

| Row | Decision completed bar | Fill completed bar | Valuation mark completed bar | Raw symbol |
| --- | --- | --- | --- | --- |
| 1 | `2022-01-03T01:00:00Z` | `2022-01-03T02:00:00Z` | `2022-01-03T03:00:00Z` | `ZNH2` |
| 2 | `2022-01-03T03:00:00Z` | `2022-01-03T04:00:00Z` | `2022-01-03T05:00:00Z` | `ZNH2` |
| 3 | `2022-01-03T05:00:00Z` | `2022-01-03T06:00:00Z` | `2022-01-03T07:00:00Z` | `ZNH2` |
| 4 | `2022-01-03T07:00:00Z` | `2022-01-03T08:00:00Z` | `2022-01-03T09:00:00Z` | `ZNH2` |

The selected segment is the shortest broader first-session segment available from already-local pre-2023 ZNH2 hourly rows while preserving a two-hour decision/fill/mark cadence. The next candidate decision at `2022-01-03T09:00:00Z` is not included because the strict next-completed-hour valuation row at `2022-01-03T11:00:00Z` is not present in the already-local hourly ledger.

The valuation convention remains:

```text
SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
```

## Implementation Files

```text
tools/databento/carver_s27_v2_pre2023_broader_dev_recon_pack.py
src/carver/spine/s27_v2_replay/pre2023_broader_development_recon_run.py
tests/test_s27_v2_pre2023_broader_development_recon.py
```

The two-row checkpoint files remain present and are not mutated as the authority for this broader checkpoint.

The broader executable function is not exported from `src/carver/spine/s27_v2_replay/__init__.py`.

## Run Artifacts

Output path:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_broader_dev_recon_2022_first_session_run
```

Run status:

```text
S27_V2_PRE2023_BROADER_DEVELOPMENT_RECON_RUN_EMITTED_NOT_RESULT
```

Internal bundle hash:

```text
fa7004cdd66cd4c910280dc3547f8b40eb8468f033f49e5f325787e0b50ea495
```

Run bundle JSON byte SHA256:

```text
62160C20AAF42C8A67D8C8702C27911F97DC71D5E759DB330F9654F0CE3784AB
```

Run manifest SHA256:

```text
C458AF089BC9C177C5ADE695B75BF83A9414F815C84D1ABF1FE182EDBB6D0954
```

Evidence manifest SHA256:

```text
FD6D1CC54CB5B26C0740AF0160A8221A46EF9623854E5793DDC5058DFF10944F
```

Trusted bundle SHA256:

```text
5E4B7C3AE5B4BBEBF408DF6D0FAC3D15CBA41EEEC4B31DBFD941F154C85E9766
```

## Mechanical Ledger Summary

Final row count:

```text
4
```

Position state:

```text
0 -> 8 -> 12 -> 14 -> 15
```

Cumulative gross PnL:

```text
-3359.375 USD
```

Cumulative commission:

```text
34.5 USD
```

Cumulative spread cost:

```text
0.0 USD
```

Cumulative net PnL:

```text
-3393.875 USD
```

Row mechanics:

| Row | Start position | Desired position | Change | Fill quantity | End position | Row gross PnL | Row commission | Row net PnL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 8 | 8 | 8 | 8 | -1000.0 | 18.4 | -1018.4 |
| 2 | 8 | 12 | 4 | 4 | 12 | -500.0 | 9.2 | -509.2 |
| 3 | 12 | 14 | 2 | 2 | 14 | -218.75 | 4.6 | -223.35 |
| 4 | 14 | 15 | 1 | 1 | 15 | -1640.625 | 2.3 | -1642.925 |

The broader run also emits `no_market_order_ledger.csv` with one metadata row per decision row:

```text
market_order_required = FALSE
market_order_rows_emitted = FALSE
market_fallback_status = NOT_REQUIRED_LIMIT_ORDER_FILLED_OR_NO_MARKET_CASE_TRIGGERED
```

## Verification

Commands run:

```powershell
python tools\databento\carver_s27_v2_pre2023_broader_dev_recon_pack.py
python -m py_compile tools\databento\carver_s27_v2_pre2023_broader_dev_recon_pack.py src\carver\spine\s27_v2_replay\pre2023_broader_development_recon_run.py
python -m pytest tests\test_s27_v2_pre2023_broader_development_recon.py tests\test_s27_v2_pre2023_multi_row_development_recon.py -q
```

Result:

```text
26 passed
```

## Next Gate

The next gate is local hostile audit of this broader Development/Reconciliation checkpoint. If local audit passes, prepare a GPT 5.5 external hostile-audit packet for the broader run.

No TEST, VALIDATION, OOS, Lockbox, Forward, provider/API, downloads, new data, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter/deployment/trading/promotion, Git actions, or source-faithful evidence claims are authorized by this record.

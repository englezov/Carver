# S09 MES Machinery Development Minimum Slice Download Provenance

Date: 2026-06-03

Status:

```text
PASS_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_QUARANTINE_ONLY_NOT_BACKTEST
```

Authorized scope:

- gate: S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_GATE
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: ohlcv-1d
- window: 2019-05-05 through 2020-04-05
- window_role: minimum oldest machinery-development slice, not scored evidence
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0

Authorization interpretation:

The operator authorized the oldest minimum S09/MES machinery-development window
download. The slice starts at the first actual MES daily bar observed from
Databento and is shorter than two years. It is not a default Dev window and is
not TEST, VALIDATION, Lockbox, or Forward.

Written data artifacts:

- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/sanitized_daily_bars/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/validation/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_row_validation.csv`

Boundary:

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST,
VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were authorized or performed.

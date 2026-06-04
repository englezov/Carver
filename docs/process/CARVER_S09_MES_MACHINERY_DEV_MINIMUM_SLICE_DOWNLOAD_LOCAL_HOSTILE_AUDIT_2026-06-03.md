# S09 MES Machinery Development Minimum Slice Download Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_NO_BACKTEST
```

Hostile audit scope:

- gate: S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_GATE
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- root: MES
- window: 2019-05-05 through 2020-04-05
- not_default_two_year_window: YES
- oldest_authorized_source_native_data_first: YES

Observed artifacts:

- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/status/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_status.json`
- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/sanitized_daily_bars/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/validation/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_row_validation.csv`
- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/provenance/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_provenance.md`

Hostile checks:

- no CFD adapter path
- no old QuantLab active-pipeline path
- no 2022-2023 default Dev window
- no forecast computation
- no diagnostics
- no backtests
- no TEST, VALIDATION, OOS, Lockbox, or Forward
- no deployment, trading, or promotion
- no Git staging, commit, push, PR, or remote operation

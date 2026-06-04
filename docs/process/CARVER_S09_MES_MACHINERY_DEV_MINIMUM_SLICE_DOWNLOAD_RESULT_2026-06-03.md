# S09 MES Machinery Development Minimum Slice Download Result

Date: 2026-06-03

Status:

```text
PASS_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_QUARANTINE_ONLY_NOT_BACKTEST
```

Downloaded bounded source-native slice:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- window: 2019-05-05 through 2020-04-05
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0
- sanitized_rows: 639
- unique_completed_dates: 289
- first_completed_date: 2019-05-05
- last_completed_date: 2020-04-05
- provider_condition_counts: {"DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY": 4, "NORMAL_PROVIDER_CONDITION": 635}

Role:

This is the oldest minimum machinery-development slice. It is quarantine-only
and not scored evidence. It does not make the strategy input-ready.

Written artifacts:

- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/status/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_status.json`
- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/sanitized_daily_bars/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/validation/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_row_validation.csv`
- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/provenance/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_provenance.md`

Boundary:

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST,
VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were performed.

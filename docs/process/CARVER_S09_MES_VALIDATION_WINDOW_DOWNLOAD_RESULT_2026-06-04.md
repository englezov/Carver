# S09 MES VALIDATION Window DataBento Download Result

Date: 2026-06-04

Status:

```text
PASS_S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_QUARANTINE_ONLY_NOT_BACKTEST
```

Downloaded bounded source-native window:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- window: 2022-02-09 through 2023-12-13
- raw_symbols: MESH2, MESM2, MESU2, MESZ2, MESH3, MESM3, MESU3, MESZ3, MESH4
- sanitized_rows: 1940
- unique_raw_union_completed_dates: 574
- first_completed_date: 2022-02-09
- last_completed_date: 2023-12-13
- provider_condition_counts: {"NORMAL_PROVIDER_CONDITION": 1940}
- provider_errors: 0
- failed_validation_checks: 0

Role:

This is a VALIDATION-window source-native data acquisition artifact only. It is
not a VALIDATION backtest, not a diagnostic, not Lockbox, and not promotion.

Artifacts:

- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/status/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_status.json`
- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/status/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_download_receipt.json`
- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/sanitized_daily_bars/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/validation/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_row_validation.csv`
- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/provenance/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_provenance.md`

Boundary:

No forecast computation, returns, PnL, positions, carry, costs, diagnostics,
backtests, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote publication was performed.

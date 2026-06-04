# S09 MES VALIDATION Window DataBento Download Local Hostile Audit

Date: 2026-06-04

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_NO_BACKTEST
```

Observed:

- status: PASS_S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_QUARANTINE_ONLY_NOT_BACKTEST
- VALIDATION window: 2022-02-09 through 2023-12-13
- provider_errors: 0
- failed_validation_checks: 0
- forecast_computation: NO
- diagnostics_run: NO
- backtests_run: NO
- lockbox_forward_access: NO
- git_operations: NO

Artifacts:

- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/validation/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_row_validation.csv`
- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/provenance/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_provenance.md`

Hostile checks:

- exactly one VALIDATION-window DataBento acquisition receipt
- no CFD adapter path
- no old QuantLab active-pipeline path
- no forecast, position, cost, diagnostic, or backtest artifacts
- no OOS, Lockbox, Forward, deployment, trading, promotion, or Git operation

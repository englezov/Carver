# S09 MES VALIDATION Window DataBento Download Provenance

Date: 2026-06-04

Status:

```text
PASS_S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_QUARANTINE_ONLY_NOT_BACKTEST
```

Authorized scope:

- gate: S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_AUTHORIZED_GATE
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: ohlcv-1d
- VALIDATION window: 2022-02-09 through 2023-12-13
- expected_completed_dates: 574
- raw_symbols: MESH2, MESM2, MESU2, MESZ2, MESH3, MESM3, MESU3, MESZ3, MESH4
- key_source: C:/Users/apops/Desktop/BentoKey.txt

State-history boundary:

TEST may be used later as VALIDATION state-history warmup only under the
separate scoring-mask doctrine. This acquisition gate downloaded only the
locked VALIDATION window and did not score evidence.

Written data artifacts:

- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/sanitized_daily_bars/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/validation/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_row_validation.csv`

Boundary:

No forecast computation, returns, PnL, positions, carry, costs, diagnostics,
backtests, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote publication was authorized or performed.

# S09 MES VALIDATION Pre-Push Package Source-Faithfulness Audit

Date: 2026-06-04

Status:

```text
PASS_S09_MES_VALIDATION_PRE_PUSH_PACKAGE_SOURCE_FAITHFULNESS_AUDIT_READY_FOR_LOCAL_COMMIT_PREP
```

## Scope

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: ohlcv-1d
- VALIDATION window: 2022-02-09 through 2023-12-13
- TEST state-history window: 2020-04-06 through 2022-02-08
- branch: codex/carver-strategy-portfolio-opus-checkpoint
- remote: https://github.com/englezov/Carver.git

## Remote Isolation

`git remote -v` points to the distinct Carver repository:

```text
origin https://github.com/englezov/Carver.git
```

It does not point to the forbidden old QuantLab remote:

```text
https://github.com/englezov/QuantLab_v3.git
```

## Package Checks

- DataBento VALIDATION download status: `PASS_S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_QUARANTINE_ONLY_NOT_BACKTEST`
- DataBento download receipt count: 1
- Download provider errors: 0
- Download failed validation checks: 0
- VALIDATION backtest status: `PASS_S09_MES_VALIDATION_WINDOW_BACKTEST_EXECUTED_EXACTLY_ONCE_NOT_PROMOTION`
- VALIDATION backtest receipt count: 1
- Scored VALIDATION completed dates: 574
- TEST state-history completed dates: 574
- DataBento API access during backtest: `NO_NEW_DATABENTO_API_CALL_USED_EXISTING_AUTHORIZED_DOWNLOADS`
- Lockbox/Forward access: `NO`
- Deployment/trading/promotion: `NO`
- Package secret scan for key-shaped `db-...` tokens: no matches in the new S09 VALIDATION package artifacts.
- New package scan for `QuantLab_v3`, old CFD broker references, `CFD_DIRECT`, and `CFD_ADAPTER`: no matches.
- Python syntax check passed for:
  - `tools/databento/carver_s09_mes_validation_window_download.py`
  - `tools/databento/carver_s09_mes_validation_window_backtest.py`

## Git Hygiene

Unstaged deletions exist under:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/provider_condition_metadata_2026-05-30
```

Those deletions are excluded from local commit prep unless separately authorized by the operator.

## Boundary

This audit authorizes no additional data access, no provider/API call, no new diagnostic, no new backtest, no OOS, no Lockbox, no Forward, no CFD adapter work, no tuning, no deployment, no trading, no promotion, no GitHub push, and no PR.

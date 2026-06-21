# S09 MES TEST Window Backtest Fail-Closed Subagent Hostile Audit Result

Date: 2026-06-04

Status:

```text
SUBAGENT_HOSTILE_AUDIT_CONFIRMS_FAIL_CLOSED_BEFORE_BACKTEST
```

Findings:

- Latest packet: `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08`.
- Manifest confirms `SOURCE_NATIVE_FUTURES`, `TEST`, `2020-04-06` through `2022-02-08`, Databento `GLBX.MDP3`, and `validation_lockbox_forward_access: NO`.
- Raw/sanitized market rows were inside TEST only; no raw provider CSV rows were outside `2020-04-06` through `2022-02-08`.
- Sanitized rows had 574 unique completed dates, min `2020-04-06`, max `2022-02-08`.
- Fail-closed blocker is supported: 574 downloaded completed dates, 570 admitted after `NORMAL_PROVIDER_CONDITION`, with quarantined dates `2020-06-30`, `2020-07-01`, `2021-12-05`, and `2022-01-02`.
- No `backtest_execution_receipt` exists.
- No forecast, backtest row, backtest summary, or success result artifacts were written.
- No VALIDATION, Lockbox, Forward, CFD, old QuantLab active pipeline, Git, deployment, trading, or promotion path was found in the fail-closed result.

Concerns Accepted:

- The attempted packet contains provider-wide `dataset_range.json` metadata. This is not market data outside TEST, but future TEST-only runs should not fetch provider-wide range metadata under the narrow authorization.
- The script used an internal `validation` output directory name for guard checks. Future script output has been renamed to `guard_checks` to avoid collision with the forbidden VALIDATION evidence window language.

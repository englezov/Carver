# S27_V2 Runtime-Evidence Remediation ZN Declared Input Pack Provenance

Date: 2026-06-09

Status:

```text
LOCAL_INPUT_PACK_DECLARED_FOR_RUNTIME_EVIDENCE_REMEDIATION_ONLY_NOT_REPLAY_NOT_BACKTEST_NOT_RESULT
```

Authorization:

```text
S27_V2_LOCAL_ONLY_RUNTIME_EVIDENCE_REMEDIATION_GATE
```

## Scope

This pack is built only from already-local ZN files and is used to remediate the runtime-evidence gate after the older first-populated pack proved stale for V/Q/M. It is not a parser/file replay execution, not a diagnostic, not a backtest, not result interpretation, not PnL evaluation, not promotion, and not a source-faithful evidence claim.

## Selected Local Overlap

```text
decision completed hour: 2026-04-13T03:00:00Z
fill completed hour: 2026-04-13T04:00:00Z
previous completed daily current-contract row: 2026-04-12T00:00:00Z
raw symbol: ZNM6
```

The selected timestamp is the first local timestamp where the inspected V/Q/M runtime status file begins and where local sigma, EWMAC16 trend, hourly decision/fill bars, and daily continuous/current rows overlap.

## Row Families

```text
DAILY_CONTINUOUS_COMPLETED_BAR = 135
DAILY_CURRENT_CONTRACT_COMPLETED_BAR = 1
HOURLY_DECISION_COMPLETED_BAR = 8
HOURLY_FILL_COMPLETED_BAR = 8
SESSION_CALENDAR = 1
ROLL_CALENDAR = 1
COST_PARAMETER = 1
```

The daily continuous file places the selected previous daily row first, followed by strict-prior daily rows from `2025-11-02` through `2026-04-11`. That preserves current selected-row scaffolding while carrying the EWMAC ledger's named 135-row daily span.

## Runtime Evidence Disposition

Local prevalidated evidence is present for sigma, EWMAC(16,64), and V/Q/M at the selected decision timestamp. This closes the stale-V/Q/M problem in the previous pack for local remediation purposes only. It still does not authorize forecast, order, fill, cost, PnL, result, source-faithful evidence, or promotion claims.

Daily/hourly level-space compatibility is represented by a proof hash, not by equality of different-hour prices. The proof is local-only: selected ZNM6 daily continuous/current rows have zero additive back adjustment, and the selected hourly rows are ZNM6 current-contract rows.

Cost/tick/multiplier/currency and working-order lifecycle remain fail-closed for executable use.

## Source Files

```text
5A34C9F0BAFB915A3584A089C7DE35EFC45FC1E6AA64046C3C6EFCDF202B4C1E  docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/ledger/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_local_continuous_daily_risk_history.csv
764660597B7686832C970D908AD82D26899F0792B953072846CB57B44A726161  docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/ledger/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_relative_vol_v_q_m_daily_ledger.csv
F53EEFFF0292869115267269B2C3C180817329DC7D24ED341E18A64CF72423AD  docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/runtime_rows/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_runtime_rows.csv
26BF37503528CCD5A8DB37DC6015529960C9258AFCB259D81300499910442096  docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/forecast_series_only_output/2026-05-31/sigma_runtime_ledger/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_runtime_ledger.csv
4632C63A333C356AAAEC0FB4794D8E74215110ADA10CBAB226A0730DA11520EB  docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/ewmac16_trend_runtime_ledger_2026-05-31/runtime_rows/20260531_ZN_S27_EWMAC16_TREND_RUNTIME_LEDGER_runtime_rows.csv
EF3425BD6A093D76B4073DCDFEE6E7E9A7E27618EEEAB41024DE39B6FDA6D511  docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/databento_ohlcv_1h_extended_forecast_only_quarantine/sanitized_bars/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_sanitized_quarantine_ohlcv_1h.csv
E8707CB3388A6AE235D7DB02F888B9A1D414BFAB3637E1B5E5E2D4856DF07E3C  docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/local_continuous_daily_lineage_2026-05-31/ledger/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_roll_plan.csv
2E1D24FE682B5C4162EC4AF0DDA41305BA51D30894A3C6A044A43DCA455D0D4A  docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/zn_lifecycle_databento_definition_probe_2026-05-31/raw_provider_metadata/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_symbology_raw_symbol_to_instrument_id.json
```


## Non-Authorization

No provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, forecast/order/fill/cost/PnL/result evidence emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim occurred.

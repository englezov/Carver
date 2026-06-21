# S27_V2 Non-2026 Oldest Local ZN Declared Input Pack Provenance

Date: 2026-06-11

Status:

```text
LOCAL_INPUT_PACK_DECLARED_FOR_NON_2026_DEVELOPMENT_RECON_ONLY_NOT_BACKTEST_NOT_RESULT
```

## Scope

This pack was built from already-local ZN source/provider/lineage files only. It is not a parser/file replay execution, not a diagnostic, not a backtest, not a result-scored run, not result interpretation, not PnL evaluation, not promotion, and not a source-faithful evidence claim.

## Selected Slice

```text
selected_decision_timestamp_utc = 2023-05-22T00:00:00Z
selected_fill_timestamp_utc = 2023-05-22T01:00:00Z
selected_previous_daily_timestamp_utc = 2023-05-21T00:00:00Z
raw_symbol = ZNU3
daily_continuous_order = CHRONOLOGICAL_ASCENDING_SELECTED_ROW_LAST
```

## Non-2026 Decision

The existing 2026 ZNM6 packs were explicitly excluded by operator instruction. The existing 2022 ZNH2 pack remains fail-closed because its V/Q/M evidence is stale before the selected 2022 decision row. The first local V/Q/M daily evidence begins on 2023-05-18; the selected slice uses 2023-05-21 V/Q/M strictly prior to the 2023-05-22 decision and avoids the 2023-05-19 roll-transition mismatch.

## Level Bridge

The older candidate-comparison hourly continuous lineage uses additive adjustment 0.84375 around the 2023 ZNM3/ZNU3 roll. This pack does not promote that lineage as level authority. Instead, it reads already-local raw ZNU3 hourly bars and normalizes them to the ten-year V/Q/M daily roll level using additive adjustment 2.28125, matching the selected daily risk-history row. This is a local level-space bridge, not a price-equality claim.

## Working-Order Context

The pack declares only first-row empty working-order state for local Development/Reconciliation runner binding: current position 0 and open working orders 0 at 2023-05-22T00:00:00Z. This is not full multi-row lifecycle evidence; the runner must bind subsequent state row by row.

## Hashes

5A34C9F0BAFB915A3584A089C7DE35EFC45FC1E6AA64046C3C6EFCDF202B4C1E  docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/ledger/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_local_continuous_daily_risk_history.csv
58EEB770CC76E4391CE346098E4B1BA95308EEBC88B72EEF18660D3024B8B5D5  docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/ledger/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_sigma_i_t_ledger.csv
764660597B7686832C970D908AD82D26899F0792B953072846CB57B44A726161  docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/ledger/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_relative_vol_v_q_m_daily_ledger.csv
B4A5AFB95E1E7F133438C55F21ADC2A2EBA26697648014052930B275862E3AB1  docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/ledger/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_roll_plan.csv
ECFF69034C8DDAE994F29932D3AFBCB276FDD803F811DAC0A18DE53BD3915AFE  docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/raw_provider_output/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_hourly_ZNU3_provider.csv
D5B06948D9C0584F93845B3C80A67B7A8EC87602E75D55D2C065ADBEEFB774A1  docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/local_lineage/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_hourly_continuous_lineage.csv

89A4F2FFC0881D4C1B796EB9D84C5B8548C4B172C9F06329493F7A4576D27970  daily_continuous_completed_bar.csv
59448057FF7557B4490B53CEE7B5745C54D187EE984F1167700C106907FC51C9  daily_current_contract_completed_bar.csv
115B49BAB42E3D16BC5BD7571C48A2B09FD6334CEA0710452FF18DAF65B8A5F0  hourly_decision_completed_bar.csv
60B590A17BEC33C06BC4D9415BB2CBDE018CE9B7B3DFB7924642C8AA99764C62  hourly_fill_completed_bar.csv
827662ED700E0CF21CE70214FACC360FB267BDCC893037E2D50FB04DAC74ED55  session_calendar.csv
641BB921E97E9CE43FE07236EBA75387B5266F38FF2DD2F9F3C1DED35289E0F8  roll_calendar.csv
299C720028FEB61C23E63D88D83F3272A632A37B1364BF9655914F6086E75C20  cost_parameter.csv

## Non-Authorizations

No provider/API access, downloads, new data acquisition, 2026 data, TEST, VALIDATION, OOS, Lockbox, Forward, backtest, result-scored run, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git action, or source-faithful evidence claim occurred.

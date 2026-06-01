# Carver Archived QuantLab US500 CFD Positive Anomaly Preservation

Date: 2026-06-01

Status:

```text
PROCESS_ONLY_ARCHIVED_CFD_POSITIVE_ANOMALY_PRESERVED_NOT_SOURCE_NATIVE_AUTHORITY
```

## Purpose

This record preserves a positive-shaped archived `QuantLab_v3` `US500` CFD result as a future investigation lead.

It is not imported into the clean Carver pipeline. It is not source-native futures evidence. It does not override the current Carver S26/S27 source-native futures machinery, the current pure ES result, or any source-native parity requirement.

## Source Workspace

Archived workspace:

```text
C:\Users\openclaw\Desktop\QuantLab_v3
```

Workspace disposition:

```text
ARCHIVED_OPERATIONAL_BLOB_DO_NOT_PIPELINE
```

Allowed use in this record:

```text
READ_ONLY_ARCHAEOLOGY
```

## Preserved Evidence

| Artifact | Path | Observed SHA256 | Preservation status |
|---|---|---:|---|
| P27DC 2023 D1/H1 context source-packet export result | `C:\Users\openclaw\Desktop\QuantLab_v3\docs\researchops\handoffs\CARVER_P27DC_ICMARKETS_US500_2023_D1_H1_READONLY_SOURCE_PACKET_EXPORT_RESULT_2026-05-15.md` | `FB5539F3B5EA3CA8BCD216E1980FFCDE3CA749E30561DADE70379261484B0372` | PRESERVED_AS_CONTEXT_ONLY |
| P27DO OOS 2024 performance one-shot result capture | `C:\Users\openclaw\Desktop\QuantLab_v3\docs\researchops\handoffs\CARVER_P27DO_OOS_2024_PERFORMANCE_ONE_SHOT_RESULT_2026-05-15.md` | `4798A7C05ACD198C0838640CB01FE5FCD40FB9600B93358D44D46E9918496B27` | PRESERVED_AS_CFD_POSITIVE_ANOMALY |
| P27DO reproduction OOS 2024 calibration replay result 005 | `C:\Users\openclaw\Desktop\QuantLab_v3\docs\researchops\handoffs\QLV3_CARVER_FAST_MR_DIAG_ICM_US500_D1_001_P27DO_REPRODUCTION_OOS_2024_CALIBRATION_REPLAY_RESULT_005_2026-05-27.md` | `783B917FF0681EA472D669190AFBF2BF7DA48C7B6CE17A033F77C6C7687B64A2` | PRESERVED_AS_FIXED_MECHANIC_REPRODUCTION |

## Result Snapshot

The archived `P27DO` result was for:

```text
candidate_id: QLV3-CARVER-26-27-ICM-US500-DRAFT-001
lane_class: CFD_DIRECT / ICMarkets US500 CFD
window: OOS_2024
symbol: US500
```

Reported positive-shaped metrics from the archived one-shot result:

| Metric | Value |
|---|---:|
| row_count | 359186 |
| completed_trade_episode_count | 138 |
| gross_pnl_usd | 679.4629807946758 |
| spread_cost_usd | 138.0 |
| swap_usd | -242.96699999999998 |
| commission_usd | 0.0 |
| net_pnl_usd | 298.49598079467575 |
| max_drawdown_usd | 340.3441411511359 |
| profit_factor | 1.4058859723863821 |
| sharpe_daily | 1.5884131556972074 |

The later reproduction replay reported exact fixed-target metric reproduction:

```text
PASS_FIXED_TARGET_METRICS
```

## Why This Matters

The current clean Carver path has produced source-native futures results that may diverge from the archived CFD result, including negative source-native ES behavior. That divergence should not be discarded.

Possible interpretations that remain open:

- the archived CFD result benefited from CFD execution semantics, broker session structure, spread/swap model, or the old limit-ladder mechanics;
- the old implementation used different state/scalar mechanics and is not comparable to the clean source-native futures backtester;
- a future `CFD_ADAPTER` lane may reproduce or falsify the positive-shaped behavior after source-native futures machinery is proven;
- ES futures may be a poor source-native expression while a CFD index adapter behaved differently under old assumptions;
- the archived result may contain implementation artifacts that only a clean second implementation can expose.

## Non-Equivalence Findings

The archived result is not faithful evidence for the current Carver S27 source-native backtester because:

- it used `US500` CFD, not source-native ES/MES/NQ/MNQ/ZN futures;
- it used ICMarkets/MT5 broker rows and CFD contract semantics;
- it used a 2023 D1/H1 context packet as warmup/context, not a source-native futures data foundation;
- it used old QuantLab state machinery, including 2560-state H1 context and dynamic scalar/state behavior;
- it used CFD execution/cost assumptions including modeled spread and swap;
- it was repeatedly labeled not deployable, not proof, not alpha, not promotion, and not source-native futures evidence.

Therefore:

```text
OLD_CFD_POSITIVE_RESULT_DOES_NOT_VALIDATE_CURRENT_SOURCE_NATIVE_BACKTESTER
OLD_CFD_POSITIVE_RESULT_DOES_NOT_RESCUE_NEGATIVE_ES_SOURCE_NATIVE_RESULT
OLD_CFD_POSITIVE_RESULT_REMAINS_INVESTIGATION_LEAD_ONLY
```

## Future Clean Gate If Needed

The next clean use of this preserved anomaly would require a separate gate:

```text
CFD_ADAPTER_US500_ARCHIVED_POSITIVE_ANOMALY_REPRODUCTION_AND_SOURCE_NATIVE_PARITY_GATE
```

That later gate would need to:

- keep source-native futures logic fixed before adapter work;
- explicitly declare `CFD_ADAPTER`;
- rebuild the adapter under Carver rules instead of importing old QuantLab code;
- compare source-native futures signals against CFD execution symbols without tuning;
- preserve broker session, spread, swap, contract-size, and fill assumptions separately;
- explain whether the old positive result survives clean implementation.

## Current Disposition

```text
PRESERVE_RESULT: YES
USE_AS_SOURCE_NATIVE_AUTHORITY: NO
USE_AS_BACKTEST_PARITY_PROOF: NO
USE_AS_ES_NEGATIVE_RESULT_OVERRIDE: NO
USE_AS_FUTURE_CFD_ADAPTER_LEAD: YES
```

## Non-Authorization

This record authorizes no code import from `QuantLab_v3`, no old pipeline execution, no CFD adapter work, no provider access, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend computation, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

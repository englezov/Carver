# Carver ZN Local Continuous Daily Databento Definition Lifecycle Probe Result

Date: 2026-05-31

Status:

```text
FAIL_CLOSED_DATABENTO_DEFINITION_PROVES_EXPIRATION_ACTIVATION_ONLY_OFFICIAL_LIFECYCLE_STILL_REQUIRED
```

## Purpose

This record preserves the bounded Databento metadata-only probe opened for the S27 EWMAC16 trend dependency.

The S27 source gate requires a source-faithful back-adjusted continuous daily ZN input before any real EWMAC16 trend runtime ledger can be emitted. Existing local dated-contract daily rows already provide adjacent ZNH6/ZNM6 rows, but the local continuous roll plan remains blocked because lifecycle blocker dates are not source-locked.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

## Authorized Provider Touch

Provider:

```text
Databento Historical
```

Dataset/schema:

```text
GLBX.MDP3 / definition
```

Request symbols:

```text
ZNH6
ZNM6
ZNU6
```

Request window:

```text
2026-03-01T00:00:00Z through 2026-05-30T00:00:00Z
```

Boundary:

```text
NO_OHLCV_DOWNLOAD
NO_MARKET_ROW_PARSING
NO_CONTINUOUS_CONTRACT_DOWNLOAD
NO_PROVIDER_BUILT_CONTINUOUS_SERIES
NO_TREND_COMPUTATION
NO_S27_COMPUTATION
NO_DIAGNOSTICS
NO_BACKTESTS
NO_POSITIONS
```

## Result

Databento returned definition metadata rows and a three-row lifecycle definition ledger.

Locked from Databento definition metadata:

| Raw symbol | Instrument id | Activation | Expiration | Currency | Exchange | Asset/group |
|---|---:|---|---|---|---|---|
| ZNH6 | 42004475 | 2025-06-18 21:30:00+00:00 | 2026-03-20 17:01:00+00:00 | USD | XCBT | ZN / ZN |
| ZNM6 | 42000661 | 2025-09-19 21:30:00+00:00 | 2026-06-18 17:01:00+00:00 | USD | XCBT | ZN / ZN |
| ZNU6 | 42001136 | 2025-12-19 22:30:00+00:00 | 2026-09-21 17:01:00+00:00 | USD | XCBT | ZN / ZN |

Still not locked:

```text
first_notice_date
delivery_window_start
delivery_window_end
last_delivery_date
official roll-blocker precedence
official daily settlement versus close policy for roll alignment
```

## Disposition

The probe improves the static identity evidence for the ZN roll chain, but it does not resolve the lifecycle blocker that stopped local continuous construction.

The S27 EWMAC16 trend dependency remains fail-closed:

```text
S27_EWMAC16_REAL_TREND_RUNTIME_LEDGER = NOT_AVAILABLE
reason = BACK_ADJUSTED_CONTINUOUS_DAILY_ZN_INPUT_NOT_SOURCE_LOCKED
```

## Artifacts

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/zn_lifecycle_databento_definition_probe_2026-05-31/
```

Important files:

```text
raw_provider_metadata/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_definition.dbn
raw_provider_metadata/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_definition_dataframe.csv
raw_provider_metadata/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_symbology_raw_symbol_to_instrument_id.json
ledger/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_lifecycle_definition_ledger.csv
status/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_status.json
provenance/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_provenance.json
hashes/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_sha256.json
```

## Next Required Gate

```text
OFFICIAL_STATIC_ZN_LIFECYCLE_EVIDENCE_OR_FAIL_CLOSED_ROLL_POLICY_DECISION
```

That gate must use official static exchange/provider lifecycle evidence for the 10-year Treasury Note futures contract family, or explicitly decide that ZN local continuous daily lineage remains blocked.

## Non-Authorization

This result authorizes no additional Databento access, no OHLCV request, no market-row parsing, no continuous-contract download, no provider-built continuous source authority, no EWMAC16 computation, no S27 computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend sleeve, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, and no Git operation.

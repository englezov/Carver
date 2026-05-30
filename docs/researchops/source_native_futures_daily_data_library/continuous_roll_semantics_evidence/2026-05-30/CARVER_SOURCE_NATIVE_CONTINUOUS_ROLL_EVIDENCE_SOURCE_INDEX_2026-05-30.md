# Carver Source-Native Continuous/Roll Evidence Source Index - 2026-05-30

## Status

```text
PROCESS_SOURCE_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Scope

Gate 2 executed static evidence ledgers only. The output identifies book, provider, exchange, and existing local-quarantine evidence needed before a later continuous/roll daily data policy decision.

No provider API call, provider login, provider account portal use, new market-data request, data download, market-row parsing, continuous-contract download, continuous-series construction, strategy input creation, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility or risk calculations, OOS, Lockbox, Forward, CFD adapter execution, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote operation occurred.

## Local Source Inputs And Hashes

| Role | Path | SHA256 |
|---|---|---|
| Local book authority, Carver.pdf | `Carver.pdf` | `AA052B8D942767A7547ECDBB09FBED22F2412FB7B1036D24AB854738308582B6` |
| Continuous/roll shape gate | `docs\process\CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_SHAPE_GATE_2026-05-30.md` | `8EA38676F008BDE787F7FD2F80D360A1FC49785BAF8FC3CD07F0EAE6A2CB04E1` |
| Continuous/roll evidence packet | `docs\process\CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET_2026-05-30.md` | `E124735263D1A1049DB49ED25103FA7F0F11EF011D6B101307B7402CE45B38ED` |
| Continuous/roll evidence execution draft | `docs\process\CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_GATE_DRAFT_2026-05-30.md` | `B8D01832AC4D285E4805ABC55060B5EE7B578C19EFD8CA0E5C835D23E1CC7335` |
| Goal completion matrix | `docs\process\CARVER_DAILY_DATA_FOUNDATION_COMPLETION_CRITERIA_AND_EVIDENCE_MATRIX_2026-05-30.md` | `0123D4C7000A604E5748F861DB71AB1AD9D858C8260E983687365DA75662F450` |
| Current authorization queue | `docs\process\CARVER_DAILY_DATA_FOUNDATION_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_2026-05-30.md` | `1BFEC1D73BFDD755C422D43F18C717B10507A6A36C64899322E23F0CCAD8DCDC` |
| Canonical 16-symbol manifest, additional local context | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\manifest\CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv` | `0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88` |

All required local-source/process hashes matched the preflight contract before the ledgers were created.

## Book Source Ranges Reviewed

- `Carver.pdf`, Strategy One pages 21-66: local extraction re-confirmed that S01 introduces futures expiry/rolling, back-adjusted futures prices, daily closing prices by contract expiry, costs separately, adjusted futures prices as excess-return series, and price-change-times-multiplier profit mechanics.
- `Carver.pdf`, Strategy Ten pages 232-259: reviewed as carry caveat range. Carry requires raw futures prices and curve-leg/expiry-distance evidence; this Gate 2 does not open carry computation.
- Existing S01 process brief reviewed as a secondary local summary, not as a replacement for the PDF.

## Provider Static Documentation Reviewed

- Databento continuous contracts example: `https://databento.com/docs/examples/symbology/continuous`
- Databento standards and conventions: `https://databento.com/docs/standards-and-conventions`
- Databento schemas and data formats: `https://databento.com/docs/schemas-and-data-formats`
- Databento portal/support-file documentation: `https://databento.com/docs/portal`

Provider evidence results:

- Databento continuous symbols are documented as smart symbology mapping to actual tradable instruments by date.
- Databento documents continuous prices as original and unadjusted, not a back-adjusted synthetic series.
- Databento documents continuous syntax and roll-rule codes, including calendar, open-interest, and volume ranks.
- Databento OHLCV bars are aggregate trade bars; official settlement-style daily statistics are a separate schema class.
- Databento condition support files/metadata are documented, but no provider API call was made by this gate.

## Exchange Or Official Product Sources Reviewed

- CME 2-Year, 5-Year, and 10-Year Treasury contract specification pages plus CME `Understanding Treasury Futures` PDF.
- CME Micro E-mini S&P 500, Nasdaq-100, Russell 2000, and Dow contract specification pages plus CME Micro E-mini futures fact-card evidence.
- CME WTI/E-mini WTI static product references and RBOB Gasoline contract specification page.
- CME Corn, Soybean, Soybean Meal, Soybean Oil, and Chicago SRW Wheat contract specification pages plus CME daily grains settlement procedure.
- CME Lean Hog and Live Cattle contract specification pages.

Exchange evidence is sufficient to identify official static source classes for policy work, but not sufficient to promote any symbol to strategy input. Full lifecycle and settlement/close policy extraction remains required.

## Existing Local Quarantine Provenance Reviewed

- Existing Databento 16-symbol dated-contract archive provenance and metadata records were inspected as local context only.
- Gate 1 fragment table outputs were reviewed as proof that local dated-contract plumbing exists for 4,483 normal provider-condition rows and excludes 85 degraded rows.
- No dated-contract fragment row was promoted to continuous or strategy-facing input.

## Evidence Boundaries

This evidence index and the CSV ledgers are evidence-only. They do not choose a continuous/roll policy, do not build a continuous row set, do not create strategy-facing daily input, and do not solve carry raw-price/curve-leg evidence.

## Blocked Or Unresolved Source Classes

- `SETTLEMENT_CLOSE_POLICY`: blocked pending decision between trade OHLCV close, official settlement/statistics, and product-family official references.
- `CONTINUOUS_LINEAGE`: blocked pending proof that every continuous row maps to raw dated-contract source rows with hashes and provider-condition labels.
- `LIFECYCLE_RULEBOOK_EXTRACTION`: partial and product-family-specific; first notice, last trade, expiration/termination, delivery/cash settlement, holidays, and roll-safety rules need full extraction before policy.
- `CARRY_RAW_PRICE_AND_CURVE_LEGS`: blocked for carry and combined trend/carry strategies.

## Output Ledgers

- `CARVER_16_SYMBOL_CONTINUOUS_ROLL_EVIDENCE_REQUIREMENTS_2026-05-30.csv`
- `CARVER_16_SYMBOL_CONTINUOUS_ROLL_PROVIDER_CAPABILITY_STATUS_2026-05-30.csv`
- `CARVER_16_SYMBOL_CONTINUOUS_ROLL_LIFECYCLE_EVIDENCE_NEEDS_2026-05-30.csv`
- `CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_PACKET_SHA256SUMS_2026-05-30.txt`

## Audit Requirement

A lean hostile audit must verify static source boundaries, schema conformity, 16-symbol coverage, conservative strategy-use labels, no provider API/login, no data download, no market-row parsing, no continuous-series construction, no strategy input, and no prohibited computation.

## Non-Authorization

This Gate 2 execution authorizes no provider API access, provider login, provider account portal use, new market-data request, data download, market-row parsing, continuous-contract download, continuous-series construction, strategy input creation, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility or risk calculations, OOS, Lockbox, Forward, CFD adapter execution, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote operations.

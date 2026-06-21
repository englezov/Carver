# Carver 16-Symbol Local Continuous Daily Lineage Rerun Provenance

Date: 2026-05-30

Status:

```text
FAIL_CLOSED_LIFECYCLE_EVIDENCE_MISSING_AFTER_ROLL_CHAIN_EXPANSION_NO_LOCAL_CONTINUOUS_SERIES_CONSTRUCTED
```

This rerun used only local Carver CSV artifacts, including the separately authorized Databento dated-contract roll-chain expansion for the locked 16 roots. It did not call Databento, request provider data, download data, use provider-built continuous contracts, run diagnostics, run backtests, compute forecasts, positions, costs, carry, trend, volatility/risk, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active pipeline state, or perform Git/remote operations.

Debug result:

- Original blocker cleared: all 16 symbols now have previous/current normal-provider-condition overlap rows available.
- Construction remains fail-closed: the locked `STATIC_LIFECYCLE_BUFFER_ROLL` requires explicit first-notice/last-trade/delivery/expiration/final-settlement blocker dates before selecting a roll transition date.
- No roll transition date was selected.
- No adjustment ledger rows were produced.
- No local continuous series rows were produced.

Input expansion fragment:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_ROLL_CHAIN_EXPANSION/2026-05-30_PREV_CURRENT_NEXT_DEV_RECON_AVAILABLE_END_2026-05-30/sanitized_bars/CARVER_16_SYMBOL_DATED_CONTRACT_ROLL_CHAIN_EXPANSION_2026-05-30.csv
SHA256: 22729608CC5B4FF4FEC0C6118654490B466776F63432E3CA73011CD926B443A8
```

Provider-condition join:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_ROLL_CHAIN_EXPANSION/2026-05-30_PREV_CURRENT_NEXT_DEV_RECON_AVAILABLE_END_2026-05-30/provider_condition_join/CARVER_16_SYMBOL_DATED_CONTRACT_ROLL_CHAIN_PROVIDER_CONDITION_JOIN_2026-05-30.csv
SHA256: 1CD183CB24E3C4A4CC569AA13C263114E3C4DF8423026D28C5430CBD8C512DA5
```

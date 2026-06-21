# Databento 16-Symbol Per-Symbol Current Instrument-ID Full-History Quarantine Archive Provenance

Date: 2026-05-30

Status:

```text
PASS_WITH_PROVIDER_CONDITION_WARNINGS_16_SYMBOL_DATED_CONTRACT_PER_SYMBOL_CURRENT_ID_FULL_HISTORY_QUARANTINE_ONLY
```

## Identity Rule

The first wide raw-symbol full-history request failed closed after the provider stream ended prematurely. The saved Databento symbology resolution also showed older raw-symbol intervals for some symbols. This archive therefore uses one exact 2026-current `instrument_id` per locked raw symbol, derived from the saved symbology resolution, while preserving the locked dated-contract identity.

## Request Strategy

One exact current `instrument_id` request was made per locked raw symbol for `GLBX.MDP3` / `ohlcv-1d`, with matching `definition` metadata requests. No continuous contracts were requested.

## Provider Condition Caveat

Databento emitted reduced-quality warnings during several per-symbol requests. The archive passes quarantine row-shape validation, but provider condition warnings remain a readiness caveat before any later strategy or production use.

## Boundaries

Quarantine-only market-row parsing was performed only on the exact provider output from this request. No diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk calculations, OOS, Lockbox, Forward, CFD adapter work, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update, or remote repository operation was performed.

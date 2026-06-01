# Governance, Scope, And Current State

## Packet Purpose

This packet asks Opus to perform a hostile review of the S27 ZN robustness checks and to make sense of the result pattern now observed:

```text
2022-2023: positive but MCPT primary window not significant
2024: strongly positive validation-style / touched evidence
2025-2026: negative available-row result, but complete-window interpretation fail-closed because provider degraded dates exist
```

The requested review is interpretive and hostile. It must decide what can and cannot be inferred from the evidence so far, what robustness checks are missing, whether the ladder is helping or merely levering regime exposure, and what the next clean gate should be.

## Source Authority

Primary source authority:

```text
00_Carver.pdf
```

Relevant book frame:

- Strategy 26: "Strategy twenty-six: Fast mean reversion", Part Four, Chapter 26, pp. 476-489.
- Strategy 27: "Strategy twenty-seven: Safer fast mean reversion", Part Four, Chapter 27, pp. 499-509.
- Part Four controlling frequency statement: p. 475 says these strategies are backtested on hourly data.
- Strategy 27 uses fast mean reversion with an EWMAC16 trend overlay and volatility attenuation; it is not a daily Appendix C strategy.

## Lane And Interpretation

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Instrument under review:

```text
ZN / US 10-year Treasury Note futures
```

Interpretation labels:

```text
S27_SOURCE_NATIVE_FUTURES_ZN_ONLY
DEVELOPMENT_RECONCILIATION
NOT_LOCKBOX
NOT_PROMOTION
```

The current evidence is not a portfolio result, not an Appendix C Jumbo result, not an adapter result, and not a CFD result.

## Controlling Boundaries

This packet must not authorize or imply:

```text
NO_NEW_PROVIDER_API_ACCESS
NO_NEW_DATA_DOWNLOAD
NO_NEW_MARKET_ROW_PARSING
NO_NEW_BACKTEST_EXECUTION
NO_DIAGNOSTICS_EXECUTION
NO_FORECAST_OR_POSITION_RECOMPUTATION
NO_TUNING
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_DEPLOYMENT
NO_TRADING
NO_PROMOTION
NO_GIT_OPERATIONS
NO_REMOTE_OPERATIONS
NO_CFD_ADAPTER
NO_OLD_QUANTLAB_ACTIVE_PIPELINE_USE
```

Opus may reason from the packet and the cited files only. It should not request live Databento access, reruns, new calculations, or hidden data.

## State Before This Packet

Previous Opus S26/S27 design audit found:

```text
AUDIT_DISPOSITION: SOURCE_PATH_DEFINED_BUT_BLOCKED_AT_FIRST_REAL_DATA_GATE_BY_FREQUENCY
```

The block was daily-vs-hourly frequency mismatch. We then built S26/S27 hourly ZN mechanics, tested 2022-2023 and 2024, ran robustness/null checks, and later added 2025-2026 hourly ZN data under an explicitly touched-support Development/Reconciliation label.

Current most important statuses:

```text
2022_2024_TOUCHED_HISTORY_STATUS:
  PASS_S27_ZN_TOUCHED_HISTORY_DEV_RECON_BACKTEST_NOT_LOCKBOX_NOT_PROMOTION

2025_2026_TOUCHED_SUPPORT_STATUS:
  FAIL_CLOSED_S27_ZN_2025_2026_TOUCHED_SUPPORT_PROVIDER_DEGRADED_DAYS_AVAILABLE_ROWS_ONLY_NOT_COMPLETE_BACKTEST

2025_2026_HOSTILE_AUDIT_DISPOSITION:
  FAIL_CLOSED_PROVIDER_DEGRADED_DAYS_NUMERIC_RESULT_AVAILABLE_ROWS_ONLY_NOT_LOCKBOX_NOT_PROMOTION
```

## Central Question

The core hostile question is:

```text
Do the 2022-2024 positive results survive enough robustness scrutiny to justify a next clean evidence gate, or do the 2025-2026 negative available-row result, MCPT weakness in 2022-2023, cost uncertainty, and provider-degraded days suggest the apparent edge is regime-specific, fragile, or mechanically overfit?
```

Opus should answer in terms of evidence quality and next gates only. No alpha claim is authorized.

# Carver Window State Warmup And Scoring Mask Opus Hostile Audit Result

Date: 2026-06-04

Status:

```text
PASS_NARROW_WARMUP_SCORING_MASK_REMEDIATION_CLEAN_TEST_RERUN_STILL_BLOCKED
```

## Scope

This record preserves the external Opus hostile audit result for the S09 MES
window warmup remediation.

Audited question:

```text
previous_window_for_state_warmup_only -> current_window_for_scoring_only
```

The audit used the readable four-file packet plus `Carver.pdf`. Zip-file packet
contents are not relied on.

## Verdict

Opus verdict:

```text
PASS
```

Narrow scope:

```text
WARMUP_TO_SCORING_MASK_REMEDIATION_ONLY
```

Blocking findings inside that narrow scope:

```text
NONE
```

## Confirmed By Opus

- The doctrine separates previous-window state warmup from current-window scored
  evidence.
- The S09 MES TEST state-history interval is `2019-05-05` through
  `2020-04-05`.
- The S09 MES TEST scoring interval remains `2020-04-06` through
  `2022-02-08`.
- Pre-TEST rows are retained only as non-scored state history.
- Forecast rows are gated to the scoring window.
- Backtest rows require both signal date and next PnL date inside the scoring
  window.
- State-history rows cannot contribute to scored trade count, costs, PnL,
  summaries, or performance.
- The stale original `PASS...` and `CONSUMED...` receipt wording is retired for
  future clean payloads.
- Direct Databento download from the TEST runner remains quarantined.
- The prior S09 MES TEST result remains diagnostic-only and cannot be used for
  VALIDATION.

## Non-Blocking Concerns

Opus recorded these as non-blocking for the warmup-mask remediation:

- The runner cannot produce clean TEST evidence today because
  `DEGRADED_OHLCV_POLICY_DISPOSITION` remains
  `POST_FAIL_DATE_SPECIFIC_POLICY_DIAGNOSTIC_ONLY_NOT_VALIDATION_GATE`.
- The whole-contract-equivalent trade-count threshold is a separate audit choice
  and must be treated as discrete-trade evidence, not fractional churn evidence.
- Mask tests use a mocked S09 forecast result for the mask-boundary question;
  this is acceptable for mask auditing but is not forecast-numerical
  correctness evidence.
- Continuous-lineage additive adjustment math at the warmup/scoring seam was not
  exhaustively re-audited by this packet.
- Operators must not combine `state_history_completed_dates` with
  `completed_dates` when reading scored evidence counts.

## Clean TEST Rerun Disposition

Opus final answer to whether this is ready for operator consideration of a
separately authorized clean TEST rerun:

```text
NO
```

Reason:

The warmup/scoring mask remediation passed, but clean TEST execution remains
blocked until at least the degraded OHLCV policy is replaced by a cold,
shape-based policy and the remaining pre-clean-TEST blockers are repaired and
separately hostile-audited.

## Boundary

This audit result authorizes no provider API access, no new market-data request,
no data download, no market-row parsing, no diagnostics, no backtests, no
forecasts as evidence, no positions as evidence, no costs as evidence, no TEST
rerun, no VALIDATION, no Lockbox, no Forward, no CFD adapter execution, no old
QuantLab active pipeline use, no tuning, no deployment, no trading, no
promotion, no Git staging, no commit, no push, no PR, and no remote operation.

# Opus Requested Output And Hostile Checklist

## Requested Output

Produce a hostile audit and interpretation memo for the S27 ZN robustness evidence.

Required final verdict fields:

```text
BLOCKING_FINDINGS: YES/NO
AUDIT_DISPOSITION: <single all-caps disposition>
RECOMMENDED_NEXT_GATE: <single exact gate name>
```

The verdict must separate:

```text
MECHANICAL_SOUNDNESS
ROBUSTNESS_EVIDENCE
STATISTICAL_EVIDENCE
COST_READINESS
DATA_QUALITY_READINESS
LOCKBOX_READINESS
PROMOTION_READINESS
```

## Questions Opus Must Answer

1. Does the evidence support that the S27 ZN machinery is mechanically coherent, or are there remaining source-faithfulness/mechanics risks that could plausibly reverse the result?

2. What should we infer from the 2022-2023 primary window being positive but not MCPT-significant?

3. What should we infer from 2024 being strongly positive but non-pristine / touched / validation-style rather than Lockbox?

4. What should we infer from 2025-2026 being negative on available rows, with complete-window interpretation fail-closed because of provider degraded days?

5. Are the 2025-2026 degraded dates likely enough to explain the sign flip, or should the negative available-row result be treated as meaningful regime evidence despite fail-closed complete-window status?

6. Is the M1 ladder a source-consistent sizing implementation, an added overlay, an exposure/risk amplifier, or an overfit layer? Explain using the fee-side and year-by-year evidence.

7. Do the current null checks sufficiently defend against beta/rate-regime exposure, serial correlation, one-bar timing leakage, and overfit? If not, name the missing tests.

8. Does the constant-long and matched-average-absolute-position beta strip evidence reduce or increase confidence?

9. Does the positive delayed 1-bar result in 2024 weaken the causal signal claim?

10. Should we continue with S27 ZN, move to broader bonds, require a clean untouched window, require futures-realistic cost closure first, or stop this lane until stronger evidence exists?

## Hostile Checklist

Attack the following possible failure modes:

```text
LOOKAHEAD_OR_SAME_BAR_EXECUTION
DAILY_SUPPORT_TOUCH_CONTAMINATION
HOURLY_DATA_PROVIDER_CONDITION_DEGRADATION
ROLL_CHAIN_OR_CONTRACT_SELECTION_ERROR
SESSION_OR_COMPLETED_BAR_ALIGNMENT_ERROR
S26_MEAN_REVERSION_FORMULA_ERROR
S27_TREND_OVERLAY_OR_VQM_DEPENDENCY_ERROR
LADDER_NON_SOURCE_NATIVE_OVERLAY
COMMISSION_ONLY_COST_UNDERSTATEMENT
SPREAD_SLIPPAGE_LIMIT_FILL_OMISSION
BETA_OR_RATE_REGIME_EXPOSURE
RANDOMIZATION_NULL_TOO_WEAK
MCPT_MULTIPLE_TESTING_OR_WINDOW_SELECTION
2024_VALIDATION_STYLE_OVERINTERPRETATION
2025_2026_NEGATIVE_RESULT_UNDERINTERPRETATION
LOCKBOX_MISLABELING
PROMOTION_LANGUAGE
```

## Evidence Interpretation Rules

Opus should use these strict labels:

```text
2022-2023 = DEVELOPMENT_RECONCILIATION_FROZEN_INITIAL_ZN_CLAIM
2024 = VALIDATION_STYLE_NON_LOCKBOX_RETAINED_NOT_PRISTINE_LOCKBOX
2025-2026 = TOUCHED_SUPPORT_DEVELOPMENT_RECONCILIATION_AVAILABLE_ROWS_ONLY_NOT_COMPLETE_WINDOW
```

No combined 2022-2026 statistic should be used as pass/fail evidence.

No result is Lockbox.

No result is promotion.

No result authorizes trading.

## Desired Next-Gate Recommendations

Opus may choose one or more, but must nominate a single best next gate:

```text
GATE_A_STOP_AND_PATCH_MECHANICS
GATE_B_FUTURES_REALISTIC_COST_AND_FILL_READINESS_BEFORE_MORE_BACKTESTS
GATE_C_PROVIDER_CONDITION_CLEAN_WINDOW_RETEST
GATE_D_BONDS_BREADTH_TEST_ZT_ZF_ZN_ONLY
GATE_E_S27_ZN_CLEAN_UNTOUCHED_LOCKBOX_SHAPE_ONLY
GATE_F_ABORT_S27_ZN_STANDALONE_AND_RECLASSIFY_AS_PORTFOLIO_OR_REGIME_DEPENDENT
GATE_G_REQUEST_EXTERNAL_REPRODUCTION_SECOND_IMPLEMENTATION
```

The recommendation should be practical and fast. It should not add ceremony unless the current evidence truly demands it.

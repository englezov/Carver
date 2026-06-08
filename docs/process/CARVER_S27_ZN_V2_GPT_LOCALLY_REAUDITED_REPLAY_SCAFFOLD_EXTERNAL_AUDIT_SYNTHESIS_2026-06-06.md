# S27 ZN V2 GPT Locally Re-Audited Replay Scaffold External Audit Synthesis

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_GPT_LOCALLY_REAUDITED_REPLAY_SCAFFOLD_EXTERNAL_AUDIT_SYNTHESIS_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Source

External GPT Extended Pro / GPT-5.5 hostile audit received from the operator after the locally re-audited scaffold packet handoff:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_LOCALLY_REAUDITED_EXTERNAL_AUDIT_HANDOFF_2026-06-06.md
```

This synthesis records the audit result only. It authorizes and performed no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Verdict

```text
PASS_WITH_REQUIRED_EDITS
```

GPT found the locally re-audited scaffold broadly aligned with the attached `Carver.pdf` and S27 ZN source-lock direction, but not ready to advance directly to parser/file replay implementation planning.

The latest local patch sequence was accepted as closed for:

```text
COST_ARITHMETIC_BINDING
PRICE_SPACE_SPREAD_COST_ARITHMETIC
LIMIT_COST_ROW_OPTIONAL_FIELD_EXCLUSIVITY
TRANSITION_OPTIONAL_FIELD_EXCLUSIVITY
TRUST_ROOT_PROVENANCE_SCHEMA_LEVEL_CROSS_CHECKS
```

No provider/API path, download path, parser/file replay execution path, diagnostics/backtest entry point, OOS/Lockbox/Forward path, live-data path, subprocess/CLI path, deployment/trading path, or PnL/result interpretation path was reported in the extracted scaffold.

## P0

```text
NONE_FOUND
```

The fail-closed runner boundary remains intact:

```text
src/carver/spine/s27_v2_replay/runner.py
```

`build_trusted_replay_bundle` still raises `ReplayExecutionBlocked`.

## P1 Source-Faithfulness Blockers

### P1-1 Source-Row And Forecast Positivity Not Fail-Closed

Affected surfaces:

```text
src/carver/spine/s27_v2_replay/source_rows.py
src/carver/spine/s27_v2_replay/forecast.py
```

The current scaffold accepts finite but non-positive source closes and forecast sigma bridge values where the local data contract/source lock requires positive values.

Current verified examples:

```text
LocalDailySourceRow.close_price uses require_finite_number
LocalDailySourceRow.annual_percentage_sigma uses require_non_negative_number
LocalHourlySourceRow.close_price uses require_finite_number
ForecastReplayLedgerRow.sigma_bridge_price_value uses require_finite_number
ForecastReplayLedgerRow.annual_percentage_sigma_value uses require_finite_number
ForecastReplayLedgerRow.sigma_price_value uses require_finite_number
```

Required patch direction:

```text
Require positive source closes, positive annual percentage sigma, positive sigma bridge price, positive sigma price, positive V/M multiplier-related values where source-locked, and fail closed on invalid row values.
```

### P1-2 Trend-Veto, Zero-Trend, And Cap Invariants Under-Enforced

Affected surface:

```text
src/carver/spine/s27_v2_replay/forecast.py
```

The current scaffold accepts `ewmac16_64_trend_sign == ZERO`, does not bind the trend-veto decision to the sign relationship between the mean-reversion forecast and EWMAC trend, and validates `capped_forecast_value` as merely finite.

Required patch direction:

```text
Reject unresolved ZERO trend unless separately source-locked.
Require opposing trend/mean-reversion signs to zero the forecast.
Require agreeing signs to preserve the pre-veto forecast.
Reject unresolved zero mean-reversion sign unless separately source-locked.
Enforce -20 <= capped_forecast_value <= 20.
```

### P1-3 Exact Fill-Lag / Next-Completed-Row Proof Not Bound

Affected surfaces:

```text
src/carver/spine/s27_v2_replay/identity.py
src/carver/spine/s27_v2_replay/transitions.py
src/carver/spine/s27_v2_replay/fills.py
```

The current scaffold only requires `fill_as_of_utc > decision_as_of_utc` and syntactic hash fields. It does not fail closed on arbitrary later fill timestamps, nor does it bind normal one-hour lag to the exact next completed hourly fill row or require explicit session-gap/overnight/roll proof for non-simple cases.

Required patch direction:

```text
Add exact next-completed hourly fill row/session-gap proof fields and validators, or otherwise fail closed on arbitrary later fills before parser/file replay planning relies on these schemas.
```

## P2 Hardening Items

### P2-1 Public Exports Expose Forgeable Structural Rows

Affected surface:

```text
src/carver/spine/s27_v2_replay/__init__.py
```

Package-level exports expose structural row dataclasses that can be caller-forged. The runner still fails closed, so this is not P0, but GPT recommends reducing the public surface or labeling structural rows as schema-only/not evidence.

### P2-2 Evidence Manifest Completeness Too Weak

Affected surfaces:

```text
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/trust_root.py
src/carver/spine/s27_v2_replay/runner.py
```

The trust-root/evidence-manifest hash equality cross-check exists, but the manifest does not yet enforce required artifact families or stale/superseded evidence completeness.

### P2-3 V/Q/M And Post-Veto Arithmetic Value-Auditable But Not Bound

Affected surface:

```text
src/carver/spine/s27_v2_replay/forecast.py
```

The scaffold exposes V, Q, raw multiplier, EWMA10 multiplier, post-veto-times-M, scalar, cap, and desired-position values, but does not bind arithmetic relationships such as:

```text
raw_multiplier = 2 - 1.5 * Q
post_veto_times_m = risk_adjusted_forecast_after_veto * M
capped_forecast = clamp(post_veto_times_m * scalar, -20, +20)
```

GPT classified this as P2 implementation hardening, with the P1 cap/sign fixes as the minimum blocker.

## P3

```text
P3_M0_CARRIES_UNUSED_CFD_ADAPTER_ENUM_VALUES
P3_IMPORT_COMPILE_ASSURANCE_REMAINS_OUTSIDE_STATIC_AUDIT_SCOPE
```

Neither P3 is a source-faithfulness blocker under the current static scaffold gate.

## Next Gate

Do not proceed directly to parser/file replay implementation planning.

The next safe gate is a narrow schema fail-closed patch and static local hostile re-audit covering:

```text
P1_SOURCE_ROW_AND_FORECAST_POSITIVITY
P1_TREND_ZERO_VETO_AND_CAP_INVARIANTS
P1_EXACT_NEXT_COMPLETED_FILL_ROW_OR_SESSION_GAP_PROOF
```

It is efficient, but separately a scope decision, to include:

```text
P2_PUBLIC_EXPORT_STRUCTURAL_SCHEMA_ONLY_HARDENING
P2_EVIDENCE_MANIFEST_REQUIRED_FAMILY_HARDENING
P2_VQM_POST_VETO_ARITHMETIC_BINDING
```

Recommended authorization text:

```text
Operator authorizes S27_V2 replay scaffold GPT P1 fail-closed schema patch only, covering source-row/forecast positivity, trend-veto/zero/cap invariants, and exact next-completed fill-row or session-gap proof scaffolding, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

If the operator wants to include the P2s in the same patch, extend the authorization explicitly to include public-export hardening, evidence-manifest required-family hardening, and V/Q/M arithmetic binding.

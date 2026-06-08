# S27 ZN V2 GPT P2 External Audit Synthesis

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_GPT_P2_EXTERNAL_AUDIT_SYNTHESIS_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Source

External GPT Extended Pro hostile audit was received after the locally re-audited GPT P2 hardening handoff:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_EXTERNAL_AUDIT_HANDOFF_2026-06-06.md
```

Verdict:

```text
PASS_WITH_REQUIRED_EDITS
```

This synthesis records the external audit result only. It authorizes and performed no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## P0 Findings

```text
NONE_FOUND
```

GPT found the scaffold still fail-closed at the runner boundary and found no parser/file replay execution path, provider/API path, download path, old close-to-close runner path, deployment/trading path, or PnL interpretation path in the supplied scaffold package.

## P1 Findings

### P1-1: Zero Mean-Reversion Forecast Is Over-Rejected

File:

```text
src/carver/spine/s27_v2_replay/forecast.py
```

Finding:

```text
FORECAST_ZERO_MEAN_REVERSION_EQUILIBRIUM_CASE_REJECTED
```

GPT found that `_nonzero_sign()` rejects zero and is applied to `risk_adjusted_forecast_before_veto_value`, so a zero mean-reversion/equilibrium forecast cannot be represented before trend-veto logic.

Why it matters:

```text
BOOK_NATIVE_FLAT_AT_EQUILIBRIUM_CASE_MUST_BE_REPRESENTABLE
```

GPT stated this conflicts with the Strategy 27 source behavior where current price equal to equilibrium closes/flattens rather than failing closed. The zero-trend case may remain fail-closed unless separately source-locked; the blocker is zero mean reversion, not zero EWMAC trend.

Minimal required correction queued:

```text
ALLOW_EXPLICIT_SOURCE_LABELED_ZERO_MEAN_REVERSION_FLAT_EQUILIBRIUM_BRANCH
```

The correction should require a source-labeled flat/equilibrium decision, post-veto forecast zero, post-veto-times-M zero, capped forecast zero, and compatible desired position zero.

## P2 Findings

### P2-1: Package Root Exposes Manually Constructible Trusted Bundle Object

Files:

```text
src/carver/spine/s27_v2_replay/__init__.py
src/carver/spine/s27_v2_replay/runner.py
```

Finding:

```text
PACKAGE_ROOT_EXPORTS_TRUSTED_REPLAY_BUNDLE_SCAFFOLD
```

GPT found that the fail-closed builder is not enough because `TrustedReplayBundleScaffold` remains package-root exported and directly instantiable with trusted-bundle status.

Why it matters:

```text
FALSE_EVIDENCE_RISK_BEFORE_AUTHORIZED_REPLAY_BUILDER_EXISTS
```

Minimal required correction queued:

```text
REMOVE_TRUSTED_REPLAY_BUNDLE_SCAFFOLD_FROM_PACKAGE_ROOT_EXPORTS_OR_MAKE_STATUS_STRUCTURAL_ONLY
```

Root exports should be limited to the fail-closed builder, exception, non-authorization constants, and structural-schema warning.

### P2-2: Source Input Manifest Under-Binds Daily Continuous And Current-Contract Split

File:

```text
src/carver/spine/s27_v2_replay/source_rows.py
```

Finding:

```text
SOURCE_INPUT_MANIFEST_HAS_AMBIGUOUS_DAILY_ROW_HASH
```

GPT found that `SourceInputManifestRow` has one `daily_row_hash`, while the source-lock/provenance design requires distinguishing:

- daily continuous/back-adjusted equilibrium input;
- daily current-contract row;
- previous completed current-contract close used for the sigma-price bridge.

Why it matters:

```text
SIGMA_BRIDGE_AND_EQUILIBRIUM_LINEAGE_CAN_BE_HIDDEN_BY_SINGLE_DAILY_HASH
```

Minimal required correction queued:

```text
ADD_EXPLICIT_DAILY_CONTINUOUS_CURRENT_CONTRACT_AND_PREVIOUS_CLOSE_HASH_BINDINGS
```

The correction should replace or supplement `daily_row_hash` with explicit `daily_continuous_row_hash`, `daily_current_contract_row_hash`, and `previous_completed_current_contract_close_hash`, or add explicit cross-check fields tying the source manifest to `DailyHourlyLevelCompatibilityLedgerRow`.

## Gate Decision

GPT gate decision:

```text
PARSER_FILE_REPLAY_IMPLEMENTATION_PLANNING_MUST_REMAIN_BLOCKED
```

After the P1 zero-forecast/equilibrium correction and the two P2 hardening edits above, GPT states the project may proceed to the next separately authorized parser/file replay implementation planning step. That would still not authorize parser execution, file replay, result interpretation, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or PnL interpretation.

## Current Queue

The current next gate is a narrow GPT P2 external-audit finding patch if separately authorized by the operator.

Patch scope to request:

```text
S27_V2 replay scaffold GPT P2 external-audit finding patch only, covering zero mean-reversion/equilibrium flat branch, package-root trusted-bundle export hardening, and source input manifest daily continuous/current-contract/previous-close hash binding.
```

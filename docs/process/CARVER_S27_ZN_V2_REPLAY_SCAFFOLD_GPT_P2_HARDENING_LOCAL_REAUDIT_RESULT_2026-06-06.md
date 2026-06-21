# S27 ZN V2 Replay Scaffold GPT P2 Hardening Local Re-Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_HARDENING_LOCAL_REAUDIT_RESULT_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

The standing local hostile-audit pre-approval rule was applied to re-audit the narrow GPT P2 hardening patch recorded at:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_HARDENING_PATCH_RECORD_2026-06-06.md
```

This re-audit performed no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run.

## Re-Audit Scope

Patched files reviewed:

```text
src/carver/spine/s27_v2_replay/__init__.py
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/runner.py
src/carver/spine/s27_v2_replay/forecast.py
```

Audit questions:

- package-root public export hardening;
- structural-schema-only warning visibility;
- active/superseded evidence status label enforcement;
- unique active artifact type enforcement;
- complete required evidence artifact family enforcement;
- evidence manifest artifact hash binding to trust-root hashes;
- V/Q/M post-veto arithmetic binding.

## Static Inspection Result

Local static inspection found:

```text
NO_P0_FOUND
NO_P1_FOUND
NO_P2_FOUND
PUBLIC_EXPORT_REDUCED_TO_FAIL_CLOSED_BOUNDARY_CONFIRMED
STRUCTURAL_SCHEMA_ONLY_WARNING_CONFIRMED
ACTIVE_SUPERSEDED_EVIDENCE_STATUS_LABELS_CONFIRMED
REQUIRED_EVIDENCE_MANIFEST_FAMILIES_CONFIRMED
UNIQUE_ACTIVE_ARTIFACT_TYPE_GUARD_CONFIRMED
TRUST_ROOT_EVIDENCE_MANIFEST_HASH_CROSS_CHECK_CONFIRMED
VQM_POST_VETO_ARITHMETIC_BINDING_CONFIRMED
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

Package file count remained:

```text
19
```

## Subagent Hostile Audit Result

Subagent:

```text
Mill
```

Result:

```text
NO_P0_P1_P2_FINDINGS_FOUND_IN_NARROW_STATIC_SCOPE
```

Confirmed:

- package-root `__all__` exports only the fail-closed replay boundary plus the structural-schema-only warning label;
- low-level row dataclasses are not exported from package root;
- active entries must use `ACTIVE_EVIDENCE`;
- superseded artifacts must use `SUPERSEDED_EVIDENCE`;
- active artifact types must be unique;
- required artifact-family coverage is enforced;
- `TrustedReplayBundleScaffold.validate()` checks required evidence artifact hashes against corresponding trust-root hashes;
- `raw_volatility_multiplier_value` is bound to `2 - 1.5 * Q`;
- `risk_adjusted_after_veto_times_m_before_scalar_value` is bound to post-veto forecast times EWMA10 multiplier M;
- `capped_forecast_value` is bound to clamped post-veto-times-M times scalar.

## Residual Gates

This pass confirms only the static scaffold hardening. It does not prove source-faithful replay.

Remaining gates before any credible replay evidence:

- no manifest hashes have been recomputed from real files under an authorized parser/replay process;
- no parser or local-row replay construction has been exercised;
- no row-level ledgers have been emitted;
- no import/compile/test execution has been run under this authorization;
- submodule row dataclasses remain structural schemas only until a future trusted replay bundle emits them under the active trust root.

## Next Gate

The GPT P2 hardening patch is locally re-audited and has no remaining P0/P1/P2 finding in this narrow static scope.

Any external audit handoff, parser/file replay implementation, parser/file replay execution, diagnostics, tests/backtests, data access, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation still requires its own proper gate.

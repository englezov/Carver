# S27 ZN V2 Replay Scaffold GPT P2 Hardening Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_HARDENING_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffold GPT P2 hardening patch only, covering public-export structural-schema-only hardening, evidence-manifest required-family hardening, and V/Q/M post-veto arithmetic binding, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow scaffold hardening patch only. It authorizes and performed no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Source Finding

Local re-audit result that queued the residual P2 items:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_FAIL_CLOSED_SCHEMA_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

Residual P2 findings patched:

```text
P2_PUBLIC_EXPORT_STRUCTURAL_SCHEMA_ONLY_HARDENING
P2_EVIDENCE_MANIFEST_REQUIRED_FAMILY_HARDENING
P2_VQM_POST_VETO_ARITHMETIC_BINDING
```

## Patched Files

```text
src/carver/spine/s27_v2_replay/__init__.py
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/runner.py
src/carver/spine/s27_v2_replay/forecast.py
```

## Patch Summary

Public-export structural-schema-only hardening:

- Package-root exports are now limited to the fail-closed replay boundary, non-authorization constants, and the structural-schema-only warning label.
- Low-level row dataclasses are no longer exported from package root.
- The package docstring now states that submodule row dataclasses are structural schemas only and are not source-faithful evidence unless emitted by a future trusted replay bundle under the active trust root.

Evidence-manifest required-family hardening:

- Added active and superseded evidence status labels.
- Added required active evidence artifact families for all trust-root hash surfaces, including source lock, local data contract, provenance design, runner, parser/extractor source, runtime/dependency manifest, replay config, source universe, raw source files, row locator, canonical serialization policy components, session/roll/tick/cost policies, and daily/hourly compatibility policy.
- `EvidenceManifest` now rejects duplicate active artifact types and missing required artifact families.
- Active manifest entries must use `ACTIVE_EVIDENCE`.
- Superseded artifacts must use `SUPERSEDED_EVIDENCE`.
- `TrustedReplayBundleScaffold.validate()` now cross-checks each required evidence artifact hash against the corresponding trust-root hash.

V/Q/M post-veto arithmetic binding:

- `raw_volatility_multiplier_value` must equal `2 - 1.5 * Q`.
- `risk_adjusted_after_veto_times_m_before_scalar_value` must equal `risk_adjusted_forecast_after_veto_value * ewma10_multiplier_m_value`.
- `capped_forecast_value` must equal the clamped value of `risk_adjusted_after_veto_times_m_before_scalar_value * scalar_value`, with the existing `[-20, 20]` cap.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
PUBLIC_EXPORT_REDUCED_TO_FAIL_CLOSED_BOUNDARY_MARKERS_PRESENT
STRUCTURAL_SCHEMA_ONLY_WARNING_MARKERS_PRESENT
REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_FAMILY_MARKERS_PRESENT
TRUST_ROOT_EVIDENCE_MANIFEST_CROSS_CHECK_MARKERS_PRESENT
VQM_ARITHMETIC_BINDING_MARKERS_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

Package file count remained:

```text
19
```

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run under this authorization.

## Next Gate

The standing local hostile-audit pre-approval rule permits a local hostile re-audit of this narrow patch. Any external audit handoff, parser/file replay work, diagnostics, backtests, data access, Git actions, adapter work, deployment, trading, promotion, or result interpretation still requires its own proper gate.

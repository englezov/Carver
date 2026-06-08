# S27 ZN V2 Replay Scaffold GPT P2 External-Audit Finding Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_EXTERNAL_AUDIT_FINDING_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffold GPT P2 external-audit finding patch only, covering zero mean-reversion/equilibrium flat branch, package-root trusted-bundle export hardening, and source input manifest daily continuous/current-contract/previous-close hash binding, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow scaffold patch only. It authorizes and performed no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run.

## Source Finding

External GPT Extended Pro audit synthesis:

```text
docs/process/CARVER_S27_ZN_V2_GPT_P2_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

Findings patched:

```text
P1_ZERO_MEAN_REVERSION_EQUILIBRIUM_FLAT_BRANCH
P2_PACKAGE_ROOT_TRUSTED_BUNDLE_EXPORT_HARDENING
P2_SOURCE_INPUT_MANIFEST_DAILY_CONTINUOUS_CURRENT_CONTRACT_PREVIOUS_CLOSE_HASH_BINDING
```

## Patched Files

```text
src/carver/spine/s27_v2_replay/forecast.py
src/carver/spine/s27_v2_replay/__init__.py
src/carver/spine/s27_v2_replay/source_rows.py
```

## Patch Summary

Zero mean-reversion/equilibrium flat branch:

- `ForecastReplayLedgerRow` now permits an explicit `FLAT_AT_EQUILIBRIUM` decision when `risk_adjusted_forecast_before_veto_value` is zero.
- Zero EWMAC16/64 trend remains fail-closed through the existing nonzero trend-sign guard.
- The flat-at-equilibrium branch requires post-veto forecast, post-veto-times-M, capped forecast, desired unrounded position, and desired rounded position to remain zero.
- Nonzero mean-reversion cases remain constrained to either permitted mean reversion when signs agree or zeroed forecast when signs oppose.

Package-root trusted-bundle export hardening:

- Removed `TrustedReplayBundleScaffold` from package-root imports and `__all__`.
- Removed `S27_V2_TRUSTED_REPLAY_BUNDLE_STATUS` from package-root imports and `__all__`.
- Removed `S27_V2_REPLAY_PLANNING_READY_STATUS` from package-root imports and `__all__`.
- Package-root exports are now limited to the fail-closed builder, exception, non-authorization tuple, and structural-schema warning label.

Source input manifest lineage binding:

- Replaced the ambiguous `daily_row_hash` with explicit:
  - `daily_continuous_row_hash`;
  - `daily_current_contract_row_hash`;
  - `previous_completed_current_contract_close_hash`.
- These names align with `DailyHourlyLevelCompatibilityLedgerRow`, making the daily continuous/current-contract/sigma-bridge lineage explicit in the source input manifest scaffold.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
FLAT_AT_EQUILIBRIUM_DECISION_MARKERS_PRESENT
ZERO_MEAN_REVERSION_DOWNSTREAM_ZERO_GUARDS_PRESENT
ZERO_TREND_STILL_FAILS_CLOSED_MARKERS_PRESENT
TRUSTED_REPLAY_BUNDLE_SCAFFOLD_NOT_EXPORTED_FROM_PACKAGE_ROOT
TRUSTED_REPLAY_BUNDLE_STATUS_NOT_EXPORTED_FROM_PACKAGE_ROOT
SOURCE_INPUT_MANIFEST_DAILY_LINEAGE_HASHES_PRESENT
AMBIGUOUS_SOURCE_INPUT_MANIFEST_DAILY_ROW_HASH_REMOVED
```

No parser execution, file replay, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation were performed.

## Next Gate

The standing local hostile-audit pre-approval rule permits a local hostile re-audit of this narrow patch. Any external audit handoff, parser/file replay implementation planning, parser/file replay execution, diagnostics, tests/backtests, data access, Git actions, adapter work, deployment, trading, promotion, or result interpretation still requires its own proper gate.

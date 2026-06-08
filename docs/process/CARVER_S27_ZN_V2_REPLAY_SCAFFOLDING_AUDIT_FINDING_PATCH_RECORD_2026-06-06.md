# S27 ZN V2 Replay Scaffolding Audit Finding Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLDING_AUDIT_FINDING_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffolding audit-finding patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow patch to the schema/code scaffold only. It authorizes and performed no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Audit Findings Patched

Source audit result:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-06.md
```

Patched P1/P2 findings:

- Expanded `src/carver/spine/s27_v2_replay/forecast.py` to remove the opaque forecast-payload risk by requiring explicit EWMA5 equilibrium, raw mean-reversion forecast, sigma bridge, annual percentage sigma, sigma price, risk-adjusted forecast before veto, EWMAC16/64 trend, trend-veto decision, risk-adjusted forecast after veto, V, Q, raw volatility multiplier, EWMA10 M, post-veto-times-M-before-scalar, scalar value, cap, desired-unrounded-position, desired-rounded-position, and final forecast fields.
- Expanded `src/carver/spine/s27_v2_replay/source_universe.py` to require daily, hourly decision/fill, session, roll, and cost-parameter universe hashes, plus inclusion/exclusion reason-code, duplicate-policy, and canonical row-locator serialization hashes.
- Expanded `src/carver/spine/s27_v2_replay/level_compatibility.py` to require current-contract/hourly raw symbols and separate proof hashes for sigma bridge, hourly/current same-level compatibility, and bridged daily continuous equilibrium.
- Expanded `src/carver/spine/s27_v2_replay/costs.py` to require explicit multiplier, currency-conversion, and deflation-policy scaffolding fields where applicable.
- Expanded `src/carver/spine/s27_v2_replay/__init__.py` exports to include `RuntimeHistoryLedgerRow`, `CostLedgerRow`, `SpreadSpace`, and `TrustedReplayBundleScaffold`.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
ALL_EXPECTED_SCAFFOLD_FILES_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
PATCH_MARKERS_PRESENT_FOR_P1_P2_LOCAL_HOSTILE_AUDIT_FINDINGS
RUNNER_ENTRY_POINT_REMAINS_FAIL_CLOSED_WITH_ReplayExecutionBlocked
```

The scan looked only at text and file inventory. Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run under this authorization.

## Remaining Gate

The next step is a local hostile re-audit of the patched scaffold if the operator authorizes it. That audit may inspect the patch and process artifacts, but it must not run parser/file replay, diagnostics, backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation unless separately authorized.

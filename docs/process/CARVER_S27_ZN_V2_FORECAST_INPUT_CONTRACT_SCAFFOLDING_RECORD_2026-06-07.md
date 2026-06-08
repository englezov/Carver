# S27 ZN V2 Forecast Input Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_FORECAST_INPUT_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after runtime_history_input_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the runtime history input contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only forecast input gate between future runtime-history inputs/states and any later forecast construction.

It locks that future parser/file replay metadata must prove:

- complete required forecast input coverage;
- each forecast input maps to the locked source kind: runtime input, runtime state, V/Q/M component, or source policy;
- each forecast input is bound to a source contract hash and forecast input policy hash;
- each forecast component maps to the exact required prior forecast inputs or prior component outputs;
- each forecast decision branch maps to the exact required prior component outputs;
- each forecast invariant maps to the exact required prior inputs, components, or branch outputs;
- dependency hashes match the supplied input, component, or branch dependency contract hashes before future forecast construction can proceed.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/forecast_input_contract.py
```

The module defines:

```text
S27_V2_FORECAST_INPUT_CONTRACT_ONLY_STATUS
PLANNED_FORECAST_INPUT_STATUS
FORECAST_INPUT_SOURCE_KINDS
REQUIRED_FORECAST_INPUTS
REQUIRED_SOURCE_KIND_BY_FORECAST_INPUT
REQUIRED_RUNTIME_HISTORY_INPUT_BY_FORECAST_INPUT
REQUIRED_RUNTIME_STATE_BY_FORECAST_INPUT
REQUIRED_VQM_COMPONENT_BY_FORECAST_INPUT
REQUIRED_POLICY_LABEL_BY_FORECAST_INPUT
REQUIRED_FORECAST_DEPENDENCIES_BY_COMPONENT
REQUIRED_FORECAST_DEPENDENCIES_BY_DECISION_BRANCH
REQUIRED_FORECAST_DEPENDENCIES_BY_INVARIANT
ForecastInputFieldContract
ForecastDependencyBindingContract
ForecastInputContractBundle
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, compute EWMA5, compute EWMAC16/64, compute sigma, compute V/Q/M, compute forecasts, construct forecast rows, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/forecast_input_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/forecast_input_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "forecast_input|ForecastInput"
rg -n "ForecastInput|S27_V2_FORECAST_INPUT|REQUIRED_FORECAST_INPUT" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
FORECAST_INPUT_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

No next gate is opened by this scaffolding record.

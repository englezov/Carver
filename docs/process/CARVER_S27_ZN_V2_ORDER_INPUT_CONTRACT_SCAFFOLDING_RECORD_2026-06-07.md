# S27 ZN V2 Order Input Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_ORDER_INPUT_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after position_input_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the position input contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only order input gate between future desired-position construction and any later order-plan construction.

It locks that future parser/file replay metadata must prove:

- complete required order input coverage;
- each order input maps to the locked source kind: position ledger output, position component, order kind, order transition kind, working-order state context, or source policy;
- each order input is bound to a source contract hash and order input policy hash;
- each order component maps to the exact required prior order inputs or prior component outputs;
- each order invariant maps to the exact required prior order inputs or component outputs;
- dependency hashes match the supplied input or component dependency contract hashes before future order-plan construction can proceed;
- no order rows, limit prices, tick rounding execution, working-order state transitions, or fills are opened by order input scaffolding.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/order_input_contract.py
```

The module defines:

```text
S27_V2_ORDER_INPUT_CONTRACT_ONLY_STATUS
PLANNED_ORDER_INPUT_STATUS
ORDER_INPUT_SOURCE_KINDS
REQUIRED_ORDER_INPUTS
REQUIRED_SOURCE_KIND_BY_ORDER_INPUT
REQUIRED_POSITION_COMPONENT_BY_ORDER_INPUT
REQUIRED_POSITION_LEDGER_OUTPUT_BY_ORDER_INPUT
REQUIRED_ORDER_KIND_BY_ORDER_INPUT
REQUIRED_ORDER_TRANSITION_KIND_BY_ORDER_INPUT
REQUIRED_ORDER_STATE_CONTEXT_BY_ORDER_INPUT
REQUIRED_POLICY_LABEL_BY_ORDER_INPUT
REQUIRED_ORDER_DEPENDENCIES_BY_COMPONENT
REQUIRED_ORDER_DEPENDENCIES_BY_INVARIANT
OrderInputFieldContract
OrderDependencyBindingContract
OrderInputContractBundle
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, compute forecasts, compute desired positions, apply rounding, generate orders, price limit orders, update working-order state, execute fills, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/order_input_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/order_input_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "order_input|OrderInput"
rg -n "OrderInput|S27_V2_ORDER_INPUT|REQUIRED_ORDER_INPUT" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
ORDER_INPUT_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

No next gate is opened by this scaffolding record.

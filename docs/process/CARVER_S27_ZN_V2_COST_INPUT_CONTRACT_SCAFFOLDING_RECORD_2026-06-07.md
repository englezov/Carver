# S27 ZN V2 Cost Input Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_COST_INPUT_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after fill_input_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the fill input contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only cost input gate between future fill-ledger construction and any later cost-ledger construction.

It locks that future parser/file replay metadata must prove:

- complete required cost input coverage;
- each cost input maps to the locked source kind: fill ledger output, cost branch, spread space, source policy, multiplier proof, or currency proof;
- each cost input is bound to a source contract hash and cost input policy hash;
- each cost component maps to the exact required prior cost inputs or prior component outputs;
- each cost invariant maps to the exact required prior cost inputs or component outputs;
- dependency hashes match the supplied input or component dependency contract hashes before future cost construction can proceed;
- no commission amount, spread amount, total cost, PnL, or replay arithmetic is opened by cost input scaffolding.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/cost_input_contract.py
```

The module defines:

```text
S27_V2_COST_INPUT_CONTRACT_ONLY_STATUS
PLANNED_COST_INPUT_STATUS
COST_INPUT_SOURCE_KINDS
REQUIRED_COST_INPUTS
REQUIRED_SOURCE_KIND_BY_COST_INPUT
REQUIRED_FILL_LEDGER_OUTPUT_BY_COST_INPUT
REQUIRED_COST_BRANCH_BY_COST_INPUT
REQUIRED_SPREAD_SPACE_BY_COST_INPUT
REQUIRED_POLICY_LABEL_BY_COST_INPUT
REQUIRED_MULTIPLIER_PROOF_BY_COST_INPUT
REQUIRED_CURRENCY_PROOF_BY_COST_INPUT
REQUIRED_COST_DEPENDENCIES_BY_COMPONENT
REQUIRED_COST_DEPENDENCIES_BY_INVARIANT
CostInputFieldContract
CostDependencyBindingContract
CostInputContractBundle
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, compute forecasts, compute desired positions, generate orders, create fill rows, compute fill prices, compute commission, compute spread cost, compute total cost, compute PnL, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/cost_input_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/cost_input_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "cost_input|CostInput"
rg -n "CostInput|S27_V2_COST_INPUT|REQUIRED_COST_INPUT" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
COST_INPUT_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

No next gate is opened by this scaffolding record.

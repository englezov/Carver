# S27 ZN V2 Fill Input Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_FILL_INPUT_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after order_input_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the order input contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only fill input gate between future order-plan/transition construction and any later fill-ledger construction.

It locks that future parser/file replay metadata must prove:

- complete required fill input coverage;
- each fill input maps to the locked source kind: order ledger output, working-order transition output, source-row proof, fill-price provenance, fill branch, or source policy;
- each fill input is bound to a source contract hash and fill input policy hash;
- each fill component maps to the exact required prior fill inputs or prior component outputs;
- each fill invariant maps to the exact required prior fill inputs or component outputs;
- dependency hashes match the supplied input or component dependency contract hashes before future fill construction can proceed;
- no fill rows, fill prices, source-row selection, cost accounting, PnL, or replay execution are opened by fill input scaffolding.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/fill_input_contract.py
```

The module defines:

```text
S27_V2_FILL_INPUT_CONTRACT_ONLY_STATUS
PLANNED_FILL_INPUT_STATUS
FILL_INPUT_SOURCE_KINDS
REQUIRED_FILL_INPUTS
REQUIRED_SOURCE_KIND_BY_FILL_INPUT
REQUIRED_ORDER_LEDGER_OUTPUT_BY_FILL_INPUT
REQUIRED_WORKING_ORDER_TRANSITION_OUTPUT_BY_FILL_INPUT
REQUIRED_SOURCE_ROW_PROOF_BY_FILL_INPUT
REQUIRED_FILL_PRICE_PROVENANCE_BY_FILL_INPUT
REQUIRED_FILL_BRANCH_BY_FILL_INPUT
REQUIRED_POLICY_LABEL_BY_FILL_INPUT
REQUIRED_FILL_DEPENDENCIES_BY_COMPONENT
REQUIRED_FILL_DEPENDENCIES_BY_INVARIANT
FillInputFieldContract
FillDependencyBindingContract
FillInputContractBundle
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, compute forecasts, compute desired positions, generate orders, price limit orders, apply tick rounding, advance working-order state, select next completed hourly rows, create fill rows, compute fill prices, compute costs/PnL, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/fill_input_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/fill_input_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "fill_input|FillInput"
rg -n "FillInput|S27_V2_FILL_INPUT|REQUIRED_FILL_INPUT" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
FILL_INPUT_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The static/read-only local hostile audit was completed and recorded in:

```text
docs/process/CARVER_S27_ZN_V2_FILL_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS` with no P0/P1/P2/P3 findings.

The next possible implementation slice still requires separate explicit operator authorization.

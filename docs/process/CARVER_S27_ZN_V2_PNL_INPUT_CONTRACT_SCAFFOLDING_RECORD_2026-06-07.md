# S27 ZN V2 PnL Input Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_PNL_INPUT_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after cost_input_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the cost input contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only PnL input gate between future cost-ledger construction and any later PnL-ledger construction.

It locks that future parser/file replay metadata must prove:

- complete required PnL input coverage;
- each PnL input maps to the locked source kind: trust-root output, source-universe output, transition ledger output, position source output, close-only price source, price-row proof, bridge proof, fill/cost hash-set output, multiplier proof, currency proof, or source policy;
- each PnL input is bound to a source contract hash and PnL input policy hash;
- each PnL component maps to the exact required prior PnL inputs or prior component outputs;
- each PnL invariant maps to the exact required prior PnL inputs or component outputs;
- dependency hashes match the supplied input or component dependency contract hashes before future PnL construction can proceed;
- no price selection, PnL amount, currency conversion, cost application, result interpretation, or replay arithmetic is opened by PnL input scaffolding.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/pnl_input_contract.py
```

The module defines:

```text
S27_V2_PNL_INPUT_CONTRACT_ONLY_STATUS
PLANNED_PNL_INPUT_STATUS
PNL_INPUT_SOURCE_KINDS
REQUIRED_PNL_INPUTS
REQUIRED_SOURCE_KIND_BY_PNL_INPUT
REQUIRED_TRUST_ROOT_OUTPUT_BY_PNL_INPUT
REQUIRED_SOURCE_UNIVERSE_OUTPUT_BY_PNL_INPUT
REQUIRED_TRANSITION_LEDGER_OUTPUT_BY_PNL_INPUT
REQUIRED_POSITION_SOURCE_OUTPUT_BY_PNL_INPUT
REQUIRED_PRICE_SOURCE_BY_PNL_INPUT
REQUIRED_PRICE_ROW_PROOF_BY_PNL_INPUT
REQUIRED_BRIDGE_PROOF_BY_PNL_INPUT
REQUIRED_FILL_HASH_SET_OUTPUT_BY_PNL_INPUT
REQUIRED_COST_HASH_SET_OUTPUT_BY_PNL_INPUT
REQUIRED_MULTIPLIER_PROOF_BY_PNL_INPUT
REQUIRED_CURRENCY_PROOF_BY_PNL_INPUT
REQUIRED_POLICY_LABEL_BY_PNL_INPUT
REQUIRED_PNL_DEPENDENCIES_BY_COMPONENT
REQUIRED_PNL_DEPENDENCIES_BY_INVARIANT
PnlInputFieldContract
PnlDependencyBindingContract
PnlInputContractBundle
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, compute forecasts, compute desired positions, generate orders, create fill rows, compute costs, select prices, compute PnL, interpret results, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/pnl_input_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/pnl_input_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "pnl_input|PnlInput"
rg -n "PnlInput|S27_V2_PNL_INPUT|REQUIRED_PNL_INPUT" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
PNL_INPUT_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

No next gate is opened by this scaffolding record.

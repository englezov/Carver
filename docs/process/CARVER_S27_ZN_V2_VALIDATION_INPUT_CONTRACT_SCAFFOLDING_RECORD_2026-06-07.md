# S27 ZN V2 Validation Input Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_VALIDATION_INPUT_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after pnl_input_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the PnL input contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only validation input gate between future PnL-ledger construction and any later validation/provenance ledger construction.

It locks that future parser/file replay metadata must prove:

- complete required validation input coverage;
- each validation input maps to the locked source kind: trust-root output, active evidence manifest output, source-input manifest output, PnL contract output, PnL input contract output, validation/provenance/local-audit schema output, unresolved gate set, or source policy;
- the unresolved gate input binds the complete locked unresolved gate tuple;
- each validation component maps to exact required prior validation inputs or prior component outputs;
- each validation ledger maps to exact required prior validation components;
- each audit checkpoint maps to exact required prior validation inputs, components, or ledger packet policies;
- each validation invariant maps to exact required prior validation inputs, components, or ledgers;
- dependency hashes match supplied input/component/ledger/audit-checkpoint dependency contract hashes before future validation construction can proceed;
- no validation ledger construction, provenance construction, local audit execution, external packet preparation, parser/file replay, result interpretation, or source-faithful evidence claim is opened by validation input scaffolding.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/validation_input_contract.py
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, compute forecasts, compute desired positions, generate orders, create fill rows, compute costs, compute PnL, construct validation ledgers, construct provenance ledgers, run local hostile audits, prepare external audit packets, interpret results, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/validation_input_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/validation_input_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "validation_input|ValidationInput"
rg -n "S27_V2_VALIDATION_INPUT|REQUIRED_VALIDATION_INPUT|ValidationInput" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
VALIDATION_INPUT_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

No next gate is opened by this scaffolding record.

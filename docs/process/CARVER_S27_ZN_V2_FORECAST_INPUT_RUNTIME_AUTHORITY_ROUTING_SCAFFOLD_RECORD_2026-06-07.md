# S27_V2 Forecast-Input Runtime Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_FORECAST_INPUT_RUNTIME_AUTHORITY_ROUTING_SCAFFOLD_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator authorized a consolidated S27_V2 parser/file replay scaffold-routing loop, limited to inert authority-routing and contract-binding scaffolds after active-trust routing external `PASS`.

This record covers only the forecast-input/runtime-history authority-routing slice inside that consolidated gate.

## Scope

Patched file:

```text
src/carver/spine/s27_v2_replay/forecast_input_contract.py
```

Upstream authority dependencies:

```text
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
src/carver/spine/s27_v2_replay/runtime_history_contract.py
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
src/carver/spine/s27_v2_replay/source_row_batch_contract.py
src/carver/spine/s27_v2_replay/parser_output_contract.py
```

## Change Summary

`ForecastInputContractBundle.validate()` now fails closed. Forecast input validation requires the routed `validate_against_runtime_history_authority(...)` path.

That routed path requires active trust inputs for validating `RuntimeHistoryInputContractBundle`:

```text
ReplayTrustRoot
EvidenceManifest
SourceRowSelectionExternalAuthorityHandle
SourceRowBatchSetContract
ParserOutputBatchSetContract
RuntimeHistoryInputContractBundle
RuntimeHistoryContractBundle
```

The forecast expected-source map is no longer accepted against coarse runtime-history input or runtime-history bundle hashes. Forecast inputs now derive source authority as follows:

- runtime input sources derive from locked `RuntimeHistoryInputFieldContract.input_field_contract_hash` values;
- runtime state sources derive from locked `RuntimeStateFamilyContract.state_contract_hash` values;
- V/Q/M sources derive from locked `VqmComponentContract.component_contract_hash` values;
- forecast policy inputs remain bound to the forecast input policy hash.

The patch also binds the cited runtime-history input contract hash, runtime-history contract bundle hash, source-input manifest contract hash, and runtime-history source manifest hash before forecast input source maps can be accepted.

## Guardrail

This scaffold remains inert. It introduces no forecast computation, parser/file replay execution path, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop to verify:

- forecast input no longer self-authenticates runtime-history authority with coarse top-level hashes;
- runtime-history input is validated through active trust before forecast consumes its input-field contracts;
- runtime state and V/Q/M authority is derived from validated runtime-history contract objects;
- no execution surface or forbidden stage transition was introduced.

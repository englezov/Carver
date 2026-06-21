# S27_V2 Position-Input Forecast Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_POSITION_INPUT_FORECAST_AUTHORITY_ROUTING_SCAFFOLD_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator authorized a consolidated S27_V2 parser/file replay scaffold-routing loop, limited to inert authority-routing and contract-binding scaffolds after active-trust routing external `PASS`.

This record covers only the position-input/forecast authority-routing slice inside that consolidated gate.

## Scope

Patched file:

```text
src/carver/spine/s27_v2_replay/position_input_contract.py
```

Upstream authority dependencies:

```text
src/carver/spine/s27_v2_replay/forecast_input_contract.py
src/carver/spine/s27_v2_replay/forecast_contract.py
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
src/carver/spine/s27_v2_replay/runtime_history_contract.py
```

## Change Summary

`PositionInputContractBundle.validate()` now fails closed. Position input validation requires the routed `validate_against_forecast_authority(...)` path.

That routed path validates `ForecastInputContractBundle` through its runtime-history authority route before consuming forecast authority, and separately validates `ForecastContractBundle`.

Position input expected-source authority is now derived as follows:

- forecast component inputs derive from locked `ForecastComponentContract.component_contract_hash` values;
- forecast ledger output input binds to the validated `ForecastContractBundle.forecast_contract_bundle_hash`;
- rounding policy, position state context, and local policy inputs remain bound to the position input policy hash.

The patch binds the cited forecast input contract hash, forecast contract bundle hash, source-input manifest contract hash, and forecast/runtime-history authority relationship before position input source maps can be accepted.

## Ledger-Output Note

This scaffold does not yet define a separate forecast ledger-row output authority object. Until that future object exists under a separate authorized scaffold, the single forecast ledger-output input is bound to the validated forecast contract bundle rather than to caller-supplied or self-derived expected maps.

## Guardrail

This scaffold remains inert. It introduces no desired-position computation, order generation, parser/file replay execution path, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop to verify:

- position input no longer self-authenticates forecast authority with coarse top-level forecast hashes;
- forecast input is validated through the runtime-history authority route before position consumes forecast input/contract authority;
- forecast component authority is derived from validated forecast component contracts;
- forecast ledger output is at least bound to the validated forecast contract bundle and not a caller-supplied expected map;
- no execution surface or forbidden stage transition was introduced.

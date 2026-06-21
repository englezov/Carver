# S27_V2 Validation And Trusted-Output Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_VALIDATION_TRUSTED_OUTPUT_AUTHORITY_ROUTING_SCAFFOLD_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator authorized a consolidated S27_V2 parser/file replay scaffold-routing loop, limited to inert authority-routing and contract-binding scaffolds after active-trust routing external `PASS`.

This record covers only the validation-input/PnL and final trusted-bundle/validation authority-routing slice inside that consolidated gate.

## Scope

Patched files:

```text
src/carver/spine/s27_v2_replay/validation_input_contract.py
src/carver/spine/s27_v2_replay/trusted_bundle_contract.py
```

Upstream authority dependencies:

```text
src/carver/spine/s27_v2_replay/pnl_input_contract.py
src/carver/spine/s27_v2_replay/pnl_contract.py
src/carver/spine/s27_v2_replay/validation_contract.py
src/carver/spine/s27_v2_replay/construction_contract.py
src/carver/spine/s27_v2_replay/trust_root.py
src/carver/spine/s27_v2_replay/evidence_manifest.py
```

## Change Summary

`ValidationInputContractBundle.validate()` now fails closed. Validation input validation requires the routed `validate_against_pnl_authority(...)` path.

That routed path validates `PnlInputContractBundle` through its cost/fill/order/source-row authority route before consuming PnL authority, and separately validates `PnlContractBundle`.

Validation input expected-source authority is now derived as follows:

- trust-root input binds to the routed `ReplayTrustRoot.replay_trust_root_hash`;
- active evidence-manifest input binds to the routed `EvidenceManifest.active_evidence_manifest_hash`;
- source-input manifest input binds to the routed `SourceInputManifestContractBundle.source_input_manifest_hash`;
- PnL contract input binds to the validated `PnlContractBundle.pnl_contract_bundle_hash`;
- PnL input contract input binds to the validated `PnlInputContractBundle.pnl_input_contract_hash`;
- validation/provenance/local-audit schema inputs bind to local validation-input schema fields;
- policy and unresolved-gate inputs bind to the validation-input policy hash.

`TrustedBundleContractBundle.validate()` now fails closed. Trusted-bundle validation requires the routed `validate_against_validation_authority(...)` path.

That routed path validates the construction contract, validates validation input through routed PnL authority, and validates the validation contract before accepting trusted-bundle expected-source maps.

Trusted-bundle expected-source authority is now derived as follows:

- trust-root input binds to the routed `ReplayTrustRoot.replay_trust_root_hash`;
- active evidence-manifest input binds to the routed `EvidenceManifest.active_evidence_manifest_hash`;
- construction input binds to the validated `ParserFileReplayConstructionContract.construction_contract_hash`;
- validation input binds to the validated `ValidationInputContractBundle.validation_input_contract_hash`;
- validation contract input binds to the validated `ValidationContractBundle.validation_contract_bundle_hash`;
- validation/provenance/local-audit ledger output inputs bind to local trusted-bundle fields;
- bundle status and final public-boundary policy inputs bind to the trusted-bundle policy hash.

Both patched bundles compare their explicit top-level authority fields to those routed active authority values before expected-source maps or field contracts can be accepted.

## Ledger-Output Boundary Notes

This scaffold does not emit validation ledgers, provenance/hash ledgers, or local hostile-audit result ledgers. Those output hashes remain trusted-bundle local scaffold fields until future authorized ledger-output authority objects exist.

This is an inert routing scaffold only. It is not source-faithful replay evidence and does not claim that any validation, provenance, audit, parser, file replay, or PnL ledger has been produced.

## Guardrail

This scaffold remains inert. It introduces no validation-ledger construction, no trusted-bundle assembly execution, no price selection, no transition replay, no PnL computation, no ledger construction, no result interpretation, no parser/file replay execution path, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, or source-faithful replay evidence claim.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop to verify:

- validation input no longer accepts PnL/trust authority solely from caller-supplied or self fields;
- trusted bundle no longer accepts construction/validation/trust authority solely from caller-supplied or self fields;
- routed PnL input, PnL contract, validation input, validation contract, construction contract, trust root, and evidence-manifest values are consumed before expected-source maps are accepted;
- validation/provenance/local-audit ledger-output boundary notes are accurate and do not claim source-faithful replay evidence;
- no execution surface or forbidden stage transition was introduced.

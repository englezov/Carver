# S27 ZN V2 Contract/Input Chain GPT Fail Hardening Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_GPT_FAIL_HARDENING_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Trigger

GPT Extended Pro returned `FAIL` for the S27 V2 contract/input chain handoff packet. The audit found no P0 issue, but found P1/P2/P3 blockers before the scaffold could safely advance to parser/file replay implementation.

This patch responds only to those external-audit blockers. It does not execute parser work, replay, diagnostics, tests, backtests, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, or result interpretation.

## Patched Scope

### Forecast Sigma Bridge

Patched:

```text
src/carver/spine/s27_v2_replay/forecast_contract.py
src/carver/spine/s27_v2_replay/forecast_input_contract.py
```

Changes:

- added explicit forecast input for previous completed current-contract close;
- separated raw mean-reversion forecast from risk-adjusted pre-trend-veto forecast;
- made `SIGMA_PRICE_BRIDGE` depend on previous completed current-contract close plus sigma state instead of hourly decision price;
- routed trend-veto decision branches through the risk-adjusted pre-veto forecast.

### V/Q/M Runtime History Binding

Patched:

```text
src/carver/spine/s27_v2_replay/runtime_history_contract.py
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
```

Changes:

- added explicit runtime state families for ten-year rolling mean percentage sigma, expanding relative-volatility distribution, and prior EWMA10 multiplier state;
- bound V/Q/M component dependencies to those granular states;
- preserved planned-only/no-computation status.

### Source-Authority Hash Binding

Patched:

```text
src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
src/carver/spine/s27_v2_replay/forecast_input_contract.py
src/carver/spine/s27_v2_replay/position_input_contract.py
src/carver/spine/s27_v2_replay/order_input_contract.py
src/carver/spine/s27_v2_replay/fill_input_contract.py
src/carver/spine/s27_v2_replay/cost_input_contract.py
src/carver/spine/s27_v2_replay/pnl_input_contract.py
src/carver/spine/s27_v2_replay/validation_input_contract.py
src/carver/spine/s27_v2_replay/trusted_bundle_contract.py
```

Changes:

- added expected-source hash maps to input bundles;
- required those maps to exactly match locked input label tuples;
- required each observed field-level source hash to equal the active expected hash for that input label.

### Construction Artifact Coverage

Patched:

```text
src/carver/spine/s27_v2_replay/construction_contract.py
```

Changes:

- locked construction output artifact families to `ARTIFACT_FAMILIES`;
- required schema-family labels to match the locked artifact-family schema labels;
- required planned construction phases to emit the expected artifact families;
- replaced set-only unresolved-gate coverage with tuple/count/order coverage so duplicates and omissions cannot hide.

### Controlled Fail-Closed Error Taxonomy

Patched:

```text
src/carver/spine/s27_v2_replay/validation.py
src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
src/carver/spine/s27_v2_replay/forecast_input_contract.py
src/carver/spine/s27_v2_replay/position_input_contract.py
src/carver/spine/s27_v2_replay/order_input_contract.py
src/carver/spine/s27_v2_replay/fill_input_contract.py
src/carver/spine/s27_v2_replay/cost_input_contract.py
src/carver/spine/s27_v2_replay/pnl_input_contract.py
src/carver/spine/s27_v2_replay/validation_input_contract.py
src/carver/spine/s27_v2_replay/trusted_bundle_contract.py
```

Changes:

- added shared `CarverBlocked` helpers for hash maps, expected hashes, and dependency hash matching;
- replaced direct missing-label dependency indexing with controlled fail-closed validation.

## Packet-Composition Finding

GPT P1-001 was partly a handoff-packet completeness finding. The next GPT re-audit packet must include package-root, trust-root, evidence-manifest, and imported base contract files needed to audit public boundary and active authority.

## Static Check

A static source scan after the patch found no remaining direct dependency lookup reads matching:

```text
dependency_hash_by_label[
input_contract_hash_by_label[
```

Remaining matches are dictionary assignments that populate label-to-hash maps before controlled helper validation.

## Non-Authorization

This patch record authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.

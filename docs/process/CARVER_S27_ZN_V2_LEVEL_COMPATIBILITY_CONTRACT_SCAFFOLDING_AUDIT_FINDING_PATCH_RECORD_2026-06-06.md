# S27 ZN V2 Level Compatibility Contract Scaffolding Audit Finding Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_AUDIT_FINDING_PATCH_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Patch Scope

Patch source:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

Patched file:

```text
src/carver/spine/s27_v2_replay/level_compatibility_contract.py
```

## Finding Patched

P2:

```text
VERDICT_PROOF_HASHES_NOT_BOUND_TO_SUPPLIED_PROOF_CONTRACTS
```

## Patch

`LevelCompatibilityContractBundle.validate()` now requires:

```text
self.verdict_contract.required_proof_contract_hashes == tuple(proof.proof_contract_hash for proof in self.proof_contracts)
```

If the verdict proof hashes do not exactly match the supplied proof contracts in locked order, validation raises:

```text
CarverBlocked
```

## Preserved Boundaries

The patch does not:

- open files;
- read files;
- enumerate paths;
- parse rows;
- execute parser work;
- execute file replay;
- compare daily/hourly price levels;
- compute bridge arithmetic;
- run diagnostics;
- run tests/backtests;
- call providers/APIs;
- download data;
- access OOS, Lockbox, or Forward;
- perform Git actions;
- perform adapter work;
- deploy, trade, promote, or interpret results.

Package-root exports were not widened.

## Next Gate

The next gate is local hostile re-audit of this narrow P2 patch, static/source-only.

## Non-Authorizations

This patch record does not authorize:

- provider/API calls;
- downloads;
- credential use;
- parser execution;
- file replay;
- diagnostics;
- tests;
- backtests;
- OOS access;
- Lockbox access;
- Forward access;
- Git staging;
- Git commits;
- Git pushes;
- PRs;
- adapter work;
- deployment;
- trading;
- promotion;
- tuning after results;
- result interpretation;
- source-faithful replay evidence claims.

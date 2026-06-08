# S27 ZN V2 Validation Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_VALIDATION_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow implementation slice scaffolding only, after pnl_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only a narrow inert validation/provenance contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior PnL contract scaffold local audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PNL_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

That audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/validation_contract.py
```

The module defines:

```text
S27_V2_VALIDATION_CONTRACT_ONLY_STATUS
PLANNED_VALIDATION_COMPONENT_STATUS
REQUIRED_VALIDATION_COMPONENT_FAMILIES
REQUIRED_VALIDATION_LEDGER_LABELS
REQUIRED_VALIDATION_AUDIT_CHECKPOINT_LABELS
REQUIRED_VALIDATION_INVARIANTS
ValidationSourceBinding
ValidationComponentContract
ValidationLedgerContract
ValidationAuditCheckpointContract
ValidationInvariantContract
ValidationContractBundle
```

## Purpose

This slice introduces a structural contract for future validation/provenance ledgers and audit checkpoints without running validation, constructing provenance, executing parser/file replay, or claiming source-faithful replay evidence.

It locks required validation component families to:

```text
TRUST_ROOT_REFERENCE
EVIDENCE_MANIFEST_REFERENCE
REQUIRED_LEDGER_FAMILY_COVERAGE
PROVENANCE_HASH_CHAIN
FAIL_CLOSED_GATE_STATUS
LOCAL_HOSTILE_AUDIT_PACKET
SUPERSESSION_MANIFEST
NON_AUTHORIZATION_PRESERVATION
```

It locks required validation ledger labels to:

```text
VALIDATION_LEDGER
PROVENANCE_AND_HASH_LEDGER
LOCAL_HOSTILE_AUDIT_RESULT
```

It locks required validation audit checkpoint labels to:

```text
SCHEMA_AND_TRUST_ROOT_CODE
FAIL_CLOSED_ROW_PATHS
DAILY_HOURLY_LEVEL_COMPATIBILITY_AND_SIGMA_BRIDGE
FORECAST_ARITHMETIC_AND_GATES
ORDER_FILL_COST_PNL_PROVENANCE
EXTERNAL_AUDIT_PACKET_AFTER_ARTIFACTS_EXIST
```

It locks required validation invariant proof labels to:

```text
ACTIVE_EVIDENCE_MANIFEST_HASH_BINDING
REQUIRED_ARTIFACT_FAMILY_COVERAGE
TRUST_ROOT_EVIDENCE_MANIFEST_CROSS_CHECK
VALIDATION_LEDGER_HASH_BINDING
PROVENANCE_AND_HASH_LEDGER_BINDING
LOCAL_HOSTILE_AUDIT_RESULT_BINDING
STALE_EVIDENCE_SUPERSESSION_BINDING
FAIL_CLOSED_UNRESOLVED_GATES_BINDING
NO_PARSER_REPLAY_EXECUTION_IN_VALIDATION_CONTRACT
NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM_IN_VALIDATION_CONTRACT
```

The scaffolding validates only supplied metadata:

- replay trust-root hash;
- active evidence manifest hash;
- source input manifest hash;
- PnL contract bundle hash;
- validation ledger schema hash;
- provenance and hash ledger schema hash;
- local hostile audit result schema hash;
- validation source binding hash;
- validation component input, definition, policy, planned-output, and contract hashes;
- validation ledger input, schema, policy, planned-output, and contract hashes;
- audit checkpoint policy, planned-scope, and contract hashes;
- invariant proof, policy, and contract hashes;
- required artifact family policy hash;
- provenance hash-chain policy hash;
- fail-closed gate policy hash;
- stale evidence supersession policy hash;
- local hostile audit policy hash;
- external audit packet policy hash;
- validation contract bundle hash;
- non-authorization tuple.

## Preserved Boundaries

The module does not:

- open files;
- read files;
- enumerate paths;
- glob directories;
- parse CSV/PDF/JSON;
- execute parser work;
- execute file replay;
- construct source rows;
- construct validation ledgers;
- construct provenance ledgers;
- run local hostile audits;
- prepare external audit packets;
- compute PnL;
- compute returns;
- compute result metrics;
- run diagnostics;
- run tests/backtests;
- call providers/APIs;
- download data;
- start subprocesses;
- invoke Git;
- access OOS, Lockbox, or Forward;
- perform adapter work;
- deploy, trade, promote, or interpret results;
- claim source-faithful replay evidence.

Package-root exports were intentionally not widened. The package root still exposes only the fail-closed runner boundary and non-authorization/status warning constants.

## Next Gate

The next gate is a local hostile audit of this narrow validation/provenance contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to this narrow validation/provenance contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_VALIDATION_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned:

```text
PASS
```

Findings:

```text
P0: NONE
P1: NONE
P2: NONE
P3: NONE
```

The next possible implementation slice requires separate explicit operator authorization.

## Static Text-Only Verification

Static text-only verification performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Package file count after this slice:

```text
36
```

Forbidden-surface scan:

```text
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest" src\carver\spine\s27_v2_replay
```

Result:

```text
NO_MATCHES
```

Package-root export check:

```text
NO_VALIDATION_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
```

No import, compile, test, parser execution, file replay, diagnostics, provider/API call, download, OOS, Lockbox, Forward, Git action, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim was performed.

## Non-Authorizations

This record does not authorize:

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

Any transition beyond this scaffolding slice requires separate explicit operator authorization.

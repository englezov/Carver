# S27 ZN V2 Replay Schema Code Scaffolding Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCHEMA_CODE_SCAFFOLDING_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay schema/code scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only schema/code scaffolding. It authorizes no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no provider/API calls, no downloads, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Scope

New isolated package:

```text
src/carver/spine/s27_v2_replay/
```

This package is separate from:

```text
src/carver/spine/s27_v2.py
```

The existing synthetic/audited `s27_v2.py` primitive surface was not modified by this scaffolding step.

## Created Scaffolding Files

```text
src/carver/spine/s27_v2_replay/__init__.py
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/validation.py
src/carver/spine/s27_v2_replay/identity.py
src/carver/spine/s27_v2_replay/canonical_hash.py
src/carver/spine/s27_v2_replay/trust_root.py
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/source_universe.py
src/carver/spine/s27_v2_replay/source_rows.py
src/carver/spine/s27_v2_replay/level_compatibility.py
src/carver/spine/s27_v2_replay/runtime_history.py
src/carver/spine/s27_v2_replay/forecast.py
src/carver/spine/s27_v2_replay/position.py
src/carver/spine/s27_v2_replay/orders.py
src/carver/spine/s27_v2_replay/transitions.py
src/carver/spine/s27_v2_replay/fills.py
src/carver/spine/s27_v2_replay/costs.py
src/carver/spine/s27_v2_replay/pnl.py
src/carver/spine/s27_v2_replay/runner.py
```

## Boundary Design

The package defines schema-only structures for:

- replay identity;
- canonical serialization policy;
- hash references and hashed artifacts;
- replay trust root;
- active evidence manifest;
- source universe proof;
- source input manifest;
- daily/hourly level compatibility ledger;
- runtime history ledger;
- forecast ledger;
- desired-position ledger;
- order ledger rows;
- working-order transition ledger;
- fill ledger rows;
- cost ledger rows;
- PnL ledger rows;
- non-authorization constants;
- fail-closed gate labels.

The package does not implement local-row parsing, file replay, strategy diagnostics, backtests, provider/API calls, downloads, OOS, Lockbox, Forward, adapter work, deployment, trading, or promotion.

The only runner-facing function is a fail-closed stub:

```text
build_trusted_replay_bundle
```

It raises:

```text
ReplayExecutionBlocked
```

until a later operator authorization explicitly permits parser/file replay execution.

## Current Static Inspection Requirement

Before any further implementation, perform static inspection only to confirm:

- no dangling imports in the new scaffold package;
- no provider/API/download/parser/replay/backtest execution path;
- `runner.py` fails closed;
- `s27_v2.py` was not modified by this scaffolding step;
- unresolved gates remain represented as fail-closed labels.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
ALL_EXPECTED_SCAFFOLD_FILES_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
RUNNER_ENTRY_POINT_FAILS_CLOSED_WITH_ReplayExecutionBlocked
```

No parser execution, file replay, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation were performed.

Python import/compile/test execution was intentionally not run under this authorization.

## Audit Finding Patch

The subsequent local hostile audit result is recorded at:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-06.md
```

That audit found no P0 execution-surface issue, but found P1/P2 schema and export gaps. The operator then authorized a narrow audit-finding patch only. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_AUDIT_FINDING_PATCH_RECORD_2026-06-06.md
```

Patched areas:

- non-opaque forecast ledger fields;
- source-universe universe/reason/duplicate/canonical-locator fields;
- daily/hourly compatibility raw-symbol and proof fields;
- cost multiplier/currency-conversion/deflation fields;
- package exports for key scaffold types.

The patch did not authorize or perform parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, or result interpretation.

## Cost Schema Re-Audit Finding Patch

A subsequent local hostile re-audit found that the cost-schema patch still partially left the price-space spread conversion basis underconstrained. The re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_PATCH_REAUDIT_RESULT_2026-06-06.md
```

The operator then authorized a narrow cost-schema re-audit finding patch only. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_COST_SCHEMA_REAUDIT_FINDING_PATCH_RECORD_2026-06-06.md
```

Patched areas:

- explicit `SpreadSpace` membership validation;
- fail-closed multiplier value/source proof requirement for positive `PRICE_SPACE` spread.

This later patch did not authorize or perform parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, or result interpretation.

## Next Gate

The cost-schema re-audit finding patch was subsequently re-audited and passed in:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLDING_COST_SCHEMA_PATCH_REAUDIT_RESULT_2026-06-06.md
```

The patched scaffold was then sent to GPT Extended Pro / GPT-5.5 for external hostile audit. That synthesis is:

```text
docs/process/CARVER_S27_ZN_V2_GPT_REPLAY_SCAFFOLD_PATCHED_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

The next step is no longer the cost-schema re-audit. The current next gate is a narrow GPT P1 schema-hardening patch if separately authorized. That patch must not run parser/file replay, diagnostics, backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation.

## GPT P1 Schema Hardening Patch

The operator later authorized the GPT P1 schema-hardening patch only. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_SCHEMA_HARDENING_PATCH_RECORD_2026-06-06.md
```

The next step after that patch is a local hostile audit of the GPT P1 schema-hardening patch if separately authorized. That audit must not run parser/file replay, diagnostics, backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation.

## GPT P1 Schema Hardening Local Audit

The operator later authorized a local hostile audit of the GPT P1 schema-hardening patch. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_SCHEMA_HARDENING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

That audit found no P0, found one remaining P1 in cost arithmetic binding, and found one P2 in transition optional-field exclusivity. The current next gate is a narrow cost-arithmetic binding patch, optionally including transition optional-field exclusivity, if separately authorized.

## Cost Arithmetic And Transition Exclusivity Patch

The operator later authorized a narrow patch for cost-arithmetic binding and transition optional-field exclusivity only. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_COST_ARITHMETIC_AND_TRANSITION_EXCLUSIVITY_PATCH_RECORD_2026-06-06.md
```

The next step after that patch is a local hostile re-audit if separately authorized. That audit must not run parser/file replay, diagnostics, backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation.

## Cost Arithmetic And Transition Exclusivity Local Re-Audit

The operator later authorized a local hostile re-audit of the cost-arithmetic binding and transition optional-field exclusivity patch only. The re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_COST_ARITHMETIC_AND_TRANSITION_EXCLUSIVITY_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

That re-audit found no P0 and no remaining P2 in the narrow transition optional-field exclusivity scope, but it did find one remaining P1: `PRICE_SPACE` spread cost is still not arithmetically bound to a numeric multiplier value and fill quantity. The current next gate is a narrow price-space spread-cost arithmetic binding patch if separately authorized.

## Price-Space Spread-Cost Arithmetic Binding Patch

The operator later authorized a narrow patch of the remaining price-space spread-cost arithmetic binding P1. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_PRICE_SPACE_SPREAD_COST_ARITHMETIC_BINDING_PATCH_RECORD_2026-06-06.md
```

That patch added numeric `contract_multiplier_value` to `CostLedgerRow` and requires `PRICE_SPACE` spread cost to equal `spread_amount * contract_multiplier_value * fill.quantity`. The current next gate is a local hostile re-audit of this narrow patch if separately authorized.

## Price-Space Spread-Cost Arithmetic Binding Local Re-Audit

The standing local hostile-audit pre-approval rule was then applied to re-audit the price-space spread-cost arithmetic binding patch. The re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_PRICE_SPACE_SPREAD_COST_ARITHMETIC_BINDING_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

That re-audit found no P0 and no remaining P1: the price-space spread-cost arithmetic binding issue is closed. It found one remaining P2: commission-only `LIMIT` cost rows can still carry irrelevant optional cost fields such as multiplier, currency-conversion, and deflation proof fields. The current next gate is a narrow `LIMIT` cost-row optional-field exclusivity patch if separately authorized.

## Limit Cost-Row Optional-Field Exclusivity Patch

The operator later authorized a narrow patch of the remaining `LIMIT` cost-row optional-field exclusivity P2. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_LIMIT_COST_ROW_OPTIONAL_FIELD_EXCLUSIVITY_PATCH_RECORD_2026-06-06.md
```

That patch rejects multiplier, currency-conversion, and deflation optional fields on commission-only `LIMIT` cost rows. The standing local hostile-audit pre-approval rule permits a local hostile re-audit of this narrow patch.

## Limit Cost-Row Optional-Field Exclusivity Local Re-Audit

The standing local hostile-audit pre-approval rule was then applied to re-audit the `LIMIT` cost-row optional-field exclusivity patch. The re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_LIMIT_COST_ROW_OPTIONAL_FIELD_EXCLUSIVITY_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

That re-audit found no P0/P1/P2/P3 in the narrow static cost-schema scope. The current next gate is an external GPT Extended Pro hostile-audit handoff packet for the locally re-audited patched scaffold if separately authorized.

## GPT Locally Re-Audited Replay Scaffold External Audit

The operator later provided the GPT Extended Pro external hostile-audit result for the locally re-audited patched scaffold. The synthesis is:

```text
docs/process/CARVER_S27_ZN_V2_GPT_LOCALLY_REAUDITED_REPLAY_SCAFFOLD_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

GPT returned `PASS_WITH_REQUIRED_EDITS`: no P0, prior cost/exclusivity patch findings accepted as closed, but three P1 source-faithfulness blockers remain before parser/file replay implementation planning:

- source-row/forecast positivity;
- trend-veto, zero-trend, and cap invariants;
- exact next-completed fill-row or session-gap proof.

The current next gate is a narrow GPT P1 fail-closed schema patch if separately authorized.

## GPT P1 Fail-Closed Schema Patch

The operator later authorized a narrow GPT P1 fail-closed schema patch covering source-row/forecast positivity, trend-veto/zero/cap invariants, and exact next-completed fill-row or session-gap proof scaffolding. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_FAIL_CLOSED_SCHEMA_PATCH_RECORD_2026-06-06.md
```

The standing local hostile-audit pre-approval rule permits a local hostile re-audit of this narrow patch.

## GPT P1 Fail-Closed Schema Local Re-Audit

The standing local hostile-audit pre-approval rule was then applied to re-audit the GPT P1 fail-closed schema patch. The re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_FAIL_CLOSED_SCHEMA_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

That re-audit found no P0/P1 in the narrow static scope and confirmed the three GPT P1 findings are closed at scaffold schema level. Residual P2 items remain: proof hashes are syntactic until parser/replay construction binds contents, and V/Q/M downstream arithmetic is not yet arithmetically bound. The current next gate is a narrow GPT P2 hardening patch if separately authorized, or external re-audit if the operator prefers.

## GPT P2 Hardening Patch

The operator later authorized a narrow GPT P2 hardening patch covering public-export structural-schema-only hardening, evidence-manifest required-family hardening, and V/Q/M post-veto arithmetic binding. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_HARDENING_PATCH_RECORD_2026-06-06.md
```

The standing local hostile-audit pre-approval rule permits a local hostile re-audit of this narrow patch.

## GPT P2 Hardening Local Re-Audit

The standing local hostile-audit pre-approval rule was then applied to re-audit the GPT P2 hardening patch. The re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_HARDENING_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

That re-audit found no P0/P1/P2 in the narrow static scope. It confirmed package-root public-export hardening, structural-schema-only warning visibility, required evidence manifest family/status/uniqueness guards, trust-root/evidence-manifest hash cross-checks, and V/Q/M post-veto arithmetic binding. The current next gate is an external GPT Extended Pro hostile-audit handoff or the next separately authorized parser/file replay implementation planning step, at the operator's choice.

## GPT P2 External Audit Synthesis

The locally re-audited GPT P2 hardening packet was sent to GPT Extended Pro for external hostile audit. The synthesis is:

```text
docs/process/CARVER_S27_ZN_V2_GPT_P2_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

GPT returned `PASS_WITH_REQUIRED_EDITS`: no P0, but one P1 and two P2 findings remain. Parser/file replay implementation planning remains blocked until the zero mean-reversion/equilibrium flat branch, package-root trusted-bundle export hardening, and source input manifest daily continuous/current-contract/previous-close hash binding are patched and re-audited. The current next gate is a narrow GPT P2 external-audit finding patch if separately authorized.

## GPT P2 External-Audit Finding Patch

The operator later authorized a narrow GPT P2 external-audit finding patch covering zero mean-reversion/equilibrium flat branch, package-root trusted-bundle export hardening, and source input manifest daily continuous/current-contract/previous-close hash binding. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_EXTERNAL_AUDIT_FINDING_PATCH_RECORD_2026-06-06.md
```

The standing local hostile-audit pre-approval rule permits a local hostile re-audit of this narrow patch before any parser/file replay implementation planning step.

## GPT P2 External-Audit Finding Patch Local Re-Audit

The standing local hostile-audit pre-approval rule was then applied to re-audit the GPT P2 external-audit finding patch. The re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P2_EXTERNAL_AUDIT_FINDING_PATCH_LOCAL_REAUDIT_RESULT_2026-06-06.md
```

That re-audit found no P0/P1/P2 in the narrow static scope. It confirmed the zero mean-reversion/equilibrium flat branch, zero EWMAC trend fail-closed behavior, package-root trusted-bundle export hardening, and source input manifest daily lineage split. The current next gate is the next separately authorized parser/file replay implementation planning step, or an external GPT re-audit if the operator wants one more external check.

## GPT P2 External-Audit Finding Patch External Re-Audit

The locally re-audited GPT P2 external-audit finding patch was sent to GPT Extended Pro for external hostile re-audit. The synthesis is:

```text
docs/process/CARVER_S27_ZN_V2_GPT_P2_EXTERNAL_AUDIT_FINDING_PATCH_EXTERNAL_REAUDIT_SYNTHESIS_2026-06-06.md
```

GPT returned `PASS`: no P0/P1/P2/P3 findings. GPT confirmed the prior zero mean-reversion/equilibrium blocker, package-root export blocker, and source input manifest daily-lineage blocker are closed. GPT stated that parser/file replay implementation planning may proceed, while parser/file replay execution and any source-faithful replay evidence claim remain outside the scaffold state and require separate authorization.

## Parser/File Replay Implementation Planning

The operator later authorized parser/file replay implementation planning. The process-only planning artifact is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_IMPLEMENTATION_PLANNING_2026-06-06.md
```

This artifact plans the next implementation slice for inert parser/file replay planning scaffolding only. It does not authorize parser/file replay execution, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Parser/File Replay Planning Code Scaffolding

The operator later authorized S27_V2 parser/file replay planning code scaffolding only. The scaffolding record is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLDING_RECORD_2026-06-06.md
```

Added inert planning modules:

```text
src/carver/spine/s27_v2_replay/file_contract.py
src/carver/spine/s27_v2_replay/parser_plan.py
src/carver/spine/s27_v2_replay/replay_config.py
src/carver/spine/s27_v2_replay/replay_builder_plan.py
src/carver/spine/s27_v2_replay/artifact_manifest_plan.py
```

These modules are structural planning scaffolds only. They do not implement parser execution, file replay, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Parser/File Replay Planning Code Scaffolding Local Audit

The operator then supplied a read-only/static local hostile-audit scope for the parser/file replay planning code scaffolding. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

That audit found no P0/P1/P2/P3 in the narrow static scope. It confirmed the five new planning modules are inert structural dataclasses/validators only, the package root remains fail-closed and does not export planning dataclasses as source-faithful evidence, the planning surfaces bind the governing planning artifact, and no forbidden execution/provider/download/backtest/diagnostic surface was found by static text scan.

## Parser/File Replay Planning Code Scaffolding External Audit Handoff

The operator later authorized preparing a GPT Extended Pro external hostile-audit handoff packet for the locally audited parser/file replay planning code scaffold. The handoff record is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLDING_EXTERNAL_AUDIT_HANDOFF_2026-06-06.md
```

The handoff is process-only. It does not authorize parser/file replay execution, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Parser/File Replay Planning Code Scaffolding External Audit Synthesis

The operator later supplied the GPT Extended Pro external hostile-audit result for the locally audited parser/file replay planning code scaffold. The synthesis is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLDING_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

GPT returned `PASS`: no P0/P1/P2/P3 findings. GPT confirmed the parser/file replay planning scaffold remains inert and structural only, package-root exports remain fail-closed, the five planning modules bind to the planning artifact and trust-root design, and evidence-manifest/replay-builder planning surfaces remain fail-closed before real parser/file replay implementation exists.

The next possible step is a separately authorized next implementation slice. Parser/file replay execution, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Parser/File Replay Next Implementation Slice Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_NEXT_IMPLEMENTATION_SLICE_SCAFFOLDING_RECORD_2026-06-06.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/construction_contract.py
```

This module locks the future parser/file replay construction phase order and validates supplied construction-contract metadata only. It does not execute parser work, file replay, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Parser/File Replay Next Implementation Slice Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the construction-contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_NEXT_IMPLEMENTATION_SLICE_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Replay Contract Layer GPT P1 Hardening Patch

The operator later authorized a narrow GPT P1 hardening patch for the replay contract layer only. The patch record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_GPT_P1_HARDENING_PATCH_RECORD_2026-06-07.md
```

Patched areas:

- stale-evidence supersession manifest trust-root binding;
- `STALE_EVIDENCE_SUPERSESSION_MANIFEST` required evidence artifact coverage;
- tuple-valued superseded-artifact manifests;
- complete locked unresolved-gate tuple coverage in construction, replay-builder, and validation contract surfaces.

The patch did not authorize or perform parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Replay Contract Layer GPT P1 Hardening Local Audit

The standing local hostile-audit pre-approval rule was applied to the replay contract-layer GPT P1 hardening patch. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_GPT_P1_HARDENING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed stale-evidence supersession trust-root binding, complete locked unresolved-gate coverage, and the preserved package-root fail-closed export boundary.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Raw File Hash Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_RAW_FILE_HASH_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/raw_file_hash_contract.py
```

This module locks future raw source file hash-set metadata before parser/file replay execution. It validates supplied contract metadata only: required raw source file family coverage, file declaration hash bindings, parser plan hash bindings, `NO_PROVIDER_API_NO_DOWNLOAD` assertions, and aggregate raw file hash-set hash presence.

It does not open files, enumerate directories, hash files, parse rows, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Raw File Hash Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the raw file hash contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_RAW_FILE_HASH_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks required raw source file family coverage and aggregate hash-set bindings, preserves no-provider/no-download assertions, and does not broaden package-root exports or add forbidden execution surfaces.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Parser Output Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only after `raw_file_hash_contract.py` local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_OUTPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/parser_output_contract.py
```

This module locks required future parser-output row families and validates supplied parser-output batch metadata only. It does not open files, enumerate paths, hash files, parse rows, construct row batches, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

## Parser Output Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the parser output contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_OUTPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks required parser-output row family coverage and aggregate batch-set bindings, preserves non-authorizations, and does not broaden package-root exports or add forbidden execution surfaces.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Source Row Batch Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only after `parser_output_contract.py` local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_ROW_BATCH_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/source_row_batch_contract.py
```

This module locks required future source-row batch families and validates supplied source-row batch metadata only. It does not open files, enumerate paths, hash files, parse rows, construct source-row objects, construct row batches, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

## Source Row Batch Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the source row batch contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_ROW_BATCH_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks required source-row batch family coverage and aggregate batch-set bindings, preserves non-authorizations, and does not broaden package-root exports or add forbidden execution surfaces.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Source Input Selection Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only after `source_row_batch_contract.py` local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_INPUT_SELECTION_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
```

This module locks required future source-input role selections and validates supplied selection metadata only. It does not open files, enumerate paths, hash files, parse rows, select rows, construct source-input manifest rows, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

## Source Input Selection Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the source input selection contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_INPUT_SELECTION_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks required source-input role coverage and role-to-family bindings, preserves non-authorizations, and does not broaden package-root exports or add forbidden execution surfaces.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Source Input Manifest Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only after `source_input_selection_contract.py` local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_INPUT_MANIFEST_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

This module locks required future source-input manifest fields and validates supplied manifest metadata only. It does not open files, enumerate paths, hash files, parse rows, select rows, construct source-input manifest rows, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

The next possible gate is a static/read-only local hostile audit under the standing local hostile-audit pre-approval rule.

## Source Input Manifest Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the source input manifest contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_INPUT_MANIFEST_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks required source-input manifest field coverage and role bindings, preserves non-authorizations, and does not broaden package-root exports or add forbidden execution surfaces.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Level Compatibility Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the source input manifest contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
```

This module locks required level-compatibility input labels, their source-input manifest field and role bindings, and the exact input-label tuple required by each locked level-compatibility proof. It validates supplied metadata only. It does not open files, parse rows, select rows, compare price levels, construct compatibility proofs, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Level Compatibility Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the level compatibility input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks level-compatibility inputs to source-input manifest fields and roles, locks proof-input bindings and matching field contract hashes, preserves non-authorizations, and does not broaden package-root exports or add forbidden execution surfaces.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Runtime History Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the level compatibility input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_RUNTIME_HISTORY_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
```

This module locks required runtime-history input labels, their source-input manifest field and role bindings, price-level input links to level-compatibility inputs, runtime state input labels, and V/Q/M dependency labels. It validates supplied metadata only. It does not open files, parse rows, select rows, compare price levels, construct compatibility proofs, compute EWMA5/EWMAC/sigma/V/Q/M, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Runtime History Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the runtime history input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_RUNTIME_HISTORY_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks runtime-history inputs to source-input manifest fields and roles, locks price-level input links to level-compatibility inputs, locks runtime state and V/Q/M dependency bindings with matching contract hashes, preserves non-authorizations, and does not broaden package-root exports or add forbidden execution surfaces.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Forecast Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the runtime history input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_FORECAST_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/forecast_input_contract.py
```

This module locks required forecast input labels, their runtime-input/runtime-state/V/Q/M/policy source-kind bindings, component dependency labels, decision-branch dependency labels, and invariant dependency labels. It validates supplied metadata only. It does not open files, parse rows, select rows, compute EWMA5/EWMAC/sigma/V/Q/M/forecasts, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Forecast Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the forecast input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_FORECAST_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks complete ordered forecast input coverage, binds forecast inputs to locked runtime-history inputs/states, V/Q/M components, and source-policy labels, locks component/branch/invariant dependency labels with matching dependency contract hashes, preserves non-authorizations, and does not broaden package-root exports or add forbidden execution surfaces.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Position Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the forecast input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_POSITION_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/position_input_contract.py
```

This module locks required position input labels, their forecast-ledger/forecast-component/rounding-policy/current-position/policy source-kind bindings, position component dependency labels, and position invariant dependency labels. It validates supplied metadata only. It does not open files, parse rows, select rows, compute forecasts, compute desired positions, apply rounding, generate orders, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Position Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the position input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_POSITION_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks ordered required position input coverage and source-kind mappings, enforces source-target exclusivity, binds position component and invariant dependency labels to matching dependency contract hashes, preserves package-root export boundaries, and does not compute desired positions, apply rounding, generate orders, interpret results, or claim source-faithful replay evidence.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Order Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the position input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_ORDER_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/order_input_contract.py
```

This module locks required order input labels, their position-ledger/position-component/order-kind/order-transition/working-order-state/policy source-kind bindings, order component dependency labels, and order invariant dependency labels. It validates supplied metadata only. It does not open files, parse rows, select rows, compute forecasts, compute desired positions, generate orders, price limit orders, apply tick rounding, advance working-order state, execute fills, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Order Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the order input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_ORDER_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks required order inputs, source-kind mappings, and dependency hash bindings, preserves package-root export boundaries, and does not generate orders, price limits, execute tick rounding, advance working-order state, execute fills, run replay, diagnostics, tests/backtests, provider/API/download, OOS/Lockbox/Forward, Git actions, or source-faithful replay evidence claims.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Fill Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the order input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_FILL_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/fill_input_contract.py
```

This module locks required fill input labels, their order-ledger/working-order-transition/source-row-proof/fill-price-provenance/fill-branch/policy source-kind bindings, fill component dependency labels, and fill invariant dependency labels. It validates supplied metadata only. It does not open files, parse rows, select rows, compute forecasts, compute desired positions, generate orders, price limits, apply tick rounding, advance working-order state, select next completed hourly rows, create fill rows, compute fill prices, compute costs/PnL, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Fill Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the fill input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_FILL_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Cost Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the fill input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_COST_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/cost_input_contract.py
```

This module locks required cost input labels, their fill-ledger/cost-branch/spread-space/policy/multiplier-proof/currency-proof source-kind bindings, cost component dependency labels, and cost invariant dependency labels. It validates supplied metadata only. It does not open files, parse rows, select rows, compute forecasts, compute desired positions, generate orders, create fill rows, compute fill prices, compute commission, compute spread cost, compute total cost, compute PnL, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Cost Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the cost input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_COST_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks required cost inputs, source-kind mappings, dependency hash bindings, and source-target exclusivity, preserves package-root export boundaries, and does not compute commission, spread, total cost, PnL, run replay, diagnostics, tests/backtests, provider/API/download, OOS/Lockbox/Forward, Git actions, or source-faithful replay evidence claims.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## PnL Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the cost input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_PNL_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/pnl_input_contract.py
```

This module locks required PnL input labels, their trust-root/source-universe/transition-ledger/position-source/price-source/price-row-proof/bridge-proof/fill-hash-set/cost-hash-set/multiplier-proof/currency-proof/policy source-kind bindings, PnL component dependency labels, and PnL invariant dependency labels. It validates supplied metadata only. It does not open files, parse rows, select rows, compute forecasts, compute desired positions, generate orders, create fill rows, compute costs, select prices, compute PnL, interpret results, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, or source-faithful replay evidence claims.

## PnL Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the PnL input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PNL_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks required PnL inputs including source-universe hash, source-kind mappings, dependency hash bindings, and source-target exclusivity, preserves package-root export boundaries, and does not select prices, compute PnL, apply costs/currency conversion, interpret results, run replay, diagnostics, tests/backtests, provider/API/download, OOS/Lockbox/Forward, Git actions, or source-faithful replay evidence claims.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Validation Input Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the PnL input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_VALIDATION_INPUT_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/validation_input_contract.py
```

This module binds future validation/provenance inputs to locked trust-root, active evidence manifest, source-input manifest, PnL contract, PnL input contract, validation/provenance/local-audit schema, unresolved-gate, and source-policy labels. It does not construct validation ledgers, construct provenance ledgers, run audits, prepare external packets, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Validation Input Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the validation input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_VALIDATION_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks validation input/component/ledger/checkpoint/invariant coverage, binds the complete unresolved-gate tuple, preserves package-root export boundaries, and does not construct validation/provenance ledgers, run audits, prepare external packets, execute parser/file replay, run diagnostics/tests/backtests, provider/API/download, OOS/Lockbox/Forward, Git actions, or source-faithful replay evidence claims.

## Trusted Bundle Contract Scaffolding

The operator later authorized the next narrow parser/file replay implementation slice scaffolding only, after the validation input contract local audit PASS. The record is:

```text
docs/process/CARVER_S27_ZN_V2_TRUSTED_BUNDLE_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/trusted_bundle_contract.py
```

This module binds future final trusted-bundle inputs, components, and invariants to locked trust-root, active evidence manifest, construction contract, validation input contract, validation contract, validation ledger, provenance ledger, local-audit result, public-boundary policy, non-authorization policy, and no-source-faithful-claim policy labels. It does not assemble trusted bundles, execute parser work, execute file replay, construct validation/provenance ledgers, run audits, prepare external packets, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Trusted Bundle Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was applied to the trusted bundle contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_TRUSTED_BUNDLE_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the scaffold is inert contract-only metadata validation, locks trusted-bundle input/component/invariant coverage, binds public-boundary, non-authorization, and no-source-faithful-claim policies, preserves package-root export boundaries, keeps the runner fail-closed, and does not assemble trusted bundles, execute parser/file replay, run diagnostics/tests/backtests, provider/API/download, OOS/Lockbox/Forward, Git actions, or source-faithful replay evidence claims.

## Replay Contract Layer GPT P1 Hardening External Re-Audit Handoff

The operator later authorized preparing a GPT Extended Pro external hostile re-audit handoff packet for the locally audited replay contract-layer GPT P1 hardening patch. The handoff record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_GPT_P1_HARDENING_EXTERNAL_REAUDIT_HANDOFF_2026-06-07.md
```

The `C:\Users\apops\Desktop\GPT` folder was cleaned first and populated with a 13-file focused packet. The large hostile-audit prompt is provided in the agent response, not written into the folder.

The handoff preparation did not authorize or perform parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Replay Contract Layer GPT P1 Hardening External Re-Audit Synthesis

The operator later supplied the GPT Extended Pro external hostile re-audit result for the locally audited replay contract-layer GPT P1 hardening patch. The synthesis is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_GPT_P1_HARDENING_EXTERNAL_REAUDIT_SYNTHESIS_2026-06-07.md
```

GPT returned `PASS`: no P0/P1/P2 findings. GPT confirmed both original P1 findings are closed: stale-evidence supersession trust-root binding and complete locked unresolved-gate coverage.

GPT listed two non-blocking P3 notes: the source zip was packaged flat rather than preserving the repo-relative path prefix, and `ReplayFailClosedGatePlan.gate_label` remains free text while `blocked_status` is the authoritative locked gate field.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Replay Contract Layer P3 Gate-Label Clarity Cleanup

The operator later authorized a narrow P3 clarity cleanup for `ReplayFailClosedGatePlan.gate_label` only. The cleanup record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_P3_GATE_LABEL_CLARITY_CLEANUP_RECORD_2026-06-07.md
```

The patch requires `ReplayFailClosedGatePlan.gate_label` to equal `ReplayFailClosedGatePlan.blocked_status`, preserving `blocked_status` as the authoritative locked unresolved-gate field while removing free-text ambiguity.

The cleanup did not authorize or perform parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Replay Contract Layer P3 Gate-Label Clarity Local Audit

The standing local hostile-audit pre-approval rule was applied to the replay contract-layer P3 gate-label clarity cleanup. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_P3_GATE_LABEL_CLARITY_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed `ReplayFailClosedGatePlan.gate_label` must now match `blocked_status`, `blocked_status` remains authoritative for coverage, and no forbidden execution surface was added.

Parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Level Compatibility Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_RECORD_2026-06-06.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/level_compatibility_contract.py
```

This module locks required daily/hourly level-compatibility proof labels and validates supplied compatibility contract metadata only. It does not open files, parse rows, compare daily/hourly price levels, compute bridge arithmetic, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Level Compatibility Contract Scaffolding Local Audit And Patch

The standing local hostile-audit pre-approval rule was later applied to audit the level-compatibility contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

The audit returned `PASS_WITH_P2_REQUIRED_EDIT`: no P0/P1/P3 findings, but one P2 finding remained. The verdict proof hashes were length-checked but not required to equal the supplied proof contract hashes.

The P2 finding patch record is:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_AUDIT_FINDING_PATCH_RECORD_2026-06-06.md
```

The patch re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_PATCH_REAUDIT_RESULT_2026-06-06.md
```

The re-audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Runtime History Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_RUNTIME_HISTORY_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/runtime_history_contract.py
```

This module locks required runtime state families and V/Q/M component labels and validates supplied runtime-history contract metadata only. It does not open files, parse rows, compute EWMA/EWMAC/sigma/V/Q/M/forecasts, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Runtime History Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the runtime-history contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_RUNTIME_HISTORY_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Forecast Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_FORECAST_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/forecast_contract.py
```

This module locks required forecast component families, forecast decision branches, and forecast invariant proof labels, and validates supplied forecast contract metadata only. It does not open files, parse rows, compute forecasts, compute positions, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Forecast Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the forecast contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_FORECAST_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Position Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_POSITION_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/position_contract.py
```

This module locks required desired-position component families, invariant labels, and rounding-policy labels, and validates supplied position contract metadata only. It does not open files, parse rows, compute positions, generate orders, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Position Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the position contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_POSITION_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Order Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_ORDER_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/order_contract.py
```

This module locks required order component families, order kind labels, transition kind labels, and order invariant labels, and validates supplied order contract metadata only. It does not open files, parse rows, generate orders, execute fills, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Order Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the order contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_ORDER_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Fill Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_FILL_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/fill_contract.py
```

This module locks required fill component families, fill price provenance labels, fill branch labels, and fill invariant labels, and validates supplied fill contract metadata only. It does not open files, parse rows, execute fills, compute fill prices, compute costs, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Fill Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the fill contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_FILL_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Cost Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_COST_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/cost_contract.py
```

This module locks required cost component families, cost branch labels, spread-space labels, and cost invariant labels, and validates supplied cost contract metadata only. It does not open files, parse rows, compute commission/spread/total costs, compute PnL, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Cost Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the cost contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_COST_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## PnL Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_PNL_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/pnl_contract.py
```

This module locks required PnL component families, close-only price-source labels, raw-symbol/roll bridge labels, and PnL invariant labels, and validates supplied PnL contract metadata only. It does not open files, parse rows, compute PnL, compute returns, compute result metrics, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## PnL Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the PnL contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PNL_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Validation Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_VALIDATION_CONTRACT_SCAFFOLDING_RECORD_2026-06-07.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/validation_contract.py
```

This module locks required validation component families, validation/provenance/audit ledger labels, audit checkpoint labels, and validation invariant labels, and validates supplied validation/provenance contract metadata only. It does not open files, parse rows, construct validation ledgers, construct provenance ledgers, run local hostile audits, prepare external audit packets, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Validation Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the validation/provenance contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_VALIDATION_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Source Universe Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_UNIVERSE_CONTRACT_SCAFFOLDING_RECORD_2026-06-06.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/source_universe_contract.py
```

This module locks required source-universe families and validates supplied source-universe contract metadata only. It does not open files, parse rows, construct source universes, filter rows, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Source Universe Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the source-universe contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_UNIVERSE_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

## Row Locator Contract Scaffolding

The operator later authorized the next narrow implementation slice scaffolding only. The record is:

```text
docs/process/CARVER_S27_ZN_V2_ROW_LOCATOR_CONTRACT_SCAFFOLDING_RECORD_2026-06-06.md
```

Added inert module:

```text
src/carver/spine/s27_v2_replay/row_locator_contract.py
```

This module locks required source row locator families and validates supplied row-locator contract metadata only. It does not open files, parse rows, enumerate paths, execute parser work, execute file replay, run diagnostics/tests/backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, perform Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Row Locator Contract Scaffolding Local Audit

The standing local hostile-audit pre-approval rule was later applied to audit the row-locator contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_ROW_LOCATOR_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. The next possible implementation slice still requires separate explicit operator authorization.

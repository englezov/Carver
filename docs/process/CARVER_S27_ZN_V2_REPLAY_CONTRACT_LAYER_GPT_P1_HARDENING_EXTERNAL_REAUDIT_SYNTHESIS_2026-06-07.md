# S27 ZN V2 Replay Contract Layer GPT P1 Hardening External Re-Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_CONTRACT_LAYER_GPT_P1_HARDENING_EXTERNAL_REAUDIT_SYNTHESIS_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Source

Operator supplied the GPT Extended Pro / GPT-5.5 external hostile re-audit result for the locally audited S27_V2 replay contract-layer GPT P1 hardening patch.

The re-audit inspected the handoff packet prepared in:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_GPT_P1_HARDENING_EXTERNAL_REAUDIT_HANDOFF_2026-06-07.md
```

The re-audit used the source packet:

```text
S27_V2_REPLAY_CONTRACT_LAYER_GPT_P1_HARDENING_SOURCE_PACKET_2026-06-07.zip
```

Observed source packet SHA256:

```text
239517b2c8f95d612fc18fff6a39e5cb820e41f8a874a683c1523215ccc1c663
```

The external re-audit reported:

```text
Python files inspected: 36
Python LOC inspected: 4,270
```

GPT did not perform a read-only GitHub cross-check. It treated the attached packet as sufficient primary evidence for the narrow re-audit.

## Verdict

```text
PASS
```

Findings:

```text
P0: NONE
P1: NONE
P2: NONE
P3: 2 NON_BLOCKING_NOTES
```

The external re-audit explicitly concluded that both original P1 findings are closed in the narrow static scope.

## Original P1 Closure

### P1-1 Stale Evidence Supersession Trust-Root Binding

GPT concluded this finding is closed.

It confirmed:

- `STALE_EVIDENCE_SUPERSESSION_MANIFEST` is present in `REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES`;
- `ReplayTrustRoot.stale_evidence_supersession_manifest_hash` exists;
- the trust-root field is validated with `require_hash`;
- `TrustedReplayBundleScaffold.validate()` cross-checks the active evidence-manifest artifact hash against the trust-root field;
- `EvidenceManifest.superseded_artifacts` is tuple-valued and enforced;
- `PlannedEvidenceManifest.superseded_artifacts` is tuple-valued and enforced.

### P1-2 Complete Unresolved-Gate Coverage

GPT concluded this finding is closed.

It confirmed:

- `REQUIRED_UNRESOLVED_GATE_LABELS` exists as a single locked unresolved-gate tuple;
- construction phase validation rejects unknown gate labels;
- the construction contract requires complete gate coverage;
- replay-builder gate validation rejects unknown blocked statuses;
- the replay-builder plan requires complete gate coverage;
- the validation contract carries the required unresolved-gate tuple;
- the validation contract requires exact tuple equality against `REQUIRED_UNRESOLVED_GATE_LABELS`.

## Package-Root And Execution-Surface Review

GPT confirmed the package root remains fail-closed.

Package-root exports remain limited to:

```text
ReplayExecutionBlocked
S27_V2_REPLAY_NON_AUTHORIZATION
STRUCTURAL_SCHEMA_ONLY_NOT_SOURCE_EVIDENCE
build_trusted_replay_bundle
```

GPT also confirmed the root execution-facing function still fails closed through:

```text
build_trusted_replay_bundle
```

No execution/provider/download/parser/replay/diagnostic/test/backtest/Git/adapter/deployment/trading/promotion surface was found in the narrow static packet review.

## P3 Notes

### P3-1 Source Packet Path-Prefix Mismatch

GPT noted that the handoff record describes the source packet as containing `.py` files under:

```text
src/carver/spine/s27_v2_replay/
```

but GPT observed the extracted zip files at archive root.

This is non-blocking because the target files were present and inspectable. Future packets should either preserve repo-relative paths in the zip or explicitly state that source files are packaged flat.

### P3-2 Free-Text Gate Label

GPT noted that `ReplayFailClosedGatePlan.gate_label` remains free text while `blocked_status` is authoritative.

This is non-blocking for the P1 closure because missing/unknown unresolved gate coverage is enforced through `blocked_status`. A later cleanup could require `gate_label == blocked_status` or rename the field to `human_label` to reduce future ambiguity.

## Residual Risk

The PASS does not mean S27 is parser-complete, replayed, source-faithful as an executed system, profitable, or ready for diagnostics/backtests/OOS/Lockbox/Forward.

The current artifact remains a scaffold/contract layer. A separately authorized trusted runner must still recompute from local rows and bind outputs to the active trust root before any replay evidence claim.

## Non-Authorization

This synthesis authorizes no code patch, no parser/file replay execution, no diagnostics, no tests/backtests, no provider/API calls, no downloads, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Next Gate

The next possible implementation gate is a narrow, separately authorized parser/file replay implementation slice.

Recommended first cleanup before or within that slice:

```text
S27_V2 replay contract-layer P3 clarity cleanup for ReplayFailClosedGatePlan.gate_label only
```

The zip path-prefix P3 is a future handoff packaging note and does not require code changes.

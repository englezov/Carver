# S27 ZN V2 Replay Scaffold GPT P1 Fail-Closed Schema Local Re-Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_FAIL_CLOSED_SCHEMA_LOCAL_REAUDIT_RESULT_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Standing local hostile-audit rule applied:

```text
Local hostile audits are pre-approved.
```

Audit boundary preserved:

```text
S27_V2 replay scaffold GPT P1 fail-closed schema patch only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a local hostile re-audit only. It authorizes and performed no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Method

Static inspection only:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Reviewed files:

```text
src/carver/spine/s27_v2_replay/source_rows.py
src/carver/spine/s27_v2_replay/forecast.py
src/carver/spine/s27_v2_replay/transitions.py
src/carver/spine/s27_v2_replay/fills.py
docs/process/CARVER_S27_ZN_V2_GPT_LOCALLY_REAUDITED_REPLAY_SCAFFOLD_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_FAIL_CLOSED_SCHEMA_PATCH_RECORD_2026-06-06.md
```

Independent subagent hostile audit was used as a parallel read-only reviewer. The subagent made no edits and reported no parser/file replay execution, Python import/compile/tests, diagnostics, backtests, provider/API calls, downloads, OOS/Lockbox/Forward access, Git commands, adapter work, deployment, trading, promotion, or result interpretation.

Package file count remained:

```text
19
```

Source-code forbidden-surface text scan found no matches for provider/API/download/backtest/diagnostic/subprocess/CLI/file-open/Git surfaces in the replay scaffold package.

## Verdict

```text
PASSED_NARROW_LOCAL_REAUDIT_WITH_RESIDUAL_P2_HARDENING_ITEMS
```

P0:

```text
NONE_FOUND
```

P1:

```text
NONE_FOUND
```

The three GPT P1 findings are closed at the scaffold schema level:

- source-row/forecast positivity now requires positive source closes, positive sigma inputs, and positive V/M multiplier-related values;
- zero EWMAC trend and zero pre-veto forecast states fail closed, trend-veto decision is bound to trend/mean-reversion sign agreement or opposition, and capped forecast is bounded to `[-20, 20]`;
- normal fill lag requires exact one-hour timing and a next-completed-hourly-row hash, while overnight/roll cases require explicit session-gap reason/proof scaffolding, and fill rows bind their decision source to the next completed hourly fill-row hash.

P2:

```text
RESIDUAL_P2_PROOF_HASHES_REMAIN_SYNTACTIC_NOT_CONTENT_BOUND
RESIDUAL_P2_VQM_AND_DOWNSTREAM_ARITHMETIC_NOT_BOUND
```

The first residual P2 is a scaffold limitation: proof hashes and reason codes are required, but the dataclasses do not verify referenced proof contents. This must not be treated as parser/file replay evidence.

The second residual P2 matches the prior GPT external audit: V/Q/M and downstream arithmetic remain value-auditable but not arithmetically bound in `ForecastReplayLedgerRow`.

P3:

```text
P3_TRANSITION_BLOCKED_MESSAGE_IS_COMBINED
```

Transition validation preserves fail-closed behavior but reports a combined blocked message for working-limit lifecycle, overnight, and roll bridge surfaces.

## Next Gate

Do not proceed directly to parser/file replay implementation planning.

The next safe code gate is a narrow P2 hardening patch if the operator wants to clear the remaining scaffold hardening items before another external audit:

```text
P2_PUBLIC_EXPORT_STRUCTURAL_SCHEMA_ONLY_HARDENING
P2_EVIDENCE_MANIFEST_REQUIRED_FAMILY_HARDENING
P2_VQM_POST_VETO_ARITHMETIC_BINDING
```

Recommended authorization text:

```text
Operator authorizes S27_V2 replay scaffold GPT P2 hardening patch only, covering public-export structural-schema-only hardening, evidence-manifest required-family hardening, and V/Q/M post-veto arithmetic binding, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

Alternatively, the operator may authorize an external re-audit of the P1-closed scaffold, but GPT already identified the P2 hardening items as efficient to include before the next implementation planning gate.

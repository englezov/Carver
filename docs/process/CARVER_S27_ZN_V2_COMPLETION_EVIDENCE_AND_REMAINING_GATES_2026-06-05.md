# Carver S27 ZN V2 Completion Evidence And Remaining Gates

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_V2_COMPLETION_EVIDENCE_MATRIX_NOT_RUNNER_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the current evidence state for the S27 ZN v2 source-faithful rebuild and
separate completed gates from remaining operator-authorized gates.

This document does not authorize provider/API access, data download, file
parsing, diagnostics, backtests, OOS, Lockbox, Forward, tuning, alpha claims,
promotion, Git staging, commit, push, PR, deployment, trading, or handoff
folder cleanup/copy.

## Evidence Matrix

| Requirement | Evidence | Status |
|---|---|---|
| Source-native lane declared | `SOURCE_NATIVE_FUTURES` in source lock, data-contract gate, implementation record, and audit records. | `COMPLETE_FOR_CURRENT_SLICE` |
| Book source-lock artifact created | `docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md` | `COMPLETE` |
| Source lock externally re-audited before v2 implementation | `docs/process/CARVER_S27_ZN_SOURCE_LOCK_REAUDIT_RESULT_2026-06-05.md` records `PASS_WITH_REQUIRED_EDITS` and `S27_ZN_BOOK_SOURCE_LOCK_PASSED_FOR_V2_IMPLEMENTATION_EXERCISE`. | `COMPLETE` |
| Old S27 results demoted | Source lock and v2 audit records label existing S27 result artifacts as `DIAGNOSTIC_ONLY_FAILURE_MAP_MATERIAL`. | `COMPLETE_FOR_CURRENT_SLICE` |
| S27 scalar locked as book-approximate | Source lock records S26 `9.3`, S27 book-estimated `around 20`, implementation freeze `20.0` not source-exact. | `COMPLETE_FOR_CURRENT_SLICE` |
| Forecast machinery implemented as v2 primitives | `src/carver/spine/s27_v2.py` implements daily runtime, forecast replay, V/Q/M, trend veto, scalar, cap, desired position. | `COMPLETE_FOR_SYNTHETIC_PRIMITIVES` |
| Execution/cost primitives implemented | `src/carver/spine/s27_v2.py` implements adjacent limit orders, market cases, one-hour fills, cost rows, PnL rows, working-order transition primitives. | `COMPLETE_FOR_SYNTHETIC_PRIMITIVES` |
| Replay-step ledger bundle implemented | `S27V2ReplayStepLedgerBundle` and tests in `tests/test_s27_v2_source_lock_synthetic.py`. | `COMPLETE_FOR_SYNTHETIC_PRIMITIVES` |
| Multi-row replay aggregation implemented | `S27V2ReplayRunLedgerBundle` and `build_s27_v2_multi_row_replay_ledger_bundle`. | `COMPLETE_FOR_CALLER_SUPPLIED_SYNTHETIC_OR_PREVALIDATED_ROWS` |
| Local hostile audit completed | `docs/process/CARVER_S27_ZN_V2_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-05.md` records Lovelace, Locke, and Nietzsche read-only audits and remediations. | `COMPLETE_FOR_CURRENT_SLICE` |
| External GPT audit remediated | `docs/process/CARVER_S27_ZN_V2_GPT_EXTERNAL_AUDIT_REMEDIATION_2026-06-05.md` records P0/P1 remediation for trend-aware limit sides, next-close-only fills, EOD cancel-before-fill, fail-closed statuses, strict-prior certification, and sigma-source status. | `COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE` |
| GPT re-audit target-position remediation | `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_TARGET_POSITION_REMEDIATION_2026-06-06.md` records the correction from order-side veto to target-position trend permission, zero-forecast flattening, direct transition fact validation, EOD market-order fail-closed behavior, and nearest-rounding lock. | `COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE_PENDING_EXTERNAL_REAUDIT` |
| GPT re-audit cap-edge remediation | `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_CAP_EDGE_REMEDIATION_2026-06-06.md` records the cap-edge adjacent candidate skip fix, order-plan internal consistency validation, and direct false-overnight guard coverage. | `COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE_PENDING_EXTERNAL_REAUDIT` |
| GPT re-audit market-fallback remediation | `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_MARKET_FALLBACK_REMEDIATION_2026-06-06.md` records the desired-side-at-cap market fallback fix, plan-level forged desired-gap validation, and direct at-cap implied-price tests. | `COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE_PENDING_EXTERNAL_REAUDIT` |
| Local data-contract gate created | `docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md`. | `COMPLETE_PROCESS_ONLY` |
| External audit packet manifest created | `docs/process/CARVER_S27_ZN_V2_EXTERNAL_AUDIT_PACKET_MANIFEST_2026-06-05.md`. | `COMPLETE_PROCESS_ONLY_NOT_HANDOFF` |
| Synthetic verification | `python -m unittest tests.test_s27_v2_source_lock_synthetic` reported `PASS_36_SYNTHETIC_UNIT_TESTS`. | `COMPLETE_FOR_CURRENT_SLICE` |
| Compile verification | `python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py` reported `PASS_COMPILE`. | `COMPLETE_FOR_CURRENT_SLICE` |

## Current Focused Hashes

| Artifact | SHA256 |
|---|---|
| `docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md` | `72A3357F320F9D92C742F58CA9B5EC0D1B865DAD488D7ADDFFBCB5CD23DAB51F` |
| `docs/process/CARVER_S27_ZN_SOURCE_LOCK_REAUDIT_RESULT_2026-06-05.md` | `36B19F379037FA465D11662D26BDDAF20ECF2DA51C77B4F45248F43DF04B133A` |
| `docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md` | `6A2D2368C6B5CBEB5E0E8275B55E0795665A0421DEDBB06A51F0FB6635B4A542` |
| `docs/process/CARVER_S27_ZN_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_2026-06-05.md` | `FF9FDF1484A56CEBAA771AFBFB12ED491F07D9D9D16752A568D86AB9E023043A` |
| `docs/process/CARVER_S27_ZN_V2_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-05.md` | `13542DF162CDB80ECEC80C670A5687B8DA9C0C5F45B0440E2E6E4EDDA8E38276` |
| `docs/process/CARVER_S27_ZN_V2_GPT_EXTERNAL_AUDIT_REMEDIATION_2026-06-05.md` | `D9BD7224D1AF4E5A5608332D3C3431EB9BE1236C88B5F20F0B697AF3A21C8838` |
| `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_TARGET_POSITION_REMEDIATION_2026-06-06.md` | `D60C457F721420D8ED34BC05D550D0ADFEA0E0CB8B07EC07326E878C0EE27252` |
| `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_CAP_EDGE_REMEDIATION_2026-06-06.md` | `68FAA8822EF365CB2EE64B94CC14DC12D51E8DDF8AD3E721E5248AB39C7B283A` |
| `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_MARKET_FALLBACK_REMEDIATION_2026-06-06.md` | `F647E2C2D507278D3DDAC1B8E82E8E9D12EB0212D229F3C272CB5A757DDA4429` |
| `docs/process/CARVER_S27_ZN_V2_EXTERNAL_AUDIT_PACKET_MANIFEST_2026-06-05.md` | `0ACDA6A46AB5219C4627A5D27DEC446313B65B7C376E600F42C6AA7DB3294F77` |
| `src/carver/spine/s27_v2.py` | `16C73F7C5BAAF73FF538DFBC051F24D6826903CA3B3E08007361D7CD9412F253` |
| `tests/test_s27_v2_source_lock_synthetic.py` | `CA181E79173767C4679C161BDC33ED1C93A810ED55F6B7881388A70CB96DBC65` |

## Remaining Gates

The following work remains outside current authorization and must not be done
without separate operator authorization:

```text
S27_V2_HANDOFF_FOLDER_CLEAN_AND_COPY
S27_V2_EXTERNAL_AUDIT_EXECUTION_BY_OPERATOR_ASSISTANCE
S27_V2_FILE_OR_DATA_CONTRACT_REPLAY_RUNNER
S27_V2_REALISTIC_LOCAL_ROW_REPLAY
S27_V2_DIAGNOSTIC
S27_V2_BACKTEST
S27_V2_EXTERNAL_REAUDIT_OF_TARGET_POSITION_REMEDIATION
S27_V2_EXTERNAL_REAUDIT_OF_CAP_EDGE_REMEDIATION
S27_V2_EXTERNAL_REAUDIT_OF_MARKET_FALLBACK_REMEDIATION
S27_V2_OOS
S27_V2_LOCKBOX
S27_V2_FORWARD
S27_V2_GIT_STAGE_COMMIT_PUSH_PR
S27_V2_PROMOTION_OR_ALPHA_INTERPRETATION
```

## Next Authorization-Ready Options

The next possible operator-authorized actions are:

1. External audit handoff preparation: clean the GPT folder and copy the
   selected packet files, with the prompt provided in the agent response.
2. Git preparation/publication: stage, commit, and push the current S27 v2
   process/code/test artifacts.
3. File/data-contract runner implementation: build a local-only parser/runner
   that satisfies `CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md`.

Each option requires explicit operator authorization before action.

## Current Gate Decision

Current state:

```text
S27_V2_SOURCE_LOCK_IMPLEMENTATION_AND_SYNTHETIC_REPLAY_PRIMITIVES_LOCAL_AUDIT_COMPLETE_PROCESS_READY_FOR_NEXT_OPERATOR_GATE
```

Still not authorized:

```text
NO_PROVIDER_API
NO_DATA_DOWNLOAD
NO_FILE_PARSING
NO_DIAGNOSTIC
NO_BACKTEST
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_TUNING
NO_ALPHA_CLAIM
NO_PROMOTION
NO_GIT_STAGE_COMMIT_PUSH_PR
NO_HANDOFF_FOLDER_CLEAN_OR_COPY
```

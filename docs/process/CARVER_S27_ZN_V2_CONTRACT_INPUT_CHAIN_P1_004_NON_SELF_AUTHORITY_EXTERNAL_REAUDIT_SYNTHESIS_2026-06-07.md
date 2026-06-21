# S27 ZN V2 Contract/Input Chain P1-004 Non-Self Authority External Re-Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_NON_SELF_AUTHORITY_EXTERNAL_REAUDIT_SYNTHESIS_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Source

GPT Extended Pro external hostile re-audit of:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_NON_SELF_AUTHORITY_EXTERNAL_REAUDIT_HANDOFF_2026-06-07.md
```

## Verdict

```text
FAIL
```

The external audit found no P0 and no P2 findings, but one P1 remains open.

## Closed Items

The audit marked the following prior P1-004 findings closed in the narrow scope:

```text
P1-004-B source-input manifest citing one selection bundle while consuming another embedded role tuple
P1-004-C runtime-history and level-compatibility row/locator hashes not bound to source-manifest authority
P1-004-D validation and PnL active authority maps collapsed distinct upstream authorities
```

## Remaining P1

### P1-004-A

Status:

```text
NOT_CLOSED
```

Finding:

```text
The selected-row authority was moved into SourceRowSelectionAuthorityContract, but that authority object is still caller-supplied and internally self-authenticating one layer up.
```

External audit concern:

```text
A forged packet can still make SourceRowSelectionAuthorityContract, expected maps, role contracts, and bundle top-level hashes internally agree without proving the selected rows are members of an active source-row batch, that locators are members of an active row-locator contract, or that the authority hash is anchored to active trust-root/evidence-manifest authority.
```

Affected surface:

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/trust_root.py
src/carver/spine/s27_v2_replay/runner.py
```

## Required Fix Direction

The next patch should make source-row-selection authority non-self-authenticating.

Acceptable fix patterns identified by the external audit:

```text
carry validated upstream authority objects and derive/verify selected-row and selected-locator maps from those objects
or add SOURCE_ROW_SELECTION_AUTHORITY as a first-class active evidence/trust-root artifact and require source_row_selection_authority_hash to equal the active evidence-manifest value
also add row-membership and locator-membership proof hashes by locked input role
```

## Gate

Parser/file replay implementation may not proceed.

The next safe gate is a narrow S27_V2 P1-004-A source-row-selection authority-anchor patch only, followed by local hostile audit and then external GPT re-audit if local audit passes.

## Non-Authorization

This synthesis authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.

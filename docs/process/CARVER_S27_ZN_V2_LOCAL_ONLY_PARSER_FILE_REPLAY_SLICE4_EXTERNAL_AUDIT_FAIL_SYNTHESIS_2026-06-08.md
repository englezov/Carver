# S27_V2 Local-Only Parser/File Replay Slice 4 External Audit Fail Synthesis

Date: 2026-06-08

Status:

```text
EXTERNAL_AUDIT_FAIL_PACKET_COMPLETENESS_ONLY
```

## Scope

External hostile audit of the `S27_V2_LOCAL_ONLY_PARSER_FILE_REPLAY_IMPLEMENTATION_SLICE_4` handoff packet.

## Verdict

The external audit returned:

```text
FAIL
```

## Failure Class

The failure was packet-completeness related, not a code-path P0/P1 execution finding.

The auditor reported that the mounted attachment set did not include the current:

```text
src/carver/spine/s27_v2_replay/position_input_contract.py
```

This prevented verification of the desired-position input authority route, public fail-closed validator, expected-source-map binding, dependency binding, and hash-content binding.

## Findings

The audit reported:

```text
No P0 findings.
One P1 packet-completeness finding.
No separately classified P2 findings.
One P3 future re-audit note.
```

P1:

```text
P1-001 - Current packet omits the desired-position input contract module required to audit Slice 4 authority routing.
```

P3:

```text
Future re-audit should also check direct downstream builder anchoring for build_position_contract(...) and build_order_contract(...).
```

## Partial Checks Passed

The audit found no forbidden provider/API, download, new data acquisition, OOS/Lockbox/Forward, backtest, result-scored run, result interpretation, PnL/result evaluation, tuning, adapter, deployment, trading, promotion, Git/PR, or source-faithful replay evidence surface in the mounted files.

The audit also observed the intended Slice 4 chain in the mounted `local_replay.py`:

- Slice 4 rebuilds Slice 3 and constructs forecast input, forecast contract, position input, position contract, order input, and order contract.
- Forecast input validation derives authority from Slice 3 runtime-history input and runtime-history contract.
- Forecast contract validation binds runtime-history/source-manifest authority and component/branch/invariant dependencies.
- Order input and order contract validation bind order authority to position input/position contract and content-bind order dependencies/policies.
- Focused tests include Slice 4 construction, public fail-closed validators, forged forecast authority map rejection, forged position dependency rejection, forged order transition policy rejection, and forged top-level policy hash rejection.

## Required Follow-Up

Prepare a corrected external re-audit packet that includes the exact current `position_input_contract.py` used by `local_replay.py` and the focused tests.

The re-audit must specifically verify:

1. `PositionInputContractBundle.validate()` fails closed.
2. The authority-aware path validates forecast input and forecast contract before accepting expected maps.
3. Position input expected-source maps derive from active forecast artifacts/contracts.
4. Component and invariant dependency bindings use active input/derived component hashes.
5. `position_input_set_hash` and `position_input_contract_hash` are content-bound.
6. Direct stale/forged position input cannot be accepted by Slice 4 artifact validation.

## Gate Decision

Parser/file replay implementation may not proceed to the next narrow slice from this failed packet.

Even after a corrected external `PASS`, the next implementation slice may proceed only after separate explicit operator authorization.

## Non-Authorization

This synthesis does not authorize provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, diagnostics outside local verification, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git staging, Git commit, Git push, PRs, or source-faithful replay evidence claims.

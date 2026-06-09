# S27 ZN V2 Executable Replay-Ledger Implementation Planning Gate

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_EXECUTABLE_REPLAY_LEDGER_IMPLEMENTATION_PLANNING_GATE_NOT_IMPLEMENTATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

This planning record defines the minimal next implementation steps required to
move from audited inert construction/contract artifacts into deterministic
local replay ledgers.

This record does not authorize implementing or running those ledgers.

## Entry Conditions

The planning gate follows these completed checkpoints:

- S27 ZN book source lock:
  `docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md`
- oldest local ZN declared input pack:
  `docs/researchops/s27_v2_local_replay_inputs/ZN/20260608_oldest_dev_recon_znh2_20220103_declared_pack`
- controlled local replay construction output:
  `docs/researchops/s27_v2_local_replay_runs/ZN/20260608_controlled_local_replay_construction_declared_pack`
- controlled construction run record:
  `docs/process/CARVER_S27_ZN_V2_CONTROLLED_LOCAL_REPLAY_CONSTRUCTION_RUN_RECORD_2026-06-08.md`
- controlled construction local hostile audit:
  `docs/process/CARVER_S27_ZN_V2_CONTROLLED_LOCAL_REPLAY_CONSTRUCTION_RUN_LOCAL_AUDIT_RESULT_2026-06-08.md`

The controlled construction run produced inert construction/contract artifacts
only. It did not produce replay ledgers, fills, cost ledgers, PnL rows,
backtest results, result-scored artifacts, or source-faithful evidence.

Key construction hashes:

```text
run manifest SHA256: 3B44823EB93CF9FE612C8419E6A3262E7D54F2CCC3F3396CB29CD7250B698D10
trusted bundle contract hash: E618E39C858AABF7DB72DA53DD8735F6ED528A4733EF881F3479C6502DE80B31
validation contract bundle hash: EC3C431C241E6BB433E0961685ECBEBE358B8F826D370EB76F064ABC63C21AD3
construction contract hash: 17EFDBF499A2EDA953C7996FC33F7721E56E39D3770A190E96EF906A39487F96
```

## Planning Conclusion

The next implementation should be one consolidated executable ledger phase, not
another one-file-at-a-time gate.

The first executable phase should not try to force a nonblocked strategy result
from the oldest development input pack. That pack contains one declared row per
required row family, which is enough to prove declared-file hashing, parsing,
source-row authority binding, and construction artifact assembly. It is not
enough by itself to honestly compute the full S27 runtime history required by
the book lock:

- EWMA5 daily equilibrium state;
- EWMAC(16,64) daily trend state;
- annual percentage sigma and price-risk bridge;
- relative volatility `V`;
- expanding/admissible quantile `Q`;
- EWMA10 volatility multiplier `M`;
- nonzero trend and mean-reversion sign handling;
- full working-limit lifecycle through orders and fills;
- numeric commission, spread, multiplier, currency, tick, session, and roll
  policy evidence.

Therefore the first executable replay-ledger phase should implement
deterministic ledgers that fail closed on unresolved or insufficient inputs,
rather than emitting fabricated forecast, order, fill, cost, or PnL rows.

## Minimal Next Implementation Phase

Recommended phase name:

```text
S27_V2_LOCAL_ONLY_EXECUTABLE_REPLAY_LEDGER_IMPLEMENTATION_PHASE_1_FAIL_CLOSED
```

The phase should be limited to the audited declared ZN input pack and the
controlled construction artifacts. It should construct deterministic local
ledger surfaces only where inputs are sufficient, and it should emit explicit
fail-closed validation/provenance outputs where inputs are insufficient.

Required phase outputs:

1. A replay-ledger run manifest bound to the controlled construction run hash.
2. A provenance/hash ledger binding input-pack hashes, construction-artifact
   hashes, source-row hashes, and any emitted executable ledger hashes.
3. A daily/hourly level-compatibility ledger row only if same-level or bridged
   compatibility can be proved from declared rows; otherwise a fail-closed
   compatibility gate.
4. A runtime-history ledger row only if strict-prior EWMA, EWMAC, sigma, and
   V/Q/M state requirements are satisfied; otherwise a fail-closed runtime
   history gate.
5. Forecast, desired-position, order, transition, fill, cost, and PnL ledger
   rows only if every upstream ledger and policy gate passes.
6. A validation ledger that records required artifact-family coverage and all
   unresolved gates.
7. A trusted-bundle output that remains non-evidence until local and external
   audit pass.

Expected result for the current one-row development pack:

```text
FAIL_CLOSED_EXECUTABLE_REPLAY_LEDGER_SURFACE_PASS_NO_RESULT
```

This means the machinery can prove that it refuses to compute source-native S27
forecast/order/PnL rows when the required history or policy evidence is absent.
It is not a backtest result, not a scored run, not PnL interpretation, and not
source-faithful evidence.

## Required Implementation Guards

The future implementation must:

- read only the audited declared input pack and controlled construction output
  named in the operator authorization;
- verify SHA256 hashes before using any row or artifact;
- use completed bars only;
- preserve strict-prior daily/hourly alignment;
- reject undeclared files, undeclared row families, undeclared construction
  artifacts, and stale hashes;
- derive every executable ledger input from validated upstream authority, not
  caller-supplied self-authenticating maps;
- emit no forecast/order/fill/cost/PnL row if any upstream gate is unresolved;
- preserve all no-provider/no-download/OOS/Lockbox/Forward/backtest/Git
  non-authorizations;
- keep result interpretation and source-faithful evidence claims blocked until
  local and external audits explicitly pass.

## Gates That Must Remain Fail-Closed

The executable phase must fail closed on:

- insufficient daily history for EWMA5 and EWMAC(16,64);
- unresolved annual percentage sigma estimator source;
- insufficient history for V/Q/M;
- incompatible daily/hourly price levels;
- zero-sign cases not source-locked;
- unresolved ZN tick rounding;
- unresolved working-limit lifecycle and overnight reset policy;
- unresolved roll bridge or roll/order interaction;
- unresolved session gap or holiday/early-close handling;
- missing numeric commission, spread, multiplier, currency, or deflation
  evidence;
- stale evidence manifest or superseded construction artifacts.

## Future Nonblocked Replay Prerequisites

A later nonblocked replay phase, if desired, will require a separately audited
declared input pack with enough local daily/hourly history and policy evidence
to compute the book-locked S27 path without these fail-closed gates. That later
phase would still not be a backtest unless explicitly authorized as such.

## Recommended Next Authorization Prompt

```text
Operator authorizes S27_V2_LOCAL_ONLY_EXECUTABLE_REPLAY_LEDGER_IMPLEMENTATION_PHASE_1_FAIL_CLOSED, after controlled local replay construction PASS and local hostile audit PASS, limited to implementing deterministic fail-closed executable replay-ledger surfaces for the audited declared ZN input pack and controlled construction artifacts.

This authorizes Codex to read only the declared ZN input pack and controlled construction output already named in the process records, verify SHA256 hashes, construct provenance/hash and validation ledgers, construct level-compatibility and runtime-history ledger rows only where inputs are sufficient, and explicitly fail closed on insufficient history, unresolved sigma/V/Q/M, tick, session, roll, cost, multiplier, currency, initial-state, or working-order lifecycle gates rather than emitting fabricated forecast, position, order, fill, cost, or PnL rows.

This also authorizes focused local verification tests, local hostile audits with subagents after meaningful checkpoints, and narrowly scoped follow-up patches for local P0/P1/P2 findings inside this exact fail-closed executable-ledger phase.

No provider/API, downloads, new data acquisition, OOS/Lockbox/Forward, backtests, result-scored runs, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git staging/commit/push/PR, or source-faithful evidence claim.
```

## Non-Authorization

This planning gate authorizes no implementation, no ledger run, no provider/API
access, no downloads, no new data acquisition, no OOS, no Lockbox, no Forward,
no backtests, no result-scored runs, no result interpretation, no PnL/result
evaluation, no tuning, no adapter work, no deployment, no trading, no
promotion, no Git actions, and no source-faithful evidence claim.

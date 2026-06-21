# Carver S27 ZN V2 GPT Reaudit Adjacent Limit Provenance Remediation

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_V2_ADJACENT_LIMIT_PROVENANCE_REMEDIATION_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

## Scope

This record covers the local response to the GPT Extended Pro re-audit that followed the limit/session provenance remediation packet.

Authorized work was limited to local implementation and synthetic-test repair. This record authorizes no provider/API use, no downloads, no parser/file replay, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no Git staging, no commit, and no push.

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Re-Audit Findings Addressed

GPT reported that the prior patch fixed the named 50-test items but left these public-boundary blockers:

- a public limit plan could omit one of the source-required adjacent limit sides;
- direct fill session/raw-symbol binding was caller-asserted rather than plan-bound;
- gap-zero no-order working states could carry arbitrary positions without forecast context;
- public cost and PnL helpers accepted externally manufactured rows without execution provenance.

## Local Remediation

The S27 V2 implementation slice now:

- requires forecast-context validation for every order plan, including gap-zero no-order plans;
- recomputes the complete source-required adjacent limit set and rejects public limit plans that omit or add sides;
- adds raw-symbol and session-id provenance fields to `S27V2OrderPlan`;
- requires direct fills to match plan-bound raw symbol and session id;
- rejects arbitrary no-context no-order states through the same order-plan validation path;
- adds fill, cost, and PnL source-status gates so externally constructed rows fail closed unless they come through validated builders.

## Test Coverage Added

The synthetic suite now includes regression coverage for:

- public limit plans omitting a source-required adjacent limit side;
- direct fill with an order plan lacking raw-symbol/session binding;
- arbitrary gap-zero no-order working states without forecast context;
- external fill rows passed directly to cost ledgers;
- external/unproven cost rows passed to PnL ledgers.

Verification run:

```text
python -m pytest tests\test_s27_v2_source_lock_synthetic.py -q
54 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py
PASS
```

## Evidence Note

Earlier records reporting 31, 36, 39, 44, or 50 synthetic tests are superseded for this local slice by this remediation record. No replay, parser, diagnostic, backtest, or result interpretation may rely on stale evidence counts or old hashes.

## Remaining Gates

This does not make S27 V2 replay-ready or backtest-ready. Remaining gates include:

- non-forgeable replay provenance for source rows and forecast contexts;
- ZN tick-size and limit-price rounding source lock;
- next-session overnight target recomputation design;
- persistent working-limit lifecycle design across normal no-fill hours;
- source-locked nonzero-position roll bridge;
- Strategy 3 sigma provenance;
- daily/hourly level compatibility proof;
- session/roll calendar proof;
- spread-unit and cost proof;
- local source-row replay over real cached ZN rows after separate authorization;
- external hostile re-audit before any diagnostic or backtest authorization.

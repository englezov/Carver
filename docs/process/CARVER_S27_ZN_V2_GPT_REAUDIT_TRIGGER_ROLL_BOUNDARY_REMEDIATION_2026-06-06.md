# Carver S27 ZN V2 GPT Reaudit Trigger And Roll Boundary Remediation

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_V2_TRIGGER_ROLL_BOUNDARY_REMEDIATION_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

## Scope

This record covers the local response to the GPT Extended Pro re-audit that followed the public-boundary remediation packet.

Authorized work was limited to local implementation and synthetic-test repair. This record authorizes no provider/API use, no downloads, no parser/file replay, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no Git staging, no commit, and no push.

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Re-Audit Findings Addressed

GPT reported that the prior patch fixed the intended builder path but left these blockers:

- `"OVERNIGHT_GAP_MARKET_RESET"` could still be injected into the public fill path as an allowed market trigger;
- allowed market-trigger strings were not bound to source conditions;
- normal one-hour transition could accept a working state carrying an overnight market trigger;
- nonzero-position roll boundary could emit raw-symbol-crossing PnL without a source-locked roll bridge;
- completion evidence with 36 tests and old hashes was stale relative to the current local slice.

## Local Remediation

The S27 V2 implementation slice now:

- removes `"OVERNIGHT_GAP_MARKET_RESET"` from fillable market-order trigger allowlist;
- carries `S27V2ForecastContext` provenance through `S27V2OrderPlan` and `S27V2WorkingOrderState`;
- requires market-order plans to include forecast-context provenance;
- validates trigger-specific source conditions:
  - large-gap trigger requires an absolute desired-position gap greater than one;
  - buy/sell cap-bound triggers require matching cap-side forecast state and one-contract gap;
  - adjacent/unpriceable triggers require one-contract gap and an unpriceable desired target;
- rejects nonzero-position roll-boundary PnL until a source-locked roll bridge exists.

## Test Coverage Added

The synthetic suite now includes regression coverage for:

- allowed but semantically wrong market trigger;
- direct fill with `"OVERNIGHT_GAP_MARKET_RESET"`;
- market plan missing forecast-context provenance;
- normal transition carrying an overnight market trigger;
- nonzero-position roll boundary without roll bridge.

Verification run:

```text
python -m pytest tests\test_s27_v2_source_lock_synthetic.py -q
44 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py
PASS
```

## Evidence Note

Earlier completion evidence that reports 36 or 39 synthetic tests is superseded for this local slice by this remediation record. No replay, parser, diagnostic, backtest, or result interpretation may rely on stale evidence counts or old hashes.

## Remaining Gates

This does not make S27 V2 backtest-ready. Remaining gates include:

- next-session overnight target recomputation design;
- persistent working-limit lifecycle design across normal no-fill hours;
- source-locked nonzero-position roll bridge;
- Strategy 3 sigma provenance;
- daily/hourly level compatibility proof;
- session/roll calendar proof;
- spread-unit and cost proof;
- local source-row replay over real cached ZN rows after separate authorization;
- external hostile re-audit before any diagnostic or backtest authorization.

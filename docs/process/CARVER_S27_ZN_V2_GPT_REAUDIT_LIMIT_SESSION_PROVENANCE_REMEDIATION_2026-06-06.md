# Carver S27 ZN V2 GPT Reaudit Limit Session Provenance Remediation

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_V2_LIMIT_SESSION_PROVENANCE_REMEDIATION_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

## Scope

This record covers the local response to the GPT Extended Pro re-audit that followed the trigger and roll-boundary remediation packet.

Authorized work was limited to local implementation and synthetic-test repair. This record authorizes no provider/API use, no downloads, no parser/file replay, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no Git staging, no commit, and no push.

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Re-Audit Findings Addressed

GPT reported that the prior patch fixed the intended builder path but left these public-boundary blockers:

- `S27V2ForecastContext` could carry non-source-faithful scalar and trend/sign combinations;
- limit-order plans did not require forecast-context provenance;
- limit-order prices were not validated against source-implied target prices;
- direct fill could bypass raw-symbol, session, EOD, overnight, and roll facts;
- direct roll-boundary transition could carry a nonzero position across raw-symbol change;
- stale `_overnight_gap_market_fills()` could still produce stale-target market fills if called directly.

## Local Remediation

The S27 V2 implementation slice now:

- requires `S27V2ForecastContext.scalar` to match the S27 source-lock scalar;
- rejects uptrend contexts with short capped forecasts and downtrend contexts with long capped forecasts;
- requires forecast-context provenance for every order-bearing plan, including limit plans;
- validates every limit-order price against `implied_price_for_target_position()`;
- requires direct fills to be explicitly bound to normal one-hour same-session and same-raw-symbol facts;
- rejects direct nonzero-position roll-boundary transitions until a source-locked roll bridge exists;
- makes `_overnight_gap_market_fills()` fail closed pending next-session desired-position recomputation.

## Test Coverage Added

The synthetic suite now includes regression coverage for:

- scalar and trend/sign forecast-context conflicts;
- limit plans missing forecast-context provenance;
- limit prices not matching source-implied target prices;
- direct fill raw-symbol and session changes;
- direct nonzero-position roll-boundary transition;
- direct stale overnight gap market helper invocation.

Verification run:

```text
python -m pytest tests\test_s27_v2_source_lock_synthetic.py -q
50 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py
PASS
```

## Evidence Note

Earlier records reporting 31, 36, 39, or 44 synthetic tests are superseded for this local slice by this remediation record. No replay, parser, diagnostic, backtest, or result interpretation may rely on stale evidence counts or old hashes.

## Remaining Gates

This does not make S27 V2 backtest-ready. Remaining gates include:

- non-forgeable replay provenance for source rows and forecast contexts;
- next-session overnight target recomputation design;
- persistent working-limit lifecycle design across normal no-fill hours;
- source-locked nonzero-position roll bridge;
- Strategy 3 sigma provenance;
- daily/hourly level compatibility proof;
- session/roll calendar proof;
- spread-unit and cost proof;
- local source-row replay over real cached ZN rows after separate authorization;
- external hostile re-audit before any diagnostic or backtest authorization.

# Carver S27 ZN M1 Ladder Dev/Reconciliation Backtest Opus 4.7 Hostile Audit Result

Date: 2026-05-31

Status:

```text
OPUS_4_7_HOSTILE_AUDIT_RESULT_PRESERVED
```

## Audited Scope

Opus 4.7 performed a read-only hostile source-faithfulness and governance audit of the Carver S26/S27 machine and the S27 ZN 2022-2023 Development/Reconciliation M1-style ladder backtest packet.

Packet reviewed:

```text
GPT/00_Carver.pdf
GPT/01_GOVERNANCE_SCOPE_AND_SOURCE_AUTHORITY.md
GPT/02_S26_S27_SOURCE_ATOMS_AND_MACHINE_PATH.md
GPT/03_S27_ZN_2022_2023_BACKTEST_ARTIFACT_SUMMARY.md
GPT/04_HOSTILE_AUDIT_CHECKLIST_AND_VERIFICATION_EVIDENCE.md
```

Audit mode:

```text
READ_ONLY
NO_EDITS
NO_CODE_RUN
NO_PROVIDER_ACCESS
NO_NEW_DATA
NO_DIAGNOSTICS
NO_NEW_BACKTESTS
NO_POSITIONS_CREATED
NO_GIT_OR_REMOTE_OPERATIONS_BY_OPUS
NO_PROMOTION
```

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_ZN_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA_WITH_NONBLOCKING_DOCUMENTATION_FINDINGS
```

## Pass Scope

```text
STRATEGY: Strategy 27, safer fast mean reversion
INSTRUMENT: ZN / US 10-year Note futures
LANE: SOURCE_NATIVE_FUTURES
WINDOW_REQUESTED: 2022-01-01 through 2023-12-31
WINDOW_EFFECTIVE: 2022-01-04 through 2023-12-29
CAPITAL: 100000 USD
POSITION_STYLE: M1-style Part-One position-management ladder, forecast-scaled, integer contracts, NEAREST rounding
RISK_PARAMETERS: target_risk=0.20, IDM=1.0, instrument_weight=1.0, FX=1.0, ZN_multiplier=1000.0, forecast_to_position_divisor=10.0
RUNTIME_GATE: strict-prior daily runtime, runtime_lag_days > 0 AND <= 10
COSTS: ETF public per-side commission only as a placeholder approximation, no spread, no slippage, no fill-quality, no margin, no prop-firm rules
STATUS: Development/Reconciliation only, NOT alpha, NOT production, NOT deployment
SUPERSESSION: prior stale-runtime result is fail-closed and cannot be cited as a valid S27 ZN result
LOCAL_EXTENDED_DAILY_RUNTIME: Dev/Reconciliation-only support stitch, NOT production continuous-contract authority
```

## Opus Findings Summary

Critical findings:

```text
NONE
```

High findings:

```text
NONE
```

Medium non-blocking findings:

```text
M-01: Combine-warning page citation missing; add Carver p.492 citation.
M-02: 2022-01-03/4 blocked-row provenance requires clearer timestamp-level disclosure.
M-03: ETF fee label is asymmetric for a futures-native lane; relabel or caveat as placeholder approximation.
M-04: S13-style V/Q/M label must pin S27 p.502 restatement, exact M EWMA span, and Q lookback/scope.
```

Low non-blocking findings:

```text
L-01: S26 chapter range should include p.475.
L-02: No FDM/single-rule atom should be cited or reframed as architectural consequence.
L-03: Forecast cap +/-20 has dual provenance and should cite original framework source.
L-04: runtime_lag_days unit should be explicit.
L-05: Local extended daily runtime cadence should be explained.
L-06: Portfolio sleeve/standalone wording should map to Carver's traded-independently/in-parallel language.
L-07: Per-side commission constant should be declared as an explicit parameter.
L-08: Position-machinery parameters need page-of-origin citations.
L-09: roll_transition_fee_sides rule should be explained.
L-10: M1-style should be glossed or renamed to Part-One position-management ladder wording.
```

## What Remains Unauthorized

This Opus pass does not authorize:

```text
provider API access
new data download
new market-row parsing
new diagnostics
new backtests beyond the artifacts already created
new forecast generation beyond the stated S27 forecast rows
new position calculation beyond the stated ladder rows
new cost modelling beyond the placeholder commission approximation
carry sleeves
trend sleeves
forecast-combination with daily Parts One/Two/Three strategies
OOS
Lockbox
Forward
deployment
live trading or paper trading
promotion of local extended daily runtime to production continuous-contract authority
promotion of this single-instrument result to alpha or portfolio evidence
CFD adapter use
old QuantLab_v3 active-pipeline use
```

## Next Documentation Closure Items

Before any later promotion-oriented gate, preserve the non-blocking fixes:

```text
1. Add p.492 citation for the do-not-combine warning.
2. Disclose the four blocked dependency timestamps or the pre-readiness trim rule.
3. Relabel/caveat the ETF commission approximation.
4. Pin S27 V/Q/M source details and implementation span/lookback.
5. Define runtime_lag_days unit.
6. Cite position-machinery source pages.
```

This record is preservation of the Opus hostile audit result only. It is not a new strategy authorization, data authorization, diagnostics authorization, backtest authorization, deployment authorization, trading authorization, or promotion.

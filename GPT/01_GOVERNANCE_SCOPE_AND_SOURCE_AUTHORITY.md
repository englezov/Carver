# Carver S26/S27 Machine And Backtest Audit Packet - Governance, Scope, Source Authority

Status:

```text
OPUS_4_7_HOSTILE_AUDIT_PACKET_GOVERNANCE_SCOPE_NOT_AUTHORIZATION
```

Packet date: 2026-05-31

## Packet Contents

This GPT folder is intended to contain exactly:

```text
00_Carver.pdf
01_GOVERNANCE_SCOPE_AND_SOURCE_AUTHORITY.md
02_S26_S27_SOURCE_ATOMS_AND_MACHINE_PATH.md
03_S27_ZN_2022_2023_BACKTEST_ARTIFACT_SUMMARY.md
04_HOSTILE_AUDIT_CHECKLIST_AND_VERIFICATION_EVIDENCE.md
```

The audit prompt is not stored in this folder. It is supplied separately by the operator.

## Audit Target

Hostile read-only audit of the S26/S27 source-faithful machine and the corrected S27 ZN 100k Development/Reconciliation backtest path.

Audit target status:

```text
PASS_S27_ZN_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA
```

Corrected backtest scope:

```text
STRATEGY: Strategy 27, safer fast mean reversion
INSTRUMENT: ZN / US 10-year Note futures
LANE: SOURCE_NATIVE_FUTURES
WINDOW_REQUESTED: 2022-01-01 through 2023-12-31
WINDOW_EFFECTIVE: 2022-01-04 through 2023-12-29
CAPITAL: 100000 USD
POSITION_STYLE: M1-style Carver forecast-to-position ladder
COSTS: ETF public per-side commission only
STATUS: Development/Reconciliation only, not alpha, not production
```

## Source Authority

Primary source authority:

```text
00_Carver.pdf
```

Source sections to verify directly in the book:

```text
Part Four framing: p.475
Strategy twenty-six: Fast mean reversion: pp.476-489
Strategy twenty-seven: Safer fast mean reversion: pp.499-509
S26 equilibrium/raw/scalar/cap region: pp.479-481
S27 EWMAC16 trend overlay: p.500
S27 volatility attenuation / safer variant: pp.501-508
S27 trading plan: p.508
```

The packet intentionally uses small source summaries and page references rather than long copied book passages.

## Current Governance Perimeter

The active Carver workspace is:

```text
C:\Users\openclaw\Desktop\Carver
```

The archived old workspace is:

```text
C:\Users\openclaw\Desktop\QuantLab_v3
```

Old QuantLab status:

```text
ARCHIVED_OPERATIONAL_BLOB_DO_NOT_PIPELINE
```

The audit must verify that the current S26/S27 machine and corrected backtest do not rely on old active QuantLab pipelines, old CFD adapter code, CFD broker-clock assumptions, CFD symbols, old OOS/Lockbox/Forward state, deployment state, or trading state.

## Non-Authorization

This packet authorizes none of the following:

```text
provider API access
new data download
new market-row parsing
new diagnostics
new backtests
forecasts beyond the artifacts already created
new position calculations
new costs or tuning
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
deployment
trading
promotion
Git staging
commit
push
PR update/opening
remote operations
```

## Specific Governance Questions For Audit

1. Does the S26/S27 machine preserve source-native futures interpretation rather than CFD/adapted interpretation?
2. Does the S27 ZN path use the book-native ZN / US 10-year Note family rather than substituting a different market?
3. Does the corrected result remain Development/Reconciliation only?
4. Is the stale prior R2-fed result explicitly superseded and fail-closed?
5. Does any artifact imply OOS, Lockbox, Forward, production, deployment, trading, promotion, or alpha?
6. Does any wording overstate the local extended daily runtime stitch as production continuous-contract authority?
7. Are costs clearly limited to ETF per-side commission only, with spread/slippage/fill quality unresolved?


# Governance Scope And Source Authority

Status:

```text
OPUS_PACKET_FOR_S27_ZN_MECHANICAL_VERIFICATION_AUDIT_READ_ONLY
```

## Source Authority

Primary book source:

```text
00_Carver.pdf
```

Relevant book scope:

- Strategy 26: Fast mean reversion.
- Strategy 27: Safer fast mean reversion.
- Part Four framing: hourly data; fast directional strategies; no buffering; fast mean reversion tries to use limit orders where possible.
- S27 depends on S26, EWMAC(16,64) trend overlay, and V/Q/M-style volatility attenuation.

## Clean Workspace Rules

Active workspace:

```text
C:\Users\openclaw\Desktop\Carver
```

Archived old workspace:

```text
C:\Users\openclaw\Desktop\QuantLab_v3
```

The old workspace is `ARCHIVED_OPERATIONAL_BLOB_DO_NOT_PIPELINE`. It may be referenced only as read-only archaeology. It must not be treated as source-native futures authority, and its old code, broker-clock assumptions, CFD adapters, or pipeline state must not be imported into Carver.

## Lane Classification

Current S27 ZN work:

```text
SOURCE_NATIVE_FUTURES
```

The current result uses Databento GLBX.MDP3 source-native futures data for ZN only, transformed through Carver-local Development/Reconciliation artifacts. It is not a CFD lane and not a deployment lane.

The archived old QuantLab `US500` CFD result remains:

```text
CFD_DIRECT / archived anomaly only
```

It is preserved as a future investigation lead, not as proof for source-native futures.

## Current Question For Opus

The previous Opus pass recommended a mechanical verification program for the strange positive S27 ZN result. That program has now been implemented locally.

Please hostile-audit whether the implemented verification is enough to say:

```text
MECHANICALLY_VERIFIED_AT_DEVELOPMENT_RECONCILIATION_SCOPE
```

or whether it still misses a blocking bug path.

Do not judge whether the strategy is good. Audit whether the current S27 ZN backtest machinery and verification evidence are mechanically credible at Development/Reconciliation scope only.

## Hard Boundaries For This Audit

This packet requests read-only audit only.

Do not authorize or assume:

- new data download;
- provider/API access;
- market-row parsing outside the packet;
- new diagnostics or backtests;
- OOS, Lockbox, or Forward;
- tuning;
- symbol/window/cost selection after seeing results;
- strategy promotion;
- CFD adapter execution;
- old QuantLab active-pipeline use;
- deployment;
- trading;
- Git operations.

## Desired Verdict

Please produce:

```text
BLOCKING_FINDINGS: YES/NO
AUDIT_DISPOSITION: <specific disposition>
RECOMMENDED_NEXT_GATE: <single next gate>
```

Also include:

- CRITICAL/HIGH/MEDIUM/LOW findings;
- whether the scalar issue is fully resolved or still risky;
- whether input-lineage/no-lookahead checks are sufficient;
- whether roll/back-adjustment and runtime alignment checks are sufficient;
- whether independent forecast/position/PnL recomputation is independent enough;
- whether fee/episode/null-test evidence is correctly scoped;
- what remains closed.

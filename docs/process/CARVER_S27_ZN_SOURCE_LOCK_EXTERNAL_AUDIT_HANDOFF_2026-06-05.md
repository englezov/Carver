# Carver S27 ZN Source Lock External Audit Handoff

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_SOURCE_LOCK_HANDOFF_REFRESHED_AFTER_REAUDIT_EDITS
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the external hostile-audit handoff for the S27 ZN v2 source-lock gate.
This is a process record only. It authorizes no implementation, no parsing, no
provider/API access, no data download, no diagnostic, no backtest, no OOS,
no Lockbox, no Forward, no adapter work, no deployment, no trading, no Git
staging, no commit, no push, and no PR.

## Gate

The next required gate is an external source-faithfulness audit of:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
```

against:

```text
Carver.pdf
```

The source lock was later re-audited. The re-audit returned
`PASS_WITH_REQUIRED_EDITS`; those edits were applied to the source-lock
artifact and the handoff folder was refreshed again.

## Handoff Folder

Desktop handoff folder:

```text
C:\Users\apops\Desktop\GPT
```

Folder rule:

```text
CARVER_GPT_HOSTILE_AUDIT_HANDOFF_FOLDER_RULE_2026-06-04
```

The folder was cleaned before the original packet was placed there. After the
operator supplied Opus and GPT 5.5 Extended Pro audit results, the source-lock
artifact was revised and the folder was refreshed. After the later re-audit,
the two required edits were applied and the folder was refreshed again.

## Packet Contents

| File | Bytes | SHA256 |
|---|---:|---|
| `00_Carver.pdf` | 29669523 | `AA052B8D942767A7547ECDBB09FBED22F2412FB7B1036D24AB854738308582B6` |
| `01_CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md` | 10196 | `236F18B18BB2B4FDB1BF9E9DCA411B6A9AAE16D73524E59D27F0710E5F9F0B49` |

## Prompt Handling

The external hostile-audit prompt was provided in the agent response, not
written into this file, to preserve the project rule that large external audit
prompts are supplied in response rather than as repository files.

## Audit Questions

The external auditor is asked to decide whether the source-lock artifact is
faithful to `Carver.pdf`, especially for:

- S27 inheritance from S26.
- S26 scalar `9.3`.
- S27 scalar "around `20`" as book text, with `20.0` only as an implementation
  freeze of that approximate estimate.
- EWMA5 equilibrium.
- Hourly current price alignment.
- EWMAC(16,64) trend veto.
- V/Q/M volatility attenuation.
- Sigma bridge.
- Forecast cap and position sizing order.
- Limit-order execution, one-hour-lag assumptions, market-order cases, roll
  handling, commissions, and spread costs.
- Rejection of old target-position close-to-close full-ladder runners as
  diagnostic-only evidence.
- Missing, ambiguous, overstated, or fail-closed source decisions.

## Stop Line

Re-audit result:

```text
S27_ZN_BOOK_SOURCE_LOCK_PASSED_FOR_V2_IMPLEMENTATION_EXERCISE
```

This handoff record does not authorize provider/API access, downloads,
diagnostics, backtests, OOS, Lockbox, Forward, tuning, alpha claims, promotion,
Git staging, commit, push, PR, deployment, or trading.

Existing S27 result artifacts remain:

```text
DIAGNOSTIC_ONLY_FAILURE_MAP_MATERIAL
```

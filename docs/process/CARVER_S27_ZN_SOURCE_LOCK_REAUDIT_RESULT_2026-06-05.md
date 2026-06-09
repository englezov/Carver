# Carver S27 ZN Source Lock Re-Audit Result

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_SOURCE_LOCK_REAUDIT_PASS_WITH_REQUIRED_EDITS_APPLIED
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the operator-supplied external re-audit of the revised S27 ZN source
lock and the exact follow-up edits applied. This is a process record only. It
authorizes no parsing, no provider/API access, no data download, no diagnostic,
no backtest, no OOS, no Lockbox, no Forward, no adapter work, no deployment, no
trading, no Git staging, no commit, no push, and no PR.

## Audit Input

Auditor attachment:

```text
C:\Users\apops\.codex\attachments\46b3270e-cc67-4027-994c-68a1c06c6f56\pasted-text.txt
```

SHA256:

```text
7F161CEBCAF38C6F0E0CED887EA730B4BB9CE10C1EDF02EA8653ECD1CF5F2E65
```

## Verdict

External verdict:

```text
PASS_WITH_REQUIRED_EDITS
```

The auditor found the revised lock broadly faithful to `Carver.pdf` and
accepted the central scalar treatment:

```text
S26_SCALAR = 9.3
S27_SCALAR = BOOK_ESTIMATED_AROUND_20
S27_IMPLEMENTATION_FREEZE = 20.0_NOT_SOURCE_EXACT_CONSTANT
```

The auditor required two edits before v2 code begins.

## Required Edits Applied

Source-lock artifact updated:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
```

Applied edit 1:

```text
APPLICATION_ORDER_REVISED_TO_MATCH_BOOK_LEDGER_BOUNDARY
```

The lock now states that v2 must compute the S26 raw forecast, compute
`sigma_price`, compute `risk_adjusted_forecast`, apply the EWMAC(16,64) veto to
the risk-adjusted forecast, apply volatility attenuation as
`adjusted_risk_adjusted_forecast = risk_adjusted_forecast * M`, then apply the
S27 scalar, forecast cap, optimal position, and S26 execution machinery.

Applied edit 2:

```text
SIGMA_PRICE_BRIDGE_REVISED_TO_PREVIOUS_COMPLETED_DAILY_CLOSE_CURRENT_TRADED_CONTRACT
```

The lock now states that:

```text
sigma_price = previous_completed_daily_close_current_traded_contract * annual_percentage_sigma / 16
```

and fail-closes if the bridge uses a same-hour price or an incompatible
back-adjusted equilibrium level without a row-level equivalence proof.

## Remaining Boundaries

The re-audit confirms these remain fail-closed before scoring or result
interpretation:

- roll, session, and working-order state ambiguity;
- `Q` causality and no future volatility distribution;
- zero-sign cases for trend and mean-reversion signs;
- capacity and speed-limit eligibility;
- execution realism;
- cost boundary between limit-order commission-only fills and market-order
  commission-plus-normal-spread fills.

## Gate Decision

After the two required edits were applied, the source-lock gate is sufficient
to begin S27 v2 code as a source-lock implementation exercise only.

Current gate:

```text
S27_ZN_BOOK_SOURCE_LOCK_PASSED_FOR_V2_IMPLEMENTATION_EXERCISE
```

Still not authorized by this record:

```text
NO_PROVIDER_API
NO_DATA_DOWNLOAD
NO_BACKTEST
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_TUNING
NO_ALPHA_CLAIM
NO_PROMOTION
NO_GIT_STAGE_COMMIT_PUSH_PR
```

Existing S27 result artifacts remain:

```text
DIAGNOSTIC_ONLY_FAILURE_MAP_MATERIAL
```

# Carver S27 GPT 5.5 Extended Pro Backtest Remediation Audit Result

Date: 2026-06-04

Mode: GPT 5.5 Extended Pro hostile audit over the pushed S27 corrected first-window backtest remediation package.

GitHub audit target:

```text
Repository: https://github.com/englezov/Carver
Branch: codex/carver-strategy-portfolio-opus-checkpoint
Commit: 2f8c69606e0ba79c7e511332406dd2d1eaf6dd7a
```

## Verdict

```text
PASS_WITH_LIMITATIONS
```

The remediation looks legitimate for the declared DEV/RECON unit/no-cost package. The orphan was preserved and quarantined, not deleted; the corrected runner does not read or write it; the current SHA manifest is consistent with declared package outputs; the blocked dependency ledger is fixed and headered; and the current result is bounded as no-cost unit plumbing, not alpha.

## Critical

None found.

The audit did not find evidence that the remediation deleted strategy evidence, laundered old output as new output, used provider/API access, ran OOS/Lockbox/Forward, promoted the result, or silently depended on the quarantined orphan file.

## High

None found.

The corrected runner's declared dependencies are the source hourly CSV plus four corrected runtime ledgers:

```text
S26 sigma
S26 daily EWMA5 equilibrium
S27 daily EWMAC16/64 trend
S27 daily ten-year V/Q/M volatility
```

The corrected runner does not read `daily_runtime_rows`.

## Medium Finding 1

Finding:

```text
"the result is the same" is only partially proven by the handoff package
```

Reason:

The remediation record says the authorized corrected backtest was rerun after remediation and produced the same headline status and row counts. The re-audit confirms the current status remains:

```text
PASS_RETARGETED_S27_ZN_DEV_RECON_UNIT_PLUMBING_NO_COST_BACKTEST_NOT_ALPHA
```

with:

```text
s27_forecast_rows: 11775
backtest_rows: 11774
blocked_dependency_rows: 0
position/alignment/continuous rows: 11775
inactive rows: 9095
source rows: 20870
gross_no_cost_pnl_usd: 531.25
```

However, the pushed handoff package did not include a side-by-side pre-hygiene/post-hygiene hash comparison for the same corrected run.

Remediation recorded after audit:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest/hashes/20260604_S27_BACKTEST_CORRECTION_AND_HYGIENE_HASH_COMPARISON.json
```

Limitation:

The pre-hygiene values are recorded retrospectively from the active Codex terminal transcript rather than from a committed pre-hygiene machine-readable receipt. Future remediations should write this comparison before changing package files.

## Medium Finding 2

Finding:

```text
strategy-bearing artifacts were not unchanged relative to the prior GitHub anchor
```

This is favorable to the remediation story if the concern is whether the corrected package merely repackaged the old bad result.

Old GitHub anchor:

```text
dc6324e4e0a61001c7c058ff646be9f6ee2b12e3
```

Current corrected branch head audited:

```text
2f8c69606e0ba79c7e511332406dd2d1eaf6dd7a
```

Old versus current:

```text
S27 forecast rows SHA:
old     6409165FAD733A77E1FF0E74683080C10D4AAD9A75AB5914A2E8FAB721BF1A9D
current 0FB0EF0E8A04A07EFC4110AA61405773199DBF61D9535A869C8C0D3D811E5021

unit/no-cost backtest rows SHA:
old     C7A2F1E5B58B7EB166ED34BA2A8F4C4C60CB8C9EE0A193DC3E600D4AEC4F2AAA
current 86087EC8CD3B0140D422A2999F26EC08ABF21FCDC2DD6D72D539CEBEB8E29DD1

status JSON SHA:
old     3BE7B04D947B9CC0088D8D7FD7B491506ADC346477C1111D91F8EC83FE9DD9F1
current C8CE29EA00B3DBE79197CFF1F595948D8190ACCA8D0C14A858B760BC982A0597

gross_no_cost_pnl_usd:
old     2968.75
current 531.25

s27_forecast_rows:
old     11771
current 11775

backtest_rows:
old     11770
current 11774

blocked_dependency_rows:
old     4
current 0
```

## Low Finding 1

Boundary rows are correctly caveated, but they are not external proof.

Rows such as:

```text
no_provider_api_access
no_oos_lockbox_forward
costs_fail_closed
real_m1_position_sizing_blocked
```

must be read as local runner boundary declarations, not independent OS/network/Git attestations.

## Low Finding 2

The package SHA manifest is correct for the declared output root, but it does not hash generated process docs.

This is acceptable for the package scope. For higher-assurance future runs, create a separate run-evidence manifest that includes process result docs and audit docs as extra paths.

## Explicit Answer

```text
"the result is the same" is supported only for the narrow post-remediation headline assertion in the handoff record, not as a complete byte-for-byte pre/post hygiene proof.

Against the prior GitHub anchor, the strategy-bearing result is demonstrably not the same.
```

## Follow-Up Rule

For every future remediation after a result-producing run, write a machine-readable before/after comparison before changing package files:

```text
artifact path
pre-remediation SHA256
post-remediation SHA256
row count before
row count after
allowed-change reason
```

The comparison must explicitly distinguish:

```text
old uncorrected -> corrected
corrected pre-hygiene -> corrected post-hygiene
```

## Non-Authorization

This audit result authorizes no provider/API call, no data download, no diagnostics, no backtest, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR.

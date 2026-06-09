# S27_V2 Runtime-Evidence Remediation Gate Record

Date: 2026-06-09

Status:

```text
LOCAL_ONLY_RUNTIME_EVIDENCE_REMEDIATION_GATE_LOCAL_AUDIT_PASS
```

Authorization:

```text
S27_V2_LOCAL_ONLY_RUNTIME_EVIDENCE_REMEDIATION_GATE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers local-only remediation after the first-populated S27_V2 ZN pack proved stale for V/Q/M. It is not provider/API access, not a download, not new data acquisition, not OOS, not Lockbox, not Forward, not a backtest, not a result-scored run, not result interpretation, not PnL evaluation, not tuning, not adapter work, not deployment, not trading, not promotion, not Git work, and not a source-faithful evidence claim.

## Code Changes

Touched code:

```text
src/carver/spine/s27_v2_replay/runtime_evidence_gate.py
tests/test_s27_v2_runtime_evidence_gate.py
```

The runtime-evidence gate now supports two locked local input-pack profiles:

```text
FIRST_POPULATED
RUNTIME_EVIDENCE_REMEDIATION
```

The remediation profile binds pass-like local statuses to exact local source paths, source byte SHA256s, and selected source rows before accepting:

```text
Strategy 3 sigma local prevalidated row
EWMAC(16,64) local prevalidated row
V/Q/M local prevalidated runtime row
daily/hourly level-space bridge proof hash
```

The gate remains non-result and keeps downstream emission flags false.

## New Declared Pack

Pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_runtime_evidence_recon_znm6_20260413_declared_pack
```

Support files:

```text
S27_V2_RUNTIME_EVIDENCE_REMEDIATION_DECLARED_INPUT_PACK_MANIFEST.json
S27_V2_RUNTIME_EVIDENCE_REMEDIATION_DECLARED_INPUT_PACK_PROVENANCE.md
S27_V2_RUNTIME_EVIDENCE_REMEDIATION_DECLARED_INPUT_PACK_SHA256SUMS.txt
```

Selected local overlap:

```text
decision completed hour = 2026-04-13T03:00:00Z
fill completed hour = 2026-04-13T04:00:00Z
previous completed daily current-contract row = 2026-04-12T00:00:00Z
raw symbol = ZNM6
```

Row counts:

```text
DAILY_CONTINUOUS_COMPLETED_BAR = 135
DAILY_CURRENT_CONTRACT_COMPLETED_BAR = 1
HOURLY_DECISION_COMPLETED_BAR = 8
HOURLY_FILL_COMPLETED_BAR = 8
SESSION_CALENDAR = 1
ROLL_CALENDAR = 1
COST_PARAMETER = 1
```

Manifest hash:

```text
0B8AE370B8B6EE3A31976448CABC30FE6AE658EEEF5123171BB67BF67805FEBC
```

## Evidence Disposition

Improved local runtime-evidence status:

```text
STRICT_PRIOR_DAILY_ADMISSIBILITY = PASS_LOCAL_DECLARED_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE
STRATEGY3_SIGMA_EVIDENCE = PASS_LOCAL_PREVALIDATED_RUNTIME_EVIDENCE_NOT_SOURCE_FAITHFUL
EWMAC_16_64_EVIDENCE = PASS_LOCAL_PREVALIDATED_RUNTIME_EVIDENCE_NOT_SOURCE_FAITHFUL
VQM_EVIDENCE = PASS_LOCAL_PREVALIDATED_RUNTIME_EVIDENCE_NOT_SOURCE_FAITHFUL
DAILY_HOURLY_LEVEL_BRIDGE = PASS_LOCAL_LEVEL_BRIDGE_PROOF_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE
```

Still fail-closed:

```text
TICK_ROUNDING_POLICY
MULTIPLIER_CURRENCY_POLICY
COMMISSION_SPREAD_POLICY
WORKING_ORDER_LIFECYCLE
```

The level bridge is a local level-space proof, not equality of different-hour prices. It binds selected ZNM6 daily continuous/current rows and selected ZNM6 hourly rows through zero additive adjustment.

## Verification

Focused tests:

```text
python -m pytest tests\test_s27_v2_runtime_evidence_gate.py -q
13 passed
```

Combined focused replay/evidence tests:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py tests\test_s27_v2_runtime_evidence_gate.py -q
84 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2_replay\runtime_evidence_gate.py tests\test_s27_v2_runtime_evidence_gate.py
PASS
```

Manual hash/count binding check:

```text
manifest row/source hashes and row counts bind local bytes
```

## Non-Authorization

This gate does not authorize provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, forecast/order/fill/cost/PnL/result evidence emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

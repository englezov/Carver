# S27 ZN V2 Full Scaffold-Routing P1 Runtime And Cost-Policy External Re-Audit Handoff

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_FULL_SCAFFOLD_ROUTING_P1_RUNTIME_COST_POLICY_EXTERNAL_REAUDIT_HANDOFF_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Consolidated Remediation Gate

This handoff was prepared after the local hostile audit returned `PASS` on the consolidated patch for GPT Extended Pro's two P1 findings from the full scaffold-routing external audit.

Still excluded:

```text
provider/API
downloads
parser/file replay execution
diagnostics
tests/backtests
OOS/Lockbox/Forward
git actions
adapter work
deployment
trading
promotion
result interpretation
source-faithful replay evidence claim
```

## Handoff Folder

Folder:

```text
C:\Users\apops\Desktop\GPT
```

The folder was cleaned before packet creation.

`Carver.pdf` copied:

```text
NO
```

Rationale:

```text
GPT already has the book attached in the app/library for this thread.
```

## Source Packet

Zip:

```text
S27_V2_P1_RUNTIME_COST_POLICY_AUTHORITY_REAUDIT_SOURCE_PACKET_2026-06-08.zip
```

Zip SHA256:

```text
225672A11393274F3C0419F48F645851892766FA47F553AD98B75A4C82DDFBEE
```

Zip entry count:

```text
53
```

Zip contents:

```text
src/carver/spine/m0.py
src/carver/spine/s27_v2_replay/*.py
```

Visible handoff-folder file count after packet creation:

```text
7
```

## Audit Question

The external auditor should decide whether the consolidated patch closes GPT's two P1 findings:

```text
P1-001 runtime-history level-compatibility authority routing
P1-002 cost policy, multiplier, and currency active trust/evidence authority routing
```

Specific checks:

```text
RuntimeHistoryInputContractBundle.validate_against_active_trust_authority(...) requires LevelCompatibilityInputContractBundle and LevelCompatibilityContractBundle.
Runtime history validates level-compatibility input through active trust/evidence/source-row-batch/parser-output authority before consuming runtime maps or bindings.
Runtime history validates the level-compatibility contract bundle before consuming runtime maps or bindings.
Runtime history binds cited level-compatibility hashes, source manifest, source universe, trust-root policy, source-row family hashes, and each level-compatibility input-field binding to validated upstream objects.
The new level-compatibility authority objects are routed downstream through forecast, position, order, fill, cost, PnL, validation, and trusted bundle.
Cost input calls require_evidence_manifest_matches_trust_root(...) before accepting cost expected-source maps.
Cost input derives commission/spread/multiplier/currency authority from ReplayTrustRoot rather than cost_input_policy_hash.
CostContractBundle.validate_against_policy_authority(...) binds commission, spread, multiplier, and currency policy fields to trust-root/evidence authority before PnL uses the cost contract.
PnL multiplier/currency authority derives from ReplayTrustRoot.contract_multiplier_currency_policy_hash rather than cost-contract-local hashes.
Scaffold-local cost branch, deflation, and calculation policies remain local and do not masquerade as source/policy authority.
No provider/API, download, parser/file replay, diagnostic, test/backtest, OOS/Lockbox/Forward, git, adapter, deployment, trading, promotion, result interpretation, or source-faithful evidence surface was introduced.
```

## Gate

Parser/file replay implementation must not proceed from this handoff alone. Any next implementation scaffold or execution step requires separate operator authorization.

## Non-Authorization

This handoff authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.

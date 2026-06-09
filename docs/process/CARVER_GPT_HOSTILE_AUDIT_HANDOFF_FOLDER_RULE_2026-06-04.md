# Carver Hostile Audit Handoff Folder Rule

Date: 2026-06-04

Status:

```text
PROCESS_ONLY_CARVER_HOSTILE_AUDIT_HANDOFF_FOLDER_RULE_NOT_AUDIT_EXECUTION
```

## Hostile Audit Authorization Rule

Hostile audits are pre-approved by the operator and should be done by spawning
subagents where the app supports subagent work.

Only large final audits require operator assistance. Large final audits include:

- GPT Extended Pro / GPT-5.5 with GitHub access;
- Opus 4.

Large hostile-audit prompts must be provided in the agent response, not written
into a file. Handoff files should contain only the selected source artifacts,
manifests, or evidence files needed by the external reviewer.

This pre-approval does not override separate critical-gate requirements for
data access/download/parsing, provider/API use, risky stage transitions,
credentials, GitHub publication, destructive operations, deployment, trading,
or promotion.

## GPT Extended Pro Handoff Folder Rule

The desktop folder:

```text
C:\Users\apops\Desktop\GPT
```

is the local hostile-audit handoff folder for GPT Extended Pro / GPT-5.5 through
the app.

Before preparing any hostile-audit handoff in that folder:

- clean the folder first;
- place no more than 20 files in the handoff folder;
- include only the specific files needed for the hostile audit question;
- avoid dumping broad repo trees, raw secrets, credentials, unrelated data, prior unsuitable workspace material, OOS, Lockbox, Forward, deployment, trading, or promotion artifacts unless separately and explicitly authorized;
- preserve repo-relative paths and/or a manifest so the receiving reviewer can understand file provenance;
- do not treat the handoff folder as source authority after review; source authority remains in the Carver repo artifacts.

## Opus 4 Handoff Rule

Opus 4 hostile-audit handoffs have a hard 5-file limit.

Before preparing an Opus 4 hostile-audit handoff:

- select no more than 5 focused files;
- prefer the smallest source-faithful bundle that lets Opus answer the audit question;
- include a manifest or compact instruction file only if it fits inside the 5-file limit;
- do not include broad repo dumps, secrets, credentials, unrelated data, prior unsuitable workspace material, OOS, Lockbox, Forward, deployment, trading, or promotion artifacts unless separately and explicitly authorized.

## Boundary

This rule authorizes no file deletion, no handoff execution, no audit execution,
no data access, no provider/API call, no diagnostic, no backtest, no OOS, no
Lockbox, no Forward, no CFD adapter work, no tuning, no deployment, no trading,
no promotion, no Git staging, no commit, no push, no PR, and no remote operation.

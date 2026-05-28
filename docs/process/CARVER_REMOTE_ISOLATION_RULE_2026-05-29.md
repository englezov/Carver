# Carver Remote Isolation Rule

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_REMOTE_ISOLATION_RULE_NOT_REMOTE_PUSH_AUTHORIZATION
```

## Rule

Carver must use a distinct GitHub repository.

The Carver workspace must not push to, reuse, or depend on the old QuantLab remote:

```text
https://github.com/englezov/QuantLab_v3.git
```

## Forbidden

- Do not add the old QuantLab remote to this repository.
- Do not push Carver commits to `englezov/QuantLab_v3`.
- Do not reuse old QuantLab branches, PRs, issues, GitHub Actions state, releases, tags, deployment environments, or repository secrets as Carver authority.
- Do not use old QuantLab CI or remote status as evidence for Carver.
- Do not create a remote or push Carver until the operator explicitly authorizes the final remote action.

## Required Future Remote Gate

Before the first Carver remote push:

- Confirm the local workspace is `C:\Users\openclaw\Desktop\Carver`.
- Confirm `git remote -v` does not point to `QuantLab_v3`.
- Create or select a distinct Carver GitHub repository.
- Record the chosen remote in a repo-local process artifact.
- Run the final package/source-faithfulness audit first.
- Commit all approved audit patches locally.
- Ask the operator for explicit remote-push authorization.

## Non-Authorization

This rule authorizes no remote creation, no remote configuration, no push, no PR, no deployment, no trading, no data work, no tests/backtests, no OOS, no Lockbox, no Forward, and no CFD adapter activity.

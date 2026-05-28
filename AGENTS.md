# Carver Agent Rules

Before any task in this folder, read:

1. `README.md`
2. `docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md`
3. `docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md`
4. `docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md`

Core rules:

- This folder is the clean active Carver research workspace.
- The old `C:\Users\openclaw\Desktop\QuantLab_v3` folder is archived and must not be used for active pipelines.
- Do not copy or resurrect old adapter code, old CFD broker-clock assumptions, old data-prep scripts, or stale pipeline state.
- Every future lane must declare `SOURCE_NATIVE_FUTURES`, `CFD_DIRECT`, or `CFD_ADAPTER` before data work.
- Source-native futures discovery must remain source-native and must not borrow CFD assumptions.
- CFD adapter work requires a separate explicit adapter gate after source-native behavior exists.
- Strategies from the book must be labeled as standalone candidates or source-native portfolio sleeves before interpretation.
- A portfolio sleeve failing standalone is not family death if the book frames it as portfolio material.
- Reconstruct complete book portfolios separately from individual strategy tests.
- Do not access OOS, Lockbox, or Forward data without explicit operator authorization.
- Do not run any backtest or diagnostic over 2 years without explicit operator approval.
- Use completed bars only.
- Do not tune parameters, thresholds, filters, exits, symbols, costs, or windows after seeing results.
- Do not trade, deploy, promote, or claim alpha from this workspace without explicit locked authorization.
- Carver must use a distinct GitHub repository. Do not push to or reuse the old `QuantLab_v3` remote, branches, PRs, Actions state, releases, tags, deployment environments, or secrets. See `docs/process/CARVER_REMOTE_ISOLATION_RULE_2026-05-29.md`.

For any risky action, ambiguous stage transition, data-window question, destructive operation, credential exposure risk, GitHub push, or governance conflict, stop and ask the operator.

# CARVER S27 ZN V2 Backtest-Readiness Planning Gate

Date: 2026-06-11

Status: PROCESS_ONLY_S27_V2_BACKTEST_READINESS_PLANNING_NOT_RUN_NOT_RESULT

This record is a planning gate only. It does not authorize or perform a
backtest, result-scored run, result interpretation, PnL evaluation, provider/API
access, downloads, OOS/Lockbox/Forward access, tuning, adapter work,
deployment, trading, promotion, Git actions, or source-faithful evidence claims.

## Current State

S27_V2 has reached a local positive-action machinery checkpoint for one audited
ZNM6 development/reconciliation row.

Locally passed machinery now includes:

- source-lock and source-native governance records;
- declared local input packs and byte/hash-bound manifests;
- replay construction and authority-routing scaffolds;
- runtime evidence and runtime-history executable surfaces;
- forecast executable ledger surface;
- position evidence and desired-position executable surface;
- order-plan executable surface;
- fill executable surface;
- inferred retail futures cost acceptance and actual cost executable surface;
- inferred valuation convention and declared valuation mark-row pack;
- actual PnL executable surface for the audited positive-action row;
- positive-action actual-PnL validation/provenance/trusted-bundle closure.

The locally closed positive-action row remains development/reconciliation
machinery evidence only. It is not a backtest result, not result interpretation,
not alpha evidence, and not a source-faithful replay evidence claim.

## Important Boundary

The completed positive-action chain is hard-bound to the audited ZNM6
development/reconciliation path and row evidence. It proves that the machinery
can construct one positive-action chain under byte/hash-bound local evidence.

It does not by itself prove that a generalized multi-row backtest runner is
ready. A backtest-ready surface must additionally prove:

- deterministic iteration over a locked local development window;
- strict-prior/completed-bar gating for every row;
- no OOS/Lockbox/Forward access;
- no provider/API/download path;
- no stale or diagnostic runner import path;
- deterministic output artifacts for each row family and executable ledger;
- complete validation/provenance/evidence/trusted-bundle closure for the run;
- clear separation between mechanical development/reconciliation PnL and any
  future source-faithful claim.

## Backtest-Readiness Requirements

Before any controlled development backtest is run, the next evidence set should
include:

1. A scoped GitHub checkpoint so GPT 5.5 Extended Pro can inspect the current
   code through GitHub.
2. A pre-run GPT hostile audit of the S27_V2 machinery, using GitHub as the
   primary code surface and Carver.pdf from the GPT library as source authority.
3. A response to any GPT P0/P1/P2 findings before run authorization.
4. A locked development input window using the oldest suitable local ZN data
   after all required warmups/evidence are populated.
5. A clear decision from the audit and local code inspection whether the next
   authorized step is:
   - a remaining multi-row backtest-runner implementation gate, or
   - a controlled local-only development backtest execution if the audited
     machinery is sufficient.
6. A backtest artifact plan that records, at minimum:
   - declared input pack and source file hashes;
   - runtime-history rows;
   - forecast rows;
   - desired-position rows;
   - order/transition rows;
   - fill rows;
   - cost rows;
   - PnL rows;
   - validation rows;
   - provenance/hash rows;
   - evidence-manifest rows;
   - trusted-bundle metadata;
   - local hostile audit record;
   - external post-run hostile audit prompt/packet.

## Cost And Valuation Policy Reminder

Book/source costs remain primary. If the book does not specify enough numeric
cost evidence, prop-firm, CFD, adapter, and personal trading costs are not
source-faithful strategy costs.

The current accepted 2.30 USD per contract per side NinjaTrader free-plan cost
is an inferred source-native retail futures development/reconciliation
assumption, not book-explicit Carver authority.

The current next-completed-hourly-close valuation convention is an engineering
valuation assumption for local development/reconciliation mechanics, not
book-explicit Carver authority.

## Recommended Next Sequence

1. Get explicit operator authorization for a scoped Git commit and remote GitHub
   push of the S27_V2 machinery checkpoint and this planning record.
2. After the push, prepare a GPT 5.5 Extended Pro pre-run hostile audit prompt.
   GPT should use the GitHub repository for full code inspection and use
   Carver.pdf from its library as the book authority.
3. Patch any GPT P0/P1/P2 findings.
4. If GPT passes, request the next exact operator authorization:
   - either multi-row backtest-runner implementation if GPT/local review finds
     the runner surface is still incomplete;
   - or controlled local-only development backtest execution if the audited
     machinery is sufficient.
5. After the first controlled development run, prepare a full artifact-set
   external audit for GPT, and later Opus when available.

## Non-Authorization

This planning gate does not authorize:

- Git staging, commit, push, branch, tag, PR, or release actions;
- provider/API access;
- downloads or new data acquisition;
- reading OOS, Lockbox, or Forward data;
- backtests or result-scored runs;
- result interpretation or PnL evaluation;
- tuning;
- adapter work;
- deployment, trading, or promotion;
- source-faithful evidence claims.

## Next Authorization Prompt

Use this prompt if the operator wants to publish the checkpoint for GPT pre-run
audit:

```text
Operator authorizes a scoped local commit and remote GitHub push for the S27_V2 locally passed machinery checkpoint through positive-action actual-PnL closure and the S27_V2 backtest-readiness planning record only.

Allowed scope is limited to S27_V2 replay code under src/carver/spine/s27_v2_replay, focused S27_V2 tests, and S27_V2 docs/process records required for the locally passed checkpoint and planning gate.

Do not stage, commit, or push unrelated workspace changes, researchops/data/input packs, Carver.pdf, credentials/keys, QuantLab references, old archive paths, unintended deletions, provider/API/download artifacts, OOS/Lockbox/Forward artifacts, backtest/result artifacts beyond process records, adapter/deployment/trading/promotion artifacts, or result interpretation artifacts.
```

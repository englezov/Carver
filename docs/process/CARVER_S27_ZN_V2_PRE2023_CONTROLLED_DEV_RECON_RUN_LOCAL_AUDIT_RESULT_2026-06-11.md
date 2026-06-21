# Local Hostile Audit - S27_V2 Pre-2023 Controlled Development/Reconciliation Run

Date: 2026-06-11

Verdict:

```text
PASS
```

Findings:

```text
P0: none
P1: none
P2: none
P3: none
```

## Scope

Audited scope:

```text
src/carver/spine/s27_v2_replay/development_recon_run.py
tests/test_s27_v2_development_recon_run.py
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_oldest_dev_recon_2022_controlled_run
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_oldest_dev_recon_2022_declared_pack
```

## Audit Answers

The audit confirmed:

- the runner is hard-locked to the declared pre-2023 ZN pack and locked output root;
- manifest hash and row-family byte hashes bind to on-disk bytes;
- the input-pack SHA file and run `SHA256SUMS.csv` verify cleanly;
- no provider/API/download/new-data path exists in the controlled runner;
- no TEST, VALIDATION, OOS, Lockbox, or Forward access is opened;
- 2023 remains preserved for TEST and excluded from this pack;
- point-in-time cutoff `2021-12-31` is preserved;
- future roll deltas remain excluded and the roll calendar stops at `2021-11-18`;
- completed-bar/strict-prior row selection holds for daily history, decision, and fill rows;
- mechanical arithmetic matches recorded ledgers:
  - forecast `4.894376401547715`;
  - desired position `8`;
  - BUY limit `130.421875`;
  - fill `TRUE`;
  - commission `18.4`;
  - spread `0.0`;
- PnL remains fail-closed because no post-fill valuation mark row is declared;
- no result interpretation, PnL evaluation, or source-faithful evidence claim is made;
- no stale diagnostic runner import/use exists in the scoped runner;
- no package-root export leak exists.

## Gate

The next non-backtest gate may proceed only with separate operator
authorization. Backtest/result/PnL-evaluation/source-faithful-evidence gates
remain unauthorized.

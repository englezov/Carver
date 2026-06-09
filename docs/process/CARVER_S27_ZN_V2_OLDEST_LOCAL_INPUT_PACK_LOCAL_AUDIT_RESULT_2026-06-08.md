# S27_V2 Oldest Local ZN Input Pack Local Audit Result

Date: 2026-06-08

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2_P3_FINDINGS
```

Audited packet:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260608_oldest_dev_recon_znh2_20220103_declared_pack
```

Related process record:

```text
docs/process/CARVER_S27_ZN_V2_OLDEST_LOCAL_INPUT_PACK_RECORD_2026-06-08.md
```

## Result

The read-only local hostile audit returned:

```text
PASS - no P0/P1/P2/P3 findings.
```

The audit confirmed:

- exactly seven declared row-family CSVs are present, with no extra row-family
  CSVs;
- all seven CSV headers match `REQUIRED_COLUMNS_BY_ROW_FAMILY` in
  `src/carver/spine/s27_v2_replay/local_replay.py`;
- current byte SHA256 values match the pack hash file, manifest, and process
  record;
- manifest/provenance/process records preserve non-authorizations and do not
  claim backtest, result interpretation, OOS, Lockbox, Forward, provider/API,
  downloads, trading, promotion, or source-faithful evidence;
- source selection is internally consistent about the 2022-01-03 first
  forecastable combined hourly/daily point, `ZNH2`, `instrument_id = 768155`,
  and the daily short-symbol ambiguity;
- no forbidden backtest, PnL, result, or promotion artifact was created in the
  declared input pack.

## Boundary

This audit result does not authorize provider/API access, downloads, new data
acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result
interpretation, PnL/result evaluation, tuning, adapter work, deployment,
trading, promotion, Git actions, or source-faithful evidence claims.

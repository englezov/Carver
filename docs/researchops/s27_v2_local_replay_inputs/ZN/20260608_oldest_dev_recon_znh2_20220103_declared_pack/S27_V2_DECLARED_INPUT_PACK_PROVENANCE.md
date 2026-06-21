# S27_V2 Oldest Local ZN Declared Input Pack Provenance

Date: 2026-06-08

Status:

```text
LOCAL_INPUT_PACK_DECLARED_FOR_PARSER_REPLAY_CONSTRUCTION_ONLY_NOT_EVIDENCE
```

This pack was generated under `S27_V2_OLDEST_LOCAL_ZN_INPUT_DECLARATION_AND_NORMALIZATION_GATE` from local dev/recon ZN files only. It is a minimal parser/file replay construction input pack, not a backtest, not a scored run, not result interpretation, and not a source-faithful evidence claim.

Oldest suitable local area:

```text
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN
```

The local daily lineage includes old historical contract rows, but its short `ZNH2` raw symbol is decade-ambiguous and has no 2022 daily lineage row. The pack therefore uses the local 2022 `daily_ZNH2_provider.csv` row with matching `instrument_id = 768155` for the previous completed current-contract daily close, then applies the hourly lineage adjustment from the 2022 decision row to produce the compatible continuous daily close.

Selected timestamps:

```text
previous completed daily current contract: 2022-01-02T00:00:00Z
decision completed hour: 2022-01-03T05:00:00Z
fill completed hour: 2022-01-03T06:00:00Z
```

Cost parameters are policy hashes only. Numeric commission/spread cost evidence is not claimed by this pack.

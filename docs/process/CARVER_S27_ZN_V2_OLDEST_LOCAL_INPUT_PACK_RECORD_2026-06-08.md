# S27_V2 Oldest Local ZN Input Pack Record

Date: 2026-06-08

Status:

```text
LOCAL_INPUT_PACK_DECLARED_FOR_PARSER_REPLAY_CONSTRUCTION_ONLY_NOT_EVIDENCE
```

Authorization:

```text
S27_V2_OLDEST_LOCAL_ZN_INPUT_DECLARATION_AND_NORMALIZATION_GATE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the creation of the first real local S27_V2 ZN declared input
pack for development/reconciliation only. It normalizes the oldest suitable
local ZN rows into the seven row-family CSVs required by
`ReplayInputDirectoryDeclaration`.

The pack is not a backtest, not a scored run, not PnL/result interpretation,
not a promotion artifact, and not a source-faithful replay evidence claim.

## Declared Input Pack

Directory:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260608_oldest_dev_recon_znh2_20220103_declared_pack
```

Required row-family CSVs:

```text
daily_continuous_completed_bar.csv
daily_current_contract_completed_bar.csv
hourly_decision_completed_bar.csv
hourly_fill_completed_bar.csv
session_calendar.csv
roll_calendar.csv
cost_parameter.csv
```

Support files:

```text
S27_V2_DECLARED_INPUT_PACK_MANIFEST.json
S27_V2_DECLARED_INPUT_PACK_PROVENANCE.md
S27_V2_DECLARED_INPUT_PACK_SHA256SUMS.txt
```

## Source Selection

Oldest suitable local area:

```text
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN
```

The hourly completed-bar local lineage begins at:

```text
2022-01-03T01:00:00Z
```

The first local forecastable/reconciliation row in the available S27 candidate
artifact is:

```text
2022-01-03T05:00:00Z
```

The declared pack therefore uses:

```text
previous completed daily current-contract row: 2022-01-02T00:00:00Z
hourly decision row: 2022-01-03T05:00:00Z
hourly fill row: 2022-01-03T06:00:00Z
raw symbol: ZNH2
instrument_id: 768155
```

The older daily lineage rows were not used as direct current-contract rows
because short raw symbols such as `ZNH2` are decade-ambiguous in the daily
lineage and the daily lineage has no 2022 row with the active 2022 instrument
id. The pack uses the local 2022 `daily_ZNH2_provider.csv` row for the previous
completed current-contract close and the local hourly lineage adjustment to
derive the compatible continuous daily close.

## Hashes

```text
B1845D317E03F9B39283F0BC880E38CC53E6E45830665E755F40189721D4BD02  daily_continuous_completed_bar.csv
183111EBD0812F147A89F97798A934C05D55F1010C1024DF0A9FC21F59BBA51D  daily_current_contract_completed_bar.csv
452796708770D200F88037F7EC5BEBAD8C9F203BE4DFABB6D9E9F9DB02D419D7  hourly_decision_completed_bar.csv
121BD0A785174F91B41E625F675E32EFE2946400C4DFDBE977B7A0161F680563  hourly_fill_completed_bar.csv
EA86B7F95F536ACA56FC70E662E2483D684B8C13AE0EF82252D297CCF7037167  session_calendar.csv
E56ECA7676759330BD06EB7BD69A3EC0A3BD240E35DE30DF0D3593F0BA3C9387  roll_calendar.csv
81277B7D9D5EF88D4F7EF29B1C0ABAAAC6A3D8591C9518B54ABFA3AC4F5EAB39  cost_parameter.csv
AA8E85E0D98D281814850E721382CB1FD8054C6E87C3A6DA7267C576BA98D186  S27_V2_DECLARED_INPUT_PACK_MANIFEST.json
```

## Local Verification

Focused parser verification:

```text
DECLARED_INPUT_PACK_PARSER_VERIFICATION_PASS
```

The parser verification constructed a `ReplayInputDirectoryDeclaration`, read
only the seven declared normalized CSV files under the declared input directory,
checked byte SHA256 values, parsed all seven row families, and validated one
content-bound row hash per family.

Focused local tests:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
49 passed
```

## Boundaries

Cost parameters in this pack are policy hashes only. Numeric commission/spread
cost evidence remains unresolved and is not claimed.

This record does not authorize provider/API access, downloads, new data
acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result
interpretation, PnL/result evaluation, tuning, adapter work, deployment,
trading, promotion, Git actions, or source-faithful evidence claims.

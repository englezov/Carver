# S27_V2 Controlled Local Replay Construction Run Record

Date: 2026-06-08

Status:

```text
LOCAL_REPLAY_CONSTRUCTION_ARTIFACTS_BUILT_AND_VALIDATED_NOT_EVIDENCE
```

Authorization:

```text
S27_V2_CONTROLLED_LOCAL_ONLY_REPLAY_CONSTRUCTION_RUN_DECLARED_ZN_INPUT_PACK
```

Input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260608_oldest_dev_recon_znh2_20220103_declared_pack
```

Output directory:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260608_controlled_local_replay_construction_declared_pack
```

## Scope

This run read only the seven declared row-family CSV files in the audited local
ZN input pack, verified byte SHA256 declarations, parsed the declared local
rows, and constructed deterministic S27_V2 local replay construction artifacts
through the audited `build_local_parser_file_replay_completion(...)` path.

The output is construction/contract material only. It is not a backtest, not a
result-scored run, not result interpretation, not PnL evaluation, not
promotion, and not a source-faithful replay evidence claim.

## Fail-Closed Precheck

The first construction attempt failed closed before output generation because
the local row-locator declaration for roll/cost rows reused a locator component
name. The row-locator contract rejected this with:

```text
S27 v2 row locator component names must be unique
```

The declaration shape was corrected to use unique locator components and the
controlled run was repeated successfully.

## Run Result

```text
CONTROLLED_LOCAL_REPLAY_CONSTRUCTION_PASS
```

Key hashes:

```text
run manifest SHA256: 3B44823EB93CF9FE612C8419E6A3262E7D54F2CCC3F3396CB29CD7250B698D10
trusted bundle contract hash: E618E39C858AABF7DB72DA53DD8735F6ED528A4733EF881F3479C6502DE80B31
validation contract bundle hash: EC3C431C241E6BB433E0961685ECBEBE358B8F826D370EB76F064ABC63C21AD3
construction contract hash: 17EFDBF499A2EDA953C7996FC33F7721E56E39D3770A190E96EF906A39487F96
```

Declared row-family parse summary:

```text
DAILY_CONTINUOUS_COMPLETED_BAR 1 B1845D317E03F9B39283F0BC880E38CC53E6E45830665E755F40189721D4BD02 BC12834DF88D336B15E2A1AB985F5125B23CB00991FFA077AA1846B24032955B
DAILY_CURRENT_CONTRACT_COMPLETED_BAR 1 183111EBD0812F147A89F97798A934C05D55F1010C1024DF0A9FC21F59BBA51D 3F492E15FA8059CC94FA9CE481FE23624DE315BA83C69E1C2AD1750179FAC28C
HOURLY_DECISION_COMPLETED_BAR 1 452796708770D200F88037F7EC5BEBAD8C9F203BE4DFABB6D9E9F9DB02D419D7 E702757C3F5AA5FCE5A0912D407D21C07F2440FE39A4DF58615B775EBA1E8CBB
HOURLY_FILL_COMPLETED_BAR 1 121BD0A785174F91B41E625F675E32EFE2946400C4DFDBE977B7A0161F680563 EF035F155EEC05F249C2CC5BF16B5270604AB9543CD521EF17FBB3A104DAE75C
SESSION_CALENDAR 1 EA86B7F95F536ACA56FC70E662E2483D684B8C13AE0EF82252D297CCF7037167 B9EB3F9D7D9CA21B6ECF858C50683D9FED3341B7E89721256ED8E7306B02C1E6
ROLL_CALENDAR 1 E56ECA7676759330BD06EB7BD69A3EC0A3BD240E35DE30DF0D3593F0BA3C9387 9AF5A177D35A9C17EC82597B8DD88B273E781D865910EFDC11254337E5CBE98B
COST_PARAMETER 1 81277B7D9D5EF88D4F7EF29B1C0ABAAAC6A3D8591C9518B54ABFA3AC4F5EAB39 E6A808FD4244723B0AC95C966C316C7083847FEF5E4A9F7D02A40717706567F9
```

## Artifact Files

The output directory contains:

- `S27_V2_CONTROLLED_LOCAL_REPLAY_CONSTRUCTION_RUN_MANIFEST.json`
- `S27_V2_CONTROLLED_LOCAL_REPLAY_CONSTRUCTION_SHA256SUMS.txt`
- 34 JSON construction artifacts under `artifacts/`, numbered
  `00_input_directory_declaration.json` through
  `33_trusted_bundle_contract.json`.

The hash ledger was checked against current bytes and all entries passed.

## Local Verification

Focused local verification:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
49 passed
```

Additional local checks confirmed no files with forbidden backtest/result/score
or PnL ledger naming were written in the output directory.

## Boundaries

The `pnl_input_contract.json` and `pnl_contract.json` files are inert contract
scaffolds only. No PnL rows, scored result rows, fills ledger, trade ledger,
cost ledger, backtest artifact, OOS artifact, Lockbox artifact, or Forward
artifact was produced.

This record does not authorize provider/API access, downloads, new data
acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result
interpretation, PnL/result evaluation, tuning, adapter work, deployment,
trading, promotion, Git actions, or source-faithful evidence claims.

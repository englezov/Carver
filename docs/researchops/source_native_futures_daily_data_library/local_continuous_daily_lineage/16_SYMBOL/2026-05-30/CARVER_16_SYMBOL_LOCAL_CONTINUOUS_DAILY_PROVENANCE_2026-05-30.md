# Carver 16-Symbol Local Continuous Daily Lineage Execution Provenance - 2026-05-30

## Status

```text
FAIL_CLOSED_NO_LOCAL_CONTINUOUS_SERIES_CONSTRUCTED_GATE1_FRAGMENT_LACKS_ADJACENT_CONTRACT_OVERLAP
```

## Scope

This execution attempted the process/local Gate 1-fragment-only local continuous daily lineage construction path authorized by the operator.

The attempt used only existing local Carver artifacts. It did not access provider APIs, log in to a provider, request or download new data, download continuous contracts, use provider-built continuous series as source authority, expand symbols, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility or risk, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active-pipeline state, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Input Hash Verification

| Input | SHA256 |
|---|---|
| `canonical_manifest` | `0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88` |
| `gate1_fragment_table` | `C18C1956A75B161B86132D3CCC43ADAED4D3D7950002DB7BD0E01D50AA5C5AC9` |
| `gate1_status` | `A81DA21AF8E6925478C6D7C2CFDC0119B56765AB4E82FB51C2294BBC8E0C6BB0` |
| `gate1_provenance` | `8D43EC12F2FF244481B7A9EB5302F36A5D4AD9D99B5A0BCBBCFFAC8BC65E6066` |
| `gate2_source_index` | `F1F0F37D93C1B40957F2AA683C975ADCA1DCD041E12D27C98A28227EED94399A` |
| `gate2_requirements` | `91764D3CBA3FA78BB1AF8DDB7D3207A33F1C154ECA1DF4611F623EBF4801CCF8` |
| `gate2_provider_status` | `CFA374099B03AAEDDAD4C25AB257347C42DEFA14E928D857B64907FA73AA457F` |
| `gate2_lifecycle` | `C36181673C9E79B0B322DDF885B32F1A5EC31DDFA7DCA99E7DFF224F6BD19BF6` |

All listed hashes matched before execution artifacts were created.

## Execution Result

The execution failed closed before constructing any continuous series.

Reason:

```text
GATE1_FRAGMENT_CONTAINS_ONLY_CURRENT_DATED_CONTRACT_PER_SYMBOL
ADJACENT_OLD_NEW_CONTRACT_PAIR_REQUIRED_FOR_ROLL_TRANSITION
SEPARATE_DATED_CONTRACT_EXPANSION_GATE_REQUIRED
```

Observed input facts:

```text
manifest_symbol_count = 16
gate1_fragment_row_count = 4483
symbols_with_roll_plan_blocked = 16
constructed_continuous_series_rows = 0
source_lineage_rows = 0
adjustment_ledger_rows = 0
```

Every symbol was preserved in the roll-plan ledger and marked fail-closed. No symbol was silently dropped, substituted, bridged, or reweighted.

## Output Files

- `CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_POLICY_STATUS_2026-05-30.csv`
- `CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_ROLL_PLAN_2026-05-30.csv`
- `CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_SOURCE_LINEAGE_2026-05-30.csv`
- `CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_ADJUSTMENT_LEDGER_2026-05-30.csv`
- `CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_SERIES_DEV_RECON_ONLY_2026-05-30.csv`
- `CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_PROVENANCE_2026-05-30.md`
- `CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_SHA256SUMS_2026-05-30.txt`

## Labels Preserved

```text
daily_price_field = DATABENTO_OHLCV_1D_CLOSE
daily_price_semantics = TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT
provider_timestamp_policy = UTC_MIDNIGHT_PROVIDER_DAILY_BAR_TIMESTAMP_NOT_EXCHANGE_SESSION_END
completed_trading_date_policy = CARRIED_FROM_SOURCE_QUARANTINE_COMPLETED_TRADING_DATE
settlement_policy = BLOCKED_PENDING_OFFICIAL_SETTLEMENT_SOURCE_GATE
provider_built_continuous_used_as_source = NO
```

## Next Required Gate

The next clean gate is a dated-contract roll-pair expansion gate that defines and authorizes the adjacent contract rows needed for local continuous roll transitions.

Suggested gate name:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_ROLL_PAIR_EXPANSION_SHAPE_GATE
```

## Non-Authorization

This failed-closed execution authorizes no provider API access, provider login, provider account portal use, new market-data request, data download, market-row parsing beyond existing Gate 1 fragment parsing, continuous-contract download, provider-built continuous source authority, strategy input creation, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility or risk calculations, OOS, Lockbox, Forward, CFD adapter execution, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote operations.

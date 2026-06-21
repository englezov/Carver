# S27_V2 First-Populated ZN Input Pack P3 Hardening And Build Record

Date: 2026-06-09

Status:

```text
LOCAL_ONLY_FIRST_POPULATED_INPUT_PACK_P3_HARDENING_AND_BUILD_LOCAL_AUDIT_PASS
```

Authorization:

```text
S27_V2_LOCAL_ONLY_FIRST_POPULATED_ZN_INPUT_PACK_P3_HARDENING_AND_BUILD
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers two local-only changes:

1. Phase 2 provenance validation was hardened so selected level row prices bind to the exact indexed row hash in Phase 1 provenance.
2. A fresh multi-row declared ZN input pack was built from already-local source/provider/lineage files, using the corrected first-post-populated rule rather than treating `2022-2023` as the S27_V2 dev/recon slice.

This is not a parser/file replay result, not a diagnostic, not a backtest, not result interpretation, not PnL evaluation, not promotion, and not a source-faithful evidence claim.

## Code Hardening

Touched code:

```text
src/carver/spine/s27_v2_replay/executable_replay.py
tests/test_s27_v2_local_replay_slice1.py
```

Hardening:

```text
Phase 2 now derives row_close_price_by_family from Phase 1 row_family_hashes plus price_row_close_prices and validates each level-row close against the close price for the exact selected row hash.
```

Regression test:

```text
test_phase2_level_price_binds_exact_indexed_row_hash
```

This test forges a valid active row hash from a different index while keeping the old close price. The validator now rejects it.

## Declared Input Pack

Pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_first_populated_dev_recon_znh2_20220103_multirow_declared_pack
```

Support files:

```text
S27_V2_FIRST_POPULATED_DECLARED_INPUT_PACK_MANIFEST.json
S27_V2_FIRST_POPULATED_DECLARED_INPUT_PACK_PROVENANCE.md
S27_V2_FIRST_POPULATED_DECLARED_INPUT_PACK_SHA256SUMS.txt
```

Row counts:

```text
DAILY_CONTINUOUS_COMPLETED_BAR = 64
DAILY_CURRENT_CONTRACT_COMPLETED_BAR = 1
HOURLY_DECISION_COMPLETED_BAR = 8
HOURLY_FILL_COMPLETED_BAR = 8
SESSION_CALENDAR = 1
ROLL_CALENDAR = 1
COST_PARAMETER = 1
```

Selected candidate row:

```text
decision completed hour = 2022-01-03T05:00:00Z
fill completed hour = 2022-01-03T06:00:00Z
previous completed daily current-contract row = 2022-01-02T00:00:00Z
raw symbol = ZNH2
```

## Hashes

```text
5437BCF2C7BCBB40BAF0BA1245DD8AE156D6E2378F482D8E7ECE3EAA551E5516  daily_continuous_completed_bar.csv
A085989CA4DB1753333B2E99E7D1A270E137FEC691C9AF88006D9CD22D4B8DA5  daily_current_contract_completed_bar.csv
C00FB1425C8A3682A9C20E3743D0C212D948D72C608950A80E281EC97C06D5C8  hourly_decision_completed_bar.csv
9B98AC49842164A60A19DA6DB519695A9B12E884A6C268917F4C06AFAD349243  hourly_fill_completed_bar.csv
D4FEC50876E1B845913E0C2125ED64725A365538A01BB1BC147999FFEA8C9AE3  session_calendar.csv
69DD394C97A4B11CCF47FB3CCC3030625F45FFE19340F65E453088B8BE8DF657  roll_calendar.csv
42F00022D7225450098DC7DA63A8937E1D823F4F218248A534828CCE74FEC888  cost_parameter.csv
5B9A6C6766C97D9C44F8E5AC7B1339D8E25E499B8FF96C2D8D1B574E76F4B781  S27_V2_FIRST_POPULATED_DECLARED_INPUT_PACK_MANIFEST.json
```

## Verification

Focused parser verification read only the seven declared row-family CSVs under the new input pack and parsed:

```text
DAILY_CONTINUOUS_COMPLETED_BAR,64
DAILY_CURRENT_CONTRACT_COMPLETED_BAR,1
HOURLY_DECISION_COMPLETED_BAR,8
HOURLY_FILL_COMPLETED_BAR,8
SESSION_CALENDAR,1
ROLL_CALENDAR,1
COST_PARAMETER,1
```

Focused tests:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
68 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2_replay\executable_replay.py tests\test_s27_v2_local_replay_slice1.py
PASS
```

## Caveats

The old path label `2022-01-01_2023-12-31` is not the S27_V2 dev/recon slice. It is only a local artifact/source folder.

The local R2 V/Q/M ledger ends at `2020-12-21`, while the selected hourly decision row is `2022-01-03T05:00:00Z`. This pack must therefore remain construction input only and must not be treated as nonblocked V/Q/M runtime evidence.

The selected daily sigma is carried from an already-local forecast sigma bridge row to satisfy the current parser schema. That does not source-lock Strategy 3 sigma and does not make old forecast/runtime rows authority.

## Non-Authorization

This record does not authorize provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

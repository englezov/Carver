# S27 V2 2023 TEST Row 441 Market-Order TBBO Extended-Lookback Evidence

Date: 2026-06-14

Status:

```text
PASS_ROW441_EXTENDED_LOOKBACK_DATABENTO_TBBO_SELECTED_NOT_RESULT
```

This process record was written by the row-441-only bounded DataBento TBBO extended-lookback evidence acquisition tool.

Scope:

- Row index: `441`
- Raw symbol: `ZNH3`
- Fill candidate timestamp: `2023-01-31T05:00:00Z`
- Request window: `2023-01-31T04:55:00Z` through `2023-01-31T05:00:05Z`
- Selection rule: latest non-crossed positive TBBO at or before fill timestamp
- Max selected quote age: `300.0` seconds
- Engineering label if selected: `ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT`

Selected row count: `1`
Failed row count: `0`
Quote rows returned: `6`
Selected quote timestamp: `2023-01-31T04:57:05.652860819Z`
Quote age seconds: `174.34714`
Bid: `114.359375`
Ask: `114.375`
Executable fill price: `114.359375`
Selection status: `PASS_ROW441_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT`
Provider condition status: `PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED`

## Artifact Hashes

Selected spread registry:

```text
0A2EC015D252A08E2AC6BFE5BBE8FFD60969C97E6C409609DC6CAF593E3E379F
```

Provider condition ledger:

```text
0353433758B0A0C5E1C06ADA15B17EEDC7716EF1032B4D4C786A4CE8910C1EF5
```

Raw DBN:

```text
00AD4BA19C673802222F94BB88F8032A651064E2F35E81DEC3188D1AF91019E8
```

Raw CSV:

```text
09DCE145FEFA1D2832D4F2F47E573C536D449299DC2903A9E776CA3DB758A155
```

Raw output registry:

```text
BC41B0BED8A6003D05FAB9A71942E760D107E3F1F6ADE97BFDBE9D0A99B1F0D5
```

Request manifest:

```text
947341820C45598F853FBA5A37685D1C5C92AC9F770EA40728D5E36CF15867C2
```

Status JSON:

```text
E1EF9B66AD9EDC969C951CBC9F59C3AF26B60C8CF421A37C7BA7B7F92B34E6F8
```

Provenance:

```text
E57B02816B247AEDEB05B8EC68049264565E360FEE64A7AE0F25D3A6D99996BF
```

SHA256 manifest:

```text
605283A9B9222ACEBBAA45202B08398E057602F3C39D853FAE46B2FD768B773E
```

This evidence gate does not authorize broader TEST continuation, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.

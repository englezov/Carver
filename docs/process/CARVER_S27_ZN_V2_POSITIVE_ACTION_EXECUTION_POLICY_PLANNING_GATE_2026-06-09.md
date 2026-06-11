# S27 V2 Positive-Action Execution-Policy Planning Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_POSITIVE_ACTION_EXECUTION_POLICY_EVIDENCE_GATE_NOT_ORDER_FILL_COST_PNL_RESULT_AUTHORITY
```

## Authorization

Operator authorized a local-only positive-action execution-policy planning and evidence gate after external PASS on the positive-action executable packet.

This record is limited to defining and source-locking the minimal evidence required before any actual limit-order, market-order, working-order, or fill ledger emission.

## Non-Authorization

This record authorizes no provider/API access, no downloads, no new data acquisition, no OOS, no Lockbox, no Forward, no backtests, no result-scored runs, no actual limit-order emission, no actual market-order emission, no actual fill emission, no actual cost emission, no PnL/result emission, no result interpretation, no PnL evaluation, no tuning, no adapter work, no deployment, no trading, no promotion, no Git actions, and no source-faithful evidence claim.

## Inputs Inspected

- `docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md`
- `docs/process/CARVER_S27_ZN_V2_NON_FORGEABLE_REPLAY_PROVENANCE_DESIGN_2026-06-06.md`
- `docs/process/CARVER_S27_ZN_V2_LOCAL_ROW_REPLAY_IMPLEMENTATION_PLAN_2026-06-06.md`
- `docs/process/CARVER_S27_ZN_V2_GPT_EXTERNAL_AUDIT_REMEDIATION_2026-06-05.md`
- `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_LIMIT_SESSION_PROVENANCE_REMEDIATION_2026-06-06.md`
- `docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md`
- `src/carver/spine/s27_v2.py`
- `src/carver/spine/s27_v2_replay/orders.py`
- `src/carver/spine/s27_v2_replay/fills.py`
- `src/carver/spine/s27_v2_replay/transitions.py`
- `src/carver/spine/s27_v2_replay/costs.py`
- `docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/S27_V2_POSITIVE_ACTION_DECLARED_INPUT_PACK_MANIFEST.json`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/session_calendar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/roll_calendar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/cost_parameter.csv`

## Positive-Action Context

The externally passed positive-action packet selected the first local post-warmup positive-action ZN development/reconciliation row:

```text
decision_timestamp_utc = 2026-04-13T13:00:00Z
fill_candidate_timestamp_utc = 2026-04-13T14:00:00Z
raw_symbol = ZNM6
current_position = 0
desired_rounded_position = -1
position_change = -1
order_intent = SELL 1
```

The current pack remains development/reconciliation evidence only. It is not a backtest, result, PnL evaluation, or source-faithful replay evidence claim.

## Evidence Decision Table

| Topic | Status | Decision |
| --- | --- | --- |
| Positive-action authority | `PASS_EXTERNAL_AUDITED_ORDER_INTENT_ONLY` | The active positive-action bundle is externally passed for flat-to-`SELL 1` intent. This does not emit an actual order. |
| Adjacent limit-order concept | `SOURCE_LOCKED_CONCEPT` | S27 v2 must use S26/S27 adjacent-position limit-order machinery, not close-to-close target-position PnL. |
| Exact formula-implied adjacent price | `STRUCTURAL_FORMULA_PRESENT_NOT_EXECUTABLE_BY_ITSELF` | `implied_price_for_target_position()` inverts the forecast-to-position formula and is covered by synthetic/source-lock tests, but process design says synthetic formula-only prices are not executable local-row evidence without tick/rounding lock. |
| ZN tick size and point value | `LOCAL_STATIC_EVIDENCE_PRESENT_NOT_FINAL_EXECUTION_LOCK` | Appendix C/static evidence contains ZN point value `1000`, tick size `0.015625`, tick value `15.625`, currency `USD`; its intake status remains `STATIC_FIELDS_EXTRACTED_CONTRACT_IDENTITY_NOT_LOCKED`, so execution use must bind source hash/effective evidence before actual executable limit prices. |
| Side-specific tick rounding | `FAIL_CLOSED_SOURCE_UNRESOLVED` | Real-row replay must fail closed before executable limit prices until ZN tick size and side-specific executable limit rounding policy are source-locked. |
| Limit-order fill condition | `SOURCE_LOCKED_CONCEPT_PENDING_EXECUTABLE_LIMIT_PRICE` | Existing process records lock close-only one-hour fill authority: buy limit fills when next completed close is at/below limit; sell limit fills when next completed close is at/above limit. Actual fill remains blocked until executable limit price and tick rounding are locked. |
| One-hour lag | `SOURCE_LOCKED_AND_LOCAL_ROW_AVAILABLE` | The selected fill candidate is the exact next completed hourly row, one hour after the decision timestamp. |
| Session continuity | `LOCAL_PROOF_AVAILABLE_FOR_THIS_ROW_NOT_FULL_LIFECYCLE` | The session row covers `2026-04-12T22:00:00Z` through `2026-04-13T21:00:00Z`; decision and fill candidate are same raw symbol/session/trading date. This supports a same-session normal-transition proof for this row only. |
| Roll continuity | `LOCAL_NO_ROLL_BOUNDARY_PROOF_AVAILABLE_FOR_THIS_ROW` | The declared roll row is `2026-02-16` ZNH6->ZNM6, while the selected row is `2026-04-13` ZNM6. Nonzero-position roll handling remains fail-closed for broader replay. |
| Initial working state | `FIRST_ROW_FLAT_EMPTY_STATE_CAN_BE_HASH_LOCKED` | First-row context can bind flat current position and empty prior working order state. Caller-created state remains non-authority. |
| Working-order lifecycle | `FAIL_CLOSED_BEYOND_FIRST_NORMAL_TRANSITION` | Multi-hour/day lifecycle remains unresolved: unfilled limit persistence, modification after fill, new adjacent orders after fill, EOD cancellation, and new-session recomputation still require implementation and audit. |
| Market fallback | `NO_MARKET_PROOF_PLANNABLE_FOR_THIS_ROW` | This row has one-contract desired gap, is not at cap, and has a priceable adjacent target. Market-order emission should be rejected for this row; broader market fallback cases remain fail-closed until separately implemented. |
| Cost treatment shape | `SOURCE_LOCKED_TREATMENT_NUMERIC_COST_POLICY_UNRESOLVED` | Source-lock requires commission for all orders, limit fills commission-only, market fills commission plus normal bid/ask spread. Numeric commission/spread policy remains unresolved and must follow project cost policy: book/source costs first, otherwise clearly labeled source-native retail futures inferred costs; never prop-firm, CFD, adapter, or personal costs. |
| Actual order/fill/cost/PnL/result emission | `BLOCKED_NOT_AUTHORIZED` | This gate emits no actual limit orders, market orders, fills, costs, PnL, result rows, backtests, or source-faithful evidence claims. |

## Minimal Evidence Required Before Actual Limit-Order Emission

Actual positive-action limit-order emission for this row requires a future implementation gate that binds:

- active positive-action bundle hash and row hash;
- active forecast/desired-position authority;
- first-row initial-state hash and flat current-position context;
- no-market trigger proof for one-contract non-cap adjacent target;
- formula-implied adjacent target price from active forecast context;
- ZN tick-size, tick-value, point-value, currency, effective-date/source evidence;
- side-specific executable limit rounding policy;
- executable tick price;
- order-plan hash and limit-order hash;
- non-authorization preservation for fill, cost, PnL, result, backtest, provider/API, downloads, Git, adapter/deployment/trading/promotion, and source-faithful evidence claims.

## Minimal Evidence Required Before Actual Fill Emission

Actual fill emission must remain separate from order emission unless explicitly authorized. It requires:

- actual emitted order hash from a trusted order-plan bundle;
- trusted working-state transition hash;
- exact next completed hourly fill-row hash;
- one-hour-lag proof;
- unchanged raw symbol, session id, and completed trading date proof;
- fill condition hash proving close-only crossing of the submitted executable limit price;
- fill price provenance locked as `LIMIT_ORDER_PRICE_FROM_FILLED_ORDER` for limit fills, or `MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE` for market fills;
- fail-closed rejection of intrabar high/low fill authority;
- no cost, PnL, result, backtest, or source-faithful evidence claim unless separately authorized.

## Minimal Evidence Required Before Actual Cost Emission

Actual cost emission remains blocked until a source-native ZN cost policy is resolved:

- book/source commission and spread assumptions if available;
- otherwise a labeled source-native retail futures inferred cost assumption;
- no prop-firm fees, evaluation fees, payout rules, CFD spreads, swaps, adapter costs, or personal trading costs;
- commission per contract, unit, currency, amount, and policy hash;
- spread unit/amount/space and multiplier/currency binding for market-order spread costs;
- explicit proof that limit fills are commission-only unless the source-lock changes.

## Recommended Next Authorization

The next useful gate is a consolidated positive-action order-policy source-lock and executable order-plan gate. It should either emit a deterministic limit-order/working-transition surface for this single audited row or fail closed with exact unresolved gates. It should not emit fills, costs, PnL, results, backtests, or source-faithful evidence claims.

Suggested operator authorization prompt:

```text
Operator authorizes S27_V2 local-only positive-action limit-order policy source-lock and executable order-plan gate, after external PASS on the positive-action executable packet and completion of the execution-policy planning gate, limited to the audited ZNM6 positive-action row at 2026-04-13T13:00:00Z.

This authorizes Codex to bind the active positive-action bundle, first-row flat/empty working-state context, no-market proof, adjacent `SELL 1` target, formula-implied adjacent limit price, ZN static tick/point-value/currency/effective evidence from already-local records, side-specific tick rounding policy, executable limit price, order-plan metadata, limit-order row, and same-session normal transition planning metadata where evidence is sufficient, and to fail closed on any unresolved execution-policy item.

This authorizes code/tests/process records/local hostile audits with subagents and narrow P0/P1/P2 follow-up patches inside this exact order-plan scope.

No provider/API access, downloads, new data acquisition, OOS/Lockbox/Forward access, backtests, result-scored runs, actual fill emission, actual cost emission, actual PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

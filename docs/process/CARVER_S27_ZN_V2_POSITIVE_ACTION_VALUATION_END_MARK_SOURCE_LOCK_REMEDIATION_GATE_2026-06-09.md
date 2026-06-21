# S27_V2 Positive-Action Valuation End-Mark Source-Lock Remediation Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_POSITIVE_ACTION_VALUATION_END_MARK_FAIL_CLOSED_NOT_SOURCE_LOCKED
```

## Authorization

Operator authorized the `S27_V2 positive-action valuation/end-mark source-lock remediation gate` after local PASS on the positive-action actual cost ledger surface.

Scope was limited to resolving or explicitly fail-closing the valuation/end-mark policy required before any actual PnL ledger or backtest-readiness surface for the audited `ZNM6` short position after:

```text
fill_timestamp_utc = 2026-04-13T14:00:00Z
fill_price = 111.046875
fill_quantity = 1
position_after_fill = -1
```

## Non-Authorization

This record authorizes no provider/API access, no market-data downloads, no new data acquisition, no OOS, no Lockbox, no Forward, no backtests, no result-scored runs, no actual PnL ledger emission, no result emission, no result interpretation, no PnL evaluation, no tuning, no adapter work, no deployment, no trading, no promotion, no Git actions, and no source-faithful evidence claim.

## Inputs Inspected

Already-local source/process records and rows inspected:

```text
Carver.pdf
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_NUMERIC_COST_ASSUMPTION_AND_VALUATION_POLICY_SOURCE_LOCK_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_INFERRED_RETAIL_COST_ACCEPTANCE_AND_VALUATION_SOURCE_LOCK_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_INFERRED_RETAIL_COST_ACCEPTANCE_AND_VALUATION_SOURCE_LOCK_LOCAL_AUDIT_RESULT_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_ACTUAL_COST_IMPLEMENTATION_RECORD_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_ACTUAL_COST_LOCAL_AUDIT_RESULT_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_PNL_BLOCKED_IMPLEMENTATION_RECORD_2026-06-09.md
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/hourly_decision_completed_bar.csv
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/hourly_fill_completed_bar.csv
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/session_calendar.csv
```

No provider API, credentialed source, market-data download, backtest, result-scored run, actual PnL emission, result interpretation, PnL evaluation, Git action, adapter/deployment/trading/promotion, or tuning was used.

## Book / Source Evidence

The targeted local PDF search and existing source-lock records support:

```text
hourly data is the stated testing frequency for Part Four fast strategies
S26/S27 order fills use a one-hour-lag backtest assumption
holding PnL is conceptually price change times point value
trading costs are separated from holding PnL
back-adjusted prices are used to reflect rolling PnL while costs are handled separately
S27 v2 PnL rows must be tied to fills and held position state
```

Relevant book-search pages included:

```text
page 15  = hourly data is the smallest collected interval
pages 26-30 = cost and holding-PnL decomposition using mid prices and back-adjustment
pages 475-482 = Part Four hourly strategy context and S26/S27 hourly price/equilibrium context
pages 490, 498 = hourly backtest caveats and one-hour-lag execution assumptions
```

This evidence is sufficient to require a future PnL surface to bind price rows, point value/currency, fills, costs, and held-position state. It is not sufficient to source-lock the first post-fill valuation/end-mark timestamp for a newly opened S27 position.

## Declared Local Pack Evidence

The audited positive-action declared pack contains these relevant completed hourly rows:

```text
hourly_decision_completed_bar.csv
completed_timestamp_utc = 2026-04-13T13:00:00Z
close_price = 111.03125

hourly_fill_completed_bar.csv
completed_timestamp_utc = 2026-04-13T14:00:00Z
close_price = 111.09375

session_calendar.csv
session_open_utc = 2026-04-12T22:00:00Z
session_close_utc = 2026-04-13T21:00:00Z
```

This pack does not include a separately declared next-hour-after-fill valuation row, a session-close valuation row, a settlement row, or a daily end-mark row for this position.

## Candidate Policies Evaluated

The following candidates are not source-locked in this gate:

```text
SAME_COMPLETED_FILL_CANDIDATE_CLOSE
NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL
SESSION_CLOSE
NEXT_DAILY_CLOSE
SETTLEMENT_END_OF_DAY
REALIZED_ONLY_UNTIL_EXIT
```

Decision notes:

- Same completed fill-candidate close would reuse the fill-decision close as the first mark after a fill at the submitted limit price. The book/source records do not explicitly authorize this as the first held-position valuation mark.
- Next completed hourly close after fill remains a plausible engineering candidate because it avoids same-bar fill/mark reuse and matches the hourly lane, but it is still not an explicit book/source lock.
- Session close, next daily close, settlement/end-of-day, and realized-only-until-exit are not explicitly selected by the S27 source-lock records for this hourly strategy path.

## Decision

```text
VALUATION_END_MARK_POLICY = FAIL_CLOSED_NOT_SOURCE_LOCKED
ACTUAL_PNL_LEDGER = FAIL_CLOSED_VALUATION_END_MARK_POLICY_NOT_SOURCE_LOCKED
BACKTEST_READINESS = FAIL_CLOSED_VALUATION_END_MARK_POLICY_NOT_SOURCE_LOCKED
RESULT_STATUS = FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
SOURCE_FAITHFUL_EVIDENCE_CLAIM = FALSE
```

The accepted actual cost ledger does not unlock PnL. Numeric cost is now locally accepted/emitted for this one limit fill, but valuation/end-mark remains the blocking prerequisite for any actual PnL ledger or backtest-readiness surface.

## Decision Block Hash

Canonical decision block bytes are the UTF-8 bytes of the exact text block below, including final newline.

```text
VALUATION_END_MARK_FAIL_CLOSED_DECISION_BLOCK_SHA256 = 423fa5e17efaec00d9b1224cd8008cb950801200c2b8b05fe145804a72f3ded2
```

`VALUATION_END_MARK_FAIL_CLOSED_DECISION_BLOCK`:

```text
decision=VALUATION_END_MARK_POLICY_FAIL_CLOSED_NOT_SOURCE_LOCKED
scope=ZNM6_POSITIVE_ACTION_SHORT_AFTER_2026-04-13T14:00:00Z_LIMIT_FILL
source_status=HOURLY_BACKTEST_AND_ONE_HOUR_EXECUTION_EXPLICIT_BUT_FIRST_POST_FILL_MARK_TIMESTAMP_NOT_EXPLICIT
rejected_candidates=SAME_COMPLETED_FILL_CANDIDATE_CLOSE|NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL|SESSION_CLOSE|NEXT_DAILY_CLOSE|SETTLEMENT_END_OF_DAY|REALIZED_ONLY_UNTIL_EXIT
actual_pnl_emission_authorized=false
backtest_readiness=false
source_faithful_evidence_claim=false
```

## Minimum Future Unlock Requirement

Before any actual PnL ledger or backtest-readiness implementation, a separate authorization must either:

- identify an explicit book/source passage or already-local source-lock artifact that selects the valuation/end-mark timestamp policy; or
- authorize an inferred valuation convention as a clearly labeled engineering assumption, not a source-faithful book rule, with local and external audit.

Any future valuation pack must also include the exact price row used for the mark, with byte/hash binding to the selected row and no same-row/self-authenticating shortcut.

## Boundary

This remediation record is process-only. It is not a PnL ledger, not a result, not backtest readiness, not result interpretation, not PnL evaluation, and not a source-faithful evidence claim.

Actual PnL rows, result rows, backtests, result interpretation, PnL evaluation, source-faithful evidence claims, provider/API access, market-data downloads, OOS/Lockbox/Forward, Git actions, adapter/deployment/trading/promotion, and tuning remain unauthorized.

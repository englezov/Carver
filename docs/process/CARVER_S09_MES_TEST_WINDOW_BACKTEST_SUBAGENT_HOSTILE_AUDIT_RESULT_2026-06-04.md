# S09 MES TEST Window Backtest Subagent Hostile Audit Result

Date: 2026-06-04

Status:

```text
SUBAGENT_HOSTILE_AUDIT_CONFIRMS_EXACTLY_ONE_TEST_BACKTEST_WITH_CONCERNS
```

Confirmed:

- exactly one TEST backtest receipt exists;
- TEST window is `2020-04-06` through `2022-02-08`;
- continuous completed dates: 574;
- forecast rows: 318;
- backtest rows: 317;
- nonzero position-change rows: 317;
- status and summary metrics match;
- completed backtest used the existing authorized TEST download, not a fresh Databento API call;
- degraded labels are preserved through lineage;
- no CFD, old QuantLab active pipeline, Git publication, deployment, trading, or promotion artifact was found in the completed TEST packet.

Concerns:

- The packet still contains an empty legacy directory named `validation`. No validation files are present; current guard output uses `guard_checks`.
- The packet also contains earlier authorized TEST download and fail-closed artifacts from before the completed backtest. Those artifacts are historical packet context, not evidence of a fresh provider/API call during the completed backtest execution.

Disposition:

The completed TEST backtest packet is accepted as exactly-one TEST execution
evidence with housekeeping concerns recorded. No cleanup, deletion, Git
operation, VALIDATION, Lockbox, Forward, deployment, trading, or promotion is
authorized by this audit record.

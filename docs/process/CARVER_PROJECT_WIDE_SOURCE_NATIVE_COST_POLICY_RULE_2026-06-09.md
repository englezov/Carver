# Carver Project-Wide Source-Native Cost Policy Rule

Date: 2026-06-09

Status:

```text
PROJECT_WIDE_SOURCE_NATIVE_COST_POLICY_RULE_PROCESS_ONLY_NOT_PIPELINE_AUTHORIZATION
```

## Rule

Use book/source costs first. If the book gives explicit commissions, spreads, fees, slippage, multipliers, or cost assumptions, those are primary.

If the book does not specify enough costs, do not use our prop-firm, CFD, adapter, or personal trading costs. Deduce a plausible book-era/source-native retail futures cost model from capital size, instrument, contract type, and realistic retail broker fee schedules, and label it as an inferred cost assumption.

Prop-firm fees, evaluation fees, payout rules, CFD broker spreads, swaps, and adapter-specific costs are not source-faithful strategy costs.

## Consequence

Any strategy cost surface must be classified as one of:

```text
BOOK_EXPLICIT_COSTS
SOURCE_NATIVE_INFERRED_RETAIL_FUTURES_COSTS
FAIL_CLOSED_COSTS_UNRESOLVED
```

`PROP_FIRM_COSTS`, `CFD_COSTS`, `ADAPTER_COSTS`, and `PERSONAL_ACCOUNT_COSTS` are not source-faithful cost classes for Carver strategy evidence.

## Non-Authorization

This rule authorizes no provider/API access, downloads, data acquisition, backtests, diagnostics, result interpretation, tuning, Git actions, adapter work, deployment, trading, promotion, or source-faithful evidence claim. It is a project-wide governance rule to be carried into future S27 and next-lab migrations.

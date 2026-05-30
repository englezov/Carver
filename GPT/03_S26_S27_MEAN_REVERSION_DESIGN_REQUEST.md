# S26/S27 Mean Reversion Design Request

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_OPUS_DESIGN_REQUEST_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Objective

Design the source-faithful research path for Carver Strategies 26 and 27 from `00_Carver.pdf`.

The operator wants Opus to determine the path from the book before local implementation begins.

## Required Work

Use `00_Carver.pdf` as the source authority and identify the exact S26/S27 scope.

Extract:

- exact strategy names and page ranges;
- whether S26/S27 are mean-reversion strategies, sleeves, filters, overlays, or portfolio components;
- all formulas and rule definitions;
- all forecast definitions;
- forecast scalars;
- forecast caps;
- combination rules;
- required data fields;
- required instrument universe;
- eligible/ineligible instrument logic;
- costs, liquidity, risk, or minimum-capital constraints;
- required tables, figures, or appendices;
- any dependency on previous strategies or portfolio machinery;
- whether synthetic conformance can be tested without real data;
- what production atoms must remain unresolved before real-data work.

## Classification Needed

Classify each of S26 and S27 as one of:

```text
STANDALONE_CANDIDATE
SOURCE_NATIVE_PORTFOLIO_SLEEVE
PORTFOLIO_ONLY_COMPONENT
BLOCKED_SOURCE_UNRESOLVED
```

If the classification differs by test scope, state that explicitly.

## Desired Path

Design the next path in stages:

1. Source atom lock.
2. Synthetic conformance gate.
3. Local code/process implementation boundary.
4. First real-data gate, if appropriate.
5. Portfolio integration gate, if appropriate.
6. Production blockers and unresolved atoms.

The path should be hostile to overreach. If S26/S27 depend on data or source atoms not yet locked, say so.

## Questions To Answer

1. What exactly are Strategies 26 and 27 in the book?
2. What pages and tables must be cited?
3. Are they standalone mean-reversion candidates or portfolio sleeves?
4. What is the minimal synthetic test surface?
5. What is the minimal real-data surface after synthetic conformance?
6. Can the current 65-row Databento Dev/Reconciliation data-ready set support the first real-data gate, or is a smaller/different instrument set required?
7. Which parts must remain closed until later gates?

## Non-Authorization

This request authorizes no code execution, no file edits, no real-data parsing, no provider API access, no diagnostics, no backtests, no real-data forecasts, no positions, no position sizing, no costs, no carry, no trend computation, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote operations.

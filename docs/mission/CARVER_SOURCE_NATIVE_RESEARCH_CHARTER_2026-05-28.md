# Carver Source-Native Research Charter

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_NOT_PIPELINE_AUTHORIZATION
```

## Purpose

This charter defines the clean Carver research mission after retiring the messy local `QuantLab_v3` workspace from active pipeline use.

The mission is not to rescue old candidates. The mission is to dissect the Carver book systematically, map its strategies and portfolios, and test them through a clean source-native futures-first process.

## Mission Objectives

1. Extract and record the book strategy set, targeting approximately 30 futures strategies where the source supports that scope.
2. Build each individual strategy as a source-native futures candidate where possible.
3. Label each strategy before interpretation as one of:
   - `STANDALONE_CANDIDATE`
   - `SOURCE_NATIVE_PORTFOLIO_SLEEVE`
   - `PORTFOLIO_ONLY_COMPONENT`
   - `BLOCKED_SOURCE_UNRESOLVED`
4. Test standalone strategies individually only when the book/source framing supports standalone interpretation.
5. Treat source-described portfolio sleeves as sleeves, not as standalone family deaths.
6. Reconstruct each complete book portfolio as its own portfolio candidate after its member sleeves are source-locked.
7. Record failures as useful research output: mechanism failure, instrument mismatch, regime sensitivity, implementation ambiguity, source-data limitation, portfolio-dependency, or adapter/deployment mismatch.

## Source-Native First Rule

Discovery is source-native futures first.

CFD work is not discovery unless the source itself is CFD-native. A CFD translation may be opened later only as an explicit adapter lane after source-native behavior exists.

## Book-Instrument Preference

Prefer the instrument or market family named in the book. When a direct local source-native futures dataset is unavailable, record the blockage rather than silently substituting a CFD or adjacent ticker.

## Evidence Windows

The default research sequence is:

```text
Development/Reconciliation -> TEST -> VALIDATION -> LOCKBOX -> Forward
```

Development/Reconciliation is process/readiness work and not promotion evidence.

Any diagnostic or backtest over 2 years requires explicit operator approval.

## Portfolio Rule

A complete book portfolio is tested as a portfolio candidate, not inferred from isolated sleeve results.

Portfolio work must lock:

- member strategies;
- source-native instruments;
- rebalance and weighting rules;
- costs and target units;
- calendar/session conventions;
- window budget;
- sleeve fail-closed behavior;
- no post-result sleeve selection or rescue.

## Non-Authorization

This charter authorizes no data export, no parsing, no implementation, no tests/backtests, no strategy computation, no OOS, no Lockbox, no Forward, no deployment, no trading, and no promotion.

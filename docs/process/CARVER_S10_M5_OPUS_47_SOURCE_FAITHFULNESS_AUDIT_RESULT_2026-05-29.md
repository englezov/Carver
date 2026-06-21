# Carver S10/M5 Opus 4.7 Source-Faithfulness Audit Result

Date: 2026-05-29

Status:

```text
OPUS_47_HOSTILE_AUDIT_RESULT_CARVER_S10_M5_PASS_PROCESS_AND_SYNTHETIC_SCOPE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the Opus 4.7 hostile source-faithfulness and governance audit result for the Carver S10/M5 carry packet as a separate audit-result artifact.

This file intentionally keeps the audit result outside the implementation conformance record, following the audit hygiene recommendation that future audits should not be embedded as self-attestation inside the object under audit.

## Audited Packet

Packet folder:

```text
GPT/OPUS_47_S10_CARRY_SOURCE_FAITHFULNESS_AUDIT_PACK_2026-05-29
```

Audit-input files:

```text
01_POST_S10_M5_NEXT_STEP_DECISION.md
02_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE.md
03_M5_SYNTHETIC_CODE.py
04_M5_SYNTHETIC_TESTS.py
05_S10_CARRY_SOURCE_EXTRACT_PACK.md
```

Declared scope:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Audit Method

The audit was read-only.

The audit did not execute tests, real data, market-row parsing, NinjaTrader export, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, promotion, remote operations, or old `QuantLab_v3` active pipelines.

## Disposition

Opus 4.7 reported:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_SCOPE
```

The audit found no Critical or High severity issues.

## Verified Scope

Opus verified that:

- M5 stops at risk-adjusted carry forecast input only.
- M5 does not emit trading signals, positions, performance metrics, returns, PnL, Sharpe, drawdown, diagnostics, backtests, or portfolio outputs.
- Production locks remain unresolved where they should: raw-carry sign convention beyond toy inputs, production held/comparison contract role, expiry calendar/day-count, roll-day handling, fixed-month commodity rules, seasonal policy, wrong-sign policy, cost eligibility, scalar, caps, FDM, forecast weighting, position sizing, and buffering.
- The synthetic implementation is compatible with the source-pack framing of carry measurement, annualization, and risk adjustment without claiming production authority.
- The post-S10/M5 next-step decision to extend S10 carry forecast-block machinery before S11 is process-safe.
- Carry5/20/60/120 smoothing spans, scalar 30, caps, cost eligibility, equal weights, and carry FDM are future S10 atoms, not current M5 outputs.
- S11, P06, P07, real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, promotion, tuning, remote operations, and old `QuantLab_v3` active-pipeline use remain closed.
- The source pack is narrow enough for this audit stage and does not copy the entire book.

## Forward Constraints From Low Findings

The audit listed low or informational residual findings. They are non-blocking for the current S10/M5 scope but become forward constraints.

### Explicit Source Locks Required Before Production

Future production-facing gates must not rely on all-`LOCKED` default source-lock ergonomics.

Before any production source, real-data caller, or broader S10 implementation is opened, source-lock status for each carry atom must be explicitly declared by the caller or gate:

- instrument identity;
- held contract rule;
- comparison contract rule;
- completed price rule;
- raw-carry sign convention;
- expiry distance and annualization;
- price risk;
- seasonal and wrong-sign policy.

### Synthetic Versus Production Labels

Future carry sign convention types should make synthetic and production labels explicit.

Acceptable future approaches include an enumerated convention or a validator that distinguishes labels such as:

```text
synthetic_*
production_*
```

The current M5 synthetic surface remains acceptable because its function names, test labels, and conformance documents repeatedly declare toy synthetic scope.

### Abstract Synthetic Fixtures

Future S10 carry forecast-block synthetic tests should prefer abstract toy contract specs over real-looking `ZN`, `MES`, or similar fixtures.

Reason:

```text
PREVENT_OPTICAL_COUPLING_BETWEEN_TOY_MATH_TESTS_AND_SOURCE_FLAGGED_REAL_INSTRUMENTS
```

### Separate Audit Result Files

Future gates should keep audit results in separate audit-result records rather than embedding pass/fail sections directly inside the implementation conformance artifact.

The implementation artifact may reference the audit result by date or file path after the separate record exists.

### Governance Text Pins Are Intentional

Tests that pin exact governance phrases are acceptable and desirable when they force re-affirmation of boundary changes.

## Future Source Extract Requirements

The current source pack is sufficient for the present audit disposition. Before future production source locks, narrow page-cited source extracts will be required for:

- production raw-carry sign convention by instrument class;
- production annualization day-count rule;
- production seasonal and wrong-sign policy;
- production smoothing span rationale;
- production scalar and cap values;
- production cost and turnover eligibility rule;
- production equal forecast weights and FDM;
- S11 trend/carry combination, only when S11 is explicitly opened later.

These extracts must remain narrow and page-cited. Do not copy the entire book into the repository or audit packet.

## Next Clean Step

The next clean process step is:

```text
CARVER_S10_CARRY_FORECAST_BLOCK_EXTENSION_GATE_DRAFT
```

That draft may define a future synthetic-only gate for:

```text
M5 risk-adjusted carry input
-> Carry5/20/60/120 smoothing
-> scalar 30
-> caps
-> eligible carry span set
-> equal weights
-> carry FDM
-> final capped S10 carry forecast output
```

No implementation is authorized by this audit result.

## Non-Authorization

This record authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no S10 implementation, no S11, no P06/P07 portfolio work, no Opus execution, no remote push, and no GitHub action.

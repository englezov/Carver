# Carver S27 Scalar Blocker Local Lean Hostile Audit

Date: 2026-06-01

Mode: Local hostile audit over the S27 scalar blocker disposition. No provider API access, no data download, no market-row parsing, no diagnostics, no backtest rerun, no positions, no costs, no tuning, no promotion, and no Git operation.

## Finding Review

### Critical

None.

### High

None.

### Medium

None.

### Low

None.

## Source-Faithfulness Check

The scalar concern was that S27 forecast artifacts record `forecast_scalar = 20.0`, while S26 uses scalar `9.3`.

Direct source check against `Carver.pdf` resolves the concern:

```text
S26 scalar: 9.3, p. 480
S27 scalar: around 20 after trend overlay and volatility multiplier, p. 502
S27 cap: common forecast cap +/-20
```

The current code preserves this split:

```text
S26_FORECAST_SCALAR = 9.3
S27_FORECAST_SCALAR = 20.0
```

The stale phrase "inherits S26 scalar 9.3" was corrected in the handoff documentation, and the S27 source-lock field/label was hardened from inherited-scalar wording to S27-specific scalar wording.

## Verification

Synthetic/unit verification:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
```

Result:

```text
42 tests passed
```

Full local unit verification:

```text
python -m unittest discover -s tests -v
```

Result:

```text
198 tests passed
1 skipped
```

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_SCALAR_BLOCKER_RESOLVED_SOURCE_FAITHFUL_20_0
```

This audit resolves only the scalar-specific blocker. It does not bless strategy performance, the backtest window, execution semantics, cost assumptions, signal-lane adaptation, CFD adaptation, OOS, Lockbox, deployment, trading, or promotion.

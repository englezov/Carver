# Carver S09 Phase-1 Multi-Instrument Forecast Conformance Surface

Status: `PROCESS_AND_SYNTHETIC_CODE_CARVER_S09_PHASE1_MULTI_INSTRUMENT_FORECAST_CONFORMANCE_NOT_DIAGNOSTIC_NOT_BACKTEST`

Date: 2026-05-29

## Purpose

Add the first forecast-only bridge from the phase-1 source-native daily futures data surface into S09 across the small multi-asset seed set: MES / ZN / ZF.

This is a conformance surface only. It checks whether ready continuous daily chains and prevalidated daily price-risk inputs can produce S09 EWMAC32 / EWMAC64 forecast blocks per instrument. It is not a portfolio construction gate.

## Scope

The surface is locked to:

- Lane class: `SOURCE_NATIVE_FUTURES`
- Roots: `MES`, `ZN`, `ZF`
- Contract chain months: `09-25`, `12-25`, `03-26`, `06-26`
- Required adjusted daily bars: `257`
- Forecast rules: EWMAC32 and EWMAC64 only
- Input state: completed daily bars only, ready continuous chains only, daily price risk timestamp aligned to the final adjusted bar

The surface consumes `Phase1ContinuousReadinessReport` and one `ContinuousChainBuildResult` per root. It produces one S09 forecast result per root.

## Explicit Non-Authorization

No returns, PnL, Sharpe, drawdown, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab imports, tuning, deployment, trading, promotion, or remote push are authorized by this artifact.

The output is not an interpretable portfolio signal. The result type carries `interpretable_portfolio_signal = False` and an empty performance metric set by construction.

## Gate Behaviour

The code must fail closed when:

- the readiness report is not fully ready,
- the roots are missing, extra, or out of order,
- the adjusted bars do not match the declared root,
- the source contract month chain differs from the phase-1 locked chain,
- fewer than 257 adjusted daily bars are available,
- daily price risk is not finite, positive, or timestamp-aligned,
- any non-source-native lane is supplied,
- any rule set other than EWMAC32 / EWMAC64 is supplied.

## Portfolio Construction Boundary

This surface deliberately stops before portfolio construction. The next gate may use these forecast-only per-instrument results as a source dependency, but it must separately authorize portfolio construction rules, instrument weights, IDM treatment, buffering/rounding interaction, cost handling, and any real-data execution path.

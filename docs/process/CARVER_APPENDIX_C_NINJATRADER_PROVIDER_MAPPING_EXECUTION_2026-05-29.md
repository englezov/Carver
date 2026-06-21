# Carver Appendix C NinjaTrader Provider Mapping Execution

Date: 2026-05-29

Status:

```text
PROCESS_SOURCE_CARVER_APPENDIX_C_NINJATRADER_PROVIDER_MAPPING_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Create a process/source provider mapping artifact for the audited Appendix C 102-row source universe using only the clean NinjaTrader static instrument evidence intake.

This is not real market data, not provider API access, not NinjaTrader historical export, not market-row parsing, not diagnostics, not a backtest, not contract-identity readiness, not session/roll readiness, not production data readiness, not deployment, not trading, and not promotion.

## Inputs

Audited Appendix C machine-readable source universe:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
```

Static provider evidence:

```text
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

Static evidence intake record:

```text
docs/process/CARVER_NINJATRADER_STATIC_INSTRUMENT_EVIDENCE_INTAKE_2026-05-29.md
```

## Output

Provider mapping artifact:

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
```

SHA-256:

```text
80c7f52fe599318fe6e095c7f6105b6b9646fc2f35dc1ccf821bcc2afe3586ce
```

Row count:

```text
102
```

## Mapping Status Counts

```text
MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW: 41
BLOCKED_UNAVAILABLE: 59
BLOCKED_CONTRACT_VARIANT_MISMATCH: 2
```

No row is marked:

```text
MAPPED_SOURCE_NATIVE_EXACT
```

because the NinjaTrader static extract provides a platform master-instrument candidate, raw currency code, point value, trading-hours template, and sanitized symbol-mapping tokens, but it does not normalize every Appendix C source exchange, currency, multiplier, and variant into a production contract-identity lock.

## Conservative Mapping Rules

The execution used only exact `author_market_code` to `ninjatrader_master_name` matching.

Rules:

- no code match in NinjaTrader futures master -> `BLOCKED_UNAVAILABLE`;
- multiple code matches -> `BLOCKED_AMBIGUOUS`;
- exact code match with no direct contradiction -> `MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW`;
- exact code match with source-family contradiction -> fail closed as `BLOCKED_CONTRACT_VARIANT_MISMATCH`;
- no nearby-market matching;
- no full-size/micro/mini substitution;
- no CFD, ETF, cash-index, option, spread, or synthetic proxy substitution;
- no portfolio member dropping;
- no portfolio reweighting.

## Explicit Variant Blocks

Two rows are blocked as source-family contradictions in the static NinjaTrader evidence:

```text
APPENDIX_C_179_004 / EUR / EUR/USD
APPENDIX_C_180_006 / MXP / MXP/USD
```

The NinjaTrader static evidence does not provide exact source-native matches for those Appendix C identities under the same author market code. The mapping therefore fails closed rather than substituting a nearby FX, crypto, or alternate provider symbol.

## Review-Required Candidate Meaning

`MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW` means:

- the Appendix C author market code exists as a NinjaTrader futures master instrument;
- the row has a plausible static source-native provider candidate;
- the row is not production-ready;
- contract identity, exchange normalization, currency normalization, multiplier semantics, active status, delivery cycle, roll behavior, trading hours, and completed-bar rules remain unresolved.

It does not authorize real-data access, provider API use, historical export, market-row parsing, diagnostics, backtests, position sizing, execution, deployment, trading, or promotion.

## Downstream Required Gates

Before any real-data Development/Reconciliation gate can be considered, the mapped and blocked rows require separate gates for:

- contract identity/readiness;
- session/roll/completed-bar readiness;
- risk, FX, cost, and carry-leg readiness;
- unresolved and blocked member policy;
- lean hostile audit of this provider mapping artifact.

## Non-Authorization

This provider mapping execution authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no silent substitution/drop/reweight, no Opus/GPT execution, no remote push, and no GitHub action.

# Carver Appendix C Static Contract Specification Evidence Intake

Date: 2026-05-29

Status:

```text
PROCESS_SOURCE_CARVER_APPENDIX_C_STATIC_CONTRACT_SPECIFICATION_EVIDENCE_INTAKE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Create a static source-native contract specification evidence intake packet for the Appendix C NinjaTrader review-required and blocked rows before any contract identity execution gate.

This intake uses only the currently authorized Carver static evidence:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
```

No external exchange or provider contract specification page was named or ingested in this gate.

## Output

Machine-readable static contract specification evidence intake:

```text
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-29.csv
```

SHA-256:

```text
9b6c915d91321b4809a2bbe7032cbb602a8092347ccee365a4f027f7f837a6af
```

Row count:

```text
102
```

## Evidence Status Counts

```text
STATIC_PROVIDER_MASTER_FIELDS_PRESENT_REQUIRES_CONTRACT_SPEC_REVIEW: 41
NO_STATIC_PROVIDER_MASTER_CONTRACT_SPEC_AVAILABLE_FOR_ROW: 59
STATIC_PROVIDER_MASTER_FIELDS_PRESENT_BUT_PROVIDER_MAPPING_VARIANT_BLOCKED: 2
```

## Included Static Fields

Where present in the NinjaTrader static master evidence, the intake records:

- provider master name;
- provider contract family text;
- provider exchange tokens;
- raw provider currency code;
- provider point value;
- tick size;
- candidate tick value derived from point value times tick size;
- trading-hours template name;
- server-supported static master flag;
- provider mapping status;
- local canonical instrument id;
- source Appendix C exchange, currency, multiplier, and first source year.

## Deliberately Unlocked Fields

The intake does not lock:

- exchange normalization;
- currency normalization;
- source multiplier semantics;
- provider point-value semantics;
- tick value;
- active tradability;
- delivery cycle;
- roll rules;
- session calendar;
- completed-bar timestamp policy;
- contract identity;
- market data readiness.

Derived candidate tick values are explicitly marked:

```text
DERIVED_CANDIDATE_FROM_POINT_VALUE_TIMES_TICK_SIZE_NOT_LOCKED
```

They are not production tick-value locks.

## Missing External Spec Pages

No provider or exchange static contract specification page was ingested.

Rows with no exact NinjaTrader static futures master candidate remain:

```text
NO_STATIC_PROVIDER_MASTER_CONTRACT_SPEC_AVAILABLE_FOR_ROW
```

Rows already blocked by provider mapping variant mismatch remain:

```text
STATIC_PROVIDER_MASTER_FIELDS_PRESENT_BUT_PROVIDER_MAPPING_VARIANT_BLOCKED
```

These statuses preserve the fail-closed provider mapping outcome rather than substituting nearby symbols.

## Future Contract Identity Use

A future contract identity execution gate may consume this intake packet as one evidence source, but it must not treat this packet as sufficient by itself to lock production identity.

Before a row can be locked, the future gate must still resolve or fail close:

- exchange equivalence;
- currency equivalence;
- multiplier semantics;
- point value semantics;
- tick value;
- active status;
- contract family;
- contract variant;
- delivery cycle;
- local canonical ID stability.

## Non-Authorization

This evidence intake authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no silent substitution/drop/reweight, no contract identity execution, no production contract identity lock, no market data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.

## Next Clean Gate

This intake should receive a lean regular hostile audit before it is used as locked process/source evidence.

After a clean audit, the next gate can be a process/source contract identity execution gate. That later gate must decide whether this static evidence is enough for any row, and which rows still require external exchange/provider contract specification pages.

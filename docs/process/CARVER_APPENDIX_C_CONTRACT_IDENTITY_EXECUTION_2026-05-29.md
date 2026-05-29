# Carver Appendix C Contract Identity Execution

Date: 2026-05-29

Status:

```text
PROCESS_SOURCE_CARVER_APPENDIX_C_CONTRACT_IDENTITY_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Create a process/source contract identity status artifact for the Appendix C rows using the audited static evidence stack available in Carver.

This is not market data readiness, not session readiness, not roll readiness, not completed-bar readiness, not risk readiness, not cost readiness, not carry-leg readiness, not diagnostics, not a backtest, not deployment, not trading, and not promotion.

## Inputs

Audited Appendix C source universe:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
```

NinjaTrader static instrument extract:

```text
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

Provider mapping artifact:

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
```

Static contract specification evidence intake:

```text
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-29.csv
```

Static contract specification evidence intake audit:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_SOURCE_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_SCOPE
```

## Output

Contract identity status artifact:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATUS_2026-05-29.csv
```

SHA-256:

```text
5ea130cf855845b948e66881784990fe7f1dd41f765f95df09a025dd673c85c2
```

Row count:

```text
102
```

## Status Counts

```text
CONTRACT_IDENTITY_REQUIRES_REVIEW: 41
CONTRACT_IDENTITY_BLOCKED_UNAVAILABLE: 59
CONTRACT_IDENTITY_BLOCKED_VARIANT_MISMATCH: 2
CONTRACT_IDENTITY_LOCKED_SOURCE_NATIVE: 0
```

## Execution Rules

The execution is fail-closed:

- rows with static NinjaTrader master fields but no external/provider/exchange contract specification page are `CONTRACT_IDENTITY_REQUIRES_REVIEW`;
- rows without an exact NinjaTrader static futures master candidate are `CONTRACT_IDENTITY_BLOCKED_UNAVAILABLE`;
- rows already blocked by provider mapping variant mismatch are `CONTRACT_IDENTITY_BLOCKED_VARIANT_MISMATCH`;
- no row is dropped;
- no row is substituted;
- no row is reweighted;
- no row is marked `CONTRACT_IDENTITY_LOCKED_SOURCE_NATIVE`.

## What Remains Unresolved

For the 41 review-required rows, the following remain unresolved:

- exchange normalization;
- raw NinjaTrader currency-code normalization;
- source multiplier versus provider point-value semantics;
- tick value as a production lock;
- active tradability;
- delivery cycle;
- local session calendar;
- roll rules;
- completed-bar timestamp policy;
- market data readiness.

For the 59 unavailable rows and 2 variant-mismatch rows, contract identity remains fail-closed until separate static source-native evidence is introduced.

## Non-Authorization

This contract identity execution authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no silent substitution/drop/reweight, no production contract identity lock, no market data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.

## Next Clean Gate

This execution artifact should receive a lean regular hostile audit before it is treated as locked.

After a clean audit, the next process-only chapter may be:

```text
APPENDIX_C_SESSION_ROLL_COMPLETED_BAR_READINESS_SHAPE_GATE
```

That next chapter must consume the contract identity status artifact as evidence and must keep real market data closed.

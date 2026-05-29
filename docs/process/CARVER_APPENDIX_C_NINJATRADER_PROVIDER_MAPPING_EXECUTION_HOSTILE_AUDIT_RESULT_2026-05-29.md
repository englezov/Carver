# Carver Appendix C NinjaTrader Provider Mapping Execution Hostile Audit Result

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_APPENDIX_C_NINJATRADER_PROVIDER_MAPPING_EXECUTION_HOSTILE_AUDIT_RESULT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Scope

Preserve the lean regular hostile audit result for the Appendix C NinjaTrader source-native provider mapping execution artifact.

Audited files:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
docs/process/CARVER_APPENDIX_C_NINJATRADER_PROVIDER_MAPPING_EXECUTION_2026-05-29.md
docs/process/CARVER_NINJATRADER_STATIC_INSTRUMENT_EVIDENCE_INTAKE_2026-05-29.md
```

Mode:

```text
READ_ONLY_LEAN_HOSTILE_AUDIT_BY_SUBAGENT
```

No edits, tests, real market data, market-row parsing, provider API access, NinjaTrader export, diagnostics, backtests, QuantLab access, or remote operations were performed by the audit.

## Findings

No Critical, High, or Medium findings.

LOW, non-blocking:

```text
The 41 mapped rows are deliberately marked MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW,
not exact. This is correct, but downstream readers must keep treating them as
candidates only because currency, multiplier semantics, exchange normalization,
active status, delivery cycle, session, roll, and completed-bar rules remain
unresolved.
```

Informational checks:

- all 102 Appendix C rows are preserved;
- no dropped rows, extra rows, or duplicate `row_id` values were found;
- status counts are `MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW: 41`, `BLOCKED_UNAVAILABLE: 59`, and `BLOCKED_CONTRACT_VARIANT_MISMATCH: 2`;
- all `mapping_status` values are from the allowed set;
- no row claims `MAPPED_SOURCE_NATIVE_EXACT`;
- the `EUR` and `MXP` variant blocks are source/governance consistent;
- real data, market-row parsing, NinjaTrader export, diagnostics, backtests, production readiness, deployment, trading, promotion, substitution, dropping, and reweighting remain closed.

## Disposition

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_SOURCE_PROVIDER_MAPPING_EXECUTION_SCOPE
```

## Non-Authorization

This audit-result record authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no silent substitution/drop/reweight, no Opus/GPT execution, no remote push, and no GitHub action.

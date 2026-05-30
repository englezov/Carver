# Lean Hostile Audit Result - Databento Appendix C Alias Mapping Evidence Gate

Date: 2026-05-30

Mode: Local hostile audit of process/source artifacts only. No OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote operations.

## Findings

### Critical

None.

### High

None.

### Medium

None.

### Low

`APPENDIX_C_175_004` (`SMI -> FSMI.c.0`) is intentionally fail-closed despite official evidence identifying `FSMI` as the SMI futures product family. This is correct because the Appendix C lock records `SOFFEX` and `EUR`, while official static evidence points to a Eurex/SIX Swiss index derivative with CHF point-value semantics. A later gate must resolve that currency/venue normalization explicitly.

`APPENDIX_C_175_005` (`DJ200S`) corrects the prior Databento candidate from `FXXS.c.0` to `FSCP.c.0`. The artifact explicitly blocks the superseded `FXXS.c.0` candidate, so no silent substitution is present.

## Audit Checks

```text
INPUT_ALIAS_ROWS_PRESERVED: YES
RESOLVED_OR_FAIL_CLOSED_EACH_ROW: YES
OFFICIAL_STATIC_EVIDENCE_RECORDED: YES
DATABENTO_METADATA_ONLY_BOUNDARY_PRESERVED: YES
OHLCV_DOWNLOAD_AUTHORIZED: NO
MARKET_ROW_ACCESS: NO
STRATEGY_USE_AUTHORIZED: NO
NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT: YES
```

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_DATABENTO_APPENDIX_C_ALIAS_MAPPING_EVIDENCE_PRE_REAL_DATA_SCOPE
```

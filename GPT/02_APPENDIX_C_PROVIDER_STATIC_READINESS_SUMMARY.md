# Appendix C Provider And Static Readiness Summary

Date: 2026-05-30

Status:

```text
OPUS_INPUT_PACKET_APPENDIX_C_PROVIDER_STATIC_READINESS_SUMMARY_NOT_EXECUTION
```

## Source Claim Under Audit

The Carver process treats Appendix C, pages 690-695, Tables 172-183 in `00_Carver.pdf` as the complete 102-instrument Jumbo futures source universe.

Machine-readable local lock:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
rows: 102
sha256: 9453A9635148AE4D998306E0AC921C534D35D4D97DDE3934C8AEA02104E48C5F
```

The audit should verify:

- whether the 102-row interpretation is source-faithful to Appendix C;
- whether the local row identity is treated as source authority rather than as provider readiness;
- whether the chapter correctly separates book universe identity from NinjaTrader executability.

## NinjaTrader Static Mapping

Local static evidence source:

```text
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

Mapping artifact:

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
rows: 102
sha256: 80C7F52FE599318FE6E095C7F6105B6B9646FC2F35DC1CCF821BCC2AFE3586CE
```

Mapping disposition:

```text
MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW: 41
BLOCKED_UNAVAILABLE: 59
BLOCKED_CONTRACT_VARIANT_MISMATCH: 2
```

Review status:

```text
REQUIRES_CONTRACT_IDENTITY_REVIEW: 41
BLOCKED: 61
```

Substitution status:

```text
FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT: 41
NO_SUBSTITUTION_ATTEMPTED: 61
```

The packet claims this is governance-safe because no missing Appendix C row is dropped from the source universe, no adjacent symbol is substituted, and no portfolio weights are rebalanced around NinjaTrader availability.

## Data-Source Finalization Decision

Decision artifact:

```text
docs/process/CARVER_APPENDIX_C_NINJATRADER_DATA_SOURCE_FINALIZATION_DECISION_2026-05-30.md
```

Decision summary:

```text
APPENDIX_C_SOURCE_CANONICAL
PRACTICAL_DATA_SOURCE_CANDIDATE = NINJATRADER
HISTORICAL_BAR_AUTHORIZATION = NONE_EXCEPT_SEPARATELY_RECORDED_MES_06_26_TINY_QUARANTINE_SLICE
LANE_CLASS = SOURCE_NATIVE_FUTURES
```

The complete Appendix C Jumbo universe is not claimed as executable in NinjaTrader. The local path narrows to a NinjaTrader-supported subset and then a tiny MES-only pilot.

Exact-code NinjaTrader candidates listed by the decision:

```text
BZ, CAC40, EMD, GE, GF, HE, HG, HH, HO, KE, LE, M2K, MBT, MES, MGC, MNQ, MYM,
N1U, NIFTY, NOK, PA, PL, QG, QM, RB, SEK, SI, TN, UB, Z3N, ZB, ZC, ZF, ZL,
ZM, ZN, ZO, ZR, ZS, ZT, ZW
```

These are candidates only, not data-ready rows.

Alias-required rows remain separately closed:

```text
AUD, CAD, CHF, EUR, GBP, JPY, MXP, NZD, ESTX50
```

## Contract Identity Hardening

Hardening update:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv
rows: 41
sha256: A5577BEBE57B637EB8BAE878641539290CB4468CE0DD9FFCC2CC66E70216B45E
```

Disposition:

```text
UNRESOLVED_FAIL_CLOSED: 33
BLOCKED_FAIL_CLOSED: 8
production_contract_identity_lock_status NOT_LOCKED: 41
data_intake_readiness_status NOT_READY_FOR_MARKET_ROW_INTAKE: 41
```

Representative blockers include unresolved quote-unit locks, delivery-cycle locks, exchange label reconciliation, source-name reconciliation, provider tick mismatches, active/retirement review, and product/variant reconciliation.

## Session/Roll/Completed-Bar Readiness

Readiness artifact:

```text
docs/researchops/session_roll/CARVER_APPENDIX_C_SESSION_ROLL_COMPLETED_BAR_READINESS_STATUS_2026-05-29.csv
rows: 102
sha256: A9EA3963304F6BFE5DA5C290BEC42095F85031D77736BCD95AC677DE465ABF16
```

Disposition:

```text
SESSION_ROLL_BLOCKED_CONTRACT_IDENTITY: 61
SESSION_ROLL_BLOCKED_NO_COMPLETED_BAR_POLICY: 41
production_session_roll_lock_status NOT_LOCKED: 102
market_row_access_status NO_MARKET_ROW_ACCESS: 102
```

## Risk/FX/Cost/Carry-Leg Readiness

Readiness artifact:

```text
docs/researchops/risk_fx_cost_carry_leg/CARVER_APPENDIX_C_RISK_FX_COST_CARRY_LEG_READINESS_STATUS_2026-05-29.csv
rows: 102
sha256: 6283DDC306ECAF646EB374F2BDC82C6A3B77F97ED342A71816F634657CE2CFAE
```

Disposition:

```text
RISK_FX_COST_CARRY_LEG_BLOCKED_CONTRACT_IDENTITY: 61
RISK_FX_COST_CARRY_LEG_BLOCKED_SESSION_ROLL_COMPLETED_BAR: 41
production_risk_fx_cost_carry_leg_lock_status NOT_LOCKED: 102
market_row_access_status NO_MARKET_ROW_ACCESS: 102
```

## 16-Row Pilot Block

Selected 16-row pilot:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

Static policy readiness refresh:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_2026-05-30.csv
rows: 16
sha256: 733B8F0ADBA8051DB6724CF4077CD4D322507DD76E841D4084751523C7F052BC
```

Disposition:

```text
STATIC_POLICY_READINESS_REFRESH_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
ready_for_tiny_historical_bar_intake NO: 16
```

This is the reason the chapter did not open a 16-row data pull.

## Audit Risk Points

The reviewer should attack these points:

- Does any artifact imply the full 102-row Appendix C Jumbo universe is executable in NinjaTrader?
- Does the 41-row exact-code candidate set silently become data-ready?
- Are alias-required rows treated as mapped without a separate alias gate?
- Are the 16 pilot rows blocked consistently before MES-only reduction?
- Does any wording imply that static evidence is equivalent to historical-bar availability?
- Does any document drop, substitute, or reweight missing Appendix C rows?

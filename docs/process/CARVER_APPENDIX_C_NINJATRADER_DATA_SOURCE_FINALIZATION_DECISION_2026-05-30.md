# Carver Appendix C NinjaTrader Data-Source Finalization Decision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_APPENDIX_C_NINJATRADER_DATA_SOURCE_FINALIZATION_DECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Close the Appendix C readiness interpretation around NinjaTrader as the practical local source-native futures data source.

This decision distinguishes:

- the full 102-row Appendix C source universe from the Carver book;
- the current NinjaTrader static-master exact-code candidate set;
- alias-required rows that may be supported through NinjaTrader symbols different from Appendix C author codes;
- unavailable, variant-mismatch, unresolved, and blocked rows;
- the next clean gate toward a tiny first NinjaTrader historical-bar intake pilot.

This is a process-only decision. It is not real-data access, not market-row parsing, not a NinjaTrader historical export, not a provider API call, not a diagnostic, not a backtest, and not trading readiness.

## Inputs

Appendix C machine-readable source universe:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
```

NinjaTrader static instrument master extract:

```text
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

NinjaTrader source-native provider mapping:

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
```

Contract identity static hardening update:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv
```

Static contract specification evidence intake:

```text
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv
```

No market rows, historical bars, NinjaTrader historical exports, provider APIs, diagnostics, or backtests were used.

## Decision

The full Appendix C 102-row universe remains the canonical book source universe:

```text
APPENDIX_C_SOURCE_CANONICAL
```

NinjaTrader is selected as the practical local source-native futures data source for the next readiness branch:

```text
PRACTICAL_DATA_SOURCE_CANDIDATE = NINJATRADER
HISTORICAL_BAR_AUTHORIZATION = NONE_EXCEPT_SEPARATELY_RECORDED_MES_06_26_TINY_QUARANTINE_SLICE
LANE_CLASS = SOURCE_NATIVE_FUTURES
```

The complete Appendix C Jumbo universe is not currently executable in NinjaTrader. Missing or ambiguous rows are not treated as project failure and must not be silently dropped, substituted, or reweighted inside a book-Jumbo claim.

The near-term branch is therefore:

```text
APPENDIX_C_SOURCE_CANONICAL
-> NINJATRADER_SUPPORTED_SUBSET_READINESS
-> TINY_NINJATRADER_HISTORICAL_BAR_INTAKE_PILOT_SHAPE
```

The next branch does not claim:

```text
COMPLETE_APPENDIX_C_JUMBO_PORTFOLIO_READY
```

## Current Classification Counts

Provider mapping against the NinjaTrader static master:

```text
MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW: 41
BLOCKED_UNAVAILABLE: 59
BLOCKED_CONTRACT_VARIANT_MISMATCH: 2
```

Static contract identity hardening update for the 41 exact-code candidates:

```text
UNRESOLVED_FAIL_CLOSED: 33
BLOCKED_FAIL_CLOSED: 8
LOCKED_STATIC_SOURCE_NATIVE: 0
NOT_READY_FOR_MARKET_ROW_INTAKE: 41
```

The 41 exact-code candidates are not yet real-data ready. They are only the exact-code NinjaTrader-supported candidate set for future static readiness work.

## Exact-Supported Candidate Set

The following Appendix C author market codes were found as exact NinjaTrader static-master candidates and remain source-native candidates, but still fail closed pending contract identity/session/risk readiness:

```text
BZ, CAC40, EMD, GE, GF, HE, HG, HH, HO, KE, LE, M2K, MBT, MES, MGC, MNQ, MYM,
N1U, NIFTY, NOK, PA, PL, QG, QM, RB, SEK, SI, TN, UB, Z3N, ZB, ZC, ZF, ZL,
ZM, ZN, ZO, ZR, ZS, ZT, ZW
```

Interpretation:

```text
NINJATRADER_EXACT_SUPPORTED_REQUIRES_STATIC_READINESS
```

They are not:

```text
NINJATRADER_DATA_READY
```

## Alias-Required Candidate Set

Some Appendix C rows use author or broker-style codes that do not equal the local NinjaTrader master instrument name, but current static master evidence suggests plausible source-native futures aliases.

These rows require a separate alias-readiness gate before they can be used:

| Appendix C code | Description | NinjaTrader alias candidates | Status |
|---|---|---|---|
| `AUD` | AUD/USD | `6A`, `M6A` | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |
| `CAD` | CAD/USD | `6C`, `M6C`, `MICD` | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |
| `CHF` | CHF/USD | `6S`, `M6S`, `MISF` | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |
| `EUR` | EUR/USD | `6E`, `E7`, `M6E`; exact `EUR` is variant-mismatch | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |
| `GBP` | GBP/USD | `6B`, `M6B` | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |
| `JPY` | JPY/USD | `6J`, `M6J`, `MIJY` | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |
| `MXP` | MXP/USD | `6M`; exact `MXP` is Micro XRP variant-mismatch | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |
| `NZD` | NZD/USD | `6N` | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |
| `ESTX50` | EUROSTOXX 50 | `FESX`, `FSXE` | `NINJATRADER_ALIAS_REQUIRED_NOT_LOCKED` |

Alias rows must not be treated as mapped until a later process/source gate locks:

- source row identity;
- NinjaTrader master instrument identity;
- exchange and currency;
- multiplier and tick semantics;
- contract variant;
- no-substitution status;
- whether the alias preserves the source-native futures instrument.

## Unavailable Rows

Rows currently marked:

```text
BLOCKED_UNAVAILABLE: 59
```

remain fail-closed for NinjaTrader data-source readiness.

This class includes much of the global Appendix C breadth, especially European rates, many European/Asian equity index rows, sector futures, volatility rows, several cross/EM FX rows, and some commodity rows not found as exact NinjaTrader master instruments.

Interpretation:

```text
NINJATRADER_UNAVAILABLE_FAIL_CLOSED
```

These rows are not dropped from Appendix C. They remain in the canonical 102-row source universe but outside the practical NinjaTrader-supported pilot branch.

## Variant-Mismatch Rows

Rows currently marked:

```text
BLOCKED_CONTRACT_VARIANT_MISMATCH: 2
```

Exact-code variant mismatches include:

| Appendix C code | Source description | Exact NinjaTrader issue | Decision |
|---|---|---|---|
| `EUR` | EUR/USD | exact `EUR` does not resolve to a clean EUR/USD futures identity matching Appendix C | use alias-readiness gate for `6E`/`E7`/`M6E`; exact `EUR` remains blocked |
| `MXP` | MXP/USD | exact `MXP` resolves to Micro XRP Futures, not Mexican Peso futures | use alias-readiness gate for `6M`; exact `MXP` remains blocked |

Interpretation:

```text
NINJATRADER_VARIANT_MISMATCH_FAIL_CLOSED
```

## Unresolved And Blocked Exact-Supported Rows

Within the 41 exact-code NinjaTrader candidates:

```text
UNRESOLVED_FAIL_CLOSED: 33
BLOCKED_FAIL_CLOSED: 8
```

Unresolved exact-supported rows require final static readiness locks. Blocked exact-supported rows require explicit rejection or source repair before they can ever join a pilot.

High-risk blocked examples:

```text
Z3N: official/provider tick mismatch review required.
NOK, SEK: official/provider tick mismatch review required.
N1U: active/retired swap futures rulebook review required.
GE: Eurodollar retirement or transition review required.
NIFTY: SGX/GIFT/NSE IX/local provider variant reconciliation required.
SI: Appendix C multiplier and full Silver futures semantics conflict.
HH: product code or rulebook reconciliation required.
```

## Candidate Pilot Pool

The first NinjaTrader historical-bar intake pilot should be tiny and deliberately narrower than Appendix C.

Recommended candidate pool for the next process-only pilot shape gate:

```text
Rates: ZT, ZF, ZN
Equity index: MES, MNQ, M2K, MYM
Energy: QM, RB
Agriculture: ZC, ZS, ZM, ZL, ZW
Livestock: HE, LE
```

Rationale:

- all are source-native futures;
- all are present in the NinjaTrader static evidence stack as exact or near-standard CME Group futures candidates;
- they span rates, equities, energy, grains/oilseeds, and livestock;
- they avoid currently blocked rows such as `SI`, `NIFTY`, `GE`, `N1U`, `Z3N`, `NOK`, `SEK`, and `HH`;
- they avoid alias-required FX until alias rules are separately locked.

This candidate pool is not authorized for market-row intake. It is only the recommended universe for the next shape gate.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_UNIVERSE_SHAPE_AND_STATIC_READINESS_GATE
```

The next gate should:

- choose a tiny pilot subset from exact-supported NinjaTrader candidates;
- require final static contract identity locks for chosen rows;
- require session/calendar/completed-bar policy before any historical bars;
- require roll/back-adjustment/stale/missing-bar policy before any historical bars;
- require risk/FX/cost/carry-leg readiness status for chosen rows;
- keep alias-required rows closed unless a separate alias gate is opened;
- keep all unavailable and variant-mismatch rows fail-closed;
- explicitly state whether the first pilot is single-instrument or multi-instrument.

Only after that process-only shape gate passes should a later operator decide whether to authorize a tiny NinjaTrader historical-bar intake pilot.

## Still Closed

The following remain closed:

```text
real market data
NinjaTrader historical export
provider API access
market-row parsing
diagnostics
backtests
returns
PnL
Sharpe
drawdown
OOS
Lockbox
Forward
CFD adapters
old QuantLab pipeline use
tuning
deployment
trading
promotion
remote operations
```

## Non-Authorization

This decision authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

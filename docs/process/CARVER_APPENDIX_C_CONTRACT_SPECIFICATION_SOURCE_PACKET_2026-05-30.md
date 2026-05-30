# Carver Appendix C Contract Specification Source Packet

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_APPENDIX_C_CONTRACT_SPECIFICATION_SOURCE_PACKET_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Identify the official static exchange/provider contract specification evidence needed for the 41 Appendix C rows currently marked:

```text
CONTRACT_IDENTITY_HARDENING_FAIL_CLOSED_EXTERNAL_SPEC_REQUIRED
```

This packet is an evidence-source map only. It does not lock contract identity, does not normalize exchange or currency values, does not resolve multiplier semantics, does not prove active tradability, and does not authorize market-row access.

## Current Inputs

Contract identity static hardening record:

```text
docs/process/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_2026-05-30.md
```

Contract identity static hardening CSV:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_2026-05-30.csv
Rows: 41
SHA256: FC276F29599C27084F80E4EAFAD0E91BA7D138BEEA74E2C4C1F9FC0FED30708E
```

NinjaTrader static instrument master extract:

```text
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

The NinjaTrader static master is provider-side candidate evidence only. It is not official exchange contract-spec evidence and cannot, by itself, lock production contract identity.

## Source Universe Count

Rows requiring external static contract-spec evidence:

```text
41
```

Source exchange labels from Appendix C among those rows:

```text
ECBOT: 17
NYMEX: 11
GLOBEX: 10
CME: 1
MONEP: 1
SGX: 1
```

Rows where Appendix C source multiplier and NinjaTrader provider point value differ numerically:

```text
11
```

Those rows require special multiplier-semantics extraction from official contract specs before they can be locked or rejected:

```text
NIFTY, SI, ZC, GF, HE, LE, ZO, KE, ZS, ZL, ZW
```

## Minimum Evidence Fields

For each row, a later contract identity hardening gate must extract and record the following from the official static source:

- official exchange or venue identity;
- official product name and product code;
- currency or settlement currency;
- contract unit, contract size, point value, or multiplier semantics;
- price quotation unit;
- minimum tick size;
- tick value;
- active/listed/trading status or retirement/transition status;
- contract family;
- contract variant, such as micro, e-mini, ultra, last-day, financial, physical, swap, or cash-settled index future;
- delivery cycle, listed contract months, or expiry-month schedule;
- source URL or file path;
- retrieval date;
- source section or page anchor;
- whether the source is an exchange contract-spec page, exchange rulebook chapter, official exchange PDF, or provider static master page.

No field may be inferred from market prices, historical bars, daily settlements, chart pages, data exports, or provider APIs.

## Evidence Source Families

### CME Group Static Sources

Applies to rows with Appendix C source exchange labels `ECBOT`, `GLOBEX`, `NYMEX`, and `CME`, plus provider exchange-token variants `CBOT`, `CME`, `CME_CBT`, `COMEX`, and `NYMEX`.

Required source class:

```text
CME Group official contract-spec page, CME Group rulebook chapter, or CME Group official product PDF/fact card where the live contract-spec page is absent, retired, or insufficient.
```

The later execution gate must distinguish CME Group corporate source from the actual designated contract market where the contract is listed, such as CME, CBOT, NYMEX, or COMEX.

The later execution gate must not treat the CME product page quote, settlement, volume, open-interest, margin, chart, or historical-data tabs as market-row evidence. Only static contract-spec fields are in scope.

### Euronext Static Sources

Applies to the `CAC40` row.

Required source class:

```text
Euronext official CAC 40 index future contract-specification page and, if needed, related Euronext static documentation for expiry months, trading calendar, and delivery/settlement definitions.
```

The later execution gate must reconcile Appendix C source exchange label `MONEP` with the current official Euronext market/venue label. That reconciliation remains unresolved in this packet.

### SGX / NSE IX / GIFT Connect Static Sources

Applies to the `NIFTY` row.

Required source class:

```text
SGX official GIFT Connect / SGX-ICI source material and NSE IX official Nifty contract specification material.
```

This row is high risk because Appendix C records source exchange `SGX`, source currency `USD`, and source multiplier `2`, while the current NinjaTrader static candidate has point value `75.0` and no provider exchange tokens in the Carver extract. A future execution gate must not silently map old SGX Nifty, GIFT Nifty, NSE IX Nifty, or local NinjaTrader NIFTY variants together.

### NinjaTrader Static Master

Applies to every row as provider-side evidence only.

Required source class:

```text
NinjaTrader static instrument master extract already present in Carver.
```

This source can support provider candidate symbol, provider exchange tokens, raw currency code, point value, tick size, tick value, provider family text, and server-supported/static-master flags. It cannot prove official exchange identity, production active tradability, delivery cycle, or final source-native contract identity without official static exchange/provider evidence.

## Row-Level Evidence Targets

| Row | Code | Source name | Source exchange | Official static evidence target | Special evidence required before lock |
|---|---:|---|---|---|---|
| APPENDIX_C_172_001 | ZT | 2-year US | ECBOT | CME Group 2-Year U.S. Treasury Note futures contract specs: `https://www.cmegroup.com/markets/interest-rates/us-treasury/2-year-us-treasury-note.contractSpecs.html`; CME/CBOT rulebook chapter if needed. | Normalize ECBOT/CBOT/CME_CBT; lock USD currency mapping; lock Treasury point-value and 1/32-style tick semantics; lock active/listed status and delivery cycle. |
| APPENDIX_C_172_002 | Z3N | 3-year US | ECBOT | CME Group 3-Year U.S. Treasury Note futures contract specs: `https://www.cmegroup.com/markets/interest-rates/us-treasury/3-year-us-treasury-note.contractSpecs.html`; CME/CBOT rulebook chapter if needed. | Normalize ECBOT/CBOT/CME_CBT; lock USD currency mapping; lock Treasury point-value and tick semantics; lock active/listed status and delivery cycle. |
| APPENDIX_C_172_003 | ZF | 5-year US | ECBOT | CME Group 5-Year U.S. Treasury Note futures contract specs: `https://www.cmegroup.com/markets/interest-rates/us-treasury/5-year-us-treasury-note.contractSpecs.html`; CME/CBOT rulebook chapter if needed. | Normalize ECBOT/CBOT/CME_CBT; lock USD currency mapping; lock Treasury point-value and tick semantics; lock active/listed status and delivery cycle. |
| APPENDIX_C_172_004 | ZN | 10-year US | ECBOT | CME Group 10-Year U.S. Treasury Note futures contract specs: `https://www.cmegroup.com/markets/interest-rates/us-treasury/10-year-us-treasury-note.contractSpecs.html`; CME/CBOT rulebook chapter if needed. | Normalize ECBOT/CBOT/CME_CBT; lock USD currency mapping; lock Treasury point-value and tick semantics; lock active/listed status and delivery cycle. |
| APPENDIX_C_172_005 | TN | 10-year Ultra US | ECBOT | CME Group Ultra 10-Year U.S. Treasury Note futures contract specs: `https://www.cmegroup.com/markets/interest-rates/us-treasury/ultra-10-year-us-treasury-note.contractSpecs.html`; CME/CBOT rulebook chapter if needed. | Lock ultra variant; normalize ECBOT/CBOT; lock USD currency mapping; lock Treasury point-value and tick semantics; lock active/listed status and delivery cycle. |
| APPENDIX_C_172_006 | ZB | 20-year US | ECBOT | CME Group U.S. Treasury Bond futures contract specs: `https://www.cmegroup.com/markets/interest-rates/us-treasury/30-year-us-treasury-bond.contractSpecs.html`; CME/CBOT rulebook chapter if needed. | Reconcile Appendix C descriptive label `20-year US` to provider family `U.S. Treasury Bond Futures`; normalize ECBOT/CBOT/CME_CBT; lock USD currency mapping, point value, tick semantics, listed status, and delivery cycle. |
| APPENDIX_C_172_007 | UB | 30-year US | ECBOT | CME Group Ultra U.S. Treasury Bond futures contract specs: `https://www.cmegroup.com/markets/interest-rates/us-treasury/ultra-t-bond.contractSpecs.html`; CME/CBOT rulebook chapter if needed. | Lock ultra variant; normalize ECBOT/CBOT/CME_CBT; lock USD currency mapping, point value, tick semantics, listed status, and delivery cycle. |
| APPENDIX_C_172_009 | N1U | 10-year US Swap | ECBOT | CME Group official 10-Year Deliverable Interest Rate Swap futures materials, including CME Group N1U final settlement procedure PDF and CBOT Rulebook Chapter 53: `https://www.cmegroup.com/trading/interest-rates/files/final-10-year-deliverable-interest-rate-swap-futures-settlement-procedure.pdf` and `https://www.cmegroup.com/rulebook/CBOT/V/53.pdf`. | Provider exchange tokens are missing; lock N1U product identity, swap variant, physical delivery status, active/retired status, point value, tick value, and delivery cycle from official swap futures sources. |
| APPENDIX_C_172_010 | GE | Eurodollar | GLOBEX | CME Group Eurodollar futures contract specification or official Eurodollar archive/rulebook source: `https://www.cmegroup.com/pt/products/interest-rates/eurodollar.html`; CME Rulebook Chapter 452 if needed. | Treat as potentially retired/transitioned; lock GE product identity, active/retired status, USD currency, contract size, tick schedule, and quarterly/serial delivery cycle from official static sources only. |
| APPENDIX_C_174_001 | MYM | Dow Jones industrial (micro) | ECBOT | CME Group Micro E-mini Dow futures contract specs: `https://www.cmegroup.com/markets/equities/dow-jones/micro-e-mini-dow.contractSpecs.html`; CBOT rulebook chapter if needed. | Lock micro/e-mini variant; normalize ECBOT/CBOT; lock USD currency, point value, tick size/value, active/listed status, and equity index quarterly cycle. |
| APPENDIX_C_174_002 | MNQ | Nasdaq (micro) | GLOBEX | CME Group Micro E-mini Nasdaq-100 futures contract specs: `https://www.cmegroup.com/markets/equities/nasdaq/micro-e-mini-nasdaq-100.contractSpecs.html`; CME rulebook chapter if needed. | Lock micro/e-mini variant; normalize GLOBEX to exchange venue; lock USD currency, point value, tick size/value, active/listed status, and equity index quarterly cycle. |
| APPENDIX_C_174_004 | M2K | Russell 2000 smallcap (micro) | GLOBEX | CME Group Micro E-mini Russell 2000 futures contract specs: `https://www.cmegroup.com/markets/equities/russell/micro-e-mini-russell-2000.contractSpecs.html`; CME rulebook chapter if needed. | Lock micro/e-mini variant; normalize GLOBEX to exchange venue; lock USD currency, point value, tick size/value, active/listed status, and equity index quarterly cycle. |
| APPENDIX_C_174_005 | EMD | S&P 400 midcap (e-mini) | GLOBEX | CME Group E-mini S&P MidCap 400 futures contract specs: `https://www.cmegroup.com/markets/equities/sp/e-mini-sandp-midcap-400.contractSpecs.html`; CME rulebook chapter if needed. | Lock e-mini variant; normalize GLOBEX to exchange venue; lock USD currency, point value, tick size/value, active/listed status, and equity index quarterly cycle. |
| APPENDIX_C_174_006 | MES | S&P 500 (micro) | GLOBEX | CME Group Micro E-mini S&P 500 futures contract specs: `https://www.cmegroup.com/markets/equities/sp/micro-e-mini-sandp-500.contractSpecs.html`; CME rulebook chapter if needed. | Lock micro/e-mini variant; normalize GLOBEX to exchange venue; lock USD currency, point value, tick size/value, active/listed status, and equity index quarterly cycle. |
| APPENDIX_C_175_002 | CAC40 | French CAC 40 | MONEP | Euronext CAC 40 Index Future contract specification: `https://live.euronext.com/en/product/index-futures/FCE-DPAR/contract-specification`; related Euronext expiry-month and calendar static documents if needed. | Reconcile Appendix C `MONEP` label to current Euronext market/venue; lock EUR currency, EUR 10/index-point contract unit, tick value, active/listed status, and expiry-month schedule. |
| APPENDIX_C_177_004 | NIFTY | Indian NIFTY | SGX | SGX official GIFT Connect Nifty futures/options source: `https://www.sgx.com/derivatives/products/gift-connect?cc=GIN`; NSE IX official Nifty 50 index futures contract specifications; any official SGX Nifty transition/retirement notice needed to reconcile old SGX source identity. | High-risk identity mismatch. Must distinguish Appendix C SGX USD multiplier 2 from NinjaTrader provider point value 75.0. Do not lock until SGX/GIFT/NSE IX product identity, currency, multiplier, listed status, delivery cycle, and local provider variant are source-reconciled. |
| APPENDIX_C_179_007 | NOK | NOK/USD | GLOBEX | CME Rulebook Chapter 264 Norwegian krone/U.S. dollar futures: `https://www.cmegroup.com/content/dam/cmegroup/rulebook/CME/III/250/264/264.pdf`; CME FX product page if available. | Lock whether Appendix C `NOK/USD` and provider `Norwegian Krona Futures` are the same USD/NOK futures product; normalize GLOBEX/CME, currency quotation, contract size, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_179_009 | SEK | SEK/USD | GLOBEX | CME Group Swedish Krona futures contract specs: `https://www.cmegroup.com/markets/fx/g10/swedish-krona.contractSpecs.html`; CME Rulebook Chapter 265: `https://www.cmegroup.com/rulebook/CME/III/250/265/265.pdf`. | Lock whether Appendix C `SEK/USD` and provider `Swedish Krona Futures` are the same USD/SEK futures product; normalize GLOBEX/CME, currency quotation, contract size, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_181_002 | HG | Copper | NYMEX | CME Group Copper futures contract specs: `https://www.cmegroup.com/markets/metals/base/copper.contractSpecs.html`; COMEX rulebook chapter if needed. | Normalize Appendix C `NYMEX` versus provider `COMEX|CME`; lock USD currency, contract unit, tick size/value, active/listed status, and delivery cycle. |
| APPENDIX_C_181_003 | MGC | Gold (micro) | NYMEX | CME Group Micro Gold futures contract specs: `https://www.cmegroup.com/markets/metals/precious/e-micro-gold.contractSpecs.html`; COMEX rulebook/fact card if needed. | Normalize Appendix C `NYMEX` versus provider `COMEX`; lock micro variant, USD currency, contract unit, tick size/value, active/listed status, and delivery cycle. |
| APPENDIX_C_181_005 | PA | Palladium | NYMEX | CME Group Palladium futures contract specs: `https://www.cmegroup.com/markets/metals/precious/palladium.contractSpecs.html`; NYMEX rulebook chapter if needed. | Normalize NYMEX/CME tokens; lock USD currency, contract unit, tick size/value, active/listed status, and delivery cycle. |
| APPENDIX_C_181_006 | PL | Platinum | NYMEX | CME Group Platinum futures contract specs: `https://www.cmegroup.com/markets/metals/precious/platinum.contractSpecs.html`; NYMEX rulebook chapter if needed. | Normalize NYMEX/CME tokens; lock USD currency, contract unit, tick size/value, active/listed status, and delivery cycle. |
| APPENDIX_C_181_007 | SI | Silver | NYMEX | CME Group Silver futures contract specs: `https://www.cmegroup.com/markets/metals/precious/silver.contractSpecs.html`; COMEX rulebook chapter if needed. | Source multiplier 1000 differs from provider point value 5000. Must lock whether Appendix C intended mini/small silver or full SI; normalize NYMEX/COMEX, variant, contract unit, point value, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_181_008 | MBT | Bitcoin (micro) | CME | CME Group Micro Bitcoin futures contract specs: `https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.contractSpecs.html`; CME rulebook chapter if needed. | Lock micro/crypto variant, USD settlement, contract unit, tick size/value, active/listed status, and delivery cycle. |
| APPENDIX_C_182_001 | BZ | Brent Crude last day | NYMEX | CME Group Brent Last Day Financial futures contract specs: `https://www.cmegroup.com/markets/energy/crude-oil/brent-crude-oil-last-day.contractSpecs.html`; NYMEX rulebook chapter if needed. | Lock last-day and financial variant; normalize NYMEX; lock USD currency, barrel contract unit, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_182_002 | QM | WTI Crude (mini) | NYMEX | CME Group E-mini Crude Oil futures contract specs: `https://www.cmegroup.com/markets/energy/crude-oil/e-mini-crude-oil.contractSpecs.html`; NYMEX rulebook chapter if needed. | Lock mini/e-mini variant; normalize NYMEX/CME tokens; lock USD currency, barrel contract unit, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_182_003 | HH | Gas last day | NYMEX | CME Group Henry Hub Natural Gas Last Day Financial futures contract specs: `https://www.cmegroup.com/markets/energy/natural-gas/henry-hub-natural-gas-last-day-financial.contractSpecs.html`; NYMEX rulebook chapter if needed. | Lock last-day and financial variant; normalize NYMEX; lock USD currency, MMBtu contract unit, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_182_004 | RB | Gasoline | NYMEX | CME Group RBOB Gasoline futures contract specs: `https://www.cmegroup.com/markets/energy/refined-products/rbob-gasoline.contractSpecs.html`; NYMEX rulebook chapter if needed. | Lock physical variant, USD currency, gallons contract unit, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_182_005 | QG | Henry Hub Gas (mini) | NYMEX | CME Group E-mini Natural Gas futures contract specs or official CME Group Micro/E-mini/standard Henry Hub fact card where live spec page is insufficient: `https://www.cmegroup.com/markets/energy/natural-gas/e-mini-natural-gas.contractSpecs.html` and `https://www.cmegroup.com/markets/energy/files/micro-henry-hub-natural-gas-fact-card.pdf`. | Provider exchange tokens are missing. Lock mini/e-mini variant, financial/physical status, USD currency, MMBtu contract unit, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_182_006 | HO | Heating Oil | NYMEX | CME Group NY Harbor ULSD futures contract specs: `https://www.cmegroup.com/markets/energy/refined-products/heating-oil.contractSpecs.html`; NYMEX rulebook chapter if needed. | Reconcile Appendix C `Heating Oil` label to current `NY Harbor ULSD Futures`; lock USD currency, gallons contract unit, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_183_003 | ZC | Corn | ECBOT | CME Group Corn futures contract specs: `https://www.cmegroup.com/markets/agriculture/grains/corn.contractSpecs.html`; CBOT rulebook chapter if needed. | Source multiplier 5000 differs from provider point value 50. Must lock price quotation in cents/bushel versus bushel contract unit semantics; normalize ECBOT/CBOT/CME_CBT, active/listed status, and delivery cycle. |
| APPENDIX_C_183_004 | GF | Feeder Cattle | GLOBEX | CME Group Feeder Cattle futures contract specs: `https://www.cmegroup.com/markets/agriculture/livestock/feeder-cattle.contractSpecs.html`; CME rulebook chapter if needed. | Source multiplier 50000 differs from provider point value 500. Must lock price quotation and hundredweight contract unit semantics; normalize GLOBEX/CME, active/listed status, and delivery cycle. |
| APPENDIX_C_183_005 | HE | Lean Hogs | GLOBEX | CME Group Lean Hog futures contract specs: `https://www.cmegroup.com/markets/agriculture/livestock/lean-hogs.contractSpecs.html`; CME rulebook chapter if needed. | Source multiplier 40000 differs from provider point value 400. Must lock price quotation and hundredweight contract unit semantics; normalize GLOBEX/CME, active/listed status, and delivery cycle. |
| APPENDIX_C_183_006 | LE | Live Cattle | GLOBEX | CME Group Live Cattle futures contract specs: `https://www.cmegroup.com/markets/agriculture/livestock/live-cattle.contractSpecs.html`; CME rulebook chapter if needed. | Source multiplier 40000 differs from provider point value 400. Must lock price quotation and hundredweight contract unit semantics; normalize GLOBEX/CME, active/listed status, and delivery cycle. |
| APPENDIX_C_183_007 | ZO | Oats | ECBOT | CME Group Oats futures contract specs: `https://www.cmegroup.com/markets/agriculture/grains/oats.contractSpecs.html`; CBOT rulebook chapter if needed. | Source multiplier 5000 differs from provider point value 50. Must lock price quotation in cents/bushel versus bushel contract unit semantics; normalize ECBOT/CBOT/CME_CBT, active/listed status, and delivery cycle. |
| APPENDIX_C_183_008 | KE | Red Wheat | ECBOT | CME Group KC HRW Wheat futures contract specs: `https://www.cmegroup.com/markets/agriculture/grains/kc-hrw-wheat.contractSpecs.html`; CBOT/KCBT/CME rulebook source if needed. | Source multiplier 5000 differs from provider point value 50. Must lock product identity as KC HRW rather than Chicago SRW; normalize ECBOT/CBOT, quotation semantics, active/listed status, and delivery cycle. |
| APPENDIX_C_183_009 | ZR | Rice | ECBOT | CME Group Rough Rice futures contract specs: `https://www.cmegroup.com/markets/agriculture/grains/rough-rice.contractSpecs.html`; CBOT rulebook chapter if needed. | Normalize ECBOT/CBOT/CME_CBT; lock USD currency, contract unit, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_183_010 | ZS | Soybeans | ECBOT | CME Group Soybean futures contract specs: `https://www.cmegroup.com/markets/agriculture/oilseeds/soybean.contractSpecs.html`; CBOT rulebook chapter if needed. | Source multiplier 5000 differs from provider point value 50. Must lock price quotation in cents/bushel versus bushel contract unit semantics; normalize ECBOT/CBOT/CME_CBT, active/listed status, and delivery cycle. |
| APPENDIX_C_183_011 | ZM | Soybean Meal | ECBOT | CME Group Soybean Meal futures contract specs: `https://www.cmegroup.com/markets/agriculture/oilseeds/soybean-meal.contractSpecs.html`; CBOT rulebook chapter if needed. | Normalize ECBOT/CBOT/CME_CBT; lock USD currency, contract unit, short-ton quotation semantics, tick value, active/listed status, and delivery cycle. |
| APPENDIX_C_183_012 | ZL | Soybean Oil | ECBOT | CME Group Soybean Oil futures contract specs: `https://www.cmegroup.com/markets/agriculture/oilseeds/soybean-oil.contractSpecs.html`; CBOT rulebook chapter if needed. | Source multiplier 60000 differs from provider point value 600. Must lock price quotation in cents/pound versus pound contract unit semantics; normalize ECBOT/CBOT/CME_CBT, active/listed status, and delivery cycle. |
| APPENDIX_C_183_013 | ZW | Wheat | ECBOT | CME Group Chicago SRW Wheat futures contract specs: `https://www.cmegroup.com/markets/agriculture/grains/wheat.contractSpecs.html`; CBOT rulebook chapter if needed. | Source multiplier 5000 differs from provider point value 50. Must lock price quotation in cents/bushel versus bushel contract unit semantics; normalize ECBOT/CBOT/CME_CBT, active/listed status, and delivery cycle. |

## Evidence Extraction Rules For The Next Gate

A later contract-spec evidence intake gate may use the targets above to extract static fields into a machine-readable source packet. That later gate must:

- record one row per Appendix C hardening candidate;
- preserve all 41 row IDs;
- record `MAPPED`, `BLOCKED`, or `UNRESOLVED` only after source evidence is inspected;
- preserve source URLs and retrieval dates;
- hash any local static PDF or CSV evidence used;
- fail closed when a product page is absent, retired, ambiguous, or conflicts with Appendix C or NinjaTrader static fields;
- never substitute a related micro, mini, full-size, last-day, physical, financial, or successor product without an explicit source-transition record;
- treat provider exchange tokens and NinjaTrader point/tick fields as corroborating evidence, not as official exchange authority;
- preserve `NO_MARKET_ROW_ACCESS` for every row.

## Rows Requiring Special Attention

### Retired Or Transition-Prone Rates Products

Rows:

```text
N1U, GE
```

Required treatment:

- use CME official rulebook/archive/PDF evidence where live product pages are absent or insufficient;
- lock whether the contract is active, retired, transitioned, or historical-only;
- do not infer readiness from stale NinjaTrader static master presence.

### FX Quote-Convention Rows

Rows:

```text
NOK, SEK
```

Required treatment:

- lock whether Appendix C descriptive labels are direct USD/foreign-currency or foreign-currency/USD quote conventions;
- lock contract unit and tick value from official CME rulebook or specs;
- do not infer from local display name alone.

### Multiplier/Point-Value Difference Rows

Rows:

```text
NIFTY, SI, ZC, GF, HE, LE, ZO, KE, ZS, ZL, ZW
```

Required treatment:

- extract official contract unit and price quotation unit;
- explain whether provider point value is per quoted price point, per cent, per hundredweight, per bushel, per pound, or another quote unit;
- reject or keep unresolved if Appendix C multiplier cannot be reconciled without inference.

### Cross-Venue Or Variant Rows

Rows:

```text
HG, MGC, SI, CAC40, NIFTY, BZ, HH, QG, HO
```

Required treatment:

- normalize source exchange label against current official venue only with explicit evidence;
- distinguish COMEX/NYMEX/CME/CBOT/Euronext/SGX/NSE IX variants;
- distinguish last-day, financial, physical, micro, mini/e-mini, and index futures variants.

## Non-Authorization

This packet authorizes no code edits outside this process artifact, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

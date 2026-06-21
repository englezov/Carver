# Carver Appendix C Jumbo Universe Transcription/Source Packet

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_APPENDIX_C_JUMBO_UNIVERSE_TRANSCRIPTION_SOURCE_PACKET_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Record the Appendix C Jumbo portfolio universe source fields needed before any future local provider mapping, real-data readiness, or production-facing P05/P06/P07 work.

This packet transcribes source universe identity only. It is not a local provider mapping, not a data-readiness record, not a market-row parser, not an implementation, not a diagnostic, not a backtest, and not a trading authorization.

## Inputs Inspected

Required Carver guardrails:

```text
README.md
docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md
docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md
docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md
```

Appendix C readiness predecessor:

```text
docs/process/CARVER_PART_ONE_JUMBO_PORTFOLIO_UNIVERSE_READINESS_SHAPE_GATE_DRAFT_2026-05-29.md
docs/process/CARVER_PART_ONE_JUMBO_PORTFOLIO_UNIVERSE_READINESS_SHAPE_GATE_DRAFT_HOSTILE_AUDIT_RESULT_2026-05-29.md
```

Local source:

```text
C:\Users\openclaw\Desktop\Carver\Carver.pdf
```

Narrow source range:

```text
Appendix C, PDF pages 690-695, Tables 172-183
```

## Source Scope

PDF page 690 states that Tables 172 to 183 are the complete list of all 102 instruments in the Jumbo portfolio, broken down by asset class.

The source fields recorded here are:

- Appendix C table number;
- PDF page range;
- source group;
- descriptive instrument name;
- author broker market code;
- exchange;
- currency;
- futures multiplier used by the author;
- first year when the instrument appears in the author's dataset.

The book warns that author market codes may vary across brokers and may differ from official exchange codes. Therefore this packet does not create local provider symbols, local canonical ids, contract availability claims, or production readiness.

## Global Readiness Defaults

For every row in this packet:

```text
lane_class = SOURCE_NATIVE_FUTURES
provider_mapping_status = UNRESOLVED
local_contract_identity_status = UNRESOLVED
market_data_readiness_status = CLOSED
substitution_policy = FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
production_use_status = NOT_AUTHORIZED
```

## Transcription Counts

| Appendix C table | Source group | Row count |
| --- | --- | ---: |
| 172 | US bond and interest rate futures | 10 |
| 173 | Other bond and interest rate futures | 11 |
| 174 | US equity index futures | 6 |
| 175 | European equity index futures | 8 |
| 176 | European stock sector futures | 8 |
| 177 | Asian equity index futures | 12 |
| 178 | Volatility futures | 2 |
| 179 | Major FX futures | 9 |
| 180 | Cross and EM FX futures | 8 |
| 181 | Metal and crypto futures | 9 |
| 182 | Energy futures | 6 |
| 183 | Agricultural futures | 13 |
| Total | Appendix C Jumbo universe | 102 |

## Table 172: US Bond And Interest Rate Futures

PDF pages: 690-691.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| 2-year US | ZT | ECBOT | USD | 2000 | 2000 |
| 3-year US | Z3N | ECBOT | USD | 2000 | 2020 |
| 5-year US | ZF | ECBOT | USD | 1000 | 1989 |
| 10-year US | ZN | ECBOT | USD | 1000 | 1982 |
| 10-year Ultra US | TN | ECBOT | USD | 1000 | 2016 |
| 20-year US | ZB | ECBOT | USD | 1000 | 1978 |
| 30-year US | UB | ECBOT | USD | 1000 | 2010 |
| 5-year US ERIS Swap | LIW | ECBOT | USD | 1000 | 2020 |
| 10-year US Swap | N1U | ECBOT | USD | 1000 | 2013 |
| Eurodollar | GE | GLOBEX | USD | 2500 | 1984 |

## Table 173: Other Bond And Interest Rate Futures

PDF page: 691.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| 10-year French (OAT) | OAT | DTB | EUR | 1000 | 2012 |
| 2-year German (Schatz) | GBS | DTB | EUR | 1000 | 2007 |
| 5-year German (Bobl) | GBM | DTB | EUR | 1000 | 2008 |
| 10-year German (Bund) | GBL | DTB | EUR | 1000 | 2006 |
| 20-year German (Buxl) | GBX | DTB | EUR | 1000 | 2015 |
| 3-year Italian (BTP) | BTS | DTB | EUR | 1000 | 2011 |
| 10-year Italian (BTP) | BTP | DTB | EUR | 1000 | 2010 |
| 10-year Japanese (JGB) | JGB | Osaka | JPY | 1000000 | 2001 |
| 3-year Korea | 3KTB | Korea | KRW | 1000000 | 2014 |
| 10-year Korea | FLKTB | Korea | KRW | 1000000 | 2014 |
| 10-year Spanish (Bono) | FBON | DTB | EUR | 1000 | 2016 |

## Table 174: US Equity Index Futures

PDF pages: 691-692.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| Dow Jones industrial (micro) | MYM | ECBOT | USD | 0.5 | 2002 |
| Nasdaq (micro) | MNQ | GLOBEX | USD | 2 | 1999 |
| Russell 1000 Value | RSV | GLOBEX | USD | 50 | 2015 |
| Russell 2000 smallcap (micro) | M2K | GLOBEX | USD | 5 | 2015 |
| S&P 400 midcap (e-mini) | EMD | GLOBEX | USD | 100 | 2002 |
| S&P 500 (micro) | MES | GLOBEX | USD | 5 | 1982 |

## Table 175: European Equity Index Futures

PDF page: 692.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| Dutch AEX | EOE | Euronext | EUR | 200 | 2009 |
| French CAC 40 | CAC40 | MONEP | EUR | 10 | 2009 |
| German DAX 30 | DAX | DTB | EUR | 1 | 2000 |
| Swiss SMI | SMI | SOFFEX | EUR | 10 | 2014 |
| EU DJ Small cap 200 | DJ200S | DTB | EUR | 50 | 2013 |
| EU STOXX select dividend 30 | DJSD | DTB | EUR | 10 | 2009 |
| EU STOXX 600 | DJ600 | DTB | EUR | 50 | 2005 |
| EUROSTOXX 50 | ESTX50 | DTB | EUR | 10 | 2014 |

## Table 176: European Stock Sector Futures

PDF page: 692.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| EU Auto | SXAP | DTB | EUR | 50 | 2015 |
| EU Basic materials | SXPP | DTB | EUR | 50 | 2018 |
| EU Health | SXDP | DTB | EUR | 50 | 2016 |
| EU Insurance | SXIP | DTB | EUR | 50 | 2020 |
| EU Oil | SXEP | DTB | EUR | 50 | 2018 |
| EU Technology | SX8P | DTB | EUR | 50 | 2018 |
| EU Travel | SXTP | DTB | EUR | 50 | 2014 |
| EU Utilities | SX6P | DTB | EUR | 50 | 2014 |

## Table 177: Asian Equity Index Futures

PDF page: 693.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| MSCI Asia | M1MS | DTB | USD | 100 | 2021 |
| FTSE China A | XINA50 | SGX | USD | 1 | 2011 |
| FTSE China H | XIN01 | SGX | USD | 2 | 2020 |
| Indian NIFTY | NIFTY | SGX | USD | 2 | 2002 |
| Japan NIKKEI | N225M | Osaka | JPY | 100 | 2011 |
| Japan NIKKEI 400 | JPNK400 | Osaka | JPY | 100 | 2015 |
| Japan Mothers index | TSEMOTHR | Osaka | JPY | 1000 | 2018 |
| Japan TOPIX | MNTPX | Osaka | JPY | 1000 | 2010 |
| Korea KOSDAQ | KOSDQ150 | Korea | KRW | 10000 | 2020 |
| Korea KOSPI | K200 | Korea | KRW | 250000 | 2014 |
| MSCI Singapore | SSG | SGX | SGD | 100 | 2001 |
| FTSE Taiwan | TWN | SGX | USD | 40 | 2020 |

## Table 178: Volatility Futures

PDF page: 693.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| VIX | VIX | CFE | USD | 1000 | 2006 |
| VSTOXX | V2TX | DTB | EUR | 100 | 2013 |

## Table 179: Major FX Futures

PDF pages: 693-694.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| AUD/USD | AUD | GLOBEX | USD | 100000 | 1987 |
| CAD/USD | CAD | GLOBEX | USD | 100000 | 1972 |
| CHF/USD | CHF | GLOBEX | USD | 125000 | 1972 |
| EUR/USD | EUR | GLOBEX | USD | 125000 | 1999 |
| GBP/USD | GBP | GLOBEX | USD | 62500 | 1975 |
| JPY/USD | JPY | GLOBEX | USD | 12500000 | 1977 |
| NOK/USD | NOK | GLOBEX | USD | 2000000 | 2002 |
| NZD/USD | NZD | GLOBEX | USD | 100000 | 2003 |
| SEK/USD | SEK | GLOBEX | USD | 2000000 | 2002 |

## Table 180: Cross And EM FX Futures

PDF page: 694.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| EUR/GBP | RP | GLOBEX | GBP | 125000 | 1999 |
| EUR/JPY | RY | GLOBEX | JPY | 125000 | 1999 |
| BRE/USD | BRE | GLOBEX | USD | 100000 | 1995 |
| USD/Offshore CNH | UC | SGX | CNH | 100000 | 2013 |
| INR/USD | SIR | GLOBEX | USD | 5000000 | 2015 |
| MXP/USD | MXP | GLOBEX | USD | 500000 | 1995 |
| RUR/USD | RUR | GLOBEX | USD | 2500000 | 2003 |
| USD/SGD | SND | SGX | SGD | 100000 | 2020 |

## Table 181: Metal And Crypto Futures

PDF page: 694.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| Aluminium | ALI | NYMEX | USD | 25 | 2019 |
| Copper | HG | NYMEX | USD | 25000 | 1995 |
| Gold (micro) | MGC | NYMEX | USD | 10 | 1975 |
| Iron | SCI | SGX | USD | 100 | 2014 |
| Palladium | PA | NYMEX | USD | 100 | 1977 |
| Platinum | PL | NYMEX | USD | 50 | 1970 |
| Silver | SI | NYMEX | USD | 1000 | 1970 |
| Bitcoin (micro) | MBT | CME | USD | 0.1 | 2017 |
| Ethereum | ETHUSDRR | CME | USD | 50 | 2012 |

## Table 182: Energy Futures

PDF page: 695.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| Brent Crude last day | BZ | NYMEX | USD | 1000 | 2020 |
| WTI Crude (mini) | QM | NYMEX | USD | 500 | 1988 |
| Gas last day | HH | NYMEX | USD | 10000 | 2006 |
| Gasoline | RB | NYMEX | USD | 42000 | 1985 |
| Henry Hub Gas (mini) | QG | NYMEX | USD | 2500 | 1990 |
| Heating Oil | HO | NYMEX | USD | 42000 | 1980 |

## Table 183: Agricultural Futures

PDF page: 695.

| Name | Author market code | Exchange | Currency | Multiplier | First source year |
| --- | --- | --- | --- | ---: | ---: |
| Bloomberg Commodity | AIGCI | ECBOT | USD | 100 | 2006 |
| Cheese | CSC | GLOBEX | USD | 20000 | 2010 |
| Corn | ZC | ECBOT | USD | 5000 | 1972 |
| Feeder Cattle | GF | GLOBEX | USD | 50000 | 1977 |
| Lean Hogs | HE | GLOBEX | USD | 40000 | 1974 |
| Live Cattle | LE | GLOBEX | USD | 40000 | 1971 |
| Oats | ZO | ECBOT | USD | 5000 | 1970 |
| Red Wheat | KE | ECBOT | USD | 5000 | 1995 |
| Rice | ZR | ECBOT | USD | 2000 | 1988 |
| Soybeans | ZS | ECBOT | USD | 5000 | 1985 |
| Soybean Meal | ZM | ECBOT | USD | 100 | 1970 |
| Soybean Oil | ZL | ECBOT | USD | 60000 | 1970 |
| Wheat | ZW | ECBOT | USD | 5000 | 1973 |

## Source-Faithfulness Constraints

This packet preserves the following source constraints:

- the Jumbo universe identity is complete only at 102 members;
- the source fields are descriptive name, author market code, exchange, currency, multiplier, and first source data year;
- author market codes are not automatically local provider codes;
- first source data year is not necessarily the instrument's first trading year;
- micro, mini, full-size, sector, cross-currency, and exchange-specific variants must not be silently substituted;
- Appendix C universe identity is separate from Strategy Nine, Strategy Ten, and Strategy Eleven signal eligibility;
- Appendix C universe identity is separate from local data readiness.

## Still Required Before Provider Mapping

Before local provider mapping work can begin, a future gate should decide:

- whether this markdown transcription is sufficient as a process source packet or whether a hash-bound machine-readable Appendix C universe file is required;
- whether each row needs a canonical local Carver instrument id;
- how to preserve table number, source page, source group, and source descriptive name in any future machine-readable artifact;
- how to record unresolved provider mappings without permitting partial portfolio execution;
- whether a provider-mapping packet should be audited before any data access.

## Still Required Before Any Data Work

Before any real-data gate, Carver must separately lock:

- local provider symbol for every member;
- source-native futures lane declaration for every member;
- exchange and contract identity;
- currency and FX handling;
- multiplier and point value;
- session calendar;
- completed-bar rule;
- roll and back-adjustment artifacts;
- source-native data availability;
- annual risk and price-risk source;
- cost source and risk-adjusted cost;
- trend eligibility;
- carry eligibility and carry curve-leg availability;
- missing-member policy;
- no-substitution policy.

None of these are authorized or solved by this packet.

## Relationship To P05/P06/P07

P05, P06, and P07 complete portfolio surfaces remain process-and-synthetic-code conformance only.

This packet supplies the Appendix C source universe identity needed before those synthetic surfaces can ever be connected to local provider readiness. It does not convert them into production portfolios.

## Audit Requirements

This packet should receive a lean regular hostile audit before it is treated as locked.

Audit focus:

- row count is exactly 102;
- table counts sum to 102;
- each Appendix C table from 172 through 183 is represented;
- source page references are narrow and consistent with Appendix C pages 690-695;
- author market codes are not promoted to local provider mappings;
- provider readiness, real data, diagnostics, backtests, and implementation remain closed;
- missing members remain fail-closed with no silent substitution, dropping, or reweighting;
- `SOURCE_NATIVE_FUTURES` remains the only lane;
- CFD adapter work and old QuantLab active-pipeline use remain closed.

## Next Proposed Authorization

```text
Operator authorizes exactly one regular hostile audit of the Carver Appendix C
Jumbo universe transcription/source packet.

Scope:
Audit the process-only source packet:
docs/process/CARVER_APPENDIX_C_JUMBO_UNIVERSE_TRANSCRIPTION_SOURCE_PACKET_2026-05-29.md

Allowed:
Read-only file inspection, narrow local Carver.pdf Appendix C source inspection,
and concise audit findings.

Forbidden:
No file edits, no code tests, no real data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no
Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no
deployment, no trading, no promotion, no Opus/GPT execution, no remote
operations.
```

## Non-Authorization

This packet authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no provider mapping, no production data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.

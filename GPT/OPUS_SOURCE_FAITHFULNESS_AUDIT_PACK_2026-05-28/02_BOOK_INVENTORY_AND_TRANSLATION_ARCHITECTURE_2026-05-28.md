# Book Inventory And Translation Architecture

Generated: 2026-05-28

Status:

```text
PROCESS_ONLY_OPUS_UPLOAD_CONTEXT_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

This file is an upload-context bundle generated from clean Carver repo-local artifacts. It authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, and no promotion.

Audit note:

- This bundle intentionally includes the first inventory and the later translation architecture together.
- If the first inventory conflicts with later architecture/M0/pre-Opus records, treat the conflict as an audit item.
- S29 and S30 are now amended in the first inventory to `PARKED_NOT_STANDALONE` in line with later architecture/M0 records.

---

## Source File: `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`

# Carver Book Strategy And Portfolio Inventory 001

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_BOOK_STRATEGY_PORTFOLIO_INVENTORY_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

Authorization:

```text
Operator authorized exactly one process-only Carver book strategy and portfolio inventory on 2026-05-28.
```

## Scope Boundary

This artifact is a process-only inventory. It inspected only:

- `Carver.pdf`, the local reference copy of Robert Carver, *Advanced Futures Trading Strategies*.
- Repo-local clean mission/process artifacts in this workspace.

It did not inspect, export, parse, or compute market data. It did not implement strategy code, write tests, run diagnostics, run backtests, access OOS/Lockbox/Forward data, execute CFD adapters, import old QuantLab adapters, tune parameters, deploy, trade, promote, or use the archived `QuantLab_v3` workspace for active pipeline work.

## Governing Local Artifacts

- `AGENTS.md`: clean Carver workspace rules; old `QuantLab_v3` is archived and not active pipeline authority.
- `README.md`: mission shell status; book dissection must be source-native futures first.
- `docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md`: strategy labels, source-native first rule, portfolio rule, and non-authorization boundaries.
- `docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md`: old workspace quarantine and clean next step.
- `docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md`: every future lane must declare exactly one of `SOURCE_NATIVE_FUTURES`, `CFD_DIRECT`, or `CFD_ADAPTER`.
- `docs/process/THREAD_HANDOFF_START_HERE_2026-05-28.md`: immediate next authorization prompt and required output artifact.

## Book Source Facts

- Local file: `C:\Users\openclaw\Desktop\Carver\Carver.pdf`
- Title metadata: *Advanced Futures Trading Strategies*
- Author metadata: Robert Carver
- PDF pages: 701
- Book framing: 30 futures strategies, price-data based, systematic, futures-specific, with a recurring 100+ instrument universe. See PDF pages 11-17.
- Data/timeframe framing: Parts One, Two, and Three are daily/once-a-day strategies; Part Four uses hourly data; Part Five is relative value across instruments or expiries. See PDF pages 15-17, 475-476, and 511-512.
- Price input framing: the book uses closing prices for each relevant time period and does not use OHLC/candlestick inputs. See PDF page 15.
- Jumbo universe: Appendix C lists 102 instruments and broker/exchange/multiplier/first-year metadata. See PDF pages 690-695.

## Label Definitions For This Inventory

Strategy labels used below:

- `STANDALONE_CANDIDATE`: the book frames the strategy as usable or testable on its own.
- `SOURCE_NATIVE_PORTFOLIO_SLEEVE`: the strategy is primarily a sleeve or building block inside a larger source-native portfolio.
- `PORTFOLIO_ONLY_COMPONENT`: the strategy is not a standalone alpha family in this inventory; it is an overlay, construction method, or allocation component.
- `BLOCKED_SOURCE_UNRESOLVED`: the book chapter exists, but a clean source-native pipeline cannot be briefed until unresolved source atoms are pinned down.
- `PARKED_NOT_STANDALONE`: later architecture amendment for a strategy admitted as book material but not advanced as standalone without direct Carver source justification and explicit operator override.

Amendment note:

- This first inventory originally used only the first four labels. Later architecture and M0 records added `PARKED_NOT_STANDALONE` for S29 and S30 after the operator asked to park the last two futures-native strategies as not standalone. The S29/S30 rows below are updated to the amended label so future readers do not rely on the legacy standalone row.

Lane class used below:

```text
SOURCE_NATIVE_FUTURES
```

No strategy in this inventory is classified as `CFD_DIRECT` or `CFD_ADAPTER`.

## Strategy Inventory

| ID | Book strategy | PDF start | Lane class | Initial label | Timeframe | Inventory interpretation |
| --- | --- | ---: | --- | --- | --- | --- |
| S01 | Buy and hold, single contract | 21 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Foundational single-future excess-return and back-adjustment baseline; likely first educational reconstruction, not a final preferred research target. |
| S02 | Buy and hold with risk scaling | 67 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Adds risk target and position sizing; foundational dependency for later candidates. |
| S03 | Buy and hold with variable risk scaling | 93 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Adds current volatility/risk forecast position scaling; foundational dependency for portfolio construction. |
| S04 | Buy and hold portfolio with variable risk position sizing | 118 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | First explicit portfolio candidate family: risk parity, All Weather, generalized risk premia, and Jumbo buy-and-hold baseline. |
| S05 | Slow trend following, long only | 148 | `SOURCE_NATIVE_FUTURES` | `SOURCE_NATIVE_PORTFOLIO_SLEEVE` | Daily close | Long-only trend filter on variable-risk positions; useful sleeve and bridge from buy-and-hold into trend. |
| S06 | Slow trend following, long and short | 163 | `SOURCE_NATIVE_FUTURES` | `SOURCE_NATIVE_PORTFOLIO_SLEEVE` | Daily close | Long/short version of slow trend; sleeve-level bridge toward forecasted EWMAC trend. |
| S07 | Slow trend following with trend strength | 177 | `SOURCE_NATIVE_FUTURES` | `SOURCE_NATIVE_PORTFOLIO_SLEEVE` | Daily close | Forecast-sized EWMAC64/256 trend; building block for multiple trend and combined portfolios. |
| S08 | Fast trend following, long and short with trend strength | 190 | `SOURCE_NATIVE_FUTURES` | `SOURCE_NATIVE_PORTFOLIO_SLEEVE` | Daily close | Faster EWMAC16/64 trend with buffering; building block for multiple trend. |
| S09 | Multiple trend following rules | 201 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Standalone multiple-EWMAC trend family; core directional candidate and dependency for many later chapters. |
| S10 | Basic carry | 232 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Standalone carry family using futures curve information; core dependency for combined carry/trend and carry variants. |
| S11 | Combined carry and trend | 264 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Core combined forecast candidate; book combines EWMAC2/4/8/16/32/64 with Carry5/20/60/120. |
| S12 | Adjusted trend | 278 | `SOURCE_NATIVE_FUTURES` | `PORTFOLIO_ONLY_COMPONENT` | Daily close | Variation/adjustment for EWMAC trend forecasts based on reversal probability; not first standalone family. |
| S13 | Trend following and carry in different risk regimes | 296 | `SOURCE_NATIVE_FUTURES` | `PORTFOLIO_ONLY_COMPONENT` | Daily close | Forecast adjustment for EWMAC/carry based on relative volatility regimes. |
| S14 | Spot trend | 306 | `SOURCE_NATIVE_FUTURES` | `PORTFOLIO_ONLY_COMPONENT` | Daily close | EWMAC variation using synthetic spot price derived from futures/carry rather than back-adjusted total return. |
| S15 | Accurate carry | 316 | `SOURCE_NATIVE_FUTURES` | `PORTFOLIO_ONLY_COMPONENT` | Daily close | Carry-estimation improvement/adjustment for instruments where front/next curve slope is not enough. |
| S16 | Trend and carry allocation | 330 | `SOURCE_NATIVE_FUTURES` | `PORTFOLIO_ONLY_COMPONENT` | Daily close | Allocation overlay for strategies that trade both trend and carry; should follow S09/S10/S11 reconstruction. |
| S17 | Normalised trend | 342 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Alternative trend rule using volatility-normalised price as EWMAC input; also dependency for S18/S19/S22. |
| S18 | Trend following asset classes | 354 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Asset-class trend from normalised futures-price basket; requires asset-class membership locked. |
| S19 | Cross-sectional momentum | 365 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Relative momentum within asset classes using instrument normalised price minus asset-class normalised price. |
| S20 | Cross-sectional carry | 377 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Relative carry within asset classes; uses smoothed carry minus asset-class median/aggregate carry. |
| S21 | Breakout | 388 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Directional breakout forecast over price ranges; can combine with trend/carry framework. |
| S22 | Value | 403 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Slow mean-reversion/value forecast using multi-year relative under/outperformance within asset class. |
| S23 | Acceleration | 410 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Forecast based on rate of change of EWMAC trend forecast. |
| S24 | Skew, a case study | 421 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily close | Example of fitting arbitrary quantifiable signal into the forecast framework; buys more negative skew, shorts more positive skew. |
| S25 | Dynamic optimisation | 443 | `SOURCE_NATIVE_FUTURES` | `PORTFOLIO_ONLY_COMPONENT` | Daily close | Portfolio construction/rounding/constraint overlay for constrained capital; requires underlying strategy positions first. |
| S26 | Fast mean reversion | 476 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Hourly | Independent fast directional mean-reversion strategy; Part Four cannot be directly combined with Parts One-Three. |
| S27 | Safer fast mean reversion | 499 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Hourly plus daily trend/vol overlays | Fast mean reversion gated by trend direction and high-volatility reduction; follows S26. |
| S28 | Cross instrument spreads | 513 | `SOURCE_NATIVE_FUTURES` | `STANDALONE_CANDIDATE` | Daily/relative value | Relative-value pair spreads; higher leverage/cost/minimum-capital complexity. |
| S29 | Cross instrument triplets | 552 | `SOURCE_NATIVE_FUTURES` | `PARKED_NOT_STANDALONE` | Daily/relative value | Amended label: relative-value synthetic triplets/butterflies are retained as book material but parked from standalone advancement unless direct Carver source justification and explicit operator override changes this. |
| S30 | Calendar trading strategies | 570 | `SOURCE_NATIVE_FUTURES` | `PARKED_NOT_STANDALONE` | Daily/relative value across expiries | Amended label: calendar spreads/triplets are retained as book material but parked from standalone advancement unless direct Carver source justification and explicit operator override changes this. |

## Complete Portfolio Inventory

The following are portfolio-level structures to reconstruct separately from isolated sleeve results. A sleeve failing standalone must not be interpreted as family death if the book frames it as portfolio material.

| Portfolio ID | Source | PDF pages | Portfolio type | Member atoms | Initial reconstruction status |
| --- | --- | ---: | --- | --- | --- |
| P01 | Risk parity example | 119-123 | Complete two-instrument portfolio | S&P 500 micro futures and US 10-year bond futures, equal capital/risk allocation, IDM leverage adjustment | `SOURCE_RULE_ATOMS_PARTIAL`; needs exact source-native contract, roll, cost, and target-risk lock before any data work. |
| P02 | All Weather example | 124-126 | Complete six-instrument portfolio | S&P 500 micro, US 10-year, US 5-year, WTI Crude Oil mini, Corn, Gold micro; instrument weights 25/12.5/12.5/12.5/12.5/25 percent | `SOURCE_RULE_ATOMS_PARTIAL`; needs source-native symbols, roll, costs, target risk, IDM, and completed-bar calendar. |
| P03 | Generalized risk premia portfolio | 127-144 | Portfolio construction method | Strategy 3 per instrument, instrument weights, IDM, capital selection, minimum-capital constraints | `SOURCE_RULE_ATOMS_PARTIAL`; becomes concrete only after universe and weights are locked. |
| P04 | Jumbo buy-and-hold risk premia portfolio | 141-144, 690-695 | Complete large-universe portfolio | S04 across the 102-instrument Appendix C universe | `SOURCE_RULE_ATOMS_PARTIAL`; canonical universe listed, but clean data/vendor/roll/session representation must be separately authorized. |
| P05 | Jumbo multiple trend portfolio | 201-227 plus Appendix C | Complete strategy portfolio candidate | S09 across eligible Jumbo instruments and eligible EWMAC speeds | `DEPENDENT_ON_S09_SOURCE_LOCK`; do not infer from S07/S08 sleeve results alone. |
| P06 | Jumbo carry portfolio | 232-259 plus Appendix C | Complete strategy portfolio candidate | S10 across eligible Jumbo instruments and eligible carry smooths | `DEPENDENT_ON_S10_SOURCE_LOCK`; requires futures curve/expiry availability and carry eligibility rules. |
| P07 | Jumbo combined trend/carry portfolio | 264-275 plus Appendix C | Complete combined strategy portfolio candidate | S11, using trend and carry forecast blocks | `DEPENDENT_ON_S09_AND_S10_SOURCE_LOCK`; likely core book portfolio candidate after foundations. |
| P08 | Trend/carry allocation portfolio overlay | 330-339 | Allocation overlay portfolio | S16 on a trend/carry base such as S11 | `DEPENDENT_ON_S11_SOURCE_LOCK`; portfolio overlay, not first standalone implementation. |
| P09 | Dynamic optimisation constrained-capital portfolio | 443-470 | Portfolio construction overlay | S25 on an underlying strategy, especially a Jumbo-style strategy whose unrounded positions exceed account practicality | `DEPENDENT_ON_UNDERLYING_STRATEGY_POSITIONS`; cannot be first active lane. |
| P10 | Fast mean reversion independent portfolio | 476-495 | Independent fast directional portfolio | S26 across eligible instruments with hourly bars | `SEPARATE_FAST_DATA_STACK_REQUIRED`; not combine-and-compare with daily sleeves without an explicit design memo. |
| P11 | Safer fast mean reversion independent portfolio | 499-508 | Independent fast directional portfolio | S27 across eligible instruments with trend and volatility overlays | `DEPENDENT_ON_S26_AND_OVERLAY_RULE_LOCK`. |
| P12 | Cross-instrument spread portfolio | 513-547 | Relative-value multi-instrument portfolio | S28 synthetic pair instruments | `SEPARATE_RV_SYNTHETIC_INSTRUMENT_STACK_REQUIRED`. |
| P13 | Cross-instrument triplet portfolio | 552-565 | Relative-value multi-instrument portfolio | S29 synthetic triplet instruments | `SEPARATE_RV_SYNTHETIC_INSTRUMENT_STACK_REQUIRED`. |
| P14 | Calendar spread/triplet portfolio | 570-590 | Relative-value term-structure portfolio | S30 within-instrument expiry pairs/triplets; examples include VIX, Eurodollar, WTI Crude Oil | `SEPARATE_MULTI_EXPIRY_STACK_REQUIRED`. |

## Source-Native Instrument Universe

Appendix C is the canonical first inventory for the Jumbo universe. It lists 102 instruments and warns that broker market codes may vary. This inventory records the source-native futures universe as a book reference, not as a live data request.

### Bonds And Interest Rates

US bond and interest-rate futures from Appendix C:

- 2-year US (`ZT`, ECBOT, USD, multiplier 2000, first data year 2000)
- 3-year US (`Z3N`, ECBOT, USD, 2000, 2020)
- 5-year US (`ZF`, ECBOT, USD, 1000, 1989)
- 10-year US (`ZN`, ECBOT, USD, 1000, 1982)
- 10-year Ultra US (`TN`, ECBOT, USD, 1000, 2016)
- 20-year US (`ZB`, ECBOT, USD, 1000, 1978)
- 30-year US (`UB`, ECBOT, USD, 1000, 2010)
- 5-year US ERIS Swap (`LIW`, ECBOT, USD, 1000, 2020)
- 10-year US Swap (`N1U`, ECBOT, USD, 1000, 2013)
- Eurodollar (`GE`, GLOBEX, USD, 2500, 1984)

Other bond and interest-rate futures:

- 10-year French OAT (`OAT`, DTB, EUR, 1000, 2012)
- 2-year German Schatz (`GBS`, DTB, EUR, 1000, 2007)
- 5-year German Bobl (`GBM`, DTB, EUR, 1000, 2008)
- 10-year German Bund (`GBL`, DTB, EUR, 1000, 2006)
- 20-year German Buxl (`GBX`, DTB, EUR, 1000, 2015)
- 3-year Italian BTP (`BTS`, DTB, EUR, 1000, 2011)
- 10-year Italian BTP (`BTP`, DTB, EUR, 1000, 2010)
- 10-year Japanese JGB (`JGB`, Osaka, JPY, 1000000, 2001)
- 3-year Korea (`3KTB`, Korea, KRW, 1000000, 2014)
- 10-year Korea (`FLKTB`, Korea, KRW, 1000000, 2014)
- 10-year Spanish Bono (`FBON`, DTB, EUR, 1000, 2016)

### Equities And Volatility

US equity index futures:

- Dow Jones industrial micro (`MYM`, ECBOT, USD, 0.5, 2002)
- Nasdaq micro (`MNQ`, GLOBEX, USD, 2, 1999)
- Russell 1000 Value (`RSV`, GLOBEX, USD, 50, 2015)
- Russell 2000 smallcap micro (`M2K`, GLOBEX, USD, 5, 2015)
- S&P 400 midcap e-mini (`EMD`, GLOBEX, USD, 100, 2002)
- S&P 500 micro (`MES`, GLOBEX, USD, 5, 1982)

European equity index futures:

- Dutch AEX (`EOE`, Euronext, EUR, 200, 2009)
- French CAC 40 (`CAC40`, MONEP, EUR, 10, 2009)
- German DAX 30 (`DAX`, DTB, EUR, 1, 2000)
- Swiss SMI (`SMI`, SOFFEX, EUR, 10, 2014)
- EU DJ Small cap 200 (`DJ200S`, DTB, EUR, 50, 2013)
- EU STOXX select dividend 30 (`DJSD`, DTB, EUR, 10, 2009)
- EU STOXX 600 (`DJ600`, DTB, EUR, 50, 2005)
- EUROSTOXX 50 (`ESTX50`, DTB, EUR, 10, 2014)

European stock sector futures:

- EU Auto (`SXAP`, DTB, EUR, 50, 2015)
- EU Basic materials (`SXPP`, DTB, EUR, 50, 2018)
- EU Health (`SXDP`, DTB, EUR, 50, 2016)
- EU Insurance (`SXIP`, DTB, EUR, 50, 2020)
- EU Oil (`SXEP`, DTB, EUR, 50, 2018)
- EU Technology (`SX8P`, DTB, EUR, 50, 2018)
- EU Travel (`SXTP`, DTB, EUR, 50, 2014)
- EU Utilities (`SX6P`, DTB, EUR, 50, 2014)

Asian equity index futures:

- MSCI Asia (`M1MS`, DTB, USD, 100, 2021)
- FTSE China A (`XINA50`, SGX, USD, 1, 2011)
- FTSE China H (`XIN01`, SGX, USD, 2, 2020)
- Indian NIFTY (`NIFTY`, SGX, USD, 2, 2002)
- Japan NIKKEI (`N225M`, Osaka, JPY, 100, 2011)
- Japan NIKKEI 400 (`JPNK400`, Osaka, JPY, 100, 2015)
- Japan Mothers index (`TSEMOTHR`, Osaka, JPY, 1000, 2018)
- Japan TOPIX (`MNTPX`, Osaka, JPY, 1000, 2010)
- Korea KOSDAQ (`KOSDQ150`, Korea, KRW, 10000, 2020)
- Korea KOSPI (`K200`, Korea, KRW, 250000, 2014)
- MSCI Singapore (`SSG`, SGX, SGD, 100, 2001)
- FTSE Taiwan (`TWN`, SGX, USD, 40, 2020)

Volatility futures:

- VIX (`VIX`, CFE, USD, 1000, 2006)
- VSTOXX (`V2TX`, DTB, EUR, 100, 2013)

### FX

Major FX futures:

- AUD/USD (`AUD`, GLOBEX, USD, 100000, 1987)
- CAD/USD (`CAD`, GLOBEX, USD, 100000, 1972)
- CHF/USD (`CHF`, GLOBEX, USD, 125000, 1972)
- EUR/USD (`EUR`, GLOBEX, USD, 125000, 1999)
- GBP/USD (`GBP`, GLOBEX, USD, 62500, 1975)
- JPY/USD (`JPY`, GLOBEX, USD, 12500000, 1977)
- NOK/USD (`NOK`, GLOBEX, USD, 2000000, 2002)
- NZD/USD (`NZD`, GLOBEX, USD, 100000, 2003)
- SEK/USD (`SEK`, GLOBEX, USD, 2000000, 2002)

Cross and EM FX futures:

- EUR/GBP (`RP`, GLOBEX, GBP, 125000, 1999)
- EUR/JPY (`RY`, GLOBEX, JPY, 125000, 1999)
- BRE/USD (`BRE`, GLOBEX, USD, 100000, 1995)
- USD/Offshore CNH (`UC`, SGX, CNH, 100000, 2013)
- INR/USD (`SIR`, GLOBEX, USD, 5000000, 2015)
- MXP/USD (`MXP`, GLOBEX, USD, 500000, 1995)
- RUR/USD (`RUR`, GLOBEX, USD, 2500000, 2003)
- USD/SGD (`SND`, SGX, SGD, 100000, 2020)

### Metals, Crypto, Energies, Agricultural

Metals and crypto futures:

- Aluminium (`ALI`, NYMEX, USD, 25, 2019)
- Copper (`HG`, NYMEX, USD, 25000, 1995)
- Gold micro (`MGC`, NYMEX, USD, 10, 1975)
- Iron (`SCI`, SGX, USD, 100, 2014)
- Palladium (`PA`, NYMEX, USD, 100, 1977)
- Platinum (`PL`, NYMEX, USD, 50, 1970)
- Silver (`SI`, NYMEX, USD, 1000, 1970)
- Bitcoin micro (`MBT`, CME, USD, 0.1, 2017)
- Ethereum (`ETHUSDRR`, CME, USD, 50, 2012)

Energy futures:

- Brent Crude last day (`BZ`, NYMEX, USD, 1000, 2020)
- WTI Crude mini (`QM`, NYMEX, USD, 500, 1988)
- Gas last day (`HH`, NYMEX, USD, 10000, 2006)
- Gasoline (`RB`, NYMEX, USD, 42000, 1985)
- Henry Hub Gas mini (`QG`, NYMEX, USD, 2500, 1990)
- Heating Oil (`HO`, NYMEX, USD, 42000, 1980)

Agricultural futures:

- Bloomberg Commodity (`AIGCI`, ECBOT, USD, 100, 2006)
- Cheese (`CSC`, GLOBEX, USD, 20000, 2010)
- Corn (`ZC`, ECBOT, USD, 5000, 1972)
- Feeder Cattle (`GF`, GLOBEX, USD, 50000, 1977)
- Lean Hogs (`HE`, GLOBEX, USD, 40000, 1974)
- Live Cattle (`LE`, GLOBEX, USD, 40000, 1971)
- Oats (`ZO`, ECBOT, USD, 5000, 1970)
- Red Wheat (`KE`, ECBOT, USD, 5000, 1995)
- Rice (`ZR`, ECBOT, USD, 2000, 1988)
- Soybeans (`ZS`, ECBOT, USD, 5000, 1985)
- Soybean Meal (`ZM`, ECBOT, USD, 100, 1970)
- Soybean Oil (`ZL`, ECBOT, USD, 60000, 1970)
- Wheat (`ZW`, ECBOT, USD, 5000, 1973)

## Source-Rule Atoms To Lock Before Any Data Work

The following atoms are unresolved process dependencies. They are not authorization to implement or test.

### Shared Source-Native Futures Atoms

- Exact source-native contract identity per instrument, including exchange code, multiplier, currency, and any micro/mini/full-size substitution rule.
- Data vendor and continuous-contract construction method.
- Contract selection and rolling rule, including completed-bar timing and roll calendars.
- Back-adjusted price construction and whether total-return/back-adjusted or synthetic spot price is required.
- Futures curve availability for carry, accurate carry, calendar spreads, and multi-expiry strategies.
- Cost source: use `config/costs.json` only once it exists; no hardcoded ad hoc cost dictionaries.
- FX/currency conversion treatment for multi-currency instruments.
- Target risk, capital base, IDM, forecast diversification multiplier, buffering, rounding, and minimum-capital rules.
- Instrument eligibility rules: liquidity, cost speed limit, first usable date, missing history, and asset-class membership.
- Completed bars only. For daily strategies, use completed daily closes; for hourly strategies, use completed hourly bars.
- Evidence windows and maximum diagnostic/backtest span. No diagnostic or backtest over 2 years without explicit operator approval.

### Strategy-Specific Atoms

- S01-S04: back-adjustment, excess return, risk measurement, variable volatility estimator, target risk, IDM, and position rounding.
- S05-S09: moving average/EWMAC definitions, forecast scalar/cap, speed set, buffering, and cost-speed eligibility.
- S10/S15/S20/S30: curve construction, held contract versus nearer/further contract, annualized carry, smoothing spans, seasonal/front-contract adjustments, and multi-expiry availability.
- S11/S16: trend/carry forecast weights, forecast diversification, allocation method, and fail-closed behavior when one sleeve is unavailable.
- S12/S13: adjustment lookup/construction for trend reversal probability and volatility regime; must be source-locked before any result is observed.
- S14: synthetic spot construction from futures and carry; no external spot feed unless explicitly authorized.
- S17-S19/S22: normalised price construction, asset-class basket membership, cross-sectional relative price, and lookback horizon.
- S21: breakout horizon set, range normalisation, smoothing, and forecast scaling.
- S23: acceleration rule source forecast, rate-of-change horizon, forecast scaling, and speed eligibility.
- S24: skew measurement window and transformation into forecast.
- S25: optimization objective, covariance matrix, tracking-error/cost penalty, constraints, integer rounding, buffering, and underlying unrounded positions.
- S26-S27: hourly data semantics, daily equilibrium update, no-buffering rule for pure fast mean reversion, trend overlay, high-volatility reduction, and independent fast-stack evaluation.
- S28-S29: synthetic spread/triplet construction, hedge ratios, leg synchronization, leverage, costs, correlation/standard-deviation estimation, and execution assumption.
- S30: calendar leg choice, simultaneous rolling of legs, expiry spacing, multi-expiry liquidity rules, and spread/triplet construction within a single instrument.

## Blockers And Quarantine Notes

- No strategy is eligible for active data work until it has a locked candidate brief.
- No `CFD_ADAPTER` lane exists. CFD adapter work requires separate explicit operator approval after source-native behavior exists.
- Do not import old QuantLab adapters, broker-clock assumptions, data-prep scripts, or stale state.
- Do not treat old VWAP or IndexHunt work as evidence for any Carver candidate.
- Do not use best-instrument logic to summarize family status.
- Do not tune parameters, thresholds, filters, exits, symbols, costs, or windows after seeing results.
- Do not collapse portfolio-sleeve performance into standalone family death.

## Recommended First Pipeline Order

This is a recommended order for future authorization prompts only. It is not authorization to implement or test.

1. Create a locked process brief for the source-native futures foundation shared by S01-S04: completed daily bars, back-adjustment, excess return, variable risk estimate, position sizing, rounding, target risk, and cost-source policy.
2. Reconstruct S01-S03 as foundational single-instrument candidates, preferably using the book's S&P 500 micro example only if source-native data availability is later authorized and locked.
3. Reconstruct S04 portfolio candidates separately: P01 risk parity, P02 All Weather, and P04 Jumbo buy-and-hold. Do not infer Jumbo from P01/P02.
4. Reconstruct S09 multiple trend as the first core directional alpha family after S07/S08 atoms are source-locked.
5. Reconstruct S10 basic carry only after futures curve/expiry data rules are locked.
6. Reconstruct S11 combined trend/carry after S09 and S10 are locked, then treat P07 as the core combined book portfolio candidate.
7. Add Part Two and Part Three daily strategies in dependency order: S12-S16 overlays after their base families, then S17-S24 standalone/additive daily candidates.
8. Defer S25 dynamic optimisation until an underlying unrounded-position portfolio exists.
9. Defer Part Four S26-S27 until a separate hourly-data stack and fast-strategy evidence budget are authorized.
10. Defer Part Five S28-S30 until a separate relative-value synthetic-instrument stack is authorized.

## Next Authorization Prompt Template

Suggested next prompt if the operator wants to proceed without data work:

```text
Operator authorizes exactly one process-only Carver candidate-brief drafting pass for the source-native futures foundation and Strategy 1-4 dependency chain.

Purpose:
Create locked candidate brief templates and unresolved-source-atom checklists for S01-S04 before any data work, implementation, tests, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, or CFD adapter activity.

Scope:
Inspect only Carver.pdf and repo-local clean mission/process artifacts. Draft process artifacts only. No market data, no computation, no strategy implementation.

Forbidden:
No data export, no market-row parsing, no implementation, no tests/backtests, no strategy computation, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old adapter import, no tuning, no deployment, no trading, no promotion.

Required status:
PROCESS_ONLY_CARVER_FOUNDATION_S01_S04_CANDIDATE_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```


---

## Source File: `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`

# Carver Source-Native Translation Architecture Goal

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

This record accepts the Opus source-translation architecture as the working goal for the clean Carver workspace, with corrections noted below.

The goal is to use the Carver book as source authority, translate book strategies into locked source-native futures candidate briefs, reconstruct complete book portfolios separately, and keep all data, implementation, testing, backtesting, OOS, Lockbox, Forward, CFD adapter, deployment, trading, and promotion work behind explicit future authorization gates.

## Accepted Architecture

The accepted high-level path is:

```text
Carver.pdf
-> M0 Source-Native Futures Foundation Spec
-> shared modules M1-M3
-> standalone/sleeve/overlay strategy briefs
-> complete portfolio reconstruction briefs
-> later separate fast-stack and RV-stack briefs only if explicitly authorized
```

The architecture is process-only. It is not a data lane, strategy lane, test lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Corrected Source Notes

The Opus architecture is accepted with these corrections and guardrails:

1. Forecast-block / "Lego" source reference:
   - The working source anchor is Strategy 11, especially the combined trend/carry building-block discussion around Carver PDF pages 264-265.
   - The Opus reference to page 406 for the "Lego" architecture is not accepted as-is and must be page-audited before any candidate brief quotes it.

2. Page references:
   - Opus page references are useful planning aids, not locked citation authority.
   - Every candidate brief or portfolio brief must re-check its own source pages against `Carver.pdf` before becoming a locked artifact.

3. S29 and S30:
   - Strategy 29, Cross instrument triplets, is admitted as source-native futures material but parked as:

```text
PARKED_NOT_STANDALONE
```

   - Strategy 30, Calendar trading strategies, is admitted as source-native futures material but parked as:

```text
PARKED_NOT_STANDALONE
```

   - They should be reconstructed only through their relative-value portfolio/synthetic-instrument context, not treated as clean standalone alpha candidates.

4. S28:
   - Strategy 28, Cross instrument spreads, remains eligible for a future source-native relative-value brief, but only with explicit caveats about synthetic-instrument complexity, costs, leverage, and the separate RV stack.

## Working Module Goal

The reusable translation modules are the durable goal of the process:

| Module | Working name | Role |
| --- | --- | --- |
| M0 | Source-Native Futures Foundation Spec | Completed bars, source-native contract identity, roll/calendar rules, back-adjustment, costs, FX, target risk, sizing, rounding, eligibility, evidence-window guard. |
| M1 | Position Sizing And Risk Scaling | Capital, risk target, volatility estimate, position sizing, IDM, rounding, buffering boundary. |
| M2 | Forecast-Block Architecture | Raw forecast, scaling, cap, forecast weights, diversification multiplier, speed/cost eligibility, buffering. |
| M3 | Multi-Instrument Portfolio Construction | Instrument weights, asset-class grouping, IDM, eligibility, minimum capital, sleeve fail-closed behavior. |
| M4 | Asset-Class And Normalised-Price Module | Normalised prices, asset-class membership, cross-sectional aggregation. |
| M5 | Futures Curve And Carry Module | Held/near/far contract logic, carry, carry smoothing, accurate carry, synthetic spot, multi-expiry availability. |
| M6 | Synthetic-Instrument RV Module | Spread/triplet construction, hedge ratios, synthetic prices, leg synchronization, leverage/cost treatment. |
| M7 | Hourly Fast-Stack Module | Hourly completed bars, daily equilibrium update, no-buffering rule, fast-stack separation. |
| M8 | Risk-Management Overlay Module | Risk-management lattice only; not alpha evidence and not promotion authority. |

## Accepted First Ten Brief Goal

The working first-ten sequence is accepted as the planning goal, subject to one-at-a-time operator authorization:

1. M0 Source-Native Futures Foundation Spec.
2. S01 Buy-and-hold, single contract.
3. S02 Buy-and-hold with risk scaling.
4. S03 Buy-and-hold with variable risk scaling.
5. S04 Buy-and-hold portfolio with variable risk position sizing.
6. P01 Risk parity example portfolio.
7. P02 All Weather example portfolio.
8. S09 Multiple trend following rules.
9. S10 Basic carry.
10. S11 Combined carry and trend.

S05-S08 are intentionally treated as source-native portfolio sleeves or building blocks rather than first-order standalone alpha candidates.

## Standing Rules

- Every future lane must declare exactly one class before data work:

```text
SOURCE_NATIVE_FUTURES
CFD_DIRECT
CFD_ADAPTER
```

- The default class for Carver book strategy translation is `SOURCE_NATIVE_FUTURES` unless the book source explicitly says otherwise.
- CFD adapter work remains quarantined and requires a separate explicit adapter gate after source-native behavior exists.
- Complete book portfolios must be reconstructed separately from individual sleeve results.
- A sleeve failing standalone is not family death if the book frames it as portfolio material.
- Parked/not-standalone is not failed alpha.
- No old QuantLab_v3 adapters, broker-clock assumptions, data-prep scripts, contaminated results, stale pipeline state, TEST/VALIDATION/Lockbox state, or convenience shortcuts are active authority.
- No data export, market-row parsing, implementation, tests/backtests, diagnostics, OOS, Lockbox, Forward, CFD adapter execution, tuning, deployment, trading, or promotion is authorized by this file.
- No diagnostic or backtest over 2 years may be run without explicit operator approval.
- Completed bars only.
- No tuning parameters, thresholds, filters, exits, symbols, costs, or windows after seeing results.

## Next Goal Gate

The next recommended authorization remains:

```text
Operator authorizes exactly one process-only Carver brief drafting pass for
the Source-Native Futures Foundation Spec (Module M0).

Purpose:
Lock M0 atoms as a single process artifact. No subsequent briefs.

Scope:
Inspect only Carver.pdf and repo-local clean mission/process artifacts.
Draft a process artifact only. No market data, no computation,
no strategy implementation, no parsing, no tests, no diagnostics,
no backtests, no OOS, no Lockbox, no Forward, no CFD adapter,
no old-adapter import, no tuning, no deployment, no trading, no promotion.

Forbidden:
Any work on S01 or any later brief until M0 is operator-locked.

Required status:
PROCESS_ONLY_CARVER_M0_FOUNDATION_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```



# 02 Source Definitions and P01/P02 Portfolio Briefs

Use this file with Carver.pdf to audit whether the P01/P02 package faithfully preserves the book definitions, source-native instrument set, portfolio weights, module dependencies, and strategy/portfolio classifications.

---

# FILE: docs\researchops\handoffs\CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md

```text
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

```

# FILE: docs\process\CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md

```text
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


```

# FILE: docs\process\CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md

```text
# Carver M0 Source-Native Futures Foundation Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M0_FOUNDATION_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

M0 is the lean foundation layer for future Carver source-native futures briefs.

It locks the process defaults and unresolved atoms that every later candidate or portfolio brief must inherit before any data work, implementation, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion.

M0 is not a strategy, not a backtest plan, not a data-surface acceptance, and not implementation authorization.

## Source Anchors

- The book is futures-specific and describes 30 futures strategies over a 100+ instrument universe. See `Carver.pdf`, PDF pages 11-17.
- The book uses closing prices for the relevant time period, not OHLC/candlestick inputs. See `Carver.pdf`, PDF page 15.
- Parts One, Two, and Three are daily/once-a-day strategies that share a position-management and forecast framework. See `Carver.pdf`, PDF page 17.
- Part Four uses faster intraday data and must remain a separate fast-stack lane. See `Carver.pdf`, PDF pages 475-476.
- Part Five uses relative-value synthetic instruments and must remain a separate RV-stack lane. See `Carver.pdf`, PDF pages 511-512.
- Appendix C lists the book's 102-instrument Jumbo futures universe and warns that broker market codes may vary. See `Carver.pdf`, PDF pages 690-695.

Page references in M0 are process anchors. Every future candidate or portfolio brief must re-check its own source pages before lock.

## Lane Class

Default Carver book strategy lane class:

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened by M0.

Any later CFD adapter work requires a separate explicit adapter gate after source-native behavior exists.

## Data Surface Posture

Operator-reported local data surface:

```text
NINJATRADER_SOURCE_NATIVE_FUTURES_DATA_SURFACE_CANDIDATE
```

Operator reports that local NinjaTrader futures data is available for broad futures coverage, including futures indices, metals, Bitcoin, and Ether, with resolution/coverage reported down to 1-minute bars and daily candles available where needed.

This is availability context only. It is not data-quality acceptance, not data acceptance, not export authorization, not parsing authorization, not diagnostic authorization, and not backtest authorization.

### Local Native Timeframe First

When a future data lane is explicitly authorized, prefer local NinjaTrader source-native futures data at the native timeframe required by the strategy.

- Use native completed daily candles for daily Carver strategies where available.
- Use native completed hourly or smaller intraday bars only for fast-stack strategies that require them.
- Do not reconstruct daily or hourly bars from 1-minute data by default.
- Reconstruct from 1-minute data only if local native timeframe data is missing, invalid, or a separate data-quality gate justifies reconstruction.
- Download or fetch external data only if local NinjaTrader data is missing, insufficient, or materially less efficient than obtaining a native source timeframe.

### NinjaTrader Non-Authorization

M0 authorizes no NinjaTrader subscription, export, parsing, brokerage connection, order-routing setup, account file handling, credential handling, live trading configuration, or broker/account integration.

Any NinjaTrader use must first pass a separate source-native data-surface gate.

## Completed-Bar Rule

All future lanes must use completed bars only.

- Daily strategies: completed daily bars.
- Fast-stack strategies: completed intraday bars at the authorized timeframe.
- RV-stack strategies: completed bars for every leg, synchronized according to the locked synthetic-instrument rule.

No lane may use partial bars or future information.

## Source-Native Instrument Identity

Each future candidate or portfolio brief must lock, before data work:

- Book instrument name.
- Book/broker code from Appendix C where applicable.
- Exchange.
- Currency.
- Multiplier.
- First source-usable date or first data date.
- Micro, mini, or full-size contract identity.
- Any substitution rule.

Book-preferred instruments must be used where available. If the exact source-native instrument is unavailable, record blockage rather than silently substituting a CFD, index proxy, ETF, adjacent ticker, or old QuantLab symbol.

## Timeframe Families

M0 recognizes three Carver source-native futures stacks:

| Stack | Scope | Default data posture |
| --- | --- | --- |
| Daily directional stack | Parts One, Two, Three | Native completed daily candles. |
| Fast stack | Part Four, S26-S27 | Separate intraday gate; use native completed intraday bars. |
| RV stack | Part Five, S28-S30 | Separate synthetic-instrument gate; use completed bars for all legs. |

No fast-stack or RV-stack lane is opened by M0.

## Foundation Atoms To Lock Per Candidate

Every candidate or portfolio brief must explicitly resolve or mark unresolved:

- Contract identity and source-native instrument mapping.
- Data surface and native timeframe.
- Exchange session definition.
- Timezone.
- Bar close timestamp semantics.
- Holiday calendar.
- Daily candle cut convention.
- Intraday bar timestamp convention when applicable.
- Continuous-contract construction.
- Contract selection and rolling rule.
- Back-adjusted price construction.
- Cost source.
- FX/currency conversion.
- Target risk and capital base.
- Volatility estimate.
- Position sizing.
- Rounding.
- Buffering.
- Instrument eligibility.
- Evidence-window budget.
- Fail-closed behavior for missing or invalid inputs.

If a required atom is unresolved, the lane remains process-only and cannot proceed to implementation or data work.

## Costs

Execution costs must come from:

```text
config/costs.json
```

once such a file exists and is explicitly authorized for the relevant lane.

No hardcoded ad hoc cost dictionaries are allowed.

If costs are unavailable, the candidate or portfolio brief must record the cost-source blockage.

## Evidence Window Guard

The default evidence sequence remains:

```text
Development/Reconciliation -> TEST -> VALIDATION -> LOCKBOX -> Forward
```

Development/Reconciliation is process/readiness work and not promotion evidence.

No diagnostic or backtest over 2 years may be run without explicit operator approval.

M0 authorizes no diagnostics and no backtests.

## Implementation And Test Posture

M0 does not authorize implementation.

After a candidate or module brief is locked, implementation still requires separate explicit implementation authorization.

When implementation is later authorized, the first tests must be synthetic/source-conformance tests, not historical backtests:

- Tiny formula/unit tests.
- Hand-built golden toy examples.
- Invariant tests.
- Book numeric example checks where available.
- Synthetic dry-run/schema checks.

Historical data evaluation requires a later separate operator authorization.

## Strategy And Portfolio Interpretation

Each strategy must be labeled before interpretation:

```text
STANDALONE_CANDIDATE
SOURCE_NATIVE_PORTFOLIO_SLEEVE
PORTFOLIO_ONLY_COMPONENT
BLOCKED_SOURCE_UNRESOLVED
PARKED_NOT_STANDALONE
```

Complete book portfolios must be reconstructed separately from individual sleeve results.

A sleeve failing standalone is not family death if the book frames it as portfolio material.

A parked/not-standalone strategy is not failed alpha.

S29 and S30 remain parked/not-standalone unless a future page-audited process artifact, direct Carver source justification, and explicit operator approval changes that classification.

## Old Workspace Quarantine

The old `C:\Users\openclaw\Desktop\QuantLab_v3` workspace is archived and must not be used for active pipelines.

M0 rejects as active authority:

- Old CFD adapters.
- Old broker-clock assumptions.
- Old data-prep scripts.
- Old mixed futures/CFD translation scripts.
- Old TEST/VALIDATION/Lockbox state.
- Old contaminated results.
- Old pipeline convenience shortcuts.

The two prior backtests remain parked operator memory for this lesson only:

```text
NON_POSITIVE_STANDALONE_DOES_NOT_ADVANCE
```

If cited beyond that general lesson, they must first be named or hash-bound in a separate process-only archaeology memo.

## Hostile Audit Requirement

Any process artifact, candidate brief, portfolio brief, implementation attestation, diagnostic result, backtest result, or gate memo that may influence a lane decision must receive a hostile audit before it is treated as locked.

Required hostile-audit method:

```text
USE_SUBAGENT_FOR_HOSTILE_AUDIT
```

Hostile audits must use a subagent unless the operator explicitly waives that requirement for a specific artifact.

## M0 Output

M0 produces only this process foundation.

The next process step, if explicitly authorized, is S01 candidate-brief drafting:

```text
PROCESS_ONLY_CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

S01 must inherit M0 and may not open implementation, data work, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, or promotion.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

```

# FILE: docs\process\CARVER_M1_POSITION_SIZING_AND_RISK_SCALING_MODULE_SPEC_2026-05-28.md

```text
# Carver M1 Position Sizing And Risk Scaling Module Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M1_POSITION_SIZING_RISK_SCALING_MODULE_SPEC_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Define the process-only implementation-ready contract for Carver Module M1:

```text
M1_POSITION_SIZING_AND_RISK_SCALING
```

M1 specifies the source-native futures atoms needed to transform capital, target risk, instrument risk, futures contract identity, FX, instrument weights, IDM, and optional forecast strength into desired futures contract exposure.

This module spec is not code, not a data lane, not a test lane, not a diagnostic lane, not a backtest lane, not an OOS lane, not a Lockbox lane, not a Forward lane, not a CFD adapter lane, not deployment, not trading, and not promotion.

## Scope

M1 owns:

- Capital-first position sizing.
- Instrument risk in annual percentage or daily price-point units.
- Target risk in annualized percentage standard deviation.
- Futures multiplier, current held-contract raw price, and FX conversion.
- Pre-validated variable volatility estimate as an input from S03/M0-locked atoms.
- Instrument weight for portfolio contexts.
- IDM as an input for portfolio contexts.
- Optional forecast strength as an input from M2.
- Whole-contract rounding policy as an unresolved atom.
- Minimum capital and indivisible-contract constraints.
- Fail-closed behavior for invalid sizing inputs.

M1 does not own:

- Forecast construction, forecast scalars, forecast caps, forecast weights, or FDM. Those belong to M2.
- Instrument universe selection, portfolio weights, IDM estimation, or portfolio aggregation. Those belong to M3.
- Futures curve/carry construction. That belongs to M5.
- Data loading, market-row parsing, NinjaTrader export, or historical evaluation.

## Source Anchors

- S02 reverses the S01 order: given capital first, calculate position size second, with instrument risk as the key input. See `Carver.pdf`, PDF page 67.
- S02 measures single-contract risk as annualized standard deviation of returns and translates it into currency terms using current price, futures multiplier, and notional exposure. See PDF pages 68-70.
- S02 states that the price used for sizing should be the price of the expiry currently held, not the back-adjusted price, and includes FX conversion. See PDF page 70.
- S02 defines target risk as annualized percentage standard deviation on capital and derives the required contract count by equating target currency risk with position risk. See PDF pages 70-71.
- S02 gives a daily price-point risk formulation based on daily back-adjusted price differences, useful when the current futures price is negative. See PDF page 72.
- S02 recalculates optimal position daily from current futures price and FX rate, then rounds contract count. See PDF pages 79-81.
- S02 uses fixed notional capital for performance reporting but warns real-money sizing should reduce after losses by using current account value as notional capital. See PDF pages 82-84.
- S02 introduces minimum capital because futures contracts are indivisible and recommends enough capital to start with at least four contracts. See PDF pages 85-87.
- S03 replaces S02 fixed instrument risk with a variable volatility estimate and reduces/increases positions as volatility rises/falls. See PDF pages 95-98.
- S04 generalizes position sizing by multiplying capital by instrument weight and later by IDM for diversification correction. See PDF pages 119-123.
- S09, S10, and S11 plug capped combined forecasts into the familiar position-sizing equations. See PDF pages 221-222, 253, and 270.

## Implementation-Ready Contract

M1 should later expose these process-level transformations once implementation is separately authorized:

1. Resolve sizing context.
   Required inputs: lane class, instrument identity, completed-bar timestamp, active stack bar convention, capital base, target risk, current held-contract raw price, multiplier, FX rate, pre-validated risk estimate, and source stack.

2. Resolve optional portfolio context.
   Required inputs when applicable: instrument weight and IDM from M3.

3. Resolve optional forecast context.
   Required input when applicable: capped combined forecast from M2. Forecast value must already be capped and source-valid before M1 receives it.

4. Produce desired unrounded contract exposure.
   Output is an unrounded desired contract count in futures contracts.

5. Apply rounding policy.
   Output is desired rounded contract count or fail-closed blockage if rounding policy is unresolved.

6. Emit sizing audit fields.
   Output must preserve all source inputs, timestamp semantics, and blockage reasons for later review.

This is an interface contract only. No executable formula, code path, or test is authorized here.

## Required Inputs

M1 requires these inputs to be locked before implementation or data work:

- Lane class: `SOURCE_NATIVE_FUTURES`.
- Instrument identity and source-native contract mapping.
- Completed-bar timestamp and active stack bar convention.
- Capital base.
- Target risk.
- Current held-contract raw price for sizing.
- Back-adjusted price-difference input if using daily price-point risk.
- Futures multiplier.
- Instrument currency and base/account currency.
- FX conversion value and timestamp convention.
- Risk estimate in annual percentage terms or daily price-point terms.
- Risk-estimate construction lock: fixed S02 risk or S03 variable-risk atoms, including EWMA/span/blend/warm-up/no-lookahead convention where applicable.
- Risk estimate timestamp and no-lookahead proof: only returns completed before sizing timestamp.
- Optional instrument weight.
- Optional IDM.
- Optional capped forecast from M2.
- Contract rounding rule.
- Minimum capital and minimum starting contract-count policy.

## Required Outputs

M1 later implementation must be able to produce:

- Desired unrounded contracts.
- Desired rounded contracts after the locked rounding rule.
- Sizing unit convention used: percentage risk or daily price-point risk.
- Capital, target risk, risk estimate, price, multiplier, FX, weight, IDM, and forecast inputs used.
- Completed-bar timestamp used for every input.
- Blockage reason if any required input is missing, stale, invalid, or unresolved.

## Fail-Closed Rules

M1 must fail closed if any of these are unresolved or invalid:

- Lane class is not `SOURCE_NATIVE_FUTURES`.
- Current held-contract price source is missing when percentage-risk sizing is used.
- Risk estimate is missing, zero, negative, stale, or uses future information.
- The risk estimate has not been pre-validated against the active source atoms before M1 consumes it.
- Current held-contract price, FX, capital, target risk, multiplier metadata, risk estimate, and any applicable weight, IDM, or forecast input are not timestamp-aligned to the sizing timestamp.
- Multiplier, FX, capital, target risk, or any context-applicable weight, IDM, or forecast input is missing or invalid.
- Rounding rule is unresolved.
- Instrument identity or roll/contract mapping is unresolved.
- Minimum-capital rule fails where the downstream lane requires tradable contract granularity.
- Any CFD proxy, adjacent symbol, ETF proxy, or old QuantLab symbol is introduced.

## Open Atoms

These atoms remain unresolved until a later authorized implementation or data-surface gate:

- Exact capital-base policy: fixed notional, current account value, or source-example capital.
- Exact target-risk policy per candidate or portfolio breadth.
- Exact annualization convention where source references differ by context.
- Exact percentage-risk versus daily-price-point sizing form by stack.
- Exact rounding rule. M1 stops at desired exposure; buffer and trade/no-trade decisions must remain in M2 or a separately authorized downstream trade-decision module.
- Exact minimum-capital rule and minimum starting contract-count rule.
- Exact FX timestamp convention.
- Exact handling of negative current futures prices.
- Exact synthetic conformance examples for later authorized implementation tests.

## Downstream Users

M1 is used by:

- S02 fixed-risk single-instrument sizing.
- S03 variable-risk single-instrument sizing.
- S04/P01/P02 multi-instrument portfolio sizing.
- S09 trend forecast-scaled sizing.
- S10 carry forecast-scaled sizing.
- S11 combined trend/carry forecast-scaled sizing.

## Hostile Audit Requirement

Before M1 is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- Source-page faithfulness.
- Correct separation from M2, M3, and M5.
- No formula implementation or code leakage.
- No data, test, diagnostic, backtest, or promotion leakage.
- No CFD, NinjaTrader operational, or old QuantLab contamination.
- Completeness of inputs, outputs, unresolved atoms, and fail-closed rules.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition after patch:

- Blocking finding patched: M1 now requires the risk estimate to be pre-validated against S02/S03 source atoms before M1 consumes it.
- Medium findings patched: optional weight, IDM, and forecast inputs now fail closed only when applicable to the active context; M1 explicitly stops at desired exposure and leaves buffer/trade-decision ownership outside M1.
- Timestamp finding patched: all sizing inputs must be timestamp-aligned to the sizing timestamp.
- Daily over-specificity patched: the spec now uses active stack bar convention while the current clean spine remains daily for S02-S11.

No data, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab, tuning, deployment, trading, or promotion leakage remains authorized by this artifact.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

```

# FILE: docs\process\CARVER_M2_FORECAST_BLOCK_ARCHITECTURE_MODULE_SPEC_2026-05-28.md

```text
# Carver M2 Forecast Block Architecture Module Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M2_FORECAST_BLOCK_ARCHITECTURE_MODULE_SPEC_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Define the process-only implementation-ready contract for Carver Module M2:

```text
M2_FORECAST_BLOCK_ARCHITECTURE
```

M2 specifies the common forecast-block architecture used by S09, S10, and S11: raw forecasts, risk normalization, forecast scalars, forecast caps, cost/speed eligibility, forecast weights, forecast diversification multiplier, combined forecast cap, and buffer/trade-decision atoms.

This module spec is not code, not a data lane, not a test lane, not a diagnostic lane, not a backtest lane, not an OOS lane, not a Lockbox lane, not a Forward lane, not a CFD adapter lane, not deployment, not trading, and not promotion.

## Lane Class

Current Carver spine lane class for M2:

```text
SOURCE_NATIVE_FUTURES
```

M2 does not open `CFD_DIRECT` or `CFD_ADAPTER`. Any future adapter use of forecast outputs requires a separate adapter gate after source-native behavior exists.

## Scope

M2 owns:

- Trading-rule forecast identity and style grouping.
- Raw forecast input contract.
- Risk-normalized forecast contract.
- Forecast scalar source tables.
- Individual forecast cap.
- Forecast variation eligibility by cost/speed limit.
- Forecast weights.
- FDM lookup and row-selection rules.
- Combined forecast cap.
- Buffer-zone and trade/no-trade source atoms where inherited by forecast strategies.
- No-lookahead and completed-bar forecast timestamp rules.

M2 does not own:

- Futures position-size arithmetic from capital/risk/multiplier/FX. That belongs to M1.
- Instrument weights, IDM, portfolio aggregation, or universe selection. Those belong to M3.
- Carry curve construction. That belongs to M5.
- Data loading, code implementation, tests, diagnostics, or backtests.

## Source Anchors

- S07 defines a forecast as a value proportional to expected risk-adjusted return and establishes the forecast/trading-rule terminology used by later forecast-block strategies. See `Carver.pdf`, PDF pages 179-180.
- S07 uses daily price-point risk to normalize trend crossover forecasts so forecast values can be compared across time and instruments. See PDF pages 179-180.
- S09 selects EWMAC trend variations 2, 4, 8, 16, 32, and 64 and uses forecast scalars, caps, optimal unrounded position, buffer zone, and trade/no-trade decision. See PDF pages 202-204.
- S09 combines capped forecasts with non-negative forecast weights that sum to 1. See PDF pages 208-209.
- S09 uses a trading-rule cost/speed eligibility rule before allocating forecast weights. The current definition pack records 0.15 SR units as source context, but the exact quote and page reference must be re-page-audited before implementation. See PDF pages 216-218 and the general cost-speed rule on PDF page 112.
- S09 applies FDM to combined trend forecasts, then caps the combined forecast again at absolute value 20. See PDF pages 221-222.
- S10 treats risk-adjusted carry as a forecast because it is expected annual return divided by annualized risk. See PDF page 241.
- S10 smooths carry forecasts over spans 5, 20, 60, and 120 business days, uses forecast scalar 30, caps forecasts, weights eligible spans equally, and applies carry FDM. See PDF pages 247-253.
- S11 states that scaled trading-rule forecasts are building blocks that can be combined because they share a common scale. See PDF pages 264-265.
- S11 uses top-down forecast weighting by style, rule, and variation; trend is divergent, carry is convergent, and the source example uses 60% trend and 40% carry. See PDF pages 265-268.
- S11 provides source table examples for combined trend/carry weights and approximate FDM by number of trading rules. The table-number/page labels for Tables 51 and 52 must be re-page-audited before implementation; interpolation remains blocked unless separately operator-locked before data work.

## Implementation-Ready Contract

M2 should later expose these process-level transformations once implementation is separately authorized:

1. Receive completed-bar source inputs for one instrument and one timestamp.
2. Construct or receive raw forecast values according to the locked rule family.
3. Normalize raw forecasts to risk-adjusted forecast units.
4. Apply source-locked forecast scalar.
5. Apply individual forecast cap.
6. Apply pre-locked cost/speed eligibility to decide which forecast variations are allowed.
7. Assign forecast weights by the locked top-down or table rule.
8. Combine capped forecasts.
9. Apply source-locked FDM.
10. Apply final combined forecast cap.
11. Emit capped combined forecast to M1.
12. Emit buffer/trade-decision atoms when the future implementation lane opens.

This is an interface contract only. No executable forecast implementation, code path, or test is authorized here.

## Source Tables To Lock

S09 trend forecast scalars:

| Filter | Scalar |
| --- | ---: |
| EWMAC2 | 12.1 |
| EWMAC4 | 8.53 |
| EWMAC8 | 5.95 |
| EWMAC16 | 4.10 |
| EWMAC32 | 2.79 |
| EWMAC64 | 1.91 |

S09 trend turnover estimates:

| Filter | Turnover per year |
| --- | ---: |
| EWMAC2 | 98.5 |
| EWMAC4 | 50.2 |
| EWMAC8 | 25.4 |
| EWMAC16 | 13.2 |
| EWMAC32 | 7.6 |
| EWMAC64 | 5.2 |

S09 trend FDM rows:

| Allowed filters | Forecast weight per filter | FDM |
| --- | ---: | ---: |
| EWMAC2, 4, 8, 16, 32, 64 | 0.167 | 1.26 |
| EWMAC4, 8, 16, 32, 64 | 0.2 | 1.19 |
| EWMAC8, 16, 32, 64 | 0.25 | 1.13 |
| EWMAC16, 32, 64 | 0.333 | 1.08 |
| EWMAC32, 64 | 0.50 | 1.03 |
| EWMAC64 | 1.0 | 1.0 |

S10 carry source values:

| Item | Value |
| --- | ---: |
| Carry forecast scalar | 30 |
| Carry spans | 5, 20, 60, 120 business days |
| Carry5 turnover | 5.75 |
| Carry20 turnover | 3.12 |
| Carry60 turnover | 1.82 |
| Carry120 turnover | 1.22 |

S10 carry FDM rows:

| Allowed carry spans | Forecast weight per span | FDM |
| --- | ---: | ---: |
| Carry5, 20, 60, 120 | 0.25 | 1.04 |
| Carry20, 60, 120 | 0.333 | 1.03 |
| Carry60, 120 | 0.5 | 1.02 |
| Carry120 | 1.0 | 1.0 |

S11 shared source values:

- Trend style: divergent.
- Carry style: convergent.
- Source style mix: 60% trend, 40% carry.
- Table 51 weights: source example rows to re-page-audit and lock before implementation.
- Table 52 FDM: approximate FDM by number of trading rules, with table-number/page labels to re-page-audit before implementation; interpolation is not authorized unless separately operator-locked before data work.

## Required Inputs

M2 requires these inputs to be locked before implementation or data work:

- Lane class: `SOURCE_NATIVE_FUTURES`.
- Completed-bar timestamp.
- Instrument identity.
- Forecast family: EWMAC trend, carry, or combined trend/carry.
- Input price series convention.
- Risk normalization convention.
- Forecast scalar source.
- Individual forecast cap.
- Cost-per-trade source and speed-limit rule.
- Turnover table or locked turnover source.
- Forecast variation set.
- Forecast weight rule.
- FDM table and row-selection rule.
- Combined forecast cap.
- Buffer rule and buffer-size source, if the downstream strategy uses buffered trading.

## Required Outputs

M2 later implementation must be able to produce:

- Raw forecast per rule variation.
- Scaled forecast per rule variation.
- Individually capped forecast per rule variation.
- Eligibility status per variation.
- Forecast weight per retained variation.
- Pre-FDM combined forecast.
- FDM used.
- Post-FDM combined forecast.
- Final capped combined forecast for M1.
- Blockage reason if forecast construction, eligibility, weighting, FDM, cap, or buffer rule is unresolved.

## Fail-Closed Rules

M2 must fail closed if:

- Lane class is missing or is not exactly `SOURCE_NATIVE_FUTURES`.
- Any forecast uses incomplete bars or future information.
- Forecast scalar, cap, speed limit, turnover, weight, or FDM source is unresolved.
- Cost eligibility cannot be determined but is required for the strategy.
- A required carry forecast needs M5 output that is unavailable or blocked.
- No eligible forecast variation remains and the candidate has no pre-locked fallback.
- S07/S08 trend components are promoted as standalone candidates through this module.
- Any parameter is changed after seeing results.

## Open Atoms

These atoms remain unresolved until a later authorized implementation gate:

- Exact EWMA calculation convention and warm-up behavior.
- Exact buffer-zone formula and trade/no-trade boundary.
- Exact handling of instruments with partial forecast-family availability.
- Exact Table 51 row-selection rule.
- Exact Table 51 table-number/page-label verification.
- Exact Table 52 interpolation policy.
- Exact Table 52 table-number/page-label verification.
- Exact synthetic conformance examples for later authorized implementation tests.

## Downstream Users

M2 is used by:

- S09 multiple trend following.
- S10 basic carry, where raw carry comes from M5.
- S11 combined carry and trend.
- Later Part Two and Part Three forecast-block extensions, only if separately authorized.

## Hostile Audit Requirement

Before M2 is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- Source-page faithfulness.
- Correct separation from M1, M3, and M5.
- Correct non-advancement of S07/S08 standalone status.
- No code, data, test, diagnostic, backtest, or promotion leakage.
- No tuning leakage after results.
- Completeness of inputs, outputs, unresolved atoms, and fail-closed rules.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition:

- No blocking findings against the M2 artifact.
- Source tables, S07/S08 sleeve non-advancement, module boundaries, and sensitive-stage non-authorization language were found process-safe.
- Residual watch items remain open atoms: EWMA convention/warm-up, buffer-zone formula, partial forecast-family handling, Table 51 row selection, Table 52 interpolation policy, and synthetic conformance examples.

No data, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab, tuning, deployment, trading, or promotion leakage remains authorized by this artifact.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

```

# FILE: docs\process\CARVER_M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION_MODULE_SPEC_2026-05-28.md

```text
# Carver M3 Multi-Instrument Portfolio Construction Module Spec

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION_MODULE_SPEC_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Define the process-only implementation-ready contract for Carver Module M3:

```text
M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION
```

M3 specifies the shared portfolio construction atoms for S04, P01, P02, and future Jumbo portfolios: instrument universe, instrument weights, top-down allocation, IDM, portfolio breadth target-risk rules, eligibility, portfolio synchronization, and aggregation boundaries.

This module spec is not code, not a data lane, not a test lane, not a diagnostic lane, not a backtest lane, not an OOS lane, not a Lockbox lane, not a Forward lane, not a CFD adapter lane, not deployment, not trading, and not promotion.

## Scope

M3 owns:

- Portfolio instrument universe declaration.
- Instrument weights as risk-capital weights.
- Top-down asset-class/group/instrument weight construction.
- Portfolio-level capital and target-risk policy atoms.
- Instrument diversification multiplier.
- Portfolio minimum-capital constraints.
- Instrument eligibility: cost, liquidity, source availability, and minimum capital.
- Completed-bar synchronization across instruments.
- Portfolio aggregation boundary and fail-closed rules.

M3 does not own:

- Single-instrument contract sizing arithmetic. That belongs to M1.
- Forecast construction and FDM. That belongs to M2.
- Carry curve construction. That belongs to M5.
- Data loading, code implementation, tests, diagnostics, or backtests.

## Source Anchors

- S04 moves from single-instrument S03 to portfolios where each sub-strategy is a version of S03 trading a different instrument. See `Carver.pdf`, PDF page 118.
- S04 says capital chunks become instrument risk allocations because each sub-strategy has approximately the same risk. See PDF page 118.
- Risk parity P01 splits capital 50/50 between S&P 500 micro futures and US 10-year bond futures. See PDF pages 119-120.
- S04 introduces IDM to correct for diversification and scale aggregate portfolio risk toward the target. See PDF pages 122-123.
- P02 All Weather uses instrument weights as risk allocations: 25% S&P 500 micro, 12.5% US 10-year, 12.5% US 5-year, 12.5% WTI Crude Oil mini, 12.5% Corn, and 25% Gold micro. See PDF page 125.
- S04 generalized risk premia uses cost, liquidity, and minimum-capital eligibility rules. See PDF page 127.
- S04 modifies minimum capital for instrument weights and IDM. See PDF pages 127-128.
- S04 handcrafting allocates first by asset class, then group, then instrument. See PDF pages 130-135.
- S04 Table 16 supplies approximate IDM values by number of instruments and warns the table assumes a relatively diversified instrument set. See PDF page 135.
- S04 gives an automatic selection procedure based on possible instruments, lowest-cost first instrument, trial portfolios, weights, IDM, minimum-capital checks, expected SR from costs/correlations, and a 10% stop rule. See PDF pages 135-140.
- S04 defines the Jumbo portfolio as 102 instruments meeting cost/liquidity thresholds and at least one year of data, using USD 50 million capital and handcrafted weights. The definition pack records IDM 2.47 as source context for the book example, but the exact value/page quote must be re-page-audited before implementation. See PDF page 141.
- S04 advises target-risk levels by portfolio breadth: 10% for one instrument, interpolate 10%-20% for two to six instruments, 20% only with all seven asset classes, and up to 25% only with at least two instruments from each asset class. See PDF pages 143-144.

## Implementation-Ready Contract

M3 should later expose these process-level transformations once implementation is separately authorized:

1. Receive an authorized portfolio intent.
2. Validate source-native instrument identities and local mapping lock status.
3. Apply the locked universe/eligibility rules.
4. Construct or validate instrument weights.
5. Resolve portfolio target-risk policy and capital base.
6. Resolve IDM source and value/rule.
7. Emit per-instrument portfolio context for M1: weight, IDM, capital base, and target risk.
8. Emit synchronization and aggregation rules for future child lanes.
9. Fail closed on missing/ineligible instruments or unresolved weight/IDM/eligibility atoms.

This is an interface contract only. No executable portfolio implementation, selection run, data query, or backtest is authorized here.

## Source Tables And Examples

P01 source example:

| Instrument | Weight | Appendix C code |
| --- | ---: | --- |
| S&P 500 micro future | 50% | `MES` |
| US 10-year bond future | 50% | `ZN` |

P02 source example:

| Instrument | Weight | Appendix C code |
| --- | ---: | --- |
| S&P 500 micro future | 25.0% | `MES` |
| US 10-year bond future | 12.5% | `ZN` |
| US 5-year bond future | 12.5% | `ZF` |
| WTI Crude Oil mini future | 12.5% | `QM` |
| Corn future | 12.5% | `ZC` |
| Gold micro future | 25.0% | `MGC` |

Appendix C broker codes may differ from local or official exchange codes. They are source-reference labels, not data-lane authorization; every future local symbol mapping, source-native contract identity, roll rule, and no-silent-substitution decision must be locked before data work.

## Required Inputs

M3 requires these inputs to be locked before implementation or data work:

- Portfolio ID and source pages.
- Lane class: `SOURCE_NATIVE_FUTURES`.
- Instrument universe.
- Source-native instrument identity for every member.
- Local symbol mapping status for every member.
- Asset class, group, and instrument classification when using handcrafted weights.
- Instrument weights or deterministic weight-construction rule.
- Portfolio capital base.
- Portfolio target-risk rule.
- IDM source and exact value/rule.
- IDM table validity check for diversification breadth.
- Cost eligibility rule.
- Liquidity eligibility rule.
- Minimum-capital rule.
- Completed-bar synchronization rule across instruments.
- Fail-closed behavior for unavailable or ineligible members.

## Required Outputs

M3 later implementation must be able to produce:

- Locked portfolio member list.
- Instrument weight per member.
- Instrument eligibility status and blockage reason.
- Portfolio target risk and capital base.
- IDM used and source.
- Per-instrument context for M1.
- Portfolio synchronization rule.
- Portfolio aggregation convention for completed daily PnL, only after separately authorized.

## Fail-Closed Rules

M3 must fail closed if:

- Lane class is missing or is not exactly `SOURCE_NATIVE_FUTURES`.
- Any instrument identity is unresolved.
- Any local mapping is silently substituted.
- M3 is used as a substitute for a separately locked complete portfolio brief, member list, and portfolio-specific source-page lock.
- Instrument weights do not sum according to the locked rule.
- IDM source or applicability is unresolved.
- Portfolio breadth does not support requested target risk.
- Cost, liquidity, or minimum-capital eligibility cannot be evaluated once required.
- Correlation matrices or expected-SR inputs are inspected before being pre-locked.
- A portfolio drops, rescues, reweights, or adds members after seeing results.
- Any old QuantLab symbol, CFD proxy, ETF proxy, or adjacent ticker is used as authority.

## Open Atoms

These atoms remain unresolved until a later authorized implementation or data-surface gate:

- Exact source-native universe for P03/P04 and later portfolios.
- Exact local symbol mapping for Appendix C broker codes.
- Exact asset-class/group taxonomy for all 102 Jumbo instruments.
- Exact IDM policy: source examples, Table 16, calculated IDM, or blocked.
- Exact source-example IDM value/page verification for P02 and Jumbo before those values are quoted as locked authority.
- Exact correlation matrix source if automatic selection is ever authorized.
- Exact expected-SR assumption if automatic selection is ever authorized.
- Exact portfolio aggregation convention for missing instruments and staggered first usable dates.
- Exact synthetic conformance examples for later authorized implementation tests.

## Downstream Users

M3 is used by:

- S04 buy-and-hold portfolio construction.
- P01 risk parity.
- P02 All Weather.
- P03/P04 and later Jumbo portfolio briefs if separately authorized.
- S09/S10/S11 portfolio children if separately authorized.

## Hostile Audit Requirement

Before M3 is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- Source-page faithfulness.
- Correct separation from M1, M2, and M5.
- No portfolio execution, data selection, or backtest leakage.
- No post-result instrument selection or reweighting leakage.
- Correct Appendix C code warning.
- Completeness of inputs, outputs, unresolved atoms, and fail-closed rules.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition after patch:

- No blocking findings against the M3 artifact.
- Non-blocking lane-class finding patched: M3 now fails closed unless lane class is exactly `SOURCE_NATIVE_FUTURES`.
- Non-blocking portfolio-independence finding patched: M3 cannot substitute for a separately locked portfolio brief, member list, and source-page lock.
- Appendix C warning strengthened to require later local mapping, source-native identity, roll-rule, and no-silent-substitution locks before data work.

No data, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, old QuantLab, tuning, deployment, trading, or promotion leakage remains authorized by this artifact.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

```

# FILE: docs\researchops\portfolios\CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md

```text
# Carver P01 Risk Parity Example Portfolio Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures portfolio brief for Carver Portfolio 1:

```text
P01_RISK_PARITY_EXAMPLE_PORTFOLIO
```

This brief inherits M0, S01, S02, S03, and S04. It reconstructs the P01 source framing and required atoms before any data work, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion.

This is a complete portfolio reconstruction brief. It is not inferred from standalone sleeve results.

## Classification

| Field | Value |
| --- | --- |
| Portfolio ID | P01 |
| Book portfolio | Risk parity example portfolio |
| Book pages | `Carver.pdf`, PDF pages 119-123 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Portfolio type | Two-instrument risk parity example |
| Member strategy machinery | S03 variable-risk buy-and-hold, wrapped by S04 portfolio construction |
| Timeframe family | Daily directional portfolio stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

P01 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md`

P01 is a prerequisite example for:

- P02 All Weather example portfolio.
- P03 generalized risk premia portfolio construction.
- P04 Jumbo buy-and-hold portfolio.
- Any later portfolio brief that uses instrument weights and IDM.

## Book Framing

Carver frames P01 as the first concrete S04 variation: a futures risk parity portfolio combining equity beta and bond duration.

Source anchors:

- The risk parity variation begins on `Carver.pdf`, PDF page 119.
- The book contrasts ordinary 60/40 cash allocation with futures-based risk allocation, noting that equities have higher risk than bonds on PDF page 119.
- Carver says S03 provides the method to construct a risk parity portfolio that can be leveraged to hit a required risk target or return expectation on PDF page 119.
- The P01 example splits total capital equally: 50% to the S&P 500 micro future and 50% to the US 10-year bond future on PDF page 120.
- The position-sizing formula generalizes S03 by applying the instrument weight to portfolio capital for each instrument on PDF page 120.
- In the book example, total capital is USD 1,000,000 and target risk is 20% on PDF page 120.
- Table 12 shows individual and aggregate results before IDM, and Carver explains that aggregate risk is below target because the two sub-strategy returns are not perfectly correlated on PDF pages 120-122.
- Carver introduces the instrument diversification multiplier (`IDM`) to scale positions so expected aggregate risk reaches target on PDF page 122.
- The book derives a rough IDM of 1.32 by dividing the 20% target risk by 15.1% realised aggregate risk in the example on PDF page 122.
- Table 13 shows the risk parity example after applying IDM 1.32, with aggregate standard deviation near 20% on PDF pages 122-123.
- Carver notes that leverage and costs rise with IDM, while risk-adjusted statistics are mostly unchanged except for rounding effects on PDF page 123.

## Portfolio Interpretation

P01 is a complete source-native futures portfolio reconstruction:

```text
SOURCE_NATIVE_FUTURES_PORTFOLIO_RECONSTRUCTION
```

P01 is not a standalone single-instrument candidate and not a sleeve result. It is the smallest complete book portfolio and should be used to lock the end-to-end portfolio mechanics before larger portfolio examples.

P01 should be used to lock these source-native portfolio primitives:

- Two instrument identities.
- Equal 50/50 instrument weights.
- S03 variable-risk sub-strategy per instrument.
- Portfolio-level capital base.
- Portfolio-level target risk.
- IDM application.
- Completed daily PnL aggregation across instruments.
- Portfolio cost aggregation.
- Fail-closed behavior when either leg is unavailable or unresolved.

## Portfolio Rule Skeleton

The P01 source rule skeleton is:

```text
For S&P 500 micro futures and US 10-year bond futures:
assign each instrument 50% portfolio weight,
run an S03-style long buy-and-hold variable-risk sub-strategy for each leg,
scale each leg by its instrument weight and the locked IDM rule,
round each leg according to the locked rule,
roll each leg according to its locked source-native roll rule,
aggregate completed daily PnL across both legs,
account for costs separately once a cost source is authorized.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, backtest rule, OOS rule, Lockbox rule, Forward rule, or promotion rule is authorized by this skeleton.

## Inherited Machinery

P01 inherits:

- M0 source-native futures defaults and non-authorization.
- S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S02 target-risk position sizing and whole-contract rounding.
- S03 variable risk estimation, non-leaking risk rule, and risk-adjusted cost atoms.
- S04 instrument weights, IDM, portfolio breadth, and multi-instrument aggregation atoms.

P01 does not authorize recalculating any inherited atom from data.

## Source-Named Instruments

The P01 book example uses:

| Role | Instrument | Book/Appendix C market code | Exchange | Currency | Multiplier | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Equity risk premium leg | S&P 500 micro future | `MES` | GLOBEX | USD | 5 | PDF pages 119-120, 692 |
| Bond duration leg | US 10-year bond future | `ZN` | ECBOT | USD | 1000 | PDF pages 119-120, 691 |

Appendix C says these market codes are the codes used by Carver's broker and may differ across brokers or official exchange codes. Any future data lane must lock exact local symbol mapping, source-native contract identity, roll rules, and whether Appendix C codes match local NinjaTrader symbols. No silent substitution, CFD proxy, ETF proxy, adjacent ticker, or old QuantLab symbol is authorized by this brief.

## Source Portfolio Parameters

The P01 book example records:

| Field | Book example value | Status |
| --- | --- | --- |
| Instrument weights | 50% S&P 500 micro, 50% US 10-year bond | Source example only; must be locked before data |
| Capital | USD 1,000,000 | Source example only; operator capital rule unresolved |
| Target risk | 20% annualised standard deviation | Source example only; portfolio breadth rule unresolved |
| IDM | 1.32 | Source example only; use or recomputation must be explicitly locked |

The IDM value in the book is derived from example realised aggregate risk. This brief does not authorize calculating IDM from local historical market data. Any future IDM source must be pre-locked before market-data inspection or remain blocked.

## Required Atoms Before Data Work

P01 cannot proceed to data work until all inherited atoms and these P01-specific atoms are locked:

- Exact source-native identity for `MES` or documented source-native S&P 500 historical bridge.
- Exact source-native identity for `ZN` or documented source-native US 10-year historical bridge.
- Exact local NinjaTrader symbol mapping for both instruments.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for both instruments.
- Daily bar synchronization rule across both instruments.
- Continuous-contract construction and roll rule for both instruments.
- Back-adjustment method for PnL for both instruments.
- Current held-contract raw price source for sizing for both instruments.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion for both instruments.
- Variable risk estimate per instrument using only returns completed before each sizing timestamp.
- Instrument weights: 50% / 50% or a documented source-rule blockage.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Pre-lock rule for any IDM calculation from correlations or realised aggregate risk.
- Contract-count rounding rule per leg.
- Portfolio aggregation convention for completed daily PnL.
- Portfolio cost aggregation rule.
- Cost source in `config/costs.json` once authorized.
- Fail-closed rule if either leg is missing, ineligible, too expensive, too illiquid, undercapitalized, or source-unresolved.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- P01 remains process-only until separately authorized.
- P01 is `SOURCE_NATIVE_FUTURES`, not CFD.
- P01 is a daily directional portfolio reconstruction.
- P01 uses completed daily bars only.
- P01 is reconstructed independently and not inferred from sleeve or standalone results.
- P01 does not authorize P02, P03, or P04.
- P01 does not authorize local data inspection or IDM calculation.
- P01 must prefer native daily futures candles when a future data lane is authorized.
- P01 must not reconstruct daily bars from 1-minute data by default.
- P01 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- P01 must not select, drop, rescue, or reweight legs after seeing results.
- P01 must not treat historical performance as promotion evidence.
- A non-positive future P01 result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native identity for the equity leg.
- Exact source-native identity for the bond leg.
- Whether either leg requires a documented source-native historical bridge.
- Exact local NinjaTrader symbol mapping for both instruments.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for both instruments.
- Daily bar synchronization rule across both instruments.
- Exact roll calendar and roll timing for both instruments.
- Exact continuous-contract/back-adjustment construction for both instruments.
- Treatment of raw futures price versus adjusted futures price for both instruments.
- Current held-contract raw price source for sizing for both instruments.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion for both instruments.
- Variable risk estimate per instrument.
- Warm-up period and first usable date per instrument.
- Instrument weights lock.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Pre-lock rule for any IDM calculation from correlations or realised aggregate risk.
- Exact contract-count rounding rule per leg.
- Portfolio aggregation convention for completed daily PnL.
- Portfolio cost aggregation rule.
- Exact cost source in `config/costs.json`.
- Fail-closed behavior for missing or invalid prices, rolls, multipliers, FX, risk estimates, costs, liquidity, capital, weights, IDM, synchronization, or sizing inputs.
- Evidence-window budget if a future diagnostic/backtest is requested.
- Exact synthetic conformance examples for later implementation testing.
- Whether any book numeric examples are sufficient for source-example conformance tests.

## Forbidden Work

This brief authorizes none of the following:

- Data export.
- Market-row parsing.
- NinjaTrader export or subscription work.
- NinjaTrader brokerage/account/credential/order-routing setup.
- Implementation.
- Unit tests.
- Synthetic tests.
- Diagnostics.
- Backtests.
- OOS, Lockbox, or Forward access.
- CFD adapter work.
- Old adapter import.
- Tuning.
- Deployment.
- Trading.
- Promotion.

## Hostile Audit Requirement

Before this P01 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0, S01, S02, S03, and S04 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct complete-portfolio reconstruction interpretation.
- Correct separation from P02, P03, and P04.
- No IDM recalculation or historical-result leakage.
- Completeness of unresolved atoms.

## Next Gate

If this P01 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No P02 work is authorized by this P01 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

```

# FILE: docs\researchops\portfolios\CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md

```text
# Carver P02 All Weather Example Portfolio Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures portfolio brief for Carver Portfolio 2:

```text
P02_ALL_WEATHER_EXAMPLE_PORTFOLIO
```

This brief inherits M0, S01, S02, S03, S04, and P01. It reconstructs the P02 source framing and required atoms before any data work, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion.

This is a complete portfolio reconstruction brief. It is not inferred from standalone sleeve results.

## Classification

| Field | Value |
| --- | --- |
| Portfolio ID | P02 |
| Book portfolio | All Weather example portfolio |
| Book pages | `Carver.pdf`, PDF pages 124-127 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Portfolio type | Six-instrument All Weather example |
| Member strategy machinery | S03 variable-risk buy-and-hold, wrapped by S04 portfolio construction |
| Timeframe family | Daily directional portfolio stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

P02 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/portfolios/CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md`

P02 is a prerequisite example for:

- P03 generalized risk premia portfolio construction.
- P04 Jumbo buy-and-hold portfolio.
- Later portfolio briefs that use asset-class buckets, sub-buckets, instrument weights, and IDM.

## Book Framing

Carver frames P02 as an All Weather extension of risk parity, adding assets that may hedge inflation and reduce dependence on the historical equity/bond correlation regime.

Source anchors:

- The All Weather variation begins on `Carver.pdf`, PDF page 124.
- Carver presents the classic All Weather cash-weight recipe as background, then distinguishes his own futures implementation on PDF pages 124-125.
- Carver states that his instrument weights reflect risk allocations rather than cash weights, because futures positions are scaled by expected standard deviation on PDF page 125.
- The P02 instrument weights are built by splitting capital into four equal buckets: stocks, bonds, commodities, and gold; then splitting bonds and commodities into two instruments each on PDF page 125.
- The P02 source weights are 25% S&P 500 micro, 12.5% US 10-year, 12.5% US 5-year, 12.5% WTI Crude Oil mini, 12.5% Corn, and 25% Gold micro on PDF page 125.
- Carver uses the same position-sizing formula as P01/S04, replacing instrument weights and instrument-specific parameters as appropriate on PDF page 125.
- The definition pack records IDM 1.81 as source context for this All Weather portfolio and the related aggregate results, but the exact value/page quote must be re-page-audited before implementation. See PDF pages 125-127.
- Tables 14 and 15 present individual and aggregate All Weather results on PDF pages 126-127; exact IDM references inside those tables must be re-page-audited before the value is quoted as locked authority.
- Carver notes the overall portfolio risk is close to the 20% target, so IDM is doing its job in the book example on PDF page 126.
- Carver warns that added diversification can still drag performance if added instruments have lower Sharpe ratios, and that backtest results should not be trusted blindly on PDF page 127.

## Portfolio Interpretation

P02 is a complete source-native futures portfolio reconstruction:

```text
SOURCE_NATIVE_FUTURES_PORTFOLIO_RECONSTRUCTION
```

P02 is not a standalone single-instrument candidate and not a sleeve result. It is the first source-defined cross-asset, six-instrument example and should be used to lock asset-bucket and sub-bucket weight handling before generalized risk premia and Jumbo portfolio work.

P02 should be used to lock these source-native portfolio primitives:

- Six source-native futures instrument identities.
- Four top-level buckets: stocks, bonds, commodities, and gold.
- Split sub-buckets for bonds and commodities.
- Instrument weights as risk allocations, not ordinary cash allocations.
- S03 variable-risk sub-strategy per instrument.
- Portfolio-level capital base.
- Portfolio-level target risk.
- IDM application.
- Completed daily PnL aggregation across six instruments.
- Portfolio cost aggregation.
- Fail-closed behavior when any leg is unavailable or unresolved.

## Portfolio Rule Skeleton

The P02 source rule skeleton is:

```text
For the six source-named All Weather futures instruments:
assign each instrument its source weight,
run an S03-style long buy-and-hold variable-risk sub-strategy for each leg,
scale each leg by its instrument weight and the locked IDM rule,
round each leg according to the locked rule,
roll each leg according to its locked source-native roll rule,
aggregate completed daily PnL across all six legs,
account for costs separately once a cost source is authorized.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, backtest rule, OOS rule, Lockbox rule, Forward rule, or promotion rule is authorized by this skeleton.

## Inherited Machinery

P02 inherits:

- M0 source-native futures defaults and non-authorization.
- S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S02 target-risk position sizing and whole-contract rounding.
- S03 variable risk estimation, non-leaking risk rule, and risk-adjusted cost atoms.
- S04 instrument weights, IDM, portfolio breadth, and multi-instrument aggregation atoms.
- P01 complete-portfolio reconstruction discipline and no-IDM-recalculation discipline.

P02 does not authorize recalculating any inherited atom from data.

## Source-Named Instruments And Weights

The P02 book example uses:

| Bucket | Instrument | Weight | Book/Appendix C market code | Exchange | Currency | Multiplier | Source |
| --- | --- | ---: | --- | --- | --- | ---: | --- |
| Stocks | S&P 500 micro future | 25.0% | `MES` | GLOBEX | USD | 5 | PDF pages 125, 692 |
| Bonds | US 10-year bond future | 12.5% | `ZN` | ECBOT | USD | 1000 | PDF pages 125, 691 |
| Bonds | US 5-year bond future | 12.5% | `ZF` | ECBOT | USD | 1000 | PDF pages 125, 691 |
| Commodities | WTI Crude Oil mini future | 12.5% | `QM` | NYMEX | USD | 500 | PDF pages 125, 695 |
| Commodities | Corn future | 12.5% | `ZC` | ECBOT | USD | 5000 | PDF pages 125, 695 |
| Gold | Gold micro future | 25.0% | `MGC` | NYMEX | USD | 10 | PDF pages 125, 694 |

Appendix C says these market codes are the codes used by Carver's broker and may differ across brokers or official exchange codes. Any future data lane must lock exact local symbol mapping, source-native contract identity, roll rules, and whether Appendix C codes match local NinjaTrader symbols. No silent substitution, CFD proxy, ETF proxy, adjacent ticker, or old QuantLab symbol is authorized by this brief.

## Source Portfolio Parameters

The P02 book example records:

| Field | Book example value | Status |
| --- | --- | --- |
| Instrument weights | 25%, 12.5%, 12.5%, 12.5%, 12.5%, 25% | Source example only; must be locked before data |
| Bucket structure | Stocks 25%, bonds 25%, commodities 25%, gold 25% | Source example only; must be locked before data |
| Target risk | 20% annualised standard deviation | Source example only; portfolio breadth rule unresolved |
| IDM | 1.81 recorded as source context pending exact quote/page re-audit | Source example only; use or recomputation must be explicitly locked |

The IDM value in the book is a source example. This brief does not authorize calculating IDM from local historical market data. Any future IDM source must be pre-locked before market-data inspection or remain blocked.

## Required Atoms Before Data Work

P02 cannot proceed to data work until all inherited atoms and these P02-specific atoms are locked:

- Exact source-native identity for each of the six instruments.
- Whether any leg requires a documented source-native historical bridge.
- Exact local NinjaTrader symbol mapping for every instrument.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument.
- Daily bar synchronization rule across all six instruments.
- Continuous-contract construction and roll rule for every instrument.
- Back-adjustment method for PnL for every instrument.
- Current held-contract raw price source for sizing for every instrument.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion for every instrument.
- Variable risk estimate per instrument using only returns completed before each sizing timestamp.
- Instrument weights exactly as source-framed or a documented source-rule blockage.
- Bucket and sub-bucket structure.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Exact IDM 1.81 source quote/page verification before treating that number as locked authority.
- Pre-lock rule for any IDM calculation from correlations or realised aggregate risk.
- Contract-count rounding rule per leg.
- Portfolio aggregation convention for completed daily PnL.
- Portfolio cost aggregation rule.
- Cost source in `config/costs.json` once authorized.
- Fail-closed rule if any leg is missing, ineligible, too expensive, too illiquid, undercapitalized, or source-unresolved.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- P02 remains process-only until separately authorized.
- P02 is `SOURCE_NATIVE_FUTURES`, not CFD.
- P02 is a daily directional portfolio reconstruction.
- P02 uses completed daily bars only.
- P02 is reconstructed independently and not inferred from sleeve or standalone results.
- P02 does not authorize P03 or P04.
- P02 does not authorize local data inspection or IDM calculation.
- P02 must prefer native daily futures candles when a future data lane is authorized.
- P02 must not reconstruct daily bars from 1-minute data by default.
- P02 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- P02 must not select, drop, rescue, or reweight legs after seeing results.
- P02 must not treat historical performance as promotion evidence.
- A non-positive future P02 result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native identity for each of the six instruments.
- Whether any leg requires a documented source-native historical bridge.
- Exact local NinjaTrader symbol mapping for every instrument.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument.
- Daily bar synchronization rule across all six instruments.
- Exact roll calendar and roll timing for every instrument.
- Exact continuous-contract/back-adjustment construction for every instrument.
- Treatment of raw futures price versus adjusted futures price for every instrument.
- Current held-contract raw price source for sizing for every instrument.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion for every instrument.
- Variable risk estimate per instrument.
- Warm-up period and first usable date per instrument.
- Instrument weights lock.
- Bucket and sub-bucket structure lock.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Exact IDM 1.81 source quote/page verification before treating that number as locked authority.
- Pre-lock rule for any IDM calculation from correlations or realised aggregate risk.
- Exact contract-count rounding rule per leg.
- Portfolio aggregation convention for completed daily PnL.
- Portfolio cost aggregation rule.
- Exact cost source in `config/costs.json`.
- Fail-closed behavior for missing or invalid prices, rolls, multipliers, FX, risk estimates, costs, liquidity, capital, weights, buckets, IDM, synchronization, or sizing inputs.
- Evidence-window budget if a future diagnostic/backtest is requested.
- Exact synthetic conformance examples for later implementation testing.
- Whether any book numeric examples are sufficient for source-example conformance tests.

## Forbidden Work

This brief authorizes none of the following:

- Data export.
- Market-row parsing.
- NinjaTrader export or subscription work.
- NinjaTrader brokerage/account/credential/order-routing setup.
- Implementation.
- Unit tests.
- Synthetic tests.
- Diagnostics.
- Backtests.
- OOS, Lockbox, or Forward access.
- CFD adapter work.
- Old adapter import.
- Tuning.
- Deployment.
- Trading.
- Promotion.

## Hostile Audit Requirement

Before this P02 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0, S01, S02, S03, S04, and P01 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct complete-portfolio reconstruction interpretation.
- Correct separation from P03 and P04.
- No IDM recalculation or historical-result leakage.
- Correct instrument mappings and weights.
- Completeness of unresolved atoms.

## Next Gate

If this P02 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_S09_MULTIPLE_TREND_FOLLOWING_CANDIDATE_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No S09 work is authorized by this P02 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.

```

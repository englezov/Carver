# Carver NinjaTrader-Supported Pilot Static Policy Evidence Packet

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_EVIDENCE_PACKET_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Identify the exact static policy evidence needed before any tiny NinjaTrader historical-bar intake can be considered for the selected 16-row NinjaTrader-supported pilot universe:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

This packet is a source and policy evidence map only. It does not lock production readiness, does not ingest historical bars, does not export from NinjaTrader, and does not authorize market-row parsing, diagnostics, backtests, deployment, trading, or promotion.

## Inputs Inspected

Current Carver static artifacts:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_UNIVERSE_SHAPE_STATIC_READINESS_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_READINESS_EXECUTION_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_READINESS_STATUS_2026-05-30.csv
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv
docs/researchops/session_roll/CARVER_APPENDIX_C_SESSION_ROLL_COMPLETED_BAR_READINESS_STATUS_2026-05-29.csv
docs/researchops/risk_fx_cost_carry_leg/CARVER_APPENDIX_C_RISK_FX_COST_CARRY_LEG_READINESS_STATUS_2026-05-29.csv
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

Official static policy/specification source targets were identified from NinjaTrader and CME Group public documentation pages only. No market rows, historical exports, provider APIs, diagnostics, or backtests were accessed.

## Current Pilot Status

The current pilot static readiness execution preserves all 16 selected row IDs and records:

```text
STATIC_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 0
STATIC_READINESS_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
CONTRACT_IDENTITY_FAIL_CLOSED_NOT_LOCKED: 16
SESSION_ROLL_COMPLETED_BAR_FAIL_CLOSED_NOT_LOCKED: 16
RISK_FX_COST_CARRY_LEG_FAIL_CLOSED_NOT_LOCKED: 16
```

This packet does not change those counts. It identifies the static evidence needed for a later execution gate to resolve or continue fail-closing each row.

## Source-Native Lane

Lane classification:

```text
SOURCE_NATIVE_FUTURES
```

Rejected lanes:

```text
CFD_DIRECT
CFD_ADAPTER
```

NinjaTrader is treated only as the practical local source-native futures data source branch. CFD assumptions, broker-clock assumptions, old QuantLab pipeline state, and adapter shortcuts are not evidence.

## Pilot Row Preservation

| Row ID | Code | Description | Current final static readiness | Evidence action |
|---|---:|---|---|---|
| `APPENDIX_C_172_001` | `ZT` | 2-year US | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_172_003` | `ZF` | 5-year US | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_172_004` | `ZN` | 10-year US | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_174_006` | `MES` | S&P 500 micro | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_174_002` | `MNQ` | Nasdaq micro | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_174_004` | `M2K` | Russell 2000 micro | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_174_001` | `MYM` | Dow Jones industrial micro | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_182_002` | `QM` | WTI Crude mini | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_182_004` | `RB` | Gasoline | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_183_003` | `ZC` | Corn | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_183_010` | `ZS` | Soybeans | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_183_011` | `ZM` | Soybean Meal | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_183_012` | `ZL` | Soybean Oil | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_183_013` | `ZW` | Wheat | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_183_005` | `HE` | Lean Hogs | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |
| `APPENDIX_C_183_006` | `LE` | Live Cattle | `FAIL_CLOSED_NOT_READY` | Preserve row; collect static policy evidence. |

No row may be silently substituted, dropped, reweighted, promoted from candidate to executable, or treated as ready merely because a NinjaTrader code exists.

## NinjaTrader Static Policy Evidence Needed

The later static-readiness execution must bind the exact NinjaTrader platform policy evidence below before any historical-bar intake.

| Policy atom | Official static source target | Why needed | Current lock state |
|---|---|---|---|
| Trading-hours template meaning | `https://ninjatrader.com/support/helpguides/nt8/trading_hours.htm` and `https://ninjatrader.com/support/helpguides/nt8/using_the_trading_hours_window.htm` | Establish that templates define session start/end behavior and can include holidays. | `NEEDED_NOT_LOCKED` |
| Applied template fields | Local sanitized NinjaTrader static master extract plus a future sanitized Trading Hours template extract if available. | The current instrument extract records template names but not full sessions, EOD markers, timezone, or holidays. | `NEEDED_NOT_LOCKED` |
| Template timezone | `https://ninjatrader.com/support/helpGuides/nt8/tradinghours.htm` and local template extract. | Lock template timezone rather than assuming CT, ET, UTC, or local PC time. | `NEEDED_NOT_LOCKED` |
| Session EOD marker and trading-date boundary | `https://ninjatrader.com/support/helpguides/nt8/using_the_trading_hours_window.htm` and local template extract. | Needed to decide completed daily bar boundaries and trading-date assignment. | `NEEDED_NOT_LOCKED` |
| Daily-bar source semantics | `https://ninjatrader.com/support/helpguides/nt8/bar_types.htm` | NinjaTrader daily bars and higher are governed by provider-recorded data, and NinjaTrader historical servers use ETH definitions for the instrument. | `NEEDED_NOT_LOCKED` |
| End-of-bar timestamp convention | `https://ninjatrader.com/support/helpguides/nt8/how_bars_are_built.htm` and `https://ninjatrader.com/support/helpguides/nt8/exporting.htm` | Lock that exported bars use end-of-bar timestamps and UTC export timezone before any parser is allowed. | `NEEDED_NOT_LOCKED` |
| Data Series parameters | `https://ninjatrader.com/support/helpguides/nt8/working_with_price_data.htm` | Lock interval type, price type, end date, and Trading Hours setting for any future pilot request. | `NEEDED_NOT_LOCKED` |
| Historical export availability and shape | `https://ninjatrader.com/support/helpguides/nt8/exporting.htm` | Identify future export evidence without running it; export remains forbidden here. | `NEEDED_NOT_LOCKED` |
| Merge policy values | `https://ninjatrader.com/support/helpGuides/nt8/merge_policy.htm` and `https://ninjatrader.com/support/helpGuides/nt8/mergepolicy.htm` | Decide whether a future pilot requests explicit contract months, non-merged data, or back-adjusted continuous data. | `NEEDED_NOT_LOCKED` |
| Contract month rollover dates and offsets | `https://ninjatrader.com/ru/support/helpGuides/nt8/editing_instruments.htm` and local sanitized contract-month evidence if extracted later. | NinjaTrader contract months, rollover dates, and offsets are not in the current static master extract. | `NEEDED_NOT_LOCKED` |
| Roll operation behavior | `https://ninjatrader.com/support/helpguides/nt8/rolling_over_a_futures_contrac.htm` | Prevent confusing workspace rollover behavior with an audited research roll rule. | `NEEDED_NOT_LOCKED` |

## CME Static Policy Evidence Needed

Because the selected pilot is CME Group-heavy, official CME Group pages are the primary exchange-side policy source family.

| Policy atom | Official static source target | Why needed | Current lock state |
|---|---|---|---|
| Product contract specs | CME product pages listed in the row table below. | Confirm product identity, venue, currency, unit, tick, listed months, and product-family status. | `PARTIAL_STATIC_EVIDENCE_PRESENT_NOT_LOCKED` |
| CME product slate | `https://www.cmegroup.com/markets/products.html` | Independent product-code and specification locator for CME, CBOT, NYMEX, and COMEX products. | `NEEDED_NOT_LOCKED` |
| CME holiday and trading-hours calendar | `https://www.cmegroup.com/trading-hours.html` | Lock holiday and early-close policy by product family/trade date. | `NEEDED_NOT_LOCKED` |
| CME expiration calendar | `https://www.cmegroup.com/tools-information/calendars/expiration-calendar.html` | Lock first trade date, last trade date, settlement date, delivery date, and other contract-event dates when needed. | `NEEDED_NOT_LOCKED` |
| CME daily settlement overview | `https://www.cmegroup.com/market-data/daily-settlements.html` | Identify official settlement family before deciding whether a daily close should use settlement. | `NEEDED_NOT_LOCKED` |
| CME settlement column semantics and update times | `https://www.cmegroup.com/trading/about-settlements.html` | Distinguish exchange settlement values from provider-recorded daily OHLC and from market data feed validation. | `NEEDED_NOT_LOCKED` |
| CME settlement procedures by product family | CME daily settlement procedure links from the daily settlements page, plus product-family procedure PDFs where available. | Needed if the pilot uses official settlement close rather than NinjaTrader provider daily close. | `NEEDED_NOT_LOCKED` |

## Product-Specific Static Source Targets

The contract identity hardening update already identified official static product pages. A later lock gate must hash-bind or otherwise preserve the exact source snapshots before marking any row production-ready.

| Code | Product source target |
|---:|---|
| `ZT` | `https://www.cmegroup.com/markets/interest-rates/us-treasury/2-year-us-treasury-note.contractSpecs.html`; `https://www.cmegroup.com/content/dam/cmegroup/education/files/understanding-treasury-futures.pdf` |
| `ZF` | `https://www.cmegroup.com/markets/interest-rates/us-treasury/5-year-us-treasury-note.contractSpecs.html`; `https://www.cmegroup.com/content/dam/cmegroup/education/files/understanding-treasury-futures.pdf` |
| `ZN` | `https://www.cmegroup.com/markets/interest-rates/us-treasury/10-year-us-treasury-note.contractSpecs.html`; `https://www.cmegroup.com/content/dam/cmegroup/education/files/understanding-treasury-futures.pdf` |
| `MES` | `https://www.cmegroup.com/markets/equities/sp/micro-e-mini-sandp-500.contractSpecs.html`; `https://www.cmegroup.com/trading/equity-index/us-index/micro-e-mini-sandp-500_contract_specifications.html` |
| `MNQ` | `https://www.cmegroup.com/markets/equities/nasdaq/micro-e-mini-nasdaq-100.contractSpecs.html`; `https://www.cmegroup.com/trading/equity-index/files/cme-micro-e-mini-futures-fact-card.pdf` |
| `M2K` | `https://www.cmegroup.com/markets/equities/russell/micro-e-mini-russell-2000.contractSpecs.html`; `https://www.cmegroup.com/trading/equity-index/files/cme-micro-e-mini-futures-fact-card.pdf` |
| `MYM` | `https://www.cmegroup.com/markets/equities/dow-jones/micro-e-mini-dow.contractSpecs.html`; `https://www.cmegroup.com/trading/equity-index/files/cme-micro-e-mini-futures-fact-card.pdf` |
| `QM` | `https://www.cmegroup.com/markets/energy/crude-oil/e-mini-crude-oil.contractSpecs.html`; `https://www.cmegroup.com/trading/energy/files/micro-wti-crude-oil-futures-fact-card.pdf` |
| `RB` | `https://www.cmegroup.com/markets/energy/refined-products/rbob-gasoline.contractSpecs.html`; `https://www.cmegroup.com/pt/products/energy/rbob-harbor-gasoline-blendstock.html` |
| `ZC` | `https://www.cmegroup.com/markets/agriculture/grains/corn.contractSpecs.html`; `https://www.cmegroup.com/trading/agricultural/files/grain-and-oilseed-futures-options-fact-card.pdf` |
| `ZS` | `https://www.cmegroup.com/markets/agriculture/oilseeds/soybean.contractSpecs.html`; `https://www.cmegroup.com/education/lessons/soybeans-product-overview.html` |
| `ZM` | `https://www.cmegroup.com/markets/agriculture/oilseeds/soybean-meal.contractSpecs.html` |
| `ZL` | `https://www.cmegroup.com/markets/agriculture/oilseeds/soybean-oil.contractSpecs.html`; `https://www.cmegroup.com/pt/products/agricultural-commodities/soybean-oil.html` |
| `ZW` | `https://www.cmegroup.com/markets/agriculture/grains/wheat.contractSpecs.html`; `https://www.cmegroup.com/trading/agricultural/files/fact-card-wheat.pdf` |
| `HE` | `https://www.cmegroup.com/markets/agriculture/livestock/lean-hogs.contractSpecs.html` |
| `LE` | `https://www.cmegroup.com/markets/agriculture/livestock/live-cattle.contractSpecs.html`; `https://www.cmegroup.com/markets/agriculture/files/cattle-futures-and-options-fact-card.pdf` |

## Evidence Needed By Product Family

| Pilot family | Codes | NinjaTrader template currently observed | Static evidence still needed |
|---|---|---|---|
| CBOT Treasury note futures | `ZT`, `ZF`, `ZN` | `CBOT Interest Rate ETH` | Full template sessions, EOD marker, timezone, holidays, early closes, CME product trading hours, settlement-time policy, quarterly delivery cycle lock, roll rule, and back-adjustment policy. |
| CME/CBOT micro equity index futures | `MES`, `MNQ`, `M2K`, `MYM` | `CME US Index Futures ETH` | Full ETH template sessions, EOD marker, timezone, holidays, early closes, quarterly delivery cycle lock, roll rule, back-adjustment policy, and settlement-vs-provider-close decision. |
| NYMEX energy futures | `QM`, `RB` | `Nymex Metals - Energy ETH` | Full ETH template sessions, EOD marker, timezone, NYMEX holiday/early close policy, product-specific listed months, roll rule, back-adjustment policy, settlement-vs-provider-close decision, and physical-delivery/expiry calendar policy. |
| CBOT grains and oilseeds | `ZC`, `ZS`, `ZM`, `ZL`, `ZW` | `CBOT Agriculturals ETH` | Full template sessions, EOD marker, timezone, grain/oilseed holiday and early close policy, product-specific listed months, quote-unit lock, roll rule, back-adjustment policy, settlement-vs-provider-close decision, and missing/stale session policy. |
| CME livestock | `HE`, `LE` | `CME Commodities ETH` | Full template sessions, EOD marker, timezone, livestock holiday and early close policy, product-specific listed months, quote-unit lock, roll rule, back-adjustment policy, settlement-vs-provider-close decision, and missing/stale session policy. |

## Required Policy Decisions Before Any Bar Intake

The next execution gate must decide, with explicit evidence, all of the following:

1. Whether the first pilot uses explicit dated contract months only or any continuous/merged instrument form.
2. Whether merge policy is `DoNotMerge`, `MergeNonBackAdjusted`, `MergeBackAdjusted`, or explicitly blocked.
3. Whether roll dates and offsets come from NinjaTrader static contract-month metadata, CME expiration/last-trade calendars, a Carver source rule, or remain blocked.
4. Whether daily bars use NinjaTrader provider-recorded daily bars, official exchange settlement values where available, or no daily pilot until the close policy is lockable.
5. Whether exported timestamps must be UTC end-of-bar timestamps and how they are reconciled back to the exchange trading date.
6. Whether the session template must be `<Use Instrument Settings>` or an explicit named ETH template per row.
7. Whether holidays and early closes are sourced from NinjaTrader template holidays, CME Group holiday/trading-hours calendars, or both with a precedence rule.
8. Whether stale and missing bar policy rejects the row, rejects the date, permits a known exchange holiday, or permits a known no-session day.
9. Whether alignment across instruments occurs by exchange trading date, UTC timestamp, or a separately locked canonical completed-bar date.
10. Whether the pilot admits only price bars or also needs volume/open-interest fields.

If any decision remains unresolved, the affected row remains fail-closed.

## Risk, FX, Cost, And Carry-Leg Evidence Needed

All 16 selected pilot contracts are currently USD-denominated in the static contract identity evidence, but USD currency in a contract spec is not sufficient by itself to lock production FX, cost, or risk readiness.

| Atom | Evidence needed | Current lock state |
|---|---|---|
| Annual risk policy | Carver/source method and future price-history window policy after completed-bar evidence exists. Static policy alone cannot compute annual risk. | `BLOCKED_UNTIL_BAR_POLICY_AND_DATA_GATE` |
| Daily price risk policy | Carver/source method plus completed daily price series after an authorized intake. Static policy alone cannot compute daily price risk. | `BLOCKED_UNTIL_BAR_POLICY_AND_DATA_GATE` |
| FX source | Base-currency decision, account/capital currency, and source for non-USD conversion if later needed. USD contract currency does not remove the need to document the policy. | `NEEDED_NOT_LOCKED` |
| Commission and fees | Official NinjaTrader commission/fee schedule and operator-selected account plan, or a fail-closed zero-trading pilot that does not use cost eligibility. | `NEEDED_NOT_LOCKED` |
| Spread/slippage proxy | Source-native futures spread/slippage policy or explicit deferral; cannot be inferred from static specs. | `NEEDED_NOT_LOCKED` |
| Risk-adjusted cost | Carver/source formula plus locked costs, turnover, point value, FX, and price risk. | `BLOCKED_UPSTREAM` |
| Trend eligibility | Strategy Nine cost/turnover rule and locked risk-adjusted cost evidence. | `BLOCKED_UPSTREAM` |
| Carry eligibility | Strategy Ten carry-span cost eligibility and locked risk-adjusted cost evidence. | `BLOCKED_UPSTREAM` |
| Carry curve legs | Contract identity, listed months, expiry/calendar policy, held/comparison selection, raw-carry sign policy, fixed-month/seasonality/wrong-sign policy. | `NEEDED_NOT_LOCKED` |

The NinjaTrader futures commissions PDF at `https://ninjatrader.com/PDF/ninjatrader_futures_commissions.pdf` and the public pricing pages may be candidate fee evidence, but they do not by themselves lock the operator's account plan, exchange/data fees, spread, slippage, turnover, or risk-adjusted cost.

## Fail-Closed Rules

Before any historical-bar intake pilot, a row must remain fail-closed unless all of the following are true:

- the row's Appendix C identity and NinjaTrader code are preserved;
- contract identity is locked from static official source/provider evidence;
- the exact trading-hours template is locked with timezone, sessions, EOD marker, holidays, and early closes;
- the completed-bar timestamp and UTC/trading-date conversion policy is locked;
- the daily close policy is locked, including whether settlement is used;
- the roll rule and merge/back-adjustment policy are locked or explicitly not used;
- stale-bar, missing-bar, and alignment policy are locked;
- risk/FX/cost/carry-leg policy is either locked for the pilot purpose or explicitly declared out of scope for a price-intake-only pilot;
- no row is substituted, dropped, reweighted, or promoted because another instrument is more convenient.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_EVIDENCE_INTAKE_OR_EXECUTION_GATE
```

That gate should use this packet to create a machine-readable static policy ledger for the 16 selected rows. It may resolve or fail-close:

- contract identity final locks;
- trading-hours template sessions, EOD markers, timezone, holidays, and early closes;
- completed-bar timestamp and UTC export policy;
- daily close or settlement policy;
- explicit-contract versus merged-continuous policy;
- roll date and back-adjustment policy;
- stale/missing/alignment policy;
- risk/FX/cost/carry-leg policy classification for the chosen first pilot purpose.

Only after a later static policy ledger marks at least one row:

```text
STATIC_POLICY_READY_FOR_TINY_HISTORICAL_BAR_INTAKE
```

should a separate operator decision consider authorizing a tiny historical-bar intake pilot.

## Non-Authorization

This packet authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.

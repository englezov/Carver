# 04 Tests, Gates, and Audit History

Use this file to audit the synthetic tests and process gates for P01/P02. Tests are intended to verify wiring, fail-closed behavior, no ES-for-MES substitution, request-bound chart normalization, direct-daily primary intake, and minute-derived fallback only.

---

# FILE: docs\process\CARVER_NINJATRADER_TRADOVATE_WEB_CHART_API_GATE_2026-05-29.md

```text

# Carver NinjaTrader Tradovate Web Chart API Gate

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_TRADOVATE_WEB_CHART_API_GATE_SYNTHETIC_ONLY
```

## Purpose

Define a controlled Web Chart API intake path so Carver does not depend on manual NinjaTrader UI exports.

The NinjaTrader web app was observed issuing chart requests through the Tradovate-compatible market-data WebSocket API. This gate documents the observed/public chart shape and implements synthetic-only request/response normalization. It does not authorize real API calls.

## Observed Web-App Surface

Read-only browser inspection of the logged-in web app observed chart request logs shaped like:

```json
{
  "symbol": "3570919",
  "chartDescription": {
    "underlyingType": "MinuteBar",
    "elementSizeUnit": "UnderlyingUnits",
    "elementSize": 5,
    "withHistogram": false
  },
  "timeRange": {
    "asMuchAsElements": 300
  }
}
```

The public Tradovate API documents endpoint `md/getChart`, chart types `MinuteBar` and `DailyBar`, and chart payloads containing OHLC bars plus up/down volume fields.

The synthetic response envelope assumed by this gate is:

```json
{
  "request": {
    "endpoint": "md/getChart",
    "payload": {
      "symbol": "4470301",
      "chartDescription": {
        "underlyingType": "MinuteBar",
        "elementSizeUnit": "UnderlyingUnits",
        "elementSize": 1,
        "withHistogram": false
      },
      "timeRange": {
        "asMuchAsElements": 3
      }
    },
    "identity": {
      "contractCode": "ZN",
      "contractMonth": "06-26",
      "displaySymbol": "ZN JUN26",
      "providerSymbolId": "4470301"
    }
  },
  "ok": true,
  "body": {
    "items": [
      {
        "timestamp": 1780000000000,
        "open": 1,
        "high": 1,
        "low": 1,
        "close": 1,
        "volume": 1,
        "complete": true
      }
    ]
  }
}
```

The `request` binding must exactly match the locked request object before any bars are normalized. A quarantined chart response cannot be paired with a different provider symbol, display symbol, contract month, endpoint, or request payload.

Each symbol must be locked by contract identity, contract month, display symbol, and provider numeric symbol id before any request payload can be built. The current locked P01/P02 validation mapping is:

```text
ZN 06-26 ZN JUN26 -> 4470301
```

The observed `ES 06-26 ES JUN26 -> 3570919` id is non-portfolio archaeology only. It is not admitted by locked-provider validation and must not be used as a substitute for `MES`.

No other provider symbol id is admitted by this synthetic gate.

## Authorized Implementation Surface

Authorized code may include only:

- Synthetic request objects for `md/getChart`.
- Endpoint allow-listing for `md/getChart` and `md/cancelChart` only.
- Read-only chart response normalization from synthetic payloads.
- Minute and daily OHLCV bar validation.
- Guardrails rejecting order/trading/report/account endpoints, arbitrary symbols, non-source-native lanes, and bulk requests.
- A disabled probe descriptor documenting what a future one-symbol probe would need, without executing it.

## Explicit Non-Authorization

This gate authorizes no real API download, no WebSocket connection, no token/cookie extraction, no browser storage inspection, no order endpoint, no account endpoint, no report endpoint, no bulk download, no market diagnostic, no historical backtest, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.

## Future Probe Boundary

A future probe, if separately authorized, must be one explicit read-only `md/getChart` request for one visible source-native contract and a small element count. It must cancel its chart subscription immediately after receipt and save any raw response only under a Git-ignored quarantine path.

No such probe is authorized by this file.

```

---

# FILE: docs\process\CARVER_P01_P02_SOURCE_NATIVE_PORTFOLIO_CONFORMANCE_GATE_2026-05-29.md

```text

# Carver P01/P02 Source-Native Portfolio Conformance Gate

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_AND_SYNTHETIC_CODE_CARVER_P01_P02_PORTFOLIO_CONFORMANCE_GATE_NOT_BACKTEST_NOT_DATA_DOWNLOAD
```

## Purpose

Wire the first place where the Carver spine clicks together:

```text
locked source-native contract identity
-> quarantined normalized chart/minute bars
-> completed daily market bars
-> prevalidated annual risk and FX inputs
-> M1/M3 sizing
-> P01/P02 exact-portfolio conformance
```

This gate is still synthetic-only. It proves the shape of the intake and portfolio conformance path without executing a real NinjaTrader/Tradovate API call, reading live browser storage, downloading market history, running a diagnostic, or running a backtest.

## Implemented Surface

The code surface added by this gate is deliberately small:

- `daily_bars.py` derives a completed daily OHLCV bar from a full contiguous one-minute synthetic session.
- `daily_bars.py` also normalizes direct daily Web Chart bars as the primary intake path when the provider supplies completed daily candles.
- `web_chart_api.py` can read a JSON chart response only from a Git-ignored quarantine directory and normalize it through the existing synthetic chart validator. The response envelope must echo the exact locked request payload and provider identity before any bars are admitted. Normalized bars remain request-bound and cannot be replayed under a different request.
- `continuous.py` defines a continuous-contract rule set but refuses to build a continuous/back-adjusted series until session, roll, back-adjustment, and cost-source rules are locked separately.
- `portfolio_conformance.py` sizes P01/P02 from exact completed daily bars, prevalidated annual risk estimates, and aligned FX rates.
- `portfolio_conformance.py` defines exact provider mapping sets that must match the portfolio legs and the locked provider registry before a real-data route can be considered mapped.
- Provider-symbol mapping status is explicit and fail-closed. The only currently locked P01/P02 mapping is `ZN 06-26 -> 4470301`. The observed `ES 06-26 -> 3570919` id is retained only as non-portfolio archaeology and is not read by locked-provider validation. P01 uses `MES` and `ZN`; P02 uses `MES`, `ZN`, `ZF`, `QM`, `ZC`, and `MGC`. Therefore real P01/P02 Web Chart conformance remains blocked until exact book-contract provider IDs are locked.

## Required Next Data-Surface Locks

Before any real P01/P02 data pull or conformance run:

- Lock exact NinjaTrader/Tradovate provider IDs for `MES`, `ZN`, `ZF`, `QM`, `ZC`, and `MGC` contract months.
- Lock the daily-session convention for each instrument.
- Lock whether the first data intake uses direct daily bars or one-minute-to-daily derivation. Direct daily is primary; minute-derived fallback must carry a separate artifact explaining why direct daily is unavailable for that route.
- Lock roll and back-adjustment rules for continuous series use.
- Lock annual risk estimates and FX inputs as prevalidated upstream facts, not post-result tuned values.
- Pass the real-data conformance preflight before any future real-data sizing call.
- Keep any raw API response under quarantine and parse only expected JSON chart envelopes.

## Explicit Non-Authorization

This gate authorizes no real WebSocket call, no token/cookie/storage extraction, no NinjaTrader export, no `.ncd` decoding, no bulk download, no data diagnostic, no backtest, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.

## Test Posture

Synthetic tests cover:

- quarantined JSON chart response normalization;
- full-session one-minute-to-completed-daily derivation;
- rejection of missing, gapped, incomplete, or misaligned bars;
- fail-closed continuous/roll/back-adjustment placeholders;
- exact P01/P02 portfolio conformance from completed daily closes;
- unresolved provider mappings for P01/P02 instruments.

The test suite does not use real market data and does not claim strategy performance.

```

---

# FILE: docs\process\CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md

```text

# Carver P01/P02 Portfolio Completion Record

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P01_P02_PORTFOLIO_PACKAGE_COMPLETE_REAL_DATA_BLOCKED
```

## Purpose

Record the first complete source-native portfolio package boundary for Carver P01/P02.

This is not a backtest and not a data run. It is the lean gate that says how P01/P02 connect from source-native instruments through completed daily bars into portfolio sizing, and which facts still block real-data conformance.

## Completed Package

The package now contains:

- P01 exact portfolio definition: `MES` and `ZN`, 50/50 risk weights.
- P02 exact portfolio definition: `MES`, `ZN`, `ZF`, `QM`, `ZC`, `MGC`, weights 25 / 12.5 / 12.5 / 12.5 / 12.5 / 25.
- Direct daily bars as the preferred first intake path because NinjaTrader can provide daily candles.
- Direct daily Web Chart normalization is represented in code as a first-class path; minute-to-daily derivation remains fallback only and requires a direct-daily-blocked artifact before it can be locked.
- Minute-to-completed-daily derivation as a tested fallback only, requiring a full contiguous locked session.
- Quarantined JSON chart response normalization with exact request/provider binding.
- P01/P02 conformance orchestration from completed daily bars, prevalidated annual risk, and aligned FX inputs.
- A completion report object that fails closed until all real-data prerequisites are locked as artifacts, not as bare status flags.
- A named real-data conformance preflight that blocks future real-data sizing until the completion report is ready.
- Continuous/roll/back-adjustment placeholders that intentionally refuse to build a series until separate source rules are locked.

## Current Mapping Status

Locked for P01/P02 validation:

```text
ZN 06-26 ZN JUN26 -> 4470301
```

Observed archaeology only; not read by locked-provider validation and not a book-contract substitute for P01/P02:

```text
ES 06-26 ES JUN26 -> 3570919
```

Still unresolved for P01/P02:

```text
MES 06-26
ZF  06-26
QM  06-26
ZC  06-26
MGC 06-26
```

`ES` must not be used as a silent replacement for `MES`.

## Real-Data Blockers

Before any real P01/P02 conformance run:

- Lock exact provider IDs for `MES`, `ZN`, `ZF`, `QM`, `ZC`, and `MGC`.
- Lock the intake-route contract as a source artifact: direct daily primary, or minute-derived fallback with a separate direct-daily-blocked artifact.
- Lock session calendars/timezones as `SessionCalendarSpec` artifacts for the selected route.
- Lock roll and back-adjustment rules as `RollRuleSpec` and `BackAdjustmentSpec` artifacts for continuous futures use.
- Lock the annual risk input source and FX input source as prevalidated facts.
- Keep raw responses inside quarantine and require exact request/provider binding.

## Non-Authorization

This record authorizes no real WebSocket call, no token/cookie/storage extraction, no NinjaTrader export, no `.ncd` decoding, no bulk download, no data diagnostic, no backtest, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.

## Audit Note

After this package is locally stable, an external Opus audit is appropriate for a higher-level source-faithfulness check:

```text
Did the Carver P01/P02 portfolio package preserve the book's instrument set,
portfolio weights, completed-bar assumptions, source-native futures boundary,
and no-substitution/no-tuning/no-backtest discipline?
```

That audit should inspect the book, the module specs, the P01/P02 briefs, this completion record, and the synthetic code/tests. It should not run data or code unless separately authorized.

```

---

# FILE: tests\test_first_portfolio_spine_synthetic.py

```text

from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from math import inf, nan
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.first_spine import (  # noqa: E402
    p01_synthetic_conformance,
    p02_synthetic_conformance,
    s01_buy_and_hold_single_contract,
)
from carver.spine.m0 import (  # noqa: E402
    BackAdjustmentSpec,
    CompletedBar,
    ContractSpec,
    CostSourceSpec,
    LaneClass,
    CarverBlocked,
    RollRuleSpec,
    SessionCalendarSpec,
    SourceRuleStatus,
)
from carver.spine.m1 import RoundingPolicy, SizingInput, TimedValue, size_contracts  # noqa: E402
from carver.spine.m3 import PortfolioLeg, PortfolioSpec, p01_risk_parity, p02_all_weather, synthetic_market_inputs  # noqa: E402
from carver.spine.s03 import S03RiskConfig, SyntheticDailyPrice, estimate_s03_annual_risk  # noqa: E402


class FirstPortfolioSpineSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ts = datetime(2026, 5, 28, tzinfo=timezone.utc)
        self.bar = CompletedBar(self.ts)

    def base_sizing(self, *, capital: float = 1_000_000, risk: float = 0.20) -> SizingInput:
        return SizingInput(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            completed_bar=self.bar,
            capital=TimedValue(capital, self.ts),
            target_risk=TimedValue(0.20, self.ts),
            current_held_price=TimedValue(5000, self.ts),
            annual_risk_estimate=TimedValue(risk, self.ts),
            multiplier=5,
            fx_rate=TimedValue(1.0, self.ts),
            risk_estimate_prevalidated=True,
            rounding_policy=RoundingPolicy.TRUNCATE,
        )

    def test_s01_requires_source_native_completed_bar(self) -> None:
        self.assertEqual(
            s01_buy_and_hold_single_contract(LaneClass.SOURCE_NATIVE_FUTURES, self.bar),
            1,
        )
        with self.assertRaises(CarverBlocked):
            s01_buy_and_hold_single_contract(LaneClass.CFD_ADAPTER, self.bar)
        with self.assertRaises(CarverBlocked):
            s01_buy_and_hold_single_contract(
                LaneClass.SOURCE_NATIVE_FUTURES,
                CompletedBar(self.ts, is_complete=False),
            )
        with self.assertRaises(CarverBlocked):
            s01_buy_and_hold_single_contract(
                LaneClass.SOURCE_NATIVE_FUTURES,
                CompletedBar(datetime(2026, 5, 28)),
            )
        with self.assertRaises(CarverBlocked):
            s01_buy_and_hold_single_contract(
                LaneClass.SOURCE_NATIVE_FUTURES,
                CompletedBar(datetime(2026, 5, 28, 14, 30, tzinfo=timezone.utc)),
            )

    def test_m0_hardening_guards_source_rules_and_contract_identity(self) -> None:
        with self.assertRaises(CarverBlocked):
            RollRuleSpec("roll calendar").require_locked()
        with self.assertRaises(CarverBlocked):
            BackAdjustmentSpec("back adjustment").require_locked()
        with self.assertRaises(CarverBlocked):
            SessionCalendarSpec("session calendar", SourceRuleStatus.LOCKED).require_locked()
        with self.assertRaises(CarverBlocked):
            CostSourceSpec("costs", SourceRuleStatus.LOCKED, "tmp/costs.json").require_locked()

        SessionCalendarSpec("session calendar", SourceRuleStatus.LOCKED, "UTC").require_locked()
        CostSourceSpec("costs", SourceRuleStatus.LOCKED, "config/costs.json").require_locked()
        ContractSpec("MES", "S&P 500 micro future", "CME", "USD", 5).validate()
        with self.assertRaises(CarverBlocked):
            ContractSpec("MES", "S&P 500 micro future", "CME", "usd", 5).validate()
        with self.assertRaises(CarverBlocked):
            ContractSpec("MES", "S&P 500 micro future", "CME", "USD", 5, LaneClass.CFD_ADAPTER).validate()

    def test_m1_sizing_invariants(self) -> None:
        base = size_contracts(self.base_sizing())
        doubled_capital = size_contracts(self.base_sizing(capital=2_000_000))
        doubled_risk = size_contracts(self.base_sizing(risk=0.40))

        self.assertAlmostEqual(doubled_capital.unrounded_contracts, base.unrounded_contracts * 2)
        self.assertAlmostEqual(doubled_risk.unrounded_contracts, base.unrounded_contracts / 2)
        self.assertEqual(base.unrounded_contracts, 40.0)

    def test_m1_fails_closed_on_invalid_context(self) -> None:
        with self.assertRaises(CarverBlocked):
            size_contracts(
                SizingInput(
                    lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                    completed_bar=self.bar,
                    capital=TimedValue(1_000_000, self.ts),
                    target_risk=TimedValue(0.20, self.ts),
                    current_held_price=TimedValue(5000, self.ts),
                    annual_risk_estimate=TimedValue(0.20, self.ts),
                    multiplier=5,
                    fx_rate=TimedValue(1.0, self.ts),
                    risk_estimate_prevalidated=False,
                )
            )

        with self.assertRaises(CarverBlocked):
            size_contracts(
                SizingInput(
                    lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                    completed_bar=self.bar,
                    capital=TimedValue(1_000_000, self.ts),
                    target_risk=TimedValue(0.20, self.ts),
                    current_held_price=TimedValue(5000, datetime(2026, 5, 27, tzinfo=timezone.utc)),
                    annual_risk_estimate=TimedValue(0.20, self.ts),
                    multiplier=5,
                    fx_rate=TimedValue(1.0, self.ts),
                    risk_estimate_prevalidated=True,
                )
            )

    def test_m1_fails_closed_on_invalid_numbers(self) -> None:
        for bad in (0, -1, nan, inf, True, "bad"):
            with self.subTest(field="capital", value=bad):
                with self.assertRaises(CarverBlocked):
                    size_contracts(replace(self.base_sizing(), capital=TimedValue(bad, self.ts)))
            with self.subTest(field="multiplier", value=bad):
                with self.assertRaises(CarverBlocked):
                    size_contracts(replace(self.base_sizing(), multiplier=bad))

    def test_p01_weights_and_synthetic_sizing(self) -> None:
        p01 = p01_risk_parity(capital=1_000_000, target_risk=0.20, idm=1.0)
        p01.validate()
        self.assertEqual([leg.code for leg in p01.legs], ["MES", "ZN"])
        self.assertEqual([leg.weight for leg in p01.legs], [0.5, 0.5])

        market = synthetic_market_inputs(
            self.ts,
            {
                "MES": (5000, 0.20, 1.0),
                "ZN": (120, 0.10, 1.0),
            },
        )
        result = p01_synthetic_conformance(p01, self.bar, market)
        self.assertAlmostEqual(result["MES"].unrounded_contracts, 20.0)
        self.assertAlmostEqual(result["ZN"].unrounded_contracts, 8.333333333333334)
        self.assertEqual(result["MES"].rounded_contracts, 20)
        self.assertEqual(result["ZN"].rounded_contracts, 8)

        spoof = PortfolioSpec(
            portfolio_id="P01_RISK_PARITY_EXAMPLE",
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            capital=1_000_000,
            target_risk=0.20,
            idm=1.0,
            legs=(
                PortfolioLeg(ContractSpec("MES", "S&P 500 micro future", "CME", "USD", 5), 0.40),
                PortfolioLeg(ContractSpec("ZN", "US 10-year bond future", "CBOT", "USD", 1000), 0.60),
            ),
        )
        with self.assertRaises(CarverBlocked):
            p01_synthetic_conformance(spoof, self.bar, market)

        exchange_spoof = PortfolioSpec(
            portfolio_id="P01_RISK_PARITY_EXAMPLE",
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            capital=1_000_000,
            target_risk=0.20,
            idm=1.0,
            legs=(
                PortfolioLeg(ContractSpec("MES", "S&P 500 micro future", "CBOT", "USD", 5), 0.50),
                PortfolioLeg(ContractSpec("ZN", "US 10-year bond future", "CBOT", "USD", 1000), 0.50),
            ),
        )
        with self.assertRaises(CarverBlocked):
            p01_synthetic_conformance(exchange_spoof, self.bar, market)

        extra_market = dict(market)
        extra_market["EXTRA"] = market["MES"]
        with self.assertRaises(CarverBlocked):
            p01_synthetic_conformance(p01, self.bar, extra_market)

    def test_p02_weights_and_synthetic_sizing(self) -> None:
        p02 = p02_all_weather(capital=1_000_000, target_risk=0.20, idm=1.0)
        p02.validate()
        self.assertEqual(
            [leg.code for leg in p02.legs],
            ["MES", "ZN", "ZF", "QM", "ZC", "MGC"],
        )
        self.assertAlmostEqual(sum(leg.weight for leg in p02.legs), 1.0)
        self.assertEqual([leg.weight for leg in p02.legs], [0.25, 0.125, 0.125, 0.125, 0.125, 0.25])

        market = synthetic_market_inputs(
            self.ts,
            {
                "MES": (5000, 0.20, 1.0),
                "ZN": (120, 0.10, 1.0),
                "ZF": (110, 0.08, 1.0),
                "QM": (80, 0.30, 1.0),
                "ZC": (500, 0.25, 1.0),
                "MGC": (2000, 0.18, 1.0),
            },
        )
        result = p02_synthetic_conformance(p02, self.bar, market)
        self.assertEqual(set(result), {"MES", "ZN", "ZF", "QM", "ZC", "MGC"})
        self.assertGreater(result["MES"].unrounded_contracts, 0)
        self.assertGreater(result["MGC"].unrounded_contracts, 0)

    def test_m3_fails_closed_on_bad_weights(self) -> None:
        bad = PortfolioSpec(
            portfolio_id="BAD",
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            capital=1_000_000,
            target_risk=0.20,
            idm=1.0,
            legs=p01_risk_parity(1_000_000, 0.20, 1.0).legs[:1],
        )
        with self.assertRaises(CarverBlocked):
            bad.validate()

    def test_s03_synthetic_volatility_estimator_feeds_m1(self) -> None:
        timestamps = tuple(datetime(2026, 5, day, tzinfo=timezone.utc) for day in (25, 26, 27, 28))
        prices = (
            SyntheticDailyPrice(CompletedBar(timestamps[0]), 100.0),
            SyntheticDailyPrice(CompletedBar(timestamps[1]), 102.0),
            SyntheticDailyPrice(CompletedBar(timestamps[2]), 101.0),
            SyntheticDailyPrice(CompletedBar(timestamps[3]), 103.0),
        )
        estimate = estimate_s03_annual_risk(prices, TimedValue(0.18, timestamps[-1]))

        returns = (0.02, (101.0 / 102.0) - 1.0, (103.0 / 101.0) - 1.0)
        alpha = 2.0 / 33.0
        ewma_variance = returns[0] * returns[0]
        for daily_return in returns[1:]:
            ewma_variance = alpha * daily_return * daily_return + (1.0 - alpha) * ewma_variance
        expected_short = (ewma_variance * 256) ** 0.5
        expected_blended = 0.30 * 0.18 + 0.70 * expected_short

        self.assertEqual(estimate.observation_count, 4)
        self.assertAlmostEqual(estimate.short_run_annual_risk, expected_short)
        self.assertAlmostEqual(estimate.as_of.value, expected_blended)

        sizing = size_contracts(
            SizingInput(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                completed_bar=CompletedBar(timestamps[-1]),
                capital=TimedValue(1_000_000, timestamps[-1]),
                target_risk=TimedValue(0.20, timestamps[-1]),
                current_held_price=TimedValue(103.0, timestamps[-1]),
                annual_risk_estimate=estimate.as_of,
                multiplier=5,
                fx_rate=TimedValue(1.0, timestamps[-1]),
                risk_estimate_prevalidated=True,
                rounding_policy=RoundingPolicy.TRUNCATE,
            )
        )
        self.assertGreater(sizing.unrounded_contracts, 0)

        with self.assertRaises(CarverBlocked):
            estimate_s03_annual_risk(prices[:1], TimedValue(0.18, timestamps[0]))
        with self.assertRaises(CarverBlocked):
            estimate_s03_annual_risk(tuple(reversed(prices)), TimedValue(0.18, timestamps[0]))
        with self.assertRaises(CarverBlocked):
            estimate_s03_annual_risk(prices, TimedValue(0.18, timestamps[0]))
        with self.assertRaises(CarverBlocked):
            estimate_s03_annual_risk(prices, TimedValue(0.18, timestamps[-1]), S03RiskConfig(long_run_weight=0.2))
        with self.assertRaises(CarverBlocked):
            estimate_s03_annual_risk(prices, TimedValue(0.18, timestamps[-1]), S03RiskConfig(ewma_span=32.5))
        with self.assertRaises(CarverBlocked):
            estimate_s03_annual_risk(prices, TimedValue(0.18, timestamps[-1]), S03RiskConfig(annualization_days=inf))


if __name__ == "__main__":
    unittest.main()

```

---

# FILE: tests\test_minute_export_intake_synthetic.py

```text

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked  # noqa: E402
from carver.spine.m3 import mes_contract  # noqa: E402
from carver.spine.minute_export import (  # noqa: E402
    EXPECTED_MINUTE_EXPORT_HEADER,
    MinuteExportSpec,
    parse_minute_export_file,
    parse_minute_export_text,
)


class MinuteExportIntakeSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = MinuteExportSpec(mes_contract(), "06-26")

    def rows(self, *data_rows: str) -> str:
        return ",".join(EXPECTED_MINUTE_EXPORT_HEADER) + "\n" + "\n".join(data_rows) + "\n"

    def good_text(self) -> str:
        return self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120",
            "MES,06-26,Last,1 Minute,2026-05-28T13:31:00+00:00,5001,5003,5000,5002,95",
        )

    def test_parse_valid_synthetic_minute_export(self) -> None:
        bars = parse_minute_export_text(self.good_text(), self.spec)

        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0].instrument, "MES")
        self.assertEqual(bars[0].contract_month, "06-26")
        self.assertEqual(bars[0].close, 5001.0)
        self.assertEqual(bars[1].volume, 95.0)

    def test_parse_explicit_file_only_inside_quarantine(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "data" / "quarantine" / "ninjatrader" / "minute_exports"
            root.mkdir(parents=True)
            export_path = root / "MES_06-26_1Minute_Last_20260528.csv"
            export_path.write_text(self.good_text(), encoding="utf-8")

            bars = parse_minute_export_file(export_path, self.spec, root)
            self.assertEqual(len(bars), 2)

            outside_path = Path(temporary_directory) / "MES_06-26_1Minute_Last_20260528.csv"
            outside_path.write_text(self.good_text(), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                parse_minute_export_file(outside_path, self.spec, root)

            cache_path = root / "20260528.Last.ncd"
            cache_path.write_text(self.good_text(), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                parse_minute_export_file(cache_path, self.spec, root)

            with self.assertRaises(CarverBlocked):
                parse_minute_export_file(root / "missing.csv", self.spec, root)
            with self.assertRaises(CarverBlocked):
                parse_minute_export_file(export_path, self.spec, Path(temporary_directory) / "missing-root")

    def test_rejects_bad_header_and_empty_export(self) -> None:
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text("", self.spec)
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text("timestamp,open\n2026-05-28T13:30:00+00:00,5000\n", self.spec)
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(
                ",".join(EXPECTED_MINUTE_EXPORT_HEADER) + ",extra\n"
                "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120,x\n",
                self.spec,
            )
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(
                ",".join(EXPECTED_MINUTE_EXPORT_HEADER) + "\n"
                "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001\n",
                self.spec,
            )

    def test_rejects_wrong_contract_surface(self) -> None:
        wrong_instrument = self.rows(
            "ES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120"
        )
        wrong_month = self.rows(
            "MES,09-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120"
        )

        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(wrong_instrument, self.spec)
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(wrong_month, self.spec)
        with self.assertRaises(CarverBlocked):
            MinuteExportSpec(mes_contract(), "13-26").validate()
        with self.assertRaises(CarverBlocked):
            MinuteExportSpec(mes_contract(), "01-26").validate()

    def test_rejects_wrong_bar_type_and_timeframe(self) -> None:
        wrong_bar_type = self.rows(
            "MES,06-26,Bid,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120"
        )
        wrong_timeframe = self.rows(
            "MES,06-26,Last,5 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120"
        )

        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(wrong_bar_type, self.spec)
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(wrong_timeframe, self.spec)

    def test_rejects_incomplete_or_bad_timestamps(self) -> None:
        naive = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00,5000,5002,4999,5001,120"
        )
        second_aligned_bad = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:01+00:00,5000,5002,4999,5001,120"
        )
        unsorted = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:31:00+00:00,5001,5003,5000,5002,95",
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120",
        )
        duplicate = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120",
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5001,5003,5000,5002,95",
        )
        gap = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120",
            "MES,06-26,Last,1 Minute,2026-05-28T13:32:00+00:00,5001,5003,5000,5002,95",
        )
        out_of_session = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T20:00:00+00:00,5000,5002,4999,5001,120"
        )
        wrong_offset = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+01:00,5000,5002,4999,5001,120"
        )
        invalid_text = self.rows(
            "MES,06-26,Last,1 Minute,not-a-time,5000,5002,4999,5001,120"
        )

        for text in (naive, second_aligned_bad, unsorted, duplicate, gap, out_of_session, wrong_offset, invalid_text):
            with self.subTest(text=text):
                with self.assertRaises(CarverBlocked):
                    parse_minute_export_text(text, self.spec)

    def test_rejects_bad_numbers_and_ohlc_shape(self) -> None:
        missing_open = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,,5002,4999,5001,120"
        )
        negative_price = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,-1,5002,4999,5001,120"
        )
        bad_volume = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,-1"
        )
        zero_price = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,0,5002,4999,5001,120"
        )
        non_finite = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,NaN,5002,4999,5001,120"
        )
        bad_high = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5000,4999,5001,120"
        )
        bad_low = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,5001,5001,120"
        )

        for text in (missing_open, negative_price, bad_volume, zero_price, non_finite, bad_high, bad_low):
            with self.subTest(text=text):
                with self.assertRaises(CarverBlocked):
                    parse_minute_export_text(text, self.spec)


if __name__ == "__main__":
    unittest.main()

```

---

# FILE: tests\test_web_chart_api_synthetic.py

```text

from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import ContractSpec, LaneClass, CarverBlocked  # noqa: E402
from carver.spine.web_chart_api import (  # noqa: E402
    ChartBarType,
    LockedWebChartSymbol,
    WebChartProbePlan,
    WebChartRequest,
    WebChartSymbol,
    assert_safe_web_chart_endpoint,
    normalize_web_chart_response,
    web_chart_response_request_binding,
)


class WebChartApiSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.zn_contract = ContractSpec("ZN", "US 10-year bond future", "CBOT", "USD", 1000)
        self.locked_symbol = LockedWebChartSymbol(self.zn_contract, "06-26", "4470301", "ZN JUN26")
        self.symbol = WebChartSymbol(self.locked_symbol, "4470301", "ZN JUN26")
        self.request = WebChartRequest(
            symbol=self.symbol,
            bar_type=ChartBarType.MINUTE,
            element_size=1,
            element_count=2,
        )

    def epoch_ms(self, year: int, month: int, day: int, hour: int, minute: int) -> int:
        return int(datetime(year, month, day, hour, minute, tzinfo=timezone.utc).timestamp() * 1000)

    def payload(self) -> dict:
        return {
            "request": web_chart_response_request_binding(self.request),
            "ok": True,
            "body": {
                "historicalId": 11,
                "realtimeId": 12,
                "items": [
                    {
                        "timestamp": self.epoch_ms(2026, 5, 28, 13, 30),
                        "open": 5000.0,
                        "high": 5002.0,
                        "low": 4999.0,
                        "close": 5001.0,
                        "upVolume": 70,
                        "downVolume": 50,
                        "complete": True,
                    },
                    {
                        "timestamp": self.epoch_ms(2026, 5, 28, 13, 31),
                        "open": 5001.0,
                        "high": 5003.0,
                        "low": 5000.0,
                        "close": 5002.0,
                        "volume": 95,
                        "complete": True,
                    },
                ],
            },
        }

    def test_builds_allowlisted_get_chart_payload(self) -> None:
        request_payload = self.request.payload()

        self.assertEqual(request_payload["symbol"], "4470301")
        self.assertEqual(request_payload["chartDescription"]["underlyingType"], "MinuteBar")
        self.assertEqual(request_payload["chartDescription"]["elementSize"], 1)
        self.assertEqual(request_payload["timeRange"]["asMuchAsElements"], 2)
        assert_safe_web_chart_endpoint("md/getChart")
        assert_safe_web_chart_endpoint("md/cancelChart")

    def test_normalizes_synthetic_web_chart_response(self) -> None:
        bars = normalize_web_chart_response(self.payload(), self.request)

        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0].timestamp, datetime(2026, 5, 28, 13, 30, tzinfo=timezone.utc))
        self.assertEqual(bars[0].volume, 120.0)
        self.assertEqual(bars[1].close, 5002.0)

    def test_rejects_trading_or_non_chart_endpoints(self) -> None:
        for endpoint in ("order/placeorder", "order/cancelorder", "account/list", "reports/requestreport"):
            with self.subTest(endpoint=endpoint):
                with self.assertRaises(CarverBlocked):
                    assert_safe_web_chart_endpoint(endpoint)
                with self.assertRaises(CarverBlocked):
                    replace(self.request, endpoint=endpoint).validate()

    def test_rejects_arbitrary_symbols_and_bulk_requests(self) -> None:
        with self.assertRaises(CarverBlocked):
            LockedWebChartSymbol(self.zn_contract, "06-26", "ZN JUN26", "ZN JUN26").validate()
        with self.assertRaises(CarverBlocked):
            WebChartSymbol(self.locked_symbol, "9999999", "ZN JUN26").validate()
        with self.assertRaises(CarverBlocked):
            WebChartSymbol(self.locked_symbol, "4470301", "MES JUN26").validate()
        with self.assertRaises(CarverBlocked):
            WebChartSymbol(self.locked_symbol, "4470301", "ZN JUN26", LaneClass.CFD_ADAPTER).validate()
        with self.assertRaises(CarverBlocked):
            LockedWebChartSymbol(self.zn_contract, "06-26", "9999999", "ZN JUN26").validate()
        with self.assertRaises(CarverBlocked):
            LockedWebChartSymbol(ContractSpec("ES", "E-mini S&P 500 future", "CME", "USD", 50), "06-26", "3570919", "ES JUN26").validate()
        with self.assertRaises(CarverBlocked):
            replace(self.request, element_count=501).validate()
        with self.assertRaises(CarverBlocked):
            replace(self.request, with_histogram=True).validate()
        with self.assertRaises(CarverBlocked):
            replace(self.request, element_size_unit="Volume").validate()
        with self.assertRaises(CarverBlocked):
            replace(self.request, bar_type="MinuteBar").validate()

    def test_rejects_bad_response_shape(self) -> None:
        bad_payloads = (
            {"request": web_chart_response_request_binding(self.request), "ok": False, "body": {"items": []}},
            {"request": web_chart_response_request_binding(self.request), "ok": True},
            {"request": web_chart_response_request_binding(self.request), "ok": True, "body": {"items": []}},
            {
                "request": web_chart_response_request_binding(self.request),
                "ok": True,
                "body": {"items": [*self.payload()["body"]["items"], *self.payload()["body"]["items"]]},
            },
            {"ok": True, "body": {"items": self.payload()["body"]["items"]}},
            {**self.payload(), "request": {**web_chart_response_request_binding(self.request), "endpoint": "md/getChart2"}},
        )
        for payload in bad_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(CarverBlocked):
                    normalize_web_chart_response(payload, self.request)

    def test_rejects_bad_bars(self) -> None:
        base_item = self.payload()["body"]["items"][0]
        bad_items = (
            {**base_item, "timestamp": "bad"},
            {**base_item, "timestamp": self.epoch_ms(2026, 5, 28, 13, 30) + 1},
            {**base_item, "open": 0},
            {**base_item, "high": 4998},
            {**base_item, "low": 5002},
            {**base_item, "complete": False},
            {key: value for key, value in base_item.items() if key != "complete"},
            {key: value for key, value in base_item.items() if key not in {"volume", "upVolume", "downVolume"}},
        )
        for item in bad_items:
            with self.subTest(item=item):
                with self.assertRaises(CarverBlocked):
                    one_bar_request = replace(self.request, element_count=1)
                    normalize_web_chart_response(
                        {"request": web_chart_response_request_binding(one_bar_request), "ok": True, "body": {"items": [item]}},
                        one_bar_request,
                    )

    def test_rejects_unordered_and_duplicate_timestamps(self) -> None:
        item_a, item_b = self.payload()["body"]["items"]
        duplicate = {"request": web_chart_response_request_binding(self.request), "ok": True, "body": {"items": [item_a, item_a]}}
        unordered = {"request": web_chart_response_request_binding(self.request), "ok": True, "body": {"items": [item_b, item_a]}}
        for payload in (duplicate, unordered):
            with self.subTest(payload=payload):
                with self.assertRaises(CarverBlocked):
                    normalize_web_chart_response(payload, self.request)

    def test_daily_request_requires_daily_alignment_and_size_one(self) -> None:
        daily_request = WebChartRequest(
            symbol=self.symbol,
            bar_type=ChartBarType.DAILY,
            element_size=1,
            element_count=1,
        )
        daily_payload = {
            "request": web_chart_response_request_binding(daily_request),
            "ok": True,
            "body": {
                "items": [
                    {
                        "timestamp": self.epoch_ms(2026, 5, 28, 0, 0),
                        "open": 5000,
                        "high": 5010,
                        "low": 4990,
                        "close": 5005,
                        "volume": 1000,
                        "complete": True,
                    }
                ]
            },
        }
        self.assertEqual(len(normalize_web_chart_response(daily_payload, daily_request)), 1)
        with self.assertRaises(CarverBlocked):
            replace(daily_request, element_size=5).validate()
        bad_daily = {
            "request": web_chart_response_request_binding(daily_request),
            "ok": True,
            "body": {"items": [{**daily_payload["body"]["items"][0], "timestamp": self.epoch_ms(2026, 5, 28, 13, 30)}]},
        }
        with self.assertRaises(CarverBlocked):
            normalize_web_chart_response(bad_daily, daily_request)

    def test_real_probe_is_disabled_until_explicitly_authorized(self) -> None:
        plan = WebChartProbePlan(self.request)
        with self.assertRaises(CarverBlocked):
            plan.require_authorized()
        WebChartProbePlan(self.request, execution_authorized=True).require_authorized()


if __name__ == "__main__":
    unittest.main()

```

---

# FILE: tests\test_daily_portfolio_conformance_synthetic.py

```text

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, time, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.continuous import (  # noqa: E402
    ContinuousContractRuleSet,
    ContinuousSeriesRequest,
    build_continuous_back_adjusted_series,
)
from carver.spine.daily_bars import (  # noqa: E402
    CompletedDailyMarketBar,
    DailyDerivationSession,
    derive_completed_daily_from_bound_web_chart,
    derive_completed_daily_from_minute_export,
    derive_completed_daily_from_web_chart,
    normalize_direct_daily_bound_web_chart,
    normalize_direct_daily_web_chart_bar,
)
from carver.spine.m0 import (  # noqa: E402
    BackAdjustmentSpec,
    CompletedBar,
    CostSourceSpec,
    RollRuleSpec,
    SessionCalendarSpec,
    SourceRuleStatus,
    CarverBlocked,
)
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m3 import (  # noqa: E402
    mes_contract,
    mgc_contract,
    p01_risk_parity,
    p02_all_weather,
    qm_contract,
    zc_contract,
    zf_contract,
    zn_contract,
)
from carver.spine.minute_export import EXPECTED_MINUTE_EXPORT_HEADER, MinuteExportSpec, parse_minute_export_text  # noqa: E402
from carver.spine.portfolio_conformance import (  # noqa: E402
    LockedPortfolioProviderMapping,
    PortfolioProviderMappingSet,
    ProviderMappingStatus,
    portfolio_conformance_from_daily_bars,
    portfolio_web_chart_mapping_status,
    require_locked_provider_mapping_set,
    require_locked_portfolio_web_chart_mapping,
)
from carver.spine.web_chart_api import (  # noqa: E402
    BoundWebChartResponse,
    ChartBarType,
    LockedWebChartSymbol,
    LOCKED_WEB_CHART_PROVIDER_SYMBOLS,
    WebChartRequest,
    WebChartSymbol,
    normalize_bound_web_chart_response,
    normalize_bound_web_chart_response_file,
    normalize_web_chart_response,
    normalize_web_chart_response_file,
    web_chart_response_request_binding,
)


class DailyPortfolioConformanceSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.session = DailyDerivationSession(time(13, 30), time(13, 33))
        self.daily_ts = datetime(2026, 5, 28, tzinfo=timezone.utc)

    def epoch_ms(self, hour: int, minute: int) -> int:
        return int(datetime(2026, 5, 28, hour, minute, tzinfo=timezone.utc).timestamp() * 1000)

    def web_request(self) -> WebChartRequest:
        locked = LockedWebChartSymbol(zn_contract(), "06-26", "4470301", "ZN JUN26")
        symbol = WebChartSymbol(locked, "4470301", "ZN JUN26")
        return WebChartRequest(symbol, ChartBarType.MINUTE, element_size=1, element_count=3)

    def daily_web_request(self) -> WebChartRequest:
        locked = LockedWebChartSymbol(zn_contract(), "06-26", "4470301", "ZN JUN26")
        symbol = WebChartSymbol(locked, "4470301", "ZN JUN26")
        return WebChartRequest(symbol, ChartBarType.DAILY, element_size=1, element_count=1)

    def zn_minute_web_request(self) -> WebChartRequest:
        return replace(self.daily_web_request(), bar_type=ChartBarType.MINUTE, element_count=3)

    def web_payload(self, request: WebChartRequest) -> dict:
        return {
            "request": web_chart_response_request_binding(request),
            "ok": True,
            "body": {
                "items": [
                    {
                        "timestamp": self.epoch_ms(13, 30),
                        "open": 5000,
                        "high": 5002,
                        "low": 4999,
                        "close": 5001,
                        "volume": 10,
                        "complete": True,
                    },
                    {
                        "timestamp": self.epoch_ms(13, 31),
                        "open": 5001,
                        "high": 5004,
                        "low": 5000,
                        "close": 5003,
                        "volume": 20,
                        "complete": True,
                    },
                    {
                        "timestamp": self.epoch_ms(13, 32),
                        "open": 5003,
                        "high": 5005,
                        "low": 5002,
                        "close": 5004,
                        "volume": 30,
                        "complete": True,
                    },
                ]
            },
        }

    def test_quarantined_web_chart_json_normalizes_before_daily_derivation(self) -> None:
        request = self.web_request()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "data" / "quarantine" / "ninjatrader" / "web_chart"
            root.mkdir(parents=True)
            response_path = root / "ZN_06-26_getChart_20260528.json"
            response_path.write_text(json.dumps(self.web_payload(request)), encoding="utf-8")

            response = normalize_bound_web_chart_response_file(response_path, request, root)
            daily = derive_completed_daily_from_bound_web_chart(response, self.session)

            self.assertEqual(daily.code, "ZN")
            self.assertEqual(daily.timestamp, self.daily_ts)
            self.assertEqual(daily.open, 5000)
            self.assertEqual(daily.high, 5005)
            self.assertEqual(daily.low, 4999)
            self.assertEqual(daily.close, 5004)
            self.assertEqual(daily.volume, 60)

            outside_path = Path(temporary_directory) / "ZN_06-26_getChart_20260528.json"
            outside_path.write_text(json.dumps(self.web_payload(request)), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                normalize_web_chart_response_file(outside_path, request, root)
            cache_path = root / "ZN_06-26_getChart_20260528.ncd"
            cache_path.write_text(json.dumps(self.web_payload(request)), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                normalize_web_chart_response_file(cache_path, request, root)

    def test_minute_export_derives_completed_daily_bar_only_for_full_session(self) -> None:
        spec = MinuteExportSpec(mes_contract(), "06-26", session_start=time(13, 30), session_end=time(13, 33))
        text = (
            ",".join(EXPECTED_MINUTE_EXPORT_HEADER)
            + "\n"
            + "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,10\n"
            + "MES,06-26,Last,1 Minute,2026-05-28T13:31:00+00:00,5001,5004,5000,5003,20\n"
            + "MES,06-26,Last,1 Minute,2026-05-28T13:32:00+00:00,5003,5005,5002,5004,30\n"
        )
        bars = parse_minute_export_text(text, spec)
        daily = derive_completed_daily_from_minute_export(bars, spec)

        self.assertEqual(daily.code, "MES")
        self.assertEqual(daily.timestamp, self.daily_ts)
        self.assertEqual(daily.close, 5004)
        with self.assertRaises(CarverBlocked):
            derive_completed_daily_from_minute_export(bars[:-1], spec)

    def test_direct_daily_web_chart_bar_normalizes_without_minute_derivation(self) -> None:
        request = self.daily_web_request()
        payload = {
            "request": web_chart_response_request_binding(request),
            "ok": True,
            "body": {
                "items": [
                    {
                        "timestamp": int(self.daily_ts.timestamp() * 1000),
                        "open": 119.0,
                        "high": 121.0,
                        "low": 118.0,
                        "close": 120.0,
                        "volume": 1000,
                        "complete": True,
                    }
                ]
            },
        }
        response = normalize_bound_web_chart_response(payload, request)
        daily = normalize_direct_daily_bound_web_chart(response)

        self.assertEqual(daily.code, "ZN")
        self.assertEqual(daily.contract, zn_contract())
        self.assertEqual(daily.timestamp, self.daily_ts)
        self.assertEqual(daily.close, 120.0)
        with self.assertRaises(CarverBlocked):
            normalize_direct_daily_web_chart_bar(response.bars[0], request)
        with self.assertRaises(CarverBlocked):
            normalize_direct_daily_bound_web_chart(
                normalize_bound_web_chart_response(payload, replace(request, bar_type=ChartBarType.MINUTE))
            )

    def test_direct_daily_bound_web_chart_rejects_cross_request_replay(self) -> None:
        request = self.daily_web_request()
        payload = {
            "request": web_chart_response_request_binding(request),
            "ok": True,
            "body": {
                "items": [
                    {
                        "timestamp": int(self.daily_ts.timestamp() * 1000),
                        "open": 119.0,
                        "high": 121.0,
                        "low": 118.0,
                        "close": 120.0,
                        "volume": 1000,
                        "complete": True,
                    }
                ]
            },
        }
        response = normalize_bound_web_chart_response(payload, request)
        spoofed_response = BoundWebChartResponse(replace(request, bar_type=ChartBarType.MINUTE, element_count=1), response.bars)

        with self.assertRaises(CarverBlocked):
            normalize_direct_daily_bound_web_chart(spoofed_response)

    def test_minute_bound_web_chart_daily_derivation_rejects_cross_request_replay(self) -> None:
        request = self.web_request()
        response = normalize_bound_web_chart_response(self.web_payload(request), request)
        spoofed_response = BoundWebChartResponse(self.daily_web_request(), response.bars)

        with self.assertRaises(CarverBlocked):
            derive_completed_daily_from_bound_web_chart(spoofed_response, self.session)

    def test_daily_derivation_rejects_gaps_wrong_alignment_and_incomplete_web_bars(self) -> None:
        request = self.web_request()
        response = normalize_bound_web_chart_response(self.web_payload(request), request)
        with self.assertRaises(CarverBlocked):
            derive_completed_daily_from_bound_web_chart(response, DailyDerivationSession(time(13, 31), time(13, 34)))

        bad_payload = self.web_payload(request)
        bad_payload["body"]["items"][1]["timestamp"] = self.epoch_ms(13, 32)
        with self.assertRaises(CarverBlocked):
            normalize_web_chart_response(bad_payload, request)

        incomplete_payload = self.web_payload(request)
        incomplete_payload["body"]["items"][0]["complete"] = False
        with self.assertRaises(CarverBlocked):
            normalize_web_chart_response(incomplete_payload, request)

    def daily_bar(self, contract, close: float) -> CompletedDailyMarketBar:
        return CompletedDailyMarketBar(
            completed_bar=CompletedBar(self.daily_ts),
            contract=contract,
            contract_month="06-26",
            open=close - 1,
            high=close + 1,
            low=close - 2,
            close=close,
            volume=100,
        )

    def test_p01_and_p02_conformance_use_completed_daily_closes(self) -> None:
        p01 = p01_risk_parity(capital=1_000_000, target_risk=0.20, idm=1.0)
        p01_bars = {
            "MES": self.daily_bar(mes_contract(), 5000),
            "ZN": self.daily_bar(zn_contract(), 120),
        }
        p01_result = portfolio_conformance_from_daily_bars(
            p01,
            p01_bars,
            {"MES": TimedValue(0.20, self.daily_ts), "ZN": TimedValue(0.10, self.daily_ts)},
            {"MES": TimedValue(1.0, self.daily_ts), "ZN": TimedValue(1.0, self.daily_ts)},
        )
        self.assertAlmostEqual(p01_result["MES"].unrounded_contracts, 20.0)
        self.assertAlmostEqual(p01_result["ZN"].unrounded_contracts, 8.333333333333334)

        p02 = p02_all_weather(capital=1_000_000, target_risk=0.20, idm=1.0)
        p02_bars = {
            "MES": self.daily_bar(mes_contract(), 5000),
            "ZN": self.daily_bar(zn_contract(), 120),
            "ZF": self.daily_bar(zf_contract(), 110),
            "QM": self.daily_bar(qm_contract(), 80),
            "ZC": self.daily_bar(zc_contract(), 500),
            "MGC": self.daily_bar(mgc_contract(), 2000),
        }
        result = portfolio_conformance_from_daily_bars(
            p02,
            p02_bars,
            {code: TimedValue(risk, self.daily_ts) for code, risk in {
                "MES": 0.20,
                "ZN": 0.10,
                "ZF": 0.08,
                "QM": 0.30,
                "ZC": 0.25,
                "MGC": 0.18,
            }.items()},
            {code: TimedValue(1.0, self.daily_ts) for code in p02_bars},
        )
        self.assertEqual(set(result), {"MES", "ZN", "ZF", "QM", "ZC", "MGC"})

        with self.assertRaises(CarverBlocked):
            portfolio_conformance_from_daily_bars(p01, {"MES": p01_bars["MES"]}, {}, {})
        with self.assertRaises(CarverBlocked):
            portfolio_conformance_from_daily_bars(
                p01,
                p01_bars,
                {"MES": TimedValue(0.20, self.daily_ts), "ZN": TimedValue(0.10, datetime(2026, 5, 27, tzinfo=timezone.utc))},
                {"MES": TimedValue(1.0, self.daily_ts), "ZN": TimedValue(1.0, self.daily_ts)},
            )

    def test_p01_p02_web_chart_mapping_status_fails_closed_until_exact_contracts_are_locked(self) -> None:
        p01_rows = portfolio_web_chart_mapping_status(p01_risk_parity(1_000_000, 0.20, 1.0), {"MES": "06-26", "ZN": "06-26"})
        self.assertEqual([(row.contract_code, row.status) for row in p01_rows], [("MES", ProviderMappingStatus.UNRESOLVED), ("ZN", ProviderMappingStatus.LOCKED)])
        with self.assertRaises(CarverBlocked):
            require_locked_portfolio_web_chart_mapping(p01_rows)

        p02 = p02_all_weather(1_000_000, 0.20, 1.0)
        p02_rows = portfolio_web_chart_mapping_status(
            p02,
            {"MES": "06-26", "ZN": "06-26", "ZF": "06-26", "QM": "06-26", "ZC": "06-26", "MGC": "06-26"},
        )
        self.assertEqual([row.contract_code for row in p02_rows], ["MES", "ZN", "ZF", "QM", "ZC", "MGC"])
        self.assertEqual(sum(row.status is ProviderMappingStatus.LOCKED for row in p02_rows), 1)

    def test_locked_web_chart_registry_contains_only_p01_p02_book_legs(self) -> None:
        book_leg_codes = {"MES", "ZN", "ZF", "QM", "ZC", "MGC"}
        self.assertEqual(set(LOCKED_WEB_CHART_PROVIDER_SYMBOLS), {("ZN", "06-26", "ZN JUN26")})
        for contract_code, contract_month, display_symbol in LOCKED_WEB_CHART_PROVIDER_SYMBOLS:
            with self.subTest(contract_code=contract_code):
                self.assertIn(contract_code, book_leg_codes)
                self.assertEqual(display_symbol, f"{contract_code} JUN26")
                self.assertEqual(contract_month, "06-26")

    def test_locked_provider_mapping_set_requires_exact_portfolio_legs(self) -> None:
        zn_mapping = LockedPortfolioProviderMapping(zn_contract(), "06-26", "ZN JUN26", "4470301")
        p01 = p01_risk_parity(1_000_000, 0.20, 1.0)

        with self.assertRaises(CarverBlocked):
            require_locked_provider_mapping_set(PortfolioProviderMappingSet(p01, (zn_mapping,)))
        with self.assertRaises(CarverBlocked):
            LockedPortfolioProviderMapping(mes_contract(), "06-26", "ES JUN26", "3570919").validate()
        with self.assertRaises(CarverBlocked):
            LockedPortfolioProviderMapping(mes_contract(), "06-26", "MES JUN26", "3570919").validate()
        with self.assertRaises(CarverBlocked):
            LockedPortfolioProviderMapping(zn_contract(), "06-26", "ZN JUN26", "999999").validate()

        zn_only = PortfolioProviderMappingSet(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            (
                LockedPortfolioProviderMapping(mes_contract(), "06-26", "MES JUN26", "3570919"),
                zn_mapping,
            ),
        )
        with self.assertRaises(CarverBlocked):
            zn_only.validate()

    def test_continuous_roll_and_back_adjustment_gate_fails_closed(self) -> None:
        unresolved_rules = ContinuousContractRuleSet(
            session_calendar=SessionCalendarSpec("session calendar"),
            roll_rule=RollRuleSpec("roll rule"),
            back_adjustment=BackAdjustmentSpec("back adjustment"),
            cost_source=CostSourceSpec("costs"),
        )
        request = ContinuousSeriesRequest(unresolved_rules, (self.daily_bar(mes_contract(), 5000),))
        with self.assertRaises(CarverBlocked):
            build_continuous_back_adjusted_series(request)

        locked_rules = ContinuousContractRuleSet(
            session_calendar=SessionCalendarSpec("session calendar", SourceRuleStatus.LOCKED, "UTC"),
            roll_rule=RollRuleSpec("roll rule", SourceRuleStatus.LOCKED),
            back_adjustment=BackAdjustmentSpec("back adjustment", SourceRuleStatus.LOCKED),
            cost_source=CostSourceSpec("costs", SourceRuleStatus.LOCKED, "config/costs.json"),
        )
        with self.assertRaises(CarverBlocked):
            build_continuous_back_adjusted_series(ContinuousSeriesRequest(locked_rules, (self.daily_bar(mes_contract(), 5000),)))


if __name__ == "__main__":
    unittest.main()

```

---

# FILE: tests\test_portfolio_completion_gate_synthetic.py

```text

from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import BackAdjustmentSpec, CarverBlocked, RollRuleSpec, SessionCalendarSpec, SourceRuleStatus  # noqa: E402
from carver.spine.m3 import p01_risk_parity, p02_all_weather  # noqa: E402
from carver.spine.portfolio_completion import (  # noqa: E402
    PortfolioCompletionStatus,
    IntakeRouteContract,
    PortfolioIntakeMode,
    RiskFxInputContract,
    SourceArtifactRef,
    build_portfolio_completion_report,
    require_real_data_conformance_preflight,
)
from carver.spine.portfolio_conformance import LockedPortfolioProviderMapping, PortfolioProviderMappingSet
from carver.spine.portfolio_conformance import ProviderMappingStatus  # noqa: E402


class PortfolioCompletionGateSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.as_of = datetime(2026, 5, 28, tzinfo=timezone.utc)
        self.locked_risk_fx = RiskFxInputContract(
            as_of=self.as_of,
            annual_risk_status=SourceRuleStatus.LOCKED,
            fx_status=SourceRuleStatus.LOCKED,
            annual_risk_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            fx_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
        )

    def test_p01_completion_report_blocks_real_data_until_exact_inputs_are_locked(self) -> None:
        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            self.locked_risk_fx,
            intake_contract=IntakeRouteContract(PortfolioIntakeMode.DIRECT_DAILY_PRIMARY),
        )

        self.assertEqual(report.status, PortfolioCompletionStatus.SYNTHETIC_READY_REAL_DATA_BLOCKED)
        self.assertEqual(report.intake_mode, PortfolioIntakeMode.DIRECT_DAILY_PRIMARY)
        self.assertEqual([(row.contract_code, row.status) for row in report.mapping_rows], [("MES", ProviderMappingStatus.UNRESOLVED), ("ZN", ProviderMappingStatus.LOCKED)])
        self.assertIn("provider mapping unresolved for MES 06-26", report.blockers)
        self.assertIn("intake route contract is unresolved", report.blockers)
        self.assertIn("session calendar is unresolved", report.blockers)
        self.assertIn("roll rule is unresolved", report.blockers)
        self.assertIn("back-adjustment rule is unresolved", report.blockers)
        with self.assertRaises(CarverBlocked):
            report.require_real_data_ready()
        with self.assertRaises(CarverBlocked):
            require_real_data_conformance_preflight(report)

    def test_p02_completion_report_names_all_book_legs_without_es_substitution(self) -> None:
        report = build_portfolio_completion_report(
            p02_all_weather(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26", "ZF": "06-26", "QM": "06-26", "ZC": "06-26", "MGC": "06-26"},
            self.locked_risk_fx,
        )

        self.assertEqual([row.contract_code for row in report.mapping_rows], ["MES", "ZN", "ZF", "QM", "ZC", "MGC"])
        self.assertNotIn("ES", [row.contract_code for row in report.mapping_rows])
        self.assertEqual(sum(row.status is ProviderMappingStatus.LOCKED for row in report.mapping_rows), 1)
        for code in ("MES", "ZF", "QM", "ZC", "MGC"):
            self.assertIn(f"provider mapping unresolved for {code} 06-26", report.blockers)

    def test_risk_fx_contract_fails_closed_until_sources_are_locked(self) -> None:
        unresolved = RiskFxInputContract(
            as_of=self.as_of,
            annual_risk_status=SourceRuleStatus.UNRESOLVED,
            fx_status=SourceRuleStatus.UNRESOLVED,
        )
        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            unresolved,
        )

        self.assertIn("annual risk input contract is unresolved", report.blockers)
        self.assertIn("FX input contract is unresolved", report.blockers)
        with self.assertRaises(CarverBlocked):
            RiskFxInputContract(
                as_of=datetime(2026, 5, 28),
                annual_risk_status=SourceRuleStatus.LOCKED,
                fx_status=SourceRuleStatus.LOCKED,
                annual_risk_artifact=SourceArtifactRef("docs/process/risk.md"),
                fx_artifact=SourceArtifactRef("docs/process/fx.md"),
            ).validate()
        with self.assertRaises(CarverBlocked):
            RiskFxInputContract(
                as_of=datetime(2026, 5, 28, 12, tzinfo=timezone.utc),
                annual_risk_status=SourceRuleStatus.LOCKED,
                fx_status=SourceRuleStatus.LOCKED,
                annual_risk_artifact=SourceArtifactRef("docs/process/risk.md"),
                fx_artifact=SourceArtifactRef("docs/process/fx.md"),
            ).validate()
        with self.assertRaises(CarverBlocked):
            RiskFxInputContract(
                as_of=self.as_of,
                annual_risk_status=SourceRuleStatus.LOCKED,
                fx_status=SourceRuleStatus.LOCKED,
                annual_risk_artifact=None,
                fx_artifact=SourceArtifactRef("docs/process/fx.md"),
            ).validate()
        with self.assertRaises(CarverBlocked):
            RiskFxInputContract(
                as_of=self.as_of,
                annual_risk_status=SourceRuleStatus.LOCKED,
                fx_status=SourceRuleStatus.LOCKED,
                annual_risk_artifact=SourceArtifactRef("tmp/risk.txt"),
                fx_artifact=SourceArtifactRef("docs/process/fx.md"),
            ).validate()
        for bad_path in (
            "docs/process/DOES_NOT_EXIST.md",
            "docs/process/../mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md",
            "docs/researchops/../../QuantLab_v3/foo.md",
            str(ROOT / "docs" / "process" / "CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
        ):
            with self.subTest(bad_path=bad_path):
                with self.assertRaises(CarverBlocked):
                    SourceArtifactRef(bad_path).validate("artifact")

    def test_report_can_only_be_ready_when_all_non_performance_inputs_are_locked(self) -> None:
        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            self.locked_risk_fx,
            intake_contract=IntakeRouteContract(
                PortfolioIntakeMode.DIRECT_DAILY_PRIMARY,
                SourceRuleStatus.LOCKED,
                SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            ),
            session_calendar=SessionCalendarSpec("P01/P02 session calendar", SourceRuleStatus.LOCKED, "UTC"),
            roll_rule=RollRuleSpec("P01/P02 roll rule", SourceRuleStatus.LOCKED),
            back_adjustment=BackAdjustmentSpec("P01/P02 back-adjustment rule", SourceRuleStatus.LOCKED),
            session_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            roll_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            back_adjustment_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
        )

        self.assertEqual(report.status, PortfolioCompletionStatus.SYNTHETIC_READY_REAL_DATA_BLOCKED)
        self.assertEqual(report.blockers, ("provider mapping unresolved for MES 06-26",))
        with self.assertRaises(CarverBlocked):
            build_portfolio_completion_report(
                p01_risk_parity(1_000_000, 0.20, 1.0),
                {"MES": "06-26", "ZN": "06-26"},
                self.locked_risk_fx,
                intake_contract=IntakeRouteContract("DIRECT_DAILY_PRIMARY"),
            )
        with self.assertRaises(CarverBlocked):
            IntakeRouteContract(
                PortfolioIntakeMode.DIRECT_DAILY_PRIMARY,
                SourceRuleStatus.LOCKED,
                "",
            ).validate()

    def test_minute_fallback_requires_direct_daily_blockage_artifact(self) -> None:
        source_artifact = SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md")
        with self.assertRaises(CarverBlocked):
            build_portfolio_completion_report(
                p01_risk_parity(1_000_000, 0.20, 1.0),
                {"MES": "06-26", "ZN": "06-26"},
                self.locked_risk_fx,
                intake_contract=IntakeRouteContract(
                    PortfolioIntakeMode.MINUTE_DERIVED_FALLBACK,
                    SourceRuleStatus.LOCKED,
                    source_artifact,
                ),
            )

        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            self.locked_risk_fx,
            intake_contract=IntakeRouteContract(
                PortfolioIntakeMode.MINUTE_DERIVED_FALLBACK,
                SourceRuleStatus.LOCKED,
                source_artifact,
                direct_daily_blocked_artifact=source_artifact,
            ),
        )

        self.assertEqual(report.intake_mode, PortfolioIntakeMode.MINUTE_DERIVED_FALLBACK)
        self.assertNotIn("intake route contract is unresolved", report.blockers)
        self.assertIn("provider mapping unresolved for MES 06-26", report.blockers)

    def test_completion_report_rejects_provider_mapping_set_mismatch(self) -> None:
        p01 = p01_risk_parity(1_000_000, 0.20, 1.0)
        zn_only_mapping_set = PortfolioProviderMappingSet(
            p01,
            (LockedPortfolioProviderMapping(p01.legs[1].contract, "06-26", "ZN JUN26", "4470301"),),
        )
        with self.assertRaises(CarverBlocked):
            build_portfolio_completion_report(
                p01,
                {"MES": "06-26", "ZN": "06-26"},
                self.locked_risk_fx,
                provider_mapping_set=zn_only_mapping_set,
            )

    def test_locked_rule_placeholders_still_need_artifact_references(self) -> None:
        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            self.locked_risk_fx,
            intake_contract=IntakeRouteContract(
                PortfolioIntakeMode.DIRECT_DAILY_PRIMARY,
                SourceRuleStatus.LOCKED,
                SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            ),
            session_calendar=SessionCalendarSpec("P01/P02 session calendar", SourceRuleStatus.LOCKED, "UTC"),
            roll_rule=RollRuleSpec("P01/P02 roll rule", SourceRuleStatus.LOCKED),
            back_adjustment=BackAdjustmentSpec("P01/P02 back-adjustment rule", SourceRuleStatus.LOCKED),
        )

        self.assertIn("session calendar artifact is unresolved", report.blockers)
        self.assertIn("roll rule artifact is unresolved", report.blockers)
        self.assertIn("back-adjustment artifact is unresolved", report.blockers)


if __name__ == "__main__":
    unittest.main()

```

---

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

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
from carver.spine.m0 import CompletedBar, LaneClass, CarverBlocked  # noqa: E402
from carver.spine.m1 import RoundingPolicy, SizingInput, TimedValue, size_contracts  # noqa: E402
from carver.spine.m3 import PortfolioLeg, PortfolioSpec, p01_risk_parity, p02_all_weather, synthetic_market_inputs  # noqa: E402


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
                PortfolioLeg("MES", "S&P 500 micro future", 0.40, 5),
                PortfolioLeg("ZN", "US 10-year bond future", 0.60, 1000),
            ),
        )
        with self.assertRaises(CarverBlocked):
            p01_synthetic_conformance(spoof, self.bar, market)

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


if __name__ == "__main__":
    unittest.main()

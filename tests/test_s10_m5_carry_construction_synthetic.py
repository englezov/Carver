from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.daily_bars import CompletedDailyMarketBar  # noqa: E402
from carver.spine.m0 import CarverBlocked, CompletedBar, LaneClass, SourceRuleStatus  # noqa: E402
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402
from carver.spine.m5 import (  # noqa: E402
    M5CarryConstructionRequest,
    M5CarryConstructionSourceLocks,
    M5RawCarrySignConvention,
    m5_synthetic_carry_construction_conformance,
)


class S10M5CarryConstructionSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.as_of = datetime(2026, 5, 29, tzinfo=timezone.utc)

    def test_m5_constructs_positive_risk_adjusted_carry_input_only(self) -> None:
        result = m5_synthetic_carry_construction_conformance(self.request())

        self.assertEqual(result.instrument, zn_contract())
        self.assertEqual(result.held_contract_month, "06-26")
        self.assertEqual(result.comparison_contract_month, "09-26")
        self.assertEqual(result.sign_convention_label, "synthetic far-minus-held")
        self.assertAlmostEqual(result.raw_carry, 3.0)
        self.assertAlmostEqual(result.expiry_distance_years, 0.25)
        self.assertAlmostEqual(result.annualization_factor, 4.0)
        self.assertAlmostEqual(result.annualized_carry, 12.0)
        self.assertAlmostEqual(result.risk_adjusted_carry, 6.0)
        self.assertEqual(result.carry_timestamp, self.as_of)
        self.assertFalse(result.interpretable_trading_signal)
        self.assertEqual(result.performance_metrics, ())
        self.assertEqual(result.position_outputs, ())

    def test_m5_constructs_negative_risk_adjusted_carry_input(self) -> None:
        request = self.request(comparison_close=99.5)

        result = m5_synthetic_carry_construction_conformance(request)

        self.assertAlmostEqual(result.raw_carry, -0.5)
        self.assertAlmostEqual(result.annualized_carry, -2.0)
        self.assertAlmostEqual(result.risk_adjusted_carry, -1.0)

    def test_m5_respects_locked_synthetic_sign_convention(self) -> None:
        request = self.request(sign=M5RawCarrySignConvention("synthetic held-minus-far", -1.0))

        result = m5_synthetic_carry_construction_conformance(request)

        self.assertAlmostEqual(result.raw_carry, -3.0)
        self.assertEqual(result.sign_convention_label, "synthetic held-minus-far")

    def test_m5_rejects_non_source_native_lane_and_unresolved_sources(self) -> None:
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(self.request(lane_class=LaneClass.CFD_ADAPTER))
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                self.request(
                    source_locks=M5CarryConstructionSourceLocks(
                        sign_convention_status=SourceRuleStatus.UNRESOLVED
                    )
                )
            )

    def test_m5_rejects_contract_identity_and_month_drift(self) -> None:
        request = self.request()
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(replace(request, instrument=mes_contract()))
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(request, comparison_bar=self.bar("06-26", 103.0))
            )
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(request, comparison_bar=self.bar("09-26", 103.0, contract=mes_contract()))
            )

    def test_m5_rejects_timestamp_and_completed_bar_drift(self) -> None:
        request = self.request()
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(request, comparison_bar=self.bar("09-26", 103.0, as_of=self.as_of + timedelta(days=1)))
            )
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(request, price_risk=TimedValue(2.0, self.as_of + timedelta(days=1)))
            )
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(request, held_bar=self.bar("06-26", 100.0, completed_bar=CompletedBar(self.as_of, is_complete=False)))
            )
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(
                    request,
                    held_bar=self.bar(
                        "06-26",
                        100.0,
                        as_of=datetime(2026, 5, 29, 12, tzinfo=timezone.utc),
                    ),
                )
            )

    def test_m5_rejects_invalid_prices_risk_expiry_and_sign_convention(self) -> None:
        request = self.request()
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(replace(request, held_bar=self.bar("06-26", 0.0)))
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(replace(request, price_risk=TimedValue(0.0, self.as_of)))
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(request, expiry_distance_years=TimedValue(-0.25, self.as_of))
            )
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(request, sign_convention=M5RawCarrySignConvention("", 1.0))
            )
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(request, sign_convention=M5RawCarrySignConvention("bad multiplier", 0.5))
            )
        with self.assertRaises(CarverBlocked):
            m5_synthetic_carry_construction_conformance(
                replace(
                    request,
                    sign_convention=M5RawCarrySignConvention(
                        "unresolved sign",
                        1.0,
                        SourceRuleStatus.UNRESOLVED,
                    ),
                )
            )

    def test_gate_doc_records_synthetic_m5_boundary(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_2026-05-29.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST", text)
        self.assertIn("risk-adjusted carry forecast input", text)
        self.assertIn("No real-data execution", text)
        self.assertIn("no S10 smoothing", text)
        self.assertIn("no S11", text)

    def request(
        self,
        *,
        comparison_close: float = 103.0,
        sign: M5RawCarrySignConvention = M5RawCarrySignConvention("synthetic far-minus-held", 1.0),
        source_locks: M5CarryConstructionSourceLocks = M5CarryConstructionSourceLocks(),
        lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
    ) -> M5CarryConstructionRequest:
        return M5CarryConstructionRequest(
            instrument=zn_contract(),
            held_bar=self.bar("06-26", 100.0),
            comparison_bar=self.bar("09-26", comparison_close),
            sign_convention=sign,
            expiry_distance_years=TimedValue(0.25, self.as_of),
            price_risk=TimedValue(2.0, self.as_of),
            source_locks=source_locks,
            lane_class=lane_class,
        )

    def bar(
        self,
        month: str,
        close: float,
        *,
        as_of: datetime | None = None,
        contract=zn_contract(),
        completed_bar: CompletedBar | None = None,
    ) -> CompletedDailyMarketBar:
        completed = completed_bar or CompletedBar(as_of or self.as_of)
        return CompletedDailyMarketBar(
            completed_bar=completed,
            contract=contract,
            contract_month=month,
            open=close,
            high=close + 1.0,
            low=close - 1.0,
            close=close,
            volume=100.0,
        )


if __name__ == "__main__":
    unittest.main()

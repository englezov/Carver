from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.daily_bars import CompletedDailyMarketBar  # noqa: E402
from carver.spine.m0 import CompletedBar, LaneClass, CarverBlocked  # noqa: E402
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402
from carver.spine.s09_zn_package import (  # noqa: E402
    S09_ZN_CONTRACT_MONTH,
    S09_ZN_DISPLAY_SYMBOL,
    S09_ZN_ELIGIBLE_SPANS,
    S09_ZN_PROVIDER_SYMBOL_ID,
    S09TinySliceConformanceRequest,
    build_s09_zn_package,
    require_s09_zn_probe_authorization,
    s09_zn_tiny_slice_forecast_conformance,
)
from carver.spine.web_chart_api import ChartBarType  # noqa: E402


class S09ZnPackageSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.start = datetime(2025, 9, 13, tzinfo=timezone.utc)

    def daily_bar(self, index: int, close: float, *, contract=None, month: str = S09_ZN_CONTRACT_MONTH) -> CompletedDailyMarketBar:
        timestamp = self.start + timedelta(days=index)
        chosen_contract = contract or zn_contract()
        return CompletedDailyMarketBar(
            completed_bar=CompletedBar(timestamp),
            contract=chosen_contract,
            contract_month=month,
            open=close,
            high=close + 1.0,
            low=close - 1.0,
            close=close,
            volume=100.0,
        )

    def zn_bars(self, count: int = 257) -> tuple[CompletedDailyMarketBar, ...]:
        return tuple(self.daily_bar(index, 110.0 + index * 0.05) for index in range(count))

    def test_builds_locked_zn_readiness_package_without_probe_execution(self) -> None:
        package = build_s09_zn_package()

        self.assertEqual(package.instrument_contract.contract, zn_contract())
        self.assertEqual(package.instrument_contract.contract_month, S09_ZN_CONTRACT_MONTH)
        self.assertEqual(package.instrument_contract.eligible_spans, S09_ZN_ELIGIBLE_SPANS)
        self.assertEqual(package.readiness_report.blockers, ())
        self.assertEqual(package.probe_plan.request.symbol.provider_symbol_id, S09_ZN_PROVIDER_SYMBOL_ID)
        self.assertEqual(package.probe_plan.request.symbol.display_symbol, S09_ZN_DISPLAY_SYMBOL)
        self.assertEqual(package.probe_plan.request.bar_type, ChartBarType.DAILY)
        self.assertEqual(package.probe_plan.request.element_size, 1)
        self.assertEqual(package.probe_plan.request.element_count, 1)
        with self.assertRaises(CarverBlocked):
            require_s09_zn_probe_authorization(package)

    def test_tiny_slice_forecast_conformance_uses_pre_normalized_zn_bars_only(self) -> None:
        bars = self.zn_bars()
        result = s09_zn_tiny_slice_forecast_conformance(
            S09TinySliceConformanceRequest(
                bars=bars,
                daily_price_risk=TimedValue(1.0, bars[-1].timestamp),
                package=build_s09_zn_package(),
            )
        )

        self.assertEqual(result.contract_code, "ZN")
        self.assertEqual([forecast.span for forecast in result.rule_forecasts], [32, 64])
        self.assertLessEqual(abs(result.final_forecast), 20.0)

    def test_tiny_slice_conformance_rejects_short_misaligned_or_wrong_contract_inputs(self) -> None:
        bars = self.zn_bars()
        package = build_s09_zn_package()
        with self.assertRaises(CarverBlocked):
            s09_zn_tiny_slice_forecast_conformance(
                S09TinySliceConformanceRequest(
                    bars=bars[:64],
                    daily_price_risk=TimedValue(1.0, bars[63].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_tiny_slice_forecast_conformance(
                S09TinySliceConformanceRequest(
                    bars=bars,
                    daily_price_risk=TimedValue(1.0, bars[-2].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_tiny_slice_forecast_conformance(
                S09TinySliceConformanceRequest(
                    bars=bars[:-1] + (self.daily_bar(256, 130.0, contract=mes_contract()),),
                    daily_price_risk=TimedValue(1.0, bars[-1].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_tiny_slice_forecast_conformance(
                S09TinySliceConformanceRequest(
                    bars=bars,
                    daily_price_risk=TimedValue(1.0, bars[-1].timestamp),
                    package=package,
                    lane_class=LaneClass.CFD_ADAPTER,
                )
            )

    def test_gate_doc_records_probe_and_conformance_non_authorization(self) -> None:
        text = (ROOT / "docs" / "process" / "CARVER_S09_REAL_DATA_READINESS_GATE_2026-05-29.md").read_text(encoding="utf-8")

        self.assertIn("One-Instrument ZN Package", text)
        self.assertIn("providerSymbolId: 4470301", text)
        self.assertIn("This gate does not execute the probe.", text)
        self.assertIn("It must not calculate returns, PnL", text)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.daily_bars import CompletedDailyMarketBar  # noqa: E402
from carver.spine.continuous import ContinuousChainBuildResult  # noqa: E402
from carver.spine.m0 import CompletedBar, LaneClass, CarverBlocked  # noqa: E402
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402
from carver.spine.s09_zn_package import (  # noqa: E402
    S09_ZN_CONTINUOUS_CONTRACT_MONTHS,
    S09_ZN_CONTINUOUS_ROLL_DATES,
    S09_ZN_CONTRACT_MONTH,
    S09_ZN_DISPLAY_SYMBOL,
    S09_ZN_ELIGIBLE_SPANS,
    S09_ZN_PROVIDER_SYMBOL_ID,
    S09_ZN_REQUIRED_DAILY_BARS,
    S09_ZN_UNIT_PRICE_RISK_CONFORMANCE_MODE,
    S09ContinuousTinySliceConformanceRequest,
    S09TinySliceConformanceRequest,
    build_s09_zn_package,
    require_s09_zn_probe_authorization,
    s09_zn_continuous_tiny_slice_forecast_conformance,
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

    def zn_bars(self, count: int = S09_ZN_REQUIRED_DAILY_BARS) -> tuple[CompletedDailyMarketBar, ...]:
        return tuple(self.daily_bar(index, 110.0 + index * 0.05) for index in range(count))

    def continuous_result(self, count: int = S09_ZN_REQUIRED_DAILY_BARS + 2, *, ready: bool = True) -> ContinuousChainBuildResult:
        segment_size = count // len(S09_ZN_CONTINUOUS_CONTRACT_MONTHS)
        bars: list[CompletedDailyMarketBar] = []
        for index in range(count):
            month_index = min(index // segment_size, len(S09_ZN_CONTINUOUS_CONTRACT_MONTHS) - 1)
            bars.append(
                self.daily_bar(
                    index,
                    110.0 + index * 0.04,
                    month=S09_ZN_CONTINUOUS_CONTRACT_MONTHS[month_index],
                )
            )
        return ContinuousChainBuildResult(
            adjusted_bars=tuple(bars),
            roll_dates=S09_ZN_CONTINUOUS_ROLL_DATES,
            source_contract_months=S09_ZN_CONTINUOUS_CONTRACT_MONTHS,
            minimum_rows=S09_ZN_REQUIRED_DAILY_BARS,
            ready=ready,
        )

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
        self.assertEqual(package.probe_plan.request.element_count, S09_ZN_REQUIRED_DAILY_BARS)
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

    def test_continuous_tiny_slice_conformance_uses_last_257_adjusted_bars_only(self) -> None:
        continuous = self.continuous_result()
        result = s09_zn_continuous_tiny_slice_forecast_conformance(
            S09ContinuousTinySliceConformanceRequest(
                continuous_result=continuous,
                daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-1].timestamp),
                package=build_s09_zn_package(),
            )
        )

        self.assertEqual(result.source_contract_months, S09_ZN_CONTINUOUS_CONTRACT_MONTHS)
        self.assertEqual(result.available_row_count, S09_ZN_REQUIRED_DAILY_BARS + 2)
        self.assertEqual(result.input_row_count, S09_ZN_REQUIRED_DAILY_BARS)
        self.assertEqual(result.price_risk_mode, S09_ZN_UNIT_PRICE_RISK_CONFORMANCE_MODE)
        self.assertFalse(result.interpretable_signal)
        self.assertEqual(result.forecast_result.as_of, continuous.adjusted_bars[-1].timestamp)
        self.assertEqual([forecast.span for forecast in result.forecast_result.rule_forecasts], [32, 64])
        self.assertLessEqual(abs(result.final_forecast), 20.0)

    def test_continuous_tiny_slice_conformance_rejects_unready_or_interpretable_inputs(self) -> None:
        continuous = self.continuous_result()
        package = build_s09_zn_package()
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=self.continuous_result(ready=False),
                    daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-1].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=ContinuousChainBuildResult(
                        adjusted_bars=continuous.adjusted_bars[:-1] + (self.daily_bar(258, 130.0, month="09-26"),),
                        roll_dates=continuous.roll_dates,
                        source_contract_months=continuous.source_contract_months,
                        minimum_rows=continuous.minimum_rows,
                        ready=True,
                    ),
                    daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-1].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=ContinuousChainBuildResult(
                        adjusted_bars=continuous.adjusted_bars[:-1]
                        + (self.daily_bar(258, 130.0, month=S09_ZN_CONTINUOUS_CONTRACT_MONTHS[0]),),
                        roll_dates=continuous.roll_dates,
                        source_contract_months=continuous.source_contract_months,
                        minimum_rows=continuous.minimum_rows,
                        ready=True,
                    ),
                    daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-1].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=ContinuousChainBuildResult(
                        adjusted_bars=continuous.adjusted_bars,
                        roll_dates=("2025-09-22",),
                        source_contract_months=continuous.source_contract_months,
                        minimum_rows=continuous.minimum_rows,
                        ready=True,
                    ),
                    daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-1].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=continuous,
                    daily_price_risk=TimedValue(2.0, continuous.adjusted_bars[-1].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=continuous,
                    daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-2].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=ContinuousChainBuildResult(
                        adjusted_bars=continuous.adjusted_bars,
                        roll_dates=continuous.roll_dates,
                        source_contract_months=("12-25", "03-26", "06-26"),
                        minimum_rows=continuous.minimum_rows,
                        ready=True,
                    ),
                    daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-1].timestamp),
                    package=package,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=continuous,
                    daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-1].timestamp),
                    package=package,
                    price_risk_mode="SOURCE_PRICE_RISK",
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_zn_continuous_tiny_slice_forecast_conformance(
                S09ContinuousTinySliceConformanceRequest(
                    continuous_result=continuous,
                    daily_price_risk=TimedValue(1.0, continuous.adjusted_bars[-1].timestamp),
                    package=package,
                    lane_class=LaneClass.CFD_ADAPTER,
                )
            )

    def test_tiny_slice_conformance_rejects_short_misaligned_or_wrong_contract_inputs(self) -> None:
        bars = self.zn_bars()
        package = build_s09_zn_package()
        with self.assertRaises(CarverBlocked):
            s09_zn_tiny_slice_forecast_conformance(
                S09TinySliceConformanceRequest(
                    bars=bars[: S09_ZN_REQUIRED_DAILY_BARS - 1],
                    daily_price_risk=TimedValue(1.0, bars[S09_ZN_REQUIRED_DAILY_BARS - 2].timestamp),
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
        conformance_text = (
            ROOT / "docs" / "process" / "CARVER_S09_ZN_TINY_SLICE_FORECAST_PLUMBING_CONFORMANCE_2026-05-29.md"
        ).read_text(encoding="utf-8")

        self.assertIn("One-Instrument ZN Package", text)
        self.assertIn("providerSymbolId: 4470301", text)
        self.assertIn("elementCount: 257", text)
        self.assertIn("This gate does not execute the probe.", text)
        self.assertIn("It must not calculate returns, PnL", text)
        self.assertIn(S09_ZN_UNIT_PRICE_RISK_CONFORMANCE_MODE, conformance_text)
        self.assertIn("interpretable_signal: FALSE", conformance_text)
        self.assertIn("No raw market rows are committed.", conformance_text)
        self.assertIn("no diagnostics, no backtests", conformance_text)


if __name__ == "__main__":
    unittest.main()

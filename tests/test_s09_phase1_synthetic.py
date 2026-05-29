from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.continuous import ContinuousChainBuildResult  # noqa: E402
from carver.spine.daily_bars import CompletedDailyMarketBar  # noqa: E402
from carver.spine.data_acquisition import (  # noqa: E402
    Phase1ContinuousReadinessReport,
    Phase1ContinuousReadinessSummary,
    build_parts_1_3_multi_asset_phase1_manifest,
)
from carver.spine.m0 import CarverBlocked, CompletedBar, LaneClass  # noqa: E402
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m3 import mes_contract, zf_contract, zn_contract  # noqa: E402
from carver.spine.s09_phase1 import (  # noqa: E402
    S09_PHASE1_CONTRACT_MONTHS,
    S09_PHASE1_ELIGIBLE_SPANS,
    S09_PHASE1_REQUIRED_DAILY_BARS,
    S09_PHASE1_ROOTS,
    S09Phase1InstrumentForecastInput,
    S09Phase1MultiInstrumentConformanceRequest,
    s09_phase1_multi_instrument_forecast_conformance,
)


class S09Phase1SyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.start = datetime(2025, 9, 13, tzinfo=timezone.utc)

    def test_phase1_multi_instrument_conformance_builds_forecasts_only(self) -> None:
        request = self.request()

        result = s09_phase1_multi_instrument_forecast_conformance(request)

        self.assertEqual(result.roots, S09_PHASE1_ROOTS)
        self.assertFalse(result.interpretable_portfolio_signal)
        self.assertEqual(result.performance_metrics, ())
        for instrument_result in result.instrument_results:
            self.assertEqual(instrument_result.available_row_count, S09_PHASE1_REQUIRED_DAILY_BARS + 2)
            self.assertEqual(instrument_result.input_row_count, S09_PHASE1_REQUIRED_DAILY_BARS)
            self.assertEqual(instrument_result.source_contract_months, S09_PHASE1_CONTRACT_MONTHS)
            self.assertEqual(
                tuple(rule.span for rule in instrument_result.forecast_result.rule_forecasts),
                S09_PHASE1_ELIGIBLE_SPANS,
            )
            self.assertLessEqual(abs(instrument_result.final_forecast), 20.0)

    def test_phase1_multi_instrument_conformance_rejects_unready_readiness(self) -> None:
        request = self.request()
        bad_report = Phase1ContinuousReadinessReport(
            request.readiness_report.manifest_id,
            request.readiness_report.summaries[:1]
            + (
                replace(
                    request.readiness_report.summaries[1],
                    ready=False,
                    adjusted_row_count=0,
                    first_date="",
                    last_date="",
                    source_contract_months=(),
                    blockers=("missing ZN chain",),
                ),
            )
            + request.readiness_report.summaries[2:],
        )

        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(replace(request, readiness_report=bad_report))

    def test_phase1_multi_instrument_conformance_rejects_missing_or_extra_roots(self) -> None:
        request = self.request()

        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(
                replace(request, instrument_inputs=request.instrument_inputs[:2])
            )
        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(
                replace(request, required_roots=("MES", "ZN"))
            )
        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(
                replace(request, instrument_inputs=(request.instrument_inputs[1], request.instrument_inputs[0], request.instrument_inputs[2]))
            )

    def test_phase1_multi_instrument_conformance_rejects_contract_or_month_drift(self) -> None:
        request = self.request()
        mes = request.instrument_inputs[0]
        wrong_contract_bar = replace(mes.continuous_result.adjusted_bars[-1], contract=zn_contract())
        wrong_contract_result = replace(
            mes.continuous_result,
            adjusted_bars=mes.continuous_result.adjusted_bars[:-1] + (wrong_contract_bar,),
        )
        wrong_month_bar = replace(mes.continuous_result.adjusted_bars[-1], contract_month="09-26")
        wrong_month_result = replace(
            mes.continuous_result,
            adjusted_bars=mes.continuous_result.adjusted_bars[:-1] + (wrong_month_bar,),
        )

        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(
                replace(
                    request,
                    instrument_inputs=(
                        replace(mes, continuous_result=wrong_contract_result),
                        request.instrument_inputs[1],
                        request.instrument_inputs[2],
                    ),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(
                replace(
                    request,
                    instrument_inputs=(
                        replace(mes, continuous_result=wrong_month_result),
                        request.instrument_inputs[1],
                        request.instrument_inputs[2],
                    ),
                )
            )

    def test_phase1_multi_instrument_conformance_rejects_readiness_date_drift(self) -> None:
        request = self.request()
        bad_first_date = Phase1ContinuousReadinessReport(
            request.readiness_report.manifest_id,
            (
                replace(request.readiness_report.summaries[0], first_date="2025-01-01"),
                request.readiness_report.summaries[1],
                request.readiness_report.summaries[2],
            ),
        )
        bad_last_date = Phase1ContinuousReadinessReport(
            request.readiness_report.manifest_id,
            (
                request.readiness_report.summaries[0],
                replace(request.readiness_report.summaries[1], last_date="2026-01-01"),
                request.readiness_report.summaries[2],
            ),
        )

        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(replace(request, readiness_report=bad_first_date))
        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(replace(request, readiness_report=bad_last_date))

    def test_phase1_multi_instrument_conformance_rejects_risk_or_rule_drift(self) -> None:
        request = self.request()
        mes = request.instrument_inputs[0]

        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(
                replace(
                    request,
                    instrument_inputs=(
                        replace(mes, daily_price_risk=TimedValue(1.0, mes.continuous_result.adjusted_bars[-2].timestamp)),
                        request.instrument_inputs[1],
                        request.instrument_inputs[2],
                    ),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(
                replace(
                    request,
                    instrument_inputs=(
                        replace(mes, eligible_spans=(16, 64)),
                        request.instrument_inputs[1],
                        request.instrument_inputs[2],
                    ),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_phase1_multi_instrument_forecast_conformance(replace(request, lane_class=LaneClass.CFD_ADAPTER))

    def test_gate_doc_records_no_portfolio_or_performance_authorization(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_PHASE1_MULTI_INSTRUMENT_FORECAST_CONFORMANCE_SURFACE_2026-05-29.md"
        ).read_text(encoding="utf-8")

        self.assertIn("MES / ZN / ZF", text)
        self.assertIn("forecast-only", text)
        self.assertIn("No returns, PnL, Sharpe", text)
        self.assertIn("not a portfolio construction gate", text)
        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_CARVER_S09_PHASE1_MULTI_INSTRUMENT_FORECAST_CONFORMANCE_NOT_DIAGNOSTIC_NOT_BACKTEST", text)

    def request(self) -> S09Phase1MultiInstrumentConformanceRequest:
        inputs = tuple(self.instrument_input(root) for root in S09_PHASE1_ROOTS)
        return S09Phase1MultiInstrumentConformanceRequest(
            readiness_report=self.readiness_report(inputs),
            instrument_inputs=inputs,
        )

    def readiness_report(
        self,
        inputs: tuple[S09Phase1InstrumentForecastInput, ...],
    ) -> Phase1ContinuousReadinessReport:
        summaries = tuple(
            Phase1ContinuousReadinessSummary(
                root=instrument.root,
                ready=True,
                adjusted_row_count=len(instrument.continuous_result.adjusted_bars),
                minimum_rows=S09_PHASE1_REQUIRED_DAILY_BARS,
                first_date=instrument.continuous_result.adjusted_bars[0].timestamp.date().isoformat(),
                last_date=instrument.continuous_result.adjusted_bars[-1].timestamp.date().isoformat(),
                source_contract_months=instrument.continuous_result.source_contract_months,
            )
            for instrument in inputs
        )
        report = Phase1ContinuousReadinessReport(build_parts_1_3_multi_asset_phase1_manifest().manifest_id, summaries)
        report.validate()
        return report

    def instrument_input(self, root: str) -> S09Phase1InstrumentForecastInput:
        continuous = self.continuous_result(root)
        return S09Phase1InstrumentForecastInput(
            root=root,
            continuous_result=continuous,
            daily_price_risk=TimedValue(self.daily_price_risk(root), continuous.adjusted_bars[-1].timestamp),
        )

    def continuous_result(self, root: str) -> ContinuousChainBuildResult:
        count = S09_PHASE1_REQUIRED_DAILY_BARS + 2
        segment_size = count // len(S09_PHASE1_CONTRACT_MONTHS)
        bars = tuple(
            self.daily_bar(
                root,
                index,
                self.base_price(root) + index * self.trend_increment(root),
                S09_PHASE1_CONTRACT_MONTHS[min(index // segment_size, len(S09_PHASE1_CONTRACT_MONTHS) - 1)],
            )
            for index in range(count)
        )
        result = ContinuousChainBuildResult(
            adjusted_bars=bars,
            roll_dates=("2025-09-22", "2025-12-22", "2026-03-23"),
            source_contract_months=S09_PHASE1_CONTRACT_MONTHS,
            minimum_rows=S09_PHASE1_REQUIRED_DAILY_BARS,
            ready=True,
        )
        result.validate()
        return result

    def daily_bar(self, root: str, index: int, close: float, contract_month: str) -> CompletedDailyMarketBar:
        timestamp = self.start + timedelta(days=index)
        return CompletedDailyMarketBar(
            completed_bar=CompletedBar(timestamp),
            contract={"MES": mes_contract(), "ZN": zn_contract(), "ZF": zf_contract()}[root],
            contract_month=contract_month,
            open=close,
            high=close + 0.75,
            low=close - 0.75,
            close=close,
            volume=100.0 + index,
        )

    def base_price(self, root: str) -> float:
        return {"MES": 5000.0, "ZN": 110.0, "ZF": 106.0}[root]

    def trend_increment(self, root: str) -> float:
        return {"MES": 0.8, "ZN": 0.04, "ZF": 0.03}[root]

    def daily_price_risk(self, root: str) -> float:
        return {"MES": 45.0, "ZN": 0.45, "ZF": 0.35}[root]


if __name__ == "__main__":
    unittest.main()

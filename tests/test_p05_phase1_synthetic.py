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
from carver.spine.m0 import CarverBlocked, CompletedBar, LaneClass, SourceRuleStatus  # noqa: E402
from carver.spine.m1 import RoundingPolicy, TimedValue  # noqa: E402
from carver.spine.m3 import PortfolioLeg, p02_all_weather, mes_contract, zf_contract, zn_contract  # noqa: E402
from carver.spine.p05_phase1 import (  # noqa: E402
    P05_PHASE1_CONSTRUCTION_ID,
    P05_PHASE1_FORECAST_DIVISOR,
    P05Phase1ConstructionRequest,
    P05Phase1ConstructionSourceLocks,
    P05Phase1LegConstructionInput,
    p05_phase1_portfolio_construction_conformance,
    p05_phase1_seed_portfolio_spec,
)
from carver.spine.s09_phase1 import (  # noqa: E402
    S09_PHASE1_CONTRACT_MONTHS,
    S09_PHASE1_REQUIRED_DAILY_BARS,
    S09_PHASE1_ROOTS,
    S09Phase1InstrumentForecastInput,
    S09Phase1MultiInstrumentConformanceRequest,
    s09_phase1_multi_instrument_forecast_conformance,
)


class P05Phase1SyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.start = datetime(2025, 9, 13, tzinfo=timezone.utc)

    def test_p05_phase1_construction_converts_forecasts_to_desired_positions_only(self) -> None:
        request = self.construction_request()

        result = p05_phase1_portfolio_construction_conformance(request)

        self.assertEqual(result.construction_id, P05_PHASE1_CONSTRUCTION_ID)
        self.assertEqual(result.roots, S09_PHASE1_ROOTS)
        self.assertFalse(result.is_complete_p02)
        self.assertFalse(result.is_complete_p05)
        self.assertFalse(result.interpretable_performance)
        self.assertEqual(result.performance_metrics, ())
        for instrument in result.instrument_results:
            self.assertEqual(instrument.contract.code, instrument.root)
            self.assertAlmostEqual(instrument.forecast_multiplier, instrument.final_forecast / P05_PHASE1_FORECAST_DIVISOR)
            self.assertAlmostEqual(
                instrument.desired_unrounded_contracts,
                instrument.base_sizing.unrounded_contracts * instrument.forecast_multiplier,
            )

    def test_p05_phase1_construction_is_not_complete_p02_or_book_p05(self) -> None:
        request = self.construction_request()

        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(replace(request, portfolio=p02_all_weather(1_000_000, 0.20, 1.03)))

        wrong_contract_portfolio = p05_phase1_seed_portfolio_spec(1_000_000, 0.20, 1.03)
        wrong_contract_portfolio = replace(
            wrong_contract_portfolio,
            legs=(
                wrong_contract_portfolio.legs[0],
                PortfolioLeg(mes_contract(), wrong_contract_portfolio.legs[1].weight),
                wrong_contract_portfolio.legs[2],
            ),
        )
        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(replace(request, portfolio=wrong_contract_portfolio))

    def test_p05_phase1_construction_rejects_forecast_or_root_drift(self) -> None:
        request = self.construction_request()
        bad_forecast = replace(request.forecast_conformance, performance_metrics=("Sharpe",))
        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(replace(request, forecast_conformance=bad_forecast))

        bad_row_count = replace(
            request.forecast_conformance,
            instrument_results=(
                replace(request.forecast_conformance.instrument_results[0], input_row_count=128),
                request.forecast_conformance.instrument_results[1],
                request.forecast_conformance.instrument_results[2],
            ),
        )
        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(replace(request, forecast_conformance=bad_row_count))

        bad_source_months = replace(
            request.forecast_conformance,
            instrument_results=(
                request.forecast_conformance.instrument_results[0],
                replace(request.forecast_conformance.instrument_results[1], source_contract_months=S09_PHASE1_CONTRACT_MONTHS[1:]),
                request.forecast_conformance.instrument_results[2],
            ),
        )
        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(replace(request, forecast_conformance=bad_source_months))

        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(replace(request, leg_inputs=request.leg_inputs[:2]))

        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(
                replace(request, leg_inputs=(request.leg_inputs[1], request.leg_inputs[0], request.leg_inputs[2]))
            )

    def test_p05_phase1_construction_rejects_unlocked_or_misaligned_sources(self) -> None:
        request = self.construction_request()
        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(
                replace(
                    request,
                    source_locks=P05Phase1ConstructionSourceLocks(
                        forecast_to_position_scale_status=SourceRuleStatus.UNRESOLVED
                    ),
                )
            )

        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(
                replace(request, capital=TimedValue(1_000_000, request.capital.as_of - timedelta(days=1)))
            )

        bad_daily_risk = replace(request.leg_inputs[0], daily_price_risk=TimedValue(999.0, request.capital.as_of))
        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(
                replace(request, leg_inputs=(bad_daily_risk, request.leg_inputs[1], request.leg_inputs[2]))
            )

        bad_prevalidation = replace(request.leg_inputs[1], risk_estimate_prevalidated=False)
        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(
                replace(request, leg_inputs=(request.leg_inputs[0], bad_prevalidation, request.leg_inputs[2]))
            )

        with self.assertRaises(CarverBlocked):
            p05_phase1_portfolio_construction_conformance(replace(request, lane_class=LaneClass.CFD_ADAPTER))

    def test_gate_doc_records_synthetic_only_construction_boundary(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_P05_PHASE1_PORTFOLIO_CONSTRUCTION_CONFORMANCE_2026-05-29.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_PHASE1_PORTFOLIO_CONSTRUCTION_CONFORMANCE_NOT_DIAGNOSTIC_NOT_BACKTEST", text)
        self.assertIn("MES / ZN / ZF", text)
        self.assertIn("not complete P02", text)
        self.assertIn("not complete P05", text)
        self.assertIn("No returns, PnL, Sharpe", text)

    def construction_request(self) -> P05Phase1ConstructionRequest:
        forecast_conformance = self.forecast_conformance()
        as_of = forecast_conformance.instrument_results[0].forecast_result.as_of
        portfolio = p05_phase1_seed_portfolio_spec(1_000_000, 0.20, 1.03)
        return P05Phase1ConstructionRequest(
            forecast_conformance=forecast_conformance,
            portfolio=portfolio,
            leg_inputs=tuple(self.leg_input(root, as_of) for root in S09_PHASE1_ROOTS),
            capital=TimedValue(portfolio.capital, as_of),
            target_risk=TimedValue(portfolio.target_risk, as_of),
            idm=TimedValue(portfolio.idm, as_of),
            rounding_policy=RoundingPolicy.TRUNCATE,
        )

    def forecast_conformance(self):
        inputs = tuple(self.instrument_forecast_input(root) for root in S09_PHASE1_ROOTS)
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
        return s09_phase1_multi_instrument_forecast_conformance(
            S09Phase1MultiInstrumentConformanceRequest(report, inputs)
        )

    def instrument_forecast_input(self, root: str) -> S09Phase1InstrumentForecastInput:
        continuous = self.continuous_result(root)
        as_of = continuous.adjusted_bars[-1].timestamp
        price, risk, _fx = self.market_values(root)
        daily_price_risk = price * risk / 16.0
        return S09Phase1InstrumentForecastInput(
            root=root,
            continuous_result=continuous,
            daily_price_risk=TimedValue(daily_price_risk, as_of),
        )

    def leg_input(self, root: str, as_of: datetime) -> P05Phase1LegConstructionInput:
        price, risk, fx = self.market_values(root)
        return P05Phase1LegConstructionInput(
            root=root,
            current_held_price=TimedValue(price, as_of),
            annual_risk_estimate=TimedValue(risk, as_of),
            daily_price_risk=TimedValue(price * risk / 16.0, as_of),
            fx_rate=TimedValue(fx, as_of),
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
        return CompletedDailyMarketBar(
            completed_bar=CompletedBar(self.start + timedelta(days=index)),
            contract={"MES": mes_contract(), "ZN": zn_contract(), "ZF": zf_contract()}[root],
            contract_month=contract_month,
            open=close,
            high=close + 0.75,
            low=close - 0.75,
            close=close,
            volume=100.0 + index,
        )

    def market_values(self, root: str) -> tuple[float, float, float]:
        return {
            "MES": (5200.0, 0.22, 1.0),
            "ZN": (110.0, 0.065, 1.0),
            "ZF": (106.0, 0.055, 1.0),
        }[root]

    def base_price(self, root: str) -> float:
        return {"MES": 5000.0, "ZN": 110.0, "ZF": 106.0}[root]

    def trend_increment(self, root: str) -> float:
        return {"MES": 0.8, "ZN": 0.04, "ZF": 0.03}[root]


if __name__ == "__main__":
    unittest.main()

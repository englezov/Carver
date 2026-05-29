from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from math import nan
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.daily_bars import CompletedDailyMarketBar  # noqa: E402
from carver.spine.m0 import CompletedBar, LaneClass, SourceRuleStatus, CarverBlocked  # noqa: E402
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m2 import (  # noqa: E402
    S09_EWMAC_SCALARS,
    ForecastBlockRequest,
    ForecastRuleInput,
    cap_forecast,
    combine_forecast_block,
    s09_fdm_for_allowed_spans,
    s09_rule_id,
)
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402
from carver.spine.s09 import (  # noqa: E402
    S09DailyPriceRiskRequest,
    S09SyntheticConvention,
    S09TrendForecastRequest,
    s09_daily_price_risk,
    s09_multiple_trend_forecast,
)


class S09M2SyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.start = datetime(2025, 9, 13, tzinfo=timezone.utc)
        self.as_of = self.start + timedelta(days=256)
        self.completed_bar = CompletedBar(self.as_of)

    def daily_bar(self, index: int, close: float, *, contract=None) -> CompletedDailyMarketBar:
        timestamp = self.start + timedelta(days=index)
        chosen_contract = contract or mes_contract()
        return CompletedDailyMarketBar(
            completed_bar=CompletedBar(timestamp),
            contract=chosen_contract,
            contract_month="06-26",
            open=close,
            high=close + 1.0,
            low=close - 1.0,
            close=close,
            volume=100.0,
        )

    def trend_bars(self, count: int = 257) -> tuple[CompletedDailyMarketBar, ...]:
        return tuple(self.daily_bar(index, 100.0 + index * 0.5) for index in range(count))

    def test_m2_scales_caps_weights_and_applies_fdm(self) -> None:
        rules = (
            ForecastRuleInput(s09_rule_id(32), TimedValue(3.0, self.as_of), S09_EWMAC_SCALARS[32]),
            ForecastRuleInput(s09_rule_id(64), TimedValue(4.0, self.as_of), S09_EWMAC_SCALARS[64]),
        )
        result = combine_forecast_block(
            ForecastBlockRequest(
                completed_bar=self.completed_bar,
                rule_inputs=rules,
                allowed_rule_ids=(s09_rule_id(32), s09_rule_id(64)),
                fdm=s09_fdm_for_allowed_spans((32, 64)),
            )
        )

        self.assertEqual([rule.rule_id for rule in result.rule_results], ["EWMAC32", "EWMAC64"])
        self.assertEqual([rule.weight for rule in result.rule_results], [0.5, 0.5])
        self.assertAlmostEqual(result.rule_results[0].scaled_forecast, 8.37)
        self.assertAlmostEqual(result.rule_results[1].scaled_forecast, 7.64)
        self.assertAlmostEqual(result.pre_fdm_forecast, (8.37 + 7.64) / 2.0)
        self.assertAlmostEqual(result.fdm, 1.03)
        self.assertAlmostEqual(result.final_forecast, result.post_fdm_forecast)

    def test_m2_caps_extreme_individual_and_combined_forecasts(self) -> None:
        self.assertEqual(cap_forecast(25.0), 20.0)
        self.assertEqual(cap_forecast(-25.0), -20.0)
        rules = (
            ForecastRuleInput(s09_rule_id(2), TimedValue(100.0, self.as_of), S09_EWMAC_SCALARS[2]),
            ForecastRuleInput(s09_rule_id(4), TimedValue(100.0, self.as_of), S09_EWMAC_SCALARS[4]),
            ForecastRuleInput(s09_rule_id(8), TimedValue(100.0, self.as_of), S09_EWMAC_SCALARS[8]),
            ForecastRuleInput(s09_rule_id(16), TimedValue(100.0, self.as_of), S09_EWMAC_SCALARS[16]),
            ForecastRuleInput(s09_rule_id(32), TimedValue(100.0, self.as_of), S09_EWMAC_SCALARS[32]),
            ForecastRuleInput(s09_rule_id(64), TimedValue(100.0, self.as_of), S09_EWMAC_SCALARS[64]),
        )
        result = combine_forecast_block(
            ForecastBlockRequest(
                completed_bar=self.completed_bar,
                rule_inputs=rules,
                allowed_rule_ids=tuple(s09_rule_id(span) for span in (2, 4, 8, 16, 32, 64)),
                fdm=s09_fdm_for_allowed_spans((2, 4, 8, 16, 32, 64)),
            )
        )

        self.assertTrue(all(rule.capped_forecast == 20.0 for rule in result.rule_results))
        self.assertEqual(result.final_forecast, 20.0)

    def test_m2_fails_closed_on_unresolved_or_invalid_source_atoms(self) -> None:
        rule = ForecastRuleInput(s09_rule_id(64), TimedValue(1.0, self.as_of), S09_EWMAC_SCALARS[64])
        with self.assertRaises(CarverBlocked):
            combine_forecast_block(
                ForecastBlockRequest(
                    completed_bar=self.completed_bar,
                    rule_inputs=(rule,),
                    allowed_rule_ids=(s09_rule_id(64),),
                    fdm=1.0,
                    speed_rule_status=SourceRuleStatus.UNRESOLVED,
                )
            )
        with self.assertRaises(CarverBlocked):
            combine_forecast_block(
                ForecastBlockRequest(
                    completed_bar=self.completed_bar,
                    rule_inputs=(replace(rule, scalar_status=SourceRuleStatus.UNRESOLVED),),
                    allowed_rule_ids=(s09_rule_id(64),),
                    fdm=1.0,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_fdm_for_allowed_spans((2, 64))
        with self.assertRaises(CarverBlocked):
            s09_rule_id(1)
        with self.assertRaises(CarverBlocked):
            combine_forecast_block(
                ForecastBlockRequest(
                    completed_bar=self.completed_bar,
                    rule_inputs=(rule,),
                    allowed_rule_ids=(s09_rule_id(64),),
                    fdm=1.0,
                    lane_class=LaneClass.CFD_ADAPTER,
                )
            )

    def test_s09_constructs_ewmac_forecasts_from_completed_daily_closes(self) -> None:
        bars = self.trend_bars()
        result = s09_multiple_trend_forecast(
            S09TrendForecastRequest(
                bars=bars,
                as_of=bars[-1].timestamp,
                daily_price_risk=TimedValue(10.0, bars[-1].timestamp),
                allowed_spans=(32, 64),
            )
        )

        self.assertEqual(result.contract_code, "MES")
        self.assertEqual(result.as_of, bars[-1].timestamp)
        self.assertEqual([forecast.span for forecast in result.rule_forecasts], [32, 64])
        self.assertEqual([rule.rule_id for rule in result.forecast_block.rule_results], ["EWMAC32", "EWMAC64"])
        self.assertGreater(result.rule_forecasts[0].fast_ewma, result.rule_forecasts[0].slow_ewma)
        self.assertGreater(result.final_forecast, 0.0)
        self.assertLessEqual(abs(result.final_forecast), 20.0)

    def test_s09_daily_price_risk_converts_annual_percentage_risk_to_price_points(self) -> None:
        risk = s09_daily_price_risk(
            S09DailyPriceRiskRequest(
                completed_bar=self.completed_bar,
                current_price=TimedValue(4000.0, self.as_of),
                annual_percentage_risk=TimedValue(0.16, self.as_of),
            )
        )

        self.assertEqual(risk.as_of, self.as_of)
        self.assertAlmostEqual(risk.value, 40.0)

    def test_s09_daily_price_risk_fails_closed_on_unlocked_or_misaligned_inputs(self) -> None:
        with self.assertRaises(CarverBlocked):
            s09_daily_price_risk(
                S09DailyPriceRiskRequest(
                    completed_bar=self.completed_bar,
                    current_price=TimedValue(4000.0, self.as_of),
                    annual_percentage_risk=TimedValue(0.16, self.as_of),
                    conversion_source_status=SourceRuleStatus.UNRESOLVED,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_daily_price_risk(
                S09DailyPriceRiskRequest(
                    completed_bar=self.completed_bar,
                    current_price=TimedValue(4000.0, self.as_of - timedelta(days=1)),
                    annual_percentage_risk=TimedValue(0.16, self.as_of),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_daily_price_risk(
                S09DailyPriceRiskRequest(
                    completed_bar=self.completed_bar,
                    current_price=TimedValue(4000.0, self.as_of),
                    annual_percentage_risk=TimedValue(0.16, self.as_of),
                    annualization_days=252,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_daily_price_risk(
                S09DailyPriceRiskRequest(
                    completed_bar=self.completed_bar,
                    current_price=TimedValue(4000.0, self.as_of),
                    annual_percentage_risk=TimedValue(0.16, self.as_of - timedelta(days=1)),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_daily_price_risk(
                S09DailyPriceRiskRequest(
                    completed_bar=self.completed_bar,
                    current_price=TimedValue(0.0, self.as_of),
                    annual_percentage_risk=TimedValue(0.16, self.as_of),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_daily_price_risk(
                S09DailyPriceRiskRequest(
                    completed_bar=self.completed_bar,
                    current_price=TimedValue(4000.0, self.as_of),
                    annual_percentage_risk=TimedValue(nan, self.as_of),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_daily_price_risk(
                S09DailyPriceRiskRequest(
                    completed_bar=self.completed_bar,
                    current_price=TimedValue(4000.0, self.as_of),
                    annual_percentage_risk=TimedValue(0.16, self.as_of),
                    lane_class=LaneClass.CFD_ADAPTER,
                )
            )

    def test_s09_rejects_incomplete_future_misaligned_or_mixed_contract_inputs(self) -> None:
        bars = self.trend_bars()
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=bars + (self.daily_bar(257, 300.0),),
                    as_of=bars[-1].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[-1].timestamp),
                    allowed_spans=(64,),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=bars[:-1],
                    as_of=bars[-1].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[-1].timestamp),
                    allowed_spans=(64,),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=bars,
                    as_of=bars[-1].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[-2].timestamp),
                    allowed_spans=(64,),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=bars[:-1] + (replace(bars[-1], contract=zn_contract()),),
                    as_of=bars[-1].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[-1].timestamp),
                    allowed_spans=(64,),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=tuple(replace(bar, completed_bar=replace(bar.completed_bar, is_complete=False)) for bar in bars),
                    as_of=bars[-1].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[-1].timestamp),
                    allowed_spans=(64,),
                )
            )

    def test_s09_fails_closed_until_synthetic_source_atoms_are_locked(self) -> None:
        bars = self.trend_bars()
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=bars,
                    as_of=bars[-1].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[-1].timestamp),
                    allowed_spans=(64,),
                    convention=S09SyntheticConvention(ewma_convention_status=SourceRuleStatus.UNRESOLVED),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=bars,
                    as_of=bars[-1].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[-1].timestamp),
                    allowed_spans=(64,),
                    convention=S09SyntheticConvention(speed_rule_status=SourceRuleStatus.UNRESOLVED),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=bars[:64],
                    as_of=bars[63].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[63].timestamp),
                    allowed_spans=(64,),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                S09TrendForecastRequest(
                    bars=bars,
                    as_of=bars[-1].timestamp,
                    daily_price_risk=TimedValue(10.0, bars[-1].timestamp),
                    allowed_spans=(64,),
                    lane_class=LaneClass.CFD_ADAPTER,
                )
            )

    def test_p05_shape_gate_is_process_only(self) -> None:
        path = ROOT / "docs" / "researchops" / "portfolios" / "CARVER_P05_JUMBO_MULTIPLE_TREND_PORTFOLIO_SHAPE_GATE_2026-05-29.md"
        text = path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_CARVER_P05_JUMBO_MULTIPLE_TREND_PORTFOLIO_SHAPE_NOT_DATA_NOT_BACKTEST", text)
        self.assertIn("S09 over a source-locked Jumbo futures universe", text)
        self.assertIn("authorizes no data access", text)


if __name__ == "__main__":
    unittest.main()

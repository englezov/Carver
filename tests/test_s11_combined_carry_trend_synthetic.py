from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CompletedBar, LaneClass, SourceRuleStatus, CarverBlocked  # noqa: E402
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m2 import FORECAST_CAP  # noqa: E402
from carver.spine.s11 import (  # noqa: E402
    S11_SOURCE_STYLE_WEIGHTS,
    S11CombinedCarryTrendConformanceRequest,
    S11CombinedCarryTrendSourceLocks,
    S11ForecastStyle,
    S11SyntheticForecastInput,
    s11_combined_carry_trend_conformance,
)


class S11CombinedCarryTrendSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.as_of = datetime(2026, 5, 29, tzinfo=timezone.utc)
        self.completed_bar = CompletedBar(self.as_of)

    def test_s11_combines_locked_synthetic_s09_and_s10_forecasts(self) -> None:
        result = s11_combined_carry_trend_conformance(self.request())

        self.assertEqual([rule.rule_id for rule in result.rule_results], ["EWMAC32", "EWMAC64", "Carry20", "Carry120"])
        self.assertEqual(result.rule_results[0].style, S11ForecastStyle.TREND)
        self.assertEqual(result.rule_results[2].style, S11ForecastStyle.CARRY)
        self.assertAlmostEqual(sum(rule.top_down_weight for rule in result.rule_results), 1.0)
        self.assertAlmostEqual(
            sum(rule.top_down_weight for rule in result.rule_results if rule.style is S11ForecastStyle.TREND),
            S11_SOURCE_STYLE_WEIGHTS[S11ForecastStyle.TREND],
        )
        self.assertAlmostEqual(
            sum(rule.top_down_weight for rule in result.rule_results if rule.style is S11ForecastStyle.CARRY),
            S11_SOURCE_STYLE_WEIGHTS[S11ForecastStyle.CARRY],
        )
        self.assertAlmostEqual(result.pre_fdm_forecast, 4.8)
        self.assertAlmostEqual(result.fdm, 1.2)
        self.assertAlmostEqual(result.post_fdm_forecast, 5.76)
        self.assertAlmostEqual(result.final_capped_s11_combined_forecast, 5.76)
        self.assertFalse(result.interpretable_trading_signal)
        self.assertEqual(result.performance_metrics, ())
        self.assertEqual(result.position_outputs, ())

    def test_s11_caps_final_combined_forecast(self) -> None:
        inputs = (
            self.input("EWMAC32", S11ForecastStyle.TREND, 20.0, style_weight=0.60, rule_weight=1.0),
            self.input("Carry120", S11ForecastStyle.CARRY, 20.0, style_weight=0.40, rule_weight=1.0),
        )
        result = s11_combined_carry_trend_conformance(
            self.request(forecast_inputs=inputs, eligible_rule_ids=("EWMAC32", "Carry120"), s11_fdm=2.0, fdm_rule_count=2)
        )

        self.assertEqual(result.pre_fdm_forecast, 20.0)
        self.assertGreater(result.post_fdm_forecast, FORECAST_CAP)
        self.assertEqual(result.final_capped_s11_combined_forecast, FORECAST_CAP)

    def test_s11_fails_closed_on_unresolved_locks_and_non_source_native_lane(self) -> None:
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(source_locks=replace(self.locks(), style_mix_status=SourceRuleStatus.UNRESOLVED))
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(source_locks=replace(self.locks(), output_boundary_status=SourceRuleStatus.UNRESOLVED))
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(self.request(lane_class=LaneClass.CFD_ADAPTER))

    def test_s11_fails_closed_on_input_status_label_timestamp_and_uncapped_values(self) -> None:
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("EWMAC32", S11ForecastStyle.TREND, 10.0, style_weight=0.60, rule_weight=1.0, label="production_s09"),
                        self.input("Carry120", S11ForecastStyle.CARRY, 5.0, style_weight=0.40, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("EWMAC32", "Carry120"),
                )
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("EWMAC32", S11ForecastStyle.TREND, 10.0, style_weight=0.60, rule_weight=1.0, status=SourceRuleStatus.UNRESOLVED),
                        self.input("Carry120", S11ForecastStyle.CARRY, 5.0, style_weight=0.40, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("EWMAC32", "Carry120"),
                )
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("EWMAC32", S11ForecastStyle.TREND, 10.0, style_weight=0.60, rule_weight=1.0, as_of=self.as_of - timedelta(days=1)),
                        self.input("Carry120", S11ForecastStyle.CARRY, 5.0, style_weight=0.40, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("EWMAC32", "Carry120"),
                )
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("EWMAC32", S11ForecastStyle.TREND, 25.0, style_weight=0.60, rule_weight=1.0),
                        self.input("Carry120", S11ForecastStyle.CARRY, 5.0, style_weight=0.40, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("EWMAC32", "Carry120"),
                )
            )

    def test_s11_fails_closed_on_style_weight_and_eligible_rule_drift(self) -> None:
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("EWMAC32", S11ForecastStyle.TREND, 10.0, style_weight=0.50, rule_weight=1.0),
                        self.input("Carry120", S11ForecastStyle.CARRY, 5.0, style_weight=0.50, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("EWMAC32", "Carry120"),
                )
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("EWMAC32", S11ForecastStyle.TREND, 10.0, style_weight=0.60, rule_weight=1.0),
                        self.input("Carry120", S11ForecastStyle.CARRY, 5.0, style_weight=0.40, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("Carry120", "EWMAC32"),
                )
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("EWMAC32", S11ForecastStyle.TREND, 10.0, style_weight=0.60, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("EWMAC32",),
                    fdm_rule_count=1,
                )
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("Carry20", S11ForecastStyle.TREND, 10.0, style_weight=0.60, rule_weight=1.0),
                        self.input("Carry120", S11ForecastStyle.CARRY, 5.0, style_weight=0.40, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("Carry20", "Carry120"),
                    fdm_rule_count=2,
                )
            )
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(
                self.request(
                    forecast_inputs=(
                        self.input("EWMAC32", "BAD_STYLE", 10.0, style_weight=0.60, rule_weight=1.0),  # type: ignore[arg-type]
                        self.input("Carry120", S11ForecastStyle.CARRY, 5.0, style_weight=0.40, rule_weight=1.0),
                    ),
                    eligible_rule_ids=("EWMAC32", "Carry120"),
                    fdm_rule_count=2,
                )
            )

    def test_s11_fails_closed_on_fdm_drift(self) -> None:
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(self.request(fdm_label="production_table_52"))
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(self.request(fdm_rule_count=3))
        with self.assertRaises(CarverBlocked):
            s11_combined_carry_trend_conformance(self.request(s11_fdm=0.0))

    def test_s11_conformance_doc_records_boundary(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S11_COMBINED_CARRY_TREND_CONFORMANCE_2026-05-29.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_CARVER_S11_COMBINED_CARRY_TREND_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST", text)
        self.assertIn("60/40", text)
        self.assertIn("final capped S11 combined carry/trend forecast output", text)
        self.assertIn("No real data", text)
        self.assertIn("no P05/P06/P07", text)

    def request(
        self,
        *,
        forecast_inputs: tuple[S11SyntheticForecastInput, ...] | None = None,
        eligible_rule_ids: tuple[str, ...] = ("EWMAC32", "EWMAC64", "Carry20", "Carry120"),
        s11_fdm: float = 1.2,
        fdm_rule_count: int = 4,
        fdm_label: str = "synthetic_s11_fdm_by_rule_count",
        source_locks: S11CombinedCarryTrendSourceLocks | None = None,
        lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
    ) -> S11CombinedCarryTrendConformanceRequest:
        return S11CombinedCarryTrendConformanceRequest(
            completed_bar=self.completed_bar,
            forecast_inputs=forecast_inputs
            or (
                self.input("EWMAC32", S11ForecastStyle.TREND, 10.0, style_weight=0.60, rule_weight=0.5),
                self.input("EWMAC64", S11ForecastStyle.TREND, 4.0, style_weight=0.60, rule_weight=0.5),
                self.input("Carry20", S11ForecastStyle.CARRY, 5.0, style_weight=0.40, rule_weight=0.5),
                self.input("Carry120", S11ForecastStyle.CARRY, -2.0, style_weight=0.40, rule_weight=0.5),
            ),
            eligible_rule_ids=eligible_rule_ids,
            s11_fdm=s11_fdm,
            fdm_rule_count=fdm_rule_count,
            fdm_label=fdm_label,
            source_locks=source_locks or self.locks(),
            lane_class=lane_class,
        )

    def input(
        self,
        rule_id: str,
        style: S11ForecastStyle,
        value: float,
        *,
        style_weight: float,
        rule_weight: float,
        variation_weight: float = 1.0,
        label: str | None = None,
        status: SourceRuleStatus = SourceRuleStatus.LOCKED,
        weight_status: SourceRuleStatus = SourceRuleStatus.LOCKED,
        as_of: datetime | None = None,
    ) -> S11SyntheticForecastInput:
        default_label = "synthetic_s09_forecast_block_output" if style is S11ForecastStyle.TREND else "synthetic_s10_forecast_block_output"
        return S11SyntheticForecastInput(
            label=label or default_label,
            rule_id=rule_id,
            style=style,
            capped_forecast=TimedValue(value, as_of or self.as_of),
            input_status=status,
            style_weight=style_weight,
            rule_weight=rule_weight,
            variation_weight=variation_weight,
            weight_status=weight_status,
        )

    def locks(self) -> S11CombinedCarryTrendSourceLocks:
        return S11CombinedCarryTrendSourceLocks(
            s09_input_provenance_status=SourceRuleStatus.LOCKED,
            s10_input_provenance_status=SourceRuleStatus.LOCKED,
            style_grouping_status=SourceRuleStatus.LOCKED,
            style_mix_status=SourceRuleStatus.LOCKED,
            top_down_weight_status=SourceRuleStatus.LOCKED,
            eligible_rule_set_status=SourceRuleStatus.LOCKED,
            fdm_status=SourceRuleStatus.LOCKED,
            combined_cap_status=SourceRuleStatus.LOCKED,
            output_boundary_status=SourceRuleStatus.LOCKED,
        )


if __name__ == "__main__":
    unittest.main()

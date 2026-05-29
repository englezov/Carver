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
from carver.spine.s10 import (  # noqa: E402
    S10_CARRY_SCALAR,
    S10CarryForecastBlockRequest,
    S10CarryForecastBlockSourceLocks,
    S10M5RiskAdjustedCarryInput,
    s10_carry_fdm_for_eligible_spans,
    s10_carry_forecast_block_conformance,
    s10_carry_rule_id,
)


class S10CarryForecastBlockSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.start = datetime(2026, 1, 30, tzinfo=timezone.utc)
        self.as_of = self.start + timedelta(days=119)
        self.completed_bar = CompletedBar(self.as_of)

    def test_s10_constructs_final_capped_carry_forecast_from_locked_m5_inputs(self) -> None:
        request = self.request(values=(0.2,) * 120, eligible_spans=(5, 20, 60, 120))

        result = s10_carry_forecast_block_conformance(request)

        self.assertEqual([forecast.rule_id for forecast in result.span_forecasts], ["Carry5", "Carry20", "Carry60", "Carry120"])
        self.assertEqual([rule.weight for rule in result.forecast_block.rule_results], [0.25, 0.25, 0.25, 0.25])
        self.assertTrue(all(rule.scalar == S10_CARRY_SCALAR for rule in result.forecast_block.rule_results))
        for rule in result.forecast_block.rule_results:
            self.assertAlmostEqual(rule.scaled_forecast, 6.0)
        self.assertAlmostEqual(result.forecast_block.pre_fdm_forecast, 6.0)
        self.assertAlmostEqual(result.forecast_block.fdm, 1.04)
        self.assertAlmostEqual(result.forecast_block.post_fdm_forecast, 6.24)
        self.assertAlmostEqual(result.final_capped_s10_carry_forecast, 6.24)
        self.assertFalse(result.interpretable_trading_signal)
        self.assertEqual(result.performance_metrics, ())
        self.assertEqual(result.position_outputs, ())

    def test_s10_smooths_each_eligible_span_before_m2_scaling(self) -> None:
        values = tuple(index / 100.0 for index in range(120))
        result = s10_carry_forecast_block_conformance(self.request(values=values, eligible_spans=(60, 120)))

        expected_60 = self.synthetic_ewma(values, 60)
        expected_120 = self.synthetic_ewma(values, 120)
        self.assertAlmostEqual(result.span_forecasts[0].smoothed_risk_adjusted_carry, expected_60)
        self.assertAlmostEqual(result.span_forecasts[1].smoothed_risk_adjusted_carry, expected_120)
        self.assertAlmostEqual(result.forecast_block.rule_results[0].scaled_forecast, expected_60 * 30.0)
        self.assertAlmostEqual(result.forecast_block.rule_results[1].scaled_forecast, expected_120 * 30.0)
        self.assertAlmostEqual(result.forecast_block.fdm, 1.02)

    def test_s10_caps_individual_and_final_forecasts_through_m2(self) -> None:
        result = s10_carry_forecast_block_conformance(self.request(values=(1.0,) * 120))

        self.assertTrue(all(rule.scaled_forecast == 30.0 for rule in result.forecast_block.rule_results))
        self.assertTrue(all(rule.capped_forecast == FORECAST_CAP for rule in result.forecast_block.rule_results))
        self.assertGreater(result.forecast_block.post_fdm_forecast, FORECAST_CAP)
        self.assertEqual(result.final_capped_s10_carry_forecast, FORECAST_CAP)

    def test_s10_locks_allowed_fdm_rows_and_rule_ids(self) -> None:
        self.assertEqual(s10_carry_rule_id(5), "Carry5")
        self.assertEqual(s10_carry_fdm_for_eligible_spans((20, 60, 120)), 1.03)
        self.assertEqual(s10_carry_fdm_for_eligible_spans((60, 120)), 1.02)
        self.assertEqual(s10_carry_fdm_for_eligible_spans((120,)), 1.0)
        with self.assertRaises(CarverBlocked):
            s10_carry_rule_id(40)
        with self.assertRaises(CarverBlocked):
            s10_carry_fdm_for_eligible_spans((5, 60, 120))
        with self.assertRaises(CarverBlocked):
            s10_carry_fdm_for_eligible_spans(())

    def test_s10_fails_closed_on_unresolved_source_locks_and_non_source_native_lane(self) -> None:
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(
                self.request(source_locks=replace(self.locks(), scalar_status=SourceRuleStatus.UNRESOLVED))
            )
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(
                self.request(source_locks=replace(self.locks(), output_boundary_status=SourceRuleStatus.UNRESOLVED))
            )
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(self.request(lane_class=LaneClass.CFD_ADAPTER))
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(
                self.request(input_status=SourceRuleStatus.UNRESOLVED)
            )

    def test_s10_fails_closed_on_history_timestamp_and_label_drift(self) -> None:
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(self.request(values=(0.2,) * 119, eligible_spans=(120,)))
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(
                self.request(as_of=self.as_of - timedelta(days=1))
            )
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(
                self.request(timestamp_offset={40: timedelta(days=-1)})
            )
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(
                self.request(timestamp_offset={40: timedelta(days=1)})
            )
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(
                self.request(timestamp_offset={40: timedelta(hours=12)})
            )
        with self.assertRaises(CarverBlocked):
            s10_carry_forecast_block_conformance(
                self.request(label="production_m5_carry")
            )

    def test_s10_conformance_doc_records_boundary(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_2026-05-29.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST", text)
        self.assertIn("Carry5/20/60/120", text)
        self.assertIn("scalar 30", text)
        self.assertIn("carry FDM", text)
        self.assertIn("No real-data execution", text)
        self.assertIn("no S11", text)

    def request(
        self,
        *,
        values: tuple[float, ...] = (0.2,) * 120,
        eligible_spans: tuple[int, ...] = (5, 20, 60, 120),
        source_locks: S10CarryForecastBlockSourceLocks | None = None,
        lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
        as_of: datetime | None = None,
        input_status: SourceRuleStatus = SourceRuleStatus.LOCKED,
        label: str = "synthetic_m5_risk_adjusted_carry",
        timestamp_offset: dict[int, timedelta] | None = None,
    ) -> S10CarryForecastBlockRequest:
        offsets = timestamp_offset or {}
        inputs = tuple(
            S10M5RiskAdjustedCarryInput(
                label=label,
                risk_adjusted_carry=TimedValue(value, self.start + timedelta(days=index) + offsets.get(index, timedelta())),
                status=input_status,
            )
            for index, value in enumerate(values)
        )
        return S10CarryForecastBlockRequest(
            completed_bar=CompletedBar(as_of or self.as_of),
            m5_carry_inputs=inputs,
            eligible_spans=eligible_spans,
            source_locks=source_locks or self.locks(),
            lane_class=lane_class,
        )

    def locks(self) -> S10CarryForecastBlockSourceLocks:
        return S10CarryForecastBlockSourceLocks(
            m5_input_provenance_status=SourceRuleStatus.LOCKED,
            input_history_status=SourceRuleStatus.LOCKED,
            smoothing_span_status=SourceRuleStatus.LOCKED,
            scalar_status=SourceRuleStatus.LOCKED,
            cap_status=SourceRuleStatus.LOCKED,
            eligibility_status=SourceRuleStatus.LOCKED,
            weight_status=SourceRuleStatus.LOCKED,
            fdm_status=SourceRuleStatus.LOCKED,
            output_boundary_status=SourceRuleStatus.LOCKED,
        )

    def synthetic_ewma(self, values: tuple[float, ...], span: int) -> float:
        alpha = 2.0 / (span + 1.0)
        smoothed = values[0]
        for value in values[1:]:
            smoothed = alpha * value + (1.0 - alpha) * smoothed
        return smoothed


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import sys
import unittest
import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.daily_bars import CompletedDailyMarketBar  # noqa: E402
from carver.spine.m0 import CompletedBar, LaneClass, SourceRuleStatus, CarverBlocked  # noqa: E402
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m2 import (  # noqa: E402
    FORECAST_CAP,
    S09_EWMAC_FDM_ROWS,
    S09_EWMAC_SCALARS,
    S09_EWMAC_SPANS,
    s09_fdm_for_allowed_spans,
)
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402
from carver.spine.s09 import S09SyntheticConvention, S09TrendForecastRequest, s09_multiple_trend_forecast  # noqa: E402


EXPECTED_S09_SPANS = (2, 4, 8, 16, 32, 64)
EXPECTED_S09_SCALARS = {
    2: 12.1,
    4: 8.53,
    8: 5.95,
    16: 4.10,
    32: 2.79,
    64: 1.91,
}
EXPECTED_S09_FDM_ROWS = {
    (2, 4, 8, 16, 32, 64): 1.26,
    (4, 8, 16, 32, 64): 1.19,
    (8, 16, 32, 64): 1.13,
    (16, 32, 64): 1.08,
    (32, 64): 1.03,
    (64,): 1.0,
}


class S09FullSourceAtomSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.start = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def daily_bar(self, index: int, close: float, *, contract=None, complete: bool = True) -> CompletedDailyMarketBar:
        return CompletedDailyMarketBar(
            completed_bar=CompletedBar(self.start + timedelta(days=index), is_complete=complete),
            contract=contract or mes_contract(),
            contract_month="06-26",
            open=close,
            high=close + 0.75,
            low=close - 0.75,
            close=close,
            volume=1000.0 + index,
        )

    def bars_from_closes(self, closes: tuple[float, ...]) -> tuple[CompletedDailyMarketBar, ...]:
        return tuple(self.daily_bar(index, close) for index, close in enumerate(closes))

    def request(
        self,
        closes: tuple[float, ...],
        *,
        spans: tuple[int, ...] = EXPECTED_S09_SPANS,
        daily_price_risk: float = 10.0,
        convention: S09SyntheticConvention = S09SyntheticConvention(),
        lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
    ) -> S09TrendForecastRequest:
        bars = self.bars_from_closes(closes)
        return S09TrendForecastRequest(
            bars=bars,
            as_of=bars[-1].timestamp,
            daily_price_risk=TimedValue(daily_price_risk, bars[-1].timestamp),
            allowed_spans=spans,
            convention=convention,
            lane_class=lane_class,
        )

    def test_full_six_speed_uptrend_matches_independent_ewma_math(self) -> None:
        closes = tuple(100.0 + index * 0.5 for index in range(260))

        result = s09_multiple_trend_forecast(self.request(closes))

        self.assertEqual(S09_EWMAC_SPANS, EXPECTED_S09_SPANS)
        self.assertEqual(S09_EWMAC_SCALARS, EXPECTED_S09_SCALARS)
        self.assertEqual(S09_EWMAC_FDM_ROWS, EXPECTED_S09_FDM_ROWS)
        self.assertEqual(tuple(rule.span for rule in result.rule_forecasts), EXPECTED_S09_SPANS)
        self.assertEqual(result.forecast_block.fdm, EXPECTED_S09_FDM_ROWS[EXPECTED_S09_SPANS])
        self.assertLessEqual(abs(result.final_forecast), FORECAST_CAP)
        for rule in result.rule_forecasts:
            expected_fast = self.recursive_ewma(closes, rule.fast_span)
            expected_slow = self.recursive_ewma(closes, rule.slow_span)
            expected_raw = (expected_fast - expected_slow) / 10.0
            self.assertAlmostEqual(rule.fast_ewma, expected_fast)
            self.assertAlmostEqual(rule.slow_ewma, expected_slow)
            self.assertAlmostEqual(rule.raw_forecast, expected_raw)
            self.assertEqual(rule.scalar, EXPECTED_S09_SCALARS[rule.span])
            self.assertGreater(rule.raw_forecast, 0.0)
            expected_scaled = rule.raw_forecast * EXPECTED_S09_SCALARS[rule.span]
            expected_capped = self.cap(expected_scaled)
            block_rule = next(block_rule for block_rule in result.forecast_block.rule_results if block_rule.rule_id == f"EWMAC{rule.span}")
            self.assertAlmostEqual(block_rule.scaled_forecast, expected_scaled)
            self.assertAlmostEqual(rule.capped_forecast, expected_capped)
            self.assertAlmostEqual(block_rule.capped_forecast, expected_capped)
        expected_pre_fdm = sum(
            self.cap(rule.raw_forecast * EXPECTED_S09_SCALARS[rule.span])
            for rule in result.rule_forecasts
        ) / len(EXPECTED_S09_SPANS)
        self.assertAlmostEqual(result.forecast_block.pre_fdm_forecast, expected_pre_fdm)
        self.assertAlmostEqual(result.forecast_block.post_fdm_forecast, expected_pre_fdm * 1.26)

    def test_downtrend_and_flat_paths_have_source_expected_signs(self) -> None:
        down = tuple(300.0 - index * 0.4 for index in range(260))
        flat = tuple(150.0 for _ in range(260))

        down_result = s09_multiple_trend_forecast(self.request(down))
        flat_result = s09_multiple_trend_forecast(self.request(flat))

        self.assertTrue(all(rule.raw_forecast < 0.0 for rule in down_result.rule_forecasts))
        self.assertLess(down_result.final_forecast, 0.0)
        for rule in flat_result.rule_forecasts:
            self.assertAlmostEqual(rule.raw_forecast, 0.0, places=12)
        self.assertAlmostEqual(flat_result.final_forecast, 0.0, places=12)

    def test_all_locked_fdm_rows_execute_through_full_s09_forecast_path(self) -> None:
        closes = tuple(100.0 + index * 0.5 for index in range(260))
        for spans, expected_fdm in EXPECTED_S09_FDM_ROWS.items():
            with self.subTest(spans=spans):
                self.assertEqual(s09_fdm_for_allowed_spans(spans), expected_fdm)
                result = s09_multiple_trend_forecast(self.request(closes, spans=spans))
                self.assertEqual(tuple(rule.span for rule in result.rule_forecasts), spans)
                self.assertEqual(tuple(rule.rule_id for rule in result.forecast_block.rule_results), tuple(f"EWMAC{span}" for span in spans))
                self.assertEqual(tuple(rule.weight for rule in result.forecast_block.rule_results), tuple(1.0 / len(spans) for _ in spans))
                self.assertEqual(result.forecast_block.fdm, expected_fdm)
                for rule in result.rule_forecasts:
                    self.assertEqual(rule.scalar, EXPECTED_S09_SCALARS[rule.span])
                    self.assertLessEqual(abs(rule.capped_forecast), FORECAST_CAP)
                    expected_scaled = rule.raw_forecast * EXPECTED_S09_SCALARS[rule.span]
                    block_rule = next(block_rule for block_rule in result.forecast_block.rule_results if block_rule.rule_id == f"EWMAC{rule.span}")
                    self.assertAlmostEqual(block_rule.scaled_forecast, expected_scaled)
                    self.assertAlmostEqual(block_rule.capped_forecast, self.cap(expected_scaled))
                expected_pre_fdm = sum(
                    self.cap(rule.raw_forecast * EXPECTED_S09_SCALARS[rule.span])
                    for rule in result.rule_forecasts
                ) / len(spans)
                self.assertAlmostEqual(result.forecast_block.pre_fdm_forecast, expected_pre_fdm)
                self.assertAlmostEqual(result.forecast_block.post_fdm_forecast, expected_pre_fdm * expected_fdm)
                self.assertAlmostEqual(result.final_forecast, self.cap(expected_pre_fdm * expected_fdm))
                self.assertLessEqual(abs(result.final_forecast), FORECAST_CAP)

        for invalid in ((2, 64), (2, 4, 16, 32, 64), (64, 32), (2, 2), (3,), ()):
            with self.subTest(invalid=invalid):
                with self.assertRaises(CarverBlocked):
                    s09_fdm_for_allowed_spans(invalid)

    def test_individual_and_combined_forecasts_cap_at_both_source_limits(self) -> None:
        up_closes = tuple(100.0 + index * 8.0 for index in range(260))
        down_closes = tuple(3000.0 - index * 8.0 for index in range(260))

        up_result = s09_multiple_trend_forecast(self.request(up_closes, daily_price_risk=0.01))
        down_result = s09_multiple_trend_forecast(self.request(down_closes, daily_price_risk=0.01))

        self.assertTrue(all(rule.capped_forecast == FORECAST_CAP for rule in up_result.rule_forecasts))
        self.assertGreater(up_result.forecast_block.post_fdm_forecast, FORECAST_CAP)
        self.assertEqual(up_result.final_forecast, FORECAST_CAP)
        self.assertTrue(all(rule.capped_forecast == -FORECAST_CAP for rule in down_result.rule_forecasts))
        self.assertLess(down_result.forecast_block.post_fdm_forecast, -FORECAST_CAP)
        self.assertEqual(down_result.final_forecast, -FORECAST_CAP)

    def test_s09_full_synthetic_gate_fails_closed_on_governance_and_input_drift(self) -> None:
        closes = tuple(100.0 + index * 0.2 for index in range(260))
        bars = self.bars_from_closes(closes)

        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(self.request(closes, lane_class=LaneClass.CFD_ADAPTER))
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                self.request(
                    closes,
                    convention=S09SyntheticConvention(scalar_status=SourceRuleStatus.UNRESOLVED),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                replace(
                    self.request(closes),
                    bars=bars[:-1] + (replace(bars[-1], contract=zn_contract()),),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                replace(
                    self.request(closes),
                    bars=bars[:-1] + (self.daily_bar(len(bars) - 1, closes[-1], complete=False),),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                replace(
                    self.request(closes),
                    bars=bars + (self.daily_bar(len(bars), 180.0),),
                    as_of=bars[-1].timestamp,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_multiple_trend_forecast(
                replace(
                    self.request(closes),
                    daily_price_risk=TimedValue(10.0, bars[-2].timestamp),
                )
            )

    def test_gate_document_preserves_synthetic_only_boundary(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_SOURCE_ATOM_LOCK_AND_SYNTHETIC_CONFORMANCE_GATE_2026-06-02.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_S09_SOURCE_ATOM_LOCK_NOT_DATA_NOT_BACKTEST", text)
        self.assertIn("EWMAC speed set", text)
        self.assertIn("Table 36", text)
        self.assertIn("provider access", text)
        self.assertIn("Databento or NinjaTrader usage", text)
        self.assertIn("backtests", text)
        self.assertIn("CFD adapter work", text)

    def test_data_backtest_readiness_gate_stays_process_only_and_index_native(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_DEV_RECON_DATA_BACKTEST_READINESS_GATE_2026-06-02.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_DEV_RECON_DATA_BACKTEST_READINESS_GATE_NOT_DATA_NOT_BACKTEST", text)
        self.assertIn("MES  - S&P 500 micro", text)
        self.assertIn("MNQ  - Nasdaq 100 micro", text)
        self.assertIn("ES` or `NQ` may not silently substitute", text)
        self.assertIn("YES_DEV_RECON_DATA_READY_NOT_STRATEGY_READY", text)
        self.assertIn("lifecycle evidence was not locked", text)
        self.assertIn("S09_SINGLE_INDEX_ROOT_CONTINUOUS_LINEAGE_AND_COST_ELIGIBILITY_PREFLIGHT", text)
        self.assertIn("authorizes no provider API access", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no backtests", text)
        self.assertIn("no CFD adapter work", text)

    def test_mes_preflight_fails_closed_before_data_expansion(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_SINGLE_INDEX_ROOT_CONTINUOUS_LINEAGE_AND_COST_ELIGIBILITY_PREFLIGHT_2026-06-02.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_PREFLIGHT_FAIL_CLOSED_NOT_DATA_NOT_BACKTEST", text)
        self.assertIn("SELECTED_ROOT: MES", text)
        self.assertIn("No `ES` or `NQ` substitution is authorized", text)
        self.assertIn("2025-04-09", text)
        self.assertIn("2026-05-29", text)
        self.assertIn("MES_CONTINUOUS_LINEAGE_BLOCKED_LIFECYCLE_EVIDENCE_REQUIRED", text)
        self.assertIn("annual_percentage_risk source", text)
        self.assertIn("MES_COST_SOURCE: NOT_LOCKED", text)
        self.assertIn("MES_SPEED_COST_ELIGIBILITY: NOT_LOCKED", text)
        self.assertIn("S09_MES_DEV_RECON_DATA_EXPANSION_AND_LINEAGE_REPAIR_GATE", text)
        self.assertIn("authorizes no provider API access", text)
        self.assertIn("no new data download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no backtests", text)
        self.assertIn("no CFD adapter work", text)
        self.assertIn("no remote operations", text)

    def test_mes_data_expansion_result_stays_quarantine_only(self) -> None:
        gate_text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_DEV_RECON_DATA_EXPANSION_AND_LINEAGE_REPAIR_GATE_2026-06-02.md"
        ).read_text(encoding="utf-8")
        result_text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_DEV_RECON_DATA_EXPANSION_RESULT_2026-06-02.md"
        ).read_text(encoding="utf-8")
        status_text = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_dev_recon_data_expansion"
            / "2022-01-03_2023-12-29"
            / "status"
            / "20260602_S09_MES_DEV_RECON_DAILY_EXPANSION_status.json"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_SOURCE_S09_MES_DATABENTO_DAILY_EXPANSION_AUTHORIZED_NOT_BACKTEST", gate_text)
        self.assertIn("DATABENTO_ACCESS_ALLOWED_ONLY_FOR_S09_MES_DAILY_EXPANSION_GATE", gate_text)
        self.assertIn("MESZ3", gate_text)
        self.assertIn("MESH4", gate_text)
        self.assertIn("no continuous-contract download", gate_text)
        self.assertIn("no real-data forecast computation", gate_text)
        self.assertIn("PASS_S09_MES_DAILY_EXPANSION_QUARANTINE_ONLY_NOT_LINEAGE_NOT_BACKTEST", result_text)
        self.assertIn("provider_errors: 0", result_text)
        self.assertIn("target_window_rows: 2065", result_text)
        self.assertIn("forecast_computation: NO", result_text)
        self.assertIn("backtests_run: NO", result_text)
        self.assertIn("S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_EXECUTION_GATE", result_text)
        self.assertIn('"status": "PASS_S09_MES_DAILY_EXPANSION_QUARANTINE_ONLY_NOT_LINEAGE_NOT_BACKTEST"', status_text)
        self.assertIn('"continuous_lineage_constructed": "NO"', status_text)
        self.assertIn('"backtests_run": "NO"', status_text)

    def test_mes_data_expansion_artifacts_have_coherent_error_and_hash_state(self) -> None:
        artifact_root = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_dev_recon_data_expansion"
            / "2022-01-03_2023-12-29"
        )
        active_provider_errors = (
            artifact_root
            / "status"
            / "20260602_S09_MES_DEV_RECON_DAILY_EXPANSION_provider_errors.csv"
        )
        hash_path = (
            artifact_root
            / "hashes"
            / "20260602_S09_MES_DEV_RECON_DAILY_EXPANSION_sha256.json"
        )
        hash_payload = json.loads(hash_path.read_text(encoding="utf-8"))

        self.assertFalse(active_provider_errors.exists())
        self.assertNotIn(str(hash_path.relative_to(ROOT)), hash_payload)
        self.assertIn(
            "docs\\researchops\\s09\\mes_dev_recon_data_expansion\\2022-01-03_2023-12-29\\status\\20260602_S09_MES_DEV_RECON_DAILY_EXPANSION_status.json",
            hash_payload,
        )

    def test_mes_continuous_lineage_risk_cost_shape_gate_blocks_execution(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_SHAPE_GATE_2026-06-02.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_SHAPE_NOT_EXECUTION_NOT_BACKTEST", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("MESH1", text)
        self.assertIn("MESH4", text)
        self.assertIn("S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_EXECUTION_GATE", text)
        self.assertIn("STATIC_LIFECYCLE_BUFFER_ROLL", text)
        self.assertIn("ES/NQ/full-size substitute rows", text)
        self.assertIn("LOCAL_ADDITIVE_BACK_ADJUSTMENT_OLD_HISTORY_TO_NEW_CONTRACT_LEVEL", text)
        self.assertIn("daily_price_risk = current_price * annual_percentage_risk / 16", text)
        self.assertIn("0.15 SR threshold", text)
        self.assertIn("eligible EWMAC speed set", text)
        self.assertIn("S09 cannot assume all six EWMAC speeds survive real-data cost filtering", text)
        self.assertIn("no provider API access", text)
        self.assertIn("no new data download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no continuous lineage construction", text)
        self.assertIn("no cost execution", text)
        self.assertIn("no S09 forecast computation", text)
        self.assertIn("no diagnostics", text)
        self.assertIn("no backtests", text)
        self.assertIn("no positions", text)
        self.assertIn("no CFD adapter work", text)
        self.assertIn("no Git staging", text)
        self.assertIn("no remote repository operations", text)

    def recursive_ewma(self, values: tuple[float, ...], span: int) -> float:
        alpha = 2.0 / (span + 1.0)
        average = values[0]
        for value in values[1:]:
            average = alpha * value + (1.0 - alpha) * average
        return average

    def cap(self, value: float) -> float:
        return min(max(value, -FORECAST_CAP), FORECAST_CAP)


if __name__ == "__main__":
    unittest.main()

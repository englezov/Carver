from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "databento" / "carver_s09_mes_test_window_backtest.py"
SPEC = importlib.util.spec_from_file_location("carver_s09_mes_test_window_backtest", SCRIPT)
assert SPEC is not None
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def _sample_dates(start: date, end: date, count: int) -> list[str]:
    days = []
    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)
    if count > len(days):
        raise AssertionError("sample count exceeds available calendar span")
    if count == 1:
        return [start.isoformat()]
    interior = [item for item in days[1:-1]][: count - 2]
    return [start.isoformat(), *[item.isoformat() for item in interior], end.isoformat()]


class S09MESTestWindowBacktestGuardTests(unittest.TestCase):
    def locked_config(self):
        return MODULE.S09MESTestWindowBacktestConfig(
            execution_authorized=True,
            databento_download_authorized=False,
            exactly_one_backtest_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2020-04-06",
            window_end="2022-02-08",
            existing_test_download_authorized=True,
        )

    def test_preflight_accepts_only_locked_test_window_when_no_receipt_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(MODULE, "OUTPUT_ROOT", Path(tmp)):
                result = MODULE.run_s09_mes_test_window_backtest_preflight(self.locked_config())

        self.assertEqual(result["status"], "AUTHORIZED_READY_FOR_EXACTLY_ONE_TEST_BACKTEST")
        self.assertEqual(result["window_start"], "2020-04-06")
        self.assertEqual(result["window_end"], "2022-02-08")

    def test_preflight_fails_closed_on_missing_authorization_or_wrong_boundary(self) -> None:
        for bad_config in (
            replace(self.locked_config(), execution_authorized=False),
            replace(self.locked_config(), databento_download_authorized=True),
            replace(self.locked_config(), existing_test_download_authorized=False),
            replace(self.locked_config(), exactly_one_backtest_authorized=False),
            replace(self.locked_config(), lane_class="CFD_ADAPTER"),
            replace(self.locked_config(), root="ES"),
            replace(self.locked_config(), row_id="APPENDIX_C_174_002"),
            replace(self.locked_config(), window_start="2020-04-05"),
            replace(self.locked_config(), window_end="2022-02-09"),
        ):
            with self.subTest(bad_config=bad_config):
                with self.assertRaises(MODULE.CarverBlocked):
                    MODULE.run_s09_mes_test_window_backtest_preflight(bad_config)

    def test_preflight_refuses_second_backtest_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "status" / f"{MODULE.RUN_ID}_backtest_execution_receipt.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_text("{}\n", encoding="utf-8")
            with patch.object(MODULE, "OUTPUT_ROOT", Path(tmp)):
                with self.assertRaises(MODULE.CarverBlocked):
                    MODULE.run_s09_mes_test_window_backtest_preflight(self.locked_config())

    def test_preflight_ignores_superseded_diagnostic_receipt_but_keeps_clean_rerun_guard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            old_receipt = (
                Path(tmp)
                / "status"
                / f"{MODULE.ORIGINAL_DIAGNOSTIC_TEST_RUN_ID}_backtest_execution_receipt.json"
            )
            old_receipt.parent.mkdir(parents=True)
            old_receipt.write_text("{}\n", encoding="utf-8")

            with patch.object(MODULE, "OUTPUT_ROOT", Path(tmp)):
                result = MODULE.run_s09_mes_test_window_backtest_preflight(self.locked_config())

        self.assertEqual(result["status"], "AUTHORIZED_READY_FOR_EXACTLY_ONE_TEST_BACKTEST")

    def test_direct_databento_download_helper_is_quarantined(self) -> None:
        with self.assertRaises(MODULE.CarverBlocked):
            MODULE._download_compute_and_write_artifacts()

    def test_existing_download_path_does_not_write_manifest_before_remediation_guards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            state_sanitized = (
                state_root
                / "sanitized_daily_bars"
                / f"{MODULE.MACHINERY_DEV_RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
            )
            state_definitions = (
                state_root
                / "raw_provider_metadata"
                / f"{MODULE.MACHINERY_DEV_RUN_ID}_definition_ledger.csv"
            )
            sanitized = (
                root
                / "sanitized_daily_bars"
                / f"{MODULE.ORIGINAL_DIAGNOSTIC_TEST_RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
            )
            definitions = (
                root
                / "raw_provider_metadata"
                / f"{MODULE.ORIGINAL_DIAGNOSTIC_TEST_RUN_ID}_definition_ledger.csv"
            )
            state_sanitized.parent.mkdir(parents=True)
            state_definitions.parent.mkdir(parents=True)
            sanitized.parent.mkdir(parents=True)
            definitions.parent.mkdir(parents=True)
            state_sanitized.write_text("raw_symbol,provider_ts_event_utc\n", encoding="utf-8")
            state_definitions.write_text("raw_symbol\n", encoding="utf-8")
            sanitized.write_text("raw_symbol,provider_ts_event_utc\n", encoding="utf-8")
            definitions.write_text("raw_symbol\n", encoding="utf-8")
            manifest = root / "manifest" / f"{MODULE.RUN_ID}_existing_download_backtest_manifest.json"

            with (
                patch.object(MODULE, "OUTPUT_ROOT", root),
                patch.object(MODULE, "MACHINERY_DEV_OUTPUT_ROOT", state_root),
                patch.object(MODULE, "_read_csv_rows", return_value=[]),
                patch.object(MODULE, "_apply_cold_degraded_ohlcv_policy", return_value=[]),
                patch.object(MODULE, "_definitions_from_existing_ledgers", return_value={}),
                patch.object(
                    MODULE,
                    "_compute_and_write_backtest_artifacts",
                    side_effect=MODULE.CarverBlocked("blocked before artifact writes"),
                ),
            ):
                with self.assertRaises(MODULE.CarverBlocked):
                    MODULE._compute_from_existing_authorized_test_download()

            self.assertFalse(manifest.exists())

    def test_degraded_ohlcv_policy_is_cold_shape_based_not_date_specific(self) -> None:
        self.assertEqual(
            MODULE._provider_condition_classification("AVAILABLE", date(2020, 6, 30)),
            "NORMAL_PROVIDER_CONDITION",
        )
        self.assertEqual(
            MODULE._provider_condition_classification("DEGRADED", date(2020, 6, 30)),
            "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY",
        )
        self.assertEqual(
            MODULE._provider_condition_classification("DEGRADED", date(2020, 6, 29)),
            "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY",
        )
        self.assertEqual(
            MODULE._provider_condition_classification("UNKNOWN", date(2020, 6, 30)),
            "DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY",
        )

    def test_cold_degraded_ohlcv_policy_reclassifies_existing_rows_without_overlay_file(self) -> None:
        rows = [
            {
                "completed_trading_date": "2021-12-05",
                "raw_symbol": "MESM0",
                "source_raw_sha256": "HASH",
                "provider_condition": "DEGRADED",
                "provider_condition_classification": "DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY",
                "open": "100",
                "high": "101",
                "low": "99",
                "close": "100",
                "volume": "1",
            },
            {
                "completed_trading_date": "2020-06-30",
                "raw_symbol": "MESM0",
                "source_raw_sha256": "HASH",
                "provider_condition": "UNKNOWN",
                "provider_condition_classification": "DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY",
                "open": "100",
                "high": "101",
                "low": "99",
                "close": "100",
                "volume": "1",
            },
        ]

        patched = MODULE._apply_cold_degraded_ohlcv_policy(rows)

        self.assertEqual(
            patched[0]["provider_condition_classification"],
            "DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY",
        )
        self.assertEqual(
            patched[0]["completed_trading_date_policy"],
            "SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE",
        )
        self.assertEqual(
            patched[0]["provider_condition_admission_policy"],
            "SOURCE_NATIVE_DEGRADED_OHLCV_COLD_SHAPE_BASED_POLICY_LOCKED",
        )
        self.assertEqual(patched[0]["strategy_readiness_status"], "SOURCE_NATIVE_DEGRADED_TEST_INPUT_COLD_SHAPE_POLICY_ADMITTED")
        self.assertEqual(patched[1]["provider_condition_admission_policy"], "QUARANTINED_NOT_STRATEGY_INPUT")

    def test_cold_degraded_ohlcv_policy_rejects_bad_shape(self) -> None:
        rows = [
            {
                "completed_trading_date": "2020-06-29",
                "raw_symbol": "MESM0",
                "source_raw_sha256": "HASH",
                "provider_condition": "DEGRADED",
                "provider_condition_classification": "DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY",
                "open": "100",
                "high": "99",
                "low": "98",
                "close": "100",
                "volume": "1",
            },
        ]

        with self.assertRaises(RuntimeError):
            MODULE._apply_cold_degraded_ohlcv_policy(rows)

    def test_sanitizer_keeps_state_history_rows_but_excludes_out_of_mask_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            provider_csv = Path(tmp) / "provider.csv"
            provider_csv.write_text(
                "\n".join(
                    [
                        "ts_event,open,high,low,close,volume,instrument_id",
                        "2019-05-04T00:00:00Z,100,101,99,100,1,1",
                        "2019-05-05T00:00:00Z,101,102,100,101,1,1",
                        "2020-04-06T00:00:00Z,102,103,101,102,1,1",
                        "2022-02-09T00:00:00Z,103,104,102,103,1,1",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            rows = MODULE._sanitize_provider_csv(provider_csv, "MESM0", {}, "HASH")

        self.assertEqual([row["completed_trading_date"] for row in rows], ["2019-05-05", "2020-04-06"])
        self.assertEqual(rows[0]["window_role"], "PRE_TEST_WARMUP_BUFFER_NOT_SCORED_EVIDENCE")
        self.assertEqual(rows[1]["window_role"], "TEST")

    def test_sanitizer_admits_sunday_provider_date_as_source_completed_trading_date_with_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            provider_csv = Path(tmp) / "provider.csv"
            provider_csv.write_text(
                "\n".join(
                    [
                        "ts_event,open,high,low,close,volume,instrument_id",
                        "2021-12-05T00:00:00Z,100,101,99,100,1,1",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            rows = MODULE._sanitize_provider_csv(
                provider_csv,
                "MESZ1",
                {"2021-12-05": "AVAILABLE"},
                "HASH",
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["provider_date"], "2021-12-05")
        self.assertEqual(rows[0]["provider_condition_date"], "2021-12-05")
        self.assertEqual(rows[0]["completed_trading_date"], "2021-12-05")
        self.assertEqual(
            rows[0]["completed_trading_date_normalization_status"],
            "SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE",
        )
        self.assertEqual(
            rows[0]["completed_trading_date_policy"],
            "SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE",
        )
        self.assertEqual(rows[0]["provider_condition_classification"], "NORMAL_PROVIDER_CONDITION")

    def test_sanitizer_rejects_duplicate_completed_date_after_source_native_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            provider_csv = Path(tmp) / "provider.csv"
            provider_csv.write_text(
                "\n".join(
                    [
                        "ts_event,open,high,low,close,volume,instrument_id",
                        "2021-12-05T00:00:00Z,100,101,99,100,1,1",
                        "2021-12-05T01:00:00Z,101,102,100,101,1,1",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(RuntimeError):
                MODULE._sanitize_provider_csv(provider_csv, "MESZ1", {}, "HASH")

    def test_lineage_readiness_guard_fails_closed_on_provisional_or_failed_inputs(self) -> None:
        fake_lineage = type("FakeLineage", (), {"ready_for_lineage_use": False})()

        with patch.object(
            MODULE,
            "evaluate_s09_mes_lineage_strategy_readiness",
            return_value={
                "strategy_input_readiness_status": "FAIL_CLOSED_PROVIDER_CONDITION_UNRESOLVED",
                "roll_readiness_status": "PROVISIONAL_NEEDS_SESSION_CALENDAR_REMEDIATION",
            },
        ):
            with self.assertRaises(MODULE.CarverBlocked):
                MODULE._assert_lineage_readiness_locked(fake_lineage)

    def test_test_runner_locked_readiness_contract_passes_lineage_guard(self) -> None:
        bars = tuple(
            MODULE.S09MESDatedContractBar(
                raw_symbol="MESH2",
                completed_trading_date=date(2022, 1, day),
                open=100.0 + day,
                high=102.0 + day,
                low=99.0 + day,
                close=101.0 + day,
                volume=1.0,
                provider_condition_classification="NORMAL_PROVIDER_CONDITION",
                source_raw_sha256="HASH",
                provider_condition_admission_policy="NORMAL_PROVIDER_CONDITION_ONLY",
            )
            for day in range(3, 9)
        )
        definition = MODULE.S09MESDatedContractDefinition(
            raw_symbol="MESH2",
            expiration=MODULE._parse_ts("2022-03-18T13:30:00Z"),
            product_code="MES",
            currency="USD",
            multiplier=5.0,
            tick_size=0.25,
            venue="XCME",
            lifecycle_source="LOCAL_TEST_DATABENTO_DEFINITION_METADATA_MESH2",
        )
        lineage = MODULE.build_s09_mes_lineage(
            MODULE.S09MESLineageRequest(
                symbol_order=("MESH2",),
                bars_by_symbol={"MESH2": bars},
                definitions_by_symbol={"MESH2": definition},
                minimum_target_rows=5,
                strategy_input_readiness_statuses=dict(MODULE.S09_MES_TEST_LOCKED_READINESS_STATUSES),
            )
        )

        MODULE._assert_lineage_readiness_locked(lineage)
        self.assertTrue(lineage.ready_for_lineage_use)

    def test_trading_day_cadence_guard_rejects_sunday_provider_dates(self) -> None:
        clean_rows = [
            {"completed_trading_date": "2020-04-06", "completed_trading_date_policy": "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE"},
            {"completed_trading_date": "2020-04-07", "completed_trading_date_policy": "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE"},
            {"completed_trading_date": "2020-04-08", "completed_trading_date_policy": "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE"},
            {"completed_trading_date": "2020-04-09", "completed_trading_date_policy": "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE"},
            {"completed_trading_date": "2020-04-10", "completed_trading_date_policy": "PROVIDER_DATE_IS_COMPLETED_TRADING_DATE"},
            {
                "completed_trading_date": "2021-12-05",
                "completed_trading_date_policy": "SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE",
            },
        ]
        MODULE._assert_clean_trading_day_cadence(clean_rows)

        with self.assertRaises(MODULE.CarverBlocked):
            MODULE._assert_clean_trading_day_cadence(
                [*clean_rows, {"completed_trading_date": "2022-01-02"}]
            )

    def test_degraded_policy_disposition_blocks_clean_test_evidence(self) -> None:
        self.assertEqual(
            MODULE.DEGRADED_OHLCV_POLICY_DISPOSITION,
            "COLD_SHAPE_BASED_POLICY_LOCKED_BEFORE_STAGE_ACCESS",
        )
        MODULE._assert_degraded_policy_validation_ready()

    def test_trade_count_metrics_separate_fractional_sample_from_whole_contract_executability(self) -> None:
        rows = [
            {"position_change_contract_equivalent": "0.000000000001"},
            {"position_change_contract_equivalent": "0.849"},
            {"position_change_contract_equivalent": "-1.0"},
            {"position_change_contract_equivalent": "1.5"},
        ]

        metrics = MODULE._trade_count_metrics(rows)

        self.assertEqual(metrics["fractional_trade_event_count"], 3)
        self.assertEqual(metrics["whole_contract_equivalent_change_count"], 2)
        self.assertAlmostEqual(metrics["fractional_turnover_contract_equivalent"], 3.349000000001)
        self.assertEqual(
            metrics["trade_count_sample_definition"],
            "FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON",
        )

    def test_state_history_and_scoring_masks_are_separate(self) -> None:
        state_dates = _sample_dates(
            MODULE.STATE_HISTORY_START,
            MODULE.STATE_HISTORY_END,
            MODULE.EXPECTED_STATE_HISTORY_COMPLETED_DATES,
        )
        scoring_dates = _sample_dates(
            MODULE.WINDOW_START,
            MODULE.WINDOW_END,
            MODULE.EXPECTED_COMPLETED_DATES,
        )
        rows = [{"completed_trading_date": item} for item in [*state_dates, *scoring_dates]]

        status = MODULE._state_scoring_mask_status(rows)

        self.assertEqual(status["state_history_completed_dates"], MODULE.EXPECTED_STATE_HISTORY_COMPLETED_DATES)
        self.assertEqual(status["scoring_completed_dates"], MODULE.EXPECTED_COMPLETED_DATES)
        self.assertTrue(status["state_history_sufficient_for_warmup"])
        MODULE._assert_state_scoring_masks(status)
        self.assertEqual(MODULE._scoring_lineage_rows(rows), [{"completed_trading_date": item} for item in scoring_dates])

    def test_state_history_mask_rejects_out_of_mask_dates(self) -> None:
        rows = [
            {"completed_trading_date": MODULE.STATE_HISTORY_START.isoformat()},
            {"completed_trading_date": "2020-04-06"},
            {"completed_trading_date": "2019-05-04"},
        ]
        status = MODULE._state_scoring_mask_status(rows)

        self.assertIn("2019-05-04", status["out_of_mask_completed_dates"])
        with self.assertRaises(MODULE.CarverBlocked):
            MODULE._assert_state_scoring_masks(status)

    def test_forecast_and_backtest_rows_score_current_window_only(self) -> None:
        class ForecastBlock:
            fdm = 1.0
            pre_fdm_forecast = 2.0

        class ForecastResult:
            forecast_block = ForecastBlock()
            final_forecast = 2.0
            rule_forecasts = ()

        dates = [
            (MODULE.WINDOW_START - timedelta(days=MODULE.WARMUP_BARS - index)).isoformat()
            for index in range(MODULE.WARMUP_BARS + 2)
        ]
        lineage_rows = [
            {
                "completed_trading_date": item,
                "source_raw_symbol": "MESM0",
                "adjusted_open": "100",
                "adjusted_high": "101",
                "adjusted_low": "99",
                "adjusted_close": str(100 + index),
                "volume": "1",
            }
            for index, item in enumerate(dates)
        ]
        risk_rows = [
            {"completed_trading_date": item, "daily_price_risk_currency_points": "1.0"}
            for item in dates
        ]

        with patch.object(MODULE, "s09_multiple_trend_forecast", return_value=ForecastResult()) as forecast_call:
            forecast_rows = MODULE._forecast_rows(lineage_rows, risk_rows)
        backtest_rows = MODULE._backtest_rows(lineage_rows, forecast_rows)

        self.assertEqual([row["completed_trading_date"] for row in forecast_rows], ["2020-04-06", "2020-04-07"])
        self.assertEqual(forecast_call.call_count, 2)
        self.assertEqual(len(backtest_rows), 1)
        self.assertEqual(backtest_rows[0]["signal_completed_trading_date"], "2020-04-06")
        self.assertEqual(backtest_rows[0]["pnl_completed_trading_date"], "2020-04-07")

    def test_real_forecast_uses_state_history_at_first_scoring_date(self) -> None:
        dates = [
            (MODULE.WINDOW_START - timedelta(days=MODULE.WARMUP_BARS - 1 - index)).isoformat()
            for index in range(MODULE.WARMUP_BARS)
        ]
        lineage_rows = [
            {
                "completed_trading_date": item,
                "source_raw_symbol": "MESM0",
                "adjusted_open": str(100 + index),
                "adjusted_high": str(101 + index),
                "adjusted_low": str(99 + index),
                "adjusted_close": str(100 + index),
                "volume": "1",
            }
            for index, item in enumerate(dates)
        ]
        risk_rows = [
            {"completed_trading_date": item, "daily_price_risk_currency_points": "1.0"}
            for item in dates
        ]

        forecast_rows = MODULE._forecast_rows(lineage_rows, risk_rows)
        expected = MODULE.s09_multiple_trend_forecast(
            MODULE.S09TrendForecastRequest(
                bars=tuple(MODULE._daily_bar_from_lineage_row(row) for row in lineage_rows),
                as_of=MODULE._midnight_utc(MODULE.WINDOW_START),
                daily_price_risk=MODULE.TimedValue(1.0, MODULE._midnight_utc(MODULE.WINDOW_START)),
                allowed_spans=MODULE.S09_EWMAC_SPANS,
            )
        )

        self.assertEqual([row["completed_trading_date"] for row in forecast_rows], ["2020-04-06"])
        self.assertAlmostEqual(float(forecast_rows[0]["final_forecast"]), expected.final_forecast)
        self.assertEqual(forecast_rows[0]["state_history_start"], MODULE.STATE_HISTORY_START.isoformat())
        self.assertEqual(forecast_rows[0]["scoring_window_start"], MODULE.WINDOW_START.isoformat())

    def test_future_clean_status_wording_is_not_stale_original_pass_receipt(self) -> None:
        mask_status = {
            "state_history_completed_dates": MODULE.EXPECTED_STATE_HISTORY_COMPLETED_DATES,
            "state_history_sufficient_for_warmup": True,
        }
        status = MODULE._status_payload(
            [{"completed_trading_date": "2020-04-06"}],
            [{"completed_trading_date": "2020-04-06"}],
            [{"position_change_contract_equivalent": "1.0"}],
            {
                "fractional_trade_event_count": 1,
                "whole_contract_equivalent_change_count": 1,
                "fractional_turnover_contract_equivalent": 1.0,
                "max_position_change_contract_equivalent": 1.0,
                "fractional_trade_event_epsilon_contract_equivalent": MODULE.FRACTIONAL_TRADE_EVENT_EPSILON_CONTRACT_EQUIVALENT,
                "whole_contract_executability_threshold": MODULE.WHOLE_CONTRACT_EXECUTABILITY_THRESHOLD,
                "trade_count_sample_definition": "FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON",
                "whole_contract_count_definition": "EXECUTABILITY_DIAGNOSTIC_NOT_STATISTICAL_SAMPLE_GATE",
            },
            [],
            mask_status,
        )
        receipt = MODULE._receipt_payload(
            status,
            MODULE.ROOT / "docs" / "researchops" / "dummy_backtest.csv",
            MODULE.ROOT / "docs" / "researchops" / "dummy_summary.csv",
        )

        self.assertNotEqual(status["status"], "PASS_S09_MES_TEST_WINDOW_BACKTEST_EXECUTED_EXACTLY_ONCE_NOT_PROMOTION")
        self.assertNotEqual(receipt["execution_receipt_status"], "CONSUMED_EXACTLY_ONE_AUTHORIZED_TEST_BACKTEST")
        self.assertEqual(status["completed_dates_field_scope"], "SCORING_WINDOW_ONLY_DO_NOT_ADD_STATE_HISTORY")
        self.assertEqual(status["scored_completed_dates"], 1)
        self.assertEqual(status["total_state_plus_scoring_completed_dates"], MODULE.EXPECTED_STATE_HISTORY_COMPLETED_DATES + 1)
        self.assertEqual(status["fractional_trade_event_count"], 1)
        self.assertEqual(status["whole_contract_equivalent_change_count"], 1)

    def test_main_fails_closed_without_explicit_backtest_execution_flag(self) -> None:
        with self.assertRaises(SystemExit) as context:
            MODULE.main([])

        self.assertIn("--execute-authorized-test-backtest", str(context.exception))

    def test_main_fails_closed_without_existing_download_flag(self) -> None:
        with self.assertRaises(SystemExit) as context:
            MODULE.main(["--execute-authorized-test-backtest"])

        self.assertIn("--use-existing-authorized-test-download", str(context.exception))


if __name__ == "__main__":
    unittest.main()

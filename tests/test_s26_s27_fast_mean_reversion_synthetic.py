from __future__ import annotations

import sys
import json
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import LaneClass, SourceRuleStatus, CarverBlocked  # noqa: E402
from carver.spine.m1 import RoundingPolicy, TimedValue  # noqa: E402
from carver.spine.m2 import FORECAST_CAP  # noqa: E402
from carver.spine.s26_s27 import (  # noqa: E402
    S26_EQUILIBRIUM_EWMA_SPAN,
    S26_EXECUTION_SEMANTICS_SOURCE_LOCK_STATUS,
    S26_FORECAST_SCALAR,
    S27_FORECAST_SCALAR,
    S26_FORECAST_ONLY_STATUS,
    S26_ZN_FORECAST_INPUT_STATUS,
    S26_ZN_FORECAST_SERIES_STATUS,
    S26_ZN_SIGMA_RUNTIME_STATUS,
    S27_FORECAST_HANDOFF_STATUS,
    S27_FORECAST_ONLY_STATUS,
    S27_FORECAST_SERIES_STATUS,
    S27_TREND_RUNTIME_LEDGER_STATUS,
    S27_TREND_RUNTIME_STATUS,
    S27_VOL_ATTENUATION_RUNTIME_LEDGER_STATUS,
    S27_VOL_ATTENUATION_RUNTIME_STATUS,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_OUTPUT_ROOT,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_END_UTC,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_START_UTC,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_STATUS,
    S27_ZN_BACKTEST_READINESS_GATE_STATUS,
    S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END,
    S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START,
    S27_ZN_DESIRED_POSITION_PLUMBING_STATUS,
    S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_STATUS,
    S26_ZN_DATABENTO_DATASET,
    S26_ZN_DATABENTO_PROVIDER,
    S26_ZN_DATABENTO_SCHEMA,
    S26_ZN_DATABENTO_STYPE_IN,
    S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC,
    S26_ZN_EXTENDED_HOURLY_REQUEST_MANIFEST_STATUS,
    S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT,
    S26_ZN_EXTENDED_HOURLY_REQUEST_START_UTC,
    S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES,
    S26_ZN_DATABENTO_OHLCV_1H_REQUIRED_COLUMNS,
    S26_ZN_HOURLY_REQUEST_END_UTC,
    S26_ZN_HOURLY_REQUEST_MANIFEST_STATUS,
    S26_ZN_HOURLY_REQUEST_OUTPUT_ROOT,
    S26_ZN_HOURLY_REQUEST_START_UTC,
    S26_ZN_HOURLY_QUARANTINE_STATUS,
    S26_ZN_TARGET_COMPLETED_TRADING_DATES,
    S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
    S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
    S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
    S26_ZN_WORKED_EXAMPLE_ROW_ID,
    S27_TREND_FAST_SPAN,
    S27_TREND_SLOW_SPAN,
    S27_VOL_ATTENUATION_SPAN,
    S26DatabentoHourlyIntakeRequestManifest,
    S26DatabentoHourlyOHLCVRawRow,
    S26ExecutionSemanticsSourceLock,
    S26ExtendedHourlyForecastOnlyCoverageManifest,
    S26FastMeanReversionRequest,
    S26QuarantinedHourlyForecastRequest,
    S26QuarantinedHourlyForecastSeriesRequest,
    S26QuarantinedHourlySourceLocks,
    S26QuarantinedHourlyZNBar,
    S26SigmaPercentRuntimeValue,
    S26SourceLocks,
    S27QuarantinedHourlyForecastRequest,
    S27QuarantinedHourlyForecastSeriesRequest,
    S27RealHourlySourceLocks,
    S27SaferFastMeanReversionRequest,
    S27SourceLocks,
    S27TrendOverlayRuntimeLedgerRequest,
    S27TrendOverlayRuntimeLedgerSourceLocks,
    S27TrendOverlayRuntimeValue,
    S27VolAttenuationRuntimeLedgerRequest,
    S27VolAttenuationRuntimeLedgerSourceLocks,
    S27VolAttenuationRuntimeValue,
    S27ZNDesiredPositionRequest,
    S27ZNPositionExecutionCostSemanticsLock,
    S27ZNPrevalidatedBasePosition,
    SyntheticHourlyPrice,
    SyntheticQuantilePoint,
    build_s26_execution_semantics_source_lock,
    build_s26_zn_extended_hourly_forecast_only_coverage_manifest,
    build_s27_zn_backtest_hourly_archive_window_manifest,
    build_s27_zn_position_execution_cost_semantics_lock,
    build_s27_zn_single_instrument_backtest_readiness_gate,
    s26_execution_semantics_source_lock,
    s26_fast_mean_reversion_forecast,
    s26_forecast_only_from_quarantined_zn_hourly_bars,
    s26_forecast_only_from_quarantined_zn_hourly_ohlcv_bars,
    s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars,
    s27_forecast_only_from_s26_forecast_row,
    s27_forecast_series_only_from_s26_forecast_series,
    s27_safer_fast_mean_reversion_forecast,
    s27_zn_desired_position_from_prevalidated_base,
    s27_zn_position_execution_cost_semantics_lock,
    s27_zn_single_instrument_backtest_readiness_gate,
    s27_trend_overlay_runtime_ledger_from_prevalidated_rows,
    s27_vol_attenuation_runtime_ledger_from_prevalidated_rows,
    validate_s27_zn_backtest_hourly_archive_window_manifest,
    normalize_s26_zn_databento_hourly_ohlcv_raw_row,
    parse_s26_zn_databento_hourly_ohlcv_csv_text,
    validate_s26_zn_hourly_databento_request_manifest,
    validate_s26_zn_extended_hourly_forecast_only_coverage_manifest,
)

FIXTURE_RAW_SHA256 = "D" * 64


class S26S27FastMeanReversionSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.start = datetime(2026, 5, 18, tzinfo=timezone.utc)

    def test_s26_reproduces_equilibrium_raw_sigma_scalar_and_cap(self) -> None:
        prices = self.prices((100.0, 110.0, 105.0, 95.0, 100.0))
        request = S26FastMeanReversionRequest(
            prices=prices,
            as_of=prices[-1].timestamp,
            sigma_percent=TimedValue(0.16, prices[-1].timestamp),
        )

        result = s26_fast_mean_reversion_forecast(request)

        equilibrium = self.ewma(tuple(point.price for point in prices), S26_EQUILIBRIUM_EWMA_SPAN)
        raw = equilibrium - 100.0
        sigma_price = 100.0 * 0.16 / 16.0
        risk_adjusted = raw / sigma_price
        scaled = risk_adjusted * S26_FORECAST_SCALAR
        self.assertAlmostEqual(result.equilibrium, equilibrium)
        self.assertAlmostEqual(result.raw_forecast, raw)
        self.assertAlmostEqual(result.sigma_price, sigma_price)
        self.assertAlmostEqual(result.risk_adjusted_forecast, risk_adjusted)
        self.assertAlmostEqual(result.scaled_forecast, scaled)
        self.assertAlmostEqual(result.capped_forecast, scaled)
        self.assertFalse(result.fdm_used)
        self.assertFalse(result.buffering_used)
        self.assertEqual(result.performance_metrics, ())
        self.assertEqual(result.position_outputs, ())

    def test_s26_raw_sign_and_cap_saturate_both_sides(self) -> None:
        positive = self.s26_for_values((100.0, 100.0, 100.0, 100.0, 80.0), sigma_percent=0.02)
        negative = self.s26_for_values((100.0, 100.0, 100.0, 100.0, 120.0), sigma_percent=0.02)

        self.assertGreater(positive.raw_forecast, 0.0)
        self.assertEqual(positive.capped_forecast, FORECAST_CAP)
        self.assertLess(negative.raw_forecast, 0.0)
        self.assertEqual(negative.capped_forecast, -FORECAST_CAP)

    def test_s26_fails_closed_on_non_synthetic_inputs_unresolved_locks_and_non_source_native_lane(self) -> None:
        prices = self.prices((100.0, 101.0, 102.0, 103.0, 104.0))
        with self.assertRaises(CarverBlocked):
            s26_fast_mean_reversion_forecast(
                S26FastMeanReversionRequest(
                    prices=(replace(prices[0], label="provider_row"),) + prices[1:],
                    as_of=prices[-1].timestamp,
                    sigma_percent=TimedValue(0.16, prices[-1].timestamp),
                )
            )
        with self.assertRaises(CarverBlocked):
            s26_fast_mean_reversion_forecast(
                S26FastMeanReversionRequest(
                    prices=prices,
                    as_of=prices[-1].timestamp,
                    sigma_percent=TimedValue(0.16, prices[-1].timestamp),
                    source_locks=replace(S26SourceLocks(), scalar_status=SourceRuleStatus.UNRESOLVED),
                )
            )
        with self.assertRaises(CarverBlocked):
            s26_fast_mean_reversion_forecast(
                S26FastMeanReversionRequest(
                    prices=prices,
                    as_of=prices[-1].timestamp,
                    sigma_percent=TimedValue(0.16, prices[-1].timestamp),
                    lane_class=LaneClass.CFD_ADAPTER,
                )
            )

    def test_s27_allows_same_sign_forecasts_and_zeroes_opposing_forecasts(self) -> None:
        cases = (
            ("positive_raw_positive_trend", self.uptrend_with_final(140.0), False),
            ("negative_raw_negative_trend", self.downtrend_with_final(160.0), False),
            ("positive_raw_negative_trend", self.downtrend_with_final(130.0), True),
            ("negative_raw_positive_trend", self.uptrend_with_final(180.0), True),
        )
        for label, prices, should_oppose in cases:
            with self.subTest(label=label):
                result = s27_safer_fast_mean_reversion_forecast(self.s27_request(prices))
                self.assertEqual(result.opposes_trend, should_oppose)
                self.assertEqual(result.trend_interaction_policy, "ZERO_OPPOSING_MEAN_REVERSION_FORECAST")
                if should_oppose:
                    self.assertEqual(result.adjusted_raw_forecast, 0.0)
                    self.assertEqual(result.capped_forecast, 0.0)
                else:
                    self.assertNotEqual(result.adjusted_raw_forecast, 0.0)
                    self.assertLessEqual(abs(result.capped_forecast), FORECAST_CAP)
                self.assertFalse(result.fdm_used)
                self.assertFalse(result.buffering_used)
                self.assertEqual(result.performance_metrics, ())
                self.assertEqual(result.position_outputs, ())

    def test_s27_reproduces_vol_attenuation_and_uses_s27_scalar_cap(self) -> None:
        prices = self.uptrend_with_final(140.0)
        quantiles = tuple(
            SyntheticQuantilePoint("synthetic_high_vol_quantile", price.timestamp, 0.8)
            for price in prices[-S27_VOL_ATTENUATION_SPAN:]
        )
        result = s27_safer_fast_mean_reversion_forecast(
            self.s27_request(prices, vol_quantiles=quantiles, sigma_percent=0.05)
        )

        self.assertAlmostEqual(result.vol_multiplier, 2.0 - 1.5 * 0.8)
        self.assertAlmostEqual(result.scalar, S27_FORECAST_SCALAR)
        self.assertLessEqual(abs(result.capped_forecast), FORECAST_CAP)

    def test_s27_fails_closed_on_unresolved_dependency_bad_quantile_and_short_history(self) -> None:
        prices = self.uptrend_with_final(140.0)
        with self.assertRaises(CarverBlocked):
            s27_safer_fast_mean_reversion_forecast(
                self.s27_request(
                    prices,
                    s27_source_locks=replace(S27SourceLocks(), trend_overlay_status=SourceRuleStatus.UNRESOLVED),
                )
            )
        bad_quantiles = tuple(
            SyntheticQuantilePoint("synthetic_bad_quantile", price.timestamp, 1.5)
            for price in prices[-S27_VOL_ATTENUATION_SPAN:]
        )
        with self.assertRaises(CarverBlocked):
            s27_safer_fast_mean_reversion_forecast(self.s27_request(prices, vol_quantiles=bad_quantiles))
        with self.assertRaises(CarverBlocked):
            s27_safer_fast_mean_reversion_forecast(self.s27_request(prices[: S27_TREND_SLOW_SPAN - 1]))

    def test_gate_docs_preserve_book_instrument_and_no_real_data_boundaries(self) -> None:
        source_atoms = (ROOT / "docs" / "process" / "CARVER_S26_S27_SOURCE_ATOM_SHEET_2026-05-30.md").read_text(
            encoding="utf-8"
        )
        gate = (
            ROOT / "docs" / "process" / "CARVER_S26_S27_SYNTHETIC_CONFORMANCE_GATE_DRAFT_2026-05-30.md"
        ).read_text(encoding="utf-8")

        self.assertIn("S26_BOOK_WORKED_EXAMPLE_US_10_YEAR_FUTURE_IDENTITY_LOCK", source_atoms)
        self.assertIn("NO_SP500_OR_MES_CLAIM_AS_S27_NATIVE_WORKED_EXAMPLE_WITHOUT_SEPARATE_SOURCE_ATOM", source_atoms)
        self.assertIn("S27_SP500_MES_NATIVE_WORKED_EXAMPLE_LOCK: NOT_LOCKED_FROM_CHAPTER_27", gate)
        self.assertIn("databento access", gate.lower())
        self.assertIn("no diagnostics", gate.lower())
        self.assertIn("no backtests", gate.lower())

    def test_s26_quarantined_zn_hourly_forecast_only_boundary_reuses_formula(self) -> None:
        bars = self.zn_quarantined_bars((100.0, 110.0, 105.0, 95.0, 100.0))
        result = s26_forecast_only_from_quarantined_zn_hourly_bars(
            S26QuarantinedHourlyForecastRequest(
                bars=bars,
                as_of=bars[-1].derived_completed_bar_end_utc,
                sigma_percent=TimedValue(0.16, bars[-1].derived_completed_bar_end_utc),
                source_locks=self.locked_quarantined_source_locks(),
            )
        )

        equilibrium = self.ewma(tuple(bar.close for bar in bars), S26_EQUILIBRIUM_EWMA_SPAN)
        raw = equilibrium - 100.0
        sigma_price = 100.0 * 0.16 / 16.0
        risk_adjusted = raw / sigma_price
        scaled = risk_adjusted * S26_FORECAST_SCALAR
        self.assertEqual(result.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        self.assertEqual(result.author_market_code, "ZN")
        self.assertEqual(result.instrument_id, S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID)
        self.assertEqual(result.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
        self.assertAlmostEqual(result.equilibrium_ewma_5, equilibrium)
        self.assertAlmostEqual(result.raw_forecast, raw)
        self.assertAlmostEqual(result.sigma_price, sigma_price)
        self.assertAlmostEqual(result.risk_adjusted_forecast, risk_adjusted)
        self.assertAlmostEqual(result.scaled_forecast, scaled)
        self.assertAlmostEqual(result.capped_forecast, scaled)
        self.assertEqual(result.forecast_output_status, S26_FORECAST_ONLY_STATUS)
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.position_outputs, ())

    def test_s26_quarantined_zn_hourly_forecast_fails_closed_without_locks_or_with_wrong_symbol(self) -> None:
        bars = self.zn_quarantined_bars((100.0, 101.0, 102.0, 103.0, 104.0))
        with self.assertRaises(CarverBlocked):
            s26_forecast_only_from_quarantined_zn_hourly_bars(
                S26QuarantinedHourlyForecastRequest(
                    bars=bars,
                    as_of=bars[-1].derived_completed_bar_end_utc,
                    sigma_percent=TimedValue(0.16, bars[-1].derived_completed_bar_end_utc),
                    source_locks=S26QuarantinedHourlySourceLocks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s26_forecast_only_from_quarantined_zn_hourly_bars(
                S26QuarantinedHourlyForecastRequest(
                    bars=(replace(bars[0], raw_symbol="ZTM6"),) + bars[1:],
                    as_of=bars[-1].derived_completed_bar_end_utc,
                    sigma_percent=TimedValue(0.16, bars[-1].derived_completed_bar_end_utc),
                    source_locks=self.locked_quarantined_source_locks(),
                )
            )

    def test_s26_quarantined_zn_hourly_gate_docs_preserve_incomplete_goal_boundary(self) -> None:
        intake_gate = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S26_ZN_HOURLY_DATABENTO_TINY_INTAKE_EXECUTION_GATE_DRAFT_2026-05-30.md"
        ).read_text(encoding="utf-8")
        handoff_gate = (
            ROOT / "docs" / "process" / "CARVER_S26_ZN_HOURLY_FORECAST_ONLY_HANDOFF_GATE_DRAFT_2026-05-30.md"
        ).read_text(encoding="utf-8")
        sigma_gate = (
            ROOT / "docs" / "process" / "CARVER_S26_ZN_HOURLY_SIGMA_PERCENT_SOURCE_GATE_2026-05-30.md"
        ).read_text(encoding="utf-8")
        audit = (
            ROOT / "docs" / "process" / "CARVER_S26_ZN_HOURLY_BRIDGE_CHAPTER_PROGRESS_AUDIT_2026-05-30.md"
        ).read_text(encoding="utf-8")

        self.assertIn("G_R1A_ZN_S26_WORKED_EXAMPLE_DATABENTO_OHLCV_1H_TINY_QUARANTINE_INTAKE", intake_gate)
        self.assertIn("42000661", intake_gate)
        self.assertIn("ZNM6", intake_gate)
        self.assertIn("S26 sigma_percent_t estimation atom", handoff_gate)
        self.assertIn("LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY", handoff_gate)
        self.assertIn("price_t * sigma_percent_t / 16", sigma_gate)
        self.assertIn("PREVALIDATED_INPUT_REQUIRED", sigma_gate)
        self.assertIn("NOT COMPLETE", audit)
        self.assertIn("no additional data download", audit.lower())

    def test_s26_execution_semantics_source_lock_is_design_only(self) -> None:
        lock: S26ExecutionSemanticsSourceLock = build_s26_execution_semantics_source_lock()

        self.assertEqual(lock.source_lock_status, S26_EXECUTION_SEMANTICS_SOURCE_LOCK_STATUS)
        self.assertEqual(lock.hourly_completed_bar_policy, "HOURLY_COMPLETED_BAR_ONLY")
        self.assertEqual(lock.forecast_availability_policy, "FORECAST_AVAILABLE_AFTER_DERIVED_COMPLETED_BAR_END_UTC")
        self.assertEqual(lock.limit_order_semantics_policy, "LIMIT_ORDER_STYLE_SEMANTICS_ONLY_NOT_MARKET_ORDER_FILL_MODEL")
        self.assertEqual(lock.no_buffering_policy, "NO_BUFFERING_USED")
        self.assertEqual(lock.no_market_order_cost_assumption_policy, "NO_MARKET_ORDER_COST_ASSUMPTION")
        self.assertEqual(lock.execution_cadence_policy, "SOURCE_FAITHFUL_HOURLY_CADENCE_NO_INTRABAR_LOOKAHEAD")
        self.assertEqual(lock.position_sizing_status, "POSITION_SIZING_CLOSED_SEPARATE_GATE_REQUIRED")
        self.assertEqual(lock.cost_model_status, "COST_MODEL_CLOSED_SEPARATE_GATE_REQUIRED")
        self.assertEqual(lock.test_boundary_status, "NOT_TEST_NOT_BACKTEST_NOT_DIAGNOSTIC")
        self.assertEqual(lock.diagnostics_outputs, ())
        self.assertEqual(lock.backtest_outputs, ())
        self.assertEqual(lock.position_outputs, ())
        self.assertEqual(lock.order_outputs, ())
        self.assertEqual(lock.fill_outputs, ())
        self.assertEqual(lock.cost_outputs, ())

    def test_s26_execution_semantics_source_lock_fails_closed_on_drift_outputs_or_non_source_native_lane(self) -> None:
        lock = build_s26_execution_semantics_source_lock()
        bad_locks = (
            replace(lock, hourly_completed_bar_policy="INTRABAR_ALLOWED"),
            replace(lock, forecast_availability_policy="FORECAST_AVAILABLE_BEFORE_COMPLETED_BAR"),
            replace(lock, limit_order_semantics_policy="MARKET_ORDER_FILL_MODEL"),
            replace(lock, no_buffering_policy="BUFFERING_ALLOWED"),
            replace(lock, no_market_order_cost_assumption_policy="MARKET_ORDER_COST_ASSUMED"),
            replace(lock, execution_cadence_policy="INTRABAR_LOOKAHEAD_ALLOWED"),
            replace(lock, position_sizing_status="POSITION_SIZING_OPEN"),
            replace(lock, cost_model_status="COST_MODEL_OPEN"),
            replace(lock, test_boundary_status="TEST_AUTHORIZED"),
            replace(lock, diagnostics_outputs=("diagnostic",)),
            replace(lock, backtest_outputs=("backtest",)),
            replace(lock, position_outputs=("position",)),
            replace(lock, order_outputs=("order",)),
            replace(lock, fill_outputs=("fill",)),
            replace(lock, cost_outputs=("cost",)),
        )
        for bad_lock in bad_locks:
            with self.subTest(lock=bad_lock):
                with self.assertRaises(CarverBlocked):
                    s26_execution_semantics_source_lock(bad_lock)

        with self.assertRaises(CarverBlocked):
            s26_execution_semantics_source_lock(lock, lane_class=LaneClass.CFD_ADAPTER)

    def test_s27_zn_position_execution_cost_semantics_lock_is_readiness_only(self) -> None:
        lock: S27ZNPositionExecutionCostSemanticsLock = build_s27_zn_position_execution_cost_semantics_lock()

        self.assertEqual(lock.source_lock_status, S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_STATUS)
        self.assertEqual(lock.sizing_formula_policy, "USE_M1_SIZE_CONTRACTS_BASE_POSITION_THEN_CAPPED_FORECAST_OVER_10")
        self.assertEqual(lock.target_risk_policy, "ANNUAL_TARGET_RISK_20_PERCENT_BOOK_DEFAULT_LOCK_REQUIRED_AT_TEST_GATE")
        self.assertEqual(lock.single_instrument_context_policy, "SINGLE_INSTRUMENT_ZN_STANDALONE_DEV_RECON_WEIGHT_1_IDM_1")
        self.assertEqual(lock.annual_risk_estimate_policy, "PREVALIDATED_S03_ANNUAL_PERCENTAGE_RISK_REQUIRED_NO_LOOKAHEAD")
        self.assertEqual(lock.multiplier_fx_policy, "ZN_CONTRACT_MULTIPLIER_AND_USD_FX_LOCK_REQUIRED_BEFORE_POSITION_OUTPUT")
        self.assertEqual(lock.forecast_to_position_policy, "FINAL_CAPPED_FORECAST_DIVIDED_BY_10_MULTIPLIES_BASE_POSITION")
        self.assertEqual(lock.execution_policy, "HOURLY_COMPLETED_BAR_NEXT_BAR_LIMIT_STYLE_NO_BUFFERING_NO_INTRABAR_LOOKAHEAD")
        self.assertEqual(
            lock.cost_model_policy,
            "COMMISSION_ONLY_DEV_RECON_ALLOWED_SPREAD_AND_MARKET_ORDER_COSTS_UNRESOLVED_FAIL_CLOSED",
        )
        self.assertEqual(lock.test_boundary_status, "READINESS_ONLY_NOT_BACKTEST_NOT_DIAGNOSTIC_NOT_POSITION")
        self.assertEqual(lock.position_outputs, ())
        self.assertEqual(lock.backtest_outputs, ())
        self.assertEqual(lock.cost_outputs, ())

    def test_s27_zn_position_execution_cost_semantics_lock_fails_closed_on_drift_or_outputs(self) -> None:
        lock = build_s27_zn_position_execution_cost_semantics_lock()
        bad_locks = (
            replace(lock, sizing_formula_policy="DIRECT_FORECAST_AS_POSITION"),
            replace(lock, target_risk_policy="TARGET_RISK_TUNED_AFTER_RESULTS"),
            replace(lock, single_instrument_context_policy="PORTFOLIO_IDM_IMPORTED"),
            replace(lock, annual_risk_estimate_policy="LOOKAHEAD_RISK_ALLOWED"),
            replace(lock, multiplier_fx_policy="MULTIPLIER_OPTIONAL"),
            replace(lock, forecast_to_position_policy="FINAL_FORECAST_DIVIDED_BY_20"),
            replace(lock, rounding_policy_status="ROUNDING_IMPLICIT"),
            replace(lock, execution_policy="BUFFERING_ALLOWED"),
            replace(lock, cost_model_policy="MARKET_ORDER_SPREAD_COST_ASSUMED"),
            replace(lock, test_boundary_status="BACKTEST_AUTHORIZED"),
            replace(lock, position_outputs=("position",)),
            replace(lock, backtest_outputs=("backtest",)),
            replace(lock, cost_outputs=("cost",)),
        )
        for bad_lock in bad_locks:
            with self.subTest(lock=bad_lock):
                with self.assertRaises(CarverBlocked):
                    s27_zn_position_execution_cost_semantics_lock(bad_lock)

        with self.assertRaises(CarverBlocked):
            s27_zn_position_execution_cost_semantics_lock(lock, lane_class=LaneClass.CFD_ADAPTER)

    def test_s27_zn_backtest_hourly_archive_window_manifest_is_process_only(self) -> None:
        manifest = build_s27_zn_backtest_hourly_archive_window_manifest()

        validated = validate_s27_zn_backtest_hourly_archive_window_manifest(manifest)

        self.assertIs(validated, manifest)
        self.assertEqual(validated.status, S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_STATUS)
        self.assertEqual(validated.provider, S26_ZN_DATABENTO_PROVIDER)
        self.assertEqual(validated.dataset, S26_ZN_DATABENTO_DATASET)
        self.assertEqual(validated.schema, S26_ZN_DATABENTO_SCHEMA)
        self.assertEqual(validated.stype_in, "raw_symbol")
        self.assertEqual(validated.target_completed_trading_date_start, S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START)
        self.assertEqual(validated.target_completed_trading_date_end, S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END)
        self.assertEqual(validated.target_completed_trading_date_start, "2022-01-01")
        self.assertEqual(validated.target_completed_trading_date_end, "2023-12-31")
        self.assertEqual(validated.request_start_utc, S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_START_UTC)
        self.assertEqual(validated.request_end_utc, S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_END_UTC)
        self.assertEqual(validated.request_start_utc.isoformat(), "2021-12-31T00:00:00+00:00")
        self.assertEqual(validated.request_end_utc.isoformat(), "2024-01-01T00:00:00+00:00")
        self.assertEqual(validated.required_raw_symbols, S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS)
        self.assertEqual(
            validated.required_raw_symbols,
            ("ZNH2", "ZNM2", "ZNU2", "ZNZ2", "ZNH3", "ZNM3", "ZNU3", "ZNZ3", "ZNH4"),
        )
        self.assertEqual(validated.output_root, S27_ZN_BACKTEST_HOURLY_ARCHIVE_OUTPUT_ROOT)
        self.assertIn("2022-01-01_2023-12-31", validated.output_root)
        self.assertIn("NO_PROVIDER_API_ACCESS", validated.no_authorization)
        self.assertIn("NO_DATA_DOWNLOAD", validated.no_authorization)
        self.assertIn("NO_BACKTESTS", validated.no_authorization)

        gate_doc = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S27_ZN_2022_2023_DEV_RECON_BACKTEST_EXECUTION_GATE_DRAFT_2026-05-31.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PROCESS_ONLY_EXECUTION_GATE_DRAFT_NOT_AUTHORIZATION", gate_doc)
        self.assertIn("2022-01-01", gate_doc)
        self.assertIn("2023-12-31", gate_doc)
        self.assertIn("ZNH2, ZNM2, ZNU2, ZNZ2, ZNH3, ZNM3, ZNU3, ZNZ3, ZNH4", gate_doc)
        self.assertIn("continuous_contracts: FORBIDDEN", gate_doc)
        self.assertIn("NO_ALPHA_CLAIM", gate_doc)
        self.assertIn("no provider API access", gate_doc)

    def test_s27_zn_backtest_hourly_archive_window_manifest_fails_closed_on_scope_drift(self) -> None:
        manifest = build_s27_zn_backtest_hourly_archive_window_manifest()
        bad_manifests = (
            replace(manifest, provider="NINJATRADER"),
            replace(manifest, dataset="XNAS.ITCH"),
            replace(manifest, schema="ohlcv-1d"),
            replace(manifest, stype_in="continuous"),
            replace(manifest, row_id="APPENDIX_C_174_006"),
            replace(manifest, author_market_code="MES"),
            replace(manifest, target_completed_trading_date_start="2024-01-01"),
            replace(manifest, required_raw_symbols=("ZN.c.0",)),
            replace(manifest, local_continuous_policy="PROVIDER_CONTINUOUS_ALLOWED"),
            replace(manifest, provider_condition_policy="DROP_MISSING_ROWS"),
            replace(manifest, no_authorization=("NO_PROVIDER_API_ACCESS",)),
        )
        for bad_manifest in bad_manifests:
            with self.subTest(manifest=bad_manifest):
                with self.assertRaises(CarverBlocked):
                    validate_s27_zn_backtest_hourly_archive_window_manifest(bad_manifest)

    def test_s27_zn_single_instrument_backtest_readiness_gate_opens_path_without_running_backtest(self) -> None:
        semantics = build_s27_zn_position_execution_cost_semantics_lock()
        manifest = build_s27_zn_backtest_hourly_archive_window_manifest()
        gate = build_s27_zn_single_instrument_backtest_readiness_gate()

        validated = s27_zn_single_instrument_backtest_readiness_gate(
            gate,
            semantics_lock=semantics,
            archive_manifest=manifest,
        )

        self.assertIs(validated, gate)
        self.assertEqual(validated.status, S27_ZN_BACKTEST_READINESS_GATE_STATUS)
        self.assertEqual(validated.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        self.assertEqual(validated.author_market_code, S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE)
        self.assertEqual(validated.forecast_series_status, S27_FORECAST_SERIES_STATUS)
        self.assertEqual(validated.first_backtest_scope, "QUARANTINED_DEV_RECON_ZN_ONLY_S27_NO_OOS_NO_LOCKBOX_NO_PROMOTION")
        self.assertEqual(validated.promotion_boundary_status, "NO_ALPHA_CLAIM_NO_DEPLOYMENT_NO_TRADING")
        self.assertEqual(validated.backtest_outputs, ())
        self.assertEqual(validated.position_outputs, ())
        self.assertEqual(validated.performance_outputs, ())

    def test_s27_zn_single_instrument_backtest_readiness_gate_fails_closed_on_drift(self) -> None:
        semantics = build_s27_zn_position_execution_cost_semantics_lock()
        manifest = build_s27_zn_backtest_hourly_archive_window_manifest()
        gate = build_s27_zn_single_instrument_backtest_readiness_gate()
        bad_gates = (
            replace(gate, status="BACKTEST_READY"),
            replace(gate, strategy_id="S26_FAST_MEAN_REVERSION_ZN"),
            replace(gate, row_id="APPENDIX_C_174_006"),
            replace(gate, forecast_series_status="UNLOCKED"),
            replace(gate, hostile_audit_status="NOT_AUDITED"),
            replace(gate, position_execution_cost_status="UNLOCKED"),
            replace(gate, hourly_archive_manifest_status="DATA_AUTHORIZED"),
            replace(gate, first_backtest_scope="PORTFOLIO_BACKTEST"),
            replace(gate, promotion_boundary_status="ALPHA_CLAIM_ALLOWED"),
            replace(gate, performance_outputs=("sharpe",)),
        )
        for bad_gate in bad_gates:
            with self.subTest(gate=bad_gate):
                with self.assertRaises(CarverBlocked):
                    s27_zn_single_instrument_backtest_readiness_gate(
                        bad_gate,
                        semantics_lock=semantics,
                        archive_manifest=manifest,
                    )

        with self.assertRaises(CarverBlocked):
            s27_zn_single_instrument_backtest_readiness_gate(
                gate,
                semantics_lock=replace(semantics, execution_policy="BUFFERING_ALLOWED"),
                archive_manifest=manifest,
            )
        with self.assertRaises(CarverBlocked):
            s27_zn_single_instrument_backtest_readiness_gate(
                gate,
                semantics_lock=semantics,
                archive_manifest=replace(manifest, required_raw_symbols=("ZN.c.0",)),
            )

    def test_s26_zn_hourly_databento_request_manifest_is_locked_and_process_only(self) -> None:
        manifest = self.load_s26_zn_request_manifest()

        validated = validate_s26_zn_hourly_databento_request_manifest(manifest)

        self.assertIs(validated, manifest)
        self.assertEqual(validated.status, S26_ZN_HOURLY_REQUEST_MANIFEST_STATUS)
        self.assertEqual(validated.provider, S26_ZN_DATABENTO_PROVIDER)
        self.assertEqual(validated.dataset, S26_ZN_DATABENTO_DATASET)
        self.assertEqual(validated.schema, S26_ZN_DATABENTO_SCHEMA)
        self.assertEqual(validated.stype_in, S26_ZN_DATABENTO_STYPE_IN)
        self.assertEqual(validated.symbols, (S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,))
        self.assertEqual(validated.expected_raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
        self.assertEqual(validated.request_start_utc, S26_ZN_HOURLY_REQUEST_START_UTC)
        self.assertEqual(validated.request_end_utc, S26_ZN_HOURLY_REQUEST_END_UTC)
        self.assertEqual(validated.target_completed_trading_dates, S26_ZN_TARGET_COMPLETED_TRADING_DATES)
        self.assertEqual(validated.output_root, S26_ZN_HOURLY_REQUEST_OUTPUT_ROOT)
        self.assertIn("NO_PROVIDER_API_ACCESS", validated.no_authorization)
        self.assertIn("NO_DATA_DOWNLOAD", validated.no_authorization)
        self.assertIn("NO_MARKET_ROW_PARSING", validated.no_authorization)

    def test_s26_zn_hourly_databento_request_manifest_fails_closed_on_scope_drift(self) -> None:
        manifest = self.load_s26_zn_request_manifest()
        bad_cases = (
            replace(manifest, dataset="XNAS.ITCH"),
            replace(manifest, schema="ohlcv-1d"),
            replace(manifest, symbols=(S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID, 123)),
            replace(manifest, expected_raw_symbol="ZTM6"),
            replace(manifest, continuous_contracts_status="OPEN"),
            replace(manifest, request_end_utc=datetime(2026, 5, 24, tzinfo=timezone.utc)),
            replace(manifest, no_authorization=tuple(item for item in manifest.no_authorization if item != "NO_DATA_DOWNLOAD")),
        )
        for bad_manifest in bad_cases:
            with self.subTest(bad_manifest=bad_manifest):
                with self.assertRaises(CarverBlocked):
                    validate_s26_zn_hourly_databento_request_manifest(bad_manifest)

    def test_s26_zn_extended_forecast_only_coverage_manifest_is_locked_and_process_only(self) -> None:
        manifest: S26ExtendedHourlyForecastOnlyCoverageManifest = (
            build_s26_zn_extended_hourly_forecast_only_coverage_manifest()
        )

        self.assertIs(validate_s26_zn_extended_hourly_forecast_only_coverage_manifest(manifest), manifest)
        self.assertEqual(manifest.status, S26_ZN_EXTENDED_HOURLY_REQUEST_MANIFEST_STATUS)
        self.assertEqual(manifest.provider, S26_ZN_DATABENTO_PROVIDER)
        self.assertEqual(manifest.dataset, S26_ZN_DATABENTO_DATASET)
        self.assertEqual(manifest.schema, S26_ZN_DATABENTO_SCHEMA)
        self.assertEqual(manifest.stype_in, S26_ZN_DATABENTO_STYPE_IN)
        self.assertEqual(manifest.symbols, (S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,))
        self.assertEqual(manifest.row_id, S26_ZN_WORKED_EXAMPLE_ROW_ID)
        self.assertEqual(manifest.expected_raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
        self.assertEqual(manifest.request_start_utc, S26_ZN_EXTENDED_HOURLY_REQUEST_START_UTC)
        self.assertEqual(manifest.request_end_utc, S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC)
        self.assertEqual(manifest.target_completed_trading_dates, S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES)
        self.assertEqual(manifest.target_completed_trading_dates[0], "2026-04-13")
        self.assertEqual(manifest.target_completed_trading_dates[-1], "2026-05-22")
        self.assertEqual(len(manifest.target_completed_trading_dates), 30)
        self.assertTrue(set(S26_ZN_TARGET_COMPLETED_TRADING_DATES).issubset(set(manifest.target_completed_trading_dates)))
        self.assertEqual(manifest.output_root, S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT)
        self.assertEqual(manifest.extended_window_purpose, "EXPAND_S26_FORECAST_ONLY_COVERAGE_BEFORE_S27_TEST_GATE")
        self.assertEqual(
            manifest.sigma_runtime_requirement,
            "ONE_PREVALIDATED_NO_LOOKAHEAD_SIGMA_RUNTIME_PER_FORECAST_ROW_REQUIRED",
        )
        self.assertEqual(manifest.output_boundary_status, "FORECAST_ONLY_NO_DIAGNOSTIC_NO_BACKTEST_NO_POSITION")
        self.assertIn("NO_PROVIDER_API_ACCESS", manifest.no_authorization)
        self.assertIn("NO_DATA_DOWNLOAD", manifest.no_authorization)
        self.assertIn("NO_FORECAST_COMPUTATION", manifest.no_authorization)

    def test_s26_zn_extended_forecast_only_coverage_manifest_fails_closed_on_scope_drift(self) -> None:
        manifest = build_s26_zn_extended_hourly_forecast_only_coverage_manifest()
        bad_cases = (
            replace(manifest, status="AUTHORIZED"),
            replace(manifest, schema="ohlcv-1d"),
            replace(manifest, symbols=(S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID, 123)),
            replace(manifest, expected_raw_symbol="ZN.c.0"),
            replace(manifest, request_start_utc=S26_ZN_HOURLY_REQUEST_START_UTC),
            replace(manifest, request_end_utc=S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC + timedelta(hours=1)),
            replace(manifest, target_completed_trading_dates=S26_ZN_TARGET_COMPLETED_TRADING_DATES),
            replace(manifest, extended_window_purpose="TEST_READY"),
            replace(manifest, sigma_runtime_requirement="SIGMA_OPTIONAL"),
            replace(manifest, output_boundary_status="DIAGNOSTICS_ALLOWED"),
            replace(manifest, continuous_contracts_status="OPEN"),
            replace(manifest, parent_symbols_status="OPEN"),
            replace(manifest, raw_symbol_selector_status="OPEN"),
            replace(manifest, output_root=S26_ZN_HOURLY_REQUEST_OUTPUT_ROOT),
            replace(manifest, no_authorization=("NO_PROVIDER_API_ACCESS",)),
        )
        for bad_manifest in bad_cases:
            with self.subTest(bad_manifest=bad_manifest):
                with self.assertRaises(CarverBlocked):
                    validate_s26_zn_extended_hourly_forecast_only_coverage_manifest(bad_manifest)

    def test_s26_zn_hourly_gate_docs_reference_machine_readable_manifest(self) -> None:
        intake_gate = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S26_ZN_HOURLY_DATABENTO_TINY_INTAKE_EXECUTION_GATE_DRAFT_2026-05-30.md"
        ).read_text(encoding="utf-8")
        result = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S26_ZN_HOURLY_REQUEST_MANIFEST_PLUMBING_RESULT_2026-05-30.md"
        ).read_text(encoding="utf-8")

        self.assertIn("CARVER_S26_ZN_DATABENTO_OHLCV_1H_REQUEST_MANIFEST_2026-05-30.json", intake_gate)
        self.assertIn("PROCESS_ONLY_REQUEST_MANIFEST_NOT_AUTHORIZATION", result)
        self.assertIn("NO_PROVIDER_API_ACCESS", result)
        self.assertIn("NO_DATA_DOWNLOAD", result)

    def test_s26_zn_hourly_raw_row_normalizes_completed_bar_without_forecast_readiness(self) -> None:
        manifest = self.load_s26_zn_request_manifest()
        raw = self.raw_zn_hourly_row(self.start)

        normalized = normalize_s26_zn_databento_hourly_ohlcv_raw_row(
            raw,
            manifest,
            completed_trading_date="2026-05-18",
        )

        self.assertEqual(normalized.lane_class, LaneClass.SOURCE_NATIVE_FUTURES)
        self.assertEqual(normalized.dataset, S26_ZN_DATABENTO_DATASET)
        self.assertEqual(normalized.schema, S26_ZN_DATABENTO_SCHEMA)
        self.assertEqual(normalized.instrument_id, S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID)
        self.assertEqual(normalized.raw_symbol, S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL)
        self.assertEqual(normalized.provider_ts_event_start_utc, self.start)
        self.assertEqual(normalized.derived_completed_bar_end_utc, self.start + timedelta(hours=1))
        self.assertEqual(normalized.completed_trading_date, "2026-05-18")
        self.assertEqual(normalized.row_shape_status, "PASS_OHLCV_1H_ROW_SHAPE")
        self.assertEqual(normalized.strategy_use_status, S26_ZN_HOURLY_QUARANTINE_STATUS)
        with self.assertRaises(CarverBlocked):
            normalized.to_forecast_bar().validate()

    def test_s26_zn_hourly_raw_row_normalizer_fails_closed_on_bad_shape_scope_and_date(self) -> None:
        manifest = self.load_s26_zn_request_manifest()
        bad_rows = (
            replace(self.raw_zn_hourly_row(self.start), schema="ohlcv-1d"),
            replace(self.raw_zn_hourly_row(self.start), instrument_id=123),
            replace(self.raw_zn_hourly_row(self.start), raw_symbol="ZTM6"),
            replace(self.raw_zn_hourly_row(self.start), provider_ts_event_start_utc=datetime(2026, 5, 16, 23, tzinfo=timezone.utc)),
            replace(self.raw_zn_hourly_row(self.start), high=99.0),
            replace(self.raw_zn_hourly_row(self.start), volume=-1.0),
            replace(self.raw_zn_hourly_row(self.start), source_raw_sha256="not_a_sha256"),
        )
        for raw in bad_rows:
            with self.subTest(raw=raw):
                with self.assertRaises(CarverBlocked):
                    normalize_s26_zn_databento_hourly_ohlcv_raw_row(
                        raw,
                        manifest,
                        completed_trading_date="2026-05-18",
                    )
        with self.assertRaises(CarverBlocked):
            normalize_s26_zn_databento_hourly_ohlcv_raw_row(
                self.raw_zn_hourly_row(self.start),
                manifest,
                completed_trading_date="2026-05-25",
            )

    def test_s26_zn_hourly_normalized_rows_can_feed_forecast_only_after_explicit_status_promotion(self) -> None:
        manifest = self.load_s26_zn_request_manifest()
        normalized = tuple(
            normalize_s26_zn_databento_hourly_ohlcv_raw_row(
                self.raw_zn_hourly_row(self.start + timedelta(hours=index), close=100.0 + index),
                manifest,
                completed_trading_date="2026-05-18",
                strategy_use_status=S26_ZN_FORECAST_INPUT_STATUS,
            )
            for index in range(S26_EQUILIBRIUM_EWMA_SPAN)
        )
        bars = tuple(bar.to_forecast_bar() for bar in normalized)
        result = s26_forecast_only_from_quarantined_zn_hourly_bars(
            S26QuarantinedHourlyForecastRequest(
                bars=bars,
                as_of=bars[-1].derived_completed_bar_end_utc,
                sigma_percent=TimedValue(0.16, bars[-1].derived_completed_bar_end_utc),
                source_locks=self.locked_quarantined_source_locks(),
            )
        )

        self.assertEqual(result.forecast_output_status, S26_FORECAST_ONLY_STATUS)
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.position_outputs, ())

    def test_s26_zn_hourly_csv_text_parser_normalizes_fixture_rows_only(self) -> None:
        manifest = self.load_s26_zn_request_manifest()
        csv_text = "\n".join(
            (
                ",".join(S26_ZN_DATABENTO_OHLCV_1H_REQUIRED_COLUMNS),
                "2026-05-18T00:00:00.000000000Z,42000661,ZNM6,100.0,101.0,99.0,100.5,10",
                "2026-05-18T01:00:00.000000000Z,42000661,ZNM6,100.5,102.0,100.0,101.5,12",
            )
        )
        mapping = {
            self.parse_utc("2026-05-18T00:00:00Z"): "2026-05-18",
            self.parse_utc("2026-05-18T01:00:00Z"): "2026-05-18",
        }

        bars = parse_s26_zn_databento_hourly_ohlcv_csv_text(
            csv_text,
            manifest,
            completed_trading_dates_by_ts_event_start_utc=mapping,
            source_raw_sha256=FIXTURE_RAW_SHA256,
        )

        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0].provider_ts_event_start_utc, self.parse_utc("2026-05-18T00:00:00Z"))
        self.assertEqual(bars[0].derived_completed_bar_end_utc, self.parse_utc("2026-05-18T01:00:00Z"))
        self.assertEqual(bars[0].strategy_use_status, S26_ZN_HOURLY_QUARANTINE_STATUS)
        self.assertEqual(bars[1].close, 101.5)

    def test_s26_zn_hourly_csv_text_parser_fails_closed_on_header_duplicate_and_missing_mapping(self) -> None:
        manifest = self.load_s26_zn_request_manifest()
        mapping = {self.parse_utc("2026-05-18T00:00:00Z"): "2026-05-18"}
        bad_header = "ts_event,instrument_id,raw_symbol,open,high,low,close\n2026-05-18T00:00:00Z,42000661,ZNM6,100,101,99,100.5"
        duplicate = "\n".join(
            (
                ",".join(S26_ZN_DATABENTO_OHLCV_1H_REQUIRED_COLUMNS),
                "2026-05-18T00:00:00Z,42000661,ZNM6,100,101,99,100.5,10",
                "2026-05-18T00:00:00Z,42000661,ZNM6,100,101,99,100.5,10",
            )
        )
        missing_mapping = "\n".join(
            (
                ",".join(S26_ZN_DATABENTO_OHLCV_1H_REQUIRED_COLUMNS),
                "2026-05-18T01:00:00Z,42000661,ZNM6,100,101,99,100.5,10",
            )
        )
        for csv_text in (bad_header, duplicate, missing_mapping):
            with self.subTest(csv_text=csv_text):
                with self.assertRaises(CarverBlocked):
                    parse_s26_zn_databento_hourly_ohlcv_csv_text(
                        csv_text,
                        manifest,
                        completed_trading_dates_by_ts_event_start_utc=mapping,
                        source_raw_sha256=FIXTURE_RAW_SHA256,
                    )

    def test_s26_g_r1b_forecast_handoff_requires_prevalidated_sigma_and_remains_output_only(self) -> None:
        bars = self.normalized_quarantine_bars_for_handoff((100.0, 110.0, 105.0, 95.0, 100.0))
        as_of = bars[-1].derived_completed_bar_end_utc

        result = s26_forecast_only_from_quarantined_zn_hourly_ohlcv_bars(
            bars,
            sigma_runtime=self.locked_sigma_runtime(as_of, value=0.16),
            as_of=as_of,
            source_locks=self.locked_quarantined_source_locks(),
        )

        equilibrium = self.ewma(tuple(bar.close for bar in bars), S26_EQUILIBRIUM_EWMA_SPAN)
        self.assertAlmostEqual(result.equilibrium_ewma_5, equilibrium)
        self.assertEqual(result.forecast_output_status, S26_FORECAST_ONLY_STATUS)
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.position_outputs, ())

    def test_s26_g_r1b_forecast_handoff_fails_closed_on_bad_sigma_or_unavailable_provider_condition(self) -> None:
        bars = self.normalized_quarantine_bars_for_handoff((100.0, 101.0, 102.0, 103.0, 104.0))
        as_of = bars[-1].derived_completed_bar_end_utc
        with self.assertRaises(CarverBlocked):
            s26_forecast_only_from_quarantined_zn_hourly_ohlcv_bars(
                bars,
                sigma_runtime=replace(self.locked_sigma_runtime(as_of), no_lookahead_status="UNRESOLVED"),
                as_of=as_of,
                source_locks=self.locked_quarantined_source_locks(),
            )
        with self.assertRaises(CarverBlocked):
            s26_forecast_only_from_quarantined_zn_hourly_ohlcv_bars(
                (replace(bars[0], provider_condition_status="PROVIDER_CONDITION_DEGRADED"),) + bars[1:],
                sigma_runtime=self.locked_sigma_runtime(as_of),
                as_of=as_of,
                source_locks=self.locked_quarantined_source_locks(),
            )
        with self.assertRaises(CarverBlocked):
            s26_forecast_only_from_quarantined_zn_hourly_ohlcv_bars(
                bars,
                sigma_runtime=replace(self.locked_sigma_runtime(as_of), source_artifact_sha256="not_a_sha256"),
                as_of=as_of,
                source_locks=self.locked_quarantined_source_locks(),
            )

    def test_s26_g_r1c_forecast_series_requires_one_sigma_per_output_and_remains_forecast_only(self) -> None:
        bars = self.normalized_quarantine_bars_for_handoff((100.0, 110.0, 105.0, 95.0, 100.0, 101.0))
        runtimes = tuple(
            self.locked_sigma_runtime(bar.derived_completed_bar_end_utc, value=0.16)
            for bar in bars[S26_EQUILIBRIUM_EWMA_SPAN - 1 :]
        )

        result = s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars(
            S26QuarantinedHourlyForecastSeriesRequest(
                bars=bars,
                sigma_runtimes=runtimes,
                source_locks=self.locked_quarantined_source_locks(),
            )
        )

        self.assertEqual(result.series_output_status, S26_ZN_FORECAST_SERIES_STATUS)
        self.assertEqual(result.input_hourly_rows, len(bars))
        self.assertEqual(len(result.forecast_rows), 2)
        self.assertEqual(result.first_forecast_as_of, bars[4].derived_completed_bar_end_utc)
        self.assertEqual(result.last_forecast_as_of, bars[5].derived_completed_bar_end_utc)
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.position_outputs, ())
        for row in result.forecast_rows:
            self.assertEqual(row.forecast_output_status, S26_FORECAST_ONLY_STATUS)
            self.assertEqual(row.diagnostics_outputs, ())
            self.assertEqual(row.backtest_outputs, ())
            self.assertEqual(row.position_outputs, ())

    def test_s26_g_r1c_forecast_series_fails_closed_on_missing_or_misaligned_sigma(self) -> None:
        bars = self.normalized_quarantine_bars_for_handoff((100.0, 101.0, 102.0, 103.0, 104.0, 105.0))
        runtimes = tuple(
            self.locked_sigma_runtime(bar.derived_completed_bar_end_utc)
            for bar in bars[S26_EQUILIBRIUM_EWMA_SPAN - 1 :]
        )

        with self.assertRaises(CarverBlocked):
            s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars(
                S26QuarantinedHourlyForecastSeriesRequest(
                    bars=bars,
                    sigma_runtimes=runtimes[:1],
                    source_locks=self.locked_quarantined_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars(
                S26QuarantinedHourlyForecastSeriesRequest(
                    bars=bars,
                    sigma_runtimes=(replace(runtimes[0], as_of=runtimes[0].as_of + timedelta(hours=99)),)
                    + runtimes[1:],
                    source_locks=self.locked_quarantined_source_locks(),
                )
            )

    def test_s27_real_hourly_handoff_uses_prevalidated_runtimes_and_remains_forecast_only(self) -> None:
        s26_row = self.s26_forecast_row((100.0, 100.0, 100.0, 100.0, 80.0), sigma_percent=0.16)
        result = s27_forecast_only_from_s26_forecast_row(
            S27QuarantinedHourlyForecastRequest(
                s26_forecast=s26_row,
                trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.25),
                vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=0.75),
                source_locks=self.locked_s27_real_hourly_source_locks(),
            )
        )

        self.assertEqual(result.forecast_output_status, S27_FORECAST_ONLY_STATUS)
        self.assertEqual(result.source_locks_status, S27_FORECAST_HANDOFF_STATUS)
        self.assertFalse(result.opposes_trend)
        self.assertAlmostEqual(result.adjusted_raw_forecast, s26_row.raw_forecast * 0.75)
        self.assertAlmostEqual(result.forecast_scalar, S27_FORECAST_SCALAR)
        self.assertLessEqual(abs(result.capped_forecast), FORECAST_CAP)
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.position_outputs, ())

    def test_s27_real_hourly_handoff_zeroes_opposing_forecast_and_fails_closed_on_unlocked_inputs(self) -> None:
        s26_row = self.s26_forecast_row((100.0, 100.0, 100.0, 100.0, 80.0), sigma_percent=0.16)
        result = s27_forecast_only_from_s26_forecast_row(
            S27QuarantinedHourlyForecastRequest(
                s26_forecast=s26_row,
                trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=-1.25),
                vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.25),
                source_locks=self.locked_s27_real_hourly_source_locks(),
            )
        )

        self.assertTrue(result.opposes_trend)
        self.assertEqual(result.adjusted_raw_forecast, 0.0)
        self.assertEqual(result.capped_forecast, 0.0)

        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=s26_row,
                    trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                    vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.0),
                    source_locks=S27RealHourlySourceLocks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=s26_row,
                    trend_runtime=replace(
                        self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                        source_artifact_sha256="not_a_sha256",
                    ),
                    vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.0),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=replace(s26_row, raw_symbol="MESM6"),
                    trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                    vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.0),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=replace(s26_row, source_locks_status="FORGED_LOCK"),
                    trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                    vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.0),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=s26_row,
                    trend_runtime=replace(
                        self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                        raw_symbol="MESM6",
                    ),
                    vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.0),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=s26_row,
                    trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                    vol_runtime=replace(
                        self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.0),
                        raw_symbol="MESM6",
                    ),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=s26_row,
                    trend_runtime=replace(
                        self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                        as_of=s26_row.derived_completed_bar_end_utc - timedelta(hours=1),
                    ),
                    vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.0),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=s26_row,
                    trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                    vol_runtime=replace(
                        self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=1.0),
                        as_of=s26_row.derived_completed_bar_end_utc - timedelta(hours=1),
                    ),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_only_from_s26_forecast_row(
                S27QuarantinedHourlyForecastRequest(
                    s26_forecast=s26_row,
                    trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                    vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=2.5),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )

    def test_s27_zn_desired_position_plumbing_applies_forecast_over_10_to_prevalidated_base(self) -> None:
        s26_row = self.s26_forecast_row((100.0, 100.0, 100.0, 100.0, 80.0), sigma_percent=0.16)
        forecast = s27_forecast_only_from_s26_forecast_row(
            S27QuarantinedHourlyForecastRequest(
                s26_forecast=s26_row,
                trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=0.75),
                source_locks=self.locked_s27_real_hourly_source_locks(),
            )
        )
        base_position = self.locked_s27_base_position(forecast.as_of, base_unrounded_contracts=3.25)

        result = s27_zn_desired_position_from_prevalidated_base(
            S27ZNDesiredPositionRequest(
                forecast=forecast,
                base_position=base_position,
                rounding_policy=RoundingPolicy.NEAREST,
                semantics_lock=build_s27_zn_position_execution_cost_semantics_lock(),
                position_output_authorization_status="PREVALIDATED_POSITION_PLUMBING_ONLY",
            )
        )

        self.assertEqual(result.position_output_status, S27_ZN_DESIRED_POSITION_PLUMBING_STATUS)
        self.assertEqual(result.forecast_to_position_divisor, 10.0)
        self.assertAlmostEqual(result.forecast_multiplier, forecast.capped_forecast / 10.0)
        self.assertAlmostEqual(result.desired_unrounded_contracts, 3.25 * forecast.capped_forecast / 10.0)
        self.assertEqual(result.desired_rounded_contracts, round(result.desired_unrounded_contracts))
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.return_outputs, ())
        self.assertEqual(result.pnl_outputs, ())
        self.assertEqual(result.cost_outputs, ())

    def test_s27_zn_desired_position_plumbing_fails_closed_on_unlocked_or_drifted_inputs(self) -> None:
        s26_row = self.s26_forecast_row((100.0, 100.0, 100.0, 100.0, 80.0), sigma_percent=0.16)
        forecast = s27_forecast_only_from_s26_forecast_row(
            S27QuarantinedHourlyForecastRequest(
                s26_forecast=s26_row,
                trend_runtime=self.locked_s27_trend_runtime(s26_row.derived_completed_bar_end_utc, trend_forecast=1.0),
                vol_runtime=self.locked_s27_vol_runtime(s26_row.derived_completed_bar_end_utc, vol_multiplier=0.75),
                source_locks=self.locked_s27_real_hourly_source_locks(),
            )
        )
        base_position = self.locked_s27_base_position(forecast.as_of, base_unrounded_contracts=3.25)
        semantics_lock = build_s27_zn_position_execution_cost_semantics_lock()
        bad_requests = (
            S27ZNDesiredPositionRequest(
                forecast=replace(forecast, row_id="APPENDIX_C_174_006"),
                base_position=base_position,
                rounding_policy=RoundingPolicy.NEAREST,
                semantics_lock=semantics_lock,
                position_output_authorization_status="PREVALIDATED_POSITION_PLUMBING_ONLY",
            ),
            S27ZNDesiredPositionRequest(
                forecast=forecast,
                base_position=replace(base_position, as_of=forecast.as_of + timedelta(hours=1)),
                rounding_policy=RoundingPolicy.NEAREST,
                semantics_lock=semantics_lock,
                position_output_authorization_status="PREVALIDATED_POSITION_PLUMBING_ONLY",
            ),
            S27ZNDesiredPositionRequest(
                forecast=forecast,
                base_position=replace(base_position, source_status="UNLOCKED"),
                rounding_policy=RoundingPolicy.NEAREST,
                semantics_lock=semantics_lock,
                position_output_authorization_status="PREVALIDATED_POSITION_PLUMBING_ONLY",
            ),
            S27ZNDesiredPositionRequest(
                forecast=forecast,
                base_position=base_position,
                rounding_policy=RoundingPolicy.TRUNCATE,
                semantics_lock=semantics_lock,
                position_output_authorization_status="PREVALIDATED_POSITION_PLUMBING_ONLY",
            ),
            S27ZNDesiredPositionRequest(
                forecast=forecast,
                base_position=base_position,
                rounding_policy=RoundingPolicy.NEAREST,
                semantics_lock=replace(semantics_lock, forecast_to_position_policy="FINAL_FORECAST_DIVIDED_BY_20"),
                position_output_authorization_status="PREVALIDATED_POSITION_PLUMBING_ONLY",
            ),
            S27ZNDesiredPositionRequest(
                forecast=forecast,
                base_position=base_position,
                rounding_policy=RoundingPolicy.NEAREST,
                semantics_lock=semantics_lock,
                position_output_authorization_status="REAL_POSITION_OUTPUT_AUTHORIZED",
            ),
        )
        for request in bad_requests:
            with self.subTest(request=request):
                with self.assertRaises(CarverBlocked):
                    s27_zn_desired_position_from_prevalidated_base(request)

        with self.assertRaises(CarverBlocked):
            s27_zn_desired_position_from_prevalidated_base(
                S27ZNDesiredPositionRequest(
                    forecast=forecast,
                    base_position=base_position,
                    rounding_policy=RoundingPolicy.NEAREST,
                    semantics_lock=semantics_lock,
                    position_output_authorization_status="PREVALIDATED_POSITION_PLUMBING_ONLY",
                    lane_class=LaneClass.CFD_ADAPTER,
                )
            )

    def test_s27_real_hourly_series_handoff_consumes_s26_series_and_runtime_rows_only(self) -> None:
        s26_series = self.s26_forecast_series((100.0, 100.0, 100.0, 100.0, 80.0, 81.0), sigma_percent=0.16)
        trend_runtimes = tuple(
            self.locked_s27_trend_runtime(row.derived_completed_bar_end_utc, trend_forecast=1.0)
            for row in s26_series.forecast_rows
        )
        vol_runtimes = tuple(
            self.locked_s27_vol_runtime(row.derived_completed_bar_end_utc, vol_multiplier=0.75)
            for row in s26_series.forecast_rows
        )

        result = s27_forecast_series_only_from_s26_forecast_series(
            S27QuarantinedHourlyForecastSeriesRequest(
                s26_forecast_series=s26_series,
                trend_runtimes=trend_runtimes,
                vol_runtimes=vol_runtimes,
                source_locks=self.locked_s27_real_hourly_source_locks(),
            )
        )

        self.assertEqual(result.series_output_status, S27_FORECAST_SERIES_STATUS)
        self.assertEqual(result.input_s26_forecast_rows, len(s26_series.forecast_rows))
        self.assertEqual(len(result.forecast_rows), 2)
        self.assertEqual(result.first_forecast_as_of, s26_series.first_forecast_as_of)
        self.assertEqual(result.last_forecast_as_of, s26_series.last_forecast_as_of)
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.position_outputs, ())
        for row in result.forecast_rows:
            self.assertEqual(row.forecast_output_status, S27_FORECAST_ONLY_STATUS)
            self.assertEqual(row.diagnostics_outputs, ())
            self.assertEqual(row.backtest_outputs, ())
            self.assertEqual(row.position_outputs, ())

    def test_s27_real_hourly_series_handoff_fails_closed_on_runtime_count_order_and_identity_drift(self) -> None:
        s26_series = self.s26_forecast_series((100.0, 101.0, 102.0, 103.0, 90.0, 91.0), sigma_percent=0.16)
        trend_runtimes = tuple(
            self.locked_s27_trend_runtime(row.derived_completed_bar_end_utc, trend_forecast=1.0)
            for row in s26_series.forecast_rows
        )
        vol_runtimes = tuple(
            self.locked_s27_vol_runtime(row.derived_completed_bar_end_utc, vol_multiplier=1.0)
            for row in s26_series.forecast_rows
        )

        with self.assertRaises(CarverBlocked):
            s27_forecast_series_only_from_s26_forecast_series(
                S27QuarantinedHourlyForecastSeriesRequest(
                    s26_forecast_series=s26_series,
                    trend_runtimes=trend_runtimes[:1],
                    vol_runtimes=vol_runtimes,
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_series_only_from_s26_forecast_series(
                S27QuarantinedHourlyForecastSeriesRequest(
                    s26_forecast_series=s26_series,
                    trend_runtimes=(replace(trend_runtimes[0], as_of=trend_runtimes[0].as_of + timedelta(hours=99)),)
                    + trend_runtimes[1:],
                    vol_runtimes=vol_runtimes,
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_series_only_from_s26_forecast_series(
                S27QuarantinedHourlyForecastSeriesRequest(
                    s26_forecast_series=s26_series,
                    trend_runtimes=trend_runtimes,
                    vol_runtimes=vol_runtimes[:1],
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_series_only_from_s26_forecast_series(
                S27QuarantinedHourlyForecastSeriesRequest(
                    s26_forecast_series=s26_series,
                    trend_runtimes=trend_runtimes,
                    vol_runtimes=(replace(vol_runtimes[0], as_of=vol_runtimes[0].as_of + timedelta(hours=99)),)
                    + vol_runtimes[1:],
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_series_only_from_s26_forecast_series(
                S27QuarantinedHourlyForecastSeriesRequest(
                    s26_forecast_series=s26_series,
                    trend_runtimes=trend_runtimes,
                    vol_runtimes=(vol_runtimes[0], vol_runtimes[0]),
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_series_only_from_s26_forecast_series(
                S27QuarantinedHourlyForecastSeriesRequest(
                    s26_forecast_series=replace(s26_series, raw_symbol="MESM6"),
                    trend_runtimes=trend_runtimes,
                    vol_runtimes=vol_runtimes,
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )
        with self.assertRaises(CarverBlocked):
            s27_forecast_series_only_from_s26_forecast_series(
                S27QuarantinedHourlyForecastSeriesRequest(
                    s26_forecast_series=replace(
                        s26_series,
                        forecast_rows=(replace(s26_series.forecast_rows[0], raw_symbol="MESM6"),)
                        + s26_series.forecast_rows[1:],
                    ),
                    trend_runtimes=trend_runtimes,
                    vol_runtimes=vol_runtimes,
                    source_locks=self.locked_s27_real_hourly_source_locks(),
                )
            )

    def test_s27_ewmac16_trend_runtime_ledger_accepts_prevalidated_rows_only(self) -> None:
        s26_series = self.s26_forecast_series((100.0, 100.5, 101.0, 101.5, 90.0, 91.0), sigma_percent=0.16)
        trend_runtimes = tuple(
            self.locked_s27_trend_runtime(row.derived_completed_bar_end_utc, trend_forecast=0.25 + index)
            for index, row in enumerate(s26_series.forecast_rows)
        )

        result = s27_trend_overlay_runtime_ledger_from_prevalidated_rows(
            S27TrendOverlayRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                trend_runtimes=trend_runtimes,
                source_locks=self.locked_s27_trend_ledger_source_locks(),
            )
        )

        self.assertEqual(result.ledger_status, S27_TREND_RUNTIME_LEDGER_STATUS)
        self.assertEqual(result.input_s26_forecast_rows, len(s26_series.forecast_rows))
        self.assertEqual(result.first_runtime_as_of, s26_series.first_forecast_as_of)
        self.assertEqual(result.last_runtime_as_of, s26_series.last_forecast_as_of)
        self.assertEqual(result.trend_runtimes, trend_runtimes)
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.position_outputs, ())

    def test_s27_ewmac16_trend_runtime_ledger_fails_closed_on_unlocked_missing_shifted_duplicate_or_wrong_identity(self) -> None:
        s26_series = self.s26_forecast_series((100.0, 100.5, 101.0, 101.5, 90.0, 91.0), sigma_percent=0.16)
        trend_runtimes = tuple(
            self.locked_s27_trend_runtime(row.derived_completed_bar_end_utc, trend_forecast=1.0)
            for row in s26_series.forecast_rows
        )

        bad_requests = (
            S27TrendOverlayRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                trend_runtimes=trend_runtimes,
                source_locks=S27TrendOverlayRuntimeLedgerSourceLocks(),
            ),
            S27TrendOverlayRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                trend_runtimes=trend_runtimes[:1],
                source_locks=self.locked_s27_trend_ledger_source_locks(),
            ),
            S27TrendOverlayRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                trend_runtimes=(replace(trend_runtimes[0], as_of=trend_runtimes[0].as_of + timedelta(hours=99)),)
                + trend_runtimes[1:],
                source_locks=self.locked_s27_trend_ledger_source_locks(),
            ),
            S27TrendOverlayRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                trend_runtimes=(trend_runtimes[0], trend_runtimes[0]),
                source_locks=self.locked_s27_trend_ledger_source_locks(),
            ),
            S27TrendOverlayRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                trend_runtimes=(replace(trend_runtimes[0], raw_symbol="MESM6"),) + trend_runtimes[1:],
                source_locks=self.locked_s27_trend_ledger_source_locks(),
            ),
            S27TrendOverlayRuntimeLedgerRequest(
                s26_forecast_series=replace(s26_series, raw_symbol="MESM6"),
                trend_runtimes=trend_runtimes,
                source_locks=self.locked_s27_trend_ledger_source_locks(),
            ),
        )
        for request in bad_requests:
            with self.subTest(request=request):
                with self.assertRaises(CarverBlocked):
                    s27_trend_overlay_runtime_ledger_from_prevalidated_rows(request)

    def test_s27_vqm_vol_runtime_ledger_accepts_prevalidated_rows_only(self) -> None:
        s26_series = self.s26_forecast_series((100.0, 100.5, 101.0, 101.5, 90.0, 91.0), sigma_percent=0.16)
        vol_runtimes = tuple(
            self.locked_s27_vol_runtime(row.derived_completed_bar_end_utc, vol_multiplier=0.75 + 0.25 * index)
            for index, row in enumerate(s26_series.forecast_rows)
        )

        result = s27_vol_attenuation_runtime_ledger_from_prevalidated_rows(
            S27VolAttenuationRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                vol_runtimes=vol_runtimes,
                source_locks=self.locked_s27_vol_ledger_source_locks(),
            )
        )

        self.assertEqual(result.ledger_status, S27_VOL_ATTENUATION_RUNTIME_LEDGER_STATUS)
        self.assertEqual(result.input_s26_forecast_rows, len(s26_series.forecast_rows))
        self.assertEqual(result.first_runtime_as_of, s26_series.first_forecast_as_of)
        self.assertEqual(result.last_runtime_as_of, s26_series.last_forecast_as_of)
        self.assertEqual(result.vol_runtimes, vol_runtimes)
        self.assertEqual(result.diagnostics_outputs, ())
        self.assertEqual(result.backtest_outputs, ())
        self.assertEqual(result.position_outputs, ())

    def test_s27_vqm_vol_runtime_ledger_fails_closed_on_unlocked_missing_shifted_duplicate_bad_envelope_or_wrong_identity(self) -> None:
        s26_series = self.s26_forecast_series((100.0, 100.5, 101.0, 101.5, 90.0, 91.0), sigma_percent=0.16)
        vol_runtimes = tuple(
            self.locked_s27_vol_runtime(row.derived_completed_bar_end_utc, vol_multiplier=1.0)
            for row in s26_series.forecast_rows
        )

        bad_requests = (
            S27VolAttenuationRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                vol_runtimes=vol_runtimes,
                source_locks=S27VolAttenuationRuntimeLedgerSourceLocks(),
            ),
            S27VolAttenuationRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                vol_runtimes=vol_runtimes[:1],
                source_locks=self.locked_s27_vol_ledger_source_locks(),
            ),
            S27VolAttenuationRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                vol_runtimes=(replace(vol_runtimes[0], as_of=vol_runtimes[0].as_of + timedelta(hours=99)),)
                + vol_runtimes[1:],
                source_locks=self.locked_s27_vol_ledger_source_locks(),
            ),
            S27VolAttenuationRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                vol_runtimes=(vol_runtimes[0], vol_runtimes[0]),
                source_locks=self.locked_s27_vol_ledger_source_locks(),
            ),
            S27VolAttenuationRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                vol_runtimes=(replace(vol_runtimes[0], vol_multiplier=2.5),) + vol_runtimes[1:],
                source_locks=self.locked_s27_vol_ledger_source_locks(),
            ),
            S27VolAttenuationRuntimeLedgerRequest(
                s26_forecast_series=s26_series,
                vol_runtimes=(replace(vol_runtimes[0], raw_symbol="MESM6"),) + vol_runtimes[1:],
                source_locks=self.locked_s27_vol_ledger_source_locks(),
            ),
            S27VolAttenuationRuntimeLedgerRequest(
                s26_forecast_series=replace(s26_series, raw_symbol="MESM6"),
                vol_runtimes=vol_runtimes,
                source_locks=self.locked_s27_vol_ledger_source_locks(),
            ),
        )
        for request in bad_requests:
            with self.subTest(request=request):
                with self.assertRaises(CarverBlocked):
                    s27_vol_attenuation_runtime_ledger_from_prevalidated_rows(request)

    def s26_for_values(self, values: tuple[float, ...], *, sigma_percent: float):
        prices = self.prices(values)
        return s26_fast_mean_reversion_forecast(
            S26FastMeanReversionRequest(
                prices=prices,
                as_of=prices[-1].timestamp,
                sigma_percent=TimedValue(sigma_percent, prices[-1].timestamp),
            )
        )

    def s27_request(
        self,
        prices: tuple[SyntheticHourlyPrice, ...],
        *,
        vol_quantiles: tuple[SyntheticQuantilePoint, ...] | None = None,
        sigma_percent: float = 0.16,
        s27_source_locks: S27SourceLocks | None = None,
    ) -> S27SaferFastMeanReversionRequest:
        return S27SaferFastMeanReversionRequest(
            prices=prices,
            as_of=prices[-1].timestamp,
            sigma_percent=TimedValue(sigma_percent, prices[-1].timestamp),
            vol_quantiles=vol_quantiles
            or tuple(
                SyntheticQuantilePoint("synthetic_mid_vol_quantile", price.timestamp, 0.5)
                for price in prices[-S27_VOL_ATTENUATION_SPAN:]
            ),
            s27_source_locks=s27_source_locks or S27SourceLocks(),
        )

    def prices(self, values: tuple[float, ...]) -> tuple[SyntheticHourlyPrice, ...]:
        return tuple(
            SyntheticHourlyPrice("synthetic_hourly_price_path", self.start + timedelta(hours=index), value)
            for index, value in enumerate(values)
        )

    def zn_quarantined_bars(self, values: tuple[float, ...]) -> tuple[S26QuarantinedHourlyZNBar, ...]:
        return tuple(
            S26QuarantinedHourlyZNBar(
                row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
                author_market_code="ZN",
                instrument_id=S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
                raw_symbol=S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
                provider_ts_event_start_utc=self.start + timedelta(hours=index),
                derived_completed_bar_end_utc=self.start + timedelta(hours=index + 1),
                completed_trading_date="2026-05-18",
                close=value,
                strategy_use_status="S26_FORECAST_INPUT_READY_QUARANTINE_ONLY",
            )
            for index, value in enumerate(values)
        )

    def locked_quarantined_source_locks(self) -> S26QuarantinedHourlySourceLocks:
        return S26QuarantinedHourlySourceLocks(
            hourly_intake_status=SourceRuleStatus.LOCKED,
            session_mapping_status=SourceRuleStatus.LOCKED,
            provider_condition_status=SourceRuleStatus.LOCKED,
            sigma_percent_status=SourceRuleStatus.LOCKED,
            forecast_output_boundary_status=SourceRuleStatus.LOCKED,
            no_diagnostics_status=SourceRuleStatus.LOCKED,
            no_backtests_status=SourceRuleStatus.LOCKED,
            no_positions_status=SourceRuleStatus.LOCKED,
        )

    def locked_s27_real_hourly_source_locks(self) -> S27RealHourlySourceLocks:
        return S27RealHourlySourceLocks(
            s26_forecast_row_status=SourceRuleStatus.LOCKED,
            trend_overlay_runtime_status=SourceRuleStatus.LOCKED,
            vol_attenuation_runtime_status=SourceRuleStatus.LOCKED,
            s27_scalar_and_cap_status=SourceRuleStatus.LOCKED,
            no_fdm_status=SourceRuleStatus.LOCKED,
            no_buffering_status=SourceRuleStatus.LOCKED,
            output_boundary_status=SourceRuleStatus.LOCKED,
        )

    def locked_s27_trend_ledger_source_locks(self) -> S27TrendOverlayRuntimeLedgerSourceLocks:
        return S27TrendOverlayRuntimeLedgerSourceLocks(
            s26_forecast_series_status=SourceRuleStatus.LOCKED,
            trend_overlay_runtime_status=SourceRuleStatus.LOCKED,
            no_lookahead_status=SourceRuleStatus.LOCKED,
            output_boundary_status=SourceRuleStatus.LOCKED,
        )

    def locked_s27_vol_ledger_source_locks(self) -> S27VolAttenuationRuntimeLedgerSourceLocks:
        return S27VolAttenuationRuntimeLedgerSourceLocks(
            s26_forecast_series_status=SourceRuleStatus.LOCKED,
            vol_attenuation_runtime_status=SourceRuleStatus.LOCKED,
            no_lookahead_status=SourceRuleStatus.LOCKED,
            output_boundary_status=SourceRuleStatus.LOCKED,
        )

    def locked_s27_trend_runtime(self, as_of: datetime, *, trend_forecast: float) -> S27TrendOverlayRuntimeValue:
        return S27TrendOverlayRuntimeValue(
            row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
            author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
            instrument_id=S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
            raw_symbol=S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
            as_of=as_of,
            trend_fast_ewma=101.0 + trend_forecast,
            trend_slow_ewma=101.0,
            trend_forecast=trend_forecast,
            runtime_status=S27_TREND_RUNTIME_STATUS,
            method_status="LOCKED_EWMAC16_TREND_OVERLAY_RUNTIME",
            no_lookahead_status="PASS_NO_LOOKAHEAD",
            source_artifact_sha256="B" * 64,
        )

    def locked_s27_vol_runtime(self, as_of: datetime, *, vol_multiplier: float) -> S27VolAttenuationRuntimeValue:
        return S27VolAttenuationRuntimeValue(
            row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
            author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
            instrument_id=S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
            raw_symbol=S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
            as_of=as_of,
            vol_multiplier=vol_multiplier,
            runtime_status=S27_VOL_ATTENUATION_RUNTIME_STATUS,
            method_status="LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME",
            no_lookahead_status="PASS_NO_LOOKAHEAD",
            source_artifact_sha256="C" * 64,
        )

    def locked_s27_base_position(self, as_of: datetime, *, base_unrounded_contracts: float) -> S27ZNPrevalidatedBasePosition:
        return S27ZNPrevalidatedBasePosition(
            row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
            author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
            as_of=as_of,
            base_unrounded_contracts=base_unrounded_contracts,
            source_status="PREVALIDATED_M1_BASE_POSITION_LOCKED",
            capital_risk_status="CAPITAL_TARGET_RISK_ANNUAL_RISK_LOCKED_NO_LOOKAHEAD",
            multiplier_fx_status="ZN_MULTIPLIER_USD_FX_LOCKED",
            source_artifact_sha256="E" * 64,
        )

    def s26_forecast_row(self, closes: tuple[float, ...], *, sigma_percent: float):
        bars = self.normalized_quarantine_bars_for_handoff(closes)
        as_of = bars[-1].derived_completed_bar_end_utc
        return s26_forecast_only_from_quarantined_zn_hourly_ohlcv_bars(
            bars,
            sigma_runtime=self.locked_sigma_runtime(as_of, value=sigma_percent),
            as_of=as_of,
            source_locks=self.locked_quarantined_source_locks(),
        )

    def s26_forecast_series(self, closes: tuple[float, ...], *, sigma_percent: float):
        bars = self.normalized_quarantine_bars_for_handoff(closes)
        runtimes = tuple(
            self.locked_sigma_runtime(bar.derived_completed_bar_end_utc, value=sigma_percent)
            for bar in bars[S26_EQUILIBRIUM_EWMA_SPAN - 1 :]
        )
        return s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars(
            S26QuarantinedHourlyForecastSeriesRequest(
                bars=bars,
                sigma_runtimes=runtimes,
                source_locks=self.locked_quarantined_source_locks(),
            )
        )

    def load_s26_zn_request_manifest(self) -> S26DatabentoHourlyIntakeRequestManifest:
        path = (
            ROOT
            / "docs"
            / "researchops"
            / "s26_s27_hourly_bridge"
            / "ZN_S26_WORKED_EXAMPLE"
            / "2026-05-18_2026-05-22"
            / "request_manifest"
            / "CARVER_S26_ZN_DATABENTO_OHLCV_1H_REQUEST_MANIFEST_2026-05-30.json"
        )
        raw = json.loads(path.read_text(encoding="utf-8"))
        return S26DatabentoHourlyIntakeRequestManifest(
            status=raw["status"],
            provider=raw["provider"],
            dataset=raw["dataset"],
            schema=raw["schema"],
            stype_in=raw["stype_in"],
            symbols=tuple(raw["symbols"]),
            row_id=raw["row_id"],
            author_market_code=raw["author_market_code"],
            expected_raw_symbol=raw["expected_raw_symbol"],
            request_start_utc=self.parse_utc(raw["request_start_utc"]),
            request_end_utc=self.parse_utc(raw["request_end_utc"]),
            target_completed_trading_dates=tuple(raw["target_completed_trading_dates"]),
            continuous_contracts_status=raw["continuous_contracts_status"],
            parent_symbols_status=raw["parent_symbols_status"],
            raw_symbol_selector_status=raw["raw_symbol_selector_status"],
            output_root=raw["output_root"],
            no_authorization=tuple(raw["no_authorization"]),
        )

    def raw_zn_hourly_row(self, timestamp: datetime, *, close: float = 101.0) -> S26DatabentoHourlyOHLCVRawRow:
        return S26DatabentoHourlyOHLCVRawRow(
            provider=S26_ZN_DATABENTO_PROVIDER,
            dataset=S26_ZN_DATABENTO_DATASET,
            schema=S26_ZN_DATABENTO_SCHEMA,
            stype_in=S26_ZN_DATABENTO_STYPE_IN,
            row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
            author_market_code="ZN",
            instrument_id=S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
            raw_symbol=S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
            provider_ts_event_start_utc=timestamp,
            open=100.0,
            high=max(102.0, close),
            low=99.0,
            close=close,
            volume=10.0,
            source_raw_sha256=FIXTURE_RAW_SHA256,
            provider_condition_status="PROVIDER_CONDITION_FIXTURE_NOT_MARKET_DATA",
        )

    def normalized_quarantine_bars_for_handoff(self, closes: tuple[float, ...]):
        manifest = self.load_s26_zn_request_manifest()
        return tuple(
            replace(
                normalize_s26_zn_databento_hourly_ohlcv_raw_row(
                    replace(
                        self.raw_zn_hourly_row(self.start + timedelta(hours=index)),
                        close=close,
                        high=max(102.0, close),
                        low=min(99.0, close),
                    ),
                    manifest,
                    completed_trading_date="2026-05-18",
                ),
                provider_condition_status="PROVIDER_CONDITION_AVAILABLE",
            )
            for index, close in enumerate(closes)
        )

    def locked_sigma_runtime(self, as_of: datetime, *, value: float = 0.16) -> S26SigmaPercentRuntimeValue:
        return S26SigmaPercentRuntimeValue(
            value=value,
            as_of=as_of,
            runtime_status=S26_ZN_SIGMA_RUNTIME_STATUS,
            method_status="LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY",
            no_lookahead_status="PASS_NO_LOOKAHEAD",
            source_artifact_sha256="A" * 64,
            source_window_status="PASS_SOURCE_WINDOW_PREVALIDATED",
        )

    def parse_utc(self, value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def uptrend_with_final(self, final_price: float) -> tuple[SyntheticHourlyPrice, ...]:
        values = tuple(100.0 + index for index in range(S27_TREND_SLOW_SPAN - 1)) + (final_price,)
        return self.prices(values)

    def downtrend_with_final(self, final_price: float) -> tuple[SyntheticHourlyPrice, ...]:
        values = tuple(200.0 - index for index in range(S27_TREND_SLOW_SPAN - 1)) + (final_price,)
        return self.prices(values)

    def ewma(self, values: tuple[float, ...], span: int) -> float:
        alpha = 2.0 / (span + 1.0)
        smoothed = values[0]
        for value in values[1:]:
            smoothed = alpha * value + (1.0 - alpha) * smoothed
        return smoothed


if __name__ == "__main__":
    unittest.main()

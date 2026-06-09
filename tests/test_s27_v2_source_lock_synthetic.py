from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked  # noqa: E402
from carver.spine.m1 import RoundingPolicy  # noqa: E402
from carver.spine.s27_v2 import (  # noqa: E402
    FORECAST_CAP,
    S26_V2_FORECAST_SCALAR,
    S27_V2_ANNUAL_PERCENTAGE_SIGMA_SOURCE_STATUS,
    S27_V2_FORECAST_SCALAR,
    S27_V2_FORECAST_SCALAR_BOOK_TEXT,
    S27_V2_DAILY_ROW_READY_STATUS,
    S27_V2_HOURLY_ROW_READY_STATUS,
    S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
    S27_V2_LEVEL_COMPATIBILITY_STATUS,
    S27V2FillCostTreatment,
    S27V2FillRow,
    S27V2ForecastContext,
    S27V2HourlyRuntimeInput,
    S27V2OrderKind,
    S27V2OrderSide,
    S27V2SessionTransitionKind,
    S27V2SourceLock,
    S27V2WorkingOrderState,
    S27V2DailyRuntimeInput,
    S27_V2_ROLL_STATE_RESET_ASSUMPTION_STATUS,
    build_s27_v2_daily_runtime_rows,
    build_s27_v2_multi_row_replay_ledger_bundle,
    build_s27_v2_replay_step_ledger_bundle,
    build_s27_v2_cost_ledger_rows,
    build_s27_v2_desired_position_row,
    build_s27_v2_forecast_replay_row,
    build_s27_v2_order_plan,
    build_s27_v2_pnl_ledger_row,
    fill_s27_v2_order_plan_one_hour_lag,
    implied_price_for_target_position,
    open_s27_v2_working_order_state,
    transition_s27_v2_working_order_state_one_hour,
    _overnight_gap_market_fills,
)


class S27V2SourceLockSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.day0 = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def test_source_lock_scalar_is_book_approximate_implementation_freeze(self) -> None:
        lock = S27V2SourceLock()

        lock.validate()

        self.assertEqual(lock.scalar_book_text, S27_V2_FORECAST_SCALAR_BOOK_TEXT)
        self.assertEqual(lock.scalar_implementation_freeze, S27_V2_FORECAST_SCALAR)
        self.assertEqual(S26_V2_FORECAST_SCALAR, 9.3)
        with self.assertRaises(CarverBlocked):
            S27V2SourceLock(scalar_implementation_freeze=9.3).validate()

    def test_daily_runtime_builds_ewma_trend_and_expanding_vqm(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 101.0, 102.0),
            current_contract=(100.0, 101.0, 102.0),
            sigma=(0.10, 0.20, 0.10),
        )

        runtime = build_s27_v2_daily_runtime_rows(rows)

        self.assertEqual(len(runtime), 3)
        self.assertAlmostEqual(runtime[0].equilibrium_ewma5, 100.0)
        self.assertGreater(runtime[2].trend_forecast, 0.0)
        self.assertAlmostEqual(runtime[0].relative_volatility_v, 1.0)
        self.assertAlmostEqual(runtime[0].quantile_q, 1.0)
        self.assertAlmostEqual(runtime[1].relative_volatility_v, 0.20 / 0.15)
        self.assertEqual(runtime[1].q_source_observation_count, 2)
        self.assertGreater(runtime[2].vol_multiplier_m, 0.0)

    def test_forecast_replay_uses_sigma_bridge_then_veto_then_vqm_then_scalar(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        hourly = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )

        replay = build_s27_v2_forecast_replay_row(
            hourly_row=hourly,
            daily_input=rows[-1],
            daily_runtime=runtime[-1],
            daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
        )

        expected_sigma_price = 99.0 * 0.16 / 16.0
        expected_risk = replay.raw_forecast / expected_sigma_price
        self.assertAlmostEqual(replay.sigma_price, expected_sigma_price)
        self.assertAlmostEqual(replay.risk_adjusted_forecast_before_veto, expected_risk)
        self.assertFalse(replay.trend_veto_applied)
        self.assertAlmostEqual(
            replay.adjusted_risk_adjusted_forecast,
            replay.risk_adjusted_forecast_after_veto * replay.vol_multiplier_m,
        )
        self.assertEqual(replay.scalar_book_text, "AROUND_20")
        self.assertEqual(replay.scalar, 20.0)
        self.assertLessEqual(abs(replay.capped_forecast), FORECAST_CAP)

    def test_forecast_replay_requires_prevalidated_statuses_and_level_compatibility(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        hourly = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_forecast_replay_row(
                hourly_row=hourly,
                daily_input=S27V2DailyRuntimeInput(
                    completed_trading_date=rows[-1].completed_trading_date,
                    completed_bar_timestamp=rows[-1].completed_bar_timestamp,
                    continuous_close=rows[-1].continuous_close,
                    current_traded_contract_close=rows[-1].current_traded_contract_close,
                    annual_percentage_sigma=rows[-1].annual_percentage_sigma,
                    source_status=S27_V2_DAILY_ROW_READY_STATUS,
                    level_compatibility_status="UNRESOLVED",
                    annual_percentage_sigma_source_status=S27_V2_ANNUAL_PERCENTAGE_SIGMA_SOURCE_STATUS,
                ),
                daily_runtime=runtime[-1],
                daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
            )
        with self.assertRaises(CarverBlocked):
            build_s27_v2_forecast_replay_row(
                hourly_row=S27V2HourlyRuntimeInput(
                    completed_bar_end_utc=hourly.completed_bar_end_utc,
                    completed_trading_date=hourly.completed_trading_date,
                    raw_symbol=hourly.raw_symbol,
                    open=hourly.open,
                    high=hourly.high,
                    low=hourly.low,
                    close=hourly.close,
                    provider_condition_status="PROVIDER_CONDITION_DEGRADED",
                ),
                daily_input=rows[-1],
                daily_runtime=runtime[-1],
                daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
            )
        with self.assertRaises(CarverBlocked):
            build_s27_v2_forecast_replay_row(
                hourly_row=hourly,
                daily_input=rows[-1],
                daily_runtime=replace(runtime[-1], current_traded_contract_close=123.0),
                daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
            )

    def test_runtime_inputs_default_to_fail_closed_without_explicit_readiness(self) -> None:
        with self.assertRaises(CarverBlocked):
            S27V2DailyRuntimeInput(
                completed_trading_date="2026-01-01",
                completed_bar_timestamp=self.day0,
                continuous_close=100.0,
                current_traded_contract_close=100.0,
                annual_percentage_sigma=0.16,
            ).validate()
        with self.assertRaises(CarverBlocked):
            S27V2HourlyRuntimeInput(
                completed_bar_end_utc=self.day0 + timedelta(hours=14),
                completed_trading_date="2026-01-01",
                raw_symbol="ZNM6",
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.0,
            ).validate()

    def test_direct_forecast_replay_requires_latest_strict_prior_certification(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        hourly = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_forecast_replay_row(
                hourly_row=hourly,
                daily_input=rows[-1],
                daily_runtime=runtime[-1],
            )

    def test_forecast_replay_vetoes_opposing_trend_and_allows_zero_flat_boundary(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(100.0, 100.0, 100.0, 100.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        opposing = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=110.0,
            high=111.0,
            low=109.0,
            close=110.0,
        )

        replay = build_s27_v2_forecast_replay_row(
            hourly_row=opposing,
            daily_input=rows[-1],
            daily_runtime=runtime[-1],
            daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
        )

        self.assertTrue(replay.trend_veto_applied)
        self.assertEqual(replay.risk_adjusted_forecast_after_veto, 0.0)
        self.assertEqual(replay.capped_forecast, 0.0)
        zero_raw = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=runtime[-1].equilibrium_ewma5,
            high=runtime[-1].equilibrium_ewma5,
            low=runtime[-1].equilibrium_ewma5,
            close=runtime[-1].equilibrium_ewma5,
        )
        flat_replay = build_s27_v2_forecast_replay_row(
            hourly_row=zero_raw,
            daily_input=rows[-1],
            daily_runtime=runtime[-1],
            daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
        )
        self.assertFalse(flat_replay.trend_veto_applied)
        self.assertEqual(flat_replay.raw_forecast, 0.0)
        self.assertEqual(flat_replay.capped_forecast, 0.0)
        with self.assertRaises(CarverBlocked):
            build_s27_v2_forecast_replay_row(
                hourly_row=opposing,
                daily_input=rows[-1],
                daily_runtime=replace(runtime[-1], trend_forecast=0.0),
                daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
            )

    def test_forecast_replay_requires_strict_prior_daily_row(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0),
            current_contract=(100.0, 100.0),
            sigma=(0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        hourly = self.hourly_row(
            end=self.day0 + timedelta(days=1),
            trading_date="2026-01-02",
            open_price=99.0,
            high=100.0,
            low=98.0,
            close=99.0,
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_forecast_replay_row(
                hourly_row=hourly,
                daily_input=rows[-1],
                daily_runtime=runtime[-1],
                daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
            )

    def test_desired_position_uses_forecast_divisor_and_rounding(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        replay = build_s27_v2_forecast_replay_row(
            hourly_row=self.hourly_row(
                end=self.day0 + timedelta(days=4, hours=14),
                trading_date="2026-01-05",
                open_price=105.0,
                high=106.0,
                low=104.0,
                close=105.0,
            ),
            daily_input=rows[-1],
            daily_runtime=runtime[-1],
            daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
        )

        position = build_s27_v2_desired_position_row(
            replay,
            base_position_contracts=3.0,
            rounding_policy=RoundingPolicy.NEAREST,
        )

        self.assertAlmostEqual(position.desired_unrounded_contracts, replay.capped_forecast / 10.0 * 3.0)
        self.assertEqual(position.desired_rounded_contracts, round(position.desired_unrounded_contracts))
        with self.assertRaises(CarverBlocked):
            build_s27_v2_desired_position_row(
                replay,
                base_position_contracts=3.0,
                rounding_policy=RoundingPolicy.FLOOR,
            )

    def test_order_plan_uses_target_position_trend_permission_for_adjacent_limits(self) -> None:
        context = S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=14),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=10.0,
            capped_forecast=0.0,
            trend_forecast=1.0,
        )

        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )

        self.assertEqual(len(plan.limit_orders), 1)
        buy = plan.limit_orders[0]
        self.assertEqual(buy.side, S27V2OrderSide.BUY)
        self.assertLess(buy.limit_price, 100.0)
        self.assertTrue(plan.end_of_day_cancel_reset_required)
        downtrend_context = replace(context, trend_forecast=-1.0)
        downtrend_plan = build_s27_v2_order_plan(
            forecast_context=downtrend_context,
            current_position=0,
            desired_rounded_position=0,
        )
        self.assertEqual(len(downtrend_plan.limit_orders), 1)
        self.assertEqual(downtrend_plan.limit_orders[0].side, S27V2OrderSide.SELL)
        self.assertGreater(downtrend_plan.limit_orders[0].limit_price, 100.0)
        long_exit_plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=1,
            desired_rounded_position=0,
        )
        long_exit_sides_and_targets = {
            (order.side, order.target_position_after_fill) for order in long_exit_plan.limit_orders
        }
        self.assertIn((S27V2OrderSide.SELL, 0), long_exit_sides_and_targets)
        self.assertIn((S27V2OrderSide.BUY, 2), long_exit_sides_and_targets)
        with self.assertRaises(CarverBlocked):
            build_s27_v2_order_plan(
                forecast_context=context,
                current_position=1,
                desired_rounded_position=-1,
            )
        short_exit_plan = build_s27_v2_order_plan(
            forecast_context=downtrend_context,
            current_position=-1,
            desired_rounded_position=0,
        )
        short_exit_sides_and_targets = {
            (order.side, order.target_position_after_fill) for order in short_exit_plan.limit_orders
        }
        self.assertIn((S27V2OrderSide.BUY, 0), short_exit_sides_and_targets)
        self.assertIn((S27V2OrderSide.SELL, -2), short_exit_sides_and_targets)
        with self.assertRaises(CarverBlocked):
            build_s27_v2_order_plan(
                forecast_context=downtrend_context,
                current_position=-1,
                desired_rounded_position=1,
            )
        uptrend_cap_edge_context = replace(context, base_position_contracts=1.0)
        uptrend_cap_edge_plan = build_s27_v2_order_plan(
            forecast_context=uptrend_cap_edge_context,
            current_position=1,
            desired_rounded_position=0,
        )
        self.assertEqual(len(uptrend_cap_edge_plan.limit_orders), 1)
        self.assertEqual(uptrend_cap_edge_plan.limit_orders[0].side, S27V2OrderSide.SELL)
        self.assertEqual(uptrend_cap_edge_plan.limit_orders[0].target_position_after_fill, 0)
        downtrend_cap_edge_context = replace(downtrend_context, base_position_contracts=1.0)
        downtrend_cap_edge_plan = build_s27_v2_order_plan(
            forecast_context=downtrend_cap_edge_context,
            current_position=-1,
            desired_rounded_position=0,
        )
        self.assertEqual(len(downtrend_cap_edge_plan.limit_orders), 1)
        self.assertEqual(downtrend_cap_edge_plan.limit_orders[0].side, S27V2OrderSide.BUY)
        self.assertEqual(downtrend_cap_edge_plan.limit_orders[0].target_position_after_fill, 0)

    def test_cap_bound_missing_limit_side_uses_market_order_when_position_gap_needs_that_side(self) -> None:
        long_cap_context = S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=15),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=10.0,
            capped_forecast=20.0,
            trend_forecast=1.0,
        )

        plan = build_s27_v2_order_plan(
            forecast_context=long_cap_context,
            current_position=19,
            desired_rounded_position=20,
        )

        self.assertEqual(plan.limit_orders, ())
        self.assertEqual(len(plan.market_orders), 1)
        self.assertEqual(plan.market_orders[0].side, S27V2OrderSide.BUY)
        self.assertEqual(plan.market_orders[0].target_position_after_fill, 20)
        self.assertEqual(plan.market_orders[0].trigger, "CAP_BOUND_NO_BUY_LIMIT_SIDE")

        short_cap_context = S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=16),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=10.0,
            capped_forecast=-20.0,
            trend_forecast=-1.0,
        )
        short_plan = build_s27_v2_order_plan(
            forecast_context=short_cap_context,
            current_position=-19,
            desired_rounded_position=-20,
        )
        self.assertEqual(short_plan.limit_orders, ())
        self.assertEqual(len(short_plan.market_orders), 1)
        self.assertEqual(short_plan.market_orders[0].side, S27V2OrderSide.SELL)
        self.assertEqual(short_plan.market_orders[0].target_position_after_fill, -20)
        self.assertEqual(short_plan.market_orders[0].trigger, "CAP_BOUND_NO_SELL_LIMIT_SIDE")
        adjacent_target_cap_context = replace(
            long_cap_context,
            base_position_contracts=1.0,
            capped_forecast=15.1,
        )
        adjacent_target_cap_plan = build_s27_v2_order_plan(
            forecast_context=adjacent_target_cap_context,
            current_position=1,
            desired_rounded_position=2,
        )
        self.assertEqual(adjacent_target_cap_plan.limit_orders, ())
        self.assertEqual(len(adjacent_target_cap_plan.market_orders), 1)
        self.assertEqual(adjacent_target_cap_plan.market_orders[0].side, S27V2OrderSide.BUY)
        self.assertEqual(adjacent_target_cap_plan.market_orders[0].target_position_after_fill, 2)
        self.assertEqual(adjacent_target_cap_plan.market_orders[0].trigger, "ADJACENT_DESIRED_TARGET_UNPRICEABLE_AT_CAP")
        adjacent_short_target_cap_context = replace(
            short_cap_context,
            base_position_contracts=1.0,
            capped_forecast=-15.1,
        )
        adjacent_short_target_cap_plan = build_s27_v2_order_plan(
            forecast_context=adjacent_short_target_cap_context,
            current_position=-1,
            desired_rounded_position=-2,
        )
        self.assertEqual(adjacent_short_target_cap_plan.limit_orders, ())
        self.assertEqual(len(adjacent_short_target_cap_plan.market_orders), 1)
        self.assertEqual(adjacent_short_target_cap_plan.market_orders[0].side, S27V2OrderSide.SELL)
        self.assertEqual(adjacent_short_target_cap_plan.market_orders[0].target_position_after_fill, -2)
        self.assertEqual(adjacent_short_target_cap_plan.market_orders[0].trigger, "ADJACENT_DESIRED_TARGET_UNPRICEABLE_AT_CAP")

    def test_implied_price_inverts_position_formula(self) -> None:
        context = S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=14),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=10.0,
            capped_forecast=0.0,
            trend_forecast=1.0,
        )

        self.assertAlmostEqual(implied_price_for_target_position(context, target_position=1), 99.95)
        self.assertAlmostEqual(implied_price_for_target_position(context, target_position=0), 100.0)
        with self.assertRaises(CarverBlocked):
            implied_price_for_target_position(context, target_position=-1)
        self.assertAlmostEqual(
            implied_price_for_target_position(replace(context, trend_forecast=-1.0), target_position=-1),
            100.05,
        )
        self.assertAlmostEqual(
            implied_price_for_target_position(replace(context, trend_forecast=-1.0), target_position=0),
            100.0,
        )
        cap_edge_context = replace(context, base_position_contracts=1.0)
        with self.assertRaises(CarverBlocked):
            implied_price_for_target_position(cap_edge_context, target_position=2)
        with self.assertRaises(CarverBlocked):
            implied_price_for_target_position(replace(cap_edge_context, trend_forecast=-1.0), target_position=-2)

    def test_market_order_and_limit_fill_cost_boundaries(self) -> None:
        context = self.context_for_desired_position(3)
        market_plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=3,
        )
        next_hour = self.hourly_row(
            end=context.as_of + timedelta(hours=1),
            trading_date="2026-01-01",
            open_price=100.25,
            high=100.5,
            low=100.0,
            close=100.1,
        )

        market_fills = self.fill_order_plan_one_hour_lag(
            market_plan,
            next_hour,
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
        )

        self.assertEqual(len(market_fills), 1)
        self.assertEqual(market_fills[0].order_kind, S27V2OrderKind.MARKET)
        self.assertEqual(market_fills[0].fill_price, next_hour.close)
        self.assertEqual(market_fills[0].cost_treatment, S27V2FillCostTreatment.COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD)
        self.assertEqual(market_fills[0].commission_cost, 6.0)
        self.assertEqual(market_fills[0].spread_cost, 1.5)

        limit_plan = build_s27_v2_order_plan(
            forecast_context=self.flat_context(),
            current_position=0,
            desired_rounded_position=0,
        )
        limit_fills = self.fill_order_plan_one_hour_lag(
            limit_plan,
            self.hourly_row(
                end=context.as_of + timedelta(hours=1),
                trading_date="2026-01-01",
                open_price=100.0,
                high=100.0,
                low=99.90,
                close=99.90,
            ),
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
        )

        self.assertEqual(len(limit_fills), 1)
        self.assertTrue(all(fill.order_kind is S27V2OrderKind.LIMIT for fill in limit_fills))
        self.assertTrue(all(fill.cost_treatment is S27V2FillCostTreatment.COMMISSION_ONLY for fill in limit_fills))
        self.assertTrue(all(fill.spread_cost == 0.0 for fill in limit_fills))
        self.assertTrue(all(fill.commission_cost == 2.0 for fill in limit_fills))

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                market_plan,
                next_hour,
                commission_per_contract=0.0,
                normal_bid_ask_spread=0.5,
            )
        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                market_plan,
                next_hour,
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.0,
            )

    def test_cost_and_pnl_ledgers_are_separate_and_timestamp_aligned(self) -> None:
        context = self.context_for_desired_position(3)
        market_plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=3,
        )
        fill_as_of = context.as_of + timedelta(hours=1)
        fills = self.fill_order_plan_one_hour_lag(
            market_plan,
            self.hourly_row(
                end=fill_as_of,
                trading_date="2026-01-01",
                open_price=100.25,
                high=100.5,
                low=100.0,
                close=100.1,
            ),
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
        )

        costs = build_s27_v2_cost_ledger_rows(fills)
        pnl = build_s27_v2_pnl_ledger_row(
            start_as_of=context.as_of,
            end_as_of=fill_as_of,
            starting_position=2,
            start_price=100.0,
            end_price=101.0,
            contract_multiplier=1000.0,
            cost_rows=costs,
        )

        self.assertEqual(costs[0].commission_cost, 6.0)
        self.assertEqual(costs[0].spread_cost, 1.5)
        self.assertEqual(pnl.gross_pnl, 2000.0)
        self.assertEqual(pnl.total_cost, 7.5)
        self.assertEqual(pnl.net_pnl, 1992.5)
        with self.assertRaises(CarverBlocked):
            build_s27_v2_pnl_ledger_row(
                start_as_of=context.as_of,
                end_as_of=fill_as_of + timedelta(hours=1),
                starting_position=2,
                start_price=100.0,
                end_price=101.0,
                contract_multiplier=1000.0,
                cost_rows=costs,
            )

    def test_limit_fill_uses_next_completed_close_not_intrabar_high_low(self) -> None:
        context = S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=14),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=10.0,
            capped_forecast=0.0,
            trend_forecast=1.0,
        )
        limit_plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )

        fills = self.fill_order_plan_one_hour_lag(
            limit_plan,
            self.hourly_row(
                end=context.as_of + timedelta(hours=1),
                trading_date="2026-01-01",
                open_price=100.0,
                high=100.10,
                low=99.90,
                close=100.0,
            ),
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
        )

        self.assertEqual(fills, ())

    def test_working_order_state_carries_remaining_orders_on_normal_transition(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        state = open_s27_v2_working_order_state(plan, raw_symbol="ZNM6", session_id="2026-01-01")

        transition = transition_s27_v2_working_order_state_one_hour(
            state,
            self.hourly_row(
                end=context.as_of + timedelta(hours=1),
                trading_date="2026-01-01",
                open_price=100.0,
                high=100.0,
                low=99.90,
                close=99.90,
            ),
            transition_kind=S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
            next_session_id="2026-01-01",
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
        )

        self.assertEqual(len(transition.fills), 1)
        self.assertEqual(transition.next_position, 1)
        self.assertEqual(transition.remaining_limit_orders, ())
        self.assertEqual(transition.canceled_limit_orders, ())

    def test_working_order_state_cancels_remaining_limits_at_end_of_day(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        state = open_s27_v2_working_order_state(plan, raw_symbol="ZNM6", session_id="2026-01-01")

        transition = transition_s27_v2_working_order_state_one_hour(
            state,
            self.hourly_row(
                end=context.as_of + timedelta(hours=1),
                trading_date="2026-01-02",
                open_price=100.0,
                high=100.0,
                low=99.90,
                close=99.90,
            ),
            transition_kind=S27V2SessionTransitionKind.END_OF_DAY_CANCEL_RESET,
            next_session_id="2026-01-02",
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
        )

        self.assertEqual(transition.fills, ())
        self.assertEqual(transition.next_position, 0)
        self.assertEqual(transition.remaining_limit_orders, ())
        self.assertEqual(len(transition.canceled_limit_orders), 1)
        self.assertEqual(transition.canceled_limit_orders[0].side, S27V2OrderSide.BUY)

    def test_direct_transition_rejects_false_eod_and_eod_market_orders(self) -> None:
        context = self.flat_context()
        limit_plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        limit_state = open_s27_v2_working_order_state(limit_plan, raw_symbol="ZNM6", session_id="2026-01-01")
        same_day_row = self.hourly_row(
            end=context.as_of + timedelta(hours=1),
            trading_date="2026-01-01",
            open_price=100.0,
            high=100.0,
            low=99.90,
            close=99.90,
        )
        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                limit_state,
                same_day_row,
                transition_kind=S27V2SessionTransitionKind.END_OF_DAY_CANCEL_RESET,
                next_session_id="2026-01-02",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

        market_context = self.context_for_desired_position(3)
        market_plan = build_s27_v2_order_plan(
            forecast_context=market_context,
            current_position=0,
            desired_rounded_position=3,
        )
        market_state = open_s27_v2_working_order_state(market_plan, raw_symbol="ZNM6", session_id="2026-01-01")
        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                market_state,
                replace(same_day_row, completed_trading_date="2026-01-02"),
                transition_kind=S27V2SessionTransitionKind.END_OF_DAY_CANCEL_RESET,
                next_session_id="2026-01-02",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_direct_transition_rejects_false_overnight_label(self) -> None:
        context = self.context_for_desired_position(1)
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=1,
        )
        state = open_s27_v2_working_order_state(plan, raw_symbol="ZNM6", session_id="2026-01-01")
        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                state,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.5,
                    high=101.0,
                    low=100.25,
                    close=100.75,
                ),
                transition_kind=S27V2SessionTransitionKind.OVERNIGHT_GAP_MARKET_RESET,
                next_session_id="2026-01-02",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_working_order_state_overnight_gap_fails_closed_without_recomputed_target(self) -> None:
        context = self.context_for_desired_position(1)
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=1,
        )
        state = open_s27_v2_working_order_state(plan, raw_symbol="ZNM6", session_id="2026-01-01")

        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                state,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-02",
                    open_price=100.5,
                    high=101.0,
                    low=100.25,
                    close=100.75,
                ),
                transition_kind=S27V2SessionTransitionKind.OVERNIGHT_GAP_MARKET_RESET,
                next_session_id="2026-01-02",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_working_order_state_roll_boundary_fails_closed_without_explicit_assumption(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        state = open_s27_v2_working_order_state(plan, raw_symbol="ZNM6", session_id="2026-01-01")
        next_row = self.hourly_row(
            end=context.as_of + timedelta(hours=1),
            trading_date="2026-01-01",
            open_price=100.0,
            high=100.0,
            low=99.90,
            close=100.0,
        )

        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                state,
                replace(next_row, raw_symbol="ZNU6"),
                transition_kind=S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
                next_session_id="2026-01-01",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )
        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                state,
                replace(next_row, raw_symbol="ZNU6"),
                transition_kind=S27V2SessionTransitionKind.ROLL_BOUNDARY,
                next_session_id="2026-01-01",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )
        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                state,
                next_row,
                transition_kind=S27V2SessionTransitionKind.ROLL_BOUNDARY,
                next_session_id="2026-01-01",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                roll_handling_status=S27_V2_ROLL_STATE_RESET_ASSUMPTION_STATUS,
            )

        transition = transition_s27_v2_working_order_state_one_hour(
            state,
            replace(next_row, raw_symbol="ZNU6"),
            transition_kind=S27V2SessionTransitionKind.ROLL_BOUNDARY,
            next_session_id="2026-01-01",
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
            roll_handling_status=S27_V2_ROLL_STATE_RESET_ASSUMPTION_STATUS,
        )
        self.assertEqual(transition.fills, ())
        self.assertEqual(transition.remaining_limit_orders, ())
        self.assertEqual(transition.canceled_limit_orders, state.limit_orders)
        self.assertEqual(transition.next_position, 0)

    def test_one_hour_lag_is_required_for_fills(self) -> None:
        context = S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=14),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=10.0,
            capped_forecast=0.0,
            trend_forecast=1.0,
        )
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                plan,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=2),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.0,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_fill_rejects_internally_inconsistent_order_plans(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        forged_plan = replace(
            plan,
            limit_orders=(replace(plan.limit_orders[0], target_position_after_fill=-99),),
        )
        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                forged_plan,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=99.9,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )
        forged_gap_plan = replace(plan, desired_rounded_position=999)
        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                forged_gap_plan,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=99.9,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_order_plan_rejects_desired_position_not_implied_by_forecast_context(self) -> None:
        context = self.flat_context()

        with self.assertRaises(CarverBlocked):
            build_s27_v2_order_plan(
                forecast_context=context,
                current_position=0,
                desired_rounded_position=1,
            )

    def test_fill_rejects_forged_market_order_trigger(self) -> None:
        context = self.context_for_desired_position(3)
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=3,
        )
        forged_plan = replace(
            plan,
            market_orders=(replace(plan.market_orders[0], trigger="FORGED_MARKET_REASON"),),
        )

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                forged_plan,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.5,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_fill_rejects_allowed_market_trigger_without_matching_source_condition(self) -> None:
        context = S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=14),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=1.0,
            capped_forecast=15.1,
            trend_forecast=1.0,
        )
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=1,
            desired_rounded_position=2,
        )
        forged_plan = replace(
            plan,
            market_orders=(
                replace(
                    plan.market_orders[0],
                    trigger="DESIRED_POSITION_MORE_THAN_ONE_CONTRACT_FROM_CURRENT",
                ),
            ),
        )

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                forged_plan,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.5,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_fill_rejects_overnight_reset_market_trigger_until_recompute_exists(self) -> None:
        context = self.context_for_desired_position(3)
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=3,
        )
        forged_plan = replace(
            plan,
            market_orders=(replace(plan.market_orders[0], trigger="OVERNIGHT_GAP_MARKET_RESET"),),
        )

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                forged_plan,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.5,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_fill_rejects_market_order_plan_without_forecast_context_provenance(self) -> None:
        context = self.context_for_desired_position(3)
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=3,
        )

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                replace(plan, forecast_context=None),
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.5,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_forecast_context_rejects_scalar_and_trend_sign_conflicts(self) -> None:
        with self.assertRaises(CarverBlocked):
            replace(self.flat_context(), scalar=9.3).validate()
        with self.assertRaises(CarverBlocked):
            replace(self.flat_context(), capped_forecast=-1.0, trend_forecast=1.0).validate()
        with self.assertRaises(CarverBlocked):
            replace(self.flat_context(), capped_forecast=1.0, trend_forecast=-1.0).validate()

    def test_fill_rejects_limit_plan_without_forecast_context_provenance(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                replace(plan, forecast_context=None),
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=99.9,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_fill_rejects_limit_price_not_source_implied(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        forged_plan = replace(
            plan,
            limit_orders=(replace(plan.limit_orders[0], limit_price=99.0),),
        )

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                forged_plan,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=99.0,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_fill_rejects_limit_plan_omitting_source_required_adjacent_side(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=1,
            desired_rounded_position=0,
        )
        self.assertEqual(len(plan.limit_orders), 2)
        forged_plan = replace(plan, limit_orders=(plan.limit_orders[0],))

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                forged_plan,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=99.9,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_direct_fill_rejects_order_plan_without_raw_symbol_session_binding(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        next_row = self.hourly_row(
            end=context.as_of + timedelta(hours=1),
            trading_date="2026-01-01",
            open_price=100.0,
            high=101.0,
            low=99.0,
            close=99.9,
        )

        with self.assertRaises(CarverBlocked):
            fill_s27_v2_order_plan_one_hour_lag(
                plan,
                next_row,
                current_raw_symbol="ZNM6",
                current_session_id="2026-01-01",
                next_session_id="2026-01-01",
                transition_kind=S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_direct_fill_rejects_raw_symbol_or_session_change(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=0,
        )
        next_row = self.hourly_row(
            end=context.as_of + timedelta(hours=1),
            trading_date="2026-01-01",
            open_price=100.0,
            high=101.0,
            low=99.0,
            close=99.9,
        )

        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                plan,
                replace(next_row, raw_symbol="ZNU6"),
                current_raw_symbol="ZNM6",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )
        with self.assertRaises(CarverBlocked):
            self.fill_order_plan_one_hour_lag(
                plan,
                replace(next_row, completed_trading_date="2026-01-02"),
                current_session_id="2026-01-01",
                next_session_id="2026-01-02",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_normal_transition_rejects_state_with_overnight_market_trigger(self) -> None:
        context = self.context_for_desired_position(3)
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=3,
        )
        state = open_s27_v2_working_order_state(plan, raw_symbol="ZNM6", session_id="2026-01-01")
        forged_state = replace(
            state,
            market_orders=(replace(state.market_orders[0], trigger="OVERNIGHT_GAP_MARKET_RESET"),),
        )

        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                forged_state,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.5,
                ),
                transition_kind=S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
                next_session_id="2026-01-01",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_direct_roll_boundary_rejects_nonzero_position_without_roll_bridge(self) -> None:
        context = self.flat_context()
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=1,
            desired_rounded_position=0,
        )
        state = open_s27_v2_working_order_state(plan, raw_symbol="ZNM6", session_id="2026-01-01")

        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                state,
                replace(
                    self.hourly_row(
                        end=context.as_of + timedelta(hours=1),
                        trading_date="2026-01-01",
                        open_price=100.0,
                        high=101.0,
                        low=99.0,
                        close=100.5,
                    ),
                    raw_symbol="ZNU6",
                ),
                transition_kind=S27V2SessionTransitionKind.ROLL_BOUNDARY,
                next_session_id="2026-01-01",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                roll_handling_status=S27_V2_ROLL_STATE_RESET_ASSUMPTION_STATUS,
            )

    def test_stale_overnight_gap_market_helper_fails_closed(self) -> None:
        context = self.context_for_desired_position(1)
        plan = build_s27_v2_order_plan(
            forecast_context=context,
            current_position=0,
            desired_rounded_position=1,
        )
        state = open_s27_v2_working_order_state(plan, raw_symbol="ZNM6", session_id="2026-01-01")

        with self.assertRaises(CarverBlocked):
            _overnight_gap_market_fills(
                state,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-02",
                    open_price=100.5,
                    high=101.0,
                    low=100.25,
                    close=100.75,
                ),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_transition_rejects_forged_working_state_before_overnight_reset(self) -> None:
        context = self.flat_context()
        forged_state = S27V2WorkingOrderState(
            opened_as_of=context.as_of,
            session_id="2026-01-01",
            raw_symbol="ZNM6",
            current_position=0,
            desired_rounded_position=999,
            limit_orders=(),
            market_orders=(),
        )

        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                forged_state,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-02",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.5,
                ),
                transition_kind=S27V2SessionTransitionKind.OVERNIGHT_GAP_MARKET_RESET,
                next_session_id="2026-01-02",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_normal_transition_rejects_arbitrary_no_order_position_without_forecast_context(self) -> None:
        context = self.flat_context()
        forged_state = S27V2WorkingOrderState(
            opened_as_of=context.as_of,
            session_id="2026-01-01",
            raw_symbol="ZNM6",
            current_position=999,
            desired_rounded_position=999,
            limit_orders=(),
            market_orders=(),
            forecast_context=None,
        )

        with self.assertRaises(CarverBlocked):
            transition_s27_v2_working_order_state_one_hour(
                forged_state,
                self.hourly_row(
                    end=context.as_of + timedelta(hours=1),
                    trading_date="2026-01-01",
                    open_price=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.5,
                ),
                transition_kind=S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
                next_session_id="2026-01-01",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
            )

    def test_cost_and_pnl_reject_external_provenance_free_rows(self) -> None:
        external_fill = S27V2FillRow(
            decision_as_of=self.day0 + timedelta(hours=14),
            fill_as_of=self.day0 + timedelta(hours=15),
            side=S27V2OrderSide.BUY,
            quantity=1,
            fill_price=100.0,
            order_kind=S27V2OrderKind.LIMIT,
            cost_treatment=S27V2FillCostTreatment.COMMISSION_ONLY,
            commission_cost=2.0,
            spread_cost=0.0,
            total_cost=2.0,
        )
        with self.assertRaises(CarverBlocked):
            build_s27_v2_cost_ledger_rows((external_fill,))

        external_cost = replace(
            build_s27_v2_cost_ledger_rows(
                (
                    replace(
                        external_fill,
                        fill_source_status="S27_V2_FILL_FROM_VALIDATED_ORDER_PLAN_ONE_HOUR_LAG",
                    ),
                )
            )[0],
            cost_source_status="S27_V2_EXTERNAL_COST_UNPROVEN",
        )
        with self.assertRaises(CarverBlocked):
            build_s27_v2_pnl_ledger_row(
                start_as_of=self.day0 + timedelta(hours=14),
                end_as_of=self.day0 + timedelta(hours=15),
                starting_position=1,
                start_price=100.0,
                end_price=101.0,
                contract_multiplier=1000.0,
                cost_rows=(external_cost,),
            )

    def test_replay_step_bundle_emits_row_level_ledgers_and_hashes(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 100.2, 100.4, 100.6),
            current_contract=(100.0, 100.0, 100.0, 100.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        hourly = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=100.30,
            high=100.35,
            low=100.28,
            close=100.30,
        )
        next_hour = self.hourly_row(
            end=hourly.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-05",
            open_price=100.23,
            high=100.25,
            low=100.20,
            close=100.20,
        )

        bundle = build_s27_v2_replay_step_ledger_bundle(
            hourly_row=hourly,
            next_hourly_row=next_hour,
            daily_input=rows[-1],
            daily_runtime=runtime[-1],
            current_position=0,
            base_position_contracts=10.0,
            rounding_policy=RoundingPolicy.NEAREST,
            transition_kind=S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
            next_session_id="2026-01-05",
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
            contract_multiplier=1000.0,
            daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
        )

        self.assertEqual(len(bundle.source_input_manifest_rows), 1)
        self.assertEqual(bundle.source_input_manifest_rows[0].hourly_close, hourly.close)
        self.assertEqual(bundle.source_input_manifest_rows[0].fill_hourly_close, next_hour.close)
        self.assertEqual(bundle.source_input_manifest_rows[0].fill_raw_symbol, next_hour.raw_symbol)
        self.assertEqual(len(bundle.level_compatibility_ledger_rows), 1)
        self.assertEqual(bundle.level_compatibility_ledger_rows[0].daily_current_traded_contract_close, rows[-1].current_traded_contract_close)
        self.assertEqual(bundle.level_compatibility_ledger_rows[0].hourly_current_price, hourly.close)
        self.assertEqual(len(bundle.forecast_replay_rows), 1)
        self.assertEqual(len(bundle.desired_position_rows), 1)
        self.assertEqual(len(bundle.limit_order_rows), 1)
        self.assertEqual(bundle.market_order_rows, ())
        self.assertEqual(len(bundle.fill_rows), 1)
        self.assertEqual(bundle.fill_rows[0].order_kind, S27V2OrderKind.LIMIT)
        self.assertEqual(len(bundle.commission_ledger_rows), 1)
        self.assertEqual(bundle.spread_cost_ledger_rows, ())
        self.assertEqual(bundle.pnl_ledger_rows[0].total_cost, 2.0)
        self.assertEqual(bundle.pnl_ledger_rows[0].net_pnl, -2.0)
        self.assertEqual(bundle.final_position, 1)
        self.assertTrue(bundle.provenance_hash_ledger_rows)
        self.assertTrue(all(len(row.sha256) == 64 for row in bundle.provenance_hash_ledger_rows))
        families = {row.artifact_family for row in bundle.provenance_hash_ledger_rows}
        self.assertEqual(
            families,
            {
                "SOURCE_INPUT_MANIFEST",
                "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER",
                "RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM",
                "FORECAST_REPLAY_LEDGER",
                "DESIRED_POSITION_LEDGER",
                "WORKING_ORDER_TRANSITION_LEDGER",
                "LIMIT_ORDER_LEDGER",
                "MARKET_ORDER_LEDGER",
                "REMAINING_LIMIT_ORDER_LEDGER",
                "CANCELED_LIMIT_ORDER_LEDGER",
                "FILL_LEDGER",
                "COMMISSION_LEDGER",
                "SPREAD_COST_LEDGER",
                "PNL_LEDGER",
                "VALIDATION_LEDGER",
            },
        )
        self.assertIn(
            "FILL_HOURLY_ROW_READY",
            {row.validation_name for row in bundle.validation_ledger_rows},
        )

    def test_replay_step_bundle_emits_market_and_spread_ledgers(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        hourly = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )
        next_hour = self.hourly_row(
            end=hourly.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-05",
            open_price=95.25,
            high=95.5,
            low=95.0,
            close=95.4,
        )

        bundle = build_s27_v2_replay_step_ledger_bundle(
            hourly_row=hourly,
            next_hourly_row=next_hour,
            daily_input=rows[-1],
            daily_runtime=runtime[-1],
            current_position=0,
            base_position_contracts=3.0,
            rounding_policy=RoundingPolicy.NEAREST,
            transition_kind=S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
            next_session_id="2026-01-05",
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
            contract_multiplier=1000.0,
            daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
        )

        self.assertEqual(bundle.limit_order_rows, ())
        self.assertEqual(len(bundle.market_order_rows), 1)
        self.assertEqual(len(bundle.fill_rows), 1)
        self.assertEqual(bundle.fill_rows[0].order_kind, S27V2OrderKind.MARKET)
        self.assertEqual(len(bundle.commission_ledger_rows), 1)
        self.assertEqual(len(bundle.spread_cost_ledger_rows), 1)
        self.assertGreater(bundle.spread_cost_ledger_rows[0].amount, 0.0)

    def test_replay_step_bundle_fails_closed_on_degraded_local_rows(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 100.2, 100.4, 100.6),
            current_contract=(100.0, 100.0, 100.0, 100.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        runtime = build_s27_v2_daily_runtime_rows(rows)
        hourly = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=100.30,
            high=100.35,
            low=100.28,
            close=100.30,
        )
        degraded_next_hour = S27V2HourlyRuntimeInput(
            completed_bar_end_utc=hourly.completed_bar_end_utc + timedelta(hours=1),
            completed_trading_date="2026-01-05",
            raw_symbol="ZNM6",
            open=100.23,
            high=100.25,
            low=100.20,
            close=100.24,
            provider_condition_status="DEGRADED",
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_replay_step_ledger_bundle(
                hourly_row=hourly,
                next_hourly_row=degraded_next_hour,
                daily_input=rows[-1],
                daily_runtime=runtime[-1],
                current_position=0,
                base_position_contracts=10.0,
                rounding_policy=RoundingPolicy.NEAREST,
                transition_kind=S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
                next_session_id="2026-01-05",
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                contract_multiplier=1000.0,
                daily_runtime_selection_status=S27_V2_LATEST_STRICT_PRIOR_DAILY_RUNTIME_SELECTION_STATUS,
            )

    def test_multi_row_replay_aggregates_consecutive_market_steps(self) -> None:
        rows = self.daily_rows(
            continuous=(106.0, 104.0, 102.0, 100.0),
            current_contract=(100.0, 100.0, 100.0, 100.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=104.0,
            high=104.5,
            low=103.5,
            close=104.0,
        )
        hour1 = self.hourly_row(
            end=hour0.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-05",
            open_price=105.0,
            high=105.5,
            low=104.5,
            close=105.0,
        )
        hour2 = self.hourly_row(
            end=hour1.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-05",
            open_price=105.25,
            high=105.75,
            low=104.75,
            close=105.25,
        )

        replay = build_s27_v2_multi_row_replay_ledger_bundle(
            daily_rows=rows,
            hourly_rows=(hour0, hour1, hour2),
            initial_position=0,
            base_position_contracts=3.0,
            rounding_policy=RoundingPolicy.NEAREST,
            transition_kinds=(
                S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
                S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
            ),
            session_ids=("2026-01-05", "2026-01-05", "2026-01-05"),
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
            contract_multiplier=1000.0,
        )

        self.assertEqual(replay.replay_step_count, 2)
        self.assertEqual(len(replay.step_bundles), 2)
        self.assertEqual(len(replay.source_input_manifest_rows), 2)
        self.assertEqual(len(replay.forecast_replay_rows), 2)
        self.assertEqual(len(replay.market_order_rows), 2)
        self.assertEqual(len(replay.spread_cost_ledger_rows), 2)
        self.assertEqual(len(replay.pnl_ledger_rows), 2)
        self.assertEqual(replay.initial_position, 0)
        self.assertEqual(replay.final_position, replay.step_bundles[-1].final_position)
        self.assertTrue(replay.provenance_hash_ledger_rows)

    def test_multi_row_replay_fails_closed_on_unresolved_carried_limits(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 100.2, 100.4, 100.6),
            current_contract=(100.0, 100.0, 100.0, 100.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=100.30,
            high=100.35,
            low=100.28,
            close=100.30,
        )
        hour1 = self.hourly_row(
            end=hour0.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-05",
            open_price=100.30,
            high=100.35,
            low=100.28,
            close=100.30,
        )
        hour2 = self.hourly_row(
            end=hour1.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-05",
            open_price=100.30,
            high=100.35,
            low=100.28,
            close=100.30,
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_multi_row_replay_ledger_bundle(
                daily_rows=rows,
                hourly_rows=(hour0, hour1, hour2),
                initial_position=0,
                base_position_contracts=10.0,
                rounding_policy=RoundingPolicy.NEAREST,
                transition_kinds=(
                    S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
                    S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
                ),
                session_ids=("2026-01-05", "2026-01-05", "2026-01-05"),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                contract_multiplier=1000.0,
            )

    def test_multi_row_replay_fails_closed_on_symbol_roll_without_explicit_status(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )
        hour1 = replace(
            self.hourly_row(
                end=hour0.completed_bar_end_utc + timedelta(hours=1),
                trading_date="2026-01-05",
                open_price=95.25,
                high=95.5,
                low=95.0,
                close=95.4,
            ),
            raw_symbol="ZNU6",
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_multi_row_replay_ledger_bundle(
                daily_rows=rows,
                hourly_rows=(hour0, hour1),
                initial_position=0,
                base_position_contracts=3.0,
                rounding_policy=RoundingPolicy.NEAREST,
                transition_kinds=(S27V2SessionTransitionKind.NORMAL_ONE_HOUR,),
                session_ids=("2026-01-05", "2026-01-05"),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                contract_multiplier=1000.0,
            )

    def test_multi_row_replay_fails_closed_on_false_eod_or_overnight_labels(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 100.2, 100.4, 100.6),
            current_contract=(100.0, 100.0, 100.0, 100.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=100.30,
            high=100.35,
            low=100.28,
            close=100.30,
        )
        hour1 = self.hourly_row(
            end=hour0.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-05",
            open_price=100.30,
            high=100.35,
            low=100.28,
            close=100.30,
        )

        for transition_kind in (
            S27V2SessionTransitionKind.END_OF_DAY_CANCEL_RESET,
            S27V2SessionTransitionKind.OVERNIGHT_GAP_MARKET_RESET,
        ):
            with self.assertRaises(CarverBlocked):
                build_s27_v2_multi_row_replay_ledger_bundle(
                    daily_rows=rows,
                    hourly_rows=(hour0, hour1),
                    initial_position=0,
                    base_position_contracts=10.0,
                    rounding_policy=RoundingPolicy.NEAREST,
                    transition_kinds=(transition_kind,),
                    session_ids=("2026-01-05", "2026-01-05"),
                    commission_per_contract=2.0,
                    normal_bid_ask_spread=0.5,
                    contract_multiplier=1000.0,
                )

    def test_multi_row_overnight_market_reset_fails_closed_without_recomputed_target(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=23),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )
        hour1 = self.hourly_row(
            end=hour0.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-06",
            open_price=95.25,
            high=95.5,
            low=95.0,
            close=95.4,
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_multi_row_replay_ledger_bundle(
                daily_rows=rows,
                hourly_rows=(hour0, hour1),
                initial_position=0,
                base_position_contracts=3.0,
                rounding_policy=RoundingPolicy.NEAREST,
                transition_kinds=(S27V2SessionTransitionKind.OVERNIGHT_GAP_MARKET_RESET,),
                session_ids=("2026-01-05", "2026-01-06"),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                contract_multiplier=1000.0,
            )

    def test_multi_row_roll_boundary_suppresses_unexecuted_plan_market_orders(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )
        hour1 = replace(
            self.hourly_row(
                end=hour0.completed_bar_end_utc + timedelta(hours=1),
                trading_date="2026-01-05",
                open_price=95.25,
                high=95.5,
                low=95.0,
                close=95.4,
            ),
            raw_symbol="ZNU6",
        )

        replay = build_s27_v2_multi_row_replay_ledger_bundle(
            daily_rows=rows,
            hourly_rows=(hour0, hour1),
            initial_position=0,
            base_position_contracts=3.0,
            rounding_policy=RoundingPolicy.NEAREST,
            transition_kinds=(S27V2SessionTransitionKind.ROLL_BOUNDARY,),
            session_ids=("2026-01-05", "2026-01-05"),
            commission_per_contract=2.0,
            normal_bid_ask_spread=0.5,
            contract_multiplier=1000.0,
            roll_handling_statuses=(S27_V2_ROLL_STATE_RESET_ASSUMPTION_STATUS,),
        )

        self.assertEqual(replay.market_order_rows, ())
        self.assertEqual(replay.fill_rows, ())
        self.assertEqual(replay.final_position, 0)

    def test_multi_row_roll_boundary_fails_closed_for_nonzero_position_without_roll_bridge(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )
        hour1 = replace(
            self.hourly_row(
                end=hour0.completed_bar_end_utc + timedelta(hours=1),
                trading_date="2026-01-05",
                open_price=95.25,
                high=95.5,
                low=95.0,
                close=95.4,
            ),
            raw_symbol="ZNU6",
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_multi_row_replay_ledger_bundle(
                daily_rows=rows,
                hourly_rows=(hour0, hour1),
                initial_position=1,
                base_position_contracts=3.0,
                rounding_policy=RoundingPolicy.NEAREST,
                transition_kinds=(S27V2SessionTransitionKind.ROLL_BOUNDARY,),
                session_ids=("2026-01-05", "2026-01-05"),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                contract_multiplier=1000.0,
                roll_handling_statuses=(S27_V2_ROLL_STATE_RESET_ASSUMPTION_STATUS,),
            )

    def test_multi_row_replay_rejects_explicit_empty_roll_statuses(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0, 104.0, 106.0),
            current_contract=(99.0, 99.0, 99.0, 99.0),
            sigma=(0.16, 0.16, 0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=4, hours=14),
            trading_date="2026-01-05",
            open_price=95.0,
            high=96.0,
            low=94.0,
            close=95.0,
        )
        hour1 = self.hourly_row(
            end=hour0.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-05",
            open_price=95.25,
            high=95.5,
            low=95.0,
            close=95.4,
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_multi_row_replay_ledger_bundle(
                daily_rows=rows,
                hourly_rows=(hour0, hour1),
                initial_position=0,
                base_position_contracts=3.0,
                rounding_policy=RoundingPolicy.NEAREST,
                transition_kinds=(S27V2SessionTransitionKind.NORMAL_ONE_HOUR,),
                session_ids=("2026-01-05", "2026-01-05"),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                contract_multiplier=1000.0,
                roll_handling_statuses=(),
            )

    def test_multi_row_replay_requires_strict_prior_daily_runtime_for_each_decision(self) -> None:
        rows = self.daily_rows(
            continuous=(100.0, 102.0),
            current_contract=(100.0, 100.0),
            sigma=(0.16, 0.16),
        )
        hour0 = self.hourly_row(
            end=self.day0 + timedelta(days=1, hours=14),
            trading_date="2026-01-02",
            open_price=99.0,
            high=100.0,
            low=98.0,
            close=99.0,
        )
        hour1 = self.hourly_row(
            end=hour0.completed_bar_end_utc + timedelta(hours=1),
            trading_date="2026-01-02",
            open_price=99.0,
            high=100.0,
            low=98.0,
            close=99.0,
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_multi_row_replay_ledger_bundle(
                daily_rows=(rows[-1],),
                hourly_rows=(hour0, hour1),
                initial_position=0,
                base_position_contracts=3.0,
                rounding_policy=RoundingPolicy.NEAREST,
                transition_kinds=(S27V2SessionTransitionKind.NORMAL_ONE_HOUR,),
                session_ids=("2026-01-02", "2026-01-02"),
                commission_per_contract=2.0,
                normal_bid_ask_spread=0.5,
                contract_multiplier=1000.0,
            )

    def test_cost_ledger_rejects_externally_constructed_zero_cost_market_fill(self) -> None:
        fill = S27V2FillRow(
            decision_as_of=self.day0 + timedelta(hours=14),
            fill_as_of=self.day0 + timedelta(hours=15),
            side=S27V2OrderSide.BUY,
            quantity=1,
            fill_price=100.0,
            order_kind=S27V2OrderKind.MARKET,
            cost_treatment=S27V2FillCostTreatment.COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD,
            commission_cost=0.0,
            spread_cost=0.5,
            total_cost=0.5,
        )

        with self.assertRaises(CarverBlocked):
            build_s27_v2_cost_ledger_rows((fill,))

    def test_runtime_inputs_require_iso_trading_dates(self) -> None:
        with self.assertRaises(CarverBlocked):
            S27V2DailyRuntimeInput(
                completed_trading_date="01/02/2026",
                completed_bar_timestamp=self.day0,
                continuous_close=100.0,
                current_traded_contract_close=100.0,
                annual_percentage_sigma=0.16,
            ).validate()
        with self.assertRaises(CarverBlocked):
            S27V2HourlyRuntimeInput(
                completed_bar_end_utc=self.day0 + timedelta(hours=14),
                completed_trading_date="2026-1-2",
                raw_symbol="ZNM6",
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.0,
            ).validate()

    def daily_rows(
        self,
        *,
        continuous: tuple[float, ...],
        current_contract: tuple[float, ...],
        sigma: tuple[float, ...],
    ) -> tuple[S27V2DailyRuntimeInput, ...]:
        self.assertEqual(len(continuous), len(current_contract))
        self.assertEqual(len(continuous), len(sigma))
        return tuple(
            S27V2DailyRuntimeInput(
                completed_trading_date=(self.day0 + timedelta(days=index)).date().isoformat(),
                completed_bar_timestamp=self.day0 + timedelta(days=index),
                continuous_close=continuous[index],
                current_traded_contract_close=current_contract[index],
                annual_percentage_sigma=sigma[index],
                source_status=S27_V2_DAILY_ROW_READY_STATUS,
                level_compatibility_status=S27_V2_LEVEL_COMPATIBILITY_STATUS,
                annual_percentage_sigma_source_status=S27_V2_ANNUAL_PERCENTAGE_SIGMA_SOURCE_STATUS,
            )
            for index in range(len(continuous))
        )

    def hourly_row(
        self,
        *,
        end: datetime,
        trading_date: str,
        open_price: float,
        high: float,
        low: float,
        close: float,
    ) -> S27V2HourlyRuntimeInput:
        return S27V2HourlyRuntimeInput(
            completed_bar_end_utc=end,
            completed_trading_date=trading_date,
            raw_symbol="ZNM6",
            open=open_price,
            high=high,
            low=low,
            close=close,
            provider_condition_status=S27_V2_HOURLY_ROW_READY_STATUS,
        )

    def fill_order_plan_one_hour_lag(
        self,
        order_plan,
        next_hourly_row: S27V2HourlyRuntimeInput,
        *,
        commission_per_contract: float,
        normal_bid_ask_spread: float,
        current_raw_symbol: str | None = None,
        current_session_id: str | None = None,
        next_session_id: str | None = None,
        transition_kind: S27V2SessionTransitionKind = S27V2SessionTransitionKind.NORMAL_ONE_HOUR,
    ) -> tuple[S27V2FillRow, ...]:
        session_id = current_session_id or next_hourly_row.completed_trading_date
        raw_symbol = current_raw_symbol or next_hourly_row.raw_symbol
        bound_plan = replace(
            order_plan,
            raw_symbol=raw_symbol,
            session_id=session_id,
        )
        return fill_s27_v2_order_plan_one_hour_lag(
            bound_plan,
            next_hourly_row,
            current_raw_symbol=raw_symbol,
            current_session_id=session_id,
            next_session_id=next_session_id or session_id,
            transition_kind=transition_kind,
            commission_per_contract=commission_per_contract,
            normal_bid_ask_spread=normal_bid_ask_spread,
        )

    def flat_context(self) -> S27V2ForecastContext:
        return S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=14),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=10.0,
            capped_forecast=0.0,
            trend_forecast=1.0,
        )

    def context_for_desired_position(self, desired_position: int) -> S27V2ForecastContext:
        if abs(desired_position) > FORECAST_CAP:
            raise ValueError("synthetic desired position helper is capped at +/-20")
        trend = 1.0 if desired_position >= 0 else -1.0
        return S27V2ForecastContext(
            as_of=self.day0 + timedelta(hours=14),
            equilibrium_ewma5=100.0,
            sigma_price=1.0,
            vol_multiplier_m=1.0,
            scalar=20.0,
            base_position_contracts=10.0,
            capped_forecast=float(desired_position),
            trend_forecast=trend,
        )


if __name__ == "__main__":
    unittest.main()

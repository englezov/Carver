from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked, CompletedBar, ContractSpec, LaneClass, SourceRuleStatus  # noqa: E402
from carver.spine.m1 import RoundingPolicy, TimedValue  # noqa: E402
from carver.spine.m2 import FORECAST_CAP  # noqa: E402
from carver.spine.p05 import (  # noqa: E402
    P05_BOOK_REFERENCE_TARGET_RISK,
    P05_COMPLETE_TREND_PORTFOLIO_ID,
    P05_FORECAST_DIVISOR,
    P05_JUMBO_REFERENCE_IDM,
    P05_STRATEGY_NINE_COST_LIMIT_SR,
    P05CompleteTrendPortfolioRequest,
    P05CompleteTrendPortfolioSourceLocks,
    P05EligibleEWMACSet,
    P05SyntheticMarketInput,
    P05SyntheticMember,
    P05SyntheticS09TrendForecastInput,
    p05_complete_trend_portfolio_conformance,
    p05_handcrafted_instrument_weights,
)


class P05CompleteTrendPortfolioSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.as_of = datetime(2026, 5, 29, tzinfo=timezone.utc)
        self.completed_bar = CompletedBar(self.as_of)

    def test_p05_emits_complete_trend_desired_position_inputs_only(self) -> None:
        result = p05_complete_trend_portfolio_conformance(self.request())

        self.assertEqual(result.portfolio_id, P05_COMPLETE_TREND_PORTFOLIO_ID)
        self.assertEqual(result.member_ids, ("SYN_BOND_A", "SYN_BOND_B", "SYN_EQUITY_A", "SYN_METAL_A"))
        self.assertTrue(result.is_synthetic_conformance)
        self.assertFalse(result.production_source_locked)
        self.assertFalse(result.interpretable_performance)
        self.assertEqual(result.performance_metrics, ())
        self.assertEqual(result.return_outputs, ())
        self.assertEqual(result.pnl_outputs, ())
        self.assertEqual(result.trading_orders, ())

        by_member = {member.member_id: member for member in result.member_results}
        self.assertAlmostEqual(by_member["SYN_BOND_A"].instrument_weight, 1.0 / 6.0)
        self.assertAlmostEqual(by_member["SYN_BOND_B"].instrument_weight, 1.0 / 6.0)
        self.assertAlmostEqual(by_member["SYN_EQUITY_A"].instrument_weight, 1.0 / 3.0)
        self.assertAlmostEqual(by_member["SYN_METAL_A"].instrument_weight, 1.0 / 3.0)

        self.assertAlmostEqual(by_member["SYN_BOND_A"].final_capped_p05_forecast, 8.24)
        self.assertAlmostEqual(by_member["SYN_BOND_B"].final_capped_p05_forecast, -4.0)
        self.assertAlmostEqual(by_member["SYN_EQUITY_A"].final_capped_p05_forecast, FORECAST_CAP)
        self.assertAlmostEqual(by_member["SYN_METAL_A"].final_capped_p05_forecast, 2.16)
        for member in result.member_results:
            self.assertAlmostEqual(member.forecast_multiplier, member.final_capped_p05_forecast / P05_FORECAST_DIVISOR)
            self.assertAlmostEqual(
                member.desired_unrounded_contracts,
                member.base_sizing.unrounded_contracts * member.forecast_multiplier,
            )

    def test_handcrafted_weights_follow_asset_group_member_taxonomy(self) -> None:
        weights = p05_handcrafted_instrument_weights(self.members())

        self.assertAlmostEqual(sum(weights.values()), 1.0)
        self.assertEqual(tuple(weights), ("SYN_BOND_A", "SYN_BOND_B", "SYN_EQUITY_A", "SYN_METAL_A"))
        self.assertAlmostEqual(weights["SYN_BOND_A"], 1.0 / 6.0)
        self.assertAlmostEqual(weights["SYN_BOND_B"], 1.0 / 6.0)
        self.assertAlmostEqual(weights["SYN_EQUITY_A"], 1.0 / 3.0)
        self.assertAlmostEqual(weights["SYN_METAL_A"], 1.0 / 3.0)

    def test_p05_uses_strategy_nine_equal_weights_fdm_and_caps(self) -> None:
        result = p05_complete_trend_portfolio_conformance(self.request())
        equity = {member.member_id: member for member in result.member_results}["SYN_EQUITY_A"]

        self.assertEqual(equity.eligible_spans, (8, 16, 32, 64))
        self.assertAlmostEqual(equity.s09_forecast_block.rule_results[0].weight, 0.25)
        self.assertAlmostEqual(equity.s09_forecast_block.fdm, 1.13)
        self.assertAlmostEqual(equity.s09_forecast_block.pre_fdm_forecast, 20.0)
        self.assertGreater(equity.s09_forecast_block.post_fdm_forecast, FORECAST_CAP)
        self.assertEqual(equity.final_capped_p05_forecast, FORECAST_CAP)

    def test_p05_fails_closed_on_unresolved_locks_and_non_source_native_lane(self) -> None:
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(
                self.request(source_locks=replace(self.locks(), output_boundary_status=SourceRuleStatus.UNRESOLVED))
            )
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(
                self.request(source_locks=replace(self.locks(), cost_eligibility_status=SourceRuleStatus.UNRESOLVED))
            )
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(lane_class=LaneClass.CFD_ADAPTER))

    def test_p05_fails_closed_on_synthetic_input_and_timestamp_drift(self) -> None:
        forecasts = list(self.forecast_inputs())
        forecasts[0] = replace(forecasts[0], label="production_s09_forecast")
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(forecast_inputs=tuple(forecasts)))

        forecasts = list(self.forecast_inputs())
        forecasts[0] = replace(forecasts[0], capped_forecast=TimedValue(6.0, self.as_of - timedelta(days=1)))
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(forecast_inputs=tuple(forecasts)))

        forecasts = list(self.forecast_inputs())
        forecasts[0] = replace(forecasts[0], capped_forecast=TimedValue(25.0, self.as_of))
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(forecast_inputs=tuple(forecasts)))

    def test_p05_fails_closed_on_member_drop_or_speed_drift(self) -> None:
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(market_inputs=self.market_inputs()[:-1]))

        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(eligible_speed_sets=self.eligible_speed_sets()[:-1]))

        bad_eligible = list(self.eligible_speed_sets())
        bad_eligible[0] = replace(bad_eligible[0], spans=(2, 64))
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(eligible_speed_sets=tuple(bad_eligible)))

        forecasts = tuple(item for item in self.forecast_inputs() if not (item.member_id == "SYN_BOND_A" and item.span == 64))
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(forecast_inputs=forecasts))

    def test_p05_fails_closed_on_member_identity_taxonomy_and_prevalidation(self) -> None:
        members = list(self.members())
        members[0] = replace(members[0], member_id="SYN_BAD_CODE")
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(members=tuple(members)))

        members = list(self.members())
        members[1] = replace(members[1], taxonomy_status=SourceRuleStatus.UNRESOLVED)
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(members=tuple(members)))

        markets = list(self.market_inputs())
        markets[0] = replace(markets[0], price_risk_prevalidated=False)
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(market_inputs=tuple(markets)))

        markets = list(self.market_inputs())
        markets[2] = replace(markets[2], cost_eligibility_prevalidated=False)
        with self.assertRaises(CarverBlocked):
            p05_complete_trend_portfolio_conformance(self.request(market_inputs=tuple(markets)))

    def test_p05_conformance_doc_records_boundary(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_2026-05-29.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST", text)
        self.assertIn("Strategy Nine", text)
        self.assertIn("Appendix C", text)
        self.assertIn("desired position inputs only", text)
        self.assertIn("No real data", text)
        self.assertIn("no P06/P07", text)

    def request(
        self,
        *,
        members: tuple[P05SyntheticMember, ...] | None = None,
        market_inputs: tuple[P05SyntheticMarketInput, ...] | None = None,
        forecast_inputs: tuple[P05SyntheticS09TrendForecastInput, ...] | None = None,
        eligible_speed_sets: tuple[P05EligibleEWMACSet, ...] | None = None,
        source_locks: P05CompleteTrendPortfolioSourceLocks | None = None,
        lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
    ) -> P05CompleteTrendPortfolioRequest:
        return P05CompleteTrendPortfolioRequest(
            completed_bar=self.completed_bar,
            members=members or self.members(),
            market_inputs=market_inputs or self.market_inputs(),
            forecast_inputs=forecast_inputs or self.forecast_inputs(),
            eligible_speed_sets=eligible_speed_sets or self.eligible_speed_sets(),
            capital=TimedValue(50_000_000.0, self.as_of),
            target_risk=TimedValue(P05_BOOK_REFERENCE_TARGET_RISK, self.as_of),
            idm=TimedValue(P05_JUMBO_REFERENCE_IDM, self.as_of),
            source_locks=source_locks or self.locks(),
            rounding_policy=RoundingPolicy.TRUNCATE,
            lane_class=lane_class,
        )

    def members(self) -> tuple[P05SyntheticMember, ...]:
        return (
            self.member("SYN_BOND_A", "Rates", "US bonds", 1000.0),
            self.member("SYN_BOND_B", "Rates", "US bonds", 1000.0),
            self.member("SYN_EQUITY_A", "Equity", "US equity", 5.0),
            self.member("SYN_METAL_A", "Metals", "Precious", 10.0),
        )

    def member(self, code: str, asset_class: str, group: str, multiplier: float) -> P05SyntheticMember:
        return P05SyntheticMember(
            member_id=code,
            contract=ContractSpec(code, f"{code} synthetic future", "SYNEX", "USD", multiplier),
            asset_class=asset_class,
            group=group,
            identity_status=SourceRuleStatus.LOCKED,
            taxonomy_status=SourceRuleStatus.LOCKED,
        )

    def market_inputs(self) -> tuple[P05SyntheticMarketInput, ...]:
        return (
            self.market("SYN_BOND_A", 112.0, 0.07, 0.45, 0.004),
            self.market("SYN_BOND_B", 98.0, 0.08, 0.49, 0.005),
            self.market("SYN_EQUITY_A", 5200.0, 0.22, 71.5, 0.002),
            self.market("SYN_METAL_A", 2400.0, 0.18, 27.0, 0.006),
        )

    def market(self, member_id: str, price: float, risk: float, daily_price_risk: float, cost: float) -> P05SyntheticMarketInput:
        return P05SyntheticMarketInput(
            member_id=member_id,
            current_held_price=TimedValue(price, self.as_of),
            annual_risk_estimate=TimedValue(risk, self.as_of),
            daily_price_risk=TimedValue(daily_price_risk, self.as_of),
            fx_rate=TimedValue(1.0, self.as_of),
            risk_adjusted_cost_per_trade=TimedValue(cost, self.as_of),
        )

    def eligible_speed_sets(self) -> tuple[P05EligibleEWMACSet, ...]:
        return (
            P05EligibleEWMACSet("SYN_BOND_A", (32, 64), SourceRuleStatus.LOCKED),
            P05EligibleEWMACSet("SYN_BOND_B", (64,), SourceRuleStatus.LOCKED),
            P05EligibleEWMACSet("SYN_EQUITY_A", (8, 16, 32, 64), SourceRuleStatus.LOCKED),
            P05EligibleEWMACSet("SYN_METAL_A", (16, 32, 64), SourceRuleStatus.LOCKED),
        )

    def forecast_inputs(self) -> tuple[P05SyntheticS09TrendForecastInput, ...]:
        values = {
            "SYN_BOND_A": {32: 6.0, 64: 10.0},
            "SYN_BOND_B": {64: -4.0},
            "SYN_EQUITY_A": {8: 20.0, 16: 20.0, 32: 20.0, 64: 20.0},
            "SYN_METAL_A": {16: 1.0, 32: 2.0, 64: 3.0},
        }
        return tuple(
            P05SyntheticS09TrendForecastInput(
                member_id=member_id,
                span=span,
                capped_forecast=TimedValue(value, self.as_of),
                label="synthetic_s09_forecast_block_output",
                input_status=SourceRuleStatus.LOCKED,
            )
            for member_id, by_span in values.items()
            for span, value in by_span.items()
        )

    def locks(self) -> P05CompleteTrendPortfolioSourceLocks:
        return P05CompleteTrendPortfolioSourceLocks(
            s09_input_provenance_status=SourceRuleStatus.LOCKED,
            member_identity_status=SourceRuleStatus.LOCKED,
            member_taxonomy_status=SourceRuleStatus.LOCKED,
            instrument_weight_status=SourceRuleStatus.LOCKED,
            idm_status=SourceRuleStatus.LOCKED,
            target_risk_capital_status=SourceRuleStatus.LOCKED,
            price_risk_status=SourceRuleStatus.LOCKED,
            fx_status=SourceRuleStatus.LOCKED,
            cost_eligibility_status=SourceRuleStatus.LOCKED,
            eligible_speed_set_status=SourceRuleStatus.LOCKED,
            forecast_weight_status=SourceRuleStatus.LOCKED,
            fdm_status=SourceRuleStatus.LOCKED,
            forecast_cap_status=SourceRuleStatus.LOCKED,
            position_input_status=SourceRuleStatus.LOCKED,
            output_boundary_status=SourceRuleStatus.LOCKED,
        )


if __name__ == "__main__":
    unittest.main()

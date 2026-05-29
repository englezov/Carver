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
from carver.spine.p07 import (  # noqa: E402
    P07_BOOK_REFERENCE_TARGET_RISK,
    P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_ID,
    P07_FORECAST_DIVISOR,
    P07_JUMBO_REFERENCE_IDM,
    P07CompleteCombinedPortfolioRequest,
    P07CompleteCombinedPortfolioSourceLocks,
    P07SyntheticMarketInput,
    P07SyntheticMember,
    P07SyntheticS11CombinedForecastInput,
    p07_complete_combined_trend_carry_portfolio_conformance,
    p07_handcrafted_instrument_weights,
)


class P07CompleteCombinedTrendCarryPortfolioSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.as_of = datetime(2026, 5, 29, tzinfo=timezone.utc)
        self.completed_bar = CompletedBar(self.as_of)

    def test_p07_emits_complete_combined_desired_position_inputs_only(self) -> None:
        result = p07_complete_combined_trend_carry_portfolio_conformance(self.request())

        self.assertEqual(result.portfolio_id, P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_ID)
        self.assertEqual(result.member_ids, ("SYN_BOND_A", "SYN_BOND_B", "SYN_EQUITY_A", "SYN_ENERGY_A"))
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
        self.assertAlmostEqual(by_member["SYN_ENERGY_A"].instrument_weight, 1.0 / 3.0)

        self.assertAlmostEqual(by_member["SYN_BOND_A"].final_capped_s11_combined_forecast, 7.5)
        self.assertAlmostEqual(by_member["SYN_BOND_B"].final_capped_s11_combined_forecast, -2.0)
        self.assertAlmostEqual(by_member["SYN_EQUITY_A"].final_capped_s11_combined_forecast, FORECAST_CAP)
        self.assertAlmostEqual(by_member["SYN_ENERGY_A"].final_capped_s11_combined_forecast, 3.25)
        for member in result.member_results:
            self.assertAlmostEqual(member.forecast_multiplier, member.final_capped_s11_combined_forecast / P07_FORECAST_DIVISOR)
            self.assertAlmostEqual(
                member.desired_unrounded_contracts,
                member.base_sizing.unrounded_contracts * member.forecast_multiplier,
            )

    def test_handcrafted_weights_follow_asset_group_member_taxonomy(self) -> None:
        weights = p07_handcrafted_instrument_weights(self.members())

        self.assertAlmostEqual(sum(weights.values()), 1.0)
        self.assertEqual(tuple(weights), ("SYN_BOND_A", "SYN_BOND_B", "SYN_EQUITY_A", "SYN_ENERGY_A"))
        self.assertAlmostEqual(weights["SYN_BOND_A"], 1.0 / 6.0)
        self.assertAlmostEqual(weights["SYN_BOND_B"], 1.0 / 6.0)
        self.assertAlmostEqual(weights["SYN_EQUITY_A"], 1.0 / 3.0)
        self.assertAlmostEqual(weights["SYN_ENERGY_A"], 1.0 / 3.0)

    def test_p07_consumes_locked_synthetic_s11_outputs_without_recombining_rules(self) -> None:
        result = p07_complete_combined_trend_carry_portfolio_conformance(self.request())
        equity = {member.member_id: member for member in result.member_results}["SYN_EQUITY_A"]

        self.assertEqual(equity.final_capped_s11_combined_forecast, FORECAST_CAP)
        self.assertAlmostEqual(equity.forecast_multiplier, 2.0)
        self.assertTrue(all(hasattr(member, "base_sizing") for member in result.member_results))
        self.assertFalse(hasattr(equity, "s09_forecast_block"))
        self.assertFalse(hasattr(equity, "s10_forecast_block"))

    def test_p07_fails_closed_on_unresolved_locks_and_non_source_native_lane(self) -> None:
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(
                self.request(source_locks=replace(self.locks(), output_boundary_status=SourceRuleStatus.UNRESOLVED))
            )
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(
                self.request(source_locks=replace(self.locks(), s11_input_provenance_status=SourceRuleStatus.UNRESOLVED))
            )
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(lane_class=LaneClass.CFD_ADAPTER))

    def test_p07_fails_closed_on_s11_input_label_status_timestamp_and_uncapped_values(self) -> None:
        forecasts = list(self.s11_forecast_inputs())
        forecasts[0] = replace(forecasts[0], label="production_s11_combined_forecast")
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(s11_forecast_inputs=tuple(forecasts)))

        forecasts = list(self.s11_forecast_inputs())
        forecasts[0] = replace(forecasts[0], input_status=SourceRuleStatus.UNRESOLVED)
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(s11_forecast_inputs=tuple(forecasts)))

        forecasts = list(self.s11_forecast_inputs())
        forecasts[0] = replace(forecasts[0], final_capped_s11_forecast=TimedValue(6.0, self.as_of - timedelta(days=1)))
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(s11_forecast_inputs=tuple(forecasts)))

        forecasts = list(self.s11_forecast_inputs())
        forecasts[0] = replace(forecasts[0], final_capped_s11_forecast=TimedValue(25.0, self.as_of))
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(s11_forecast_inputs=tuple(forecasts)))

    def test_p07_fails_closed_on_member_drop_or_s11_forecast_drift(self) -> None:
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(market_inputs=self.market_inputs()[:-1]))

        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(
                self.request(s11_forecast_inputs=self.s11_forecast_inputs()[:-1])
            )

        forecasts = list(self.s11_forecast_inputs())
        forecasts[0] = replace(forecasts[0], member_id="SYN_UNKNOWN")
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(s11_forecast_inputs=tuple(forecasts)))

    def test_p07_fails_closed_on_member_identity_taxonomy_and_prevalidation(self) -> None:
        members = list(self.members())
        members[0] = replace(members[0], member_id="SYN_BAD_CODE")
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(members=tuple(members)))

        members = list(self.members())
        members[1] = replace(members[1], taxonomy_status=SourceRuleStatus.UNRESOLVED)
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(members=tuple(members)))

        markets = list(self.market_inputs())
        markets[0] = replace(markets[0], price_risk_prevalidated=False)
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(market_inputs=tuple(markets)))

        markets = list(self.market_inputs())
        markets[2] = replace(markets[2], cost_eligibility_prevalidated=False)
        with self.assertRaises(CarverBlocked):
            p07_complete_combined_trend_carry_portfolio_conformance(self.request(market_inputs=tuple(markets)))

    def test_p07_conformance_doc_records_boundary(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_2026-05-29.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "PROCESS_AND_SYNTHETIC_CODE_CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST",
            text,
        )
        self.assertIn("Strategy Eleven", text)
        self.assertIn("S11 combined carry/trend forecast outputs", text)
        self.assertIn("desired position inputs only", text)
        self.assertIn("No real data", text)
        self.assertIn("no production source locks", text)

    def request(
        self,
        *,
        members: tuple[P07SyntheticMember, ...] | None = None,
        market_inputs: tuple[P07SyntheticMarketInput, ...] | None = None,
        s11_forecast_inputs: tuple[P07SyntheticS11CombinedForecastInput, ...] | None = None,
        source_locks: P07CompleteCombinedPortfolioSourceLocks | None = None,
        lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES,
    ) -> P07CompleteCombinedPortfolioRequest:
        return P07CompleteCombinedPortfolioRequest(
            completed_bar=self.completed_bar,
            members=members or self.members(),
            market_inputs=market_inputs or self.market_inputs(),
            s11_forecast_inputs=s11_forecast_inputs or self.s11_forecast_inputs(),
            capital=TimedValue(50_000_000.0, self.as_of),
            target_risk=TimedValue(P07_BOOK_REFERENCE_TARGET_RISK, self.as_of),
            idm=TimedValue(P07_JUMBO_REFERENCE_IDM, self.as_of),
            source_locks=source_locks or self.locks(),
            rounding_policy=RoundingPolicy.TRUNCATE,
            lane_class=lane_class,
        )

    def members(self) -> tuple[P07SyntheticMember, ...]:
        return (
            self.member("SYN_BOND_A", "Rates", "US bonds", 1000.0),
            self.member("SYN_BOND_B", "Rates", "US bonds", 1000.0),
            self.member("SYN_EQUITY_A", "Equity", "US equity", 5.0),
            self.member("SYN_ENERGY_A", "Energy", "Crude oil", 500.0),
        )

    def member(self, code: str, asset_class: str, group: str, multiplier: float) -> P07SyntheticMember:
        return P07SyntheticMember(
            member_id=code,
            contract=ContractSpec(code, f"{code} synthetic future", "SYNEX", "USD", multiplier),
            asset_class=asset_class,
            group=group,
            identity_status=SourceRuleStatus.LOCKED,
            taxonomy_status=SourceRuleStatus.LOCKED,
        )

    def market_inputs(self) -> tuple[P07SyntheticMarketInput, ...]:
        return (
            self.market("SYN_BOND_A", 112.0, 0.07, 0.45, 0.004),
            self.market("SYN_BOND_B", 98.0, 0.08, 0.49, 0.005),
            self.market("SYN_EQUITY_A", 5200.0, 0.22, 71.5, 0.002),
            self.market("SYN_ENERGY_A", 78.0, 0.32, 1.62, 0.006),
        )

    def market(self, member_id: str, price: float, risk: float, daily_price_risk: float, cost: float) -> P07SyntheticMarketInput:
        return P07SyntheticMarketInput(
            member_id=member_id,
            current_held_price=TimedValue(price, self.as_of),
            annual_risk_estimate=TimedValue(risk, self.as_of),
            daily_price_risk=TimedValue(daily_price_risk, self.as_of),
            fx_rate=TimedValue(1.0, self.as_of),
            risk_adjusted_cost_per_trade=TimedValue(cost, self.as_of),
        )

    def s11_forecast_inputs(self) -> tuple[P07SyntheticS11CombinedForecastInput, ...]:
        values = {
            "SYN_BOND_A": 7.5,
            "SYN_BOND_B": -2.0,
            "SYN_EQUITY_A": 20.0,
            "SYN_ENERGY_A": 3.25,
        }
        return tuple(
            P07SyntheticS11CombinedForecastInput(
                member_id=member_id,
                final_capped_s11_forecast=TimedValue(value, self.as_of),
                label="synthetic_s11_combined_carry_trend_forecast_output",
                input_status=SourceRuleStatus.LOCKED,
            )
            for member_id, value in values.items()
        )

    def locks(self) -> P07CompleteCombinedPortfolioSourceLocks:
        return P07CompleteCombinedPortfolioSourceLocks(
            s11_input_provenance_status=SourceRuleStatus.LOCKED,
            member_identity_status=SourceRuleStatus.LOCKED,
            member_taxonomy_status=SourceRuleStatus.LOCKED,
            instrument_weight_status=SourceRuleStatus.LOCKED,
            idm_status=SourceRuleStatus.LOCKED,
            target_risk_capital_status=SourceRuleStatus.LOCKED,
            price_risk_status=SourceRuleStatus.LOCKED,
            fx_status=SourceRuleStatus.LOCKED,
            cost_eligibility_status=SourceRuleStatus.LOCKED,
            forecast_cap_status=SourceRuleStatus.LOCKED,
            position_input_status=SourceRuleStatus.LOCKED,
            output_boundary_status=SourceRuleStatus.LOCKED,
        )


if __name__ == "__main__":
    unittest.main()

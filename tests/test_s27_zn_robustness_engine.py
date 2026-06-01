from __future__ import annotations

import unittest
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "audit" / "carver_s27_zn_robustness.py"
SPEC = importlib.util.spec_from_file_location("carver_s27_zn_robustness", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
robustness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(robustness)

beta_strip_rows = robustness.beta_strip_rows
delayed_position_rows = robustness.delayed_position_rows
random_position_rows = robustness.random_position_rows
shuffled_position_rows = robustness.shuffled_position_rows
summarize_position_rows = robustness.summarize_position_rows


class S27ZNRobsutnessEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = (
            {
                "entry_bar_end_utc": "2022-01-01T00:00:00Z",
                "entry_completed_trading_date": "2022-01-01",
                "entry_raw_symbol": "ZNH2",
                "capped_forecast": "10.0",
                "m1_ladder_contracts": "2",
                "unit_no_ladder_contracts": "1",
                "price_change_points": "0.5",
                "zn_contract_multiplier": "1000.0",
                "m1_ladder_estimated_etf_fee_usd": "1.0",
                "unit_estimated_etf_fee_usd": "1.0",
            },
            {
                "entry_bar_end_utc": "2022-01-01T01:00:00Z",
                "entry_completed_trading_date": "2022-01-01",
                "entry_raw_symbol": "ZNH2",
                "capped_forecast": "-10.0",
                "m1_ladder_contracts": "-1",
                "unit_no_ladder_contracts": "-1",
                "price_change_points": "-0.25",
                "zn_contract_multiplier": "1000.0",
                "m1_ladder_estimated_etf_fee_usd": "2.0",
                "unit_estimated_etf_fee_usd": "2.0",
            },
            {
                "entry_bar_end_utc": "2022-01-01T02:00:00Z",
                "entry_completed_trading_date": "2022-01-01",
                "entry_raw_symbol": "ZNH2",
                "capped_forecast": "5.0",
                "m1_ladder_contracts": "1",
                "unit_no_ladder_contracts": "1",
                "price_change_points": "-0.125",
                "zn_contract_multiplier": "1000.0",
                "m1_ladder_estimated_etf_fee_usd": "3.0",
                "unit_estimated_etf_fee_usd": "3.0",
            },
        )

    def test_summarize_position_rows_computes_signal_attributable_pnl(self) -> None:
        active = summarize_position_rows(
            self.rows,
            position_field="m1_ladder_contracts",
            fee_field="m1_ladder_estimated_etf_fee_usd",
        )
        beta = summarize_position_rows(
            beta_strip_rows(self.rows, notional_position=1),
            position_field="robustness_contracts",
            fee_field="robustness_fee_usd",
        )

        self.assertEqual(active["rows"], 3)
        self.assertEqual(active["gross_pnl_usd"], 1125.0)
        self.assertEqual(active["net_pnl_usd"], 1119.0)
        self.assertEqual(beta["net_pnl_usd"], 125.0)
        self.assertEqual(active["net_pnl_usd"] - beta["net_pnl_usd"], 994.0)

    def test_shuffled_positions_preserve_multiset_but_change_order(self) -> None:
        shuffled = tuple(shuffled_position_rows(self.rows, position_field="m1_ladder_contracts", seed=7))

        self.assertCountEqual([row["robustness_contracts"] for row in shuffled], [2, -1, 1])
        self.assertNotEqual([row["robustness_contracts"] for row in shuffled], [2, -1, 1])

    def test_random_positions_preserve_abs_distribution_and_seed(self) -> None:
        first = tuple(random_position_rows(self.rows, position_field="m1_ladder_contracts", seed=11))
        second = tuple(random_position_rows(self.rows, position_field="m1_ladder_contracts", seed=11))

        self.assertEqual(first, second)
        self.assertCountEqual([abs(row["robustness_contracts"]) for row in first], [2, 1, 1])
        self.assertTrue(all(row["robustness_contracts"] != 0 for row in first))

    def test_delayed_positions_shift_by_one_and_zero_first_row(self) -> None:
        delayed = tuple(delayed_position_rows(self.rows, position_field="m1_ladder_contracts", lag=1))

        self.assertEqual([row["robustness_contracts"] for row in delayed], [0, 2, -1])

    def test_window_validation_fails_closed_on_mislabeled_long_window(self) -> None:
        rows = [
            {"entry_completed_trading_date": "2021-01-01"},
            {"entry_completed_trading_date": "2023-01-02"},
        ]

        validation = robustness._window_validation_rows("2022_2023_INITIAL_DEV_RECON", rows)

        self.assertEqual(validation[0]["check"], "WINDOW_SCOPE")
        self.assertEqual(validation[0]["status"], "FAIL_WINDOW_GREATER_THAN_TWO_YEARS_DATE_BOUND")
        self.assertEqual(validation[0]["window_start"], "2021-01-01")
        self.assertEqual(validation[0]["window_end"], "2023-01-02")

    def test_preflight_fails_closed_before_summaries_on_unexpected_window(self) -> None:
        rows = [
            {
                "window_label": "LOCKBOX",
                "entry_completed_trading_date": "2025-01-02",
                "entry_bar_end_utc": "2025-01-02T04:00:00Z",
                "exit_bar_end_utc": "2025-01-02T05:00:00Z",
                "forecast_status": "PASS_S27_FORECAST_RUNTIME_DEV_RECON_ONLY",
                "same_input_status": "PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET",
            }
        ]

        with self.assertRaises(SystemExit) as raised:
            robustness._preflight_robustness_windows(rows)

        self.assertIn("unexpected window labels", str(raised.exception))

    def test_preflight_fails_closed_before_summaries_on_duplicate_or_unordered_rows(self) -> None:
        duplicate_rows = [
            {
                "window_label": "2022_2023_INITIAL_DEV_RECON",
                "entry_completed_trading_date": "2022-01-04",
                "entry_bar_end_utc": "2022-01-04T04:00:00Z",
                "exit_bar_end_utc": "2022-01-04T05:00:00Z",
                "forecast_status": "PASS_S27_FORECAST_RUNTIME_DEV_RECON_ONLY",
                "same_input_status": "PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET",
            },
            {
                "window_label": "2022_2023_INITIAL_DEV_RECON",
                "entry_completed_trading_date": "2022-01-04",
                "entry_bar_end_utc": "2022-01-04T04:00:00Z",
                "exit_bar_end_utc": "2022-01-04T05:00:00Z",
                "forecast_status": "PASS_S27_FORECAST_RUNTIME_DEV_RECON_ONLY",
                "same_input_status": "PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET",
            },
            {
                "window_label": "2024_VALIDATION_STYLE",
                "entry_completed_trading_date": "2024-01-02",
                "entry_bar_end_utc": "2024-01-02T04:00:00Z",
                "exit_bar_end_utc": "2024-01-02T05:00:00Z",
                "forecast_status": "PASS_S27_FORECAST_RUNTIME_DEV_RECON_ONLY",
                "same_input_status": "PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET",
            },
        ]

        with self.assertRaises(SystemExit) as raised:
            robustness._preflight_robustness_windows(duplicate_rows)

        self.assertIn("duplicate entry_bar_end_utc", str(raised.exception))

    def test_summary_rows_label_fractional_beta_strip_as_non_tradable(self) -> None:
        summary_rows = robustness._window_summary_rows("2022_2023_INITIAL_DEV_RECON", list(self.rows))
        matched = next(row for row in summary_rows if row["measure"] == "CONSTANT_LONG_MATCHED_AVG_ABS_POSITION_BETA_STRIP")
        signal_attributable = next(row for row in summary_rows if row["measure"] == "SIGNAL_ATTRIBUTABLE_M1_MINUS_MATCHED_AVG_ABS_BETA")

        self.assertEqual(
            matched["baseline_interpretation"],
            "ATTRIBUTION_ONLY_FRACTIONAL_EXPOSURE_BASELINE_NOT_TRADABLE_POSITION",
        )
        self.assertEqual(
            signal_attributable["baseline_interpretation"],
            "ATTRIBUTION_ONLY_M1_MINUS_FRACTIONAL_BETA_BASELINE_NOT_TRADABLE_POSITION",
        )

    def test_forward_horizon_structure_uses_signal_aligned_future_price_change(self) -> None:
        rows = [
            {
                "capped_forecast": "10",
                "entry_continuous_close": "100",
            },
            {
                "capped_forecast": "10",
                "entry_continuous_close": "99",
            },
            {
                "capped_forecast": "-10",
                "entry_continuous_close": "101",
            },
        ]

        horizon_rows = robustness._forward_horizon_rows("2022_2023_INITIAL_DEV_RECON", rows, horizons=(1, 2))

        self.assertEqual(horizon_rows[0]["horizon_bars"], 1)
        self.assertEqual(horizon_rows[0]["mean_signal_aligned_forward_points"], 0.5)
        self.assertEqual(horizon_rows[1]["horizon_bars"], 2)
        self.assertEqual(horizon_rows[1]["mean_signal_aligned_forward_points"], 1.0)


if __name__ == "__main__":
    unittest.main()

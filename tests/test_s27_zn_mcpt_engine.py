from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "audit" / "carver_s27_zn_mcpt.py"
SPEC = importlib.util.spec_from_file_location("carver_s27_zn_mcpt", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
mcpt = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mcpt)


class S27ZNMcptEngineTests(unittest.TestCase):
    def test_one_sided_p_value_uses_plus_one_correction(self) -> None:
        nulls = np.array([1.0, 2.0, 3.0, 4.0])

        self.assertEqual(mcpt.one_sided_upper_p_value(3.0, nulls), 0.6)

    def test_position_fee_recomputes_shifted_position_turnover(self) -> None:
        positions = np.array([1.0, -1.0, -1.0, 2.0])
        roll_fee_sides = np.zeros(4)

        fees = mcpt.position_fee_usd(positions, roll_fee_sides)

        self.assertEqual(fees, 7.55)

    def test_stationary_block_bootstrap_indices_are_seed_deterministic(self) -> None:
        first = mcpt.stationary_block_bootstrap_indices(10, mean_block_length=3, rng=np.random.default_rng(7))
        second = mcpt.stationary_block_bootstrap_indices(10, mean_block_length=3, rng=np.random.default_rng(7))

        self.assertEqual(first.tolist(), second.tolist())
        self.assertEqual(len(first), 10)
        self.assertTrue(np.all((first >= 0) & (first < 10)))

    def test_max_t_adjustment_uses_trialwise_family_max(self) -> None:
        observed = 10.0
        nulls_by_family = {
            "A": np.array([1.0, 11.0, 2.0]),
            "B": np.array([9.0, 8.0, 12.0]),
        }

        adjusted = mcpt.max_t_adjusted_p_value(observed, nulls_by_family)

        self.assertEqual(adjusted, 0.75)

    def test_mcpt_preflight_fails_closed_on_out_of_bounds_window_dates(self) -> None:
        rows = [
            {
                "window_label": "2022_2023_INITIAL_DEV_RECON",
                "entry_completed_trading_date": "2021-12-31",
                "entry_bar_end_utc": "2021-12-31T04:00:00Z",
                "exit_bar_end_utc": "2021-12-31T05:00:00Z",
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
            mcpt.preflight_rows(rows)

        self.assertIn("outside declared MCPT bounds", str(raised.exception))

    def test_mcpt_preflight_fails_closed_on_unordered_rows(self) -> None:
        rows = [
            {
                "window_label": "2022_2023_INITIAL_DEV_RECON",
                "entry_completed_trading_date": "2022-01-04",
                "entry_bar_end_utc": "2022-01-04T05:00:00Z",
                "exit_bar_end_utc": "2022-01-04T06:00:00Z",
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
            mcpt.preflight_rows(rows)

        self.assertIn("not chronological", str(raised.exception))

    def test_mcpt_interpretation_keeps_touched_2024_out_of_lockbox(self) -> None:
        self.assertEqual(
            mcpt.mcpt_interpretation("2022_2023_INITIAL_DEV_RECON", 0.6254),
            "PRIMARY_TEST_WINDOW_NOT_SIGNIFICANT_NOT_LOCKBOX",
        )
        self.assertEqual(
            mcpt.mcpt_interpretation("2024_VALIDATION_STYLE", 0.012),
            "TOUCHED_2024_MCPT_THRESHOLD_HIT_INFORMATIONAL_NOT_LOCKBOX",
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
MODULE_PATH = ROOT / "tools" / "databento" / "carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("s27_corrected_runner_for_test", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class S27CorrectedBacktestRunnerPreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = load_runner_module()

    def test_runner_requires_explicit_backtest_authorization_before_inputs(self) -> None:
        old = os.environ.pop(self.runner.AUTH_ENV_VAR, None)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.runner.OUTPUT_ROOT = Path(tmp) / "backtest_output"
                with self.assertRaises(SystemExit) as raised:
                    self.runner.main()
                self.assertIn("requires", str(raised.exception))
                self.assertFalse((self.runner.OUTPUT_ROOT / "corrected_runtime_alignment_rows").exists())
        finally:
            if old is not None:
                os.environ[self.runner.AUTH_ENV_VAR] = old

    def test_forecast_builder_consumes_locked_runtime_ledgers_not_hourly_equilibrium(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for name in ("hourly.csv", "sigma.csv", "equilibrium.csv", "trend.csv", "vol.csv"):
                (tmp_path / name).write_text("fixture\n", encoding="utf-8")
            self.runner.HOURLY_SOURCE_CSV = tmp_path / "hourly.csv"
            self.runner.S26_SIGMA_RUNTIME_CSV = tmp_path / "sigma.csv"
            self.runner.S26_DAILY_EQUILIBRIUM_RUNTIME_CSV = tmp_path / "equilibrium.csv"
            self.runner.S27_TREND_RUNTIME_CSV = tmp_path / "trend.csv"
            self.runner.S27_VOL_RUNTIME_CSV = tmp_path / "vol.csv"

            as_of = "2022-01-05T15:00:00+00:00"
            hourly = [self.hourly_row(as_of=as_of, completed_date="2022-01-05", close=100.0)]
            runtime_ledgers = {
                "sigma": {as_of: self.runtime(as_of, runtime_status=self.runner.S26_ZN_SIGMA_RUNTIME_STATUS, sigma_percent_t="0.16")},
                "equilibrium": {
                    as_of: self.runtime(
                        as_of,
                        runtime_status=self.runner.S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS,
                        method_status=self.runner.S26_DAILY_EQUILIBRIUM_METHOD_STATUS,
                        equilibrium_ewma_5="105.0",
                        last_daily_row_used="2022-01-04",
                    )
                },
                "trend": {
                    as_of: self.runtime(
                        as_of,
                        runtime_status=self.runner.S27_TREND_RUNTIME_STATUS,
                        method_status=self.runner.S27_DAILY_TREND_METHOD_STATUS,
                        trend_forecast="1.0",
                        last_daily_row_used="2022-01-04",
                    )
                },
                "vol": {
                    as_of: self.runtime(
                        as_of,
                        runtime_status=self.runner.S27_VOL_ATTENUATION_RUNTIME_STATUS,
                        method_status=self.runner.S27_DAILY_VOL_ATTENUATION_METHOD_STATUS,
                        vol_multiplier="0.75",
                        source_vqm_completed_trading_date="2022-01-04",
                    )
                },
            }

            s26_rows, s27_rows, blocked_rows, alignment_rows = self.runner._build_forecasts(hourly, runtime_ledgers)

            self.assertEqual(blocked_rows, [])
            self.assertEqual(len(alignment_rows), 1)
            self.assertAlmostEqual(s26_rows[0]["equilibrium_ewma5"], 105.0)
            self.assertAlmostEqual(s26_rows[0]["raw_forecast_equilibrium_minus_price"], 5.0)
            self.assertAlmostEqual(s27_rows[0]["adjusted_raw_forecast"], 3.75)
            self.assertEqual(alignment_rows[0]["alignment_status"], "PASS_CORRECTED_RUNTIME_ROWS_MATCH_FORECAST_TIMESTAMP")

    def test_forecast_builder_rejects_old_vqm_method_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for name in ("hourly.csv", "sigma.csv", "equilibrium.csv", "trend.csv", "vol.csv"):
                (tmp_path / name).write_text("fixture\n", encoding="utf-8")
            self.runner.HOURLY_SOURCE_CSV = tmp_path / "hourly.csv"
            self.runner.S26_SIGMA_RUNTIME_CSV = tmp_path / "sigma.csv"
            self.runner.S26_DAILY_EQUILIBRIUM_RUNTIME_CSV = tmp_path / "equilibrium.csv"
            self.runner.S27_TREND_RUNTIME_CSV = tmp_path / "trend.csv"
            self.runner.S27_VOL_RUNTIME_CSV = tmp_path / "vol.csv"
            as_of = "2022-01-05T15:00:00+00:00"
            runtime_ledgers = self.valid_runtime_ledgers(as_of)
            runtime_ledgers["vol"][as_of]["method_status"] = "LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME"

            with self.assertRaises(SystemExit):
                self.runner._build_forecasts(
                    [self.hourly_row(as_of=as_of, completed_date="2022-01-05", close=100.0)],
                    runtime_ledgers,
                )

    def valid_runtime_ledgers(self, as_of: str):
        return {
            "sigma": {as_of: self.runtime(as_of, runtime_status=self.runner.S26_ZN_SIGMA_RUNTIME_STATUS, sigma_percent_t="0.16")},
            "equilibrium": {
                as_of: self.runtime(
                    as_of,
                    runtime_status=self.runner.S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS,
                    method_status=self.runner.S26_DAILY_EQUILIBRIUM_METHOD_STATUS,
                    equilibrium_ewma_5="105.0",
                    last_daily_row_used="2022-01-04",
                )
            },
            "trend": {
                as_of: self.runtime(
                    as_of,
                    runtime_status=self.runner.S27_TREND_RUNTIME_STATUS,
                    method_status=self.runner.S27_DAILY_TREND_METHOD_STATUS,
                    trend_forecast="1.0",
                    last_daily_row_used="2022-01-04",
                )
            },
            "vol": {
                as_of: self.runtime(
                    as_of,
                    runtime_status=self.runner.S27_VOL_ATTENUATION_RUNTIME_STATUS,
                    method_status=self.runner.S27_DAILY_VOL_ATTENUATION_METHOD_STATUS,
                    vol_multiplier="0.75",
                    source_vqm_completed_trading_date="2022-01-04",
                )
            },
        }

    def hourly_row(self, *, as_of: str, completed_date: str, close: float):
        return {
            "row_id": "APPENDIX_C_172_004",
            "author_market_code": "ZN",
            "instrument_id": "42000661",
            "raw_symbol": "ZNM6",
            "completed_trading_date": completed_date,
            "derived_completed_bar_end_utc": as_of,
            "continuous_close": str(close),
        }

    def runtime(self, as_of: str, **overrides):
        row = {
            "row_id": "APPENDIX_C_172_004",
            "author_market_code": "ZN",
            "instrument_id": "42000661",
            "raw_symbol": "ZNM6",
            "as_of": as_of,
            "runtime_status": "",
            "method_status": "",
            "no_lookahead_status": "PASS_NO_LOOKAHEAD",
        }
        row.update(overrides)
        return row


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
MODULE_PATH = ROOT / "tools" / "databento" / "carver_s27_zn_2022_2023_corrected_runtime_ledgers.py"


def load_module():
    spec = importlib.util.spec_from_file_location("s27_corrected_runtime_ledger_prep_for_test", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class S27CorrectedRuntimeLedgerPrepTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_runtime_prep_requires_explicit_authorization_before_outputs(self) -> None:
        old_auth = os.environ.pop(self.module.AUTH_ENV_VAR, None)
        old_output = os.environ.get("CARVER_S27_CORRECTED_RUNTIME_OUTPUT_ROOT")
        try:
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "runtime_ledgers"
                os.environ["CARVER_S27_CORRECTED_RUNTIME_OUTPUT_ROOT"] = str(out)
                with self.assertRaises(SystemExit) as raised:
                    self.module.main()
                self.assertIn(self.module.AUTH_ENV_VAR, str(raised.exception))
                self.assertFalse(out.exists())
        finally:
            if old_auth is not None:
                os.environ[self.module.AUTH_ENV_VAR] = old_auth
            if old_output is None:
                os.environ.pop("CARVER_S27_CORRECTED_RUNTIME_OUTPUT_ROOT", None)
            else:
                os.environ["CARVER_S27_CORRECTED_RUNTIME_OUTPUT_ROOT"] = old_output

    def test_builds_four_corrected_runtime_ledgers_from_fixture_rows(self) -> None:
        forecast = self.forecast_row(as_of="2021-03-15T14:00:00+00:00", completed_date="2021-03-15")
        daily = self.daily_rows(start=date(2021, 1, 1), count=70)
        sigma = [self.sigma_row(row["completed_trading_date"], 0.12) for row in daily]
        vqm = [self.vqm_row(row["completed_trading_date"], 0.75) for row in daily]

        ledgers = self.module._build_corrected_runtime_ledgers(
            forecast_rows=[forecast],
            daily_rows=daily,
            sigma_rows=sigma,
            vqm_rows=vqm,
            source_hashes={
                "hourly": "A" * 64,
                "r2_daily": "B" * 64,
                "vqm_daily": "C" * 64,
                "extended_daily": "D" * 64,
            },
        )

        self.assertEqual(set(ledgers), {"sigma", "equilibrium", "trend", "vol"})
        self.assertEqual([len(rows) for rows in ledgers.values()], [1, 1, 1, 1])
        self.assertEqual(ledgers["sigma"][0]["runtime_status"], self.module.S26_ZN_SIGMA_RUNTIME_STATUS)
        self.assertEqual(ledgers["equilibrium"][0]["method_status"], self.module.S26_DAILY_EQUILIBRIUM_METHOD_STATUS)
        self.assertEqual(ledgers["trend"][0]["method_status"], self.module.S27_DAILY_TREND_METHOD_STATUS)
        self.assertEqual(ledgers["vol"][0]["method_status"], self.module.S27_DAILY_VOL_ATTENUATION_METHOD_STATUS)
        self.assertEqual(ledgers["equilibrium"][0]["last_daily_row_used"], "2021-03-11")
        self.assertEqual(ledgers["trend"][0]["last_daily_row_used"], "2021-03-11")
        self.assertEqual(ledgers["vol"][0]["source_vqm_completed_trading_date"], "2021-03-11")
        self.assertEqual(ledgers["vol"][0]["vol_multiplier"], 0.75)
        for rows in ledgers.values():
            self.assertEqual(rows[0]["as_of"], forecast["derived_completed_bar_end_utc"])
            self.assertEqual(rows[0]["no_lookahead_status"], "PASS_NO_LOOKAHEAD")
            self.assertEqual(rows[0]["source_artifact_sha256"], "D" * 64)
            self.assertEqual(rows[0]["forecast_target_source_artifact_sha256"], "A" * 64)

    def test_rejects_missing_composite_source_hash(self) -> None:
        forecast = self.forecast_row(as_of="2021-03-15T14:00:00+00:00", completed_date="2021-03-15")
        daily = self.daily_rows(start=date(2021, 1, 1), count=70)
        sigma = [self.sigma_row(row["completed_trading_date"], 0.12) for row in daily]
        vqm = [self.vqm_row(row["completed_trading_date"], 0.75) for row in daily]

        with self.assertRaises(SystemExit):
            self.module._build_corrected_runtime_ledgers(
                forecast_rows=[forecast],
                daily_rows=daily,
                sigma_rows=sigma,
                vqm_rows=vqm,
                source_hashes={"hourly": "A" * 64, "r2_daily": "B" * 64, "vqm_daily": "C" * 64},
            )

    def test_rejects_non_strict_prior_vqm_dependency(self) -> None:
        forecast = self.forecast_row(as_of="2021-03-15T14:00:00+00:00", completed_date="2021-03-15")
        daily = self.daily_rows(start=date(2021, 1, 1), count=70)
        sigma = [self.sigma_row(row["completed_trading_date"], 0.12) for row in daily]
        vqm = [self.vqm_row("2021-03-15", 0.75)]

        with self.assertRaises(SystemExit):
            self.module._build_corrected_runtime_ledgers(
                forecast_rows=[forecast],
                daily_rows=daily,
                sigma_rows=sigma,
                vqm_rows=vqm,
                source_hashes={
                    "hourly": "A" * 64,
                    "r2_daily": "B" * 64,
                    "vqm_daily": "C" * 64,
                    "extended_daily": "D" * 64,
                },
            )

    def forecast_row(self, *, as_of: str, completed_date: str):
        return {
            "row_id": "APPENDIX_C_172_004",
            "author_market_code": "ZN",
            "instrument_id": "42000661",
            "raw_symbol": "ZNH2",
            "derived_completed_bar_end_utc": as_of,
            "completed_trading_date": completed_date,
        }

    def daily_rows(self, *, start: date, count: int):
        rows = []
        for offset in range(count):
            day = start + timedelta(days=offset)
            rows.append({"completed_trading_date": day.isoformat(), "continuous_close": 100.0 + offset})
        return rows

    def sigma_row(self, day: str, value: float):
        return {
            "completed_trading_date": day,
            "sigma_i_t": value,
            "source_window_start": "2021-01-01",
            "source_window_end": day,
            "source_window_rows": "34",
        }

    def vqm_row(self, day: str, multiplier: float):
        return {
            "completed_trading_date": day,
            "vol_multiplier_m_ewma10": multiplier,
            "relative_volatility_v": "1.1",
            "quantile_q": "0.5",
            "historical_v_observation_count": "10",
        }


if __name__ == "__main__":
    unittest.main()

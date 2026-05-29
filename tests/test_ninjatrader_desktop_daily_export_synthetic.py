from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked, ContractSpec  # noqa: E402
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402
from carver.spine.ninjatrader_desktop_export import (  # noqa: E402
    DEFAULT_NINJATRADER_DAILY_EXPORT_QUARANTINE,
    EXPECTED_NINJATRADER_DAILY_EXPORT_HEADER,
    S09_ZN_DESKTOP_DAILY_EXPORT_FILE_NAME,
    NinjaTraderDailyExportSpec,
    parse_ninjatrader_daily_export_file,
    parse_ninjatrader_daily_export_text,
    s09_zn_ninjatrader_daily_export_spec,
)


class NinjaTraderDesktopDailyExportSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = NinjaTraderDailyExportSpec(
            contract=zn_contract(),
            contract_month="06-26",
            display_symbol="ZN 06-26",
            expected_rows=257,
        )

    def rows(self, *data_rows: str) -> str:
        return ",".join(EXPECTED_NINJATRADER_DAILY_EXPORT_HEADER) + "\n" + "\n".join(data_rows) + "\n"

    def trade_date(self, offset: int) -> str:
        return (date(2026, 1, 1) + timedelta(days=offset)).isoformat()

    def data_row(self, instrument: str, contract_month: str, display_symbol: str, trade_date: str, close: float) -> str:
        return (
            f"{instrument},{contract_month},{display_symbol},Last,1 Day,{trade_date},"
            f"{close - 0.5},{close + 0.25},{close - 1.0},{close},1200"
        )

    def good_text(self) -> str:
        return self.rows(
            *(
                self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0)
                for offset in range(257)
            )
        )

    def test_s09_zn_export_spec_is_locked_to_257_daily_rows(self) -> None:
        spec = s09_zn_ninjatrader_daily_export_spec()

        self.assertEqual(spec.contract, zn_contract())
        self.assertEqual(spec.contract_month, "06-26")
        self.assertEqual(spec.display_symbol, "ZN 06-26")
        self.assertEqual(spec.expected_rows, 257)
        self.assertTrue(DEFAULT_NINJATRADER_DAILY_EXPORT_QUARANTINE.is_absolute())
        self.assertEqual(DEFAULT_NINJATRADER_DAILY_EXPORT_QUARANTINE, ROOT / "data" / "quarantine" / "ninjatrader" / "desktop_daily_exports")
        self.assertEqual(S09_ZN_DESKTOP_DAILY_EXPORT_FILE_NAME, "ZN_06-26_Daily_Last_257.csv")

    def test_parse_valid_locked_daily_export(self) -> None:
        bars = parse_ninjatrader_daily_export_text(self.good_text(), self.spec)

        self.assertEqual(len(bars), 257)
        self.assertEqual(bars[0].code, "ZN")
        self.assertEqual(bars[0].contract_month, "06-26")
        self.assertEqual(bars[0].timestamp.isoformat(), "2026-01-01T00:00:00+00:00")
        self.assertEqual(bars[-1].timestamp.isoformat(), f"{self.trade_date(256)}T00:00:00+00:00")
        self.assertEqual(bars[-1].volume, 1200.0)

    def test_parse_explicit_file_only_inside_desktop_export_quarantine(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "data" / "quarantine" / "ninjatrader" / "desktop_daily_exports"
            root.mkdir(parents=True)
            export_path = root / "ZN_06-26_Daily_Last_257.csv"
            export_path.write_text(self.good_text(), encoding="utf-8")

            bars = parse_ninjatrader_daily_export_file(export_path, self.spec, root)
            self.assertEqual(len(bars), 257)

            outside_path = Path(temporary_directory) / "ZN_06-26_Daily_Last_257.csv"
            outside_path.write_text(self.good_text(), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                parse_ninjatrader_daily_export_file(outside_path, self.spec, root)

            cache_path = root / "ZN_06-26.Last.ncd"
            cache_path.write_text(self.good_text(), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                parse_ninjatrader_daily_export_file(cache_path, self.spec, root)

            wrong_name_path = root / "ZN_06-26_Daily_Last_257_copy.csv"
            wrong_name_path.write_text(self.good_text(), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                parse_ninjatrader_daily_export_file(wrong_name_path, self.spec, root)

            with self.assertRaises(CarverBlocked):
                parse_ninjatrader_daily_export_file(root / "missing.csv", self.spec, root)
            with self.assertRaises(CarverBlocked):
                parse_ninjatrader_daily_export_file(export_path, self.spec, Path(temporary_directory) / "missing-root")

    def test_rejects_es_or_mes_substitution_and_display_symbol_drift(self) -> None:
        es_text = self.rows(
            *(
                self.data_row("ES", "06-26", "ES 06-26", self.trade_date(offset), 109.0 + offset / 100.0)
                for offset in range(257)
            )
        )
        mes_text = self.rows(
            *(
                self.data_row("MES", "06-26", "MES 06-26", self.trade_date(offset), 109.0 + offset / 100.0)
                for offset in range(257)
            )
        )
        es_spec = NinjaTraderDailyExportSpec(ContractSpec("ES", "E-mini S&P 500 future", "CME", "USD", 50), "06-26", "ES 06-26", expected_rows=257)
        mes_spec = NinjaTraderDailyExportSpec(mes_contract(), "06-26", "MES 06-26", expected_rows=257)
        zn_jun_display = self.rows(
            *(
                self.data_row("ZN", "06-26", "ZN JUN26", self.trade_date(offset), 109.0 + offset / 100.0)
                for offset in range(257)
            )
        )

        with self.assertRaises(CarverBlocked):
            parse_ninjatrader_daily_export_text(es_text, self.spec)
        with self.assertRaises(CarverBlocked):
            parse_ninjatrader_daily_export_text(mes_text, mes_spec)
        with self.assertRaises(CarverBlocked):
            parse_ninjatrader_daily_export_text(es_text, es_spec)
        with self.assertRaises(CarverBlocked):
            parse_ninjatrader_daily_export_text(zn_jun_display, self.spec)

    def test_rejects_bad_header_wrong_route_and_wrong_count(self) -> None:
        with self.assertRaises(CarverBlocked):
            parse_ninjatrader_daily_export_text("", self.spec)
        with self.assertRaises(CarverBlocked):
            parse_ninjatrader_daily_export_text("trade_date,close\n2026-05-28,110\n", self.spec)
        wrong_bar_type = self.rows(
            *(
                self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0).replace(",Last,", ",Bid,")
                for offset in range(257)
            )
        )
        wrong_timeframe = self.rows(
            *(
                self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0).replace(",1 Day,", ",1 Minute,")
                for offset in range(257)
            )
        )
        wrong_count = self.rows(
            *(self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0) for offset in range(256))
        )
        for text in (wrong_bar_type, wrong_timeframe, wrong_count):
            with self.subTest(text=text):
                with self.assertRaises(CarverBlocked):
                    parse_ninjatrader_daily_export_text(text, self.spec)

    def test_rejects_bad_dates_ordering_numbers_and_ohlc_shape(self) -> None:
        duplicate = self.rows(
            self.data_row("ZN", "06-26", "ZN 06-26", "2026-01-01", 109.0),
            self.data_row("ZN", "06-26", "ZN 06-26", "2026-01-01", 109.5),
            *(self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0) for offset in range(2, 257)),
        )
        unsorted = self.rows(
            self.data_row("ZN", "06-26", "ZN 06-26", "2026-01-02", 109.5),
            self.data_row("ZN", "06-26", "ZN 06-26", "2026-01-01", 109.0),
            *(self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0) for offset in range(2, 257)),
        )
        bad_date = self.rows(
            self.data_row("ZN", "06-26", "ZN 06-26", "2026/01/01", 109.0),
            *(self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0) for offset in range(1, 257)),
        )
        bad_high = self.rows(
            "ZN,06-26,ZN 06-26,Last,1 Day,2026-01-01,109.0,109.1,108.5,109.5,1000",
            *(self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0) for offset in range(1, 257)),
        )
        bad_low = self.rows(
            "ZN,06-26,ZN 06-26,Last,1 Day,2026-01-01,109.0,110.0,109.6,109.5,1000",
            *(self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0) for offset in range(1, 257)),
        )
        negative_volume = self.rows(
            "ZN,06-26,ZN 06-26,Last,1 Day,2026-01-01,109.0,110.0,108.5,109.5,-1",
            *(self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0) for offset in range(1, 257)),
        )
        non_finite = self.rows(
            "ZN,06-26,ZN 06-26,Last,1 Day,2026-01-01,NaN,110.0,108.5,109.5,1000",
            *(self.data_row("ZN", "06-26", "ZN 06-26", self.trade_date(offset), 109.0 + offset / 100.0) for offset in range(1, 257)),
        )

        for text in (duplicate, unsorted, bad_date, bad_high, bad_low, negative_volume, non_finite):
            with self.subTest(text=text):
                with self.assertRaises(CarverBlocked):
                    parse_ninjatrader_daily_export_text(text, self.spec)


if __name__ == "__main__":
    unittest.main()

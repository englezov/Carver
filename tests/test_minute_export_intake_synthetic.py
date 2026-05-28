from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked  # noqa: E402
from carver.spine.m3 import mes_contract  # noqa: E402
from carver.spine.minute_export import (  # noqa: E402
    EXPECTED_MINUTE_EXPORT_HEADER,
    MinuteExportSpec,
    parse_minute_export_text,
)


class MinuteExportIntakeSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = MinuteExportSpec(mes_contract(), "06-26")

    def rows(self, *data_rows: str) -> str:
        return ",".join(EXPECTED_MINUTE_EXPORT_HEADER) + "\n" + "\n".join(data_rows) + "\n"

    def good_text(self) -> str:
        return self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120",
            "MES,06-26,Last,1 Minute,2026-05-28T13:31:00+00:00,5001,5003,5000,5002,95",
        )

    def test_parse_valid_synthetic_minute_export(self) -> None:
        bars = parse_minute_export_text(self.good_text(), self.spec)

        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0].instrument, "MES")
        self.assertEqual(bars[0].contract_month, "06-26")
        self.assertEqual(bars[0].close, 5001.0)
        self.assertEqual(bars[1].volume, 95.0)

    def test_rejects_bad_header_and_empty_export(self) -> None:
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text("", self.spec)
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text("timestamp,open\n2026-05-28T13:30:00+00:00,5000\n", self.spec)
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(
                ",".join(EXPECTED_MINUTE_EXPORT_HEADER) + ",extra\n"
                "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120,x\n",
                self.spec,
            )
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(
                ",".join(EXPECTED_MINUTE_EXPORT_HEADER) + "\n"
                "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001\n",
                self.spec,
            )

    def test_rejects_wrong_contract_surface(self) -> None:
        wrong_instrument = self.rows(
            "ES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120"
        )
        wrong_month = self.rows(
            "MES,09-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120"
        )

        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(wrong_instrument, self.spec)
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(wrong_month, self.spec)
        with self.assertRaises(CarverBlocked):
            MinuteExportSpec(mes_contract(), "13-26").validate()
        with self.assertRaises(CarverBlocked):
            MinuteExportSpec(mes_contract(), "01-26").validate()

    def test_rejects_wrong_bar_type_and_timeframe(self) -> None:
        wrong_bar_type = self.rows(
            "MES,06-26,Bid,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120"
        )
        wrong_timeframe = self.rows(
            "MES,06-26,Last,5 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120"
        )

        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(wrong_bar_type, self.spec)
        with self.assertRaises(CarverBlocked):
            parse_minute_export_text(wrong_timeframe, self.spec)

    def test_rejects_incomplete_or_bad_timestamps(self) -> None:
        naive = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00,5000,5002,4999,5001,120"
        )
        second_aligned_bad = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:01+00:00,5000,5002,4999,5001,120"
        )
        unsorted = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:31:00+00:00,5001,5003,5000,5002,95",
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120",
        )
        duplicate = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120",
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5001,5003,5000,5002,95",
        )
        gap = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,120",
            "MES,06-26,Last,1 Minute,2026-05-28T13:32:00+00:00,5001,5003,5000,5002,95",
        )
        out_of_session = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T20:00:00+00:00,5000,5002,4999,5001,120"
        )
        wrong_offset = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+01:00,5000,5002,4999,5001,120"
        )
        invalid_text = self.rows(
            "MES,06-26,Last,1 Minute,not-a-time,5000,5002,4999,5001,120"
        )

        for text in (naive, second_aligned_bad, unsorted, duplicate, gap, out_of_session, wrong_offset, invalid_text):
            with self.subTest(text=text):
                with self.assertRaises(CarverBlocked):
                    parse_minute_export_text(text, self.spec)

    def test_rejects_bad_numbers_and_ohlc_shape(self) -> None:
        missing_open = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,,5002,4999,5001,120"
        )
        negative_price = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,-1,5002,4999,5001,120"
        )
        bad_volume = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,-1"
        )
        zero_price = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,0,5002,4999,5001,120"
        )
        non_finite = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,NaN,5002,4999,5001,120"
        )
        bad_high = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5000,4999,5001,120"
        )
        bad_low = self.rows(
            "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,5001,5001,120"
        )

        for text in (missing_open, negative_price, bad_volume, zero_price, non_finite, bad_high, bad_low):
            with self.subTest(text=text):
                with self.assertRaises(CarverBlocked):
                    parse_minute_export_text(text, self.spec)


if __name__ == "__main__":
    unittest.main()

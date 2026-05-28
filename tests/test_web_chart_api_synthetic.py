from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import ContractSpec, LaneClass, CarverBlocked  # noqa: E402
from carver.spine.web_chart_api import (  # noqa: E402
    ChartBarType,
    LockedWebChartSymbol,
    WebChartProbePlan,
    WebChartRequest,
    WebChartSymbol,
    assert_safe_web_chart_endpoint,
    normalize_web_chart_response,
)


class WebChartApiSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.es_contract = ContractSpec("ES", "E-mini S&P 500 future", "CME", "USD", 50)
        self.locked_symbol = LockedWebChartSymbol(self.es_contract, "06-26", "3570919", "ES JUN26")
        self.symbol = WebChartSymbol(self.locked_symbol, "3570919", "ES JUN26")
        self.request = WebChartRequest(
            symbol=self.symbol,
            bar_type=ChartBarType.MINUTE,
            element_size=1,
            element_count=2,
        )

    def epoch_ms(self, year: int, month: int, day: int, hour: int, minute: int) -> int:
        return int(datetime(year, month, day, hour, minute, tzinfo=timezone.utc).timestamp() * 1000)

    def payload(self) -> dict:
        return {
            "ok": True,
            "body": {
                "historicalId": 11,
                "realtimeId": 12,
                "items": [
                    {
                        "timestamp": self.epoch_ms(2026, 5, 28, 13, 30),
                        "open": 5000.0,
                        "high": 5002.0,
                        "low": 4999.0,
                        "close": 5001.0,
                        "upVolume": 70,
                        "downVolume": 50,
                        "complete": True,
                    },
                    {
                        "timestamp": self.epoch_ms(2026, 5, 28, 13, 31),
                        "open": 5001.0,
                        "high": 5003.0,
                        "low": 5000.0,
                        "close": 5002.0,
                        "volume": 95,
                        "complete": True,
                    },
                ],
            },
        }

    def test_builds_allowlisted_get_chart_payload(self) -> None:
        request_payload = self.request.payload()

        self.assertEqual(request_payload["symbol"], "3570919")
        self.assertEqual(request_payload["chartDescription"]["underlyingType"], "MinuteBar")
        self.assertEqual(request_payload["chartDescription"]["elementSize"], 1)
        self.assertEqual(request_payload["timeRange"]["asMuchAsElements"], 2)
        assert_safe_web_chart_endpoint("md/getChart")
        assert_safe_web_chart_endpoint("md/cancelChart")

    def test_normalizes_synthetic_web_chart_response(self) -> None:
        bars = normalize_web_chart_response(self.payload(), self.request)

        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0].timestamp, datetime(2026, 5, 28, 13, 30, tzinfo=timezone.utc))
        self.assertEqual(bars[0].volume, 120.0)
        self.assertEqual(bars[1].close, 5002.0)

    def test_rejects_trading_or_non_chart_endpoints(self) -> None:
        for endpoint in ("order/placeorder", "order/cancelorder", "account/list", "reports/requestreport"):
            with self.subTest(endpoint=endpoint):
                with self.assertRaises(CarverBlocked):
                    assert_safe_web_chart_endpoint(endpoint)
                with self.assertRaises(CarverBlocked):
                    replace(self.request, endpoint=endpoint).validate()

    def test_rejects_arbitrary_symbols_and_bulk_requests(self) -> None:
        with self.assertRaises(CarverBlocked):
            LockedWebChartSymbol(self.es_contract, "06-26", "ES JUN26", "ES JUN26").validate()
        with self.assertRaises(CarverBlocked):
            WebChartSymbol(self.locked_symbol, "9999999", "ES JUN26").validate()
        with self.assertRaises(CarverBlocked):
            WebChartSymbol(self.locked_symbol, "3570919", "MES JUN26").validate()
        with self.assertRaises(CarverBlocked):
            WebChartSymbol(self.locked_symbol, "3570919", "ES JUN26", LaneClass.CFD_ADAPTER).validate()
        with self.assertRaises(CarverBlocked):
            LockedWebChartSymbol(self.es_contract, "06-26", "9999999", "ES JUN26").validate()
        with self.assertRaises(CarverBlocked):
            replace(self.request, element_count=501).validate()
        with self.assertRaises(CarverBlocked):
            replace(self.request, with_histogram=True).validate()
        with self.assertRaises(CarverBlocked):
            replace(self.request, element_size_unit="Volume").validate()
        with self.assertRaises(CarverBlocked):
            replace(self.request, bar_type="MinuteBar").validate()

    def test_rejects_bad_response_shape(self) -> None:
        bad_payloads = (
            {"ok": False, "body": {"items": []}},
            {"ok": True},
            {"ok": True, "body": {"items": []}},
            {"ok": True, "body": {"items": [*self.payload()["body"]["items"], *self.payload()["body"]["items"]]}},
        )
        for payload in bad_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(CarverBlocked):
                    normalize_web_chart_response(payload, self.request)

    def test_rejects_bad_bars(self) -> None:
        base_item = self.payload()["body"]["items"][0]
        bad_items = (
            {**base_item, "timestamp": "bad"},
            {**base_item, "timestamp": self.epoch_ms(2026, 5, 28, 13, 30) + 1},
            {**base_item, "open": 0},
            {**base_item, "high": 4998},
            {**base_item, "low": 5002},
            {**base_item, "complete": False},
            {key: value for key, value in base_item.items() if key != "complete"},
            {key: value for key, value in base_item.items() if key not in {"volume", "upVolume", "downVolume"}},
        )
        for item in bad_items:
            with self.subTest(item=item):
                with self.assertRaises(CarverBlocked):
                    normalize_web_chart_response({"ok": True, "body": {"items": [item]}}, replace(self.request, element_count=1))

    def test_rejects_unordered_and_duplicate_timestamps(self) -> None:
        item_a, item_b = self.payload()["body"]["items"]
        duplicate = {"ok": True, "body": {"items": [item_a, item_a]}}
        unordered = {"ok": True, "body": {"items": [item_b, item_a]}}
        for payload in (duplicate, unordered):
            with self.subTest(payload=payload):
                with self.assertRaises(CarverBlocked):
                    normalize_web_chart_response(payload, self.request)

    def test_daily_request_requires_daily_alignment_and_size_one(self) -> None:
        daily_request = WebChartRequest(
            symbol=self.symbol,
            bar_type=ChartBarType.DAILY,
            element_size=1,
            element_count=1,
        )
        daily_payload = {
            "ok": True,
            "body": {
                "items": [
                    {
                        "timestamp": self.epoch_ms(2026, 5, 28, 0, 0),
                        "open": 5000,
                        "high": 5010,
                        "low": 4990,
                        "close": 5005,
                        "volume": 1000,
                        "complete": True,
                    }
                ]
            },
        }
        self.assertEqual(len(normalize_web_chart_response(daily_payload, daily_request)), 1)
        with self.assertRaises(CarverBlocked):
            replace(daily_request, element_size=5).validate()
        bad_daily = {"ok": True, "body": {"items": [{**daily_payload["body"]["items"][0], "timestamp": self.epoch_ms(2026, 5, 28, 13, 30)}]}}
        with self.assertRaises(CarverBlocked):
            normalize_web_chart_response(bad_daily, daily_request)

    def test_real_probe_is_disabled_until_explicitly_authorized(self) -> None:
        plan = WebChartProbePlan(self.request)
        with self.assertRaises(CarverBlocked):
            plan.require_authorized()
        WebChartProbePlan(self.request, execution_authorized=True).require_authorized()


if __name__ == "__main__":
    unittest.main()

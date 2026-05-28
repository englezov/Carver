from __future__ import annotations

import json
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, time, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.continuous import (  # noqa: E402
    ContinuousContractRuleSet,
    ContinuousSeriesRequest,
    build_continuous_back_adjusted_series,
)
from carver.spine.daily_bars import (  # noqa: E402
    CompletedDailyMarketBar,
    DailyDerivationSession,
    derive_completed_daily_from_bound_web_chart,
    derive_completed_daily_from_minute_export,
    derive_completed_daily_from_web_chart,
    normalize_direct_daily_bound_web_chart,
    normalize_direct_daily_web_chart_bar,
)
from carver.spine.m0 import (  # noqa: E402
    BackAdjustmentSpec,
    CompletedBar,
    CostSourceSpec,
    RollRuleSpec,
    SessionCalendarSpec,
    SourceRuleStatus,
    CarverBlocked,
)
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.m3 import (  # noqa: E402
    mes_contract,
    mgc_contract,
    p01_risk_parity,
    p02_all_weather,
    qm_contract,
    zc_contract,
    zf_contract,
    zn_contract,
)
from carver.spine.minute_export import EXPECTED_MINUTE_EXPORT_HEADER, MinuteExportSpec, parse_minute_export_text  # noqa: E402
from carver.spine.portfolio_conformance import (  # noqa: E402
    LockedPortfolioProviderMapping,
    PortfolioProviderMappingSet,
    ProviderMappingStatus,
    portfolio_conformance_from_daily_bars,
    portfolio_web_chart_mapping_status,
    require_locked_provider_mapping_set,
    require_locked_portfolio_web_chart_mapping,
)
from carver.spine.web_chart_api import (  # noqa: E402
    BoundWebChartResponse,
    ChartBarType,
    LockedWebChartSymbol,
    WebChartRequest,
    WebChartSymbol,
    normalize_bound_web_chart_response,
    normalize_bound_web_chart_response_file,
    normalize_web_chart_response,
    normalize_web_chart_response_file,
    web_chart_response_request_binding,
)


class DailyPortfolioConformanceSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.session = DailyDerivationSession(time(13, 30), time(13, 33))
        self.daily_ts = datetime(2026, 5, 28, tzinfo=timezone.utc)

    def epoch_ms(self, hour: int, minute: int) -> int:
        return int(datetime(2026, 5, 28, hour, minute, tzinfo=timezone.utc).timestamp() * 1000)

    def web_request(self) -> WebChartRequest:
        contract = mes_contract()
        es_contract = replace(contract, code="ES", name="E-mini S&P 500 future", multiplier=50)
        locked = LockedWebChartSymbol(es_contract, "06-26", "3570919", "ES JUN26")
        symbol = WebChartSymbol(locked, "3570919", "ES JUN26")
        return WebChartRequest(symbol, ChartBarType.MINUTE, element_size=1, element_count=3)

    def daily_web_request(self) -> WebChartRequest:
        locked = LockedWebChartSymbol(zn_contract(), "06-26", "4470301", "ZN JUN26")
        symbol = WebChartSymbol(locked, "4470301", "ZN JUN26")
        return WebChartRequest(symbol, ChartBarType.DAILY, element_size=1, element_count=1)

    def es_daily_web_request(self) -> WebChartRequest:
        return replace(self.web_request(), bar_type=ChartBarType.DAILY, element_count=1)

    def zn_minute_web_request(self) -> WebChartRequest:
        return replace(self.daily_web_request(), bar_type=ChartBarType.MINUTE, element_count=3)

    def web_payload(self, request: WebChartRequest) -> dict:
        return {
            "request": web_chart_response_request_binding(request),
            "ok": True,
            "body": {
                "items": [
                    {
                        "timestamp": self.epoch_ms(13, 30),
                        "open": 5000,
                        "high": 5002,
                        "low": 4999,
                        "close": 5001,
                        "volume": 10,
                        "complete": True,
                    },
                    {
                        "timestamp": self.epoch_ms(13, 31),
                        "open": 5001,
                        "high": 5004,
                        "low": 5000,
                        "close": 5003,
                        "volume": 20,
                        "complete": True,
                    },
                    {
                        "timestamp": self.epoch_ms(13, 32),
                        "open": 5003,
                        "high": 5005,
                        "low": 5002,
                        "close": 5004,
                        "volume": 30,
                        "complete": True,
                    },
                ]
            },
        }

    def test_quarantined_web_chart_json_normalizes_before_daily_derivation(self) -> None:
        request = self.web_request()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "data" / "quarantine" / "ninjatrader" / "web_chart"
            root.mkdir(parents=True)
            response_path = root / "ES_06-26_getChart_20260528.json"
            response_path.write_text(json.dumps(self.web_payload(request)), encoding="utf-8")

            response = normalize_bound_web_chart_response_file(response_path, request, root)
            daily = derive_completed_daily_from_bound_web_chart(response, self.session)

            self.assertEqual(daily.code, "ES")
            self.assertEqual(daily.timestamp, self.daily_ts)
            self.assertEqual(daily.open, 5000)
            self.assertEqual(daily.high, 5005)
            self.assertEqual(daily.low, 4999)
            self.assertEqual(daily.close, 5004)
            self.assertEqual(daily.volume, 60)

            outside_path = Path(temporary_directory) / "ES_06-26_getChart_20260528.json"
            outside_path.write_text(json.dumps(self.web_payload(request)), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                normalize_web_chart_response_file(outside_path, request, root)
            cache_path = root / "ES_06-26_getChart_20260528.ncd"
            cache_path.write_text(json.dumps(self.web_payload(request)), encoding="utf-8")
            with self.assertRaises(CarverBlocked):
                normalize_web_chart_response_file(cache_path, request, root)

    def test_minute_export_derives_completed_daily_bar_only_for_full_session(self) -> None:
        spec = MinuteExportSpec(mes_contract(), "06-26", session_start=time(13, 30), session_end=time(13, 33))
        text = (
            ",".join(EXPECTED_MINUTE_EXPORT_HEADER)
            + "\n"
            + "MES,06-26,Last,1 Minute,2026-05-28T13:30:00+00:00,5000,5002,4999,5001,10\n"
            + "MES,06-26,Last,1 Minute,2026-05-28T13:31:00+00:00,5001,5004,5000,5003,20\n"
            + "MES,06-26,Last,1 Minute,2026-05-28T13:32:00+00:00,5003,5005,5002,5004,30\n"
        )
        bars = parse_minute_export_text(text, spec)
        daily = derive_completed_daily_from_minute_export(bars, spec)

        self.assertEqual(daily.code, "MES")
        self.assertEqual(daily.timestamp, self.daily_ts)
        self.assertEqual(daily.close, 5004)
        with self.assertRaises(CarverBlocked):
            derive_completed_daily_from_minute_export(bars[:-1], spec)

    def test_direct_daily_web_chart_bar_normalizes_without_minute_derivation(self) -> None:
        request = self.daily_web_request()
        payload = {
            "request": web_chart_response_request_binding(request),
            "ok": True,
            "body": {
                "items": [
                    {
                        "timestamp": int(self.daily_ts.timestamp() * 1000),
                        "open": 119.0,
                        "high": 121.0,
                        "low": 118.0,
                        "close": 120.0,
                        "volume": 1000,
                        "complete": True,
                    }
                ]
            },
        }
        response = normalize_bound_web_chart_response(payload, request)
        daily = normalize_direct_daily_bound_web_chart(response)

        self.assertEqual(daily.code, "ZN")
        self.assertEqual(daily.contract, zn_contract())
        self.assertEqual(daily.timestamp, self.daily_ts)
        self.assertEqual(daily.close, 120.0)
        with self.assertRaises(CarverBlocked):
            normalize_direct_daily_web_chart_bar(response.bars[0], request)
        with self.assertRaises(CarverBlocked):
            normalize_direct_daily_bound_web_chart(
                normalize_bound_web_chart_response(payload, replace(request, bar_type=ChartBarType.MINUTE))
            )

    def test_direct_daily_bound_web_chart_rejects_cross_request_replay(self) -> None:
        request = self.daily_web_request()
        payload = {
            "request": web_chart_response_request_binding(request),
            "ok": True,
            "body": {
                "items": [
                    {
                        "timestamp": int(self.daily_ts.timestamp() * 1000),
                        "open": 119.0,
                        "high": 121.0,
                        "low": 118.0,
                        "close": 120.0,
                        "volume": 1000,
                        "complete": True,
                    }
                ]
            },
        }
        response = normalize_bound_web_chart_response(payload, request)
        spoofed_response = BoundWebChartResponse(self.es_daily_web_request(), response.bars)

        with self.assertRaises(CarverBlocked):
            normalize_direct_daily_bound_web_chart(spoofed_response)

    def test_minute_bound_web_chart_daily_derivation_rejects_cross_request_replay(self) -> None:
        request = self.web_request()
        response = normalize_bound_web_chart_response(self.web_payload(request), request)
        spoofed_response = BoundWebChartResponse(self.zn_minute_web_request(), response.bars)

        with self.assertRaises(CarverBlocked):
            derive_completed_daily_from_bound_web_chart(spoofed_response, self.session)

    def test_daily_derivation_rejects_gaps_wrong_alignment_and_incomplete_web_bars(self) -> None:
        request = self.web_request()
        response = normalize_bound_web_chart_response(self.web_payload(request), request)
        with self.assertRaises(CarverBlocked):
            derive_completed_daily_from_bound_web_chart(response, DailyDerivationSession(time(13, 31), time(13, 34)))

        bad_payload = self.web_payload(request)
        bad_payload["body"]["items"][1]["timestamp"] = self.epoch_ms(13, 32)
        with self.assertRaises(CarverBlocked):
            normalize_web_chart_response(bad_payload, request)

        incomplete_payload = self.web_payload(request)
        incomplete_payload["body"]["items"][0]["complete"] = False
        with self.assertRaises(CarverBlocked):
            normalize_web_chart_response(incomplete_payload, request)

    def daily_bar(self, contract, close: float) -> CompletedDailyMarketBar:
        return CompletedDailyMarketBar(
            completed_bar=CompletedBar(self.daily_ts),
            contract=contract,
            contract_month="06-26",
            open=close - 1,
            high=close + 1,
            low=close - 2,
            close=close,
            volume=100,
        )

    def test_p01_and_p02_conformance_use_completed_daily_closes(self) -> None:
        p01 = p01_risk_parity(capital=1_000_000, target_risk=0.20, idm=1.0)
        p01_bars = {
            "MES": self.daily_bar(mes_contract(), 5000),
            "ZN": self.daily_bar(zn_contract(), 120),
        }
        p01_result = portfolio_conformance_from_daily_bars(
            p01,
            p01_bars,
            {"MES": TimedValue(0.20, self.daily_ts), "ZN": TimedValue(0.10, self.daily_ts)},
            {"MES": TimedValue(1.0, self.daily_ts), "ZN": TimedValue(1.0, self.daily_ts)},
        )
        self.assertAlmostEqual(p01_result["MES"].unrounded_contracts, 20.0)
        self.assertAlmostEqual(p01_result["ZN"].unrounded_contracts, 8.333333333333334)

        p02 = p02_all_weather(capital=1_000_000, target_risk=0.20, idm=1.0)
        p02_bars = {
            "MES": self.daily_bar(mes_contract(), 5000),
            "ZN": self.daily_bar(zn_contract(), 120),
            "ZF": self.daily_bar(zf_contract(), 110),
            "QM": self.daily_bar(qm_contract(), 80),
            "ZC": self.daily_bar(zc_contract(), 500),
            "MGC": self.daily_bar(mgc_contract(), 2000),
        }
        result = portfolio_conformance_from_daily_bars(
            p02,
            p02_bars,
            {code: TimedValue(risk, self.daily_ts) for code, risk in {
                "MES": 0.20,
                "ZN": 0.10,
                "ZF": 0.08,
                "QM": 0.30,
                "ZC": 0.25,
                "MGC": 0.18,
            }.items()},
            {code: TimedValue(1.0, self.daily_ts) for code in p02_bars},
        )
        self.assertEqual(set(result), {"MES", "ZN", "ZF", "QM", "ZC", "MGC"})

        with self.assertRaises(CarverBlocked):
            portfolio_conformance_from_daily_bars(p01, {"MES": p01_bars["MES"]}, {}, {})
        with self.assertRaises(CarverBlocked):
            portfolio_conformance_from_daily_bars(
                p01,
                p01_bars,
                {"MES": TimedValue(0.20, self.daily_ts), "ZN": TimedValue(0.10, datetime(2026, 5, 27, tzinfo=timezone.utc))},
                {"MES": TimedValue(1.0, self.daily_ts), "ZN": TimedValue(1.0, self.daily_ts)},
            )

    def test_p01_p02_web_chart_mapping_status_fails_closed_until_exact_contracts_are_locked(self) -> None:
        p01_rows = portfolio_web_chart_mapping_status(p01_risk_parity(1_000_000, 0.20, 1.0), {"MES": "06-26", "ZN": "06-26"})
        self.assertEqual([(row.contract_code, row.status) for row in p01_rows], [("MES", ProviderMappingStatus.UNRESOLVED), ("ZN", ProviderMappingStatus.LOCKED)])
        with self.assertRaises(CarverBlocked):
            require_locked_portfolio_web_chart_mapping(p01_rows)

        p02 = p02_all_weather(1_000_000, 0.20, 1.0)
        p02_rows = portfolio_web_chart_mapping_status(
            p02,
            {"MES": "06-26", "ZN": "06-26", "ZF": "06-26", "QM": "06-26", "ZC": "06-26", "MGC": "06-26"},
        )
        self.assertEqual([row.contract_code for row in p02_rows], ["MES", "ZN", "ZF", "QM", "ZC", "MGC"])
        self.assertEqual(sum(row.status is ProviderMappingStatus.LOCKED for row in p02_rows), 1)

    def test_locked_provider_mapping_set_requires_exact_portfolio_legs(self) -> None:
        zn_mapping = LockedPortfolioProviderMapping(zn_contract(), "06-26", "ZN JUN26", "4470301")
        p01 = p01_risk_parity(1_000_000, 0.20, 1.0)

        with self.assertRaises(CarverBlocked):
            require_locked_provider_mapping_set(PortfolioProviderMappingSet(p01, (zn_mapping,)))
        with self.assertRaises(CarverBlocked):
            LockedPortfolioProviderMapping(mes_contract(), "06-26", "ES JUN26", "3570919").validate()
        with self.assertRaises(CarverBlocked):
            LockedPortfolioProviderMapping(mes_contract(), "06-26", "MES JUN26", "3570919").validate()
        with self.assertRaises(CarverBlocked):
            LockedPortfolioProviderMapping(zn_contract(), "06-26", "ZN JUN26", "999999").validate()

        zn_only = PortfolioProviderMappingSet(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            (
                LockedPortfolioProviderMapping(mes_contract(), "06-26", "MES JUN26", "3570919"),
                zn_mapping,
            ),
        )
        with self.assertRaises(CarverBlocked):
            zn_only.validate()

    def test_continuous_roll_and_back_adjustment_gate_fails_closed(self) -> None:
        unresolved_rules = ContinuousContractRuleSet(
            session_calendar=SessionCalendarSpec("session calendar"),
            roll_rule=RollRuleSpec("roll rule"),
            back_adjustment=BackAdjustmentSpec("back adjustment"),
            cost_source=CostSourceSpec("costs"),
        )
        request = ContinuousSeriesRequest(unresolved_rules, (self.daily_bar(mes_contract(), 5000),))
        with self.assertRaises(CarverBlocked):
            build_continuous_back_adjusted_series(request)

        locked_rules = ContinuousContractRuleSet(
            session_calendar=SessionCalendarSpec("session calendar", SourceRuleStatus.LOCKED, "UTC"),
            roll_rule=RollRuleSpec("roll rule", SourceRuleStatus.LOCKED),
            back_adjustment=BackAdjustmentSpec("back adjustment", SourceRuleStatus.LOCKED),
            cost_source=CostSourceSpec("costs", SourceRuleStatus.LOCKED, "config/costs.json"),
        )
        with self.assertRaises(CarverBlocked):
            build_continuous_back_adjusted_series(ContinuousSeriesRequest(locked_rules, (self.daily_bar(mes_contract(), 5000),)))


if __name__ == "__main__":
    unittest.main()

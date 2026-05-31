from __future__ import annotations

import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked  # noqa: E402
from carver.spine.s09_zn_package import S09_ZN_REQUIRED_DAILY_BARS  # noqa: E402
from carver.spine.tradovate_api_probe import (  # noqa: E402
    AUTHORIZED_TRADOVATE_ENDPOINTS,
    AUTHORIZED_TRADOVATE_QUARANTINE_ROOT,
    DEFAULT_TRADOVATE_MD_WS_URL,
    SINGLE_PROBE_SENTINEL_NAME,
    TradovateCredentialBundle,
    _authorized_quarantine_root,
    _build_quarantine_payload,
    _claim_single_probe,
    _decode_frame,
    _require_single_probe_not_consumed,
    _read_local_probe_env,
    _send_ws_request,
    build_s09_zn_tradovate_probe_config,
    load_tradovate_credentials,
    run_s09_zn_tradovate_api_probe,
)
import carver.spine.tradovate_api_probe as tradovate_probe  # noqa: E402
from carver.spine.web_chart_api import ChartBarType, normalize_bound_web_chart_response  # noqa: E402


class TradovateApiProbeSyntheticTests(unittest.TestCase):
    def credentials(self) -> TradovateCredentialBundle:
        return TradovateCredentialBundle("synthetic-md-token", DEFAULT_TRADOVATE_MD_WS_URL)

    def test_builds_exact_s09_zn_direct_daily_api_probe_config(self) -> None:
        config = build_s09_zn_tradovate_probe_config(self.credentials())
        payload = config.request.payload()

        self.assertEqual(config.credentials.websocket_url, DEFAULT_TRADOVATE_MD_WS_URL)
        self.assertEqual(payload["symbol"], "4470301")
        self.assertEqual(payload["chartDescription"]["underlyingType"], "DailyBar")
        self.assertEqual(payload["chartDescription"]["elementSize"], 1)
        self.assertEqual(payload["timeRange"]["asMuchAsElements"], 257)
        self.assertEqual(config.request.element_count, S09_ZN_REQUIRED_DAILY_BARS)

    def test_probe_config_rejects_wrong_symbol_bar_type_or_count(self) -> None:
        config = build_s09_zn_tradovate_probe_config(self.credentials())
        with self.assertRaises(CarverBlocked):
            replace(config, request=replace(config.request, element_count=258)).validate()

        minute_request = replace(config.request, bar_type=ChartBarType.MINUTE)
        with self.assertRaises(CarverBlocked):
            replace(config, request=minute_request).validate()

        bad_credentials = TradovateCredentialBundle("synthetic-md-token", "wss://example.com/v1/websocket")
        with self.assertRaises(CarverBlocked):
            build_s09_zn_tradovate_probe_config(bad_credentials)
        with self.assertRaises(CarverBlocked):
            build_s09_zn_tradovate_probe_config(self.credentials(), Path("tmp/not-the-quarantine"))

    def test_probe_execution_fails_closed_when_optional_websocket_client_is_missing(self) -> None:
        if tradovate_probe.connect is not None:
            self.skipTest("optional websockets package is installed")
        config = build_s09_zn_tradovate_probe_config(self.credentials())
        with self.assertRaises(CarverBlocked):
            run_s09_zn_tradovate_api_probe(config)

    def test_only_authorized_tradovate_probe_endpoints_can_be_framed(self) -> None:
        sent: list[str] = []

        _send_ws_request(sent.append, "authorize", 1, "token-value")
        _send_ws_request(sent.append, "md/getChart", 2, {"symbol": "4470301"})
        _send_ws_request(sent.append, "md/cancelChart", 3, {"subscriptionId": 10})

        self.assertEqual(AUTHORIZED_TRADOVATE_ENDPOINTS, frozenset({"authorize", "md/getChart", "md/cancelChart"}))
        self.assertEqual(sent[0], "authorize\n1\n\ntoken-value")
        self.assertEqual(sent[1], 'md/getChart\n2\n\n{"symbol":"4470301"}')
        self.assertEqual(sent[2], 'md/cancelChart\n3\n\n{"subscriptionId":10}')
        with self.assertRaises(CarverBlocked):
            _send_ws_request(sent.append, "order/placeorder", 4, {})
        with self.assertRaises(CarverBlocked):
            _send_ws_request(sent.append, "account/list", 5, {})

    def test_tradovate_frame_decode_rejects_close_or_bad_shapes(self) -> None:
        self.assertEqual(_decode_frame("h"), [])
        self.assertEqual(_decode_frame('a[{"s":200,"i":1}]'), [{"s": 200, "i": 1}])
        for frame in ("c[1000]", "bad", "a{}", "a[1]"):
            with self.subTest(frame=frame):
                with self.assertRaises(CarverBlocked):
                    _decode_frame(frame)

    def test_local_credentials_are_loaded_only_from_ignored_runtime_file(self) -> None:
        env_file = ROOT / "runtime" / "tradovate_api_probe.env"
        env_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            env_file.write_text("CARVER_TRADOVATE_MD_ACCESS_TOKEN='secret-token'\n", encoding="utf-8")
            values = _read_local_probe_env(Path("runtime/tradovate_api_probe.env"))
            bundle = load_tradovate_credentials({}, Path("runtime/tradovate_api_probe.env"))
        finally:
            env_file.unlink(missing_ok=True)

        self.assertEqual(values["CARVER_TRADOVATE_MD_ACCESS_TOKEN"], "secret-token")
        self.assertEqual(bundle.md_access_token, "secret-token")
        self.assertEqual(bundle.websocket_url, DEFAULT_TRADOVATE_MD_WS_URL)
        with self.assertRaises(CarverBlocked):
            _read_local_probe_env(ROOT / "not-runtime.env")

    def test_single_probe_sentinel_and_quarantine_root_are_hard_boundaries(self) -> None:
        self.assertEqual(
            _authorized_quarantine_root(Path("data/quarantine/ninjatrader/web_chart")),
            AUTHORIZED_TRADOVATE_QUARANTINE_ROOT.resolve(),
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _require_single_probe_not_consumed(root)
            sentinel = _claim_single_probe(root)
            self.assertEqual(sentinel.name, SINGLE_PROBE_SENTINEL_NAME)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "STARTED")
            with self.assertRaises(CarverBlocked):
                _require_single_probe_not_consumed(root)
            with self.assertRaises(CarverBlocked):
                _claim_single_probe(root)

    def test_quarantine_payload_normalizes_official_daily_chart_bars_for_existing_validator(self) -> None:
        request = build_s09_zn_tradovate_probe_config(self.credentials()).request
        first = datetime(2025, 1, 1, tzinfo=timezone.utc)
        raw_bars = []
        for index in range(S09_ZN_REQUIRED_DAILY_BARS):
            timestamp = first + timedelta(days=index)
            raw_bars.append(
                {
                    "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                    "open": 110.0 + index * 0.01,
                    "high": 111.0 + index * 0.01,
                    "low": 109.0 + index * 0.01,
                    "close": 110.5 + index * 0.01,
                    "upVolume": 100,
                    "downVolume": 50,
                }
            )

        payload = _build_quarantine_payload(request, raw_bars, [{"s": 200, "i": 2}], 10, 11)
        response = normalize_bound_web_chart_response(payload, request)

        self.assertEqual(len(response.bars), S09_ZN_REQUIRED_DAILY_BARS)
        self.assertEqual(response.bars[0].timestamp, first)
        self.assertEqual(response.bars[-1].volume, 150.0)
        self.assertEqual(payload["request"]["identity"]["contractCode"], "ZN")
        self.assertEqual(payload["raw"]["source"], "tradovate_market_data_websocket")


if __name__ == "__main__":
    unittest.main()

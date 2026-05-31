from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Any, Callable

try:
    from websockets.sync.client import connect
except ModuleNotFoundError:  # pragma: no cover - exercised when optional dependency is absent
    connect = None

from .m0 import CarverBlocked
from .s09_zn_package import S09_ZN_REQUIRED_DAILY_BARS, build_s09_zn_package
from .web_chart_api import DEFAULT_WEB_CHART_QUARANTINE, WebChartRequest, web_chart_response_request_binding


AUTHORIZED_TRADOVATE_ENDPOINTS = frozenset({"authorize", "md/getChart", "md/cancelChart"})
DEFAULT_TRADOVATE_MD_WS_URL = "wss://md.tradovateapi.com/v1/websocket"
LOCAL_PROBE_ENV_FILE = Path("runtime/tradovate_api_probe.env")
CARVER_WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
AUTHORIZED_TRADOVATE_QUARANTINE_ROOT = CARVER_WORKSPACE_ROOT / DEFAULT_WEB_CHART_QUARANTINE
SINGLE_PROBE_SENTINEL_NAME = "ZN_06-26_DailyBar_257_getChart.SINGLE_PROBE_COMPLETED"


@dataclass(frozen=True)
class TradovateCredentialBundle:
    md_access_token: str
    websocket_url: str = DEFAULT_TRADOVATE_MD_WS_URL

    def validate(self) -> None:
        if not isinstance(self.md_access_token, str) or not self.md_access_token.strip():
            raise CarverBlocked("Tradovate market-data access token is missing")
        if "\n" in self.md_access_token or "\r" in self.md_access_token:
            raise CarverBlocked("Tradovate market-data access token is malformed")
        if self.websocket_url != DEFAULT_TRADOVATE_MD_WS_URL:
            raise CarverBlocked("Tradovate websocket URL is not allow-listed")


@dataclass(frozen=True)
class TradovateProbeConfig:
    request: WebChartRequest
    credentials: TradovateCredentialBundle
    quarantine_root: Path = AUTHORIZED_TRADOVATE_QUARANTINE_ROOT

    def validate(self) -> None:
        self.request.validate()
        self.credentials.validate()
        payload = self.request.payload()
        if payload["symbol"] != "4470301":
            raise CarverBlocked("Tradovate API probe is locked to ZN provider symbol 4470301")
        if payload["chartDescription"]["underlyingType"] != "DailyBar":
            raise CarverBlocked("Tradovate API probe is locked to DailyBar")
        if payload["chartDescription"]["elementSize"] != 1:
            raise CarverBlocked("Tradovate API probe is locked to daily element size 1")
        if payload["timeRange"]["asMuchAsElements"] != S09_ZN_REQUIRED_DAILY_BARS:
            raise CarverBlocked("Tradovate API probe is locked to 257 daily bars")
        if _authorized_quarantine_root(self.quarantine_root) != AUTHORIZED_TRADOVATE_QUARANTINE_ROOT.resolve():
            raise CarverBlocked("Tradovate API probe output must stay in the locked Carver web-chart quarantine")


@dataclass(frozen=True)
class TradovateProbeResult:
    output_path: Path
    bar_count: int
    historical_id: int | None
    realtime_id: int | None


def build_s09_zn_tradovate_probe_config(
    credentials: TradovateCredentialBundle,
    quarantine_root: Path = AUTHORIZED_TRADOVATE_QUARANTINE_ROOT,
) -> TradovateProbeConfig:
    package = build_s09_zn_package()
    config = TradovateProbeConfig(package.probe_plan.request, credentials, quarantine_root)
    config.validate()
    return config


def load_tradovate_credentials(
    environ: dict[str, str] | None = None,
    env_file: Path = LOCAL_PROBE_ENV_FILE,
) -> TradovateCredentialBundle:
    env = dict(environ or os.environ)
    if env_file.exists():
        env.update(_read_local_probe_env(env_file))
    md_token = env.get("CARVER_TRADOVATE_MD_ACCESS_TOKEN")
    if md_token:
        return TradovateCredentialBundle(
            md_access_token=md_token,
            websocket_url=DEFAULT_TRADOVATE_MD_WS_URL,
        )
    raise CarverBlocked(
        "Tradovate credentials are missing; set CARVER_TRADOVATE_MD_ACCESS_TOKEN or a local runtime/tradovate_api_probe.env"
    )


def run_s09_zn_tradovate_api_probe(config: TradovateProbeConfig) -> TradovateProbeResult:
    config.validate()
    if connect is None:
        raise CarverBlocked("Tradovate API probe requires the optional websockets package")
    root = _authorized_quarantine_root(config.quarantine_root)
    root.mkdir(parents=True, exist_ok=True)
    sentinel_path = _claim_single_probe(root)
    output_path = _next_output_path(root)
    request_payload = config.request.payload()
    raw_messages: list[dict[str, Any]] = []
    bars: list[dict[str, Any]] = []
    historical_id: int | None = None
    realtime_id: int | None = None
    chart_ids: set[int] = set()
    cancel_errors: list[str] = []

    with connect(config.credentials.websocket_url, open_timeout=30, close_timeout=10) as websocket:
        recv = lambda: _safe_recv(websocket)
        try:
            _wait_open(recv)
            _send_ws_request(websocket.send, "authorize", 1, config.credentials.md_access_token)
            auth_response = _wait_response(recv, 1, raw_messages)
            _require_status_ok(auth_response, "Tradovate authorize")

            _send_ws_request(websocket.send, "md/getChart", 2, request_payload)
            chart_response = _wait_response(recv, 2, raw_messages)
            _require_status_ok(chart_response, "Tradovate md/getChart")
            response_body = chart_response.get("d")
            if not isinstance(response_body, dict):
                raise CarverBlocked("Tradovate chart response is missing subscription ids")
            historical_id = _optional_int(response_body.get("historicalId"))
            realtime_id = _optional_int(response_body.get("realtimeId"))
            chart_ids = {value for value in (historical_id, realtime_id) if value is not None}
            if not chart_ids:
                raise CarverBlocked("Tradovate chart response did not include chart subscription ids")

            bars = _collect_chart_bars(recv, raw_messages, chart_ids, config.request.element_count)
        finally:
            for request_id, subscription_id in enumerate(sorted(chart_ids), start=3):
                try:
                    _send_ws_request(websocket.send, "md/cancelChart", request_id, {"subscriptionId": subscription_id})
                    cancel_response = _wait_response(recv, request_id, raw_messages, timeout_messages=20)
                    _require_status_ok(cancel_response, "Tradovate md/cancelChart")
                except CarverBlocked as exc:
                    cancel_errors.append(str(exc))

    if cancel_errors:
        raise CarverBlocked("Tradovate md/cancelChart did not confirm for every chart subscription")

    payload = _build_quarantine_payload(config.request, bars, raw_messages, historical_id, realtime_id)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    sentinel_path.write_text(f"COMPLETED {output_path.name}", encoding="utf-8")
    return TradovateProbeResult(
        output_path=output_path,
        bar_count=len(payload["body"]["items"]),
        historical_id=historical_id,
        realtime_id=realtime_id,
    )


def main() -> int:
    try:
        credentials = load_tradovate_credentials()
        config = build_s09_zn_tradovate_probe_config(credentials)
        result = run_s09_zn_tradovate_api_probe(config)
    except CarverBlocked as exc:
        print(f"CARVER_S09_ZN_DIRECT_DAILY_API_PROBE_BLOCKED {exc}", file=sys.stderr)
        return 2
    print(f"CARVER_S09_ZN_DIRECT_DAILY_API_PROBE_CAPTURED {result.bar_count} {result.output_path}")
    return 0


def _read_local_probe_env(path: Path) -> dict[str, str]:
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("local Tradovate credential file does not exist") from exc
    runtime_root = (CARVER_WORKSPACE_ROOT / "runtime").resolve()
    try:
        resolved.relative_to(runtime_root)
    except ValueError as exc:
        raise CarverBlocked("local Tradovate credential file must stay under ignored runtime/") from exc
    values: dict[str, str] = {}
    for raw_line in resolved.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise CarverBlocked("local Tradovate credential file contains an invalid line")
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values

def _authorized_quarantine_root(root: Path) -> Path:
    candidate = Path(root)
    if not candidate.is_absolute():
        candidate = CARVER_WORKSPACE_ROOT / candidate
    return candidate.resolve()


def _single_probe_sentinel(root: Path) -> Path:
    return root / SINGLE_PROBE_SENTINEL_NAME


def _claim_single_probe(root: Path) -> Path:
    if _single_probe_sentinel(root).exists():
        raise CarverBlocked("S09 ZN direct-daily API probe has already been consumed")
    if any(root.glob("ZN_06-26_DailyBar_257_getChart_*.json")):
        raise CarverBlocked("S09 ZN direct-daily API probe output already exists")
    try:
        with _single_probe_sentinel(root).open("x", encoding="utf-8") as sentinel:
            sentinel.write("STARTED")
    except FileExistsError as exc:
        raise CarverBlocked("S09 ZN direct-daily API probe has already been claimed") from exc

    return _single_probe_sentinel(root)


def _require_single_probe_not_consumed(root: Path) -> None:
    if _single_probe_sentinel(root).exists():
        raise CarverBlocked("S09 ZN direct-daily API probe has already been consumed")
    if any(root.glob("ZN_06-26_DailyBar_257_getChart_*.json")):
        raise CarverBlocked("S09 ZN direct-daily API probe output already exists")


def _send_ws_request(send: Callable[[str], None], endpoint: str, request_id: int, body: str | dict[str, Any]) -> None:
    if endpoint not in AUTHORIZED_TRADOVATE_ENDPOINTS:
        raise CarverBlocked("Tradovate API probe endpoint is not authorized")
    if not isinstance(request_id, int) or request_id <= 0:
        raise CarverBlocked("Tradovate API probe request id must be positive")
    if isinstance(body, str):
        body_text = body
    else:
        body_text = json.dumps(body, separators=(",", ":"))
    send(f"{endpoint}\n{request_id}\n\n{body_text}")


def _wait_open(recv: Callable[[], str]) -> None:
    frame = recv()
    if frame != "o":
        raise CarverBlocked("Tradovate websocket did not open with expected frame")


def _safe_recv(websocket: Any) -> str:
    try:
        frame = websocket.recv(timeout=30)
    except TimeoutError as exc:
        raise CarverBlocked("Tradovate websocket receive timed out") from exc
    if not isinstance(frame, str):
        raise CarverBlocked("Tradovate websocket frame must be text")
    return frame


def _wait_response(
    recv: Callable[[], str],
    request_id: int,
    raw_messages: list[dict[str, Any]],
    timeout_messages: int = 200,
) -> dict[str, Any]:
    for _ in range(timeout_messages):
        for message in _decode_frame(recv()):
            raw_messages.append(message)
            if message.get("i") == request_id and "s" in message:
                return message
    raise CarverBlocked("Tradovate websocket response timed out")


def _collect_chart_bars(
    recv: Callable[[], str],
    raw_messages: list[dict[str, Any]],
    chart_ids: set[int],
    required_count: int,
) -> list[dict[str, Any]]:
    collected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for _ in range(1000):
        for message in _decode_frame(recv()):
            raw_messages.append(message)
            if message.get("e") != "chart":
                continue
            data = message.get("d")
            if not isinstance(data, dict):
                continue
            charts = data.get("charts")
            if not isinstance(charts, list):
                continue
            for chart in charts:
                if not isinstance(chart, dict) or chart.get("id") not in chart_ids:
                    continue
                raw_bars = chart.get("bars")
                if not isinstance(raw_bars, list):
                    continue
                for raw_bar in raw_bars:
                    if not isinstance(raw_bar, dict):
                        raise CarverBlocked("Tradovate chart bar must be an object")
                    timestamp = _bar_timestamp(raw_bar)
                    if timestamp in seen:
                        continue
                    seen.add(timestamp)
                    collected.append(raw_bar)
        if len(collected) >= required_count:
            break
    if len(collected) < required_count:
        raise CarverBlocked("Tradovate chart response did not contain 257 daily bars")
    return sorted(collected, key=_bar_timestamp)[-required_count:]


def _decode_frame(frame: str) -> list[dict[str, Any]]:
    if frame == "h":
        return []
    if frame.startswith("c"):
        raise CarverBlocked("Tradovate websocket closed before probe completed")
    if not frame.startswith("a"):
        raise CarverBlocked("Tradovate websocket sent an unexpected frame")
    try:
        messages = json.loads(frame[1:])
    except json.JSONDecodeError as exc:
        raise CarverBlocked("Tradovate websocket frame is not valid JSON") from exc
    if not isinstance(messages, list):
        raise CarverBlocked("Tradovate websocket frame payload must be a list")
    for message in messages:
        if not isinstance(message, dict):
            raise CarverBlocked("Tradovate websocket message must be an object")
    return messages


def _require_status_ok(message: dict[str, Any], operation: str) -> None:
    if message.get("s") != 200:
        raise CarverBlocked(f"{operation} failed")


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise CarverBlocked("Tradovate chart subscription id must be an integer")
    return value


def _build_quarantine_payload(
    request: WebChartRequest,
    raw_bars: list[dict[str, Any]],
    raw_messages: list[dict[str, Any]],
    historical_id: int | None,
    realtime_id: int | None,
) -> dict[str, Any]:
    items = [_normalize_tradovate_bar(raw_bar) for raw_bar in raw_bars]
    items.sort(key=lambda item: item["timestamp"])
    if len(items) != request.element_count:
        raise CarverBlocked("Tradovate quarantine payload does not contain the requested bar count")
    return {
        "request": web_chart_response_request_binding(request),
        "ok": True,
        "body": {
            "historicalId": historical_id,
            "realtimeId": realtime_id,
            "items": items,
        },
        "raw": {
            "source": "tradovate_market_data_websocket",
            "messages": raw_messages,
        },
    }


def _normalize_tradovate_bar(raw_bar: dict[str, Any]) -> dict[str, Any]:
    timestamp = _parse_tradovate_timestamp(_bar_timestamp(raw_bar))
    if timestamp.date() >= datetime.now(timezone.utc).date():
        raise CarverBlocked("Tradovate daily bar is not proven complete")
    return {
        "timestamp": int(timestamp.timestamp() * 1000),
        "open": _require_number(raw_bar.get("open"), "open"),
        "high": _require_number(raw_bar.get("high"), "high"),
        "low": _require_number(raw_bar.get("low"), "low"),
        "close": _require_number(raw_bar.get("close"), "close"),
        "volume": _volume(raw_bar),
        "complete": True,
    }


def _bar_timestamp(raw_bar: dict[str, Any]) -> str:
    value = raw_bar.get("timestamp")
    if not isinstance(value, str) or not value:
        raise CarverBlocked("Tradovate chart bar timestamp is missing")
    return value


def _parse_tradovate_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CarverBlocked("Tradovate chart bar timestamp is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CarverBlocked("Tradovate chart bar timestamp must be timezone-aware")
    parsed = parsed.astimezone(timezone.utc)
    if parsed.hour or parsed.minute or parsed.second or parsed.microsecond:
        raise CarverBlocked("Tradovate DailyBar timestamp must be date-aligned")
    return parsed


def _require_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CarverBlocked(f"Tradovate chart bar {name} must be numeric")
    result = float(value)
    if result <= 0:
        raise CarverBlocked(f"Tradovate chart bar {name} must be positive")
    return result


def _volume(raw_bar: dict[str, Any]) -> float:
    if "volume" in raw_bar:
        value = raw_bar["volume"]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise CarverBlocked("Tradovate chart bar volume must be non-negative")
        return float(value)
    up = raw_bar.get("upVolume", 0)
    down = raw_bar.get("downVolume", 0)
    if isinstance(up, bool) or isinstance(down, bool) or not isinstance(up, (int, float)) or not isinstance(down, (int, float)):
        raise CarverBlocked("Tradovate chart bar volume fields must be numeric")
    if up < 0 or down < 0:
        raise CarverBlocked("Tradovate chart bar volume fields must be non-negative")
    return float(up) + float(down)


def _next_output_path(root: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return root / f"ZN_06-26_DailyBar_257_getChart_{stamp}.json"


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
import json
from math import isfinite
from numbers import Real
from pathlib import Path
from typing import Any

from .m0 import ContractSpec, LaneClass, CarverBlocked, require_finite_positive, require_source_native


ALLOWED_CHART_ENDPOINTS = frozenset({"md/getChart", "md/cancelChart"})
MAX_SYNTHETIC_CHART_ELEMENTS = 500
DEFAULT_WEB_CHART_QUARANTINE = Path("data/quarantine/ninjatrader/web_chart")
LOCKED_WEB_CHART_PROVIDER_SYMBOLS = {
    ("ES", "06-26", "ES JUN26"): "3570919",
    ("ZN", "06-26", "ZN JUN26"): "4470301",
}


class ChartBarType(StrEnum):
    MINUTE = "MinuteBar"
    DAILY = "DailyBar"


@dataclass(frozen=True)
class LockedWebChartSymbol:
    contract: ContractSpec
    contract_month: str
    provider_symbol_id: str
    display_symbol: str
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    def validate(self) -> None:
        require_source_native(self.lane_class)
        self.contract.validate()
        if not isinstance(self.provider_symbol_id, str) or not self.provider_symbol_id.isdigit():
            raise CarverBlocked("web chart provider symbol id must be a numeric string")
        expected_display = f"{self.contract.code} {_display_contract_month(self.contract_month)}"
        if self.display_symbol != expected_display:
            raise CarverBlocked("web chart display symbol does not match source-native contract month")
        _require_contract_month(self.contract_month)
        locked_id = LOCKED_WEB_CHART_PROVIDER_SYMBOLS.get((self.contract.code, self.contract_month, self.display_symbol))
        if locked_id is None or self.provider_symbol_id != locked_id:
            raise CarverBlocked("web chart symbol is not in the locked provider mapping")


@dataclass(frozen=True)
class WebChartSymbol:
    locked: LockedWebChartSymbol
    provider_symbol_id: str
    display_symbol: str
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    @property
    def contract(self) -> ContractSpec:
        return self.locked.contract

    @property
    def contract_month(self) -> str:
        return self.locked.contract_month

    def validate(self) -> None:
        require_source_native(self.lane_class)
        self.locked.validate()
        if self.provider_symbol_id != self.locked.provider_symbol_id:
            raise CarverBlocked("web chart provider symbol id does not match locked mapping")
        if self.display_symbol != self.locked.display_symbol:
            raise CarverBlocked("web chart display symbol does not match locked mapping")


@dataclass(frozen=True)
class WebChartRequest:
    symbol: WebChartSymbol
    bar_type: ChartBarType
    element_size: int
    element_count: int
    endpoint: str = "md/getChart"
    element_size_unit: str = "UnderlyingUnits"
    with_histogram: bool = False

    def validate(self) -> None:
        if self.endpoint not in ALLOWED_CHART_ENDPOINTS:
            raise CarverBlocked("web chart endpoint is not allow-listed")
        if self.endpoint != "md/getChart":
            raise CarverBlocked("only md/getChart request normalization is authorized")
        if not isinstance(self.bar_type, ChartBarType):
            raise CarverBlocked("web chart bar type must be a locked ChartBarType")
        self.symbol.validate()
        if self.element_size_unit != "UnderlyingUnits":
            raise CarverBlocked("web chart element size unit must be UnderlyingUnits")
        if self.with_histogram:
            raise CarverBlocked("web chart histogram requests are not authorized")
        _require_positive_int("web chart element size", self.element_size)
        _require_positive_int("web chart element count", self.element_count)
        if self.element_count > MAX_SYNTHETIC_CHART_ELEMENTS:
            raise CarverBlocked("web chart element count exceeds synthetic gate maximum")
        if self.bar_type is ChartBarType.DAILY and self.element_size != 1:
            raise CarverBlocked("daily web chart requests must use element size 1")

    def payload(self) -> dict[str, Any]:
        self.validate()
        return {
            "symbol": self.symbol.locked.provider_symbol_id,
            "chartDescription": {
                "underlyingType": self.bar_type.value,
                "elementSizeUnit": self.element_size_unit,
                "elementSize": self.element_size,
                "withHistogram": self.with_histogram,
            },
            "timeRange": {"asMuchAsElements": self.element_count},
        }


@dataclass(frozen=True)
class WebChartBar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    complete: bool

    def validate(self, request: WebChartRequest) -> None:
        request.validate()
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise CarverBlocked("web chart bar timestamp must be timezone-aware")
        if request.bar_type is ChartBarType.MINUTE and (self.timestamp.second or self.timestamp.microsecond):
            raise CarverBlocked("minute web chart timestamp must be minute-aligned")
        if request.bar_type is ChartBarType.DAILY and (
            self.timestamp.hour or self.timestamp.minute or self.timestamp.second or self.timestamp.microsecond
        ):
            raise CarverBlocked("daily web chart timestamp must be date-aligned")
        require_finite_positive("web chart open", self.open)
        require_finite_positive("web chart high", self.high)
        require_finite_positive("web chart low", self.low)
        require_finite_positive("web chart close", self.close)
        _require_finite_non_negative("web chart volume", self.volume)
        if self.high < max(self.open, self.low, self.close):
            raise CarverBlocked("web chart high is inconsistent with OHLC")
        if self.low > min(self.open, self.high, self.close):
            raise CarverBlocked("web chart low is inconsistent with OHLC")
        if not self.complete:
            raise CarverBlocked("web chart bar is not complete")


@dataclass(frozen=True)
class WebChartProbePlan:
    request: WebChartRequest
    execution_authorized: bool = False

    def require_authorized(self) -> None:
        self.request.validate()
        if not self.execution_authorized:
            raise CarverBlocked("real web chart probe execution is not authorized")


def normalize_web_chart_response(payload: dict[str, Any], request: WebChartRequest) -> tuple[WebChartBar, ...]:
    request.validate()
    if not isinstance(payload, dict):
        raise CarverBlocked("web chart response must be an object")
    _require_response_request_binding(payload, request)
    if not payload.get("ok", False):
        raise CarverBlocked("web chart response is not ok")
    body = payload.get("body")
    if not isinstance(body, dict):
        raise CarverBlocked("web chart response body is missing")
    raw_bars = body.get("items")
    if not isinstance(raw_bars, list):
        raise CarverBlocked("web chart response body items are missing")
    if len(raw_bars) > request.element_count:
        raise CarverBlocked("web chart response contains more bars than requested")
    if not raw_bars:
        raise CarverBlocked("web chart response contains no bars")

    bars: list[WebChartBar] = []
    previous_timestamp: datetime | None = None
    seen_timestamps: set[datetime] = set()
    for raw in raw_bars:
        bar = _normalize_raw_bar(raw)
        bar.validate(request)
        if bar.timestamp in seen_timestamps:
            raise CarverBlocked("web chart response contains duplicate timestamp")
        if previous_timestamp is not None and bar.timestamp <= previous_timestamp:
            raise CarverBlocked("web chart response bars must be strictly increasing")
        seen_timestamps.add(bar.timestamp)
        previous_timestamp = bar.timestamp
        bars.append(bar)
    return tuple(bars)


def web_chart_response_request_binding(request: WebChartRequest) -> dict[str, Any]:
    request_payload = request.payload()
    return {
        "endpoint": request.endpoint,
        "payload": request_payload,
        "identity": {
            "contractCode": request.symbol.contract.code,
            "contractMonth": request.symbol.contract_month,
            "displaySymbol": request.symbol.display_symbol,
            "providerSymbolId": request.symbol.provider_symbol_id,
        },
    }


def normalize_web_chart_response_file(
    file_path: Path | str,
    request: WebChartRequest,
    quarantine_root: Path | str = DEFAULT_WEB_CHART_QUARANTINE,
) -> tuple[WebChartBar, ...]:
    try:
        root = Path(quarantine_root).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("web chart quarantine root does not exist") from exc
    try:
        path = Path(file_path).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("web chart response file does not exist") from exc
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CarverBlocked("web chart response file must be inside the quarantine root") from exc
    if not path.is_file():
        raise CarverBlocked("web chart response path must be a file")
    if path.suffix.lower() != ".json":
        raise CarverBlocked("web chart response file must be JSON")
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise CarverBlocked("web chart response file must contain JSON") from exc
    return normalize_web_chart_response(payload, request)


def assert_safe_web_chart_endpoint(endpoint: str) -> None:
    if endpoint not in ALLOWED_CHART_ENDPOINTS:
        raise CarverBlocked("endpoint is not an allowed read-only chart endpoint")


def _require_response_request_binding(payload: dict[str, Any], request: WebChartRequest) -> None:
    binding = payload.get("request")
    if not isinstance(binding, dict):
        raise CarverBlocked("web chart response request binding is missing")
    if binding != web_chart_response_request_binding(request):
        raise CarverBlocked("web chart response request binding does not match locked request")


def _normalize_raw_bar(raw: Any) -> WebChartBar:
    if not isinstance(raw, dict):
        raise CarverBlocked("web chart bar must be an object")
    timestamp = _parse_timestamp(raw.get("timestamp"))
    open_price = _parse_float("open", raw.get("open"))
    high = _parse_float("high", raw.get("high"))
    low = _parse_float("low", raw.get("low"))
    close = _parse_float("close", raw.get("close"))
    volume = _parse_volume(raw)
    if "complete" not in raw:
        raise CarverBlocked("web chart bar complete flag is missing")
    complete = raw["complete"]
    if not isinstance(complete, bool):
        raise CarverBlocked("web chart bar complete flag must be boolean")
    return WebChartBar(timestamp, open_price, high, low, close, volume, complete)


def _parse_volume(raw: dict[str, Any]) -> float:
    if "volume" in raw:
        return _parse_float("volume", raw["volume"])
    if "upVolume" not in raw or "downVolume" not in raw:
        raise CarverBlocked("web chart bar volume evidence is missing")
    up = raw["upVolume"]
    down = raw["downVolume"]
    return _parse_float("upVolume", up) + _parse_float("downVolume", down)


def _parse_timestamp(value: Any) -> datetime:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(float(value)):
        raise CarverBlocked("web chart timestamp must be finite epoch milliseconds")
    return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc)


def _parse_float(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise CarverBlocked(f"{name} must be finite")
    return float(value)


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be non-negative")


def _require_positive_int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CarverBlocked(f"{name} must be a positive integer")


def _require_contract_month(value: str) -> None:
    if not isinstance(value, str) or len(value) != 5 or value[2] != "-":
        raise CarverBlocked("web chart contract month must use MM-YY")
    month, year = value.split("-")
    if not (month.isdigit() and year.isdigit()):
        raise CarverBlocked("web chart contract month must use MM-YY")
    month_number = int(month)
    if month_number < 1 or month_number > 12:
        raise CarverBlocked("web chart contract month has invalid month")


def _display_contract_month(value: str) -> str:
    month, year = value.split("-")
    month_names = {
        "01": "JAN",
        "02": "FEB",
        "03": "MAR",
        "04": "APR",
        "05": "MAY",
        "06": "JUN",
        "07": "JUL",
        "08": "AUG",
        "09": "SEP",
        "10": "OCT",
        "11": "NOV",
        "12": "DEC",
    }
    if month not in month_names:
        raise CarverBlocked("web chart contract month has invalid display month")
    return f"{month_names[month]}{year}"

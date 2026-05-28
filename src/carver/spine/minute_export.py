from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from io import StringIO
from math import isfinite
from numbers import Real
from pathlib import Path

from .m0 import ContractSpec, CarverBlocked, require_finite_positive


EXPECTED_MINUTE_EXPORT_HEADER = (
    "instrument",
    "contract_month",
    "bar_type",
    "timeframe",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
)

DEFAULT_MINUTE_EXPORT_QUARANTINE = Path("data/quarantine/ninjatrader/minute_exports")


@dataclass(frozen=True)
class MinuteExportSpec:
    contract: ContractSpec
    contract_month: str
    bar_type: str = "Last"
    timeframe: str = "1 Minute"
    session_start: time = time(13, 30)
    session_end: time = time(20, 0)
    timezone_offset_seconds: int = 0
    allowed_contract_months: tuple[str, ...] = ("03", "06", "09", "12")

    def validate(self) -> None:
        self.contract.validate()
        _require_contract_month(self.contract_month, self.allowed_contract_months)
        if self.bar_type != "Last":
            raise CarverBlocked("minute export bar_type must be Last")
        if self.timeframe != "1 Minute":
            raise CarverBlocked("minute export timeframe must be 1 Minute")
        if self.session_start >= self.session_end:
            raise CarverBlocked("minute export session window is invalid")
        _require_offset_seconds(self.timezone_offset_seconds)
        for month in self.allowed_contract_months:
            if not isinstance(month, str) or len(month) != 2 or not month.isdigit():
                raise CarverBlocked("allowed contract months must use MM strings")


@dataclass(frozen=True)
class MinuteBar:
    instrument: str
    contract_month: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def validate(self, spec: MinuteExportSpec) -> None:
        spec.validate()
        if self.instrument != spec.contract.code:
            raise CarverBlocked("minute bar instrument does not match expected contract")
        if self.contract_month != spec.contract_month:
            raise CarverBlocked("minute bar contract month does not match expected contract month")
        _validate_completed_minute(self.timestamp, spec)
        require_finite_positive("minute open", self.open)
        require_finite_positive("minute high", self.high)
        require_finite_positive("minute low", self.low)
        require_finite_positive("minute close", self.close)
        _require_finite_non_negative("minute volume", self.volume)
        if self.high < max(self.open, self.low, self.close):
            raise CarverBlocked("minute high is inconsistent with OHLC")
        if self.low > min(self.open, self.high, self.close):
            raise CarverBlocked("minute low is inconsistent with OHLC")


def parse_minute_export_text(text: str, spec: MinuteExportSpec) -> tuple[MinuteBar, ...]:
    spec.validate()
    if not isinstance(text, str) or not text.strip():
        raise CarverBlocked("minute export text is empty")

    reader = csv.DictReader(StringIO(text), strict=True)
    if tuple(reader.fieldnames or ()) != EXPECTED_MINUTE_EXPORT_HEADER:
        raise CarverBlocked("minute export header does not match expected schema")

    bars: list[MinuteBar] = []
    previous_timestamp: datetime | None = None
    seen_timestamps: set[datetime] = set()
    for row in reader:
        if set(row) != set(EXPECTED_MINUTE_EXPORT_HEADER):
            raise CarverBlocked("minute export row does not match expected schema")
        if row["bar_type"] != spec.bar_type:
            raise CarverBlocked("minute export row has wrong bar_type")
        if row["timeframe"] != spec.timeframe:
            raise CarverBlocked("minute export row has wrong timeframe")
        if any(value is None for value in row.values()):
            raise CarverBlocked("minute export row has extra fields")
        if any(row[column] is None or row[column] == "" for column in EXPECTED_MINUTE_EXPORT_HEADER):
            raise CarverBlocked("minute export row has missing fields")
        bar = MinuteBar(
            instrument=row["instrument"],
            contract_month=row["contract_month"],
            timestamp=_parse_timestamp(row["timestamp"]),
            open=_parse_float("open", row["open"]),
            high=_parse_float("high", row["high"]),
            low=_parse_float("low", row["low"]),
            close=_parse_float("close", row["close"]),
            volume=_parse_float("volume", row["volume"]),
        )
        bar.validate(spec)
        if bar.timestamp in seen_timestamps:
            raise CarverBlocked("minute export contains duplicate timestamp")
        if previous_timestamp is not None:
            if bar.timestamp <= previous_timestamp:
                raise CarverBlocked("minute export rows must be strictly increasing")
            if bar.timestamp - previous_timestamp != timedelta(minutes=1):
                raise CarverBlocked("minute export rows must be contiguous one-minute bars")
        seen_timestamps.add(bar.timestamp)
        previous_timestamp = bar.timestamp
        bars.append(bar)

    if not bars:
        raise CarverBlocked("minute export contains no rows")
    return tuple(bars)


def parse_minute_export_file(
    file_path: Path | str,
    spec: MinuteExportSpec,
    quarantine_root: Path | str = DEFAULT_MINUTE_EXPORT_QUARANTINE,
) -> tuple[MinuteBar, ...]:
    try:
        root = Path(quarantine_root).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("minute export quarantine root does not exist") from exc
    try:
        path = Path(file_path).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("minute export file does not exist") from exc
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CarverBlocked("minute export file must be inside the quarantine root") from exc
    if not path.is_file():
        raise CarverBlocked("minute export path must be a file")
    if path.suffix.lower() not in {".csv", ".txt"}:
        raise CarverBlocked("minute export file must be CSV/text, not platform cache")
    return parse_minute_export_text(path.read_text(encoding="utf-8-sig"), spec)


def _parse_timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked("minute timestamp is missing")
    try:
        timestamp = datetime.fromisoformat(value)
    except ValueError as exc:
        raise CarverBlocked("minute timestamp must be ISO-8601") from exc
    _validate_completed_minute(timestamp)
    return timestamp


def _validate_completed_minute(timestamp: datetime, spec: MinuteExportSpec | None = None) -> None:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise CarverBlocked("minute timestamp must be timezone-aware")
    if timestamp.second or timestamp.microsecond:
        raise CarverBlocked("minute timestamp must be minute-aligned")
    if spec is not None:
        if int(timestamp.utcoffset().total_seconds()) != spec.timezone_offset_seconds:
            raise CarverBlocked("minute timestamp timezone offset does not match export spec")
        minute_time = timestamp.timetz().replace(tzinfo=None)
        if minute_time < spec.session_start or minute_time >= spec.session_end:
            raise CarverBlocked("minute timestamp is outside locked session window")


def _parse_float(name: str, value: str) -> float:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked(f"{name} is missing")
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be numeric") from exc
    if not isfinite(parsed):
        raise CarverBlocked(f"{name} must be finite")
    return parsed


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be non-negative")


def _require_contract_month(value: str, allowed_months: tuple[str, ...]) -> None:
    if not isinstance(value, str) or len(value) != 5 or value[2] != "-":
        raise CarverBlocked("contract month must use MM-YY")
    month, year = value.split("-")
    if not (month.isdigit() and year.isdigit()):
        raise CarverBlocked("contract month must use MM-YY")
    month_number = int(month)
    if month_number < 1 or month_number > 12:
        raise CarverBlocked("contract month has invalid month")
    if month not in allowed_months:
        raise CarverBlocked("contract month is not allowed for this source-native contract")


def _require_offset_seconds(value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CarverBlocked("timezone offset must be integer seconds")

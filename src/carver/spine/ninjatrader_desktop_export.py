from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from io import StringIO
from math import isfinite
from numbers import Real
from pathlib import Path

from .daily_bars import CompletedDailyMarketBar
from .m0 import CompletedBar, ContractSpec, CarverBlocked, require_finite_positive
from .m3 import zn_contract


CARVER_WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
EXPECTED_NINJATRADER_DAILY_EXPORT_HEADER = (
    "instrument",
    "contract_month",
    "display_symbol",
    "bar_type",
    "timeframe",
    "trade_date",
    "open",
    "high",
    "low",
    "close",
    "volume",
)

DEFAULT_NINJATRADER_DAILY_EXPORT_QUARANTINE = (
    CARVER_WORKSPACE_ROOT / "data" / "quarantine" / "ninjatrader" / "desktop_daily_exports"
)
S09_ZN_DESKTOP_DAILY_EXPORT_FILE_NAME = "ZN_06-26_Daily_Last_257.csv"


@dataclass(frozen=True)
class NinjaTraderDailyExportSpec:
    contract: ContractSpec
    contract_month: str
    display_symbol: str
    expected_rows: int
    bar_type: str = "Last"
    timeframe: str = "1 Day"
    allowed_contract_months: tuple[str, ...] = ("03", "06", "09", "12")

    def validate(self) -> None:
        self.contract.validate()
        if self.contract != zn_contract():
            raise CarverBlocked("NinjaTrader desktop daily export is locked to ZN")
        _require_contract_month(self.contract_month, self.allowed_contract_months)
        if self.contract_month != "06-26":
            raise CarverBlocked("NinjaTrader desktop daily export is locked to ZN 06-26")
        if self.display_symbol != f"{self.contract.code} {self.contract_month}":
            raise CarverBlocked("NinjaTrader desktop display symbol must match contract and month")
        if self.display_symbol != "ZN 06-26":
            raise CarverBlocked("NinjaTrader desktop daily export display symbol is locked to ZN 06-26")
        if self.bar_type != "Last":
            raise CarverBlocked("NinjaTrader daily export bar_type must be Last")
        if self.timeframe != "1 Day":
            raise CarverBlocked("NinjaTrader daily export timeframe must be 1 Day")
        _require_positive_int("NinjaTrader daily export expected rows", self.expected_rows)
        if self.expected_rows != 257:
            raise CarverBlocked("NinjaTrader desktop daily export is locked to 257 rows")


def s09_zn_ninjatrader_daily_export_spec() -> NinjaTraderDailyExportSpec:
    return NinjaTraderDailyExportSpec(
        contract=zn_contract(),
        contract_month="06-26",
        display_symbol="ZN 06-26",
        expected_rows=257,
    )


def parse_ninjatrader_daily_export_text(
    text: str,
    spec: NinjaTraderDailyExportSpec,
) -> tuple[CompletedDailyMarketBar, ...]:
    spec.validate()
    if not isinstance(text, str) or not text.strip():
        raise CarverBlocked("NinjaTrader daily export text is empty")

    reader = csv.DictReader(StringIO(text), strict=True)
    if tuple(reader.fieldnames or ()) != EXPECTED_NINJATRADER_DAILY_EXPORT_HEADER:
        raise CarverBlocked("NinjaTrader daily export header does not match expected schema")

    bars: list[CompletedDailyMarketBar] = []
    previous_timestamp: datetime | None = None
    seen_timestamps: set[datetime] = set()
    for row in reader:
        if set(row) != set(EXPECTED_NINJATRADER_DAILY_EXPORT_HEADER):
            raise CarverBlocked("NinjaTrader daily export row does not match expected schema")
        if any(value is None for value in row.values()):
            raise CarverBlocked("NinjaTrader daily export row has extra fields")
        if any(row[column] is None or row[column] == "" for column in EXPECTED_NINJATRADER_DAILY_EXPORT_HEADER):
            raise CarverBlocked("NinjaTrader daily export row has missing fields")
        _validate_identity(row, spec)

        timestamp = _parse_trade_date(row["trade_date"])
        bar = CompletedDailyMarketBar(
            completed_bar=CompletedBar(timestamp),
            contract=spec.contract,
            contract_month=row["contract_month"],
            open=_parse_float("open", row["open"]),
            high=_parse_float("high", row["high"]),
            low=_parse_float("low", row["low"]),
            close=_parse_float("close", row["close"]),
            volume=_parse_float("volume", row["volume"]),
        )
        bar.validate()
        if timestamp in seen_timestamps:
            raise CarverBlocked("NinjaTrader daily export contains duplicate trade date")
        if previous_timestamp is not None and timestamp <= previous_timestamp:
            raise CarverBlocked("NinjaTrader daily export rows must be strictly increasing by trade date")
        seen_timestamps.add(timestamp)
        previous_timestamp = timestamp
        bars.append(bar)

    if len(bars) != spec.expected_rows:
        raise CarverBlocked("NinjaTrader daily export row count does not match locked expected rows")
    return tuple(bars)


def parse_ninjatrader_daily_export_file(
    file_path: Path | str,
    spec: NinjaTraderDailyExportSpec,
    quarantine_root: Path | str = DEFAULT_NINJATRADER_DAILY_EXPORT_QUARANTINE,
) -> tuple[CompletedDailyMarketBar, ...]:
    try:
        root = Path(quarantine_root).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("NinjaTrader daily export quarantine root does not exist") from exc
    try:
        path = Path(file_path).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("NinjaTrader daily export file does not exist") from exc
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CarverBlocked("NinjaTrader daily export file must be inside the quarantine root") from exc
    if not path.is_file():
        raise CarverBlocked("NinjaTrader daily export path must be a file")
    if path.name != S09_ZN_DESKTOP_DAILY_EXPORT_FILE_NAME:
        raise CarverBlocked("NinjaTrader daily export filename is not the locked ZN 06-26 file")
    if path.suffix.lower() not in {".csv", ".txt"}:
        raise CarverBlocked("NinjaTrader daily export file must be CSV/text, not platform cache")
    return parse_ninjatrader_daily_export_text(path.read_text(encoding="utf-8-sig"), spec)


def _validate_identity(row: dict[str, str], spec: NinjaTraderDailyExportSpec) -> None:
    if row["instrument"] != spec.contract.code:
        raise CarverBlocked("NinjaTrader daily export instrument does not match expected contract")
    if row["contract_month"] != spec.contract_month:
        raise CarverBlocked("NinjaTrader daily export contract month does not match expected contract month")
    if row["display_symbol"] != spec.display_symbol:
        raise CarverBlocked("NinjaTrader daily export display symbol does not match expected contract")
    if row["bar_type"] != spec.bar_type:
        raise CarverBlocked("NinjaTrader daily export row has wrong bar_type")
    if row["timeframe"] != spec.timeframe:
        raise CarverBlocked("NinjaTrader daily export row has wrong timeframe")


def _parse_trade_date(value: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked("NinjaTrader daily export trade date is missing")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise CarverBlocked("NinjaTrader daily export trade date must use YYYY-MM-DD") from exc
    return parsed.replace(tzinfo=timezone.utc)


def _parse_float(name: str, value: str) -> float:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked(f"{name} is missing")
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be numeric") from exc
    if not isfinite(parsed):
        raise CarverBlocked(f"{name} must be finite")
    if name == "volume":
        _require_finite_non_negative(name, parsed)
    else:
        require_finite_positive(name, parsed)
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
    for allowed in allowed_months:
        if not isinstance(allowed, str) or len(allowed) != 2 or not allowed.isdigit():
            raise CarverBlocked("allowed contract months must use MM strings")


def _require_positive_int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CarverBlocked(f"{name} must be a positive integer")

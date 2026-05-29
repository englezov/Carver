from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from math import isfinite
from numbers import Real
from pathlib import Path

from .daily_bars import CompletedDailyMarketBar
from .m0 import CompletedBar, ContractSpec, LaneClass, CarverBlocked, require_finite_positive, require_non_empty_text, require_source_native
from .m3 import mes_contract, mgc_contract, qm_contract, zc_contract, zf_contract, zn_contract


CARVER_WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE = (
    CARVER_WORKSPACE_ROOT / "data" / "quarantine" / "ninjatrader" / "native_daily_exports"
)
PARTS_1_3_DAILY_SEED_MANIFEST_CONFIG = (
    CARVER_WORKSPACE_ROOT / "config" / "carver_daily_futures_manifest_parts_1_3_seed.json"
)
NINJATRADER_MANIFEST_DAILY_EXPORT_HELPER = CARVER_WORKSPACE_ROOT / "tools" / "nt8" / "CarverManifestDailyExporter.cs"


class AcquisitionFrequency(StrEnum):
    DAILY = "DAILY"


class NinjaTraderDataType(StrEnum):
    LAST = "Last"


class NinjaTraderInterval(StrEnum):
    DAY = "Day"


@dataclass(frozen=True)
class FuturesRootManifestEntry:
    contract: ContractSpec
    asset_class: str
    book_role: str
    frequency: AcquisitionFrequency = AcquisitionFrequency.DAILY
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    @property
    def root(self) -> str:
        return self.contract.code

    def validate(self) -> None:
        require_source_native(self.lane_class)
        self.contract.validate()
        require_non_empty_text("asset class", self.asset_class)
        require_non_empty_text("book role", self.book_role)
        if self.frequency is not AcquisitionFrequency.DAILY:
            raise CarverBlocked("initial acquisition manifest is locked to daily futures data")


@dataclass(frozen=True)
class NinjaTraderNativeDailyExportRequest:
    contract: ContractSpec
    contract_month: str
    ninjatrader_symbol: str
    start_date: str
    end_date: str
    data_type: NinjaTraderDataType = NinjaTraderDataType.LAST
    interval: NinjaTraderInterval = NinjaTraderInterval.DAY
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    def validate(self) -> None:
        require_source_native(self.lane_class)
        self.contract.validate()
        _require_contract_month(self.contract_month)
        if self.ninjatrader_symbol != f"{self.contract.code} {_contract_month_to_ninjatrader(self.contract_month)}":
            raise CarverBlocked("NinjaTrader symbol does not match source-native contract month")
        start = _parse_yyyy_mm_dd(self.start_date, "start date")
        end = _parse_yyyy_mm_dd(self.end_date, "end date")
        if start > end:
            raise CarverBlocked("NinjaTrader export start date must not be after end date")
        if self.data_type is not NinjaTraderDataType.LAST:
            raise CarverBlocked("NinjaTrader daily export request is locked to Last data")
        if self.interval is not NinjaTraderInterval.DAY:
            raise CarverBlocked("NinjaTrader daily export request is locked to Day interval")

    @property
    def native_file_name(self) -> str:
        self.validate()
        return f"{self.contract.code} {self.contract_month}.Last.txt"

    @property
    def quarantine_relative_path(self) -> Path:
        self.validate()
        return Path(self.contract.code) / self.native_file_name

    def quarantine_path(self, root: Path | str = DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE) -> Path:
        return _resolve_carver_quarantine(root) / self.quarantine_relative_path


@dataclass(frozen=True)
class SourceNativeDailyAcquisitionManifest:
    manifest_id: str
    roots: tuple[FuturesRootManifestEntry, ...]
    export_requests: tuple[NinjaTraderNativeDailyExportRequest, ...]
    minimum_continuous_rows: int
    lane_class: LaneClass = LaneClass.SOURCE_NATIVE_FUTURES

    def validate(self) -> None:
        require_source_native(self.lane_class)
        require_non_empty_text("manifest id", self.manifest_id)
        _require_positive_int("minimum continuous rows", self.minimum_continuous_rows)
        if not self.roots:
            raise CarverBlocked("acquisition manifest requires at least one futures root")
        if not self.export_requests:
            raise CarverBlocked("acquisition manifest requires at least one export request")

        seen_roots: set[str] = set()
        for root in self.roots:
            root.validate()
            if root.root in seen_roots:
                raise CarverBlocked("acquisition manifest contains duplicate futures roots")
            seen_roots.add(root.root)

        request_keys: set[tuple[str, str]] = set()
        for request in self.export_requests:
            request.validate()
            if request.contract.code not in seen_roots:
                raise CarverBlocked("export request root is not declared in manifest roots")
            key = (request.contract.code, request.contract_month)
            if key in request_keys:
                raise CarverBlocked("acquisition manifest contains duplicate export request")
            request_keys.add(key)


@dataclass(frozen=True)
class NinjaTraderManifestExportPlanRow:
    manifest_id: str
    root: str
    contract_month: str
    ninjatrader_symbol: str
    start_date: str
    end_date: str
    data_type: NinjaTraderDataType
    interval: NinjaTraderInterval
    native_file: Path

    def validate(self, manifest: SourceNativeDailyAcquisitionManifest) -> None:
        manifest.validate()
        if self.manifest_id != manifest.manifest_id:
            raise CarverBlocked("NinjaTrader manifest export row has wrong manifest id")
        if self.data_type is not NinjaTraderDataType.LAST:
            raise CarverBlocked("NinjaTrader manifest export row is locked to Last data")
        if self.interval is not NinjaTraderInterval.DAY:
            raise CarverBlocked("NinjaTrader manifest export row is locked to Day interval")
        if self.native_file.is_absolute():
            raise CarverBlocked("NinjaTrader manifest export row native file must be relative")
        for request in manifest.export_requests:
            if (
                self.root == request.contract.code
                and self.contract_month == request.contract_month
                and self.ninjatrader_symbol == request.ninjatrader_symbol
                and self.start_date == request.start_date
                and self.end_date == request.end_date
                and self.native_file == request.quarantine_relative_path
            ):
                return
        raise CarverBlocked("NinjaTrader manifest export row is not declared in the acquisition manifest")

    @property
    def output_path(self) -> Path:
        if self.native_file.is_absolute():
            raise CarverBlocked("NinjaTrader manifest export row native file must be relative")
        return DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE / self.native_file


@dataclass(frozen=True)
class NativeDailyExportValidationSummary:
    root: str
    contract_month: str
    ninjatrader_symbol: str
    native_file: Path
    row_count: int
    first_date: str
    last_date: str
    first_open: float
    first_high: float
    first_low: float
    first_close: float
    last_open: float
    last_high: float
    last_low: float
    last_close: float

    def validate(self) -> None:
        require_non_empty_text("root", self.root)
        _require_contract_month(self.contract_month)
        require_non_empty_text("NinjaTrader symbol", self.ninjatrader_symbol)
        if self.native_file.is_absolute():
            raise CarverBlocked("native daily export validation summary file path must be relative")
        _require_positive_int("native daily export validation row count", self.row_count)
        first = _parse_yyyy_mm_dd(self.first_date, "first date")
        last = _parse_yyyy_mm_dd(self.last_date, "last date")
        if first > last:
            raise CarverBlocked("native daily export validation summary first date must not be after last date")
        for name, value in (
            ("first open", self.first_open),
            ("first high", self.first_high),
            ("first low", self.first_low),
            ("first close", self.first_close),
            ("last open", self.last_open),
            ("last high", self.last_high),
            ("last low", self.last_low),
            ("last close", self.last_close),
        ):
            require_finite_positive(name, value)


@dataclass(frozen=True)
class NativeDailyExportForensicReport:
    manifest_id: str
    summaries: tuple[NativeDailyExportValidationSummary, ...]
    minimum_continuous_rows: int
    identical_first_date_count: int
    identical_first_ohlc_count: int
    potential_provider_merge_policy: bool

    def validate(self, manifest: SourceNativeDailyAcquisitionManifest) -> None:
        manifest.validate()
        if self.manifest_id != manifest.manifest_id:
            raise CarverBlocked("native daily export forensic report manifest id mismatch")
        if self.minimum_continuous_rows != manifest.minimum_continuous_rows:
            raise CarverBlocked("native daily export forensic report minimum rows mismatch")
        if len(self.summaries) != len(manifest.export_requests):
            raise CarverBlocked("native daily export forensic report must cover every manifest request")
        for summary in self.summaries:
            summary.validate()
        expected_files = {request.quarantine_relative_path for request in manifest.export_requests}
        actual_files = {summary.native_file for summary in self.summaries}
        if actual_files != expected_files:
            raise CarverBlocked("native daily export forensic report file set does not match manifest")
        _require_positive_int("identical first date count", self.identical_first_date_count)
        _require_positive_int("identical first OHLC count", self.identical_first_ohlc_count)


def build_parts_1_3_daily_seed_manifest() -> SourceNativeDailyAcquisitionManifest:
    roots = (
        FuturesRootManifestEntry(mes_contract(), "Equity index", "P01/P02 equity leg; daily stack seed"),
        FuturesRootManifestEntry(zn_contract(), "Bond", "P01/P02/S09 ZN continuous-readiness seed"),
        FuturesRootManifestEntry(zf_contract(), "Bond", "P02 bond leg; daily stack seed"),
        FuturesRootManifestEntry(qm_contract(), "Energy", "P02 commodity leg; daily stack seed"),
        FuturesRootManifestEntry(zc_contract(), "Grain", "P02 commodity leg; daily stack seed"),
        FuturesRootManifestEntry(mgc_contract(), "Metal", "P02 gold leg; daily stack seed"),
    )
    zn_chain = tuple(
        NinjaTraderNativeDailyExportRequest(
            zn_contract(),
            contract_month,
            ninjatrader_symbol,
            start_date="2025-05-29",
            end_date="2026-05-28",
        )
        for contract_month, ninjatrader_symbol in (
            ("09-25", "ZN SEP25"),
            ("12-25", "ZN DEC25"),
            ("03-26", "ZN MAR26"),
            ("06-26", "ZN JUN26"),
        )
    )
    manifest = SourceNativeDailyAcquisitionManifest(
        manifest_id="CARVER_PARTS_1_3_DAILY_SEED_S09_ZN_CONTINUOUS_READINESS",
        roots=roots,
        export_requests=zn_chain,
        minimum_continuous_rows=257,
    )
    manifest.validate()
    return manifest


def build_ninjatrader_manifest_export_plan(
    manifest: SourceNativeDailyAcquisitionManifest | None = None,
) -> tuple[NinjaTraderManifestExportPlanRow, ...]:
    active_manifest = manifest or build_parts_1_3_daily_seed_manifest()
    active_manifest.validate()
    rows = tuple(
        NinjaTraderManifestExportPlanRow(
            manifest_id=active_manifest.manifest_id,
            root=request.contract.code,
            contract_month=request.contract_month,
            ninjatrader_symbol=request.ninjatrader_symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            data_type=request.data_type,
            interval=request.interval,
            native_file=request.quarantine_relative_path,
        )
        for request in active_manifest.export_requests
    )
    for row in rows:
        row.validate(active_manifest)
    return rows


def render_ninjatrader_manifest_export_plan_csv(
    manifest: SourceNativeDailyAcquisitionManifest | None = None,
) -> str:
    rows = build_ninjatrader_manifest_export_plan(manifest)
    header = "manifest_id,root,contract_month,ninjatrader_symbol,start_date,end_date,data_type,interval,native_file"
    rendered_rows = [
        ",".join(
            (
                row.manifest_id,
                row.root,
                row.contract_month,
                row.ninjatrader_symbol,
                row.start_date,
                row.end_date,
                row.data_type.value,
                row.interval.value,
                row.native_file.as_posix(),
            )
        )
        for row in rows
    ]
    return "\n".join((header, *rendered_rows)) + "\n"


def load_parts_1_3_daily_seed_manifest_config(
    path: Path | str = PARTS_1_3_DAILY_SEED_MANIFEST_CONFIG,
) -> dict:
    try:
        resolved = Path(path).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("daily futures manifest config does not exist") from exc
    expected = PARTS_1_3_DAILY_SEED_MANIFEST_CONFIG.resolve()
    if resolved != expected:
        raise CarverBlocked("daily futures manifest config path is not the locked seed manifest")
    try:
        payload = json.loads(resolved.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise CarverBlocked("daily futures manifest config must be valid JSON") from exc
    require_seed_manifest_config_matches_code(payload, build_parts_1_3_daily_seed_manifest())
    return payload


def require_seed_manifest_config_matches_code(
    payload: dict,
    manifest: SourceNativeDailyAcquisitionManifest,
) -> None:
    manifest.validate()
    if not isinstance(payload, dict):
        raise CarverBlocked("daily futures manifest config must be a JSON object")
    if payload.get("manifest_id") != manifest.manifest_id:
        raise CarverBlocked("daily futures manifest config id does not match code manifest")
    if payload.get("lane_class") != LaneClass.SOURCE_NATIVE_FUTURES.value:
        raise CarverBlocked("daily futures manifest config lane class must be SOURCE_NATIVE_FUTURES")
    if payload.get("frequency") != AcquisitionFrequency.DAILY.value:
        raise CarverBlocked("daily futures manifest config frequency must be DAILY")
    if payload.get("data_type") != NinjaTraderDataType.LAST.value:
        raise CarverBlocked("daily futures manifest config data type must be Last")
    if payload.get("interval") != NinjaTraderInterval.DAY.value:
        raise CarverBlocked("daily futures manifest config interval must be Day")
    if payload.get("minimum_continuous_rows") != manifest.minimum_continuous_rows:
        raise CarverBlocked("daily futures manifest config minimum rows do not match code manifest")

    config_roots = payload.get("roots")
    if not isinstance(config_roots, list):
        raise CarverBlocked("daily futures manifest config roots must be a list")
    expected_roots = [
        {
            "root": root.root,
            "book_name": root.contract.name,
            "asset_class": root.asset_class,
            "book_role": root.book_role,
        }
        for root in manifest.roots
    ]
    if any(not isinstance(row, dict) for row in config_roots):
        raise CarverBlocked("daily futures manifest config roots must contain only objects")
    if config_roots != expected_roots:
        raise CarverBlocked("daily futures manifest config roots do not match code manifest")

    config_requests = payload.get("first_chain_requests")
    if not isinstance(config_requests, list):
        raise CarverBlocked("daily futures manifest config requests must be a list")
    expected_requests = [
        {
            "root": request.contract.code,
            "contract_month": request.contract_month,
            "ninjatrader_symbol": request.ninjatrader_symbol,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "native_file": request.quarantine_relative_path.as_posix(),
        }
        for request in manifest.export_requests
    ]
    if config_requests != expected_requests:
        raise CarverBlocked("daily futures manifest config requests do not match code manifest")


def require_manifest_export_request(
    manifest: SourceNativeDailyAcquisitionManifest,
    request: NinjaTraderNativeDailyExportRequest,
) -> None:
    manifest.validate()
    request.validate()
    for candidate in manifest.export_requests:
        if candidate == request:
            return
    raise CarverBlocked("native NinjaTrader daily export request is not declared in the acquisition manifest")


def parse_native_ninjatrader_daily_export_text(
    text: str,
    request: NinjaTraderNativeDailyExportRequest,
    manifest: SourceNativeDailyAcquisitionManifest | None = None,
) -> tuple[CompletedDailyMarketBar, ...]:
    request.validate()
    require_manifest_export_request(manifest or build_parts_1_3_daily_seed_manifest(), request)
    if not isinstance(text, str) or not text.strip():
        raise CarverBlocked("native NinjaTrader daily export text is empty")

    bars: list[CompletedDailyMarketBar] = []
    seen_timestamps: set[datetime] = set()
    previous_timestamp: datetime | None = None
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        fields = line.split(";")
        if len(fields) != 6:
            raise CarverBlocked("native NinjaTrader daily export row must have 6 semicolon fields")
        timestamp = _parse_yyyymmdd(fields[0], line_number)
        start = _parse_yyyy_mm_dd(request.start_date, "start date")
        end = _parse_yyyy_mm_dd(request.end_date, "end date")
        if timestamp.date() < start.date() or timestamp.date() > end.date():
            raise CarverBlocked("native NinjaTrader daily export row is outside locked request date range")
        bar = CompletedDailyMarketBar(
            completed_bar=CompletedBar(timestamp),
            contract=request.contract,
            contract_month=request.contract_month,
            open=_parse_float("open", fields[1]),
            high=_parse_float("high", fields[2]),
            low=_parse_float("low", fields[3]),
            close=_parse_float("close", fields[4]),
            volume=_parse_float("volume", fields[5], allow_zero=True),
        )
        bar.validate()
        if timestamp in seen_timestamps:
            raise CarverBlocked("native NinjaTrader daily export contains duplicate trade date")
        if previous_timestamp is not None and timestamp <= previous_timestamp:
            raise CarverBlocked("native NinjaTrader daily export rows must be strictly increasing by trade date")
        seen_timestamps.add(timestamp)
        previous_timestamp = timestamp
        bars.append(bar)

    if not bars:
        raise CarverBlocked("native NinjaTrader daily export contains no completed daily rows")
    return tuple(bars)


def parse_native_ninjatrader_daily_export_file(
    file_path: Path | str,
    request: NinjaTraderNativeDailyExportRequest,
    quarantine_root: Path | str = DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE,
    manifest: SourceNativeDailyAcquisitionManifest | None = None,
) -> tuple[CompletedDailyMarketBar, ...]:
    request.validate()
    active_manifest = manifest or build_parts_1_3_daily_seed_manifest()
    require_manifest_export_request(active_manifest, request)
    root = _resolve_carver_quarantine(quarantine_root)
    try:
        path = Path(file_path).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("native NinjaTrader daily export file does not exist") from exc
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CarverBlocked("native NinjaTrader daily export file must be inside the Carver quarantine") from exc
    if not path.is_file():
        raise CarverBlocked("native NinjaTrader daily export path must be a file")
    if path.name != request.native_file_name:
        raise CarverBlocked("native NinjaTrader daily export filename does not match locked request")
    if path.suffix.lower() != ".txt":
        raise CarverBlocked("native NinjaTrader daily export must be the platform text export")
    return parse_native_ninjatrader_daily_export_text(path.read_text(encoding="utf-8-sig"), request, active_manifest)


def validate_manifest_native_daily_exports(
    manifest: SourceNativeDailyAcquisitionManifest | None = None,
    quarantine_root: Path | str = DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE,
) -> NativeDailyExportForensicReport:
    active_manifest = manifest or build_parts_1_3_daily_seed_manifest()
    active_manifest.validate()
    summaries: list[NativeDailyExportValidationSummary] = []
    for request in active_manifest.export_requests:
        bars = parse_native_ninjatrader_daily_export_file(
            request.quarantine_path(quarantine_root),
            request,
            quarantine_root=quarantine_root,
            manifest=active_manifest,
        )
        first = bars[0]
        last = bars[-1]
        summaries.append(
            NativeDailyExportValidationSummary(
                root=request.contract.code,
                contract_month=request.contract_month,
                ninjatrader_symbol=request.ninjatrader_symbol,
                native_file=request.quarantine_relative_path,
                row_count=len(bars),
                first_date=first.timestamp.date().isoformat(),
                last_date=last.timestamp.date().isoformat(),
                first_open=first.open,
                first_high=first.high,
                first_low=first.low,
                first_close=first.close,
                last_open=last.open,
                last_high=last.high,
                last_low=last.low,
                last_close=last.close,
            )
        )

    identical_first_date_count = _largest_duplicate_count(summary.first_date for summary in summaries)
    identical_first_ohlc_count = _largest_duplicate_count(
        (
            summary.first_open,
            summary.first_high,
            summary.first_low,
            summary.first_close,
        )
        for summary in summaries
    )
    report = NativeDailyExportForensicReport(
        manifest_id=active_manifest.manifest_id,
        summaries=tuple(summaries),
        minimum_continuous_rows=active_manifest.minimum_continuous_rows,
        identical_first_date_count=identical_first_date_count,
        identical_first_ohlc_count=identical_first_ohlc_count,
        potential_provider_merge_policy=identical_first_date_count > 1 and identical_first_ohlc_count > 1,
    )
    report.validate(active_manifest)
    return report


def render_native_daily_export_forensic_markdown(report: NativeDailyExportForensicReport) -> str:
    lines = [
        f"Manifest: `{report.manifest_id}`",
        "",
        "| File | Rows | First date | Last date | First OHLC | Last OHLC |",
        "|---|---:|---|---|---|---|",
    ]
    for summary in report.summaries:
        lines.append(
            "| "
            + " | ".join(
                (
                    summary.native_file.as_posix(),
                    str(summary.row_count),
                    summary.first_date,
                    summary.last_date,
                    _format_ohlc(summary.first_open, summary.first_high, summary.first_low, summary.first_close),
                    _format_ohlc(summary.last_open, summary.last_high, summary.last_low, summary.last_close),
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            f"Minimum continuous-readiness target: `{report.minimum_continuous_rows}` rows.",
            f"Largest identical first-date cluster: `{report.identical_first_date_count}`.",
            f"Largest identical first-OHLC cluster: `{report.identical_first_ohlc_count}`.",
            f"Potential provider merge policy: `{str(report.potential_provider_merge_policy).upper()}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def _resolve_carver_quarantine(root: Path | str) -> Path:
    try:
        resolved = Path(root).resolve(strict=True)
    except FileNotFoundError as exc:
        raise CarverBlocked("native NinjaTrader daily export quarantine root does not exist") from exc
    expected = DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE.resolve()
    try:
        resolved.relative_to(expected)
    except ValueError as exc:
        raise CarverBlocked("native NinjaTrader daily export quarantine root must stay under the Carver native daily quarantine") from exc
    return resolved


def _contract_month_to_ninjatrader(contract_month: str) -> str:
    _require_contract_month(contract_month)
    month, year = contract_month.split("-")
    codes = {
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
    return f"{codes[month]}{year}"


def _parse_yyyymmdd(value: str, line_number: int) -> datetime:
    if not isinstance(value, str) or len(value) != 8 or not value.isdigit():
        raise CarverBlocked(f"native NinjaTrader daily export date is invalid on line {line_number}")
    try:
        parsed = datetime.strptime(value, "%Y%m%d")
    except ValueError as exc:
        raise CarverBlocked(f"native NinjaTrader daily export date is invalid on line {line_number}") from exc
    return parsed.replace(tzinfo=timezone.utc)


def _parse_yyyy_mm_dd(value: str, name: str) -> datetime:
    if not isinstance(value, str):
        raise CarverBlocked(f"{name} must use YYYY-MM-DD")
    try:
        return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must use YYYY-MM-DD") from exc


def _parse_float(name: str, value: str, allow_zero: bool = False) -> float:
    if not isinstance(value, str) or not value.strip():
        raise CarverBlocked(f"{name} is missing")
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CarverBlocked(f"{name} must be numeric") from exc
    if not isfinite(parsed):
        raise CarverBlocked(f"{name} must be finite")
    if allow_zero:
        _require_finite_non_negative(name, parsed)
    else:
        require_finite_positive(name, parsed)
    return parsed


def _require_contract_month(value: str) -> None:
    if not isinstance(value, str) or len(value) != 5 or value[2] != "-":
        raise CarverBlocked("contract month must use MM-YY")
    month, year = value.split("-")
    if not (month.isdigit() and year.isdigit()):
        raise CarverBlocked("contract month must use MM-YY")
    month_number = int(month)
    if month_number < 1 or month_number > 12:
        raise CarverBlocked("contract month has invalid month")


def _require_finite_non_negative(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)) or value < 0:
        raise CarverBlocked(f"{name} must be non-negative")


def _require_positive_int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CarverBlocked(f"{name} must be a positive integer")


def _largest_duplicate_count(values) -> int:
    counts: dict[object, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    if not counts:
        raise CarverBlocked("cannot compute duplicate count for empty values")
    return max(counts.values())


def _format_ohlc(open_value: float, high_value: float, low_value: float, close_value: float) -> str:
    return f"{open_value:g}/{high_value:g}/{low_value:g}/{close_value:g}"

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .daily_bars import CompletedDailyMarketBar
from .first_spine import p01_synthetic_conformance, p02_synthetic_conformance
from .m0 import CarverBlocked, ContractSpec
from .m1 import RoundingPolicy, SizingResult, TimedValue
from .m3 import LegMarketInput, PortfolioSpec
from .web_chart_api import LOCKED_WEB_CHART_PROVIDER_SYMBOLS


class ProviderMappingStatus(StrEnum):
    LOCKED = "LOCKED"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class PortfolioProviderMappingRow:
    contract_code: str
    contract_month: str
    display_symbol: str
    status: ProviderMappingStatus
    provider_symbol_id: str | None = None


@dataclass(frozen=True)
class LockedPortfolioProviderMapping:
    contract: ContractSpec
    contract_month: str
    display_symbol: str
    provider_symbol_id: str

    @property
    def code(self) -> str:
        return self.contract.code

    def validate(self) -> None:
        self.contract.validate()
        if self.display_symbol != _display_symbol(self.contract.code, self.contract_month):
            raise CarverBlocked("provider mapping display symbol does not match contract month")
        if not isinstance(self.provider_symbol_id, str) or not self.provider_symbol_id.isdigit():
            raise CarverBlocked("provider mapping id must be a numeric string")
        locked_id = LOCKED_WEB_CHART_PROVIDER_SYMBOLS.get((self.contract.code, self.contract_month, self.display_symbol))
        if locked_id != self.provider_symbol_id:
            raise CarverBlocked("provider mapping is not locked in the observed mapping registry")


@dataclass(frozen=True)
class PortfolioProviderMappingSet:
    portfolio: PortfolioSpec
    mappings: tuple[LockedPortfolioProviderMapping, ...]

    def validate(self) -> None:
        self.portfolio.validate()
        expected_codes = {leg.code for leg in self.portfolio.legs}
        provided_codes = {mapping.code for mapping in self.mappings}
        if provided_codes != expected_codes:
            raise CarverBlocked("locked provider mappings must exactly match portfolio legs")
        leg_by_code = {leg.code: leg for leg in self.portfolio.legs}
        seen_ids: set[str] = set()
        for mapping in self.mappings:
            mapping.validate()
            leg = leg_by_code[mapping.code]
            if mapping.contract != leg.contract:
                raise CarverBlocked("provider mapping contract does not match portfolio leg")
            if mapping.provider_symbol_id in seen_ids:
                raise CarverBlocked("provider mapping ids must be unique")
            seen_ids.add(mapping.provider_symbol_id)

    @property
    def contract_months(self) -> dict[str, str]:
        self.validate()
        return {mapping.code: mapping.contract_month for mapping in self.mappings}


def portfolio_web_chart_mapping_status(
    portfolio: PortfolioSpec,
    contract_months: dict[str, str],
) -> tuple[PortfolioProviderMappingRow, ...]:
    portfolio.validate()
    expected_codes = {leg.code for leg in portfolio.legs}
    if set(contract_months) != expected_codes:
        raise CarverBlocked("portfolio mapping status requires exact contract months for all legs")
    rows: list[PortfolioProviderMappingRow] = []
    for leg in portfolio.legs:
        contract_month = contract_months[leg.code]
        display_symbol = _display_symbol(leg.code, contract_month)
        provider_symbol_id = LOCKED_WEB_CHART_PROVIDER_SYMBOLS.get((leg.code, contract_month, display_symbol))
        rows.append(
            PortfolioProviderMappingRow(
                contract_code=leg.code,
                contract_month=contract_month,
                display_symbol=display_symbol,
                status=ProviderMappingStatus.LOCKED if provider_symbol_id else ProviderMappingStatus.UNRESOLVED,
                provider_symbol_id=provider_symbol_id,
            )
        )
    return tuple(rows)


def require_locked_portfolio_web_chart_mapping(rows: tuple[PortfolioProviderMappingRow, ...]) -> None:
    if not rows:
        raise CarverBlocked("portfolio web chart mapping rows are missing")
    for row in rows:
        if row.status is not ProviderMappingStatus.LOCKED or not row.provider_symbol_id:
            raise CarverBlocked(f"web chart mapping for {row.contract_code} {row.contract_month} is unresolved")


def require_locked_provider_mapping_set(mapping_set: PortfolioProviderMappingSet) -> None:
    mapping_set.validate()


def portfolio_conformance_from_daily_bars(
    portfolio: PortfolioSpec,
    daily_bars: dict[str, CompletedDailyMarketBar],
    annual_risk_estimates: dict[str, TimedValue],
    fx_rates: dict[str, TimedValue],
    rounding_policy: RoundingPolicy = RoundingPolicy.NEAREST,
) -> dict[str, SizingResult]:
    portfolio.validate()
    expected_codes = {leg.code for leg in portfolio.legs}
    if set(daily_bars) != expected_codes:
        raise CarverBlocked("portfolio daily bars must exactly match portfolio legs")
    if set(annual_risk_estimates) != expected_codes:
        raise CarverBlocked("portfolio risk estimates must exactly match portfolio legs")
    if set(fx_rates) != expected_codes:
        raise CarverBlocked("portfolio FX rates must exactly match portfolio legs")

    timestamps = {daily_bars[code].timestamp for code in expected_codes}
    if len(timestamps) != 1:
        raise CarverBlocked("portfolio daily bars must share one completed date")
    as_of = next(iter(timestamps))

    market_inputs: dict[str, LegMarketInput] = {}
    for leg in portfolio.legs:
        bar = daily_bars[leg.code]
        bar.validate()
        if bar.contract != leg.contract:
            raise CarverBlocked("portfolio daily bar contract does not match portfolio leg")
        risk = annual_risk_estimates[leg.code]
        fx = fx_rates[leg.code]
        if risk.as_of != as_of or fx.as_of != as_of:
            raise CarverBlocked("portfolio risk and FX timestamps must align to completed date")
        market_inputs[leg.code] = LegMarketInput(
            current_held_price=TimedValue(bar.close, as_of),
            annual_risk_estimate=risk,
            fx_rate=fx,
            risk_estimate_prevalidated=True,
        )

    if portfolio.portfolio_id == "P01_RISK_PARITY_EXAMPLE":
        return p01_synthetic_conformance(
            portfolio,
            next(iter(daily_bars.values())).completed_bar,
            market_inputs,
            rounding_policy,
        )
    if portfolio.portfolio_id == "P02_ALL_WEATHER_EXAMPLE":
        return p02_synthetic_conformance(
            portfolio,
            next(iter(daily_bars.values())).completed_bar,
            market_inputs,
            rounding_policy,
        )
    raise CarverBlocked("portfolio conformance is locked only for P01/P02")


def _display_symbol(contract_code: str, contract_month: str) -> str:
    if len(contract_month) != 5 or contract_month[2] != "-":
        raise CarverBlocked("contract month must use MM-YY")
    month, year = contract_month.split("-")
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
        raise CarverBlocked("contract month has invalid display month")
    return f"{contract_code} {month_names[month]}{year}"

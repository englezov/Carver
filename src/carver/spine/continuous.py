from __future__ import annotations

from dataclasses import dataclass

from .daily_bars import CompletedDailyMarketBar
from .m0 import BackAdjustmentSpec, CostSourceSpec, RollRuleSpec, SessionCalendarSpec, CarverBlocked


@dataclass(frozen=True)
class ContinuousContractRuleSet:
    session_calendar: SessionCalendarSpec
    roll_rule: RollRuleSpec
    back_adjustment: BackAdjustmentSpec
    cost_source: CostSourceSpec

    def require_locked(self) -> None:
        self.session_calendar.require_locked()
        self.roll_rule.require_locked()
        self.back_adjustment.require_locked()
        self.cost_source.require_locked()


@dataclass(frozen=True)
class ContinuousSeriesRequest:
    rules: ContinuousContractRuleSet
    bars: tuple[CompletedDailyMarketBar, ...]

    def validate(self) -> None:
        if not self.bars:
            raise CarverBlocked("continuous series request requires completed daily bars")
        self.rules.require_locked()
        previous = None
        contract_code = self.bars[0].code
        for bar in self.bars:
            bar.validate()
            if bar.code != contract_code:
                raise CarverBlocked("continuous series request cannot mix contract codes")
            if previous is not None and bar.timestamp <= previous:
                raise CarverBlocked("continuous series bars must be strictly increasing")
            previous = bar.timestamp


def build_continuous_back_adjusted_series(request: ContinuousSeriesRequest) -> tuple[CompletedDailyMarketBar, ...]:
    request.validate()
    raise CarverBlocked("continuous roll/back-adjustment implementation requires a separately locked source rule artifact")

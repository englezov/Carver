"""First-spine machinery for synthetic conformance tests."""

from .m0 import (
    BackAdjustmentSpec,
    BarConvention,
    CarverBlocked,
    CompletedBar,
    ContractSpec,
    CostSourceSpec,
    LaneClass,
    RollRuleSpec,
    SessionCalendarSpec,
    SourceRulePlaceholder,
    SourceRuleStatus,
)
from .m1 import RoundingPolicy, SizingInput, SizingResult, TimedValue, size_contracts
from .m3 import PortfolioLeg, PortfolioSpec, p01_risk_parity, p02_all_weather
from .s03 import S03RiskConfig, S03RiskEstimate, SyntheticDailyPrice, estimate_s03_annual_risk

__all__ = [
    "BackAdjustmentSpec",
    "BarConvention",
    "CarverBlocked",
    "CompletedBar",
    "ContractSpec",
    "CostSourceSpec",
    "LaneClass",
    "PortfolioLeg",
    "PortfolioSpec",
    "RoundingPolicy",
    "RollRuleSpec",
    "S03RiskConfig",
    "S03RiskEstimate",
    "SessionCalendarSpec",
    "SourceRulePlaceholder",
    "SourceRuleStatus",
    "SyntheticDailyPrice",
    "SizingInput",
    "SizingResult",
    "TimedValue",
    "estimate_s03_annual_risk",
    "p01_risk_parity",
    "p02_all_weather",
    "size_contracts",
]

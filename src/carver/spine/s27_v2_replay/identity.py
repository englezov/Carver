from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .validation import require_hour_aligned_utc, require_integer, require_iso_date, require_text


@dataclass(frozen=True)
class ReplayIdentity:
    replay_id: str
    step_index: int
    strategy_id: str
    lane: str
    instrument: str
    raw_symbol: str
    session_id: str
    completed_trading_date: str
    decision_as_of_utc: datetime
    fill_as_of_utc: datetime

    def validate(self) -> None:
        require_text("S27 v2 replay id", self.replay_id)
        require_integer("S27 v2 step index", self.step_index)
        if self.step_index < 0:
            raise CarverBlocked("S27 v2 step index must be non-negative")
        if self.strategy_id != S27_V2_STRATEGY_ID:
            raise CarverBlocked("S27 v2 replay identity strategy id mismatch")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 replay identity lane must be SOURCE_NATIVE_FUTURES")
        if self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 replay identity instrument must be ZN")
        require_text("S27 v2 replay raw symbol", self.raw_symbol)
        require_text("S27 v2 replay session id", self.session_id)
        require_iso_date("S27 v2 replay completed trading date", self.completed_trading_date)
        require_hour_aligned_utc("S27 v2 decision as-of", self.decision_as_of_utc)
        require_hour_aligned_utc("S27 v2 fill as-of", self.fill_as_of_utc)
        if self.fill_as_of_utc <= self.decision_as_of_utc:
            raise CarverBlocked("S27 v2 fill time must follow decision time")

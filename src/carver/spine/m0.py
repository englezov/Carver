from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class CarverBlocked(ValueError):
    """Raised when a source-native gate fails closed."""


class LaneClass(StrEnum):
    SOURCE_NATIVE_FUTURES = "SOURCE_NATIVE_FUTURES"
    CFD_DIRECT = "CFD_DIRECT"
    CFD_ADAPTER = "CFD_ADAPTER"


class BarConvention(StrEnum):
    DAILY_COMPLETED = "DAILY_COMPLETED"


@dataclass(frozen=True)
class CompletedBar:
    timestamp: datetime
    convention: BarConvention = BarConvention.DAILY_COMPLETED
    is_complete: bool = True

    def validate(self) -> None:
        if not self.is_complete:
            raise CarverBlocked("bar is not completed")
        if self.convention is not BarConvention.DAILY_COMPLETED:
            raise CarverBlocked("only completed daily bars are authorized in this gate")
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise CarverBlocked("completed daily bar timestamp must be timezone-aware")
        if (
            self.timestamp.hour
            or self.timestamp.minute
            or self.timestamp.second
            or self.timestamp.microsecond
        ):
            raise CarverBlocked("completed daily bar timestamp must be date-aligned")


def require_source_native(lane_class: LaneClass) -> None:
    if lane_class is not LaneClass.SOURCE_NATIVE_FUTURES:
        raise CarverBlocked("lane class must be SOURCE_NATIVE_FUTURES")

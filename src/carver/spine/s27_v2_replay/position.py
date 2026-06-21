from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .identity import ReplayIdentity
from .validation import require_hash, require_integer, require_text


@dataclass(frozen=True)
class DesiredPositionLedgerRow:
    identity: ReplayIdentity
    forecast_hash: str
    rounding_policy: str
    desired_unrounded_position_hash: str
    desired_rounded_position: int
    desired_position_hash: str

    def validate(self) -> None:
        self.identity.validate()
        require_hash("S27 v2 desired-position forecast hash", self.forecast_hash)
        require_text("S27 v2 desired-position rounding policy", self.rounding_policy)
        if self.rounding_policy != "NEAREST":
            raise CarverBlocked("S27 v2 desired-position rounding policy must be NEAREST")
        require_hash("S27 v2 desired unrounded position hash", self.desired_unrounded_position_hash)
        require_integer("S27 v2 desired rounded position", self.desired_rounded_position)
        require_hash("S27 v2 desired-position hash", self.desired_position_hash)

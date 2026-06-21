from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from ..m0 import CarverBlocked
from .constants import BLOCKED_OVERNIGHT, BLOCKED_ROLL_BRIDGE, BLOCKED_WORKING_LIMIT_LIFECYCLE
from .identity import ReplayIdentity
from .validation import require_hash, require_integer, require_text


@dataclass(frozen=True)
class WorkingOrderTransitionLedgerRow:
    identity: ReplayIdentity
    starting_working_state_hash: str
    starting_position: int
    order_plan_hash: str
    previous_step_hash_or_initial_state_hash: str
    transition_kind: str
    one_hour_lag_proof_hash: str
    next_completed_hourly_fill_row_hash: str
    fill_lag_reason_code: str
    session_gap_proof_hash: str | None
    session_transition_row_hash: str
    raw_symbol_session_date_continuity_proof_hash: str
    roll_boundary_row_hash: str | None
    overnight_recomputed_target_policy_hash: str | None
    ending_working_state_hash: str
    ending_position: int
    transition_hash: str

    def validate(self) -> None:
        try:
            self.identity.validate()
            require_hash("S27 v2 starting working-state hash", self.starting_working_state_hash)
            require_integer("S27 v2 starting position", self.starting_position)
            require_hash("S27 v2 transition order-plan hash", self.order_plan_hash)
            require_hash(
                "S27 v2 previous step or initial-state hash",
                self.previous_step_hash_or_initial_state_hash,
            )
            require_text("S27 v2 transition kind", self.transition_kind)
            if self.transition_kind not in (
                "NORMAL_ONE_HOUR_LAG",
                "EOD_OVERNIGHT_RECOMPUTE",
                "ROLL_BOUNDARY",
            ):
                raise CarverBlocked("S27 v2 transition kind is unresolved")
            require_hash("S27 v2 one-hour lag proof hash", self.one_hour_lag_proof_hash)
            require_hash("S27 v2 next completed hourly fill-row hash", self.next_completed_hourly_fill_row_hash)
            require_text("S27 v2 fill-lag reason code", self.fill_lag_reason_code)
            require_hash("S27 v2 session transition row hash", self.session_transition_row_hash)
            require_hash(
                "S27 v2 raw-symbol/session/date continuity proof hash",
                self.raw_symbol_session_date_continuity_proof_hash,
            )
            if self.transition_kind == "NORMAL_ONE_HOUR_LAG":
                if self.fill_lag_reason_code != "EXACT_NEXT_COMPLETED_HOURLY_ROW":
                    raise CarverBlocked("S27 v2 normal transition must use exact next completed hourly fill row")
                if self.identity.fill_as_of_utc - self.identity.decision_as_of_utc != timedelta(hours=1):
                    raise CarverBlocked("S27 v2 normal transition fill time must be exactly one hour after decision")
                if self.session_gap_proof_hash is not None:
                    raise CarverBlocked("S27 v2 normal transition must not carry session-gap proof")
                if self.roll_boundary_row_hash is not None or self.overnight_recomputed_target_policy_hash is not None:
                    raise CarverBlocked("S27 v2 normal transition must not carry roll or overnight policy hashes")
            elif self.transition_kind == "EOD_OVERNIGHT_RECOMPUTE":
                if self.fill_lag_reason_code != "SESSION_GAP_OVERNIGHT_NEXT_COMPLETED_HOURLY_ROW":
                    raise CarverBlocked("S27 v2 overnight transition must declare session-gap fill-lag reason")
                if self.session_gap_proof_hash is None:
                    raise CarverBlocked("S27 v2 overnight transition requires session-gap proof")
                require_hash("S27 v2 overnight session-gap proof hash", self.session_gap_proof_hash)
                if self.roll_boundary_row_hash is not None:
                    raise CarverBlocked("S27 v2 overnight transition must not carry roll-boundary row hash")
                if self.overnight_recomputed_target_policy_hash is None:
                    raise CarverBlocked("S27 v2 overnight transition requires recomputed-target policy hash")
                require_hash(
                    "S27 v2 overnight recomputed-target policy hash",
                    self.overnight_recomputed_target_policy_hash,
                )
            elif self.transition_kind == "ROLL_BOUNDARY":
                if self.fill_lag_reason_code != "ROLL_SESSION_GAP_NEXT_COMPLETED_HOURLY_ROW":
                    raise CarverBlocked("S27 v2 roll transition must declare roll/session-gap fill-lag reason")
                if self.session_gap_proof_hash is None:
                    raise CarverBlocked("S27 v2 roll transition requires session-gap proof")
                require_hash("S27 v2 roll session-gap proof hash", self.session_gap_proof_hash)
                if self.overnight_recomputed_target_policy_hash is not None:
                    raise CarverBlocked("S27 v2 roll transition must not carry overnight recompute policy hash")
                if self.roll_boundary_row_hash is None:
                    raise CarverBlocked("S27 v2 roll transition requires roll-boundary row hash")
                require_hash("S27 v2 roll-boundary row hash", self.roll_boundary_row_hash)
            require_hash("S27 v2 ending working-state hash", self.ending_working_state_hash)
            require_integer("S27 v2 ending position", self.ending_position)
            require_hash("S27 v2 transition hash", self.transition_hash)
        except CarverBlocked as exc:
            raise CarverBlocked(
                f"{BLOCKED_WORKING_LIMIT_LIFECYCLE}; {BLOCKED_OVERNIGHT}; {BLOCKED_ROLL_BRIDGE}"
            ) from exc

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .fast_segment_emitter import FastSegmentArtifacts
from .fast_execution_state import FastExecutionStateVerification
from .local_replay import canonical_sha256
from .test_incremental_runner import (
    AUTHORIZATION,
    NON_AUTHORIZATIONS,
    IncrementalSegmentBundle,
    _write_json,
)


STATUS = "LOCAL_2023_TEST_FAST_SEGMENT_TBBO_REQUIREMENTS_DERIVED_NOT_PROVIDER_NOT_RESULT"
PLANNER_MODE = "DERIVE_REQUIREMENTS_FROM_VALIDATED_SEGMENT_AND_TERMINAL_BLOCKER_NOT_LEGACY_LEDGER"
MISSING_STATUS = "REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE"
SUPPORTED_STATUS = "MARKET_ORDER_TBBO_EVIDENCE_ALREADY_BOUND_IN_SEGMENT_NOT_PROVIDER"


@dataclass(frozen=True)
class FastTBBORequirementRow:
    row_index: int
    decision_timestamp_utc: str
    fill_candidate_timestamp_utc: str
    raw_symbol: str
    order_side: str
    order_quantity: int
    requirement_status: str
    source_ledger: str
    source_row_hash: str
    row_hash: str

    def validate(self) -> None:
        _validate_timestamp(self.decision_timestamp_utc, "decision timestamp")
        _validate_timestamp(self.fill_candidate_timestamp_utc, "fill candidate timestamp")
        if self.order_side not in {"BUY", "SELL"}:
            raise CarverBlocked("S27 v2 fast TBBO planner order side drift")
        if self.order_quantity <= 0:
            raise CarverBlocked("S27 v2 fast TBBO planner order quantity drift")
        if self.requirement_status not in {MISSING_STATUS, SUPPORTED_STATUS}:
            raise CarverBlocked("S27 v2 fast TBBO planner requirement status drift")
        _validate_hash(self.source_row_hash, "source row")
        if self.row_hash != canonical_sha256(_row_payload(self)):
            raise CarverBlocked("S27 v2 fast TBBO planner requirement row hash drift")


@dataclass(frozen=True)
class FastTBBORequirementPlan:
    status: str
    authorization_label: str
    planner_mode: str
    segment_bundle_hash: str
    fast_segment_artifacts_hash: str
    execution_state_verification_hash: str
    supported_market_order_count: int
    missing_requirement_count: int
    first_missing_row_index: int | None
    last_missing_row_index: int | None
    requirement_rows: tuple[FastTBBORequirementRow, ...]
    plan_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(
        self,
        *,
        artifacts: FastSegmentArtifacts,
        segment_bundle: IncrementalSegmentBundle,
        execution_state_verification: FastExecutionStateVerification,
    ) -> None:
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 fast TBBO planner status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast TBBO planner authorization mismatch")
        if self.planner_mode != PLANNER_MODE:
            raise CarverBlocked("S27 v2 fast TBBO planner mode drift")
        if self.segment_bundle_hash != segment_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast TBBO planner segment binding drift")
        if self.fast_segment_artifacts_hash != artifacts.bundle_hash:
            raise CarverBlocked("S27 v2 fast TBBO planner artifacts binding drift")
        if self.execution_state_verification_hash != execution_state_verification.verification_hash:
            raise CarverBlocked("S27 v2 fast TBBO planner execution-state binding drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast TBBO planner non-authorizations drift")
        artifacts.validate(segment_bundle=segment_bundle, execution_state_verification=execution_state_verification)
        missing = [row for row in self.requirement_rows if row.requirement_status == MISSING_STATUS]
        if len(missing) != self.missing_requirement_count:
            raise CarverBlocked("S27 v2 fast TBBO planner missing requirement count drift")
        if self.first_missing_row_index != (missing[0].row_index if missing else None):
            raise CarverBlocked("S27 v2 fast TBBO planner first missing row drift")
        if self.last_missing_row_index != (missing[-1].row_index if missing else None):
            raise CarverBlocked("S27 v2 fast TBBO planner last missing row drift")
        for row in self.requirement_rows:
            row.validate()
        expected = _derive_plan(
            artifacts=artifacts,
            segment_bundle=segment_bundle,
            execution_state_verification=execution_state_verification,
        )
        if _plan_payload(self) != _plan_payload(expected):
            raise CarverBlocked("S27 v2 fast TBBO planner active requirement derivation drift")
        if self.plan_hash != canonical_sha256(_plan_payload(self)):
            raise CarverBlocked("S27 v2 fast TBBO planner hash drift")


def build_fast_tbbo_requirement_plan(
    *,
    artifacts: FastSegmentArtifacts,
    segment_bundle: IncrementalSegmentBundle,
    execution_state_verification: FastExecutionStateVerification,
) -> FastTBBORequirementPlan:
    artifacts.validate(segment_bundle=segment_bundle, execution_state_verification=execution_state_verification)
    plan = _derive_plan(
        artifacts=artifacts,
        segment_bundle=segment_bundle,
        execution_state_verification=execution_state_verification,
    )
    plan.validate(
        artifacts=artifacts,
        segment_bundle=segment_bundle,
        execution_state_verification=execution_state_verification,
    )
    return plan


def write_fast_tbbo_requirement_plan(
    plan: FastTBBORequirementPlan,
    *,
    artifacts: FastSegmentArtifacts,
    segment_bundle: IncrementalSegmentBundle,
    execution_state_verification: FastExecutionStateVerification,
    output_root: Path | str,
) -> None:
    plan.validate(
        artifacts=artifacts,
        segment_bundle=segment_bundle,
        execution_state_verification=execution_state_verification,
    )
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    _write_json(root / "fast_tbbo_requirement_plan.json", _plan_public_payload(plan))
    rows = [asdict(row) for row in plan.requirement_rows]
    if not rows:
        (root / "fast_tbbo_requirements.csv").write_text("", encoding="ascii")
        return
    with (root / "fast_tbbo_requirements.csv").open("w", encoding="ascii", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _derive_plan(
    *,
    artifacts: FastSegmentArtifacts,
    segment_bundle: IncrementalSegmentBundle,
    execution_state_verification: FastExecutionStateVerification,
) -> FastTBBORequirementPlan:
    requirement_rows: list[FastTBBORequirementRow] = []
    supported_market_count = 0

    no_market_by_index = _rows_by_index(artifacts.segment_rows_by_ledger["no_market_order_ledger.csv"])
    market_by_index = _rows_by_index(artifacts.segment_rows_by_ledger["market_order_ledger.csv"])
    market_fill_by_index = _rows_by_index(artifacts.segment_rows_by_ledger["market_fill_metadata_ledger.csv"])
    cost_by_index = _rows_by_index(artifacts.segment_rows_by_ledger["cost_ledger.csv"])
    for row_index, no_market in sorted(no_market_by_index.items()):
        if no_market.get("market_order_required") != "TRUE":
            continue
        market = _required(market_by_index, row_index, "market order")
        market_fill = _required(market_fill_by_index, row_index, "market fill metadata")
        cost = _required(cost_by_index, row_index, "cost")
        if cost.get("tbbo_selected_spread_row_hash") in {"", "MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE", "NOT_APPLICABLE"}:
            requirement_rows.append(
                _requirement_row(
                    row_index=row_index,
                    decision_timestamp_utc=market["decision_timestamp_utc"],
                    fill_candidate_timestamp_utc=market_fill["fill_timestamp_utc"],
                    raw_symbol=market["raw_symbol"],
                    order_side=market["order_side"],
                    order_quantity=int(market["order_quantity"]),
                    requirement_status=MISSING_STATUS,
                    source_ledger="cost_ledger.csv",
                    source_row_hash=cost["row_hash"],
                )
            )
        else:
            supported_market_count += 1

    terminal = artifacts.terminal_fail_row
    if terminal.get("market_order_required") == "TRUE" and terminal.get("market_spread_cost_status") == (
        "FAIL_CLOSED_BOUNDED_TBBO_SPREAD_EVIDENCE_REQUIRED_FOR_MARKET_ORDER"
    ):
        requirement_rows.append(
            _requirement_row(
                row_index=int(terminal["row_index"]),
                decision_timestamp_utc=terminal["decision_timestamp_utc"],
                fill_candidate_timestamp_utc=terminal["fill_candidate_timestamp_utc"],
                raw_symbol=terminal["raw_symbol"],
                order_side=terminal["order_side"],
                order_quantity=abs(int(terminal["position_change_contracts"])),
                requirement_status=MISSING_STATUS,
                source_ledger="fail_closed_ledger.csv",
                source_row_hash=terminal["row_hash"],
            )
        )

    missing = [row for row in requirement_rows if row.requirement_status == MISSING_STATUS]
    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "planner_mode": PLANNER_MODE,
        "segment_bundle_hash": segment_bundle.bundle_hash,
        "fast_segment_artifacts_hash": artifacts.bundle_hash,
        "execution_state_verification_hash": execution_state_verification.verification_hash,
        "supported_market_order_count": supported_market_count,
        "missing_requirement_count": len(missing),
        "first_missing_row_index": missing[0].row_index if missing else None,
        "last_missing_row_index": missing[-1].row_index if missing else None,
        "requirement_rows": tuple(requirement_rows),
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    plan = FastTBBORequirementPlan(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        planner_mode=PLANNER_MODE,
        segment_bundle_hash=segment_bundle.bundle_hash,
        fast_segment_artifacts_hash=artifacts.bundle_hash,
        execution_state_verification_hash=execution_state_verification.verification_hash,
        supported_market_order_count=supported_market_count,
        missing_requirement_count=len(missing),
        first_missing_row_index=missing[0].row_index if missing else None,
        last_missing_row_index=missing[-1].row_index if missing else None,
        requirement_rows=tuple(requirement_rows),
        plan_hash=canonical_sha256(payload),
    )
    return plan


def _requirement_row(
    *,
    row_index: int,
    decision_timestamp_utc: str,
    fill_candidate_timestamp_utc: str,
    raw_symbol: str,
    order_side: str,
    order_quantity: int,
    requirement_status: str,
    source_ledger: str,
    source_row_hash: str,
) -> FastTBBORequirementRow:
    payload = {
        "row_index": row_index,
        "decision_timestamp_utc": decision_timestamp_utc,
        "fill_candidate_timestamp_utc": fill_candidate_timestamp_utc,
        "raw_symbol": raw_symbol,
        "order_side": order_side,
        "order_quantity": order_quantity,
        "requirement_status": requirement_status,
        "source_ledger": source_ledger,
        "source_row_hash": source_row_hash,
    }
    return FastTBBORequirementRow(row_hash=canonical_sha256(payload), **payload)


def _rows_by_index(rows: tuple[Mapping[str, str], ...]) -> dict[int, Mapping[str, str]]:
    return {int(row["row_index"]): row for row in rows}


def _required(rows: Mapping[int, Mapping[str, str]], row_index: int, label: str) -> Mapping[str, str]:
    row = rows.get(row_index)
    if row is None:
        raise CarverBlocked(f"S27 v2 fast TBBO planner missing {label} row {row_index}")
    return row


def _plan_public_payload(plan: FastTBBORequirementPlan) -> dict[str, Any]:
    return asdict(plan)


def _plan_payload(plan: FastTBBORequirementPlan) -> dict[str, Any]:
    data = asdict(plan)
    data.pop("plan_hash", None)
    return data


def _row_payload(row: FastTBBORequirementRow) -> dict[str, Any]:
    data = asdict(row)
    data.pop("row_hash", None)
    return data


def _validate_timestamp(value: str, label: str) -> None:
    if not value.startswith("2023-"):
        raise CarverBlocked(f"S27 v2 fast TBBO planner {label} outside 2023 TEST window")


def _validate_hash(value: str, label: str) -> None:
    if len(value) != 64 or any(char not in "0123456789abcdefABCDEF" for char in value):
        raise CarverBlocked(f"S27 v2 fast TBBO planner invalid hash for {label}")

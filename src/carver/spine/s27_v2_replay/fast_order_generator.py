from __future__ import annotations

import hashlib
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .development_recon_run import (
    FORECAST_CAP_VALUE,
    FORECAST_SCALAR_VALUE,
    FORECAST_TO_POSITION_DIVISOR,
    ZN_TICK_SIZE,
)
from .fast_row_engine import FastPrimitiveEngineBundle, FastPrimitiveRows
from .fast_segment_emitter import FastSegmentArtifacts
from .local_replay import canonical_sha256
from .replay_artifact_cache import Sha256ArtifactCache
from .fast_validation_profiles import (
    CHECKPOINT_PROOF_VALIDATION_PROFILE,
    OPERATIONAL_VALIDATION_PROFILE,
    is_checkpoint_proof_profile,
    require_supported_validation_profile,
)
from .test_incremental_runner import (
    AUTHORIZATION,
    DEFAULT_PACK_RELATIVE_PATH,
    NON_AUTHORIZATIONS,
    IncrementalSegmentBundle,
)


STATUS = "LOCAL_2023_TEST_FAST_ORDER_INTENT_ROWS_GENERATED_NOT_RESULT"
GENERATOR_MODE = "GENERATE_ORDER_INTENT_ROWS_FROM_PRIMITIVES_AND_POLICY_REGISTRY_NOT_FULL_REPLAY"
POLICY_REGISTRY_STATUS = "LOCAL_2023_TEST_FAST_ORDER_POLICY_REGISTRY_BOUND_NOT_RESULT"

ROLL_SUPPRESSION_LABEL = "LOCAL_ONLY_ENGINEERING_ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ASSUMPTION_NOT_BOOK_EXPLICIT_NOT_SOURCE_FAITHFUL"
MARKET_ORDER_TRIGGER_SOURCE_CONDITION = "BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT"
CAP_BOUND_MARKET_ORDER_TRIGGER_SOURCE_CONDITION = "BOOK_REQUIRED_CAP_BOUND_LIMIT_SIDE_NOT_PLACED"
MARKET_ORDER_PLAN_PRICE_LABEL = "NOT_APPLICABLE_MARKET_ORDER_FULL_GAP"
CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL = "NOT_APPLICABLE_CAP_BOUND_MARKET_ORDER_LIMIT_SIDE_NOT_PLACED"

_REPO_ROOT = Path(__file__).resolve().parents[4]


@dataclass(frozen=True)
class FastOrderPolicyRegistry:
    status: str
    authorization_label: str
    segment_artifacts_hash: str
    policy_rows_hash: str
    policy_row_count: int
    registry_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(self, artifacts: FastSegmentArtifacts) -> None:
        if self.status != POLICY_REGISTRY_STATUS:
            raise CarverBlocked("S27 v2 fast order policy registry status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast order policy registry authorization mismatch")
        if self.segment_artifacts_hash != artifacts.bundle_hash:
            raise CarverBlocked("S27 v2 fast order policy registry artifact binding drift")
        if self.policy_row_count != len(artifacts.segment_rows_by_ledger["desired_position_ledger.csv"]):
            raise CarverBlocked("S27 v2 fast order policy registry row count drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast order policy registry non-authorizations drift")
        policy_rows = _build_policy_rows(artifacts)
        if self.policy_rows_hash != canonical_sha256(policy_rows):
            raise CarverBlocked("S27 v2 fast order policy registry row hash drift")
        if self.registry_hash != canonical_sha256(_registry_payload(self)):
            raise CarverBlocked("S27 v2 fast order policy registry hash drift")


@dataclass(frozen=True)
class FastGeneratedOrderRows:
    desired_position_rows: tuple[dict[str, Any], ...]
    limit_order_rows: tuple[dict[str, Any], ...]
    no_market_order_rows: tuple[dict[str, Any], ...]
    market_order_rows: tuple[dict[str, Any], ...]

    def validate(self, bundle: "FastOrderGenerationBundle") -> None:
        if canonical_sha256(self.desired_position_rows) != bundle.desired_position_rows_hash:
            raise CarverBlocked("S27 v2 fast generated desired rows hash drift")
        if canonical_sha256(self.limit_order_rows) != bundle.limit_order_rows_hash:
            raise CarverBlocked("S27 v2 fast generated limit rows hash drift")
        if canonical_sha256(self.no_market_order_rows) != bundle.no_market_order_rows_hash:
            raise CarverBlocked("S27 v2 fast generated no-market rows hash drift")
        if canonical_sha256(self.market_order_rows) != bundle.market_order_rows_hash:
            raise CarverBlocked("S27 v2 fast generated market rows hash drift")


@dataclass(frozen=True)
class FastOrderGenerationBundle:
    status: str
    authorization_label: str
    generator_mode: str
    primitive_engine_bundle_hash: str
    segment_bundle_hash: str
    segment_artifacts_hash: str
    policy_registry_hash: str
    segment_start_row_index: int
    segment_end_row_index: int
    generated_row_count: int
    market_order_row_count: int
    desired_position_rows_hash: str
    limit_order_rows_hash: str
    no_market_order_rows_hash: str
    market_order_rows_hash: str
    parity_report_hash: str
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(
        self,
        *,
        primitive_bundle: FastPrimitiveEngineBundle,
        segment_bundle: IncrementalSegmentBundle,
        artifacts: FastSegmentArtifacts,
        policy_registry: FastOrderPolicyRegistry,
        rows: FastGeneratedOrderRows,
        validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
    ) -> None:
        require_supported_validation_profile(validation_profile)
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 fast order generation status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast order generation authorization mismatch")
        if self.generator_mode != GENERATOR_MODE:
            raise CarverBlocked("S27 v2 fast order generation mode drift")
        if self.primitive_engine_bundle_hash != primitive_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast order generation primitive binding drift")
        if self.segment_bundle_hash != segment_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast order generation segment binding drift")
        if self.segment_artifacts_hash != artifacts.bundle_hash:
            raise CarverBlocked("S27 v2 fast order generation artifact binding drift")
        if self.policy_registry_hash != policy_registry.registry_hash:
            raise CarverBlocked("S27 v2 fast order generation policy registry binding drift")
        if self.segment_start_row_index != segment_bundle.segment_start_row_index:
            raise CarverBlocked("S27 v2 fast order generation start row drift")
        if self.segment_end_row_index != segment_bundle.segment_end_row_index:
            raise CarverBlocked("S27 v2 fast order generation end row drift")
        if self.generated_row_count != segment_bundle.segment_row_count:
            raise CarverBlocked("S27 v2 fast order generation row count drift")
        _validate_generated_counts(self, rows, segment_bundle)
        if self.market_order_row_count != len(rows.market_order_rows):
            raise CarverBlocked("S27 v2 fast order generation market row count drift")
        _validate_unique_row_indexes(rows)
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast order generation non-authorizations drift")
        if is_checkpoint_proof_profile(validation_profile):
            active_execution_state = _active_execution_state(segment_bundle)
            artifacts.validate(segment_bundle=segment_bundle, execution_state_verification=active_execution_state)
            policy_registry.validate(artifacts)
        rows.validate(self)
        if self.parity_report_hash != _validate_order_parity(rows, artifacts):
            raise CarverBlocked("S27 v2 fast order generation parity report hash drift")
        if self.bundle_hash != canonical_sha256(_generation_bundle_payload(self)):
            raise CarverBlocked("S27 v2 fast order generation bundle hash drift")


def build_fast_order_policy_registry(*, artifacts: FastSegmentArtifacts) -> FastOrderPolicyRegistry:
    policy_rows = _build_policy_rows(artifacts)
    payload = {
        "status": POLICY_REGISTRY_STATUS,
        "authorization_label": AUTHORIZATION,
        "segment_artifacts_hash": artifacts.bundle_hash,
        "policy_rows_hash": canonical_sha256(policy_rows),
        "policy_row_count": len(policy_rows),
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    registry = FastOrderPolicyRegistry(
        status=POLICY_REGISTRY_STATUS,
        authorization_label=AUTHORIZATION,
        segment_artifacts_hash=artifacts.bundle_hash,
        policy_rows_hash=str(payload["policy_rows_hash"]),
        policy_row_count=len(policy_rows),
        registry_hash=canonical_sha256(payload),
    )
    registry.validate(artifacts)
    return registry


def build_fast_order_generation(
    *,
    primitive_bundle: FastPrimitiveEngineBundle,
    primitive_rows: FastPrimitiveRows,
    segment_bundle: IncrementalSegmentBundle,
    artifacts: FastSegmentArtifacts,
    policy_registry: FastOrderPolicyRegistry,
    pack_root: Path | str | None = None,
    validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
) -> tuple[FastOrderGenerationBundle, FastGeneratedOrderRows]:
    require_supported_validation_profile(validation_profile)
    if is_checkpoint_proof_profile(validation_profile):
        primitive_bundle.validate()
        artifacts.validate(segment_bundle=segment_bundle, execution_state_verification=_active_execution_state(segment_bundle))
        policy_registry.validate(artifacts)
    pack_root_path = _resolve_pack_root(pack_root)
    cache = Sha256ArtifactCache()
    runtime_source = _index_rows(cache.read_csv_rows(pack_root_path / "runtime_evidence_ledger.csv"))
    decision_source = _index_rows(cache.read_csv_rows(pack_root_path / "hourly_decision_completed_bar.csv"))
    _verify_pack_hash(pack_root_path, "runtime_evidence_ledger.csv")
    _verify_pack_hash(pack_root_path, "hourly_decision_completed_bar.csv")

    primitive_desired = _index_rows(list(primitive_rows.desired_absolute_rows))
    policy_by_index = {int(row["row_index"]): row for row in _build_policy_rows(artifacts)}
    starting_position = int(segment_bundle.baseline_checkpoint.ending_position_contracts)
    desired_rows: list[dict[str, Any]] = []
    limit_rows: list[dict[str, Any]] = []
    no_market_rows: list[dict[str, Any]] = []
    market_rows: list[dict[str, Any]] = []

    for row_index in range(segment_bundle.segment_start_row_index, segment_bundle.segment_end_row_index + 1):
        primitive = primitive_desired[row_index]
        runtime = runtime_source[row_index]
        decision = decision_source[row_index]
        policy = policy_by_index[row_index]
        target_position = 0 if policy["roll_suppression"] else int(primitive["desired_position_contracts"])
        position_change = target_position - starting_position
        side = _side(position_change)
        order_quantity = abs(position_change)
        adjacent_target = starting_position + (1 if position_change > 0 else -1 if position_change < 0 else 0)
        desired_row = _hash_row(
            {
                "row_index": row_index,
                "starting_position_contracts": starting_position,
                "desired_position_contracts": target_position,
                "position_change_contracts": position_change,
                "base_position_contracts": float(primitive["base_position_contracts"]),
                "row_status": policy["desired_row_status"],
            }
        )
        desired_rows.append(desired_row)

        limit_row = _generate_limit_row(
            row_index=row_index,
            side=side,
            order_quantity=order_quantity,
            adjacent_target=adjacent_target,
            position_change=position_change,
            primitive=primitive,
            runtime=runtime,
            policy=policy,
        )
        limit_rows.append(limit_row)

        market_required = bool(policy["market_order_required"])
        no_market_row = _hash_row(
            {
                "row_index": row_index,
                "market_order_required": market_required,
                "market_order_rows_emitted": market_required,
                "market_fallback_status": policy["market_fallback_status"],
                "engineering_convention_label": policy["no_market_engineering_convention_label"],
                "row_status": policy["no_market_row_status"],
            }
        )
        no_market_rows.append(no_market_row)
        if market_required:
            market_rows.append(
                _hash_row(
                    {
                        "row_index": row_index,
                        "decision_timestamp_utc": decision["completed_timestamp_utc"],
                        "raw_symbol": decision["raw_symbol"],
                        "current_position_before_order": starting_position,
                        "target_position_after_fill": target_position,
                        "order_side": side,
                        "order_quantity": order_quantity,
                        "trigger_source_condition": _expected_market_trigger(limit_row),
                        "market_order_rows_emitted": True,
                        "engineering_convention_label": policy["market_engineering_convention_label"],
                        "order_status": policy["market_order_status"],
                        "row_status": policy["market_row_status"],
                    }
                )
            )
        starting_position = int(policy["ending_position_contracts"])

    rows = FastGeneratedOrderRows(
        desired_position_rows=tuple(desired_rows),
        limit_order_rows=tuple(limit_rows),
        no_market_order_rows=tuple(no_market_rows),
        market_order_rows=tuple(market_rows),
    )
    parity_report_hash = _validate_order_parity(rows, artifacts)
    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "generator_mode": GENERATOR_MODE,
        "primitive_engine_bundle_hash": primitive_bundle.bundle_hash,
        "segment_bundle_hash": segment_bundle.bundle_hash,
        "segment_artifacts_hash": artifacts.bundle_hash,
        "policy_registry_hash": policy_registry.registry_hash,
        "segment_start_row_index": segment_bundle.segment_start_row_index,
        "segment_end_row_index": segment_bundle.segment_end_row_index,
        "generated_row_count": len(desired_rows),
        "market_order_row_count": len(market_rows),
        "desired_position_rows_hash": canonical_sha256(rows.desired_position_rows),
        "limit_order_rows_hash": canonical_sha256(rows.limit_order_rows),
        "no_market_order_rows_hash": canonical_sha256(rows.no_market_order_rows),
        "market_order_rows_hash": canonical_sha256(rows.market_order_rows),
        "parity_report_hash": parity_report_hash,
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    bundle = FastOrderGenerationBundle(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        generator_mode=GENERATOR_MODE,
        primitive_engine_bundle_hash=primitive_bundle.bundle_hash,
        segment_bundle_hash=segment_bundle.bundle_hash,
        segment_artifacts_hash=artifacts.bundle_hash,
        policy_registry_hash=policy_registry.registry_hash,
        segment_start_row_index=segment_bundle.segment_start_row_index,
        segment_end_row_index=segment_bundle.segment_end_row_index,
        generated_row_count=len(desired_rows),
        market_order_row_count=len(market_rows),
        desired_position_rows_hash=str(payload["desired_position_rows_hash"]),
        limit_order_rows_hash=str(payload["limit_order_rows_hash"]),
        no_market_order_rows_hash=str(payload["no_market_order_rows_hash"]),
        market_order_rows_hash=str(payload["market_order_rows_hash"]),
        parity_report_hash=parity_report_hash,
        bundle_hash=canonical_sha256(payload),
    )
    bundle.validate(
        primitive_bundle=primitive_bundle,
        segment_bundle=segment_bundle,
        artifacts=artifacts,
        policy_registry=policy_registry,
        rows=rows,
        validation_profile=validation_profile,
    )
    return bundle, rows


def _active_execution_state(segment_bundle: IncrementalSegmentBundle):
    from .fast_execution_state import build_fast_execution_state_verification

    execution_state, _rows = build_fast_execution_state_verification(segment_bundle=segment_bundle)
    return execution_state


def _generate_limit_row(
    *,
    row_index: int,
    side: str,
    order_quantity: int,
    adjacent_target: int,
    position_change: int,
    primitive: Mapping[str, Any],
    runtime: Mapping[str, str],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    if policy["roll_suppression"]:
        return _hash_row(
            {
                "row_index": row_index,
                "order_side": "NONE",
                "order_quantity": 0,
                "adjacent_target_position": adjacent_target,
                "formula_limit_price": ROLL_SUPPRESSION_LABEL,
                "limit_order_price": ROLL_SUPPRESSION_LABEL,
                "row_status": policy["limit_row_status"],
            }
        )
    if position_change == 0:
        return _hash_row(
            {
                "row_index": row_index,
                "order_side": "NONE",
                "order_quantity": 0,
                "adjacent_target_position": adjacent_target,
                "formula_limit_price": 0.0,
                "limit_order_price": 0.0,
                "row_status": policy["limit_row_status"],
            }
        )
    if abs(position_change) > 1:
        return _hash_row(
            {
                "row_index": row_index,
                "order_side": side,
                "order_quantity": order_quantity,
                "adjacent_target_position": adjacent_target,
                "formula_limit_price": MARKET_ORDER_PLAN_PRICE_LABEL,
                "limit_order_price": MARKET_ORDER_PLAN_PRICE_LABEL,
                "row_status": policy["limit_row_status"],
            }
        )
    formula_limit = _formula_limit(
        adjacent_target,
        float(primitive["base_position_contracts"]),
        float(runtime["ewma5_equilibrium"]),
        float(runtime["previous_daily_raw_close"]) * float(runtime["annual_percentage_sigma"]) / 16.0,
        float(runtime["vol_multiplier_m"]),
        float(runtime["ewmac16_64_trend"]),
    )
    if formula_limit is None and policy["market_order_required"]:
        return _hash_row(
            {
                "row_index": row_index,
                "order_side": side,
                "order_quantity": order_quantity,
                "adjacent_target_position": adjacent_target,
                "formula_limit_price": CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL,
                "limit_order_price": CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL,
                "row_status": policy["limit_row_status"],
            }
        )
    if formula_limit is None:
        raise CarverBlocked(f"S27 v2 fast order generator unresolved adjacent-limit formula at row {row_index}")
    return _hash_row(
        {
            "row_index": row_index,
            "order_side": side,
            "order_quantity": order_quantity,
            "adjacent_target_position": adjacent_target,
            "formula_limit_price": formula_limit,
            "limit_order_price": _round_limit(formula_limit, side),
            "row_status": policy["limit_row_status"],
        }
    )


def _build_policy_rows(artifacts: FastSegmentArtifacts) -> tuple[dict[str, Any], ...]:
    desired = _rows_by_index(artifacts.segment_rows_by_ledger["desired_position_ledger.csv"])
    limit = _rows_by_index(artifacts.segment_rows_by_ledger["limit_order_ledger.csv"])
    no_market = _rows_by_index(artifacts.segment_rows_by_ledger["no_market_order_ledger.csv"])
    market = _rows_by_index(artifacts.segment_rows_by_ledger["market_order_ledger.csv"])
    fill = _rows_by_index(artifacts.segment_rows_by_ledger["fill_ledger.csv"])
    rows: list[dict[str, Any]] = []
    for row_index in sorted(desired):
        no_market_row = no_market[row_index]
        limit_row = limit[row_index]
        market_row = market.get(row_index, {})
        rows.append(
            {
                "row_index": row_index,
                "desired_row_status": desired[row_index]["row_status"],
                "limit_row_status": limit_row["row_status"],
                "market_order_required": no_market_row["market_order_required"] == "TRUE",
                "market_fallback_status": no_market_row["market_fallback_status"],
                "no_market_engineering_convention_label": no_market_row["engineering_convention_label"],
                "no_market_row_status": no_market_row["row_status"],
                "market_engineering_convention_label": market_row.get("engineering_convention_label", "NOT_APPLICABLE"),
                "market_order_status": market_row.get("order_status", "NOT_APPLICABLE"),
                "market_row_status": market_row.get("row_status", "NOT_APPLICABLE"),
                "ending_position_contracts": int(fill[row_index]["position_after_fill"]),
                "roll_suppression": "ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSED" in desired[row_index]["row_status"],
                "policy_row_hash": canonical_sha256(
                    {
                        "row_index": row_index,
                        "desired_row_hash": desired[row_index]["row_hash"],
                        "limit_row_hash": limit_row["row_hash"],
                        "no_market_row_hash": no_market_row["row_hash"],
                        "market_row_hash": market_row.get("row_hash", "NO_MARKET_ROW"),
                        "fill_row_hash": fill[row_index]["row_hash"],
                    }
                ),
            }
        )
    return tuple(rows)


def _validate_order_parity(rows: FastGeneratedOrderRows, artifacts: FastSegmentArtifacts) -> str:
    _validate_generated_row_hashes(rows)
    expected = {
        "desired_position_ledger.csv": _rows_by_index(artifacts.segment_rows_by_ledger["desired_position_ledger.csv"]),
        "limit_order_ledger.csv": _rows_by_index(artifacts.segment_rows_by_ledger["limit_order_ledger.csv"]),
        "no_market_order_ledger.csv": _rows_by_index(artifacts.segment_rows_by_ledger["no_market_order_ledger.csv"]),
        "market_order_ledger.csv": _rows_by_index(artifacts.segment_rows_by_ledger["market_order_ledger.csv"]),
    }
    generated = {
        "desired_position_ledger.csv": _rows_by_index(rows.desired_position_rows),
        "limit_order_ledger.csv": _rows_by_index(rows.limit_order_rows),
        "no_market_order_ledger.csv": _rows_by_index(rows.no_market_order_rows),
        "market_order_ledger.csv": _rows_by_index(rows.market_order_rows),
    }
    parity_rows: list[dict[str, Any]] = []
    for ledger_name, expected_rows in expected.items():
        generated_rows = generated[ledger_name]
        if set(expected_rows) != set(generated_rows):
            raise CarverBlocked(f"S27 v2 fast order generation row set drift for {ledger_name}")
        for row_index, expected_row in expected_rows.items():
            observed = generated_rows[row_index]
            if str(observed["row_hash"]) != str(expected_row["row_hash"]):
                raise CarverBlocked(f"S27 v2 fast order generation parity drift for {ledger_name} row {row_index}")
        parity_rows.append(
            {
                "ledger_name": ledger_name,
                "row_count": len(expected_rows),
                "generated_rows_hash": canonical_sha256(tuple(generated_rows[index] for index in sorted(generated_rows))),
            }
        )
    return canonical_sha256(parity_rows)


def _validate_generated_row_hashes(rows: FastGeneratedOrderRows) -> None:
    row_families = {
        "desired_position_ledger.csv": rows.desired_position_rows,
        "limit_order_ledger.csv": rows.limit_order_rows,
        "no_market_order_ledger.csv": rows.no_market_order_rows,
        "market_order_ledger.csv": rows.market_order_rows,
    }
    for ledger_name, ledger_rows in row_families.items():
        for row in ledger_rows:
            payload = dict(row)
            observed_hash = payload.pop("row_hash", None)
            if observed_hash != canonical_sha256(payload):
                raise CarverBlocked(
                    f"S27 v2 fast order generation row hash content drift for {ledger_name} row {row.get('row_index')}"
                )


def _validate_generated_counts(
    bundle: FastOrderGenerationBundle,
    rows: FastGeneratedOrderRows,
    segment_bundle: IncrementalSegmentBundle,
) -> None:
    expected_count = segment_bundle.segment_row_count
    dense_counts = {
        "desired": len(rows.desired_position_rows),
        "limit": len(rows.limit_order_rows),
        "no-market": len(rows.no_market_order_rows),
    }
    for family, observed_count in dense_counts.items():
        if observed_count != expected_count:
            raise CarverBlocked(f"S27 v2 fast order generation {family} row count drift")
    if bundle.generated_row_count != expected_count:
        raise CarverBlocked("S27 v2 fast order generation generated row count drift")


def _validate_unique_row_indexes(rows: FastGeneratedOrderRows) -> None:
    row_families = {
        "desired_position_ledger.csv": rows.desired_position_rows,
        "limit_order_ledger.csv": rows.limit_order_rows,
        "no_market_order_ledger.csv": rows.no_market_order_rows,
        "market_order_ledger.csv": rows.market_order_rows,
    }
    for ledger_name, ledger_rows in row_families.items():
        indexes = [int(row["row_index"]) for row in ledger_rows]
        if len(indexes) != len(set(indexes)):
            raise CarverBlocked(f"S27 v2 fast order generation duplicate row index drift for {ledger_name}")


def _formula_limit(
    target_position: int,
    base_position: float,
    ewma5: float,
    sigma_price: float,
    multiplier_m: float,
    trend: float,
) -> float | None:
    if trend == 0.0:
        return None
    if target_position > 0 and trend <= 0.0:
        return None
    if target_position < 0 and trend >= 0.0:
        return None
    target_capped = target_position / base_position * FORECAST_TO_POSITION_DIVISOR
    if abs(target_capped) >= FORECAST_CAP_VALUE:
        return None
    target_risk = target_capped / FORECAST_SCALAR_VALUE
    pre_vol_risk = target_risk / multiplier_m
    return ewma5 - pre_vol_risk * sigma_price


def _expected_market_trigger(limit_row: Mapping[str, Any]) -> str:
    if limit_row["formula_limit_price"] == CAP_BOUND_MARKET_ORDER_PLAN_PRICE_LABEL:
        return CAP_BOUND_MARKET_ORDER_TRIGGER_SOURCE_CONDITION
    return MARKET_ORDER_TRIGGER_SOURCE_CONDITION


def _round_limit(price: float, side: str) -> float:
    if side == "BUY":
        return math.floor((price + 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    if side == "SELL":
        return math.ceil((price - 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    return 0.0


def _side(position_change: int) -> str:
    if position_change > 0:
        return "BUY"
    if position_change < 0:
        return "SELL"
    return "NONE"


def _index_rows(rows: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...]) -> dict[int, Mapping[str, Any]]:
    return {int(row["row_index"]): row for row in rows}


def _rows_by_index(rows: tuple[Mapping[str, Any], ...]) -> dict[int, Mapping[str, Any]]:
    return {int(row["row_index"]): row for row in rows}


def _hash_row(row: dict[str, Any]) -> dict[str, Any]:
    output = dict(row)
    output["row_hash"] = canonical_sha256(output)
    return output


def _resolve_pack_root(path: Path | str | None) -> Path:
    if path is None:
        return (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()
    resolved = Path(path).resolve()
    if resolved != (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 fast order generator pack root is locked")
    return resolved


def _verify_pack_hash(pack_root: Path, name: str) -> None:
    manifest = Sha256ArtifactCache().read_json(pack_root / "S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST.json")
    expected = manifest.get("row_family_files", {}).get(name, {}).get("sha256")
    actual = hashlib.sha256((pack_root / name).read_bytes()).hexdigest()
    if expected != actual:
        raise CarverBlocked(f"S27 v2 fast order generator pack hash drift for {name}")


def _registry_payload(registry: FastOrderPolicyRegistry) -> dict[str, Any]:
    payload = asdict(registry)
    payload.pop("registry_hash", None)
    return payload


def _generation_bundle_payload(bundle: FastOrderGenerationBundle) -> dict[str, Any]:
    payload = asdict(bundle)
    payload.pop("bundle_hash", None)
    return payload

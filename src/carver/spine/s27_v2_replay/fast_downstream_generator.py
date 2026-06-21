from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from ..m0 import CarverBlocked
from .development_recon_run import ACCEPTED_COMMISSION_PER_CONTRACT, CONTRACT_POINT_VALUE
from .fast_order_generator import (
    FastGeneratedOrderRows,
    FastOrderGenerationBundle,
    FastOrderPolicyRegistry,
    ROLL_SUPPRESSION_LABEL,
)
from .fast_row_engine import FastPrimitiveEngineBundle
from .fast_segment_emitter import FastSegmentArtifacts
from .local_replay import canonical_sha256
from .replay_artifact_cache import Sha256ArtifactCache
from .fast_validation_profiles import (
    CHECKPOINT_PROOF_VALIDATION_PROFILE,
    is_checkpoint_proof_profile,
    require_supported_validation_profile,
)
from .test_incremental_runner import (
    AUTHORIZATION,
    BACKTEST_STATUS,
    COMBINED_TBBO_REGISTRY_NAME,
    DEFAULT_COMBINED_TBBO_RELATIVE_PATH,
    DEFAULT_PACK_RELATIVE_PATH,
    NON_AUTHORIZATIONS,
    PNL_EVALUATION_STATUS,
    RESULT_STATUS,
    INPUT_MANIFEST_NAME,
    IncrementalSegmentBundle,
)


STATUS = "LOCAL_2023_TEST_FAST_DOWNSTREAM_ROWS_GENERATED_NOT_RESULT"
GENERATOR_MODE = "GENERATE_DOWNSTREAM_ROWS_FROM_ORDER_INTENTS_AND_POLICY_REGISTRY_NOT_FULL_REPLAY"
POLICY_REGISTRY_STATUS = "LOCAL_2023_TEST_FAST_DOWNSTREAM_POLICY_REGISTRY_BOUND_NOT_RESULT"

DOWNSTREAM_LEDGER_FILES = (
    "working_order_transition_ledger.csv",
    "fill_ledger.csv",
    "market_fill_metadata_ledger.csv",
    "cost_ledger.csv",
    "pnl_ledger.csv",
    "validation_ledger.csv",
)
COMBINED_TBBO_REGISTRY_MANIFEST_NAME = "combined_market_order_tbbo_registry_manifest.json"

_REPO_ROOT = Path(__file__).resolve().parents[4]
VALUATION_CONVENTION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"
MARKET_FILL_PRICE_PROVENANCE_BY_SIDE = {
    "BUY": "MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE",
    "SELL": "MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE",
}
MARKET_COST_ACCOUNTING_CONVENTION_BY_SIDE = {
    "BUY": "ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST",
    "SELL": "BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST",
}
MARKET_SPREAD_COST_STATUS_BY_SIDE = {
    "BUY": "PASS_DATABENTO_TBBO_ASK_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL",
    "SELL": "PASS_DATABENTO_TBBO_BID_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL",
}
ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS = (
    "LOCAL_ENGINEERING_ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSED_ROW_EMITTED_NOT_RESULT"
)
ROW892_SESSION_END_LIMIT_CONVENTION = "SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT"
ROW892_SESSION_END_LIMIT_RULE = (
    "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_SESSION_VALUATION_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
)
ROW892_SESSION_END_LIMIT_ROW_STATUS = "LOCAL_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ROW_EMITTED_NOT_RESULT"
ROW1355_SESSION_END_LIMIT_VALUATION_GAP_CONVENTION = (
    "SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT"
)
ROW1355_SESSION_END_LIMIT_VALUATION_GAP_RULE = (
    "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_AVAILABLE_VALUATION_GAP_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT"
)
ROW1355_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS = (
    "LOCAL_ENGINEERING_SESSION_END_ADJACENT_LIMIT_VALUATION_GAP_ROW_EMITTED_NOT_RESULT"
)
RUN_LEDGER_FIELDNAMES = {
    "working_order_transition_ledger.csv": (
        "row_index",
        "starting_position_contracts",
        "ending_position_contracts",
        "working_state_before",
        "working_state_after",
        "same_session",
        "row_status",
        "row_hash",
    ),
    "fill_ledger.csv": (
        "row_index",
        "fill_executed",
        "fill_rule",
        "fill_candidate_close",
        "fill_price",
        "fill_quantity",
        "position_after_fill",
        "row_status",
        "row_hash",
    ),
    "market_fill_metadata_ledger.csv": (
        "row_index",
        "fill_timestamp_utc",
        "raw_symbol",
        "order_side",
        "fill_quantity",
        "fill_price",
        "fill_price_provenance",
        "fill_source_row_hash",
        "same_session",
        "roll_boundary_status",
        "working_state_before",
        "position_after_fill",
        "commission_per_contract",
        "commission_amount",
        "market_spread_cost_status",
        "pnl_emission_status",
        "row_status",
        "row_hash",
    ),
    "cost_ledger.csv": (
        "row_index",
        "cost_policy_id",
        "order_cost_type",
        "commission_amount",
        "spread_cost_amount",
        "total_cost_amount",
        "currency",
        "market_cost_accounting_convention",
        "spread_cost_reason",
        "tbbo_quote_ts_event",
        "tbbo_bid_px",
        "tbbo_ask_px",
        "tbbo_full_spread_points",
        "tbbo_full_spread_value_per_contract",
        "tbbo_selected_spread_row_hash",
        "tbbo_selected_spread_ledger_sha256",
        "row_status",
        "row_hash",
    ),
    "pnl_ledger.csv": (
        "row_index",
        "valuation_mark_timestamp_utc",
        "valuation_mark_close_price",
        "valuation_convention_label",
        "existing_position_gross_pnl",
        "fill_gross_pnl",
        "row_gross_pnl_amount",
        "row_net_pnl_amount",
        "cumulative_gross_pnl_amount",
        "cumulative_commission_amount",
        "cumulative_spread_amount",
        "cumulative_net_pnl_amount",
        "ending_position_contracts",
        "result_status",
        "backtest_status",
        "pnl_evaluation_status",
        "source_faithful_evidence_claimed",
        "row_status",
        "row_hash",
    ),
    "validation_ledger.csv": (
        "row_index",
        "result_status",
        "backtest_status",
        "source_faithful_evidence_claimed",
        "non_authorizations",
        "row_status",
        "row_hash",
    ),
}


@dataclass(frozen=True)
class FastDownstreamPolicyRegistry:
    status: str
    authorization_label: str
    segment_artifacts_hash: str
    order_generation_bundle_hash: str
    order_rows_hash: str
    policy_rows_hash: str
    policy_row_count: int
    registry_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(
        self,
        *,
        artifacts: FastSegmentArtifacts,
        primitive_bundle: FastPrimitiveEngineBundle,
        segment_bundle: IncrementalSegmentBundle,
        order_policy_registry: FastOrderPolicyRegistry,
        order_bundle: FastOrderGenerationBundle,
        order_rows: FastGeneratedOrderRows,
        validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
    ) -> None:
        require_supported_validation_profile(validation_profile)
        if self.status != POLICY_REGISTRY_STATUS:
            raise CarverBlocked("S27 v2 fast downstream policy registry status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast downstream policy registry authorization mismatch")
        if self.segment_artifacts_hash != artifacts.bundle_hash:
            raise CarverBlocked("S27 v2 fast downstream policy registry artifact binding drift")
        if self.order_generation_bundle_hash != order_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast downstream policy registry order bundle binding drift")
        if self.order_rows_hash != _order_rows_hash(order_rows):
            raise CarverBlocked("S27 v2 fast downstream policy registry order rows binding drift")
        if self.policy_row_count != len(order_rows.desired_position_rows):
            raise CarverBlocked("S27 v2 fast downstream policy registry row count drift")
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast downstream policy registry non-authorizations drift")
        if is_checkpoint_proof_profile(validation_profile):
            active_segment = _validate_active_artifact_authority(artifacts=artifacts, segment_bundle=segment_bundle)
            order_bundle.validate(
                primitive_bundle=primitive_bundle,
                segment_bundle=active_segment,
                artifacts=artifacts,
                policy_registry=order_policy_registry,
                rows=order_rows,
                validation_profile=validation_profile,
            )
        policy_rows = _build_policy_rows(artifacts=artifacts, order_rows=order_rows)
        if self.policy_rows_hash != canonical_sha256(policy_rows):
            raise CarverBlocked("S27 v2 fast downstream policy registry row hash drift")
        if self.registry_hash != canonical_sha256(_registry_payload(self)):
            raise CarverBlocked("S27 v2 fast downstream policy registry hash drift")


@dataclass(frozen=True)
class FastGeneratedDownstreamRows:
    transition_rows: tuple[dict[str, Any], ...]
    fill_rows: tuple[dict[str, Any], ...]
    market_fill_metadata_rows: tuple[dict[str, Any], ...]
    cost_rows: tuple[dict[str, Any], ...]
    pnl_rows: tuple[dict[str, Any], ...]
    validation_rows: tuple[dict[str, Any], ...]

    def validate(self, bundle: "FastDownstreamGenerationBundle") -> None:
        if canonical_sha256(self.transition_rows) != bundle.transition_rows_hash:
            raise CarverBlocked("S27 v2 fast downstream transition rows hash drift")
        if canonical_sha256(self.fill_rows) != bundle.fill_rows_hash:
            raise CarverBlocked("S27 v2 fast downstream fill rows hash drift")
        if canonical_sha256(self.market_fill_metadata_rows) != bundle.market_fill_metadata_rows_hash:
            raise CarverBlocked("S27 v2 fast downstream market-fill metadata rows hash drift")
        if canonical_sha256(self.cost_rows) != bundle.cost_rows_hash:
            raise CarverBlocked("S27 v2 fast downstream cost rows hash drift")
        if canonical_sha256(self.pnl_rows) != bundle.pnl_rows_hash:
            raise CarverBlocked("S27 v2 fast downstream pnl rows hash drift")
        if canonical_sha256(self.validation_rows) != bundle.validation_rows_hash:
            raise CarverBlocked("S27 v2 fast downstream validation rows hash drift")


@dataclass(frozen=True)
class FastDownstreamGenerationBundle:
    status: str
    authorization_label: str
    generator_mode: str
    primitive_engine_bundle_hash: str
    segment_bundle_hash: str
    segment_artifacts_hash: str
    order_generation_bundle_hash: str
    downstream_policy_registry_hash: str
    segment_start_row_index: int
    segment_end_row_index: int
    generated_row_count: int
    market_fill_metadata_row_count: int
    transition_rows_hash: str
    fill_rows_hash: str
    market_fill_metadata_rows_hash: str
    cost_rows_hash: str
    pnl_rows_hash: str
    validation_rows_hash: str
    parity_report_hash: str
    coherence_report_hash: str
    bundle_hash: str
    non_authorizations: tuple[str, ...] = NON_AUTHORIZATIONS

    def validate(
        self,
        *,
        primitive_bundle: FastPrimitiveEngineBundle,
        segment_bundle: IncrementalSegmentBundle,
        artifacts: FastSegmentArtifacts,
        order_policy_registry: FastOrderPolicyRegistry,
        order_bundle: FastOrderGenerationBundle,
        order_rows: FastGeneratedOrderRows,
        downstream_policy_registry: FastDownstreamPolicyRegistry,
        rows: FastGeneratedDownstreamRows,
        validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
    ) -> None:
        require_supported_validation_profile(validation_profile)
        if self.status != STATUS:
            raise CarverBlocked("S27 v2 fast downstream generation status mismatch")
        if self.authorization_label != AUTHORIZATION:
            raise CarverBlocked("S27 v2 fast downstream generation authorization mismatch")
        if self.generator_mode != GENERATOR_MODE:
            raise CarverBlocked("S27 v2 fast downstream generation mode drift")
        if self.primitive_engine_bundle_hash != primitive_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast downstream generation primitive binding drift")
        if self.segment_bundle_hash != segment_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast downstream generation segment binding drift")
        if self.segment_artifacts_hash != artifacts.bundle_hash:
            raise CarverBlocked("S27 v2 fast downstream generation artifact binding drift")
        if self.order_generation_bundle_hash != order_bundle.bundle_hash:
            raise CarverBlocked("S27 v2 fast downstream generation order binding drift")
        if self.downstream_policy_registry_hash != downstream_policy_registry.registry_hash:
            raise CarverBlocked("S27 v2 fast downstream generation policy binding drift")
        if self.segment_start_row_index != segment_bundle.segment_start_row_index:
            raise CarverBlocked("S27 v2 fast downstream generation start row drift")
        if self.segment_end_row_index != segment_bundle.segment_end_row_index:
            raise CarverBlocked("S27 v2 fast downstream generation end row drift")
        if self.generated_row_count != segment_bundle.segment_row_count:
            raise CarverBlocked("S27 v2 fast downstream generation row count drift")
        _validate_dense_generated_counts(self, rows, segment_bundle)
        if self.market_fill_metadata_row_count != len(rows.market_fill_metadata_rows):
            raise CarverBlocked("S27 v2 fast downstream generation market-fill row count drift")
        _validate_unique_row_indexes(rows)
        if self.non_authorizations != NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 fast downstream generation non-authorizations drift")

        if is_checkpoint_proof_profile(validation_profile):
            order_bundle.validate(
                primitive_bundle=primitive_bundle,
                segment_bundle=segment_bundle,
                artifacts=artifacts,
                policy_registry=order_policy_registry,
                rows=order_rows,
                validation_profile=validation_profile,
            )
            downstream_policy_registry.validate(
                artifacts=artifacts,
                primitive_bundle=primitive_bundle,
                segment_bundle=segment_bundle,
                order_policy_registry=order_policy_registry,
                order_bundle=order_bundle,
                order_rows=order_rows,
                validation_profile=validation_profile,
            )
        rows.validate(self)
        if self.parity_report_hash != _validate_downstream_parity(rows, artifacts):
            raise CarverBlocked("S27 v2 fast downstream generation parity report hash drift")
        coherence_hash = _validate_downstream_coherence(
            rows=rows,
            order_rows=order_rows,
            segment_bundle=segment_bundle,
        )
        if self.coherence_report_hash != coherence_hash:
            raise CarverBlocked("S27 v2 fast downstream generation coherence report hash drift")
        if self.bundle_hash != canonical_sha256(_generation_bundle_payload(self)):
            raise CarverBlocked("S27 v2 fast downstream generation bundle hash drift")


def build_fast_downstream_policy_registry(
    *,
    primitive_bundle: FastPrimitiveEngineBundle,
    segment_bundle: IncrementalSegmentBundle,
    artifacts: FastSegmentArtifacts,
    order_policy_registry: FastOrderPolicyRegistry,
    order_bundle: FastOrderGenerationBundle,
    order_rows: FastGeneratedOrderRows,
    validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
) -> FastDownstreamPolicyRegistry:
    require_supported_validation_profile(validation_profile)
    policy_rows = _build_policy_rows(artifacts=artifacts, order_rows=order_rows)
    payload = {
        "status": POLICY_REGISTRY_STATUS,
        "authorization_label": AUTHORIZATION,
        "segment_artifacts_hash": artifacts.bundle_hash,
        "order_generation_bundle_hash": order_bundle.bundle_hash,
        "order_rows_hash": _order_rows_hash(order_rows),
        "policy_rows_hash": canonical_sha256(policy_rows),
        "policy_row_count": len(policy_rows),
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    registry = FastDownstreamPolicyRegistry(
        status=POLICY_REGISTRY_STATUS,
        authorization_label=AUTHORIZATION,
        segment_artifacts_hash=artifacts.bundle_hash,
        order_generation_bundle_hash=order_bundle.bundle_hash,
        order_rows_hash=str(payload["order_rows_hash"]),
        policy_rows_hash=str(payload["policy_rows_hash"]),
        policy_row_count=len(policy_rows),
        registry_hash=canonical_sha256(payload),
    )
    registry.validate(
        artifacts=artifacts,
        primitive_bundle=primitive_bundle,
        segment_bundle=segment_bundle,
        order_policy_registry=order_policy_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
        validation_profile=validation_profile,
    )
    return registry


def build_fast_downstream_generation(
    *,
    primitive_bundle: FastPrimitiveEngineBundle,
    segment_bundle: IncrementalSegmentBundle,
    artifacts: FastSegmentArtifacts,
    order_policy_registry: FastOrderPolicyRegistry,
    order_bundle: FastOrderGenerationBundle,
    order_rows: FastGeneratedOrderRows,
    downstream_policy_registry: FastDownstreamPolicyRegistry,
    validation_profile: str = CHECKPOINT_PROOF_VALIDATION_PROFILE,
) -> tuple[FastDownstreamGenerationBundle, FastGeneratedDownstreamRows]:
    require_supported_validation_profile(validation_profile)
    if is_checkpoint_proof_profile(validation_profile):
        order_bundle.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment_bundle,
            artifacts=artifacts,
            policy_registry=order_policy_registry,
            rows=order_rows,
            validation_profile=validation_profile,
        )
        downstream_policy_registry.validate(
            artifacts=artifacts,
            primitive_bundle=primitive_bundle,
            segment_bundle=segment_bundle,
            order_policy_registry=order_policy_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            validation_profile=validation_profile,
        )

    rows = _generate_downstream_rows_from_policy(
        policy_rows=_build_policy_rows(artifacts=artifacts, order_rows=order_rows),
        order_rows=order_rows,
        segment_bundle=segment_bundle,
    )
    parity_report_hash = _validate_downstream_parity(rows, artifacts)
    coherence_report_hash = _validate_downstream_coherence(
        rows=rows,
        order_rows=order_rows,
        segment_bundle=segment_bundle,
    )
    payload = {
        "status": STATUS,
        "authorization_label": AUTHORIZATION,
        "generator_mode": GENERATOR_MODE,
        "primitive_engine_bundle_hash": primitive_bundle.bundle_hash,
        "segment_bundle_hash": segment_bundle.bundle_hash,
        "segment_artifacts_hash": artifacts.bundle_hash,
        "order_generation_bundle_hash": order_bundle.bundle_hash,
        "downstream_policy_registry_hash": downstream_policy_registry.registry_hash,
        "segment_start_row_index": segment_bundle.segment_start_row_index,
        "segment_end_row_index": segment_bundle.segment_end_row_index,
        "generated_row_count": len(rows.fill_rows),
        "market_fill_metadata_row_count": len(rows.market_fill_metadata_rows),
        "transition_rows_hash": canonical_sha256(rows.transition_rows),
        "fill_rows_hash": canonical_sha256(rows.fill_rows),
        "market_fill_metadata_rows_hash": canonical_sha256(rows.market_fill_metadata_rows),
        "cost_rows_hash": canonical_sha256(rows.cost_rows),
        "pnl_rows_hash": canonical_sha256(rows.pnl_rows),
        "validation_rows_hash": canonical_sha256(rows.validation_rows),
        "parity_report_hash": parity_report_hash,
        "coherence_report_hash": coherence_report_hash,
        "non_authorizations": NON_AUTHORIZATIONS,
    }
    bundle = FastDownstreamGenerationBundle(
        status=STATUS,
        authorization_label=AUTHORIZATION,
        generator_mode=GENERATOR_MODE,
        primitive_engine_bundle_hash=primitive_bundle.bundle_hash,
        segment_bundle_hash=segment_bundle.bundle_hash,
        segment_artifacts_hash=artifacts.bundle_hash,
        order_generation_bundle_hash=order_bundle.bundle_hash,
        downstream_policy_registry_hash=downstream_policy_registry.registry_hash,
        segment_start_row_index=segment_bundle.segment_start_row_index,
        segment_end_row_index=segment_bundle.segment_end_row_index,
        generated_row_count=len(rows.fill_rows),
        market_fill_metadata_row_count=len(rows.market_fill_metadata_rows),
        transition_rows_hash=str(payload["transition_rows_hash"]),
        fill_rows_hash=str(payload["fill_rows_hash"]),
        market_fill_metadata_rows_hash=str(payload["market_fill_metadata_rows_hash"]),
        cost_rows_hash=str(payload["cost_rows_hash"]),
        pnl_rows_hash=str(payload["pnl_rows_hash"]),
        validation_rows_hash=str(payload["validation_rows_hash"]),
        parity_report_hash=parity_report_hash,
        coherence_report_hash=coherence_report_hash,
        bundle_hash=canonical_sha256(payload),
    )
    bundle.validate(
        primitive_bundle=primitive_bundle,
        segment_bundle=segment_bundle,
        artifacts=artifacts,
        order_policy_registry=order_policy_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_policy_registry,
        rows=rows,
        validation_profile=validation_profile,
    )
    return bundle, rows


def _build_policy_rows(
    *,
    artifacts: FastSegmentArtifacts,
    order_rows: FastGeneratedOrderRows,
) -> tuple[dict[str, Any], ...]:
    desired = _rows_by_index(order_rows.desired_position_rows)
    limit = _rows_by_index(order_rows.limit_order_rows)
    no_market = _rows_by_index(order_rows.no_market_order_rows)
    market = _rows_by_index(order_rows.market_order_rows)
    source = _load_downstream_source(pack_root=_resolve_pack_root(None), tbbo_root=_resolve_tbbo_root(None))
    decision_source = source["decision"]
    fill_source = source["fill"]
    mark_source = source["mark"]
    rows: list[dict[str, Any]] = []
    for row_index in sorted(desired):
        policy = _derive_downstream_policy(
            row_index=row_index,
            desired_row=desired[row_index],
            limit_row=limit[row_index],
            no_market_row=no_market[row_index],
            market_row=market.get(row_index),
            decision_row=decision_source[row_index],
            fill_row=fill_source[row_index],
            mark_row=mark_source[row_index],
        )
        rows.append(
            {
                "row_index": row_index,
                "desired_row_hash": desired[row_index]["row_hash"],
                "limit_row_hash": limit[row_index]["row_hash"],
                "no_market_row_hash": no_market[row_index]["row_hash"],
                "market_order_row_hash": market.get(row_index, {}).get("row_hash", "NO_MARKET_ROW"),
                **policy,
                "policy_row_hash": canonical_sha256(
                    {
                        "row_index": row_index,
                        "desired_row_hash": desired[row_index]["row_hash"],
                        "limit_row_hash": limit[row_index]["row_hash"],
                        "no_market_row_hash": no_market[row_index]["row_hash"],
                        "market_order_row_hash": market.get(row_index, {}).get("row_hash", "NO_MARKET_ROW"),
                        "transition_policy": {
                            "working_state_before": policy["transition_working_state_before"],
                            "working_state_after": policy["transition_working_state_after"],
                            "same_session": policy["transition_same_session"],
                            "row_status": policy["transition_row_status"],
                        },
                        "downstream_policy": {
                            "fill_rule": policy["fill_rule"],
                            "fill_row_status": policy["fill_row_status"],
                            "cost_row_status": policy["cost_row_status"],
                            "pnl_row_status": policy["pnl_row_status"],
                            "validation_row_status": policy["validation_row_status"],
                            "market_fill_row_status": policy["market_fill_row_status"],
                        },
                    }
                ),
            }
        )
    return tuple(rows)


def _derive_downstream_policy(
    *,
    row_index: int,
    desired_row: Mapping[str, Any],
    limit_row: Mapping[str, Any],
    no_market_row: Mapping[str, Any],
    market_row: Mapping[str, Any] | None,
    decision_row: Mapping[str, Any],
    fill_row: Mapping[str, Any],
    mark_row: Mapping[str, Any],
) -> dict[str, Any]:
    if str(decision_row["raw_symbol"]) != str(fill_row["raw_symbol"]) or str(fill_row["raw_symbol"]) != str(mark_row["raw_symbol"]):
        raise CarverBlocked(f"S27 v2 fast downstream source raw-symbol drift at row {row_index}")
    if market_row is not None:
        if not _is_true(no_market_row["market_order_required"]) or not _is_true(no_market_row["market_order_rows_emitted"]):
            raise CarverBlocked(f"S27 v2 fast downstream market policy flag drift at row {row_index}")
        if int(market_row["target_position_after_fill"]) != int(desired_row["desired_position_contracts"]):
            raise CarverBlocked(f"S27 v2 fast downstream market target drift at row {row_index}")
        if int(market_row["current_position_before_order"]) != int(desired_row["starting_position_contracts"]):
            raise CarverBlocked(f"S27 v2 fast downstream market start drift at row {row_index}")
        return {
            "transition_working_state_before": "EMPTY_INITIAL_WORKING_STATE",
            "transition_working_state_after": "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION",
            "transition_same_session": _bool_label(str(decision_row["session_id"]) == str(fill_row["session_id"])),
            "transition_row_status": "LOCAL_MARKET_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT",
            "fill_rule": MARKET_FILL_PRICE_PROVENANCE_BY_SIDE[str(market_row["order_side"])],
            "fill_row_status": "LOCAL_MARKET_ORDER_FILL_ROW_EMITTED_NOT_RESULT",
            "cost_row_status": "LOCAL_MARKET_ORDER_ACTUAL_COST_ROW_EMITTED_NOT_PNL_NOT_RESULT",
            "pnl_row_status": "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
            "validation_row_status": "LOCAL_MARKET_ORDER_PNL_VALIDATION_ROW_EMITTED_NOT_RESULT",
            "market_fill_row_status": "LOCAL_MARKET_FILL_METADATA_ROW_EMITTED_NOT_RESULT",
            "market_fill_roll_boundary_status": "NO_ROLL_BOUNDARY_SAME_RAW_SYMBOL",
        }

    convention = str(no_market_row["engineering_convention_label"])
    side = str(limit_row["order_side"])
    order_quantity = int(limit_row["order_quantity"])
    limit_price = _limit_price_value(limit_row["limit_order_price"])
    fill_executed = order_quantity > 0 and _limit_fill(side, float(fill_row["close_price"]), limit_price)
    same_session = str(decision_row["session_id"]) == str(fill_row["session_id"]) == str(mark_row["session_id"])

    if convention == ROLL_SUPPRESSION_LABEL:
        row_status = ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSION_ROW_STATUS
        return {
            "transition_working_state_before": "NO_OPEN_WORKING_ORDER_CARRIED",
            "transition_working_state_after": "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION",
            "transition_same_session": _bool_label(same_session),
            "transition_row_status": row_status,
            "fill_rule": ROLL_SUPPRESSION_LABEL,
            "fill_row_status": row_status,
            "cost_row_status": row_status,
            "pnl_row_status": row_status,
            "validation_row_status": row_status,
            "market_fill_row_status": "NO_MARKET_FILL_METADATA_ROW",
            "market_fill_roll_boundary_status": "NO_MARKET_ORDER",
        }

    if convention == ROW892_SESSION_END_LIMIT_CONVENTION:
        fill_rule = ROW892_SESSION_END_LIMIT_RULE
        row_status = ROW892_SESSION_END_LIMIT_ROW_STATUS
        transition_status = row_status
    elif convention == ROW1355_SESSION_END_LIMIT_VALUATION_GAP_CONVENTION:
        fill_rule = ROW1355_SESSION_END_LIMIT_VALUATION_GAP_RULE
        row_status = ROW1355_SESSION_END_LIMIT_VALUATION_GAP_ROW_STATUS
        transition_status = row_status
    else:
        fill_rule = "ONE_HOUR_CLOSE_ONLY_LIMIT_FILL"
        row_status = "LOCAL_FILL_ROW_EMITTED_NOT_RESULT"
        transition_status = "LOCAL_WORKING_ORDER_TRANSITION_ROW_EMITTED_NOT_RESULT"

    if side == "NONE":
        working_after = "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
    elif fill_executed:
        working_after = "NO_OPEN_WORKING_ORDER_AFTER_FILL_DECISION"
    else:
        working_after = "UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE"

    return {
        "transition_working_state_before": "NO_OPEN_WORKING_ORDER_CARRIED",
        "transition_working_state_after": working_after,
        "transition_same_session": _bool_label(same_session),
        "transition_row_status": transition_status,
        "fill_rule": fill_rule,
        "fill_row_status": row_status,
        "cost_row_status": "LOCAL_COST_ROW_EMITTED_NOT_RESULT",
        "pnl_row_status": "LOCAL_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
        "validation_row_status": "LOCAL_VALIDATION_ROW_EMITTED_NOT_RESULT",
        "market_fill_row_status": "NO_MARKET_FILL_METADATA_ROW",
        "market_fill_roll_boundary_status": "NO_MARKET_ORDER",
    }


def _generate_downstream_rows_from_policy(
    *,
    policy_rows: tuple[Mapping[str, Any], ...],
    order_rows: FastGeneratedOrderRows,
    segment_bundle: IncrementalSegmentBundle,
) -> FastGeneratedDownstreamRows:
    pack_root = _resolve_pack_root(None)
    tbbo_root = _resolve_tbbo_root(None)
    source = _load_downstream_source(pack_root=pack_root, tbbo_root=tbbo_root)
    desired = _rows_by_index(order_rows.desired_position_rows)
    limit = _rows_by_index(order_rows.limit_order_rows)
    market = _rows_by_index(order_rows.market_order_rows)
    fill_source = source["fill"]
    mark_source = source["mark"]
    tbbo = source["tbbo"]
    cost_parameter = source["cost"]
    tbbo_registry_sha = source["tbbo_registry_sha"]
    transition_rows: list[dict[str, Any]] = []
    fill_rows: list[dict[str, Any]] = []
    market_fill_metadata_rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    pnl_rows: list[dict[str, Any]] = []
    validation_rows: list[dict[str, Any]] = []
    previous_mark_price = float(segment_bundle.baseline_checkpoint.valuation_mark_close_price)
    cumulative_gross = float(segment_bundle.baseline_checkpoint.cumulative_gross_pnl_amount)
    cumulative_commission = float(segment_bundle.baseline_checkpoint.cumulative_commission_amount)
    cumulative_spread = float(segment_bundle.baseline_checkpoint.cumulative_spread_amount)
    for policy in policy_rows:
        row_index = int(policy["row_index"])
        desired_row = desired[row_index]
        limit_row = limit[row_index]
        market_row = market.get(row_index)
        fill_bar = fill_source[row_index]
        mark_bar = mark_source[row_index]
        starting_position = int(desired_row["starting_position_contracts"])
        target_position = int(desired_row["desired_position_contracts"])
        position_change = int(desired_row["position_change_contracts"])
        order_quantity = int(limit_row["order_quantity"])
        side = str(limit_row["order_side"])
        fill_close = float(fill_bar["close_price"])
        mark_price = float(mark_bar["close_price"])

        if market_row is not None:
            tbbo_row = _market_spread_row(tbbo=tbbo, row_index=row_index, side=side, fill_bar=fill_bar)
            fill_quantity = int(market_row["order_quantity"])
            fill_price = float(tbbo_row["selected_executable_market_fill_price"])
            signed_fill = fill_quantity if side == "BUY" else -fill_quantity
            position_after_fill = target_position
            commission = ACCEPTED_COMMISSION_PER_CONTRACT * fill_quantity
            spread = 0.0
            fill_payload = {
                "row_index": row_index,
                "fill_executed": True,
                "fill_rule": MARKET_FILL_PRICE_PROVENANCE_BY_SIDE[side],
                "fill_candidate_close": fill_close,
                "fill_price": fill_price,
                "fill_quantity": fill_quantity,
                "position_after_fill": position_after_fill,
                "row_status": policy["fill_row_status"],
            }
            market_payload = {
                "row_index": row_index,
                "fill_timestamp_utc": fill_bar["completed_timestamp_utc"],
                "raw_symbol": fill_bar["raw_symbol"],
                "order_side": side,
                "fill_quantity": fill_quantity,
                "fill_price": fill_price,
                "fill_price_provenance": MARKET_FILL_PRICE_PROVENANCE_BY_SIDE[side],
                "fill_source_row_hash": fill_bar["source_row_hash"],
                "same_session": policy["transition_same_session"] == "TRUE",
                "roll_boundary_status": policy["market_fill_roll_boundary_status"],
                "working_state_before": policy["transition_working_state_before"],
                "position_after_fill": position_after_fill,
                "commission_per_contract": ACCEPTED_COMMISSION_PER_CONTRACT,
                "commission_amount": commission,
                "market_spread_cost_status": MARKET_SPREAD_COST_STATUS_BY_SIDE[side],
                "pnl_emission_status": "LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT",
                "row_status": policy["market_fill_row_status"],
            }
            market_fill_metadata_rows.append(_materialize_row(market_payload, "market_fill_metadata_ledger.csv"))
            cost_payload = {
                "row_index": row_index,
                "cost_policy_id": cost_parameter["cost_policy_id"],
                "order_cost_type": f"MARKET_ORDER_{side}_{'ASK' if side == 'BUY' else 'BID'}_FILL_ACTUAL_COST_NOT_PNL",
                "commission_amount": commission,
                "spread_cost_amount": spread,
                "total_cost_amount": commission + spread,
                "currency": cost_parameter["currency"],
                "market_cost_accounting_convention": MARKET_COST_ACCOUNTING_CONVENTION_BY_SIDE[side],
                "spread_cost_reason": (
                    f"NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_"
                    f"{'ASK' if side == 'BUY' else 'BID'}"
                ),
                "tbbo_quote_ts_event": tbbo_row["selected_quote_ts_event"],
                "tbbo_bid_px": tbbo_row["bid_px_00"],
                "tbbo_ask_px": tbbo_row["ask_px_00"],
                "tbbo_full_spread_points": tbbo_row["spread_points"],
                "tbbo_full_spread_value_per_contract": tbbo_row["spread_cost_usd_per_contract"],
                "tbbo_selected_spread_row_hash": tbbo_row["row_hash"],
                "tbbo_selected_spread_ledger_sha256": tbbo_registry_sha,
                "row_status": policy["cost_row_status"],
            }
        else:
            limit_price = _limit_price_value(limit_row["limit_order_price"])
            fill_quantity = order_quantity if _limit_fill(side, fill_close, limit_price) else 0
            signed_fill = fill_quantity if side == "BUY" else -fill_quantity if side == "SELL" else 0
            position_after_fill = starting_position + signed_fill
            fill_price = limit_price if fill_quantity else 0.0
            commission = ACCEPTED_COMMISSION_PER_CONTRACT * abs(fill_quantity)
            spread = 0.0
            fill_payload = {
                "row_index": row_index,
                "fill_executed": fill_quantity > 0,
                "fill_rule": policy["fill_rule"],
                "fill_candidate_close": fill_close,
                "fill_price": fill_price,
                "fill_quantity": fill_quantity,
                "position_after_fill": position_after_fill,
                "row_status": policy["fill_row_status"],
            }
            cost_payload = {
                "row_index": row_index,
                "cost_policy_id": cost_parameter["cost_policy_id"],
                "commission_amount": commission,
                "spread_cost_amount": spread,
                "total_cost_amount": commission + spread,
                "currency": cost_parameter["currency"],
                "row_status": policy["cost_row_status"],
            }

        transition_payload = {
            "row_index": row_index,
            "starting_position_contracts": starting_position,
            "ending_position_contracts": position_after_fill,
            "working_state_before": policy["transition_working_state_before"],
            "working_state_after": policy["transition_working_state_after"],
            "same_session": policy["transition_same_session"] == "TRUE",
            "row_status": policy["transition_row_status"],
        }
        existing_gross = starting_position * (mark_price - previous_mark_price) * CONTRACT_POINT_VALUE
        fill_gross = signed_fill * (mark_price - fill_price) * CONTRACT_POINT_VALUE if fill_quantity else 0.0
        if (
            fill_quantity == 0
            and policy["pnl_row_status"]
            == "LOCAL_ENGINEERING_ROLL_BOUNDARY_NO_NEW_ORDER_SUPPRESSED_ROW_EMITTED_NOT_RESULT"
        ):
            row_gross = existing_gross
        else:
            row_gross = existing_gross + fill_gross
        row_net = row_gross if commission == 0.0 and spread == 0.0 else row_gross - commission - spread
        cumulative_gross += row_gross
        cumulative_commission += commission
        cumulative_spread += spread
        cumulative_net = cumulative_gross - cumulative_commission - cumulative_spread
        pnl_payload = {
            "row_index": row_index,
            "valuation_mark_timestamp_utc": mark_bar["completed_timestamp_utc"],
            "valuation_mark_close_price": mark_price,
            "valuation_convention_label": VALUATION_CONVENTION_LABEL,
            "existing_position_gross_pnl": existing_gross,
            "fill_gross_pnl": fill_gross,
            "row_gross_pnl_amount": row_gross,
            "row_net_pnl_amount": row_net,
            "cumulative_gross_pnl_amount": cumulative_gross,
            "cumulative_commission_amount": cumulative_commission,
            "cumulative_spread_amount": cumulative_spread,
            "cumulative_net_pnl_amount": cumulative_net,
            "ending_position_contracts": position_after_fill,
            "result_status": RESULT_STATUS,
            "backtest_status": BACKTEST_STATUS,
            "pnl_evaluation_status": PNL_EVALUATION_STATUS,
            "source_faithful_evidence_claimed": False,
            "row_status": policy["pnl_row_status"],
        }
        validation_payload = {
            "row_index": row_index,
            "result_status": RESULT_STATUS,
            "backtest_status": BACKTEST_STATUS,
            "source_faithful_evidence_claimed": False,
            "non_authorizations": NON_AUTHORIZATIONS,
            "row_status": policy["validation_row_status"],
        }
        transition_rows.append(_materialize_row(transition_payload, "working_order_transition_ledger.csv"))
        fill_rows.append(_materialize_row(fill_payload, "fill_ledger.csv"))
        cost_rows.append(_materialize_row(cost_payload, "cost_ledger.csv"))
        pnl_rows.append(_materialize_row(pnl_payload, "pnl_ledger.csv"))
        validation_rows.append(_materialize_row(validation_payload, "validation_ledger.csv"))
        previous_mark_price = mark_price
    return FastGeneratedDownstreamRows(
        transition_rows=tuple(transition_rows),
        fill_rows=tuple(fill_rows),
        market_fill_metadata_rows=tuple(market_fill_metadata_rows),
        cost_rows=tuple(cost_rows),
        pnl_rows=tuple(pnl_rows),
        validation_rows=tuple(validation_rows),
    )


def _validate_downstream_parity(rows: FastGeneratedDownstreamRows, artifacts: FastSegmentArtifacts) -> str:
    expected = {
        "working_order_transition_ledger.csv": _rows_by_index(
            artifacts.segment_rows_by_ledger["working_order_transition_ledger.csv"]
        ),
        "fill_ledger.csv": _rows_by_index(artifacts.segment_rows_by_ledger["fill_ledger.csv"]),
        "market_fill_metadata_ledger.csv": _rows_by_index(
            artifacts.segment_rows_by_ledger["market_fill_metadata_ledger.csv"]
        ),
        "cost_ledger.csv": _rows_by_index(artifacts.segment_rows_by_ledger["cost_ledger.csv"]),
        "pnl_ledger.csv": _rows_by_index(artifacts.segment_rows_by_ledger["pnl_ledger.csv"]),
        "validation_ledger.csv": _rows_by_index(artifacts.segment_rows_by_ledger["validation_ledger.csv"]),
    }
    generated = {
        "working_order_transition_ledger.csv": _rows_by_index(rows.transition_rows),
        "fill_ledger.csv": _rows_by_index(rows.fill_rows),
        "market_fill_metadata_ledger.csv": _rows_by_index(rows.market_fill_metadata_rows),
        "cost_ledger.csv": _rows_by_index(rows.cost_rows),
        "pnl_ledger.csv": _rows_by_index(rows.pnl_rows),
        "validation_ledger.csv": _rows_by_index(rows.validation_rows),
    }
    parity_rows: list[dict[str, Any]] = []
    for ledger_name, expected_rows in expected.items():
        generated_rows = generated[ledger_name]
        if set(expected_rows) != set(generated_rows):
            raise CarverBlocked(f"S27 v2 fast downstream row set drift for {ledger_name}")
        for row_index, expected_row in expected_rows.items():
            observed = generated_rows[row_index]
            if dict(observed) != dict(expected_row):
                raise CarverBlocked(f"S27 v2 fast downstream parity drift for {ledger_name} row {row_index}")
        parity_rows.append(
            {
                "ledger_name": ledger_name,
                "row_count": len(expected_rows),
                "generated_rows_hash": canonical_sha256(tuple(generated_rows[index] for index in sorted(generated_rows))),
            }
        )
    return canonical_sha256(parity_rows)


def _validate_downstream_coherence(
    *,
    rows: FastGeneratedDownstreamRows,
    order_rows: FastGeneratedOrderRows,
    segment_bundle: IncrementalSegmentBundle,
) -> str:
    desired = _rows_by_index(order_rows.desired_position_rows)
    limit = _rows_by_index(order_rows.limit_order_rows)
    no_market = _rows_by_index(order_rows.no_market_order_rows)
    market = _rows_by_index(order_rows.market_order_rows)
    transition = _rows_by_index(rows.transition_rows)
    fill = _rows_by_index(rows.fill_rows)
    market_fill = _rows_by_index(rows.market_fill_metadata_rows)
    cost = _rows_by_index(rows.cost_rows)
    pnl = _rows_by_index(rows.pnl_rows)
    validation = _rows_by_index(rows.validation_rows)

    previous_position = int(segment_bundle.baseline_checkpoint.ending_position_contracts)
    cumulative_gross = float(segment_bundle.baseline_checkpoint.cumulative_gross_pnl_amount)
    cumulative_commission = float(segment_bundle.baseline_checkpoint.cumulative_commission_amount)
    cumulative_spread = float(segment_bundle.baseline_checkpoint.cumulative_spread_amount)
    cumulative_net = float(segment_bundle.baseline_checkpoint.cumulative_net_pnl_amount)
    coherence_rows: list[dict[str, Any]] = []

    for row_index in range(segment_bundle.segment_start_row_index, segment_bundle.segment_end_row_index + 1):
        desired_row = desired[row_index]
        transition_row = transition[row_index]
        fill_row = fill[row_index]
        cost_row = cost[row_index]
        pnl_row = pnl[row_index]
        validation_row = validation[row_index]
        if int(desired_row["starting_position_contracts"]) != previous_position:
            raise CarverBlocked(f"S27 v2 fast downstream starting position drift at row {row_index}")
        if int(transition_row["starting_position_contracts"]) != previous_position:
            raise CarverBlocked(f"S27 v2 fast downstream transition start drift at row {row_index}")
        if int(transition_row["ending_position_contracts"]) != int(fill_row["position_after_fill"]):
            raise CarverBlocked(f"S27 v2 fast downstream transition/fill position drift at row {row_index}")
        if int(pnl_row["ending_position_contracts"]) != int(fill_row["position_after_fill"]):
            raise CarverBlocked(f"S27 v2 fast downstream pnl/fill position drift at row {row_index}")
        order_quantity = int(limit[row_index]["order_quantity"])
        fill_quantity = int(fill_row["fill_quantity"])
        if fill_row["fill_executed"] == "FALSE" and fill_quantity != 0:
            raise CarverBlocked(f"S27 v2 fast downstream no-fill quantity drift at row {row_index}")
        if fill_row["fill_executed"] == "TRUE" and fill_quantity <= 0:
            raise CarverBlocked(f"S27 v2 fast downstream filled quantity drift at row {row_index}")
        if fill_quantity > order_quantity:
            raise CarverBlocked(f"S27 v2 fast downstream fill quantity exceeds order quantity at row {row_index}")
        if row_index in market:
            metadata = market_fill.get(row_index)
            if metadata is None:
                raise CarverBlocked(f"S27 v2 fast downstream missing market-fill metadata at row {row_index}")
            if metadata["raw_symbol"] == "":
                raise CarverBlocked(f"S27 v2 fast downstream market-fill raw symbol missing at row {row_index}")
            if metadata["fill_timestamp_utc"] == "":
                raise CarverBlocked(f"S27 v2 fast downstream market-fill timestamp missing at row {row_index}")
            if metadata["order_side"] != market[row_index]["order_side"]:
                raise CarverBlocked(f"S27 v2 fast downstream market-fill side drift at row {row_index}")
            if int(metadata["fill_quantity"]) != int(fill_row["fill_quantity"]):
                raise CarverBlocked(f"S27 v2 fast downstream market-fill quantity drift at row {row_index}")
            if metadata["fill_price"] != fill_row["fill_price"]:
                raise CarverBlocked(f"S27 v2 fast downstream market-fill price drift at row {row_index}")
            if int(metadata["position_after_fill"]) != int(fill_row["position_after_fill"]):
                raise CarverBlocked(f"S27 v2 fast downstream market-fill position drift at row {row_index}")
            if metadata["fill_price_provenance"] == "":
                raise CarverBlocked(f"S27 v2 fast downstream market-fill provenance missing at row {row_index}")
            if metadata["fill_source_row_hash"] == "":
                raise CarverBlocked(f"S27 v2 fast downstream market-fill source hash missing at row {row_index}")
        elif row_index in market_fill:
            raise CarverBlocked(f"S27 v2 fast downstream unexpected market-fill metadata at row {row_index}")

        commission = float(cost_row["commission_amount"])
        spread = float(cost_row["spread_cost_amount"])
        total_cost = float(cost_row["total_cost_amount"])
        if abs((commission + spread) - total_cost) > 1e-9:
            raise CarverBlocked(f"S27 v2 fast downstream total cost arithmetic drift at row {row_index}")
        row_gross = float(pnl_row["row_gross_pnl_amount"])
        row_net = float(pnl_row["row_net_pnl_amount"])
        if abs((row_gross - total_cost) - row_net) > 1e-6:
            raise CarverBlocked(f"S27 v2 fast downstream row net pnl arithmetic drift at row {row_index}")
        cumulative_gross += row_gross
        cumulative_commission += commission
        cumulative_spread += spread
        cumulative_net += row_net
        if abs(cumulative_gross - float(pnl_row["cumulative_gross_pnl_amount"])) > 1e-6:
            raise CarverBlocked(f"S27 v2 fast downstream cumulative gross drift at row {row_index}")
        if abs(cumulative_commission - float(pnl_row["cumulative_commission_amount"])) > 1e-6:
            raise CarverBlocked(f"S27 v2 fast downstream cumulative commission drift at row {row_index}")
        if abs(cumulative_spread - float(pnl_row["cumulative_spread_amount"])) > 1e-6:
            raise CarverBlocked(f"S27 v2 fast downstream cumulative spread drift at row {row_index}")
        if abs(cumulative_net - float(pnl_row["cumulative_net_pnl_amount"])) > 1e-6:
            raise CarverBlocked(f"S27 v2 fast downstream cumulative net drift at row {row_index}")
        if validation_row["result_status"] != RESULT_STATUS:
            raise CarverBlocked(f"S27 v2 fast downstream result status drift at row {row_index}")
        if validation_row["backtest_status"] != BACKTEST_STATUS:
            raise CarverBlocked(f"S27 v2 fast downstream backtest status drift at row {row_index}")
        if validation_row["source_faithful_evidence_claimed"] != "FALSE":
            raise CarverBlocked(f"S27 v2 fast downstream source-faithful flag drift at row {row_index}")
        if pnl_row["result_status"] != RESULT_STATUS:
            raise CarverBlocked(f"S27 v2 fast downstream pnl result status drift at row {row_index}")
        if pnl_row["backtest_status"] != BACKTEST_STATUS:
            raise CarverBlocked(f"S27 v2 fast downstream pnl backtest status drift at row {row_index}")
        if pnl_row["pnl_evaluation_status"] != PNL_EVALUATION_STATUS:
            raise CarverBlocked(f"S27 v2 fast downstream pnl evaluation status drift at row {row_index}")
        if pnl_row["source_faithful_evidence_claimed"] != "FALSE":
            raise CarverBlocked(f"S27 v2 fast downstream pnl source-faithful flag drift at row {row_index}")
        previous_position = int(fill_row["position_after_fill"])
        coherence_rows.append(
            {
                "row_index": row_index,
                "ending_position_contracts": previous_position,
                "row_net_pnl_amount": pnl_row["row_net_pnl_amount"],
                "total_cost_amount": cost_row["total_cost_amount"],
                "validation_row_hash": validation_row["row_hash"],
            }
        )
    return canonical_sha256(coherence_rows)


def _load_downstream_source(*, pack_root: Path, tbbo_root: Path) -> dict[str, Any]:
    cache = Sha256ArtifactCache()
    _verify_pack_hash(pack_root, "hourly_decision_completed_bar.csv")
    _verify_pack_hash(pack_root, "hourly_fill_completed_bar.csv")
    _verify_pack_hash(pack_root, "valuation_mark_completed_bar.csv")
    _verify_pack_hash(pack_root, "cost_parameter.csv")
    decision_rows = _index_rows(cache.read_csv_rows(pack_root / "hourly_decision_completed_bar.csv"))
    fill_rows = _index_rows(cache.read_csv_rows(pack_root / "hourly_fill_completed_bar.csv"))
    mark_rows = _index_rows(cache.read_csv_rows(pack_root / "valuation_mark_completed_bar.csv"))
    cost_rows = cache.read_csv_rows(pack_root / "cost_parameter.csv")
    if len(cost_rows) != 1:
        raise CarverBlocked("S27 v2 fast downstream cost parameter row count drift")
    tbbo_path = tbbo_root / COMBINED_TBBO_REGISTRY_NAME
    tbbo_sha = hashlib.sha256(tbbo_path.read_bytes()).hexdigest()
    tbbo_manifest = cache.read_json(tbbo_root / COMBINED_TBBO_REGISTRY_MANIFEST_NAME)
    if tbbo_manifest.get("registry") != COMBINED_TBBO_REGISTRY_NAME:
        raise CarverBlocked("S27 v2 fast downstream TBBO registry manifest file drift")
    if tbbo_manifest.get("registry_sha256") != tbbo_sha:
        raise CarverBlocked("S27 v2 fast downstream TBBO registry manifest hash drift")
    tbbo_rows = _index_rows(cache.read_csv_rows(tbbo_path))
    return {
        "decision": decision_rows,
        "fill": fill_rows,
        "mark": mark_rows,
        "cost": dict(cost_rows[0]),
        "tbbo": tbbo_rows,
        "tbbo_registry_sha": tbbo_sha,
    }


def _market_spread_row(
    *,
    tbbo: Mapping[int, Mapping[str, str]],
    row_index: int,
    side: str,
    fill_bar: Mapping[str, str],
) -> Mapping[str, str]:
    try:
        row = tbbo[row_index]
    except KeyError as exc:
        raise CarverBlocked(f"S27 v2 fast downstream missing market TBBO evidence for row {row_index}") from exc
    if row["fill_timestamp_utc"] != fill_bar["completed_timestamp_utc"]:
        raise CarverBlocked(f"S27 v2 fast downstream market TBBO fill timestamp drift at row {row_index}")
    if row["raw_symbol"] != fill_bar["raw_symbol"]:
        raise CarverBlocked(f"S27 v2 fast downstream market TBBO raw symbol drift at row {row_index}")
    if row["market_order_side"] != side:
        raise CarverBlocked(f"S27 v2 fast downstream market TBBO side drift at row {row_index}")
    if side == "BUY" and float(row["selected_executable_market_fill_price"]) != float(row["ask_px_00"]):
        raise CarverBlocked(f"S27 v2 fast downstream market BUY fill must bind selected ask at row {row_index}")
    if side == "SELL" and float(row["selected_executable_market_fill_price"]) != float(row["bid_px_00"]):
        raise CarverBlocked(f"S27 v2 fast downstream market SELL fill must bind selected bid at row {row_index}")
    return row


def _limit_fill(side: str, close_price: float, limit_price: float) -> bool:
    if side == "BUY":
        return close_price <= limit_price
    if side == "SELL":
        return close_price >= limit_price
    return False


def _limit_price_value(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _materialize_row(payload: Mapping[str, Any], ledger_name: str) -> dict[str, str]:
    typed = dict(payload)
    row_hash = canonical_sha256(typed)
    row = {field: _csv_value(typed.get(field, "")) for field in RUN_LEDGER_FIELDNAMES[ledger_name]}
    row["row_hash"] = row_hash
    return row


def _csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (dict, list, tuple)):
        import json

        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _bool_label(value: bool) -> str:
    return "TRUE" if value else "FALSE"


def _is_true(value: Any) -> bool:
    return value is True or str(value).upper() == "TRUE"


def _index_rows(rows: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...]) -> dict[int, Mapping[str, Any]]:
    return {int(row["row_index"]): row for row in rows}


def _resolve_pack_root(path: Path | str | None) -> Path:
    if path is None:
        return (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve()
    resolved = Path(path).resolve()
    if resolved != (_REPO_ROOT / DEFAULT_PACK_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 fast downstream pack root is locked")
    return resolved


def _resolve_tbbo_root(path: Path | str | None) -> Path:
    if path is None:
        return (_REPO_ROOT / DEFAULT_COMBINED_TBBO_RELATIVE_PATH).resolve()
    resolved = Path(path).resolve()
    if resolved != (_REPO_ROOT / DEFAULT_COMBINED_TBBO_RELATIVE_PATH).resolve():
        raise CarverBlocked("S27 v2 fast downstream TBBO root is locked")
    return resolved


def _verify_pack_hash(pack_root: Path, name: str) -> None:
    manifest = Sha256ArtifactCache().read_json(pack_root / INPUT_MANIFEST_NAME)
    expected = manifest.get("row_family_files", {}).get(name, {}).get("sha256")
    actual = hashlib.sha256((pack_root / name).read_bytes()).hexdigest()
    if expected != actual:
        raise CarverBlocked(f"S27 v2 fast downstream pack hash drift for {name}")


def _validate_dense_generated_counts(
    bundle: FastDownstreamGenerationBundle,
    rows: FastGeneratedDownstreamRows,
    segment_bundle: IncrementalSegmentBundle,
) -> None:
    expected_count = segment_bundle.segment_row_count
    dense_counts = {
        "transition": len(rows.transition_rows),
        "fill": len(rows.fill_rows),
        "cost": len(rows.cost_rows),
        "pnl": len(rows.pnl_rows),
        "validation": len(rows.validation_rows),
    }
    for family, observed_count in dense_counts.items():
        if observed_count != expected_count:
            raise CarverBlocked(f"S27 v2 fast downstream {family} row count drift")
    if bundle.generated_row_count != expected_count:
        raise CarverBlocked("S27 v2 fast downstream generated row count drift")


def _validate_active_artifact_authority(
    *,
    artifacts: FastSegmentArtifacts,
    segment_bundle: IncrementalSegmentBundle | None,
) -> IncrementalSegmentBundle:
    from .fast_execution_state import build_fast_execution_state_verification
    from .test_incremental_runner import build_incremental_segment_from_existing_artifacts

    active_segment = segment_bundle or build_incremental_segment_from_existing_artifacts()
    active_segment.validate_against_active_files()
    active_execution, _rows = build_fast_execution_state_verification(segment_bundle=active_segment)
    artifacts.validate(segment_bundle=active_segment, execution_state_verification=active_execution)
    return active_segment


def _validate_unique_row_indexes(rows: FastGeneratedDownstreamRows) -> None:
    row_families = {
        "working_order_transition_ledger.csv": rows.transition_rows,
        "fill_ledger.csv": rows.fill_rows,
        "market_fill_metadata_ledger.csv": rows.market_fill_metadata_rows,
        "cost_ledger.csv": rows.cost_rows,
        "pnl_ledger.csv": rows.pnl_rows,
        "validation_ledger.csv": rows.validation_rows,
    }
    for ledger_name, ledger_rows in row_families.items():
        indexes = [int(row["row_index"]) for row in ledger_rows]
        if len(indexes) != len(set(indexes)):
            raise CarverBlocked(f"S27 v2 fast downstream duplicate row index drift for {ledger_name}")


def _validate_order_rows_against_bundle(
    *,
    order_bundle: FastOrderGenerationBundle,
    order_rows: FastGeneratedOrderRows,
) -> None:
    if canonical_sha256(order_rows.desired_position_rows) != order_bundle.desired_position_rows_hash:
        raise CarverBlocked("S27 v2 fast downstream order desired rows hash drift")
    if canonical_sha256(order_rows.limit_order_rows) != order_bundle.limit_order_rows_hash:
        raise CarverBlocked("S27 v2 fast downstream order limit rows hash drift")
    if canonical_sha256(order_rows.no_market_order_rows) != order_bundle.no_market_order_rows_hash:
        raise CarverBlocked("S27 v2 fast downstream order no-market rows hash drift")
    if canonical_sha256(order_rows.market_order_rows) != order_bundle.market_order_rows_hash:
        raise CarverBlocked("S27 v2 fast downstream order market rows hash drift")


def _order_rows_hash(rows: FastGeneratedOrderRows) -> str:
    return canonical_sha256(
        {
            "desired_position_rows_hash": canonical_sha256(rows.desired_position_rows),
            "limit_order_rows_hash": canonical_sha256(rows.limit_order_rows),
            "no_market_order_rows_hash": canonical_sha256(rows.no_market_order_rows),
            "market_order_rows_hash": canonical_sha256(rows.market_order_rows),
        }
    )


def _rows_by_index(rows: tuple[Mapping[str, Any], ...]) -> dict[int, Mapping[str, Any]]:
    return {int(row["row_index"]): row for row in rows}


def _registry_payload(registry: FastDownstreamPolicyRegistry) -> dict[str, Any]:
    payload = asdict(registry)
    payload.pop("registry_hash", None)
    return payload


def _generation_bundle_payload(bundle: FastDownstreamGenerationBundle) -> dict[str, Any]:
    payload = asdict(bundle)
    payload.pop("bundle_hash", None)
    return payload

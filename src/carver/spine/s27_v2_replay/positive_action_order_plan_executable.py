from __future__ import annotations

import csv
from dataclasses import dataclass
from hashlib import sha256
from math import ceil, floor, isclose
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .desired_position_executable import (
    CONTRACT_POINT_VALUE,
    CONTRACT_POINT_VALUE_CURRENCY,
    PROVIDER_CONTRACT_MULTIPLIER_REJECTION_LABEL,
)
from .forecast_executable import FORECAST_CAP_VALUE, FORECAST_SCALAR_VALUE
from .local_replay import canonical_sha256
from .positive_action_executable import (
    EXPECTED_POSITIVE_ACTION_MANIFEST_SHA256,
    EXPECTED_RAW_SYMBOL,
    EXPECTED_SELECTED_DECISION,
    EXPECTED_SELECTED_FILL,
    POSITIVE_ACTION_PACK_RELATIVE_PATH,
    PositiveActionExecutableBundle,
    build_positive_action_executable_replay,
)
from .validation import require_finite_number, require_hash, require_integer, require_positive_number, require_text


S27_V2_POSITIVE_ACTION_ORDER_PLAN_AUTHORIZATION = (
    "S27_V2_LOCAL_ONLY_POSITIVE_ACTION_LIMIT_ORDER_POLICY_AND_EXECUTABLE_ORDER_PLAN"
)
S27_V2_POSITIVE_ACTION_ORDER_PLAN_STATUS = (
    "S27_V2_POSITIVE_ACTION_LIMIT_ORDER_PLAN_LOCAL_DEV_RECON_NOT_FILL_NOT_RESULT"
)

LIMIT_ORDER_PLAN_ROW_STATUS = "LOCAL_POSITIVE_ACTION_LIMIT_ORDER_ROW_EMITTED_NOT_FILL_NOT_RESULT"
NORMAL_TRANSITION_PLAN_ROW_STATUS = "LOCAL_POSITIVE_ACTION_NORMAL_TRANSITION_PLANNED_NOT_FILL"

LIMIT_ORDER_REASON_CODE = "S27_POSITIVE_ACTION_ADJACENT_SELL_LIMIT_ORDER_BOUND_TO_ACTIVE_PACKET"
NORMAL_TRANSITION_REASON_CODE = "S27_POSITIVE_ACTION_ONE_HOUR_SAME_SESSION_TRANSITION_PLANNED_NO_FILL_EMITTED"

ORDER_SIDE = "SELL"
ORDER_KIND = "LIMIT"
ORDER_QUANTITY = 1
CURRENT_POSITION = 0
TARGET_POSITION_AFTER_FILL = -1
POSITION_CHANGE = -1

ZN_TICK_SIZE = 0.015625
ZN_TICK_VALUE = 15.625
TICK_ROUNDING_POLICY_LABEL = (
    "LOCAL_ONLY_CONSERVATIVE_ZN_LIMIT_ROUNDING_BUY_DOWN_SELL_UP_TO_EXECUTABLE_TICK"
)
SELL_TICK_ROUNDING_DIRECTION = "ROUND_UP_TO_NEAREST_ZN_TICK_FOR_SELL_LIMIT"
NO_MARKET_ORDER_PROOF_LABEL = "PASS_NO_MARKET_ONE_CONTRACT_PRICEABLE_NON_CAP_ADJACENT_TARGET"
INITIAL_WORKING_STATE_POLICY_LABEL = "FIRST_ROW_FLAT_EMPTY_WORKING_STATE_CONTEXT"
NORMAL_TRANSITION_POLICY_LABEL = "ONE_HOUR_SAME_SESSION_SAME_RAW_SYMBOL_TRANSITION_PLANNED_NOT_FILL"
SESSION_PROOF_LABEL = "PASS_LOCAL_SAME_SESSION_DECISION_FILL_CANDIDATE"
ROLL_PROOF_LABEL = "PASS_LOCAL_NO_ROLL_BOUNDARY_ON_SELECTED_TRADING_DATE"
COST_POLICY_STATUS = "FAIL_CLOSED_SOURCE_NATIVE_COST_POLICY_UNRESOLVED_FOR_ACTUAL_COST_LEDGER"

_REPO_ROOT = Path(__file__).resolve().parents[4]
_POSITIVE_ACTION_PACK_PATH = (_REPO_ROOT / POSITIVE_ACTION_PACK_RELATIVE_PATH).resolve()
_STATIC_SPEC_PATH = (
    _REPO_ROOT
    / "docs"
    / "researchops"
    / "contract_specs"
    / "CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv"
)
_PROVIDER_DEFINITION_PATH = (
    _REPO_ROOT
    / "docs"
    / "researchops"
    / "s26_s27_hourly_bridge"
    / "ZN_S27_EWMAC16_TREND_DEPENDENCY"
    / "zn_lifecycle_databento_definition_probe_2026-05-31"
    / "raw_provider_metadata"
    / "20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_definition_dataframe.csv"
)
_EXPECTED_STATIC_SPEC_SHA256 = "908d9c147babf839ff4475f4286bf9e7828921f274f2d1a4a7a4cb5c2b7ead1d"
_EXPECTED_PROVIDER_DEFINITION_SHA256 = "cb1908e05cd41037a681a1a9aede56eb93001ad7c4576b048b15c87b0ec00742"
_EXPECTED_ZNM6_INSTRUMENT_ID = "42000661"
_EXPECTED_ZNM6_EXCHANGE = "XCBT"
_EXPECTED_ZNM6_ACTIVATION = "2025-09-19 21:30:00+00:00"
_EXPECTED_ZNM6_EXPIRATION = "2026-06-18 17:01:00+00:00"

ORDER_PLAN_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_MARKET_ORDER_EMISSION",
    "NO_FILL_EMISSION",
    "NO_COST_EMISSION",
    "NO_PNL_RESULT_EMISSION",
    "NO_RESULT_INTERPRETATION",
    "NO_PNL_EVALUATION",
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)


@dataclass(frozen=True)
class PositiveActionLimitOrderPlanRow:
    ledger_label: str
    row_status: str
    reason_code: str
    positive_action_bundle_hash: str
    positive_action_row_hash: str
    input_pack_path: str
    input_manifest_sha256: str
    selected_decision_timestamp_utc: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    current_position_before_order: int
    target_position_after_fill: int
    position_change_contracts: int
    order_required: bool
    order_kind: str
    order_side: str
    order_quantity: int
    formula_implied_limit_price: float
    executable_tick_limit_price: float
    tick_size: float
    tick_value: float
    tick_value_currency: str
    contract_point_value: float
    contract_point_value_currency: str
    static_spec_source_file_hash: str
    static_spec_zn_row_hash: str
    provider_definition_source_file_hash: str
    provider_definition_znm6_row_hash: str
    provider_instrument_id: str
    provider_activation: str
    provider_expiration: str
    provider_contract_multiplier_field_value: str
    provider_contract_multiplier_rejection_label: str
    tick_rounding_policy_label: str
    tick_rounding_policy_hash: str
    tick_rounding_direction: str
    no_market_order_proof_label: str
    no_market_order_proof_hash: str
    initial_working_state_policy_label: str
    initial_working_state_hash: str
    order_plan_hash: str
    limit_order_hash: str
    actual_market_order_rows_emitted: bool
    actual_fill_rows_emitted: bool
    actual_cost_rows_emitted: bool
    actual_pnl_rows_emitted: bool
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action limit-order row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_against_active(self, active_positive: PositiveActionExecutableBundle) -> None:
        if self.ledger_label != "POSITIVE_ACTION_LIMIT_ORDER_PLAN_LEDGER":
            raise CarverBlocked("S27 v2 positive-action limit-order ledger label is not locked")
        if self.row_status != LIMIT_ORDER_PLAN_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action limit-order status is not locked")
        if self.reason_code != LIMIT_ORDER_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action limit-order reason code is not locked")
        for name, hash_value in (
            ("positive-action bundle", self.positive_action_bundle_hash),
            ("positive-action row", self.positive_action_row_hash),
            ("manifest", self.input_manifest_sha256),
            ("static spec file", self.static_spec_source_file_hash),
            ("static ZN row", self.static_spec_zn_row_hash),
            ("provider definition file", self.provider_definition_source_file_hash),
            ("provider ZNM6 row", self.provider_definition_znm6_row_hash),
            ("tick rounding policy", self.tick_rounding_policy_hash),
            ("no-market proof", self.no_market_order_proof_hash),
            ("initial working state", self.initial_working_state_hash),
            ("order plan", self.order_plan_hash),
            ("limit order", self.limit_order_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action limit-order {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("decision timestamp", self.selected_decision_timestamp_utc),
            ("fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("order kind", self.order_kind),
            ("order side", self.order_side),
            ("tick value currency", self.tick_value_currency),
            ("point value currency", self.contract_point_value_currency),
            ("provider instrument id", self.provider_instrument_id),
            ("provider activation", self.provider_activation),
            ("provider expiration", self.provider_expiration),
            ("provider contract multiplier field", self.provider_contract_multiplier_field_value),
            ("provider multiplier rejection label", self.provider_contract_multiplier_rejection_label),
            ("tick rounding policy", self.tick_rounding_policy_label),
            ("tick rounding direction", self.tick_rounding_direction),
            ("no-market proof", self.no_market_order_proof_label),
            ("initial working-state policy", self.initial_working_state_policy_label),
        ):
            require_text(f"S27 v2 positive-action limit-order {name}", value)
        for name, value in (
            ("current position", self.current_position_before_order),
            ("target position", self.target_position_after_fill),
            ("position change", self.position_change_contracts),
            ("order quantity", self.order_quantity),
        ):
            require_integer(f"S27 v2 positive-action limit-order {name}", value)
        self._validate_locked_identity(active_positive)
        self._validate_static_and_provider_binding()
        self._validate_formula_tick_and_order_hashes(active_positive)
        if any(
            flag is not False
            for flag in (
                self.actual_market_order_rows_emitted,
                self.actual_fill_rows_emitted,
                self.actual_cost_rows_emitted,
                self.actual_pnl_rows_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action order-plan cannot emit market/fill/cost/PnL rows")
        if self.row_hash != canonical_sha256(_limit_order_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action limit-order row hash must be content-bound")

    def _validate_locked_identity(self, active_positive: PositiveActionExecutableBundle) -> None:
        active_row = active_positive.positive_action_row
        if self.positive_action_bundle_hash != active_positive.bundle_hash:
            raise CarverBlocked("S27 v2 positive-action limit-order must bind active positive-action bundle")
        if self.positive_action_row_hash != active_row.row_hash:
            raise CarverBlocked("S27 v2 positive-action limit-order must bind active positive-action row")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action order-plan is locked to the positive-action pack")
        if self.input_manifest_sha256 != EXPECTED_POSITIVE_ACTION_MANIFEST_SHA256:
            raise CarverBlocked("S27 v2 positive-action order-plan manifest hash is not locked")
        if self.selected_decision_timestamp_utc != EXPECTED_SELECTED_DECISION:
            raise CarverBlocked("S27 v2 positive-action order-plan decision timestamp is not locked")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 positive-action order-plan fill timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 positive-action order-plan raw symbol is not locked")
        if self.current_position_before_order != CURRENT_POSITION:
            raise CarverBlocked("S27 v2 positive-action order-plan first-row current position must be flat")
        if self.target_position_after_fill != TARGET_POSITION_AFTER_FILL:
            raise CarverBlocked("S27 v2 positive-action order-plan target must be adjacent short one")
        if self.position_change_contracts != POSITION_CHANGE:
            raise CarverBlocked("S27 v2 positive-action order-plan position change is not locked")
        if self.order_required is not True:
            raise CarverBlocked("S27 v2 positive-action order-plan must require one order")
        if self.order_kind != ORDER_KIND or self.order_side != ORDER_SIDE or self.order_quantity != ORDER_QUANTITY:
            raise CarverBlocked("S27 v2 positive-action order-plan must emit exactly SELL 1 limit order")
        if active_row.current_position_before_order != CURRENT_POSITION:
            raise CarverBlocked("S27 v2 active positive-action current position must remain flat")
        if active_row.desired_rounded_position != TARGET_POSITION_AFTER_FILL:
            raise CarverBlocked("S27 v2 active positive-action desired position must be -1")
        if active_row.position_change_contracts != POSITION_CHANGE:
            raise CarverBlocked("S27 v2 active positive-action position change must be -1")
        if active_row.order_side != ORDER_SIDE or active_row.order_quantity != ORDER_QUANTITY:
            raise CarverBlocked("S27 v2 active positive-action order intent must remain SELL 1")

    def _validate_static_and_provider_binding(self) -> None:
        if self.static_spec_source_file_hash != _verify_locked_file_hash(
            _STATIC_SPEC_PATH,
            _EXPECTED_STATIC_SPEC_SHA256,
            "Appendix C static ZN spec",
        ):
            raise CarverBlocked("S27 v2 positive-action static spec file hash mismatch")
        static_row = _locked_static_zn_row()
        _validate_static_zn_row_values(static_row)
        if self.static_spec_zn_row_hash != _source_row_hash("appendix_c_static_zn_execution_spec", static_row):
            raise CarverBlocked("S27 v2 positive-action static ZN row hash must bind active static row")
        provider_row = _locked_provider_znm6_row()
        if self.provider_definition_source_file_hash != _verify_locked_file_hash(
            _PROVIDER_DEFINITION_PATH,
            _EXPECTED_PROVIDER_DEFINITION_SHA256,
            "provider definition",
        ):
            raise CarverBlocked("S27 v2 positive-action provider definition file hash mismatch")
        if self.provider_definition_znm6_row_hash != _source_row_hash(
            "databento_provider_definition_znm6_execution",
            provider_row,
        ):
            raise CarverBlocked("S27 v2 positive-action provider ZNM6 row hash must bind active provider row")
        if self.provider_instrument_id != _EXPECTED_ZNM6_INSTRUMENT_ID:
            raise CarverBlocked("S27 v2 positive-action provider instrument id is not locked")
        if self.provider_activation != _EXPECTED_ZNM6_ACTIVATION or self.provider_expiration != _EXPECTED_ZNM6_EXPIRATION:
            raise CarverBlocked("S27 v2 positive-action provider effective window is not locked")
        if self.provider_contract_multiplier_field_value != "2147483647":
            raise CarverBlocked("S27 v2 positive-action provider multiplier sentinel must remain explicit")
        if self.provider_contract_multiplier_rejection_label != PROVIDER_CONTRACT_MULTIPLIER_REJECTION_LABEL:
            raise CarverBlocked("S27 v2 positive-action provider multiplier rejection label is not locked")
        if self.contract_point_value != CONTRACT_POINT_VALUE or self.contract_point_value_currency != CONTRACT_POINT_VALUE_CURRENCY:
            raise CarverBlocked("S27 v2 positive-action point value must bind Appendix C static authority")
        if self.tick_size != ZN_TICK_SIZE or self.tick_value != ZN_TICK_VALUE or self.tick_value_currency != "USD":
            raise CarverBlocked("S27 v2 positive-action ZN tick values must bind static evidence")

    def _validate_formula_tick_and_order_hashes(self, active_positive: PositiveActionExecutableBundle) -> None:
        row = active_positive.positive_action_row
        require_positive_number("S27 v2 positive-action formula-implied limit price", self.formula_implied_limit_price)
        require_positive_number("S27 v2 positive-action executable tick limit price", self.executable_tick_limit_price)
        expected_formula = _formula_implied_limit_price(row)
        _require_close("S27 v2 positive-action formula-implied limit price", self.formula_implied_limit_price, expected_formula)
        expected_tick_price = _round_limit_price_to_executable_tick(
            self.formula_implied_limit_price,
            ORDER_SIDE,
            self.tick_size,
        )
        _require_close("S27 v2 positive-action executable tick limit price", self.executable_tick_limit_price, expected_tick_price)
        if self.executable_tick_limit_price < self.formula_implied_limit_price:
            raise CarverBlocked("S27 v2 positive-action sell limit executable price cannot improve fill versus formula")
        if self.tick_rounding_policy_label != TICK_ROUNDING_POLICY_LABEL:
            raise CarverBlocked("S27 v2 positive-action tick rounding policy label is not locked")
        if self.tick_rounding_direction != SELL_TICK_ROUNDING_DIRECTION:
            raise CarverBlocked("S27 v2 positive-action sell tick rounding direction is not locked")
        if self.tick_rounding_policy_hash != _policy_hash(
            "tick_rounding",
            TICK_ROUNDING_POLICY_LABEL,
            SELL_TICK_ROUNDING_DIRECTION,
            self.tick_size,
        ):
            raise CarverBlocked("S27 v2 positive-action tick rounding policy hash must bind policy")
        if self.no_market_order_proof_label != NO_MARKET_ORDER_PROOF_LABEL:
            raise CarverBlocked("S27 v2 positive-action no-market proof label is not locked")
        if self.no_market_order_proof_hash != _policy_hash(
            "no_market_order_proof",
            NO_MARKET_ORDER_PROOF_LABEL,
            self.current_position_before_order,
            self.target_position_after_fill,
            row.capped_forecast_value,
            FORECAST_CAP_VALUE,
        ):
            raise CarverBlocked("S27 v2 positive-action no-market proof hash must bind source condition")
        if self.initial_working_state_policy_label != INITIAL_WORKING_STATE_POLICY_LABEL:
            raise CarverBlocked("S27 v2 positive-action initial working-state policy is not locked")
        if self.initial_working_state_hash != _policy_hash(
            "initial_working_state",
            INITIAL_WORKING_STATE_POLICY_LABEL,
            self.raw_symbol,
            self.selected_decision_timestamp_utc,
            self.current_position_before_order,
            "EMPTY_WORKING_ORDER_SET",
        ):
            raise CarverBlocked("S27 v2 positive-action initial working-state hash must bind empty first-row context")
        if self.order_plan_hash != _order_plan_hash(self):
            raise CarverBlocked("S27 v2 positive-action order-plan hash must bind active order plan")
        if self.limit_order_hash != _limit_order_hash(self):
            raise CarverBlocked("S27 v2 positive-action limit-order hash must bind row fields")


@dataclass(frozen=True)
class PositiveActionNormalTransitionPlanRow:
    ledger_label: str
    row_status: str
    reason_code: str
    positive_action_bundle_hash: str
    limit_order_hash: str
    order_plan_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    selected_fill_timestamp_utc: str
    raw_symbol: str
    session_calendar_row_hash: str
    roll_calendar_row_hash: str
    hourly_fill_row_hash: str
    session_proof_label: str
    session_proof_hash: str
    roll_proof_label: str
    roll_proof_hash: str
    normal_transition_policy_label: str
    normal_transition_policy_hash: str
    working_order_state_before_hash: str
    working_order_state_after_planned_hash: str
    fill_rows_emitted: bool
    actual_fill_ledger_status: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 positive-action transition-plan row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_against_limit_row(self, limit_row: PositiveActionLimitOrderPlanRow) -> None:
        if self.ledger_label != "POSITIVE_ACTION_NORMAL_TRANSITION_PLAN_LEDGER":
            raise CarverBlocked("S27 v2 positive-action transition-plan ledger label is not locked")
        if self.row_status != NORMAL_TRANSITION_PLAN_ROW_STATUS:
            raise CarverBlocked("S27 v2 positive-action transition-plan status is not locked")
        if self.reason_code != NORMAL_TRANSITION_REASON_CODE:
            raise CarverBlocked("S27 v2 positive-action transition-plan reason is not locked")
        for name, hash_value in (
            ("positive-action bundle", self.positive_action_bundle_hash),
            ("limit order", self.limit_order_hash),
            ("order plan", self.order_plan_hash),
            ("session row", self.session_calendar_row_hash),
            ("roll row", self.roll_calendar_row_hash),
            ("hourly fill row", self.hourly_fill_row_hash),
            ("session proof", self.session_proof_hash),
            ("roll proof", self.roll_proof_hash),
            ("normal transition policy", self.normal_transition_policy_hash),
            ("working state before", self.working_order_state_before_hash),
            ("working state planned after", self.working_order_state_after_planned_hash),
            ("row", self.row_hash),
        ):
            require_hash(f"S27 v2 positive-action transition-plan {name} hash", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("decision timestamp", self.selected_decision_timestamp_utc),
            ("fill timestamp", self.selected_fill_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("session proof", self.session_proof_label),
            ("roll proof", self.roll_proof_label),
            ("normal transition policy", self.normal_transition_policy_label),
            ("actual fill ledger status", self.actual_fill_ledger_status),
        ):
            require_text(f"S27 v2 positive-action transition-plan {name}", value)
        if self.positive_action_bundle_hash != limit_row.positive_action_bundle_hash:
            raise CarverBlocked("S27 v2 transition plan must bind active positive-action bundle")
        if self.limit_order_hash != limit_row.limit_order_hash or self.order_plan_hash != limit_row.order_plan_hash:
            raise CarverBlocked("S27 v2 transition plan must bind active limit order and order plan")
        if self.input_pack_path != limit_row.input_pack_path:
            raise CarverBlocked("S27 v2 transition plan must bind same input pack")
        if self.selected_decision_timestamp_utc != EXPECTED_SELECTED_DECISION:
            raise CarverBlocked("S27 v2 transition plan decision timestamp is not locked")
        if self.selected_fill_timestamp_utc != EXPECTED_SELECTED_FILL:
            raise CarverBlocked("S27 v2 transition plan fill timestamp is not locked")
        if self.raw_symbol != EXPECTED_RAW_SYMBOL:
            raise CarverBlocked("S27 v2 transition plan raw symbol is not locked")
        session_row = _locked_session_row()
        roll_row = _locked_roll_row()
        rows_by_file = _read_pack_rows(_POSITIVE_ACTION_PACK_PATH)
        hourly_fill_hash = _row_hashes_by_file(rows_by_file)["hourly_fill_completed_bar.csv"][0]
        if self.session_calendar_row_hash != _source_row_hash("positive_action_session_calendar_row", session_row):
            raise CarverBlocked("S27 v2 transition plan session row hash must bind active session row")
        if self.roll_calendar_row_hash != _source_row_hash("positive_action_roll_calendar_row", roll_row):
            raise CarverBlocked("S27 v2 transition plan roll row hash must bind active roll row")
        if self.hourly_fill_row_hash != hourly_fill_hash:
            raise CarverBlocked("S27 v2 transition plan hourly fill row hash must bind declared fill row")
        _validate_same_session_transition(session_row)
        _validate_no_roll_boundary(roll_row)
        if self.session_proof_label != SESSION_PROOF_LABEL:
            raise CarverBlocked("S27 v2 transition plan session proof label is not locked")
        if self.session_proof_hash != _policy_hash(
            "session_proof",
            SESSION_PROOF_LABEL,
            session_row,
            EXPECTED_SELECTED_DECISION,
            EXPECTED_SELECTED_FILL,
        ):
            raise CarverBlocked("S27 v2 transition plan session proof hash must bind session evidence")
        if self.roll_proof_label != ROLL_PROOF_LABEL:
            raise CarverBlocked("S27 v2 transition plan roll proof label is not locked")
        if self.roll_proof_hash != _policy_hash(
            "roll_proof",
            ROLL_PROOF_LABEL,
            roll_row,
            EXPECTED_SELECTED_DECISION[:10],
            EXPECTED_RAW_SYMBOL,
        ):
            raise CarverBlocked("S27 v2 transition plan roll proof hash must bind roll evidence")
        if self.normal_transition_policy_label != NORMAL_TRANSITION_POLICY_LABEL:
            raise CarverBlocked("S27 v2 transition plan normal-transition policy is not locked")
        if self.normal_transition_policy_hash != _policy_hash(
            "normal_transition_policy",
            NORMAL_TRANSITION_POLICY_LABEL,
            self.session_proof_hash,
            self.roll_proof_hash,
            self.hourly_fill_row_hash,
        ):
            raise CarverBlocked("S27 v2 transition plan normal-transition hash must bind evidence")
        if self.working_order_state_before_hash != limit_row.initial_working_state_hash:
            raise CarverBlocked("S27 v2 transition plan must start from the active initial working state")
        if self.working_order_state_after_planned_hash != _policy_hash(
            "planned_working_state_after_order_submission",
            "LIMIT_ORDER_WORKING_PENDING_FILL_DECISION_NOT_FILLED",
            limit_row.limit_order_hash,
            EXPECTED_SELECTED_FILL,
        ):
            raise CarverBlocked("S27 v2 transition plan working state after hash must bind pending limit")
        if self.fill_rows_emitted is not False:
            raise CarverBlocked("S27 v2 transition plan cannot emit fill rows")
        if self.actual_fill_ledger_status != "FAIL_CLOSED_ACTUAL_FILL_LEDGER_NOT_EMITTED":
            raise CarverBlocked("S27 v2 transition plan actual fill status must remain fail-closed")
        if self.row_hash != canonical_sha256(_transition_plan_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 transition-plan row hash must be content-bound")


@dataclass(frozen=True)
class PositiveActionOrderPlanExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    positive_action_bundle: PositiveActionExecutableBundle
    limit_order_row: PositiveActionLimitOrderPlanRow
    transition_plan_row: PositiveActionNormalTransitionPlanRow
    limit_order_rows_emitted: bool
    market_order_rows_emitted: bool
    transition_metadata_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_metadata_rows_emitted: bool
    provenance_metadata_rows_emitted: bool
    trusted_bundle_metadata_emitted: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = ORDER_PLAN_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITIVE_ACTION_ORDER_PLAN_STATUS:
            raise CarverBlocked("S27 v2 positive-action order-plan bundle status is not locked")
        if self.authorization_label != S27_V2_POSITIVE_ACTION_ORDER_PLAN_AUTHORIZATION:
            raise CarverBlocked("S27 v2 positive-action order-plan authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 positive-action order-plan must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 positive-action order-plan lane must remain source-native futures")
        if Path(self.input_pack_path).resolve() != _POSITIVE_ACTION_PACK_PATH:
            raise CarverBlocked("S27 v2 positive-action order-plan is locked to the declared positive-action pack")
        active_positive = build_positive_action_executable_replay(_POSITIVE_ACTION_PACK_PATH)
        self.positive_action_bundle.validate()
        if self.positive_action_bundle != active_positive:
            raise CarverBlocked("S27 v2 positive-action order-plan must bind active positive-action bundle")
        self.limit_order_row._validate_against_active(active_positive)
        self.transition_plan_row._validate_against_limit_row(self.limit_order_row)
        if any(
            flag is not True
            for flag in (
                self.limit_order_rows_emitted,
                self.transition_metadata_rows_emitted,
                self.validation_metadata_rows_emitted,
                self.provenance_metadata_rows_emitted,
                self.trusted_bundle_metadata_emitted,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action order-plan must emit only authorized order metadata surfaces")
        if any(
            flag is not False
            for flag in (
                self.market_order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 positive-action order-plan cannot emit market/fill/cost/PnL/result/evidence")
        if self.non_authorizations != ORDER_PLAN_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 positive-action order-plan must preserve non-authorizations")
        require_hash("S27 v2 positive-action order-plan bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_order_plan_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 positive-action order-plan bundle hash must be content-bound")


def build_positive_action_limit_order_plan(
    input_pack_path: str | Path = _POSITIVE_ACTION_PACK_PATH,
) -> PositiveActionOrderPlanExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _POSITIVE_ACTION_PACK_PATH:
        raise CarverBlocked("S27 v2 positive-action order-plan is locked to the declared positive-action pack")
    positive_bundle = build_positive_action_executable_replay(pack_path)
    limit_row = _build_limit_order_row(pack_path, positive_bundle)
    transition_row = _build_transition_plan_row(pack_path, positive_bundle, limit_row)
    bundle = PositiveActionOrderPlanExecutableBundle(
        status=S27_V2_POSITIVE_ACTION_ORDER_PLAN_STATUS,
        authorization_label=S27_V2_POSITIVE_ACTION_ORDER_PLAN_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        positive_action_bundle=positive_bundle,
        limit_order_row=limit_row,
        transition_plan_row=transition_row,
        limit_order_rows_emitted=True,
        market_order_rows_emitted=False,
        transition_metadata_rows_emitted=True,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_metadata_rows_emitted=True,
        provenance_metadata_rows_emitted=True,
        trusted_bundle_metadata_emitted=True,
        bundle_hash="0" * 64,
    )
    bundle = PositiveActionOrderPlanExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_order_plan_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_limit_order_row(
    pack_path: Path,
    positive_bundle: PositiveActionExecutableBundle,
) -> PositiveActionLimitOrderPlanRow:
    active_row = positive_bundle.positive_action_row
    static_row = _locked_static_zn_row()
    provider_row = _locked_provider_znm6_row()
    formula_price = _formula_implied_limit_price(active_row)
    executable_price = _round_limit_price_to_executable_tick(formula_price, ORDER_SIDE, ZN_TICK_SIZE)
    initial_state_hash = _policy_hash(
        "initial_working_state",
        INITIAL_WORKING_STATE_POLICY_LABEL,
        EXPECTED_RAW_SYMBOL,
        EXPECTED_SELECTED_DECISION,
        CURRENT_POSITION,
        "EMPTY_WORKING_ORDER_SET",
    )
    row = PositiveActionLimitOrderPlanRow(
        ledger_label="POSITIVE_ACTION_LIMIT_ORDER_PLAN_LEDGER",
        row_status=LIMIT_ORDER_PLAN_ROW_STATUS,
        reason_code=LIMIT_ORDER_REASON_CODE,
        positive_action_bundle_hash=positive_bundle.bundle_hash,
        positive_action_row_hash=active_row.row_hash,
        input_pack_path=str(pack_path),
        input_manifest_sha256=EXPECTED_POSITIVE_ACTION_MANIFEST_SHA256,
        selected_decision_timestamp_utc=EXPECTED_SELECTED_DECISION,
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        current_position_before_order=CURRENT_POSITION,
        target_position_after_fill=TARGET_POSITION_AFTER_FILL,
        position_change_contracts=POSITION_CHANGE,
        order_required=True,
        order_kind=ORDER_KIND,
        order_side=ORDER_SIDE,
        order_quantity=ORDER_QUANTITY,
        formula_implied_limit_price=formula_price,
        executable_tick_limit_price=executable_price,
        tick_size=ZN_TICK_SIZE,
        tick_value=ZN_TICK_VALUE,
        tick_value_currency="USD",
        contract_point_value=CONTRACT_POINT_VALUE,
        contract_point_value_currency=CONTRACT_POINT_VALUE_CURRENCY,
        static_spec_source_file_hash=_verify_locked_file_hash(
            _STATIC_SPEC_PATH,
            _EXPECTED_STATIC_SPEC_SHA256,
            "Appendix C static ZN spec",
        ),
        static_spec_zn_row_hash=_source_row_hash("appendix_c_static_zn_execution_spec", static_row),
        provider_definition_source_file_hash=_verify_locked_file_hash(
            _PROVIDER_DEFINITION_PATH,
            _EXPECTED_PROVIDER_DEFINITION_SHA256,
            "provider definition",
        ),
        provider_definition_znm6_row_hash=_source_row_hash("databento_provider_definition_znm6_execution", provider_row),
        provider_instrument_id=provider_row["instrument_id"],
        provider_activation=provider_row["activation"],
        provider_expiration=provider_row["expiration"],
        provider_contract_multiplier_field_value=provider_row["contract_multiplier"],
        provider_contract_multiplier_rejection_label=PROVIDER_CONTRACT_MULTIPLIER_REJECTION_LABEL,
        tick_rounding_policy_label=TICK_ROUNDING_POLICY_LABEL,
        tick_rounding_policy_hash=_policy_hash(
            "tick_rounding",
            TICK_ROUNDING_POLICY_LABEL,
            SELL_TICK_ROUNDING_DIRECTION,
            ZN_TICK_SIZE,
        ),
        tick_rounding_direction=SELL_TICK_ROUNDING_DIRECTION,
        no_market_order_proof_label=NO_MARKET_ORDER_PROOF_LABEL,
        no_market_order_proof_hash=_policy_hash(
            "no_market_order_proof",
            NO_MARKET_ORDER_PROOF_LABEL,
            CURRENT_POSITION,
            TARGET_POSITION_AFTER_FILL,
            active_row.capped_forecast_value,
            FORECAST_CAP_VALUE,
        ),
        initial_working_state_policy_label=INITIAL_WORKING_STATE_POLICY_LABEL,
        initial_working_state_hash=initial_state_hash,
        order_plan_hash="0" * 64,
        limit_order_hash="0" * 64,
        actual_market_order_rows_emitted=False,
        actual_fill_rows_emitted=False,
        actual_cost_rows_emitted=False,
        actual_pnl_rows_emitted=False,
        row_hash="0" * 64,
    )
    row = PositiveActionLimitOrderPlanRow(
        **{**row.__dict__, "order_plan_hash": _order_plan_hash(row)}
    )
    row = PositiveActionLimitOrderPlanRow(
        **{**row.__dict__, "limit_order_hash": _limit_order_hash(row)}
    )
    row = PositiveActionLimitOrderPlanRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_limit_order_row_hash_payload(row))}
    )
    row._validate_against_active(positive_bundle)
    return row


def _build_transition_plan_row(
    pack_path: Path,
    positive_bundle: PositiveActionExecutableBundle,
    limit_row: PositiveActionLimitOrderPlanRow,
) -> PositiveActionNormalTransitionPlanRow:
    session_row = _locked_session_row()
    roll_row = _locked_roll_row()
    _validate_same_session_transition(session_row)
    _validate_no_roll_boundary(roll_row)
    rows_by_file = _read_pack_rows(pack_path)
    hourly_fill_hash = _row_hashes_by_file(rows_by_file)["hourly_fill_completed_bar.csv"][0]
    session_hash = _source_row_hash("positive_action_session_calendar_row", session_row)
    roll_hash = _source_row_hash("positive_action_roll_calendar_row", roll_row)
    session_proof_hash = _policy_hash(
        "session_proof",
        SESSION_PROOF_LABEL,
        session_row,
        EXPECTED_SELECTED_DECISION,
        EXPECTED_SELECTED_FILL,
    )
    roll_proof_hash = _policy_hash(
        "roll_proof",
        ROLL_PROOF_LABEL,
        roll_row,
        EXPECTED_SELECTED_DECISION[:10],
        EXPECTED_RAW_SYMBOL,
    )
    normal_transition_hash = _policy_hash(
        "normal_transition_policy",
        NORMAL_TRANSITION_POLICY_LABEL,
        session_proof_hash,
        roll_proof_hash,
        hourly_fill_hash,
    )
    row = PositiveActionNormalTransitionPlanRow(
        ledger_label="POSITIVE_ACTION_NORMAL_TRANSITION_PLAN_LEDGER",
        row_status=NORMAL_TRANSITION_PLAN_ROW_STATUS,
        reason_code=NORMAL_TRANSITION_REASON_CODE,
        positive_action_bundle_hash=positive_bundle.bundle_hash,
        limit_order_hash=limit_row.limit_order_hash,
        order_plan_hash=limit_row.order_plan_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=EXPECTED_SELECTED_DECISION,
        selected_fill_timestamp_utc=EXPECTED_SELECTED_FILL,
        raw_symbol=EXPECTED_RAW_SYMBOL,
        session_calendar_row_hash=session_hash,
        roll_calendar_row_hash=roll_hash,
        hourly_fill_row_hash=hourly_fill_hash,
        session_proof_label=SESSION_PROOF_LABEL,
        session_proof_hash=session_proof_hash,
        roll_proof_label=ROLL_PROOF_LABEL,
        roll_proof_hash=roll_proof_hash,
        normal_transition_policy_label=NORMAL_TRANSITION_POLICY_LABEL,
        normal_transition_policy_hash=normal_transition_hash,
        working_order_state_before_hash=limit_row.initial_working_state_hash,
        working_order_state_after_planned_hash=_policy_hash(
            "planned_working_state_after_order_submission",
            "LIMIT_ORDER_WORKING_PENDING_FILL_DECISION_NOT_FILLED",
            limit_row.limit_order_hash,
            EXPECTED_SELECTED_FILL,
        ),
        fill_rows_emitted=False,
        actual_fill_ledger_status="FAIL_CLOSED_ACTUAL_FILL_LEDGER_NOT_EMITTED",
        row_hash="0" * 64,
    )
    row = PositiveActionNormalTransitionPlanRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_transition_plan_row_hash_payload(row))}
    )
    row._validate_against_limit_row(limit_row)
    return row


def _formula_implied_limit_price(active_row: Any) -> float:
    target_capped_forecast = TARGET_POSITION_AFTER_FILL / active_row.base_unrounded_contracts * 10.0
    if abs(target_capped_forecast) >= FORECAST_CAP_VALUE:
        raise CarverBlocked("S27 v2 positive-action adjacent target is not priceable")
    if active_row.ewmac16_64_trend_value >= 0.0:
        raise CarverBlocked("S27 v2 positive-action sell target must be trend-permitted by negative EWMAC")
    target_risk_adjusted = target_capped_forecast / FORECAST_SCALAR_VALUE
    pre_vol_risk_adjusted = target_risk_adjusted / active_row.ewma10_multiplier_m_value
    implied = active_row.ewma5_equilibrium_value - pre_vol_risk_adjusted * active_row.sigma_price_value
    require_positive_number("S27 v2 positive-action formula-implied limit price", implied)
    return implied


def _round_limit_price_to_executable_tick(price: float, side: str, tick_size: float) -> float:
    require_positive_number("S27 v2 positive-action limit price", price)
    require_positive_number("S27 v2 positive-action tick size", tick_size)
    if side == "SELL":
        return ceil((price - 1e-12) / tick_size) * tick_size
    if side == "BUY":
        return floor((price + 1e-12) / tick_size) * tick_size
    raise CarverBlocked("S27 v2 positive-action limit side is unresolved")


def _locked_static_zn_row() -> dict[str, str]:
    _verify_locked_file_hash(_STATIC_SPEC_PATH, _EXPECTED_STATIC_SPEC_SHA256, "Appendix C static ZN spec")
    rows = [row for row in _read_csv_rows(_STATIC_SPEC_PATH) if row.get("author_market_code") == "ZN"]
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 positive-action static ZN spec must have exactly one row")
    row = rows[0]
    _validate_static_zn_row_values(row)
    return row


def _validate_static_zn_row_values(row: dict[str, str]) -> None:
    if row.get("official_product_code") != "ZN":
        raise CarverBlocked("S27 v2 positive-action static spec must bind ZN")
    if row.get("official_currency") != "USD":
        raise CarverBlocked("S27 v2 positive-action static spec must bind USD")
    if float(row.get("official_point_value", "nan")) != CONTRACT_POINT_VALUE:
        raise CarverBlocked("S27 v2 positive-action static spec must bind 1000 USD point value")
    if float(row.get("official_tick_size", "nan")) != ZN_TICK_SIZE:
        raise CarverBlocked("S27 v2 positive-action static spec must bind ZN tick size")
    if float(row.get("official_tick_value", "nan")) != ZN_TICK_VALUE:
        raise CarverBlocked("S27 v2 positive-action static spec must bind ZN tick value")


def _locked_provider_znm6_row() -> dict[str, str]:
    _verify_locked_file_hash(_PROVIDER_DEFINITION_PATH, _EXPECTED_PROVIDER_DEFINITION_SHA256, "provider definition")
    rows = [row for row in _read_csv_rows(_PROVIDER_DEFINITION_PATH) if row.get("raw_symbol") == EXPECTED_RAW_SYMBOL]
    selected_key = _utc_second_key(EXPECTED_SELECTED_DECISION)
    active_prior = [
        row
        for row in rows
        if _utc_second_key(row.get("activation", "")) <= selected_key <= _utc_second_key(row.get("expiration", ""))
        and _utc_second_key(row.get("ts_recv", "")) <= selected_key
    ]
    if not active_prior:
        raise CarverBlocked("S27 v2 positive-action provider definition must bind an active prior ZNM6 row")
    latest_key = max(_utc_second_key(row.get("ts_recv", "")) for row in active_prior)
    latest_rows = [row for row in active_prior if _utc_second_key(row.get("ts_recv", "")) == latest_key]
    if len(latest_rows) != 1:
        raise CarverBlocked("S27 v2 positive-action provider definition latest prior ZNM6 row must be unique")
    row = latest_rows[0]
    if row.get("instrument_id") != _EXPECTED_ZNM6_INSTRUMENT_ID:
        raise CarverBlocked("S27 v2 positive-action provider definition must bind ZNM6 instrument id")
    if row.get("exchange") != _EXPECTED_ZNM6_EXCHANGE:
        raise CarverBlocked("S27 v2 positive-action provider definition must bind XCBT")
    if row.get("activation") != _EXPECTED_ZNM6_ACTIVATION or row.get("expiration") != _EXPECTED_ZNM6_EXPIRATION:
        raise CarverBlocked("S27 v2 positive-action provider definition effective dates are not locked")
    if row.get("currency") != "USD":
        raise CarverBlocked("S27 v2 positive-action provider definition must bind USD")
    if row.get("group") != "ZN" or row.get("asset") != "ZN" or row.get("security_type") != "FUT":
        raise CarverBlocked("S27 v2 positive-action provider definition must bind ZN future")
    if row.get("contract_multiplier") != "2147483647":
        raise CarverBlocked("S27 v2 positive-action provider multiplier sentinel must remain explicit")
    return row


def _locked_session_row() -> dict[str, str]:
    rows = _read_csv_rows(_POSITIVE_ACTION_PACK_PATH / "session_calendar.csv")
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 positive-action session calendar must have one row")
    return rows[0]


def _locked_roll_row() -> dict[str, str]:
    rows = _read_csv_rows(_POSITIVE_ACTION_PACK_PATH / "roll_calendar.csv")
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 positive-action roll calendar must have one row")
    return rows[0]


def _validate_same_session_transition(row: dict[str, str]) -> None:
    if row.get("raw_symbol") != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 positive-action session row must bind ZNM6")
    if row.get("trading_date") != EXPECTED_SELECTED_DECISION[:10]:
        raise CarverBlocked("S27 v2 positive-action session row must bind selected trading date")
    if row.get("readiness_status") != "READY_SESSION_CALENDAR_LOCAL_RUNTIME_EVIDENCE_RECON_NOT_EXECUTION_POLICY":
        raise CarverBlocked("S27 v2 positive-action session row must remain local execution-planning evidence")
    if not (row.get("session_open_utc", "") < EXPECTED_SELECTED_DECISION < EXPECTED_SELECTED_FILL < row.get("session_close_utc", "")):
        raise CarverBlocked("S27 v2 positive-action decision/fill candidate must be inside one session")


def _validate_no_roll_boundary(row: dict[str, str]) -> None:
    if row.get("incoming_raw_symbol") != EXPECTED_RAW_SYMBOL:
        raise CarverBlocked("S27 v2 positive-action roll row must bind incoming ZNM6")
    if row.get("trading_date") == EXPECTED_SELECTED_DECISION[:10]:
        raise CarverBlocked("S27 v2 positive-action selected row cannot be on a roll boundary")
    if row.get("readiness_status") != "READY_ROLL_CALENDAR_LOCAL_RUNTIME_EVIDENCE_RECON_NOT_EXECUTION_POLICY":
        raise CarverBlocked("S27 v2 positive-action roll row must remain local execution-planning evidence")


def _read_pack_rows(pack_path: Path) -> dict[str, tuple[dict[str, str], ...]]:
    return {
        filename: tuple(_read_csv_rows(pack_path / filename))
        for filename in (
            "daily_continuous_completed_bar.csv",
            "daily_current_contract_completed_bar.csv",
            "hourly_decision_completed_bar.csv",
            "hourly_fill_completed_bar.csv",
            "session_calendar.csv",
            "roll_calendar.csv",
            "cost_parameter.csv",
        )
    }


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise CarverBlocked(f"S27 v2 positive-action order-plan source file {path.name} has no rows")
    return rows


def _row_hashes_by_file(rows_by_file: dict[str, tuple[dict[str, str], ...]]) -> dict[str, tuple[str, ...]]:
    row_family_by_file = {
        "daily_continuous_completed_bar.csv": "DAILY_CONTINUOUS_COMPLETED_BAR",
        "daily_current_contract_completed_bar.csv": "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
        "hourly_decision_completed_bar.csv": "HOURLY_DECISION_COMPLETED_BAR",
        "hourly_fill_completed_bar.csv": "HOURLY_FILL_COMPLETED_BAR",
        "session_calendar.csv": "SESSION_CALENDAR",
        "roll_calendar.csv": "ROLL_CALENDAR",
        "cost_parameter.csv": "COST_PARAMETER",
    }
    return {
        filename: tuple(
            canonical_sha256(
                {
                    "artifact": "S27_V2_LOCAL_SOURCE_ROW",
                    "row_family": row_family_by_file[filename],
                    "row_number": row_number,
                    "row": row,
                }
            )
            for row_number, row in enumerate(rows, start=1)
        )
        for filename, rows in rows_by_file.items()
    }


def _verify_locked_file_hash(path: Path, expected_hash: str, label: str) -> str:
    observed_hash = sha256(path.read_bytes()).hexdigest()
    if observed_hash != expected_hash:
        raise CarverBlocked(f"S27 v2 positive-action {label} byte hash must match audited packet")
    return observed_hash


def _utc_second_key(value: str) -> str:
    require_text("S27 v2 positive-action provider timestamp", value)
    normalized = value.replace(" ", "T")
    if normalized.endswith("+00:00"):
        normalized = normalized[:-6] + "Z"
    if not normalized.endswith("Z"):
        raise CarverBlocked("S27 v2 positive-action provider timestamp must be UTC")
    return normalized[:19]


def _require_close(name: str, observed: float, expected: float) -> None:
    require_finite_number(name, observed)
    require_finite_number(f"{name} expected", expected)
    if not isclose(observed, expected, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked(f"{name} must bind source formula")


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_ORDER_PLAN_POLICY", "label": label, "values": values})


def _source_row_hash(label: str, row: dict[str, str]) -> str:
    return canonical_sha256({"artifact": "S27_V2_POSITIVE_ACTION_ORDER_PLAN_SOURCE_ROW", "label": label, "row": row})


def _order_plan_hash(row: PositiveActionLimitOrderPlanRow) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_POSITIVE_ACTION_ORDER_PLAN",
            "positive_action_bundle_hash": row.positive_action_bundle_hash,
            "current_position": row.current_position_before_order,
            "target_position": row.target_position_after_fill,
            "order_side": row.order_side,
            "order_quantity": row.order_quantity,
            "formula_implied_limit_price": row.formula_implied_limit_price,
            "executable_tick_limit_price": row.executable_tick_limit_price,
            "tick_rounding_policy_hash": row.tick_rounding_policy_hash,
            "no_market_order_proof_hash": row.no_market_order_proof_hash,
            "initial_working_state_hash": row.initial_working_state_hash,
        }
    )


def _limit_order_hash(row: PositiveActionLimitOrderPlanRow) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_POSITIVE_ACTION_LIMIT_ORDER",
            "order_plan_hash": row.order_plan_hash,
            "decision_timestamp": row.selected_decision_timestamp_utc,
            "raw_symbol": row.raw_symbol,
            "side": row.order_side,
            "quantity": row.order_quantity,
            "current_position": row.current_position_before_order,
            "target_position_after_fill": row.target_position_after_fill,
            "formula_implied_limit_price": row.formula_implied_limit_price,
            "executable_tick_limit_price": row.executable_tick_limit_price,
            "tick_size": row.tick_size,
            "tick_rounding_direction": row.tick_rounding_direction,
        }
    )


def _limit_order_row_hash_payload(row: PositiveActionLimitOrderPlanRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _transition_plan_row_hash_payload(row: PositiveActionNormalTransitionPlanRow) -> dict[str, object]:
    return {key: value for key, value in row.__dict__.items() if key != "row_hash"}


def _order_plan_bundle_hash_payload(bundle: PositiveActionOrderPlanExecutableBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_POSITIVE_ACTION_ORDER_PLAN_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "fill_rows_emitted": bundle.fill_rows_emitted,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "limit_order_row_hash": bundle.limit_order_row.row_hash,
        "limit_order_rows_emitted": bundle.limit_order_rows_emitted,
        "market_order_rows_emitted": bundle.market_order_rows_emitted,
        "non_authorizations": bundle.non_authorizations,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "positive_action_bundle_hash": bundle.positive_action_bundle.bundle_hash,
        "provenance_metadata_rows_emitted": bundle.provenance_metadata_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
        "transition_metadata_rows_emitted": bundle.transition_metadata_rows_emitted,
        "transition_plan_row_hash": bundle.transition_plan_row.row_hash,
        "trusted_bundle_metadata_emitted": bundle.trusted_bundle_metadata_emitted,
        "validation_metadata_rows_emitted": bundle.validation_metadata_rows_emitted,
    }

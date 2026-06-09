from __future__ import annotations

import csv
from dataclasses import dataclass
from hashlib import sha256
from math import floor, isclose
from pathlib import Path
from typing import Any

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .forecast_executable import (
    ForecastExecutableBundle,
    build_forecast_executable_ledgers_on_remediation_pack,
)
from .local_replay import canonical_sha256
from .runtime_evidence_gate import RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH
from .validation import (
    require_finite_number,
    require_hash,
    require_integer,
    require_positive_number,
    require_text,
)


S27_V2_DESIRED_POSITION_AUTHORIZATION = "S27_V2_NON_RESULT_DESIRED_POSITION_EXECUTABLE_LEDGER"
S27_V2_DESIRED_POSITION_STATUS = "S27_V2_DESIRED_POSITION_EXECUTABLE_REMEDIATION_PACK_NON_RESULT"
DESIRED_POSITION_LEDGER_ROW_STATUS = "LOCAL_DESIRED_POSITION_LEDGER_EMITTED_NOT_ORDER_NOT_RESULT_NOT_EVIDENCE"

CAPITAL_ACCOUNT_VALUE = 500000.0
CAPITAL_CURRENCY = "USD"
CAPITAL_POLICY_LABEL = "BOOK_EXAMPLE_ARBITRARY_CAPITAL_500000_USD_FIXED_BEFORE_DESIRED_POSITION_RESULTS"
ANNUAL_TARGET_RISK = 0.20
RISK_TARGET_POLICY_LABEL = "BOOK_USUAL_TARGET_RISK_20_PERCENT_FOR_US_10_YEAR_EXAMPLE_FIXED_BEFORE_DESIRED_POSITION_RESULTS"
INSTRUMENT_WEIGHT = 1.0
INSTRUMENT_DIVERSIFICATION_MULTIPLIER = 1.0
FX_RATE = 1.0
FX_RATE_PAIR = "USD/USD"
FORECAST_TO_POSITION_DIVISOR = 10.0
DIVISOR_POLICY_LABEL = (
    "BOOK_SCALED_FORECAST_DIVISOR_10_LOCALLY_BOUND_FROM_S26_POSITION_AND_LIMIT_PRICE_TEXT_"
    "AND_S27_INHERITANCE_PENDING_EXTERNAL_AUDIT"
)
CONTRACT_POINT_VALUE = 1000.0
CONTRACT_POINT_VALUE_CURRENCY = "USD"
CONTRACT_POINT_VALUE_SOURCE_LABEL = "APPENDIX_C_STATIC_ZN_POINT_VALUE_AUTHORITY"
PROVIDER_CONTRACT_MULTIPLIER_REJECTION_LABEL = (
    "DATABENTO_DEFINITION_CONTRACT_MULTIPLIER_2147483647_NOT_POINT_VALUE_AUTHORITY"
)
ROUNDING_POLICY_LABEL = "OPERATOR_FIXED_ROUND_HALF_AWAY_FROM_ZERO_BEFORE_DESIRED_POSITION_RESULTS"
INITIAL_POSITION_POLICY_LABEL = "INITIAL_FLAT_ZERO_FIRST_DEV_RECON_ROW_OPERATOR_FIXED_NOT_RESULT_TUNED"
INITIAL_CURRENT_POSITION_CONTRACTS = 0

DESIRED_POSITION_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_ORDER_FILL_COST_PNL_RESULT_EMISSION",
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

_REPO_ROOT = Path(__file__).resolve().parents[4]
_REMEDIATION_PACK_PATH = (_REPO_ROOT / RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH).resolve()
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
_REMEDIATION_MANIFEST_FILENAME = "S27_V2_RUNTIME_EVIDENCE_REMEDIATION_DECLARED_INPUT_PACK_MANIFEST.json"
_EXPECTED_REMEDIATION_MANIFEST_SHA256 = "0b8ae370b8b6ee3a31976448cabc30fe6ae658eeef5123171bb67bf67805febc"
_EXPECTED_COST_PARAMETER_SHA256 = "e6b7c69a712fd7a5effbabbd4c809f24c1a6dfabbfb1ce317b387c923ac7f098"
_EXPECTED_STATIC_SPEC_SHA256 = "908d9c147babf839ff4475f4286bf9e7828921f274f2d1a4a7a4cb5c2b7ead1d"
_EXPECTED_PROVIDER_DEFINITION_SHA256 = "cb1908e05cd41037a681a1a9aede56eb93001ad7c4576b048b15c87b0ec00742"
_EXPECTED_ZNM6_INSTRUMENT_ID = "42000661"
_EXPECTED_ZNM6_EXCHANGE = "XCBT"
_EXPECTED_ZNM6_ACTIVATION = "2025-09-19 21:30:00+00:00"
_EXPECTED_ZNM6_EXPIRATION = "2026-06-18 17:01:00+00:00"


@dataclass(frozen=True)
class DesiredPositionExecutableLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    forecast_bundle_hash: str
    forecast_row_hash: str
    input_pack_path: str
    selected_decision_timestamp_utc: str
    selected_previous_daily_timestamp_utc: str
    raw_symbol: str
    capital_account_value: float
    capital_currency: str
    capital_policy_label: str
    capital_policy_hash: str
    annual_target_risk: float
    risk_target_policy_label: str
    risk_target_policy_hash: str
    instrument_weight: float
    instrument_diversification_multiplier: float
    fx_rate: float
    fx_rate_pair: str
    single_instrument_policy_hash: str
    contract_point_value: float
    contract_point_value_currency: str
    contract_point_value_source_label: str
    static_spec_source_file_hash: str
    static_spec_zn_row_hash: str
    provider_definition_source_file_hash: str
    provider_definition_znm6_row_hash: str
    provider_instrument_id: str
    provider_activation: str
    provider_expiration: str
    provider_contract_multiplier_field_value: str
    provider_contract_multiplier_rejection_label: str
    provider_contract_multiplier_rejection_hash: str
    current_price_value: float
    current_price_hash: str
    annual_percentage_risk_value: float
    annual_percentage_risk_hash: str
    base_unrounded_contracts: float
    base_unrounded_contracts_hash: str
    capped_forecast_value: float
    capped_forecast_hash: str
    forecast_to_position_divisor: float
    divisor_policy_label: str
    divisor_policy_hash: str
    desired_unrounded_contracts: float
    desired_unrounded_contracts_hash: str
    rounding_policy_label: str
    rounding_policy_hash: str
    desired_rounded_contracts: int
    desired_rounded_contracts_hash: str
    initial_current_position_contracts: int
    initial_position_policy_label: str
    initial_position_policy_hash: str
    row_hash: str

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 desired-position row standalone validation is not authoritative; validate the bundle"
        )

    def _validate_structural_formula(self) -> None:
        if self.ledger_label != "DESIRED_POSITION_LEDGER":
            raise CarverBlocked("S27 v2 desired-position ledger label is not locked")
        if self.row_status != DESIRED_POSITION_LEDGER_ROW_STATUS:
            raise CarverBlocked("S27 v2 desired-position row status is not locked")
        if self.reason_code != "S27_DESIRED_POSITION_BOUND_TO_ACTIVE_FORECAST_AND_PRE_RESULT_POLICIES_NOT_ORDER":
            raise CarverBlocked("S27 v2 desired-position reason is not locked")
        for name, hash_value in (
            ("forecast bundle hash", self.forecast_bundle_hash),
            ("forecast row hash", self.forecast_row_hash),
            ("capital policy hash", self.capital_policy_hash),
            ("risk target policy hash", self.risk_target_policy_hash),
            ("single-instrument policy hash", self.single_instrument_policy_hash),
            ("static spec file hash", self.static_spec_source_file_hash),
            ("static spec ZN row hash", self.static_spec_zn_row_hash),
            ("provider definition file hash", self.provider_definition_source_file_hash),
            ("provider definition ZNM6 row hash", self.provider_definition_znm6_row_hash),
            ("provider multiplier rejection hash", self.provider_contract_multiplier_rejection_hash),
            ("current price hash", self.current_price_hash),
            ("annual percentage risk hash", self.annual_percentage_risk_hash),
            ("base unrounded contracts hash", self.base_unrounded_contracts_hash),
            ("capped forecast hash", self.capped_forecast_hash),
            ("divisor policy hash", self.divisor_policy_hash),
            ("desired unrounded contracts hash", self.desired_unrounded_contracts_hash),
            ("rounding policy hash", self.rounding_policy_hash),
            ("desired rounded contracts hash", self.desired_rounded_contracts_hash),
            ("initial position policy hash", self.initial_position_policy_hash),
        ):
            require_hash(f"S27 v2 desired-position {name}", hash_value)
        for name, value in (
            ("input pack path", self.input_pack_path),
            ("selected decision timestamp", self.selected_decision_timestamp_utc),
            ("selected previous daily timestamp", self.selected_previous_daily_timestamp_utc),
            ("raw symbol", self.raw_symbol),
            ("capital currency", self.capital_currency),
            ("capital policy label", self.capital_policy_label),
            ("risk target policy label", self.risk_target_policy_label),
            ("FX rate pair", self.fx_rate_pair),
            ("contract point value currency", self.contract_point_value_currency),
            ("contract point value source label", self.contract_point_value_source_label),
            ("provider instrument id", self.provider_instrument_id),
            ("provider activation", self.provider_activation),
            ("provider expiration", self.provider_expiration),
            ("provider contract multiplier field", self.provider_contract_multiplier_field_value),
            ("provider multiplier rejection label", self.provider_contract_multiplier_rejection_label),
            ("divisor policy label", self.divisor_policy_label),
            ("rounding policy label", self.rounding_policy_label),
            ("initial position policy label", self.initial_position_policy_label),
        ):
            require_text(f"S27 v2 desired-position {name}", value)
        self._validate_policy_constants()
        self._validate_value_hash("current price", self.current_price_value, self.current_price_hash)
        self._validate_positive_value_hash("annual percentage risk", self.annual_percentage_risk_value, self.annual_percentage_risk_hash)
        self._validate_value_hash("capped forecast", self.capped_forecast_value, self.capped_forecast_hash)
        self._validate_value_hash("base unrounded contracts", self.base_unrounded_contracts, self.base_unrounded_contracts_hash)
        expected_base = (
            self.capital_account_value
            * self.annual_target_risk
            * self.instrument_weight
            * self.instrument_diversification_multiplier
            / (
                self.current_price_value
                * self.contract_point_value
                * self.fx_rate
                * self.annual_percentage_risk_value
            )
        )
        _require_close("S27 v2 base unrounded contracts", self.base_unrounded_contracts, expected_base)
        self._validate_value_hash("desired unrounded contracts", self.desired_unrounded_contracts, self.desired_unrounded_contracts_hash)
        expected_desired_unrounded = self.base_unrounded_contracts * self.capped_forecast_value / self.forecast_to_position_divisor
        _require_close("S27 v2 desired unrounded contracts", self.desired_unrounded_contracts, expected_desired_unrounded)
        require_integer("S27 v2 desired rounded contracts", self.desired_rounded_contracts)
        if self.desired_rounded_contracts != _round_half_away_from_zero(self.desired_unrounded_contracts):
            raise CarverBlocked("S27 v2 desired rounded contracts must bind half-away-from-zero policy")
        if self.desired_rounded_contracts_hash != _value_hash("desired rounded contracts", self.desired_rounded_contracts):
            raise CarverBlocked("S27 v2 desired rounded contracts hash must bind value")
        require_integer("S27 v2 initial/current position", self.initial_current_position_contracts)
        require_hash("S27 v2 desired-position row hash", self.row_hash)
        if self.row_hash != canonical_sha256(_desired_position_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 desired-position row hash must be content-bound")

    def _validate_policy_constants(self) -> None:
        if self.capital_account_value != CAPITAL_ACCOUNT_VALUE or self.capital_currency != CAPITAL_CURRENCY:
            raise CarverBlocked("S27 v2 desired-position capital policy is not locked")
        if self.capital_policy_label != CAPITAL_POLICY_LABEL:
            raise CarverBlocked("S27 v2 desired-position capital policy label is not locked")
        if self.capital_policy_hash != _policy_hash("capital", self.capital_policy_label, self.capital_account_value, self.capital_currency):
            raise CarverBlocked("S27 v2 desired-position capital policy hash must bind policy")
        if self.annual_target_risk != ANNUAL_TARGET_RISK or self.risk_target_policy_label != RISK_TARGET_POLICY_LABEL:
            raise CarverBlocked("S27 v2 desired-position risk target policy is not locked")
        if self.risk_target_policy_hash != _policy_hash("risk_target", self.risk_target_policy_label, self.annual_target_risk):
            raise CarverBlocked("S27 v2 desired-position risk target policy hash must bind policy")
        for name, value in (
            ("instrument weight", self.instrument_weight),
            ("instrument diversification multiplier", self.instrument_diversification_multiplier),
            ("FX rate", self.fx_rate),
            ("forecast-to-position divisor", self.forecast_to_position_divisor),
            ("contract point value", self.contract_point_value),
        ):
            require_positive_number(f"S27 v2 desired-position {name}", value)
        if self.instrument_weight != INSTRUMENT_WEIGHT:
            raise CarverBlocked("S27 v2 desired-position instrument weight is not locked")
        if self.instrument_diversification_multiplier != INSTRUMENT_DIVERSIFICATION_MULTIPLIER:
            raise CarverBlocked("S27 v2 desired-position IDM is not locked")
        if self.fx_rate != FX_RATE or self.fx_rate_pair != FX_RATE_PAIR:
            raise CarverBlocked("S27 v2 desired-position FX policy is not locked")
        if self.single_instrument_policy_hash != _policy_hash(
            "single_instrument_context",
            INSTRUMENT_WEIGHT,
            INSTRUMENT_DIVERSIFICATION_MULTIPLIER,
            FX_RATE,
            FX_RATE_PAIR,
        ):
            raise CarverBlocked("S27 v2 desired-position single-instrument policy hash must bind policy")
        if self.forecast_to_position_divisor != FORECAST_TO_POSITION_DIVISOR:
            raise CarverBlocked("S27 v2 desired-position forecast divisor is not locked")
        if self.divisor_policy_label != DIVISOR_POLICY_LABEL:
            raise CarverBlocked("S27 v2 desired-position divisor policy label is not locked")
        if self.divisor_policy_hash != _policy_hash("forecast_to_position_divisor", self.divisor_policy_label, self.forecast_to_position_divisor):
            raise CarverBlocked("S27 v2 desired-position divisor policy hash must bind policy")
        if self.contract_point_value != CONTRACT_POINT_VALUE or self.contract_point_value_currency != CONTRACT_POINT_VALUE_CURRENCY:
            raise CarverBlocked("S27 v2 desired-position ZN point value is not locked")
        if self.contract_point_value_source_label != CONTRACT_POINT_VALUE_SOURCE_LABEL:
            raise CarverBlocked("S27 v2 desired-position point-value source label is not locked")
        if self.provider_contract_multiplier_field_value != "2147483647":
            raise CarverBlocked("S27 v2 desired-position provider multiplier sentinel must be explicitly rejected")
        if self.contract_point_value == float(self.provider_contract_multiplier_field_value):
            raise CarverBlocked("S27 v2 desired-position cannot use provider contract_multiplier as point value")
        if self.provider_contract_multiplier_rejection_label != PROVIDER_CONTRACT_MULTIPLIER_REJECTION_LABEL:
            raise CarverBlocked("S27 v2 desired-position provider multiplier rejection label is not locked")
        if self.provider_contract_multiplier_rejection_hash != _policy_hash(
            "provider_contract_multiplier_rejection",
            self.provider_contract_multiplier_rejection_label,
            self.provider_contract_multiplier_field_value,
        ):
            raise CarverBlocked("S27 v2 desired-position provider multiplier rejection hash must bind policy")
        if self.rounding_policy_label != ROUNDING_POLICY_LABEL:
            raise CarverBlocked("S27 v2 desired-position rounding policy label is not locked")
        if self.rounding_policy_hash != _policy_hash("rounding_policy", self.rounding_policy_label):
            raise CarverBlocked("S27 v2 desired-position rounding policy hash must bind policy")
        if self.initial_current_position_contracts != INITIAL_CURRENT_POSITION_CONTRACTS:
            raise CarverBlocked("S27 v2 desired-position initial/current position is not locked")
        if self.initial_position_policy_label != INITIAL_POSITION_POLICY_LABEL:
            raise CarverBlocked("S27 v2 desired-position initial position policy label is not locked")
        if self.initial_position_policy_hash != _policy_hash(
            "initial_position_policy",
            self.initial_position_policy_label,
            self.initial_current_position_contracts,
        ):
            raise CarverBlocked("S27 v2 desired-position initial position policy hash must bind policy")

    def _validate_value_hash(self, name: str, value: float, hash_value: str) -> None:
        require_finite_number(f"S27 v2 desired-position {name}", value)
        require_hash(f"S27 v2 desired-position {name} hash", hash_value)
        if hash_value != _value_hash(name, value):
            raise CarverBlocked(f"S27 v2 desired-position {name} hash must bind value")

    def _validate_positive_value_hash(self, name: str, value: float, hash_value: str) -> None:
        require_positive_number(f"S27 v2 desired-position {name}", value)
        require_hash(f"S27 v2 desired-position {name} hash", hash_value)
        if hash_value != _value_hash(name, value):
            raise CarverBlocked(f"S27 v2 desired-position {name} hash must bind value")


@dataclass(frozen=True)
class DesiredPositionExecutableBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    forecast_bundle: ForecastExecutableBundle
    desired_position_row: DesiredPositionExecutableLedgerRow
    desired_position_rows_emitted: bool
    order_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = DESIRED_POSITION_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_DESIRED_POSITION_STATUS:
            raise CarverBlocked("S27 v2 desired-position executable status is not locked")
        if self.authorization_label != S27_V2_DESIRED_POSITION_AUTHORIZATION:
            raise CarverBlocked("S27 v2 desired-position executable authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 desired-position executable must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 desired-position executable must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 desired-position executable is locked to the audited remediation pack")
        self.forecast_bundle.validate()
        active_forecast = build_forecast_executable_ledgers_on_remediation_pack(pack_path)
        if self.forecast_bundle != active_forecast:
            raise CarverBlocked("S27 v2 desired-position executable must bind active forecast bundle")
        self.desired_position_row._validate_structural_formula()
        active_row = _build_active_desired_position_row(pack_path, active_forecast)
        if self.desired_position_row != active_row:
            raise CarverBlocked("S27 v2 desired-position row must match active forecast and position policies")
        if self.desired_position_rows_emitted is not True:
            raise CarverBlocked("S27 v2 desired-position executable must mark desired-position rows emitted")
        if any(
            flag is not False
            for flag in (
                self.order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 desired-position executable cannot emit order/fill/cost/PnL/result/evidence")
        if self.non_authorizations != DESIRED_POSITION_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 desired-position executable must preserve non-authorizations")
        require_hash("S27 v2 desired-position executable bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_desired_position_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 desired-position executable bundle hash must be content-bound")


def build_desired_position_executable_ledger(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> DesiredPositionExecutableBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 desired-position executable is locked to the audited remediation pack")
    forecast_bundle = build_forecast_executable_ledgers_on_remediation_pack(pack_path)
    desired_row = _build_active_desired_position_row(pack_path, forecast_bundle)
    bundle = DesiredPositionExecutableBundle(
        status=S27_V2_DESIRED_POSITION_STATUS,
        authorization_label=S27_V2_DESIRED_POSITION_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        forecast_bundle=forecast_bundle,
        desired_position_row=desired_row,
        desired_position_rows_emitted=True,
        order_rows_emitted=False,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = DesiredPositionExecutableBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_desired_position_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_desired_position_row(
    pack_path: Path,
    forecast_bundle: ForecastExecutableBundle,
) -> DesiredPositionExecutableLedgerRow:
    manifest = _read_manifest(pack_path)
    cost_path = pack_path / "cost_parameter.csv"
    _verify_locked_file_hash(cost_path, _EXPECTED_COST_PARAMETER_SHA256, "cost parameter")
    cost_row = _read_csv_rows(cost_path)[0]
    static_row = _locked_static_zn_row()
    provider_row = _locked_provider_znm6_row(manifest)
    forecast_row = forecast_bundle.forecast_row

    _validate_static_point_value(static_row)
    _validate_provider_identity(provider_row, manifest)
    _validate_cost_parameter_row(cost_row, manifest)

    current_price = forecast_row.hourly_current_price_value
    annual_percentage_risk = forecast_row.annual_percentage_sigma_value
    base_unrounded = (
        CAPITAL_ACCOUNT_VALUE
        * ANNUAL_TARGET_RISK
        * INSTRUMENT_WEIGHT
        * INSTRUMENT_DIVERSIFICATION_MULTIPLIER
        / (current_price * CONTRACT_POINT_VALUE * FX_RATE * annual_percentage_risk)
    )
    desired_unrounded = base_unrounded * forecast_row.capped_forecast_value / FORECAST_TO_POSITION_DIVISOR
    desired_rounded = _round_half_away_from_zero(desired_unrounded)

    row = DesiredPositionExecutableLedgerRow(
        ledger_label="DESIRED_POSITION_LEDGER",
        row_status=DESIRED_POSITION_LEDGER_ROW_STATUS,
        reason_code="S27_DESIRED_POSITION_BOUND_TO_ACTIVE_FORECAST_AND_PRE_RESULT_POLICIES_NOT_ORDER",
        forecast_bundle_hash=forecast_bundle.bundle_hash,
        forecast_row_hash=forecast_row.row_hash,
        input_pack_path=str(pack_path),
        selected_decision_timestamp_utc=manifest["selected_decision_timestamp_utc"],
        selected_previous_daily_timestamp_utc=manifest["selected_previous_daily_timestamp_utc"],
        raw_symbol=manifest["selected_raw_symbol"],
        capital_account_value=CAPITAL_ACCOUNT_VALUE,
        capital_currency=CAPITAL_CURRENCY,
        capital_policy_label=CAPITAL_POLICY_LABEL,
        capital_policy_hash=_policy_hash("capital", CAPITAL_POLICY_LABEL, CAPITAL_ACCOUNT_VALUE, CAPITAL_CURRENCY),
        annual_target_risk=ANNUAL_TARGET_RISK,
        risk_target_policy_label=RISK_TARGET_POLICY_LABEL,
        risk_target_policy_hash=_policy_hash("risk_target", RISK_TARGET_POLICY_LABEL, ANNUAL_TARGET_RISK),
        instrument_weight=INSTRUMENT_WEIGHT,
        instrument_diversification_multiplier=INSTRUMENT_DIVERSIFICATION_MULTIPLIER,
        fx_rate=FX_RATE,
        fx_rate_pair=FX_RATE_PAIR,
        single_instrument_policy_hash=_policy_hash(
            "single_instrument_context",
            INSTRUMENT_WEIGHT,
            INSTRUMENT_DIVERSIFICATION_MULTIPLIER,
            FX_RATE,
            FX_RATE_PAIR,
        ),
        contract_point_value=CONTRACT_POINT_VALUE,
        contract_point_value_currency=CONTRACT_POINT_VALUE_CURRENCY,
        contract_point_value_source_label=CONTRACT_POINT_VALUE_SOURCE_LABEL,
        static_spec_source_file_hash=_verify_locked_file_hash(
            _STATIC_SPEC_PATH,
            _EXPECTED_STATIC_SPEC_SHA256,
            "Appendix C static ZN spec",
        ),
        static_spec_zn_row_hash=_source_row_hash("appendix_c_static_zn_spec", static_row),
        provider_definition_source_file_hash=_verify_locked_file_hash(
            _PROVIDER_DEFINITION_PATH,
            _EXPECTED_PROVIDER_DEFINITION_SHA256,
            "provider definition",
        ),
        provider_definition_znm6_row_hash=_source_row_hash("databento_provider_definition_znm6", provider_row),
        provider_instrument_id=provider_row["instrument_id"],
        provider_activation=provider_row["activation"],
        provider_expiration=provider_row["expiration"],
        provider_contract_multiplier_field_value=provider_row["contract_multiplier"],
        provider_contract_multiplier_rejection_label=PROVIDER_CONTRACT_MULTIPLIER_REJECTION_LABEL,
        provider_contract_multiplier_rejection_hash=_policy_hash(
            "provider_contract_multiplier_rejection",
            PROVIDER_CONTRACT_MULTIPLIER_REJECTION_LABEL,
            provider_row["contract_multiplier"],
        ),
        current_price_value=current_price,
        current_price_hash=_value_hash("current price", current_price),
        annual_percentage_risk_value=annual_percentage_risk,
        annual_percentage_risk_hash=_value_hash("annual percentage risk", annual_percentage_risk),
        base_unrounded_contracts=base_unrounded,
        base_unrounded_contracts_hash=_value_hash("base unrounded contracts", base_unrounded),
        capped_forecast_value=forecast_row.capped_forecast_value,
        capped_forecast_hash=_value_hash("capped forecast", forecast_row.capped_forecast_value),
        forecast_to_position_divisor=FORECAST_TO_POSITION_DIVISOR,
        divisor_policy_label=DIVISOR_POLICY_LABEL,
        divisor_policy_hash=_policy_hash("forecast_to_position_divisor", DIVISOR_POLICY_LABEL, FORECAST_TO_POSITION_DIVISOR),
        desired_unrounded_contracts=desired_unrounded,
        desired_unrounded_contracts_hash=_value_hash("desired unrounded contracts", desired_unrounded),
        rounding_policy_label=ROUNDING_POLICY_LABEL,
        rounding_policy_hash=_policy_hash("rounding_policy", ROUNDING_POLICY_LABEL),
        desired_rounded_contracts=desired_rounded,
        desired_rounded_contracts_hash=_value_hash("desired rounded contracts", desired_rounded),
        initial_current_position_contracts=INITIAL_CURRENT_POSITION_CONTRACTS,
        initial_position_policy_label=INITIAL_POSITION_POLICY_LABEL,
        initial_position_policy_hash=_policy_hash(
            "initial_position_policy",
            INITIAL_POSITION_POLICY_LABEL,
            INITIAL_CURRENT_POSITION_CONTRACTS,
        ),
        row_hash="0" * 64,
    )
    row = DesiredPositionExecutableLedgerRow(
        **{**row.__dict__, "row_hash": canonical_sha256(_desired_position_row_hash_payload(row))}
    )
    row._validate_structural_formula()
    return row


def _read_manifest(pack_path: Path) -> dict[str, Any]:
    manifest_path = pack_path / _REMEDIATION_MANIFEST_FILENAME
    import json

    manifest_bytes = manifest_path.read_bytes()
    observed_hash = sha256(manifest_bytes).hexdigest()
    if observed_hash != _EXPECTED_REMEDIATION_MANIFEST_SHA256:
        raise CarverBlocked("S27 v2 desired-position audited remediation manifest hash mismatch")
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if not isinstance(manifest, dict):
        raise CarverBlocked("S27 v2 desired-position manifest must be a JSON object")
    return manifest


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise CarverBlocked(f"S27 v2 desired-position source file {path.name} has no rows")
    return rows


def _locked_static_zn_row() -> dict[str, str]:
    _verify_locked_file_hash(_STATIC_SPEC_PATH, _EXPECTED_STATIC_SPEC_SHA256, "Appendix C static ZN spec")
    rows = [row for row in _read_csv_rows(_STATIC_SPEC_PATH) if row.get("author_market_code") == "ZN"]
    if len(rows) != 1:
        raise CarverBlocked("S27 v2 desired-position static ZN spec must have exactly one row")
    return rows[0]


def _locked_provider_znm6_row(manifest: dict[str, Any]) -> dict[str, str]:
    _verify_locked_file_hash(_PROVIDER_DEFINITION_PATH, _EXPECTED_PROVIDER_DEFINITION_SHA256, "provider definition")
    selected_raw_symbol = manifest.get("selected_raw_symbol")
    selected_decision_key = _utc_second_key(str(manifest.get("selected_decision_timestamp_utc", "")))
    rows = [row for row in _read_csv_rows(_PROVIDER_DEFINITION_PATH) if row.get("raw_symbol") == selected_raw_symbol]
    active_rows = [
        row
        for row in rows
        if _utc_second_key(row.get("activation", "")) <= selected_decision_key <= _utc_second_key(row.get("expiration", ""))
    ]
    prior_active_rows = [
        row
        for row in active_rows
        if _utc_second_key(row.get("ts_recv", "")) <= selected_decision_key
    ]
    if not prior_active_rows:
        raise CarverBlocked("S27 v2 desired-position provider definition must bind prior active ZNM6 row")
    latest_key = max(_utc_second_key(row.get("ts_recv", "")) for row in prior_active_rows)
    latest_rows = [row for row in prior_active_rows if _utc_second_key(row.get("ts_recv", "")) == latest_key]
    if len(latest_rows) != 1:
        raise CarverBlocked("S27 v2 desired-position provider definition latest prior ZNM6 row must be unique")
    if latest_rows[0].get("instrument_id") != _EXPECTED_ZNM6_INSTRUMENT_ID:
        raise CarverBlocked("S27 v2 desired-position provider definition must bind ZNM6 instrument_id 42000661")
    return latest_rows[0]


def _validate_static_point_value(row: dict[str, str]) -> None:
    if row.get("official_product_code") != "ZN":
        raise CarverBlocked("S27 v2 desired-position static spec must bind ZN")
    if row.get("official_currency") != CONTRACT_POINT_VALUE_CURRENCY:
        raise CarverBlocked("S27 v2 desired-position static spec must bind USD")
    if float(row.get("official_point_value", "nan")) != CONTRACT_POINT_VALUE:
        raise CarverBlocked("S27 v2 desired-position static spec must bind 1000 USD point value")
    if float(row.get("official_tick_size", "nan")) != 0.015625:
        raise CarverBlocked("S27 v2 desired-position static spec must bind ZN tick size")
    if float(row.get("official_tick_value", "nan")) != 15.625:
        raise CarverBlocked("S27 v2 desired-position static spec must bind ZN tick value")


def _validate_provider_identity(row: dict[str, str], manifest: dict[str, Any]) -> None:
    if row.get("raw_symbol") != manifest.get("selected_raw_symbol"):
        raise CarverBlocked("S27 v2 desired-position provider definition must bind selected raw symbol")
    if row.get("instrument_id") != _EXPECTED_ZNM6_INSTRUMENT_ID:
        raise CarverBlocked("S27 v2 desired-position provider definition must bind ZNM6 instrument_id")
    if row.get("exchange") != _EXPECTED_ZNM6_EXCHANGE:
        raise CarverBlocked("S27 v2 desired-position provider definition must bind XCBT exchange")
    if row.get("activation") != _EXPECTED_ZNM6_ACTIVATION:
        raise CarverBlocked("S27 v2 desired-position provider definition must bind exact ZNM6 activation")
    if row.get("expiration") != _EXPECTED_ZNM6_EXPIRATION:
        raise CarverBlocked("S27 v2 desired-position provider definition must bind exact ZNM6 expiration")
    if row.get("currency") != CONTRACT_POINT_VALUE_CURRENCY:
        raise CarverBlocked("S27 v2 desired-position provider definition must bind USD currency")
    if row.get("group") != "ZN" or row.get("asset") != "ZN" or row.get("security_type") != "FUT":
        raise CarverBlocked("S27 v2 desired-position provider definition must bind ZN futures identity")
    if row.get("contract_multiplier") != "2147483647":
        raise CarverBlocked("S27 v2 desired-position provider multiplier sentinel must remain explicit")


def _validate_cost_parameter_row(row: dict[str, str], manifest: dict[str, Any]) -> None:
    if row.get("raw_symbol") != manifest.get("selected_raw_symbol"):
        raise CarverBlocked("S27 v2 desired-position cost parameter row must bind selected raw symbol")
    if row.get("effective_trading_date") != str(manifest.get("selected_decision_timestamp_utc", ""))[:10]:
        raise CarverBlocked("S27 v2 desired-position cost parameter row must bind selected effective date")
    if row.get("readiness_status") != "READY_COST_PARAMETER_HASHES_LOCAL_ONLY_FAIL_CLOSED_FOR_EXECUTION":
        raise CarverBlocked("S27 v2 desired-position cost parameter row must remain fail-closed for execution")
    require_hash("S27 v2 desired-position cost multiplier policy hash", row.get("contract_multiplier_value_hash", ""))
    require_hash("S27 v2 desired-position cost currency policy hash", row.get("currency_policy_hash", ""))


def _verify_locked_file_hash(path: Path, expected_hash: str, label: str) -> str:
    observed_hash = sha256(path.read_bytes()).hexdigest()
    if observed_hash != expected_hash:
        raise CarverBlocked(f"S27 v2 desired-position {label} byte hash must match audited packet")
    return observed_hash


def _round_half_away_from_zero(value: float) -> int:
    require_finite_number("S27 v2 desired-position rounding input", value)
    if value > 0:
        return floor(value + 0.5)
    if value < 0:
        return -floor(abs(value) + 0.5)
    return 0


def _utc_second_key(value: str) -> str:
    require_text("S27 v2 desired-position provider timestamp", value)
    normalized = value.replace(" ", "T")
    if normalized.endswith("+00:00"):
        normalized = normalized[:-6] + "Z"
    if not normalized.endswith("Z"):
        raise CarverBlocked("S27 v2 desired-position provider timestamp must be UTC")
    return normalized[:19]


def _require_close(name: str, observed: float, expected: float) -> None:
    if not isclose(observed, expected, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked(f"{name} must bind source formula")


def _value_hash(label: str, value: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_DESIRED_POSITION_VALUE", "label": label, "value": value})


def _policy_hash(label: str, *values: object) -> str:
    return canonical_sha256({"artifact": "S27_V2_DESIRED_POSITION_POLICY", "label": label, "values": values})


def _source_row_hash(label: str, row: dict[str, str]) -> str:
    return canonical_sha256({"artifact": "S27_V2_DESIRED_POSITION_LOCKED_SOURCE_ROW", "label": label, "row": row})


def _desired_position_row_hash_payload(row: DesiredPositionExecutableLedgerRow) -> dict[str, object]:
    return {
        "annual_percentage_risk_hash": row.annual_percentage_risk_hash,
        "annual_percentage_risk_value": row.annual_percentage_risk_value,
        "annual_target_risk": row.annual_target_risk,
        "base_unrounded_contracts": row.base_unrounded_contracts,
        "base_unrounded_contracts_hash": row.base_unrounded_contracts_hash,
        "capital_account_value": row.capital_account_value,
        "capital_currency": row.capital_currency,
        "capital_policy_hash": row.capital_policy_hash,
        "capital_policy_label": row.capital_policy_label,
        "capped_forecast_hash": row.capped_forecast_hash,
        "capped_forecast_value": row.capped_forecast_value,
        "contract_point_value": row.contract_point_value,
        "contract_point_value_currency": row.contract_point_value_currency,
        "contract_point_value_source_label": row.contract_point_value_source_label,
        "current_price_hash": row.current_price_hash,
        "current_price_value": row.current_price_value,
        "desired_rounded_contracts": row.desired_rounded_contracts,
        "desired_rounded_contracts_hash": row.desired_rounded_contracts_hash,
        "desired_unrounded_contracts": row.desired_unrounded_contracts,
        "desired_unrounded_contracts_hash": row.desired_unrounded_contracts_hash,
        "divisor_policy_hash": row.divisor_policy_hash,
        "divisor_policy_label": row.divisor_policy_label,
        "forecast_bundle_hash": row.forecast_bundle_hash,
        "forecast_row_hash": row.forecast_row_hash,
        "forecast_to_position_divisor": row.forecast_to_position_divisor,
        "fx_rate": row.fx_rate,
        "fx_rate_pair": row.fx_rate_pair,
        "initial_current_position_contracts": row.initial_current_position_contracts,
        "initial_position_policy_hash": row.initial_position_policy_hash,
        "initial_position_policy_label": row.initial_position_policy_label,
        "input_pack_path": row.input_pack_path,
        "instrument_diversification_multiplier": row.instrument_diversification_multiplier,
        "instrument_weight": row.instrument_weight,
        "ledger_label": row.ledger_label,
        "provider_activation": row.provider_activation,
        "provider_contract_multiplier_field_value": row.provider_contract_multiplier_field_value,
        "provider_contract_multiplier_rejection_hash": row.provider_contract_multiplier_rejection_hash,
        "provider_contract_multiplier_rejection_label": row.provider_contract_multiplier_rejection_label,
        "provider_definition_source_file_hash": row.provider_definition_source_file_hash,
        "provider_definition_znm6_row_hash": row.provider_definition_znm6_row_hash,
        "provider_expiration": row.provider_expiration,
        "provider_instrument_id": row.provider_instrument_id,
        "raw_symbol": row.raw_symbol,
        "reason_code": row.reason_code,
        "risk_target_policy_hash": row.risk_target_policy_hash,
        "risk_target_policy_label": row.risk_target_policy_label,
        "rounding_policy_hash": row.rounding_policy_hash,
        "rounding_policy_label": row.rounding_policy_label,
        "row_status": row.row_status,
        "selected_decision_timestamp_utc": row.selected_decision_timestamp_utc,
        "selected_previous_daily_timestamp_utc": row.selected_previous_daily_timestamp_utc,
        "single_instrument_policy_hash": row.single_instrument_policy_hash,
        "static_spec_source_file_hash": row.static_spec_source_file_hash,
        "static_spec_zn_row_hash": row.static_spec_zn_row_hash,
    }


def _desired_position_bundle_hash_payload(bundle: DesiredPositionExecutableBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_DESIRED_POSITION_EXECUTABLE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "desired_position_row_hash": bundle.desired_position_row.row_hash,
        "desired_position_rows_emitted": bundle.desired_position_rows_emitted,
        "fill_rows_emitted": bundle.fill_rows_emitted,
        "forecast_bundle_hash": bundle.forecast_bundle.bundle_hash,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "order_rows_emitted": bundle.order_rows_emitted,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
    }

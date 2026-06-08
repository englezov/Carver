from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.canonical_hash import (
    S27_V2_CANONICAL_SERIALIZATION_POLICY_CONTRACT_ONLY_STATUS,
    CanonicalSerializationPolicy,
)
from carver.spine.s27_v2_replay.constants import (
    S27_V2_INSTRUMENT,
    S27_V2_LANE,
    S27_V2_STRATEGY_ID,
)
from carver.spine.s27_v2_replay.file_contract import (
    LocalFileDeclaration,
    ParserSourceDeclaration,
    RawSourceFileDeclaration,
    ReplayInputDirectoryDeclaration,
    RuntimeDependencyDeclaration,
)
from carver.spine.s27_v2_replay.local_replay import (
    LocalParserFileReplaySlice1Inputs,
    build_local_parser_file_replay_completion,
    build_local_parser_file_replay_slice2,
    build_local_parser_file_replay_slice3,
    build_local_parser_file_replay_slice4,
    build_local_parser_file_replay_slice5,
    build_local_parser_file_replay_slice6,
    build_local_parser_file_replay_slice7,
    build_local_parser_file_replay_slice1,
    build_source_input_manifest_contract,
    build_source_input_selection_contract,
    build_source_row_selection_authority_contract,
    build_source_row_selection_external_authority_handle,
    build_parser_output_contract,
    build_raw_file_hash_set_contract,
    build_source_row_batch_contract,
    canonical_sha256,
    parse_declared_source_file,
)
from carver.spine.s27_v2_replay.parser_plan import (
    CostParameterParserPlan,
    DailyParserPlan,
    HourlyParserPlan,
    ParserFamilyPlan,
    ParserPlanBundle,
    RollParserPlan,
    SessionParserPlan,
)
from carver.spine.s27_v2_replay.row_locator_contract import (
    PLANNED_ROW_LOCATOR_FAMILY_STATUS,
    REQUIRED_ROW_LOCATOR_FAMILIES,
    S27_V2_ROW_LOCATOR_CONTRACT_ONLY_STATUS,
    RowLocatorFieldBinding,
    SourceRowFamilyLocatorContract,
    SourceRowLocatorContractBundle,
)
from carver.spine.s27_v2_replay.source_universe_contract import (
    PLANNED_SOURCE_UNIVERSE_FAMILY_STATUS,
    REQUIRED_SOURCE_UNIVERSE_FAMILIES,
    S27_V2_SOURCE_UNIVERSE_CONTRACT_ONLY_STATUS,
    SourceUniverseContractBundle,
    SourceUniverseFamilyContract,
    SourceUniverseInclusionRule,
)


CANONICAL_POLICY_HASH = sha256(b"canonical-policy").hexdigest()
ROW_LOCATOR_POLICY_HASH = sha256(b"row-locator-policy").hexdigest()
COMPLETED_BAR_POLICY_HASH = sha256(b"completed-bar-policy").hexdigest()
STRICT_PRIOR_POLICY_HASH = sha256(b"strict-prior-policy").hexdigest()
INPUT_DIRECTORY_HASH = sha256(b"input-directory").hexdigest()


CSV_TEXT_BY_FAMILY = {
    "DAILY_CONTINUOUS_COMPLETED_BAR": (
        "completed_timestamp_utc,trading_date,raw_symbol,row_locator,close_price,"
        "annual_percentage_sigma,readiness_status\n"
        "2024-01-02T21:00:00Z,2024-01-02,ZNM24,dc-1,112.5,8.2,READY_COMPLETED_BAR\n"
    ),
    "DAILY_CURRENT_CONTRACT_COMPLETED_BAR": (
        "completed_timestamp_utc,trading_date,raw_symbol,row_locator,close_price,"
        "annual_percentage_sigma,readiness_status\n"
        "2024-01-02T21:00:00Z,2024-01-02,ZNM24,dcc-1,111.75,8.2,READY_COMPLETED_BAR\n"
    ),
    "HOURLY_DECISION_COMPLETED_BAR": (
        "completed_timestamp_utc,trading_date,raw_symbol,session_id,row_locator,"
        "close_price,readiness_status\n"
        "2024-01-02T14:00:00Z,2024-01-02,ZNM24,RTH,hd-1,111.875,READY_COMPLETED_BAR\n"
    ),
    "HOURLY_FILL_COMPLETED_BAR": (
        "completed_timestamp_utc,trading_date,raw_symbol,session_id,row_locator,"
        "close_price,readiness_status\n"
        "2024-01-02T15:00:00Z,2024-01-02,ZNM24,RTH,hf-1,111.90625,READY_COMPLETED_BAR\n"
    ),
    "SESSION_CALENDAR": (
        "trading_date,session_id,raw_symbol,session_open_utc,session_close_utc,"
        "row_locator,readiness_status\n"
        "2024-01-02,RTH,ZNM24,2024-01-02T13:00:00Z,2024-01-02T21:00:00Z,session-1,"
        "READY_SESSION_CALENDAR\n"
    ),
    "ROLL_CALENDAR": (
        "trading_date,expiring_raw_symbol,incoming_raw_symbol,roll_policy_hash,"
        "row_locator,readiness_status\n"
        f"2024-01-02,ZNH24,ZNM24,{sha256(b'roll-policy').hexdigest()},roll-1,"
        "READY_ROLL_CALENDAR\n"
    ),
    "COST_PARAMETER": (
        "effective_trading_date,raw_symbol,commission_policy_hash,spread_policy_hash,"
        "contract_multiplier_value_hash,currency_policy_hash,row_locator,readiness_status\n"
        f"2024-01-02,ZNM24,{sha256(b'commission').hexdigest()},"
        f"{sha256(b'spread').hexdigest()},{sha256(b'multiplier').hexdigest()},"
        f"{sha256(b'currency').hexdigest()},cost-1,READY_COST_PARAMETERS\n"
    ),
}


PARSER_OUTPUT_ROW_FAMILY_LABEL_BY_NAME = {
    "DAILY_COMPLETED_BAR_PARSER_PLAN": "DAILY_COMPLETED_BAR_OUTPUT_ROWS",
    "HOURLY_COMPLETED_BAR_PARSER_PLAN": "HOURLY_COMPLETED_BAR_OUTPUT_ROWS",
    "SESSION_CALENDAR_PARSER_PLAN": "SESSION_CALENDAR_OUTPUT_ROWS",
    "ROLL_CALENDAR_PARSER_PLAN": "ROLL_CALENDAR_OUTPUT_ROWS",
    "COST_PARAMETER_PARSER_PLAN": "COST_PARAMETER_OUTPUT_ROWS",
}

PARSER_OUTPUT_ROW_FAMILIES_BY_NAME = {
    "DAILY_COMPLETED_BAR_PARSER_PLAN": (
        "DAILY_CONTINUOUS_COMPLETED_BAR",
        "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
    ),
    "HOURLY_COMPLETED_BAR_PARSER_PLAN": (
        "HOURLY_DECISION_COMPLETED_BAR",
        "HOURLY_FILL_COMPLETED_BAR",
    ),
    "SESSION_CALENDAR_PARSER_PLAN": ("SESSION_CALENDAR",),
    "ROLL_CALENDAR_PARSER_PLAN": ("ROLL_CALENDAR",),
    "COST_PARAMETER_PARSER_PLAN": ("COST_PARAMETER",),
}


def test_declared_file_parser_builds_structural_rows_and_content_hashes(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)

    parsed = parse_declared_source_file(
        fixtures.input_directory,
        fixtures.input_directory.raw_source_files[0],
    )

    assert parsed.row_family == "DAILY_CONTINUOUS_COMPLETED_BAR"
    assert parsed.file_sha256 == fixtures.input_directory.raw_source_files[0].local_file.expected_sha256
    assert len(parsed.rows) == 1
    assert parsed.rows[0].row_locator == "dc-1"
    assert parsed.row_hashes == (parsed.rows[0].row_hash,)
    parsed.validate()


def test_slice1_constructs_raw_parser_output_and_source_row_batch_contracts(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)

    artifacts = build_local_parser_file_replay_slice1(fixtures)

    assert tuple(parsed.row_family for parsed in artifacts.parsed_files) == REQUIRED_ROW_LOCATOR_FAMILIES
    assert tuple(
        binding.file_family for binding in artifacts.raw_file_hash_contract.raw_file_hash_bindings
    ) == REQUIRED_ROW_LOCATOR_FAMILIES
    assert tuple(
        contract.row_family
        for contract in artifacts.parser_output_contract.parsed_output_family_contracts
    ) == REQUIRED_ROW_LOCATOR_FAMILIES
    assert tuple(
        contract.row_family
        for contract in artifacts.source_row_batch_contract.source_row_batch_family_contracts
    ) == REQUIRED_ROW_LOCATOR_FAMILIES
    artifacts.validate()


def test_declared_sha_mismatch_fails_closed(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    target = tmp_path / fixtures.input_directory.raw_source_files[0].local_file.declared_path
    target.write_text(CSV_TEXT_BY_FAMILY["DAILY_CONTINUOUS_COMPLETED_BAR"] + "\n", encoding="utf-8")

    with pytest.raises(CarverBlocked, match="SHA256 mismatch"):
        parse_declared_source_file(
            fixtures.input_directory,
            fixtures.input_directory.raw_source_files[0],
        )


def test_trailing_csv_cells_fail_closed_even_when_declared_sha_matches(tmp_path):
    fixtures = _build_slice1_fixtures(
        tmp_path,
        overrides={
            "DAILY_CONTINUOUS_COMPLETED_BAR": (
                CSV_TEXT_BY_FAMILY["DAILY_CONTINUOUS_COMPLETED_BAR"].rstrip("\n")
                + ",unexpected-extra-cell\n"
            )
        },
    )

    with pytest.raises(CarverBlocked, match="row width"):
        parse_declared_source_file(
            fixtures.input_directory,
            fixtures.input_directory.raw_source_files[0],
        )


def test_stale_raw_file_hash_set_authority_fails_closed(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    stale_input_directory = ReplayInputDirectoryDeclaration(
        declared_path=fixtures.input_directory.declared_path,
        source_universe_manifest_hash=fixtures.input_directory.source_universe_manifest_hash,
        raw_file_hash_set_hash=_h("stale-raw-file-hash-set"),
        row_locator_hash=fixtures.input_directory.row_locator_hash,
        raw_source_files=fixtures.input_directory.raw_source_files,
        parser_sources=fixtures.input_directory.parser_sources,
        runtime_dependencies=fixtures.input_directory.runtime_dependencies,
        input_directory_declaration_hash=fixtures.input_directory.input_directory_declaration_hash,
    )
    stale_fixtures = LocalParserFileReplaySlice1Inputs(
        input_directory=stale_input_directory,
        parser_plan_bundle=fixtures.parser_plan_bundle,
        row_locator_contract=fixtures.row_locator_contract,
        source_universe_contract=fixtures.source_universe_contract,
        canonical_serialization_policy=fixtures.canonical_serialization_policy,
    )

    with pytest.raises(CarverBlocked, match="row locator to raw file hash set"):
        stale_fixtures.validate()


def test_parser_output_builder_rejects_stale_raw_file_hash_contract(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    stale_raw_contract = replace(
        artifacts.raw_file_hash_contract,
        raw_file_hash_set_hash=_h("stale-raw-file-hash-set"),
    )

    with pytest.raises(CarverBlocked, match="active raw file hash set"):
        build_parser_output_contract(
            fixtures,
            stale_raw_contract,
            artifacts.parsed_files,
        )


def test_parser_output_builder_rejects_internally_stale_raw_file_hash_contract(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    stale_binding = replace(
        artifacts.raw_file_hash_contract.raw_file_hash_bindings[0],
        file_hash_binding_hash=_h("internally-stale-file-binding"),
    )
    stale_raw_contract = replace(
        artifacts.raw_file_hash_contract,
        raw_file_hash_bindings=(
            stale_binding,
            *artifacts.raw_file_hash_contract.raw_file_hash_bindings[1:],
        ),
    )

    with pytest.raises(CarverBlocked, match="deterministic active construction"):
        build_parser_output_contract(
            fixtures,
            stale_raw_contract,
            artifacts.parsed_files,
        )


def test_source_row_batch_builder_rejects_stale_parser_output_contract(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    stale_parser_output_contract = replace(
        artifacts.parser_output_contract,
        raw_file_hash_set_hash=_h("stale-raw-file-hash-set"),
    )

    with pytest.raises(CarverBlocked, match="active raw file hash set"):
        build_source_row_batch_contract(
            fixtures,
            stale_parser_output_contract,
            artifacts.parsed_files,
        )


def test_source_row_batch_builder_rejects_internally_stale_parser_output_contract(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    stale_family_contract = replace(
        artifacts.parser_output_contract.parsed_output_family_contracts[0],
        parser_output_family_contract_hash=_h("internally-stale-parser-output-family"),
    )
    stale_parser_output_contract = replace(
        artifacts.parser_output_contract,
        parsed_output_family_contracts=(
            stale_family_contract,
            *artifacts.parser_output_contract.parsed_output_family_contracts[1:],
        ),
    )

    with pytest.raises(CarverBlocked, match="deterministic active construction"):
        build_source_row_batch_contract(
            fixtures,
            stale_parser_output_contract,
            artifacts.parsed_files,
        )


def test_slice2_constructs_source_selection_and_manifest_from_slice1_outputs(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)

    artifacts = build_local_parser_file_replay_slice2(fixtures)

    assert tuple(
        contract.input_role
        for contract in artifacts.source_input_selection_contract.role_selection_contracts
    ) == (
        "DAILY_CONTINUOUS_EQUILIBRIUM_ROW",
        "DAILY_CURRENT_CONTRACT_PRICE_ROW",
        "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_ROW",
        "HOURLY_DECISION_CURRENT_PRICE_ROW",
        "HOURLY_FILL_CURRENT_PRICE_ROW",
        "SESSION_CALENDAR_CONTEXT_ROW",
        "ROLL_CALENDAR_CONTEXT_ROW",
        "COST_PARAMETER_CONTEXT_ROW",
    )
    assert tuple(
        contract.manifest_field
        for contract in artifacts.source_input_manifest_contract.manifest_field_contracts
    ) == (
        "DAILY_CONTINUOUS_ROW_HASH",
        "DAILY_CURRENT_CONTRACT_ROW_HASH",
        "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_HASH",
        "HOURLY_DECISION_ROW_HASH",
        "HOURLY_FILL_ROW_HASH",
        "SESSION_CALENDAR_CONTEXT_HASH",
        "ROLL_CALENDAR_CONTEXT_HASH",
        "COST_PARAMETER_CONTEXT_HASH",
    )
    artifacts.validate()


def test_slice2_manifest_public_validate_remains_active_trust_fail_closed(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice2(fixtures)

    with pytest.raises(CarverBlocked, match="active trust authority"):
        artifacts.source_input_manifest_contract.validate()


def test_slice2_source_row_selection_rejects_stale_slice1_artifacts(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    stale_source_row_batch = replace(
        artifacts.source_row_batch_contract,
        source_row_batch_set_hash=_h("stale-source-row-batch-set"),
    )
    stale_artifacts = replace(
        artifacts,
        source_row_batch_contract=stale_source_row_batch,
    )

    with pytest.raises(CarverBlocked, match="slice1 artifacts"):
        build_source_row_selection_authority_contract(fixtures, stale_artifacts)


def test_slice2_selection_rejects_forged_external_authority_handle(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    slice1_artifacts = build_local_parser_file_replay_slice1(fixtures)
    authority = build_source_row_selection_authority_contract(fixtures, slice1_artifacts)
    external_authority = build_source_row_selection_external_authority_handle(
        fixtures,
        slice1_artifacts,
        authority,
    )
    forged_external_authority = replace(
        external_authority,
        source_row_selection_authority_hash=_h("forged-source-row-selection-authority"),
        authority_handle_hash=_h("forged-source-row-selection-authority-handle"),
    )

    with pytest.raises(CarverBlocked, match="authority hash"):
        build_source_input_selection_contract(
            fixtures,
            slice1_artifacts,
            forged_external_authority,
            authority,
        )


def test_slice2_manifest_rejects_forged_selection_contract_bundle(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    slice1_artifacts = build_local_parser_file_replay_slice1(fixtures)
    authority = build_source_row_selection_authority_contract(fixtures, slice1_artifacts)
    external_authority = build_source_row_selection_external_authority_handle(
        fixtures,
        slice1_artifacts,
        authority,
    )
    selection_contract = build_source_input_selection_contract(
        fixtures,
        slice1_artifacts,
        external_authority,
        authority,
    )
    forged_selection_contract = replace(
        selection_contract,
        source_input_selection_contract_hash=_h("forged-selection-contract"),
    )

    with pytest.raises(CarverBlocked, match="content-bound"):
        build_source_input_manifest_contract(
            fixtures,
            slice1_artifacts,
            external_authority,
            forged_selection_contract,
        )


def test_slice2_artifact_validate_rejects_direct_forged_selected_row_authority(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice2(fixtures)
    authority = artifacts.source_input_selection_contract.source_row_selection_authority
    forged_authority = replace(
        authority,
        selected_row_hash_by_input_role={
            **authority.selected_row_hash_by_input_role,
            "DAILY_CONTINUOUS_EQUILIBRIUM_ROW": _h("forged-selected-row"),
        },
    )
    forged_selection_contract = replace(
        artifacts.source_input_selection_contract,
        source_row_selection_authority=forged_authority,
    )
    forged_artifacts = replace(
        artifacts,
        source_input_selection_contract=forged_selection_contract,
    )

    with pytest.raises(CarverBlocked, match="content-bound|active parsed row"):
        forged_artifacts.validate()


def test_slice2_role_contract_hash_binds_policy_and_proof_fields(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice2(fixtures)
    role_contract = artifacts.source_input_selection_contract.role_selection_contracts[0]
    forged_role_contract = replace(
        role_contract,
        completed_bar_policy_hash=_h("forged-completed-bar-policy"),
    )
    forged_selection_contract = replace(
        artifacts.source_input_selection_contract,
        role_selection_contracts=(
            forged_role_contract,
            *artifacts.source_input_selection_contract.role_selection_contracts[1:],
        ),
    )
    forged_artifacts = replace(
        artifacts,
        source_input_selection_contract=forged_selection_contract,
    )

    with pytest.raises(CarverBlocked, match="role contract hash"):
        forged_artifacts.validate()


def test_slice2_manifest_field_hash_binds_policy_and_proof_fields(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice2(fixtures)
    manifest_field = artifacts.source_input_manifest_contract.manifest_field_contracts[0]
    forged_manifest_field = replace(
        manifest_field,
        strict_prior_policy_hash=_h("forged-strict-prior-policy"),
    )
    forged_manifest_contract = replace(
        artifacts.source_input_manifest_contract,
        manifest_field_contracts=(
            forged_manifest_field,
            *artifacts.source_input_manifest_contract.manifest_field_contracts[1:],
        ),
    )
    forged_artifacts = replace(
        artifacts,
        source_input_manifest_contract=forged_manifest_contract,
    )

    with pytest.raises(CarverBlocked, match="field contract hash"):
        forged_artifacts.validate()


def test_slice3_constructs_level_compatibility_and_runtime_history_scaffolds(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)

    artifacts = build_local_parser_file_replay_slice3(fixtures)

    assert tuple(
        field.input_label
        for field in artifacts.level_compatibility_input_contract.input_field_contracts
    ) == (
        "LEVEL_COMPAT_DAILY_CONTINUOUS_INPUT",
        "LEVEL_COMPAT_DAILY_CURRENT_CONTRACT_INPUT",
        "LEVEL_COMPAT_PREVIOUS_CURRENT_CLOSE_INPUT",
        "LEVEL_COMPAT_HOURLY_DECISION_INPUT",
        "LEVEL_COMPAT_HOURLY_FILL_INPUT",
    )
    assert tuple(
        field.input_label
        for field in artifacts.runtime_history_input_contract.input_field_contracts
    ) == (
        "RUNTIME_DAILY_CONTINUOUS_EQUILIBRIUM_INPUT",
        "RUNTIME_DAILY_CURRENT_CONTRACT_PRICE_INPUT",
        "RUNTIME_PREVIOUS_CURRENT_CONTRACT_CLOSE_INPUT",
        "RUNTIME_HOURLY_DECISION_PRICE_INPUT",
        "RUNTIME_SESSION_CALENDAR_CONTEXT_INPUT",
        "RUNTIME_ROLL_CALENDAR_CONTEXT_INPUT",
    )
    artifacts.validate()


def test_slice3_public_input_validators_remain_active_trust_fail_closed(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice3(fixtures)

    with pytest.raises(CarverBlocked, match="active trust authority"):
        artifacts.level_compatibility_input_contract.validate()
    with pytest.raises(CarverBlocked, match="active trust authority"):
        artifacts.runtime_history_input_contract.validate()


def test_slice3_rejects_forged_level_compatibility_manifest_field_binding(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice3(fixtures)
    first_field = artifacts.level_compatibility_input_contract.input_field_contracts[0]
    forged_field = replace(
        first_field,
        selected_row_hash=_h("forged-level-compat-selected-row"),
    )
    forged_level_input = replace(
        artifacts.level_compatibility_input_contract,
        input_field_contracts=(
            forged_field,
            *artifacts.level_compatibility_input_contract.input_field_contracts[1:],
        ),
    )
    forged_artifacts = replace(
        artifacts,
        level_compatibility_input_contract=forged_level_input,
    )

    with pytest.raises(CarverBlocked, match="content-bound|active selected row"):
        forged_artifacts.validate()


def test_slice3_rejects_forged_runtime_level_compatibility_binding(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice3(fixtures)
    first_binding = artifacts.runtime_history_input_contract.level_compatibility_input_bindings[0]
    forged_binding = replace(
        first_binding,
        level_compatibility_input_field_contract_hash=_h("forged-level-input-binding"),
    )
    forged_runtime_input = replace(
        artifacts.runtime_history_input_contract,
        level_compatibility_input_bindings=(
            forged_binding,
            *artifacts.runtime_history_input_contract.level_compatibility_input_bindings[1:],
        ),
    )
    forged_artifacts = replace(
        artifacts,
        runtime_history_input_contract=forged_runtime_input,
    )

    with pytest.raises(CarverBlocked, match="content-bound|active level input"):
        forged_artifacts.validate()


def test_slice3_rejects_forged_runtime_vqm_dependency_binding(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice3(fixtures)
    first_binding = artifacts.runtime_history_input_contract.vqm_dependency_binding_contracts[0]
    forged_binding = replace(
        first_binding,
        required_runtime_dependency_contract_hashes=(
            _h("forged-vqm-dependency"),
            *first_binding.required_runtime_dependency_contract_hashes[1:],
        ),
    )
    forged_runtime_input = replace(
        artifacts.runtime_history_input_contract,
        vqm_dependency_binding_contracts=(
            forged_binding,
            *artifacts.runtime_history_input_contract.vqm_dependency_binding_contracts[1:],
        ),
    )
    forged_artifacts = replace(
        artifacts,
        runtime_history_input_contract=forged_runtime_input,
    )

    with pytest.raises(CarverBlocked, match="content-bound|active dependencies"):
        forged_artifacts.validate()


def test_slice3_rejects_forged_runtime_expected_selected_row_maps(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice3(fixtures)
    forged_runtime_input = replace(
        artifacts.runtime_history_input_contract,
        expected_selected_row_hash_by_input_label={
            **artifacts.runtime_history_input_contract.expected_selected_row_hash_by_input_label,
            "RUNTIME_DAILY_CONTINUOUS_EQUILIBRIUM_INPUT": _h("forged-runtime-selected-row"),
        },
    )
    forged_artifacts = replace(
        artifacts,
        runtime_history_input_contract=forged_runtime_input,
    )

    with pytest.raises(CarverBlocked, match="selected-row map"):
        forged_artifacts.validate()


def test_slice3_rejects_forged_top_level_input_policy_hashes(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice3(fixtures)
    forged_level_input = replace(
        artifacts.level_compatibility_input_contract,
        level_compatibility_policy_hash=_h("forged-level-compat-policy"),
    )
    forged_level_artifacts = replace(
        artifacts,
        level_compatibility_input_contract=forged_level_input,
    )

    with pytest.raises(CarverBlocked, match="policy hash"):
        forged_level_artifacts.validate()

    forged_runtime_input = replace(
        artifacts.runtime_history_input_contract,
        runtime_history_input_policy_hash=_h("forged-runtime-input-policy"),
    )
    forged_runtime_artifacts = replace(
        artifacts,
        runtime_history_input_contract=forged_runtime_input,
    )

    with pytest.raises(CarverBlocked, match="policy hash"):
        forged_runtime_artifacts.validate()


def test_slice4_constructs_forecast_position_order_transition_scaffolds(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)

    artifacts = build_local_parser_file_replay_slice4(fixtures)

    assert tuple(
        field.input_label for field in artifacts.forecast_input_contract.input_field_contracts
    ) == (
        "FORECAST_HOURLY_DECISION_PRICE_INPUT",
        "FORECAST_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_INPUT",
        "FORECAST_EWMA5_EQUILIBRIUM_STATE_INPUT",
        "FORECAST_SIGMA_ESTIMATOR_STATE_INPUT",
        "FORECAST_EWMAC16_64_TREND_STATE_INPUT",
        "FORECAST_RELATIVE_VOLATILITY_V_INPUT",
        "FORECAST_EXPANDING_QUANTILE_Q_INPUT",
        "FORECAST_RAW_VOLATILITY_MULTIPLIER_INPUT",
        "FORECAST_EWMA10_MULTIPLIER_M_INPUT",
        "FORECAST_SCALAR_SOURCE_LOCK_INPUT",
        "FORECAST_CAP_POLICY_INPUT",
        "FORECAST_DESIRED_POSITION_REFERENCE_POLICY_INPUT",
    )
    assert tuple(
        field.input_label for field in artifacts.position_input_contract.input_field_contracts
    ) == (
        "POSITION_FORECAST_HASH_INPUT",
        "POSITION_CAPPED_FORECAST_INPUT",
        "POSITION_DESIRED_POSITION_REFERENCE_INPUT",
        "POSITION_FORECAST_TO_POSITION_DIVISOR_POLICY_INPUT",
        "POSITION_ROUNDING_POLICY_INPUT",
        "POSITION_CURRENT_POSITION_CONTEXT_INPUT",
        "POSITION_INITIAL_POSITION_POLICY_INPUT",
    )
    assert tuple(
        field.input_label for field in artifacts.order_input_contract.input_field_contracts
    ) == (
        "ORDER_DESIRED_POSITION_HASH_INPUT",
        "ORDER_DESIRED_ROUNDED_POSITION_INPUT",
        "ORDER_CURRENT_POSITION_CONTEXT_INPUT",
        "ORDER_LIMIT_KIND_POLICY_INPUT",
        "ORDER_MARKET_KIND_POLICY_INPUT",
        "ORDER_NORMAL_ONE_HOUR_LAG_TRANSITION_INPUT",
        "ORDER_EOD_OVERNIGHT_RECOMPUTE_TRANSITION_INPUT",
        "ORDER_ROLL_BOUNDARY_TRANSITION_INPUT",
        "ORDER_WORKING_ORDER_STATE_CONTEXT_INPUT",
        "ORDER_TICK_ROUNDING_POLICY_INPUT",
        "ORDER_ADJACENT_LIMIT_LADDER_POLICY_INPUT",
        "ORDER_MARKET_FALLBACK_POLICY_INPUT",
    )
    artifacts.validate()


def test_slice4_public_input_validators_remain_authority_fail_closed(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice4(fixtures)

    with pytest.raises(CarverBlocked, match="runtime-history authority"):
        artifacts.forecast_input_contract.validate()
    with pytest.raises(CarverBlocked, match="forecast authority"):
        artifacts.position_input_contract.validate()
    with pytest.raises(CarverBlocked, match="position authority"):
        artifacts.order_input_contract.validate()


def test_slice4_rejects_forged_forecast_runtime_authority_map(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice4(fixtures)
    forged_forecast_input = replace(
        artifacts.forecast_input_contract,
        expected_source_contract_hash_by_input_label={
            **artifacts.forecast_input_contract.expected_source_contract_hash_by_input_label,
            "FORECAST_HOURLY_DECISION_PRICE_INPUT": _h("forged-forecast-runtime-authority"),
        },
    )
    forged_artifacts = replace(artifacts, forecast_input_contract=forged_forecast_input)

    with pytest.raises(CarverBlocked, match="forecast expected source contract map"):
        forged_artifacts.validate()


def test_slice4_rejects_forged_position_forecast_dependency(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice4(fixtures)
    forged_binding = replace(
        artifacts.position_input_contract.component_dependency_bindings[1],
        required_dependency_contract_hashes=(
            _h("forged-position-forecast-component"),
            *artifacts.position_input_contract.component_dependency_bindings[
                1
            ].required_dependency_contract_hashes[1:],
        ),
    )
    forged_position_input = replace(
        artifacts.position_input_contract,
        component_dependency_bindings=(
            artifacts.position_input_contract.component_dependency_bindings[0],
            forged_binding,
            *artifacts.position_input_contract.component_dependency_bindings[2:],
        ),
    )
    forged_artifacts = replace(artifacts, position_input_contract=forged_position_input)

    with pytest.raises(CarverBlocked, match="position component dependency"):
        forged_artifacts.validate()


def test_slice4_rejects_forged_order_transition_policy_binding(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice4(fixtures)
    forged_transition_kind = replace(
        artifacts.order_contract.transition_kind_contracts[0],
        required_policy_hashes=(
            _h("forged-order-transition-policy"),
            *artifacts.order_contract.transition_kind_contracts[0].required_policy_hashes[1:],
        ),
    )
    forged_order_contract = replace(
        artifacts.order_contract,
        transition_kind_contracts=(
            forged_transition_kind,
            *artifacts.order_contract.transition_kind_contracts[1:],
        ),
    )
    forged_artifacts = replace(artifacts, order_contract=forged_order_contract)

    with pytest.raises(CarverBlocked, match="order transition kind must bind order input policy"):
        forged_artifacts.validate()


def test_slice4_rejects_forged_top_level_policy_hashes(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice4(fixtures)
    forged_forecast_input = replace(
        artifacts.forecast_input_contract,
        forecast_input_policy_hash=_h("forged-forecast-policy"),
    )
    forged_forecast_artifacts = replace(artifacts, forecast_input_contract=forged_forecast_input)

    with pytest.raises(CarverBlocked, match="forecast input policy hash"):
        forged_forecast_artifacts.validate()

    forged_order_input = replace(
        artifacts.order_input_contract,
        order_input_policy_hash=_h("forged-order-policy"),
    )
    forged_order_artifacts = replace(artifacts, order_input_contract=forged_order_input)

    with pytest.raises(CarverBlocked, match="order input policy hash"):
        forged_order_artifacts.validate()


def test_slice5_constructs_fill_input_and_fill_contract_scaffolds(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)

    artifacts = build_local_parser_file_replay_slice5(fixtures)

    assert tuple(
        field.input_label for field in artifacts.fill_input_contract.input_field_contracts
    ) == (
        "FILL_ORDER_PLAN_HASH_INPUT",
        "FILL_LIMIT_ORDER_HASH_INPUT",
        "FILL_MARKET_ORDER_HASH_INPUT",
        "FILL_WORKING_ORDER_TRANSITION_HASH_INPUT",
        "FILL_NEXT_COMPLETED_HOURLY_ROW_HASH_INPUT",
        "FILL_LIMIT_PRICE_PROVENANCE_INPUT",
        "FILL_MARKET_PRICE_PROVENANCE_INPUT",
        "FILL_LIMIT_BRANCH_INPUT",
        "FILL_MARKET_BRANCH_INPUT",
        "FILL_QUANTITY_AND_SIDE_BINDING_INPUT",
        "FILL_ONE_HOUR_LAG_POLICY_INPUT",
        "FILL_SESSION_GAP_POLICY_INPUT",
    )
    assert tuple(
        component.component_family for component in artifacts.fill_contract.component_contracts
    ) == (
        "ORDER_PLAN_REFERENCE",
        "WORKING_ORDER_TRANSITION_REFERENCE",
        "NEXT_COMPLETED_HOURLY_FILL_ROW",
        "LIMIT_FILL_PRICE_PROVENANCE",
        "MARKET_FILL_PRICE_PROVENANCE",
        "FILL_QUANTITY_AND_SIDE_BINDING",
    )
    artifacts.validate()


def test_slice5_public_fill_input_validator_remains_authority_fail_closed(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice5(fixtures)

    with pytest.raises(CarverBlocked, match="order and source-row authority"):
        artifacts.fill_input_contract.validate()


def test_slice5_rejects_forged_fill_expected_source_row_map(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice5(fixtures)
    forged_fill_input = replace(
        artifacts.fill_input_contract,
        expected_source_contract_hash_by_input_label={
            **artifacts.fill_input_contract.expected_source_contract_hash_by_input_label,
            "FILL_NEXT_COMPLETED_HOURLY_ROW_HASH_INPUT": _h("forged-fill-row-authority"),
        },
    )
    forged_artifacts = replace(artifacts, fill_input_contract=forged_fill_input)

    with pytest.raises(CarverBlocked, match="fill expected source contract map"):
        forged_artifacts.validate()


def test_slice5_rejects_forged_fill_order_dependency(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice5(fixtures)
    forged_binding = replace(
        artifacts.fill_input_contract.component_dependency_bindings[0],
        required_dependency_contract_hashes=(
            _h("forged-fill-order-plan"),
            *artifacts.fill_input_contract.component_dependency_bindings[
                0
            ].required_dependency_contract_hashes[1:],
        ),
    )
    forged_fill_input = replace(
        artifacts.fill_input_contract,
        component_dependency_bindings=(
            forged_binding,
            *artifacts.fill_input_contract.component_dependency_bindings[1:],
        ),
    )
    forged_artifacts = replace(artifacts, fill_input_contract=forged_fill_input)

    with pytest.raises(CarverBlocked, match="fill component dependency"):
        forged_artifacts.validate()


def test_slice5_rejects_forged_fill_policy_and_source_binding(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice5(fixtures)
    forged_fill_input = replace(
        artifacts.fill_input_contract,
        fill_input_policy_hash=_h("forged-fill-policy"),
    )
    forged_policy_artifacts = replace(artifacts, fill_input_contract=forged_fill_input)

    with pytest.raises(CarverBlocked, match="fill input policy hash"):
        forged_policy_artifacts.validate()

    forged_source_binding = replace(
        artifacts.fill_contract.source_binding,
        order_contract_bundle_hash=_h("forged-order-contract-for-fill"),
    )
    forged_fill_contract = replace(
        artifacts.fill_contract,
        source_binding=forged_source_binding,
    )
    forged_source_artifacts = replace(artifacts, fill_contract=forged_fill_contract)

    with pytest.raises(CarverBlocked, match="fill source binding must bind order contract"):
        forged_source_artifacts.validate()


def test_completion_loop_constructs_cost_pnl_validation_and_trusted_bundle(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)

    artifacts = build_local_parser_file_replay_completion(fixtures)

    assert tuple(
        field.input_label for field in artifacts.slice7_artifacts.slice6_artifacts.cost_input_contract.input_field_contracts
    ) == (
        "COST_FILL_LEDGER_HASH_INPUT",
        "COST_FILL_ORDER_KIND_INPUT",
        "COST_FILL_QUANTITY_INPUT",
        "COST_LIMIT_COMMISSION_ONLY_BRANCH_INPUT",
        "COST_MARKET_COMMISSION_PLUS_SPREAD_BRANCH_INPUT",
        "COST_COMMISSION_POLICY_INPUT",
        "COST_SPREAD_POLICY_INPUT",
        "COST_PRICE_SPACE_INPUT",
        "COST_CURRENCY_SPACE_INPUT",
        "COST_CONTRACT_MULTIPLIER_POLICY_INPUT",
        "COST_CURRENCY_CONVERSION_POLICY_INPUT",
        "COST_DEFLATION_POLICY_INPUT",
        "COST_CALCULATION_POLICY_INPUT",
    )
    assert tuple(
        component.component_family
        for component in artifacts.slice7_artifacts.pnl_contract.component_contracts
    ) == (
        "TRUST_ROOT_REFERENCE",
        "TRANSITION_STATE_REFERENCE",
        "POSITION_SOURCE_REFERENCE",
        "CLOSE_ONLY_PRICE_SOURCE_POLICY",
        "RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE",
        "CONTRACT_MULTIPLIER_CURRENCY_POLICY",
        "FILL_COST_APPLICATION",
        "PNL_SUMMARY",
    )
    assert artifacts.trusted_bundle_contract.status == "S27_V2_TRUSTED_BUNDLE_CONTRACT_ONLY"
    artifacts.validate()


def test_slice6_public_cost_input_validator_remains_authority_fail_closed(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice6(fixtures)

    with pytest.raises(CarverBlocked, match="requires fill authority"):
        artifacts.cost_input_contract.validate()


def test_slice6_rejects_forged_cost_policy_and_fill_authority(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice6(fixtures)
    forged_map = {
        **artifacts.cost_input_contract.expected_source_contract_hash_by_input_label,
        "COST_FILL_LEDGER_HASH_INPUT": _h("forged-fill-ledger-authority"),
    }
    forged_input = replace(
        artifacts.cost_input_contract,
        expected_source_contract_hash_by_input_label=forged_map,
    )
    forged_artifacts = replace(artifacts, cost_input_contract=forged_input)

    with pytest.raises(CarverBlocked, match="cost expected source contract hash map"):
        forged_artifacts.validate()

    forged_contract = replace(
        artifacts.cost_contract,
        commission_policy_hash=_h("forged-commission-policy"),
    )
    forged_policy_artifacts = replace(artifacts, cost_contract=forged_contract)

    with pytest.raises(CarverBlocked, match="cost contract"):
        forged_policy_artifacts.validate()


def test_slice7_public_pnl_input_validator_remains_authority_fail_closed(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice7(fixtures)

    with pytest.raises(CarverBlocked, match="requires cost and upstream replay authority"):
        artifacts.pnl_input_contract.validate()


def test_slice7_rejects_forged_pnl_cost_hash_set_and_policy(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice7(fixtures)
    forged_input = replace(
        artifacts.pnl_input_contract,
        cost_hash_set_hash=_h("forged-cost-hash-set"),
    )
    forged_artifacts = replace(artifacts, pnl_input_contract=forged_input)

    with pytest.raises(CarverBlocked, match="PnL routed authority"):
        forged_artifacts.validate()

    forged_contract = replace(
        artifacts.pnl_contract,
        pnl_formula_policy_hash=_h("forged-pnl-formula-policy"),
    )
    forged_policy_artifacts = replace(artifacts, pnl_contract=forged_contract)

    with pytest.raises(CarverBlocked, match="PnL formula policy"):
        forged_policy_artifacts.validate()


def test_completion_rejects_forged_validation_and_trusted_bundle_authority(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_completion(fixtures)
    forged_validation_input = replace(
        artifacts.validation_input_contract,
        pnl_contract_bundle_hash=_h("forged-pnl-contract-for-validation"),
    )
    forged_validation_artifacts = replace(
        artifacts,
        validation_input_contract=forged_validation_input,
    )

    with pytest.raises(CarverBlocked, match="validation routed authority"):
        forged_validation_artifacts.validate()

    forged_bundle = replace(
        artifacts.trusted_bundle_contract,
        construction_contract_hash=_h("forged-construction-contract"),
    )
    forged_bundle_artifacts = replace(
        artifacts,
        trusted_bundle_contract=forged_bundle,
    )

    with pytest.raises(CarverBlocked, match="trusted bundle routed authority"):
        forged_bundle_artifacts.validate()


def test_parser_output_builder_rejects_forged_parsed_rows_not_in_declared_file(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    forged_row = replace(
        artifacts.parsed_files[0].rows[0],
        row_locator="forged-row-locator",
        row_hash=_h("forged-daily-continuous-row"),
    )
    forged_parsed = replace(
        artifacts.parsed_files[0],
        rows=(forged_row,),
        row_hashes=(forged_row.row_hash,),
        parsed_output_batch_hash=canonical_sha256(
            {
                "artifact": "S27_V2_PARSED_DECLARED_SOURCE_FILE",
                "file_sha256": artifacts.parsed_files[0].file_sha256,
                "resolved_path": artifacts.parsed_files[0].resolved_path,
                "row_family": artifacts.parsed_files[0].row_family,
                "row_hashes": (forged_row.row_hash,),
            }
        ),
    )

    with pytest.raises(CarverBlocked, match="declared local file bytes"):
        build_parser_output_contract(
            fixtures,
            artifacts.raw_file_hash_contract,
            (forged_parsed, *artifacts.parsed_files[1:]),
        )


def test_raw_file_hash_builder_rejects_forged_parsed_rows_not_in_declared_file(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    forged_row = replace(
        artifacts.parsed_files[0].rows[0],
        row_locator="forged-row-locator",
        row_hash=_h("forged-daily-continuous-row"),
    )
    forged_parsed = replace(
        artifacts.parsed_files[0],
        rows=(forged_row,),
        row_hashes=(forged_row.row_hash,),
        parsed_output_batch_hash=canonical_sha256(
            {
                "artifact": "S27_V2_PARSED_DECLARED_SOURCE_FILE",
                "file_sha256": artifacts.parsed_files[0].file_sha256,
                "resolved_path": artifacts.parsed_files[0].resolved_path,
                "row_family": artifacts.parsed_files[0].row_family,
                "row_hashes": (forged_row.row_hash,),
            }
        ),
    )

    with pytest.raises(CarverBlocked, match="declared local file bytes"):
        build_raw_file_hash_set_contract(
            fixtures.input_directory,
            fixtures.parser_plan_bundle,
            (forged_parsed, *artifacts.parsed_files[1:]),
        )


def test_source_row_batch_builder_rejects_forged_parsed_rows_not_in_declared_file(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    forged_row = replace(
        artifacts.parsed_files[0].rows[0],
        row_locator="forged-row-locator",
        row_hash=_h("forged-daily-continuous-row"),
    )
    forged_parsed = replace(
        artifacts.parsed_files[0],
        rows=(forged_row,),
        row_hashes=(forged_row.row_hash,),
        parsed_output_batch_hash=canonical_sha256(
            {
                "artifact": "S27_V2_PARSED_DECLARED_SOURCE_FILE",
                "file_sha256": artifacts.parsed_files[0].file_sha256,
                "resolved_path": artifacts.parsed_files[0].resolved_path,
                "row_family": artifacts.parsed_files[0].row_family,
                "row_hashes": (forged_row.row_hash,),
            }
        ),
    )

    with pytest.raises(CarverBlocked, match="declared local file bytes"):
        build_source_row_batch_contract(
            fixtures,
            artifacts.parser_output_contract,
            (forged_parsed, *artifacts.parsed_files[1:]),
        )


def test_inputs_reject_internally_stale_row_locator_family_contract(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    stale_row_locator_family = replace(
        fixtures.row_locator_contract.row_family_contracts[0],
        family_contract_hash=_h("internally-stale-row-locator-family"),
    )
    stale_row_locator_contract = replace(
        fixtures.row_locator_contract,
        row_family_contracts=(
            stale_row_locator_family,
            *fixtures.row_locator_contract.row_family_contracts[1:],
        ),
    )
    stale_fixtures = LocalParserFileReplaySlice1Inputs(
        input_directory=fixtures.input_directory,
        parser_plan_bundle=fixtures.parser_plan_bundle,
        row_locator_contract=stale_row_locator_contract,
        source_universe_contract=fixtures.source_universe_contract,
        canonical_serialization_policy=fixtures.canonical_serialization_policy,
    )

    with pytest.raises(CarverBlocked, match="row locator family hash"):
        stale_fixtures.validate()


def test_inputs_reject_internally_stale_source_universe_family_contract(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    stale_source_universe_family = replace(
        fixtures.source_universe_contract.family_contracts[0],
        family_contract_hash=_h("internally-stale-source-universe-family"),
    )
    stale_source_universe_contract = replace(
        fixtures.source_universe_contract,
        family_contracts=(
            stale_source_universe_family,
            *fixtures.source_universe_contract.family_contracts[1:],
        ),
    )
    stale_fixtures = LocalParserFileReplaySlice1Inputs(
        input_directory=fixtures.input_directory,
        parser_plan_bundle=fixtures.parser_plan_bundle,
        row_locator_contract=fixtures.row_locator_contract,
        source_universe_contract=stale_source_universe_contract,
        canonical_serialization_policy=fixtures.canonical_serialization_policy,
    )

    with pytest.raises(CarverBlocked, match="source universe family hash"):
        stale_fixtures.validate()


def test_inputs_reject_internally_stale_parser_family_plan(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    stale_daily_family_plan = replace(
        fixtures.parser_plan_bundle.daily_parser_plan.family_plan,
        parser_extractor_source_hash=_h("stale-daily-parser-extractor-source"),
    )
    stale_parser_plan_bundle = replace(
        fixtures.parser_plan_bundle,
        daily_parser_plan=DailyParserPlan(stale_daily_family_plan),
    )
    stale_fixtures = LocalParserFileReplaySlice1Inputs(
        input_directory=fixtures.input_directory,
        parser_plan_bundle=stale_parser_plan_bundle,
        row_locator_contract=fixtures.row_locator_contract,
        source_universe_contract=fixtures.source_universe_contract,
        canonical_serialization_policy=fixtures.canonical_serialization_policy,
    )

    with pytest.raises(CarverBlocked, match="parser family plan hash"):
        stale_fixtures.validate()


def test_raw_file_hash_builder_rejects_internally_stale_parser_family_plan(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    artifacts = build_local_parser_file_replay_slice1(fixtures)
    stale_daily_family_plan = replace(
        fixtures.parser_plan_bundle.daily_parser_plan.family_plan,
        parser_extractor_source_hash=_h("stale-daily-parser-extractor-source"),
    )
    stale_parser_plan_bundle = replace(
        fixtures.parser_plan_bundle,
        daily_parser_plan=DailyParserPlan(stale_daily_family_plan),
    )

    with pytest.raises(CarverBlocked, match="parser family plan hash"):
        build_raw_file_hash_set_contract(
            fixtures.input_directory,
            stale_parser_plan_bundle,
            artifacts.parsed_files,
        )


def test_inputs_reject_wrong_source_universe_locator_family_mapping(tmp_path):
    fixtures = _build_slice1_fixtures(tmp_path)
    daily_universe_index = 2
    stale_daily_universe = replace(
        fixtures.source_universe_contract.family_contracts[daily_universe_index],
        source_row_locator_family="ROLL_CALENDAR",
    )
    stale_daily_universe = replace(
        stale_daily_universe,
        family_contract_hash=_source_universe_family_contract_hash(stale_daily_universe),
    )
    stale_family_contracts = (
        fixtures.source_universe_contract.family_contracts[:daily_universe_index]
        + (stale_daily_universe,)
        + fixtures.source_universe_contract.family_contracts[daily_universe_index + 1 :]
    )
    stale_source_universe_contract = replace(
        fixtures.source_universe_contract,
        family_contracts=stale_family_contracts,
    )
    stale_source_universe_contract = replace(
        stale_source_universe_contract,
        source_universe_contract_bundle_hash=_expected_source_universe_contract_bundle_hash(
            raw_file_hash_set_hash=stale_source_universe_contract.raw_file_hash_set_hash,
            row_locator_contract_bundle_hash=stale_source_universe_contract.row_locator_contract_bundle_hash,
            inclusion_rules=stale_source_universe_contract.inclusion_rules,
            family_contracts=stale_source_universe_contract.family_contracts,
        ),
    )
    stale_input_directory = replace(
        fixtures.input_directory,
        source_universe_manifest_hash=stale_source_universe_contract.source_universe_contract_bundle_hash,
    )
    stale_row_locator_contract = replace(
        fixtures.row_locator_contract,
        source_universe_manifest_hash=stale_source_universe_contract.source_universe_contract_bundle_hash,
    )
    stale_fixtures = LocalParserFileReplaySlice1Inputs(
        input_directory=stale_input_directory,
        parser_plan_bundle=fixtures.parser_plan_bundle,
        row_locator_contract=stale_row_locator_contract,
        source_universe_contract=stale_source_universe_contract,
        canonical_serialization_policy=fixtures.canonical_serialization_policy,
    )

    with pytest.raises(CarverBlocked, match="row-locator family"):
        stale_fixtures.validate()


def _build_slice1_fixtures(
    tmp_path,
    overrides: dict[str, str] | None = None,
) -> LocalParserFileReplaySlice1Inputs:
    raw_source_files = tuple(
        _write_raw_source_declaration(tmp_path, row_family, overrides or {})
        for row_family in REQUIRED_ROW_LOCATOR_FAMILIES
    )
    parser_plan_bundle = _parser_plan_bundle()
    raw_file_hash_set_hash = _expected_raw_file_hash_set_hash(
        raw_source_files,
        parser_plan_bundle,
    )
    row_locator_contract = _row_locator_contract(
        raw_source_files,
        parser_plan_bundle,
        raw_file_hash_set_hash,
    )
    source_universe_contract = _source_universe_contract(
        raw_file_hash_set_hash,
        row_locator_contract.row_locator_contract_bundle_hash,
    )
    row_locator_contract = replace(
        row_locator_contract,
        source_universe_manifest_hash=source_universe_contract.source_universe_contract_bundle_hash,
    )
    input_directory = ReplayInputDirectoryDeclaration(
        declared_path=str(tmp_path),
        source_universe_manifest_hash=source_universe_contract.source_universe_contract_bundle_hash,
        raw_file_hash_set_hash=raw_file_hash_set_hash,
        row_locator_hash=row_locator_contract.row_locator_contract_bundle_hash,
        raw_source_files=raw_source_files,
        parser_sources=_parser_sources(),
        runtime_dependencies=(
            RuntimeDependencyDeclaration(
                dependency_name="python",
                dependency_version_label="test-runtime",
                dependency_manifest_hash=_h("python-runtime-manifest"),
                runtime_environment_hash=_h("runtime-environment"),
            ),
        ),
        input_directory_declaration_hash=INPUT_DIRECTORY_HASH,
    )
    canonical_policy = _canonical_policy()
    fixtures = LocalParserFileReplaySlice1Inputs(
        input_directory=input_directory,
        parser_plan_bundle=parser_plan_bundle,
        row_locator_contract=row_locator_contract,
        source_universe_contract=source_universe_contract,
        canonical_serialization_policy=canonical_policy,
    )
    fixtures.validate()
    return fixtures


def _write_raw_source_declaration(
    tmp_path,
    row_family: str,
    overrides: dict[str, str],
) -> RawSourceFileDeclaration:
    filename = f"{row_family.lower()}.csv"
    csv_text = overrides.get(row_family, CSV_TEXT_BY_FAMILY[row_family])
    (tmp_path / filename).write_bytes(csv_text.encode("utf-8"))
    return RawSourceFileDeclaration(
        local_file=LocalFileDeclaration(
            declared_path=filename,
            expected_artifact_type="LOCAL_CSV",
            expected_sha256=sha256(csv_text.encode("utf-8")).hexdigest(),
            expected_row_family=row_family,
            expected_timezone_policy_hash=_h(f"{row_family}-timezone"),
            canonical_serialization_policy_hash=CANONICAL_POLICY_HASH,
            operator_authorization_label="S27_V2_LOCAL_ONLY_PARSER_FILE_REPLAY_IMPLEMENTATION_SLICE_1",
            no_provider_no_download_assertion_label="NO_PROVIDER_API_NO_DOWNLOAD",
        ),
        raw_symbol_family="ZN",
        completed_bar_policy_hash=COMPLETED_BAR_POLICY_HASH,
        row_locator_policy_hash=ROW_LOCATOR_POLICY_HASH,
        strict_prior_policy_hash=STRICT_PRIOR_POLICY_HASH,
    )


def _parser_sources() -> tuple[ParserSourceDeclaration, ...]:
    return tuple(
        ParserSourceDeclaration(
            parser_name=parser_name,
            parser_source_hash=_h(f"{parser_name}-source"),
            parser_contract_hash=_h(f"{parser_name}-contract"),
            expected_input_artifact_type="LOCAL_CSV",
            expected_output_row_family=PARSER_OUTPUT_ROW_FAMILY_LABEL_BY_NAME[parser_name],
            expected_output_row_families=PARSER_OUTPUT_ROW_FAMILIES_BY_NAME[parser_name],
        )
        for parser_name in (
            "DAILY_COMPLETED_BAR_PARSER_PLAN",
            "HOURLY_COMPLETED_BAR_PARSER_PLAN",
            "SESSION_CALENDAR_PARSER_PLAN",
            "ROLL_CALENDAR_PARSER_PLAN",
            "COST_PARAMETER_PARSER_PLAN",
        )
    )


def _parser_plan_bundle() -> ParserPlanBundle:
    daily = DailyParserPlan(_parser_family_plan("DAILY_COMPLETED_BAR_PARSER_PLAN"))
    hourly = HourlyParserPlan(_parser_family_plan("HOURLY_COMPLETED_BAR_PARSER_PLAN"))
    session = SessionParserPlan(_parser_family_plan("SESSION_CALENDAR_PARSER_PLAN"))
    roll = RollParserPlan(_parser_family_plan("ROLL_CALENDAR_PARSER_PLAN"))
    cost = CostParameterParserPlan(_parser_family_plan("COST_PARAMETER_PARSER_PLAN"))
    return ParserPlanBundle(
        daily_parser_plan=daily,
        hourly_parser_plan=hourly,
        session_parser_plan=session,
        roll_parser_plan=roll,
        cost_parameter_parser_plan=cost,
        parser_plan_bundle_hash=canonical_sha256(
            {
                "artifact": "S27_V2_PARSER_PLAN_BUNDLE",
                "parser_plan_hashes": (
                    daily.family_plan.parser_plan_hash,
                    hourly.family_plan.parser_plan_hash,
                    session.family_plan.parser_plan_hash,
                    roll.family_plan.parser_plan_hash,
                    cost.family_plan.parser_plan_hash,
                ),
            }
        ),
    )


def _parser_family_plan(parser_name: str) -> ParserFamilyPlan:
    return ParserFamilyPlan(
        parser_family_label=parser_name,
        parser_extractor_source_hash=_h(f"{parser_name}-extractor"),
        expected_input_artifact_types=("LOCAL_CSV",),
        expected_output_row_schema_family=PARSER_OUTPUT_ROW_FAMILY_LABEL_BY_NAME[parser_name],
        canonical_row_locator_policy_hash=ROW_LOCATOR_POLICY_HASH,
        completed_bar_policy_hash=COMPLETED_BAR_POLICY_HASH,
        strict_prior_policy_hash=STRICT_PRIOR_POLICY_HASH,
        duplicate_policy_hash=_h(f"{parser_name}-duplicate"),
        missing_policy_hash=_h(f"{parser_name}-missing"),
        degraded_row_policy_hash=_h(f"{parser_name}-degraded"),
        fail_closed_reason_code="FAIL_CLOSED_ON_SCHEMA_OR_HASH_MISMATCH",
        parser_plan_hash=_expected_parser_family_plan_hash(parser_name),
    )


def _row_locator_contract(
    raw_source_files: tuple[RawSourceFileDeclaration, ...],
    parser_plan_bundle: ParserPlanBundle,
    raw_file_hash_set_hash: str,
) -> SourceRowLocatorContractBundle:
    parser_plan_hash_by_family = {
        "DAILY_CONTINUOUS_COMPLETED_BAR": parser_plan_bundle.daily_parser_plan.family_plan.parser_plan_hash,
        "DAILY_CURRENT_CONTRACT_COMPLETED_BAR": parser_plan_bundle.daily_parser_plan.family_plan.parser_plan_hash,
        "HOURLY_DECISION_COMPLETED_BAR": parser_plan_bundle.hourly_parser_plan.family_plan.parser_plan_hash,
        "HOURLY_FILL_COMPLETED_BAR": parser_plan_bundle.hourly_parser_plan.family_plan.parser_plan_hash,
        "SESSION_CALENDAR": parser_plan_bundle.session_parser_plan.family_plan.parser_plan_hash,
        "ROLL_CALENDAR": parser_plan_bundle.roll_parser_plan.family_plan.parser_plan_hash,
        "COST_PARAMETER": parser_plan_bundle.cost_parameter_parser_plan.family_plan.parser_plan_hash,
    }
    contracts = tuple(
        _row_locator_family_contract(raw_declaration, parser_plan_hash_by_family[raw_declaration.local_file.expected_row_family])
        for raw_declaration in raw_source_files
    )
    return SourceRowLocatorContractBundle(
        status=S27_V2_ROW_LOCATOR_CONTRACT_ONLY_STATUS,
        input_directory_declaration_hash=INPUT_DIRECTORY_HASH,
        source_universe_manifest_hash=_h("source-universe-placeholder"),
        raw_file_hash_set_hash=raw_file_hash_set_hash,
        row_locator_policy_hash=ROW_LOCATOR_POLICY_HASH,
        row_family_contracts=contracts,
        row_locator_contract_bundle_hash=_expected_row_locator_contract_bundle_hash(
            contracts,
            raw_file_hash_set_hash,
        ),
    )


def _row_locator_family_contract(
    raw_declaration: RawSourceFileDeclaration,
    parser_plan_hash: str,
) -> SourceRowFamilyLocatorContract:
    row_family = raw_declaration.local_file.expected_row_family
    return SourceRowFamilyLocatorContract(
        row_family=row_family,
        family_status=PLANNED_ROW_LOCATOR_FAMILY_STATUS,
        raw_file_declaration_hash=canonical_sha256(raw_declaration),
        parser_family_plan_hash=parser_plan_hash,
        expected_output_schema_family=row_family,
        field_binding=RowLocatorFieldBinding(
            row_family=row_family,
            raw_symbol_family="ZN",
            locator_component_names=("completed_timestamp_utc", "trading_date", "raw_symbol", "row_locator"),
            timestamp_component_name="completed_timestamp_utc",
            trading_date_component_name="trading_date",
            canonical_serialization_policy_hash=CANONICAL_POLICY_HASH,
            row_locator_policy_hash=ROW_LOCATOR_POLICY_HASH,
        ),
        completed_bar_policy_hash=COMPLETED_BAR_POLICY_HASH,
        strict_prior_policy_hash=STRICT_PRIOR_POLICY_HASH,
        duplicate_policy_hash=_h(f"{row_family}-locator-duplicate"),
        missing_policy_hash=_h(f"{row_family}-locator-missing"),
        no_future_rows_proof_hash=_h(f"{row_family}-locator-no-future"),
        planned_row_universe_hash=_h(f"{row_family}-planned-row-universe"),
        planned_locator_output_hash=_h(f"{row_family}-planned-locator-output"),
        family_contract_hash=_expected_row_locator_family_contract_hash(
            row_family=row_family,
            raw_file_declaration_hash=canonical_sha256(raw_declaration),
            parser_plan_hash=parser_plan_hash,
        ),
    )


def _source_universe_contract(
    raw_file_hash_set_hash: str,
    row_locator_contract_bundle_hash: str,
) -> SourceUniverseContractBundle:
    inclusion_rules = tuple(
        SourceUniverseInclusionRule(
            rule_label=f"{family}_RULE",
            applies_to_family=family,
            inclusion_reason_code_hash=_h(f"{family}-include"),
            exclusion_reason_code_hash=_h(f"{family}-exclude"),
            rule_policy_hash=_h(f"{family}-rule"),
        )
        for family in REQUIRED_SOURCE_UNIVERSE_FAMILIES
    )
    family_contracts = tuple(
        _source_universe_family_contract(family)
        for family in REQUIRED_SOURCE_UNIVERSE_FAMILIES
    )
    return SourceUniverseContractBundle(
        status=S27_V2_SOURCE_UNIVERSE_CONTRACT_ONLY_STATUS,
        strategy_id=S27_V2_STRATEGY_ID,
        lane=S27_V2_LANE,
        instrument=S27_V2_INSTRUMENT,
        requested_start="2024-01-01",
        requested_end="2024-01-02",
        raw_file_hash_set_hash=raw_file_hash_set_hash,
        row_locator_contract_bundle_hash=row_locator_contract_bundle_hash,
        strict_prior_candidate_set_hash=STRICT_PRIOR_POLICY_HASH,
        canonical_row_locator_serialization_hash=CANONICAL_POLICY_HASH,
        inclusion_rules=inclusion_rules,
        family_contracts=family_contracts,
        source_universe_contract_bundle_hash=_expected_source_universe_contract_bundle_hash(
            raw_file_hash_set_hash=raw_file_hash_set_hash,
            row_locator_contract_bundle_hash=row_locator_contract_bundle_hash,
            inclusion_rules=inclusion_rules,
            family_contracts=family_contracts,
        ),
    )


def _source_universe_family_contract(universe_family: str) -> SourceUniverseFamilyContract:
    locator_family_by_universe_family = {
        "INSTRUMENT_UNIVERSE": "N/A",
        "RAW_SYMBOL_UNIVERSE": "N/A",
        "DAILY_ROW_UNIVERSE": "DAILY_CONTINUOUS_COMPLETED_BAR",
        "HOURLY_DECISION_FILL_ROW_UNIVERSE": "HOURLY_DECISION_COMPLETED_BAR",
        "SESSION_ROW_UNIVERSE": "SESSION_CALENDAR",
        "ROLL_ROW_UNIVERSE": "ROLL_CALENDAR",
        "COST_PARAMETER_ROW_UNIVERSE": "COST_PARAMETER",
    }
    return SourceUniverseFamilyContract(
        universe_family=universe_family,
        family_status=PLANNED_SOURCE_UNIVERSE_FAMILY_STATUS,
        source_row_locator_family=locator_family_by_universe_family[universe_family],
        planned_universe_hash=_h(f"{universe_family}-planned-universe"),
        inclusion_rule_hash=_h(f"{universe_family}-inclusion-rule"),
        duplicate_policy_hash=_h(f"{universe_family}-duplicate"),
        missing_policy_hash=_h(f"{universe_family}-missing"),
        repair_rejection_policy_hash=_h(f"{universe_family}-repair-reject"),
        no_future_rows_proof_hash=_h(f"{universe_family}-no-future"),
        family_contract_hash=_expected_source_universe_family_contract_hash(universe_family),
    )


def _canonical_policy() -> CanonicalSerializationPolicy:
    return CanonicalSerializationPolicy(
        status_label=S27_V2_CANONICAL_SERIALIZATION_POLICY_CONTRACT_ONLY_STATUS,
        schema_hash=_h("canonical-schema"),
        hash_algorithm_version_hash=_h("hash-algorithm"),
        field_ordering_policy_hash=_h("field-ordering"),
        decimal_float_normalization_policy_hash=_h("decimal-float"),
        timezone_normalization_policy_hash=_h("timezone"),
        row_ordering_collation_policy_hash=_h("row-ordering"),
        null_missing_sentinel_policy_hash=_h("null-missing"),
        string_encoding_policy_hash=_h("string-encoding"),
        hash_payload_version_policy_hash=_h("payload-version"),
        canonical_serialization_policy_hash=CANONICAL_POLICY_HASH,
    )


def _h(label: str) -> str:
    return sha256(label.encode("utf-8")).hexdigest()


def _expected_raw_file_hash_set_hash(
    raw_source_files: tuple[RawSourceFileDeclaration, ...],
    parser_plan_bundle: ParserPlanBundle,
) -> str:
    parser_plan_hash_by_family = {
        "DAILY_CONTINUOUS_COMPLETED_BAR": parser_plan_bundle.daily_parser_plan.family_plan.parser_plan_hash,
        "DAILY_CURRENT_CONTRACT_COMPLETED_BAR": parser_plan_bundle.daily_parser_plan.family_plan.parser_plan_hash,
        "HOURLY_DECISION_COMPLETED_BAR": parser_plan_bundle.hourly_parser_plan.family_plan.parser_plan_hash,
        "HOURLY_FILL_COMPLETED_BAR": parser_plan_bundle.hourly_parser_plan.family_plan.parser_plan_hash,
        "SESSION_CALENDAR": parser_plan_bundle.session_parser_plan.family_plan.parser_plan_hash,
        "ROLL_CALENDAR": parser_plan_bundle.roll_parser_plan.family_plan.parser_plan_hash,
        "COST_PARAMETER": parser_plan_bundle.cost_parameter_parser_plan.family_plan.parser_plan_hash,
    }
    binding_hashes = tuple(
        canonical_sha256(
            {
                "artifact": "S27_V2_RAW_SOURCE_FILE_HASH_BINDING",
                "file_family": declaration.local_file.expected_row_family,
                "file_sha256": declaration.local_file.expected_sha256,
                "local_file_declaration_hash": canonical_sha256(declaration.local_file),
                "parser_family_plan_hash": parser_plan_hash_by_family[
                    declaration.local_file.expected_row_family
                ],
            }
        )
        for declaration in raw_source_files
    )
    return canonical_sha256(
        {
            "artifact": "S27_V2_RAW_FILE_HASH_SET",
            "binding_hashes": binding_hashes,
            "input_directory_declaration_hash": INPUT_DIRECTORY_HASH,
            "parser_plan_bundle_hash": parser_plan_bundle.parser_plan_bundle_hash,
        }
    )


def _expected_parser_family_plan_hash(parser_name: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_PARSER_FAMILY_PLAN",
            "canonical_row_locator_policy_hash": ROW_LOCATOR_POLICY_HASH,
            "completed_bar_policy_hash": COMPLETED_BAR_POLICY_HASH,
            "degraded_row_policy_hash": _h(f"{parser_name}-degraded"),
            "duplicate_policy_hash": _h(f"{parser_name}-duplicate"),
            "expected_input_artifact_types": ("LOCAL_CSV",),
            "expected_output_row_schema_family": PARSER_OUTPUT_ROW_FAMILY_LABEL_BY_NAME[parser_name],
            "fail_closed_reason_code": "FAIL_CLOSED_ON_SCHEMA_OR_HASH_MISMATCH",
            "missing_policy_hash": _h(f"{parser_name}-missing"),
            "parser_extractor_source_hash": _h(f"{parser_name}-extractor"),
            "parser_family_label": parser_name,
            "strict_prior_policy_hash": STRICT_PRIOR_POLICY_HASH,
        }
    )


def _expected_row_locator_family_contract_hash(
    *,
    row_family: str,
    raw_file_declaration_hash: str,
    parser_plan_hash: str,
) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_ROW_LOCATOR_FAMILY_CONTRACT",
            "completed_bar_policy_hash": COMPLETED_BAR_POLICY_HASH,
            "duplicate_policy_hash": _h(f"{row_family}-locator-duplicate"),
            "expected_output_schema_family": row_family,
            "family_status": PLANNED_ROW_LOCATOR_FAMILY_STATUS,
            "field_binding": RowLocatorFieldBinding(
                row_family=row_family,
                raw_symbol_family="ZN",
                locator_component_names=("completed_timestamp_utc", "trading_date", "raw_symbol", "row_locator"),
                timestamp_component_name="completed_timestamp_utc",
                trading_date_component_name="trading_date",
                canonical_serialization_policy_hash=CANONICAL_POLICY_HASH,
                row_locator_policy_hash=ROW_LOCATOR_POLICY_HASH,
            ),
            "missing_policy_hash": _h(f"{row_family}-locator-missing"),
            "no_future_rows_proof_hash": _h(f"{row_family}-locator-no-future"),
            "parser_family_plan_hash": parser_plan_hash,
            "planned_locator_output_hash": _h(f"{row_family}-planned-locator-output"),
            "planned_row_universe_hash": _h(f"{row_family}-planned-row-universe"),
            "raw_file_declaration_hash": raw_file_declaration_hash,
            "row_family": row_family,
            "strict_prior_policy_hash": STRICT_PRIOR_POLICY_HASH,
        }
    )


def _expected_row_locator_contract_bundle_hash(
    contracts: tuple[SourceRowFamilyLocatorContract, ...],
    raw_file_hash_set_hash: str,
) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_ROW_LOCATOR_CONTRACT_BUNDLE",
            "family_contract_hashes": tuple(
                contract.family_contract_hash
                for contract in contracts
            ),
            "input_directory_declaration_hash": INPUT_DIRECTORY_HASH,
            "raw_file_hash_set_hash": raw_file_hash_set_hash,
            "row_locator_policy_hash": ROW_LOCATOR_POLICY_HASH,
            "status": S27_V2_ROW_LOCATOR_CONTRACT_ONLY_STATUS,
        }
    )


def _expected_source_universe_family_contract_hash(universe_family: str) -> str:
    locator_family_by_universe_family = {
        "INSTRUMENT_UNIVERSE": "N/A",
        "RAW_SYMBOL_UNIVERSE": "N/A",
        "DAILY_ROW_UNIVERSE": "DAILY_CONTINUOUS_COMPLETED_BAR",
        "HOURLY_DECISION_FILL_ROW_UNIVERSE": "HOURLY_DECISION_COMPLETED_BAR",
        "SESSION_ROW_UNIVERSE": "SESSION_CALENDAR",
        "ROLL_ROW_UNIVERSE": "ROLL_CALENDAR",
        "COST_PARAMETER_ROW_UNIVERSE": "COST_PARAMETER",
    }
    return canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_UNIVERSE_FAMILY_CONTRACT",
            "duplicate_policy_hash": _h(f"{universe_family}-duplicate"),
            "family_status": PLANNED_SOURCE_UNIVERSE_FAMILY_STATUS,
            "inclusion_rule_hash": _h(f"{universe_family}-inclusion-rule"),
            "missing_policy_hash": _h(f"{universe_family}-missing"),
            "no_future_rows_proof_hash": _h(f"{universe_family}-no-future"),
            "planned_universe_hash": _h(f"{universe_family}-planned-universe"),
            "repair_rejection_policy_hash": _h(f"{universe_family}-repair-reject"),
            "source_row_locator_family": locator_family_by_universe_family[universe_family],
            "universe_family": universe_family,
        }
    )


def _source_universe_family_contract_hash(contract: SourceUniverseFamilyContract) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_UNIVERSE_FAMILY_CONTRACT",
            "duplicate_policy_hash": contract.duplicate_policy_hash,
            "family_status": contract.family_status,
            "inclusion_rule_hash": contract.inclusion_rule_hash,
            "missing_policy_hash": contract.missing_policy_hash,
            "no_future_rows_proof_hash": contract.no_future_rows_proof_hash,
            "planned_universe_hash": contract.planned_universe_hash,
            "repair_rejection_policy_hash": contract.repair_rejection_policy_hash,
            "source_row_locator_family": contract.source_row_locator_family,
            "universe_family": contract.universe_family,
        }
    )


def _expected_source_universe_contract_bundle_hash(
    *,
    raw_file_hash_set_hash: str,
    row_locator_contract_bundle_hash: str,
    inclusion_rules: tuple[SourceUniverseInclusionRule, ...],
    family_contracts: tuple[SourceUniverseFamilyContract, ...],
) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_SOURCE_UNIVERSE_CONTRACT_BUNDLE",
            "family_contract_hashes": tuple(
                contract.family_contract_hash
                for contract in family_contracts
            ),
            "inclusion_rule_hashes": tuple(
                canonical_sha256(rule)
                for rule in inclusion_rules
            ),
            "instrument": S27_V2_INSTRUMENT,
            "lane": S27_V2_LANE,
            "raw_file_hash_set_hash": raw_file_hash_set_hash,
            "requested_end": "2024-01-02",
            "requested_start": "2024-01-01",
            "row_locator_contract_bundle_hash": row_locator_contract_bundle_hash,
            "status": S27_V2_SOURCE_UNIVERSE_CONTRACT_ONLY_STATUS,
            "strategy_id": S27_V2_STRATEGY_ID,
        }
    )

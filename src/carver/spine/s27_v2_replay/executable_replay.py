from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import (
    BLOCKED_COST_SCHEMA,
    BLOCKED_LEVEL_COMPATIBILITY,
    BLOCKED_RUNTIME_HISTORY,
    BLOCKED_SIGMA,
    BLOCKED_TICK,
    REQUIRED_UNRESOLVED_GATE_LABELS,
)
from .local_replay import (
    LocalParserFileReplayCompletionArtifacts,
    LocalParserFileReplaySlice1Inputs,
    canonical_sha256,
    build_local_parser_file_replay_completion,
)
from .validation import require_finite_number, require_hash, require_non_empty_tuple, require_text, require_tuple


S27_V2_EXECUTABLE_REPLAY_PHASE1_AUTHORIZATION = (
    "S27_V2_LOCAL_ONLY_EXECUTABLE_REPLAY_LEDGER_IMPLEMENTATION_PHASE_1_FAIL_CLOSED"
)
S27_V2_EXECUTABLE_REPLAY_PHASE2_AUTHORIZATION = (
    "S27_V2_LOCAL_ONLY_EXECUTABLE_REPLAY_LEDGER_IMPLEMENTATION_PHASE_2"
)
S27_V2_EXECUTABLE_REPLAY_PHASE1_STATUS = "FAIL_CLOSED_EXECUTABLE_REPLAY_LEDGER_SURFACE_PASS_NO_RESULT"
S27_V2_EXECUTABLE_REPLAY_PROVENANCE_STATUS = "S27_V2_EXECUTABLE_REPLAY_PROVENANCE_LEDGER_FAIL_CLOSED_ONLY"
S27_V2_EXECUTABLE_REPLAY_VALIDATION_STATUS = "S27_V2_EXECUTABLE_REPLAY_VALIDATION_LEDGER_FAIL_CLOSED_ONLY"
S27_V2_EXECUTABLE_REPLAY_TRUSTED_BUNDLE_STATUS = "S27_V2_EXECUTABLE_REPLAY_TRUSTED_BUNDLE_FAIL_CLOSED_NOT_EVIDENCE"
S27_V2_EXECUTABLE_REPLAY_PHASE2_STATUS = (
    "S27_V2_EXECUTABLE_REPLAY_PHASE2_RUNTIME_SURFACES_NOT_RESULT_NOT_EVIDENCE"
)

S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
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

CONTROLLED_CONSTRUCTION_RUN_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
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

REQUIRED_CONSTRUCTION_RUN_MANIFEST_KEYS = (
    "artifact",
    "artifact_files",
    "authorization",
    "boundaries",
    "construction_contract_hash",
    "input_directory_declaration_hash",
    "input_pack",
    "non_authorizations",
    "output_directory",
    "parser_plan_bundle_hash",
    "raw_file_hash_set_hash",
    "row_family_summary",
    "row_locator_hash",
    "source_universe_manifest_hash",
    "status",
    "trusted_bundle_contract_hash",
    "validation_contract_bundle_hash",
    "verification",
)

REQUIRED_CONSTRUCTION_RUN_ARTIFACT_FILES = (
    "artifacts/00_input_directory_declaration.json",
    "artifacts/01_parser_plan_bundle.json",
    "artifacts/02_row_locator_contract.json",
    "artifacts/03_source_universe_contract.json",
    "artifacts/04_canonical_serialization_policy.json",
    "artifacts/05_parsed_declared_source_files.json",
    "artifacts/06_raw_file_hash_contract.json",
    "artifacts/07_parser_output_contract.json",
    "artifacts/08_source_row_batch_contract.json",
    "artifacts/09_source_row_selection_external_authority.json",
    "artifacts/10_source_input_selection_contract.json",
    "artifacts/11_source_input_manifest_contract.json",
    "artifacts/12_level_compatibility_input_contract.json",
    "artifacts/13_level_compatibility_contract.json",
    "artifacts/14_runtime_history_input_contract.json",
    "artifacts/15_runtime_history_contract.json",
    "artifacts/16_forecast_input_contract.json",
    "artifacts/17_forecast_contract.json",
    "artifacts/18_position_input_contract.json",
    "artifacts/19_position_contract.json",
    "artifacts/20_order_input_contract.json",
    "artifacts/21_order_contract.json",
    "artifacts/22_fill_input_contract.json",
    "artifacts/23_fill_contract.json",
    "artifacts/24_replay_trust_root.json",
    "artifacts/25_evidence_manifest.json",
    "artifacts/26_cost_input_contract.json",
    "artifacts/27_cost_contract.json",
    "artifacts/28_pnl_input_contract.json",
    "artifacts/29_pnl_contract.json",
    "artifacts/30_construction_contract.json",
    "artifacts/31_validation_input_contract.json",
    "artifacts/32_validation_contract.json",
    "artifacts/33_trusted_bundle_contract.json",
)

EXECUTABLE_LEDGER_LABELS = (
    "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER",
    "RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM",
    "FORECAST_REPLAY_LEDGER",
    "DESIRED_POSITION_LEDGER",
    "LIMIT_ORDER_LEDGER",
    "MARKET_ORDER_LEDGER",
    "WORKING_ORDER_TRANSITION_LEDGER",
    "FILL_LEDGER",
    "COMMISSION_LEDGER",
    "SPREAD_COST_LEDGER",
    "PNL_LEDGER",
)

_NO_EXECUTABLE_ROW_HASH = canonical_sha256(
    {
        "artifact": "S27_V2_NO_EXECUTABLE_LEDGER_ROW_EMITTED",
        "authorization": S27_V2_EXECUTABLE_REPLAY_PHASE1_AUTHORIZATION,
    }
)

PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS = "EXECUTABLE_NON_RESULT_LEVEL_COMPATIBILITY_SAME_LEVEL_PASS"
PHASE2_LEVEL_COMPATIBILITY_FAIL_STATUS = "FAIL_CLOSED_LEVEL_COMPATIBILITY_NOT_PROVED"
PHASE2_RUNTIME_HISTORY_READY_STATUS = "RUNTIME_HISTORY_INPUT_HISTORY_SUFFICIENT_NOT_FORECAST_EVIDENCE"
PHASE2_RUNTIME_HISTORY_FAIL_STATUS = "FAIL_CLOSED_INSUFFICIENT_STRICT_PRIOR_RUNTIME_HISTORY"
PHASE2_RUNTIME_HISTORY_MINIMUM_DAILY_ROWS = 64


@dataclass(frozen=True)
class ExecutableReplayGateLedgerRow:
    ledger_label: str
    gate_status: str
    reason_code: str
    blocked_gate_labels: tuple[str, ...]
    upstream_authority_hashes: tuple[str, ...]
    executable_row_emitted: bool
    executable_row_hash: str
    gate_row_hash: str

    def validate(self) -> None:
        require_text("S27 v2 executable replay gate ledger label", self.ledger_label)
        if self.ledger_label not in EXECUTABLE_LEDGER_LABELS:
            raise CarverBlocked("S27 v2 executable replay gate ledger label is not locked")
        require_text("S27 v2 executable replay gate status", self.gate_status)
        if self.gate_status != "FAIL_CLOSED_NO_EXECUTABLE_ROW":
            raise CarverBlocked("S27 v2 executable replay gate must remain fail-closed")
        require_text("S27 v2 executable replay gate reason code", self.reason_code)
        if self.reason_code != _reason_code_by_ledger_label(self.ledger_label):
            raise CarverBlocked("S27 v2 executable replay gate reason must match locked ledger label")
        require_non_empty_tuple("S27 v2 executable replay blocked gates", self.blocked_gate_labels)
        for blocked_gate in self.blocked_gate_labels:
            require_text("S27 v2 executable replay blocked gate", blocked_gate)
            if blocked_gate not in REQUIRED_UNRESOLVED_GATE_LABELS:
                raise CarverBlocked("S27 v2 executable replay blocked gate must be source-locked")
        if self.blocked_gate_labels != _blocked_gates_by_ledger_label(self.ledger_label):
            raise CarverBlocked("S27 v2 executable replay blocked gates must match locked ledger label")
        require_non_empty_tuple("S27 v2 executable replay upstream hashes", self.upstream_authority_hashes)
        for upstream_hash in self.upstream_authority_hashes:
            require_hash("S27 v2 executable replay upstream authority hash", upstream_hash)
        if self.executable_row_emitted is not False:
            raise CarverBlocked("S27 v2 phase 1 must not emit executable ledger rows")
        require_hash("S27 v2 executable replay no-row hash", self.executable_row_hash)
        if self.executable_row_hash != _NO_EXECUTABLE_ROW_HASH:
            raise CarverBlocked("S27 v2 executable replay no-row hash must be locked")
        require_hash("S27 v2 executable replay gate row hash", self.gate_row_hash)
        if self.gate_row_hash != canonical_sha256(_gate_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 executable replay gate row hash must be content-bound")


@dataclass(frozen=True)
class ExecutableReplayProvenanceLedger:
    status: str
    authorization_label: str
    input_directory_declaration_hash: str
    raw_file_hash_set_hash: str
    parser_output_contract_hash: str
    source_row_batch_contract_hash: str
    source_input_manifest_hash: str
    level_compatibility_contract_hash: str
    runtime_history_contract_hash: str
    construction_contract_hash: str
    validation_contract_bundle_hash: str
    trusted_bundle_contract_hash: str
    row_family_hashes: tuple[tuple[str, tuple[str, ...]], ...]
    price_row_close_prices: tuple[tuple[str, tuple[float, ...]], ...]
    construction_run_manifest_sha256: str
    provenance_ledger_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS

    def validate(self) -> None:
        require_text("S27 v2 executable replay provenance status", self.status)
        if self.status != S27_V2_EXECUTABLE_REPLAY_PROVENANCE_STATUS:
            raise CarverBlocked("S27 v2 executable replay provenance must remain fail-closed only")
        require_text("S27 v2 executable replay authorization label", self.authorization_label)
        if self.authorization_label != S27_V2_EXECUTABLE_REPLAY_PHASE1_AUTHORIZATION:
            raise CarverBlocked("S27 v2 executable replay authorization label is not locked")
        require_hash("S27 v2 executable input directory hash", self.input_directory_declaration_hash)
        require_hash("S27 v2 executable raw file hash set", self.raw_file_hash_set_hash)
        require_hash("S27 v2 executable parser output contract hash", self.parser_output_contract_hash)
        require_hash("S27 v2 executable source-row batch contract hash", self.source_row_batch_contract_hash)
        require_hash("S27 v2 executable source-input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 executable level compatibility contract hash", self.level_compatibility_contract_hash)
        require_hash("S27 v2 executable runtime history contract hash", self.runtime_history_contract_hash)
        require_hash("S27 v2 executable construction contract hash", self.construction_contract_hash)
        require_hash("S27 v2 executable validation contract bundle hash", self.validation_contract_bundle_hash)
        require_hash("S27 v2 executable trusted bundle contract hash", self.trusted_bundle_contract_hash)
        require_non_empty_tuple("S27 v2 executable row family hashes", self.row_family_hashes)
        if tuple(family for family, _ in self.row_family_hashes) != (
            "DAILY_CONTINUOUS_COMPLETED_BAR",
            "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
            "HOURLY_DECISION_COMPLETED_BAR",
            "HOURLY_FILL_COMPLETED_BAR",
            "SESSION_CALENDAR",
            "ROLL_CALENDAR",
            "COST_PARAMETER",
        ):
            raise CarverBlocked("S27 v2 executable row family hashes must match locked local families")
        for family, row_hashes in self.row_family_hashes:
            require_text("S27 v2 executable row family", family)
            require_non_empty_tuple("S27 v2 executable row family row hashes", row_hashes)
            for row_hash in row_hashes:
                require_hash("S27 v2 executable row family row hash", row_hash)
        require_non_empty_tuple("S27 v2 executable price row close prices", self.price_row_close_prices)
        if tuple(family for family, _ in self.price_row_close_prices) != (
            "DAILY_CONTINUOUS_COMPLETED_BAR",
            "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
            "HOURLY_DECISION_COMPLETED_BAR",
            "HOURLY_FILL_COMPLETED_BAR",
        ):
            raise CarverBlocked("S27 v2 executable price row close-price families must match locked local families")
        row_hashes_by_family = _row_hashes_by_family(self.row_family_hashes)
        for family, close_prices in self.price_row_close_prices:
            require_non_empty_tuple("S27 v2 executable price row close-price tuple", close_prices)
            if len(close_prices) != len(row_hashes_by_family[family]):
                raise CarverBlocked("S27 v2 executable price row close prices must bind row hashes")
            for close_price in close_prices:
                require_finite_number("S27 v2 executable price row close price", close_price)
        require_hash("S27 v2 executable construction run manifest hash", self.construction_run_manifest_sha256)
        if self.non_authorizations != S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 executable provenance must preserve phase 1 non-authorizations")
        require_hash("S27 v2 executable provenance ledger hash", self.provenance_ledger_hash)
        if self.provenance_ledger_hash != canonical_sha256(_provenance_ledger_hash_payload(self)):
            raise CarverBlocked("S27 v2 executable provenance ledger hash must be content-bound")


@dataclass(frozen=True)
class ExecutableReplayValidationLedger:
    status: str
    authorization_label: str
    gate_rows: tuple[ExecutableReplayGateLedgerRow, ...]
    required_unresolved_gate_labels: tuple[str, ...]
    forecast_rows_emitted: bool
    order_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    validation_ledger_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS

    def validate(self) -> None:
        require_text("S27 v2 executable validation status", self.status)
        if self.status != S27_V2_EXECUTABLE_REPLAY_VALIDATION_STATUS:
            raise CarverBlocked("S27 v2 executable validation must remain fail-closed only")
        require_text("S27 v2 executable validation authorization label", self.authorization_label)
        if self.authorization_label != S27_V2_EXECUTABLE_REPLAY_PHASE1_AUTHORIZATION:
            raise CarverBlocked("S27 v2 executable validation authorization label is not locked")
        require_non_empty_tuple("S27 v2 executable validation gate rows", self.gate_rows)
        if tuple(row.ledger_label for row in self.gate_rows) != EXECUTABLE_LEDGER_LABELS:
            raise CarverBlocked("S27 v2 executable validation gates must cover locked executable ledgers")
        for row in self.gate_rows:
            row.validate()
        require_tuple("S27 v2 executable required unresolved gates", self.required_unresolved_gate_labels)
        for blocked_gate in self.required_unresolved_gate_labels:
            require_text("S27 v2 executable unresolved gate", blocked_gate)
            if blocked_gate not in REQUIRED_UNRESOLVED_GATE_LABELS:
                raise CarverBlocked("S27 v2 executable unresolved gate must be source-locked")
        if self.required_unresolved_gate_labels != _expected_unresolved_gate_labels(self.gate_rows):
            raise CarverBlocked("S27 v2 executable unresolved gate set must match gate rows exactly")
        if any(
            flag is not False
            for flag in (
                self.forecast_rows_emitted,
                self.order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 phase 1 must not emit result or evidence rows")
        if self.non_authorizations != S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 executable validation must preserve phase 1 non-authorizations")
        require_hash("S27 v2 executable validation ledger hash", self.validation_ledger_hash)
        if self.validation_ledger_hash != canonical_sha256(_validation_ledger_hash_payload(self)):
            raise CarverBlocked("S27 v2 executable validation ledger hash must be content-bound")


@dataclass(frozen=True)
class FailClosedExecutableReplayBundle:
    status: str
    authorization_label: str
    input_pack_path: str
    construction_output_path: str
    provenance_ledger: ExecutableReplayProvenanceLedger
    validation_ledger: ExecutableReplayValidationLedger
    trusted_bundle_contract_hash: str
    fail_closed_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS

    def validate(self) -> None:
        require_text("S27 v2 fail-closed executable replay status", self.status)
        if self.status != S27_V2_EXECUTABLE_REPLAY_TRUSTED_BUNDLE_STATUS:
            raise CarverBlocked("S27 v2 executable replay bundle must remain non-evidence")
        require_text("S27 v2 executable replay bundle authorization", self.authorization_label)
        if self.authorization_label != S27_V2_EXECUTABLE_REPLAY_PHASE1_AUTHORIZATION:
            raise CarverBlocked("S27 v2 executable replay bundle authorization is not locked")
        require_text("S27 v2 executable input pack path", self.input_pack_path)
        require_text("S27 v2 executable construction output path", self.construction_output_path)
        self.provenance_ledger.validate()
        self.validation_ledger.validate()
        require_hash("S27 v2 executable trusted bundle contract hash", self.trusted_bundle_contract_hash)
        if self.trusted_bundle_contract_hash != self.provenance_ledger.trusted_bundle_contract_hash:
            raise CarverBlocked("S27 v2 executable bundle must bind provenance trusted bundle contract")
        if self.non_authorizations != S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 executable bundle must preserve phase 1 non-authorizations")
        require_hash("S27 v2 executable fail-closed bundle hash", self.fail_closed_bundle_hash)
        if self.fail_closed_bundle_hash != canonical_sha256(_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 executable bundle hash must be content-bound")


@dataclass(frozen=True)
class Phase2LevelCompatibilityLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    source_input_manifest_hash: str
    level_compatibility_contract_hash: str
    daily_continuous_row_hash: str
    daily_current_contract_row_hash: str
    hourly_decision_row_hash: str
    hourly_fill_row_hash: str
    daily_continuous_close_price: float
    daily_current_contract_close_price: float
    hourly_decision_close_price: float
    hourly_fill_close_price: float
    row_hash: str

    def validate(self) -> None:
        require_text("S27 v2 phase 2 level ledger label", self.ledger_label)
        if self.ledger_label != "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER":
            raise CarverBlocked("S27 v2 phase 2 level ledger label is not locked")
        require_text("S27 v2 phase 2 level ledger status", self.row_status)
        if self.row_status not in (
            PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS,
            PHASE2_LEVEL_COMPATIBILITY_FAIL_STATUS,
        ):
            raise CarverBlocked("S27 v2 phase 2 level ledger status is not locked")
        require_text("S27 v2 phase 2 level reason", self.reason_code)
        if self.row_status == PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS:
            if self.reason_code != "SAME_LEVEL_COMPATIBLE":
                raise CarverBlocked("S27 v2 phase 2 level pass reason must be locked")
            if len(
                {
                    self.daily_continuous_close_price,
                    self.daily_current_contract_close_price,
                    self.hourly_decision_close_price,
                    self.hourly_fill_close_price,
                }
            ) != 1:
                raise CarverBlocked("S27 v2 phase 2 level pass requires identical same-level prices")
        if self.row_status == PHASE2_LEVEL_COMPATIBILITY_FAIL_STATUS and self.reason_code != (
            "FAIL_CLOSED_UNBRIDGED_DAILY_HOURLY_LEVEL_MISMATCH"
        ):
            raise CarverBlocked("S27 v2 phase 2 level fail reason must be locked")
        require_hash("S27 v2 phase 2 source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 phase 2 level contract hash", self.level_compatibility_contract_hash)
        require_hash("S27 v2 phase 2 daily continuous row hash", self.daily_continuous_row_hash)
        require_hash("S27 v2 phase 2 daily current-contract row hash", self.daily_current_contract_row_hash)
        require_hash("S27 v2 phase 2 hourly decision row hash", self.hourly_decision_row_hash)
        require_hash("S27 v2 phase 2 hourly fill row hash", self.hourly_fill_row_hash)
        for name, price in (
            ("daily continuous close", self.daily_continuous_close_price),
            ("daily current-contract close", self.daily_current_contract_close_price),
            ("hourly decision close", self.hourly_decision_close_price),
            ("hourly fill close", self.hourly_fill_close_price),
        ):
            if not isinstance(price, (int, float)) or isinstance(price, bool):
                raise CarverBlocked(f"S27 v2 phase 2 {name} must be numeric")
        require_hash("S27 v2 phase 2 level row hash", self.row_hash)
        if self.row_hash != canonical_sha256(_phase2_level_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 phase 2 level row hash must be content-bound")


@dataclass(frozen=True)
class Phase2RuntimeHistoryLedgerRow:
    ledger_label: str
    row_status: str
    reason_code: str
    source_input_manifest_hash: str
    runtime_history_contract_hash: str
    level_compatibility_row_hash: str
    level_compatibility_passed: bool
    daily_continuous_row_hashes: tuple[str, ...]
    hourly_decision_row_hashes: tuple[str, ...]
    observed_daily_continuous_rows: int
    required_minimum_daily_continuous_rows: int
    runtime_numeric_values_emitted: bool
    row_hash: str

    def validate(self) -> None:
        require_text("S27 v2 phase 2 runtime ledger label", self.ledger_label)
        if self.ledger_label != "RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM":
            raise CarverBlocked("S27 v2 phase 2 runtime ledger label is not locked")
        require_text("S27 v2 phase 2 runtime ledger status", self.row_status)
        if self.row_status not in (
            PHASE2_RUNTIME_HISTORY_READY_STATUS,
            PHASE2_RUNTIME_HISTORY_FAIL_STATUS,
        ):
            raise CarverBlocked("S27 v2 phase 2 runtime ledger status is not locked")
        require_text("S27 v2 phase 2 runtime reason", self.reason_code)
        if self.row_status == PHASE2_RUNTIME_HISTORY_READY_STATUS and self.reason_code != (
            "STRICT_PRIOR_HISTORY_COUNT_SUFFICIENT_RUNTIME_VALUES_NOT_EMITTED_IN_PHASE2"
        ):
            raise CarverBlocked("S27 v2 phase 2 runtime ready reason must be locked")
        if self.row_status == PHASE2_RUNTIME_HISTORY_FAIL_STATUS and self.reason_code != (
            "FAIL_CLOSED_MINIMUM_64_DAILY_STRICT_PRIOR_ROWS_NOT_AVAILABLE"
        ) and self.reason_code != "FAIL_CLOSED_UPSTREAM_LEVEL_COMPATIBILITY_NOT_PROVED":
            raise CarverBlocked("S27 v2 phase 2 runtime fail reason must be locked")
        require_hash("S27 v2 phase 2 runtime source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 phase 2 runtime contract hash", self.runtime_history_contract_hash)
        require_hash("S27 v2 phase 2 runtime level row hash", self.level_compatibility_row_hash)
        if not isinstance(self.level_compatibility_passed, bool):
            raise CarverBlocked("S27 v2 phase 2 runtime level pass flag must be boolean")
        require_non_empty_tuple("S27 v2 phase 2 runtime daily row hashes", self.daily_continuous_row_hashes)
        for row_hash in self.daily_continuous_row_hashes:
            require_hash("S27 v2 phase 2 runtime daily row hash", row_hash)
        require_non_empty_tuple("S27 v2 phase 2 runtime hourly row hashes", self.hourly_decision_row_hashes)
        for row_hash in self.hourly_decision_row_hashes:
            require_hash("S27 v2 phase 2 runtime hourly row hash", row_hash)
        if self.observed_daily_continuous_rows != len(self.daily_continuous_row_hashes):
            raise CarverBlocked("S27 v2 phase 2 runtime observed daily count must bind row hashes")
        if self.required_minimum_daily_continuous_rows != PHASE2_RUNTIME_HISTORY_MINIMUM_DAILY_ROWS:
            raise CarverBlocked("S27 v2 phase 2 runtime minimum history is locked")
        if self.row_status == PHASE2_RUNTIME_HISTORY_READY_STATUS and (
            not self.level_compatibility_passed
            or self.observed_daily_continuous_rows < self.required_minimum_daily_continuous_rows
        ):
            raise CarverBlocked("S27 v2 phase 2 runtime ready row must bind sufficient upstream inputs")
        if self.row_status == PHASE2_RUNTIME_HISTORY_FAIL_STATUS:
            if self.reason_code == "FAIL_CLOSED_MINIMUM_64_DAILY_STRICT_PRIOR_ROWS_NOT_AVAILABLE" and (
                self.observed_daily_continuous_rows >= self.required_minimum_daily_continuous_rows
            ):
                raise CarverBlocked("S27 v2 phase 2 runtime history-count fail row must bind insufficient history")
            if self.reason_code == "FAIL_CLOSED_UPSTREAM_LEVEL_COMPATIBILITY_NOT_PROVED" and (
                self.level_compatibility_passed
            ):
                raise CarverBlocked("S27 v2 phase 2 runtime level fail row must bind failed level compatibility")
        if self.runtime_numeric_values_emitted is not False:
            raise CarverBlocked("S27 v2 phase 2 must not emit runtime numeric values")
        require_hash("S27 v2 phase 2 runtime row hash", self.row_hash)
        if self.row_hash != canonical_sha256(_phase2_runtime_row_hash_payload(self)):
            raise CarverBlocked("S27 v2 phase 2 runtime row hash must be content-bound")


@dataclass(frozen=True)
class Phase2ExecutableReplayBundle:
    status: str
    authorization_label: str
    phase1_fail_closed_bundle: FailClosedExecutableReplayBundle
    level_compatibility_row: Phase2LevelCompatibilityLedgerRow
    runtime_history_row: Phase2RuntimeHistoryLedgerRow
    phase2_unresolved_gate_labels: tuple[str, ...]
    forecast_rows_emitted: bool
    order_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    phase2_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS

    def validate(self) -> None:
        require_text("S27 v2 phase 2 bundle status", self.status)
        if self.status != S27_V2_EXECUTABLE_REPLAY_PHASE2_STATUS:
            raise CarverBlocked("S27 v2 phase 2 bundle status is not locked")
        require_text("S27 v2 phase 2 authorization label", self.authorization_label)
        if self.authorization_label != S27_V2_EXECUTABLE_REPLAY_PHASE2_AUTHORIZATION:
            raise CarverBlocked("S27 v2 phase 2 authorization label is not locked")
        self.phase1_fail_closed_bundle.validate()
        self.level_compatibility_row.validate()
        self.runtime_history_row.validate()
        _validate_phase2_rows_against_phase1_provenance(
            self.level_compatibility_row,
            self.runtime_history_row,
            self.phase1_fail_closed_bundle.provenance_ledger,
        )
        if self.runtime_history_row.level_compatibility_row_hash != self.level_compatibility_row.row_hash:
            raise CarverBlocked("S27 v2 phase 2 runtime row must bind active level row")
        if self.runtime_history_row.level_compatibility_passed != (
            self.level_compatibility_row.row_status == PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS
        ):
            raise CarverBlocked("S27 v2 phase 2 runtime row must bind active level status")
        require_tuple("S27 v2 phase 2 unresolved gate labels", self.phase2_unresolved_gate_labels)
        for gate_label in self.phase2_unresolved_gate_labels:
            require_text("S27 v2 phase 2 unresolved gate label", gate_label)
            if gate_label not in REQUIRED_UNRESOLVED_GATE_LABELS:
                raise CarverBlocked("S27 v2 phase 2 unresolved gate label must be source-locked")
        if self.phase2_unresolved_gate_labels != _expected_phase2_unresolved_gate_labels(
            self.level_compatibility_row,
            self.runtime_history_row,
        ):
            raise CarverBlocked("S27 v2 phase 2 unresolved gates must match runtime rows exactly")
        if any(
            flag is not False
            for flag in (
                self.forecast_rows_emitted,
                self.order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 phase 2 must not emit forecast/order/fill/cost/PnL/result/evidence")
        if self.non_authorizations != S27_V2_EXECUTABLE_PHASE1_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 phase 2 bundle must preserve non-authorizations")
        require_hash("S27 v2 phase 2 bundle hash", self.phase2_bundle_hash)
        if self.phase2_bundle_hash != canonical_sha256(_phase2_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 phase 2 bundle hash must be content-bound")


def build_fail_closed_executable_replay_ledgers(
    inputs: LocalParserFileReplaySlice1Inputs,
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
    *,
    input_pack_path: str,
    construction_output_path: str,
    construction_run_manifest_bytes: bytes,
) -> FailClosedExecutableReplayBundle:
    inputs.validate()
    construction_artifacts.validate()
    expected_artifacts = build_local_parser_file_replay_completion(inputs)
    if construction_artifacts != expected_artifacts:
        raise CarverBlocked("S27 v2 executable replay must match active controlled construction artifacts")

    provenance_ledger = _build_provenance_ledger(
        inputs,
        construction_artifacts,
        construction_run_manifest_sha256=_validated_construction_run_manifest_sha256(
            construction_run_manifest_bytes,
            inputs,
            construction_artifacts,
            input_pack_path=input_pack_path,
            construction_output_path=construction_output_path,
        ),
    )
    validation_ledger = _build_validation_ledger(construction_artifacts)
    bundle = FailClosedExecutableReplayBundle(
        status=S27_V2_EXECUTABLE_REPLAY_TRUSTED_BUNDLE_STATUS,
        authorization_label=S27_V2_EXECUTABLE_REPLAY_PHASE1_AUTHORIZATION,
        input_pack_path=input_pack_path,
        construction_output_path=construction_output_path,
        provenance_ledger=provenance_ledger,
        validation_ledger=validation_ledger,
        trusted_bundle_contract_hash=construction_artifacts.trusted_bundle_contract.trusted_bundle_contract_hash,
        fail_closed_bundle_hash="0" * 64,
    )
    bundle = FailClosedExecutableReplayBundle(
        **{
            **bundle.__dict__,
            "fail_closed_bundle_hash": canonical_sha256(_bundle_hash_payload(bundle)),
        }
    )
    bundle.validate()
    return bundle


def build_phase2_executable_replay_ledgers(
    inputs: LocalParserFileReplaySlice1Inputs,
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
    *,
    input_pack_path: str,
    construction_output_path: str,
    construction_run_manifest_bytes: bytes,
) -> Phase2ExecutableReplayBundle:
    phase1_bundle = build_fail_closed_executable_replay_ledgers(
        inputs,
        construction_artifacts,
        input_pack_path=input_pack_path,
        construction_output_path=construction_output_path,
        construction_run_manifest_bytes=construction_run_manifest_bytes,
    )
    level_row = _build_phase2_level_compatibility_row(construction_artifacts)
    runtime_row = _build_phase2_runtime_history_row(construction_artifacts, level_row)
    bundle = Phase2ExecutableReplayBundle(
        status=S27_V2_EXECUTABLE_REPLAY_PHASE2_STATUS,
        authorization_label=S27_V2_EXECUTABLE_REPLAY_PHASE2_AUTHORIZATION,
        phase1_fail_closed_bundle=phase1_bundle,
        level_compatibility_row=level_row,
        runtime_history_row=runtime_row,
        phase2_unresolved_gate_labels=_expected_phase2_unresolved_gate_labels(level_row, runtime_row),
        forecast_rows_emitted=False,
        order_rows_emitted=False,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        phase2_bundle_hash="0" * 64,
    )
    bundle = Phase2ExecutableReplayBundle(
        **{
            **bundle.__dict__,
            "phase2_bundle_hash": canonical_sha256(_phase2_bundle_hash_payload(bundle)),
        }
    )
    bundle.validate()
    return bundle


def _build_phase2_level_compatibility_row(
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
) -> Phase2LevelCompatibilityLedgerRow:
    slice3 = construction_artifacts.slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts
    slice2 = slice3.slice2_artifacts
    parsed_by_family = _parsed_file_by_family(slice2.slice1_artifacts.parsed_files)
    daily_continuous = parsed_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"].rows[0]
    daily_current = parsed_by_family["DAILY_CURRENT_CONTRACT_COMPLETED_BAR"].rows[0]
    hourly_decision = parsed_by_family["HOURLY_DECISION_COMPLETED_BAR"].rows[0]
    hourly_fill = parsed_by_family["HOURLY_FILL_COMPLETED_BAR"].rows[0]
    same_level = (
        daily_continuous.close_price
        == daily_current.close_price
        == hourly_decision.close_price
        == hourly_fill.close_price
    )
    row = Phase2LevelCompatibilityLedgerRow(
        ledger_label="DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER",
        row_status=(
            PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS
            if same_level
            else PHASE2_LEVEL_COMPATIBILITY_FAIL_STATUS
        ),
        reason_code=(
            "SAME_LEVEL_COMPATIBLE"
            if same_level
            else "FAIL_CLOSED_UNBRIDGED_DAILY_HOURLY_LEVEL_MISMATCH"
        ),
        source_input_manifest_hash=slice2.source_input_manifest_contract.source_input_manifest_hash,
        level_compatibility_contract_hash=slice3.level_compatibility_contract.level_compatibility_contract_bundle_hash,
        daily_continuous_row_hash=daily_continuous.row_hash,
        daily_current_contract_row_hash=daily_current.row_hash,
        hourly_decision_row_hash=hourly_decision.row_hash,
        hourly_fill_row_hash=hourly_fill.row_hash,
        daily_continuous_close_price=daily_continuous.close_price,
        daily_current_contract_close_price=daily_current.close_price,
        hourly_decision_close_price=hourly_decision.close_price,
        hourly_fill_close_price=hourly_fill.close_price,
        row_hash="0" * 64,
    )
    row = Phase2LevelCompatibilityLedgerRow(
        **{
            **row.__dict__,
            "row_hash": canonical_sha256(_phase2_level_row_hash_payload(row)),
        }
    )
    row.validate()
    return row


def _build_phase2_runtime_history_row(
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
    level_row: Phase2LevelCompatibilityLedgerRow,
) -> Phase2RuntimeHistoryLedgerRow:
    slice3 = construction_artifacts.slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts
    parsed_by_family = _parsed_file_by_family(slice3.slice2_artifacts.slice1_artifacts.parsed_files)
    daily_continuous = parsed_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"]
    hourly_decision = parsed_by_family["HOURLY_DECISION_COMPLETED_BAR"]
    sufficient_history = (
        level_row.row_status == PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS
        and len(daily_continuous.rows) >= PHASE2_RUNTIME_HISTORY_MINIMUM_DAILY_ROWS
    )
    fail_reason = "FAIL_CLOSED_MINIMUM_64_DAILY_STRICT_PRIOR_ROWS_NOT_AVAILABLE"
    if level_row.row_status != PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS and (
        len(daily_continuous.rows) >= PHASE2_RUNTIME_HISTORY_MINIMUM_DAILY_ROWS
    ):
        fail_reason = "FAIL_CLOSED_UPSTREAM_LEVEL_COMPATIBILITY_NOT_PROVED"
    row = Phase2RuntimeHistoryLedgerRow(
        ledger_label="RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM",
        row_status=(
            PHASE2_RUNTIME_HISTORY_READY_STATUS
            if sufficient_history
            else PHASE2_RUNTIME_HISTORY_FAIL_STATUS
        ),
        reason_code=(
            "STRICT_PRIOR_HISTORY_COUNT_SUFFICIENT_RUNTIME_VALUES_NOT_EMITTED_IN_PHASE2"
            if sufficient_history
            else fail_reason
        ),
        source_input_manifest_hash=slice3.slice2_artifacts.source_input_manifest_contract.source_input_manifest_hash,
        runtime_history_contract_hash=slice3.runtime_history_contract.runtime_history_contract_bundle_hash,
        level_compatibility_row_hash=level_row.row_hash,
        level_compatibility_passed=level_row.row_status == PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS,
        daily_continuous_row_hashes=daily_continuous.row_hashes,
        hourly_decision_row_hashes=hourly_decision.row_hashes,
        observed_daily_continuous_rows=len(daily_continuous.rows),
        required_minimum_daily_continuous_rows=PHASE2_RUNTIME_HISTORY_MINIMUM_DAILY_ROWS,
        runtime_numeric_values_emitted=False,
        row_hash="0" * 64,
    )
    row = Phase2RuntimeHistoryLedgerRow(
        **{
            **row.__dict__,
            "row_hash": canonical_sha256(_phase2_runtime_row_hash_payload(row)),
        }
    )
    row.validate()
    return row


def _build_provenance_ledger(
    inputs: LocalParserFileReplaySlice1Inputs,
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
    *,
    construction_run_manifest_sha256: str,
) -> ExecutableReplayProvenanceLedger:
    slice1 = construction_artifacts.slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts
    source_manifest = construction_artifacts.slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    slice3 = construction_artifacts.slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts
    row_family_hashes = tuple(
        (parsed.row_family, parsed.row_hashes)
        for parsed in slice1.parsed_files
    )
    price_row_close_prices = tuple(
        (
            parsed.row_family,
            tuple(row.close_price for row in parsed.rows),
        )
        for parsed in slice1.parsed_files
        if parsed.row_family in (
            "DAILY_CONTINUOUS_COMPLETED_BAR",
            "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
            "HOURLY_DECISION_COMPLETED_BAR",
            "HOURLY_FILL_COMPLETED_BAR",
        )
    )
    ledger = ExecutableReplayProvenanceLedger(
        status=S27_V2_EXECUTABLE_REPLAY_PROVENANCE_STATUS,
        authorization_label=S27_V2_EXECUTABLE_REPLAY_PHASE1_AUTHORIZATION,
        input_directory_declaration_hash=inputs.input_directory.input_directory_declaration_hash,
        raw_file_hash_set_hash=inputs.input_directory.raw_file_hash_set_hash,
        parser_output_contract_hash=slice1.parser_output_contract.parser_output_contract_hash,
        source_row_batch_contract_hash=slice1.source_row_batch_contract.source_row_batch_contract_hash,
        source_input_manifest_hash=source_manifest.source_input_manifest_hash,
        level_compatibility_contract_hash=slice3.level_compatibility_contract.level_compatibility_contract_bundle_hash,
        runtime_history_contract_hash=slice3.runtime_history_contract.runtime_history_contract_bundle_hash,
        construction_contract_hash=construction_artifacts.construction_contract.construction_contract_hash,
        validation_contract_bundle_hash=construction_artifacts.validation_contract.validation_contract_bundle_hash,
        trusted_bundle_contract_hash=construction_artifacts.trusted_bundle_contract.trusted_bundle_contract_hash,
        row_family_hashes=row_family_hashes,
        price_row_close_prices=price_row_close_prices,
        construction_run_manifest_sha256=construction_run_manifest_sha256,
        provenance_ledger_hash="0" * 64,
    )
    ledger = ExecutableReplayProvenanceLedger(
        **{
            **ledger.__dict__,
            "provenance_ledger_hash": canonical_sha256(_provenance_ledger_hash_payload(ledger)),
        }
    )
    ledger.validate()
    return ledger


def _build_validation_ledger(
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
) -> ExecutableReplayValidationLedger:
    upstream = (
        construction_artifacts.construction_contract.construction_contract_hash,
        construction_artifacts.validation_contract.validation_contract_bundle_hash,
        construction_artifacts.trusted_bundle_contract.trusted_bundle_contract_hash,
    )
    gate_rows = tuple(
        _build_gate_row(
            ledger_label=ledger_label,
            blocked_gate_labels=_blocked_gates_by_ledger_label(ledger_label),
            reason_code=_reason_code_by_ledger_label(ledger_label),
            upstream_authority_hashes=upstream,
        )
        for ledger_label in EXECUTABLE_LEDGER_LABELS
    )
    unresolved_gate_labels = _expected_unresolved_gate_labels(gate_rows)
    ledger = ExecutableReplayValidationLedger(
        status=S27_V2_EXECUTABLE_REPLAY_VALIDATION_STATUS,
        authorization_label=S27_V2_EXECUTABLE_REPLAY_PHASE1_AUTHORIZATION,
        gate_rows=gate_rows,
        required_unresolved_gate_labels=unresolved_gate_labels,
        forecast_rows_emitted=False,
        order_rows_emitted=False,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        validation_ledger_hash="0" * 64,
    )
    ledger = ExecutableReplayValidationLedger(
        **{
            **ledger.__dict__,
            "validation_ledger_hash": canonical_sha256(_validation_ledger_hash_payload(ledger)),
        }
    )
    ledger.validate()
    return ledger


def _build_gate_row(
    *,
    ledger_label: str,
    blocked_gate_labels: tuple[str, ...],
    reason_code: str,
    upstream_authority_hashes: tuple[str, ...],
) -> ExecutableReplayGateLedgerRow:
    row = ExecutableReplayGateLedgerRow(
        ledger_label=ledger_label,
        gate_status="FAIL_CLOSED_NO_EXECUTABLE_ROW",
        reason_code=reason_code,
        blocked_gate_labels=blocked_gate_labels,
        upstream_authority_hashes=upstream_authority_hashes,
        executable_row_emitted=False,
        executable_row_hash=_NO_EXECUTABLE_ROW_HASH,
        gate_row_hash="0" * 64,
    )
    row = ExecutableReplayGateLedgerRow(
        **{
            **row.__dict__,
            "gate_row_hash": canonical_sha256(_gate_row_hash_payload(row)),
        }
    )
    row.validate()
    return row


def _validated_construction_run_manifest_sha256(
    construction_run_manifest_bytes: bytes,
    inputs: LocalParserFileReplaySlice1Inputs,
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
    *,
    input_pack_path: str,
    construction_output_path: str,
) -> str:
    if not isinstance(construction_run_manifest_bytes, bytes) or not construction_run_manifest_bytes:
        raise CarverBlocked("S27 v2 construction run manifest bytes are required")
    try:
        manifest = json.loads(construction_run_manifest_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CarverBlocked("S27 v2 construction run manifest must be JSON bytes") from exc
    if not isinstance(manifest, dict):
        raise CarverBlocked("S27 v2 construction run manifest must be an object")
    if tuple(manifest) != REQUIRED_CONSTRUCTION_RUN_MANIFEST_KEYS:
        raise CarverBlocked("S27 v2 construction run manifest keys must match locked schema")
    if manifest.get("artifact") != "S27_V2_CONTROLLED_LOCAL_REPLAY_CONSTRUCTION_RUN_MANIFEST":
        raise CarverBlocked("S27 v2 construction run manifest artifact label is not locked")
    if manifest.get("authorization") != "S27_V2_CONTROLLED_LOCAL_ONLY_REPLAY_CONSTRUCTION_RUN_DECLARED_ZN_INPUT_PACK":
        raise CarverBlocked("S27 v2 construction run manifest authorization is not locked")
    if _normalized_path_text(manifest.get("input_pack")) != _normalized_path_text(input_pack_path):
        raise CarverBlocked("S27 v2 construction run manifest input pack must match executable bundle")
    if _normalized_path_text(manifest.get("output_directory")) != _normalized_path_text(construction_output_path):
        raise CarverBlocked("S27 v2 construction run manifest output directory must match executable bundle")
    expected_hash_by_key = {
        "input_directory_declaration_hash": inputs.input_directory.input_directory_declaration_hash,
        "raw_file_hash_set_hash": inputs.input_directory.raw_file_hash_set_hash,
        "parser_plan_bundle_hash": inputs.parser_plan_bundle.parser_plan_bundle_hash,
        "row_locator_hash": inputs.input_directory.row_locator_hash,
        "source_universe_manifest_hash": inputs.input_directory.source_universe_manifest_hash,
        "construction_contract_hash": construction_artifacts.construction_contract.construction_contract_hash,
        "validation_contract_bundle_hash": construction_artifacts.validation_contract.validation_contract_bundle_hash,
        "trusted_bundle_contract_hash": construction_artifacts.trusted_bundle_contract.trusted_bundle_contract_hash,
    }
    for key, expected_hash in expected_hash_by_key.items():
        observed = manifest.get(key)
        if not isinstance(observed, str) or observed.lower() != expected_hash:
            raise CarverBlocked("S27 v2 construction run manifest must bind active construction artifacts")
    if manifest.get("status") != "LOCAL_REPLAY_CONSTRUCTION_ARTIFACTS_BUILT_AND_VALIDATED_NOT_EVIDENCE":
        raise CarverBlocked("S27 v2 construction run manifest status is not the audited construction status")
    if tuple(manifest.get("non_authorizations", ())) != CONTROLLED_CONSTRUCTION_RUN_NON_AUTHORIZATIONS:
        raise CarverBlocked("S27 v2 construction run manifest non-authorizations must match locked boundary")
    if manifest.get("boundaries") != {
        "cost_rows_are_policy_hashes_only": True,
        "no_pnl_rows_or_result_scores_written": True,
        "pnl_contract_is_inert_contract_scaffold": True,
    }:
        raise CarverBlocked("S27 v2 construction run manifest boundaries must match locked non-result claims")
    if manifest.get("verification") != {
        "build_local_parser_file_replay_completion": "PASS",
        "completion_validate": "PASS",
        "inputs_validate": "PASS",
    }:
        raise CarverBlocked("S27 v2 construction run manifest verification must match controlled construction PASS")
    _validate_manifest_row_family_summary(manifest.get("row_family_summary"), construction_artifacts)
    _validate_manifest_artifact_files(
        manifest.get("artifact_files"),
        construction_output_path=construction_output_path,
        construction_artifacts=construction_artifacts,
    )
    return sha256(construction_run_manifest_bytes).hexdigest()


def _validate_manifest_row_family_summary(
    row_family_summary: object,
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
) -> None:
    if not isinstance(row_family_summary, list) or not row_family_summary:
        raise CarverBlocked("S27 v2 construction run manifest row-family summary is required")
    slice1 = construction_artifacts.slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts
    if len(row_family_summary) != len(slice1.parsed_files):
        raise CarverBlocked("S27 v2 construction run manifest row-family summary must cover parsed files")
    for observed, parsed in zip(row_family_summary, slice1.parsed_files, strict=True):
        if not isinstance(observed, dict):
            raise CarverBlocked("S27 v2 construction run manifest row-family entry must be an object")
        normalized_observed = _normalized_manifest_row_family_entry(observed)
        expected = {
            "file_sha256": parsed.file_sha256,
            "parsed_output_batch_hash": parsed.parsed_output_batch_hash,
            "row_count": len(parsed.rows),
            "row_family": parsed.row_family,
            "row_hashes": list(parsed.row_hashes),
        }
        if normalized_observed != expected:
            raise CarverBlocked("S27 v2 construction run manifest row-family summary must bind parsed rows")


def _normalized_manifest_row_family_entry(observed: dict[str, object]) -> dict[str, object]:
    if tuple(observed) != ("file_sha256", "parsed_output_batch_hash", "row_count", "row_family", "row_hashes"):
        raise CarverBlocked("S27 v2 construction run manifest row-family entry keys must be locked")
    file_sha = observed["file_sha256"]
    parsed_hash = observed["parsed_output_batch_hash"]
    row_hashes = observed["row_hashes"]
    require_text("S27 v2 construction run manifest row-family file hash", file_sha)
    require_text("S27 v2 construction run manifest row-family parsed hash", parsed_hash)
    file_sha = file_sha.lower()
    parsed_hash = parsed_hash.lower()
    require_hash("S27 v2 construction run manifest row-family file hash", file_sha)
    require_hash("S27 v2 construction run manifest row-family parsed hash", parsed_hash)
    if not isinstance(row_hashes, list) or not row_hashes:
        raise CarverBlocked("S27 v2 construction run manifest row-family row hashes are required")
    normalized_row_hashes: list[str] = []
    for row_hash in row_hashes:
        require_text("S27 v2 construction run manifest row-family row hash", row_hash)
        row_hash = row_hash.lower()
        require_hash("S27 v2 construction run manifest row-family row hash", row_hash)
        normalized_row_hashes.append(row_hash)
    return {
        "file_sha256": file_sha,
        "parsed_output_batch_hash": parsed_hash,
        "row_count": observed["row_count"],
        "row_family": observed["row_family"],
        "row_hashes": normalized_row_hashes,
    }


def _validate_manifest_artifact_files(
    artifact_files: object,
    *,
    construction_output_path: str,
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
) -> None:
    if not isinstance(artifact_files, list) or not artifact_files:
        raise CarverBlocked("S27 v2 construction run manifest artifact files are required")
    if len(artifact_files) != len(REQUIRED_CONSTRUCTION_RUN_ARTIFACT_FILES):
        raise CarverBlocked("S27 v2 construction run manifest artifact files must cover locked output set")
    output_root = Path(construction_output_path).expanduser().resolve()
    seen_files: list[str] = []
    for artifact_file in artifact_files:
        if not isinstance(artifact_file, dict) or tuple(artifact_file) != ("file", "sha256"):
            raise CarverBlocked("S27 v2 construction run manifest artifact-file entries must be locked")
        file_name = artifact_file["file"]
        file_hash = artifact_file["sha256"]
        require_text("S27 v2 construction run manifest artifact file", file_name)
        if file_name in seen_files:
            raise CarverBlocked("S27 v2 construction run manifest artifact files must be unique")
        seen_files.append(file_name)
        require_text("S27 v2 construction run manifest artifact file hash", file_hash)
        file_hash = file_hash.lower()
        require_hash("S27 v2 construction run manifest artifact file hash", file_hash)
        artifact_path = (output_root / file_name).resolve()
        try:
            artifact_path.relative_to(output_root)
        except ValueError as exc:
            raise CarverBlocked("S27 v2 construction run manifest artifact path must stay inside output") from exc
        if not artifact_path.is_file():
            raise CarverBlocked("S27 v2 construction run manifest artifact file must exist")
        artifact_bytes = artifact_path.read_bytes()
        if sha256(artifact_bytes).hexdigest() != file_hash:
            raise CarverBlocked("S27 v2 construction run manifest artifact file hash must match bytes")
        _validate_manifest_artifact_json_binding(file_name, artifact_bytes, construction_artifacts)
    if tuple(seen_files) != REQUIRED_CONSTRUCTION_RUN_ARTIFACT_FILES:
        raise CarverBlocked("S27 v2 construction run manifest artifact files must match locked output set")


def _validate_manifest_artifact_json_binding(
    file_name: str,
    artifact_bytes: bytes,
    construction_artifacts: LocalParserFileReplayCompletionArtifacts,
) -> None:
    try:
        artifact_json = json.loads(artifact_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CarverBlocked("S27 v2 construction artifact file must be JSON") from exc
    if not isinstance(artifact_json, dict):
        raise CarverBlocked("S27 v2 construction artifact file must be a JSON object")
    slice1 = construction_artifacts.slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.slice1_artifacts
    source_manifest = construction_artifacts.slice7_artifacts.slice6_artifacts.slice5_artifacts.slice4_artifacts.slice3_artifacts.slice2_artifacts.source_input_manifest_contract
    expected_hash_by_file_and_key = {
        ("artifacts/07_parser_output_contract.json", "parser_output_contract_hash"): (
            slice1.parser_output_contract.parser_output_contract_hash
        ),
        ("artifacts/08_source_row_batch_contract.json", "source_row_batch_contract_hash"): (
            slice1.source_row_batch_contract.source_row_batch_contract_hash
        ),
        ("artifacts/11_source_input_manifest_contract.json", "source_input_manifest_hash"): (
            source_manifest.source_input_manifest_hash
        ),
        ("artifacts/30_construction_contract.json", "construction_contract_hash"): (
            construction_artifacts.construction_contract.construction_contract_hash
        ),
        ("artifacts/31_validation_input_contract.json", "validation_input_contract_hash"): (
            construction_artifacts.validation_input_contract.validation_input_contract_hash
        ),
        ("artifacts/32_validation_contract.json", "validation_contract_bundle_hash"): (
            construction_artifacts.validation_contract.validation_contract_bundle_hash
        ),
        ("artifacts/33_trusted_bundle_contract.json", "trusted_bundle_contract_hash"): (
            construction_artifacts.trusted_bundle_contract.trusted_bundle_contract_hash
        ),
    }
    for (expected_file, expected_key), expected_hash in expected_hash_by_file_and_key.items():
        if file_name == expected_file:
            observed_hash = artifact_json.get(expected_key)
            if not isinstance(observed_hash, str) or observed_hash.lower() != expected_hash:
                raise CarverBlocked("S27 v2 construction artifact JSON must bind active artifact hash")


def _normalized_path_text(value: object) -> str:
    require_text("S27 v2 construction run manifest path", value)
    return Path(value).expanduser().as_posix()


def _expected_unresolved_gate_labels(
    gate_rows: tuple[ExecutableReplayGateLedgerRow, ...],
) -> tuple[str, ...]:
    return tuple(
        gate
        for gate in REQUIRED_UNRESOLVED_GATE_LABELS
        if any(gate in row.blocked_gate_labels for row in gate_rows)
    )


def _expected_phase2_unresolved_gate_labels(
    level_row: Phase2LevelCompatibilityLedgerRow,
    runtime_row: Phase2RuntimeHistoryLedgerRow,
) -> tuple[str, ...]:
    unresolved: list[str] = []
    if level_row.row_status != PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS:
        unresolved.append(BLOCKED_LEVEL_COMPATIBILITY)
    if runtime_row.row_status != PHASE2_RUNTIME_HISTORY_READY_STATUS:
        unresolved.extend([BLOCKED_RUNTIME_HISTORY, BLOCKED_SIGMA])
    unresolved.extend([BLOCKED_TICK, BLOCKED_COST_SCHEMA])
    return tuple(
        gate
        for gate in REQUIRED_UNRESOLVED_GATE_LABELS
        if gate in unresolved
    )


def _validate_phase2_rows_against_phase1_provenance(
    level_row: Phase2LevelCompatibilityLedgerRow,
    runtime_row: Phase2RuntimeHistoryLedgerRow,
    provenance: ExecutableReplayProvenanceLedger,
) -> None:
    if level_row.source_input_manifest_hash != provenance.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 phase 2 level row must bind active phase 1 source manifest")
    if runtime_row.source_input_manifest_hash != provenance.source_input_manifest_hash:
        raise CarverBlocked("S27 v2 phase 2 runtime row must bind active phase 1 source manifest")
    if level_row.level_compatibility_contract_hash != provenance.level_compatibility_contract_hash:
        raise CarverBlocked("S27 v2 phase 2 level row must bind active level compatibility contract")
    if runtime_row.runtime_history_contract_hash != provenance.runtime_history_contract_hash:
        raise CarverBlocked("S27 v2 phase 2 runtime row must bind active runtime history contract")
    row_hashes_by_family = _row_hashes_by_family(provenance.row_family_hashes)
    row_close_price_by_family = _row_close_price_by_family(
        provenance.row_family_hashes,
        provenance.price_row_close_prices,
    )
    if level_row.daily_continuous_row_hash not in row_hashes_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 phase 2 level row must bind active daily continuous row")
    if level_row.daily_current_contract_row_hash not in row_hashes_by_family["DAILY_CURRENT_CONTRACT_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 phase 2 level row must bind active daily current-contract row")
    if level_row.hourly_decision_row_hash not in row_hashes_by_family["HOURLY_DECISION_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 phase 2 level row must bind active hourly decision row")
    if level_row.hourly_fill_row_hash not in row_hashes_by_family["HOURLY_FILL_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 phase 2 level row must bind active hourly fill row")
    if runtime_row.daily_continuous_row_hashes != row_hashes_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 phase 2 runtime row must bind active daily history row tuple")
    if runtime_row.hourly_decision_row_hashes != row_hashes_by_family["HOURLY_DECISION_COMPLETED_BAR"]:
        raise CarverBlocked("S27 v2 phase 2 runtime row must bind active hourly decision row tuple")
    daily_continuous_close = row_close_price_by_family["DAILY_CONTINUOUS_COMPLETED_BAR"][
        level_row.daily_continuous_row_hash
    ]
    daily_current_close = row_close_price_by_family["DAILY_CURRENT_CONTRACT_COMPLETED_BAR"][
        level_row.daily_current_contract_row_hash
    ]
    hourly_decision_close = row_close_price_by_family["HOURLY_DECISION_COMPLETED_BAR"][
        level_row.hourly_decision_row_hash
    ]
    hourly_fill_close = row_close_price_by_family["HOURLY_FILL_COMPLETED_BAR"][
        level_row.hourly_fill_row_hash
    ]
    if level_row.daily_continuous_close_price != daily_continuous_close:
        raise CarverBlocked("S27 v2 phase 2 level row price must bind active daily continuous row")
    if level_row.daily_current_contract_close_price != daily_current_close:
        raise CarverBlocked("S27 v2 phase 2 level row price must bind active daily current-contract row")
    if level_row.hourly_decision_close_price != hourly_decision_close:
        raise CarverBlocked("S27 v2 phase 2 level row price must bind active hourly decision row")
    if level_row.hourly_fill_close_price != hourly_fill_close:
        raise CarverBlocked("S27 v2 phase 2 level row price must bind active hourly fill row")
    active_same_level = len(
        {
            daily_continuous_close,
            daily_current_close,
            hourly_decision_close,
            hourly_fill_close,
        }
    ) == 1
    if active_same_level != (level_row.row_status == PHASE2_LEVEL_COMPATIBILITY_PASS_STATUS):
        raise CarverBlocked("S27 v2 phase 2 level status must bind active parsed close prices")


def _row_hashes_by_family(
    row_family_hashes: tuple[tuple[str, tuple[str, ...]], ...],
) -> dict[str, tuple[str, ...]]:
    by_family = {
        family: row_hashes
        for family, row_hashes in row_family_hashes
    }
    required = (
        "DAILY_CONTINUOUS_COMPLETED_BAR",
        "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
        "HOURLY_DECISION_COMPLETED_BAR",
        "HOURLY_FILL_COMPLETED_BAR",
        "SESSION_CALENDAR",
        "ROLL_CALENDAR",
        "COST_PARAMETER",
    )
    if tuple(by_family) != required:
        raise CarverBlocked("S27 v2 phase 2 provenance row families must match locked local pack")
    return by_family


def _price_row_close_prices_by_family(
    price_row_close_prices: tuple[tuple[str, tuple[float, ...]], ...],
) -> dict[str, tuple[float, ...]]:
    by_family = {
        family: close_prices
        for family, close_prices in price_row_close_prices
    }
    required = (
        "DAILY_CONTINUOUS_COMPLETED_BAR",
        "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
        "HOURLY_DECISION_COMPLETED_BAR",
        "HOURLY_FILL_COMPLETED_BAR",
    )
    if tuple(by_family) != required:
        raise CarverBlocked("S27 v2 phase 2 provenance close-price families must match locked local pack")
    return by_family


def _row_close_price_by_family(
    row_family_hashes: tuple[tuple[str, tuple[str, ...]], ...],
    price_row_close_prices: tuple[tuple[str, tuple[float, ...]], ...],
) -> dict[str, dict[str, float]]:
    row_hashes_by_family = _row_hashes_by_family(row_family_hashes)
    close_prices_by_family = _price_row_close_prices_by_family(price_row_close_prices)
    return {
        family: dict(zip(row_hashes_by_family[family], close_prices_by_family[family], strict=True))
        for family in close_prices_by_family
    }


def _blocked_gates_by_ledger_label(ledger_label: str) -> tuple[str, ...]:
    if ledger_label == "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER":
        return (BLOCKED_LEVEL_COMPATIBILITY,)
    if ledger_label == "RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM":
        return (BLOCKED_RUNTIME_HISTORY, BLOCKED_SIGMA)
    if ledger_label in ("FORECAST_REPLAY_LEDGER", "DESIRED_POSITION_LEDGER"):
        return (BLOCKED_RUNTIME_HISTORY, BLOCKED_SIGMA, BLOCKED_TICK)
    if ledger_label in (
        "LIMIT_ORDER_LEDGER",
        "MARKET_ORDER_LEDGER",
        "WORKING_ORDER_TRANSITION_LEDGER",
        "FILL_LEDGER",
    ):
        return (BLOCKED_RUNTIME_HISTORY, BLOCKED_TICK)
    if ledger_label in ("COMMISSION_LEDGER", "SPREAD_COST_LEDGER"):
        return (BLOCKED_COST_SCHEMA,)
    if ledger_label == "PNL_LEDGER":
        return (BLOCKED_RUNTIME_HISTORY, BLOCKED_COST_SCHEMA)
    raise CarverBlocked("S27 v2 executable ledger label is not locked")


def _reason_code_by_ledger_label(ledger_label: str) -> str:
    return {
        "DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER": (
            "FAIL_CLOSED_COMPATIBILITY_BRIDGE_POLICY_NOT_EXECUTABLE_FROM_DECLARED_ROWS"
        ),
        "RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM": (
            "FAIL_CLOSED_INSUFFICIENT_STRICT_PRIOR_HISTORY_FOR_EWMA_EWMAC_SIGMA_VQM"
        ),
        "FORECAST_REPLAY_LEDGER": "FAIL_CLOSED_UPSTREAM_RUNTIME_HISTORY_LEDGER_NOT_EMITTED",
        "DESIRED_POSITION_LEDGER": "FAIL_CLOSED_UPSTREAM_FORECAST_LEDGER_NOT_EMITTED",
        "LIMIT_ORDER_LEDGER": "FAIL_CLOSED_UPSTREAM_POSITION_AND_TICK_POLICY_NOT_EXECUTABLE",
        "MARKET_ORDER_LEDGER": "FAIL_CLOSED_UPSTREAM_POSITION_AND_MARKET_ORDER_POLICY_NOT_EXECUTABLE",
        "WORKING_ORDER_TRANSITION_LEDGER": "FAIL_CLOSED_WORKING_LIMIT_LIFECYCLE_NOT_EXECUTABLE",
        "FILL_LEDGER": "FAIL_CLOSED_UPSTREAM_ORDER_TRANSITION_LEDGER_NOT_EMITTED",
        "COMMISSION_LEDGER": "FAIL_CLOSED_NUMERIC_COMMISSION_EVIDENCE_NOT_BOUND",
        "SPREAD_COST_LEDGER": "FAIL_CLOSED_NUMERIC_SPREAD_MULTIPLIER_CURRENCY_EVIDENCE_NOT_BOUND",
        "PNL_LEDGER": "FAIL_CLOSED_UPSTREAM_FILL_COST_AND_RUNTIME_LEDGERS_NOT_EMITTED",
    }[ledger_label]


def _gate_row_hash_payload(row: ExecutableReplayGateLedgerRow) -> dict[str, object]:
    return {
        "artifact": "S27_V2_EXECUTABLE_REPLAY_GATE_LEDGER_ROW",
        "blocked_gate_labels": row.blocked_gate_labels,
        "executable_row_emitted": row.executable_row_emitted,
        "executable_row_hash": row.executable_row_hash,
        "gate_status": row.gate_status,
        "ledger_label": row.ledger_label,
        "reason_code": row.reason_code,
        "upstream_authority_hashes": row.upstream_authority_hashes,
    }


def _provenance_ledger_hash_payload(ledger: ExecutableReplayProvenanceLedger) -> dict[str, object]:
    return {
        "artifact": "S27_V2_EXECUTABLE_REPLAY_PROVENANCE_LEDGER",
        "authorization_label": ledger.authorization_label,
        "construction_contract_hash": ledger.construction_contract_hash,
        "construction_run_manifest_sha256": ledger.construction_run_manifest_sha256,
        "input_directory_declaration_hash": ledger.input_directory_declaration_hash,
        "level_compatibility_contract_hash": ledger.level_compatibility_contract_hash,
        "non_authorizations": ledger.non_authorizations,
        "parser_output_contract_hash": ledger.parser_output_contract_hash,
        "price_row_close_prices": ledger.price_row_close_prices,
        "raw_file_hash_set_hash": ledger.raw_file_hash_set_hash,
        "row_family_hashes": ledger.row_family_hashes,
        "source_input_manifest_hash": ledger.source_input_manifest_hash,
        "source_row_batch_contract_hash": ledger.source_row_batch_contract_hash,
        "status": ledger.status,
        "runtime_history_contract_hash": ledger.runtime_history_contract_hash,
        "trusted_bundle_contract_hash": ledger.trusted_bundle_contract_hash,
        "validation_contract_bundle_hash": ledger.validation_contract_bundle_hash,
    }


def _validation_ledger_hash_payload(ledger: ExecutableReplayValidationLedger) -> dict[str, object]:
    return {
        "artifact": "S27_V2_EXECUTABLE_REPLAY_VALIDATION_LEDGER",
        "authorization_label": ledger.authorization_label,
        "cost_rows_emitted": ledger.cost_rows_emitted,
        "fill_rows_emitted": ledger.fill_rows_emitted,
        "forecast_rows_emitted": ledger.forecast_rows_emitted,
        "gate_row_hashes": tuple(row.gate_row_hash for row in ledger.gate_rows),
        "non_authorizations": ledger.non_authorizations,
        "order_rows_emitted": ledger.order_rows_emitted,
        "pnl_rows_emitted": ledger.pnl_rows_emitted,
        "required_unresolved_gate_labels": ledger.required_unresolved_gate_labels,
        "result_scored_run_emitted": ledger.result_scored_run_emitted,
        "source_faithful_evidence_claimed": ledger.source_faithful_evidence_claimed,
        "status": ledger.status,
    }


def _bundle_hash_payload(bundle: FailClosedExecutableReplayBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_FAIL_CLOSED_EXECUTABLE_REPLAY_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "construction_output_path": bundle.construction_output_path,
        "input_pack_path": bundle.input_pack_path,
        "non_authorizations": bundle.non_authorizations,
        "provenance_ledger_hash": bundle.provenance_ledger.provenance_ledger_hash,
        "status": bundle.status,
        "trusted_bundle_contract_hash": bundle.trusted_bundle_contract_hash,
        "validation_ledger_hash": bundle.validation_ledger.validation_ledger_hash,
    }


def _phase2_level_row_hash_payload(row: Phase2LevelCompatibilityLedgerRow) -> dict[str, object]:
    return {
        "artifact": "S27_V2_PHASE2_LEVEL_COMPATIBILITY_EXECUTABLE_LEDGER_ROW",
        "daily_continuous_close_price": row.daily_continuous_close_price,
        "daily_continuous_row_hash": row.daily_continuous_row_hash,
        "daily_current_contract_close_price": row.daily_current_contract_close_price,
        "daily_current_contract_row_hash": row.daily_current_contract_row_hash,
        "hourly_decision_close_price": row.hourly_decision_close_price,
        "hourly_decision_row_hash": row.hourly_decision_row_hash,
        "hourly_fill_close_price": row.hourly_fill_close_price,
        "hourly_fill_row_hash": row.hourly_fill_row_hash,
        "ledger_label": row.ledger_label,
        "level_compatibility_contract_hash": row.level_compatibility_contract_hash,
        "reason_code": row.reason_code,
        "row_status": row.row_status,
        "source_input_manifest_hash": row.source_input_manifest_hash,
    }


def _phase2_runtime_row_hash_payload(row: Phase2RuntimeHistoryLedgerRow) -> dict[str, object]:
    return {
        "artifact": "S27_V2_PHASE2_RUNTIME_HISTORY_EXECUTABLE_LEDGER_ROW",
        "daily_continuous_row_hashes": row.daily_continuous_row_hashes,
        "hourly_decision_row_hashes": row.hourly_decision_row_hashes,
        "ledger_label": row.ledger_label,
        "level_compatibility_passed": row.level_compatibility_passed,
        "level_compatibility_row_hash": row.level_compatibility_row_hash,
        "observed_daily_continuous_rows": row.observed_daily_continuous_rows,
        "reason_code": row.reason_code,
        "required_minimum_daily_continuous_rows": row.required_minimum_daily_continuous_rows,
        "runtime_history_contract_hash": row.runtime_history_contract_hash,
        "runtime_numeric_values_emitted": row.runtime_numeric_values_emitted,
        "row_status": row.row_status,
        "source_input_manifest_hash": row.source_input_manifest_hash,
    }


def _phase2_bundle_hash_payload(bundle: Phase2ExecutableReplayBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_PHASE2_EXECUTABLE_REPLAY_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "fill_rows_emitted": bundle.fill_rows_emitted,
        "forecast_rows_emitted": bundle.forecast_rows_emitted,
        "level_compatibility_row_hash": bundle.level_compatibility_row.row_hash,
        "non_authorizations": bundle.non_authorizations,
        "order_rows_emitted": bundle.order_rows_emitted,
        "phase1_fail_closed_bundle_hash": bundle.phase1_fail_closed_bundle.fail_closed_bundle_hash,
        "phase2_unresolved_gate_labels": bundle.phase2_unresolved_gate_labels,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "runtime_history_row_hash": bundle.runtime_history_row.row_hash,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
    }


def _parsed_file_by_family(construction_parsed_files: tuple[object, ...]) -> dict[str, object]:
    by_family = {
        parsed.row_family: parsed
        for parsed in construction_parsed_files
    }
    required = (
        "DAILY_CONTINUOUS_COMPLETED_BAR",
        "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
        "HOURLY_DECISION_COMPLETED_BAR",
        "HOURLY_FILL_COMPLETED_BAR",
        "SESSION_CALENDAR",
        "ROLL_CALENDAR",
        "COST_PARAMETER",
    )
    if tuple(by_family) != required:
        raise CarverBlocked("S27 v2 phase 2 parsed families must match locked local pack")
    return by_family

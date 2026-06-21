from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest
from .level_compatibility_contract import REQUIRED_LEVEL_COMPATIBILITY_PROOFS
from .parser_output_contract import ParserOutputBatchSetContract
from .source_input_manifest_contract import (
    REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS,
    REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD,
    SourceInputManifestContractBundle,
)
from .source_input_selection_contract import (
    REQUIRED_SOURCE_INPUT_ROLES,
    SourceRowSelectionExternalAuthorityHandle,
)
from .source_row_batch_contract import SourceRowBatchSetContract
from .trust_root import ReplayTrustRoot
from .validation import (
    require_expected_hash,
    require_hash,
    require_hash_map,
    require_hash_map_matches_active_authority,
    require_matching_dependency_hashes,
    require_non_empty_tuple,
    require_text,
)


S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_ONLY_STATUS = (
    "S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_ONLY"
)
PLANNED_LEVEL_COMPATIBILITY_INPUT_STATUS = "PLANNED_LEVEL_COMPATIBILITY_INPUT_ONLY"

REQUIRED_LEVEL_COMPATIBILITY_INPUTS = (
    "LEVEL_COMPAT_DAILY_CONTINUOUS_INPUT",
    "LEVEL_COMPAT_DAILY_CURRENT_CONTRACT_INPUT",
    "LEVEL_COMPAT_PREVIOUS_CURRENT_CLOSE_INPUT",
    "LEVEL_COMPAT_HOURLY_DECISION_INPUT",
    "LEVEL_COMPAT_HOURLY_FILL_INPUT",
)

REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT = {
    "LEVEL_COMPAT_DAILY_CONTINUOUS_INPUT": "DAILY_CONTINUOUS_ROW_HASH",
    "LEVEL_COMPAT_DAILY_CURRENT_CONTRACT_INPUT": "DAILY_CURRENT_CONTRACT_ROW_HASH",
    "LEVEL_COMPAT_PREVIOUS_CURRENT_CLOSE_INPUT": "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_HASH",
    "LEVEL_COMPAT_HOURLY_DECISION_INPUT": "HOURLY_DECISION_ROW_HASH",
    "LEVEL_COMPAT_HOURLY_FILL_INPUT": "HOURLY_FILL_ROW_HASH",
}

REQUIRED_LEVEL_COMPATIBILITY_INPUTS_BY_PROOF = {
    "SIGMA_BRIDGE_USES_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE": (
        "LEVEL_COMPAT_DAILY_CURRENT_CONTRACT_INPUT",
        "LEVEL_COMPAT_PREVIOUS_CURRENT_CLOSE_INPUT",
    ),
    "HOURLY_CURRENT_MATCHES_DAILY_CURRENT_CONTRACT_LEVEL": (
        "LEVEL_COMPAT_DAILY_CURRENT_CONTRACT_INPUT",
        "LEVEL_COMPAT_HOURLY_DECISION_INPUT",
        "LEVEL_COMPAT_HOURLY_FILL_INPUT",
    ),
    "CONTINUOUS_TO_CURRENT_CONTRACT_LEVEL_BRIDGE": (
        "LEVEL_COMPAT_DAILY_CONTINUOUS_INPUT",
        "LEVEL_COMPAT_DAILY_CURRENT_CONTRACT_INPUT",
        "LEVEL_COMPAT_PREVIOUS_CURRENT_CLOSE_INPUT",
    ),
    "BRIDGED_DAILY_CONTINUOUS_EQUILIBRIUM": (
        "LEVEL_COMPAT_DAILY_CONTINUOUS_INPUT",
        "LEVEL_COMPAT_DAILY_CURRENT_CONTRACT_INPUT",
    ),
}


@dataclass(frozen=True)
class LevelCompatibilityInputFieldContract:
    input_label: str
    input_status: str
    source_input_manifest_field: str
    source_input_role: str
    source_input_manifest_field_contract_hash: str
    selected_row_hash: str
    selected_row_locator_hash: str
    level_compatibility_input_policy_hash: str
    price_level_space_policy_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    no_future_rows_proof_hash: str
    input_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 level compatibility input label", self.input_label)
        if self.input_label not in REQUIRED_LEVEL_COMPATIBILITY_INPUTS:
            raise CarverBlocked("S27 v2 level compatibility input label is not locked")
        require_text("S27 v2 level compatibility input status", self.input_status)
        if self.input_status != PLANNED_LEVEL_COMPATIBILITY_INPUT_STATUS:
            raise CarverBlocked("S27 v2 level compatibility input must remain planned-only")
        require_text(
            "S27 v2 level compatibility source input manifest field",
            self.source_input_manifest_field,
        )
        if self.source_input_manifest_field not in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS:
            raise CarverBlocked("S27 v2 level compatibility input manifest field is not locked")
        if (
            self.source_input_manifest_field
            != REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[self.input_label]
        ):
            raise CarverBlocked(
                "S27 v2 level compatibility input must use the locked source-input manifest field"
            )
        require_text("S27 v2 level compatibility source input role", self.source_input_role)
        if self.source_input_role not in REQUIRED_SOURCE_INPUT_ROLES:
            raise CarverBlocked("S27 v2 level compatibility source input role is not locked")
        if (
            self.source_input_role
            != REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[self.source_input_manifest_field]
        ):
            raise CarverBlocked("S27 v2 level compatibility input must use the locked source-input role")
        require_hash(
            "S27 v2 level compatibility source-input manifest field contract hash",
            self.source_input_manifest_field_contract_hash,
        )
        require_hash("S27 v2 level compatibility selected row hash", self.selected_row_hash)
        require_hash("S27 v2 level compatibility selected row locator hash", self.selected_row_locator_hash)
        require_hash(
            "S27 v2 level compatibility input policy hash",
            self.level_compatibility_input_policy_hash,
        )
        require_hash(
            "S27 v2 level compatibility price-level-space policy hash",
            self.price_level_space_policy_hash,
        )
        require_hash("S27 v2 level compatibility completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 level compatibility strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 level compatibility no-future-rows proof hash", self.no_future_rows_proof_hash)
        require_hash("S27 v2 level compatibility input field contract hash", self.input_field_contract_hash)


@dataclass(frozen=True)
class LevelCompatibilityProofInputBindingContract:
    proof_label: str
    required_input_labels: tuple[str, ...]
    required_input_field_contract_hashes: tuple[str, ...]
    proof_input_binding_policy_hash: str
    proof_input_binding_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 level compatibility proof-input binding label", self.proof_label)
        if self.proof_label not in REQUIRED_LEVEL_COMPATIBILITY_PROOFS:
            raise CarverBlocked("S27 v2 level compatibility proof-input binding label is not locked")
        require_non_empty_tuple(
            "S27 v2 level compatibility proof required input labels",
            self.required_input_labels,
        )
        if self.required_input_labels != REQUIRED_LEVEL_COMPATIBILITY_INPUTS_BY_PROOF[self.proof_label]:
            raise CarverBlocked("S27 v2 level compatibility proof inputs must match locked input tuple")
        require_non_empty_tuple(
            "S27 v2 level compatibility proof required input field contract hashes",
            self.required_input_field_contract_hashes,
        )
        if len(self.required_input_field_contract_hashes) != len(self.required_input_labels):
            raise CarverBlocked(
                "S27 v2 level compatibility proof input hashes must match required input labels"
            )
        for input_hash in self.required_input_field_contract_hashes:
            require_hash("S27 v2 level compatibility proof input field contract hash", input_hash)
        require_hash(
            "S27 v2 level compatibility proof-input binding policy hash",
            self.proof_input_binding_policy_hash,
        )
        require_hash(
            "S27 v2 level compatibility proof-input binding contract hash",
            self.proof_input_binding_contract_hash,
        )


@dataclass(frozen=True)
class LevelCompatibilityInputContractBundle:
    status: str
    source_input_manifest_contract_hash: str
    source_input_manifest_hash: str
    source_input_selection_contract_hash: str
    level_compatibility_policy_hash: str
    source_input_manifest_contract_bundle: SourceInputManifestContractBundle
    input_field_contracts: tuple[LevelCompatibilityInputFieldContract, ...]
    expected_source_contract_hash_by_input_label: dict[str, str]
    expected_selected_row_hash_by_input_label: dict[str, str]
    expected_selected_row_locator_hash_by_input_label: dict[str, str]
    proof_input_binding_contracts: tuple[LevelCompatibilityProofInputBindingContract, ...]
    level_compatibility_input_set_hash: str
    level_compatibility_input_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 level compatibility input requires active trust authority"
        )

    def validate_against_active_trust_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        self._validate_contract_only_shape(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )

    def _validate_contract_only_shape(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        require_text("S27 v2 level compatibility input contract status", self.status)
        if self.status != S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 level compatibility input contract must remain contract-only")
        if tuple(REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT) != REQUIRED_LEVEL_COMPATIBILITY_INPUTS:
            raise CarverBlocked("S27 v2 level compatibility input map must cover the locked input tuple")
        if tuple(REQUIRED_LEVEL_COMPATIBILITY_INPUTS_BY_PROOF) != REQUIRED_LEVEL_COMPATIBILITY_PROOFS:
            raise CarverBlocked("S27 v2 level compatibility proof-input map must cover the locked proof tuple")
        require_hash(
            "S27 v2 level compatibility source-input manifest contract hash",
            self.source_input_manifest_contract_hash,
        )
        require_hash("S27 v2 level compatibility source-input manifest hash", self.source_input_manifest_hash)
        require_hash(
            "S27 v2 level compatibility source-input selection contract hash",
            self.source_input_selection_contract_hash,
        )
        require_hash("S27 v2 level compatibility policy hash", self.level_compatibility_policy_hash)
        self._validate_source_input_manifest_bundle_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )
        require_hash_map(
            "S27 v2 level compatibility expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 level compatibility expected source contract hash map",
            self.expected_source_contract_hash_by_input_label,
            self._active_source_contract_hash_by_input_label(),
            REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 level compatibility selected-row hash map",
            self.expected_selected_row_hash_by_input_label,
            self._active_selected_row_hash_by_input_label(),
            REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 level compatibility selected-row-locator hash map",
            self.expected_selected_row_locator_hash_by_input_label,
            self._active_selected_row_locator_hash_by_input_label(),
            REQUIRED_LEVEL_COMPATIBILITY_INPUTS,
        )
        require_non_empty_tuple(
            "S27 v2 level compatibility input field contracts",
            self.input_field_contracts,
        )
        seen_inputs: set[str] = set()
        input_contract_hash_by_label: dict[str, str] = {}
        for contract in self.input_field_contracts:
            contract.validate()
            if contract.input_label in seen_inputs:
                raise CarverBlocked("S27 v2 level compatibility input labels must be unique")
            seen_inputs.add(contract.input_label)
            require_expected_hash(
                "S27 v2 level compatibility input source contract hash",
                contract.input_label,
                contract.source_input_manifest_field_contract_hash,
                self.expected_source_contract_hash_by_input_label,
            )
            require_expected_hash(
                "S27 v2 level compatibility selected row hash",
                contract.input_label,
                contract.selected_row_hash,
                self.expected_selected_row_hash_by_input_label,
            )
            require_expected_hash(
                "S27 v2 level compatibility selected row locator hash",
                contract.input_label,
                contract.selected_row_locator_hash,
                self.expected_selected_row_locator_hash_by_input_label,
            )
            input_contract_hash_by_label[contract.input_label] = contract.input_field_contract_hash
        if (
            tuple(contract.input_label for contract in self.input_field_contracts)
            != REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        ):
            raise CarverBlocked("S27 v2 level compatibility inputs must match the locked input tuple")
        require_non_empty_tuple(
            "S27 v2 level compatibility proof-input binding contracts",
            self.proof_input_binding_contracts,
        )
        seen_proofs: set[str] = set()
        for binding in self.proof_input_binding_contracts:
            binding.validate()
            if binding.proof_label in seen_proofs:
                raise CarverBlocked("S27 v2 level compatibility proof-input bindings must be unique")
            seen_proofs.add(binding.proof_label)
            require_matching_dependency_hashes(
                "S27 v2 level compatibility proof-input binding",
                binding.required_input_labels,
                binding.required_input_field_contract_hashes,
                input_contract_hash_by_label,
            )
        if (
            tuple(binding.proof_label for binding in self.proof_input_binding_contracts)
            != REQUIRED_LEVEL_COMPATIBILITY_PROOFS
        ):
            raise CarverBlocked(
                "S27 v2 level compatibility proof-input bindings must match the locked proof tuple"
            )
        require_hash(
            "S27 v2 level compatibility input set hash",
            self.level_compatibility_input_set_hash,
        )
        require_hash(
            "S27 v2 level compatibility input contract hash",
            self.level_compatibility_input_contract_hash,
        )
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 level compatibility input contract must preserve non-authorizations")

    def _active_source_contract_hash_by_input_label(self) -> dict[str, str]:
        manifest_field_contract_hash_by_field = self._manifest_field_contract_hash_by_field()
        return {
            input_label: manifest_field_contract_hash_by_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ]
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        }

    def _active_selected_row_hash_by_input_label(self) -> dict[str, str]:
        return {
            input_label: self.source_input_manifest_contract_bundle.expected_selected_row_hash_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ]
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        }

    def _active_selected_row_locator_hash_by_input_label(self) -> dict[str, str]:
        return {
            input_label: self.source_input_manifest_contract_bundle.expected_selected_row_locator_hash_by_manifest_field[
                REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT[input_label]
            ]
            for input_label in REQUIRED_LEVEL_COMPATIBILITY_INPUTS
        }

    def _validate_source_input_manifest_bundle_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        self.source_input_manifest_contract_bundle.validate_against_active_trust_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )
        if (
            self.source_input_manifest_contract_bundle.source_input_manifest_contract_hash
            != self.source_input_manifest_contract_hash
        ):
            raise CarverBlocked("S27 v2 level compatibility must bind cited source-input manifest contract")
        if self.source_input_manifest_contract_bundle.source_input_manifest_hash != self.source_input_manifest_hash:
            raise CarverBlocked("S27 v2 level compatibility must bind cited source-input manifest hash")
        if (
            self.source_input_manifest_contract_bundle.source_input_selection_contract_hash
            != self.source_input_selection_contract_hash
        ):
            raise CarverBlocked("S27 v2 level compatibility must bind cited source-input selection")

    def _manifest_field_contract_hash_by_field(self) -> dict[str, str]:
        manifest_field_contract_hash_by_field = {
            contract.manifest_field: contract.manifest_field_contract_hash
            for contract in self.source_input_manifest_contract_bundle.manifest_field_contracts
        }
        if tuple(manifest_field_contract_hash_by_field) != REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS:
            raise CarverBlocked("S27 v2 level compatibility manifest field contracts must match locked fields")
        return manifest_field_contract_hash_by_field

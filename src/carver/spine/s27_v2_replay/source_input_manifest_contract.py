from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .evidence_manifest import EvidenceManifest, require_evidence_manifest_matches_trust_root
from .parser_output_contract import ParserOutputBatchSetContract
from .source_input_selection_contract import (
    REQUIRED_SOURCE_INPUT_ROLES,
    SourceInputRoleSelectionContract,
    SourceInputSelectionContractBundle,
    SourceRowSelectionExternalAuthorityHandle,
)
from .source_row_batch_contract import SourceRowBatchSetContract
from .trust_root import ReplayTrustRoot
from .validation import (
    require_expected_hash,
    require_hash,
    require_hash_map,
    require_hash_map_matches_active_authority,
    require_non_empty_tuple,
    require_text,
)


S27_V2_SOURCE_INPUT_MANIFEST_CONTRACT_ONLY_STATUS = "S27_V2_SOURCE_INPUT_MANIFEST_CONTRACT_ONLY"
PLANNED_SOURCE_INPUT_MANIFEST_FIELD_STATUS = "PLANNED_SOURCE_INPUT_MANIFEST_FIELD_ONLY"

REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS = (
    "DAILY_CONTINUOUS_ROW_HASH",
    "DAILY_CURRENT_CONTRACT_ROW_HASH",
    "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_HASH",
    "HOURLY_DECISION_ROW_HASH",
    "HOURLY_FILL_ROW_HASH",
    "SESSION_CALENDAR_CONTEXT_HASH",
    "ROLL_CALENDAR_CONTEXT_HASH",
    "COST_PARAMETER_CONTEXT_HASH",
)

REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD = {
    "DAILY_CONTINUOUS_ROW_HASH": "DAILY_CONTINUOUS_EQUILIBRIUM_ROW",
    "DAILY_CURRENT_CONTRACT_ROW_HASH": "DAILY_CURRENT_CONTRACT_PRICE_ROW",
    "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_HASH": "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_ROW",
    "HOURLY_DECISION_ROW_HASH": "HOURLY_DECISION_CURRENT_PRICE_ROW",
    "HOURLY_FILL_ROW_HASH": "HOURLY_FILL_CURRENT_PRICE_ROW",
    "SESSION_CALENDAR_CONTEXT_HASH": "SESSION_CALENDAR_CONTEXT_ROW",
    "ROLL_CALENDAR_CONTEXT_HASH": "ROLL_CALENDAR_CONTEXT_ROW",
    "COST_PARAMETER_CONTEXT_HASH": "COST_PARAMETER_CONTEXT_ROW",
}


@dataclass(frozen=True)
class SourceInputManifestFieldContract:
    manifest_field: str
    field_status: str
    source_input_role: str
    source_input_role_contract_hash: str
    selected_row_hash: str
    selected_row_locator_hash: str
    manifest_field_policy_hash: str
    canonical_field_serialization_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    no_future_rows_proof_hash: str
    manifest_field_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 source input manifest field", self.manifest_field)
        if self.manifest_field not in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS:
            raise CarverBlocked("S27 v2 source input manifest field is not locked")
        require_text("S27 v2 source input manifest field status", self.field_status)
        if self.field_status != PLANNED_SOURCE_INPUT_MANIFEST_FIELD_STATUS:
            raise CarverBlocked("S27 v2 source input manifest field must remain planned-only")
        require_text("S27 v2 source input manifest source role", self.source_input_role)
        if self.source_input_role not in REQUIRED_SOURCE_INPUT_ROLES:
            raise CarverBlocked("S27 v2 source input manifest source role is not locked")
        if self.source_input_role != REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[self.manifest_field]:
            raise CarverBlocked("S27 v2 source input manifest field must use the locked input role")
        require_hash(
            "S27 v2 source input manifest source role contract hash",
            self.source_input_role_contract_hash,
        )
        require_hash("S27 v2 source input manifest selected row hash", self.selected_row_hash)
        require_hash("S27 v2 source input manifest selected row locator hash", self.selected_row_locator_hash)
        require_hash("S27 v2 source input manifest field policy hash", self.manifest_field_policy_hash)
        require_hash(
            "S27 v2 source input manifest canonical field serialization hash",
            self.canonical_field_serialization_hash,
        )
        require_hash("S27 v2 source input manifest completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 source input manifest strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 source input manifest no-future-rows proof hash", self.no_future_rows_proof_hash)
        require_hash("S27 v2 source input manifest field contract hash", self.manifest_field_contract_hash)


@dataclass(frozen=True)
class SourceInputManifestContractBundle:
    status: str
    source_input_selection_contract_hash: str
    source_input_selection_set_hash: str
    source_universe_contract_bundle_hash: str
    row_locator_contract_bundle_hash: str
    canonical_serialization_policy_hash: str
    source_input_selection_contract_bundle: SourceInputSelectionContractBundle
    manifest_field_contracts: tuple[SourceInputManifestFieldContract, ...]
    source_input_role_selection_contracts: tuple[SourceInputRoleSelectionContract, ...]
    active_source_input_role_contract_hash_by_input_role: dict[str, str]
    active_selected_row_hash_by_input_role: dict[str, str]
    active_selected_row_locator_hash_by_input_role: dict[str, str]
    expected_source_input_role_contract_hash_by_manifest_field: dict[str, str]
    expected_selected_row_hash_by_manifest_field: dict[str, str]
    expected_selected_row_locator_hash_by_manifest_field: dict[str, str]
    source_input_manifest_schema_hash: str
    source_input_manifest_hash: str
    source_input_manifest_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 source input manifest requires active trust authority"
        )

    def validate_against_active_trust_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        self._validate_active_trust_authority(
            replay_trust_root,
            evidence_manifest,
            source_row_selection_external_authority,
        )
        self._validate_contract_only_shape(
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )

    def _validate_contract_only_shape(
        self,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        require_text("S27 v2 source input manifest contract status", self.status)
        if self.status != S27_V2_SOURCE_INPUT_MANIFEST_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 source input manifest contract must remain contract-only")
        if tuple(REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD) != REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS:
            raise CarverBlocked("S27 v2 source input manifest role map must cover the locked field tuple")
        require_hash(
            "S27 v2 source input manifest source input selection contract hash",
            self.source_input_selection_contract_hash,
        )
        require_hash(
            "S27 v2 source input manifest source input selection-set hash",
            self.source_input_selection_set_hash,
        )
        require_hash(
            "S27 v2 source input manifest source universe contract bundle hash",
            self.source_universe_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source input manifest row locator contract bundle hash",
            self.row_locator_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source input manifest canonical serialization policy hash",
            self.canonical_serialization_policy_hash,
        )
        self._validate_source_input_selection_bundle_authority(
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )
        require_hash_map(
            "S27 v2 source input manifest active source-role contract map",
            self.active_source_input_role_contract_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map(
            "S27 v2 source input manifest active selected-row map",
            self.active_selected_row_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map(
            "S27 v2 source input manifest active selected-row-locator map",
            self.active_selected_row_locator_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        self._validate_source_input_role_selection_authority()
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest source-role authority",
            self.expected_source_input_role_contract_hash_by_manifest_field,
            self._active_source_input_role_contract_hash_by_manifest_field(),
            REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest selected-row authority",
            self.expected_selected_row_hash_by_manifest_field,
            self._active_selected_row_hash_by_manifest_field(),
            REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest selected-row-locator authority",
            self.expected_selected_row_locator_hash_by_manifest_field,
            self._active_selected_row_locator_hash_by_manifest_field(),
            REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS,
        )
        require_non_empty_tuple("S27 v2 source input manifest field contracts", self.manifest_field_contracts)
        seen_fields: set[str] = set()
        for contract in self.manifest_field_contracts:
            contract.validate()
            if contract.manifest_field in seen_fields:
                raise CarverBlocked("S27 v2 source input manifest fields must be unique")
            seen_fields.add(contract.manifest_field)
            require_expected_hash(
                "S27 v2 source input manifest role contract hash",
                contract.manifest_field,
                contract.source_input_role_contract_hash,
                self.expected_source_input_role_contract_hash_by_manifest_field,
            )
            require_expected_hash(
                "S27 v2 source input manifest selected row hash",
                contract.manifest_field,
                contract.selected_row_hash,
                self.expected_selected_row_hash_by_manifest_field,
            )
            require_expected_hash(
                "S27 v2 source input manifest selected row locator hash",
                contract.manifest_field,
                contract.selected_row_locator_hash,
                self.expected_selected_row_locator_hash_by_manifest_field,
            )
        if (
            tuple(contract.manifest_field for contract in self.manifest_field_contracts)
            != REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
        ):
            raise CarverBlocked("S27 v2 source input manifest fields must match the locked field tuple")
        require_hash("S27 v2 source input manifest schema hash", self.source_input_manifest_schema_hash)
        require_hash("S27 v2 source input manifest hash", self.source_input_manifest_hash)
        require_hash("S27 v2 source input manifest contract hash", self.source_input_manifest_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 source input manifest contract must preserve non-authorizations")

    def _validate_source_input_role_selection_authority(self) -> None:
        role_contract_by_role = self._source_input_role_selection_contract_by_role()
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest active source-role contract authority",
            self.active_source_input_role_contract_hash_by_input_role,
            {
                input_role: role_contract_by_role[input_role].source_input_role_contract_hash
                for input_role in REQUIRED_SOURCE_INPUT_ROLES
            },
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest active selected-row authority",
            self.active_selected_row_hash_by_input_role,
            {
                input_role: role_contract_by_role[input_role].selected_row_hash
                for input_role in REQUIRED_SOURCE_INPUT_ROLES
            },
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest active selected-row-locator authority",
            self.active_selected_row_locator_hash_by_input_role,
            {
                input_role: role_contract_by_role[input_role].selected_row_locator_hash
                for input_role in REQUIRED_SOURCE_INPUT_ROLES
            },
            REQUIRED_SOURCE_INPUT_ROLES,
        )

    def _validate_active_trust_authority(
        self,
        replay_trust_root: ReplayTrustRoot,
        evidence_manifest: EvidenceManifest,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
    ) -> None:
        require_evidence_manifest_matches_trust_root(replay_trust_root, evidence_manifest)
        source_row_selection_external_authority.validate()
        if source_row_selection_external_authority.replay_trust_root_hash != replay_trust_root.replay_trust_root_hash:
            raise CarverBlocked("S27 v2 source input manifest must bind external replay trust root")
        if (
            source_row_selection_external_authority.active_evidence_manifest_hash
            != replay_trust_root.active_evidence_manifest_hash
        ):
            raise CarverBlocked("S27 v2 source input manifest must bind trust-root active evidence manifest")
        if (
            source_row_selection_external_authority.active_evidence_manifest_hash
            != evidence_manifest.active_evidence_manifest_hash
        ):
            raise CarverBlocked("S27 v2 source input manifest must bind active evidence manifest")
        if (
            source_row_selection_external_authority.source_row_selection_authority_hash
            != replay_trust_root.source_row_selection_authority_hash
        ):
            raise CarverBlocked("S27 v2 source input manifest must bind trust-root row-selection authority")
        expected_manifest_hashes = (
            (
                "SOURCE_ROW_SELECTION_AUTHORITY",
                source_row_selection_external_authority.source_row_selection_authority_hash,
            ),
            (
                "SOURCE_ROW_BATCH_CONTRACT",
                source_row_selection_external_authority.source_row_batch_contract_hash,
            ),
            (
                "SOURCE_ROW_BATCH_SET",
                source_row_selection_external_authority.source_row_batch_set_hash,
            ),
            (
                "SOURCE_ROW_LOCATOR",
                source_row_selection_external_authority.row_locator_contract_bundle_hash,
            ),
            (
                "SOURCE_INPUT_UNIVERSE_MANIFEST",
                source_row_selection_external_authority.source_universe_contract_bundle_hash,
            ),
        )
        for artifact_type, expected_hash in expected_manifest_hashes:
            if evidence_manifest.active_hash_by_type(artifact_type) != expected_hash:
                raise CarverBlocked("S27 v2 source input manifest external authority must match evidence manifest")

    def _validate_source_input_selection_bundle_authority(
        self,
        source_row_selection_external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        self.source_input_selection_contract_bundle.validate_against_external_authority(
            source_row_selection_external_authority,
            source_row_batch_contract,
            parser_output_contract,
        )
        if (
            self.source_input_selection_contract_bundle.source_input_selection_contract_hash
            != self.source_input_selection_contract_hash
        ):
            raise CarverBlocked("S27 v2 source input manifest must bind cited selection contract")
        if (
            self.source_input_selection_contract_bundle.source_input_selection_set_hash
            != self.source_input_selection_set_hash
        ):
            raise CarverBlocked("S27 v2 source input manifest must bind cited selection set")
        if (
            self.source_input_selection_contract_bundle.source_universe_contract_bundle_hash
            != self.source_universe_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 source input manifest must bind cited source universe")
        if (
            self.source_input_selection_contract_bundle.row_locator_contract_bundle_hash
            != self.row_locator_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 source input manifest must bind cited row locator")
        if (
            self.source_input_selection_contract_bundle.role_selection_contracts
            != self.source_input_role_selection_contracts
        ):
            raise CarverBlocked("S27 v2 source input manifest role contracts must come from cited selection")
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest active source-role map from cited selection",
            self.active_source_input_role_contract_hash_by_input_role,
            {
                contract.input_role: contract.source_input_role_contract_hash
                for contract in self.source_input_selection_contract_bundle.role_selection_contracts
            },
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest active selected-row map from cited selection",
            self.active_selected_row_hash_by_input_role,
            self.source_input_selection_contract_bundle.expected_selected_row_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input manifest active selected-row-locator map from cited selection",
            self.active_selected_row_locator_hash_by_input_role,
            self.source_input_selection_contract_bundle.expected_selected_row_locator_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )

    def _source_input_role_selection_contract_by_role(self) -> dict[str, SourceInputRoleSelectionContract]:
        require_non_empty_tuple(
            "S27 v2 source input manifest source-input role selection contracts",
            self.source_input_role_selection_contracts,
        )
        role_contract_by_role: dict[str, SourceInputRoleSelectionContract] = {}
        for contract in self.source_input_role_selection_contracts:
            contract.validate()
            if contract.input_role in role_contract_by_role:
                raise CarverBlocked("S27 v2 source input manifest source-input role contracts must be unique")
            role_contract_by_role[contract.input_role] = contract
        if tuple(role_contract_by_role) != REQUIRED_SOURCE_INPUT_ROLES:
            raise CarverBlocked("S27 v2 source input manifest source-input role contracts must match locked roles")
        return role_contract_by_role

    def _active_source_input_role_contract_hash_by_manifest_field(self) -> dict[str, str]:
        return {
            manifest_field: self.active_source_input_role_contract_hash_by_input_role[
                REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[manifest_field]
            ]
            for manifest_field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
        }

    def _active_selected_row_hash_by_manifest_field(self) -> dict[str, str]:
        return {
            manifest_field: self.active_selected_row_hash_by_input_role[
                REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[manifest_field]
            ]
            for manifest_field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
        }

    def _active_selected_row_locator_hash_by_manifest_field(self) -> dict[str, str]:
        return {
            manifest_field: self.active_selected_row_locator_hash_by_input_role[
                REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD[manifest_field]
            ]
            for manifest_field in REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
        }

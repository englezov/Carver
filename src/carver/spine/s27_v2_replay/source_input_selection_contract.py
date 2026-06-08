from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .parser_output_contract import ParserOutputBatchSetContract
from .source_row_batch_contract import (
    REQUIRED_SOURCE_ROW_BATCH_FAMILIES,
    SourceRowBatchFamilyContract,
    SourceRowBatchSetContract,
)
from .validation import (
    require_expected_hash,
    require_hash,
    require_hash_map,
    require_hash_map_matches_active_authority,
    require_non_empty_tuple,
    require_text,
)


S27_V2_SOURCE_INPUT_SELECTION_CONTRACT_ONLY_STATUS = "S27_V2_SOURCE_INPUT_SELECTION_CONTRACT_ONLY"
PLANNED_SOURCE_INPUT_ROLE_STATUS = "PLANNED_SOURCE_INPUT_ROLE_ONLY"
PLANNED_SOURCE_ROW_SELECTION_AUTHORITY_STATUS = "PLANNED_SOURCE_ROW_SELECTION_AUTHORITY_ONLY"
PLANNED_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_STATUS = (
    "PLANNED_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_ONLY"
)

REQUIRED_SOURCE_INPUT_ROLES = (
    "DAILY_CONTINUOUS_EQUILIBRIUM_ROW",
    "DAILY_CURRENT_CONTRACT_PRICE_ROW",
    "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_ROW",
    "HOURLY_DECISION_CURRENT_PRICE_ROW",
    "HOURLY_FILL_CURRENT_PRICE_ROW",
    "SESSION_CALENDAR_CONTEXT_ROW",
    "ROLL_CALENDAR_CONTEXT_ROW",
    "COST_PARAMETER_CONTEXT_ROW",
)

REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE = {
    "DAILY_CONTINUOUS_EQUILIBRIUM_ROW": "DAILY_CONTINUOUS_COMPLETED_BAR",
    "DAILY_CURRENT_CONTRACT_PRICE_ROW": "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
    "PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE_ROW": "DAILY_CURRENT_CONTRACT_COMPLETED_BAR",
    "HOURLY_DECISION_CURRENT_PRICE_ROW": "HOURLY_DECISION_COMPLETED_BAR",
    "HOURLY_FILL_CURRENT_PRICE_ROW": "HOURLY_FILL_COMPLETED_BAR",
    "SESSION_CALENDAR_CONTEXT_ROW": "SESSION_CALENDAR",
    "ROLL_CALENDAR_CONTEXT_ROW": "ROLL_CALENDAR",
    "COST_PARAMETER_CONTEXT_ROW": "COST_PARAMETER",
}


def _ordered_hash_map_payload(hash_by_label: dict[str, str], required_labels: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    require_hash_map("S27 v2 source row selection authority payload map", hash_by_label, required_labels)
    return tuple((label, hash_by_label[label]) for label in required_labels)


def _canonical_sha256(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True)
class SourceRowSelectionExternalAuthorityHandle:
    authority_status: str
    replay_trust_root_hash: str
    active_evidence_manifest_hash: str
    source_row_batch_contract_hash: str
    source_row_batch_set_hash: str
    source_universe_contract_bundle_hash: str
    row_locator_contract_bundle_hash: str
    source_row_selection_authority_hash: str
    selected_row_membership_proof_set_hash: str
    selected_row_locator_membership_proof_set_hash: str
    authority_handle_policy_hash: str
    authority_handle_hash: str

    def validate(self) -> None:
        require_text("S27 v2 source row selection external authority status", self.authority_status)
        if self.authority_status != PLANNED_SOURCE_ROW_SELECTION_EXTERNAL_AUTHORITY_STATUS:
            raise CarverBlocked("S27 v2 source row selection authority must be externally anchored")
        require_hash(
            "S27 v2 source row selection external replay trust-root hash",
            self.replay_trust_root_hash,
        )
        require_hash(
            "S27 v2 source row selection external active evidence-manifest hash",
            self.active_evidence_manifest_hash,
        )
        require_hash(
            "S27 v2 source row selection external source-row-batch contract hash",
            self.source_row_batch_contract_hash,
        )
        require_hash(
            "S27 v2 source row selection external source-row-batch set hash",
            self.source_row_batch_set_hash,
        )
        require_hash(
            "S27 v2 source row selection external source-universe contract bundle hash",
            self.source_universe_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source row selection external row-locator contract bundle hash",
            self.row_locator_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source row selection external authority hash",
            self.source_row_selection_authority_hash,
        )
        require_hash(
            "S27 v2 source row selection external selected-row membership proof-set hash",
            self.selected_row_membership_proof_set_hash,
        )
        require_hash(
            "S27 v2 source row selection external selected-row-locator membership proof-set hash",
            self.selected_row_locator_membership_proof_set_hash,
        )
        require_hash(
            "S27 v2 source row selection external authority-handle policy hash",
            self.authority_handle_policy_hash,
        )
        require_hash(
            "S27 v2 source row selection external authority-handle hash",
            self.authority_handle_hash,
        )


@dataclass(frozen=True)
class SourceRowSelectionAuthorityContract:
    authority_status: str
    source_row_batch_contract_hash: str
    source_row_batch_set_hash: str
    source_universe_contract_bundle_hash: str
    row_locator_contract_bundle_hash: str
    selected_row_membership_proof_set_hash: str
    selected_row_locator_membership_proof_set_hash: str
    selected_row_hash_by_input_role: dict[str, str]
    selected_row_locator_hash_by_input_role: dict[str, str]
    selected_row_membership_proof_hash_by_input_role: dict[str, str]
    selected_row_locator_membership_proof_hash_by_input_role: dict[str, str]
    source_row_selection_authority_policy_hash: str
    source_row_selection_authority_hash: str

    def validate(self) -> None:
        require_text("S27 v2 source row selection authority status", self.authority_status)
        if self.authority_status != PLANNED_SOURCE_ROW_SELECTION_AUTHORITY_STATUS:
            raise CarverBlocked("S27 v2 source row selection authority must remain planned-only")
        require_hash(
            "S27 v2 source row selection authority source-row-batch contract hash",
            self.source_row_batch_contract_hash,
        )
        require_hash(
            "S27 v2 source row selection authority source-row-batch set hash",
            self.source_row_batch_set_hash,
        )
        require_hash(
            "S27 v2 source row selection authority source-universe contract bundle hash",
            self.source_universe_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source row selection authority row-locator contract bundle hash",
            self.row_locator_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source row selection authority selected-row membership proof-set hash",
            self.selected_row_membership_proof_set_hash,
        )
        require_hash(
            "S27 v2 source row selection authority selected-row-locator membership proof-set hash",
            self.selected_row_locator_membership_proof_set_hash,
        )
        require_hash_map(
            "S27 v2 source row selection authority selected-row map",
            self.selected_row_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map(
            "S27 v2 source row selection authority selected-row-locator map",
            self.selected_row_locator_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map(
            "S27 v2 source row selection authority selected-row membership proof map",
            self.selected_row_membership_proof_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map(
            "S27 v2 source row selection authority selected-row-locator membership proof map",
            self.selected_row_locator_membership_proof_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash(
            "S27 v2 source row selection authority policy hash",
            self.source_row_selection_authority_policy_hash,
        )
        require_hash(
            "S27 v2 source row selection authority hash",
            self.source_row_selection_authority_hash,
        )
        self._validate_content_bound_hashes()

    def _validate_content_bound_hashes(self) -> None:
        selected_row_membership_proof_set_hash = _canonical_sha256(
            {
                "artifact": "S27_V2_SOURCE_ROW_SELECTION_SELECTED_ROW_MEMBERSHIP_PROOF_SET",
                "authority_status": self.authority_status,
                "proof_hash_by_input_role": _ordered_hash_map_payload(
                    self.selected_row_membership_proof_hash_by_input_role,
                    REQUIRED_SOURCE_INPUT_ROLES,
                ),
                "source_row_batch_contract_hash": self.source_row_batch_contract_hash,
                "source_row_batch_set_hash": self.source_row_batch_set_hash,
                "source_universe_contract_bundle_hash": self.source_universe_contract_bundle_hash,
            }
        )
        if selected_row_membership_proof_set_hash != self.selected_row_membership_proof_set_hash:
            raise CarverBlocked("S27 v2 source row selection selected-row proof set must be content-bound")

        selected_row_locator_membership_proof_set_hash = _canonical_sha256(
            {
                "artifact": "S27_V2_SOURCE_ROW_SELECTION_SELECTED_ROW_LOCATOR_MEMBERSHIP_PROOF_SET",
                "authority_status": self.authority_status,
                "proof_hash_by_input_role": _ordered_hash_map_payload(
                    self.selected_row_locator_membership_proof_hash_by_input_role,
                    REQUIRED_SOURCE_INPUT_ROLES,
                ),
                "row_locator_contract_bundle_hash": self.row_locator_contract_bundle_hash,
                "source_row_batch_contract_hash": self.source_row_batch_contract_hash,
                "source_row_batch_set_hash": self.source_row_batch_set_hash,
                "source_universe_contract_bundle_hash": self.source_universe_contract_bundle_hash,
            }
        )
        if selected_row_locator_membership_proof_set_hash != self.selected_row_locator_membership_proof_set_hash:
            raise CarverBlocked("S27 v2 source row selection selected-row-locator proof set must be content-bound")

        source_row_selection_authority_hash = _canonical_sha256(
            {
                "artifact": "S27_V2_SOURCE_ROW_SELECTION_AUTHORITY",
                "authority_status": self.authority_status,
                "row_locator_contract_bundle_hash": self.row_locator_contract_bundle_hash,
                "selected_row_hash_by_input_role": _ordered_hash_map_payload(
                    self.selected_row_hash_by_input_role,
                    REQUIRED_SOURCE_INPUT_ROLES,
                ),
                "selected_row_locator_hash_by_input_role": _ordered_hash_map_payload(
                    self.selected_row_locator_hash_by_input_role,
                    REQUIRED_SOURCE_INPUT_ROLES,
                ),
                "selected_row_locator_membership_proof_hash_by_input_role": _ordered_hash_map_payload(
                    self.selected_row_locator_membership_proof_hash_by_input_role,
                    REQUIRED_SOURCE_INPUT_ROLES,
                ),
                "selected_row_locator_membership_proof_set_hash": self.selected_row_locator_membership_proof_set_hash,
                "selected_row_membership_proof_hash_by_input_role": _ordered_hash_map_payload(
                    self.selected_row_membership_proof_hash_by_input_role,
                    REQUIRED_SOURCE_INPUT_ROLES,
                ),
                "selected_row_membership_proof_set_hash": self.selected_row_membership_proof_set_hash,
                "source_row_batch_contract_hash": self.source_row_batch_contract_hash,
                "source_row_batch_set_hash": self.source_row_batch_set_hash,
                "source_row_selection_authority_policy_hash": self.source_row_selection_authority_policy_hash,
                "source_universe_contract_bundle_hash": self.source_universe_contract_bundle_hash,
            }
        )
        if source_row_selection_authority_hash != self.source_row_selection_authority_hash:
            raise CarverBlocked("S27 v2 source row selection authority hash must be content-bound")


@dataclass(frozen=True)
class SourceInputRoleSelectionContract:
    input_role: str
    role_status: str
    source_row_family: str
    source_row_batch_family_contract_hash: str
    source_row_batch_hash: str
    row_selector_policy_hash: str
    row_locator_policy_hash: str
    selected_row_locator_hash: str
    selected_row_hash: str
    selected_row_membership_proof_hash: str
    selected_row_locator_membership_proof_hash: str
    selected_row_timestamp_policy_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    no_future_rows_proof_hash: str
    source_input_role_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 source input role", self.input_role)
        if self.input_role not in REQUIRED_SOURCE_INPUT_ROLES:
            raise CarverBlocked("S27 v2 source input role is not locked")
        require_text("S27 v2 source input role status", self.role_status)
        if self.role_status != PLANNED_SOURCE_INPUT_ROLE_STATUS:
            raise CarverBlocked("S27 v2 source input role must remain planned-only")
        require_text("S27 v2 source input source row family", self.source_row_family)
        if self.source_row_family not in REQUIRED_SOURCE_ROW_BATCH_FAMILIES:
            raise CarverBlocked("S27 v2 source input source row family is not locked")
        if self.source_row_family != REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[self.input_role]:
            raise CarverBlocked("S27 v2 source input role must use the locked source row family")
        require_hash(
            "S27 v2 source input source row batch family contract hash",
            self.source_row_batch_family_contract_hash,
        )
        require_hash("S27 v2 source input source row batch hash", self.source_row_batch_hash)
        require_hash("S27 v2 source input row selector policy hash", self.row_selector_policy_hash)
        require_hash("S27 v2 source input row locator policy hash", self.row_locator_policy_hash)
        require_hash("S27 v2 source input selected row locator hash", self.selected_row_locator_hash)
        require_hash("S27 v2 source input selected row hash", self.selected_row_hash)
        require_hash(
            "S27 v2 source input selected row membership proof hash",
            self.selected_row_membership_proof_hash,
        )
        require_hash(
            "S27 v2 source input selected row-locator membership proof hash",
            self.selected_row_locator_membership_proof_hash,
        )
        require_hash(
            "S27 v2 source input selected row timestamp policy hash",
            self.selected_row_timestamp_policy_hash,
        )
        require_hash("S27 v2 source input completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 source input strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 source input no-future-rows proof hash", self.no_future_rows_proof_hash)
        require_hash("S27 v2 source input role contract hash", self.source_input_role_contract_hash)


@dataclass(frozen=True)
class SourceInputSelectionContractBundle:
    status: str
    source_row_batch_contract_hash: str
    source_row_batch_set_hash: str
    source_universe_contract_bundle_hash: str
    row_locator_contract_bundle_hash: str
    canonical_serialization_policy_hash: str
    source_row_selection_authority: SourceRowSelectionAuthorityContract
    source_row_selection_authority_hash: str
    role_selection_contracts: tuple[SourceInputRoleSelectionContract, ...]
    expected_source_row_batch_contract_hash_by_input_role: dict[str, str]
    expected_source_row_batch_hash_by_input_role: dict[str, str]
    active_selected_row_hash_by_input_role: dict[str, str]
    active_selected_row_locator_hash_by_input_role: dict[str, str]
    expected_selected_row_hash_by_input_role: dict[str, str]
    expected_selected_row_locator_hash_by_input_role: dict[str, str]
    expected_selected_row_membership_proof_hash_by_input_role: dict[str, str]
    expected_selected_row_locator_membership_proof_hash_by_input_role: dict[str, str]
    source_input_selection_set_hash: str
    source_input_selection_contract_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        raise CarverBlocked(
            "S27 v2 source input selection requires an external authority handle"
        )

    def validate_against_external_authority(
        self,
        external_authority: SourceRowSelectionExternalAuthorityHandle,
        source_row_batch_contract: SourceRowBatchSetContract,
        parser_output_contract: ParserOutputBatchSetContract,
    ) -> None:
        external_authority.validate()
        source_row_batch_contract.validate_against_parser_output_authority(parser_output_contract)
        self.source_row_selection_authority.validate()
        self._validate_contract_only_shape()
        self._validate_source_row_batch_authority(source_row_batch_contract)
        self._validate_external_authority_binding(external_authority)
        self._validate_source_row_selection_authority(external_authority)
        self._validate_role_selection_contracts()
        require_hash("S27 v2 source input selection-set hash", self.source_input_selection_set_hash)
        require_hash("S27 v2 source input selection contract hash", self.source_input_selection_contract_hash)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 source input selection contract must preserve non-authorizations")

    def _validate_contract_only_shape(self) -> None:
        require_text("S27 v2 source input selection contract status", self.status)
        if self.status != S27_V2_SOURCE_INPUT_SELECTION_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 source input selection contract must remain contract-only")
        if tuple(REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE) != REQUIRED_SOURCE_INPUT_ROLES:
            raise CarverBlocked("S27 v2 source input role map must cover the locked role tuple")
        require_hash(
            "S27 v2 source input selection source row batch contract hash",
            self.source_row_batch_contract_hash,
        )
        require_hash("S27 v2 source input selection source row batch-set hash", self.source_row_batch_set_hash)
        require_hash(
            "S27 v2 source input selection source universe contract bundle hash",
            self.source_universe_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source input selection row locator contract bundle hash",
            self.row_locator_contract_bundle_hash,
        )
        require_hash(
            "S27 v2 source input selection canonical serialization policy hash",
            self.canonical_serialization_policy_hash,
        )
        require_hash_map(
            "S27 v2 source input selection expected source-row-batch contract map",
            self.expected_source_row_batch_contract_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map(
            "S27 v2 source input selection expected source-row-batch hash map",
            self.expected_source_row_batch_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map(
            "S27 v2 source input selection active selected-row authority map",
            self.active_selected_row_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map(
            "S27 v2 source input selection active selected-row-locator authority map",
            self.active_selected_row_locator_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input selection selected-row authority",
            self.expected_selected_row_hash_by_input_role,
            self._active_selected_row_hash_by_input_role(),
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input selection selected-row-locator authority",
            self.expected_selected_row_locator_hash_by_input_role,
            self._active_selected_row_locator_hash_by_input_role(),
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input selection selected-row membership proof authority",
            self.expected_selected_row_membership_proof_hash_by_input_role,
            self._active_selected_row_membership_proof_hash_by_input_role(),
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input selection selected-row-locator membership proof authority",
            self.expected_selected_row_locator_membership_proof_hash_by_input_role,
            self._active_selected_row_locator_membership_proof_hash_by_input_role(),
            REQUIRED_SOURCE_INPUT_ROLES,
        )

    def _validate_role_selection_contracts(self) -> None:
        require_non_empty_tuple(
            "S27 v2 source input role selection contracts",
            self.role_selection_contracts,
        )
        seen_roles: set[str] = set()
        for contract in self.role_selection_contracts:
            contract.validate()
            if contract.input_role in seen_roles:
                raise CarverBlocked("S27 v2 source input role selections must be unique")
            seen_roles.add(contract.input_role)
            require_expected_hash(
                "S27 v2 source input role source-row-batch contract hash",
                contract.input_role,
                contract.source_row_batch_family_contract_hash,
                self.expected_source_row_batch_contract_hash_by_input_role,
            )
            require_expected_hash(
                "S27 v2 source input role source-row-batch hash",
                contract.input_role,
                contract.source_row_batch_hash,
                self.expected_source_row_batch_hash_by_input_role,
            )
            require_expected_hash(
                "S27 v2 source input role selected row hash",
                contract.input_role,
                contract.selected_row_hash,
                self.expected_selected_row_hash_by_input_role,
            )
            require_expected_hash(
                "S27 v2 source input role selected row locator hash",
                contract.input_role,
                contract.selected_row_locator_hash,
                self.expected_selected_row_locator_hash_by_input_role,
            )
            require_expected_hash(
                "S27 v2 source input role selected row membership proof hash",
                contract.input_role,
                contract.selected_row_membership_proof_hash,
                self.expected_selected_row_membership_proof_hash_by_input_role,
            )
            require_expected_hash(
                "S27 v2 source input role selected row-locator membership proof hash",
                contract.input_role,
                contract.selected_row_locator_membership_proof_hash,
                self.expected_selected_row_locator_membership_proof_hash_by_input_role,
            )
        if tuple(contract.input_role for contract in self.role_selection_contracts) != REQUIRED_SOURCE_INPUT_ROLES:
            raise CarverBlocked("S27 v2 source input roles must match the locked role tuple")

    def _active_source_row_batch_contract_hash_by_input_role_from_authority(
        self,
        source_row_batch_contract: SourceRowBatchSetContract,
    ) -> dict[str, str]:
        source_row_batch_family_by_family = self._source_row_batch_family_contract_by_family(
            source_row_batch_contract,
        )
        return {
            input_role: source_row_batch_family_by_family[
                REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[input_role]
            ].source_row_batch_family_contract_hash
            for input_role in REQUIRED_SOURCE_INPUT_ROLES
        }

    def _active_source_row_batch_hash_by_input_role_from_authority(
        self,
        source_row_batch_contract: SourceRowBatchSetContract,
    ) -> dict[str, str]:
        source_row_batch_family_by_family = self._source_row_batch_family_contract_by_family(
            source_row_batch_contract,
        )
        return {
            input_role: source_row_batch_family_by_family[
                REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE[input_role]
            ].source_row_batch_hash
            for input_role in REQUIRED_SOURCE_INPUT_ROLES
        }

    def _active_selected_row_hash_by_input_role(self) -> dict[str, str]:
        return self.source_row_selection_authority.selected_row_hash_by_input_role

    def _active_selected_row_locator_hash_by_input_role(self) -> dict[str, str]:
        return self.source_row_selection_authority.selected_row_locator_hash_by_input_role

    def _active_selected_row_membership_proof_hash_by_input_role(self) -> dict[str, str]:
        return self.source_row_selection_authority.selected_row_membership_proof_hash_by_input_role

    def _active_selected_row_locator_membership_proof_hash_by_input_role(self) -> dict[str, str]:
        return self.source_row_selection_authority.selected_row_locator_membership_proof_hash_by_input_role

    def _validate_external_authority_binding(
        self,
        external_authority: SourceRowSelectionExternalAuthorityHandle,
    ) -> None:
        if external_authority.source_row_batch_contract_hash != self.source_row_batch_contract_hash:
            raise CarverBlocked("S27 v2 source input selection must bind external source-row-batch contract")
        if external_authority.source_row_batch_set_hash != self.source_row_batch_set_hash:
            raise CarverBlocked("S27 v2 source input selection must bind external source-row-batch set")
        if external_authority.source_universe_contract_bundle_hash != self.source_universe_contract_bundle_hash:
            raise CarverBlocked("S27 v2 source input selection must bind external source universe")
        if external_authority.row_locator_contract_bundle_hash != self.row_locator_contract_bundle_hash:
            raise CarverBlocked("S27 v2 source input selection must bind external row locator")
        if external_authority.source_row_selection_authority_hash != self.source_row_selection_authority_hash:
            raise CarverBlocked("S27 v2 source input selection must bind external row-selection authority")
        if (
            external_authority.selected_row_membership_proof_set_hash
            != self.source_row_selection_authority.selected_row_membership_proof_set_hash
        ):
            raise CarverBlocked("S27 v2 source input selection must bind external selected-row proof set")
        if (
            external_authority.selected_row_locator_membership_proof_set_hash
            != self.source_row_selection_authority.selected_row_locator_membership_proof_set_hash
        ):
            raise CarverBlocked("S27 v2 source input selection must bind external selected-row-locator proof set")

    def _validate_source_row_batch_authority(
        self,
        source_row_batch_contract: SourceRowBatchSetContract,
    ) -> None:
        if source_row_batch_contract.source_row_batch_contract_hash != self.source_row_batch_contract_hash:
            raise CarverBlocked("S27 v2 source input selection must bind active source-row-batch contract")
        if source_row_batch_contract.source_row_batch_set_hash != self.source_row_batch_set_hash:
            raise CarverBlocked("S27 v2 source input selection must bind active source-row-batch set")
        if source_row_batch_contract.source_universe_contract_bundle_hash != self.source_universe_contract_bundle_hash:
            raise CarverBlocked("S27 v2 source input selection must bind source-row-batch source universe")
        if source_row_batch_contract.row_locator_contract_bundle_hash != self.row_locator_contract_bundle_hash:
            raise CarverBlocked("S27 v2 source input selection must bind source-row-batch row locator")
        require_hash_map_matches_active_authority(
            "S27 v2 source input selection source-row-batch contract authority",
            self.expected_source_row_batch_contract_hash_by_input_role,
            self._active_source_row_batch_contract_hash_by_input_role_from_authority(
                source_row_batch_contract,
            ),
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input selection source-row-batch hash authority",
            self.expected_source_row_batch_hash_by_input_role,
            self._active_source_row_batch_hash_by_input_role_from_authority(
                source_row_batch_contract,
            ),
            REQUIRED_SOURCE_INPUT_ROLES,
        )

    def _source_row_batch_family_contract_by_family(
        self,
        source_row_batch_contract: SourceRowBatchSetContract,
    ) -> dict[str, SourceRowBatchFamilyContract]:
        source_row_batch_family_by_family = {
            contract.row_family: contract
            for contract in source_row_batch_contract.source_row_batch_family_contracts
        }
        if tuple(source_row_batch_family_by_family) != REQUIRED_SOURCE_ROW_BATCH_FAMILIES:
            raise CarverBlocked("S27 v2 source input selection source-row-batch families must match locked tuple")
        return source_row_batch_family_by_family

    def _validate_source_row_selection_authority(
        self,
        external_authority: SourceRowSelectionExternalAuthorityHandle,
    ) -> None:
        self.source_row_selection_authority.validate()
        require_hash(
            "S27 v2 source input selection source-row-selection authority hash",
            self.source_row_selection_authority_hash,
        )
        if (
            self.source_row_selection_authority.source_row_selection_authority_hash
            != self.source_row_selection_authority_hash
        ):
            raise CarverBlocked("S27 v2 source input selection must bind active row-selection authority hash")
        if self.source_row_selection_authority.source_row_batch_contract_hash != self.source_row_batch_contract_hash:
            raise CarverBlocked("S27 v2 source input selection authority must bind source-row-batch contract")
        if self.source_row_selection_authority.source_row_batch_set_hash != self.source_row_batch_set_hash:
            raise CarverBlocked("S27 v2 source input selection authority must bind source-row-batch set")
        if (
            self.source_row_selection_authority.source_universe_contract_bundle_hash
            != self.source_universe_contract_bundle_hash
        ):
            raise CarverBlocked("S27 v2 source input selection authority must bind source universe")
        if self.source_row_selection_authority.row_locator_contract_bundle_hash != self.row_locator_contract_bundle_hash:
            raise CarverBlocked("S27 v2 source input selection authority must bind row locator")
        if (
            self.source_row_selection_authority.selected_row_membership_proof_set_hash
            != external_authority.selected_row_membership_proof_set_hash
        ):
            raise CarverBlocked("S27 v2 source input selection authority must bind external row proof set")
        if (
            self.source_row_selection_authority.selected_row_locator_membership_proof_set_hash
            != external_authority.selected_row_locator_membership_proof_set_hash
        ):
            raise CarverBlocked("S27 v2 source input selection authority must bind external locator proof set")
        require_hash_map_matches_active_authority(
            "S27 v2 source input selection active selected-row authority map",
            self.active_selected_row_hash_by_input_role,
            self.source_row_selection_authority.selected_row_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )
        require_hash_map_matches_active_authority(
            "S27 v2 source input selection active selected-row-locator authority map",
            self.active_selected_row_locator_hash_by_input_role,
            self.source_row_selection_authority.selected_row_locator_hash_by_input_role,
            REQUIRED_SOURCE_INPUT_ROLES,
        )

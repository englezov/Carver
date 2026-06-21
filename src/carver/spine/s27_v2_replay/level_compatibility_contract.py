from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION
from .validation import require_hash, require_non_empty_tuple, require_text


S27_V2_LEVEL_COMPATIBILITY_CONTRACT_ONLY_STATUS = "S27_V2_LEVEL_COMPATIBILITY_CONTRACT_ONLY"
PLANNED_LEVEL_COMPATIBILITY_PROOF_STATUS = "PLANNED_LEVEL_COMPATIBILITY_PROOF_ONLY"

LEVEL_COMPATIBILITY_REASON_CODES = (
    "SAME_LEVEL_COMPATIBLE",
    "BRIDGED_CONTINUOUS_COMPATIBLE",
)

REQUIRED_LEVEL_COMPATIBILITY_PROOFS = (
    "SIGMA_BRIDGE_USES_PREVIOUS_COMPLETED_CURRENT_CONTRACT_CLOSE",
    "HOURLY_CURRENT_MATCHES_DAILY_CURRENT_CONTRACT_LEVEL",
    "CONTINUOUS_TO_CURRENT_CONTRACT_LEVEL_BRIDGE",
    "BRIDGED_DAILY_CONTINUOUS_EQUILIBRIUM",
)


@dataclass(frozen=True)
class LevelCompatibilitySourceBinding:
    daily_continuous_row_family_hash: str
    daily_current_contract_row_family_hash: str
    previous_completed_current_contract_close_family_hash: str
    hourly_decision_row_family_hash: str
    hourly_fill_row_family_hash: str
    source_universe_contract_hash: str
    row_locator_contract_hash: str
    binding_hash: str

    def validate(self) -> None:
        require_hash("S27 v2 level compatibility daily continuous family hash", self.daily_continuous_row_family_hash)
        require_hash(
            "S27 v2 level compatibility daily current-contract family hash",
            self.daily_current_contract_row_family_hash,
        )
        require_hash(
            "S27 v2 level compatibility previous completed current-contract close family hash",
            self.previous_completed_current_contract_close_family_hash,
        )
        require_hash("S27 v2 level compatibility hourly decision family hash", self.hourly_decision_row_family_hash)
        require_hash("S27 v2 level compatibility hourly fill family hash", self.hourly_fill_row_family_hash)
        require_hash("S27 v2 level compatibility source universe contract hash", self.source_universe_contract_hash)
        require_hash("S27 v2 level compatibility row locator contract hash", self.row_locator_contract_hash)
        require_hash("S27 v2 level compatibility source binding hash", self.binding_hash)


@dataclass(frozen=True)
class LevelCompatibilityProofContract:
    proof_label: str
    proof_status: str
    required_input_hashes: tuple[str, ...]
    proof_policy_hash: str
    planned_proof_output_hash: str
    proof_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 level compatibility proof label", self.proof_label)
        if self.proof_label not in REQUIRED_LEVEL_COMPATIBILITY_PROOFS:
            raise CarverBlocked("S27 v2 level compatibility proof label is not locked")
        require_text("S27 v2 level compatibility proof status", self.proof_status)
        if self.proof_status != PLANNED_LEVEL_COMPATIBILITY_PROOF_STATUS:
            raise CarverBlocked("S27 v2 level compatibility proof must remain planned-only")
        require_non_empty_tuple("S27 v2 level compatibility proof input hashes", self.required_input_hashes)
        for input_hash in self.required_input_hashes:
            require_hash("S27 v2 level compatibility proof input hash", input_hash)
        require_hash("S27 v2 level compatibility proof policy hash", self.proof_policy_hash)
        require_hash("S27 v2 level compatibility planned proof output hash", self.planned_proof_output_hash)
        require_hash("S27 v2 level compatibility proof contract hash", self.proof_contract_hash)


@dataclass(frozen=True)
class LevelCompatibilityVerdictContract:
    compatibility_verdict: str
    compatibility_reason_code: str
    required_proof_contract_hashes: tuple[str, ...]
    continuous_adjustment_bridge_policy_hash: str
    sigma_bridge_level_source_policy_hash: str
    verdict_policy_hash: str
    planned_ledger_schema_hash: str
    verdict_contract_hash: str

    def validate(self) -> None:
        require_text("S27 v2 level compatibility verdict", self.compatibility_verdict)
        if self.compatibility_verdict != "PASS":
            raise CarverBlocked("S27 v2 level compatibility contract only permits planned PASS verdict shape")
        require_text("S27 v2 level compatibility reason code", self.compatibility_reason_code)
        if self.compatibility_reason_code not in LEVEL_COMPATIBILITY_REASON_CODES:
            raise CarverBlocked("S27 v2 level compatibility reason code is not locked")
        require_non_empty_tuple(
            "S27 v2 level compatibility required proof contract hashes",
            self.required_proof_contract_hashes,
        )
        for proof_hash in self.required_proof_contract_hashes:
            require_hash("S27 v2 level compatibility required proof contract hash", proof_hash)
        require_hash(
            "S27 v2 level compatibility continuous adjustment bridge policy hash",
            self.continuous_adjustment_bridge_policy_hash,
        )
        require_hash(
            "S27 v2 level compatibility sigma bridge level source policy hash",
            self.sigma_bridge_level_source_policy_hash,
        )
        require_hash("S27 v2 level compatibility verdict policy hash", self.verdict_policy_hash)
        require_hash("S27 v2 level compatibility planned ledger schema hash", self.planned_ledger_schema_hash)
        require_hash("S27 v2 level compatibility verdict contract hash", self.verdict_contract_hash)


@dataclass(frozen=True)
class LevelCompatibilityContractBundle:
    status: str
    source_binding: LevelCompatibilitySourceBinding
    proof_contracts: tuple[LevelCompatibilityProofContract, ...]
    verdict_contract: LevelCompatibilityVerdictContract
    daily_hourly_level_compatibility_policy_hash: str
    level_compatibility_contract_bundle_hash: str
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 level compatibility contract status", self.status)
        if self.status != S27_V2_LEVEL_COMPATIBILITY_CONTRACT_ONLY_STATUS:
            raise CarverBlocked("S27 v2 level compatibility contract must remain contract-only")
        self.source_binding.validate()
        require_non_empty_tuple("S27 v2 level compatibility proof contracts", self.proof_contracts)
        seen_proofs: set[str] = set()
        for proof in self.proof_contracts:
            proof.validate()
            if proof.proof_label in seen_proofs:
                raise CarverBlocked("S27 v2 level compatibility proof contracts must be unique")
            seen_proofs.add(proof.proof_label)
        if tuple(proof.proof_label for proof in self.proof_contracts) != REQUIRED_LEVEL_COMPATIBILITY_PROOFS:
            raise CarverBlocked("S27 v2 level compatibility proof contracts must match locked proof tuple")
        self.verdict_contract.validate()
        if len(self.verdict_contract.required_proof_contract_hashes) != len(REQUIRED_LEVEL_COMPATIBILITY_PROOFS):
            raise CarverBlocked("S27 v2 level compatibility verdict must reference every proof contract")
        if self.verdict_contract.required_proof_contract_hashes != tuple(
            proof.proof_contract_hash for proof in self.proof_contracts
        ):
            raise CarverBlocked("S27 v2 level compatibility verdict proof hashes must match proof contracts")
        require_hash(
            "S27 v2 level compatibility daily/hourly policy hash",
            self.daily_hourly_level_compatibility_policy_hash,
        )
        require_hash(
            "S27 v2 level compatibility contract bundle hash",
            self.level_compatibility_contract_bundle_hash,
        )
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 level compatibility contract must preserve non-authorizations")

"""Validation profile labels for fast S27_V2 mechanical replay."""

OPERATIONAL_VALIDATION_PROFILE = "OPERATIONAL_SEGMENT_HASH_AND_GENERATED_ROWS_NOT_FULL_PROOF"
CHECKPOINT_PROOF_VALIDATION_PROFILE = "CHECKPOINT_PROOF_PARITY_ORACLE_EXPLICIT_ONLY"
SUPPORTED_VALIDATION_PROFILES = (
    OPERATIONAL_VALIDATION_PROFILE,
    CHECKPOINT_PROOF_VALIDATION_PROFILE,
)


def is_checkpoint_proof_profile(validation_profile: str) -> bool:
    return validation_profile == CHECKPOINT_PROOF_VALIDATION_PROFILE


def require_supported_validation_profile(validation_profile: str) -> None:
    from ..m0 import CarverBlocked

    if validation_profile not in SUPPORTED_VALIDATION_PROFILES:
        raise CarverBlocked("S27 v2 fast validation profile is not recognized")

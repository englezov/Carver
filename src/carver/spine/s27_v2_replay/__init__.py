"""S27 ZN V2 trusted replay scaffolding.

Package-root exports are intentionally limited to the fail-closed replay
boundary. Row dataclasses in submodules are structural schemas only; they are
not source-faithful evidence unless a future trusted replay bundle emits them
under the active trust root.
"""

from .constants import (
    S27_V2_REPLAY_NON_AUTHORIZATION,
    STRUCTURAL_SCHEMA_ONLY_NOT_SOURCE_EVIDENCE,
)
from .runner import ReplayExecutionBlocked, build_trusted_replay_bundle

__all__ = [
    "ReplayExecutionBlocked",
    "S27_V2_REPLAY_NON_AUTHORIZATION",
    "STRUCTURAL_SCHEMA_ONLY_NOT_SOURCE_EVIDENCE",
    "build_trusted_replay_bundle",
]

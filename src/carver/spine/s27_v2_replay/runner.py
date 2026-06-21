from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .constants import S27_V2_REPLAY_NON_AUTHORIZATION, S27_V2_TRUSTED_REPLAY_BUNDLE_STATUS
from .evidence_manifest import EvidenceManifest, require_evidence_manifest_matches_trust_root
from .trust_root import ReplayTrustRoot
from .validation import require_text


class ReplayExecutionBlocked(CarverBlocked):
    """Raised because this scaffold is not authorized to execute replay."""


@dataclass(frozen=True)
class TrustedReplayBundleScaffold:
    status: str
    trust_root: ReplayTrustRoot
    evidence_manifest: EvidenceManifest
    non_authorizations: tuple[str, ...] = S27_V2_REPLAY_NON_AUTHORIZATION

    def validate(self) -> None:
        require_text("S27 v2 trusted replay bundle status", self.status)
        if self.status != S27_V2_TRUSTED_REPLAY_BUNDLE_STATUS:
            raise CarverBlocked("S27 v2 trusted replay bundle status mismatch")
        require_evidence_manifest_matches_trust_root(self.trust_root, self.evidence_manifest)
        if self.non_authorizations != S27_V2_REPLAY_NON_AUTHORIZATION:
            raise CarverBlocked("S27 v2 replay scaffold must preserve non-authorizations")


def build_trusted_replay_bundle(*_args: object, **_kwargs: object) -> TrustedReplayBundleScaffold:
    """Fail closed until parser/file replay execution receives separate authorization."""
    raise ReplayExecutionBlocked("S27 v2 trusted replay bundle execution is not authorized by scaffolding")

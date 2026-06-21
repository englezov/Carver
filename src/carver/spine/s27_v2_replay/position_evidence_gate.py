from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..m0 import CarverBlocked
from .constants import S27_V2_INSTRUMENT, S27_V2_LANE, S27_V2_STRATEGY_ID
from .forecast_executable import (
    ForecastExecutableBundle,
    build_forecast_executable_ledgers_on_remediation_pack,
)
from .local_replay import canonical_sha256
from .runtime_evidence_gate import RUNTIME_EVIDENCE_REMEDIATION_PACK_RELATIVE_PATH
from .validation import require_hash, require_text, require_tuple


S27_V2_POSITION_EVIDENCE_AUTHORIZATION = "S27_V2_POSITION_EVIDENCE_FAIL_CLOSED_GATE"
S27_V2_POSITION_EVIDENCE_STATUS = "S27_V2_POSITION_EVIDENCE_FAIL_CLOSED_NON_RESULT_NOT_POSITION"
POSITION_EVIDENCE_CHECK_STATUS_PASS = "PASS_ACTIVE_FORECAST_AUTHORITY_NOT_POSITION"
POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED = "FAIL_CLOSED_POSITION_EVIDENCE_UNRESOLVED"

POSITION_EVIDENCE_LABELS = (
    "FORECAST_AUTHORITY",
    "FORECAST_TO_POSITION_DIVISOR",
    "BASE_POSITION",
    "CAPITAL_ACCOUNT_VALUE",
    "RISK_TARGET",
    "MULTIPLIER_CURRENCY",
    "ROUNDING_POLICY",
    "INITIAL_CURRENT_POSITION_CONTEXT",
)

POSITION_EVIDENCE_GATE_BY_LABEL = {
    "FORECAST_AUTHORITY": "PASS_ACTIVE_FORECAST_EXECUTABLE_BUNDLE_NOT_POSITION",
    "FORECAST_TO_POSITION_DIVISOR": "BLOCKED_SOURCE_UNRESOLVED_FORECAST_TO_POSITION_DIVISOR_POLICY",
    "BASE_POSITION": "BLOCKED_SOURCE_UNRESOLVED_BASE_OR_OPTIMAL_POSITION_POLICY",
    "CAPITAL_ACCOUNT_VALUE": "BLOCKED_SOURCE_UNRESOLVED_CAPITAL_ACCOUNT_VALUE_POLICY",
    "RISK_TARGET": "BLOCKED_SOURCE_UNRESOLVED_RISK_TARGET_POLICY",
    "MULTIPLIER_CURRENCY": "BLOCKED_SOURCE_UNRESOLVED_CONTRACT_MULTIPLIER_CURRENCY_POLICY",
    "ROUNDING_POLICY": "BLOCKED_SOURCE_UNRESOLVED_POSITION_ROUNDING_POLICY",
    "INITIAL_CURRENT_POSITION_CONTEXT": "BLOCKED_SOURCE_UNRESOLVED_INITIAL_CURRENT_POSITION_CONTEXT",
}

POSITION_EVIDENCE_REQUIRED_STATUS_BY_LABEL = {
    "FORECAST_AUTHORITY": POSITION_EVIDENCE_CHECK_STATUS_PASS,
    "FORECAST_TO_POSITION_DIVISOR": POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
    "BASE_POSITION": POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
    "CAPITAL_ACCOUNT_VALUE": POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
    "RISK_TARGET": POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
    "MULTIPLIER_CURRENCY": POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
    "ROUNDING_POLICY": POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
    "INITIAL_CURRENT_POSITION_CONTEXT": POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
}

POSITION_EVIDENCE_NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
    "NO_DESIRED_POSITION_EMISSION",
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


@dataclass(frozen=True)
class PositionEvidenceCheck:
    evidence_label: str
    evidence_status: str
    gate_label: str
    upstream_forecast_bundle_hash: str
    observed_value_hash: str
    summary: str
    check_hash: str

    def validate(self) -> None:
        require_text("S27 v2 position evidence label", self.evidence_label)
        if self.evidence_label not in POSITION_EVIDENCE_LABELS:
            raise CarverBlocked("S27 v2 position evidence label is not locked")
        require_text("S27 v2 position evidence status", self.evidence_status)
        if self.evidence_status != POSITION_EVIDENCE_REQUIRED_STATUS_BY_LABEL[self.evidence_label]:
            raise CarverBlocked("S27 v2 position evidence status must match locked gate semantics")
        require_text("S27 v2 position evidence gate label", self.gate_label)
        if self.gate_label != POSITION_EVIDENCE_GATE_BY_LABEL[self.evidence_label]:
            raise CarverBlocked("S27 v2 position evidence gate label must match locked evidence label")
        require_hash("S27 v2 position evidence upstream forecast bundle hash", self.upstream_forecast_bundle_hash)
        require_hash("S27 v2 position evidence observed value hash", self.observed_value_hash)
        require_text("S27 v2 position evidence summary", self.summary)
        require_hash("S27 v2 position evidence check hash", self.check_hash)
        if self.check_hash != canonical_sha256(_position_evidence_check_hash_payload(self)):
            raise CarverBlocked("S27 v2 position evidence check hash must be content-bound")


@dataclass(frozen=True)
class PositionEvidenceGateBundle:
    status: str
    authorization_label: str
    strategy_id: str
    instrument: str
    lane: str
    input_pack_path: str
    forecast_bundle: ForecastExecutableBundle
    evidence_checks: tuple[PositionEvidenceCheck, ...]
    fail_closed_gate_labels: tuple[str, ...]
    forecast_authority_accepted: bool
    position_evidence_ready: bool
    desired_position_rows_emitted: bool
    order_rows_emitted: bool
    fill_rows_emitted: bool
    cost_rows_emitted: bool
    pnl_rows_emitted: bool
    result_scored_run_emitted: bool
    source_faithful_evidence_claimed: bool
    bundle_hash: str
    non_authorizations: tuple[str, ...] = POSITION_EVIDENCE_NON_AUTHORIZATIONS

    def validate(self) -> None:
        if self.status != S27_V2_POSITION_EVIDENCE_STATUS:
            raise CarverBlocked("S27 v2 position evidence status is not locked")
        if self.authorization_label != S27_V2_POSITION_EVIDENCE_AUTHORIZATION:
            raise CarverBlocked("S27 v2 position evidence authorization is not active")
        if self.strategy_id != S27_V2_STRATEGY_ID or self.instrument != S27_V2_INSTRUMENT:
            raise CarverBlocked("S27 v2 position evidence must remain ZN S27_V2 only")
        if self.lane != S27_V2_LANE:
            raise CarverBlocked("S27 v2 position evidence must remain source-native futures")
        pack_path = Path(self.input_pack_path).resolve()
        if pack_path != _REMEDIATION_PACK_PATH:
            raise CarverBlocked("S27 v2 position evidence is locked to the audited remediation pack")
        self.forecast_bundle.validate()
        active_forecast = build_forecast_executable_ledgers_on_remediation_pack(pack_path)
        if self.forecast_bundle != active_forecast:
            raise CarverBlocked("S27 v2 position evidence must bind active forecast executable bundle")
        require_tuple("S27 v2 position evidence checks", self.evidence_checks)
        if tuple(check.evidence_label for check in self.evidence_checks) != POSITION_EVIDENCE_LABELS:
            raise CarverBlocked("S27 v2 position evidence checks must match locked label tuple")
        for check in self.evidence_checks:
            check.validate()
            if check.upstream_forecast_bundle_hash != active_forecast.bundle_hash:
                raise CarverBlocked("S27 v2 position evidence check must bind active forecast bundle")
        active_checks = _build_active_position_evidence_checks(active_forecast)
        if self.evidence_checks != active_checks:
            raise CarverBlocked("S27 v2 position evidence checks must match active forecast-bound readiness")
        expected_fail_closed = tuple(
            POSITION_EVIDENCE_GATE_BY_LABEL[label]
            for label in POSITION_EVIDENCE_LABELS
            if POSITION_EVIDENCE_REQUIRED_STATUS_BY_LABEL[label] == POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED
        )
        require_tuple("S27 v2 position evidence fail-closed gates", self.fail_closed_gate_labels)
        if self.fail_closed_gate_labels != expected_fail_closed:
            raise CarverBlocked("S27 v2 position evidence fail-closed gates must remain unresolved")
        if self.forecast_authority_accepted is not True:
            raise CarverBlocked("S27 v2 position evidence must accept active forecast authority")
        if self.position_evidence_ready is not False:
            raise CarverBlocked("S27 v2 position evidence cannot be ready while position prerequisites fail closed")
        if any(
            flag is not False
            for flag in (
                self.desired_position_rows_emitted,
                self.order_rows_emitted,
                self.fill_rows_emitted,
                self.cost_rows_emitted,
                self.pnl_rows_emitted,
                self.result_scored_run_emitted,
                self.source_faithful_evidence_claimed,
            )
        ):
            raise CarverBlocked("S27 v2 position evidence cannot emit desired-position/order/fill/cost/PnL/result/evidence")
        if self.non_authorizations != POSITION_EVIDENCE_NON_AUTHORIZATIONS:
            raise CarverBlocked("S27 v2 position evidence must preserve non-authorizations")
        require_hash("S27 v2 position evidence bundle hash", self.bundle_hash)
        if self.bundle_hash != canonical_sha256(_position_evidence_bundle_hash_payload(self)):
            raise CarverBlocked("S27 v2 position evidence bundle hash must be content-bound")


def build_position_evidence_fail_closed_gate(
    input_pack_path: str | Path = _REMEDIATION_PACK_PATH,
) -> PositionEvidenceGateBundle:
    pack_path = Path(input_pack_path).resolve()
    if pack_path != _REMEDIATION_PACK_PATH:
        raise CarverBlocked("S27 v2 position evidence run is locked to the audited remediation pack")
    forecast_bundle = build_forecast_executable_ledgers_on_remediation_pack(pack_path)
    checks = _build_active_position_evidence_checks(forecast_bundle)
    bundle = PositionEvidenceGateBundle(
        status=S27_V2_POSITION_EVIDENCE_STATUS,
        authorization_label=S27_V2_POSITION_EVIDENCE_AUTHORIZATION,
        strategy_id=S27_V2_STRATEGY_ID,
        instrument=S27_V2_INSTRUMENT,
        lane=S27_V2_LANE,
        input_pack_path=str(pack_path),
        forecast_bundle=forecast_bundle,
        evidence_checks=checks,
        fail_closed_gate_labels=tuple(
            POSITION_EVIDENCE_GATE_BY_LABEL[label]
            for label in POSITION_EVIDENCE_LABELS
            if POSITION_EVIDENCE_REQUIRED_STATUS_BY_LABEL[label] == POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED
        ),
        forecast_authority_accepted=True,
        position_evidence_ready=False,
        desired_position_rows_emitted=False,
        order_rows_emitted=False,
        fill_rows_emitted=False,
        cost_rows_emitted=False,
        pnl_rows_emitted=False,
        result_scored_run_emitted=False,
        source_faithful_evidence_claimed=False,
        bundle_hash="0" * 64,
    )
    bundle = PositionEvidenceGateBundle(
        **{**bundle.__dict__, "bundle_hash": canonical_sha256(_position_evidence_bundle_hash_payload(bundle))}
    )
    bundle.validate()
    return bundle


def _build_active_position_evidence_checks(
    forecast_bundle: ForecastExecutableBundle,
) -> tuple[PositionEvidenceCheck, ...]:
    forecast_hash = forecast_bundle.bundle_hash
    summaries = {
        "FORECAST_AUTHORITY": (
            "Active forecast executable bundle validates and rebuilds from the audited remediation pack; "
            "this authorizes readiness input only, not desired-position emission."
        ),
        "FORECAST_TO_POSITION_DIVISOR": (
            "Forecast-to-position divisor is present only in pre-v2 diagnostic code and is not v2 source authority."
        ),
        "BASE_POSITION": (
            "Book/source-native base or optimal position sizing evidence is not bound under the v2 trust model."
        ),
        "CAPITAL_ACCOUNT_VALUE": (
            "Capital/account value policy for position sizing is unresolved for v2 source-native evidence."
        ),
        "RISK_TARGET": "Risk target policy for position sizing is unresolved for v2 source-native evidence.",
        "MULTIPLIER_CURRENCY": (
            "The remediation pack carries cost-parameter hashes, but multiplier/currency remains fail-closed for "
            "position sizing authority."
        ),
        "ROUNDING_POLICY": (
            "Nearest rounding appears only in planned/pre-v2 surfaces; tie-break and source policy remain unresolved."
        ),
        "INITIAL_CURRENT_POSITION_CONTEXT": (
            "Initial/current position context and first-row policy are unresolved under v2 source authority."
        ),
    }
    observed_hashes = {
        "FORECAST_AUTHORITY": forecast_bundle.forecast_row.row_hash,
        "FORECAST_TO_POSITION_DIVISOR": _unresolved_value_hash("FORECAST_TO_POSITION_DIVISOR"),
        "BASE_POSITION": _unresolved_value_hash("BASE_POSITION"),
        "CAPITAL_ACCOUNT_VALUE": _unresolved_value_hash("CAPITAL_ACCOUNT_VALUE"),
        "RISK_TARGET": _unresolved_value_hash("RISK_TARGET"),
        "MULTIPLIER_CURRENCY": _unresolved_value_hash("MULTIPLIER_CURRENCY"),
        "ROUNDING_POLICY": _unresolved_value_hash("ROUNDING_POLICY"),
        "INITIAL_CURRENT_POSITION_CONTEXT": _unresolved_value_hash("INITIAL_CURRENT_POSITION_CONTEXT"),
    }
    checks = []
    for label in POSITION_EVIDENCE_LABELS:
        check = PositionEvidenceCheck(
            evidence_label=label,
            evidence_status=POSITION_EVIDENCE_REQUIRED_STATUS_BY_LABEL[label],
            gate_label=POSITION_EVIDENCE_GATE_BY_LABEL[label],
            upstream_forecast_bundle_hash=forecast_hash,
            observed_value_hash=observed_hashes[label],
            summary=summaries[label],
            check_hash="0" * 64,
        )
        checks.append(
            PositionEvidenceCheck(
                **{**check.__dict__, "check_hash": canonical_sha256(_position_evidence_check_hash_payload(check))}
            )
        )
    return tuple(checks)


def _unresolved_value_hash(label: str) -> str:
    return canonical_sha256(
        {
            "artifact": "S27_V2_POSITION_EVIDENCE_UNRESOLVED_VALUE",
            "label": label,
            "status": POSITION_EVIDENCE_CHECK_STATUS_FAIL_CLOSED,
        }
    )


def _position_evidence_check_hash_payload(check: PositionEvidenceCheck) -> dict[str, object]:
    return {
        "evidence_label": check.evidence_label,
        "evidence_status": check.evidence_status,
        "gate_label": check.gate_label,
        "observed_value_hash": check.observed_value_hash,
        "summary": check.summary,
        "upstream_forecast_bundle_hash": check.upstream_forecast_bundle_hash,
    }


def _position_evidence_bundle_hash_payload(bundle: PositionEvidenceGateBundle) -> dict[str, object]:
    return {
        "artifact": "S27_V2_POSITION_EVIDENCE_FAIL_CLOSED_GATE_BUNDLE",
        "authorization_label": bundle.authorization_label,
        "cost_rows_emitted": bundle.cost_rows_emitted,
        "desired_position_rows_emitted": bundle.desired_position_rows_emitted,
        "evidence_check_hashes": tuple(check.check_hash for check in bundle.evidence_checks),
        "fail_closed_gate_labels": bundle.fail_closed_gate_labels,
        "fill_rows_emitted": bundle.fill_rows_emitted,
        "forecast_authority_accepted": bundle.forecast_authority_accepted,
        "forecast_bundle_hash": bundle.forecast_bundle.bundle_hash,
        "input_pack_path": bundle.input_pack_path,
        "instrument": bundle.instrument,
        "lane": bundle.lane,
        "non_authorizations": bundle.non_authorizations,
        "order_rows_emitted": bundle.order_rows_emitted,
        "pnl_rows_emitted": bundle.pnl_rows_emitted,
        "position_evidence_ready": bundle.position_evidence_ready,
        "result_scored_run_emitted": bundle.result_scored_run_emitted,
        "source_faithful_evidence_claimed": bundle.source_faithful_evidence_claimed,
        "status": bundle.status,
        "strategy_id": bundle.strategy_id,
    }

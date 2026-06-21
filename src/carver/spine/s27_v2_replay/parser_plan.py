from __future__ import annotations

from dataclasses import dataclass

from ..m0 import CarverBlocked
from .validation import require_hash, require_non_empty_tuple, require_text


@dataclass(frozen=True)
class ParserFamilyPlan:
    parser_family_label: str
    parser_extractor_source_hash: str
    expected_input_artifact_types: tuple[str, ...]
    expected_output_row_schema_family: str
    canonical_row_locator_policy_hash: str
    completed_bar_policy_hash: str
    strict_prior_policy_hash: str
    duplicate_policy_hash: str
    missing_policy_hash: str
    degraded_row_policy_hash: str
    fail_closed_reason_code: str
    parser_plan_hash: str

    def validate(self) -> None:
        require_text("S27 v2 parser family label", self.parser_family_label)
        require_hash("S27 v2 parser/extractor source hash", self.parser_extractor_source_hash)
        require_non_empty_tuple("S27 v2 parser expected input artifact types", self.expected_input_artifact_types)
        for artifact_type in self.expected_input_artifact_types:
            require_text("S27 v2 parser expected input artifact type", artifact_type)
        require_text("S27 v2 parser expected output row schema family", self.expected_output_row_schema_family)
        require_hash("S27 v2 parser canonical row locator policy hash", self.canonical_row_locator_policy_hash)
        require_hash("S27 v2 parser completed-bar policy hash", self.completed_bar_policy_hash)
        require_hash("S27 v2 parser strict-prior policy hash", self.strict_prior_policy_hash)
        require_hash("S27 v2 parser duplicate policy hash", self.duplicate_policy_hash)
        require_hash("S27 v2 parser missing policy hash", self.missing_policy_hash)
        require_hash("S27 v2 parser degraded-row policy hash", self.degraded_row_policy_hash)
        require_text("S27 v2 parser fail-closed reason code", self.fail_closed_reason_code)
        require_hash("S27 v2 parser plan hash", self.parser_plan_hash)


@dataclass(frozen=True)
class DailyParserPlan:
    family_plan: ParserFamilyPlan

    def validate(self) -> None:
        self.family_plan.validate()
        if self.family_plan.parser_family_label != "DAILY_COMPLETED_BAR_PARSER_PLAN":
            raise CarverBlocked("S27 v2 daily parser plan family label mismatch")


@dataclass(frozen=True)
class HourlyParserPlan:
    family_plan: ParserFamilyPlan

    def validate(self) -> None:
        self.family_plan.validate()
        if self.family_plan.parser_family_label != "HOURLY_COMPLETED_BAR_PARSER_PLAN":
            raise CarverBlocked("S27 v2 hourly parser plan family label mismatch")


@dataclass(frozen=True)
class SessionParserPlan:
    family_plan: ParserFamilyPlan

    def validate(self) -> None:
        self.family_plan.validate()
        if self.family_plan.parser_family_label != "SESSION_CALENDAR_PARSER_PLAN":
            raise CarverBlocked("S27 v2 session parser plan family label mismatch")


@dataclass(frozen=True)
class RollParserPlan:
    family_plan: ParserFamilyPlan

    def validate(self) -> None:
        self.family_plan.validate()
        if self.family_plan.parser_family_label != "ROLL_CALENDAR_PARSER_PLAN":
            raise CarverBlocked("S27 v2 roll parser plan family label mismatch")


@dataclass(frozen=True)
class CostParameterParserPlan:
    family_plan: ParserFamilyPlan

    def validate(self) -> None:
        self.family_plan.validate()
        if self.family_plan.parser_family_label != "COST_PARAMETER_PARSER_PLAN":
            raise CarverBlocked("S27 v2 cost parameter parser plan family label mismatch")


@dataclass(frozen=True)
class ParserPlanBundle:
    daily_parser_plan: DailyParserPlan
    hourly_parser_plan: HourlyParserPlan
    session_parser_plan: SessionParserPlan
    roll_parser_plan: RollParserPlan
    cost_parameter_parser_plan: CostParameterParserPlan
    parser_plan_bundle_hash: str

    def validate(self) -> None:
        self.daily_parser_plan.validate()
        self.hourly_parser_plan.validate()
        self.session_parser_plan.validate()
        self.roll_parser_plan.validate()
        self.cost_parameter_parser_plan.validate()
        require_hash("S27 v2 parser plan bundle hash", self.parser_plan_bundle_hash)

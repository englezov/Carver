from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import BackAdjustmentSpec, CarverBlocked, RollRuleSpec, SessionCalendarSpec, SourceRuleStatus  # noqa: E402
from carver.spine.m3 import p01_risk_parity, p02_all_weather  # noqa: E402
from carver.spine.portfolio_completion import (  # noqa: E402
    PortfolioCompletionStatus,
    IntakeRouteContract,
    PortfolioIntakeMode,
    RiskFxInputContract,
    SourceArtifactRef,
    build_portfolio_completion_report,
)
from carver.spine.portfolio_conformance import ProviderMappingStatus  # noqa: E402


class PortfolioCompletionGateSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.as_of = datetime(2026, 5, 28, tzinfo=timezone.utc)
        self.locked_risk_fx = RiskFxInputContract(
            as_of=self.as_of,
            annual_risk_status=SourceRuleStatus.LOCKED,
            fx_status=SourceRuleStatus.LOCKED,
            annual_risk_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            fx_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
        )

    def test_p01_completion_report_blocks_real_data_until_exact_inputs_are_locked(self) -> None:
        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            self.locked_risk_fx,
            intake_contract=IntakeRouteContract(PortfolioIntakeMode.DIRECT_DAILY_PRIMARY),
        )

        self.assertEqual(report.status, PortfolioCompletionStatus.SYNTHETIC_READY_REAL_DATA_BLOCKED)
        self.assertEqual(report.intake_mode, PortfolioIntakeMode.DIRECT_DAILY_PRIMARY)
        self.assertEqual([(row.contract_code, row.status) for row in report.mapping_rows], [("MES", ProviderMappingStatus.UNRESOLVED), ("ZN", ProviderMappingStatus.LOCKED)])
        self.assertIn("provider mapping unresolved for MES 06-26", report.blockers)
        self.assertIn("intake route contract is unresolved", report.blockers)
        self.assertIn("session calendar is unresolved", report.blockers)
        self.assertIn("roll rule is unresolved", report.blockers)
        self.assertIn("back-adjustment rule is unresolved", report.blockers)
        with self.assertRaises(CarverBlocked):
            report.require_real_data_ready()

    def test_p02_completion_report_names_all_book_legs_without_es_substitution(self) -> None:
        report = build_portfolio_completion_report(
            p02_all_weather(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26", "ZF": "06-26", "QM": "06-26", "ZC": "06-26", "MGC": "06-26"},
            self.locked_risk_fx,
        )

        self.assertEqual([row.contract_code for row in report.mapping_rows], ["MES", "ZN", "ZF", "QM", "ZC", "MGC"])
        self.assertNotIn("ES", [row.contract_code for row in report.mapping_rows])
        self.assertEqual(sum(row.status is ProviderMappingStatus.LOCKED for row in report.mapping_rows), 1)
        for code in ("MES", "ZF", "QM", "ZC", "MGC"):
            self.assertIn(f"provider mapping unresolved for {code} 06-26", report.blockers)

    def test_risk_fx_contract_fails_closed_until_sources_are_locked(self) -> None:
        unresolved = RiskFxInputContract(
            as_of=self.as_of,
            annual_risk_status=SourceRuleStatus.UNRESOLVED,
            fx_status=SourceRuleStatus.UNRESOLVED,
        )
        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            unresolved,
        )

        self.assertIn("annual risk input contract is unresolved", report.blockers)
        self.assertIn("FX input contract is unresolved", report.blockers)
        with self.assertRaises(CarverBlocked):
            RiskFxInputContract(
                as_of=datetime(2026, 5, 28),
                annual_risk_status=SourceRuleStatus.LOCKED,
                fx_status=SourceRuleStatus.LOCKED,
                annual_risk_artifact=SourceArtifactRef("docs/process/risk.md"),
                fx_artifact=SourceArtifactRef("docs/process/fx.md"),
            ).validate()
        with self.assertRaises(CarverBlocked):
            RiskFxInputContract(
                as_of=datetime(2026, 5, 28, 12, tzinfo=timezone.utc),
                annual_risk_status=SourceRuleStatus.LOCKED,
                fx_status=SourceRuleStatus.LOCKED,
                annual_risk_artifact=SourceArtifactRef("docs/process/risk.md"),
                fx_artifact=SourceArtifactRef("docs/process/fx.md"),
            ).validate()
        with self.assertRaises(CarverBlocked):
            RiskFxInputContract(
                as_of=self.as_of,
                annual_risk_status=SourceRuleStatus.LOCKED,
                fx_status=SourceRuleStatus.LOCKED,
                annual_risk_artifact=None,
                fx_artifact=SourceArtifactRef("docs/process/fx.md"),
            ).validate()
        with self.assertRaises(CarverBlocked):
            RiskFxInputContract(
                as_of=self.as_of,
                annual_risk_status=SourceRuleStatus.LOCKED,
                fx_status=SourceRuleStatus.LOCKED,
                annual_risk_artifact=SourceArtifactRef("tmp/risk.txt"),
                fx_artifact=SourceArtifactRef("docs/process/fx.md"),
            ).validate()
        for bad_path in (
            "docs/process/DOES_NOT_EXIST.md",
            "docs/process/../mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md",
            "docs/researchops/../../QuantLab_v3/foo.md",
            str(ROOT / "docs" / "process" / "CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
        ):
            with self.subTest(bad_path=bad_path):
                with self.assertRaises(CarverBlocked):
                    SourceArtifactRef(bad_path).validate("artifact")

    def test_report_can_only_be_ready_when_all_non_performance_inputs_are_locked(self) -> None:
        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            self.locked_risk_fx,
            intake_contract=IntakeRouteContract(
                PortfolioIntakeMode.DIRECT_DAILY_PRIMARY,
                SourceRuleStatus.LOCKED,
                SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            ),
            session_calendar=SessionCalendarSpec("P01/P02 session calendar", SourceRuleStatus.LOCKED, "UTC"),
            roll_rule=RollRuleSpec("P01/P02 roll rule", SourceRuleStatus.LOCKED),
            back_adjustment=BackAdjustmentSpec("P01/P02 back-adjustment rule", SourceRuleStatus.LOCKED),
            session_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            roll_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            back_adjustment_artifact=SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
        )

        self.assertEqual(report.status, PortfolioCompletionStatus.SYNTHETIC_READY_REAL_DATA_BLOCKED)
        self.assertEqual(report.blockers, ("provider mapping unresolved for MES 06-26",))
        with self.assertRaises(CarverBlocked):
            build_portfolio_completion_report(
                p01_risk_parity(1_000_000, 0.20, 1.0),
                {"MES": "06-26", "ZN": "06-26"},
                self.locked_risk_fx,
                intake_contract=IntakeRouteContract("DIRECT_DAILY_PRIMARY"),
            )
        with self.assertRaises(CarverBlocked):
            IntakeRouteContract(
                PortfolioIntakeMode.DIRECT_DAILY_PRIMARY,
                SourceRuleStatus.LOCKED,
                "",
            ).validate()

    def test_locked_rule_placeholders_still_need_artifact_references(self) -> None:
        report = build_portfolio_completion_report(
            p01_risk_parity(1_000_000, 0.20, 1.0),
            {"MES": "06-26", "ZN": "06-26"},
            self.locked_risk_fx,
            intake_contract=IntakeRouteContract(
                PortfolioIntakeMode.DIRECT_DAILY_PRIMARY,
                SourceRuleStatus.LOCKED,
                SourceArtifactRef("docs/process/CARVER_P01_P02_PORTFOLIO_COMPLETION_RECORD_2026-05-29.md"),
            ),
            session_calendar=SessionCalendarSpec("P01/P02 session calendar", SourceRuleStatus.LOCKED, "UTC"),
            roll_rule=RollRuleSpec("P01/P02 roll rule", SourceRuleStatus.LOCKED),
            back_adjustment=BackAdjustmentSpec("P01/P02 back-adjustment rule", SourceRuleStatus.LOCKED),
        )

        self.assertIn("session calendar artifact is unresolved", report.blockers)
        self.assertIn("roll rule artifact is unresolved", report.blockers)
        self.assertIn("back-adjustment artifact is unresolved", report.blockers)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import sys
import unittest
from datetime import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import BackAdjustmentSpec, LaneClass, RollRuleSpec, SessionCalendarSpec, SourceRuleStatus, CarverBlocked  # noqa: E402
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402
from carver.spine.portfolio_completion import IntakeRouteContract, PortfolioIntakeMode, SourceArtifactRef  # noqa: E402
from carver.spine.portfolio_conformance import ProviderMappingStatus  # noqa: E402
from carver.spine.s09_readiness import (  # noqa: E402
    S09InstrumentDataContract,
    S09ReadinessStatus,
    build_s09_readiness_report,
    require_s09_real_data_readiness_preflight,
    s09_provider_mapping_status,
)


class S09ReadinessSyntheticTests(unittest.TestCase):
    def artifact(self) -> SourceArtifactRef:
        return SourceArtifactRef("docs/process/CARVER_S09_REAL_DATA_READINESS_GATE_2026-05-29.md")

    def locked_zn_contract(self) -> S09InstrumentDataContract:
        artifact = self.artifact()
        return S09InstrumentDataContract(
            contract=zn_contract(),
            contract_month="06-26",
            intake_contract=IntakeRouteContract(
                PortfolioIntakeMode.DIRECT_DAILY_PRIMARY,
                SourceRuleStatus.LOCKED,
                artifact,
            ),
            session_calendar=SessionCalendarSpec("S09 ZN session calendar", SourceRuleStatus.LOCKED, "UTC"),
            roll_rule=RollRuleSpec("S09 ZN roll rule", SourceRuleStatus.LOCKED),
            back_adjustment=BackAdjustmentSpec("S09 ZN back-adjustment rule", SourceRuleStatus.LOCKED),
            daily_price_risk_status=SourceRuleStatus.LOCKED,
            eligible_spans_status=SourceRuleStatus.LOCKED,
            eligible_spans=(32, 64),
            session_artifact=artifact,
            roll_artifact=artifact,
            back_adjustment_artifact=artifact,
            daily_price_risk_artifact=artifact,
            eligible_spans_artifact=artifact,
        )

    def test_provider_mapping_status_is_exact_and_no_es_for_mes(self) -> None:
        zn_row = s09_provider_mapping_status(zn_contract(), "06-26")
        self.assertEqual(zn_row.status, ProviderMappingStatus.LOCKED)
        self.assertEqual(zn_row.provider_symbol_id, "4470301")
        self.assertEqual(zn_row.display_symbol, "ZN JUN26")

        mes_row = s09_provider_mapping_status(mes_contract(), "06-26")
        self.assertEqual(mes_row.status, ProviderMappingStatus.UNRESOLVED)
        self.assertEqual(mes_row.display_symbol, "MES JUN26")
        self.assertIsNone(mes_row.provider_symbol_id)

    def test_default_s09_readiness_blocks_real_data_until_artifacts_are_locked(self) -> None:
        report = build_s09_readiness_report(S09InstrumentDataContract(mes_contract(), "06-26"))

        self.assertEqual(report.status, S09ReadinessStatus.SYNTHETIC_READY_REAL_DATA_BLOCKED)
        self.assertIn("provider mapping unresolved for MES 06-26", report.blockers)
        self.assertIn("session calendar is unresolved", report.blockers)
        self.assertIn("roll rule is unresolved", report.blockers)
        self.assertIn("back-adjustment rule is unresolved", report.blockers)
        self.assertIn("intake route contract is unresolved", report.blockers)
        self.assertIn("daily price-risk source is unresolved", report.blockers)
        self.assertIn("eligible EWMAC speed-set source is unresolved", report.blockers)
        with self.assertRaises(CarverBlocked):
            require_s09_real_data_readiness_preflight(report)

    def test_s09_readiness_can_be_ready_without_executing_data_when_all_artifacts_are_locked(self) -> None:
        report = build_s09_readiness_report(self.locked_zn_contract())

        self.assertEqual(report.status, S09ReadinessStatus.REAL_DATA_READY_NOT_EXECUTION_AUTHORIZATION)
        self.assertEqual(report.blockers, ())
        require_s09_real_data_readiness_preflight(report)

    def test_s09_readiness_requires_valid_eligible_speed_set_and_artifact(self) -> None:
        artifact = self.artifact()
        with self.assertRaises(CarverBlocked):
            build_s09_readiness_report(
                S09InstrumentDataContract(
                    contract=zn_contract(),
                    contract_month="06-26",
                    eligible_spans_status=SourceRuleStatus.LOCKED,
                    eligible_spans=(2, 64),
                    eligible_spans_artifact=artifact,
                )
            )

        missing_artifact = build_s09_readiness_report(
            S09InstrumentDataContract(
                contract=zn_contract(),
                contract_month="06-26",
                eligible_spans_status=SourceRuleStatus.LOCKED,
                eligible_spans=(64,),
            )
        )
        self.assertIn("eligible EWMAC speed-set source artifact is unresolved", missing_artifact.blockers)

    def test_minute_fallback_still_requires_direct_daily_blocked_artifact(self) -> None:
        artifact = self.artifact()
        with self.assertRaises(CarverBlocked):
            build_s09_readiness_report(
                S09InstrumentDataContract(
                    contract=zn_contract(),
                    contract_month="06-26",
                    intake_contract=IntakeRouteContract(
                        PortfolioIntakeMode.MINUTE_DERIVED_FALLBACK,
                        SourceRuleStatus.LOCKED,
                        artifact,
                    ),
                )
            )

        report = build_s09_readiness_report(
            S09InstrumentDataContract(
                contract=zn_contract(),
                contract_month="06-26",
                intake_contract=IntakeRouteContract(
                    PortfolioIntakeMode.MINUTE_DERIVED_FALLBACK,
                    SourceRuleStatus.LOCKED,
                    artifact,
                    direct_daily_blocked_artifact=artifact,
                ),
            )
        )
        self.assertNotIn("intake route contract is unresolved", report.blockers)

    def test_s09_readiness_rejects_non_source_native_lane_and_bad_month(self) -> None:
        with self.assertRaises(CarverBlocked):
            build_s09_readiness_report(
                S09InstrumentDataContract(
                    contract=zn_contract(),
                    contract_month="06-26",
                    lane_class=LaneClass.CFD_ADAPTER,
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_provider_mapping_status(zn_contract(), "2026-06")

    def test_gate_doc_records_non_authorization(self) -> None:
        text = (ROOT / "docs" / "process" / "CARVER_S09_REAL_DATA_READINESS_GATE_2026-05-29.md").read_text(encoding="utf-8")

        self.assertIn("DIRECT_DAILY_PRIMARY", text)
        self.assertIn("ZN 06-26 ZN JUN26 -> 4470301", text)
        self.assertIn("MES` remains unresolved", text)
        self.assertIn("authorizes no real data/API/WebSocket access", text)


if __name__ == "__main__":
    unittest.main()

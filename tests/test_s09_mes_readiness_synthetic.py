from __future__ import annotations

import hashlib
import json
import sys
import unittest
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from math import inf, nan
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked, CompletedBar, LaneClass, SourceRuleStatus  # noqa: E402
from carver.spine.m1 import TimedValue  # noqa: E402
from carver.spine.s09_mes_readiness import (  # noqa: E402
    S09MESAnnualRiskBlendRequest,
    S09MESCostComponentSetRequest,
    S09MESDailyPriceRiskRequest,
    S09MESDevelopmentReconciliationWindowRequest,
    S09MESExecutionPreflightRequest,
    S09MESLockedCostComponent,
    S09MESOldestAuthorizedDesignOrderingRequest,
    S09MESRiskAdjustedCostRequest,
    S09MESRiskAdjustedCostSpeedEligibilityRequest,
    S09MESStrategyInputReadinessGateConfig,
    S09MESStrategyInputReadinessRequest,
    evaluate_s09_mes_strategy_input_readiness,
    run_s09_mes_strategy_input_readiness_gate,
    s09_mes_annual_risk_from_locked_components,
    s09_mes_daily_price_risk_from_locked_inputs,
    s09_mes_development_reconciliation_window,
    s09_mes_execution_preflight,
    s09_mes_oldest_authorized_design_ordering,
    s09_mes_risk_adjusted_cost_from_locked_inputs,
    s09_mes_speed_eligibility_from_risk_adjusted_cost,
    s09_mes_total_cost_from_locked_components,
)


class S09MESReadinessSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.as_of = datetime(2022, 1, 3, tzinfo=timezone.utc)
        self.completed_bar = CompletedBar(self.as_of)

    def locked_request(self) -> S09MESStrategyInputReadinessRequest:
        return S09MESStrategyInputReadinessRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            root="MES",
            row_id="APPENDIX_C_174_006",
            expansion_status="PASS_S09_MES_DAILY_EXPANSION_QUARANTINE_ONLY_NOT_LINEAGE_NOT_BACKTEST",
            continuous_lineage_status=SourceRuleStatus.LOCKED,
            roll_plan_status=SourceRuleStatus.LOCKED,
            roll_date_normalization_status=SourceRuleStatus.LOCKED,
            back_adjustment_status=SourceRuleStatus.LOCKED,
            provider_condition_admission_status=SourceRuleStatus.LOCKED,
            oldest_authorized_data_ordering_status=SourceRuleStatus.LOCKED,
            development_reconciliation_window_status=SourceRuleStatus.LOCKED,
            annual_risk_runtime_status=SourceRuleStatus.LOCKED,
            daily_price_risk_runtime_status=SourceRuleStatus.LOCKED,
            cost_source_status=SourceRuleStatus.LOCKED,
            historical_cost_values_status=SourceRuleStatus.LOCKED,
            risk_adjusted_cost_status=SourceRuleStatus.LOCKED,
            speed_cost_eligibility_status=SourceRuleStatus.LOCKED,
            eligible_speed_set_status=SourceRuleStatus.LOCKED,
            table36_fdm_row_status=SourceRuleStatus.LOCKED,
            hash_bound_provenance_status=SourceRuleStatus.LOCKED,
            speed_eligibility_basis="LOCKED_COST_SCREEN_0_15_SR_THRESHOLD",
            eligible_spans=(16, 32, 64),
            fdm=1.08,
        )

    def test_mes_readiness_passes_only_after_all_components_are_locked(self) -> None:
        result = evaluate_s09_mes_strategy_input_readiness(self.locked_request())

        self.assertTrue(result.ready)
        self.assertEqual(result.root, "MES")
        self.assertEqual(result.eligible_spans, (16, 32, 64))
        self.assertEqual(result.fdm, 1.08)
        self.assertEqual(result.readiness_status, "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY")
        self.assertEqual(result.blockers, ())

    def test_mes_readiness_fails_closed_on_unresolved_component_or_wrong_fdm(self) -> None:
        unresolved_cost = replace(self.locked_request(), cost_source_status=SourceRuleStatus.UNRESOLVED)
        with self.assertRaises(CarverBlocked):
            evaluate_s09_mes_strategy_input_readiness(unresolved_cost)

        wrong_fdm = replace(self.locked_request(), fdm=1.26)
        with self.assertRaises(CarverBlocked):
            evaluate_s09_mes_strategy_input_readiness(wrong_fdm)

    def test_mes_readiness_requires_every_component_lock(self) -> None:
        status_fields = (
            "continuous_lineage_status",
            "roll_plan_status",
            "roll_date_normalization_status",
            "back_adjustment_status",
            "provider_condition_admission_status",
            "oldest_authorized_data_ordering_status",
            "development_reconciliation_window_status",
            "annual_risk_runtime_status",
            "daily_price_risk_runtime_status",
            "cost_source_status",
            "historical_cost_values_status",
            "risk_adjusted_cost_status",
            "speed_cost_eligibility_status",
            "eligible_speed_set_status",
            "table36_fdm_row_status",
            "hash_bound_provenance_status",
        )
        for field in status_fields:
            with self.subTest(field=field):
                request = replace(self.locked_request(), **{field: SourceRuleStatus.UNRESOLVED})
                with self.assertRaises(CarverBlocked):
                    evaluate_s09_mes_strategy_input_readiness(request)

    def test_mes_readiness_rejects_substitution_and_silent_speed_assumption(self) -> None:
        with self.assertRaises(CarverBlocked):
            evaluate_s09_mes_strategy_input_readiness(replace(self.locked_request(), root="ES"))
        with self.assertRaises(CarverBlocked):
            evaluate_s09_mes_strategy_input_readiness(replace(self.locked_request(), row_id="APPENDIX_C_174_002"))
        with self.assertRaises(CarverBlocked):
            evaluate_s09_mes_strategy_input_readiness(replace(self.locked_request(), speed_eligibility_basis="ASSUMED_ALL_SIX_SPEEDS"))
        with self.assertRaises(CarverBlocked):
            evaluate_s09_mes_strategy_input_readiness(replace(self.locked_request(), lane_class=LaneClass.CFD_ADAPTER))

    def test_mes_readiness_allows_locked_all_six_speed_set_when_not_assumed(self) -> None:
        result = evaluate_s09_mes_strategy_input_readiness(
            replace(
                self.locked_request(),
                eligible_spans=(2, 4, 8, 16, 32, 64),
                fdm=1.26,
                speed_eligibility_basis="LOCKED_COST_SCREEN_ALL_SIX_SPEEDS_SURVIVE",
            )
        )

        self.assertTrue(result.ready)
        self.assertEqual(result.eligible_spans, (2, 4, 8, 16, 32, 64))
        self.assertEqual(result.fdm, 1.26)

    def test_mes_readiness_does_not_reject_non_assumption_label(self) -> None:
        result = evaluate_s09_mes_strategy_input_readiness(
            replace(self.locked_request(), speed_eligibility_basis="NON_ASSUMPTION_COST_SCREEN_LOCKED")
        )

        self.assertTrue(result.ready)

    def test_mes_annual_risk_blends_locked_long_run_and_ewma32_current_risk(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESAnnualRiskBlendRequest as ExportedRequest,
            s09_mes_annual_risk_from_locked_components as exported_helper,
        )

        self.assertIs(ExportedRequest, S09MESAnnualRiskBlendRequest)
        self.assertIs(exported_helper, s09_mes_annual_risk_from_locked_components)

        result = s09_mes_annual_risk_from_locked_components(
            S09MESAnnualRiskBlendRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                completed_bar=self.completed_bar,
                long_run_annual_risk=TimedValue(0.20, self.as_of),
                long_run_status=SourceRuleStatus.LOCKED,
                current_ewma32_annual_risk=TimedValue(0.10, self.as_of),
                current_risk_status=SourceRuleStatus.LOCKED,
                blend_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(result.as_of, self.as_of)
        self.assertAlmostEqual(result.annual_percentage_risk, 0.13)
        self.assertEqual(result.long_run_weight, 0.30)
        self.assertEqual(result.current_risk_weight, 0.70)
        self.assertEqual(result.blend_basis, "LOCKED_30_70_LONG_RUN_CURRENT_EWMA32_ANNUAL_PERCENTAGE_RISK")
        self.assertTrue(result.ready_for_daily_price_risk)

    def test_mes_annual_risk_blend_fails_closed_without_locked_source_components(self) -> None:
        base = S09MESAnnualRiskBlendRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            completed_bar=self.completed_bar,
            long_run_annual_risk=TimedValue(0.20, self.as_of),
            long_run_status=SourceRuleStatus.LOCKED,
            current_ewma32_annual_risk=TimedValue(0.10, self.as_of),
            current_risk_status=SourceRuleStatus.LOCKED,
            blend_status=SourceRuleStatus.LOCKED,
        )

        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, long_run_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, current_risk_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, blend_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, long_run_annual_risk=TimedValue(0.20, self.as_of - timedelta(days=1))))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, current_ewma32_annual_risk=TimedValue(0.10, self.as_of - timedelta(days=1))))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, ewma_span=16))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, ewma_span=True))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, ewma_span=32.0))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, long_run_weight=0.50, current_risk_weight=0.50))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, long_run_weight=True))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, current_risk_weight=nan))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, long_run_weight=0.30, current_risk_weight=0.60))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, long_run_annual_risk=TimedValue(0.0, self.as_of)))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, current_ewma32_annual_risk=TimedValue(nan, self.as_of)))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, long_run_annual_risk=TimedValue(inf, self.as_of)))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, current_ewma32_annual_risk=TimedValue("0.10", self.as_of)))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, completed_bar=CompletedBar(self.as_of, is_complete=False)))
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(
                replace(
                    base,
                    completed_bar=CompletedBar(datetime(2022, 1, 3)),
                    long_run_annual_risk=TimedValue(0.20, datetime(2022, 1, 3)),
                    current_ewma32_annual_risk=TimedValue(0.10, datetime(2022, 1, 3)),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(
                replace(
                    base,
                    completed_bar=CompletedBar(datetime(2022, 1, 3, 12, tzinfo=timezone.utc)),
                    long_run_annual_risk=TimedValue(0.20, datetime(2022, 1, 3, 12, tzinfo=timezone.utc)),
                    current_ewma32_annual_risk=TimedValue(0.10, datetime(2022, 1, 3, 12, tzinfo=timezone.utc)),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_mes_annual_risk_from_locked_components(replace(base, lane_class=LaneClass.CFD_ADAPTER))

    def test_mes_oldest_authorized_design_ordering_requires_earliest_completed_dates_first(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESOldestAuthorizedDesignOrderingRequest as ExportedRequest,
            s09_mes_oldest_authorized_design_ordering as exported_helper,
        )

        self.assertIs(ExportedRequest, S09MESOldestAuthorizedDesignOrderingRequest)
        self.assertIs(exported_helper, s09_mes_oldest_authorized_design_ordering)

        result = s09_mes_oldest_authorized_design_ordering(
            S09MESOldestAuthorizedDesignOrderingRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                root="MES",
                row_id="APPENDIX_C_174_006",
                authorized_completed_dates=(
                    date(2022, 1, 3),
                    date(2022, 1, 4),
                    date(2022, 1, 5),
                ),
                admitted_completed_dates=(
                    date(2022, 1, 3),
                    date(2022, 1, 4),
                ),
                authorization_status=SourceRuleStatus.LOCKED,
                provenance_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(result.first_authorized_completed_date, date(2022, 1, 3))
        self.assertEqual(result.first_admitted_completed_date, date(2022, 1, 3))
        self.assertEqual(result.admitted_completed_dates, (date(2022, 1, 3), date(2022, 1, 4)))
        self.assertEqual(result.ordering_basis, "LOCKED_OLDEST_AUTHORIZED_COMPLETED_SOURCE_NATIVE_DATA_FIRST")
        self.assertTrue(result.ready_for_runtime_gate)

    def test_mes_oldest_authorized_design_ordering_fails_closed_on_newer_start_or_gaps(self) -> None:
        base = S09MESOldestAuthorizedDesignOrderingRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            root="MES",
            row_id="APPENDIX_C_174_006",
            authorized_completed_dates=(
                date(2022, 1, 3),
                date(2022, 1, 4),
                date(2022, 1, 5),
            ),
            admitted_completed_dates=(
                date(2022, 1, 3),
                date(2022, 1, 4),
            ),
            authorization_status=SourceRuleStatus.LOCKED,
            provenance_status=SourceRuleStatus.LOCKED,
        )

        hostile_requests = (
            replace(base, admitted_completed_dates=(date(2022, 1, 4), date(2022, 1, 5))),
            replace(base, admitted_completed_dates=(date(2022, 1, 3), date(2022, 1, 5))),
            replace(base, admitted_completed_dates=(date(2022, 1, 3), date(2022, 1, 3))),
            replace(base, admitted_completed_dates=(datetime(2022, 1, 3, tzinfo=timezone.utc),)),
            replace(base, authorized_completed_dates=(date(2022, 1, 4), date(2022, 1, 3))),
            replace(base, admitted_completed_dates=(date(2022, 1, 2),)),
            replace(base, admitted_completed_dates=()),
            replace(base, authorization_status=SourceRuleStatus.UNRESOLVED),
            replace(base, provenance_status=SourceRuleStatus.UNRESOLVED),
            replace(base, root="ES"),
            replace(base, row_id="APPENDIX_C_174_002"),
            replace(base, lane_class=LaneClass.CFD_ADAPTER),
        )
        for request in hostile_requests:
            with self.subTest(request=request):
                with self.assertRaises(CarverBlocked):
                    s09_mes_oldest_authorized_design_ordering(request)

    def test_mes_development_reconciliation_window_locks_oldest_authorized_dev_only_window(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESDevelopmentReconciliationWindowRequest as ExportedRequest,
            s09_mes_development_reconciliation_window as exported_helper,
        )

        self.assertIs(ExportedRequest, S09MESDevelopmentReconciliationWindowRequest)
        self.assertIs(exported_helper, s09_mes_development_reconciliation_window)

        result = s09_mes_development_reconciliation_window(
            S09MESDevelopmentReconciliationWindowRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                root="MES",
                row_id="APPENDIX_C_174_006",
                phase_label="DEVELOPMENT_RECONCILIATION",
                authorized_completed_dates=(
                    date(2022, 1, 3),
                    date(2022, 1, 4),
                    date(2022, 1, 5),
                ),
                window_completed_dates=(
                    date(2022, 1, 3),
                    date(2022, 1, 4),
                ),
                window_status=SourceRuleStatus.LOCKED,
                authorization_status=SourceRuleStatus.LOCKED,
                provenance_status=SourceRuleStatus.LOCKED,
                oldest_authorized_data_ordering_status=SourceRuleStatus.LOCKED,
                no_oos_lockbox_forward_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(result.window_start, date(2022, 1, 3))
        self.assertEqual(result.window_end, date(2022, 1, 4))
        self.assertEqual(result.completed_dates, (date(2022, 1, 3), date(2022, 1, 4)))
        self.assertEqual(result.window_span_days, 1)
        self.assertEqual(result.window_basis, "LOCKED_S09_MES_DEV_RECON_OLDEST_AUTHORIZED_SOURCE_NATIVE_COMPLETED_DATES")
        self.assertTrue(result.ready_for_readiness_gate)

    def test_mes_development_reconciliation_window_fails_closed_on_scope_drift(self) -> None:
        base = S09MESDevelopmentReconciliationWindowRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            root="MES",
            row_id="APPENDIX_C_174_006",
            phase_label="DEVELOPMENT_RECONCILIATION",
            authorized_completed_dates=(
                date(2022, 1, 3),
                date(2022, 1, 4),
                date(2022, 1, 5),
                date(2024, 1, 5),
            ),
            window_completed_dates=(
                date(2022, 1, 3),
                date(2022, 1, 4),
            ),
            window_status=SourceRuleStatus.LOCKED,
            authorization_status=SourceRuleStatus.LOCKED,
            provenance_status=SourceRuleStatus.LOCKED,
            oldest_authorized_data_ordering_status=SourceRuleStatus.LOCKED,
            no_oos_lockbox_forward_status=SourceRuleStatus.LOCKED,
        )

        hostile_requests = (
            replace(base, phase_label="TEST"),
            replace(base, phase_label="LOCKBOX"),
            replace(base, window_completed_dates=(date(2022, 1, 4), date(2022, 1, 5))),
            replace(base, window_completed_dates=(date(2022, 1, 3), date(2022, 1, 5))),
            replace(base, window_completed_dates=(date(2022, 1, 3), date(2024, 1, 5))),
            replace(base, window_completed_dates=(datetime(2022, 1, 3, tzinfo=timezone.utc),)),
            replace(base, authorized_completed_dates=(date(2022, 1, 4), date(2022, 1, 3))),
            replace(base, window_completed_dates=()),
            replace(base, window_status=SourceRuleStatus.UNRESOLVED),
            replace(base, authorization_status=SourceRuleStatus.UNRESOLVED),
            replace(base, provenance_status=SourceRuleStatus.UNRESOLVED),
            replace(base, oldest_authorized_data_ordering_status=SourceRuleStatus.UNRESOLVED),
            replace(base, no_oos_lockbox_forward_status=SourceRuleStatus.UNRESOLVED),
            replace(base, root="ES"),
            replace(base, row_id="APPENDIX_C_174_002"),
            replace(base, lane_class=LaneClass.CFD_ADAPTER),
        )
        for request in hostile_requests:
            with self.subTest(request=request):
                with self.assertRaises(CarverBlocked):
                    s09_mes_development_reconciliation_window(request)

    def test_mes_execution_preflight_is_process_only_authorization_request_ready(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESExecutionPreflightRequest as ExportedRequest,
            s09_mes_execution_preflight as exported_helper,
        )

        self.assertIs(ExportedRequest, S09MESExecutionPreflightRequest)
        self.assertIs(exported_helper, s09_mes_execution_preflight)

        result = s09_mes_execution_preflight(
            S09MESExecutionPreflightRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                root="MES",
                row_id="APPENDIX_C_174_006",
                gate_name="S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE",
                process_gate_status="PROCESS_ONLY_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_GATE_NOT_EXECUTION",
                oldest_authorized_completed_date=date(2022, 1, 3),
                target_completed_date_start=date(2022, 1, 3),
                target_completed_date_end=date(2023, 12, 29),
                development_reconciliation_window_status=SourceRuleStatus.LOCKED,
                oldest_authorized_data_ordering_status=SourceRuleStatus.LOCKED,
                no_data_execution_status=SourceRuleStatus.LOCKED,
                no_backtest_status=SourceRuleStatus.LOCKED,
                no_oos_lockbox_forward_status=SourceRuleStatus.LOCKED,
                no_cfd_quantlab_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(
            result.preflight_status,
            "READY_FOR_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_AUTHORIZATION_REQUEST_NOT_EXECUTION",
        )
        self.assertEqual(result.window_start, date(2022, 1, 3))
        self.assertEqual(result.window_end, date(2023, 12, 29))
        self.assertEqual(result.window_span_days, 725)
        self.assertTrue(result.ready_for_authorization_request)

    def test_mes_execution_preflight_fails_closed_on_stage_or_scope_drift(self) -> None:
        base = S09MESExecutionPreflightRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            root="MES",
            row_id="APPENDIX_C_174_006",
            gate_name="S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE",
            process_gate_status="PROCESS_ONLY_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_GATE_NOT_EXECUTION",
            oldest_authorized_completed_date=date(2022, 1, 3),
            target_completed_date_start=date(2022, 1, 3),
            target_completed_date_end=date(2023, 12, 29),
            development_reconciliation_window_status=SourceRuleStatus.LOCKED,
            oldest_authorized_data_ordering_status=SourceRuleStatus.LOCKED,
            no_data_execution_status=SourceRuleStatus.LOCKED,
            no_backtest_status=SourceRuleStatus.LOCKED,
            no_oos_lockbox_forward_status=SourceRuleStatus.LOCKED,
            no_cfd_quantlab_status=SourceRuleStatus.LOCKED,
        )

        hostile_requests = (
            replace(base, lane_class=LaneClass.CFD_ADAPTER),
            replace(base, root="ES"),
            replace(base, row_id="APPENDIX_C_174_002"),
            replace(base, gate_name="S09_MES_LOCKBOX_GATE"),
            replace(base, process_gate_status="READY_FOR_BACKTEST"),
            replace(base, oldest_authorized_completed_date=date(2022, 1, 4)),
            replace(base, target_completed_date_start=date(2022, 1, 4)),
            replace(base, target_completed_date_end=date(2024, 1, 5)),
            replace(base, target_completed_date_start=datetime(2022, 1, 3, tzinfo=timezone.utc)),
            replace(base, development_reconciliation_window_status=SourceRuleStatus.UNRESOLVED),
            replace(base, oldest_authorized_data_ordering_status=SourceRuleStatus.UNRESOLVED),
            replace(base, no_data_execution_status=SourceRuleStatus.UNRESOLVED),
            replace(base, no_backtest_status=SourceRuleStatus.UNRESOLVED),
            replace(base, no_oos_lockbox_forward_status=SourceRuleStatus.UNRESOLVED),
            replace(base, no_cfd_quantlab_status=SourceRuleStatus.UNRESOLVED),
        )
        for request in hostile_requests:
            with self.subTest(request=request):
                with self.assertRaises(CarverBlocked):
                    s09_mes_execution_preflight(request)

    def test_mes_strategy_input_readiness_gate_preflight_requires_evidence_handoff_and_blocks_backtest(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESStrategyInputReadinessGateConfig as ExportedConfig,
            run_s09_mes_strategy_input_readiness_gate as exported_helper,
        )

        self.assertIs(ExportedConfig, S09MESStrategyInputReadinessGateConfig)
        self.assertIs(exported_helper, run_s09_mes_strategy_input_readiness_gate)

        base = S09MESStrategyInputReadinessGateConfig(
            execution_authorized=True,
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            root="MES",
            row_id="APPENDIX_C_174_006",
            evidence_completion_status="LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION",
            evidence_handoff_status="S09_MES_EVIDENCE_COMPLETION_HANDOFF_READY_FOR_READINESS_GATE_NOT_BACKTEST",
            strategy_input_readiness_status="S09_MES_STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_GATE",
            next_gate="S09_MES_STRATEGY_INPUT_READINESS_GATE",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )

        result = run_s09_mes_strategy_input_readiness_gate(base)

        self.assertEqual(result["status"], "AUTHORIZED_READINESS_PREFLIGHT_ONLY_NOT_EXECUTED")
        self.assertEqual(result["gate"], "S09_MES_STRATEGY_INPUT_READINESS_GATE")
        self.assertEqual(result["lane_class"], "SOURCE_NATIVE_FUTURES")
        self.assertEqual(result["root"], "MES")
        self.assertEqual(result["row_id"], "APPENDIX_C_174_006")
        self.assertEqual(
            result["evidence_completion_status"],
            "LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION",
        )
        self.assertEqual(
            result["strategy_input_readiness_status"],
            "S09_MES_STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_GATE",
        )
        self.assertEqual(result["databento_api_access"], "NO")
        self.assertEqual(result["market_row_parsing"], "NO")
        self.assertEqual(result["forecast_computation"], "NO")
        self.assertEqual(result["diagnostics_run"], "NO")
        self.assertEqual(result["backtests_run"], "NO")
        self.assertEqual(result["test_validation_lockbox_forward_access"], "NO")

        hostile_configs = (
            replace(base, execution_authorized=False),
            replace(base, lane_class=LaneClass.CFD_ADAPTER),
            replace(base, root="ES"),
            replace(base, row_id="APPENDIX_C_174_002"),
            replace(base, evidence_completion_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY"),
            replace(base, evidence_handoff_status="READY_FOR_BACKTEST"),
            replace(base, strategy_input_readiness_status="S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY"),
            replace(base, next_gate="S09_MES_DEV_RECON_BACKTEST_GATE"),
            replace(base, machinery_development_slice="2022-01-03 through 2023-12-29"),
            replace(base, databento_api_access_authorized=True),
            replace(base, market_row_parsing_authorized=True),
            replace(base, forecast_computation_authorized=True),
            replace(base, diagnostics_authorized=True),
            replace(base, backtest_authorized=True),
            replace(base, test_validation_lockbox_forward_authorized=True),
        )
        for config in hostile_configs:
            with self.subTest(config=config):
                with self.assertRaises(CarverBlocked):
                    run_s09_mes_strategy_input_readiness_gate(config)

    def test_mes_strategy_input_readiness_gate_executor_writes_ready_dev_recon_only_packet(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_readiness_gate import (  # noqa: PLC0415
            HASH_PATH,
            RESULT_PATH,
            STATUS_PATH,
            S09MESStrategyInputReadinessGateExecutionConfig,
            build_readiness_manifest_payload,
            run_strategy_input_readiness_gate_guard,
        )

        base = S09MESStrategyInputReadinessGateExecutionConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            evidence_status_path=(
                ROOT
                / "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/"
                "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json"
            ),
            evidence_hash_path=(
                ROOT
                / "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/hashes/"
                "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt"
            ),
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
            git_operations_authorized=False,
        )

        result = run_strategy_input_readiness_gate_guard(base)
        manifest = build_readiness_manifest_payload(base)
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        result_text = RESULT_PATH.read_text(encoding="utf-8")
        hashes = HASH_PATH.read_text(encoding="utf-8")
        combined = "\n".join((json.dumps(manifest, sort_keys=True), json.dumps(status, sort_keys=True), result_text, hashes))

        self.assertEqual(result["status"], "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY_NOT_BACKTEST_AUTHORIZATION")
        self.assertEqual(result["spine_status"], "AUTHORIZED_READINESS_PREFLIGHT_ONLY_NOT_EXECUTED")
        self.assertEqual(result["next_gate"], "S09_MES_FIRST_DEV_RECON_BACKTEST_AUTHORIZATION_GATE")
        self.assertEqual(manifest["strategy_input_readiness_status"], "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(status["status"], "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY_NOT_BACKTEST_AUTHORIZATION")
        self.assertEqual(status["first_backtest_authorization_required"], "YES")
        self.assertEqual(status["next_gate"], "S09_MES_FIRST_DEV_RECON_BACKTEST_AUTHORIZATION_GATE")
        self.assertEqual(status["forecast_computation"], "NO")
        self.assertEqual(status["diagnostics_run"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertEqual(status["git_operations"], "NO")
        self.assertIn("20260603_S09_MES_STRATEGY_INPUT_READINESS_status.json", hashes)
        self.assertNotIn("/hashes/", hashes)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

        hostile_configs = (
            replace(base, execution_authorized=False),
            replace(base, lane_class="CFD_ADAPTER"),
            replace(base, root="ES"),
            replace(base, row_id="APPENDIX_C_174_002"),
            replace(base, machinery_development_slice="2022-01-03 through 2023-12-29"),
            replace(base, evidence_status_path=ROOT / "missing_status.json"),
            replace(base, evidence_hash_path=ROOT / "missing_hash.txt"),
            replace(base, databento_api_access_authorized=True),
            replace(base, market_row_parsing_authorized=True),
            replace(base, forecast_computation_authorized=True),
            replace(base, diagnostics_authorized=True),
            replace(base, backtest_authorized=True),
            replace(base, test_validation_lockbox_forward_authorized=True),
            replace(base, git_operations_authorized=True),
        )
        for config in hostile_configs:
            with self.subTest(config=config):
                with self.assertRaises(CarverBlocked):
                    run_strategy_input_readiness_gate_guard(config)

        for line in hashes.splitlines():
            if not line.strip():
                continue
            expected_hash, relative_path = line.split("  ", 1)
            self.assertNotIn("/hashes/", relative_path)
            actual_hash = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest().upper()
            self.assertEqual(actual_hash, expected_hash)

    def roll_risk_cost_manifest_artifacts(self, artifact_schema):
        return (
            artifact_schema(
                relative_path="roll_date_normalization/<STAMP>_S09_MES_ROLL_DATE_NORMALIZATION_ledger.csv",
                fields=(
                    "provider_date",
                    "completed_trading_date",
                    "old_symbol",
                    "new_symbol",
                    "authority_source",
                    "authority_sha256",
                    "status",
                ),
                status=SourceRuleStatus.LOCKED,
            ),
            artifact_schema(
                relative_path="risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
                fields=(
                    "completed_trading_date",
                    "long_run_annual_risk",
                    "current_ewma32_annual_risk",
                    "annual_percentage_risk",
                    "source_sha256",
                    "status",
                ),
                status=SourceRuleStatus.LOCKED,
            ),
            artifact_schema(
                relative_path="risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv",
                fields=(
                    "completed_trading_date",
                    "current_price",
                    "annual_percentage_risk",
                    "daily_price_risk_currency",
                    "source_sha256",
                    "status",
                ),
                status=SourceRuleStatus.LOCKED,
            ),
            artifact_schema(
                relative_path="cost/<STAMP>_S09_MES_COST_VALUE_ledger.csv",
                fields=(
                    "completed_trading_date",
                    "component_name",
                    "amount_currency",
                    "currency",
                    "charge_timing",
                    "effective_start",
                    "effective_end",
                    "source_label",
                    "source_sha256",
                    "status",
                ),
                status=SourceRuleStatus.LOCKED,
            ),
            artifact_schema(
                relative_path="cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv",
                fields=(
                    "completed_trading_date",
                    "total_cost_per_trade_currency",
                    "daily_price_risk_currency",
                    "risk_adjusted_cost_per_trade_sr",
                    "status",
                ),
                status=SourceRuleStatus.LOCKED,
            ),
            artifact_schema(
                relative_path="speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv",
                fields=(
                    "span",
                    "turnover",
                    "risk_adjusted_cost_per_trade_sr",
                    "threshold_sr",
                    "eligible",
                    "status",
                ),
                status=SourceRuleStatus.LOCKED,
            ),
            artifact_schema(
                relative_path="status/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_status.json",
                fields=(
                    "status",
                    "databento_api_access",
                    "new_provider_data_download",
                    "market_row_parsing",
                    "strategy_input_readiness_status",
                ),
                status=SourceRuleStatus.LOCKED,
            ),
            artifact_schema(
                relative_path="provenance/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_provenance.md",
                fields=("scope", "inputs", "non_authorization", "oldest_authorized_ordering"),
                status=SourceRuleStatus.LOCKED,
            ),
            artifact_schema(
                relative_path="hashes/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_sha256.txt",
                fields=("sha256", "relative_path"),
                status=SourceRuleStatus.LOCKED,
            ),
        )

    def test_mes_roll_risk_cost_execution_output_manifest_locks_expected_artifact_contract(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESRollRiskCostExecutionArtifactSchema as ExportedArtifactSchema,
            S09MESRollRiskCostExecutionOutputManifestRequest as ExportedRequest,
            s09_mes_roll_risk_cost_execution_output_manifest as exported_helper,
        )
        from carver.spine.s09_mes_readiness import (  # noqa: PLC0415
            S09MESRollRiskCostExecutionArtifactSchema,
            S09MESRollRiskCostExecutionOutputManifestRequest,
            s09_mes_roll_risk_cost_execution_output_manifest,
        )

        self.assertIs(ExportedArtifactSchema, S09MESRollRiskCostExecutionArtifactSchema)
        self.assertIs(ExportedRequest, S09MESRollRiskCostExecutionOutputManifestRequest)
        self.assertIs(exported_helper, s09_mes_roll_risk_cost_execution_output_manifest)

        result = s09_mes_roll_risk_cost_execution_output_manifest(
            S09MESRollRiskCostExecutionOutputManifestRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                root="MES",
                row_id="APPENDIX_C_174_006",
                gate_name="S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE",
                output_root=(
                    "docs/researchops/s09/mes_roll_date_normalization_runtime_risk_cost_execution/"
                    "2022-01-03_2023-12-29"
                ),
                artifact_schemas=self.roll_risk_cost_manifest_artifacts(S09MESRollRiskCostExecutionArtifactSchema),
                manifest_status=SourceRuleStatus.LOCKED,
                authorization_request_status=SourceRuleStatus.LOCKED,
                no_execution_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(
            result.manifest_status,
            "S09_MES_ROLL_RISK_COST_EXECUTION_OUTPUT_MANIFEST_READY_NOT_EXECUTION",
        )
        self.assertEqual(
            result.output_root,
            "docs/researchops/s09/mes_roll_date_normalization_runtime_risk_cost_execution/2022-01-03_2023-12-29",
        )
        self.assertEqual(len(result.artifact_schemas), 9)
        self.assertTrue(result.ready_for_authorized_runner_contract)

    def test_mes_roll_risk_cost_execution_output_manifest_fails_closed_on_contract_drift(self) -> None:
        from carver.spine.s09_mes_readiness import (  # noqa: PLC0415
            S09MESRollRiskCostExecutionArtifactSchema,
            S09MESRollRiskCostExecutionOutputManifestRequest,
            s09_mes_roll_risk_cost_execution_output_manifest,
        )

        artifacts = self.roll_risk_cost_manifest_artifacts(S09MESRollRiskCostExecutionArtifactSchema)
        base = S09MESRollRiskCostExecutionOutputManifestRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            root="MES",
            row_id="APPENDIX_C_174_006",
            gate_name="S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE",
            output_root=(
                "docs/researchops/s09/mes_roll_date_normalization_runtime_risk_cost_execution/"
                "2022-01-03_2023-12-29"
            ),
            artifact_schemas=artifacts,
            manifest_status=SourceRuleStatus.LOCKED,
            authorization_request_status=SourceRuleStatus.LOCKED,
            no_execution_status=SourceRuleStatus.LOCKED,
        )

        hostile_requests = (
            replace(base, lane_class=LaneClass.CFD_ADAPTER),
            replace(base, root="ES"),
            replace(base, row_id="APPENDIX_C_174_002"),
            replace(base, gate_name="S09_MES_LOCKBOX_GATE"),
            replace(base, output_root="docs/researchops/s09/mes_roll_date_normalization_runtime_risk_cost_execution/2023-01-03_2024-12-31"),
            replace(base, artifact_schemas=artifacts[:-1]),
            replace(base, artifact_schemas=artifacts + (artifacts[-1],)),
            replace(
                base,
                artifact_schemas=(replace(artifacts[0], fields=artifacts[0].fields[:-1]),) + artifacts[1:],
            ),
            replace(base, artifact_schemas=(replace(artifacts[0], relative_path=""),) + artifacts[1:]),
            replace(base, artifact_schemas=(replace(artifacts[0], status=SourceRuleStatus.UNRESOLVED),) + artifacts[1:]),
            replace(base, manifest_status=SourceRuleStatus.UNRESOLVED),
            replace(base, authorization_request_status=SourceRuleStatus.UNRESOLVED),
            replace(base, no_execution_status=SourceRuleStatus.UNRESOLVED),
        )
        for request in hostile_requests:
            with self.subTest(request=request):
                with self.assertRaises(CarverBlocked):
                    s09_mes_roll_risk_cost_execution_output_manifest(request)

    def test_mes_daily_price_risk_uses_locked_current_price_and_annual_risk(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESDailyPriceRiskRequest as ExportedRequest,
            s09_mes_daily_price_risk_from_locked_inputs as exported_helper,
        )

        self.assertIs(ExportedRequest, S09MESDailyPriceRiskRequest)
        self.assertIs(exported_helper, s09_mes_daily_price_risk_from_locked_inputs)

        result = s09_mes_daily_price_risk_from_locked_inputs(
            S09MESDailyPriceRiskRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                completed_bar=self.completed_bar,
                current_price=TimedValue(4000.0, self.as_of),
                current_price_status=SourceRuleStatus.LOCKED,
                annual_percentage_risk=TimedValue(0.16, self.as_of),
                annual_risk_runtime_status=SourceRuleStatus.LOCKED,
                conversion_source_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(result.daily_price_risk_currency, 40.0)
        self.assertEqual(result.as_of, self.as_of)
        self.assertEqual(result.conversion_basis, "LOCKED_CURRENT_PRICE_TIMES_LOCKED_ANNUAL_PERCENTAGE_RISK_OVER_16")
        self.assertTrue(result.ready_for_risk_adjusted_cost)

    def test_mes_daily_price_risk_fails_closed_without_locked_aligned_inputs(self) -> None:
        base = S09MESDailyPriceRiskRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            completed_bar=self.completed_bar,
            current_price=TimedValue(4000.0, self.as_of),
            current_price_status=SourceRuleStatus.LOCKED,
            annual_percentage_risk=TimedValue(0.16, self.as_of),
            annual_risk_runtime_status=SourceRuleStatus.LOCKED,
            conversion_source_status=SourceRuleStatus.LOCKED,
        )

        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, current_price_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, annual_risk_runtime_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, conversion_source_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, current_price=TimedValue(4000.0, self.as_of - timedelta(days=1))))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, annual_percentage_risk=TimedValue(0.16, self.as_of - timedelta(days=1))))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, annualization_days=252))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, annualization_days=True))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, annualization_days=16.0))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, completed_bar=CompletedBar(self.as_of, is_complete=False)))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(
                replace(
                    base,
                    completed_bar=CompletedBar(datetime(2022, 1, 3)),
                    current_price=TimedValue(4000.0, datetime(2022, 1, 3)),
                    annual_percentage_risk=TimedValue(0.16, datetime(2022, 1, 3)),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(
                replace(
                    base,
                    completed_bar=CompletedBar(datetime(2022, 1, 3, 12, tzinfo=timezone.utc)),
                    current_price=TimedValue(4000.0, datetime(2022, 1, 3, 12, tzinfo=timezone.utc)),
                    annual_percentage_risk=TimedValue(0.16, datetime(2022, 1, 3, 12, tzinfo=timezone.utc)),
                )
            )
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, current_price=TimedValue(0.0, self.as_of)))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, annual_percentage_risk=TimedValue(nan, self.as_of)))
        with self.assertRaises(CarverBlocked):
            s09_mes_daily_price_risk_from_locked_inputs(replace(base, lane_class=LaneClass.CFD_ADAPTER))

    def test_mes_runtime_risk_values_require_same_completed_bar_timestamp(self) -> None:
        annual = s09_mes_annual_risk_from_locked_components(
            S09MESAnnualRiskBlendRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                completed_bar=self.completed_bar,
                long_run_annual_risk=TimedValue(0.20, self.as_of),
                long_run_status=SourceRuleStatus.LOCKED,
                current_ewma32_annual_risk=TimedValue(0.10, self.as_of),
                current_risk_status=SourceRuleStatus.LOCKED,
                blend_status=SourceRuleStatus.LOCKED,
            )
        )
        daily = s09_mes_daily_price_risk_from_locked_inputs(
            S09MESDailyPriceRiskRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                completed_bar=self.completed_bar,
                current_price=TimedValue(4000.0, self.as_of),
                current_price_status=SourceRuleStatus.LOCKED,
                annual_percentage_risk=TimedValue(annual.annual_percentage_risk, self.as_of),
                annual_risk_runtime_status=SourceRuleStatus.LOCKED,
                conversion_source_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(daily.daily_price_risk_currency, 32.5)

    def test_mes_runtime_risk_ledger_renderers_output_locked_source_native_values(self) -> None:
        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESAnnualRiskRuntimeLedgerRow,
            S09MESDailyPriceRiskRuntimeLedgerRow,
            render_s09_mes_annual_risk_runtime_ledger_csv,
            render_s09_mes_daily_price_risk_runtime_ledger_csv,
        )

        annual_csv = render_s09_mes_annual_risk_runtime_ledger_csv(
            (
                S09MESAnnualRiskRuntimeLedgerRow(
                    completed_trading_date=date(2022, 1, 3),
                    long_run_annual_risk=0.20,
                    current_ewma32_annual_risk=0.10,
                    annual_percentage_risk=0.13,
                    source_sha256="B" * 64,
                    status="LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE",
                ),
            )
        )
        daily_csv = render_s09_mes_daily_price_risk_runtime_ledger_csv(
            (
                S09MESDailyPriceRiskRuntimeLedgerRow(
                    completed_trading_date=date(2022, 1, 3),
                    current_price=4000.0,
                    annual_percentage_risk=0.13,
                    daily_price_risk_currency=32.5,
                    source_sha256="C" * 64,
                    status="LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE",
                ),
            )
        )

        self.assertEqual(
            annual_csv,
            (
                "completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,"
                "annual_percentage_risk,source_sha256,status\r\n"
                f"2022-01-03,0.2,0.1,0.13,{'B' * 64},LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE\r\n"
            ),
        )
        self.assertEqual(
            daily_csv,
            (
                "completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,"
                "source_sha256,status\r\n"
                f"2022-01-03,4000.0,0.13,32.5,{'C' * 64},LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE\r\n"
            ),
        )

    def test_mes_runtime_risk_ledger_renderers_fail_closed_on_unlocked_or_inconsistent_values(self) -> None:
        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESAnnualRiskRuntimeLedgerRow,
            S09MESDailyPriceRiskRuntimeLedgerRow,
            render_s09_mes_annual_risk_runtime_ledger_csv,
            render_s09_mes_daily_price_risk_runtime_ledger_csv,
        )

        annual = S09MESAnnualRiskRuntimeLedgerRow(
            completed_trading_date=date(2022, 1, 3),
            long_run_annual_risk=0.20,
            current_ewma32_annual_risk=0.10,
            annual_percentage_risk=0.13,
            source_sha256="B" * 64,
            status="LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE",
        )
        daily = S09MESDailyPriceRiskRuntimeLedgerRow(
            completed_trading_date=date(2022, 1, 3),
            current_price=4000.0,
            annual_percentage_risk=0.13,
            daily_price_risk_currency=32.5,
            source_sha256="C" * 64,
            status="LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE",
        )

        hostile_annual_rows = (
            (),
            (replace(annual, completed_trading_date=datetime(2022, 1, 3, tzinfo=timezone.utc)),),
            (replace(annual, long_run_annual_risk=0.0),),
            (replace(annual, current_ewma32_annual_risk=nan),),
            (replace(annual, annual_percentage_risk=0.14),),
            (replace(annual, source_sha256=""),),
            (replace(annual, source_sha256="Z" * 64),),
            (replace(annual, status="PROVISIONAL"),),
        )
        for rows in hostile_annual_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_annual_risk_runtime_ledger_csv(rows)

        hostile_daily_rows = (
            (),
            (replace(daily, completed_trading_date=datetime(2022, 1, 3, tzinfo=timezone.utc)),),
            (replace(daily, current_price=0.0),),
            (replace(daily, annual_percentage_risk=nan),),
            (replace(daily, daily_price_risk_currency=33.0),),
            (replace(daily, source_sha256=""),),
            (replace(daily, source_sha256="Z" * 64),),
            (replace(daily, status="PROVISIONAL"),),
        )
        for rows in hostile_daily_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_daily_price_risk_runtime_ledger_csv(rows)

    def test_mes_runtime_risk_ledger_audit_preserves_no_execution_boundary(self) -> None:
        audit_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_RUNTIME_RISK_LEDGER_RENDERERS_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
        )
        text = audit_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_S09_MES_RUNTIME_RISK_LEDGER_RENDERERS_NOT_DATA_NOT_EXECUTION_NOT_BACKTEST", text)
        self.assertIn("render_s09_mes_annual_risk_runtime_ledger_csv", text)
        self.assertIn("render_s09_mes_daily_price_risk_runtime_ledger_csv", text)
        self.assertIn("completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_sha256,status", text)
        self.assertIn("completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,source_sha256,status", text)
        self.assertIn("LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE", text)
        self.assertIn("LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("no Databento API access", text)
        self.assertIn("no provider download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no runtime risk execution", text)
        self.assertIn("no cost extraction", text)
        self.assertIn("no forecast computation", text)
        self.assertIn("no backtests", text)
        self.assertIn("no OOS", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)
        self.assertIn("no Git staging", text)

    def locked_cost_component(
        self,
        component_name: str,
        value: float,
        *,
        timing: str = "PER_SIDE",
        status: SourceRuleStatus = SourceRuleStatus.LOCKED,
    ) -> S09MESLockedCostComponent:
        return S09MESLockedCostComponent(
            component_name=component_name,
            amount_currency=value,
            currency="USD",
            charge_timing=timing,
            effective_start=date(2022, 1, 1),
            effective_end=date(2022, 12, 31),
            source_label=f"LOCKED_{component_name.upper()}_SOURCE",
            source_sha256="A" * 64,
            status=status,
        )

    def locked_cost_request(self) -> S09MESCostComponentSetRequest:
        return S09MESCostComponentSetRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            root="MES",
            row_id="APPENDIX_C_174_006",
            completed_trading_date=date(2022, 1, 3),
            components=(
                self.locked_cost_component("exchange_fee", 0.35),
                self.locked_cost_component("clearing_regulatory_fee", 0.02),
                self.locked_cost_component("broker_commission", 0.50),
                self.locked_cost_component("spread_slippage", 1.25, timing="ROUND_TURN"),
            ),
            component_set_status=SourceRuleStatus.LOCKED,
        )

    def test_mes_total_cost_aggregates_locked_cost_components_with_round_turn_semantics(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESCostComponentSetRequest as ExportedRequest,
            S09MESLockedCostComponent as ExportedComponent,
            s09_mes_total_cost_from_locked_components as exported_helper,
        )

        self.assertIs(ExportedRequest, S09MESCostComponentSetRequest)
        self.assertIs(ExportedComponent, S09MESLockedCostComponent)
        self.assertIs(exported_helper, s09_mes_total_cost_from_locked_components)

        result = s09_mes_total_cost_from_locked_components(self.locked_cost_request())

        self.assertAlmostEqual(result.total_cost_per_trade_currency, 2.99)
        self.assertEqual(result.currency, "USD")
        self.assertEqual(
            result.component_round_turn_costs,
            (
                ("exchange_fee", 0.70),
                ("clearing_regulatory_fee", 0.04),
                ("broker_commission", 1.00),
                ("spread_slippage", 1.25),
            ),
        )
        self.assertEqual(result.cost_basis, "LOCKED_MES_COST_COMPONENTS_ROUND_TURN_PER_TRADE_USD")
        self.assertTrue(result.ready_for_risk_adjusted_cost)

    def test_mes_total_cost_fails_closed_without_complete_locked_source_native_cost_evidence(self) -> None:
        base = self.locked_cost_request()

        hostile_requests = (
            replace(base, component_set_status=SourceRuleStatus.UNRESOLVED),
            replace(base, components=base.components[:3]),
            replace(base, components=base.components + (self.locked_cost_component("exchange_fee", 0.01),)),
            replace(base, components=(replace(base.components[0], status=SourceRuleStatus.UNRESOLVED),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], currency="EUR"),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], charge_timing="DAILY"),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], amount_currency=-0.01),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], amount_currency=nan),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], amount_currency=True),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], source_label=""),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], source_sha256=""),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], effective_start=datetime(2022, 1, 1, tzinfo=timezone.utc)),) + base.components[1:]),
            replace(base, components=(replace(base.components[0], effective_start=date(2022, 1, 4)),) + base.components[1:]),
            replace(base, completed_trading_date=datetime(2022, 1, 3, tzinfo=timezone.utc)),
            replace(base, root="ES"),
            replace(base, row_id="APPENDIX_C_174_002"),
            replace(base, lane_class=LaneClass.CFD_ADAPTER),
        )
        for request in hostile_requests:
            with self.subTest(request=request):
                with self.assertRaises(CarverBlocked):
                    s09_mes_total_cost_from_locked_components(request)

    def test_mes_risk_adjusted_cost_uses_locked_cost_and_annualized_price_risk(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESRiskAdjustedCostRequest as ExportedRequest,
            s09_mes_risk_adjusted_cost_from_locked_inputs as exported_helper,
        )

        self.assertIs(ExportedRequest, S09MESRiskAdjustedCostRequest)
        self.assertIs(exported_helper, s09_mes_risk_adjusted_cost_from_locked_inputs)

        result = s09_mes_risk_adjusted_cost_from_locked_inputs(
            S09MESRiskAdjustedCostRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                total_cost_per_trade_currency=3.0,
                total_cost_status=SourceRuleStatus.LOCKED,
                daily_price_risk_currency=500.0,
                daily_price_risk_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(result.annualized_price_risk_currency, 40000.0)
        self.assertEqual(result.risk_adjusted_cost_per_trade_sr, 0.000075)
        self.assertEqual(
            result.cost_basis,
            "LOCKED_TOTAL_COST_PER_TRADE_OVER_LOCKED_ANNUALIZED_USD_PRICE_RISK_FROM_DAILY_X16_X_MES_MULTIPLIER",
        )
        self.assertTrue(result.ready_for_speed_eligibility)

    def test_mes_risk_adjusted_cost_fails_closed_without_locked_inputs(self) -> None:
        base = S09MESRiskAdjustedCostRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            total_cost_per_trade_currency=3.0,
            total_cost_status=SourceRuleStatus.LOCKED,
            daily_price_risk_currency=500.0,
            daily_price_risk_status=SourceRuleStatus.LOCKED,
        )

        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, total_cost_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, daily_price_risk_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, total_cost_per_trade_currency=0.0))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, daily_price_risk_currency=0.0))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, total_cost_per_trade_currency=-1.0))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, daily_price_risk_currency=-1.0))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, total_cost_per_trade_currency=nan))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, daily_price_risk_currency=inf))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, total_cost_per_trade_currency="3.0"))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, total_cost_per_trade_currency=True))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, contract_multiplier_usd_per_point=50.0))
        with self.assertRaises(CarverBlocked):
            s09_mes_risk_adjusted_cost_from_locked_inputs(replace(base, lane_class=LaneClass.CFD_ADAPTER))

    def test_mes_cost_and_risk_adjusted_cost_ledgers_use_locked_components_only(self) -> None:
        cost = s09_mes_total_cost_from_locked_components(self.locked_cost_request())
        risk_adjusted = s09_mes_risk_adjusted_cost_from_locked_inputs(
            S09MESRiskAdjustedCostRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                total_cost_per_trade_currency=cost.total_cost_per_trade_currency,
                total_cost_status=SourceRuleStatus.LOCKED,
                daily_price_risk_currency=500.0,
                daily_price_risk_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertAlmostEqual(risk_adjusted.risk_adjusted_cost_per_trade_sr, 0.00007475)

    def test_mes_cost_ledger_renderers_output_locked_source_native_cost_values(self) -> None:
        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESCostValueLedgerRow,
            S09MESRiskAdjustedCostLedgerRow,
            render_s09_mes_cost_value_ledger_csv,
            render_s09_mes_risk_adjusted_cost_ledger_csv,
        )

        cost_csv = render_s09_mes_cost_value_ledger_csv(
            (
                S09MESCostValueLedgerRow(
                    completed_trading_date=date(2022, 1, 3),
                    component_name="exchange_fee",
                    amount_currency=0.35,
                    currency="USD",
                    charge_timing="PER_SIDE",
                    effective_start=date(2022, 1, 1),
                    effective_end=date(2022, 12, 31),
                    source_label="LOCKED_EXCHANGE_FEE_SOURCE",
                    source_sha256="D" * 64,
                    status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
                ),
                S09MESCostValueLedgerRow(
                    completed_trading_date=date(2022, 1, 3),
                    component_name="clearing_regulatory_fee",
                    amount_currency=0.02,
                    currency="USD",
                    charge_timing="PER_SIDE",
                    effective_start=date(2022, 1, 1),
                    effective_end=date(2022, 12, 31),
                    source_label="LOCKED_CLEARING_REGULATORY_FEE_SOURCE",
                    source_sha256="E" * 64,
                    status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
                ),
                S09MESCostValueLedgerRow(
                    completed_trading_date=date(2022, 1, 3),
                    component_name="broker_commission",
                    amount_currency=0.50,
                    currency="USD",
                    charge_timing="PER_SIDE",
                    effective_start=date(2022, 1, 1),
                    effective_end=date(2022, 12, 31),
                    source_label="LOCKED_BROKER_COMMISSION_SOURCE",
                    source_sha256="F" * 64,
                    status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
                ),
                S09MESCostValueLedgerRow(
                    completed_trading_date=date(2022, 1, 3),
                    component_name="spread_slippage",
                    amount_currency=1.25,
                    currency="USD",
                    charge_timing="ROUND_TURN",
                    effective_start=date(2022, 1, 1),
                    effective_end=date(2022, 12, 31),
                    source_label="LOCKED_SPREAD_SLIPPAGE_SOURCE",
                    source_sha256="A" * 64,
                    status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
                ),
            )
        )
        risk_adjusted_csv = render_s09_mes_risk_adjusted_cost_ledger_csv(
            (
                S09MESRiskAdjustedCostLedgerRow(
                    completed_trading_date=date(2022, 1, 3),
                    total_cost_per_trade_currency=2.99,
                    daily_price_risk_currency=500.0,
                    risk_adjusted_cost_per_trade_sr=0.00007475,
                    status="LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE",
                ),
            )
        )

        self.assertEqual(
            cost_csv.splitlines()[0],
            "completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status",
        )
        self.assertIn("2022-01-03,exchange_fee,0.35,USD,PER_SIDE,2022-01-01,2022-12-31,LOCKED_EXCHANGE_FEE_SOURCE", cost_csv)
        self.assertIn("2022-01-03,spread_slippage,1.25,USD,ROUND_TURN,2022-01-01,2022-12-31,LOCKED_SPREAD_SLIPPAGE_SOURCE", cost_csv)
        self.assertEqual(
            risk_adjusted_csv,
            (
                "completed_trading_date,total_cost_per_trade_currency,daily_price_risk_currency,"
                "risk_adjusted_cost_per_trade_sr,status\r\n"
                "2022-01-03,2.99,500.0,7.475e-05,LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE\r\n"
            ),
        )

    def test_mes_cost_ledger_renderers_fail_closed_on_unlocked_or_inconsistent_values(self) -> None:
        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESCostValueLedgerRow,
            S09MESRiskAdjustedCostLedgerRow,
            render_s09_mes_cost_value_ledger_csv,
            render_s09_mes_risk_adjusted_cost_ledger_csv,
        )

        cost = S09MESCostValueLedgerRow(
            completed_trading_date=date(2022, 1, 3),
            component_name="exchange_fee",
            amount_currency=0.35,
            currency="USD",
            charge_timing="PER_SIDE",
            effective_start=date(2022, 1, 1),
            effective_end=date(2022, 12, 31),
            source_label="LOCKED_EXCHANGE_FEE_SOURCE",
            source_sha256="D" * 64,
            status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
        )
        risk_adjusted = S09MESRiskAdjustedCostLedgerRow(
            completed_trading_date=date(2022, 1, 3),
            total_cost_per_trade_currency=2.99,
            daily_price_risk_currency=500.0,
            risk_adjusted_cost_per_trade_sr=0.00007475,
            status="LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE",
        )

        hostile_cost_rows = (
            (),
            (replace(cost, completed_trading_date=datetime(2022, 1, 3, tzinfo=timezone.utc)),),
            (replace(cost, component_name="platform_fee"),),
            (replace(cost, amount_currency=-0.01),),
            (replace(cost, currency="EUR"),),
            (replace(cost, charge_timing="DAILY"),),
            (replace(cost, effective_start=datetime(2022, 1, 1, tzinfo=timezone.utc)),),
            (replace(cost, effective_start=date(2022, 1, 4)),),
            (replace(cost, source_label=""),),
            (replace(cost, source_sha256=""),),
            (replace(cost, source_sha256="Z" * 64),),
            (replace(cost, status="PROVISIONAL"),),
        )
        for rows in hostile_cost_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_cost_value_ledger_csv(rows)

        hostile_risk_adjusted_rows = (
            (),
            (replace(risk_adjusted, completed_trading_date=datetime(2022, 1, 3, tzinfo=timezone.utc)),),
            (replace(risk_adjusted, total_cost_per_trade_currency=0.0),),
            (replace(risk_adjusted, daily_price_risk_currency=0.0),),
            (replace(risk_adjusted, risk_adjusted_cost_per_trade_sr=0.006),),
            (replace(risk_adjusted, status="PROVISIONAL"),),
        )
        for rows in hostile_risk_adjusted_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_risk_adjusted_cost_ledger_csv(rows)

    def test_mes_cost_ledger_audit_preserves_no_execution_boundary(self) -> None:
        audit_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_COST_LEDGER_RENDERERS_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
        )
        text = audit_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_S09_MES_COST_LEDGER_RENDERERS_NOT_DATA_NOT_EXECUTION_NOT_BACKTEST", text)
        self.assertIn("render_s09_mes_cost_value_ledger_csv", text)
        self.assertIn("render_s09_mes_risk_adjusted_cost_ledger_csv", text)
        self.assertIn("completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status", text)
        self.assertIn("completed_trading_date,total_cost_per_trade_currency,daily_price_risk_currency,risk_adjusted_cost_per_trade_sr,status", text)
        self.assertIn("LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE", text)
        self.assertIn("LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("no Databento API access", text)
        self.assertIn("no provider download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no runtime risk execution", text)
        self.assertIn("no cost extraction", text)
        self.assertIn("no forecast computation", text)
        self.assertIn("no backtests", text)
        self.assertIn("no OOS", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)
        self.assertIn("no Git staging", text)

    def test_mes_speed_eligibility_uses_precomputed_risk_adjusted_cost_and_table_36_fdm(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESRiskAdjustedCostSpeedEligibilityRequest as ExportedRequest,
            s09_mes_speed_eligibility_from_risk_adjusted_cost as exported_helper,
        )

        self.assertIs(ExportedRequest, S09MESRiskAdjustedCostSpeedEligibilityRequest)
        self.assertIs(exported_helper, s09_mes_speed_eligibility_from_risk_adjusted_cost)

        result = s09_mes_speed_eligibility_from_risk_adjusted_cost(
            S09MESRiskAdjustedCostSpeedEligibilityRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                risk_adjusted_cost_per_trade_sr=0.006,
                risk_adjusted_cost_status=SourceRuleStatus.LOCKED,
                threshold_sr=0.15,
                threshold_status=SourceRuleStatus.LOCKED,
                turnover_status=SourceRuleStatus.LOCKED,
            )
        )

        self.assertEqual(result.eligible_spans, (16, 32, 64))
        self.assertEqual(result.fdm, 1.08)
        self.assertEqual(result.eligibility_basis, "LOCKED_COST_SCREEN_0_15_SR_THRESHOLD_PRECOMPUTED_RISK_ADJUSTED_COST")
        self.assertEqual(result.rejected_spans, (2, 4, 8))
        self.assertTrue(result.ready_for_readiness_gate)

    def test_mes_speed_eligibility_fails_closed_without_cost_lock_or_surviving_speed(self) -> None:
        base = S09MESRiskAdjustedCostSpeedEligibilityRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            risk_adjusted_cost_per_trade_sr=0.006,
            risk_adjusted_cost_status=SourceRuleStatus.LOCKED,
            threshold_sr=0.15,
            threshold_status=SourceRuleStatus.LOCKED,
            turnover_status=SourceRuleStatus.LOCKED,
        )

        with self.assertRaises(CarverBlocked):
            s09_mes_speed_eligibility_from_risk_adjusted_cost(replace(base, risk_adjusted_cost_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_speed_eligibility_from_risk_adjusted_cost(replace(base, risk_adjusted_cost_per_trade_sr=0.0))
        with self.assertRaises(CarverBlocked):
            s09_mes_speed_eligibility_from_risk_adjusted_cost(replace(base, risk_adjusted_cost_per_trade_sr=0.03))
        with self.assertRaises(CarverBlocked):
            s09_mes_speed_eligibility_from_risk_adjusted_cost(replace(base, lane_class=LaneClass.CFD_ADAPTER))
        with self.assertRaises(CarverBlocked):
            s09_mes_speed_eligibility_from_risk_adjusted_cost(replace(base, threshold_sr=0.20))
        with self.assertRaises(CarverBlocked):
            s09_mes_speed_eligibility_from_risk_adjusted_cost(replace(base, threshold_status=SourceRuleStatus.UNRESOLVED))
        with self.assertRaises(CarverBlocked):
            s09_mes_speed_eligibility_from_risk_adjusted_cost(replace(base, turnover_status=SourceRuleStatus.UNRESOLVED))

    def test_mes_speed_eligibility_status_can_feed_readiness_only_after_locks(self) -> None:
        speed = s09_mes_speed_eligibility_from_risk_adjusted_cost(
            S09MESRiskAdjustedCostSpeedEligibilityRequest(
                lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                risk_adjusted_cost_per_trade_sr=0.006,
                risk_adjusted_cost_status=SourceRuleStatus.LOCKED,
                threshold_sr=0.15,
                threshold_status=SourceRuleStatus.LOCKED,
                turnover_status=SourceRuleStatus.LOCKED,
            )
        )
        ready = evaluate_s09_mes_strategy_input_readiness(
            replace(
                self.locked_request(),
                eligible_spans=speed.eligible_spans,
                fdm=speed.fdm,
                speed_eligibility_basis=speed.eligibility_basis,
            )
        )

        self.assertTrue(ready.ready)

    def test_mes_speed_eligibility_and_status_renderers_output_locked_contracts(self) -> None:
        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESRollRiskCostExecutionStatus,
            S09MESSpeedEligibilityLedgerRow,
            render_s09_mes_roll_risk_cost_execution_status_json,
            render_s09_mes_speed_eligibility_ledger_csv,
        )

        speed_csv = render_s09_mes_speed_eligibility_ledger_csv(
            (
                S09MESSpeedEligibilityLedgerRow(
                    span=16,
                    turnover=13.2,
                    risk_adjusted_cost_per_trade_sr=0.006,
                    threshold_sr=0.15,
                    eligible=True,
                    status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
                ),
                S09MESSpeedEligibilityLedgerRow(
                    span=2,
                    turnover=98.5,
                    risk_adjusted_cost_per_trade_sr=0.006,
                    threshold_sr=0.15,
                    eligible=False,
                    status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
                ),
            )
        )
        status_json = render_s09_mes_roll_risk_cost_execution_status_json(
            S09MESRollRiskCostExecutionStatus(
                status="READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST",
                databento_api_access="NO",
                new_provider_data_download="NO",
                market_row_parsing="NO",
                strategy_input_readiness_status="S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY",
            )
        )

        self.assertEqual(
            speed_csv,
            (
                "span,turnover,risk_adjusted_cost_per_trade_sr,threshold_sr,eligible,status\r\n"
                "16,13.2,0.006,0.15,True,LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE\r\n"
                "2,98.5,0.006,0.15,False,LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE\r\n"
            ),
        )
        self.assertEqual(
            status_json,
            (
                "{\n"
                '  "databento_api_access": "NO",\n'
                '  "market_row_parsing": "NO",\n'
                '  "new_provider_data_download": "NO",\n'
                '  "status": "READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST",\n'
                '  "strategy_input_readiness_status": "S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY"\n'
                "}\n"
            ),
        )

    def test_mes_speed_eligibility_and_status_renderers_fail_closed_on_contract_drift(self) -> None:
        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESRollRiskCostExecutionStatus,
            S09MESSpeedEligibilityLedgerRow,
            render_s09_mes_roll_risk_cost_execution_status_json,
            render_s09_mes_speed_eligibility_ledger_csv,
        )

        speed = S09MESSpeedEligibilityLedgerRow(
            span=16,
            turnover=13.2,
            risk_adjusted_cost_per_trade_sr=0.006,
            threshold_sr=0.15,
            eligible=True,
            status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
        )
        status = S09MESRollRiskCostExecutionStatus(
            status="READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST",
            databento_api_access="NO",
            new_provider_data_download="NO",
            market_row_parsing="NO",
            strategy_input_readiness_status="S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY",
        )

        hostile_speed_rows = (
            (),
            (replace(speed, span=3),),
            (replace(speed, turnover=12.0),),
            (replace(speed, risk_adjusted_cost_per_trade_sr=0.0),),
            (replace(speed, threshold_sr=0.20),),
            (replace(speed, eligible=False),),
            (replace(speed, status="PROVISIONAL"),),
        )
        for rows in hostile_speed_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_speed_eligibility_ledger_csv(rows)

        hostile_statuses = (
            replace(status, status="READY_FOR_BACKTEST"),
            replace(status, databento_api_access="YES"),
            replace(status, new_provider_data_download="YES"),
            replace(status, market_row_parsing="YES"),
            replace(status, strategy_input_readiness_status="READY_FOR_LOCKBOX"),
            replace(
                status,
                status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
                strategy_input_readiness_status="S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY",
            ),
        )
        for payload in hostile_statuses:
            with self.subTest(payload=payload):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_roll_risk_cost_execution_status_json(payload)

    def test_mes_speed_status_audit_preserves_no_execution_boundary(self) -> None:
        audit_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_SPEED_STATUS_RENDERERS_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
        )
        text = audit_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_S09_MES_SPEED_STATUS_RENDERERS_NOT_DATA_NOT_EXECUTION_NOT_BACKTEST", text)
        self.assertIn("render_s09_mes_speed_eligibility_ledger_csv", text)
        self.assertIn("render_s09_mes_roll_risk_cost_execution_status_json", text)
        self.assertIn("span,turnover,risk_adjusted_cost_per_trade_sr,threshold_sr,eligible,status", text)
        self.assertIn("READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST", text)
        self.assertIn("FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY", text)
        self.assertIn("LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("no Databento API access", text)
        self.assertIn("no provider download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no runtime risk execution", text)
        self.assertIn("no cost extraction", text)
        self.assertIn("no forecast computation", text)
        self.assertIn("no backtests", text)
        self.assertIn("no OOS", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)
        self.assertIn("no Git staging", text)

    def test_synthetic_guard_record_preserves_non_data_boundary(self) -> None:
        text = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_STRATEGY_INPUT_READINESS_SYNTHETIC_GUARD_2026-06-02.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_S09_MES_READINESS_GUARD_NOT_DATA_NOT_BACKTEST", text)
        self.assertIn("evaluate_s09_mes_strategy_input_readiness", text)
        self.assertIn("not an assumption", text)
        self.assertIn("no provider API access", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no continuous lineage construction", text)
        self.assertIn("no S09 forecast computation", text)
        self.assertIn("no backtests", text)


if __name__ == "__main__":
    unittest.main()

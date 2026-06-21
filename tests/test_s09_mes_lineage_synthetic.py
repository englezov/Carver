from __future__ import annotations

import ast
import hashlib
import sys
import tempfile
import unittest
import json
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked  # noqa: E402
from carver.spine.s09_mes_lineage import (  # noqa: E402
    S09_MES_LINEAGE_READINESS_KEYS,
    S09MESDatedContractBar,
    S09MESDatedContractDefinition,
    S09MESLineageRequest,
    S09MESRollDateNormalizationAuthority,
    build_s09_mes_lineage,
    evaluate_s09_mes_lineage_strategy_readiness,
    normalize_s09_mes_roll_provider_date,
)


class S09MESLineageSyntheticTests(unittest.TestCase):
    def bar(
        self,
        symbol: str,
        day: str,
        close: float,
        *,
        condition: str = "NORMAL_PROVIDER_CONDITION",
        admission_policy: str = "NORMAL_PROVIDER_CONDITION_ONLY",
    ) -> S09MESDatedContractBar:
        return S09MESDatedContractBar(
            raw_symbol=symbol,
            completed_trading_date=date.fromisoformat(day),
            open=close - 1.0,
            high=close + 2.0,
            low=close - 2.0,
            close=close,
            volume=1000.0,
            provider_condition_classification=condition,
            source_raw_sha256=f"sha-{symbol}",
            provider_condition_admission_policy=admission_policy,
        )

    def definition(self, symbol: str, expiration: str) -> S09MESDatedContractDefinition:
        return S09MESDatedContractDefinition(
            raw_symbol=symbol,
            expiration=datetime.fromisoformat(expiration).replace(tzinfo=timezone.utc),
            product_code="MES",
            currency="USD",
            multiplier=5.0,
            tick_size=0.25,
            venue="XCME",
            lifecycle_source="DATABENTO_DEFINITION_CROSSCHECK_PLUS_LOCAL_CME_STATIC_EXTRACT",
        )

    def test_builds_static_buffer_roll_and_additive_lineage_without_strategy_output(self) -> None:
        old_dates = ("2026-03-10", "2026-03-11", "2026-03-12", "2026-03-13", "2026-03-16", "2026-03-17", "2026-03-18", "2026-03-19")
        new_dates = ("2026-03-10", "2026-03-11", "2026-03-12", "2026-03-13", "2026-03-16", "2026-03-17")
        old = tuple(self.bar("MESH6", day, 100.0 + index) for index, day in enumerate(old_dates))
        new = tuple(self.bar("MESM6", day, 200.0 + index) for index, day in enumerate(new_dates))

        result = build_s09_mes_lineage(
            S09MESLineageRequest(
                symbol_order=("MESH6", "MESM6"),
                bars_by_symbol={"MESH6": old, "MESM6": new},
                definitions_by_symbol={
                    "MESH6": self.definition("MESH6", "2026-03-20T13:30:00"),
                    "MESM6": self.definition("MESM6", "2026-06-19T13:30:00"),
                },
                minimum_target_rows=5,
            )
        )

        self.assertEqual(len(result.roll_events), 1)
        self.assertEqual(result.roll_events[0].old_symbol, "MESH6")
        self.assertEqual(result.roll_events[0].new_symbol, "MESM6")
        self.assertEqual(result.roll_events[0].roll_transition_date.isoformat(), "2026-03-13")
        self.assertEqual(result.roll_events[0].roll_buffer_date.isoformat(), "2026-03-13")
        self.assertEqual(result.roll_events[0].old_history_additive_adjustment, 100.0)
        self.assertEqual([row.completed_trading_date.isoformat() for row in result.adjusted_rows], [
            "2026-03-10",
            "2026-03-11",
            "2026-03-12",
            "2026-03-13",
            "2026-03-16",
            "2026-03-17",
        ])
        self.assertEqual([row.adjusted_close for row in result.adjusted_rows], [200.0, 201.0, 202.0, 203.0, 204.0, 205.0])
        self.assertEqual(result.continuous_lineage_status, "PROVISIONAL_LOCAL_LINEAGE_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_LOCKED")
        self.assertEqual(result.roll_plan_status, "PROVISIONAL_PROVIDER_DATE_ROLL_PLAN_TRADING_DAY_SEMANTICS_NOT_LOCKED")
        self.assertEqual(result.back_adjustment_status, "PROVISIONAL_LOCAL_BACK_ADJUSTMENT_NOT_STRATEGY_INPUT")
        self.assertEqual(result.provider_condition_admission_status, "LOCKED")

    def test_fails_closed_on_degraded_rows_non_mes_or_missing_roll_overlap(self) -> None:
        with self.assertRaises(CarverBlocked):
            build_s09_mes_lineage(
                S09MESLineageRequest(
                    symbol_order=("MESH6",),
                    bars_by_symbol={"MESH6": (self.bar("MESH6", "2026-03-10", 100.0, condition="DEGRADED"),)},
                    definitions_by_symbol={"MESH6": self.definition("MESH6", "2026-03-20T13:30:00")},
                    minimum_target_rows=1,
                )
            )

    def test_degraded_rows_require_explicit_locked_ohlcv_admission_policy(self) -> None:
        with self.assertRaises(CarverBlocked):
            self.bar(
                "MESH6",
                "2026-03-10",
                100.0,
                condition="DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY",
            ).validate()

        admitted = self.bar(
            "MESH6",
            "2026-03-10",
            100.0,
            condition="DEGRADED_PROVIDER_CONDITION_OHLCV_ADMITTED_BY_OPERATOR_POLICY",
            admission_policy="SOURCE_NATIVE_DEGRADED_OHLCV_COLD_SHAPE_BASED_POLICY_LOCKED",
        )

        admitted.validate()

        with self.assertRaises(CarverBlocked):
            build_s09_mes_lineage(
                S09MESLineageRequest(
                    symbol_order=("ESH6",),
                    bars_by_symbol={"ESH6": (self.bar("ESH6", "2026-03-10", 100.0),)},
                    definitions_by_symbol={"ESH6": self.definition("ESH6", "2026-03-20T13:30:00")},
                    minimum_target_rows=1,
                )
            )

        with self.assertRaises(CarverBlocked):
            build_s09_mes_lineage(
                S09MESLineageRequest(
                    symbol_order=("MESH6", "MESM6"),
                    bars_by_symbol={
                        "MESH6": tuple(self.bar("MESH6", day, 100.0) for day in ("2026-03-10", "2026-03-11", "2026-03-12", "2026-03-13", "2026-03-16")),
                        "MESM6": (self.bar("MESM6", "2026-03-16", 200.0),),
                    },
                    definitions_by_symbol={
                        "MESH6": self.definition("MESH6", "2026-03-20T13:30:00"),
                        "MESM6": self.definition("MESM6", "2026-06-19T13:30:00"),
                    },
                    minimum_target_rows=1,
                )
            )

    def test_builds_mes_2019_to_2020_one_digit_contract_year_order(self) -> None:
        old_dates = ("2019-05-20", "2019-05-21", "2019-05-22", "2019-05-23", "2019-05-24", "2019-05-27", "2019-05-28")
        new_dates = ("2019-05-20", "2019-05-21", "2019-05-22", "2019-05-23", "2019-05-24", "2019-05-27")
        old = tuple(self.bar("MESZ9", day, 2900.0 + index) for index, day in enumerate(old_dates))
        new = tuple(self.bar("MESH0", day, 3000.0 + index) for index, day in enumerate(new_dates))

        result = build_s09_mes_lineage(
            S09MESLineageRequest(
                symbol_order=("MESZ9", "MESH0"),
                bars_by_symbol={"MESZ9": old, "MESH0": new},
                definitions_by_symbol={
                    "MESZ9": self.definition("MESZ9", "2019-12-20T13:30:00"),
                    "MESH0": self.definition("MESH0", "2020-03-20T13:30:00"),
                },
                minimum_target_rows=5,
            )
        )

        self.assertEqual(result.source_contracts, ("MESZ9", "MESH0"))
        self.assertEqual(len(result.roll_events), 1)
        self.assertEqual(result.roll_events[0].old_symbol, "MESZ9")
        self.assertEqual(result.roll_events[0].new_symbol, "MESH0")

    def test_additive_adjustment_is_continuous_across_warmup_scoring_seam(self) -> None:
        old_dates = ("2020-03-30", "2020-03-31", "2020-04-01", "2020-04-02", "2020-04-03", "2020-04-05")
        new_dates = (
            "2020-03-30",
            "2020-03-31",
            "2020-04-01",
            "2020-04-02",
            "2020-04-03",
            "2020-04-05",
            "2020-04-06",
            "2020-04-07",
        )
        old = tuple(self.bar("MESH0", day, 100.0 + index) for index, day in enumerate(old_dates))
        new = tuple(self.bar("MESM0", day, 200.0 + index) for index, day in enumerate(new_dates))

        result = build_s09_mes_lineage(
            S09MESLineageRequest(
                symbol_order=("MESH0", "MESM0"),
                bars_by_symbol={"MESH0": old, "MESM0": new},
                definitions_by_symbol={
                    "MESH0": self.definition("MESH0", "2020-04-08T13:30:00"),
                    "MESM0": self.definition("MESM0", "2020-06-19T13:30:00"),
                },
                minimum_target_rows=5,
                roll_buffer_completed_days=1,
            )
        )
        by_date = {row.completed_trading_date.isoformat(): row for row in result.adjusted_rows}

        self.assertEqual(result.roll_events[0].roll_transition_date.isoformat(), "2020-04-05")
        self.assertEqual(by_date["2020-04-05"].source_raw_symbol, "MESH0")
        self.assertEqual(by_date["2020-04-06"].source_raw_symbol, "MESM0")
        self.assertEqual(by_date["2020-04-05"].adjusted_close, 205.0)
        self.assertEqual(by_date["2020-04-06"].adjusted_close, 206.0)
        self.assertEqual(by_date["2020-04-05"].cumulative_additive_adjustment, 100.0)
        self.assertEqual(by_date["2020-04-06"].cumulative_additive_adjustment, 0.0)

    def test_strategy_readiness_remains_blocked_until_risk_and_cost_are_locked(self) -> None:
        result = build_s09_mes_lineage(
            S09MESLineageRequest(
                symbol_order=("MESH6",),
                bars_by_symbol={"MESH6": tuple(self.bar("MESH6", f"2026-03-{day:02d}", 100.0 + day) for day in range(10, 16))},
                definitions_by_symbol={"MESH6": self.definition("MESH6", "2026-03-20T13:30:00")},
                minimum_target_rows=5,
            )
        )

        readiness = evaluate_s09_mes_lineage_strategy_readiness(result)

        self.assertEqual(readiness["continuous_lineage_status"], "PROVISIONAL_LOCAL_LINEAGE_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_LOCKED")
        self.assertEqual(readiness["official_lifecycle_evidence_status"], "FAIL_CLOSED_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_HASH_BOUND")
        self.assertEqual(readiness["roll_trading_day_semantics_status"], "FAIL_CLOSED_S09_MES_PROVIDER_DATE_ROLL_SEMANTICS_NOT_SOURCE_LOCKED")
        self.assertEqual(readiness["annual_risk_runtime_status"], "FAIL_CLOSED_S09_MES_ANNUAL_RISK_RUNTIME_NOT_LOCKED")
        self.assertEqual(readiness["cost_source_status"], "FAIL_CLOSED_S09_MES_COST_SOURCE_NOT_LOCKED")
        self.assertEqual(readiness["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertFalse(result.ready_for_lineage_use)

    def test_locked_readiness_contract_makes_lineage_usable_without_changing_default_guard(self) -> None:
        locked_statuses = {
            key: "LOCKED"
            for key in S09_MES_LINEAGE_READINESS_KEYS
        }
        result = build_s09_mes_lineage(
            S09MESLineageRequest(
                symbol_order=("MESH6",),
                bars_by_symbol={"MESH6": tuple(self.bar("MESH6", f"2026-03-{day:02d}", 100.0 + day) for day in range(10, 16))},
                definitions_by_symbol={"MESH6": self.definition("MESH6", "2026-03-20T13:30:00")},
                minimum_target_rows=5,
                strategy_input_readiness_statuses=locked_statuses,
            )
        )

        readiness = evaluate_s09_mes_lineage_strategy_readiness(result)

        self.assertEqual(readiness, locked_statuses)
        self.assertTrue(result.ready_for_lineage_use)

        with self.assertRaises(CarverBlocked):
            build_s09_mes_lineage(
                S09MESLineageRequest(
                    symbol_order=("MESH6",),
                    bars_by_symbol={"MESH6": tuple(self.bar("MESH6", f"2026-03-{day:02d}", 100.0 + day) for day in range(10, 16))},
                    definitions_by_symbol={"MESH6": self.definition("MESH6", "2026-03-20T13:30:00")},
                    minimum_target_rows=5,
                    strategy_input_readiness_statuses={"continuous_lineage_status": "LOCKED"},
                )
            )

    def test_roll_provider_date_normalization_requires_explicit_completed_date_authority(self) -> None:
        from carver.spine import (  # noqa: PLC0415
            S09MESRollDateNormalizationAuthority as ExportedAuthority,
            normalize_s09_mes_roll_provider_date as exported_normalize,
        )

        self.assertIs(ExportedAuthority, S09MESRollDateNormalizationAuthority)
        self.assertIs(exported_normalize, normalize_s09_mes_roll_provider_date)

        normalized = normalize_s09_mes_roll_provider_date(
            provider_date=date(2022, 3, 13),
            authority_rows=(
                S09MESRollDateNormalizationAuthority(
                    provider_date=date(2022, 3, 13),
                    completed_trading_date=date(2022, 3, 14),
                    authority_source="CME_GLOBEX_SESSION_CALENDAR_HASH_BOUND_EXTRACT",
                    authority_sha256="A" * 64,
                ),
            ),
        )

        self.assertEqual(normalized, date(2022, 3, 14))

        with self.assertRaises(CarverBlocked):
            normalize_s09_mes_roll_provider_date(
                provider_date=datetime(2022, 3, 13, tzinfo=timezone.utc),
                authority_rows=(
                    S09MESRollDateNormalizationAuthority(
                        provider_date=date(2022, 3, 13),
                        completed_trading_date=date(2022, 3, 14),
                        authority_source="CME_GLOBEX_SESSION_CALENDAR_HASH_BOUND_EXTRACT",
                        authority_sha256="A" * 64,
                    ),
                ),
            )

        with self.assertRaises(CarverBlocked):
            normalize_s09_mes_roll_provider_date(
                provider_date=date(2022, 3, 13),
                authority_rows=(
                    S09MESRollDateNormalizationAuthority(
                        provider_date=datetime(2022, 3, 13, tzinfo=timezone.utc),
                        completed_trading_date=date(2022, 3, 14),
                        authority_source="CME_GLOBEX_SESSION_CALENDAR_HASH_BOUND_EXTRACT",
                        authority_sha256="A" * 64,
                    ),
                ),
            )

        with self.assertRaises(CarverBlocked):
            normalize_s09_mes_roll_provider_date(
                provider_date=date(2022, 3, 13),
                authority_rows=(
                    S09MESRollDateNormalizationAuthority(
                        provider_date=date(2022, 3, 13),
                        completed_trading_date=datetime(2022, 3, 14, tzinfo=timezone.utc),
                        authority_source="CME_GLOBEX_SESSION_CALENDAR_HASH_BOUND_EXTRACT",
                        authority_sha256="A" * 64,
                    ),
                ),
            )

        with self.assertRaises(CarverBlocked):
            normalize_s09_mes_roll_provider_date(
                provider_date=date(2022, 6, 12),
                authority_rows=(),
            )

        with self.assertRaises(CarverBlocked):
            normalize_s09_mes_roll_provider_date(
                provider_date=date(2022, 6, 12),
                authority_rows=(
                    S09MESRollDateNormalizationAuthority(
                        provider_date=date(2022, 3, 13),
                        completed_trading_date=date(2022, 3, 14),
                        authority_source="CME_GLOBEX_SESSION_CALENDAR_HASH_BOUND_EXTRACT",
                        authority_sha256="A" * 64,
                    ),
                ),
            )

        with self.assertRaises(CarverBlocked):
            normalize_s09_mes_roll_provider_date(
                provider_date=date(2022, 3, 13),
                authority_rows=(
                    S09MESRollDateNormalizationAuthority(
                        provider_date=date(2022, 3, 13),
                        completed_trading_date=date(2022, 3, 14),
                        authority_source="CME_GLOBEX_SESSION_CALENDAR_HASH_BOUND_EXTRACT",
                        authority_sha256="A" * 64,
                    ),
                    S09MESRollDateNormalizationAuthority(
                        provider_date=date(2022, 3, 13),
                        completed_trading_date=date(2022, 3, 15),
                        authority_source="CME_GLOBEX_SESSION_CALENDAR_HASH_BOUND_EXTRACT",
                        authority_sha256="B" * 64,
                    ),
                ),
            )

        with self.assertRaises(CarverBlocked):
            normalize_s09_mes_roll_provider_date(
                provider_date=date(2022, 9, 11),
                authority_rows=(
                    S09MESRollDateNormalizationAuthority(
                        provider_date=date(2022, 9, 11),
                        completed_trading_date=date(2022, 9, 12),
                        authority_source="CME_GLOBEX_SESSION_CALENDAR_HASH_BOUND_EXTRACT",
                        authority_sha256="",
                    ),
                ),
            )

    def test_local_execution_artifacts_lock_lineage_but_not_strategy_input(self) -> None:
        status_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_continuous_lineage_risk_cost_eligibility"
            / "2022-01-03_2023-12-29"
            / "status"
            / "20260603_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_strategy_input_readiness_status.json"
        )
        roll_plan_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_continuous_lineage_risk_cost_eligibility"
            / "2022-01-03_2023-12-29"
            / "roll_plan"
            / "20260603_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_roll_plan.csv"
        )
        provenance_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_continuous_lineage_risk_cost_eligibility"
            / "2022-01-03_2023-12-29"
            / "provenance"
            / "20260603_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_provenance.md"
        )

        status = json.loads(status_path.read_text(encoding="utf-8"))
        roll_plan = roll_plan_path.read_text(encoding="utf-8")
        provenance = provenance_path.read_text(encoding="utf-8")

        manifest_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_continuous_lineage_risk_cost_eligibility"
            / "2022-01-03_2023-12-29"
            / "input_manifest"
            / "20260603_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_input_hash_manifest.csv"
        )
        continuous_text = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_continuous_lineage_risk_cost_eligibility"
            / "2022-01-03_2023-12-29"
            / "continuous_series"
            / "20260603_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_continuous_daily_mes_dev_recon_only.csv"
        ).read_text(encoding="utf-8")

        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY_LIFECYCLE_RISK_COST_SPEED_NOT_LOCKED")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["new_provider_data_download"], "NO")
        self.assertEqual(status["continuous_lineage_status"], "PROVISIONAL_LOCAL_LINEAGE_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_LOCKED")
        self.assertEqual(status["roll_plan_status"], "PROVISIONAL_PROVIDER_DATE_ROLL_PLAN_TRADING_DAY_SEMANTICS_NOT_LOCKED")
        self.assertEqual(status["back_adjustment_status"], "PROVISIONAL_LOCAL_BACK_ADJUSTMENT_NOT_STRATEGY_INPUT")
        self.assertEqual(status["provider_condition_admission_status"], "LOCKED")
        self.assertEqual(status["official_lifecycle_evidence_status"], "FAIL_CLOSED_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_HASH_BOUND")
        self.assertEqual(status["roll_trading_day_semantics_status"], "FAIL_CLOSED_S09_MES_PROVIDER_DATE_ROLL_SEMANTICS_NOT_SOURCE_LOCKED")
        self.assertEqual(status["annual_risk_runtime_status"], "FAIL_CLOSED_S09_MES_ANNUAL_RISK_RUNTIME_NOT_LOCKED")
        self.assertEqual(status["cost_source_status"], "FAIL_CLOSED_S09_MES_COST_SOURCE_NOT_LOCKED")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertEqual(status["target_window_adjusted_rows"], 619)
        self.assertEqual(status["roll_events"], 12)
        self.assertTrue(manifest_path.exists())
        manifest_text = manifest_path.read_text(encoding="utf-8")
        self.assertIn("source_sanitized_csv", manifest_text)
        self.assertIn("static_mes_extract_narrow_scope", manifest_text)
        self.assertIn("MESH2,MESM2,2022-03-18,2022-03-13,2022-03-13", roll_plan)
        self.assertNotIn("DEGRADED", continuous_text)
        self.assertIn("provider trading-date rows", provenance)
        self.assertIn("no provider API access", provenance)
        self.assertIn("no S09 forecast computation", provenance)
        self.assertIn("no backtests", provenance)

    def test_next_source_lock_gate_preserves_no_data_and_no_backtest_boundary(self) -> None:
        gate_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_OFFICIAL_LIFECYCLE_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_SOURCE_LOCK_GATE_2026-06-03.md"
        )
        text = gate_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_SOURCE_LOCK_GATE_NOT_EXECUTION_NOT_BACKTEST", text)
        self.assertIn("S09_MES_OFFICIAL_LIFECYCLE_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_SOURCE_LOCK_EXECUTION_GATE", text)
        self.assertIn("Operator has authorized Databento API access if needed at this stage.", text)
        self.assertIn("This gate does not currently need a Databento OHLCV request", text)
        self.assertIn("No S09 forecast may be computed while this remains unresolved.", text)
        self.assertIn("daily_price_risk = current_price * annual_percentage_risk / 16", text)
        self.assertIn("0.15 SR cost threshold production interpretation", text)
        self.assertIn("No default assumption that all six speeds survive is allowed.", text)
        self.assertIn("READY_FOR_S09_DEV_RECON_FORECAST_GATE_NOT_BACKTEST", text)
        self.assertIn("FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY", text)
        self.assertIn("no Databento OHLCV request", text)
        self.assertIn("no provider login", text)
        self.assertIn("no new data download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no risk runtime execution", text)
        self.assertIn("no cost computation", text)
        self.assertIn("no S09 forecast computation", text)
        self.assertIn("no backtests", text)
        self.assertIn("no Git staging", text)

    def test_deprecated_two_year_mes_executables_fail_closed_before_provider_or_parsing(self) -> None:
        deprecated_tools = (
            ROOT / "tools" / "databento" / "carver_s09_mes_dev_recon_daily_expansion.py",
            ROOT / "tools" / "databento" / "carver_s09_mes_continuous_lineage_risk_cost_eligibility.py",
            ROOT / "tools" / "databento" / "carver_s09_mes_roll_risk_cost_execution.py",
        )

        for path in deprecated_tools:
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                tree = ast.parse(source)
                main_node = next(
                    node
                    for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == "main"
                )
                first_statement = main_node.body[0]

                self.assertIsInstance(first_statement, ast.Raise)
                self.assertIn("DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE", source)
                self.assertIn("2019-05-05 through 2020-04-05", source)
                self.assertLess(
                    source.index("DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE"),
                    source.index("2022-01-03_2023-12-29"),
                )
                pre_quarantine_source = source[: source.index("DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE")]
                self.assertNotIn("import databento", pre_quarantine_source)

    def test_source_lock_execution_result_keeps_mes_not_strategy_ready(self) -> None:
        result_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_SOURCE_LOCK_EXECUTION_RESULT_2026-06-03.md"
        )
        status_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_source_lock"
            / "2022-01-03_2023-12-29"
            / "status"
            / "20260603_S09_MES_SOURCE_LOCK_strategy_input_readiness_status.json"
        )
        ledger_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_source_lock"
            / "2022-01-03_2023-12-29"
            / "readiness"
            / "20260603_S09_MES_SOURCE_LOCK_readiness_ledger.csv"
        )
        hashes_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_source_lock"
            / "2022-01-03_2023-12-29"
            / "hashes"
            / "20260603_S09_MES_SOURCE_LOCK_sha256.txt"
        )

        text = result_path.read_text(encoding="utf-8")
        status = json.loads(status_path.read_text(encoding="utf-8"))
        ledger = ledger_path.read_text(encoding="utf-8")
        hashes = hashes_path.read_text(encoding="utf-8")

        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_SOURCE_LOCK_INCOMPLETE_NOT_STRATEGY_READY")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["new_provider_data_download"], "NO")
        self.assertEqual(status["market_row_parsing"], "NO")
        self.assertEqual(status["daily_price_risk_conversion_source_status"], "LOCKED_BOOK_SOURCE_ATOM")
        self.assertEqual(status["daily_price_risk_runtime_status"], "FAIL_CLOSED_S09_MES_DAILY_PRICE_RISK_RUNTIME_BLOCKED_BY_ANNUAL_RISK")
        self.assertEqual(status["cost_source_status"], "FAIL_CLOSED_S09_MES_SOURCE_NATIVE_COST_SOURCE_NOT_LOCKED")
        self.assertEqual(status["eligible_speed_set_status"], "FAIL_CLOSED_S09_MES_ELIGIBLE_SPEED_SET_NOT_LOCKED")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertIn("daily_price_risk = current_price * annual_percentage_risk / 16", text)
        self.assertIn("no Databento API call", text)
        self.assertIn("no provider login", text)
        self.assertIn("no OHLCV request", text)
        self.assertIn("no new data download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no risk runtime execution", text)
        self.assertIn("no cost computation", text)
        self.assertIn("no S09 forecast computation", text)
        self.assertIn("no backtests", text)
        self.assertIn("no Git staging", text)
        self.assertIn("daily_price_risk_conversion_source_status,LOCKED_BOOK_SOURCE_ATOM", ledger)
        self.assertIn("official_lifecycle_evidence_status,FAIL_CLOSED_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_NOT_HASH_BOUND", ledger)
        self.assertIn("CARVER_S09_MES_SOURCE_LOCK_EXECUTION_RESULT_2026-06-03.md", hashes)
        self.assertIn("20260603_S09_MES_SOURCE_LOCK_strategy_input_readiness_status.json", hashes)

    def test_official_static_evidence_result_locks_only_generic_mes_facts(self) -> None:
        result_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_OFFICIAL_STATIC_LIFECYCLE_ROLL_RISK_COST_EVIDENCE_RESULT_2026-06-03.md"
        )
        status_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_official_static_evidence"
            / "2022-01-03_2023-12-29"
            / "status"
            / "20260603_S09_MES_OFFICIAL_STATIC_EVIDENCE_status.json"
        )
        ledger_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_official_static_evidence"
            / "2022-01-03_2023-12-29"
            / "evidence"
            / "20260603_S09_MES_OFFICIAL_STATIC_EVIDENCE_ledger.csv"
        )
        hashes_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_official_static_evidence"
            / "2022-01-03_2023-12-29"
            / "hashes"
            / "20260603_S09_MES_OFFICIAL_STATIC_EVIDENCE_sha256.txt"
        )

        text = result_path.read_text(encoding="utf-8")
        status = json.loads(status_path.read_text(encoding="utf-8"))
        ledger = ledger_path.read_text(encoding="utf-8")
        hashes = hashes_path.read_text(encoding="utf-8")

        self.assertEqual(status["status"], "PARTIAL_LOCK_GENERIC_MES_FACTS_STRATEGY_INPUT_FAIL_CLOSED")
        self.assertEqual(status["generic_mes_product_spec_status"], "LOCKED_OFFICIAL_CME_PUBLIC_STATIC")
        self.assertEqual(status["historical_contract_lifecycle_status"], "FAIL_CLOSED_S09_MES_HISTORICAL_CONTRACT_LIFECYCLE_NOT_HASH_BOUND_PER_CONTRACT")
        self.assertEqual(status["roll_trading_day_semantics_status"], "FAIL_CLOSED_S09_MES_PROVIDER_DATE_ROLL_SEMANTICS_NOT_SOURCE_LOCKED")
        self.assertEqual(status["cost_value_status"], "FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_EXTRACTED")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertIn("Micro E-mini S&P 500 futures contract is $5 x the S&P 500 Index", text)
        self.assertIn("minimum tick of 0.25 index points", text)
        self.assertIn("no OHLCV request", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no cost computation", text)
        self.assertIn("generic_mes_product_spec_status,LOCKED_OFFICIAL_CME_PUBLIC_STATIC", ledger)
        self.assertIn("historical_contract_lifecycle_status,FAIL_CLOSED_S09_MES_HISTORICAL_CONTRACT_LIFECYCLE_NOT_HASH_BOUND_PER_CONTRACT", ledger)
        self.assertIn("CARVER_S09_MES_OFFICIAL_STATIC_LIFECYCLE_ROLL_RISK_COST_EVIDENCE_RESULT_2026-06-03.md", hashes)
        self.assertIn("20260603_S09_MES_OFFICIAL_STATIC_EVIDENCE_status.json", hashes)

    def test_historical_lifecycle_cost_risk_extraction_result_locks_mes_contract_dates_only(self) -> None:
        result_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_HISTORICAL_LIFECYCLE_COST_AND_RISK_VALUE_EXTRACTION_RESULT_2026-06-03.md"
        )
        status_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_historical_lifecycle_cost_risk_extraction"
            / "2022-01-03_2023-12-29"
            / "status"
            / "20260603_S09_MES_HISTORICAL_LIFECYCLE_COST_RISK_EXTRACTION_status.json"
        )
        lifecycle_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_historical_lifecycle_cost_risk_extraction"
            / "2022-01-03_2023-12-29"
            / "lifecycle"
            / "20260603_S09_MES_HISTORICAL_LIFECYCLE_ledger.csv"
        )
        source_hash_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_historical_lifecycle_cost_risk_extraction"
            / "2022-01-03_2023-12-29"
            / "source_extracts"
            / "20260603_S09_MES_STATIC_SOURCE_EXTRACT_sha256.txt"
        )
        packet_hash_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_historical_lifecycle_cost_risk_extraction"
            / "2022-01-03_2023-12-29"
            / "hashes"
            / "20260603_S09_MES_HISTORICAL_LIFECYCLE_COST_RISK_EXTRACTION_sha256.txt"
        )

        text = result_path.read_text(encoding="utf-8")
        status = json.loads(status_path.read_text(encoding="utf-8"))
        lifecycle = lifecycle_path.read_text(encoding="utf-8")
        source_hashes = source_hash_path.read_text(encoding="utf-8")
        packet_hashes = packet_hash_path.read_text(encoding="utf-8")

        self.assertEqual(status["status"], "PARTIAL_LOCK_MES_HISTORICAL_LIFECYCLE_DATES_STRATEGY_INPUT_FAIL_CLOSED")
        self.assertEqual(status["historical_contract_lifecycle_status"], "LOCKED_DERIVED_THIRD_FRIDAY_RULE_FROM_GENERIC_CME_STATIC_SOURCE")
        self.assertEqual(status["contract_count"], 13)
        self.assertEqual(status["cost_value_status"], "FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_EXTRACTED")
        self.assertEqual(status["annual_risk_runtime_source_status"], "FAIL_CLOSED_S09_MES_S03_ANNUAL_RISK_SOURCE_NOT_PRODUCTION_LOCKED")
        self.assertEqual(status["roll_trading_day_semantics_status"], "FAIL_CLOSED_S09_MES_PROVIDER_DATE_ROLL_SEMANTICS_NOT_SOURCE_LOCKED")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        for raw_symbol, blocker_date in {
            "MESH1": "2021-03-19",
            "MESM1": "2021-06-18",
            "MESU1": "2021-09-17",
            "MESZ1": "2021-12-17",
            "MESH2": "2022-03-18",
            "MESM2": "2022-06-17",
            "MESU2": "2022-09-16",
            "MESZ2": "2022-12-16",
            "MESH3": "2023-03-17",
            "MESM3": "2023-06-16",
            "MESU3": "2023-09-15",
            "MESZ3": "2023-12-15",
            "MESH4": "2024-03-15",
        }.items():
            self.assertIn(f"{raw_symbol},{blocker_date}", lifecycle)
        self.assertIn("no OHLCV request", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no cost computation", text)
        self.assertIn("no S09 forecast computation", text)
        self.assertIn("cme_mes_contract_specs_extract.md", source_hashes)
        self.assertIn("cme_micro_emini_faq_extract.md", source_hashes)
        self.assertIn("cme_settlement_extract.md", source_hashes)
        self.assertIn("cme_historical_fees_source_location_extract.md", source_hashes)
        self.assertIn("cme_current_fees_source_location_extract.md", source_hashes)
        self.assertIn("20260603_S09_MES_HISTORICAL_LIFECYCLE_ledger.csv", packet_hashes)
        self.assertIn("20260603_S09_MES_HISTORICAL_LIFECYCLE_COST_RISK_EXTRACTION_status.json", packet_hashes)

    def test_roll_risk_cost_value_lock_result_partially_locks_method_but_not_strategy_input(self) -> None:
        result_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_VALUE_LOCK_RESULT_2026-06-03.md"
        )
        status_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_risk_cost_value_lock"
            / "2022-01-03_2023-12-29"
            / "status"
            / "20260603_S09_MES_ROLL_RISK_COST_VALUE_LOCK_status.json"
        )
        readiness_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_risk_cost_value_lock"
            / "2022-01-03_2023-12-29"
            / "readiness"
            / "20260603_S09_MES_ROLL_RISK_COST_VALUE_LOCK_readiness_ledger.csv"
        )
        roll_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_risk_cost_value_lock"
            / "2022-01-03_2023-12-29"
            / "roll"
            / "20260603_S09_MES_ROLL_SEMANTICS_LOCK_ledger.csv"
        )
        risk_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_risk_cost_value_lock"
            / "2022-01-03_2023-12-29"
            / "risk"
            / "20260603_S09_MES_ANNUAL_RISK_METHOD_LOCK_ledger.csv"
        )
        cost_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_risk_cost_value_lock"
            / "2022-01-03_2023-12-29"
            / "cost"
            / "20260603_S09_MES_COST_VALUE_LOCK_ledger.csv"
        )
        speed_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_risk_cost_value_lock"
            / "2022-01-03_2023-12-29"
            / "speed"
            / "20260603_S09_MES_SPEED_ELIGIBILITY_LOCK_ledger.csv"
        )
        hash_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_risk_cost_value_lock"
            / "2022-01-03_2023-12-29"
            / "hashes"
            / "20260603_S09_MES_ROLL_RISK_COST_VALUE_LOCK_sha256.txt"
        )

        text = result_path.read_text(encoding="utf-8")
        status = json.loads(status_path.read_text(encoding="utf-8"))
        readiness = readiness_path.read_text(encoding="utf-8")
        roll = roll_path.read_text(encoding="utf-8")
        risk = risk_path.read_text(encoding="utf-8")
        cost = cost_path.read_text(encoding="utf-8")
        speed = speed_path.read_text(encoding="utf-8")
        hashes = hash_path.read_text(encoding="utf-8")

        self.assertEqual(status["status"], "PARTIAL_LOCK_S09_MES_RISK_METHOD_LIFECYCLE_DATES_STRATEGY_INPUT_FAIL_CLOSED")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["new_provider_data_download"], "NO")
        self.assertEqual(status["market_row_parsing"], "NO")
        self.assertEqual(status["historical_contract_lifecycle_status"], "LOCKED_DERIVED_THIRD_FRIDAY_RULE_FROM_GENERIC_CME_STATIC_SOURCE")
        self.assertEqual(status["annual_risk_source_method_status"], "LOCKED_SOURCE_METHOD_PART_ONE_S03_VARIABLE_RISK_FAMILY")
        self.assertEqual(status["annual_risk_runtime_value_status"], "FAIL_CLOSED_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_NOT_EXECUTED")
        self.assertEqual(status["roll_trading_day_semantics_status"], "FAIL_CLOSED_S09_MES_PROVIDER_DATE_SUNDAY_ROWS_NOT_NORMALIZED_TO_EXCHANGE_COMPLETED_TRADING_DAY")
        self.assertEqual(status["cost_value_status"], "FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_EXTRACTED")
        self.assertEqual(status["speed_cost_eligibility_status"], "FAIL_CLOSED_S09_MES_SPEED_COST_ELIGIBILITY_NOT_COMPUTABLE")
        self.assertEqual(status["eligible_speed_set_status"], "FAIL_CLOSED_S09_MES_ELIGIBLE_SPEED_SET_NOT_LOCKED")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertIn("annual_risk_source_method_status,LOCKED_SOURCE_METHOD_PART_ONE_S03_VARIABLE_RISK_FAMILY", readiness)
        self.assertIn("roll_trading_day_semantics_status,FAIL_CLOSED_S09_MES_PROVIDER_DATE_SUNDAY_ROWS_NOT_NORMALIZED_TO_EXCHANGE_COMPLETED_TRADING_DAY", readiness)
        self.assertIn("STATIC_LIFECYCLE_BUFFER_ROLL_5_COMPLETED_PROVIDER_DATES", roll)
        self.assertIn("Sunday provider-date labels", roll)
        self.assertIn("EWMA32", risk)
        self.assertIn("30/70", risk)
        self.assertIn("source method only", risk)
        self.assertIn("exchange_fee_value,FAIL_CLOSED_S09_MES_EXCHANGE_FEE_VALUE_NOT_EXTRACTED", cost)
        self.assertIn("broker_commission_value,FAIL_CLOSED_S09_MES_BROKER_COMMISSION_NOT_LOCKED", cost)
        self.assertIn("EWMAC2,98.5", speed)
        self.assertIn("EWMAC64,5.2", speed)
        self.assertIn("0.15 SR", speed)
        self.assertIn("no Databento API call", text)
        self.assertIn("no OHLCV request", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no risk runtime execution", text)
        self.assertIn("no cost computation", text)
        self.assertIn("no S09 forecast computation", text)
        self.assertIn("no backtests", text)
        self.assertIn("CARVER_S09_MES_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_VALUE_LOCK_RESULT_2026-06-03.md", hashes)
        self.assertIn("20260603_S09_MES_ROLL_RISK_COST_VALUE_LOCK_status.json", hashes)
        for line in hashes.splitlines():
            if not line.strip():
                continue
            expected_hash, relative_path = line.split("  ", 1)
            actual_hash = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest().upper()
            self.assertEqual(actual_hash, expected_hash)

    def test_roll_date_normalization_runtime_risk_cost_execution_shape_gate_is_strict(self) -> None:
        gate_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE_2026-06-03.md"
        )
        text = gate_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_GATE_NOT_EXECUTION", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("MES", text)
        self.assertIn("2022-01-03 through 2023-12-29", text)
        self.assertIn("S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE", text)
        self.assertIn("Sunday provider-date labels", text)
        self.assertIn("exchange completed trading-date authority", text)
        self.assertIn("no silent date shifting", text)
        self.assertIn("annualized percentage-return risk", text)
        self.assertIn("EWMA32", text)
        self.assertIn("30/70", text)
        self.assertIn("daily_price_risk = current_price * annual_percentage_risk / 16", text)
        self.assertIn("historical MES exchange/clearing/regulatory/broker/spread/slippage", text)
        self.assertIn("risk-adjusted cost per trade", text)
        self.assertIn("0.15 SR", text)
        self.assertIn("EWMAC2", text)
        self.assertIn("EWMAC64", text)
        self.assertIn("Table 36 FDM", text)
        self.assertIn("no default all-six-speed assumption", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("later data must not shape parameters, thresholds, filters, costs, speed selection, FDM selection, or rescue choices", text)
        self.assertIn("if the oldest available authorized MES data is insufficient, fail closed rather than silently designing on newer data", text)
        self.assertIn("READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST", text)
        self.assertIn("FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY", text)
        self.assertIn("no Databento API access", text)
        self.assertIn("no provider login", text)
        self.assertIn("no OHLCV request", text)
        self.assertIn("no new data download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no risk runtime execution", text)
        self.assertIn("no cost computation", text)
        self.assertIn("no S09 forecast computation", text)
        self.assertIn("no diagnostics", text)
        self.assertIn("no backtests", text)
        self.assertIn("no CFD adapter work", text)
        self.assertIn("no old QuantLab active-pipeline use", text)
        self.assertIn("no TEST", text)
        self.assertIn("no VALIDATION", text)
        self.assertIn("no OOS", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)
        self.assertIn("no deployment", text)
        self.assertIn("no trading", text)
        self.assertIn("no promotion", text)
        self.assertIn("no Git staging", text)
        self.assertIn("no remote operations", text)

    def test_roll_risk_cost_authorization_ready_packet_preserves_scope(self) -> None:
        packet_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_ROLL_RISK_COST_AUTHORIZATION_READY_PACKET_2026-06-03.md"
        )
        text = packet_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_ROLL_RISK_COST_AUTHORIZATION_READY_PACKET_NOT_AUTHORIZATION_NOT_EXECUTION", text)
        self.assertIn("READY_FOR_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_AUTHORIZATION_REQUEST_NOT_EXECUTION", text)
        self.assertIn("S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("MES", text)
        self.assertIn("2022-01-03 through 2023-12-29", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("later data must not shape parameters, thresholds, filters, costs, speed selection, FDM selection, or rescue choices", text)
        self.assertIn("Allowed if separately authorized", text)
        self.assertIn("roll-date normalization ledger", text)
        self.assertIn("annual-risk runtime ledger", text)
        self.assertIn("daily price-risk runtime ledger", text)
        self.assertIn("cost value ledger", text)
        self.assertIn("risk-adjusted cost ledger", text)
        self.assertIn("speed eligibility ledger", text)
        self.assertIn("No Databento API access unless explicitly restated by the operator", text)
        self.assertIn("No backtest, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", text)
        self.assertIn("Copy-Ready Authorization Prompt", text)
        self.assertIn("Operator authorizes one bounded S09 MES source-native Development/Reconciliation roll-date normalization and runtime risk/cost execution gate", text)
        self.assertIn("This packet is not authorization", text)

    def test_post_authorization_roll_risk_cost_execution_plan_is_process_safe(self) -> None:
        plan_path = (
            ROOT
            / "docs"
            / "superpowers"
            / "plans"
            / "2026-06-03-s09-mes-roll-risk-cost-execution.md"
        )
        text = plan_path.read_text(encoding="utf-8")

        self.assertIn("# S09 MES Roll Risk Cost Execution Implementation Plan", text)
        self.assertIn("REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development", text)
        self.assertIn("Goal:", text)
        self.assertIn("S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("2022-01-03 through 2023-12-29", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("Task 1: Authorization And Input Hash Preflight", text)
        self.assertIn("Task 2: Roll Date Normalization Ledger", text)
        self.assertIn("Task 3: Annual And Daily Price Risk Runtime Ledgers", text)
        self.assertIn("Task 4: Historical MES Cost And Risk-Adjusted Cost Ledgers", text)
        self.assertIn("Task 5: Speed Eligibility And Readiness Status", text)
        self.assertIn("Task 6: Automatic Local Hostile Audit And Verification", text)
        self.assertIn("tests/test_s09_mes_lineage_synthetic.py", text)
        self.assertIn("tools/databento/carver_s09_mes_roll_risk_cost_execution.py", text)
        self.assertIn("roll_date_normalization/<STAMP>_S09_MES_ROLL_DATE_NORMALIZATION_ledger.csv", text)
        self.assertIn("risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv", text)
        self.assertIn("risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv", text)
        self.assertIn("cost/<STAMP>_S09_MES_COST_VALUE_ledger.csv", text)
        self.assertIn("cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv", text)
        self.assertIn("speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv", text)
        self.assertIn("No Databento API access unless explicitly restated by the operator", text)
        self.assertIn("No forecast computation, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", text)
        self.assertNotIn("TBD", text)
        self.assertNotIn("TODO", text)

    def test_s09_mes_roll_risk_cost_execution_requires_explicit_authorization(self) -> None:
        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESRollRiskCostExecutionConfig,
            run_s09_mes_roll_risk_cost_execution,
        )

        config = S09MESRollRiskCostExecutionConfig(
            execution_authorized=False,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            target_start="2022-01-03",
            target_end="2023-12-29",
        )

        with self.assertRaises(CarverBlocked):
            run_s09_mes_roll_risk_cost_execution(config)

    def test_s09_mes_roll_risk_cost_execution_authorization_guard_audit_preserves_boundary(self) -> None:
        audit_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_ROLL_RISK_COST_EXECUTION_AUTHORIZATION_GUARD_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
        )
        text = audit_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_S09_MES_ROLL_RISK_COST_AUTHORIZATION_GUARD_NOT_DATA_NOT_EXECUTION_NOT_BACKTEST", text)
        self.assertIn("run_s09_mes_roll_risk_cost_execution", text)
        self.assertIn("execution_authorized=False", text)
        self.assertIn("S09 MES roll risk cost execution is not operator-authorized", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("no Databento API access", text)
        self.assertIn("no provider download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no roll execution", text)
        self.assertIn("no runtime risk execution", text)
        self.assertIn("no cost extraction", text)
        self.assertIn("no forecast computation", text)
        self.assertIn("no backtests", text)
        self.assertIn("no OOS", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)
        self.assertIn("no Git staging", text)

    def test_s09_mes_roll_normalization_ledger_renderer_outputs_hash_bound_completed_dates(self) -> None:
        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESRollNormalizationLedgerRow,
            render_s09_mes_roll_normalization_ledger_csv,
        )

        csv_text = render_s09_mes_roll_normalization_ledger_csv(
            (
                S09MESRollNormalizationLedgerRow(
                    provider_date=date(2022, 3, 13),
                    completed_trading_date=date(2022, 3, 14),
                    old_symbol="MESH2",
                    new_symbol="MESM2",
                    authority_source="AUTHORIZED_CME_COMPLETED_TRADING_DAY_AUTHORITY",
                    authority_sha256="A" * 64,
                    status="LOCKED_SOURCE_NATIVE_COMPLETED_TRADING_DATE",
                ),
            )
        )

        self.assertEqual(
            csv_text,
            (
                "provider_date,completed_trading_date,old_symbol,new_symbol,authority_source,authority_sha256,status\r\n"
                "2022-03-13,2022-03-14,MESH2,MESM2,AUTHORIZED_CME_COMPLETED_TRADING_DAY_AUTHORITY,"
                f"{'A' * 64},LOCKED_SOURCE_NATIVE_COMPLETED_TRADING_DATE\r\n"
            ),
        )

    def test_s09_mes_roll_normalization_ledger_renderer_fails_closed_on_drift(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
            S09MESRollNormalizationLedgerRow,
            render_s09_mes_roll_normalization_ledger_csv,
        )

        base = S09MESRollNormalizationLedgerRow(
            provider_date=date(2022, 3, 13),
            completed_trading_date=date(2022, 3, 14),
            old_symbol="MESH2",
            new_symbol="MESM2",
            authority_source="AUTHORIZED_CME_COMPLETED_TRADING_DAY_AUTHORITY",
            authority_sha256="A" * 64,
            status="LOCKED_SOURCE_NATIVE_COMPLETED_TRADING_DATE",
        )

        hostile_rows = (
            (),
            (replace(base, provider_date=datetime(2022, 3, 13, tzinfo=timezone.utc)),),
            (replace(base, completed_trading_date=datetime(2022, 3, 14, tzinfo=timezone.utc)),),
            (replace(base, old_symbol="ESH2"),),
            (replace(base, new_symbol="ESM2"),),
            (replace(base, old_symbol="MESM2", new_symbol="MESH2"),),
            (replace(base, authority_source=""),),
            (replace(base, authority_sha256=""),),
            (replace(base, authority_sha256="Z" * 64),),
            (replace(base, status="PROVISIONAL"),),
        )
        for rows in hostile_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_roll_normalization_ledger_csv(rows)

    def test_s09_mes_roll_normalization_ledger_audit_preserves_no_execution_boundary(self) -> None:
        audit_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_ROLL_NORMALIZATION_LEDGER_RENDERER_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
        )
        text = audit_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_S09_MES_ROLL_NORMALIZATION_LEDGER_RENDERER_NOT_DATA_NOT_EXECUTION_NOT_BACKTEST", text)
        self.assertIn("render_s09_mes_roll_normalization_ledger_csv", text)
        self.assertIn("provider_date,completed_trading_date,old_symbol,new_symbol,authority_source,authority_sha256,status", text)
        self.assertIn("LOCKED_SOURCE_NATIVE_COMPLETED_TRADING_DATE", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("no Databento API access", text)
        self.assertIn("no provider download", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no roll execution", text)
        self.assertIn("no runtime risk execution", text)
        self.assertIn("no cost extraction", text)
        self.assertIn("no forecast computation", text)
        self.assertIn("no backtests", text)
        self.assertIn("no OOS", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)
        self.assertIn("no Git staging", text)

    def test_s09_mes_roll_risk_cost_execution_result_preserves_no_backtest_boundary(self) -> None:
        result_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_RESULT_2026-06-03.md"
        )
        text = result_path.read_text(encoding="utf-8")

        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("2022-01-03 through 2023-12-29", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("no forecast computation", text)
        self.assertIn("no diagnostics", text)
        self.assertIn("no backtests", text)
        self.assertIn("no OOS", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)

    def test_s09_mes_runtime_risk_cost_input_lock_authorization_packet_preserves_next_boundary(self) -> None:
        packet_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_AUTHORIZATION_READY_PACKET_2026-06-03.md"
        )
        text = packet_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION", text)
        self.assertIn("S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_GATE", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("MES", text)
        self.assertIn("machinery_development_slice: 2019-05-05 through 2020-04-05", text)
        self.assertIn("runtime_input_lock_scope: oldest minimum machinery-development slice only", text)
        self.assertIn("2022-2023 is not the Dev/Reconciliation default", text)
        self.assertIn("3:3:4 TEST/VALIDATION/LOCKBOX windows are separately locked and separately gated", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("Required unresolved inputs", text)
        self.assertIn("annual-risk runtime values", text)
        self.assertIn("daily price-risk values", text)
        self.assertIn("historical MES exchange/clearing/regulatory/broker/spread/slippage cost values", text)
        self.assertIn("risk-adjusted cost values", text)
        self.assertIn("speed eligibility values", text)
        self.assertIn("No Databento API access unless explicitly restated by the operator", text)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", text)
        self.assertIn("Operator authorizes one bounded S09 MES source-native Development/Reconciliation runtime risk and historical cost input-lock gate using oldest authorized completed source-native data first", text)
        self.assertIn("This packet is not authorization", text)
        self.assertNotIn("target_window: 2022-01-03 through 2023-12-29", text)

    def test_s09_mes_runtime_risk_cost_input_lock_plan_is_process_safe(self) -> None:
        plan_path = (
            ROOT
            / "docs"
            / "superpowers"
            / "plans"
            / "2026-06-03-s09-mes-runtime-risk-cost-input-lock.md"
        )
        text = plan_path.read_text(encoding="utf-8")

        self.assertIn("# S09 MES Runtime Risk Cost Input Lock Implementation Plan", text)
        self.assertIn("REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development", text)
        self.assertIn("S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_GATE", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("machinery_development_slice: 2019-05-05 through 2020-04-05", text)
        self.assertIn("runtime_input_lock_scope: oldest minimum machinery-development slice only", text)
        self.assertIn("3:3:4 TEST/VALIDATION/LOCKBOX windows are separately locked and separately gated", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("Task 1: Authorization Guard And Input Manifest", text)
        self.assertIn("Task 2: Runtime Annual Risk And Daily Price Risk Ledgers", text)
        self.assertIn("Task 3: Historical Cost Value Lock", text)
        self.assertIn("Task 4: Risk-Adjusted Cost And Speed Eligibility", text)
        self.assertIn("Task 5: Strategy Input Readiness Packet", text)
        self.assertIn("No Databento API access unless explicitly restated by the operator", text)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", text)
        self.assertIn("Operator authorizes one bounded S09 MES source-native Development/Reconciliation runtime risk and historical cost input-lock gate using oldest authorized completed source-native data first", text)
        self.assertNotIn("target_window: 2022-01-03 through 2023-12-29", text)
        self.assertNotIn("mes_runtime_risk_cost_input_lock/2022-01-03_2023-12-29", text)
        self.assertNotIn("TBD", text)
        self.assertNotIn("TODO", text)

    def test_s09_mes_runtime_risk_cost_input_lock_requires_authorization(self) -> None:
        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockConfig,
            run_s09_mes_runtime_risk_cost_input_lock,
        )

        config = S09MESRuntimeRiskCostInputLockConfig(
            execution_authorized=False,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice_start="2019-05-05",
            machinery_development_slice_end="2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
        )

        with self.assertRaises(CarverBlocked):
            run_s09_mes_runtime_risk_cost_input_lock(config)

    def test_s09_mes_runtime_risk_cost_input_lock_authorized_runner_returns_fail_closed_bundle_without_io(self) -> None:
        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockConfig,
            run_s09_mes_runtime_risk_cost_input_lock,
        )

        config = S09MESRuntimeRiskCostInputLockConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice_start="2019-05-05",
            machinery_development_slice_end="2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
        )

        bundle = run_s09_mes_runtime_risk_cost_input_lock(config)

        status_path = (
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/"
            "status/20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_status.json"
        )
        hash_path = (
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/"
            "hashes/20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_sha256.txt"
        )
        self.assertIn(status_path, bundle)
        self.assertIn(hash_path, bundle)
        status = json.loads(bundle[status_path])
        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_NOT_STRATEGY_READY")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["new_provider_data_download"], "NO")
        self.assertEqual(status["market_row_parsing"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertNotIn("2022-01-03", "\n".join(bundle))
        self.assertNotIn("2023-12-29", "\n".join(bundle))
        self.assertNotIn(hash_path, bundle[hash_path])

    def test_s09_mes_runtime_risk_cost_input_manifest_requires_local_hash_bound_machinery_slice(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockInputManifestRow,
            render_s09_mes_runtime_risk_cost_input_manifest_csv,
        )

        base = S09MESRuntimeRiskCostInputLockInputManifestRow(
            input_name="machinery_dev_lineage_status",
            relative_path=(
                "docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/"
                "status/20260603_S09_MES_MACHINERY_DEV_LINEAGE_status.json"
            ),
            required_status="FAIL_CLOSED_S09_MES_MACHINERY_DEV_LINEAGE_NOT_STRATEGY_INPUT",
            sha256="A" * 64,
            status="HASH_BOUND_LOCAL_MACHINERY_SLICE_INPUT",
        )

        csv_text = render_s09_mes_runtime_risk_cost_input_manifest_csv((base,))

        self.assertEqual(
            csv_text,
            (
                "input_name,relative_path,required_status,sha256,status\r\n"
                "machinery_dev_lineage_status,"
                "docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/"
                "status/20260603_S09_MES_MACHINERY_DEV_LINEAGE_status.json,"
                "FAIL_CLOSED_S09_MES_MACHINERY_DEV_LINEAGE_NOT_STRATEGY_INPUT,"
                f"{'A' * 64},HASH_BOUND_LOCAL_MACHINERY_SLICE_INPUT\r\n"
            ),
        )

        hostile_rows = (
            (),
            (replace(base, input_name=""),),
            (replace(base, relative_path="C:/Users/openclaw/Desktop/Carver/docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/status/x.json"),),
            (replace(base, relative_path="../docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/status/x.json"),),
            (replace(base, relative_path="docs/researchops/s09/mes_runtime_risk_cost_input_lock/2022-01-03_2023-12-29/status/x.json"),),
            (replace(base, relative_path="docs/researchops/s09/mes_test/2020-04-06_2022-02-08/status/x.json"),),
            (replace(base, required_status=""),),
            (replace(base, sha256=""),),
            (replace(base, sha256="Z" * 64),),
            (replace(base, status="PROVISIONAL"),),
        )
        for rows in hostile_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_runtime_risk_cost_input_manifest_csv(rows)

    def test_s09_mes_runtime_risk_cost_input_lock_renders_runtime_risk_ledgers_fail_closed_on_drift(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockAnnualRiskLedgerRow,
            S09MESRuntimeRiskCostInputLockDailyPriceRiskLedgerRow,
            render_s09_mes_runtime_risk_cost_annual_risk_ledger_csv,
            render_s09_mes_runtime_risk_cost_daily_price_risk_ledger_csv,
        )

        annual = S09MESRuntimeRiskCostInputLockAnnualRiskLedgerRow(
            completed_trading_date=date(2020, 3, 2),
            long_run_annual_risk=0.18,
            current_ewma32_annual_risk=0.22,
            annual_percentage_risk=0.208,
            source_sha256="B" * 64,
            status="LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE",
        )
        daily = S09MESRuntimeRiskCostInputLockDailyPriceRiskLedgerRow(
            completed_trading_date=date(2020, 3, 2),
            current_price=3000.0,
            annual_percentage_risk=0.208,
            daily_price_risk_currency=39.0,
            source_sha256="C" * 64,
            status="LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE",
        )

        self.assertEqual(
            render_s09_mes_runtime_risk_cost_annual_risk_ledger_csv((annual,)),
            (
                "completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,"
                "annual_percentage_risk,source_sha256,status\r\n"
                f"2020-03-02,0.18,0.22,0.208,{'B' * 64},"
                "LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE\r\n"
            ),
        )
        self.assertEqual(
            render_s09_mes_runtime_risk_cost_daily_price_risk_ledger_csv((daily,)),
            (
                "completed_trading_date,current_price,annual_percentage_risk,"
                "daily_price_risk_currency,source_sha256,status\r\n"
                f"2020-03-02,3000.0,0.208,39.0,{'C' * 64},"
                "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE\r\n"
            ),
        )

        hostile_annual_rows = (
            (),
            (replace(annual, completed_trading_date=datetime(2020, 3, 2, tzinfo=timezone.utc)),),
            (replace(annual, long_run_annual_risk=0.0),),
            (replace(annual, current_ewma32_annual_risk=0.0),),
            (replace(annual, annual_percentage_risk=0.21),),
            (replace(annual, source_sha256=""),),
            (replace(annual, source_sha256="Z" * 64),),
            (replace(annual, status="PROVISIONAL"),),
        )
        for rows in hostile_annual_rows:
            with self.subTest(annual_rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_runtime_risk_cost_annual_risk_ledger_csv(rows)

        hostile_daily_rows = (
            (),
            (replace(daily, completed_trading_date=datetime(2020, 3, 2, tzinfo=timezone.utc)),),
            (replace(daily, current_price=0.0),),
            (replace(daily, annual_percentage_risk=0.0),),
            (replace(daily, daily_price_risk_currency=38.0),),
            (replace(daily, source_sha256=""),),
            (replace(daily, source_sha256="Z" * 64),),
            (replace(daily, status="PROVISIONAL"),),
        )
        for rows in hostile_daily_rows:
            with self.subTest(daily_rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_runtime_risk_cost_daily_price_risk_ledger_csv(rows)

    def test_s09_mes_runtime_risk_cost_input_lock_renders_cost_value_ledger_fail_closed_on_drift(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockCostValueLedgerRow,
            render_s09_mes_runtime_risk_cost_cost_value_ledger_csv,
        )

        rows = (
            S09MESRuntimeRiskCostInputLockCostValueLedgerRow(
                completed_trading_date=date(2020, 3, 2),
                component_name="exchange_fee",
                amount_currency=0.20,
                currency="USD",
                charge_timing="PER_SIDE",
                effective_start=date(2019, 5, 5),
                effective_end=date(2020, 4, 5),
                source_label="HASH_BOUND_HISTORICAL_MES_EXCHANGE_FEE_SOURCE",
                source_sha256="D" * 64,
                status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
            ),
            S09MESRuntimeRiskCostInputLockCostValueLedgerRow(
                completed_trading_date=date(2020, 3, 2),
                component_name="clearing_regulatory_fee",
                amount_currency=0.04,
                currency="USD",
                charge_timing="PER_SIDE",
                effective_start=date(2019, 5, 5),
                effective_end=date(2020, 4, 5),
                source_label="HASH_BOUND_HISTORICAL_MES_CLEARING_REGULATORY_SOURCE",
                source_sha256="E" * 64,
                status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
            ),
            S09MESRuntimeRiskCostInputLockCostValueLedgerRow(
                completed_trading_date=date(2020, 3, 2),
                component_name="broker_commission",
                amount_currency=0.25,
                currency="USD",
                charge_timing="PER_SIDE",
                effective_start=date(2019, 5, 5),
                effective_end=date(2020, 4, 5),
                source_label="HASH_BOUND_HISTORICAL_MES_BROKER_COMMISSION_SOURCE",
                source_sha256="F" * 64,
                status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
            ),
            S09MESRuntimeRiskCostInputLockCostValueLedgerRow(
                completed_trading_date=date(2020, 3, 2),
                component_name="spread_slippage",
                amount_currency=1.25,
                currency="USD",
                charge_timing="ROUND_TURN",
                effective_start=date(2019, 5, 5),
                effective_end=date(2020, 4, 5),
                source_label="HASH_BOUND_HISTORICAL_MES_SPREAD_SLIPPAGE_POLICY",
                source_sha256="1" * 64,
                status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
            ),
        )

        csv_text = render_s09_mes_runtime_risk_cost_cost_value_ledger_csv(rows)

        self.assertEqual(
            csv_text,
            (
                "completed_trading_date,component_name,amount_currency,currency,charge_timing,"
                "effective_start,effective_end,source_label,source_sha256,status\r\n"
                f"2020-03-02,exchange_fee,0.2,USD,PER_SIDE,2019-05-05,2020-04-05,"
                f"HASH_BOUND_HISTORICAL_MES_EXCHANGE_FEE_SOURCE,{'D' * 64},"
                "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE\r\n"
                f"2020-03-02,clearing_regulatory_fee,0.04,USD,PER_SIDE,2019-05-05,2020-04-05,"
                f"HASH_BOUND_HISTORICAL_MES_CLEARING_REGULATORY_SOURCE,{'E' * 64},"
                "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE\r\n"
                f"2020-03-02,broker_commission,0.25,USD,PER_SIDE,2019-05-05,2020-04-05,"
                f"HASH_BOUND_HISTORICAL_MES_BROKER_COMMISSION_SOURCE,{'F' * 64},"
                "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE\r\n"
                f"2020-03-02,spread_slippage,1.25,USD,ROUND_TURN,2019-05-05,2020-04-05,"
                f"HASH_BOUND_HISTORICAL_MES_SPREAD_SLIPPAGE_POLICY,{'1' * 64},"
                "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE\r\n"
            ),
        )

        hostile_row_sets = (
            (),
            rows[:3],
            (rows[1], rows[0], rows[2], rows[3]),
            (replace(rows[0], component_name="exchange_fee"), replace(rows[0], component_name="exchange_fee"), rows[2], rows[3]),
            (replace(rows[0], completed_trading_date=datetime(2020, 3, 2, tzinfo=timezone.utc)), *rows[1:]),
            (replace(rows[0], component_name="current_fee_default"), *rows[1:]),
            (replace(rows[0], amount_currency=-0.01), *rows[1:]),
            (replace(rows[0], currency="EUR"), *rows[1:]),
            (replace(rows[0], charge_timing="PER_CONTRACT"), *rows[1:]),
            (replace(rows[0], effective_start=date(2020, 3, 3)), *rows[1:]),
            (replace(rows[0], effective_end=date(2020, 3, 1)), *rows[1:]),
            (replace(rows[0], source_label=""), *rows[1:]),
            (replace(rows[0], source_sha256=""), *rows[1:]),
            (replace(rows[0], source_sha256="Z" * 64), *rows[1:]),
            (replace(rows[0], status="PROVISIONAL"), *rows[1:]),
        )
        for row_set in hostile_row_sets:
            with self.subTest(row_set=row_set):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_runtime_risk_cost_cost_value_ledger_csv(row_set)

    def test_s09_mes_runtime_risk_cost_input_lock_renders_risk_adjusted_cost_and_speed_ledgers_fail_closed_on_drift(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockRiskAdjustedCostLedgerRow,
            S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow,
            render_s09_mes_runtime_risk_cost_risk_adjusted_cost_ledger_csv,
            render_s09_mes_runtime_risk_cost_speed_eligibility_ledger_csv,
        )

        risk_adjusted = S09MESRuntimeRiskCostInputLockRiskAdjustedCostLedgerRow(
            completed_trading_date=date(2020, 3, 2),
            total_cost_per_trade_currency=2.0,
            daily_price_risk_currency=40.0,
            risk_adjusted_cost_per_trade_sr=0.000625,
            status="LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE",
        )
        speed_rows = (
            S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow(
                span=2,
                turnover=98.5,
                risk_adjusted_cost_per_trade_sr=0.001,
                threshold_sr=0.15,
                eligible=True,
                status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
            ),
            S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow(
                span=4,
                turnover=50.2,
                risk_adjusted_cost_per_trade_sr=0.001,
                threshold_sr=0.15,
                eligible=True,
                status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
            ),
            S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow(
                span=8,
                turnover=25.4,
                risk_adjusted_cost_per_trade_sr=0.001,
                threshold_sr=0.15,
                eligible=True,
                status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
            ),
            S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow(
                span=16,
                turnover=13.2,
                risk_adjusted_cost_per_trade_sr=0.001,
                threshold_sr=0.15,
                eligible=True,
                status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
            ),
            S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow(
                span=32,
                turnover=7.6,
                risk_adjusted_cost_per_trade_sr=0.001,
                threshold_sr=0.15,
                eligible=True,
                status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
            ),
            S09MESRuntimeRiskCostInputLockSpeedEligibilityLedgerRow(
                span=64,
                turnover=5.2,
                risk_adjusted_cost_per_trade_sr=0.001,
                threshold_sr=0.15,
                eligible=True,
                status="LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE",
            ),
        )

        self.assertEqual(
            render_s09_mes_runtime_risk_cost_risk_adjusted_cost_ledger_csv((risk_adjusted,)),
            (
                "completed_trading_date,total_cost_per_trade_currency,daily_price_risk_currency,"
                "risk_adjusted_cost_per_trade_sr,status\r\n"
                "2020-03-02,2.0,40.0,0.000625,LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE\r\n"
            ),
        )
        self.assertEqual(
            render_s09_mes_runtime_risk_cost_speed_eligibility_ledger_csv(speed_rows),
            (
                "span,turnover,risk_adjusted_cost_per_trade_sr,threshold_sr,eligible,status\r\n"
                "2,98.5,0.001,0.15,True,LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE\r\n"
                "4,50.2,0.001,0.15,True,LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE\r\n"
                "8,25.4,0.001,0.15,True,LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE\r\n"
                "16,13.2,0.001,0.15,True,LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE\r\n"
                "32,7.6,0.001,0.15,True,LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE\r\n"
                "64,5.2,0.001,0.15,True,LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE\r\n"
            ),
        )

        hostile_risk_adjusted_rows = (
            (),
            (replace(risk_adjusted, completed_trading_date=datetime(2020, 3, 2, tzinfo=timezone.utc)),),
            (replace(risk_adjusted, total_cost_per_trade_currency=0.0),),
            (replace(risk_adjusted, daily_price_risk_currency=0.0),),
            (replace(risk_adjusted, risk_adjusted_cost_per_trade_sr=0.06),),
            (replace(risk_adjusted, status="PROVISIONAL"),),
        )
        for rows in hostile_risk_adjusted_rows:
            with self.subTest(risk_adjusted_rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_runtime_risk_cost_risk_adjusted_cost_ledger_csv(rows)

        hostile_speed_rows = (
            (),
            speed_rows[:5],
            (speed_rows[1], speed_rows[0], *speed_rows[2:]),
            (replace(speed_rows[0], span=3), *speed_rows[1:]),
            (replace(speed_rows[0], turnover=99.0), *speed_rows[1:]),
            (replace(speed_rows[0], risk_adjusted_cost_per_trade_sr=0.0), *speed_rows[1:]),
            (replace(speed_rows[0], threshold_sr=0.20), *speed_rows[1:]),
            (replace(speed_rows[0], eligible=False), *speed_rows[1:]),
            (replace(speed_rows[0], eligible="True"), *speed_rows[1:]),
            (replace(speed_rows[0], status="ASSUMED_ALL_SIX_SPEEDS"), *speed_rows[1:]),
        )
        for rows in hostile_speed_rows:
            with self.subTest(speed_rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_runtime_risk_cost_speed_eligibility_ledger_csv(rows)

    def test_s09_mes_runtime_risk_cost_input_lock_status_and_provenance_preserve_fail_closed_boundary(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockStatus,
            render_s09_mes_runtime_risk_cost_input_lock_provenance_md,
            render_s09_mes_runtime_risk_cost_input_lock_status_json,
        )

        payload = S09MESRuntimeRiskCostInputLockStatus(
            status="FAIL_CLOSED_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_NOT_STRATEGY_READY",
            gate="S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_GATE",
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access="NO",
            new_provider_data_download="NO",
            market_row_parsing="NO",
            forecast_computation="NO",
            diagnostics_run="NO",
            backtests_run="NO",
            test_validation_lockbox_forward_access="NO",
            strategy_input_readiness_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
        )

        status_text = render_s09_mes_runtime_risk_cost_input_lock_status_json(payload)
        status = json.loads(status_text)

        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_NOT_STRATEGY_READY")
        self.assertEqual(status["machinery_development_slice"], "2019-05-05 through 2020-04-05")
        self.assertEqual(status["runtime_input_lock_scope"], "oldest minimum machinery-development slice only")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertNotIn("2022-01-03", status_text)
        self.assertNotIn("2023-12-29", status_text)

        provenance = render_s09_mes_runtime_risk_cost_input_lock_provenance_md(payload)
        self.assertIn("S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_GATE", provenance)
        self.assertIn("2019-05-05 through 2020-04-05", provenance)
        self.assertIn("oldest minimum machinery-development slice only", provenance)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations were performed.", provenance)
        self.assertNotIn("2022-01-03", provenance)
        self.assertNotIn("2023-12-29", provenance)

        hostile_payloads = (
            replace(payload, status="READY"),
            replace(payload, gate="S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE"),
            replace(payload, lane_class="CFD_ADAPTER"),
            replace(payload, root="ES"),
            replace(payload, row_id="WRONG"),
            replace(payload, machinery_development_slice="2022-01-03 through 2023-12-29"),
            replace(payload, runtime_input_lock_scope="two year dev window"),
            replace(payload, design_ordering="latest data first"),
            replace(payload, databento_api_access="YES"),
            replace(payload, new_provider_data_download="YES"),
            replace(payload, market_row_parsing="YES"),
            replace(payload, forecast_computation="YES"),
            replace(payload, diagnostics_run="YES"),
            replace(payload, backtests_run="YES"),
            replace(payload, test_validation_lockbox_forward_access="YES"),
            replace(payload, strategy_input_readiness_status="S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY"),
        )
        for hostile in hostile_payloads:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_runtime_risk_cost_input_lock_status_json(hostile)

    def test_s09_mes_runtime_risk_cost_input_lock_hash_manifest_is_local_and_deterministic(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockHashManifestEntry,
            render_s09_mes_runtime_risk_cost_input_lock_sha256_manifest,
        )

        status_entry = S09MESRuntimeRiskCostInputLockHashManifestEntry(
            relative_path="docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/status/20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_status.json",
            artifact_text='{"status":"FAIL_CLOSED"}\n',
        )
        provenance_entry = S09MESRuntimeRiskCostInputLockHashManifestEntry(
            relative_path="docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/provenance/20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_provenance.md",
            artifact_text="# provenance\n",
        )

        manifest = render_s09_mes_runtime_risk_cost_input_lock_sha256_manifest(
            (provenance_entry, status_entry)
        )

        expected_status_hash = hashlib.sha256(status_entry.artifact_text.encode("utf-8")).hexdigest().upper()
        expected_provenance_hash = hashlib.sha256(provenance_entry.artifact_text.encode("utf-8")).hexdigest().upper()
        self.assertEqual(
            manifest,
            (
                f"{expected_provenance_hash}  {provenance_entry.relative_path}\n"
                f"{expected_status_hash}  {status_entry.relative_path}\n"
            ),
        )

        hostile_entry_sets = (
            (),
            (replace(status_entry, relative_path=""),),
            (replace(status_entry, relative_path="C:/Users/openclaw/Desktop/Carver/docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/status/x.json"),),
            (replace(status_entry, relative_path="../docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/status/x.json"),),
            (replace(status_entry, relative_path="docs/researchops/s09/mes_runtime_risk_cost_input_lock/2022-01-03_2023-12-29/status/x.json"),),
            (replace(status_entry, relative_path="docs/researchops/s09/mes_validation/2022-02-09_2023-12-13/status/x.json"),),
            (replace(status_entry, artifact_text=""),),
            (status_entry, replace(status_entry, artifact_text="different\n")),
        )
        for entries in hostile_entry_sets:
            with self.subTest(entries=entries):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_runtime_risk_cost_input_lock_sha256_manifest(entries)

    def test_s09_mes_runtime_risk_cost_input_lock_builds_complete_in_memory_artifact_bundle(self) -> None:
        from tools.databento.carver_s09_mes_runtime_risk_cost_input_lock import (  # noqa: PLC0415
            S09MESRuntimeRiskCostInputLockArtifactBundleRequest,
            build_s09_mes_runtime_risk_cost_input_lock_artifact_bundle,
        )

        request = S09MESRuntimeRiskCostInputLockArtifactBundleRequest(
            input_manifest_csv="input_name,relative_path,required_status,sha256,status\r\n",
            annual_risk_csv="completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_sha256,status\r\n",
            daily_price_risk_csv="completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,source_sha256,status\r\n",
            cost_value_csv="completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status\r\n",
            risk_adjusted_cost_csv="completed_trading_date,total_cost_per_trade_currency,daily_price_risk_currency,risk_adjusted_cost_per_trade_sr,status\r\n",
            speed_eligibility_csv="span,turnover,risk_adjusted_cost_per_trade_sr,threshold_sr,eligible,status\r\n",
            status_json='{"status":"FAIL_CLOSED_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_NOT_STRATEGY_READY"}\n',
            provenance_md="# S09 MES Runtime Risk Cost Input Lock Provenance\n",
        )

        bundle = build_s09_mes_runtime_risk_cost_input_lock_artifact_bundle(request)

        expected_paths = (
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/input_manifest/20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_input_manifest.csv",
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/risk/20260603_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv",
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/cost/20260603_S09_MES_COST_VALUE_ledger.csv",
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/cost/20260603_S09_MES_RISK_ADJUSTED_COST_ledger.csv",
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/speed/20260603_S09_MES_SPEED_ELIGIBILITY_ledger.csv",
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/status/20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_status.json",
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/provenance/20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_provenance.md",
            "docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/hashes/20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)
        self.assertEqual(bundle[expected_paths[0]], request.input_manifest_csv)
        self.assertEqual(bundle[expected_paths[7]], request.provenance_md)

        hash_manifest = bundle[expected_paths[8]]
        self.assertIn(expected_paths[0], hash_manifest)
        self.assertIn(expected_paths[7], hash_manifest)
        self.assertNotIn(expected_paths[8], hash_manifest)
        self.assertNotIn("2022-01-03", "\n".join(bundle))
        self.assertNotIn("2023-12-29", "\n".join(bundle))

        hostile_requests = (
            S09MESRuntimeRiskCostInputLockArtifactBundleRequest(
                input_manifest_csv="",
                annual_risk_csv=request.annual_risk_csv,
                daily_price_risk_csv=request.daily_price_risk_csv,
                cost_value_csv=request.cost_value_csv,
                risk_adjusted_cost_csv=request.risk_adjusted_cost_csv,
                speed_eligibility_csv=request.speed_eligibility_csv,
                status_json=request.status_json,
                provenance_md=request.provenance_md,
            ),
            S09MESRuntimeRiskCostInputLockArtifactBundleRequest(
                input_manifest_csv=request.input_manifest_csv,
                annual_risk_csv=request.annual_risk_csv,
                daily_price_risk_csv=request.daily_price_risk_csv,
                cost_value_csv=request.cost_value_csv,
                risk_adjusted_cost_csv=request.risk_adjusted_cost_csv,
                speed_eligibility_csv=request.speed_eligibility_csv,
                status_json='{"status":"READY"}\n',
                provenance_md=request.provenance_md,
            ),
            S09MESRuntimeRiskCostInputLockArtifactBundleRequest(
                input_manifest_csv=request.input_manifest_csv,
                annual_risk_csv=request.annual_risk_csv,
                daily_price_risk_csv=request.daily_price_risk_csv,
                cost_value_csv=request.cost_value_csv,
                risk_adjusted_cost_csv=request.risk_adjusted_cost_csv,
                speed_eligibility_csv=request.speed_eligibility_csv,
                status_json=request.status_json,
                provenance_md="2022-01-03 through 2023-12-29\n",
            ),
        )
        for hostile in hostile_requests:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    build_s09_mes_runtime_risk_cost_input_lock_artifact_bundle(hostile)

    def test_s09_mes_runtime_risk_cost_input_lock_written_packet_is_hash_bound_fail_closed(self) -> None:
        result_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_RESULT_2026-06-03.md"
        )
        audit_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
        )
        output_root = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_runtime_risk_cost_input_lock"
            / "2019-05-05_2020-04-05"
        )
        status_path = output_root / "status" / "20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_status.json"
        hashes_path = output_root / "hashes" / "20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_sha256.txt"
        expected_artifacts = (
            output_root / "input_manifest" / "20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_input_manifest.csv",
            output_root / "risk" / "20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
            output_root / "risk" / "20260603_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv",
            output_root / "cost" / "20260603_S09_MES_COST_VALUE_ledger.csv",
            output_root / "cost" / "20260603_S09_MES_RISK_ADJUSTED_COST_ledger.csv",
            output_root / "speed" / "20260603_S09_MES_SPEED_ELIGIBILITY_ledger.csv",
            status_path,
            output_root / "provenance" / "20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_provenance.md",
            result_path,
            audit_path,
        )

        result = result_path.read_text(encoding="utf-8")
        audit = audit_path.read_text(encoding="utf-8")
        status = json.loads(status_path.read_text(encoding="utf-8"))
        hashes = hashes_path.read_text(encoding="utf-8")

        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_NOT_STRATEGY_READY")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["market_row_parsing"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertIn("SOURCE_NATIVE_FUTURES", result)
        self.assertIn("APPENDIX_C_174_006", result)
        self.assertIn("2019-05-05 through 2020-04-05", result)
        self.assertIn("oldest minimum machinery-development slice only", result)
        self.assertIn("oldest authorized completed source-native data first", result)
        self.assertIn("3:3:4 TEST/VALIDATION/LOCKBOX windows are separately locked and separately gated", result)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", result)
        self.assertIn("LOCAL_HOSTILE_AUDIT_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_FAIL_CLOSED_NO_BACKTEST", audit)
        self.assertIn("header-only fail-closed ledgers", audit)
        self.assertIn("20260603_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_sha256.txt", audit)
        self.assertNotIn("2022-01-03_2023-12-29", result)
        self.assertNotIn("2022-01-03_2023-12-29", audit)

        result_artifact_lines = [line for line in result.splitlines() if line.startswith("- `")]
        audit_artifact_lines = [line for line in audit.splitlines() if line.startswith("- `docs/")]
        self.assertEqual(len(result_artifact_lines), len(set(result_artifact_lines)))
        self.assertEqual(len(audit_artifact_lines), len(set(audit_artifact_lines)))

        for artifact_path in expected_artifacts:
            self.assertTrue(artifact_path.exists(), artifact_path)
            self.assertIn(artifact_path.relative_to(ROOT).as_posix(), hashes)
        self.assertNotIn(hashes_path.relative_to(ROOT).as_posix(), hashes)

        for line in hashes.splitlines():
            if not line.strip():
                continue
            expected_hash, relative_path = line.split("  ", 1)
            actual_hash = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest().upper()
            self.assertEqual(actual_hash, expected_hash)

    def test_s09_mes_strategy_input_evidence_completion_authorization_packet_is_process_only(self) -> None:
        packet_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_AUTHORIZATION_READY_PACKET_2026-06-03.md"
        )
        text = packet_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION", text)
        self.assertIn("S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("2019-05-05 through 2020-04-05", text)
        self.assertIn("oldest minimum machinery-development slice only", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("FAIL_CLOSED_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_NOT_STRATEGY_READY", text)
        self.assertIn("annual-risk runtime values", text)
        self.assertIn("daily price-risk values", text)
        self.assertIn("historical MES exchange/clearing/regulatory/broker/spread/slippage cost values", text)
        self.assertIn("risk-adjusted cost values", text)
        self.assertIn("speed eligibility values", text)
        self.assertIn("official lifecycle evidence", text)
        self.assertIn("roll trading-day semantics", text)
        self.assertIn("3:3:4 TEST/VALIDATION/LOCKBOX windows are separately locked and separately gated", text)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", text)
        self.assertIn("No Databento API access unless explicitly restated by the operator", text)
        self.assertNotIn("2022-01-03_2023-12-29", text)

    def test_s09_mes_strategy_input_next_evidence_authorization_packet_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_strategy_input_next_evidence_authorization_packet_bundle,
        )

        bundle = build_s09_mes_strategy_input_next_evidence_authorization_packet_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_NEXT_EVIDENCE_AUTHORIZATION_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_NEXT_EVIDENCE_AUTHORIZATION_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_NEXT_EVIDENCE_AUTHORIZATION_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_STRATEGY_INPUT_NEXT_EVIDENCE_AUTHORIZATION_PACKET_NOT_AUTHORIZATION_NOT_DATA_NOT_BACKTEST",
            packet,
        )
        self.assertIn("remaining_evidence_count: 10", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("2019-05-05 through 2020-04-05", packet)
        self.assertIn("SOURCE_NATIVE_FUTURES", packet)
        self.assertIn("APPENDIX_C_174_006", packet)
        for evidence_name in (
            "official_lifecycle_evidence",
            "roll_trading_day_semantics",
            "annual_risk_runtime_values",
            "daily_price_risk_values",
            "historical_mes_cost_values",
            "risk_adjusted_cost_values",
            "speed_eligibility_values",
            "eligible_speed_set",
            "table36_fdm_row",
            "hash_bound_provenance",
        ):
            self.assertIn(evidence_name, packet)
        self.assertIn("requires separate explicit operator authorization", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no market-row parsing", packet)
        self.assertIn("no forecast computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Forward", packet)
        self.assertIn("no Git staging", packet)
        self.assertIn("build_s09_mes_strategy_input_next_evidence_authorization_packet_bundle", audit)
        self.assertIn("hash manifest covers packet and audit only", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)

    def test_s09_mes_strategy_input_evidence_family_authorization_preflight_scopes_one_family_only(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceFamilyAuthorizationConfig,
            run_s09_mes_strategy_input_evidence_family_authorization_preflight,
        )

        base = S09MESStrategyInputEvidenceFamilyAuthorizationConfig(
            execution_authorized=True,
            selected_evidence_name="official_lifecycle_evidence",
            evidence_completion_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
            remaining_evidence_count=10,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            risk_runtime_computation_authorized=False,
            cost_computation_authorized=False,
            speed_eligibility_computation_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )

        result = run_s09_mes_strategy_input_evidence_family_authorization_preflight(base)

        self.assertEqual(result["status"], "AUTHORIZED_EVIDENCE_FAMILY_PREFLIGHT_ONLY_NOT_EXECUTED")
        self.assertEqual(result["selected_evidence_name"], "official_lifecycle_evidence")
        self.assertEqual(result["remaining_evidence_count"], "10")
        self.assertEqual(result["lane_class"], "SOURCE_NATIVE_FUTURES")
        self.assertEqual(result["root"], "MES")
        self.assertEqual(result["row_id"], "APPENDIX_C_174_006")
        self.assertEqual(result["machinery_development_slice"], "2019-05-05 through 2020-04-05")
        self.assertEqual(result["databento_api_access"], "NO")
        self.assertEqual(result["market_row_parsing"], "NO")
        self.assertEqual(result["risk_runtime_computation"], "NO")
        self.assertEqual(result["cost_computation"], "NO")
        self.assertEqual(result["speed_eligibility_computation"], "NO")
        self.assertEqual(result["forecast_computation"], "NO")
        self.assertEqual(result["diagnostics_run"], "NO")
        self.assertEqual(result["backtests_run"], "NO")
        self.assertEqual(result["test_validation_lockbox_forward_access"], "NO")
        self.assertIn("Official per-contract lifecycle evidence", result["blocking_reason"])
        self.assertIn("Lock per-contract lifecycle evidence", result["next_action"])

        hostile_configs = (
            replace(base, execution_authorized=False),
            replace(base, selected_evidence_name="all_evidence"),
            replace(base, evidence_completion_status="LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION"),
            replace(base, remaining_evidence_count=0),
            replace(base, remaining_evidence_count=True),
            replace(base, lane_class="CFD_ADAPTER"),
            replace(base, root="ES"),
            replace(base, row_id="APPENDIX_C_174_002"),
            replace(base, machinery_development_slice="2022-01-03 through 2023-12-29"),
            replace(base, runtime_input_lock_scope="full two year dev window"),
            replace(base, design_ordering="newest data first"),
            replace(base, databento_api_access_authorized=True),
            replace(base, market_row_parsing_authorized=True),
            replace(base, risk_runtime_computation_authorized=True),
            replace(base, cost_computation_authorized=True),
            replace(base, speed_eligibility_computation_authorized=True),
            replace(base, forecast_computation_authorized=True),
            replace(base, diagnostics_authorized=True),
            replace(base, backtest_authorized=True),
            replace(base, test_validation_lockbox_forward_authorized=True),
        )
        for config in hostile_configs:
            with self.subTest(config=config):
                with self.assertRaises(CarverBlocked):
                    run_s09_mes_strategy_input_evidence_family_authorization_preflight(config)

    def test_s09_mes_strategy_input_official_lifecycle_authorization_ready_packet_scopes_one_family(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceFamilyAuthorizationConfig,
            build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle,
        )

        config = S09MESStrategyInputEvidenceFamilyAuthorizationConfig(
            execution_authorized=True,
            selected_evidence_name="official_lifecycle_evidence",
            evidence_completion_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
            remaining_evidence_count=10,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            risk_runtime_computation_authorized=False,
            cost_computation_authorized=False,
            speed_eligibility_computation_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )

        bundle = build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle(config)

        expected_paths = (
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_OFFICIAL_LIFECYCLE_EVIDENCE_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_OFFICIAL_LIFECYCLE_EVIDENCE_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_OFFICIAL_LIFECYCLE_EVIDENCE_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_STRATEGY_INPUT_OFFICIAL_LIFECYCLE_EVIDENCE_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION",
            packet,
        )
        self.assertIn("selected_evidence_name: official_lifecycle_evidence", packet)
        self.assertIn("Official per-contract lifecycle evidence is not locked for the machinery slice.", packet)
        self.assertIn("Lock per-contract lifecycle evidence from explicitly authorized source-native sources.", packet)
        self.assertIn("remaining_evidence_count: 10", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("2019-05-05 through 2020-04-05", packet)
        self.assertIn("SOURCE_NATIVE_FUTURES", packet)
        self.assertIn("APPENDIX_C_174_006", packet)
        self.assertIn("operator authorization wording", packet)
        self.assertIn("official_lifecycle_evidence", packet)
        self.assertNotIn("roll_trading_day_semantics", packet)
        self.assertNotIn("annual_risk_runtime_values", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no market-row parsing", packet)
        self.assertIn("no risk runtime computation", packet)
        self.assertIn("no cost computation", packet)
        self.assertIn("no speed eligibility computation", packet)
        self.assertIn("no forecast computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Forward", packet)
        self.assertIn("no Git staging", packet)
        self.assertIn("build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle", audit)
        self.assertIn("hash manifest covers selected packet and audit only", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)

    def test_s09_mes_strategy_input_roll_semantics_authorization_ready_packet_uses_post_lifecycle_state(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceFamilyAuthorizationConfig,
            build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle,
            run_s09_mes_strategy_input_evidence_family_authorization_preflight,
        )

        config = S09MESStrategyInputEvidenceFamilyAuthorizationConfig(
            execution_authorized=True,
            selected_evidence_name="roll_trading_day_semantics",
            evidence_completion_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
            remaining_evidence_count=9,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            risk_runtime_computation_authorized=False,
            cost_computation_authorized=False,
            speed_eligibility_computation_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )

        preflight = run_s09_mes_strategy_input_evidence_family_authorization_preflight(config)
        self.assertEqual(preflight["selected_evidence_name"], "roll_trading_day_semantics")
        self.assertEqual(preflight["remaining_evidence_count"], "9")
        self.assertIn("Roll trading-day semantics", preflight["blocking_reason"])
        self.assertIn("Lock provider dates to completed trading dates", preflight["next_action"])

        bundle = build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle(config)

        expected_paths = (
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_ROLL_TRADING_DAY_SEMANTICS_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_ROLL_TRADING_DAY_SEMANTICS_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_ROLL_TRADING_DAY_SEMANTICS_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_STRATEGY_INPUT_ROLL_TRADING_DAY_SEMANTICS_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION",
            packet,
        )
        self.assertIn("selected_evidence_name: roll_trading_day_semantics", packet)
        self.assertIn("remaining_evidence_count: 9", packet)
        self.assertIn("Roll trading-day semantics are not locked to completed bars.", packet)
        self.assertIn("Lock provider dates to completed trading dates before strategy computation.", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no market-row parsing", packet)
        self.assertIn("no forecast computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Forward", packet)
        self.assertIn("build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

        with self.assertRaises(CarverBlocked):
            run_s09_mes_strategy_input_evidence_family_authorization_preflight(
                replace(config, selected_evidence_name="official_lifecycle_evidence")
            )

    def test_s09_mes_strategy_input_annual_risk_authorization_ready_packet_uses_post_roll_state(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceFamilyAuthorizationConfig,
            build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle,
            run_s09_mes_strategy_input_evidence_family_authorization_preflight,
        )

        config = S09MESStrategyInputEvidenceFamilyAuthorizationConfig(
            execution_authorized=True,
            selected_evidence_name="annual_risk_runtime_values",
            evidence_completion_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
            remaining_evidence_count=8,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            risk_runtime_computation_authorized=False,
            cost_computation_authorized=False,
            speed_eligibility_computation_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )

        preflight = run_s09_mes_strategy_input_evidence_family_authorization_preflight(config)
        self.assertEqual(preflight["selected_evidence_name"], "annual_risk_runtime_values")
        self.assertEqual(preflight["remaining_evidence_count"], "8")
        self.assertIn("Annual-risk runtime values", preflight["blocking_reason"])
        self.assertIn("Compute only from hash-bound authorized source-native machinery-slice inputs", preflight["next_action"])

        bundle = build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle(config)

        expected_paths = (
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_ANNUAL_RISK_RUNTIME_VALUES_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_ANNUAL_RISK_RUNTIME_VALUES_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_ANNUAL_RISK_RUNTIME_VALUES_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_STRATEGY_INPUT_ANNUAL_RISK_RUNTIME_VALUES_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION",
            packet,
        )
        self.assertIn("selected_evidence_name: annual_risk_runtime_values", packet)
        self.assertIn("remaining_evidence_count: 8", packet)
        self.assertIn("Annual-risk runtime values are not locked from authorized source-native inputs.", packet)
        self.assertIn("Compute only from hash-bound authorized source-native machinery-slice inputs.", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no market-row parsing", packet)
        self.assertIn("no forecast computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Forward", packet)
        self.assertIn("build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

        for locked_name in ("official_lifecycle_evidence", "roll_trading_day_semantics"):
            with self.subTest(locked_name=locked_name):
                with self.assertRaises(CarverBlocked):
                    run_s09_mes_strategy_input_evidence_family_authorization_preflight(
                        replace(config, selected_evidence_name=locked_name)
                    )

    def test_s09_mes_strategy_input_daily_price_risk_authorization_ready_packet_uses_post_annual_risk_state(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceFamilyAuthorizationConfig,
            build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle,
            run_s09_mes_strategy_input_evidence_family_authorization_preflight,
        )

        config = S09MESStrategyInputEvidenceFamilyAuthorizationConfig(
            execution_authorized=True,
            selected_evidence_name="daily_price_risk_values",
            evidence_completion_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
            remaining_evidence_count=7,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            risk_runtime_computation_authorized=False,
            cost_computation_authorized=False,
            speed_eligibility_computation_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )

        preflight = run_s09_mes_strategy_input_evidence_family_authorization_preflight(config)
        self.assertEqual(preflight["selected_evidence_name"], "daily_price_risk_values")
        self.assertEqual(preflight["remaining_evidence_count"], "7")
        self.assertIn("Daily price-risk values", preflight["blocking_reason"])
        self.assertIn("Compute from locked current price and locked annual percentage risk only", preflight["next_action"])

        bundle = build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle(config)
        expected_paths = (
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_DAILY_PRICE_RISK_VALUES_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_DAILY_PRICE_RISK_VALUES_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_DAILY_PRICE_RISK_VALUES_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn("selected_evidence_name: daily_price_risk_values", packet)
        self.assertIn("remaining_evidence_count: 7", packet)
        self.assertIn("Daily price-risk values are blocked until annual-risk runtime is locked.", packet)
        self.assertIn("Compute from locked current price and locked annual percentage risk only.", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no market-row parsing", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

        for locked_name in ("official_lifecycle_evidence", "roll_trading_day_semantics", "annual_risk_runtime_values"):
            with self.subTest(locked_name=locked_name):
                with self.assertRaises(CarverBlocked):
                    run_s09_mes_strategy_input_evidence_family_authorization_preflight(
                        replace(config, selected_evidence_name=locked_name)
                    )

    def test_s09_mes_strategy_input_historical_cost_authorization_ready_packet_uses_post_daily_price_state(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceFamilyAuthorizationConfig,
            build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle,
            run_s09_mes_strategy_input_evidence_family_authorization_preflight,
        )

        config = S09MESStrategyInputEvidenceFamilyAuthorizationConfig(
            execution_authorized=True,
            selected_evidence_name="historical_mes_cost_values",
            evidence_completion_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY",
            remaining_evidence_count=6,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            risk_runtime_computation_authorized=False,
            cost_computation_authorized=False,
            speed_eligibility_computation_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )

        preflight = run_s09_mes_strategy_input_evidence_family_authorization_preflight(config)
        self.assertEqual(preflight["selected_evidence_name"], "historical_mes_cost_values")
        self.assertEqual(preflight["remaining_evidence_count"], "6")
        self.assertIn("Historical MES cost components", preflight["blocking_reason"])
        self.assertIn("Lock exchange, clearing/regulatory, broker, and spread/slippage cost evidence", preflight["next_action"])

        bundle = build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle(config)
        expected_paths = (
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_HISTORICAL_MES_COST_VALUES_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_HISTORICAL_MES_COST_VALUES_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_STRATEGY_INPUT_HISTORICAL_MES_COST_VALUES_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn("selected_evidence_name: historical_mes_cost_values", packet)
        self.assertIn("remaining_evidence_count: 6", packet)
        self.assertIn("Historical MES cost components are not locked from source-native evidence.", packet)
        self.assertIn("Lock exchange, clearing/regulatory, broker, and spread/slippage cost evidence.", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no market-row parsing", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("build_s09_mes_strategy_input_selected_evidence_authorization_packet_bundle", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

        for locked_name in (
            "official_lifecycle_evidence",
            "roll_trading_day_semantics",
            "annual_risk_runtime_values",
            "daily_price_risk_values",
        ):
            with self.subTest(locked_name=locked_name):
                with self.assertRaises(CarverBlocked):
                    run_s09_mes_strategy_input_evidence_family_authorization_preflight(
                        replace(config, selected_evidence_name=locked_name)
                    )

    def test_s09_mes_historical_cost_source_acquisition_extraction_authorization_packet_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_bundle,
        )

        bundle = build_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_SOURCE_ACQUISITION_EXTRACTION_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION",
            packet,
        )
        self.assertIn("next_gate: source-native historical MES cost source acquisition/extraction", packet)
        self.assertIn("selected_evidence_name: historical_mes_cost_values", packet)
        self.assertIn("remaining_evidence_count: 6", packet)
        self.assertIn("current_historical_cost_status: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED", packet)
        self.assertIn("exchange_fee", packet)
        self.assertIn("clearing_regulatory_fee", packet)
        self.assertIn("broker_commission", packet)
        self.assertIn("spread_slippage", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no provider login", packet)
        self.assertIn("no web access", packet)
        self.assertIn("no source extraction", packet)
        self.assertIn("no market-row parsing", packet)
        self.assertIn("no cost computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Git staging", packet)
        self.assertIn("build_s09_mes_historical_mes_cost_source_acquisition_extraction_authorization_packet_bundle", audit)
        self.assertIn("must be reviewed by a spawned hostile-audit subagent", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)
        self.assertNotIn("risk_adjusted_cost_values,LOCKED", combined)
        self.assertNotIn("speed_eligibility_values,LOCKED", combined)

    def test_s09_mes_historical_cost_blocker_decision_packet_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_bundle,
        )

        bundle = build_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_BLOCKER_DECISION_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION",
            packet,
        )
        self.assertIn("next_gate: historical MES cost blocker decision", packet)
        self.assertIn("remaining_evidence_count: 6", packet)
        self.assertIn("official_cme_2019_fee_schedule_archive_permitted_route", packet)
        self.assertIn("broker_commission_source_or_policy", packet)
        self.assertIn("spread_slippage_source_or_policy", packet)
        self.assertIn("No default choice is selected by this packet.", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no provider login", packet)
        self.assertIn("no web access", packet)
        self.assertIn("no source extraction", packet)
        self.assertIn("no cost computation", packet)
        self.assertIn("no risk-adjusted cost computation", packet)
        self.assertIn("no speed eligibility computation", packet)
        self.assertIn("no forecast computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Git staging", packet)
        self.assertIn("build_s09_mes_historical_mes_cost_blocker_decision_authorization_packet_bundle", audit)
        self.assertIn("must be reviewed by a spawned hostile-audit subagent", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)
        self.assertNotIn("LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE", combined)

    def test_s09_mes_historical_cost_remaining_blockers_after_exchange_and_nfa_packet_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_bundle,
        )

        bundle = build_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_EXCHANGE_AND_NFA_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION",
            packet,
        )
        self.assertIn("next_gate: historical MES cost remaining blocker decision after exchange and NFA extraction", packet)
        self.assertIn("exchange_fee_value: PARTIAL_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK", packet)
        self.assertIn("clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK", packet)
        self.assertIn("historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED", packet)
        self.assertIn("remaining_evidence_count: 6", packet)
        self.assertIn("broker_commission_source_or_policy", packet)
        self.assertIn("spread_slippage_source_or_policy", packet)
        self.assertIn("official_cme_2020_fee_schedule_coverage_permitted_route", packet)
        self.assertIn("No default choice is selected by this packet.", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no provider login", packet)
        self.assertIn("no web access", packet)
        self.assertIn("no source extraction", packet)
        self.assertIn("no cost computation", packet)
        self.assertIn("no risk-adjusted cost computation", packet)
        self.assertIn("no speed eligibility computation", packet)
        self.assertIn("no forecast computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Git staging", packet)
        self.assertIn(
            "build_s09_mes_historical_mes_cost_remaining_blockers_after_exchange_and_nfa_packet_bundle",
            audit,
        )
        self.assertIn("must be reviewed by a spawned hostile-audit subagent", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)
        self.assertNotIn("LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE", combined)

    def test_s09_mes_historical_cost_remaining_blockers_after_etf_packet_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_bundle,
        )

        bundle = build_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_AUTHORIZATION_READY_PACKET_2026-06-03.md",
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_AUTHORIZATION_READY_PACKET_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_AUTHORIZATION_READY_PACKET_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_HISTORICAL_MES_COST_REMAINING_BLOCKERS_AFTER_ETF_AUTHORIZATION_READY_NOT_AUTHORIZATION_NOT_EXECUTION",
            packet,
        )
        self.assertIn("next_gate: historical MES cost remaining blocker decision after ETF selected broker fee extraction", packet)
        self.assertIn(
            "exchange_fee_value: SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_FULL_MACHINERY_SLICE_NOT_FULL_COST_LOCK",
            packet,
        )
        self.assertIn("clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK", packet)
        self.assertIn("broker_commission_value: PARTIAL_SELECTED_BROKER_VENUE_CURRENT_MICRO_COMMISSION_SOURCE_EXTRACTED_NOT_FULL_COST_LOCK", packet)
        self.assertIn("Elite Trader Funding current micro fee source: 0.62 USD per side", packet)
        self.assertIn("broker_current_fee_static_historical_policy", packet)
        self.assertIn("spread_slippage_source_or_policy", packet)
        self.assertIn("official_cme_2020_fee_schedule_coverage: PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED", packet)
        self.assertNotIn("official_cme_2020_fee_schedule_coverage_permitted_route", packet)
        self.assertIn("historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED", packet)
        self.assertIn("remaining_evidence_count: 6", packet)
        self.assertIn("No default choice is selected by this packet.", packet)
        self.assertIn("This packet is not authorization.", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no provider login", packet)
        self.assertIn("no web access", packet)
        self.assertIn("no source extraction", packet)
        self.assertIn("no cost computation", packet)
        self.assertIn("no risk-adjusted cost computation", packet)
        self.assertIn("no speed eligibility computation", packet)
        self.assertIn("no forecast computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Git staging", packet)
        self.assertIn(
            "build_s09_mes_historical_mes_cost_remaining_blockers_after_etf_packet_bundle",
            audit,
        )
        self.assertIn("must be reviewed by a spawned hostile-audit subagent", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)
        self.assertNotIn("LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE", combined)

    def test_s09_mes_etf_static_broker_fee_policy_is_locked_without_full_cost_readiness(self) -> None:
        policy_path = Path(
            "docs/process/"
            "CARVER_S09_MES_ETF_STATIC_BROKER_COMMISSION_POLICY_LOCK_RESULT_2026-06-03.md"
        )
        self.assertTrue(policy_path.exists(), f"Missing policy artifact: {policy_path}")
        policy = policy_path.read_text(encoding="utf-8")
        source_extract = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "cost_source_extracts/elite_trader_funding_selected_broker_fee_extract.md"
        ).read_text(encoding="utf-8")
        cost_source_status = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_status.csv"
        ).read_text(encoding="utf-8")
        active_cost_ledger = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv"
        ).read_text(encoding="utf-8")

        self.assertIn("LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION", policy)
        self.assertIn(
            "operator_policy_authorization: apply current Elite Trader Funding micro fee as static selected-venue broker commission",
            policy,
        )
        self.assertIn(
            "broker_commission_value: LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION_0_62_PER_SIDE",
            policy,
        )
        self.assertIn("amount_currency: 0.62", policy)
        self.assertIn("charge_timing: PER_SIDE", policy)
        self.assertIn("correction_policy: any replacement after result exposure invalidates affected scored/run evidence", policy)
        self.assertIn("spread_slippage_policy: AUTHORIZED_TBBO_BOUNDED_RAW_ACQUISITION_COMPLETED_NO_SPREAD_LOCK", policy)
        self.assertIn("historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED", policy)
        self.assertIn("No active cost ledger rows were written.", policy)
        self.assertIn("no backtests", policy)
        self.assertIn("no TEST", policy)
        self.assertIn("no VALIDATION", policy)
        self.assertIn("no Lockbox", policy)

        self.assertIn("STATIC_SELECTED_BROKER_POLICY_LOCKED_FOR_HISTORICAL_SIMULATION_USE", source_extract)
        self.assertIn(
            "broker_commission_value: LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION_0_62_PER_SIDE",
            source_extract,
        )
        self.assertIn("historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED", source_extract)
        self.assertIn(
            "broker_commission_value,LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION_0_62_PER_SIDE",
            cost_source_status,
        )
        self.assertIn(
            "historical_mes_cost_values,LOCKED_S09_MES_HISTORICAL_COST_VALUES_NOT_RISK_ADJUSTED_COST",
            cost_source_status,
        )
        self.assertIn(
            "broker_commission,0.62,USD,PER_SIDE,2019-05-05,2020-04-05,"
            "LOCKED_ETF_STATIC_SELECTED_BROKER_COMMISSION_POLICY",
            active_cost_ledger,
        )
        self.assertIn("LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE", active_cost_ledger)

    def test_s09_mes_spread_slippage_source_or_policy_gate_result_fails_closed_without_selected_policy(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_spread_slippage_source_or_policy_gate_result_bundle,
        )

        bundle = build_s09_mes_spread_slippage_source_or_policy_gate_result_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_RESULT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        packet = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = packet + audit + hashes

        self.assertIn("AUTHORIZED_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_GATE_OPENED_FAIL_CLOSED_NO_SOURCE_OR_POLICY_SELECTED", packet)
        self.assertIn("operator_authorization: spread_slippage_source_or_policy gate", packet)
        self.assertIn("selected_evidence_name: historical_mes_cost_values", packet)
        self.assertIn("spread_slippage_policy: FAIL_CLOSED_S09_MES_SPREAD_SLIPPAGE_POLICY_NOT_LOCKED", packet)
        self.assertIn("spread_slippage_source_or_policy: no source-native spread/slippage source or explicit numeric conservative policy was selected by this authorization alone", packet)
        self.assertIn("historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED", packet)
        self.assertIn("broker_current_fee_static_historical_policy", packet)
        self.assertIn("spread_slippage_source_or_policy", packet)
        self.assertIn("no Databento API access", packet)
        self.assertIn("no provider login", packet)
        self.assertIn("no web access", packet)
        self.assertIn("no source extraction", packet)
        self.assertIn("no market-row parsing", packet)
        self.assertIn("no cost ledger rows", packet)
        self.assertIn("no cost computation", packet)
        self.assertIn("no risk-adjusted cost computation", packet)
        self.assertIn("no speed eligibility computation", packet)
        self.assertIn("no forecast computation", packet)
        self.assertIn("no diagnostics", packet)
        self.assertIn("no backtests", packet)
        self.assertIn("no TEST", packet)
        self.assertIn("no VALIDATION", packet)
        self.assertIn("no Lockbox", packet)
        self.assertIn("no Git staging", packet)
        self.assertIn("build_s09_mes_spread_slippage_source_or_policy_gate_result_bundle", audit)
        self.assertIn("must be reviewed by a spawned hostile-audit subagent", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)
        self.assertNotIn("LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE", combined)

    def test_s09_mes_spread_slippage_bid_ask_metadata_preflight_is_bounded(self) -> None:
        from tools.databento.carver_s09_mes_spread_slippage_bid_ask_metadata_preflight import (  # noqa: PLC0415
            RAW_SYMBOLS,
            S09MESSpreadSlippageBidAskMetadataPreflightConfig,
            build_request_manifest_payload,
            run_preflight_guard,
        )

        config = S09MESSpreadSlippageBidAskMetadataPreflightConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
            metadata_only=True,
            raw_quote_download=False,
            schemas=("mbp-1", "tbbo"),
        )

        result = run_preflight_guard(config)
        manifest = build_request_manifest_payload(config)

        self.assertEqual(result["status"], "AUTHORIZED_METADATA_PREFLIGHT_ONLY_READY")
        self.assertEqual(manifest["dataset"], "GLBX.MDP3")
        self.assertEqual(manifest["raw_symbols"], list(RAW_SYMBOLS))
        self.assertEqual(manifest["schemas"], ["mbp-1", "tbbo"])
        self.assertEqual(manifest["metadata_only"], "YES")
        self.assertEqual(manifest["raw_quote_download"], "NO")
        self.assertEqual(manifest["spread_slippage_policy_lock"], "NO")
        self.assertEqual(manifest["cost_ledger_rows"], "NO")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(manifest["test_validation_lockbox_forward_access"], "NO")

        hostile_configs = (
            replace(config, execution_authorized=False),
            replace(config, lane_class="CFD_ADAPTER"),
            replace(config, root="ES"),
            replace(config, row_id="APPENDIX_C_174_007"),
            replace(config, window_start="2020-04-06"),
            replace(config, window_end="2022-02-08"),
            replace(config, metadata_only=False),
            replace(config, raw_quote_download=True),
            replace(config, schemas=("trades",)),
            replace(config, schemas=("mbp-1", "ohlcv-1d")),
        )
        for hostile in hostile_configs:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    run_preflight_guard(hostile)

    def test_s09_mes_spread_slippage_tbbo_bounded_acquisition_guard_is_strict(self) -> None:
        from tools.databento.carver_s09_mes_spread_slippage_tbbo_bounded_acquisition import (  # noqa: PLC0415
            RAW_SYMBOLS,
            S09MESSpreadSlippageTBBBOBoundedAcquisitionConfig,
            build_request_manifest_payload,
            run_acquisition_guard,
        )

        config = S09MESSpreadSlippageTBBBOBoundedAcquisitionConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
            schema="tbbo",
            raw_quote_download=True,
            spread_slippage_policy_lock=False,
            cost_ledger_rows=False,
        )

        result = run_acquisition_guard(config)
        manifest = build_request_manifest_payload(config)

        self.assertEqual(result["status"], "AUTHORIZED_TBBO_BOUNDED_RAW_ACQUISITION_READY")
        self.assertEqual(manifest["dataset"], "GLBX.MDP3")
        self.assertEqual(manifest["schema"], "tbbo")
        self.assertEqual(manifest["raw_symbols"], list(RAW_SYMBOLS))
        self.assertEqual(manifest["raw_quote_download"], "YES_TBBO_ONLY")
        self.assertEqual(manifest["mbp_1_download"], "NO")
        self.assertEqual(manifest["spread_slippage_policy_lock"], "NO")
        self.assertEqual(manifest["cost_ledger_rows"], "NO")
        self.assertEqual(manifest["cost_computation"], "NO")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(manifest["test_validation_lockbox_forward_access"], "NO")

        hostile_configs = (
            replace(config, execution_authorized=False),
            replace(config, lane_class="CFD_ADAPTER"),
            replace(config, root="ES"),
            replace(config, row_id="APPENDIX_C_174_007"),
            replace(config, window_start="2020-04-06"),
            replace(config, window_end="2022-02-08"),
            replace(config, schema="mbp-1"),
            replace(config, schema="trades"),
            replace(config, raw_quote_download=False),
            replace(config, spread_slippage_policy_lock=True),
            replace(config, cost_ledger_rows=True),
        )
        for hostile in hostile_configs:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    run_acquisition_guard(hostile)

    def test_s09_mes_spread_slippage_tbbo_source_native_extraction_locks_cost_without_backtest(self) -> None:
        from tools.databento.carver_s09_mes_spread_slippage_tbbo_source_native_extraction import (  # noqa: PLC0415
            S09MESSpreadSlippageTBBOSourceNativeExtractionConfig,
            build_request_manifest_payload,
            lock_spread_slippage_from_summary,
            run_extraction_guard,
        )

        config = S09MESSpreadSlippageTBBOSourceNativeExtractionConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
            schema="tbbo",
            acquired_raw_tbbo_only=True,
            degraded_day_policy="EXCLUDE_DEGRADED_PROVIDER_DAYS_FROM_ESTIMATOR_PRESERVE_IN_QUARANTINE",
            spread_slippage_policy_lock=True,
            historical_cost_ledger_rows=True,
            risk_adjusted_cost_computation=False,
            forecast_computation=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
            git_operations_authorized=False,
        )

        result = run_extraction_guard(config)
        manifest = build_request_manifest_payload(config)
        lock = lock_spread_slippage_from_summary(
            median_spread_points=0.25,
            valid_quote_rows_used=30_519_879,
            degraded_quote_rows_excluded=936_077,
            crossed_or_empty_rows_rejected=619,
        )

        self.assertEqual(result["status"], "AUTHORIZED_TBBO_SOURCE_NATIVE_SPREAD_SLIPPAGE_EXTRACTION_READY")
        self.assertEqual(manifest["schema"], "tbbo")
        self.assertEqual(manifest["acquired_raw_tbbo_only"], "YES")
        self.assertEqual(
            manifest["degraded_day_policy"],
            "EXCLUDE_DEGRADED_PROVIDER_DAYS_FROM_ESTIMATOR_PRESERVE_IN_QUARANTINE",
        )
        self.assertEqual(manifest["spread_slippage_policy_lock"], "YES_SOURCE_NATIVE_TBBO_ONLY")
        self.assertEqual(manifest["historical_cost_ledger_rows"], "YES_COMPLETE_COST_COMPONENTS_ONLY")
        self.assertEqual(manifest["risk_adjusted_cost_computation"], "NO")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(manifest["test_validation_lockbox_forward_access"], "NO")

        self.assertEqual(lock["status"], "LOCKED_SOURCE_NATIVE_TBBO_MEDIAN_SPREAD_SLIPPAGE_VALUE")
        self.assertEqual(lock["median_spread_points"], "0.25")
        self.assertEqual(lock["locked_spread_slippage_round_turn_usd"], "1.25")
        self.assertEqual(lock["charge_timing"], "ROUND_TURN")
        self.assertEqual(lock["valid_quote_rows_used"], "30519879")
        self.assertEqual(lock["degraded_quote_rows_excluded"], "936077")

        policy_path = Path(
            "docs/process/"
            "CARVER_S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_AND_DEGRADED_DAY_POLICY_LOCK_RESULT_2026-06-03.md"
        )
        self.assertTrue(policy_path.exists(), f"Missing spread/slippage extraction artifact: {policy_path}")
        policy = policy_path.read_text(encoding="utf-8")
        cost_ledger = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv"
        ).read_text(encoding="utf-8")
        cost_status = json.loads(
            Path(
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
                "cost/20260603_S09_MES_HISTORICAL_COST_VALUE_status.json"
            ).read_text(encoding="utf-8")
        )
        cost_source_status = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_status.csv"
        ).read_text(encoding="utf-8")

        self.assertIn("LOCKED_SOURCE_NATIVE_TBBO_MEDIAN_SPREAD_SLIPPAGE_VALUE", policy)
        self.assertIn("median_spread_points: 0.25", policy)
        self.assertIn("locked_spread_slippage_round_turn_usd: 1.25", policy)
        self.assertIn("degraded_day_policy: EXCLUDE_DEGRADED_PROVIDER_DAYS_FROM_ESTIMATOR_PRESERVE_IN_QUARANTINE", policy)
        self.assertIn("no risk-adjusted cost computation", policy)
        self.assertIn("no backtests", policy)
        self.assertIn("no TEST", policy)
        self.assertIn("no VALIDATION", policy)
        self.assertIn("no Lockbox", policy)

        self.assertIn("2020-03-02,exchange_fee,0.2,USD,PER_SIDE,2019-05-05,2020-04-05", cost_ledger)
        self.assertIn("2020-03-02,clearing_regulatory_fee,0.02,USD,PER_SIDE,2019-05-05,2020-04-05", cost_ledger)
        self.assertIn("2020-03-02,broker_commission,0.62,USD,PER_SIDE,2019-05-05,2020-04-05", cost_ledger)
        self.assertIn("2020-03-02,spread_slippage,1.25,USD,ROUND_TURN,2019-05-05,2020-04-05", cost_ledger)
        self.assertEqual(cost_status["status"], "LOCKED_S09_MES_HISTORICAL_COST_VALUES_NOT_RISK_ADJUSTED_COST")
        self.assertEqual(cost_status["locked_historical_cost_rows"], 4)
        self.assertEqual(cost_status["missing_cost_components"], [])
        self.assertEqual(cost_status["total_round_turn_cost_per_trade_currency"], 2.93)
        self.assertEqual(cost_status["risk_adjusted_cost_computation"], "NO")
        self.assertEqual(cost_status["backtests_run"], "NO")
        self.assertIn(
            "spread_slippage_policy,LOCKED_SOURCE_NATIVE_TBBO_MEDIAN_SPREAD_SLIPPAGE_VALUE",
            cost_source_status,
        )
        self.assertIn(
            "historical_mes_cost_values,LOCKED_S09_MES_HISTORICAL_COST_VALUES_NOT_RISK_ADJUSTED_COST",
            cost_source_status,
        )
        self.assertNotIn("READY_FOR_BACKTEST", policy + cost_ledger + cost_source_status)
        self.assertNotIn("READY_FOR_LOCKBOX", policy + cost_ledger + cost_source_status)

        hostile_configs = (
            replace(config, execution_authorized=False),
            replace(config, lane_class="CFD_ADAPTER"),
            replace(config, root="ES"),
            replace(config, row_id="APPENDIX_C_174_007"),
            replace(config, window_start="2020-04-06"),
            replace(config, window_end="2022-02-08"),
            replace(config, schema="mbp-1"),
            replace(config, acquired_raw_tbbo_only=False),
            replace(config, degraded_day_policy="INCLUDE_DEGRADED_DAYS"),
            replace(config, spread_slippage_policy_lock=False),
            replace(config, historical_cost_ledger_rows=False),
            replace(config, risk_adjusted_cost_computation=True),
            replace(config, forecast_computation=True),
            replace(config, diagnostics_authorized=True),
            replace(config, backtest_authorized=True),
            replace(config, test_validation_lockbox_forward_authorized=True),
            replace(config, git_operations_authorized=True),
        )
        for hostile in hostile_configs:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    run_extraction_guard(hostile)

    def test_s09_mes_dual_cost_scenario_policy_locks_both_models_without_backtest(self) -> None:
        from tools.databento.carver_s09_mes_dual_cost_scenario_policy import (  # noqa: PLC0415
            S09MESDualCostScenarioPolicyConfig,
            build_cost_scenario_rows,
            build_request_manifest_payload,
            run_dual_cost_scenario_policy_guard,
        )

        config = S09MESDualCostScenarioPolicyConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
            dual_scenario_policy=True,
            conservative_pass_through_scenario=True,
            etf_all_in_sim_fee_scenario=True,
            risk_adjusted_cost_values_lock=False,
            speed_eligibility_computation=False,
            forecast_computation=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
            git_operations_authorized=False,
        )

        result = run_dual_cost_scenario_policy_guard(config)
        manifest = build_request_manifest_payload(config)
        rows = build_cost_scenario_rows(
            daily_price_risk_currency=57.18365213859373,
            current_price=3072.5,
        )

        self.assertEqual(result["status"], "AUTHORIZED_DUAL_COST_SCENARIO_POLICY_READY")
        self.assertEqual(manifest["dual_scenario_policy"], "YES")
        self.assertEqual(manifest["risk_adjusted_cost_values_lock"], "NO")
        self.assertEqual(manifest["speed_eligibility_computation"], "NO")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(tuple(row["scenario_name"] for row in rows), (
            "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH",
            "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED",
        ))
        self.assertEqual(rows[0]["total_round_turn_cost_per_trade_currency"], "2.93")
        self.assertEqual(rows[0]["annualized_price_risk_currency"], "4574.6921710874985")
        self.assertEqual(rows[0]["cost_to_annualized_price_risk_pct"], "0.064048")
        self.assertEqual(rows[1]["total_round_turn_cost_per_trade_currency"], "2.49")
        self.assertEqual(rows[1]["annualized_price_risk_currency"], "4574.6921710874985")
        self.assertEqual(rows[1]["cost_to_annualized_price_risk_pct"], "0.054430")

        result_path = Path("docs/process/CARVER_S09_MES_DUAL_COST_SCENARIO_POLICY_LOCK_RESULT_2026-06-03.md")
        self.assertTrue(result_path.exists(), f"Missing dual-cost scenario result: {result_path}")
        result_text = result_path.read_text(encoding="utf-8")
        scenario_ledger = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "cost/20260603_S09_MES_COST_SCENARIO_POLICY_ledger.csv"
        ).read_text(encoding="utf-8")
        scenario_status = json.loads(
            Path(
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
                "cost/20260603_S09_MES_COST_SCENARIO_POLICY_status.json"
            ).read_text(encoding="utf-8")
        )

        self.assertIn("LOCKED_S09_MES_DUAL_COST_SCENARIO_POLICY_NOT_RISK_ADJUSTED_COST", result_text)
        self.assertIn("CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH,2.93,57.18365213859373,4574.6921710874985,0.000640,0.064048", scenario_ledger)
        self.assertIn("ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED,2.49,57.18365213859373,4574.6921710874985,0.000544,0.054430", scenario_ledger)
        self.assertEqual(scenario_status["status"], "LOCKED_S09_MES_DUAL_COST_SCENARIO_POLICY_NOT_RISK_ADJUSTED_COST")
        self.assertEqual(scenario_status["scenario_count"], 2)
        self.assertEqual(scenario_status["risk_adjusted_cost_values_lock"], "NO")
        self.assertEqual(scenario_status["backtests_run"], "NO")
        self.assertNotIn("READY_FOR_BACKTEST", result_text + scenario_ledger)
        self.assertNotIn("READY_FOR_LOCKBOX", result_text + scenario_ledger)

        hostile_configs = (
            replace(config, execution_authorized=False),
            replace(config, lane_class="CFD_ADAPTER"),
            replace(config, root="ES"),
            replace(config, row_id="APPENDIX_C_174_007"),
            replace(config, window_start="2020-04-06"),
            replace(config, dual_scenario_policy=False),
            replace(config, conservative_pass_through_scenario=False),
            replace(config, etf_all_in_sim_fee_scenario=False),
            replace(config, risk_adjusted_cost_values_lock=True),
            replace(config, speed_eligibility_computation=True),
            replace(config, forecast_computation=True),
            replace(config, diagnostics_authorized=True),
            replace(config, backtest_authorized=True),
            replace(config, test_validation_lockbox_forward_authorized=True),
            replace(config, git_operations_authorized=True),
        )
        for hostile in hostile_configs:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    run_dual_cost_scenario_policy_guard(hostile)

    def test_s09_mes_dual_risk_adjusted_cost_values_lock_both_models_without_speed_or_backtest(self) -> None:
        from tools.databento.carver_s09_mes_dual_cost_scenario_policy import (  # noqa: PLC0415
            build_cost_scenario_rows,
        )
        from tools.databento.carver_s09_mes_dual_risk_adjusted_cost_values import (  # noqa: PLC0415
            S09MESDualRiskAdjustedCostValuesConfig,
            build_dual_risk_adjusted_cost_rows,
            build_request_manifest_payload,
            run_dual_risk_adjusted_cost_values_guard,
        )

        config = S09MESDualRiskAdjustedCostValuesConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
            dual_cost_scenario_policy_status="LOCKED_S09_MES_DUAL_COST_SCENARIO_POLICY_NOT_RISK_ADJUSTED_COST",
            risk_adjusted_cost_values_lock=True,
            speed_eligibility_computation=False,
            forecast_computation=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
            git_operations_authorized=False,
        )
        policy_rows = build_cost_scenario_rows(
            daily_price_risk_currency=57.18365213859373,
            current_price=3072.5,
        )

        result = run_dual_risk_adjusted_cost_values_guard(config)
        manifest = build_request_manifest_payload(config)
        rows = build_dual_risk_adjusted_cost_rows(policy_rows=policy_rows)

        self.assertEqual(result["status"], "AUTHORIZED_DUAL_RISK_ADJUSTED_COST_VALUES_READY")
        self.assertEqual(manifest["risk_adjusted_cost_values_lock"], "YES_DUAL_SCENARIO")
        self.assertEqual(manifest["speed_eligibility_computation"], "NO")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(tuple(row["scenario_name"] for row in rows), (
            "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH",
            "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED",
        ))
        self.assertEqual(rows[0]["total_cost_per_trade_currency"], "2.93")
        self.assertEqual(rows[0]["daily_price_risk_currency"], "57.18365213859373")
        self.assertEqual(rows[0]["annualized_price_risk_currency"], "4574.6921710874985")
        self.assertEqual(rows[0]["risk_adjusted_cost_per_trade_sr"], "0.000640")
        self.assertEqual(rows[1]["total_cost_per_trade_currency"], "2.49")
        self.assertEqual(rows[1]["daily_price_risk_currency"], "57.18365213859373")
        self.assertEqual(rows[1]["annualized_price_risk_currency"], "4574.6921710874985")
        self.assertEqual(rows[1]["risk_adjusted_cost_per_trade_sr"], "0.000544")

        result_path = Path("docs/process/CARVER_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_LOCK_RESULT_2026-06-03.md")
        self.assertTrue(result_path.exists(), f"Missing dual risk-adjusted cost result: {result_path}")
        result_text = result_path.read_text(encoding="utf-8")
        risk_adjusted_ledger = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "cost/20260603_S09_MES_DUAL_RISK_ADJUSTED_COST_ledger.csv"
        ).read_text(encoding="utf-8")
        risk_adjusted_status = json.loads(
            Path(
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
                "cost/20260603_S09_MES_DUAL_RISK_ADJUSTED_COST_status.json"
            ).read_text(encoding="utf-8")
        )

        self.assertIn("LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_NOT_SPEED_NOT_BACKTEST", result_text)
        self.assertIn(
            "2020-03-02,CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH,2.93,57.18365213859373,4574.6921710874985,0.000640",
            risk_adjusted_ledger,
        )
        self.assertIn(
            "2020-03-02,ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED,2.49,57.18365213859373,4574.6921710874985,0.000544",
            risk_adjusted_ledger,
        )
        self.assertEqual(risk_adjusted_status["status"], "LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_NOT_SPEED_NOT_BACKTEST")
        self.assertEqual(risk_adjusted_status["scenario_count"], 2)
        self.assertEqual(risk_adjusted_status["risk_adjusted_cost_values_lock"], "YES_DUAL_SCENARIO")
        self.assertEqual(risk_adjusted_status["speed_eligibility_computation"], "NO")
        self.assertEqual(risk_adjusted_status["backtests_run"], "NO")
        self.assertNotIn("READY_FOR_BACKTEST", result_text + risk_adjusted_ledger)
        self.assertNotIn("READY_FOR_LOCKBOX", result_text + risk_adjusted_ledger)
        self.assertNotIn("CFD_ADAPTER", result_text + risk_adjusted_ledger)

        hostile_configs = (
            replace(config, execution_authorized=False),
            replace(config, lane_class="CFD_ADAPTER"),
            replace(config, root="ES"),
            replace(config, row_id="APPENDIX_C_174_007"),
            replace(config, window_start="2020-04-06"),
            replace(config, dual_cost_scenario_policy_status="UNLOCKED"),
            replace(config, risk_adjusted_cost_values_lock=False),
            replace(config, speed_eligibility_computation=True),
            replace(config, forecast_computation=True),
            replace(config, diagnostics_authorized=True),
            replace(config, backtest_authorized=True),
            replace(config, test_validation_lockbox_forward_authorized=True),
            replace(config, git_operations_authorized=True),
        )
        for hostile in hostile_configs:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    run_dual_risk_adjusted_cost_values_guard(hostile)

    def test_s09_mes_dual_speed_eligibility_values_lock_both_models_without_eligible_set_or_backtest(self) -> None:
        from tools.databento.carver_s09_mes_dual_risk_adjusted_cost_values import (  # noqa: PLC0415
            build_dual_risk_adjusted_cost_rows,
        )
        from tools.databento.carver_s09_mes_dual_speed_eligibility_values import (  # noqa: PLC0415
            S09MESDualSpeedEligibilityValuesConfig,
            build_dual_speed_eligibility_rows,
            build_request_manifest_payload,
            run_dual_speed_eligibility_values_guard,
        )

        config = S09MESDualSpeedEligibilityValuesConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
            dual_risk_adjusted_cost_status="LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_NOT_SPEED_NOT_BACKTEST",
            speed_eligibility_values_lock=True,
            eligible_speed_set_lock=False,
            table36_fdm_row_lock=False,
            forecast_computation=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
            git_operations_authorized=False,
        )
        risk_rows = build_dual_risk_adjusted_cost_rows(
            policy_rows=(
                {
                    "scenario_name": "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH",
                    "total_round_turn_cost_per_trade_currency": "2.93",
                    "daily_price_risk_currency": "57.18365213859373",
                    "status": "LOCKED_COST_SCENARIO_POLICY_VALUE_NOT_BACKTEST",
                },
                {
                    "scenario_name": "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED",
                    "total_round_turn_cost_per_trade_currency": "2.49",
                    "daily_price_risk_currency": "57.18365213859373",
                    "status": "LOCKED_COST_SCENARIO_POLICY_VALUE_NOT_BACKTEST",
                },
            )
        )

        result = run_dual_speed_eligibility_values_guard(config)
        manifest = build_request_manifest_payload(config)
        rows = build_dual_speed_eligibility_rows(risk_adjusted_rows=risk_rows)

        self.assertEqual(result["status"], "AUTHORIZED_DUAL_SPEED_ELIGIBILITY_VALUES_READY")
        self.assertEqual(manifest["speed_eligibility_values_lock"], "YES_DUAL_SCENARIO")
        self.assertEqual(manifest["eligible_speed_set_lock"], "NO")
        self.assertEqual(manifest["table36_fdm_row_lock"], "NO")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[0]["scenario_name"], "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH")
        self.assertEqual(rows[0]["span"], "2")
        self.assertEqual(rows[0]["annualized_cost_burden_sr"], "0.063040")
        self.assertEqual(rows[0]["threshold_sr"], "0.15")
        self.assertEqual(rows[0]["eligible"], "True")
        self.assertEqual(rows[5]["span"], "64")
        self.assertEqual(rows[5]["annualized_cost_burden_sr"], "0.003328")
        self.assertEqual(rows[5]["eligible"], "True")
        self.assertEqual(rows[6]["scenario_name"], "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED")
        self.assertEqual(rows[6]["span"], "2")
        self.assertEqual(rows[6]["annualized_cost_burden_sr"], "0.053584")
        self.assertEqual(rows[11]["span"], "64")
        self.assertEqual(rows[11]["annualized_cost_burden_sr"], "0.002829")
        self.assertEqual(rows[11]["eligible"], "True")
        self.assertEqual(sum(row["eligible"] == "True" for row in rows), 12)

        result_path = Path("docs/process/CARVER_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_LOCK_RESULT_2026-06-03.md")
        self.assertTrue(result_path.exists(), f"Missing dual speed eligibility result: {result_path}")
        result_text = result_path.read_text(encoding="utf-8")
        speed_ledger = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "speed/20260603_S09_MES_DUAL_SPEED_ELIGIBILITY_ledger.csv"
        ).read_text(encoding="utf-8")
        speed_status = json.loads(
            Path(
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
                "speed/20260603_S09_MES_DUAL_SPEED_ELIGIBILITY_status.json"
            ).read_text(encoding="utf-8")
        )

        self.assertIn("LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_ALL_SPEEDS_SURVIVE_NOT_ELIGIBLE_SET_NOT_BACKTEST", result_text)
        self.assertIn("CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH,2,98.5,0.000640,0.063040,0.15,True", speed_ledger)
        self.assertIn("ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED,64,5.2,0.000544,0.002829,0.15,True", speed_ledger)
        self.assertEqual(speed_status["status"], "LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_ALL_SPEEDS_SURVIVE_NOT_ELIGIBLE_SET_NOT_BACKTEST")
        self.assertEqual(speed_status["speed_eligibility_values_lock"], "YES_DUAL_SCENARIO")
        self.assertEqual(speed_status["eligible_speed_set_lock"], "NO")
        self.assertEqual(speed_status["table36_fdm_row_lock"], "NO")
        self.assertEqual(speed_status["scenario_count"], 2)
        self.assertEqual(speed_status["eligible_row_count"], 12)
        self.assertEqual(speed_status["backtests_run"], "NO")
        self.assertNotIn("READY_FOR_BACKTEST", result_text + speed_ledger)
        self.assertNotIn("READY_FOR_LOCKBOX", result_text + speed_ledger)
        self.assertNotIn("CFD_ADAPTER", result_text + speed_ledger)

        hostile_configs = (
            replace(config, execution_authorized=False),
            replace(config, lane_class="CFD_ADAPTER"),
            replace(config, root="ES"),
            replace(config, row_id="APPENDIX_C_174_007"),
            replace(config, window_start="2020-04-06"),
            replace(config, dual_risk_adjusted_cost_status="UNLOCKED"),
            replace(config, speed_eligibility_values_lock=False),
            replace(config, eligible_speed_set_lock=True),
            replace(config, table36_fdm_row_lock=True),
            replace(config, forecast_computation=True),
            replace(config, diagnostics_authorized=True),
            replace(config, backtest_authorized=True),
            replace(config, test_validation_lockbox_forward_authorized=True),
            replace(config, git_operations_authorized=True),
        )
        for hostile in hostile_configs:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    run_dual_speed_eligibility_values_guard(hostile)

    def test_s09_mes_eligible_speed_set_table36_fdm_lock_uses_corrected_dual_speed_values_only(self) -> None:
        from tools.databento.carver_s09_mes_dual_risk_adjusted_cost_values import (  # noqa: PLC0415
            build_dual_risk_adjusted_cost_rows,
        )
        from tools.databento.carver_s09_mes_dual_speed_eligibility_values import (  # noqa: PLC0415
            build_dual_speed_eligibility_rows,
        )
        from tools.databento.carver_s09_mes_eligible_speed_set_table36_fdm_lock import (  # noqa: PLC0415
            S09MESEligibleSpeedSetTable36FDMLockConfig,
            build_eligible_speed_set_table36_fdm_row,
            build_request_manifest_payload,
            run_eligible_speed_set_table36_fdm_lock_guard,
        )

        config = S09MESEligibleSpeedSetTable36FDMLockConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
            dual_speed_eligibility_status="LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_ALL_SPEEDS_SURVIVE_NOT_ELIGIBLE_SET_NOT_BACKTEST",
            eligible_speed_set_lock=True,
            table36_fdm_row_lock=True,
            hash_bound_provenance_lock=False,
            forecast_computation=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
            git_operations_authorized=False,
        )
        risk_rows = build_dual_risk_adjusted_cost_rows(
            policy_rows=(
                {
                    "scenario_name": "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH",
                    "total_round_turn_cost_per_trade_currency": "2.93",
                    "daily_price_risk_currency": "57.18365213859373",
                    "status": "LOCKED_COST_SCENARIO_POLICY_VALUE_NOT_BACKTEST",
                },
                {
                    "scenario_name": "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED",
                    "total_round_turn_cost_per_trade_currency": "2.49",
                    "daily_price_risk_currency": "57.18365213859373",
                    "status": "LOCKED_COST_SCENARIO_POLICY_VALUE_NOT_BACKTEST",
                },
            )
        )
        speed_rows = build_dual_speed_eligibility_rows(risk_adjusted_rows=risk_rows)

        result = run_eligible_speed_set_table36_fdm_lock_guard(config)
        manifest = build_request_manifest_payload(config)
        row = build_eligible_speed_set_table36_fdm_row(speed_rows=speed_rows)

        self.assertEqual(result["status"], "AUTHORIZED_ELIGIBLE_SPEED_SET_TABLE36_FDM_LOCK_READY")
        self.assertEqual(manifest["eligible_speed_set_lock"], "YES")
        self.assertEqual(manifest["table36_fdm_row_lock"], "YES")
        self.assertEqual(manifest["hash_bound_provenance_lock"], "NO")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(row.eligible_spans, (2, 4, 8, 16, 32, 64))
        self.assertEqual(row.table36_fdm, 1.26)
        self.assertEqual(row.status, "LOCKED_SOURCE_NATIVE_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM")

        result_path = Path("docs/process/CARVER_S09_MES_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM_ROW_LOCK_RESULT_2026-06-03.md")
        self.assertTrue(result_path.exists(), f"Missing eligible/FDM result: {result_path}")
        result_text = result_path.read_text(encoding="utf-8")
        ledger = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "speed/20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv"
        ).read_text(encoding="utf-8")
        status = json.loads(
            Path(
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
                "speed/20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_status.json"
            ).read_text(encoding="utf-8")
        )

        self.assertIn("LOCKED_S09_MES_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM_ROW_NOT_BACKTEST", result_text)
        self.assertEqual(ledger.splitlines()[0], "eligible_spans,table36_fdm,source_label,source_sha256,status")
        self.assertIn("2|4|8|16|32|64,1.26,LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_LEDGER,", ledger)
        self.assertIn(",LOCKED_SOURCE_NATIVE_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM", ledger)
        self.assertEqual(status["status"], "LOCKED_S09_MES_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM_ROW_NOT_BACKTEST")
        self.assertEqual(status["eligible_spans"], [2, 4, 8, 16, 32, 64])
        self.assertEqual(status["table36_fdm"], 1.26)
        self.assertEqual(status["remaining_evidence_count"], 1)
        self.assertEqual(status["hash_bound_provenance_lock"], "NO")
        self.assertEqual(status["forecast_computation"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertNotIn("READY_FOR_BACKTEST", result_text + ledger)
        self.assertNotIn("READY_FOR_LOCKBOX", result_text + ledger)
        self.assertNotIn("CFD_ADAPTER", result_text + ledger)

        hostile_configs = (
            replace(config, execution_authorized=False),
            replace(config, lane_class="CFD_ADAPTER"),
            replace(config, root="ES"),
            replace(config, row_id="APPENDIX_C_174_007"),
            replace(config, window_start="2020-04-06"),
            replace(config, dual_speed_eligibility_status="UNLOCKED"),
            replace(config, eligible_speed_set_lock=False),
            replace(config, table36_fdm_row_lock=False),
            replace(config, hash_bound_provenance_lock=True),
            replace(config, forecast_computation=True),
            replace(config, diagnostics_authorized=True),
            replace(config, backtest_authorized=True),
            replace(config, test_validation_lockbox_forward_authorized=True),
            replace(config, git_operations_authorized=True),
        )
        for hostile in hostile_configs:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    run_eligible_speed_set_table36_fdm_lock_guard(hostile)

        with self.assertRaises(CarverBlocked):
            build_eligible_speed_set_table36_fdm_row(speed_rows=({**speed_rows[0], "eligible": "False"}, *speed_rows[1:]))

    def test_s09_mes_hash_bound_provenance_lock_completes_evidence_without_readiness_or_backtest(self) -> None:
        from tools.databento.carver_s09_mes_hash_bound_provenance_lock import (  # noqa: PLC0415
            HASH_PATH,
            S09MESHashBoundProvenanceLockConfig,
            STATUS_PATH,
            build_request_manifest_payload,
            run_hash_bound_provenance_lock_guard,
        )

        config = S09MESHashBoundProvenanceLockConfig(
            execution_authorized=True,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
            hash_bound_provenance_lock=True,
            strategy_input_readiness_gate=False,
            forecast_computation=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
            git_operations_authorized=False,
        )

        result = run_hash_bound_provenance_lock_guard(config)
        manifest = build_request_manifest_payload(config)
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        ledger = Path(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/"
            "evidence/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_required_evidence_ledger.csv"
        ).read_text(encoding="utf-8")
        result_text = Path("docs/process/CARVER_S09_MES_HASH_BOUND_PROVENANCE_LOCK_RESULT_2026-06-03.md").read_text(encoding="utf-8")
        hashes = HASH_PATH.read_text(encoding="utf-8")
        combined = "\n".join((json.dumps(manifest, sort_keys=True), json.dumps(status, sort_keys=True), ledger, result_text, hashes))

        self.assertEqual(result["status"], "AUTHORIZED_HASH_BOUND_PROVENANCE_LOCK_READY")
        self.assertEqual(manifest["hash_bound_provenance_lock"], "YES")
        self.assertEqual(manifest["strategy_input_readiness_gate"], "NO")
        self.assertEqual(manifest["next_gate"], "S09_MES_STRATEGY_INPUT_READINESS_GATE")
        self.assertEqual(manifest["forecast_computation"], "NO")
        self.assertEqual(manifest["diagnostics_run"], "NO")
        self.assertEqual(manifest["backtests_run"], "NO")
        self.assertEqual(manifest["test_validation_lockbox_forward_access"], "NO")
        self.assertEqual(status["status"], "LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION")
        self.assertEqual(status["remaining_evidence_count"], 0)
        self.assertEqual(status["hash_bound_provenance_status"], "LOCKED_SOURCE_NATIVE_HASH_BOUND_PROVENANCE")
        self.assertEqual(status["strategy_input_readiness_status"], "S09_MES_STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_GATE")
        self.assertEqual(status["next_gate"], "S09_MES_STRATEGY_INPUT_READINESS_GATE")
        self.assertEqual(status["forecast_computation"], "NO")
        self.assertEqual(status["diagnostics_run"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertIn("hash_bound_provenance,LOCKED_SOURCE_NATIVE_EVIDENCE,LOCKED_SOURCE_NATIVE_EVIDENCE", ledger)
        self.assertIn("20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv", hashes)
        self.assertNotIn("/hashes/", hashes)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

        hostile_configs = (
            replace(config, execution_authorized=False),
            replace(config, lane_class="CFD_ADAPTER"),
            replace(config, root="ES"),
            replace(config, row_id="APPENDIX_C_174_007"),
            replace(config, window_start="2020-04-06"),
            replace(config, window_end="2020-04-06"),
            replace(config, hash_bound_provenance_lock=False),
            replace(config, strategy_input_readiness_gate=True),
            replace(config, forecast_computation=True),
            replace(config, diagnostics_authorized=True),
            replace(config, backtest_authorized=True),
            replace(config, test_validation_lockbox_forward_authorized=True),
            replace(config, git_operations_authorized=True),
        )
        for hostile in hostile_configs:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    run_hash_bound_provenance_lock_guard(hostile)

    def test_s09_mes_official_lifecycle_evidence_artifact_contract_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_official_lifecycle_evidence_artifact_contract_bundle,
        )

        bundle = build_s09_mes_official_lifecycle_evidence_artifact_contract_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_ARTIFACT_CONTRACT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_ARTIFACT_CONTRACT_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_ARTIFACT_CONTRACT_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        contract = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = contract + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_OFFICIAL_LIFECYCLE_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION",
            contract,
        )
        self.assertIn("selected_evidence_name: official_lifecycle_evidence", contract)
        self.assertIn("2019-05-05 through 2020-04-05", contract)
        self.assertIn("SOURCE_NATIVE_FUTURES", contract)
        self.assertIn("APPENDIX_C_174_006", contract)
        self.assertIn(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv",
            contract,
        )
        self.assertIn(
            "raw_symbol,first_completed_trading_date,last_completed_trading_date,expiration_completed_trading_date,source_label,source_sha256,status",
            contract,
        )
        self.assertIn("LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE", contract)
        self.assertIn("completed bars only", contract)
        self.assertIn("MES symbols only", contract)
        self.assertIn("no Databento API access", contract)
        self.assertIn("no provider login", contract)
        self.assertIn("no source extraction", contract)
        self.assertIn("no market-row parsing", contract)
        self.assertIn("no risk runtime computation", contract)
        self.assertIn("no cost computation", contract)
        self.assertIn("no forecast computation", contract)
        self.assertIn("no diagnostics", contract)
        self.assertIn("no backtests", contract)
        self.assertIn("no TEST", contract)
        self.assertIn("no VALIDATION", contract)
        self.assertIn("no Lockbox", contract)
        self.assertIn("no Forward", contract)
        self.assertIn("no Git staging", contract)
        self.assertIn("build_s09_mes_official_lifecycle_evidence_artifact_contract_bundle", audit)
        self.assertIn("hash manifest covers contract and audit only", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

    def test_s09_mes_roll_trading_day_semantics_artifact_contract_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_roll_trading_day_semantics_artifact_contract_bundle,
        )

        bundle = build_s09_mes_roll_trading_day_semantics_artifact_contract_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        contract = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = contract + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION",
            contract,
        )
        self.assertIn("selected_evidence_name: roll_trading_day_semantics", contract)
        self.assertIn("official_lifecycle_evidence_status: LOCKED_SOURCE_NATIVE_EVIDENCE", contract)
        self.assertIn("remaining_evidence_count: 9", contract)
        self.assertIn("2019-05-05 through 2020-04-05", contract)
        self.assertIn("SOURCE_NATIVE_FUTURES", contract)
        self.assertIn("APPENDIX_C_174_006", contract)
        self.assertIn(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv",
            contract,
        )
        self.assertIn(
            "old_symbol,new_symbol,provider_roll_date,completed_roll_date,source_label,source_sha256,status",
            contract,
        )
        self.assertIn("LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS", contract)
        self.assertIn("completed bars only", contract)
        self.assertIn("MES symbols only", contract)
        self.assertIn("no Databento API access", contract)
        self.assertIn("no provider login", contract)
        self.assertIn("no source extraction", contract)
        self.assertIn("no market-row parsing", contract)
        self.assertIn("no risk runtime computation", contract)
        self.assertIn("no cost computation", contract)
        self.assertIn("no forecast computation", contract)
        self.assertIn("no diagnostics", contract)
        self.assertIn("no backtests", contract)
        self.assertIn("no TEST", contract)
        self.assertIn("no VALIDATION", contract)
        self.assertIn("no Lockbox", contract)
        self.assertIn("no Forward", contract)
        self.assertIn("no Git staging", contract)
        self.assertIn("build_s09_mes_roll_trading_day_semantics_artifact_contract_bundle", audit)
        self.assertIn("hash manifest covers contract and audit only", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

    def test_s09_mes_annual_risk_runtime_artifact_contract_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_annual_risk_runtime_artifact_contract_bundle,
        )

        bundle = build_s09_mes_annual_risk_runtime_artifact_contract_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        contract = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = contract + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION",
            contract,
        )
        self.assertIn("selected_evidence_name: annual_risk_runtime_values", contract)
        self.assertIn("official_lifecycle_evidence_status: LOCKED_SOURCE_NATIVE_EVIDENCE", contract)
        self.assertIn("roll_trading_day_semantics_status: LOCKED_SOURCE_NATIVE_EVIDENCE", contract)
        self.assertIn("remaining_evidence_count: 8", contract)
        self.assertIn("2019-05-05 through 2020-04-05", contract)
        self.assertIn("SOURCE_NATIVE_FUTURES", contract)
        self.assertIn("APPENDIX_C_174_006", contract)
        self.assertIn(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
            contract,
        )
        self.assertIn(
            "completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_label,source_sha256,status",
            contract,
        )
        self.assertIn("LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE", contract)
        self.assertIn("30/70 annual-risk blend", contract)
        self.assertIn("completed bars only", contract)
        self.assertIn("no Databento API access", contract)
        self.assertIn("no provider login", contract)
        self.assertIn("no source extraction", contract)
        self.assertIn("no market-row parsing", contract)
        self.assertIn("no cost computation", contract)
        self.assertIn("no forecast computation", contract)
        self.assertIn("no diagnostics", contract)
        self.assertIn("no backtests", contract)
        self.assertIn("no TEST", contract)
        self.assertIn("no VALIDATION", contract)
        self.assertIn("no Lockbox", contract)
        self.assertIn("no Forward", contract)
        self.assertIn("no Git staging", contract)
        self.assertIn("build_s09_mes_annual_risk_runtime_artifact_contract_bundle", audit)
        self.assertIn("hash manifest covers contract and audit only", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

    def test_s09_mes_daily_price_risk_artifact_contract_is_process_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_daily_price_risk_artifact_contract_bundle,
        )

        bundle = build_s09_mes_daily_price_risk_artifact_contract_bundle()

        expected_paths = (
            "docs/process/CARVER_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
            "docs/process/CARVER_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        contract = bundle[expected_paths[0]]
        audit = bundle[expected_paths[1]]
        hashes = bundle[expected_paths[2]]
        combined = contract + audit + hashes

        self.assertIn(
            "PROCESS_ONLY_S09_MES_DAILY_PRICE_RISK_VALUES_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION",
            contract,
        )
        self.assertIn("selected_evidence_name: daily_price_risk_values", contract)
        self.assertIn("official_lifecycle_evidence_status: LOCKED_SOURCE_NATIVE_EVIDENCE", contract)
        self.assertIn("roll_trading_day_semantics_status: LOCKED_SOURCE_NATIVE_EVIDENCE", contract)
        self.assertIn("annual_risk_runtime_values_status: LOCKED_SOURCE_NATIVE_EVIDENCE", contract)
        self.assertIn("remaining_evidence_count: 7", contract)
        self.assertIn("2019-05-05 through 2020-04-05", contract)
        self.assertIn("SOURCE_NATIVE_FUTURES", contract)
        self.assertIn("APPENDIX_C_174_006", contract)
        self.assertIn(
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv",
            contract,
        )
        self.assertIn(
            "completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,source_label,source_sha256,status",
            contract,
        )
        self.assertIn("LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE", contract)
        self.assertIn("current_price * annual_percentage_risk / 16", contract)
        self.assertIn("completed bars only", contract)
        self.assertIn("locked annual-risk runtime value", contract)
        self.assertIn("no Databento API access", contract)
        self.assertIn("no provider login", contract)
        self.assertIn("no source extraction", contract)
        self.assertIn("no market-row parsing", contract)
        self.assertIn("no cost computation", contract)
        self.assertIn("no forecast computation", contract)
        self.assertIn("no diagnostics", contract)
        self.assertIn("no backtests", contract)
        self.assertIn("no TEST", contract)
        self.assertIn("no VALIDATION", contract)
        self.assertIn("no Lockbox", contract)
        self.assertIn("no Forward", contract)
        self.assertIn("no Git staging", contract)
        self.assertIn("build_s09_mes_daily_price_risk_artifact_contract_bundle", audit)
        self.assertIn("hash manifest covers contract and audit only", audit)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertNotIn(expected_paths[2], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

    def test_s09_mes_roll_trading_day_semantics_lock_builds_only_authorized_family_from_local_roll_plan(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESRollTradingDaySemanticsLockConfig,
            build_s09_mes_roll_trading_day_semantics_lock_bundle_from_local_roll_plan,
            write_s09_mes_roll_trading_day_semantics_lock_artifacts,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            roll_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_machinery_dev_lineage"
                / "2019-05-05_2020-04-05"
                / "roll_plan"
            )
            roll_root.mkdir(parents=True)
            roll_plan_path = roll_root / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_roll_plan.csv"
            roll_plan_text = (
                "old_symbol,new_symbol,expiration_date,roll_buffer_date,roll_transition_date,old_close_on_roll_date,new_close_on_roll_date,old_history_additive_adjustment,old_source_raw_sha256,new_source_raw_sha256,roll_rule,adjustment_method\n"
                "MESM9,MESU9,2019-06-21,2019-06-16,2019-06-16,2895.75,2899.75,4.0,"
                f"{'A' * 64},{'B' * 64},STATIC_LIFECYCLE_BUFFER_ROLL_5_PROVIDER_DATES_MACHINERY_ONLY,LOCAL_ADDITIVE_BACK_ADJUSTMENT_NOT_STRATEGY_INPUT\n"
            )
            roll_plan_path.write_text(roll_plan_text, encoding="utf-8", newline="\n")
            roll_plan_sha256 = hashlib.sha256(roll_plan_text.encode("utf-8")).hexdigest().upper()
            hash_root = roll_plan_path.parents[1] / "hashes"
            hash_root.mkdir(parents=True)
            hash_path = hash_root / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_sha256.json"
            hash_path.write_text(
                json.dumps(
                    {
                        roll_plan_path.relative_to(root).as_posix().replace("/", "\\"): roll_plan_sha256,
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
            lifecycle_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_strategy_input_evidence_completion"
                / "2019-05-05_2020-04-05"
                / "lifecycle"
            )
            lifecycle_root.mkdir(parents=True)
            lifecycle_path = lifecycle_root / "20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv"
            lifecycle_path.write_text(
                "raw_symbol,first_completed_trading_date,last_completed_trading_date,expiration_completed_trading_date,source_label,source_sha256,status\n"
                f"MESM9,2019-05-05,2019-06-20,2019-06-21,LOCAL_DATABENTO_DEFINITION_CROSSCHECK_MESM9,{'C' * 64},LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE\n"
                f"MESU9,2019-05-05,2019-09-19,2019-09-20,LOCAL_DATABENTO_DEFINITION_CROSSCHECK_MESU9,{'D' * 64},LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE\n",
                encoding="utf-8",
                newline="\n",
            )

            config = S09MESRollTradingDaySemanticsLockConfig(
                execution_authorized=True,
                selected_evidence_name="roll_trading_day_semantics",
                lane_class="SOURCE_NATIVE_FUTURES",
                root="MES",
                row_id="APPENDIX_C_174_006",
                machinery_development_slice="2019-05-05 through 2020-04-05",
                runtime_input_lock_scope="oldest minimum machinery-development slice only",
                design_ordering="oldest authorized completed source-native data first",
                local_metadata_root=root,
                databento_api_access_authorized=False,
                provider_login_authorized=False,
                market_row_parsing_authorized=False,
                risk_runtime_computation_authorized=False,
                cost_computation_authorized=False,
                speed_eligibility_computation_authorized=False,
                forecast_computation_authorized=False,
                diagnostics_authorized=False,
                backtest_authorized=False,
                test_validation_lockbox_forward_authorized=False,
                git_operations_authorized=False,
            )

            bundle = build_s09_mes_roll_trading_day_semantics_lock_bundle_from_local_roll_plan(config)

            expected_paths = (
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_status.json",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_provenance.md",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_sha256.txt",
            )
            self.assertEqual(tuple(bundle), expected_paths)

            roll_ledger = bundle[expected_paths[0]]
            status = json.loads(bundle[expected_paths[1]])
            provenance = bundle[expected_paths[2]]
            hashes = bundle[expected_paths[3]]
            combined = "\n".join(bundle.values())

            self.assertEqual(
                roll_ledger.splitlines()[0],
                "old_symbol,new_symbol,provider_roll_date,completed_roll_date,source_label,source_sha256,status",
            )
            self.assertIn(
                f"MESM9,MESU9,2019-06-16,2019-06-17,LOCAL_MACHINERY_DEV_ROLL_PLAN_COMPLETED_BAR_NORMALIZATION,{roll_plan_sha256},LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS",
                roll_ledger,
            )
            self.assertEqual(status["status"], "LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS")
            self.assertEqual(status["selected_evidence_name"], "roll_trading_day_semantics")
            self.assertEqual(status["remaining_evidence_count"], 8)
            self.assertEqual(status["databento_api_access"], "NO")
            self.assertEqual(status["market_row_parsing"], "NO")
            self.assertEqual(status["forecast_computation"], "NO")
            self.assertEqual(status["backtests_run"], "NO")
            self.assertIn("roll_trading_day_semantics source-native evidence locking", provenance)
            self.assertIn("no Databento API access", provenance)
            self.assertIn("no market-row parsing", provenance)
            self.assertIn(expected_paths[0], hashes)
            self.assertIn(expected_paths[1], hashes)
            self.assertIn(expected_paths[2], hashes)
            self.assertNotIn(expected_paths[3], hashes)
            self.assertNotIn("/risk/", combined)
            self.assertNotIn("/cost/", combined)
            self.assertNotIn("/speed/", combined)
            self.assertNotIn("READY_FOR_BACKTEST", combined)
            self.assertNotIn("READY_FOR_LOCKBOX", combined)
            self.assertNotIn("CFD_ADAPTER", combined)

            written = write_s09_mes_roll_trading_day_semantics_lock_artifacts(
                execution_authorized=True,
                bundle=bundle,
                root=root,
            )
            self.assertEqual(tuple(path.relative_to(root).as_posix() for path in written), expected_paths)
            for path in written:
                self.assertTrue(path.exists(), path)
            with self.assertRaises(CarverBlocked):
                write_s09_mes_roll_trading_day_semantics_lock_artifacts(
                    execution_authorized=False,
                    bundle=bundle,
                    root=root,
                )

            hostile_configs = (
                replace(config, execution_authorized=False),
                replace(config, selected_evidence_name="official_lifecycle_evidence"),
                replace(config, lane_class="CFD_ADAPTER"),
                replace(config, root="ES"),
                replace(config, row_id="APPENDIX_C_174_002"),
                replace(config, machinery_development_slice="2022-01-03 through 2023-12-29"),
                replace(config, databento_api_access_authorized=True),
                replace(config, provider_login_authorized=True),
                replace(config, market_row_parsing_authorized=True),
                replace(config, forecast_computation_authorized=True),
                replace(config, diagnostics_authorized=True),
                replace(config, backtest_authorized=True),
                replace(config, test_validation_lockbox_forward_authorized=True),
                replace(config, git_operations_authorized=True),
            )
            for hostile in hostile_configs:
                with self.subTest(hostile=hostile):
                    with self.assertRaises(CarverBlocked):
                        build_s09_mes_roll_trading_day_semantics_lock_bundle_from_local_roll_plan(hostile)

    def test_s09_mes_annual_risk_runtime_lock_builds_only_authorized_family_from_local_lineage(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESAnnualRiskRuntimeValuesLockConfig,
            build_s09_mes_annual_risk_runtime_values_lock_bundle_from_local_lineage,
            write_s09_mes_annual_risk_runtime_values_lock_artifacts,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            lineage_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_machinery_dev_lineage"
                / "2019-05-05_2020-04-05"
                / "continuous_series"
            )
            lineage_root.mkdir(parents=True)
            continuous_path = lineage_root / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_continuous_daily_mes_machinery_only.csv"
            rows = [
                "completed_trading_date,source_raw_symbol,raw_open,raw_high,raw_low,raw_close,adjusted_open,adjusted_high,adjusted_low,adjusted_close,volume,cumulative_additive_adjustment,source_raw_sha256,lineage_status"
            ]
            start = date(2019, 5, 5)
            for index in range(40):
                day = start + timedelta(days=index)
                close = 100.0 + index
                rows.append(
                    f"{day.isoformat()},MESM9,{close - 1.0},{close + 1.0},{close - 2.0},{close},{close - 1.0},{close + 1.0},{close - 2.0},{close},1000.0,0.0,{'A' * 64},PROVISIONAL_LOCAL_MACHINERY_LINEAGE_NOT_STRATEGY_INPUT"
                )
            continuous_text = "\n".join(rows) + "\n"
            continuous_path.write_text(continuous_text, encoding="utf-8", newline="\n")
            continuous_sha256 = hashlib.sha256(continuous_text.encode("utf-8")).hexdigest().upper()
            hash_root = continuous_path.parents[1] / "hashes"
            hash_root.mkdir(parents=True)
            hash_path = hash_root / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_sha256.json"
            hash_path.write_text(
                json.dumps(
                    {
                        continuous_path.relative_to(root).as_posix().replace("/", "\\"): continuous_sha256,
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )

            evidence_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_strategy_input_evidence_completion"
                / "2019-05-05_2020-04-05"
            )
            lifecycle_root = evidence_root / "lifecycle"
            lifecycle_root.mkdir(parents=True)
            (lifecycle_root / "20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv").write_text(
                "raw_symbol,first_completed_trading_date,last_completed_trading_date,expiration_completed_trading_date,source_label,source_sha256,status\n"
                f"MESM9,2019-05-05,2019-06-20,2019-06-21,LOCAL_DATABENTO_DEFINITION_CROSSCHECK_MESM9,{'B' * 64},LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE\n",
                encoding="utf-8",
                newline="\n",
            )
            roll_root = evidence_root / "roll"
            roll_root.mkdir(parents=True)
            (roll_root / "20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv").write_text(
                "old_symbol,new_symbol,provider_roll_date,completed_roll_date,source_label,source_sha256,status\n"
                f"MESM9,MESU9,2019-06-16,2019-06-17,LOCAL_MACHINERY_DEV_ROLL_PLAN_COMPLETED_BAR_NORMALIZATION,{'C' * 64},LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS\n",
                encoding="utf-8",
                newline="\n",
            )

            config = S09MESAnnualRiskRuntimeValuesLockConfig(
                execution_authorized=True,
                selected_evidence_name="annual_risk_runtime_values",
                lane_class="SOURCE_NATIVE_FUTURES",
                root="MES",
                row_id="APPENDIX_C_174_006",
                machinery_development_slice="2019-05-05 through 2020-04-05",
                runtime_input_lock_scope="oldest minimum machinery-development slice only",
                design_ordering="oldest authorized completed source-native data first",
                local_metadata_root=root,
                annual_risk_runtime_computation_authorized=True,
                databento_api_access_authorized=False,
                provider_login_authorized=False,
                market_row_parsing_authorized=False,
                cost_computation_authorized=False,
                speed_eligibility_computation_authorized=False,
                forecast_computation_authorized=False,
                diagnostics_authorized=False,
                backtest_authorized=False,
                test_validation_lockbox_forward_authorized=False,
                git_operations_authorized=False,
            )

            bundle = build_s09_mes_annual_risk_runtime_values_lock_bundle_from_local_lineage(config)

            expected_paths = (
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_status.json",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_provenance.md",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_sha256.txt",
            )
            self.assertEqual(tuple(bundle), expected_paths)

            annual_ledger = bundle[expected_paths[0]]
            status = json.loads(bundle[expected_paths[1]])
            provenance = bundle[expected_paths[2]]
            hashes = bundle[expected_paths[3]]
            combined = "\n".join(bundle.values())

            self.assertEqual(
                annual_ledger.splitlines()[0],
                "completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_label,source_sha256,status",
            )
            self.assertGreater(len(annual_ledger.splitlines()), 1)
            self.assertIn(
                f"LOCAL_MACHINERY_DEV_CONTINUOUS_LINEAGE_EWMA32_ANNUAL_RISK,{continuous_sha256},LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE",
                annual_ledger,
            )
            self.assertEqual(status["status"], "LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE")
            self.assertEqual(status["selected_evidence_name"], "annual_risk_runtime_values")
            self.assertEqual(status["remaining_evidence_count"], 7)
            self.assertEqual(status["annual_risk_runtime_computation"], "YES_ANNUAL_RISK_ONLY")
            self.assertEqual(status["databento_api_access"], "NO")
            self.assertEqual(status["market_row_parsing"], "NO")
            self.assertEqual(status["forecast_computation"], "NO")
            self.assertEqual(status["backtests_run"], "NO")
            self.assertIn("annual_risk_runtime_values source-native evidence locking", provenance)
            self.assertIn("30/70 long-run/current EWMA32 annual-risk blend", provenance)
            self.assertIn("no Databento API access", provenance)
            self.assertIn("no market-row parsing", provenance)
            self.assertIn(expected_paths[0], hashes)
            self.assertIn(expected_paths[1], hashes)
            self.assertIn(expected_paths[2], hashes)
            self.assertNotIn(expected_paths[3], hashes)
            self.assertNotIn("2022-01-03_2023-12-29", combined)
            self.assertNotIn("READY_FOR_BACKTEST", combined)
            self.assertNotIn("READY_FOR_LOCKBOX", combined)
            self.assertNotIn("CFD_ADAPTER", combined)
            self.assertNotIn("/cost/", combined)
            self.assertNotIn("/speed/", combined)

            written = write_s09_mes_annual_risk_runtime_values_lock_artifacts(
                execution_authorized=True,
                bundle=bundle,
                root=root,
            )
            self.assertEqual(tuple(path.relative_to(root).as_posix() for path in written), expected_paths)
            for path in written:
                self.assertTrue(path.exists(), path)
            with self.assertRaises(CarverBlocked):
                write_s09_mes_annual_risk_runtime_values_lock_artifacts(
                    execution_authorized=False,
                    bundle=bundle,
                    root=root,
                )

            hostile_configs = (
                replace(config, execution_authorized=False),
                replace(config, selected_evidence_name="daily_price_risk_values"),
                replace(config, lane_class="CFD_ADAPTER"),
                replace(config, root="ES"),
                replace(config, row_id="APPENDIX_C_174_002"),
                replace(config, machinery_development_slice="2022-01-03 through 2023-12-29"),
                replace(config, annual_risk_runtime_computation_authorized=False),
                replace(config, databento_api_access_authorized=True),
                replace(config, provider_login_authorized=True),
                replace(config, market_row_parsing_authorized=True),
                replace(config, cost_computation_authorized=True),
                replace(config, speed_eligibility_computation_authorized=True),
                replace(config, forecast_computation_authorized=True),
                replace(config, diagnostics_authorized=True),
                replace(config, backtest_authorized=True),
                replace(config, test_validation_lockbox_forward_authorized=True),
                replace(config, git_operations_authorized=True),
            )
            for hostile in hostile_configs:
                with self.subTest(hostile=hostile):
                    with self.assertRaises(CarverBlocked):
                        build_s09_mes_annual_risk_runtime_values_lock_bundle_from_local_lineage(hostile)

    def test_s09_mes_daily_price_risk_lock_builds_only_authorized_family_from_locked_annual_risk(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESDailyPriceRiskValuesLockConfig,
            build_s09_mes_daily_price_risk_values_lock_bundle_from_locked_annual_risk,
            write_s09_mes_daily_price_risk_values_lock_artifacts,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            lineage_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_machinery_dev_lineage"
                / "2019-05-05_2020-04-05"
                / "continuous_series"
            )
            lineage_root.mkdir(parents=True)
            continuous_path = lineage_root / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_continuous_daily_mes_machinery_only.csv"
            continuous_text = (
                "completed_trading_date,source_raw_symbol,raw_open,raw_high,raw_low,raw_close,adjusted_open,adjusted_high,adjusted_low,adjusted_close,volume,cumulative_additive_adjustment,source_raw_sha256,lineage_status\n"
                f"2019-06-11,MESM9,99.0,101.0,98.0,100.0,99.0,101.0,98.0,100.0,1000.0,0.0,{'A' * 64},PROVISIONAL_LOCAL_MACHINERY_LINEAGE_NOT_STRATEGY_INPUT\n"
                f"2019-06-12,MESM9,111.0,113.0,110.0,112.0,111.0,113.0,110.0,112.0,1000.0,0.0,{'A' * 64},PROVISIONAL_LOCAL_MACHINERY_LINEAGE_NOT_STRATEGY_INPUT\n"
            )
            continuous_path.write_text(continuous_text, encoding="utf-8", newline="\n")
            continuous_sha256 = hashlib.sha256(continuous_text.encode("utf-8")).hexdigest().upper()
            hash_root = continuous_path.parents[1] / "hashes"
            hash_root.mkdir(parents=True)
            (hash_root / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_sha256.json").write_text(
                json.dumps(
                    {continuous_path.relative_to(root).as_posix().replace("/", "\\"): continuous_sha256},
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )

            evidence_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_strategy_input_evidence_completion"
                / "2019-05-05_2020-04-05"
            )
            lifecycle_root = evidence_root / "lifecycle"
            lifecycle_root.mkdir(parents=True)
            (lifecycle_root / "20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv").write_text(
                "raw_symbol,first_completed_trading_date,last_completed_trading_date,expiration_completed_trading_date,source_label,source_sha256,status\n"
                f"MESM9,2019-05-05,2019-06-20,2019-06-21,LOCAL_DATABENTO_DEFINITION_CROSSCHECK_MESM9,{'B' * 64},LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE\n",
                encoding="utf-8",
                newline="\n",
            )
            roll_root = evidence_root / "roll"
            roll_root.mkdir(parents=True)
            (roll_root / "20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv").write_text(
                "old_symbol,new_symbol,provider_roll_date,completed_roll_date,source_label,source_sha256,status\n"
                f"MESM9,MESU9,2019-06-16,2019-06-17,LOCAL_MACHINERY_DEV_ROLL_PLAN_COMPLETED_BAR_NORMALIZATION,{'C' * 64},LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS\n",
                encoding="utf-8",
                newline="\n",
            )
            annual_root = evidence_root / "risk"
            annual_root.mkdir(parents=True)
            annual_path = annual_root / "20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv"
            annual_text = (
                "completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_label,source_sha256,status\n"
                f"2019-06-11,0.2,0.1,0.13,LOCAL_MACHINERY_DEV_CONTINUOUS_LINEAGE_EWMA32_ANNUAL_RISK,{'D' * 64},LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE\n"
                f"2019-06-12,0.3,0.2,0.23,LOCAL_MACHINERY_DEV_CONTINUOUS_LINEAGE_EWMA32_ANNUAL_RISK,{'D' * 64},LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE\n"
            )
            annual_path.write_text(annual_text, encoding="utf-8", newline="\n")
            annual_sha256 = hashlib.sha256(annual_text.encode("utf-8")).hexdigest().upper()
            combined_source_sha256 = hashlib.sha256(
                (continuous_sha256 + annual_sha256).encode("utf-8")
            ).hexdigest().upper()

            config = S09MESDailyPriceRiskValuesLockConfig(
                execution_authorized=True,
                selected_evidence_name="daily_price_risk_values",
                lane_class="SOURCE_NATIVE_FUTURES",
                root="MES",
                row_id="APPENDIX_C_174_006",
                machinery_development_slice="2019-05-05 through 2020-04-05",
                runtime_input_lock_scope="oldest minimum machinery-development slice only",
                design_ordering="oldest authorized completed source-native data first",
                local_metadata_root=root,
                daily_price_risk_computation_authorized=True,
                databento_api_access_authorized=False,
                provider_login_authorized=False,
                market_row_parsing_authorized=False,
                risk_runtime_computation_authorized=False,
                cost_computation_authorized=False,
                speed_eligibility_computation_authorized=False,
                forecast_computation_authorized=False,
                diagnostics_authorized=False,
                backtest_authorized=False,
                test_validation_lockbox_forward_authorized=False,
                git_operations_authorized=False,
            )

            bundle = build_s09_mes_daily_price_risk_values_lock_bundle_from_locked_annual_risk(config)

            expected_paths = (
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_DAILY_PRICE_RISK_status.json",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_DAILY_PRICE_RISK_provenance.md",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_DAILY_PRICE_RISK_sha256.txt",
            )
            self.assertEqual(tuple(bundle), expected_paths)

            daily_ledger = bundle[expected_paths[0]]
            status = json.loads(bundle[expected_paths[1]])
            provenance = bundle[expected_paths[2]]
            hashes = bundle[expected_paths[3]]
            combined = "\n".join(bundle.values())

            self.assertEqual(
                daily_ledger.splitlines()[0],
                "completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,source_label,source_sha256,status",
            )
            self.assertIn(
                f"2019-06-11,100.0,0.13,0.8125,LOCAL_MACHINERY_DEV_CONTINUOUS_LINEAGE_AND_ANNUAL_RISK_DAILY_PRICE_RISK,{combined_source_sha256},LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE",
                daily_ledger,
            )
            self.assertIn(
                f"2019-06-12,112.0,0.23,1.61,LOCAL_MACHINERY_DEV_CONTINUOUS_LINEAGE_AND_ANNUAL_RISK_DAILY_PRICE_RISK,{combined_source_sha256},LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE",
                daily_ledger,
            )
            self.assertEqual(status["status"], "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE")
            self.assertEqual(status["selected_evidence_name"], "daily_price_risk_values")
            self.assertEqual(status["remaining_evidence_count"], 6)
            self.assertEqual(status["daily_price_risk_computation"], "YES_DAILY_PRICE_ONLY")
            self.assertEqual(status["databento_api_access"], "NO")
            self.assertEqual(status["market_row_parsing"], "NO")
            self.assertEqual(status["forecast_computation"], "NO")
            self.assertEqual(status["backtests_run"], "NO")
            self.assertIn("daily_price_risk_values source-native evidence locking", provenance)
            self.assertIn("current_price * annual_percentage_risk / 16", provenance)
            self.assertIn("no Databento API access", provenance)
            self.assertIn("no market-row parsing", provenance)
            self.assertIn(expected_paths[0], hashes)
            self.assertIn(expected_paths[1], hashes)
            self.assertIn(expected_paths[2], hashes)
            self.assertNotIn(expected_paths[3], hashes)
            self.assertNotIn("2022-01-03_2023-12-29", combined)
            self.assertNotIn("READY_FOR_BACKTEST", combined)
            self.assertNotIn("READY_FOR_LOCKBOX", combined)
            self.assertNotIn("CFD_ADAPTER", combined)
            self.assertNotIn("/cost/", combined)
            self.assertNotIn("/speed/", combined)

            written = write_s09_mes_daily_price_risk_values_lock_artifacts(
                execution_authorized=True,
                bundle=bundle,
                root=root,
            )
            self.assertEqual(tuple(path.relative_to(root).as_posix() for path in written), expected_paths)
            for path in written:
                self.assertTrue(path.exists(), path)
            with self.assertRaises(CarverBlocked):
                write_s09_mes_daily_price_risk_values_lock_artifacts(
                    execution_authorized=False,
                    bundle=bundle,
                    root=root,
                )

            hostile_configs = (
                replace(config, execution_authorized=False),
                replace(config, selected_evidence_name="historical_mes_cost_values"),
                replace(config, lane_class="CFD_ADAPTER"),
                replace(config, root="ES"),
                replace(config, row_id="APPENDIX_C_174_002"),
                replace(config, machinery_development_slice="2022-01-03 through 2023-12-29"),
                replace(config, daily_price_risk_computation_authorized=False),
                replace(config, databento_api_access_authorized=True),
                replace(config, provider_login_authorized=True),
                replace(config, market_row_parsing_authorized=True),
                replace(config, risk_runtime_computation_authorized=True),
                replace(config, cost_computation_authorized=True),
                replace(config, speed_eligibility_computation_authorized=True),
                replace(config, forecast_computation_authorized=True),
                replace(config, diagnostics_authorized=True),
                replace(config, backtest_authorized=True),
                replace(config, test_validation_lockbox_forward_authorized=True),
                replace(config, git_operations_authorized=True),
            )
            for hostile in hostile_configs:
                with self.subTest(hostile=hostile):
                    with self.assertRaises(CarverBlocked):
                        build_s09_mes_daily_price_risk_values_lock_bundle_from_locked_annual_risk(hostile)

    def test_s09_mes_historical_cost_attempt_fails_closed_when_active_cost_rows_are_missing(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESHistoricalMESCostValuesAttemptConfig,
            build_s09_mes_historical_mes_cost_values_fail_closed_bundle_from_active_evidence,
            write_s09_mes_historical_mes_cost_values_fail_closed_artifacts,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cost_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_strategy_input_evidence_completion"
                / "2019-05-05_2020-04-05"
                / "cost"
            )
            cost_root.mkdir(parents=True)
            (cost_root / "20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv").write_text(
                "completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status\n",
                encoding="utf-8",
                newline="\n",
            )

            config = S09MESHistoricalMESCostValuesAttemptConfig(
                execution_authorized=True,
                selected_evidence_name="historical_mes_cost_values",
                lane_class="SOURCE_NATIVE_FUTURES",
                root="MES",
                row_id="APPENDIX_C_174_006",
                machinery_development_slice="2019-05-05 through 2020-04-05",
                runtime_input_lock_scope="oldest minimum machinery-development slice only",
                design_ordering="oldest authorized completed source-native data first",
                local_metadata_root=root,
                historical_cost_values_authorized=True,
                databento_api_access_authorized=False,
                provider_login_authorized=False,
                market_row_parsing_authorized=False,
                risk_runtime_computation_authorized=False,
                cost_computation_authorized=False,
                speed_eligibility_computation_authorized=False,
                forecast_computation_authorized=False,
                diagnostics_authorized=False,
                backtest_authorized=False,
                test_validation_lockbox_forward_authorized=False,
                git_operations_authorized=False,
            )

            bundle = build_s09_mes_historical_mes_cost_values_fail_closed_bundle_from_active_evidence(config)

            expected_paths = (
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_status.json",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_provenance.md",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_sha256.txt",
            )
            self.assertEqual(tuple(bundle), expected_paths)

            ledger = bundle[expected_paths[0]]
            status = json.loads(bundle[expected_paths[1]])
            provenance = bundle[expected_paths[2]]
            hashes = bundle[expected_paths[3]]
            combined = "\n".join(bundle.values())

            self.assertEqual(
                ledger,
                "completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status\r\n",
            )
            self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED")
            self.assertEqual(status["selected_evidence_name"], "historical_mes_cost_values")
            self.assertEqual(status["remaining_evidence_count"], 6)
            self.assertEqual(status["locked_historical_cost_rows"], 0)
            self.assertEqual(status["missing_cost_components"], ["exchange_fee", "clearing_regulatory_fee", "broker_commission", "spread_slippage"])
            self.assertEqual(status["cost_computation"], "NO")
            self.assertEqual(status["databento_api_access"], "NO")
            self.assertEqual(status["backtests_run"], "NO")
            self.assertIn("historical_mes_cost_values authorized evidence attempt", provenance)
            self.assertIn("active cost ledger is header-only", provenance)
            self.assertIn("no Databento API access", provenance)
            self.assertIn(expected_paths[0], hashes)
            self.assertIn(expected_paths[1], hashes)
            self.assertIn(expected_paths[2], hashes)
            self.assertNotIn(expected_paths[3], hashes)
            self.assertNotIn("2022-01-03_2023-12-29", combined)
            self.assertNotIn("READY_FOR_BACKTEST", combined)
            self.assertNotIn("READY_FOR_LOCKBOX", combined)
            self.assertNotIn("CFD_ADAPTER", combined)
            self.assertNotIn("/speed/", combined)

            written = write_s09_mes_historical_mes_cost_values_fail_closed_artifacts(
                execution_authorized=True,
                bundle=bundle,
                root=root,
            )
            self.assertEqual(tuple(path.relative_to(root).as_posix() for path in written), expected_paths)
            for path in written:
                self.assertTrue(path.exists(), path)
            with self.assertRaises(CarverBlocked):
                write_s09_mes_historical_mes_cost_values_fail_closed_artifacts(
                    execution_authorized=False,
                    bundle=bundle,
                    root=root,
                )

            hostile_configs = (
                replace(config, execution_authorized=False),
                replace(config, selected_evidence_name="risk_adjusted_cost_values"),
                replace(config, lane_class="CFD_ADAPTER"),
                replace(config, root="ES"),
                replace(config, row_id="APPENDIX_C_174_002"),
                replace(config, machinery_development_slice="2022-01-03 through 2023-12-29"),
                replace(config, historical_cost_values_authorized=False),
                replace(config, databento_api_access_authorized=True),
                replace(config, provider_login_authorized=True),
                replace(config, market_row_parsing_authorized=True),
                replace(config, risk_runtime_computation_authorized=True),
                replace(config, cost_computation_authorized=True),
                replace(config, speed_eligibility_computation_authorized=True),
                replace(config, forecast_computation_authorized=True),
                replace(config, diagnostics_authorized=True),
                replace(config, backtest_authorized=True),
                replace(config, test_validation_lockbox_forward_authorized=True),
                replace(config, git_operations_authorized=True),
            )
            for hostile in hostile_configs:
                with self.subTest(hostile=hostile):
                    with self.assertRaises(CarverBlocked):
                        build_s09_mes_historical_mes_cost_values_fail_closed_bundle_from_active_evidence(hostile)

    def test_s09_mes_official_lifecycle_evidence_lock_builds_only_authorized_family_from_local_metadata(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESOfficialLifecycleEvidenceLockConfig,
            build_s09_mes_official_lifecycle_evidence_lock_bundle_from_local_metadata,
            write_s09_mes_official_lifecycle_evidence_lock_artifacts,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_machinery_dev_minimum_slice"
                / "2019-05-05_2020-04-05"
                / "raw_provider_metadata"
            )
            source_root.mkdir(parents=True)
            definition_path = source_root / "20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_MESM9_definition.csv"
            definition_text = (
                "ts_recv,raw_symbol,expiration,asset,currency,contract_multiplier,min_price_increment,exchange\n"
                "2019-05-05 16:05:05.052696398+00:00,MESM9,2019-06-21 13:30:00+00:00,MES,USD,5.0,0.25,XCME\n"
                "2019-06-20 00:00:00+00:00,MESM9,2019-06-21 13:30:00+00:00,MES,USD,5.0,0.25,XCME\n"
            )
            definition_path.write_text(definition_text, encoding="utf-8", newline="\n")
            definition_sha256 = hashlib.sha256(definition_text.encode("utf-8")).hexdigest().upper()
            ledger_path = source_root / "20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_definition_ledger.csv"
            ledger_path.write_text(
                "raw_symbol,definition_rows,definition_status,definition_csv\n"
                f"MESM9,42,DATABENTO_DEFINITION_ROWS_PRESENT,{definition_path.relative_to(root).as_posix()}\n",
                encoding="utf-8",
                newline="\n",
            )
            crosscheck_root = (
                root
                / "docs"
                / "researchops"
                / "s09"
                / "mes_machinery_dev_lineage"
                / "2019-05-05_2020-04-05"
                / "lifecycle"
            )
            crosscheck_root.mkdir(parents=True)
            crosscheck_path = crosscheck_root / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_definition_crosscheck_ledger.csv"
            crosscheck_path.write_text(
                "raw_symbol,definition_csv,definition_csv_sha256,expiration_utc,product_code,currency,multiplier,tick_size,venue,lifecycle_source_status\n"
                f"MESM9,{definition_path.relative_to(root).as_posix()},{definition_sha256},2019-06-21T13:30:00+00:00,MES,USD,5.0,0.25,XCME,PROVIDER_DEFINITION_CROSSCHECK_ONLY_NOT_OFFICIAL_ROLL_SEMANTICS_LOCK\n",
                encoding="utf-8",
                newline="\n",
            )

            config = S09MESOfficialLifecycleEvidenceLockConfig(
                execution_authorized=True,
                selected_evidence_name="official_lifecycle_evidence",
                lane_class="SOURCE_NATIVE_FUTURES",
                root="MES",
                row_id="APPENDIX_C_174_006",
                machinery_development_slice="2019-05-05 through 2020-04-05",
                runtime_input_lock_scope="oldest minimum machinery-development slice only",
                design_ordering="oldest authorized completed source-native data first",
                local_metadata_root=root,
                databento_api_access_authorized=False,
                provider_login_authorized=False,
                market_row_parsing_authorized=False,
                risk_runtime_computation_authorized=False,
                cost_computation_authorized=False,
                speed_eligibility_computation_authorized=False,
                forecast_computation_authorized=False,
                diagnostics_authorized=False,
                backtest_authorized=False,
                test_validation_lockbox_forward_authorized=False,
                git_operations_authorized=False,
            )

            bundle = build_s09_mes_official_lifecycle_evidence_lock_bundle_from_local_metadata(config)

            expected_paths = (
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_status.json",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_provenance.md",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_sha256.txt",
            )
            self.assertEqual(tuple(bundle), expected_paths)

            lifecycle = bundle[expected_paths[0]]
            status = json.loads(bundle[expected_paths[1]])
            provenance = bundle[expected_paths[2]]
            hashes = bundle[expected_paths[3]]
            combined = "\n".join(bundle.values())

            self.assertEqual(
                lifecycle.splitlines()[0],
                "raw_symbol,first_completed_trading_date,last_completed_trading_date,expiration_completed_trading_date,source_label,source_sha256,status",
            )
            self.assertIn(
                f"MESM9,2019-05-05,2019-06-20,2019-06-21,LOCAL_DATABENTO_DEFINITION_CROSSCHECK_MESM9,{definition_sha256},LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE",
                lifecycle,
            )
            self.assertEqual(status["status"], "LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE")
            self.assertEqual(status["selected_evidence_name"], "official_lifecycle_evidence")
            self.assertEqual(status["remaining_evidence_count"], 9)
            self.assertEqual(status["databento_api_access"], "NO")
            self.assertEqual(status["market_row_parsing"], "NO")
            self.assertEqual(status["forecast_computation"], "NO")
            self.assertEqual(status["backtests_run"], "NO")
            self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
            self.assertIn("official_lifecycle_evidence source-native evidence locking", provenance)
            self.assertIn("no Databento API access", provenance)
            self.assertIn("no market-row parsing", provenance)
            self.assertIn(expected_paths[0], hashes)
            self.assertIn(expected_paths[1], hashes)
            self.assertIn(expected_paths[2], hashes)
            self.assertNotIn(expected_paths[3], hashes)
            self.assertNotIn("/roll/", combined)
            self.assertNotIn("/risk/", combined)
            self.assertNotIn("/cost/", combined)
            self.assertNotIn("/speed/", combined)
            self.assertNotIn("READY_FOR_BACKTEST", combined)
            self.assertNotIn("READY_FOR_LOCKBOX", combined)
            self.assertNotIn("CFD_ADAPTER", combined)

            written = write_s09_mes_official_lifecycle_evidence_lock_artifacts(
                execution_authorized=True,
                bundle=bundle,
                root=root,
            )
            self.assertEqual(tuple(path.relative_to(root).as_posix() for path in written), expected_paths)
            for path in written:
                self.assertTrue(path.exists(), path)
            with self.assertRaises(CarverBlocked):
                write_s09_mes_official_lifecycle_evidence_lock_artifacts(
                    execution_authorized=False,
                    bundle=bundle,
                    root=root,
                )

            hostile_configs = (
                replace(config, execution_authorized=False),
                replace(config, selected_evidence_name="roll_trading_day_semantics"),
                replace(config, lane_class="CFD_ADAPTER"),
                replace(config, root="ES"),
                replace(config, row_id="APPENDIX_C_174_002"),
                replace(config, machinery_development_slice="2022-01-03 through 2023-12-29"),
                replace(config, databento_api_access_authorized=True),
                replace(config, provider_login_authorized=True),
                replace(config, market_row_parsing_authorized=True),
                replace(config, forecast_computation_authorized=True),
                replace(config, diagnostics_authorized=True),
                replace(config, backtest_authorized=True),
                replace(config, test_validation_lockbox_forward_authorized=True),
                replace(config, git_operations_authorized=True),
            )
            for hostile in hostile_configs:
                with self.subTest(hostile=hostile):
                    with self.assertRaises(CarverBlocked):
                        build_s09_mes_official_lifecycle_evidence_lock_bundle_from_local_metadata(hostile)

    def test_s09_mes_strategy_input_evidence_completion_bookkeeping_marks_lifecycle_locked_only(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_strategy_input_evidence_completion_partial_bookkeeping_bundle,
        )

        bundle = build_s09_mes_strategy_input_evidence_completion_partial_bookkeeping_bundle(
            locked_evidence_names=("official_lifecycle_evidence",),
        )

        expected_paths = (
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/evidence/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_required_evidence_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/provenance/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_provenance.md",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/hashes/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        ledger = bundle[expected_paths[0]]
        status = json.loads(bundle[expected_paths[1]])
        provenance = bundle[expected_paths[2]]
        hashes = bundle[expected_paths[3]]
        combined = "\n".join(bundle.values())

        self.assertIn(
            "official_lifecycle_evidence,LOCKED_SOURCE_NATIVE_EVIDENCE,LOCKED_SOURCE_NATIVE_EVIDENCE",
            ledger,
        )
        self.assertIn(
            "roll_trading_day_semantics,LOCKED_SOURCE_NATIVE_EVIDENCE,FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_NOT_LOCKED",
            ledger,
        )
        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY")
        self.assertEqual(status["remaining_evidence_count"], 9)
        self.assertEqual(status["locked_evidence_names"], ["official_lifecycle_evidence"])
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertIn("partial evidence bookkeeping", provenance)
        self.assertIn("official_lifecycle_evidence", provenance)
        self.assertIn(expected_paths[0], hashes)
        self.assertIn(expected_paths[1], hashes)
        self.assertIn(expected_paths[2], hashes)
        self.assertNotIn(expected_paths[3], hashes)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)
        self.assertNotIn("CFD_ADAPTER", combined)

        roll_locked_bundle = build_s09_mes_strategy_input_evidence_completion_partial_bookkeeping_bundle(
            locked_evidence_names=("official_lifecycle_evidence", "roll_trading_day_semantics"),
        )
        roll_locked_ledger = roll_locked_bundle[expected_paths[0]]
        roll_locked_status = json.loads(roll_locked_bundle[expected_paths[1]])
        self.assertIn(
            "roll_trading_day_semantics,LOCKED_SOURCE_NATIVE_EVIDENCE,LOCKED_SOURCE_NATIVE_EVIDENCE",
            roll_locked_ledger,
        )
        self.assertIn(
            "annual_risk_runtime_values,LOCKED_SOURCE_NATIVE_EVIDENCE,FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_NOT_LOCKED",
            roll_locked_ledger,
        )
        self.assertEqual(roll_locked_status["remaining_evidence_count"], 8)
        self.assertEqual(
            roll_locked_status["locked_evidence_names"],
            ["official_lifecycle_evidence", "roll_trading_day_semantics"],
        )

        annual_locked_bundle = build_s09_mes_strategy_input_evidence_completion_partial_bookkeeping_bundle(
            locked_evidence_names=(
                "official_lifecycle_evidence",
                "roll_trading_day_semantics",
                "annual_risk_runtime_values",
            ),
        )
        annual_locked_ledger = annual_locked_bundle[expected_paths[0]]
        annual_locked_status = json.loads(annual_locked_bundle[expected_paths[1]])
        self.assertIn(
            "annual_risk_runtime_values,LOCKED_SOURCE_NATIVE_EVIDENCE,LOCKED_SOURCE_NATIVE_EVIDENCE",
            annual_locked_ledger,
        )
        self.assertIn(
            "daily_price_risk_values,LOCKED_SOURCE_NATIVE_EVIDENCE,FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_NOT_LOCKED",
            annual_locked_ledger,
        )
        self.assertEqual(annual_locked_status["remaining_evidence_count"], 7)
        self.assertEqual(
            annual_locked_status["locked_evidence_names"],
            ["official_lifecycle_evidence", "roll_trading_day_semantics", "annual_risk_runtime_values"],
        )

        daily_price_locked_bundle = build_s09_mes_strategy_input_evidence_completion_partial_bookkeeping_bundle(
            locked_evidence_names=(
                "official_lifecycle_evidence",
                "roll_trading_day_semantics",
                "annual_risk_runtime_values",
                "daily_price_risk_values",
            ),
        )
        daily_price_locked_ledger = daily_price_locked_bundle[expected_paths[0]]
        daily_price_locked_status = json.loads(daily_price_locked_bundle[expected_paths[1]])
        self.assertIn(
            "daily_price_risk_values,LOCKED_SOURCE_NATIVE_EVIDENCE,LOCKED_SOURCE_NATIVE_EVIDENCE",
            daily_price_locked_ledger,
        )
        self.assertIn(
            "historical_mes_cost_values,LOCKED_SOURCE_NATIVE_EVIDENCE,FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_NOT_LOCKED",
            daily_price_locked_ledger,
        )
        self.assertEqual(daily_price_locked_status["remaining_evidence_count"], 6)
        self.assertEqual(
            daily_price_locked_status["locked_evidence_names"],
            [
                "official_lifecycle_evidence",
                "roll_trading_day_semantics",
                "annual_risk_runtime_values",
                "daily_price_risk_values",
            ],
        )

        hostile_locked_sets = (
            (),
            ("roll_trading_day_semantics",),
            ("official_lifecycle_evidence", "annual_risk_runtime_values"),
            ("official_lifecycle_evidence", "roll_trading_day_semantics", "daily_price_risk_values"),
            ("official_lifecycle_evidence", "unknown_evidence"),
        )
        for locked in hostile_locked_sets:
            with self.subTest(locked=locked):
                with self.assertRaises(CarverBlocked):
                    build_s09_mes_strategy_input_evidence_completion_partial_bookkeeping_bundle(
                        locked_evidence_names=locked,
                    )

    def test_s09_mes_strategy_input_evidence_completion_guard_requires_authorization_and_boundaries(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceCompletionConfig,
            run_s09_mes_strategy_input_evidence_completion,
        )

        base = S09MESStrategyInputEvidenceCompletionConfig(
            execution_authorized=False,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice_start="2019-05-05",
            machinery_development_slice_end="2020-04-05",
            runtime_input_lock_scope="oldest minimum machinery-development slice only",
            design_ordering="oldest authorized completed source-native data first",
            databento_api_access_authorized=False,
            market_row_parsing_authorized=False,
            forecast_computation_authorized=False,
            diagnostics_authorized=False,
            backtest_authorized=False,
            test_validation_lockbox_forward_authorized=False,
        )

        with self.assertRaises(CarverBlocked):
            run_s09_mes_strategy_input_evidence_completion(base)

        authorized = replace(base, execution_authorized=True)
        result = run_s09_mes_strategy_input_evidence_completion(authorized)
        self.assertEqual(result["status"], "AUTHORIZED_PREFLIGHT_ONLY_NOT_EXECUTED")
        self.assertEqual(result["gate"], "S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE")
        self.assertEqual(result["lane_class"], "SOURCE_NATIVE_FUTURES")
        self.assertEqual(result["machinery_development_slice"], "2019-05-05 through 2020-04-05")
        self.assertEqual(result["forecast_computation"], "NO")
        self.assertEqual(result["backtests_run"], "NO")
        self.assertEqual(result["test_validation_lockbox_forward_access"], "NO")

        hostile_configs = (
            replace(authorized, lane_class="CFD_ADAPTER"),
            replace(authorized, root="ES"),
            replace(authorized, row_id="APPENDIX_C_174_002"),
            replace(authorized, machinery_development_slice_start="2022-01-03", machinery_development_slice_end="2023-12-29"),
            replace(authorized, runtime_input_lock_scope="two year dev window"),
            replace(authorized, design_ordering="newest data first"),
            replace(authorized, databento_api_access_authorized=True),
            replace(authorized, market_row_parsing_authorized=True),
            replace(authorized, forecast_computation_authorized=True),
            replace(authorized, diagnostics_authorized=True),
            replace(authorized, backtest_authorized=True),
            replace(authorized, test_validation_lockbox_forward_authorized=True),
        )
        for config in hostile_configs:
            with self.subTest(config=config):
                with self.assertRaises(CarverBlocked):
                    run_s09_mes_strategy_input_evidence_completion(config)

    def test_s09_mes_strategy_input_evidence_completion_guard_audit_is_process_only(self) -> None:
        audit_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GUARD_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
        )
        text = audit_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_AND_SYNTHETIC_CODE_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GUARD_NOT_DATA_NOT_BACKTEST", text)
        self.assertIn("S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("2019-05-05 through 2020-04-05", text)
        self.assertIn("oldest minimum machinery-development slice only", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("no Databento API access", text)
        self.assertIn("no market-row parsing", text)
        self.assertIn("no forecast computation", text)
        self.assertIn("no diagnostics", text)
        self.assertIn("no backtests", text)
        self.assertIn("no TEST", text)
        self.assertIn("no VALIDATION", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)
        self.assertIn("no Git staging", text)
        self.assertNotIn("2022-01-03_2023-12-29", text)

    def test_s09_mes_strategy_input_evidence_completion_builds_fail_closed_in_memory_bundle(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_strategy_input_evidence_completion_artifact_bundle,
        )

        bundle = build_s09_mes_strategy_input_evidence_completion_artifact_bundle()

        expected_paths = (
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/evidence/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_required_evidence_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/lifecycle/20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_RISK_ADJUSTED_COST_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/speed/20260603_S09_MES_SPEED_ELIGIBILITY_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/speed/20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/provenance/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_provenance.md",
            "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/hashes/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt",
        )
        self.assertEqual(tuple(bundle), expected_paths)

        ledger = bundle[expected_paths[0]]
        self.assertEqual(
            ledger.splitlines()[0],
            "evidence_name,required_status,current_status,blocking_reason,next_action",
        )
        for evidence_name in (
            "official_lifecycle_evidence",
            "roll_trading_day_semantics",
            "annual_risk_runtime_values",
            "daily_price_risk_values",
            "historical_mes_cost_values",
            "risk_adjusted_cost_values",
            "speed_eligibility_values",
            "eligible_speed_set",
            "table36_fdm_row",
            "hash_bound_provenance",
        ):
            self.assertIn(evidence_name, ledger)
        self.assertIn("FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_NOT_LOCKED", ledger)

        self.assertEqual(bundle[expected_paths[1]].splitlines()[0], "raw_symbol,first_completed_trading_date,last_completed_trading_date,expiration_completed_trading_date,source_label,source_sha256,status")
        self.assertEqual(bundle[expected_paths[2]].splitlines()[0], "old_symbol,new_symbol,provider_roll_date,completed_roll_date,source_label,source_sha256,status")
        self.assertEqual(bundle[expected_paths[3]].splitlines()[0], "completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_label,source_sha256,status")
        self.assertEqual(bundle[expected_paths[4]].splitlines()[0], "completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,source_label,source_sha256,status")
        self.assertEqual(bundle[expected_paths[5]].splitlines()[0], "completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status")
        self.assertEqual(bundle[expected_paths[6]].splitlines()[0], "completed_trading_date,total_cost_per_trade_currency,daily_price_risk_currency,risk_adjusted_cost_per_trade_sr,source_label,source_sha256,status")
        self.assertEqual(bundle[expected_paths[7]].splitlines()[0], "span,turnover,risk_adjusted_cost_per_trade_sr,threshold_sr,eligible,source_label,source_sha256,status")
        self.assertEqual(bundle[expected_paths[8]].splitlines()[0], "eligible_spans,table36_fdm,source_label,source_sha256,status")

        status = json.loads(bundle[expected_paths[9]])
        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["market_row_parsing"], "NO")
        self.assertEqual(status["forecast_computation"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")

        provenance = bundle[expected_paths[10]]
        self.assertIn("S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE", provenance)
        self.assertIn("2019-05-05 through 2020-04-05", provenance)
        self.assertIn("header-only/preflight evidence completion bundle", provenance)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", provenance)

        hashes = bundle[expected_paths[11]]
        for expected_path in expected_paths[:-1]:
            self.assertIn(expected_path, hashes)
        self.assertNotIn(expected_paths[11], hashes)
        self.assertNotIn("2022-01-03_2023-12-29", "\n".join(bundle.values()))
        self.assertNotIn("READY_FOR_BACKTEST", "\n".join(bundle.values()))
        self.assertNotIn("READY_FOR_LOCKBOX", "\n".join(bundle.values()))

    def test_s09_mes_strategy_input_evidence_completion_renders_lifecycle_and_roll_semantics_ledgers(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow,
            S09MESStrategyInputEvidenceCompletionRollSemanticsRow,
            render_s09_mes_strategy_input_evidence_completion_lifecycle_ledger_csv,
            render_s09_mes_strategy_input_evidence_completion_roll_semantics_ledger_csv,
        )

        lifecycle = S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow(
            raw_symbol="MESM9",
            first_completed_trading_date=date(2019, 5, 6),
            last_completed_trading_date=date(2019, 6, 20),
            expiration_completed_trading_date=date(2019, 6, 21),
            source_label="LOCKED_CME_MES_LIFECYCLE_SOURCE",
            source_sha256="A" * 64,
            status="LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE",
        )
        roll = S09MESStrategyInputEvidenceCompletionRollSemanticsRow(
            old_symbol="MESM9",
            new_symbol="MESU9",
            provider_roll_date=date(2019, 6, 16),
            completed_roll_date=date(2019, 6, 17),
            source_label="LOCKED_CME_GLOBEX_COMPLETED_BAR_CALENDAR",
            source_sha256="B" * 64,
            status="LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS",
        )

        lifecycle_csv = render_s09_mes_strategy_input_evidence_completion_lifecycle_ledger_csv((lifecycle,))
        roll_csv = render_s09_mes_strategy_input_evidence_completion_roll_semantics_ledger_csv((roll,))

        self.assertEqual(
            lifecycle_csv.splitlines()[0],
            "raw_symbol,first_completed_trading_date,last_completed_trading_date,expiration_completed_trading_date,source_label,source_sha256,status",
        )
        self.assertIn("MESM9,2019-05-06,2019-06-20,2019-06-21,LOCKED_CME_MES_LIFECYCLE_SOURCE", lifecycle_csv)
        self.assertEqual(
            roll_csv.splitlines()[0],
            "old_symbol,new_symbol,provider_roll_date,completed_roll_date,source_label,source_sha256,status",
        )
        self.assertIn("MESM9,MESU9,2019-06-16,2019-06-17,LOCKED_CME_GLOBEX_COMPLETED_BAR_CALENDAR", roll_csv)

        hostile_lifecycle_rows = (
            (),
            (replace(lifecycle, raw_symbol="ESM9"),),
            (replace(lifecycle, raw_symbol="MESM9-CFD"),),
            (replace(lifecycle, first_completed_trading_date=datetime(2019, 5, 6, tzinfo=timezone.utc)),),
            (replace(lifecycle, last_completed_trading_date=date(2019, 5, 5)),),
            (replace(lifecycle, expiration_completed_trading_date=date(2019, 6, 20)),),
            (replace(lifecycle, source_label=""),),
            (replace(lifecycle, source_sha256=""),),
            (replace(lifecycle, source_sha256="Z" * 64),),
            (replace(lifecycle, status="PROVISIONAL"),),
        )
        for rows in hostile_lifecycle_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_lifecycle_ledger_csv(rows)

        hostile_roll_rows = (
            (),
            (replace(roll, old_symbol="ESM9"),),
            (replace(roll, new_symbol="ESU9"),),
            (replace(roll, provider_roll_date=datetime(2019, 6, 16, tzinfo=timezone.utc)),),
            (replace(roll, completed_roll_date=datetime(2019, 6, 17, tzinfo=timezone.utc)),),
            (replace(roll, completed_roll_date=date(2019, 6, 15)),),
            (replace(roll, source_label=""),),
            (replace(roll, source_sha256=""),),
            (replace(roll, source_sha256="Z" * 64),),
            (replace(roll, status="PROVISIONAL"),),
        )
        for rows in hostile_roll_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_roll_semantics_ledger_csv(rows)

    def test_s09_mes_strategy_input_evidence_completion_renders_runtime_risk_ledgers(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceCompletionAnnualRiskRow,
            S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow,
            render_s09_mes_strategy_input_evidence_completion_annual_risk_ledger_csv,
            render_s09_mes_strategy_input_evidence_completion_daily_price_risk_ledger_csv,
        )

        annual = S09MESStrategyInputEvidenceCompletionAnnualRiskRow(
            completed_trading_date=date(2020, 3, 2),
            long_run_annual_risk=0.20,
            current_ewma32_annual_risk=0.10,
            annual_percentage_risk=0.13,
            source_label="LOCKED_MES_ANNUAL_RISK_RUNTIME_SOURCE",
            source_sha256="C" * 64,
            status="LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE",
        )
        daily = S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow(
            completed_trading_date=date(2020, 3, 2),
            current_price=3000.0,
            annual_percentage_risk=0.13,
            daily_price_risk_currency=24.375,
            source_label="LOCKED_MES_DAILY_PRICE_RISK_SOURCE",
            source_sha256="D" * 64,
            status="LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE",
        )

        annual_csv = render_s09_mes_strategy_input_evidence_completion_annual_risk_ledger_csv((annual,))
        daily_csv = render_s09_mes_strategy_input_evidence_completion_daily_price_risk_ledger_csv((daily,))

        self.assertEqual(
            annual_csv.splitlines()[0],
            "completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_label,source_sha256,status",
        )
        self.assertIn("2020-03-02,0.2,0.1,0.13,LOCKED_MES_ANNUAL_RISK_RUNTIME_SOURCE", annual_csv)
        self.assertEqual(
            daily_csv.splitlines()[0],
            "completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,source_label,source_sha256,status",
        )
        self.assertIn("2020-03-02,3000.0,0.13,24.375,LOCKED_MES_DAILY_PRICE_RISK_SOURCE", daily_csv)

        hostile_annual_rows = (
            (),
            (replace(annual, completed_trading_date=datetime(2020, 3, 2, tzinfo=timezone.utc)),),
            (replace(annual, long_run_annual_risk=0.0),),
            (replace(annual, current_ewma32_annual_risk=-0.01),),
            (replace(annual, annual_percentage_risk=0.14),),
            (replace(annual, source_label=""),),
            (replace(annual, source_sha256=""),),
            (replace(annual, source_sha256="Z" * 64),),
            (replace(annual, status="PROVISIONAL"),),
        )
        for rows in hostile_annual_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_annual_risk_ledger_csv(rows)

        hostile_daily_rows = (
            (),
            (replace(daily, completed_trading_date=datetime(2020, 3, 2, tzinfo=timezone.utc)),),
            (replace(daily, current_price=0.0),),
            (replace(daily, annual_percentage_risk=-0.01),),
            (replace(daily, daily_price_risk_currency=24.0),),
            (replace(daily, source_label=""),),
            (replace(daily, source_sha256=""),),
            (replace(daily, source_sha256="Z" * 64),),
            (replace(daily, status="PROVISIONAL"),),
        )
        for rows in hostile_daily_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_daily_price_risk_ledger_csv(rows)

    def test_s09_mes_strategy_input_evidence_completion_renders_cost_speed_fdm_and_hash_ledgers(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceCompletionCostValueRow,
            S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow,
            S09MESStrategyInputEvidenceCompletionHashManifestEntry,
            S09MESStrategyInputEvidenceCompletionRiskAdjustedCostRow,
            S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow,
            render_s09_mes_strategy_input_evidence_completion_cost_value_ledger_csv,
            render_s09_mes_strategy_input_evidence_completion_eligible_speed_set_fdm_ledger_csv,
            render_s09_mes_strategy_input_evidence_completion_hash_manifest,
            render_s09_mes_strategy_input_evidence_completion_risk_adjusted_cost_ledger_csv,
            render_s09_mes_strategy_input_evidence_completion_speed_eligibility_ledger_csv,
        )

        cost_rows = (
            S09MESStrategyInputEvidenceCompletionCostValueRow(
                completed_trading_date=date(2020, 3, 2),
                component_name="exchange_fee",
                amount_currency=0.20,
                currency="USD",
                charge_timing="PER_SIDE",
                effective_start=date(2019, 5, 5),
                effective_end=date(2020, 4, 5),
                source_label="LOCKED_HISTORICAL_MES_EXCHANGE_FEE_SOURCE",
                source_sha256="E" * 64,
                status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
            ),
            S09MESStrategyInputEvidenceCompletionCostValueRow(
                completed_trading_date=date(2020, 3, 2),
                component_name="clearing_regulatory_fee",
                amount_currency=0.04,
                currency="USD",
                charge_timing="PER_SIDE",
                effective_start=date(2019, 5, 5),
                effective_end=date(2020, 4, 5),
                source_label="LOCKED_HISTORICAL_MES_CLEARING_REGULATORY_SOURCE",
                source_sha256="F" * 64,
                status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
            ),
            S09MESStrategyInputEvidenceCompletionCostValueRow(
                completed_trading_date=date(2020, 3, 2),
                component_name="broker_commission",
                amount_currency=0.25,
                currency="USD",
                charge_timing="PER_SIDE",
                effective_start=date(2019, 5, 5),
                effective_end=date(2020, 4, 5),
                source_label="LOCKED_HISTORICAL_MES_BROKER_COMMISSION_SOURCE",
                source_sha256="1" * 64,
                status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
            ),
            S09MESStrategyInputEvidenceCompletionCostValueRow(
                completed_trading_date=date(2020, 3, 2),
                component_name="spread_slippage",
                amount_currency=1.25,
                currency="USD",
                charge_timing="ROUND_TURN",
                effective_start=date(2019, 5, 5),
                effective_end=date(2020, 4, 5),
                source_label="LOCKED_HISTORICAL_MES_SPREAD_SLIPPAGE_POLICY",
                source_sha256="2" * 64,
                status="LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE",
            ),
        )
        risk_adjusted = S09MESStrategyInputEvidenceCompletionRiskAdjustedCostRow(
            completed_trading_date=date(2020, 3, 2),
            total_cost_per_trade_currency=2.0,
            daily_price_risk_currency=40.0,
            risk_adjusted_cost_per_trade_sr=0.000625,
            source_label="LOCKED_MES_RISK_ADJUSTED_COST_SOURCE",
            source_sha256="3" * 64,
            status="LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE",
        )
        speed_rows = (
            S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(2, 98.5, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "4" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
            S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(4, 50.2, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "5" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
            S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(8, 25.4, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "6" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
            S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(16, 13.2, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "7" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
            S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(32, 7.6, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "8" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
            S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(64, 5.2, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "9" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
        )
        fdm = S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow(
            eligible_spans=(2, 4, 8, 16, 32, 64),
            table36_fdm=1.26,
            source_label="LOCKED_TABLE_36_FDM_SOURCE",
            source_sha256="A" * 64,
            status="LOCKED_SOURCE_NATIVE_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM",
        )

        cost_csv = render_s09_mes_strategy_input_evidence_completion_cost_value_ledger_csv(cost_rows)
        risk_adjusted_csv = render_s09_mes_strategy_input_evidence_completion_risk_adjusted_cost_ledger_csv((risk_adjusted,))
        speed_csv = render_s09_mes_strategy_input_evidence_completion_speed_eligibility_ledger_csv(speed_rows)
        fdm_csv = render_s09_mes_strategy_input_evidence_completion_eligible_speed_set_fdm_ledger_csv((fdm,))

        self.assertEqual(
            cost_csv.splitlines()[0],
            "completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status",
        )
        self.assertIn("2020-03-02,exchange_fee,0.2,USD,PER_SIDE,2019-05-05,2020-04-05", cost_csv)
        self.assertIn("2020-03-02,2.0,40.0,0.000625,LOCKED_MES_RISK_ADJUSTED_COST_SOURCE", risk_adjusted_csv)
        self.assertIn("2,98.5,0.001,0.15,True,LOCKED_MES_SPEED_SOURCE", speed_csv)
        self.assertEqual(
            fdm_csv,
            (
                "eligible_spans,table36_fdm,source_label,source_sha256,status\r\n"
                f"2|4|8|16|32|64,1.26,LOCKED_TABLE_36_FDM_SOURCE,{'A' * 64},"
                "LOCKED_SOURCE_NATIVE_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM\r\n"
            ),
        )

        manifest = render_s09_mes_strategy_input_evidence_completion_hash_manifest(
            (
                S09MESStrategyInputEvidenceCompletionHashManifestEntry(
                    relative_path="docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_COST_VALUE_ledger.csv",
                    artifact_text=cost_csv,
                ),
                S09MESStrategyInputEvidenceCompletionHashManifestEntry(
                    relative_path="docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/speed/20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv",
                    artifact_text=fdm_csv,
                ),
            )
        )
        self.assertIn("20260603_S09_MES_COST_VALUE_ledger.csv", manifest)
        self.assertIn("20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv", manifest)

        hostile_cost_sets = (
            (),
            cost_rows[:3],
            (cost_rows[1], cost_rows[0], *cost_rows[2:]),
            (replace(cost_rows[0], completed_trading_date=datetime(2020, 3, 2, tzinfo=timezone.utc)), *cost_rows[1:]),
            (replace(cost_rows[0], component_name="current_fee_default"), *cost_rows[1:]),
            (replace(cost_rows[0], amount_currency=-0.01), *cost_rows[1:]),
            (replace(cost_rows[0], currency="EUR"), *cost_rows[1:]),
            (replace(cost_rows[0], charge_timing="PER_CONTRACT"), *cost_rows[1:]),
            (replace(cost_rows[0], effective_start=date(2020, 3, 3)), *cost_rows[1:]),
            (replace(cost_rows[0], effective_end=date(2020, 3, 1)), *cost_rows[1:]),
            (replace(cost_rows[0], source_label=""), *cost_rows[1:]),
            (replace(cost_rows[0], source_sha256="Z" * 64), *cost_rows[1:]),
            (replace(cost_rows[0], status="PROVISIONAL"), *cost_rows[1:]),
        )
        for rows in hostile_cost_sets:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_cost_value_ledger_csv(rows)

        hostile_speed_sets = (
            (),
            speed_rows[:5],
            (speed_rows[1], speed_rows[0], *speed_rows[2:]),
            (replace(speed_rows[0], span=3), *speed_rows[1:]),
            (replace(speed_rows[0], turnover=99.0), *speed_rows[1:]),
            (replace(speed_rows[0], risk_adjusted_cost_per_trade_sr=0.0), *speed_rows[1:]),
            (replace(speed_rows[0], threshold_sr=0.2), *speed_rows[1:]),
            (replace(speed_rows[0], eligible=False), *speed_rows[1:]),
            (replace(speed_rows[0], source_label=""), *speed_rows[1:]),
            (replace(speed_rows[0], source_sha256="Z" * 64), *speed_rows[1:]),
            (replace(speed_rows[0], status="ASSUMED_ALL_SIX_SPEEDS"), *speed_rows[1:]),
        )
        for rows in hostile_speed_sets:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_speed_eligibility_ledger_csv(rows)

        hostile_risk_adjusted_rows = (
            (),
            (replace(risk_adjusted, completed_trading_date=datetime(2020, 3, 2, tzinfo=timezone.utc)),),
            (replace(risk_adjusted, total_cost_per_trade_currency=0.0),),
            (replace(risk_adjusted, daily_price_risk_currency=0.0),),
            (replace(risk_adjusted, risk_adjusted_cost_per_trade_sr=0.06),),
            (replace(risk_adjusted, source_label=""),),
            (replace(risk_adjusted, source_sha256="Z" * 64),),
            (replace(risk_adjusted, status="PROVISIONAL"),),
        )
        for rows in hostile_risk_adjusted_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_risk_adjusted_cost_ledger_csv(rows)

        hostile_fdm_rows = (
            (),
            (replace(fdm, eligible_spans=(2, 4, 8, 16, 32)),),
            (replace(fdm, table36_fdm=1.19),),
            (replace(fdm, source_label=""),),
            (replace(fdm, source_sha256="Z" * 64),),
            (replace(fdm, status="PROVISIONAL"),),
        )
        for rows in hostile_fdm_rows:
            with self.subTest(rows=rows):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_eligible_speed_set_fdm_ledger_csv(rows)

        hostile_manifest_entries = (
            (),
            (
                S09MESStrategyInputEvidenceCompletionHashManifestEntry(
                    relative_path="C:/tmp/out.csv",
                    artifact_text=cost_csv,
                ),
            ),
            (
                S09MESStrategyInputEvidenceCompletionHashManifestEntry(
                    relative_path="docs/researchops/s09/mes_strategy_input_evidence_completion/2022-01-03_2023-12-29/cost/out.csv",
                    artifact_text=cost_csv,
                ),
            ),
            (
                S09MESStrategyInputEvidenceCompletionHashManifestEntry(
                    relative_path="docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/hashes/out.txt",
                    artifact_text=cost_csv,
                ),
            ),
        )
        for entries in hostile_manifest_entries:
            with self.subTest(entries=entries):
                with self.assertRaises(CarverBlocked):
                    render_s09_mes_strategy_input_evidence_completion_hash_manifest(entries)

    def test_s09_mes_strategy_input_evidence_completion_builds_locked_in_memory_bundle_from_supplied_rows(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceCompletionAnnualRiskRow,
            S09MESStrategyInputEvidenceCompletionCostValueRow,
            S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow,
            S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow,
            S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow,
            S09MESStrategyInputEvidenceCompletionLockedBundleRequest,
            S09MESStrategyInputEvidenceCompletionRiskAdjustedCostRow,
            S09MESStrategyInputEvidenceCompletionRollSemanticsRow,
            S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow,
            build_s09_mes_strategy_input_evidence_completion_locked_artifact_bundle,
        )

        request = S09MESStrategyInputEvidenceCompletionLockedBundleRequest(
            lifecycle_rows=(
                S09MESStrategyInputEvidenceCompletionLifecycleEvidenceRow("MESM9", date(2019, 5, 6), date(2019, 6, 20), date(2019, 6, 21), "LOCKED_CME_MES_LIFECYCLE_SOURCE", "A" * 64, "LOCKED_SOURCE_NATIVE_LIFECYCLE_EVIDENCE"),
            ),
            roll_semantics_rows=(
                S09MESStrategyInputEvidenceCompletionRollSemanticsRow("MESM9", "MESU9", date(2019, 6, 16), date(2019, 6, 17), "LOCKED_CME_GLOBEX_COMPLETED_BAR_CALENDAR", "B" * 64, "LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS"),
            ),
            annual_risk_rows=(
                S09MESStrategyInputEvidenceCompletionAnnualRiskRow(date(2020, 3, 2), 0.20, 0.10, 0.13, "LOCKED_MES_ANNUAL_RISK_RUNTIME_SOURCE", "C" * 64, "LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE"),
            ),
            daily_price_risk_rows=(
                S09MESStrategyInputEvidenceCompletionDailyPriceRiskRow(date(2020, 3, 2), 3000.0, 0.13, 24.375, "LOCKED_MES_DAILY_PRICE_RISK_SOURCE", "D" * 64, "LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE"),
            ),
            cost_value_rows=(
                S09MESStrategyInputEvidenceCompletionCostValueRow(date(2020, 3, 2), "exchange_fee", 0.20, "USD", "PER_SIDE", date(2019, 5, 5), date(2020, 4, 5), "LOCKED_HISTORICAL_MES_EXCHANGE_FEE_SOURCE", "E" * 64, "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE"),
                S09MESStrategyInputEvidenceCompletionCostValueRow(date(2020, 3, 2), "clearing_regulatory_fee", 0.04, "USD", "PER_SIDE", date(2019, 5, 5), date(2020, 4, 5), "LOCKED_HISTORICAL_MES_CLEARING_REGULATORY_SOURCE", "F" * 64, "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE"),
                S09MESStrategyInputEvidenceCompletionCostValueRow(date(2020, 3, 2), "broker_commission", 0.25, "USD", "PER_SIDE", date(2019, 5, 5), date(2020, 4, 5), "LOCKED_HISTORICAL_MES_BROKER_COMMISSION_SOURCE", "1" * 64, "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE"),
                S09MESStrategyInputEvidenceCompletionCostValueRow(date(2020, 3, 2), "spread_slippage", 1.25, "USD", "ROUND_TURN", date(2019, 5, 5), date(2020, 4, 5), "LOCKED_HISTORICAL_MES_SPREAD_SLIPPAGE_POLICY", "2" * 64, "LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE"),
            ),
            risk_adjusted_cost_rows=(
                S09MESStrategyInputEvidenceCompletionRiskAdjustedCostRow(date(2020, 3, 2), 2.0, 40.0, 0.000625, "LOCKED_MES_RISK_ADJUSTED_COST_SOURCE", "3" * 64, "LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE"),
            ),
            speed_eligibility_rows=(
                S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(2, 98.5, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "4" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
                S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(4, 50.2, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "5" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
                S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(8, 25.4, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "6" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
                S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(16, 13.2, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "7" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
                S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(32, 7.6, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "8" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
                S09MESStrategyInputEvidenceCompletionSpeedEligibilityRow(64, 5.2, 0.001, 0.15, True, "LOCKED_MES_SPEED_SOURCE", "9" * 64, "LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE"),
            ),
            eligible_speed_set_fdm_rows=(
                S09MESStrategyInputEvidenceCompletionEligibleSpeedSetFDMRow((2, 4, 8, 16, 32, 64), 1.26, "LOCKED_TABLE_36_FDM_SOURCE", "A" * 64, "LOCKED_SOURCE_NATIVE_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM"),
            ),
        )

        bundle = build_s09_mes_strategy_input_evidence_completion_locked_artifact_bundle(request)
        text = "\n".join(bundle) + "\n" + "\n".join(bundle.values())

        self.assertEqual(len(bundle), 12)
        status = json.loads(bundle["docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json"])
        self.assertEqual(status["status"], "LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION")
        self.assertEqual(status["remaining_evidence_count"], 0)
        self.assertEqual(status["strategy_input_readiness_status"], "S09_MES_STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_GATE")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["market_row_parsing"], "NO")
        self.assertEqual(status["forecast_computation"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertIn("official_lifecycle_evidence,LOCKED_SOURCE_NATIVE_EVIDENCE,LOCKED_SOURCE_NATIVE_EVIDENCE", text)
        self.assertIn("MESM9,2019-05-06,2019-06-20,2019-06-21", text)
        self.assertIn("2|4|8|16|32|64,1.26", text)
        self.assertNotIn("FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_NOT_LOCKED", text)
        self.assertNotIn("2022-01-03_2023-12-29", text)
        self.assertNotIn("READY_FOR_BACKTEST", text)
        self.assertNotIn("READY_FOR_LOCKBOX", text)
        self.assertNotIn("TEST/VALIDATION/LOCKBOX", text)
        hashes = bundle["docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/hashes/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt"]
        self.assertIn("20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv", hashes)
        self.assertNotIn("/hashes/", hashes)

        hostile_requests = (
            replace(request, lifecycle_rows=()),
            replace(request, cost_value_rows=request.cost_value_rows[:3]),
            replace(request, speed_eligibility_rows=request.speed_eligibility_rows[:5]),
            replace(request, eligible_speed_set_fdm_rows=()),
        )
        for hostile in hostile_requests:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    build_s09_mes_strategy_input_evidence_completion_locked_artifact_bundle(hostile)

    def test_s09_mes_strategy_input_evidence_completion_builds_readiness_handoff_without_backtest_authorization(self) -> None:
        from dataclasses import replace  # noqa: PLC0415

        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest,
            build_s09_mes_strategy_input_evidence_completion_readiness_handoff_bundle,
        )

        request = S09MESStrategyInputEvidenceCompletionReadinessHandoffRequest(
            evidence_completion_status="LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION",
            strategy_input_readiness_status="S09_MES_STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_GATE",
            remaining_evidence_count=0,
            next_gate="S09_MES_STRATEGY_INPUT_READINESS_GATE",
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            machinery_development_slice="2019-05-05 through 2020-04-05",
            databento_api_access="NO",
            market_row_parsing="NO",
            forecast_computation="NO",
            diagnostics_run="NO",
            backtests_run="NO",
            test_validation_lockbox_forward_access="NO",
        )

        bundle = build_s09_mes_strategy_input_evidence_completion_readiness_handoff_bundle(request)
        self.assertEqual(
            tuple(bundle),
            (
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/handoff/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_readiness_handoff.json",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/handoff/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_readiness_handoff.md",
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/handoff/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_readiness_handoff_sha256.txt",
            ),
        )
        status = json.loads(next(iter(bundle.values())))
        text = "\n".join(bundle) + "\n" + "\n".join(bundle.values())

        self.assertEqual(status["next_gate"], "S09_MES_STRATEGY_INPUT_READINESS_GATE")
        self.assertEqual(status["remaining_evidence_count"], 0)
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertIn("evidence locked; readiness gate next", text)
        self.assertIn("does not authorize Development/Reconciliation backtesting", text)
        self.assertNotIn("READY_FOR_BACKTEST", text)
        self.assertNotIn("READY_FOR_LOCKBOX", text)
        self.assertNotIn("2022-01-03_2023-12-29", text)

        hostile_requests = (
            replace(request, evidence_completion_status="FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY"),
            replace(request, strategy_input_readiness_status="S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY"),
            replace(request, remaining_evidence_count=1),
            replace(request, next_gate="S09_MES_DEV_RECON_BACKTEST_GATE"),
            replace(request, lane_class="CFD_ADAPTER"),
            replace(request, root="ES"),
            replace(request, databento_api_access="YES"),
            replace(request, market_row_parsing="YES"),
            replace(request, forecast_computation="YES"),
            replace(request, diagnostics_run="YES"),
            replace(request, backtests_run="YES"),
            replace(request, test_validation_lockbox_forward_access="YES"),
        )
        for hostile in hostile_requests:
            with self.subTest(hostile=hostile):
                with self.assertRaises(CarverBlocked):
                    build_s09_mes_strategy_input_evidence_completion_readiness_handoff_bundle(hostile)

    def test_s09_mes_strategy_input_evidence_completion_plan_is_process_safe(self) -> None:
        plan_path = (
            ROOT
            / "docs"
            / "superpowers"
            / "plans"
            / "2026-06-03-s09-mes-strategy-input-evidence-completion.md"
        )
        text = plan_path.read_text(encoding="utf-8")

        self.assertIn("# S09 MES Strategy Input Evidence Completion Implementation Plan", text)
        self.assertIn("S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("2019-05-05 through 2020-04-05", text)
        self.assertIn("oldest minimum machinery-development slice only", text)
        self.assertIn("oldest authorized completed source-native data first", text)
        self.assertIn("carver_s09_mes_strategy_input_evidence_completion.py", text)
        self.assertIn("build_s09_mes_strategy_input_evidence_completion_artifact_bundle", text)
        self.assertIn("official_lifecycle_evidence", text)
        self.assertIn("roll_trading_day_semantics", text)
        self.assertIn("annual_risk_runtime_values", text)
        self.assertIn("historical_mes_cost_values", text)
        self.assertIn("risk_adjusted_cost_values", text)
        self.assertIn("speed_eligibility_values", text)
        self.assertIn("table36_fdm_row", text)
        self.assertIn("hash_bound_provenance", text)
        self.assertIn("No Databento API access unless explicitly restated by the operator", text)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", text)
        self.assertIn("Git staging, commit, push, PR, and remote operations require separate explicit operator authorization", text)
        self.assertNotIn("2022-01-03_2023-12-29", text)
        for placeholder in ("TBD", "TODO", "implement later"):
            self.assertNotIn(placeholder, text)

    def test_s09_mes_strategy_input_evidence_completion_writer_materializes_fail_closed_packet_under_explicit_call(self) -> None:
        from tools.databento.carver_s09_mes_strategy_input_evidence_completion import (  # noqa: PLC0415
            build_s09_mes_strategy_input_evidence_completion_artifact_bundle,
            write_s09_mes_strategy_input_evidence_completion_artifacts,
        )

        bundle = build_s09_mes_strategy_input_evidence_completion_artifact_bundle()
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(CarverBlocked):
                write_s09_mes_strategy_input_evidence_completion_artifacts(
                    execution_authorized=False,
                    bundle=bundle,
                    root=Path(tmpdir),
                )
            self.assertFalse((Path(tmpdir) / "docs").exists())

            written = write_s09_mes_strategy_input_evidence_completion_artifacts(
                execution_authorized=True,
                bundle=bundle,
                root=Path(tmpdir),
            )

            relative_written = tuple(path.relative_to(Path(tmpdir)).as_posix() for path in written)
            self.assertIn(
                "docs/process/CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_RESULT_2026-06-03.md",
                relative_written,
            )
            self.assertIn(
                "docs/process/CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_LOCAL_HOSTILE_AUDIT_2026-06-03.md",
                relative_written,
            )
            self.assertIn(
                "docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/hashes/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt",
                relative_written,
            )

            status_path = (
                Path(tmpdir)
                / "docs"
                / "researchops"
                / "s09"
                / "mes_strategy_input_evidence_completion"
                / "2019-05-05_2020-04-05"
                / "status"
                / "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json"
            )
            hashes_path = (
                Path(tmpdir)
                / "docs"
                / "researchops"
                / "s09"
                / "mes_strategy_input_evidence_completion"
                / "2019-05-05_2020-04-05"
                / "hashes"
                / "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt"
            )
            result_path = Path(tmpdir) / "docs" / "process" / "CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_RESULT_2026-06-03.md"
            audit_path = Path(tmpdir) / "docs" / "process" / "CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_LOCAL_HOSTILE_AUDIT_2026-06-03.md"

            status = json.loads(status_path.read_text(encoding="utf-8"))
            result = result_path.read_text(encoding="utf-8")
            audit = audit_path.read_text(encoding="utf-8")
            hashes = hashes_path.read_text(encoding="utf-8")

            self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY")
            self.assertIn("S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE", result)
            self.assertIn("header-only fail-closed ledgers", result)
            self.assertIn("LOCAL_HOSTILE_AUDIT_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_FAIL_CLOSED_NO_BACKTEST", audit)
            self.assertIn("no Databento API access", audit)
            self.assertIn("no market-row parsing", audit)
            self.assertIn("no backtests", audit)
            self.assertIn("no TEST", audit)
            self.assertIn("no VALIDATION", audit)
            self.assertIn("no Lockbox", audit)
            self.assertIn("no Forward", audit)
            self.assertIn("no Git staging", audit)
            self.assertNotIn("2022-01-03_2023-12-29", result + audit + hashes)
            self.assertNotIn("READY_FOR_BACKTEST", result + audit + hashes)
            self.assertNotIn("READY_FOR_LOCKBOX", result + audit + hashes)

            for line in hashes.splitlines():
                if not line.strip():
                    continue
                expected_hash, relative_path = line.split("  ", 1)
                self.assertNotIn("/hashes/", relative_path)
                actual_hash = hashlib.sha256((Path(tmpdir) / relative_path).read_bytes()).hexdigest().upper()
                self.assertEqual(actual_hash, expected_hash)

    def test_s09_mes_strategy_input_evidence_completion_written_packet_is_hash_bound_locked_no_readiness(self) -> None:
        output_root = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_strategy_input_evidence_completion"
            / "2019-05-05_2020-04-05"
        )
        status_path = output_root / "status" / "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json"
        hashes_path = output_root / "hashes" / "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt"
        result_path = ROOT / "docs" / "process" / "CARVER_S09_MES_HASH_BOUND_PROVENANCE_LOCK_RESULT_2026-06-03.md"
        audit_path = ROOT / "docs" / "process" / "CARVER_S09_MES_HASH_BOUND_PROVENANCE_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md"

        expected_files = (
            output_root / "evidence" / "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_required_evidence_ledger.csv",
            output_root / "lifecycle" / "20260603_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv",
            output_root / "roll" / "20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv",
            output_root / "risk" / "20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv",
            output_root / "risk" / "20260603_S09_MES_DAILY_PRICE_RISK_ledger.csv",
            output_root / "cost" / "20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv",
            output_root / "cost" / "20260603_S09_MES_RISK_ADJUSTED_COST_ledger.csv",
            output_root / "speed" / "20260603_S09_MES_SPEED_ELIGIBILITY_ledger.csv",
            output_root / "speed" / "20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv",
            status_path,
            output_root / "provenance" / "20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_provenance.md",
            result_path,
            audit_path,
            hashes_path,
        )
        for path in expected_files:
            self.assertTrue(path.exists(), path)

        status = json.loads(status_path.read_text(encoding="utf-8"))
        result = result_path.read_text(encoding="utf-8")
        audit = audit_path.read_text(encoding="utf-8")
        hashes = hashes_path.read_text(encoding="utf-8")
        combined = result + audit + hashes + "\n".join(path.read_text(encoding="utf-8") for path in expected_files if path != hashes_path)

        self.assertEqual(status["status"], "LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION")
        self.assertEqual(status["remaining_evidence_count"], 0)
        self.assertEqual(status["hash_bound_provenance_status"], "LOCKED_SOURCE_NATIVE_HASH_BOUND_PROVENANCE")
        self.assertEqual(status["strategy_input_readiness_status"], "S09_MES_STRATEGY_INPUT_EVIDENCE_LOCKED_AWAITING_READINESS_GATE")
        self.assertEqual(status["next_gate"], "S09_MES_STRATEGY_INPUT_READINESS_GATE")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["market_row_parsing"], "NO")
        self.assertEqual(status["forecast_computation"], "NO")
        self.assertEqual(status["diagnostics_run"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertIn("LOCAL_HOSTILE_AUDIT_HASH_BOUND_PROVENANCE_LOCKED_NO_READINESS_NO_BACKTEST", audit)
        self.assertIn("remaining_evidence_count is 0", audit)
        self.assertIn("hash_bound_provenance,LOCKED_SOURCE_NATIVE_EVIDENCE,LOCKED_SOURCE_NATIVE_EVIDENCE", combined)
        self.assertIn("20260603_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv", hashes)
        self.assertNotIn("2022-01-03_2023-12-29", combined)
        self.assertNotIn("READY_FOR_BACKTEST", combined)
        self.assertNotIn("READY_FOR_LOCKBOX", combined)

        for line in hashes.splitlines():
            if not line.strip():
                continue
            expected_hash, relative_path = line.split("  ", 1)
            self.assertNotIn("/hashes/", relative_path)
            actual_hash = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest().upper()
            self.assertEqual(actual_hash, expected_hash)

    def test_s09_mes_machinery_dev_minimum_slice_download_requires_authorization(self) -> None:
        from tools.databento.carver_s09_mes_machinery_dev_minimum_slice_download import (  # noqa: PLC0415
            S09MESMachineryDevMinimumSliceDownloadConfig,
            run_s09_mes_machinery_dev_minimum_slice_download,
        )

        config = S09MESMachineryDevMinimumSliceDownloadConfig(
            execution_authorized=False,
            lane_class="SOURCE_NATIVE_FUTURES",
            root="MES",
            row_id="APPENDIX_C_174_006",
            window_start="2019-05-05",
            window_end="2020-04-05",
        )

        with self.assertRaises(CarverBlocked):
            run_s09_mes_machinery_dev_minimum_slice_download(config)

    def test_s09_mes_machinery_dev_minimum_slice_download_rejects_non_oldest_or_two_year_window(self) -> None:
        from tools.databento.carver_s09_mes_machinery_dev_minimum_slice_download import (  # noqa: PLC0415
            S09MESMachineryDevMinimumSliceDownloadConfig,
            run_s09_mes_machinery_dev_minimum_slice_download,
        )

        hostile_configs = (
            S09MESMachineryDevMinimumSliceDownloadConfig(
                execution_authorized=True,
                lane_class="CFD_ADAPTER",
                root="MES",
                row_id="APPENDIX_C_174_006",
                window_start="2019-05-05",
                window_end="2020-04-05",
            ),
            S09MESMachineryDevMinimumSliceDownloadConfig(
                execution_authorized=True,
                lane_class="SOURCE_NATIVE_FUTURES",
                root="ES",
                row_id="APPENDIX_C_174_006",
                window_start="2019-05-05",
                window_end="2020-04-05",
            ),
            S09MESMachineryDevMinimumSliceDownloadConfig(
                execution_authorized=True,
                lane_class="SOURCE_NATIVE_FUTURES",
                root="MES",
                row_id="APPENDIX_C_174_006",
                window_start="2022-01-03",
                window_end="2023-12-29",
            ),
            S09MESMachineryDevMinimumSliceDownloadConfig(
                execution_authorized=True,
                lane_class="SOURCE_NATIVE_FUTURES",
                root="MES",
                row_id="APPENDIX_C_174_006",
                window_start="2019-05-05",
                window_end="2021-05-05",
            ),
        )

        for config in hostile_configs:
            with self.subTest(config=config):
                with self.assertRaises(CarverBlocked):
                    run_s09_mes_machinery_dev_minimum_slice_download(config)

    def test_s09_mes_roll_risk_cost_execution_packet_integrity_audit_is_hash_bound(self) -> None:
        status_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_date_normalization_runtime_risk_cost_execution"
            / "2022-01-03_2023-12-29"
            / "status"
            / "20260603_S09_MES_ROLL_RISK_COST_EXECUTION_status.json"
        )
        hashes_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_roll_date_normalization_runtime_risk_cost_execution"
            / "2022-01-03_2023-12-29"
            / "hashes"
            / "20260603_S09_MES_ROLL_RISK_COST_EXECUTION_sha256.txt"
        )
        audit_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_ROLL_RISK_COST_EXECUTION_PACKET_INTEGRITY_AUDIT_2026-06-03.md"
        )

        status = json.loads(status_path.read_text(encoding="utf-8"))
        hashes = hashes_path.read_text(encoding="utf-8")
        audit = audit_path.read_text(encoding="utf-8")

        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["new_provider_data_download"], "NO")
        self.assertEqual(status["market_row_parsing"], "NO")
        self.assertIn("HASH_BOUND_S09_MES_ROLL_RISK_COST_EXECUTION_PACKET_FAIL_CLOSED_NOT_STRATEGY_INPUT", audit)
        self.assertIn("FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY", audit)
        self.assertIn("header-only fail-closed ledgers", audit)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", audit)
        self.assertIn("20260603_S09_MES_ROLL_RISK_COST_EXECUTION_sha256.txt", audit)

        for line in hashes.splitlines():
            if not line.strip():
                continue
            expected_hash, relative_path = line.split("  ", 1)
            actual_hash = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest().upper()
            self.assertEqual(actual_hash, expected_hash)

    def test_s09_mes_pre_backtest_usable_history_after_warmup_discussion_is_locked(self) -> None:
        discussion_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_PRE_BACKTEST_USABLE_HISTORY_AFTER_WARMUP_DISCUSSION_2026-06-03.md"
        )
        text = discussion_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_PRE_BACKTEST_USABLE_HISTORY_AFTER_WARMUP_DISCUSSION_NOT_BACKTEST", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("MES", text)
        self.assertIn("current observed artifact window: 2022-01-03 through 2023-12-29", text)
        self.assertIn("not the default Development/Reconciliation backtest window", text)
        self.assertIn("Default Dev/Reconciliation selection must start from oldest authorized source-native data first", text)
        self.assertIn("Do not default to a convenient two-year window", text)
        self.assertIn("target_window_rows = 2065", text)
        self.assertIn("target_window_adjusted_rows = 619", text)
        self.assertIn("total_adjusted_rows = 929", text)
        self.assertIn("pre_target_context_rows = 310", text)
        self.assertIn("EWMAC64", text)
        self.assertIn("slow_span = 256", text)
        self.assertIn("minimum_completed_bars = 257", text)
        self.assertIn("619 usable target rows if pre-target context is authorized for warmup only", text)
        self.assertIn("approximately 362 usable target rows if warmup must be consumed inside the target window", text)
        self.assertIn("annual-risk warmup and first usable date remain not locked", text)
        self.assertIn("provider-date Sunday rows and exchange completed-bar normalization remain unresolved", text)
        self.assertIn("No Dev/Reconciliation backtest may run until a first_usable_date, warmup_rows_consumed, usable_rows_remaining, and warmup policy are locked", text)
        self.assertIn("no forecast computation", text)
        self.assertIn("no diagnostics", text)
        self.assertIn("no backtests", text)
        self.assertIn("no OOS", text)
        self.assertIn("no Lockbox", text)
        self.assertIn("no Forward", text)
        self.assertIn("no Git staging", text)

    def test_strategy_window_allocation_doctrine_rejects_fixed_two_year_dev_default(self) -> None:
        doctrine_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_STRATEGY_WINDOW_ALLOCATION_AND_SMALL_SLICE_CONSTRUCTION_DOCTRINE_2026-06-03.md"
        )
        text = doctrine_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_STRATEGY_WINDOW_ALLOCATION_SMALL_SLICE_CONSTRUCTION_DOCTRINE_NOT_BACKTEST", text)
        self.assertIn("Dev/Reconciliation is not a default two-year window", text)
        self.assertIn("Each strategy has a different expected trade count and statistical sample requirement", text)
        self.assertIn("TEST, VALIDATION, and Lockbox windows must be allocated per strategy", text)
        self.assertIn("window allocation must be based on expected trade count, bar frequency, warmup loss, and source-native data availability", text)
        self.assertIn("If data is needed only to construct the strategy, use the smallest source-native construction slice that satisfies the construction dependency", text)
        self.assertIn("Construction slices are not scored evidence windows", text)
        self.assertIn("Do not burn two years of data to construct a strategy when a smaller source-native slice is sufficient", text)
        self.assertIn("oldest authorized source-native data first", text)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", text)
        self.assertIn("This doctrine supersedes any old-lab fixed Dev-window relic", text)
        self.assertNotIn("default 2 year dev window", text.lower())

    def test_s09_mes_three_three_four_test_validation_lockbox_window_plan_is_locked(self) -> None:
        window_path = (
            ROOT
            / "docs"
            / "process"
            / "CARVER_S09_MES_TEST_VALIDATION_LOCKBOX_3_3_4_WINDOW_PLAN_2026-06-03.md"
        )
        text = window_path.read_text(encoding="utf-8")

        self.assertIn("PROCESS_ONLY_S09_MES_TEST_VALIDATION_LOCKBOX_3_3_4_WINDOW_PLAN_NOT_DATA_NOT_BACKTEST", text)
        self.assertIn("SOURCE_NATIVE_FUTURES", text)
        self.assertIn("APPENDIX_C_174_006", text)
        self.assertIn("MES", text)
        self.assertIn("machinery_development_slice: 2019-05-05 through 2020-04-05", text)
        self.assertIn("remaining_scored_pool_completed_dates: 1914", text)
        self.assertIn("split_ratio: 3:3:4", text)
        self.assertIn("TEST completed dates: 574", text)
        self.assertIn("TEST window: 2020-04-06 through 2022-02-08", text)
        self.assertIn("VALIDATION completed dates: 574", text)
        self.assertIn("VALIDATION window: 2022-02-09 through 2023-12-13", text)
        self.assertIn("LOCKBOX completed dates: 766", text)
        self.assertIn("LOCKBOX window: 2023-12-14 through 2026-05-29", text)
        self.assertIn("Lockbox access remains separately gated", text)
        self.assertIn("The Lockbox span is longer than two calendar years and therefore requires explicit operator authorization before any Lockbox diagnostic or backtest", text)
        self.assertIn("Stage data must be downloaded separately only when that stage is reached and authorized", text)
        self.assertIn("No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations", text)

    def test_s09_mes_machinery_dev_lineage_packet_preserves_no_forecast_boundary(self) -> None:
        status_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_machinery_dev_lineage"
            / "2019-05-05_2020-04-05"
            / "status"
            / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_status.json"
        )
        continuous_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_machinery_dev_lineage"
            / "2019-05-05_2020-04-05"
            / "continuous_series"
            / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_continuous_daily_mes_machinery_only.csv"
        )
        provenance_path = (
            ROOT
            / "docs"
            / "researchops"
            / "s09"
            / "mes_machinery_dev_lineage"
            / "2019-05-05_2020-04-05"
            / "provenance"
            / "20260603_S09_MES_MACHINERY_DEV_LINEAGE_provenance.md"
        )

        status = json.loads(status_path.read_text(encoding="utf-8"))
        continuous_text = continuous_path.read_text(encoding="utf-8")
        provenance = provenance_path.read_text(encoding="utf-8")

        self.assertEqual(status["status"], "FAIL_CLOSED_S09_MES_MACHINERY_DEV_LINEAGE_NOT_STRATEGY_INPUT")
        self.assertEqual(status["databento_api_access"], "NO")
        self.assertEqual(status["new_provider_data_download"], "NO")
        self.assertEqual(status["source_window"], "2019-05-05 through 2020-04-05")
        self.assertEqual(status["window_role"], "MINIMUM_OLDEST_MACHINERY_DEVELOPMENT_SLICE_NOT_SCORED_EVIDENCE")
        self.assertEqual(status["forecast_computation"], "NO")
        self.assertEqual(status["diagnostics_run"], "NO")
        self.assertEqual(status["backtests_run"], "NO")
        self.assertEqual(status["test_validation_lockbox_forward_access"], "NO")
        self.assertEqual(status["ewmac64_minimum_completed_bars"], 257)
        self.assertEqual(status["provider_condition_admission_status"], "LOCKED_NORMAL_PROVIDER_ROWS_ONLY")
        self.assertEqual(status["strategy_input_readiness_status"], "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY")
        self.assertIn("first_ewmac64_usable_completed_date", status)
        self.assertIn("lineage_status", continuous_text)
        self.assertNotIn("DEGRADED_OR_UNRESOLVED", continuous_text)
        self.assertIn("no S09 forecast computation", provenance)
        self.assertIn("no backtests", provenance)
        self.assertIn("not scored evidence", provenance)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import sys
import tempfile
import unittest
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.continuous import (  # noqa: E402
    ContinuousChainRequest,
    build_back_adjusted_continuous_chain,
)
from carver.spine.data_acquisition import (  # noqa: E402
    DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE,
    build_parts_1_3_daily_seed_manifest,
    build_zn_continuous_readiness_from_native_exports,
)
from carver.spine.daily_bars import CompletedDailyMarketBar  # noqa: E402
from carver.spine.m0 import (  # noqa: E402
    BackAdjustmentSpec,
    CompletedBar,
    CostSourceSpec,
    RollRuleSpec,
    SessionCalendarSpec,
    SourceRuleStatus,
    CarverBlocked,
)
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402


class ContinuousSyntheticTests(unittest.TestCase):
    def locked_rules(self):
        return (
            SessionCalendarSpec("ZN completed daily session calendar", SourceRuleStatus.LOCKED, "UTC"),
            RollRuleSpec("ZN manifest chain observed-last-date roll segmentation", SourceRuleStatus.LOCKED),
            BackAdjustmentSpec("ZN additive close-gap back-adjustment at overlapping roll date", SourceRuleStatus.LOCKED),
            CostSourceSpec("cost source not used for parser-only continuous readiness", SourceRuleStatus.LOCKED, "config/costs.json"),
        )

    def rule_set(self):
        from carver.spine.continuous import ContinuousContractRuleSet

        session, roll, back_adjustment, cost = self.locked_rules()
        return ContinuousContractRuleSet(session, roll, back_adjustment, cost)

    def bar(self, trade_date: str, contract_month: str, close: float) -> CompletedDailyMarketBar:
        return CompletedDailyMarketBar(
            completed_bar=CompletedBar(datetime.fromisoformat(trade_date).replace(tzinfo=timezone.utc)),
            contract=zn_contract(),
            contract_month=contract_month,
            open=close - 0.25,
            high=close + 0.50,
            low=close - 0.75,
            close=close,
            volume=1000,
        )

    def test_builds_additive_back_adjusted_chain_from_overlapping_contracts(self) -> None:
        request = ContinuousChainRequest(
            rules=self.rule_set(),
            contract_bars=(
                (self.bar("2026-01-01", "09-25", 100), self.bar("2026-01-02", "09-25", 102)),
                (
                    self.bar("2026-01-02", "12-25", 110),
                    self.bar("2026-01-03", "12-25", 115),
                    self.bar("2026-01-04", "12-25", 116),
                ),
                (self.bar("2026-01-04", "03-26", 130), self.bar("2026-01-05", "03-26", 131)),
            ),
            minimum_rows=5,
        )

        result = build_back_adjusted_continuous_chain(request)

        self.assertEqual([bar.timestamp.date().isoformat() for bar in result.adjusted_bars], [
            "2026-01-01",
            "2026-01-02",
            "2026-01-03",
            "2026-01-04",
            "2026-01-05",
        ])
        self.assertEqual([bar.close for bar in result.adjusted_bars], [100, 102, 107, 108, 109])
        self.assertEqual(result.roll_dates, ("2026-01-03", "2026-01-05"))
        self.assertTrue(result.ready)

    def test_chain_fails_closed_without_overlap_or_with_bad_contract_shape(self) -> None:
        missing_overlap = ContinuousChainRequest(
            rules=self.rule_set(),
            contract_bars=(
                (self.bar("2026-01-01", "09-25", 100), self.bar("2026-01-02", "09-25", 102)),
                (self.bar("2026-01-03", "12-25", 115),),
            ),
            minimum_rows=2,
        )
        with self.assertRaises(CarverBlocked):
            build_back_adjusted_continuous_chain(missing_overlap)

        mixed_code = CompletedDailyMarketBar(
            completed_bar=CompletedBar(datetime(2026, 1, 1, tzinfo=timezone.utc)),
            contract=mes_contract(),
            contract_month="09-25",
            open=100,
            high=101,
            low=99,
            close=100,
            volume=1,
        )
        with self.assertRaises(CarverBlocked):
            build_back_adjusted_continuous_chain(
                ContinuousChainRequest(
                    rules=self.rule_set(),
                    contract_bars=((self.bar("2026-01-01", "09-25", 100),), (mixed_code,)),
                    minimum_rows=2,
                )
            )

    def test_chain_fails_closed_on_unresolved_rules_ordering_grouping_and_duplicates(self) -> None:
        unresolved_session, roll, back_adjustment, cost = self.locked_rules()
        unresolved_rules = type(self.rule_set())(
            type(unresolved_session)("session calendar"),
            roll,
            back_adjustment,
            cost,
        )
        with self.assertRaises(CarverBlocked):
            build_back_adjusted_continuous_chain(
                ContinuousChainRequest(unresolved_rules, ((self.bar("2026-01-01", "09-25", 100),),), 1)
            )

        with self.assertRaises(CarverBlocked):
            build_back_adjusted_continuous_chain(
                ContinuousChainRequest(
                    self.rule_set(),
                    ((self.bar("2026-01-01", "12-25", 100),), (self.bar("2026-01-01", "09-25", 100),)),
                    1,
                )
            )

        with self.assertRaises(CarverBlocked):
            build_back_adjusted_continuous_chain(
                ContinuousChainRequest(
                    self.rule_set(),
                    ((self.bar("2026-01-01", "09-25", 100), self.bar("2026-01-02", "12-25", 101)),),
                    1,
                )
            )

        with self.assertRaises(CarverBlocked):
            build_back_adjusted_continuous_chain(
                ContinuousChainRequest(
                    self.rule_set(),
                    ((self.bar("2026-01-01", "09-25", 100), self.bar("2026-01-01", "09-25", 101)),),
                    1,
                )
            )

    def test_builds_readiness_from_manifest_exports_without_strategy_computation(self) -> None:
        manifest = build_parts_1_3_daily_seed_manifest()
        with tempfile.TemporaryDirectory():
            root = DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE / "_synthetic_continuous_test"
            try:
                for request in manifest.export_requests:
                    path = root / request.quarantine_relative_path
                    path.parent.mkdir(parents=True, exist_ok=True)
                    index = manifest.export_requests.index(request)
                    first_day = 20 + index
                    second_day = 21 + index
                    path.write_text(
                        f"202605{first_day:02d};109.96875;109.984375;109.625;109.828125;1159364\n"
                        f"202605{second_day:02d};109.859375;110.15625;109.8125;109.90625;491263\n",
                        encoding="utf-8",
                    )

                result = build_zn_continuous_readiness_from_native_exports(self.rule_set(), manifest, root)

                self.assertEqual(len(result.adjusted_bars), 5)
                self.assertFalse(result.ready)
                self.assertEqual(result.minimum_rows, 257)
            finally:
                if root.exists():
                    shutil.rmtree(root)


if __name__ == "__main__":
    unittest.main()

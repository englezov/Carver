from __future__ import annotations

import sys
import tempfile
import unittest
import shutil
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.data_acquisition import (  # noqa: E402
    DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE,
    NinjaTraderDataType,
    NinjaTraderInterval,
    NinjaTraderNativeDailyExportRequest,
    build_parts_1_3_daily_seed_manifest,
    load_parts_1_3_daily_seed_manifest_config,
    parse_native_ninjatrader_daily_export_file,
    parse_native_ninjatrader_daily_export_text,
    require_seed_manifest_config_matches_code,
)
from carver.spine.m0 import CarverBlocked, ContractSpec, LaneClass  # noqa: E402
from carver.spine.m3 import mes_contract, zn_contract  # noqa: E402


class DataAcquisitionSyntheticTests(unittest.TestCase):
    def zn_request(self) -> NinjaTraderNativeDailyExportRequest:
        return NinjaTraderNativeDailyExportRequest(
            zn_contract(),
            "06-26",
            "ZN JUN26",
            start_date="2025-05-29",
            end_date="2026-05-28",
        )

    def good_text(self) -> str:
        return (
            "20260526;109.96875;109.984375;109.625;109.828125;1159364\n"
            "20260527;109.859375;110.15625;109.8125;109.90625;491263\n"
            "20260528;109.875;110.234375;109.546875;110.046875;162271\n"
        )

    def test_builds_parts_1_3_seed_manifest_without_execution(self) -> None:
        manifest = build_parts_1_3_daily_seed_manifest()

        self.assertEqual(manifest.manifest_id, "CARVER_PARTS_1_3_DAILY_SEED_S09_ZN_CONTINUOUS_READINESS")
        self.assertEqual({root.root for root in manifest.roots}, {"MES", "ZN", "ZF", "QM", "ZC", "MGC"})
        self.assertEqual([(request.contract.code, request.contract_month) for request in manifest.export_requests], [
            ("ZN", "09-25"),
            ("ZN", "12-25"),
            ("ZN", "03-26"),
            ("ZN", "06-26"),
        ])
        self.assertEqual(manifest.minimum_continuous_rows, 257)
        for request in manifest.export_requests:
            self.assertEqual(request.interval, NinjaTraderInterval.DAY)
            self.assertEqual(request.data_type, NinjaTraderDataType.LAST)
            self.assertTrue(str(request.quarantine_relative_path).startswith("ZN"))

    def test_json_seed_manifest_matches_code_manifest(self) -> None:
        manifest = build_parts_1_3_daily_seed_manifest()
        payload = load_parts_1_3_daily_seed_manifest_config()

        self.assertEqual(payload["manifest_id"], manifest.manifest_id)
        self.assertEqual(payload["first_chain_requests"][-1]["native_file"], "ZN/ZN 06-26.Last.txt")

        drifted = copy.deepcopy(payload)
        drifted["first_chain_requests"][-1]["ninjatrader_symbol"] = "ZN 06-26"
        with self.assertRaises(CarverBlocked):
            require_seed_manifest_config_matches_code(drifted, manifest)

        duplicate_root = copy.deepcopy(payload)
        duplicate_root["roots"].append(copy.deepcopy(duplicate_root["roots"][-1]))
        with self.assertRaises(CarverBlocked):
            require_seed_manifest_config_matches_code(duplicate_root, manifest)

        non_dict_root = copy.deepcopy(payload)
        non_dict_root["roots"].append("ZN")
        with self.assertRaises(CarverBlocked):
            require_seed_manifest_config_matches_code(non_dict_root, manifest)

    def test_native_export_request_locks_symbol_dates_and_quarantine_path(self) -> None:
        request = self.zn_request()

        self.assertEqual(request.native_file_name, "ZN 06-26.Last.txt")
        self.assertEqual(request.quarantine_relative_path.as_posix(), "ZN/ZN 06-26.Last.txt")
        self.assertEqual(DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE, ROOT / "data" / "quarantine" / "ninjatrader" / "native_daily_exports")

        bad_symbol = NinjaTraderNativeDailyExportRequest(zn_contract(), "06-26", "ZN 06-26", "2025-05-29", "2026-05-28")
        with self.assertRaises(CarverBlocked):
            bad_symbol.validate()
        bad_dates = NinjaTraderNativeDailyExportRequest(zn_contract(), "06-26", "ZN JUN26", "2026-05-28", "2025-05-29")
        with self.assertRaises(CarverBlocked):
            bad_dates.validate()
        cfd_contract = ContractSpec("ZN", "CFD-ish", "BROKER", "USD", 1, LaneClass.CFD_ADAPTER)
        with self.assertRaises(CarverBlocked):
            NinjaTraderNativeDailyExportRequest(cfd_contract, "06-26", "ZN JUN26", "2025-05-29", "2026-05-28").validate()

    def test_parser_requires_manifest_declared_request(self) -> None:
        es_contract = ContractSpec("ES", "E-mini S&P 500 future", "CME", "USD", 50)
        es_request = NinjaTraderNativeDailyExportRequest(es_contract, "06-26", "ES JUN26", "2025-05-29", "2026-05-28")
        mes_request = NinjaTraderNativeDailyExportRequest(mes_contract(), "06-26", "MES JUN26", "2025-05-29", "2026-05-28")

        with self.assertRaises(CarverBlocked):
            parse_native_ninjatrader_daily_export_text(self.good_text(), es_request)
        with self.assertRaises(CarverBlocked):
            parse_native_ninjatrader_daily_export_text(self.good_text(), mes_request)

    def test_parses_native_semicolon_daily_export_as_completed_bars(self) -> None:
        bars = parse_native_ninjatrader_daily_export_text(self.good_text(), self.zn_request())

        self.assertEqual(len(bars), 3)
        self.assertEqual(bars[0].code, "ZN")
        self.assertEqual(bars[0].contract_month, "06-26")
        self.assertEqual(bars[0].timestamp.isoformat(), "2026-05-26T00:00:00+00:00")
        self.assertEqual(bars[-1].close, 110.046875)

    def test_native_export_parser_rejects_bad_rows(self) -> None:
        cases = [
            "",
            "20260526;109.9;110.0;109.6;109.8\n",
            "2026052x;109.9;110.0;109.6;109.8;1\n",
            "20250528;109.9;110.0;109.6;109.8;1\n",
            "20260526;109.9;109.0;109.6;109.8;1\n",
            "20260526;109.9;110.0;109.95;109.8;1\n",
            "20260526;NaN;110.0;109.6;109.8;1\n",
            "20260526;109.9;110.0;109.6;109.8;-1\n",
            "20260527;109.9;110.0;109.6;109.8;1\n20260526;109.9;110.0;109.6;109.8;1\n",
            "20260526;109.9;110.0;109.6;109.8;1\n20260526;109.9;110.0;109.6;109.8;1\n",
        ]
        for text in cases:
            with self.subTest(text=text):
                with self.assertRaises(CarverBlocked):
                    parse_native_ninjatrader_daily_export_text(text, self.zn_request())

    def test_native_export_file_must_stay_in_locked_carver_quarantine(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temp = Path(temporary_directory)
            root = DEFAULT_NATIVE_DAILY_EXPORT_QUARANTINE / "_synthetic_unit_test"
            try:
                export_dir = root / "ZN"
                export_dir.mkdir(parents=True, exist_ok=True)
                export_path = export_dir / "ZN 06-26.Last.txt"
                export_path.write_text(self.good_text(), encoding="utf-8")

                bars = parse_native_ninjatrader_daily_export_file(export_path, self.zn_request(), root)
                self.assertEqual(len(bars), 3)

                wrong_name = export_dir / "ZN JUN26.Last.txt"
                wrong_name.write_text(self.good_text(), encoding="utf-8")
                with self.assertRaises(CarverBlocked):
                    parse_native_ninjatrader_daily_export_file(wrong_name, self.zn_request(), root)

                outside_root = temp / "native_daily_exports"
                outside_root.mkdir()
                outside_file = outside_root / "ZN 06-26.Last.txt"
                outside_file.write_text(self.good_text(), encoding="utf-8")
                with self.assertRaises(CarverBlocked):
                    parse_native_ninjatrader_daily_export_file(outside_file, self.zn_request(), outside_root)
            finally:
                if root.exists():
                    shutil.rmtree(root)

    def test_manifest_rejects_duplicate_or_undeclared_roots(self) -> None:
        manifest = build_parts_1_3_daily_seed_manifest()
        duplicate_roots = type(manifest)(
            manifest.manifest_id,
            manifest.roots + manifest.roots[:1],
            manifest.export_requests,
            manifest.minimum_continuous_rows,
        )
        with self.assertRaises(CarverBlocked):
            duplicate_roots.validate()

        undeclared = type(manifest)(
            manifest.manifest_id,
            manifest.roots[:1],
            manifest.export_requests,
            manifest.minimum_continuous_rows,
        )
        with self.assertRaises(CarverBlocked):
            undeclared.validate()

        bad_mes_request = NinjaTraderNativeDailyExportRequest(mes_contract(), "06-26", "MES JUN26", "2025-05-29", "2026-05-28")
        duplicate_requests = type(manifest)(
            manifest.manifest_id,
            manifest.roots,
            manifest.export_requests + manifest.export_requests[:1] + (bad_mes_request,),
            manifest.minimum_continuous_rows,
        )
        with self.assertRaises(CarverBlocked):
            duplicate_requests.validate()


if __name__ == "__main__":
    unittest.main()

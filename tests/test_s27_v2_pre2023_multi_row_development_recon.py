from __future__ import annotations

import csv
import json
from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.pre2023_multi_row_development_recon_run import (
    NON_AUTHORIZATIONS,
    OUTPUT_RELATIVE_PATH,
    PACK_RELATIVE_PATH,
    _bundle_payload,
    run_pre2023_multi_row_development_recon,
)


PACK_ROOT = ROOT / PACK_RELATIVE_PATH
RUN_ROOT = ROOT / OUTPUT_RELATIVE_PATH


@pytest.fixture(scope="module")
def multi_row_bundle():
    return run_pre2023_multi_row_development_recon()


def _rows(root: Path, name: str) -> list[dict[str, str]]:
    with (root / name).open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _json(root: Path, name: str) -> dict[str, object]:
    return json.loads((root / name).read_text(encoding="ascii"))


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_bundle_payload(bundle)))


def test_multi_row_pack_declares_minimum_oldest_2022_slice():
    manifest = _json(PACK_ROOT, "S27_V2_PRE2023_MULTI_ROW_DECLARED_INPUT_PACK_MANIFEST.json")
    decisions = _rows(PACK_ROOT, "hourly_decision_completed_bar.csv")
    fills = _rows(PACK_ROOT, "hourly_fill_completed_bar.csv")
    marks = _rows(PACK_ROOT, "valuation_mark_completed_bar.csv")

    assert manifest["status"] == "LOCAL_PRE2023_MULTI_ROW_DEV_RECON_PACK_DECLARED_NOT_RESULT"
    assert manifest["selected_slice_rule"] == "MINIMUM_OLDEST_2022_MULTI_ROW_DEV_RECON_AFTER_WARMUPS_PRESERVE_2023_FOR_TEST"
    assert [row["completed_timestamp_utc"] for row in decisions] == ["2022-01-03T01:00:00Z", "2022-01-03T03:00:00Z"]
    assert [row["completed_timestamp_utc"] for row in fills] == ["2022-01-03T02:00:00Z", "2022-01-03T04:00:00Z"]
    assert [row["completed_timestamp_utc"] for row in marks] == ["2022-01-03T03:00:00Z", "2022-01-03T05:00:00Z"]
    assert all(row["raw_symbol"] == "ZNH2" for row in decisions + fills + marks)
    assert all(row["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT" for row in marks)
    for required in ("NO_2023_TEST_DATA", "NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"):
        assert required in manifest["explicitly_excluded_data"]


def test_multi_row_pack_hashes_bind_file_bytes():
    manifest = _json(PACK_ROOT, "S27_V2_PRE2023_MULTI_ROW_DECLARED_INPUT_PACK_MANIFEST.json")

    for filename, declared in manifest["row_family_files"].items():
        assert declared["sha256"].lower() == _sha256(PACK_ROOT / filename)


def test_multi_row_run_carries_position_state_and_pnl(multi_row_bundle):
    positions = _rows(RUN_ROOT, "desired_position_ledger.csv")
    orders = _rows(RUN_ROOT, "limit_order_ledger.csv")
    fills = _rows(RUN_ROOT, "fill_ledger.csv")
    pnl = _rows(RUN_ROOT, "pnl_ledger.csv")

    assert multi_row_bundle.row_count == 2
    assert multi_row_bundle.final_position_contracts == 12
    assert float(positions[0]["starting_position_contracts"]) == 0
    assert float(positions[0]["desired_position_contracts"]) == 8
    assert float(positions[0]["position_change_contracts"]) == 8
    assert float(orders[0]["limit_order_price"]) == pytest.approx(130.421875)
    assert fills[0]["fill_executed"] == "TRUE"
    assert float(fills[0]["fill_quantity"]) == 8
    assert float(fills[0]["position_after_fill"]) == 8

    assert float(positions[1]["starting_position_contracts"]) == 8
    assert float(positions[1]["desired_position_contracts"]) == 12
    assert float(positions[1]["position_change_contracts"]) == 4
    assert float(orders[1]["adjacent_target_position"]) == 9
    assert float(orders[1]["limit_order_price"]) == pytest.approx(130.328125)
    assert fills[1]["fill_executed"] == "TRUE"
    assert float(fills[1]["fill_quantity"]) == 4
    assert float(fills[1]["position_after_fill"]) == 12

    assert float(pnl[0]["row_gross_pnl_amount"]) == pytest.approx(-1000.0)
    assert float(pnl[0]["row_net_pnl_amount"]) == pytest.approx(-1018.4)
    assert float(pnl[1]["existing_position_gross_pnl"]) == pytest.approx(-250.0)
    assert float(pnl[1]["fill_gross_pnl"]) == pytest.approx(-250.0)
    assert float(pnl[1]["row_net_pnl_amount"]) == pytest.approx(-509.2)
    assert float(pnl[1]["cumulative_net_pnl_amount"]) == pytest.approx(-1527.6)
    assert multi_row_bundle.cumulative_net_pnl_amount == pytest.approx(-1527.6)


def test_multi_row_run_writes_hash_bound_metadata(multi_row_bundle):
    manifest = _json(RUN_ROOT, "run_manifest.json")
    evidence = _json(RUN_ROOT, "evidence_manifest.json")
    trusted = _json(RUN_ROOT, "trusted_bundle.json")
    sha_rows = _rows(RUN_ROOT, "SHA256SUMS.csv")
    sha_by_path = {row["relative_path"]: row["sha256"] for row in sha_rows}

    assert manifest["status"] == "S27_V2_PRE2023_MULTI_ROW_DEVELOPMENT_RECON_RUN_EMITTED_NOT_RESULT"
    assert manifest["row_count"] == 2
    assert manifest["result_interpretation"] == "NO"
    assert manifest["source_faithful_evidence_claim"] == "NO"
    assert evidence["run_manifest_hash"] == _sha256(RUN_ROOT / "run_manifest.json")
    assert trusted["result_status"] == "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
    assert trusted["source_faithful_evidence_claimed"] is False
    assert multi_row_bundle.run_manifest_hash == _sha256(RUN_ROOT / "run_manifest.json")
    assert multi_row_bundle.evidence_manifest_hash == _sha256(RUN_ROOT / "evidence_manifest.json")
    assert multi_row_bundle.trusted_bundle_hash == _sha256(RUN_ROOT / "trusted_bundle.json")
    for relative_path, digest in sha_by_path.items():
        assert digest == _sha256(RUN_ROOT / relative_path)


def test_multi_row_run_rejects_out_of_scope_paths(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited multi-row pack"):
        run_pre2023_multi_row_development_recon(tmp_path, RUN_ROOT)
    with pytest.raises(CarverBlocked, match="output root is locked"):
        run_pre2023_multi_row_development_recon(PACK_ROOT, tmp_path)


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("row_count", 1),
        ("final_position_contracts", 8),
        ("cumulative_gross_pnl_amount", 0.0),
        ("cumulative_commission_amount", 0.0),
        ("cumulative_spread_amount", 1.0),
        ("cumulative_net_pnl_amount", 1.0),
    ),
)
def test_multi_row_run_rejects_bundle_forgery(multi_row_bundle, field_name, forged_value):
    forged = _rehash_bundle(replace(multi_row_bundle, **{field_name: forged_value}))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_multi_row_run_preserves_non_authorizations(multi_row_bundle):
    assert multi_row_bundle.non_authorizations == NON_AUTHORIZATIONS
    for required in ("NO_TEST_ACCESS", "NO_VALIDATION_ACCESS", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD", "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM"):
        assert required in multi_row_bundle.non_authorizations

    forged = _rehash_bundle(replace(multi_row_bundle, non_authorizations=tuple(x for x in NON_AUTHORIZATIONS if x != "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM")))
    with pytest.raises(CarverBlocked):
        forged.validate()


def test_multi_row_run_is_not_package_root_exported():
    assert "run_pre2023_multi_row_development_recon" not in getattr(package_root, "__all__", ())
    assert not hasattr(package_root, "run_pre2023_multi_row_development_recon")

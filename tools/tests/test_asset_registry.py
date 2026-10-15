"""Failure-path checks for local asset lookup; no real datasets are loaded."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / "check_assets.py"
SPEC = importlib.util.spec_from_file_location("check_assets", TOOL)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class AssetRegistryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "model.bin").write_bytes(b"test")

    def asset(self, **extra):
        return {"id": "fixture", "title_cn": "测试资产", "category": "model_checkpoint",
                "locations": [{"path": str(self.root), "expected": "directory",
                               "probes": [{"path": "model.bin", "expected": "file"}]}], **extra}

    def test_existing_directory_with_missing_required_payload_fails(self):
        value = self.asset()
        value["locations"][0]["probes"][0]["path"] = "missing.bin"
        result = module.check_asset(value)
        self.assertEqual(result["access_status"], "PARTIAL")
        self.assertFalse(result["strict_passed"])

    def test_metadata_only_cannot_qualify_as_data(self):
        result = module.check_asset(self.asset(payload_status="METADATA_ONLY"))
        self.assertEqual(result["access_status"], "ACCESSIBLE")
        self.assertFalse(result["strict_passed"])

    def test_missing_optional_receipt_does_not_block_payload(self):
        value = self.asset()
        value["locations"][0]["probes"].append(
            {"path": "optional.json", "expected": "file", "required": False})
        self.assertTrue(module.check_asset(value)["strict_passed"])

    def test_broken_cache_symlink_is_unavailable(self):
        link = self.root / "broken.bin"
        link.symlink_to(self.root / "absent-target.bin")
        result = module.check_path(link, "file")
        self.assertEqual(result["status"], "NOT_FOUND")
        self.assertFalse(result["ok"])

    def test_cli_strict_missing_payload_and_unknown_identity_fail(self):
        value = self.asset()
        value["locations"][0]["probes"][0]["path"] = "absent.bin"
        catalog = self.root / "catalog.json"
        catalog.write_text(json.dumps({"schema_version": 1, "projects": [], "assets": [value]}))
        self.assertEqual(module.main(["--catalog", str(catalog), "--asset", "fixture", "--strict"]), 1)
        self.assertEqual(module.main(["--catalog", str(catalog), "--asset", "unknown", "--strict"]), 2)

    def test_snapshot_refuses_to_overwrite_prior_observation(self):
        catalog = self.root / "catalog.json"
        catalog.write_text(json.dumps({"schema_version": 1, "projects": [], "assets": [self.asset()]}))
        output = self.root / "existing.json"
        output.write_text("unchanged")
        self.assertEqual(module.main(["--catalog", str(catalog), "--output", str(output)]), 2)
        self.assertEqual(output.read_text(), "unchanged")

    def test_listing_cannot_be_mistaken_for_strict_access_check(self):
        catalog = self.root / "catalog.json"
        catalog.write_text(json.dumps({"schema_version": 1, "projects": [], "assets": [self.asset()]}))
        self.assertEqual(module.main(["--catalog", str(catalog), "--list", "--strict"]), 2)

    def test_misspelled_incomplete_status_is_rejected(self):
        catalog = self.root / "catalog.json"
        catalog.write_text(json.dumps({"schema_version": 1, "projects": [], "assets": [
            self.asset(payload_status="INCOMPELTE")]}))
        self.assertEqual(module.main(["--catalog", str(catalog), "--asset", "fixture", "--strict"]), 2)

    def test_unavailable_associated_project_is_not_an_implicit_dependency(self):
        project = {"id": "unrelated", "title_cn": "关联项目", "locations": [
            {"path": str(self.root / "missing-project"), "expected": "directory"}]}
        asset = self.asset(projects=["unrelated"])
        catalog = self.root / "catalog.json"
        catalog.write_text(json.dumps({"schema_version": 1, "projects": [project], "assets": [asset]}))
        self.assertEqual(module.main(["--catalog", str(catalog), "--asset", "fixture", "--strict"]), 0)
        asset["required_projects"] = ["unrelated"]
        catalog.write_text(json.dumps({"schema_version": 1, "projects": [project], "assets": [asset]}))
        self.assertEqual(module.main(["--catalog", str(catalog), "--asset", "fixture", "--strict"]), 1)

    def test_project_only_access_works_without_registered_assets(self):
        project = {"id": "empty", "title_cn": "尚无资产的项目", "locations": [
            {"path": str(self.root), "expected": "directory"}]}
        catalog = self.root / "catalog.json"
        catalog.write_text(json.dumps({"schema_version": 1, "projects": [project], "assets": []}))
        self.assertEqual(module.main(["--catalog", str(catalog), "--project", "empty", "--strict"]), 0)
        project["locations"][0]["path"] = str(self.root / "absent")
        catalog.write_text(json.dumps({"schema_version": 1, "projects": [project], "assets": []}))
        self.assertEqual(module.main(["--catalog", str(catalog), "--project", "empty", "--strict"]), 1)


if __name__ == "__main__":
    unittest.main()

"""Regressions for ownership omissions that a link-only check cannot detect."""
import json
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_anchor_organization import inspect


class AnchorOrganizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        self.anchor = "main/problem_anchors/15_representation/15_18_relation/15_18_relation_anchor.md"
        self.experiment = "main/experiments/A15/15_18_relation/first_flow"
        self.registry = {
            "schema_version": 1,
            "lines": [{"id": "A15", "anchor_root": "main/problem_anchors/15_representation",
                       "experiment_root": "main/experiments/A15", "index": "main/problem_anchors/15_representation/README.md",
                       "layout": "parent_subanchor"}],
            "anchors": [{"id": "15_18", "line": "A15", "parent_id": None,
                         "path": self.anchor, "companions": [], "experiment_roots": [self.experiment]}],
            "support_records": [], "legacy_experiments": []}
        self.write(self.anchor, "# Design\nUnknown\n")
        self.write("main/problem_anchors/15_representation/README.md", "[Design](15_18_relation/15_18_relation_anchor.md)")
        self.write(self.experiment + "/protocol.md", "# Protocol\nNOT RUN\n")

    def tearDown(self):
        self.temp.cleanup()

    def write(self, path, text):
        file = self.project / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def check(self):
        self.write("main/anchor_ownership.json", json.dumps(self.registry))
        return inspect(self.project)

    def test_registered_parent_child_and_experiments_have_unique_owners(self):
        child = "main/problem_anchors/15_representation/15_18_relation/subanchors/15_18_01_control_anchor.md"
        self.write(child, "# Local control\nUnknown")
        self.registry["anchors"].append({"id": "15_18_01", "line": "A15", "parent_id": "15_18",
                                         "path": child, "companions": [], "experiment_roots": []})
        issues, counts = self.check()
        self.assertEqual(issues, [])
        self.assertEqual(counts["anchors"], 2)
        self.assertEqual(counts["experiment_records"], 1)

    def test_support_directory_cannot_hide_a_live_unnumbered_anchor(self):
        self.write("main/problem_anchors/topic_key/anchor.md", "# New design")
        self.registry["support_records"].append({"path": "main/problem_anchors/topic_key", "reason": "support notes"})
        issues, _ = self.check()
        self.assertTrue(any("ORPHAN_ANCHOR main/problem_anchors/topic_key/anchor.md" in issue for issue in issues))

    def test_linked_but_unowned_experiment_is_still_an_error(self):
        self.write("main/experiments/A15/unregistered/protocol.md", "# Protocol\n[Anchor](../../problem.md)")
        issues, _ = self.check()
        self.assertTrue(any("ORPHAN_EXPERIMENT main/experiments/A15/unregistered/protocol.md" in issue for issue in issues))

    def test_topic_experiment_root_is_rejected_even_with_registry_entry(self):
        self.registry["lines"][0]["experiment_root"] = "main/experiments/topic"
        self.registry["anchors"][0]["experiment_roots"] = ["main/experiments/topic/round"]
        self.write("main/experiments/topic/round/protocol.md", "# Proposed")
        issues, _ = self.check()
        self.assertTrue(any(issue.startswith("UNNUMBERED_EXPERIMENT_LINE") for issue in issues))

    def test_number_collision_and_wrong_parent_are_not_accepted(self):
        other = "main/problem_anchors/15_representation/15_19_other/15_19_other_anchor.md"
        self.write(other, "# Independent decision")
        self.registry["anchors"].append({"id": "15_18", "line": "A15", "parent_id": "15_99",
                                         "path": other, "companions": [], "experiment_roots": []})
        issues, _ = self.check()
        self.assertTrue(any(issue.startswith("DUPLICATE_ANCHOR_ID 15_18") for issue in issues))
        self.assertTrue(any(issue.startswith("INVALID_PARENT 15_18") for issue in issues))

    def test_archive_snapshots_and_support_notes_are_not_new_owners(self):
        self.write("main/problem_anchors/15_representation/archive/old/anchor.md", "# Original frozen design")
        self.write("main/experiments/archive/old/protocol.md", "# Original frozen protocol")
        self.write("main/problem_anchors/15_representation/notes.md", "# A supporting explanation")
        issues, counts = self.check()
        self.assertEqual(issues, [])
        self.assertEqual(counts["anchor_files"], 1)
        self.assertEqual(counts["experiment_records"], 1)

    def test_explicit_numbered_flat_legacy_layout_is_preserved(self):
        old = "main/problem_anchors/15_representation/15_18_anchor.md"
        (self.project / self.anchor).unlink()
        self.write(old, "# Historical numbered design")
        self.registry["lines"][0]["layout"] = "registered_flat"
        self.registry["anchors"][0]["path"] = old
        self.assertEqual(self.check()[0], [])

    def test_legacy_experiment_needs_a_real_owner_and_reason(self):
        old = "main/experiments/A02/historical"
        self.write(old + "/protocol_for_approval.md", "# Historical protocol")
        self.registry["legacy_experiments"].append({"path": old, "owner_ids": ["15_18"], "reason": "immutable A02 identity"})
        self.assertEqual(self.check()[0], [])
        self.registry["legacy_experiments"][0]["owner_ids"] = ["15_99"]
        self.assertTrue(any(issue.startswith("INVALID_LEGACY_OWNER") for issue in self.check()[0]))

    def test_registry_cannot_escape_project_or_assign_history_as_current(self):
        self.registry["anchors"][0]["companions"] = ["../outside.md"]
        self.write("main/problem_anchors/15_representation/archive/snapshot_anchor.md", "# Original")
        self.registry["anchors"][0]["path"] = "main/problem_anchors/15_representation/archive/snapshot_anchor.md"
        issues, _ = self.check()
        self.assertTrue(any(issue.startswith("OUTSIDE_PROJECT") for issue in issues))
        self.assertTrue(any(issue.startswith("HISTORICAL_CANONICAL_OWNER") for issue in issues))

    def reading_map(self):
        row = {"id": "15_18", "line": "A15", "parent_id": None,
               "source": self.anchor,
               "source_sha256": hashlib.sha256((self.project / self.anchor).read_bytes()).hexdigest()}
        row.update({key: "Existing bounded explanation" for key in
                    ("title_cn", "question_cn", "why_cn", "approach_cn", "role_for_parent_cn", "evidence_state_cn", "boundary_cn")})
        return {"anchors": [row]}

    def test_current_derived_map_preserves_registered_ownership(self):
        self.write("main/research_map.json", json.dumps(self.reading_map()))
        self.assertEqual(self.check()[0], [])

    def test_map_cannot_silently_drop_or_invent_an_owner(self):
        data = self.reading_map()
        data["anchors"][0]["id"] = "15_99"
        self.write("main/research_map.json", json.dumps(data))
        issues, _ = self.check()
        self.assertTrue(any(issue.startswith("MISSING_MAP_ANCHOR 15_18") for issue in issues))
        self.assertTrue(any(issue.startswith("UNKNOWN_MAP_ANCHOR 15_99") for issue in issues))

    def test_map_must_refresh_when_anchor_changes(self):
        self.write("main/research_map.json", json.dumps(self.reading_map()))
        self.write(self.anchor, "# Revised design\nUnknown\n")
        self.assertTrue(any(issue.startswith("STALE_MAP_SOURCE 15_18") for issue in self.check()[0]))

    def test_map_cannot_reparent_a_question_or_link_absent_results(self):
        data = self.reading_map()
        data["anchors"][0].update(parent_id="15_99", related_results=["main/absent.md"])
        self.write("main/research_map.json", json.dumps(data))
        issues, _ = self.check()
        self.assertTrue(any(issue.startswith("WRONG_MAP_OWNER 15_18") for issue in issues))
        self.assertTrue(any(issue.startswith("MISSING_MAP_REFERENCE 15_18") for issue in issues))


if __name__ == "__main__":
    unittest.main()

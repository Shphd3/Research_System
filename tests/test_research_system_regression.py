import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests" / "fixtures" / "research_system_regression.json"


class ResearchSystemRegressionCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.cases = cls.data["cases"]

    def test_corpus_has_ten_real_tasks(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertEqual(len(self.cases), 10)
        self.assertEqual(len({case["id"] for case in self.cases}), 10)

    def test_scoring_prioritizes_science_and_has_hard_failures(self):
        scoring = self.data["scoring"]
        dimensions = scoring["dimensions"]
        self.assertEqual(sum(dimensions.values()), 10)
        self.assertEqual(dimensions["scientific_correctness_and_claim_safety"], 4)
        self.assertGreaterEqual(len(scoring["hard_failures"]), 4)
        self.assertIn("fresh tasks", scoring["procedure"])

    def test_every_case_has_auditable_expectations_and_real_sources(self):
        required = {
            "id",
            "task_type",
            "prompt",
            "skill",
            "source_paths",
            "baseline_failure",
            "target_behavior",
            "claim_boundary",
            "next_step",
        }
        for case in self.cases:
            self.assertEqual(set(case), required, case["id"])
            self.assertTrue((ROOT / ".agents" / "skills" / case["skill"]).is_dir())
            self.assertTrue(case["source_paths"], case["id"])
            for relative in case["source_paths"]:
                self.assertTrue((ROOT / relative).is_file(), f"{case['id']}: {relative}")

    def test_corpus_covers_result_design_protocol_meeting_and_narrow_work(self):
        kinds = {case["task_type"] for case in self.cases}
        self.assertEqual(
            kinds,
            {
                "completed_result_explanation",
                "anchor_audit",
                "protocol_audit",
                "meeting_synthesis",
                "narrow_explanation",
            },
        )
        result_cases = [
            case
            for case in self.cases
            if case["task_type"] == "completed_result_explanation"
        ]
        self.assertGreaterEqual(len(result_cases), 5)


if __name__ == "__main__":
    unittest.main()

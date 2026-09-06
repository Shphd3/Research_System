import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidatorIntegrationTests(unittest.TestCase):
    def test_live_repository_has_no_structural_errors(self):
        completed = subprocess.run(
            [str(ROOT / "researchctl"), "check", "--repository"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=40,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["ok"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["repository"]["current_focuses"], 8)
        self.assertGreater(result["repository"]["registered_references"], 8)
        self.assertGreater(result["repository"]["skill_references"], 0)


if __name__ == "__main__":
    unittest.main()

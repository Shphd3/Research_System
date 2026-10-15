"""Structural checks only; semantic scenarios need actual answer review."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]


class MethodContractTests(unittest.TestCase):
    def test_web_prompt_routes_to_owner(self):
        text = (ROOT / 'prompts/project_instructions/research_progress_project_prompt.md').read_text(encoding='utf-8')
        self.assertIn('research-reasoning-auditor', text)

    def test_no_competing_root_skill(self):
        self.assertFalse((ROOT / '.agents/skills/research-exploration').exists())

    def test_scenario_ids(self):
        text = (ROOT / 'docs/methodology/research_exploration_regression_cases.md').read_text(encoding='utf-8')
        ids = re.findall(r'^\| (R\d+) \|', text, re.M)
        self.assertEqual(ids, [f'R{i:02d}' for i in range(1, 22)])
        mapping = (ROOT / 'docs/methodology/research_exploration_mapping.md').read_text(encoding='utf-8')
        for case in set(re.findall(r'R\d{2}', mapping)):
            self.assertIn(case, ids)

    def test_skill_frontmatter(self):
        folders = [ROOT / '.agents/skills' / name for name in ['experiment-card-writer', 'problem-anchor-writer', 'research-communication', 'research-final-report', 'research-progress-core', 'research-reasoning-auditor', 'research-sync-gate', 'scholar-mode']]
        self.assertTrue(folders)
        for folder in folders:
            self.assertTrue(folder.is_dir(), str(folder))
            text = (folder / 'SKILL.md').read_text(encoding='utf-8')
            match = re.match(r'---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n', text)
            self.assertIsNotNone(match, str(folder))
            self.assertEqual(match[1], folder.name)
            self.assertLessEqual(len(match[2]), 1024)


if __name__ == '__main__':
    unittest.main()

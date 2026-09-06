from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]

ENTRY_FILES = (
    "README.md",
    "templates/README.md",
    "prompts/README.md",
    "prompts/project_instructions/README.md",
    "paper_reading/README.md",
    "papers/README.md",
    "sync/README.md",
    "Projects/README_local_worktrees.md",
)

ACTIVE_CONTROL_ROOTS = (
    "AGENTS.md",
    "README.md",
    "docs",
    ".agents/skills",
    "templates",
    "prompts",
    "paper_reading/README.md",
    "sync/README.md",
)

DEPRECATED_STATE_NAMES = {
    "HUMAN_RESULT_CONFIRMED",
    "AI_REVISED_AWAITING_HUMAN_CONFIRMATION",
}

REMOVED_TEMPLATES = {
    "templates/research_process/research_loop_folder_template.md",
    "templates/research_process/experiment_understanding_and_execution_gate_template_cn.md",
    "templates/meeting/meeting_notes_template.md",
    "templates/archive/daily_card_template_0519.md",
    "templates/archive/daily_card_template_0521.md",
}


def active_control_files():
    for relative in ACTIVE_CONTROL_ROOTS:
        path = ROOT / relative
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from (
                item
                for item in path.rglob("*.md")
                if "archive" not in item.relative_to(path).parts
            )


class EntrypointConsistencyTests(unittest.TestCase):
    def test_entry_readmes_exist(self):
        for relative in ENTRY_FILES:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_active_control_surfaces_use_current_focus_states(self):
        for path in active_control_files():
            text = path.read_text(encoding="utf-8-sig")
            for token in DEPRECATED_STATE_NAMES:
                self.assertNotIn(token, text, str(path.relative_to(ROOT)))

    def test_removed_templates_are_absent(self):
        for relative in REMOVED_TEMPLATES:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_every_current_template_is_listed_once(self):
        readme = (ROOT / "templates/README.md").read_text(encoding="utf-8")
        templates = sorted(
            path.relative_to(ROOT / "templates").as_posix()
            for path in (ROOT / "templates").rglob("*.md")
            if path.name != "README.md"
        )
        for relative in templates:
            self.assertEqual(readme.count(f"`{relative}`"), 1, relative)

    def test_prompt_index_names_only_existing_prompts(self):
        readme = (
            ROOT / "prompts/project_instructions/README.md"
        ).read_text(encoding="utf-8")
        mentioned = set(re.findall(r"`([^`]+_prompt(?:_cn)?\.md)`", readme))
        existing = {
            path.name
            for path in (ROOT / "prompts/project_instructions").glob("*.md")
            if path.name != "README.md"
        }
        self.assertEqual(mentioned, existing)

    def test_reading_and_sync_entries_follow_current_boundaries(self):
        reading = (ROOT / "paper_reading/README.md").read_text(encoding="utf-8")
        self.assertNotIn("_templates/", reading)
        self.assertNotIn("recordings.md", reading)
        sync = (ROOT / "sync/README.md").read_text(encoding="utf-8")
        self.assertIn("only when the user explicitly requests", sync)
        self.assertNotIn("whenever a mainline state change", sync)


if __name__ == "__main__":
    unittest.main()

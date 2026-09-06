from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"


class ResearchCommunicationSkillTests(unittest.TestCase):
    def test_one_router_replaces_three_writing_skills(self):
        merged = SKILLS / "research-communication"
        self.assertTrue((merged / "SKILL.md").is_file())
        for name in (
            "meeting-outline-writer",
            "research-story-writer",
            "handoff-report-writer",
        ):
            self.assertFalse((SKILLS / name).exists(), name)

    def test_router_is_small_and_routes_to_exactly_three_references(self):
        skill = (SKILLS / "research-communication" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertLessEqual(len(skill.split()), 300)
        referenced = set(re.findall(r"references/([a-z_]+\.md)", skill))
        self.assertEqual(referenced, {"meeting.md", "story.md", "handoff.md"})
        for filename in referenced:
            self.assertTrue(
                (SKILLS / "research-communication" / "references" / filename).is_file()
            )

    def test_handoff_mode_retains_explicit_external_action_gate(self):
        handoff = (
            SKILLS / "research-communication" / "references" / "handoff.md"
        ).read_text(encoding="utf-8")
        self.assertIn("explicit user request", handoff)
        self.assertIn("Do not overwrite dirty collaborator files", handoff)
        self.assertIn("Commit and push only when the user explicitly asks", handoff)

    def test_root_routing_surfaces_no_longer_name_removed_skills(self):
        for relative in ("AGENTS.md", "docs/skills.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            for removed in (
                "meeting-outline-writer",
                "research-story-writer",
                "handoff-report-writer",
            ):
                self.assertNotIn(removed, text, f"{relative}: {removed}")

    def test_root_routing_surfaces_list_every_root_skill(self):
        skill_names = {
            path.parent.name for path in SKILLS.glob("*/SKILL.md")
        }
        for relative in ("AGENTS.md", "docs/skills.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            missing = sorted(name for name in skill_names if f"`{name}`" not in text)
            self.assertEqual(missing, [], relative)

    def test_large_multimode_skills_use_small_progressive_routers(self):
        expected = {
            "research-progress-core": {
                "focus_cycle.md",
                "result_interpretation.md",
                "daily_report.md",
                "failure_decomposition.md",
                "goal_audit.md",
                "algorithm_specification.md",
                "profiling_and_evidence.md",
            },
            "research-mainline": {
                "layout_and_naming.md",
                "artifact_lifecycle.md",
                "line_direction_contract.md",
                "publication_and_archive.md",
            },
        }
        for skill_name, reference_names in expected.items():
            skill_path = SKILLS / skill_name / "SKILL.md"
            skill = skill_path.read_text(encoding="utf-8")
            self.assertLessEqual(len(skill.split()), 500, skill_name)
            referenced = set(re.findall(r"references/([a-z_]+\.md)", skill))
            self.assertEqual(referenced, reference_names, skill_name)
            for filename in referenced:
                self.assertTrue(
                    (SKILLS / skill_name / "references" / filename).is_file()
                )


if __name__ == "__main__":
    unittest.main()

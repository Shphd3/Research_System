from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AnchorArchitectureTests(unittest.TestCase):
    def test_root_system_design_and_superpowers_scaffolds_are_absent(self):
        self.assertFalse((ROOT / "docs" / "design.md").exists())
        self.assertFalse((ROOT / ".superpowers").exists())
        self.assertFalse((ROOT / "docs" / "superpowers").exists())

    def test_anchor_is_the_only_project_research_design_owner(self):
        controls = [
            ROOT / "AGENTS.md",
            ROOT / ".agents" / "skills" / "problem-anchor-writer" / "SKILL.md",
            ROOT / ".agents" / "skills" / "research-mainline" / "SKILL.md",
        ]
        text = "\n".join(path.read_text(encoding="utf-8") for path in controls)
        self.assertIn("sole canonical current research design", text)
        self.assertIn("Do not create a parallel `design.md`", text)

    def test_anchor_contract_keeps_the_complete_design_chain(self):
        skill = (
            ROOT / ".agents" / "skills" / "problem-anchor-writer" / "SKILL.md"
        ).read_text(encoding="utf-8")
        required_sections = (
            "## 1. Problem Definition",
            "## 2. Physical Priors",
            "## 3. Falsifiable Hypotheses",
            "## 4. Mathematical Model",
            "## 5. Computational Realization",
            "## 6. Minimal Falsification Tests",
            "## 7. Current Evidence",
            "## 8. Claim Boundary And Next Decision",
        )
        for section in required_sections:
            self.assertIn(section, skill)
        self.assertIn("references/learnable_research_design.md", skill)
        self.assertIn("adopt, adapt, baseline, or reject", skill)

    def test_root_entry_points_do_not_reference_deleted_system_design(self):
        for relative in ("AGENTS.md", "PROJECTS.md", "README.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("docs/design.md", text, relative)


if __name__ == "__main__":
    unittest.main()

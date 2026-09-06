from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]

CURRENT_FOCUS_PATHS = (
    "daily_research_reports/0901/focus_m2d2_semantic_geometric_form.md",
    "daily_research_reports/0906/focus_gmm_pseudolabel_handoff.md",
    "daily_research_reports/0903/focus_gmm_pseudolabel_oracle_gap.md",
    "daily_research_reports/0904/focus_layerwise_moe_insertion_validation.md",
    "daily_research_reports/0904/focus_headwise_causal_semantic_retrieval_audit.md",
    "daily_research_reports/0903/focus_sae_hierarchical_teacher_construction.md",
    "daily_research_reports/backup/2026/08/0830/focus_qwen3_30b_semantic_representation_separability.md",
    "daily_research_reports/backup/2026/08/0829/focus_gradient_consistent_hierarchical_routing.md",
)

VALID_STATES = {
    "task_state": {"DRAFT", "ACTIVE", "CLOSED"},
    "question_state": {"AWAITING_HUMAN_CONFIRMATION", "HUMAN_CONFIRMED"},
    "design_state": {
        "NOT_REQUIRED",
        "AWAITING_HUMAN_CONFIRMATION",
        "HUMAN_CONFIRMED",
    },
    "result_state": {
        "NOT_AVAILABLE",
        "AWAITING_HUMAN_CONFIRMATION",
        "HUMAN_CONFIRMED",
    },
}


def metadata(text: str) -> dict[str, str]:
    match = re.search(r"```text\n(.*?)\n```", text, re.DOTALL)
    if not match:
        return {}
    values = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


class FocusStateArchitectureTests(unittest.TestCase):
    def test_current_focuses_use_orthogonal_states(self):
        for relative in CURRENT_FOCUS_PATHS:
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            fields = metadata(path.read_text(encoding="utf-8"))
            for key, allowed in VALID_STATES.items():
                self.assertIn(key, fields, f"{relative}: {key}")
                self.assertIn(fields[key], allowed, f"{relative}: {key}")

    def test_current_focuses_do_not_copy_other_lifecycles(self):
        forbidden = {
            "status",
            "core_question",
            "plain_language_design",
            "protocol_state",
            "execution_state",
            "conversation_owner",
            "ownership_status",
        }
        for relative in CURRENT_FOCUS_PATHS:
            fields = metadata((ROOT / relative).read_text(encoding="utf-8"))
            self.assertEqual(forbidden.intersection(fields), set(), relative)

    def test_closed_focus_has_human_confirmed_result(self):
        for relative in CURRENT_FOCUS_PATHS:
            fields = metadata((ROOT / relative).read_text(encoding="utf-8"))
            if fields["task_state"] == "CLOSED":
                self.assertEqual(fields["result_state"], "HUMAN_CONFIRMED", relative)

    def test_template_assigns_protocol_and_execution_state_to_their_owners(self):
        text = (ROOT / "templates/research_process/focus_writing_template.md").read_text(
            encoding="utf-8"
        )
        for key in VALID_STATES:
            self.assertIn(f"{key}:", text)
        self.assertIn("Protocol 的草稿/批准状态只由", text)
        self.assertIn("执行的未开始/运行中/完成/失败状态只由", text)


if __name__ == "__main__":
    unittest.main()

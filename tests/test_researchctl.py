import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "researchctl"


class ResearchCtlTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "daily_research_reports" / "0906").mkdir(parents=True)
        self.focus = self.root / "daily_research_reports" / "0906" / "focus_demo.md"
        self.anchor = self.root / "Projects" / "demo" / "main" / "anchor.md"
        self.anchor.parent.mkdir(parents=True)
        self.anchor.write_text("# Anchor\n", encoding="utf-8")
        self.focus.write_text(
            "problem_key: demo.problem\n\n"
            "[Anchor](../../Projects/demo/main/anchor.md)\n",
            encoding="utf-8",
        )
        (self.root / "PROJECTS.md").write_text(
            "| Problem key | Focus |\n"
            "|---|---|\n"
            "| `demo.problem` | `daily_research_reports/0906/focus_demo.md` |\n",
            encoding="utf-8",
        )
        research = self.root / ".research"
        research.mkdir()
        (research / "config.json").write_text(
            json.dumps(
                {"schema_version": 2, "state_path": ".research/runtime/state.json"}
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def run_ctl(self, *args, conversation="conversation-a", expect=0):
        env = os.environ.copy()
        env["RESEARCHCTL_ROOT"] = str(self.root)
        if conversation is None:
            env.pop("CODEX_THREAD_ID", None)
            env.pop("RESEARCHCTL_THREAD_ID", None)
        else:
            env["CODEX_THREAD_ID"] = conversation
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=self.root,
            env=env,
            text=True,
            capture_output=True,
        )
        self.assertEqual(
            completed.returncode,
            expect,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        stream = completed.stdout if completed.stdout.strip() else completed.stderr
        return json.loads(stream)

    def register(self, part, *, conversation="conversation-a", paths=()):
        args = ["context", "demo.problem", "--task", part]
        for path in paths:
            args.extend(["--path", path])
        return self.run_ctl(*args, conversation=conversation)

    def write_repository_contract(self, *, role="PRIMARY", protocol_approved=True):
        protocol = self.root / "Projects" / "demo" / "main" / "protocol.md"
        protocol.write_text(
            "status: APPROVED_FOR_EXECUTION\n"
            if protocol_approved
            else "# Protocol without a decision record\n",
            encoding="utf-8",
        )
        self.focus.write_text(
            "# Demo\n\n"
            "```text\n"
            "type: meeting_cycle_core_task\n"
            "task_state: ACTIVE\n"
            "problem_key: demo.problem\n"
            f"focus_role: {role}\n"
            "question_state: HUMAN_CONFIRMED\n"
            "design_state: HUMAN_CONFIRMED\n"
            "result_state: NOT_AVAILABLE\n"
            "anchor: Projects/demo/main/anchor.md\n"
            "protocol: Projects/demo/main/protocol.md\n"
            "```\n",
            encoding="utf-8",
        )
        (self.root / "PROJECTS.md").write_text(
            "## Current Focus Priority\n\n"
            "| Problem key | Role | Owning Focus | Current state |\n"
            "|---|---|---|---|\n"
            "| `demo.problem` | `PRIMARY` | "
            "`daily_research_reports/0906/focus_demo.md` | active |\n",
            encoding="utf-8",
        )

    def test_same_problem_supports_different_conversation_parts(self):
        first = self.register("audit metric", conversation="conversation-a")
        second = self.register("inspect baseline", conversation="conversation-b")

        self.assertEqual(first["task"]["problem_key"], "demo.problem")
        self.assertEqual(second["task"]["task_part"], "inspect baseline")
        self.assertTrue(
            any(item["code"] == "SAME_PROBLEM" for item in second["advisories"])
        )

        status = self.run_ctl("status", "demo.problem", conversation=None)
        self.assertEqual(len(status["tasks"]), 2)
        self.assertEqual({task["status"] for task in status["tasks"]}, {"OPEN"})

    def test_path_overlap_warns_but_never_blocks(self):
        self.register(
            "revise anchor interpretation",
            conversation="conversation-a",
            paths=("Projects/demo/main/anchor.md",),
        )
        second = self.register(
            "audit anchor evidence",
            conversation="conversation-b",
            paths=("Projects/demo/main",),
        )

        overlap = [item for item in second["advisories"] if item["code"] == "PATH_OVERLAP"]
        self.assertEqual(len(overlap), 1)
        self.assertEqual(overlap[0]["level"], "WARNING")
        checked = self.run_ctl("check", "demo.problem", conversation=None)
        self.assertTrue(checked["ok"])
        self.assertTrue(any(item["code"] == "PATH_OVERLAP" for item in checked["advisories"]))

    def test_one_conversation_updates_its_single_open_task(self):
        first = self.register("first part", paths=("Projects/demo/main/anchor.md",))
        second = self.register("refined part", paths=("daily_research_reports/0906",))

        self.assertEqual(first["task"]["task_id"], second["task"]["task_id"])
        status = self.run_ctl("status", conversation=None)
        self.assertEqual(len(status["tasks"]), 1)
        self.assertEqual(status["tasks"][0]["task_part"], "refined part")

    def test_context_loads_registered_sources_without_file_contents(self):
        result = self.register("explain current design")
        returned_paths = {item["path"] for item in result["context"]}

        self.assertIn("daily_research_reports/0906/focus_demo.md", returned_paths)
        self.assertIn("Projects/demo/main/anchor.md", returned_paths)
        self.assertNotIn("# Anchor", json.dumps(result))

    def test_release_closes_only_calling_conversation_task(self):
        first = self.register("first part", conversation="conversation-a")
        self.register("second part", conversation="conversation-b")

        closed = self.run_ctl(
            "release", first["task"]["task_id"], conversation="conversation-a"
        )
        self.assertEqual(closed["status"], "CLOSED")
        status = self.run_ctl("status", conversation=None)
        self.assertEqual(len(status["tasks"]), 1)
        all_tasks = self.run_ctl("status", "--all", conversation=None)
        self.assertEqual(len(all_tasks["tasks"]), 2)

    def test_named_stale_task_can_be_closed_from_another_conversation(self):
        task = self.register("first part", conversation="conversation-a")["task"]
        result = self.run_ctl(
            "release", task["task_id"], conversation="conversation-b"
        )
        self.assertEqual(result["status"], "CLOSED")
        self.assertEqual(result["closed_by_conversation_id"], "conversation-b")

    def test_no_expiry_or_lease_fields_exist(self):
        task = self.register("long-running analysis")["task"]
        self.assertNotIn("expires_at", task)
        self.assertNotIn("lease", json.dumps(task).lower())

    def test_unregistered_problem_and_escaping_path_are_refused(self):
        missing = self.run_ctl(
            "context", "missing.problem", "--task", "unknown", expect=2
        )
        self.assertEqual(missing["error"], "UNREGISTERED_PROBLEM")

        escaped = self.run_ctl(
            "context",
            "demo.problem",
            "--task",
            "unsafe",
            "--path",
            "../outside.md",
            expect=2,
        )
        self.assertEqual(escaped["error"], "INVALID_PATH")

    def test_missing_conversation_identifier_does_not_write_state(self):
        result = self.run_ctl(
            "context",
            "demo.problem",
            "--task",
            "part",
            conversation=None,
            expect=2,
        )
        self.assertEqual(result["error"], "CONVERSATION_ID_REQUIRED")
        self.assertFalse((self.root / ".research" / "runtime" / "state.json").exists())

    def test_v1_active_claims_migrate_to_advisory_tasks(self):
        state_path = self.root / ".research" / "runtime" / "state.json"
        state_path.parent.mkdir(parents=True)
        state_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "bindings": {},
                    "claims": {
                        "claim-old": {
                            "claim_id": "claim-old",
                            "owner": "conversation-old",
                            "problem_key": "demo.problem",
                            "resources": ["artifact:Projects/demo/main/anchor.md"],
                            "acquired_at": "2026-09-05T00:00:00Z",
                            "status": "ACTIVE",
                        }
                    },
                    "runs": {},
                    "events": [],
                }
            ),
            encoding="utf-8",
        )

        status = self.run_ctl("status", conversation=None)
        self.assertEqual(status["schema_version"], 2)
        self.assertEqual(len(status["tasks"]), 1)
        self.assertEqual(status["tasks"][0]["conversation_id"], "conversation-old")

    def test_corrupt_registry_is_not_silently_replaced(self):
        state_path = self.root / ".research" / "runtime" / "state.json"
        state_path.parent.mkdir(parents=True)
        state_path.write_text("not-json\n", encoding="utf-8")

        result = self.run_ctl("status", conversation=None, expect=4)

        self.assertEqual(result["error"], "CORRUPT_STATE")
        self.assertEqual(state_path.read_text(encoding="utf-8"), "not-json\n")

    def test_repository_check_accepts_valid_orthogonal_contract(self):
        self.write_repository_contract()

        result = self.run_ctl("check", "--repository", conversation=None)

        self.assertTrue(result["ok"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["repository"]["current_focuses"], 1)
        self.assertEqual(result["repository"]["protocol_authorizations"], 1)

    def test_repository_check_detects_drift_and_missing_authorization(self):
        self.write_repository_contract(role="SECONDARY", protocol_approved=False)
        text = self.focus.read_text(encoding="utf-8").replace(
            "result_state: NOT_AVAILABLE",
            "result_state: NOT_AVAILABLE\nconversation_owner: old-thread",
        )
        self.focus.write_text(text, encoding="utf-8")

        result = self.run_ctl(
            "check", "--repository", conversation=None, expect=4
        )
        codes = {item["code"] for item in result["errors"]}

        self.assertIn("PROJECTS_FOCUS_ROLE_DRIFT", codes)
        self.assertIn("FOCUS_OWNS_FOREIGN_STATE", codes)
        self.assertIn("PROTOCOL_AUTHORIZATION_UNDECLARED", codes)


if __name__ == "__main__":
    unittest.main()

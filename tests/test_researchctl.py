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

    def test_context_ignores_fenced_block_delimiters_when_scanning_links(self):
        self.focus.write_text(
            "# Demo\n\n"
            "```text\n"
            "problem_key: demo.problem\n"
            "task_state: ACTIVE\n"
            "```\n\n"
            + ("This prose is not a path. " * 20)
            + "`0903/focus_other.md` is unrelated.\n\n"
            "[Anchor](../../Projects/demo/main/anchor.md)\n",
            encoding="utf-8",
        )

        result = self.register("scan focus with fenced metadata")
        returned_paths = {item["path"] for item in result["context"]}

        self.assertIn("daily_research_reports/0906/focus_demo.md", returned_paths)
        self.assertIn("Projects/demo/main/anchor.md", returned_paths)

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

    def write_execution_envelope(self):
        envelope = self.root / "docs" / "execution_envelope.md"
        envelope.parent.mkdir(parents=True, exist_ok=True)
        envelope.write_text(
            "# Execution Envelope\n\n"
            "```yaml\n"
            "default_profile: h100-4-reserved\n"
            "profiles:\n"
            "  h100-4-reserved:\n"
            "    status: default\n"
            "images:\n"
            "  shphd-h100:\n"
            "    url: \"registry.example.invalid/ns/image:tag\"\n"
            "legacy_profiles: [local-2xh100]\n"
            "legacy_images:\n"
            "  ngc-pytorch-25-06:\n"
            "    url: \"registry.example.invalid/ns/legacy:tag\"\n"
            "```\n",
            encoding="utf-8",
        )

    def write_protocol_front_matter(self, body):
        self.write_repository_contract()
        protocol = self.root / "Projects" / "demo" / "main" / "protocol.md"
        protocol.write_text(body, encoding="utf-8")
        return protocol

    def test_repository_check_flags_unregistered_execution_keys(self):
        self.write_execution_envelope()
        self.write_protocol_front_matter(
            "---\n"
            "status: APPROVED_FOR_EXECUTION\n"
            "resource_profile: h100-8-reserved\n"
            "image_id: shphd-unknown\n"
            "---\n\n"
            "# Protocol\n"
        )

        result = self.run_ctl("check", "--repository", conversation=None)
        codes = {item["code"] for item in result["advisories"]}

        self.assertTrue(result["ok"])
        self.assertIn("PROTOCOL_RESOURCE_PROFILE_UNKNOWN", codes)
        self.assertIn("PROTOCOL_IMAGE_ID_UNKNOWN", codes)

    def test_repository_check_accepts_registered_and_legacy_execution_keys(self):
        self.write_execution_envelope()
        self.write_protocol_front_matter(
            "---\n"
            "status: APPROVED_FOR_EXECUTION\n"
            "resource_profile: h100-4-reserved\n"
            "image_id: shphd-h100\n"
            "---\n\n"
            "# Protocol\n"
        )

        result = self.run_ctl("check", "--repository", conversation=None)
        codes = {item["code"] for item in result["advisories"]}

        self.assertNotIn("PROTOCOL_RESOURCE_PROFILE_UNKNOWN", codes)
        self.assertNotIn("PROTOCOL_IMAGE_ID_UNKNOWN", codes)

    def test_repository_check_requires_an_expanded_image_in_a_run_receipt(self):
        self.write_execution_envelope()
        self.write_protocol_front_matter(
            "---\n"
            "status: APPROVED_FOR_EXECUTION\n"
            "---\n\n"
            "# Protocol\n\nExecution: job `pt-abc12345` succeeded.\n"
        )

        result = self.run_ctl("check", "--repository", conversation=None)
        codes = {item["code"] for item in result["advisories"]}

        self.assertIn("EXECUTION_RECEIPT_INCOMPLETE", codes)

    def test_repository_check_accepts_a_receipt_with_the_image(self):
        self.write_execution_envelope()
        self.write_protocol_front_matter(
            "---\n"
            "status: APPROVED_FOR_EXECUTION\n"
            "---\n\n"
            "# Protocol\n\nExecution: job `pt-abc12345` on "
            "`registry.example.invalid/ns/image:tag`.\n"
        )

        result = self.run_ctl("check", "--repository", conversation=None)
        codes = {item["code"] for item in result["advisories"]}

        self.assertNotIn("EXECUTION_RECEIPT_INCOMPLETE", codes)

    def test_missing_execution_envelope_is_reported_not_silently_skipped(self):
        self.write_repository_contract()

        result = self.run_ctl("check", "--repository", conversation=None)

        codes = {item["code"] for item in result["advisories"]}
        self.assertIn("EXECUTION_ENVELOPE_MISSING", codes)

    def write_date_report(self, body, *, relative="0901/focus_demo.md"):
        report = self.root / "daily_research_reports" / relative
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(body, encoding="utf-8")
        return report

    def write_date_figure(self, name="panel.png", *, date="0901"):
        figure = self.root / "daily_research_reports" / date / "figures" / name
        figure.parent.mkdir(parents=True, exist_ok=True)
        figure.write_bytes(b"\x89PNG\r\n\x1a\n")
        return figure

    def test_repository_check_flags_an_unresolved_figure_link(self):
        self.write_repository_contract()
        self.write_date_report("# Focus\n\n![panel](figures/missing.png)\n")

        result = self.run_ctl("check", "--repository", conversation=None, expect=4)
        codes = {item["code"] for item in result["errors"]}

        self.assertIn("FIGURE_LINK_UNRESOLVED", codes)

    def test_repository_check_flags_a_figure_outside_the_date_directory(self):
        self.write_repository_contract()
        outside = self.root / "Projects" / "demo" / "main" / "figures" / "panel.png"
        outside.parent.mkdir(parents=True, exist_ok=True)
        outside.write_bytes(b"\x89PNG\r\n\x1a\n")
        self.write_date_report(
            "# Focus\n\n![panel](../../Projects/demo/main/figures/panel.png)\n"
        )

        result = self.run_ctl("check", "--repository", conversation=None, expect=4)
        codes = {item["code"] for item in result["errors"]}

        self.assertIn("FIGURE_OUTSIDE_DATE_FIGURES", codes)

    def test_repository_check_flags_an_absolute_figure_path(self):
        self.write_repository_contract()
        self.write_date_report("# Focus\n\n![panel](/tmp/panel.png)\n")

        result = self.run_ctl("check", "--repository", conversation=None, expect=4)
        codes = {item["code"] for item in result["errors"]}

        self.assertIn("FIGURE_PATH_NOT_DATE_LOCAL", codes)

    def test_repository_check_accepts_a_date_local_figure_copy(self):
        self.write_repository_contract()
        self.write_date_figure()
        self.write_date_report("# Focus\n\n![panel](figures/panel.png)\n")

        result = self.run_ctl("check", "--repository", conversation=None)

        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["repository"]["date_figure_violations"], 0)

    def test_archived_date_directories_are_not_retrofitted(self):
        self.write_repository_contract()
        archived = self.write_date_report(
            "# Old\n\n![panel](figures/missing.png)\n",
            relative="backup/2026/08/0830/focus_old.md",
        )
        self.assertTrue(archived.is_file())

        result = self.run_ctl("check", "--repository", conversation=None)

        self.assertTrue(result["ok"], result["errors"])

    def write_sources_manifest(self, rows, *, date="0901"):
        manifest = (
            self.root / "daily_research_reports" / date / "figures" / "SOURCES.md"
        )
        manifest.parent.mkdir(parents=True, exist_ok=True)
        header = (
            "# Figure Sources\n\n"
            "| File | Origin | Source | SHA256 | Note |\n"
            "|---|---|---|---|---|\n"
        )
        manifest.write_text(header + "".join(rows), encoding="utf-8")
        return manifest

    def test_repository_check_flags_an_undeclared_date_figure(self):
        self.write_repository_contract()
        self.write_date_figure()

        result = self.run_ctl("check", "--repository", conversation=None)
        codes = {item["code"] for item in result["advisories"]}

        self.assertIn("FIGURE_MANIFEST_MISSING", codes)

    def test_repository_check_flags_a_stale_reading_copy(self):
        self.write_repository_contract()
        self.write_date_figure()
        evidence = self.root / "Projects" / "demo" / "main" / "figures" / "panel.png"
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_bytes(b"\x89PNG\r\n\x1a\nchanged")
        self.write_sources_manifest(
            [
                "| `panel.png` | copy | `Projects/demo/main/figures/panel.png` | "
                f"`{'0' * 64}` | experiment figure |\n"
            ]
        )

        result = self.run_ctl("check", "--repository", conversation=None, expect=4)
        codes = {item["code"] for item in result["errors"]}

        self.assertIn("FIGURE_COPY_MISMATCH", codes)

    def test_repository_check_flags_a_self_referencing_manifest_row(self):
        self.write_repository_contract()
        figure = self.write_date_figure()
        self.write_sources_manifest(
            [
                "| `panel.png` | copy | "
                f"`{figure.relative_to(self.root).as_posix()}` | "
                f"`{'0' * 64}` | experiment figure |\n"
            ]
        )

        result = self.run_ctl("check", "--repository", conversation=None, expect=4)
        codes = {item["code"] for item in result["errors"]}

        self.assertIn("FIGURE_COPY_SELF_REFERENCE", codes)

    def test_repository_check_accepts_a_generated_figure_row(self):
        self.write_repository_contract()
        self.write_date_figure()
        self.write_sources_manifest(
            [
                "| `panel.png` | generated | `scripts/build.py` from `tables/x.csv` | "
                f"`{'0' * 64}` | exact artifact join |\n"
            ]
        )

        result = self.run_ctl("check", "--repository", conversation=None)

        self.assertTrue(result["ok"], result["errors"])
        self.assertNotIn(
            "FIGURE_MANIFEST_MISSING",
            {item["code"] for item in result["advisories"]},
        )

    def write_profiled_envelope(self, *, profile_status="default"):
        envelope = self.root / "docs" / "execution_envelope.md"
        envelope.parent.mkdir(parents=True, exist_ok=True)
        envelope.write_text(
            "# Execution Envelope\n\n"
            "```yaml\n"
            "default_profile: h100-4-reserved\n"
            "default_image: shphd-lite-0911\n"
            "profiles:\n"
            "  h100-4-reserved:\n"
            f"    status: {profile_status}\n"
            "    surface: acp\n"
            "    workspace: share-space\n"
            "    aec2: share-cluster\n"
            "    worker_spec: n6ls.iu.i40.4\n"
            "    worker_nodes: 1\n"
            "    worker_processes: 4\n"
            "    quota_type: reserved\n"
            "    priority: normal\n"
            '    storage_mount: "vol-1:/data"\n'
            "  h100-4-spot:\n"
            "    status: deferred\n"
            '    deferred_on: "2026-09-10"\n'
            "    worker_spec: n6ls.iu.i40.4\n"
            "    quota_type: spot\n"
            "images:\n"
            "  shphd-lite-0911:\n"
            "    status: default\n"
            '    url: "registry.example.invalid/ns/shphd:tag1"\n'
            '    interpreter: "Python 3.10"\n'
            "submission:\n"
            '  entry_point: "/opt/shim.sh"\n'
            '  default_mode: "DRY_RUN=1"\n'
            "```\n",
            encoding="utf-8",
        )

    def test_envelope_resolves_the_default_tuple_from_the_registry(self):
        self.write_profiled_envelope()

        result = self.run_ctl("envelope", conversation=None)

        self.assertEqual(result["resource_profile"], "h100-4-reserved")
        self.assertEqual(result["image_id"], "shphd-lite-0911")
        self.assertEqual(result["image_url"], "registry.example.invalid/ns/shphd:tag1")
        self.assertEqual(result["workspace"], "share-space")
        self.assertEqual(result["quota_type"], "reserved")
        self.assertEqual(result["storage_mount"], "vol-1:/data")
        self.assertEqual(result["submission_entry_point"], "/opt/shim.sh")

    def test_envelope_shell_format_prints_assignments(self):
        self.write_profiled_envelope()

        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "envelope", "--format", "shell"],
            cwd=self.root,
            env={**os.environ, "RESEARCHCTL_ROOT": str(self.root)},
            text=True,
            capture_output=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('WORKER_SPEC="n6ls.iu.i40.4"', completed.stdout)
        self.assertIn(
            'IMAGE_URL="registry.example.invalid/ns/shphd:tag1"', completed.stdout
        )

    def test_envelope_refuses_a_deferred_profile(self):
        self.write_profiled_envelope()

        result = self.run_ctl(
            "envelope", "--profile", "h100-4-spot", conversation=None, expect=2
        )

        self.assertEqual(result["error"], "PROFILE_DEFERRED")

    def test_envelope_refuses_an_unknown_key(self):
        self.write_profiled_envelope()

        result = self.run_ctl(
            "envelope", "--image", "shphd-does-not-exist", conversation=None, expect=2
        )

        self.assertEqual(result["error"], "UNKNOWN_IMAGE_KEY")


if __name__ == "__main__":
    unittest.main()

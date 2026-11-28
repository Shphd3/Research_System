import os
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates/execution/acp_submit_template.sh"
SHARED = "/data/250010109/MoE_Router/acp_receipts"


class ExecutionReceiptPaths(unittest.TestCase):
    def preview(self, **paths):
        env = {"PATH": os.environ["PATH"], "JOB_NAME": "paths-test",
               "REMOTE_CMD": "true", "DRY_RUN": "1", **paths}
        result = subprocess.run(["bash", str(TEMPLATE)], env=env, cwd=ROOT,
                                capture_output=True, text=True, check=True)
        self.assertIn("[dry-run]", result.stdout)
        return result.stdout

    def test_system_root_uses_execution_storage(self):
        for inputs in ({}, {"REMOTE_DIR": str(ROOT) + "/"}):
            with self.subTest(inputs=inputs):
                output = self.preview(**inputs)
                self.assertRegex(output, rf"(?m)^receipt_directory\s+{SHARED}$")
                self.assertIn(f"mkdir -p {SHARED}/pod;", output)

    def test_external_workspace_keeps_its_pod_logs(self):
        output = self.preview(REMOTE_DIR="/mounted/experiment")
        self.assertIn("mkdir -p /mounted/experiment/acp_receipts/pod;", output)

    def test_explicit_destinations(self):
        output = self.preview(REMOTE_DIR=str(ROOT), RUN_ROOT="/receipts",
                              POD_LOG_DIR="/durable/pod")
        self.assertRegex(output, r"(?m)^receipt_directory\s+/receipts$")
        self.assertIn("mkdir -p /durable/pod;", output)

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_script(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


class OdphScriptsTest(unittest.TestCase):
    def test_artifact_check_passes(self):
        result = run_script("scripts/check_agent_artifacts.py")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("ODPH v0.2", result.stdout)

    def test_generated_schema_is_current(self):
        result = run_script("scripts/generate_artifacts.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("up to date", result.stdout)

    def test_validator_accepts_action_and_change_task(self):
        for document in [
            "source/examples/change-chain/actions/tc01-create-objective.yaml",
            "source/examples/change-chain/change-tasks/change-chain.yaml",
        ]:
            result = run_script("scripts/validate_package.py", document)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("valid ODPH change-control document", result.stdout)

    def test_complete_example_validator_passes(self):
        result = run_script("scripts/validate_examples.py")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("16 ChangeActions", result.stdout)


if __name__ == "__main__":
    unittest.main()

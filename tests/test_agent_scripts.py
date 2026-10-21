import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "source/examples/retention-change/change-package.yaml"


def run_script(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


class OdphScriptsTest(unittest.TestCase):
    def test_artifact_check_passes(self):
        result = run_script("scripts/check_agent_artifacts.py")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_generated_schema_is_current(self):
        result = run_script("scripts/generate_artifacts.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_complete_package_validates(self):
        result = run_script("scripts/validate_package.py", PACKAGE, "--at", "2026-10-21T12:00:00Z", "--current-rev", "184")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("valid ODPH Change Package", result.stdout)

    def test_complete_example_validator_passes(self):
        result = run_script("scripts/validate_examples.py")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("retention graph-change", result.stdout)

    def test_object_search_reads_the_change_package_record(self):
        result = run_script("scripts/search_objects.py", "--id", "ChangePackage")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("graph-change", result.stdout)


if __name__ == "__main__":
    unittest.main()

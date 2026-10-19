import json
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
        self.assertIn("ODPH", result.stdout)

    def test_generated_schema_is_current(self):
        result = run_script("scripts/generate_artifacts.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("up to date", result.stdout)

    def test_validator_accepts_full_and_minimal_packages(self):
        for example in ["minimal.yaml", "full-retention-review.yaml"]:
            result = run_script("scripts/validate_package.py", f"source/examples/{example}")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("valid ODPH package", result.stdout)

    def test_object_search_returns_evidence_object(self):
        result = run_script("scripts/search_objects.py", "evidence", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("EvidenceEvent", {record["id"] for record in json.loads(result.stdout)})


if __name__ == "__main__":
    unittest.main()

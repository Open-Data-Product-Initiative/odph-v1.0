import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"


class GwpArtifactsTest(unittest.TestCase):
    def test_schema_declares_governed_work_package_root(self):
        schema = yaml.safe_load((SOURCE / "schema" / "gwp.yaml").read_text(encoding="utf-8"))
        json_schema = json.loads((SOURCE / "schema" / "gwp.json").read_text(encoding="utf-8"))
        self.assertEqual(schema, json_schema)
        self.assertEqual(schema["required"], ["schema", "version", "kind", "package"])
        self.assertEqual(schema["properties"]["kind"]["const"], "GovernedWorkPackage")
        self.assertIn("evidence", schema["properties"])
        self.assertIn("corrections", schema["properties"])

    def test_examples_cover_package_and_all_object_kinds(self):
        examples = SOURCE / "examples"
        expected = {
            "minimal.yaml", "full-retention-review.yaml", "context-package.yaml", "mandate.yaml",
            "work-envelope.yaml", "execution-package.yaml", "execution-request.yaml",
            "revocation-policy.yaml", "evidence-event.yaml", "correction.yaml",
        }
        self.assertEqual({path.name for path in examples.glob("*.yaml")}, expected)
        full = yaml.safe_load((examples / "full-retention-review.yaml").read_text(encoding="utf-8"))
        self.assertEqual(full["kind"], "GovernedWorkPackage")
        self.assertEqual(full["package"]["metadata"]["conformanceProfile"], "kentaro-v0.1-local-only")
        self.assertEqual(
            {item["kind"] for item in full["package"]["objects"]},
            {"ContextPackage", "Mandate", "WorkEnvelope", "ExecutionPackage", "ExecutionRequest", "RevocationPolicy"},
        )
        self.assertEqual(full["evidence"]["events"][0]["kind"], "EvidenceEvent")
        self.assertEqual(full["corrections"][0]["kind"], "Correction")

    def test_object_records_and_guidance_are_gwp_aligned(self):
        records = [json.loads(line) for line in (SOURCE / "objects.jsonl").read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual(
            {record["id"] for record in records},
            {"ContextPackage", "Mandate", "WorkEnvelope", "ExecutionPackage", "ExecutionRequest", "RevocationPolicy", "EvidenceEvent", "Correction"},
        )
        guidance = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/schema/gwp.yaml", guidance)
        self.assertIn("/objects.jsonl", guidance)
        self.assertIn("never permission to execute", guidance)


if __name__ == "__main__":
    unittest.main()

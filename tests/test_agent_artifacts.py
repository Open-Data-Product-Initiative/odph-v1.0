import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"


class OdphArtifactsTest(unittest.TestCase):
    def test_schema_declares_the_two_v02_document_kinds(self):
        schema = yaml.safe_load((SOURCE / "odph-v0.2/schema/kentaro-change.yaml").read_text(encoding="utf-8"))
        json_schema = json.loads((SOURCE / "odph-v0.2/schema/kentaro-change.json").read_text(encoding="utf-8"))
        self.assertEqual(schema, json_schema)
        self.assertEqual(schema["$id"], "https://opendataproducts.org/odph-v0.2/schema/kentaro-change.yaml")
        self.assertEqual(schema["oneOf"], [{"$ref": "#/$defs/KentaroAction"}, {"$ref": "#/$defs/KentaroChangeTask"}])
        self.assertEqual(schema["$defs"]["KentaroAction"]["properties"]["kind"]["const"], "KentaroAction")
        self.assertEqual(schema["$defs"]["KentaroChangeTask"]["properties"]["kind"]["const"], "KentaroChangeTask")

    def test_examples_cover_the_six_case_mortgage_renewal_chain(self):
        root = SOURCE / "examples/mortgage-renewal"
        self.assertEqual(len(list((root / "actions").glob("*.yaml"))), 16)
        self.assertEqual(len(list((root / "change-tasks").glob("*.yaml"))), 1)
        self.assertEqual(len(list((root / "specifications").rglob("*.yaml"))), 16)
        task = yaml.safe_load((root / "change-tasks/mortgage-renewal-planning-change.yaml").read_text(encoding="utf-8"))
        self.assertEqual(task["kind"], "KentaroChangeTask")
        self.assertEqual(len(task["actions"]), 5)

    def test_object_records_and_guidance_are_v02_aligned(self):
        records = [json.loads(line) for line in (SOURCE / "objects.jsonl").read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual({record["id"] for record in records}, {"KentaroAction", "KentaroChangeTask"})
        guidance = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/odph-v0.2/schema/kentaro-change.yaml", guidance)
        self.assertIn("/examples/mortgage-renewal/", guidance)
        self.assertIn("MCP is planned only for v0.3", guidance)


if __name__ == "__main__":
    unittest.main()

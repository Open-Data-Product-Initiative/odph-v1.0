import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"


class OdphArtifactsTest(unittest.TestCase):
    def test_schema_declares_the_two_v02_document_kinds(self):
        schema = yaml.safe_load((SOURCE / "odph-v0.2/schema/change-control.yaml").read_text(encoding="utf-8"))
        json_schema = json.loads((SOURCE / "odph-v0.2/schema/change-control.json").read_text(encoding="utf-8"))
        self.assertEqual(schema, json_schema)
        self.assertEqual(schema["$id"], "https://opendataproducts.org/odph-v0.2/schema/change-control.yaml")
        self.assertEqual(schema["oneOf"], [{"$ref": "#/$defs/ChangeAction"}, {"$ref": "#/$defs/ChangeTask"}])
        self.assertEqual(schema["$defs"]["ChangeAction"]["properties"]["kind"]["const"], "ChangeAction")
        self.assertEqual(schema["$defs"]["ChangeTask"]["properties"]["kind"]["const"], "ChangeTask")

    def test_examples_cover_the_six_case_generic_change_chain(self):
        root = SOURCE / "examples/change-chain"
        self.assertEqual(len(list((root / "actions").glob("*.yaml"))), 16)
        self.assertEqual(len(list((root / "change-tasks").glob("*.yaml"))), 1)
        self.assertEqual(len(list((root / "specifications").rglob("*.yaml"))), 16)
        task = yaml.safe_load((root / "change-tasks/change-chain.yaml").read_text(encoding="utf-8"))
        self.assertEqual(task["kind"], "ChangeTask")
        self.assertEqual(len(task["actions"]), 5)

    def test_object_records_and_guidance_are_v02_aligned(self):
        records = [json.loads(line) for line in (SOURCE / "objects.jsonl").read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual({record["id"] for record in records}, {"ChangeAction", "ChangeTask"})
        guidance = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/odph-v0.2/schema/change-control.yaml", guidance)
        self.assertIn("/examples/change-chain/", guidance)
        self.assertIn("MCP is planned only for v0.3", guidance)


if __name__ == "__main__":
    unittest.main()

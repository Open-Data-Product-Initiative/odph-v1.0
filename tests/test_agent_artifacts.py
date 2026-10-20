import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"


class OdphArtifactsTest(unittest.TestCase):
    def test_schema_declares_all_eight_top_level_object_kinds(self):
        schema = yaml.safe_load((SOURCE / "odph-v0.2/schema/change-control.yaml").read_text(encoding="utf-8"))
        json_schema = json.loads((SOURCE / "odph-v0.2/schema/change-control.json").read_text(encoding="utf-8"))
        self.assertEqual(schema, json_schema)
        self.assertEqual(schema["$id"], "https://opendataproducts.org/odph-v0.2/schema/change-control.yaml")
        self.assertEqual(schema["oneOf"], [{"$ref": f"#/$defs/{object_id}"} for object_id in [
            "ContextPackage", "Mandate", "WorkEnvelope", "ExecutionPackage",
            "ExecutionRequest", "EvidenceEvent", "ChangeAction", "ChangeTask",
        ]])
        for object_id in ["ContextPackage", "Mandate", "WorkEnvelope", "ExecutionPackage", "ExecutionRequest", "EvidenceEvent"]:
            self.assertEqual(schema["$defs"][object_id]["allOf"][-1]["properties"]["kind"]["const"], object_id)
        self.assertEqual(
            schema["$defs"]["ObjectMetadata"]["required"],
            ["id", "name", "description", "version", "createdAt", "actor"],
        )
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
        for filename, object_kind in [
            ("context-package.yaml", "ContextPackage"),
            ("mandate.yaml", "Mandate"),
            ("work-envelope.yaml", "WorkEnvelope"),
            ("execution-package.yaml", "ExecutionPackage"),
            ("execution-request.yaml", "ExecutionRequest"),
            ("evidence-event.yaml", "EvidenceEvent"),
        ]:
            example = yaml.safe_load((SOURCE / "examples" / filename).read_text(encoding="utf-8"))
            self.assertEqual(example["kind"], object_kind)

    def test_schema_validates_each_standalone_governed_work_object(self):
        schema = yaml.safe_load((SOURCE / "odph-v0.2/schema/change-control.yaml").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        required_groups = {
            "context-package.yaml": {"metadata", "provenance", "context"},
            "mandate.yaml": {"metadata", "provenance", "mandate", "boundary"},
            "work-envelope.yaml": {"metadata", "provenance", "assignment", "boundary"},
            "execution-package.yaml": {"metadata", "provenance", "execution", "boundary", "plan"},
            "execution-request.yaml": {"metadata", "provenance", "execution", "request"},
            "evidence-event.yaml": {"metadata", "provenance", "evidence"},
        }
        for filename, groups in required_groups.items():
            example = yaml.safe_load((SOURCE / "examples" / filename).read_text(encoding="utf-8"))
            self.assertFalse({"id", "version", "createdAt", "actor"} & set(example))
            self.assertTrue(groups <= set(example), filename)
            self.assertIn("en", example["metadata"]["name"])
            self.assertIn("en", example["metadata"]["description"])
            errors = sorted(validator.iter_errors(example), key=lambda error: list(error.path))
            self.assertEqual(errors, [], f"{filename}: {errors}")

    def test_object_records_and_guidance_are_v02_aligned(self):
        records = [json.loads(line) for line in (SOURCE / "objects.jsonl").read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual({record["id"] for record in records}, {
            "ContextPackage", "Mandate", "WorkEnvelope", "ExecutionPackage",
            "ExecutionRequest", "EvidenceEvent", "ChangeAction", "ChangeTask",
        })
        guidance = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/odph-v0.2/schema/change-control.yaml", guidance)
        self.assertIn("/examples/change-chain/", guidance)
        self.assertIn("They do not replace Maysano APIs.", guidance)

    def test_documentation_yaml_examples_use_block_structure(self):
        documentation = (SOURCE / "index.html.md").read_text(encoding="utf-8")
        yaml_blocks = re.findall(r"```yaml\n(.*?)```", documentation, flags=re.DOTALL)
        self.assertGreater(len(yaml_blocks), 0)
        for block in yaml_blocks:
            self.assertNotIn("{", block, "YAML examples must not hide nested maps in flow notation")


if __name__ == "__main__":
    unittest.main()

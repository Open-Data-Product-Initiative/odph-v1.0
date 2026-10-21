import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(ROOT / "scripts"))
from validate_package import validate_package


class ChangePackageTest(unittest.TestCase):
    def setUp(self):
        self.schema = yaml.safe_load((SOURCE / "odph-v0.2/schema/change-package.yaml").read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(self.schema, format_checker=FormatChecker())
        self.source_example = SOURCE / "examples/retention-change"

    def variant(self, mutate):
        temporary = tempfile.TemporaryDirectory()
        copied = Path(temporary.name) / "retention-change"
        shutil.copytree(self.source_example, copied)
        package_path = copied / "change-package.yaml"
        package = yaml.safe_load(package_path.read_text(encoding="utf-8"))
        mutate(package, copied)
        package_path.write_text(yaml.safe_dump(package, sort_keys=False), encoding="utf-8")
        self.addCleanup(temporary.cleanup)
        return package_path, package

    def schema_errors(self, package):
        return list(self.validator.iter_errors(package))

    def test_canonical_schema_and_example(self):
        derived = json.loads((SOURCE / "odph-v0.2/schema/change-package.json").read_text(encoding="utf-8"))
        self.assertEqual(self.schema, derived)
        self.assertEqual(self.schema["$id"], "https://opendataproducts.org/odph/v0.2/schema/change-package.yaml")
        self.assertFalse(self.schema_errors(yaml.safe_load((self.source_example / "change-package.yaml").read_text(encoding="utf-8"))))

    def test_every_top_level_section_is_required(self):
        base = yaml.safe_load((self.source_example / "change-package.yaml").read_text(encoding="utf-8"))
        for section in ["meta", "need", "auth", "context", "actions", "evidence"]:
            document = copy.deepcopy(base)
            document.pop(section)
            self.assertTrue(self.schema_errors(document), section)

    def test_unknown_and_reserved_kind_diagnostics(self):
        path, _ = self.variant(lambda document, root: document.update(kind="unknown"))
        self.assertEqual(validate_package(path, at="2026-10-21T12:00:00Z"), ["unknown-kind"])
        path, _ = self.variant(lambda document, root: document.update(kind="graph-operation"))
        self.assertEqual(validate_package(path, at="2026-10-21T12:00:00Z"), ["unsupported-kind"])

    def test_closed_enums_reject_invalid_values(self):
        mutations = [
            lambda d: d["need"]["actor"].update(type="robot"),
            lambda d: d["need"]["job"].update(type="wish"),
            lambda d: d["need"]["gap"].update(type="unclear"),
            lambda d: d["need"]["success"][0].update(type="technical"),
            lambda d: d["actions"][0].update(op="delete"),
            lambda d: d["actions"][0]["evidence"].update(runState="done"),
        ]
        for mutation in mutations:
            document = yaml.safe_load((self.source_example / "change-package.yaml").read_text(encoding="utf-8"))
            mutation(document)
            self.assertTrue(self.schema_errors(document))

    def test_file_paths_and_action_reasoning_are_closed(self):
        for value in ["/absolute.odpc.yaml", "../parent.odpc.yaml", "artefacts/not-allowed.txt"]:
            path, _ = self.variant(lambda document, root, value=value: document["actions"][0].update(file=value))
            self.assertTrue(validate_package(path, at="2026-10-21T12:00:00Z")[0].startswith("schema:"))
        for field in ["gap", "finding", "effect"]:
            path, _ = self.variant(lambda document, root, field=field: document["actions"][0].pop(field))
            self.assertTrue(validate_package(path, at="2026-10-21T12:00:00Z")[0].startswith("schema:"))

    def test_context_authority_graph_and_evidence_semantics(self):
        for field in ["current", "target"]:
            path, _ = self.variant(lambda document, root, field=field: document["context"].pop(field))
            self.assertTrue(validate_package(path, at="2026-10-21T12:00:00Z")[0].startswith("schema:"))
        path, _ = self.variant(lambda document, root: document["auth"].update(until="2026-10-21T09:00:00Z"))
        self.assertIn("invalid-authority-range", validate_package(path, at="2026-10-21T12:00:00Z"))
        self.assertIn("expired-authority", validate_package(path, at="2027-01-01T00:00:00Z"))
        path, _ = self.variant(lambda document, root: document["context"]["target"].update(graph="graph/retention-context.odpg.yaml"))
        self.assertIn("unchanged-graph", validate_package(path, at="2026-10-21T12:00:00Z"))
        self.assertIn("graph-drift", validate_package(self.source_example / "change-package.yaml", at="2026-10-21T12:00:00Z", current_revision=185))
        path, _ = self.variant(lambda document, root: document["evidence"].update(outcomeState="pass"))
        self.assertIn("incomplete-evidence", validate_package(path, at="2026-10-21T12:00:00Z"))

    def test_actions_must_connect_need_current_and_target_graphs(self):
        path, _ = self.variant(lambda document, root: document["actions"][0].update(finding="Completely unrelated observation."))
        self.assertIn("action-1:ungrounded-finding", validate_package(path, at="2026-10-21T12:00:00Z"))
        path, _ = self.variant(lambda document, root: document["actions"][0].update(effect="Unrealised unrelated target state."))
        self.assertIn("action-1:missing-target-effect", validate_package(path, at="2026-10-21T12:00:00Z"))
        path, _ = self.variant(lambda document, root: document["actions"][0].update(gap="Unrelated warehouse condition.", finding="Unrelated warehouse condition.", effect="Unrelated warehouse condition."))
        self.assertIn("action-1:unconnected-business-need", validate_package(path, at="2026-10-21T12:00:00Z"))


if __name__ == "__main__":
    unittest.main()

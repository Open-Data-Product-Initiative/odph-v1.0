#!/usr/bin/env python
import json
import sys

import yaml

from odph_paths import EXAMPLES_DIR, LLMS_TXT, OBJECTS_JSONL, SCHEMA_JSON, SCHEMA_YAML


EXPECTED_OBJECT_IDS = {"ChangeAction", "ChangeTask"}


def load_yaml(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def check_schema():
    schema = load_yaml(SCHEMA_YAML)
    json_schema = json.loads(SCHEMA_JSON.read_text(encoding="utf-8"))
    assert schema["$id"] == "https://opendataproducts.org/odph-v0.2/schema/change-control.yaml"
    assert json_schema == schema
    assert schema["oneOf"] == [{"$ref": "#/$defs/ChangeAction"}, {"$ref": "#/$defs/ChangeTask"}]
    assert set(schema["$defs"]) >= {"ChangeAction", "ChangeTask", "SpecificationChange", "ActionReference"}


def check_examples():
    root = EXAMPLES_DIR / "change-chain"
    assert len(list((root / "actions").glob("*.yaml"))) == 16
    assert len(list((root / "change-tasks").glob("*.yaml"))) == 1
    assert len(list((root / "specifications").rglob("*.yaml"))) == 16


def check_records_and_guidance():
    records = [json.loads(line) for line in OBJECTS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert {record["id"] for record in records} == EXPECTED_OBJECT_IDS
    for record in records:
        assert all(record.get(field) for field in ["definition", "requiredFields", "doUseFor", "doNotUseFor", "exampleFile"])
    llms = LLMS_TXT.read_text(encoding="utf-8")
    for path in ["/odph-v0.2/schema/change-control.yaml", "/odph-v0.2/schema/change-control.json", "/objects.jsonl", "/examples/change-chain/"]:
        assert path in llms


def main():
    checks = [check_schema, check_examples, check_records_and_guidance]
    failures = []
    for check in checks:
        try:
            check()
        except Exception as exc:
            failures.append(f"{check.__name__}: {exc}")
    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures), file=sys.stderr)
        return 1
    print("OK: ODPH v0.2 agent artifacts are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

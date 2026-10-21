#!/usr/bin/env python3
import json
import sys

import yaml

from odph_paths import LLMS_TXT, OBJECTS_JSONL, PACKAGE_EXAMPLE, SCHEMA_JSON, SCHEMA_YAML


def check_schema():
    schema = yaml.safe_load(SCHEMA_YAML.read_text(encoding="utf-8"))
    derived = json.loads(SCHEMA_JSON.read_text(encoding="utf-8"))
    assert schema == derived
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"] == "https://opendataproducts.org/odph/v0.2/schema/change-package.yaml"
    assert schema["oneOf"] == [
        {"$ref": "#/$defs/GraphChangePackage"},
        {"$ref": "#/$defs/GraphOperationStub"},
    ]
    assert schema["$defs"]["PackageKind"]["enum"] == ["graph-change", "graph-operation"]


def check_example():
    package = yaml.safe_load(PACKAGE_EXAMPLE.read_text(encoding="utf-8"))
    assert package["kind"] == "graph-change"
    assert set(package) == {"schema", "version", "kind", "meta", "need", "auth", "context", "actions", "evidence"}
    assert len(package["actions"]) == 4
    assert len({action["id"] for action in package["actions"]}) == len(package["actions"])
    assert package["actions"][-1]["op"] == "apply"
    for relative in [
        package["context"]["current"]["graph"], package["context"]["target"]["graph"],
        *[action["file"] for action in package["actions"]],
    ]:
        assert (PACKAGE_EXAMPLE.parent / relative).is_file(), relative


def check_records_and_guidance():
    records = [json.loads(line) for line in OBJECTS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert [record["id"] for record in records] == ["ChangePackage"]
    assert records[0]["kinds"] == ["graph-change", "graph-operation"]
    guidance = LLMS_TXT.read_text(encoding="utf-8")
    for path in ["/odph-v0.2/schema/change-package.yaml", "/odph-v0.2/schema/change-package.json", "/examples/retention-change/change-package.yaml"]:
        assert path in guidance


def main():
    failures = []
    for check in [check_schema, check_example, check_records_and_guidance]:
        try:
            check()
        except Exception as exc:
            failures.append(f"{check.__name__}: {exc}")
    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures), file=sys.stderr)
        return 1
    print("OK: ODPH v0.2 Change Package artifacts are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

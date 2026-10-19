#!/usr/bin/env python
import json
import sys

import yaml

from odph_paths import EXAMPLES_DIR, LLMS_TXT, OBJECTS_JSONL, SCHEMA_JSON, SCHEMA_YAML


EXPECTED_EXAMPLES = {
    "minimal.yaml", "full-retention-review.yaml", "context-package.yaml", "mandate.yaml",
    "work-envelope.yaml", "execution-package.yaml", "execution-request.yaml",
    "revocation-policy.yaml", "evidence-event.yaml", "correction.yaml",
}
EXPECTED_OBJECT_IDS = {
    "ContextPackage", "Mandate", "WorkEnvelope", "ExecutionPackage", "ExecutionRequest",
    "RevocationPolicy", "EvidenceEvent", "Correction",
}


def load_yaml(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def check_schema():
    schema = load_yaml(SCHEMA_YAML)
    json_schema = json.loads(SCHEMA_JSON.read_text(encoding="utf-8"))
    assert schema["required"] == ["schema", "version", "kind", "package"]
    assert json_schema == schema
    assert schema["properties"]["kind"]["const"] == "OpenDataProductHarness"
    assert schema["properties"]["package"]["$ref"] == "#/$defs/Package"
    assert set(schema["$defs"]) >= {"Reference", "ContextPackage", "Mandate", "WorkEnvelope", "ExecutionPackage", "ExecutionRequest", "RevocationPolicy", "EvidenceEvent", "Correction"}


def check_examples():
    actual = {path.name for path in EXAMPLES_DIR.glob("*.yaml")}
    assert actual == EXPECTED_EXAMPLES, f"Unexpected examples: {sorted(actual)}"
    minimal = load_yaml(EXAMPLES_DIR / "minimal.yaml")
    assert minimal["kind"] == "OpenDataProductHarness"
    assert minimal["package"]["metadata"]["conformanceProfile"] == "local-only"
    full = load_yaml(EXAMPLES_DIR / "full-retention-review.yaml")
    assert full["package"]["metadata"]["conformanceProfile"] == "kentaro-v0.1-local-only"
    assert {item["kind"] for item in full["package"]["objects"]} == {"ContextPackage", "Mandate", "WorkEnvelope", "ExecutionPackage", "ExecutionRequest", "RevocationPolicy"}
    assert full["evidence"]["events"][0]["kind"] == "EvidenceEvent"
    assert full["corrections"][0]["kind"] == "Correction"


def check_records_and_guidance():
    records = [json.loads(line) for line in OBJECTS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert {record["id"] for record in records} == EXPECTED_OBJECT_IDS
    for record in records:
        assert all(record.get(field) for field in ["definition", "requiredFields", "doUseFor", "doNotUseFor", "exampleFile"])
    llms = LLMS_TXT.read_text(encoding="utf-8")
    for path in ["/schema/odph.yaml", "/schema/odph.json", "/objects.jsonl", "/examples/full-retention-review.yaml"]:
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
    print("OK: ODPH agent artifacts are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

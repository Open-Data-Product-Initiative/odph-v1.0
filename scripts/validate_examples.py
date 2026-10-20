#!/usr/bin/env python
"""Validate the complete v0.2 change-chain example chain."""
import hashlib
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from open_data_products.agent import validate_document

from odph_paths import EXAMPLES_DIR, SCHEMA_YAML


class NoDatesSafeLoader(yaml.SafeLoader):
    pass


for first_char, resolvers in list(NoDatesSafeLoader.yaml_implicit_resolvers.items()):
    NoDatesSafeLoader.yaml_implicit_resolvers[first_char] = [
        (tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"
    ]


def load_yaml(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=NoDatesSafeLoader)


def resolve(base, reference):
    candidate = (base / reference).resolve()
    root = EXAMPLES_DIR.resolve()
    if root not in candidate.parents and candidate != root:
        raise ValueError(f"reference escapes examples: {reference}")
    if not candidate.is_file():
        raise ValueError(f"referenced file is missing: {reference}")
    return candidate


def validate_schema(document, path, validator):
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    if errors:
        formatted = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors
        )
        raise ValueError(f"{path}: {formatted}")


def validate_specification(path, expected_family):
    result = validate_document(path)
    if not result.valid:
        raise ValueError(f"{path}: {'; '.join(result.errors)}")
    actual_family = {"odpc": "ODPC", "odps": "ODPS", "odpg": "ODPG"}.get(result.spec)
    if actual_family != expected_family:
        raise ValueError(f"{path}: expected {expected_family}, got {actual_family}")
    if actual_family == "ODPG":
        graph = load_yaml(path)
        for node in graph["graph"]["nodes"]:
            local_ref = node["$ref"].split("#", 1)[0]
            if local_ref:
                resolve(path.parent, local_ref)


def has_cycle(actions):
    graph = {action["id"]: action.get("dependsOn", []) for action in actions}
    for action_id, dependencies in graph.items():
        missing = set(dependencies) - set(graph)
        if missing:
            raise ValueError(f"{action_id}: missing dependencies {sorted(missing)}")
    visiting, visited = set(), set()

    def visit(action_id):
        if action_id in visiting:
            raise ValueError(f"dependency cycle includes {action_id}")
        if action_id not in visited:
            visiting.add(action_id)
            for dependency in graph[action_id]:
                visit(dependency)
            visiting.remove(action_id)
            visited.add(action_id)

    for action_id in graph:
        visit(action_id)


def main():
    schema = load_yaml(SCHEMA_YAML)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    root = EXAMPLES_DIR / "change-chain"
    actions = sorted((root / "actions").glob("*.yaml"))
    tasks = sorted((root / "change-tasks").glob("*.yaml"))
    if len(actions) != 16 or len(tasks) != 1:
        raise ValueError("expected 16 action files and one change task")

    for action_path in actions:
        action = load_yaml(action_path)
        validate_schema(action, action_path, validator)
        specification = action["specification"]
        specification_path = resolve(root, specification["file"])
        checksum = hashlib.sha256(specification_path.read_bytes()).hexdigest()
        if checksum != specification["sha256"]:
            raise ValueError(f"{action_path}: specification checksum does not match")
        validate_specification(specification_path, specification["family"])

    for task_path in tasks:
        task = load_yaml(task_path)
        validate_schema(task, task_path, validator)
        identifiers = [action["id"] for action in task["actions"]]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError(f"{task_path}: duplicate action IDs")
        has_cycle(task["actions"])
        for action_ref in task["actions"]:
            action_path = resolve(root, action_ref["actionFile"])
            action = load_yaml(action_path)
            validate_schema(action, action_path, validator)
            if action["kind"] != "KentaroAction":
                raise ValueError(f"{action_path}: Change Task references a non-action document")
            if action["metadata"].get("parentChangeTask") != task["metadata"]["id"]:
                raise ValueError(f"{action_path}: parentChangeTask does not match {task_path}")

    print(f"OK: validated {len(actions)} KentaroActions, {len(tasks)} KentaroChangeTask, and their ODPC, ODPS, and ODPG files.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3
"""Validate an ODPH v0.2 Change Package without claiming live Maysano access."""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from odph_paths import SCHEMA_YAML


class NoDatesSafeLoader(yaml.SafeLoader):
    pass


for first_char, resolvers in list(NoDatesSafeLoader.yaml_implicit_resolvers.items()):
    NoDatesSafeLoader.yaml_implicit_resolvers[first_char] = [
        (tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"
    ]


STOP_WORDS = {"a", "an", "and", "as", "at", "before", "by", "for", "from", "has", "in", "is", "no", "not", "of", "on", "or", "the", "to", "with"}


def load_data(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle) if path.suffix.lower() == ".json" else yaml.load(handle, Loader=NoDatesSafeLoader)


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def resolve_file(package_path, reference):
    root = package_path.parent.resolve()
    candidate = (root / reference).resolve()
    if root not in candidate.parents or not candidate.is_file():
        raise ValueError(f"invalid-reference:{reference}")
    return candidate


def text_terms(value):
    return {word for word in re.findall(r"[a-z0-9]+", yaml.safe_dump(value, sort_keys=True).lower()) if len(word) > 2 and word not in STOP_WORDS}


def validate_referenced_document(path, expected=None):
    from open_data_products.agent import validate_document

    result = validate_document(path)
    if not result.valid:
        return f"invalid-referenced-document:{path.name}"
    if expected and result.spec.upper() != expected:
        return f"wrong-referenced-family:{path.name}"
    return None


def semantic_errors(package, package_path, *, at=None, current_revision=None, check_references=True):
    errors = []
    auth = package["auth"]
    try:
        starts, ends = parse_time(auth["at"]), parse_time(auth["until"])
        evaluated_at = parse_time(at) if isinstance(at, str) else (at or datetime.now(timezone.utc))
        if ends <= starts:
            errors.append("invalid-authority-range")
        if evaluated_at > ends:
            errors.append("expired-authority")
    except (TypeError, ValueError):
        errors.append("invalid-authority-time")

    current = package["context"]["current"]
    if current_revision is not None and current["rev"] != current_revision:
        errors.append("graph-drift")

    current_graph = target_graph = None
    try:
        current_path = resolve_file(package_path, current["graph"])
        target_path = resolve_file(package_path, package["context"]["target"]["graph"])
        current_graph, target_graph = load_data(current_path), load_data(target_path)
        if check_references:
            for graph_path in [current_path, target_path]:
                failure = validate_referenced_document(graph_path, "ODPG")
                if failure:
                    errors.append(failure)
        if current_graph == target_graph:
            errors.append("unchanged-graph")
    except ValueError as exc:
        errors.append(str(exc))

    need_terms = text_terms(package["need"])
    current_terms = text_terms(current_graph) if current_graph is not None else set()
    target_terms = text_terms(target_graph) if target_graph is not None else set()
    for index, action in enumerate(package["actions"], start=1):
        try:
            action_path = resolve_file(package_path, action["file"])
            if check_references:
                family = Path(action["file"]).name.split(".")[-2].upper()
                failure = validate_referenced_document(action_path, family)
                if failure:
                    errors.append(f"action-{index}:{failure}")
        except ValueError as exc:
            errors.append(f"action-{index}:{exc}")
        action_terms = text_terms({key: action[key] for key in ["gap", "finding", "effect"]})
        if len(action_terms & need_terms) < 2:
            errors.append(f"action-{index}:unconnected-business-need")
        if len(text_terms(action["finding"]) & current_terms) < 2:
            errors.append(f"action-{index}:ungrounded-finding")
        if len(text_terms(action["effect"]) & target_terms) < 2:
            errors.append(f"action-{index}:missing-target-effect")

    if package["evidence"]["outcomeState"] == "pass" and any(
        action["evidence"][state] != "pass"
        for action in package["actions"] for state in ["runState", "graphState"]
    ):
        errors.append("incomplete-evidence")
    return errors


def validate_package(package_path, *, schema_path=SCHEMA_YAML, at=None, current_revision=None, check_references=True):
    import jsonschema

    package_path, schema_path = Path(package_path), Path(schema_path)
    package = load_data(package_path)
    kind = package.get("kind") if isinstance(package, dict) else None
    if kind == "graph-operation":
        return ["unsupported-kind"]
    if kind != "graph-change":
        return ["unknown-kind"]
    schema = load_data(schema_path)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    shape = sorted(validator.iter_errors(package), key=lambda error: list(error.path))
    if shape:
        return [f"schema:{'.'.join(map(str, error.path)) or '<root>'}:{error.message}" for error in shape]
    return semantic_errors(package, package_path, at=at, current_revision=current_revision, check_references=check_references)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an ODPH Change Package.")
    parser.add_argument("package", help="Path to a Change Package YAML or JSON document")
    parser.add_argument("--schema", default=str(SCHEMA_YAML))
    parser.add_argument("--at", help="RFC 3339 evaluation time; defaults to current UTC time")
    parser.add_argument("--current-rev", type=int, help="Authoritative Maysano revision supplied at apply time")
    parser.add_argument("--no-reference-check", action="store_true", help="Skip local ODPC, ODPS, and ODPG validation")
    args = parser.parse_args(argv)
    try:
        errors = validate_package(args.package, schema_path=args.schema, at=args.at, current_revision=args.current_rev, check_references=not args.no_reference_check)
    except (FileNotFoundError, json.JSONDecodeError, yaml.YAMLError, ValueError) as exc:
        print(f"Validation setup failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        print(f"{args.package}: invalid ODPH Change Package", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"{args.package}: valid ODPH Change Package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

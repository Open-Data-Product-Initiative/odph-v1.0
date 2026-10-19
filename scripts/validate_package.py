#!/usr/bin/env python
import argparse
import json
import sys
from pathlib import Path

import yaml

from odph_paths import SCHEMA_YAML


class NoDatesSafeLoader(yaml.SafeLoader):
    pass


for first_char, resolvers in list(NoDatesSafeLoader.yaml_implicit_resolvers.items()):
    NoDatesSafeLoader.yaml_implicit_resolvers[first_char] = [
        (tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"
    ]


def load_data(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle) if path.suffix.lower() == ".json" else yaml.load(handle, Loader=NoDatesSafeLoader)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an ODPH YAML or JSON package against the ODPH schema.")
    parser.add_argument("package", help="Path to an ODPH YAML or JSON package")
    parser.add_argument("--schema", default=str(SCHEMA_YAML), help="Schema path; defaults to source/schema/odph.yaml")
    args = parser.parse_args(argv)
    try:
        import jsonschema
    except ModuleNotFoundError:
        print("Missing dependency: jsonschema. Install with `python -m pip install -r scripts/requirements-agent.txt`.", file=sys.stderr)
        return 2
    try:
        package = load_data(Path(args.package))
        schema = load_data(Path(args.schema))
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(package), key=lambda error: list(error.path))
    except (FileNotFoundError, json.JSONDecodeError, yaml.YAMLError, jsonschema.SchemaError) as exc:
        print(f"Validation setup failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        print(f"{args.package}: invalid ODPH package", file=sys.stderr)
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            print(f"- {location}: {error.message}", file=sys.stderr)
        return 1
    print(f"{args.package}: valid ODPH package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

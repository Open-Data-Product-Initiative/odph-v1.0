#!/usr/bin/env python
import argparse
import json

import yaml

from gwp_paths import SCHEMA_JSON, SCHEMA_YAML


def render_schema_json():
    with SCHEMA_YAML.open(encoding="utf-8") as handle:
        return json.dumps(yaml.safe_load(handle), indent=2) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate derived GWP artifacts from canonical sources.")
    parser.add_argument("--check", action="store_true", help="Check without writing files.")
    args = parser.parse_args(argv)
    expected = render_schema_json()
    current = SCHEMA_JSON.read_text(encoding="utf-8") if SCHEMA_JSON.exists() else ""
    if args.check:
        if current != expected:
            print(f"{SCHEMA_JSON}: out of date. Run `python scripts/generate_artifacts.py`.")
            return 1
        print("OK: GWP artifacts are up to date.")
        return 0
    SCHEMA_JSON.write_text(expected, encoding="utf-8")
    print(f"Generated {SCHEMA_JSON.relative_to(SCHEMA_JSON.parents[2])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

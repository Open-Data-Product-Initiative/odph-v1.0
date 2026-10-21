#!/usr/bin/env python3
"""Validate the canonical complete ODPH v0.2 graph-change example."""
import sys

from odph_paths import PACKAGE_EXAMPLE
from validate_package import validate_package


def main():
    errors = validate_package(PACKAGE_EXAMPLE, at="2026-10-21T12:00:00Z", current_revision=184)
    if errors:
        print("\n".join(f"FAIL {error}" for error in errors), file=sys.stderr)
        return 1
    print("OK: complete retention graph-change package and 6 referenced ODPG/ODPC/ODPS artifacts validate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

---
title: Validation and runtime checks | ODPH v0.2
---

# Validation and runtime checks

## Level 1: static schema validation

- Validate `KentaroAction` and `KentaroChangeTask` YAML against [`kentaro-change-v0.2.schema.yaml`](odph-v0.2/schema/kentaro-change.yaml).
- Validate ODPC files against the ODPC schema.
- Validate ODPS files against the ODPS schema.
- Validate ODPG files against the ODPG graph schema.

Run the repository checks:

```sh
python scripts/generate_artifacts.py --check
python scripts/check_agent_artifacts.py
python scripts/validate_examples.py
python -m unittest discover -s tests
bundle exec middleman build
```

`validate_examples.py` uses the Open Data Products SDK schemas for ODPC, ODPS 4.2, and ODPG, verifies every referenced file and checksum, and checks the published Kentaro schema locally. CI runs the same checks.

## Level 2: cross-file and runtime validation

Before a Maysano write, resolve every referenced specification file; verify the checksum; verify action references; reject duplicate action IDs and dependency cycles; verify required Maysano object versions and the current graph revision; and verify ODPC, ODPS, and ODPG files are mutually consistent. Verify approvals before every write.

Record submitted file identifiers, resulting Maysano identities and versions, validation outcomes, and reconciliation state. Maysano is authoritative for returned state; these checks do not turn Kentaro into a record store.

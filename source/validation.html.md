---
title: Change Package validation | ODPH v0.2
---

# Change Package validation

Shape validation uses JSON Schema Draft 2020-12. Deterministic validation handles relationships and lifecycle conditions that JSON Schema cannot infer: authorization range and expiry, local referenced-document validation, meaningful G0/G1 difference, action grounding in the business need and G0, target effects in G1, apply-time graph drift, and completion state.

```sh
python3 scripts/generate_artifacts.py --check
python3 scripts/check_agent_artifacts.py
python3 scripts/validate_examples.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

To validate a package at a supplied authoritative graph revision:

```sh
python3 scripts/validate_package.py source/examples/retention-change/change-package.yaml \
  --at 2026-10-21T12:00:00Z --current-rev 184
```

The supplied revision is an input to the local validator, not a Maysano query. A different revision returns `graph-drift`. Maysano remains responsible for write-time revision, authority, graph-state, and authoritative-evidence validation.

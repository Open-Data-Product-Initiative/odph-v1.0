# Business Harness Model

ODPH v0.2 packages eight peer top-level object kinds around versioned ODPC, ODPS, and ODPG YAML specifications. The package view groups them by the question they answer: **Business Need** (`ContextPackage`, `Mandate`, `WorkEnvelope`), **Actions** (`ExecutionRequest`, `ChangeTask`, `ChangeAction`, and optional `ExecutionPackage`), and **Evidence** (`EvidenceEvent`). It does not replace business-object, graph, or Maysano record authority.

Maysano is authoritative for accepted specification versions, object identities, graph state, approvals, applied changes, and audit evidence. ODPH retrieves bounded context, creates and validates one specification file at a time, obtains business-owner agreement, submits that file to Maysano, and records evidence.

## Repository structure

- `source/index.html.md`: v0.2 overview and links to the published documentation set.
- `source/odph-v0.2/schema/change-control.yaml`: canonical ChangeAction/ChangeTask schema published at `/odph-v0.2/schema/change-control.yaml`.
- `source/odph-v0.2/schema/change-control.json`: generated JSON representation.
- `source/examples/change-chain/`: six linked change-chain test cases, actions, a composite Change Task, and referenced ODPC, ODPS, and ODPG files.
- `scripts/validate_examples.py`: complete static and cross-file example validation.
- `source/objects.jsonl`: machine-readable definitions for the eight v0.2 top-level object kinds.

## Local checks

```sh
python -m pip install -r scripts/requirements-agent.txt
python scripts/generate_artifacts.py --check
python scripts/check_agent_artifacts.py
python scripts/validate_examples.py
python -m unittest discover -s tests
bundle exec middleman build
```

Direct workflows are ordered Maysano resource writes. They do not claim multi-action atomicity or automatic rollback, and they do not replace Maysano’s system-of-record role.

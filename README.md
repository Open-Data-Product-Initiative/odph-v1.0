# ODPH v0.2 Draft: Kentaro Change Control

ODPH v0.2 is a thin Kentaro change-control layer around versioned ODPC, ODPS, and ODPG YAML specifications. It does not model business objects, graph connections, runtime execution, or an alternate record store.

Maysano is authoritative for accepted specification versions, object identities, graph state, approvals, applied changes, and audit evidence. Kentaro retrieves bounded context, creates and validates one specification file at a time, obtains business-owner agreement, submits that file to Maysano, and records evidence.

## Repository structure

- `source/index.html.md`: v0.2 overview and links to the published documentation set.
- `source/odph-v0.2/schema/kentaro-change.yaml`: canonical KentaroAction/KentaroChangeTask schema published at `/odph-v0.2/schema/kentaro-change.yaml`.
- `source/odph-v0.2/schema/kentaro-change.json`: generated JSON representation.
- `source/examples/change-chain/`: six linked change-chain test cases, actions, a composite Change Task, and referenced ODPC, ODPS, and ODPG files.
- `scripts/validate_examples.py`: complete static and cross-file example validation.
- `source/objects.jsonl`: machine-readable definitions for the two v0.2 document kinds.

## Local checks

```sh
python -m pip install -r scripts/requirements-agent.txt
python scripts/generate_artifacts.py --check
python scripts/check_agent_artifacts.py
python scripts/validate_examples.py
python -m unittest discover -s tests
bundle exec middleman build
```

Direct workflows are ordered Maysano resource writes. They do not claim multi-action atomicity or automatic rollback. MCP is planned only for v0.3; it does not replace Maysano APIs or Maysano’s system-of-record role.

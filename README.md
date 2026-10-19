# Governed Work Package (GWP) 0.1 Draft

This repository contains non-ratified design material for a governed work package: a bounded, evidence-oriented interchange model for human and agent work.

GWP references authoritative product, portfolio, graph, platform, or internal sources; it does not duplicate their authority or grant external execution permission. A local `allowed` result means only that an action is structurally within supplied local objects.

## Repository structure

- `source/index.html.md`: human-readable specification in the existing three-column Slate layout.
- `source/schema/gwp.yaml`: canonical YAML serialization of JSON Schema.
- `source/schema/gwp.json`: generated JSON Schema.
- `source/examples/`: minimal, full, and standalone synthetic examples.
- `source/objects.jsonl`: one machine-readable object definition per line.
- `source/llms.txt`: agent discovery, modelling, and safety guidance.

## Local checks

```sh
python scripts/generate_artifacts.py --check
python scripts/check_agent_artifacts.py
python -m unittest discover -s tests
bundle exec middleman build
```

Schema validation checks document shape. Cross-object subset, authority-chain, freshness, and outcome rules need deterministic relationship evaluation in addition to JSON Schema.

# Open Data Product Harness

ODPH v0.2 is a draft specification for one Change Package that carries a business need through controlled company-graph work and evidence.

The canonical schema is [`source/odph-v0.2/schema/change-package.yaml`](source/odph-v0.2/schema/change-package.yaml). The complete retention example is [`source/examples/retention-change/change-package.yaml`](source/examples/retention-change/change-package.yaml).

## Checks

```sh
python3 scripts/generate_artifacts.py --check
python3 scripts/check_agent_artifacts.py
python3 scripts/validate_examples.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

The local validator accepts a supplied graph revision; it does not query or write Maysano.

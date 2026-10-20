---
title: ODPH v0.2 Draft | Kentaro Change Control
---

# ODPH v0.2 Draft

## A thin Kentaro change-control layer

ODPH v0.2 controls proposed changes around versioned business specifications. It does not remodel objectives, use cases, data products, graph connections, or runtime execution objects.

<aside class="warning">This is pre-release material. Direct v0.2 workflows perform ordered, resource-level Maysano writes. They are not multi-action atomic and do not roll back automatically.</aside>

| Document | Use it for | It contains |
| --- | --- | --- |
| [`KentaroAction`](kentaro-action.html) | One agreed direct Maysano API operation. | One reference to one ODPC, ODPS, or ODPG YAML file. |
| [`KentaroChangeTask`](kentaro-change-task.html) | A later composite business change. | References to existing action files and their dependencies. |

## Documentation

- [Architecture and responsibilities](architecture.html)
- [KentaroAction reference](kentaro-action.html)
- [KentaroChangeTask reference](kentaro-change-task.html)
- [Specification artefacts: ODPC, ODPS, ODPG](specification-artefacts.html)
- [Guided workflow execution](guided-workflow.html)
- [Change Task execution](change-task-execution.html)
- [Banking mortgage-renewal test chain](mortgage-renewal.html)
- [Schema reference](schema-reference.html)
- [Validation and runtime checks](validation.html)
- [Roadmap](roadmap.html)

## Published contract and examples

The canonical YAML schema is [`kentaro-change.yaml`](odph-v0.2/schema/kentaro-change.yaml); the mechanically derived JSON representation is [`kentaro-change.json`](odph-v0.2/schema/kentaro-change.json). Both use the v0.2 schema identifier `https://opendataproducts.org/odph-v0.2/schema/kentaro-change.yaml`.

The linked mortgage-renewal example bundle is under [`examples/mortgage-renewal/`](examples/mortgage-renewal/). It contains sixteen individually validated `KentaroAction` files, one later composite `KentaroChangeTask`, and the referenced ODPC, ODPS, and ODPG files.

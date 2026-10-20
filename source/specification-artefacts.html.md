---
title: Specification artefacts | ODPH v0.2
---

# Specification artefacts: ODPC, ODPS, ODPG

`KentaroAction.specification` is a file reference, not a business-object envelope.

| Family | Carries | Validated against |
| --- | --- | --- |
| `ODPC` | Objective or use-case definitions and their business semantics. | ODPC schema |
| `ODPS` | Data-product definition, lifecycle, SLA, and data-quality terms. | ODPS schema |
| `ODPG` | Nodes and connections between objectives, use cases, and data products. | ODPG graph schema |

ODPG is the declared connection artefact. Connections are not raw relationship JSON. The mortgage-renewal graph versions show the progression from the first objective/use-case connection to the later outreach planning graph.

Every referenced file must be a contained relative `.yaml` or `.yml` path and must match the SHA-256 checksum in its action. The [validation guide](validation.html) describes the static and runtime checks.

---
title: Architecture and responsibilities | ODPH v0.2
---

# Architecture and responsibilities

Maysano is the authoritative record for accepted specification versions, object identities, graph state, approvals, applied changes, and audit evidence. Kentaro retrieves bounded Maysano context; creates and validates specification files; presents a proposed change to the business owner; submits agreed files to Maysano; and records evidence. Kentaro is not a second record store.

| Concern | Authoritative location |
| --- | --- |
| Data-product definition | ODPS YAML and the ODPS schema |
| Objective and use-case definition | ODPC YAML and the ODPC schema |
| Connections | ODPG YAML graph specification and the ODPG schema |
| Accepted identity, version, approval, graph state, applied change | Maysano |
| Generated file validation, proposal presentation, submission evidence | Kentaro |

ODPH v0.2 only names a file, its family, checksum, bounded Maysano context, review needs, and acceptance criteria. Object identity, business fields, domain semantics, and lifecycle state belong in the referenced ODPC, ODPS, or ODPG file.

There are no generic object payloads, generic relationship payloads, raw relationship JSON, API request bodies, authority levels, tool lists, data-access grants, or runtime-cache details in this contract.

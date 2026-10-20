---
title: ODPH v0.2 Draft | Kentaro Change Control
search: true
---

# ODPH v0.2 Draft

## Overview

ODPH v0.2 controls proposed changes around versioned business specifications. It does not remodel objectives, use cases, data products, graph connections, or runtime execution objects.

<aside class="warning">This is pre-release material. Direct v0.2 workflows perform ordered, resource-level Maysano writes. They are not multi-action atomic and do not roll back automatically.</aside>

# Architecture and responsibilities

## Authority boundary

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

# KentaroAction

## Direct specification change

A `KentaroAction` is one agreed direct Maysano API operation. It references exactly one generated specification file and Kentaro validates that file against the declared ODPC, ODPS, or ODPG schema before submitting it.

`operation` is only `create` or `update`. An `update` requires `expectedVersion`. A connection change is an ODPG file update. A deprecation is a new ODPC or ODPS file version with its lifecycle state changed. A business-object update is a new ODPC or ODPS file version. `link`, `unlink`, and `deprecate` are not KentaroAction operations.

The action cannot embed or duplicate the referenced specification’s object fields. See the complete [schema reference](#schema-reference) and the [first guided workflow](#guided-workflow-execution).

# KentaroChangeTask

## Composite change planning

A `KentaroChangeTask` is a later v0.2 composite business change. It groups multiple existing `KentaroAction` files and declares their dependencies. It does not embed, copy, or recreate ODPC, ODPS, or ODPG content.

It records the bounded Maysano graph revision, action-file references, dependencies, required reviewers, acceptance criteria, execution status, and resulting evidence. Static validation rejects a task with fewer than two actions or unknown fields. Runtime validation rejects missing action files, duplicate action IDs, missing dependencies, and dependency cycles.

The [mortgage-renewal planning Change Task](examples/mortgage-renewal/change-tasks/mortgage-renewal-planning-change.yaml) is the composite example.

# Specification artefacts

## ODPC, ODPS, and ODPG

`KentaroAction.specification` is a file reference, not a business-object envelope.

| Family | Carries | Validated against |
| --- | --- | --- |
| `ODPC` | Objective or use-case definitions and their business semantics. | ODPC schema |
| `ODPS` | Data-product definition, lifecycle, SLA, and data-quality terms. | ODPS schema |
| `ODPG` | Nodes and connections between objectives, use cases, and data products. | ODPG graph schema |

ODPG is the declared connection artefact. Connections are not raw relationship JSON. The mortgage-renewal graph versions show the progression from the first objective/use-case connection to the later outreach planning graph.

Every referenced file must be a contained relative `.yaml` or `.yml` path and must match the SHA-256 checksum in its action. The [validation guide](#validation-and-runtime-checks) describes the static and runtime checks.

# Guided workflow execution

## Direct Maysano writes

Phase 1 v0.2 creates and submits one validated specification file at a time through Maysano resource APIs.

For the first mortgage-renewal test case the direct flow is:

1. Kentaro retrieves bounded Maysano graph context.
2. The business owner agrees the objective draft.
3. Kentaro creates and validates an ODPC objective YAML file.
4. Kentaro sends that validated file to Maysano.
5. Kentaro reads the returned objective identity and version.
6. The business owner agrees the use-case draft.
7. Kentaro creates and validates an ODPC use-case YAML file.
8. Kentaro sends that validated file to Maysano.
9. Kentaro creates and validates an ODPG graph specification connecting objective and use case.
10. Kentaro sends that graph file to Maysano.
11. Kentaro records evidence for each completed action.

Direct workflows use ordered resource-level writes. There is no multi-action atomicity, automatic rollback, or all-or-nothing execution claim. If an action fails, Kentaro stops and records completed actions, pending actions, returned Maysano identities and versions, the failure reason, and required reconciliation work.

# Change Task execution

## Declared dependency order

Phase 2 later v0.2 validates a complete Change Task before execution. The initial implementation still sends individual Maysano API calls in declared dependency order; the task does not grant server-side atomic execution.

The composite mortgage-renewal planning example creates one objective, one use case, two data products, reuses the existing Mortgage Renewal Customer Profile, and updates one ODPG graph specification that expresses the new connections. Before each write Kentaro verifies the agreed approvals, applicable object versions, and current graph revision. It records each submitted file identifier, Maysano identity and version, validation outcome, and reconciliation state.

# Banking mortgage-renewal test chain

## Validated example bundle

The principal v0.2 examples are linked source files in [`examples/mortgage-renewal/`](examples/mortgage-renewal/). The actions refer to their specification files from the bundle root so every reference remains contained.

| Test case | Expected specification artefacts |
| --- | --- |
| 01 | ODPC objective v1; ODPC use case v1; ODPG graph v1 |
| 02 | ODPS Mortgage Renewal Eligibility v1; ODPG graph v2 |
| 03 | ODPS Mortgage Renewal Eligibility v2 with revised SLA and DQ terms |
| 04 | ODPC second use case v1; ODPG graph v3 |
| 05 | ODPS Mortgage Renewal Customer Profile v1; ODPS Mortgage Renewal Eligibility v3, deprecated; ODPG graph v4 |
| 06 | ODPC new objective v1; ODPC new use case v1; ODPS Mortgage Renewal Offer Eligibility v1; ODPS Mortgage Outreach Capacity Forecast v1; ODPG graph v5 |

Test cases 01–05 demonstrate direct actions. Test case 06 also provides the later composite `KentaroChangeTask`, which references its five separately valid action files and uses dependencies to order the individual resource writes.

# Schema reference

## Common fields

The canonical v0.2 contract is [`kentaro-change.yaml`](odph-v0.2/schema/kentaro-change.yaml). `additionalProperties: false` is intentional at every Kentaro document object: unknown top-level or nested fields fail validation.

Both document kinds require `schema`, `version`, `kind`, `metadata`, `graphContext`, `intent`, `review`, and `acceptanceCriteria`.

| Field | Type and allowed values | Requirement |
| --- | --- | --- |
| `schema` | String. `https://opendataproducts.org/odph-v0.2/schema/kentaro-change.yaml` or `.json`. | Required. |
| `version` | Exact string `0.2-draft`. | Required. |
| `kind` | `KentaroAction` or `KentaroChangeTask`. | Required; selects the document kind. |
| `metadata` | Object. | Required. |
| `graphContext` | Object. | Required. |
| `intent` | Object. | Required. |
| `review` | Object. | Required. |
| `acceptanceCriteria` | Array of one or more non-empty strings. | Required. |

### `metadata`

Required: `id`, `title`, `requestedBy`, `createdAt`. `id` is a string of 3–128 characters matching `^[a-z0-9][a-z0-9-]*$`. `title` and `requestedBy` are non-empty strings; `createdAt` is an RFC 3339 date-time string. Optional `parentTestCase` and `parentChangeTask` use the same identifier rule.

### `graphContext`

Required: `source: maysano` and `baseGraphRevision`, which is a non-negative integer or non-empty string. Optional `requiredObjects` is an array of object references. Each reference requires `id` (identifier) and `expectedVersion` (non-negative integer or non-empty string), and may declare `specificationFamily` as `ODPC`, `ODPS`, or `ODPG`.

### `intent` and `review`

`intent` requires non-empty `businessOwner`, `reason`, and `expectedOutcome`, plus `policyProfile`, which uses the identifier rule. `review.requiredRoles` is a non-empty, unique array of non-empty strings. `review.approvalExpiresAt` is optional and uses the date-time format.

## `KentaroAction.specification`

`KentaroAction` additionally requires `specification`.

| Field | Type and allowed values | Requirement |
| --- | --- | --- |
| `operation` | `create` or `update`. | Required. `update` requires `expectedVersion`. |
| `family` | `ODPC`, `ODPS`, or `ODPG`. | Required. |
| `file` | Relative YAML filename ending `.yaml` or `.yml`; it cannot start with `/` or contain `..` traversal. | Required. |
| `sha256` | Exactly 64 hexadecimal characters. | Required. |
| `expectedVersion` | Non-negative integer or non-empty string. | Required only for `update`. |

The referenced file carries the object identity, business fields, and domain semantics. The action does not duplicate them.

## `KentaroChangeTask.actions`

`KentaroChangeTask` additionally requires `actions`: an array with at least two references. Every reference requires `id` and `actionFile`; `actionFile` has the same contained relative-YAML rule as `specification.file`. Optional `dependsOn` is an array of unique action IDs in the same task. Runtime validation rejects missing references, duplicate action IDs, and dependency cycles.

## Deliberate v0.2 limits

The schema has no `ContextPackage`, `Mandate`, `WorkEnvelope`, `ExecutionPackage`, `ExecutionRequest`, `EvidenceEvent`, `Correction`, `RevocationPolicy`, `tools`, `dataAccess`, `approvalRights`, `authorityLevel`, runtime-cache details, API request bodies, generic object payloads, or generic relationship payloads. It does not embed ODPC, ODPS, or ODPG content, and it does not add generic `link`, `unlink`, or `deprecate` operations.

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

# Roadmap

## Delivery direction

| Phase | Direction |
| --- | --- |
| v0.2 Phase 1 | Guided, object-level workflows using one `KentaroAction` and one validated specification file per Maysano resource write. |
| v0.2 Phase 2 | Validated `KentaroChangeTask` orchestration that still executes through individual Maysano API calls. |
| v0.3 | Planned MCP interface to Kentaro capabilities: `kentaro.create_change_task`, `kentaro.validate_change_task`, `kentaro.submit_change_task`, and `kentaro.get_change_task_status`. MCP does not replace Maysano APIs or become the record store. |
| Future | Maysano-native composite execution may add server-side validation, locking, atomic execution, and grouped audit. This is not required for v0.2. |

# Published contract and examples

## Machine-readable sources

The canonical YAML schema is [`kentaro-change.yaml`](odph-v0.2/schema/kentaro-change.yaml); the mechanically derived JSON representation is [`kentaro-change.json`](odph-v0.2/schema/kentaro-change.json). Both use the v0.2 schema identifier `https://opendataproducts.org/odph-v0.2/schema/kentaro-change.yaml`.

The linked mortgage-renewal example bundle is under [`examples/mortgage-renewal/`](examples/mortgage-renewal/). It contains sixteen individually validated `KentaroAction` files, one later composite `KentaroChangeTask`, and the referenced ODPC, ODPS, and ODPG files.

---
title: Business Harness Model
search: true
---

# Business Harness Model

## Overview

ODPH v0.2 governs bounded change work around versioned business specifications. A delivery packages independently addressable top-level objects: the six governed-work objects below plus `ChangeAction` and `ChangeTask`. A conforming implementation must make the six concerns visible before it represents a business change as ready to submit.

<aside class="warning">This is pre-release material. Direct v0.2 workflows perform ordered, resource-level Maysano writes. They are not multi-action atomic and do not roll back automatically.</aside>

# The six aspects of governed change work

## A task is only one part of the model

The six aspects are top-level object kinds, not six peer fields copied into every YAML document. They keep a change request from becoming an unbounded task list. `ChangeAction` and `ChangeTask` are peer top-level object kinds: the action declares one direct specification change, while the task packages a dependency-ordered composite change. Maysano remains the authority for accepted records, approvals, applied changes, and audit evidence; ODPH prepares, validates, presents, submits, and links the resulting evidence.

```text
bounded source context
        |
ContextPackage -> Mandate -> WorkEnvelope -> ExecutionPackage -> ExecutionRequest
                                                               |
                                EvidenceBundle <- receipts, outcomes, reconciliation
```

| Aspect | Question it answers | v0.2 expression | It must not become |
| --- | --- | --- | --- |
| `ContextPackage` | What was known, from which versions, and how fresh was it? | Bounded Maysano graph revision, required object versions, source provenance, and reported conflicts. | A shadow copy of the portfolio. |
| `Mandate` | What is the durable business boundary for this area? | The accountable business owner and applicable policy profile, backed by Maysano approval and policy records. | A task-level permission or an implicit tool grant. |
| `WorkEnvelope` | What narrowly bounded assignment is permitted now? | Requested result, scope, exclusions, review roles, expiry, and acceptance conditions for this change. | A way to expand the mandate. |
| `ExecutionPackage` | What coordinated plan will meet that assignment? | A plan with steps, dependencies, expected outcomes, and acceptance criteria. | Independent authority or an autonomous runbook. |
| `ExecutionRequest` | Which single external write is proposed? | An explicit proposal bound to its plan and revocation policy. | An implicit command or embedded business content. |
| `EvidenceBundle` | What proves what was considered, decided, attempted, and returned? | Validation results, approvals, submitted-file identifiers, Maysano identities and versions, outcomes, and reconciliation state. | A claim of immutable retention or a second system of record. |

The six aspects have a strict direction: context informs the boundary; the mandate limits the assignment; the assignment limits the plan; the plan limits each proposed write; and evidence records the result. A task that lacks any of those links is incomplete even if its YAML is structurally valid.

# ContextPackage

A `ContextPackage` is a bounded observation, not a copied catalog. It identifies the retrieval scope, source IDs and versions, retrieval time, freshness, and observed conflicts. Every source observation is attributable to a version and retrieval time; stale or contradictory input must be made visible for human resolution.

| Attribute | Structure | Purpose |
| --- | --- | --- |
| `id`, `kind`, `version`, `createdAt`, `actor` | Common object identity and attribution. `kind` is `ContextPackage`. | Makes this particular observation addressable and attributable. |
| `sourceReferences` | Array of `{id, version, retrievedAt}` references. | Identifies the bounded evidence consulted. |
| `relationshipReferences` | Array of `{id, version}` references. | Links the context to related governed objects without copying them. |
| `retrievalScope` | Object describing the retrieved objectives, use cases, data products, graph, or other source slice. | Declares what was looked at. |
| `freshness` | `fresh`, `stale`, or `unknown`. | Prevents unqualified reuse of old context. |
| `conflicts` | Array of observed conflicts or an empty array. | Records what must be resolved; empty means none observed in this snapshot. |

```yaml
id: context-service-change
kind: ContextPackage
version: 1
createdAt: "2026-10-20T00:00:00Z"
actor: change-team
sourceReferences:
  - {id: maysano:graph, version: 4, retrievedAt: "2026-10-20T00:00:00Z"}
relationshipReferences: []
retrievalScope: {graphRevision: 4, objectiveIds: [service-objective]}
freshness: fresh
conflicts: []
```

# Mandate

A `Mandate` is the durable business boundary for an area of work. It names the accountable owner, permitted scope, tools, data access, review rights, authority level, and expiry. ODPH does not mint authority: a local policy match never grants connector, credential, data-access, or external-write rights.

| Attribute | Structure | Purpose |
| --- | --- | --- |
| Common identity and references | `id`, `kind: Mandate`, `version`, `createdAt`, `actor`, `sourceReferences`, `relationshipReferences`. | Stable attribution and links. |
| `businessArea`, `owner` | Non-empty strings. | Names the durable area and accountable person or role. |
| `scope`, `tools`, `dataAccess`, `approvalRights` | Arrays of non-empty strings. | Defines the outer permitted boundary. |
| `authorityLevel` | Local integer `0`–`3`; it has no portable cross-organisation meaning. | Supports local comparison only. |
| `expiresAt` | RFC 3339 timestamp. | Makes the boundary reviewable and finite. |

```yaml
id: mandate-service-change
kind: Mandate
version: 1
createdAt: "2026-10-20T00:00:00Z"
actor: service-owner
sourceReferences: []
relationshipReferences: []
businessArea: Service planning
owner: Head of Service
scope: [service-change]
tools: [maysano.change-proposal]
dataAccess: [service-planning-context]
approvalRights: [reviewed-change-proposal]
authorityLevel: 1
expiresAt: "2027-01-01T00:00:00Z"
```

# WorkEnvelope

A `WorkEnvelope` narrows one mandate into one assignment. It states the requested result, accountable owner, allowed subset, and expiry. It may narrow a mandate but must never broaden it; relationship validation must reject a missing mandate version or an expanded boundary.

| Attribute | Structure | Purpose |
| --- | --- | --- |
| Common identity and references | `id`, `kind: WorkEnvelope`, `version`, `createdAt`, `actor`, `sourceReferences`, `relationshipReferences`. | Stable attribution and links. |
| `mandateReference` | `{id, version}` reference to exactly one `Mandate`. | Establishes the durable boundary being narrowed. |
| `requestedResult`, `owner` | Non-empty strings. | States the expected assignment result and accountable owner. |
| Boundary fields | `scope`, `tools`, `dataAccess`, `approvalRights`, `authorityLevel`. | Must be a subset of the referenced mandate. |
| `expiresAt` | RFC 3339 timestamp. | Defines the assignment review horizon. |

```yaml
id: envelope-service-change
kind: WorkEnvelope
version: 1
createdAt: "2026-10-20T00:00:00Z"
actor: service-owner
sourceReferences: []
relationshipReferences: [{id: mandate-service-change, version: 1}]
mandateReference: {id: mandate-service-change, version: 1}
requestedResult: Reviewed service change proposal
owner: Head of Service
scope: [service-change]
tools: [maysano.change-proposal]
dataAccess: [service-planning-context]
approvalRights: [reviewed-change-proposal]
authorityLevel: 1
expiresAt: "2026-12-01T00:00:00Z"
```

# ExecutionPackage

An `ExecutionPackage` is the non-authoritative plan under one work envelope. It describes steps, dependencies, expected outputs, timing, and acceptance criteria. It can be associated with a `ChangeTask`, but neither object replaces the other: the package governs plan scope; the task governs a composite change.

| Attribute | Structure | Purpose |
| --- | --- | --- |
| Common identity and references | `id`, `kind: ExecutionPackage`, `version`, `createdAt`, `actor`, `sourceReferences`, `relationshipReferences`. | Stable attribution and links. |
| `workEnvelopeReference` | `{id, version}` reference to exactly one `WorkEnvelope`. | Binds the plan to its assignment. |
| Boundary fields | `scope`, `tools`, `dataAccess`, `approvalRights`, `authorityLevel`. | Must not exceed the envelope. |
| `plannedSteps`, `dependencies` | Ordered / unordered arrays of non-empty strings. | Makes the plan and its prerequisites reviewable. |
| `expectedOutputs`, `timing`, `acceptanceCriteria` | Output list, non-empty timing string, and criteria list. | States what good completion looks like. |

```yaml
id: package-service-change
kind: ExecutionPackage
version: 1
createdAt: "2026-10-20T00:00:00Z"
actor: change-team
sourceReferences: []
relationshipReferences: [{id: envelope-service-change, version: 1}]
workEnvelopeReference: {id: envelope-service-change, version: 1}
scope: [service-change]
tools: [maysano.change-proposal]
dataAccess: [service-planning-context]
approvalRights: [reviewed-change-proposal]
authorityLevel: 1
plannedSteps: [Validate context, Prepare the proposed specification, Request review]
expectedOutputs: [Reviewed service change proposal]
dependencies: [Current Maysano graph]
timing: Before the service review
acceptanceCriteria: [Names version expectations and unresolved conflicts]
```

# ExecutionRequest

An `ExecutionRequest` is one explicit proposed external action, never an implicit command. It points to its plan and the revocation policy that protects its authority chain. It can be packaged with a `ChangeAction` for one Maysano resource write. Passing local validation is not permission to dispatch automatically.

| Attribute | Structure | Purpose |
| --- | --- | --- |
| Common identity and references | `id`, `kind: ExecutionRequest`, `version`, `createdAt`, `actor`, `sourceReferences`, `relationshipReferences`. | Stable attribution and links. |
| `executionPackageReference` | `{id, version}` reference. | Binds the request to an approved plan. |
| `revocationPolicyReference` | `{id, version}` reference. | Binds a future executable request to its suspension and restoration path. |
| `action`, `tool`, `target` | Non-empty strings. | Declares exactly what is proposed. |
| `requestedAuthority`, `approvalRequired`, `approvalExpiresAt` | Local authority level, boolean approval gate, timestamp or `null`. | Makes authority and time limits explicit. |
| `redactedParameters` | Object; never raw secrets. | Carries only safe, referential request context. |

```yaml
id: request-service-change
kind: ExecutionRequest
version: 1
createdAt: "2026-10-20T00:00:00Z"
actor: change-team
sourceReferences: []
relationshipReferences: [{id: package-service-change, version: 1}]
executionPackageReference: {id: package-service-change, version: 1}
revocationPolicyReference: {id: policy-service-change, version: 1}
action: submit reviewed service specification
tool: maysano.change-proposal
target: service planning graph
requestedAuthority: 1
approvalRequired: true
approvalExpiresAt: "2026-12-01T00:00:00Z"
redactedParameters: {contextReference: context-service-change}
```

# EvidenceEvent

An `EvidenceEvent` is the durable atomic record; an `EvidenceBundle` is an exportable grouping of its events. The event links a work envelope to attributable proof of context retrieval, validation, review, submission, returned state, failure, correction, or reconciliation. A local export is not a claim of immutable platform retention.

| Attribute | Structure | Purpose |
| --- | --- | --- |
| Common identity and references | `id`, `kind: EvidenceEvent`, `version`, `createdAt`, `actor`, `sourceReferences`, `relationshipReferences`. | Stable attribution and source provenance. |
| `occurredAt` | RFC 3339 timestamp. | Records when the event happened. |
| `workEnvelopeReference` | `{id, version}` reference. | Associates proof with one bounded assignment. |
| `eventType` | Extensible non-empty string. | Names the event, such as `context_retrieved` or `validation_completed`. |
| `payload` | Object. | Carries structured, non-secret event details and authoritative receipt references. |

```yaml
id: evidence-context-retrieved
kind: EvidenceEvent
version: 1
createdAt: "2026-10-20T00:00:00Z"
occurredAt: "2026-10-20T00:00:00Z"
actor: change-team
sourceReferences:
  - {id: maysano:graph, version: 4, retrievedAt: "2026-10-20T00:00:00Z"}
relationshipReferences: [{id: envelope-service-change, version: 1}]
workEnvelopeReference: {id: envelope-service-change, version: 1}
eventType: context_retrieved
payload: {contextPackageReference: {id: context-service-change, version: 1}}
```

# Architecture and responsibilities

## Authority boundary

Maysano is the authoritative record for accepted specification versions, object identities, graph state, approvals, applied changes, and audit evidence. ODPH retrieves bounded Maysano context; creates and validates specification files; presents a proposed change to the business owner; submits agreed files to Maysano; and records evidence. ODPH is not a second record store.

| Concern | Authoritative location |
| --- | --- |
| Data-product definition | ODPS YAML and the ODPS schema |
| Objective and use-case definition | ODPC YAML and the ODPC schema |
| Connections | ODPG YAML graph specification and the ODPG schema |
| Accepted identity, version, approval, graph state, applied change | Maysano |
| Generated file validation, proposal presentation, submission evidence | ODPH |

ODPH v0.2 serializes all eight top-level object kinds. A delivery must connect the objects instead of pretending that a task or action is self-sufficient. Object identity, business fields, domain semantics, and lifecycle state belong in the referenced ODPC, ODPS, or ODPG file.

There are no raw relationship JSON, API request bodies, or runtime-cache details in this contract. Boundary fields declare a local governed-work model; they do not issue real tools, data access, approval rights, or authority.

# ChangeAction

## Direct specification change

A `ChangeAction` is a peer top-level object for one agreed direct Maysano API operation. It references exactly one generated specification file and ODPH validates that file against the declared ODPC, ODPS, or ODPG schema before submitting it. It can be packaged with an `ExecutionRequest`, but it does not replace that request's plan, revocation, or approval chain.

`operation` is only `create` or `update`. An `update` requires `expectedVersion`. A connection change is an ODPG file update. A deprecation is a new ODPC or ODPS file version with its lifecycle state changed. A business-object update is a new ODPC or ODPS file version. `link`, `unlink`, and `deprecate` are not ChangeAction operations.

| Attribute | Structure | Purpose |
| --- | --- | --- |
| `schema`, `version`, `kind` | v0.2 schema identifier, `0.2-draft`, and `ChangeAction`. | Identifies the action contract. |
| `metadata` | `id`, title, requester, creation time, and optional parent identifiers. | Stable action identity and provenance. |
| `graphContext` | Maysano graph revision plus optional required object versions. | Pins the context against which the write is safe. |
| `intent` | Business owner, reason, expected outcome, and policy profile. | Links the write to a business purpose. |
| `specification` | `create` or `update`, family, contained YAML file, SHA-256, and update version where relevant. | Names exactly one separately validated standard-family artefact. |
| `review`, `acceptanceCriteria` | Required roles, optional approval expiry, and one or more criteria. | Makes the human review gate explicit. |

```yaml
schema: https://opendataproducts.org/odph-v0.2/schema/change-control.yaml
version: 0.2-draft
kind: ChangeAction
metadata: {id: create-service-objective, title: Create service objective, requestedBy: Change Team, createdAt: '2026-10-20T00:00:00Z'}
graphContext: {source: maysano, baseGraphRevision: 4}
intent: {businessOwner: Head of Service, reason: Establish a reviewed service objective, expectedOutcome: Accepted objective version, policyProfile: service-change}
specification: {operation: create, family: ODPC, file: specifications/odpc/service-objective-v1.yaml, sha256: 9a8b0c06bb51226e0a30a2c7f79ef43f378c9bf913ac3489928ccfe341c593f2}
review: {requiredRoles: [Head of Service]}
acceptanceCriteria: [Objective is accepted by Maysano]
```

The action cannot embed or duplicate the referenced specification’s object fields. See the complete [schema reference](#schema-reference) and the [first guided workflow](#guided-workflow-execution).

# ChangeTask

## Composite change planning

A `ChangeTask` is a peer top-level object for a composite business change. It groups multiple existing `ChangeAction` files and declares their dependencies. It does not embed, copy, or recreate ODPC, ODPS, or ODPG content, and it does not replace the context, mandate, work-envelope, execution-package, execution-request, or evidence responsibilities.

It records the bounded Maysano graph revision, action-file references, dependencies, required reviewers, acceptance criteria, execution status, and resulting evidence. Static validation rejects a task with fewer than two actions or unknown fields. Runtime validation rejects missing action files, duplicate action IDs, missing dependencies, and dependency cycles.

| Attribute | Structure | Purpose |
| --- | --- | --- |
| `schema`, `version`, `kind` | v0.2 schema identifier, `0.2-draft`, and `ChangeTask`. | Identifies the task contract. |
| `metadata`, `graphContext`, `intent` | Same structures as `ChangeAction`. | Establishes provenance, bounded context, and business purpose. |
| `actions` | At least two `{id, actionFile, dependsOn?}` references. | Packages independently valid actions and their declared order. |
| `review`, `acceptanceCriteria` | Required roles, optional approval expiry, and one or more criteria. | Holds the composite review gate. |

```yaml
schema: https://opendataproducts.org/odph-v0.2/schema/change-control.yaml
version: 0.2-draft
kind: ChangeTask
metadata: {id: service-change, title: Service change, requestedBy: Change Team, createdAt: '2026-10-20T00:00:00Z'}
graphContext: {source: maysano, baseGraphRevision: 4}
intent: {businessOwner: Head of Service, reason: Deliver the reviewed service change, expectedOutcome: Accepted change chain, policyProfile: service-change}
actions:
  - {id: create-service-objective, actionFile: actions/create-service-objective.yaml}
  - {id: update-service-graph, actionFile: actions/update-service-graph.yaml, dependsOn: [create-service-objective]}
review: {requiredRoles: [Head of Service]}
acceptanceCriteria: [All actions reconcile with returned Maysano versions]
```

The [example Change Task](examples/change-chain/change-tasks/change-chain.yaml) is the composite example.

# Specification artefacts

## ODPC, ODPS, and ODPG

`ChangeAction.specification` is a file reference, not a business-object envelope.

| Family | Carries | Validated against |
| --- | --- | --- |
| `ODPC` | Objective or use-case definitions and their business semantics. | ODPC schema |
| `ODPS` | Data-product definition, lifecycle, SLA, and data-quality terms. | ODPS schema |
| `ODPG` | Nodes and connections between objectives, use cases, and data products. | ODPG graph schema |

ODPG is the declared connection artefact. Connections are not raw relationship JSON. The example graph versions show the progression from an initial objective/use-case connection to a later composite change.

Every referenced file must be a contained relative `.yaml` or `.yml` path and must match the SHA-256 checksum in its action. The [validation guide](#validation-and-runtime-checks) describes the static and runtime checks.

# Guided workflow execution

## Direct Maysano writes

Phase 1 v0.2 creates and submits one validated specification file at a time through Maysano resource APIs.

For the first generic change-chain test case the direct flow is:

1. ODPH retrieves bounded Maysano graph context.
2. The business owner agrees the objective draft.
3. ODPH creates and validates an ODPC objective YAML file.
4. ODPH sends that validated file to Maysano.
5. ODPH reads the returned objective identity and version.
6. The business owner agrees the use-case draft.
7. ODPH creates and validates an ODPC use-case YAML file.
8. ODPH sends that validated file to Maysano.
9. ODPH creates and validates an ODPG graph specification connecting objective and use case.
10. ODPH sends that graph file to Maysano.
11. ODPH records evidence for each completed action.

Direct workflows use ordered resource-level writes. There is no multi-action atomicity, automatic rollback, or all-or-nothing execution claim. If an action fails, ODPH stops and records completed actions, pending actions, returned Maysano identities and versions, the failure reason, and required reconciliation work.

# Change Task execution

## Declared dependency order

Phase 2 later v0.2 validates a complete Change Task before execution. The initial implementation still sends individual Maysano API calls in declared dependency order; the task does not grant server-side atomic execution.

The composite example creates one objective, one use case, two data products, reuses an existing context data product, and updates one ODPG graph specification that expresses the new connections. Before each write ODPH verifies the agreed approvals, applicable object versions, and current graph revision. It records each submitted file identifier, Maysano identity and version, validation outcome, and reconciliation state.

# Generic change-chain example

## Validated example bundle

The principal v0.2 examples are linked source files in [`examples/change-chain/`](examples/change-chain/). The actions refer to their specification files from the bundle root so every reference remains contained.

| Test case | Expected specification artefacts |
| --- | --- |
| 01 | ODPC objective v1; ODPC use case v1; ODPG graph v1 |
| 02 | ODPS Primary Data Product v1; ODPG graph v2 |
| 03 | ODPS Primary Data Product v2 with revised SLA and DQ terms |
| 04 | ODPC second use case v1; ODPG graph v3 |
| 05 | ODPS Context Data Product v1; ODPS Primary Data Product v3, deprecated; ODPG graph v4 |
| 06 | ODPC secondary objective v1; ODPC secondary use case v1; ODPS Additional Data Product v1; ODPS Capacity Data Product v1; ODPG graph v5 |

Test cases 01–05 demonstrate direct actions. Test case 06 also provides the later composite `ChangeTask`, which references its five separately valid action files and uses dependencies to order the individual resource writes.

# Schema reference

## Common fields

The canonical v0.2 contract is [`change-control.yaml`](odph-v0.2/schema/change-control.yaml). `additionalProperties: false` is intentional at every ODPH document object: unknown top-level or nested fields fail validation.

Both document kinds require `schema`, `version`, `kind`, `metadata`, `graphContext`, `intent`, `review`, and `acceptanceCriteria`.

| Field | Type and allowed values | Requirement |
| --- | --- | --- |
| `schema` | String. `https://opendataproducts.org/odph-v0.2/schema/change-control.yaml` or `.json`. | Required. |
| `version` | Exact string `0.2-draft`. | Required. |
| `kind` | `ChangeAction` or `ChangeTask`. | Required; selects the document kind. |
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

## `ChangeAction.specification`

`ChangeAction` additionally requires `specification`.

| Field | Type and allowed values | Requirement |
| --- | --- | --- |
| `operation` | `create` or `update`. | Required. `update` requires `expectedVersion`. |
| `family` | `ODPC`, `ODPS`, or `ODPG`. | Required. |
| `file` | Relative YAML filename ending `.yaml` or `.yml`; it cannot start with `/` or contain `..` traversal. | Required. |
| `sha256` | Exactly 64 hexadecimal characters. | Required. |
| `expectedVersion` | Non-negative integer or non-empty string. | Required only for `update`. |

The referenced file carries the object identity, business fields, and domain semantics. The action does not duplicate them.

## `ChangeTask.actions`

`ChangeTask` additionally requires `actions`: an array with at least two references. Every reference requires `id` and `actionFile`; `actionFile` has the same contained relative-YAML rule as `specification.file`. Optional `dependsOn` is an array of unique action IDs in the same task. Runtime validation rejects missing references, duplicate action IDs, and dependency cycles.

## Deliberate v0.2 limits

The eight object kinds form one packageable model. Their boundary and evidence fields are intentionally declarative: they do not become raw API request bodies or authority grants. The schema does not embed ODPC, ODPS, or ODPG content, and it does not add generic `link`, `unlink`, or `deprecate` operations.

# Validation and runtime checks

## Level 1: static schema validation

- Validate `ChangeAction` and `ChangeTask` YAML against [`change-control.yaml`](odph-v0.2/schema/change-control.yaml).
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

`validate_examples.py` uses the Open Data Products SDK schemas for ODPC, ODPS 4.2, and ODPG, verifies every referenced file and checksum, and checks the published ODPH schema locally. CI runs the same checks.

## Level 2: cross-file and runtime validation

Before a Maysano write, resolve every referenced specification file; verify the checksum; verify action references; reject duplicate action IDs and dependency cycles; verify required Maysano object versions and the current graph revision; and verify ODPC, ODPS, and ODPG files are mutually consistent. Verify approvals before every write.

Record submitted file identifiers, resulting Maysano identities and versions, validation outcomes, and reconciliation state. Maysano is authoritative for returned state; these checks do not turn ODPH into a record store.

# Roadmap

## Delivery direction

| Phase | Direction |
| --- | --- |
| v0.2 Phase 1 | Guided, object-level workflows using one `ChangeAction` and one validated specification file per Maysano resource write. |
| v0.2 Phase 2 | Validated `ChangeTask` orchestration that still executes through individual Maysano API calls. |
| v0.3 | Planned MCP interface to ODPH capabilities: `odph.create_change_task`, `odph.validate_change_task`, `odph.submit_change_task`, and `odph.get_change_task_status`. MCP does not replace Maysano APIs or become the record store. |
| Future | Maysano-native composite execution may add server-side validation, locking, atomic execution, and grouped audit. This is not required for v0.2. |

# Published contract and examples

## Machine-readable sources

The canonical YAML schema is [`change-control.yaml`](odph-v0.2/schema/change-control.yaml); the mechanically derived JSON representation is [`change-control.json`](odph-v0.2/schema/change-control.json). Both use the v0.2 schema identifier `https://opendataproducts.org/odph-v0.2/schema/change-control.yaml`.

The linked change-chain example bundle is under [`examples/change-chain/`](examples/change-chain/). It contains sixteen individually validated `ChangeAction` files, one later composite `ChangeTask`, and the referenced ODPC, ODPS, and ODPG files.

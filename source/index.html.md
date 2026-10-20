---
title: Business Harness Model
search: true
---

# Business Harness Model

## Overview

ODPH v0.2 governs bounded change work around versioned business specifications. A delivery packages independently addressable top-level objects: the six governed-work objects below plus `ChangeAction` and `ChangeTask`. A conforming implementation must make the six concerns visible before it represents a business change as ready to submit.

<aside class="warning">This is pre-release material. Direct v0.2 workflows perform ordered, resource-level Maysano writes. They are not multi-action atomic and do not roll back automatically.</aside>

# Harness package skeleton

## How the top-level objects are combined

A Business Harness package is a reviewed delivery bundle of independently valid top-level ODPH objects. The skeleton below is intentionally incomplete: it shows the composition and reference chain before the specification defines each object in detail. `package` is an authoring and delivery view, not a ninth schema kind; each object remains a separately validated top-level YAML document. Examples use block-style YAML so every semantic group, reference, and list has a visible indentation level.

```yaml
package:
  metadata:
    id: service-change-harness
    name:
      en: Reviewed service change
    description:
      en: Business Harness package for the reviewed service change.

  businessHarness:
    contextPackage:
      kind: ContextPackage
      metadata:
        id: context-service-change
        name:
          en: Current service-change context
        description:
          en: Bounded change context
        version: 1
      context:
        retrievalScope: # bounded source-specific context
        freshness: fresh
        conflicts: []

    mandate:
      kind: Mandate
      metadata:
        id: mandate-service-change
        name:
          en: Service-change mandate
        description:
          en: Durable change boundary
        version: 1
      mandate:
        businessArea: Service planning
        owner: Head of Service
      boundary: # local permissions and limits

    workEnvelope:
      kind: WorkEnvelope
      metadata:
        id: envelope-service-change
        name:
          en: Reviewed service-change assignment
        description:
          en: Bounded change assignment
        version: 1
      assignment:
        mandateReference:
          id: mandate-service-change
          version: 1
        requestedResult: # reviewed deliverable
      boundary: # narrowed local permissions and limits

  execution:
    executionPackage:
      kind: ExecutionPackage
      metadata:
        id: package-service-change
        name:
          en: Service-change execution plan
        description:
          en: Planned service-change work
        version: 1
      execution:
        workEnvelopeReference:
          id: envelope-service-change
          version: 1
      plan:
        plannedSteps: # ordered steps
        expectedOutputs: # expected results
        acceptanceCriteria: # review conditions

    executionRequest:
      kind: ExecutionRequest
      metadata:
        id: request-service-change
        name:
          en: Submit reviewed service specification
        description:
          en: Proposed external submission
        version: 1
      execution:
        executionPackageReference:
          id: package-service-change
          version: 1
        revocationPolicyReference: # policy ID and version
      request:
        action: # explicit proposed action
        approval:
          required: true
          expiresAt: # approval expiry

  evidence:
    - kind: EvidenceEvent
      metadata:
        id: evidence-context-retrieved
        name:
          en: Service-change context retrieved
        description:
          en: Recorded context retrieval
        version: 1
      evidence:
        workEnvelopeReference:
          id: envelope-service-change
          version: 1
        eventType: context_retrieved
        payload: # event-specific evidence

  changeControl:
    actions:
      - kind: ChangeAction
        specification:
          operation: create
          family: ODPC
          file: specifications/odpc/service-objective-v1.yaml
          sha256: # source file checksum
    task:
      kind: ChangeTask
      actions:
        - id: create-service-objective
          actionFile: actions/create-service-objective.yaml
```

# Model map

## How the top-level objects connect

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

# Business-level harness

### Common object contract

The six governed-work objects—`ContextPackage`, `Mandate`, `WorkEnvelope`, `ExecutionPackage`, `ExecutionRequest`, and `EvidenceEvent`—are composed with the `CommonObject` definition. Identity, human-readable purpose, and provenance are grouped rather than flattened into every object.

| Element name | Type | Options | Description |
| --- | --- | --- | --- |
| `kind` | string | Required; constrained by object definition | Discriminator for the top-level object kind. Each object table names its permitted constant value. |
| `metadata` | object | Required; closed structure | Groups object identity, human-readable purpose, and attribution. |
| `metadata.id` | string | Required; minimum length 1 | Stable identifier of this object version. The schema does not impose a global identifier pattern. |
| `metadata.name` | object | Required; one or more language keys | Human-readable, language-keyed name of the object. Each value is a non-empty string. |
| `metadata.description` | object | Required; one or more language keys | Human-readable, language-keyed description of the object’s purpose and bounded meaning. Each value is a non-empty string. |
| `metadata.version` | integer | Required; minimum `1` | Positive version of this ODPH object, used by all object references. |
| `metadata.createdAt` | string | Required; RFC 3339 `date-time` | Time at which this object version was created. |
| `metadata.actor` | string | Required; minimum length 1 | Attributed creator or producing actor. It is attribution, not authentication proof. |
| `provenance` | object | Required; closed structure | Groups source observations and relationships without embedding their contents. |
| `provenance.sourceReferences` | array of `Reference` | Required; may be empty | Versioned source observations or records used when producing the object. |
| `provenance.relationshipReferences` | array of `Reference` | Required; may be empty | Versioned links to related ODPH objects or governed records. |

### Reference

| Element name | Type | Options | Description |
| --- | --- | --- | --- |
| `id` | string | Required; minimum length 1 | Identifier of the referenced object or source. |
| `version` | integer | Required; minimum `1` | Exact referenced version. |
| `retrievedAt` | string | Optional; RFC 3339 `date-time` | Retrieval time for an observed source reference. |
| `objectType` | string | Optional | Source-specific or ODPH object-type label. |
| `uri` | string | Optional; `uri-reference` format | Relative or absolute locator for the reference. |

### Boundary

`Mandate`, `WorkEnvelope`, and `ExecutionPackage` additionally compose the `Boundary` definition under their `boundary` element.

| Element name | Type | Options | Description |
| --- | --- | --- | --- |
| `scope` | array of string | Required; items have minimum length 1 | Declared business scope. A relationship validator must ensure a child boundary does not broaden its parent. |
| `tools` | array of string | Required; items have minimum length 1 | Named local tool or capability boundary. This declaration does not grant access. |
| `dataAccess` | array of string | Required; items have minimum length 1 | Named local data-access boundary. This declaration does not grant data access. |
| `approvalRights` | array of string | Required; items have minimum length 1 | Named local approval boundary. This declaration does not confer approval rights. |
| `authorityLevel` | integer | Required; `0`–`3` | Local ordinal used for deterministic comparison only; values have no portable cross-organisation meaning. |

## ContextPackage

A `ContextPackage` is a bounded observation, not a copied catalog. It identifies the retrieval scope, source IDs and versions, retrieval time, freshness, and observed conflicts. Every source observation is attributable to a version and retrieval time; stale or contradictory input must be made visible for human resolution.

| Element name | Type | Options | Description |
| --- | --- | --- | --- |
| `kind` | string | Required; constant `ContextPackage` | Discriminator for a bounded, attributable context observation. All `CommonObject` elements are also required. |
| `context` | object | Required; closed structure | Groups the scope, freshness, and conflict statement for this observation. |
| `context.retrievalScope` | object | Required; open structure | Source-specific description of the retrieved objectives, use cases, data products, graph revision, or other bounded slice. |
| `context.freshness` | string | Required; `fresh`, `stale`, or `unknown` | Declared freshness state of this observation. It does not assert a universal source-consistency guarantee. |
| `context.conflicts` | array | Required; may be empty | Observed conflicts that need resolution. An empty array means no conflict was observed in this snapshot. |

```yaml
kind: ContextPackage
metadata:
  id: context-service-change
  name:
    en: Current service-change context
  description:
    en: Bounded Maysano graph context used to prepare the service change.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: change-team
provenance:
  sourceReferences:
    - id: maysano:graph
      version: 4
      retrievedAt: "2026-10-20T00:00:00Z"
  relationshipReferences: []
context:
  retrievalScope:
    graphRevision: 4
    objectiveIds:
      - service-objective
  freshness: fresh
  conflicts: []
```

## Mandate

A `Mandate` is the durable business boundary for an area of work. It names the accountable owner, permitted scope, tools, data access, review rights, authority level, and expiry. ODPH does not mint authority: a local policy match never grants connector, credential, data-access, or external-write rights.

| Element name | Type | Options | Description |
| --- | --- | --- | --- |
| `kind` | string | Required; constant `Mandate` | Discriminator for a durable business boundary. All `CommonObject` and `Boundary` elements are also required. |
| `mandate` | object | Required; closed structure | Groups the durable business boundary's area, owner, and review expiry. |
| `mandate.businessArea` | string | Required; minimum length 1 | Business area governed by this mandate. |
| `mandate.owner` | string | Required; minimum length 1 | Accountable owner of the durable boundary. |
| `mandate.expiresAt` | string | Required; RFC 3339 `date-time` | Time after which the mandate must be reviewed or replaced. |
| `boundary` | `Boundary` object | Required | Local scope, tool, data-access, approval, and authority constraints. |

```yaml
kind: Mandate
metadata:
  id: mandate-service-change
  name:
    en: Service-change mandate
  description:
    en: Durable business boundary for service planning changes.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: service-owner
provenance:
  sourceReferences: []
  relationshipReferences: []
mandate:
  businessArea: Service planning
  owner: Head of Service
  expiresAt: "2027-01-01T00:00:00Z"
boundary:
  scope:
    - service-change
  tools:
    - maysano.change-proposal
  dataAccess:
    - service-planning-context
  approvalRights:
    - reviewed-change-proposal
  authorityLevel: 1
```

## WorkEnvelope

A `WorkEnvelope` narrows one mandate into one assignment. It states the requested result, accountable owner, allowed subset, and expiry. It may narrow a mandate but must never broaden it; relationship validation must reject a missing mandate version or an expanded boundary.

| Element name | Type | Options | Description |
| --- | --- | --- | --- |
| `kind` | string | Required; constant `WorkEnvelope` | Discriminator for an assignment-specific boundary. All `CommonObject` and `Boundary` elements are also required. |
| `assignment` | object | Required; closed structure | Groups the assignment's parent mandate, result, owner, and expiry. |
| `assignment.mandateReference` | `Reference` object | Required | Exact ID and version of the `Mandate` being narrowed. Relationship validation rejects a missing or broadened parent boundary. |
| `assignment.requestedResult` | string | Required; minimum length 1 | Business result requested for this assignment. |
| `assignment.owner` | string | Required; minimum length 1 | Accountable owner of this assignment. |
| `assignment.expiresAt` | string | Required; RFC 3339 `date-time` | Time after which the assignment boundary is no longer valid. |
| `boundary` | `Boundary` object | Required | Local scope, tool, data-access, approval, and authority constraints. |

```yaml
kind: WorkEnvelope
metadata:
  id: envelope-service-change
  name:
    en: Reviewed service-change assignment
  description:
    en: Bounded assignment to prepare and review the service change.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: service-owner
provenance:
  sourceReferences: []
  relationshipReferences:
    - id: mandate-service-change
      version: 1
assignment:
  mandateReference:
    id: mandate-service-change
    version: 1
  requestedResult: Reviewed service change proposal
  owner: Head of Service
  expiresAt: "2026-12-01T00:00:00Z"
boundary:
  scope:
    - service-change
  tools:
    - maysano.change-proposal
  dataAccess:
    - service-planning-context
  approvalRights:
    - reviewed-change-proposal
  authorityLevel: 1
```

# Execution

## ExecutionPackage

An `ExecutionPackage` is the non-authoritative plan under one work envelope. It describes steps, dependencies, expected outputs, timing, and acceptance criteria. It can be associated with a `ChangeTask`, but neither object replaces the other: the package governs plan scope; the task governs a composite change.

| Element name | Type | Options | Description |
| --- | --- | --- |
| `kind` | string | Required; constant `ExecutionPackage` | Discriminator for a non-authoritative plan. All `CommonObject` and `Boundary` elements are also required. |
| `execution` | object | Required; closed structure | Groups the envelope reference that bounds this execution package. |
| `execution.workEnvelopeReference` | `Reference` object | Required | Exact ID and version of the `WorkEnvelope` that bounds this plan. |
| `boundary` | `Boundary` object | Required | Local scope, tool, data-access, approval, and authority constraints. |
| `plan` | object | Required; closed structure | Groups steps, outputs, dependencies, timing, and criteria. |
| `plan.plannedSteps` | array of string | Required; items have minimum length 1 | Ordered plan steps. The schema permits an empty array; a profile may impose a stronger minimum. |
| `plan.expectedOutputs` | array of string | Required; items have minimum length 1 | Outputs expected from the planned work. The schema permits an empty array. |
| `plan.dependencies` | array of string | Required; items have minimum length 1 | Named prerequisites or external dependencies. The schema permits an empty array. |
| `plan.timing` | string | Required; minimum length 1 | Human-readable timing constraint for the plan. |
| `plan.acceptanceCriteria` | array of string | Required; items have minimum length 1 | Conditions used to evaluate the planned result. The schema permits an empty array. |

```yaml
kind: ExecutionPackage
metadata:
  id: package-service-change
  name:
    en: Service-change execution plan
  description:
    en: Planned work required to prepare the reviewed service change.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: change-team
provenance:
  sourceReferences: []
  relationshipReferences:
    - id: envelope-service-change
      version: 1
execution:
  workEnvelopeReference:
    id: envelope-service-change
    version: 1
boundary:
  scope:
    - service-change
  tools:
    - maysano.change-proposal
  dataAccess:
    - service-planning-context
  approvalRights:
    - reviewed-change-proposal
  authorityLevel: 1
plan:
  plannedSteps:
    - Validate context
    - Prepare the proposed specification
    - Request review
  expectedOutputs:
    - Reviewed service change proposal
  dependencies:
    - Current Maysano graph
  timing: Before the service review
  acceptanceCriteria:
    - Names version expectations and unresolved conflicts
```

## ExecutionRequest

An `ExecutionRequest` is one explicit proposed external action, never an implicit command. It points to its plan and the revocation policy that protects its authority chain. It can be packaged with a `ChangeAction` for one Maysano resource write. Passing local validation is not permission to dispatch automatically.

| Element name | Type | Options | Description |
| --- | --- | --- |
| `kind` | string | Required; constant `ExecutionRequest` | Discriminator for one explicit proposed action. All `CommonObject` elements are also required. |
| `execution` | object | Required; closed structure | Groups the plan and revocation-policy references for this request. |
| `execution.executionPackageReference` | `Reference` object | Required | Exact ID and version of the `ExecutionPackage` that contains the request. |
| `execution.revocationPolicyReference` | `Reference` object | Required | Exact ID and version of the policy governing suspension or restoration of this request authority chain. |
| `request` | object | Required; closed structure | Groups the action proposal, requested authority, approval, and non-secret parameters. |
| `request.action` | string | Required; minimum length 1 | Human-readable proposed action. It is not an implicit dispatch instruction. |
| `request.tool` | string | Required; minimum length 1 | Named tool or capability requested by the action. |
| `request.target` | string | Required; minimum length 1 | Intended target of the action. |
| `request.requestedAuthority` | integer | Required; `0`–`3` | Requested local authority ordinal. It must be compared to the enclosing boundary by relationship validation. |
| `request.approval` | object | Required; closed structure | Groups the approval requirement and its expiry. |
| `request.approval.required` | boolean | Required | Whether a platform approval decision is required before execution. |
| `request.approval.expiresAt` | string or null | Required; RFC 3339 `date-time` or `null` | Expiry of the applicable approval when present. |
| `request.redactedParameters` | object | Optional; open structure | Non-secret request context. Raw secrets must not be included. |

```yaml
kind: ExecutionRequest
metadata:
  id: request-service-change
  name:
    en: Submit reviewed service specification
  description:
    en: Explicit request to submit the reviewed service change.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: change-team
provenance:
  sourceReferences: []
  relationshipReferences:
    - id: package-service-change
      version: 1
execution:
  executionPackageReference:
    id: package-service-change
    version: 1
  revocationPolicyReference:
    id: policy-service-change
    version: 1
request:
  action: submit reviewed service specification
  tool: maysano.change-proposal
  target: service planning graph
  requestedAuthority: 1
  approval:
    required: true
    expiresAt: "2026-12-01T00:00:00Z"
  redactedParameters:
    contextReference: context-service-change
```

# Evidence and assurance

## EvidenceEvent

An `EvidenceEvent` is the durable atomic record; an `EvidenceBundle` is an exportable grouping of its events. The event links a work envelope to attributable proof of context retrieval, validation, review, submission, returned state, failure, correction, or reconciliation. A local export is not a claim of immutable platform retention.

| Element name | Type | Options | Description |
| --- | --- | --- |
| `kind` | string | Required; constant `EvidenceEvent` | Discriminator for one durable, attributable event. All `CommonObject` elements are also required. |
| `evidence` | object | Required; closed structure | Groups the time, assignment, type, and payload of this event. |
| `evidence.occurredAt` | string | Required; RFC 3339 `date-time` | Time at which the recorded event occurred. |
| `evidence.workEnvelopeReference` | `Reference` object | Required | Exact ID and version of the `WorkEnvelope` to which the evidence belongs. |
| `evidence.eventType` | string | Required; minimum length 1 | Extensible event label, such as `context_retrieved` or `validation_completed`. |
| `evidence.payload` | object | Required; open structure | Structured, non-secret event details and authoritative receipt references. |

```yaml
kind: EvidenceEvent
metadata:
  id: evidence-context-retrieved
  name:
    en: Service-change context retrieved
  description:
    en: Evidence that the bounded Maysano context was retrieved.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: change-team
provenance:
  sourceReferences:
    - id: maysano:graph
      version: 4
      retrievedAt: "2026-10-20T00:00:00Z"
  relationshipReferences:
    - id: envelope-service-change
      version: 1
evidence:
  occurredAt: "2026-10-20T00:00:00Z"
  workEnvelopeReference:
    id: envelope-service-change
    version: 1
  eventType: context_retrieved
  payload:
    contextPackageReference:
      id: context-service-change
      version: 1
```

# System boundaries

## Architecture and responsibilities

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

# Change-control delivery

## ChangeAction

### Direct specification change

A `ChangeAction` is a peer top-level object for one agreed direct Maysano API operation. It references exactly one generated specification file and ODPH validates that file against the declared ODPC, ODPS, or ODPG schema before submitting it. It can be packaged with an `ExecutionRequest`, but it does not replace that request's plan, revocation, or approval chain.

`operation` is only `create` or `update`. An `update` requires `expectedVersion`. A connection change is an ODPG file update. A deprecation is a new ODPC or ODPS file version with its lifecycle state changed. A business-object update is a new ODPC or ODPS file version. `link`, `unlink`, and `deprecate` are not ChangeAction operations.

| Element name | Type | Options | Description |
| --- | --- | --- |
| `schema` | string | Required; canonical YAML or JSON schema URL | Identifies the v0.2 change-control schema used to validate this document. |
| `version` | string | Required; constant `0.2-draft` | Version of the ChangeAction contract. |
| `kind` | string | Required; constant `ChangeAction` | Discriminator for a single direct Maysano resource operation. |
| `metadata` | object | Required; closed structure | Contains `id`, `title`, `requestedBy`, and `createdAt`; optional `parentTestCase` and `parentChangeTask` use the identifier pattern `^[a-z0-9][a-z0-9-]*$`. |
| `graphContext` | object | Required; closed structure | Contains `source: maysano`, `baseGraphRevision`, and optional versioned `requiredObjects`. |
| `intent` | object | Required; closed structure | Contains `businessOwner`, `reason`, `expectedOutcome`, and an identifier-form `policyProfile`. |
| `specification` | object | Required; closed structure | Contains `operation`, `family`, contained YAML `file`, 64-character hexadecimal `sha256`, and `expectedVersion` when `operation` is `update`. |
| `review` | object | Required; closed structure | Contains a non-empty, unique `requiredRoles` array and optional `approvalExpiresAt`. |
| `acceptanceCriteria` | array of string | Required; at least 1 item | Non-empty criteria used to determine whether the requested change is acceptable. |

```yaml
schema: https://opendataproducts.org/odph-v0.2/schema/change-control.yaml
version: 0.2-draft
kind: ChangeAction
metadata:
  id: create-service-objective
  title: Create service objective
  requestedBy: Change Team
  createdAt: "2026-10-20T00:00:00Z"
graphContext:
  source: maysano
  baseGraphRevision: 4
intent:
  businessOwner: Head of Service
  reason: Establish a reviewed service objective
  expectedOutcome: Accepted objective version
  policyProfile: service-change
specification:
  operation: create
  family: ODPC
  file: specifications/odpc/service-objective-v1.yaml
  sha256: 9a8b0c06bb51226e0a30a2c7f79ef43f378c9bf913ac3489928ccfe341c593f2
review:
  requiredRoles:
    - Head of Service
acceptanceCriteria:
  - Objective is accepted by Maysano
```

The action cannot embed or duplicate the referenced specification’s object fields. See the complete [schema reference](#schema-reference) and the [first guided workflow](#guided-workflow-execution).

## ChangeTask

### Composite change planning

A `ChangeTask` is a peer top-level object for a composite business change. It groups multiple existing `ChangeAction` files and declares their dependencies. It does not embed, copy, or recreate ODPC, ODPS, or ODPG content, and it does not replace the context, mandate, work-envelope, execution-package, execution-request, or evidence responsibilities.

It records the bounded Maysano graph revision, action-file references, dependencies, required reviewers, acceptance criteria, execution status, and resulting evidence. Static validation rejects a task with fewer than two actions or unknown fields. Runtime validation rejects missing action files, duplicate action IDs, missing dependencies, and dependency cycles.

| Element name | Type | Options | Description |
| --- | --- | --- |
| `schema` | string | Required; canonical YAML or JSON schema URL | Identifies the v0.2 change-control schema used to validate this document. |
| `version` | string | Required; constant `0.2-draft` | Version of the ChangeTask contract. |
| `kind` | string | Required; constant `ChangeTask` | Discriminator for a composite, dependency-ordered change. |
| `metadata` | object | Required; closed structure | Contains `id`, `title`, `requestedBy`, and `createdAt`; optional parent identifiers use the identifier pattern. |
| `graphContext` | object | Required; closed structure | Contains `source: maysano`, `baseGraphRevision`, and optional versioned `requiredObjects`. |
| `intent` | object | Required; closed structure | Contains `businessOwner`, `reason`, `expectedOutcome`, and identifier-form `policyProfile`. |
| `actions` | array of `ActionReference` | Required; at least 2 items | Each item contains action `id`, contained YAML `actionFile`, and optional unique `dependsOn` action IDs. Runtime validation rejects missing references and dependency cycles. |
| `review` | object | Required; closed structure | Contains a non-empty, unique `requiredRoles` array and optional `approvalExpiresAt`. |
| `acceptanceCriteria` | array of string | Required; at least 1 item | Non-empty criteria used to determine whether the complete change is acceptable. |

```yaml
schema: https://opendataproducts.org/odph-v0.2/schema/change-control.yaml
version: 0.2-draft
kind: ChangeTask
metadata:
  id: service-change
  title: Service change
  requestedBy: Change Team
  createdAt: "2026-10-20T00:00:00Z"
graphContext:
  source: maysano
  baseGraphRevision: 4
intent:
  businessOwner: Head of Service
  reason: Deliver the reviewed service change
  expectedOutcome: Accepted change chain
  policyProfile: service-change
actions:
  - id: create-service-objective
    actionFile: actions/create-service-objective.yaml
  - id: update-service-graph
    actionFile: actions/update-service-graph.yaml
    dependsOn:
      - create-service-objective
review:
  requiredRoles:
    - Head of Service
acceptanceCriteria:
  - All actions reconcile with returned Maysano versions
```

The [example Change Task](examples/change-chain/change-tasks/change-chain.yaml) is the composite example.

## Specification artefacts

### ODPC, ODPS, and ODPG

`ChangeAction.specification` is a file reference, not a business-object envelope.

| Family | Carries | Validated against |
| --- | --- | --- |
| `ODPC` | Objective or use-case definitions and their business semantics. | ODPC schema |
| `ODPS` | Data-product definition, lifecycle, SLA, and data-quality terms. | ODPS schema |
| `ODPG` | Nodes and connections between objectives, use cases, and data products. | ODPG graph schema |

ODPG is the declared connection artefact. Connections are not raw relationship JSON. The example graph versions show the progression from an initial objective/use-case connection to a later composite change.

Every referenced file must be a contained relative `.yaml` or `.yml` path and must match the SHA-256 checksum in its action. The [validation guide](#validation-and-runtime-checks) describes the static and runtime checks.

## Guided workflow execution

### Direct Maysano writes

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

## Change Task execution

### Declared dependency order

Phase 2 later v0.2 validates a complete Change Task before execution. The initial implementation still sends individual Maysano API calls in declared dependency order; the task does not grant server-side atomic execution.

The composite example creates one objective, one use case, two data products, reuses an existing context data product, and updates one ODPG graph specification that expresses the new connections. Before each write ODPH verifies the agreed approvals, applicable object versions, and current graph revision. It records each submitted file identifier, Maysano identity and version, validation outcome, and reconciliation state.

## Generic change-chain example

### Validated example bundle

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

# Reference and delivery

## Schema reference

### Common fields

The canonical v0.2 contract is [`change-control.yaml`](odph-v0.2/schema/change-control.yaml). `ChangeAction` and `ChangeTask` use closed nested structures. The governed-work object definitions deliberately retain open structures where the model carries source-specific scope, conflict, or evidence payload content.

Both document kinds require `schema`, `version`, `kind`, `metadata`, `graphContext`, `intent`, `review`, and `acceptanceCriteria`.

| Element name | Type | Options | Description |
| --- | --- | --- |
| `schema` | string | Required; canonical YAML or JSON URL | Schema identifier for the change-control document. |
| `version` | string | Required; constant `0.2-draft` | Version of the change-control contract. |
| `kind` | string | Required; `ChangeAction` or `ChangeTask` | Selects the change-control object definition. |
| `metadata` | object | Required; closed structure | Stable document identity and provenance. |
| `graphContext` | object | Required; closed structure | Bounded Maysano source and graph revision. |
| `intent` | object | Required; closed structure | Accountable business owner, reason, outcome, and policy profile. |
| `review` | object | Required; closed structure | Required reviewer roles and optional approval expiry. |
| `acceptanceCriteria` | array of string | Required; at least 1 item | Criteria used to judge the requested change. |

#### `metadata`

Required: `id`, `title`, `requestedBy`, `createdAt`. `id` is a string of 3–128 characters matching `^[a-z0-9][a-z0-9-]*$`. `title` and `requestedBy` are non-empty strings; `createdAt` is an RFC 3339 date-time string. Optional `parentTestCase` and `parentChangeTask` use the same identifier rule.

#### `graphContext`

Required: `source: maysano` and `baseGraphRevision`, which is a non-negative integer or non-empty string. Optional `requiredObjects` is an array of object references. Each reference requires `id` (identifier) and `expectedVersion` (non-negative integer or non-empty string), and may declare `specificationFamily` as `ODPC`, `ODPS`, or `ODPG`.

#### `intent` and `review`

`intent` requires non-empty `businessOwner`, `reason`, and `expectedOutcome`, plus `policyProfile`, which uses the identifier rule. `review.requiredRoles` is a non-empty, unique array of non-empty strings. `review.approvalExpiresAt` is optional and uses the date-time format.

### `ChangeAction.specification`

`ChangeAction` additionally requires `specification`.

| Element name | Type | Options | Description |
| --- | --- | --- |
| `operation` | string | Required; `create` or `update` | Requested direct Maysano resource operation. `update` requires `expectedVersion`. |
| `family` | string | Required; `ODPC`, `ODPS`, or `ODPG` | Standard-family schema against which the referenced file is validated. |
| `file` | string | Required; contained relative `.yaml` or `.yml` path | File location; it cannot start with `/` or contain `..` path traversal. |
| `sha256` | string | Required; exactly 64 hexadecimal characters | SHA-256 checksum of the referenced file bytes. |
| `expectedVersion` | integer or string | Required for `update`; integer is at least `0`, string has minimum length 1 | Version expected by Maysano before an update is accepted. |

The referenced file carries the object identity, business fields, and domain semantics. The action does not duplicate them.

### `ChangeTask.actions`

`ChangeTask` additionally requires `actions`: an array with at least two references. Every reference requires `id` and `actionFile`; `actionFile` has the same contained relative-YAML rule as `specification.file`. Optional `dependsOn` is an array of unique action IDs in the same task. Runtime validation rejects missing references, duplicate action IDs, and dependency cycles.

### Deliberate v0.2 limits

The eight object kinds form one packageable model. Their boundary and evidence fields are intentionally declarative: they do not become raw API request bodies or authority grants. The schema does not embed ODPC, ODPS, or ODPG content, and it does not add generic `link`, `unlink`, or `deprecate` operations.

## Validation and runtime checks

### Level 1: static schema validation

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

### Level 2: cross-file and runtime validation

Before a Maysano write, resolve every referenced specification file; verify the checksum; verify action references; reject duplicate action IDs and dependency cycles; verify required Maysano object versions and the current graph revision; and verify ODPC, ODPS, and ODPG files are mutually consistent. Verify approvals before every write.

Record submitted file identifiers, resulting Maysano identities and versions, validation outcomes, and reconciliation state. Maysano is authoritative for returned state; these checks do not turn ODPH into a record store.

## Published contract and examples

### Machine-readable sources

The canonical YAML schema is [`change-control.yaml`](odph-v0.2/schema/change-control.yaml); the mechanically derived JSON representation is [`change-control.json`](odph-v0.2/schema/change-control.json). Both use the v0.2 schema identifier `https://opendataproducts.org/odph-v0.2/schema/change-control.yaml`.

The linked change-chain example bundle is under [`examples/change-chain/`](examples/change-chain/). It contains sixteen individually validated `ChangeAction` files, one later composite `ChangeTask`, and the referenced ODPC, ODPS, and ODPG files.

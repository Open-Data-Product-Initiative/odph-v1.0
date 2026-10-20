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

A Business Harness package is a reader view of one governed business change. It groups collections of independently valid peer top-level objects by the question they answer: **why**, **how**, or **what proves the result**. The group-level `metadata` explains the group; it does not create a ninth schema kind, grant authority, or replace the contained objects.

```yaml
package:
  businessNeed:
    metadata:
      answers: Why is this change needed, permitted, and bounded?
      decision: Reserve contact-centre capacity before eligible customers reach their service-term end date.
      desiredOutcome: A reviewed capacity plan and the supporting data products are accepted for use in weekly planning.
    contextPackages:
      - kind: ContextPackage
        content: Current graph revision, forecast demand, capacity data quality, and unresolved planning assumptions.
    mandates:
      - kind: Mandate
        content: Durable authority for customer-service capacity planning; excludes customer contact and operational dispatch.
    workEnvelopes:
      - kind: WorkEnvelope
        content: A reviewed weekly capacity plan with demand assumptions, review slots, owner, expiry, and acceptance criteria.

  actions:
    metadata:
      answers: How will the agreed change be carried out?
      rule: No external write occurs until the proposed action is approved.
    executionRequests:
      - kind: ExecutionRequest
        content: Submit the reviewed capacity-planning change to Maysano.
    changeTasks:
      - kind: ChangeTask
        content: The dependency-ordered set of specification changes required for the capacity plan.
    changeActions:
      - kind: ChangeAction
        content: One checksum-verified create or update of an ODPC, ODPS, or ODPG file.
    executionPackages:
      - kind: ExecutionPackage
        optional: true
        content: Use only when a complex action plan needs separate review; otherwise the WorkEnvelope and ChangeTask are sufficient.

  evidence:
    metadata:
      answers: What proves what was considered, approved, done, and returned?
    evidenceEvents:
      - kind: EvidenceEvent
        content: Context revision and retrieval time, decisions, approvals, submitted files, returned Maysano versions, and reconciliation outcome.
```

# Model map

## How the top-level objects connect

The three groups are package metadata, not new schema kinds. Their contents remain independently valid top-level objects: **Business Need** establishes why work is permitted; **Actions** defines how a proposed change is carried out; and **Evidence** records what proves the result. Maysano remains the authority for accepted records, approvals, applied changes, and audit evidence; ODPH prepares, validates, presents, submits, and links the resulting evidence.

```text
Business Need                         Actions                       Evidence
-------------                         -------                       --------
ContextPackage -> Mandate             ExecutionRequest             EvidenceEvent[]
                  -> WorkEnvelope     ChangeTask -> ChangeAction[]       ^
                                     (ExecutionPackage: optional)        |
                                                                    proof of all groups
```

<table>
<thead>
<tr>
<th>Group</th>
<th>Object kind</th>
<th>Question it answers</th>
<th>It must not become</th>
</tr>
</thead>
<tbody>
<tr>
<td>Business Need</td>
<td><code>ContextPackage</code></td>
<td>What was known, from which versions, and how fresh was it?</td>
<td>A shadow copy of the portfolio.</td>
</tr>
<tr>
<td>Business Need</td>
<td><code>Mandate</code></td>
<td>What is the durable business boundary for this area?</td>
<td>A task-level permission or an implicit tool grant.</td>
</tr>
<tr>
<td>Business Need</td>
<td><code>WorkEnvelope</code></td>
<td>What narrowly bounded assignment is permitted now?</td>
<td>A way to expand the mandate.</td>
</tr>
<tr>
<td>Actions</td>
<td><code>ExecutionPackage</code> (optional)</td>
<td>Does a complex action plan need separate review?</td>
<td>Independent authority or an autonomous runbook.</td>
</tr>
<tr>
<td>Actions</td>
<td><code>ExecutionRequest</code></td>
<td>Which single external write is proposed?</td>
<td>An implicit command or embedded business content.</td>
</tr>
<tr>
<td>Actions</td>
<td><code>ChangeTask</code></td>
<td>How are related specification changes ordered and reviewed?</td>
<td>The business rationale or a claim of all-or-nothing execution.</td>
</tr>
<tr>
<td>Actions</td>
<td><code>ChangeAction</code></td>
<td>Which one versioned specification file is created or updated?</td>
<td>An embedded business object or a generic relationship command.</td>
</tr>
<tr>
<td>Evidence</td>
<td><code>EvidenceEvent</code></td>
<td>What proves what was considered, decided, attempted, and returned?</td>
<td>A claim of immutable retention or a second system of record.</td>
</tr>
</tbody>
</table>

The package-level order is deliberate: Business Need explains **why**, Actions explains **how**, and Evidence explains **what proves the result**. `ExecutionPackage` is optional because a `WorkEnvelope` already defines the business assignment and a `ChangeTask` already orders the delivery work.

# Business Need

### Common object contract

The six governed-work objects—`ContextPackage`, `Mandate`, `WorkEnvelope`, `ExecutionPackage`, `ExecutionRequest`, and `EvidenceEvent`—are composed with the `CommonObject` definition. Identity, human-readable purpose, and provenance are grouped rather than flattened into every object.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constrained by object definition</td>
<td>Discriminator for the top-level object kind. Each object table names its permitted constant value.</td>
</tr>
<tr>
<td><code>metadata</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups object identity, human-readable purpose, and attribution.</td>
</tr>
<tr>
<td><code>metadata.id</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Stable identifier of this object version. The schema does not impose a global identifier pattern.</td>
</tr>
<tr>
<td><code>metadata.name</code></td>
<td>object</td>
<td>Required; one or more language keys</td>
<td>Human-readable, language-keyed name of the object. Each value is a non-empty string.</td>
</tr>
<tr>
<td><code>metadata.description</code></td>
<td>object</td>
<td>Required; one or more language keys</td>
<td>Human-readable, language-keyed description of the object’s purpose and bounded meaning. Each value is a non-empty string.</td>
</tr>
<tr>
<td><code>metadata.version</code></td>
<td>integer</td>
<td>Required; minimum <code>1</code></td>
<td>Positive version of this ODPH object, used by all object references.</td>
</tr>
<tr>
<td><code>metadata.createdAt</code></td>
<td>string</td>
<td>Required; RFC 3339 <code>date-time</code></td>
<td>Time at which this object version was created.</td>
</tr>
<tr>
<td><code>metadata.actor</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Attributed creator or producing actor. It is attribution, not authentication proof.</td>
</tr>
<tr>
<td><code>provenance</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups source observations and relationships without embedding their contents.</td>
</tr>
<tr>
<td><code>provenance.sourceReferences</code></td>
<td>array of <code>Reference</code></td>
<td>Required; may be empty</td>
<td>Versioned source observations or records used when producing the object.</td>
</tr>
<tr>
<td><code>provenance.relationshipReferences</code></td>
<td>array of <code>Reference</code></td>
<td>Required; may be empty</td>
<td>Versioned links to related ODPH objects or governed records.</td>
</tr>
</tbody>
</table>

### Reference

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>id</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Identifier of the referenced object or source.</td>
</tr>
<tr>
<td><code>version</code></td>
<td>integer</td>
<td>Required; minimum <code>1</code></td>
<td>Exact referenced version.</td>
</tr>
<tr>
<td><code>retrievedAt</code></td>
<td>string</td>
<td>Optional; RFC 3339 <code>date-time</code></td>
<td>Retrieval time for an observed source reference.</td>
</tr>
<tr>
<td><code>objectType</code></td>
<td>string</td>
<td>Optional</td>
<td>Source-specific or ODPH object-type label.</td>
</tr>
<tr>
<td><code>uri</code></td>
<td>string</td>
<td>Optional; <code>uri-reference</code> format</td>
<td>Relative or absolute locator for the reference.</td>
</tr>
</tbody>
</table>

### Boundary

`Mandate`, `WorkEnvelope`, and `ExecutionPackage` additionally compose the `Boundary` definition under their `boundary` element.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>scope</code></td>
<td>array of string</td>
<td>Required; items have minimum length 1</td>
<td>Declared business scope. A relationship validator must ensure a child boundary does not broaden its parent.</td>
</tr>
<tr>
<td><code>tools</code></td>
<td>array of string</td>
<td>Required; items have minimum length 1</td>
<td>Named local tool or capability boundary. This declaration does not grant access.</td>
</tr>
<tr>
<td><code>dataAccess</code></td>
<td>array of string</td>
<td>Required; items have minimum length 1</td>
<td>Named local data-access boundary. This declaration does not grant data access.</td>
</tr>
<tr>
<td><code>approvalRights</code></td>
<td>array of string</td>
<td>Required; items have minimum length 1</td>
<td>Named local approval boundary. This declaration does not confer approval rights.</td>
</tr>
<tr>
<td><code>authorityLevel</code></td>
<td>integer</td>
<td>Required; <code>0</code>–<code>3</code></td>
<td>Local ordinal used for deterministic comparison only; values have no portable cross-organisation meaning.</td>
</tr>
</tbody>
</table>

## ContextPackage

A `ContextPackage` is a bounded observation, not a copied catalog. It identifies the retrieval scope, source IDs and versions, retrieval time, freshness, and observed conflicts. Every source observation is attributable to a version and retrieval time; stale or contradictory input must be made visible for human resolution.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constant <code>ContextPackage</code></td>
<td>Discriminator for a bounded, attributable context observation. All <code>CommonObject</code> elements are also required.</td>
</tr>
<tr>
<td><code>context</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups the scope, freshness, and conflict statement for this observation.</td>
</tr>
<tr>
<td><code>context.retrievalScope</code></td>
<td>object</td>
<td>Required; open structure</td>
<td>Source-specific description of the retrieved objectives, use cases, data products, graph revision, or other bounded slice.</td>
</tr>
<tr>
<td><code>context.freshness</code></td>
<td>string</td>
<td>Required; <code>fresh</code>, <code>stale</code>, or <code>unknown</code></td>
<td>Declared freshness state of this observation. It does not assert a universal source-consistency guarantee.</td>
</tr>
<tr>
<td><code>context.conflicts</code></td>
<td>array</td>
<td>Required; may be empty</td>
<td>Observed conflicts that need resolution. An empty array means no conflict was observed in this snapshot.</td>
</tr>
</tbody>
</table>

```yaml
kind: ContextPackage
metadata:
  id: capacity-planning-context
  name:
    en: Capacity-planning evidence
  description:
    en: Bounded evidence used to decide whether customer-service capacity should be reserved before service terms end.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: capacity-planning-team
provenance:
  sourceReferences:
    - id: maysano:graph
      version: 4
      retrievedAt: "2026-10-20T00:00:00Z"
  relationshipReferences: []
context:
  retrievalScope:
    graphRevision: 4
    useCaseId: plan-service-delivery
    dataProductIds:
      - primary-data-product
      - context-data-product
  freshness: fresh
  conflicts:
    - The demand forecast is fresh, but its capacity assumptions still require business-owner review.
```

## Mandate

A `Mandate` is the durable business boundary for an area of work. It names the accountable owner, permitted scope, tools, data access, review rights, authority level, and expiry. ODPH does not mint authority: a local policy match never grants connector, credential, data-access, or external-write rights.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constant <code>Mandate</code></td>
<td>Discriminator for a durable business boundary. All <code>CommonObject</code> and <code>Boundary</code> elements are also required.</td>
</tr>
<tr>
<td><code>mandate</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups the durable business boundary's area, owner, and review expiry.</td>
</tr>
<tr>
<td><code>mandate.businessArea</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Business area governed by this mandate.</td>
</tr>
<tr>
<td><code>mandate.owner</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Accountable owner of the durable boundary.</td>
</tr>
<tr>
<td><code>mandate.expiresAt</code></td>
<td>string</td>
<td>Required; RFC 3339 <code>date-time</code></td>
<td>Time after which the mandate must be reviewed or replaced.</td>
</tr>
<tr>
<td><code>boundary</code></td>
<td><code>Boundary</code> object</td>
<td>Required</td>
<td>Local scope, tool, data-access, approval, and authority constraints.</td>
</tr>
</tbody>
</table>

```yaml
kind: Mandate
metadata:
  id: customer-capacity-mandate
  name:
    en: Customer-service capacity planning
  description:
    en: Authority to prepare and review capacity-planning changes; it does not authorise customer contact or operational dispatch.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: head-of-customer-service
provenance:
  sourceReferences: []
  relationshipReferences: []
mandate:
  businessArea: Customer service capacity planning
  owner: Head of Customer Service
  expiresAt: "2027-01-01T00:00:00Z"
boundary:
  scope:
    - customer-capacity-planning
  tools:
    - maysano.change-proposal
  dataAccess:
    - capacity-planning-context
  approvalRights:
    - reviewed-capacity-plan
  authorityLevel: 1
```

## WorkEnvelope

A `WorkEnvelope` narrows one mandate into one assignment. It states the requested result, accountable owner, allowed subset, and expiry. It may narrow a mandate but must never broaden it; relationship validation must reject a missing mandate version or an expanded boundary.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constant <code>WorkEnvelope</code></td>
<td>Discriminator for an assignment-specific boundary. All <code>CommonObject</code> and <code>Boundary</code> elements are also required.</td>
</tr>
<tr>
<td><code>assignment</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups the assignment's parent mandate, result, owner, and expiry.</td>
</tr>
<tr>
<td><code>assignment.mandateReference</code></td>
<td><code>Reference</code> object</td>
<td>Required</td>
<td>Exact ID and version of the <code>Mandate</code> being narrowed. Relationship validation rejects a missing or broadened parent boundary.</td>
</tr>
<tr>
<td><code>assignment.requestedResult</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Business result requested for this assignment.</td>
</tr>
<tr>
<td><code>assignment.owner</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Accountable owner of this assignment.</td>
</tr>
<tr>
<td><code>assignment.expiresAt</code></td>
<td>string</td>
<td>Required; RFC 3339 <code>date-time</code></td>
<td>Time after which the assignment boundary is no longer valid.</td>
</tr>
<tr>
<td><code>boundary</code></td>
<td><code>Boundary</code> object</td>
<td>Required</td>
<td>Local scope, tool, data-access, approval, and authority constraints.</td>
</tr>
</tbody>
</table>

```yaml
kind: WorkEnvelope
metadata:
  id: capacity-plan-assignment
  name:
    en: Capacity plan before service terms end
  description:
    en: Assignment to prepare a reviewed weekly capacity plan for customers likely to require a service change.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: head-of-customer-service
provenance:
  sourceReferences: []
  relationshipReferences:
    - id: customer-capacity-mandate
      version: 1
assignment:
  mandateReference:
    id: customer-capacity-mandate
    version: 1
  requestedResult: Reviewed weekly capacity plan, including demand assumptions, available review slots, and unresolved conflicts.
  owner: Head of Customer Service
  expiresAt: "2026-12-01T00:00:00Z"
boundary:
  scope:
    - customer-capacity-planning
  tools:
    - maysano.change-proposal
  dataAccess:
    - capacity-planning-context
  approvalRights:
    - reviewed-capacity-plan
  authorityLevel: 1
```

# Actions

## ExecutionPackage (optional)

An `ExecutionPackage` is an optional, separately reviewable action plan under one work envelope. Use it when the planned steps, dependencies, outputs, timing, and criteria need their own review. Do not create it merely to repeat a `WorkEnvelope` or `ChangeTask`.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constant <code>ExecutionPackage</code></td>
<td>Discriminator for an optional, separately reviewable action plan. All <code>CommonObject</code> and <code>Boundary</code> elements are also required.</td>
</tr>
<tr>
<td><code>execution</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups the envelope reference that bounds this execution package.</td>
</tr>
<tr>
<td><code>execution.workEnvelopeReference</code></td>
<td><code>Reference</code> object</td>
<td>Required</td>
<td>Exact ID and version of the <code>WorkEnvelope</code> that bounds this plan.</td>
</tr>
<tr>
<td><code>boundary</code></td>
<td><code>Boundary</code> object</td>
<td>Required</td>
<td>Local scope, tool, data-access, approval, and authority constraints.</td>
</tr>
<tr>
<td><code>plan</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups steps, outputs, dependencies, timing, and criteria.</td>
</tr>
<tr>
<td><code>plan.plannedSteps</code></td>
<td>array of string</td>
<td>Required; items have minimum length 1</td>
<td>Ordered plan steps. The schema permits an empty array; a profile may impose a stronger minimum.</td>
</tr>
<tr>
<td><code>plan.expectedOutputs</code></td>
<td>array of string</td>
<td>Required; items have minimum length 1</td>
<td>Outputs expected from the planned work. The schema permits an empty array.</td>
</tr>
<tr>
<td><code>plan.dependencies</code></td>
<td>array of string</td>
<td>Required; items have minimum length 1</td>
<td>Named prerequisites or external dependencies. The schema permits an empty array.</td>
</tr>
<tr>
<td><code>plan.timing</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Human-readable timing constraint for the plan.</td>
</tr>
<tr>
<td><code>plan.acceptanceCriteria</code></td>
<td>array of string</td>
<td>Required; items have minimum length 1</td>
<td>Conditions used to evaluate the planned result. The schema permits an empty array.</td>
</tr>
</tbody>
</table>

```yaml
kind: ExecutionPackage
metadata:
  id: capacity-plan-execution
  name:
    en: Capacity-plan preparation
  description:
    en: Reviewable preparation of a weekly capacity plan and the supporting specification change.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: capacity-planning-team
provenance:
  sourceReferences: []
  relationshipReferences:
    - id: capacity-plan-assignment
      version: 1
execution:
  workEnvelopeReference:
    id: capacity-plan-assignment
    version: 1
boundary:
  scope:
    - customer-capacity-planning
  tools:
    - maysano.change-proposal
  dataAccess:
    - capacity-planning-context
  approvalRights:
    - reviewed-capacity-plan
  authorityLevel: 1
plan:
  plannedSteps:
    - Confirm the demand forecast, graph revision, and unresolved capacity assumptions.
    - Prepare the capacity-planning use case and supporting data-product specifications.
    - Request business-owner, data-product-owner, and graph-steward review.
  expectedOutputs:
    - Reviewed weekly capacity plan
    - Dependency-ordered ChangeTask with validated specification files
  dependencies:
    - Current Maysano graph revision
    - Approved forecast and capacity data sources
  timing: Before the next weekly contact-centre planning cycle
  acceptanceCriteria:
    - States the forecast source, capacity assumptions, review owners, and every unresolved conflict.
```

## ExecutionRequest

An `ExecutionRequest` is one explicit proposed external action, never an implicit command. It binds directly to the `WorkEnvelope` that permits the action and to the revocation policy that protects that authority chain. It may additionally cite an `ExecutionPackage` when a complex action plan received separate review. Passing local validation is not permission to dispatch automatically.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constant <code>ExecutionRequest</code></td>
<td>Discriminator for one explicit proposed action. All <code>CommonObject</code> elements are also required.</td>
</tr>
<tr>
<td><code>execution</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups the required work-envelope and revocation-policy references, with an optional separately reviewed plan.</td>
</tr>
<tr>
<td><code>execution.workEnvelopeReference</code></td>
<td><code>Reference</code> object</td>
<td>Required</td>
<td>Exact ID and version of the <code>WorkEnvelope</code> that permits the proposed action.</td>
</tr>
<tr>
<td><code>execution.executionPackageReference</code></td>
<td><code>Reference</code> object</td>
<td>Optional</td>
<td>Exact ID and version of a separately reviewed <code>ExecutionPackage</code>, used only for complex action delivery.</td>
</tr>
<tr>
<td><code>execution.revocationPolicyReference</code></td>
<td><code>Reference</code> object</td>
<td>Required</td>
<td>Exact ID and version of the policy governing suspension or restoration of this request authority chain.</td>
</tr>
<tr>
<td><code>request</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups the action proposal, requested authority, approval, and non-secret parameters.</td>
</tr>
<tr>
<td><code>request.action</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Human-readable proposed action. It is not an implicit dispatch instruction.</td>
</tr>
<tr>
<td><code>request.tool</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Named tool or capability requested by the action.</td>
</tr>
<tr>
<td><code>request.target</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Intended target of the action.</td>
</tr>
<tr>
<td><code>request.requestedAuthority</code></td>
<td>integer</td>
<td>Required; <code>0</code>–<code>3</code></td>
<td>Requested local authority ordinal. It must be compared to the enclosing boundary by relationship validation.</td>
</tr>
<tr>
<td><code>request.approval</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups the approval requirement and its expiry.</td>
</tr>
<tr>
<td><code>request.approval.required</code></td>
<td>boolean</td>
<td>Required</td>
<td>Whether a platform approval decision is required before execution.</td>
</tr>
<tr>
<td><code>request.approval.expiresAt</code></td>
<td>string or null</td>
<td>Required; RFC 3339 <code>date-time</code> or <code>null</code></td>
<td>Expiry of the applicable approval when present.</td>
</tr>
<tr>
<td><code>request.redactedParameters</code></td>
<td>object</td>
<td>Optional; open structure</td>
<td>Non-secret request context. Raw secrets must not be included.</td>
</tr>
</tbody>
</table>

```yaml
kind: ExecutionRequest
metadata:
  id: submit-capacity-plan
  name:
    en: Submit reviewed capacity-planning change
  description:
    en: Explicit request to submit the reviewed capacity-planning ChangeTask to Maysano.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: capacity-planning-team
provenance:
  sourceReferences: []
  relationshipReferences:
    - id: capacity-plan-assignment
      version: 1
execution:
  workEnvelopeReference:
    id: capacity-plan-assignment
    version: 1
  revocationPolicyReference:
    id: capacity-change-policy
    version: 1
request:
  action: submit reviewed capacity-planning ChangeTask
  tool: maysano.change-proposal
  target: Maysano customer-service capacity-planning graph
  requestedAuthority: 1
  approval:
    required: true
    expiresAt: "2026-12-01T00:00:00Z"
  redactedParameters:
    contextReference: capacity-planning-context
```

# Evidence

## EvidenceEvent

An `EvidenceEvent` is the durable atomic record; an `EvidenceBundle` is an exportable grouping of its events. The event links a work envelope to attributable proof of context retrieval, validation, review, submission, returned state, failure, correction, or reconciliation. A local export is not a claim of immutable platform retention.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constant <code>EvidenceEvent</code></td>
<td>Discriminator for one durable, attributable event. All <code>CommonObject</code> elements are also required.</td>
</tr>
<tr>
<td><code>evidence</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Groups the time, assignment, type, and payload of this event.</td>
</tr>
<tr>
<td><code>evidence.occurredAt</code></td>
<td>string</td>
<td>Required; RFC 3339 <code>date-time</code></td>
<td>Time at which the recorded event occurred.</td>
</tr>
<tr>
<td><code>evidence.workEnvelopeReference</code></td>
<td><code>Reference</code> object</td>
<td>Required</td>
<td>Exact ID and version of the <code>WorkEnvelope</code> to which the evidence belongs.</td>
</tr>
<tr>
<td><code>evidence.eventType</code></td>
<td>string</td>
<td>Required; minimum length 1</td>
<td>Extensible event label, such as <code>context_retrieved</code> or <code>validation_completed</code>.</td>
</tr>
<tr>
<td><code>evidence.payload</code></td>
<td>object</td>
<td>Required; open structure</td>
<td>Structured, non-secret event details and authoritative receipt references.</td>
</tr>
</tbody>
</table>

```yaml
kind: EvidenceEvent
metadata:
  id: capacity-context-retrieved
  name:
    en: Capacity-planning context retrieved
  description:
    en: Evidence that the current planning graph and capacity sources were retrieved before the capacity decision.
  version: 1
  createdAt: "2026-10-20T00:00:00Z"
  actor: capacity-planning-team
provenance:
  sourceReferences:
    - id: maysano:graph
      version: 4
      retrievedAt: "2026-10-20T00:00:00Z"
  relationshipReferences:
    - id: capacity-plan-assignment
      version: 1
evidence:
  occurredAt: "2026-10-20T00:00:00Z"
  workEnvelopeReference:
    id: capacity-plan-assignment
    version: 1
  eventType: context_retrieved
  payload:
    contextPackageReference:
      id: capacity-planning-context
      version: 1
```

# System boundaries

## Architecture and responsibilities

Maysano is the authoritative record for accepted specification versions, object identities, graph state, approvals, applied changes, and audit evidence. ODPH retrieves bounded Maysano context; creates and validates specification files; presents a proposed change to the business owner; submits agreed files to Maysano; and records evidence. ODPH is not a second record store.

<table>
<thead>
<tr>
<th>Concern</th>
<th>Authoritative location</th>
</tr>
</thead>
<tbody>
<tr>
<td>Data-product definition</td>
<td>ODPS YAML and the ODPS schema</td>
</tr>
<tr>
<td>Objective and use-case definition</td>
<td>ODPC YAML and the ODPC schema</td>
</tr>
<tr>
<td>Connections</td>
<td>ODPG YAML graph specification and the ODPG schema</td>
</tr>
<tr>
<td>Accepted identity, version, approval, graph state, applied change</td>
<td>Maysano</td>
</tr>
<tr>
<td>Generated file validation, proposal presentation, submission evidence</td>
<td>ODPH</td>
</tr>
</tbody>
</table>

ODPH v0.2 serializes all eight top-level object kinds. A delivery must connect the objects instead of pretending that a task or action is self-sufficient. Object identity, business fields, domain semantics, and lifecycle state belong in the referenced ODPC, ODPS, or ODPG file.

There are no raw relationship JSON, API request bodies, or runtime-cache details in this contract. Boundary fields declare a local governed-work model; they do not issue real tools, data access, approval rights, or authority.

# Change-control delivery

## ChangeAction

### Direct specification change

A `ChangeAction` is a peer top-level object for one agreed direct Maysano API operation. It references exactly one generated specification file and ODPH validates that file against the declared ODPC, ODPS, or ODPG schema before submitting it. It can be packaged with an `ExecutionRequest`, but it does not replace that request's plan, revocation, or approval chain.

`operation` is only `create` or `update`. An `update` requires `expectedVersion`. A connection change is an ODPG file update. A deprecation is a new ODPC or ODPS file version with its lifecycle state changed. A business-object update is a new ODPC or ODPS file version. `link`, `unlink`, and `deprecate` are not ChangeAction operations.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>schema</code></td>
<td>string</td>
<td>Required; canonical YAML or JSON schema URL</td>
<td>Identifies the v0.2 change-control schema used to validate this document.</td>
</tr>
<tr>
<td><code>version</code></td>
<td>string</td>
<td>Required; constant <code>0.2-draft</code></td>
<td>Version of the ChangeAction contract.</td>
</tr>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constant <code>ChangeAction</code></td>
<td>Discriminator for a single direct Maysano resource operation.</td>
</tr>
<tr>
<td><code>metadata</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains <code>id</code>, <code>title</code>, <code>requestedBy</code>, and <code>createdAt</code>; optional <code>parentTestCase</code> and <code>parentChangeTask</code> use the identifier pattern <code>^[a-z0-9][a-z0-9-]*$</code>.</td>
</tr>
<tr>
<td><code>graphContext</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains <code>source: maysano</code>, <code>baseGraphRevision</code>, and optional versioned <code>requiredObjects</code>.</td>
</tr>
<tr>
<td><code>intent</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains <code>businessOwner</code>, <code>reason</code>, <code>expectedOutcome</code>, and an identifier-form <code>policyProfile</code>.</td>
</tr>
<tr>
<td><code>specification</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains <code>operation</code>, <code>family</code>, contained YAML <code>file</code>, 64-character hexadecimal <code>sha256</code>, and <code>expectedVersion</code> when <code>operation</code> is <code>update</code>.</td>
</tr>
<tr>
<td><code>review</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains a non-empty, unique <code>requiredRoles</code> array and optional <code>approvalExpiresAt</code>.</td>
</tr>
<tr>
<td><code>acceptanceCriteria</code></td>
<td>array of string</td>
<td>Required; at least 1 item</td>
<td>Non-empty criteria used to determine whether the requested change is acceptable.</td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>schema</code></td>
<td>string</td>
<td>Required; canonical YAML or JSON schema URL</td>
<td>Identifies the v0.2 change-control schema used to validate this document.</td>
</tr>
<tr>
<td><code>version</code></td>
<td>string</td>
<td>Required; constant <code>0.2-draft</code></td>
<td>Version of the ChangeTask contract.</td>
</tr>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; constant <code>ChangeTask</code></td>
<td>Discriminator for a composite, dependency-ordered change.</td>
</tr>
<tr>
<td><code>metadata</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains <code>id</code>, <code>title</code>, <code>requestedBy</code>, and <code>createdAt</code>; optional parent identifiers use the identifier pattern.</td>
</tr>
<tr>
<td><code>graphContext</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains <code>source: maysano</code>, <code>baseGraphRevision</code>, and optional versioned <code>requiredObjects</code>.</td>
</tr>
<tr>
<td><code>intent</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains <code>businessOwner</code>, <code>reason</code>, <code>expectedOutcome</code>, and identifier-form <code>policyProfile</code>.</td>
</tr>
<tr>
<td><code>actions</code></td>
<td>array of <code>ActionReference</code></td>
<td>Required; at least 2 items</td>
<td>Each item contains action <code>id</code>, contained YAML <code>actionFile</code>, and optional unique <code>dependsOn</code> action IDs. Runtime validation rejects missing references and dependency cycles.</td>
</tr>
<tr>
<td><code>review</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Contains a non-empty, unique <code>requiredRoles</code> array and optional <code>approvalExpiresAt</code>.</td>
</tr>
<tr>
<td><code>acceptanceCriteria</code></td>
<td>array of string</td>
<td>Required; at least 1 item</td>
<td>Non-empty criteria used to determine whether the complete change is acceptable.</td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr>
<th>Family</th>
<th>Carries</th>
<th>Validated against</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>ODPC</code></td>
<td>Objective or use-case definitions and their business semantics.</td>
<td>ODPC schema</td>
</tr>
<tr>
<td><code>ODPS</code></td>
<td>Data-product definition, lifecycle, SLA, and data-quality terms.</td>
<td>ODPS schema</td>
</tr>
<tr>
<td><code>ODPG</code></td>
<td>Nodes and connections between objectives, use cases, and data products.</td>
<td>ODPG graph schema</td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr>
<th>Test case</th>
<th>Expected specification artefacts</th>
</tr>
</thead>
<tbody>
<tr>
<td>01</td>
<td>ODPC objective v1; ODPC use case v1; ODPG graph v1</td>
</tr>
<tr>
<td>02</td>
<td>ODPS Primary Data Product v1; ODPG graph v2</td>
</tr>
<tr>
<td>03</td>
<td>ODPS Primary Data Product v2 with revised SLA and DQ terms</td>
</tr>
<tr>
<td>04</td>
<td>ODPC second use case v1; ODPG graph v3</td>
</tr>
<tr>
<td>05</td>
<td>ODPS Context Data Product v1; ODPS Primary Data Product v3, deprecated; ODPG graph v4</td>
</tr>
<tr>
<td>06</td>
<td>ODPC secondary objective v1; ODPC secondary use case v1; ODPS Additional Data Product v1; ODPS Capacity Data Product v1; ODPG graph v5</td>
</tr>
</tbody>
</table>

Test cases 01–05 demonstrate direct actions. Test case 06 also provides the later composite `ChangeTask`, which references its five separately valid action files and uses dependencies to order the individual resource writes.

# Reference and delivery

## Schema reference

### Common fields

The canonical v0.2 contract is [`change-control.yaml`](odph-v0.2/schema/change-control.yaml). `ChangeAction` and `ChangeTask` use closed nested structures. The governed-work object definitions deliberately retain open structures where the model carries source-specific scope, conflict, or evidence payload content.

Both document kinds require `schema`, `version`, `kind`, `metadata`, `graphContext`, `intent`, `review`, and `acceptanceCriteria`.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>schema</code></td>
<td>string</td>
<td>Required; canonical YAML or JSON URL</td>
<td>Schema identifier for the change-control document.</td>
</tr>
<tr>
<td><code>version</code></td>
<td>string</td>
<td>Required; constant <code>0.2-draft</code></td>
<td>Version of the change-control contract.</td>
</tr>
<tr>
<td><code>kind</code></td>
<td>string</td>
<td>Required; <code>ChangeAction</code> or <code>ChangeTask</code></td>
<td>Selects the change-control object definition.</td>
</tr>
<tr>
<td><code>metadata</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Stable document identity and provenance.</td>
</tr>
<tr>
<td><code>graphContext</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Bounded Maysano source and graph revision.</td>
</tr>
<tr>
<td><code>intent</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Accountable business owner, reason, outcome, and policy profile.</td>
</tr>
<tr>
<td><code>review</code></td>
<td>object</td>
<td>Required; closed structure</td>
<td>Required reviewer roles and optional approval expiry.</td>
</tr>
<tr>
<td><code>acceptanceCriteria</code></td>
<td>array of string</td>
<td>Required; at least 1 item</td>
<td>Criteria used to judge the requested change.</td>
</tr>
</tbody>
</table>

#### `metadata`

Required: `id`, `title`, `requestedBy`, `createdAt`. `id` is a string of 3–128 characters matching `^[a-z0-9][a-z0-9-]*$`. `title` and `requestedBy` are non-empty strings; `createdAt` is an RFC 3339 date-time string. Optional `parentTestCase` and `parentChangeTask` use the same identifier rule.

#### `graphContext`

Required: `source: maysano` and `baseGraphRevision`, which is a non-negative integer or non-empty string. Optional `requiredObjects` is an array of object references. Each reference requires `id` (identifier) and `expectedVersion` (non-negative integer or non-empty string), and may declare `specificationFamily` as `ODPC`, `ODPS`, or `ODPG`.

#### `intent` and `review`

`intent` requires non-empty `businessOwner`, `reason`, and `expectedOutcome`, plus `policyProfile`, which uses the identifier rule. `review.requiredRoles` is a non-empty, unique array of non-empty strings. `review.approvalExpiresAt` is optional and uses the date-time format.

### `ChangeAction.specification`

`ChangeAction` additionally requires `specification`.

<table>
<thead>
<tr>
<th>Element name</th>
<th>Type</th>
<th>Options</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>operation</code></td>
<td>string</td>
<td>Required; <code>create</code> or <code>update</code></td>
<td>Requested direct Maysano resource operation. <code>update</code> requires <code>expectedVersion</code>.</td>
</tr>
<tr>
<td><code>family</code></td>
<td>string</td>
<td>Required; <code>ODPC</code>, <code>ODPS</code>, or <code>ODPG</code></td>
<td>Standard-family schema against which the referenced file is validated.</td>
</tr>
<tr>
<td><code>file</code></td>
<td>string</td>
<td>Required; contained relative <code>.yaml</code> or <code>.yml</code> path</td>
<td>File location; it cannot start with <code>/</code> or contain <code>..</code> path traversal.</td>
</tr>
<tr>
<td><code>sha256</code></td>
<td>string</td>
<td>Required; exactly 64 hexadecimal characters</td>
<td>SHA-256 checksum of the referenced file bytes.</td>
</tr>
<tr>
<td><code>expectedVersion</code></td>
<td>integer or string</td>
<td>Required for <code>update</code>; integer is at least <code>0</code>, string has minimum length 1</td>
<td>Version expected by Maysano before an update is accepted.</td>
</tr>
</tbody>
</table>

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

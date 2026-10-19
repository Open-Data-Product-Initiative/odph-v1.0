---
title: Open Data Product Harness (ODPH) 0.1 Draft | OpenDataProducts.org
language_tabs:
- yaml
- json
toc_footers:
  - License <a href='https://www.apache.org/licenses/LICENSE-2.0'>Apache 2.0</a>
  - <br/><a href='https://opendataproducts.org'>Specification home</a>
  - <br/>OpenDataProducts.org
includes: []
search: true
code_clipboard: true
meta:
  - name: description
    content: Open Data Product Harness (ODPH) 0.1 Draft defines a bounded, evidence-oriented interchange model for governed human and agent work. It is non-ratified design material, not execution authority.
  - name: spec-version
    content: "0.1-draft"
  - name: llms
    content: /llms.txt
  - name: ai-agent-guidance
    content: Use /llms.txt and /schema/odph.yaml before generating or validating a package.
---

# OPEN DATA PRODUCT HARNESS

## Version 0.1 Draft

<aside class="warning">This is non-ratified design material. It describes a local planning-and-evidence interchange model grounded in Kentaro's local governance core. It is not an ODPS, ODPC, ODPG, or Maysano specification, and it creates no new authority model.</aside>

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in BCP 14 ([RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) and [RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174)) when, and only when, they appear in all capitals.

| Topic | Link | Description |
|---|---|---|
| Version source | <a href="https://github.com/Open-Data-Product-Initiative/odph-v1.0">ODPH draft on GitHub</a> | Proposed source repository for the draft |
| Full example | [full-retention-review.yaml](examples/full-retention-review.yaml) | A synthetic local-only package |
| Schema | [odph.yaml](schema/odph.yaml) | Canonical YAML serialization of JSON Schema |

# Purpose and standards-family boundary

ODPH describes bounded work by which people and agents inspect sourced context, prepare a plan, propose actions, and retain attributable evidence. It is neither a data-product descriptor nor a catalog entry.

```text
ODPS / another product model  -> authoritative data-product definition
ODPC                           -> reusable portfolio objects
ODPG / another graph model     -> relationships between portfolio objects
ODPH (proposed)                 -> bounded governed work against such context
```

A package MAY reference an ODPS product, an ODPC object, an ODPG graph node, a Maysano record, or another internal source. It MUST reference those sources rather than duplicate their complete metadata. This keeps ODPH aligned with the standards family without making it ODPS-only.

## What ODPH does not do

A conforming implementation MUST distinguish a local planning and evidence artefact from an authoritative business-system record. A valid package does not by itself grant tool, connector, credential, or data access; make an approval real; execute a request; write a portfolio or graph record; suspend a live credential; or constitute immutable, retention-enforced, compliance-grade audit.

```text
local policy result: allowed
meaning: structurally in scope under supplied local objects
not meaning: permission to execute in an external system
```

Kentaro v0.1 is deliberately read-only. A future execution profile requires an independently verified platform contract, narrow credentials, real approval semantics, and platform-side enforcement.

# Conceptual model

The six parts are six conceptual concerns, not six peer fields in a planning document. `RevocationPolicy` and `Correction` are cross-cutting controls. `EvidenceBundle` is a logical/exported grouping; the durable local record is an `EvidenceEvent`.

```text
                         sourced, bounded context
                                  │
                         ContextPackage
                                  │
Mandate ──narrows to──> WorkEnvelope ──plans through──> ExecutionPackage
                                                              │
                                                     proposes zero or more
                                                              │
                                                     ExecutionRequest(s)
                                                              │
                  RevocationPolicy ──guards each request─────┘

Context + versions + evaluation + outputs + corrections ──> EvidenceBundle
Correction ──targets one object and names its destination───┘
```

The arrows are constraints, not workflow automation. A human MAY co-author, revise, reject, or terminate any local artefact. No arrow authorizes an agent to continue autonomously.

| Part | Core question | Stable meaning | Human responsibility | Machine responsibility |
|---|---|---|---|---|
| ContextPackage | What did we know? | A bounded observation with provenance and freshness. | Set scope; resolve material conflicts. | Preserve IDs, versions, and times; report gaps. |
| Mandate | What could this area permit? | Durable upper boundary for scope and authority. | Own and review the boundary. | Validate structure and expiry. |
| WorkEnvelope | What is permitted now? | Assignment-specific subset of one Mandate. | Set result, owner, exclusions, and expiry. | Reject expansion; flag absent ownership. |
| ExecutionPackage | What is the plan? | Non-authoritative plan under one envelope. | Approve or revise the plan. | Validate that it does not broaden the envelope. |
| ExecutionRequest | What action is proposed? | One proposed action, never an implicit command. | Decide whether a future action is acceptable. | Evaluate deterministically; do not dispatch locally. |
| EvidenceBundle | What supports the work? | Exportable grouping of attributable events. | Review interpretations and corrections. | Preserve references; redact; optionally hash-chain. |

# Object vocabulary

## ContextPackage

A `ContextPackage` is a snapshot of the authorized context seen for one assignment. It is evidence of observation, not a shadow portfolio. It MUST identify a retrieval scope, at least one source reference with ID, version, and retrieval time, a `freshness` state (`fresh`, `stale`, or `unknown`), and observed conflicts.

```yaml
id: context-retention-review
kind: ContextPackage
version: 1
retrievalScope:
  objectiveIds: [objective-retention]
sourceReferences:
  - id: demo:objective-retention
    version: 1
    retrievedAt: "2026-10-17T08:00:00Z"
freshness: fresh
conflicts: []
```

An empty conflict list means none were observed in this snapshot; it is not a claim of universal consistency.

## Mandate

A `Mandate` is the durable outer boundary for a business area. It is about authority, not a task plan. The boundary axes are `scope`, `tools`, `dataAccess`, `approvalRights`, and `authorityLevel`, with an owner, business area, and expiry.

```yaml
id: mandate-commercial-analysis
kind: Mandate
businessArea: Commercial analysis
owner: Commercial director
scope: [renewal-prioritisation]
tools: [draft.decision_note]
dataAccess: [customer_health_summary]
approvalRights: [reviewed_draft]
authorityLevel: 1 # Local ordinal; not a portable standard meaning
expiresAt: "2027-01-01T00:00:00Z"
```

The current local profile validates an integer `authorityLevel` from 0 through 3 but does not assign portable meanings to those values. A future ratified standard MUST either define a normative enum and behaviour or make authority class profile-specific.

## WorkEnvelope

A `WorkEnvelope` turns one durable Mandate into one assignment. It MUST point to exactly one Mandate ID and version. Its requested result and shorter-lived review boundary MAY only narrow—not expand—the Mandate's boundary.

```yaml
id: work-retention-review
kind: WorkEnvelope
mandateReference: {id: mandate-commercial-analysis, version: 1}
requestedResult: Draft a renewal-prioritisation decision note
owner: Commercial director
scope: [renewal-prioritisation]
tools: [draft.decision_note]
dataAccess: [customer_health_summary]
approvalRights: [reviewed_draft]
authorityLevel: 1
expiresAt: "2026-12-01T00:00:00Z"
```

## ExecutionPackage

An `ExecutionPackage` is the human-and-agent plan inside one WorkEnvelope. It has no independent authority. It MUST reference one envelope and remain within that envelope's boundary.

```yaml
id: package-retention-review
kind: ExecutionPackage
workEnvelopeReference: {id: work-retention-review, version: 1}
plannedSteps:
  - Review the sourced customer-health summary.
  - Prepare a decision-note draft.
expectedOutputs: [Decision-note draft]
dependencies: [Current customer-health summary]
timing: Before the next commercial review
acceptanceCriteria:
  - Names source limits and unresolved assumptions.
```

The current simple profile uses ordered strings. A future minor version SHOULD support structured plan steps with ID, purpose, inputs, outputs, dependencies, and acceptance criteria. A step MUST NOT smuggle in tool calls, credentials, or an autonomous runbook.

## ExecutionRequest

An `ExecutionRequest` names one proposed action and points to both its `ExecutionPackage` and applicable `RevocationPolicy`. The local profile requires `action`, `tool`, `target`, `requestedAuthority`, `approvalRequired`, and `approvalExpiresAt`.

```yaml
id: request-retention-note
kind: ExecutionRequest
executionPackageReference: {id: package-retention-review, version: 1}
revocationPolicyReference: {id: policy-retention-draft, version: 1}
action: prepare decision-note draft
tool: draft.decision_note
target: local draft
requestedAuthority: 1
approvalRequired: false
approvalExpiresAt: null
redactedParameters:
  customerHealthSummary: {sourceReference: demo:objective-retention}
```

| Outcome | Meaning |
|---|---|
| `allowed` | Structurally in supplied local boundaries; never execution permission. |
| `approval_required` | A future boundary requires approval; the package does not obtain it. |
| `denied` | The request is outside a declared boundary. |
| `escalated` | Context, ownership, consistency, expiry, or authority is ambiguous. |

`redactedParameters` MUST NOT contain raw secrets. A platform execution profile SHOULD accept secret references supplied by the platform rather than secret values in a package.

## EvidenceBundle and EvidenceEvent

`EvidenceBundle` is the package-level export: context, object versions, policy classifications, output references, corrections, actors, and timestamps for one work envelope. `EvidenceEvent` is the durable atomic record.

```yaml
id: event-context-retrieved
kind: EvidenceEvent
occurredAt: "2026-10-17T08:00:00Z"
workEnvelopeReference: {id: work-retention-review, version: 1}
eventType: context_retrieved
payload:
  contextPackageReference: {id: context-retention-review, version: 1}
```

An event MUST point to one WorkEnvelope, include at least one source reference, name an extensible `eventType`, record `occurredAt`, and carry an object payload. An export MAY include `previousHash` and `recordHash`; that detects alteration of the exported sequence only. It does not establish immutable storage, retention guarantees, or platform audit.

# Cross-cutting controls

## RevocationPolicy

A future execution-capable profile MUST bind every request to an active `RevocationPolicy` matching the same Mandate and WorkEnvelope chain. The policy describes how a future platform would suspend, narrow, or restore authority; it does not mean Kentaro can perform those operations today.

```yaml
id: policy-retention-draft
kind: RevocationPolicy
policyId: policy-retention-draft
scope: capability
authorityChain:
  mandateReference: {id: mandate-commercial-analysis, version: 1}
  workEnvelopeReference: {id: work-retention-review, version: 1}
accountableOwnerRole: Service Owner
suspensionTriggers:
  - outside_work_envelope_or_mandate
  - source_evidence_missing_stale_or_contradictory
  - deterministic_validation_or_policy_control_failed
expiryOrReviewDate: "2026-12-01T00:00:00Z"
localStatus: declared_active
```

A policy needs a single identity (`policyId` equal to its object `id`), a scope, authority-chain references, suspend/restore/narrow/emergency roles, accountable ownership, minimum suspension triggers, a positive repeated-failure threshold, action and notification requirements, expiry/review, and local status (`declared_active` or `simulated_suspended`). A cross-organization standard SHOULD use portable role identifiers rather than local organisation titles.

## Correction

A `Correction` is structured human or system feedback. It MUST name a target object version, a kind (`output`, `context`, `mandate`, `policy`, or `tool`), a destination, and a summary. It records a reason to improve something; it MUST NOT silently rewrite the target.

```yaml
id: correction-retention-wording
kind: Correction
targetReference: {id: package-retention-review, version: 1}
correctionKind: output
destination: local package revision
summary: Use the agreed renewal terminology.
```

# Common object contract

Every object uses a stable `id`, `kind`, positive instance `version`, `createdAt`, declared `actor`, `sourceReferences`, and `relationshipReferences`. `actor` is attribution, not authentication proof. A `Reference` always includes an ID and version; a source observation also includes `retrievedAt`.

```json
{
  "id": "work-retention-review",
  "kind": "WorkEnvelope",
  "version": 1,
  "createdAt": "2026-10-17T08:00:00Z",
  "actor": "demo-user",
  "sourceReferences": [{"id": "demo:objective-retention", "version": 1, "retrievedAt": "2026-10-17T08:00:00Z"}],
  "relationshipReferences": [{"id": "mandate-commercial-analysis", "version": 1}]
}
```

# Integrity rules

The value of ODPH is in its relationships rather than its field names. A conforming deterministic validator MUST apply these rules in addition to schema validation.

| Condition | Required result |
|---|---|
| WorkEnvelope points to a missing or wrong Mandate version | invalid / denied |
| Envelope boundary is not a Mandate subset | invalid / denied |
| ExecutionPackage has no WorkEnvelope or broadens it | invalid / denied |
| Request has no matching RevocationPolicy chain | invalid / denied |
| Request tool or authority exceeds its envelope | denied |
| Owner is absent; a source is stale or conflicting; policy is expired | escalated |
| Request declares an approval requirement | approval_required |
| Revocation status is simulated suspended | denied; no dispatch |
| Evidence lacks source ID, version, or retrieval time | invalid |

```text
Schema validation: is the document well shaped?
Relationship validation: do references, subsets, freshness, and authority chains hold?
Platform enforcement: may a real external action happen now?
```

Passing the first two checks MUST NOT alter an external system.

# Conformance profiles

Package metadata MUST declare a conformance profile. An implementation MUST disclose its profile in output and MUST NOT claim a stronger profile merely because it rendered a plan, screenshot, or evidence file.

| Profile | Permitted claim | Prohibited claim |
|---|---|---|
| `local-only` | Local validation, deterministic evaluation, draft/report generation, redacted evidence export. | Live access, real approval, live suspension, external action. |
| `platform-governed-read` | Read from a verified platform contract with provenance. | Writing or approval processing unless separately declared. |
| `platform-governed-execution` | A platform may execute after its own scope, approval, identity, revocation, and audit checks. | Treating local `allowed` as permission. |

# Schema and examples

The canonical schema is YAML serialization of JSON Schema. The published JSON schema is mechanically derived from it. Schema validation handles document shape and local object fields; deterministic validation handles cross-object references, subset rules, chain matching, freshness, and outcomes.

```yaml
schema: https://opendataproducts.org/odph-v1.0/schema/odph.yaml
version: "0.1-draft"
kind: OpenDataProductHarness
package:
  metadata:
    id: odph-retention-review-2026-10
    conformanceProfile: kentaro-v0.1-local-only
  objects: [] # Objects are listed in full-retention-review.yaml
```

Use the full example for an end-to-end synthetic package and standalone examples when authoring or testing one object kind. Do not present a loose YAML template as a "YAML Schema".

# Questions before ratification

1. What is the formal name and standards-family home: package, work contract, governance profile, or operating-framework component?
2. Is the top-level format one self-contained package, a folder of standalone fragments, or both?
3. Can authority levels receive portable meanings, or must they be profile-specific?
4. Which role vocabulary and data-classification taxonomy can be portable?
5. What output-reference, identity, approval, revocation, idempotency, receipt, retention, and audit contracts are required for a true execution profile?
6. Which relationships should be represented as ODPG relationships rather than embedded references?

# Recommended first publication scope

Publish `0.1-draft` as a local planning-and-evidence interchange model: the six conceptual parts and two controls; JSON Schema and its YAML serialization; full/minimal/standalone examples; JSONL object records; deterministic validation; and agent guidance. Defer live execution, approval semantics, credentials, tenant controls, retention, and audit claims until a verified platform contract exists.

```text
Useful now: clear, validated, reviewable work packages.
Deferred: business authority and external execution.
```

# Source basis

This material is grounded in Kentaro's local schema validator, deterministic policy evaluator, evidence exporter, and synthetic governance example. The ODPC v1.0 presentation pattern informed the document structure: human-readable specification, schema, JSONL records, standalone and full examples, validator, and agent guidance.

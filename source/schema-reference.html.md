---
title: Schema reference | ODPH v0.2
---

# Schema reference

The canonical v0.2 contract is [`change-control.yaml`](odph-v0.2/schema/change-control.yaml). It validates eight peer top-level object kinds. The six governed-work objects use common identity, attribution, source, and relationship fields; `ChangeAction` and `ChangeTask` retain their constrained change-control structures.

## Top-level object kinds

| Object kind | Required structure | Detailed field table and example |
| --- | --- | --- |
| `ContextPackage` | Common fields, `retrievalScope`, `freshness`, `conflicts`. | [ContextPackage](index.html#contextpackage) |
| `Mandate` | Common fields, durable boundary fields, business area, owner, expiry. | [Mandate](index.html#mandate) |
| `WorkEnvelope` | Common fields, mandate reference, narrowed boundary, result, owner, expiry. | [WorkEnvelope](index.html#workenvelope) |
| `ExecutionPackage` | Common fields, envelope reference, boundary, plan, outputs, dependencies, timing, criteria. | [ExecutionPackage](index.html#executionpackage) |
| `ExecutionRequest` | Common fields, execution-package and revocation-policy references, proposed action and approval limit. | [ExecutionRequest](index.html#executionrequest) |
| `EvidenceEvent` | Common fields, event time, envelope reference, type, payload. | [EvidenceEvent](index.html#evidenceevent) |
| `ChangeAction` | v0.2 change-control header, context, intent, one specification, review, criteria. | [ChangeAction](index.html#changeaction) |
| `ChangeTask` | v0.2 change-control header, context, intent, action references, review, criteria. | [ChangeTask](index.html#changetask) |

## Common governed-work fields

`ContextPackage`, `Mandate`, `WorkEnvelope`, `ExecutionPackage`, `ExecutionRequest`, and `EvidenceEvent` require `kind`, `metadata`, and `provenance`. `metadata` groups `id`, positive integer `version`, `createdAt`, and `actor`; `provenance` groups `sourceReferences` and `relationshipReferences`. A source reference has `id` and `version`, with `retrievedAt` when it is an observation; relationship references link other ODPH objects by ID and version.

## ChangeAction and ChangeTask fields

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

### `metadata`

Required: `id`, `title`, `requestedBy`, `createdAt`. `id` is a string of 3–128 characters matching `^[a-z0-9][a-z0-9-]*$`. `title` and `requestedBy` are non-empty strings; `createdAt` is an RFC 3339 date-time string. Optional `parentTestCase` and `parentChangeTask` use the same identifier rule.

### `graphContext`

Required: `source: maysano` and `baseGraphRevision`, which is a non-negative integer or non-empty string. Optional `requiredObjects` is an array of object references. Each reference requires `id` (identifier) and `expectedVersion` (non-negative integer or non-empty string), and may declare `specificationFamily` as `ODPC`, `ODPS`, or `ODPG`.

### `intent` and `review`

`intent` requires non-empty `businessOwner`, `reason`, and `expectedOutcome`, plus `policyProfile`, which uses the identifier rule. `review.requiredRoles` is a non-empty, unique array of non-empty strings. `review.approvalExpiresAt` is optional and uses the date-time format.

## `ChangeAction.specification`

`ChangeAction` additionally requires `specification`.

| Element name | Type | Options | Description |
| --- | --- | --- |
| `operation` | string | Required; `create` or `update` | Requested direct Maysano resource operation. `update` requires `expectedVersion`. |
| `family` | string | Required; `ODPC`, `ODPS`, or `ODPG` | Standard-family schema against which the referenced file is validated. |
| `file` | string | Required; contained relative `.yaml` or `.yml` path | File location; it cannot start with `/` or contain `..` path traversal. |
| `sha256` | string | Required; exactly 64 hexadecimal characters | SHA-256 checksum of the referenced file bytes. |
| `expectedVersion` | integer or string | Required for `update`; integer is at least `0`, string has minimum length 1 | Version expected by Maysano before an update is accepted. |

The referenced file carries the object identity, business fields, and domain semantics. The action does not duplicate them.

## `ChangeTask.actions`

`ChangeTask` additionally requires `actions`: an array with at least two references. Every reference requires `id` and `actionFile`; `actionFile` has the same contained relative-YAML rule as `specification.file`. Optional `dependsOn` is an array of unique action IDs in the same task. Runtime validation rejects missing references, duplicate action IDs, and dependency cycles.

## Deliberate v0.2 limits

The eight object kinds form one packageable model. Boundary and evidence fields are declarative and do not become raw API request bodies or authority grants. The schema does not embed ODPC, ODPS, or ODPG content, and it does not add generic `link`, `unlink`, or `deprecate` operations.

---
title: Schema reference | ODPH v0.2
---

# Schema reference

The canonical v0.2 contract is [`kentaro-change.yaml`](odph-v0.2/schema/kentaro-change.yaml). `additionalProperties: false` is intentional at every Kentaro document object: unknown top-level or nested fields fail validation.

## Common fields

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

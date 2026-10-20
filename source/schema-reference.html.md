---
title: Schema reference | ODPH v0.2
---

# Schema reference

The canonical v0.2 contract is [`change-control.yaml`](odph-v0.2/schema/change-control.yaml). It validates eight peer top-level object kinds. The six governed-work objects use common identity, attribution, source, and relationship fields; `ChangeAction` and `ChangeTask` retain their constrained change-control structures.

## Top-level object kinds

<table>
<thead>
<tr>
<th>Object kind</th>
<th>Required structure</th>
<th>Detailed field table and example</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>ContextPackage</code></td>
<td>Common fields, <code>retrievalScope</code>, <code>freshness</code>, <code>conflicts</code>.</td>
<td><a href="index.html#contextpackage">ContextPackage</a></td>
</tr>
<tr>
<td><code>Mandate</code></td>
<td>Common fields, durable boundary fields, business area, owner, expiry.</td>
<td><a href="index.html#mandate">Mandate</a></td>
</tr>
<tr>
<td><code>WorkEnvelope</code></td>
<td>Common fields, mandate reference, narrowed boundary, result, owner, expiry.</td>
<td><a href="index.html#workenvelope">WorkEnvelope</a></td>
</tr>
<tr>
<td><code>ExecutionPackage</code></td>
<td>Common fields, envelope reference, boundary, plan, outputs, dependencies, timing, criteria.</td>
<td><a href="index.html#executionpackage">ExecutionPackage</a></td>
</tr>
<tr>
<td><code>ExecutionRequest</code></td>
<td>Common fields, execution-package and revocation-policy references, proposed action and approval limit.</td>
<td><a href="index.html#executionrequest">ExecutionRequest</a></td>
</tr>
<tr>
<td><code>EvidenceEvent</code></td>
<td>Common fields, event time, envelope reference, type, payload.</td>
<td><a href="index.html#evidenceevent">EvidenceEvent</a></td>
</tr>
<tr>
<td><code>ChangeAction</code></td>
<td>v0.2 change-control header, context, intent, one specification, review, criteria.</td>
<td><a href="index.html#changeaction">ChangeAction</a></td>
</tr>
<tr>
<td><code>ChangeTask</code></td>
<td>v0.2 change-control header, context, intent, action references, review, criteria.</td>
<td><a href="index.html#changetask">ChangeTask</a></td>
</tr>
</tbody>
</table>

## Common governed-work fields

`ContextPackage`, `Mandate`, `WorkEnvelope`, `ExecutionPackage`, `ExecutionRequest`, and `EvidenceEvent` require `kind`, `metadata`, and `provenance`. `metadata` groups the stable `id`, language-keyed `name` and `description`, positive integer `version`, `createdAt`, and `actor`; `provenance` groups `sourceReferences` and `relationshipReferences`. A source reference has `id` and `version`, with `retrievedAt` when it is an observation; relationship references link other ODPH objects by ID and version.

## ChangeAction and ChangeTask fields

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

### `metadata`

Required: `id`, `title`, `requestedBy`, `createdAt`. `id` is a string of 3–128 characters matching `^[a-z0-9][a-z0-9-]*$`. `title` and `requestedBy` are non-empty strings; `createdAt` is an RFC 3339 date-time string. Optional `parentTestCase` and `parentChangeTask` use the same identifier rule.

### `graphContext`

Required: `source: maysano` and `baseGraphRevision`, which is a non-negative integer or non-empty string. Optional `requiredObjects` is an array of object references. Each reference requires `id` (identifier) and `expectedVersion` (non-negative integer or non-empty string), and may declare `specificationFamily` as `ODPC`, `ODPS`, or `ODPG`.

### `intent` and `review`

`intent` requires non-empty `businessOwner`, `reason`, and `expectedOutcome`, plus `policyProfile`, which uses the identifier rule. `review.requiredRoles` is a non-empty, unique array of non-empty strings. `review.approvalExpiresAt` is optional and uses the date-time format.

## `ChangeAction.specification`

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

## `ChangeTask.actions`

`ChangeTask` additionally requires `actions`: an array with at least two references. Every reference requires `id` and `actionFile`; `actionFile` has the same contained relative-YAML rule as `specification.file`. Optional `dependsOn` is an array of unique action IDs in the same task. Runtime validation rejects missing references, duplicate action IDs, and dependency cycles.

## Deliberate v0.2 limits

The eight object kinds form one packageable model. Boundary and evidence fields are declarative and do not become raw API request bodies or authority grants. The schema does not embed ODPC, ODPS, or ODPG content, and it does not add generic `link`, `unlink`, or `deprecate` operations.

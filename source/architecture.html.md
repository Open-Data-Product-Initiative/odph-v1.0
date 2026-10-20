---
title: Architecture and responsibilities | ODPH v0.2
---

# Architecture and responsibilities

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

ODPH v0.2 packages eight peer top-level object kinds: ContextPackage, Mandate, WorkEnvelope, ExecutionPackage, ExecutionRequest, EvidenceEvent, ChangeAction, and ChangeTask. Object identity, business fields, domain semantics, and lifecycle state still belong in the referenced ODPC, ODPS, or ODPG file.

There are no raw relationship JSON, API request bodies, or runtime-cache details in this contract. Boundary fields describe a local governed-work model; they do not issue real tools, data access, approval rights, or authority.

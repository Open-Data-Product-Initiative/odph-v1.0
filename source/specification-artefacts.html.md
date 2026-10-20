---
title: Specification artefacts | ODPH v0.2
---

# Specification artefacts: ODPC, ODPS, ODPG

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

Every referenced file must be a contained relative `.yaml` or `.yml` path and must match the SHA-256 checksum in its action. The [validation guide](validation.html) describes the static and runtime checks.

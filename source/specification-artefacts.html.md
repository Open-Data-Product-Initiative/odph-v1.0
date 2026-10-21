---
title: Referenced specifications | ODPH v0.2
---

# Referenced specifications

An ODPH Change Package controls work over standards-owned artifacts; it does not re-model their domain fields.

<table>
<thead><tr><th>Suffix</th><th>Artifact</th><th>Role in a graph-change package</th></tr></thead>
<tbody>
<tr><td><code>.odpc.yaml</code></td><td>ODPC</td><td>Objective and use-case definitions.</td></tr>
<tr><td><code>.odps.yaml</code></td><td>ODPS</td><td>Data-product definition and governed output.</td></tr>
<tr><td><code>.odpg.yaml</code></td><td>ODPG</td><td>Current and target graph fragments plus graph-change work.</td></tr>
</tbody>
</table>

The package example uses a current ODPG fragment at revision 184, a target ODPG fragment, two ODPC files, and one ODPS file. Each file validates against its own declared standard schema before it can support a conformant package.

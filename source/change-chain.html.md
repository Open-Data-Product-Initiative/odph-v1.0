---
title: Generic change-chain example | ODPH v0.2
---

# Generic change-chain example

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

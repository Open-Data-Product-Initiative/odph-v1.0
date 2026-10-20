---
title: Generic change-chain example | ODPH v0.2
---

# Generic change-chain example

The principal v0.2 examples are linked source files in [`examples/change-chain/`](examples/change-chain/). The actions refer to their specification files from the bundle root so every reference remains contained.

| Test case | Expected specification artefacts |
| --- | --- |
| 01 | ODPC objective v1; ODPC use case v1; ODPG graph v1 |
| 02 | ODPS Primary Data Product v1; ODPG graph v2 |
| 03 | ODPS Primary Data Product v2 with revised SLA and DQ terms |
| 04 | ODPC second use case v1; ODPG graph v3 |
| 05 | ODPS Context Data Product v1; ODPS Primary Data Product v3, deprecated; ODPG graph v4 |
| 06 | ODPC secondary objective v1; ODPC secondary use case v1; ODPS Additional Data Product v1; ODPS Capacity Data Product v1; ODPG graph v5 |

Test cases 01–05 demonstrate direct actions. Test case 06 also provides the later composite `KentaroChangeTask`, which references its five separately valid action files and uses dependencies to order the individual resource writes.

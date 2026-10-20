---
title: Banking mortgage-renewal test chain | ODPH v0.2
---

# Banking mortgage-renewal test chain

The principal v0.2 examples are linked source files in [`examples/mortgage-renewal/`](examples/mortgage-renewal/). The actions refer to their specification files from the bundle root so every reference remains contained.

| Test case | Expected specification artefacts |
| --- | --- |
| 01 | ODPC objective v1; ODPC use case v1; ODPG graph v1 |
| 02 | ODPS Mortgage Renewal Eligibility v1; ODPG graph v2 |
| 03 | ODPS Mortgage Renewal Eligibility v2 with revised SLA and DQ terms |
| 04 | ODPC second use case v1; ODPG graph v3 |
| 05 | ODPS Mortgage Renewal Customer Profile v1; ODPS Mortgage Renewal Eligibility v3, deprecated; ODPG graph v4 |
| 06 | ODPC new objective v1; ODPC new use case v1; ODPS Mortgage Renewal Offer Eligibility v1; ODPS Mortgage Outreach Capacity Forecast v1; ODPG graph v5 |

Test cases 01–05 demonstrate direct actions. Test case 06 also provides the later composite `KentaroChangeTask`, which references its five separately valid action files and uses dependencies to order the individual resource writes.

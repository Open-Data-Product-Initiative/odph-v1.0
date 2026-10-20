---
title: Guided workflow execution | ODPH v0.2
---

# Guided workflow execution

Phase 1 v0.2 creates and submits one validated specification file at a time through Maysano resource APIs.

For the first change-chain test case the direct flow is:

1. ODPH retrieves bounded Maysano graph context.
2. The business owner agrees the objective draft.
3. ODPH creates and validates an ODPC objective YAML file.
4. ODPH sends that validated file to Maysano.
5. ODPH reads the returned objective identity and version.
6. The business owner agrees the use-case draft.
7. ODPH creates and validates an ODPC use-case YAML file.
8. ODPH sends that validated file to Maysano.
9. ODPH creates and validates an ODPG graph specification connecting objective and use case.
10. ODPH sends that graph file to Maysano.
11. ODPH records evidence for each completed action.

Direct workflows use ordered resource-level writes. There is no multi-action atomicity, automatic rollback, or all-or-nothing execution claim. If an action fails, ODPH stops and records completed actions, pending actions, returned Maysano identities and versions, the failure reason, and required reconciliation work.

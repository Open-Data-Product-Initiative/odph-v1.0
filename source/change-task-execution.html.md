---
title: Change Task execution | ODPH v0.2
---

# Change Task execution

Phase 2 later v0.2 validates a complete Change Task before execution. The initial implementation still sends individual Maysano API calls in declared dependency order; the task does not grant server-side atomic execution.

The composite example creates one objective, one use case, two data products, reuses an existing context data product, and updates one ODPG graph specification that expresses the new connections. Before each write ODPH verifies the agreed approvals, applicable object versions, and current graph revision. It records each submitted file identifier, Maysano identity and version, validation outcome, and reconciliation state.

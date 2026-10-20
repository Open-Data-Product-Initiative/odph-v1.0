---
title: ChangeTask reference | ODPH v0.2
---

# ChangeTask reference

A `ChangeTask` is a peer top-level object for a composite business change. It groups multiple existing `ChangeAction` files and declares their dependencies. It does not embed, copy, or recreate ODPC, ODPS, or ODPG content, and it does not replace the ContextPackage, Mandate, WorkEnvelope, ExecutionPackage, ExecutionRequest, or EvidenceEvent objects.

It records the bounded Maysano graph revision, action-file references, dependencies, required reviewers, acceptance criteria, execution status, and resulting evidence. Static validation rejects a task with fewer than two actions or unknown fields. Runtime validation rejects missing action files, duplicate action IDs, missing dependencies, and dependency cycles.

The [example Change Task](examples/change-chain/change-tasks/change-chain.yaml) is the composite example.

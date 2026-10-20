---
title: KentaroChangeTask reference | ODPH v0.2
---

# KentaroChangeTask reference

A `KentaroChangeTask` is a later v0.2 composite business change. It groups multiple existing `KentaroAction` files and declares their dependencies. It does not embed, copy, or recreate ODPC, ODPS, or ODPG content.

It records the bounded Maysano graph revision, action-file references, dependencies, required reviewers, acceptance criteria, execution status, and resulting evidence. Static validation rejects a task with fewer than two actions or unknown fields. Runtime validation rejects missing action files, duplicate action IDs, missing dependencies, and dependency cycles.

The [mortgage-renewal planning Change Task](examples/mortgage-renewal/change-tasks/mortgage-renewal-planning-change.yaml) is the composite example.

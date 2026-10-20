---
title: ChangeAction reference | ODPH v0.2
---

# ChangeAction reference

A `ChangeAction` is a peer top-level object for one agreed direct Maysano API operation. It references exactly one generated specification file and ODPH validates that file against the declared ODPC, ODPS, or ODPG schema before submitting it. It can be packaged with an `ExecutionRequest`, but it does not replace that request's plan, revocation, or approval chain.

`operation` is only `create` or `update`. An `update` requires `expectedVersion`. A connection change is an ODPG file update. A deprecation is a new ODPC or ODPS file version with its lifecycle state changed. A business-object update is a new ODPC or ODPS file version. `link`, `unlink`, and `deprecate` are not ChangeAction operations.

The action cannot embed or duplicate the referenced specification’s object fields. See the complete [schema reference](schema-reference.html) and the [first guided workflow](guided-workflow.html).

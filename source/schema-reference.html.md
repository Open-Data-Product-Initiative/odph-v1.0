---
title: Change Package schema reference | ODPH v0.2
---

# Change Package schema reference

The canonical source is [`change-package.yaml`](odph-v0.2/schema/change-package.yaml), a JSON Schema Draft 2020-12 document with a `oneOf` discriminator: `GraphChangePackage` or an invalid-by-design `GraphOperationStub`.

`graph-change` requires the header (`schema`, `version`, `kind`) and exactly six sections: `meta`, `need`, `auth`, `context`, `actions`, and `evidence`. Every object sets `additionalProperties: false`.

## Reusable definitions

Definitions are reused only where their meaning is identical across archetypes: `NonEmptyString`, `Identifier`, `Timestamp`, `RelativeYamlFile`, `Party`, `BusinessNeed`, `Authority`, `CurrentContext`, `ActionEvidence`, `PackageEvidence`, and `PackageKind`.

`NonEmptyString` has minimum length one; trim-only content is rejected by semantic validation. `Identifier` is three to 128 lower-case hyphenated characters. `Timestamp` is a date-time. `PackageKind` contains only `graph-change` and `graph-operation`.

## File references

`context.current.graph` and `context.target.graph` are ODPG files. `actions[].file` is an ODPC, ODPS, or ODPG file. Each referenced document validates against its own declared schema. ODPH intentionally has no `specificationFamily`, checksum, dependency, generic authority, generic boundary, policy-profile, or data-access model.

## Reserved graph-operation

`graph-operation` establishes an extension point for future ODPR-governed operational work. v0.2 defines neither its fields nor a permissive body. Raw schema validation makes it invalid and the implementation validator returns `unsupported-kind` before normal schema reporting.

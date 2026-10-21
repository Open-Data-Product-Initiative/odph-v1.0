---
title: Open Data Product Harness Change Package | ODPH v0.2
search: true
---

# Open Data Product Harness Change Package

ODPH v0.2 defines one machine-readable Change Package. It carries a business need into controlled work against a bounded company-graph fragment and records the evidence needed to judge the result. It is not a second company graph, permission system, execution API, or audit store. Maysano remains authoritative for graph state, applied changes, and authoritative evidence.

<aside class="warning">This is a v0.2 draft. A conformant package is controlled work, not authority to execute it. Maysano independently validates revision, authority, and realised graph state when applying work.</aside>

# Package archetypes

`kind` selects a package archetype. `graph-change` is complete and conformant in v0.2. `graph-operation` is reserved for future governed operational work using ODPR; it has no action or evidence model in this version and cannot accept arbitrary documents.

```yaml
kind: graph-operation
```

The marker above is reserved and unsupported in v0.2. The implementation validator reports `unsupported-kind` rather than treating it as a malformed graph-change package.

# Information continuity

For `graph-change`, information must remain continuous from the established business proposition to the verified result:

```text
BusinessNeed -> G0 -> G1 -> ordered actions -> action evidence -> verified outcome
```

`G0` is the selected current graph fragment at a Maysano revision. `G1` is the target graph fragment. Each action states the relevant need gap, the observed G0 finding, and the required G1 effect. A package cannot claim completion merely because files were generated.

# Graph-change model

Every complete graph-change package has a header and six required sections: `meta`, `need`, `auth`, `context`, `actions`, and `evidence`. All objects are closed: unknown fields are rejected.

## `meta`

`meta` identifies this package only. It is not a company graph node or a cross-package reference scheme. It requires a lower-case hyphenated `id`, a title, and creation time.

```yaml
meta:
  id: retention-intervention
  title: Improve retention intervention decisions
  created: '2026-10-21T10:00:00Z'
```

## `need`

`need` is the first-class business proposition established with the business user and relevant graph context. Its narrative is retained as `text`; the actor, situation, job, gap, outcome, and success tests make it machine-readable and testable. Graph-change requires both a graph success test and a business success test.

```yaml
need:
  text: Retention teams need a governed basis for deciding customer interventions.
  actor:
    type: team
    name: Retention teams
  situation: Before customer renewal
  job:
    type: decision
    text: Identify customers who need intervention.
  gap:
    type: missing
    text: The company graph has no governed retention decision path.
  outcome: Retention teams use an owned, governed decision basis.
  success:
    - type: graph
      test: The realised graph contains the retention path.
    - type: business
      test: The retention lead accepts the decision basis for operational use.
```

## `auth`

`auth` identifies the owner, authoriser, authorization time, and expiry for this one package. It deliberately has no reusable permission wrapper, tool grant, data-access list, or separate lifecycle object. The validator requires `until` to be later than `at` and rejects application after expiry.

```yaml
auth:
  owner:
    type: team
    name: Customer Insights
  by:
    type: role
    name: Director of Customer Insights
  at: '2026-10-21T10:00:00Z'
  until: '2026-11-30T23:59:59Z'
```

## `context`

`context` holds only the affected graph fragment, never the whole company graph. A graph-change requires both `current` and `target`. The current graph records its Maysano source, revision, retrieval time, and G0 graph file. The target graph file expresses G1. Both files must validate as ODPG and cannot be unchanged.

```yaml
context:
  current:
    source: maysano
    rev: 184
    at: '2026-10-21T09:50:00Z'
    graph: graph/retention-context.odpg.yaml
  target:
    graph: graph/retention-target.odpg.yaml
```

## `actions`

Actions are the ordered work required to realise G1. Each action changes one ODPC, ODPS, or ODPG YAML file. The referenced file declares and validates against its own standard-family schema; ODPH does not repeat a family label, checksum, dependency ID, or generic reference wrapper. `gap`, `finding`, and `effect` are mandatory and connect the action to the business need, G0, and G1.

```yaml
actions:
  - title: Create retention objective
    op: create
    file: artefacts/retention-objective.odpc.yaml
    gap: Retention teams lack a stated retention objective.
    finding: No current retention objective represents preventable customer churn.
    effect: A retention objective exists and is owned by Customer Insights.
    evidence:
      runState: pending
      graphState: pending
```

`op` is a closed enum: `create`, `update`, or `retire`. List position defines order; there are no action IDs or dependency references. `runState` proves the requested artefact change completed; `graphState` proves the realised graph satisfies that action's effect.

## `evidence`

Package evidence records the outcome state. It is not an unstructured event list. A package is complete only when every action has `runState: pass`, every action has `graphState: pass`, and `outcomeState: pass`. A passing outcome also requires both graph and business success tests to pass; business proof may require an authorised human decision.

```yaml
evidence:
  outcomeState: pending
```

# Schema reference

The canonical JSON Schema Draft 2020-12 source is [`change-package.yaml`](odph-v0.2/schema/change-package.yaml); [`change-package.json`](odph-v0.2/schema/change-package.json) is mechanically derived from it.

<table>
<thead><tr><th>Section</th><th>Required fields</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>meta</code></td><td><code>id</code>, <code>title</code>, <code>created</code></td><td>Identifies the package.</td></tr>
<tr><td><code>need</code></td><td><code>text</code>, <code>actor</code>, <code>situation</code>, <code>job</code>, <code>gap</code>, <code>outcome</code>, <code>success</code></td><td>Establishes the business proposition and tests.</td></tr>
<tr><td><code>auth</code></td><td><code>owner</code>, <code>by</code>, <code>at</code>, <code>until</code></td><td>Bounds the authorization for this package.</td></tr>
<tr><td><code>context</code></td><td><code>current</code>, <code>target</code></td><td>States the relevant G0 and intended G1.</td></tr>
<tr><td><code>actions</code></td><td>one or more complete actions</td><td>Orders controlled ODPC, ODPS, and ODPG changes.</td></tr>
<tr><td><code>evidence</code></td><td><code>outcomeState</code></td><td>Records whether the verified outcome passed.</td></tr>
</tbody>
</table>

`Party.type` is one of `person`, `role`, `team`, `organisation`, `customer`, `partner`, or `system`. Job types are `decision`, `service`, `process`, `capability`, or `obligation`; gap types are `missing`, `incomplete`, `unlinked`, `unowned`, `conflicting`, or `outdated`. Success types are `graph` and `business`. Evidence states are `pending`, `pass`, and `fail`.

`RelativeYamlFile` must be a relative `.yaml` or `.yml` path and cannot begin with `/` or contain `..`. `SpecFile` is limited to `.odpc.yaml`, `.odps.yaml`, or `.odpg.yaml` (and `.yml` equivalents); graph context files are limited to ODPG suffixes.

# Complete graph-change example

The complete retention package and every referenced artifact are published in [`examples/retention-change/`](examples/retention-change/). It is the primary v0.2 example.

```yaml
schema: https://opendataproducts.org/odph/v0.2/schema/change-package.yaml
version: 0.2-draft
kind: graph-change

meta:
  id: retention-intervention
  title: Improve retention intervention decisions
  created: '2026-10-21T10:00:00Z'

need:
  text: >-
    Retention teams need a governed basis for deciding which customers need
    intervention before renewal.
  actor:
    type: team
    name: Retention teams
  situation: Before customer renewal
  job:
    type: decision
    text: Identify customers who need intervention.
  gap:
    type: missing
    text: >-
      The company graph has no retention objective, intervention use case, or
      governed product that provides the required customer signals.
  outcome: >-
    Retention teams use an owned, governed decision basis for customer
    interventions.
  success:
    - type: graph
      test: >-
        The realised graph contains the retention objective, intervention use
        case, governed product, ownership, and required relationships.
    - type: business
      test: The retention lead accepts the decision basis for operational use.

auth:
  owner:
    type: team
    name: Customer Insights
  by:
    type: role
    name: Director of Customer Insights
  at: '2026-10-21T10:00:00Z'
  until: '2026-11-30T23:59:59Z'

context:
  current:
    source: maysano
    rev: 184
    at: '2026-10-21T09:50:00Z'
    graph: graph/retention-context.odpg.yaml
  target:
    graph: graph/retention-target.odpg.yaml

actions:
  - title: Create retention objective
    op: create
    file: artefacts/retention-objective.odpc.yaml
    gap: Retention teams lack a stated retention objective.
    finding: No current retention objective represents preventable customer churn.
    effect: A retention objective exists and is owned by Customer Insights.
    evidence:
      runState: pending
      graphState: pending
  - title: Create retention-intervention use case
    op: create
    file: artefacts/retention-intervention.odpc.yaml
    gap: Retention teams lack a defined intervention decision.
    finding: No current retention use case connects customer signals to intervention work.
    effect: A retention-intervention use case contributes to the retention objective.
    evidence:
      runState: pending
      graphState: pending
  - title: Update Customer Signals for retention use
    op: update
    file: artefacts/customer-signals.odps.yaml
    gap: Retention teams need a governed source of customer signals.
    finding: Customer Signals exists but does not support the retention intervention decision.
    effect: Customer Signals supports the retention-intervention use case with a governed output.
    evidence:
      runState: pending
      graphState: pending
  - title: Connect the retention path in the company graph
    op: update
    file: graph/retention-target.odpg.yaml
    gap: The intended retention decision path is not governed.
    finding: No current retention graph path links an objective, use case, and product.
    effect: Customer Signals supports the retention-intervention use case and retention objective.
    evidence:
      runState: pending
      graphState: pending

evidence:
  outcomeState: pending
```

# Conformance and validator behaviour

The validator first reads top-level `kind`. `graph-change` receives full schema and deterministic validation; `graph-operation` receives the explicit `unsupported-kind` diagnostic; every other value receives `unknown-kind`. For graph-change it validates schema shape, expiry and authorization range, local ODPG and standard-family files, meaningful G0/G1 difference, each action's need/G0/G1 connection, and completion state. When Maysano supplies an apply-time revision, a mismatch returns `graph-drift` and requires a new package.

The deterministic validator does not infer business semantics from JSON Schema. It checks the declared package against supplied graph artifacts; Maysano must independently validate the current graph revision and realised graph state immediately before applying work.

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

```yaml
schema: https://opendataproducts.org/odph/v0.2/schema/change-package.yaml
version: 0.2-draft
kind: graph-change
```

Every complete graph-change package has a header and six required sections: `meta`, `need`, `auth`, `context`, `actions`, and `evidence`. All objects are closed: unknown fields are rejected.

<table>
<thead><tr><th>Element name</th><th>Type</th><th>Mandatory</th><th>Options</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>schema</code></td><td>string</td><td>Yes</td><td>Canonical Change Package URL</td><td>Declares the schema used to validate this document.</td></tr>
<tr><td><code>version</code></td><td>string</td><td>Yes</td><td><code>0.2-draft</code></td><td>Declares the draft contract version.</td></tr>
<tr><td><code>kind</code></td><td>string</td><td>Yes</td><td><code>graph-change</code></td><td>Selects the only conformant v0.2 package archetype.</td></tr>
</tbody>
</table>

## `meta`

```yaml
meta:
  id: retention-intervention
  title: Improve retention intervention decisions
  created: '2026-10-21T10:00:00Z'
```

`meta` identifies this package only. It is not a company graph node or a cross-package reference scheme. It requires a lower-case hyphenated `id`, a title, and creation time.

<table>
<thead><tr><th>Element name</th><th>Type</th><th>Mandatory</th><th>Options</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>meta</code></td><td>object</td><td>Yes</td><td>Closed</td><td>Package metadata. It identifies this package and is not a graph node or reference mechanism.</td></tr>
<tr><td><code>meta.id</code></td><td>string</td><td>Yes</td><td>3–128 characters, <code>^[a-z0-9][a-z0-9-]*$</code></td><td>Stable, lower-case hyphenated identifier for this package.</td></tr>
<tr><td><code>meta.title</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Human-readable title for the controlled business change.</td></tr>
<tr><td><code>meta.created</code></td><td>string</td><td>Yes</td><td>RFC 3339 date-time</td><td>Time at which this package version was created.</td></tr>
</tbody>
</table>

## `need`

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

`need` is the first-class business proposition established with the business user and relevant graph context. Its narrative is retained as `text`; the actor, situation, job, gap, outcome, and success tests make it machine-readable and testable. Graph-change requires both a graph success test and a business success test.

<table>
<thead><tr><th>Element name</th><th>Type</th><th>Mandatory</th><th>Options</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>need</code></td><td>object</td><td>Yes</td><td>Closed</td><td>The complete, testable business proposition for this package.</td></tr>
<tr><td><code>need.text</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Preserves the business user’s narrative in their own terms.</td></tr>
<tr><td><code>need.actor</code></td><td>object (<code>Party</code>)</td><td>Yes</td><td><code>type</code> and <code>name</code></td><td>Named business actor whose need is being addressed.</td></tr>
<tr><td><code>need.actor.type</code></td><td>string</td><td>Yes</td><td><code>person</code>, <code>role</code>, <code>team</code>, <code>organisation</code>, <code>customer</code>, <code>partner</code>, <code>system</code></td><td>Classifies the actor without inventing an ODPH reference identity.</td></tr>
<tr><td><code>need.actor.name</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Business-readable name of the actor. The company graph remains authoritative where an identity exists.</td></tr>
<tr><td><code>need.situation</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Business situation in which the need matters.</td></tr>
<tr><td><code>need.job</code></td><td>object</td><td>Yes</td><td><code>type</code> and <code>text</code></td><td>Classifies and describes the work the actor needs to accomplish.</td></tr>
<tr><td><code>need.job.type</code></td><td>string</td><td>Yes</td><td><code>decision</code>, <code>service</code>, <code>process</code>, <code>capability</code>, <code>obligation</code></td><td>Closed job category.</td></tr>
<tr><td><code>need.job.text</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Specific job statement in business language.</td></tr>
<tr><td><code>need.gap</code></td><td>object</td><td>Yes</td><td><code>type</code> and <code>text</code></td><td>Known deficiency between the current state and the needed decision basis.</td></tr>
<tr><td><code>need.gap.type</code></td><td>string</td><td>Yes</td><td><code>missing</code>, <code>incomplete</code>, <code>unlinked</code>, <code>unowned</code>, <code>conflicting</code>, <code>outdated</code></td><td>Closed classification of the business or graph gap.</td></tr>
<tr><td><code>need.gap.text</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Specific explanation of the deficiency.</td></tr>
<tr><td><code>need.outcome</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Business condition intended when the package is complete.</td></tr>
<tr><td><code>need.success</code></td><td>array of objects</td><td>Yes</td><td>One or more items</td><td>Tests used to judge the graph and business outcome.</td></tr>
<tr><td><code>need.success[].type</code></td><td>string</td><td>Yes</td><td><code>graph</code> or <code>business</code>; at least one of each</td><td>Distinguishes realised graph proof from business acceptance.</td></tr>
<tr><td><code>need.success[].test</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Observable condition that must pass for that success dimension.</td></tr>
</tbody>
</table>

## `auth`

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

`auth` identifies the owner, authoriser, authorization time, and expiry for this one package. It deliberately has no reusable permission wrapper, tool grant, data-access list, or separate lifecycle object. The validator requires `until` to be later than `at` and rejects application after expiry.

<table>
<thead><tr><th>Element name</th><th>Type</th><th>Mandatory</th><th>Options</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>auth</code></td><td>object</td><td>Yes</td><td>Closed</td><td>Authorization facts that apply only to this Change Package.</td></tr>
<tr><td><code>auth.owner</code></td><td>object (<code>Party</code>)</td><td>Yes</td><td><code>type</code> and <code>name</code></td><td>Business owner accountable for the need and its intended outcome.</td></tr>
<tr><td><code>auth.by</code></td><td>object (<code>Party</code>)</td><td>Yes</td><td><code>type</code> and <code>name</code></td><td>Named person, role, team, or other actor authorising this package.</td></tr>
<tr><td><code>auth.at</code></td><td>string</td><td>Yes</td><td>RFC 3339 date-time</td><td>Time at which the package was authorised.</td></tr>
<tr><td><code>auth.until</code></td><td>string</td><td>Yes</td><td>RFC 3339 date-time; later than <code>auth.at</code></td><td>Exclusive authorization boundary. Application after this time is rejected.</td></tr>
</tbody>
</table>

## `context`

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

`context` holds only the affected graph fragment, never the whole company graph. A graph-change requires both `current` and `target`. The current graph records its Maysano source, revision, retrieval time, and G0 graph file. The target graph file expresses G1. Both files must validate as ODPG and cannot be unchanged.

<table>
<thead><tr><th>Element name</th><th>Type</th><th>Mandatory</th><th>Options</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>context</code></td><td>object</td><td>Yes</td><td>Closed</td><td>Bounded G0 and G1 graph fragments relevant to this package.</td></tr>
<tr><td><code>context.current</code></td><td>object</td><td>Yes</td><td><code>source</code>, <code>rev</code>, <code>at</code>, <code>graph</code></td><td>Selected current graph state, G0.</td></tr>
<tr><td><code>context.current.source</code></td><td>string</td><td>Yes</td><td><code>maysano</code></td><td>Identifies the authoritative source for the supplied current revision.</td></tr>
<tr><td><code>context.current.rev</code></td><td>integer</td><td>Yes</td><td>0 or greater</td><td>Maysano revision expected when the package is applied. A mismatch is graph drift.</td></tr>
<tr><td><code>context.current.at</code></td><td>string</td><td>Yes</td><td>RFC 3339 date-time</td><td>Time at which the current graph fragment was selected.</td></tr>
<tr><td><code>context.current.graph</code></td><td>filepath</td><td>Yes</td><td>Relative <code>.odpg.yaml</code> or <code>.odpg.yml</code></td><td>ODPG file that expresses G0. Absolute paths and <code>..</code> traversal are rejected.</td></tr>
<tr><td><code>context.target</code></td><td>object</td><td>Yes</td><td><code>graph</code></td><td>Intended target graph state, G1.</td></tr>
<tr><td><code>context.target.graph</code></td><td>filepath</td><td>Yes</td><td>Relative <code>.odpg.yaml</code> or <code>.odpg.yml</code></td><td>ODPG file that expresses G1. It must differ meaningfully from G0.</td></tr>
</tbody>
</table>

## `actions`

```yaml
actions:
  - id: create-retention-objective
    title: Create retention objective
    op: create
    file: artefacts/retention-objective.odpc.yaml
    gap: Retention teams lack a stated retention objective.
    finding: No current retention objective represents preventable customer churn.
    effect: A retention objective exists and is owned by Customer Insights.
    evidence:
      runState: pending
      graphState: pending

  - id: create-churn-use-case
    title: Create preventable churn use case
    op: create
    file: artefacts/preventable-churn-use-case.odpc.yaml
    gap: No agreed use case turns the retention objective into defined work.
    finding: Existing retention activity focuses on campaign delivery, not churn prevention.
    effect: A use case defines the target population, value hypothesis and success measures.
    evidence:
      runState: pending
      graphState: pending

  - id: create-customer-retention-data-product
    title: Create customer retention signals data product
    op: create
    file: artefacts/customer-retention-signals.odps.yaml
    gap: Teams lack a governed data product for retention decision-making.
    finding: Churn-related signals exist across CRM, billing and support systems.
    effect: A governed data product makes approved retention signals available for the use case.
    evidence:
      runState: pending
      graphState: pending

  - id: link-retention-initiative-in-graph
    title: Link the objective, use case and data product
    op: apply
    file: artefacts/retention-churn-relationships.odpg.yaml
    gap: The new portfolio objects have no declared relationships.
    finding: The business graph does not yet connect the retention objective to its delivery assets.
    effect: >
      The objective is linked to the use case, and the use case is linked
      to the supporting data product.
    evidence:
      runState: pending
      graphState: pending
```

Actions are the ordered work required to realise G1. Each action changes one ODPC, ODPS, or ODPG YAML file. The referenced file declares and validates against its own standard-family schema; ODPH does not repeat a family label, checksum, dependency ID, or generic reference wrapper. `gap`, `finding`, and `effect` are mandatory and connect the action to the business need, G0, and G1.

<table>
<thead><tr><th>Element name</th><th>Type</th><th>Mandatory</th><th>Options</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>actions</code></td><td>array of objects</td><td>Yes</td><td>One or more uniquely identified items</td><td>Ordered work required to realise G1. Array position is the action order.</td></tr>
<tr><td><code>actions[].id</code></td><td>string</td><td>Yes</td><td>3–128 lower-case hyphenated characters; unique within the package</td><td>Stable action identifier for evidence, review, and references to this specific controlled change.</td></tr>
<tr><td><code>actions[].title</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Human-readable statement of the change.</td></tr>
<tr><td><code>actions[].op</code></td><td>string</td><td>Yes</td><td><code>create</code>, <code>update</code>, <code>retire</code>, <code>apply</code></td><td>Closed operation applied to the referenced standard artifact. <code>apply</code> requires an ODPG file.</td></tr>
<tr><td><code>actions[].file</code></td><td>filepath</td><td>Yes</td><td>Relative <code>.odpc.yaml</code>, <code>.odps.yaml</code>, or <code>.odpg.yaml</code> (or <code>.yml</code>)</td><td>Standard-owned artifact to validate. The file declares its own ODPC, ODPS, or ODPG schema.</td></tr>
<tr><td><code>actions[].gap</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Relevant fact from <code>need.gap</code> that makes this action necessary.</td></tr>
<tr><td><code>actions[].finding</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Relevant observed fact in G0. The semantic validator checks that it is grounded in the supplied current graph.</td></tr>
<tr><td><code>actions[].effect</code></td><td>string</td><td>Yes</td><td>Non-empty</td><td>Required condition in G1. The semantic validator checks that the target graph contains it.</td></tr>
<tr><td><code>actions[].evidence</code></td><td>object</td><td>Yes</td><td><code>runState</code> and <code>graphState</code></td><td>Per-action evidence of execution and realised graph state.</td></tr>
<tr><td><code>actions[].evidence.runState</code></td><td>string</td><td>Yes</td><td><code>pending</code>, <code>pass</code>, <code>fail</code></td><td>Whether the specified artifact change completed successfully.</td></tr>
<tr><td><code>actions[].evidence.graphState</code></td><td>string</td><td>Yes</td><td><code>pending</code>, <code>pass</code>, <code>fail</code></td><td>Whether the realised graph satisfies this action’s declared effect.</td></tr>
</tbody>
</table>

`id` is required and unique within the package. `op` is a closed enum: `create`, `update`, `retire`, or `apply`; `apply` requires an ODPG file. List position defines order. `runState` proves the requested artefact change completed; `graphState` proves the realised graph satisfies that action's effect.

## `evidence`

```yaml
evidence:
  outcomeState: pending
```

Package evidence records the outcome state. It is not an unstructured event list. A package is complete only when every action has `runState: pass`, every action has `graphState: pass`, and `outcomeState: pass`. A passing outcome also requires both graph and business success tests to pass; business proof may require an authorised human decision.

<table>
<thead><tr><th>Element name</th><th>Type</th><th>Mandatory</th><th>Options</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>evidence</code></td><td>object</td><td>Yes</td><td>Closed</td><td>Package-level evidence state.</td></tr>
<tr><td><code>evidence.outcomeState</code></td><td>string</td><td>Yes</td><td><code>pending</code>, <code>pass</code>, <code>fail</code></td><td>Outcome verdict. <code>pass</code> is valid only when all action run and graph states pass and both success dimensions are proven.</td></tr>
</tbody>
</table>

# Schema reference

The canonical JSON Schema Draft 2020-12 source is [`change-package.yaml`](odph-v0.2/schema/change-package.yaml); [`change-package.json`](odph-v0.2/schema/change-package.json) is mechanically derived from it.

<table>
<thead><tr><th>Section</th><th>Mandatory</th><th>Optional</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td>Document</td><td><code>schema</code>, <code>version</code>, <code>kind</code></td><td>None</td><td>Identifies the v0.2 Change Package contract.</td></tr>
<tr><td><code>meta</code></td><td><code>id</code>, <code>title</code>, <code>created</code></td><td>None</td><td>Identifies the package.</td></tr>
<tr><td><code>need</code></td><td><code>text</code>, <code>actor</code>, <code>situation</code>, <code>job</code>, <code>gap</code>, <code>outcome</code>, <code>success</code></td><td>None</td><td>Establishes the business proposition and tests.</td></tr>
<tr><td><code>auth</code></td><td><code>owner</code>, <code>by</code>, <code>at</code>, <code>until</code></td><td>None</td><td>Bounds the authorization for this package.</td></tr>
<tr><td><code>context</code></td><td><code>current</code>, <code>target</code></td><td>None</td><td>States the relevant G0 and intended G1.</td></tr>
<tr><td><code>actions</code></td><td>At least one uniquely identified action</td><td>None</td><td>Orders controlled ODPC, ODPS, and ODPG changes.</td></tr>
<tr><td>Package <code>evidence</code></td><td><code>outcomeState</code></td><td>None</td><td>Records whether the verified outcome passed.</td></tr>
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
      governed product that provides the required customer signals; the
      portfolio objects and their relationships are absent.
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
  - id: create-retention-objective
    title: Create retention objective
    op: create
    file: artefacts/retention-objective.odpc.yaml
    gap: Retention teams lack a stated retention objective.
    finding: No current retention objective represents preventable customer churn.
    effect: A retention objective exists and is owned by Customer Insights.
    evidence:
      runState: pending
      graphState: pending
  - id: create-churn-use-case
    title: Create preventable churn use case
    op: create
    file: artefacts/preventable-churn-use-case.odpc.yaml
    gap: No agreed use case turns the retention objective into defined work.
    finding: Existing retention activity focuses on campaign delivery, not churn prevention.
    effect: A use case defines the target population, value hypothesis and success measures.
    evidence:
      runState: pending
      graphState: pending
  - id: create-customer-retention-data-product
    title: Create customer retention signals data product
    op: create
    file: artefacts/customer-retention-signals.odps.yaml
    gap: Teams lack a governed data product for retention decision-making.
    finding: Churn-related signals exist across CRM, billing and support systems.
    effect: A governed data product makes approved retention signals available for the use case.
    evidence:
      runState: pending
      graphState: pending
  - id: link-retention-initiative-in-graph
    title: Link the objective, use case and data product
    op: apply
    file: artefacts/retention-churn-relationships.odpg.yaml
    gap: The new portfolio objects have no declared relationships.
    finding: The business graph does not yet connect the retention objective to its delivery assets.
    effect: >-
      The objective is linked to the use case, and the use case is linked to
      the supporting data product.
    evidence:
      runState: pending
      graphState: pending

evidence:
  outcomeState: pending
```

# Conformance and validator behaviour

The validator first reads top-level `kind`. `graph-change` receives full schema and deterministic validation; `graph-operation` receives the explicit `unsupported-kind` diagnostic; every other value receives `unknown-kind`. For graph-change it validates schema shape, expiry and authorization range, local ODPG and standard-family files, meaningful G0/G1 difference, each action's need/G0/G1 connection, and completion state. When Maysano supplies an apply-time revision, a mismatch returns `graph-drift` and requires a new package.

The deterministic validator does not infer business semantics from JSON Schema. It checks the declared package against supplied graph artifacts; Maysano must independently validate the current graph revision and realised graph state immediately before applying work.

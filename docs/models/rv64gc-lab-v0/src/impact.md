# Conservative change impact

Byte authentication answers whether a supplied file matches its pin. It cannot
answer which earlier evidence a source, adapter or configuration change affects.
The existing evidence policy requires analysis of **both old and new dependency
graphs**, retaining deleted requirements and evidence, with broad validation when
influence is uncertain. This chapter documents the bounded implementation of
that graph operation in `scripts/change_impact.py`.

This is a pure operation on caller-supplied, reviewed projections. It does not
load a dossier, discover imports, read files, run a reference or update a record.
The caller must construct a complete relevant projection from canonical sources,
authenticate its inputs and supply the actual change inventory. No persisted
graph format or second canonical parser is introduced. The retained-experiment
evaluator does not yet consume this API; complete closure, source-grounded property
adequacy, collector provenance and qualification remain pending.

## Inputs and edge direction

`DependencyNode(key, kind, profile_ids, fingerprint, path=None)` and
`DependencyGraph(profile_ids, nodes, edges)` are frozen values. An edge
`("result", "input")` says **result depends on input**. A change to input therefore
travels in the reverse direction to result. For example:

```text
evidence -> obligation -> requirement -> case input
```

The public call is:

```python
analyze_impact(old, new, *, changed_paths=(), uncertain=False)
```

Each graph declares its profile universe, including profiles that currently have
no nodes. Nodes have nonempty profile memberships within that universe. Edge
endpoints must exist and have at least one profile in common. This is an influence
projection, not the starter requirement graph's integrity checker: cycles and
self-dependencies are accepted and terminate through visited sets. The caller
still applies the canonical graph's own integrity rules before projecting it.

Fingerprints are lowercase SHA256 strings identifying the relevant content or
canonical metadata. `None` explicitly means unknown and triggers broad validation;
it never means unchanged. Paths are optional canonical repository-relative strings,
checked through the existing lexical path predicate. A path can map to several
nodes, all of which are selected by a change. This API performs no physical-path
or file-hash verification. Actual fingerprint production remains the caller's job.

The closed kind vocabulary is `requirement`, `obligation`, `evidence`, `case-input`,
`semantic`, `configuration`, `implementation`, `primitive`, `generator`,
`comparator`, `source`, `reference-build`, `policy`, `schema`, `build`, `artifact`
and `test`. Only the first four allow conditional narrowing through declared
edges. Every other kind defaults to broad validation of its associated profiles
when affected. This includes a shared node reached transitively, and both its old
and new memberships and kinds. Relabeling a changed old source as a new case input
cannot erase the old broad-validation obligation.

## Selection and broadening

The algorithm seeds added/deleted nodes, changes to content or significant node
metadata, the dependent endpoint of every added/deleted edge, and every node
whose old or new path appears in `changed_paths`. Profile ordering, node ordering
and edge ordering have no meaning. It then traverses reverse edges from the union
of the old and new graphs, retaining old deleted targets in the result.

An unknown fingerprint broadens its profiles even without an observed edit.
Unmapped changed paths, explicit `uncertain=True`, or a change to the graph's
profile universe broaden all profiles from both versions, including empty and
removed profiles. Broadening selects every old/new node in those profiles and
continues reverse traversal. It repeats until stable: a shared primitive exposed
by broadening profile P can also broaden profile Q. Merely doing one expansion
would miss that second obligation.

The frozen `ChangeImpact` result contains sorted tuples:

| Field | Meaning |
| --- | --- |
| `seed_ids` | Nodes directly selected by additions, deletions, metadata/content/edge edits or mapped changed paths |
| `affected_ids` | Reverse closure plus broad-profile expansion, including removed old nodes |
| `affected_profile_ids` | Every old/new profile of affected nodes, plus explicitly broadened profiles |
| `broadened_profile_ids` | Profiles requiring complete validation rather than only the conditional graph selection |
| `stale_evidence_ids` | Affected IDs with kind `evidence` in either version; recommendations for invalidation and revalidation |
| `unmapped_paths` | Changed paths with no old or new node mapping |
| `broadening_reasons` | Sorted applicable codes: `uncertain-influence`, `unmapped-change`, `profile-scope-change`, `unknown-fingerprint`, `shared-kind-influence` |

The result does not modify an evidence status. The caller must mark affected
evidence stale and perform the policy's required checks before crediting it again.
An empty result is conditional on the supplied projection, known pins and change
inventory; it establishes neither complete influence coverage nor currentness.
There is no `qualified` field or processor acceptance verdict.

## Complete synthetic example

Run this from the repository root. It creates no files or captures. The pins are
illustrative metadata, not hashes of actual artifacts, and no process runs:

```bash
PYTHONPATH=scripts python3 - <<'PY_IMPACT'
from dataclasses import replace
from change_impact import DependencyNode as Node, DependencyGraph as Graph, analyze_impact

nodes = (
    Node("case", "case-input", ("p",), "a" * 64, "cases/example.s"),
    Node("req", "requirement", ("p",), "b" * 64),
    Node("obl", "obligation", ("p",), "c" * 64),
    Node("ev", "evidence", ("p",), "d" * 64),
    Node("unrelated", "requirement", ("p",), "e" * 64),
)
edges = (("req", "case"), ("obl", "req"), ("ev", "obl"))
old = Graph(("p",), nodes, edges)
new = replace(old, nodes=(replace(nodes[0], fingerprint="f" * 64), *nodes[1:]))
changed = analyze_impact(old, new)
print(changed.seed_ids, changed.affected_ids, changed.stale_evidence_ids)
print(changed.broadened_profile_ids)

# Removing an edge does not silently discharge its former dependents.
removed = analyze_impact(old, replace(old, edges=edges[1:]))
print(removed.seed_ids, removed.affected_ids)

# An unmapped source edit selects the whole declared profile.
unmapped = analyze_impact(old, old, changed_paths=("new/source.py",))
print(unmapped.broadened_profile_ids, unmapped.unmapped_paths)
print(unmapped.affected_ids, unmapped.broadening_reasons)

# Broad P exposes a shared primitive, which also broadens Q.
shared = Graph(("p", "q"), (
    Node("unknown", "case-input", ("p",), None),
    Node("primitive", "primitive", ("p", "q"), "a" * 64),
    Node("ev-q", "evidence", ("q",), "b" * 64),
), ())
expanded = analyze_impact(shared, shared)
print(expanded.broadened_profile_ids, expanded.stale_evidence_ids)
PY_IMPACT
python3 scripts/probe_change_impact.py
python3 -O scripts/probe_change_impact.py
```

The example prints:

```text
('case',) ('case', 'ev', 'obl', 'req') ('ev',)
()
('req',) ('ev', 'obl', 'req')
('p',) ('new/source.py',)
('case', 'ev', 'obl', 'req', 'unrelated') ('unmapped-change',)
('p', 'q') ('ev-q',)
```

## Bounds, controls and limitations

Each graph permits 1–64 unique profile IDs, 0–512 unique nodes and 0–4096 unique
edges. Profile IDs have 1–128 characters, node IDs 1–1024, and paths 1–4096.
The changed-path inventory permits at most 1024 unique paths. These are character
limits, not encoded-byte limits. Inputs require the exact public dataclass types,
plain tuples/strings and a plain Boolean; ambiguous subclasses, mutable lists,
unknown kinds, duplicate IDs/edges/paths, unsafe paths, unresolved edges and
incompatible scopes raise `ImpactError`. Count envelopes are checked before node
indexing or edge traversal. Both graphs are validated; malformed old data cannot
silently disappear into a well-formed new graph.

These are bounds on already-allocated graph metadata. The two graphs can jointly
have 128 profiles, 1024 node IDs and 8192 edges. They do not alter the retained-file
128 MiB read/16 MiB snapshot ledger or promise a process RAM/time ceiling.

The tracked probe exercises positive, removed-edge, old/deleted-evidence, shared
scope, unknown/unmapped, fixed-point, ordering, cycle, type and inclusive-boundary
cases. It independently checks all 4096 pairs of directed three-node graphs with
one explicit changed input against set-based reachability. The registered normal
and optimized suites also omit individual semantic and validation guards; only
actual discriminating omissions are counted. Synthetic checks validate this
operation, not a real graph's completeness or a CPU experiment.

The explicit reverse union is retained even though seeding every changed-edge
dependent makes a one-sided traversal redundant in the bounded diagnostic.
Run `python3 [-O] scripts/probe_change_impact.py --redundancy` to rederive all
32768 old/new/seed combinations over three nodes. This separate diagnostic checks
both one-sided closures against the union; it is not a registered discriminating
omission or a universal proof.
Neither that observation nor any passing helper result permits missing canonical
dependencies, invented fingerprints or reuse of invalidated evidence. The
existing policy's broad campaigns and full applicable release gate still apply.

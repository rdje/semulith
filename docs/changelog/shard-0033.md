# CHANGELOG shard — SEMULITH-UT-0048 … SEMULITH-UT-0048

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-UT-0048 (leaf UPSTREAM-TRACK.1) — the issue owns its state, the indices are mirrors

**Two director instructions that turn out to be one design.** *"For each vendor keep an index of
all the bugs you reported, their state"* and *"the subtree for each bug shall be self-contained"*
cannot both be satisfied by a maintained index: if the subtree carries its own state, then every
index is **derived**, and a derived thing that nobody checks drifts. That is exactly why
`FRONTIER-SYNC` and `REGISTRY-MIRROR` exist facing inwards. This is the same doctrine facing out.

Measured before building — the same facts in three places, and nothing checking them:

```
$ grep -c 'LS-00' docs/upstream/README.md                      -> 4  rows
$ grep -c 'LS-00' docs/upstream/linkedspec/README.md           -> 5  rows
$ grep -l 'State' docs/upstream/linkedspec/*/REPORT.md | wc -l -> 3  reports
$ grep -c upstream scripts/check_doctrines.project.sh          -> 0  gates
```

**Each issue now carries `issue.sexp`** — the single owner of its id, severity, state, affected
pins, fix status and dated history, living inside the subtree it describes. An S-expression,
because an issue record is a source of truth like any other
(`decision_one-format-every-source-of-truth`).

**`UPSTREAM-INDEX`** (12 arms, 10 of them RED) checks both indices and each `REPORT.md` against
the records, in both directions: stale state, stale severity, an issue with no row, a row with no
issue, an invented state or severity, a directory with no record, a report disagreeing with the
record beside it, a `verified` claim with no pin, and a directory whose name does not carry its id.

⛔ **It caught three real violations in the tracker it was written for**, which is the only
evidence worth having that a gate discriminates:

```
NOT CONTAINED LS-001: …/evidence/patched.txt:1 references '/Volumes/' — outside its own subtree
NOT CONTAINED LS-001: …/evidence/shipped.txt:1 references '/Volumes/' — outside its own subtree
NOT CONTAINED LS-001: …/issue.sexp:4      references 'scripts/'  — outside its own subtree
```

A maintainer copying that directory out would have got a machine path from my disk and a pointer
to this repository's tooling. Fixed in the content, not in the gate.

⛔ **Two failures worth keeping.** Three arms failed at first *for the wrong reason*: the fixture
computed `${1%%-*}` on `LS-001-a` and got `LS`. The fixture was wrong, not the gate — fixing it
took 8/12 to 12/12. And the gate exited 1 printing **nothing**, because `set -e` aborted the
assignment before `rc` could be read: a breach with no reason is indistinguishable from a crash.

**`docs/tasks/` crossed its aggregate ceiling** on the way through, by 3,057 bytes. Raised under
[`decision_task-tree-family-bound`](docs/decisions/decision_task-tree-family-bound.md) — which
records the two rejected alternatives first, because raising a bound because it fired is the
reflex the registry warns against. Compaction was checked (the archive is not a duplicate of its
tree) and a subdirectory was rejected for a mechanical reason: `check_frontier_sync.sh` matches
index links with a **flat** pattern, and breaking a gate to satisfy a bound is a worse trade. The
grounds are real — the family was bounded when the project tracked 17 lanes and now tracks 25,
two of them created this session on instruction. ⛔ **The per-part bound is untouched**: the
aggregate answers "how many lanes", the per-part answers "has one tree become a monolith", and
only the first question changed.


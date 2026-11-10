# A docs-only commit answers a check from its last green run when nothing the check reads has changed

- **Type:** `decision`
- **Date:** `2026-10-27`
- **Status:** `active`
- **Owner / source:** `XTASK.8` slice d, on the director's instruction of 2026-10-26 ("50min is not acceptable …
  shorten it by a lot": "well under ten minutes for a code commit and a few minutes for a docs-only commit");
  measured in slices a–c: after the pooled slot and the parallel prefetch the gate is 6.8–9.4 min, bounded by
  PROFILE-CONSISTENCY (403 s) and GUEST-GEN (323 s), whose inputs a documentation commit never touches.
answers: When may the commit gate skip a check, and what makes the skip sound?

## The fact / decision

The project doctrine slot may answer a registered check from its **last green run** on a commit when all three
hold: (1) the check **declares its input closure** — the tracked path prefixes it reads — in
`scripts/check_doctrines.project.sh` next to the registry; (2) **no staged path lies inside that closure**; (3)
the closure's **content key** — a digest of `git ls-files -s` over the closure, i.e. every tracked file's blob
id as the commit will carry it — **equals the key recorded by the check's last green run**. A check with no
declared closure always runs. A run with no staged set (outside a commit: `cargo xtask focused`, a hand run)
always runs everything. A refusal is never recorded as green. `DOCTRINE_DOCS_ONLY=0` disables the path (the
control); `DOCTRINE_TIMES` records a skipped check as `skipped`.

## Why

The two checks that bound the gate are self-tests over synthetic fixtures plus a judgement of tracked sources
under `scripts/`, `profiles/`, `schema/`, `crates/`, `definitions/`, `evidence/` — bytes a documentation commit
does not change. Re-running them proves nothing new about that commit; it costs the director seven minutes per
docs commit, and the project's rule is that nothing is re-measured when its inputs are byte-identical to a
measured run (the GUEST-GEN and FIXTURE-FINGERPRINT doctrines rest on the same idea: a key over the inputs, a
refusal when it drifts). The soundness of the skip rests entirely on the closure being honest: a check that
reads outside its declared closure can be stale. That is why the closure is declared in reviewed text beside
the registry, why the key covers the whole closure's tracked content rather than the staged paths alone, why a
missing declaration means "always run", and why the first closures are the few heavy checks whose inputs the
unit measured (`grep` census in target/xtask/xt0018), not the whole registry.

## How to apply

- Declare a closure only after reading the check for every path it opens (`grep -o '<prefix>/…'` over the
  script and the Python it calls); a check that reads a `.md` the commit could change has `docs/` in its
  closure and therefore never skips on a docs commit.
- The green record lives under `target/doctrine-gate/green/<ID>` (the key, one line) — untracked, per clone;
  a fresh clone runs everything once.
- Untracked inputs (pinned binaries under `target/refs`, acquired suites) are outside the key: a check whose
  verdict depends on them keeps running or declares no closure.
- Measure: the docs-only gate's wall before/after on an idle machine; a RED control — a staged change inside a
  closure (a `scripts/` edit) must run the check and a drifted key must run it even with no staged path inside.
- Related: [[alternate-port-and-features]] (the tooling slot this lands in), the pooled slot and its cargo lane
  (`XTASK.8` slices a–c), [[two-cargo-runs-of-one-binary-race]].

## Addendum (2026-11-10, `XTASK.16`): the declaration turned round

The rule above let a check skip when nothing staged lay inside the inputs it declared. Its own text names the weakness: "The soundness of the skip rests entirely on the closure being honest." The declarations were not complete, twice.

| What moved | When | What the declarations missed |
| --- | --- | --- |
| The six drivers, into `xtask/src/` | 2026-10-27 and 2026-10-28 | No declaration named `xtask/`, so a commit changing only a driver skipped that driver's own check |
| A credit's facts, into decision records a selection names | 2026-11-07 | `PROFILE-CONSISTENCY` declared no document, and reads four |

**Measured** (`target/xtask/xt0090`). Of 189 commits since 2026-10-27, 11 change `xtask/` and stage nothing inside any declaration, and one of them changed three of the six drivers. With every documentation file absent from the working tree, CONTRACT-FREEZE, DEF-GEN, ARTIFACT-COHORT, RECORD-SCHEMA and GUEST-GEN pass, and PROFILE-CONSISTENCY passes with four files present. All 42 doctrines pass unskipped on the tree, so nothing wrong landed.

**The rule now.** `scripts/doctrine_skip.sh` declares the *ledger*: the short list of documentation that records the work. One of the six checks is answered from its last green run when both hold:

1. every staged path is ledger, and none is a document that tracked data names;
2. every tracked byte outside the ledger is as it was at the check's last green run.

Anything else runs the check: a driver, the engine, a manifest, a hook, a unit book, a document nobody listed.

**Why this shape.** A list of what a check reads must be complete to be sound, and it goes stale without a sound when an input moves. A list of what may be ignored only has to be short. Leaving a path out of it costs minutes, never soundness.

**What holds it.**

- The gate runs the rule's controls, `scripts/probe_doctrine_skip.sh`, before it may skip anything, and refuses the commit at once when they fail.
- The documents tracked data names are derived from the index at every commit, so a new selection naming a decision record needs no edit.
- `scripts/probe_ledger_independence.sh` removes the ledger from the working tree, runs the six checks and restores it. Its control removes the named documents too, and PROFILE-CONSISTENCY must then fail.

**What it does not see.** A script that starts reading a ledger document. Only the probe measures that, and it runs by hand until `XTASK.17`.

**Cost.** A ledger-only commit still takes about two minutes of gate (104 s measured). A commit that touches only `xtask/`, the engine or a unit book now runs the six, about 20 minutes.

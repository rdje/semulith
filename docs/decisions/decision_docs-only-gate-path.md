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

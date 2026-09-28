# CHANGELOG shard — SEMULITH-SF-0047 … SEMULITH-SF-0047

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-SF-0047 (leaf SOT-FORMAT.9) — two readers, one format, and a defect worth reporting

**What landed.** LinkedSpec published its integration document (`ad290bdb4`), discharging the
blocker this tree had carried since `2026-09-14`. `vendor/linkedspec` is now a submodule **pinned
to that exact commit**, with RGX `8763a0e6bea9` and PGEN `db6f8c6836fe` — the revisions the
guide's own evidence section names. The documented PGEN bootstrap produced all four `generated/`
products; the consumer built in 32.15s.

**The point of the leaf was never the submodule — it was the agreement.** Two readers of one
format that disagree is the defect `SOT-FORMAT` exists to prevent, and it hides: each reader is
self-consistent, each passes its own tests, and the disagreement surfaces only as a model that
behaves differently depending on which tool built it. `scripts/compare_readers.py` (11 arms) now
compares both over every tracked `.sexp`:

```
agree   definitions/riscv/m.sexp             438 nodes identical
agree   definitions/riscv/rv64i.sem.sexp    1550 nodes identical
agree   definitions/riscv/rv64i.sexp        1716 nodes identical
agree   profiles/rv64i-lab-v0/encoding.sexp   18 nodes identical
DIFFER  materials/catalog.sexp  <root>: A has 43 element(s), B has 6
```

⛔ **The defect.** A double-quoted string containing **LF** is not read as one string by
`specs/Lispish.spec`. It does not merely lose its newline — it stops being a string, and its
remaining text is re-lexed as syntax, so a `)` in the continuation closes a form that was never
open. Our 43-form catalogue read as 6, with 37 nested inside the fifth, **exit 0, no diagnostic**.

Located by refutation rather than guessing: `;` inside a string and parentheses inside a string
were both hypothesised and both **refuted** — the reader handles them correctly. Spaces, parens,
TAB and CR inside a one-line string all round-trip. Only LF breaks it, which points at
`Lispish.spec:69`, `/"(.*?)(?<!\\)"/` — `.` does not match LF without DOTALL — after which the
text falls through to `others: /[^\s"{}()\[\];]+/` and splits on whitespace.

**The fix was validated before being reported**, on a *copy* of the spec so the pinned submodule
stays clean: `(?s)` on lines 69 and 71 takes the reproduction from `4 matched / 4 differed` to
`8 matched / 0 differed`, and makes all five files agree. It is LinkedSpec's change to make —
patching a pinned submodule is how a pin becomes a fork.

⚠️ **The leaf is `blocked`, not `done`.** Its acceptance says the readers agree on *every* tracked
file; they agree on four of five. Rewriting the criterion to match the result is the only real
failure available here.

**An upstream issue tracker**, `docs/upstream/`, because a defect found in a dependency is work
this project owns until it is verified fixed. Each issue is a **self-contained sub-tree** a
maintainer can copy out and run without this repository — REPORT, VALIDATE, a repro script, one
file per case, an expected-values table, our captured evidence, and where we have one, a candidate
patch. Verified self-contained by copying each sub-tree to a scratch directory and re-running it
there.

Three issues raised, each with an id, a severity and a state:

| ID | Title | Severity | State |
| --- | --- | --- | --- |
| `LS-001` | a double-quoted string containing LF is not one string | `high` | `draft` |
| `LS-002` | quoted and bare atoms are indistinguishable — no consumer can round-trip | `medium` | `draft` |
| `LS-003` | three first-consumer papercuts in the integration guide | `low` | `draft` |

⛔ The state vocabulary keeps `fixed-upstream` and `verified` apart on purpose: **a fix we have not
re-run is a claim**, and adopting a new pin on the strength of a changelog entry is how a consumer
inherits a regression. Severity is graded by whether the consumer is *told* — silence is what makes
`LS-001` high.

⭐ Two integration consequences worth their own line, both measured here. Our doctrine gates now
walk a vendored tree: `check_fixture_fingerprints.sh` **died with RecursionError** on 1.7 GB of
another project's JSON, and `RECORD-SCHEMA` judged their records by our schema. Exactly two gates
walk the filesystem — the other four use `git ls-files`, which sees a submodule as a single entry
— so both were fixed and the reason written beside the exclusion. And the bug reports' own
`cases/*.sexp` are deliberately pathological, so they are excluded from the reader-agreement sweep
with an arm proving it: a corpus and a bug-report fixture must not share a scan.

⛔ **Three departures from the published guide, all mine, all named in the tree.** I jumped to the
line the director pointed at and skipped *Initial PGEN preparation* 100 lines earlier — the guide
says plainly that checkout does not generate PGEN's parser inputs, and I had not read it. I used
`--recursive` where two targeted inits were prescribed, costing 1.7 GB and 30 nested submodules. I
used bare `cargo` instead of `tools/run_cargo_local.sh`. A guide is only followed if you read the
part before the part you were sent to.


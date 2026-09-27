# CHANGELOG shard — SEMULITH-MM-0034 … SEMULITH-MM-0034

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-MM-0034 — the dual mandate: production-grade **and** a teaching text

**What changed.** A director instruction that reshapes every model this project will produce:
each must be signoff, production-grade work **and** serve as educational material from which a
student can learn to build production-grade CPU/DSP models capable of running real compiled code
(C, Rust, …). Recorded as
[`decision_dual-mandate-production-and-teaching`](docs/decisions/decision_dual-mandate-production-and-teaching.md),
carried into `MODEL-BOOKS` and `MODEL-METHOD`, and aligned into `ROADMAP.md` §1.

⭐ **What the teaching mandate actually changes** — it is not "add explanation", which would change
nothing. Four concrete things: reasoning becomes recoverable including the rejected alternatives;
**mistakes stay in the record**; the *order* of the work is justified rather than listed; and
"runs real code" becomes a target with stated limits.

⛔ **The mistakes are the most instructive pages.** This project has already found, in its own
work, a matched profile that matched only an instruction set, a comparator that called a truncated
trace agreement, a self-test that ran four of fourteen arms, and a gate report that counted a
*mention* as an implementation. Removing those to look competent would remove the teaching.

**What "runs real code" costs, measured rather than assumed.** The first profile is `RV64I` with
no extensions: no `M` (multiply and divide become runtime calls), no `A` (no atomics), no `F`/`D`
(soft-float ABI), no `C`. Running C or Rust on it needs materials the ISA chapters do not own and
this project has **not pinned** — the psABI, the ELF specification, a startup/runtime contract,
the compiler-runtime intrinsics a no-`M` soft-float target calls, and a program-exit convention.
Those are now acquisition items in `MODEL-METHOD.4` rather than assumptions.

⚠️ It also makes an existing honesty load-bearing: `state.json` records ABI register roles as
`software-convention` because the ISA chapter does not own them. Once real code runs, that
convention stops being background reading and becomes a pinned material with a digest.

⛔ Neither mandate may be traded for the other. Simplifying a contract to make a chapter easier is
a production defect; omitting reasoning to keep a record terse is a teaching defect. Where they
genuinely conflict the production artifact wins and the book explains the complexity — a student
learning from a simplified fiction learns a fiction.



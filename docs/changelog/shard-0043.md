# CHANGELOG shard — SEMULITH-RM-0059 … SEMULITH-RM-0057

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-RM-0059 (leaf ROADMAP-V3.3) — ROADMAP v0.3: the star gets a start condition

`ROADMAP.md` supersedes v0.2 (the house pattern: the delivery manifest and git carry the old
bytes; v0.2 was `live`, so no disposition change was needed). v0.3 lands the adopted package:
P1's start condition (`SOT-FORMAT.2` constructs + `MODEL-METHOD.10` extraction contract — the
remaining format-migration leaves are consumed by later milestones, not by P1's start); the
execution-authority row in the §1 decision table (semantics are data and the data executes);
the lane-consumption rule in §1; P1's G1 sharpened to the star-facing proof — a compiled
freestanding guest program retires under first-divergence comparison, C named as the first
guest path, and the first mdBook increment ships in the same milestone; the v0.4 trigger moves
to P1 first-slice completion. Under review, `LIVE_STATUS.md`'s `MODEL-METHOD` count was
re-derived: `3/10` (a spelling no gate can see) → `6 of 13` (the gated spelling). File: 24,065
bytes against the 24,576 ceiling. Tree `ROADMAP-V3` complete, 3/3.

## SEMILITH-RM-0058 (leaf ROADMAP-V3.2) — every lane names the milestone that consumes it

The sequencing vacuum, measured rather than asserted: `27` commits since any milestone tree
was last touched, and that touch was P0 closure. The roadmap's warning ("evidence tooling does
not become an unrelated research product") becomes an operational rule: every cross-cutting
tree's Metadata declares `Consumed by:` — milestone plus latest consumption point; lanes
without a named consumer are descoped at the next roadmap revision; new lanes must name a
consumer at proposal. First application covers all seven current lanes. The mechanical census
gate is **proposed to the director, not registered** — new governance is announced before it is
tasked. Record: `docs/decisions/decision_lane-consumption.md`; tree `ROADMAP-V3` at 2/3.

## SEMULITH-RM-0057 (leaf ROADMAP-V3.1) — the semantics data is the execution authority

Director-delegated decision (`2026-09-27`: "the decision is yours to make but it got to be sota,
signoff and production-grade") resolving the open contradiction between `docs/ARCHITECTURE.md`
§1.1 (semantics are data) and §2 (canonical Rust semantic functions): P1 executes the 32-form
semantics data directly — a definitional interpreter, keeping exactly one owned implementation
per rule (OWN-01); compiled or IR handlers enter only as generated, fingerprinted artifacts
behind an observational-equivalence regression. The pattern is the one this project's own pinned
Sail reference uses: the interpreter is the reference behaviour; compilation of the same
semantics is a derived artifact that must agree with it. Revisit conditions named: a measured
P2/P4 performance need, or the explicit semantic-IR migration decision. Record:
`docs/decisions/decision_interpreter-before-compiler.md`; tree `ROADMAP-V3` registered (1/3).


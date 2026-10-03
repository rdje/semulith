# A tracked generated module needs a tracked canonical input — the rv64gc state module's landing is flip-bound

- **Type:** `decision`
- **Date:** `2026-10-03`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.2` slice (c) (the (c1)/(c2) split); constrains slices (d)–(h).

## Context

STATE-GEN (`scripts/check_state_gen.sh`) proves `crates/semulith-core/src/state.rs` is the
byte-exact function of the TRACKED `profiles/rv64i-lab-v0/state.sexp` — regenerate and
diff, in a fresh clone, with no network. P4-SYSTEM.2 slice (c) authored the rv64gc state
document, but the unit declares `(vehicle (route profile-resolution))`, under which a
`state.sexp` inside the unit is a refused contradiction until the atomic route flip
(slice h). The document is therefore staged untracked at `target/p4-system-2/`.

The question: may the rv64gc generated state module land in `crates/` before the flip?

## Decision

**No.** A tracked generated artifact whose canonical input is untracked is a copy, not a
derivation: a fresh clone could not re-derive it, and the generator-gate could not judge
it there. The measured alternatives: landing the module with a skip-if-absent gate leg
(a standing hole in the byte-exact property — refused); a hand-written interim state
module (a second owner — OWN-01 forbids); tracking the descriptor at a non-unit path (a
category lie — the document is the unit's, and every consumer discovers it by unit).

So slice (c2)'s tracked landing rides the flip (slice h): the descriptor moves into the
unit, the module lands in `crates/` in the same green commit, the STATE-GEN census and
the FACT-OWNERSHIP rows extend to the pair there. The interim evidence is the scratch
proof, recorded in the leaf: the generator emits the module (40,198 bytes) and a scratch
`rustc --test` harness exercises it behaviorally (reset values per the document — mode M,
the mstatus composite `0xA0000000`, misa's declared value — the address lookup over the
33 CSRs, the view discipline, the field tables, x0 and the mode transitions; 4/4).

## Consequences

- Slice (d)'s engine execution works against scratch-level artifacts the same way; its
  tracked landing is the flip's, in one green commit.
- The unit's `outcome.rs`/`state.rs` "no privilege modelled" comments stay TRUE until the
  engine actually gains the semantics (slice d) — they are brought in line in that commit,
  never earlier, never later.
- The rule generalizes: any future staged artifact follows the same staging — authored and
  validated untracked, generated surfaces proven at scratch, tracked landing at the flip.

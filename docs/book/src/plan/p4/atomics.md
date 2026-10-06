# P4.4 — Atomics and reservations

**Status:** Landed and closed (slices a–f, 2026-10-05)

The design brief (the A fragment is Zaamo + Zalrsc's 22 forms; a minimal exact
reservation; the deterministic SC policy as data; an atomic bind) executes in six
checkpoints. Slice (a): the `rv_a`/`rv64_a` tables are re-pinned through the tracked
`extensions/` fetch route — the 22 forms (the nine AMOs and the lr/sc pair, each
`.W` and `.D`) that the pinned RVWMO chapter's Tables 6/7 enumerate exactly — and
`definitions/riscv/a.sexp` is generated from them, owning the `aq`/`rl` ordering
fields. The assembler learns the A machinery: the `.aq`/`.rl`/`.aqrl` mnemonic
suffix as the aq/rl FIELD VALUES (never table names; all four combinations assemble
— every aq/rl effect is defined "as viewed by other RISC-V harts", so at one hart
they decode and order nothing observable), and the `(rs1)` parenthesized-address
spelling for the lr/sc/amo shapes. 88 words (22 forms × 4 suffix combinations)
round-trip through spike-dasm exactly; every shape it cannot assemble is refused by
name. The pin exposed its own census's blind spot — the scope-vs-tables leg had
never collected a `rv64_*` table — fixed at root with the rv64i dossier's declared
"pinned for the fragment, not the scope" exclusion extended to the A tables until
the bind. The slot stays declared and the scope census stays 65: both grow only at
slice (e)'s atomic bind, one green commit.

Slice (b): the semantics language grows 40→43 forms. A RESERVATION contract block
states the one-hart rules once — the minimal exact reservation, physical-keyed; any
LR replaces, any SC clears, traps do not invalidate — and three operators carry the
policies the brief decided: `load-reserved`, `store-conditional` (yields the rd
code, 0/1, never spurious under the declared deterministic policy), and `amo` — one
operator for the closed nine, translating ONCE under the store/AMO rules (never a
load page fault; the decomposition into load-op-store would deliver the wrong fault
cause), the boundary shape a load followed by a store. `a.sem.sexp` covers all 22
forms, every rule locator-cited and resolving offline against the pinned A chapter.
Two measured design points: the AMO's operation is the funct5 literal (a bare
symbol would be refused as a phantom operand), and the closed set is RE-DERIVED from
the composed encodings; and the `Sem` variants emit exactly when the composition
composes `riscv/a` — the evaluator's exhaustive match is the `.2` slice-d wall, so
the tracked modules regenerate hash-only while the scratch composition lowers and
compiles standalone.

Slice (c): the reservation is hart state now — `reservation.rs` owns (physical
address, width, valid), the minimal conformant set, physical-keyed, with exactly
the spec's one-hart invalidation set: any LR replaces; any completed SC clears; a
trap clears nothing (measured on Sail 0.14: its cancellation fires on the completed
SC path only). The deterministic SC policy rides as data in `state.sexp` beside the
census candidate, and gen_state's census gate is generalised to refuse any carried
hart state the census does not declare. The evaluator arms exist and are proven in
scratch — 16/16 over the LR/SC pair and every must-fail cell, the AMO nine × `.W`/`.D`
with old-value rd sign-extended, the translated AMO faulting 15 never 13 on an
unreadable page, misaligned atomics taking cause 7 before translation, the
constrained loop succeeding on its first SC — and land tracked at the bind.

Slice (d): the corpus exists. Twelve staged guests cover the brief's families —
the nine AMOs × `.W`/`.D` with rd sign-extended at the word edge and the min/max
signedness disagreements, every aq/rl combination executed identically, register
overlaps, the LR/SC pairs and every one-hart must-fail (different address,
intervening SC, LR-replaces, width mismatch, SC-without-LR, a failed SC writing
nothing), a constrained loop closing on its first SC, misaligned atomics taking
cause 7 before translation, the translated AMO faulting 15 never 13, and an alias
cell proving the reservation physical-keyed. Every expectation is derived by a
spec-side model written from the pinned chapters and the declared policy — never
engine output — and every word assembled by the tracked assembler's A machinery;
the corpus runs 12 PASS / 0 FAIL through the slice-(c) scratch engine,
deterministic on re-run. The matrix rehearsal resolves all 28 cells with the new
guests riding the seven existing axes, and the coverage rehearsal reads 22/22 —
the bind's 87-form denominator is fully exercised in staging.

Slice (e) — **the bind**: one green commit makes A real. The slot becomes an
extension, the census dual edit grows 65 → 87 (the RVWMO Tables 6/7 enumeration),
`definition_rv64gc.rs` regenerates with the 22 forms and the three `Sem` variants,
the evaluator arms port byte-identical from the scratch proof, and the twelve
guests land tracked — the full 88-guest corpus executes green through the tracked
engine, with the slice-(c) proof re-run against it. The reservation and its
deterministic SC policy, and the misaligned-cause-7 choice, are profile decisions
with verbatim requirement and obligation mirrors. The fetch leg's scope-vs-tables
check flips on its own to 87 == 87, and every one of the 76 pre-bind guests runs
byte-identical against the parent engine (3,468 trace lines, `cmp` clean) — the
22 new forms are additive; the corpus never noticed. The profile now executes
atomics.

Slice (f) — and **the leaf closes**: the matched experiment. Every atomics guest
also runs under Sail 0.14 with the tracked override — validated unchanged (A
supported, the region's AMOCASQ/RsrvEventual/AccessFault all present, as the
brief measured) — and the comparison rides the corpus's own change-observation
rule: **eleven guests AGREE step-for-step** (the LR/SC pairs and every must-fail,
the AMOs at both widths with the old-value sign extension, the suffix cells, the
translated AMO faulting 15 never 13, misaligned cause-by-kind, the alias cell
proving the reservation physical-keyed on both sides, the constrained loop
closing on its first SC — Sail's SC is deterministic under RsrvEventual, exactly
the declared policy). The twelfth is a NAMED DIVERGENCE: the laboratory's
declared width-equal SC policy fails a `.D` SC after a `.W` LR where Sail's
platform reservation matches on the physical address alone — both legal under
§12.1.2's latitude, recorded with the mm-wfi honesty. The experiment also caught
a real defect of the bind day: the uniform-cause-7 misaligned policy is illegal
for LR — the exception table maps load-reserved to load exceptions, and Sail
delivered 5. The policy is now kind-matched (LR → 5, SC/AMO → 7) in the engine,
the contract, and the decision record. The acceptance reads as measured:
single-core reservation behaviour is validated — atomic widths, reservation
semantics, failed conditional stores, overlap and external-write cases — and the
multicore memory model stays `MC-MULTICORE`'s, never smuggled.

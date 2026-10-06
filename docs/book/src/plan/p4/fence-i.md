# P4.6 — Instruction visibility and fence semantics

**Status:** Landed and closed (a–c, 2026-10-05)

The design brief (fence.i the declared nop on an always-coherent engine; the
bind miniaturized to one form) executes in three checkpoints. Slice (a):
the slot's payload is pinned and authored. `rv_zifencei` lands through the tracked
`extensions/` fetch
route — 73 bytes, exactly one row — with the fetch leg's named exclusion keeping
the census at 87 until the bind. The generated fragment owns no fields (imm12/rs1/rd
are the base's, decoded-and-ignored per the shall-ignore rule), and `zifencei.sem.sexp`
states the declared nop with every normative sentence located (the
coherent/uncached-RAM latitude meets a re-read-per-fetch machine). One brief
claim measured false: the operand list refused the standard-software spelling —
the assembler gains a named zero-operand acceptance. No Sem variant, no
generator change — the one-form nop lowers over the existing machinery.

Slice (b): THE BIND. The slot becomes the extension and fence.i is legal — the
census grows 87 → 88, the generated definition gains the row over the existing
nop, and the requirement pair lands with no new decision record. The two fencei guests re-derive exactly as
pre-committed: the delivery is gone, and the marker that proved
it now commits — x2 ← 7, as on both references. The acceptance pair
stands — with the synchronization (fencei-selfmod) and without
(fault-selfmod, immediate visibility by declared choice) — with the
reserved-fields word ignored end-to-end. The corpus reads 101/101,
98 pre-bind guests byte-identical.

Slice (c): the matched experiment and the leaf's acceptance. The chapter's
contract is three sentences (stores to instruction memory are not guaranteed
visible until a FENCE.I; the fence orders the accesses before it ahead of the
fetches after it) — and
both engines land on the same reading: the laboratory's re-read-per-fetch
makes the fence a nop by construction, and Sail's FENCEI is "a nop for the
memory model" with its fields decoded-not-fixed. Against the matched
configuration (validate-config clean), all six fence.i guests AGREE
step-for-step, 29 steps, the patched fetch reading 7. The criterion closes on
the pair: WITH the synchronization (fencei-selfmod's fence.i executed and legal
between the store and the patched fetch, on both engines) and WITHOUT
(fault-selfmod, immediate visibility as the declared subset). The goal's other
half — when stale state MAY persist — is a declared latitude, not a fixture:
modelling a forever-caching hart would contradict the always-coherent census
(rejected at the brief). The reserved-fields word executes on both sides.

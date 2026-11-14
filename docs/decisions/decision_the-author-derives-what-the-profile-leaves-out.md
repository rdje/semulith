# The expectations author derives the trap for what the profile leaves out, and still refuses what it cannot derive

- **Type:** `decision`
- **Date:** `2026-11-14`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.20` slice b2's brief, `SEMULITH-P4-0406`; the window's item "the author's vocabulary" ([`decision_csr-write-three-producers.md`](decision_csr-write-three-producers.md), from [`decision_the-seventeen-called.md`](decision_the-seventeen-called.md) finding 5). The engineer's call under [`decision_findings-are-the-engineers-to-call.md`](decision_findings-are-the-engineers-to-call.md).
answers: Which accesses outside the profile does the author derive as an illegal-instruction trap, which does it keep refusing, and why is the line where it is?

## What was measured

`target/p4-system-20/b2-brief/measure_excluded.py`, at `202a7943`: one guest per access, a handler recording `mcause` and `mtval`, run on the author (`derive_snapshot`), the lab engine and the pinned reference under the profile override. Twelve CSR addresses outside the state table (`hstatus`, `hedeleg`, `hgatp`, `vsstatus`, `pmpcfg0`, `pmpaddr0`, `mcountinhibit`, `tselect`, `mseccfg`, `senvcfg`, `mconfigptr`, and the unnamed `0x7c0`) read with `csrrs`, and eight SYSTEM words the encoding does not decode (`hfence.vvma`, `hfence.gvma`, `hlv.b`, `sinval.vma`, `sfence.w.inval`, `dret`, `wrs.nto`, `mnret`).

| Producer | All 20 accesses |
| --- | --- |
| lab engine | illegal-instruction, `mcause` 2, `mtval` the instruction word |
| pinned reference | illegal-instruction, `mcause` 2; `mtval` the word, except 0 for `mcountinhibit`, `tselect`, `senvcfg` and `mconfigptr` |
| author | refuses every one (`SnapshotUnsupported`) |

So the engine and the reference agree that each is a trap, and the author can derive none, so no case can witness one (the limit `decision_the-seventeen-called.md` names for `hstatus` and `pmpcfg0`). The four `mtval` differences are the reference's: the lab's declared policy writes the word, as the engine does.

## The line, and why it is there

The author refuses "unknown valid instruction vocabulary … rather than fabricating a trap", and GUEST-GEN holds it to that with a control that reads `mvendorid` (`0xf11`). That rule is right, and it stays: a refusal is how the author fails safe. What b2 changes is what counts as unknown.

1. **A CSR the state table does not declare is reserved, and the laboratory traps a reserved instruction.** The profile's CSR set is closed (`D-CSR-SET`: the committed minimum of 33), every member is in `state.sexp`, and the pinned chapter says "Instructions that access a non-existent CSR are reserved" (RVP-CSR §1.1.1). The architecture leaves a reserved instruction's behaviour unspecified; the laboratory's `D-RESERVED-DECODE` convention makes it illegal-instruction with `xtval` the word, which the engine applies and the rv64gc corpus already cites (`a-lrsc-illegal`: "NO row matches — delivered illegal-instruction, cause 2, xtval the word"). The author reads the set from the table, so this derives from data, not from a list of exceptions. `mvendorid` is such a CSR, and its control is re-expressed (item 3).
2. **A SYSTEM-opcode word the encoding does not decode is reserved, by the same convention.** The profile's instruction scope is closed by its encoding (200 forms); a word no row matches is the reserved case, as the author already treats it in the A space. The author asks the encoding it derives with, so a frozen copy answers for itself.
3. **What stays refused is what the author cannot derive inside the profile:** an instruction the profile has whose semantics the author does not model, such as a write to `mcycle` or `minstret` ("writable counter rebasing is outside this bounded author's scope"). GUEST-GEN's control moves from `mvendorid` to such a write, so it still proves that unknown semantics refuse.
4. **The trap is the lab's:** `mcause` 2 and `xtval` the instruction word, before any register or CSR effect, with the privilege check first as today. A case that witnesses one of the four CSRs above must select it, since the reference writes 0.

## How it is held

Slice b2 extends `scripts/probe_csr_author_engine.py`, or adds its sibling, with the twenty accesses above and a sweep of the SYSTEM words the encoding does not decode, run on the author and the engine; the GREEN arm on the real tree and a RED arm that restores the refusal. Nothing is credited in the window, so nothing lapses.

## What this does not settle

- Whether a case witnesses one of these traps. `REQ-D-NO-H` and `REQ-D-NO-PMP` can; that is slice f's, with the re-capture.
- Reserved encodings of instructions the profile does have (a reserved field inside a known form): those keep their existing handling.

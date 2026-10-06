# P4.5 — Interrupts, counters and wait

**Status:** Landed and closed (slices a–d, 2026-10-05)

The design brief (a declared virtual-time domain, pending evaluation at the step
head, a real halt with WFI's spec wake)
executes in four checkpoints. Slice (a): time moves. The laboratory's virtual-time
domain advances one tick per step boundary, retired or halted — a pure function of
the step index, so determinism holds by construction. The
storage is ONE domain: `mcycle` holds it, `time` views it, and `minstret`
counts genuinely — a trapped, reserved or halted step never increments. The
rate and the count rule are data in the state document. The moving counters
exposed a latent defect — a field-less CSR view masked to zero, so the counter
views would have read 0 forever — fixed at root as a full-width shadow.
mm-counters, the only counter-reading guest of all 88, re-derives five cells
by design (time at executed step k is k); the other 87 run byte-identical.

Slice (b): interrupts fire. Every step head evaluates pending — the (a)(b)(c)
taken-rule, the global enables, the delegation mask, the fixed priorities with
the M-source bits read-only 0 — and delivery honors both xtvec.MODEs (BASE for
the trap, BASE + 4×cause vectored) with the Interrupt-bit cause, the un-fetched
xepc and the xPIE/xIE/xPP stack. Seven i-* guests carry the evidence: the
taken-rule per mode, the enable immediacy, the timer across the ticking domain,
the delegation mask, the priority drain, both vector modes, and a nested
delivery's stack restoration — 95/95, all 88 pre-slice guests byte-identical
(the census proved none could become eligible).

Slice (c): the acceptance's machinery. A legal WFI now halts the hart — one
ACTIVE/WAITING bit, cold-ACTIVE at reset, declared in the state document's
SEM-08 census like the TLB and the reservation before it. A halted step retires
nothing and issues no fetch, but the domain ticks. The wake is the spec's own
condition — a locally-enabled pending interrupt at any privilege, regardless of
the global enables and of mideleg — and the taken-rule decides what follows:
the trap with xepc = the WFI's pc + 4, or execution simply continues. The
expectations vocabulary gains the `<halted>` pseudo-step. Four wake guests
carry the family — the timer wake (rdinstret 11 at the handler, the acceptance
observed), the wake-without-trap idle loop, the delegated source waking an
M-mode hart, the software-posted sources — and mm-wfi
re-derives around arranged wakes, trap cells unchanged: 99/99, 94 pre-slice
guests byte-identical.

Slice (d): the matched attempt and the leaf's acceptance. Against the matched
Sail configuration (the override materialized fresh, validate-config clean),
six guests AGREE (i-accept, i-deleg, i-enable, i-nest, i-vector, w-sw; 218
steps, Sail numbering the delivery step and printing no row — the laboratory's
own convention). The six named divergences are all platform-shaped, never
semantic: Sail's timer gates on `plat_have_clint` (i-prio, i-timer); its WFI is
a nop under the matched platform (the four `<halted>`-step guests); and
mm-wfi's TW cell is the named gap, freshly measured — with the wait modeled the
delivered trap is identical, 30/30. The `.4` re-run under the fresh override
reproduces 11 AGREE + 1 named of 12 — verdict-neutral. The criterion closes on
w-timer's own run: rdinstret = 11 at the handler, nothing retired across the
halt, and the timer trap with mepc = the WFI's pc + 4. The wake occurred
without CPU retirement: the laboratory makes time pass while nothing executes.

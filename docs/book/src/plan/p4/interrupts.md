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
semantic in that historical classification: under the public matched configuration,
Sail does not assert comparator STIP (i-prio, i-timer); its WFI is
a nop under the matched platform (the four `<halted>`-step guests); and
mm-wfi's TW cell is the named gap, freshly measured — with the wait modeled the
delivered trap is identical, 30/30. The `.4` re-run under the fresh override
reproduces 11 AGREE + 1 named of 12 — verdict-neutral. The criterion closes on
w-timer's own run: rdinstret = 11 at the handler, nothing retired across the
halt, and the timer trap with mepc = the WFI's pc + 4. The wake occurred
without CPU retirement: the laboratory makes time pass while nothing executes.

The independent expectation author now includes the selected counter-enable and STCE
CSR rules (P4.12 e1b2). Its finite controls check thirty counter/timer mode combinations,
including S stimecmp read/write faults before effects and M-mode bypass. Accessibility
never changes counter values or progression. Two earlier mode-matrix guests now derive
through these gates; the author still explicitly refuses writable counter rebasing.

Supervisor interrupt CSR visibility is also conditional on delegation. P4.13
repairs the shared `sip`/`sie` view logic and the independent author: undelegated
bits read zero and ignore writes, even if `mip` is pending. Revoking delegation
preserves pending/enabled owner state. That earlier repair still assumed computed `mip.STIP=1` at reset. The later
STCE repair below corrects this: cold STCE=0 exposes software pending zero,
and `sip` is zero with `mideleg=0`.
Interrupt selection and WFI wake still use the machine owners and their explicit
delegation rules; the CSR-view repair does not change those rules.


P4.13's later Sstc review found a production defect (repaired by c13a2): the STIP overlay
then ignored STCE=0, which must restore the software-writable M-mode
fallback. It also found that mm-stimecmp's terminal zero read cannot distinguish
success from a final trap. The pending fallback is now repaired; the terminal witness repair remains
owned before SSTC contract credit;
[the runtime chapter](contract-runtime.md#sstc-prerequisites-two-discovered-defects)
gives the public reproduction and the ordered repair plan. The earlier timer
receipts above describe their recorded inputs and do not establish this missing case.

The current timer corpus explicitly enables STCE before comparator use. Its
fresh w-timer run reads instret=13 and time=17 after the same two idle boundaries,
with mepc=0x80000034. Earlier numeric receipts above refer to their historical
inputs. [The runtime chapter](contract-runtime.md#explicit-comparator-setup-before-fallback-repair)
shows the setup, all nine budgets, the worked wake sequence and reference limits.
The fallback defect is repaired: cold pending is zero, M software owns STIP
with STCE clear, and enabling the comparator retains raw software pending.
The terminal S-mode witness repair remains pending. The runtime chapter gives
the current selection table, transitions and v2 supersession.

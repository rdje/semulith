# The information a unit demands — CPU, DSP, board

> The [information catalog](../contracts/information-catalog.md) lists twenty-four
> categories of things a processor model *could* need, plus fifteen DSP-specific questions.
> This chapter answers a sharper question, per unit kind: **which of that information is
> load-bearing, in what form must you have it, and what exactly does its absence prevent?**
> The catalogue owns the category definitions (cited below as C01–C24); nothing here
> restates them. What this chapter adds is the *demand* and the *price*, measured on the
> two units this project has actually built — `rv64i-lab-v0` (CPU) and `dsp56300-lab-v0`
> (DSP) — and, for the board, derived honestly from the composition work that is not yet
> measured.
>
> **This is a live chapter.** It is re-derived, not just re-read: each unit the project
> models measures its own demand list, and the chapter changes with what is measured — a
> "prospective" section becomes measured (the board's, when P4–P7 land), a class that
> was one row splits (as "the widths" had to split into widths *and their readout
> semantics* when the DSP bit), a row that never bites merges away. The rule for
> changing it is the rule it already lives by: every claim cites a measured instance,
> and anything not yet measured says so.

"Prevents" has two distinct meanings, and keeping them apart is the spine of the whole
chapter:

- **Prevents the model.** There is nothing to derive from. You cannot build it, only
  invent it — and an invented fact is the one thing this project's rules forbid outright.
- **Prevents the claim.** You *can* build something — but it is not evidence. A missing
  reference route does not stop honest experimental work; it stops the differential
  claim (SRC-02). Confusing these is how projects ship an experimental model wearing a
  validated one's clothes.

There is also a third, quieter meaning that only shows up in practice: **prevents the
bound** — you can build it and run it, but you cannot *say what you don't model*, because
the census was never taken. That is the failure the claim gates exist to refuse.

---

## CPU — measured on `rv64i-lab-v0`

**1. The specification's identity** (C23). Not "the RISC-V spec, v20260120" — a version
string identifies nothing. The *publication* plus the *revision*, pinned as bytes with a
digest. The same specification exists in two publications that number the same chapters
differently; an external reviewer once "disproved" this project's citations by reading
the other one. *Absence prevents*: every downstream citation — nothing you say about the
machine can be resolved back to text. This is step 0 of [the method](../contracts/method.md)
for a reason.

**2. The architectural state census, including hidden state** (C02). Every register, its
width, its reset value — and the state that is *not* a named register: pending effects,
loop machinery, anything that influences future behaviour. *Absence prevents*: the
definition of "state" itself. You cannot say what you compare, what you snapshot, or what
you replay. The scalar profile's replay is honest *because* its census answers "pending or
partially committed effects: present false" out loud.

**3. The encodings, machine-readable** (C03). Bit layouts in a form a generator can
consume. The pinned RISC-V specification renders its encoding diagrams as *images* — so
the layouts came from a second source (`riscv-opcodes`), whose ancestry had to be recorded:
it is upstream of Spike's decoder but not of Sail's, which means Sail agreeing with our
bytes is independent confirmation and Spike agreeing is not. *Absence prevents*: decode.
And absence of the *ancestry record* prevents knowing whether your differential test is
two opinions or one.

**4. Per-instruction semantics, cited** (C04). Every effect — result, flags, PC rules,
suppressed writes — with a locator into the pinned text. *Absence prevents*: the model.
Semantics without citations do not prevent building; they prevent *reviewing* — nothing
can be falsified, because nothing says what the rule was derived from. Cited is not
verified; it is the precondition for verification to mean anything.

**5. The fault model, including what is UNSPECIFIED** (C11, C14, C22). Causes, priorities,
tval rules — and an explicit list of what the architecture leaves open. *Absence
prevents*: honesty about policy. `fence.i` executes as a NOP on both references but is a
reserved encoding in this profile; the divergence is respectable *only* because it is
declared (`expect_divergence`), not because it is small.

**6. Reset and entry state** (C17, C20). Where the first instruction comes from and what
every register holds there. *Absence prevents*: step 0. One reference begins at the ELF
entry, another runs a built-in reset vector first — without this fact, your comparator
reports a divergence that is pure harness.

**7. An independent reference, its independence inventory, and a matched configuration**
(C23). Three separate things, each with its own price:

- *No reference* → no differential claim, ever. Experimental work may proceed and must say
  it is experimental.
- *No independence inventory* → agreement that may be one opinion. Sail and Spike share
  184 of 199 floating-point source files; an FP differential between them would test one
  implementation twice.
- *No matched configuration* → green verdicts on a fiction. The ISA string matched for
  four leaves while the reference kept its default platform underneath — a probe read a
  CLINT timer nobody had configured. The reference must be *configured to the profile*,
  and the configuration read back, not assumed.

**8. The environment contract — lab vs board** (C19, C20). Which memory and devices the
laboratory supplies, and which are out of scope. *Absence prevents*: a clean comparison —
every reference drags in some board (Spike bundles an interrupt controller and a UART you
cannot remove), and without the contract you are comparing your CPU against somebody
else's computer.

**9. Timing — only if claimed** (C17, C24). Cycle behaviour needs its own evidence axis.
*Absence prevents*: nothing, if you say so. Everything, if you don't.

---

## DSP — measured on `dsp56300-lab-v0`

A DSP needs **everything the CPU needs** — the classes above do not shrink — *plus* the
information that breaks the scalar assumptions. This is the measured list; each item
earned its place by biting at least once.

**10. The widths, and each width's readout semantics** (C02, C06). Not just "24-bit
registers, 56-bit accumulators" but *what the bus sees on every read*: the A2 extension
byte is sign-extended through bit 7; an A1 read through the limiter returns a saturation
constant and sets a sticky flag when the value does not fit; an 8-bit short immediate to
X0–Y1 lands in bits 23–16 as a *fraction*. *Absence prevents*: correct data movement —
the demo guest's `move #$5,x1` producing `x1=050000` looked like a toolchain bug and was
the manual's rule. On an unfamiliar ISA the first reflex is "the toolchain is wrong"; the
correct one is "read the move semantics".

**11. The address spaces, with a unit per space** (C10). P/X/Y, each word-addressed, a
word meaning 24 bits — "address + 1" is not "the next octet". *Absence prevents*: naming
an address at all. This project's scalar-shaped schema refuses `memory_spaces` by name;
that refusal is the finding (F3), and it is why the DSP model stands as a sibling crate
today.

**12. The arithmetic model** (C06). The fractional ×2 in every multiply, where rounding
happens relative to accumulation, where saturation happens relative to narrowing, which
flags are sticky and survive what. *Absence prevents*: every MAC being right — off by a
factor of two *and* by the flag state. Worse: wrong in a way guests will not discriminate
unless expectations are derived by hand *before* the model runs (EVD-05), because a model
and its unchecked expectations share the same misunderstanding.

**13. The operating-mode map** (C15, C22). Which mode bits change execution and which are
stored but inert — and *who says so*. The DSP56300's SA/SC/DM bits are silicon-real, but
the pinned reference deliberately does not execute them. *Absence prevents*: the claim's
boundary — either you model behaviour no oracle can check, or you quietly scope it out.
The reference's documented gaps bound the claim axes, and the subset's exclusions map
onto them one-to-one.

**14. The loop and stack machinery** (C02, C05). Zero-overhead loops are *state*: LA, LC,
the loop flag, the 16-level hardware stack, the push/pop discipline on entry and exit.
*Absence prevents*: loops that are observably right — a wrong stack slot is invisible to
register dumps and memory dumps alike, which is why the comparison dumps the stack too.
This is the state census reopening per profile (F6), not a defect in the census method.

**15. The per-instruction condition-code rules, and scepticism about the document itself**
(C04, C22). "Standard definition" vs "special definition" per instruction — and the
knowledge that the *extraction* may invert the manual's own prose: the FM's U-bit row says
"set if the two MSBs are identical" and prints an equation that computes the opposite.
*Absence prevents*: SR ever being right; and only *full*-state comparison catches it,
because a guest that never discriminates U passes either way. When the document disagrees
with itself, the measured machine is the arbiter — and the arbitration is written down.

**16. What a DSP does not need when the oracle lacks it: timing.** The reference models
no pipeline interlocks and publishes base-table cycle counts only. *Absence prevents*:
the cycle claim — nothing else. The comparator skips `cyc` by a recorded rule, the model
emits none, and no timing rides this path. A bounded "we cannot know" stated out loud is
worth more than a number.

---

## Board — prospective (P4–P7; derived from the composition work, not yet measured)

Everything above is measured. This section is not, and says so: it is what the project's
composition machinery already *demands*, which is the best available map of what a board
will demand.

**17. The composition itself** (C01, C19). Which units, merged into one definition —
possible only because every source of truth is one format; two formats would be two merge
semantics and the union would be hoped, not decided. *Absence prevents*: the board as an
object — there is no "the board", only units in a pile.

**18. The memory map and the device models** (C19). Addresses, device register semantics,
reset state. *Absence prevents*: discharging the CPU's environment assumptions — the lab
profile declares 8 assumptions and a composition must produce a named guarantee for each
or be refused. An unmapped address is a guessed device; a guessed device is an invented
fact.

**19. Interrupt routing and delivery** (C14). Sources, priorities, the delivery windows.
*Absence prevents*: diagnosing any boot hang — "the CPU is wrong" and "the board never
delivered the interrupt" are indistinguishable without this, and they have opposite
owners.

**20. The boot contract** (C17, C20). Reset vector, boot device, the initial image.
*Absence prevents*: anything running at all. The functional oracle for a board is real
software — Linux boot is this project's — and boot software exercises exactly the
information nobody probes in a lab: the map, the devices, the delivery paths, in the
first hundred instructions.

**21. Bus fabric semantics** (C16, C19). Arbitration, contention, DMA visibility. The
DSP56300 dedicates status bits to core-vs-DMA priority — the fabric matters enough that
architectures spend register space on it. *Absence prevents*: any statement about
device-driver-facing behaviour, which is most of what an OS observes.

---

## The pattern

Lay the three lists side by side and the recursion the design discussions predicted is
visible: **a CPU is the base set; a DSP is the base set plus the axes that break scalar
assumptions; a board is the base set plus composition.** The catalogue is one census,
applied at three depths. And each kind's "absence prevents" comes in the same three
shapes: *you cannot build* (missing input), *you cannot claim* (missing evidence), or
*you cannot bound* (missing census — you do not know what you do not model). The first
two are this project's rules (no invented facts; no reference, no differential claim).
The third is its temperament: the honest answer to "what does it take to model X" always
ends with "— and here is what we still do not know."

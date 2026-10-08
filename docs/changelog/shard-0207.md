# DEV_NOTES shard — _(2026-10-05)_ … _(2026-10-05)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-05)_ — "no assembler shapes" was true until the table said otherwise (P4-SYSTEM.6 slice a)

Execution of the `.6` brief's checkpoint (a) measured:

- **A no-change claim must be measured, not inherited.** Decision 1's "no
  assembler shapes (the zero-operand ecall/ebreak precedent)" read true — and
  was FALSE on first probe: ecall/ebreak carry no operand fields, but fence.i's
  table row LISTS imm12/rs1/rd, and the table-driven arity check refused the
  bare standard-software spelling. The chapter itself settles what the correct
  behavior is ("standard software shall zero these fields"), so the acceptance
  landed as a named, cited special case in the assembler — the same shape as
  the A-suffix machinery, never a table edit. The OTHER no-change claims held
  under the same discipline: the nop effect needs no Sem variant (the existing
  arm), and gen_definition's lowering of the one-form fragment needs no
  conditional support at all — the emitted mask covers funct3+opcode only,
  which is exactly the shall-ignore decode, over two standalone-compiling trial
  compositions.
- **The pin's strength is the second measurement.** 73 bytes is one curl — the
  evidence is the fresh re-fetch being byte-identical, the scope-vs-tables leg
  enumerating 87==87 with the table pinned-but-excluded (the named exclusion
  with its flip condition), and the fragment leg agreeing the generated
  zifencei.sexp against the pin. A pin nobody re-derives is a number, not a
  corroboration.
- **The shall-ignore rule is a DECODE property, and both decoders show it.**
  The fragment keeps the operand fields out of the mask, so 0x0011118f
  (nonzero imm12/rs1/rd) decodes as fence.i in the generated module — and
  spike-dasm, the documented second decoder, returns `fence.i` for the same
  word. The reserved-fields probe cell at slice (b) is already sanctioned by
  measurement.

promotion: declined (the durability is the machinery — the zero-operand
acceptance is armed by the probe spellings and the 99-guest byte-exact
re-assembly, both re-runnable).
## _(2026-10-05)_ — Sail numbers the delivery step too, and a named gap can be configuration-shaped (P4-SYSTEM.5 slice d)

The `.5` matched attempt measured:

- **The interrupt-delivery step convention is the fetch-fault convention.** The
  first comparator run "diverged" every i-* guest at its first delivery — Sail
  had no row there. Reading the trace: Sail's numbering JUMPS [9] → [11] at the
  delivery — it numbers the step and prints no row, exactly the `.3` `<fetch
  page fault>` convention. The comparator keys on row numbers (the `.3`
  comparator's own shape); a step no row carries must declare no observation —
  which is precisely what our delivery steps declare. What looked like a
  systematic mismatch was the same declaration in two notations.
- **Every named divergence was platform-shaped, and each had a sentence.** STIP
  needs plat_have_clint (interrupt_regs.sail:250-263) — without a CLINT the
  whole timer block, not just the counter registers, is silent. The halt needs
  a dwell — Sail's wfi is a nop under the matched platform (wfi_is_nop=true, a
  platform declaration, not a shortcut). The TW gap is configuration-shaped:
  under the matched platform Sail NEVER judges TW (the judgment lives only in
  the wait-exit path the nop never reaches); under the wfi-wait variant the
  delivered trap is identical to ours — cause 2, mepc = the wfi's pc, xtval =
  the wfi's word — 30/30. A "reference-model gap" can be the platform both
  sides agreed to declare, and re-measuring it beats inheriting its name.

promotion: declined (the durability is the machinery — the corpus verdicts are
armed by make check; the attempt re-derives from the tracked override).
## _(2026-10-05)_ — the wake is a head evaluation like any other, and the span-zero wake is still evidence (P4-SYSTEM.5 slice c)

Execution of the `.5` brief's checkpoint (c) measured:

- **The WFI-specific mepc rule needs no special case.** §2.1.3.3's "execution
  resumes in the trap handler and mepc = pc + 4" looked like a WFI-only delivery
  path. It falls out of the generic machinery: the WFI RETIRES into the halt (pc
  advanced, instret counted), so the resume's between-instructions delivery writes
  xepc = the hart's pc, which IS the WFI's pc + 4. The halt's whole shape is one
  head evaluation in front of slice (b)'s: waiting → wake? → fall through to the
  ordinary pending evaluation — the same step does wake and delivery, and the
  untrapped resume just executes. One evaluation point, no parallel path.
- **A software-posted source wakes in zero halted steps — and the cell still
  falsifies.** With SSIP posted before the wfi, the very next head resumes, so
  the trace is observationally a nop's. The cell's power is against the WRONG
  wake rule: a wake that required the global enable would stall the guest
  forever, and its expectations (which continue past the wfi) could never derive.
  Evidence strength is not always a trace difference; sometimes it is the
  impossibility of deriving the same file under the false rule (promotion:
  declined — the durability is the machinery: w-sw and the wake suite re-run it).
- **The text-keyed `#|end` is a collision hazard.** mm-wfi's derivation stopped
  26 steps early: stage1's `csrrs x8, mepc, x0` has the same text as the
  fall-through's `#|end` instruction, and the text-keyed marker fired at the
  first occurrence the flow reached. The pc-keyed directives fixed this class
  for derivations at slice (b); the end marker still keys on text — stage1's
  mepc-step moved to x10 to disambiguate. A marker keyed on content will
  eventually meet two identical instructions; the fix is at the guest, never by
  weakening the convention.
- **A gated CSR read is a delivery, not a refusal.** The derivation tool models
  the counter-ACCESS gates (rdtime below M with the gates shut) as the engine's
  own cause-2 trap; the mode-privilege refusal stays for authoring errors. The
  wake corpus reads counters in M only, but the honest mirror is what lets a
  future guest exercise the gate without tooling work.

promotion: declined (the durability is the machinery — the wait/interrupts suites
and the 99-guest corpus re-run every one of these).
## _(2026-10-05)_ — the trap-entry stack runs the other way, and sip cannot clear SEIP (P4-SYSTEM.5 slice b)

Execution of the `.5` brief's checkpoint (b) measured:

- **The derivation tool had the xRET-side stack where trap entry runs the other
  way.** The forked tool's `deliver()` wrote MIE <- MPIE, MPIE <- 0 — mret's
  direction. Trap entry is MPIE <- MIE, MIE <- 0, and the engine's privilege.rs
  had it right all along. The .2–.4 corpora never caught the tool: every prior
  trap fired with MIE=MPIE=0, where the inverted and the correct forms coincide.
  The first guest that enabled interrupts (i-deleg's ecall with MIE=1) nested the
  re-posted SSI INSIDE the M handler and marched mepc into an mret self-loop —
  the tracer showed MIE=1 one step after the ecall, where spec delivery leaves
  it 0. A state-discipline bug hides exactly where every prior execution made
  the wrong and the right form agree; the test that varies the input bit is the
  one that matters (promotion: declined — the durability is the machinery: the
  i-deleg guest and the interrupts suite re-run it).
- **Two read-only bits are load-bearing guest-design facts.** i-vector's
  SEI-to-S cell asked the S handler to clear SEIP through sip — read-only there
  (Computed in the field tables); the engine would have re-delivered forever.
  The guest now rides SEI to M (cleared through mip) and SSI to S (cleared
  through sip) — the same vector evidence with legal clears. And i-accept's
  mtvec delta was 8 bytes long: the delivery landed past the handler's two
  evidence reads and the guest "passed" gutted — caught by reading the
  derivation, not by any verdict. A guest that terminates is not a guest that
  evidenced anything.
- **Authoring against the wrong clock is a silent narrative lie.** i-timer's
  stimecmp=3 assumed time counts the marker instructions; the declared domain
  ticks every step, so time was 5 at that write and STIP never cleared. The
  re-authored guest writes stimecmp=8 and observes 1→0→1 at steps 3→6→8, the
  step counts spelled in the derivations. The same census discipline caught
  S-mode `mstatus` accesses (illegal from S — the guests now ride sstatus) and
  mstatus's UXL/SXL reset bits the tool never modeled (0xA00000000 — the
  runner's first mismatch named them).


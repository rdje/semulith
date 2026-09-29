# The references, their configuration, and what agreement is worth

The materials bill lists the reference models as *materials* — pinned identities, digests,
terms. This chapter is about using them: how each was obtained, how it was configured to
match this profile, what the matched profile actually demonstrated — and, hardest, what an
"AGREE" verdict is worth. The short version, argued below: **less than it feels like, and
more than nothing** — and the difference between those is made by controls, not by
confidence.

A reference model here is a *differential partner*, never a source of truth. The
specification is the truth; the references are two more implementations of it, with their
own bugs, their own bundled assumptions, and — the subject of half this chapter — their own
shared ancestry.

## The cast, honestly labelled

From `profiles/rv64i-lab-v0/references.sexp` (the dossier of record; the bill's
`reference-models.md` table is generated from it):

- **`sail-riscv` 0.14** — the RISC-V International *formal model*, written in the Sail
  ISA-description language, obtained as a pinned prebuilt binary. The primary oracle
  candidate, because it is the only one configurable down to this profile's whole
  platform — and because it is the encoding-independent leg (see the inventory below).
- **`spike` 1.1.1-dev** — the historical golden model, an independently written C++
  interpreter, built from source at a pinned commit (`1e05ddac`). The second
  implementation.
- **`qemu` 11.1.1** — a pre-existing host binary, a dynamic binary translator. Obtained,
  **never configured, never exercised**, independence **unexamined** — recorded so that
  "we have three models" is never misread as "we have three opinions". Nothing this
  project holds rests on it.
- **`act4`** — the RISC-V architectural test corpus, *located and deliberately not
  acquired*. It is a test corpus, not a model — and (the single most important lineage
  fact in the dossier) its expected results are computed by a **configured Sail model**,
  so ACT agreeing with sail-riscv is one semantics answering twice.

## Obtaining a reference so that "obtained" means something

Every obtained candidate is pinned by digest, and the acquisition tool
(`scripts/fetch_references.sh`) was fired RED before it was trusted: corrupting a pinned
digest produced `DIFFERS spike binary …` naming both hashes; restoring produced `MATCH`.
The failures are on the record too — the `brew` package named `sail` is a WordPress
provisioning CLI (the name matched; the software did not), and building Sail from source
was never needed once the prebuilt binary was pinned. An honest "no route" bounds a claim
(SRC-02); a reputation-based availability claim would be the kind of lie SRC-03 exists to
prevent.

## Matching the profile — told through the controls that changed the observation

"Configured to match" is a claim, and this project does not believe claims it has not seen
fail. Three controls made it a measurement.

**The ISA-string control.** The Sail model ships defaulting to a 96-extension ISA string
(`rv64imafdcbvh_…`). The tracked override
(`profiles/rv64i-lab-v0/reference/sail-rv64i-lab-v0.override.sexp`) drives it down to
`rv64i_zvl32b`, and the string is **read back** — `sail_riscv_sim --print-isa-string` —
rather than trusted from the command line. The control: flipping `M` back on in the
override made the read-back report `rv64im_zvl32b` against the pinned `rv64i_zvl32b` — the
verifier caught a one-letter configuration drift. Spike's side is the same discipline with
a different read-back: `--isa=rv64i --priv=m` is the input, and `spike --dump-dts` reporting
`riscv,isa = "rv64i"` is the read-back (with the control that `--isa=rv64im` reports
`rv64im`). The lesson that cost a real defect: the ISA string establishes **the
instruction set and nothing else** — which brings us to the platform.

**The platform correction (DIFF-PLATFORM-DEFAULT).** Underneath a correctly matched ISA
string, the Sail model kept its *default platform*: a core-local interruptor at
`0x0200_0000`, an interrupt generator, live machine interrupt sources, and I/O memory
regions. Measured by probe, not suspected: a guest read the CLINT's `mtime` at
`0x0200_BFF8` with a plain `ld` — no CSR instruction needed — and the value **advanced
across reads** (2, then 3). The laboratory's profile declares no device, so a reference
serving a live counter where the model raises an access fault is not a matched experiment;
it is two experiments. The fix is the override's platform half: `clint` off, the interrupt
generator off, all three machine interrupt sources off, and `memory.regions` reduced to
the single `MainMemory` region the profile declares. Both probes then raised
`load-access-fault`, and the repair is held by a tracked negative fixture,
`guest-no-device` — a guest that *must* fault, so a device becoming reachable again turns
the run red. (And it carries `(cross_model false)`: Spike's built-in CLINT cannot be
configured away, so its comparison on this guest is disabled — printed on every run, never
silently applied.)

**The decisive control (P0-PROFILE.6).** With the profile matched, `smoke-trap` — a
misaligned load — agreed three ways. Then the control: the Sail configuration's misaligned
policy was flipped back to *"handled invisibly"*, **the same ELF and nothing else
changed**, and the run failed exactly where it should:

```
FIRST DIVERGENCE at aligned step 2 … sail-riscv writes=[(x1, 0)] … spike writes=[]
```

One model loaded a value; the other trapped. **The two models agree because the profile
is matched** — and that sentence is now a measurement, not a hope. This is the control
the whole chapter exists to teach: if you configure a reference and never flip one knob
back, you have not matched a profile, you have written a configuration file.

## What comparison actually compares

The three models do not emit the same trace shape, so comparison happens in one
observation vocabulary — `(pc, encoded word, register writes, trap)` — and the differences
that are *harness*, not semantics, are enumerated in the dossier rather than smoothed
over. Each one was found by being bitten:

- **DIFF-TRAP-RECORD-SHAPE** — Spike emits *no* commit record for a trapping instruction;
  Sail records the trapping instruction as a step carrying the trap. The comparator's
  first version compared only the overlapping prefix and printed `AGREE over 2 aligned
  step(s)` for a run in which one model trapped and the other stopped — **a false pass,
  caught by running it**. A shorter trace is now a non-agreeing verdict that must be
  explained, and the adapter reassembles Spike's split record from its own disassembly
  line. This mistake is why the mutation suite exists.
- **DIFF-RESET-VECTOR** — Spike executes a five-instruction built-in reset vector at
  `0x1000` before the ELF entry; Sail begins at the entry. Traces are aligned on the first
  step whose pc is the declared entry — comparing step 0 with step 0 would manufacture a
  divergence out of a harness difference.
- **DIFF-ELF-STRICTNESS** — Spike refuses an ELF with no section header table; Sail loads
  it. The guest writer emits the conformant artifact — an input only one comparator
  accepts is not a matched experiment.
- **DIFF-FETCH-GRANULARITY** — Sail performs two 16-bit fetch reads per 32-bit
  instruction. Below this profile's observation granularity — recorded, not normalized,
  so it cannot surprise a future memory-access comparison.

And the adapter's own discipline: each model's *spelling* of an exception is mapped to the
architectural cause code from the pinned causes table, and **an unrecognised spelling
raises**. That refusal fired mid-run when a misaligned store arrived spelled
`misaligned-store/amo` — a trap the comparator cannot name is a trap it would otherwise
drop, and a dropped trap reads exactly like agreement. (The ecall/ebreak spellings —
`m-call` / `trap_machine_ecall`, `software-breakpoint` / `trap_breakpoint` — were learned
by measurement the same way.)

## When the references disagree with *each other*

Two measured reference-vs-reference differences, and they teach more than any agreement:

- **DIFF-FENCEI-EXECUTED** — the word `0x0000100F` (fence.i) **executes as a nop on both
  references**, although the matched configurations exclude Zifencei (the override sets
  `Zifencei supported: false`; Spike runs `--isa=rv64i`). This profile declares Zifencei
  absent, so semulith reports the reserved encoding under its declared
  `D-RESERVED-DECODE` policy and stops. A legitimate UNSPECIFIED divergence — and the
  comparator now expresses it *as* an expected divergence: `it-fencei` declares
  `(expect_divergence (difference "DIFF-FENCEI-EXECUTED") (at_step 1))`, the prefix must
  agree, the first divergence must land at exactly that step, and sail vs spike must agree
  over their full length. The deeper lesson, measured twice now: **the ISA string and even
  the extension flags do not fully describe what a reference executes.**
- **DIFF-TVAL-PHYS-MASK** — sail 0.14 masks the access-fault tval to its 56-bit
  physical-address width; spike and semulith report the full address. Measured at the
  interaction-matrix probes (an `sd` at `0xFFFF…FFF8` reports `0x00FF…FFF8` on sail; at
  exactly 2^56 sail reports tval 0). Not a defect in anyone — a recorded difference, whose
  consequence is in the evidence plan: three-way tval comparisons keep fault addresses
  below 2^56, which is why the `it-fault-wrap-sd` guest wraps to address 0 instead of the
  top of the space.

The pattern to copy: a difference between references is **recorded with its measurement**,
never averaged away and never silently absorbed into a mask.

## Why three models is not three opinions

`EVD-04` requires shared semantic ancestry to be *examined* rather than inferred from the
fact that the binaries differ. The dossier's independence inventory does that per
subsystem and per pair — including the pairs nobody has examined, because an omitted pair
reads exactly like an independent one:

- **Instruction encoding — sail ↔ spike: not-shared.** Spike's `encoding.h` declares
  itself generated from `riscv-opcodes`; the Sail model hand-writes 59 `encdec` mapping
  files and never mentions the table. ⭐ And the cut runs *the other way than first
  assumed*: **our** assembler parses `riscv-opcodes`, so our bytes share an ancestor with
  *Spike*, not Sail. Sail decoding our guests as intended is the genuinely independent
  confirmation of the encoding; Spike doing so is the same table answering twice.
- **Floating point — shared.** Both vendor Berkeley SoftFloat; after normalizing one
  release-number comment line, **184 of 199** overlapping files are byte-identical. A
  differential FP test between them would test one implementation twice. Nothing in this
  profile rests on floating point — the record stands so that P4's evidence plan never
  counts that agreement as two opinions.
- **Integer semantics — no-evidence-of-sharing.** No textual reference from one codebase
  to the other. Deliberately *not* recorded as `not-shared`: absence of a textual
  reference is weak evidence, and the strongest claim the evidence supports is what the
  record says. The 492-step differential rests on exactly this honesty.
- **Expected-result derivation — shared.** ACT's signatures are computed by a configured
  Sail model. ACT remains valuable as *external tests* — a corpus someone else chose —
  and can never serve as independent confirmation of Sail.
- **QEMU ↔ each — not-examined.** Nobody has looked; recorded as unexamined, and any leaf
  proposing QEMU as a comparator must do the examination *before* its agreement counts.

So what is an AGREE worth? Per leg, precisely: the **encoding** of our guests is
independently confirmed by Sail alone; the **semantics** rest on both references agreeing
with each other and with specification-derived expectations across the whole corpus
(40 guests, 492 aligned steps, byte-identical reproduction — finite, tested evidence,
never universal proof, EVD-01); and **nothing** rests on ACT4 or QEMU. Two honest limits
complete the picture: the Sail model will not emit its effective merged configuration
(measured — the dump ignores the override), so the effective configuration is recorded as
(release default) + (tracked override) and the merge is ours, not the model's report; and
every verdict above is a verdict about *these inputs on these hosts*, reproducible by
`scripts/run_semulith_smoke.py`, not a property of the universe.

## Build it yourself

1. Obtain each reference by pinned digest, and fire the fetcher RED before trusting it.
2. Configure the reference to the profile — then **read the configuration back**
   (`--print-isa-string`, `--dump-dts`), never trusting the command line you typed.
3. Match the **whole platform**, not the instruction set: probe for devices the profile
   does not declare (a live counter where you expect a fault is the tell).
4. Run the control: flip one configuration knob back, same input, and watch the
   observation change. A match never seen to fail is a configuration file, not evidence.
5. Record every difference you observe — harness, vocabulary, or reference-vs-reference —
   with its measurement, before you build on the comparison.
6. Examine ancestry per subsystem before counting agreement as opinions; write down the
   pairs you have *not* examined, because an omitted pair reads exactly like an
   independent one.

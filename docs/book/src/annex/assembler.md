# Annex: how the tracked assembler works

`scripts/riscv_asm.py` is the project's RISC-V assembler and ELF64 writer, using the
Python standard library. It exists so that every guest program's bytes can be
*accounted for*: who encoded them, from which table, with which rule. This chapter walks
through it the way the code is organized, so that a reader could write an equivalent tool —
not just agree that this one works.

## Why it exists at all

The laboratory's evidence rules (EVD-05) require a guest's expected observations to be
derived from the **specification**, never from a model's output. The same discipline applies
to the program's bytes: they must be encoded independently of the models under test. A
cross-compiler would encode them fine, but it would be one more artifact whose provenance
has to be established, installed, and pinned. The assembler is the smaller, auditable thing:
it reads its encodings from pinned tables, carries **no opcode constant of its own**, and
refuses anything it cannot derive. A typo in it cannot invent an instruction — it can only
fail to find one.

## The pipeline it sits in

```text
riscv-opcodes (pinned upstream, target/refs/riscv-opcodes/)
    rv_i, rv64_i          fixed bits + operand list per instruction
    arg_lut.csv           where each operand field sits in the 32-bit word
    constants.py          how the B/J immediates are scattered
        │  scripts/gen_fragments.py
        ▼
definitions/riscv/rv64i.sexp        the reusable fragment (tracked, the one format)
        │  composed by
        ▼
profiles/rv64i-lab-v0/encoding.sexp the unit's composition document (tracked)
        │  Assembler(encoding.sexp) — resolve_composition() merges the fragments
        ▼
   instruction words ──► gen_guests.py ──► crates/semulith-verify/src/guests.rs
                     └──► write_elf64() ──► the ELF the live experiment runs
```

Two read paths exist, and the asymmetry is deliberate: the **canonical** path reads the
tracked `encoding.sexp` — the encodings the repository owns, so a fresh clone can build
every guest with no network and no upstream checkout. The upstream-table path exists only
so `gen_fragments.py` can *re-derive* the canonical fragment from the pinned upstream, and
a gate (`scripts/check_definition_gen.sh`, and the fragment's own regeneration check) keeps
the derived artifact honest.

## The tables, and what a line means

A line in `rv_i` is a name, then operands and fixed-bit assignments:

```text
addi    rd rs1 imm12           14..12=0 6..2=0x04 1..0=3
add     rd rs1 rs2 31..25=0  14..12=0 6..2=0x0C 1..0=3
beq     bimm12hi rs1 rs2 bimm12lo 14..12=0 6..2=0x18 1..0=3
```

Reading `addi` aloud: bits 14..12 (the funct3 field) are 0, bits 6..2 are 0x04, bits 1..0
are 3 — and the remaining fields are the operands `rd`, `rs1`, `imm12`. Where those fields
*sit* is a separate table, `arg_lut.csv`:

```text
"rd", 11, 7
"imm12", 31, 20
"shamtd", 25, 20
```

So encoding `addi x9, x8, -2048` is: start from zero, OR in the fixed bits, place `x9` into
bits 11..7, `x8` into bits 19..15, and `-2048 & 0xFFF` into bits 31..20. Every placement goes
through one width-checked helper (`_place`): a value that does not fit its field is refused,
never masked.

## Composition: a unit never copies an instruction

`encoding.sexp` does not list instructions; it *composes* fragments
(`(compose (base "riscv/rv64i") (extensions))`). One resolver — `resolve_composition()` —
turns that into the merged instruction set, and it is shared by the assembler and the
composition checker on purpose: a second, hand-written resolver was a measured regression
source (`MODEL-COMPOSE.4`), so there is exactly one. A fragment that names a `requires` the
composition has not provided is refused by name — a fragment with an unmet dependency would
compose by luck, not by construction.

## The three operand classes

1. **Fixed bits** — placed verbatim from the table.
2. **Contiguous fields** — `rd`, `rs1`, `rs2`, `imm12`, `imm20`, the shift amounts `shamtd`
   (6 bits) and `shamtw` (5 bits), FENCE's `fm`/`pred`/`succ`, and the S-type pair
   `imm12hi`/`imm12lo`. Each is range-checked against the architecture's rule: a 12-bit
   immediate must lie in −2048..2047, a shift amount in its field's width, a register in
   x0..x31. The S-type stores *one* immediate split across two fields; the assembler takes
   the byte offset once and splits it itself.
3. **Scrambled fields** — the B- and J-type immediates, spread across non-adjacent bits.
   Their layout is *derived, not typed*: `constants.py` states it in machine-readable form,
   and the assembler parses those descriptors:

   ```text
   "bimm12hi": "imm[12|10:5]"      "bimm12lo": "imm[4:1|11]"
   "jimm20":   "imm[20|10:1|11|19:12]"
   ```

   The derivation is **self-validating**: the bits a descriptor accounts for must total
   exactly the field's width from `arg_lut.csv` (7, 5, and 20 respectively), or the table is
   refused. A silently wrong immediate is an instruction that assembles and jumps to the
   wrong address — so a layout the assembler cannot reconcile is a layout it will not use.

Two conventions fall out of the specification and are enforced here: branch and jump offsets
are in **bytes**, and bit 0 is not encoded (offsets are "signed multiples of 2 bytes") — an
odd offset is refused rather than silently truncated.

## The front-end: two passes, deliberate smallness

`assemble_units()` makes two passes because a branch may target a label defined *later*: pass one
records statements and label addresses, pass two resolves a label operand to
`target − pc` — exactly what the specification means by "added to the address of the branch
instruction". Duplicate and undefined labels are refused.

Registers are accepted only as `x0`..`x31` — or `f0`..`f31` where the operand is a
floating-point register. ABI names (`ra`, `sp`, `a0`, `ft0`, …) are a software convention,
not architecture, and the assembler deliberately does not know them — a guest that means
`x1` says `x1`, and the trace, the expectations, and the source all speak the same names.

**Which file an operand names is derived, not typed** (`P4-SYSTEM.7`). The opcode tables
name only the *field* — `fcvt.w.s` lists `rd rs1 rm` — yet its `rd` is an integer register
and its `rs1` a floating-point one. The semantics say which: the rule reads `(freg rs1)` and
writes `(reg rd)`. So the assembler reads the unit's composed semantics files and spells an
operand `f0..f31` exactly when its rule names it through `(freg …)`; the other spelling is
refused by name:

```text
fcvt.w.s x5, f1, 1      # x5 <- f1 converted, rounding mode 1 (RTZ)
fadd.s x1, f2, f3, 0    # refused: "operand rd is an f-register (its semantics read
                        #  (freg rd)) — spell it f0..f31, got 'x1'"
```

The rounding-mode field `rm` is written as its 3-bit value (`0` RNE … `4` RMM, `7` DYN): the
mode names belong to the specification's table, not to this assembler, and the guest's
comment names the mode. Against the second decoder, all 30 F forms round-trip through
`spike-dasm` (which prints no rounding mode — the field is checked as bits 14..12). General
shorthands (`li`, `mv`, `nop`, …) are absent. The unit's explicitly declared architectural
counter aliases, such as `rdcycle`, are accepted with their pinned encoding.

The raw-data escape hatches place bytes verbatim: `.word 0x…` emits four bytes (added by
`P2-SCALAR.3`), and `.half 0x…` emits two (added by `P4-SYSTEM.12`). They exist because the honest
spelling of "this guest deliberately executes a *reserved* encoding" cannot go through the
mnemonic path — the operand range checks are precisely what refuses such words there
(`fault-reserved`'s 0xFFFFFFFF, `fault-shiftw-res`'s `slliw` with `imm[5]` set). `.word`
takes one numeric literal, range-checked to 32 bits; `.half` checks 16 bits.

## Compressed instructions and exact byte images

The 37 C forms at RV64 with D assemble on a composition that includes C. Compact fields
spell their architectural registers x8–x15 or f8–f15, and each scattered immediate takes one
argument. Arguments follow the encoding's declared field order. For example:

```text
c.addi x1, -32          # signed six-bit immediate
c.addi16sp 16          # x2 is implicit
c.addi4spn x8, 4       # x2 is implicit; unsigned offset in bytes
c.lw x8, x8, 124       # destination, address register, unsigned byte offset
c.fld f8, x8, 0        # the expansion declares an f destination and x address
c.fsd x8, f9, 0        # address register, f source, byte offset
c.lui x3, -32          # unshifted signed six-bit value: -32 << 12
c.jalr x1              # source register; x1's link is pc+2
c.nop                  # also accepts an explicit HINT immediate
```

Widths and low zero bits come from the declared scatter pieces. Out-of-range and misaligned
immediates, wrong register files, and reserved operands refuse by name. If operands select a
more specific encoding, the assembler requires that spelling: `c.mv x1, x0` would encode
`c.jr x1`. A deliberately illegal parcel uses `.half`.

`assemble_units()` returns each value with its byte length, address and original text.
`assemble_image()` joins their little-endian bytes without padding. Labels advance by two or
four, so a normal instruction following `c.nop` starts two bytes later. The legacy `assemble()`
API returns four-byte words and refuses any short unit; callers must choose a sized API.
The C assembler probe checks 37 hand-encoded words, 21 operand refusals, HINTs and an exact mixed
image. Wrong compact-register bases, word-stride labels and padded parcels all fail its controls.

The rv64gc guest generator selects the exact byte fixture explicitly:

```sh
python3 scripts/gen_guests.py --encoding profiles/rv64gc-lab-v0/encoding.sexp \
  --guests-dir profiles/rv64gc-lab-v0/guests --image-format bytes \
  --out crates/semulith-verify/src/guests_rv64gc.rs
```

The generated Guest carries `image: &[u8]`; the rv64gc runner loads it directly. Default word
mode retains the scalar fixture's `words: &[u32]` API and refuses a short unit. Representation
does not change observations: both modes carry the same specification-derived expectations.
A compiled probe checks exact loaded bytes and mixed instruction execution through the tracked
runner. Padding the generated image or changing its load offset fails the check.

## The spec-side expectation author

`scripts/derive_rv64gc_expectations.py` computes expected observations independently of the
instruction engine, using hand-written specification rules and the exact-rational FP
reference. A source directive can explain the computed result and name its locator:

```text
addi x5, x0, 1  #: the stage marker begins at 1. | RVI-RV32I 1.1.4
```

```sh
# compare the explicit historical author corpus without changing a file:
python3 scripts/derive_rv64gc_expectations.py --check-owned
# inspect one record for drift, or author it deliberately:
python3 scripts/derive_rv64gc_expectations.py --check profiles/rv64gc-lab-v0/guests/m-div.s
python3 scripts/derive_rv64gc_expectations.py profiles/rv64gc-lab-v0/guests/m-div.s
```

The promotion census identifies 42 records that this producer re-derives byte-for-byte.
Other legacy records keep their original producers and prose; this is an explicit bounded
author, with unknown instruction shapes refused by name. Reserved OP/shift upper bits refuse
before effects. Its data walk checks SUM, MXR and the U bit, including the rule that SUM
allows supervisor data access to user pages but never supervisor instruction fetch there.
C expansion and instruction-fetch translation are still upcoming authoring work. None of
these checks turn the author into a conformance oracle.

## The ELF writer — and a measured harness difference

`write_elf64()` wraps the words in a minimal ELF64 little-endian RISC-V executable: one
`PT_LOAD` segment at the entry address. Notably, it emits a **section header table even
though execution does not need one** — because of a measured difference between the two
reference models: Sail loaded and ran a sectionless ELF without complaint; Spike refused it
outright (`elfloader.cc` asserts `e_shstrndx < e_shnum`, and `0 < 0` is false). That is a
*harness* difference, not a semantic one, and the right response is to emit the conformant
artifact rather than carry a per-model variant — an input only one comparator accepts is not
a matched experiment.

## Running the rv64gc Sail experiment

The tracked adapter builds an ELF from the exact byte image and runs the binary pinned by
the profile's reference dossier. It materializes the matched override through the existing
conversion owner. For example, with the reference binary acquired:

```sh
python3 scripts/run_rv64gc_sail.py m-mul m-div m-word m-alias \
  --out-dir target/rv64gc-sail
```

Each guest runs twice. Both processes must succeed, produce fresh trace files and yield
byte-identical traces. Every ordinary expected instruction needs a trace row, even if it
changes no register. A declared interrupt-delivery or fetch-fault gap instead needs its
matching trace event. An empty or truncated trace cannot agree just because a missing
instruction writes nothing. Malformed, duplicate and unknown records refuse by name.

```sh
# cached row evidence can be checked without launching a reference process:
python3 scripts/run_rv64gc_sail.py --check-trace target/rv64gc-sail/m-div.0.trace m-div
```

The cached check explicitly says that process status is unavailable. The verdict covers
the declared register change-observations, with finite-input scope; it does not certify
unrecorded state or turn a component run into profile acceptance.

## The refusal discipline

Every failure is an `AsmError` that names what could not be derived — an unknown mnemonic, a
malformed register, an immediate out of range, an odd branch offset, a table whose shape
changed, a fragment whose dependency is unmet. The principle is the project's general one:
**a generator that guesses is a second definition.** The assembler's value as evidence
machinery is precisely that its output is a pure function of tracked, pinned inputs — and
that everything else is a loud refusal.

## What it does not claim

The pinned specification artifacts do not contain the encodings (the format diagrams are
images — measured: zero bit-pattern strings in any of them), so the encodings come from
`riscv-opcodes`, which is *also* upstream of Sail and Spike. That shared ancestry is stated,
not hidden: byte-level agreement with the references is **not** an independent confirmation
of the encodings. The recorded mitigation (P0-PROFILE.6) is a second decoder from a
different codebase — `spike-dasm` was asked to disassemble the emitted bytes and required to
return the mnemonics that were requested. What the live differential independently confirms
is the *semantics*, which is what it is for.

## Try it

```sh
# assemble two instructions by hand, from the canonical composition:
python3 - <<'EOF'
import sys; sys.path.insert(0, "scripts")
from pathlib import Path
from riscv_asm import Assembler
asm = Assembler(Path("profiles/rv64i-lab-v0/encoding.sexp"))
for word, text in asm.assemble(["loop: addi x1, x1, -1", "bne x1, x0, loop"]):
    print(f"{word:#010x}  {text}")
EOF

# the guests the commit gate runs are generated through this same assembler:
python3 scripts/gen_guests.py --check     # refuses drift between guests.rs and the sources
```

The chapter on the laboratory's guests (see *P2 — the first validated profile*) shows what
those bytes are for: every value they produce was predicted from the specification before
any model ran, and the assembler is how the *program* side of that experiment stays equally
accountable.

## Independent compressed component expectations

The expectation author uses `scripts/spec_c.py` to hand-reconstruct C fields from the pinned
specification diagrams. Its `execute_c` component handles one complete parcel. It returns
the next address and GPR writes, so the caller can commit those writes after all reads.
Traps and memory/FP effects use the same spec-side hart as ordinary operations.

```bash
PYTHONPATH=scripts python3 - <<'PY'
from derive_rv64gc_expectations import Hart, execute_c
hart = Hart()
next_pc, observation = execute_c(hart, 0x5081)  # C.LI x1,-32
assert next_pc == 0x80000002
assert observation['writes'] == {1: 0xffffffffffffffe0}
PY
python3 scripts/probe_c_author.py
```

The hart also offers exact translated parcel fetching. This reads memory under the fixed
64-KiB laboratory region; the image length does not define where fetching stops.

```bash
PYTHONPATH=scripts python3 - <<'PY'
from derive_rv64gc_expectations import Hart, ENTRY, REGION
hart = Hart()
hart.pc = ENTRY + REGION - 2
hart.write(hart.pc, 2, 0x5081)
assert hart.fetch_instruction() == ('insn', 0x5081, 2)
assert hart.log == [('fetch', hart.pc, 2)]  # no inaccessible neighbor read
PY
python3 scripts/probe_gc_fetch.py
```

A word prefix instead reads two parcels. A second-parcel fault saves the starting PC in
EPC and the failed virtual address in tval. Page walks precede their physical requests;
a failed translation issues no fetch request, while a refused request counts as an attempt.
Fetch itself advances neither time nor retirement. These APIs are finite spec-side evidence;
compressed guest execution with explicit budgets is the next slice. The existing
`--check-owned` route retains its 42 historical byte-identical records.

# The compiled guest: when the compiler becomes the tester

Every guest before this one was **hand-written assembly**: a person chose each
instruction, and a person derived each expected value from the specification's prose.
That is strong evidence — 492/492 agreed steps strong — but it carries one honest
weakness, and this book exists to say such things plainly: **the same mind reads the
specification twice** — once to write the model, once to write the test. A
misunderstanding the author holds will sit identically in both, and the comparison will
agree beautifully on a shared mistake.

The way out is to make the test-writer someone who was never in the room. A C compiler is
exactly that: an industrial, independently maintained reader of the architecture, which
turns *its* understanding of C and of RV64I into an instruction sequence — register
allocation, calling conventions, jump tables — that no one here chose. If the model
misread the specification, code emitted from that independent reading has a real chance
of stepping on the difference. That is the idea behind `guests/c-scope.c`, the first
**compiled** guest — and the roadmap agreed with the idea years before it landed: gate
`G1`'s sixth criterion demands that *a compiled freestanding guest program retires under
first-divergence comparison — **not a hand-encoded toy***, with C named as the first
guest path (Rust is only fractionally executable on this profile, and no riscv64i Rust
target exists — a measured fact, recorded in
`reference_what-running-real-rust-actually-requires`).

## The guest: self-checking by design

`c-scope.c` is a freestanding C tour of the profile's whole declared scope: 64-bit and
32-bit arithmetic (including the wrap directions), every load/store width with
little-endian lane composition, branches and a counted loop, real function calls through
the argument registers with an actual stack, and variable shifts. No multiplication or
division anywhere — M is not in this profile, and `-nostdlib` means a helper call would
fail the link rather than slip one in. ⛔ A measured correction (P2-SCALAR.5 strand 3):
an earlier draft of this paragraph promised "a `switch` that compiles to an indirect
jump" — but clang at -O1 constant-folds `pick()`, so the ELF contains NO jump table; the
evidence covers what the ELF contains, and the jump-table idiom is pinned instead by
`dir-chase`'s measured load→jalr sequence. The chapter's lesson stands, sharpened: the
compiler, not the author, chooses the instruction sequence.

The design decision that makes it work as evidence: the guest is **self-checking**.
Every expected value is a constant derived from the C abstract machine and written into
the source by the author (`fib(20) == 6765`, little-endian lane contents, shift
results). Each check that fails routes to `fail(code)` — a distinct, observable fail
token followed by `ebreak`. So *any* runner that mis-executes — semulith, sail, spike —
takes a visibly different path from the other two, and the three-way first-divergence
comparison fires at exactly that check. Three-way agreement on the success path **is**
the expectation.

Why not the per-step expectation documents the assembly guests carry? Because for a
compiled guest, *the compiler — not the author — chooses the instruction sequence.* A
document pinning "step 47 writes x13" would be a fingerprint of one compiler's output,
not a derivation from the specification. The honest layering, kept deliberately: the
specification-derived per-step expectations stay with the assembly corpus; the compiled
guest's evidence is the differential plus its self-checks (`EVD-04` applies throughout:
agreement is tested evidence for these inputs, never universal proof).

## The toolchain: measured present, never installed

The blocker that held this guest back was not technical difficulty but two undecided
questions — who may own the work, and what compiles it. Both were answered by delegation
on `2026-09-30`, and the toolchain answer is a good example of the project's
measure-first rule (`decision_c-guest-routing-and-toolchain`):

- **Apple clang 21.0.0 has no RISC-V backend.** Asking it for `--target=riscv64` fails:
  `unable to create target: 'No available targets are compatible with triple
  "riscv64-unknown-unknown-elf"'`. Assumption would have shipped a broken script.
- **Homebrew `llvm@21` clang 21.1.8 compiles RV64I correctly** — verified by compiling
  `-march=rv64i -mabi=lp64` and reading the object code back with `llvm-objdump`.
- The keg ships no linker; **zig 0.16.0's bundled `ld.lld` 21.1.8** does the link.

Nothing was installed. `scripts/build_c_guest.sh` *probes* every candidate for the
RISC-V backend and **refuses by name** if none is found — a clang that cannot target
riscv64 is never silently substituted. The resulting ELF is a build artifact with the
same standing as the reference binaries: the live differential needs it, the commit gate
does not. The tracked facts are the C source, the build script, and the pinned toolchain
identity.

## Two defects the process caught before any green — and why they are the best part

The dual mandate says the mistakes stay in the record because they are the instructive
part. This guest produced two in one afternoon, plus a third in the gate machinery —
each found by an instrument, never by review.

**1. The guest caught its own author's undefined behavior.** The first compiled binary
stopped at `fail(0x0501)` — the `fib` check. The disassembly showed something alarming:
clang had deleted *the entire rest of the program* and routed the fall-through straight
to `fail`. That is the signature of whole-program UB exploitation, and the hunt is the
lesson. The first suspect — strict aliasing on the buffer's width-punned accesses — was
measured **innocent** by the `-fno-strict-aliasing` control. Bisecting the sections
found the real cause: the draft tested the *W shamt boundary with `w32 << 33`. But a
32-bit shift by ≥ 32 is **undefined behavior in C** (C11 6.5.7p3) — it is *not* "the ISA
reads five shamt bits". The C abstract machine simply cannot express that boundary;
clang, allowed anything by UB, chose to delete half the program. With the shift narrowed
to the C-legal 31, the same compile restored `call fib` and all four closing `emit`
calls. The boundary itself stays where it always was — `bound-shiftw`'s *assembly*, the
one place it can be stated. The comment now lives in the guest's section 6, where it
bites.

**2. A comparator gap that 492/492 never exercised.** With the guest clean, the
three-way comparison diverged at aligned step 7 — on `li a0, 0` with a0 already zero.
Sail and spike log the destination register on *every* retired instruction, so both
recorded `x10 <- 0`. Semulith's runner diffs **values** — its declared observation
vocabulary is *the visible register change* — so it recorded nothing. Both are
defensible reductions; they are just not the same one. The hand-written corpus never
saw the case, because its authors pre-write destinations so that every expected write is
visible (the P2-SCALAR.1 lesson, enforced by the offline gate). A compiler emits
no-change writes routinely. The fix went where the vocabulary is owned: `align` in
`compare_traces.py` — the single funnel all three traces pass through — now reduces
every trace to visible changes using a shadow register file seeded from the declared
reset state. The two new self-test arms exist to keep the reduction honest: a dropped
no-change record must agree (GREEN), and a real change must *never* be dropped (RED),
19/0. A normalization that could hide a difference would be worse than the gap it
closed.

**3. The gate caught itself.** `GATE-REPORT`'s tamper control worked by editing the
report's verdict text — `sed 's/incomplete/passed/'` — and asserting the edit is
detectable. That arm would have silently stopped discriminating on the very day a report
legitimately read `passed` — which was this day. It caught its own assumption; the edit
now targets the `Verdict:` marker itself (self-test 6/0). A gate whose self-test
encodes today's expected answer is a gate with a shelf life; the fix removes the
assumption, not just the failure.

## What it proved — and what it did not

Proven: a genuinely compiled freestanding C program retires under first-divergence
comparison against **both** pinned references — **129/129 aligned steps**, reproduced
byte-identically (`python3 scripts/run_semulith_smoke.py`; the smoke's `.c` path builds
the guest, runs it under a budget the closing `ebreak` beats, and reads `e_entry` from
the ELF header). Gate `G1`'s verdict moved from `incomplete` to **`passed`** — moved by
the inputs, through the same generator that refused to flatter the earlier state.

Not proven, stated with the same emphasis as everywhere in this book: this is finite,
tested evidence — one program, two references, one host (`EVD-01`). It is not a
conformance result, and the `CPU-LAB` processor gate has not run. What the compiled
guest changes is the *shape* of the evidence: for the first time, the instruction
stream being checked was written by an independent party. The next layer of exactly
that idea is the external campaign — the pinned ACT4 suite, assembled by the same
toolchain — which is `P2-SCALAR.5`'s second strand.

## Re-run it yourself

```
scripts/build_c_guest.sh                      # probe the pinned toolchain, build the ELF
cargo run -p semulith-cli -- run target/refs/guests/c-scope.elf
python3 scripts/run_semulith_smoke.py         # the full three-way differential
scripts/gate_report.py rv64i-lab-v0 --gate G1 --stdout | grep Verdict
```

# Architecture and canonical definitions — v0.2

## 1. Logical authority, modular files

The canonical processor definition is a versioned package. Its initial layout is:

| Owned input | Content | Owner |
|---|---|---|
| `model.toml` | Model identity, definition version, file manifest, supported generator capabilities | Processor definition |
| `encodings.json` | Encoding fields, decode context, validity predicates, semantic handler bindings | Processor definition |
| `state.json` | Register/state descriptors, widths, aliases, reset constraints | Processor definition |
| `semantics/*.rs` | Typed executable operations, effects, exceptional behavior, progress rules | Processor definition |
| `profiles/*.toml` | Features, configuration constraints, implemented scope, selected choices | Processor definition |
| `sources.toml` | Applicable specification revisions and precise source locators | Processor dossier |
| `requirements.jsonl` | Traceable statements of obligations and evidence policy | Verification dossier |
| `environment/*.toml` | Versioned assumptions/guarantees and their test obligations | CPU/environment contract |

This is a proposed repository layout. Only the planning schemas/examples in this package exist now. File formats may evolve — and have: §1.1–§1.3 describe the format the canonical definition actually uses today, the fragment and its composition operator, and the schema layer that turns "it parses" into validation. OWN-01 remains: one executable owner for each semantic rule.

### 1.1 One format: every engine input is an S-expression

The table above is the v0.2 proposal, and its per-file formats — JSON for encodings, Rust
sources for semantics, TOML for profiles — have been superseded by one decision (director,
2026-09-14, `decision_one-format-every-source-of-truth`): **every source of truth the generator
engine reads is one format, S-expression data**. The reason is composition, not tidiness: a
board that composes two processors must merge their definitions, requirements, obligations and
pinned sources, and a merge is only definable when both sides are the same kind of thing — three
formats would be three merge semantics.

What exists in that format today:

- `definitions/` holds reusable fragments (§1.2), and a profile composes them with its own
  `encoding.sexp`. All of it parses with the project's reader `scripts/sexp.py` and with the
  LinkedSpec Rust route (`specs/Lispish.spec` on the vendored submodule — no S-expression parser
  is hand-written in this project's crates). The two readers are compared mechanically on every
  tracked `.sexp` file by `scripts/compare_readers.py`, which reports agreement file by file and
  refuses an unbuilt or disagreeing reader rather than counting it as agreeing; the comparison
  classifies the two documented reader-contract differences (quoted-numeric typing, escape
  retention) instead of mistaking them for agreement or for defects.
- **Semantics are data, cited.** `definitions/riscv/rv64i.sem.sexp` expresses each instruction's
  semantics in the same format, every rule carrying a citation into the pinned specification
  snapshot; `scripts/check_semantics.py` reports 52 of 52 declared instructions with checked
  semantics — well-formed, complete and cited. *Cited is not verified*: correctness against the
  specification is a differential experiment against an independent reference (P1/P2). This does
  not change §2's generation boundary — the execution backend is still generated dispatch over
  canonical handlers; the data is the definition those handlers derive from.
- The profile **records** are in the format now: `requirements.sexp` (28) and
  `contract-obligations.sexp` (36), converted by `SOT-FORMAT.3` behind the schema layer (§1.3),
  with the round-trip against the retired JSONL proven byte-identical, not asserted. The
  remaining **configuration** inputs moved with `SOT-FORMAT.4`: `profile.sexp` (the
  `[profile]`/`[state]`/`[scope]` tables and all 28 `[[decision]]` records), `state.sexp`,
  `sources.sexp`, `references.sexp`, the matched-profile override `reference/sail-rv64i-lab-v0.
  override.sexp`, and the guest expectations `guests/*.expected.sexp` are all one document form
  each, validated against six schemas, with the round-trip against the retired TOML/JSON proven
  field-for-field and the files' commentary surviving as first-class `(comment "…")` forms —
  the format's reserved annotation head, never dropped. The one foreign-tool input — the Sail
  model reads JSON — is derived from its `.sexp` on every run (`target/refs/…override.json`,
  byte-identical to the tracked original), so the `.sexp` stays the single source of truth.

### 1.2 Fragments, and the composition operator

A **fragment** is a complete, independently checkable description of one thing — one ISA base,
one extension, one semantics set. It lives in `definitions/` rather than inside a profile
because a base ISA is shared by every profile that composes it; copying it per profile would be
the duplication composition exists to avoid. Each fragment declares its `id`, its `kind`, the
fragments it `requires` — the M extension requires the base because it reuses the base's operand
fields and defines none of its own; a fragment with a hidden dependency is a fragment that
composes by luck — and the pinned `source` files it was generated from. Fragments are generated
by `scripts/gen_fragments.py` from pinned upstream tables and are changed by regeneration, not
by hand.

**Composition** is the operator that makes a unit from fragments: a unit's encoding space is the
union of its fragments' encoding spaces, and the union is decided, not hoped.
`scripts/check_encoding_disjoint.py` refuses any word that two instructions both claim, so a
profile that composes an extension overlapping its base fails loudly. Encoding composition is
decidable and checked today (`MODEL-COMPOSE.1`/`.2`); the records compose the same way
(`SOT-FORMAT.5`): `scripts/merge_records.py` unions two units' requirements, obligations and
pinned sources by id — same id must mean the same content, a source id must pin the same bytes,
and every dependency, obligation link and citation must resolve across the union or the
composition is refused with the conflicting fact named. And the composition claim is
conditional no longer in name only: `scripts/discharge_assumptions.py` is the mechanical form
of `docs/CPU_ENVIRONMENT.md` §5 — every `environment-assumption` must be discharged by a named
guarantee in the merged unit, or the composition is rejected naming it (`MODEL-COMPOSE.3`; the
profile's own 8 assumptions discharge 8/8 today).

### 1.3 The schema layer

An S-expression reader accepts anything syntactically, so "it parses" is not validation. The
schema layer declares every construct — its head, its fields, their arity and value types,
whether they repeat — as data in `schema/`, and refuses an undeclared construct, an unknown
field, a wrong arity or a wrong value type **by name**, never silently. Adding a domain
construct — a register file, a memory map, a peripheral — then requires a schema file and zero
lines of reader code. The schema language is written in itself, and its own description
validating under itself is the fixpoint that proves extensibility rather than asserting it
(`scripts/check_sexp_schema.py <file.sexp> <schema.sexp>`; `schema/schema.sexp` is the language
in itself).

Built today: the language (`schema/schema.sexp`, four declaration kinds — `(schema …)`,
`(construct …)`, `(field …)`, and `(operator …)` for positional mini-languages the record
grammar cannot state, such as the fragment files' `(fixed (31 25 0x0) …)` triples and the
semantics effect expressions; field declarations since `SOT-FORMAT.3` also carry optional
facets — `(pattern …)`, `(min-length N)`, `(min N)`, `(unique yes)` — the record contracts
demanded and the layer now states as data), plus one schema per corpus family — `encoding.sexp`,
`fragment.sexp`, `semantics.sexp`, `requirements.sexp`, `contract-obligations.sexp` and, since
`SOT-FORMAT.4`, `profile.sexp`, `state.sexp`, `sources.sexp`, `references.sexp`,
`override.sexp`, `expectations.sexp` — under which the tracked corpus validates; the semantics'
32-form language is data there, and `scripts/check_semantics.py` loads it. The profile's
requirement and obligation catalogues are in the format behind this layer (`SOT-FORMAT.3`), and
its whole dossier with them (`.4`), each family read through the single mapping owner —
`scripts/records_sexp.py` for the catalogues, `scripts/dossier_sexp.py` for the dossier — so the
correspondence lives in exactly one place per family; the frozen `examples/` JSONL stay JSONL on
purpose, still validated by the tracked JSON-schema validator. The layer deliberately never reads
a second file: checks that need two sources of truth (operand scoping against the encoding,
coverage of the declared instructions, citation against a profile's pinned sources) live in the
consumers. Configuration, state and provenance converted behind this layer at `.4`; records learn
to merge across a composition boundary at `.5`, and the `SOURCE-FORMAT` gate that refuses any
source outside the format lands at `.6`; until then, `check_semantics.py`/
`check_encoding_disjoint.py` keep checking what they already checked.

These executable definitions belong on the engine/model side of the archogen boundary. They are not implementation syntax to add to eADL. eADL may describe the offered hardware contracts; a versioned adapter connects archogen's resolved implementation plan to Semulith models and composition.

Requirements record what needs to be true and why. They are not an alternative executable instruction implementation. An independent reference is intentionally a separate interpretation used to challenge the canonical model, not a competing production authority.

## 2. Generation boundaries

| Artifact | Derivation | Independence/maintenance rule |
|---|---|---|
| Decoder and decoded-operation types | Encoding/context/validity definitions | Generated; do not maintain a second handwritten table |
| State accessors and inspection metadata | State/alias definitions | Generated checks plus target-specific operations where required |
| Reference interpreter | Generated dispatch plus canonical Rust semantic functions | The functions own behavior; this backend is not an external oracle |
| Disassembler/encoder | Shared encoding fields with explicit syntax metadata | Round-trip agreement is structural evidence, not independent ISA validation |
| Semantic documentation | Canonical descriptors, source-linked handlers, later rendered semantic IR | Handwritten explanation is labeled rationale and reviewed for drift |
| Requirement coverage skeleton | Requirement catalog and declared obligations | Generated skeleton does not invent test results or test adequacy |
| Generated tests | Encoding/semantic constraints | Useful for integration, coverage, and mutation; keep independent expected cases |
| JIT or other optimized backend | Later supported semantic lowering | Preserve defined effects and compare against retained reference plus external evidence |
| Board maps and hardware description | Canonical board composition | Device behavior remains owned by the device definition |
| Platform capability manifest for archogen | Accepted processor/device/board profile and explicit boot contract | Read-only derived view; eADL imports or selects facts without becoming a second hardware implementation |
| Golden results/reference traces | Independent reference, manual derivation, hardware, or proof artifact | Never automatically rewritten from DUT output |

A generated interpreter does not require that every semantic statement already lives in a DSL. Initially the compiler and generated dispatch execute canonical Rust handlers. A later semantic IR becomes the canonical semantic representation only through an explicit migration; the superseded production representation then becomes derived or is removed. Retaining it as an independent comparison implementation requires clear ownership and separate maintenance status.

Generated outputs embed a manifest of definition, generator, configuration, and source fingerprints. CI regenerates and detects drift. An importer also records input dialect and translation coverage; an unsupported construct is a model-generation failure, not a guessed translation.

## 3. Runtime boundary

```text
Pinned external specifications ──► Reviewed canonical processor definition
                                     ──► Generated types and dispatch
                                     ──► CPU state and semantics ──► Observed architectural behavior ──┐
                                          │                                                          │
                                          ▼                                                          ▼
                            Versioned environment contract                          Comparison and evidence
                                 ◄──► Processor test environment (laboratory)              ▲
                                 ◄──► Later board and devices                                 │
                                                              Independent reference and fixtures ──┘
```

LAB and BOARD are alternative providers. The laboratory supplies controlled memory, faults, counter samples, and input events; a board supplies corresponding real modeled device behavior after the CPU gate. The observation layer can be a no-op diagnostic observer without removing semantic effects.

## 4. Rust ownership map

| Component/module | Initial crate | Dependency rule |
|---|---|---|
| Profiles, typed values, generated state, decode/semantics | `semulith-core` | No dependency on CLI or verification harness |
| Environment request/response contract types | `semulith-core` | Describes boundary, does not implement board devices |
| Execution control, progress and stop types | `semulith-core` | Guest time and event ordering are explicit |
| Controlled memory and event fixtures | `semulith-verify` | Implements core boundary for tests |
| Source/evidence graph, adapters, comparators, reducer | `semulith-verify` | Does not supply production instruction semantics |
| User commands and report presentation | `semulith-cli` | Calls core/verification APIs without duplicating behavior |
| Definition generation | Initially build/development module with deterministic outputs | Separate crate only when its scope warrants it |
| Later board/device implementations | Later system crate(s) | Consume versioned core types; no dependency on test-only fixtures |

The task boundary is architectural behavior, not arbitrary crate count. Concrete target state and common arithmetic use native fixed-width values. A nonstandard width can use masked fixed-width storage when it fits; genuinely larger values use an appropriate fallback. Arbitrary width does not imply allocating for every operation.

## 5. Effects, errors, and progress

Use separate typed families for:

- `TargetEvent`: an architectural trap/exception, completed access, or other guest event.
- `Advance`: completed or partial execution progress, waiting, or a requested control stop.
- `ModelError`: missing model behavior, invalid description/configuration, inconsistent internal state, or harness contract violation.
- `UndefinedCase`: a source-classified case handled by the selected diagnostic/exploration policy, not automatically converted into a guest exception.

A target exception may be delivered to a modeled handler and execution continue; it is not synonymous with stopping the emulator. Precise enum shapes are a P1 design result. Constructors and tests help enforce classification, but types alone cannot prove that a developer chose the correct variant.

The execution unit can be an instruction, packet, or restartable suboperation. Required pending effects are model state. Operand snapshots, forwarding, fault priority, partial commits, and restart locations follow the processor definition. Disabling diagnostics must not remove them.

## 6. Performance choices and numeric qualification

Prefer fixed-width scalar storage, generated dispatch, reusable buffers, and no mandatory heap allocation or string formatting in the common execution path. A generic observer with a no-op implementation is a useful design; inspect generated code or measured behavior rather than assuming it is free. Trait objects are not universally forbidden; choose static/dynamic dispatch using measured cost and extensibility needs.

Keep separate benchmark modes for untraced execution, instrumented comparison, and diagnostic tracing. Measure arithmetic, control flow, memory, and fault-heavy mixes separately, along with allocation counts. Small early benchmarks establish regressions, not predicted Linux boot speed.

The numeric interface represents rounding mode, flags, result bits, conversions, and target NaN/boxing rules explicitly. Before production floating-point support, qualify a named Rust implementation against these semantics and independent evidence. Capture shared SoftFloat ancestry, target specialization, thread-local/global status handling, and exact compiler/features. If no suitable Rust implementation passes, implement the required subset in Rust and defer the corresponding CPU capability until validated; no silent native-float or FFI fallback.

TestFloat ordinarily obtains DUT expected values from SoftFloat, so a direct SoftFloat comparison is not automatically another independent numerical engine. See [TestFloat](https://www.jhauser.us/arithmetic/TestFloat.html) and [SoftFloat specializations](https://www.jhauser.us/arithmetic/SoftFloat-3/doc/SoftFloat-source.html).

## 7. Replay, configuration, and snapshots

Capture the effective configuration after defaults and overrides, not merely the supplied fragment. Identity includes code and generator versions, compile features, numeric specialization, initial state, guest image, environment policy, reference adapters, external events, and relevant nondeterministic choices.

Replay may initially restart from an initial fixture. A mid-execution snapshot must additionally capture all future-relevant pending state and validate compatibility. A seed without the generator version and event stream is insufficient.

<!-- ANCHOR: rv64gc-snapshot -->
### RV64GC laboratory snapshots

`semulith snapshot` and `semulith resume` support `--profile=rv64gc-lab-v0`.
The checkpoint is taken **after N execution boundaries**: instructions, delivered
traps and waiting boundaries all count. It resumes from that point to the recorded
total budget. A checkpoint at zero records reset state; one at the full budget
has an empty continuation.
Resume continues the recorded cold-started execution at its step index; the
environment's cold-reset requirements apply at the original run entry.

The versioned JSON format `semulith-rv64gc-snapshot-v1` retains all owners in this
profile's state census: x0–x31 and PC, current privilege, f0–f31, all 26 CSR
storage owners, all four TLB slots and their FIFO replacement position, the LR/SC
physical address/width/valid reservation, ACTIVE/WAITING state, and the complete
declared memory region. CSR aliases are reconstructed from their shared storage.
Cleared reservation metadata and invalid TLB slots remain exact. The library
also retains typed laboratory fault regions; the ELF CLI uses ordinary flat memory.
This format covers the single-hart laboratory. Board/device state and external
event streams need their own declared snapshot contract.

For an ELF built at `target/guest.elf`, these commands record and resume a run
with 64 KiB of memory. All paths are relative to the repository root:

```sh
cargo run -q -p semulith-cli -- snapshot target/guest.elf --profile=rv64gc-lab-v0 --at=12 --steps=60 --size=65536 > target/checkpoint.json
cargo run -q -p semulith-cli -- resume target/checkpoint.json --profile=rv64gc-lab-v0
```

To inspect the uninterrupted run under the same environment:

```sh
cargo run -q -p semulith-cli -- run target/guest.elf --profile=rv64gc-lab-v0 --steps=60 --size=65536
```

The resumed output starts at `[12]` and matches the uninterrupted output from
that boundary onward. ELF loading uses the profile's 2-byte instruction alignment,
so compressed instructions and halfword-aligned entries are supported.

RV64GC snapshots default to 64 MiB and accept explicitly declared regions from
1 byte through 64 MiB without address wrap, and total budgets up to 1,000,000
boundaries. Sparse 4 KiB chunks bound encoding overhead. JSON is limited to
`2 × 64 MiB + 1 MiB`, nesting depth12 and 131072 structural tokens before parsing;
these are artifact limits rather than exact process-RAM limits. The profile's
address width is unchanged. The existing RV64I format and defaults remain supported.
The RV64GC snapshot CLI bounds its ELF input to 65 MiB before parsing.

Restoration checks the compiled definition pins, harness version, runtime-source
fingerprint and Cargo lock identity before executing. It checks complete state
shapes, TLB/reservation structure, ordered nonoverlapping memory runs and the
digest of the entire rebuilt region, including zero bytes. A foreign runtime,
missing state, corrupt memory or unsupported bound refuses with exit2; a model
error during continuation exits1. Harness fetch totals describe the continuation.

The snapshot proof splits every current RV64GC guest at three points through JSON,
including the guest's fault policy, and checks continued steps, fetch totals,
complete final CPU state and memory. Additional controls exercise live reservation
and wait effects, retained TLB replacement state and malformed records. CLI tests
compare ELF continuations for atomics, wait, translation and floating-point cases.
This supplies the snapshot kind of `G-REPLAY`.

### RV64GC replay bundles

`bundle` and `replay` also accept `--profile=rv64gc-lab-v0`. For example, record
the tracked LR/SC guest and reproduce its complete result:

```sh
cargo run -q -p semulith-cli -- bundle --profile=rv64gc-lab-v0 --guest=a-lrsc-pair > target/lrsc-replay.json
cargo run -q -p semulith-cli -- replay target/lrsc-replay.json --profile=rv64gc-lab-v0
```

The current format `semulith-rv64gc-replay-v2` contains a complete input checkpoint,
including memory bytes and typed fault regions; the guest catalogue is not needed
to replay it. The CLI records guests from reset with 64 KiB of memory.
The library can instead record a continuation from any supported checkpoint.
Each record explicitly selects the flat-memory laboratory with no external event
stream. A producer-source identity accompanies the checkpoint's definition,
runtime and dependency identities. These identify the experiment; they are not
signatures authenticating an external author's claims.

The recorded result includes each boundary's incoming PC, resulting privilege
mode and ordered GPR changes, the total fetch requests, any model error, and a
SHA256 receipt of the complete canonical final checkpoint. The final receipt
covers FP/CSR/privilege/TLB/reservation/wait owners and memory, including changes
that the printed GPR trace cannot show. Replay restores the saved input and
recomputes every receipt. An identical replay exits0, including reproduction of
a recorded model error; that establishes reproducibility, not CPU correctness.

A changed trace reports its first differing boundary and field, such as
`MISMATCH at boundary 0: PC`. A fetch-count, model-error or final-state mismatch
names its aggregate receipt without claiming to locate the original instruction.
Mismatches and refused producer/runtime/memory identities exit1. Usage, unreadable
files, malformed records and unsupported formats/event policies exit2.

Bundle continuations are limited to 10,000 boundaries, with the snapshot memory
bound of 64 MiB. JSON is limited to 145 MiB, nesting depth12 and 2,000,000 opening
braces/brackets, commas and colons before parsing. Recorded GPR changes must be
ordered unique x1–x31; model-error text is bounded to 4096 bytes. These artifact
limits bound work without promising an exact process-RAM ceiling. The CLI bounds
its file read before parsing. Its `--mutate=none` spelling selects production.
Board/device/event replay remains outside this laboratory format.

All current RV64GC guests round-trip and replay through this format. Controls
alter PC, privilege, GPR changes, length, fetch/error/final receipts and identities;
mid-execution and empty continuations also replay. CLI checks exercise atomics,
wait/timer, translation and floating-point guests. This supplies the bundle kind
of `G-REPLAY`; the remaining CPU-SYSTEM acceptance work stays open.
Digest strings are escaped as JSON data, including rejected foreign identities;
escaping does not weaken restoration's identity and memory checks.

### RV64GC divergence reduction

Reduce a deliberately wrong model against production, saving a replayable record:

```sh
cargo run -q -p semulith-cli -- reduce --profile=rv64gc-lab-v0 --guest=guest-control --mutate=zext-addi > target/addi-reduced.json
cargo run -q -p semulith-cli -- replay target/addi-reduced.json --profile=rv64gc-lab-v0
```

Use `--mutate=jal-no-link` for the other control. JSON goes to stdout; the byte
counts, evaluation count, retained boundary and minimality result go to stderr.
Both controls retain their original difference (boundary 1/x1 and boundary 7/x5).
An identical reduction replay exits0; this verifies reproducibility of the wrong
result, not correctness of that model or independent ISA acceptance.

The reducer reruns both complete tables from cold reset after each deletion.
It deletes two-byte image chunks, with a final single data byte when present.
Chunks can contain instructions or data; dynamic execution can skip or reuse
encodings. Retention requires the original first differing paired step's index
and both complete observations: incoming PC, resulting mode and all GPR changes.
Deleting bytes can change addresses and control flow; a changed index or value
is rejected. Model errors and length/fetch/final-state-only differences are
outside this property; no paired difference exits1 with that scope named.

The domain is a cold 64 KiB region based at entry, an image up to 65,536 bytes,
at most 1,000 steps, and the same typed fault regions on both sides. The default
512 property evaluations include the original and reserved final verification;
`--evaluations=2` returns an unchanged retaining case with no minimality claim.
A completed single-chunk deletion pass establishes **1-minimality in that deletion
domain**, not a global minimum. A capped search labels minimality unestablished.

`semulith-rv64gc-reduction-v1` stores the original bytes, reducer-source identity,
search limit/count/minimality and two complete reduced-run bundles with identical
cold input. Replay repeats the deterministic search, checks the resulting bytes
and search receipt, replays every child receipt and verifies exact original/reduced
difference retention. It does not require the guest catalogue. Identity, search
or result failures exit1; malformed/unsupported records or usage exit2.

Reduction JSON is bounded to 16 MiB, depth12 and 2,000,000 structural punctuation
characters. The direct reduction reader checks this before parsing. The shared
CLI replay reader applies the common 145 MiB replay guard before parsing the root
format, then the 16 MiB bound for reduction records. Child states must be canonical
cold checkpoints, with zeros after the declared image; arbitrary continuations
use ordinary bundles. These limits bound work without defining a process RAM cap.
This evidence completes the four laboratory `G-REPLAY` kinds; CPU-SYSTEM remains
incomplete on its other axes. The full mutation campaign remains `.15` work.

### RV64GC detector controls

The text demo exposes two deliberately wrong models over the complete RV64GC
instruction table. They perturb the canonical effect data consumed by the same
evaluator; they provide detector controls rather than alternative ISA authorities.

| Mutation | Deliberate fault | `guest-control` first difference |
| --- | --- | --- |
| `zext-addi` | 32-bit ADDI zero-extends its immediate | boundary1, x1 |
| `jal-no-link` | 32-bit JAL suppresses the link-register write | boundary7, x5 |

```sh
cargo run -q -p semulith-cli -- demo --profile=rv64gc-lab-v0 --guest=guest-control --mutate=zext-addi
cargo run -q -p semulith-cli -- demo --profile=rv64gc-lab-v0 --guest=guest-control --mutate=jal-no-link
```

Both examples intentionally exit1: the designated wrong behavior fails the
specification-derived guest expectations. The output identifies the model and
prints both observations at the first differing paired boundary. `--mutate=none`
selects production. A mutation may leave an unaffected guest's trace identical;
this is a finite detector experiment, not a verdict over the whole model.

The overlays retain every other row, encoding, operand, length and compressed
expansion. In particular, C.JALR and C.ADDI retain their own generated effects:

```sh
cargo run -q -p semulith-cli -- demo --profile=rv64gc-lab-v0 --guest=c-links --mutate=jal-no-link
```

That case meets its expectations and exits0. The library's
`model_rv64gc::Model::from_mutation` resolves the same names; `Model::table`
returns the complete table. `run_rv64gc::run_guest_with_model` and
`run_from_with_model` run a selected control with the existing memory/fault policy.
Each control table is cached once with a bounded rebuilt effect spine. Unexpected
canonical effect shapes refuse by name instead of silently building a different
fault. Every current guest checks production trace, fetch, final CPU state and
memory parity through the named API.

The RV64GC demo emits text. Its `--json` flag now refuses with exit2 and an explicit
unsupported-report message; previously that flag silently printed text with a
successful exit. Scalar demo JSON remains available. Unknown GC control names
also refuse2. Replay bundles can record these same named controls, as described
below. Finite divergence reduction completed P4.16 (see the reduction section
above). The complete validator mutation campaign
remains P4.15's work, and CPU-SYSTEM acceptance remains incomplete.

### Recording a declared control model

V2 records a mandatory canonical `model`: `production`, `mutant:zext-addi` or
`mutant:jal-no-link`. That outer field selects the continuation's effect table.
The input checkpoint pins compatibility with the base production definition and
state inventory; it is input data rather than proof of how that state originated.
The producer and runtime identities also pin the controller source. Standalone
snapshot resume continues to select production.

For example, record the deliberately wrong ADDI control and replay its result:

```sh
cargo run -q -p semulith-cli -- bundle --profile=rv64gc-lab-v0 --guest=guest-control --mutate=zext-addi > target/addi-control.json
cargo run -q -p semulith-cli -- replay target/addi-control.json --profile=rv64gc-lab-v0
```

Both commands exit0. Replay identifies `mutant:zext-addi` and reproduces that
model's recorded wrong result; the demo's production comparison still detects
the boundary1/x1 difference. `--mutate=jal-no-link` similarly records and replays
the boundary7/x5 control. The Rust API offers `BundleRv64gc::record_with_model`
and a typed `model()` accessor. Model choice is explicit, and all state, fault,
trace and final-receipt checks still apply.

Changing a valid recorded choice causes re-execution under that choice, exposing
any changed observations. A missing v2 choice, unknown canonical name, non-string
or name longer than64bytes refuses2. CLI mutation names use `none`, `zext-addi`
and `jal-no-link`; recorded names use the canonical forms above.

The parser recognizes the previous v1 production shape, which has no outer model
field. A v1 record carrying that reserved choice refuses2. Parsing supplies its
production meaning and writing emits v2, while keeping its recorded identities.
It cannot make an old source identity current: foreign producer/runtime pins
still refuse1 before continuation. The format's finite limits are unchanged.
Production corpus round trips, both wrong-model round trips, changed-choice
controls, legacy shape/identity checks and the real CLI exercise this boundary.
<!-- ANCHOR_END: rv64gc-snapshot -->

# DEV_NOTES.md

## _(2026-10-08)_ — accepted privilege paths needed independent guards (P4-SYSTEM.12 e1a)

The pre-bind census ran all 139 historical guests with their already-declared budgets.
It found 113 exact architectural traces, four disagreements and 22 named refusals. Three
of those disagreements came from missing author rules: misa had no fixed reset/read-only
field handling; satp/SFENCE ignored TVM; SRET ignored U/TSR legality. Existing known CSR
privilege failures raised model Refusal instead of the architectural illegal instruction.
The task owns every disagreement/refusal before adoption: privilege here, vocabulary next,
and the declared cached-translation policy after that. No engine trace supplies counts.

misa now fixes RV64 plus A/C/D/F/I/M/S/U, matching the independently selected laboratory
policy. Writes ignore its read-only fields without making its RW address illegal. Known
CSR access faults and xRET/SFENCE legality deliver original bits before own side effects.
M-mode ignores S interception; legal returns retain the existing mode-stack rules.

- Validation: fixed reset/ignored writes/alias, CSR unit discipline, MRET lower modes,
  SRET U/TSR, SFENCE U/TVM, satp read/write TVM, M bypass and legal controls. Nine mutations
  fail behaviorally; parent 132506f RED. Five mode-matrix guests match 140 architectural
  steps, including two previously refused CSR-permission guests. GUEST-GEN 71/71.
- Regression: all 97 prior historical-route texts and 42 owned records exact; eight extra
  historical-route outputs are not adopted or written. Full parcel census now 118 exact,
  one cache disagreement (sv39-tlb-fence) and 20 named vocabulary refusals, all owned.
  Production unit/images/records unchanged. Cache repair is scheduled before C counts.
- Promotion: declined — permanent mode/field fixtures and nine behavioral controls retain
  this author lesson; the full-census findings and immediate schedule live in the tree.

## _(2026-10-08)_ — source length is not a guest budget (P4-SYSTEM.12 d3d2)

The independent author has an explicit parcel route, selected by --parcels --steps N.
It loads exact sized units, fetches current memory each step, and keys directives by
byte PC. The declared 1..10000 boundary budget governs source run-off, faults, pending
interrupt delivery and halted ticks; source end comments cannot shorten it. Refused
fetches count, failed translations do not, and delivery/wait boundaries never retire.
A store patch is visible to the next fetch, including a compressed unit in a word store.
Known reserved C/wider-prefix bits follow the laboratory diagnostic; unknown valid
vocabulary still refuses. All requested derivations finish before any record is written.

- Validation: hand mixed image/PC/writes/annotations, repeated spellings, source run-off,
  upper-parcel refusal, full ILEN diagnostics, code patch, pending-before-fetch, halted
  ticks, retirement and bounded-budget/refused-batch controls. Eight mutations RED;
  parent 740efda RED (API absent). GUEST-GEN 61/61; 97 prior texts and 42 refusals exact;
  all 42 owned records exact. Newly emitted documents validate against the schema.
- Five already-owned gaps repaired on the new route using budgets declared first:
  dir-runoff 3 steps/5 parcels, fault-fetch 3/5, it-prio-jump 4/7, sv39-straddle 52/104,
  sv39-perm-rwx 114/226. All 176 committed architectural observations match. Parcel
  counts are independently derived and differ from the old word-request convention;
  old records stay untouched until the C bind changes their declared extent together.
- Promotion: declined — permanent byte/budget/visibility fixtures and eight mutations
  retain this bounded authoring lesson. Next: staged corpus/count derivation, then bind.

## _(2026-10-08)_ — independent parcel fetch needs a correct walk (P4-SYSTEM.12 d3d1)

The author now fetches from memory under the selected C/ILEN=32 profile. Each required
parcel walks first, then issues exactly two bytes. Refused physical requests count;
translation failures issue none. A second-parcel fault keeps the instruction start in
EPC and the failed virtual address in tval. Wider prefixes retain all ILEN bits, while a
compressed parcel at a region/page end leaves its neighbor untouched. Unwritten in-region
bytes remain zero. Fetch does not tick time or retirement; guest boundaries own those.

Four existing walk defects were reproduced before repair: canonical sign validation
ignored bit 38, reserved high PTE bits passed, a bottom-level pointer raised author Refusal,
and M-mode data skipped MPRV/MPP translation. The corrected Svade walk also rejects reserved
non-leaf U/A/D while retaining RSW/G, and applies permissions to effective data privilege.
Odd-PC fetch fixtures exposed a fifth defect: exception/interrupt delivery assigned EPC
without clearing bit zero. M/S delivery now masks that bit while retaining bit one.

- Validation: pure hand-parcel/PTE fixtures, both canonical signs, all ten reserved high
  bits and four access kinds, non-leaf levels, MPRV/SUM/U, exact request/refusal schedules,
  translated straddles, starting EPC/failing VA, M/S/interrupt EPC, and no walk writes.
  Parent f8f213c is RED; nine mutations fail for their intended behavioral reasons.
  GUEST-GEN 52/52; complete before/after census 97/97 exact, 42 refused unchanged;
  all 42 owned records exact. No historical observations overwritten. Old guest route
  remains word-based until d3d2 explicitly integrates byte execution and declared budgets.
- Promotion: declined — the independent component, permanent fixtures and nine mutation
  controls retain the local fetch/walk lesson. Completed receipts archived verbatim.

## _(2026-10-08)_ — a wider prefix still needs ILEN diagnostic bits (P4-SYSTEM.12 d3d0)

The C evaluator stopped after its first parcel when the lowest five bits were all ones.
That identifies a wider instruction, but the nonzero illegal-instruction diagnostic must
contain min(actual length, ILEN, MXLEN) bits; ILEN=32 here. An all-ones 32-bit instruction
was reported as 0xffff, and a second-parcel fault was suppressed. Only true compressed
prefixes now finish after one parcel. Wider prefixes read two, preserving all ILEN bits
without requesting a third. The diagnosis came while deriving the independent author fetch.

- Validation: three new cases (all-ones/other prefix bits, upper access refusal, translated
  second-page fault) fail on b48201c and the short-ILEN mutation; repaired C probe 18/18.
  DEF-GEN 55/55; make check green. Production C remains unbound; old records unchanged.
- Containment: the sharder now states the governed ceiling without claiming it was
  crossed; lower targets are allowed. Header checks fail on the old wording (10/2),
  then pass on the corrected producer (12/0). Only the new shard is regenerated.
- Promotion: declined — permanent probes and mutation retain the fetch lesson; the
  sharder's header tests retain its reporting repair. Independent walker/fetch follows.

## _(2026-10-08)_ — independent C rules keep lengths and original bits (P4-SYSTEM.12 d3c)

The author lacked C decoding and five base shapes needed by compressed instructions.
A separate spec_c.py reconstructs fields and base words from the pinned chapter and its
three public SVG listings, without reading engine/assembler mappings. execute_c passes
length 2 and original parcel bits to the existing spec-side base rules; normal word callers
retain length 4. C.JALR reads old rs1 even when it links into that same register. Missing
SRAI, ADDIW, ADDW/SUBW and JALR rules use fixed-bit guards; W results truncate/sign-extend.
Reserved parcels and FS-Off traps retain the original 16-bit tval. FP loads dirty FS;
read-only stores retain the declared Precise state. The unused ADDIW locator is repaired.

- Validation: 37 expansion/effect cases, 22 limits, 79 one-hot immediate bits, 11 reserved
  parcels, 10 hints, two branch outcomes, link aliasing, memory/FP and word-overflow checks.
  One-hot cases catch a bit permutation that all-ones limits miss. Six mutations RED;
  GUEST-GEN 42/42; 42 owned records exact. All 91 older emitted texts remain exact.
  New JALR vocabulary emits six other guests; three show the already-owned source-end/fetch
  gaps. Their names and immediate d3d repair schedule live in the tree. No record overwritten.
- Promotion: declined — the independent component, permanent probe and six mutation controls
  retain this bounded lesson. Guest parcel fetching/budgets and production binding follow.

## _(2026-10-08)_ — absence is not a no-write instruction (P4-SYSTEM.12 d3b)

The scratch comparator skipped any absent row whose expected writes were empty and ignored
process status. A failed process with an empty trace could agree with an ordinary nop.
The tracked adapter requires every ordinary row and successful fresh output. A declared
interrupt or fetch-delivery gap instead needs its matching numbered trace event; unknown,
malformed, duplicate and orphan records refuse. Exact assembler bytes pass through the
tracked ELF writer's public API, removing the scratch compiler-path assumptions. The binary
is digest-checked against the dossier and the override comes from the existing conversion
owner. Two executions must produce byte-identical traces. Comparison remains declared GPR
change-observations, not unrecorded state.

- Validation: four behavioral absence mutations RED; GUEST-GEN 35/35. All 95 cached corpus
  traces audited: 79 from AGREE-claimed cells pass the new comparator (nine interrupt and
  one fetch-page-fault event gaps, no ordinary gaps); sixteen named not-matches unchanged.
  Cached process statuses are unavailable. Fresh M 4/4 verifies status and 99 observations,
  with repeat traces identical. A temporary mixed C image verifies five hand-derived pcs,
  words and writes, including a word at 2-mod-4 and a trailing parcel; repeats identical.
- Promotion: declined — the permanent adapter, offline probe and mutation controls retain
  this local lesson. Wider experimental policy remains owned by P4-SYSTEM.14.

## _(2026-10-08)_ — an author is an input worth tracking (P4-SYSTEM.12 d3a)

The latest rv64gc expectation producer lived only in target/. Promotion retains its spec-side
rules and adds repository-derived paths and non-writing checks. A 139-program census measured
42 byte-identical authored records, 49 other outputs and 48 unsupported programs. Only the
42 are the declared owned check corpus; no historical expectation is overwritten. All 91
outputs stayed exact before semantic repairs. Reserved OP/shift bits previously selected
ordinary operations; narrow fixed-bit guards now refuse them and unknown stock mnemonics
refuse by name. The permission audit found missing SUM/MXR/U checks, repaired from the pinned
supervisor chapter. The affected guest now agrees on all 169 committed observations; the
other 90 legacy output texts are unchanged.

- Validation: owned 42 exact, seven reserved refusals, direct SUM/MXR/U PTE fixtures, six
  behavioral RED mutations; GUEST-GEN 30/30. The component probe uses no instruction engine.
- Scope: source-end stopping and missing instruction-fetch translation still limit this
  author; d3d owns run-off/straddle support before C evidence. The scratch Sail comparator
  also admitted an empty failed trace as AGREE for ordinary no-write steps; d3b owns repair
  and an audit of prior traces. Both findings are durable in the task tree.
- Promotion: declined — the tracked author, owned corpus and controls retain the local lesson.

## _(2026-10-08)_ — the fixture must retain the assembler's extent (P4-SYSTEM.12 d2)

A word fixture cannot represent a compressed guest. The generator now reads sized units at
the declared entry and emits exact u8 images for rv64gc with --image-format bytes. Its runner
loads those bytes directly. Scalar replay/reduction still consume the unchanged word API;
word mode explicitly refuses short units. Regeneration commands identify each configuration
and canonical output, so checking a temporary mirror does not change the generated header.

- Validation: a hand-encoded 14-byte guest executes through the tracked runner on a temporary
  C composition: a word at 2-mod-4, a jump over an illegal parcel and the trailing halfword,
  signed writes, exact memory bytes and fetch counts. A word-only case reads two parcels.
  Padding/loader controls RED; prior generator refuses the guest. GUEST-GEN 23/23; make check
  green. Before/after hashes, extents and every expectation agree for 139 GC and 49 I guests.
- Production C remains unbound; d3 promotes and extends the expectation/Sail producers.
- Promotion: declined — the permanent compiled runner probe retains the lesson.

## _(2026-10-08)_ — an instruction image has byte lengths (P4-SYSTEM.12 d1)

The assembler's word list could not carry C. Sized units retain value, byte length, pc and
source text; the image API concatenates exact little-endian units, and the old word API
refuses short units. Compressed operands group scattered immediate pieces and use declared
field order. Their layouts own width, signedness and alignment; expansion mappings identify
FP register fields. Compact indices spell architectural registers x8–15/f8–15. Reserved
operands and operands selecting a more-specific form are refused with an explicit .half escape.

- Validation: all 37 forms against hand-encoded words, 21 operand refusals, hints, mixed byte
  labels/images; three behavioral RED mutations; GUEST-GEN 20/20, DEF-GEN 54/54, corpus 77/77.
- Producer census: rv64gc authoring and Sail adapters remain scratch tools from earlier leaves;
  d3 owns their tracked promotion and byte-identical re-derivation before C extensions.
- README's stale no-implementation disclaimer traced to planning import 724e422 and corrected
  to experimental implementations with no conformance/accepted-profile claim.
- Promotion: declined — the permanent probe and its controls retain the evidence.

## _(2026-10-08)_ — execute the mappings before replacing the fields (P4-SYSTEM.12 c2)

C expansions reuse ordinary instruction rules, but those rules read base operand names.
The evaluator maps all bindings over the original compressed fields, preserves each value
and width, then replaces the operand set. Otherwise a sign bit can disappear or a mapping
can accidentally read an already-replaced field. Exact parcel requests let the processor
decide length before touching the next page. Restart state belongs to the instruction start;
a fault value belongs to the failing parcel. The unbound production table retains its fetch
shape until the bind. Its generator now emits optional expansion metadata even when absent.

- Validation: 15 permanent engine probes green, all 15 RED on b71bc1b; two behavioral mutation
  controls; DEF-GEN 54/54; strict workspace checks green. C binding/reference evidence next.
- Promotion: declined — the tracked probe and controls retain the evidence.

## _(2026-10-08)_ — a masked word is still a four-byte request (P4-SYSTEM.12 c1)

The helper named fetch16 requested four bytes and masked its reply. A two-byte instruction
at the end of a region still faulted. FetchParcel pins its two-byte extent in the boundary
types, and providers, counters and injection spans honor it. C-enabled execution will use
exact parcels; preserving one request per 32-bit instruction would require a partial-success
protocol without a measured need. The production table remains unbound in this slice.

- Validation: two-byte region success, word refusal, odd/outside faults, immediate visibility,
  injection extent; make check green (150 core / 17 DSP / 193 verify).
- Promotion: declined — the boundary extent tests retain this local finding.

## _(2026-10-07)_ — recover the language slice, then prove the emitted table (P4-SYSTEM.12 slice b)

Five uncommitted files survived the crash while the resume pointer still said no work was in
flight. The task-tree frontier and design brief identified their owner unambiguously: C's
language slice. The surviving semantics declarations checked, but the generator loaded and
dropped their expansion metadata. Completion emits the bindings, reserved predicates, lengths
and specificity order on a temporary C composition; the real unit's C slot stays unbound.

The probe uses hand-written spec-side mappings and immediate limits, then compiles the emitted
Rust to check those mappings, base effects, C.JALR's pc+2 rule and the decoder. It caught its own
incorrect assumption that every reserved predicate concerned a zero immediate (C.ADDIW instead
reserves rd=x0). The existing citation reader refused an expansion-only file because it walked
only ordinary rules; both forms now share the locator check. C.J's longer scatter list also
made the generator's inline-array assumption fail rustfmt; the established wrapping threshold
fixes it without changing the existing tables.

- **Validation:** 37 forms, 104 spec-side checks; compiled decoder 8/8; DEF-GEN 51/51;
  semantics 46/46; citations 0 findings; workspace, doctrines and all books green. A wrong compact-register
  offset and reversed specificity order both fail; an unbound base operand refuses generation.
- Promotion: declined — local reader/emitter adaptations; the permanent probe and controls
  retain their evidence. The director requested the next handoff checkpoint, so stop before (c).

## _(2026-10-06)_ — the doc had the right algebra; the code had the field width (P4-SYSTEM.12 slice a2)

`exec.rs`'s module doc says an immediate carries its composed width — 21 for JAL's `jimm20`. The
code pushed the field's width, 20, so a JAL's offset was sign-extended from bit 19: a jump of
+512 KiB went backward, one past −512 KiB went forward, in both engines since P1. `bimm12` had
been special-cased correctly, `jimm20` never was, and no corpus program jumps that far — so
every gate stayed green. It surfaced only because C's `c.j` offset has the same shape (imm[11:1]
in an 11-bit field) and binding it meant reading the extractor closely.

- **Validation:** the boundary tests RED on both engines before the fix, GREEN after; both
  corpora unchanged; the rv64i release decision amended.
- Promotion: declined — the boundary test is the record; slice (b)'s expansion vectors make
  "every immediate at its extremes" mechanical for C.

## _(2026-10-06)_ — a control that pinned today's numbers, and a tool that would have read mul as sub (P4-SYSTEM.11 slice b)

M bound cleanly — 139/139, the 135 pre-slice guests byte-identical, the four new ones RED on the
parent — but three things surfaced on the way. The gate report's own controls, written one leaf
earlier, asserted rv64gc's live counts ("100 checks, 14 realized"); the first legitimate growth of
the contract broke them, exactly the hard-coded-unit-fact defect the generator was built to
remove. They now assert deltas from a baseline taken at run time, plus one independent recount.
The authoring tool's OP branch read any funct3=0 word with a nonzero funct7 as `sub`, so `mul`
would have been mis-derived silently; the M branch decodes first. And four expected results
landed in registers already holding 0 — no change observed, so an engine that wrote nothing would
have passed; sentinels fixed them (the `.8` lesson, again).

- **Validation:** identity 135/0 + 4 RED; EVD-05 digests pinned before the engine had M; the
  generator's controls 17/17 with two mutations caught; the census leg 163 == 163.
- Promotion: PROMOTED — docs/knowledge/self-test-arms-that-never-ran.md extended (a control pinned to the live data).

## _(2026-10-06)_ — a contract that could only grow, and a gate whose own control hid its finding (P4-SYSTEM.9)

The environment contract's "version" was a string on every record that nothing checked, and seven
leaves had added records under v0. `.9` made a version a document — its members listed, frozen by
content hashes — so "versioned, not edited in place" is now something a gate can refuse. Two
things went wrong on the way and both were caught by gates. The first v1 ids collided with rv64i's
(`OB-ENV-VIRTUAL-TIME` exists there with the same check ids), and the gate report — which counts a
check as implemented when its id appears anywhere in code — credited rv64i with rv64gc's new
registry; GATE-REPORT noticed its own output change. The second was in the new gate itself: its
GREEN control copied the live files, so an edited frozen record made the self-test fail and the
gate said "does not discriminate" rather than naming the edit. Judging first fixed it.

- **Validation:** CONTRACT-FREEZE 7/7 controls; an edited frozen v1 record named and refused
  (rc=1); the check registry 14/14; RECORD-SCHEMA ok; the corpus 135/135.
- Promotion: PROMOTED — docs/knowledge/self-test-arms-that-never-ran.md extended (the masking GREEN control).

## _(2026-10-06)_ — the instruction that wrote its result and then trapped, and a reference that agreed for the wrong reason (P4-SYSTEM.8 slice a)

The engine writes straight through to state, so "completes or faults as a unit" holds only
where every fault point precedes every commit in a rule's tree. The zicsr rules read the
old value into rd and THEN attempted the write: a write to a read-only CSR committed rd and
trapped. The fix is the spec's own word for CSRRW — atomic: one `csr-rw` operation judges
the read and the write before the old value reaches rd. The authoring tool had never
derived the case at all — it refused read-only writes as "fix the guest" — which is why no
guest covered it. The second engine taught the other half: Sail's matched configuration has
no `cycle` (Zicntr is off behind the CLINT wall), so it trapped on the probe for an
unrelated reason; a legal read of the same CSR beside the refused write exposed that, and
`mhartid` gave the clean comparison.

- **Validation:** RED first (the new guest failed at step 9 on the old engine), then 127/127;
  identity 125/0 with both new guests RED on the parent; Sail AGREE on `mm-csr-ro-write`, the
  counters guest the named Zicntr-absent cell.
- Promotion: PROMOTED — docs/knowledge/an-oracle-can-share-the-convention-it-judges.md extended (the mirror case).

## _(2026-10-06)_ — the patch that passed without itself, and a deviation that was the oracle's (P4-SYSTEM.7 slice d3)

The plan, recorded at (d1), was to patch the qualification record's deviation (ii) in the new
`fp::convert`: "an sNaN through a format conversion gets no NV flag". The spec-side vectors
passed — and passed again with the patch bypassed. A patch whose absence the tests cannot see
is either untested or patching nothing, so the backend was probed directly: `convert_r` raises
INVALID_OP for a signaling NaN in both directions. Slice (a)'s own run file then said the
rest: all 24 recorded disagreements are `apfloat NV, mpfr -`. MPFR has a single NaN kind and
cannot express a signaling one; the record had booked the oracle's silence against the
backend. The correction went to the record (a second dated amendment), not just to the code —
and to three places this session had propagated the error, including a (c6) "fix" that raised
a correct count of two deviations to an incorrect three on the record's word.

- **Validation:** 230/230 vectors (54 conversions); FP-VECTORS hardware agree 2131 (the tie
  mutation caught on the conversion leg); fp.rs over the 63,752-case corpus: 0 vs the
  exact-rational reference, 24 vs MPFR — all signaling NaNs, all the oracle's.
- Promotion: PROMOTED — docs/knowledge/an-oracle-can-share-the-convention-it-judges.md extended (the starkest form: an oracle that cannot represent the case).

## _(2026-10-06)_ — the bind that was already proven, a green gate that never saw the new files, and a number corrected in the slice that wrote it (P4-SYSTEM.7 slice c6)

The bind itself was uneventful by design: every leg had run green in the staging worktree, so
landing it was a byte-identical copy (38/38, `cmp`-verified) followed by the same checks in
the tracked tree — and the one command the worktree could not run (the reference verify reads
the untracked fetched area) ran there: 118 == 118. The interesting part was the stale-fact
sweep. `fp.rs`'s module doc, written in slice (c4) part 2, quoted slice (a)'s 362 overflow
cases — in the same commit whose decision-record amendment re-measured them to 290. The
amendment updated the record; the prose that quoted the record's old number was a second
copy nobody re-read. The schema's FP contract (slice c3) still counted two backend
deviations, one fewer than the amendment found. Neither is gated: the claim-verification
standard's constant sweep is the unmechanized rule that would have caught both.

"Already proven" had a hole. `make gate` was green in the worktree and again in the main tree,
and the commit's own pre-commit run refused `f-sgnj.expected.sexp`: an empty derivation. The
authored comment began `|sNaN|:` and `|` is the directive's separator; the tool partitioned it
instead of refusing. The two green runs never looked — DOSSIER-SCHEMA enumerates
`git ls-files`, and the 22 new corpus files were untracked until `git add`. A tracked-only
sweep is right for a commit gate and blind to everything not yet staged; stage (or
`git add -N`) new files before the gate run you intend to cite.

- **Validation:** 114/114 (103 byte-identical); 30/30 F forms; 118 == 118; coverage
  118/118; the matrix 28 cells; the fixed tool refuses the old line; DOSSIER-SCHEMA ok with
  the guests staged; `make check` + `make gate` green.
- Promotion: PROMOTED — docs/knowledge/zero-hits-absence-or-blindness.md extended (the denominator rule, one level up) + INDEX.

## _(2026-10-06)_ — a reference stops where its first consumer stopped (P4-SYSTEM.7 slice c5)

`scripts/specfp.py` was tracked at slice (c4) as the FP authority, and its `fma` computed
`(a×b)+c` — enough for `fp.rs`'s vectors, which exercise the backend's one fused primitive.
The corpus needs all four fused forms as the chapter writes them, and the obvious shortcut —
flip a register's sign bit and call FMADD — is exactly how the MODEL does it, so a reference
built that way would check the model against itself. The reference now forms the signed terms
exactly; the sign-flip construction became the cross-check instead (they must agree, and do,
on 464,000 cases; each of two planted mutations is caught). The staged corpus's other lesson
was procedural: the derivation tool imports `scripts/` relative to its own file, so a copy
outside the worktree read the main tree's dossier reader against the worktree's edited
profile — it refused loudly (`undeclared field 'f_single'`), and the re-derivation ran from a
copy placed inside the worktree.

- **Validation:** 464,000/0 (RED 490 and 153,438); 22/22 re-derived byte-identical; 114/114
  on the scratch engine (RED on dropped accrual); identity 103/0 + 11 RED; FP-VECTORS 176.
- Promotion: declined (recorded in the P4-SYSTEM leaf — the signed-term construction is `fma`'s docstring; the independent-construction lesson is the c4 oracle card's).

## _(2026-10-06)_ — the FP model layer, and the oracle that agreed because it shared the convention (P4-SYSTEM.7 slice c4)

`fp.rs` is the RISC-V policy over rustc_apfloat: canonical NaN, NaN-boxing, the rounding-mode
resolution, min/max/compares/class in bits, NaN→int's maximum, the FMA ∞×0 rule, and a
square root of its own (exact integer √ with a sticky remainder — the backend has none). Its
overflow and underflow come from ONE exactly-unbounded value: the same operation in a
backend format of equal precision and a 15-bit exponent, so "rounded as though the exponent
range were unbounded" (IEEE §7.4/§7.5) is computed, not approximated.

Its unit vectors came from a new spec-side reference in exact rationals. Three of 176 failed
on first run — at 2^-126·(1−2^-24), RNE/RUP/RMM, the backend raised no UF — and the cause
was not in `fp.rs`. Slice (a)'s MPFR generator judged UF on the DELIVERED result (the
backend's own convention) and OF on the EXACT magnitude (IEEE judges the unbounded ROUNDED
result): the oracle had agreed with the backend by sharing its rules. Corrected, 72 of the
recorded overflow "deviations" were the oracle's own false positives, and a third backend
deviation (underflow) appeared. SoftFloat's RISC-V specialization, read in source, takes the
IEEE side on both. The decision record carries a dated amendment; the generator and
reference are tracked (`scripts/specfp.py`, `scripts/gen_fp_vectors.py`) and gated by the new
FP-VECTORS doctrine, which also re-checks the reference against the host's hardware IEEE on
directed ties every run (a half-up mutation had survived 1,313 random cases).

- **Validation:** 176/176 spec-side vectors; `fp.rs` vs the corrected MPFR oracle 0/51,840,
  vs the exact-rational reference 0/63,480 (RED: one corrupted line caught by both); FP-VECTORS
  6/6 with the reference-mutation arm; `make check` + `make gate` green.
- Promotion: PROMOTED — docs/knowledge/an-oracle-can-share-the-convention-it-judges.md + INDEX.

## _(2026-10-06)_ — "the cargo cache stays on-volume" was true of one command (P4-SYSTEM.7 slice c4 part 1)

Slice (a) fetched `rustc_apfloat` with `CARGO_HOME=.app-data/cargo-home` and recorded the
cache as on-volume. It was — for that command. Nothing made it true for the next one: no
`.cargo/config.toml`, no `CARGO_HOME` in the Makefile, none in the shell. The workspace had
never had a registry dependency before, so every later `cargo` run silently resolved the
crate through the shared `~/.cargo` (`cargo metadata` named
`~/.cargo/registry/src/…/rustc_apfloat-…/Cargo.toml`). A locality claim about a store is a
claim about EVERY path that reads it; the acquisition path is one of them. The fix is the one
mechanism every cargo invocation in the tree obeys — `.cargo/config.toml` source replacement
to an untracked on-volume directory populated by `make vendor` — and its RED is loud: with the
store absent, cargo refuses to build rather than falling back.

- **Validation:** cargo metadata's path before/after; the shared cache's stat snapshot
  unchanged by a full build; the missing-store failure; `make check` + `make gate` green.
- Promotion: PROMOTED — docs/knowledge/a-locality-claim-covers-every-reader-of-the-store.md + INDEX.

## _(2026-10-06)_ — a move census that reuses the mover's filter cannot see what the filter drops (LIVE-CONTAINMENT.3)

Partitioning TOOLBOX.md's 76-row table, the mover selected rows by `startswith("| \`")`
— and the census that "proved" the move used the same predicate, so it reported 75 of
75 moved, exactly once. One row starts `| any project check's \`--self-test\` |`: no
backtick in its first cell, invisible to both. A second census selecting rows by
POSITION (every table line after the header and separator) found 76 and named the
missing one; the move was re-run from HEAD with the positional selector. The doctrine
partition had the same latent shape (it happened to have no such row). REGISTRY-MIRROR
now also judges the doctrine families' union, so a long-form row lost in a future move
is a gate failure, not an accident of census design.

- **Validation:** 35 + 76 rows each exactly once (positional census); REGISTRY-MIRROR
  13/13 and RED on a removed row; `make gate` green.
- Promotion: declined — the existing card a-survey-that-found-things-can-still-have-missed-things.md
  states the lesson; this entry records its instance.

## _(2026-10-06)_ — a registered pressure control nothing enforces is a wish (LIVE-CONTAINMENT.1)

`docs/TASK_TREE.md`'s registry row has said "one row per active tree; completed trees
leave the index" since SEMULITH-TREES.4 — and the index carried 22 completed trees (of
31) at 8,172 / 8,192 B. Nothing had ever applied the control, and the reason was
mechanical: FRONTIER-SYNC's CLOSURE rule demanded an index row for EVERY tree file, so
obeying the registry would have failed the gate. The two rules contradicted each other
and the enforced one won by default. Now the completed rows live verbatim in
`docs/TASK_TREE_CLOSED.md` (registered, bounded), and FRONTIER-SYNC gates both files:
one row per tree by its status, a completed tree left in the index refused (22 such
findings against the real pre-move index), the leaf-count checks running on the
register too. The book includes both anchors live.

- **Validation:** FRONTIER-SYNC 20/20 (4 new arms); RED 22× on the real pre-move index;
  the move census exact; README-ROUTING-CLOSURE, TREE-CLAIMS, DERIVED-COUNTS green;
  `make book` rc=0; `make gate` green.
- Promotion: declined (mechanized — FRONTIER-SYNC refuses the state this lesson describes).

## _(2026-10-06)_ — a locator that resolves can still name the wrong section (CITATION-ACCURACY.1)

`P4-SYSTEM.7` slice (c3) part 1 found the rv64gc FP-CSR content cited `RVI-F §20.1.1`
(the F register state — real, and wrong: the fcsr is §20.1.2), with every gate green.
The measurement of WHY nothing saw it: `check_citations.py` globs the semantics files
only and asks whether the cited section EXISTS — a wrong-but-real locator passes it by
construction, and no gate read a quote at all. The new tool reads every string atom of
every tracked `.sexp`, attributes a quoted phrase only when the attribution is decidable
(R1 adjacency, R2 a source's leading locator, R3 an expectation step's source, R4 a
single-locator string — 24 of 108 quotes today; the rest counted, never guessed at), and
checks the phrase against the cited section in order, ellipses honoured. Two renderings
of the pinned HTML had to be measured before matching was honest: code literals arrive
quoted (`('pc'+4)`) and dash ranges carry zero-width spaces (`7—\u200b5`). Run against
the real pre-fix files it reports six misses and, for each, the section that does hold
the sentence (§20.1.2) — the refusal names the cure.

- **Validation:** the doctrine's 14 controls pass on synthetic pages; a mutation (the
  matcher forced to always-match) turns 6 RED arms red; HEAD judges 24 quotes, 0
  findings; the pre-fix corpus 6 misses; DERIVED-COUNTS 431 → 445 arms, 34 → 35
  doctrines; `make gate` green.
- Promotion: declined — the lesson is mechanized: the CITATION-QUOTES row in
  DOCTRINE_ENFORCEMENT.md is its retrievable statement, and the gate enforces it.

## _(2026-10-06)_ — frm held what the spec writes, not what the laboratory preferred (P4-SYSTEM.7 slice c1)

Slice (b) declared `frm` WARL one-of 0..4 — an illegal write retaining the old
value — and parked Sail's "stores anything" as a named difference for slice (e).
Re-reading the pinned F chapter for slice (c)'s dyn-rm resolution exposed it: FSRM
writes "the three least-significant bits of integer register rs1 into frm" (no
legalization), and the rounding-mode table names 101–111 *dynamic reserved
rounding modes*, a state frm must be able to HOLD for the sentence to mean
anything. Three artifacts had encoded the one misreading — the declaration, the
privilege unit tests, the spec-side authoring tool — so every check agreed with
every other. The fix went in at the declaration (`(legalize (any))`, the FSRM
sentence quoted in the statement); the generated state mirror and the definition
manifest regenerated; the tests now assert 7 lands from a fcsr slice and 6 from a
frm write of 0b1110. `fp-fcsr-view` was re-derived spec-side FIRST (the tool
corrected) and run against the unfixed engine: step 15 read `0x45` where the
specification gives `0xE5` — RED for the right reason — then green on the fix.
The guest's step 13 now also writes bit 8, so the legality cell it sits in is
fcsr's own "shall ignore writes to these bits / supply a zero value" sentence, not
a retention the spec never granted.

Also recorded here: the pinned revision WEAKENED the reserved-rm rule — "The
behavior of floating-point instructions that depend on rounding mode when executed
with a reserved rounding mode is reserved" — while calling the ratified
illegal-instruction mandate "still valid behavior". The laboratory takes
illegal-instruction for static 101/110 and dynamic 101–111 (Sail's
`Fcsr_RM_Illegal`, `fext_insts.sail:51-63`); slice (c3) states it in the
operator's contract. Two incidental defects of the authoring tool were fixed in
passing: its header template still named "P4-SYSTEM.5 slice b, the interrupts
corpus" (both FP guests carried that false provenance line — corrected, values
byte-unchanged in `fp-fs-off`), and it wrote directives into S-expression strings
unescaped, so a `"` in a directive would have silently broken the file — it now
refuses by name (fired RED once). And the book's P4 chapter carried a duplicated
`## Gate CPU-SYSTEM` heading (slice b) and "underway" headings over the closed
`.3`/`.4` sections — fixed.

- **Validation:** `cargo test -p semulith-core --lib` 134/134; `cargo test -p
  semulith-verify run_rv64gc` 4/4 (103/103) — and RED against the unfixed
  legalization (fp-fcsr-view step 15); `gen_state.py --check` byte-exact after the
  restore; INTERACTION-MATRIX ok; `make check` + `make gate` green.
- Promotion: PROMOTED — docs/knowledge/a-legalization-rule-is-a-claim-the-spec-must-grant.md
  + INDEX (the map regenerated).

## _(2026-10-06)_ — the identity proof's RED control is what makes it a proof (P4-SYSTEM.7 slice b)

Slice (b)'s byte-level identity proof (101 pre-slice guests, both CLIs — the
parent worktree's build vs the post-slice build) came back "101 byte-identical,
0 diverge" on its first run. It was also worthless: the harness had passed
`--profile NAME` where the CLI wants `--profile=NAME`, so every one of the 202
runs had failed with the SAME usage-error text — and identical failure output
compares byte-identical. What caught it was the control the proof carried by
design: the two NEW guests (fp-fs-off, fp-fcsr-view) MUST diverge on the parent
engine — the FS gate and the fcsr composition did not exist there — and they
"didn't". A comparison harness whose failure mode is identical on both sides
reports identity on garbage; the must-diverge control is the only arm that can
see it (the a-shorter-trace lesson's sibling: prefix agreement was the green
there, identical errors here). After the fix: 101 byte-identical for real
(5,491 trace lines), both new guests diverging on the parent as required.

Also measured this slice, for the record: Sail puts the FS gate on the DECODE
clause (`encdec … when currentlyEnabled(Ext_F)` — a dynamic state gate at
legality, never a static encoding property), which settled where ours lives
(the permission model for the FP CSRs now; `fp_enabled()` for the binds' arms);
and Sail's `write_fcsr` marks the context Dirty on every FP-CSR write
(fdext_regs.sail:455), the discipline our csr_write now follows.

- **Validation:** the fixed harness re-ran green with the control RED where it
  must be; `cargo test -p semulith-verify run_rv64gc` 4/4 (103/103); STATE-GEN
  29/29 with the new RED arm; `make check` rc=0, `make gate` green
  (DERIVED-COUNTS 430→431 re-derived).
- Promotion: PROMOTED — the must-diverge-control lesson is retrievable
  (docs/knowledge/an-identity-proof-needs-a-must-diverge-control.md + INDEX;
  the map regenerated). The Sail placements are recorded in the leaf's own
  checklist and need no card.

## _(2026-10-06)_ — the FP qualification: two candidates, three lineages, and MPFR is a thing you measure too (P4-SYSTEM.7 slice a)

The `.7` brief's slice (a) measured:

- **The arithmetic core is the easy part; the policy surface is where backends
  differ.** rustc_apfloat matches MPFR on every add/sub/mul/div/fma value across
  all five rounding modes and both widths — 63,752 cases, zero core
  disagreements. Every disagreement was a boundary the crate explicitly does not
  own: LLVM signals opOverflow only for infinite results (IEEE wants the
  magnitude rule — 362 measured cases), format conversion of an sNaN carries no
  NV (24), NaN→int converts to 0 (RISC-V wants max + NV — 340), fmin/fmax's
  signed-zero pair and both-NaN payload are LLVM's conventions (240), and
  format-conversion payloads scale per LLVM where RISC-V canonicalizes (32). A
  backend qualification that stops at "the adds agree" would have missed the
  whole story; the per-op disagreement tables BY NAME are the deliverable.
- **MPFR needed four corrections of its own.** The DON'T-USE MPFR_RNDNA (RNDA
  behavior for the arithmetic ops — RMM rides mpfr_round_nearest_away); the OF/UF
  flags are exponent-range-shaped (computed spec-side against an exact shadow —
  and the shadow needs 2100 bits, not 300: f64max + 1 spans 1024 bits); NaN
  results canonicalize (payloads dropped); the NAN flag is "result is NaN", never
  IEEE's NV. A reference library's flags are ITS semantics — the generator that
  trusts them writes a wrong spec.
- **softfloat's failure is capability, not quality.** Its arithmetic core is
  MPFR-exact where it exists (including the sqrt APFloat lacks), 3-5× cheaper
  per op; it simply has no rounding modes, no flags, no FMA, no 64-bit
  conversions, no min/max — five of §6's explicit requirements. The one family
  it differs on (it clears the propagated NaN's sign; IEEE-unspecified) is
  recorded as its convention, moot for the verdict. The lesson reached the
  knowledge layer as its own card (the candidate-landscape census is a lead,
  the crate's own documents are the measurement surface) — PROMOTED, the kind
  the layer exists for.

promotion: PROMOTED — `docs/knowledge/a-candidate-landscape-census-entry-is-a-lead.md`
(the landscape-census lesson; the MPFR-measurement half lives in the decision record's
own text, which is the durable home for backend-specific facts).
## _(2026-10-05)_ — a designed AGREE is still a measurement, and a clause can live one hop away (P4-SYSTEM.6 slice c)

Execution of the `.6` brief's checkpoint (c) measured:

- **"Sail lands identically" is a hypothesis until the trace agrees.** Decision
  2 promised AGREE by design — Sail's FENCEI is "a nop for the memory model" —
  and the experiment's job was to measure it, not assume it. The measurement
  has two legs before any guest runs: the override validates unchanged
  (Zifencei already true), and Sail's OWN source carries the shall-ignore
  sentence as a comment while its encdec binds the fields as variables — so
  0x0011118F decodes as FENCEI on both sides. Then the traces: 6 AGREE of 6,
  zero non-AGREE cells to name. A designed outcome with zero divergences is
  the easiest experiment to wave through, and the one that most needs the
  numbers written down.
- **A referenced clause is still load-bearing — and its location is not the
  reference.** The brief's pre-condition 2 said the fetch-cache candidate's
  why "says 'without Zifencei'" — the clause actually lives in rv64i's
  verbatim text, which rv64gc's candidate only references. The re-answer would
  have been the same either way, but the imprecision is recorded because the
  census's whole point is that these sentences are checked, not remembered
  (promotion: declined — the re-answered candidate is in the descriptor and
  STATE-GEN re-derives it on every change).
- **The staleness half of an acceptance can be honest as a latitude.** The
  goal asks "when stale state MAY persist" — and the spec's own implicit-reads
  sentence lets a valid implementation cache every fetchable byte forever. The
  rejected option was modelling a caching hart to make staleness executable:
  it would contradict the unit's own `present false` census to demonstrate a
  machine this unit is not. The latitude is pinned by declaration (the
  sentence is located, the choice is named, the census is re-answered), which
  is the whole truth of the position — a fixture for it would have been a lie.

promotion: declined (the durability is the machinery — the six AGREEs re-run
against the materialized override; the acceptance pair is armed by make check).
## _(2026-10-05)_ — the mirror's byte-identity is the point, and a bind can be invisible in its own trace (P4-SYSTEM.6 slice b)

Execution of the `.6` brief's checkpoint (b) measured:

- **The mirror holds .s byte-identical ALWAYS — and that is the discipline, not
  an obstacle.** My first draft restated four .s headers to the bound state, and
  the governor measured every one as MIRROR DRIFT: the base mirror's rule is
  that rv64gc's .s files are byte-identical to rv64i's owners with NO exception
  list, while an .expected.sexp may differ only for a RECORDED re-derivation.
  The `.2` slice-(g) shape was already the answer: the rv64gc-specific reading
  lives in the expectation comment block, never in the mirrored source. The
  decision-3 corrections (dir-selfmod-fence's data fence is not the fetch
  synchronization; fault-selfmod's stale "without Zifencei") landed exactly
  there, with both names joining MIRROR_REDERIVED and the reason recorded
  beside the slice-(f)/(g) reasons (promotion: declined — the durability is the
  machinery: the governor names drift on every gate run).
- **A bind can be invisible in its own trace.** min-fencei's demo trace is
  byte-identical pre- and post-bind: the pre-bind ReservedDecode delivery wrote
  no register and vectored to mtvec=0, so the recorded step (pc, mode, writes)
  is the same tuple as the post-bind retiring nop. The semantic change (a
  trap-conversion vs a retirement) is real and shows in the expectations; the
  trace just has no slot for it. it-fencei carries the visible half: the
  continuation marker commits now (x2 ← 7), exactly as on both references.
- **Memory-backed fetch is a derivation-level discipline too.** The new
  fencei-selfmod guest needs the spec-side model to re-read the patched word —
  the store's effect lands in the program map with the patch named in the insn
  text (the `.2` comment convention, tooled at last). The engine always re-read
  (D-CODE-VISIBILITY); the derivation tool simply had to catch up — a guest
  whose patch the model ignores would derive the WRONG patched step silently.

promotion: declined (the durability is the machinery — the mirror governor and
the 101-guest corpus re-run every one of these).

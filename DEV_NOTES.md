# DEV_NOTES.md

## _(2026-09-30)_ — the packet and the delayed writeback (DSP-REVIEW.4)

The tree named this leaf "the single most likely place the scalar abstraction breaks"
and the measurement agreed — twice. The packet: ≤8 instructions, all operands read at E1
simultaneously (Table 3-3's read cycles are all "i"), one functional unit each — so two
stores to one address have a joint outcome that instruction-stepping miscomputes. The
delayed writeback: load results land at i+4, interlocks are eliminated BY DESIGN ("no
stall is introduced if the register being read has data placed by a load"), and the
manual's own §5.7.1 worked example shows an interrupt inside the window producing
incorrect results — the exact delayed-effect shape .2's SAT measurement fed in. The
third unmeasured-number slip of the day happened in this leaf's checklist (101 measured
after 21 was composed) — the practiced rule is now "paste real output, never compose",
and it is written into the leaf's own checklist block where the next author sees it.

Lesson: `promotion: declined` (the breaks are the artifact's own section).

## _(2026-09-30)_ — the synthetic boundary fixture (DSP-REVIEW.6)

The design question was what "through the real API" means, and the answer was measured:
gen_state.py's refusal list is the boundary's own documentation (the unknown dossier
name, the XLEN owner split, the second profile id, the nonstandard width — each refused
by name), and the schema layer refuses the packet/space/delayed-effect shapes the same
way. The fixture pins the REFUSALS — green while the boundary stands, RED the day a
shape becomes supported (the fixture measures the boundary moving, which is its whole
purpose). The packet descriptor was reduced until its ONLY refusal is `packet` itself
(the kind/requires/source fields satisfied first, so the pin measures the construct,
not descriptor hygiene). The vendor gaps filed with .3 were answered same-day (the
2026-09-30 DSP batch) and their channel contract now lives in
`docs/knowledge/the-chipdoc-channel.md` (adopted per Policy 12: the content copied in,
never depended on externally).

Lesson: `promotion: declined` (recorded in the leaf; the channel contract is the
knowledge card's).

## _(2026-09-30)_ — the loop/restart survey (DSP-REVIEW.5)

The measured content: SPLOOP's full state census (buffer + hidden LBC ×2 + ILC + RILC +
SPLX), the drain-vs-no-drain asymmetry between interrupts and exceptions (§7.13.1 vs
§7.13.3 — the leaf's load-bearing fact: a restart model treating them alike is wrong by
construction), the not-interruptible formula for short loops, and restart as
re-execution under modified rules. The SEM-04 framing (the acceptance): per-instruction
completion holds across interrupts; the persistent loop state is exactly ILC + refill;
the .4 break stands beside it. MFENCE measured C66x-only (0/34/0 hits); its violated
restrictions are undefined-by-omission. DMA ordering is out of ALL three CPU manuals by
their own deferral — the catalog's answer must cite the programmer's guide; recorded so.

Lesson: `promotion: declined` (recorded in the leaf).

## _(2026-09-30)_ — addressing and address spaces; the vendor-diversity filing (DSP-REVIEW.3 + DR-0087)

Q6 measured first per the acceptance: bytes on both sides, one numbering — the lab's
units answer holds for these targets. The interesting findings are the seams: AMR (a
control register carrying addressing mode — the lab has no CSR surface), the .D units
as the only address generators with cross-file routing, two L1 spaces against the lab's
identical fetch/data maps, circular addressing on a NAMED register subset. Measured
absences done right (named searches): no bit-reversed ADDRESSING (BITR is a data op), no
strided modes, no word-addressed space. The vendor sweep measured the corpus, not memory:
adi/dsp/sharc exists EMPTY, no Motorola/NXP DSP line exists — two gaps filed through the
(now two-way) channel; the C55x want dissolved (already catalogued — my first edit
duplicated its id and the materials gate refused by name; the duplicate was removed, the
gate's refusal is the recorded evidence the census exists). Four more manual defects
recorded unresolved, incl. the AMR table's row-shift and the cross-chapter alignment
precondition.

Lesson: `promotion: declined` (recorded in the leaf).

## _(2026-09-30)_ — the rounding/saturation survey (DSP-REVIEW.2)

The manuals write the ordering as inline arithmetic, so the leaf records it that way:
multiply → accumulate → round-add → shift/saturate → narrow, per instruction, quoted.
Two measurements deserve their names: the flag side effect is per-instruction DATA
(SADD2's own entry says it does NOT set the SAT bit — a model that derives "saturated ⇒
flag set" is wrong by construction), and SAT's update lands one cycle after the result
(the delayed-effect shape the tree predicted). The seven manual defects are recorded with
quotes and NOT resolved (upstream facts; our intuition is not their authority) — the
DOTPNRSU2 32-vs-33-bit intermediate split is a core-version profile-pinning obligation.
In-flight authoring slip owned: a fabricated filename went into a checklist's recorded
output block in the first draft; measured, corrected to the real pasted output, and noted
in the block itself.

Lesson: `promotion: declined` (recorded in the leaf).

## _(2026-09-30)_ — the DSP widths survey (DSP-REVIEW.1)

Method matters more than findings here: pdftotext extraction of the three catalogued TI
C6000 manuals, every fact quoted with page+section, every ABSENCE measured by named
searches (`guard` = 1 boilerplate hit; `Q15` = 0; `Q31` = exactly 1). Findings: no
accumulator/guard machinery anywhere in the family (accumulation is explicit ADDs — a
measured non-finding that stops anyone adding accumulator state speculatively); the
40-bit long/64-bit pair/128-bit quad width ladder (quads C66x-only) with the odd:even
zero-fill rule; scaling carried by instruction MNEMONICS (the S-family <<1+saturate,
MPYIHR's round), not mode bits — the opcode-map `s` bit is the A/B side-select, a trap
measured and recorded in the artifact. The classification seed for .7: register grouping
with a width+fill rule. Also fixed in passing: the tree's G1 blocker (long resolved) and
LIVE_STATUS's P2 row (stale at 8/9 from an aborted multi-file edit — its MEMORY half had
died on an assertion before writing, and only some of the files went in; measured now).

Lesson: `promotion: declined` (the method is the leaf's acceptance; the trap lives in the
artifact where the next reader meets it).

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

## _(2026-09-30)_ — the CPU-LAB report and the experimental release (P2-SCALAR.9, slice c; the tree closes)

The report's probes are all static over tracked artifacts (the generator's byte-stability
rule): the obligations census reuses G0's exact probe (concrete check ids vs tracked
executables — measured 0/72 today), the requirements census is read from the catalogue
(28 planned + 1 partial — so G-OBLIGATIONS reads open on the record's own terms), the
matrix/campaign/portability/replay axes read their tracked records (interactions.sexp,
act4.sexp, portability.sexp, the suite census). The verdict rule has no path to `passed`
over an open axis (EVD-08). The named decision: experimental release of the versioned
artifact (dossier digest in the report), the closing conditions enumerated. Defect owned:
the G0 limitation "No CPU model exists" was P0 prose, stale since the interpreter landed
— fixed in the generator, and the repair is regenerable (GATE-REPORT). MEMORY's
active-trees count sat at 6/9 across the .7/.8 commits (edited around, not in) — cosmetic
resume-pointer drift, caught and corrected at closure; TREE-CLAIMS would have caught a
contradiction at the tree's close, which is exactly what the line now does cleanly.

Lesson: `promotion: declined` (the axes' state lives in the generated report; the
decision record carries the reasoning).

## _(2026-09-30)_ — the Rosetta proof: the x86-64 leg green under translation (P2-SCALAR.9, slice b)

The leg's two halves were measured separately: the fixtures cross-compiled for
x86_64-apple-darwin and ran green under Rosetta (cargo test --target, rc=0), and the
agreement contract — the digest manifest — matched the aarch64 recording byte-for-byte
(0670a01b…5bb52; the demo --json fingerprints are architecture-independent by
construction: addresses and values, no host bytes). The instrument's verdict strings
gained annotations ("green (Rosetta translation; …)"), so the ladder's normalization
learned prefix matching — a one-line fix with the self-test re-run. The record's verdict
moved incomplete → passed with the nuance preserved: the bare-metal leg is the CI
matrix's ubuntu job, landing at the next approved push; Rosetta expires fall 2027 and is
the bridge only. Also owned: slice (a)'s LOCKSTEP claimed a plan/p2.md line that commit
never carried — the .9 book section lands with (b) and the miss is on the record.

Lesson: `promotion: declined` (the normalization fix is measured by the self-test).

## _(2026-09-30)_ — the CI two-host matrix; Rosetta comes live mid-slice (P2-SCALAR.9, slice a)

The matrix is a third workflow rather than edits to rust.yml/doctrines.yml: those own
check and enforce; portability owns host-matrix evidence with its own provisioning
(nightly + miri + the BE target on the x86-64 job). The agreement mechanism is the `.8`
contract: both hosts emit the digest manifest (`demo --json` per guest, sha256-chained),
the `agree` job diffs them byte-exactly. The instrument's `--leg` selector makes each CI
job run exactly its leg; the four-leg verdict stays the full-run form. Measured locally:
native leg + manifest emission green, digest byte-identical to the `.8` recording; the
workflow mirrors the existing two (no tabs, three jobs) — CI proof lands at the next
approved push. Mid-slice the director's Rosetta install landed (via VLC's Intel build):
re-measured live (`arch -x86_64` → `x86_64`, the probe binary runs). One trap re-armed
and avoided: editing a running shell script — the restructuring was done quiescent this
time.

Lesson: `promotion: declined` (the workflow's shape is the record).

## _(2026-09-30)_ — the release route decision and the Rosetta measurement (P2-SCALAR.9 opens)

The director picked the two-route answer to the .9 fork: CI matrix permanent + Rosetta
bridge. The measurement that shaped it: Rosetta on macOS 27.0 is present-but-inert —
/usr/libexec/rosetta/ holds oahd/translate_tool/runtime, the x86-64 dyld cache sits in
the Rosetta cryptex (/System/Volumes/Preboot/Cryptexes/Rosetta/…), but the daemon is off
and exec fails (Bad CPU type; translate_tool wants the legacy cache path). External
corroboration for the symptom: the missing dyld_shared_cache_x86_64 is the documented
signature of an unprovisioned Rosetta, and on Tahoe the classic install flag misbehaves
(Jamf field report) — the activation path is recorded in the decision record. The
director's horizon fact (Rosetta phase-out fall 2027) is what makes "bridge, never
foundation" explicit on the record.

Lesson: `promotion: declined` (the decision record IS the durable form).

## _(2026-09-30)_ — the portability matrix and the honest incomplete (P2-SCALAR.8)

The leaf's substance was measurement: Rosetta absent (arch -x86_64 → Bad CPU type in
executable), no qemu user-mode x86-64 runner, Miri present on nightly (809936eac6), the
powerpc64 BE target provisioned. The instrument's first live run reported ALL legs red
against a green reality — the pipefail + grep -q defect (grep -q exits on first match,
cargo dies by SIGPIPE, pipefail reports the pipe's death as the leg's verdict); fixed by
capture-then-read, the pattern now named in the script's comment. A second authoring slip:
editing the script while a run was in flight — bash reads scripts incrementally and hit
the shifted bytes; the honest rerun was clean. The verdict ladder (passed / incomplete /
failed) carries 6 self-test arms. The record is plain-atom portability.sexp, and .9's
release report is the gate that must carry the x86-64 leg's absence. Drift owned: the
model book's bench-arm count went stale across two leaves (44 → 53); fixed, and the fix
is noted here because the book is the review surface.

Lesson: `promotion: declined` (the SIGPIPE rule lives in the instrument's comment; the
self-test enforces the verdict ladder).

## _(2026-09-30)_ — mid-execution snapshots (P2-SCALAR.7)

The design question was completeness, and the answer was already pinned: state.sexp's
hidden-state census (SEM-08) measured all seven candidates absent, so the snapshot is
registers + pc + memory — the sparse encoding (non-zero runs, digested over the whole
region) plus the bundle's definition-pin check (extracted as `check_definition_pins`,
shared, not duplicated) plus `run_state[_over]` (the state-returning runner form) plus
`FlatMemory::bytes_mut` for the resume rebuild. The proof suite splits all 49 guests at
three points each through the JSON round-trip — continuations identical, crossing logs
included; the memory-state guests are the load-bearing arms. RED arms refuse by name:
corrupted run (digest), foreign definition (pin), at_step>budget, a run past the region,
a partial register file, a mutant model (not offered). In-flight RED: my own test
arithmetic — the encoding splits runs at zero bytes, so "the image's first run" is ONE
byte and the overrun tamper fit; re-aimed one-past-the-end. A genuine surprise measured:
the CLI's 2 GiB region makes snapshot capture hash 2 GiB per call — seconds, acceptable
for a CLI tool, noted for the record (the suite's region is 64 KiB). Validation: 180/180
verify suites; make check/gate/book green.

Lesson: `promotion: declined` (recorded in the leaf).

## _(2026-09-30)_ — the PDF re-sourcing probe: measured adopt-in-principle (MODEL-METHOD.14)

The probe answered the cost question by attempting the whole sweep rather than sampling:
the naive in-order parser over pdftotext's layout-fragmented output (one field per line)
recovered every opcode (the per-page mnemonic row zips with the page's 7-bit opcode row)
and both funct streams for 37/52 forms; the 15 misses are all parser-side ordering gaps
(f7/f3 streams need page-local alignment), none a value conflict and none a document
absence — and every gap was caught by the incumbent comparison, demonstrating the control
a completed re-source would rely on. The numbering trap (PDF ch.2/ch.4 vs pinned HTML
§1.1/§3.1) was handled by keying on content. Decision: adopt-in-principle; the re-source
is a later reviewed leaf under .8's ownership. Housekeeping: the closure sweep found .15
and .17 still marked `active` with Results landed — tree-internal drift, corrected.

Lesson: `promotion: declined` (recorded in the leaf; the probe numbers live there and in
the decision record).

## _(2026-09-30)_ — min-fencei: the one-word retained divergence (P2-SCALAR.6)

Implementation matched the design exactly — the expected-divergence protocol
(at_step 0, vacuous prefix), the adapters' run-off-the-end handling, and the stop-reason
tables all predated this leaf, so no instrument needed to change: the guest, its
expectation document, one test suite, the census arm, the matrix cell. The live run shows
the protocol working at the boundary: EXPECTED DIVERGENCE at aligned step 0 vs each
reference; sail vs spike AGREE over their full 2 steps (fence.i nop + the illegal zero
word). The one tight spot: references.sexp sat 49 B under its per-part ceiling, so the
retention note is written to fit (32,765/32,768) rather than moving the ceiling for a
sentence. Validation: 175/175 verify suites; smoke green incl. the four-step protocol;
bench 53 arms; gate green.

Lesson: `promotion: declined` (recorded in the leaf).

## _(2026-09-30)_ — the discrepancy census: one divergence exists (P2-SCALAR.6 design)

Discrepancy reduction opened with the measurement its acceptance implies: enumerate every
recorded difference and every campaign result before minimizing anything. Eight
`references.sexp` difference records dispositioned with citations — two harness, one
trace-vocabulary, one sub-granularity observable, one corrected configuration defect
(pinned by guest-no-device), one board-layer (stated precondition, not a model defect),
one reference-vs-reference (sail's 56-bit tval mask; spike AND semulith agree) — leaving
exactly one model-vs-references behavioral divergence: DIFF-FENCEI-EXECUTED, the
legitimate UNSPECIFIED case. The minimization is one word (0x0000100F alone reproduces
it: policy trap at step 0; both references nop and run off the end into the measured
illegal zero word, staying each other's control). The reducer stays out of scope by
design: it minimizes against MUTANT divergences, not reference differences.

## _(2026-09-30)_ — the directed guests land; P2-SCALAR.5 done (PS-0070)

The eight guests from the measured census landed with the full wiring (gen_guests tuple +
regenerated guests.rs, one run/tests.rs suite each, the mutation census's 55 pinned
crossings, the smoke tuple, matrix cells chosen by the axis each guest genuinely
exercises). The offline differential earned its keep twice, both authoring-side:
dir-ext-matrix's first draft put its data cell at entry+0x60 — INSIDE the 0x8C code
region — so the zeroing stores patched the remaining instructions and the run stopped at
25 of 35 steps (D-CODE-VISIBILITY working as declared, against the author); moved to
0xA0, census addresses with it. dir-x0-writes' step-0 auipc constant was hand-typed
0x8000000080000000; re-derived. And the generated-fixture discipline bit once: guests.rs
must be REGENERATED after an expectation edit — a stale fixture replays the old words
(the two "persistent" failures were exactly that, not model behavior). The live smoke ran
all 48 guests three-way green: 642/642 aligned steps (+150), every run reproducing. One
documentary defect closed (c-scope.c's overclaim; the jump-table idiom is now a measured
guest). Validation: 174/174 verify suites; smoke 262 PASS / 0 FAIL; coverage 52/52;
matrix self-test 12/0; comparator 19/0; bench 52 arms after the wasm rebuild
(smoke-bench reads the built artifact — `make ci` builds before running; a bare
smoke-bench on a stale module reads the old guest set, measured); `make gate` green;
both books render.

Lesson: `promotion: declined` (the regenerate-after-edit rule is enforced by the
differential itself — stale fixtures fail loudly, measured this strand).

## _(2026-09-30)_ — strand 3 designed: eight measured gaps, two probes, one defect (P2-SCALAR.5)

Directed-sequence design started from a census, not intuition: every candidate was checked
against the tracked guests' sources AND expectation documents, the disassembled compiled
guest, and the ACT4 testplan/bodies. Verdicts: run-off-the-end is uncovered on semulith
(the harness budget equals the expectation count, so the fall-through fetch never happens
— a harness-shape finding, not a guest gap); load→use-as-address exists nowhere (every
jalr base is materialized, never loaded — and `c-scope.c`'s "indirect jump through a
switch" was constant-folded out of its ELF: logged defect, comment corrected in-strand);
the sign-extending cross-width round-trip matrix is pinned only for same-width pairs;
store→fence→execute is unpinned (`fault-selfmod` is the no-fence shape); slt→branch
chains are unpinned (ACT4's slt is compare-and-store); no loop loads AND stores per
iteration; deepest pinned serial chain is 7–8 (single-producer); six load widths and six
*W forms lack x0-destination success-path pins. The two behavior-uncertain candidates were
probed three-way before authoring: the zero word past a program traps illegal-instruction
(0x02, tval 0, word 0) on all three models (sail `c.illegal`, spike `c.unimp`, semulith
the policy conversion — the existing adapters read all three spellings), and a patched
word stays visible through `fence rw,rw` on all three (x2 ← 7). Eight guests designed,
each with its matrix cell named; ceiling expansion pre-stated per the `.1` rule.

Lesson: `promotion: declined` — the census verdicts carry their citations in the leaf;
the probes' traces are the measurement record the guests will re-pin as tracked evidence.

## _(2026-09-30)_ — the ACT4 RV64I campaign: 51/51 three-way, recorded and gated (P2-SCALAR.5, strand 2c)

The fleet run was green on the first attempt — and the first obligation was to prove the
green was real, not an extraction artifact. The cross-check: the extracted slot census
(17,017) reconciles EXACTLY against the measured static counts — 18,092 RVTEST_SIGUPD
instances, minus 1,530 dead-path instances in the six branch tests (255 each: sigupds sit
on both paths, one executes), plus 414 store-test read-back slots (sb/sd/sh/sw record
2n+1), plus 51 final_sig_offset words. Per-file deltas are uniform (+1 everywhere except
the ten explained files), and all three models agree on every count. The record is
`act4.sexp`, emitted by the runner from measured rows; RECORD-SCHEMA rule 13 re-derives
its three carried counts and closes the verdict vocabulary (self-test +5 arms, 39/0).
Two in-flight REDs, both authoring-side, both caught by the schema layer before any
commit: `(min N)` is a repeat-occurrence facet, not an integer bound (the kernel refused
it by name), and atom fields are exactly `(name value)` — the emitter's multi-value
`sparse_paths`/`evidence_note` failed uniform arity; fixed at the emitter, the record
regenerated. Ceiling re-derivations (profiles/ 99→104 files, bytes untouched at 0.83×;
schema/ health 16→18) are recorded in the registry with grounds. The campaign's standing
is stated everywhere it appears: external tests with Sail-derived expectations — EVD-04's
shared-ancestry row already forbids reading them as a second opinion.

Lesson: `promotion: declined` — the reconciliation arithmetic and the two REDs are in the
leaf's verification log where they bite.

## _(2026-09-30)_ — the ACT4 harness stands: I-add-00 three-way (P2-SCALAR.5, strand 2b)

The slice retired both toolchain risks by measurement before any fleet run: clang 21.1.8
(the docs name LLVM 22) assembled the suite's macro machinery with zero diagnostics, and
sail 0.14 (the cached README pins 0.13.1; the checked-in configs target 0.14.1) terminated
on the HTIF verdict under the laboratory override, printing `RVCP-SUMMARY: TEST SIGRUN`
itself. The design's observation adaptation works as recorded: semulith's new
`--trace-stores` (the crossing log surfaced, `mem[W,0xADDR] <- 0xVALUE`, width masked),
sail's `--trace-mem` (`mem[W,…]`), spike's commit log (`mem 0xADDR 0xVALUE` on the commit
line — a load's line carries no value, so the anchored two-group match can only take a
store). Signature extraction filters stores to `[begin_signature, end_signature)` from the
ELF's exported symbols; the verdict is the first HTIF pair (low 1|3, high 0), separated
from console bytes (high 0x01010000) by the high word — the self-test proves the channel
separation and the three RED arms (corrupted slot caught at its ordinal; shorter signature
≠ agreement; verdict-less trace refuses), 7/0. Result: I-add-00 — 513 signature slots
(512 sigupds + the final-offset word) agree semulith↔sail-derived AND spike↔sail; all
three verdicts pass. Semulith's budget is derived from sail's executed step count (4× +
10,000) because its halt is a store loop, unlike the references' native HTIF exit. No
model semantics changed; the smoke corpus is untouched.

Lesson: `promotion: declined` (the vocabulary spellings live in the harness's own comments
with the measurement citation; the RED controls enforce the rest).

## _(2026-09-30)_ — ACT4 acquired sparse; the strand-2 design measured against the fetch (P2-SCALAR.5, strand 2a)

The design doctrine is "measured first", so the design commit already carries the fetch: a blobless sparse clone (sparse to `tests/env` + `tests/rv64i/I` + `config`, pinned `e2216915…`) — 45 MB instead of the ~672 MB full tree, on the repository volume, untracked. Measured against the pinned headers, two planning-doc facts were stale: the README's sail pin (0.13.1) is superseded by the checked-in `sail.json` targeting the 0.14.1 schema, and the signature mechanism is HTIF-`tohost` in signature mode (`sail_macros.h` forcibly overrides the DUT's halt/console macros), not the old riscof signature-dump flow. The design's core decision follows from the measured mechanism: run the SIGNATURE-mode build on all three models, extract `[begin_signature, end_signature)` stores and the `tohost` verdict from each store trace — which is why the CLI learns to print the crossing log it already records (observability, not semantics). Byte-budget discipline: the live tree stood 1,226 B under its per-part ceiling, so `.4`'s design moved to the archive rather than the ceiling moving. Validation: `make gate` green (docs-only; the checker's new status value covered by its self-test).

Lesson: `promotion: declined` — the fetch recipe and census live in the leaf's strand-2 design where they bite.

## _(2026-09-30)_ — the compiled guest, written into the model book (P2-SCALAR.5, director request)

The director asked for the C-guest story in the mdBook before ending the session. It landed as a dedicated model-book chapter (`compiled-guest.md`, between references and evidence — the book's own reading order: cast, then the newest evidence kind, then the ledger), written in the book's voice: the shared-mind weakness of hand-written assembly; the self-checking design and why per-step expectation documents deliberately stay with the assembly corpus (the compiler, not the author, chooses the sequence — a step-pinned document would fingerprint one compiler's output, not derive from the specification); the measured toolchain; all three in-flight defects as the teaching record per the dual mandate; and the honest limits (129/129 three-way is finite tested evidence, not conformance). The evidence chapter's live-differential bullet points at it. Validation: `mdbook build` renders; `make gate` all green; CHANGELOG crossed its ceiling with the entry and was sharded (completeness exact).

Lesson: none new — the chapter itself is the retrievable form (the dual mandate's rule: the teaching text is where the instructive mistakes live).

## _(2026-09-30)_ — the compiled C guest retires three-way; G1 reads passed (P2-SCALAR.5, strand 1)

The strand opened with the blocker answered (PS-0062: routing + the measured toolchain) and hit two REDs before any green — both authoring-side, both diagnosed by tool, neither a model defect. RED ONE was the subtlest defect this laboratory has produced, and the guest caught it in its own author: the first compiled binary stopped at `fail(0x0501)` with the trace showing the whole post-memory section deleted. The disassembly showed clang had concluded the path was unreachable — whole-program UB exploitation. The first suspect (strict aliasing on the width-punned buffer accesses) was measured INNOCENT by the `-fno-strict-aliasing` control; bisecting sections found `w32 << 33` — a 32-bit shift by ≥ 32 is UB in C (C11 6.5.7p3), NOT "the ISA reads 5 shamt bits" — and with the amount narrowed to 31 the same compile restored `call fib` + 4× `call emit`. The lesson is recorded in the guest's own comments: the *W shamt boundary is not expressible through the C abstract machine, so it stays with `bound-shiftw`'s assembly. RED TWO was a genuine comparator gap the 492/492 corpus never exercised: with the guest clean, the three-way comparison diverged at aligned step 7 — `li a0, 0` with a0 already 0 logs `x10 <- 0` on BOTH references while semulith, whose runner diffs VALUES (the declared visible-change vocabulary, the `.1` lesson), records nothing. The fix went where the vocabulary is owned: `align` in `compare_traces.py` (the one funnel all three parsers flow through) now reduces every trace to visible changes via a shadow register file from the declared reset state (x1..x31 = 0, x0 hardwired — a nonzero x0 record stays visible as a real vocabulary mismatch), with +2 self-test arms (a dropped no-change record GREEN; a real change RED — the reduction may never mask a difference), 19/0. Soundness argument recorded in the function: a wrong value still records a change, a skipped change still diverges — only an observationally identical write is dropped, which is the vocabulary's definition of nothing-to-see. Then the green: `c-scope` (self-checking — expected values are C-semantics constants in the source, a mis-execution routes to a fail code) AGREEs with sail-riscv 0.14 AND spike 1.1.1-dev over 129/129 aligned steps and reproduces byte-identically; the smoke's new `.c` path builds via `scripts/build_c_guest.sh` (toolchain probed per candidate, refused by name if absent — Apple clang's exact error is in the leaf), runs with a budget the closing ebreak beats, and reads `e_entry` from the ELF header (a linked image's headers precede its first instruction). `gate_report.py` grew the criterion-6 met branch and the Limitations branch — **G1: `passed`**, verdict moving because the inputs did. Validation: full smoke 221 PASS / 0 FAIL (the 40 assembled guests unchanged); comparator self-test 19/0; `make gate` all green; `make book` renders both books. No Rust changed.

Lesson: `promotion: declined` (recorded in the leaf) — the C-UB lesson lives in the guest's comments where it bites; the vocabulary rule is enforced by the comparator's self-test arms.

## _(2026-09-30)_ — the routing answered, the toolchain measured: P2-SCALAR.5 unblocked (PS-0062)

The director delegated the two decisions `.5` was blocked on. Routing: the C guest lands in `P2-SCALAR.5` — the measured G0 precedent (the tree completes, the gate keeps the criterion visible every commit through GATE-REPORT, EVD-08 makes `passed` over a missing check mechanically unreachable); reopening P1-LAB would relocate bookkeeping, not evidence. Toolchain: measured, not installed — Apple clang 21.0.0 has NO RISC-V backend (the exact triple error is in the decision record); Homebrew `llvm@21` clang 21.1.8 compiled `-march=rv64i -mabi=lp64` to correct RV64I (objdump-verified); the keg ships no linker, and zig 0.16.0's bundled `ld.lld` (Homebrew LLD 21.1.8) does. Rejected: a system-wide GNU toolchain (multi-GB off-volume mutation for zero evidence gain) and routing clang's `-S` through the project's assembler (the criterion wants a genuinely compiled artifact). Recorded as `decision_c-guest-routing-and-toolchain`; `.5` blocked → active with the three-strand design before code. House-keeping under pressure: MEMORY.md's byte ceiling fired mid-commit (7217 > 7168) and was answered by demotion-grade trimming, never by raising the cap; KNOWLEDGE_MAP.md regenerated for the new record. Validation: `make gate` all green (docs-only commit).

Lesson: `promotion: declined` (recorded in the leaf) — the decision record IS the durable form.

## _(2026-09-30)_ — the SEMULITH- prefix, pinned at the boundary and watched (PREFIX-DISCIPLINE.1 — tree closes)

The director's ruling ("it is SEMULITH and not SEMILITH … only SEMULITH") answered the drift finding surfaced the same day. The measurement behind it: `git log --format='%s'` census over all 123 commits — both spellings across 10+ areas (`SEMILITH-PL` ×13 the worst), exactly one non-prefixed subject ("Initial commit"). Subjects are immutable, so the design question was WHERE the rule lives: not a history scan (fails forever on the recorded drift), but the boundary where new subjects enter — `.githooks/commit-msg` refuses any leading work-unit id not beginning `SEMULITH-`, with `SEMULITH` named in the refusal (red for the right reason, per the registry's verdict-and-reason rule). The hook is a NEUTRAL scaffold file (`update_scaffold.sh` syncs it; §21 forbids carrying the pin upstream), so the pin alone would be a silent-revert waiting to happen — the same exposure as the repaired spine defects, answered the same way: `COMMIT-PREFIX` (#29) probes the hook BEHAVIOURALLY (synthetic SEMILITH- must be refused naming SEMULITH; SEMULITH- must pass), so a reverted pin turns the very next commit RED, named. Discrimination observed before registration: the check fired RED on the real tree pre-pin (`NOT REFUSED`), and its self-test covers the four fixtures (unpinned / refuse-all-wrong-reason / over-tight / correctly-pinned) 4/0. One nuance discovered by the LESSON-PROMOTION gate, not by reading: the decline token must sit on ONE line in a staged task file — a wrapped `promotion: declined (…)` is invisible to its grep. Ruling recorded as `decision_work-unit-prefix-semulith.md`; COMMIT.md states the prefix; both mirrors carry the row; LIVE_STATUS re-derived (29 / 301, the gate's own numbers). Validation: live hook probes both directions; `COMMIT-PREFIX: ok`; `make gate` all green.

Lesson: `promotion: declined` (recorded in the leaf) — the ruling is the decision record; the mechanism is the hook, the probe, and their mirror rows.

## _(2026-09-30)_ — the channel answers: the poller fix, measured; the heard gaps reconciled (MODEL-METHOD.17)

Chipdoc's relayed note (via the director) answered the deafness `.16` surfaced: corpus `6bfabf2` makes `poll_semulith_gaps.py` descend into the `(materials …)` wrapper. Verified by measurement, not accepted: the same probe `.16` ran now reports `semulith_gaps_open: 2` against the real catalogue — pre-fix it said 0, and `.16` needed a scratch probe (flat seen, nested not) to prove the instrument discriminated at all; the channel now exhibits the discrimination itself. The two it heard were this catalogue's status-less records, and both were already dispositioned here: `GAP-INTEL-SDM-VOL1` (closed by `X86-SDM-VOL1-253665`, catalogued `.13`) and `GAP-RISCV-JAN-2026-PDF` (closed by the decline decision recorded at filing, `.12`) — chipdoc had mirrored both resolved on its side. The reconcile adds `(status resolved)` + evidence to both records so the two-way channel reads true; post-reconcile the poller reports 0 open / 0 unmirrored. The v20260120 gap's ⛔ deafness paragraph now records the fix — a live catalogue may not assert a dead channel. Corpus re-pinned `f33d330` → `92a73b6`: the working-tree path sweep first REPRODUCED the recorded f33d330 figure (5313 files / 257 PDFs) and only then was trusted for the new pin — identical, and the git delta shows why (6 files, scripts and channel, no documents). Feed census at the new pin (corpus diff, not recall): 68/14, the delta exactly chipdoc's two resolved-gap mirror records. Snapshot refreshed; REQ-008 carries the true date 2026-09-29. The consequence chipdoc flags: the channel is TWO-WAY — a new gap filed in `materials/catalog.sexp` now surfaces there without an operator relay. Validation: `materials.py --verify` 45/45 / 0 drift; RECORD-SCHEMA ok; self-test 20/0; `make gate` all green.

Lesson: `promotion: declined` (recorded in the leaf) — the two-way channel lives in the gap records and MEMORY.md.

## _(2026-09-30)_ — the v20260120 PDFs: verify the answer, then adopt through the seam (MODEL-METHOD.16)

The director's relay of chipdoc's answer (REQ-008 fulfilled, both PDFs mirrored, "same bytes", plus a numbering correction) was treated as four claims to verify, not one message to trust: (1) the mirror exists — `risc-v/isa/reference/docs.riscv.org-v20260120/` holds both PDFs + README + SHA256SUMS; (2) byte-equality — chipdoc's unprivileged PDF hashes to `06bb3c23…d150bc`, identical to the independent docs.riscv.org fetch `MODEL-BOOKS.2` measured, so the corroboration is two acquisitions, one set of bytes; (3) REQ-008 read in the ledger, the correction verbatim; (4) the numbering claim re-measured HERE from the extracted text layer — `Chapter 2. RV32I Base Integer Instruction Set, Version 2.1` / `Chapter 4. RV64I` — where the pinned HTML has §1.1/§3.1. The correction is correct, and it converts `.14`'s "a locator mapping is required" into three exactly measured numberings (HTML §1.1/§3.1 · this PDF ch.2/ch.4 · GitHub §2/§4). Both PDFs went through the corpus seam as reference-only materials (digests verified at fetch; the unprivileged one EQUAL to the web-fetched copy at fetch time), the catalogue gap was filed and resolved the same day, and the `.materials/web-sourced/` stopgap — hours old, uncommitted — was retired: the `.4` "URL kind when a second web-sourced family arrives" trigger fired and unfired in one day. The channel measurement, made before the relay arrived: chipdoc's `poll_semulith_gaps.py` reports `semulith_gaps_open: 0` against the real catalogue because its gap scan reads only top-level `(gap …)` forms and this catalogue nests gaps inside the single `(materials …)` form (scratch probe: flat seen, nested not) — the polled route is deaf to our gaps today; surfaced for a chipdoc-side fix, chipdoc untouched. House-keeping under pressure: `docs/tasks/MODEL-METHOD.md` crossed its 64 KiB per-part ceiling twice mid-leaf (67,737 B → checklists archived; 65,032 B growing → all 2026-09-27 done-leaf bodies archived); the ceiling was obeyed, never raised — the live tree now keeps only active/proposed leaves, frontier, decisions, open questions and both logs. Validation: catalogue parses/loads (45 materials); `--fetch` 2/2 digests verified; `--verify` 45/45; `--list` zero drift at `f33d330`; `make gate` all green (FRONTIER-SYNC caught the index cell naming `.16` post-completion — fixed in the index, never the tree).

Lesson: `promotion: declined` (recorded in the leaf) — the poller finding lives in the gap record; the numbering trap lives in the material notes.

## _(2026-09-29)_ — the chipdoc feed consumed: adoption is copy-and-verify (MODEL-METHOD.15)

The director supplied the corpus root and ordered a git-ignored local cache. The mechanics were cheap precisely because of an earlier design decision: chipdoc's feed (`catalog/semulith-proposals.sexp`) writes its `(material …)` proposals in THIS catalogue's own syntax, so adopting a proposal is copying a record into `materials/catalog.sexp` and letting `materials.py --fetch` re-verify its digest at copy time — no transcription, and nothing trusted from the feed. Seven adopted: the director's 2026-09-27 flagged set (psABI, SBI, BRS, U-Boot, DT, FU540, virtio, ACT) minus psABI, which was already catalogued and cached since `.11` (its SRC-02 "prefer the corpus copy" follow-up discharges here: the corpus PDF form was already the preferred one; the `.4` canonical HTML render stays beside it in `run-real-code/`). The corpus re-pin (`3c45e81` → `73711d6`) is what `corpus_drift()` compares against `rev-parse --short HEAD`, so the drift warning cleared with the variable set; the corpus block's census was re-derived at the new pin by the same path sweep (5309 files / 255 PDFs; was 3684 / 196). Two snapshot-kind materials exercised the manifest path: ACT4 (136/136 entries) and U-Boot (1219/1219) — a snapshot's identity is its SHA256SUMS digest, never a page's. The channel snapshot (`.semulith-data/chipdoc/`, git-ignored, new `.gitignore` entry) holds the map, the feed and the requests ledger; the corpus path lives in its untracked README only — Policy 12 binds tracked files, and every tracked reference stays `$SEMULITH_CHIPDOC_ROOT`. Measured absences, both recorded in the leaf: the pinned v20260120 snapshot carries no PDF (72 HTML pages + SHA256SUMS; `find -iname '*.pdf'` empty), so `.14`'s probe input stays the `.4` release-asset acquisition; and the feed proposes no psABI record because psABI was already ours. One in-flight correction, mine: the snapshot README's feed census was first typed from recall (60 materials / 10 gaps) and corrected by grep (67 / 11) — CLAIM_VERIFICATION biting on a one-line claim; caught before commit. CHANGELOG.md crossed its 64 KiB ceiling with this leaf's entry and DEV_NOTES.md crossed its own 48 KiB ceiling with this note; the DOC-SHARDING machinery answered both as designed: `shard_history.py` moved the oldest entries to `docs/changelog/shard-0067.md` (66,625 → 64,566 B) and `shard-0068.md` (50,024 → 47,681 B); completeness exact both times, manifest 70 rows. Validation: `materials.py --verify` 43/43 / 0 drift; `--self-test` 20/0; `make gate` all green.

Lesson: `promotion: declined` (recorded in the leaf) — the recall-vs-grep correction is the CLAIM_VERIFICATION discipline already documented in `docs/CLAIM_VERIFICATION.md`.

## _(2026-09-29)_ — the approval record: an exceptional push is an auditable act (PUSH-DISCIPLINE.3 — tree closes)

The variable-only approval (`SEMULITH_PUSH_APPROVED=… git push`) left no trace beyond the push itself — measured at HEAD: COMMIT.md carried no approval act and no ledger existed. The act is now a script: `scripts/approved_push.sh '<reason>'` — (1) non-empty reason (the .1 rule); (2) `make ci` green FIRST — a red suite refuses and NOTHING is written (a record of a push that never happened would be a lie in the ledger); (3) the entry appended to `docs/push-approvals.md` and committed as its OWN commit (`SEMULITH-PUSH-NNNN: push approved — <reason>` — the only way the record travels in the pushed history); (4) the push runs with the approval variable set and the hook re-verifies cadence + suite + record. The entry carries the sequential id, the act's timestamp (a dated ledger entry is a record of an act, not a currency claim — LIVE-DOC-CURRENCY does not bind it), the director as approver, the reason verbatim, the derived range (`<upstream>..<work-head>`, N commits), the suite line. Cadence pushes leave no entry. Append-only is enforced by `PUSH-RECORD` (#28): a staged change must keep HEAD's content a PREFIX of the new content (stronger than "no deletions" — an edit inside an old entry is the falsification this file exists to make visible), plus entry shape and sequential ids; self-test 6/0; fired RED on the real corpus before registration (a Reason-less entry appended to the real ledger → `MISSING FIELD`, named, then restored). The hook closes the loop: on the approval path, `pre_push.sh` requires the chain — HEAD is the record commit, HEAD~1 is the work head the entry names, the reasons match — and refuses a missing or disagreeing record (self-test 9/0 → 14/0). ⭐ The design's own defect, caught by MEASUREMENT not review: "the entry covers HEAD" is a fixpoint impossibility (the record commit advances HEAD) — and it was caught only once the scratch push ran the REAL boundary: the first scratch repo had NO hooks installed, so the defective check never ran (the shim fix: a scratch `pre-push` exec'ing the real `pre_push.sh`). The honest semantics: the entry names the WORK head; the record commit rides on top; the hook verifies the chain. Two more authoring defects, mine, owned: this host's `sed` is GNU-flavored and `sed -i ''` misparses (the codebase's `sed -i.bak` form is portable — the gate's self-test uses it); and a heredoc collision (a python edit script containing bare `EOF` lines) truncated its own input and executed fragments as shell, creating a stray `base` commit on the real repo — dropped by `git reset --mixed HEAD~1` with nothing lost and nothing pushed, and the ledger/`/docs` outside-path check confirmed nothing escaped the repo. COMMIT.md names the act; the ledger has its routes-registry row (append_history, health near the ceiling per the calibration rule). The tree closes 3/3. Validation: `make ci` green; `make gate` all green (28 doctrines / 297 arms); `check_push_cadence.sh --self-test` 11/0 unchanged. No push was attempted at any point.

Lesson: `promotion: declined` (recorded in the leaf) — the fixpoint semantics and the shim pattern are recorded in the scripts and this leaf.

## _(2026-09-29)_ — full CI at the pre-push boundary, on both paths (PUSH-DISCIPLINE.2)

Policy 16's unenforced half: the full suite ran server-side ON push (workflows trigger `on: push`), so a red CI run told you what you already shipped. Fix at the boundary. The suite is NAMED, not implied: `make ci` = `check` (fmt + clippy `-D warnings` + all tests — CI's rust.yml) + `gate` (every doctrine — CI's doctrines.yml) + `bench` + `smoke-bench` + `book`; it matches the server workflows and consciously exceeds them with the bench and the books, all local, deterministic, no network. Excluded with the reason recorded: the live three-way smoke needs the untracked reference binaries under `target/refs/` — its standing as not-a-commit-gate unchanged. The hook now execs `scripts/pre_push.sh`: (1) cadence FIRST via `check_push_cadence.sh --gate` (unchanged; the number lives there alone) — a refused push never burns the suite, measured by the stub suite's absent marker; (2) `make ci` on both paths — cadence push and director-approved alike; a red run refuses naming the failing leg from make's own `*** [leg]` error line and points at the log; (3) the green-run record `target/push/last-green.txt` + `last-green.log` — untracked, on-volume, overwritten per green run, answering "what did the last green run cover, and when" without git archaeology; NOT `.3`'s tracked append-only approval record (a different artifact, stated in both places). Acceptance (d), fired RED by a deliberately broken check: the self-test's failing scratch `ci` target → refusal naming the leg, no record; plus the record-preservation arm (a red run after a green one leaves the green record intact). Self-test 9/0 in scratch repos with a real bare upstream and a stub Makefile (the `.1` throwaway-repo pattern). One authoring defect, mine: `local record_dir=… log="$record_dir/…"` in ONE declaration tripped `set -u` (the second assignment reads the first before it exists) — 3/6 became 9/0 after the split. On this repository the hook refuses cadence-first at 115/300 with both routes named and the suite unburned; `make ci` is green end to end; the cadence self-test is unchanged (11/0); `make gate` all green (27/291). No push was attempted at any point.

Lesson: `promotion: declined` (recorded in the leaf) — the set -u ordering slip is fixed in the script; the record's shape is documented in it.


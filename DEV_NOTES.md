# DEV_NOTES.md

## _(2026-10-01)_ — the capability report is the capstone, and the registry is its claim list (P3-BREADTH.6 slice 3)

The slice order was measured, not planned: a BREADTH report generated before the unit
registration read "1 registered unit" and listed the DSP56300 family — whose evidence
anchors axis 1 had just measured green — as UNCLAIMED. The claim list IS the unit
registry, so the report had to be the leaf's last slice. With slice 2's registration
landed, the builder's three axes are the roadmap's gate text measured from tracked
files by concrete artifact name: axis 1 counts six anchors for the DSP subset (the
declared scope + vehicle, the `.a56`+`.meta` corpus, the crate's 17 tests, the
differential driver, the recorded comparison contract, the registered smoke-agreement
mechanism) plus the scalar unit's GC record; axis 2 requires each of the nine
exercised-case constructs to be DECLARED in its schema AND CARRIED by `dossier_sexp`
(the silent-drop class `.2` eliminated); axis 3 parses the pinned oracle survey for
its per-family verdicts and lists every family no registered unit backs as
**unclaimed**, explicitly — TI C6000 (ABSENT for execution), ADI SHARC (PARTIAL) —
plus the blanket rule: the registry is complete, everything else is unclaimed by
omission. EVD-08's shape holds by construction: no code path to `passed` while an
axis's anchors are absent.

Placement needed a rule, now written in `check_gate_report.sh`'s header: per-profile
reports live under `profiles/<id>/`; a CROSS-ARCHITECTURE gate's report lives at the
repo level (`docs/BREADTH-REPORT.md`) because no profile directory may own it. The
repo-level leg enforces the same regenerate-never-edit rule with the same three
controls; the self-test covers it (12/12; 4 reports in sync — G0/G1/GC regenerate
byte-identical). One cosmetic bug caught by reading the rendered report: doubled
backticks around the probe list (nested f-string quoting). Verdict: `passed` — and
the report's own "what passed does NOT mean" bounds it: exercised cases only, no
DSP56300 family compatibility, no RISC-V conformance upgrade, the slice-gated `.1`
legs named. The tree closes 8/8.

Validation: `gate_report.py --gate BREADTH` → `passed` (5,789 B); GATE-REPORT
self-test 12/12, 4 reports in sync; `make gate` all-doctrines-green.

## _(2026-10-01)_ — the second unit's book, and the ceiling the director raised (P3-BREADTH.6 slice 2)

Registering the unit meant the book generator had to stop refusing the DSP shape. The
three measured walls — exactly one `encoding_source` required (`gen_model_book: REFUSED
— … found 0`, rc=2), `encoding.sexp` required, `state["integer_registers"]` assumed —
each became an extension naming its case: `emit_encoding` emits the declared-vehicle
fragment when the profile declares `(route sibling-crate)` (the refusal stands without
the declaration — applicability derives from the vehicle block, the `.7` decision);
`emit_contracts` treats `encoding.sexp` as the ONE document a sibling-crate unit may
lack (its table row names the deferred lane and the reopening conditions), reads
register families / memory spaces / the hardware stack when there is no integer file,
and counts the `.a56` checkpoint corpus when no `*.expected.sexp` guests exist. The
rv64i regression control is byte-exact: `git diff` over the four regenerated fragments
shows ONLY the generator-digest header line.

The census took judgement, not mechanics: the requires set is C17-in / C14-out against
rv64i's — reset is this unit's own decision (D-RESET-STATE) while interrupts are a named
exclusion — and the 24 rows distinguish `missing` (excluded subsystems with named
closing routes: interrupts, modes, OnCE) from `out-of-scope` (the architecture never
owed them: FP, SIMD, MMU, multicore). SEAM-INTEGRITY caught one under-evidenced ROOT
CAUSE box on the first pass — fixed with the probe's concrete command line, the gate
doing its job (679 boxes re-accepted).

The same slice carries a director ruling, documented on the record: **task-tree growth
is allowed** — the docs/tasks/ per-part rose to 128 KiB
(`decision_task-tree-per-part-growth`) after six forced archive operations in one day,
two of them archiving ACTIVE narratives hours old. The director's invariant stands and
is recorded with it: a bound remains — a file must stay readable in one sitting, growth
is never unbounded; and his standing instruction: **ask for ceiling raises — they are
approved; document everything — requests, rulings, nothing under the radar.** My open
request under it: MEMORY.md (7,168 B) and LIVE_STATUS.md (6,144 B) both needed
fit-trims in three of today's commits — a modest raise (≈ 8 KiB each) would end the
recurring compression of resume-pointer content. Awaiting the director's word; the
fit-trims continue meanwhile.

Validation: UNIT-BOOKS ok (2 units, both build); MATERIALS-BILL ok (12 DSP materials,
every section negative); SCOPE-COVERAGE ok (2 units may code); `mdbook build` rc 0;
`make gate` all-doctrines-green (SEAM-INTEGRITY 679 boxes).

## _(2026-10-01)_ — the second unit's contract records, and the fixture that noticed (P3-BREADTH.6 slice 1)

The DSP profile's `requirements.sexp`/`contract-obligations.sexp` landed as governed
documents, closing the DOSSIER's records row. The shape is RECORD-SCHEMA's rules applied,
not invented: COVERAGE forced each requirement's statement to be its decision's
byte-identical text (seven decisions → seven `REQ-D-*`), MIRROR forced each mirror
obligation to restate it verbatim, AUTHORITY forced `defined` ⇒ `architecture` (the three
laboratory decisions take `laboratory`), and OBLIGED forced the ±POS/NEG pair per
obligation — 26 declared checks over contract `dsp56300-lab-env-v0`. The six `OB-ENV-*`
records carry the laboratory's half of the contract: no guest-reachable time source (`cyc`
is informational and never compared), sequential scalar issue (the F5 pending-writes
window measured ABSENT by the F6 census), cold reset to D-RESET-STATE's values, one 24-bit
P-space word per fetch, no asynchronous events (interrupts are a named subset exclusion),
and instruction-level atomicity. RECORD-SCHEMA attached with zero gate edits — the
catalogue auto-discovery found the new files and every cross-rule passed on the first run
(10 record files).

The interesting failure was FACT-OWNERSHIP's self-test, which did exactly what it exists
to do: its GREEN fixture's pair spec globs the REAL corpus
(`profiles/*/contract-obligations.sexp` × same-unit `requirements.sexp`), so landing the
DSP catalogues turned the fixture RED — `UNREGISTERED MIRROR PAIR`, the fixture registry
named only rv64i's pair. The re-pin names both units (`__CHECKED__ 5 → 6`) with the reason
in the check's comment — the same designed staleness the synth probes carry: a fixture
calibrated to a corpus the work just outgrew. Validation: both catalogues schema-validate
ok; RECORD-SCHEMA ok (10 files); FACT-OWNERSHIP ok (25 kinds), self-test 10/10;
`make gate` all-doctrines-green. The rv64i catalogues are byte-untouched.

## _(2026-10-01)_ — ask through the channel, and write down how asking works (P5-BOARD.8)

The director offered CHIPDOC's web-scorching for the network-connected board's component
documentation. The useful engineering content was the survey BEFORE the ask: the
snapshotted feed already holds a complete register-level Ethernet contract (TI-DP83816),
the ESP32 register maps, both SiFive SoC manuals, and the AM335x TRM — so the ten
requests only cover what is genuinely missing, each with a QEMU-oracle note or an
explicit probe flag (the AR9271 request expects a measured negative, which is itself the
answer to "is any WiFi baseband documented"). The process defect found and fixed: the
filing mechanics (requests.sexp preferred, gaps the false-positive-prone fallback,
exactly-once ids, the watcher firing on file change) lived only in the corpus-side
CHANNEL.md — a session had to re-derive them, and the director noticed. The fix is a
knowledge card, not a complaint: the next session reads
`docs/knowledge/the-chipdoc-request-channel.md` and files in one step. Verification
worth naming: chipdoc's poller was RUN (read-only, its own documented interface) and saw
exactly the ten new ids — the channel measured live, not assumed.

## _(2026-10-01)_ — the landing is the boring part when the measurement came first (P3-BREADTH.7 slice 3)

After slices 1–2 measured every attaching gate against the drafts, the landing itself was
a rename plus the ownership rows: `git mv` semantics for the three documents, five rows
in `fact_ownership.tsv`, and two census arms that only exist post-landing (they measure
the real two-unit corpus: a GREEN pair-registered arm and a RED unregistered-pair arm —
a gate whose arms depend on the corpus they judge is only writable after the corpus
lands, which is why they were scheduled, not forgotten, in slice 2). The one judgment
worth recording: the DSP's `guests/` registered as a fact owner with NO mirror — the
rv64 guest kind has a generated mirror (`guests.rs`, GUEST-GEN), and the DSP's honestly
has none yet; the registry's "mirror `-`" spelling is the honest zero, not a gap. The
DOSSIER's deferral rows now name `.6` for requirements and unit registration — the
earlier "lands with the model slice" wording was stale the day the model slice closed
without them, and two slices carried the correction.

## _(2026-10-01)_ — the matrix fit, the census didn't (P3-BREADTH.7 slice 2)

Two opposite findings in one slice. INTERACTION-MATRIX needed no gate change at all: the
schema is shape-generic (axes + cells + dispositions), the mechanism registry extends by
design (two DSP entries, each with a proof-of-life needle), and the orphan sweep only
globs `*.expected.sexp` — the `.a56` corpus is invisible to it, so a mechanism/degenerate
matrix resolves cleanly. The DSP's six-axis matrix (progress, stop, loop, stack, alias,
state) is real content: every cell lands on the smoke agreement, the typed-stop type, or
a cannot-arise reason. FACT-OWNERSHIP, in contrast, had a genuine second-unit defect: its
completeness census enumerated restatement pairs as a cross product of glob expansions —
exact while one unit existed, and the DSP's landing probe showed it inventing cross-unit
pairs (rv64's requirements "restating" the DSP's profile). The fix keeps the census's
teeth where they're checkable: same-unit pairing inside `profiles/*/`, and cross-family
pairs are registry-nominated with a restater-participation census — owner-side
participation is deliberately not required, because the DSP's state.sexp has no generated
mirror by design (the `state.rs` naming convention exists precisely to reserve that
claim). Fact kinds are now qualified per unit. Also landed: DOSSIER-SCHEMA, the 30th
doctrine — the dossier documents now schema-validate as a class, fired RED on the pre-fix
D-FENCE document recovered from git history before registration. Process lesson the hard
way: DERIVED-COUNTS measures the working tree, not the staged set — two co-developed
slices that interlock through a count must land in one commit, or the hook refuses both.

## _(2026-10-01)_ — applicability is data, not a waiver (P3-BREADTH.7 slice 1)

The fork was: named deferrals (gates learn to skip a declared unit) versus the full
evidence-shape machinery (per-step expectations and a 21-cell exercised matrix for a
checkpoint-compared subset). Both were wrong, and the measurement showed why: a deferral
is a weakening surface whose expiry answers "when does the leaf close" — but the gates'
contracts become applicable when the unit's DOCUMENTS exist, which the gates already
re-derive per commit; and the fiction machinery builds evidence the subset's claim never
cites. The adopted shape: the unit DECLARES its vehicle (route × comparison, closed
enums, laboratory authority), gates apply the contracts matching the declaration, and a
declaration that contradicts the documents is a finding. No expiry machinery is needed
because the contradiction check fires the day declaration and documents disagree — the
trigger is the document landing, which is exactly when the full contract becomes
applicable. The one piece of real machinery earned its place: the guest census measures
"every declared form is exercised" for the DSP's actual corpus (both directions), and it
measured 19/19. Fixture-writing lesson, again: `printf '%s'` does not interpret `\n` in
its argument — `%b` does; two self-test arms caught the glued lines before anything else
could.

## _(2026-10-01)_ — measure the lane before funding it (P3-BREADTH.5 slice 3)

`.4` had deferred "the generator generalization" to `.5` as a phrase; slice 3 turned the
phrase into a measurement. The reading: `gen_definition.py` refuses a second unit at
three named walls, and they are load-bearing, not cosmetic — the 32-bit decode table is
the emission's shape, the semantics corpus is the input the whole interpreter-before-
compiler direction runs on, and the semantics language itself is scalar-shaped (31
operators; load/store have no space parameter; `reg`/`pc` are the only state reads). So
"generalize for the DSP" means a 24-bit emission, a new fragment family, the DSP's
semantics re-expressed as data, and `Sem` enum variants — a lane. The discipline question
was whether the exercised target DEMONSTRATES the need (`.5`'s own acceptance), and it
does not: the sibling crate covers subset v0, differentially agreed 6/6, and no current
milestone consumes the generated form. The deferral names its reopening conditions, which
is what keeps it a decision rather than a drift. The dossier landing became its own leaf
(`.7`) because its real content is a doctrine design choice — how a gate says "this unit
is out of my scope" without going silent — and that deserves a leaf, not a paragraph.

## _(2026-10-01)_ — measure the attachment before landing the document (P3-BREADTH.5 slice 2)

The slice's real content was a measurement discipline: the DSP's `profile.sexp` and
`state.sexp` were drafted, then placed untracked — and intent-to-added, because three of
the four attaching gates enumerate units through `git ls-files` while PROFILE-CONSISTENCY
globs the filesystem; the difference mattered, and the first measurement saw only one
gate's verdict — and every attaching gate was run before anything landed. The haul:
PROFILE-CONSISTENCY's EVD-04 and SRC-03 arms had seven latent defects to catch in a
dossier that had sat tracked-but-unchecked since `.4` — an "obtained" candidate with no
binary/digest/injection, and independence pairs naming labels instead of candidates. The
fix made the dossier better, not just greener: the asm/emu legs and gearmulator are now
first-class candidates, so the independence rows name things the dossier describes. Two
more defects fell out of the re-validation sweep: rv64's own `profile.sexp` had drifted
from its schema (two notes on D-FENCE — ungated, because no gate schema-validates the
dossier documents as a class; the landing slice now owns that leg), and the coverage
denominator counted a comment's prose as mnemonics. Design note: the taxonomy's scalar
shape lived in exactly two closed places (the schema's scope construct and
`_SCOPE_LISTS`), and the gate readers were already generic over group names — the whole
extension was schema fields plus one tuple, no reader edits. That is what generic readers
buy: the schema is where per-target shape lives, and adding a target is naming it there.

## _(2026-10-01)_ — moving a refusal one layer down, on purpose (P3-BREADTH.5 slice 1)

The interesting engineering was not the schema constructs but the boundary mechanics. The
synth fixture exists to measure the pipeline's refusal boundary; when the schema learned
`memory_spaces`, probe 2's pin went stale and the suite turned RED on the first run —
that RED is the fixture working, and the re-pin (schema accepts rc 0, generator refuses
`memory_spaces declared` rc 2) is the boundary's new position measured rather than
asserted. Two silent-path hazards had to be closed for the move to be honest: the mapping
owner built the state document from named fields only, so a schema-legal `memory_spaces`
would have vanished before the generator could refuse it (the same class `.2` fixed for
operands — the promoted lesson's second instance); and `gen_state.py` subscripted
`doc["xlen"]`, so the schema's newly-optional xlen would have crashed with a KeyError
traceback instead of a named Refusal. Both are now refusals by name with RED self-test
arms. A design rule the slice surfaced and recorded: a profile document that no gate reads
is an ungoverned claim — PROFILE-CONSISTENCY attaches at `profile.sexp`, so the DSP's
`state.sexp` waits for the scope-taxonomy slice rather than landing unread.

## _(2026-10-01)_ — the census as a harvest, not a rewrite (P3-BREADTH.1, the F6 leg)

F6 is the finding that the hidden-state census reopens per profile; the live question was
what "re-run" means when this profile's `state.sexp` is deferred to `.5`. Answer: the
census lands as a measured record, not a schema document — `.5`'s named cases (special
registers, F1 widths, F3 spaces) harvest it. The substantive content was already earned by
the differential campaign: the A2/B2 sign-extended readout, the A1/B1 raw reads, S's
absent writer, the stale popped stack slots that are hidden from the programmer but inside
the dump. The census's own contribution is the surface-completeness argument — before
asking "is anything hidden?", prove the observation surface covers every mutable cell:
stack slot 0 is unwritable by the pre-incremented SP, P below the deviation window is
constant because subset v0 decodes no P-space write, and the harness's private X window is
excluded by the harness's own contract on both engines. With that argument in place the
6/6 agreement becomes a completeness measurement, not just an equality measurement. The
scalar census's seven candidates were re-asked verbatim; three flipped to "absent
architecturally" (no reservation mechanism, no FP, no vector unit exist in the family to
hide), and the fetch-cache answer came out one step stronger than rv64's — the DSP56300
has no instruction cache at all.

## _(2026-10-01)_ — where the manual and the silicon part ways (P3-BREADTH.4 slice 4)

Form-coverage completion for `semulith-dsp56300` was a decode exercise plus a semantics
arbitration exercise. The decode side was routine in the good way: FM figures give the
shapes, the pinned assembler's probe words confirm every mask (one probe misalignment on
my side — reading the lod two lines off — caught instantly by the pinned decode test).
The semantics side is where the differential campaign earned its keep: first smoke run
was 2 agree / 4 fail, and every failure was a real model defect with a distinct root
cause. RTS restores PC only, not SR (FM 13-168 was right; my 56000-style assumption was
wrong — the jsr guest pins it: the U bit survives both returns). A short immediate to an
accumulator sign-extends through A2, falsifying the FM's "remaining bits are zeroed"
prose. A1/B1 memory reads are raw — the shifter/limiter lives on the whole-accumulator
read path (my FM-derived limiter on A1 was an over-application, refuted by a stored
$FE00FF). The S bit sets only on accumulator bus reads, so no subset-v0 path sets it at
all (an ASR of a negative accumulator proved it). And a keep-mask nibble-slip
(`0xFF00…` for `0x00FF…`) zeroed A2 on the 24-bit logical ops — the kind of bug the
reference's b2=$FE dump line makes instantly visible. Guest-side lesson: the assembler
will shorten `move #$000002,x1` to the fractional short form; `#>` forces the long form,
and the model's typed OutOfWindow stop is what caught the runaway. The reference's emit
source was used to LOCATE mechanisms (TOOLBOX); every rule's evidence is the dump
agreement, so EVD-04's independence ledger is unchanged and the claim stays
EXPERIMENTAL.

## _(2026-10-01)_ — a chapter with a lifecycle (MODEL-METHOD.19)

The director ruled the demand chapter a live one: its content will sharpen as more CPUs,
DSPs and boards are modelled. The marker that went in states the evolution rule —
re-derived per unit, prospective-becomes-measured, classes split or merge — and
deliberately carries no date, because a hand-kept "status as of" is false the day after
(LIVE-DOC-CURRENCY); git carries the currency, the chapter carries the rule. A document's
lifecycle is part of its contract, and naming it keeps the next editor from treating a
measured-on-two-units list as a settled one.

## _(2026-10-01)_ — what it takes, per kind (MODEL-METHOD.18)

The director asked for the precise set of information needed to model a CPU, a DSP, or a
board, and what not having it prevents. The interesting part of the answer is that
"prevents" is not one word but three. Prevents-the-model is the one everyone expects: no
encodings, no decode; no semantics, no model. Prevents-the-claim is the one this project
was built around: you can always BUILD something — the question is whether it may call
itself evidence, and that fails for want of a reference (SRC-02), an independence
inventory (184/199 shared SoftFloat files), or a matched configuration (the ISA string
that matched for four leaves while the platform underneath did not). And
prevents-the-bound is the quiet one: without the census you can build it and run it and
still be unable to say what you do not model. The per-kind lists then write themselves
from the record — a CPU is the base set, a DSP is the base set plus the axes that broke
scalar assumptions (each one measured: the x1=050000 readout, the memory_spaces refusal,
the U-bit inversion), a board is the base set plus composition, prospective and marked
so. A catalogue says what could be known; a demand list says what it costs not to.
Promotion: declined in the leaf (the chapter is the durable artifact — it lives in the
book where the director reads it).

## _(2026-10-01)_ — the first DSP instruction executes (P3-BREADTH.4, slice 3)

A bounded model earns its keep in the details nobody warns you about. Three earned their
record this slice. (1) The manual's own extraction lies: FM Table 5-1's U-bit row says
"set if the two MSBs are identical" in prose and prints "U = (Bit 47 xor Bit 46)" as the
equation — an inversion (the equation should read xnor), proven by the reference's
`sr c00310`, which agrees with the prose. The differential harness exists for exactly
this class of question: when the document disagrees with itself, the measured machine is
the arbiter, and the arbitration is recorded where the next reader meets it (`exec.rs`'s
module docs). (2) A naming convention is a fact with an owner: the crate's state module
was born `state.rs`, and FACT-OWNERSHIP refused the commit because this repo has already
decided that `crates/*/src/state.rs` means "a GENERATED mirror of a profile's
`state.sexp`". Renaming to `machine.rs` was not routing around the gate — it was
learning that the name was already taken by a stronger claim. (3) The honest dump has a
hole in it: the runner emits no `cyc` line, because the reference's cycle counts are
base-table informational and a fabricated number would be a timing claim by stealth. The
comparator skips `cyc` by a recorded rule with the reason in its header — an absence
with a name, like every other exclusion in this subset. The reward: the demo guest's
dump is byte-identical between the two engines, 53 fields, on the crate's first run.
Promotion: declined in the leaf (the crate, the comparator, and the recorded inversion
are the durable outputs, living where the next evaluator meets them).

## _(2026-10-01)_ — a second profile walks into the gates (P3-BREADTH.4, slice 2)

The dossier slice's first job was a measurement, not a file: how do the auto-discovering
gates treat a second, deliberately partial profile? The answer, read from the gate sources
and then confirmed by a green `make gate` with the dossier present, is better than hoped:
every one of them keys on `profiles/*/profile.sexp` or `profiles/*/encoding.sexp`, so a
dossier whose schema-deferred documents do not exist yet is simply invisible — and the day
those documents land (the model slice, then `.5`), the gates attach with no gate edit at
all. The discipline that made this boring is the same one that made the deferrals explicit:
DOSSIER.md carries a deferral table in which every absent document names its owning leaf,
so "invisible to the gates" never reads as "forgotten". Two smaller facts earned their
keep: `fetch_references.sh` processed candidates only by hardcoded id, so the dsp56300
ledger needed a generic source-tarball leg (the discriminator — asset + source_commit +
asset_sha256 — was chosen so the rv64 ledger provably never reaches it, then re-verified
identical); and the FM manual's pin gained a second acquisition route when NXP's own
locator served byte-identical bytes to the chipdoc-cached copy — a version string is not an
identity, but a digest match from two independent routes is close to one. Promotion:
declined in the leaf (the census lives where the next profile meets it; the durable output
is the measured answer, not a method).

## _(2026-10-01)_ — the bounded subset, chosen against the gaps (P3-BREADTH.4, slice 1)

Selecting a "narrow real slice" is itself measurement work, not preference. Three censuses
did the deciding: the pinned reference's `Instruction` enum (its decode is DSP56300-complete,
so coverage bounds nothing), its `LIMITATIONS.md` read in full (SA/SC/DM mode bits inert,
stack extension absent, peripheral interrupts unverified, cycle counts base-table only —
each gap became a named exclusion, because evidence cannot outrun the oracle's own honesty),
and the difftest harness's comparison contract (checkpoint-level canonical end-state:
registers, deviation-encoded X/Y windows, 15 stack slots; `steps` is the compared counter,
`cyc` informational forever — a simpler shape than the RISC-V per-instruction commit walk,
and a different one: a per-case comparator, not a first-divergence walk). The subset that
survives is `dsp56300-lab-v0` v0: non-parallel moves with the A2/B2 extension readout (F6's
named case), the immediate/register ALU core, signed `mpy`/`mac`, `nop/jmp/jsr/rts`,
`do`/`enddo`/`rep`, linear addressing. The hardest call was excluding parallel moves — the
defining DSP shape — and the honest way to exclude something load-bearing is to name it as
the first extension candidate rather than let it slip out silently. The vehicle (a sibling
crate, manual-derived, EXPERIMENTAL) followed from the tree's own routing: the pipeline
refuses a second unit by name and that generator work is `.5`'s; building the generalization
before its exercising target exists is the speculative generality P3 was created to refuse.
Two gaps surfaced and were routed, not smoothed over: the profile schema's scope taxonomy is
scalar-named (a `.5` named case), and the auto-discovering gates have never met a second,
deliberately partial profile (the dossier slice's first measurement).

## _(2026-10-01)_ — the evidence path, run for real (P3-BREADTH.3, slice 2)

A survey says a path exists; only running it proves it reproduces here. The DSP56300 route
pinned (commit `c60aeedb`, sha256-recorded tarball under `target/refs/`, the RISC-V
references' own discipline), built on-volume (31.7 s; the upstream's 1.98.1 toolchain pin
sidestepped with `RUSTUP_TOOLCHAIN=1.98.0` because installing it would write the OFF-VOLUME
rustup store — §13 applies to reference builds too), and exercised with a synthetic micro
guest: assembler rc 0, emulator rc 0, 16 steps, canonical dump. The value of the demo was in
the verification, not the run: hand arithmetic reproduced the 56-bit accumulator to the bit
(`001f253d515280`), the memory deviation dump proved the X/Y-space stores landed where
aimed, and the one value that looked wrong (`move #$5,x1` → `x1=050000`) traced to the
family manual's §3.4.1.3 (an 8-bit short immediate to X0/X1/Y0/Y1 is a fraction stored in
bits 23–16) — a reminder that on an unfamiliar ISA the FIRST reflex is "the toolchain is
wrong" and the correct one is "read the manual's move semantics". Promotion: declined in the
leaf (dated evidence; its durable output is the demonstrated path, recorded in the tree).

## _(2026-10-01)_ — the oracle question, answered by census (P3-BREADTH.3, slice 1)

The tree carried an open question — "whether any real DSP oracle becomes available at all" —
and the honest way to answer it was enumeration, not memory: one survey per measured family
over the same enumerator (QEMU/MAME/gem5/GDB-sim/binutils/LLVM/vendor tools/dedicated
projects), one URL per claim, then the two load-bearing positives re-fetched from primary
sources. The answer inverted the tree's prior assumption for two of three families: DSP56300
has a STRONG path (an MIT toolkit whose authors already built the exact differential harness
this project would need, silicon-sealed), SHARC-2106x a PARTIAL one (MAME's BSD-3 core, but
the assembler leg is unbuildable-as-licensed), and only TI C6000 is truly oracle-less (the
vendor discontinued its simulator in 2014). The slice decision — DSP56300 — follows from
RK08's rule (evidence path, not manual convenience) and fits the findings' conditioning: it
activates F1/F3/F6 and leaves F4/F5/F2 unbuilt, recorded rather than lost. Promotion:
declined in the leaf (the survey is dated evidence; its durable output is the decision).

## _(2026-10-01)_ — a dead justification camouflaged a live silent path (P3-BREADTH.2)

The hook audit's only silent escape hatch survived review precisely because it carried a
plausible justification: `extract_operands`' `_` arm skipped operands naming no field,
"because FENCE's `fm`/`pred`/`succ` have no field ranges" — true when written, false since
`P2-SCALAR.1` gave all three fields, leaving the arm unreachable for real data but live for
any future unfielded operand, with enforcement only in a test ratchet whose own whitelist
comment had gone stale in the same way. The fix put the invariant where ARCHITECTURE §2 says
it lives: generation time. `gen_definition.py` now refuses an unfielded operand by name
(rc 2; the DEF-GEN self-test's new RED arm feeds `add` an `rs9` operand and demands the
refusal), the runtime arm returns `ModelError::InvalidDescription` instead of skipping, and
the ratchet is strict. Wider census result: no opaque hooks anywhere — the three seams that
exist (`Environment`, `step_over`, bench `Observer`) are typed contracts that cannot reach
instruction behaviour. Lesson promoted to
`docs/knowledge/a-dead-justification-camouflages-a-silent-path.md` — census the SHAPES
silence takes, then re-measure each justification's premise; never read the comment as the
check.

## _(2026-10-01)_ — F2's honest limit, retired (P3-BREADTH.1, slice 1)

The findings report graded itself and flagged F2 — register grouping with fill
semantics — as the one finding whose NEEDS-A-CHANGE classification rested on the state
document's shape rather than a measured refusal, and named the remedy: a grouping probe
in the synth suite. The probe is the real scalar profile's state document plus one
synthetic `register_groups` form under `integer_registers` (an odd:even pair with the
TI C64x zero-fill readout rule, locator in the descriptor's header comment), reduced
until the schema layer's ONLY refusal is the grouping shape:
`undeclared field "register_groups"`, rc 1 — the checker recurses into nested
constructs, so the pin measures the file's nesting, not just its top level. The wider
result is the routing determination: applying the findings meant measuring that the
required-unconditional set is empty. F4/F5 carry the review's own VLIW condition, F2's
implementation idles unless `.3` picks TI, F6 is per-profile work whose method already
exists and is gated. Implementing any of them today would add unexercised abstraction
surface — precisely what the tree's gate refuses ("stabilize only what has been
demonstrated"). `.1` is slice-gated, not closed: the implementation legs stay owned by
name and reopen with `.3`'s slice decision. Scalar regression re-run green across the
board (`make check` 180/180, gen_state rc 0, DEF-GEN ok, G1 `passed` re-derived).

## _(2026-10-01)_ — the routing method held (DSP-REVIEW.7, tree closed)

The tree pre-committed to its routing method before the first finding existed —
locator, executable demonstration, scalar reproduction check — and the capstone leaf
graded itself against exactly that. The payoff: the one finding that could not meet the
method (F2, register grouping, never pushed through the pipeline as a probe) is visible
as a labeled honest limit instead of passing as measured. The scalar controls did real
work too: the same generator that refuses a 24-bit state document with rc 2 emits the
scalar profile's 64-bit one with rc 0 — "the limitation does not fire for
`rv64i-lab-v0`" is a pasted command, not an argument. Six findings routed to
`P3-BREADTH`, five non-findings classified out as semantics data, and the review's
lasting discipline — a TI absence is never a DSP absence — is now the receiver's
inheritance, not just this tree's rule.

## _(2026-09-30)_ — TI's absences are TI's (DSP-REVIEW.8)

The review extracted three TI manuals first, and the absence facts it pinned (no
accumulator, no guard bits, no bit-reversed addressing) were one lazy reading away from
becoming "DSPs don't have accumulators". The two manuals the chipdoc channel answered
the same day measured the opposite: DSP56300 has two 56-bit accumulators with 8-bit
extension registers, SHARC has 80-bit accumulators and prints the words "guard bits",
and both have bit-reversed addressing. The `.4` break — the execute packet and the
delayed visible writeback — is now scoped where it belongs: TI-family-shaped, not
DSP-shaped, with SHARC's interlocked five-stage pipeline as the printed counterexample.
A finding's scope is only ever as wide as the corpus measured so far; the tree's own
rule (a TI absence is never restated as a DSP absence) is now armed for `.7`'s report.
Also recorded, fourth time this day: an unmeasured number composed into a checklist
(9 and 11 written where the tool said 14) — caught pre-commit, again. The practiced
rule holds: paste real output, never compose it.

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


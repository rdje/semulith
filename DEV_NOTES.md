# DEV_NOTES.md

## _(2026-10-02)_ — the ceiling taxed a property the file could not have: the instrument must match the failure mode (P5-BOARD.12)

The day after the composed-unit bound raise, the director delegated the policy question
it stood on ("yours to decision and act upon … SOTA, SIGNOFF and PRODUCTION-GRADE").
The ruling: a per-part byte ceiling exists to catch silent accretion in
hand-maintained files, and a regeneration-gated derived file cannot accrete silently —
every byte is re-derived on every commit, and its size is a pure function of
already-bounded inputs. So the interim 128 KiB raise (one day old) was the right
stopgap and the wrong instrument, and the gate went two-tier: authored members keep
the 64 KiB ceiling, derived members are exempt **as a checked property** — a
fact_ownership.tsv mirror row with a regeneration-doctrine governor (closed set), never
a declaration. The exemption consuming the FACT-OWNERSHIP registry is the part that
makes it signoff-grade: the registry is already completeness-checked (every governor
registered, every corpus pair named), so no second declaration surface exists to drift,
and an authored file cannot smuggle under the exemption because nothing regenerates it.

Two implementation details worth remembering. The per-part loop previously inspected
only the single biggest member (`sort -rn | head -1`) — a second over-ceiling file was
never even reported; the two-tier rule forced judging EVERY member, which is strictly
stronger for authored content too. And the self-test harness gained the arms in the
real corpus's shape: the RED for an authored file over the ceiling fires on fixtures
because the real corpus's authored members are all (correctly) under the ceiling — a
control that only ever sees GREEN in production is exactly the kind that must be seen
RED in the harness. And a third, caught by DERIVED-COUNTS itself: the regen-set arms
were first written under a new `armregen` helper the enumerator does not count, so 2
of 17 arms were invisible to the arm total (357 ≠ 359) — fixed by folding the probe
into `arm`'s optional `[cmd...]` form rather than teaching the enumerator a third
idiom. New self-test idioms are not free: the arm total is a census, and a census
only counts the shapes it knows.

Lesson: **promoted** — `docs/knowledge/a-byte-ceiling-applies-to-authored-content.md`
(the question form + the checked-exemption pattern; the ruling itself is
`decision_derived-members-of-bounded-families`).

## _(2026-10-02)_ — a freshness gate deferred to "the first tracked board" lands exactly once (P5-BOARD.3)

`compose_units.py` shipped with its freshness proof explicitly deferred — "lands with
the first tracked board" — and P5-BOARD.3 was that board. The shape that landed: one
generator (`gen_board.py`, boards discovered by declaration, never a hardcoded id),
seven artifacts per board, and the BOARD-GEN doctrine re-deriving all seven on every
commit. The compose factorization is the part worth remembering: `compose()` took a
manifest FILE, which pins part resolution to the manifest's location — useless inside a
generator that derives the manifest itself and must compose in scratch. The fix was not
a second materialization path but `compose_resolved(comp_id, part_dirs, out_dir)` — the
manifest-file entry point and the generator both land on it (the refactor measured
byte-identical on the real parts, self-test 9/9).

Two measurements did the design's real work. The FACT-OWNERSHIP probe: placing the
composed catalogues in the board directory tripped the gate's self-test on EXACTLY the
two new restatement pairs — the gate refusing to judge an unregistered corpus is the
registry doing its job; registration (8 rows), not weakening, was the fix. And the
design brief's register-surface containment check turned out NOT implementable: the
device dossiers carry register offsets in prose with datasheet citations (measured in
both `state.sexp` documents and the expectations), never as machine-readable data — so
the generator's refusals are scoped to what board.sexp itself proves (overlap, window ↔
device resolution, executable-mmio, ghost console), and machine-readable offsets arrive
with the device models, where the check belongs. A brief line that says "measured at
execution" is a promise; the honest outcome can be "the data is not there".

Lesson: `promotion: declined` (recorded in the leaf) — derive-from-declaration and
measure-before-design already carry their decision records
(`decision_device-applicability-by-declared-vehicle`, `decision_gate-applicability-by-
declared-vehicle`); the compose factorization is recorded with the leaf and in
`compose_units.py`'s own docstring.

## _(2026-10-02)_ — the channel answered in hours; the survey's excluded layer was our own catalog (MCU-DOCS.2)

The twelve MCU requests came back 12/12 fulfilled the same day — the channel's report
(`build_responses.py --report`, rc 0) is the verification entry point, and the adoption
pattern from P5-BOARD.9 (adopt → fetch with digest re-verification → mark our own file)
carried unchanged. The routes the channel measured are worth reading in the answers:
Arm's documentation-service API works; NXP/Microchip/ST's live URLs 404/403/reset to
automated clients and the Wayback captures of the same official URLs carried the bytes.

The execution's real event: the RP2040 datasheet answer read "already held before this
request" — and it was held **twice**: corpus-side, and in our own tracked catalog as
`RP2040-DS` since 2026-09-14 (digest-identical, cached). The `.1` survey had measured
the corpus's proposals feed, not the corpus tree, and not our catalog — the
survey-sampling failure class from MODEL-METHOD.13 recurring at a second layer. Fixed
at root: no duplicate record adopted, the request's answer records the redundancy, and
the knowledge card gained the three-layer "already held" rule with the cheap
complement-check commands.

Lesson: **promoted** — `docs/knowledge/a-survey-that-found-things-can-still-have-missed-things.md`
(the recurrence + the three-layer rule).

## _(2026-10-02)_ — the reading-experience audit's yield was drift, not style (BOOK-APPARATUS.2)

The first audit pass against `decision_mdbook-incremental-engaging` ran as six parallel
read-only chapter-group reviews with the decision's four criteria operationalized
(incremental build-up; motivation before mechanism; layered density; both-audiences
engagement), each returning per-chapter verdicts with line-level evidence. The signing
discipline: **every flagged item was re-verified against the repository before any edit**
— and that verification caught one audit false-positive class (a `grep -c` miscount of
the rv64i profile's inline decision forms; the real count is 28, verified by enumerating
the ids) and one of my own typos (a search string that silently didn't match —
`grep`-verified after the edit, not assumed).

The measured surprise: the audit's yield was **factual drift**, twelve places where
hand-carried repository facts in the book had gone stale — the class DERIVED-COUNTS was
founded on, living in chapters no enumerator covers. Three genuine style violations
(a duplicated sentence, a cold open, a 68-line accreted list item) were the minority.
Two mermaid blocks rendered as raw source in the book; replaced by text flows rather
than adding `mdbook-mermaid` (a dependency the project hasn't sanctioned).

Lesson: `promotion: declined` — the audit method is the decision record's own
consequence clause (`.2` owns the pass; the pass is recorded); the drift fixes are
per-slice history.

## _(2026-10-02)_ — registration day: the enumeration follows the declaration (P5-BOARD.11)

Registering the first board and the first devices measured exactly where the machinery
was processor-shaped: not only the two `sibling-crate` conditionals the `.2` routing
note had named — the emitters also *load* `references.sexp` (absent from all three new
dossiers; the board has no `profile.sexp` at all), `emit_contracts` reads
`interactions.sexp` and globs `guests/`, and the MATERIALS-BILL gate's COMPLETENESS half
would have reported CANNOT JUDGE for all three. The generalization is one function
(`unit_shape`: `board.sexp` present → board; the vehicle route otherwise) consumed by
both the generator and the gate, with the census per shape (`shape_contracts`) and the
fragments carrying route-honest content — a device has no encoding space and pins no
reference models, and the bill SAYS so rather than omitting the chapters. The board's
pinned-specifications fragment enumerates the composition pins straight from
`board.sexp` — the definition's own data becomes the bill's specification surface.

Two measurement notes worth keeping: the pre-fix refusal was re-verified by running the
parent commit's generator from git (`git show <sha>:scripts/gen_model_book.py`), not by
trusting the code reading; and the processor books' regenerated fragments were proven
byte-identical modulo the embedded generator hash (`diff` with the Generator line
filtered — empty) before regeneration replaced them. The BREADTH report's stale "2
registered units" turned out to live in the GENERATOR's hardcoded prose, so the fix
landed there and the report regenerated (the GATE-REPORT drift gate would have refused
a hand edit — the derived surface was edited at its source).

Lesson: `promotion: declined` (recorded in the leaf) — derive-applicability-from-the-
declaration already has its decision records
(`decision_device-applicability-by-declared-vehicle`,
`decision_gate-applicability-by-declared-vehicle`); the regenerate-vs-edit and
verify-the-parent's-behaviour techniques are the house's standing rules.

## _(2026-10-02)_ — the second device dossier: content only, and the PDF text layer lies (P5-BOARD.10)

The LAN9118 dossier (`lan9118-lab-v0`) needed **no machinery edit** — the `.2`
by-declaration generalization was measured sufficient at the design brief, and the
measurement held: every gate derived the device route from the `vehicle` declaration on
first contact. The leaf's substance was the datasheet itself (109 pages; a real MAC+PHY,
not a UART): 52 mirrored records against the UART's 19, three indexing levels (direct
CSRs → MAC_CSR synchronizer → MII PHY bridge), and mirrors **generated** from
requirements.sexp (`target/gen_nic_mirrors.py`) so the 52/52/52 verbatim discipline is
impossible to break by hand — the gate would refuse drift anyway, but not hand-writing
it is the stronger guarantee.

The two extraction hazards, both measured and both now durable: (1) `pdftotext -layout`
and `-raw` **disagree on Table 5-1's Default column** (two-column pages scramble row
pairing) — per-register sections are the authority, and arithmetic cross-checks confirm
(TDFREE `1200h` = Table 5-3's 4608 B at the default split); (2) §3.11's "2 s"/"100 s"
reset times are **the PDF's own text layer mis-mapping µ to ASCII s** (hexdump-verified —
not an extraction drop), internally contradicted by §5.3.13's clean "100us" and §3.11.4's
own 100 ms bound. Only cleanly stated figures were pinned; the defect is recorded in
`REQ-D-NIC-RESETS`.

The composition findings are the leaf's sharpest output: FREE_RUN/GPT_CNT/INT_DEAS are
guest-readable time sources inside a device whose CPU contract excludes all of them
(`REQ-D-NIC-TIME-SOURCES` — frozen/deterministic, never wall-clock, never the retired-
instruction count; `.4` owns the verdict), and the PHY link scene under a recorded-trace
wire (`REQ-D-NIC-PHY-LINK`). The `profiles/` per-part bound bit for the first time
(32→64 KiB; `decision_profiles-family-five-units`).

Lesson: **promoted** — `docs/knowledge/a-pdf-text-layer-is-not-the-page.md` (the two
text-layer failure modes and the verify-with-hexdump rule).

## _(2026-10-02)_ — a device dossier reuses the machinery by declaration, and a datasheet's silences are requirements (P5-BOARD.2)

The first device unit (`sifive-uart-lab-v0`) taught the dossier machinery its third shape
(after generated-definition and sibling-crate): `vehicle (route device-model) (comparison
register-expectations)`. The load-bearing design choices:

**Applicability is derived, never exempted.** The instruction-shaped gates
(EXTRACTION, EXERCISE-COVERAGE, INTERACTION-MATRIX) read the `vehicle` declaration and
derive what applies: the device answers the legs it honestly can (every state element a
reset — the FIFOs' resets are recorded as *"unspecified", sourced to the measured silence*,
which satisfies the contract without inventing behaviour; every obligation a POS+NEG pair)
and the rest is n/a *by declaration* — with contradiction = RED in both directions (an
`encoding.sexp` or a `guests/` corpus beside the declaration refuses). Anti-drift by
construction: the day P5-BOARD.5's probes land, the gate refuses until taught the device
exercise leg.

**A datasheet's silence is a record, not an oversight.** Six of the nineteen requirements
are `unspecified`-category non-commitments — the sharpest found in execution: §13.8's
watermark bits carry a strict-inequality RAISED and a strict-inequality CLEARED condition
each, and the manual never says whether the bit is a pure level of FIFO occupancy or holds
between the two. The `==` boundary and every pre-first-condition value (including the
X-marked resets) are undetermined (`REQ-D-UART-WM-MODE`), so the expectation documents pin
a watermark bit only when its raised condition holds under *every* reading. The first
draft asserted "level conditions" — the dossier's own expected-results discipline caught
it before it ossified, exactly the failure EVD-05 exists to prevent.

**Naming is contract-shaped.** A private `REQ-U-` id prefix (for the unspecified records)
collided with RECORD-SCHEMA's mechanical `D-X` → `REQ-D-X` decision→requirement mapping —
the mapping is the contract, the prefix was convention. The records are now named by their
`source_semantics` category in prose and carry the house id shape; one fact, three
surfaces (requirement, obligation, decision), one wording, mechanically mirrored.

Validation: all dossier documents schema-validate; the three profile-glob gates decide the
device by declaration; every edited check's self-test green (17/9/14/41/7/14/10 arms, 0
fail); `make gate` all doctrines green; the mdBook builds and its index stays byte-exact.

## _(2026-10-02)_ — a board specification is data with its absences declared, and a label is not a source (P5-BOARD.1)

`netboard-lab-v0` is the first board and `schema/board.sexp` the first non-processor
source-of-truth schema. Two design decisions are worth the ink:

**An absence the contract depends on is data, not prose.** `rv64i-lab-env-v0` v0 admits no
guest-reachable time source and no asynchronous event — and both absences must be *platform*
properties to be real (the CPU contract's own lesson: excluding CSR instructions does not
exclude reading `mtime` over MMIO). So the schema gives `timers` and `interrupt-controller`
explicit `(present false)` forms carrying the reason and the obligation ids they satisfy;
an undocumented absence would read as an oversight, and an oversight is how a CLINT slips
in as a "feature" and becomes a `.4` composition rejection. The `satisfies` fields
pre-wire `scripts/discharge_assumptions.py`'s verdict without computing it — declaration
here, computation there.

**Verify the label against the artifact before you inherit it.** The design brief named the
serial device "16550-compatible (source SIFIVE-FU540-C000 v1p5)". A `pdftotext` census of
the pinned PDF: zero occurrences of "16550"; §13 is the SiFive UART (txdata/rxdata/txctrl/
rxctrl/ie/ip/div, 8-entry FIFOs, 32-bit-aligned only). The pin was the intent, the label
was wrong — so the board adopts the SiFive UART and the label is corrected at every record
(`materials/catalog.sexp`, `D-BOARD-UART-KIND`; the tree keeps the brief's original lines
with a dated correction, per the house pattern). Consequence that mattered: the UART's
sourced instance address (`0x1001_0000`, Table 58) collided with the pre-verification
sketch's NIC address — measuring first caught that too. Memory map: RAM 2 GiB at
`0x8000_0000` (the harness's existing DEFAULT_BASE/SIZE, so laboratory guests run
unchanged), UART at the FU540 instance address, the LAN9118 in a 256-byte window at
`0x1002_0000` (Table 5-1's direct-register span, offsets 0x00–0xFC).

Scope routing: registration of the board unit (`materials/units.sexp`, the `kind` edit,
the per-unit book) is deferred to `.3` — the registry admits a new kind "the day a real
unit needs one", and registration day carries UNIT-BOOKS / MATERIALS-BILL /
book-generator / BREADTH-prose consequences (all censused before deciding) that belong to
the materialization leaf, not to a specification. The third `profiles/` directory
re-derived the family bound to 3× by the standing arithmetic; nothing fired (142 < 240).

## _(2026-10-02)_ — the book's index is a function of the book, not a page someone keeps (BOOK-APPARATUS.1)

The director's apparatus directive audited against the real book: the glossary cannot fork
(`docs/book/src/glossary.md` splices the canonical `docs/GLOSSARY.md` at build time), the two
annexes already match the directive's definition — and the **index was absent**. It now exists
the only way this repository tolerates a fact about a changing population: derived.
`scripts/gen_book_index.py` reads `SUMMARY.md` (the chapter set, in reading order), the
canonical glossary plus the book's acronym table (the term set), and every chapter's text (the
occurrence set, case-insensitive and word-bounded); `scripts/check_book_index.sh` — the 31st
project doctrine, `BOOK-INDEX` — regenerates in memory and refuses drift, with six self-test
arms fired RED before registration (hand-edit DRIFT, stale-behind-edited-chapters DRIFT,
missing chapter and missing SUMMARY refused **by name**). The generator refuses what it cannot
emit rather than guessing, per house style. One build-exposed defect fixed at root: the
generator's printed term count was a fudge factor (`47` against the real `40`) — now derived
from the emitted rows. The annex policy is stated where a reader meets it
(`docs/book/src/introduction.md`): chapters stay readable top to bottom; what is too technical
for the main line lives in an annex. The directive's second half (incremental buildup, both
audiences engaged) became `decision_mdbook-incremental-engaging` + `BOOK-APPARATUS.2`; the TOC
request was withdrawn by the director — the mdBook sidebar is the TOC, and the contents page
built to satisfy it was reverted as redundant.

Validation: `gen_book_index.py` → 15,019 B / 40 terms; `mdbook build docs/book` rc 0;
`check_book_index.sh --self-test` 6/6; `check_doctrines.sh` all green.

## _(2026-10-01)_ — an answered channel still reads `open` until you flip it (P5-BOARD.9)

The second chipdoc incident, from our side: the acquisition agent answered all ten
P5-BOARD.8 requests (5 fulfilled, 5 measured negatives, chipdoc `542a14b`), and
semulith's `requests.sexp` kept saying `open` — because the seam is hard (chipdoc never
writes here) and only WE flip our own statuses. CHANNEL.md §0.3/§0.5 (re-read on the
director's pointer) closes exactly that gap: `catalog/responses.sexp` re-keys every
answer by OUR ids, and `build_responses.py --report` prints the join (run live before
any edit: 5/5, exit 0). The adoption kept the house rules: digests re-verified at
fetch, never trusted from the feed (`materials.py --verify` 52/0); the corpus re-pinned
with the same census (`c4ad8a2`, 5696/293); the proposals feed's records adopted
verbatim in our syntax. The five blocked answers are recorded as RESULTS — each names
what was tried, what returned, and the consequence (LAN9118 is the wired-NIC primary;
SARA-R4 the cellular primary; the AR9271 probe's negative IS its answer) — and the
channel's exactly-once rule means they are never re-filed without a new route. Two
knowledge cards covered the channel with overlapping, drifting scope; the refreshed
split is: `the-chipdoc-request-channel.md` owns the full ask→answer loop,
`the-chipdoc-channel.md` keeps the measured history and cross-links. `P5-BOARD.1`
inherits five sourced network-device candidates plus five closed alternatives.

Validation: `build_responses.py --report` exit 0; `materials.py --fetch` 5× sha256
verified; `materials.py --verify` 52/0; `make gate` all-doctrines-green.

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


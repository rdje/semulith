# DEV_NOTES.md

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

## _(2026-09-28)_ — the performance baseline: noise first, thresholds never (P1-LAB.11)

Root cause: gate `G1`'s fifth criterion and ARCHITECTURE §6's three benchmark modes had no instrument — every runner was correctness-oriented (`run_over` stops at the first trap, always records crossings: one fused mode), no allocation counting existed, and the zero-dependency rule (RUST-01) rules out the usual benchmarking crates, so the harness is ours. Implementation: `semulith-verify::bench` — programmatically generated mixes whose every word is decode-round-trip-pinned to the generated definition (the encoders are harness data, .9's standing); one counting environment wrapper makes the census comparable across modes without recording it; the instrumented runner is generic over `Observer`, so static-vs-dynamic is literally one function instantiated two ways, measured as two cells. The fault mix needed a stated harness policy: a delivered exception is observed and execution resumes at pc+4 (delivery-continues, ARCHITECTURE §5) — `run_over` could never drive it. Validation: 10 suites — decode round-trip for every word of every mix; per-mix census proving each mix exercises its own class (the misaligned pair never crosses the boundary; only the out-of-region ld faults at it); the pc+4 continuation pinned; four-mode agreement at test budgets; the allocator counting a known allocation (≥-assertions — sibling tests allocate concurrently); stats pinned on known inputs. Measured on the named host: untraced 47–54 ns/step; instrumented +24–40%; diagnostic +4–8% further; static/dyn ×0.974–1.002 — the parked dispatch question answered within noise. Noise spread 1.7–7.4% per cell, one 113% scheduler outlier; no threshold set (RUST-04).

Design notes, kept: (1) the measured modes share `run`'s snapshot/diff/trap-mapping/`Recording` as `pub(crate)` — a measured mode can never drift from the production observation construction it measures. (2) The executed word comes from the harness's own image, never a second fetch — a re-fetch would (correctly) count as extraneous in the census. (3) The first calibration run at iterations=1000 showed spreads up to 116% — millisecond-scale runs are scheduler-dominated; lifting the counter past addi's 12-bit range (lui+addiw pair) made 10000-iteration runs the default and the noise honest (1.7–7.4%). A benchmark whose runs are too short measures the OS, not the interpreter. (4) RUST-03's departure is now a number: exactly 1.00 allocation/step untraced (`extract_operands`' Vec) — recorded in the tree's Decisions for the milestone that needs it; P1's Non-Goals still exclude optimization.

Lessons: declined here (harness-policy shape and the image-word lookup are module-doc design notes; "a zero-cost assumption is a claim until measured" already lives in ARCHITECTURE §6; the short-run noise lesson is recorded above for this tree's readers and generalizes only when a second benchmark exists).

## _(2026-09-28)_ — replay and reduction: a result becomes an artifact (P1-LAB.10)

Root cause: `.8`/`.9` built the vocabulary, the comparator, and the mutation seam, but a result was never *recorded* — G-REPLAY's "reproduce from recorded definitions, tools, inputs, and event choices" had no definitions-and-inputs carrier, so gate `G1`'s "failures are replayable" and T007's "replay/reduction preserves mismatch" were claims without artifacts. Implementation: `semulith-verify::replay` — the `Bundle` flattens `definition::MANIFEST` into the algorithm block (the OWN-03 pins become the algorithm/version accompaniment; the harness version and `production`/`mutant:<name>` model complete the tool identity), carries the platform/entry/image-with-sha256/events/budget, and records the steps + the stop's canonical render; `replay()` checks identity by name — pins against the live manifest both directions, then the image digest against the bundle's own words — and walks recorded-vs-replayed through `run::compare`, so drift is named at the first differing observation rather than summarised. The stop is compared rendered, not re-typed: `Failed`/`Undefined` stops carry data no JSON round-trip could rebuild, and the render is deterministic — nothing is lost. `semulith-verify::reduce` — ddmin over the word sequence (ILEN 32 ⇒ one word = one observation step), retention = the original first divergence exactly (same `at`, same `what`); the strictness is free and load-bearing — a same-step retained divergence is byte-identical because the executed prefix is unchanged, and a removal that shifts the symptom is a different bug wearing the original's clothes. The accepted-removal invariant makes retention structural: the result cannot fail to retain. Validation: 15 replay suites (all four guests replay identically under production + the zext-addi mutant; tamper arms — image, entry, region, budget, generator pin, input pin, dropped pin, scripted event claim, missing accompaniment — each refused or named-mismatched; empty-run replay) and 6 reduce suites (three prefix minimizations with exhaustive 1-minimality witnesses — the witness loop re-runs the property on every single deletion; phantom-load refused `NoDivergence`; clean model refused). CLI exercised end to end.

Design notes, kept: (1) the bare-seed refusal is structural — `Bundle::parse` names the missing field, so "a seed accompanied by algorithm/version and event choices" is a property of the format, not a policy a reader could waive. (2) One test-expectation bug was caught by the suite itself: I first asserted the jalr-odd-bit case minimizes to the 11-word prefix by counting the divergence at "step 10 = word 10"; step 10 executes word *8* (the loop revisits words 1–2), and the first-divergence walk never reaches the words behind the trapping jalr — the true minimum is 9 words. A retention predicate defined on the comparator's own verdict, not on my hand-traced indices, is what made the suite able to correct its author. (3) `InsnDef` is not `Clone` (the `.9` suite copies rows by struct-update syntax — every field is `Copy` but the struct declares no derives), so the table copy follows the same idiom rather than adding a derive to the generated module.

Lessons: declined here (the retention-invariant and the structural bare-seed refusal are recorded in the module docs; the census-class-not-reducible boundary is the `.9` lesson reused at a new surface, which is itself the pattern — a detector's jurisdictions stay named as they grow).

## _(2026-09-28)_ — the validator mutation suite: a differential that is known to disagree (P1-LAB.9)

EVD-09's demand after `.8`: the differential had only ever agreed. The fix is one parameter, not a feature: `exec::step_over` / `run::run_over` take the instruction table (production delegates with `INSNS`; the scan is pinned to the generated `decode`), and `semulith-verify::mutate` swaps one row — a mutated effect tree rebuilt from the real one, or a mask/value row — so a wrong model is *data the one evaluator consumes* (OWN-01). Where a wrong behaviour can only exist as harness code (deferred traps, fabricated substitutions, stale configs), the arm mutates the observation stream and says so. Eleven arms: the eight designated classes plus the JALR odd-bit arm the fixture note names (fault at 0x80000029, as predicted), the four-guest crossing census, and the writes-blind suppression exhibit. Every guest arm re-derives the pinned expectations against the real model before judging the mutant. `.1`–`.8` checklists archive to `docs/tasks/archive/P1-LAB.md` — per-part ceiling obeyed, not raised.


Every dated entry here must reach the retrievable layer: a card under
[`docs/knowledge/`](docs/knowledge/INDEX.md), or a decision record, or an explicit decline in
the owning task leaf. That is the `LESSON-PROMOTION` doctrine, and the reason for it is that a
lesson nobody can retrieve by question is a lesson nobody has.

## _(2026-09-28)_ — the first execution slice: the definition executes, and agrees with two references (P1-LAB.8)

Root cause: `.6` had lowered the semantics into `Sem` trees and pinned "evaluation stays with `.8`" — the evaluator existed nowhere, and the one design point the tracked documents genuinely did not pin was the width algebra: `check_semantics.py` checks well-formedness, completeness and citations only, so what `sext N` MEANS operationally was undefined. Two candidate readings each fail half the corpus ("extend the low N bits" zero-extends LB; "extend from N bits" identity-extends LUI); the unique reading under which all 52 trees are simultaneously correct is extend-FROM-the-operand's-own-width-TO-N, with literal shifts widening the result (LUI's `shl` assembles a 32-bit constant) and computed shifts operating at the left operand's width — the rule that makes `sraiw` replicate bit 31 rather than bit 63. Implementation: `semulith-core::exec` evaluates the generated trees (no handwritten per-instruction behavior exists anywhere); `semulith-verify::run` records `(pc, word, register writes, trap)` steps — the same vocabulary `compare_traces.py` reduces the references to — plus the full boundary-crossing log, and `compare` reports the first divergence naming the differing field (a register, the trap cause, the tval, a missing write; a length mismatch is a non-agreement, never a prefix pass); `semulith-verify::elf` loads the writer's ELF64 with named-field refusals; `guests.rs` is generated from the tracked guests + EVD-05 expectations (`gen_guests.py`, GUEST-GEN — fired RED on a hand-edited fixture before registration). Validation: the offline differential runs all four guests against the generated fixture on every `make check` (77 verify suites green); the live experiment `scripts/run_semulith_smoke.py` agrees with sail-riscv AND spike on every enabled comparison — 34 aligned steps, byte-identical reproduction.

Design notes, kept: (1) fetch faults record NO step — a failed fetch supplies no word, and inventing one would put a fiction in the comparison vocabulary (fetch-fault comparison against the references is future work, recorded in `Stop::FetchFault`). (2) The generated fixture needed `#[rustfmt::skip]` on every data array: rustfmt packs scalar/struct arrays horizontally, so byte-stable emission means freezing the layout, the same "fmt-stable emission" discipline `.3`/`.6` already carried. (3) The runner observes register writes by state diff, so a write to x0 can never appear — the architecture's own rule, obtained for free. (4) The misaligned access is raised before the boundary is crossed, and the crossing log proves it: the request log shows the environment never saw the access.

Lessons: declined here — the width-algebra decision is recorded in the `.8` leaf's Decisions and the `exec` module docs (it is P1-LAB-evaluation specific); "cited ≠ verified" already has its card (`docs/knowledge/re-derivable-vs-cited-evidence.md`) and the shorter-trace rule has `docs/knowledge/a-shorter-trace-is-not-agreement.md` — this slice is their worked example at model scale, not a new lesson.

## _(2026-09-28)_ — the graph and report checker, and the citation that became a derivation (P1-LAB.7)

Root cause: the planning package's schema check results lived only in its delivered document — "All 5 records validate", "All 6 rejected", "fingerprint matches" were citations of Python `jsonschema` 4.26.0, and nothing in the workspace could re-derive them (RUST-01's production-modeling rule had no production evidence machinery). Implementation: five dependency-free modules in `semulith-verify` — `json` (a reader holding `json.loads` parity: last-wins duplicate keys, the int/float distinction Python blurs with `bool`), `pattern` (a regex subset implementing exactly the two constructs census the tracked schemas use, refusing groups/alternation/`.` by name), `sha256` (FIPS 180-4, known-answer pinned), `schema` (the Python validator's keyword subset and refusal discipline; two tightenings — array `type` and schema-valued `additionalProperties`, the latter silently skipped by the Python tool — verdicts proven unchanged on the frozen corpus), and `graph` (the §3 invariants: orphan links, scope, unique ids, cycles, unpinned sources, artifact hashes, missing evidence, gate policy). The library takes evidence bytes through an injected resolver — no `std::fs` — so PORT-WEB holds by construction; filesystem access lives in the CLI command and the tests. `semulith check-examples` presents the report; RECORD-SCHEMA runs the Rust engine after the Python phase and fired RED on a mutated requirement (`EV-GHOST` → ORPHAN-EVIDENCE, rc=1) before landing. Validation: 59 verify suites green (16 graph suites: 3 PACKAGE_CHECKS re-derivations, the intact-bundle verdict, and one mutation per designated rejection plus a fully-met `passed` control); `make check` clean at `-D warnings`; wasm build green; gate green.

Design notes, kept: (1) verdict honesty is a type, not a string — `GateStatus::{Passed, Incomplete, Failed}` with `Incomplete` the expected state of the `planned` fixture, so "the checker says pass" has exactly one typed expression and the fixture cannot reach it by accident. (2) The acceptance's "rejects X" clauses are proven by mutations that must be caught — a suite never run against a broken bundle is not known to detect anything, the same rule `.9` applies to the model. (3) `uniqueItems` distinguishes `Int(1)` from `Float(1.0)` while `enum`/`const` compare across the boundary — Python's two different equalities, kept as data rather than "fixed".

Lessons: declined here (checker-specific design notes; the resolver-injection pattern for wasm-pure libraries is stated in the module docs where the next pure crate meets it).

## _(2026-09-28)_ — DEV_NOTES joins the shard family, and a lying header is a defect (DOC-SHARDING.2)

Root cause this leaf closes: `DEV_NOTES.md` stood at 49,145 of its 49,152-byte ceiling with the remedy unbuilt — `.1`'s sharder, manifest and freeze check were all scoped to `CHANGELOG.md`, so the only responses were compression or this leaf. Implementation: generalization, not a fork — `scripts/shard_history.py` takes the registry ceiling per head and writes a shard header that names the head it was cut from and that head's own ceiling (`# DEV_NOTES shard … crossed its 48 KiB ceiling`; CHANGELOG keeps its byte-identical `.1` shape, asserted); `scripts/check_changelog_shards.sh` learns the two-head family — one partition scan over both live heads + shards, so an entry heading carried twice anywhere fails, with a fired RED probe (a scratch shard holding a live DEV_NOTES heading) recorded in the leaf. First event: 2 entries into `docs/changelog/shard-0027.md`, head 48,954 → 46,212, `31 == 29 kept + 2 moved` proved at the event, 29-row manifest frozen. Validation: sharder self-test 12/0 (two new arms), SHARD-FREEZE self-test 14/0 (two new arms), real-tree RED probes for both tools, gate green.

Defects found and fixed, same slice: (1) the registry comment on `docs/changelog/` claimed DEV_NOTES was "sharded from 2026-09-27" — designed end-state stated as present fact; corrected with the fix cited. (2) Two stray duplicate headings inside `DEV_NOTES.md` (a heading line repeated with no body, one above MODEL-COMPOSE.3's entry and one above SOT-FORMAT.6's) — the new two-head UNIQUE leg found them within a minute of first running; the old leg never looked at DEV_NOTES.md. Both removed; the entries themselves exist exactly once.

Lessons: declined here (the probe-discipline lesson — pass `--root` explicitly when probing path-aware tools; a default derived from `git rev-parse` reached the REAL repository mid-probe and the tool's own refusal was the only thing that prevented it writing into `docs/changelog/` — is stated in this entry, which is where anyone running shard probes meets it).

## _(2026-09-28)_ — the canonical definition, generated (P1-LAB.6)

Root cause: the definition was checkable but not consumable — SEMANTICS proved 52/52 cited, but no executable artifact carried the facts and OWN-03's manifest existed nowhere. Implementation: `scripts/gen_definition.py` generates `crates/semulith-core/src/definition.rs` from the encoding composition plus the semantics data: `FIELDS` with scatters, 52 `INSNS` decode rows, `Sem` effect trees, `decode`, and `MANIFEST` (inputs+sha256, generator hash, configuration as data, upstream source pins); the generator re-derives the SEMANTICS checks it emits through and refuses unknown shapes by name. The 22nd doctrine `DEF-GEN` refuses drift; self-test 8/0, fired RED. Validation: 10 definition suites green; clippy clean; wasm green; gate green (22 doctrines / 245 arms). Kept: emit effect trees fully broken per line so generator shape and rustfmt's agree (drift compares content, never formatting); an unjudgeable input must refuse (rc=2), not report a verdict — the RED-firing rite caught `relative_to` crashing on a relative `--encoding`.

Lessons: declined (generation specifics).

## _(2026-09-27)_ — four typed outcome families, SEM-01 made structural (P1-LAB.5)

Root cause: SEM-01's separation lived only in `RULES.md`; the laboratory could report a contract violation (`.4`) but had no type for a trap, a stop, a gap, or a reserved word — and a single error enum is the classic way that distinction dies. Implementation: `semulith-core::outcome` — the four families as enums with named, source-linked variants, `StepOutcome` the step-level sum, and `From<env::ContractViolation> for ModelError` the one legal crossing (a harness violation IS a model error). No other `From` between families exists, on purpose. Validation: 5 suites green; clippy -D warnings clean; wasm green; gate green. Design notes, kept: (1) the acceptance's "delivered and execution continue" is a property of the HARNESS composition, so the test owns a stub stepper — production semantics stay with `.8`. (2) ExceptionCause carries no cause *numbers* — this profile models no privileged CSR to hold them, and inventing numbers would be a second fact.

Lessons: declined here (the family shapes are `.8`'s design consumer; nothing generalizes past this module).

## _(2026-09-27)_ — the environment boundary, and fixtures that answer it (P1-LAB.4)

Root cause: `rv64i-lab-env-v0` named a boundary (fetch supply, widths, address space, misalignment) but no Rust type could express a crossing — `docs/CPU_ENVIRONMENT.md` §4.1's "testable independently of the CPU instruction handler" had no request to test. Implementation: `semulith-core::env` — `Request`/`Response`/`Failure`/`ContractViolation`/`Environment`, with the width set pinned by construction (fetch carries no width at all; a fifth load/store width cannot be formed, which is stronger than refusing one) and the two failure families distinct by type (SEM-01 in embryo — `.5` re-homes `ContractViolation` into `ModelError`). `semulith-verify::fixtures` — `FlatMemory` (u128 region checks, LE assembly by hand loop, fetch counter, alignment-before-region order stated on the method) and `ScriptedEnv` (scripted faults as environment answers; uncovered requests are violations, never invented data). Validation: 16 suites green; clippy -D warnings clean; wasm build green; gate green. Design notes, kept: (1) the fixture must surface test bugs loudly (load_image panics on a mis-sized image) — a fixture that modeled test bugs would teach tests to expect wrongness. (2) No asynchronous event exists to script — the platform declares none, and an absence has to be a platform property to be real (OB-ENV-EVENT-DELIVERY).

Lessons: declined here (fixture specifics live in the module docs; the boundary's SEM-01 typing is `.5`'s design result, not this slice's lesson).

## _(2026-09-27)_ — architectural state, generated from the descriptor (P1-LAB.3)

Root cause: the state accessors of `docs/ARCHITECTURE.md` §2 existed only as a table row; the descriptor `state.sexp` had no executable half, and the C02 alias question had no code to answer it. Implementation: `scripts/gen_state.py` derives `crates/semulith-core/src/state.rs` from the descriptor via `dossier_sexp.load_state`, emitting fixed-width storage (`[u64; 32]` + pc, 264 bytes inline, RUST-03), the x0 hardwired discipline (write discarded, read masks to 0), the three ISA-chapter-named aliases as views over the one storage, the inspection-metadata table (`ELEMENTS`), and the SEM-08 census as data. Byte-deterministic; the input sha256 rides in the header. The `STATE-GEN` doctrine (`scripts/check_state_gen.sh`) regenerates in memory and refuses drift; self-test 6 pass / 0 fail; fired RED on a hand-edited module (rc=1, naming DRIFT) before registration. Validation: 22 suites green; clippy -D warnings clean; wasm build green; REGISTRY-MIRROR and FACT-OWNERSHIP re-run green after registration. Design notes, kept: (1) generated Rust must be emitted formatter-stable or the drift gate fights `cargo fmt` — the generator's output is the formatted shape, verified by regen-diff after `cargo fmt --all`. (2) `dossier_sexp.family_for` names the dossier family from the file NAME, so self-test descriptor surgery must keep the `state.sexp` basename (per-case directories). (3) The generator binds the descriptor's `xlen` to `arith::XLEN` at generation time — the executable owner of XLEN stays unique, and a descriptor/code disagreement is a refusal, not a choice.

Lessons: declined here (all three notes are P1-LAB-generation specifics; nothing here generalizes past `.6`, where the generation manifest lands).

## _(2026-09-27)_ — target arithmetic primitives, and the width-sensitivity trap (P1-LAB.2)

Implementation: `semulith-core::arith`, one function per semantics-data operation, contracts written to SEM-03 (width/signedness/intermediate precision/truncation/exceptional behavior per function), source links as doc comments naming requirement ids + pinned locators. The first code content in the workspace. Validation: 12 test suites — boundary at XLEN, 8-bit-exhaustive against different-host-width references (multiply-as-shift, De Morgan), 100k-draw word-op sweep; clippy -D warnings clean; gate green. Design notes, kept: (1) the exhaustive layer caught the signed-op width-sensitivity trap on its first run — `slt`/`sar` compared against an `i8` reference without embedding the signed view at XLEN; the primitives were right, the test was wrong, and the trap is now a knowledge card. (2) Unmasked shift amounts panic via `debug_assert` rather than silently wrapping — a decoder bug must not produce a plausible-looking wrong result; the masking rule lives in `shamt64`/`shamt32` next to the REQ-D-SHAMT citation. (3) `implementation_status` on the requirements stays `planned` until the interpreter can exercise instruction-level obligations — do not inflate status to match enthusiasm.

Lessons: promoted to `docs/knowledge/reduced-width-verification-of-signed-ops.md` (the width-sensitivity rule and the per-operation table).

## _(2026-09-27)_ — the laboratory crates and the Wasm gate (P1-LAB.1, PORT-WEB.1)

Root cause: the crate boundary was a `docs/ARCHITECTURE.md` §4 table with no crates behind it, and the browser target was a decision with no instrument. Implementation: three crates with one-directional edges (`cli → {core, verify}`, `verify → core`, `core →` nothing — the wiring IS the deliverable at `.1`; behaviour stays with its owning leaf); `scripts/check_wasm_build.sh` registered as the `PORT-WEB` doctrine — preflight refuses when the rustup target is absent (exit 2), the 4-arm self-test re-runs before every judgement, the verdict is a plain `cargo build --workspace --target wasm32-unknown-unknown`. Validation: `make check` green (5 suites, 0 warnings at `-D warnings`); self-test 4 pass / 0 fail; fired RED on a real `std::os::unix` import (rc=1, naming `lib.rs:13`); `make gate` green after registration. Design notes, kept: (1) the self-test caught my own first cut — bin crates want `src/main.rs`, not `src/bin.rs`, and cargo fails builds with rc=101, not 1; a control never run RED is not known to work. (2) Scratch builds pass `--target-dir` inside the temp dir — the measured family defect is self-test state leaking into the real run through environment variables.

Lessons: declined here (both notes are recorded in the PORT-WEB.1 leaf checklist).

## _(2026-09-27)_ — the sanctioned watcher is a ruling, not a false positive (ARTIFACT-CLEANUP.2)

The director ruled CHIPDOC's ChipdocWatcher stays, and the census stopped crying wolf the
honest way: the exemption is a RULING in data (doctrine/sanctioned_processes.tsv), not a
vocabulary in detection — the pattern-free census is untouched, and only director-ruled
standing processes skip it. Design note worth keeping: a detection list and an exemption list
are different shapes of the same text file; the difference is WHO adds a row and WHY (an agent
proposes, the director disposes, the ruling is quoted). Verified both directions: handoff OK
with PID 36462 alive; the row absent -> the same process flags.

Lessons: declined here (the propose-vs-dispose discipline is stated in the registry header).

## _(2026-09-27)_ — no coding without the source of truth, mechanized (MODEL-METHOD.6)

Root cause this leaf closes: the rule was the director's prose and nothing enforced it. The
design turn: the census already said which categories are missing, but 'missing' alone cannot
block coding — the excluded subsystems (C07/C08/...) are missing and must stay legal. The gate
needs the scope to DECLARE what it requires; the registry gained (requires …) and the refusal
keys on required × missing. rv64i-lab-v0 declares its 14 in-scope categories; the six
excluded ones stay legal because they are not required.

Composed, not duplicated: SCOPE-COVERAGE says the facts are OWNED; EXTRACTION says they are
EXTRACTABLE; both must pass before P1-LAB writes code. MODEL-METHOD closes 13/13 — the
method, the census, the acquisitions, and the coding gate all landed in one session.

Validation: gate 7/0; real run '1 unit(s) may code'; RED fired pre-registration; whole
enforcer green (19 doctrines, 227 arms).

Lessons: declined here (the OWN-vs-EXTRACT composition rule is stated in the gate's header).

## _(2026-09-27)_ — the method, in prose, written to be learned from (MODEL-METHOD.5)

Root cause this leaf closes: the method existed only as the history of its exercise — eleven
leaves of it — and a method that lives only in its own history cannot be learned from. The
document is written against what the session actually did, with the rejections kept, and it
names the four judgement calls (publication, class, authority, disagreement classification)
rather than letting them look like mechanics.

The acceptance probe worth keeping: the body of docs/METHOD.md references no project-owned
tool, path, or id outside the worked example — the carryability claim is checked, not
asserted. The mdBook carries the document verbatim, the house pattern for every source doc.

Lessons: declined here (the framing is the document's own closing section).

## _(2026-09-27)_ — the run-real-code set is acquired, and the PDF question is answered (MODEL-METHOD.4)

Root cause this leaf closes: the census (" + bt + ".3" + bt + ") named the run-real-code set as the
reachable acquisition, and nothing pinned it. Four fetches, four digests, one cache, one
answered question.

Design choices, stated — the home problem consumed the design time, and the answer is worth
keeping: every natural home refused these documents for a MEASURED reason. The profile's
sources.sexp composes base_url/file (one origin; this set is four); the materials catalogue's
fetch seam copies from an $ENV-rooted corpus (no URL kind); docs/provenance manifests list
tracked bytes (third-party documents are not redistributed — the same doctrine that keeps
.materials/ gitignored). So the tracked record is the leaf's digest table plus the cache
README, and a materials.py URL kind is the named candidate only if a second web set arrives.
Two pins are branch-pinned (master/main) — the digest is the protection; locator-stable pins
are P1-LAB's refinement.

The PDF question answered YES with extraction evidence (funct7/rs2/rs1/funct3 as clean text
cells; 1.96 MB extract). SRC-02: the v20260120-tagged release asset was not found (three
release pages searched); chipdoc unavailable here.

Validation: every cached copy re-hashed to the recorded digest; content sanity per document;
RECORD-SCHEMA green on the revised C20 census row; whole gate green.

Lessons: declined here (the home-selection reasoning is stated in the leaf, where the next
acquisition meets it).

## _(2026-09-27)_ — the census sweeps the snapshot, and missing changes its meaning (MODEL-METHOD.3)

Root cause this leaf closes: the .2 first pass wrote dispositions from the profile's
exclusions, and four of its reasons asserted material absence nobody had checked. The census
evidenced every covered row against the cached snapshot and corrected the mistake the
evidence revealed: the excluded subsystems' chapters are IN the snapshot — a-st-ext, rvwmo,
v-st-ext, f/d/q-st-ext, counters, zicsr, zifencei. So `missing` means the profile excludes
the subsystem (the facts are not part of this unit's model), not that the material is absent.
That flip matters downstream: .4's acquisition list is now honestly short — the run-real-code
set and the privileged/debug VOLUMES, not chapters the snapshot already carries.

Design choices, stated: `deferred-to-board` is a new disposition value (zero kernel lines)
because device and interconnect categories are P5-BOARD's to own, and the CPU records an
environment assumption in their place — the leaf's own rule. RECORD-SCHEMA rule 12 keeps every
named material resolvable against catalog.sexp, so a covered-by that names a document nobody
acquired is refused like an unpinned citation. The census counts: 10 covered, 4 partial, 6
missing (closers named), 3 deferred-to-board, 1 out-of-scope (C17 — contract-owned).

Validation: the page-level sweep (each covered category's subject found in its pinned page);
RECORD-SCHEMA 33/0 (was 32) + real run green; whole gate green.

Lessons: declined here (the excluded-vs-absent distinction is stated in the catalogue header
and the owning leaf).

## _(2026-09-27)_ — the materials requirement: what each unit owes its model (MODEL-METHOD.2)

Root cause this leaf closes: the materials side recorded documents (who/what/where) but
nothing recorded what information a unit OWES its model — no category-to-material binding, no
unit registry, no layer. The fix walks the .3 path a third time: schema declares, the mapping
owner carries, RECORD-SCHEMA gates.

Design choices, stated: the disposition vocabulary is the point — `missing` means the unit
REQUIRES the category (a reason is owed), `out-of-scope` means it never owed it, and the
acceptance's rule is the mechanical form of that honesty (a board-layer `missing` for a
processor is a lie about what was required). The unit registry keys the layer rule: layer
claims without a registry prove nothing, so the gate refuses those too. The duplicate-id arm
grew a per-family key — category-need records have no `id`; they key on (category, unit),
and the first cut that assumed `id` reported every need as a duplicate of None. The
`dict_to_form` dispatch also had to move its specific keys first: units and
category-needs both carry a `kind` field, which collided with the requirement
branch until `book`/`disposition` dispatched first — a measured,
not hypothetical, ordering constraint.

Validation: RECORD-SCHEMA 32/0 (was 26); 7 record files green; the 24-row first honest pass
(8 covered, 6 missing-with-reason, 4 partial, 6 out-of-scope). The .3 census revises
dispositions against evidence from here.

Lessons: declined here (the ABSENT-vs-NEVER-NEEDED vocabulary is stated in the schema header
and the owning leaf).

## _(2026-09-27)_ — the no-duplicated-fact rule is a registry, and every mirror is governed (MODEL-METHOD.7)

Root cause this leaf closes: the no-duplicated-fact rule lived only in
`decision_canonical-definition-input` prose, while the corpus it governs had grown
derived mirrors — and one of them (28 obligations restating their requirement's statement,
measured) had NO governor at all. The fix is shaped like the routes registry beside which it
lives: `doctrine/fact_ownership.tsv` names one owner per fact kind, each legal mirror, and
the governing doctrine; the FACT-OWNERSHIP gate verifies the registry holds AND is complete
against the corpus's actual restatement pairs — a completeness claim needs a census, so the
four real pairs are enumerated in the gate.

Design choices, stated: the registry's mirror column means "a file that restates the owner's
fact" — direction matters, and getting it uniform (owner owns; mirror derives) took one
measured failure (the encoding pair's family prefix did not match one way; symmetric
directory-prefix matching fixed it). The governor belongs in the family gate, not the
registry: RECORD-SCHEMA rule 9 keys on the obligation's own `requirement_id` (the 8
environment-assumptions keep their own statements — the arm keys on the parameter, not the
direction).

Validation: RECORD-SCHEMA 26/0 (was 23) + real run green on the 28 real mirrors; gate 8/0;
both acceptance shapes fired. Whole enforcer green.

Lessons: declined here (the govern-every-mirror rule is stated in the gate's header and the
owning leaf).

## _(2026-09-27)_ — the extraction contract: one set, four ways (MODEL-METHOD.10)

Root cause this leaf closes: every per-family check proved its own leg, and nothing proved
the legs described the SAME instruction set. Measured pre-code: no requirement↔instruction
link existed, and the ALU family (13 instructions) had no requirement at all — the contract
as stated failed the real corpus on the requirement leg.

The fix is two-handed, and both halves matter. Corpus: `(insns …)` on the schema
(kind-agnostic — a memory-kind requirement names FENCE, an event-kind names ECALL and
EBREAK), two new D/REQ/OB triples whose statements are grounded in the corpus's own
semantics (the §1.1.4 effects, including SLTIU's sign-then-unsigned quirk — the statements
must match the decisions exactly, `RECORD-SCHEMA` rule 4, and the semantic file is the
corpus's own authority for what the spec says). Tool: `check_extraction.py` requires
SCOPE == ENCODING == SEMANTICS == REQUIREMENTS — one set, four ways — plus resets and
checks. Gating: `EXTRACTION` (17th doctrine), because P1-LAB must cite a verdict that
runs.

Measured en route: `RECORD-SCHEMA` caught a wrong obligation id (`OB-D-ALU-REG`
vs `OB-ALU-REG`) mid-curation — a gate earning its keep on the authoring side, not just
the review side. And `R.dump` drops file headers: a load→modify→dump rewrite must
re-prepend the `;;` header or the diff shows comment loss. The curation script now
does, and the diff is minimal (11 insns additions + 2+2+2 new records).

Validation: tool 6/0, gate 3/0; real corpus SUFFICIENT; the acceptance's RED on a copy with
one sem rule removed (`does not cover: add`). REGRESSION: RECORD-SCHEMA 23/0,
PROFILE-CONSISTENCY 39/0, GATE-REPORT re-derived 28/28/36/72, whole gate green.

Lessons: declined here (the integrative-pattern rule is stated in the tool's docstring and
the owning leaf).

## _(2026-09-27)_ — a composition is an ordinary unit, and the tree closes (MODEL-COMPOSE.5)

Root cause this leaf closes: composition produced verdicts (encoding union, record merge,
assumption/guarantee discharge, slots, refinement) but nothing produced a UNIT from them —
`computer -> board -> soc -> {cpu, device}` had one record shape at level one and no shape at
all above it. The fix is deliberately boring: `compose_units.py` merges the parts with
`merge_units(…)` — the same code, no fork — and writes an ordinary unit directory through the
single mapping owners. Boring is the point: the acceptance is that a two-level composition is
checked by the same code as a one-level one, and the way to get that is to not write new check
code at all.

Design choices, stated: part paths resolve against the manifest's own directory (the way
fragment-root resolves against its document); provenance is kept, not rewritten — merged
records keep their origin units' `profile_ids`, the board overwrites only the encoding
document's own identity field; exactly one ISA-carrying part (two is a multiprocessor — the
address-space operator stays refused-until-earned); no new doctrine gate, because the derived
files are ordinary corpus covered by the existing gates wherever they land. The tracked-board
freshness proof (manifest -> derived bytes, the gen_fragments precedent) is the first tracked
board's job, named in the leaf.

Measured en route: the first implementation read only the first `(part …)` child of the
manifest — every multi-part composition silently halved. The self-test's census arm caught it
(2 obligations where 3 were owed). A census that counts is the cheapest oracle there is.

Validation: `--self-test` 9/0; real corpus board through unmodified `merge_records`,
`discharge_assumptions`, and the encoding read path (26/34/3 + 52 instructions). Regression:
whole guard set green.

Lessons: declined here (the materialize-then-stay-ordinary rule is stated in the tool's
docstring and the owning leaf).

## _(2026-09-27)_ — a silent override is refused, and the execution authority gets its gate (MODEL-COMPOSE.6)

Root cause this leaf closes: two measurements, one design. (1) The refinement edge had no
vocabulary — nothing in `schema/semantics.sexp` could declare "this extension changes that
base behaviour", so a silent override was indistinguishable from a composed corpus. (2) The two
tools that judge the semantics corpus — `check_semantics.py` (well-formed, complete, cited)
and `check_citations.py` (52/52 locators resolve) — were invoked by NOTHING in the gate set;
the corpus the engine will execute was healthy only when someone ran them by hand. The third
orphan of the family `MODEL-COMPOSE.4` closed for encodings — the same probe, the same
shape, the same fix: wire the capability into the gate set or watch it rot.

Design choices, stated: the declaration lives on the AUTHORED side (the `.sem.sexp` files),
never in the generated fragments — generated and hand-derived content have different provenance
and must not share a file, the `rv64i.sem.sexp` header's own rule. The compose mode
schema-validates each file first and refuses a violating FILE as a rejection (rc=1), reserving
rc=2 for a broken language. The citation arm NAMED-SKIPs when neither the fetched area nor the
manifest-verified cache exists — a check that cannot judge never reports green.

Validation: tool `--self-test` 8/0 (declared refinement accepted; silent/double/lie/arity/schema
arms each naming their reason); gate `--self-test` 7/0; real run `ok (3 check(s))` with
52/52 citations inside the gate for the first time; the acceptance's RED on a real-shaped
composition. Per-fragment mode byte-stable.

Lessons: declined here (the "orphaned tool" pattern is now demonstrated three times; a knowledge
card is due on a FOURTH instance — that is the threshold, stated so the count is honest).

## _(2026-09-27)_ — slots are data, and the unit's union is decided again (MODEL-COMPOSE.4)

Root cause this leaf closes: two substrate defects found by probe before any code. (1) Since
`MODEL-COMPOSE.2` moved instructions into fragments, NOTHING decided the unit's composed
encoding space — the disjointness checker read compositions its own way, could no longer read a
unit's `encoding.sexp` at all (probe: REFUSED, "yielded no instructions"), and no gate
invoked the tool on the unit's fragments. (2) The checker never schema-validated its input — a
planted `(widget "x")` in a real `compose` passed silently. A slot verdict on a
document nobody validates, over a union nobody decided, would be a claim without legs.

The fix, in order: data first (`(status …)` and `(slot …)` in `schema/encoding.sexp`,
zero kernel lines); then ONE resolver — `riscv_asm.resolve_composition(…)` extracted and
shared by the assembler and the checker (a second hand-written resolver is how the `.2`
regression happened); then the checker validates the document and each resolved fragment against
the schema layer before unioning; then `UNIT-COMPOSITION` (15th doctrine) wires the
verdict into the gate set — a restored capability that no gate invokes is the defect restated.

⭐ Two more latent bugs of the same family surfaced in the resolver while testing:
`children(…, "extensions")[0]` and `children(…, "requires")[0]` index a
first child the 0-or-more grammar does not guarantee — absence is schema-legal; the corpus
always writes the markers, so both IndexErrors were live but unfired. The self-test's fixtures
omit the markers and prove the paths. The `.2` precedent as no-regression proof: the
resolver is refactored, not rewritten — `run_smoke` ok, nothing observable moved.

Lessons: declined here (the "capability without a re-runner" lesson is stated in the gate's
header, where anyone restoring a capability meets it).

## _(2026-09-27)_ — assumption/guarantee discharge is a verdict (MODEL-COMPOSE.3)

Root cause this leaf closes: a conditional composition claim ("the CPU is validated under
explicit environment assumptions") is only as strong as the demonstration that the assumptions
hold — and the demonstration lived only in `docs/CPU_ENVIRONMENT.md` §5 prose. The
design insight, measured before any code: the discharge edge already exists in the corpus as
obligation dependencies — `SOT-FORMAT.5`'s census showed all 8 environment-assumptions
depending on `cpu-guarantee` obligations. The operator's job was to make that edge a
verdict, not to invent it.

The rule: an assumption is discharged when every dependency resolves in the `merge_units(…)`
union to an obligation whose direction is a guarantee — keying on "not environment-assumption"
so a future device-guarantee value is accepted by construction (the vocabulary extension is
deliberately not this leaf; it is a `(values …)` data change the day a real device
unit exists). Refusals: the missing guarantee fires in the union's closure (`DANGLING DEP`)
— where the acceptance's RED lands is recorded honestly, not re-implemented — while a chain
(demand → demand, `UNDISCHARGED CHAIN`) and a zero-dependency assumption (`UNDISCHARGEABLE`)
are the discharge-specific refusals. Complement stated in the tool: an unclaimed guarantee is
not an error.

Validation: `discharge_assumptions.py --self-test` 6/0; real corpus 8/8 with every edge
printed; cross-unit discharge (a unit carrying only `OB-ENTRY-STATE`); guarantee removed →
rejected naming it, from both the assumption and the requirement side. Regression: merge 18/0,
SOURCE-FORMAT 7/0, sexp 18/0, kernel 50/0, RECORD-SCHEMA 23/0, semantics 52/52, citations
52/52, materials 20/0, smoke ok, readers 28/28; whole gate green.

Lessons: declined here (the "new direction values accepted by construction" rule is stated in
the tool's docstring and the owning leaf, where anyone extending the vocabulary meets it).

## _(2026-09-27)_ — the split cannot return: SOURCE-FORMAT registers, SOT-FORMAT closes (SOT-FORMAT.6)

Root cause this leaf closes: retirement recorded only in prose decays. Every source of truth was
converted (`.1`–`.5`), but no check enumerated the source-of-truth families, so one
`profile.toml` copied from an old branch would have re-entered silently and the merge rule `.5`
defines would be meaningless again. The gate (`scripts/check_source_format.sh`) owns exactly one
question — nothing outside the format, nothing unreadable inside it: the FORMAT arm refuses a
tracked `.toml`/`.json`/`.jsonl`/`.yaml` under `definitions/`, `schema/`, `profiles/`,
`materials/` by name; the PARSES arm requires every `.sexp` there to parse with `sexp.py`;
schema coverage is deliberately other gates' lane (two gates reporting one breach is noise).
Fired RED before registration against a scratch copy of the real corpus with one planted
`profile.toml`. The corpus boundary arms matter as much as the refusal arms: `profiles/*.md`
(dossier prose) and `*.s` (guest programs) must NOT be refused — the gate refuses the split's
shapes, never prose or programs.

⭐ Reading for this leaf surfaced two stale lines, both corrected in passing: the replacement
decision's own *How to apply* said "write the EBNF in `pgen`", contradicting its body — the
director corrected the identification on `2026-09-14` (*"Not it is not PGEN. It is LinkedSpec"*).
The lesson: a decision record's summary lines drift before its body does; reading the whole
record, not the header, is what catches it.

Validation: `--self-test` 7/0; real run `ok (28 source-of-truth file(s))`; both mirrors updated
in the registering commit; `REGISTRY-MIRROR` and `DERIVED-COUNTS` (14 doctrines, 184 arms) green;
full enforcer green. `SOT-FORMAT` closes 10/10.

Lessons: declined here (the corpus-boundary lesson is demonstrated by the gate's own census arms
and stated in its header); the pgen-staleness observation is general but thin — one instance,
recorded in the corrected record and this note; a second instance would earn a knowledge card.

## _(2026-09-27)_ — the record merge is definable, and it decides (SOT-FORMAT.5)

Root cause this leaf closes: composition is a merge, and with everything in one format the
records' union finally has a rule. Design (recorded in the leaf, before code): a unit is a
directory carrying `requirements.sexp` / `contract-obligations.sexp` / `sources.sexp` by name,
read through the single mapping owners (`records_sexp.py`, `dossier_sexp.py`) — the merge
parses nothing itself. Merge key is `id`; on collision every field must be equal except
`profile_ids`, which is membership and unions; sources collide on full pins (same id + different
`sha256` = two texts of one specification). After the union, every reference must resolve in
it — requirements' `dependencies`/`obligation_ids`/`source_refs`, obligations' likewise.

Two measured defects, both found by probe before any code was written:

1. **RECORD-SCHEMA never refused duplicate record ids.** The gate built `by_id` as a dict
   comprehension — last wins, silent. A scratch catalogue with two `REQ-D-A` records differing
   in `risk` returned `rc=0`. Fixed as rule 8 (UNIQUE-ID) with a fired RED arm; self-test
   22 → 23.
2. **Obligation `dependencies` were checked against nothing**, and the first closure run on the
   real profile reported `OB-ENV-RESET` → `OB-ENTRY-STATE` as dangling — because the check
   looked only in requirements. Measured truth: every cpu-guarantee depends on its requirement
   (`OB-XLEN` → `REQ-D-XLEN`), every environment-assumption on the guarantees it discharges
   (`OB-ENV-RESET` → `OB-ENTRY-STATE`). An obligation's dependency now resolves against
   requirements ∪ obligations; a requirement's against requirements — inferred from all 42
   real records, zero dangling.

Validation: `merge_records.py --self-test` 18/0 (10 GREEN unions, 8 RED contradictions, each
naming its fact); the real profile self-composes (26 req + 34 ob + 3 src); an edited copy is
refused naming field and both values; a scratch extension unit composes against the base and is
refused by name without it. Regression: sexp 18/0, kernel 50/0, RECORD-SCHEMA 23/0 + real run
green, semantics 52/52, citations 52/52, materials 20/0, smoke ok, readers 28/28, G0 diff
empty, `make check` green.

Lessons: promoted — `docs/knowledge/a-duplicate-id-is-a-contradiction-not-a-shadowing.md`
(the id-keyed dict that collapses duplicates is the same failure in any gate). The
mixed-namespace dependency fact is declined here: measured, owned and enforced by
`merge_records.py`'s closure, where anyone extending the record families meets it.


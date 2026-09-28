# CHANGELOG.md

## SEMILITH-PL-0010 (leaf P1-LAB.10) — replay and reduction; a result becomes an artifact

- `semulith-verify::replay` is the recorded input bundle (G-REPLAY): `algorithm` pins flattened from `definition::MANIFEST` — profile, ilen, generator name+sha256, every input pin — plus the harness version and the model under test (`production` or `mutant:<name>`, resolved through the `.9` vocabulary); the platform region and entry; the image words with a sha256 guard; the recorded event choice (`DeclaredNone`, OB-ENV-EVENT-DELIVERY named — the platform's actual choice, recorded as data); the step budget; and the recorded steps plus the stop's canonical render. `replay()` checks identity by name — definition pins against the live manifest, then the image digest against the bundle's own words — and walks recorded-vs-replayed through `run::compare`, so drift is named at the first differing observation. JSON both ways through the crate's own reader and a hand-rolled writer; a document missing any accompaniment fails parse naming the field — the bare-seed refusal is structural (ARCHITECTURE §7: a seed without the generator version and event stream is insufficient).
- `semulith-verify::reduce` is the minimizer (EVD-02): classic ddmin over the guest word sequence with retention = the original first divergence exactly (same step, same field description — identical prefix semantics make a same-step divergence byte-identical). Every accepted removal preserves the property structurally, so the result always retains; each minimized result carries an exhaustive 1-minimality witness (no single-word deletion retains). Measured on the suite: zext-addi → the 2-word prefix (x1 @ step 1), jal-no-link → 4 words (x5 @ step 7), jalr-odd-bit → 9 words (trap @ step 10, tval 0x80000029 re-derived from the minimized program — the fixture note's prediction, retained). Named boundary: phantom-load is refused `NoDivergence` — census-class wrong behaviour is not reducible on observations.
- `semulith-cli` gains `semulith bundle --guest=X --mutate=Y` (write the bundle JSON), `semulith replay <file>` (re-derive and judge: identical rc 0, named mismatch/refusal rc 1), and `semulith reduce --guest=X --mutate=Y` (print the minimized program with its retained divergence). Exercised end to end: bundle → replay identical; a hand-corrupted bundle refused naming the digest.
- Verification: 179 tests green across 5 suites (114 verify incl. 15 replay + 6 reduce); clippy `-D warnings` clean; wasm build rc=0; `make gate` 23 doctrines green. Book P1 gains "Replay and reduction"; the `.9` acceptance checklist archives to `docs/tasks/archive/P1-LAB.md` (per-part ceiling obeyed).
- Pressure valve, same commit: both append heads crossed their registry ceilings on this entry — CHANGELOG.md sheds its oldest entry to `docs/changelog/shard-0033.md` (head 67,723 → 64,156), DEV_NOTES.md its two oldest to `shard-0034.md` (51,872 → 48,589); the manifest re-freezes at 36 rows and SHARD-FREEZE stays green.
- Lockstep: MEMORY/LIVE_STATUS (P1 10/12)/TASK_TREE/CHANGELOG/DEV_NOTES + book P1 and this tree; frontier moves to `.11` (performance baseline).

## SEMILITH-LB-0001 (leaf LAB-BENCH.1) — the laboratory bench: feel the tool while it builds

- `semulith demo [--guest NAME] [--mutate NAME] [--json]` runs a tracked guest under the real or a mutated model and prints the full observation trace with the judgement — the pinned expectation verdict and, for mutants, the first divergence named, or the crossing-census story when the trace never betrays the mutation (the phantom-load arm). Exit codes make the detector legible: 0 clean, 1 a caught mutant, 2 usage.
- The browser bench: `bench/index.html` over a std-only wasm module (`semulith-verify`'s cdylib with an `extern "C"` surface in `src/wasm.rs` — no wasm-bindgen, no new dependency, RUST-01 untouched). Guest × model selectors render both traces side by side with the first divergence highlighted; `make bench` builds the module, `scripts/smoke_bench.js` verifies the page's engine headlessly with node (8 arms: clean × 4 guests, the three trace-level mutants at their .9-pinned steps, the census arm at 7-vs-0). Same `run`/`mutate` engine the commit gate tests; the JSON shape is shared with `demo --json`.
- `semulith-verify` gains `report` (the demo/bench judgement: the `.9` anchor made reusable — architectural expectations and the crossing census as two separate verdicts, because the phantom-load arm keeps one while breaking the other) and promotes the suite's pinned census table to the public surface.
- Verification: 158 tests green across 5 suites (93 verify incl. 5 report suites); clippy `-D warnings` clean; wasm workspace build rc=0 (PORT-WEB holds with the new cdylib); `make gate` 23 doctrines green; smoke_bench 8/0. Book P1 gains "The laboratory bench"; TOOLBOX gains the two bench tools.

## SEMILITH-PL-0009 (leaf P1-LAB.9) — the validator mutation suite; a differential that is known to disagree

- `semulith-core::exec::step_over` and `semulith-verify::run::run_over` parameterize the single execution path over the instruction table — production delegates with `definition::INSNS`; the table scan applies exactly the predicate the generated `decode` documents, pinned by a core suite over every canonical word, operand-varied encodings, and unclaimed words. A mutation is data the one evaluator consumes (OWN-01); there is no second implementation of any rule.
- `semulith-verify::mutate` is the EVD-09 suite, 11 arms: the eight designated wrong-behaviour classes — wrong sign extension (x1 @ guest-control step 1), suppressed register write (x5 @ step 7), wrong trap cause (@ step 0), illegal-opcode substitution for a model limitation (SEM-02 — the limitation carried as the undefined case, the fabrication caught @ step 0), an extra memory access (the architectural trace still agrees; the pinned four-guest data-crossing census catches the phantom load), shifted event delivery (the missing trap @ its due step), an overbroad mask hiding a changed defined bit (bit 30 of SRAI/SRLI — srli executes as srai, x1 @ step 2), a stale reference configuration (the pc @ step 0) — plus the JALR odd-bit arm the `guest-control.expected.sexp` note names: the mutant faults with `InstructionAddressMisaligned` at 0x80000029, exactly the fault both references can never show. The comparison-suppression exhibit proves the writes leg is load-bearing: a writes-blind comparator agrees with a mutant the real comparator catches. Every guest arm re-derives the pinned GUEST-GEN expectations against the real model before judging the mutant.
- The `.1`–`.8` acceptance checklists archive verbatim to `docs/tasks/archive/P1-LAB.md` — the live file crossed its per-part ceiling; the ceiling was obeyed, not raised (the SOT-FORMAT precedent). The family aggregate (665,577 B > 640 KiB) is re-derived to 1 MiB per the documented precedent: lanes grew 25 → 32 since the 2026-09-20 derivation and the evidence archives are the designed growth — per-part stays 64 KiB and bit correctly (`docs/decisions/decision_task-tree-family-bound-rederivation.md`).
- Verification: 152 tests green across 5 suites (88 verify incl. 11 mutate arms; 25 core exec); clippy `-D warnings` clean; wasm build rc=0; `make gate` 23 doctrines green. Book P1's "Validating the validator" now describes the landed suite.
- Lockstep: MEMORY/LIVE_STATUS (P1 9/12)/TASK_TREE/CHANGELOG/DEV_NOTES + book P1 and this tree; frontier moves to `.10` (replay and reduction).


## SEMILITH-PL-0008 (leaf P1-LAB.8) — the first execution slice; the definition executes

- `semulith-core::exec` is the definitional interpreter: `step` fetches through the environment contract, decodes, extracts operands (scattered B/J immediates unscrambled; split fields bound per the semantics rule) and evaluates the generated `Sem` trees — the semantics DATA stays the one executable owner (OWN-01); there is no handwritten per-instruction behavior. The width algebra (`sext`/`zext` extend from the operand's own width; literal shifts widen; shifts operate at the operand's width, so `sraiw` replicates bit 31, not bit 63) is the unique reading under which all 52 trees are correct at once — LUI extends from bit 31, LB from 8 — now differentially validated, not assumed. 24 test suites cover every outcome family and every reporting point (misaligned target on the branch, fetch fault at the pc, misaligned access raised before the boundary, reserved decode carried as `UndefinedCase`, ECALL/EBREAK as requested traps).
- `semulith-verify` gains the observation layer: `run` records `(pc, word, register writes, trap)` steps — the same vocabulary `compare_traces.py` reduces the references to — plus the full boundary-crossing log, and `compare` reports the FIRST divergence with the differing field named (a register, the trap cause, the tval, a missing write; a length mismatch is a non-agreement, never a prefix pass). `elf` loads the writer's ELF64 with named-field refusals. `guests.rs` is GENERATED from the tracked guests and their specification-derived expectations (`scripts/gen_guests.py`); GUEST-GEN — the 23rd doctrine — refuses drift and fired RED on a hand-edited fixture before registration.
- `semulith-cli` gains `semulith run <elf>`. The offline differential (the GUEST-GEN fixture) re-runs all four guests against their EVD-05 expectations on every `make check` — 77 verify suites green. The live experiment `scripts/run_semulith_smoke.py` agrees with sail-riscv AND spike on every enabled comparison: 34 aligned steps across the four guests, byte-identical reproduction on re-run.
- Verification: 141 tests green across 5 suites; clippy `-D warnings` clean; wasm build rc=0; `make gate` 23 doctrines green; GUEST-GEN self-test 7/0. Book P1 gains "The first execution slice".
- Lockstep: MEMORY/LIVE_STATUS (P1 8/12, doctrines 23, arms 254)/TASK_TREE/TOOLBOX/DOCTRINE_ENFORCEMENT/doctrine/fact_ownership.tsv + book doctrines chapter and this tree; frontier moves to `.9` (validator mutation suite).

## SEMILITH-PL-0007 (leaf P1-LAB.7) — the graph and report checker; the citation becomes a derivation

- `semulith-verify` gains five dependency-free modules: `json` (a `json.loads`-parity reader), `pattern` (a regex subset refusing everything outside the census by name), `sha256` (FIPS 180-4, known-answer pinned), `schema` (the Python validator's keyword subset and refusal discipline, plus two verdict-neutral tightenings: array `type`, schema-valued `additionalProperties`), and `graph` (the `EVIDENCE_AND_GATES.md` §3 invariants over the frozen `examples/` bundle). The PACKAGE_CHECKS schema results are re-derived in Rust per RUST-01 — 5/5 records validate, 6/6 negative controls rejected with reasons named, the synthetic source fingerprint matches the ledger pin.
- Every designated rejection has a mutation suite that must catch it: orphan IDs, stale hashes, unsupported `passed` claims, missing evidence, deleted dependency links, out-of-scope profiles, duplicate ids, unpinned sources, undeclared checks, dependency cycles — plus the positive control (a fully met bundle gates `passed`). The intact fixture is graph-clean and honestly `incomplete` (`GateStatus` is a type, so "pass" has exactly one expression). The library is `std::fs`-free (evidence bytes arrive through a resolver), keeping the workspace wasm-buildable.
- `semulith check-examples` presents the report; `RECORD-SCHEMA` now runs the Rust engine after the Python phase on every commit and fired RED against a mutated requirement before landing. Verification: 59 verify suites green; `make check` clean; wasm green; gate green. Book P1 gains "The graph and report checker".
- Lockstep: MEMORY/LIVE_STATUS (P1 7/12)/TASK_TREE/DEV_NOTES/TOOLBOX/DOCTRINE_ENFORCEMENT + book doctrines chapter/check_requirements.sh and this tree; frontier moves to `.8` (first execution slice).

## SEMILITH-DS-0003 (leaf DOC-SHARDING.2) — DEV_NOTES joins the shard family

- `DEV_NOTES.md` gets `CHANGELOG.md`'s lifecycle, by generalization rather than a fork: `scripts/shard_history.py` writes a shard header naming the head it was cut from and that head's own registry ceiling (`# DEV_NOTES shard … 48 KiB`; CHANGELOG's `.1` header shape stays byte-identical, self-test arm), and `scripts/check_changelog_shards.sh` learns the two-head family — one COVERAGE/FROZEN/APPEND-ONLY scan over the shared `docs/changelog/` manifest, UNIQUE across both live heads + shards. First event: 2 entries to `shard-0027.md`, `31 == 29+2` proved at the event, head 48,954 → 46,212, 29-row manifest frozen.
- Both tools fired RED on the real tree pre-commit (a scratch shard carrying a live DEV_NOTES heading; the old sharder writing CHANGELOG-provenanced DEV_NOTES shards). The new UNIQUE leg then exposed two stray duplicate headings inside DEV_NOTES.md itself — removed; each entry exists exactly once. The registry comment that claimed DEV_NOTES was already sharded (designed end-state stated as present fact) is corrected.
- Verification: sharder self-test 12/0, SHARD-FREEZE self-test 14/0, gate green; doctrine mirrors and the routed-destination count (31, unchanged — one family, not a new directory) in sync.

## SEMILITH-AC-0052 (tree ARTIFACT-CLEANUP) — the 2026-09-28 cleanup run

- §8 time-triggered run (last record `2026-09-26`): pre-delete census 132 cargo incremental-cache `.bin` files / 720 MB, every one under a cargo `*/incremental/*` directory (`target/` own + wasm32 profiles, `.app-data/target/` vendored-consumer builds); 0 stray `.bin`/`.log` in `target/release` / `target/debug/deps`; the 7 `.app-data/cargo-home/**/tests/data/*.bin` crate-source fixtures classified inputs and kept. Post-delete re-census: 0 incremental `.bin`; `.app-data` 2.0 G → 1.4 G. Record overwritten (latest entry only) and the run evidenced in the tree's Verification Log; enforcer green.

## SEMILITH-PL-0006 (leaf P1-LAB.6) — the canonical definition, generated

- `semulith-core::definition` exists, and it is generated: `scripts/gen_definition.py` lowers the unit's canonical definition — `profiles/rv64i-lab-v0/encoding.sexp` composing `definitions/riscv/rv64i.sexp` through the one shared resolver, plus `definitions/riscv/rv64i.sem.sexp`, the execution authority — into 12 operand fields (scatters attached), 52 decode rows (mask/value/operands/upstream-table/locator), and every semantics rule's effect tree as a typed `Sem` value. OWN-01 holds structurally: the semantics DATA owns each rule; there is no handwritten second copy, and the interpreter slice (`.8`) will evaluate exactly these trees. `decode(word)` is generated fixed-bit dispatch; a word no entry matches is reserved-decode, the caller's classification.
- OWN-03's manifest rides as data (`MANIFEST`): the four canonical inputs by path and sha256, the generator named and content-hashed, the configuration (profile/ilen/fragments) as data, and the `rv_i`/`rv64_i` upstream pins from the fragment. The 22nd registered doctrine, `DEF-GEN` (`scripts/check_definition_gen.sh`), regenerates in memory and refuses drift with the regeneration command; its 8-arm self-test re-runs before every judgement; fired RED against a hand-edited module before registration — the rite caught a real defect (a relative `--encoding` path crashed `relative_to`, and the check collapsed an unjudgeable crash to rc=1; the generator now refuses out-of-repo inputs by name and the check propagates rc=2 as REFUSED). The owner→mirror pairs (encodings, semantics, state → `definition.rs`) are registered in `doctrine/fact_ownership.tsv` and its census.
- The generator re-derives every check it emits through — schema validation per input, the SEMANTICS binding rule (split `imm12`/`bimm12`, `shamt`), the MODEL-COMPOSE.6 refinement rule, completeness, fixed-field sanity — and refuses by name: another unit, an unsupported ilen, an instruction without semantics, an operand the encoding does not provide, a missing semantics document, a non-literal width. FENCE's `fm`/`pred`/`succ` stay declared-but-unfielded with a test ratchet naming the three decorations.
- Verification: 10 new definition suites green; `make check` 5 suites / 53 tests / 0 warnings; wasm build green; `make gate` green with 22 doctrines (245 arms). TOOLBOX gains the rows `.3` owed (`gen_state.py`/`check_state_gen.sh` were missing from the tool table).
- Lockstep: MEMORY/LIVE_STATUS/TASK_TREE/book P1 + doctrines chapters and this tree; frontier moves to `.7` (graph and report checker).

## SEMILITH-PL-0005 (leaf P1-LAB.5) — four typed outcome families, SEM-01 made structural

- `semulith-core::outcome`: `TargetEvent` (`Exception` with the unprivileged cause vocabulary, each cause named by its rule; `RequestedTrap` for ECALL/EBREAK — delivery is a data event, not a stop command), `Advance` (`Completed`, `Stop{reason}` — no waiting/partial advance, platform facts recorded in the docs), `ModelError` (`Unimplemented`/`InvalidDescription`/`InconsistentState`/`ContractViolation` — `.4`'s boundary-local violation re-homed), `UndefinedCase` (`ReservedDecode` — REQ-D-RESERVED-DECODE's case carried as its own outcome, never auto-converted to an exception). `StepOutcome` is the step-level sum `.8` produces and the harness matches.
- The acceptance proven by a stub stepper (test code, not production semantics): `a_delivered_exception_lets_execution_continue` (harness records the `Breakpoint` trap, the next instruction still runs, pc advances past all three); `an_unimplemented_instruction_is_not_an_illegal_instruction_trap` (the `Failed` arm has no typed expression that reaches an `IllegalInstruction` `Exception`). Plus family distinctness, the `ContractViolation` re-home round trip, and `UndefinedCase` ≠ `Exception`.
- Verification: 5 new suites green; `make check` 5 suites / 43 tests / 0 warnings; wasm build green; `make gate` green.
- Lockstep: MEMORY/LIVE_STATUS/TASK_TREE/book P1 chapter and this tree; frontier moves to `.6` (canonical definition skeleton).

## SEMILITH-PL-0004 (leaf P1-LAB.4) — the environment boundary, and fixtures that answer it

- `semulith-core::env` owns the request/response contract the CPU crosses: `Request` (Fetch — width pinned to 32 by construction, OB-ENV-FETCH-SUPPLY; Load/Store at `AccessWidth` B/H/W/D, OB-ENV-ACCESS-WIDTHS — an unofferable width cannot be formed), `Response` (raw bits, no extension — REQ-D-LOAD-EXT stays instruction-layer), and two failure families kept apart by construction: `Failure` (target-facing: AccessFault, Misaligned — the profile's "not substituted" rule) and `ContractViolation` (the environment broke a rule; SEM-01's separation, boundary-local until `.5`). One trait, `Environment::request`, drives every crossing. Addresses are bare `u64` (SEM-05).
- `semulith-verify::fixtures` implements it: `FlatMemory` — one little-endian main-memory region, no side effects (OB-MAIN-VS-IO), re-read per fetch so stores are immediately visible (OB-CODE-VISIBILITY), fetch counter as the no-extraneous witness, alignment judged before region membership (stated, tested); `ScriptedEnv` — the conversation pinned in advance, faults scriptable, and a request the script does not cover reports `ResponseMismatch`/`ScriptExhausted` instead of inventing data (§4.1.4's negative-fixture rule, exercised for real).
- Verification: 16 new suites green (12 fixture + 4 contract-property), all without an instruction handler; `make check` 5 suites / 42 tests / 0 warnings; wasm build green; `make gate` green.
- Lockstep: MEMORY/LIVE_STATUS/TASK_TREE/book P1 chapter and this tree; frontier moves to `.5` (typed outcome families).

## SEMILITH-PL-0003 (leaf P1-LAB.3) — architectural state, generated from the descriptor

- `semulith-core::state` exists, and it is generated: `scripts/gen_state.py` derives `state.rs` from `profiles/rv64i-lab-v0/state.sexp` through `dossier_sexp` (the single mapping owner), byte-deterministically, with the input's sha256 in the module header (OWN-03). The generator is deliberately narrow — it refuses, naming the construct, any descriptor shape it cannot emit (another profile, a non-64 width, an unmapped special register, a missing SEM-08 census). The 21st registered doctrine, `STATE-GEN` (`scripts/check_state_gen.sh`), re-runs its 6-arm self-test before judging and refuses drift with the regeneration command; fired RED against a hand-edited module before registration. The owner→mirror pair is registered in `doctrine/fact_ownership.tsv`.
- The state: 32 × 64-bit integer registers + pc, 264 bytes inline, no heap (RUST-03); x0 hardwired zero (write discarded, read yields 0); the three ISA-chapter-named roles (x1 return address, x2 stack pointer, x5 alternate link) emitted as alias views over the one storage — C02's "does writing one alias affect every other view" answered by 10 test suites; laboratory reset per REQ-D-ENTRY-STATE/OB-ENV-RESET (x1..x31 = 0, pc = environment-supplied entry); SEM-08's hidden-state census carried as data (7 candidates checked, none present).
- Verification: 22 test suites green (12 arithmetic + 10 state); `cargo clippy --all-targets --all-features -- -D warnings` clean; workspace still builds for `wasm32-unknown-unknown`; `make gate` green with the doctrine registered and both mirrors (DOCTRINE_ENFORCEMENT.md, the book's doctrines chapter) in sync.
- Lockstep: `LIVE_STATUS.md` re-derived (21 registered, 237 self-test arms; P1 3/12); the name list in the doctrines row completed (STATE-GEN added; SCOPE-COVERAGE, omitted when it landed, restored); `MEMORY.md`, `docs/TASK_TREE.md`, the book's P1 chapter, and this tree updated. The frontier moves to `.4` (environment boundary and fixtures).

## SEMILITH-PL-0002 (leaf P1-LAB.2) — target arithmetic primitives, verified exhaustively at reduced width

- `semulith-core::arith`: 18 SEM-03 primitives — ALU register/immediate ops, shifts with the REQ-D-SHAMT masks as named functions, the `*W` word ops (REQ-D-WSUFFIX), `sext`/`bits` extraction and extension, LUI/AUIPC offset formation. Each contract states width, signedness, intermediate precision, truncation, exceptional behavior; each doc comment source-links the requirement record and pinned locator (REQ-D-ALU-REG/IMM, REQ-D-SHAMT, REQ-D-WSUFFIX, REQ-D-LUI-AUIPC, REQ-D-LOAD-EXT, REQ-D-XLEN). Unmasked shift amounts panic in debug instead of silently wrapping.
- Verification, the acceptance's shape: boundary suites at full XLEN; an **8-bit exhaustive layer** (every `(x, y)` for the binary ops, every `(x, shamt)`, every `(x, from_bits)`, every `(lo, hi)` window) against references formulated on a different host width; a 100k-draw boundary-heavy sweep of the word ops against a u64-width reference. 12 suites green; clippy `-D warnings` clean.
- The exhaustive layer failed on its first run for exactly the reason the acceptance exists: `slt`/`sar` are width-sensitive, and the naive low-byte comparison of signed ops is wrong — fixed by embedding the narrow signed view at XLEN. The lesson is promoted to `docs/knowledge/reduced-width-verification-of-signed-ops.md` (LESSON-PROMOTION satisfied in-commit).
- Scope, stated: the requirements' `implementation_status` stays `planned` — these are the executable halves; instruction-level obligation checks need the interpreter slice (`.8`). The frontier moves to `.3` (architectural state).

Validation: `cargo test -p semulith-core` 12/0; `cargo clippy --all-targets --all-features -- -D warnings` clean; `make gate` → `=== all doctrines green ===`.

## SEMILITH-PL-0001 (leaf P1-LAB.1, PORT-WEB.1) — the laboratory gets its three crates, and the browser target gets its gate

- `P1-LAB.1`: `crates/app` (the `semulith` placeholder) replaced by the three laboratory crates, wired per `docs/ARCHITECTURE.md` §4 — `semulith-core` depends on nothing (`Cargo.lock` carries no dependencies block for it), `semulith-verify` holds the fixtures home and depends on core only, `semulith-cli` (binary name `semulith`, ROADMAP.md §8) calls both. `make check` green at `-D warnings`; `cargo tree` shows the one-directional edges.
- `PORT-WEB.1` (same commit, as its acceptance requires): the workspace builds for `wasm32-unknown-unknown` from the first slice, enforced by the 20th registered doctrine, `scripts/check_wasm_build.sh` — it refuses with install instructions when the rustup target is absent, re-runs its 4-arm self-test before every judgement, and was fired RED against the real workspace (a `std::os::unix` import in `semulith-core`, refused naming `lib.rs:13`) before registration. CI's doctrines workflow now installs the Wasm target. No host-only API exists yet; the build itself is the standing proof.
- Docs in lockstep: mirrors in `DOCTRINE_ENFORCEMENT.md`, the book's doctrines chapter, `TOOLBOX.md`; `LIVE_STATUS.md` re-derived (20 registered, 231 self-test arms; P1 In Progress, 1/12) with a stale MODEL-METHOD row corrected; the book's P1 chapter now states the crates exist and build for host and Wasm. Fixed in passing: a layer-A typo (`sexr_file` → `sexpr_file`); the `DOCTRINE_ENFORCEMENT.md` ceiling re-derived 20 → 24 KiB in the routes registry (the 20th doctrine row is the surface's contract expanding, the same grounds as the TOOLBOX raise). Both append heads sharded again the day they were sharded — the pressure valve working as designed; the `docs/changelog/` file-count ceiling re-derived 20 → 40 in the same commit (the family now carries shards for two append heads — the derivation is recorded in the registry).

Validation: `make gate` green (20 doctrines); `make check` green (fmt + clippy -D warnings + 5 test suites); `bash scripts/check_wasm_build.sh --self-test` → 4 pass / 0 fail.

## SEMILITH-AC-0051 (leaf ARTIFACT-CLEANUP.2) — the sanctioned watcher is a ruling, not a false positive

The director ruled CHIPDOC's ChipdocWatcher ("it will stay there — do not worry about it from
now on"), and the ruling is now data: `doctrine/sanctioned_processes.tsv` carries the
executable substring, the ruling, and its date, and `check_no_background_jobs.sh` exempts
matching processes from both census arms — with the detection itself untouched, because the
census's whole design is that a list of things you thought of cannot see the thing you did not.
An agent proposes a row; only the director's ruling lands one. Verified both directions: the
live check prints `handoff: OK` with the watcher running, and the control probe (row absent)
flags the same process again. Tracked-content gates are unaffected.

## SEMILITH-MM-0050 (leaf MODEL-METHOD.6) — no coding without the source of truth, and MODEL-METHOD closes

The director's rule is a gate now. The unit registry gains `(requires …)` — the categories a
unit's scope declares — and `SCOPE-COVERAGE` (19th doctrine, 7 arms) refuses the day a required
category is `missing` or has no census row, fired RED before registration on a scratch unit whose
required category was absent. A unit with an undeclared scope refuses too: code may not start
against a scope never declared. `rv64i-lab-v0` declares its 14 in-scope categories, and the
verdict reads `1 unit(s) may code — every required category covered` — P1-LAB's precondition is a
verdict, composed with EXTRACTION (coverage says the facts are OWNED; extraction says they are
EXTRACTABLE). **`MODEL-METHOD` closes at 13/13**: the method in prose, the census, the
acquisitions, and the coding gate all landed; every P1 precondition is mechanical.

## SEMILITH-MM-0049 (leaf MODEL-METHOD.5) — the method, in prose, written to be learned from

`docs/METHOD.md` is the method this project actually exercised this session, written to be
carried: document → decision → requirement → obligation → check, with the ORDER justified at
each step and the rejected alternatives kept — a version string is not an identity, a laboratory
policy must never read as an architectural rule, one fact has one owner and every mirror is
governed, positive-AND-negative checks carry derived-not-copied values, and a check that cannot
judge never reports green over an absence. One rule — the shift-amount rule — is walked end to
end by name, its two non-mechanical steps flagged inside the walk. A closing section names the
four steps no gate can take (choosing the publication, classing the fact, judging the authority,
classifying the disagreement) and declares everything else mechanical — which is the method's
discipline, stated as a rule. The mdBook carries it verbatim under The contracts; the
carryability probe confirms the body depends on no tool, path, or id this project owns.

## SEMILITH-MM-0048 (leaf MODEL-METHOD.4) — the run-real-code set is acquired, and the PDF question is answered

What the ISA chapters do not own is now pinned: the RISC-V psABI canonical render, the System V
ELF specification, the generic syscall header (the hosted exit convention), and the LLVM
compiler-rt builtins inventory — the last carrying `__muldi3 (di_int a, di_int b); // a * b`,
the soft-multiply intrinsic a no-`M` target calls. Each is digest-pinned in the owning leaf,
cached on-volume under `.materials/run-real-code/`, and re-derivable from the recorded curl
commands; the bytes stay out of git, per the no-redistribution doctrine — the tracked record is
the digest table, not the documents. The startup/runtime contract needed no acquisition: the
harness contract already owns entry state and the ECALL/EBREAK exit convention.

⭐ The PDF question (MODEL-BOOKS.2) is answered **YES**: the specification's PDF rendering carries
the instruction-format tables as selectable text — `pdftotext` extracts 1.96 MB from the
release asset, and the RV32I format-table region yields `funct7 / rs2 / rs1 / funct3` as clean
cells. Encodings can be re-sourced from the primary document. SRC-02 records: the pinned
revision's release PDF was not located in three pages of releases; the chipdoc corpus route was
unavailable here (`$SEMULITH_CHIPDOC_ROOT` unset) — the psABI came from its canonical public
render instead.

## SEMILITH-MM-0047 (leaf MODEL-METHOD.3) — the census sweeps the snapshot, and missing changes its meaning

The coverage census for `rv64i-lab-v0` did what a first pass cannot: it opened the pinned
snapshot and checked. Every covered category's subject matter is present in the pinned pages —
and, the measured surprise, so are the excluded subsystems' chapters (a/d/f/q/v-st-ext, rvwmo,
counters, zicsr, zifencei). `missing` therefore never meant "material absent"; it means the
profile EXCLUDES the subsystem, and all six missing rows now name what would close them: a
profile revision against snapshot chapters (C07/C08/C16), the separate Privileged Architecture
manual (C12/C14/C15), the Debug specification (C18). Device and interconnect categories became
the new `deferred-to-board` disposition — P5-BOARD's to own, with the CPU recording an
environment assumption in their place. Final census: 10 covered, 4 partial, 6 missing with
closers, 3 deferred-to-board, 1 out-of-scope. RECORD-SCHEMA rule 12 (UNRESOLVED MATERIAL) keeps
every named material honest against the catalogue; 33 arms.

## SEMILITH-MM-0046 (leaf MODEL-METHOD.2) — the materials requirement: what each unit owes its model

The catalogue of documents gains the requirement layer: `schema/units.sexp` +
`schema/category-needs.sexp` declare two record families (zero kernel lines), and
`materials/units.sexp` + `materials/category-needs.sexp` carry the one-row registry and all 24
INFORMATION_CATALOG categories for `rv64i-lab-v0` — each bound to the material kind that
supplies it, at its layer, with an honest disposition. The vocabulary distinguishes ABSENT from
NEVER-NEEDED: `missing` (a reason is owed — C07/C08/C12/C15/C16/C18, excluded subsystems) versus
`out-of-scope` (C17/C19–C21, board-layer facts a processor never owed). RECORD-SCHEMA rules 10–11
enforce it — the acceptance's shape, a board-layer `missing` for a processor, refuses as
`LAYER LIE` — 6 new arms, 32 total, 7 record files green. The DSP-specific questions of the
catalog's §5 ride as their own D-category ids, admitted by the schema and pre-built for nobody.

## SEMILITH-MM-0045 (leaf MODEL-METHOD.7) — the no-duplicated-fact rule is a registry, and every mirror is governed

"Single source of truth" now means one owner per fact, mechanized. `doctrine/fact_ownership.tsv`
names the one owning file per fact kind (8 kinds — configuration, state, encodings, semantics,
requirements, obligations, pinned sources, materials), each legal derived mirror, and the
doctrine governing every owner→mirror pair; `FACT-OWNERSHIP` (18th doctrine, 8 arms) verifies one
owner each, owners exist, every governor is a registered doctrine that runs, and the corpus's four
restatement pairs are all named. The acceptance's shape — a fact stated in two, refused — fires as
`UNGOVERNED MIRROR` and `UNREGISTERED MIRROR PAIR`.

⭐ The inventory found what the rule exists to catch: the corpus's mirrors were mostly governed
(decision↔requirement by RECORD-SCHEMA; state↔profile by PROFILE-CONSISTENCY; composition↔fragments
by UNIT-COMPOSITION), but 28 obligations restate their requirement's statement — all matching
today, nothing refusing the day one drifts. RECORD-SCHEMA gains rule 9 (MIRROR) with 3 arms; 26
total. An ungoverned mirror is how one fact quietly becomes two; the registry makes that a verdict.

## SEMILITH-MM-0044 (leaf MODEL-METHOD.10) — the extraction contract: one set, four ways

*"The engine can extract all it needs"* is a verdict now. `scripts/check_extraction.py` requires
SCOPE (the profile's declared instruction set), ENCODING (the composed union), SEMANTICS, and
REQUIREMENTS to be ONE set — every declared instruction with all three — plus every state element
with a reset and every obligation with a positive and a negative check. The real corpus passes:
`SUFFICIENT for an engine: 52 instructions, each with encoding + semantics + requirement`.

⭐ The contract as stated first fired RED on the real corpus — measured, not assumed: no
requirement↔instruction link existed, and the whole ALU family (13 instructions) had no
requirement at all. The leaf fixed the corpus, not the contract: `(insns …)` on the schema
(kind-agnostic — FENCE names one instruction, ECALL-EBREAK two), two new decision/requirement/
obligation triples grounded in the corpus's own §1.1.4 semantics (SLTIU's sign-then-unsigned quirk
included), and the count-bearing docs re-derived (28 decisions, 28 requirements, 36 obligations,
72 checks; G0-REPORT regenerated in the commit). RECORD-SCHEMA caught a wrong obligation id
mid-curation and was fixed before commit. The acceptance fired RED on a real-corpus copy with one
instruction's semantics removed. `EXTRACTION` is the 17th project doctrine — **P1's start
condition is now fully met**, and P1-LAB cites a check that runs.

## SEMILITH-MC-0043 (leaf MODEL-COMPOSE.5) — a composition is an ordinary unit, and the tree closes

Nesting, materialized: `schema/composition.sexp` — `(composition (id …) (part …))`, zero kernel
lines — and `scripts/compose_units.py` turn a board manifest into an ordinary unit directory.
The parts merge through `merge_units(…)` — the same code the verdicts consume, not a fork — the
three catalogues write through the single mapping owners, provenance kept (`profile_ids` stay
with their origin units), and an `encoding.sexp` derives when exactly one part carries one. The
acceptance is the run: a board materialized from the real profile's parts (26 requirements, 34
obligations, 3 sources, the 52-instruction encoding) self-merges, discharges 8/8, and resolves
through the encoding read path — every check the unmodified one-level tools already own.
Two ISA-carrying parts refuse with the multiprocessor boundary named (the address-space operator
stays earned-from-a-real-case). **`MODEL-COMPOSE` closes at 6/6** — composition is now a verdict,
a discharge, and a materializable unit.

## SEMILITH-MC-0042 (leaf MODEL-COMPOSE.6) — a silent override is refused, and the execution authority gets its gate

The hard axis has its first mechanical form. `schema/semantics.sexp` gains `(refines (insn "name"))` —
zero kernel lines — and `check_semantics.py --compose` decides the rule over a unit's fragments in
composition order: an instruction whose semantics appear in more than one file is an override,
legal only when the extending file declares the refinement. The acceptance fired RED on a
real-shaped composition (a fake extension redefining `add` → `SILENT REDEFINITION`,
rc=1); a declared refinement is accepted and reported; both lies (a declaration naming nothing the
file defines, refining nothing an earlier file defines) are refused by name.

⭐ The third orphan of the family `MODEL-COMPOSE.4` closed for encodings: `check_semantics.py`
and `check_citations.py` were invoked by NOTHING — the semantics corpus, which `ROADMAP.md`
names the execution authority, was healthy only by hand. `SEMANTICS` (16th project doctrine) now
runs the per-fragment checks and the 52/52 citation resolution in every gate, with a NAMED SKIP —
never a green lie — when the offline cache cannot judge. The IALIGN-class (global-behaviour)
refinement stays named-and-deferred: per-instruction is the granularity the corpus writes.

## SEMILITH-MC-0041 (leaf MODEL-COMPOSE.4) — slots are data, and the unit's union is decided again

Top-down composition with holes is real, and it is declared, never inferred: `compose`
gains `(status complete|partial)` and `(slot (id …) (requires …))` in
`schema/encoding.sexp` — zero kernel lines. A partial composition passes the checks
that apply and is reported partial (`PARTIAL — 1 slot(s) unbound: clint requires riscv/timer`);
a composition claiming completeness while a hole is open is refused, and a partial declaration
with nothing unbound is refused too — both directions of the silence rule.

⭐ The substrate was two measured defects, not one. Since `MODEL-COMPOSE.2` moved the
instructions into fragments, nothing decided the unit's composed encoding space — the disjointness
checker read compositions its own way and could no longer read a unit at all. And it never
schema-validated its input (a planted `(widget "x")` passed silently). Both are closed:
one resolver (`riscv_asm.resolve_composition`) now serves the assembler and the
checker, the composition document and each resolved fragment validate against the schema layer
before unioning, and `UNIT-COMPOSITION` (15th project doctrine) decides every tracked
unit — the profile composes 52/52. Two more latent bugs of the same family surfaced in the
resolver itself (`[0]`-indexed children the 0-or-more grammar does not guarantee) and are
fixed with arms proving the absent-marker paths. Nothing observable moved: every guest still
assembles, matches, and reproduces.

## SEMILITH-MC-0040 (leaf MODEL-COMPOSE.3) — assumption/guarantee discharge is a verdict

The composition claim is conditional no longer in name only. `scripts/discharge_assumptions.py` is
the mechanical form of `docs/CPU_ENVIRONMENT.md` §5: every `environment-assumption` in
the merged obligation set must be discharged by named guarantees — every dependency resolving
to an obligation whose direction is a guarantee — or the composition is rejected naming the
assumption and the reason. The profile's own 8 assumptions discharge 8/8 today, every edge
printed (`OB-ENV-RESET -> 'OB-ENTRY-STATE' (cpu-guarantee)`, and kin); a unit
carrying only the reset guarantee discharges `OB-ENV-RESET` across the boundary; and
removing that one guarantee rejects the composition from both halves of the corpus (`DANGLING DEP`
on the assumption, `UNDEFINED OBLIGATION` on the requirement). Discharge-specific refusals
proven on fixtures: a demand pointing at a demand (`UNDISCHARGED CHAIN`), an assumption
naming no guarantee (`UNDISCHARGEABLE`) — and the complement, stated so nobody reverses
it: an unclaimed guarantee is not an error.

`SOT-FORMAT`'s census did the design work: the discharge edge already existed in the
corpus as obligation dependencies — the operator made it a verdict instead of a hope.

## SEMILITH-SF-0061 (leaf SOT-FORMAT.6) — the split cannot return: SOURCE-FORMAT registers, SOT-FORMAT closes

The 14th project doctrine is registered: `scripts/check_source_format.sh` refuses a source of
truth outside the one format — a tracked `.toml` / `.json` / `.jsonl` / `.yaml` under
`definitions/`, `schema/`, `profiles/`, `materials/` is named and refused (the FORMAT arm,
fired RED before registration against a scratch copy of the real corpus with one planted
`profile.toml`), and every `.sexp` there must parse with the one reader (PARSES). The real
corpus — 28 source-of-truth files — is green. Retirement in prose decays; the gate is the
decay's answer. Both doctrine mirrors (`DOCTRINE_ENFORCEMENT.md`, the mdBook) carry the row in
the registering commit; LIVE_STATUS's 14 doctrines / 184 arms are re-derived, not remembered.

The supersession chain was verified, not assumed: `decision_canonical-definition-input` has
carried its replacement since `SEMILITH-SF-0041`. Two stale lines surfaced while reading for
this leaf — the replacement record's own *How to apply* still said "write the EBNF in `pgen`"
against its director-corrected body (LinkedSpec), and both INDEX descriptions repeated it —
corrected in passing, with the reason recorded in the record. **SOT-FORMAT closes at 10/10.**

## SEMILITH-SF-0060 (leaf SOT-FORMAT.5) — the record merge is definable, and it decides

The union this tree exists for is now checked: `scripts/merge_records.py` merges two units'
requirements, obligations and pinned sources by id — the same id must carry the same content
(`profile_ids` excepted: it is membership, and it unions), a source id must pin the same
bytes, and every dependency, obligation link and citation must resolve across the union. Two
units compose, or the refusal names the conflicting fact, both values, both units. The real
profile composes with itself (26 + 34 + 3); one edited statement in a copied unit is refused
naming the field; an extension unit whose requirement depends on the base's `REQ-D-XLEN`
composes — and is refused by name when the base is withheld. `MODEL-COMPOSE.3` reads the merged
view (`merge_units(…)` plus the direction census: 26 cpu-guarantee, 8 environment-assumption).

⭐ **Two defects found by probe before any code, both closed.** RECORD-SCHEMA never refused
duplicate record ids — its id → record map collapsed them last-wins, so a catalogue could
contradict itself and stay green (`rc=0`, measured) — rule 8 (UNIQUE-ID) now refuses, 23 arms.
And obligation `dependencies` were checked against nothing: the corpus's cpu-guarantees depend
on requirements while its environment-assumptions depend on guarantees — a mixed namespace the
new closure resolves against requirements ∪ obligations, measured on all 42 records, zero
dangling.

## SEMILITH-SF-0059 (leaf SOT-FORMAT.4) — the dossier moves behind the schema layer, commentary and all

The profile dossier retires its last TOML/JSON: `profile.toml` (26 decisions), `state.json`,
`sources.toml`, `references.toml`, the matched Sail override and the four guest expectation
files are now one S-expression document form each — `profile.sexp`, `state.sexp`,
`sources.sexp`, `references.sexp`, `reference/sail-rv64i-lab-v0.override.sexp`,
`guests/*.expected.sexp` — validated by six new schemas (`schema/{profile,state,sources,
references,override,expectations}.sexp`). `convert_dossier.py --verify` proves the migration
the way `.3` did: every document re-derives field-for-field from its source, and the comment
census is exact line by line.

⭐ **Comments became first-class forms.** The schema kernel reserves one head — `(comment "…")`,
inert at any position, never declared, never forbidden — and the dossier's 158 comment lines
(the warnings, the provenance, the "why" of 26 decisions) survive as data a merge can carry
instead of syntax a parser drops. A typo'd `commment` is still refused by name; a construct,
operator or field named `comment` is refused as dead vocabulary. The open question the tree
carried — do comments belong to the form or the file — is answered: to the file, as an ordered
annotation stream.

**Consumers changed at the seam, not in their logic.** Every gate and tool keeps receiving the
exact dicts `tomllib`/`json` produced, now through the single mapping owner
`scripts/dossier_sexp.py` — which is what makes the verdicts mechanical rather than hopeful:
`PROFILE-CONSISTENCY`'s 39 arms re-fire on converted fixtures (rule 5b included), `run_smoke`
and `compare_platforms` are unmoved, the regenerated G0 report's diff is input names only, and
the Sail override's JSON is *derived* from the tracked `.sexp` on every run — byte-identical to
the original it replaces, the `.sexp` the single source of truth. `compare_readers` sweeps 28
of 28 files across all three readers. Measured en route: the DOSSIER's "no gate has been run"
was stale (`G0` has run; verdict `incomplete`) — corrected; `schema/` reached its file-count
ceiling at exactly 12 and was re-derived to 24, grounds recorded in the registry; the
`profiles/` per-part re-derivation `.3` carried open was not needed (`references.sexp` is
30,012 B against 32,768).

====

## SEMILITH-SF-0058 (leaf SOT-FORMAT.3) — the records move behind the schema layer

`profiles/rv64i-lab-v0/{requirements,contract-obligations}.jsonl` (26 + 34 records) retire into
`{requirements,contract-obligations}.sexp`, one form per record, JSON keys verbatim as field
names. The losslessness the acceptance demands is a comparison, not a review:
`convert_records.py --verify` re-derives the JSONL from the converted files **byte-identical**,
field by field, both catalogues.

⭐ **The schema layer grew four field facets rather than go weaker than the contract it
replaces** — `(pattern …)`, `(min-length N)`, `(min N)`, `(unique yes)` on `(field …)`, the
`.2` boundary one level down (a new declaration KIND would change the kernel; facets on the
existing kind are the language; the fixpoint declares them). And `parameters` stopped being a
lie: the old JSON schema's `additionalProperties` banned the very arrays three obligations
write and the validator never descended into it — the new format types every value
(`(int …)/(str …)/(true)/(false)/(null)/(ints …)/(strs …)`) and refuses a float, a mixed list
or a nested value by name.

**`RECORD-SCHEMA` reads both tracks now**: the frozen `examples/` JSONL on the tracked JSON
validator; the converted catalogues through the single mapping owner `scripts/records_sexp.py`,
validated by the schema layer plus every cross-check (CITED / RESOLVED / COVERAGE / LINKED /
OBLIGED / AUTHORITY) re-fired against the converted form — 22 arms where 15 stood, each RED arm
naming its reason. `gate_report.py` reads the same mapping; the G0 report diff is input names
only (26 requirements, 34 obligations, 68 checks, verdict untouched). `compare_readers` sweeps
13 of 13 with the catalogues and the two new schemas in corpus; `run_smoke` and the 52-of-52
verdict are unmoved. Measured en route: `LIVE_STATUS.md` had carried the contract as 33
obligations / 66 checks since before `P0-PROFILE.10`; re-derived to 34 / 68.


## SEMULITH-DS-0002 (leaf DOC-SHARDING.1) — the fired ceiling gets its sharder, and the freeze gets its proof

**Measured trigger.** `CHANGELOG.md` sat at 65,527 of 65,536 bytes — 9 bytes of headroom, recorded
at adoption as transition debt with this leaf as its named owner. The registry's owner column
promised *shard when the ceiling fires*; this slice is the sharder, not another compressed entry.

**What landed.** `scripts/shard_history.py` moves the oldest whole `## ` entries — byte-verbatim,
a file is preamble plus concatenated blocks, so head-after + shard == head-before exactly,
asserted and printed at the event (29 entries: 28 kept + 1 moved, order and bytes exact). One
entry moved (`SEMILITH-P0-0031`, 3.4 KiB); the head rewrote 65,527 → 62,086 bytes, under target
with room for this entry. Re-running is a no-op. The two existing date-named shards stay
untouched — a shard's entries are never edited — and join the new freeze manifest
`docs/changelog/SHARDS.sha256` (3 rows, sha256sum format, paths repo-root-relative).

**`SHARD-FREEZE`** — the 13th project doctrine, 12 self-test arms, each RED arm naming its reason —
proves the durable half: every shard hashes to its manifest row (one edited byte after the event
fails with both digests named); the manifest only grows against `git show HEAD:…`; no `## `
heading appears twice across head and shards. ⛔ Fired RED on the real tree before registration:
with no manifest yet, both existing shards reported `UNMANIFESTED` — the adoption gap itself, not
a synthetic stand-in. ⭐ The completeness proof belongs to the shard event (the tool holds both
sides exactly once); the freeze proof belongs to the manifest (it holds every side forever) —
splitting the two halves is what makes each half checkable.

**Lockstep, because mirrors rot.** Both doctrine mirrors gain the row (`DOCTRINE_ENFORCEMENT.md`
and the book chapter, per `REGISTRY-MIRROR`); `LIVE_STATUS.md`'s derived counts move 12 → 13
doctrines and 157 → 169 self-test arms — re-derived by `check_derived_counts.sh --list`, never
incremented by hand; `README_POLICY.md`'s transition-debt note records the discharged half and
leaves `DEV_NOTES.md` its still-live trigger for the day its ceiling fires.

## SEMULITH-RM-0060 — browser/Wasm target

`decision_browser-wasm-target`; lane `PORT-WEB` (consumed by `P1-LAB`).

## SEMILITH-SF-0057 (leaf SOT-FORMAT.2) — the constructs already in use, declared as data

The schema layer leaves paper: `schema/encoding.sexp`, `schema/fragment.sexp` and
`schema/semantics.sexp` declare every construct the three corpus families write — records and
positional mini-languages alike. The schema language gains exactly one new declaration kind,
`(operator (name SYM) (fixed N) | (variadic) [(min N)] [(arg SPEC)])`, for the shapes no record
grammar can state: `(fixed (31 25 0x0) …)` triples, `(operands rd rs1 rs2)` lists, the
`(pieces (12 12) …)` pairs, and the semantics effect expressions. `scripts/check_semantics.py`
now loads its 32-form table from `schema/semantics.sexp` — a new semantic form is a schema
edit, zero lines of Python (demonstrated with a 33rd form, then reverted). The `52 of 52`
verdict is byte-identical; the four MODEL-METHOD.9 controls still fire RED. Kernel self-test
`16 → 31 arms`; the whole corpus validates against its schema; `compare_readers` sweeps the
three new files the moment they are tracked (`9 of 9 agree`, document layer zero class notes).
The layer that never reads a second file: operand scoping stays in the checker. Gate
registration stays deferred to `SOT-FORMAT.6` per the tree's frontier. Tree `SOT-FORMAT` at
5/10.

## SEMULITH-RM-0059 (leaf ROADMAP-V3.3) — ROADMAP v0.3: the star gets a start condition

`ROADMAP.md` supersedes v0.2 (the house pattern: the delivery manifest and git carry the old
bytes; v0.2 was `live`, so no disposition change was needed). v0.3 lands the adopted package:
P1's start condition (`SOT-FORMAT.2` constructs + `MODEL-METHOD.10` extraction contract — the
remaining format-migration leaves are consumed by later milestones, not by P1's start); the
execution-authority row in the §1 decision table (semantics are data and the data executes);
the lane-consumption rule in §1; P1's G1 sharpened to the star-facing proof — a compiled
freestanding guest program retires under first-divergence comparison, C named as the first
guest path, and the first mdBook increment ships in the same milestone; the v0.4 trigger moves
to P1 first-slice completion. Under review, `LIVE_STATUS.md`'s `MODEL-METHOD` count was
re-derived: `3/10` (a spelling no gate can see) → `6 of 13` (the gated spelling). File: 24,065
bytes against the 24,576 ceiling. Tree `ROADMAP-V3` complete, 3/3.

## SEMILITH-RM-0058 (leaf ROADMAP-V3.2) — every lane names the milestone that consumes it

The sequencing vacuum, measured rather than asserted: `27` commits since any milestone tree
was last touched, and that touch was P0 closure. The roadmap's warning ("evidence tooling does
not become an unrelated research product") becomes an operational rule: every cross-cutting
tree's Metadata declares `Consumed by:` — milestone plus latest consumption point; lanes
without a named consumer are descoped at the next roadmap revision; new lanes must name a
consumer at proposal. First application covers all seven current lanes. The mechanical census
gate is **proposed to the director, not registered** — new governance is announced before it is
tasked. Record: `docs/decisions/decision_lane-consumption.md`; tree `ROADMAP-V3` at 2/3.

## SEMULITH-RM-0057 (leaf ROADMAP-V3.1) — the semantics data is the execution authority

Director-delegated decision (`2026-09-27`: "the decision is yours to make but it got to be sota,
signoff and production-grade") resolving the open contradiction between `docs/ARCHITECTURE.md`
§1.1 (semantics are data) and §2 (canonical Rust semantic functions): P1 executes the 32-form
semantics data directly — a definitional interpreter, keeping exactly one owned implementation
per rule (OWN-01); compiled or IR handlers enter only as generated, fingerprinted artifacts
behind an observational-equivalence regression. The pattern is the one this project's own pinned
Sail reference uses: the interpreter is the reference behaviour; compilation of the same
semantics is a derived artifact that must agree with it. Revisit conditions named: a measured
P2/P4 performance need, or the explicit semantic-IR migration decision. Record:
`docs/decisions/decision_interpreter-before-compiler.md`; tree `ROADMAP-V3` registered (1/3).

## LS-002 → `verified` — the design question closes with a re-run, not a changelog

Upstream confirmed the kind-strict grammar (`77d7b3db1`) and the native adapter (`df845ce61`)
are ancestors of the published pin `a8d34c845` — checked mechanically here with
`merge-base --is-ancestor`, not taken on their word — and prescribed the verification
instrument: `sexpr_file` with `SExprDocumentV1.spec` (the old `lispish_file` adapter is
insufficient). That instrument is exactly what `SOT-FORMAT.10` just added: LS-002's own four
cases re-run through the document layer return distinct kinds for every quoted/bare pair, and
the consumer's whole corpus agrees with its canonical reader there with zero classified
residue. The record gains the `verified-against` pin and the captured transcript; `VERIFIED.md`
carries the reply to upstream in the same envelope as the report. All three of this project's
LinkedSpec issues are now `verified`.

## SEMULITH-SF-0056 (leaf SOT-FORMAT.10) — the document grammar joins the agreement sweep

Director decision on the recorded candidate: adopt SExprDocumentV1 **additively** — a third
reader in `compare_readers.py`, never a replacement. The Lispish layer stays as what it is (the
LS-001/LS-002 regression guard, CLASS notes and all); the new document layer answers both CLASS
families by construction — tagged kinds keep `"20260911"` a `string` (quoted-numeric cannot
arise), raw lexemes decoded on OUR side with sexp.py's own escape table (escape-retention
cannot arise) — and it compares **every** form in every file, not the first. 28 self-test arms
(7 new), and the falsifiable acceptance was exceeded: **6 of 6** tracked files agree in the
document layer with ZERO class notes, because `schema/schema.sexp` itself joined the corpus and
passes both layers — the schema language's fixpoint now also verifies through the document
grammar. Upstream's instruction for LS-002 verification ("use `sexpr_file` with
`SExprDocumentV1.spec`; the lispish_file adapter is insufficient") describes exactly this
layer — which is what the next commit uses to close LS-002.

## SEMULITH-UT-0055 (leaf UPSTREAM-TRACK.4) — the reply travels in the same envelope

Director instruction `2026-09-26`: the verification acknowledgment to LinkedSpec is a
git-tracked note inside the bug's own directory. The subtree was already the envelope a
maintainer copies out — `VERIFIED.md` is now the reply inside that envelope, beside the report
it answers: what shipped, what we re-ran against which pin, the result, what it unblocks, and
where the residue lives (for LS-001: classified under LS-002, not this defect).

The note is gated, not just written: `UPSTREAM-INDEX` refuses a `verified` state whose subtree
carries no `VERIFIED.md`, and refuses a note that does not name the pin the record was verified
against — the note and the record must agree the way the indices and the record must agree.
Fired RED on the real tracker against both LS-001 and LS-003 before the notes existed; 17 arms
(16 → 17) with the wrong-pin refusal; green after, both notes self-contained and pin-consistent.

## SEMULITH-SF-0054 (leaf SOT-FORMAT.1) — the schema language, written in itself

The gap was "it parses": an S-expression reader accepts anything syntactically, so a mistyped
head or field was invisible. `schema/schema.sexp` now declares the language in itself —
`(construct (name …) (field …)…)`, atom fields, form fields in the corpus's two house shapes
(`(source (file …) …)` whole-list and `(effect (set …))` value-held), `(empty yes)` markers
for the corpus's `(requires)`/`(extensions)` idiom, `(values …)` spellings, sibling repetition —
and `scripts/check_sexp_schema.py` (16 arms, 13 RED, each naming its construct, field and
reason) validates any file against any schema. The fixpoint is the proof, not a slogan:
`schema.sexp` conforms to `schema.sexp`.

⭐ The first design assumed a tidy uniform `(name value)` pair grammar — and the real corpus
refuted it before it shipped. Reading `rv64i.sexp`/`rv64i.sem.sexp` first is what made the
language fit the files `.2` must declare; an invented grammar would have met the corpus as an
argument. `schema/` is registered in `doctrine/readme_routes.tsv` in its creating commit, and
`TOOLBOX.md` gains the row.

## SEMULITH-SF-0053 (leaf SOT-FORMAT.8) — the contract names its format at last

The mdBook chapter *"Architecture and canonical definitions"* includes `docs/ARCHITECTURE.md`
verbatim, and that document named no format, no `definitions/` directory and no composition —
four commits had introduced all three, and the director's only window showed none of it
(`grep -c 'S-expression'` → 0). The drift is closed at the source document: §1.1 records the
one-format decision and what exists in it today (fragments, cited semantics at 52 of 52, the
two-reader agreement check), §1.2 defines the fragment and the composition operator that is
*decided, not hoped* (`check_encoding_disjoint.py`), §1.3 states the schema layer's contract and
labels it specified-not-built. Built claims name their instruments; pending layers say pending;
the one count that moves (`5 of 5`) was rephrased to "agreement file by file" so the prose
cannot drift. `make book` builds; the chapter preface needed no edit — that was the point.

Also: a knowledge card for the session's other lesson — a director-named action runs first,
right after context recovery; standing cadences queue behind it.

## SEMULITH-UT-0052 (leaf UPSTREAM-TRACK.2) — `verified` must carry the re-run that earned it

The tracker already refused a `verified` with no pin. It now refuses the next hole too: a
`verified` whose event names a pin but captures no `(repro …)` output **inside the subtree** —
the pin retires upstream's changelog claim, but only the captured run retires ours. Four new
self-test arms (pin-without-repro, artifact missing, artifact escaping the subtree, pin+artifact
accepted); `16 pass / 0 fail`.

⛔ **Fired RED on the real tracker before any artifact existed** — the strengthened gate refused
LS-001's just-committed `verified` ("captures no (repro …) re-run output", rc=1). Then the
evidence landed and every state became earned, not asserted:

- **LS-001 → `verified`** — the reproduction re-ran and was captured into the subtree itself:
  `evidence/verified-a8d34c845.txt`, `8 matched / 0 differed`. A maintainer copying the issue
  directory out now carries the proof with it.
- **LS-003 → `verified`** — the three first-consumer papercuts are remedied in the guide at the
  adopted pin, and each remedy was *exercised* during the pin update (workspace exclusion,
  prerequisite chain, maintained wrapper), transcript captured — exit statuses, not banners,
  per the guide's own warning.
- **LS-002 → `acknowledged`** — upstream took ownership by name: the LS-001 fix commit records
  "LS-002 and related kind/strict requirements remain .83.1 owned". No re-run owed; the design
  question is theirs until it ships.

## SEMULITH-SF-0051 (leaf SOT-FORMAT.9) — the pin moves, the readers agree, the loop closes

Director instruction `2026-09-26`: upstream fixed and pushed the reported bugs, so the LinkedSpec
pin advances `ad290bdb4` → `a8d34c845` (`origin/main` tip, ~120 commits). The update followed the
guide's own flow — fetch, check out the reviewed revision, re-verify, THEN commit the pointer.
RGX stays at `8763a0e6` on both pins (bootstrap: "already generated", a no-op); the consumer
rebuilt in 20.39 s.

**LS-001 is `verified`, not just `fixed-upstream`.** Our self-contained reproduction re-ran
against the new binary and grammar: `8 matched / 0 differed` (was 4/4), and both readers now
agree on **all five** tracked `.sexp` files, including the 43-form catalogue that had read as 6.
The issue record, both index mirrors and the REPORT carry the `verified-against` pin the
UPSTREAM-INDEX gate requires.

**The fix moved the disagreement one layer down, and that layer is enumerated, not hidden.**
The corpus census found exactly four residue atoms in `materials/catalog.sexp`: two
quoted-numeric strings (`"20260911"`, `"1992"` — Lispish discards quote-kind, LS-002) and two
escape-retained strings (`\"` kept verbatim — the guide documents this). Both are CLASS families
in `compare_readers.py` now: each is anchored to exact byte meaning (`sexp._atom(A) == B`
exactly; decoding B with sexp.py's own escape table reproduces A exactly), with 9 new self-test
arms (4 GREEN classification, 5 RED masking) and a fired RED proof — the pre-fix grammar still
makes the comparator report the original 43-vs-6 defect, rc=1. "Agree" still means same structure.

**Named departure, one.** The guide now prescribes copying the consumer source into the
application's crate; semulith builds the vendored example workspace in place (virtual root
manifest has no package to own it) — recorded in the tree, to revisit when the engine adopts the
reader. Upstream's document grammar (SExprDocumentV1, tagged kinds) is the durable answer to both
CLASS families when that day comes.

## SEMULITH-AC-0050 (leaf ARTIFACT-CLEANUP.1) — the first §8 cleanup, measured and recorded

Session-directive §8 requires an artifact cleanup roughly every 24 h, tracked in
`docs/ARTIFACT_CLEANUP.md`. The file did not exist — the "no file → clean this session" trigger
fired — so the cleanup owns a task-tree now, the same as any other change.

**Census before deleting anything** — 22 `.bin` under `target/`, 18 under `.app-data/target/`,
all of them cargo incremental caches in the directive's enumerated scope; 7 crate **source**
fixtures under `.app-data/cargo-home/` (inputs, not artifacts — kept); 13 reference-run logs
under `target/refs/` (kept: evidence trails, 1.3 MB, outside the enumerated cargo dirs).

**Measured, not asserted:** 40 files / 341 MB deleted (`.app-data` 1.4 G → 1.1 G); zero after;
`git status` shows only the intended tracked files. The record is overwrite-only — one date and
one line per run, so the file can never become the changelog it exists to prevent — and it is a
governed live surface from its first commit (registered in `doctrine/readme_routes.tsv`).


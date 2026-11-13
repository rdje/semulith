# CHANGELOG.md

## SEMULITH-P4-0404 (leaf P4-SYSTEM.20 slice a2) — a board's processor version is held to the unit's identity

The processor pin is unit, version and dossier digest, and the platform generator checked the unit and the digest but never the version. It now holds the version to the unit's `identity.sexp` and refuses a unit with none; two RED arms prove both. The closed `.15` to `.19` records and rows moved verbatim to archive part 38, which takes the P4 tree from 128,577 to 96,808 B.

## SEMULITH-P4-0403 (leaf P4-SYSTEM.20 slice a) — the version label leaves the pinned file, and the 42 credits it lapses are retired

`identity.sexp` in every profile now holds the version and status, which no case pins; `profile.sexp` and its schema lose them, and the report reads the identity. rv64gc is version 1, in development. The 42 case credits the move lapsed are retired (recoverable at a88b01a0) and their requirements read `planned`, so `CPU-SYSTEM` reads `incomplete` with four owned open axes until slice f; version 0 stays verifiable at `194437d6`. The report's decision controls no longer depend on the real unit's credits.

## SEMULITH-P4-0402 (leaf P4-SYSTEM.20, slice a brief) — a lapsed credit is a gate finding, so the slice that lapses one retires it

Measured on a clone: one comment line in `profile.sexp` makes the requirement-status derivation refuse, 42 drift and 42 findings, on every commit. The window's slices a to f therefore retire what they lapse, as a49-1 did, and slice f re-issues the 46 credits that stand at `194437d6`. The release identity becomes `identity.sexp` in every profile, since three have no `gate.sexp`.

## SEMULITH-AC-0099 (leaf ARTIFACT-CLEANUP.43) — the cleanup tools' usage text, which the book shows, says what is true today

Four usage blocks the book includes said that work finished on 2026-10-20 was pending and copied self-test counts the driver no longer held (100 outcomes where it measures 168); the toolbox and the doctrine row had the same drift. They now state the present and name the driver for the counts. Measured: editing a pinned source leaves selection approving 0 until the next capture, then 6 again.

## SEMULITH-AC-0098 (leaf ARTIFACT-CLEANUP.38) — the cleanup tree's completed checklists retire into a third ledger generation

The live narrative stood at 14,616 B, 129 B under the point where ordinary growth stops. Generation 3 retains df8f4043's live tree whole and its exact 15,120 B suffix, the chain re-derives generation 2's descriptor, and the live narrative is 2,814 B. The probe's latest-predecessor leaf count is re-pinned from 23 to 42, as `.23` re-pinned it from 19.

## SEMULITH-AC-0097 (leaf ARTIFACT-CLEANUP.41) — the fourteenth recurring cleanup

At 93 h, on a clean tree: the orphan act removed 21 directories (496,149,522 B), then 67 candidates planned and 6 captured Cargo incremental outputs (15,766,338 B) removed, residue 0. The 4 scratch repositories under `target/` are all known keepers: no landed unit left a clone.

## SEMULITH-XTASK-0091 (leaf XTASK.18) — the chain accepts a colon after the work-unit number, and says what it wants

`cargo xtask commit-unit` refused `SEMULITH-LC-0056: …`, which the commit-msg hook accepts, and its refusal gave no reason. It now accepts a space or a colon after the number, and a refusal prints the shape it wants and the first line it got. The XTASK turn after five feature units.

## SEMULITH-P4-0401 (leaf P4-SYSTEM.20) — the next pinned window is version 1: what each item lapses, and the label that should not

Measured on a throwaway clone: the expectations author, the state table and `profile.sexp` each lapse 42 of 46 credits; the override and the contract lapse none; the state table also moves the engine. The version label sits in a file every case pins, so the window first moves it out. Eight slices; version 1's hosted run needs a push. A stale goal clause I had written is corrected.

## SEMULITH-P5-0020 (leaf P5-BOARD.13) — a board on the accepted processor needs a processor contract that admits devices

Measured before composing: `rv64gc-lab-v0`'s effective contract has 10 environment assumptions, and `OB-GC-ENV-DATA-ACCESS` admits only main memory, with no MMIO. No board with a device composes version 0. The call: the device-region supersession rides in the next pinned window (`P4-SYSTEM.20`), and the netboard re-bases onto that version rather than a second board. `.13` is blocked on it.

## SEMULITH-P4-0400 (leaf P4-SYSTEM.19 slice a) — the scalar unit's recorded runs are held to what they cover, and measured again

The CPU-LAB report now reads `rv64i-lab-v0`'s recorded runs from a `gate.sexp`, each held to what it covers by the verifier the CPU-SYSTEM report uses. Portability re-measured on all four legs (`3fbc498e…` over 49 guests, as both hosted hosts gave), the hosted run recorded, and the ACT4 campaign of 2026-09-30, read as stale by name, run again: 51 pass. The netboard re-pinned deliberately; `.20` owns the next pinned window.

## SEMULITH-P4-0399 (leaf P4-SYSTEM.18 slice c2b) — rv64gc-lab-v0 version 0 is accepted, and CPU-SYSTEM reads passed

The release decision is recorded: `accepted` for version 0, pinned to the dossier's digest, with eight capability limits in `gate.sexp`; the report verifies it and reads `passed`, 10 of 10 axes. The dossier's stale sentences were corrected before the digest was taken. README's claim scope and the book's claim page say what is and is not claimed. The netboard composes the scalar unit, so `P5-BOARD.13` owns a board on the accepted processor.

## SEMULITH-P4-0398 (leaf P4-SYSTEM.18 slice c2a) — the terms of what the release ships and relies on are recorded, and OQ-1 closes

The dossier said its terms were due at the first release candidate, and three cited sources read `unrecorded`. Read from each document: the psABI and the SBI are CC BY 4.0; the FU540-C000 manual is CC BY-NC-ND 4.0, so it is cited, never redistributed. All 30 retained excerpts are named by a retention record. OQ-1 closes by census.

## SEMULITH-LC-0056 (leaf LIVE-CONTAINMENT.4) — the changelog sharded, and the leaf's frontier status corrected

The 17 oldest entries moved verbatim into `docs/changelog/shard-0425.md`: the head went from 64,229 B to under 49,152 B of its 65,536 B ceiling. `LIVE-CONTAINMENT`'s frontier row said `.4` was `pending` where the leaf and the index say `active`. `XTASK.18` opened: the chain refused this unit's first subject, which the hook accepts.

## SEMULITH-XTASK-0090 (leaf XTASK.16) — a check runs when its driver changes, and the chain runs the tests

The gate could answer six heavy checks from their last green run on a commit that changed only their own drivers, because no declared input named `xtask/`. Now a check skips only when every staged path is ledger documentation. All 42 doctrines pass unskipped on the tree. The focused set runs `cargo test --all`, which nothing ran at a commit before.

## SEMULITH-XTASK-0089 (leaf XTASK.15) — the commit chain and its sweep are tracked

`cargo xtask commit-unit <dir>` lands a unit: it reads the message first, runs the focused set, commits under the hooks, empties the message and sweeps the unit's scratch. Before, both were untracked shell files under `target/`. Its git ignores a hook's repository variables, shown on a decoy repository.

## SEMULITH-P4-0397 (leaf P4-SYSTEM.18 slice c1) — a release decision is held to the unit, the dossier and the report

A decision row used to need only a tracked file. Now the record pins the unit, the version and the dossier's digest, and `accepted` stands only over nine green axes, a native x86-64 record and a declared limit. No decision is recorded yet; on a clone with the real dossier the report reads `passed`.

## SEMULITH-P4-0396 (leaf P4-SYSTEM.18 slice b) — the hosted run is a record, and the report shows the native x86-64 leg

Run 42418631491 on the pushed tree: x86-64 and arm64 hardware each pass 519 tests and give the same digest over 210 guests, equal to this host's. `scripts/hosted_matrix.py` freezes it into the dossier, tied to the tree. Found on the way: the scalar unit's portability record is stale (`P4-SYSTEM.19`), and the record's "suites" were tests.

## SEMULITH-AC-0096 (leaf ARTIFACT-CLEANUP.40) — the thirteenth recurring cleanup

At 61 h, on a clean tree: the orphan act removed 17 directories (576,723,648 B), then 139 candidates planned and 6 captured Cargo incremental outputs (15,766,339 B) removed, residue 0. Outside the plan, 21 scratch clones that landed units had left (524,516 KiB) are gone and the sweep that missed them is fixed; `XTASK.15` will track it.

## SEMULITH-P4-0395 (leaf P4-SYSTEM.18) — what the director said, and D79 needs no `sudo`

The director's words of 2026-11-07 are on the record: technical questions are the engineer's to settle, and the one push is allowed as an exception. D79's capture of 2026-10-17 is intact, so it needs no `sudo`.

## SEMULITH-P4-0394 (leaf P4-SYSTEM.18) — the release decision comes before the next pinned window

No item on the window's list changes a claim any credit makes, so each goes into the capability limits by name and the window follows as its own version. The director may reverse the order. What remains is a hosted run, which needs a push the director approves, and then the named decision.

## SEMULITH-P4-0393 (leaf P4-SYSTEM.18 slice a) — a recorded row states what it covers, and portability re-measured

`G-PORTABILITY` read green on a record of 168 guests with 210 in the tree. Each row with a recorded verdict now states what it covers and stops being evidence when that moves. Portability was re-measured over the 210: all four legs green, the x86-64 manifest byte-identical.

## SEMULITH-XTASK-0088 (leaf XTASK.13 slice j) — UNIT-BOOKS' probes judge a fixture of their own

The navigation probe's command-line tests ran the real tool, so a damaged real registry read as a probe that failed. They now run a copy inside the fixture, and the same damage fails by its own name.

## SEMULITH-P4-0392 (P4-SYSTEM.14 a51-14) — the four with nothing to run credited, and `G-OBLIGATIONS` closes

Each on a selection's record: 46 `implemented`, 2 `not-applicable`, none `planned`. `CPU-SYSTEM` reads 1 of 10 axes open, `G-RELEASE`, and a closed axis grants no release.

## SEMULITH-P4-0391 (P4-SYSTEM.14 a51-13) — the four with nothing to run measured once each

Each record taken once: all 25 facts read their declared value, and all 11 runs exited 0 and repeated byte for byte. Nothing is credited yet.

## SEMULITH-P4-0390 (P4-SYSTEM.14 a51-12) — the four with nothing to run declared, each fact with its expected value

`REQ-D-ABI`, `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP` and `REQ-D-SCOPE-CENSUS`, declared before anything runs. Measuring found all 44 retained guests are tagged soft-float, on purpose, so the ABI statement holds for what the compiler builds, and the record names that as a limit.

## SEMULITH-P4-0389 (P4-SYSTEM.14 a51-11) — track 4's tool: a credit may name a selection's record

Four requirements have nothing to run. A credit may now name a selection's record in place of a case: facts declared before anything runs, one measurement retained, and each read reading the facts again. Nothing is credited yet.

## SEMULITH-AC-0095 (leaf ARTIFACT-CLEANUP.39) — the twelfth recurring cleanup

At 24 h, on a clean tree: the orphan act removed 1 directory (62,595,188 B), then 169 candidates planned and 6 captured Cargo incremental outputs (15,766,339 B) removed, residue 0.

## SEMULITH-P4-0388 (P4-SYSTEM.14 a51-10) — the four with no switch credited

`REQ-D-ENDIAN`, `REQ-D-FENCE`, `REQ-D-WALK-IMPLICIT` and `REQ-GC-PARTIAL-PROGRESS` at 11 of 11 legs, each on a declared disposition because the pinned reference offers nothing to select otherwise: 42 `implemented`, 4 `planned`, 2 `not-applicable`.

## SEMULITH-XTASK-0087 (leaf XTASK.13 slice i) — RECORD-SCHEMA judges a frozen copy, and a damaged real schema is named

The controls read the real grammars, so damage read as a check that cannot discriminate. They now read a frozen copy, and a real step before the judge names each real facet and document that fails. Measuring also found a JSON schema that is not JSON crashed the judge into an empty report: it now refuses, naming the file.

## SEMULITH-P4-0387 (P4-SYSTEM.14 a51-9) — the four with no switch captured exactly once each, and the walks compared

Each once, each control where declared, the walk record retained: all 42 compared files byte-identical to the rehearsal, no finding.

## SEMULITH-P4-0386 (P4-SYSTEM.14 a51-8) — the four with no switch declared, each with its disposition, and a call corrected

`REQ-D-ENDIAN`, `REQ-D-FENCE`, `REQ-D-WALK-IMPLICIT` and `REQ-GC-PARTIAL-PROGRESS` get real cases, rehearsed at 11 of 11 legs. Each has a declared disposition and keeps the category its source gives it: a51-0's move to `source-specific` was wrong, and the mirror rule caught it.

## SEMULITH-P4-0385 (P4-SYSTEM.14 a51-7) — track 3's tools: a declared disposition is a row the review reads, and a walk's reads are compared

The policy's `source-specific` row now reads a declared record, which must name the case's own control. `semulith run --trace-walks` and `scripts/measure_walk_trace.py` compare what a walk reads on both producers. `credits.sexp` went from 63,828 B to 54,439 B, with one repeated sentence moved to its header.

## SEMULITH-P4-0384 (P4-SYSTEM.14 a51-6) — the two with a switch credited

`REQ-D-NO-H` and `REQ-D-NO-PMP` at 11 of 11 legs, each measured against a hart that has what the profile excludes: 38 `implemented`, 8 `planned`, 2 `not-applicable`.

## SEMULITH-P4-0383 (P4-SYSTEM.14 a51-5) — the two with a switch captured exactly once each, each effect at a witness

Each once, each control where declared, each effect retained: all 22 compared files byte-identical to the rehearsal, no finding.

## SEMULITH-XTASK-0086 (leaf XTASK.13 slice h) — CONTRACT-FREEZE judges a frozen unit, and a lost contract is named

Measuring first found the self-test was the only thing catching a deleted contract: the judge alone read `ok (0 versioned unit(s))`. The judge now names it, and the controls read a small frozen unit, so a damaged real contract fails by its own name.

## SEMULITH-P4-0382 (P4-SYSTEM.14 a51-4) — the two with a switch of the last 17 declared

`REQ-D-NO-H` and `REQ-D-NO-PMP` get real cases, rehearsed at 11 of 11 legs: a hart with H differs at `misa`, and a hart with 16 PMP entries at a load at S's privilege. The alternative gains `pmp_count`.

## SEMULITH-P4-0381 (P4-SYSTEM.14 a51-3) — the first six of the last 17 credited

Six credits at 11 of 11 legs each: 36 `implemented`, 10 `planned`, 2 `not-applicable`. `REQ-GC-PRIV-INSNS`, which the route expected to end `partial`, reads `implemented`, with what stays out named.

## SEMULITH-P4-0380 (P4-SYSTEM.14 a51-2) — the first six of the last 17 captured exactly once each, through the tracked guard

Each once, each control where declared, all 60 compared files byte-identical to the rehearsal: no finding. The first real use of `scripts/capture_guarded.py`.

## SEMULITH-P4-0379 (P4-SYSTEM.14 a51-1) — the first six of the last 17 declared, and the reference's wfi turned on

Six cases, 68 witnesses, each statement traced clause by clause and rehearsed on a clone: 11 of 11 legs each. The override's `wfi_is_nop` had been hiding the reference's `wfi`; with it off, all 345 steps of the privileged forms agree, including `wfi` refused under `TW`.

## SEMULITH-P4-0378 (P4-SYSTEM.14 a51-0) — the last 17 called, and measuring the reference overturned the route's reading of them

Each of the 17 now has a route. The pinned binary has switches and traces the route assumed it lacked, so most get real cases, not arguments. `REQ-D-SBI` moved out of the CPU's scope to `P6-LINUX.2`: 30 `implemented`, 2 `not-applicable`, 16 `planned`.

## SEMULITH-XTASK-0085 (leaf XTASK.13 slice g) — EXERCISE-COVERAGE judges frozen fragments, so a damaged real one names itself

A deleted or broken definition fragment used to make the check refuse as non-discriminating, pointing into its own scratch copy. Its controls now read frozen copies, so the real check fails by the fragment's own name, on all five damaged states measured.

## SEMULITH-P4-0377 (P4-SYSTEM.14 a50-c2) — the capture guard is a tracked tool, and it held on a real run

`scripts/capture_guarded.py` replaces a script that lived under `target/`: 22 tests, 17 mutations caught, and seven real captures on a clone byte-identical to the retained ones. `probe_config_effect.py` now reads all ten retained effects, not three.

## SEMULITH-P4-0376 (P4-SYSTEM.14 a50-c1) — the CLI reads what its usage says

`semulith run x.elf --steps 3` now works, as the usage always said: `--name VALUE` and `--name=VALUE` are one request for every value option, a missing value is refused by name, and a test holds the option list to the parsers and the usage.

## SEMULITH-P4-0375 (P4-SYSTEM.14 a50-4) — the seven credited, each measured against what selects otherwise

Seven credits at 11 of 11 legs each, every selection shown to change something at a declared witness: 30 `implemented`, 17 `planned`, 1 `not-applicable`. All 17 left end at a ruling. `G-TRACE` lists all 30.

## SEMULITH-P4-0374 (P4-SYSTEM.14 a50-3) — the seven captured exactly once each, the guard's load limit measured, and a CSR write census

Each of the seven once, each control where declared, each effect retained: all 77 compared files match the rehearsal, no finding. The capture guard's load limit moved from 8 to 32 on 0 refusals in 210 rehearsed captures at load 15 to 73. A census of CSR writes found a defect in the pinned expectations author on `medeleg`, `mtvec` and `stvec`, which no retained expectation reaches and the next window fixes.

## SEMULITH-P4-0373 (P4-SYSTEM.14 a50-2) — the seven with a real switch, declared, and what writing them found

Seven cases, 149 witnesses, each statement traced clause by clause and rehearsed end to end on a clone: 11 of 11 legs each. The work found a setting the pinned override lacks: a misaligned AMO judged before translation, which no guest had exercised. Two cases select it themselves, and the override moves with the next window.

## SEMULITH-P4-0372 (P4-SYSTEM.14 a50-1) — a case may declare what selects otherwise, and its effect is measured against that

For a requirement whose selection is already the profile override there was nothing to compare it with. A case can now state the other choice, in a closed vocabulary measured against the pinned binary, and the same guest runs under it. No case declares one yet, and no credit moved.

## SEMULITH-P4-0371 (P4-SYSTEM.14 a49-4) — the superseded cases leave the tree, listed, and the list reads back from history

23 directories and 16 overlay and effect files are out, 3.8 MB; `evidence/` holds 25 cases and 23 credits stay current. A new book page lists all of them and a test reads each row back from history. The book's runnable examples, which had drifted at a49-3, name today's cases with re-measured numbers. The window that carries fetch faults closes.

## SEMULITH-XTASK-0084 (leaf XTASK.13 slice f) — MATERIALS-BILL's controls judge frozen dossiers, and a lost board definition is named

A deleted dossier file, device source or board definition, or an edited bill, used to make the doctrine refuse itself with no name, and now fails by its unit's name. The self-test reads 29 frozen files, 245,396 B, and two tracebacks became refusals.

## SEMULITH-XTASK-0083 (leaf XTASK.14) — a killed gate cannot block a cleanup: printable prefetch keys

The prefetch named its record files with control characters, so a gate that died left names the artifact census refuses, and one killed gate blocked every later cleanup. Keys are percent-encoded now, on both sides, and a new arm holds the two equal. Over a whole self-test: 0 misses.

## SEMULITH-AC-0094 (leaf ARTIFACT-CLEANUP.37) — the eleventh recurring cleanup, and a defect its census found

At 24 h, on a clean tree: the orphan act found 0, then 133 candidates planned and 6 captured Cargo incremental outputs (15,766,340 B) removed by the guarded core, residue 0. The first plan refused: a gate that died left self-test files named with control characters, so any killed gate could block every later cleanup. That residue is removed, and printable record keys are next, `XTASK.8`'s.

## SEMULITH-P4-0370 (leaf P4-SYSTEM.14 a49-3) — 23 credits under eleven legs, G-STATE and G-TRACE restored, and Batch II-b implemented

The 19 re-issued and REQ-GC-ATOMICS, REQ-GC-C, REQ-GC-F and REQ-GC-D new, each case 11 of 11 legs: 23 implemented, 24 planned, 2 of 10 axes open. REQ-GC-C witnesses its second-parcel fetch fault.

## SEMULITH-P4-0369 (leaf P4-SYSTEM.14 a49-2) — the window's 23 cases captured exactly once each, and no behaviour moved

Each once from the declaration commit, each control where declared. All 153 files compared with the 17 unchanged predecessors are byte-identical, every compared file matches its rehearsal, and the three effect traces match theirs: no finding.

## SEMULITH-P4-0368 (leaf P4-SYSTEM.14 a49-1) — the window opens: a case carries a fetch fault, the review reads every clause, and 23 cases declared on it

A wordless boundary may now be a fetch fault. An eleventh review leg holds every clause of a requirement's statement to a witness or a stated limit, and it found five clauses the ten legs had passed. All 19 credits are retired until a49-3, and 23 cases are declared, F and D with up to 93 witnesses. Self-test arms that named real cases now judge a stub, so no later window breaks them.

## SEMULITH-P4-0367 (leaf P4-SYSTEM.14 a49-0) — the director's ruling recorded, a call reversed on its measurement, and the window proved on a throwaway clone

The calls on the engineer's findings are the engineer's, to the director's standard. Three planned requirements state a fetch fault, not one, so a case learns to carry one now, at the window's lowest price. On a clone: 23 of 23 captured in 42 s, and all 171 files compared with the 19 predecessors byte-identical.

## SEMULITH-P4-0366 (leaf P4-SYSTEM.14 a48-1) — Batch II-b's four programs and cases, declared before their captures, and what writing them found

The A, C, F and D extensions: 239 witnesses, all three producers agreeing, rehearsed first. A case cannot carry a fetch fault, so REQ-GC-C's second-parcel fault stays the corpus guest's until the next window, raised to the director. Forms are not the requirement: the first drafts agreed with Sail and missed most of what the statements say.

## SEMULITH-XTASK-0082 (leaf XTASK.13 slice e) — PLATFORM-GEN's controls judge a small frozen tree, and two arms stop passing for the wrong reason

A deleted board, dossier or manifest now fails by its own name. Two RED arms were firing on a path in the fingerprint whatever the bytes said; they now judge the generation just found in sync. A manifest with no definition beside it fails by name. 13 arms. `CHANGELOG.md` sharded.

## SEMULITH-P4-0365 (leaf P4-SYSTEM.14 a47-3) — Batch II-a credited: five more requirements implemented, and a configuration requirement that names no form

ECALL and EBREAK, Zicsr, the counters, FENCE.I and IALIGN: 19 `implemented`, 28 `planned`, 10 of 10 legs each. A stale claim about `REQ-D-ECALL-EBREAK` left the gate's statement.

## SEMULITH-P4-0364 (leaf P4-SYSTEM.14 a47-2) — Batch II-a captured exactly once each, byte-identical to its rehearsal, after the guard refused once

AGREE, AGREE, each control DIVERGE where declared. The load guard's first attempt stopped at its ten-minute limit, capturing nothing and spending no case id. Nothing credited.

## SEMULITH-P4-0363 (leaf P4-SYSTEM.14 a47-1) — Batch II-a's five programs and cases, declared before their captures, and what reading them found

ECALL and EBREAK, Zicsr, the counters, FENCE.I and IALIGN: 62 witnesses, all three producers agreeing, rehearsed first. Reading them found that ten of the remaining 28 need a tool that reads a declared alternative, and that three of those have no switch, so 17 end at a ruling. A declared case now belongs to the profile it names.

## SEMULITH-P4-0362 (leaf P4-SYSTEM.14 a46-4) — Batch I credited: nine more requirements implemented, and a form that writes no GPR read after its step

The RV64I base: 14 `implemented`, 33 `planned`, 10 of 10 legs each. The coverage leg now predeclares a branch, a store or a load to `x0` by the read that observes it, named in advance. The gate added about 20 seconds per captured case, against a limit of a minute.

## SEMULITH-P4-0361 (leaf P4-SYSTEM.14 a46-3) — Batch I captured exactly once each, byte-identical to its rehearsal

The nine cases of the RV64I base: AGREE, AGREE, each control DIVERGE where declared. Every compared file matches the rehearsal on the clone. Nothing credited.

## SEMULITH-XTASK-0081 (leaf XTASK.13 slice d) — BOARD-GEN's controls judge a small frozen tree

A deleted `board.sexp` or part catalogue now fails by its own name rather than reading as a check that stopped discriminating. Reading before freezing found the real run would then have read a deleted definition as `no board declares itself yet`; a manifest with no definition beside it now fails by name. 11 arms.

## SEMULITH-P4-0360 (leaf P4-SYSTEM.14 a46-2) — Batch I's nine programs and cases, declared before their captures, and rehearsed first

The RV64I base: nine requirements, one case each, 108 witnesses. All three producers agree on every program. A full rehearsal on a throwaway clone found two faults before they could spend a case id. The family's bound is re-derived once, for all five batches. Nothing captured or credited.

## SEMULITH-P4-0359 (leaf P4-SYSTEM.14 a46-1) — Batch I's walls cleared: the case index generated, its statements retained

`evidence/README.md` could not take another row, so the membership now comes from each `case.sexp` and the credit catalogue, into [the retained cases](docs/models/rv64gc-lab-v0/src/retained-cases.md). Two excerpts retained for Batch I. Nothing credited or captured.

## SEMULITH-P4-0358 (leaf P4-SYSTEM.14 a46-0) — G-OBLIGATIONS' other 42 routed: 28 in batches on the tools as they are, 14 raised for a ruling

All 42 have their contract checks realized, and 158 of 173 guests agree with Sail. One case at a time would be 140 units and 56 hours of gate; five batches are 20 units and 8. Nothing moves here.

## SEMULITH-P4-0357 (leaf P4-SYSTEM.14 a43e-5) — five credits, REQ-D-SSTC implemented, G-STATE 4 of 4, and G-TRACE read from evidence/: the window closed

`CR-GC-M-4`, `CR-D-XLEN-3`, `CR-D-CSR-SET-2`, `CR-D-ZICNTR-2` and `CR-D-SSTC-1`, 10 of 10 legs each. SSTC is the first case to witness delivered interrupts, from S, from U and to M. `gate_report.py` reads each credited record from `evidence/`, and a credited case with no `G-TRACE` row keeps the axis open. `CPU-SYSTEM` reads 2 of 10 axes open.

## SEMULITH-P4-0356 (leaf P4-SYSTEM.14 a43e-4) — the window's five cases captured exactly once each, and three effects retained

`rv64gc-m-forms-v6`, `rv64gc-xlen-forms-v3`, `rv64gc-csr-set-v2`, `rv64gc-zicntr-v2` and `rv64gc-sstc-v1`: AGREE, AGREE, each control DIVERGE where declared. The four's traces are byte-identical to their predecessors'. Run on the director's word with a sibling active, not on a quiet host: a load and spawn check before each case replaces the three-minute wait. Nothing credited.

## SEMULITH-XTASK-0080 (leaf XTASK.13 slice c) — BOOK-INDEX's controls judge a small frozen book

A deleted chapter, `SUMMARY.md` or glossary now fails by its own name rather than reading as a check that stopped discriminating. Reading before freezing found the real run would then have read a deleted `SUMMARY.md` as `no project book yet`; it no longer does. 14 arms.

## SEMULITH-P4-0355 (leaf P4-SYSTEM.14 a43e-3) — the window's five cases declared on contract v3, committed before their captures

`rv64gc-m-forms-v6`, `rv64gc-xlen-forms-v3`, `rv64gc-csr-set-v2`, `rv64gc-zicntr-v2` and `rv64gc-sstc-v1`, 67 manifest children each with no report or book generator; the evidence family re-derived for thirteen cases (287 files, 172 MiB). PNT resumed on the director's word. Nothing captured or credited.

## SEMULITH-P4-0354 (leaf P4-SYSTEM.14) — PNT paused at a handoff-ready checkpoint, on the director's word

`MEMORY.md` records the pause and the next action, a43e-3. The pinned window stays open meanwhile: no credit is current until a43e-5.

## SEMULITH-P4-0353 (leaf P4-SYSTEM.14 a43e-c1) — the prose of the books gets its spaces back, and a doctrine keeps them

534 lost spaces in 37 documents (`All114effective`, `its102/114`), measured on a clean copy with every doctrine green, restored by a rewrite of prose alone. `PROSE-SPACING` names each breach by path, line and token; a real name ending in a number is listed in `doctrine/prose_identifiers.txt`. Evidence: `target/p4-system-14/a43e-c1`.

## SEMULITH-P4-0352 (leaf P4-SYSTEM.14 a43e-2) — the window's last pinned edits: a directive's `{new}` always resolves, and contract v3 lets four requirements say what holds

a43e-2, no credit and no retained case moved. `{new}` is the value a step writes, on both routes; a key with no value is refused by name, and 41 literal placeholders in two records are gone. Contract v3 restates four successors with their requirement's id, so `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP`, `REQ-D-ECALL-EBREAK` and `REQ-GC-PRIV-INSNS` stop stating what a frozen record said; `G-CONTRACT` stays 114 of 114 and `G-OBLIGATIONS` reads 0 not resolved. Rule 7 now skips superseded records. Evidence: `target/p4-system-14/a43e-2`.

## SEMULITH-P4-0351 (leaf P4-SYSTEM.14 a43e-1) — the window that opens SSTC: a delivered interrupt is a boundary a case can say, the report leaves the experiments' inputs, and four credits are retired

a43e-1, on the director's "Pick yourself.": option A of `decision_sstc-delivery-needs-the-pinned-window.md`. `word` and `length` are optional in a `step`; a boundary may fetch nothing exactly when its record declares an interrupt delivered there, and it then writes nothing; a wait, a fetch fault and a half-fetched step stay unsupported. `contract_measure` moves to `scripts/effective_contract.py`, so the next manifests pin no report generator. The predicted cost, exactly: `CR-GC-M-3`, `CR-D-XLEN-2`, `CR-D-CSR-SET-1` and `CR-D-ZICNTR-1` retired by removal, 47 planned, 1 not-applicable, G-TRACE red, G-STATE 0 of 4, GS 4 of 10 open, until each case is re-captured once (a43e-3 … a43e-5). The dossier copies left. Eight probes moved rather than the three predicted, and the real check is stricter than the prototype's. No retained evidence byte moved.

## SEMULITH-AC-0093 (leaf ARTIFACT-CLEANUP.29) — the ruled class C carried out: whole orphan incremental directories go, 1.05 GB, and the strict tools do not move

`scripts/artifact_cleanup_orphans.py`, its own act: a crate-hash directory of cargo's shape in which nothing changed since the last recorded act goes whole. 114 directories, 10,925 files, 1,049,630,763 B, residue 0, none kept; 21 younger ones kept; a build afterwards recompiled nothing. 12 tests, seven guard omissions each RED by one test, in ARTIFACT-COHORT. `.37` runs it before its four.

## SEMULITH-P4-0350 (leaf P4-SYSTEM.14 a45-1) — eight requirements that no credit could ever close, rebound to the effective contract, and a rule so none strands again

a45-1: 8 of 48 rv64gc requirements named only superseded obligations, so `G-OBLIGATIONS` could never have gone green, with every gate passing. Seven rebind to the successor the contract names; `REQ-D-RESOLUTION-ROUTE` is `not-applicable`, a stage that ended: 43 planned, 4 implemented, 1 not-applicable. RECORD-SCHEMA's `SUPERSEDED OBLIGATION` holds it, fired RED on the real tree. Four statements read stale, and their words are owned by the pinned `profile.sexp` and frozen contract versions: a rider on the window.

## SEMULITH-XTASK-0079 (leaf XTASK.13 slice b6) — the rest of GUEST-GEN's self-test judges frozen copies: the doctrine meets ruling 5 whole

Seven probes and the staging tool take DEF-GEN's frozen composition; `frozen_owned.image_root` patches the one `ROOT` name of the pinned image module. Six damaged live states, each restored: a deleted fragment goes from refused, `246 pass / 154 fail`, to `rc=1` naming the file at 400 of 400, and garbled fragment, semantics, encoding, state and profile the same. DEF-GEN's frozen tree gains `profile.sexp`: without it the frozen assembler read IALIGN 32. Taken at 4 of 5 features, recorded why: the rest wait on the director's pick.

## SEMULITH-LC-0055 (leaf LIVE-CONTAINMENT.4) — every book's 404 page finds its own assets

D80: each of the seven books wrote `base href="/"` into its 404 page, so on a static host that falls back to that page, 106 of 106 assets answered 404. One `site-url` line per `book.toml`, mdBook's public setting: 0 broken, and of 359 built files only the seven `404.html` differ. UNIT-BOOKS holds each book to its own path from here; `scripts/serve_book_404.py` is the reproduction.

## SEMULITH-P4-0349 (leaf P4-SYSTEM.14 a43e-0) — the pinned window proved on a throwaway clone: SSTC reaches 10 of 10 legs, and the open decision carries the numbers

a43e-0: 15 changed lines add the typed event binding; `contract_measure` moves out, leaving 67 manifest children and no report or book generator; SSTC then captures and reads `DIV-POLICY: satisfied — 10 of 10 legs satisfied`, while `credit_records` reads all four credits lapsed, as predicted. No real evidence moved. The first run read 9 of 10, and `sstc-timer.s` now cites the requirement's own source at the control's witness. The pick stays the director's.

## SEMULITH-P4-0348 (leaf P4-SYSTEM.14 a43b-c1) — 285 guest citations re-pointed at sections the pinned pages have, and a check so they stay there

a43b-c1: logged as 37; `check_citations.py --corpus`, extended to read both halves of a guest, fired RED on 285 of 9,437 citations in 54 files, an older manual's numbering. A reviewed mapping, one rule per stale pair, re-points them: 0 findings. SEMANTICS runs it on every commit from here, with five new self-test arms. It proves a section exists, not what it says. The 42 owned records re-derive byte-identically; nothing a case pins moved.

## SEMULITH-P4-0347 (leaf P4-SYSTEM.14 a43d-3) — the SSTC program in the corpus, all three producers agreeing, and its case raised to the director

a43d-3: `sstc-timer.s` enters the corpus, 192 instructions, 315 steps: the author, the lab engine and the reference on the case's configuration all agree. Its case cannot be written: a delivered interrupt is a boundary with no instruction word, and the pinned case tools refuse it by design ("unfetched boundaries need typed event binding"). Adding the binding lapses all four credits, so `decision_sstc-delivery-needs-the-pinned-window.md` raises it with options and a recommendation. No pinned path moved; the four credits stay current.

## SEMULITH-P4-0346 (leaf P4-SYSTEM.14 a43d-2) — the SSTC case designed, delivery no longer named out, and its normative statements retained

a43d-2: on the case's own configuration the reference has a timer source, so delivery, a scheduled delivery and five suppressions are in. A draft of 192 instructions and 315 steps reads `AGREE 315 declared steps`, and `DIVERGE step 8 (rdtime x5)` under the profile override. An exact delivery boundary is what both producers do here, not a latency claim. `RVP-SSTC-STATEMENTS`, `RVP-STIMECMP-STATEMENTS` and `RVP-STCE-STATEMENTS` retained; the tool selects a whole paragraph by its anchor or its opening words, its older excerpts byte-identical. A control caught a lost guard omission in the first draft.

## SEMULITH-XTASK-0078 (leaf XTASK.13 slice b5) — GUEST-GEN's author probes judge frozen copies of their other corpus reads; a drafted step dropped on a measurement

`scripts/fixtures/guest-gen/corpus/` holds the 26 records the author does not own and must reproduce; `frozen_owned.py` gains `judge_corpus`; the five probes' live reads go from 33, 57, 29, 25 and 23 files to 0 (`scripts/live_reads.py`, new, an audit-hook census). `mm-sret` edited with its fixture regenerated: refused, `399 pass / 1 fail`, becomes `MIRROR DRIFT — mm-sret.s` with the self-test at 400 of 400. A real-run step drafted for these records was dropped: the mirror governor names each of the 26, measured one edit at a time, so the step could never fire alone. Seven other probes' composition reads are b6.

## SEMULITH-P4-0345 (leaf P4-SYSTEM.14 a43c-5) — the reviews read the ZICNTR case and `REQ-D-ZICNTR` is credited `implemented`: G-STATE 3 of 4

a43c-5: `rv64gc-zicntr-v1` reads `satisfied`, 10 of 10 legs, and the review needed no change. `FEATURE_DISPOSITIONS["OB-ZICNTR"]` is the first to name the counter rule. `CR-D-ZICNTR-1`, `authority review`, on one finite case of 44 witnesses: 44 planned, 4 implemented, 4 of 4 records current, 0 drift. Its limitations name what it does not claim: a write through `mcycle` or `minstret`, Zihpm's absence, rates, a CLINT, timer delivery. No dossier copy, by the director's ruling. The five closed CSR-SET records moved to archive part 27.

## SEMULITH-P4-0344 (leaf P4-SYSTEM.14 a43c-4) — the ZICNTR case captured exactly once, and its configuration's effect retained

a43c-4: `rv64gc-zicntr-v1` ran once on a quiet host behind its guards: 292 steps, baseline and repeat AGREE, the control DIVERGE at its declared step 109 (x21 21 against the wrong 102), complete, qualification false, three traces byte-identical, 14 files retained; the family holds all 177; the case `pending`, the three credits current. `scripts/measure_config_effect.py` ran once under the profile override and retained the raw trace and the record: step 6, `rdcycle x5` traps there. The probe's retained-record test now judges every retained effect.

## SEMULITH-AC-0092 (leaf ARTIFACT-CLEANUP.36) — the tenth recurring cleanup through the supported act

.36: at 26 h, on a clean tree, the four acts ran in target/artifact-cleanup/AC0092 (log inside) at `handoff: OK`: 334 candidates planned, 6 captured Cargo incremental outputs (15,766,335 B) strictly selected and removed by the guarded core under a fresh census, residue 0, journal `complete`/`verified`, `--inspect` confirming; 26,002 retained files kept. Re-census against AC0091: 328 unrecorded (1,371,671,258 B), 120 new and 120 gone; they stay for `.29`'s ruled class C. The record is overwritten; `.37` is due after 2026-11-06T00:16Z.

## SEMULITH-P4-0343 (leaf P4-SYSTEM.14 a43c-3) — the ZICNTR case's three declarations, and the director's ruling on the dossier copies

a43c-3: planned experiment, dependency manifest (67 children, two of them the case's own) and authority record, from `capture_div.py --declare`; this commit is the declaration commit. **The director ruled (a43b-c3):** no dossier copy for a new case until the next pinned window, which retires them all (`decision_dossier-copies-retire-at-the-next-window.md`). Measured while recording it: `experiment_verification.py:39` is the one import that makes `gate_report.py` a pinned input of every experiment, so the window moves that function out too, and editing a report never lapses evidence again. Next: a43c-4, the capture.

## SEMULITH-P4-0342 (leaf P4-SYSTEM.14 a43c-2) — the ZICNTR program and its case: 292 steps, 44 predeclared witnesses, in M, S and U

a43c-2: `zicntr.s` enters the corpus, all three producers agreeing (the author, the lab engine, the reference under the case's overlay, whose configuration is byte-identical to CSR-SET's). `rv64gc-zicntr-v1`: 44 witnesses, 26 boundary rows, control `refused-read-committed` (x21 at boundary 109, 21 against the wrong 102). The family's seventh re-derivation: 177 files, 112 MiB, 160 present. No retained case moved. Next: a43c-3, the declarations.

## SEMULITH-P4-0341 (leaf P4-SYSTEM.14 a43c-1) — the ZICNTR case designed, and its normative statements retained

a43c-1: CSR-SET's route for `REQ-D-ZICNTR`, in five units. A draft program, 163 instructions and 292 steps, agrees with the reference under the overlay and first differs at `rdcycle x5` under the profile override. Retained: `RVI-ZICNTR-STATEMENTS` (§6.1, §6.1.1), the normative input, and `RVP-COUNTEREN-STATEMENTS` (§2.1.1.11), what the refused reads rest on; `scounteren`'s statement has no anchor to select, so it is cited. Out of scope, named for the limitations: a write through `mcycle` or `minstret` (the pinned deriver refuses it) and Zihpm's absence. Next: a43c-2.

## SEMULITH-XTASK-0077 (leaf XTASK.13 slice b4) — GUEST-GEN's author probes judge a frozen owned corpus, and its real check re-derives the live one

`scripts/fixtures/guest-gen/owned/` holds the 42 owned guests, laid out as the repository is; `scripts/frozen_owned.py` points the pinned deriver's `REPO` and `ENCODING` at them for the one call, so the deriver does not move. Eight author probes and `probe_gc_owned_extent` take them. `--check-owned` is now a real-run step, measured RED: a mirrored record's value edit goes from a refusal (`391 pass / 9 fail`) to `MIRROR DRIFT — inj-walk-l0.s` at 400 of 400, and one line of silent prose, which only this step can read, goes from a silent `rc=0` to `DRIFT — inj-walk-l0`. The probes' other corpus reads are still live: slice b5. Next: features, ZICNTR (a43c).

## SEMULITH-P4-0340 (leaf P4-SYSTEM.14 a43b-3h) — `REQ-D-CSR-SET` credited `implemented`: the first `implementation-defined` requirement, G-STATE 2 of 4

a43b-3h: `CR-D-CSR-SET-1`, `authority review`, on one finite case of 53 witnesses: 45 planned, 3 implemented, 3 of 3 records current, 0 drift. Its limitations name what it does not claim: `mip`'s value directly, a CLINT or any device, a non-member address trapping, field semantics, counter rates, timer delivery, numerics. **Raised to the director (a43b-c3):** the dossier copy and its `G-TRACE` row are left out, a departure from the capture plan's step (iii): `references.sexp` would reach 77,669 B against the per-part 65,536 B, and moving the copies edits a tool all three manifests pin. Next: XTASK.13 b4, then ZICNTR.

## SEMULITH-P4-0339 (leaf P4-SYSTEM.14 a43b-3g) — the reviews read the CSR-SET case, and the comparison leg reads the requirement's category: 10 of 10

a43b-3g: `review_div_policy.py`'s comparison leg measured `defined`'s row for every category, so a configuration alone would have satisfied it, against the policy's words. It now reads the category: `defined` is unchanged to the byte; `implementation-defined` needs the recorded selection and a retained effect, seven pins read against the case's own bytes and the first difference re-derived offline at a declared property's step; any other category stays pending and is named. `RETAINED_CAPTURES` names the case: method `satisfied` over 88 files; policy `satisfied`, 10 of 10 legs, no credit yet. `FEATURE_DISPOSITIONS["OB-CSR-SET"]` is the first that says a rule applies. `DIV-POLICY-PROBE`: 48 tests, 27 seams. Next: a43b-3h, the credit.

## SEMULITH-P4-0338 (leaf P4-SYSTEM.14 a43b-3f) — the CSR-SET case captured exactly once, and its configuration's effect retained

a43b-3f: `rv64gc-csr-set-v1` ran once on a quiet host behind its guards: 157 steps, baseline and repeat AGREE, the control DIVERGE at its declared step 130 (x28 5 against the wrong 9), complete, qualification false, three traces byte-identical, 14 files retained; the family holds all 155; the case `pending`, both credits current. `scripts/measure_config_effect.py` (new; `schema/config-effect.sexp`; `scripts/probe_config_effect.py`, 10 tests and nine omissions) ran the same guest under the profile override, once, and retained the raw trace and what ran by digest, no verdict: `step 34 (csrrs x20, mcycle, x0): Sail {}, expectations {'x20': 34}`, the observed effect the policy's `implementation-defined` row asks for. Next: a43b-3g, the reviews.

## SEMULITH-P4-0337 (leaf P4-SYSTEM.14 a43b-3e) — the CSR-SET case's three declarations, committed before its capture

a43b-3e: planned experiment, dependency manifest (67 children, two of them the case's own) and authority record, from `capture_div.py --declare`; preflight `ready`; 7 cases, 1 declared, crediting nothing. The 67 children and 13 authority views are frozen until the capture.

## SEMULITH-P4-0336 (leaf P4-SYSTEM.14 a43b-3d) — the CSR-SET program and its case: all 33 CSRs, 53 predeclared witnesses, in M, S and U

a43b-3d: `csr-set.s` rewritten before any capture (136 instructions, 157 steps), judged three ways: the spec-side author, the lab fixture, the pinned Sail under the overlay. `evidence/rv64gc-csr-set-v1/`: the case (second method and adversarial case declared, the first to do so), its prepared inputs. The evidence family re-derived for seven cases (155 files, 96 MiB). Uncaptured; status unchanged.

## SEMULITH-XTASK-0076 (leaf XTASK.13 slice b3) — GUEST-GEN's parcel author probe judges frozen copies

`scripts/fixtures/guest-gen/parcel-legacy/` holds the five legacy guests and the probe composes over DEF-GEN's frozen encoding, state and definitions; `--cold` copies what it reads. A deleted live guest now reaches the generator's refusal naming the file, the self-test at 400 of 400. A real-run `--check-owned` step was drafted and taken back: six author probes still read the live owned corpus, so it could not fire. That is slice b4.

## SEMULITH-P4-0335 (leaf P4-SYSTEM.14 a43b-3c) — a case's reference configuration, as data: the overlay, its controls and the census tool

a43b-3c: `schema/overlay.sexp` and the first overlay; `prepare_div_inputs.reference_config` applies it over the mapped profile override and refuses any overlay that changes nothing, overlaps or names another case (14 tests, nine omissions in PROFILE-CONSISTENCY). `scripts/census_reference_config.py` re-derives a43b-3a's table from the tracked route, identically. No lapse: v5 and xlen-v2 still `--verify` equal. Two defects logged and scheduled: 37 stale guest citations (a43b-c1) and the deriver's literal `{new}` (a43b-c2).

## SEMULITH-P4-0334 (leaf P4-SYSTEM.14 a43b-3b) — CSR-SET's normative statements retained: RVP-CSR §1.1.1, the first from the privileged volume

a43b-3b: five exact statements of §1.1.1 in `profiles/rv64gc-lab-v0/retained/rvp-csr-statements.html` (2,750 B, `RVP-CSR-STATEMENTS`) under the privileged preface's licence statement (`materials/RVP_CSR_RETENTION.md`), through `scripts/retain_statements.py`, one table for the excerpts to come; 19 cache-free tests and nine omissions in PROFILE-CONSISTENCY. No case, capture or credit yet.

## SEMULITH-P4-0333 (leaf P4-SYSTEM.14 a43b-3a) — the CSR-SET case designed: the reference configuration the case's own, all 33 CSRs witnessed

a43b-3a: measured before declaring on 28 of 33: the pinned Sail implements Zicntr under its public configuration (a CLINT device region, one tick per instruction), all five counter values agree, and over 171 guests the variant gains `mm-counters`, `mm-csr-ro-counters` and `c-irq` and loses `mip` readers, so it is per-case data, costing no lapse (`decision_reference-config-per-case.md`). The program is redesigned (136 instructions, 157 steps, M/S/U, all 33 CSRs, `AGREE` as a draft) and the policy review's category row is to be judged. This removes what ZICNTR waited for; raised to the director.

## SEMULITH-AC-0091 (leaf ARTIFACT-CLEANUP.35) — the ninth recurring cleanup through the supported act

.35: at 39 h, on a clean tree, the four acts ran in target/artifact-cleanup/AC0091 (log inside) at `handoff: OK`: 334 candidates planned, 6 captured Cargo incremental outputs (15,766,335 B) strictly selected and removed by the guarded core under a fresh census, residue 0, journal `complete`/`verified`, `--inspect` confirming; 25,436 retained files kept. Re-census against AC0090: 328 unrecorded (1,368,785,623 B), 39 new and 39 gone; they stay for `.29`'s ruled class C. The record is overwritten; `.36` is due after 2026-11-04T21:49Z.

## SEMULITH-P4-0332 (leaf P4-SYSTEM.14 a43b-2e) — the reviews read v5 and xlen-v2 and both are re-credited: the window closed

a43b-2e: the method review's rows name v5 and xlen-v2 (both `satisfied`, 88 authenticated files) and both measure 10 of 10 legs; `CR-GC-M-3` and `CR-D-XLEN-2` re-issue the credits by the same act, `CR-D-XLEN-2` with two limitations fewer than `CR-D-XLEN-1` — the producer's M words no longer describe its evidence; `REQ-GC-M` and `REQ-D-XLEN` `implemented` (46 planned / 2 implemented, 0 drift); both measured records in the dossier, their G-TRACE rows back, G-TRACE green (GS 3 of 10 axes open). The probes re-stated; `derived-status` 37 again. The planned lapse that opens CSR-SET ran a43b-2a … a43b-2e in one day. Containment: four closed records and 12 rows into `archive/P4-SYSTEM-25.md`. Next: a43b-3, CSR-SET.

## SEMULITH-P4-0331 (leaf P4-SYSTEM.14 a43b-2d) — v5 and xlen-v2 captured, exactly once each: traces byte-identical to their predecessors'

a43b-2d: each re-capture ran once on a quiet host behind three guards (a clean tree, no frozen path moved since the declaration commit, the declarations equal to their regeneration) and the retention preflight: baseline and repeat AGREE, the control DIVERGE at its declared step, complete, qualification false. All six traces and six stdout streams are byte-identical to v4's and xlen-v1's; each stderr differs only by the case directory it prints; each measured record differs from its predecessor's only in the manifest, stderr and receipt digests and, for XLEN, the control's declared id and prose. The family holds all 133 files; v5 and xlen-v2 `pending`. The retained-capture rows move with the re-credits (a43b-2e): a row names its capture commit. Next: a43b-2e.

## SEMULITH-XTASK-0075 (leaf XTASK.13 slice b2) — GUEST-GEN's base-mirror and parcel-count arms judge a frozen owner→mirror pair

`scripts/fixtures/guest-gen/base-mirror/` holds the eight guests the mirror governor's predicates need, from both units (7 recorded re-derivations, 3 of them pinned source re-derivations, and a count-only migration); the three base-mirror arms judge it under DEF-GEN's frozen encoding, the governor's seven self-test arms take that encoding (`check_gc_mirror.py --self-test --encoding`, its composition from the encoding's own root), and the five parcel-count arms count the frozen mirror (`derive_gc_parcel_counts.py --encoding --guests`; its self-test's manifest census over its own hand guests). Measured, HEAD's checker over HEAD's tree against the slice's: a damaged live mirror record, an unassemblable rv64i guest and a deleted rv64gc guest no longer refuse through these arms — the first two fail by name (exit 1; the generator's named refusal), the third keeps one miss, the parcel author's cold probe (slice b3). A first before run was invalid: `cargo xtask` fixes its root at build time (knowledge card `an-xtask-binary-judges-the-tree-it-was-built-in.md`). The book's doctrines page explains ruling 5 with the table. None of the paths frozen for a43b-2d moved. `GUEST-GEN --self-test: 400 pass / 0 fail`. Next: a43b-2d.

## SEMULITH-P4-0330 (leaf P4-SYSTEM.14 a43b-2c) — v5 and xlen-v2 declared: the control the case's own, the predeclaration otherwise identical

a43b-2c: `rv64gc-m-forms-v5` and `rv64gc-xlen-forms-v2` declared — each its predecessor's case file with the new id and the control declared (`wrong-quotient`; `truncated-address`), its four prepared inputs re-derived case-independently and byte-identical to v4's / xlen-v1's, its three declarations written from `capture_div.py --declare`; this commit is the declaration commit the captures name. With the id substituted, v5's planned record differs from v4's only in the dependency manifest's digest, xlen-v2's from xlen-v1's only in that digest and the control's id and prose; the literal guard and the case probe's control check (fired RED once) hold on both. The evidence family's fifth re-derivation: 133 files / 80 MiB, 105 present; `evidence/README.md` compressed. `6 case(s), 0 credited, 2 declared`. The manifests' 67 children and the 13 authority views are frozen until the captures. Next: XTASK.13 slice b2, then a43b-2d.

## SEMULITH-P4-0329 (leaf P4-SYSTEM.14 a43b-2b) — the one pinned edit: the control declared per case, CSR-SET's second-method vocabulary, both credits retired

a43b-2b: the case's `control` form gains optional `id` and `statement`, the producer emits them and refuses by name a case declaring neither (no M literal remains in `capture_div.py`; the four retained declarations render to their own bytes); two optional case forms, `second_method` and `adversarial`, judged by the policy review's risk-method leg at any risk by five conditions read from the record (distinct producer versions, recorded pairs whose shared inputs are the declared common inputs, no `shared` pair, adversarial properties of an agreeing capture); the command probe's literal guard (a unique-token control planned verbatim, prose only from the case file or the reviewed neutral set). Found and repaired: probes planning history now plan copies that declare a control, and the method review, which detected `stale` by regenerating, re-checks the declaration route's pins on the capture's own manifest when the producer refuses (v4 and xlen-v1 `stale` at `schema/matched-case.sexp`, not `refused`); knowledge card `a-producer-refusal-hides-staleness-detected-by-regeneration.md`. The lapse: `CR-GC-M-2`, `CR-D-XLEN-1` retired with `credits.sexp`; 48 planned; dossier copies and G-TRACE rows out, G-TRACE open (GS 4 of 10). Probes: DIV-COMMAND 20, DIV-METHOD 22, DIV-POLICY-PROBE 33; eight new seams, each RED; the token-facet inventory 127 with two new token languages. Next: a43b-2c.

## SEMULITH-P4-0328 (leaf P4-SYSTEM.14 a43b-2a) — the lapse window that opens CSR-SET, designed

a43b-2a, documentation only: the control's id and statement become optional fields of the case's `control` form that the producer requires (the four retained declarations cannot gain fields; one schema, not two); CSR-SET's high-risk vocabulary is two optional case forms, `second_method` and `adversarial`, judged for high or critical risk by five conditions read from the measured record (the graph's producers with distinct versions; recorded pairs whose shared inputs are the declared common inputs; no independence credit beyond the pair's assessment; adversarial properties of an agreeing capture); a guard against the literals' return; the order 2b (one pinned edit, both credits retired, 48 / 0) → 2c (v5, xlen-v2 declared, family 89 → 133) → 2d (captured once, traces identical) → 2e (re-credited, 46 / 2) → CSR-SET. The tree record, `decision_producer-debt-paid-before-the-next-case.md` and the unit book's policy page carry it. Containment: eleven closed `.14` records and 33 rows verbatim into `archive/P4-SYSTEM-24.md` (the live tree 129,223 → 93,927 B before the record); this file sharded (`shard-0422.md`, 15 entries; 64,028 → 48,866 B). The main book's task-history list, stuck at part 19, now lists the parts by glob. Next: a43b-2b.


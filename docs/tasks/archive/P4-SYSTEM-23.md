# P4-SYSTEM ordinary history — part 23

Ordinary, directly readable task history: the complete records of the closed `.14` units
a43a-1, a43b-1, a43d-1, a44, a44-1 and a44-2a, and the acceptance rows of the closed units a43b-1–a44-2a,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0321` on top of commit `9d0240d78e7cff138556806a6d26cfbc14b94fce`
(9 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a42ax–a42bc and a43 and the rows through a43a-1 are in part 22,
the earlier ones in parts 13–21. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a43a-2a, SEMULITH-P4-0321.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a44-2a | 1839 | `481e4c399c013b453314fe14be02cf4dcc7ad47c39b3fa3567fee5c10719a824` |
| record a44-1 | 5192 | `ddea34b807767189fdd905a13facc4ad87aa0f1d70850af049ef122c9812b138` |
| record a44 | 1987 | `a414bdc15362b7a3b950572b37ba8948526e73a730e9f075c2c87730bd41a522` |
| record a43d-1 | 2595 | `9e8908b328062d16d32cfedfbe02b9e330ce001f05da98ecdfc9770f03f59b63` |
| record a43b-1 | 4099 | `7c12e71f73057ad392bffe55fb769c7bea604982f83d36058e336902c7c9dbf7` |
| record a43a-1 | 4309 | `637fb906ef8cb507986b378de18d4f32deed60625d4840d626ed9bec03570c40` |
| acceptance rows a43b-1–a43d-1 | 2565 | `2aeb5cdcc8476deae93666f4ff9f680e9fda3965cb4c6859e32ce450d7f6ade9` |
| acceptance rows a44–a44 | 761 | `a95504d1f8ddd183c140479867e29f9d1bae19cc4364ea79b4a0327ecf7e7d47` |
| acceptance rows a44-1–a44-2a | 2060 | `a38f88ac83d48add23410a4860cb0bcde161f55d2170cb3824ad537402db9a9b` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-23.md)   # a span, by its line range
```

<a id="a44-2a"></a>

### .14 a44-2a / SEMULITH-P4-0313: the matched cases' declarations as data — read beside the code, equal to it (completed)

The first half of a44-1's a44-2, split so the lapse window stays one slice: no pinned file is touched, so `CR-GC-M-1` stays
current. `schema/matched-case.sexp` (the 27th schema) declares a case — its program, properties and their RV64 values, control,
reviewed steps, authority, normative inputs and prepared pins; `scripts/matched_gpr_case.py` reads a declaration, validates it,
maps it onto `ReviewedPropertyCase` and renders its canonical text; a case without one, one that does not validate, one whose
id disagrees with its directory and one whose control names no property are refused by name.
`evidence/rv64gc-signed-div-truncation-v2/case.sexp` (2,756 B) and `evidence/rv64gc-m-forms-v3/case.sexp` (12,565 B) were
rendered from the in-code facts. Measured: each declaration loads equal to `reviewed_case(id)` and its prepared rows equal
`CURATED_INPUTS[id]`; each renders back byte for byte; `scripts/probe_matched_gpr_case.py` 7 tests / 0 failures plain and
optimized, five seams (missing-refusal, id-binding, control-binding and schema 1 loss each, value-mapping 2), its 12 arms in
PROFILE-CONSISTENCY. Re-derived: the evidence family (22 slots per case, ceiling 45, health 42 — the addendum to
`decision_evidence-family-two-cases.md`; `evidence/README.md` 4,095 B under its 4,096 B cap); the schema census (27 schemas,
122 facets, five reviewed token examples; RECORD-SCHEMA's token arms 106 → 127 and 612 → 738 failures, measured); the method
probe's runtime population 103 → 104 (the declaration is a file of the retained case); LIVE_STATUS's arm total 1,692 → 1,694. Nothing
reads the declarations yet: a44-2b switches the tools to them and removes the in-code tables — the one lapse.

<a id="a44-1"></a>

### .14 a44-1 / SEMULITH-P4-0312: the case-declaration design — what moves to data, what is re-derived, the one lapse (completed)

Documentation only; the inventory is target/p4-system-14/a44-1/inventory.md (a read-only census of both scripts, every reader
and both manifests; its key lines re-checked by `grep -n`: `capture_div.py:408` `len(children) == 64`,
`matched_gpr_artifacts.py:21` `MANIFEST_INPUTS = 64`, `review_div_capture.py:36,53,295` the closed module and data-path
censuses, `probe_div_capture_inputs.py:37` `FAMILY_FILES = 43`, `review_div_capture.py:345,349` and `capture_div.py:217` the
M-specific checks). **Correction first (§15, own defect):** a44 recorded that ruling B costs two re-captures because both
retained cases pin both declaration scripts. The signed-DIV case's capture has been `invalidated` since 2026-10-22 (five of its
pinned inputs moved; `evidence/README.md`) and credits nothing (`REQUIREMENT-STATUS: … 2 case(s), 1 credited`), so only the M
case must be re-captured — one re-capture, as recommended; the DIV case stays a historical, invalidated capture. The a44 text,
the two decision records and the live rows are corrected; `evidence/README.md`'s "uncredited" (stale since a42az) too.
What a declaration is today: in `matched_gpr_property.py`, per case — the case id, the guest source's name, boundary count,
size and SHA, the properties (id, cell, witness step and register, expected value, statement), the control (property, value,
reason), the limitation, the reviewed steps, the source locator, category, risk and coverage, and the authority (requirement,
obligations, source id, publication SHA, the requirement's and obligation's semantic digests) with its normative-source input
rows; in `capture_div.py` — the four curated inputs (role, id, name, bytes, SHA). Shared, and staying in code: the profile,
the entry point, the property bound, the reference-identity row and the tool paths.
The design: one file per case, `evidence/<case>/case.sexp`, validated by a new `schema/matched-case.sexp`, carrying every
per-case field above (register values as hex strings, as the expectation files write them). `reviewed_case(case_id)` reads it
and refuses a case without one by name; `CURATED_INPUTS` becomes the file's prepared rows; the in-script tables and `_CASES` are
removed (one definition). The M-specific checks in pinned code become checks of the file against the catalogues — the
normative-source rows, the source id and the obligation count come from the case file and are verified against the
requirement, obligation and source catalogues — so a non-M case (XLEN, CSR-SET, SSTC) is accepted on its own authority. The
case file is a pinned input of its own manifest, and the manifest's fixed 64 becomes the reviewed population counted from the
declaration, so a new case's file touches no other case's pins.
Re-derived in the same slice, each measured: the module and data-path censuses of `review_div_capture.py` (the case file a
declared data read); the evidence family (22 slots per case; its members and the 43-file row of `doctrine/readme_routes.tsv`,
by `decision_evidence-family-two-cases.md`'s mechanism); the probes that mutate the two scripts' text
(`probe_matched_gpr_property.py`'s four mutation strings, `probe_div_command.py`'s identity-digest rewrite) re-pointed to the
loader, their loss counts in `check_profile_consistency.rs` re-measured; the consumer pointers of `review_div_method.py` and
`review_div_policy.py` moved to the new case when it exists.
The one lapse: the slice that edits the pinned scripts invalidates the M v3 capture, as any pinned edit does. The credits schema
has no retired state and a lapsed record is a finding, so `CR-GC-M-1` is retired in that slice (removed from `credits.sexp`, the
retirement recorded in `decision_req-gc-m-credited-implemented.md`) and REQ-GC-M honestly reads `planned` until the M case is
re-captured as v4 and re-credited (`CR-GC-M-2`), the dossier copy (`references.sexp`) and `gate.sexp` following.
Slices: a44-2 the schema, the case files of the two existing cases (their facts moved; a test asserts each loaded case equals
the in-code one before the in-code one is removed), the tools reading them, the censuses re-derived, `CR-GC-M-1` retired; a44-3
the M v4 case declared (its case file, prepared inputs and three declarations, committed); a44-4 the capture, exactly once, and
the method and policy reviews (10 of 10 legs); a44-5 the re-credit. Then the XLEN (a43a-2), CSR-SET and SSTC declarations as
data, one per unit. ZICNTR stays open (the reference). The first gate refused once: PROFILE-CONSISTENCY's
`RED omitted capture retention declaration-regeneration` arm saw a second failure, `15 != 21` in the retention probe's rerun
test (target/p4-system-14/a44-1/gate-1-refused-selftest.log), which 15 re-runs never reproduced — direct, plain and
optimized, eight concurrent, four under 24 CPU-bound processes (race/). The probe's rerun mode does not check its first
retain's success, so a failed first retain reads as a file count; the hardening (assert the first retain's code, name its
reason) joins a44-2, which re-points these probes anyway.

<a id="a44"></a>

### .14 a44 / SEMULITH-P4-0310: the director's rulings of 2026-10-28 recorded — case declarations to data, two re-captures (completed)

The director granted the five recommendations of the session's status report ("I grant all your recommendations"; "Your
recommendations better be sota, signoff and production-grade"; "next push granted"), recorded one ruling per file under
`decision_director-rulings-2026-10-28.md`. This tree's is ruling 1, option B of the P4-0306 finding
(`decision_case-declarations-as-data.md`): a matched case's declaration — its properties (the `_CASES` table of
`scripts/matched_gpr_property.py`) and its input pins (`CURATED_INPUTS` of `scripts/capture_div.py`) — moves into one data
file per case under `evidence/<case>/`, read by the tools, which refuse a case without one. Measured while recording it: BOTH
retained cases pin both scripts (`grep -c` of each name in `evidence/rv64gc-m-forms-v3/dependencies.sexp` and
`evidence/rv64gc-signed-div-truncation-v2/dependencies.sexp` = 1 each), so the ruling costs two re-captures — the M case as
v4 and the signed-DIV case as v3 — not the one the recommendation named [corrected in a44-1: the DIV capture is invalidated
since 2026-10-22 and uncredited, so one re-capture, M as v4]; recorded as measured and told to the director. Each
re-capture must reproduce its predecessor's verdicts with the manifest change the only declared difference, and `CR-GC-M-1`
is re-issued against v4 through the crediting act. The route: a44-1 the case file, its schema and the tools reading it (the
in-script tables removed); then the M re-capture (a44-1's slices); then the XLEN (a43a-2), CSR-SET and SSTC declarations as
data. LIVE_STATUS's P4 line also gains `.17` slice b, which P4-0309 left out (an own lockstep miss). Not covered: the ZICNTR program waits for a pinned reference that implements Zicntr (the a43d-1 addendum) — a
reference re-pin no option addressed, raised to the director as an Open Question.

<a id="a43d-1"></a>

### .14 a43d-1 / SEMULITH-P4-0308: the SSTC case's crediting program — access, both gates and the kernel's own timer matched; delivery named out (completed)

Feature 12 (cycle three), on clean 623ee0d7. Two probes first, both in target/p4-system-14/a43d/draft: with STCE set and
`stimecmp` = 0 the laboratory reads `mip.STIP` (0x20) where the pinned Sail reads 0, and the supervisor timer interrupt the
laboratory delivers at the next step head never arrives in Sail (the override declares `platform/clint` unsupported — the
dossier's "unmatched timer source"); `time` traps there too (Zicntr off). So the program witnesses what the reference can
see. `profiles/rv64gc-lab-v0/guests/sstc.s` — 44 instructions, 52 executed steps, M and S: `mtvec` to a two-visit handler;
in M, `stimecmp` readable with STCE and TM both clear (resets to 0), written 2^40 and read back (all 64 bits); `mret` to S;
the first S access refused (`mcounteren.TM` clear — the handler's visit 1 sets TM and returns), the second refused
(`menvcfg.STCE` clear — visit 2 sets STCE, the visit told by an `mscratch` flag), the third succeeds (2^40); then the
S-mode kernel programs its own timer (2^41) and reads it back — the extension's purpose without an M-mode round trip.
Expectations derived on the parcel route (`--parcels --steps 52`: 52 steps, 104 fetches, schema-valid). Judged three ways:
the lab fixture (guests_rv64gc.rs 170 → 171 guests, 5581 expected steps; `every_guest_matches_its_expectations` ok), the
pinned Sail sim live over the canonical ELF (`AGREE on 52 of 52 declared steps`, modes M and S — an experiment, not a
capture; two same-value flag reads needed sentinels first, 48 → 52), and the lab demo's trace (52 steps). Registered in
run-order.txt and the legality × delegation interaction cell; GUEST-GEN (200 s), EXERCISE-COVERAGE 19/19,
INTERACTION-MATRIX, DERIVED-COUNTS, GATE-REPORT and MATERIALS-BILL green; GS-REPORT.md and the internal-contracts fragment
regenerated after `git add`; REQUIREMENT-STATUS unchanged; no touched path is pinned by the M manifest. Delivery, the
scheduled-time boundaries and suppression stay corpus-judged (`mm-stimecmp`, `w-timer`) and are the case's named
limitation. **The plan's record is corrected in the same addendum:** the ZICNTR case cannot be matched against this
reference at all (a succeeding counter read traps in Sail; the gating trap paths would agree for different reasons), so
its program waits for a reference with Zicntr — the pinned-tooling ruling. Evidence target/p4-system-14/a43d (draft/,
guest-test.log, demo-sstc.txt).

<a id="a43b-1"></a>

### .14 a43b-1 / SEMULITH-P4-0307: the CSR-SET case's crediting program — 28 of the 33 matched live, the counters named out (completed)

Feature 11 (cycle three), on clean e7c56f47. `profiles/rv64gc-lab-v0/guests/csr-set.s` — 98 instructions, 103 executed steps
(two trap-handler round trips), the first matched program to run in S mode: `mtvec` to a recording handler, `mstatus.FS`
Initial, then each of 28 CSRs read into a sentinel-loaded register in M (a zero reset is an observed change) — mhartid,
misa 0x800000000014112d, mstatus 0xa00002000, mtvec, medeleg, mideleg, mie, mip, mscratch, mepc, mcause, mtval, menvcfg,
mcounteren, sstatus 0x200002000, stvec, sscratch, sepc, scause, stval, sie, sip, scounteren, satp, stimecmp, fflags, frm,
fcsr; the alias pairs written through one name and read through the other (mideleg.SSI then `sie` → `mie` = 2; `sstatus`.SIE
→ `mstatus`; `fflags` 31 and `frm` 4 → `fcsr` 0x9f, and FS Dirty with SD summarizing it in `mstatus`); the refused write
(`csrrw` to the read-only mhartid: cause 2 recorded, the sentinel kept, mhartid preserved); then `mret` to S, `sstatus`
readable, an M-level CSR (`mscratch`) refused from S (cause 2, the handler returns to S), `sscratch` readable. Expectations
derived on the parcel route (`--parcels --steps 103`: 103 steps, 206 fetches, schema-valid). Judged three ways: the lab
fixture (guests_rv64gc.rs 169 → 170 guests; `every_guest_matches_its_expectations` ok), the pinned Sail sim live over the
canonical ELF with the retained override (`AGREE on 103 of 103 declared steps`, modes M and S — an experiment, not a
capture: target/p4-system-14/a43b/draft/), and the lab demo's trace (103 steps). Registered in run-order.txt and the
alias × legality interaction cell; GUEST-GEN (198 s), EXERCISE-COVERAGE 19/19, INTERACTION-MATRIX, DERIVED-COUNTS,
GATE-REPORT and MATERIALS-BILL green; GS-REPORT.md and the internal-contracts fragment regenerated after `git add`.
REQUIREMENT-STATUS unchanged; no touched path is pinned by the M manifest.

**Two limits measured before the program was written, both named in the plan's record (addendum):** (1) under the
pinned override the reference has no Zicntr — `csrrs` of mcycle, minstret, cycle, time and instret each trap
illegal-instruction in Sail (33-CSR probe: 27 of 33 reset values agree, the five counters trap, one parser artefact) — a
REFERENCE limitation the dossier already records (`references.md`: "disabled reference Zicntr … leave those observations
unmatched"), so the five counter CSRs are out of the matched program and stay corpus-judged (`mm-counters`,
`mm-csr-ro-counters`): the case can witness 28 of the 33 against the reference, the policy's "genuine reference limitation
leaves the affected comparison uncredited"; (2) the spec-side deriver refuses any CSR outside its 33-name vocabulary
(`csr 0x… outside the corpus's vocabulary`) and is a pinned input of the retained DIV case, so the "non-member address
traps" witness cannot be derived today — the negative side is the refused write and the privilege-refused access; a
same-value write is not a change (the second handler read needed a sentinel: 101 → 103 of 103). The first probe also
showed a trap with `mtvec` = 0 cascading into a fetch fault at address 0 — the handler is set first. With this record
the leaf stood at 132,282 B of the task family's 131,072-byte per-part ceiling (README-ROUTING-CLOSURE refused), so the
standing mechanism ran (a42ba's mover, adapted: target/p4-system-14/a43b/move_closed_records.py, move.log): the closed
records a42ax–a42bc and a43 (seven, 29,853 B) and the closed acceptance rows a42ay–a43a-1 (two spans, 23 rows, 20,279 B)
moved verbatim into docs/tasks/archive/P4-SYSTEM-22.md, each span's SHA256 in the part's table and found once, one pointer
each in the live tree; the live file 132,282 → 83,313 B (0.64× of the ceiling), part 22 52,383 B; TASK-HISTORY-LINKS,
TASK-ACCEPTANCE and SEAM-INTEGRITY (1613 → 1590 live boxes) green. Evidence target/p4-system-14/a43b (draft/,
guest-test.log, demo-csr-set.txt, move.log).

<a id="a43a-1"></a>

### .14 a43a-1 / SEMULITH-P4-0306: the XLEN case's crediting program — in the corpus, agreed live by Sail (completed)

Feature 10 of the second cycle, on clean 2429670f: the first of the XLEN case's units (`decision_state-capture-plan.md`
item 1 (i), split: the program and its expectations here; properties, curated inputs and the declaration next).
`profiles/rv64gc-lab-v0/guests/xlen-forms.s` — 25 instructions, every witness a GPR change at a step boundary, each line
citing its chapter: bit 63 exists and shifts by 63 read it back (`slli`/`srli`/`srai`), bits 32..63 are real and the
6-bit shift amount 40 is legal, 2^63 - 1 + 1 wraps to -2^63 and -1 + -1 discards the carry (RVI-RV64I §3.1.1, §3.1.2.1;
RVI-RV32I §1.1.4), `lui` sign-extends its immediate to 64 bits and the `*W` family (`addiw`, `srliw`, `sraiw`, `addw`,
`subw`, `sllw`) ignores the upper input bits and sign-extends its word (§3.1.2, §3.1.2.2); then the address-space witness:
`mtvec` set to a handler six instructions on, a load at 2^40 (outside every declared region) raising a load access fault,
the handler reading `mcause` = 5 and `mtval` = 0x0000010000000000 into x30/x31 — the full 64-bit address, formed and
reported (RVP-MACHINE §2.1.6–7; D-ADDRESS-SPACE). Expectations derived on the parcel route
(`derive_rv64gc_expectations.py --parcels --steps 25`: 25 steps, 50 fetches, schema-valid, byte-identical to the scratch
derivation; the deriver's owned list untouched — it is a pinned input of the retained DIV case). Judged three ways: the
lab fixture (`gen_guests.py` → guests_rv64gc.rs 168 → 169 guests, 5401 → 5426 expected steps;
`every_guest_matches_its_expectations` ok), the pinned Sail sim live over the canonical ELF with the retained override
(`AGREE on 25 of 25 declared steps`, the trap boundary `trapping from M to M to handle load-access-fault` included — an
experiment, not a capture: target/p4-system-14/a43a/draft/sail_experiment.py, sail.trace), and the lab demo's trace. The
CLI's `run` refuses the GC profile by name, so the lab is judged through the corpus. Registered in run-order.txt (after the
M group) and the boundary × boundary interaction cell; GUEST-GEN, EXERCISE-COVERAGE (19/19), INTERACTION-MATRIX,
DERIVED-COUNTS, GATE-REPORT and MATERIALS-BILL green; GS-REPORT.md and the internal-contracts fragment regenerated
(the interactions digest, the corpus count). The portability record of P4-0304 stays a session over 168 guests; the next
recording run re-measures over 169. REQUIREMENT-STATUS unchanged: `47 planned, 1 implemented; 1 of 1 credit record(s)
current` — no file this unit touched is pinned by the M manifest (checked by name).

**Finding, raised to the director (widens the P4-0303 blocker):** the closure review the plan asked for shows the M case's
manifest (64 inputs: 20 definitions, 5 profile files, 4 schemas, 35 scripts) pins `scripts/matched_gpr_property.py` (the
`_CASES` table) and `scripts/capture_div.py` (`CURATED_INPUTS`) — the two files a new case's properties and input pins are
declared in. Declaring the XLEN case (a43a-2) as the M case was declared lapses `CR-GC-M-1` and drops REQ-GC-M to
`planned`, exactly as the six-line gate_report.py fix would. Options: (A) rule that the capture's dependency closure is the
measurement's (semantics, schemas, comparators, collector, the expectation author) and not the case-declaration or report
tooling, with a re-pin procedure for the retained manifest; (B) move case declarations to data (`evidence/<case>/case.sexp`
read by the tools), one re-capture of M as v4 under the new manifest, then every later case adds data only; (C) accept one
lapse-and-re-credit cycle per new case. Until the ruling, the other three programs (a43b-1 CSR-SET, a43c-1 ZICNTR, a43d-1
SSTC) can land the same way as this one, touching no pinned file. The first chain's focused stage refused twice, both
mine: GATE-REPORT (the GS report had been regenerated before the new guest files were tracked — its dossier digest is
over the TRACKED source files; regenerated after `git add`) and SEAM-INTEGRITY (the NO REGRESSION box carried no
declared evidence signature; a `grep -c` token added). Evidence target/p4-system-14/a43a (draft/, guest-test.log,
demo-xlen-forms.txt, m-manifest-census.txt, chain-1-refused.log).

<a id="acceptance-rows-a43b-1-to-a43d-1"></a>

## acceptance-rows-a43b-1-to-a43d-1

- [x] `.14` a43b-1 **ROOT CAUSE** — at e7c56f47: `grep -c csr-set profiles/rv64gc-lab-v0/guests/run-order.txt` = 0; REQ-D-CSR-SET reads `planned` with no program witnessing the 33; the 33-CSR Sail probe: 27 of 33 reset values agree with the deriver, the five counters trap illegal-instruction (Zicntr unsupported in the pinned override), so a program over all 33 cannot match.
- [x] `.14` a43b-1 **ADDRESSED** — `derive_rv64gc_expectations.py --parcels --steps 103 csr-set.s` → `wrote csr-set.expected.sexp (103 steps)`, `check_sexp_schema: ok`; `grep -c '(step' profiles/rv64gc-lab-v0/guests/csr-set.expected.sexp` = 103; `gen_guests.py --check` → `matches the tracked guests` (170); `cargo test -p semulith-verify every_guest_matches_its_expectations` → `test result: ok. 1 passed`; live Sail `AGREE on 103 of 103 declared steps` (modes M and S).
- [x] `.14` a43b-1 **NO REGRESSION** — `grep -c csr-set evidence/rv64gc-m-forms-v3/dependencies.sexp` = 0 (no pinned path touched); `python3 -B scripts/requirement_status.py` → `47 planned, 1 implemented; … 1 of 1 credit record(s) current; 0 drift`; `bash scripts/check_guest_gen.sh` rc=0 (198 s); INTERACTION-MATRIX ok (no orphan guests), EXERCISE-COVERAGE 19/19, DERIVED-COUNTS, GATE-REPORT, MATERIALS-BILL ok; probes 22/0, 25/0, 34 tests / 36 failures as pinned.
- [x] `.14` a43d-1 **ROOT CAUSE** — at 623ee0d7: `grep -c sstc profiles/rv64gc-lab-v0/guests/run-order.txt` = 0; REQ-D-SSTC reads `planned`; the mip probe: lab `mip` 0x20 vs Sail 0x0 with STCE set and stimecmp 0 — the pinned reference has no timer source, so delivery cannot be a matched witness and the program must be shaped to what the reference sees.
- [x] `.14` a43d-1 **ADDRESSED** — `derive_rv64gc_expectations.py --parcels --steps 52 sstc.s` → `wrote sstc.expected.sexp (52 steps)`, `check_sexp_schema: ok`; `grep -c '(step' profiles/rv64gc-lab-v0/guests/sstc.expected.sexp` = 52; `gen_guests.py --check` → `matches the tracked guests` (171); `cargo test -p semulith-verify every_guest_matches_its_expectations` → `test result: ok. 1 passed`; live Sail `AGREE on 52 of 52 declared steps`.
- [x] `.14` a43d-1 **NO REGRESSION** — `grep -c sstc evidence/rv64gc-m-forms-v3/dependencies.sexp` = 0; `python3 -B scripts/requirement_status.py` → `47 planned, 1 implemented; … 1 of 1 credit record(s) current; 0 drift`; `bash scripts/check_guest_gen.sh` rc=0 (200 s); INTERACTION-MATRIX ok, EXERCISE-COVERAGE 19/19, DERIVED-COUNTS, GATE-REPORT, MATERIALS-BILL ok; probes 22/0, 25/0, 34 tests / 36 failures as pinned.

<a id="acceptance-rows-a44-to-a44"></a>

## acceptance-rows-a44-to-a44

- [x] `.14` a44 **ROOT CAUSE** — the declarations waited on a ruling (P4-0306 finding); measured for the ruling's cost: `grep -c matched_gpr_property.py` and `grep -c capture_div.py` = 1 each in both `evidence/*/dependencies.sexp` — two retained cases pin both scripts.
- [x] `.14` a44 **ADDRESSED** — five records (`decision_director-rulings-2026-10-28.md` and the four rulings) with their INDEX rows (`grep -c 2026-10-28 docs/decisions/INDEX.md` ≥ 5); the frontier row, the route and the ZICNTR Open Question in this leaf.
- [x] `.14` a44 **NO REGRESSION** — documentation only (`git diff --cached --name-only | grep -cvE '\.md$'` = 0); the prechecks green on the staged tree (target/p4-system-14/a44/prechecks.txt) and the commit gate (chain log).

<a id="acceptance-rows-a44-1-to-a44-2a"></a>

## acceptance-rows-a44-1-to-a44-2a

- [x] `.14` a44-1 **ROOT CAUSE** — the a44 record's cost claim rested on a pin count alone; the DIV case's standing: `evidence/README.md` "`invalidated` since 2026-10-22", `python3 -B scripts/requirement_status.py` → `2 case(s), 1 credited`; the inventory's line references re-checked (`grep -n`, listed in the a44-1 record).
- [x] `.14` a44-1 **ADDRESSED** — the design recorded (what moves, what is re-derived, the one lapse, five slices); the a44 text, `decision_director-rulings-2026-10-28.md`, `decision_case-declarations-as-data.md`, docs/TASK_TREE.md, LIVE_STATUS.md and evidence/README.md corrected (`grep -c 'two re-captures'` in the live rows = 0).
- [x] `.14` a44-1 **NO REGRESSION** — documentation only (`git diff --cached --name-only | grep -cvE '\.md$'` = 0); the prechecks green on the staged tree (target/p4-system-14/a44-1/prechecks.txt) and the commit gate (chain log).
- [x] `.14` a44-2a **ROOT CAUSE** — a case's declaration lived only in two pinned scripts (`grep -c '_CASES = ' scripts/matched_gpr_property.py` = 1, `grep -c '^CURATED_INPUTS = ' scripts/capture_div.py` = 1); no schema described one (`ls schema | wc -l` = 26).
- [x] `.14` a44-2a **ADDRESSED** — target/p4-system-14/a44-2a/probe.txt: `MATCHED-GPR-CASE: 7 tests / 0 failures / 0 errors` plain and `-O`; the five seams 1, 1, 1, 1 and 2 failures; generation: loaded == in-code, prepared == pinned, render(read) identical for both cases; `probe_div_capture_inputs.py` `34 tests / 0 failures`; `probe_schema_token_facets.py` OK (27 schemas, 122 facets).
- [x] `.14` a44-2a **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1176 pass / 0 fail` (374 s); `RECORD-SCHEMA: ok (23 record file(s) …)`; `DERIVED-COUNTS: ok (5 derived count claim(s) re-derived)`; `cargo test -p xtask` `test result: ok. 17 passed` (the S-expression and schema corpus tests read the new files); no pinned path touched (`git diff --cached --name-only` against both `dependencies.sexp`: `grep -c` 0); `python3 -B scripts/requirement_status.py` → `1 of 1 credit record(s) current`.


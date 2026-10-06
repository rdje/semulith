# P4-SYSTEM — archived completed-leaf evidence (part 4)

Completed acceptance checklists archived verbatim from [`../P4-SYSTEM.md`](../P4-SYSTEM.md)
under its per-part ceiling (part 3 at its own). Opened `2026-10-06` at the `.11` design.

<!-- archived verbatim from docs/tasks/P4-SYSTEM.md at the 2026-10-06 `.11` design crossing: `.8` slices (a)–(e) -->

`P4-SYSTEM.8` slice (a) — the CSR rd-before-trap defect fixed at root; two stale texts and a wrong unreachable cause (`2026-10-06`, `SEMULITH-P4-0058`):

- [x] **REPRODUCE / ISSUE** — the brief's pre-condition 3, as a RED guest before any fix:

  ```
  probe csrrw x5, cycle, x6 (M, x5 = 7) on the HEAD engine → [5] x5 <- 0x5, then cause 2
  $ cargo test -p semulith-verify run_rv64gc (mm-csr-ro-write added, the old engine) →
    FAILED: "mm-csr-ro-write: step 9 writes match the specification-derived expectations"
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the zicsr rules committed rd before judging the write:
  `git show HEAD:definitions/riscv/zicsr.sem.sexp | grep -c "(seq (set (reg rd) (csr-read
  (field csr)))"` → 6 rules of that shape — `Set` writes rd as soon as its value evaluates,
  and `csr-write`'s permission check (`privilege.rs`) ran second. No guest caught it because
  the authoring tool REFUSED read-only writes ("fix the guest") and knew no immediate forms.

- [x] **FIX** — `schema/semantics.sexp`: `(csr-rw a v)` — the atomic read-write (CSRRW
  "atomically swaps"): read and write judged first, v written, the OLD value yielded, a
  refusal delivered before any effect; `gen_definition.py` lowers it (`Sem::CsrRw`, the
  extended surface); `exec_rv64gc.rs`: the `CsrRw` arm; `zicsr.sem.sexp`: every writing form
  with a destination is `(set (reg rd) (csr-rw …))`. Riding along: LR's unreachable
  boundary-Misaligned arm 7 → 5 (an LR is a load); `a-lrsc-fault`'s ".s" and expectation
  prose ("cause 7 every visit" — the LR's is 5) corrected and RE-DERIVED (every value
  identical; the current tool also fixed a text the `.4` tool had keyed by instruction text);
  the authoring tool taught read-only writes, the immediate forms, `mhartid`, and a
  family-aware header (it stamped the FP header on every file). Two guests:
  `mm-csr-ro-write` (mhartid — implemented on both engines) and `mm-csr-ro-counters`
  (cycle/time/instret).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 4 passed (127 guests)
  $ identity_8a.py <fixed CLI> <HEAD CLI> → identity: 125 byte-identical, 0 diverge;
    RED mm-csr-ro-write and mm-csr-ro-counters — both diverge on the parent engine
  $ compare_sail.py (matched config) → AGREE mm-csr-ro-write 51 steps; AGREE a-lrsc-fault
    41 (its re-derived expectations); DIVERGE mm-csr-ro-counters at step 45, the LEGAL read
    of cycle — "verdict: 2 AGREE of 3", rc=1: the matched override runs Zicntr OFF (the
    recorded CLINT wall), so cycle/time/instret do not exist on sail; a Zicntr+CLINT variant
    fails validate-config ("The CLINT … is not in a defined memory region") — the named
    not-matchable cell, as mm-counters before it
  the derivation tool before/after over the corpus: 76 of 76 jointly derivable files
    byte-identical; the newly derivable mm-csr-ro-write/mm-csr-rw match their tracked
    writes; F/D re-derived 22/22 identical with the family-aware header
  ```

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`;
  the brief's pre-condition 3 corrected in place (its sail half was the Zicntr-absent trap).

- [x] **LOCKSTEP** — this tree (the brief's correction note, checklist, logs, changelog,
  frontier), `DEV_NOTES.md` (sharded first; PROMOTED — the oracle card's mirror case),
  `CHANGELOG.md`, `MEMORY.md` (next_action → b), the book (the new P4.8 chapter, SUMMARY,
  the P4 index), `schema/semantics.sexp`.

`P4-SYSTEM.8` slice (b) — the fault-priority table declared; its missing pairs pinned on both engines (`2026-10-06`, `SEMULITH-P4-0059`):

- [x] **REPRODUCE / ISSUE** — the priority TOPIC was handed to `.8` four times (the archived
  `.2`/`.3`/`.4` briefs) and never declared; the census of what was pinned:

  ```
  $ git show HEAD:profiles/rv64gc-lab-v0/profile.sexp | grep -c "D-FAULT-PRIORITY" → 0
  pinned already: fault-fetch (fetch fault over decode), it-prio-load (misaligned over the
    out-of-region access fault, bare), f-fs-off/d-fs-off (illegal over the access fault),
    a-amo-sv39 (an AMO's misaligned over translation)
  unpinned: a plain load/store's misaligned over a PAGE fault; illegal over misaligned and
    over a page fault; translation succeeding then the physical access refused (grep of the
    sv39 expectations for "access fault" → nothing)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the engine already orders every pair as
  the table and `.3` decision 7 require (both engines agree below); what was missing was the
  DECLARATION and the pins. The table, measured where it lives: priv/machine.html §2.1.1.15,
  "Synchronous exception priority in decreasing priority order" — its one
  implementation-defined position is load/store/AMO misaligned (high or low).

- [x] **FIX** — `profile.sexp`: `D-FAULT-PRIORITY` (the table, the laboratory's HIGH choice,
  the unreachable rows named — instruction-misaligned under IALIGN 16, breakpoints without
  Sdtrig — and the guest pinning each adjacent pair) + REQ-D-FAULT-PRIORITY + OB-FAULT-PRIORITY
  (identical statements, the MIRROR rule); `prio-sv39`: sv39-fault-invalid's page-table
  prologue verbatim up to its last table store (its auipc chains are pc-relative), one leaf
  added by absolute address (VA 0x0040_3000 → PA 0x1000_0000, outside the region), eight
  S-mode cells; the matrix's placements; the authoring tool's header learns `prio-`.

- [x] **ADDRESSED (verified)** —

  ```
  prio-sv39 derived spec-side (128 steps) — the cells' causes: misaligned+unmapped ld 4,
    sd 6; aligned+unmapped 13 (the control); misaligned+mapped-outside 4; aligned
    mapped-outside ld 5, sd 7; FS=Off flw on the unmapped VA 2; FS=Off misaligned fld 2
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 4 passed (128 guests)
  $ compare_sail.py (matched config) → AGREE prio-sv39 128 steps; "verdict: 1 AGREE of 1", rc=0
  $ bash scripts/check_requirements.sh → RECORD-SCHEMA: ok (20 record file(s) …)
  $ python3 scripts/check_interaction_matrix.py profiles/rv64gc-lab-v0 → 28 cells, every
    disposition resolves
  ```

- [x] **NO REGRESSION** — no engine change (the guest pins existing behaviour; it passes on
  the parent engine by design — a characterization, not a RED); `make check` rc=0; `make
  gate` → `=== all doctrines green ===`. Observed on the way: `check_sexp_schema` judges each
  top-level form against the declared constructs and so accepted a decision placed AFTER the
  profile's closing form; the dossier loader (RECORD-SCHEMA, PROFILE-CONSISTENCY) refused it
  ("expected exactly one document form … found 2") — the one-root rule is the loader's, by
  design (record files hold many forms), and it held.

- [x] **LOCKSTEP** — this tree, `profile.sexp` + the two record files, `CHANGELOG.md`,
  `MEMORY.md` (next_action → c), the book (P4.8 chapter).
  `promotion: declined (the priority table is the decision record itself; no new lesson).`

`P4-SYSTEM.8` slice (c) — the typed fault-injection carrier (`2026-10-06`, `SEMULITH-P4-0060`):

- [x] **REPRODUCE / ISSUE** — the acceptance needs "a fault injected after the Nth
  suboperation", and no rv64gc mechanism could inject one:

  ```
  $ git show HEAD:schema/expectations.sexp | grep -c refuse → 0
  $ git show HEAD:crates/semulith-verify/src/run_rv64gc.rs | grep -c Refusing → 0
  the corpus environment (FlatMemory) refuses only by region and alignment; an AMO's two
    halves share address and width, so no split was reachable (the brief's pre-condition 4)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the brief's decision 4 builds it. The
  boundary already carries the shape — four request kinds (`git show HEAD:crates/semulith-core/src/env.rs | grep -cE '^    (Fetch|Load|Store|WalkAccess) \{'` → 4; an AMO issues a Load then a Store) and one access-fault answer the
  engine maps to the architectural cause by kind — so injection is a refusal at the boundary,
  never a hook inside an instruction.

- [x] **FIX** — `schema/expectations.sexp`: `(refuse (kind fetch|load|store|walk) (base …)
  (size …))`, the experiment's refusal regions; `dossier_sexp.py`: their round trip;
  `gen_guests.py`: `RefusalKind`/`Refusal` and a per-guest refusal table in both generated
  modules (empty for every guest that injects nothing — `guests.rs` regenerated too);
  `run_rv64gc.rs`: `Refusing`, under the fetch counter (a refused fetch is still counted),
  answering every request whose kind matches and whose bytes intersect a region with an
  access fault; the authoring tool: `#|refuse:` honoured with the engine's own per-half causes
  (a refused LR/plain load 5, store/SC 7, either half of an AMO 7, a walk read the original
  access's access fault) — and its walk now answers an out-of-region PTE read with that access
  fault where it read zeros (a page fault) before; fetch refusals refused by name (it has no
  fetch translation model). `inj-carrier`: the carrier's end-to-end proof.

- [x] **ADDRESSED (verified)** —

  ```
  inj-carrier derived: the refused store 7 (A unchanged, read back 0); the refused load 5
    and the word inside its bytes 5 (sentinels untouched); the unrefused C round-trips 0x55;
    the AMO on A — its load completes, its store is refused — cause 7, x11 untouched, A 0
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 4 passed (129 guests)
    RED — the runner's refusals emptied: FAILED, "inj-carrier: step 12 writes match the
    specification-derived expectations"; restored → ok
  $ cargo test -p semulith-verify the_refusal_predicate → test result: ok. 1 passed (inside,
    straddling both edges, adjacent both sides, another kind, a PTE read)
  $ check_sexp_schema (an unknown kind, a scratch copy) → REFUSED … "poke" is not one of
    ['fetch', 'load', 'store', 'walk'], rc=1
  the tool before/after over the corpus: 80 of 80 jointly derivable files byte-identical
  ```

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`; every
  pre-existing guest's expectations byte-identical; the matrix 28 cells.

- [x] **LOCKSTEP** — this tree, `CHANGELOG.md`, `MEMORY.md` (next_action → d), the book (P4.8
  chapter). `promotion: declined (the carrier's design is the schema comment and the brief's decision 4).`

`P4-SYSTEM.8` slice (d) — the injected-fault corpus; rv64gc's partial-progress obligation; the state candidate re-answered (`2026-10-06`, `SEMULITH-P4-0061`):

- [x] **REPRODUCE / ISSUE** — rv64gc declared no partial-progress obligation and its state
  candidate waited on `.8`:

  ```
  $ git show HEAD:profiles/rv64gc-lab-v0/contract-obligations.sexp | grep -c PARTIAL-PROGRESS → 0
  state.sexp's "pending or partially committed effects": "… P4-SYSTEM.8's, which reopens
    this candidate"; the carrier (c) had one proof guest and no corpus
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the leaf's acceptance ("a fault injected
  after the Nth suboperation leaves the architecturally required state") needs the injected
  cells and the declared discipline; the census of which suboperations exist is the brief's
  pre-condition 2 (`git show HEAD:crates/semulith-core/src/env.rs | grep -cE '^    (Fetch|Load|Store|WalkAccess) \{'` → 4 boundary request kinds).

- [x] **FIX** — five guests over the carrier: `inj-atomics` (an LR whose load is refused —
  cause 5, no reservation, so the next SC fails rd←1; an SC whose store is refused — 7, rd
  and memory untouched; an AMO's store refused after its load, and an AMO's load refused so
  its store never issues — 7 both, rd untouched), `inj-fp` (FLD/FLW refused — 5, the f-register
  unwritten and FS NOT dirtied; FSD/FSW refused — 7, memory unchanged), `inj-walk-l2/l1/l0`
  (a walk read refused at each Sv39 level — the ORIGINAL access's access fault 5/7/7, never a
  page fault); `OB-GC-PARTIAL-PROGRESS` + its mirror `REQ-GC-PARTIAL-PROGRESS` (the unit
  discipline, the standing reads declared, the fixtures named); `state.sexp`'s candidate
  re-answered (`state_rv64gc.rs` regenerated); the matrix's placements. Two authoring defects
  re-derived, never fitted: the walk guests' prologue sliced one line early (its own `csrrw
  mtvec` doubled, every pc-relative table address off by 4 — the derivation showed the table
  stores faulting with 6); read-backs into registers already 0 (no observable change —
  sentinels added). Out of scope, named: a FETCH-refusal guest — the carrier honours fetch
  refusals, but the authoring model has no fetch translation model; fetch faults stay covered
  by fault-fetch (region) and sv39-straddle (translation).

- [x] **ADDRESSED (verified)** —

  ```
  derived: inj-atomics lr.d 5, sc.d (no reservation) x6 <- 1, M still 0, sc.d 7, amoadd.w 7,
    A still 0, amoor.d 7; inj-fp fld 5, mstatus FS Clean (0x4080), fsd 7, A still 0, flw 5,
    fsw 7, FS still Clean; inj-walk-l2/l1/l0 ld 5, sd 7, amoadd.d 7
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 5 passed (134 guests)
    RED — a refused walk read mutated into a page fault (translation.rs): FAILED, "inj-walk-l2:
    step 64 writes match…" — the first failing guest, so the 129 before it were blind to it;
    restored → ok
  $ bash scripts/check_requirements.sh → RECORD-SCHEMA: ok (20 record file(s) …)
  gen_state → state_rv64gc.rs: the candidate's why only (2 lines); definition_rv64gc.rs
    re-fingerprints the state document (DEF-GEN named the drift); the matrix 28 cells
  ```

- [x] **NO REGRESSION** — no engine change; every pre-existing guest unchanged; `make check`
  rc=0; `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — this tree, the two record files and `state.sexp` (+ its module),
  `CHANGELOG.md`, `MEMORY.md` (next_action → e), the book (P4.8 chapter).
  `promotion: declined (per-slice corpus; the discipline is the obligation record itself).`

`P4-SYSTEM.8` slice (e) — the sail attempt, the reports, the book and THE LEAF ACCEPTANCE; the leaf CLOSES (`2026-10-06`, `SEMULITH-P4-0062`):

- [x] **REPRODUCE / ISSUE** — the leaf's acceptance reads "a fault injected after the Nth
  suboperation leaves the architecturally required state"; the second engine's view of the
  `.8` corpus was unmeasured for the injected guests.

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the closing step. What sail can say was
  measured, not assumed: its configuration has no refusal regions
  (`grep -c refuse target/refs/sail-rv64gc-lab-v0.override.json` → 0), so an injected guest's
  refused access PROCEEDS there — those cells are not matchable by construction.

- [x] **FIX** — the experiment over all ten `.8` guests (`target/p4-system-8/sail/`); the
  ledger's seventh experiment (`references.sexp`); the leaf's status **done** and Result;
  the frontier → `.9` (the environment contract v1 — the design brief first);
  `docs/TASK_TREE.md`, MEMORY, LIVE_STATUS; the book's P4.8 chapter closed.

- [x] **ADDRESSED (verified)** —

  ```
  $ compare_sail.py (matched config, ten guests) → AGREE mm-csr-ro-write 51, a-lrsc-fault 41,
    prio-sv39 128; DIVERGE mm-csr-ro-counters at its legal cycle read (Zicntr off — named);
    DIVERGE inj-carrier step 12, inj-atomics 14, inj-fp 21, inj-walk-l2/l1/l0 64 — each at its
    FIRST refused access (sail lets it proceed; the walks reach L0T[3]'s V=0 and page-fault 13)
    — "verdict: 3 AGREE of 10"
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 5 passed (134 guests)
  ```

- [x] **THE LEAF ACCEPTANCE** — "a fault injected after the Nth suboperation leaves the
  architecturally required state": the typed carrier (c) refuses a chosen suboperation's
  access, and on every multi-suboperation instruction the profile has, the state is the
  required one — an AMO's store refused after its completed load (inj-carrier, inj-atomics:
  rd and memory untouched), an LR's load (no reservation registered), an SC's store, the FP
  transfers (no f-register write, FS not dirtied), a translation walk refused at each of its
  three levels (the original access's access fault) — each derived spec-side and satisfied by
  the engine (134/134), with the mutation that maps a refused walk read to a page fault caught.
  The goal's other parts: fault priority declared (D-FAULT-PRIORITY) and pinned on both engines
  (prio-sv39 AGREE); suppressed effects (the CSR rd-before-trap defect fixed at root, sail
  AGREE); restart locations (every cell resumes at xepc + 4 through its handler — the
  continuation proofs); partial commits under the new system features declared impossible and
  checked (OB-GC-PARTIAL-PROGRESS), the standing reads declared (SEM-06).

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`;
  records only.

- [x] **LOCKSTEP** — `references.sexp`, this tree (status, result, frontier, checklist, logs,
  changelog), `docs/TASK_TREE.md`, `MEMORY.md` (P4 8/10; next_action → the `.9` design brief),
  `LIVE_STATUS.md`, `CHANGELOG.md`, the book.
  `promotion: declined (the leaf's lessons were promoted at their slices — the oracle card's mirror case).`

<!-- archived verbatim from docs/tasks/P4-SYSTEM.md at the 2026-10-06 `.11` slice-(d) crossing: `.9` slices (a)–(d), `.10` slices (a)–(c) -->

`P4-SYSTEM.9` slice (a) — the contract becomes a versioned document; v0 recorded and frozen; CONTRACT-FREEZE (`2026-10-06`, `SEMULITH-P4-0064`):

- [x] **REPRODUCE / ISSUE** — the brief's pre-condition 1, measured:

  ```
  $ git ls-tree --name-only HEAD schema/ | grep -c "contract.sexp$" → 0 (no contract construct)
  $ git show HEAD:profiles/rv64gc-lab-v0/contract-obligations.sexp | grep -c '^(obligation' → 46,
    every one contract_version "0"; nothing checks the version or which records make it up
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the version was data on each record and nothing else
  (`git grep -n contract_version HEAD -- 'scripts/*.py' 'scripts/*.sh'` → the record
  reader/writer, the board/platform generators' pins and self-test fixtures — no rule judges
  which records make up a version), so "versioned, not edited in place" could not be checked
  and seven leaves added records under v0.

- [x] **FIX** — `schema/contract.sexp` (one `contract` per version: id, version, extends,
  status open/frozen, statement, `member`s with a sha256 once frozen, `supersede` entries);
  `profiles/rv64gc-lab-v0/contract.sexp` recording v0 as it stands — 46 members, FROZEN, each
  record line pinned; `scripts/check_contract_freeze.sh` — CONTRACT-FREEZE, the 37th project
  doctrine (members real and of their version; every record in exactly one version; frozen
  records unedited; extends and supersede well-formed), registered on its five surfaces.

- [x] **ADDRESSED (verified)** —

  ```
  $ bash scripts/check_contract_freeze.sh --self-test → 7 pass / 0 fail (GREEN the real
    contract; RED an edited frozen record — FROZEN RECORD EDITED; a dropped member —
    UNVERSIONED RECORD; a member naming nothing; a member of another version; an extension of
    no version; a supersession of a record not inherited)
  $ bash scripts/check_contract_freeze.sh → CONTRACT-FREEZE: ok (1 versioned unit(s), 1
    version(s), 0 finding(s))
  $ check_sexp_schema contract.sexp schema/contract.sexp → ok
  ```

- [x] **NO REGRESSION** — no record changed (v0 pins today's bytes); `make check` rc=0; `make
  gate` → `=== all doctrines green ===` (DERIVED-COUNTS re-derived: 37 doctrines, 473 arms).

- [x] **LOCKSTEP** — this tree, the doctrine surfaces (registry, `docs/doctrines/definition.md`,
  `DOCTRINE_ENFORCEMENT.md`, the book's doctrine chapter, `docs/toolbox/definition.md`),
  `LIVE_STATUS.md`, `CHANGELOG.md`, `MEMORY.md` (next_action → b), the book (the new P4.9
  chapter). `promotion: declined (the mechanism is the doctrine row and the schema's own comment).`

`P4-SYSTEM.9` slice (b) — contract v1: the four environment assumptions, each with realized POS/NEG fixtures; the check registry (`2026-10-06`, `SEMULITH-P4-0065`):

- [x] **REPRODUCE / ISSUE** — the brief's pre-conditions 2 and 4, measured:

  ```
  $ git show HEAD:profiles/rv64gc-lab-v0/contract-obligations.sexp | grep -c environment-assumption → 0
  $ git grep -c "CHK-ENV-" HEAD -- crates scripts → nothing (no check names a fixture)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the four topics were routed to `.9` by name
  (`env.rs:96-98`, `reservation.rs:26-28`, `timekeeping.rs:8-9`, `state.sexp:652`) and the
  gate report counts a check implemented only when its id appears in code
  (`gate_report.py:63-77` — `git grep` of the id), so declared-only checks read 0 forever.

- [x] **FIX** — contract v1 (`contract.sexp`: extends v0, open) with four
  `environment-assumption` records under `rv64gc-lab-env-v1`: `OB-GC-ENV-TRANSLATION-INPUTS`
  (walk reads are the WalkAccess kind, from the memory the hart's stores write; the
  environment never writes a PTE; a refused walk read is the original access's access
  fault), `OB-GC-ENV-INTERRUPT-SOURCES` (v1 supplies none: MSIP/MTIP/MEIP 0 and unwritable, STIP
  the hart's own comparison, SSIP/SEIP software's), `OB-GC-ENV-VIRTUAL-TIME` (one tick per step
  boundary, retired or halted or trapping; instret on retirement only; no host time),
  `OB-GC-ENV-RESERVATION-EVENTS` (no external invalidation at one hart; the eventuality holds
  trivially) — each stating what would falsify it, with typed parameters; the missing
  negative fixture written (`env-irq-sources`: ones written to mip leave only SSIP/SEIP —
  0x202 — and STIP appears only from time >= stimecmp); the check registry
  `crates/semulith-verify/src/contract_checks_rv64gc.rs` (10 checks → guests, `.8`'s
  partial-progress pair included) and its tests; the corpus's comparison helper moved up so
  both judge by one rule.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify contract_checks → test result: ok. 2 passed (every
    realized check's guests exist and hold; every v1 and partial-progress check realized —
    10 declared, 10 registered under their own obligations)
    RED — one registry entry dropped: FAILED, "OB-GC-ENV-INTERRUPT-SOURCES declares
    CHK-GC-ENV-INTERRUPT-SOURCES-NEG, which no registry entry realizes"; restored → ok
  $ bash scripts/check_contract_freeze.sh → ok (1 versioned unit(s), 2 version(s), 0 finding(s))
  $ bash scripts/check_requirements.sh → RECORD-SCHEMA: ok
  $ cargo test -p semulith-verify run_rv64gc → test result: ok (135 guests)
  ```

- [x] **NO REGRESSION** — v0 untouched (its pins hold); `make check` rc=0; `make gate` →
  `=== all doctrines green ===`. On the way GATE-REPORT refused: rv64i's G0 report suddenly
  read "2 are implemented" — the v1 records were first named `OB-ENV-VIRTUAL-TIME` etc., and
  rv64i's own `OB-ENV-VIRTUAL-TIME` declares `CHK-ENV-VIRTUAL-TIME-POS/NEG`, so the report's
  measure (`git grep` of a check id under `scripts/`/`crates/`) credited rv64i with rv64gc's
  registry. The ids are now unit-unique (`OB-GC-ENV-…`, `CHK-GC-ENV-…`); the measure itself is
  not unit-scoped — named for `.10`.

- [x] **LOCKSTEP** — this tree, `contract.sexp` + the obligations file, the matrix,
  `CHANGELOG.md`, `MEMORY.md` (next_action → c), the book (P4.9 chapter).
  `promotion: declined (the registry's purpose is its module doc; no new lesson).`

`P4-SYSTEM.9` slice (c) — the stale v0 statements superseded in v1; the forward references in code resolved (`2026-10-06`, `SEMULITH-P4-0066`):

- [x] **REPRODUCE / ISSUE** — two frozen v0 statements are false of this unit, measured:

  ```
  $ grep -o '(obligation (id "OB-GC-PRIV-INSNS").*' contract-obligations.sexp → "wfi executes
    as a no-op when legal … sfence.vma … its invalidation effect is a stated no-op at this stage
    (no translation caches are modelled" — a wait state since .5 (wait.rs), a TLB since .3
  $ sed -n 26p contract-obligations.sexp → OB-ECALL-EBREAK (an rv64i mirror): "With no
    privileged modes in this profile … reported to the harness … execution stops" — this
    composition delivers the trap to a handler
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — v0 was edited by no one after `.2` wrote it
  (`git log -S 'wfi executes as a no-op when legal' --format=%h -- …contract-obligations.sexp`
  → b95af58 only, `.2` slice e; correctly — contract changes were `.9`'s charter), and the
  base mirror must stay byte-identical to its
  rv64i owner (MIRROR-DERIVE, `check_requirements.sh:544-552`); with v0 now frozen
  (CONTRACT-FREEZE), the only legal correction is a later version's record.

- [x] **FIX** — v1 gains `OB-GC-PRIV-INSNS-V1` (wfi ENTERS the wait; sfence.vma invalidates the
  modelled TLB by the four cases) and `OB-GC-ECALL-EBREAK-V1` (the traps are delivered — cause
  by originating mode, delegation, the handler — never a harness report), each with a
  `supersede` entry naming the v0 record and why; their four checks realized in the registry
  (mm-wfi, w-timer, sv39-tlb-fence / mm-csr-legality-u, w-notrap; mm-ecall-modes, mm-ebreak /
  mm-ecall-deleg); the code comments that pointed forward to "`.9`'s charter" (`env.rs` ×2,
  `translation.rs`, `reservation.rs`, `timekeeping.rs`) now name the v1 obligations, and
  `env.rs`'s module doc no longer says the boundary's scope is rv64i's alone.

- [x] **ADDRESSED (verified)** —

  ```
  $ bash scripts/check_contract_freeze.sh → ok (1 versioned unit(s), 2 version(s), 0
    finding(s)) — both supersessions replace an inherited record by a v1 member
  $ cargo test -p semulith-verify contract_checks → test result: ok. 2 passed (14 declared
    checks, 14 realized)
  $ bash scripts/check_requirements.sh → RECORD-SCHEMA: ok
  ```

- [x] **NO REGRESSION** — v0 untouched (its 46 pins hold); `make check` rc=0; `make gate` →
  `=== all doctrines green ===`. Named, not changed: the requirement mirrors of the two
  superseded records (REQ-GC-PRIV-INSNS, REQ-D-ECALL-EBREAK) still state v0's text — they
  mirror the frozen v0 obligations by the MIRROR rule; the contract is where v1 corrects them.

- [x] **LOCKSTEP** — this tree, `contract.sexp` + the obligations file, the registry, the five
  code comments, `CHANGELOG.md`, `MEMORY.md` (next_action → d), the book (P4.9 chapter).
  `promotion: declined (supersession is the contract schema's own mechanism).`

`P4-SYSTEM.9` slice (d) — the ENVIRONMENT document, v1 frozen, THE LEAF ACCEPTANCE; the leaf CLOSES (`2026-10-06`, `SEMULITH-P4-0067`):

- [x] **REPRODUCE / ISSUE** — the leaf's acceptance reads "every new assumption has a positive
  and a negative fixture; the contract is versioned, not edited in place"; rv64gc had no
  contract-level prose (`git ls-files profiles/rv64gc-lab-v0/ENVIRONMENT.md` → nothing) and v1
  was still open.

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the closing step. One defect found on the way,
  in this leaf's own gate: CONTRACT-FREEZE ran its controls before judging and its GREEN arm
  copied the live files, so an edited frozen record surfaced as "REFUSED — the check does not
  discriminate" (rc=2) instead of the finding — measured by editing a pinned v1 record.

- [x] **FIX** — `profiles/rv64gc-lab-v0/ENVIRONMENT.md` (the versions, the boundary inventory
  dispositioned, the four assumptions with what would falsify each, the supersessions, the
  realized fixtures, what is deliberately not here — including the named gap: rv64i's eight base
  `OB-ENV-*` assumptions were never restated for rv64gc); v1 FROZEN (its six members pinned);
  CONTRACT-FREEZE judges first and runs its controls only to certify a pass; the leaf's status
  **done** and Result; the frontier → `.10`; `docs/TASK_TREE.md`, MEMORY, LIVE_STATUS; the book.

- [x] **ADDRESSED (verified)** —

  ```
  a frozen v1 record edited (a scratch edit, restored after) → bash scripts/check_contract_freeze.sh
    → "FROZEN RECORD EDITED rv64gc-lab-v0 [rv64gc-lab-env-v1]: OB-GC-ENV-VIRTUAL-TIME no longer
    matches its pin", rc=1; restored → ok (1 versioned unit(s), 2 version(s), 0 finding(s)), rc=0
  $ bash scripts/check_contract_freeze.sh --self-test → 7 pass / 0 fail
  $ cargo test -p semulith-verify → test result: ok (the registry: 14 checks realized)
  ```

- [x] **THE LEAF ACCEPTANCE** — "every new assumption has a positive and a negative fixture": the
  four v1 environment assumptions (and v1's two superseding guarantees) each name a POS and a
  NEG check, and every one is realized — bound to tracked guests by the registry, run under the
  corpus's rule, a declared-but-unrealized check refused (RED-proven); "the contract is
  versioned, not edited in place": versions are documents with listed members, v0 and v1 are
  frozen by content pins, CONTRACT-FREEZE refuses an edited frozen record (RED-proven on v0 at
  (a) and on v1 here), and v0's two wrong statements were superseded by v1 records, never
  rewritten. Goal coverage: translation inputs, interrupt sources, counter progress and
  reservation invalidation are each stated (`OB-GC-ENV-*`).

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — `ENVIRONMENT.md`, `contract.sexp`, the gate, this tree, `docs/TASK_TREE.md`,
  `DEV_NOTES.md` (PROMOTED — the self-test card's masking-control case), `CHANGELOG.md`,
  `MEMORY.md` (9/10; next_action → the `.10` design brief), `LIVE_STATUS.md`, the book.

`P4-SYSTEM.10` slice (a) — the contract measure, unit-scoped and supersession-aware (`2026-10-06`, `SEMULITH-P4-0069`):

- [x] **REPRODUCE / ISSUE** — the census at `293fad3`: the G-CONTRACT measure was a tree-wide
  grep (`git show HEAD:scripts/gate_report.py | grep -c '"git", "grep"'` → 2: `build()` and
  `build_cpulab()`), MIRROR-DERIVE shares 26 check ids across the units, and the denominator
  counted v1's two superseded records (rv64gc 14 of 104).

- [x] **ROOT CAUSE (WHY + WHERE)** — `gate_report.py:63-77` and `:546-552` asked "does any tracked
  executable NAME this id", a question about the tree, not about the unit. Measured in a scratch
  worktree (`git worktree add --detach target/p4-system-10/wt HEAD`, removed after) with
  `CHK-ALU-IMM-POS` realized only in rv64gc's registry:

  ```
  $ git show HEAD:scripts/gate_report.py > wt/scripts/gate_report.py (HEAD's generator, rc=0)
    → G0 "which **1 is implemented"; GC "| `G-CONTRACT` | 1 of 72 declared obligation checks implemented"
  ```

- [x] **FIX** — `contract_measure()`: the effective contract (the latest version's chain, minus
  every superseded record; a unit with no contract document is all its records) and the pairs
  THIS unit's registry realizes under the obligation that declares them, read exactly (an entry
  the reader cannot parse is a refusal). The registry is named by a new `(registry (path …))`
  construct (`schema/contract.sexp`; rv64gc's `contract.sexp` names
  `contract_checks_rv64gc.rs`). Both builders use it. The generator gained `--self-test` (7
  arms), run by GATE-REPORT's self-test. The registry gained the pairing test (every entry
  realizes a check its own obligation declares). G0's measure paragraph and the book's quote
  of it re-worded.

- [x] **ADDRESSED (verified)** —

  ```
  the same scratch tree, the new generator → G0 "which **0 are implemented", GC "0 of 72";
    rv64gc 15 of 100 (the shared id credited to the unit that realizes it, only)
  live: rv64gc 14 of 100 (50 effective obligations), rv64i 0 of 72
  $ python3 scripts/gate_report.py --self-test → 7 pass / 0 fail
  $ bash scripts/check_gate_report.sh --self-test → 13 pass / 0 fail
  a registry entry CHK-SVADE-POS under OB-GC-ENV-VIRTUAL-TIME (a backed-up scratch edit, restored
    — git diff clean) → cargo test -p semulith-verify contract_checks → test result: FAILED.
    "no obligation record declares this pair"; restored → test result: ok. 3 passed
  ```

- [x] **NO REGRESSION** — rv64i's GC and G1 reports byte-identical under the new measure
  (`diff` empty); G0's counts and verdict unchanged, its measure paragraph re-worded;
  `make check` rc=0; `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — the generator, the schema, the contract document, the registry test, the
  GATE-REPORT controls, G0-REPORT, the book (`plan/p0.md`'s quote; the new `plan/p4/gate.md`),
  this tree, `CHANGELOG.md`, `MEMORY.md`.
  promotion: declined (the cross-unit credit is recorded where it lives — the `contract_measure` comment's "third wrong cut", beside the two before it; no new general lesson beyond the zero-hits card's scoping row)

`P4-SYSTEM.10` slice (b) — the `GS` builder over all ten axes; the unit's evidence manifest; the first report (`2026-10-06`, `SEMULITH-P4-0070`):

- [x] **REPRODUCE / ISSUE** — no CPU-SYSTEM path: `main()` accepted `G0`/`G1`/`GC`/`BREADTH`;
  the nearest builder run on rv64gc (stdout only, nothing written) read G-REPLAY green from
  rv64i's suites and G-INTERACTIONS incomplete on a hard-coded 21:

  ```
  $ python3 scripts/gate_report.py rv64gc-lab-v0 --gate GC --stdout (rc=0)
    | `G-REPLAY` | replay bundles (P1-LAB.10) + mid-execution snapshots (P2-SCALAR.7): 5 snapshot suites … | **green**
    | `G-INTERACTIONS` | 28 cells declared, every disposition resolving (217 dispositions) … | **incomplete**
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `build_cpulab` (`git show HEAD:scripts/gate_report.py`,
  `:574-578`, `:591`, `:599`, `:604`) holds one unit's facts as constants and its suite
  locations as paths; five of §7's axes are answered by suites and records whose location is the
  unit's business, so a generator that hard-codes them reports one unit's evidence about another.

- [x] **FIX** — `build_cpusystem()` (`--gate GS`): all ten §7 axes; G-SCOPE (the composition's
  status and unfilled slots), G-STATE (the census answered + the `state` requirements
  implemented), G-CONTRACT (`contract_measure` + the latest version frozen), G-OBLIGATIONS
  (every requirement resolved and implemented, under a tracked `EVIDENCE_POLICY.md`),
  G-INTERACTIONS (per cell, never an aggregate) computed from the dossier; G-TRACE,
  G-REGRESSION, G-PORTABILITY, G-REPLAY, G-RELEASE answered by the unit's new evidence manifest
  (`schema/gate.sexp`; `profiles/rv64gc-lab-v0/gate.sexp`), every declaration VERIFIED (a test
  function in a tracked file; a tracked record with a passing recorded verdict; an experiment
  record), the required kinds held by the generator (`GS_KINDS`). Every open item names its
  owning leaf (`.11`–`.18`); an open axis without one prints **unowned**. `passed` needs all ten
  green (`_gs_verdict`). `GS-REPORT.md` generated; GATE-REPORT discovers and syncs it.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/gate_report.py rv64gc-lab-v0 --gate GS (rc=0) → **Verdict: `incomplete`.** Open axes (9 of 10);
    G-REPLAY "1 of 4 required kinds evidenced — open: `snapshot`, `replay-bundle`, `reduction`";
    G-INTERACTIONS "28 cells declared, 28 with a resolving disposition" **green**
  $ python3 scripts/gate_report.py --self-test → 17 pass / 0 fail (the 7 measure arms + 10 GS arms:
    a missing test fn, a foreign kind, two locators, not-applicable, a failing record, an unowned
    axis, the slots filled → G-SCOPE green, an undispositioned cell, the verdict function)
  $ bash scripts/check_gate_report.sh → GATE-REPORT: ok (5 generated report(s) in sync with their inputs)
  $ bash scripts/check_gate_report.sh --self-test → 16 pass / 0 fail
  the literal census (ast over build_cpusystem/_verify_evidence/_gs_verdict/contract_measure): only
    0/1/2 — indices and the rules "exactly one locator", "none open", "at most one registry"; no unit fact
  ```

- [x] **NO REGRESSION** — rv64i's G0/G1/GC reports in sync (GATE-REPORT above); `make check`
  rc=0; `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — the generator, `schema/gate.sexp`, the manifest, `GS-REPORT.md`, this tree,
  the book (`plan/p4/gate.md`), `CHANGELOG.md`, `MEMORY.md`.
  promotion: declined (the hard-coded-unit-facts defect is recorded where it lives — the `build_cpusystem` header beside `build_cpulab`; the manifest-verified-by-generator pattern is this leaf's design, in its brief)

`P4-SYSTEM.10` slice (c) — THE LEAF ACCEPTANCE; the leaf CLOSES (`2026-10-06`, `SEMULITH-P4-0071`):

- [x] **REPRODUCE / ISSUE** — the leaf's acceptance reads "reproducible from pinned inputs;
  fidelity reported per axis; missing checks read `incomplete`"; at `f8567fb` the report
  existed and its reproducibility was not yet measured outside this checkout.

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the closing step. The one input that could
  break reproduction is anything untracked — `target/` holds the reference binaries and every
  scratch tool — so the measurement is a checkout that has none:

  ```
  $ git worktree add -q --detach target/p4-system-10/fresh HEAD (rc=0); in it: ls target → "No such file or directory"
  ```

- [x] **FIX** — the leaf's status **done** and its Result; the frontier → `.11` (bind M, its
  design brief first); `docs/TASK_TREE.md`, MEMORY, LIVE_STATUS; the book chapter closed.

- [x] **ADDRESSED (verified)** —

  ```
  in the fresh worktree (no target/), each report regenerated to stdout and diffed (rc=0 each):
    rv64gc-lab-v0 GS, rv64i-lab-v0 GC, G1, G0: byte-identical in a fresh worktree
    GS sha256 bba3e6f20aa2a040… regenerated = bba3e6f20aa2a040… tracked
  ```

- [x] **THE LEAF ACCEPTANCE** — "reproducible from pinned inputs": the report reads only tracked
  files (the dossier, its manifest, the registry, the test sources) and regenerates byte-identically
  in a checkout with no `target/` (above), and GATE-REPORT refuses a report out of sync with its
  inputs. "Fidelity reported per axis": one row per §7 axis — ten — each with its own measured
  state and verdict, never rolled up; no sentence says the profile is supported. "Missing checks
  read `incomplete`": G-CONTRACT reads 14 of 100 realized → **incomplete**; every required kind
  with no verified evidence reads open; `passed` is reachable only with all ten green (the
  `_gs_verdict` arm, `python3 scripts/gate_report.py --self-test` → 17 pass / 0 fail). The verdict
  today is `incomplete`, 9 of 10 axes open, each open item owned by `.11`–`.18`.

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — this tree (status, Result, frontier), `docs/TASK_TREE.md`, `MEMORY.md`,
  `LIVE_STATUS.md`, `CHANGELOG.md`, the book (`plan/p4/gate.md` closed; the `plan/p4.md` index).
  promotion: declined (a closing slice — the reproduction measurement is the leaf acceptance's own evidence; no new lesson)

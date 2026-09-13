# CHANGELOG.md

## SEMULITH-P0-0029 (leaf P0-PROFILE.9) — gate `G0` is run, and reads `incomplete`

**What changed.** The P0 tree is closed at 9/9 and **gate `G0` has been run**. Its report is
generated, not written: `scripts/gate_report.py` derives it from the profile, the requirements,
the obligations, the reference dossier and the guest expectations — all tracked — so it
regenerates byte-identically in a fresh clone with no reference binaries present.

**Verdict: `incomplete`**, for a measured reason: *66 declared checks, 0 implemented*. All three
criteria are met — semantics resolved (every requirement sourced; 2 honestly `partial` with their
open question in-record), an evidence path that works (2 experiments, 2 models, reproduced), and
differences enumerated (4 differences, 6 independence records across 4 verdict classes).

- `EVIDENCE_POLICY.md` — five obligation classes and what closes each, **declared before any model
  exists** (`crates/` still holds the scaffold's placeholder), which is the whole point of
  `EVD-03`: an implementation that picks its own evidence afterwards picks what it can produce.
- `scripts/gate_report.py` — **no code path reaches `passed`** while declared checks exceed
  implemented ones.
- `GATE-REPORT` doctrine — the tracked report must equal a freshly derived one. Fired RED by
  hand-editing exactly the word that matters: `incomplete` → `passed` fails the commit, quoting
  both lines.

⛔ **The generator was wrong twice, both times in the direction that inflates the verdict.** Asked
how many checks are implemented, it first grepped the whole tree for the id *pattern* and counted
`EVIDENCE_POLICY.md`, a document that merely describes the naming convention. Narrowed to
`scripts/`, it still counted `check_requirements.sh`, which tests for the `-POS`/`-NEG` suffix
while enforcing that the ids exist — *a gate about checks is not a check*. Both said `1` where the
truth is `0`. A gate report that cannot tell a mention from an implementation does not stay wrong
by one; it drifts toward the comfortable answer, and the comfortable answer is the one `EVD-08`
forbids.

⛔ **The evidence policy's own first draft stated class populations and got two wrong** — reading
the profile's *authority* distribution (14/8) instead of the requirements' *category* distribution
(13/10), which is precisely the non-mechanical mapping this profile documents. The counts were
removed from the policy; the generated report derives them.

⚠️ **What `incomplete` means.** Not that the milestone failed — its criteria are met. That the
declared evidence does not yet exist, which is the correct state for a milestone whose job was to
establish what evidence would be required. `P1-LAB` is where the 66 checks acquire fixtures.

**Validation.** `GATE-REPORT --self-test: 3 pass / 0 fail`, fired RED on the real report. Gate
green; `make check` `1 passed`; `run_smoke.py` ok; `fetch_references.sh --verify-only` 11 of 11.


## SEMULITH-P0-0028 (leaf P0-PROFILE.8) — the third guest program, and a bit layout derived rather than typed

**What changed.** `P0-PROFILE.6` left this leaf **blocked on a source, not on effort**: branches
and jumps scatter their immediate across non-adjacent bits, and the pinned specification renders
that layout only as an image. The assembler refused both formats rather than type one from memory.

- The layout is now **derived** from `riscv-opcodes`' machine-readable descriptor table
  (`"jimm20": "imm[20|10:1|11|19:12]"` and kin), pinned with its digest in `references.toml`.
  ⭐ The derivation is **self-validating**: the bits each descriptor accounts for must total the
  width of the field it fills — 7, 5, 20, 20 — or the table is refused.
- `guest-control.s` — the third representative program: a counted loop, a `JAL` that skips two
  instructions, `AUIPC`, and a `JALR` with a deliberately odd offset.
- Expectations for it and for `smoke-trap`: **28 specification-derived values across three
  programs, plus 3 negative observations**, each with its derivation and source locator.
- `fetch_references.sh` gains the strongest cheap control available, now permanent:
  `MATCH encoding tables vs profile scope  52 == 52, symmetric difference NONE`.

⭐ **The negative observations were fired RED behaviourally**, by breaking the program rather than
the expectation: making the `JAL` land on the next instruction so it skips nothing gave
`guest-control: 2 register(s) that must never be written — but ['x6'] were written`. A checker
that only inspects registers it expects to change cannot see a jump that failed to skip.

⛔ **A control that PASSED is reported as a finding.** Replacing the `JALR` offset `+13` with `+12`
changed nothing — both land identically, *because* the low bit is cleared. The landing address
alone therefore does not discriminate `D-JALR-LSB`; what does is that execution continues instead
of attempting a misaligned fetch, and both available references clear the bit, so **the failing
branch has never been observed here**. Tested evidence for the behaviour, not a discrimination
between two behaviours. Recorded in a `limit` field; a real control needs `P1-LAB`'s mutation suite.

⛔ The runner was caught conflating **assembled instructions** with **executed steps** — equal for
straight-line code, wrong the moment a loop exists (12 instructions, 13 steps).

**Validation.** All three programs agree across both models over 28 aligned steps and reproduce
byte-identically. Independent decode confirmed the scrambled immediates before any model ran them.
Two further controls on the acquisition tool fired RED. Gate green; `make check` `1 passed`.

⛔ **A ceiling fired during this leaf and was obeyed, not raised.** `CHANGELOG.md` crossed its
bound (66,708 > 65,536) and the registry's owner column prescribes sharding. Pre-`P0-PROFILE.5`
entries moved **unedited** to `docs/changelog/2026-09-pre-p0.md`; this file is now 32,487 bytes.
The new directory was **registered in the same commit that created it**, with its own per-part,
file-count and aggregate ceilings — sharding a capped file into an ungoverned neighbour is the
exact failure the routing registry exists to prevent, and it would have looked like a fix.


## SEMULITH-P0-0027 (leaf P0-PROFILE.4) — the environment contract, and the two obligations that are "none"

**What changed.** `rv64i-lab-env-v0`: **33 obligations** (25 CPU guarantees, 8 environment
assumptions), the second of `SCP-01`'s four artifacts. `P0-PROFILE.3`'s named gap — 25 obligation
ids checked against nothing — is **closed by a rule**, not by assertion: obligation ids resolving
went from `0 of 25` to `25 of 25`.

- `profiles/rv64i-lab-v0/contract-obligations.jsonl` — generated from the requirements, so the ids
  close by construction rather than by transcription.
- `profiles/rv64i-lab-v0/ENVIRONMENT.md` — the contract, the authority mapping, and all ten
  boundary items from `docs/CPU_ENVIRONMENT.md` §2 dispositioned: **4 in scope, 6 out with reasons**.
- `RECORD-SCHEMA` gains rules 6 and 7, plus a `--audit` mode.

⭐ **Rule 7 is the mechanical form of the contract's first sentence.** *Laboratory policy cannot
override an architectural requirement*: an obligation whose requirement is architecturally
`defined` must carry `authority: architecture`. Fired RED on the real contract —
`AUTHORITY DOWNGRADE … [OB-WSUFFIX]: its requirement 'REQ-D-WSUFFIX' is architecturally 'defined',
but the obligation claims authority 'laboratory'`. Mislabelling an ISA rule as a harness choice is
how a defect becomes an unfalsifiable "profile difference".

⭐ **Two assumptions are "none", and say why.** No virtual time is architecturally readable (no
CSRs, no `Zicntr`/`Zihpm`), and the harness's retired-instruction count is explicitly *not
target-visible*. No asynchronous event is deliverable **by construction** — no controller, mode or
CSR exists to enable, mask or report one, so there is no legal delivery point to specify. A "none"
that is merely absent is indistinguishable from one nobody considered.

⚠️ **The 66 checks are DECLARED, not implemented.** They name fixtures `P1-LAB` will build.
`EVD-03` working as intended — required evidence declared before the implementation that would be
tempted to choose evidence it can easily produce — never 66 passing checks.

🔎 **Routed to `P1-LAB`:** the rules fired first on the *shipped* planning-package examples, not on
this profile. Both example requirements name obligations that do not exist, and the one obligation
defined is named by nobody and declares no negative check. Those files are `frozen-in-place`, so
they are not edited to satisfy a later rule; the finding goes to the milestone that builds the
referential graph checker, and `--audit` keeps it re-derivable.

**Validation.** `RECORD-SCHEMA --self-test: 15 pass / 0 fail`, 15 written and 15 run; both new
rules fired RED on the real contract and restored. Gate green; `make check` `1 passed`; book
renders; smoke test still `ok`.


## SEMULITH-P0-0026 (leaf P0-PROFILE.3) — the requirements catalogue, and a validator that refuses what it cannot check

**What changed.** The profile's 25 decisions were prose in a TOML file. They are now
**25 machine-readable requirement records**, generated from `profile.toml` rather than
transcribed, each carrying its source locator, its semantic category, its risk, its dependencies
and the obligation id the environment contract will define.

- `profiles/rv64i-lab-v0/requirements.jsonl` — 25 records, all valid. Citations: `RVI-RV32I` ×12,
  `RVI-RV64I` ×8, `RVI-INTRO` ×8, no empty locator. 23 `resolved`, **2 honestly `partial`** with
  their open question named inside the record (`REQ-D-SHIFTW-RESERVED` → `OQ-2`,
  `REQ-D-ECALL-EBREAK` → `OQ-5`). All `implementation_status: planned` — no CPU code exists.
- `scripts/validate_records.py` — a JSON Schema validator for exactly the 17 keywords this
  project's three schemas use, **censused rather than guessed**.
- `scripts/check_requirements.sh`, registered as `RECORD-SCHEMA`.

⛔ **Why a tracked validator rather than a dependency.** `jsonschema`, `fastjsonschema` and
`pydantic` are all absent on this host, and installing one would put a dependency store on a
different volume from the repository. A vendored copy under `target/` would leave the gate
depending on an untracked directory. 180 tracked lines work from a fresh clone.

⭐ **Its soundness property is the refusal, not the coverage.** A partial validator that silently
ignores a keyword reports `valid` for a document it never fully checked. This one raises:
`REFUSED: schema uses ['maximum'], which this validator does not implement`. A schema gaining a
keyword breaks the gate loudly instead of quietly widening what passes.

⭐ **`source_semantics` is not a mechanical function of the profile's `authority` field**, and the
judgement table says so. `laboratory` covers both *"the specification says UNSPECIFIED and we
chose"* (`D-RESERVED-DECODE` → `unspecified`) and *"the specification delegates to the EEI and we
chose"* (`D-ENTRY-STATE`, `D-CODE-VISIBILITY` → `implementation-defined`). Collapsing them would
record a laboratory policy as an architectural rule — the exact failure `profile.toml`'s own
header warns about.

**The sharpest new rule:** a record may not be `research_status: resolved` while carrying an
`OPEN:` note. Both halves are individually true, which is what makes the pair the most convenient
lie a requirements catalogue can tell.

**Validation.** Validator fired RED across 12 controls, one per rule class plus the refusal.
`RECORD-SCHEMA --self-test: 11 pass / 0 fail`, 11 written and 11 run. Fired RED on the **real**
catalogue three times: `STATEMENT DRIFT`, `RESOLVED WITH AN OPEN QUESTION`, `UNPINNED SOURCE`.
The three shipped example files now validate for the first time — a claim nothing previously
checked. Gate green; `make check` `1 passed`; book renders; smoke test still `ok`.

⛔ **Two defects in this leaf's own instruments were found by their arms.** The gate excluded
`target/` by absolute path, filtering away its own fixtures (ten arms failed with *"no .jsonl
record file found"*); and the cross-checks re-parsed a file that had already failed to parse, so a
malformed record **crashed** the gate instead of failing it. A traceback is not a verdict.

⚠️ **Named gap:** the 25 `OB-*` obligation ids are checked against nothing, because the
environment contract that defines them is `P0-PROFILE.4` — now the frontier. `evidence_ids` are
deliberately empty: real evidence exists from `.6`, but evidence *records* are `.9`'s deliverable
and a dangling id would be worse than none.

**Housekeeping.** Three stale per-leaf checklists had accumulated in `P0-PROFILE.md` instead of
being archived; they are now in `docs/tasks/archive/`, unedited. Live tree 24,768 bytes, archive
55,397 of a 65,536 per-part ceiling — the archive will need splitting or compaction before long.


## SEMULITH-MIR-0025 (leaf MIRROR-DRIFT.4) — re-derive the counts the live docs carry

**What changed.** `MIRROR-DRIFT.1`–`.3` gated what live documents say about *task-trees*. They
said nothing about any other countable population, and the gap closed itself in the most
convincing way available: **within one working session this repository committed two such numbers
wrong.**

- `LIVE_STATUS.md` claimed `24 destinations governed`; the registry held **25** rows — stale since
  `SEMULITH-P0-0013` added the `profiles/` row.
- It claimed `107 self-test arms`; the real total was **112**.

Neither was a typo. Both were maintained as **running totals** — take the number already written
down, add what you just contributed, write the sum back. ⭐ *A running total is a memory of a
measurement, not a measurement*, and nothing recomputed either one.

- **New doctrine `DERIVED-COUNTS`** (`scripts/check_derived_counts.sh`): routed destinations,
  registered doctrines, book chapters and self-test arms are each re-derived from the population
  they summarise. `--list` prints every covered claim, its enumerator and its current value, so a
  claim and its producer travel together. Scope comes from the routes registry's `hot_live` rows,
  so history is never rewritten.
- **It caught its own registration.** Adding the doctrine made the repository hold nine project
  doctrines where the page said eight, and the gate blocked the commit until the number was
  re-derived rather than incremented.

⛔ **The first cut was wrong in the worst possible direction and a GREEN arm found it.** Extraction
used `sed -nE "s/.*${pat}.*/\1/p"`, whose leading `.*` is greedy: on `12 widgets` it consumed the
`1` and captured `2`. A drifting count could have read as a matching one — a gate reporting
agreement about the wrong number. Extraction is now taken off the front of a `grep -o` match, and
a pattern that does not begin with its `([0-9]+)` group is refused rather than parsed.

**The `TASK-ACCEPTANCE` recipient-tree boundary is documented, not relaxed.** That gate requires
every staged `docs/tasks/*.md` to carry a ticked checklist and cannot distinguish the leaf that
*owns* a change from a tree that merely *receives* a routed finding. The obvious fix — require
only one staged leaf to pass — was rejected: it reopens the measured "co-staged unrelated leaf
supplies the evidence" hole that box-scoping was hardened to close. The workflow instead is that a
routed annotation lands as its own doc-only commit, which is also independently better because the
annotation stays separately revertible.

**Validation.** `--self-test` → `10 pass / 0 fail` (8 RED arms), 10 written and 10 run. Fired RED
on the real corpus before the repair and green after. Gate green; `make check` `1 passed`; book
renders; `scripts/run_smoke.py` still `ok`, so the P0 evidence path is undisturbed.
Tree `MIRROR-DRIFT` complete at 4/4.


## SEMULITH-P0-0023 (leaf P0-PROFILE.7) — the independence inventory, and the 184 files that are the same file

**What changed.** `P0-PROFILE.6` recorded that two models agree over 15 aligned steps. That
sentence is worth exactly as much as their independence, and nothing had examined it. Six pairs
are now inventoried per subsystem, across four verdict classes.

| Subsystem | Pair | Verdict |
| --- | --- | --- |
| instruction encoding | sail ↔ spike | **not shared** |
| floating point | sail ↔ spike | **shared** |
| integer semantics | sail ↔ spike | no evidence of sharing |
| expected-result derivation | act4 ↔ sail | **shared** |
| all | qemu ↔ sail, qemu ↔ spike | **not examined** |

⛔ **The headline: the two models run the same floating-point source.** Both vendor Berkeley
SoftFloat — Sail Release 3e (326 files), Spike Release 3d (263). Of the 199 `.c` files present in
both copies, **184 are byte-identical** once the release-number comment is normalized;
`f64_add.c` differs by exactly one line. A Sail-versus-Spike floating-point comparison executes
one implementation twice. **Nothing currently held is affected** — this profile declares no
floating point — so it is routed to `P4-SYSTEM.7` with the measurement, and recorded in
[`reference_softfloat-shared-ancestry`](docs/decisions/reference_softfloat-shared-ancestry.md).

⭐ **The encoding row cuts the other way, and was not anticipated.** Spike generates `encoding.h`
from `riscv-opcodes` (`c1d9bdf`); the Sail model hand-writes 59 files of `encdec` mappings and
never mentions `riscv-opcodes` under `model/`. Our assembler takes its encodings from
`riscv-opcodes` — so it shares an ancestor with Spike and **not** with Sail, which makes Sail
decoding our bytes an independent confirmation and Spike doing so not one. Independence is a
property of a pair and a subsystem, never of a tool.

⛔ **An instrument answered blind and nearly became a finding.** `strings | grep -ci softfloat`
returned `0` for *both* binaries. `nm -a` showed why that was blindness: Spike carries 649,743
symbols and 495 softfloat-shaped ones; the Sail release binary carries 400 symbols in total. The
source was cloned instead — at `29e6158`, the exact commit the binary's own `--build-info` names.

**New gate rule with real teeth:** an experiment may not compare two models whose independence has
never been examined. Fired RED on the real dossier: `UNEXAMINED PAIR rv64i-lab-v0/smoke-arith …
'not-examined' is a legal verdict, silence is not`. `--self-test` → `36 pass / 0 fail`, 36 arms
written and 36 run.

**Housekeeping forced by a ceiling, not a preference.** `docs/tasks/P0-PROFILE.md` crossed the
per-part ceiling (73,317 B > 65,536). The completed-leaf evidence was split, unedited, to
`docs/tasks/archive/` — the response the registry's own header prescribes. Verified that this did
not move pressure somewhere ungoverned: `git ls-files` is recursive, so the archive still counts
toward the family aggregate (240,293 B against a 393,216 ceiling).

🔎 `LIVE_STATUS.md` claimed "24 destinations governed" while the registry holds 25 rows and the
gate prints 25 — stale since `SEMULITH-P0-0013`. Corrected. The *class* — a live document
restating a count a registry owns — is not yet mechanized; `TREE-CLAIMS` covers task-tree facts
only. Owner: `MIRROR-DRIFT.4`, opened next.

🔎 **A gate boundary worth reporting.** `TASK-ACCEPTANCE` requires *every* staged `docs/tasks/*.md`
to carry a ticked checklist, which cannot distinguish the leaf that **owns** a change from a tree
that merely **receives** a routed finding. Annotating `P4-SYSTEM.7` with this leaf's measurement
therefore had to land as its own commit, because P4 has not started and ticking its template
would be a lie. The split is correct; the gate's inability to tell the two apart is the defect,
and an author hitting a gate's boundary is the highest-signal report that gate can receive.


## SEMULITH-P0-0021 (leaf P0-PROFILE.6) — run the matched-profile experiment, and the control that makes it mean something

**What changed.** `G0`'s second criterion — *an actual evidence path works* — is met. Two guest
programs run on two independently built reference models configured to the same profile, agree
with each other and with values derived from the specification, and reproduce byte for byte.

| Experiment | Exercises | Result |
| --- | --- | --- |
| `smoke-arith` | `LUI` sign-extension, the `*W` family, 6-bit **and** 5-bit shift amounts, wrapping addition | `AGREE over 12 aligned step(s)`; 12 of 12 specification-derived values match |
| `smoke-trap` | a misaligned 4-byte load (`D-MISALIGN-DATA`) | `AGREE over 3`, including cause `0x04`, `tval 0x80000401` on both |

- `scripts/riscv_asm.py` — an RV64I assembler and ELF writer that reads its encodings from the
  pinned tables and **carries no opcode of its own**, so a typo cannot invent an instruction.
- `scripts/compare_traces.py` — first-divergence comparison with a versioned exception adapter
  grounded in the pinned cause table. Ships 8 self-test arms.
- `scripts/run_smoke.py` — the whole path in one command.
- Tracked guest sources, and `smoke-arith.expected.toml`: 12 expected values, each with its
  derivation and its source locator, **written before the program was run**.
- `PROFILE-CONSISTENCY` gains 4 rules — an experiment claiming agreement must name the control
  that was observed failing.

⭐ **The control is the point.** Two models agreeing is a weak result until the agreement is shown
to be doing work. Flipping the Sail configuration's misaligned policy back to "handled invisibly"
— same ELF, nothing else changed — produced `FIRST DIVERGENCE at aligned step 2`: one model
loaded, the other trapped. The models agree *because* the profile is matched, and that is now a
measurement. It also resolves `OQ-3`: the laboratory's contained-trap choice is expressible in
the reference's configuration, so no comparator normalization is needed.

⛔ **The comparator was caught reporting a false pass, by running it.** Comparing only the
overlapping prefix, it printed `AGREE over 2 aligned step(s)` for a run in which one model trapped
and the other stopped emitting records. A shorter trace is now a non-agreeing verdict that must be
explained. Promoted to
[`docs/knowledge/a-shorter-trace-is-not-agreement.md`](docs/knowledge/a-shorter-trace-is-not-agreement.md).

⛔ **The pinned specification does not contain instruction encodings.** Measured: zero seven-bit
patterns across all six pinned artifacts; the format diagrams are images (31 in the RV32I chapter
alone). The semantics are all there in prose — the half that matters for expected values — so
encodings come from a separately pinned `riscv-opcodes`, recorded as its own provenance. That
source is upstream of both models, so encoding agreement is **not** independent evidence.
⭐ It contains exactly **52** instructions for this profile's extension set, and `P0-PROFILE.1`
enumerated exactly 52 by hand from the prose without using it. Symmetric difference: none.

**Four differences enumerated, not smoothed over.** Spike refuses an ELF with no section header
table while Sail loads it; Spike runs a built-in reset vector before the entry; Spike emits no
commit record for a trapping instruction; Sail performs two 16-bit fetch reads per 32-bit
instruction.

⚠️ **Scope, stated plainly.** This is evidence for *these inputs on these two models*. It is not
universal trace inclusion, and two models with shared ancestry can agree while both are wrong —
which is why `P0-PROFILE.7`, the independence inventory, is now the frontier.

**Validation.** `scripts/run_smoke.py` → all checks PASS. Two controls fired RED (un-match the
profile; falsify one expected value). `compare_traces.py --self-test` → `8 pass / 0 fail`, 8
written and 8 run. `check_profile_consistency.sh --self-test` → `30 pass / 0 fail`, with
`NO CONTROL` fired RED on the real dossier. Gate green; `make check` `1 passed`; book renders.


## SEMULITH-P0-0020 (leaf P0-PROFILE.5) — obtain three reference models and pin exactly which they are

**What changed.** The project had a subject and no second opinion about it. It now has three
reference models, obtained and run on this host, each configured as close to `rv64i-lab-v0` as it
can be, and each pinned so the next reader knows exactly which binary produced a number.

| Candidate | Status | Matched by | Self-report |
| --- | --- | --- | --- |
| Sail RISC-V 0.14 (prebuilt `Mac-arm64`) | obtained | a tracked JSON override | `rv64i_zvl32b` |
| Spike 1.1.1-dev (source build `1e05ddac`) | obtained | `--isa=rv64i --priv=m` | `rv64i` |
| QEMU 11.1.1 (pre-existing host toolchain) | obtained | `-cpu rv64i` | emits none |
| ACT, `act4` branch | reachable, **not acquired** | — | — |

- `profiles/rv64i-lab-v0/references.toml` — the dossier: 4 candidates, 3 recorded attempts.
- `profiles/rv64i-lab-v0/reference/sail-rv64i-lab-v0.override.json` — the tracked matched profile.
- `scripts/fetch_references.sh` — acquires and re-verifies, entirely on the repository volume.
- `PROFILE-CONSISTENCY` extended with 13 rules for the dossier, including one that **refuses a
  candidate with no `lineage`**.
- `docs/decisions/decision_reference-acquisition-route.md` supersedes the roadmap's cost estimate.

**The budget was wrong in the project's favour.** The plan priced this on building Sail through
an OCaml/opam toolchain. Release 0.14 publishes a native binary for this host's architecture, so
Sail became the *cheapest* candidate. Spike built against the system toolchain with no new
dependency installed; QEMU was already present and offers a CPU model named `rv64i`.

⛔ **One attempt failed and it is the instructive one.** The host package manager's `sail` formula
is a CLI for deploying WordPress sites to DigitalOcean — an exact name collision. The lookup
succeeded; the referent was wrong. Promoted to
[`docs/knowledge/availability-is-not-identity.md`](docs/knowledge/availability-is-not-identity.md).

⛔ **Two profile/reference differences are enumerated, not rounded away.** Sail cannot be
configured to exactly `extensions = []` — from 96 supported extensions it bottoms out at
`rv64i_zvl32b`, a vestigial minimum vector-length class instantiated even with the vector unit
disabled. And Sail **will not emit its effective configuration**: `--print-default-config`
ignores `--config-override` and the dumps are byte-identical, so the effective configuration is
*(default) + (our tracked override)* and that merge is ours, not the model's account of itself.

⛔ **Three models is not three opinions, and this commit claims neither usability nor
independence.** ACT derives its expected results from a configured Sail model. Spike and QEMU are
*plausibly* independent — a hypothesis. `P0-PROFILE.6` decides usability by running an
experiment; `P0-PROFILE.7` examines ancestry per subsystem.

**Validation.** `scripts/fetch_references.sh --verify-only` → six re-derivations, all `MATCH`,
`rc=0`. Fired RED on two controls: a corrupted digest → `DIFFERS spike binary`; re-enabling `M`
in the tracked override → `DIFFERS matched-profile ISA string … pinned rv64i_zvl32b actual
rv64im_zvl32b`. The 13 new dossier rules fired RED **on the real dossier**: `NO LINEAGE …/qemu`
and six `UNEARNED OBTAINED …/act4`. `PROFILE-CONSISTENCY --self-test: 26 pass / 0 fail`, 26 arms
written and 26 run — and the same reconciliation was run across every project harness (`9/9`,
`7/7`, `12/12`, `26/26`, and `9/9` on seam-integrity's own idiom), so none is skipping arms.
Gate green; `make check` `1 passed`; `make book` renders.


## SEMULITH-MIR-0019 (leaf MIRROR-DRIFT.3) — gate the live documents' tree claims

**What changed.** The third and last mirror on the resume path. `MEMORY.md` and `LIVE_STATUS.md`
state facts that `docs/tasks/` owns — how many leaves a tree has, how many are done, which tree
is active, which leaf is next. Thirteen such claims, held by zero instruments.

- **New doctrine `TREE-CLAIMS`** (`scripts/check_tree_claims.sh`): leaf totals, done counts, the
  frontier leaf and the set of active trees, all re-derived from the trees.
- **Its scope is data, not a list.** It reads the `hot_live` rows of `doctrine/readme_routes.tsv`,
  so a live surface registered tomorrow is covered tomorrow with no edit to the script — and
  `append_history` files are excluded deliberately, because a changelog line reading "2 of 9
  leaves" was true when it was written and rewriting it would corrupt the record.
- **Tree `MIRROR-DRIFT` closed, 3 of 3.** Index, doctrine documents and live docs are all gated.

**Validation.** This leaf had **no drift to repair** — the census at `.1` predicted it and the
gate confirmed it: `TREE-CLAIMS: ok (3 live document(s) …)`, `rc=0`. A mirror that happens to be
correct today is not a checked mirror, so the falsification came from breaking the real documents
on purpose and watching each control fire: `COUNT DRIFT MEMORY.md: '2 of 9 leaves' for
MIRROR-DRIFT; the tree has 2 of 3`; `DONE FRONTIER … the tree records it 'done'`;
`MISSING ACTIVE MEMORY.md: 'P0-PROFILE' is 'active' and the pointer does not name it`;
`COUNT DRIFT LIVE_STATUS.md: '13 leaves' for P1-LAB; the tree has 12`. Each restored.
`--self-test` → `12 pass / 0 fail`, 12 arms written and 12 run.

⭐ **The gates now catch each other.** Registering `TREE-CLAIMS` without adding its rows to the
two doctrine documents failed immediately — `NOT MIRRORED … 'TREE-CLAIMS' is registered and has
no row`, in both — which is `MIRROR-DRIFT.2`'s gate catching `.3`'s omission inside the same
commit. The identical omission had previously survived two registrations unnoticed.

⛔ Two of this leaf's own instruments were corrected by other gates rather than by review. A
first cut of the frontier rule matched any line *mentioning* "frontier leaf" and fired twice on
`MEMORY.md`, once on the pointer and once on a sentence describing it — a rule that fires on
prose teaches its reader to re-word the prose, so it is now anchored on the label, and the
narrowing was re-fired RED to prove it had not been disabled. And `SEAM-INTEGRITY` refused this
leaf's `ADDRESSED` box for carrying an assertion instead of a command; the box now carries the
census and its output.


## SEMULITH-MIR-0018 (leaf MIRROR-DRIFT.2) — gate the doctrine documents against the registry

**What changed.** Two documents restate the doctrine registry that lives in two shell arrays:
`DOCTRINE_ENFORCEMENT.md`, which calls itself "the human-readable mirror of the enforcer
registry", and the mdBook chapter `docs/book/src/working/doctrines.md`. Nothing compared either
with the arrays, and the book had fallen behind: it listed **3** project doctrines while **5**
were registered and running.

- **New doctrine `REGISTRY-MIRROR`** (`scripts/check_registry_mirror.sh`). Every registered id
  has a row in both documents; every id-shaped row is actually registered; project doctrines sit
  under the project heading and universal ones do not; every registered path exists and is
  executable; and a sentence of the form `<N> checks run today` states the real universal count.
  The **registry is authoritative**, and the failure text says so.
- **The book chapter repaired and grown.** The three missing rows added, plus two new sections
  that document the family honestly: which mirrors drifted, in which direction, and why a gate
  was chosen over a generator.
- **The silent-arm-swallow found at `.1` is now caught, not just written down.** Both self-test
  harnesses gained a strict-arity guard on every fixture helper, so a missing `;` before an `arm`
  call fails the self-test instead of deleting it.

**Validation.** Fired RED on the real documents before the repair — three `NOT MIRRORED`
findings, `rc=1` — and green after: `REGISTRY-MIRROR: ok (2 document(s) mirror the registry)`,
`rc=0`. The gate also fired in the **opposite** direction unprompted, catching a book row added
one step before its registration: `PHANTOM doctrines.md: 'REGISTRY-MIRROR' has a row but is
registered nowhere`. A document promising a gate that does not run is the more dangerous drift,
and it was caught on the real corpus.

`--self-test` → `11 pass / 0 fail` (10 RED arms plus a refusal arm asserting `rc=2`), with arms
written (`11`) reconciled against arms run (`11`). The new `argc` guard was fired RED by
deleting one `;`: `index() got 6 argument(s), expected 2`, `15 pass / 1 fail`, restored to
`16 pass / 0 fail`. Whole gate `all doctrines green`; `make check` `1 passed`; `make book`
`HTML book written`.


## SEMULITH-MIR-0017 (leaf MIRROR-DRIFT.1) — gate the task-tree index against the trees

**What changed.** `docs/TASK_TREE.md` is a hand-kept mirror of the task-trees under
`docs/tasks/`, updated by a *conditional* step in `COMMIT.md` ("only if the frontier changes")
and compared with its source by nothing. It had drifted: the index named `P0-PROFILE.2` as the
next leaf while the tree named `.5`, and `.2` was already `done`. One row of fourteen — and the
one that rotted was the only `active` tree, which is the only row the documented resume path
(`MEMORY.md` → the index row → the tree's frontier) ever reads.

- **New doctrine `FRONTIER-SYNC`** (`scripts/check_frontier_sync.sh`, registered in the project
  slot). It compares six properties, all of them functions of the tree: the frontier leaf, that
  neither document points at a `done` leaf, the status cells, any `A/B leaves complete` or
  `A of B leaves done` count, index↔tree closure in both directions, and that every leaf id
  named actually exists. The **tree is authoritative** and the failure message says so, because
  editing a summary to match its record is safe while editing the record to match its summary
  destroys the evidence.
- **New task-tree `MIRROR-DRIFT`** — every hand-kept mirror of a machine-readable source is
  gated. `.1` done; `.2` (the doctrine documents vs the enforcer registry) and `.3` (the live
  docs' derived numbers) are scoped with their measurements already taken.
- `DOCTRINE_ENFORCEMENT.md`'s project-doctrine table was split into three GFM fragments by two
  stray blank lines, so two registered doctrines rendered as literal text rather than rows.
  Repaired; the table now holds all six.

**Validation.** `check_frontier_sync.sh --self-test` → `16 pass / 0 fail` (14 RED arms, each
asserting the reason, plus two arms that assert `rc=2` refusal rather than a silent pass). Fired
RED against the **real** index before the repair — `FRONTIER DRIFT P0-PROFILE: index says '.2',
tree's Current Frontier says 'P0-PROFILE.5'`, `rc=1` — and green after:
`ok (15 tree(s) mirrored by docs/TASK_TREE.md)`, `rc=0`. Whole gate `all doctrines green`,
`rc=0`; `make check` `test result: ok. 1 passed; 0 failed`.

⛔ **The self-test lied first.** Its opening run printed `4 pass / 0 fail` while executing four
of fourteen arms: ten `arm` calls shared a physical line with the fixture call before them, so
bash handed them to a function that reads `$1`/`$2` and discards the rest — silently. Adding the
separator gave `13 pass / 1 fail`, and that failure was a genuine defect in the gate. Promoted
to [`docs/knowledge/self-test-arms-that-never-ran.md`](docs/knowledge/self-test-arms-that-never-ran.md).

⚠️ The mdBook's doctrine chapter is knowingly **not** updated by this commit. It already omitted
two registered doctrines; adding this one by hand would repair the symptom and destroy the
evidence `MIRROR-DRIFT.2` needs, whose acceptance requires firing its gate RED on the real
drift. Owner: `MIRROR-DRIFT.2`, the next commit.

---

Earlier entries are sharded, unedited, into [`docs/changelog/`](docs/changelog/) — beginning with
[`2026-09-pre-p0.md`](docs/changelog/2026-09-pre-p0.md), which holds everything up to and
including `SEMULITH-PKG.8`. Git history remains canonical for all of it.

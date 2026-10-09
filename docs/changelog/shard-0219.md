# DEV_NOTES shard — _(2026-10-08)_ … _(2026-10-08)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-08)_ — independent translation cache (P4-SYSTEM.12 e1c1)

Hart.walk always rewalked PTEs while SFENCE emitted flush prose. Added the selected
four-slot FIFO cache from state.sexp and pinned supervisor rules: 4-KiB keys, 16-bit
ASIDs, inherited globals, cached leaf/A/D bits and live permission checks. Legal fences
select register identity; illegal fences have no cache effect. Failed translations
never install. Direct permission fixtures now fence explicit PTE edits.

- Validation: parent ff75610 RED; 13 mutations RED; GUEST-GEN 103/103. Census 139/139
  architectural traces exact, zero refusals; 120/121 prior word texts exact, only the
  known incorrect unadopted cache guest corrected. All 42 owned records byte-exact.
  Production records/counts unchanged. Full evidence: docs/tasks/P4-SYSTEM.md e1c1.
- Promotion: declined — permanent hand fixtures and RED controls retain this lesson.
  Archive-family pressure is routed to LIVE-CONTAINMENT.4 before further appends.

## _(2026-10-08)_ — a zero operand value is not register x0 (P4-SYSTEM.12 e1c0)

SFENCE used values to choose scope, losing x0 register identity. Three evaluator tests
fail on c413dd3; history e839c1b introduced the value-only API. Nonzero registers holding
zero must select page/ASID zero, retaining other entries and globals under the declared
no-over-fence policy. The old fixture also encoded wrong registers and refilled in M.

The semantic effect now carries values and identity flags; None is x0, Some(0) a real
zero selection. Corrected raw words and armed the S refill with an occupancy assertion.
Four stale gate mutations now replace exactly one parsed effect; obsolete arity refuses.
Full root/history and verification: docs/tasks/P4-SYSTEM.md e1c0 and the Sv39 book.

- Validation: parent 0/3 then green; two selector mutations RED; translation 29/29;
  make check (153 core, 17 DSP, 193 verify), DEF-GEN 56/56 and books green. Scalar
  definition changes only two generator digests. Corpus/profile/counts unchanged.
- Promotion: declined — permanent regressions, typed API and arity gate retain the lesson.
  Independent author cache is next. New summaries kept bounded after archive pressure.

## _(2026-10-08)_ — CSR vocabulary and quoted annotations (P4-SYSTEM.12 e1b2)

The remaining three parcel refusals were mcounteren's missing address and a source
annotation containing quotes. Registered mcounteren/scounteren/menvcfg, legalized the
selected CY/TM/IR and STCE fields, retained WPRI and ignored unimplemented HPM fields.
S stimecmp read/write needs both mcounteren.TM and menvcfg.STCE before own effects;
M bypass and U address privilege remain intact. Counter accessibility changes no value
or progression. Writable counter rebasing remains an explicit bounded-author refusal.

records_sexp.quote_string exposes the existing canonical escape table. Its form renderer
and the expectation emitter share it, so quotes, backslashes, control characters and
Unicode round-trip for program, instruction, derivation and source. Removed the parcel
annotation refusal; historical word routing is unchanged. No engine trace provides values.

- Validation: masks/WPRI/alias, 30 counter/timer mode gates, read/write unit discipline,
  annotation/all-field literal round-trips, non-string refusal and emitted schema. Eight
  mutations and parent f099905 fail; three formerly refused guests match 117 steps.
  GUEST-GEN 89/89. All 121 prior word texts and 42 owned records byte-identical.
- Census: 138/139 architectural traces exact, zero vocabulary refusals; sv39-tlb-fence
  steps 191/192/195 remain the owned cache-policy disagreement. Fix e1c before staging
  C/counts. Production images/records/counts unchanged. Completed e1b1 receipt archived
  verbatim; DEV_NOTES crosses its fixed ceiling and shards with byte/order proof.
- Promotion: declined — permanent mode/string fixtures and eight RED controls retain
  this bounded-author lesson; the cache's schedule and reproduction are in the tree.

## _(2026-10-08)_ — author vocabulary is distinct from illegal instructions (P4-SYSTEM.12 e1b1)

Seventeen pre-bind refusals named valid integer operations whose computations or stock
prose were missing from the independent author. Added comparisons/XORI, XLEN and word
shifts, signed/unsigned branches and narrow load/store rules from the pinned chapters.
SLTIU sign-extends its immediate before the unsigned comparison; W shifts mask counts
to five bits, operate on the low word and sign-extend the result. Branch offsets remain
byte-relative and may target a two-mod-four address in this profile.

Reserved W shift bits are independently known. ReservedInstruction names that outcome
before effects, and the parcel route alone delivers the declared raw-word diagnostic.
Generic unknown valid vocabulary remains a Refusal. The older XORI/LBU negative controls
now use the real unmodeled mvendorid CSR, so extending coverage does not drop that guard.

- Validation: 22 hand arithmetic/alias/x0 cases, ten branch cases, narrow memory
  sign/width/alignment and three reserved raw words. Eight mutations and parent c70693d
  fail; 17 formerly refused guests match 471 architectural steps. GUEST-GEN 80/80.
- Regression: 105 prior historical word texts and 42 owned records byte-identical;
  16 new word outputs not adopted/written. All 139 parcel guests: 135 exact, one owned
  cached-translation disagreement, three named CSR/directive refusals. Record hashes
  unchanged. e1b2 owns the remaining vocabulary, e1c the cache, before count adoption.
- Containment: e1a receipt and closed .11 design/split moved verbatim to archive part 5;
  reconstruction asserted, fixed ceilings preserved. Promotion: declined — hand fixtures
  and eight mutation controls retain the lesson; remaining gaps are scheduled in the tree.

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


# DEV_NOTES.md

## _(2026-10-10)_ — authenticate citation evidence at both readers (P4-SYSTEM.13 c18c)

Actual locator/quote readers both returned rc=0 on three fetched RISC-V HTML
pages whose hashes differed from the source ledger, despite identical lengths.
Full byte diff isolates one Antora UI-version metadata value per page; architecture
text unchanged. The snapshot matches exact pins. The failure is reader identity,
not an ISA disagreement: published read headings without checking bytes, and
quote corpus used the same preferred fetched route. History roots: 32b72dbc's
reader, 3afd2757's route, bf2070a7's quote consumer. SEMANTICS also gated locator
work only on cache availability; cache failures could become an absence skip.

Shared verified_source now requires a regular file, valid SHA256/byte-length pin,
exact length and exact digest before either reader uses a page. Both paths refuse
alteration and malformed identity clearly; no silent fallback or repin. Shared
presence-only dispatch checks fetched-only data, treats partial/corrupt evidence
as present and permits a named skip only for absence. Cache resolution errors
propagate; quote entrypoint distinguishes source refusal from a text mismatch.
Non-snapshot http_status=0 handling and explicit synthetic --pages interface stay
unchanged. Locator controls run with SEMANTICS. All self-test scratch now derives
from target/doctrine-selftest; synthetic root paths are relative, not serialized
absolute paths. Correct the old pre-integration "not a commit gate" docstring.

Observed new controls against old code: locator 15 pass/3 fail (same-size text,
wrong length, absent identity), quote 14/1 (default-corpus changed bytes accepted).
After repair: locator 21/0, quote 15/0, SEMANTICS 8/0. Actual mismatched pages then
refuse through locator/quote tools and both wrappers (rc=1/2/1/2), naming source
and sha256. Seven route cases cover total absence, fetched-only, cache-only,
changed preferred source with valid fallback, quote integration, changed cache
page with valid manifest and corrupt manifest. No named skip hides corruption.

Authenticate snapshot manifest and all 72 files (0 failures), save/verify the old
three fetched pages on-volume, prove metadata-only diff, restore exactly 3 files /
226648 B and rehash against unchanged ledger. Public locators resolve 10 files/
12 bindings; quote corpus 118 attributed, 0 findings, 88 unattributed, two named
non-HTML source IDs (three instances). All 84 registry entries, production/core/
author/generated/frozen and 112 base/348 GC input files remain exact; 82/114 unchanged.
make ci rc=0, all five legs green (Rust 167/17/203, doctrines, bench, smoke bench,
main+five model books). Focused identities/controls/routes also rc=0. LIVE_STATUS
changes only doctrine arms 649→650; 47 chapters/P4 12/18 unchanged. Next c19 LOAD-X0.

Promoted to [a-version-string-is-not-an-identity](docs/knowledge/a-version-string-is-not-an-identity.md)
and its index: authenticating at acquisition does not authenticate a later reader;
presence dispatch must never turn corruption into absence.

## _(2026-10-10)_ — realize load extension and low-bit stores (P4-SYSTEM.13 c18b)

Bind LOAD-EXT POS scope-mem, NEG bound-ext/dir-ext-matrix, all eleven forms and
111 boundaries/222 parcels. Literal sign-edge arithmetic pins 8/16/32 widths on
both sides and unsigned partners; zero LB visibly overwrites -1. Wider reads
observe narrow stores leaving higher lanes zero, full SD/LD preserves the pattern,
and cross-width high lanes use the read width's sign. Non-clamping source values
distinguish truncation from saturation.

Before credit, seventeen isolated author copies fail committed observations:
signed LB/LH/LW zero-extension at scope-mem steps 12/14/16; unsigned LBU/LHU/LWU
sign-extension at steps 13/15/17; LD low-word18; SB/SH/SW high-bit selection at
bound-ext steps 23/28/33, overwide writes at scope-mem steps 22/24/26, saturation at
bound-ext steps 42/44 and scope-mem step 28; SD low-word at scope-mem step 17. Public registry gate
first fails the missing LOAD-EXT entry (rc=101), then both bindings run. Normal
full independent replay is 167/5365/10524 exact; Rust 167/17/203 passes make check.
Only registry/tests, review docs and derived GS change; every prior 82 entry and
112 base/348 GC canonical+guest inputs, production core/author, generated data and
frozen definitions remain exact. Effective 82/114, registry 84, sixteen pairs/freeze
remain. NEG is a legal semantic counterexample, not an invented trap.

Source review found fetched RV32I/RV64I bytes differ from ledger digests, with
same lengths. Exact diff is one Antora UI-version meta value per page; the local
snapshot matches both pinned hashes, and its full relevant sections supplied this
review. check_citations._work_dir prefers any fetched directory; published reads
without digest checks, and quote reader uses the route directly. Owned priority
c18c repairs both evidence paths immediately after this commit, before further
runtime pairs. No architecture-body or processor mismatch; no repin or silent
fallback authorized. Details/reproduction and repair schedule are in the task.

Focused identity/reports/freeze/schema/bounds/counts and main+five model books
pass (rc=0). Required hooks precede c18c. The first hook refused the combined
acceptance box; split ROOT CAUSE/ADDRESSED/NO REGRESSION into distinct ticked
boxes with their own actual tool results, then rerun the required hook.
LIVE_STATUS unchanged: 649 arms/47 chapters/P4 12/18. .14 retains status/experiment work.
promotion: declined (worked matrix and finite controls live in the integer book; the separate identity defect is owned with immediate repair in the task).

## _(2026-10-10)_ — bound live history and correct current summary pointers (P4-SYSTEM.13 c18a)

Move eight oldest whole DEV entries through shard_history into shard-0223; old
21 entries = 13 live + 8 moved, exact order/bytes. Head 46093→31607 B before this
new note; inverse SHA 0f5b1aae5a4f4d5db4c98a64935d5d5c98b5cc1d2d1dc360bae49b502c92167f.
Manifest 15 live rows, 225 logical with sealed history; old prefix/index untouched.
A new navigation footer follows the preserved tail separator. Removing only that
footer and this new entry restores the exact old-head inverse.

Move completed c17a–f designs/diagnosis, acceptance, verification, commit and
changelog blocks verbatim into archive 8: 16048/13941/1758/904/2093 B. Task
88963→54940 B at partition; ordered inverse SHA
6dc33f903c724b56063445e4d3c162b5e5f06d0673fe0a0ba7c959443bf1bac7.
The ownership plan was the sole pre-partition addition; every moved block matches
committed d5519fb. Also move 22982 B of appended profile progress (SHA
8702aa8818fd213186bdafcf103cb513ad2cb26df70904d5bc2753d1c6b3e184).
Archive payload markers declare exact byte lengths/hashes; all six re-read exact.
The archive is 59436 B, below the fixed 131072 part cap; archive 7 stays untouched.
Current profile keeps normative interface sections, canonical/GS/registry/book
pointers and history link. Historical "current" labels retain their source context
inside the explicitly historical archive, not live authority.

Scoped review also found duplicated summaries that escaped append-only progress:
ENV intro v2=11 and runtime count76, old frozen-v1 STIP source, and book intro64.
Canonical probe gives 12 members and 80/114, with v2 STCE-selected software/
comparator pending. Blame locates member row at e0f3daea, count76 at 01154383,
old boundary source at 75c20ff0, book64 at c0507d02. Correct the effective source,
remove the stale self-currency phrase, label v1 bindings historical, and route
live totals to canonical membership/derived report/current book summary. The
archived old runtime table remains exact for audit; all current feature examples
stay in the book. No production, frozen-record or contract-credit change.

Focused partition/source identity, shard freeze/bounds/frontier/counts/contracts/
reports and main/model books all pass (rc=0). The new frozen shard intentionally
retains its source entry’s trailing blank line: exclude only that byte-proven file
from diff whitespace review; every other changed file passes. LIVE_STATUS
remains 649 arms/47 chapters/P4 12/18, effective 80/114. c18b load matrix next.
promotion: declined (byte-authenticated archive payloads, canonical/derived pointers and existing containment doctrine retain the proof and prevent duplicate summary drift).


## _(2026-10-10)_ — realize signed word results and ignored overflow (P4-SYSTEM.13 c17f)

Bind WSUFFIX POS scope-alu/bound-arith, NEG bound-shiftw: all nine RV64I forms
in REQ-D-WSUFFIX over 122 boundaries/244 parcels. M's five word forms retain
separate existing M evidence. Sixteen isolated author copies fail named
observations before credit: nine zero-extended results, four full-width right
sources, three signed-32 saturating add/subtracts. Zero-extension first fails
ADDIW bound-arith 17; SLLIW bound-shiftw 41; SRLIW 34; SRAIW scope-alu 29;
ADDW scope-alu 23; SUBW bound-arith 20; SLLW bound-shiftw 53; SRLW 51;
SRAW scope-alu 27. Source-width errors first fail SRLIW scope-alu 28, SRAIW
bound-shiftw 59, SRLW scope-alu 26, SRAW bound-shiftw 58. Saturation fails
ADDIW bound-arith 17, ADDW 19 and SUBW scope-alu 24. Shared finishes condition
only the named mnemonic; every other expression stays unchanged.

ADDIW on 0xdeadb7ef7fffffff plus one ignores the upper word and wraps to
0xffffffff80000000; zero-extension gives positive 0x80000000, saturation
0x7fffffff. SUBW on INT32_MIN minus 1620 wraps to positive 0x7ffff9ac, whereas
saturation stays INT32_MIN. Right-shift source width matters; for add/subtract
and left shift, pre-truncation commutes with a correct final low32 truncation,
so equivalent rewrites are not misclassified as faulty countermodels.

Registry 82, effective 80/114: thirteen scope/twenty guest/six boundary/one
execution pairs, seventeen runtime pairs/freeze remain. Make check passes
fmt/clippy and Rust 167/17/203; normal selected/full corpus exact 167/5365/10524.
Identity preserves all 112 base/348 GC canonical/guest files and prior 80 entries,
production/core/author/definitions/generated/frozen bytes. Integer probe retains
23 arithmetic/10 branches, 17 gaps/476 steps, 42 owned records; guest generators
49/167 fresh, mirror 49 with 42 count migrations/7 explicit re-derivations.
Five reports/count claims, three frozen versions/zero findings, schema 270/two
named skips, 37 bounded routes and main/model books pass. LIVE_STATUS unchanged
649 arms/47 chapters/P4 12/18. No live reference rerun for unchanged inputs/rules.
Next c18a losslessly contains near-ceiling DEV/profile history, then c18b loads.
promotion: declined (canonical independent witnesses, executable registry pair and integer runtime chapter retain the signed-word guarantee).


## _(2026-10-10)_ — complete SHAMT requirement associations (P4-SYSTEM.13 c17e)

The original base associations (1abba2e) omitted SLLW/SRLW/SRAW; GC copied the
nine-form list at b95af58. The statement already names all twelve. Aggregate
extraction still covers the omitted forms through WSUFFIX, hiding the individual
requirement's missing associations. Two focused owner/mirror assertions query
canonical catalogs and compare the complete twelve-form list; observe cargo test
rc101 / 0 passed / 2 failed BEFORE data repair. Both diagnostics print nine
actual names against twelve expected. Add only the three insns fields to
REQ-D-SHAMT in both catalogs; then the same command passes 2/0. Order does not
matter; duplicates fail. Shared catalog client preserves the old obligation
query/caching behavior while serving the two flat requirement catalogs.

No statement/status/obligation/instruction/expectation change. Identity proves
every other requirement field/record and 111 other base/347 other GC inputs exact;
production/core/definitions/generated/frozen/80 registry entries exact. Re-pin
base dossier 267e8e23…a55f → f9246561…a8dc after profile documentation; regenerate
board/platform/model/report owners. Eight board data documents retain all other
values, with only shared pin and the three associations in its composed requirement
changed; map/four model material bodies retain all but display pin/provenance.

Make check passes fmt/clippy and Rust 167/17/203. RECORD-SCHEMA validates 20 files
and the Rust graph examples, EXTRACTION five units sufficient, five reports
fresh, freeze three versions/zero findings, dossier schema 270/two named skips,
materials five units, derived counts five claims, bounded routes 37 and main/model
books pass. LIVE_STATUS unchanged at 649 arms/47 chapters/P4 12/18; effective
78/114 unchanged. The association defect is closed, c17f word-result review next;
.14 retains statuses/experiment/registration work. No reference rerun is needed
for metadata-only changes: all execution inputs and rules remain byte-exact.
promotion: declined (two refusing cross-record assertions and integer runtime chapter retain the association repair and history root).


## _(2026-10-10)_ — realize all twelve shift-count domains (P4-SYSTEM.13 c17d)

Bind SHAMT POS to scope-alu and NEG to bound-shift/bound-shiftw: 180 boundaries /
360 parcels. The frozen statement and pinned RV64I 3.1.2.1–2 specify six bits for
XLEN immediate/register counts, five for word immediates and low-five rs2 for
word registers. Twelve isolated author copies each change one mnemonic count
expression; all fail before credit. XLEN five-bit copies first fail SLLI
bound-shift 1, SRLI 35, SRAI 73, SLL 87, SRA 88 and SRL bound-shiftw 49. Four-bit
word-immediate copies fail SLLIW bound-shiftw 46, SRLIW scope-alu 28, SRAIW 29.
Six-bit word-register copies fail SLLW scope-alu 25, SRLW bound-shiftw 51 and SRAW 55.
The repaired SRAW count-96 witness now independently closes its old masking gap;
source-width witnesses remain exact. These legal counterexamples invent no traps.

Add only two registry entries and their declared-check closure: registry 80,
effective 78/114, thirteen scope/nineteen guest/six boundary/one execution pairs.
Eighteen runtime pairs/freeze remain. Make check passes fmt/clippy and Rust
167/17/201; integer probe retains 23 arithmetic/10 branches, 17 gaps/476 steps,
42 owned records exact. Full independent author corpus is 167/5365/10524 exact.
Byte comparisons preserve all 112 base/348 GC canonical/guest files, prior 78
registry entries, production/core/definitions/generated/frozen data. Freeze
three versions/zero findings, schema 270/two named skips, five fresh reports,
five derived counts, 37 bounded routes and main/model books pass. LIVE_STATUS
stays 649 arms/47 chapters/P4 12/18. Profile/book/resume report the new pair.

Scoped requirement review found REQ-D-SHAMT's insns fields omit SLLW/SRLW/SRAW
in BOTH owner and GC mirror, although its statement explicitly covers all twelve.
Record probes confirm 9/12; git log -S and git show locate incomplete base
associations at 1abba2e and the GC copy at b95af58 (original d3fecbf had none).
WSUFFIX covers the three in aggregate extraction, hiding per-requirement metadata
incompleteness. No execution/frozen-statement defect. Own c17e metadata repair
immediately next with a refusing closure assertion and dependent regeneration;
keep this binding's exact-input proof bounded. c17f WSUFFIX follows; .14 retains
statuses/structured experiments/registration work.
promotion: declined (canonical witnesses, executable registry pair and integer runtime chapter retain independently discriminated count domains).


## _(2026-10-10)_ — distinguish arithmetic-W source width (P4-SYSTEM.13 c17c)

The separate width diagnosis showed both isolated full-width arithmetic-W authors
survived every old corpus observation: all 38 source occurrences already were
canonical signed words. Both public literal forms on zero-extended 0x80000001 by
one distinguish correct 0xffffffffc0000000 from bad positive 0x40000000.

Append four pre-derived instructions to both bound-shiftw programs: AND obtains
x17=0x0000000080000001 from x8/x12; ADDI sets x18=1; SRAW x19,x17,x18 and SRAIW
x20,x17,1 each require 0xffffffffc0000000. Literal words are 00c478b3, 00100913,
4128d9bb and 4018da1b at 0x800000e0/e4/e8/ec, recorded before models execute.
All 56 old instruction positions/bytes/observations stay exact; budgets become
60 steps, base 60 word requests / GC 120 parcels. Each isolated wrong author now
fails only its new boundary (58/59); public wrong tables first fail there too.

Existing hand-encoded garbage-upper-word cases already discriminate both rules.
Add isolated sraw-width/sraiw-width mutation routes, observe each rc1 with its
named arithmetic-word reason before arm registration, then register two controls.
Normal probe retains 23 arithmetic/10 branch cases and 42 owned records exact;
17 gaps now have 476 steps. Derived doctrine total becomes 649 (GUEST-GEN 145).
The independent full corpus matches 167/5365/10524; make check passes Rust
167/17/201, fmt/clippy. Fresh pinned Sail agrees on all 60 declared rows/change
observations and repeats byte-identically. Base live smoke passes all enabled
comparisons/reproductions, including the changed program against Sail and Spike.

Identity proves 110 other base/346 other GC inputs, production/core/definitions,
frozen records/78 entries and all other generated guest data exact. Re-pin shared
base dossier df48b3a6…f38a → 267e8e23…a55f through the declared board definition;
eight board S-expression data documents retain every other value; map/four
material bodies change only display pin/provenance. Derive all five reports and
both model-book units, including base expected-step total 644→648. Freshness,
freeze (three versions/zero findings), schema (270/two named skips), counts (five
claims), main/five model books pass. Both source-width evidence defects close;
core rules stay correct and unchanged, effective credit stays 76/114. c17d SHAMT
binding follows isolated mask controls. Finite reference/platform limits remain.
promotion: declined (durable isolated controls, derived guest boundaries and integer runtime book retain the verified repair).


## _(2026-10-10)_ — close SRAW mask discrimination with a pre-derived boundary (P4-SYSTEM.13 c17b)

Append SRAW x16,x8,x10 = 0x40a4583b at 0x800000dc to both bound-shiftw profiles.
Existing x8=0xffffffff80000001 and x10=96 give count zero; literal expected x16
is 0xffffffff80000001, recorded before either engine executes. Preserve all 55
old instruction positions/bytes and observations. Budgets become 56 steps, base
56 word requests / GC 112 parcels. Correct SRLW step 51's explanatory six-bit
alternative to zero in the explicitly defined wide evaluator; its required
expected identity remains unchanged. No production instruction rule changes.

The isolated SRAW author now fails only new boundary 55; public step_over bad
table also fails there (rc101). The normal independent corpus matches all 167
guests / 5361 boundaries / 10516 parcels. Add one hand-encoded count-96/garbage-
upper-word case and isolated sraw-count mutation to the durable integer probe.
Observe rc1 with SRAW five-bit count before registering the GUEST-GEN arm.
Normal probe: 23 arithmetic/10 branches, 17 gaps/472 steps, 42 owned records exact.
GUEST-GEN 143, global arms 647. Fresh pinned Sail agrees on 56 declared rows and
change observations; two traces byte-identical, including the added SRAW.

Identity keeps 110 other base and 346 other GC canonical/guest files, all core,
definitions, production author, frozen records and 78 entries exact. Both Rust
guest fixtures retain every other guest datum byte-exact. Re-pin base dossier
from 9f7cecb3…d784 to df48b3a6…f38a, regenerate board/platform/model-book outputs;
parsed board data stays exact except the pin, map/material bodies except display
and provenance. Rust make check passes 167/17/201; focused gates and final make ci
pass all five legs (check, gate, bench, smoke-bench, main/model books).
SRAW count-mask coverage and SRLW explanatory defects closed,
no new contract credit: 76/114, nineteen pairs/freeze remain. Initial CI refused
the base material's old 643 expected-step total; second refused G0/G1's matching
old totals. Re-derive through the owners; fresh base live smoke rc0 verifies all
enabled comparisons, including bound-shiftw against Sail/Spike over 56 steps.

Adjacent width review confirms a separate evidence defect, OPEN priority-next
c17c before c17d SHAMT binding: isolated SRAW and SRAIW full-width source authors
each match the entire 167/5361/10516 corpus. Public bad tables match 105 boundaries;
all 38 arithmetic-W source occurrences already are canonical signed words.
Both literal SRAW/SRAIW with x8=0x0000000080000001 and count one distinguish
correct 0xffffffffc0000000 from bad 0x40000000. The current count-zero witness
cannot test pre-shift truncation. Core correct; add derived witnesses and durable
isolated controls next. Task and integer book retain the diagnosis and ownership.
promotion: declined (durable author case/refusing control, boundary guest and integer runtime book retain the verified repair).


## _(2026-10-10)_ — diagnose SRAW mask coverage and retain bounded evidence (P4-SYSTEM.13 c17a)

Before registering SHAMT, isolate SRAW's five-to-six-bit count mutation in a
spec-side author copy. It still matches all 167 guests / 5360 boundaries /
10514 parcels. The public step_over API with a caller-supplied mutated SRAW
Sem tree also matches all three SRAW-bearing programs / 104 boundaries.
Root: count 20 gives the same mask; -1 shifts the negative word by 31 or 63
to all-ones; remaining destination is x0. Immediate SRAIW sweeps do not
exercise this register-count distinction. Core semantics are correct; corpus
coverage defect OPEN and owned priority-next c17b, before c17c binding.

Hand-encoded SRAW x16,x8,x10 = 0x40a4583b, x8=0xffffffff80000001 and x10=96,
yields x16=0xffffffff80000001 under the correct count-zero rule, all-ones under
the six-bit/count-32 copy. Both independent author and public core agree.
Also diagnose SRLW step 51's explanatory alternative: widening its count in
the present wide evaluator yields zero, not the old prose's 0xffffffff80000000.
The existing correct expected value is unchanged. c17b adds the pre-derived
SRAW boundary to both profiles and corrects only the misleading explanation.

Before further evidence growth, shard CHANGELOG's oldest 35 entries to 0221
(101=66+35) and DEV_NOTES's oldest 13 to 0222 (28=15+13). Ordered inverse byte
identity hashes: 27d7e70f97cba0f6100be7bf89bf0959831fcb4e00f598d2b9eee36ccff91d92
and 68c5290cc5d653f6cba04960ddd190eaf4e3b726c06dfed2f5ff8941f28c9526.
Manifest now fourteen shards; no sealed archive descriptor changes. Move fourteen
each of completed c8–c16 designs, acceptance, verification, commit and changelog
blocks byte-verbatim to task archive part 7; full inverse hash
0a208867adf4e332fca70d2d9c19639030425778c244667024acd4a2451b552c.
Task 126431 to 53929 B at partition, archive 125593 B under fixed 131072 cap.
Move 6973 B of completed integer book sections exactly (SHA256
c6c65a32bb94ea55c25ed01d2c27a13c8d07236d882d0de36e016f045562f30d)
into a linked chapter, retaining old anchor routes. Add diagnosis and repair
ownership there; chapters 46 to 47, the only changed LIVE_STATUS metric.
All production/core/author/guest/canonical data and 76/114 credit remain exact.
SHARD-FREEZE passes 224 logical rows/two heads; bounds 37 destinations, frontier
33 trees, five derived claims, freeze three/zero findings, five fresh reports/
20 controls and main/model books pass. Post-edit history/book comparison retains
every old byte in order. Commit hooks precede priority-next c17b.
promotion: declined (integer runtime chapter and scheduled task retain the diagnosis; c17b owns durable controls and repair).


## _(2026-10-10)_ — U-immediate sign and instruction PC (P4-SYSTEM.13 c16)

Read/rehashed RV64I 3.1.2.1 (49,246 B, 6eadb316…f13abd), canonical U rows and
shared width/PC/wrapping lowering. POS scope-alu/dir-chase, NEG bound-arith:
79 boundaries / 158 parcels independently exact. LUI 0x80000 gives
0xffffffff80000000; LUI 0x7ffff gives 0x7ffff000. AUIPC at 0x80000074 with
0x80000 wraps to 0x74; the positive edge at 0x80000078 gives 0xfffff078.
Zero offsets return each actual instruction PC, including chase offsets 0/16/28.
Seven wrong alternatives fail intended steps: LUI zero extension/no shift at
scope 3; AUIPC zero extension/no shift/saturation at bound 29; next-PC or
sign-extended base at chase 0. NEG is a legal semantic counterexample witness.

Own/fix encountered stale smoke headers in both profiles: original b8d09f5
pre-B/J comment, copied unchanged at 133e722, also still named profile.toml.
Comments now describe profile.sexp and implemented B/J support. Both old/new
images are exactly twelve instructions / 48 bytes. Generated data bodies
stay exact; only source fingerprint comments regenerate. GC's other 347
canonical/guest files, author/core and all 76 prior entries remain exact.
Independent integer probe retains 22 arithmetic/10 branch cases, 17 gaps/471
steps and 42 owned records exact. Registry 78, effective 76/114: thirteen scope,
eighteen guest, six direct assumption and one execution pair. Initial commit hook
correctly refused PLATFORM-GEN: the base comment changed its dossier digest while
the board retained f24ca76d…8a74e. Own and rederive pin 9f7cecb3…d784 through the
shared digest owner; regenerate board/platform and model-book materials. Independent
parsed-data comparison retains all board semantics except the digest pin; map and
four material bodies retain all other content. BOARD-GEN, PLATFORM-GEN/11 controls,
MATERIALS-BILL (five units), refreshed reports and schema pass before retry.
make check passes Rust 167/17/201; GUEST-GEN fixtures/mirror and 142 controls
pass, schema 270/two skips, freeze three/zero findings, five reports/20 controls
and all book builds pass. Next OB-SHAMT;
nineteen runtime pairs/freeze remain.
promotion: declined (canonical rules, exact observations and worked runtime book retain the evidence and header correction).


## _(2026-10-10)_ — register ALU wrapping and operand overlap (P4-SYSTEM.13 c15)

Read pinned RV32I 1.1.4.2, seven semantic rows and shared lowering/GPR discipline.
POS binds scope-alu/bound-arith; NEG bound-alias. Independent replay matches
31+31+37 boundaries / 198 parcels and every committed observation. Selected
witnesses distinguish AND/OR/XOR (0x450/0x674/0x224), signed/unsigned -1 comparisons,
INT64_MAX +1 and INT64_MIN -1 wrapping, and aliased ADD x20,x20,x20 from 5 to 10.
SUB and SLT identical-source results visibly overwrite earlier values with zero.

Eight in-memory author alternatives fail their named steps: saturating ADD/SUB
at boundary steps 5/6, swapped SLT/SLTU signedness at scope steps 11/13, wrong
AND/OR/XOR at scope steps 5/6/7, prematurely cleared aliased ADD sources at alias
step 24. The durable integer-author probe retains 22 arithmetic/10 branch cases,
17 corpus gaps/471 steps and 42 owned records exact. NEG is a semantic
counterexample witness for legal programs, not an invented trap requirement.
Identity retains all 348 canonical/guest files, four author/generated files,
all core bytes and 74 earlier entries. Registry 76, effective 74/114: thirteen
scope pairs, seventeen guest pairs, six assumption pairs and one execution pair.
make check passes Rust 167/17/201, fmt/clippy; schema 270/two named skips,
freeze three/zero findings, report controls 20/0 and five fresh reports, and
main/model book builds pass. Twenty runtime pairs/freeze remain; next OB-LUI-AUIPC.
promotion: declined (existing bindings, observations and worked runtime book retain the finite realization).


## _(2026-10-10)_ — bind immediate ALU arithmetic and counterexamples (P4-SYSTEM.13 c14b)

Rehash/read the pinned RV32I 1.1.4.1 clauses; six authored semantic rows match
sign extension, wrapping arithmetic, signed/unsigned comparison and logical
operations. POS names scope-alu, NEG bound-arith; both whole legal programs.
Their 31+31 boundaries /62+62 parcels independently match every committed GPR
change. Scope steps 8/9/10 read ANDI/ORI/XORI values 0xffffffff80000000,
0xffffffff800007ff and 0x7fffffff; step 16 observes the visible 1-to-0 unsigned result,
step 17 proves SLTIU sign-extends -1 before unsigned comparison. Boundary step 8
wraps INT64_MIN + -1 to 0x7fffffffffffffff; steps 9/10 cover -2048/+2047.

Five in-memory author alternatives fail exact observations: zero-extended SLTIU
at scope step 17, unsigned SLTI at step 14, zero-extended ANDI/XORI at steps 8/10, saturating ADDI at
bound step 8. Existing integer-author sign mutant refuses; normal 22 arithmetic/10
branch cases and 17 corpus gaps/471 steps pass, plus 42 owned records exact.
The new binding changes no instruction, expectation, canonical record, author
or core semantics. Identity: 348 profile files+four author/generated files and 72
prior entries exact. Registry: 74, effective 72/114:13 scope,16 guest,6 direct
assumption,1 execution pair. Gate oracle 20/0 passes with actual ALU registered.
make check passes Rust 167/17/201 and fmt/clippy. Focused schema270/two skips,
freeze3/zero findings, five report freshness checks and books pass. Hooks precede
commit; no new mechanism warrants repeated full CI.
Next OB-ALU-REG; 21 runtime pairs/freeze remain. Promotion declined: exact guest
bindings, original expected observations and worked runtime book retain it.


## _(2026-10-10)_ — contract-count controls survive complete registration (P4-SYSTEM.13 c14a)

The shared-id self-test hard-coded CHK-ALU-IMM-POS as unregistered. Simulating
its valid registration produced 17/18 controls: inserting it again cannot earn
another check, so actual 114/71 correctly disagreed with expected 114/72.
The production measure was right; fix the test before the planned ALU binding.
Scratch catalogs now add one reserved check to an independently selected
effective record. It earns credit only through that unit's exact registry pair;
an undeclared or unbound copy earns none, and a unit without a registry gets none.
New duplicate and full-coverage controls require no real check to stay missing.
The full fixture realizes every effective pair, then independently distinguishes
a new unbound declaration and its binding. Duplicate-credit mutant fails 19/20;
all 20 corrected controls and the formerly failing ALU-bound fixture pass.
Production AST outside _selftest, all crates/profile/author bytes and 70/114 stay
exact. The report wrapper verifies all generated reports; no new CPU credit.
No Rust change; report wrapper verifies five reports, all20 controls pass,
make book succeeds and derived-count controls10/0. Commit hooks precede c14b. Next
c14b OB-ALU-IMM. Promotion declined: live oracle controls and runtime book retain
this correction and its future full-coverage edge case.


## _(2026-10-10)_ — observable supervisor timer programming (P4-SYSTEM.13 c13b)

The terminal-zero guest defect is closed for SSTC contract coverage by direct
Execution evidence, separate from provider-assumption Boundary and static Scope.
Registry tests run the new architectural witness plus companion guests using
one existing corpus comparison helper. POS retains i-timer/w-timer; NEG retains
mm-stimecmp. No production semantics or old input changes are introduced.

POS executes thirteen S instructions /26 parcels with TM/STCE/delegation seeded
and interrupt enables clear. It programs compare 16, reads16 and pending 0,
programs 0 and reads pending 32, programs 32/read-back/cleared pending, then writes
and reads 0x8000000000000020 to retain the full 64-bit compare value. Sentinels
make zero reads visible. Each boundary checks all 32 GPRs, S mode/next PC, raw
compare, time/retirement and fetch count; no M round trip hides inside the budget.
NEG has three six-step cases: S missing TM, S missing STCE, U despite open gates.
CSRRW must deliver cause2 before source/destination/compare effects. Actual M
handler reads cause2, offending word 0x14d29373, EPC 0x1000 and unchanged compare 101,
then writes marker42. Trap owners and all GPRs/mode/PC/counters/fetches are exact;
first step does not retire. Direct pair totals 31 boundaries /62 parcels.

Independent counter-author replay agrees with all literal values. Its scratch
forced-all-S-illegal copy still matches old mm-stimecmp's 35/70, ending unexpectedly
in M, but the new POS refuses at boundary 2. Disabling that positive verifier
fails with a terminal-control-missed reason before its new GUEST-GEN arm is
registered. Real-engine tests reject POS with either gate closed, and reject
NEG with opened permission. Three direct tests and four registry tests pass.
GUEST-GEN142, registered shell arms646. Full make ci passes all five legs; Rust167/17/201, all doctrines/books green.

Identity: 348 profile canonical/guest files and four author/generated files exact,
core entirely unchanged, all 70 prior registry entries exact. Full independent
corpus remains 167/5360/10514 and --check-owned 42 exact. Schema/freeze/gate owners
retain their authority; report controls 18/0. Registry now 72 including historical
superseded checks, effective 70/114:13 scope,15 guest,6 direct assumption,1 direct
execution pair. Twenty-two runtime pairs and freeze remain. Next OB-ALU-IMM;
CPU-SYSTEM/firmware/Linux acceptance is not implied.
Promotion declined: the live execution mechanism, refusing control and worked
runtime book retain the lesson with its exact old/new witness behavior.


## _(2026-10-10)_ — STCE selects software or comparator STIP (P4-SYSTEM.13 c13a2)

Pinned Machine 2.1.1.18 makes STCE-clear STIP behave as absent Sstc;
2.1.1.9 then permits M software writes. The old unconditional comparator
introduced in 47badd2 discarded those writes and made cold pending one.
Repair the shared CSR field selection/legalization: cold STCE=0 reads raw
mip.STIP=0; M sets/clears it. STCE=1 selects unsigned time>=stimecmp and
ignores STIP writes. sip.STIP stays read-only/delegated. Retaining software
STIP behind the comparator is an explicit lab choice; no hidden owner is added.
Four core regressions fail before repair and pass after, including 48 actual
CSR instructions across all six forms, raw states and compare/source choices.
Existing comparator-only interrupt/time/event fixtures now enable STCE explicitly;
cold reset expectations become zero. State and definition input pins regenerate.
Affected FP-dirty comments now cite pinned conservative tracking permission,
removing implementation-specific dependency assumptions without changing FP.

The independent author follows the same clauses. Eight literal source/write
cases plus retention pass; four new source/write/retention mutants each fail
before registration. GUEST-GEN141; registered shell arms645. All 167 guests
remain independently exact at 5360 boundaries / 10514 parcels, all 42 owned
records exact. Original public CSR reproduction changes rc101 to rc0. Corrected
public Sail diagnostic still reports its qualified STCE-enabled platform gap.

Open v2 supersedes the frozen interrupt-source assumption, with a direct
POS/NEG pair executing 27 instructions / 54 parcels. Literal observations
cover source selection/transitions, forbidden M pending writes, retained raw
STIP and read-only delegated sip in M/S; every step checks all GPRs, mode/PC,
raw owner and parcel count. Ignored architectural writes are not invented
provider violations. Old bindings still run, but superseded credit is removed:
70 registry entries, 57 effective obligations / 114 checks / 68 realized.
No SSTC credit yet: c13b must repair the old terminal-zero witness hole.

Gate-report self-tests exposed an oracle defect: every registry entry was
assumed effective. Recount now independently intersects effective declared
pairs and registry pairs; dropping supersessions restores old credit. A new
synthetic realized-record supersession control catches the disabled filter;
mutant 16 pass / 2 fail, corrected 18/0. Production measure remains unchanged.

Identity proof: 335 guest files (334 source/record files plus run order), all
52 frozen record lines and both frozen forms exact; 68 earlier bindings exact.
DEV_NOTES containment moves 21 completed entries verbatim to shard-0220,
15329 B. Inverse reconstruction SHA256 b2fc35ed2b74186ccd13b60fda26e891c7ad39f5ee81f7d99403785712bf8306
matches committed head; fixed caps unchanged. Focused make check passes
Rust167/17/198; schema270/two named skips, freeze3/zero findings.
Full CI first exposed a stale compressed staging blueprint: c-irq still lacked
STCE, so both GREEN staging arms failed x7 (139/141). Repair its independent
setup/deadline/budget/PC checkpoints to the adopted input, not the processor.
Staging now gives 28 guests / 37 forms / 431 boundaries / 712 parcels; repeat
is byte-exact, both corrupted record controls refuse. Its c-irq body and complete
semantic record equal the adopted guest (19/32). All production inputs stay exact.
Full make ci passes all five legs (check, gate, bench, smoke-bench, book);
Rust167/17/198, all doctrines green and both book families build.
Promotion declined: explicit contract/history and worked runtime book retain
these corrections and controls.


## _(2026-10-10)_ — explicit comparator setup preserves timer schedules (P4-SYSTEM.13 c13a1)

Nine timer-source guests now enable STCE in M with LUI x31,0x80000 and CSRRS
menvcfg; x31 was unused. Independent derivation preceded processor execution.
Budgets increase by two, bodies move eight bytes and finite deadlines increase
by two ticks. All body instruction bytes except declared deadline immediates
and all GPR observations under that exact transformation agree. The nine inputs
span 281 boundaries / 524 parcels; full corpus 167 / 5360 / 10514. mm-stimecmp
and 316 other guest files, all four contract/version files and registry stay exact.
Removing stale inline chronology while providing fresh route provenance saves
19880 B across the nine source/record pairs; fixed family ceilings need no change.
The w-timer comment's old mepc=0x80000044 was wrong: assembly and observation
both give old WFI+4=0x8000002c, now 0x80000034. Handler instret/time now 13/17.

Historical author ownership is explicit: 41 captures stay exact; env-irq-sources
is a fresh parcel record with fixed author budget 13. --check-owned still checks
42 inputs. Both branches refuse count/write/comment/line-ending drift; new
wrong-budget and word-route mutants fail before their two GUEST-GEN registrations.

Fresh public Sail attempts: w-sw agrees (19 steps, two identical traces); six
inputs diverge at declared timer/wait observations, and w-notrap/w-timer processes
refuse rc1 after disabled counter reads and trap loops. Old inputs reproduce the
process refusals. The older timer diagnostic left STCE clear and therefore
confounded its laboratory result with the known overlay defect. Repaired here:
ten boundaries, explicit enable and bit-63 read-back on both independent sides.
It still observes Sail STIP=0 at both reads, versus laboratory 1; traces repeat
exactly. Removing enable makes its read-back guard refuse. Public config rejects
Zicntr without a time source and CLINT without a region. No submodule internals
are used; remove the maintained implementation-specific symbol from the book.

First full CI passed Rust 163/17/198 but refused a stale GS digest; regenerate
before final CI. Final make ci passes all five legs; Rust 163/17/198, registry
4/0, schema270/two skips, freeze3/zero findings and gate controls17/0.
Current docs also correct an old 64-check summary to verified 68.
No architectural fallback repair or new contract credit in this prerequisite.
Next c13a2 dynamic STIP/author/state/v2 supersession, then c13b direct S witnesses.
Promotion declined: the current owned-record protocol and worked timer example
are maintained in tracked author diagnostics and the runtime book.


Earlier entries: [history manifest](docs/changelog/SHARDS.sha256).

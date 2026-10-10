# DEV_NOTES shard — _(2026-10-10)_ … _(2026-10-10)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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


Earlier entries: [history manifest](docs/changelog/SHARDS.sha256).

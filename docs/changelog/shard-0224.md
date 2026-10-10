# DEV_NOTES shard — _(2026-10-10)_ … _(2026-10-10)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

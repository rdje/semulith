# DEV_NOTES shard — _(2026-10-10)_ … _(2026-10-10)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-10)_ — observe FENCE fields and preservation (P4-SYSTEM.13 c25)

Authenticated RV32I1.1.7 requires reserved-config acceptance and ignored rs1/rd.
Direct matrix4096 configs × three modes × five register pairs=61440 boundaries,
plus three LR.D/FENCE/SC.D/LD and three translated ADDI/FENCE/ADDI programs.
Full GPR/FPR/26 CSR owner/PC/mode/memory and exact requests preserve reservations
and warm mappings. Direct61461/122922/122934requests; companions39/78 yield
pair61500/123000. POS ordinary/TSO; NEG adversarial accepted forms, not traps.

Ten wrong tables reject; initial mask-control reason was corrected with public
step_over diagnosis: ReservedDecode advances time but not retirement, so CSR
counter comparison fails before final outcome. Actual disabled-GPR observer RED
rc=101, restored; missing-binding RED rc=101 before two Execution entries.
Small provenance defect owned/fixed: STOCK fence's1.1.6 locator introduced by
022f557 points at Load/Store, correct Memory Ordering is1.1.7. Exact one-line
source delta; canonical fault-fence already correct. Independent all61440 words/
full states and six integration programs rc=0; author omits nine data requests,
which public CPU observer judges separately. No architectural defect found.

verify.py rc=0: prior96 entries/112 base+348 GC input/core/generated/frozen bytes
exact; all scripts/author bytes exact except locator. Full167/5365/10524 unchanged.
make check rc=0, Rust167/17/214. Registry98/effective96/114, nine pairs/freeze.
LIVE unchanged652 arms/49 chapters/P4 12/18. Focused gates/all six books rc=0; hooks next.
promotion: declined (finite matrix, masks' retirement distinction and author-log
limits retained in worked memory chapter/tree). c26a task containment next.

## _(2026-10-10)_ — observe implicit Sv39 requests and no-write faults (P4-SYSTEM.13 c24)

Bind WALK-IMPLICIT with 20 actual CPU cases: nine Fetch/LD/SD × one/two/three
levels, two boundaries each; eleven Svade/invalid/refused/noncanonical faults.
Direct total29 boundaries/50 parcels/104 requests. Literal physical paths and
full GPR/PC/mode/status/satp/trap/counters/memory precede CPU execution. Exact
requests distinguish walks, parcels and explicit data; second access hits the
same-page cache. Faults leave all PTE bytes unchanged and stop before data.
Existing three-level CPU boundary/core tests remain; this binds the missing pair.

Seven corrupted-capture controls reject; actual disabled-request observer RED
rc=101. Actual walker Load+D/Response::Load and write-A-before-fault mutations
both RED rc=101 at request predicate, then core bytes restored. Missing-binding
RED rc=101 precedes two Execution entries. Successful walk-as-Load paths
retain state/memory with request guard disabled, rc=0; all-case state-only probe
correctly RED rc=101 because Walk-only refusal is bypassed. Write-A with request
guard disabled still memory-RED rc=101; with request+memory guards disabled,
original trap/state GREEN rc=0. Final restored make check rc=0. Authenticated supervisor/introduction
sources; independent20-case word/path/state/memory/fetch-walk proof rc=0. Author
omits explicit data logs; public observer verifies those. Companions188/376 POS,
255/510 NEG plus direct29/50 yield472/936.

verify.py rc=0: prior94 bindings,112 base/348 GC inputs/core/author/generated/
frozen bytes exact; full167/5365/10524 unchanged. make check rc=0, Rust167/17/212.
Registry96/effective94/114 (13 scope/23 guest/6 boundary/5 execution pairs), ten
runtime pairs/freeze. LIVE unchanged652 arms/49 chapters/P4 12/18. Focused gates/
all six books rc=0. Hooks precede c25. promotion: declined (finite matrix and independent-log limits
retained in worked runtime chapter and tree). c25 FENCE follows clean workflow.

## _(2026-10-10)_ — retain 64-bit user registers and addresses (P4-SYSTEM.13 c23b)

Authenticated RV64I3.1.1 fixes XLEN=64; Sv39 keeps its canonical subset. Two
four-word U/Sv39 programs start at VA 0x100001000/0xffffffff80001000 and map to
PA0x80001000 through one A/D-set user 1GiB leaf each. ADDI retains a high pointer,
LD/SD retain all payload bits, AUIPC retains virtual PC. Literal high-bit sentinels
precede register writes. All GPRs/PC/U/UXL/trap/counters/memory and actual requests
are observed: two cases/eight boundaries/16 parcels/22 total requests.

Seven isolated public effects narrow ADDI/LD/SD/AUIPC/next-PC values or addresses;
all 14 case/control combinations fail. Actual disabled-GPR auditor lets unused
x7 truncation escape (meaningful RED rc=101); restored. Declaration missing-
binding RED rc=101 precedes two Execution entries. Successful walk-as-Load paths
retain state/memory with request guard disabled, rc=0; all-case state-only probe
correctly RED rc=101 because Walk-only refusal is bypassed. Write-A with request
guard disabled still memory-RED rc=101; with request+memory guards disabled,
original trap/state GREEN rc=0. Final restored make check rc=0. Independent author matches
words/PTEs/canonical mappings/GPR/PC/U/memory and fetch/walk logs; it does not
log data requests, which the public CPU observer separately verifies.

verify.py rc=0: prior 92 entries/all 112 base+348 GC input/core/author/generated/
frozen bytes exact; normal full 167/5365/10524 unchanged. Companions 31/62 POS,
89/178 NEG plus direct 8/16 yield pair 128/256. make check rc=0 (Rust 167/17/210).
Registry 94/effective 92/114; eleven runtime pairs/freeze. LIVE_STATUS unchanged
(652 arms,49 chapters,P4 12/18). Focused gates/all six books rc=0; hooks precede
c24 WALK-IMPLICIT. promotion: declined (finite virtual-width/physical-request
separation and author-log limits retained in worked book matrix and owning tree).

## _(2026-10-10)_ — preserve control-transfer witnesses in a bounded chapter (P4-SYSTEM.13 c23a)

Integer runtime chapter reached 31,694/32,768 B (1,074 B room). Move its whole
ordered suffix (immediate transfers, JALR diagnosis and realization) into
contract-control.md, preserving the leading separator and all 9,822 B:
SHA256 d1da14f93bf6f352739edd2a2e784cabd4f782481fb729bc67c2b1fc05b819c0.
Remove only the new navigation/header to reconstruct the original 31,694 B:
SHA256 9beabe26eafc6b026ab8310cddf25f3ca97919ce5787e89536725a62149c7a7b.
Integer/control now 21,969/10,013 B. SUMMARY/index/profile ENV/GS/runtime summary
follow the move; book count 48→49, fixed caps unchanged.

verify.py rc=0 proves inverse, all 92 registry/core/author/generated/frozen bytes
and 112 base/348 GC canonical/guest inputs exact. Explicit new-file census 51
under 80 files/524,288 family bytes/32,768 part caps. Effective90/114 unchanged;
no Rust code changed. LIVE_STATUS changes only book chapters 48→49, doctrine 652
arms/P4 12/18 unchanged. Focused gates/all six books rc=0; hooks precede then c23b
XLEN and remaining runtime pairs/freeze. promotion: declined (existing bounded
suffix-move protocol; exact inverse and ownership retained in tree/book navigation).


Earlier completed entries: [docs/changelog/shard-0226.md](docs/changelog/shard-0226.md); its frozen manifest records the exact payload.

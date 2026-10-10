# Gaps and laboratory choices

The specifications deliberately leave choices; the model also has uncompleted
evidence. Those are different facts. `materials/category-needs.sexp` enumerates
C01–C24 for this unit. The required subset contains C01–C07, C09–C17 and C22–C24.
Required `partial` rows name a bounded choice or outstanding evidence; registration
never turns partial collection into accepted semantics. V is out of scope;
C19/C21 platform composition and external events are deferred. C18 distinguishes
base counters and laboratory observations from excluded architectural debug.
C20 has acquired LP64D/SBI materials but no firmware/boot acceptance.

## Worked choices

**Svade:** a valid translation requiring an A or D update faults instead of
modifying the PTE. This is a selected architecture option, sourced in the pinned
Supervisor revision. The FU540 precedent supports the choice, not a hardware
validation claim. An observer should check trap cause/address, saved start PC,
unchanged PTE and the actual walk path; a final GPR alone cannot establish them.

**Code visibility:** this laboratory re-fetches instructions from coherent RAM.
A store can become visible without FENCE.I; executing FENCE.I remains legal and
fulfills the selected synchronization contract. The no-fence case is a policy
control, not proof of every permitted cache implementation. SFENCE.VMA separately
invalidates selected translation state; instruction visibility is not translation
visibility.

**Reservation/SC:** the chosen reservation matches physical address and width,
with no spurious completed failure. A nonmatching SC still obtains physical store
permission after translation; a target refusal traps without a data store.
Physical aliases can match; equal virtual addresses with changed translations
need not. These choices require their own history and permission witnesses and
do not establish multicore eventual progress.

**Time and wait:** virtual time is a declared laboratory input; counter gates,
stimecmp/STCE and ACTIVE/WAITING affect observations. The matched public Sail
configuration has named timer/wait differences. A platform mismatch must remain
named, rather than adding an undeclared device to force equality.

**FP:** target bits, flags, rounding, boxing and traps are observed through the
qualified Rust backend and exact expected-result methods. A comparator's matching
bits do not authenticate its implementation ancestry. Independently derived
arithmetic fixtures must state their own producer and shared inputs.

## Remaining research and engineering

REQ-D-ECALL-EBREAK retains its partial OQ-5 disposition. Historical mirrored
requirements and supersessions need mechanical reconciliation; requirement
statuses remain unpromoted. Structured matched experiments, controls, producer
relationships and prospective policy adequacy remain .14 work. Full external,
workload and validator-mutation regression is .15; GC snapshot/replay/reduction
is .16; host/portable qualification is .17; release decision is .18.

The scalar laboratory already has operational snapshot/replay facilities. Their
existence does not remove the explicit GC CLI refusals. Likewise the netboard's
devices are separately registered units; they do not become this processor's
platform simply because the directories coexist.

# P4.6 — Instruction visibility and fence semantics

**Status:** Landed and closed (a–c, 2026-10-05)

The design brief (fence.i the declared nop on an always-coherent engine; the
bind miniaturized to one form) executes in three checkpoints. Slice (a):
the slot's payload is pinned and authored. `rv_zifencei` lands through the tracked
`extensions/` fetch
route — 73 bytes, exactly one row — with the fetch leg's named exclusion keeping
the census at 87 until the bind. The generated fragment owns no fields (imm12/rs1/rd
are the base's, decoded-and-ignored per the shall-ignore rule), and `zifencei.sem.sexp`
states the declared nop with every normative sentence located (the
coherent/uncached-RAM latitude meets a re-read-per-fetch machine). One brief
claim measured false: the operand list refused the standard-software spelling —
the assembler gains a named zero-operand acceptance. No Sem variant, no
generator change — the one-form nop lowers over the existing machinery.

Slice (b): THE BIND. The slot becomes the extension and fence.i is legal — the
census grows 87 → 88, the generated definition gains the row over the existing
nop, and the requirement pair lands with no new decision record. The two fencei guests re-derive exactly as
pre-committed: the delivery is gone, and the marker that proved
it now commits — x2 ← 7, as on both references. The acceptance pair
stands — with the synchronization (fencei-selfmod) and without
(fault-selfmod, immediate visibility by declared choice) — with the
reserved-fields word ignored end-to-end. The corpus reads 101/101,
98 pre-bind guests byte-identical.

Slice (c): the matched experiment and the leaf's acceptance. The chapter's
contract is three sentences (stores to instruction memory are not guaranteed
visible until a FENCE.I; the fence orders the accesses before it ahead of the
fetches after it) — and
both engines land on the same reading: the laboratory's re-read-per-fetch
makes the fence a nop by construction, and Sail's FENCEI is "a nop for the
memory model" with its fields decoded-not-fixed. Against the matched
configuration (validate-config clean), all six fence.i guests AGREE
step-for-step, 29 steps, the patched fetch reading 7. The criterion closes on
the pair: WITH the synchronization (fencei-selfmod's fence.i executed and legal
between the store and the patched fetch, on both engines) and WITHOUT
(fault-selfmod, immediate visibility as the declared subset). The goal's other
half — when stale state MAY persist — is a declared latitude, not a fixture:
modelling a forever-caching hart would contradict the always-coherent census
(rejected at the brief). The reserved-fields word executes on both sides.

## Direct contract observations

P4.13 c28d binds OB-GC-FENCEI's two checks to direct CPU execution plus the
unchanged fencei-selfmod, fault-selfmod and fencei-reserved guests. The pinned
RVI-ZIFENCEI 4.1 page is authenticated before deriving values: 32,380 bytes,
SHA-256 4026de34713f4b898595eb4a17bb58176a0e2905196705a904d3d8fab4432a91.
Its forward-compatibility rule requires ignoring funct12, rs1 and rd. Its coherent/
uncached-memory latitude permits this laboratory's no-op implementation; immediate
visibility without the fence remains the explicitly stronger laboratory choice.
No reference implementation assumption is used by these witnesses.

The field matrix executes all 4,096 funct12 values with five representative
rs1/rd pairs: 0/0, 0/31, 31/0, 31/31 and 7/13. Crossing M/S/U gives 61,440
boundaries. The standard all-zero-fields encoding supplies three positive cells;
the remaining 61,437 negative cells require normal execution of ignored fields,
rather than an illegal-instruction trap. For example, 0xffff9f8f has funct12=4095,
rs1=x31 and rd=x31, yet still retires as FENCE.I.

Each cell observes the complete GPR/FPR files, all 26 CSR storage owners, memory,
PC/mode, reservation, full TLB including replacement cursor, wait state, boundary
outcome and exact request list. The seeded TLB contains local/global entries with
a nonzero FIFO cursor; the reservation is valid and wait state Active. FENCE.I
preserves them. Its only progress is PC+4, mcycle 41→42 and minstret 17→18, with
two FetchParcel requests and no data/walk requests. The tests cover all immediate
values and the stated five register pairs, not every possible register pairing.

The visibility programs patch actual instruction bytes. There are 36 programs:
32-bit ADDI versus C.LI target, entry at 0 or 2 modulo 4, M/S/U, and standard
FENCE.I, nonzero-fields FENCE.I or a no-fence NOP control. All have five boundaries:

| Boundary | Operation | Required observation |
| --- | --- | --- |
| 0 | SH patches the future target | exactly two bytes change; one halfword Store |
| 1 | FENCE.I or control NOP | state preserved apart from ordinary progress |
| 2 | LHU reads the patched halfword | x10 receives the written value; one halfword Load |
| 3 | ADDI x7,x0,1 | x7 becomes 1 |
| 4 | fetch and execute the target | x8 becomes 7 from the patched bytes |

For a word target at 0x1010, the initial ADDI x8,x0,2 is 0x00200413.
SH writes 0x0070 at 0x1012, changing only its high halfword. The later fetch
reads 0x00700413, ADDI x8,x0,7; LHU already read back 0x0070. For a compressed
target, SH replaces C.LI x8,2 (0x4409) with C.LI x8,7 (0x441d), and the target
needs only one parcel. Halfword stores remain naturally aligned even when the
32-bit target starts at 2 modulo 4. The source register and target address are
seeded before execution, independently of the tested instruction sequence.

The standard and nonzero fences give the same result. Replacing the fence with
ADDI x0,x0,0 also sees the changed bytes under this coherent provider. This does
not require a caching implementation to expose stores before FENCE.I, and it
does not prove arbitrary providers coherent. The separate ordering-assumption
auditor retains its discarded-store and stale-parcel controls.

Direct totals are 61,620 boundaries, 123,222 parcels and 123,294 requests. The
unchanged companions contribute 17 boundaries/34 parcels, giving the pair
61,637/123,256. Independent derivation checks all field-state results, program
words/lengths, patched values and parcel logs. Its log omits the 72 explicit
SH/LHU requests; the direct CPU observer owns those checks and complete retained
reservation/TLB fields. The literal expectations precede CPU execution.

Eleven wrong public instruction tables reject tightened ignored-bit masks,
GPR/FPR/CSR writes, extra load/store, trap, PC skip, reservation consumption and
TLB invalidation. Sixteen corrupted captures exercise every observation family,
including a cursor-only TLB change whose mappings remain identical. Disabling
the actual request predicate lets a state-equivalent extra load through and
fails the control. Temporarily admitting FENCE.I into the actual WFI-word
condition fails the wait-state observation. Both mutations restore exactly;
production CPU semantics remain unchanged.

The completeness test first fails the missing CHK-GC-FENCEI-POS entry, then
passes after two Execution bindings. Registry size becomes 102, effective
G-CONTRACT 100/114. Seven runtime pairs and final v2 freeze remain. Structured
experiment records and requirement statuses remain P4.14's work.

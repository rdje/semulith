# P4.13 — Completing the environment contract

**Status:** Census, state inventory and seven executable scope pairs landed; version 2 remains open.

The complete instruction set now runs, including multiply/divide and compressed
instructions. Its contract still contains declarations inherited from earlier
stages. This work checks every effective obligation, fills the remaining boundary
assumptions, and realizes each declared check before freezing version 2.

The census finds 53 effective obligations and 106 checks. Thirty-four checks currently
run through the unit's registry. A check will receive credit only when its actual
fixture runs: instruction guarantees use executable observations; a scope choice
such as the selected firmware ABI uses a predicate over the canonical documents
and a negative fixture that violates that predicate. Running an unrelated program
cannot establish a scope declaration.

Five boundary topics remain: address units, access widths and memory attributes,
event delivery, ordering, and reset. The scalar profile's assumptions cannot be
copied unchanged. For example, this processor can take interrupts, fetches exact
16-bit parcels, selects RVWMO, and resets floating-point, translation-cache,
reservation and wait state as well as integer registers and CSRs. Time, parcel
fetch and partial progress already have GC-specific records.

Some inherited statements need replacements. Two describe obsolete definition
stages; another describes the earlier floating-point qualification condition.
The fault-priority statement also needs more precise language: address triggers
are absent, while EBREAK and C.EBREAK still raise environment-break exceptions
with cause 3. The pinned priority table distinguishes these cases.

Versioning preserves the record. Frozen version-0 and version-1 statements and
their hashes stay unchanged; version 2 names each replacement and why it replaces
the old statement. The complete per-obligation plan is in the active task tree's
`.13` census. Completion requires every effective check to run, the state census
to describe the actual complete state, and version 2 to be frozen. Until then,
G-CONTRACT and CPU-SYSTEM remain incomplete.

## Complete state inventory

The state census now describes the whole selected laboratory profile. Its twelve
candidates are answered, and its consequence names every state owner:

| State | What must be retained for exact continuation |
| --- | --- |
| Integer registers and control | x1–x31, PC and current privilege mode; x0 is constant |
| Floating point | f0–f31, each 64 bits |
| CSRs | 26 storage owners behind 33 named CSRs |
| Memory | The laboratory's main-memory bytes |
| Translation cache | Four TLB entries and the FIFO replacement position |
| Reservation | Physical address, width and validity |
| Waiting | ACTIVE or WAITING |

CSR aliases add no storage. For example, `time` and `cycle` view `mcycle`, and
`fcsr` combines `fflags` and `frm`. The virtual clock is already part of those
owners; this laboratory has no external timer or interrupt-controller state.
Cold reset constructs all owners anew. Exact continuation must also preserve
the current TLB replacement position, reservation and wait state: cold reset is
not a substitute for restoring them.

This correction changes the declared inventory and its generated metadata.
The definition module also records the updated state-source hash in its
provenance manifest. Storage, reset values, accessors and execution remain
byte-identical. Snapshot
and replay serialization still belong to P4.16; this inventory does not claim
that those features are implemented.

## Executable scope checks

The registry now distinguishes guest evidence from scope evidence. Its normal
Rust tests run every entry. The first scope pair checks the composition selection:
RV64I with 64-bit registers, the exact selected extension set, its nine encoding
fragments, and a complete composition.

The negative check first requires the real declarations to pass, then changes six
independent copies: remove C, add H, change XLEN, leave C unbound, change the base
fragment, or mark the composition partial. Each copy must fail for its specific
reason. Further controls deliberately disable each predicate family; the negative
check must then fail. Unknown check ids are refused. All copies stay in memory.

This adds two real checks without running an unrelated program as evidence of
selection. All twenty earlier guest bindings stay unchanged. The effective
contract reached 22 of 106 checks at that slice. The following structured
scope checks raise it to 34; version 2 remains open.

## Structured scope and identity

Six more scope pairs validate the extension dependencies, privilege-source
revision, CSR inventory, PMP and hypervisor exclusions, and equality between the
profile's instruction names and the resolved encoding. Their 17 violating copies
must each fail for a specific reason. Two examples show why a count or an agreement
between files is insufficient:

- Removing `fcsr` from both the profile and state lists leaves them agreeing, but
  violates the independently stated committed CSR selection.
- Replacing one C instruction name with an unknown name leaves the count intact,
  but violates equality with the composed encoding.

The privilege check also binds the declared version to exact source identities.
A different well-formed digest fails. The two public pages were rehashed when
these expectations were recorded; the ordinary scope check needs no artifact
cache and makes no fresh artifact-byte verification claim.

The seven scope pairs plus the twenty existing guest checks now realize 34 of
106 checks. These are selection and consistency checks. CSR field behavior and
instruction semantics retain their execution evidence; firmware is still future
work. Older notes and changelog entries were archived verbatim with exact
reconstruction, so their history remains available within the fixed size limits.

## Enforcing the guest toolchain

Before realizing the ABI scope, review found that the legacy C build printed
its tool versions without enforcing them. An isolated reproduction accepted
version-99 compiler and linker stand-ins. ACT4's duplicated discovery also crashed
when an explicit compiler was missing. Both callers now use the same resolver.

The resolver validates clang/LLD 21.1.8, Zig 0.16.0 when used as the linker driver,
and ACT4's LLVM 21.1.8 symbol reader. It checks these identities before writing a
backend probe. An explicit override that is missing, has the wrong version, or
cannot compile RV64I is refused; no fallback bypasses that override. For example:

```bash
bash scripts/build_c_guest.sh c-scope
SEMULITH_RISCV_CLANG=tools/clang bash scripts/build_c_guest.sh c-scope
```

The second command succeeds only when `tools/clang` exists and satisfies the
same pin and backend requirements. Probe files remain under the repository's
output directory and are cleaned on either outcome. Twenty isolated controls
cover both callers and refusal paths; disabling identity checking makes the
controls fail. The installed pinned tools still build the exact same C ELF.
That guest uses RV64I/LP64; the selected GC LP64D ABI still needs its own scope
checks, and firmware implementation remains later work.

# The complete materials bill

The unit pins the RISC-V Ratified Specifications Library revision named in the
ledger, not an interchangeable GitHub PDF or a newer live page. The HTML locators
refer to that publication's numbering. Cached PDF pins use HTTP0 as an explicit
cache-artifact declaration; it does not mean a successful web acquisition. At
registration all24 source artifacts were authenticated against their unchanged
hashes and byte lengths through the public cache routes. Acquisition grants no
reuse terms, independence or conformance credit; release-time terms recording
remains an owned dossier question. One licensed DIV statement has a scoped
retention decision in `materials/RVI_M_RETENTION.md`; see the
[capture plan](capture-plan.md#retain-licensed-text-with-its-own-identity).

## Pinned specifications

{{#include materials/pinned-specifications.md}}

The table and ledger supply exact identities. Each section below states the
role in this selected processor and the boundary of that role.

### RVI-INTRO

The execution-environment boundary, hart and trap vocabulary make assumptions explicit.

**Does not supply:** a memory map, reset vector, operating system or deterministic harness policy.

### RVI-RV32I

The base register, instruction, control-flow and memory rules underlie the RV64 composition.

**Does not supply:** the RV64 width deltas, compressed decoding or privileged trap routing.

### RVI-RV64I

XLEN64, W operations, wider shifts and LD/SD/LWU supply the RV64 deltas.

**Does not supply:** the inherited base rules by itself, or any M/A/F/D/C extension.

### RVI-NAMING

The G abbreviation and canonical extension ordering constrain the selected ISA identity.

**Does not supply:** a complete Linux platform, timer, page-table policy or evidence of implementation.

### RVI-G-LISTING

The instruction listings and opcode map provide a scope cross-check.

**Does not supply:** all instruction semantics, field legalization or a qualified decoder.

### RVI-M

Multiply/divide rules specify high halves, signed overflow and division by zero.

**Does not supply:** host arithmetic permission to trap or independent expected-result provenance.

### RVI-A

LR/SC, AMOs and ordering annotations define the atomic surface and permitted reservation latitude.

**Does not supply:** a unique reservation policy, all multicore outcomes or a proof of progress for this one-hart model.

### RVI-F

Single-precision operations, flags, rounding and FP CSR dependencies specify target behavior.

**Does not supply:** an implementation backend, authenticated comparator ancestry or sufficient numeric qualification.

### RVI-D

Double-precision operations, FLEN64 and NaN boxing extend F with explicit dependencies.

**Does not supply:** a native-host float fallback or universal acceptance from a few matching values.

### RVI-C

Compressed encodings and expansion rules change instruction lengths and alignment.

**Does not supply:** permission to fetch an unnecessary second parcel or assume every reserved parcel is legal.

### RVI-ZC

The decomposition selects Zca and Zcd at RV64 with D; the RV32-only Zcf leg is excluded.

**Does not supply:** selection of every Zc extension or extra instructions merely because the chapter names them.

### RVI-ZICSR

The six CSR instruction forms define source/destination suppression and access effects.

**Does not supply:** every CSR address, every privileged field mask or authorization to bypass privilege gates.

### RVI-ZIFENCEI

Instruction-fetch synchronization defines the obligation for newly stored code.

**Does not supply:** a mandatory instruction cache or cache timing; immediate coherent visibility is an explicit laboratory choice.

### RVI-ZICNTR

The base cycle/time/instret views and access discipline supply selected counter rules.

**Does not supply:** a physical time source, a cycle-accurate CPU, or selection of Zihpm merely because the chapter describes it.

### RVI-RVWMO

The architectural memory model constrains ordered and atomic observations.

**Does not supply:** evidence for weak multicore executions, coherency or fairness from a sequential one-hart run.

### RVP-INTRO

The privileged architecture establishes mode responsibilities and the platform boundary.

**Does not supply:** an implemented supervisor, device controller or boot chain.

### RVP-CSR

CSR address conventions and WPRI/WARL/WLRL rules structure the declared state census.

**Does not supply:** one universal field implementation or all optional CSRs.

### RVP-MACHINE

Machine traps, delegation, return, WFI and selected control fields provide privileged rules.

**Does not supply:** selected PMP support, a reset platform or every optional machine extension.

### RVP-SUPERVISOR

Supervisor control, Sv39 walks, permissions, invalidation and inline Svade constrain translation.

**Does not supply:** selection of Sv48/Sv57 or automatic PTE A/D updates; the profile deliberately chooses faulting Svade.

### RVP-INSNS

The privileged instruction listing cross-checks mret/sret/wfi/sfence.vma encoding scope.

**Does not supply:** their entire behavioral contract or permission to treat a historical no-op description as current.

### RVP-SSTC

stimecmp and menvcfg.STCE define the supervisor timer interface and gating.

**Does not supply:** a CLINT, PLIC, physical clock or matching public-reference time source.

### RVI-PSABI

The ratified psABI defines LP64D calling conventions and ABI_FLEN64.

**Does not supply:** a compiler, executable loader, C library, syscall implementation or successful workload execution.

### RVI-SBI

The ratified SBI2.0 specification defines the intended M-mode firmware interface.

**Does not supply:** implemented firmware, a board memory map, kernel compatibility or a host-modeled replacement service.

### SIFIVE-FU540-C000

The U54 Bare/Sv39 and faulting A/D behavior provides an implementation precedent for selection.

**Does not supply:** this processor identity, hardware validation, a FU540 board model or authority to import every SoC feature.

## Encoding artifacts

{{#include materials/encoding-tables.md}}

### RISCV-OPCODES

The exact selected files provide fixed bits, operand positions, CSR addresses,
field masks and trap numbers used by the canonical definition. Base and extension
fragments retain their own source identities. The assembler follows these
published tables; using its output does not make guest encodings independent of
the decoder's inputs. A literal parcel/fetch witness and a deliberately corrupted
expected result test different risks from merely re-encoding the same mnemonic.

**Does not supply:** instruction semantics, a complete source license review,
authenticated Sail/Spike implementation ancestry, or an independent numeric oracle.

## Reference candidates

{{#include materials/reference-models.md}}

### sail-riscv

The pinned public model, public configuration validator, matched override and
tracked adapter provide a finite second execution opinion. The generated table
retains the exact configuration and recorded historical differences. A repeatable
GPR change trace establishes only those changes and witnessed delivery gaps;
full PCs, FP state, memory, CSRs and requests require their own observations.

**Does not supply:** authenticated implementation ancestry, independent floating-
point numeric evidence, a matching timer/injected physical-failure environment,
or structured requalification records simply because prose records earlier runs.

### spike

The reference dossier pins the candidate and records its investigation limits.
It is a candidate, not an automatic second accepted comparator. A usable route
needs a declared configuration, producer, observations, repeat and discriminating
controls under the current policy. No new Spike run is claimed by registration.

**Does not supply:** a matched GC experiment here, lineage independence or
additional acceptance credit from candidate availability.

## Internal contracts

{{#include materials/internal-contracts.md}}

The generated counts enumerate declared files/records. In particular, the
obligation catalogue includes historical v0/v1/v2 records. Effective membership,
supersession, realized checks and frozen state are computed separately by the
[processor gate](evidence.md). Raw catalogue checks are not that denominator.

### profile.sexp

The profile selects exact features, decisions, sources and laboratory authority.
The selection is input to composed generation and scope validation.

**Does not supply:** evidence that every decision is implemented or qualified;
requirements may include additional records beyond one decision mirror.

### state.sexp

The state census declares architectural views, storage owners, aliases, reset,
legalization and hidden-state candidates. Views do not create extra stored state.

**Does not supply:** GC snapshot serialization, replay compatibility or evidence
that every legal transition preserves all owners.

### encoding.sexp

The composition names the base and selected extensions with their canonical
fragments and sources. Scope and definition gates check the declared composition.

**Does not supply:** correctness of every semantic effect or independence from
an assembler using the same canonical input tables.

### requirements.sexp

The requirement catalogue records source meaning, risk, status and verbatim
mirrors. RECORD-SCHEMA checks declared mirrors; evidence policy decides what a
future status derivation must require.

**Does not supply:** implementation credit from a typed status, resolved research
from an unresolved source question, or automatic grandfathering of earlier runs.

### contract-obligations.sexp

The included versioned catalogue declares assumptions/guarantees and their
positive/negative checks. contract.sexp owns version membership and supersession;
CONTRACT-FREEZE authenticates frozen records. The registry owns executable bindings.

**Does not supply:** proof that a binding observes all claimed effects, a full
processor verdict, or permission to rewrite an earlier frozen record in place.

### guests/

Canonical programs and source-derived expectations exercise selected instruction
and boundary behavior. Examples include page-end C fetch, x0 loads, CSR legality,
Svade faults and traps delivered to handlers. The guest comparison's observed
fields must be named before drawing a conclusion.

**Does not supply:** exhaustive architecture coverage, independent encoding
provenance, structured experiment records or full-state evidence from a GPR-only
comparison. Direct contract observers address additional named properties.

### interactions.sexp

The declared matrix assigns fault, alias, boundary, event, progress and restart
cells a guest, mechanism or explicit degenerate argument. A resolving disposition
is a graph-integrity fact with a finite scope.

**Does not supply:** execution of every cross-product, multicore progress, missing
external suites, replay or portability qualification.

# Processor Information Catalog — v0.2

Version: 0.2 | 2026-09-13


This is a collection checklist. Not every target implements every category. Each category needs an explicit applicability decision and evidence, rather than an invented default.

## 1 Identity, state, and instruction semantics

| ID | Category | Information to collect | Representative validation question |
|---|---|---|---|
| C01 | Identity and configuration | Architecture revision, extension versions, feature dependencies, core parameters, identification registers, selectable implementation choices, errata applicability | Does feature discovery describe exactly the enabled semantics? |
| C02 | Architectural and persistent state | Registers, widths, banks, aliases, overlaps, special registers, condition state, stacks, loop state, accumulators, reset values, retained state, hidden state affecting future behavior | Does writing one alias correctly affect every other view? |
| C03 | Fetch and encoding | Instruction lengths, alignment, encodings, prefixes, modes, fetch-unit organization, packet boundaries, decode priority, reserved encodings, fetch permissions, faults across boundaries | Can decode fail or fault at the correct point without fetching extra bytes observably? |
| C04 | Basic execution semantics | Preconditions, explicit and implicit operands, bit-exact operations, signedness, flag effects, PC rules, destinations, suppressed writes, exception ordering | Are both the result and every side effect correct at boundary values? |
| C05 | Control flow | Branches, calls, returns, delay slots, link values, indirect-target rules, instruction-state changes, predication, hardware loops, repeat instructions, interruptibility | Does execution resume at the right place after an interrupted loop or delayed branch? |
| C06 | Integer and fixed-point numerics | Width of each intermediate, truncation, sign/zero extension, carry and borrow, overflow, saturation, fractional scaling, guard bits, rounding, shifts, division corner cases, decimal/BCD formats when present | At which precise operation does rounding or saturation occur? |
| C07 | Floating-point numerics | Encodings and formats, supported operations, rounding modes, NaNs and payload policy, infinities, signed zero, subnormals, flush modes, exception flags and traps, fused operations, conversions, approximate-instruction guarantees | Does a NaN, underflow, or conversion produce the target result and status rather than the host default? |
| C08 | SIMD, vectors, and specialized compute | Lane mapping, widths, masks, inactive/tail behavior, widening/narrowing, reductions and their order, register grouping, vector length, restart state, gather/scatter, matrix/tensor state when present | What happens to completed lanes when a later lane faults? |
| C09 | Issue groups and exposed sequencing | Packet membership, old/new operand visibility, forwarding, functional-unit legality where architectural, delayed completion, conflict rules, interlocks, explicit no-ops, multi-step instructions | Can two operations be executed in host source order without changing guest results? |

## 2 Memory, protection, events, and concurrency

| ID | Category | Information to collect | Representative validation question |
|---|---|---|---|
| C10 | Addressing and storage organization | Address widths and units, address spaces, instruction/data separation, byte/word packing, endianness by access type, bank selection, address arithmetic, circular/modulo and bit-reversed modes, alignment and wraparound | Does an address increment mean one octet, one word, or another target unit? |
| C11 | Memory access and fault semantics | Access widths, alignment policy, atomicity, split accesses, ordering of subaccesses, memory attributes, access permissions, fault priorities, partial writes, access side effects | Can a failing access already have modified memory or a device? |
| C12 | Translation and protection | MMU/MPU, page-table formats, walk ordering, permissions, privilege checks, address tags/capabilities where present, accessed/dirty updates, address-space identifiers, translation invalidation, nested translation | Does permission failure produce the correct fault and permitted page-table side effects? |
| C13 | Cache and instruction visibility | Architecturally required maintenance, instruction/data visibility, synchronization, noncoherent regions, DMA visibility, stale translations and code, memory types | When must newly written code become executable, and when may stale state persist? |
| C14 | Exceptions and interrupts | Sources, routing, priority, masks, pending/active state, precise/imprecise behavior, saved state, nesting, return, delivery boundaries, level/edge behavior, reset precedence | What happens if an exception and external interrupt are both eligible? |
| C15 | Privilege and execution modes | Mode transitions, control-register permissions, secure states where present, virtualization controls, trap interception, context state, mode-dependent decoding | Does the same instruction trap or act differently in each supported mode? |
| C16 | Atomic and multicore behavior | Memory-consistency rules, barriers, atomic widths, reservations, failed conditional stores, coherency obligations, mixed-size accesses, topology, forward progress, heterogeneous cores | Is an observed load value legal under the selected architecture's memory model? |
| C17 | Reset, idle, power, and time | Reset classes and sequences, initial state, retained state, halt/wait/wake, timers, counter widths and rollover, counter enable rules, clock-domain relationships, asynchronous progress | Can a halted core still receive the event that wakes it? |
| C18 | Debug and implementation observation | Breakpoints, watchpoints, single stepping, debug entry/exit, trace, performance counters, feature probes, implementation-defined control fields | Which observations are promised, and which are explicitly unavailable? |

## 3 The machine and its software environment

| ID | Category | Information to collect | Representative validation question |
|---|---|---|---|
| C19 | Platform, devices, and interconnect | Memory map, RAM/ROM behavior, MMIO or port I/O, device register semantics, DMA, interrupt controllers, timers, mailboxes, boot media, device discovery, accelerator interfaces | Does the actual firmware find and interact with the devices it expects? |
| C20 | Program and system environment | Executable format, load addresses, entry state, linker conventions, ABI, startup firmware, system calls, semihosting, firmware interfaces, libraries, debugger conventions | Is the failure a CPU-semantic error or a missing environment service? |
| C21 | External inputs and interaction | Device input traces, asynchronous arrival, reset/interrupt injection, clock sources, random/entropy inputs, coprocessor events, co-simulation scheduling | Can the same external experiment be replayed without accidental host-dependent behavior? |

## 4 Specification meaning, evidence, and operations

| ID | Category | Information to collect | Representative validation question |
|---|---|---|---|
| C22 | Specification status and unresolved behavior | Normative rules, implementation-defined and unspecified choices, undefined behavior, constrained-unpredictable cases, reserved fields, contradictions, errata, missing dependencies | Is an unknown fact in our research being confused with a choice the architecture permits? |
| C23 | Provenance and conformance evidence | Document revisions and sections, source hashes, source availability and reuse terms, model/tool versions, test provenance, hardware identity, coverage, unresolved discrepancies | Which evidence supports this exact behavioral claim? |
| C24 | Model operation and reproducibility | Embedding API, controlled stepping, stop reasons, traces, event recording, snapshots, compatibility versioning, deterministic seed policy, resource limits, performance measurements | Can a failing run be reconstructed after the model has changed? |

C17 spans CPU state and environment time; its collection must be checked against C19 and the CPU/environment contract.

C19–C21 are not all properties of the CPU itself. They are necessary to define the environment in which software observes the CPU. Intel's own manuals separate basic architecture, instruction reference, system programming, and model-specific registers; this is a useful illustration of why an opcode reference alone is insufficient. See [Intel SDM overview](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html).

## 5 Collection questions specific to DSPs

For each DSP target, explicitly investigate these points even if the final answer is “absent”:

1. What are the operand, product, accumulator, guard, and output widths?
2. Which fractional formats exist, and where is scaling applied?
3. Is rounding applied before or after accumulation, saturation, and narrowing?
4. Is saturation per operation, per lane, or only at a later transfer?
5. Which sticky flags survive later operations, interrupts, and context switches?
6. Are instruction and data addresses expressed in the same units?
7. How do multiple memory spaces and address generators interact?
8. Which modulo, circular, strided, and bit-reversed modes are supported?
9. Which operations share an issue group, and when are their operands observed?
10. Are results delayed, bypassed, or interlocked? What happens on an early read?
11. What is the architectural status of resource conflicts or illegal packets?
12. How do repeats and hardware loops interact with interrupts and exceptions?
13. Can a single instruction issue multiple memory accesses or computations?
14. What are the required ordering rules for DMA, buffers, mailboxes, and stream I/O?
15. Which compiler-generated prologues, epilogues, and runtime helpers depend on special state?

These are framework requirements to investigate across targets, not a claim that every DSP implements every listed feature.

## 6 Information that must not be conflated

| Distinction | Consequence |
|---|---|
| CPU ISA versus platform | An accurate CPU alone cannot promise to boot arbitrary board firmware. |
| Instruction semantics versus ABI | The ABI belongs to the software environment; keep CPU instructions independent of one calling convention. |
| Algorithmic DSP function versus processor execution | Reproducing an FFT mathematically does not establish that the DSP machine code executes correctly. |
| Mathematical arithmetic versus target arithmetic | Intermediate truncation, saturation, or fusion can change final bits. |
| Host execution versus guest execution | Host endianness, integer behavior, floating-point defaults, and thread scheduling cannot define the target accidentally. |
| Known absent versus unimplemented | An instruction absent from the target may trap; an instruction missing from the model is a model limitation. |
| Architecturally unspecified versus not yet researched | The former has a specification-defined meaning; the latter is a project evidence gap. |
| Functional cache effects versus cache performance | Data visibility and maintenance may be required even when cache-hit timing is omitted. |


# CPU/environment contract — v0.2

## 1. Purpose and ownership

The CPU is validated under explicit environment assumptions. The laboratory and later board must demonstrate that they satisfy those assumptions. This is a conditional composition claim, not a claim that a CPU is correct under every possible device response.

The contract has its own ID, version, requirement catalog, parameters, legal-event rules, and tests. Scalar configuration fields do not express all obligations: ordering, temporal rules, and relationships between responses must also be enumerable named requirements.

Every entry identifies its authority: processor specification, chosen implementation parameter, platform specification, or explicitly synthetic laboratory policy. Laboratory policy cannot override an architectural requirement.

## 2. Boundary inventory

| Boundary item | CPU obligation | Environment obligation | Check |
|---|---|---|---|
| Fetch | Request architecturally needed instruction units under correct mode and permissions | Supply bytes/units or specified failure with matching address-space attributes | Boundary crossing, alignment, no extraneous side-effecting fetch |
| Data access | Calculate target addresses and apply architectural priority/ordering | Honor widths, attributes, access responses, and permitted side effects | Fault/no-fault pairs, split-access order |
| Translation/protection | Implement selected MMU/MPU/CSR semantics and permitted walk effects | Provide memory and physical attributes used by walks | Permission combinations, A/D effects or source-required traps |
| Interrupts | Apply masks, priority, acceptance and return rules | Supply configured source state and legal event ordering | Eligible/ineligible boundaries, pending/clear, nesting |
| Counter input | Apply architectural access/width/state rules | Supply values and progress under declared virtual-time policy | Wrap, monotonicity where required, mode gating, idle wake |
| Reservations | Maintain selected architectural reservation semantics | Report external invalidation events required by the selected contract | Success/failure, overlap, external write and context cases |
| Reset | Enter required state and handle retained/pending state | Order reset events and provide specified reset inputs | Cold/warm reset fixtures where supported |
| Waiting | Suspend/continue under target rules | Allow eligible external events to progress while the CPU waits | Timer/interrupt wake without CPU retirement |
| Code visibility | Apply architectural instruction visibility and invalidation rules | Maintain coherent/noncoherent storage behavior as declared | Rewrite code, synchronization, cache/version invalidation |
| Partial progress | Expose defined commits, exception and restart state | Preserve already issued external effects as required | Fault injected after the Nth suboperation |

Some entries, such as page-walk A/D policy and reservation behavior, have architecture-constrained choices rather than unrestricted environment knobs. Each parameter must be validated against the selected extensions and specification revision.

## 3. Minimum record structure

Use the supplied `contract-obligation.schema.json` starter schema. Each record includes ID, contract/profile identity, direction (`assumption` or `guarantee`), statement, authority, source locators, parameters, dependencies, and required checks.

Represent units and event boundaries explicitly: memory address units, access widths in target bits, virtual-time domain, permitted event delivery point, and ordering constraints. A source phrase such as “eventually” requires the chosen fairness/progress assumptions and its evidence method, not an arbitrary fixed test timeout.

The complete manifest is derived from the contract records. Export an assumption inventory for each profile. Generate reference configurations from a reviewed mapping and report unmapped or unsupported fields; a successful config diff does not validate the implementation of the harness.

## 4. How to validate the laboratory

1. Test requests and responses against contract properties independently of the CPU instruction handler.
2. Feed controlled equivalent response schedules to the model and reference where their interfaces allow it.
3. Verify the adapter's state mapping, address units, event positioning, and normalization using separate fixtures.
4. Retain negative fixtures that must be reported as contract violations rather than target exceptions.
5. Inject one changed environmental response and confirm the expected architectural effect changes.
6. Run actual matched-profile reference smoke tests, including a failure/event case rather than only arithmetic.

If a reference cannot expose a needed event or fault boundary, record the gap and use an alternative specified evidence method. Do not claim arbitrary injection equivalence merely because both programs can execute an ELF file.

## 5. Board composition gate

For every CPU assumption, identify the board/device guarantee satisfying it or reject the composition. Check reset wiring, memory attributes, source priorities, counter units, time progress, access side effects, reservation invalidations, and instruction visibility. Reuse the interface tests against the board provider where meaningful.

When Linux reveals a seam error, classify its owner, reduce the failing interaction, amend the responsible contract or implementation, invalidate affected evidence, and rerun the relevant CPU/device/composition gates. The original CPU-first ordering is preserved because all board code still follows the accepted CPU profile.

## 6. Timing and concurrency

There are distinct obligations for target-visible sequencing, timer scheduling, and implementation-performance prediction. A DSP's delayed result can be part of functional semantics even without a physically timed memory hierarchy. Time-based devices need progress when no instruction retires.

Initial single-core laboratory execution is deterministic under recorded inputs. Later multicore requires explicit atomicity, memory ordering, reservations, and fairness. A stronger execution model may yield a legal subset of architectural outcomes, but coverage of all weaker outcomes is a separate claim requiring its own exploration method and corpus.

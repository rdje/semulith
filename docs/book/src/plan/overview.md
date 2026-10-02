# Milestones and their dependencies

The plan is a dependency graph, not a schedule. No elapsed-time estimate is attached to any
node, because the facts that would make an estimate meaningful — how a specification reads
under scrutiny, whether a reference model can actually be driven, how long discrepancy
reduction takes — do not exist yet. They are produced by P0 and P1.

Every node, what it requires, and what it closes. A row's *requires* column is the whole of
its incoming edges — there are no implied prerequisites.

| Milestone | Requires | Gate | What that gate closes |
| --- | --- | --- | --- |
| **P0** profile and evidence access | — | `G0` | foundational semantics resolved; an actual evidence path works; profile/reference differences enumerated |
| **P1** processor laboratory | P0 | `G1` | failures replay; model limitations are distinguishable from target traps; malformed evidence links are rejected; the baseline is measured |
| **D** DSP specification and stress review | P1 | — | discriminating real-spec cases reviewed; synthetic stress fixtures executable |
| **P2** validated RV64I profile | P1 | `CPU-LAB` | the selected scalar profile passes the full processor gate |
| **P3** shared interfaces and a real DSP slice | P2, D | `BREADTH` | the stated real DSP subset has evidence; the public abstraction supports the exercised cases |
| **A** stable cross-architecture API | P3 | — | the claim P3 authorises; unsupported families stay unclaimed |
| **P4** Linux CPU profile | P2 | `CPU-SYSTEM` | the complete declared profile passes, including its environment contract |
| **G** CPU release | P4 | *the processor gate itself* | authorises board implementation |
| **P5** board model | G | `BOARD` | devices and composition pass; the board satisfies every CPU assumption |
| **AG** archogen OS integration | P5 | `ARCHOGEN-OS` | a pinned generated OS boots and completes its declared functional suite |
| **P6** Linux userspace | P5 | `LINUX` | reproducible cold boot to `init` and a shell, a guest program, timer-driven scheduling, a documented shutdown |
| **P7** headless computer | P6 | `SYSTEM` | the declared headless workload suite; storage persists; snapshot/restore preserves relevant state |
| **MC** multicore CPU | G | *its own gate* | memory model, atomicity, reservations, event delivery, progress — revalidated |
| **SMP** SMP Linux | P7, MC | — | a later integration test, never the evidence for MC |

The same graph appears in `ROADMAP.md` §6 as a Mermaid diagram, which renders on GitHub. This
table is its exact edge list.


## What the arrows mean

An arrow is a *work* dependency: the target cannot be honestly completed before the source.
It is not an instruction to run several efforts in parallel, and it is not a claim that the
graph is the only order that would work.

Two edges are worth reading carefully:

- **`P1 → D` and `D → P3`.** The DSP path gates a claim of a *stable cross-architecture API*.
  It does **not** block architecture-specific CPU progress toward Linux. The point of pulling
  DSP work early is that scalar-CPU-shaped abstractions quietly bake in assumptions — uniform
  operand widths, one address space, instruction-level atomicity — which a real DSP violates,
  and discovering that after an API is published is expensive.
- **`G → P5`, not `P2 → P5`.** Board work follows the *CPU release gate* for the profile it
  uses. A smaller accepted profile can support an earlier board branch (see the archogen
  route), but never an unaccepted one.

## Reading the gates

A kernel banner is not `LINUX`. A boot is not `CPU-SYSTEM`. Each gate closes exactly what it
says and nothing adjacent.

# Semulith

**Semulith builds trustworthy CPU and DSP software models in Rust, then composes validated
processor profiles into boards and complete computers capable of running Linux.** The first
deliverable is the processor: one canonical executable definition, a reference interpreter,
and reproducible evidence for a precisely stated supported profile.

Semulith also has a concrete consumer: **archogen**, which generates specific-purpose
operating systems from its eADL source of truth and needs explicit platform contracts to
execute and validate them against.

> **Claim scope.** No CPU implementation, conformance result, or accepted processor profile
> is claimed. `schemas/` and `examples/` are data-contract starters whose evidence records
> are deliberately `planned`. *Semulith* is a proposed name; no crate, repository, domain, or
> trademark has been reserved. See [`LIVE_STATUS.md`](LIVE_STATUS.md) for what is actually built.

## Start here

| Read | For |
| --- | --- |
| [`ROADMAP.md`](ROADMAP.md) | direction, decisions, milestones P0–P7, dependency graph, acceptance gates |
| [`RULES.md`](RULES.md) | the short normative engineering rules, with stable IDs |
| [`docs/`](docs/) | the detailed contracts — architecture, evidence and gates, CPU/environment, archogen |
| [`CLAUDE.md`](CLAUDE.md) · [`AGENTS.md`](AGENTS.md) | the agent bootstrap: how work is tracked, evidenced, and committed here |
| [`docs/book/`](docs/book/) | the mdBook — the reviewable narrative surface |

## Layout

| Path | What lives there |
| --- | --- |
| `crates/` | the Rust workspace |
| `schemas/` · `examples/` | starter data contracts and their synthetic, explicitly planned fixtures |
| `docs/tasks/` · [`docs/TASK_TREE.md`](docs/TASK_TREE.md) | task-trees — every change is owned by a leaf **before** it is made |
| [`docs/decisions/`](docs/decisions/) | durable cross-cutting decisions and facts (memory layer C) |
| `docs/provenance/` | frozen delivery records for supplied design inputs |
| `scripts/` · `.githooks/` · `.github/workflows/` | the mechanical doctrine enforcement |

## Commands

| Command | Does |
| --- | --- |
| `make gate` | run the doctrine enforcer — also the pre-commit hook and CI |
| `make check` | `cargo fmt --check` + `clippy -D warnings` + `cargo test --all` |
| `make book` | build the mdBook |
| `make hooks` | activate the git hooks once per clone (`core.hooksPath=.githooks`) |

## How this repository works

- **Nothing changes without a task-tree leaf first.** The leaf carries the goal, the
  acceptance checklist, the evidence, and the commit — see [`docs/TASK_TREE.md`](docs/TASK_TREE.md).
- **Durable memory is four layers**: [`MEMORY.md`](MEMORY.md) (resume pointer) ·
  `docs/tasks/` (work) · [`docs/decisions/`](docs/decisions/) (facts) · git (history).
  Defined in [`MEMORY_ARCHITECTURE.md`](MEMORY_ARCHITECTURE.md).
- **Diagnose tools-first** ([`TOOLBOX.md`](TOOLBOX.md)), commit per [`COMMIT.md`](COMMIT.md),
  and expect every mechanizable rule to be gated ([`DOCTRINE_ENFORCEMENT.md`](DOCTRINE_ENFORCEMENT.md)).
- **Evidence is a claim with named legs.** A number is checked when it is *re-derived*,
  *falsified*, and *durable* — [`docs/CLAIM_VERIFICATION.md`](docs/CLAIM_VERIFICATION.md).
  Finite testing is tested evidence, never universal proof, and a reference that shares an
  ancestor is not a second opinion — [`docs/EVIDENCE_AND_GATES.md`](docs/EVIDENCE_AND_GATES.md).

This landing page is governed by [`README_POLICY.md`](README_POLICY.md) and mechanically
capped on **both** line and byte count. Route changing detail to its canonical home above
rather than growing this file.

## License

Dual-licensed under MIT or Apache-2.0.
